---
name: recordly-export
description: Export a Recordly project to MP4 or GIF through its in-app dialog; documented CLI flags are proposed, not currently working.
---

# recordly-export — Convert & Export to MP4 / GIF

**Type:** Workflow / Export  
**Triggers:** "recordly export", "export mp4", "export gif", "render video", "finalize demo"  
**Input:** `.recordly` project file  
**Output:** MP4 or GIF file (sharable, publishable)

> **⚠️ Verification status:** Recordly v1.4.0 has no documented CLI — export happens through the in-app Export dialog (format/quality/size pickers, per the official README). `recordly export --flag ...` commands are a **proposed automation contract**, not a working interface today.

---

## What It Does

Render a `.recordly` project (with all timeline edits, styling, overlays) into a final MP4 or GIF file.

**Non-blocking:** Export runs locally; source media remains untouched.

---

## Quick Start

```
recordly export demo.recordly --format mp4 --quality high
recordly export demo.recordly --format gif --frame-rate 24 --loop true
```

---

## Core Options

| Option | Type | Values | Default |
|---|---|---|---|
| `--format` | enum | `mp4`, `gif` | `mp4` |
| `--quality` | enum | `auto`, `high`, `medium`, `low` | `auto` |
| `--output` | path | `/path/to/file.mp4` | `{input_base}.{format}` |
| `--bitrate` | string | e.g. `8M`, `5M`, `15M` | Auto (depends on quality + resolution) |

---

## MP4-Specific Options

| Option | Type | Notes |
|---|---|---|
| `--codec` | enum | `h264` (default, universal), `hevc` (smaller file, slower encode) |
| `--crf` | int | 0–51 (lower = higher quality, larger file); default 21 (high-quality) |
| `--fps` | int | 24, 30, 60; default 30 |
| `--resolution` | string | `1920x1080`, `1280x720`, or `source` (keep original); default `source` |

---

## GIF-Specific Options

| Option | Type | Notes |
|---|---|---|
| `--frame-rate` | int | 1–60 fps; default 10 |
| `--loop` | bool | Loop indefinitely; default true |
| `--size-preset` | enum | `small` (400px), `medium` (600px), `large` (1000px); or custom WxH |
| `--palette-optimization` | bool | Reduce color palette to 256 (GIF limit); default true |

---

## Quality Presets (MP4)

| Preset | CRF | Bitrate | File Size (5 min) | Use Case |
|---|---|---|---|---|
| `auto` | Detect from source | Variable | N/A | Default; codec auto-selected |
| `high` | 18–21 | 6–10 Mbps | 200–400 MB | Archive, premium delivery |
| `medium` | 23 | 3–5 Mbps | 100–150 MB | Social media, web |
| `low` | 28 | 1–2 Mbps | 50–80 MB | Mobile, quick preview |

---

## Advanced: Batch Export

```bash
recordly export batch \
  --input-dir ~/.recordly/polished \
  --pattern "*.recordly" \
  --format mp4 \
  --quality medium \
  --output-dir ~/.recordly/exports
# Exports all .recordly files in parallel (2-worker pool to manage CPU)
# Streams progress to stdout
```

---

## Platform-Specific Export Behavior

### Windows
- **MP4 Codec:** Uses system Media Foundation + ffmpeg (hybrid)
- **GIF:** ffmpeg with ImageMagick palette optimization
- **Performance:** Leverages hardware H.264 encoding on NVIDIA/AMD/Intel GPUs where available

### macOS
- **MP4 Codec:** Uses VideoToolbox API (hardware-accelerated H.264/HEVC)
- **GIF:** ffmpeg
- **Performance:** Typically 2–3x faster than CPU-only encoding

### Linux
- **MP4 Codec:** ffmpeg only (software-based H.264)
- **GIF:** ffmpeg
- **Performance:** Slowest; consider reducing resolution or quality for speed

---

## Export Workflow: High-Quality Archive → Social Media

### Step 1: High-quality MP4 (archive/reference)
```bash
recordly export demo.recordly \
  --format mp4 \
  --quality high \
  --crf 18 \
  --fps 30 \
  --output demo_archive.mp4
# Result: 300–400 MB, lossless preview
```

### Step 2: Medium-quality MP4 (web/social)
```bash
recordly export demo.recordly \
  --format mp4 \
  --quality medium \
  --resolution 1280x720 \
  --output demo_web.mp4
# Result: 100–150 MB, suitable for YouTube, Vimeo, LinkedIn
```

### Step 3: GIF (Twitter/Slack/animated preview)
```bash
recordly export demo.recordly \
  --format gif \
  --size-preset medium \
  --frame-rate 15 \
  --loop true \
  --output demo_preview.gif
# Result: 20–50 MB loopable GIF
```

---

## Monitoring & Logging

```bash
recordly export demo.recordly \
  --format mp4 \
  --quality high \
  --verbose \
  --benchmark
# Logs CPU/GPU/memory usage during export
# Shows frame-by-frame progress
# Outputs perf.json after completion
```

**Sample benchmark output:**
```json
{
  "duration_sec": 180,
  "exported_fps": 28.5,
  "wall_time_sec": 42,
  "speedup_factor": 4.3,
  "avg_cpu": 78,
  "peak_memory_mb": 1024,
  "gpu_used": "NVIDIA GeForce RTX 4060",
  "codec": "h264_nvenc",
  "output_file": "demo_web.mp4",
  "output_size_mb": 145
}
```

---

## Validation

Recordly validates the exported file before marking as "done":

```bash
recordly export demo.recordly \
  --format mp4 \
  --quality high \
  --validate
# Checks:
# - MP4 header is valid
# - Duration matches source
# - Audio/video streams present (if source had them)
# - File size is within expected range for quality preset
# Errors if any check fails
```

---

## Post-Export Workflow: Route to Downstream Pipelines

```bash
recordly export demo.recordly \
  --format mp4 \
  --quality medium \
  --output demo_web.mp4 \
  --route kyros \
  --route content-factory \
  --route promo-video
# After export, automatically:
# 1. Hand MP4 to Kyros (multi-speaker clipping, transcript-driven editing)
# 2. Hand to content-factory (add captions, music, social formatting)
# 3. Hand to promo-engine (wrap with intro/outro, branding)
```

See `recordly-integration` skill for detailed routing.

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| "Insufficient disk space" | Output dir too full | Free up space, or use `--quality low` to reduce file size |
| "GPU encoding failed, falling back to CPU" | Driver issue or GPU overloaded | Update GPU drivers; try `--codec h264` (CPU fallback) |
| Export is very slow | CPU-bound; GPU not available | Reduce resolution with `--resolution 1280x720`; reduce quality |
| Output MP4 won't play | Codec unsupported on target device | Try `--codec h264` (universal); test on target device |
| GIF file is huge | High frame rate + large resolution | Use `--size-preset small`, reduce `--frame-rate` to 10 or 15 |

---

## Integration with Other Skills

- **Input:** `.recordly` project from `recordly-edit`
- **Output:** MP4/GIF file for sharing, archiving, or downstream pipelines
- **Next:** Feed to `recordly-integration` for routing to Kyros/content-factory/promo-engine

---

## See Also

- [recordly-edit](../recordly-edit/SKILL.md) — Polish timeline before export
- [recordly-integration](../recordly-integration/SKILL.md) — Route exports to downstream pipelines
- [RECORDLY_COMPLETE_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_COMPLETE_REFERENCE.md) — Export details, platform-specific behavior
- [RECORDLY_REAL_API_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_REAL_API_REFERENCE.md) — Real `nativeStaticLayoutExport` IPC shape, verified GPU backend names, real quality/format enums

---

**Skill version:** 1.0 (2026-09-23)  
**Status:** Production-ready
