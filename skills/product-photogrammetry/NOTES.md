# Running notes — product-photogrammetry

Append findings here as real scans happen. Most-recent first. This is the "learn as you
go" log the skill's main file points to — keep entries short and concrete (what was
tried, what actually happened, what to do differently next time).

## Research pass — 2026-08-23 (before any real scan attempted yet)

- Verified real CLI command names against rshelp.capturingreality.com (List of All CLI
  Commands, Reconstruction Commands, Model Export pages) rather than guessing flag names.
- Confirmed export requires a one-time GUI export to generate a reusable params XML —
  `-exportModel`'s XML argument has no documented hand-written syntax.
- Confirmed metal/shiny connectors (every HDMI/USB shell in this catalog) need matte
  scanning spray or foot/foundation powder before capture — photogrammetry cannot
  reconstruct specular surfaces from photos alone, this is a hard physical constraint,
  not a settings tweak.
- Decided to scale meshes post-export against `products.csv`'s own verified dimensions
  rather than RealityScan's native `defineDistance` GUI tool, since that data already
  exists and is already trusted — avoids a manual step per product.
- Not yet verified: actual triangle-count/texture-size sweet spot for this specific
  object class (small cable+connector) — the 30-60k/2048px starting point in SKILL.md is
  a reasonable-sounding default, not yet confirmed against a real scan's output quality.
- Not yet verified: whether `-calculateNormalModel` quality is actually sufficient for a
  connector macro close-up, or whether `-calculateHighModel` is worth its slower cost for
  that specific component.
