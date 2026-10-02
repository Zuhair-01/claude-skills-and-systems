#!/usr/bin/env python3
"""B-roll: search the local library first, then free professional sources; download,
tag, and keep everything in one growing manifest.

Library (shared across every project — never per-project):
  Second_Brain/Workflow/30 - Resources/Broll_Library/{manifest.json, clips/}
  override with env BROLL_LIB

Subcommands:
  find    "concept"                       search the LOCAL library (always do this first)
  search  "concept" [--n 8] [--portrait]  search remote sources, print candidates
  get     URL --tags a,b [--concept c]    download a candidate into the library
  register FILE --tags a,b --source s --license l   add a manually-downloaded clip
  stats                                   what the library holds

Sources: Pexels + Pixabay (free API keys, env PEXELS_API_KEY / PIXABAY_API_KEY),
Internet Archive + Wikimedia Commons + NASA (keyless). See references/broll_sources.md.
"""
import argparse, hashlib, json, os, re, sys, urllib.parse, urllib.request

LIB = os.environ.get("BROLL_LIB") or os.path.expanduser(
    r"~/Desktop/Empire_Base/Second_Brain/Workflow/30 - Resources/Broll_Library")
CLIPS = os.path.join(LIB, "clips")
MANIFEST = os.path.join(LIB, "manifest.json")
UA = {"User-Agent": "style-clone/1.0 (personal editing pipeline)"}


def load():
    os.makedirs(CLIPS, exist_ok=True)
    return json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else []


def save(m):
    json.dump(m, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


# ---------------- remote sources ----------------

def pexels(q, n, portrait):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    u = ("https://api.pexels.com/videos/search?query=" + urllib.parse.quote(q) +
         f"&per_page={n}&size=medium" + ("&orientation=portrait" if portrait else ""))
    try:
        d = get_json(u, {"Authorization": key})
    except Exception as e:
        print(f"  pexels: {e}", file=sys.stderr)
        return []
    out = []
    for v in d.get("videos", []):
        files = sorted(v.get("video_files", []), key=lambda f: -(f.get("width") or 0))
        best = next((f for f in files if (f.get("width") or 0) <= 2160), files[0] if files else None)
        if not best:
            continue
        out.append({"source": "pexels", "url": best["link"], "page": v.get("url"),
                    "w": best.get("width"), "h": best.get("height"),
                    "duration": v.get("duration"), "author": (v.get("user") or {}).get("name"),
                    "license": "Pexels License (no attribution required)"})
    return out


def pixabay(q, n, portrait):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return []
    u = (f"https://pixabay.com/api/videos/?key={key}&q=" + urllib.parse.quote(q) +
         f"&per_page={max(3, n)}")
    try:
        d = get_json(u)
    except Exception as e:
        print(f"  pixabay: {e}", file=sys.stderr)
        return []
    out = []
    for v in d.get("hits", []):
        vs = v.get("videos", {})
        best = vs.get("large") or vs.get("medium") or vs.get("small") or {}
        if not best.get("url"):
            continue
        if portrait and (best.get("width") or 0) > (best.get("height") or 1):
            continue
        out.append({"source": "pixabay", "url": best["url"], "page": v.get("pageURL"),
                    "w": best.get("width"), "h": best.get("height"),
                    "duration": v.get("duration"), "author": v.get("user"),
                    "license": "Pixabay Content License (no attribution required)"})
    return out


def archive_org(q, n, portrait):
    u = ("https://archive.org/advancedsearch.php?q=" +
         urllib.parse.quote(f'{q} AND mediatype:(movies)') +
         "&fl[]=identifier&fl[]=title&fl[]=licenseurl&rows=" + str(n) + "&output=json")
    try:
        d = get_json(u)
    except Exception as e:
        print(f"  archive: {e}", file=sys.stderr)
        return []
    return [{"source": "archive.org", "url": f"https://archive.org/details/{h['identifier']}",
             "page": f"https://archive.org/details/{h['identifier']}",
             "title": h.get("title"), "license": h.get("licenseurl") or "check on page",
             "note": "resolve the actual .mp4 via the details page or yt-dlp"}
            for h in d.get("response", {}).get("docs", [])]


def wikimedia(q, n, portrait):
    u = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
         "&gsrnamespace=6&gsrlimit=" + str(n) + "&gsrsearch=" +
         urllib.parse.quote(f"filetype:video {q}") +
         "&prop=imageinfo&iiprop=url|size|extmetadata")
    try:
        d = get_json(u)
    except Exception as e:
        print(f"  wikimedia: {e}", file=sys.stderr)
        return []
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii.get("url"):
            continue
        lic = ((ii.get("extmetadata") or {}).get("LicenseShortName") or {}).get("value", "check")
        out.append({"source": "wikimedia", "url": ii["url"], "page": ii.get("descriptionurl"),
                    "w": ii.get("width"), "h": ii.get("height"),
                    "license": lic + " (attribution usually required)"})
    return out


def nasa(q, n, portrait):
    u = "https://images-api.nasa.gov/search?media_type=video&q=" + urllib.parse.quote(q)
    try:
        d = get_json(u)
    except Exception as e:
        print(f"  nasa: {e}", file=sys.stderr)
        return []
    return [{"source": "nasa", "url": it.get("href"), "page": it.get("href"),
             "title": (it.get("data") or [{}])[0].get("title"),
             "license": "Public domain (NASA)",
             "note": "href is a collection.json — pick the largest .mp4 inside"}
            for it in d.get("collection", {}).get("items", [])[:n]]


SOURCES = [pexels, pixabay, archive_org, wikimedia, nasa]


# ---------------- library ops ----------------

def cmd_find(a):
    m, q = load(), a.concept.lower()
    terms = [t for t in re.split(r"[\s,]+", q) if t]
    hits = []
    for c in m:
        hay = " ".join([c.get("concept") or ""] + c.get("tags", []) + [c.get("title") or ""]).lower()
        score = sum(1 for t in terms if t in hay)
        if score:
            hits.append((score, c))
    hits.sort(key=lambda x: -x[0])
    print(json.dumps([c for _, c in hits[:a.n]], ensure_ascii=False, indent=1))
    if not hits:
        print(f"# nothing local for '{a.concept}' — run: broll.py search \"{a.concept}\"",
              file=sys.stderr)


def cmd_search(a):
    have = {k: bool(os.environ.get(k)) for k in ("PEXELS_API_KEY", "PIXABAY_API_KEY")}
    if not any(have.values()):
        print("# no PEXELS_API_KEY / PIXABAY_API_KEY set — modern lifestyle footage will be "
              "thin. Both are free: pexels.com/api, pixabay.com/api/docs\n", file=sys.stderr)
    res = []
    for fn in SOURCES:
        r = fn(a.concept, a.n, a.portrait)
        for x in r:
            x["concept"] = a.concept
        res += r
    print(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"\n# {len(res)} candidates. Eyeball before downloading — "
          f"apply the fit test in references/broll_sources.md.", file=sys.stderr)


def cmd_get(a):
    m = load()
    tmp = os.path.join(CLIPS, "_dl.tmp")
    req = urllib.request.Request(a.url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        while True:
            b = r.read(1 << 16)
            if not b:
                break
            f.write(b)
    sha = hashlib.sha1(open(tmp, "rb").read()).hexdigest()[:16]
    dest = os.path.join(CLIPS, sha + ".mp4")
    if os.path.exists(dest):
        os.remove(tmp)
        print(f"already in library: {dest}")
        return
    os.rename(tmp, dest)
    entry = {"sha": sha, "path": dest, "concept": a.concept or "",
             "tags": [t.strip() for t in (a.tags or "").split(",") if t.strip()],
             "source": a.source or urllib.parse.urlparse(a.url).netloc,
             "src_url": a.url, "license": a.license or "UNVERIFIED — fill this in",
             "orientation": a.orientation, "title": a.title or ""}
    m.append(entry)
    save(m)
    print(json.dumps(entry, ensure_ascii=False, indent=1))


def cmd_register(a):
    m = load()
    sha = hashlib.sha1(open(a.file, "rb").read()).hexdigest()[:16]
    dest = os.path.join(CLIPS, sha + os.path.splitext(a.file)[1])
    if not os.path.exists(dest):
        with open(a.file, "rb") as s, open(dest, "wb") as d:
            d.write(s.read())
    m = [c for c in m if c.get("sha") != sha]
    m.append({"sha": sha, "path": dest, "concept": a.concept or "",
              "tags": [t.strip() for t in (a.tags or "").split(",") if t.strip()],
              "source": a.source or "manual", "src_url": a.src_url or "",
              "license": a.license or "UNVERIFIED — fill this in",
              "orientation": a.orientation, "title": a.title or ""})
    save(m)
    print(f"registered {sha} -> {dest}")


def cmd_stats(a):
    m = load()
    tags = {}
    for c in m:
        for t in c.get("tags", []):
            tags[t] = tags.get(t, 0) + 1
    print(f"{len(m)} clips in {LIB}")
    print("unverified licences:", sum(1 for c in m if "UNVERIFIED" in (c.get("license") or "")))
    for t, n in sorted(tags.items(), key=lambda x: -x[1])[:30]:
        print(f"  {n:3}  {t}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find"); f.add_argument("concept"); f.add_argument("--n", type=int, default=8)
    f.set_defaults(fn=cmd_find)

    s = sub.add_parser("search"); s.add_argument("concept"); s.add_argument("--n", type=int, default=8)
    s.add_argument("--portrait", action="store_true"); s.set_defaults(fn=cmd_search)

    g = sub.add_parser("get"); g.add_argument("url")
    for x in ("tags", "concept", "source", "license", "title"):
        g.add_argument("--" + x, default=None)
    g.add_argument("--orientation", default="unknown"); g.set_defaults(fn=cmd_get)

    r = sub.add_parser("register"); r.add_argument("file")
    for x in ("tags", "concept", "source", "license", "title", "src_url"):
        r.add_argument("--" + x, default=None)
    r.add_argument("--orientation", default="unknown"); r.set_defaults(fn=cmd_register)

    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
