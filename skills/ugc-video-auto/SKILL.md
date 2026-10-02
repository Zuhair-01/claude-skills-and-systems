---
name: ugc-video-auto
description: Full UGC ad video pipeline — generates a character image on Higgsfield, then creates a Seedance 2.0 video from it. Orchestrates the complete flow from image prompt to finished UGC video. Use when the user wants to create a UGC ad video end-to-end, or wants to take a generated image from Higgsfield's image tab into video creation. Triggers on "create a UGC video", "make a UGC ad", "UGC pipeline", "turn this into a UGC video", or any request combining image generation with video creation for ads/UGC content. Requires Playwright MCP tools.
---

# UGC Video Auto — Full Pipeline via Playwright

This skill orchestrates the complete UGC ad video pipeline on Higgsfield: generate a character image → select it for video → add a UGC video prompt → generate a Seedance 2.0 video. All automated via Playwright.

---

## Pipeline Overview

```
Step 1: Generate character image  →  /image/soul-v2
Step 2: Navigate to video page    →  /create/video?model=seedance_2_0
Step 3: Select image from gallery →  Upload dialog → "Image Generations" tab
Step 4: Write UGC video prompt    →  Lexical editor (contenteditable)
Step 5: Configure & generate      →  Click Generate
```

---

## Prerequisites

- User must be **logged in** to higgsfield.ai in the Playwright browser session
- **Playwright MCP** plugin must be enabled
- Load each Playwright tool with `ToolSearch` before first use

## Input Requirements

The user provides:
1. **Character description** OR a pre-made image prompt (invoke `/ugc-hot-girl` to generate one)
2. **Product/brand context** — what the UGC video is advertising
3. **Video style** — testimonial, product showcase, unboxing, reaction, etc.

Optional overrides:
- **Image model**: Soul 2.0 (default, best for portraits)
- **Video model**: Seedance 2.0 (default)
- **Duration**: 5s, 8s (default), 10s
- **Ratio**: Auto, 16:9, 9:16 (TikTok/Reels), 1:1
- **Resolution**: 720p (default), 1080p

---

## Full Automation Flow

### Phase 1: Generate the Character Image

#### Step 1.1: Navigate to image generation

```
browser_navigate → url: "https://higgsfield.ai/image/soul-v2"
```

Wait for page load, take a snapshot.

#### Step 1.2: Clear the prompt bar, then enter the image prompt

**Per standing project rule (CLAUDE.md): always clear the prompt bar via
JS before typing, and screenshot after clearing to confirm it's empty.**
(Step 2.6 below already does this correctly for the video prompt — this
step brings the image prompt into line with the same rule.)

Find the textbox (Playwright ID: `hf:tour-image-prompt`, placeholder: "Describe the scene you imagine"):

```
browser_click → ref: <textbox_ref>, element: "Image prompt textbox"
browser_evaluate → clear the textbox value via JS
browser_take_screenshot → confirm the textbox is visibly empty
browser_type → ref: <textbox_ref>, text: "<character image prompt>"
```

If the user hasn't provided an image prompt, use `/ugc-hot-girl` to generate one first.

#### Step 1.3: Generate the image

Find the Generate button (shows "Generate XXXX free gens left"):

**ASK USER FOR CONFIRMATION** — this uses credits/free generations.

```
browser_click → ref: <generate_button_ref>, element: "Generate button"
```

#### Step 1.4: Wait for generation

```
browser_wait_for → time: 20
```

Take a screenshot. Verify the new image appears as the **first item** in the History grid. Confirm by checking the first grid element's innerHTML contains an `<img>` tag with a fresh asset URL.

---

### Phase 2: Create the Video from the Generated Image

#### Step 2.1: Navigate to Seedance 2.0 video page

```
browser_navigate → url: "https://higgsfield.ai/create/video?model=seedance_2_0"
```

Wait for page load, take a snapshot. Confirm "Seedance 2.0" appears in the Model button.

#### Step 2.2: Open the upload media dialog

Find the upload area — look for `generic [cursor=pointer]` containing:
- `paragraph: Upload media`
- `paragraph: Image, Video or Audio`

```
browser_click → ref: <upload_area_ref>, element: "Upload media area"
```

This opens a **dialog** with tabs: Uploads, Image Generations, Video Generations, Elements, Liked.

#### Step 2.3: Switch to Image Generations tab

```
browser_click → ref: <image_gen_tab_ref>, element: "Image Generations tab"
```

Look for `button "Image Generations"` in the dialog's tab bar.

#### Step 2.4: Select the generated image

The most recently generated image is the **first item** in the grid.

It initially appears as a `button "Check eligibility"`. Click it:

```
browser_click → ref: <first_image_ref>, element: "First image (most recent generation)"
```

After clicking, the button transforms into a `generic [cursor=pointer]` with an image preview and a green checkmark — meaning it's selected and eligible.

**Important**: The first "Check eligibility" button in the list is always the most recent image. After clicking, its ref disappears from the snapshot and is replaced by a new generic element.

#### Step 2.5: Close the dialog

```
browser_press_key → key: "Escape"
```

Take a snapshot. Verify:
- The upload area **no longer shows** "Upload media" text
- Instead it shows a `generic [cursor=pointer]` with nested image elements (48px thumbnails)
- The old `paragraph: Upload media` and `paragraph: Image, Video or Audio` are gone

#### Step 2.6: Clear any existing prompt

The video page uses a **Lexical rich text editor** (contenteditable div), NOT a standard textbox. To clear it:

```
browser_evaluate → function: "() => { const el = document.querySelector('[data-lexical-editor]'); el.focus(); el.click(); }"
browser_press_key → key: "Control+a"
browser_press_key → key: "Backspace"
```

Take a snapshot. The textbox should now show the placeholder: "Describe your scene in detail. Use @ to reference assets"

#### Step 2.7: Enter the UGC video prompt

After clearing, take a snapshot to get the fresh textbox ref. Then type **slowly** (required for the Lexical editor):

```
browser_type → ref: <textbox_ref>, text: "<UGC video prompt>", slowly: true
```

**UGC Video Prompt Templates** (pick based on style):

**Testimonial / Talking Head:**
```
The woman from @image1 is talking directly to camera with natural hand gestures, warm golden hour lighting, casual authentic vibe. She speaks enthusiastically, leaning in slightly for emphasis. Soft bokeh background, shallow depth of field. Natural skin texture, realistic lip movement, TikTok UGC testimonial style. Smooth handheld camera, 24fps.
```

**Product Showcase:**
```
The woman from @image1 holds up a product toward the camera, turning it to show different angles. Excited genuine expression, eyes wide. Ring light illumination, clean background. She points at the product features, nodding enthusiastically. Close-up selfie framing, iPhone-quality video, authentic UGC feel.
```

**Reaction / Unboxing:**
```
The woman from @image1 opens a package with excited anticipation, pulling out a product and reacting with genuine delight. Surprised expression, mouth open, then breaking into a wide smile. Natural bedroom lighting, casual setting. Handheld camera feel, authentic unboxing energy, TikTok style.
```

**Before/After:**
```
The woman from @image1 starts looking skeptical, touching her face doubtfully. Then she applies a product, and her expression transforms to amazement, touching her skin in disbelief. Soft ring light, bathroom mirror setting. Split-feel transformation moment, genuine reaction, UGC testimonial.
```

**Lifestyle / Day-in-the-Life:**
```
The woman from @image1 walks through a bright modern space, casually interacting with a product as part of her routine. Natural morning light, relaxed movement, authentic candid energy. Camera follows with gentle tracking, shallow depth of field. Aspirational but relatable lifestyle content.
```

#### Step 2.8: Configure video settings (optional)

Default settings work well for most UGC:
- **Duration**: 8s (good for short-form)
- **Ratio**: Auto (or 9:16 for TikTok/Reels)
- **Resolution**: 720p

To change ratio for TikTok vertical:
```
browser_click → ref: <ratio_button_ref>, element: "Ratio selector"
```
Then select "9:16" from the dropdown.

#### Step 2.9: Generate the video

Take a screenshot showing the final form state.

**ASK USER FOR CONFIRMATION** — video generation costs more credits than images.

The Generate button shows credit cost (e.g., "Generate 30 20"):

```
browser_click → ref: <generate_button_ref>, element: "Generate video button"
```

#### Step 2.10: Monitor generation

After clicking Generate:
1. The video enters the generation queue
2. Check the History tab for progress
3. Periodically take screenshots to show status
4. Seedance 2.0 videos typically take 1-3 minutes

---

## Key Element Patterns Reference

### Image Generation Page (`/image/soul-v2`)

| Element | Pattern |
|---|---|
| Prompt textbox | `textbox` with ID `hf:tour-image-prompt` |
| Model selector | `group > button` containing "Soul 2.0" |
| Aspect ratio | `button` showing "3:4" |
| Resolution | `button` showing "2k" |
| Generate button | `button "Generate XXXX free gens left"` |
| First result | First `generic` child in the History grid |

### Video Creation Page (`/create/video`)

| Element | Pattern |
|---|---|
| Upload area (empty) | `generic [cursor=pointer]` with `paragraph: Upload media` |
| Upload area (filled) | `generic [cursor=pointer]` with nested image thumbnails, no "Upload media" text |
| Upload dialog | `dialog` with tab bar: Uploads, Image Generations, etc. |
| Image Generations tab | `button "Image Generations"` in dialog |
| First image in gallery | First `button "Check eligibility"` in dialog grid |
| Selected image | `generic [cursor=pointer]` with nested img (replaces Check eligibility button) |
| Prompt editor | `[data-lexical-editor]` contenteditable div |
| Prompt textbox (in snapshot) | `textbox [active]` after focusing the Lexical editor |
| Model button | `button "Model"` containing "Seedance 2.0" |
| Duration button | `button "Duration"` |
| Ratio button | `button "Auto Ratio"` |
| Resolution button | `button "720p Resolution"` |
| Generate button | `button "Generate XX XX"` with credit cost |

---

## Error Handling

- **Not logged in**: Ask user to log in (`! open https://higgsfield.ai`)
- **Image prompt bar missing**: Refresh the page — this is an intermittent platform bug
- **"Check eligibility" doesn't transform**: The image may not be compatible with Seedance 2.0. Try a different image or re-generate
- **Lexical editor won't clear**: Try triple-clicking to select all, then Backspace. Or use `browser_evaluate` to clear innerHTML
- **Dialog won't close on Escape**: Click outside the dialog area
- **Insufficient credits**: Warn the user before generating. Video costs more than images
- **Stale refs**: Always take a fresh snapshot before each interaction. Refs change after any page state change

---

## Example End-to-End Workflow

```
User: "Create a UGC ad video with a hot girl promoting my new skincare serum"

1. Invoke /ugc-hot-girl → generates beauty/skincare image prompt:
   "Attractive young woman, early 20s, clear dewy skin, dark brown hair in
    messy bun... ring light illumination... photorealistic, 4K..."

2. Phase 1 — Image Generation:
   → Navigate to /image/soul-v2
   → Type the image prompt
   → Confirm with user → Click Generate
   → Wait 15-20s → Image appears in grid ✓

3. Phase 2 — Video Creation:
   → Navigate to /create/video?model=seedance_2_0
   → Click upload area → Image Generations tab
   → Click first image (Check eligibility) → Escape
   → Image loaded into form ✓
   → Clear old prompt → Type UGC testimonial prompt:
     "The woman from @image1 holds up a small serum bottle, examining it
      with genuine curiosity. She applies a drop to her fingertip, touches
      her cheek, and her expression lights up with delight..."
   → Set ratio to 9:16 for TikTok
   → Confirm with user → Click Generate
   → Video generating... done ✓

4. Report: "Your UGC video is ready! Check the History tab."
```

---

## Pipeline Skills Reference

| Step | Skill | What it does |
|---|---|---|
| 1 | `/ugc-hot-girl` | Generates the character image prompt |
| 2 | `/higgsfield-image-auto` | Automates just the image generation step |
| 3 | `/seedance-auto-generate` | Automates just the video generation step (from local file) |
| **Full** | **`/ugc-video-auto`** | **This skill — runs the entire pipeline end-to-end** |

You can use the individual skills separately, or invoke `/ugc-video-auto` to run everything in one go.
