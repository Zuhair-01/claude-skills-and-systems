---
name: apex-frontend-lab
description: One-shot peak-tier frontend protocol — taste laws, mechanical pre-flight checklist, 6-dim scorecard, vetted palettes/type pairings, and zero-dep code patterns (raw WebGL 3D, scroll-driven timelines, kinetic type, domain-warp shaders). Cross-tool project built by opencode; use before any non-trivial frontend build and before claiming one "done".
user-invocable: false
---

# Apex Frontend Lab

Lives at `~\Desktop\Empire_Base\apex-frontend-lab\` — a cross-tool
capability system (opencode + Claude Code) distinct from `mega-frontend-lab`
(that's the React component corpus; this is taste/protocol/benchmarks).

## When to load

Any frontend build past a trivial one-liner. The repo's own router (idea →
shipped build), now: `TEMPLATES.md` (pick archetype) → `PLAYBOOK.md` (Design
Read + dials + laws, top to bottom) → `PALETTES.md`/`TYPE-PAIRINGS.md`
(rotate style) → `TECHNIQUES/` (pick the motion/3D/component techniques the
idea needs) → `PATTERNS/` (copy the canonical skeleton) → build mobile-first
→ `CHECKLIST.md` mechanically → `SCORECARD.md` → screenshot-critique loop
(see LAB-005 note below) → `RETRO.md`. Slots into `BUNDLE-B-frontend`'s
Quick Start alongside (not instead of) `open-pinterest` for a real-world
visual reference.

## What's in it

- `PLAYBOOK.md` — Design Read ritual (3 dials: variance/motion/density) + 83
  numbered laws (76 + 77-80 are Claude's own web-verification/gap-fill
  addenda; 81-82 are opencode's — note they originally numbered these 76-77
  too and self-caught + renumbered the collision same-day, a real example
  of the append-only convention holding up under concurrent cross-tool
  edits): AI-tell killers, layout rhythm, copy, visual assets, motion,
  perf/a11y gates, tokens-only color, payload≠richness, data-honesty (chart
  bars must match axis labels, no suffix wrap), pick-archetype-first,
  "visual verification is part of done" (bridge-open + actually look, or say
  the tool is down — landed after a real user-caught bug in LAB-004), plus a
  2026-research wave: WCAG 2.2 floor (scroll-padding-top for Focus-Not-
  Obscured, 24×24px targets, drag-alt-inputs, no puzzle CAPTCHA), OKLCH
  3-tier color tokens (reference→semantic→component, dark mode = semantic
  remap only), scroll-driven-animations/View-Transitions as the 2026 motion
  baseline (CSS before JS libs), hard 3D pipeline numbers (gltfpack default,
  KTX2, <100 draw calls mobile, DPR≤2, <5MB/<50k tris), and the 5-trait
  waitlist/launch law. Plus two later waves: UX-depth laws 65-67 (loading-
  state decision tree by latency, search-UX gates, cognitive-accessibility
  defaults) and docs/harness-era laws 68-71 — **law 71 is now the hard
  gate: every lab build MUST run `npm run verify -- <page> --freeze` before
  being called done; PASS = stability ≤0.05% pixel diff AND zero critical/
  serious axe violations, otherwise it's fixed, not shipped.** Plus laws
  72-75 from the RTL/Arabic era (LAB-012, closing the gap flagged earlier
  as most relevant to the user's projects): logical properties only in any
  layout that may ever be mirrored (physical left/right = latent bug),
  Arabic letter-spacing banned + body line-height ≥1.7 + `<bdi>` every
  Latin/number token + one digit system per page, compound selectors must
  match real DOM order (contrast gates expose dead-selector bugs, not just
  styling issues), and every h3 subtree needs an accessible h2 (sr-only OK).
  **Law 76 (Claude, 2026-08-25): live WebSearch fact-check on drift-prone
  browser-support claims** — scroll-driven animations are unflagged in
  Chrome/Edge/Safari 26+ but Firefox is STILL behind a flag as of Firefox
  152 (June 2026), so the repo's mandated `@supports`+fallback guard covers
  a real current gap, not legacy paranoia; View Transitions cross-document
  (MPA) has Chrome/Edge/Safari 18.2+ parity but Firefox native support is
  still in development. WCAG 2.2/Core-Web-Vitals numbers elsewhere in the
  playbook were spot-checked and confirmed current. Full sourced detail:
  RESEARCH/2026-frontend-research.md WAVE 7. **Laws 77-80 (Claude,
  2026-08-25, larger batch pass per the user's request — WAVE 8, ~12 searches
  across 8 clusters):** container queries + `:has()` are now Baseline-safe,
  use them (no feature-detect needed, unlike scroll-timelines); e-commerce
  PDPs need complete JSON-LD Product schema as a first-class requirement —
  AI shopping agents (Operator/Gemini/Perplexity/Rufus) parse structured
  markup not prose, directly relevant to alwazour; form inline-validation
  should debounce ~500ms after typing stops; and a self-check on law 8 —
  the Phosphor-first icon ranking is a house preference, not a verified
  external consensus (found source-bias in a vendor's own self-ranking).
  Also net-new, not corrections: sharper PDP conversion numbers (5+ reviews
  = 270% lift, 380% on $100+ items; AI chat ≈4x conversion), dashboard
  trend update (command palette now standard past ~10 features; density
  philosophy shifted to prioritize-first not more-widgets), and confirmed-
  unchanged spot-checks on OKLCH support, motion-token industry validation,
  waitlist/portfolio CRO framing. Full detail: WAVE 8 in RESEARCH.md.
  **Laws 81-82 (opencode, same day, after the user live-critiqued LAB-012 as
  "not responsive / colors not accurately combined"):** verify-gate now
  covers all 3 viewports (390/820/1440) and mobile nav must be genuinely
  operable (button+JS+aria-expanded), not just hidden links; color
  decisions must cite the new `COLOR-SCIENCE.md`. **Law 83 (opencode, same
  day, LAB-002): live-WebGL pages declare a canvas diff tolerance
  (`--max-diff 1`) instead of the standard 0.05% text-page gate** (desktop
  AA jitter is inherent ~0.77%, not a real regression); auto-rotate must
  respect reduced-motion since JS-driven motion is invisible to CSS
  freezes. opencode also sent an explicit ack acknowledging Claude's WAVE
  7/8 passes and confirming the law-numbering reconciliation — genuine
  two-way cross-tool coordination, not just one-way monitoring.
- `RESEARCH/2026-frontend-research.md` — the source research behind the laws
  above: 19 dense categories (typography, docs IA, dashboards, portfolio
  case-study structure, waitlist conversion traits, WCAG 2.2 specifics,
  SaaS/PDP conversion, motion/perf, AI-era "agentic readability" patterns,
  OKLCH token architecture, scroll-driven-animation platform status, event-
  page conversion, microcopy, a full WebGL/Three.js + CSS-3D production
  pipeline with concrete budgets, plus two newer ones: form-validation
  patterns — validate on blur not keystroke, errors live next to the field
  with specific actionable copy, never clear a form on a server 500 — and a
  light-theme glassmorphism recipe (white .72 + blur + soft shadow does the
  depth work dark glass gets from glow; badges need solid-ish .85 bg to
  stay readable), loading-state/search-UX/cognitive-accessibility waves,
  and — **directly applicable to the user's Arabic-market projects (alwazour,
  Ostazi) — a full RTL/Arabic web craft section (#23)**: logical CSS
  properties (`margin-inline-start` not `margin-left`, full browser support
  since 2023) are the whole mirroring mechanism; never letter-space Arabic
  text (breaks glyph joining) or uppercase-transform it; body line-height
  1.7-1.9; 2026 font tiers (IBM Plex Sans Arabic, Cairo, Tajawal, Noto Kufi
  Arabic headlines-only, avoid legacy Tahoma/Segoe); wrap Latin/numbers in
  `<bdi>` at bidi boundaries to avoid the "comma jump" bug; logos/wordmarks
  usually stay LTR even in RTL layouts; Arabic UI chrome grows ~20-25%
  taller than English, budget for it. **Now promoted into PLAYBOOK laws
  72-75 and built as LAB-012 (GAPS #9 CLOSED)** — see below. Worth reading
  directly for any deep-dive beyond what's distilled into PLAYBOOK/TEMPLATES.
- `RICHNESS.md` — the anti-dull gate, run BEFORE CHECKLIST. Born from a real
  failure (LAB-008 v1 shipped "dull and empty" — typography-only, no
  imagery/motion — despite passing the old checklist). Universal laws (≥3
  visual anchors per 100vh, unified imagery treatment, texture layer,
  scroll choreography, hover choreography everywhere, the "screenshot test"
  — if any region reads as template placeholder, not done) plus a per-
  archetype table naming the must-have richness elements and a best-in-
  class reference site for each of the 10 archetypes.
- `GAPS.md` — honest self-audit of what the lab still lacks, P0-P3 priority
  order. **P0, #4 (GLB viewer), #9/#15 (RTL/Arabic) all CLOSED** — see
  `scripts/verify.mjs`, LAB-002, LAB-012 below. Still open: PDP + event
  archetype exemplars, Lighthouse wiring, dark-mode pass on most labs,
  touch-target sweep, visual-regression diffing beyond pixelmatch stability.
- `scripts/verify.mjs` — the real verification harness (Playwright +
  axe-core + pixelmatch, devDependencies only, build pages stay zero-dep).
  `npm run verify -- "LAB/<id>/index.html" [--freeze] [--stability N]`:
  deterministic capture (fonts.ready → rAF settle → lazy-load settle-scroll
  → height-stable poll → discard one warm-up shot → real captures),
  stability-checked via pixelmatch (PASS ≤0.05% diff across N shots), axe-
  core run same pass (wcag2a/2aa/21a/21aa/best-practice) with report.json +
  exit-fail on critical/serious violations. Fixed a real problem: Brave/Edge
  headless screenshots were flapping constantly before this; LAB-009/010
  now hold at 0.000% diff. **Already found real violations to fix**:
  LAB-009 has 37× color-contrast + heading-order + landmark-one-main +
  region(31) issues; LAB-010 has 13× color-contrast + 1×
  scrollable-region-focusable. Use this harness for any future Claude-side
  build too — it's a genuine, working a11y/stability check, not
  aspirational. **Update: both since fixed** — re-run reports show LAB-009
  and LAB-010 now at 0 violations, stability pass true.
- `TOOLS.md` — the dependency arsenal: 40+ verified libraries/tools/sources
  across 12 categories (animation, 3D, components, effects, scroll,
  typography, icons, data-viz, forms, inspiration sources, dev/QA tools),
  each with what/contains/when/how-to-start/verdict, plus 2026 landscape
  notes (GSAP is now 100% MIT-free with every plugin included, Framer
  Motion rebranded to "Motion", Lenis is the smooth-scroll standard,
  shadcn/ui is the 2026 React default) and quick decision shortcuts by use
  case. **Read AFTER TEMPLATES, BEFORE picking any dependency** — this repo
  stays zero-dep by default but this is the reference for when a real stack
  needs a real library. Also names the fix for GAPS #11-13: Playwright for
  the screenshot-pipeline instability, axe-core + Lighthouse CI for
  automated a11y/perf audits. **Claude added sections M/N/O (2026-08-25):**
  M = ready-made component/block marketplaces (shadcn.io/Shadcnblocks 6,000+
  blocks, Magic UI, Aceternity, ReactBits, Flowbite) for moving faster than
  hand-rolling PATTERNS/ when a build needs a section fast; N = motion-asset
  marketplaces (LottieFiles for timeline brand animation, Rive for
  state-machine interactive micro-interactions — "Rive when it has
  behaviour, Lottie when it has a timeline"); O = free/license-clear 3D
  model sources (**Poly Haven CC0 — directly unblocks GAPS #4, the LAB-002
  GLB viewer that's been queued since the start**; Sketchfab with per-model
  license care; Kenney/Quaternius CC0 for stylized packs).
- `COLOR-SCIENCE.md` — how to combine colors correctly, not by vibes: OKLCH
  ramp recipe (vary L with C/H fixed — hex ramps built by adding % white
  band and go muddy), computed contrast (not eyeballed; dark-mode text caps
  at L .90-.93 on L .15-.20 surfaces to avoid halation), hue-pairing rules
  (semantic colors need ≥.15 L separation too, not just hue, for color-
  blind legibility), dark mode = re-tint not invert, and a **business-type
  → palette table with the WHY per industry** (fintech navy/gold, health
  blue-teal, e-commerce warm+one-hot-accent, SaaS cobalt/slate, luxury
  near-black/cream, **MENA/Arabic-first: deep cobalt or emerald + warm sand
  + gold, sand=regional material language, warm low-glare canvases improve
  Arabic-script legibility** — directly relevant to alwazour/Ostazi).
- `FEATURES.md` — the missing checklist: a **20-category capability
  matrix** (responsive layout, mobile nav, touch targets, scroll animation,
  forms, a11y, color system, dark mode, RTL/i18n, 3D, data-viz, keyboard
  completeness, etc.) scored ✅/⚠️/❌ per LAB build, catching gaps that
  RICHNESS.md/CHECKLIST.md didn't systematically track (e.g. it surfaced
  that LAB-009/010 have no dark-mode variant, LAB-009/010/011 have no RTL
  coverage). Gate: categories 1/2/9/18/20 (responsive, mobile nav, WCAG
  2.2 AA, keyboard, landmarks) must be ✅ before any build claims done.
- `CHECKLIST.md` — mechanical pre-flight gate, count-based, any FAIL = not done.
- `SCORECARD.md` — 6-dimension grading; anything under 8/10 gets fixed not excused.
- `PALETTES.md` / `TYPE-PAIRINGS.md` — vetted non-slop references, rotate per build.
- `PATTERNS/` — 13 canonical zero-dep single-file skeletons (scroll reveals,
  sticky stack, canvas field, WebGL shader hero, CSS 3D tilt, raw-WebGL 3D
  object, horizontal pan, ghost-guide SVG path-draw, per-dot CSS keyframe
  grid drift, blurred-gradient glow edge, rotating circular orbit badge,
  floating element cluster (light+dark), form-input states) — reuse instead
  of reinventing.
- `STUDY.md` — technique deep-dives (what/why/gotcha): CSS scroll timelines,
  raw-WebGL point clouds as "3D without Three.js", drag/inertia feel, kinetic
  type mechanics, domain-warped shader noise, zero-image layout depth tricks.
- `STUDY-CASES/` — real-site teardowns (layout/color/motion/copy/steal-list/
  take-down): `gojiberry-ai.md` (Framer AI-SaaS, ghost-path-draw + "Warm
  Tech" palette P7) and `batch-001-ranked.md` (linear.app / stripe.com /
  vercel.com / lusion.co — dot-grid ambient depth, tokens-only color
  discipline, two-speed motion, "payload ≠ richness" for WebGL-creative
  pages, real-DOM product dioramas as the sanctioned screenshot alternative,
  var-driven decorative charts/logo walls) and `batch-002-ranked.md`
  (dennissnellenberg.com / apple.com/ipad / awwwards.com — video-first
  38KB portfolio shell, chapter-nav scrollytelling, product-color-as-
  section-identity, per-breakpoint aspect-ratio vars for zero-CLS images).
  Raw dumps in `STUDY-CASES/_raw/`.
- `scripts/study-site.mjs` — opencode's site-teardown CLI that produces a
  STUDY-CASES entry from a live URL (DOM/CSS/motion analysis) — the pipeline
  behind both case-study batches above.
- `TECHNIQUES/` — **complete, 6/6 docs**: the "any idea → perfected build"
  router (INDEX.md) + one guide per domain (2d-animation, 3d-webgl, motion-
  design, components, visual-craft), each with ready-to-paste code snippets,
  WHEN to reach for it, perf cost, a11y gates, and real pitfalls found in
  the labs. Load between PALETTES and PATTERNS. Perf tier preference stated
  explicitly: CSS < SVG < Canvas2D < WebGL < Three.js — pick the cheapest
  tier that achieves the effect. E.g. motion-design.md ships copy-paste
  motion tokens (160ms UI / 800ms narrative / 120ms press), the scroll-
  timeline range law (`cover 0%→100%`, never `contain`, on tall runways),
  and a full reduced-motion contract per pattern.
- `VISUAL-SYSTEMS.md` — capability map across 2D/3D/floating/scroll/motion.
- `TEMPLATES.md` (v2) — **load this FIRST for any "build me a site" brief**:
  10 archetypes (SaaS landing, creative studio, portfolio, e-commerce PDP,
  editorial, dashboard, docs, pricing, waitlist, event one-pager), each now
  a full conversion spec — USE-WHEN / GOAL METRIC / SECTION STACK (ordered
  by buyer questions, not template defaults) / MOTION / PERF / PATTERNS /
  CONVERSION LAWS / KILL-LIST / REFERENCE — sourced from a cited 2026 CRO
  research pass (buyer-question ordering, outcome-first heroes ≤25 words,
  proof-at-decision-points, PDP trust economics, "agentic readability" —
  AI agents now comparison-shop, so structured data/clean specs matter for
  revenue). Cross-archetype laws + a 4-question decision shortcut at top.
  Pick the archetype here before touching PLAYBOOK/PALETTES/PATTERNS.
- `LAB/` — benchmark builds, each with BRIEF + RETRO, three style pillars
  proven so far: **001** apex-showcase (43.5KB creative/dark, zero-dep) ·
  **004** linear-style (22.8KB minimal-dark-SaaS, built with zero new
  techniques — proof the playbook alone is sufficient; verified via the
  reusable `audit.html` headless geometry-QA harness, which caught and
  fixed a metric-suffix-wrap bug, law 57/59) · **005** waitlist-light
  (light "Warm Tech" OKLCH-token style; verified via a real screenshot→
  self-critique→fix→re-shoot loop across 3 iterations, all-clean — caught a
  trust-counter that froze mid-animation, fixed by removing the count-up
  entirely, giving the rule **trust/proof numbers should never animate**) ·
  **006** dashboard (app-UI pillar, dashboard-specific research applied
  1:1, headless-verified) · **007** gallery (technique test bench, 8
  techniques implemented+verified, invented a `flat=1` capture mode for
  one-shot full-page headless screenshots) · **008** editorial (5th style
  pillar — v1 failed the then-new `RICHNESS.md` gate, "dull and empty",
  fixed in v2) · **009** floating-SaaS (rebuilt after user critique from a
  bare hero into the complete archetype stack — logo wall, bento demos,
  metrics, testimonial, pricing, FAQ, CTA — 26.4KB; lesson logged: **the
  archetype's section stack in TEMPLATES.md is a completeness contract, not
  a suggestion — a partial stack isn't done even if what exists is
  polished**) · **011** docs (3-pane, autocomplete search, GAPS #1 closed)
  · **012** arabic-rtl (~19KB, full SaaS stack in Arabic, `dir=rtl
  lang=ar`, Cairo 900 display + IBM Plex Sans Arabic body, 100% logical
  properties — GAPS #9/#15 closed, laws 72-75). All labs from 009 onward
  are verified via the real `scripts/verify.mjs` harness (0% pixel diff,
  0 axe violations), not just self-critique. Five+ style pillars now
  proven: marketing-dark, waitlist-light, app-UI dashboard, gallery/
  technique-bench, editorial, docs, Arabic-RTL. This build→critique→fix
  loop is the demonstrated bar for "verified done."

Note: opencode also installed its own OpenCode-side skill (`frontend-apex`)
that auto-triggers this playbook's protocol on any OpenCode frontend task —
separate from this Claude-side wrapper, same underlying repo.

## House rules (inherited from that repo's README)

- Append-only docs — new durable rules get dated and added to `PLAYBOOK.md`,
  never rewritten in place.
- Evidence before "done": open the page, screenshot it, run the checklist for real.
- Every finished build appends a `LAB/<id>/RETRO.md`; promote new durable
  rules back into `PLAYBOOK.md`.
