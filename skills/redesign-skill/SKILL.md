---
name: redesign-existing-projects
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
---

# Redesign Skill

> Shared rule source: "generic AI pattern" detection and the premium-quality bar this skill applies
> both live in `taste-skill` (Section 9 "AI Tells", Section 14 pre-flight checklist). Use those
> sections as the audit checklist in Step 1 below rather than re-deriving criteria.

## How This Works

When applied to an existing project, follow this sequence:

1. **Scan** — Read the codebase. Identify the framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state you find. Produce the **Audit Report** (see format below) before touching code on any project with real users or a production deploy.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.
4. **Verify** — Confirm nothing broke (see Verification below) before considering the pass done.

## Before You Start

- `git status` first. Uncommitted changes that aren't yours to touch get stashed, not overwritten.
- Confirm the project has no auto-deploy-on-push into production (check CI config, `vercel.json`, deploy hooks). If it does, treat every commit as a live production change — smaller diffs, verify locally first, ask before pushing.
- Presentation layer only. This skill changes CSS, markup structure, component styling, and client-side interaction states. It does not touch business logic, data fetching, API routes, database schema, or auth — if a "design" problem turns out to need a logic change, flag it and stop rather than drifting into a backend edit.
- Take a baseline screenshot (or short screen recording) of the pages you're about to touch, in both light and dark mode if the project has both. You can't prove "improved" without a "before."

## Design Audit

### Typography

Check for these problems and fix them:

- **Browser default fonts or Inter everywhere.** Replace with a font that has character. Good options: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. For editorial/creative projects, pair a serif header with a sans-serif body.
- **Headlines lack presence.** Increase size for display text, tighten letter-spacing, reduce line-height. Headlines should feel heavy and intentional.
- **Body text too wide.** Limit paragraph width to roughly 65 characters. Increase line-height for readability.
- **Only Regular (400) and Bold (700) weights used.** Introduce Medium (500) and SemiBold (600) for more subtle hierarchy.
- **Numbers in proportional font.** Use a monospace font or enable tabular figures (`font-variant-numeric: tabular-nums`) for data-heavy interfaces.
- **Missing letter-spacing adjustments.** Use negative tracking for large headers, positive tracking for small caps or labels.
- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps instead.
- **Orphaned words.** Single words sitting alone on the last line. Fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces

- **Pure `#000000` background.** Replace with off-black, dark charcoal, or tinted dark (`#0a0a0a`, `#121212`, or a dark navy).
- **Oversaturated accent colors.** Keep saturation below 80%. Desaturate accents so they blend with neutrals instead of screaming.
- **More than one accent color.** Pick one. Remove the rest. Consistency beats variety.
- **Mixing warm and cool grays.** Stick to one gray family. Tint all grays with a consistent hue (warm or cool, not both).
- **Purple/blue "AI gradient" aesthetic.** This is the most common AI design fingerprint. Replace with neutral bases and a single, considered accent.
- **Generic `box-shadow`.** Tint shadows to match the background hue. Use colored shadows (e.g., dark blue shadow on a blue background) instead of pure black at low opacity.
- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns to backgrounds. Pure flat vectors feel sterile.
- **Perfectly even gradients.** Break the uniformity with radial gradients, noise overlays, or mesh gradients instead of standard linear 45-degree fades.
- **Inconsistent lighting direction.** Audit all shadows to ensure they suggest a single, consistent light source.
- **Hardcoded colors instead of theme tokens.** If the project supports light/dark mode (or should), colors belong in CSS variables/tokens defined once, not scattered literal hex values — a real dark-mode pass means redefining tokens in one place, not hunting every component.
- **Dark mode that's just inverted light mode.** True dark mode needs its own contrast pass — pure white text on dark backgrounds is often too harsh; off-white (`#e8e8e8`-ish) reads better at scale.
- **Random dark sections in a light mode page (or vice versa).** A single dark-background section breaking an otherwise light page looks like a copy-paste accident. Either commit to a full dark mode or keep a consistent background tone throughout. If contrast is needed, use a slightly darker shade of the same palette — not a sudden jump to `#111` in the middle of a cream page.
- **Empty, flat sections with no visual depth.** Sections that are just text on a plain background feel unfinished. Add high-quality background imagery (blurred, overlaid, or masked), subtle patterns, or ambient gradients. Use reliable placeholder sources like `https://picsum.photos/seed/{name}/1920/1080` when real assets are not available. Experiment with background images behind hero sections, feature blocks, or CTAs — even a subtle full-width photo at low opacity adds presence.

### Layout

- **Everything centered and symmetrical.** Break symmetry with offset margins, mixed aspect ratios, or left-aligned headers over centered content.
- **Three equal card columns as feature row.** This is the most generic AI layout. Replace with a 2-column zig-zag, asymmetric grid, horizontal scroll, or masonry layout.
- **Using `height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh` to prevent layout jumping on mobile browsers (iOS Safari viewport bug).
- **Complex flexbox percentage math.** Replace with CSS Grid for reliable multi-column structures.
- **No max-width container.** Add a container constraint (around 1200-1440px) with auto margins so content doesn't stretch edge-to-edge on wide screens.
- **Cards of equal height forced by flexbox.** Allow variable heights or use masonry when content varies in length.
- **Uniform border-radius on everything.** Vary the radius: tighter on inner elements, softer on containers.
- **No overlap or depth.** Elements sit flat next to each other. Use negative margins to create layering and visual depth.
- **Symmetrical vertical padding.** Top and bottom padding are always identical. Adjust optically — bottom padding often needs to be slightly larger.
- **Dashboard always has a left sidebar.** Try top navigation, a floating command menu, or a collapsible panel instead.
- **Missing whitespace.** Double the spacing. Let the design breathe. Dense layouts work for data dashboards, not for marketing pages.
- **Buttons not bottom-aligned in card groups.** When cards have different content lengths, CTAs end up at random heights. Pin buttons to the bottom of each card so they form a clean horizontal line regardless of content above.
- **Feature lists starting at different vertical positions.** In pricing tables or comparison cards, the list of features should start at the same Y position across all columns. Use consistent spacing above the list or fixed-height title/price blocks.
- **Inconsistent vertical rhythm in side-by-side elements.** When placing cards, columns, or panels next to each other, align shared elements (titles, descriptions, prices, buttons) across all items. Misaligned baselines make the layout look broken.
- **Mathematical alignment that looks optically wrong.** Centering by the math doesn't always look centered to the eye. Icons next to text, play buttons in circles, or text in buttons often need 1-2px optical adjustments to feel right.

### Interactivity and States

- **No hover states on buttons.** Add background shift, slight scale, or translate on hover.
- **No active/pressed feedback.** Add a subtle `scale(0.98)` or `translateY(1px)` on press to simulate a physical click.
- **Instant transitions with zero duration.** Add smooth transitions (200-300ms) to all interactive elements.
- **Missing focus ring.** Ensure visible focus indicators for keyboard navigation. This is an accessibility requirement, not optional.
- **No loading states.** Replace generic circular spinners with skeleton loaders that match the layout shape.
- **No empty states.** An empty dashboard showing nothing is a missed opportunity. Design a composed "getting started" view.
- **No error states.** Add clear, inline error messages for forms. Do not use `window.alert()`.
- **Dead links.** Buttons that link to `#`. Either link to real destinations or visually disable them.
- **No indication of current page in navigation.** Style the active nav link differently so users know where they are.
- **Scroll jumping.** Anchor clicks jump instantly. Add `scroll-behavior: smooth`.
- **Animations using `top`, `left`, `width`, `height`.** Switch to `transform` and `opacity` for GPU-accelerated, smooth animation.

### Content

- **Generic names like "John Doe" or "Jane Smith".** Use diverse, realistic-sounding names.
- **Fake round numbers like `99.99%`, `50%`, `$100.00`.** Use organic, messy data: `47.2%`, `$99.00`, `+1 (312) 847-1928`.
- **Placeholder company names like "Acme Corp", "Nexus", "SmartFlow".** Invent contextual, believable brand names.
- **AI copywriting cliches.** Never use "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", or "In the world of...". Write plain, specific language.
- **Exclamation marks in success messages.** Remove them. Be confident, not loud.
- **"Oops!" error messages.** Be direct: "Connection failed. Please try again."
- **Passive voice.** Use active voice: "We couldn't save your changes" instead of "Mistakes were made."
- **All blog post dates identical.** Randomize dates to appear real.
- **Same avatar image for multiple users.** Use unique assets for every distinct person.
- **Lorem Ipsum.** Never use placeholder latin text. Write real draft copy.
- **Title Case On Every Header.** Use sentence case instead.

### Component Patterns

- **Generic card look (border + shadow + white background).** Remove the border, or use only background color, or use only spacing. Cards should exist only when elevation communicates hierarchy.
- **Always one filled button + one ghost button.** Add text links or tertiary styles to reduce visual noise.
- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, or plain text labels.
- **Accordion FAQ sections.** Use a side-by-side list, searchable help, or inline progressive disclosure.
- **3-card carousel testimonials with dots.** Replace with a masonry wall, embedded social posts, or a single rotating quote.
- **Pricing table with 3 towers.** Highlight the recommended tier with color and emphasis, not just extra height.
- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections instead of popups for simple actions.
- **Avatar circles exclusively.** Try squircles or rounded squares for a less generic look.
- **Light/dark toggle always a sun/moon switch.** Use a dropdown, system preference detection, or integrate it into settings.
- **Footer link farm with 4 columns.** Simplify. Focus on main navigational paths and legally required links.

### Accessibility

- **Contrast below WCAG AA.** Body text needs 4.5:1 against its background, large/bold text needs 3:1. Check every text/background pairing you touch, not just the obvious ones (placeholder text, disabled states, and text-on-image are the usual failures).
- **No `prefers-reduced-motion` handling.** Any scroll-driven, parallax, or auto-playing animation needs a reduced-motion fallback (`@media (prefers-reduced-motion: reduce)` — disable or drastically shorten motion, don't just slow it down).
- **Interactive elements smaller than 24x24px with no padding.** Icon-only buttons need a real hit target, not just a visually small icon.
- **Color as the only signal.** Error/success/warning states that rely purely on red/green need an icon or text label too (color-blind users, and it reads faster anyway).
- **Missing landmark roles or heading hierarchy skips.** One `<h1>` per page, no skipping from `<h2>` to `<h4>`.

### Responsiveness & Touch

- **Desktop-first with breakpoints bolted on.** Verify the actual mobile viewport (not just a shrunk browser window) — check `100vw` overflow from unaccounted scrollbars, fixed-width elements, and text that doesn't wrap.
- **Touch targets under 44x44px.** Apple/Google's minimum for anything tappable — buttons, nav items, form controls.
- **No safe-area handling on mobile.** Fixed headers/footers need `env(safe-area-inset-*)` padding so they don't collide with notches/home indicators.
- **Hover-only interactions with no touch equivalent.** Tooltips, dropdown reveals, and hover-to-show actions need a tap-triggered fallback on touch devices.

### Performance

- **Web fonts blocking render.** Use `font-display: swap` and preload the critical font file; don't let typography choices tank First Contentful Paint.
- **Images with no explicit width/height (or `aspect-ratio`).** This is the #1 cause of layout shift (CLS) — every image needs its dimensions reserved before it loads.
- **Unoptimized image formats.** Prefer WebP/AVIF with a fallback; use the framework's image component (e.g. `next/image`) instead of a raw `<img>` when one is available.
- **Below-the-fold images loading eagerly.** Lazy-load anything not in the initial viewport (`loading="lazy"`, or the framework's built-in equivalent).

### Iconography

- **Lucide or Feather icons exclusively.** These are the "default" AI icon choice. Use Phosphor, Heroicons, or a custom set for differentiation.
- **Rocketship for "Launch", shield for "Security".** Replace cliche metaphors with less obvious icons (bolt, fingerprint, spark, vault).
- **Inconsistent stroke widths across icons.** Audit all icons and standardize to one stroke weight.
- **Missing favicon.** Always include a branded favicon.
- **Stock "diverse team" photos.** Use real team photos, candid shots, or a consistent illustration style instead of uncanny stock imagery.

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Inline styles mixed with CSS classes.** Move all styling to the project's styling system.
- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `em`, `max-width`) for flexible layouts.
- **Missing alt text on images.** Describe image content for screen readers. Never leave `alt=""` or `alt="image"` on meaningful images.
- **Arbitrary z-index values like `9999`.** Establish a clean z-index scale in the theme/variables.
- **Commented-out dead code.** Remove all debug artifacts before shipping.
- **Import hallucinations.** Check that every import actually exists in `package.json` or the project dependencies.
- **Missing meta tags.** Add proper `<title>`, `description`, `og:image`, and social sharing meta tags.

### Strategic Omissions (What AI Typically Forgets)

- **No legal links.** Add privacy policy and terms of service links in the footer.
- **No "back" navigation.** Dead ends in user flows. Every page needs a way back.
- **No custom 404 page.** Design a helpful, branded "page not found" experience.
- **No form validation.** Add client-side validation for emails, required fields, and format checks.
- **No "skip to content" link.** Essential for keyboard users. Add a hidden skip-link.
- **No cookie consent.** If required by jurisdiction, add a compliant consent banner.

## Upgrade Techniques

When upgrading a project, pull from these high-impact techniques to replace generic patterns:

### Typography Upgrades
- **Variable font animation.** Interpolate weight or width on scroll or hover for text that feels alive.
- **Outlined-to-fill transitions.** Text starts as a stroke outline and fills with color on scroll entry or interaction.
- **Text mask reveals.** Large typography acting as a window to video or animated imagery behind it.

### Layout Upgrades
- **Broken grid / asymmetry.** Elements that deliberately ignore column structure — overlapping, bleeding off-screen, or offset with calculated randomness.
- **Whitespace maximization.** Aggressive use of negative space to force focus on a single element.
- **Parallax card stacks.** Sections that stick and physically stack over each other during scroll.
- **Split-screen scroll.** Two halves of the screen sliding in opposite directions.

### Motion Upgrades
- **Smooth scroll with inertia.** Decouple scrolling from browser defaults for a heavier, cinematic feel.
- **Staggered entry.** Elements cascade in with slight delays, combining Y-axis translation with opacity fade. Never mount everything at once.
- **Spring physics.** Replace linear easing with spring-based motion for a natural, weighty feel on all interactive elements.
- **Scroll-driven reveals.** Content entering through expanding masks, wipes, or draw-on SVG paths tied to scroll progress.

### Surface Upgrades
- **True glassmorphism.** Go beyond `backdrop-filter: blur`. Add a 1px inner border and a subtle inner shadow to simulate edge refraction.
- **Spotlight borders.** Card borders that illuminate dynamically under the cursor.
- **Grain and noise overlays.** A fixed, pointer-events-none overlay with subtle noise to break digital flatness.
- **Colored, tinted shadows.** Shadows that carry the hue of the background rather than using generic black.

## Fix Priority

Apply changes in this order for maximum visual impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Verification

Before calling a pass done:

1. **Load it in a real browser** (use the `run` skill if this project has one, or start the dev server directly) and click through the pages you touched — a diff that only passed `tsc`/build is not verified, it's untested.
2. **Compare against the baseline screenshot.** Confirm the change is actually visible and is the change you intended.
3. **Check the browser console for new errors/warnings.** A visual improvement that throws a hydration mismatch or a missing-key warning is a regression, not a win.
4. **Re-test the interactive states you touched** — hover, focus, active, loading, error, empty — don't just eyeball the static layout.
5. **If the project has a test suite, run it.** CSS/markup changes can still break selector-dependent tests (`data-testid`, class-based queries) or snapshot tests.
6. **Diff review before committing.** Read the actual changed lines — confirm nothing outside the presentation layer got touched, and nothing was deleted that shouldn't have been.

## Audit Report Format

For any project with real users or a live deploy, produce this before making changes, so scope is agreed before code moves:

```
## Redesign Audit — <project name>

**Stack:** <framework, styling method, version>
**Scope of this pass:** <pages/components in scope — be explicit about what's NOT included>

### Findings (ranked by impact, cheapest fix first)
1. [Typography] <finding> → <fix> — risk: low/med/high
2. [Color] <finding> → <fix> — risk: low/med/high
...

### Out of scope / flagged, not fixed
- <anything that looked like a design problem but was actually a logic/data issue>
```

## Rules

- Work with the existing tech stack. Do not migrate frameworks or styling libraries.
- Do not break existing functionality. Verify after every change (see Verification above), not just "test."
- Before importing any new library, check the project's dependency file first.
- If the project uses Tailwind, check the version (v3 vs v4) before modifying config.
- If the project has no framework, use vanilla CSS.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
- On a production project with no staging gate (auto-deploy on push), never push without showing the diff and getting explicit confirmation first — the "redesign" and the "deploy" are two separate decisions.
