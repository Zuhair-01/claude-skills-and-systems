---
name: open-pinterest
description: Find real-world UI/UX/3D/motion references on Pinterest, download the actual images AND videos into the project, edit/customize them (including subject-only background-removed cutouts), then hand them to the design skills (taste-skill, motion-ui, threejs, frontend-design) to build tailored components. Use when a project needs visuals we can't generate ourselves — 3D elements, floating components, scroll animations, motion-graphics loops, hero art, texture/background refs, icon/component refs — and the ask mentions "Pinterest", "find inspiration", "get a reference", "download and use this look", or wants a video/motion pin, not just a still.
---

# Open Pinterest

For arbitrary UI/3D/motion assets where an existing real design already has the look wanted,
this skill goes to Pinterest, finds it, downloads the real images **and videos**, and wires
them into the frontend build — customized/edited as needed (including cutting a subject out of
its background), not just used as a moodboard.

**For a photoreal marketing photo/video where the exact scene is brand-specific** (a real
person/setting that needs to match the brief exactly, not "close enough" from an existing
photo) — `web-imagegen` (Qwen/Gemini) generates it from scratch instead of sourcing; write the
prompt per `no-ai-slop-visuals` first. Use Pinterest when a matching real photo/reference
already exists or the need is UI/3D/motion reference rather than a usable final photo/video.

## Sibling sources (pick via `frontend-reference-sources`)
Pinterest is the **broad net**. If the ask is narrower, that router points elsewhere first:
`refero.design` (real product-UI screens), `supahero.io` (hero sections), `60fps.design` (motion/
interaction clips), `21st.dev`→`magic-ui-generator` (component code), `motion.dev`→`motion-ui`
(coding the animation). The sourcing/eval/wire-in/completion-gate protocol below applies to all of them.

## When to use
- Need 3D-style hero elements, floating/glass/blob shapes, textures, backgrounds, illustration
  style refs, icon/component refs, or a specific scroll/motion *look* to replicate in code.
- The reference is a **video or motion-graphics pin** (a loop, transition, camera move) rather
  than a still image — this skill downloads those too via `scripts/download_video.py`, it isn't
  images-only.
- Only the *subject* of a reference photo matters, not the background it was shot against —
  `scripts/remove_bg.py` cuts it out as a transparent PNG.
- User says "find X on Pinterest and use it" / "get that vibe" / "download some refs" / "get me
  a video/animation reference".
- User points at a *specific image* (a pin, a pasted screenshot, "find more like this one") rather
  than describing a style in words — use the visual-search drill-down (step 2b: open the pin,
  read its "More like this"/crop-similarity grid, walk closest-match to closest-match) instead of
  guessing keywords for something that's easier to match by eye than by caption.

## Query intelligence (do this before searching)

A vague ask like "make it look cool" or "3D stuff" returns junk on Pinterest. Translate the
actual brief into 2-4 specific, jargon-precise queries before touching the browser:

1. Extract the real intent: what element (hero, card, nav, cursor, loader, background), what
   physical/visual metaphor (glass, liquid, paper, clay, chrome, aurora), what motion (parallax,
   scroll-scrub, magnetic hover, marquee, morph), what mood (brutalist, editorial, luxury,
   playful, cyberpunk, minimal-swiss).
2. Compose queries as `<element> <material/style> <motion> ui` — e.g. project says "make the
   hero pop, kinda futuristic" → try `"3D floating glass hero ui"`, `"holographic gradient hero
   section"`, `"scroll parallax 3d hero website"`. Fan out 2-4 variants rather than one guess;
   different phrasings surface different pin clusters on Pinterest.
3. Reuse the project's own vocabulary if it has a brand/design doc (frontend_master_spec,
   BRAND.md, taste-skill brief) — pull adjectives from there instead of inventing new ones, so
   the references actually match the project's direction.
4. If results still look generic/stocky, add a qualifier: `award winning`, `awwwards`, `dribbble
   shot`, `behance case study` — these bias Pinterest toward curated design-site pins over random
   photos.

## Flow

1. **Search Pinterest via the browser** (`claude-in-chrome` skill — load its tools first if
   deferred). Navigate to `https://www.pinterest.com/search/pins/?q=<query>` with a specific
   query (e.g. "3D glassmorphism floating card UI", "dark saas hero scroll animation").
   Scroll to load enough pins (15-30 per query — you need a real pool, not just what's above the
   fold) — run each query from step 0 separately rather than one long combined string,
   Pinterest's ranking degrades fast on multi-clause queries.

2. **Actually look at every candidate before picking — don't grab the first N.** A caption
   match is not a visual match; Pinterest's own ranking is noisy and mixes in near-misses,
   stock photos, and unrelated boards. For each candidate pin:
   - Read the pin at real resolution (screenshot or `read_page` image) and judge it against the
     actual brief from step 0 — element type, material/style, motion implied by the composition,
     mood. Reject anything that's a caption-keyword match but a visual miss (wrong subject,
     wrong style era, low production quality, watermarked stock).
   - For video pins, don't judge off the thumbnail — thumbnails are often a random frame.
     Open the pin, let it play a few seconds (or check `read_network_requests` for the actual
     clip), and confirm the *motion* is what's wanted (the loop style, camera move, transition
     timing) — a still frame can look right and the actual animation still be wrong.
   - Rank the surviving pool and keep only the ones that genuinely fit; it's fine to end up with
     3 great refs from 25 candidates instead of forcing 10.

   **Fast bulk-collect (once you know which pins on a search grid are keepers):** instead of
   clicking into each pin individually, run one `javascript_tool` pass on the search results page:
   ```js
   Array.from(document.querySelectorAll('img')).map(i => i.src)
     .filter(s => s.includes('pinimg.com'))
     .map(s => s.replace('/236x/','/736x/').replace('/474x/','/736x/')) // upsize thumbnails
   ```
   This grabs every visible pin's image URL in one round-trip instead of one navigate+click per
   pin. For video pins on the same grid, collect page links separately (thumbnails are `<img>`,
   not the video): `Array.from(document.querySelectorAll('a[href*="/pin/"]')).map(a => a.href)`.
   Scroll first to load more of the grid, then run both collectors once per search query — this
   turns an N-pin research pass into ~2 tool calls per query instead of 2×N.

   **Goal-fit filter, not just visual-fit.** A pin can be a genuine visual/caption match and
   still be the wrong choice because the *metaphor* doesn't belong to the project's actual
   domain. Before keeping a candidate, ask: does this visual metaphor's meaning match what the
   project is really claiming, not just what it looks like? Example: a "verified badge/trust
   icon" search correctly returns polished results — but a generic blue circular checkmark is a
   reskinned social-media verified badge; it visually reads as "trust" but semantically claims
   "this account is authentic," not "we checked this person's credentials." For a tutoring
   platform that verifies real teaching qualifications, a document/seal/attestation-stamp
   metaphor is the actual claim being made — a checkmark badge is generic slop even at high
   production quality. Apply this same test to typography (does the alphabet/script used in the
   reference match the project's actual language and cultural register, or is it a Latin
   pictogram bolted onto a caption?) and to motion (does the reveal technique suit the subject's
   pace/formality, or is it a trend borrowed from an unrelated category?). Write the rejection
   reason down (one line) next to any strong-looking pin you drop for this reason — it's the
   part future reuse most needs, since the visual-fit pass alone won't catch it again.

2b. **Visual search — drill in via Pinterest's own similarity engine, not just the text bar.**
    Once evaluation (step 2) surfaces one candidate that's closest to the goal but not quite it,
    don't just retype the search query — open that pin and let Pinterest's visual matching find
    closer ones for you:
    - Navigate to the pin's own page (`https://www.pinterest.com/pin/<id>/`). Pinterest renders a
      "More like this" grid below the pin, ranked by visual similarity to *that specific image*
      (material, composition, color, shape) — this catches near-matches a caption-based query
      would never surface, because it isn't keyword-driven.
    - Pinterest also exposes crop-based visual search on the pin image itself: hovering shows a
      small draggable crop/magnifier control (desktop) that searches on just the cropped region
      (e.g. only the chair's leg detail, only the card's corner radius) rather than the whole
      image — use `computer` to hover the pin image and click the search-icon overlay if present,
      then drag the crop box onto the specific detail that matters before reading the resulting
      grid. If the overlay isn't present/clickable in a given layout, the "More like this" grid
      alone is still the visual-match signal — proceed with that.
    - Run the same judgment pass from step 2 against this new grid (goal-fit filter included), not
      a lighter one — "visually similar" still mixes in near-misses.
    - **Walk it like nearest-neighbor search**: pick the new closest match, open *that* pin, read
      its "More like this" grid, repeat. 2-3 hops usually converges tightly on the actual look;
      stop once a hop stops producing anything closer than what you already have, or once you hit
      a genuine keeper.
    - Use this mode whenever the ask is "find something like *this specific image*" (a pasted
      reference, a pin already found, a screenshot) rather than "find X style" — it's the
      image-similarity path, keyword search is the caption-similarity path; reach for whichever
      matches what you're actually starting from, or chain both (keyword search to find a seed →
      visual search to refine it).

3. **Download** the chosen refs:
   - Images: `scripts/download.py <out_dir> <url> [url2 ...]` (stdlib only, no deps). Pull the
     full-res URL (`i.pinimg.com/originals/...` or the highest-res `736x`/`564x` srcset entry,
     not the thumbnail). Pass every URL for a topic in one call — it dedupes by content hash.
   - Videos/motion pins: `scripts/download_video.py <out_dir> <pin_page_url> [url2 ...]` — shells
     out to yt-dlp (installed as a Python module: `python3 -m yt_dlp`), pass the pin *page* URL
     directly, it resolves the real media itself.
   - Save into the current project, e.g. `design-refs/pinterest/<topic>/`.
   - **If a URL/pin won't download** (403/blocked CDN, blob:/canvas-rendered, right-click-disabled
     overlay): bump the resolution segment in the URL (`236x`/`474x` → `736x` → `originals`)
     first; if that fails, re-fetch via `mcp__claude-in-chrome__read_network_requests` (open the
     pin, let it load, read the real response out of the network log — bypasses Referer/CDN
     checks since the browser already authenticated); last resort, screenshot the pin at max
     viewport width and crop.

4. **Show the user a quick contact sheet** (thumbnails) if more than a few — confirm which
   ones to actually use before wiring them in. Skip this if the user already picked exact pins.

5. **Isolate the subject when only the component matters, not the scene it was shot in**
   (a chair, an icon, a 3D object, a UI card photographed on a desk/background) —
   `scripts/remove_bg.py <in_file> [out_file]` (rembg, installed; first run downloads the
   ~176MB u2net model once, then it's cached) outputs a transparent-background PNG. Use this
   whenever the reference is "the object" not "the whole photo" — skip it for full-scene refs
   (hero backgrounds, textures, whole-page layouts) where the background *is* the point.

6. **Edit/customize further** as needed — crop, recolor, compress, convert to webp — with
   whatever's already installed (`sharp` via a one-off `npx`, ImageMagick `magick` if present,
   or Python `Pillow`, already present via rembg's deps). Don't install a new image lib for a
   one-off edit.

7. **Wire it in — and close the loop so we stop depending on Pinterest for this look next time**:
   - For a *look/motion pattern* to recreate in code: hand the refs to `taste-skill` /
     `motion-ui` / `threejs` / `frontend-design` as visual direction. Ask that skill to name the
     concrete technique it's replicating (e.g. "glass refraction via `backdrop-filter` +
     layered gradients", "scroll-scrub via `IntersectionObserver` + CSS custom properties") —
     not just "make it look like this."
   - For a cutout *asset* to actually use as-is: drop the edited file into the component's
     `public/`/`assets/` path **and add the import/reference in the actual component file** —
     a file sitting in `assets/` that nothing imports is not done.
   - **Learn it, don't just reuse it**: once a look/motion pattern has been rebuilt in code for
     a project, note the reusable technique (one line: what it is + which skill/component
     implements it) in that project's design doc (BRAND.md / frontend_master_spec-equivalent,
     or `design-refs/pinterest/<topic>/README.md` if no project doc exists). Next time the same
     *style* is wanted, check that note before going back to Pinterest — generating it directly
     with the technique already in hand beats re-sourcing a new reference every time, and is the
     actual goal: fewer Pinterest round-trips over time, not more.

8. **Completion gate — do not report this skill "done" on download alone.** Downloading a
   reference is step 3 of 8, not the finish line. Before ending the task:
   - Grep/read the actual component file(s) that were supposed to use the reference and confirm
     the technique or asset is really there (an import, a background-image path, a class name
     matching the pattern named in step 7) — don't just say it was "handed off."
   - If time/scope cut the task short before wiring-in happened, say so explicitly ("downloaded
     3 refs to `design-refs/pinterest/hero-glass/`, not yet wired into a component") instead of
     letting a successful download read as a successful build. A pile of downloaded files with
     nothing referencing them is an unfinished task, not a finished one.
   - **State the proof in the response, not just in your own head.** The user can't see the grep
     you ran — say the actual path (`design-refs/pinterest/<topic>/`) and the actual component
     file/line where the technique landed. "Referenced a Pinterest look" with no path named is
     the same as not having checked; a session that skipped this skill entirely can say that
     sentence just as easily as one that didn't.

## Rules
- **HARD RULE — product references must match the source, not just the vibe.** When the
  reference being replaced/sourced is an actual *product* (a cable, connector, device, part —
  anything going into a product listing, 3D model, or technical diagram, e.g. alwazour), the bar
  is accuracy, not aesthetics. Match the reference image as closely as possible: exact color,
  connector/port type and count, cable structure, material finish, proportions, and any other
  technical detail visible in the source — these are spec details a customer/engineer will
  actually check, not style cues to loosely riff on. Don't substitute a similar-looking product
  because it's a "close enough" visual match; if no candidate matches the real technical details,
  say so instead of picking the closest generic one. This overrides the usual "style reference,
  not literal" latitude given to non-product visual refs (hero art, textures, UI motion) below.
- Real photography/screenshots of other people's product UI are references for *style*, not
  code — never ship a competitor's screenshot as-is in a live product. Generic textures,
  patterns, illustrations, and backgrounds are fine to use directly once downloaded.
- Query Pinterest with the actual design vocabulary (glassmorphism, brutalist, claymorphism,
  bento grid, aurora gradient, liquid metal, etc.) — vague queries return junk.
- Keep downloaded refs out of git if the repo is public and licensing is unclear; note this to
  the user rather than silently deciding.
