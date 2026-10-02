---
name: seedance-auto-generate
description: Automatically generate a Seedance 2.0 video on Higgsfield using Playwright browser automation. Use when the user provides an image and wants to create an AI video from it on Higgsfield. Triggers on requests like "generate a video", "create a seedance video", "make a video on higgsfield", "auto-generate video", or any request to automatically submit a video generation job to higgsfield.ai. Requires Playwright MCP tools.
---

# Seedance 2.0 Auto-Generate via Playwright

This skill automates the full Higgsfield Seedance 2.0 video creation flow using Playwright browser automation. It uploads an image, fills in a prompt, and clicks Generate — hands-free.

> **Source**: [github.com/beshuaxian/higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng)

---

## Available Sub-Skills (Prompt Generators)

This auto-generate skill is the **automation engine**. To craft the best possible prompt for your video, **first invoke the matching style sub-skill** before running this automation. Each sub-skill turns Claude into a specialized prompt engineer for that video style — generating large, detailed, paste-ready prompts with powerful **2-second hooks** that stop the scroll.

### How to Use Sub-Skills

1. **Pick the sub-skill** that matches your video style from the table below
2. **Invoke it** with `/01-cinematic`, `/07-ecommerce-ad`, `/15-real-estate`, etc.
3. The sub-skill generates a **production-grade Seedance 2.0 prompt** (15-25 lines, with timeline, camera, lighting, sound, and 2-second hook)
4. Then invoke `/seedance-auto-generate` to **automatically submit** the prompt + image to Higgsfield

### Creative Styles

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/01-cinematic` | Cinematic Film | Film quality — dramatic lighting, camera language, depth of field, anamorphic, noir, epic |
| `/02-3d-cgi` | 3D CGI | 3D rendered — Pixar, Unreal Engine, photorealistic, isometric, ray tracing, volumetric |
| `/03-cartoon` | Cartoon & Animation | 2D animation — cel-shaded, hand-drawn, flat vector, watercolor, rubber hose, motion graphics |
| `/04-comic-to-video` | Comic to Video | Animate comics — manga pages, webtoons, storyboards, sequential art, graphic novels |
| `/05-fight-scenes` | Fight Scenes & Action | Combat — martial arts, sword fights, chase scenes, superhero battles, action choreography |
| `/08-anime-action` | Anime | Japanese animation — shonen, seinen, mecha, magical girl, isekai, anime openings |

### Commercial & Marketing

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/06-motion-design-ad` | Motion Design Ad | Software/SaaS — product launches, feature showcases, app promos, tech demos, UI animation |
| `/07-ecommerce-ad` | E-Commerce Ad | Product ads — fashion, beauty, electronics, food, Amazon/Shopify/TikTok Shop, unboxing |
| `/09-product-360` | Product 360 | Turntable — multi-angle showcase, product reveal, hero shots, beauty shots, product spin |
| `/11-social-hook` | Social Hook | Viral content — TikTok, Instagram Reels, YouTube Shorts, scroll-stopping hooks |
| `/12-brand-story` | Brand Story | Brand narrative — origin stories, mission videos, company culture, founder stories |

### Industry-Specific

| Slash Command | Skill Name | When to Use |
|---|---|---|
| `/10-music-video` | Music Video | Beat-synced — performance, lyric video, music visualization, concert visuals, album art |
| `/13-fashion-lookbook` | Fashion Lookbook | Fashion — lookbooks, model walks, outfit showcases, runway clips, streetwear, campaigns |
| `/14-food-beverage` | Food & Beverage | Food — restaurant promos, recipe content, food ASMR, menu showcases, appetite appeal |
| `/15-real-estate` | Real Estate | Property — house tours, architecture, interior design, listings, virtual tours, renovation |

### What Each Sub-Skill Generates

Every sub-skill provides:
- **2-Second Hook Framework** — 10-12 attention-grabbing opener patterns
- **Timeline Segmentation** — beat-by-beat breakdown up to 15s
- **Camera Movement Encyclopedia** — 15-20+ techniques with exact phrasing
- **Lighting & Atmosphere** — setups that communicate mood and quality
- **Sound Design** — ambient, foley, music, silence guidance
- **Material Reference Strategy** — `@image1` `@video1` `@audio1` best practices
- **Platform Optimization** — TikTok, Instagram, YouTube, etc.
- **5+ Large Example Prompts** — 15-25 lines each, production-quality

> Each skill also has a Chinese version at `skills/XX-name/zh-CN/SKILL.md`

---

## Seedance 2.0 Specs

| Input | Format | Limit |
|---|---|---|
| Image | jpeg, png, webp, bmp, tiff, gif | Up to 9, each < 30MB |
| Video | mp4, mov | Up to 3, each < 50MB, 2-15s total |
| Audio | mp3, wav | Up to 3, each < 15MB, up to 15s total |
| Text | Natural language prompt | — |
| **Combined** | — | **Max 12 files total** |
| **Output** | Video | **4-15s, 720p, with sound** |

Reference materials in prompts: `@image1` `@video1` `@audio1`

---

## Prerequisites

- User must be **logged in** to higgsfield.ai in the Playwright browser session
- **Playwright MCP** plugin must be enabled
- Image file must be accessible within the project directory (copy from Downloads if needed)

## Input Requirements

The user provides:
1. **An image file** (path on disk — `.png`, `.jpg`, `.webp`, etc.)
2. **A description or prompt** for the video (or invoke a sub-skill first to generate one)

Optional overrides (defaults shown):
- **Duration**: `8s` (options: 5s, 8s, 10s)
- **Ratio**: `Auto` (options: Auto, 16:9, 9:16, 1:1)
- **Resolution**: `720p` (options: 720p, 1080p)

---

## Automation Flow

Follow these steps exactly using Playwright MCP tools. Load each tool with `ToolSearch` before first use.

### Step 0: Prepare the image

If the image is outside a Playwright-allowed directory (e.g. in
`~\Downloads\`), copy it into one first — there is no fixed
"project root" folder for this on this machine, so use the scratchpad
directory listed in your system prompt, or the specific project's asset
folder if this is part of a larger project (e.g. `clip-platform`'s
storage dir):

```
cp "<source_path>" "<scratchpad_or_project_assets_dir>/<filename>"
```

Confirm the destination is actually within Playwright's allowed roots
before uploading — don't assume a folder name from an example; verify.

### Step 1: Navigate to Seedance 2.0 creation page

```
browser_navigate → url: "https://higgsfield.ai/create/video?model=seedance_2_0"
```

The `?model=seedance_2_0` query parameter pre-selects the Seedance 2.0 model automatically.

Wait for the page to load, then take a snapshot to confirm:
- The page title contains "Create AI Videos"
- The Model button shows "Seedance 2.0"

If a cookie consent dialog appears, close it by clicking the "Close" button (x).

### Step 2: Open the upload dialog

Take a snapshot and find the upload area. It contains text like "Upload media" and "Image, Video or Audio". Click the upload area element.

This opens a **dialog** with tabs: "Uploads", "Image Generations", "Video Generations", "Elements", "Liked".

### Step 3: Trigger the file chooser

Inside the dialog, find and click the **"Upload media"** button (the first clickable item in the dialog grid — it has an upload icon and text "Upload media" with subtext "Protected content is not allowed").

This triggers a **file chooser** modal. The tool result will say: `[File chooser]: can be handled by browser_file_upload`

### Step 4: Upload the image file

```
browser_file_upload → paths: ["<absolute path to the copied file from Step 0>"]
```

Use the absolute Windows path with double backslashes. The file must be within Playwright's actual allowed roots for this session — verify, don't assume a specific folder name.

### Step 5: Wait for upload to process

```
browser_wait_for → time: 5
```

Wait 5 seconds for the image to upload and appear in the asset grid.

### Step 6: Select the uploaded image

Take a snapshot of the dialog. The **newly uploaded image** appears as the **first item after the "Upload media" button** in the grid. It will be a `generic [cursor=pointer]` element. Click it.

**Important**: The newly uploaded image is always the first grid item right after the upload button. Look for the element immediately following the upload button in the dialog's grid.

### Step 7: Close the dialog

```
browser_press_key → key: "Escape"
```

The dialog closes. The image is now loaded into the form — the upload area is replaced by an image preview.

### Step 8: Verify image is loaded

Take a snapshot. Confirm:
- The upload area now shows an image preview (a `figure` with `img "media is loading"` or similar)
- The prompt textbox is visible (labeled "Prompt" with placeholder "Describe your scene in detail")
- The Model still shows "Seedance 2.0"

### Step 9: Clear the prompt bar, then enter the prompt

**Per standing project rule (CLAUDE.md): always clear the prompt bar via
JS before typing a new prompt, and always screenshot after clearing to
confirm it's empty.** A leftover prompt from a prior generation
concatenating onto the new one still spends real credits on a garbled
result.

```
browser_click → ref: <textbox_ref>, element: "Prompt textbox"
browser_evaluate → clear the textbox value via JS
browser_take_screenshot → confirm the textbox is visibly empty
browser_type → ref: <textbox_ref>, text: "<the video prompt>"
```

The prompt should be crafted by one of the 15 sub-skills listed above. If the user hasn't specified a style, pick the best-matching sub-skill and use it to generate the prompt first.

### Step 10: Adjust settings (optional)

If the user wants non-default settings:

- **Duration**: Click the "Duration" button, then select the desired option
- **Ratio**: Click the "Auto Ratio" button, then select (16:9, 9:16, 1:1)
- **Resolution**: Click the "720p Resolution" button, then select (720p, 1080p)

### Step 11: Generate

Take a screenshot to show the user the final form state before generating.

**ASK THE USER FOR CONFIRMATION** before clicking Generate — this costs credits.

```
browser_click → ref: <generate_button_ref>, element: "Generate button"
```

The Generate button shows the credit cost (e.g., "Generate 48 32"). After clicking, the video enters the generation queue.

### Step 12: Monitor generation

After clicking Generate:
1. The page may redirect or show a progress indicator
2. Click the "History" tab to see generation status
3. Wait and periodically check until the video is ready
4. Once complete, the video will appear in the History tab

---

## Key Element Patterns (for snapshot navigation)

These are the typical element patterns found on the page. Refs change between sessions — always take a fresh snapshot before interacting.

| Element | How to find it |
|---|---|
| Upload area | `generic [cursor=pointer]` containing text "Upload media" and "Image, Video or Audio" |
| Upload button in dialog | First item in `dialog > generic > generic` grid, contains "Upload media" text |
| Newly uploaded image | First `generic [cursor=pointer]` after the upload button in dialog grid |
| Prompt textbox | `textbox` inside `generic` with label "Prompt" |
| Model button | `button "Model"` containing "Seedance 2.0" |
| Duration button | `button "Duration"` |
| Ratio button | `button "Auto Ratio"` or `button "16:9 Ratio"` |
| Resolution button | `button "720p Resolution"` |
| Generate button | `button "Generate ..."` with credit cost numbers |

---

## Error Handling

- **Not logged in**: If the page shows a login prompt instead of the creation form, ask the user to log in manually (`! open https://higgsfield.ai` in the CLI)
- **File chooser not triggered**: Retry clicking the upload media button; sometimes a second click is needed
- **Image not appearing in grid**: Wait longer (up to 10s) and re-snapshot
- **Dialog won't close**: Try clicking outside the dialog area, or press Escape again
- **Insufficient credits**: The Generate button shows the cost — warn the user before clicking

---

## Example Workflows

### Example 1: Real Estate Video (end-to-end)

```
User: "Create a video for this house photo at C:\Users\User\Downloads\house.webp"

Step 1 → Invoke /15-real-estate with the image to craft a cinematic real estate prompt
Step 2 → Copy image to a Playwright-allowed dir: cp Downloads/house.webp <scratchpad>/house.webp
Step 3 → Run this automation flow with the image + generated prompt
Step 4 → Confirm with user before clicking Generate
Step 5 → Monitor until video is complete
```

### Example 2: Product Ad

```
User: "Make a TikTok ad for my sneakers" + [sneaker photo]

Step 1 → Invoke /07-ecommerce-ad to craft a product showcase prompt
Step 2 → Copy image, run automation, set ratio to 9:16 for TikTok vertical
Step 3 → Confirm and generate
```

### Example 3: Anime-Style Fight Scene

```
User: "Turn this character art into an anime fight scene"

Step 1 → Invoke /08-anime-action to craft an anime action prompt
Step 2 → Copy image, run automation
Step 3 → Confirm and generate
```

### Example 4: Quick Generate (no sub-skill)

```
User: "Just generate a video from this image, cinematic style"

Step 1 → Write a concise cinematic prompt directly (or auto-invoke /01-cinematic)
Step 2 → Copy image, run automation
Step 3 → Confirm and generate
```
