#!/usr/bin/env python3
"""Cut a downloaded ref down to just the subject (transparent PNG). Uses rembg.

Usage: remove_bg.py <in_file> [out_file]
Default out_file: <in_file stem>_cutout.png next to the input.
"""
import sys
from pathlib import Path


def demo():
    # ponytail: no model download in CI — checks path logic only
    assert _out_path(Path("x/y.jpg"), None) == Path("x/y_cutout.png")
    print("ok")


def _out_path(in_file: Path, out_file: str | None) -> Path:
    return Path(out_file) if out_file else in_file.with_name(f"{in_file.stem}_cutout.png")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        demo()
        sys.exit(0)
    if len(sys.argv) < 2:
        print("usage: remove_bg.py <in_file> [out_file]", file=sys.stderr)
        sys.exit(1)

    from rembg import remove  # first run downloads the u2net model (~176MB), then cached

    in_file = Path(sys.argv[1])
    out_file = _out_path(in_file, sys.argv[2] if len(sys.argv) > 2 else None)
    out_file.write_bytes(remove(in_file.read_bytes()))
    print(f"saved:{out_file}")
