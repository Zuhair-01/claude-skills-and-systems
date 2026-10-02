---
name: watermark-removal
description: Remove overlay watermarks, seller logos, and baked-in marketplace text from product/reference photos before shipping them on a site. Use when a sourced image (Pinterest, a marketplace listing, an invoice photo) has a logo band, diagonal repeating text, or a corner stamp burned into the pixels. Does NOT relicense the image and does NOT fix branding physically printed on the real product itself.
---

# Watermark Removal

**The pixels are the ONLY thing this touches. It never changes what license an
image carries** — stripping a Pinterest re-pin's watermark doesn't make it
yours to use commercially. If the source itself is legally risky (see
`open-pinterest`'s licensing note), fix the source, not the watermark.

**It also never touches branding that is physically part of the real
product** — text molded into a plastic case, a logo printed on real
packaging. That is the object, not an overlay; "removing" it with inpainting
or AI editing fabricates the product photo. If the branding is on the object
itself, re-source a different real photo instead of editing this one.

Use this only for an overlay added on top of a real photo after the fact: a
seller's logo band along one edge, a diagonal repeating "SAMPLE" / site-name
text tiled across the frame, a corner badge, a URL stamp.

## Pick the technique by what the watermark actually is

| Watermark shape | Technique | Cost |
|---|---|---|
| Sits in a strip/corner, product still fills the frame after cutting it away | **Crop** | Free, instant, zero fabrication |
| Small logo/text stamped over a plain/simple background | **OpenCV inpaint** (local) | Free, instant |
| Large or diagonal repeating text over a complex/detailed background | **AI edit** (`edit` skill / muapi.ai) | Costs API credits, best quality |

Always try crop first — it invents nothing. Reach for inpaint only when the
mark truly overlaps product detail you can't just cut away. Reach for the AI
tier only when local inpaint's result looks smeared (check the output before
shipping it — see Verify below).

## 1. Crop — free, use whenever the watermark hugs an edge

```bash
python3 ~/.claude/skills/watermark-removal/scripts/remove_watermark.py crop \
  IN.jpg OUT.jpg --top 0 --bottom 40 --left 0 --right 0
```
Margins are pixels, measured off the real image (zoom/screenshot it first —
never guess coordinates). If cropping would cut into the actual product,
this is the wrong technique; move to inpaint or AI edit instead.

## 2. Local inpaint — free, for a small stamp on simple background

```bash
python3 ~/.claude/skills/watermark-removal/scripts/remove_watermark.py inpaint \
  IN.jpg OUT.jpg --box 400,20,620,80 --box 10,10,90,50
```
- `--box x0,y0,x1,y1` (repeatable) — pixel coordinates of each watermark
  region, top-left origin, from a real look at the image, not a guess.
- Uses OpenCV Telea inpainting (`--method ns` for the Navier-Stokes variant
  if Telea looks wrong on a particular image — try both, keep the better one).
- This *fabricates* the pixels under the mask from surrounding texture. Fine
  for a small mark on a flat/simple area (a plain background, a solid-color
  cable jacket). Looks visibly smeared on anything with fine real detail
  (product labeling, a busy background, a textured surface) — check the
  result at full zoom before using it; don't trust the script blind.
- The script warns when a mask covers >15% of the frame — that's the signal
  to stop trusting local inpaint and move to the AI tier or re-source instead.

## 3. AI edit — best quality, costs credits, for hard cases

For a watermark too large/detailed for local inpaint to reconstruct
convincingly (diagonal repeating site-name text across a photo, a
semi-transparent logo over real product detail), use the `edit` skill
(`muapi-media-editing`, `~/.claude/skills-library/edit/SKILL.md`):

```bash
bash enhance-image.sh --op background-remove --image-url "https://..."   # if isolating the subject also solves it
bash edit-image.sh --image-url "https://..." --prompt \
  "remove the watermark text and logo overlay, keep the product exactly unchanged, do not alter shape/color/text on the product itself" \
  --model flux-kontext-pro
```
Requires `MUAPI_KEY` (see `core/platform/setup.sh`) and a reachable image URL
(upload the local file somewhere fetchable first, or use whatever the `edit`
skill's own upload path is — check its SKILL.md). Always inspect the result:
a prompt-based edit can subtly redraw product details along with the
watermark — reject and retry with a tighter prompt if the product itself
changed.

## Verify before shipping — every time, no exceptions

Open the output at full resolution (zoom, not the thumbnail) and check:
- [ ] The watermark is actually gone, not just faded/blurred
- [ ] No fabricated texture bleeds into a part of the product a customer
      would actually look at (a connector, a label, a port) — smeared
      background fill is fine, smeared product detail is not
- [ ] Nothing about the real product changed shape, color, or text
- [ ] If none of the three techniques gets a clean result, the honest move
      is re-sourcing a different photo, not shipping a degraded edit

## Batch note

For many images in one pass (a product catalog sweep), still look at each
one before picking crop vs inpaint vs AI — the "smallest technique that
actually removes the mark cleanly" call is per-image, a fixed margin/box
that worked for one photo will crop into the product on another.
