---
name: vercel-deploy-preflight
description: >
  Pre-deploy gate for Vercel. Run BEFORE every Vercel deploy (git push to a
  connected repo, `vercel`, `vercel --prod`, or clicking Deploy) to catch the
  things that make Vercel email "Deployment has failed" — build errors, missing
  env vars, case-sensitive import breaks, out-of-sync lockfile, wrong Node
  version, devDependency needed at build time. Reproduces Vercel's build locally
  first so a green local run == a green Vercel run. Triggers: "deploy", "ship
  it", "push to prod", "vercel", "deployment failed", "why did my deploy fail",
  plus the deploy-intent hook fires it automatically.
risk: safe
date_added: 2026-09-01
---

# Vercel Deploy Preflight

**Goal:** never let a deploy fail on Vercel. Vercel builds on clean Linux with
only `dependencies` + committed lockfile. Most failures are things that "work on
my machine". This skill reproduces that environment locally and checks parity.

## When to run

Automatically before ANY of: `git push` on a Vercel-connected repo, `vercel`,
`vercel --prod`, `vercel deploy`, or the user says deploy / ship / go live.
Also run it in reverse when a deploy already failed — same checks find the cause.

## The one command

```bash
python "$HOME/.claude/skills/vercel-deploy-preflight/preflight.py"
```

Run it from the project root. It exits non-zero and prints exactly what will
break if anything is wrong. If it passes, the deploy is safe — proceed.

## What it checks (and why each one fails Vercel)

1. **Clean production build** — `rm -rf node_modules .next && npm ci && npm run build`
   (or the detected package manager / framework build). This is the single
   highest-value check: Vercel does exactly this. TS errors, ESLint errors
   (Next fails the build on these by default), broken imports all surface here.
2. **Lockfile in sync & committed** — `npm ci` fails hard if `package-lock.json`
   doesn't match `package.json`. Also checks the lockfile isn't gitignored /
   uncommitted.
3. **Case-sensitive imports** — `import './Button'` when the file is `button.tsx`
   works on Windows/macOS, fails on Vercel's Linux. Scans for import paths whose
   case doesn't match the real filename.
4. **Env var parity** — collects every `process.env.X` / `import.meta.env.X` in
   source, diffs against `.env` / `.env.local` / `.env.example`, and lists vars
   that must exist in the Vercel dashboard. Missing `NEXT_PUBLIC_*` at build
   time = broken build or broken runtime.
5. **Build-time deps in the right place** — anything imported by
   `next.config.*`, `*.config.*`, or non-lazy server code that lives in
   `devDependencies` will be absent on Vercel (`NODE_ENV=production` prune).
6. **Node version pin** — warns if there's no `engines.node` in package.json or
   `.nvmrc`; Vercel's default Node may differ from yours.
7. **Uncommitted changes** — you're about to deploy what's committed, not what's
   on disk. Lists the diff so there's no surprise.
8. **Migrations in the build script without an env guard** — a build/`vercel-build`
   script that runs `prisma migrate deploy` / `migrate deploy` / `db push` with
   no `VERCEL_ENV === 'production'` (or `NODE_ENV`) gate. Preview deploys then
   either crash on a missing prod DB URL or, worse, mutate the prod schema from
   a branch. Previews should compile-only.

## If a check fails

Fix the root cause, don't skip. The checklist maps 1:1 to a Vercel failure
email — a green preflight is the whole point. Re-run until clean, then deploy.

## Lessons logged (real failures this skill now guards against)

- **2026-09-01 · ostazi-api** — every *preview* build failed in ~6s:
  `TypeError: Invalid URL` from `new URL(process.env.DATABASE_URL)` in the
  `vercel-build` script. `DATABASE_URL` was set for the **Production** scope
  only, so preview/branch deploys had it undefined. Two root causes: (a) env
  var not set for all scopes it's used in — check #4; (b) the build script ran
  `prisma migrate deploy` unconditionally, which must NEVER run from a preview
  branch against the shared prod DB. Fix pattern: gate on
  `process.env.VERCEL_ENV === 'production'` — previews compile-only, skip
  migrations; a missing prod env var fails loud instead of with an opaque error.
  → check #8 below now flags migrate-on-every-build.

## Notes

- Framework auto-detected: Next.js, Vite, Astro, SvelteKit, CRA, plain node.
- Monorepo: run from the app subdirectory, or pass `--dir apps/web`.
- `--fast` skips the full clean rebuild (checks 2-7 only) for a quick sanity
  pass; never use `--fast` as the final gate before `--prod`.
