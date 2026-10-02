#!/usr/bin/env python3
"""Download Pinterest video/motion pins via yt-dlp (already installed as a module).

Usage: download_video.py <out_dir> <pin_url> [pin_url2 ...]

Each arg is a pin PAGE url (pinterest.com/pin/...), not a raw .mp4 — yt-dlp
resolves the actual media itself. Saves as <video_id>.mp4 into out_dir.
"""
import subprocess
import sys
from pathlib import Path


def download(pin_url: str, out_dir: Path) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-o", str(out_dir / "%(id)s.%(ext)s"),
        "--no-playlist",
        pin_url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return f"error: {r.stderr.strip()[-500:]}"
    return "ok"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: download_video.py <out_dir> <pin_url> [pin_url2 ...]", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(sys.argv[1])
    ok, fail = 0, 0
    for url in sys.argv[2:]:
        result = download(url, out_dir)
        print(f"{url}: {result}")
        if result == "ok":
            ok += 1
        else:
            fail += 1
    print(f"done: {ok} ok, {fail} failed")
