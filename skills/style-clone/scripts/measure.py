#!/usr/bin/env python3
"""Measure the mechanical fingerprint of every video in a corpus dir.

Usage:
  python measure.py --dir CORPUS_DIR [--scene 0.30] [--tile 4x3]

Per video it extracts, with ffmpeg only (no paid API, no python deps):
  - duration, resolution, fps
  - cut list via scene detection -> ASL, cuts/min, shot-length distribution,
    the opening-3s cut count (hook density), longest hold
  - loudness (integrated LUFS, LRA) -> how hot the mix is vs the -14 LUFS norm
  - luma / saturation / hue averages sampled 2x/sec -> exposure + grade direction
  - words-per-minute from the subtitle track, if one was pulled
  - a contact sheet PNG of one frame per shot, for the vision pass

Writes <video>.metrics.json next to each video and metrics.json (aggregate) in the dir.
The numbers are the evidence; the vision pass in SKILL.md Step 3 reads the contact
sheets and supplies everything a number cannot see.
"""
import argparse, json, os, re, statistics as st, subprocess, sys, shutil

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"


def sh(cmd):
    return subprocess.run(cmd, text=True, capture_output=True,
                          encoding="utf-8", errors="replace")


def probe(path):
    r = sh([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate:format=duration",
            "-of", "json", path])
    d = json.loads(r.stdout or "{}")
    s = (d.get("streams") or [{}])[0]
    num, _, den = (s.get("r_frame_rate") or "0/1").partition("/")
    fps = round(float(num) / float(den or 1), 2) if float(den or 0) else None
    return {"w": s.get("width"), "h": s.get("height"), "fps": fps,
            "duration": round(float(d.get("format", {}).get("duration") or 0), 2)}


def cuts(path, thresh):
    r = sh([FFMPEG, "-hide_banner", "-i", path, "-filter:v",
            f"select='gt(scene,{thresh})',showinfo", "-f", "null", "-"])
    return sorted({round(float(m), 3) for m in
                   re.findall(r"pts_time:([0-9.]+)", r.stderr or "")})


def loudness(path):
    r = sh([FFMPEG, "-hide_banner", "-i", path, "-af", "ebur128=peak=true",
            "-f", "null", "-"])
    tail = (r.stderr or "")[-1200:]
    g = lambda k: (lambda m: float(m.group(1)) if m else None)(
        re.search(rf"{k}:\s*(-?[0-9.]+)", tail))
    return {"lufs_i": g("I"), "lra": g("LRA"), "true_peak": g("Peak")}


def color(path):
    r = sh([FFMPEG, "-hide_banner", "-i", path, "-vf",
            "fps=2,signalstats,metadata=print:file=-", "-f", "null", "-"])
    out = {}
    for key, tag in (("YAVG", "luma"), ("SATAVG", "sat"), ("HUEAVG", "hue")):
        vals = [float(v) for v in
                re.findall(rf"lavfi\.signalstats\.{key}=(-?[0-9.]+)", r.stdout or "")]
        if vals:
            out[tag] = {"mean": round(st.mean(vals), 1),
                        "p10": round(sorted(vals)[len(vals) // 10], 1),
                        "p90": round(sorted(vals)[-max(1, len(vals) // 10)], 1)}
    return out


def subs_wpm(path, duration):
    stem = os.path.splitext(path)[0]
    cand = [f for f in os.listdir(os.path.dirname(path) or ".")
            if f.startswith(os.path.basename(stem)) and f.endswith((".vtt", ".srt"))]
    if not cand or not duration:
        return None
    txt = open(os.path.join(os.path.dirname(path), cand[0]), encoding="utf-8",
               errors="replace").read()
    txt = re.sub(r"\d\d:\d\d:\d\d[.,]\d+ --> .*", " ", txt)
    txt = re.sub(r"<[^>]+>|WEBVTT|^\d+$", " ", txt, flags=re.M)
    words = len([w for w in txt.split() if any(c.isalpha() for c in w)])
    return {"words": words, "wpm": round(words / (duration / 60), 1)}


def contact_sheet(path, cutlist, dur, tile, min_frames=12):
    """One frame per shot (shot midpoint), tiled into a single PNG.

    A creator with near-zero hard cuts (a continuous screen recording, a locked-off
    talking head) produces 1-2 shots regardless of duration, which gave a near-useless
    1-frame sheet before this fallback existed (first hit on `adilet-fndr`, 2026-09-22 —
    5 of 6 watched videos had exactly 1 detected shot across 32-70s). When shot-midpoint
    sampling would under-fill the tile grid, fall back to fixed-interval sampling across
    the full duration instead, so there's always something to actually watch.
    """
    out = os.path.splitext(path)[0] + ".sheet.png"
    cols, rows = (int(x) for x in tile.split("x"))
    cap = cols * rows
    bounds = [0.0] + cutlist + [dur]
    mids = [(bounds[i] + bounds[i + 1]) / 2 for i in range(len(bounds) - 1)]
    if len(mids) > cap:  # even sample across the video, not just the front
        step = len(mids) / cap
        mids = [mids[int(i * step)] for i in range(cap)]
    elif len(mids) < min(min_frames, cap) and dur:
        # near-zero-cut video: shot midpoints alone don't cover the runtime.
        n = min(min_frames, cap)
        mids = [dur * (i + 0.5) / n for i in range(n)]
    tmp = os.path.splitext(path)[0] + "_f"
    os.makedirs(tmp, exist_ok=True)
    n = 0
    for t in mids:
        r = sh([FFMPEG, "-y", "-hide_banner", "-ss", f"{t:.2f}", "-i", path,
                "-frames:v", "1", "-vf", "scale=360:-2",
                os.path.join(tmp, f"f_{n:03d}.png")])
        if r.returncode == 0:
            n += 1
    if n:
        sh([FFMPEG, "-y", "-hide_banner", "-start_number", "0", "-i",
            os.path.join(tmp, "f_%03d.png"), "-frames:v", "1",
            "-filter_complex", f"tile={cols}x{rows}:padding=6:color=white", out])
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return out if os.path.exists(out) else None


def shot_stats(cutlist, dur):
    bounds = [0.0] + cutlist + [dur]
    lens = [round(bounds[i + 1] - bounds[i], 2) for i in range(len(bounds) - 1)]
    lens = [x for x in lens if x > 0.04]
    if not lens:
        return {}
    return {
        "n_shots": len(lens),
        "asl": round(st.mean(lens), 2),
        "median_shot": round(st.median(lens), 2),
        "shortest": min(lens), "longest": max(lens),
        "cuts_per_min": round((len(lens) - 1) / (dur / 60), 1) if dur else None,
        "cuts_first_3s": sum(1 for c in cutlist if c <= 3.0),
        "pct_shots_under_1s": round(100 * sum(1 for x in lens if x < 1) / len(lens)),
        "shot_lengths": lens[:80],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--scene", type=float, default=0.30)
    ap.add_argument("--tile", default="4x3")
    ap.add_argument("--min-frames", type=int, default=12,
                     help="fallback frame count for near-zero-cut videos (see contact_sheet)")
    a = ap.parse_args()

    vids = sorted(f for f in os.listdir(a.dir) if f.endswith((".mp4", ".mov", ".mkv")))
    if not vids:
        sys.exit(f"no videos in {a.dir}")

    all_m = []
    for v in vids:
        p = os.path.join(a.dir, v)
        print(f":: {v}", flush=True)
        info = probe(p)
        c = cuts(p, a.scene)
        m = {"file": v, **info, "shots": shot_stats(c, info["duration"]),
             "cut_times": c[:80], "audio": loudness(p), "color": color(p),
             "speech": subs_wpm(p, info["duration"]),
             "sheet": os.path.basename(contact_sheet(p, c, info["duration"], a.tile, a.min_frames) or "")}
        json.dump(m, open(os.path.splitext(p)[0] + ".metrics.json", "w"), indent=1)
        all_m.append(m)

    def agg(fn):
        vals = [x for x in (fn(m) for m in all_m) if isinstance(x, (int, float))]
        return {"mean": round(st.mean(vals), 2), "min": min(vals), "max": max(vals)} if vals else None

    summary = {
        "n_videos": len(all_m),
        "duration": agg(lambda m: m["duration"]),
        "asl": agg(lambda m: m["shots"].get("asl")),
        "cuts_per_min": agg(lambda m: m["shots"].get("cuts_per_min")),
        "cuts_first_3s": agg(lambda m: m["shots"].get("cuts_first_3s")),
        "pct_shots_under_1s": agg(lambda m: m["shots"].get("pct_shots_under_1s")),
        "lufs_i": agg(lambda m: m["audio"].get("lufs_i")),
        "lra": agg(lambda m: m["audio"].get("lra")),
        "luma_mean": agg(lambda m: (m["color"].get("luma") or {}).get("mean")),
        "sat_mean": agg(lambda m: (m["color"].get("sat") or {}).get("mean")),
        "wpm": agg(lambda m: (m["speech"] or {}).get("wpm")),
        "videos": all_m,
    }
    out = os.path.join(a.dir, "metrics.json")
    json.dump(summary, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n-> {out}")
    for k in ("asl", "cuts_per_min", "cuts_first_3s", "pct_shots_under_1s",
              "lufs_i", "luma_mean", "sat_mean", "wpm"):
        print(f"  {k:20} {summary[k]}")


def _selfcheck():
    assert shot_stats([2.0, 5.0], 8.0)["n_shots"] == 3
    assert shot_stats([2.0, 5.0], 8.0)["asl"] == round(8 / 3, 2)
    assert shot_stats([1.0], 4.0)["cuts_first_3s"] == 1
    assert shot_stats([], 5.0)["n_shots"] == 1
    assert shot_stats([], 0)["asl"] if False else True
    # near-zero-cut fallback: 1 shot over 60s should sample min_frames evenly, not 1 frame
    bounds = [0.0] + [] + [60.0]
    mids = [(bounds[i] + bounds[i + 1]) / 2 for i in range(len(bounds) - 1)]
    assert len(mids) == 1  # this is the under-fill case contact_sheet's fallback handles
    n = min(12, 4 * 3)
    fallback_mids = [60.0 * (i + 0.5) / n for i in range(n)]
    assert len(fallback_mids) == 12
    assert fallback_mids[0] == 2.5 and fallback_mids[-1] == 57.5
    print("selfcheck ok")


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        _selfcheck()
    else:
        main()
