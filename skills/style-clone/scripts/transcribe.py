#!/usr/bin/env python3
"""Word-level transcript of raw footage (or a reference video) using faster-whisper.

Usage:
  python transcribe.py VIDEO [--out transcript.json] [--lang ar|en] [--model small]

Emits {"lang", "duration", "words":[{"w","start","end"}], "segments":[...]}.
Word timings are what the whole edit hangs off: dead-air cuts, caption chunks,
and b-roll entry points are all derived from them (see edl.py).
"""
import argparse, json, os, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=None)
    ap.add_argument("--lang", default=None, help="ar / en; auto-detect if omitted")
    ap.add_argument("--model", default="small",
                    help="tiny|base|small|medium|large-v3 — small is the sane default; "
                         "use medium+ for Arabic")
    ap.add_argument("--device", default="cpu",
                    help="cpu (default — CTranslate2's CUDA path needs a cuBLAS build "
                         "this box doesn't have; pass cuda once that's confirmed working)")
    a = ap.parse_args()

    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device=a.device, compute_type="int8")
    segs, info = model.transcribe(a.video, language=a.lang, word_timestamps=True,
                                  vad_filter=True,
                                  vad_parameters={"min_silence_duration_ms": 250})

    words, segments = [], []
    for s in segs:
        segments.append({"start": round(s.start, 3), "end": round(s.end, 3),
                         "text": s.text.strip()})
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "start": round(w.start, 3),
                          "end": round(w.end, 3)})
        print(f"[{s.start:7.2f}] {s.text.strip()[:90]}", flush=True)

    out = a.out or os.path.splitext(a.video)[0] + ".transcript.json"
    data = {"lang": info.language, "duration": round(info.duration, 2),
            "words": words, "segments": segments}
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(words)} words, {len(segments)} segments -> {out}")
    if not words:
        print("WARNING: no words. Music-only or failed detection — edl.py will need "
              "--silence-fallback.", file=sys.stderr)


if __name__ == "__main__":
    main()
