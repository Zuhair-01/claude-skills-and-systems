---
name: bundle-b-frontend-ui
description: Frontend and UI design bundle for React, Next.js, CSS, components, design systems, animation, and visual taste — deduped router to canonical skills, covering every UI surface (not just marketing pages) via taste-skill's Category Router.
user-invocable: false
---

# BUNDLE B: Frontend & UI Design

**Orchestrates:** React/Next.js code patterns, visual/aesthetic direction, component generation,
animation, design-system tokens, accessibility, 3D — across marketing pages, dashboards, mobile,
data-heavy UI, and every other surface `taste-skill`'s Category Router (its Section 13) covers.
**Deduped 2026-08-17, widened 2026-08-23:** this bundle previously listed 6 skill names and waved
at "15+ more" unnamed ones, including `framer-motion` which was never actually live. It was rebuilt
as an accurate router to a small set of canonical, deduped skills, then widened so its Quick Start
routes by *what the user handed you* first (screenshot vs. text-only vs. image-gen brief), not just
by surface type — see `taste-skill`'s Appendix H, which this bundle now defers to instead of
duplicating.

## Quick Start — Step 0: What did the user hand you?
Before picking a build skill below, classify the input (full logic + why in `taste-skill`'s
Appendix H — this is the condensed version):
- **A real screenshot/Figma export/hand sketch to match exactly** → `visual-to-code` (extraction,
  not reinterpretation — the image is the spec).
- **Text-only brief, image-gen tooling available, brief wants a fully custom look** →
  `image-to-code-skill` (generates its own reference mockup, then builds to match it) — route
  through `open-pinterest` first (below) if a specific real-world look is wanted.
- **Text-only brief, no image-gen tooling, or a look this skill's own dial system can produce** →
  `taste-skill` directly.
- **Google Stitch workflow specifically** → `stitch-skill`.
- **Generic/throwaway prototype where speed beats originality** → `web-prototype`.
- **Multi-variant exploration ("show me a few options")** → `magic-ui-generator` + `shadcn`.

## Quick Start — Step 1: What kind of surface is it?
- **Any task needing a real-world visual/motion look (not just generic styling) →
  `frontend-reference-sources` FIRST**, before generating from scratch: it routes to the best-fit
  source (`open-pinterest` broad net · `refero.design` real product-UI screens · `supahero.io`
  hero sections · `60fps.design` motion/interaction clips · `21st.dev`→`magic-ui-generator` for
  component blocks · `motion.dev`→`motion-ui` for coding the animation), sources + evaluates the
  reference against the brief, downloads, cuts out subject if needed, *then* hands it to the skill
  below as visual direction. Skip only when the task is pure logic/layout with no specific look
  requested.
- **Any non-trivial build → `apex-frontend-lab`** (cross-tool, opencode-maintained, actively
  growing) for the Design Read ritual + 48 taste laws + mechanical pre-flight checklist +
  zero-dep 3D/motion/shader patterns — read its `PLAYBOOK.md` before code, run its `CHECKLIST.md`
  before calling it done.
- **Any surface at all (marketing, dashboard, mobile, data table, forms, 3D, realtime, ecommerce,
  and 30+ more) → `taste-skill`**, whose Section 13 Category Router classifies the surface and
  either builds it directly (marketing/portfolio/redesign) or names the exact specialist skill +
  monitor step for everything else. This bundle no longer hand-lists per-surface routing —
  `taste-skill`'s router is the single source of truth for that, kept current via its own
  100-search 2026 research pass (its Appendix F/G).
- Multi-variant AI component generation (21st.dev) → `magic-ui-generator` + `shadcn`
- React/Next.js code patterns → `frontend-patterns` (code) / `react-best-practices` (perf rules)
- Next.js App Router → `nextjs-best-practices` (principles) + `nextjs-app-router-patterns` (playbook)
- Animation → `motion-ui` (component/state motion) ; **scroll-scrubbed / pinned / timeline / SplitText / SVG-morph → GSAP** via `motion-ui`'s GSAP section → off-context `gsap-*` skills (100% free incl. all plugins since Apr 2025)
- 3D → `threejs` (raw/procedural, 3D-is-the-product) ; **decorative/hero interactive scene → Spline** via `threejs`'s Spline section → off-context `spline-3d-integration`
- Charts / data-viz in a shadcn app → **bklit UI** (`bklit.com`) via `shadcn` — registry add + `ui.bklit.com/studio` playground; don't hand-roll Recharts
- Tailwind styling → `tailwind-patterns`
- UX/heuristic audit (not generative) → `uxui-principles`
- Existing site upgrade → `redesign-skill` / `design-review` (or `taste-skill`'s own Section 11
  redesign protocol when the taste/aesthetic layer is the actual work)

## Primary Skills
- `taste-skill` — canonical anti-slop/premium visual-taste generator AND category router (dials,
  presets, AI-tell bans, GSAP skeletons, pre-flight checklist, plus a Section 13 router covering
  every UI surface type and an Appendix H input-type trigger map). Absorbs `gpt-tasteskill` and
  `high-end-visual-design` (now redirect stubs).
- `visual-to-code` — exact reproduction of a supplied reference image (screenshot, Figma export,
  sketch, or a look sourced via `open-pinterest`) as pixel-accurate code. Use when the image is
  ground truth to extract from, not a starting point to riff on — see Quick Start Step 0.
- `image-to-code-skill` — generates its own reference mockup image first, then implements to match
  it. Use for text-only briefs where image-gen tooling should drive the visual direction before code
  is written — distinct from `visual-to-code`, which requires a pre-existing ground-truth image.
- `uxui-principles` — canonical UX/UI heuristic evaluator (168 principles, antipattern detection).
  Absorbs `frontend-design` and `ui-ux-pro-max` (now redirect stubs).
- `frontend-patterns` — canonical React/Next.js code-pattern guide (composition, hooks, forms,
  error boundaries, a11y, quick-reference tables). Absorbs `react-patterns` (now a redirect stub).
- `nextjs-best-practices` — Next.js App Router principles/decision-trees (complementary to, not a
  duplicate of, `nextjs-app-router-patterns`'s code playbook).
- `tailwind-patterns` — Tailwind CSS v4 config/patterns, design tokens.
- `design-system` — design-system generation/audit, visual consistency.

## Secondary Skills
- `motion-ui` — canonical animation skill (tokens, perf/a11y/SSR, core patterns). Points to
  off-context `framer-motion`, `motion-advanced`, `motion-patterns`, `animejs-animation`,
  `threejs-animation` for deep techniques not worth inlining (gestures, SVG draw-on, toasts, page
  transitions, non-React animation).
- `magic-ui-generator` — 21st.dev/Magic: multi-variant AI component generation (Shadcn/Magic
  UI/Aceternity-sourced). Newly installed live; previously off-context and unreferenced.
- `shadcn` — shadcn/ui component management/docs; the base layer most generated components sit on.
  Newly installed live.
- `nextjs-app-router-patterns` — code playbook (parallel/intercepting routes, streaming, route
  handlers, metadata).
- `ui-design` — muapi.ai API wrapper for wireframe/mockup image generation (distinct tool, not a
  taste-skill duplicate).
- `stitch-skill` — semantic DESIGN.md generator for Google Stitch; translates this bundle's own
  anti-slop directives into Stitch's format, not a competing taste system.
- `web-prototype` — single-file HTML prototype from a seed template + layout library. Faster than
  `taste-skill`'s full dial-driven build for throwaway/internal/low-stakes pages that explicitly
  don't need bespoke originality — not a substitute when the brief cares about not looking templated.
- `imagegen-frontend-web` / `imagegen-frontend-mobile` — aspect-ratio/composition-correct reference
  image generation for web vs. mobile targets respectively; feed the mobile variant into native
  mobile builds (`ios-developer`/`flutter-expert`/etc.), not the web one — wrong-platform composition
  otherwise.
- `design-review` / `redesign-skill` — audit-then-fix workflows for existing UIs.
- `accessibility` — WCAG 2.2 AA implementation.
- `react-best-practices` — Vercel's 45-rule performance catalogue.
- `canvas-design` — static PNG/PDF art (posters, illustrations), different medium from UI code.
- `threejs` — 3D scenes/materials/controls for the browser.
- `brandkit` / `brand-guidelines` — brand identity boards and reference tokens.

## Aesthetic Presets (invoke directly, not via taste-skill)
- `brutalist-skill` — Swiss/military industrial aesthetic.
- `minimalist-skill` — warm monochrome editorial minimalism.
- `soft-skill` — Apple/Linear-tier soft premium (double-bezel cards, squircle radii, spring motion).

## Usage Example
```
User: "Build an animated button component with Tailwind"
→ frontend-patterns (component scaffold) or magic-ui-generator (multi-variant AI gen)
→ tailwind-patterns (styling)
→ motion-ui (animation)
→ Result: Production button
```

## Fallback (off-context, pull via `python3 ~/.claude/overseer/search.py <name>`)
- Deep gesture/SVG/toast animation → `motion-advanced`, `motion-patterns`
- Non-React animation → `animejs-animation`, `threejs-animation`
- More component-library options → `frontend-upgrade-kit` (Magic UI, Aceternity-style, RetroUI, etc.)
- Documentation → BUNDLE-O
- Testing → BUNDLE-G
