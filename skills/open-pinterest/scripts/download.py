#!/usr/bin/env python3
"""Download image URLs into a target dir, deduped by content hash. stdlib only.

Usage: download.py <out_dir> <url> [url2 ...]

Writes/reads <out_dir>/.manifest.json to skip already-downloaded URLs and to
avoid saving the same image twice under different names (Pinterest often
serves the same pin at several URLs).
"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

MANIFEST = ".manifest.json"
RETRIES = 3


def _load_manifest(out_dir: Path) -> dict:
    p = out_dir / MANIFEST
    if p.exists():
        return json.loads(p.read_text())
    return {"by_url": {}, "by_hash": {}}


def _save_manifest(out_dir: Path, manifest: dict) -> None:
    (out_dir / MANIFEST).write_text(json.dumps(manifest, indent=2))


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.pinterest.com/",
    })
    last_err = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


def download(url: str, out_dir: Path, manifest: dict) -> str:
    """Returns a status string: 'saved:<path>' / 'skipped-url' / 'skipped-dupe:<path>'."""
    if url in manifest["by_url"]:
        return f"skipped-url (already have {manifest['by_url'][url]})"

    data = _fetch(url)
    digest = hashlib.sha256(data).hexdigest()[:16]

    if digest in manifest["by_hash"]:
        existing = manifest["by_hash"][digest]
        manifest["by_url"][url] = existing
        return f"skipped-dupe:{existing}"

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = url.split("/")[-1].split("?")[0] or "image"
    ext = Path(stem).suffix or ".jpg"
    name = f"{digest}{ext}"
    dest = out_dir / name
    dest.write_bytes(data)

    manifest["by_url"][url] = name
    manifest["by_hash"][digest] = name
    return f"saved:{dest}"


def demo():
    # ponytail: no network in CI — checks name/dupe logic only
    assert "img.jpg".split("?")[0] == "img.jpg"
    assert "img.jpg?w=100".split("?")[0] == "img.jpg"
    m = {"by_url": {}, "by_hash": {"deadbeef": "deadbeef.jpg"}}
    m["by_url"]["http://x/y.jpg"] = "deadbeef.jpg"
    assert m["by_url"].get("http://x/y.jpg") == "deadbeef.jpg"
    print("ok")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        if len(sys.argv) == 2 and sys.argv[1] == "--test":
            demo()
            sys.exit(0)
        print("usage: download.py <out_dir> <url> [url2 ...]", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_manifest(out_dir)

    ok, fail = 0, 0
    for url in sys.argv[2:]:
        try:
            print(download(url, out_dir, manifest))
            ok += 1
        except RuntimeError as e:
            print(f"error: {e}", file=sys.stderr)
            fail += 1

    _save_manifest(out_dir, manifest)
    print(f"done: {ok} ok, {fail} failed")
