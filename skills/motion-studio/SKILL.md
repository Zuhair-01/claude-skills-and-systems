---
name: motion-studio
description: Make a product or showreel motion video rendered from code (deterministic seek(t) engine, closed-form springs, beat-synced synthesized sound, self-critique loop). Use when the user asks for a launch video, showreel, product reel, animated explainer or motion ad produced from code rather than an NLE. Works from any agent (Claude Code, Codex, OpenCode) with shell access.
---

# motion-studio

The harness behind the "one prompt" motion trend. The prompt is 10% of the video;
the other 90% is this: a render engine, closed-form springs, a measured beat grid,
code-synthesized sound, and a critique loop that makes the model fix its own frames.

Project root (default): `~\Desktop\motion-studio`

## Inputs to collect first
Product + URL, duration, formats (9:16 / 1:1 / 16:9), brand colors + fonts,
a reference (frame, video or image folder), music (file or "synthesize").

## Pipeline
1. Gather assets from the URL with Playwright into `./assets`. List them.
   Never redraw product UI from imagination — crop and animate the real thing.
2. If a reference exists, write `docs/style_guide.md` from it (ffmpeg one frame / 0.5s).
3. Measure or synthesize music. `python beats.py <track> --out beats.json`.
4. Write `docs/shotlist.md` on the beat grid. Show it and wait for OK.
5. Build `index.html` with `window.seek(t)` using `lib/motion.js` springs. Follow `CLAUDE.md`/`AGENTS.md`.
6. `node render.mjs` → `node critique.mjs` → critique-pass (`prompts/06_critique_pass.txt`). 3 rounds minimum.
7. `node mix.mjs` → `out/final.mp4` at -14 LUFS. Render 9:16, 1:1 and 16:9 from the same timeline.
8. Deliver `final.mp4`, `contact.png`, `poster.png`. Say what you'd improve next.

## Hard rules
- Real product UI only. Never invent screens.
- No `Math.random`, no timers, no CSS transitions in render mode. Seeded noise only.
- Banned: corner labels, centered title on gradient, everything fading in.
- One display face, one UI face, one accent color. New thing on screen every 2-4s.
- Every move is a closed-form spring from `lib/motion.js`. A value with many targets
  uses `track()` (sum of one spring per change), never a restarted animation.

## Flagship + craft
- `films/brud-mascot.html` — a working mascot-led product reel (consistent vector mascot,
  live editor UI, counting numbers, pixel-dissolve, brand accent, post grain). Clone its
  structure for the next one; render with `render.mjs --in films/<name>.html`.
- `docs/research/MOTION_CRAFT_CATALOG.md` — read before a new film (kinetic type, 2.5D camera,
  post texture, transitions, sound, beat-sync, and the impact/effort priority table).
- `score.mjs` — synthesize a full score → `out/music.wav` (mix.mjs picks it up).

## Prompt library
`prompts/01_showreel_oneliner.txt` · `02_brand_product.txt` · `03_reference.txt` ·
`04_ui_morph_spec.xml` · `05_director_brief.txt` · `06_critique_pass.txt`

## Effort
Medium for fixes/re-renders; **xhigh** for new films; **max** when the first 3s must carry a launch.
