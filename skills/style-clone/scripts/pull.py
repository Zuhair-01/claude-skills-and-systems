#!/usr/bin/env python3
"""Pull a creator's recent short-form videos + metadata + subs into a corpus dir.

Usage:
  python pull.py <profile_or_video_url> --out DIR [--n 12]

Accepts an Instagram profile URL/@handle, a TikTok profile, a YouTube channel/@handle,
or a plain list of individual video URLs (one per --url flag, repeatable).
Instagram profile scraping often needs cookies; if the profile pull returns nothing,
fall back to passing individual reel URLs. See SKILL.md Step 1.
"""
import argparse, json, os, subprocess, sys, shutil

YTDLP = shutil.which("yt-dlp") or "yt-dlp"


def norm(target: str) -> str:
    t = target.strip()
    if t.startswith("@"):
        return f"https://www.instagram.com/{t[1:]}/reels/"
    if "instagram.com" in t and "/reels" not in t and "/reel/" not in t and "/p/" not in t:
        return t.rstrip("/") + "/reels/"
    return t


def run(cmd, **kw):
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="profile URL, @handle, or single video URL")
    ap.add_argument("--url", action="append", default=[], help="explicit video URL (repeatable)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--cookies-from-browser", default=None,
                    help="e.g. chrome — needed for most Instagram profile pulls")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    urls = list(a.url)
    if a.target and not urls:
        urls = [norm(a.target)]
    if not urls:
        sys.exit("give a target or at least one --url")

    base = [YTDLP, "--ignore-errors", "--no-warnings"]
    if a.cookies_from_browser:
        base += ["--cookies-from-browser", a.cookies_from_browser]

    for u in urls:
        cmd = base + [
            "--playlist-end", str(a.n),
            "-f", "bv*+ba/b", "--merge-output-format", "mp4",
            "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,ar.*",
            "--write-info-json",
            "-o", os.path.join(a.out, "%(playlist_index|0)03d_%(id)s.%(ext)s"),
            u,
        ]
        print("::", " ".join(cmd[-2:]), flush=True)
        r = run(cmd)
        if r.returncode != 0:
            print(r.stderr[-1500:], file=sys.stderr)

    vids = sorted(f for f in os.listdir(a.out) if f.endswith(".mp4"))
    if not vids:
        sys.exit("NO VIDEOS PULLED — private profile or login wall. Retry with "
                 "--cookies-from-browser chrome, or pass individual reel URLs via --url.")

    # flatten the useful bits of each info.json so the analysis step has engagement signal
    idx = []
    for f in os.listdir(a.out):
        if not f.endswith(".info.json"):
            continue
        try:
            d = json.load(open(os.path.join(a.out, f), encoding="utf-8"))
        except Exception:
            continue
        idx.append({k: d.get(k) for k in
                    ("id", "title", "description", "duration", "view_count",
                     "like_count", "comment_count", "upload_date", "uploader",
                     "webpage_url", "width", "height", "fps")})
    idx.sort(key=lambda d: (d.get("view_count") or 0), reverse=True)
    json.dump(idx, open(os.path.join(a.out, "corpus.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(vids)} videos, {len(idx)} metadata records -> {a.out}")


if __name__ == "__main__":
    main()
