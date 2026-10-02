---
name: readme-banner-design
description: Design a project/repo banner (GitHub README hero, portfolio card banner) as a small hand-written inline SVG. Use whenever asked for a "banner", "hero graphic", or "card image" for a specific software project — not for full pages/apps (route those to taste-skill instead).
---

# README / project banner design

A banner is a ~4:1 SVG (900x220 or 1200x300 both work) that has to say what one specific
project *does*, in one glance, without a screenshot. It is one of the few places a small
hand-rolled decorative SVG is the right call (taste-skill Section 4.8 flags hand-rolled SVG as
discouraged *default*, but a project banner/wordmark is its named exception).

## Check the repo first

Before drawing anything, check whether the project already has a real banner:
```
gh api repos/<owner>/<repo>/contents/.github    # banner.svg often hides here, not /assets
gh api repos/<owner>/<repo>/contents/assets
gh api repos/<owner>/<repo>/contents/README.md   # grep for ![...](path) and check every match
```
A README's own image reference is ground truth for where its banner actually lives — the
`.github/` folder is a common miss if you only check `assets/`. If a real banner exists, use it.
Never redraw one that's already good; that's the laziest and most honest source of truth for
what the project's owner actually wants representing it.

## The generic-template trap (why this skill exists)

The single easiest failure mode: draw one banner, then reuse its skeleton for every other
project by just swapping the accent color. Concretely: a radial glow + three petal-shapes
rotated 120° around a circle + title + one-line tagline, recolored per project. It reads as
one template wearing five costumes the moment two of them sit in the same grid — which is
exactly where banners get used (a portfolio's project grid, a skills page). If you catch
yourself reusing the same `<g transform="rotate(N)">` shape loop across projects, stop and
design each one from its actual mechanism instead.

## Design from the mechanism, not a mood

Before drawing, answer: what does this project actually *do*, mechanically? Then draw that:
- A router/dispatcher → a hub with labeled spokes to what it routes between (real labels, not
  generic dots).
- A protocol/bridge/API → the actual message shape (a request/response pair, real-looking
  field names) flowing between two real endpoints.
- A detector/scanner → the signal it watches plus the flag it raises, not an abstract eye icon.
- A pipeline → stages left to right, not a gear icon.
A generic "AI product" abstraction (rotating triangles, floating orbs, a glowing brain) is
the tell that the design skipped this step.

## Visual language

- **Dark background, ~4:1 aspect** (900x220 or 1200x300). Matches GitHub README dark-mode and
  most portfolio dark themes without a light/dark variant.
- **One accent color per project, not reused across the set.** If you're building banners for
  several projects in the same session, keep a running list of accents used so far and pick a
  genuinely different hue/family each time (same discipline as taste-skill's Section 4.2 color
  lock, applied per-asset instead of per-page).
- **Typography carries real weight.** A bold display title + one plain-language tagline line is
  often enough — resist stacking three lines of stat/feature copy under it, that's a card body's
  job, not a banner's.
- **Devtool/CLI projects**: lean into a terminal or DevTools-panel aesthetic (monospace type,
  real-looking protocol/command output) over abstract shapes — it's honest to what the thing is.
- **Consumer/product projects**: a labeled diagram of the actual flow beats an abstract mark.
- Avoid: purple/AI-gradient glow as a default reach (taste-skill's LILA RULE applies here too),
  Inter as the display font, a generic circular "AI eye" or "neural network dots" motif.

## Motion (optional, keep it earned)

A banner can carry a small native SVG animation (`<animate>`, `<animateMotion>`) — a packet
traveling a wire, a waveform drifting, a status dot pulsing — but it needs to represent something
real about the project (data flowing through the router it draws, a pulse it actually detects),
same "motion must be motivated" rule as taste-skill Section 5. Keep it subtle and loopable;
this asset usually sits inside a card that already has its own hover/sheen animation layered on
top in CSS, so the SVG's own motion should read as ambient, not competing for attention.

## Before shipping

- Does this banner's shape/layout differ from every other banner in the same set, not just its
  color?
- Could you swap two projects' banners and have them still make sense? If yes, they're not
  mechanism-specific enough.
- Zero em-dashes, zero "Elevate/Seamless/Unleash"-style copy (taste-skill Sections 9.G, 4.9).
- Test it scaled down to actual card width (often 200-300px wide once cropped into a grid) —
  text/pills sized for the full 900-1200px canvas can collide or become unreadable at that scale.
  Overlaid text/status pills (drawn in HTML/CSS on top of the image, not baked into the SVG) are
  especially prone to landing on top of the SVG's own title text once everything scales down —
  check that combination at real card width, not just at full size.
