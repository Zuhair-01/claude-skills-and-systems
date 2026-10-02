#!/usr/bin/env python3
"""Vercel deploy preflight. Reproduces Vercel's Linux build locally + parity checks.
Exit 0 = safe to deploy. Non-zero = will (probably) fail on Vercel, reason printed.

Usage:
  python preflight.py [--dir PATH] [--fast]
    --dir   project/app root (default: cwd)
    --fast  skip the clean rebuild (checks 2-7 only); NOT valid as the final --prod gate
"""
import argparse, json, os, re, subprocess, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path

FAILS, WARNS = [], []


def fail(m): FAILS.append(m)
def warn(m): WARNS.append(m)


def run(cmd, cwd, timeout=900):
    try:
        p = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str),
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 1, f"timed out after {timeout}s"
    except FileNotFoundError as e:
        return 127, str(e)


def detect_pm(root):
    if (root / "pnpm-lock.yaml").exists(): return "pnpm"
    if (root / "yarn.lock").exists(): return "yarn"
    if (root / "bun.lockb").exists(): return "bun"
    return "npm"


def git(args, root):
    return run(["git"] + args, root)


# ---- check 2: lockfile ------------------------------------------------------
def check_lockfile(root, pm):
    lf = {"npm": "package-lock.json", "pnpm": "pnpm-lock.yaml",
          "yarn": "yarn.lock", "bun": "bun.lockb"}[pm]
    p = root / lf
    if not p.exists():
        fail(f"no {lf} - Vercel needs a committed lockfile for reproducible installs")
        return
    rc, out = git(["check-ignore", lf], root)
    if rc == 0:
        fail(f"{lf} is gitignored - Vercel won't see it")
    rc, out = git(["ls-files", "--error-unmatch", lf], root)
    if rc != 0:
        fail(f"{lf} is not committed - commit it before deploying")
    rc, out = git(["status", "--porcelain", lf], root)
    if out.strip():
        fail(f"{lf} has uncommitted changes - run install, then commit the lockfile")


# ---- check 6: node version -------------------------------------------------
def check_node(root, pkg):
    if (root / ".nvmrc").exists():
        return
    if pkg.get("engines", {}).get("node"):
        return
    warn("no engines.node in package.json and no .nvmrc - Vercel picks its default "
         "Node major, which may differ from yours. Pin it.")


# ---- check 7: uncommitted -------------------------------------------------
def check_dirty(root):
    rc, out = git(["status", "--porcelain"], root)
    if out.strip():
        warn("uncommitted changes - you deploy what's committed, not what's on disk:\n"
             + "\n".join("    " + l for l in out.strip().splitlines()[:20]))


# ---- check 3: case-sensitive imports ------------------------------------
IMPORT_RE = re.compile(r"""(?:import|require)\s*(?:\([^)]*|[^'"]*)['"](\.[^'"]+)['"]""")
EXTS = ["", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json"]


def check_case(root):
    src_files = []
    for ext in ("ts", "tsx", "js", "jsx", "mjs"):
        src_files += list(root.rglob(f"*.{ext}"))
    src_files = [f for f in src_files if "node_modules" not in f.parts
                 and ".next" not in f.parts and "dist" not in f.parts]
    problems = []
    for f in src_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in IMPORT_RE.finditer(text):
            spec = m.group(1)
            base = (f.parent / spec).resolve()
            for ext in EXTS:
                cand = Path(str(base) + ext)
                if cand.exists():
                    # verify real on-disk case matches
                    try:
                        real = cand.resolve()
                        parent = real.parent
                        actual = next((x.name for x in parent.iterdir()
                                       if x.name.lower() == real.name.lower()), None)
                        if actual and actual != real.name:
                            problems.append(f"{f.name}: import '{spec}' resolves to "
                                            f"'{actual}' (case mismatch - fails on Linux)")
                    except Exception:
                        pass
                    break
            else:
                if (base.is_dir() or Path(str(base)).exists()):
                    continue
    for p in dict.fromkeys(problems):
        fail(p)


# ---- check 4: env var parity -------------------------------------------
ENV_RE = re.compile(r"(?:process\.env|import\.meta\.env)\.([A-Z0-9_]+)")


def load_env_keys(p):
    keys = set()
    if p.exists():
        for line in p.read_text(errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                keys.add(line.split("=", 1)[0].strip())
    return keys


def check_env(root):
    used = set()
    for ext in ("ts", "tsx", "js", "jsx", "mjs"):
        for f in root.rglob(f"*.{ext}"):
            if any(x in f.parts for x in ("node_modules", ".next", "dist")):
                continue
            try:
                used |= set(ENV_RE.findall(f.read_text(errors="ignore")))
            except Exception:
                pass
    BUILTIN = {"NODE_ENV", "VERCEL", "VERCEL_ENV", "VERCEL_URL", "VERCEL_REGION",
               "CI", "PORT", "npm_package_version", "NEXT_RUNTIME"}
    used -= BUILTIN
    local = (load_env_keys(root / ".env") | load_env_keys(root / ".env.local")
             | load_env_keys(root / ".env.production") | load_env_keys(root / ".env.example"))
    missing = sorted(used - local)
    if missing:
        warn("env vars referenced in code but not in any local .env - confirm each "
             "exists in the Vercel dashboard (Project -> Settings -> Environment Variables):\n"
             + "\n".join("    " + k for k in missing))


# ---- check 5: build-time deps in devDependencies ----------------------
def check_migrate_guard(root, pkg):
    scripts = pkg.get("scripts", {})
    build_blob = " ".join(scripts.get(k, "") for k in ("build", "vercel-build", "postinstall"))
    referenced = re.findall(r"node\s+([^\s&|]+\.[cm]?js)", build_blob)
    files_to_scan = [root / f for f in referenced if (root / f).exists()]
    MIG = re.compile(r"migrate\s+deploy|db\s+push|prisma\s+migrate")
    GUARD = re.compile(r"VERCEL_ENV|NODE_ENV")
    for blob, label in [(build_blob, "package.json build scripts")] + \
            [(_read(f), f.name) for f in files_to_scan]:
        if MIG.search(blob) and not GUARD.search(blob):
            warn(f"{label} runs DB migrations with no VERCEL_ENV/NODE_ENV guard - "
                 "preview deploys will run them against prod (or crash on a missing "
                 "prod DB URL). Gate on process.env.VERCEL_ENV === 'production'.")


def _read(p):
    try:
        return p.read_text(errors="ignore")
    except Exception:
        return ""


def check_build_deps(root, pkg):
    dev = set(pkg.get("devDependencies", {}))
    if not dev:
        return
    config_files = [p for p in root.glob("*.config.*")] + \
                   [p for p in root.glob("next.config.*")]
    hit = set()
    imp_re = re.compile(r"""(?:from|require\()\s*['"]([^'".][^'"]*)['"]""")
    for cf in config_files:
        try:
            for m in imp_re.finditer(cf.read_text(errors="ignore")):
                pkg_name = m.group(1)
                top = pkg_name.split("/")[0] if not pkg_name.startswith("@") \
                    else "/".join(pkg_name.split("/")[:2])
                if top in dev:
                    hit.add((cf.name, top))
        except Exception:
            pass
    for cf, dep in sorted(hit):
        warn(f"{cf} imports '{dep}' which is in devDependencies - Vercel prunes "
             f"those in production builds. Move it to dependencies if the build needs it.")


# ---- check 8: vercel.json shape --------------------------------------
# 2026-09-13 incident: functions.*.includeFiles set to an array of two
# globs (to cover two node_modules paths) fails Vercel's config schema --
# it accepts only a single glob STRING there. This isn't a build failure,
# it's a "Schema verification failed" deploy-time rejection that never even
# reaches the build step, so check_build's local rebuild can't catch it.
# Confirmed live: 3 straight production deploys silently ● Error'd on this
# while the site kept serving a stale build. Combine multiple paths with
# brace-expansion in one string instead: "node_modules/{a,b}/**".
def check_vercel_json(root):
    for candidate in [root / "vercel.json", root.parent / "vercel.json"]:
        if not candidate.exists():
            continue
        try:
            cfg = json.loads(candidate.read_text(errors="ignore"))
        except Exception as e:
            fail(f"{candidate.name} is not valid JSON: {e}")
            return
        for fn_name, fn_cfg in (cfg.get("functions") or {}).items():
            if isinstance(fn_cfg, dict) and isinstance(fn_cfg.get("includeFiles"), list):
                fail(f"{candidate.name}: functions.\"{fn_name}\".includeFiles is an array -- "
                     "Vercel's schema only accepts a single glob string there. Combine paths "
                     "with brace-expansion, e.g. \"node_modules/{a,b}/**\", or deploys will "
                     "fail schema validation before the build even starts.")
        return


# ---- check 1: clean production build ----------------------------------
def check_build(root, pm, pkg):
    scripts = pkg.get("scripts", {})
    if "build" not in scripts:
        warn("no build script in package.json - skipping clean-build check "
             "(if this is a static/no-build project, that's fine)")
        return
    print("  running clean production build (this is the slow one)...", flush=True)
    for d in ("node_modules", ".next", "dist", ".vercel/output"):
        run(f'rm -rf "{d}"', root)
    install = {"npm": "npm ci", "pnpm": "pnpm i --frozen-lockfile",
               "yarn": "yarn install --frozen-lockfile",
               "bun": "bun install --frozen-lockfile"}[pm]
    rc, out = run(install, root)
    if rc != 0:
        fail(f"`{install}` failed - lockfile likely out of sync with package.json:\n"
             + tail(out))
        return
    env = dict(os.environ, NODE_ENV="production", CI="1", VERCEL="1", VERCEL_ENV="production")
    try:
        p = subprocess.run(f"{pm} run build", cwd=root, shell=True,
                           capture_output=True, text=True, timeout=1200, env=env)
        rc, out = p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        rc, out = 1, "build timed out after 1200s"
    if rc != 0:
        fail("production build FAILED - this is exactly what Vercel will do:\n" + tail(out))
    else:
        print("  clean build passed.", flush=True)


def tail(s, n=40):
    lines = s.strip().splitlines()
    return "\n".join("    " + l for l in lines[-n:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    root = Path(a.dir).resolve()
    if not (root / "package.json").exists():
        print(f"no package.json in {root} - pass --dir to the app root", file=sys.stderr)
        sys.exit(2)
    pkg = json.loads((root / "package.json").read_text(errors="ignore"))
    pm = detect_pm(root)
    print(f"vercel-deploy-preflight  dir={root}  pm={pm}  mode={'fast' if a.fast else 'full'}")

    rc, _ = git(["rev-parse", "--is-inside-work-tree"], root)
    is_git = rc == 0

    if is_git:
        check_lockfile(root, pm)
        check_dirty(root)
    check_node(root, pkg)
    check_case(root)
    check_env(root)
    check_build_deps(root, pkg)
    check_migrate_guard(root, pkg)
    check_vercel_json(root)
    if not a.fast:
        check_build(root, pm, pkg)
    else:
        warn("--fast: skipped the clean rebuild. Do a full run before `vercel --prod`.")

    print()
    for w in WARNS:
        print("WARN  " + w)
    for f in FAILS:
        print("FAIL  " + f)
    print()
    if FAILS:
        print(f"NOT SAFE TO DEPLOY - {len(FAILS)} blocking issue(s). Fix the root cause, re-run.")
        sys.exit(1)
    if WARNS:
        print(f"Deploy likely OK - {len(WARNS)} warning(s) above, review them.")
    else:
        print("All checks passed. Safe to deploy.")
    sys.exit(0)


if __name__ == "__main__":
    main()
