---
name: free-ugc-pipeline
description: Zero-cost UGC ad video pipeline — free keyless image generation, local TTS voiceover, Remotion compositing. Use when the user wants a UGC-style video but has no Higgsfield/Seedance/ElevenLabs credits, or wants a free-tier fallback before spending on the paid pipeline (ugc-video-auto, seedance-2). Produces a real finished MP4 (static-image + Ken Burns motion + word-timed captions + voiceover), not a talking-avatar video.
---

# Free UGC Pipeline (No-Credit Fallback)

Full zero-cost alternative to the Higgsfield/Seedance UGC pipeline. Use this
when `seedance-2` / `ugc-video-auto` aren't usable (no credits, muapi backend
missing — see Handoff Log 2026-08-18). Trades "AI talking avatar" for
"static character photo + Ken Burns motion + TikTok captions + voiceover" —
a real, shippable ad format, just not lip-synced video.

## Pipeline

```
1. Character prompt  -> ugc-hot-girl skill (reusable identity, anti-slop framework)
2. Image generation  -> Pollinations.ai (free, keyless, HTTP GET)
3. Script            -> social skill's short-form video science (hook/structure/caption rules)
4. Voiceover         -> local Voicebox server (installed once, runs at localhost:17493)
5. Compositing       -> Remotion (Ken Burns pan/zoom + word-timed TikTok captions)
```

## Step 1-2: Reusable character + free image gen

Use `ugc-hot-girl` for the prompt framework (anti-slop rules: no "perfect/
flawless/8K/hyperrealistic", always specify skin texture/pores, candid
mid-conversation energy). Build ONE fixed identity (face/hair/eyes/expression)
and reuse it across projects — only swap clothing/lighting/background per
brief. See `~/Desktop/Empire_Base/ugc_demo/brand_character.md` for the
template pattern and a worked example ("Maya").

Generate with Pollinations (no key, no signup):
```bash
ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$PROMPT")
curl -s -o character.jpg "https://image.pollinations.ai/prompt/${ENC}?width=896&height=1152&nologo=true&seed=42&model=flux"
```
Quality ceiling: decent but has visible AI tells (waxy skin, glossy eyes) —
it's a demo/placeholder tier, not a Higgsfield-Soul-2.0 replacement. Use
Higgsfield's free daily image gens instead when login is available; this is
the fallback when it isn't.

## Step 3: Script with real short-form science

Pull the actual hook/structure/caption rules from the `social` skill's
"Short-Form Video (TikTok, Reels, Shorts)" section — don't freehand a script:
- 3-second rule: visual + verbal + text hook must all land in the first second
- Pick a structure: Problem-Solution (15-30s) / List (30-60s) / Tutorial (30-60s)
- Caption rules: max 2 lines, 3-5 words/line, bold sans-serif + black outline,
  highlight key words, timing matched exactly to speech (not guessed)

## Step 4: Local voiceover (Voicebox)

Voicebox must be installed (`Voicebox_0.4.5_setup.msi`, needs admin — run via
"Run as administrator" in File Explorer, msiexec silent install fails with
error 1925 insufficient privileges). Once installed:

```bash
"/c/Program Files/Voicebox/voicebox-server.exe" &   # starts API on :17493
```

First run needs a model downloaded (`POST /models/download {"model_name":"luxtts"}`
— LuxTTS is the CPU-friendly fast option, ~1.2GB, one-time). Poll
`GET /models/status` (NOT `/models/progress/{name}`, which is an SSE stream
that burns tokens on heartbeats) until `"downloaded": true`.

Generate with `POST /generate` — response includes `word_timestamps`
(word/start/end in seconds), which feed directly into the Remotion caption
sync in Step 5. Full API surface via `GET /openapi.json` on the running server.

## Step 5: Remotion compositing

Scaffold at `~/Desktop/Empire_Base/ugc_demo/remotion/` — `Composition.tsx`
does Ken Burns (spring-eased scale, never linear per editing science) +
word-highlighted TikTok captions driven directly by Voicebox's
`word_timestamps` (not manually timed). Render:
```bash
npm install && npx remotion render src/index.ts UgcReel out/final.mp4
```

## When to use the paid pipeline instead

Once Higgsfield credits/login or the muapi backend are available, prefer
`ugc-video-auto` / `seedance-2` — genuine AI video with lip-sync beats a
static-image-plus-motion composite every time. This skill exists purely to
ship something real when the paid path isn't available.

## Related Skills
- `ugc-hot-girl` — character prompt framework
- `social` — short-form video hook/structure/caption science
- `remotion-video-creation` — deeper Remotion patterns (captions, timing, transitions)
- `ugc-video-auto`, `seedance-2` — the paid/full pipeline this is a fallback for
