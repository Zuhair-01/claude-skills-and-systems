---
name: no-ai-slop-visuals
description: Write prompts for AI image/video generation (Qwen, Gemini, Seedance, etc.) that produce results indistinguishable from real photography/footage — not the generic over-smooth, over-symmetric, "AI-generated" look. Use whenever generating a photo or video meant to pass as real (marketing content, social posts, UGC-style clips), before writing the actual prompt.
---

# No-AI-Slop Visuals

Most AI image/video generators default to a recognizable "AI look" unless the
prompt actively fights it: too-smooth skin, too-perfect symmetry, over-lit
scenes, generic bokeh, that plastic HDR sheen, motion that's too fluid to be
real. This skill is the prompt-writing checklist that avoids it — the actual
generation runs through `web-imagegen` (Qwen/Gemini, see that tool) or
whichever generator the task calls for.

## The tell-tale AI-slop patterns to actively avoid

- **Buzzword stacking with no specificity**: "hyper-detailed, 8k, trending on
  artstation, masterpiece, ultra realistic" — these are dead giveaways in the
  prompt AND bias the model toward the over-rendered look. Delete all of them.
- **Perfect symmetry / perfect lighting** — real photos have uneven light,
  off-center framing, a slightly awkward angle. A studio-perfect 3-point-lit
  face reads as generated.
- **Skin/surface over-smoothing** — always explicitly counter this: "visible
  skin texture, pores, natural imperfections", "worn/weathered surface, not
  pristine."
- **Generic "cinematic" with nothing concrete backing it** — "cinematic
  lighting" alone is a slop-trigger phrase at this point (every slop image
  claims it). Replace with a real technical specification: a named lens
  (35mm/50mm), a real lighting setup (single window light, one desk lamp,
  overcast daylight), a specific film stock or color-grade feel (Kodak
  Portra warmth, slightly underexposed).
- **Motion that's too smooth (video specifically)** — AI video defaults to
  glide-cam-perfect motion, warping/morphing at the edges of moving objects,
  and background elements that don't obey real physics (flags/hair moving
  wrong, reflections not matching). Counter with: "handheld camera, slight
  natural shake", "real-world physics, no morphing", specific real camera
  movement (a slow push-in, a static tripod shot) rather than vague
  "dynamic camera."
- **The plastic/HDR sheen** — counter with "unedited photo, natural color,
  no HDR, no over-processing", or reference a specific real photography style
  (photojournalism, documentary, candid smartphone photo).

## Human figures specifically — where generators fail hardest

(Research-backed tells, 2026 — [Ender Tech](https://endertech.com/blog/6-ways-to-identify-ai-generated-images-with-examples), [Which One Is AI](https://whichoneis.ai/blog/how-to-spot-ai-generated-images), [Faux Lens](https://fauxlens.com/blog/5-signs-of-ai-images), [Eyesift](https://www.eyesift.com/blog/how-to-spot-ai-images-2026/), [Imagera](https://imagera.ai/blog/is-this-ai-generated-how-to-tell-2026))

These are the actual failure points to counter in the prompt, not just
"realistic" as a word:

- **Hands are the single biggest tell.** Models still get finger count,
  merged fingers, wrong thumb placement, and unnatural knuckle bends wrong
  constantly — and when a hand holds an object, it often floats next to it
  or melts into it instead of gripping it. Counter: keep hands out of frame
  or partially obscured where the composition allows (pocket, behind an
  object, motion-blurred), or if hands must be visible and holding
  something, say so explicitly ("hand naturally gripping the pen, visible
  finger pressure") and inspect the output before shipping — this is the one
  category worth a manual check every time.
- **Eyes**: mismatched pupil size, irises with an unnaturally uniform
  pattern, a too-symmetric/centered gaze. Counter: specify a natural,
  slightly off-camera gaze or genuine asymmetry ("looking slightly past the
  camera, natural asymmetric expression") rather than a straight-on stare.
- **Teeth**: AI defaults to a single uniform white block instead of
  individual teeth. Counter: a closed-mouth or slight expression avoids this
  entirely — don't prompt a big open smile unless the brief needs it.
- **Skin**: the airbrushed/plastic look is the single most common tell after
  hands. Always state it explicitly: "visible skin texture, natural pores,
  slight asymmetry, unretouched" — never leave skin unspecified, the default
  is over-smoothed.
- **Hair**: strands that merge into smooth clumps instead of individual
  hairs, especially at the hairline and flyaways. Counter: "individual hair
  strands visible, a few flyaways, natural hairline" if hair is prominent in
  frame.
- **Background/architecture**: AI backgrounds can defy physics at a glance —
  stairs leading nowhere, warped text on signs, windows at impossible
  angles, objects blending into each other. Keep the background simple and
  plausible, or specify a real, ordinary environment rather than an
  elaborate constructed scene the model has to reason through.

**Practical rule**: if the figure is a secondary/background element, none of
this needs much attention. If a human is the *subject* (a face close-up, a
hand holding the product, a visible full-body pose), budget the prompt
specifically for hands + skin + eyes — those three cover most of what reads
as "off" at a glance, even before teeth/hair get noticed.

## What to specify instead (the actual recipe)

1. **Frame it as a real photography/videography genre**, not "an image of X":
   editorial photograph, documentary photo, candid smartphone shot, security
   camera still, home-video clip, photojournalism — each genre carries its
   own real-world imperfection signature the model will lean into.
2. **Name a real camera/lens/shot type**: 35mm f/1.8 shallow depth of field,
   wide-angle security cam distortion, handheld vertical phone video —
   forces the model away from its default "clean render" mode.
3. **Add at least one deliberate imperfection**: uneven lighting, a slightly
   messy background, motion blur on a moving element, a worn/lived-in
   surface, natural skin texture. Perfection is the tell.
4. **Be scene-specific, not generic** — the exact setting, the exact object
   in frame, real cultural/environmental detail (a specific room type, real
   local objects/clutter) does more to sell "real" than any quality buzzword
   ever will. This is also what makes web-imagegen beat Pinterest sourcing
   for brand work: the scene can be exactly what the brief needs, not just
   close enough.
5. **Say explicitly what NOT to include**: no text overlay, no logo, no
   watermark (crop the platform's own watermark after — see `web-imagegen`),
   no obvious CGI/render feel.

## Honest finding (2026-09-12): negative/technical instructions alone are not enough

Tested "handheld smartphone video... static tripod-adjacent shot with slight natural shake,
overcast daylight... no slow motion, no color grading, home-video quality" on Qwen video (a
puppy in leaves). Result: still read as obvious AI slop — oversaturated color, glossy
over-rendered fur, unnaturally symmetric floating leaves. The model has a strong default
stylization bias that a list of "don't do X" instructions does not reliably override.

**What this means in practice**: don't trust a prompt just because it follows this checklist's
word-level recipe — always render a frame/still and actually look at it (oversaturation, glossy/
plastic surfaces, physics-defying motion of small objects like leaves/hair/fabric) before calling
a result usable. If the model keeps defaulting to its stylized look, the more reliable lever is
the **scene/subject choice itself**, not more negative instructions: real documented human
subjects in real specific settings (the Ostazi tutoring photo, which worked) generate more
convincingly than generic "impressive nature/animal footage" style prompts, which is exactly the
territory stock-AI-content lives in and where these models are tuned to look most "impressive"
(= most slop). Prefer mundane, specific, human-context scenes over anything that reads as a
nature-documentary or stock-footage moment.

## Video-specific additions

- Prefer **short, single-action prompts** over multi-beat scene descriptions
  — the model tracks one clear action per shot far more believably than a
  sequence of events.
- State the **camera behavior explicitly**: static tripod / slow handheld
  push-in / natural pan — never leave it to the model's default (which tends
  toward an unrealistically smooth glide).
- Expect current web-tool video gen (Qwen) to run **image-to-video**
  underneath even when using the direct "Create Video" text-to-video mode —
  which means the same anti-slop rules for images apply first: a slop-looking
  source image produces a slop-looking video. Get the still right first.

## Worked example (Ostazi carousel via `web-imagegen`/Qwen, verified 2026-09-12)

Non-Higgsfield route. Do NOT copy its "warm desk lamp" / "shallow depth of field" wording into a
Higgsfield `soul_2`/`seedance_2_5` prompt — see the correction section above.

Slop version (avoid): *"a student studying, cinematic lighting, hyper
detailed, 8k"* → generic, over-lit, could be any stock photo site.

Actual prompt used, and it worked:
> "editorial documentary photograph, candid moment: a Syrian teenage student
> sitting at a wooden desk in a modest Damascus apartment bedroom late
> evening, warm single desk lamp casting soft directional light, open
> notebook with handwritten Arabic math notes, a laptop showing a video call
> tutoring session, slightly tired but focused expression, natural skin
> texture with visible pores, realistic imperfect room lighting, shot on
> 50mm lens shallow depth of field, muted warm color grade, photojournalism
> style, no text overlay, no logos"

Result: judged as not reading as AI-generated — worn wall texture, a family
photo detail in the background, handwritten notes, believable uneven lamp
light. The specificity (Damascus apartment, Arabic math notes, the exact
tutoring-app context) is what made it usable for Ostazi specifically, not
just "a studying photo."

## Higgsfield-specific corrections (verified 2026-09-25 against Higgsfield's own internal prompt guides)

This skill's generic recipe was written for Qwen/Gemini and is **wrong in one place for
Higgsfield's UGC-tuned models** (`soul_2` image, `seedance_2_5` video): Higgsfield's own
`ugc-review-video` and `character-sheet` workflow docs (read via `get_workflow_instructions` /
`get_workflow_bundle_file`, not guessed) explicitly ban the exact phrasing this skill's step 2
recommended.

- **Drop "shallow depth of field" / "f/1.8" / named-aperture language for a phone-UGC shot.**
  Higgsfield's own `ugc-character.md`: *"Depth of field — describe naturally as 'subject in clear
  focus with the background naturally falling out as in any phone photo.' Do NOT use 'minimal
  depth of field, soft subtle separation' — that's editorial DSLR language, NOT phone
  aesthetic."* A phone selfie has a wide-open sensor with everything roughly in focus, not a
  DSLR-style blur; asking for shallow DOF is itself an AI-slop tell on this class of model.
- **"Cinematic" is banned outright, not just discouraged, on Higgsfield's video quality tail**:
  their Seedance prompt rules list `no cinematic grade, no film grain, no bokeh, no lens flare,
  no fisheye lens, no ultra-wide distortion, no slow motion, no beauty filter` verbatim as the
  standard negative tail. Never write "cinematic lighting" into a Higgsfield UGC/selfie prompt,
  not even as an upgraded "named lens" version of it.
- **Light: cool/neutral daylight, never warm.** Their guide: *"MUST be cool/neutral daylight,
  NEVER golden hour, NEVER warm sunset, NEVER orange/amber cast."* This directly overrides this
  skill's own worked example below (which used "warm single desk lamp" / "muted warm color
  grade") for a different, non-Higgsfield model — don't carry that warm-light habit into a
  Higgsfield prompt.
- **Ban these skin/quality adjectives, they read as retouched**: `glowing skin`, `flawless skin`,
  `radiant complexion`. Use instead: `phone-sensor grain and realistic skin pores and texture
  preserved, no retouch, no smooth-skin filter, no professional gloss`.
- **Ban "aware of the lens" framing.** `warm smile at the camera`, `looking at the camera with a
  smile`, `direct eye contact with the camera and a confident smile` are flagged as an
  "aware-of-camera mimic" — a real candid selfie catches someone mid-action, not posed for the
  shot. Use a mid-action or natural-unguarded expression instead ("caught mid-sentence", "natural
  unguarded face, soft neutral expression, not smiling at the camera").
- **Deliberate imperfection, Higgsfield's own version**: "slightly off-center, slightly
  imperfect framing — not posed, not studio-centered", "spontaneous angle with a slight casual
  tilt", "captured mid-moment, NOT a formal pose". Same principle as this skill's own item 3
  above, just their exact vetted wording for their own models.
- **This is model-family-specific, not universal** — don't over-generalize it. Higgsfield's own
  Veo 3 / Veo 3.1 route is a *cinematic* model by design ("ultra-realistic, top-tier cinematic
  quality") and is judged by different tells (audio-visual sync, natural speech motion), so the
  "no cinematic, no bokeh" ban above applies to the Seedance/UGC-selfie route specifically, not to
  every Higgsfield model. Check the model's own `description`/`tags` via `models_explore` before
  assuming either rule set.
- **When the Higgsfield MCP tools are live, don't freehand a prompt from this skill's generic
  recipe alone for a Higgsfield job** — load the matching workflow instructions
  (`get_workflow_instructions`, e.g. `ugc-review-video` for a talking creator, `character-sheet`
  for a reference sheet) and follow its own de-slop language, which is longer, more specific, and
  authored by the platform that will actually render it. This skill's general checklist (hands,
  eyes, teeth, hair, background physics, "always look at the frame before trusting the prompt")
  still applies underneath — it just doesn't replace Higgsfield's own model-specific banned/
  recommended phrase lists when a Higgsfield model is the target.
- **NEVER name a social platform/app/UI concept in a `soul_2` prompt, not even to ban it — this is
  a confirmed failure mode, not a theory (2026-09-25, personal-brand presenter thread).** A locked
  "chest-up, direct-to-camera, podcast mic, 9:16" composition on `soul_2` first hallucinated a mild
  avatar+username overlay with only a generic `"no UI elements"` negative present. Adding EXPLICIT
  named negatives on the retry (`"no Instagram Stories or Reels interface, no username..."`) made
  it categorically worse: a full Instagram Stories viewer chrome with the literal word
  **"Instagram"** rendered as on-screen text, plus a wrong person's avatar. `soul_2`'s
  `generate_image` call has no separate negative-prompt parameter — `"no X"` is just more text in
  the same positive prompt string, and this model clearly does not reliably parse negation: naming
  a concept, even to forbid it, reads as an instruction to render it. **Rule: if a specific
  app/platform/UI artifact shows up unwanted, fix it by REMOVING every word that could semantically
  point at that concept (positive or negative) — never by adding a "no <concept>" clause.** Prefer
  only fully generic negatives that don't name a platform ("no on-screen text/graphics" is fine;
  "no Instagram" is not).
- **9:16 is itself a bias source for this exact composition** — it's Instagram Reels/Stories'
  native aspect ratio, so "mic + direct-to-camera + 9:16" is close to asking for the literal shape
  of a scraped Reels screenshot (soul_2 is UGC-trained, likely scraped from exactly that kind of
  content). If a locked chest-up/mic/direct-address composition keeps pulling in app chrome despite
  clean wording, generate the anchor still at a non-Reels-native ratio (3:4 or 4:5) and crop/pad to
  9:16 afterward if the final use genuinely needs it, rather than fighting the bias at 9:16 directly.
- **If a bad render can't be fixed by re-prompting `soul_2` (the composition itself seems to be the
  trigger), edit the existing clean-except-artifact image instead of regenerating from scratch** —
  `gpt_image_2` accepts a reference image (via a prior job_id or `media_import_url`, never a raw
  URL) and does real reference-based editing: describe the fix as a plain positive photo-editing
  instruction ("remove the banner overlay at the top/bottom, extend the wall/fabric naturally to
  fill it") without naming any platform. This is a different cost tier — check with `get_cost`
  first, it is NOT the same ~0.12cr as a `soul_2` still (an edit pass came back at 6.5cr in this
  session) — and ask before spending, same as any other Higgsfield spend.

## Routing

- **Higgsfield MCP available** (check the tool list / `ToolSearch`): use it directly —
  `generate_image` (`soul_2` + a trained `soul_id` for a specific person's identity, `gpt_image_2`
  for general/typography work) and `generate_video` (`seedance_2_5` for UGC-style talking/selfie
  content, `veo3_1`/`veo3_1_lite` for a native-audio cinematic talking clip). Always `get_cost:
  true` first (free) and confirm the exact credit number with the user before submitting. Load
  `get_workflow_instructions` for the matching workflow (`ugc-review-video`, `character-sheet`,
  `thumbnail-generation`, etc.) rather than writing the prompt from this skill alone — see the
  correction section above for why.
- **No Higgsfield tools / a non-Higgsfield job**: `web-imagegen <qwen|gemini> "<prompt>" [--mode
  image|video] --out <dir>` for quick photoreal stills and short (~5s) clips. Qwen images are the
  verified-reliable path; Qwen video through this tool is currently unreliable (see status note in
  `web_imagegen.py`) — for anything longer than ~5s, or until that's fixed, use
  **`veo-flow-free-video-gen`** (Google Flow/Veo 3.1, free, longer + extendable/stitchable clips)
  instead, which has its own physics-grounded no-slop prompt methodology — the two skills'
  principles agree, use whichever tool fits the length/platform needed. This route's DSLR/shallow-
  DOF/warm-light language is fine here — it is Qwen/Gemini-specific, not Higgsfield's UGC route
  (see the correction section above).
- Sits upstream of `content-factory` stage 4a/4b (photo + video sourcing) and
  `marketing-psychology`/`social-growth-science` (the copy this visual pairs
  with) — write the prompt with this checklist before calling the tool, not
  after judging a slop result.
- For brand-specific product visuals with 3D/exact-geometry needs, `threejs`/
  `product-photogrammetry` may still beat generation — this skill is for
  photoreal *scenes* (people, settings, lifestyle), not precise product
  render accuracy.
