---
name: frontend-reference-sources
description: Router for WHERE to source a real-world visual/motion/component reference before a frontend build — picks the right gallery among Pinterest, refero.design, supahero.io, 60fps.design, 21st.dev, and points motion.dev at implementation. Use whenever a frontend/UI task calls for a specific real-world look or interaction (not pure logic/layout). This is the "source before you build" step BUNDLE-B-frontend and CLAUDE.md Rule 7's frontend sub-rule require; it replaces "go straight to open-pinterest" with "pick the best-fit source first".
---

# Frontend Reference Sources

Before building any UI with a specific real-world look/motion (Rule 7 frontend sub-rule),
pick the right source here, pull the actual reference (image / video / component), then hand
it to the build skill (`taste-skill` / `visual-to-code` / `motion-ui` / `threejs` / `apex-frontend-lab`).
Pure logic/layout with no look requested → skip this, build directly.

All galleries are browsed with the `claude-in-chrome` skill (same flow as `open-pinterest`:
navigate, scroll to load, screenshot/`read_page` to judge, collect image/video URLs via
`javascript_tool`, download into `design-refs/<source>/<topic>/`). None need a paid API.

## Which source

| Source | Reach for it when | What you get | Notes |
|---|---|---|---|
| **open-pinterest** (skill) | Broadest net — a style/metaphor/texture/3D look with no obvious category home; need to fan out many queries; need subject background-cut | Stills + video pins, `remove_bg.py`, visual-similarity drill-down | The general fallback. Full sourcing/eval/wire-in protocol lives in that skill — the other rows below still follow its step 2 (judge every candidate) and step 7-8 (wire in + close the loop). |
| **refero.design/styles** | Want *real shipping product UI* organized by style, element, or page type (auth, onboarding, pricing, settings, empty states…) — more curated to product design than Pinterest | Full-page + component screenshots from real apps, filterable by style tag | Best first stop for "what do good X screens actually look like". `https://refero.design/styles` for style index; browse categories/elements from the nav. Screenshots are style refs, not code — never ship one as-is. |
| **supahero.io** | The task is specifically a **hero section** (landing/marketing top fold) | Curated gallery of real hero sections, many with the interaction visible | `https://supahero.io`. Narrow and deep — use it instead of a generic "hero" Pinterest query when hero is the actual deliverable. |
| **60fps.design** | Need a **motion / micro-interaction** reference — transition timing, easing feel, scroll behavior, hover/press detail — judged as video, not a still | Short screen-recordings of high-craft UI animations | `https://60fps.design`. The curated equivalent of open-pinterest's video-pin path; prefer it when the ask is about *how it moves*. Download the clip, name the technique for `motion-ui`. |
| **21st.dev** | Want **component-level building blocks** (animated buttons, marquees, bento grids, nav, pricing tables) as actual React/Tailwind code, or multi-variant exploration | Browsable registry of community React components + Magic MCP | Route via the **`magic-ui-generator`** skill (+ `shadcn`) — it already wraps 21st.dev/Magic. Use for "give me 3 versions of this component", not for whole-page direction. |
| **skiper-ui.com** | Want a **premium animated component** (scroll-triggered reveals, cursor-follow effects, parallax cards, marquees) with copy-paste React/Tailwind + Motion code already wired | Curated, higher-polish component gallery than raw 21st.dev — each entry ships working code, not just a screenshot | `https://skiper-ui.com`. Browse with `claude-in-chrome`, copy the component code directly (it's MIT/open, not a style ref) — adapt props/content to the brief, don't ship unstyled. Good default before 21st.dev when the bar is "looks expensive." |
| **VengeanceUI** (GitHub `Ashutoshx7/VengeanceUI`) | Want **landing-page-specific animated sections** (hero, feature grid, testimonial, CTA blocks) as copy-paste components, subtle rather than flashy | Open-source (1k+★) component set built for landing pages — Tailwind + animation, tasteful/restrained by design | Pull via `gh repo view Ashutoshx7/VengeanceUI` / clone, or browse their docs site if linked from the repo. Best fit for whole-landing-page assembly rather than one hero/motion element — pairs with supahero for hero-specific direction. |
| **animata.design** | Want a **single reusable CSS/React micro-animation** (hover cards, text reveals, loaders, buttons, badges) as a drop-in snippet, broader and more granular than skiper-ui's larger sections | Open-source animated component gallery, categorized by element type, copy-paste code per component | `https://animata.design`. Use for small/atomic motion pieces feeding into a larger composition — the granular counterpart to skiper-ui/VengeanceUI's bigger sections. |
| **motion.dev** | **Implementation**, not reference — you've picked the motion and need to build it in React/JS | The Motion library (successor to Framer Motion) docs + examples | Not a gallery. Feeds **`motion-ui`**. Docs: `https://motion.dev/docs`; `https://motion.dev/llms.txt` for a token-cheap docs dump (via `context7` / `WebFetch`). |
| **GSAP** (`gsap.com`) | **Implementation** — scroll-scrubbed / pinned / horizontal-scroll sequences, choreographed timelines, SplitText reveals, SVG morph/draw, Flip | GreenSock library + all plugins (100% free since Apr 2025, no key) | Not a gallery. Feeds **`motion-ui`** → off-context `gsap-*` skills (`gsap-scrolltrigger` is the main one). Use GSAP for the scroll spine, Motion for components. |
| **Spline** (`spline.design`) | **Implementation** — a decorative/hero interactive 3D scene where a designer-built scene beats hand-coding three.js | Hosted `.splinecode` scene URL + React/vanilla runtime | Not a gallery. Feeds **`threejs`** → off-context `spline-3d-integration` skill. Heavier payload — lazy-load + fallback + mobile downscale mandatory. Raw three.js when 3D is the product. |
| **bklit UI** (`bklit.com`, `ui.bklit.com/studio`) | **Implementation** — charts & data-viz components in a shadcn/React project (line/area/ring/radar, legends) | shadcn registry + interactive Studio playground that emits React code | Not a gallery. Feeds **`dataviz`** + **`shadcn`** + `taste-skill` dashboard/data-heavy route. `npx shadcn@latest add` from the bklit registry; tune in Studio, copy code. Built on shadcn/ui + Recharts — fits any existing shadcn app. |
| **Arabic Font Pack** (local, `Second_Brain/30-Resources/Fonts/Arabic/`) | Brief needs Arabic type and doesn't name a specific typeface — hero calligraphy, display headline, heading family, or body/UI text | 4 pre-studied families (decorative Thuluth script, 2 display faces, a headings family, a full-weight-ladder text face, a small-size UI face) with a by-role decision table already built from rendered previews | Not a gallery — already-owned assets. Read `Arabic_Font_Pack_Guide.md` in that folder before defaulting to a Google Fonts Arabic face; it says which of the 4 to reach for by role (hero/display/heading/body/dense-UI), not just by name. |
| **heritagetype.com** | Brief needs a real **vintage/heritage typeface specimen** — period-accurate lettering to reference or trace for a logo, wordmark, or display headline (not a generic Google Fonts pick) | Curated vintage type specimens, scanned/rendered, browsable by era/style | Public gallery, browse with `claude-in-chrome` like refero — screenshot the specimen, never ship the scan itself as a font; use it as the shape/weight/era reference when picking or customizing a real webfont. |
| **oldbookillustrations.com** | Brief needs **public-domain 19th-century engravings/illustrations** — botanical, anatomical, ornamental, or figurative line art for a vintage/editorial/apothecary aesthetic | High-res scans of real antique book plates, public domain, free to use directly (not just a style reference) | Actual usable assets, not just inspiration — download and use the image itself (still background-cut with open-pinterest's `remove_bg.py` if only the subject matters against a new ground). Site is browsable/searchable by subject. |
| **imagetopaper.com** | Brief needs **paper/print textures** (aged paper, canvas, grain) or a quick photo→paper-texture conversion for a vintage/print-look background | Paper texture library + a paper-effect image converter | Use for background texture layers under vintage type/illustration compositions — pairs naturally with heritagetype + oldbookillustrations for a full period-print look. |

## Flow

1. Classify the ask: whole-page look → refero (or Pinterest); hero → supahero; motion/interaction → 60fps; a polished animated component/section → skiper-ui or VengeanceUI (landing-page sections) before 21st.dev; a small atomic micro-animation → animata.design; a broader/multi-variant component search → 21st.dev via `magic-ui-generator`; vintage/period type or print texture → heritagetype/oldbookillustrations/imagetopaper; already know the motion, need to code it → motion.dev via `motion-ui`. When in doubt or the category is fuzzy → `open-pinterest`. Multiple apply (e.g. hero *with* a specific scroll motion) → hit both (supahero + 60fps).
2. Source + judge every candidate against the brief (open-pinterest step 2 — caption match ≠ visual match; goal-fit filter).
3. Download into `design-refs/<source>/<topic>/`.
4. Hand to the build skill as visual direction; make it name the concrete technique it's replicating.
5. Close the loop: note the reusable technique in the project's design doc so next time it's built directly, not re-sourced (open-pinterest step 7).
6. Completion gate: cite the real `design-refs/<source>/<topic>/` path and the component file/line where the technique landed — a download with nothing referencing it is an unfinished task.

## Tooling

**motion.dev docs — `scripts/fetch_motion_docs.py`** (no deps, no browser):
- `python scripts/fetch_motion_docs.py` → the full llms.txt index (every doc + `/examples/*` code demo, one line each)
- `python scripts/fetch_motion_docs.py scroll` → index lines matching a term
- `python scripts/fetch_motion_docs.py https://motion.dev/docs/react-scroll-animations` → that page as text
Use this from `motion-ui` when implementing a Motion animation — it's the canonical API source, cheaper than `context7` and always current.

**Galleries (refero / supahero / 60fps) — browser collection.** All three are JS SPAs; a plain
HTTP scraper gets nothing. Browse with `claude-in-chrome` (navigate → scroll to load → judge
candidates on screen), then collect asset URLs in one `javascript_tool` pass and download with
open-pinterest's `scripts/download.py` (images) / `download_video.py` (60fps clips):
```js
// images (refero, supahero): grab full-res, skip thumbs/sprites
Array.from(document.querySelectorAll('img')).map(i => i.currentSrc || i.src)
  .filter(s => /refero\.design|supahero|cdn|images\./.test(s) && !/icon|logo|avatar/.test(s))
// 60fps: motion clips are <video>, collect the sources
Array.from(document.querySelectorAll('video')).flatMap(v =>
  [v.currentSrc, ...Array.from(v.querySelectorAll('source')).map(s => s.src)]).filter(Boolean)
```
Save into `design-refs/refero/<topic>/` etc. Same judge-every-candidate + wire-in + completion-gate rules as `open-pinterest`.

**21st.dev components — Magic MCP (optional, needs a free key).** `magic-ui-generator` already
covers browsing 21st.dev. For in-session multi-variant generation add the official MCP once:
```
setx TWENTY_FIRST_API_KEY "<key from https://21st.dev/magic/console>"
claude mcp add magic -- cmd /c npx -y @21st-dev/magic@latest
```
It then appears as `mcp__magic__*` tools. Until added, use `magic-ui-generator` + browser.
