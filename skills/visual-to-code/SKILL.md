---
name: visual-to-code
description: Reproduce a visual reference (screenshot of a real site/app, Figma/Sketch export, hand-drawn sketch/wireframe, or a look sourced live from Pinterest) as pixel-accurate working frontend code. Use whenever the user pastes/attaches an image and says "build this", "clone this", "match this exactly", "make it look like this screenshot", gives a Figma link/export, or says "find X on Pinterest and build it exactly". Different from image-to-code-skill, which generates its OWN mockup image first — this skill starts from an image that's already ground truth (user-supplied, or sourced via open-pinterest) and extracts it rather than riffing on it.
---

# Visual → Code: Exact Reproduction

The image is the spec. Your job is extraction accuracy, not "inspired by."
Do not add flourishes the image doesn't show. Do not omit details it does show.

## 0. Get the source image

- **User already attached/pasted one** → skip to §1.
- **No image yet, user described a look** ("find a glassmorphism pricing card and build it", "get that Pinterest look and clone it") → invoke `open-pinterest` first to search, vet, and download the actual reference image(s) into the project. Use its query-intelligence step to turn the vague ask into 2-4 sharp queries, and its vetting step to reject caption-matches that are visual misses — don't hand this skill a junk pin. Once a pin is downloaded to a local file, that file becomes the ground-truth source for everything below.
- **A live URL was given instead of an image** → screenshot it yourself (Playwright/claude-in-chrome) rather than working from memory of what the site looks like.

## 1. Classify the source (changes what you can trust)

- **Screenshot of a live site/app** — pixel values are real but you can't measure them directly from a raster image. Cross-check with the actual site's DOM/computed styles if the URL is available (open it, inspect computed CSS) instead of eyeballing.
- **Figma/Sketch export** — if the user has access to the file, get exact values (spacing, hex colors, font sizes, radii) from the design tool/inspector rather than guessing from the flattened image. Ask for a Figma link/dev-mode access if only a flat PNG was shared and precision matters.
- **Hand sketch/wireframe** — no exact values exist; this is intent, not spec. Infer a clean, sensible implementation of the *structure* (layout, hierarchy, component types) and say so — don't fake false precision.
- **Pinterest-sourced pin** (via §0) — treat it exactly like a screenshot: real design, but a compressed/re-encoded JPEG, so sample colors with some tolerance and note it's a photographed/rendered reference, not a live DOM you can inspect.

Ask the user which case applies if it's ambiguous and precision matters (a wireframe vs. a real screenshot look similar when compressed).

## 2. Extract before you code

Go region by region (nav, hero, cards, footer, etc.) and pin down, in this order:

1. **Layout**: grid/flex structure, column counts, container max-width, breakpoint behavior implied by the crop
2. **Spacing**: padding/margin/gap — use the image's own repeating units as a ruler (e.g. "gap between cards ≈ half the card's internal padding") rather than absolute guesses
3. **Type**: exact visible copy (transcribe it verbatim, don't paraphrase), font family if identifiable (check for a visible brand/system-font tell), weight, size ratios between heading levels
4. **Color**: sample hex values directly from the image file where possible (via a tool call, not by eye) for backgrounds, text, accents, borders
5. **Components**: button shapes/radii, card elevation/borders, icon style, input styling
6. **States implied**: hover/active/focus cues visible (shadows, underlines) vs. states you must invent (mark these explicitly as invented)

Write this extraction down as a short spec before touching code — a bullet list is enough, not a doc.

## 3. Match the target stack — don't assume

Before picking React+Tailwind by default, check the actual project:
- Existing repo → read `package.json` / look at sibling components for the real stack (Vue, Svelte, plain HTML, styled-components, CSS modules, whatever's there). Match it.
- No existing project / greenfield → default to **React + Tailwind**.
- User explicitly asks for plain HTML/CSS → use that, framework-agnostic markup.
- When genuinely unsure and it matters, ask — don't silently pick a stack that doesn't fit the codebase.

## 4. Build, then verify visually — never claim a match unverified

1. Implement the extracted spec.
2. Render it (dev server / Playwright screenshot — see `reference_local_playwright_screenshots` memory) and place the screenshot next to the source image.
3. Diff them yourself: spacing, colors, line-wraps, alignment. Fix mismatches.
4. Only report "done"/"matches" after this side-by-side check. If you cannot render (no way to preview), say so explicitly instead of asserting a visual match you didn't verify — this is a hard rule, see `feedback_no_blind_frontend_claims` memory.

## 5. What NOT to do

- Don't invent extra sections, copy, or polish the image doesn't show.
- Don't round every image to your own "good taste" defaults (taste-skill/frontend defaults) if it conflicts with what's actually in the image — fidelity beats aesthetic opinion here. Note conflicts to the user rather than silently overriding.
- Don't guess colors "by eye" from a screenshot when you can sample the actual pixel values — the difference between eyeballed and sampled colors is exactly the kind of avoidable error this skill exists to prevent.
- Don't skip the visual-diff step (§3) even under time pressure — an unverified "looks right" is worse than saying "I built it, haven't visually confirmed yet."
