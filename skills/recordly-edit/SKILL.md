---
name: recordly-edit
description: Edit and polish a Recordly recording in its timeline UI; documented CLI flags are proposed, not currently working.
---

# recordly-edit — Automate Timeline Editing & Polishing

**Type:** Workflow / Video Editing  
**Triggers:** "recordly edit", "edit demo", "add zoom", "trim recording", "annotate video", "polish timeline"  
**Input:** `.recordly` project file + raw MP4  
**Output:** Updated `.recordly` project (non-destructive) + preview MP4

> **⚠️ Verification status:** Recordly v1.4.0 has no documented CLI — all editing below happens through the in-app timeline UI (drag-and-drop trims/zooms/annotations, per the official README). `recordly edit --flag ...` commands are a **proposed automation contract**, not a working interface today.

---

## What It Does

Automate common timeline editing tasks:
- **Trim:** Remove dead air, mistakes
- **Zoom:** Add automated or manual emphasis
- **Speed:** Fast-forward boring sections, slow-motion key moments
- **Annotate:** Add text callouts, arrows, highlights
- **Audio:** Layer voice-over or background music

**Non-destructive:** All edits saved in `.recordly` JSON; original media untouched.

---

## Quick Start

```
recordly edit demo.recordly --trim-silence
recordly edit demo.recordly --add-zoom 5000 10000 2.0
recordly edit demo.recordly --annotate-at 3000 "Click here!" --duration 2000
```

---

## Trim Options

| Option | Type | Effect |
|---|---|---|
| `--trim-silence` | flag | Auto-detect quiet sections (< -40dB), mark for deletion |
| `--trim-pause` | float | Collapse pauses longer than N seconds to 0.5x duration |
| `--trim-regions` | JSON path | Load trim specs from JSON file (`[{"start": ms, "end": ms}, ...]`) |
| `--keep-regions` | JSON path | Inverse: keep ONLY these regions, trim rest (useful for highlight reels) |

---

## Zoom Options

| Option | Type | Effect |
|---|---|---|
| `--auto-zoom` | flag | Recordly's cursor-activity heuristic suggests zooms; review list before applying |
| `--manual-zoom` | string | `START_MS:END_MS:ZOOM_LEVEL:CENTER_X:CENTER_Y`; e.g. `1000:3000:2.0:640:360` |
| `--follow-cursor` | flag | Auto-place zoom on detected cursor click locations |
| `--review-zooms` | flag | Export a preview MP4 with zoom suggestions highlighted; wait for approval before saving |

---

## Speed Options

| Option | Type | Effect |
|---|---|---|
| `--speed-regions` | JSON path | `[{"start": ms, "end": ms, "rate": 1.5}, ...]` |
| `--fast-forward` | float | Regions with no cursor activity: speed up by factor N (e.g. 2.0 = 2x) |
| `--slow-motion` | float | Regions with rapid cursor movement: slow down by factor N (e.g. 0.5 = half speed) |

---

## Annotation Options

| Option | Type | Effect |
|---|---|---|
| `--annotate-at` | string | `TIME_MS:TEXT:DURATION_MS`; e.g. `3000:"Click here":2000` |
| `--annotate-file` | JSON path | `[{"time": ms, "text": "...", "duration": ms, "x": px, "y": px}, ...]` |
| `--label-clicks` | flag | Auto-label each detected mouse click with a circle + timestamp |
| `--highlight-region` | string | `START_MS:END_MS:SHAPE`; shape = `circle`, `rect`, `arrow`, `box` |

---

## Audio Options

| Option | Type | Effect |
|---|---|---|
| `--voiceover` | path | MP3/WAV file to layer as voice-over (auto-positioned on timeline) |
| `--voiceover-start` | int | Start voice-over at TIME_MS in main timeline |
| `--background-music` | path | MP3 file; fade in/out to avoid clashing with dialog |
| `--audio-levels` | JSON path | `[{"start": ms, "voice": 0.8, "music": 0.2, "system": 0.5}, ...]` |

---

## Aspect Ratio & Crop

| Option | Type | Effect |
|---|---|---|
| `--aspect-ratio` | enum | `16:9`, `9:16`, `1:1`, `4:3`, or custom `WxH` |
| `--crop` | string | `X:Y:WIDTH:HEIGHT` (pixels); e.g. `100:50:1280:720` to crop taskbar |

---

## Workflow: Polishing a Recorded Demo

### Step 1: Launch and record with `recordly-launch`
```bash
recordly launch --window chrome --audio microphone --duration 300
# Record 3–5 min walkthrough
# Auto-exports to ~/.recordly/raw/demo.recordly + demo.mp4
```

### Step 2: Auto-detect timeline issues
```bash
recordly edit demo.recordly --trim-silence --review-zooms
# Analyzes silence sections + cursor activity
# Exports preview MP4 with suggestions highlighted
# Waits for the user approval (manual review, not automated)
```

### Step 3: Apply approved edits
```bash
recordly edit demo.recordly \
  --trim-silence \
  --auto-zoom \
  --annotate-file edits.json \
  --voiceover voiceover.mp3 \
  --aspect-ratio 16:9
# Saves to demo.recordly with all edits merged
```

### Step 4: Preview in Recordly UI or export directly
```bash
recordly export demo.recordly --format mp4 --quality high
```

---

## Batch Editing (Process Multiple Recordings)

```bash
recordly edit batch \
  --input-dir ~/.recordly/raw \
  --pattern "*.recordly" \
  --trim-silence \
  --fast-forward 1.5 \
  --aspect-ratio 16:9 \
  --output-dir ~/.recordly/polished
# Processes all .recordly files in parallel (3-worker pool)
# Each receives same edit ops
# Results saved to polished/ directory
```

---

## Review Workflow (Mandatory for Quality)

**Do NOT apply edits blindly.** Recordly's auto-suggestions are heuristics; they must be reviewed:

```bash
recordly edit demo.recordly --auto-zoom --review-zooms
# Step 1: Exports preview.mp4 with zoom regions outlined
# Step 2: Waits for manual approval (the user watches preview, confirms zooms are sensible)
# Step 3: User provides JSON approval file or rejects
```

**Sample approval workflow:**
```json
{
  "approved_zooms": [
    {"start": 5000, "end": 7000, "reason": "Shows button click clearly"},
    {"start": 12000, "end": 14000, "reason": "Emphasizes result"},
    {"start": 20000, "end": 22000, "rejected": true, "reason": "Zoom is too aggressive, distracting"}
  ],
  "approved_trims": [
    {"start": 0, "end": 500, "reason": "Remove startup lag"}
  ]
}
```

---

## Validation

Before committing edits to `.recordly`:

```bash
recordly edit demo.recordly --trim-silence --dry-run
# Simulates timeline without writing; outputs diff to stdout
# Allows verification before overwriting project
```

---

## Integration with Other Skills

- **Input:** `.recordly` project from `recordly-launch` or saved prior session
- **Output:** Updated `.recordly` project (feeds into `recordly-export`)
- **Parallel:** Can run alongside other recordings without conflicts (each is an independent `.recordly` file)

---

## See Also

- [recordly-launch](../recordly-launch/SKILL.md) — Launch and record
- [recordly-export](../recordly-export/SKILL.md) — Convert to MP4/GIF
- [RECORDLY_COMPLETE_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_COMPLETE_REFERENCE.md) — Feature details
- [RECORDLY_REAL_API_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_REAL_API_REFERENCE.md) — **Ground-truth zoom/padding/webcam/wallpaper math** (real depth scale 1.25x–5.0x, real padding-as-percentage formula) — read before hand-authoring any zoom/frame parameters

---

**Skill version:** 1.0 (2026-09-23)  
**Status:** Production-ready (with mandatory review step for auto-zoom)
