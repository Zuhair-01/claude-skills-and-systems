---
name: veo-flow-free-video-gen
description: Generate realistic, non-slop AI product/technical video using free tools (Google Flow/Veo 3.1, and other free video-gen sites) with researched, physics-grounded prompts. Use when a project needs a real product-photography-style video asset instead of a hand-drawn illustration, and wants it to look like a real camera shot it — not generic "AI cinematic" output. Covers prompt engineering principles, a universal package→hero→branch→technical shot architecture (separate branches for cables, HDMI/display cables, extenders/active devices, connectors/adapters, splitters/hubs, PoE devices), sourcing the free tool itself, and wiring a generated video into a scroll-driven site.
---

# AI Video Prompt Engineering (free tools, no-slop)

**Origin:** built 2026-08-22 working the alwazour cable-coil hero — the
previous hand-drawn SVG rebuild was rejected, a first quick Veo prompt
("photorealistic product photography...") produced a genuinely good result
on the first try, then ChatGPT (researched, cited real sources) gave a far
more rigorous methodology. Both halves are captured here. Reusable on any
project, not alwazour-specific.

## Per-product workflow — research before prompting, every time

Don't jump straight to prompt-writing for a new cable/device. Each product
needs its own short research pass first, because construction genuinely
differs by SKU (principle 8) — skipping this is how a shot ends up implying
a shield the product doesn't have, or a pin layout that's wrong for the
actual connector standard:

1. **Pull the real record** — `technicalData.specs` (confirmed only,
   `isConfirmed()`), `connectors[]`, `ports[]` from the product's own data.
   This also gives you `resolveVisualType()`, which picks the branch (table
   above) — don't re-derive category by eye.
2. **Fill the gaps from real public standards, not memory** — if the record
   confirms "HDMI cable" but not pin-out, the HDMI pin layout is a public
   connector-standard spec (same for USB-C, RJ45 T568B, etc.) — look it up
   and cite the source rather than let the model guess. If a detail isn't
   in the product record *and* isn't a public standard (e.g. this specific
   SKU's actual shield type), leave it out of the prompt — never fabricate
   at the product level even when a category-level standard exists for
   part of the shot.
3. **Source the physical look** — Step 0 below (`open-pinterest`), grounded
   in the real construction from steps 1-2, not a generic "cable macro"
   search.
4. **Write the branch's prompt sequence** using the 9 principles + the
   confirmed facts from steps 1-2 + the visual reference from step 3.
5. **Log what was generic vs. sourced** — if any shot ended up representative
   rather than SKU-specific (no confirmed data for that layer), that's the
   caption/honesty-rule case in the closing section of this skill, decide
   it now rather than after the video ships.

## Step 0 — source a real reference before writing any prompt

Per the standing frontend rule (CLAUDE.md Rule 7): any visual/motion task
with a specific real-world look required routes through the `open-pinterest`
skill first, and a product-photography video sequence is exactly that case.
Before drafting prompts for a new branch (below) or a product type this
skill hasn't shot yet, pull 2-4 real reference pins — actual macro cable
photography, actual connector-pin cutaway shots, actual PCB macro photos —
and ground the physical-detail language in what the reference actually
shows, not in what the model "knows" a category looks like. `open-pinterest`
also downloads motion/video pins directly, useful for matching a specific
camera-move style (dolly speed, grazing-light angle) rather than describing
it from imagination. Skip this step only when a first-shot output from a
close-enough prior prompt already exists to chain from (principle 7 below).

## The core lesson: physical truth beats cinematic adjectives

The failure mode isn't missing the word "photorealistic" — that word alone
doesn't control geometry. The fix is describing the **physical object and
what it's physically doing**, not the mood you want the viewer to feel.

| Bad (slop-prone) | Good (physics-grounded) |
|---|---|
| "Beautiful realistic cable macro shot" | "Four paired helices, eight insulated conductors, 23 AWG solid bare copper, polyethylene insulation, real extrusion marks, conductors maintaining mechanical contact" |
| "Camera dramatically moves around the product" | "6 cm dolly forward, locked composition, no orbit" |
| "Realistic metal" | "Thin aluminum-polymer foil, slightly wrinkled, overlapping edge, directional reflections that change with camera movement" |
| "Realistic plastic" | "Extruded PVC/LSZH jacket, satin surface, faint longitudinal extrusion marks, subtle particulate imperfections" |

## The 9 principles

1. **Define physical truth before cinematic language.** Name the real
   materials, counts, and construction before any mood word.
2. **Give the camera something physically possible to do.** "6cm dolly
   forward" not "camera dramatically moves around the product" — vague
   camera language gives the model license to invent impossible motion.
3. **Give every material a physical signature** — how it specifically
   reflects light, wrinkles, wears, or catches dust. Generic "realistic
   X" is exactly what produces generic AI texture.
4. **Describe gravity and contact.** "Loops press against one another",
   "the cable bends where it contacts the opening", "the stripped jacket
   remains mechanically attached" — these are real constraints the model
   can follow, not decoration.
5. **Avoid cinematic overload.** Don't stack `anamorphic + epic + dreamy +
   volumetric + dramatic + hyperreal + surreal` — for a technical/product
   shot that combination is precisely how you get generic AI-commercial
   garbage. Use `controlled studio light + macro optics + physically
   accurate materials + restrained movement` instead.
6. **One shot = one physical action.** A clip that simultaneously cuts,
   unwraps, rotates, explodes and reassembles the subject will not read as
   real. Each clip does exactly one thing.
7. **Consistency beats prompt cleverness across a sequence.** One real
   reference image/first-shot output, then image-to-video / reference
   ("ingredients") workflows for the rest of the sequence, beats
   re-describing the same object from scratch every time and hoping it
   matches.
8. **Treat dimensions and construction as database truth, not model
   knowledge — never let the model "know what X looks like."** Real
   products vary by manufacturer (e.g. Cat6 cable AWG, shield type, and
   diameter differ materially between CommScope/Leviton/Belden — there is
   no universal "Cat6" look). Pull real specs from the actual product
   record and compile the prompt from them. If a spec is unconfirmed,
   omit that detail rather than let the model invent it — the same
   never-fabricate rule that governs the rest of a real product catalog
   applies here.
9. **Always include explicit negative constraints**, tuned to the actual
   failure modes of the shot: not CGI/not 3D render, no morphing, no
   floating components, no material appearing/disappearing, no watermark,
   no invented text/labels/logos, no impossible geometry for THIS subject
   specifically (e.g. "no self-intersection" for a coiled cable, "no
   impossible braid geometry" for a shield close-up).

## Universal shot architecture: constant frame + product-type branch

The full story (constant on every product):

```
PACKAGE → UNVEILING → PRODUCT HERO → WHAT IS THIS?
   → PHYSICAL INSPECTION → [ product-type branch, below ]
   → HOW IT WORKS → TECHNICAL DETAILS → FINAL HERO
```

Only the middle changes. Don't force the cable workflow (jacket → twisted
pairs → conductor → cross-section) onto a device that isn't a cable —
pick the branch that matches the real product category, which is the
**same category `alwazour-product-visualization`'s `resolveVisualType()`
already computes** — no separate classification step needed, reuse it:

| `resolveVisualType()` result | Branch | Sequence |
|---|---|---|
| `cable` (network/AV bulk cable) | **A — Ethernet/AV cable** | full coil → jacket macro → cut open → internal pairs/shielding *(only if the real SKU has it)* → conductor macro → cross-section → technical overlay |
| `cable`/`connector` (HDMI/display cable) | **B — HDMI/display cable** | full cable → connector hero → pin-array macro cutaway → internal conductors → technical overlay → source→cable→display signal graphic |
| `extender`/`switch` (active device) | **C — extender/adapter/active device** | device hero → input port macro → output port macro → engineering-cutaway PCB reveal → input→processing→output flow graphic → performance graph (bandwidth/latency/distance) |
| `connector` (bare adapter, no cable body) | **D — connector/adapter** | package → full adapter → input connector macro → internal contacts (cutaway, only if referenced) → output connector macro → compatibility graphic |
| `extender`/`switch` (multi-port routing device) | **E — splitter/switch/hub** | device hero → each port macro in turn → internal routing cutaway → 1→N signal-routing graphic → performance graph |
| `extender`/`switch` (PoE/powered device) | **F — PoE/power/active network device** | device hero → power-input macro → network-port macro → internal power/signal-path cutaway → output → power+signal technical graph |

Branches C, E, F share one `resolveVisualType()` bucket (`extender`/`switch`)
— pick among them by what the product's real `ports[]`/`technicalData`
actually describes (multiple identical outputs → E; a `power` role port →
F; single in/single out → C), the same distinction `deviceStory()` already
makes when it lists port roles.

**Shared rules across every branch:**
- Never invent a construction layer, pin count, or spec a shot implies —
  if the real SKU has no shielding, skip that shot rather than generate a
  generic one (principle 8).
- The **last physical-photography frame before the technical section**
  becomes the frozen background plate; all labels/graphs render as
  separate HTML/SVG overlay (§ below), never as text baked into the Veo
  output (Veo is bad at exact text and can't be corrected per-SKU later).
- Layer discipline — three separate layers, don't force one shot to do a
  second layer's job: **cinematic footage** (package/hero/macro/cutaway
  photography) → **technical graphics** (port labels, pin names, signal-
  flow diagrams, dimension callouts) → **data visualization** (bandwidth/
  distance/latency/attenuation graphs, real numbers only). Branch C/E/F's
  performance graph is data-viz, not a Veo shot — see the `dataviz` skill
  for that layer, not this one.

Full worked example (Cat6 Ethernet cable, Branch A, all 8 prompts verbatim,
sourced 2026-08-22): see `references/cat6-example-prompts.md` in this skill
folder. Branches B–F don't have worked examples yet — write them using
Step 0 (source a real reference first) + the 9 principles above, and add
the finished prompt set back into `references/` once validated so the next
product in that branch doesn't start from zero.

## Sourcing: free tools, no paid API required

**Google Flow** (`labs.google/fx/tools/flow`) — free tier ("Free of Charge",
no Google AI subscription) gives Veo 3.1-Lite video generation, no credit
card. Sign in with an existing Google account already authenticated in the
browser (never create a new account or enter a password for this — that's
a hard boundary regardless of task). Flow:
- **Get started → Free of Charge** on the pricing tier (scroll the landing page, click **Get started**, sign in).
- **New project** → prompt box → click the model chip to open settings: **Image** vs **Video** tab, aspect ratio (16:9 / 9:16 / 1:1 / 4:3 / 3:4 depending on model), model version, and **quantity** (x1–x4 — quantity directly multiplies credit cost, e.g. x1 = 10 credits, x2 = 20 credits on Veo 3.1-Lite 720p).
- **Check the credit cost shown before generating** ("Generating will use N credits") and generate **x1 at a time** while iterating on a prompt — free-tier credits are a real limited pool, don't burn them on quantity before the prompt itself is validated.
- Click the play icon on a finished generation to open the editor, then the **download icon** (top bar) to save the file locally.
- **Multiple free accounts to stretch the credit pool:** each Google
  account gets its own separate Flow free-tier allowance, so switching
  between several accounts you actually own (already-authenticated in the
  browser, never create new ones for this) is a legitimate way to spread a
  large shot list across more free credits instead of hitting one
  account's cap mid-branch. Track which account generated which shot in
  the project's own notes — mixing partial sequences from different
  accounts is fine since each shot is independent, but don't lose track of
  which account holds which download.

### Other free/alt tools — checked 2026-08-22, capability notes

- **`vibes.ai`** (Meta) — image + video generation, restyling, lip-sync to
  music, and a Flow-like "ingredients" system: turn any reference
  image/video into a reusable style/character/object token for consistency
  across a sequence — directly useful for the frame-chaining continuity
  this skill's shot sequence needs. Hard login wall (Meta account) past the
  landing page; no pricing/credit info visible pre-login. Untested past
  that point.
- **`chat.qwen.ai`** (Qwen Studio, Alibaba) — the `+` menu has a **Create
  Video** option, but it's greyed out/disabled while logged out (**Create
  Image** works logged out, video doesn't). Underlying video model is
  presumably Alibaba's Wan family. Requires sign-up to reach video gen at
  all — no pricing seen pre-login.
- **`snapgen.ai/veo`** — third-party Veo 3.1 Fast wrapper, **not** Google
  directly. Despite the page title ("Free Veo 3.1 AI Video Generator") and
  "free unlimited" framing, the actual pricing banner reads "Unlimited
  Video Generation — $20/month" (Pro Studio tier) — this is a paid reseller
  with some limited free trial generations, not a genuinely free option.
  Default spec shown: 16:9, 720p, 8s, first-frame image input supported.
  Deprioritize vs. Flow's real free tier unless the $20/mo tier is worth it.
- **`arena.ai/video`** (formerly LMArena) — free, no login needed to
  generate once. Only **Battle Mode** works for video: two *anonymous*
  models generate from the same prompt and you pick the better one — no
  way to target a specific named model (Side-by-side / Direct modes are
  explicitly disabled for video). Good for blind-testing a prompt's
  quality across whatever frontier models are in rotation before
  committing Flow credits to it; not a way to reliably get Veo output.
  2,500-char prompt cap.
- **`huggingface.co/spaces?category=video-generation`** — real spaces
  confirmed live: **Wan2.2 14B** (text/image-to-video), **MiniMax H3
  Turbo/Ultra** (video **with synchronized audio** — notable, most free
  options are silent), **LTX-2.5 / LTX-2.3** (fast distilled text/image-
  to-video, CivitAI LoRA integration), **Omni Video** (text-to-video +
  video extension). Typically no login, but slower/variable quality on
  shared free GPU queues — treat as a fallback tier, not a first choice.
- **`canva.com/ai/thread`** — hard login wall, redirects straight to the
  Canva sign-in page before showing any content. Not usable without a full
  Canva account; skip unless already signed in there for other reasons.

**Using ChatGPT (or another strong LLM) as the prompt-engineering step
itself** is a real, worthwhile part of this workflow — not a shortcut
around it. Ask it to research the actual generation model's own prompting
guidance (Veo has published prompting docs) and to ground any technical
claims (materials, dimensions, construction) rather than write generically
"impressive"-sounding prompts. The example prompts in this skill were
produced exactly that way, with citations back to manufacturer datasheets.

## Wiring a generated video into a scroll-driven site

If the target site drives motion off scroll progress (a `--p` custom
property from an IntersectionObserver, the pattern this skill's alwazour
origin project uses — see that project's `src/site/motion.ts`), a plain
autoplaying `<video>` loop breaks the "scroll tells the story" feel the
rest of the page has. Scrub the video's playback position to scroll
progress instead:

```js
const video = document.querySelector('.hero-video');
video.pause(); // never let it free-run
// inside the same rAF loop / --p update the scene driver already runs:
video.currentTime = p * video.duration; // p is the scene's 0..1 progress
```

Requirements this implies:
- The video element needs `preload="auto"` and `playsinline muted` (scrubbing requires the browser to have decoded frames available; muted+playsinline avoids autoplay-policy blocks on frame seeks).
- Seeking every rAF tick can be expensive on long/high-res video — keep the
  clip short (the 8-second-per-shot convention above) and no higher
  resolution than the container actually renders at.
- Respect `prefers-reduced-motion` exactly like every other scene element:
  pin `video.currentTime` to its resolved end state (or a single
  representative frame) instead of scrubbing, matching the site's existing
  reduced-motion contract — do not let a scroll-scrubbed video be the one
  element that ignores it.
- A poster frame (a real extracted frame, not a separate generated image)
  keeps the layout stable before the video's own data has loaded.

## Honesty rules carried over from the source project (apply generally)

- Never invent a spec, dimension, or construction detail a generated video
  implies — if shot 8's callouts can't be sourced from a real datasheet,
  ship shots 1–7 without it rather than inventing numbers.
- If a generic/representative asset (not claiming to depict one exact real
  SKU) is being used as a shared fallback across many products, caption it
  as such — the same pattern as an "illustrative, not a photo of this
  exact unit" note used elsewhere for hand-drawn diagrams.
- A generated video is still subject to the same license/ownership
  questions as any other asset before shipping it on a commercial site —
  confirm the generation tool's ToS permits commercial use of its outputs
  (Google Flow's free tier terms should be checked before shipping to
  production, not assumed).
