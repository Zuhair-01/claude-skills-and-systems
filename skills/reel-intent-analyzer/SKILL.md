---
name: reel-intent-analyzer
description: "Analyze a video/reel link (Instagram Reels, TikTok, YouTube Shorts, or any yt-dlp URL) to find the content and goal/intent behind it -- hook, structure, CTA, what to do with it (clip-platform repurpose, script extraction). Also handles dev/tutorial/build videos: pulls repo links, stack, and techniques shown to use as training/reference material and close gaps in an existing project. No paid API keys needed. Use for: 'what is this reel about', 'what's the goal here', 'is this sellable as UGC', 'extract the hook formula', 'what repo/stack is this', 'how do I add this to my project'."
description_full: |
  Analyze a video/reel link (Instagram Reels, TikTok, YouTube Shorts, or any yt-dlp-supported URL)
  to figure out what the user wants FROM it — the content, the goal/intent behind it, the hook,
  structure, and what to do with it (e.g. replicate for clip-platform, extract a script, pull the
  offer/CTA, judge if it's worth cutting into clips). Works standalone, with no paid API keys.
  Use when: (1) user pastes a reel/short/TikTok link and asks "what is this about / what's the
  goal here / break this down", (2) user gives a link + a specific prompt ("is this sellable as a
  UGC ad", "extract the hook formula", "what's the CTA"), (3) user wants a video's content and
  intent turned into a written brief before repurposing it, (4) the video is dev/tutorial/build
  content (coding demo, tool walkthrough, "how I built X") and the goal is to pull it in as
  reference/training material — extract the repo links, stack, and techniques shown and map them
  against an existing project to find and close gaps.
---

# Reel Intent Analyzer

Turns a video link + your prompt into: **what the video actually is** (content) and **what its
goal is** (intent) — grounded in real frames and real transcript, not a guess from the caption.

No paid video-AI API required. Uses `yt-dlp` (download) + `ffmpeg` (keyframes) + Claude's native
multimodal vision (Read tool) + the video's own subtitles/caption text.

## When to use vs. `seek-and-analyze-video`

- Use **this skill** by default — zero external API keys, works offline once downloaded.
- Use `seek-and-analyze-video` (Memories.ai) only if the user explicitly wants persistent
  cross-session video search/memory, or asks to search TikTok/IG for videos by topic (discovery,
  not analysis of a specific link).
- Use `style-clone` instead whenever the ask is about a *creator* rather than a video —
  learning how someone edits, cloning their style onto the user's own footage, or sourcing
  b-roll for a script. This skill reads one video's content and intent; `style-clone`
  studies a whole profile, keeps a validated template in the vault's Style Library, and
  cuts the finished piece. If a request starts here and turns into "now make mine look
  like theirs", hand over (CLAUDE.md Rule 14).

## Workflow

### Perception tools (built 2026-09-26): use these BEFORE eyeballing frames

`python "$SECOND_BRAIN\Workflow\30 - Resources\Scripts\perceive.py" <video.mp4> --out <dir> [--vlm] [--no-speech]` writes `report.md` + `report.json` + contact sheets: shot/cut times (frame-difference peaks, catches dissolves and overlays), the editing cadence the cuts follow (bpm-equivalent, regularity, whether accents of the music sit on it), loudness/peak/LRA, band energy, tempo, voice via **VAD** (music-only reels report "no speech"), SFX-like accents off the beat, **OCR of on-screen text with first/last-seen times and text height** (headlines vs card UI micro-text), palette, optional per-shot captions from the local moondream VLM. Use it for reference studies AND for QA of our own renders (cadence, text size, loudness). Then LOOK at the sheets.
`python ...\Scripts\listen.py take.wav [more takes] --text "expected line" --lang ar` checks voice takes: normalised word-by-word comparison (harakat folded), dropped/wrong/extra words, Whisper confidence, unintended internal pauses, level/clipping; ranks several takes. It cannot judge naturalness (the user's ear); for spectrogram artifacts also see `voice_lab/ears_check.py`.
Pitfalls these encode: Whisper hallucinates phrases ("We'll be right back") on music, so never trust a transcript without VAD; `ffmpeg scene>0.30` misses dissolves and overlay pop-ups (measured: zero cuts found in a reel with 9); librosa's tempo can be an octave or 3:2 off, the cuts' own cadence is the truth; sampled frames every 0.5 s can fake a "cuts on the beat" story; `ffmpeg ebur128` prints per frame, parse only the Summary block; Instagram view counts are often not returned by yt-dlp (say so, never invent). OCR needs `pip install rapidocr-onnxruntime` (installed, 12 MB); Arabic OCR is untested.

### Step 0 — Read the ask, pick a mode

Before touching the video, decide what "what I want from it" means here:
- No extra prompt given → default to a full **marketing/content breakdown** (Step 4 template).
- A specific marketing-style prompt ("is this a good clip candidate", "what's the offer", "write
  me a hook like this one") → the whole analysis answers THAT question; the generic breakdown
  becomes supporting evidence, not the deliverable.
- The video is dev/tutorial/build content, or the prompt is about learning/replicating/closing a
  gap in one of your own projects ("what repo is this", "how do I add this to clip-platform",
  "what's this stack") → switch to **Dev/Reference mode** (Step 4b) instead of the marketing
  template.

### Step 1 — Get the video (URL or already-local file)

**If given a URL:**
```bash
# ALWAYS wipe first — this is a fixed path reused across runs. yt-dlp skips
# downloading when a same-named file already exists, so a stale video.mp4 from
# a PRIOR unrelated analysis gets silently reused for the new URL while
# meta.json (which has no such collision) correctly reflects the new one —
# you end up analyzing the wrong video with the right caption. Caught
# 2026-09-29 analyzing a freelancing reel and getting a stale Coca-Cola promo.
rm -rf /tmp/reel-analysis && mkdir -p /tmp/reel-analysis && cd /tmp/reel-analysis
yt-dlp "URL" -o "video.%(ext)s" --merge-output-format mp4
yt-dlp "URL" --write-subs --write-auto-subs --sub-langs "en.*,ar.*" --skip-download -o "video" 2>/dev/null || true
yt-dlp "URL" --dump-json --no-download > meta.json
```

**If given an already-downloaded local file** (e.g. a batch of reels saved to
a vault/resources folder for later processing): skip the download, copy or
symlink it into the working dir as `video.mp4`, and skip `meta.json`
entirely — there's no caption/view-count metadata for a bare local file, so
go straight to frames + transcript and don't invent numbers that aren't
there. Filenames that look like platform media IDs (e.g. `Da0iDR4vl5M.mp4`)
are almost always Instagram/TikTok exports — treat as Reels/Shorts format
by default unless told otherwise.

Notes:
- Instagram Reels sometimes need a logged-in cookie for private/age-gated content:
  `--cookies-from-browser chrome`. Try without first.
- `meta.json` gives you `description`, `title`, `uploader`, `duration`, `view_count`,
  `like_count` — read these, they often state the goal directly (caption = stated intent).
- If subs/auto-subs come back empty (most Reels have no captions track), don't block — move to
  Step 2b for audio transcript.

### Step 2 — Get the transcript

**2a. If subtitles downloaded:** read the `.vtt`/`.srt` file directly (Read tool).

**2b. If no subtitles (common for Reels/TikTok):** extract audio and transcribe.

```bash
ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3 -y
```

Then transcribe with whatever local/cloud STT is already set up in this environment (check for a
whisper install first: `which whisper` or `pip show openai-whisper`). If nothing is set up, skip
transcript and rely on visual analysis + on-screen text burned into frames — don't stop the task
to install a new dependency unless the user asks for word-perfect transcript.

**Windows + `openai-whisper` CLI + Arabic/non-Latin transcript → set `PYTHONIOENCODING=utf-8`
first.** The Windows terminal's default cp1252 console cannot print Arabic and whisper's CLI
prints each line as it transcribes, so it crashes mid-run ("Skipping audio.mp3 due to
UnicodeEncodeError") even though the model itself works fine — the fix is encoding on stdout,
not a model or language problem. Run it as `PYTHONIOENCODING=utf-8 whisper audio.mp3 --language
Arabic --model small --output_format txt --output_dir .`; same fix applies to any Python one-liner
that prints Arabic on this box (write to a UTF-8-opened file instead of `print()` when in doubt).

### Step 3 — Extract keyframes

Sample enough frames to see the whole arc — hook, mid, payoff/CTA — without flooding context.
For short-form (typically 15–90s), 1 frame every 1.5–2s is plenty:

```bash
ffmpeg -i video.mp4 -vf "fps=1/1.5,scale=480:-1" -q:v 3 frame_%03d.jpg
```

For longer videos (>3 min), switch to scene-change detection instead of fixed fps so you don't
burn context on near-duplicate frames:

```bash
ffmpeg -i video.mp4 -vf "select='gt(scene,0.35)',scale=480:-1" -vsync vfr -q:v 3 frame_%03d.jpg
```

Cap it: if you get more than ~15-18 frames, thin them out (keep every Nth) before reading — you
don't need every frame, you need enough to reconstruct the beat structure.

### Step 4 — Read and analyze

Use the Read tool on the frame images directly (multimodal) plus the transcript/caption text.
Reconstruct the video as a sequence of beats: what's shown, what's said/on-screen-text, in order.

Default breakdown template (skip/reorder sections the user's prompt didn't ask for):

1. **Content** — what actually happens, beat by beat (hook → build → payoff/CTA), 1 line each.
2. **Format** — talking head / voiceover-over-broll / text-meme / tutorial / skit / UGC-ad style, etc.
3. **Hook** (first 1-3s) — the exact line or visual that's meant to stop the scroll.
4. **Goal/intent** — what the creator wants the viewer to do or feel: sell a product, build
   authority, get saves/shares, drive to link in bio, entertain, educate, recruit, etc. Base this
   on the CTA, caption, and what's actually being pitched — not a generic guess.
5. **CTA** — explicit ask, if any (follow, buy, comment, link in bio, DM).
6. **Answer to the user's specific prompt**, if one was given — put this FIRST in the reply if
   present, the rest is supporting context.

### Step 4b — Dev/Reference mode (tutorial, build, tool-demo content)

Goal here isn't marketing analysis — it's turning the video into something you can act on inside
a real project. Pull from frames, transcript, `meta.json` description, and pinned comment if
visible (that's where creators dump repo links):

1. **What's being built/shown** — the actual feature or technique, in plain terms.
2. **Stack/tools named or visible** — libraries, frameworks, CLI tools, on-screen editor/terminal
   text. Read code visible in frames literally, don't paraphrase syntax.
3. **Repo/link extraction** — pull any `github.com/...` URL from the description, comments, or
   on-screen text. If a repo is named but no URL given, search for it:
   `gh search repos "<name>" --limit 5` or `WebSearch`.
4. **Gap check against your project** — if the user names a project (or it's obvious from
   context, e.g. clip-platform, OmniRoute, AXIS), compare what the video shows against that
   project's current state before claiming it's missing:
   - `grep`/`Glob` the project for the relevant feature/pattern already existing
   - `git log --oneline -20` in that project for recent related work
   - Only then report it as a real gap, not an assumed one
5. **If cloning the repo is useful**, do it into the scratchpad (or ask where, if it's meant to be
   merged into an existing project) — see repo-download below. Don't install/run untrusted repo
   code without confirming with the user first.

**Cloning a referenced repo:**

```bash
gh repo clone owner/repo /path/to/scratchpad/repo-name
# or, no gh auth needed:
git clone https://github.com/owner/repo.git /path/to/scratchpad/repo-name
```

Then skim `README.md` + top-level structure (`Glob`) before deciding what's actually reusable —
don't dump the whole repo into context.

Output for this mode: a short brief — what it does, the stack, the repo link (if any), what's
already covered in your project vs. what's the actual gap, and next step if you want to close it.

### Step 5 — Cleanup

Delete `/tmp/reel-analysis` contents when done unless the user wants the downloaded file kept
(e.g. they're about to feed it into clip-platform or another editing pipeline — then tell them
the path instead of deleting).

## Common pitfalls

- **Treating the caption as ground truth for content.** Captions are often bait/unrelated to what
  the video shows — always verify against frames.
- **Over-sampling frames.** Reading 40 frames of a 20s reel wastes context for no extra signal;
  stick to the fps/scene-change guidance above.
- **Skipping the meta.json.** `view_count`/`like_count`/`comment_count` are useful signal for
  "did this actually work" if the user's prompt is about virality or replication.
- **Private/login-walled Reels.** If `yt-dlp` fails auth, fall back to
  `mcp__claude-in-chrome` (navigate to the reel, screenshot the visible frames, read on-screen
  caption/comments) rather than giving up — load the Chrome tools via ToolSearch first.

## Related

- `video-download` — the yt-dlp reference this skill leans on for flags/troubleshooting.
- `ffmpeg` — frame/audio extraction reference.
- `seek-and-analyze-video` — alternative when persistent video memory/search across sessions is
  actually wanted (needs Memories.ai API key).
- `youtube-shorts` / `video-shortform` — for the reverse direction, once intent is known and the
  ask shifts to "now make one like this."
