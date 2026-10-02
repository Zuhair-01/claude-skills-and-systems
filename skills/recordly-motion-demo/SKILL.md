---
name: recordly-motion-demo
description: End-to-end pipeline for professional product-tutorial/demo videos — real Recordly screen capture, motion-graphics polish via Remotion (since Recordly's own edit/export CLIs are not real), and Arabic OmniVoice narration. Use for "how to" / onboarding / feature-walkthrough videos of a real product, not synthetic/faked UI.
---

# recordly-motion-demo — Screen-capture + motion-graphics tutorial pipeline

**Type:** Workflow / Video Production
**Triggers:** "make a demo video", "tutorial video", "walkthrough video", "record + edit a product demo professionally", "recordly + motion"
**Companions:** `recordly-launch` (capture), `recordly-edit` / `recordly-export` (their CLI sections are a **documented-but-fictional contract** — read the gap below before trusting either), `remotion-video-creation`, `omnivoice` (Arabic narration), `motion-ui`

---

## Why this skill exists

Two real gaps discovered building the Ostazi student/teacher signup + parent-student
linking tutorials (2026-09-28):
1. `recordly-launch`'s CLI is real (`recordly-cli.js sources|record <sec> <label> <windowFilter>`,
   verified live via Playwright's Electron launcher against the actual installed app).
2. `recordly-edit` and `recordly-export`'s elaborate flags (`--auto-zoom`, `--annotate-file`,
   `--voiceover`, `--format mp4 --quality high`, etc.) are **NOT implemented** — both skills say
   so themselves ("proposed automation contract, not a working interface today"). Editing/export
   only exist through Recordly's own in-app UI.

So a "record it, then script the edit" plan silently breaks at step 2 unless you route around it.
This skill is that route: capture raw with the real CLI, then do all zoom/annotate/caption/voiceover
work as a **Remotion composition** over the raw footage instead of a nonexistent Recordly CLI call.

## The real pipeline

```
1. RECORD (real, scripted)
   node recordly-cli.js sources                        # list capturable windows
   node recordly-cli.js record <seconds> <label> <windowNameContains>
   → raw .mp4 in %APPDATA%\Recordly\recordings\

2. WATCH THE RAW FOOTAGE FIRST (mandatory, no exceptions)
   Note every real timestamp: clicks, page transitions, form fills, error/success states.
   Motion overlays (zoom, callout arrows, highlight boxes) get their position/timing from
   THESE real timestamps — never invented or estimated blind. Same "real geometry only"
   rule as motion-reel-pipeline's on-screen-diagram rule.

3. SCRIPT THE NARRATION (per-step, matches the real UI copy)
   Write what's actually on screen (button labels, field names) — don't paraphrase into
   generic UX language the viewer won't see. For Ostazi: Arabic narration via OmniVoice
   (local, D:/AI_Models/OmniVoice/.venv python; edge-tts Arabic voices are banned per
   the user's 2026-09-25 standing rule); the user approves the narration audio before it's final.

4. BUILD THE MOTION LAYER IN REMOTION (not Recordly)
   - Import the raw .mp4 as a background track.
   - Add: branded intro/outro card (pull the product's real colors/logo — styleDigest,
     never invented), kinetic caption per step timed to the narration's word timestamps,
     callout circle/arrow/box at the REAL click coordinate from step 2 (zoom scale
     1.25x-5.0x per RECORDLY_REAL_API_REFERENCE.md's real math if zooming in), soft
     cross-fade between segments (e.g. Student flow -> Teacher flow, or Student-generates
     -> Parent-redeems).
   - Follow `remotion-video-creation`'s 29 rules (captions, audio, transitions sections).

5. RENDER + QA
   Render via Remotion (not the fictional `recordly export` CLI). Run the same QA bar as
   any other production video: stills at every transition, captions readable in both
   themes/aspect ratios if multi-platform, Arabic frame check, no invented UI states.

6. CLEANUP (for real-account demos)
   If recorded against a real backend (not a disposable dev/staging environment): delete
   the demo account(s) created during capture before or right after export. Reusing one
   real phone number across sequential single-account demos (e.g. Student signup, delete,
   then Teacher signup) is fine — reusing it for two roles that must exist SIMULTANEOUS
   in the same video (e.g. a Parent redeeming a Student's live link code) is not possible
   with one number, since this schema enforces one user per phone number. That case needs
   two real numbers open at once, or two separate recording passes cut together.
```

## When to reach for this vs. plain `recordly-launch`

- **Plain `recordly-launch` capture only** — a quick internal reference clip, no polish needed.
- **This skill** — anything going out publicly or to real users/customers as a tutorial,
  onboarding video, or feature walkthrough: needs the motion layer + narration to read as
  a produced piece, not a raw screen grab.

## Known constraints (don't relearn these)

- Recordly's own zoom/annotate/voiceover/export automation does not exist yet — always plan
  the edit as a Remotion build, never as a `recordly edit`/`recordly export` CLI call.
- One phone number = one account (schema-level unique constraint) — plan multi-role scenes
  (parent+student, two simultaneous roles) around two real numbers or two recording passes,
  not one reused number.
- Real WhatsApp OTP costs a real send — reuse the standing test number
  (`0968304197`, gateway's own, self-send/free/no-report-risk) for single-role passes; a
  second role needed simultaneously needs a second real number, ask the user for it rather
  than guessing one.
- Never fabricate a click position, UI state, or diagram geometry not actually seen in the
  raw footage — same standing rule as every other production skill in this stack.

## See also

- [recordly-launch](../recordly-launch/SKILL.md) — the real capture CLI
- [recordly-edit](../recordly-edit/SKILL.md) / [recordly-export](../recordly-export/SKILL.md) —
  read these for the UI-only reality, not as a CLI reference
- [remotion-video-creation] — the actual editing/motion engine this skill routes to
- [omnivoice] — Arabic narration engine, local, zero cost
- `RECORDLY_REAL_API_REFERENCE.md` (Second_Brain/30-Resources/Capabilities/) — real zoom/padding math if replicating Recordly's own visual language inside Remotion
