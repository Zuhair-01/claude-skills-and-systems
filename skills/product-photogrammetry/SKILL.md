---
name: product-photogrammetry
description: Turn a set of real multi-angle product photos into an actual measured 3D mesh (GLB) via RealityScan/RealityCapture's headless CLI, for the alwazour Product Technical Experience Engine. Use when a real GLB is needed for a product and single-image neural generation (fal-3d, Hunyuan3D, Stable Fast 3D) isn't accurate enough — real photogrammetry from real photos beats any single-image guess.
---

# Product Photogrammetry (RealityScan pipeline)

**Governing principle, same as `alwazour-product-visualization`:** the mesh must trace
back to real photos of the real physical product — never a single-image neural guess
dressed up as "3D scan," and never a hand-modeled placeholder presented as final. If no
real multi-angle photo set exists yet for a SKU, the honest state is the existing
placeholder/single-image fallback (see that skill's §46 fallback hierarchy and §2.5), not
a fabricated "photogrammetry" result.

## Why this exists

Single-image tools (fal-3d, Hunyuan3D-2.1, Stable Fast 3D) infer geometry they can't see
— the back of a connector, the true cable diameter, real proportions — from training-data
priors, not measurement. RealityScan (formerly RealityCapture, Epic Games) reconstructs
from actual multi-angle photos of the real object: structure-from-motion + multi-view
stereo, so occluded geometry isn't guessed, it's triangulated from another photo that
actually saw it. Free for individuals/businesses under $1M annual revenue (still requires
a free Epic Games account + EULA acceptance — not open-source, unlike Meshroom).

## Prerequisites (one-time, human-driven — never do these yourself)

1. A free Epic Games account (epicgames.com) — account creation is prohibited for
   Claude to do on the user's behalf; the user does this themselves.
2. RealityScan installed (realityscan.com or via Epic Games Launcher).
3. Confirm the install path once, e.g. `C:\Program Files\Epic Games\RealityScan\RealityScan.exe`
   — every command below assumes that binary exists and is licensed/activated.

## Photo capture checklist (real, physical — the human does this part)

Before any CLI step, a real photo set must exist for the exact SKU:

- Plain matte, non-reflective background (patterned surfaces confuse feature matching)
- Soft, even, diffuse lighting — no harsh shadows or specular hotspots on metal shells
- 25-35 full-circle shots at a consistent distance, 60-70% overlap between consecutive
  frames, plus a few shots from slightly above/below
- 8-10 additional macro close-ups on the highest-detail component (e.g. a connector end)
  — this is what a scroll-story macro scene will zoom into
- The product stays physically still; only the camera moves
- **A real ruler or known-length object in at least a few frames, clearly visible and in
  focus** — this is what lets the mesh get correct real-world scale (see "Real-world
  scale" below); skip it only for a product whose exact length/diameter is already a
  verified field in `products.csv` (e.g. `HDMI-1-5M-20`'s 1500mm), which can rescale the
  mesh after the fact instead.
- Save to `data/real/scans/<slug>/photos/*.jpg` in the alwazour repo (new directory,
  gitignored — raw scan photos and intermediate RealityScan project files are large and
  don't belong in git; only the final compressed GLB does)

Never proceed to reconstruction on a photo set that doesn't meet this bar — a rushed
15-photo set with harsh shadows produces a worse mesh than the single-image neural
fallback, which defeats the entire point of choosing photogrammetry.

### Metal/shiny connectors need surface prep first — this is not optional

**Photogrammetry fundamentally cannot reconstruct a specular (mirror-like) surface** —
feature-matching needs consistent surface detail across photos, and a reflection changes
with every camera angle, so the algorithm either fails to align those regions or bakes in
phantom geometry. Every HDMI/USB/connector shell in this catalog is exactly this case
(polished or plated metal). Real, verified mitigations, in order of preference:

1. **Matte scanning spray** (3D-scanning-specific dulling spray, sold for this exact
   purpose) — light, even coat, fully removable afterward with no residue.
2. **Foot/foundation powder** as a cheap substitute — a light dusting achieves a similar
   matte diffusion if scanning spray isn't on hand.
3. **Cross-polarization** (a polarizing filter on the light source AND the camera lens,
   oriented perpendicular to each other) reduces glare but does *not* restore surface
   detail on its own — real sources confirm a polarizer alone still scans poorly; only
   combine it with surface prep, never use it as a substitute for dulling the surface.

Do this to the metal shell before the capture session, not after a failed scan — a
scan attempted on an untreated shiny connector will show as visible holes, phantom
bumps, or a smeared/melted-looking shell in the mesh, and no amount of cleanup fixes that
after the fact; the photos themselves lack the information.

## Headless CLI pipeline

RealityScan supports full command-line automation via `-headless` — every step below is
scriptable, no GUI interaction needed once photos exist. Commands below are verified
against RealityScan's own documentation (rshelp.capturingreality.com → Command Line
Interface / List of All CLI Commands / Reconstruction Commands / Model Export) as of this
skill's last research pass — re-verify against the installed version's own command list
if a command errors, since flags have changed across releases.

**One-time manual step before the pipeline is fully scriptable**: RealityScan's
`-exportModel`/`-exportSelectedModel` CLI commands take an *export-parameters XML file*
(controls mesh format — OBJ/GLB/FBX/STL —, texture format/resolution, decimation, axis
orientation), and that XML has no documented hand-written syntax — the real workflow is
to export once through the GUI, then copy the `<ModelExport>` block out of the `.rsinfo`
file RealityScan writes alongside that export into a standalone `glb_export_params.xml`.
Every export after that first one is fully CLI-driven by referencing this same params
file. Do this once per output need (e.g. once for "web GLB, Draco-friendly, no baked
normals since gltf-transform adds those") — not once per product.

Real batch-script conventions: `^` continues a command onto the next line, `-set
"Param=value"` overrides a specific setting inline, `#`/`//`/`REM` lines are comments.

```bat
"C:\Program Files\Epic Games\RealityScan\RealityScan.exe" -headless ^
  -newScene ^
  -addFolder "data\real\scans\<slug>\photos" ^
  -align ^
  -selectMaximalComponent ^
  -setReconstructionRegionAuto ^
  -calculateNormalModel ^
  -selectMaximalComponent ^
  -simplify <target-triangle-count> ^
  -smooth ^
  -calculateTexture ^
  -exportModel "Model 1" "data\real\scans\<slug>\raw.glb" "glb_export_params.xml" ^
  -save "data\real\scans\<slug>\project.rsproj" ^
  -quit
```

Notes on the real, non-obvious steps in that chain:

- **`-setReconstructionRegionAuto` (or `-setReconstructionRegionByDensity` for a tighter
  crop) matters** — without it, RealityScan may mesh the whole capture volume including
  background/turntable clutter caught at the edges of frame, not just the dense object
  point cloud. Crop before meshing, not after.
- **`-calculateNormalModel` vs `-calculateHighModel`**: normal quality is the right
  default for a small handheld object at this photo count; reserve high quality (much
  slower) for a product whose macro connector detail genuinely needs finer geometry after
  a first normal-quality pass looks insufficient — don't default to high quality
  everywhere, it costs real processing time for often-marginal gain at this object scale.
- **`-simplify` target and texture resolution**: start around 30-60k triangles / 2048px
  texture pre-compression for a cable/connector, then let `gltf-transform` (see below) do
  the real web-weight reduction via Draco + KTX2 — don't try to hit final web-weight
  triangle counts directly out of RealityScan, its decimation is optimized for visual
  mesh quality, not web delivery size.

### Real-world scale — use the catalog's own verified data first

RealityScan's native scaling tool is `defineDistance` (place two control points across a
known real measurement, tell it the true distance) — genuinely useful when no other
source of scale exists, but it's an interactive/GUI-first tool with no simple scripted
syntax for defining new point pairs blind. **For this catalog specifically, there's a
better source already sitting in `products.csv`**: a cable's real length (`HDMI-1-5M-20`
→ 1500mm), a connector's real known standard dimension, etc. are already verified data
this project trusts. Post-process the exported GLB with a small script that measures the
mesh's own bounding box (or two identifiable landmark vertices) along its long axis and
applies one uniform scale factor to match the *already-verified* real dimension — this
reuses data this project already trusts instead of re-deriving scale through RealityScan's
GUI-driven control-point tool per product. Fall back to `defineDistance` with a real
ruler in frame only for a product with no verified dimension in `products.csv` yet.

## After export: same pipeline as §2.5's other GLB sources

The raw RealityScan export feeds into the exact same downstream steps already built for
fal-3d/Hunyuan3D output — no new integration path:

1. Compress with `@gltf-transform/cli` (already installed in `alwazour/package.json`):
   Draco geometry + KTX2/webp textures, per `alwazour-product-visualization/SKILL.md`
   §2.5 and §44's performance requirement (this site targets throttled 3G).
2. Save to `public/products/<slug>/hero.glb` (or whichever real path the R3F
   `ExperienceProduct.glbUrl` convention lands on).
3. `ProductModel` (in `src/experience/`) already prefers a real GLB over the placeholder
   the moment `glbUrl` is set — no code change needed, just point it at the new file.

## Quality gate before calling a scan "done"

- Does the mesh actually look like the specific real product when compared side-by-side
  with its own reference photo — not just "a plausible cable"?
- Zoom to the connector macro level: are the shell proportions, contact block position,
  and strain-relief boot recognizable as the real part, not smoothed into a blob?
- Does the exported/compressed GLB still hold up after Draco+KTX2 compression, or did
  compression destroy the one thing photogrammetry bought over the neural fallback (real
  measured detail)? Check both the raw and compressed export before deciding compression
  settings are acceptable — this is a real tradeoff, not a fixed answer.
- If the scan looks worse than the existing single-image fallback for this SKU, don't
  ship it — that means the photo set didn't meet the capture checklist, not that
  photogrammetry failed as an approach. Re-shoot rather than settle.

## Learn-and-improve loop

Keep a short running note (in this file, or a sibling `NOTES.md` in this skill's
directory) of what actually worked per product category once real scans start
happening — lighting setups that worked/failed, triangle-count/texture-size sweet spots
for cables vs. boxier products like a cabinet or PDU, CLI flag names that changed between
RealityScan versions. This skill should get more precise with real use, not stay
static — the user explicitly asked for "learn as you go and improve."

## Relationship to other skills

- `alwazour-product-visualization` — the governing skill for the whole alwazour site;
  this skill is one *source* for the GLBs that skill's §2.5 R3F pipeline consumes.
- `fal-3d` / free single-image tools (Hunyuan3D-2.1, Stable Fast 3D via Hugging Face
  Spaces) — the fallback path when no real multi-angle photo set exists yet for a SKU.
  Prefer this skill's output over those whenever a real photo set exists; never claim a
  single-image result is "photogrammetry."
