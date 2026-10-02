---
name: image-restoration-accuracy
description: |
  Restore poor-quality / unclear product images (blurry, compressed, screenshotted,
  low-res, glare-heavy) into a cleaner, more legible reference WITHOUT changing
  what the product actually is. Use whenever a source photo is too degraded to
  confidently read (brand, model, connector, port count, cable structure,
  packaging text) before it feeds a product listing, 3D model, technical diagram,
  scroll animation, or database entry. Especially: alwazour product photos that
  arrive blurry/low-res/screenshotted before photo_families.json ingestion.
triggers:
  - "unclear product image"
  - "blurry product photo"
  - "restore this image"
  - "upscale this product photo"
  - "can't read the label/model number"
  - "is this photo good enough to use"
  - "remove the logo/watermark/branding from this photo"
---

# Image Restoration & Accuracy

**Mission:** recover the maximum reliable visual information from a degraded
image without inventing what isn't there. Not "make it prettier" —
"prove what you can claim, label what you can't."

This is a **judgment protocol**, not a single tool. Claude has no local
image-editing engine — restoration passes are done by (a) reading the image
directly with Claude's own vision (inspection, OCR, before/after comparison),
(b) calling `fal-upscale` / `image-enhancer` (skills-library, off-context —
`python3 ~/.claude/overseer/search.py fal upscale` or `image-enhancer` to
pull them) for actual pixel-level super-resolution/denoise/deblur, and
(c) Python/PIL (already installed) for crop, perspective-correct, exposure
normalize, and multi-variant comparison grids. Never fabricate a "restored"
image by generative inpainting when the ask is factual (Mode A/B below) —
a generative model filling gaps is Reconstruction, not Recovery (see §3).

## 1. The three-state rule

Every claim about the product gets one label, always carried into output:

| State | Meaning |
|---|---|
| **CONFIRMED** | Directly, clearly visible in source pixels. |
| **PROBABLE** | Strongly implied by shape/context/another image of the same SKU, not fully legible. |
| **UNKNOWN** | Not recoverable from any available source. Say so — never guess silently. |

Never present PROBABLE or UNKNOWN as CONFIRMED. A model number you can't
fully read stays partially masked (`CAT6A U/???`) rather than autocompleted
to a plausible-sounding SKU.

## 2. Identity lock — never let restoration change

brand · logo · model/SKU · connector type & count · port arrangement ·
housing shape/proportions · cable count/construction · meaningful component
color · markings/warning/regulatory text · fastener positions · vent
pattern · packaging layout. If a restoration pass would nudge any of these
(a denoiser rounding off a screw, a super-res model "completing" a logo),
reject that pass and fall back to a more conservative one.

**This protects only branding physically part of the real product** (molded
into the case, printed on real packaging). It does NOT protect a
third-party overlay burned onto the photo after the fact — a seller's logo
band, a marketplace watermark, a Pinterest site-name stamp, a reseller's
corner badge. That overlay isn't product identity, it's noise sitting on
top of it, and removing it is in-scope. Tell the two apart before touching
anything: is the mark part of the object (protected) or laid over the
photo (removable)? When genuinely unsure, treat it as protected and ask.

**Removing an overlay watermark/logo → hand off to the `watermark-removal`
skill**, don't reinvent it here. Run it as its own pass, positioned after
geometry stabilization (§5 step 2) and before super-resolution (§5 step 3)
— cleaning the overlay first keeps the SR/denoise pass from baking watermark
edges into the product texture. `watermark-removal` already encodes the
crop → local-inpaint → AI-edit escalation and its own product-untouched
verification; this skill's §6 red-flag/verify pass still applies afterward
on top of it.

## 3. Recovery vs. Reconstruction — the hard boundary

- **Recovery** (allowed, default): denoise, deblur, deblock/decompress,
  super-resolution, perspective correction, exposure/white-balance fix,
  crop, OCR of existing text. All work on information already in the pixels.
- **Reconstruction** (forbidden for Mode A/B): inpainting a missing side,
  inventing hidden internal geometry, "completing" unreadable text,
  generating an unseen connector or packaging face. Only allowed in Mode C,
  and every reconstructed pixel must be labeled inferred/illustrative in
  the deliverable, never presented as photographic evidence.

## 4. Output modes — pick one before starting

| Mode | Use | License to alter |
|---|---|---|
| **A — Factual restoration** | product DB, spec extraction, technical docs | none beyond Recovery; max evidence preservation |
| **B — Presentation restoration** | listing photo, marketing crop | may clean lighting/background/composition; identity+geometry still locked |
| **C — Visual reconstruction** | concept render, illustrative-only | may reconstruct, but must be labeled inferred everywhere it appears |

Default to **Mode A** unless the user says otherwise. alwazour catalog work
is always Mode A/B — see §8.

## 5. Workflow

1. **Inspect** — read the image(s) directly (Claude vision). Classify
   degradation: blur type (motion/defocus/resize/compression), noise type,
   exposure issues, geometry distortion, source type (screenshot, WhatsApp
   recompress, photo-of-screen, catalog scan). If multiple images of the
   same product exist, treat them as one source set — a detail unclear in
   image 1 may be CONFIRMED from image 2's rear/label shot.
2. **Stabilize geometry first** — orientation, crop, perspective-rectify
   (PIL `ImageOps`/affine transform) before any pixel enhancement. Never
   sharpen a still-skewed image.
3. **Restore signal** — for real detail recovery beyond what direct
   reading gives you, call `fal-upscale` (super-resolution) and/or
   `image-enhancer` (denoise/deblur/decompression) from skills-library.
   Prefer structure-preserving/conservative settings; over-denoising turns
   screws, braiding, and embossed labels into plastic-looking smears —
   that's a red flag, redo with a lighter pass (see §7).
4. **Recover text** — crop the text region tight, rectify, then read it
   directly with Claude vision at native res AND on the enhanced crop.
   Compare the two readings: same characters → CONFIRMED, minor diff →
   PROBABLE, contradictory → UNKNOWN. Never round an uncertain model
   number/SKU up to a "clean-looking" one.
5. **Selective detail pass** — re-process only evidence-bearing regions
   (label, connector, fasteners, cable jacket, ports) at higher effort
   rather than globally over-sharpening the whole frame.
6. **Verify against source** — before/after check: does silhouette,
   connector count, port count, color, and text still match the original
   pixels? Any invented edge, duplicated screw, or symmetric feature that
   wasn't symmetric in source → reject the pass, fall back a step.
7. **Cross-check externally when identity is uncertain** — search by
   brand/model/connector combo (WebSearch/WebFetch) against manufacturer
   pages/datasheets first, distributor catalogs second. If a source
   contradicts the photo, record the conflict — don't silently overwrite
   the photo with the web result.
8. **Export + handoff** — see §6.

## 6. Downstream handoff (always produce this, even inline)

```
RESTORED_ASSET
- original_source: <path/url>
- restored_source: <path, if a new file was produced>
- mode: A|B|C
- processing_steps: <what was actually run>
- confirmed_features: [...]
- probable_features: [...]
- unknown_features: [...]
- text_detected: <raw + confidence>
- identity_confidence: 0-1
- geometry_confidence: 0-1
- recommended_downstream_use: <e.g. "safe for photo_families.json entry", "needs manufacturer photo instead">
- forbidden_assumptions: <explicitly list anything the next skill must NOT infer>
```

Any skill consuming this output (e.g. `alwazour-product-visualization`,
a 3D pipeline, a listing generator) treats it as a reference with known
gaps, never as permission to invent what's UNKNOWN.

## 7. Red flags — reject the restoration pass and redo lighter

double edges/haloing · waxy-plastic surfaces · fake-looking crisp text on a
region that was blurry · a connector that gained/lost a pin or port ·
duplicated screws · an asymmetric feature that became symmetric with no
evidence · repeated texture tiling (generative artifact) · a "too perfect"
technical surface. If restoration keeps producing these, stop — report the
source as **unrecoverable** rather than shipping a confident-looking guess.

## 8. alwazour integration

For alwazour catalog photos: this skill runs **before** a photo is fed into
`tools/ingest_pi.py` / considered for `photo_families.json`. If a candidate
source photo (Wikimedia Commons or invoice/product photo) is too degraded to
confirm connector type/count or read the label, run this skill first;
only a CONFIRMED identity record clears it for the pipeline described in
`alwazour-product-visualization/SKILL.md` §5. A PROBABLE/UNKNOWN result
means: keep searching for a better source, don't ingest the degraded one —
per that skill's hard rule that a real photo is never faked or guessed into
existence.

## 9. Confidence is a workflow signal, not science

Assigning `connector_type: 0.99, cable_gauge: 0.31` is there to decide what
needs a human/second source, not to be quoted as measured fact. Low
confidence on a Tier-1 feature (brand/model/connector) blocks publishing;
low confidence on Tier-4 (background, dust, cosmetic) never blocks anything.
