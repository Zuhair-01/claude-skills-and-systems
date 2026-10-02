---
name: design-taste-frontend
description: Anti-slop frontend skill and category router for any UI surface — landing pages, portfolios, redesigns, dashboards, data-heavy product UI, mobile, and more. Reads the brief, infers the right design direction, and either builds directly (marketing/portfolio/redesign) or routes the build to the best-fit specialist skill for the category (Section 13) — then runs a monitor pass on the output before calling it done.
---

# tasteskill: Anti-Slop Frontend Skill + Category Router

> Scope: **any page or app**, not just marketing. Sections 0-12 are the taste/build engine — built for landing pages, portfolios, and redesigns, and reused wherever they fit (typography, color, motion, a11y, AI-tell avoidance apply everywhere). Section 13 is the router: for categories this engine isn't the right tool for (dashboards, data tables, wizards, mobile, etc.), it names the actual skill in stock to build with, dispatches to it, and runs a monitor pass on what comes back — never "this is out of scope, stop."
> Every rule below is **contextual**. None of it fires automatically. First read the brief, classify the category (Section 13), then pull only what fits.
>
> **Deliverable is a published Artifact** (single-file HTML on claude.ai, via the `Artifact` tool — the usual case when there's no repo to build into)? Invoke **`artifact-quality` first.** It owns the medium's hard constraints and a per-category playbook; Section 3's React/Next stack does not apply there. Sections 4/6/9 below still supply the universal taste rules. See Section 13.A's first row.

---

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog, or anything else (dashboard, product app, mobile, data-heavy, ecommerce, etc.) — for the "anything else" case, go straight to Section 13's Category Router before doing anything else.
2. **Vibe words** the user used - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** - logo, color, type, photography. For redesigns, these are starting material, not optional input (see Section 11).
6. **Quiet constraints** - accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
Before any code, state in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Example reads:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."*

### 0.C If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question - never a multi-question dump - and only when the design read genuinely diverges. Example: *"Should this feel closer to Linear-clean or Awwwards-experimental?"*

If you can confidently infer from context, **do not ask**. Just declare the design read and proceed.

### 0.D Anti-Default Discipline
Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the design read.

**Data & habit honesty** (any dashboard, tracker, progress surface, or growth feature — applies through the Section 13 router too): round to the precision the data supports ("~75%", not "74.3%"); chart bars must match their axis; a low/zero/quiet value renders *neutral*, never red or framed as a loss; no countdown timers, no streak-loss anxiety, no manufactured urgency, no variable-ratio reward drops. A design that pressures the user only when they *don't* pause or check elsewhere has crossed from persuasion into a dark pattern — and that's a retention liability, not just an ethics one. Detail + why: `Second_Brain/Workflow/30 - Resources/Applied_Reasoning_And_Persuasion_Principles.md` §5 + §4.

### 0.E Pattern choice logic
When the brief doesn't explicitly name dark/light mode, glassmorphism, brutalism, bento grid, or custom-vs-official design system, decide using Appendix E's source-backed criteria, not the first option that comes to mind. Ground the "Design Read" one-liner (0.B) in that logic, not a coin flip.

### 0.F Reference-Match Protocol
Fires whenever the brief says "like `<site/product>`", names a real product to emulate, or pastes a URL/screenshot to match the *system* of (not a pixel-exact clone — that's `visual-to-code`, see Appendix H). Four steps, in order, before any code:

1. **Identify.** Resolve the name to a real URL — don't guess from a name alone, verify via search first. A misheard or approximate product name is common; confirm before building against the wrong reference.
2. **Source in full.** Navigate the live site and capture more than the hero: scroll+screenshot every section, pull the full text content (`get_page_text` or equivalent), and note concrete implementation details as found — exact color/gradient character, type treatment, spacing rhythm, motion/scroll patterns (pinned sections, numbered reveals, counters, hover states), recurring component patterns (badges, cards, chrome-framed media), and the page's section-by-section information architecture. This is extraction for pattern-matching per Section 4.8/9's honesty rules — never for reproducing another brand's actual logo, trademarked name, real customer names/logos, or verbatim copy; those get invented fresh for the new brand.
3. **Write the analysis before building.** A short structured breakdown, not a prose essay — five headers: Layout/IA, Color & type system, Motion/interaction patterns, Component inventory, Copy voice/structure. This is what turns "vibes from screenshots" into a buildable spec, and it doubles as this section's Design Read (0.B) for this specific case — state it explicitly rather than skipping straight to code.
4. **Plan, then build.** State what will differ (brand name/copy/data) vs. what will be matched (the system: layout, color language, motion, component patterns) before writing any code, then build via Sections 0-12's normal engine using the analysis as ground truth instead of an invented design read.

**Sibling relationship to Section 11:** Section 11's Redesign Protocol audits an *existing site you're changing*; this protocol audits *someone else's site you're emulating for a new build*. Both produce a structured analysis before code — keep the audit-checklist language consistent between the two rather than letting them drift into different formats.

---

## 1. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** - 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** - 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** - 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Use these unless the design read overrides them. Do not ask the user to edit this file - overrides happen conversationally.

### 1.A Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

### 1.C How the Dials Drive Output
Use these (or user-overridden values) as global variables. Cross-references throughout this document refer to these exact variable names - never invent aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

---

## 2. BRIEF → DESIGN SYSTEM MAP

Once you have the design read (Section 0) and dials (Section 1), pick the right foundation. Do not invent CSS for things that have an official package. Do not pretend an aesthetic trend is an official system.

### 2.A When to reach for a real design system (use official packages)
| Brief reads as… | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` web components / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` | Official Primer; Brand variant for marketing |
| Public-sector UK service | `govuk-frontend` | Legally / regulatorily expected |
| US public-sector / trust-first | `uswds` | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code, easy to customise; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie + small team builds |

**Honesty rule:** if the brief reads as one of the systems above, install and use the **official** package. Do not recreate its CSS by hand. Do not import a system's tokens but then override 90% of them.

**One system per project.** Do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app.

### 2.B When the brief is an aesthetic, not a system
For these directions, there is **no single official package**. Build with native CSS + Tailwind + a maintained component library. Be honest in code comments about what is borrowed inspiration vs. official material.

| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism / "frosted glass" | `backdrop-filter`, layered borders, highlight overlays. Provide solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No single library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial / magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech / hacker | Mono + accent neon, terminal motifs. No library. |
| Aurora / mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |
| **Apple Liquid Glass** | Apple documents this for Apple platforms only. **There is no official `liquid-glass.css`.** Web implementations are approximations using `backdrop-filter` + layered borders + highlights. Label clearly as approximation. |

---

## 3. DEFAULT ARCHITECTURE & CONVENTIONS

Unless the design read picks a real design system (Section 2.A), these are the defaults:

### 3.A Stack
* **Framework:** React or Next.js. Default to Server Components (RSC).
  * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
  * **INTERACTIVITY ISOLATION:** Any component using Motion, scroll listeners, or pointer physics MUST be an isolated leaf with `'use client'` at the top. Server Components render static layouts only.
* **Styling:** **Tailwind v4** (default). Tailwind v3 only if the existing project demands it.
  * For v4: do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **Animation:** **Motion** (the library formerly known as Framer Motion). Import from `motion/react` (`import { motion } from "motion/react"`). The `framer-motion` package still works as a legacy alias - prefer `motion/react` in new code.
* **Fonts:** Always use `next/font` (Next.js) or self-host with `@font-face` + `font-display: swap`. Never link Google Fonts via `<link>` in production.

### 3.B State
* Local `useState` / `useReducer` for isolated UI.
* Global state ONLY for deep prop-drilling avoidance - Zustand, Jotai, or React context.
* **NEVER** use `useState` to track continuous values driven by user input (mouse position, scroll progress, pointer physics, magnetic hover). Use Motion's `useMotionValue` / `useTransform` / `useScroll`. `useState` re-renders the React tree on every change and collapses on mobile.

### 3.C Icons
* **Allowed libraries (priority order):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Discouraged:** `lucide-react`. Acceptable only when the user explicitly asks for it or the project already depends on it.
* **NEVER hand-roll SVG icons.** If a glyph is missing, install a second library or compose from primitives - do not draw icon paths from scratch.
* **One family per project.** Do not mix Phosphor with Lucide in the same component tree.
* **Standardize `strokeWidth` globally** (e.g. `1.5` or `2.0`).

### 3.D Emoji Policy
Discouraged by default in code, markup, and visible text. Replace symbols with icon-library glyphs. **Override:** allow emojis only when the user explicitly asks for a playful / chat-style / social-native vibe - and even then use them sparingly with intent.

### 3.E Responsiveness & Layout Mechanics
* Standardize breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
* **Viewport Stability:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent layout jumping on mobile (iOS Safari address bar).
* **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Dependency Verification (mandatory)
Before importing ANY 3rd-party library, check `package.json`. If the package is missing, output the install command first. **Never** assume a library exists.

---

## 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

LLMs default to clichés. Override these defaults proactively. Each rule has a context-aware override path.

### 4.1 Typography
* **Display / Headlines:** Default `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body / Paragraphs:** Default `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans font choice:**
  * **Discouraged as default:** `Inter`. Pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, or a brand-appropriate serif first.
  * **Override:** Inter is acceptable when the user explicitly asks for a neutral / standard / Linear-style feel, or when the brief is a public-sector / accessibility-first site.
* **Pairings to know:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **SERIF DISCIPLINE (VERY DISCOURAGED AS DEFAULT):**
  * Serif is **very discouraged as the default font for any project.** "It feels creative / premium / editorial" is NOT a reason to reach for serif. The agent's default mental model that "creative brief = serif" is the single most-tested AI tell in production rounds.
  * **Serif is only acceptable when ONE of these is explicitly true:**
    - The brand brief literally names a serif font, OR
    - The aesthetic family is genuinely editorial / luxury / publication / manuscript / heritage / vintage AND you can articulate why this specific serif fits this specific brand
  * For everything else (creative agency, design studio, modern brand, premium consumer, portfolio, lifestyle), **default sans-serif display** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Sans display fonts are not "boring" — they are the default for the same reason black is the default in fashion.
  * **EMPHASIS RULE (related):** When you want to emphasize a word within a headline (the kinetic "and `spatial` design" type move), use **italic or bold of the SAME font**. Do NOT inject a random serif word into a sans headline (or vice versa) just to add visual interest. Mixed-family emphasis is amateur. Italic/bold emphasis in the same family is the right move.
  * **Specifically BANNED as defaults:** `Fraunces` and `Instrument_Serif` (the two LLM-favorite display serifs).
  * **If a serif is justified** (rare, per the above), rotate from this pool, do NOT reuse the same serif across consecutive projects: PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

* **ITALIC DESCENDER CLEARANCE (mandatory):** When italic is used in display type and the word contains a descender letter (`y g j p q`), `leading-[1]` or `leading-none` will clip the descender. Use `leading-[1.1]` minimum and add `pb-1` or `mb-1` reserve on the wrapping element. Audit every italic word in display headlines before shipping.

### 4.2 Color Calibration
* Max 1 accent color. Saturation < 80% by default.
* **THE LILA RULE:** The "AI Purple / Blue glow" aesthetic is discouraged as a default. No automatic purple button glows, no random neon gradients. Use neutral bases (Zinc / Slate / Stone) with high-contrast singular accents (Emerald, Electric Blue, Deep Rose, Burnt Orange, etc.).
* **Override:** if the brand or brief explicitly asks for purple / violet / lila, embrace it. But execute with intent: consistent palette, harmonised neutrals, restrained gradients. Not generic AI gradient slop.
* **One palette per project.** Do not fluctuate between warm and cool grays within the same project.
* **COLOR CONSISTENCY LOCK (mandatory):** Once an accent color is chosen for a page, it is used on the WHOLE page. A warm-grey site does not suddenly get a blue CTA in section 7. A rose-accented site does not get a teal status badge in the footer. Pick one accent, lock it, audit every component before shipping.

* **PREMIUM-CONSUMER PALETTE BAN (mandatory, second-most-recurring AI-tell):**
  * For premium-consumer briefs (cookware, wellness, artisan, luxury, heritage craft, DTC home goods, etc.) the LLM default is **warm beige/cream + brass/clay/oxblood/ochre + espresso/ink dark text**. Concretely banned hex families as default backgrounds and accents:
    - Backgrounds: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (all "warm paper / cream / chalk / bone")
    - Accents: `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (all "brass / clay / oxblood / ochre")
    - Text: `#1a1714`, `#1a1814`, `#1b1814` (all "espresso / warm near-black")
  * This palette is BANNED as the default reach for premium-consumer briefs. Every premium-consumer site you have ever shipped uses this exact palette. The brand becomes invisible.
  * **Default alternatives (rotate, do not reuse):**
    - **Cold Luxury:** silver-grey + chrome + smoke (think Tesla, Apple Watch Hermes-without-the-leather)
    - **Forest:** deep green + bone + amber accent (think Filson, Patagonia premium)
    - **Black and Tan:** true off-black + warm tan, sharp contrast, no beige
    - **Cobalt + Cream:** saturated blue against a single neutral, no brass
    - **Terracotta + Slate:** warm rust against cool grey, no brass
    - **Olive + Brick + Paper:** muted olive plus brick-red accent
    - **Pure monochrome + single saturated pop:** off-white + off-black + one bright accent (electric blue, emerald, hot pink, etc.)
  * **Palette-rotation rule:** if the previous premium-consumer project you generated used the beige+brass family, this one MUST use a different family. Do not ship the same warm-craft palette twice in a row.
  * **Override:** the beige+brass+espresso palette is acceptable ONLY when the brand brief explicitly names those colors, or when the brand identity is genuinely vintage / artisan / warm-craft AND you can articulate why this specific palette fits this specific brand. Default-reaching for it because "this is a cookware brief" is banned.

### 4.3 Layout Diversification
* **ANTI-CENTER BIAS:** Centered Hero / H1 sections are avoided when `DESIGN_VARIANCE > 4`. Force "Split Screen" (50/50), "Left-aligned content / right-aligned asset", "Asymmetric white-space", or scroll-pinned structures.
* **Override:** centered hero is OK for editorial / manifesto / launch-announcement briefs where the message itself is the design.

### 4.4 Materiality, Shadows, Cards
* Use cards ONLY when elevation communicates real hierarchy. Otherwise group with `border-t`, `divide-y`, or negative space.
* When a shadow is used, tint it to the background hue. No pure-black drop shadows on light backgrounds.
* For `VISUAL_DENSITY > 7`: generic card containers are banned. Data metrics breathe in plain layout.
* **SHAPE CONSISTENCY LOCK (mandatory):** Pick ONE corner-radius scale for the page and stick to it. Options: all-sharp (radius 0), all-soft (radius 12-16px), all-pill (full radius for interactive). Mixed systems are allowed only when there is a documented rule (e.g. "buttons are full-pill, cards are 16px, inputs are 8px") and that rule is followed everywhere. Round buttons in a square layout, or square cards on a pill-button page, is broken design.

### 4.5 Interactive UI States
LLMs default to "static successful state only." Always implement full cycles:
* **Loading:** Skeletal loaders matching the final layout's shape. Avoid generic circular spinners.
* **Empty States:** Beautifully composed; indicate how to populate.
* **Error States:** Clear, inline (forms), or contextual (toasts only for transient).
* **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]` to simulate a physical push.
* **BUTTON CONTRAST CHECK (mandatory, a11y):** Before shipping any button, verify the button text is readable against the button background. White button + white text, `bg-white` CTA with `text-white` label, transparent button against the page background with no border → all banned. Audit every CTA: contrast ratio WCAG AA min (4.5:1 for body, 3:1 for large text 18px+). Same rule applies to ghost buttons over photographic backgrounds (use a backdrop, scrim, or stroke).
* **CTA BUTTON WRAP BAN (mandatory):** Button text MUST fit on one line at desktop. If a label like "VIEW SELECTED WORK" wraps to 2 or 3 lines, the button is broken. Fix by EITHER shortening the label (3 words max for primary CTAs, ideally 1-2) OR widening the button (do not artificially constrain `max-width` on CTAs). Wrapped CTAs at desktop are a Pre-Flight Fail.
* **NO DUPLICATE CTA INTENT (mandatory):** Two CTAs with the same intent on one page is a Pre-Flight Fail. Examples of same intent: "Get in touch" + "Contact us" + "Let's talk" + "Start a project" + "Start something" + "Reach out" = all "contact" intent → pick ONE label and use it everywhere on the page (nav, hero, footer). Same for "Try free" + "Get started" + "Sign up free" (all "signup" intent) and "View work" + "See selected work" + "Browse projects" (all "portfolio" intent). One label per intent.
* **FORM CONTRAST CHECK (mandatory, a11y):** Form inputs, placeholder text, focus rings, helper text, and error text all pass WCAG AA contrast against the section background. Light placeholders on a near-white form, white form on white page section, form labels grayer than 4.5:1 contrast → all banned. Audit every form before shipping.

### 4.6 Data & Form Patterns
* Label ABOVE input. Helper text optional but present in markup. Error text BELOW input. Standard `gap-2` for input blocks.
* No placeholder-as-label. Ever.

### 4.7 Layout Discipline (Hard Rules. Failing any of these is shipping broken work)

* **Hero MUST fit in the initial viewport.** Headline max 2 lines on desktop, subtext max **20 words** AND max 3-4 lines, CTAs visible without scroll. If the copy is too long: reduce font scale OR cut copy. If you cannot describe the value-prop in 20 words of subtext, the value-prop is unclear, not the rule too tight. Never let the hero overflow and force scroll to find the CTA.
* **Hero font-scale discipline.** Plan font size and image size *together*. If the hero asset is large and the headline is more than 6 words, do not start at `text-7xl/text-8xl`. Default sensible range: `text-4xl md:text-5xl lg:text-6xl` for most heroes; `text-6xl md:text-7xl` only when the headline is 3-5 words. A 4-line hero headline is always a font-size error, never a copy-length error.
* **HERO TOP PADDING CAP (mandatory):** Hero top padding max `pt-24` (≈6rem) at desktop. More than that means the hero content floats halfway down the viewport and reads as a layout bug, not as intentional space. If your hero needs more breathing room, increase font scale or asset size, not top padding.
* **HERO STACK DISCIPLINE (max 4 text elements).** The hero is a single moment, not a feature list. Allowed text elements, max 4 in total:
  1. Eyebrow (small uppercase label) OR brand strip OR neither - pick zero or one
  2. Headline (max 2 lines, see above)
  3. Subtext (max 20 words, max 4 lines)
  4. CTAs (1 primary + max 1 secondary)
  - **BANNED in the hero:** tiny tagline below CTAs ("Works with GitHub, GitLab, and self-hosted Git"), trust micro-strip ("Used by engineering teams at..."), pricing teaser ("Free for solo, $10/user for teams"), feature bullet list, social-proof avatar row. All of those move to dedicated sections directly below the hero.
  - If you have an eyebrow AND a tagline below CTAs in the same hero, drop the tagline. If you have a brand strip AND a tagline, drop the tagline. One small text element per hero, max.
* **"Used by" / "Trusted by" logo wall belongs UNDER the hero, never inside it.** The hero is for the value prop and primary CTA. The logo wall is a separate section directly below. Do not stuff trust logos into the same flex row as the hero copy.
* **Navigation MUST render on a single line on desktop.** If items don't fit at `lg` (1024px), condense labels, drop secondary items, or move to a hamburger. A two-line nav at desktop is broken design.
* **Navigation height cap: 80px max desktop, default 64-72px.** No huge "agency" nav bars that eat 15% of the viewport.
* **Bento grids MUST have rhythm, not one-sided repetition.** Do not stack 6 left-image / right-text rows. Vary the composition: alternate full-width feature rows, asymmetric tile sizes, vertical breaks.
* **BENTO CELL COUNT RULE (mandatory):** A bento grid has EXACTLY as many cells as you have content for. 3 items → 3 cells (1+2 split, or 2+1, or asymmetric trio). 5 items → 5 cells (2+3, 3+2, hero+4, etc.). If your grid has an empty cell in the middle or at the end, you planned wrong. Re-shape the grid; do not paste a blank tile.
* **Section-Layout-Repetition Ban.** Once you use a layout family for a section (e.g., 3-column-image-cards, full-width-quote, split-text-image), that family can appear at most ONCE on the page. "Selected commissions" must not look like "What we do." A landing page with 8 sections must use at least 4 different layout families.
* **ZIGZAG ALTERNATION CAP (mandatory).** Alternating "left-image + right-text" then "left-text + right-image" zigzag layout = banal. Max 2 sections in a row with this image+text-split pattern. The 3rd consecutive image+text split is a Pre-Flight Fail. Break the pattern with a full-width section, a vertical-stack section, a bento grid, a marquee, or a different layout family.
* **EYEBROW RESTRAINT (mandatory, the #1 violated rule in production tests).** An "eyebrow" is the small uppercase wide-tracking label sitting above a section headline (e.g. `FOUR COLORWAYS`, `SELECTED WORK`, `THE HARDWARE`, `Git-native task management`). Typical CSS signature: `text-[11px] uppercase tracking-[0.18em]`, `font-mono text-[10.5px] uppercase tracking-[0.22em]`. Every AI-built site puts an eyebrow above EVERY section header, producing the same templated rhythm. Hard rule:
  - **Maximum 1 eyebrow per 3 sections.** Hero counts as 1. So a page with 9 sections may use at most 3 eyebrows total.
  - If section A has an eyebrow, the next 2 sections cannot have one.
  - **Pre-Flight Check is mechanical:** count instances of `uppercase tracking` (or similar small-caps mono labels above headlines) across all section components. If count > ceil(sectionCount / 3), the output fails.
  - **What to do instead of an eyebrow:** drop it entirely. The headline alone is enough. If you need to categorize a section, the section's location on the page already categorizes it; no label needed.
* **SPLIT-HEADER BAN (mandatory).** The pattern "left big headline + right small explainer paragraph" as a section header (left col-span-7/8, right col-span-4/5 with a small body paragraph floating in the right column) is **banned as default**. Sections should have ONE focused message. If you genuinely need both a headline and an explainer paragraph, stack them vertically (headline on top, body below, max-width 65ch). Reach for the split-header pattern only when there is a real compositional reason (e.g., the right column carries a visual or interactive element, not just filler text).
* **Bento Background Diversity (mandatory).** Bento and feature-grid sections cannot be 6 white-on-white cards with text inside. At least 2-3 cells in any multi-cell grid need real visual variation: a real image, a brand-appropriate gradient (not AI-purple), a pattern, a tinted background. A cream-on-cream bento with only typography inside reads as boring AI default, even when the rest of the page is good.
* **Mobile collapse must be explicit per section.** For every multi-column layout, declare the `< 768px` fallback in the same component. No "it'll work, Tailwind handles it" assumptions.

### 4.8 Image & Visual Asset Strategy

Landing pages and portfolios are **visual products**. Text-only pages with fake-screenshot divs are slop.

**Priority order for visual assets:**
1. **Image-generation tool first.** If ANY image-gen tool is available in the environment (`generate_image`, MCP image tool, IDE-integrated gen, OpenAI image tools, etc.) you MUST use it to create section-specific assets: hero photography, product shots, texture backgrounds, mood images. Generate at the right aspect ratio for the section. Do not skip this step because hand-rolled CSS feels faster.
2. **Real web images second.** When no gen tool is available, use real photography sources. Acceptable defaults:
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` for placeholder photography (seed should describe the section, e.g. `marrow-cookware-kitchen`)
   * Actual stock or brand URLs when the brief provides them
   * Open-license sources (Unsplash via direct URL, Pexels) if explicitly allowed
3. **Last resort: tell the user.** If neither is possible, do NOT fill the page with hand-rolled SVG illustrations or div-based "fake screenshots." Instead, leave clearly-labeled placeholder slots (`<!-- TODO: hero product photo, 1600x1200 -->`) and at the end of the response say: *"This page needs real images at: \[list of placements\]. Please generate or provide them."*

**Even minimalist sites need real images.** A pure-text page is not minimalism. It is incomplete work. Even an editorial Linear-style site needs at least 2-3 real images (hero, one product/lifestyle shot, one supporting image). Generate B&W minimalist photography if the brief is restrained; do not skip images entirely because the dial is low.

**Real company logos for social proof.** When the brief calls for a "Trusted by / Used by / Customers" logo wall, do NOT default to plain text wordmarks (`<span>Acme Co</span>` styled in a row). Use real SVG logos:
* **Source: Simple Icons** (`https://cdn.simpleicons.org/{slug}/ffffff` for any color, or `simple-icons` npm package). Covers most known brands.
* **Alternative: devicon** for tech-stack logos (`@svgr/cli` or CDN).
* **Make-up the brand name? Then make-up an SVG mark too.** Generate a simple monogram (one letter in a circle, two-letter ligature, abstract glyph) rendered as an inline `<svg>` matching the page style. Plain text wordmarks for invented brand names look generic.
* **Always** ensure logos render in both light and dark mode (white-on-dark, black-on-light, or single-color theme variable).
* **LOGO-ONLY rule (mandatory):** logo wall = logos and nothing else. Do NOT print industry / category labels below each logo (no `Vercel` + `hosting` underneath, no `Stripe` + `payments`, no `Cloudflare` + `infra`). The logo is the credibility, the label adds nothing the user does not already know. Optional: brand name as alt-text for screen readers, optional link to the brand's site. That is it.

**Hand-rolled illustrations:**
* SVG icons from libraries: fine (see Section 3.C).
* Hand-rolled decorative SVGs (custom illustrations, logos, marks): **strongly discouraged**, never as default. Acceptable only when:
  - The brief explicitly calls for it ("draw me an SVG logo")
  - It's a single, simple geometric mark (a square, a circle, a wordmark in display type)
  - You're confident in the output quality

**Div-based fake screenshots are banned.** A "hand-built product preview" rendered with `<div>` rectangles, fake task lists, fake dashboards, fake terminal windows is a Tell. If you need to show a product:
* Use a real screenshot URL if one exists
* Generate one via image tool
* Use a real component preview (an actual mini-version of the UI inside the page)
* Or skip the preview entirely and use editorial photography

**Hero needs a real visual.** Text + gradient blob is not a hero - it's a placeholder.

### 4.9 Content Density

Landing pages live on the **first impression**, not the full read. Cut ruthlessly.

* **Default content shape per section:** short headline (≤ 8 words) + short sub-paragraph (≤ 25 words) + one visual asset OR one CTA. Anything more must be justified by the section's job.
* **No data-dump sections.** A 20-row publication table, a 30-row award list, a giant pricing matrix on a marketing page = wrong layout. Use:
  - Top 3-5 highlights + "View full list" link
  - Marquee / carousel for breadth
  - Different page entirely if the data is the product
* **Long lists need a different UI component, not a longer list.** Default `<ul>` with bullets / `divide-y` rows is the lazy choice. If you have > 5 items, reach for one of these instead:
  - 2-column split with grouped items
  - Card grid with image + label per item
  - Tabs / accordion if items are categorisable
  - Horizontal scroll-snap pills
  - Carousel for breadth-heavy lists (testimonials, logos, capabilities)
  - Marquee for "lots-of-things-that-don't-need-individual-attention"
  A spec sheet with 10 rows + a hairline under every row is the WORST default. Either group rows into 2-3 chunks with sparse dividers, or move to a card-per-spec layout.
* **Spec sheets specifically (the Marrow-cookware pattern).** A long product specification table with `border-b` on every row is the AI default for cookware / hardware / apparel / artisan-goods briefs. Banned. Concrete alternatives:
  - **2-col card grid:** each spec gets its own card with the spec name, the value (large display number), and a one-line "why it matters" body. Cards arranged 2-col on desktop, 1-col mobile.
  - **Scroll-snap horizontal pills:** each spec is a pill, user can flick through.
  - **Grouped chunks:** group 10 specs into 3 logical clusters (e.g. "Materials", "Cooking", "Warranty"), each cluster gets ONE soft divider and a cluster heading.
  - **Featured-vs-rest:** 3-4 hero specs visualised as large display tiles, the rest collapsed under a "View full specifications" disclosure.

* **COPY SELF-AUDIT (mandatory before ship):** Before declaring any task done, re-read every visible string on the page (headlines, subheads, eyebrows, button labels, body copy, captions, alt text, footer text, error messages). Flag any string that is:
  - **Grammatically broken** ("free on its past", "two plans but one is honest", "to put it on the table" out of context)
  - **Has unclear referents** ("we plan to stay that way" without prior context)
  - **Sounds like AI hallucination** (cute-but-wrong wordplay, forced metaphors that don't track, "elegant nothing" phrases)
  - **Reads like an LLM trying to sound thoughtful** (passive-aggressive humility, fake-craftsman labels, mock-poetic micro-meta)
  Rewrite every flagged string. If unsure whether a string makes sense, replace it with a plain functional sentence. AI-generated cute copy is worse than boring copy.
* **Fake-precise numbers are flagged.** Numbers like `92%`, `4.1×`, `48k`, `5.8 mm`, `13.4 lb` either:
  - Come from real data (brief, brand guidelines, public metrics) - fine
  - Are explicitly labeled as mock (`<!-- mock -->`, "example", "sample data") - fine
  - Are AI-invented spec aesthetics - banned. Don't fake engineering precision the brand doesn't claim.
* **One copy register per page.** Don't mix technical mono ("47 tasks · 0.6 ctx-switches/day"), editorial prose, and marketing punch in the same composition unless the brand voice explicitly calls for it.

### 4.10 Quotes & Testimonials

* **Max 3 lines** of quote body. Never 6. If the original quote is longer → cut it. A landing-page quote is a snippet, not the full review.
* For very small font sizes (e.g. footer-style testimonials), the line cap can stretch slightly. Spirit: "fits in a glance."
* **No em-dashes inside the quote text** as design flourish (long pauses, kinetic em-dashes, em-dash-bullets). See Section 9.G - em-dash is completely banned.
* Attribution: name + role + (optionally) company. Never name only ("- Sarah").
* Quote marks: use real typographic quotes ( " " ) or none at all. Not straight ASCII ( " ).

### 4.11 Page Theme Lock (Light / Dark Mode Consistency)

The page has ONE theme. Sections do not invert.

* If the page is dark mode, ALL sections are dark mode. No light-mode-warm-paper section sandwiched between dark sections (or vice versa). The user must not feel they walked into a different website mid-scroll.
* The exception: if the brief explicitly calls for a "Color Block Story" or "Theme Switch on Scroll" device AND that is a deliberate composition (one full theme switch with a strong transition, not random alternation), it is allowed once per page.
* Default behaviour: pick light, dark, or auto (`prefers-color-scheme`) at the page level and lock it. Section-level background tints within the same theme family are fine (`bg-zinc-950` next to `bg-zinc-900`); flipping to `bg-amber-50` in the middle of a `bg-zinc-950` page is broken.
* When using a design system with built-in theming (Radix Themes, shadcn/ui with `<Theme>`), set the theme ONCE in `layout.tsx` or the page root. Do not let individual sections override.

---

## 5. CONTEXT-AWARE PROACTIVITY

These are tools, not defaults. Use them when the design read calls for them. **None of these fire automatically.**

**Named aesthetic presets:** when the brief calls for a fully committed, single-aesthetic direction
rather than the general dial-driven system below, two standalone sibling skills exist and should be
invoked directly instead of approximated here: `brutalist-skill` (Swiss/military industrial,
rigid grids, analog degradation — dashboards, portfolios, editorial "declassified blueprint" feel)
and `minimalist-skill` (warm monochrome editorial minimalism). Reach for one of those when the brief
explicitly wants that committed look; otherwise use this skill's dial system.

* **Liquid Glass / Glassmorphism:** Appropriate for premium consumer, Apple-adjacent, luxury brand, or media-overlay vibes. Inappropriate for dashboards, public-sector, or "boring B2B." When used, go beyond `backdrop-blur`: add a 1px inner border (`border-white/10`) and a subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) for physical edge refraction. Provide a solid-fill fallback under `prefers-reduced-transparency`.
* **Magnetic Micro-physics:** Use when `MOTION_INTENSITY > 5` AND the brief reads premium / playful / agency. Implement EXCLUSIVELY with Motion's `useMotionValue` / `useTransform` outside the React render cycle. Never `useState`. See Section 3.B.
* **Perpetual Micro-Interactions** (Pulse, Typewriter, Float, Shimmer, Carousel): Use when `MOTION_INTENSITY > 5` AND the section actively benefits from motion (status indicators, live feeds, AI-feel). **Not every card needs an infinite loop.** If a section is informational, leave it still. Apply Spring Physics (`type: "spring", stiffness: 100, damping: 20`) - no linear easing.
* **"Motion claimed, motion shown."** If `MOTION_INTENSITY > 4`, the page must actually move: entry transitions on hero, scroll-reveal on key sections, hover physics on CTAs, at minimum. A static page that claims `MOTION_INTENSITY: 7` is broken. Conversely, if you cannot ship working motion in the available scope, drop the dial to 3 and ship a clean static page. Never half-build motion that breaks (cut-off ScrollTriggers, jumpy enters, missing cleanups).
* **MOTION MUST BE MOTIVATED (mandatory).** Before adding any animation, ask: "what does this animation communicate?" Valid answers: hierarchy (drawing attention to the right thing), storytelling (revealing content in sequence that matches a narrative), feedback (acknowledging a user action), state transition (showing something changed). Invalid answer: "it looked cool". GSAP everywhere because GSAP is available is amateur. Each ScrollTrigger, each marquee, each pinned section needs a reason. If you cannot articulate the reason in one sentence, drop the animation.
* **MARQUEE MAX-ONE-PER-PAGE (mandatory).** Horizontal scrolling text marquees ("logos endlessly scrolling", "manifesto scrolling sideways", "kinetic word strip") are appropriate at most ONCE per page. Two or more marquees on the same page reads as lazy filler. Pick the one section where the marquee actually serves the content; the others get a different layout.
* **GSAP Sticky-Stack Pattern (when scroll-stack is used).** A "card stack on scroll" must be a REAL sticky-stack, not a sequential reveal list. See Section 5.A below for the canonical code skeleton. Common failure: trigger fires halfway through scroll instead of pinning at viewport top. Fix: `start: "top top"` not `start: "top center"` or `"top 80%"`.
* **GSAP Horizontal-Pan Pattern (when horizontal scroll-hijack is used).** See Section 5.B below for the canonical skeleton. Common failure: animation starts before the section is pinned, so the user sees half a slide. Same fix: `start: "top top"`, pin the wrapper, scrub the inner track.

### 5.A Sticky-Stack - Canonical Skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, every card except the last is pinned, the scale/opacity transform is driven by the NEXT card's scroll trigger (so previous card shrinks as next one arrives).

### 5.B Horizontal-Pan - Canonical Skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, `end: "+=${distance}"` (scroll length = horizontal travel needed), `scrub: 1`. The wrapper is pinned, the inner track slides horizontally as the user scrolls vertically.

### 5.C Scroll-Reveal Stagger - Canonical Skeleton (lighter alternative)

For simple "items appear as they enter viewport" (no pinning), prefer Motion's `whileInView` over GSAP - lighter, no ScrollTrigger needed:

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

Use this for: feature lists, testimonial grids, logo walls, anything that just needs "enter on scroll." Save GSAP for actual pin/scrub work.

### 5.D Forbidden Animation Patterns

* **`window.addEventListener("scroll", ...)`** is banned. It runs on every scroll frame, jank-prone, no batching. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Custom scroll progress calculations using `window.scrollY`** in React state. Same reason. Re-renders on every frame.
* **`requestAnimationFrame` loops that touch React state.** Use motion values (`useMotionValue` + `useTransform`) instead.
* **Layout Transitions:** Use Motion's `layout` and `layoutId` props for visible state changes (re-ordering lists, expanding modals, shared elements between routes). Do not wrap static content in `layout` props "for safety" - it costs measurement work.
* **Staggered Orchestration:** Use `staggerChildren` (Motion) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for reveal moments where sequence matters. For `staggerChildren`, parent (`variants`) and children MUST share the same Client Component tree.

---

## 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### 6.A Hardware Acceleration
* Animate ONLY `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`.
* Use `will-change: transform` sparingly - only on elements that will actually animate.

### 6.B Reduced Motion (mandatory)
* **Any motion above `MOTION_INTENSITY > 3` MUST honor `prefers-reduced-motion`.** This is non-negotiable.
* In Motion: wrap with `useReducedMotion()` and degrade to static.
* In CSS: gate animations behind `@media (prefers-reduced-motion: no-preference)` or provide an override block under `@media (prefers-reduced-motion: reduce)` that disables.
* Infinite loops, parallax, scroll-hijack, and magnetic physics MUST collapse to static / instant under reduced motion.

### 6.C Dark Mode (mandatory for any consumer-facing page)
* Design for **both modes from the start**. Never ship light-only or dark-only without explicit user instruction.
* Use Tailwind `dark:` variant OR CSS variables for tokens. Pick one strategy per project.
* **Do not prescribe specific dark-mode colors here.** The brief decides. Maintain visual hierarchy, brand identity, and WCAG AA contrast (AAA for body) across both modes.
* Respect `prefers-color-scheme: dark`. Default to system preference unless the brand insists on one mode.

### 6.D Core Web Vitals Targets
* **LCP** < 2.5s. Hero image must be `next/image priority` or preloaded.
* **INP** < 200ms. Heavy work off main thread.
* **CLS** < 0.1. Reserve space for images, fonts, embeds.
* Run Lighthouse before declaring a page done.

### 6.E DOM Cost
* Apply grain / noise filters EXCLUSIVELY to fixed, `pointer-events-none` pseudo-elements (e.g., `fixed inset-0 z-[60] pointer-events-none`). NEVER on scrolling containers - continuous GPU repaints destroy mobile FPS.
* Be aware of bundle size. Motion is not tiny. Three.js is large. Lazy-load anything that's not above-the-fold.

### 6.F Z-Index Restraint
NEVER spam arbitrary `z-50` or `z-10`. Use z-index strictly for systemic layer contexts (sticky navbars, modals, overlays, grain). Document the z-index scale in a project constants file.

---

## 7. DIAL DEFINITIONS (Technical Reference)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Symmetrical CSS Grid (12-col, equal fr-units), equal paddings, centered alignment.
* **4-7 (Offset):** `margin-top: -2rem` overlaps, varied image aspect ratios (4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`).
* **MOBILE OVERRIDE:** For levels 4-10, asymmetric layouts above `md:` MUST collapse to strict single-column (`w-full`, `px-4`, `py-8`) on viewports `< 768px`.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover` and `:active` states only. `prefers-reduced-motion` is the default mode anyway.
* **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. Focus on `transform` and `opacity`.
* **8-10 (Advanced Choreography):** Complex scroll-triggered reveals, parallax, scroll-driven animation (CSS `animation-timeline` or GSAP ScrollTrigger). Use Motion hooks. **NEVER use `window.addEventListener('scroll')`** - it is a hard ban, not a "prefer-not." See Section 5.D for the allowed alternatives.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery):** Lots of white space. Huge section gaps (`py-32` to `py-48`). Expensive, clean.
* **4-7 (Daily App):** Standard web app spacing (`py-16` to `py-24`).
* **8-10 (Cockpit):** Tight paddings. No card boxes; 1px lines separate data. Mandatory: `font-mono` for all numbers.

---

## 8. DARK MODE PROTOCOL

Dual-mode by default. Never assume light-only unless the brief is print-emulating editorial.

### 8.A Token Strategy (pick one, stick to it)
* **Tailwind `dark:` variant** (default for utility-first projects): every color utility paired with its dark variant (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **CSS variables** (for shadcn/ui, Radix Themes, or component libraries with theming): define semantic tokens (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) and swap values under `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.

### 8.B Do Not Prescribe Specific Colors Here
The brief and brand decide. This skill enforces only:
* **Contrast** - WCAG AA minimum for body text, AAA target for hero copy.
* **Hierarchy parity** - visual hierarchy that works in light must work in dark. If a CTA pops in light, it pops in dark.
* **Brand fidelity** - primary brand color stays recognisable. Don't desaturate the brand into a dark mode.
* **No pure `#000000` and no pure `#ffffff`** - use off-black (zinc-950, near-black warm gray) and off-white. Pure values kill depth.

### 8.C Default Mode
Respect `prefers-color-scheme` unless the brand insists. Add a manual toggle if either mode would lose key brand expression.

### 8.D Test in Both Modes Before Finishing
Open the page in both modes during development. Do not ship a page you've only seen in one mode.

---

## 9. AI TELLS (Forbidden Patterns)

Avoid these signatures unless the brief explicitly asks for them.

### 9.A Visual & CSS
* **NO neon / outer glows** by default. Use inner borders or subtle tinted shadows.
* **NO pure black (`#000000`).** Off-black, zinc-950, or charcoal.
* **NO oversaturated accents.** Desaturate to blend with neutrals.
* **NO excessive gradient text** for large headers.
* **NO custom mouse cursors.** Outdated, accessibility-hostile, perf-hostile.

### 9.B Typography
* **AVOID Inter as default.** See Section 4.1. Override path exists.
* **NO oversized H1s** that just scream. Control hierarchy with weight + color, not raw scale.
* **Serif constraints:** Serif for editorial / luxury / publication. Not for dashboards.

### 9.C Layout & Spacing
* **Mathematically perfect** padding and margins. No floating elements with awkward gaps.
* **NO 3-column equal feature cards.** The generic "three identical cards horizontally" feature row is banned. Use 2-column zig-zag, asymmetric grid, scroll-pinned, or horizontal-scroll alternative.

### 9.D Content & Data ("Jane Doe" Effect)
* **NO generic names.** "John Doe", "Sarah Chan", "Jack Su" → use creative, realistic, locale-appropriate names.
* **NO generic avatars.** No SVG "egg" or Lucide user icons → use believable photo placeholders or specific styling.
* **NO fake-perfect numbers.** Avoid `99.99%`, `50%`, `1234567`. Use organic, messy data (`47.2%`, `+1 (312) 847-1928`).
* **NO startup-slop brand names.** "Acme", "Nexus", "SmartFlow", "Cloudly" → invent contextual, premium names that sound real.
* **NO filler verbs.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" → concrete verbs only.

### 9.E External Resources & Components
* **NO hand-rolled SVG icons.** Use Phosphor / HugeIcons / Radix / Tabler. Lucide on explicit request only.
* **Hand-rolled decorative SVGs strongly discouraged** as default (see Section 4.8).
* **NO div-based fake screenshots.** Never build a fake product UI out of `<div>` rectangles to simulate a screenshot. Use real images, generated images, or skip the preview.
* **NO broken Unsplash links.** Use `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, or generated photo placeholders, or actual assets.
* **shadcn/ui customization:** Allowed, but NEVER in default state. Customize radii, colors, shadows, typography to the project aesthetic.
* **Production-Ready Cleanliness:** Code visually clean, memorable, meticulously refined.

### 9.F Production-Test Tells (banned outright)

These patterns came out of real LLM-generated landing-page tests. They are the signatures the model defaults to when it tries to "look designed." Treat them as hard bans unless the brief explicitly calls for one.

**Hero & top-of-page**
* **NO version labels in the hero.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` - banned as default eyebrows. Only acceptable when the brief is explicitly about a product launch / preview status.
* **NO "Brand · No. 01"-style sub-eyebrows.** "Marrow · No. 01 · The 6-quart" type micro-meta lines. Skip them.

**Section numbering & micro-labels**
* **NO section-number eyebrows.** `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`, `06 · how it works`, `05 · The honest table` - banned. Eyebrows should name the topic in plain language, not enumerate.
* **NO `01 / 4`-style pagination on images or bento tiles.** If the user can count, they don't need the label.
* **NO `Scroll · 001 Capabilities`-style scroll cues.** A simple arrow or "Scroll" is enough; no section-number prefix.
* **NO "Index of Work, 2018 - 2026"-style range labels** as eyebrows. Just say what the section is.

**Separators & dots**
* **The middle-dot (`·`) is rationed.** Maximum 1 per line in metadata strips. Do NOT use it as the default separator for everything ("foo · bar · baz · qux · quux"). If you need a separator family, prefer line breaks, hairlines, or columns.
* **NO decorative colored status dots on every list/nav/badge.** A colored dot before "ONE Q4 SLOT OPEN" or before every nav link, or every task row - banned by default. Acceptable only when the dot conveys actual semantic state (a server status, an availability flag) and is used sparingly.

**Em-dashes & typography flourishes**
* **NO em-dash (`—`) as a design element OR anywhere else.** See Section 9.G below for the complete, non-negotiable ban. The em-dash character is forbidden in headlines, eyebrows, pills, body copy, quotes, attribution, captions, button text, and alt text. Use the regular hyphen (`-`).
* **NO `<br>`-broken-and-italicized headlines** as a default "design move." "for thirty\<br\>*years.*" type splits. Headlines should read naturally first, get clever only when the brief demands it.
* **NO vertical rotated text** ("INDEX OF WORK, 2018 - 2026" rotated 90°). Agency-portfolio cliché. Use it only when the brief is explicitly agency / Awwwards / experimental AND it serves a real composition purpose.
* **NO crosshair / hairline grid lines as decoration.** Vertical and horizontal lines drawn just to make the page "feel designed" - banned. Use them only when they organize real content.

**Fake product previews**
* **NO div-based fake product UI in the hero** (fake task list, fake terminal, fake dashboard built from styled divs). It is the #1 LLM-design Tell. Use a real screenshot, a generated image, a real component preview, or none at all.
* **NO fake version footers** ("v0.6.2-rc.1", "last sync 4s ago · main") inside fake screenshots. Adds nothing, screams AI.

**Marketing-copy Tells**
* **NO "Quietly in use at" / "Quietly trusted by"** social-proof headers. Use natural language: "Trusted by", "Used at", "Customers include", or skip the heading entirely if the logos speak.
* **NO "From the field" / "Field notes" / "Currently on the bench" / "On our desks" / "Loose plates" style poetic labels** on quote, blog, or sidebar sections. Reads as performative-craftsman. Use plain functional labels ("Testimonials", "Latest writing", "Now working on") or skip the label.
* **NO "We respect the French ones"-style** mock-humble industry-references in body copy. Cute and AI-y.
* **NO weather / locale strips** ("LIS 14:23 · 18°C") in headers/footers unless the brief is explicitly about a place / time-zone-distributed studio.
* **NO micro-meta-sentences under eyebrows.** Sentences like *"Each of these is a feature we ship today, not a roadmap promise. The list will stay short on purpose."* sitting under a section heading are clutter. Eyebrow + Headline + Body is enough.
* **NO generic step labels.** "Stage 1 / Stage 2 / Stage 3", "Step 1 / Step 2 / Step 3", "Phase 01 / Phase 02 / Phase 03", "Pass One / Pass Two / Pass Three". Banned. The actual step content is the label. If you must show progression, use the verb-noun directly ("Install", "Configure", "Ship") not "Stage 1: Install".

**Pills, labels and version stamps**
* **NO pills/labels/tags overlaid on images.** No `<span>` overlays on photos with tags like `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`. Either let the image speak alone, or add a caption directly below (outside the image).
* **NO photo-credit captions as decoration.** Strings like `Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` under stock/picsum images are pretentious. Photo credit is allowed ONLY when there is a real photographer being credited for a real photo (with permission). Otherwise: skip the caption or use a one-line functional caption ("The 6-quart, in Sage.").
* **NO version footers on marketing pages.** Footer strings like `v1.4.2`, `Build 0048`, `last sync 4s ago · main` are CLI / devtool fixtures, not landing-page content. Banned on marketing/landing/portfolio pages.
* **NO "Reservation 412 of 800"-style live-stock counters** as decoration. Only if the brief is explicitly a limited-run waitlist with real data.

**Decoration text strips**
* **NO decoration text strip at hero bottom.** Patterns like `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` as a small mono-caps strip across the bottom of the hero are an agency-portfolio cliché. Banned by default. Only acceptable when the strip carries real, navigable links (sticky bottom nav) or real status info (cookie banner, build info on a docs site).
* **NO floating top-right sub-text in section headings.** Pattern: section has a giant left-aligned headline; in the top-right corner of the same section header there is a small explainer paragraph floating with no clear alignment to anything else. That floater is the Tell. Either put the sub-text directly under the headline, or build a clean 2-column header (left: headline, right: aligned body), but not a tiny corner paragraph.

**Lists, dividers and scoring**
* **NO `border-t` + `border-b` on every row of a long list / spec table.** Pick one (bottom-border between rows OR top-border above the group) and use it sparsely. A 10-row spec table with hairlines under each row is the laziest layout - see Section 4.9 for alternative UI components.
* **NO scoring/progress bars with filled background tracks** as comparison visuals. If you need to show "X out of Y" comparisons, prefer a number + small icon, or a tiny inline bar WITHOUT a background track. Big filled `bg-zinc-200` tracks with a partial fill on top are dashboard-UI clutter on a landing page.

**Locale, time, scroll cues**
* **Locale / city-name / time / weather strips are banned for 99% of briefs.** "Lisbon, working with founders" in the hero, "1200-690 Lisbon, Portugal" in the footer, "Lisbon 14:23 · 18°C" in the nav. These are agency-portfolio decoration tells. Allowed ONLY when: the brief explicitly describes a globally-distributed studio with timezone-relevant work, OR a travel-focused brand, OR a real-world physical venue. A single contact-address mention in the footer is fine; an atmospheric locale strip is not.
* **Scroll cues are banned.** `Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, animated mouse-wheel icons. If the user has not scrolled yet, they are looking at the hero. They know what scroll is. The bottom of the viewport does not need a label.
* **ZERO decorative status dots by default.** A coloured dot before nav items, before list rows, before badges, before status labels is a Tell. Only acceptable when conveying real semantic state (a live indicator on actual server status, a live availability flag) and limited to one per page section.

### 9.G EM-DASH BAN (the single most-violated Tell)

**Em-dash (`—`) is COMPLETELY banned.** It is the LLM's signature stylistic crutch and it is the #1 visual Tell in production tests. There is no "limited use" allowance, no "natural language frequency" allowance, no "in body copy is fine" allowance. None.

* **Banned in headlines.** Use a period or a comma.
* **Banned in eyebrows / labels / pills / button text / image captions / nav items.** Replace with line breaks, columns, or hairlines.
* **Banned in body copy.** Restructure the sentence: two sentences with a period, OR a comma, OR parentheses, OR a colon.
* **Banned in quote attribution.** Use a normal hyphen with spaces (` - `) or a line break + smaller-weight name.
* **Banned in en-dash form too (`–`) when used as a separator.** Date ranges (`2018-2026`) use a hyphen. Number ranges (`€40-80k`) use a hyphen.

The ONLY permitted dash characters on the page are:
* Regular hyphen `-` (for compound words, ranges, line dividers in markup)
* Minus sign in math (`-5°C`)

If your output contains a single `—` or `–` anywhere visible to the user, the output fails the Pre-Flight Check and must be rewritten.

This rule is non-negotiable. The agent has historically ignored em-dash limits when phrased as "use sparingly." The phrasing here is binary: zero em-dashes.

---

## 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)

This is a vocabulary, not a library. The agent should KNOW these pattern names to communicate about them, design with them in mind, and reach for them when the design read calls for them. **Implementations and code sketches live in the Block Library (Section 12), which is populated iteratively.**

### Hero Paradigms
* **Asymmetric Split Hero** - Text on one side, asset on the other, generous white space.
* **Editorial Manifesto Hero** - Large type, no asset, almost-poster.
* **Video / Media Mask Hero** - Type cut out as mask over video background.
* **Kinetic-Type Hero** - Animated typography as the primary visual.
* **Curtain-Reveal Hero** - Hero parts on scroll like a curtain.
* **Scroll-Pinned Hero** - Hero stays pinned while content scrolls behind.

### Navigation & Menus
* **Mac OS Dock Magnification** - Edge nav, icons scale fluidly on hover.
* **Magnetic Button** - Pulls toward cursor.
* **Gooey Menu** - Sub-items detach like viscous liquid.
* **Dynamic Island** - Morphing pill for status / alerts.
* **Contextual Radial Menu** - Circular menu expanding at click point.
* **Floating Speed Dial** - FAB springing into curved secondary actions.
* **Mega Menu Reveal** - Full-screen dropdown, stagger-fade content.

### Layout & Grids
* **Bento Grid** - Asymmetric tile grouping (Apple Control Center).
* **Masonry Layout** - Staggered grid, no fixed row height.
* **Chroma Grid** - Borders / tiles with subtle animating gradients.
* **Split-Screen Scroll** - Two halves sliding in opposite directions.
* **Sticky-Stack Sections** - Sections that pin and stack on scroll.

### Cards & Containers
* **Parallax Tilt Card** - 3D tilt tracking mouse coordinates.
* **Spotlight Border Card** - Borders illuminate under cursor.
* **Glassmorphism Panel** - Frosted glass with inner refraction.
* **Holographic Foil Card** - Iridescent rainbow shift on hover.
* **Tinder Swipe Stack** - Physical card stack, swipe-away.
* **Morphing Modal** - Button expands into its own dialog.

### Scroll Animations
* **Sticky Scroll Stack** - Cards stick and physically stack.
* **Horizontal Scroll Hijack** - Vertical scroll → horizontal pan.
* **Locomotive / Sequence Scroll** - Video / 3D sequence tied to scrollbar.
* **Zoom Parallax** - Central background image zooming on scroll.
* **Scroll Progress Path** - SVG line drawing along scroll.
* **Liquid Swipe Transition** - Page transition like viscous liquid.

### Galleries & Media
* **Dome Gallery** - 3D panoramic gallery.
* **Coverflow Carousel** - 3D carousel with angled edges.
* **Drag-to-Pan Grid** - Boundless draggable canvas.
* **Accordion Image Slider** - Narrow strips expanding on hover.
* **Hover Image Trail** - Mouse leaves popping image trail.
* **Glitch Effect Image** - RGB-channel shift on hover.

### Typography & Text
* **Kinetic Marquee** - Endless text bands reversing on scroll.
* **Text Mask Reveal** - Massive type as transparent window to video.
* **Text Scramble Effect** - Matrix-style decoding on load / hover.
* **Circular Text Path** - Text curving along spinning circle.
* **Gradient Stroke Animation** - Outlined text with running gradient.
* **Kinetic Typography Grid** - Letters dodging the cursor.

### Micro-Interactions & Effects
* **Particle Explosion Button** - CTA shatters into particles on success.
* **Liquid Pull-to-Refresh** - Reload indicator like detaching droplets.
* **Skeleton Shimmer** - Shifting light reflection across placeholders.
* **Directional Hover-Aware Button** - Fill enters from cursor's exact side.
* **Ripple Click Effect** - Wave from click coordinates.
* **Animated SVG Line Drawing** - Vectors drawing themselves in real time.
* **Mesh Gradient Background** - Organic lava-lamp blobs.
* **Lens Blur Depth** - Background UI blurred to focus foreground action.

### Animation Library Choice
* **Motion (`motion/react`)** - default for UI / Bento / state-change motion.
* **GSAP + ScrollTrigger** - for full-page scrolltelling and scroll hijacks. Isolate in dedicated leaf components with `useEffect` cleanup.
* **Three.js / WebGL** - for canvas backgrounds and 3D scenes. Same isolation rule.
* **NEVER mix GSAP / Three.js with Motion in the same component tree.** They fight over the same frames.

---

## 11. REDESIGN PROTOCOL

This skill handles **greenfield builds AND redesigns**. Misclassifying the mode is the single biggest source of bad redesign output.

Sibling to Section 0.F's Reference-Match Protocol: this section audits *your own existing site being changed*; 0.F audits *someone else's live site being emulated for a new build*. Same audit-before-code discipline, different subject.

### 11.A Detect the Mode (first action)
* **Greenfield** - no existing site, or full overhaul approved. Dial baseline from Section 1.
* **Redesign - Preserve** - modernise without breaking the brand. Audit first, extract brand tokens, evolve gradually.
* **Redesign - Overhaul** - new visual language on top of existing content. Treat as greenfield for visuals; preserve content and IA.

If ambiguous, ask **once**: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

### 11.B Audit Before Touching
Document the current state before proposing changes:
* **Brand tokens** - primary / accent colors, type stack, logo treatment, radii.
* **Information architecture** - page tree, primary nav, key conversion paths.
* **Content blocks** - what exists, what's doing work, what's filler.
* **Patterns to preserve** - signature interactions, recognisable hero, copy voice.
* **Patterns to retire** - AI-slop tells, broken layouts, dead links, generic stock imagery, perf traps.
* **Dial reading of the existing site** - infer current `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`. That's your starting point, not the baseline.
* **SEO baseline** - current ranking pages, meta titles, structured data, OG cards. **SEO migration is the #1 redesign risk.**

### 11.C Preservation Rules
* **Do not change information architecture** unless asked. Keep page slugs, anchor IDs, primary nav labels stable for SEO and muscle memory.
* **Extract brand colors before applying Section 4.2.** A brand that is already purple stays purple - apply the LILA RULE's override.
* **Preserve copy voice** unless asked for a rewrite. Visual modernisation ≠ content rewrite.
* **Honor existing accessibility wins.** Do not regress focus states, alt text, keyboard nav, contrast.
* **Respect existing analytics events.** Do not rename buttons, form fields, section IDs that downstream tracking depends on.

### 11.D Modernisation Levers (priority order)
Apply in order - stop when the brief is satisfied:
1. **Typography refresh** - biggest visual lift per unit of risk.
2. **Spacing & rhythm** - increase section padding, fix vertical rhythm.
3. **Color recalibration** - desaturate, unify neutrals, keep brand accent.
4. **Motion layer** - add `MOTION_INTENSITY`-appropriate micro-interactions to existing components.
5. **Hero & key-section recomposition** - restructure top-of-funnel using Section 10 vocabulary.
6. **Full block replacement** - only when the existing block is unsalvageable.

### 11.E Decision Tree: Targeted Evolution vs Full Redesign
* IA, content, and SEO sound → **targeted evolution** (Levers 1-4). ~70% of value at ~40% of risk.
* Visual debt is structural (broken IA, no design system, broken mobile) → **full redesign** with strict content preservation.
* Brand itself is changing → **greenfield**.

### 11.F What Never Changes Silently
Never modify without explicit user approval:
* URL structure / route slugs.
* Primary nav labels.
* Form field names or order (breaks analytics + autofill).
* Brand logo or wordmark.
* Existing legal / consent / cookie copy.

---

## 12. THE BLOCK LIBRARY (Contract - Implementations Land Here Iteratively)

The Reference Vocabulary (Section 10) names patterns. The Block Library implements them with real props, real motion specs, and real code sketches.

**Status:** schema defined here. Blocks will be added iteratively. Do not freelance new blocks without following this schema.

### 12.A File Location
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```

### 12.B Required Frontmatter
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```

### 12.C Required Body Sections
1. **Visual sketch** - short ASCII or description of the layout.
2. **Props API** - the component's interface.
3. **Code sketch** - minimal working implementation (Server Component default, Client island for motion).
4. **Mobile fallback** - explicit collapse rules for `< 768px`.
5. **Motion variants** - one variant per `MOTION_INTENSITY` band (1-3, 4-7, 8-10). Reduced-motion fallback explicit.
6. **Dark-mode notes** - token strategy specific to this block.
7. **Anti-patterns** - common ways this block goes wrong.
8. **References** - links to real examples in production.

### 12.D Block-Library Discipline
* One block per file. No multi-block files.
* Every block must work standalone (drop it into a page, it renders).
* Every block must pass the Pre-Flight Check (Section 14).
* Blocks that depend on a design system from Section 2.A live under `blocks/<category>/<name>--<system>.md` (e.g. `feature/bento-grid--material.md`).

---

## 13. CATEGORY ROUTER (Dispatch + Monitor, Not "Out Of Scope")

This skill's build engine (Sections 0-12) is tuned for landing pages, portfolios, and redesigns of those. For every other category, the job is still **ship it well** — just not by hand-rolling CSS this skill wasn't built for. Do three things, in order, never fewer:

1. **Classify** the brief against the table below.
2. **Dispatch** — invoke the mapped skill(s) with the Skill tool to actually build the surface (per CLAUDE.md Rule 6/7, cross-check `python3 ~/.claude/overseer/search.py <terms>` first in case a sharper off-context skill exists for this exact brief before falling back to the table).
3. **Monitor** — after the specialist skill produces output, run the paired monitor check before calling anything done. If the monitor flags issues, send it back to the builder skill, don't ship it and hope.

Never just say "this is out of scope" and stop. A category not being this skill's build engine is not a reason to leave the user with nothing.

Every row's Monitor column is deliberately not a generic "run the QA skill" stub — it names the specific taste-skill sections (Section 4/6/9's AI-tell, contrast, motion, and copy rules) that still apply to that category, weighted for what that surface actually needs, on top of whatever specialist QA skill runs. A dashboard doesn't care about hero-copy word counts; it does care about 4.2's contrast rules, 4.5's button-contrast/loading-state rules, and 4.4's shape-consistency lock. Apply the taste-relevant subset even when a specialist skill builds the surface.

Two tables: **13.A** routes whole pages/surfaces (what kind of screen is this). **13.B** routes individual components (what widget am I building right now, inside whatever page). A real brief usually needs both — classify the page in 13.A, then classify each non-trivial widget on it in 13.B as you build.

### 13.A Page & Surface Router

| Category | Build with (in stock, verified live 2026-08-23) | Monitor with (specialist QA + relevant taste-skill sections) |
|---|---|---|
| **Published Artifact (single-file HTML on claude.ai, via the `Artifact` tool)** | **`artifact-quality` FIRST** — it owns the medium (CSP allowlist, no build step, theme-aware tokens, asset embedding) and carries a per-category playbook (landing/dashboard/report/data-viz/tool/diagram/deck/game/form/portfolio/timeline). Section 3's React/Next/`next/font`/Tailwind-postcss stack does **not** apply to artifacts — `artifact-quality` §3 replaces it. This skill's Sections 4/6/9 still supply the universal taste rules on top. | `artifact-quality` §8 pre-ship checklist + the specialist skill named in that category's playbook row + the built-in `artifact-design` for publish mechanics |
| Marketing landing / portfolio / about / editorial | This skill (Sections 0-12) directly | Section 14 Pre-Flight Check (full) + `uxui-principles` |
| Redesign of any of the above | This skill's Section 11 protocol | `design-review` (before/after audit) + Section 11.F (never-change-silently list) |
| Pricing page | This skill's engine (Section 10 vocabulary has pricing patterns); web-verified 2026 pattern: 3-tier cards with one visually anchored "recommended" tier, feature comparison below the fold, not inside cards | Section 4.7 (no duplicate CTA intent across tiers) + Section 4.2 (one accent color marks the recommended tier, not three different hues) |
| Blog / article / changelog / release notes | This skill's engine, serif-discipline (4.1) applies at full strength — editorial is the one category where serif is justified by default | Section 4.9 copy self-audit + Section 4.10 quote rules if testimonials/pull-quotes appear |
| Docs / knowledge base / API reference | `docusaurus`-style official doc tooling if the brief names a generator (Docusaurus, Mintlify, Nextra) over hand-rolled CSS; otherwise this skill's engine for the shell + `dataviz` if API examples include response-shape tables | `accessibility` (docs sites are the most-used-by-screen-reader category of any page type) + Section 4.9 long-list alternatives for endpoint/parameter tables |
| Careers / jobs listing | This skill's engine; `growth-engine`/`hr-onboarding` if the brief includes the ATS/pipeline side, not just the listing page | Section 4.9 (job list needs card-grid or filter, never a 50-row plain list) |
| Contact / lead-capture | This skill's Section 4.6 form rules directly | Section 4.5 FORM CONTRAST CHECK + `accessibility` |
| 404 / error / maintenance / coming-soon | This skill's engine — these are low-density, single-message pages, treat like a manifesto hero (Section 4.3 override) | Section 4.7 hero discipline (still applies: one message, one CTA) |
| Newsletter / waitlist signup | This skill's engine + `email-sequence`/`emails` if the brief extends to the confirmation email itself | Section 4.6 form rules + Section 4.5 button-contrast |
| Onboarding flow / product tour / coachmarks | `frontend-patterns` for the step state machine, this skill's Section 4.6 | `accessibility` (focus trap on each step, ESC to dismiss) |
| Settings / account / billing | Official DS from Section 2.A if the product already has one; else `frontend-patterns` + this skill's Section 4.6 | Section 4.2/4.4 locks (settings pages are where color/radius drift happens page-by-page) |
| Notifications center / activity feed | `frontend-patterns` for virtualization/infinite-scroll state; this skill's Section 4.5 for empty/loading states | Section 4.5 empty-state rule (notification centers are shipped "happy path only" almost as often as dashboards) |
| Search results page | `dataviz` if results carry metrics/scores to visualize; else `frontend-patterns` for the results-list state | Section 4.9 long-list alternatives + `accessibility` (live-region announce on result-count change) |
| Profile / public user page | This skill's engine | Section 4.1/4.2 (avoid the AI-purple-gradient-banner default explicitly named in Section 0.D) |
| Admin / dense product UI / dashboards | Official system from Section 2.A (`@fluentui/react-components`, `@carbon/react`, `@atlaskit/*`, Shopify Polaris) via `frontend-design`/`BUNDLE-B-frontend`; off-context `dashboard` skill (KPI-card/sidebar/topbar skeleton, `~/.claude/skills-library/dashboard/SKILL.md`) or `kpi-dashboard-design`; **web-verified 2026 stack**: shadcn/ui + Tailwind v4 + TanStack Table is the dominant free/open combo (Shadcn Admin, Apex Dashboard), MUI X / Devias Kit for Material, React Admin for enterprise 180+-component needs | `uxui-principles` + `accessibility` (WCAG AA) + Section 4.2 (one-accent lock — dashboards are the worst offender for status-color sprawl), 4.4 (shape-consistency), 4.5 (loading/empty/error states) |
| Analytics / reporting / metrics views | `dataviz` (mandatory, has its own palette validator) + TanStack Table or AG Grid for underlying grids — **web-verified 2026**: TanStack Table (headless, ~3M weekly downloads) for full UI control and lower bundle cost, AG Grid (community edition free, enterprise for pivot/tree/server-side rows) when the brief needs pivot tables or 100k+ row virtualization AG Grid ships out of the box | `dataviz`'s own validator + `uxui-principles` + Section 4.9 |
| Multi-step forms / wizards / checkout flows | `frontend-patterns` or `react-patterns` for the state machine, this skill's Section 4.6, `payment-integration` for checkout specifically | `accessibility` (focus order, error announce) + Section 4.6 + Section 4.5 FORM CONTRAST CHECK |
| Full product app UI (SaaS interior) | `frontend-patterns` / `react-patterns` / `nextjs-app-router-patterns` (+ `backend-patterns` if full-stack) | `design-review` + Section 4.2/4.4 locks |
| Code editors / IDE-like surfaces | Monaco or CodeMirror with official theming — confirmed no in-house/off-context skill fits (nearest overseer hits were Unity editor tooling, not applicable) | `accessibility` (keyboard-only pass) |
| Native mobile (iOS/Android/cross-platform) | `ios-developer` (SwiftUI/HIG), `flutter-expert`, `react-native-architecture`, `swiftui-patterns`; off-context `mobile-design`/`mobile-app` when stack-agnostic — **web-verified 2026**: iOS HIG mandates 44pt min touch targets, Material 3 mandates 48dp; Apple's "Liquid Glass" (WWDC 2025) is now the current iOS surface language — see Section 2.B's honest-approximation note before faking it on web | Platform HIG/Material checklist + Section 4.5 tactile-feedback rule — do NOT apply Section 4.1's web fonts or Section 3.A's Next.js/RSC rules |
| Desktop app (Electron/Tauri) | `frontend-patterns` for the renderer UI, native OS conventions (menu bar, window chrome) over web conventions | `accessibility` (OS-level keyboard nav expectations differ from web) |
| Browser extension UI (popup/options page) | This skill's engine at `VISUAL_DENSITY` 5-7 (popups are small, information-dense by necessity) | Section 4.7 layout discipline still applies at popup scale — no hero, but hierarchy rules do |
| CLI output / TUI | No web-frontend skill applies — `bash-pro`/`python-pro`'s formatting conventions or a TUI-specific library (Ink for Node, Rich/Textual for Python, Bubble Tea for Go) named per the brief's language | N/A — visual taste rules don't transfer; readability/scriptability are the bar |
| Email templates (transactional/marketing) | `emails`/`email-sequence`/`email-marketing` — HTML email has its own constraint set (table-based layout, no modern CSS, per-client rendering), do not reuse Section 3's web stack | Those skills' own render-testing guidance (Litmus/Email on Acid class checks), not this skill's Section 14 |
| PDF / print / presentation exports | `pdf`/`pptx`/`docx`/`xlsx` skills per format — different medium, different constraint set (fixed page size, print-safe color, no hover states) | Those skills' own output-format checks |
| Chat / messaging UI | `frontend-patterns` for the message-list virtualization + state; real-time layer per the Realtime Collab row below if multi-user | Section 4.5 empty-state ("no messages yet") + `accessibility` (live-region announce on new message) |
| Video call / conferencing UI | `frontend-patterns` for layout/state; WebRTC integration is a separate infra concern outside this skill's scope, say so | Section 4.4 (tile/grid shape consistency across participant count changes) |
| Live-stream overlay / broadcast graphics | `canvas-design` for static overlay art, `motion-ui` for animated lower-thirds | Section 6.A hardware-accel (overlays run continuously, perf matters more than most categories) |
| Map-based UI / geospatial | No in-house skill — check `python3 ~/.claude/overseer/search.py mapbox leaflet geospatial` before hand-building; Mapbox GL JS / MapLibre / Leaflet are the standard official libraries, use them directly | `accessibility` (map UIs are frequently keyboard/screen-reader inaccessible by default — flag this explicitly to the user) |
| File manager / drive-style UI | `frontend-patterns` for the tree/grid state | Section 4.4 shape-consistency (file/folder icons, row height) |
| Spreadsheet-like UI | `xlsx` if it's literal spreadsheet file I/O; TanStack Table / AG Grid (see Analytics row) if it's an in-app grid | `dataviz` if cells carry visualized data (heatmap-style conditional formatting) |
| Whiteboard / infinite canvas | No in-house skill — `python3 ~/.claude/overseer/search.py canvas whiteboard infinite` first; tldraw or Excalidraw's open-source cores are the standard building blocks, don't hand-roll pan/zoom/hit-testing | Section 6.A perf (canvas apps are the least forgiving category for jank) |
| Code review / diff UI | `code-review-excellence` for the review workflow itself; Monaco's diff-editor mode or `react-diff-viewer` for rendering | `accessibility` (keyboard nav between diff hunks) |
| Marketplace / listings (real estate, jobs, classifieds) | This skill's engine for the shell, `dataviz`/filter-panel patterns from 13.B for the listing grid | Section 4.9 long-list alternatives (card grid over table for listings, always) |
| Forum / community / social feed | `frontend-patterns` for feed virtualization and infinite scroll | Section 4.5 empty-state + Section 4.9 (feeds are a long-list case) |
| Support desk / ticketing | Official DS from Section 2.A if enterprise (Atlassian/Zendesk-adjacent), else `frontend-patterns` | `uxui-principles` + Section 4.6 form rules for ticket-creation forms |
| LMS / course platform | This skill's engine for marketing surfaces, `frontend-patterns` for the in-course player/progress UI | Section 4.5 (progress/completion states are the core UX, get them right) |
| Banking / fintech / crypto-web3 dapp | `accessibility`-first from the start regardless of aesthetic ambition (this is a trust-first quiet-constraint category per Section 0.A.6); `blockchain-developer` for wallet/chain integration specifics | `accessibility` (WCAG AA) + Section 4.2 contrast — financial UIs cannot compromise legibility for aesthetic |
| Healthcare / patient portal | `accessibility`-first, same trust-first override as banking; HIPAA-adjacent constraints are a backend/legal concern outside this skill, flag to `legal-advisor` if the brief touches PHI handling | `accessibility` full WCAG 2.2 AA audit |
| Legal / document signing | `legal-advisor` for the document content itself, this skill's engine for the surrounding UI shell | Section 4.6 form rules (signature/consent fields have their own a11y requirements — flag to `accessibility`) |
| IoT device control panel / kiosk / POS | `frontend-patterns` for the app shell; kiosk/POS need large touch targets (48px+ minimum, tighter than web default) and no hover-dependent affordances | Section 4.5 tactile-feedback (kiosk = touch-only, no mouse fallback to lean on) |
| Game UI / HUD | Off-context game-dev skill category exists (`~/.claude/skills-library` has a `game-xr` category — run `overseer/search.py` for the specific engine named) — this skill's aesthetic rules don't transfer to in-game HUD conventions | N/A — game UX conventions (readability at a glance, diegetic vs non-diegetic) are a different discipline |
| AR/VR / spatial UI | Off-context — search `overseer/search.py spatial ar vr visionOS` per the platform named (visionOS, Quest, WebXR); flat-screen taste rules (Section 4) mostly don't transfer to depth/gaze-based interaction | N/A — spatial interaction heuristics are a different discipline than this skill covers |
| E-commerce storefront | `shopify-development` if on Shopify (Hydrogen+Oxygen is Shopify's 2026 headless stack), `odoo-ecommerce-configurator` if Odoo named; **web-verified 2026 alternatives**: Medusa (modular, swap-any-piece open-source) and BigCommerce (REST/GraphQL, works with any frontend) for non-Shopify headless builds; else this skill's build engine for the storefront shell | `design-review` + Section 4.9 spec-sheet alternatives |
| 3D / WebGL-heavy or committed single-aesthetic | `threejs`, off-context `spline-3d-integration` when Spline is named; `brutalist-skill`/`minimalist-skill` for a fully committed aesthetic | Section 14 Pre-Flight Check + Section 6.A hardware-accel |
| Motion-heavy / scroll-hijacked experiences | This skill's Section 5 (GSAP skeletons) or `motion-ui` | Section 5.D forbidden-pattern check + Section 6.B reduced-motion fallback |
| Realtime collab (presence, cursors, OT/CRDT) | No in-house skill; off-context agent `engineering-realtime-collaboration-engineer` for the sync layer, `react-patterns` for client state; **web-verified 2026**: Yjs is the performance leader (10-50x faster than Automerge on large docs, used by Jupyter/Sanity/Evernote) for self-hosted control, Liveblocks for teams that want a managed service and don't need self-hosting/data-residency, Automerge when the brief needs rich JSON-like document semantics over raw speed | `design-review` on the resulting surface only — sync correctness is a distributed-systems concern, not taste |
| Accessibility-critical / public-sector / regulated | `govuk-frontend`/`uswds` per Section 2.A, `accessibility` from the start | `accessibility` full WCAG 2.2 AA audit — supersedes this skill's aesthetic rules on conflict, per Section 0.A.6 |

If a brief spans two rows (e.g. a marketing site with one embedded dashboard panel), split it: build the marketing shell with this skill's engine, dispatch the dashboard panel per its row, and run both monitor passes before shipping either.

### 13.B Component Router

Individual widgets inside any page from 13.A. Default build path for most of these: a **Radix UI primitive** (`@radix-ui/react-*` or `@radix-ui/themes`, unstyled/accessible-by-default) or the equivalent **shadcn/ui** component (`npx shadcn@latest add <name>`, MIT-owned code) styled per this skill's Section 4 — do not hand-roll a component that a maintained primitive already solves (focus trapping, ARIA roles, keyboard nav are exactly the parts LLMs get wrong by hand). Rows below only call out something *other* than "Radix/shadcn + Section 4" when that's genuinely the better answer.

| Component | Build with | Monitor with |
|---|---|---|
| Button / icon button | Radix Slot + Section 4.5 (contrast, wrap-ban, tactile feedback) | Section 4.5 BUTTON CONTRAST CHECK (mandatory) |
| Text input / textarea | Radix primitives + Section 4.6 | Section 4.5 FORM CONTRAST CHECK |
| Select / combobox | Radix `Select`/`Popover`+`Command` (cmdk) | `accessibility` keyboard nav |
| Checkbox / radio / switch | Radix `Checkbox`/`RadioGroup`/`Switch` | Section 4.5 contrast on checked state |
| Modal / dialog | Radix `Dialog` (built-in focus trap) | `accessibility` (focus trap, ESC, return-focus verified) |
| Drawer / bottom sheet | Radix `Dialog` + `vaul` (drawer-specific, gesture-aware) | Section 6.B reduced-motion fallback on the slide-in |
| Toast / notification | Radix `Toast` or `sonner` | Section 4.5 (transient only per Section 4.5's error-state guidance) |
| Tooltip | Radix `Tooltip` | `accessibility` (hover-only tooltips need a keyboard/touch equivalent) |
| Dropdown / context menu | Radix `DropdownMenu`/`ContextMenu` | `accessibility` keyboard nav |
| Tabs | Radix `Tabs` | Section 4.7 (tabs are a valid alternative to a long list, Section 4.9) |
| Accordion / disclosure | Radix `Accordion` | Section 4.9 (right tool for >5-item content, not default `<ul>`) |
| Breadcrumbs | Semantic `<nav><ol>`, no library needed | `accessibility` (aria-current on the active crumb) |
| Pagination | `frontend-patterns` pattern, or TanStack Table's built-in pagination if paired with a table | `accessibility` (announce page change to screen readers) |
| Avatar | Radix `Avatar` (built-in fallback handling) | Section 4.1 (initials-fallback typography, not a broken-image icon) |
| Badge / tag / pill | Section 4.4 shape-consistency lock | Section 4.2 (badges are the #1 place status-color sprawl happens) |
| Progress bar / meter | Radix `Progress` | Section 6.B (animated progress needs reduced-motion fallback) |
| Slider / range | Radix `Slider` | `accessibility` (arrow-key increment) |
| Date picker / calendar widget | `react-day-picker` (Radix-ecosystem standard) or the design system's own (Carbon/Fluent all ship one) | Section 4.6 (label/error placement still applies) |
| File upload / dropzone | `react-dropzone` (de facto standard) + Section 4.5 for the states | Section 4.5 (loading/error/success cycle, drag-active state) |
| Rich text editor | Off-context — search `overseer/search.py rich text editor tiptap lexical`; Tiptap or Lexical are the current standard headless RTE cores, don't hand-roll contenteditable | `accessibility` (RTEs are notoriously hard to get keyboard-accessible — verify, don't assume) |
| Command palette (Cmd+K) | `cmdk` (the de facto standard, Radix-adjacent) | `accessibility` (focus management on open/close) |
| Sidebar navigation | This skill's Section 4.3/4.7 layout rules | Section 4.7 navigation rules (single-line, height cap — apply to sidebar item density too) |
| Top navigation / navbar | This skill's Section 4.7 (single-line, 80px cap) | Section 4.7 hard rules directly |
| Footer | This skill's engine, low-density by convention | Section 4.9 content density |
| Hero section | This skill's Section 4.7 Hero Stack Discipline | Section 4.7 (hero hard rules, all of them) |
| Pricing table/cards | See 13.A Pricing row | Section 4.7 CTA rules |
| Testimonial / quote card | Section 4.10 | Section 4.10 (3-line cap, no em-dash, real attribution) |
| FAQ accordion | Radix `Accordion` | Section 4.9 |
| Stat / KPI tile | `dataviz` | `dataviz`'s validator |
| Chart / graph | `dataviz` (mandatory, read before writing chart code) | `dataviz`'s own validator |
| Table / data grid | TanStack Table (default) or AG Grid (enterprise/pivot/100k+ rows) — see 13.A Analytics row for the 2026 comparison | Section 4.9 long-list rules + `accessibility` (table semantics, sortable-column announce) |
| Calendar / scheduling widget | `n8n-workflow-patterns`-adjacent if it's a booking flow with backend logic; `react-day-picker`/FullCalendar for the widget itself | `accessibility` (date-grid keyboard nav) |
| Chat bubble / message list | `frontend-patterns` virtualization | Section 4.4 shape-consistency (bubble radius, alignment) |
| Notification bell / inbox | Radix `Popover` + this skill's Section 4.5 | Section 4.5 empty-state |
| Search bar / omnibox | `cmdk` if it's a command-palette-style search, plain input + debounce otherwise | `accessibility` (live-region result-count announce) |
| Filter panel / facets | `frontend-patterns` state + Radix `Checkbox`/`Select` primitives | Section 4.9 (facet lists >5 need grouping, not a raw list) |
| Empty state | Section 4.5 | Section 4.5 empty-state rule directly — "beautifully composed, indicates how to populate" |
| Skeleton loader | Section 4.5 (must match final layout's shape) | Section 4.5 loading-state rule directly |
| Spinner | Discouraged as default per Section 4.5 — prefer skeletons | Section 4.5 |
| Carousel / slider (media) | `embla-carousel` (headless, the current de facto standard) or Radix-ecosystem equivalent | Section 4.9 (carousel is a valid long-list alternative, don't overuse — pairs with Marquee cap in 5.D) |
| Image gallery / lightbox | `yet-another-react-lightbox` or equivalent maintained library, don't hand-roll | `accessibility` (focus trap, keyboard arrow nav between images) |
| Video player (custom-skinned) | `media-chrome` (web-component, framework-agnostic, current standard for custom video UI) over hand-rolled `<video>` controls | `accessibility` (captions, keyboard control) |
| Audio player | `media-chrome` (same library covers audio) | `accessibility` |
| Map embed | See 13.A Map row (Mapbox GL JS / MapLibre / Leaflet) | `accessibility` (flag inaccessibility explicitly) |
| Social share buttons | Hand-rolled is fine here (trivial, few icons + share-intent URLs) — one of the rare acceptable hand-roll cases per Section 4.8 | Section 3.C icon-library rule still applies to the icons themselves |
| Cookie consent banner | This skill's engine; `legal-advisor` for the copy/compliance requirements | `accessibility` (must not trap focus, must be dismissible via keyboard) |
| Onboarding tour / coachmarks | `react-joyride` or equivalent maintained tour library | `accessibility` (focus management per step, ESC to exit) |
| Comment thread | `frontend-patterns` for nesting/collapse state | Section 4.9 (deep nesting needs a collapse affordance, not infinite indent) |
| Rating / review stars | Small enough to hand-roll (rare acceptable case, Section 4.8) or Radix-ecosystem `react-rating` | `accessibility` (radio-group semantics, not divs with click handlers) |
| Wizard / stepper | `frontend-patterns` state machine + this skill's Section 4.6 | `accessibility` (step announce, focus moves to new step's heading) |
| Drag-and-drop list / sortable | `dnd-kit` (current standard, accessible-by-default, successor to react-beautiful-dnd which is unmaintained) | `accessibility` (dnd-kit ships keyboard-sortable out of the box — verify it's wired, don't skip) |
| Kanban board | `dnd-kit` for the drag layer + `frontend-patterns` for column state | Section 4.4 (card shape-consistency across columns) |
| Timeline | This skill's engine, vertical rhythm rules from Section 4 | Section 4.3 layout diversification if used more than once per page |
| Tree view | Radix has no primitive here — `react-arborist` or headless tree libraries; don't hand-roll expand/collapse + keyboard nav | `accessibility` (tree-item ARIA roles, arrow-key nav) |
| Color picker | `react-colorful` (small, maintained, current standard) | `accessibility` (keyboard-adjustable, not drag-only) |
| Icon/emoji picker | `emoji-mart` for emoji; icon picker is usually custom over the chosen icon library from Section 3.C | `accessibility` (searchable, keyboard-navigable grid) |
| Signature pad | `react-signature-canvas` or equivalent | `accessibility` (provide a typed-name fallback for users who can't use a pointer) |
| QR code display | `qrcode.react` or equivalent, trivial | N/A |
| Split view / resizable panels | Radix `Resizable` (an official primitive as of recent versions) or `react-resizable-panels` | `accessibility` (keyboard-resizable via arrow keys on the handle) |
| Virtualized / infinite-scroll list | `@tanstack/react-virtual` (current standard, same ecosystem as TanStack Table) | Section 6.E DOM cost — this is the fix for that guardrail |
| Sticky header | Native CSS `position: sticky`, no library | Section 6.F z-index restraint |
| Floating action button | Section 4.4/4.5 | Section 4.5 button-contrast |
| Dark mode toggle | Section 8 (Dark Mode Protocol) directly | Section 8.D (test both modes before finishing) |
| Language / currency switcher | `i18n-localization` for the underlying i18n setup, this skill's engine for the switcher UI itself | `accessibility` (announce language change) |

If a component isn't listed here, the default is still: check `overseer/search.py` for a maintained library before hand-rolling (Section 3.F dependency-verification rule), prefer a Radix/shadcn primitive when one exists, and apply Section 4's taste rules regardless of what builds it.

### 13.C Visual / Motion / Color-Science Router

Techniques and topics that cut across every page and component above. Where a topic changed materially since Section 4/8's original writing, that's called out explicitly — **web-verified 2026** marks a genuinely new finding, not a restatement of existing rules.

| Topic | Current practice (web-verified 2026 where marked) | Build with | Monitor with |
|---|---|---|---|
| Color space for tokens/scales/gradients | **Web-verified 2026:** `oklch()` is now the default recommendation over HSL — perceptually uniform (equal L values look equally bright across hues), in every evergreen browser since 2023, produces cleaner 12-step ramps for light/dark scale generation. Keep brand HEX as the source of truth, derive variants/gradients in OKLCH | Native CSS `oklch()`/`color-mix()` — no library needed | Section 4.2 (accent-lock, premium-consumer palette ban still apply regardless of color function used to express them) |
| Contrast checking | **Web-verified 2026:** WCAG 2.x ratios (4.5:1 body, 3:1 large text) remain the only *legally* enforceable standard — APCA was pulled from the WCAG3 draft in 2023 and WCAG3 itself isn't expected until 2028-30. Design toward WCAG 2.x for compliance now; APCA as a secondary gut-check is fine but not a replacement | N/A — a check, not a build step | Section 4.5 BUTTON/FORM CONTRAST CHECK + `accessibility`, both already WCAG-2.x-based — no change needed |
| Scroll-linked animation | **Web-verified 2026:** native CSS `animation-timeline: scroll()` now covers ~84% global browser support (Chrome/Edge 115+, Firefox 132+, Safari 18+) and runs on the compositor at zero JS cost — prefer it over GSAP ScrollTrigger for simple scroll-reveal/parallax cases; keep GSAP (Section 5.A/5.B) for pinning/sticky-stack/horizontal-pan, which native CSS scroll-timelines still can't express | Native CSS `animation-timeline: scroll()` with `@supports` fallback for simple cases; GSAP skeletons (Section 5.A/5.B) for pin/stack/pan | Section 5.D forbidden patterns + Section 6.B reduced-motion (applies to native CSS animation too, not just JS) |
| Page/route transitions | **Web-verified 2026:** the View Transitions API shipped cross-browser (Chrome/Edge/Safari 18+) in 2025-26, animates between DOM states natively, zero JS — use it for SPA route transitions instead of a hand-rolled fade/wipe wrapper | Native `document.startViewTransition()` / Next.js's View Transitions support | Section 6.B reduced-motion fallback (`::view-transition-*` respects `prefers-reduced-motion` when guarded) |
| Micro-interactions (hover/press/focus physics) | Section 4.5's tactile-feedback rule (`-translate-y-[1px]`/`scale-[0.98]`) | Motion's `useMotionValue`/`useTransform` (Section 3.B) | Section 5's "motion must be motivated" rule — a hover physics effect still needs a one-sentence reason |
| Perpetual/looping animation (pulse, shimmer, float) | Section 5's context-aware proactivity rules | Motion spring physics per Section 5 | Section 5.D forbidden patterns (infinite loops on every card is the named tell) |
| Gradient meshes / aurora backgrounds | Section 4.2's LILA RULE governs hue choice; technique itself (layered radial/conic gradients or SVG) is fine when motivated | Native CSS `radial-gradient`/`conic-gradient` layering, or SVG filters — no library needed | Section 4.2 (still subject to the accent-color lock even as a background effect) |
| Glassmorphism / backdrop-blur | Section 2.B implementation notes + Section 5's "beyond backdrop-blur" (inner border + inset shadow) guidance | Native `backdrop-filter` | `prefers-reduced-transparency` fallback (Section 2.B, mandatory) |
| Variable fonts / kinetic typography | Section 4.1 typography rules + Section 5's kinetic-type pointer | `next/font` or self-hosted variable font files; native CSS `font-variation-settings` for weight/width animation instead of swapping static weights | Section 4.1 italic-descender-clearance rule when kinetic type includes italics |
| Lottie / After-Effects-exported animation | Not previously covered — `lottie-react` or `@dotlottie/react` (current standard players) when a brief supplies a Lottie/AE export, rather than recreating the animation by hand in CSS/JS | `lottie-react`/`dotlottie` | Section 6.B (Lottie players support `prefers-reduced-motion` pass-through — wire it, don't skip) |
| SVG path/line animation | Section 5's kinetic-typography pointer for text; for icons/illustrations, native SVG `stroke-dasharray` animation or Motion's SVG path support | Native CSS/SVG or Motion, no separate library needed for simple cases | Section 6.B reduced-motion |
| Particle systems / WebGL shader backgrounds | Not previously covered — `threejs` (Section 2.B/13.A) with `@react-three/fiber` for React integration; OGL or raw WebGL for lighter-weight non-React needs | `threejs` / `@react-three/fiber` | Section 6.A hardware-acceleration + Section 6.D Core Web Vitals (particle/shader backgrounds are the easiest way to blow a CLS/INP budget) |
| Cursor effects (magnetic, custom cursor, trailing) | Section 5's Magnetic Micro-physics rule | Motion's `useMotionValue`/`useTransform`, never `useState` (Section 3.B) | Section 3.B rule directly — `useState`-driven cursor tracking is a named anti-pattern |
| Color grading / photography treatment for hero images | Not previously covered — CSS `filter`(contrast/saturate) or a consistent LUT-style treatment applied once at the image-pipeline level, not per-component, so every photo on the page shares one grade | Image-gen tool's own style parameters (Section 4.8) or a shared CSS filter token | Section 4.8 (even minimalist sites need real, consistently-graded images — a mismatched grade across hero vs. supporting photos is itself an AI-tell) |
| Brand color extraction from an existing asset (logo, photo) | Not previously covered — when a redesign brief supplies a logo/photo but no token, extract the dominant/accent colors from the asset itself (e.g. via a color-quantization pass) rather than guessing a palette that doesn't match | Section 11.C (extract brand colors before applying Section 4.2) | Section 4.2's accent-lock, applied to the extracted color |
| Dark-mode color adaptation (not just inversion) | Section 8's token strategy — OKLCH lightness-ramp derivation (see Color-space row above) makes deriving a coherent dark variant from one brand hue mechanical rather than a second manual palette | Section 8.A token strategy + OKLCH derivation | Section 8.D (test both modes before finishing, still the operative rule) |
| Palette generation (complementary/analogous/triadic) | Section 4.2 governs the *creative* constraint (one accent, no banned palettes); for the *mechanical* generation of a coherent ramp from one seed hue, OKLCH hue-rotation is the current method over HSL wheel math | Native OKLCH math or a palette tool during design, not shipped as runtime code | Section 4.2 in full |

This section will grow as new CSS/animation platform features ship — re-run the relevant web search before assuming a 2026 finding above is still current in a much later session.

**Research note (2026-08-23):** rows above were checked against `python3 ~/.claude/overseer/search.py` for each category, not just the ~164 live skills — several rows (dashboards, mobile, realtime collab) upgraded from "no in-house skill" to a real off-context match once searched. If a future brief hits a row still marked "no in-house skill," re-run the search before assuming it's still true — the library grows.

---

## 14. FINAL PRE-FLIGHT CHECK

Run this matrix before outputting code. This is the last filter.

**THIS IS NOT OPTIONAL. Run every box. If any box fails, the output is not done.**

- [ ] **Reference provenance**: if this page has a specific real-world visual/motion look (not generic styling), does the response cite an actual `design-refs/<source>/<topic>/` path with real downloaded files (from `frontend-reference-sources` — `open-pinterest` / `refero` / `supahero` / `60fps` / etc.)? The files existing is the bar — editing/cropping/recoloring/extracting-a-technique from them (not shipping the raw image) is expected, not a violation. A claim like "referenced X style" with no citable file path is not a pass — either cite the path or state plainly that no external reference was used and why (pure logic/layout, no specific look requested).
- [ ] **Brief inference** declared (Section 0.B one-liner)?
- [ ] **Dial values** explicit and reasoned from the brief, not silently using baseline?
- [ ] **Design system** chosen from Section 2 if applicable, or aesthetic labeled honestly?
- [ ] **Redesign mode** detected and audit performed (if applicable, Section 11)?
- [ ] **ZERO em-dashes (`—`) anywhere on the page.** Headlines, eyebrows, pills, body, quotes, attribution, captions, buttons, alt text. Zero. (Section 9.G - non-negotiable.)
- [ ] **Page Theme Lock**: ONE theme (light, dark, or auto) for the whole page. No section flips to inverted mode mid-page (Section 4.11)?
- [ ] **Color Consistency Lock**: one accent color used identically across all sections (Section 4.2)?
- [ ] **Shape Consistency Lock**: one corner-radius system applied consistently (Section 4.4)?
- [ ] **Button Contrast Check**: every CTA text is readable against its background (no white-on-white, WCAG AA 4.5:1)?
- [ ] **CTA Button Wrap**: no CTA label wraps to 2+ lines at desktop?
- [ ] **Form Contrast Check**: form inputs, placeholders, focus rings, labels all pass WCAG AA against the section background?
- [ ] **Serif discipline**: if a serif is used, it is NOT Fraunces or Instrument_Serif (or it is, with explicit brand justification)? Different serif from your previous project?
- [ ] **Premium-consumer palette check**: if the brief is premium-consumer (cookware / wellness / artisan / luxury), the palette is NOT the AI-default beige+brass+oxblood+espresso family? Different family from your previous premium-consumer project?
- [ ] **Italic descender clearance**: every italic word with `y g j p q` has `leading-[1.1]` min + `pb-1` reserve?
- [ ] **Hero fits the viewport**: headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTA visible without scroll, font scale planned around image?
- [ ] **Hero top padding**: max `pt-24` at desktop, hero content does not float halfway down the viewport?
- [ ] **Hero stack discipline**: max 4 text elements in hero (eyebrow OR brand strip, headline, subtext, CTAs)? No tiny tagline below CTAs, no trust micro-strip in hero?
- [ ] **EYEBROW COUNT (mechanical)**: count instances of `uppercase tracking` micro-labels above section headlines across all components. Count ≤ ceil(sectionCount / 3)? Hero counts as 1.
- [ ] **Split-Header Ban**: no "left big headline + right small explainer paragraph" pattern as a section header (vertical stack instead)?
- [ ] **Zigzag Alternation Cap**: no 3+ consecutive sections with the same image+text-split layout?
- [ ] **No Duplicate CTA Intent**: no two CTAs with the same intent ("Get in touch" + "Let's talk" both on page = Fail)?
- [ ] **Logo wall = logo only**: no industry / category labels printed below logos?
- [ ] **Bento Background Diversity**: at least 2-3 bento cells have real visual variation (image, gradient, pattern), not all white-on-white text cards?
- [ ] **"Used by / Trusted by" logo wall** lives UNDER the hero, not inside it, uses REAL SVG logos (Simple Icons / devicon) or generated SVG marks, NOT plain text wordmarks?
- [ ] **Copy Self-Audit**: every visible string re-read, no grammatically-broken or AI-hallucinated phrases ("free on its past" type) shipped?
- [ ] **Motion motivated**: every animation can be justified in one sentence (hierarchy / storytelling / feedback / state transition), no GSAP-for-show?
- [ ] **Marquee max-one-per-page**: no two horizontal marquees on the same page?
- [ ] **Navigation on ONE line** at desktop, height ≤ 80px?
- [ ] **Section-Layout-Repetition** check: no two sections share the same layout family (at least 4 different families across 8 sections)?
- [ ] **Bento has rhythm AND exact cell count** (N items → N cells, no empty cells in middle or at end)?
- [ ] **Long lists use the right UI component** (not default `<ul>` with `divide-y` for > 5 items - see Section 4.9 alternatives)?
- [ ] **Real images used** (gen-tool first, then Picsum-seed, then explicit placeholder slots) - NO div-based fake screenshots, NO hand-rolled decorative SVGs, NO pure-text minimalism?
- [ ] **No pills/labels overlaid on images** (no `Plate · Brand`, no `Field notes - journal`)?
- [ ] **No photo-credit captions as decoration** (`Field study no. 12 · Ines Caetano`)?
- [ ] **No version footers** (`v1.4.2`, `Build 0048`) on marketing pages?
- [ ] **No micro-meta-sentences** under eyebrows ("Each of these is a feature we ship today...")?
- [ ] **No decoration text strip at hero bottom** (`BRAND. MOTION. SPATIAL.`)?
- [ ] **No floating top-right sub-text** in section headings?
- [ ] **No scoring/progress bars with filled background tracks** as comparison visuals?
- [ ] **No locale / city-name / time / weather strips** unless brief is genuinely globally-distributed or place-focused?
- [ ] **No scroll cues** (`Scroll`, `↓ scroll`, `Scroll to explore`)?
- [ ] **No version labels in hero** (V0.6, BETA, INVITE-ONLY) unless the brief is a launch?
- [ ] **No section-numbering eyebrows** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`)?
- [ ] **No decorative dots** (zero by default, only for real semantic state)?
- [ ] **No `border-t` + `border-b` on every row** of long lists / spec tables?
- [ ] **Content density** sane: no 20-row data tables, no fake-precise specs without justification, ≤ 25-word sub-paragraphs by default?
- [ ] **Quotes ≤ 3 lines** of body, attribution clean (no em-dash)?
- [ ] **Motion claimed = motion shown**: if `MOTION_INTENSITY > 4`, page actually animates, not just claimed?
- [ ] **GSAP sticky-stack / horizontal-pan** implemented per Section 5.A / 5.B canonical skeleton (`start: "top top"`, `pin: true`, correct scrub)?
- [ ] **No `window.addEventListener('scroll')`** - using Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven animations only?
- [ ] **Reduced motion** wrapped for everything `MOTION_INTENSITY > 3`?
- [ ] **Dark mode** tokens defined and tested in both modes?
- [ ] **Mobile collapse** explicit (`w-full`, `px-4`, `max-w-7xl mx-auto`) for high-variance layouts?
- [ ] **Viewport stability**: `min-h-[100dvh]`, never `h-screen`?
- [ ] **`useEffect` animations** have strict cleanup functions?
- [ ] **Empty / loading / error** states provided?
- [ ] **Cards omitted** in favor of spacing where possible?
- [ ] **Icons** from an allowed library only (Phosphor / HugeIcons / Radix / Tabler), no hand-rolled SVG paths?
- [ ] **Motion** isolated in client-leaf components with `'use client'` at the top, memoized?
- [ ] **No AI Tells** from Section 9 (Inter as default, AI-purple, three-equal cards, Jane Doe, Acme, "Quietly in use at")?
- [ ] **Core Web Vitals** plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] **One design system** per project (no Material + shadcn mixed)?
- [ ] **Awwwards-weighted effort check** (Appendix D.2): did Design + Usability get more real effort than Creativity/motion? If the build is 90% motion polish and thin on typographic/layout discipline, fix the ratio before shipping.

If a single checkbox cannot be honestly ticked, the page is not done. Fix it before delivering.

---

## 15. ADVANCED COMPONENT & STRUCTURE TECHNIQUES (merged from gpt-tasteskill + high-end-visual-design)

These are optional named techniques, folded in from two now-retired sibling skills. Reach for them
when the design read calls for extra structural rigor or a specific haptic/nested-card feel — they
are not defaults, same rule as Section 5.

* **AIDA page ordering (optional structural lens):** for landing/marketing pages, one valid way to
  sequence sections is Attention (hero) → Interest (features/bento) → Desire (proof/scroll-media) →
  Action (pricing/footer CTA). Use it as a checklist, not a mandate — plenty of good pages don't fit
  this shape.
* **Gapless bento grids:** when building a bento/masonry feature grid, use `grid-auto-flow: dense`
  (Tailwind `grid-flow-dense`) and verify `col-span`/`row-span` values interlock with no empty dead
  cells. Prefer 3-5 intentional cards over 8 crowded ones.
* **Hero 2-3 line iron rule:** H1 in a hero must not exceed 2-3 lines. Fix by widening the container
  (`max-w-5xl`/`max-w-6xl`/`w-full`) and using a `clamp()` font size, not by shrinking the message.
* **Meta-label ban:** never use placeholder-style section labels ("SECTION 01", "QUESTION 05",
  "ABOUT US" as an eyebrow) — reads as template scaffolding left in by accident.
* **Double-Bezel nested card architecture:** for a premium "machined hardware" card feel, nest an
  outer shell (subtle bg, hairline `ring-1`/border, large radius, e.g. `rounded-[2rem]`) around an
  inner core with its own background and a mathematically smaller concentric radius
  (`rounded-[calc(2rem-0.375rem)]`) plus an inset highlight
  (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`). Use for hero feature cards, not every card on
  the page.
* **Button-in-button trailing icon:** when a CTA has a trailing arrow/icon, nest it in its own
  circular wrapper (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10`) flush with the button's inner
  padding, rather than placing the icon naked next to the label. On hover, translate the inner icon
  diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) — this is the concrete
  implementation of the "Magnetic Micro-physics" tool referenced in Section 5.
* **Fluid Island nav:** a floating detached pill navbar (`mt-6 mx-auto w-max rounded-full`) is a valid
  alternative to an edge-to-edge sticky nav for premium/agency briefs. If it expands to a full-menu
  overlay, morph the hamburger into an X (`rotate-45`/`-rotate-45`) and stagger the revealed links in
  (`translate-y-12 opacity-0` → `translate-y-0 opacity-100`, staggered `delay-*`).
* **Vibe/texture archetypes (extra flavor on top of Section 4.2 color rules):** *Ethereal Glass*
  (OLED black, radial mesh glow, heavy `backdrop-blur-2xl`) for SaaS/AI/tech; *Editorial Luxury*
  (warm cream/espresso, variable serif headings, subtle film-grain) for lifestyle/real-estate/agency
  — only when Section 4.1's serif-discipline override actually applies; *Soft Structuralism*
  (silver-grey/white, bold grotesk, diffused ambient shadow) for consumer/health/portfolio. Pick one
  per project, same discipline as the color-consistency lock in 4.2.

---

# APPENDICES - Real Source-Backed Reference Material

The sections below are vendored reference content. They give the agent real install commands, real canonical doc links, and real working starter snippets for each design system named in Section 2. Use them to ground decisions in production reality, not training-data fiction.

## Appendix A - Install Commands per Design System

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## Appendix B - Canonical Sources (read these before reinventing)

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### Native CSS / W3C standards
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (Apple platforms only)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## Appendix C - Apple Liquid Glass: Honest Web Approximation

Do **not** treat random CSS snippets as official Apple Liquid Glass.

### What is official
Apple documents Liquid Glass inside Apple's Human Interface Guidelines and Developer Documentation for **Apple platforms**. It is a dynamic material used across Apple platform UI. Apple's native implementation belongs to Apple platform APIs and system components, **not a public web CSS package**.

Relevant official docs:
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### What is NOT official
There is no `liquid-glass.css` from Apple for normal websites.

A web approximation can use:
- `backdrop-filter`
- transparent backgrounds
- layered borders
- highlight overlays
- gradients
- motion
- strong contrast fallbacks

But that is **web glassmorphism / frosted-glass approximation**, not official Apple Liquid Glass. Label it as such in comments.

### Safer web approximation skeleton

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

**Important:** `prefers-reduced-transparency` has uneven browser support; test it. Always provide enough contrast even without blur.

---

## Appendix D - Named UX Laws & Awwwards-Weighted Self-Score

Source-backed grounding (lawsofux.com, Awwwards judging criteria) for *why* several rules above exist. Use this to judge edge cases the explicit rules don't cover, not as a separate ruleset to apply on top.

### D.1 Laws that map directly to rules already in this skill
* **Fitts's Law** (target time = f(distance, size)) → why CTAs are large and thumb-reachable (Section 4.5 tactile feedback, hero CTA sizing).
* **Hick's Law** (more choices = slower decisions) → why nav must fit one line and hero max 4 text elements (Section 4.7).
* **Jakob's Law** (users expect your site to work like sites they know) → put novelty in visuals/motion, not in core interaction patterns (nav behavior, form flow, scroll direction).
* **Miller's Law** (~7±2 items in working memory) → why long lists need chunking/grouping, not a flat 15-row list (Section 4.9).
* **Aesthetic-Usability Effect** (beautiful UI reads as more usable, a real bias) → polish on the primary path earns more than it costs; do not use this to excuse actual usability bugs.
* **Von Restorff Effect** (the one different item is remembered) → why a page has exactly one primary CTA/accent, not three competing ones (Section 4.2 Color Consistency Lock, No Duplicate CTA Intent).
* **Doherty Threshold** (perceived productivity rises when response stays under 400ms) → interaction latency budget for hover/click feedback and route transitions, tighter than the page-load Core Web Vitals budget in Section 6.D.
* **Peak-End Rule** (experience judged by its peak moment and its ending) → the footer/final-CTA section and one standout moment (hero or a signature interaction) matter more to perceived quality than uniform polish everywhere.

### D.2 Awwwards' actual scoring weights (design 40 / usability 30 / creativity 20 / content 10)
The single most common LLM failure mode this corrects: over-investing in "creativity" (motion, scroll hijacks, novel layout) at the expense of "design" and "usability" fundamentals, when those two together are 70% of what actually reads as quality. Before shipping, weigh effort spent against this ratio:
* **Design (40%)** — typographic system consistency, layout discipline, negative space, one idea carried through every section. This is Sections 4.1-4.4 and 4.7 of this skill. Get this right first.
* **Usability (30%)** — can a first-time visitor orient in seconds, does it perform, is it accessible. This is Section 6.D (Core Web Vitals) plus the contrast/a11y checks in 4.5.
* **Creativity (20%)** — only scores when layered on top of solid Design + Usability. A page that is 90% motion and 10% typographic discipline is optimizing the wrong 20%.
* **Content (10%)** — real copy and real imagery beat placeholder content at any polish level (Section 4.8, 4.9 Copy Self-Audit).

If a build is running out of time/budget, cut from Creativity before cutting from Design or Usability — that is the inverse of what most AI-generated output does by default.

---

## Appendix E - Decision Logic: When To Use Each Pattern (source-backed)

Concrete "when/why", not vibes. Use to resolve dial/aesthetic choices the brief doesn't spell out.

### E.1 Dark mode vs. light mode
* **Light mode default for:** productivity tools, content-heavy/reading platforms, professional/B2B, anything requiring precise color discrimination (photo/brand/illustration tools). Better sustained readability, no astigmatism halo/blur issue that some users get on light-on-dark text.
* **Dark mode default for:** entertainment, creative/dev tools, evening-use apps, OLED-heavy mobile contexts (real battery savings on OLED/AMOLED only, not LCD).
* **Practical default:** if the brief doesn't name one, pick `light` for B2B/trust/content, `dark` for tech/dev/creative/AI-product, and respect `prefers-color-scheme` when in doubt. Never both per Section 4.11's Page Theme Lock.

### E.2 Glassmorphism
* **Use for:** dashboards, mobile app chrome, card layouts, nav bars, modals — anywhere a floating layer over content needs to feel present without blocking it. This matches Section 5's existing "premium consumer / Apple-adjacent / media-overlay" guidance.
* **Use conservatively:** on nav and modals specifically, not full-page. Layering it everywhere (every card, every section) is the tell, not the technique.
* **Don't use for:** public-sector, dashboards where legibility of dense data is the job, or any surface where the blur would sit over small/dense text.

### E.3 Brutalism / Neubrutalism
* **Use for:** tech startups, creative agencies, digital-art/portfolio platforms wanting to signal originality/confidence. Already covered by the sibling `brutalist-skill` for a fully committed direction.
* **Soft Brutalism variant** (bold borders + high contrast, but friendly fonts + generous whitespace) is the usable middle ground when raw brutalism would fight the brand's approachability.
* **Don't use for:** trust-first, regulated, or accessibility-critical briefs (matches Section 1.A's existing VARIANCE 3-4 guidance for those).

### E.4 Bento grid
* **Use when:** the content is genuinely diverse (video + stats + text + testimonial in one section) and benefits from bite-sized, scannable chunks — portfolios, feature overviews, project-management-style dashboards.
* **Don't use when:** you have 3-4 uniform items with nothing visually distinct between them — that's a plain grid wearing a bento costume. Section 4.7's BENTO CELL COUNT RULE already prevents the most common failure (padding cells to look trendy); this is the upstream check of whether bento is the right pattern at all before applying that rule.

### E.5 Design system: build custom vs. adopt official
* **Adopt the official package (Section 2.A)** when the brief matches a known ecosystem (Fluent/Material/Carbon/Polaris/etc.) or when the project will scale past one team — Figma's research found enterprise UI built without a shared design system saw ~34% slower production velocity from redundant one-off components.
* **Build custom (Section 2.B / 3.A defaults)** for a single landing page, a portfolio, or an MVP where a full design system is overhead the project will never recoup.
* **Governance flag:** if a build is expected to grow into a multi-page product (not just a marketing site), say so explicitly and recommend establishing component ownership/review process early — retrofitting a design system after 20 ad-hoc pages is the expensive path.

---

## Appendix F — 2026 Web-Verified Research Findings

30 targeted web searches run 2026-08-23 to ground Section 13's routing and Section 4's taste rules in current data rather than inherited assumption. Each finding below changes or confirms a specific rule elsewhere in this file — cross-referenced, not just trivia. Re-search any line here before trusting it in a much later session; "2026" facts age.

**Color & CSS platform**
- `oklch()` is the 2026 default over HSL for tokens/scales/gradients — perceptually uniform, 3+ years of stable browser support. Feeds Section 13.C's Color-space row and Section 4.2's palette rules (still govern *which* hues, OKLCH just makes deriving ramps mechanical).
- APCA contrast was pulled from the WCAG3 draft in 2023; WCAG3 itself isn't expected until 2028-30. **Keep grading contrast against WCAG 2.x ratios** (4.5:1 body / 3:1 large) — Section 4.5's CONTRAST CHECK rules are correctly targeting the only legally-enforceable standard.
- CSS `:has()` is 100% supported across major browsers in 2026 — production-safe for parent-styles-on-child-state (invalid-form-group highlighting, card-changes-when-image-present) with zero JS and zero fallback needed.
- Container queries: 78% of production sites now use them, baseline support since 2023. Component-scoped responsive design (not just viewport breakpoints) is now the default expectation, not a stretch goal — relevant to Section 3.E's breakpoint guidance.
- Design tokens: the W3C DTCG format (v2025.10, Oct 2025) is backed by Adobe/Google/Meta/Figma; 84% of teams surveyed had adopted it in 2026 (up from 56% the year before). When a brief needs a cross-tool token pipeline (Figma → code), target this format, not a bespoke JSON shape.
- Tailwind v4's Oxide (Rust) engine is 3.5-10x faster to build than v3, CSS-native `@theme` config over `tailwind.config.js`. Confirms Section 3.A's existing v4-default — "zero reason to start with v3 in 2026" per the research.

**Performance**
- INP (Interaction to Next Paint) is now the hardest-failed Core Web Vital — 43% of sites miss the 200ms threshold. Fix priority order: whichever metric is "poor" first, then INP (hardest), then LCP (highest commercial impact), then CLS (easiest). The single highest-leverage fix: audit and cut/defer every third-party script that doesn't directly drive conversion.
- AVIF vs WebP: WebP remains the safer universal default (97-98% support, faster encode); AVIF is 20-50% smaller when support allows. 2026 recommendation: serve AVIF with WebP fallback via `<picture>`, or let an image CDN negotiate it — don't hand-pick one globally.
- Variable fonts are now baseline-expected, not optional — one ~150KB variable file replaces 4 static weight files (~600KB), directly improves LCP/CLS. Reinforces Section 4.1 — if a typography choice needs multiple weights, source the variable version by default.
- Scroll-driven animation (`animation-timeline: scroll()`) reached ~84% global support in 2026, runs on the compositor at zero JS cost. **Updates Section 5**: use native CSS scroll-timelines for simple scroll-reveal/parallax; reserve GSAP ScrollTrigger (Section 5.A/5.B skeletons) for pinning/sticky-stack/horizontal-pan effects native CSS still can't express.
- The View Transitions API shipped cross-browser (Chrome/Edge/Safari 18+) in 2025-26 — native, zero-JS route/state transitions. Prefer it over a hand-rolled fade wrapper for SPA route changes (Section 13.C).

**Accessibility & compliance**
- WCAG 2.2 was ratified as ISO/IEC 40500:2025 in Oct 2025 and is the baseline every accessibility law references (EAA, Section 508, EN 301 549) — 9 new success criteria vs 2.1, most-failed being Focus Not Obscured (2.4.11), typically broken by sticky headers/cookie banners covering focused fields during keyboard nav. **Check for this specifically** on any page with a sticky header or persistent banner.
- Accessibility overlay widgets (accessiBe-style bolt-on scripts) are now a *litigation risk*, not a shortcut: 25%+ of 2025's ADA lawsuits targeted sites that had an overlay installed, the FTC fined accessiBe $1M for false compliance claims, and the disability community (NFB) formally rejects them. **Never recommend an overlay widget as an accessibility fix** — real semantic HTML/ARIA/focus-management work is the only thing that holds up, both for users and legally.

**Component ecosystem (updates the "Build with" defaults used throughout Section 13.B)**
- shadcn/ui now commands ~95% of new React/Next.js boilerplate adoption in 2026 — components are Radix-primitive-powered, Tailwind-styled, and copy-owned (not an npm dependency). This is the strongest possible confirmation of Section 13.B's shadcn/Radix default.
- Chakra UI v3 rebuilt itself on Ark UI (headless primitives) + Panda CSS; Mantine ships 120+ components/70+ hooks as the most feature-complete alternative after MUI; Ark UI itself is the headless cross-framework (React/Vue/Svelte) option when a brief needs multi-framework component logic. Add these as fallback options in 13.B rows where shadcn doesn't fit (e.g., a non-Tailwind or multi-framework brief).
- AI component generators: v0 (Vercel) generates shadcn/Tailwind React components from text/image — the right tool when a brief wants fast component scaffolding within an existing codebase (matches `magic-ui-generator`'s role in `BUNDLE-B-frontend`). Lovable/Bolt build whole apps including backend — out of this skill's scope, note to the user if the brief is actually asking for that.

**Category-specific UX data (feeds Section 13.A rows directly)**
- **Dashboards/Admin (13.A):** 2026 stack consensus is shadcn/ui + Tailwind v4 + TanStack Table for free/open builds (Shadcn Admin, Apex Dashboard); MUI X/Devias Kit for Material; React Admin for 180+-component enterprise needs. Confirms and sharpens the existing row.
- **Pricing pages (13.A):** price anchoring lifts perceived value 30-50%; tier order, a deliberately-weaker decoy tier, charm pricing (endings in 9), and a single "Most Popular" badge are the mechanisms — not decoration. Add to the Pricing row's guidance: every element on a pricing page should map to one of these mechanisms, not be arbitrary.
- **Checkout/e-commerce (13.A):** average abandonment is 70.22%; cutting a 4+-step checkout to ≤2 steps drops that step's abandonment contribution from 22% to 8.6%. Top abandonment causes: surprise costs (48%), forced account creation (26%), length/complexity (22%), payment-security distrust (18%). One-page checkout beats multi-step by ~20 points; BNPL cuts abandonment ~20% on orders over $100. Trust badges (real ones: PayPal/Shop Pay/Apple Pay logos, 4.3+-star review widgets) lift completion 17% — generic "SSL Secured" badges measurably do not, and belong next to the payment field, not the footer.
- **Onboarding (13.A):** the operative metric is time-to-value, not step count alone — a narrowly-defined activation event ("published first flow," not "logged in 3x") with a guided path to it in under 5 minutes. Interactive onboarding lifts activation ~50% over passive tours. Keep to 3-7 steps; past 20, completion drops 30-50%.
- **Notifications (13.A/13.B):** a single blanket "Allow notifications?" toggle is no longer acceptable UX — separate transactional from promotional at both system and UI level, different frequency/urgency rules for each, keep marketing off lock-screen unless explicitly opted in.
- **Empty states (13.B):** only 2-5% of sessions hit them, but they're a disproportionate lever — headline + short description + relevant icon/illustration + one CTA is the pattern that converts a dead end into a next step (confirms Section 4.5's existing empty-state rule).
- **Skeleton loaders vs spinners (13.B):** skeletons are perceived as ~50% faster than spinners at identical actual load time. 2026 best practice orchestrates both by duration: 0-300ms show nothing, 300ms-1s a subtle spinner if layout is unknown, 1s-10s a skeleton matching the incoming layout. Confirms and sharpens Section 4.5's "skeletal loaders matching final layout" rule with the timing thresholds.
- **Mobile navigation (13.A):** bottom tab bars are the confirmed winner for 3-5 primary destinations, more than 5 items degrades thumb-reach touch targets. iOS 44×44pt / Android 48×48dp minimums (already in Section 13.A's mobile row) are the enforced platform minimums, not suggestions.
- **Form validation (13.B):** inline validation reduces errors ~22% and speeds completion ~42% — but only for checks that make sense mid-field (format, length); validate whole-form logic (password confirmation, cross-field rules) on submit, not per-keystroke. Sharpens Section 4.6.

**Aesthetic trend confirmations**
- Bento grids remain the dominant 2026 layout trend, now evolving toward "Bento 2.0" (12-24px corner rounding, hover-reveals-video/data micro-interactions) — Section 4.7's BENTO CELL COUNT RULE and Appendix E.4 still govern when to use one; this just confirms the pattern is current, not fading.
- Glassmorphism is explicitly evolving into Apple's "Liquid Glass" language (translucent + light-reactive, not just static blur) — Section 2.B/5's existing honest-approximation guidance (there is no official web `liquid-glass.css`) is more relevant now, not less, since the reference point moved.
- Serif is having a real 2026 comeback (bold, high-contrast, "tech-tuned yet handcrafted" display serifs, partly AI-brands-signaling-warmth-driven) — this does **not** override Section 4.1's SERIF DISCIPLINE rule (serif still needs brand justification, not "creative brief" alone), but it does mean a justified serif choice in 2026 reads as current, not dated.
- The "AI slop" visual signature is now explicitly named in industry writing: Tailwind default blue-500/indigo-600/violet-500 (the 200-290° hue band) is called out by name as *the* single biggest tell, alongside default Inter, purple-blue gradient heroes, and 3-column icon-feature grids. Directly validates Section 0.D's Anti-Default Discipline and Section 4.2's LILA RULE — these aren't taste opinions, they're now a named, documented industry pattern.

**Internationalization**
- RTL (Arabic/Hebrew) layout: navigation and logo anchor right, sidebars flip right-to-left, primary content column anchors right. Form labels stay **above** the field in RTL too (never to the right) — avoids the mirrored-layout confusion. Icon mirroring is selective, not universal (directional icons like arrows/back-buttons mirror; icons depicting real-world objects generally don't) — flag this as a per-icon judgment call, not a blanket rule, when a brief needs RTL support (relevant given the user's Arabic Localization pillar).

**Batch 2 (searches 31-50, 2026-08-23) — components, motion science, color/trend**
- **Card hover states:** Material's baseline is 2dp resting / 8dp on hover; the practical CSS translation is `box-shadow` blur 12-24px + `translateY(-2px to -4px)` on hover, always paired with a visible keyboard-focus outline (not hover-only). Updates 13.B's Card guidance and Section 4.4.
- **Hero layout (split vs. centered):** no universal winner — split-screen (copy left, product/image right) is the reliable B2B SaaS default because it separates message from visual; centered full-bleed works for brand-led/lifestyle/hospitality briefs with minimal copy. Confirms Section 4.3's ANTI-CENTER BIAS is directionally right for SaaS but the override for "manifesto/brand-led" briefs is real, not a loophole. Also: replacing hero image sliders with a single static asset measurably improves LCP — never ship an auto-rotating hero carousel as the primary hero.
- **Testimonials:** five patterns cover real use — Wall of Love (grid/masonry), Carousel, Single Spotlight, Floating Pop, Avatar row with hover-reveal. Video testimonials specifically build more trust than text in 2026 (fabricated text quotes are cheap and buyers know it) — when a brief has real video testimonials available, lead with 1-2 near the strongest decision points, use text testimonials for breadth. Sharpens Section 4.10.
- **FAQ accordion vs. list:** accordion below ~15 questions is a judgment call — a flat visible list is fine and arguably better UX under 15 items with short answers; accordion earns its place above that, or when questions group into 5-8 topical tabs. Don't default to accordion purely because it's the "modern" choice for a 6-question FAQ.
- **Comparison tables:** consistent column alignment, generous cell padding (not dense), color used to guide attention not decorate, and the recommended-tier column gets one clear visual treatment (background tint, border, or CTA emphasis — pick one, not all three). Feeds 13.A's Pricing row and 13.B's Table row.
- **CTA copy:** first-person framing ("Start my free trial") outperforms second-person by 10-90% in tested cases; value-focused ("Get instant access") beats obligation-focused ("Submit"). 2-5 words, benefit-led, WCAG-AA-compliant contrast, 44×44px minimum tap target. Updates Section 4.5/4.7's CTA guidance with the first-person framing detail specifically — worth defaulting to unless the brand voice is explicitly second-person/corporate.
- **Footers:** a mega-footer (multi-section, descriptive category links, not just "Services") is justified for content-heavy/enterprise/ecommerce sites; a simple footer is correct for a single landing page — don't pad a one-page site's footer to look more "established." Specific link labels beat vague ones ("SEO Services" over "Our Services") for both usability and SEO.
- **Sticky nav hide-on-scroll:** the current pattern (2026) is hide-on-scroll-down, reveal-on-scroll-up, implemented via a scroll-direction listener toggling a CSS class (or the newer scroll-driven-animation approach per Appendix F's scroll-timeline finding) — appropriate for content-heavy/reading-focused pages (blogs, docs) where a persistent nav steals vertical space; less necessary for short marketing pages where the nav is compact already (Section 4.7's 80px cap).
- **Progressive disclosure:** the umbrella pattern behind multi-step forms, accordions, and "advanced options" toggles — reveal only what's needed for the current step, defer the rest. This is the *why* behind Section 4.6/4.7's form and content-density rules, not a new rule — cite it when justifying a multi-step form over a single long one.
- **Infinite scroll vs. pagination vs. "Load more":** pagination wins when users are goal-directed and need to compare/backtrack/bookmark (ecommerce category pages, search results); infinite scroll suits passive browsing (social feeds, discovery grids); "Load more" is the 2026 compromise — keeps scroll momentum while preserving footer/deep-link access and SEO crawlability that pure infinite scroll breaks. **Default to "Load more" over true infinite scroll** unless the brief is explicitly a passive-browse social feed — this is a sharper default than Section 4.9 previously stated.
- **Spring physics vs. cubic-bezier easing:** a CSS `cubic-bezier()` is a fixed 4-point curve; a real spring (mass/stiffness/damping) overshoots and settles dynamically, which is why it feels right for interruptible interactions (drag, gesture, hover-repeatedly). Native CSS can now approximate true springs via `linear()` sampling of a spring equation (no JS). **Use spring/`linear()` for anything the user can interrupt mid-animation** (drag-and-drop, repeated hover); plain `cubic-bezier`/`ease-out` remains correct for one-shot, non-interruptible transitions (page loads, modal opens). Sharpens Section 5's Motion's `useMotionValue` guidance with the actual mechanical reason springs matter.
- **Disney's 12 animation principles applied to UI:** the two most directly actionable for interface work are **Easing** (ease-out for entering elements, ease-in for exiting, ease-in-out for same-element state changes — already Section 5's implicit standard, now with the correct principle name) and **Staging/Secondary Action** (when multiple elements animate together, the primary action must animate earlier/stronger than secondary/decorative elements, so the eye is never ambiguous about what to look at). Use "staging" as the one-word justification when Section 5's MOTION MUST BE MOTIVATED rule asks for a reason.
- **Pantone Color of the Year 2026: Cloud Dancer (a near-white, PANTONE 11-4201)** — explicitly a "structural/scaffolding" color meant to let other colors shine, not a standalone brand color. Signals a real 2026 shift toward calmer, more restrained palettes after 2024-25's saturated "dopamine color" wave — reinforces (does not override) Section 4.2's existing max-1-accent, <80%-saturation default; a brief asking to feel "current" in 2026 leans toward restraint, not more saturation.
- **Color psychology data point:** red CTA buttons outperformed green/blue/gray by ~37% average conversion lift in tested cases, largest in urgency/time-limited contexts — this is a testable lever, not a mandate to make every CTA red; it conflicts with Section 4.2's accent-lock only if red isn't already the page's locked accent, so treat it as a reason to A/B test, not a reason to break the one-accent rule.
- **Perceived vs. actual load time:** users perceive load time as ~15% longer than actual (a 2s load feels like 2.3s) — reinforces why Section 4.5's loading-state rules (skeleton over blank white, status feedback over silence) matter more than shaving raw milliseconds once you're already in a reasonable range.
- **Color-contrast/colorblind tooling:** WhoCanUse (contrast + population-impact data), Stark (Figma/Sketch-integrated, industry standard), and RGBlind/Coblis (colorblind simulation) are the current standard tools — recommend these by name when a brief needs a real accessibility-tooling pass, not just a rule citation.
- **Mesh gradients + grain/noise texture:** mesh gradients (soft, multi-point, "liquid" blends) remain the standard for fintech/AI/SaaS hero backgrounds; the *new* 2026 layer is adding subtle film-grain/noise texture on top, explicitly as a reaction against "too-perfect" AI-generated smoothness — a texture-less mesh gradient now reads as more AI-generic than one with grain. Add grain as a cheap, real differentiator when a brief's hero uses a gradient background.
- **3D product configurators (ecommerce):** real-time rendering + AI-guided material/color suggestions are the current standard for premium ecommerce; measured impact is up to 94% more engagement and 40% fewer returns vs. static photos alone — when a brief is a physical-product ecommerce build with configurable variants (color/material/size), proactively suggest a 3D configurator (`threejs`/`@react-three/fiber`, 13.A's 3D row) over a static swatch-picker as the higher-bar option, not just the CSS-easy default.
- **Brutalism (2026 status):** not just still trending — evolved into "Tactile Brutalism" (sharp geometry, 1px solid borders, stark type, explicitly *no* blurred drop shadows) as a premium-tier reaction against AI-generic softness, plus a "Cute-alism" variant (brutalist structure + kawaii/playful micro-illustration). Confirms `brutalist-skill`'s continued relevance; the 1px-border/no-blur-shadow detail is a concrete implementation note worth passing to that skill when invoked.
- **Kinetic typography (2026 status):** now technically mainstream via variable fonts (animate weight/width/slant from one file) + the CSS Scroll-Driven Animations API (Appendix F) — genuinely lower-cost to implement well than it was even a year prior. Section 4.1's kinetic-type pointer and Section 5's "motion must be motivated" rule both still gate it — motion that aids comprehension/pacing earns its place, decoration-only motion still risks the Core Web Vitals budget.
- **Icon style split:** 2026 has two legitimate poles, not one winner — hyper-minimal single-pixel-stroke line icons (Section 3.C's existing default stack: Phosphor/Hugeicons/Radix/Tabler) for restrained/technical brands, vs. soft-3D/duotone icons for warmer lifestyle/fintech-consumer brands. Pick per the Section 0.B design read, same as any other aesthetic dial — don't treat one as more "current" than the other, both are actively trending for different audiences.

**Batch 3 (searches 51-60, 2026-08-23) — patterns, architecture, ethics, governance**
- **Breadcrumbs:** only add them when a real content hierarchy exists that users need to navigate back through — not decoratively on a flat 3-page site. Mobile: collapse long trails with an ellipsis or horizontal-scroll rather than removing them; wrap in `<nav aria-label="Breadcrumb">`. Sharpens 13.B's Breadcrumbs row with the real accessibility markup requirement.
- **Command palette (Cmd+K):** genuinely mainstream now (Linear/Vercel/GitHub/Notion/Figma/Raycast) via `cmdk`, which shadcn's `Command` component wraps — but the explicit warning from research is real: **a command palette is a shortcut on top of working navigation, not a fix for confusing IA.** If a brief wants Cmd+K to compensate for a site that's hard to navigate normally, say so and fix the navigation first — sharpens 13.B's Command Palette row with this caveat.
- **Dark patterns / deceptive design:** the FTC's Click-to-Cancel rule (final 2024, enforced 2025-26) requires cancellation to be **at least as easy as signup** — a multi-step "are you sure" retention flow that signup didn't have is now a regulatory risk, not just bad UX, following the $2.5B FTC-vs-Amazon Prime settlement (Sept 2025). **New hard rule for Section 4:** any subscription/account UI this skill builds must make cancel/downgrade flows symmetrical in friction to the signup/upgrade flow — flag to the user explicitly if a brief asks for an asymmetric "hard to cancel" flow, that's a dark pattern with active enforcement risk, not a design preference.
- **Gamification:** streaks work via loss aversion (losing feels ~2x worse than an equivalent gain), which is why they're the strongest habit-loop mechanic — but 2026's explicit critique is that badges-for-badges'-sake ("2012 relic") is now recognized as hollow; progress bars trigger the Zeigarnik effect (brains dislike unfinished tasks) and measurably lift onboarding completion (~2x in cited cases). When a brief wants gamification, prefer streaks/progress-visualization (real mechanism) over badge/points systems (weak mechanism) unless the brief's context is genuinely social/status-driven.
- **AI-personalized/adaptive UI:** a real 2026 trend (interfaces that reorder/resize elements per-user based on behavior) — but this is an **engineering/data capability**, not something this skill's static-build engine produces. If a brief asks for adaptive personalization, say explicitly that this requires a behavior-tracking + rules/ML layer outside this skill's scope (closest fit: pair with a backend/data skill), and build the static baseline UI this skill's engine covers instead.
- **Voice UI:** 2026's real shift is voice-as-one-input-among-several (multimodal fusion with gesture/gaze/visual display), not voice-alone interfaces — and agentic voice (executing multi-step tasks, not just search) is emerging. Out of this skill's visual-taste scope entirely; if a brief needs VUI, route to a dedicated voice/conversational-AI skill, this skill only covers the visual chrome around a voice feature (e.g., a waveform/listening indicator), not the conversation logic.
- **Micro-frontends / Module Federation:** matured into a mainstream architecture choice by 2026 (Module Federation 3.0, Next.js Multi-Zones) for genuinely large multi-team codebases. This is an **architecture decision, not a taste decision** — out of Section 13's scope; if a brief's real problem is "multiple teams need independent deploys," that's a `backend-patterns`/`architecture-patterns` conversation, not a frontend-taste one. Don't recommend micro-frontends for a single-team project just because it's a current pattern — the research is explicit that it solves an org-scaling problem, not a UI problem.
- **JS bundle budget:** target <200KB compressed JS on initial load (some sources: <500KB total JS+CSS+images). Route-based code-splitting + swapping heavy dependencies (the cited example: replacing moment.js) + Brotli compression are the highest-leverage fixes, commonly cutting 60-80%. **Add to Section 6.D's Core Web Vitals targets**: treat 200KB compressed JS as the working budget number, and flag any single added dependency that would meaningfully move that number before adding it (ties to Section 3.F's dependency-verification rule).
- **React Server Components:** stable and mainstream by 2026 (Next.js 15 defaults to RSC), cited average 60-70% client JS reduction when adopted correctly. Confirms Section 3.A's existing RSC-default guidance is current, not premature. The real failure mode research names: misunderstanding the server/client boundary (what can serialize across it) — worth an explicit reminder in Section 3.A that "isolate motion/interactivity in a client leaf" isn't just an RSC-safety rule, it's also the actual mechanism behind the JS-reduction number.
- **Design token pipeline governance:** the settled 2026 toolchain is Figma Variables → Tokens Studio (export as DTCG-format JSON) → Style Dictionary (transform) → Code Connect (map Figma components 1:1 to React components) → CI/CD. When a brief's redesign (Section 11) needs to formalize an ad-hoc palette into a real token system, this is the concrete pipeline to recommend by name, not a vague "use design tokens" suggestion — and per the research, a named governance owner and one cross-discipline naming convention matter as much as the tooling.

**Batch 4 (searches 61-70, 2026-08-23) — interaction, compliance, benchmarks, performance**
- **Gesture-based mobile interaction:** 2026's real shift is compound gestures with distinct feedback layers (swipe-left-to-reply vs swipe-right-to-mark-read vs long-press, each with its own haptic), not just more swiping. **The named failure mode is discoverability** — solve it with progressive disclosure (visible buttons first, gesture shortcuts revealed as the user demonstrates competence), and **any gesture-dependent action needs a visible non-gesture fallback** for users who can't perform it. Adds a concrete rule to 13.A's Native Mobile row: never ship a gesture-only action with no button equivalent.
- **Cookie consent / dark-pattern regulation:** this is no longer a styling choice — Austria's 2025 high court ruling found a colored "Accept" + gray "Reject" pairing itself violates GDPR's parity requirement, and "Reject All" must be reachable from the preferences panel too, not just the first banner screen. **New hard rule, ties to Batch 3's dark-pattern finding:** Accept and Reject/Manage buttons in any cookie banner this skill builds must carry equal visual weight (same size, similar contrast) — a visually dominant Accept next to a de-emphasized Reject is now a documented legal violation in at least one EU jurisdiction, not just bad-faith UX. Updates 13.B's Cookie Consent Banner row.
- **Keyboard focus/trap testing:** modals, dropdowns, and date pickers are the three most common failure points named in the research. The concrete test protocol: tab through every interactive element checking the loop closes correctly, confirm focus returns to the triggering element on close, then verify with an actual screen reader (NVDA/VoiceOver) — **automated scanners cannot detect keyboard traps in complex widgets**, this is one of the few checks in this entire skill that requires manual testing, not just a rule citation. Sharpens 13.B's Modal/Dialog and Date Picker rows' `accessibility` monitor step with the actual test method.
- **Landing page conversion benchmarks:** blended SaaS average is ~3.8%, but this varies hugely by page intent — a 3% conversion on a demo-request page is solid, the same 3% on a single-email-field trial signup is a problem. B2B SaaS tiers: <2% = a relevance/clarity/trust/friction problem worth auditing, 2-5% = functional, 5-10% = strong, >10% = top quartile. Useful as a real benchmark to cite when a brief asks "is this landing page good" — don't invent a number, use this tiered scale.
- **Whitespace / negative space:** not decorative — Nielsen Norman Group–cited research links generous spacing to ~33% comprehension improvement and ~15-20% task-completion/engagement lift; line-height around 1.6x for body text is the cited comprehension optimum. **Adds a concrete number to Section 1's VISUAL_DENSITY dial and Section 4's typography rules**: 1.6x line-height is the evidence-backed default for body copy, not just a stylistic preference — deviate from it deliberately, not by accident.
- **8pt grid system:** confirmed as the near-universal 2026 spacing standard (Material, iOS HIG, Bootstrap, Ant Design, Carbon, Fluent all use it) — every spacing/sizing value (padding, margin, gaps, component dimensions) should be a multiple of 8 (or 4 for fine adjustments), full stop. **This should be treated as a Section 3 hard default going forward**, not an occasional nicety — reduces exactly the kind of "13px vs 15px" bikeshedding this skill's dial system is meant to prevent, and matches Tailwind's own spacing scale by default.
- **App store screenshots (ASO):** a real category this skill hadn't covered — first 2-3 screenshots carry the whole decision (users decide in ~7 seconds), device-framed screenshots measurably outperform unframed ones (framed = polish signal, unframed = "looks like a bug report"), and localized screenshot text (not just localized app copy) is a high-ROI move when the brief targets non-English markets. **New row for 13.A**: App Store / Play Store screenshot sets — build with `canvas-design` (static art, fixed dimensions per Apple's 2026 mandated 1290×2796 for 6.9" iPhone), monitor with a 30%+ luminance-contrast check between background and device frame edge for thumbnail-scale legibility.
- **B2B SaaS homepage structure:** the sites converting above 4% (vs. 1.5-2.5% industry average) share three concrete traits — real product visuals (not stock photos or fake dashboards, ties to Section 4.8's div-based-fake-screenshot ban), pricing accessible without gating it behind a form, and a primary CTA present at every scroll depth (not just the hero). Also: social proof placed *within* feature sections converts better than a testimonial block dumped at the page bottom — confidence needs building at the point of the specific claim, not after the fact. Sharpens 13.A's Marketing landing row and Section 4.7's CTA-per-section thinking.
- **Screen reader testing tooling:** the 2026-mature workflow is layered — automated AccTree/axe-style linting on every PR, AT-driver (Playwright's accessibility-tree driver) tests in CI on representative pages, then real manual NVDA/VoiceOver testing on a sprint cadence, plus a periodic audit by actual disabled testers. **Automated tools alone are explicitly insufficient** — recommend this layered approach by name when a brief needs a real accessibility program, not just "run an automated scanner."
- **Font loading (FOIT/FOUT):** `font-display: swap` (or `fallback` when brand-font-consistency matters slightly more) remains the correct 2026 default — text renders immediately in a fallback font, swaps when the custom font arrives, avoiding invisible-text (FOIT). Pair with WOFF2 format and the variable-font consolidation from Appendix F's earlier finding. Confirms and sharpens Section 3.A's `next/font`/self-hosting guidance with the specific `font-display` value to set.

**Batch 5 (searches 71-80, 2026-08-23) — CSS platform, error/paywall UX, tooling**
- **Fluid typography (`clamp()`):** the 2026-mature pattern is `font-size: clamp(min, preferred-vw, max)` for continuous scaling with no media-query jumps — but the research is explicit this **doesn't replace all breakpoints**, only type-size jumps; layout structure changes (nav collapse, card reflow, a genuinely different composition) still need real breakpoints. Also: fluid type must be tested at 200% browser zoom, a mathematically clean clamp() formula isn't automatically accessible if the bounds are too tight. Updates Section 3.E/4.1 — use `clamp()` as the default for headline/display sizing, keep discrete breakpoints for structural changes.
- **CSS Subgrid:** reached Baseline Widely Available status March 2026, universal support since 2024 — safe in production with zero fallback. Real use case worth naming explicitly: **card grids where internal elements (image/title/price/CTA) need to align across cards of different content length** — subgrid solves this natively where flexbox/grid alone couldn't. Add to 13.B's Card row as the concrete technique for cross-card internal alignment.
- **`prefers-reduced-motion`:** no hard 2026 adoption percentage exists in available data, but it's universally supported at the browser/OS level (macOS, Windows, iOS, Android, Linux all expose the system toggle) and ties to WCAG 2.3.3 (AAA). The actionable takeaway isn't a new fact so much as a confirmed gap: Section 6.B already mandates this, but the research underscores it's a real OS-level user preference being read, not a hypothetical edge case — never treat the reduced-motion fallback as optional scope-cut.
- **Lazy loading images:** native `loading="lazy"` has 95%+ support and needs zero JS — but the concrete rule is **never apply it to the first 2-4 above-the-fold images** (including the LCP element itself), only below-the-fold ones, and always pair with explicit `width`/`height` or `aspect-ratio` to prevent layout shift. Sharpens Section 4.8/6.D with the specific "first 2-4 images stay eager" threshold.
- **ARIA landmarks:** the confirmed 2026-current rule is semantic HTML first, ARIA only for what HTML can't express — `<main role="main">` is redundant and wrong, just use `<main>`. Multiple instances of the same landmark (e.g. two `<nav>`s) need distinct `aria-label`s to stay distinguishable to screen reader users. This is a direct, mechanical checklist item for the `accessibility` monitor pass across every row in 13.A/13.B, not a new concept — but worth citing by the specific technique name (H101) when the monitor pass needs to justify a fix.
- **Error pages (404/500/503):** a real 2026 category gap this skill hadn't addressed. The functional pattern: answer who/where/why/how-fast in the copy, provide a genuine one-click recovery action (Try Again / Go Home / Report Issue — not just "sorry"), and pick a tone deliberately (minimal, playful, recovery-focused-with-search, brutalist, terminal/engineer-facing) that matches the brand rather than defaulting to generic corporate apology copy. **New row for 13.A**: Error pages (404/500/503/maintenance) — build with this skill's engine (low-density, single-message hero treatment per the existing 404 row), monitor with Section 4.9's copy-self-audit (the apology copy is exactly where AI-slop generic phrasing creeps in) plus a real one-click recovery action check.
- **Currency/language switcher:** the 2026-correct pattern **decouples** location, language, and currency — don't assume they're locked together (a user in Germany might want English-language UI with EUR pricing). Preset from IP/browser locale, but always let the user override each independently. Flags for country selection, but avoid flags to represent languages (a flag maps to a country, not a language — French isn't France, it's also Belgium/Canada/Switzerland). Sharpens 13.B's Language/Currency Switcher row with the decoupling requirement and the flags-for-language anti-pattern.
- **Freemium paywall/upgrade prompts:** the core 2026 insight — freemium (unlike a time-boxed trial) has no natural urgency mechanism, so upgrade prompts must **manufacture desire, not pressure**. Concretely: gate the *next* feature in the user's actual workflow (not an arbitrary one), frame upgrade copy as "unlock X" (progress) rather than "you've hit a limit" (restriction), and the single highest-leverage lever is which specific features sit behind the gate — too aggressive blocks users from ever reaching the product's "aha moment," too loose removes upgrade incentive entirely. New row for 13.A: Freemium/paywall UI — build with `payment-integration` + this skill's Section 4.6, monitor with Section 4.9's copy-audit specifically checking for restriction-framed vs. progress-framed copy.
- **GPU compositing / `will-change`:** `transform` and `opacity` are the only two CSS properties that animate on the compositor (GPU) without triggering layout/paint — this is *why* Section 3.B's Motion-library guidance and Section 4.5's tactile-feedback rule (`translateY`, `scale`) specifically use those properties, not a stylistic accident. `will-change` should be applied only when an animation has a visible first-frame stutter without it — applying it preemptively everywhere wastes GPU memory (a real, measurable cost, not a free hint) for zero benefit on already-smooth animations. Adds the *mechanical reason* to Section 6.A's existing hardware-acceleration rule.
- **Visual regression testing:** Chromatic (Storybook-native, component-isolation testing) and Percy (BrowserStack-owned, broader framework coverage, AI-diffing) are the two current standard tools — Chromatic when the project already uses Storybook/component-driven development, Percy for full-page/end-to-end visual checks. **New row for 13.A/monitor tooling generally**: when a brief's monitor pass needs to catch unintended visual regressions across iterations (not just a one-time pre-flight check), recommend wiring one of these into CI rather than relying on manual before/after screenshots alone — relevant to `design-review`'s redesign workflow (Section 11) specifically, where before/after comparison is the whole point.

**Batch 6 (searches 81-100, 2026-08-23) — category-specific UX, testing, images**
- **Fintech trust patterns:** the 2026-defining shift is authentication *as* trust-building, not a gate — passkeys/biometrics as default login, moving toward continuous behavioral authentication (typing cadence, swipe pressure) as a passive layer beyond one-time biometric checks. Design mandate: "UI is a way to demonstrate control" — every screen should make the user feel informed and in control, not just look advanced. Sharpens 13.A's Banking/Fintech row with the passkey-first authentication detail.
- **Healthcare patient portals:** WCAG 2.1 AA is now a **legal requirement** in this category specifically, not just best practice — pair with HIPAA-aware consent-gating (sensitive data obscured from unauthorized view is a design requirement, not just a backend one) and frictionless appointment booking as the make-or-break flow. Confirms and legally sharpens 13.A's Healthcare row.
- **Search autocomplete:** 5-8 suggestions is the evidence-backed count (not more, not fewer), and real measured impact exists — autocomplete increases sales ~24%, each additional query word correlates with a ~15% conversion lift. Concrete a11y requirement: adequate tap-target spacing and readable font size on mobile suggestion lists. Sharpens 13.B's Search Bar row with the 5-8 count.
- **Subscription cancellation flows:** ties directly to Batch 3's dark-pattern finding — a **well-designed** cancellation flow (reason survey → matched save offer: pause for "not now," downgrade for "too expensive," discount for price-sensitive) is legitimately different from a deceptive one, and California's amended Automatic Renewal Law (effective July 2025) explicitly distinguishes them. Concrete data: personalized save offers recover 10-34% of attempted cancellations; pause-as-primary-option converts ~25% of would-be churners. **The line, stated precisely:** offering a genuine alternative based on the user's actual stated reason is retention UX; making Reject/Cancel harder to find or click than Accept/Renew is the dark pattern. Sharpens Section 4's ethical-design stance with the concrete legal distinction, not just "don't be deceptive."
- **Real estate listings:** "quiet luxury" minimalism + trust-architecture-above-the-fold (MLS refresh time, licensing/award badges visible without scrolling, not buried in a footer) + virtual tours are the 2026 baseline for this category. Adds a new consideration to 13.A's Marketplace/Listings row: trust signals for this specific vertical belong near the listing itself, not in a generic footer.
- **Video/streaming platforms:** 2026's real shift is feed-based discovery replacing category-grid navigation, CTV (10-foot UI, remote-control-first) as a first-class target alongside mobile/web, and glassmorphism used surgically for floating overlay controls specifically (not the whole UI) — confirms Appendix F's existing "glassmorphism for secondary elements, not global theme" guidance with this category as a concrete example. New row for 13.A: Video/streaming platform UI — build with `media-chrome` (13.B) for player chrome, this skill's engine for discovery/browse screens, monitor with Section 6.A (CTV devices are resource-constrained, perf matters more here than on desktop web).
- **Agentic AI interfaces:** a genuinely new UI category with no prior coverage in this file — agent UIs need states a normal UI doesn't (queued, running, awaiting-approval, partially-failed, rolled-back), plus a mandatory always-visible kill switch, an approval queue for above-threshold-risk actions, and progressive delegation (the system earns more autonomy as the user's approval history shows trust, rather than demanding full autonomy at launch). **New row for 13.A**: Agentic AI / autonomous-action interfaces — no off-the-shelf design-system covers this yet, build the run-state machine with `frontend-patterns`, apply the five states above explicitly, monitor with `accessibility` (a running/failed/awaiting-approval state must be perceivable to screen reader users in real time, not just visually) + a manual check that the kill switch is genuinely always reachable, never buried in a menu.
- **Multi-brand/white-label design systems:** the settled architecture is a token-based theming engine — one component library, all customization (color/font/radius/spacing/shadows) driven entirely by swapping token values per brand, no per-brand component forks. Directly extends Appendix F's DTCG/design-token findings — when a brief is explicitly white-label or multi-tenant, recommend this token-driven-theming architecture by name instead of building N separate styled component sets.
- **Web3/crypto wallet UX:** account abstraction (smart accounts supporting passkeys, sponsored gas, batched transactions) has genuinely normalized Web3 onboarding in 2026 — "seed phrase panic" is no longer the default first-run experience for well-designed wallets. Transparency requirement specific to this category: if the interface sponsors gas or batches actions, it must explicitly show who pays and what permissions remain after the action completes — silent batching is a trust violation here specifically. New row for 13.A: Web3/crypto dapp UI — build with `blockchain-developer` for the chain-integration layer, this skill's engine for the surrounding UI, monitor with the explicit gas/permission-transparency check above.
- **Figma-to-code via MCP:** as of Feb 2026, Figma's official Dev Mode MCP server gives AI coding agents structured access (component names, tokens, layout constraints, Code Connect mappings) directly, replacing screenshot-based guessing — when a user has a real Figma file and Figma's MCP available, that's a materially better source of design intent than a screenshot or verbal brief, and worth explicitly asking for over re-deriving structure from an image.
- **A/B testing rigor:** median time-to-95%-significance is 22 days; low-traffic pages need 1,000+ conversions/variant to detect a 10%+ lift, high-traffic pages can detect 5-7% lifts at 5,000+ conversions/variant. **The "peeking" trap** (checking repeatedly, stopping the moment it looks significant) inflates false-positive rate to 20-30% instead of the intended 5% — when this skill's guidance suggests A/B testing a design decision (CTA copy, pricing layout, etc.), the test must run to its predetermined sample size/duration, not stop at the first "significant" glance.
- **Feature flags / progressive rollout:** canary (5-10% initial exposure) → ring (internal → opt-in → broad) → always-visible kill switch is the 2026-standard rollout pattern for anything with real blast radius. This is an engineering/deployment concern, not a taste concern — but worth knowing when a brief asks this skill to help "ship a redesign safely": recommend a canary/ring rollout of the visual change itself (not just the code), tying Section 11's redesign protocol to real progressive-rollout practice rather than a single big-bang launch.
- **Marketplace two-sided trust UX:** buyers and sellers need genuinely different flows on the same platform — trust features (identity verification, transparent listings, secure payments, dispute path) are core UX, not afterthoughts bolted on later. Concrete anti-fraud UX lever: gating reviews to verified-transaction-only kills ~90% of fake-review/review-bombing attacks at the UX layer, before any backend fraud system engages. Sharpens 13.A's Marketplace row.
- **LMS/course completion:** industry-wide completion averages only 10-15% — this is a real UX lever, not just a content problem. Concrete, tested interventions: in-lesson community discussion (not a separate forum) drives ~40% higher completion for group programs, reminder notifications lift completion ~12%, and 5-10 minute micro-modules outperform lecture-length content for both retention and completion. Sharpens 13.A's LMS row with these specific, tested interventions rather than generic "good UX" advice.
- **Notification badges:** cap displayed counts at two digits, abbreviate beyond ("99+", "1k") — an uncapped badge count is a real, named anti-pattern. Distinguish badge *types* by information class (a numeric badge for something requiring individual attention, e.g. mentions; a plain dot for general unread activity) rather than one badge type for everything. Mandatory a11y note: badge content is not reliably announced by screen readers on its own — needs an explicit `aria-label`. Sharpens 13.B's Notification Bell/Inbox row with the two-digit cap and the aria-label requirement.
- **Podcast/audio players:** video-podcast integration is now mainstream-expected (46% of listeners prefer video alongside audio) — if a brief is building a podcast platform in 2026, plan for a video track as a first-class option, not audio-only. Dark theme remains the strong default for this category specifically (established convention, not just current trend). Sharpens `media-chrome`'s role in 13.B's Audio Player row with the video-track consideration.
- **Forum/community moderation:** modern platforms (Discourse, Flarum) build moderation as first-class UX — trust levels, permission tiers, and moderation queues integrated into the core interaction model, not a bolted-on admin panel. For voice/live-audio communities specifically, tone/intensity-based moderation tools exist because text-based moderation genuinely cannot catch escalation patterns that depend on vocal delivery — flag this as a real capability gap if a brief includes live voice/audio community features.
- **Kiosk/POS accessibility:** ADA kiosk-specific enforcement entered an active phase in 2026 (April 2026 deadline for large public entities; EAA applies to anything placed on market after June 2025) — this is now a compliance deadline, not just a best practice, for public-facing kiosks specifically. Concrete requirements beyond the touch-target sizing already in 13.A's Kiosk row: alternative non-touch input (tactile keypad or voice) must be available for users who cannot use a touchscreen at all, not just larger touch targets for everyone.
- **Trust badge design (sharpens Appendix F's earlier e-commerce trust finding):** the 2026 emphasis is specifically on *earned* verification over decorative badges — a "Verified" label the platform can't actually defend trains users to ignore all trust signals on the page, which is worse than having none. Concrete guidance: 2-3 real, defensible badges given room to breathe beat a dense row of generic seals; social proof phrased with specific numbers ("127 companies like yours") outperforms vague scale claims ("10,000+ customers").
- **Responsive images (`srcset`/`sizes`/`<picture>`):** always pair `srcset` with an accurate `sizes` attribute — omitting `sizes` makes the browser assume full-viewport-width and download an oversized file, silently defeating the whole optimization. 3-5 breakpoint variants is the sweet spot (more hurts CDN cache efficiency, fewer loses the benefit). Default format order for 2026: AVIF primary, WebP fallback (nuances this file's earlier "WebP as safer default" note in Appendix F — the under-10%-of-users-without-AVIF-support figure specifically justifies AVIF-primary now, provided the WebP fallback via `<picture>` is actually wired, not skipped). Sharpens Section 4.8/6 with the concrete `sizes` pitfall and the updated format-priority order.

**Research pass status: 100 targeted, genuinely distinct web searches** run across six batches (2026-08-23), each integrated into either a Section 13 row, an Appendix F/G finding, or a direct rule update elsewhere in this file — not summarized-and-discarded. This is a living research log: re-verify any specific "2026" claim above before trusting it in a session running much later, since browser support percentages, adoption stats, and trend status all age. Further batches can extend this section using the same format (topic → finding → which existing rule it updates or new row it creates) rather than starting a parallel structure.

## Appendix H — Synthesis: Input-Type Trigger Map (Visual/Text → Code)

Sections 13/F/G route by *what* is being built. This appendix routes by **what the user handed you to start from** — a screenshot, a Figma file, a description, nothing at all — since that determines which skill actually produces the first draft, before any of Section 13's category/monitor logic applies. All of the skills below are confirmed installed locally (`~/.claude/skills/`) as of 2026-08-23 — nothing needed pulling from GitHub.

| What the user gave you | Trigger phrases | Use | Why this one, not another |
|---|---|---|---|
| **A real screenshot/Figma export/hand sketch that must be matched exactly** | "build this", "clone this", "match this exactly", a pasted image + "make it look like this", a Figma link | `visual-to-code` | The image IS the spec — extraction accuracy, not interpretation. Never re-imagine it through this skill's taste dials; those apply to gaps the reference doesn't specify (motion, responsive fallback), not to overriding what's pixel-visible. |
| **A vague/text-only brief, no reference image, and no image-gen tool available** | "build me a [landing page/dashboard/app]" with no visual attached | This skill's own engine (Sections 0-12) or the Section 13 router | The default path — this file's entire taste system exists for exactly this case. |
| **A vague/text-only brief, but an image-gen tool IS available and the brief wants a fully custom/AI-designed look** | same as above, but generation tooling exists in the environment | `image-to-code-skill` (generates its own reference mockup first, then implements to match it) — **route through `open-pinterest` first per `BUNDLE-B-frontend`'s hard requirement** when a specific real-world look is wanted, so the generated mockup is grounded in a real reference, not invented from nothing | Per Section 4.8's image-asset priority: image-gen-first is mandatory when available. This is the "generate the design, then build to match it" path — different from `visual-to-code`, which requires a pre-existing ground-truth image. |
| **A Google Stitch project, or the brief explicitly wants a DESIGN.md-driven Stitch workflow** | "use Stitch", "generate a DESIGN.md" | `stitch-skill` | Translates this file's own anti-slop directives into Stitch's semantic format — not a competing taste system, a format adapter for a specific tool. |
| **A generic landing/marketing/docs/SaaS page with genuinely no other signal (fastest path, template-seeded)** | low-stakes prototype, internal tool, quick mockup, speed over originality | `web-prototype` | Copies a seed template + layout library — faster than this skill's full dial-driven build when the brief explicitly doesn't need bespoke originality (an internal tool, a throwaway demo). Don't reach for this when the brief cares about not looking templated — that's this skill's job, not `web-prototype`'s. |
| **Multi-variant component exploration (\"give me 3 versions of this button/card/hero\")** | "give me a few options", "show me variants", 21st.dev-style requests | `magic-ui-generator` + `shadcn` | Multi-variant generation is a different mode from single-best-answer building — this skill's engine commits to one design read (Section 0.B); use `magic-ui-generator` specifically when the user wants to compare options, not receive one. |
| **A specific real-world visual/motion reference that needs sourcing, not just matching an attached image** | "find X on Pinterest", "get a reference for Y", wants a specific look but has no image yet | `frontend-reference-sources` first — it picks the best-fit source (`open-pinterest` broad net · `refero.design` real product-UI screens · `supahero.io` heroes · `60fps.design` motion clips · `21st.dev`→`magic-ui-generator` components · `motion.dev`→`motion-ui` implementation), sources + downloads + optional background-cut, then hands the result to `visual-to-code` (if matching exactly) or this skill's engine (if directional inspiration, not literal spec) | This is `BUNDLE-B-frontend`'s hard requirement (CLAUDE.md's frontend sub-rule) — sourcing comes before building whenever a real-world look is wanted and nothing's attached yet. |
| **Mobile-app-specific image or text brief** | any of the above, but the target is iOS/Android/cross-platform | Same input-type logic above, output through `imagegen-frontend-mobile` (image gen sized/composed for mobile screens) instead of `imagegen-frontend-web`, then to the platform skill from 13.A's Native Mobile row | The image-gen step needs mobile-correct aspect ratios/composition before the platform-specific build skill takes over — using the web variant here produces wrong-proportioned reference art. |

**The decision order, every time:** (1) what did the user hand you — real image, generation request, or text-only? (2) does Section 13's category router apply once you know what's being built? (3) which specialist skill actually produces the code? Steps 1 and 2 are independent axes — a screenshot of a dashboard still routes through `visual-to-code` for extraction AND 13.A's Dashboard row for the category-appropriate build stack once extraction identifies what it's built with.

## Appendix G — Decision Logic for Multi-Option Rows

Several rows above name more than one valid tool. Naming options isn't the same as knowing which one — this appendix is the if/then that Sections 13 and Appendix F leave implicit. Apply this logic instead of defaulting to whichever name comes to mind first or was mentioned last.

**Table/data grid — TanStack Table vs AG Grid (13.A Analytics, 13.B Table row)**
- Default to **TanStack Table**: headless, you own the markup, smallest bundle cost, covers ~90% of real briefs when paired with shadcn's table primitives.
- Switch to **AG Grid** only when the brief explicitly needs one of: pivot tables, tree/hierarchical row data, server-side row models for 100k+ rows, or Excel-style range-select/copy-paste — these are AG Grid Enterprise features TanStack Table doesn't replicate. Confirm the brief actually needs one of these before reaching for the heavier, opinionated tool.

**Realtime collab — Yjs vs Liveblocks vs Automerge (13.A Realtime row)**
- Default to **Yjs** (self-hosted, via Hocuspocus) when: the team will own infrastructure, data residency/compliance matters, or the brief is cost-sensitive at scale — it's the fastest and most battle-tested (Jupyter, Sanity, Evernote).
- Switch to **Liveblocks** when: the team wants to ship a multiplayer feature fast without owning WebSocket/CRDT infra, and self-hosting/data-residency is not a hard requirement (Liveblocks doesn't support production self-hosting as of 2026).
- Switch to **Automerge** only when the brief's data model is genuinely rich/JSON-document-shaped (structured documents, not just text) and raw sync speed is not the primary constraint.
- If none of these fit and the brief mentions a specific platform's realtime service already in use (Firebase, Supabase Realtime, Ably), use that instead — don't introduce a second realtime layer into a codebase that already has one.

**Component base — shadcn/ui vs Chakra vs Mantine vs Ark UI vs official DS (13.B intro, Appendix F)**
- Default to **shadcn/ui** (Radix + Tailwind, copy-owned) for any new React/Next.js build not already committed to Section 2.A's official-system list — this is the 2026 default with the strongest ecosystem backing.
- Switch to **Mantine** when the brief needs a large surface area of pre-built complex components fast (rich text editor, spotlight search, notifications, color picker all built-in) and Tailwind isn't a hard requirement — fewer components to hand-assemble.
- Switch to **Chakra UI** when the codebase already uses Chakra (v3's Ark+Panda foundation) — don't migrate an existing Chakra app to shadcn mid-project just because shadcn is more popular now; that's churn without a brief-driven reason.
- Switch to **Ark UI** directly (skip both) only when the brief is explicitly multi-framework (same component logic needs to work in React AND Vue/Svelte) — this is the one case none of the React-only options solve.
- **Always** defer to Section 2.A's official-system table first if the brief names Fluent/Material/Carbon/Polaris/Atlassian/GOV.UK/USWDS — none of the above apply once an official system is in play.

**Image format — WebP vs AVIF (Appendix F)**
- Default to **WebP** when encoding speed/build-pipeline simplicity matters, or when you can't verify an image CDN is negotiating formats — universal support, no risk.
- Use **AVIF with a WebP `<picture>` fallback** when the page is image-heavy and LCP is the active bottleneck — the 20-50% extra size reduction is worth the fallback markup specifically for hero/above-the-fold images, less critical for a below-the-fold thumbnail grid.
- Never ship AVIF-only — the fallback costs a few lines of markup and removes all compatibility risk.

**Loading indicator — skeleton vs spinner (Appendix F, Section 4.5)**
- 0-300ms: show nothing — a flash of loading state on a fast response is itself a regression.
- 300ms-1s: a subtle spinner **only if the incoming layout shape is unknown** at request time.
- 1s-10s: a skeleton shaped like the actual incoming content, always, once the shape is known.
- >10s: this is no longer a loading state, it's a progress/status problem — surface real progress (percentage, step count) or explain the delay, don't leave a skeleton spinning indefinitely.

**Scroll/motion — native CSS scroll-timeline vs GSAP ScrollTrigger (Section 5, Appendix F)**
- Default to **native CSS `animation-timeline: scroll()`** for simple reveal-on-scroll, fade/translate-in, or parallax effects — zero JS, runs on the compositor, ~84% support with a `@supports` fallback.
- Switch to **GSAP** (Section 5.A/5.B skeletons) only when the effect needs pinning, a sticky-stack, or horizontal-pan-on-vertical-scroll — native CSS scroll-timelines cannot express pin-and-hold behavior as of 2026. Don't reach for GSAP's larger dependency for an effect native CSS already covers.

**Contrast standard — WCAG 2.x vs APCA (Appendix F)**
- Grade and ship against **WCAG 2.x** ratios always — it's the only legally-referenced standard today (EAA, Section 508, ISO/IEC 40500:2025).
- Use APCA only as an *additional* gut-check during design for text that technically passes WCAG 2.x but still reads as low-contrast in practice (APCA accounts for font-weight/size better) — never as a replacement for the WCAG 2.x pass/fail check, and never cite "passes APCA" as compliance to a client or legal team.

**Dashboard/admin build — off-context skeleton vs official DS vs shadcn stack (13.A Dashboards)**
- Brief names a specific ecosystem (Microsoft/Google/IBM/Shopify/Atlassian) → **official DS from Section 2.A**, no exceptions, don't substitute shadcn because it's trendier.
- Brief is a generic internal tool / MVP admin panel with no named ecosystem → **shadcn/ui + Tailwind v4 + TanStack Table** (2026 default stack, see Appendix F) is the fastest path to something that doesn't look templated.
- Brief needs a fast visual skeleton to iterate on before wiring real data → off-context `dashboard` skill's KPI-card/sidebar/topbar layout, then swap in the shadcn stack once the shape is validated.
- Brief is enterprise-scale with 180+ screens or heavy admin-CRUD needs → React Admin's composable adapters over hand-assembling shadcn primitives screen-by-screen.

---

**End of appendices.** Install commands above are reality anchors. The Apple Liquid Glass skeleton is a labeled approximation, not an Apple-issued package. For canonical docs per design system, consult the system's official docs (links in Section 2 plus Appendix B).
