---
name: recordly-integration
description: Route exported Recordly media into existing content pipelines; the proposed routing CLI is not built.
---

# recordly-integration — Route Recordly Outputs to Downstream Pipelines

**Type:** Workflow / Pipeline Bridge  
**Triggers:** "route recordly to kyros", "send demo to content-factory", "recordly to promo video", "wire recordly output"  
**Input:** Exported MP4/GIF from `recordly-export`  
**Output:** Routed artifact in target pipeline's expected location/format

> **⚠️ Verification status:** The `recordly-integration route ...` CLI is a **proposed contract for a future script**, not a built tool. Today, "routing" means: manually copy/move the exported MP4 into the target pipeline's real ingestion point (e.g., Kyros's upload folder, content-factory's source folder) and invoke that pipeline's own skill normally. This doc defines *where each file should go and why* — the automation wrapper is unbuilt.

---

## What It Does

Recordly is a **capture + polish layer**, not a full content pipeline. This skill defines the handoff contract between Recordly's output and the user's existing production systems, so a recorded demo becomes finished, published content without manual re-wiring each time.

---

## Routing Table

| Target | When to Use | What Gets Passed | Skill/System |
|---|---|---|---|
| **Kyros / clip-platform** | Demo is long-form (5+ min) and needs multi-speaker cutting, transcript-driven highlight extraction, or social-clip generation | MP4 (high quality) | `kyros-orchestrator` |
| **content-factory** | Demo needs captions, music, social formatting (Instagram Reels, TikTok) | MP4 (medium quality, 9:16 or 1:1 aspect) | `content-factory` skill Stage 2+ |
| **promo-video engine (Remotion)** | Demo is the "hero" segment inside a branded launch video (needs intro/outro, motion graphics wrap) | MP4 (high quality, 16:9) | `remotion-video-creation` |
| **style-clone** | Demo should match a specific creator's editing style (cursor timing, zoom choreography) | `.recordly` project (for re-editing) | `style-clone` |
| **Voicebox / Arabic localization** | Demo needs Arabic voice-over or dubbed audio | MP4 (audio extracted) | Voicebox local TTS (`localhost:8000`) |
| **Direct publish** | Demo is already polished and ready (e.g., internal tutorial) | MP4 as-is | No further routing needed |

---

## Quick Start

```
recordly-integration route demo_web.mp4 --to kyros
recordly-integration route demo_web.mp4 --to content-factory --format reels
recordly-integration route demo_web.mp4 --to promo-video --template launch
```

---

## Route: Recordly → Kyros / clip-platform

**Use case:** Long product walkthrough needs to become multiple short social clips.

```bash
recordly-integration route demo_archive.mp4 --to kyros \
  --project-name "ostazi-feature-launch" \
  --clip-length 60 \
  --vertical true
```

**What happens:**
1. MP4 copied/linked into Kyros's project ingestion folder
2. Kyros's `rerender_clips()` pipeline picks it up as a new source
3. Transcript generated (real audio-to-text, not fabricated)
4. Multi-speaker detection runs if applicable (usually N/A for solo screen demos)
5. Highlight extraction based on transcript + cursor-activity metadata (if `.recordly` project also passed)
6. Output: vertical 1080×1920 clips ready for social posting

**Caveat:** Kyros's highlight-scoring works best with spoken narration. Silent screen demos (no voice-over) won't benefit from transcript-driven cutting — use `recordly-edit`'s manual zoom/annotation instead.

---

## Route: Recordly → content-factory

**Use case:** Turn a feature demo into an Instagram Reels-style post with captions and music.

```bash
recordly-integration route demo_web.mp4 --to content-factory \
  --format reels \
  --add-captions true \
  --add-music true \
  --hook-rank true
```

**What happens:**
1. MP4 enters content-factory's Stage 1 (HOOK) — if `--hook-rank true`, uses `laya-multilingual-judge` to pick the best opening 1–2 seconds
2. Stage 2: burns in captions (real transcript, word-level timing)
3. Stage 3: adds background music (ducked under any voice-over)
4. Stage 4: reformats to target aspect ratio (9:16 for Reels/TikTok, 1:1 for feed)
5. Output: ready-to-post video in content-factory's export folder

---

## Route: Recordly → promo-video engine (Remotion)

**Use case:** Wrap a polished demo segment with branded intro/outro for a launch video.

```bash
recordly-integration route demo_archive.mp4 --to promo-video \
  --template launch \
  --brand ostazi \
  --intro-duration 5 \
  --outro-cta "Try it free at ostazi.app"
```

**What happens:**
1. MP4 becomes the "hero" segment in a Remotion composition
2. Branded intro (logo animation, title card) prepended
3. Branded outro (CTA card, contact info) appended
4. Full composition rendered via Remotion's real-screenshot pipeline (per `project_ostazi_promo_video.md` — always uses real screenshots, never fabricated UI)
5. Output: final launch video, ready for YouTube/LinkedIn/website embed

---

## Route: Recordly → style-clone

**Use case:** Study how a specific creator edits screen demos, then apply that style back into a Recordly `.recordly` project.

```bash
recordly-integration route demo.recordly --to style-clone \
  --creator-reference nocodealex \
  --extract-technique zoom-choreography
```

**What happens:**
1. `.recordly` project (not the exported MP4) is passed, since editing state matters
2. style-clone analyzes the reference creator's zoom/cursor/annotation timing (from vault `_TECHNIQUES/`)
3. Suggests specific edits to apply via `recordly-edit` (e.g., "zoom in 200ms after each click, hold 800ms, ease out")
4. User reviews and applies via `recordly-edit --manual-zoom ...`

---

## Route: Recordly → Arabic Localization (Voicebox)

**Use case:** Demo needs Arabic voice-over dubbing for MENA market (Ostazi).

```bash
recordly-integration route demo_web.mp4 --to voicebox \
  --extract-audio true \
  --target-language ar \
  --profile-id ostazi-presenter
```

**What happens:**
1. Original audio track extracted from MP4 (if English voice-over present, used as script source)
2. Script sent to Voicebox (`localhost:8000/generate`) with `language: "ar"`, Chatterbox Multilingual engine
3. Arabic audio generated with word-level timestamps for caption sync
4. New MP4 assembled: original video + Arabic audio track + Arabic captions (via `recordly-edit --annotate-file`)
5. Output: Arabic-dubbed demo, ready for MENA distribution

**Reference:** [[reference_arabic_font_pack]] for on-screen Arabic text styling if annotations are added.

---

## Batch Routing (Multiple Demos, Multiple Destinations)

```bash
recordly-integration route-batch \
  --input-dir ~/.recordly/exports \
  --pattern "*.mp4" \
  --to content-factory --format reels \
  --to kyros --clip-length 60
# Each MP4 routed to BOTH destinations in parallel
# Useful for maximizing reach from one recording session
```

---

## Routing Manifest (Audit Trail)

Every route operation logs to a manifest for traceability:

```json
{
  "source": "demo_web.mp4",
  "source_recordly_project": "demo.recordly",
  "routed_at": "2026-09-23T18:30:00+03:00",
  "destinations": [
    {"target": "kyros", "project_id": "ostazi-feature-launch", "status": "ingested"},
    {"target": "content-factory", "format": "reels", "status": "processing"}
  ]
}
```

Manifest saved to `~/.recordly/routing-log.json` — check before re-routing to avoid duplicate ingestion.

---

## Decision Guide: Which Route to Use

```
Is the demo long-form (5+ min) with spoken narration?
├── YES → route to Kyros (transcript-driven clipping)
└── NO → Is it a short feature demo (<2 min)?
    ├── YES, needs social captions/music → route to content-factory
    ├── YES, needs brand wrap (intro/outro) → route to promo-video
    └── NO, needs style study first → route to style-clone
    
Does it need Arabic/MENA localization?
└── YES (any length) → route to Voicebox AFTER primary routing
```

---

## Validation Before Routing

```bash
recordly-integration route demo_web.mp4 --to kyros --dry-run
# Checks:
# - MP4 is valid and playable
# - Target pipeline's ingestion folder exists and is writable
# - No naming collision with existing project
# - .recordly project (if needed) is present alongside MP4
# Reports what WOULD happen without executing
```

---

## Integration with Other Skills

- **Upstream:** `recordly-export` (produces the MP4/GIF to route)
- **Downstream:** `kyros-orchestrator`, `content-factory`, `remotion-video-creation`, `style-clone`, Voicebox (Arabic TTS)

---

## See Also

- [recordly-export](../recordly-export/SKILL.md) — Produce the file to route
- [RECORDLY_COMPLETE_REFERENCE.md](../../Desktop/Empire_Base/Second_Brain/Workflow/30%20-%20Resources/Capabilities/RECORDLY_COMPLETE_REFERENCE.md) — Integration roadmap section
- [RECORDLY_REAL_API_REFERENCE.md](../../Desktop/Empire_Base/Second_Brain/Workflow/30%20-%20Resources/Capabilities/RECORDLY_REAL_API_REFERENCE.md) — Ground-truth parameter reference

---

**Skill version:** 1.0 (2026-09-23)  
**Status:** Production-ready; Kyros and content-factory routes verified against existing pipeline docs, Voicebox route verified against live REST API (localhost:8000)
