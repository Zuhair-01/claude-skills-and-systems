---
name: artifact-quality
description: Anti-slop design engine for published Artifacts — the single-file HTML pages rendered by the Artifact tool and hosted on claude.ai. Use BEFORE writing any artifact whose look matters (landing page, dashboard, report, data-viz, tool, diagram, deck, game, form, portfolio). Covers the medium's hard constraints (CSP allowlist, no build step, theme-awareness, asset embedding), the default-Claude-artifact slop signature to kill, and a per-category playbook for every artifact type. Layers on top of the built-in artifact-design skill and defers universal taste rules to taste-skill Sections 4/6/9.
---

# artifact-quality: Make Artifacts Not Look Like AI Slop

> **Scope:** the `Artifact` tool specifically — one `.html` file, wrapped in a
> `<!doctype>…<body>` skeleton at publish time, served from its own origin on
> claude.ai. This is a *different medium* from a Next.js project. taste-skill
> Section 3's stack (React, RSC, `next/font`, Tailwind v4 postcss) mostly does
> **not** apply here. This skill supplies the medium-correct stack and the
> per-category design moves; taste-skill Sections 4 / 6 / 9 still own the
> universal taste rules (typography, color calibration, motion motivation,
> AI-tell avoidance, copy). The built-in `artifact-design` skill still owns
> publish mechanics — load it too.

---

## 0. WHEN THIS FIRES

Invoke this skill (before writing the file) whenever ALL of:
- the deliverable is going out through the `Artifact` tool (a hosted claude.ai page), **and**
- its visual quality matters — anyone will look at it, share it, or judge it.

Skip it only for a throwaway page the user explicitly framed as disposable, or a
pure Markdown artifact a loaded skill told you to publish (still run §4 + §8).

If the user asked for "a page / site / app / dashboard / report / deck / tool"
without saying *artifact*, and there's no repo to build into, the deliverable is
almost certainly an artifact — this skill fires.

**Order of operations:** `artifact-quality` (this file — medium + category
direction) → build → `artifact-design` (publish-mechanics sanity) → §8 pre-ship
→ `Artifact` publish. For a frontend brief that *also* names a real-world visual
look, `open-pinterest` still runs first per CLAUDE.md Rule 7.

---

## 1. THE MEDIUM: HARD CONSTRAINTS (violating any = broken artifact)

| Constraint | What it means for the build |
|---|---|
| **CSP allowlist** | Scripts load **only** from `cdnjs.cloudflare.com`, `cdn.jsdelivr.net/npm/`, `cdn.tailwindcss.com`, `code.jquery.com`. Stylesheets **only** from `fonts.googleapis.com` (+ font files from `fonts.gstatic.com`). **Everything else is blocked silently** — no external CSS, no external images, no `fetch`/XHR/WebSocket, no unpkg, no esm.sh. |
| **Inline everything** | All CSS and JS you write goes *in the file*. Third-party CSS → paste it inline. Images / fonts / audio you control → embed as `data:` URIs (counts toward the 16MB cap). |
| **No build step** | No JSX transpile, no PostCSS, no bundler. Ship browser-runnable HTML/CSS/JS. React only via **UMD builds** (`react/18.3.1/umd/react.production.min.js` + react-dom) with `React.createElement` or `htm` — never JSX source. Usually you don't need React at all. |
| **Skeleton is provided** | The file is wrapped in `<!doctype><head>…</head><body>` at publish. Write page content directly. Put your `<title>` + `<style>` at the top of the file. No `<html>/<head>/<body>` tags of your own. |
| **Theme-aware, 3 states** | Explicit choice → `data-theme="dark"`/`"light"` on `:root`. Default "system" → nothing stamped, only `prefers-color-scheme` separates them. Palette **must** be defined as tokens on bare `:root`, re-declared under `@media (prefers-color-scheme: dark):root:not([data-theme="light"])` **and** under `:root[data-theme="dark"]`. `body` needs an explicit token background — a transparent body borrows the host's theme and looks broken. See §7. |
| **Fonts** | No `next/font`. Use `<link>` to `fonts.googleapis.com` OR a system stack. Every face needs a real fallback stack. Self-hosted font → `@font-face` with a `data:` URI. |
| **16 MB cap** | Rendered page including every `data:` URI. Big hero image → compress hard (WebP, ~1600px max, quality ~72) before embedding, or use `picsum.photos`/a brand-provided URL. |
| **No horizontal body scroll** | Wide tables / diagrams / code / charts go in their **own** `overflow-x:auto` container. The page body never scrolls sideways at any width. |
| **`localStorage` works** | Per-artifact origin, per-viewer, survives republish, never reaches Claude or other viewers. Wrap every read/write in try/catch — it throws in some contexts. Good for: remembered tab, collapsed section, unsent draft. Not for anything that must persist reliably. |
| **Mermaid is native** | ` ```mermaid ` fences (MD) or `<pre class="mermaid">` (HTML) render with no library. Don't load mermaid.js. |
| **Downloads are inert for viewers** | `<a download>` (incl. `data:`/`blob:`), script-driven saves — all blocked in the viewer sandbox. Never hand the viewer a file via a link. Use the `assets`/SendUserFile capability path instead (see `artifact-capabilities`). |

**CDN libraries, how to load:** `<script src="https://cdnjs.cloudflare.com/ajax/libs/<lib>/<exact-version>/<umd-file>"></script>` **before** any inline script that uses it, pinned to an exact version, UMD build (defines a global). Common good picks that exist on cdnjs: `gsap`, `d3`, `chart.js`, `three`, `anime`, `pixi.js`, `echarts`, `katex`, `marked`, `dompurify`, `lucide` (icon font/sprite), `canvas-confetti`, `tone`, `matter-js`, `p5`, `dayjs`.

---

## 2. THE DEFAULT-CLAUDE-ARTIFACT SLOP SIGNATURE (kill on sight)

The look every un-directed artifact converges to. If your draft has 3+ of these,
it reads as AI slop regardless of how clean the code is:

1. **Inter (or system-ui) at every size**, one weight, no display face.
2. **Indigo / violet / purple-blue accent** (`#6366f1`, `#8b5cf6`, `#7c3aed`) — often as a gradient, often glowing.
3. **`bg-gray-50` / `#f9fafb` page**, white cards, `shadow-sm`, `rounded-xl`, `border-gray-200`. The "Tailwind default component gallery" surface.
4. **Everything centered** — centered hero, centered section headings, `max-w-2xl mx-auto` on all prose.
5. **Three equal cards in a row**, each with an emoji or a Lucide icon in a tinted circle, a bold line, two gray lines.
6. **Emoji as UI** — 🚀 in the H1, ✨ on the CTA, 📊 📈 🎯 as section markers.
7. **A single hero gradient blob** (radial, purple→transparent, `blur-3xl`, `opacity-20`) behind centered text.
8. **No motion, or infinite pulse on everything.**
9. **Dark mode = `filter: invert()` energy** — gray text on gray, no real dark palette, `body` background left transparent.
10. **Fake data that's obviously fake** — "Lorem ipsum", "$123,456", "John Doe", "Acme Inc", flat 12-month arrays.

The fix is never "add more" — it's **pick a real direction** (§5) and commit.

---

## 3. STACK FOR ARTIFACTS (medium-correct defaults)

**Default: vanilla.** HTML + modern CSS + a little vanilla JS handles the large
majority of artifacts (landing, report, dashboard, diagram, deck, portfolio,
timeline, most tools). Reach for a library only when it earns its bytes.

| Need | Reach for | Not |
|---|---|---|
| Layout, spacing, responsive | Native CSS Grid + `clamp()` + container queries + `min()/max()` | flexbox percentage math |
| Styling system | Hand-written CSS with `:root` tokens (§7). Tailwind **Play CDN** (`cdn.tailwindcss.com`) only for speed on a simple page — never ship it with the default palette; set `tailwind.config` inline with real tokens | shipping Play-CDN Tailwind untouched |
| State / interactivity | Vanilla JS, `<template>`, event delegation, CSS `:has()`/`:target`/`<details>` for zero-JS toggles | React for a page with two buttons |
| Charts | `dataviz` skill's guidance + Chart.js or ECharts or hand-rolled inline SVG/D3. Read `dataviz` before writing chart code. | a chart lib's default colors |
| Motion | CSS transitions/`@keyframes`, Web Animations API, `animation-timeline: scroll()` (guard with `@supports`). GSAP (cdnjs) only for pin/scrub/timeline sequencing. | framer-motion (needs a build) |
| 3D | `three` UMD from cdnjs, raw WebGL, or `pixi.js` for 2D-accelerated | react-three-fiber (needs a build) |
| Icons | Inline SVG you paste from a set (Lucide, Phosphor, Tabler — grab the paths), or the Lucide sprite from cdnjs. One family. `strokeWidth` fixed globally. | emoji, hand-drawn `<path>` |
| Rich text / MD render | `marked` + `dompurify` (both cdnjs) | `dangerouslySetInnerHTML` unsanitized |
| Real React app (genuine component tree, heavy interactivity) | React + ReactDOM UMD from cdnjs + `htm` (cdnjs) for JSX-like syntax without a transpile | pretending you can ship `.jsx` |

**Fonts that aren't Inter** (all on Google Fonts, `<link>`-able): *Space Grotesk,
Bricolage Grotesque, Instrument Sans, Sora, Fraunces, Newsreader, Libre
Caslon, DM Sans, DM Mono, IBM Plex Sans/Mono, Geist (via cdnjs `@fontsource`
inline), Archivo, Manrope, Spectral, Source Serif 4, JetBrains Mono.* Pick a
**display** face + a **text** face + optionally **mono**. Per taste-skill 4.1:
serif is *only* for genuinely editorial/report artifacts, and `Fraunces`/
`Instrument Serif` are banned as the lazy default even there — rotate.

---

## 4. UNIVERSAL TASTE (defer to taste-skill, apply this subset always)

Every artifact, regardless of category, gets the taste-skill checks that don't
depend on being a marketing page. Load taste-skill for the detail; the
high-yield subset:

- **4.1 Typography** — display face ≠ text face isn't automatic; real scale (`clamp()`), `tracking-tight` on display, `max-width: 65ch` on prose, italic-descender clearance.
- **4.2 Color** — ONE accent, locked page-wide, saturation < 80%, neutral base (zinc/slate/stone/warm-gray — pick one temperature). The LILA RULE: no default purple glow. Tint shadows to the background hue.
- **4.4 Shape** — one corner-radius scale, one border treatment, cards only when elevation means something.
- **4.5 States** — loading (skeleton, not spinner), empty (composed, tells you how to fill it), error (inline), `:active` tactile feedback, button/text contrast WCAG AA (4.5:1 body, 3:1 large).
- **4.9 Long lists** — >5 items is a grid / filter / accordion / table, never a raw 40-row `<ul>`.
- **6.B Reduced motion** — every animation wrapped in `@media (prefers-reduced-motion: no-preference)` or given a static fallback.
- **9 / 4.9 Copy** — no Lorem, no em-dash-itis, real-looking data, no "Trusted by" without real logos. If data is illustrative, label it *illustrative*.
- **Anti-default (0.D)** — no AI-purple gradient, no centered-hero-over-mesh, no three-equal-emoji-cards, no glass-on-everything, no infinite-loop-everywhere.
- **Data honesty (dashboards, reports, trackers, meters)** — round to the precision the data supports ("~75%", never "74.3%"); chart bars must match their axis labels; a low or zero value is shown *neutral*, never as red or a "loss". No countdown timers, no manufactured urgency, no streak-loss framing on anything a person builds a habit around. (`30 - Resources/Applied_Reasoning_And_Persuasion_Principles.md` §5.)

---

## 5. CATEGORY PLAYBOOKS

Classify the artifact, then build to its row. Each playbook: the **slop tell**
for that type, then the **moves** that fix it. Cross-cutting rules (§1, §4, §7)
still apply on top.

### 5.1 Landing / marketing / product page
- **Slop tell:** centered hero, purple gradient blob, 3 emoji feature cards, `bg-gray-50`, "Get Started" + "Learn More" buttons, fake logo wall of styled `<span>`s.
- **Moves:** Use taste-skill Sections 0–12 as the build engine (this *is* its home category) but with §3's vanilla stack, not Next. Asymmetric or split hero (VARIANCE 7–9), one locked accent, real generated/`picsum` imagery (taste-skill 4.8 — text-only is incomplete), ≥4 distinct section layout families, ≤1 eyebrow per 3 sections, hero fits one viewport, nav on one line. Motion: scroll-reveal via `animation-timeline: scroll()` + one deliberate hero moment.
- **Verify:** taste-skill §14 Pre-Flight (full) + §8 here.

### 5.2 Dashboard / analytics / metrics view
- **Slop tell:** 4 identical KPI cards with a green ▲ and a fake %, a single line chart, sidebar of emoji nav items, everything `rounded-xl shadow-sm`.
- **Moves:** Density is the point — VISUAL_DENSITY 6–8, so **plain layout over card-in-card**; group with `border-t`/`divide-y`, not nested elevation. One accent for "primary metric / positive", one neutral-dark for "attention", never a rainbow of status hues (taste-skill 4.2 — dashboards are the worst offender). Numbers get a **tabular-nums** mono or a proper figures setting, right-aligned. Real chart work → `dataviz` skill + its palette validator. Every widget gets loading + empty + error states (§4.5). Tables → hand-rolled `<table>` with sticky `<thead>` in an `overflow-x:auto` wrapper, or a small D3/vanilla virtual list past ~200 rows. Sidebar/topbar: single-line, ≤72px topbar, inline-SVG icons one family.
- **Verify:** `uxui-principles` + §8 + taste-skill 4.2/4.4/4.5.

### 5.3 Document / report / memo / long-form explainer
- **Slop tell:** `max-w-2xl mx-auto`, Inter 16px, `#374151` body, H2s with an emoji, a gray callout box every other paragraph, no hierarchy between a section and a sub-point.
- **Moves:** This is the one category where **editorial serif is a legit default** (taste-skill 4.1) — pair a text serif (Newsreader, Source Serif 4, Spectral, Libre Caslon) with a grotesque display/label face; rotate, don't reach for Fraunces. Real prose measure (62–72ch), `line-height ~1.65`, `text-wrap: pretty` on headings, `hanging-punctuation` where supported. Give the document a **masthead** (title / author-or-context / date / reading time) and a sticky or margin **table of contents** that scroll-spies via `IntersectionObserver`. Footnotes as `<sup>` + a real notes section, not parenthetical asides. Pull-quotes and data callouts get *one* treatment, used consistently. Drop caps or a rule-and-smallcaps section opener beats an emoji. Dark mode: warm off-black paper (`oklch(0.16 0.01 60)`), not `#000`.
- **Verify:** `accessibility` (reports are heavily screen-read) + taste-skill 4.9/4.10 + §8.

### 5.4 Data-viz / chart-forward piece
- **Slop tell:** Chart.js defaults (that specific teal/pink/purple), a legend nobody reads, gridlines everywhere, no title that states the finding, 3D pie.
- **Moves:** **Read the `dataviz` skill before the first line of chart code** — it has a form heuristic, a color formula with a runnable validator, and mark specs. Chart title states the *takeaway* ("Signups doubled after the pricing change"), not the *variable* ("Signups over time"). Direct-label series, kill the legend where you can. One sequential or one categorical ramp from `dataviz`'s palette, validated. Axes: start bars at zero, don't truncate; thin or no gridlines; `tabular-nums` on tick labels. Annotate the point that matters. Everything in an `overflow-x:auto` wrapper with a sensible `min-width` so mobile scrolls instead of squishing. Motion: a single on-load draw-in (respecting reduced-motion), not perpetual.
- **Verify:** `dataviz`'s own validator + §8.

### 5.5 Tool / calculator / converter / interactive utility / mini-app
- **Slop tell:** one centered `<input>`, a purple "Calculate" button, result in an `alert()`-shaped box, no keyboard support, no persistence, no empty/error state.
- **Moves:** Layout the tool like an instrument: inputs grouped left/top, output prominent and live-updating (no submit button for anything cheap to compute — bind on `input`). Labels above inputs, helper + error text in the markup (§4.6). Full state cycle (§4.5) — including invalid input handled *inline*. Persist the last-used inputs to `localStorage` (try/catch). Keyboard: everything reachable, `Enter` does the obvious thing, visible focus rings. If there's a result to share, use the capability path, never a download link (§1). Show the *method* (a formula, a breakdown) not just a number — that's what makes a tool feel trustworthy vs. a black box. `prefers-reduced-motion` on any transition.
- **Verify:** `accessibility` (keyboard-only pass) + §8.

### 5.6 Diagram / architecture / flow / system explainer
- **Slop tell:** raw Mermaid default theme (that lavender fill, Comic-ish edges), or a grid of divs with arrows made of borders.
- **Moves:** Prefer the **`archify` skill** — it produces validated, themed, exportable diagram artifacts and is already wired in. If hand-doing it: native Mermaid (`<pre class="mermaid">`) but with an inline `mermaid.initialize({ theme: 'base', themeVariables: {...} })` mapped to your §7 tokens so it matches the page in both themes. For bespoke diagrams, **inline SVG** with real layout math, consistent node sizing, orthogonal or smooth-curve edges (`stroke-linecap:round`), labeled edges, a legend if there are node types. One accent for "the path being highlighted", neutral for everything else. Optional: a trace/draw-on animation via `stroke-dasharray` (reduced-motion aware). Wrap in `overflow:auto` with pan/zoom only if it genuinely doesn't fit.
- **Verify:** `artifact-diagramming` skill + §8.

### 5.7 Game / interactive toy / simulation / generative piece
- **Slop tell:** `<canvas>` with a 2px black border centered on `bg-gray-50`, "Score: 0" in Inter, arrow-keys-only, no start screen, no restart, no mobile input.
- **Moves:** Full loop — start screen, play, pause (on blur / `Esc`), game-over with restart, score persistence to `localStorage`. `requestAnimationFrame` with a fixed timestep accumulator, not frame-coupled physics. Canvas sized to `devicePixelRatio`, `image-rendering: pixelated` only if the art is pixel art. Input: keyboard **and** pointer/touch (on-screen controls or tap zones on mobile). Sound optional and behind a mute toggle + first-gesture unlock (`Tone` or raw `AudioContext`, both fine). Give it a *look* — a palette, a font, a title treatment — a game is a tiny brand. Libraries if warranted: `matter-js` (physics), `p5` (creative coding), `pixi.js` (many sprites). No external asset fetches — sprites/audio are `data:` URIs or drawn procedurally.
- **Verify:** manual playtest of every state + §8 + 60fps check.

### 5.8 Form / survey / quiz / poll / sign-up sheet
- **Slop tell:** placeholder-as-label, one long ungrouped column, a purple submit button, no validation until submit, "Thank you!" that replaces the page with nothing.
- **Moves:** Labels always visible and above the field (§4.6), never placeholder-as-label. Group related fields with `<fieldset>`/legend. Validate on blur, summarize errors at submit with focus moved to the first bad field, `aria-describedby` wiring the error to the input. Progress indication for multi-step (real steps, focus moves to the new step heading). A composed success state that says what happens next. If it actually collects responses (poll/sheet/quiz-with-results), that needs a runtime capability — load `artifact-capabilities`; a pure-frontend form that pretends to submit is slop. Radio/checkbox: real inputs styled via `:checked` + `:has()`, not divs with click handlers. Never build a form that collects credentials or payment under false pretenses (publish policy).
- **Verify:** `accessibility` (full form a11y pass) + §4.5 + §8.

### 5.9 Slide deck / pitch / presentation
- **Slop tell:** 16:9 divs stacked vertically, one giant centered word per "slide", a purple accent bar, no navigation, bullet lists in Inter.
- **Moves:** Real deck mechanics — one slide in view at a time, keyboard (`←/→`, `Space`), on-screen prev/next, a slide counter, ideally `?slide=N` in the hash and a press-`o` overview grid. Each slide is a `min-h-[100dvh]` (or fixed-aspect) section with a consistent safe-area margin. Vary slide layouts (title / statement / data / image-led / quote / comparison) — a deck where every slide is "heading + 3 bullets" is a slop tell. One type system, one accent, a visible baseline grid. Transitions: a single crisp slide/fade via the View Transitions API or a CSS transform, reduced-motion aware. Presenter-ish niceties: a subtle progress bar, `f` for fullscreen.
- **Verify:** taste-skill 4.3 (layout diversification across slides) + §8.

### 5.10 Portfolio / profile / résumé / "about me"
- **Slop tell:** centered avatar circle, name in Inter bold, a row of Lucide social icons, three project cards with `picsum` images and "Project One / Lorem", a purple "Contact Me".
- **Moves:** Pick a point of view — editorial, brutalist, minimal-Swiss, terminal, monospace-zine — and commit (taste-skill picks one from the brief). Real hierarchy: the *work* is the hero, not the avatar. Project entries get real structure (role, year, stack, outcome, one strong image or an actual embed) and at least two layout treatments across the list. Type-led is fine here — a strong display face doing most of the work. If it's a résumé specifically: print stylesheet (`@media print`), real dates, `overflow-x:auto` never needed because it's one column. One contact CTA, one label for it, everywhere (§4.7 no-duplicate-intent).
- **Verify:** taste-skill §14 + §8.

### 5.11 Timeline / roadmap / changelog / process walkthrough
- **Slop tell:** a vertical purple line with alternating left/right cards, each with an emoji dot, dates in gray Inter, infinite identical entries.
- **Moves:** If >8 entries, the alternating-card timeline breaks down — switch to a dense left-rail-date + right-content list, or group by period with sticky period headers. Consistent entry structure, but vary emphasis (a major milestone gets a full-width break). Real dates, `<time datetime>`. The connecting line is a `border-l` or a thin SVG, not a fat gradient. Optional scroll-reveal per entry (`animation-timeline: view()`), reduced-motion aware. For a changelog: version + date + categorized changes (Added/Fixed/Changed), filterable by type if long.
- **Verify:** taste-skill 4.3 (don't repeat one layout family down the whole page) + §8.

**Spans two categories?** (e.g. a report with an embedded dashboard panel) —
build the shell to its playbook, build the panel to *its* playbook, run both
verify passes.

---

## 6. MOTION IN A SINGLE FILE (no build, no framer-motion)

- **Default:** CSS `transition` + `@keyframes` + `Web Animations API` (`el.animate([...], {...})`) for anything sequenced from JS.
- **Scroll-reveal / parallax:** native `animation-timeline: scroll()` / `view()`, wrapped in `@supports (animation-timeline: view())` with a "just show it" fallback. ~85% support in 2026; the fallback covers the rest.
- **Route/state transitions:** `document.startViewTransition()` — native, cross-browser 2026, respects `prefers-reduced-motion` when guarded.
- **Pin / scrub / stagger-timeline / horizontal-pan:** GSAP + ScrollTrigger from cdnjs (`gsap/3.x/gsap.min.js` + `ScrollTrigger.min.js`). This is the one motion case worth a library.
- **Every** animation lives under `@media (prefers-reduced-motion: no-preference)` or has an explicit static end-state. Motion must be *motivated* — a one-sentence reason per effect (taste-skill §5). No infinite pulse/float/shimmer on every card (the named tell).
- Continuous values (scroll progress, pointer position) → drive a CSS custom property via `requestAnimationFrame`, not React state, not a layout-thrashing `style.top`.

---

## 7. THEME-AWARE PALETTE RECIPE (mandatory pattern)

```css
:root {
  color-scheme: light dark;
  --bg:        oklch(0.98 0.005 95);
  --surface:   oklch(0.995 0.003 95);
  --text:      oklch(0.22 0.01 60);
  --text-dim:  oklch(0.48 0.01 60);
  --border:    oklch(0.90 0.005 95);
  --accent:    oklch(0.62 0.16 250);   /* pick ONE, not purple-by-default */
  --accent-fg: oklch(0.99 0 0);
  --radius: 10px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:       oklch(0.17 0.01 60);
    --surface:  oklch(0.21 0.012 60);
    --text:     oklch(0.94 0.006 95);
    --text-dim: oklch(0.68 0.01 95);
    --border:   oklch(0.30 0.012 60);
    --accent:   oklch(0.70 0.15 250);
    --accent-fg: oklch(0.15 0.01 60);
  }
}
:root[data-theme="dark"] {
  /* repeat the dark values so an explicit toggle wins in both directions */
  --bg: oklch(0.17 0.01 60); --surface: oklch(0.21 0.012 60);
  --text: oklch(0.94 0.006 95); --text-dim: oklch(0.68 0.01 95);
  --border: oklch(0.30 0.012 60); --accent: oklch(0.70 0.15 250);
  --accent-fg: oklch(0.15 0.01 60);
}
body { background: var(--bg); color: var(--text); }
```

Rules:
- **Never** give a color its only definition inside a media/`[data-theme]` block — bare `:root` always has the full set.
- `body` **always** gets an explicit token background (transparent = borrows host theme = looks broken).
- Keep brand HEX as source of truth if given; derive ramp/variants in OKLCH (perceptually uniform).
- If you add a theme toggle: flip `data-theme` on `:root`, persist to `localStorage` (try/catch), and default to "no attribute = follow system".
- Design *and test* both themes before publishing (§8).

---

## 8. PRE-SHIP CHECKLIST (run before every `Artifact` publish)

**Medium correctness**
- [ ] No `<html>/<head>/<body>` tags I added; `<title>` + `<style>` at top of file.
- [ ] `<title>` is a real 2–4-word name, stable, not a summary. `favicon` emoji set (first publish only).
- [ ] Zero external resources outside the CSP allowlist. No `fetch`/XHR to anything. All images/fonts/audio I control are `data:` URIs or allowlisted URLs.
- [ ] Every CDN script pinned to an exact version, UMD build, loaded before the inline script that uses it.
- [ ] Rendered size < 16MB.
- [ ] No `<a download>` / script-save handed to the viewer.
- [ ] Wide content (tables, charts, diagrams, code) each in its own `overflow-x:auto` box. Body does not scroll horizontally at 320px, 768px, 1440px.
- [ ] Every `localStorage` access in try/catch, page renders fine with no stored value.

**Theme**
- [ ] Full palette on bare `:root`. Dark values under both `@media prefers-color-scheme` (guarded `:not([data-theme="light"])`) and `:root[data-theme="dark"]`.
- [ ] `body` has an explicit token background.
- [ ] Checked in light, dark, and system-default — all three legible, no gray-on-gray, no invisible borders.

**Taste (taste-skill subset, §4)**
- [ ] Not the slop signature (§2) — display face present, accent is not default-purple, not `bg-gray-50`+white-cards, not centered-everything, no emoji-as-UI.
- [ ] ONE accent, locked page-wide. One neutral temperature. One radius scale. One icon family, fixed strokeWidth.
- [ ] Loading / empty / error states exist wherever they can occur. Buttons + text pass WCAG AA contrast.
- [ ] Every animation is reduced-motion-guarded and motivated. No infinite-loop-on-everything.
- [ ] No Lorem, no fake-obvious data, illustrative data labeled as such. Long lists aren't raw `<ul>`s.

**Category**
- [ ] Ran the matching §5 playbook's verify line (its specialist skill + named taste-skill sections).
- [ ] If it collects responses / needs live or shared state / per-viewer identity → declared the right runtime capability via `artifact-capabilities` (a form that only pretends to submit is slop).

**Security (CLAUDE.md Rule 8 pre-ship gate)**
- [ ] Any user-supplied string rendered as HTML goes through `dompurify` (or `textContent`, never `innerHTML`).
- [ ] No secrets / API keys / tokens in the file (it's world-readable once shared).
- [ ] Not impersonating a real person/org; no fabricated records presented as genuine; no credential/payment collection under false pretense.

---

## 9. RELATIONSHIP TO OTHER SKILLS

| Skill | Owns |
|---|---|
| `artifact-quality` (this) | Medium constraints, slop signature, per-category design direction, the artifact stack. |
| `artifact-design` (built-in) | Publish mechanics, title/favicon/description rules, update flow. Load alongside this. |
| `artifact-diagramming` (built-in) | Inline-SVG diagram mechanics for artifacts — pairs with §5.6. |
| `artifact-capabilities` (built-in) | Runtime capability contracts — load when §5.5 / §5.8 / a stateful page needs them. |
| `taste-skill` | Universal taste engine (Sections 4/6/9) + the landing/portfolio build engine reused by §5.1/§5.10. This skill is its Artifact-medium adapter. |
| `dataviz` | All chart/graph/KPI work — mandatory read for §5.2/§5.4. |
| `archify` | Preferred builder for §5.6 diagram artifacts. |
| `open-pinterest` | Runs first (CLAUDE.md Rule 7) when the brief names a real-world visual/motion look. |
