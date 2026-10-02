---
name: raylight-motion-video
description: Make polished product/app demo videos (3D device mockups, camera moves, screen-recording style motion) using Raylight (raylight.app) — a browser-based motion-design tool for SaaS/product marketing videos, controlled directly from Claude via its MCP server. Use for Ostazi (or any brand's) app/website promo videos, feature-announcement clips, SaaS launch videos, and any ask that wants a "screen recording that looks cinematic" rather than a narrated kinetic-type reel. Triggers: "raylight", "product demo video", "app promo video", "screen mockup video", "make it look like a $10k video", "SaaS launch video", "put my screenshots in a 3D phone/laptop and animate it".
---

# Raylight motion video

Raylight is a browser tool (raylight.app) for building product-marketing motion videos: real screens
(screenshots/clips) placed inside animated 3D device mockups (iPhone/iPad/MacBook), with camera moves
(push-in, pull-back, dolly), scene effects (depth of field, bloom, film grain, motion blur, color grade),
shot-to-shot transitions, timeline-based animation blocks, and generated sound effects/music/voiceover.
It ships a first-party **MCP server** so an AI agent (Claude, ChatGPT, Cursor) can read a project's shots,
apply edits, and render frames to check its own work — this is what makes it usable "flawlessly" from
Claude Code instead of us hand-clicking a web UI.

## When to use this vs. the other video skills

- **Raylight** — the shot is a real UI screen (a website, app screen, dashboard, product photo) that needs
  to look like a cinematic, camera-moved screen recording: Ostazi's app on a phone, a feature walkthrough,
  a "here's the new dashboard" clip, a hero video for a landing page. Fastest path to a professional-looking
  product video with zero manual keyframing.
- `motion-reel-pipeline` / Remotion (`remotion-video-creation`, `video-shotcraft`) — narrated kinetic-type
  cards, custom illustrated motion graphics, anything needing frame-perfect code-driven control or assets
  Raylight can't natively build (custom shaders, non-standard layouts). Heavier, slower, fully bespoke.
- Use both together when useful: build the device-mockup shots in Raylight, export, then cut them into a
  Remotion sequence alongside narration/kinetic type via `ffmpeg`/`video-editing`.

## Connection status (this machine)

The Raylight MCP server is already registered at user scope:
```
claude mcp add --transport http raylight https://api.raylight.app/mcp --scope user
```
Check it's live: `claude mcp list` should show `raylight: https://api.raylight.app/mcp (HTTP)`.

**First-time auth (the user must do this himself — account creation + OAuth approval are never done by
Claude, see the account-creation rule):** the MCP tools will prompt an OAuth sign-in the first time
they're called. Tell the user: "Raylight will ask you to approve access — go to raylight.app, sign up free
(no card required), and approve the connection when it pops up." After that one-time approval, every
future session can call the tools directly with no further action from him.

## Workflow (once connected)

1. **`get_editor_status`** — check whether a Raylight editor tab is open and connected. If not:
   **`list_projects`** and hand the user the exact `editUrl` to open in his browser (he opens it — user
   drives the browser tab per the AI-gen-tools rule, this session drives it through MCP after that).
2. **Start from a template when one fits** the use case (product demo / app promo / SaaS launch / feature
   announcement / website hero) — browse `raylight.app/templates`, pick the closest match, "start from
   template" instead of a blank canvas. Templates already carry proven timing/camera moves.
3. **Feed it real assets**: actual Ostazi screenshots (live site, not mockups/placeholders — per the
   no-ground-truth rule) or a short screen-recording clip. Never invented UI.
4. **Describe the edit in plain English** through the MCP tools, e.g.:
   - "Make a 20 second product demo from these app screenshots"
   - "Slow down the title and add a slow push-in on shot 2"
   - "Render the last shot and tell me what looks off"
   Raylight's agent loop applies the edit, renders real frames, and checks its own work (catches things
   like a phone cut off at the frame edge) before handing back.
5. **Sound**: voiceover/SFX/music are credit-metered (see Pricing below) — write the VO script first,
   route it through the same voice-quality bar as `motion-reel-pipeline` (never a robotic default voice
   for anything the user will publish; Arabic VO still goes through OmniVoice/Fish Audio, not Raylight's
   built-in voices, unless the user explicitly wants Raylight's voice for speed).
6. **Export**: Free plan exports 1080p60 with a small "Made in Raylight" watermark badge — fine for
   drafts/review, NOT for final Ostazi-branded delivery. A paid plan (see below) or spending 500 credits
   removes the badge on a single export. Confirm with the user before spending credits or upgrading.
7. QA and handoff exactly as `motion-reel-pipeline` stage 9/11 (frame-check, no placeholders, brand
   contact block correct, Handoff Log entry on a milestone).

## Pricing / limits (checked live 2026-09-26, verify again before relying on numbers — they change)

| Plan | Price | MCP calls/week | Exports | Monthly credits |
|---|---|---|---|---|
| Free | $0, no card | 50 | 1080p60, watermark badge | none (pay-as-you-go packs) |
| Hobby | $9-12/mo | 1,000 | clean 4K60 | 300 |
| Pro | $18-24/mo | 5,000 | clean 4K60, embeds | 1,000 |
| Max | $36.75-49/mo | unlimited | clean 4K60 | 5,000 |

Credits: sound effect take = 10, music track = 100, voiceover = 15 per 500 characters. Free plan has
no monthly credit allowance — buy a pack, or lean on the flow entirely without Raylight's audio gen
(use OmniVoice/Fish Audio + `ffmpeg` mixing instead, same as the rest of the pipeline) to stay free.
**Never upgrade or buy credits without asking the user first** — this is a spend decision (see credits
permission rule).

## Gotchas

- MCP edits act on the project **currently open in the user's browser tab** — nothing happens if no editor
  tab is connected. Always `get_editor_status` first; don't assume a prior session's tab is still open.
- Video uploads on Free are capped at 50MB / 1 min per clip — fine for a UI screen-recording source clip,
  not for a long raw capture; trim first with `ffmpeg` if needed.
- The watermark badge on Free exports means Free output is a draft/preview tier only — flag this to
  the user before treating a Free-tier export as final deliverable.
- Treat anything Raylight's own generative agent invents (background music mood, SFX picks, auto-camera
  moves) as a first draft to review, not a final creative decision — same bar as any AI-gen output per
  the design-quality-bar memory.

## Learned from the first real build (Ostazi promo, 2026-09-26)

- **`upload_media {url}` only accepts http(s) URLs — a local `file:///` path errors immediately.**
  For a local file: small ones (<5MB) can go inline as `{base64, mime}`, but the base64 string
  itself is huge in a tool call and burns context fast — prefer way 3 (`{mime, bytes}` → PUT to a
  signed `uploadUrl` → `upload_media {assetId}` to finish) for anything non-trivial.
- **The signed-URL PUT is flaky over `curl`/`Invoke-WebRequest` from this environment**: it
  reliably sends 100% of the bytes but then the client-side timeout fires waiting on the response
  header (seen at 45s and 90s). The upload usually already succeeded server-side despite the
  client timing out — always call `upload_media {assetId}` afterward to check before assuming
  failure and re-uploading (a genuine retry PUT on an already-used signed URL comes back 400).
- **`start_from_template` does NOT open/switch the user's tab** — it returns a fresh `editUrl` the
  user has to open themselves; the previously-open project stays connected until they do.
- **A template's media/text slots are NOT empty placeholders** — they carry the original creator's
  actual content (their own screenshots, wordmark text, even a licensed music bed). Read
  `get_project_overview` first to see exactly what's there before assuming a slot is blank.
- **`update_asset` cannot swap an image's source** — it only edits transform/name/etc. To put a
  different image into an existing template slot: `remove_asset` the old one, then `add_image` at
  the same `shotId` with the same `position`/`rotationDeg` (copied from `get_shot_details`) so the
  template's tilt/depth staging is preserved, just with new content inside it.
- **Real screenshots plug straight into a template's existing Hero Reveal / liquid-glass shots** —
  no separate image-gen pass was needed to look premium; Raylight's own tilt + z-depth + dolly +
  bloom/vignette/DOF stack is what makes a plain screenshot read as expensive. Reserve
  `no-ai-slop-visuals`/Higgsfield generation for content Raylight can't source directly (background
  scenes, lifestyle shots), not for the app/website screens themselves — those should always be
  real captures, never invented UI.
- **A live Android APK screenshot is a legitimate source too**, not just website screenshots: boot
  the project's AVD (`emulator -avd <name>`, then `adb wait-for-device` + poll
  `getprop sys.boot_completed`), launch the app (`adb shell monkey -p <package> -c
  android.intent.category.LAUNCHER 1`), `adb shell screencap -p /sdcard/x.png` + `adb pull`. On
  Windows git-bash, set `export MSYS_NO_PATHCONV=1` first or `/sdcard/...` gets mangled into a
  Windows path and the pull fails silently.
- **`render_stills`/`render_filmstrip` fail if the editor browser tab is hidden/backgrounded** —
  heavy assets (especially video) load too slowly for the render to capture them in time. The tab
  needs to stay visible on screen (any monitor/workspace is fine, it does not need window focus)
  for the whole render call. Tell the user this up front before the first render of a session.
- **A backend blocker (e.g. OTP send failing) is a real finding, not a tap-targeting mistake** —
  when the same correct demo credentials fail the same way twice, stop retrying blindly and check
  project memory/docs for a known issue before assuming user error. Confirmed here: Ostazi's
  WhatsApp OTP has no Syria sender configured, so no account (real or seeded demo) can complete
  phone-OTP login on this build; the documented interim unblock is a `EXPOSE_DEV_OTP`/
  `DEV_OTP_ALLOWLIST` Vercel env var pair, but that only covers one bare test number with no seeded
  profile data — not actually useful for a rich dashboard screenshot even if flipped. Reading Vercel
  env vars directly got auto-blocked as credential access; that kind of check goes through the user.

## Reference

Official pages read for this skill (re-check if anything here seems stale): raylight.app,
raylight.app/pricing, raylight.app/mcp, raylight.app/agents, raylight.app/templates.
