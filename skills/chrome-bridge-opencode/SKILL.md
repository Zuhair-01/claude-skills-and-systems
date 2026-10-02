---
name: chrome-bridge-opencode
description: Drive the user's real Chrome browser from ANY Claude Code session via the local claude-chrome-mcp bridge (node CLI, no MCP registration needed). Use when asked to open/browse/click/fill/screenshot/scrape/debug web pages in Chrome, verify UI work, capture network/console output, record GIFs of flows, or automate anything in the user's actual logged-in browser. Windows machine - paths are absolute.
---

# Chrome Bridge (OpenCode-installed) — usage from Claude Code

## What this is

A local bridge (`claude-chrome-mcp v2.1.0` + custom command layer) installed by an
OpenCode session on 2026-08-24 that lets AI sessions drive the user's REAL Chrome
via the official Claude extension. Claude Code does NOT need its own `/chrome`
integration for this - the bridge is an authenticated local HTTP MCP endpoint plus
a high-level CLI that composes all 14 tools into one-shot verbs.

**Primary interface — always prefer the CLI:**

```
node ~\.local\share\claude-chrome-mcp\chrome.mjs <verb> [args]
```

Works from any session (Claude Code, OpenCode, Codex) because it's just node +
localhost HTTP. Auth token is read from disk automatically - never print it,
never commit it anywhere.

## Verb reference

| Verb | Example | Notes |
|---|---|---|
| `tabs` | `chrome.mjs tabs` | list tabs in the automation group |
| `open <url>` | `chrome.mjs open https://ostazi-edu.com` | new tab + settle + screenshot |
| `goto/back/forward` | `chrome.mjs goto https://x.com 3` | optional tab id |
| `see [tab]` | `chrome.mjs see` | PNG saved to `%TEMP%\opencode\chrome\`, path printed - READ the file to actually look |
| `zoom x0 y0 x1 y1` | `chrome.mjs zoom 100 200 500 400` | zoomed screenshot |
| `read [tab]` | `chrome.mjs read` | full page text |
| `tree [tab] interactive` | | accessibility tree; refs (`ref_N`) drive everything |
| `find "<query>"` | `chrome.mjs find "search bar"` | natural-language element search |
| `click "<query>\|ref_N"` | `chrome.mjs click "login button"` | find -> scroll_to -> click |
| `write "<query>" <val>` | `chrome.mjs write "email field" a@b.c` | checkbox/select aware |
| `fill '<json>'` | `chrome.mjs fill '{"name":"the user","phone":"+963..."}'` | multi-field one shot |
| `type`, `press`, `hover`, `scroll` | `press "Enter"`, `press "ctrl+a Delete"` | |
| `waitfor "<query>" [sec]` | `chrome.mjs waitfor "submit button" 30` | poll until present |
| `js "<code>"` | `chrome.mjs js "document.title"` | execute in page context |
| `console [--errors] [pattern]` | | page console messages |
| `net [urlPattern]` | `chrome.mjs net /api/` | recent network requests |
| `record start\|stop\|export\|clear` | | GIF recording of the session |

## Workflow patterns that work well

1. **Verify frontend changes**: `open` the local URL -> `see` -> Read the PNG ->
   `console --errors` -> fix -> repeat.
2. **Deterministic clicking on complex pages**: `tree <tab> interactive`, pick the
   exact `ref_N`, `click ref_N`. Coordinates are last resort.
3. **Dynamic pages**: `waitfor "<element description>" 30` before interacting.
4. **Debugging APIs**: `net /api/` after reproducing, `console --errors`.

## Preconditions & ownership (IMPORTANT)

- The bridge server ONLY runs while Chrome is running AND the extension has
  connected (user clicks the Claude extension icon once after Chrome start).
- The extension serves ONE master at a time. Currently OpenCode owns the slot.
  If the user says Claude's own `/chrome` should take over, they run:
  `powershell -File ~\.local\bin\chrome-mcp-toggle.ps1` (then restart Chrome).
  While flipped to Claude Code's built-in integration, THIS bridge is offline -
  tell the user, don't fight it.

## Failures -> fixes

Full runbook (same content as OpenCode's chrome-bridge-troubleshooting skill):
`~\.config\opencode\skills\chrome-bridge-troubleshooting\SKILL.md`

Quick triage:
```
powershell -ExecutionPolicy Bypass -File ~\.local\bin\chrome-bridge-doctor.ps1
```
Self-heals registry drift, rival manifests, squatters, token desync; ends
HEALTHY or with ONE human action. Add `-RotateToken` to rotate credentials.
Then `mcp-call.mjs status` for a raw handshake probe.
`bridge_down` -> Chrome closed / extension not clicked / slot toggled away.

## Security boundaries

- Server binds 127.0.0.1 only, bearer token required (256-bit, auto-generated).
- Token lives ONLY in `~\.claude-chrome-mcp\claude-chrome-mcp-native-host.bat`
  and `~\.config\opencode\opencode.jsonc`. Never echo it, never write it into
  repos/docs/screenshots.
- You are driving the user's REAL logged-in browser: never enter credentials,
  never submit payments, never touch banking/gov sites without explicit
  instruction; announce before acting on logged-in sessions.
