#!/usr/bin/env python3
"""Turn a word-level transcript + a target style DNA into an editable EDL.

Usage:
  python edl.py --video RAW.mp4 --transcript RAW.transcript.json --dna dna.json \
                [--out edl.json] [--keep-fillers]

What it decides mechanically (numbers, no taste):
  - dead-air removal: every inter-word gap over `max_gap` is cut, leaving `pad` of air
  - the resulting timeline, in both source and timeline time
  - `visual_beats`: the timestamps where a visual change (punch-in, angle, b-roll)
    MUST happen for the finished piece to hit the DNA's target ASL
  - caption chunks with word timings, ready for karaoke/highlight styling
  - b-roll slots: the beats worth filling, ranked, with the phrase that will be
    on screen — `concept` and `clip` are left null ON PURPOSE

What it does NOT decide (taste — Claude fills these in the EDL before render):
  - which concept a b-roll slot gets, and which clip
  - which words get caption emphasis
  - where the deliberate holds go (a beat can be deleted to create one)

dna.json is the machine-readable half of a STYLE_DNA.md — see SKILL.md Phase 4.
"""
import argparse, json, os, sys

DEFAULT_DNA = {
    "asl": 1.8, "max_gap": 0.35, "pad": 0.12, "caption_max_words": 4,
    "caption_max_chars": 26, "broll_share": 0.25, "broll_len": 1.8,
    "cuts_first_3s": 2, "lufs": -14.0,
}
FILLERS = {"um", "uh", "erm", "like,", "you know", "يعني", "اه", "ااه"}


def load_dna(path):
    d = dict(DEFAULT_DNA)
    if path:
        d.update(json.load(open(path, encoding="utf-8")))
    return d


def keep_ranges(words, max_gap, pad, drop_fillers):
    """Merge words into speech blocks, cutting any gap longer than max_gap."""
    ws = [w for w in words if not (drop_fillers and w["w"].lower().strip(".,!?") in FILLERS)]
    if not ws:
        return []
    blocks, cur = [], {"src_in": max(0.0, ws[0]["start"] - pad), "src_out": ws[0]["end"],
                       "words": [ws[0]]}
    for prev, w in zip(ws, ws[1:]):
        if w["start"] - prev["end"] > max_gap:
            cur["src_out"] = prev["end"] + pad
            blocks.append(cur)
            cur = {"src_in": max(0.0, w["start"] - pad), "src_out": w["end"], "words": [w]}
        else:
            cur["words"].append(w)
    cur["src_out"] = ws[-1]["end"] + pad
    blocks.append(cur)

    t = 0.0
    for b in blocks:
        b["src_in"], b["src_out"] = round(b["src_in"], 3), round(b["src_out"], 3)
        b["tl_in"] = round(t, 3)
        t += b["src_out"] - b["src_in"]
        b["tl_out"] = round(t, 3)
        b["text"] = " ".join(w["w"] for w in b["words"])
    return blocks


def to_timeline(blocks, src_t):
    """Map a source timestamp onto the cut timeline; None if it was cut out."""
    for b in blocks:
        if b["src_in"] <= src_t <= b["src_out"]:
            return round(b["tl_in"] + (src_t - b["src_in"]), 3)
    return None


def visual_beats(blocks, total, dna):
    """Timestamps needing a visual change so the piece hits the target ASL.

    Existing hard cuts (block joins) already supply some. The rest are placed at
    the widest word gaps inside blocks — the natural breath points, which is where
    a real editor punches in or drops b-roll.
    """
    target_n = max(1, int(round(total / dna["asl"])))
    existing = [b["tl_in"] for b in blocks[1:]]
    if len(existing) >= target_n:
        return sorted(round(x, 3) for x in existing)

    cands = []
    for b in blocks:
        for prev, w in zip(b["words"], b["words"][1:]):
            tl = to_timeline(blocks, w["start"])
            if tl is None:
                continue
            gap = w["start"] - prev["end"]
            # prefer a real breath, and never stack beats closer than 0.6s
            cands.append({"tl": round(tl, 3), "gap": round(gap, 3),
                          "phrase": " ".join(x["w"] for x in b["words"][
                              max(0, b["words"].index(prev) - 3):
                              b["words"].index(prev) + 4])})
    cands.sort(key=lambda c: -c["gap"])
    picked = list(existing)
    for c in cands:
        if len(picked) >= target_n:
            break
        if all(abs(c["tl"] - p) > 0.6 for p in picked):
            picked.append(c["tl"])
    return sorted(round(x, 3) for x in picked)


def hook_check(beats, dna):
    got = sum(1 for b in beats if b <= 3.0)
    return {"cuts_first_3s": got, "target": dna["cuts_first_3s"],
            "ok": abs(got - dna["cuts_first_3s"]) <= 1}


def captions(blocks, dna):
    out = []
    for b in blocks:
        chunk = []
        for w in b["words"]:
            chunk.append(w)
            txt = " ".join(x["w"] for x in chunk)
            last = w is b["words"][-1]
            if len(chunk) >= dna["caption_max_words"] or len(txt) >= dna["caption_max_chars"] or last:
                out.append({
                    "start": round(b["tl_in"] + (chunk[0]["start"] - b["src_in"]), 3),
                    "end": round(b["tl_in"] + (chunk[-1]["end"] - b["src_in"]), 3),
                    "text": txt,
                    "words": [{"w": x["w"],
                               "start": round(b["tl_in"] + (x["start"] - b["src_in"]), 3),
                               "end": round(b["tl_in"] + (x["end"] - b["src_in"]), 3)}
                              for x in chunk],
                    "emphasis": [],
                })
                chunk = []
    return out


def broll_slots(beats, caps, total, dna):
    """Rank beats as b-roll candidates until the DNA's b-roll share is covered."""
    budget = total * dna["broll_share"]
    slots, used = [], 0.0
    for t in beats:
        if used >= budget:
            break
        if t < 1.0 or t > total - dna["broll_len"]:
            continue
        if slots and t - slots[-1]["tl_in"] < dna["broll_len"] * 2:
            continue
        phrase = next((c["text"] for c in caps if c["start"] <= t <= c["end"]), "")
        slots.append({"tl_in": t, "tl_out": round(min(total, t + dna["broll_len"]), 3),
                      "phrase_on_screen": phrase,
                      "concept": None, "clip": None, "fit_note": None,
                      "transition": "cut",
                      # kind: "footage" (sourced/found clip, broll.py) or "graphic"
                      # (a card built with graphics.py — clip is then a PNG path, and
                      # render.py loops it as a still instead of a video). pip: true
                      # composites the talking-head take as a small corner box on top
                      # of this slot instead of leaving it a bare full-bleed graphic —
                      # set it whenever the loaded DNA says the presenter stays visible
                      # under graphics (see render.py --pip-corner/--pip-width-pct).
                      "kind": None, "pip": False})
        used += dna["broll_len"]
    return slots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--dna", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--keep-fillers", action="store_true")
    a = ap.parse_args()

    dna = load_dna(a.dna)
    tr = json.load(open(a.transcript, encoding="utf-8"))
    if not tr.get("words"):
        sys.exit("transcript has no word timings — re-run transcribe.py, or hand-write the EDL")

    blocks = keep_ranges(tr["words"], dna["max_gap"], dna["pad"], not a.keep_fillers)
    total = blocks[-1]["tl_out"]
    beats = visual_beats(blocks, total, dna)
    caps = captions(blocks, dna)

    edl = {
        "source": os.path.abspath(a.video),
        "dna": dna,
        "timeline_duration": total,
        "source_duration": tr.get("duration"),
        "removed_dead_air": round((tr.get("duration") or total) - total, 2),
        "cuts": [{k: b[k] for k in ("src_in", "src_out", "tl_in", "tl_out", "text")}
                 for b in blocks],
        "visual_beats": beats,
        "hook": hook_check(beats, dna),
        "captions": caps,
        "broll": broll_slots(beats, caps, total, dna),
        "sfx": [], "music": None,
        "grade": {"lut": None, "eq": None},
        "audio": {"target_lufs": dna["lufs"]},
    }
    out = a.out or os.path.splitext(a.video)[0] + ".edl.json"
    json.dump(edl, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"-> {out}")
    print(f"  {len(blocks)} speech blocks, {edl['removed_dead_air']}s dead air removed")
    print(f"  timeline {total}s | {len(beats)} visual beats "
          f"(ASL {round(total / max(1, len(beats)), 2)}s vs target {dna['asl']}s)")
    print(f"  hook: {edl['hook']}")
    print(f"  {len(caps)} caption chunks | {len(edl['broll'])} b-roll slots to fill")


def _selfcheck():
    words = [{"w": f"w{i}", "start": i * 0.4, "end": i * 0.4 + 0.3} for i in range(10)]
    words += [{"w": "after", "start": 8.0, "end": 8.4}]  # 4.1s of dead air
    b = keep_ranges(words, 0.35, 0.1, False)
    assert len(b) == 2, b
    assert b[1]["tl_in"] < 8.0, "dead air not removed"
    assert to_timeline(b, 0.5) is not None and to_timeline(b, 6.0) is None
    d = dict(DEFAULT_DNA)
    caps = captions(b, d)
    assert caps and all(c["end"] >= c["start"] for c in caps)
    assert all(len(c["words"]) <= d["caption_max_words"] for c in caps)
    bts = visual_beats(b, b[-1]["tl_out"], d)
    assert bts == sorted(bts) and len(set(bts)) == len(bts)
    print("selfcheck ok")


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        _selfcheck()
    else:
        main()
