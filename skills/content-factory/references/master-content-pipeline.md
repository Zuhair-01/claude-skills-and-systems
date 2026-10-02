# Master Content Pipeline (multi-brand, reusable)

Generalized from the Alwazour Technical Instagram build (the first brand
this was proven on end-to-end: strategy → visual pack → hand-built
Arabic-safe slides → posted carousel). Layers ON TOP of `SKILL.md`'s
stage map — use that for the actual reel/carousel/post mechanics; this
doc adds the steps that come BEFORE stage 0 and AFTER stage 8 when
onboarding a brand or running a full multi-week batch, and defines how
per-brand state persists so the next session doesn't re-derive it.

## When to use this vs. plain SKILL.md stages
- One-off "make me a carousel about X" → just run SKILL.md stages 0-8.
- "Get <brand> ready for posting" / onboarding a brand for the first
  time / refreshing an existing brand's whole calendar → run this full
  pipeline, which wraps SKILL.md stages 3-8 per piece.

## Stages

### A. Brand study
Visit the live site (Playwright/claude-in-chrome), read any existing
vault/memory docs for the brand first (don't re-derive what's already
written). Extract: palette + fonts (exact tokens, not vibes), tone,
offer, real audience, real differentiators, and — critically — what's
**verifiably true** (product count, service scope, team size) vs. what
would be fabrication if claimed. Write/update a **brand lock file**:
`<Project>/BRAND_LOCK.md` — tokens, contact info (verified against the
live profile/bio, never reused from an old template without
cross-checking — see the Alwazour Technical WhatsApp-number incident),
audience, and the non-negotiable facts.

### B. Science pass
Before asking ChatGPT anything, check what's already researched:
`marketing-psychology` and `social-growth-science` skills cover hook
formulas, the 4 U's, awareness-stage targeting, carousel pacing,
posting-cadence fundamentals. Only take an open question to ChatGPT if
it's not already answered there — don't re-research settled psychology
per brand.

### C. ChatGPT strategy consult (paste-workflow only)
Claude drafts one consolidated prompt: site link + brand facts from the
lock file + the specific open question (competitor angle, category-
specific credibility patterns, format mix). the user pastes into ChatGPT
web, pastes the reply back. **Never browser-extract ChatGPT** — 5x token
cost, confirmed standing rule. Output feeds SKILL.md stage 1 (STRATEGY):
pillars + ratios, caption formula, carousel templates, reel concepts,
calendar shape.

### D. Per-piece production
Run SKILL.md stages 2-7 per planned piece (hook → structure → design/
produce → captions → assemble → package). For any slide carrying Arabic
text: build as hand-coded HTML/SVG rendered via Playwright, NOT Gemini —
this is the proven zero-fabrication, pixel-exact method (Gemini garbles
Arabic). For photographic/background elements: source real photos
(Pinterest via `open-pinterest`, or the brand's own product shots) and
composite into the coded template — the "hybrid" method, not a fully
AI-generated scene, matches what's already posted and working.

### E. Brand-identity lock (persists forward)
Once a brand's token sheet + contact-info rule is set, every future
piece for that brand reuses `BRAND_LOCK.md` without re-deciding it. Any
correction (e.g. a wrong phone number caught after publishing) gets
fixed in the lock file immediately so it can't recur.

### F. QA gate (before SKILL.md stage 8's retention check)
- Zero fabricated stats/testimonials/scale claims — cross-check against
  the lock file's verified facts.
- No vendor/tool names in client-facing copy (mechanisms, not brands).
- Every carousel's last slide carries the brand's real, lock-file
  contact info (WhatsApp/site/location or brand-equivalent).
- Arabic mixed-phrase bidi check: any English brand/product term sitting
  next to Arabic text gets wrapped as ONE `dir=ltr; unicode-bidi:isolate`
  unit, not isolated word-by-word (isolating separately still garbles
  under RTL reordering).
- Rendered PNG opened and read, not just the HTML source trusted (print/
  export pagination and bidi bugs don't reliably preview in a scrolled
  DOM view).

### G. Per-brand sub-pipeline file
Each brand gets `<Project>/PIPELINE.md`: a short doc recording which
stages are done, links to `BRAND_LOCK.md`, the calendar file, and any
brand-specific deviation from this master doc (e.g. Kyros = carousels/
posts only, no reels; Ostazi = real-supply honesty constraint on every
credibility claim).

## Standing rules that apply to every brand, every piece
- ChatGPT: paste-workflow only, never browser-extract.
- Gemini/AI image-gen: the user drives (clicks/prompts), Claude navigates
  and guides — unless he says go fully autonomous.
- Verify live site state fresh before treating any local screenshot/doc
  as current ground truth.
- When a fact can't be verified, downgrade to the honest unconfirmed
  state — never pick an unverified number just to fill a slide.
