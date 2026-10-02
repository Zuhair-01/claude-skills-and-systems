---
name: threejs
description: |
  Three.js skills for creating 3D elements and interactive experiences in the browser — scenes, materials, controls, and post-processing.
triggers:
  - "threejs"
  - "three.js"
  - "3d web"
  - "webgl scene"
  - "3d interactive"
od:
  mode: prototype
  category: 3d-shaders
  upstream: "https://github.com/CloudAI-X/threejs-skills"
---

# threejs

> Curated from CloudAI-X.

## What it does

Three.js skills for creating 3D elements and interactive experiences in the browser — scenes, materials, controls, and post-processing.

## Source

- Upstream: https://github.com/CloudAI-X/threejs-skills
- Category: `3d-shaders`

## Raw three.js vs Spline — pick first

- **Raw three.js / R3F** (this skill + `apex-frontend-lab`'s zero-dep WebGL patterns) — when you
  need procedural geometry, custom shaders, tight bundle control, data-driven scenes, or the 3D is
  the product. More code, full control, smallest runtime.
- **Spline** (`spline.design` — "Figma for 3D") — when a designer-built interactive scene (objects,
  materials, baked animation, hover/scroll events, physics) is faster than hand-coding, and the 3D
  is decorative/hero-level. Export = a hosted `.splinecode` URL; embed via `@splinetool/react-spline`
  or the vanilla runtime. Cost: heavier payload (lazy-load + fallback + mobile downscale are
  mandatory). Full embedding/runtime-control/perf guide = the off-context **`spline-3d-integration`**
  library skill → `python3 ~/.claude/overseer/search.py spline`.
- Either way, source the *look* first via `frontend-reference-sources` (Rule 7 frontend sub-rule).

## How to use

This catalogue entry advertises the skill in Open Design so the agent
discovers it during planning. To run the full upstream workflow with
its original assets, scripts, and references, install the upstream
bundle into your active agent's skills directory:

```bash
# Inspect the upstream README for exact paths
open https://github.com/CloudAI-X/threejs-skills
```

Then ask the agent to invoke this skill by name (`threejs`) or with
one of the trigger phrases listed in this skill's frontmatter.
