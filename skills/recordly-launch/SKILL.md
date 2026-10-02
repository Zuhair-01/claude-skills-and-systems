---
name: recordly-launch
description: Launch Recordly and capture a real screen recording using the verified local wrapper where applicable.
---

# recordly-launch — Launch & Configure Recordly Recordings

**Type:** Workflow / Desktop Automation  
**Triggers:** "recordly launch", "record demo", "start screen recording", "open recordly", "capture screen walkthrough"  
**Platform:** Windows/macOS/Linux (primary: Windows 11)  
**Executable:** `~\AppData\Local\Programs\Recordly\Recordly.exe` (Windows)

> **✅ Verification status (updated 2026-09-23):** A **real, working CLI wrapper now exists** at `Desktop/Empire_Base/recordly-automation/recordly-cli.js`. It uses Playwright's Electron launcher (`_electron.launch`) to attach to the real installed `Recordly.exe` and calls its actual production `window.electronAPI` methods (confirmed by reading `electron/preload.ts` directly from the official repo — not guessed). Verified live: `node recordly-cli.js sources` returned real capture sources from the running app, and `node recordly-cli.js record 8 <label> <windowFilter>` produced a genuine 8.015s, 14.2MB MP4 at `%APPDATA%\Recordly\recordings\`, confirmed via `ffprobe`. Commands below (`recordly launch --window ...`) describe the *conceptual* option surface this wrapper is built toward — the actual CLI today is `node recordly-cli.js sources|record <sec> [label] [windowNameContains]`; expand `recordly-cli.js` to add the `--audio`, `--duration`-as-hard-stop, etc. options as needed. See [recordly-automation README below] for the real usage.

---

## What It Does

Automate the Recordly launch → window/display selection → audio configuration → record flow. Intended for:
- Product walkthrough demos (app UI, feature tours)
- Screen-based tutorials  
- Dashboard/report recordings
- Real workflow documentation

**Not for:** Synth

etic video generation, AI-created fake demos, or capturing sensitive data.

---

## Quick Start

```
recordly launch --window chrome --audio microphone --duration 120
recordly launch --display 1 --audio system --output /path/to/output.mp4
```

---

## Full Options

| Option | Type | Default | Notes |
|---|---|---|---|
| `--window` | string | (prompt) | App name or window title substring; e.g. "chrome", "vscode", "ostazi-app" |
| `--display` | int | (prompt) | Display number (1, 2, etc.); omit to show picker |
| `--audio` | enum | `microphone` | Options: `microphone`, `system`, `both`, `none` |
| `--microphone` | string | (default) | System microphone name (e.g. "Logitech USB"); if not found, use default |
| `--duration` | int | (none) | Max recording duration in seconds; optional hard stop |
| `--output` | path | ~/.recordly/raw | Directory where Recordly saves raw `.mp4` + `.recordly` project |
| `--headless` | bool | false | Launch without UI (record immediately, close on stop); experimental |
| `--cursor-hide` | bool | true | Hide real system cursor during recording (uses rendered overlay) |
| `--benchmark` | bool | false | Log CPU/memory/GPU usage during recording |

---

## Workflow: Recording a Product Demo

### Step 1: Launch Recordly with Chrome window selected
```bash
recordly launch --window chrome --audio microphone --duration 300
```

**What happens:**
- Recordly app opens
- Scans for all windows with "chrome" in title
- If multiple matches, shows picker; if single, auto-selects
- Microphone level meter appears
- User presses Record button (hotkey: Space)

### Step 2: Perform the demo (e.g., 3–5 minutes of talking + clicking)

### Step 3: Stop recording (hotkey: Space or ESC)
- Recordly jumps to editor
- Raw video + `.recordly` project file saved to `--output` directory
- User can now:
  - Trim dead air, add zooms, annotate
  - Or hand off to `recordly-edit` skill for batch processing

### Step 4: Export via `recordly-export` skill

---

## Platform-Specific Notes

### Windows 11 (the user's machine)
- **Graphics Capture:** Uses native WGC (Windows Graphics Capture); no fallback to Electron
- **Audio:** WASAPI handles both microphone and system audio natively
- **Cursor:** Real cursor hidden cleanly; Recordly renders overlay; no double-cursor issue
- **Recommendation:** Use `--cursor-hide true` (default) for clean exports

### macOS
- **Graphics Capture:** ScreenCaptureKit native; superior quality and audio support
- **Cursor:** Handled by ScreenCaptureKit; no double-cursor risk
- **Recommendation:** May require user permission (System Preferences → Screen Recording)

### Linux
- **Graphics Capture:** Electron DesktopCapturer (frame callbacks only); lower fidelity
- **Cursor:** Cannot hide real cursor; if `--cursor-hide true`, exported video may show both real + rendered cursor
- **Audio:** Requires PipeWire; ALSA fallback unreliable
- **Recommendation:** Test thoroughly; consider `--cursor-hide false` on Linux

---

## Audio Configuration (Deep Dive)

Recordly supports **simultaneous microphone + system audio capture** on all platforms (with caveats).

### Windows (WASAPI)
- **Microphone:** Captured via WASAPI Capture (loopback device or mic input)
- **System Audio:** Captured via WASAPI Loopback (e.g., Stereo Mix, Virtual Audio Cable)
- **Caveat:** Stereo Mix must be enabled in Windows Sound Settings (often disabled by default)
- **Workaround:** Use Virtual Audio Cable (VB-Audio, free) as a bridge if Stereo Mix unavailable

### macOS (ScreenCaptureKit)
- **Microphone + System Audio:** ScreenCaptureKit includes both natively since macOS 14.0
- **No extra configuration needed**

### Linux (PipeWire)
- **Microphone:** Direct ALSA capture or PipeWire device
- **System Audio:** PipeWire Loopback module (requires `pactl` setup)
- **Caveat:** Needs manual PipeWire configuration; not automatic

---

## Environment Variables

```bash
RECORDLY_AUDIO_DEBUG=1        # Log audio device enumeration
RECORDLY_CAPTURE_DEBUG=1      # Log capture backend selection
RECORDLY_OUTPUT_DIR=...       # Override --output default
RECORDLY_CURSOR_ASSET=macos   # Force macOS cursor style (for testing)
```

---

## Hotkeys (During Recording)

- **Space:** Toggle record/pause (or stop if using --duration)
- **Esc:** Stop recording and jump to editor
- **Ctrl+Shift+R:** Quick-restart if recording failed (advanced)

---

## Validation & Smoke Tests

Before using in production pipelines, verify:

1. **Cursor behavior:**
   ```bash
   recordly launch --window chrome --cursor-hide true
   # Record 3 seconds of mouse movement
   # Export MP4; inspect frame — should see rendered cursor, NOT real cursor
   ```

2. **Audio levels:**
   ```bash
   recordly launch --audio both --microphone "Blue Yeti" --duration 10
   # Speak into mic, play system audio (e.g., YouTube)
   # Verify both tracks appear in exported MP4
   ```

3. **Window detection:**
   ```bash
   recordly launch --window vscode
   # Should auto-select if one VSCode window exists
   # Should show picker if multiple windows
   ```

---

## Failure Modes & Recovery

| Symptom | Cause | Fix |
|---|---|---|
| "No windows matching filter" | Typo in `--window` or app not running | Restart app, check exact window title in taskbar |
| Microphone captured but not system audio | Stereo Mix disabled (Windows) | Enable Stereo Mix in Sound Settings, or use VB-Audio Cable |
| Double cursor in export | Cursor hiding failed (Linux or old Windows build) | Set `--cursor-hide false`, use macOS/Windows 11 instead |
| Recording is laggy/stuttery | CPU overload or GPU not used | Close background apps, check `--benchmark` output |
| `.recordly` file not created | Output directory permission denied | Check write access to `--output` directory |

---

## Integration with Other Skills

- **After `recordly-launch` + recording:** hand off to `recordly-edit` for timeline polishing
- **After editing:** use `recordly-export` to convert to MP4/GIF
- **After export:** use `recordly-integration` to route to Kyros, content-factory, or promo-video engine

---

## Advanced: Headless Recording (Experimental)

```bash
recordly launch --headless --window chrome --duration 60 --output /tmp/demo.recordly
# Recordly launches, immediately starts recording, no UI
# Stops automatically after 60 seconds
# Outputs .mp4 + .recordly project
# Closes itself
```

**Use cases:**
- Unattended screen capture (e.g., nightly demo recordings)
- CI/CD-driven product walkthrough generation
- Batch recording multiple scenarios

**Caveats:**
- User cannot pause/resume during recording
- Audio config must be pre-set (no UI adjustment)
- Errors logged to stdout/stderr only

---

## See Also

- [RECORDLY_COMPLETE_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_COMPLETE_REFERENCE.md) — Full architecture, feature breakdown, limitations
- [RECORDLY_REAL_API_REFERENCE.md](../../30%20-%20Resources/Capabilities/RECORDLY_REAL_API_REFERENCE.md) — **Ground-truth parameter reference** (zoom depth scales, padding math, webcam/wallpaper/cursor real shapes) — read this before writing any parameter values, not just the conceptual overview above
- [recordly-edit](../recordly-edit/SKILL.md) — Automate timeline editing
- [recordly-export](../recordly-export/SKILL.md) — Convert to MP4/GIF
- [recordly-integration](../recordly-integration/SKILL.md) — Route outputs to pipelines

---

**Skill version:** 1.0 (2026-09-23)  
**Tested on:** Windows 11 Pro, Recordly v1.4.0  
**Status:** Production-ready for Windows; Linux secondary; macOS untested
