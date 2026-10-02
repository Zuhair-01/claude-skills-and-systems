---
name: content-factory
description: >-
  End-to-end producer for social content that Claude Code builds itself — reels
  (script + shotlist + captions + assembly), carousels (copy + designed slides
  rendered to PNG), and text posts. Orchestrates research → hook → structure →
  design/production → export, wiring the existing skill stack. Use when the ask
  is "make me a reel/carousel/post about X", "turn this into content", "batch a
  week of posts", "design these slides", "produce this video". Each stage can be
  run alone ("just write the hooks", "just design the slides from this script").
triggers:
  - make a reel
  - make a carousel
  - produce this video
  - design these slides
  - turn this into content
  - batch a week of content
  - content factory
  - script this reel
---

# content-factory

Textbook: `Second_Brain/30-Resources/Curriculum/Product_Business_5_Pillars_Mastery.md` §5E.
Ecosystem map (which skill per lane, produce sub-lane selection): `Second_Brain/30-Resources/Social_Content_Skill_Ecosystem.md`.
Onboarding a brand from scratch or refreshing its whole calendar (not a one-off piece): `references/master-content-pipeline.md` wraps the stage map below with brand-study/science-pass/ChatGPT-consult/QA steps and a per-brand lock file.
This skill = the assembly line. It calls other skills per stage; it does not replace them.

## Stage map (run all, or jump to one)

| Stage | What Claude does | Skills / tools used |
|---|---|---|
| 0 RESEARCH | Pull the niche's current hooks/angles; check what's trending; find 5 reference accounts + their patterns | `WebSearch`, `open-pinterest` (visual refs), `reel-intent-analyzer`, `seek-and-analyze-video` |
| 1 STRATEGY | Pick format (reel vs carousel vs post) for the message; define the ONE target person; awareness stage | `marketing-psychology`, `social-growth-science` |
| 2 HOOK | 10 hook variants, score by "would I stop scrolling", pick 1–2. Optional pre-filter: `laya_judge.tournament_rank()` (`laya-multilingual-judge` skill) pairwise-narrows the 10 down to a top 3-4 before the final human/Claude call — matches Laya's actual competence (small pairwise sets), never ask it to rank all 10 at once (its documented weak spot) | `marketing-psychology` (§4 U's, awareness), `copywriting` |
| 3 STRUCTURE | Reel: beat sheet (0–3 hook / 3–15 deliver / re-hook / loop-CTA). Carousel: slide-by-slide (slide1 hook → stakes → 1 idea/slide → recap → CTA). Post: inverted-pyramid draft | `social-growth-science` |
| 4a DESIGN (carousel/post) | Write ONE self-contained HTML file, one `<section class="slide">` per slide at 1080×1350 (4:5), consistent tokens; **source 1-3 real photos per carousel and build at least one real diagram per slide type** (see Photo+diagram rule below) — flat text-on-color is a fail state, not a starting point; render each to PNG with Playwright. **Or**, when the brief wants motion (see "VIDEO slides" recipe below): each slide is a short b-roll clip matched to that slide's specific line, text burned in via `render.py`'s caption engine | `web-imagegen` / `open-pinterest` for photography, `taste-skill` / `canvas-design` for the look, `playwright-skill` for PNG export; `style-clone` (`render.py` + `Broll_Library` + `visual-per-clause.md`) for video slides |
| 4b PRODUCE (reel) | Option A: AI video via `seedance-2`/`higgsfield-image-auto`/`avatar-video`/`sora`/`web-imagegen` (Qwen video mode, Create Video). Option B: talking-head/screen-record shotlist for the user to film. Option C: motion-graphics reel built as HTML/CSS/Canvas → screen-capture → mp4 | `ai-video-prompt-engineering`, `video-shortform`, `remotion-video-creation`, `motion-ui`, `ffmpeg` |
| 5 CAPTIONS | Burned-in captions (short-form needs them — 50%+ watch muted), on-screen text for first frame | `ffmpeg` (subtitles), `video-editing` |
| 6 ASSEMBLE | Stitch clips, add音 audio/music, trim to <30s where possible, 9:16 1080×1920, no watermark | `ffmpeg`, `auto_clipper.py` (the user's, `--gpu`) |
| 7 PACKAGE | Post caption (hook line + value + soft CTA + question), 3–5 niche hashtags, alt text, suggested post time; save to project `content/` folder | — |
| 8 REVIEW | Run the `social-growth-science` hard-rules check + retention-risk read of the first 3s before calling it done | `social-growth-science` |

## Carousel render recipe (the part Claude fully owns)

```
1. Build slides.html — <section class="slide"> × N, each 1080×1350px, position:relative.
   Shared: --bg, --ink, --accent, one display font + one body font. Slide number + @handle on every slide.
2. Slide 1: 60–90px headline, one promise, max contrast. Slides 3–N: one idea, ≤25 words, big.
   Second-to-last: recap (bullet list of the N ideas). Last: "Follow @X · Save this · [question]".
3. Render: playwright → for each .slide, element.screenshot({path: `slide-${i}.png`}).  (headless, deviceScaleFactor 2)
4. Output: content/<slug>/slide-1..N.png + caption.txt + the source slides.html.
```

## Carousel render recipe — VIDEO slides (b-roll behind text)

Added 2026-09-23, at the user's explicit request: "the format where its getting viral, a
b-roll or wtv in background and something relateable to the text thats over it." This is
IG's video-carousel format (a swipeable post where individual cards are short looping
clips, not flat PNGs) — a real, currently-missing capability, not a variant of the PNG
recipe above. Pick this over the PNG recipe when the brief specifically wants that
"scroll-stopping motion behind punchy text" feel (common in viral finance/motivation/
tips carousels) rather than a clean static infographic look.

**Engine: `style-clone`'s `render.py`/`graphics.py`, not a new build.** This is the same
text-over-real-footage compositing this skill already owns for reels — a video carousel
is just N short independent renders instead of one continuous cut:

```
1. Write the slide-by-slide script (Stage 3) as normal — one idea/beat per slide.
2. For EACH slide, classify what the text needs behind it using style-clone's
   `_TECHNIQUES/visual-per-clause.md` classifier (case 1-7) — this is the rule that
   actually makes it "relateable" instead of generic scrolling footage: the background
   has to demonstrate or relate to THIS slide's specific claim, never a stock "vibes" loop
   reused across slides. Source the clip from `Broll_Library/` (check `manifest.json`
   first) or pull a new one (`style-clone`'s `pull.py`) if nothing fits — never force-fit
   an unrelated clip because it's already on disk.
3. Render each slide as its own short vertical/4:5 clip via `render.py`: source = that
   slide's b-roll clip, one `cuts` entry spanning the clip's usable length, the slide's
   line as a single `captions` entry (burned in via the existing ASS engine — same
   caption styling this skill already uses for reels, don't invent a new text treatment).
   `crop_x` (added 2026-09-23 to `render.py`) lets you recenter the crop per-slide if the
   b-roll's default center-crop cuts through the subject — check every slide's frame
   before calling it done, don't assume centered is fine.
4. Keep each slide SHORT and loop-friendly (2-4s) — this is a carousel card someone taps
   through, not a reel; a slide that's still setting up when they swipe to the next one
   has failed the same way a boring reel intro does.
5. Output: content/<slug>/slide-1..N.mp4 + caption.txt. Same slide-count/pacing rules as
   the PNG recipe (slide 1 hook, recap second-to-last, CTA last) — only the rendering
   engine changes, not the copy/structure stages above it.
```

**Hard rule specific to this format:** a b-roll clip that's just "on-brand vibes" and
doesn't actually relate to that slide's specific line is worse than a static PNG slide —
it reads as filler motion, not production value. Reuse `visual-per-clause.md`'s
discipline exactly as written; don't relax it because this is a carousel and not a reel.

## Reel motion-graphics recipe (no camera, no AI credits)

```
1. Build reel.html at 1080×1920, an animated sequence: keyframed CSS/Canvas, text pops synced to a beat.
2. Timeline via Web Animations API or a simple requestAnimationFrame clock; total ≤ 25s.
3. Capture: playwright page.video / or screen-record the tab / or render frames + ffmpeg -framerate 30.
4. ffmpeg: add audio track, -vf for safe margins, export H.264 mp4 9:16, faststart, no watermark.
```

## Real camera footage, or a named creator's style
This skill produces content from scratch. When the job is **cutting the user's own raw
footage**, or matching a specific creator's editing, or sourcing b-roll that fits the
script's actual words, hand to `style-clone` (CLAUDE.md Rule 14) — it holds the corpus
analysis, the vault Style Library, the b-roll library and the transcribe → EDL → render
pipeline. Come back here for the copy, hooks and caption layer around it.

## Batch mode ("a week of content")
Stage 0–1 once for the week's theme → generate 12–15 hooks → assign 5 to reels, 3 to carousels, 5 to posts → run stages 3–7 per item → dump all into `content/week-NN/` with a `calendar.md` (item, format, hook, caption, suggested day/time).

## Output contract
Always produce actual files in a `content/<slug>/` folder (PNGs, mp4, caption.txt, source html), not just text. End with a one-screen summary table: item · format · hook · file path · predicted weak point.

## Hard rules
- Hook first, every stage serves the first 3 seconds. A great slide 4 can't save a dead slide 1.
- Captions burned in for all short-form. Text on the first frame stating the payoff.
- 9:16 1080×1920 video / 4:5 1080×1350 carousel. No platform watermark. Has audio.
- Never fabricate stats/testimonials in the copy (kills trust + reach).
- Consistency of slide design > cleverness — swiping must feel effortless.
- If positioning/message is unclear, stop at stage 1 and fix it — don't produce 10 polished posts of a muddy message.
- **Photo + diagram, not flat text-on-color** (learned 2026-09-01, Ostazi/Kyros/Alwazour
  Studio rebuild after the user flagged v1 as "just words slapped on a slide, no diagrams
  no visuals"). Every carousel slide needs at minimum one of: a real sourced photo
  (`open-pinterest`, watermark-checked, as a photo-band top or full-bleed background
  with a gradient fade into the slide's bg color — never a raw unedited screenshot) or
  a real hand-built diagram (checkmark/status icons as SVG not bare unicode, a progress/
  meter bar, a labeled timeline, a browser-chrome frame, an input→process→output
  pipeline, a numbered step-chain with connector lines, a comparison-row table). Text-
  only slides are the default failure mode this rule exists to stop — treat a slide
  with only a headline + body paragraph as unfinished, not "minimal." Reuse the
  `<photo-band + text-below>` shape proven across all three rebuilt brands rather than
  inventing a new layout each time.
- **Never reuse a photo** — not across slides in one carousel, not across carousels in
  a series, not even the same photo cropped differently (learned 2026-09-07, Ostazi
  C4/C5: a prior pass avoided reuse by dropping photos entirely, which is the wrong
  fix — that read as flat/generic). Source a NEW topic-accurate photo every time via
  `web-imagegen` or `open-pinterest`; only reuse if nothing better/relatable exists for
  that topic. Full rule: memory `feedback_no_photo_reuse_rule.md`.
- **`web-imagegen` vs `open-pinterest` — pick by whether the exact scene exists in
  reality** (added 2026-09-12, first real use: Ostazi tutoring-at-home carousel).
  `web-imagegen <qwen|gemini> "<prompt>" --count N --out <dir>` drives Qwen/Gemini's
  real web chat (via CDP into the user's own logged-in Brave — connects automatically
  if Brave was launched with `--remote-debugging-port=9222`) to generate a genuinely
  new photoreal image or video, not sourced from anywhere. Use it when the brief needs
  a *specific, brand-accurate scene* Pinterest can't supply as a real photo (a Syrian
  student studying with a specific tutoring-app laptop screen, a specific product in a
  specific setting) — write the prompt for photorealism explicitly: editorial/
  documentary photography language, natural imperfections (skin texture, uneven
  lighting, worn surfaces), a real lens/depth-of-field cue, explicitly no text/logo
  overlay. **Crop the platform watermark** (bottom-right on Qwen output) before using
  the image anywhere. Fall back to `open-pinterest` when an existing real photo already
  matches the brief, or the need is a style/diagram/motion *reference* rather than a
  usable final asset.
- **One visual template per carousel SERIES, no exceptions** — every carousel meant to
  post together/back-to-back (e.g. a brand's C1-C5 batch) must share the exact same
  slide shell (same photo-band vs full-bleed pattern, same badge/pill/gradient system)
  end to end. Building one carousel in a batch on a different template than its
  siblings is a real bug, not a style choice (caught 2026-09-07: Ostazi C3 used a
  photo-driven template while C4/C5 shipped as flat navy/cream text-only — looked like
  two different designers). Before rendering, diff the new carousel's slide-shell CSS
  classes against the last-approved carousel in the same series.
- **Every carousel needs a genuine idea, not a numbered-list template filled with
  generic content** — a flat "3 steps: X → Y → Z" explainer with no real insight or
  tension is a fail state even with good visuals (killed 2026-09-07: Ostazi's "how
  matching works" concept, the user: "the ostazi posts are weak... from the idea n
  scripting"). Before scripting, the concept must survive: "does this teach something
  the reader didn't already assume, or create a real curiosity gap?" If not, go back to
  stage 0/1 for a sharper angle before writing slide copy — a strong angle is the actual
  gate, not the numbered-slide format doing the work by itself.
- **Swipe-completion psychology** (see `marketing-psychology` step 5 and
  `Second_Brain/30-Resources/Curriculum/Marketing_Psychology_Deep_Research_2026_09_06.md`):
  slide-1 must front-load the payoff inside the first glance (2026 attention is ~1s,
  not the old "3-second rule") — don't bury the promise under a setup sentence. The
  numbered/open-loop format (mistake N/3, step N/3) is neurologically correct — it's a
  real dopamine information-gap trigger, not just a content trick — but the HARD rule
  attached to it: every open loop opened on slide 1 must close with a real, specific
  payoff by the last slide. A curiosity gap with a weak/generic answer destroys trust
  faster than never opening the loop at all — check this before calling any carousel
  script final.

## Voice-aware scripts (any reel/video that a synthetic voice will speak) — added 2026-09-25
Before writing or approving a spoken script, read `Empire_Base/Second_Brain/Workflow/30 - Resources/Voice_Engine_and_Script_Guide.md` section 4 and section 1. In short: write the SPOKEN script separately from captions; one idea per ~6-14-word sentence; punctuation and per-sentence pauses are the direction; emotion arc not constant energy; no `[sigh]` tag (renders as noise/buzz in local TTS) and any other tag only after an isolated test; spell out numbers; transcreate per language and dialect instead of translating; output a direction sheet (`text | speed | pause_after | emotion note`) so the render can direct each sentence. The right voice engine depends on the project (section 1 table); the user's ear approves, never claim a voice verified.
