#!/usr/bin/env python3
"""Remove overlay watermarks/logos/text baked into a product photo's pixels.

Two real techniques, pick per case:
  crop    - cut away a watermark that sits in a strip/corner (a seller logo
            band along one edge, a corner badge). Honest: nothing invented,
            just less canvas. Best when the watermark hugs an edge and the
            product still fills the frame after the cut.
  inpaint - reconstruct the pixels under a watermark that sits ON TOP of the
            product (semi-transparent diagonal text across the middle, a
            small logo stamped over the product body) using OpenCV's Telea
            algorithm. This FABRICATES texture in the masked region from
            surrounding pixels - fine for a repeating diagonal text overlay
            or a small stamp on a plain background, but never use it to
            "remove" branding that is physically printed on the real product
            (packaging text, a molded logo) - that's the object itself, not
            an overlay, and inpainting it is fabricating the product photo.
            Re-source a different real photo instead.

Usage:
  python3 remove_watermark.py crop IN OUT --top N --bottom N --left N --right N
  python3 remove_watermark.py inpaint IN OUT --box x0,y0,x1,y1 [--box x0,y0,x1,y1 ...]
  python3 remove_watermark.py inpaint IN OUT --box x0,y0,x1,y1 --radius 5 --method ns

Coordinates are pixels, origin top-left, from a screenshot/zoom of IN at its
real resolution - look at the actual image before picking a box, don't guess.
"""
import argparse
import sys

import cv2
import numpy as np


def do_crop(src, out, top, bottom, left, right):
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        sys.exit(f"could not read {src}")
    h, w = img.shape[:2]
    y0, y1 = top, h - bottom
    x0, x1 = left, w - right
    if y1 <= y0 or x1 <= x0:
        sys.exit(f"crop margins ({top},{bottom},{left},{right}) leave nothing on a {w}x{h} image")
    cropped = img[y0:y1, x0:x1]
    cv2.imwrite(out, cropped)
    print(f"cropped {w}x{h} -> {cropped.shape[1]}x{cropped.shape[0]}, saved {out}")


def do_inpaint(src, out, boxes, radius, method):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        sys.exit(f"could not read {src}")
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    for (x0, y0, x1, y1) in boxes:
        x0, x1 = sorted((max(0, x0), min(w, x1)))
        y0, y1 = sorted((max(0, y0), min(h, y1)))
        mask[y0:y1, x0:x1] = 255
    if not mask.any():
        sys.exit("no valid box intersected the image")
    algo = cv2.INPAINT_NS if method == "ns" else cv2.INPAINT_TELEA
    result = cv2.inpaint(img, mask, radius, algo)
    cv2.imwrite(out, result)
    covered = 100.0 * mask.sum() / 255 / (h * w)
    print(f"inpainted {len(boxes)} region(s), {covered:.1f}% of frame, saved {out}")
    if covered > 15:
        print("WARNING: inpainted area is large - reconstructed texture may look soft/wrong; "
              "consider re-sourcing a clean photo instead of trusting this much fabricated area")


def parse_box(s):
    parts = [int(v) for v in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box must be x0,y0,x1,y1")
    return tuple(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("crop")
    c.add_argument("src")
    c.add_argument("out")
    c.add_argument("--top", type=int, default=0)
    c.add_argument("--bottom", type=int, default=0)
    c.add_argument("--left", type=int, default=0)
    c.add_argument("--right", type=int, default=0)

    i = sub.add_parser("inpaint")
    i.add_argument("src")
    i.add_argument("out")
    i.add_argument("--box", type=parse_box, action="append", required=True, dest="boxes")
    i.add_argument("--radius", type=int, default=5)
    i.add_argument("--method", choices=["telea", "ns"], default="telea")

    args = ap.parse_args()
    if args.cmd == "crop":
        do_crop(args.src, args.out, args.top, args.bottom, args.left, args.right)
    else:
        do_inpaint(args.src, args.out, args.boxes, args.radius, args.method)


if __name__ == "__main__":
    main()
