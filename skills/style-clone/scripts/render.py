#!/usr/bin/env python3
"""Render an EDL to a finished vertical cut: jump cuts, punch-ins, b-roll inserts,
styled karaoke captions, grade, music bed with ducking, loudness normalisation.

Usage:
  python render.py --edl RAW.edl.json --out final.mp4 [--size 1080x1920] [--fps 30]
                   [--punch] [--no-captions] [--music bed.mp3] [--music-db -18]

Three passes on purpose — one monster filter_complex is undebuggable:
  1. A-roll: trim + concat every kept block (+ optional punch-in on beats), grade
  2. B-roll: overlay each filled slot on top of the A-roll
  3. Finish: burn captions (.ass), mix music with sidechain ducking, loudnorm, export

Only b-roll slots with a `clip` path are used — unfilled slots are skipped silently,
so a half-filled EDL still renders.
"""
import argparse, json, os, shutil, subprocess, sys

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

# ASS colours are &HBBGGRR (blue-green-red), not RGB — &H0000E5FF is amber, not blue.
# base  = a word before it is spoken; accent = as it lands, and any emphasis word.
DEFAULT_CAPTION_STYLE = {
    "font": "Arial", "size_pct": 5.2, "bold": -1,
    "base": "&H00FFFFFF", "accent": "&H0000E5FF",
    "outline_col": "&H00000000", "outline": 3.5,
    "shadow": 0, "align": 2, "margin_v_pct": 22, "uppercase": False,
    "karaoke": True,
}


def has_audio(path):
    """Broll_Library clips are commonly video-only (confirmed 2026-09-23: all 22 clips
    in the current library have zero audio streams) — `pass_aroll` used to assume `0:a`
    always exists and crashed with an opaque filtergraph error on any of them used as a
    source. Probe first instead of assuming."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=index", "-of", "csv=p=0", path],
                       text=True, capture_output=True)
    return bool(r.stdout.strip())


def run(cmd, label):
    print(f":: {label}", flush=True)
    r = subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        sys.exit(f"ffmpeg failed at: {label}")
    return r


def ass_time(t):
    h, rem = divmod(max(0.0, t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(edl, path, W, H, style):
    st = {**DEFAULT_CAPTION_STYLE, **(style or {})}
    fs = int(H * st["size_pct"] / 100)
    mv = int(H * st["margin_v_pct"] / 100)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{st['font']},{fs},{st['accent']},{st['base']},{st['outline_col']},&H64000000,{st['bold']},0,0,0,100,100,0,0,1,{st['outline']},{st['shadow']},{st['align']},60,60,{mv},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    acc, base = st["accent"], st["base"]
    up = (lambda s: s.upper()) if st["uppercase"] else (lambda s: s)
    lines = []
    for c in edl.get("captions", []):
        emph = set(c.get("emphasis") or [])   # word indices carrying the meaning
        if st["karaoke"] and c.get("words"):
            parts = []
            for i, w in enumerate(c["words"]):
                cs = max(1, int(round((w["end"] - w["start"]) * 100)))
                # an emphasised word is accent-coloured before AND after it lands
                # (\c primary + \2c secondary), so it reads ahead of being spoken;
                # the trailing tags restore the style defaults for the words after it
                parts.append(
                    f"{{\\k{cs}\\c{acc}\\2c{acc}}}{up(w['w'])}{{\\c{acc}\\2c{base}}}"
                    if i in emph else f"{{\\kf{cs}}}{up(w['w'])}")
            body = " ".join(parts)
        else:
            body = " ".join(
                (f"{{\\c{acc}}}{up(w)}{{\\c{base}}}" if i in emph else up(w))
                for i, w in enumerate(c["text"].split()))
        lines.append(f"Dialogue: 0,{ass_time(c['start'])},{ass_time(c['end'])},Cap,,0,0,0,,{body}")
    open(path, "w", encoding="utf-8-sig").write(head + "\n".join(lines) + "\n")
    return path


def segments(cuts, beats, punch, amount=0.06):
    """Split each kept block at the visual beats inside it, and give consecutive
    segments alternating zoom levels.

    Why split instead of animating a zoom: ffmpeg's crop evaluates w/h once at init,
    so a t-dependent zoom is not possible in one pass — and a real editor wouldn't
    animate it anyway. A hard angle change on the beat IS the jump cut.
    """
    segs = []
    lvl = 0
    for c in cuts:
        inner = sorted(b for b in beats if c["tl_in"] < b < c["tl_out"] - 0.15) if punch else []
        marks = [c["src_in"]] + [c["src_in"] + (b - c["tl_in"]) for b in inner] + [c["src_out"]]
        for i in range(len(marks) - 1):
            segs.append({"src_in": round(marks[i], 3), "src_out": round(marks[i + 1], 3),
                         "zoom": 1.0 + (amount if (punch and lvl % 2) else 0.0),
                         "crop_x": c.get("crop_x", 0.5)})
            lvl += 1
    return segs


def pass_aroll(edl, out, W, H, fps, punch):
    src = edl["source"]
    src_has_audio = has_audio(src)
    segs = segments(edl["cuts"], edl.get("visual_beats", []), punch)
    g = edl.get("grade") or {}
    n = len(segs)
    audio_pad = "[0:a]" if src_has_audio else "[1:a]"
    # an input pad can only be consumed once — every trim needs its own copy
    fc = [f"[0:v]split={n}" + "".join(f"[sv{i}]" for i in range(n)),
          f"{audio_pad}asplit={n}" + "".join(f"[sa{i}]" for i in range(n))]
    vs, as_ = [], []
    for i, s in enumerate(segs):
        z = s["zoom"]
        # zoom by cropping a tighter window of the source, then scaling back up
        crop_in = (f"crop=w=iw/{z:.4f}:h=ih/{z:.4f}:x=(iw-ow)/2:y=(ih-oh)/2," if z > 1.0 else "")
        # Landscape source -> vertical target: `force_original_aspect_ratio=increase` scales
        # to cover, which for 16:9->9:16 already matches the target height exactly, so the
        # final crop only trims WIDTH — this crops horizontally, not vertically, and by
        # default (x unset) ffmpeg centers that crop blindly, no subject awareness (found
        # 2026-09-23 testing real Broll_Library footage). `crop_x` (0.0=left edge, 1.0=right
        # edge, default 0.5=center) lets a human editor who's actually looked at the footage
        # recenter the crop per-cut in the EDL — a real ML subject-tracking crop would be
        # better but isn't installed; a manual override beats a silently-blind default.
        cx = s.get("crop_x", 0.5)
        fc.append(f"[sv{i}]trim={s['src_in']}:{s['src_out']},setpts=PTS-STARTPTS,{crop_in}"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H}:x=(iw-ow)*{cx:.3f}:y=(ih-oh)*0.5,"
                  f"fps={fps},setsar=1[v{i}]")
        fc.append(f"[sa{i}]atrim={s['src_in']}:{s['src_out']},asetpts=PTS-STARTPTS[a{i}]")
        vs.append(f"[v{i}]"); as_.append(f"[a{i}]")
    fc.append("".join(v + a for v, a in zip(vs, as_)) +
              f"concat=n={len(segs)}:v=1:a=1[vc][ac]")

    chain = "[vc]" + (g.get("eq") or "null")   # e.g. eq=contrast=1.06:saturation=1.1
    if g.get("lut"):
        chain += f",lut3d='{g['lut']}'"
    fc.append(chain + "[vout]")

    ins = [FFMPEG, "-y", "-hide_banner", "-i", src]
    if not src_has_audio:
        ins += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    run(ins + ["-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[ac]", "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out],
        f"pass 1/3 A-roll ({len(segs)} segments{', punch-in' if punch else ''}"
        f"{', synthesized silent audio (source had none)' if not src_has_audio else ''})")


IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

PIP_POS = {  # (x, y) expressions relative to the overlay frame, margin substituted in
    "bottom-left":  ("{m}", "H-h-{m}"),
    "bottom-right": ("W-w-{m}", "H-h-{m}"),
    "top-left":     ("{m}", "{m}"),
    "top-right":    ("W-w-{m}", "{m}"),
    "bottom-center": ("(W-w)/2", "H-h-{m}"),  # the mavgpt-style "under the chin" spot
    "center":        ("(W-w)/2", "(H-h)/2"),
}


def build_broll_graph(slots, W, H, grade, pip_width_pct, pip_margin_pct, pip_corner):
    """Pure filter-graph construction, kept separate from ffmpeg execution so the
    split-count logic (the exact class of 'input pad consumed twice' bug this pipeline
    hit once already, in pass_aroll) can be unit-tested without running ffmpeg."""
    pip_slots = [s for s in slots if s.get("pip")]
    n_pip = len(pip_slots)

    extra_inputs = []   # one ffmpeg -i spec (list of args) per slot, in order
    fc = []
    if n_pip:
        # [0:v] feeds both the main overlay chain AND a trim per PiP slot — ffmpeg
        # only lets an input pad feed ONE filter, so split it into (1 base + n_pip) copies.
        fc.append(f"[0:v]split={n_pip + 1}[base0]" +
                  "".join(f"[pipsrc{i}]" for i in range(n_pip)))
        cur = "[base0]"
    else:
        cur = "[0:v]"

    pip_i = 0
    for i, s in enumerate(slots, start=1):
        is_badge = s.get("kind") == "badge"
        is_graphic = s.get("kind") == "graphic" or s["clip"].lower().endswith(IMAGE_EXT)
        dur = s["tl_out"] - s["tl_in"]
        extra_inputs.append(
            (["-loop", "1", "-t", f"{dur:.3f}", "-i", s["clip"]] if (is_graphic or is_badge)
             else ["-stream_loop", "-1", "-t", f"{dur:.3f}", "-i", s["clip"]]))
        if is_badge:
            # small, colorkeyed, positioned — the base footage stays fully visible around
            # it. Never the full-frame is_graphic path: a badge that covered the whole
            # frame would hide the presenter it's supposed to sit on top of.
            bw = int(W * s.get("badge_width_pct", 42) / 100)
            m = int(W * s.get("badge_margin_pct", 6) / 100)
            xexpr, yexpr = PIP_POS[s.get("badge_pos", "bottom-center")]
            ck = s.get("chroma_key", "0x00FF00")
            fc.append(f"[{i}:v]scale={bw}:-2,"
                      f"colorkey={ck}:{s.get('chroma_similarity', 0.35)}:"
                      f"{s.get('chroma_blend', 0.12)},"
                      f"setpts=PTS-STARTPTS+{s['tl_in']:.3f}/TB[b{i}]")
            fc.append(f"{cur}[b{i}]overlay=x={xexpr.format(m=m)}:y={yexpr.format(m=m)}:"
                      f"enable='between(t,{s['tl_in']:.3f},{s['tl_out']:.3f})'[ov{i}]")
            cur = f"[ov{i}]"
            continue
        cx = s.get("crop_x", 0.5)   # see pass_aroll's crop_x comment — same blind-center fix
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H}:x=(iw-ow)*{cx:.3f}:y=(ih-oh)*0.5,"
                  f"setpts=PTS-STARTPTS+{s['tl_in']:.3f}/TB,{grade}[b{i}]")
        fc.append(f"{cur}[b{i}]overlay=enable='between(t,{s['tl_in']:.3f},{s['tl_out']:.3f})'"
                  f"[ov{i}]")
        cur = f"[ov{i}]"
        if s.get("pip"):
            m = int(W * pip_margin_pct / 100)
            pw = int(W * pip_width_pct / 100)
            xexpr, yexpr = PIP_POS[pip_corner]
            fc.append(f"[pipsrc{pip_i}]trim={s['tl_in']:.3f}:{s['tl_out']:.3f},"
                      f"setpts=PTS-STARTPTS+{s['tl_in']:.3f}/TB,scale={pw}:-2[pip{i}]")
            fc.append(f"{cur}[pip{i}]overlay=x={xexpr.format(m=m)}:y={yexpr.format(m=m)}:"
                      f"enable='between(t,{s['tl_in']:.3f},{s['tl_out']:.3f})'[ovp{i}]")
            cur = f"[ovp{i}]"
            pip_i += 1

    return extra_inputs, fc, cur, n_pip


def pass_broll(edl, aroll, out, W, H, pip_width_pct=30, pip_margin_pct=4,
               pip_corner="bottom-left"):
    slots = [s for s in edl.get("broll", []) if s.get("clip")]
    if not slots:
        shutil.copy(aroll, out)
        print(":: pass 2/3 b-roll — no filled slots, skipped")
        return
    grade = (edl.get("grade") or {}).get("broll_match", "eq=saturation=1.0")
    extra_inputs, fc, cur, n_pip = build_broll_graph(
        slots, W, H, grade, pip_width_pct, pip_margin_pct, pip_corner)

    ins = [FFMPEG, "-y", "-hide_banner", "-i", aroll]
    for spec in extra_inputs:
        ins += spec

    run(ins + ["-filter_complex", ";".join(fc), "-map", cur, "-map", "0:a",
               "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "copy", out],
        f"pass 2/3 b-roll ({len(slots)} inserts, {n_pip} with PiP)")


def pass_finish(edl, vid, out, W, H, ass_path, music, music_db):
    lufs = (edl.get("audio") or {}).get("target_lufs", -14.0)
    ins = [FFMPEG, "-y", "-hide_banner", "-i", vid]
    fc = []
    # -map takes bracket syntax ([label]) only for an actual filtergraph output;
    # a stream nothing has touched must be mapped as a raw stream (0:v, no brackets) —
    # passing "[0:v]" here when no video filter ran is invalid and ffmpeg rejects it.
    v = "0:v"
    if ass_path:
        esc = ass_path.replace("\\", "/").replace(":", "\\:")
        fc.append(f"[0:v]subtitles='{esc}'[vout]")
        v = "[vout]"
    if music:
        ins += ["-stream_loop", "-1", "-i", music]
        fc.append(f"[1:a]volume={music_db}dB,aformat=channel_layouts=stereo[mus]")
        fc.append("[mus][0:a]sidechaincompress=threshold=0.04:ratio=8:attack=8:release=350[duck]")
        fc.append(f"[0:a][duck]amix=inputs=2:duration=first:dropout_transition=0,"
                  f"loudnorm=I={lufs}:TP=-1.5:LRA=11[aout]")
        amap = "[aout]"
    else:
        fc.append(f"[0:a]loudnorm=I={lufs}:TP=-1.5:LRA=11[aout]")
        amap = "[aout]"
    run(ins + ["-filter_complex", ";".join(fc), "-map", v, "-map", amap,
               "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
               "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", out],
        f"pass 3/3 finish (captions{'+music' if music else ''}, loudnorm {lufs} LUFS)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edl", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--punch", action="store_true")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--music", default=None)
    ap.add_argument("--music-db", type=float, default=-18.0)
    ap.add_argument("--pip-width-pct", type=float, default=30,
                    help="PiP box width as %% of frame width, for broll slots with pip:true")
    ap.add_argument("--pip-margin-pct", type=float, default=4)
    ap.add_argument("--pip-corner", default="bottom-left", choices=list(PIP_POS))
    a = ap.parse_args()

    edl = json.load(open(a.edl, encoding="utf-8"))
    W, H = (int(x) for x in a.size.split("x"))
    work = os.path.splitext(a.out)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    aroll = os.path.join(work, "aroll.mp4")
    withb = os.path.join(work, "broll.mp4")

    pass_aroll(edl, aroll, W, H, a.fps, a.punch)
    pass_broll(edl, aroll, withb, W, H, a.pip_width_pct, a.pip_margin_pct, a.pip_corner)
    ass_path = None
    if not a.no_captions and edl.get("captions"):
        ass_path = write_ass(edl, os.path.join(work, "caps.ass"), W, H,
                             edl.get("caption_style"))
    pass_finish(edl, withb, a.out, W, H, ass_path, a.music, a.music_db)
    print(f"\n-> {a.out}\n   intermediates kept in {work} (delete when happy)")
    print("   now run measure.py on the OUTPUT and score it against the DNA "
          "scorecard — see SKILL.md Phase 7.")


def _selfcheck():
    cuts = [{"src_in": 0.0, "src_out": 2.0, "tl_in": 0.0, "tl_out": 2.0},
            {"src_in": 5.0, "src_out": 6.0, "tl_in": 2.0, "tl_out": 3.0}]
    s = segments(cuts, [1.0, 2.0], punch=True)
    assert len(s) == 3, s                      # block 1 split at the inner beat
    assert s[0]["src_out"] == 1.0 and s[1]["src_in"] == 1.0
    assert s[0]["zoom"] == 1.0 and s[1]["zoom"] > 1.0   # alternating
    assert len(segments(cuts, [1.0, 2.0], punch=False)) == 2
    assert all(x["src_out"] > x["src_in"] for x in s)
    assert all(x["crop_x"] == 0.5 for x in s), "crop_x should default to centered"
    cuts_x = [{"src_in": 0.0, "src_out": 2.0, "tl_in": 0.0, "tl_out": 2.0, "crop_x": 0.2}]
    assert segments(cuts_x, [], punch=False)[0]["crop_x"] == 0.2, \
        "an explicit per-cut crop_x must carry through to its segment(s)"
    assert ass_time(3661.5).startswith("1:01:01")
    import tempfile, json as j
    edl = {"captions": [{"start": 0.0, "end": 1.0, "text": "hi there",
                         "words": [{"w": "hi", "start": 0.0, "end": 0.5},
                                   {"w": "there", "start": 0.5, "end": 1.0}],
                         "emphasis": [1]}]}
    p = os.path.join(tempfile.gettempdir(), "t.ass")
    write_ass(edl, p, 1080, 1920, {"uppercase": True})
    txt = open(p, encoding="utf-8-sig").read()
    assert "\\kf50}HI" in txt, txt[-300:]                     # plain word sweeps
    assert "\\k50\\c&H0000E5FF\\2c&H0000E5FF}THERE" in txt, txt[-300:]   # emphasis holds accent
    assert "Dialogue: 0,0:00:00.00,0:00:01.00" in txt, txt[-300:]
    assert "\\C" not in txt, "uppercase leaked into ASS override tags"
    # non-karaoke path keeps emphasis too
    p2 = os.path.join(tempfile.gettempdir(), "t2.ass")
    write_ass(edl, p2, 1080, 1920, {"karaoke": False})
    t2 = open(p2, encoding="utf-8-sig").read()
    assert "hi {\\c&H0000E5FF}there" in t2, t2[-300:]

    # build_broll_graph: the split-count bug class — [0:v] must be consumed exactly
    # once as a raw input pad; every other reference has to go through a split output.
    slots_no_pip = [{"tl_in": 1.0, "tl_out": 2.0, "clip": "a.mp4"}]
    _, fc0, cur0, n0 = build_broll_graph(slots_no_pip, 1080, 1920, "null", 30, 4, "bottom-left")
    raw_uses = sum(g.count("[0:v]") for g in fc0)
    assert raw_uses == 1 and n0 == 0 and cur0 == "[ov1]", (raw_uses, n0, cur0)

    slots_2pip = [
        {"tl_in": 1.0, "tl_out": 2.0, "clip": "a.png", "pip": True},
        {"tl_in": 5.0, "tl_out": 6.0, "clip": "b.mp4", "pip": True},
        {"tl_in": 8.0, "tl_out": 9.0, "clip": "c.mp4"},  # no pip
    ]
    ins2, fc2, cur2, n2 = build_broll_graph(slots_2pip, 1080, 1920, "null", 25, 5, "bottom-left")
    graph = ";".join(fc2)
    assert n2 == 2
    assert graph.count("[0:v]") == 1, "raw input pad used more than once — will fail in ffmpeg"
    assert "split=3[base0][pipsrc0][pipsrc1]" in graph
    # every split output must be consumed exactly once downstream
    for label in ("[base0]", "[pipsrc0]", "[pipsrc1]"):
        assert graph.count(label) == 2, (label, graph)  # once produced, once consumed
    assert "-loop" in ins2[0] and "1" in ins2[0]          # slot 1 is a .png -> looped image
    assert "-stream_loop" in ins2[1]                       # slot 2 is a .mp4 -> looped video

    # badge slot: colorkeyed, small, positioned — never the full-frame is_graphic path
    slots_badge = [{"tl_in": 2.0, "tl_out": 4.0, "clip": "badge.png", "kind": "badge",
                    "badge_pos": "bottom-center", "chroma_key": "0x00FF00"}]
    _, fcb, curb, nb = build_broll_graph(slots_badge, 1080, 1920, "null", 30, 4, "bottom-left")
    graphb = ";".join(fcb)
    assert nb == 0                                # badges don't use the PiP split path
    assert "colorkey=0x00FF00" in graphb
    assert "crop=1080:1920" not in graphb          # must NOT take the full-frame path
    assert "(W-w)/2" in graphb                     # bottom-center is horizontally centered
    assert curb == "[ov1]"
    assert "-stream_loop" in ins2[2]                       # slot 3 (no pip) still a video
    assert cur2 == "[ov3]", cur2    # slot 3 has no pip, so the chain ends on its plain overlay
    assert "y=H-h-54" in graph, graph   # bottom-left margin = int(1080*5/100) = 54
    assert "x=54" in graph
    assert "hi {\\c&H0000E5FF}there" in t2, t2[-300:]
    print("selfcheck ok")


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        _selfcheck()
    else:
        main()
