---
name: text-hook-power-word-mining
description: Mine the highest-performing on-screen TITLE TEXT (text hooks) in a niche, extract the winning hook FORMATS and POWER PHRASES, then remix them into new title-text options for a given topic — the local, no-subscription version of Kallaway's "Text Hook Power Word Mining" skill. Use when asked to write/improve a reel/Short/TikTok title text or on-screen hook overlay, to "mine power words", "find the best hooks in my niche", "text hook", "title text", "on-screen hook", "hook overlay", "comment TEXT", "power phrase", "remix hooks", "why isn't my hook working", or to build a swipe file / hook database from competitor videos. Pairs with retention-toolkit (the 30-technique spine) and social-growth-science (algorithm mechanics). NOT for the spoken hook alone (use retention-toolkit) or full scripts (use reel-production-pipeline / content-factory).
metadata:
  version: 1.0.0
  written_by: opencode
  source: Kallaway text-hook system (see vault doc in Sources)
---

# text-hook-power-word-mining

Turns any niche into a data-backed **title-text generator**. It is the manual, local
implementation of Kallaway's paid Sandcastles "Text Hook Power Word Mining" skill:
curate top performers → extract their on-screen title text verbatim → mine the recurring
**formats** + **power phrases** → remix → emit new title-text options that obey the design
and writing rules. No Sandcastles subscription required.

> Canonical framework (read it): `Second_Brain/Workflow/30 - Resources/Research/Kallaway_Text_Hook_System_2026-10-01.md`.
> This skill is the *operational* layer; don't fork that doc, point to it.

## 0. Non-negotiables
- **Real facts only.** Any number, dollar, day count, or result must be real. Use `[INSERT]` until it is. Never fabricate specificity to make a hook land.
- **One CTA per video**, tied to the money path.
- **The title text is the highest-leverage part of the hook** — eyes hunt for text and parse power phrases faster than they process the image. Spend your time here.
- Output must pass the **Gate** (§5) before you present it.

## 1. The framework in one screen (from Kallaway)
- **Text hook** = the designed on-screen *title text*, NOT the word-for-word captions.
- **Formula: `Subject repeater` + ONE of** → **Pain Point Reminder** | **Dream Outcome Teaser** | **Future Potential State Change**. (Kallaway's carousel says there are **6 categories**; only these **3** are documented — the other 3 are a known gap, fill from the original carousel video.)
- Names / proper nouns / jargon are attention magnets (especially capitalised).
- **Power word/phrase** = a **1–3 word** cluster that is a heat-seeking missile for attention ("social media machine", "scientifically impossible to skip").
- **Hook maxing Level 1** = remix the **format** (grammatical skeleton). **Level 2** = remix the **power words** (twist, keep the psychology). Combine both.
- Validation signal: a power phrase appearing in **2+** of a creator's top videos is a repeatable pattern, not a fluke.

## 2. Workflow

### Step 1 — COLLECT (30–50 top performers)
Pick the highest-performing videos in the niche (last 3–6 months, sort by outlier score / views).
- **Best input:** a curated list of 30–50 title texts (you or the user already have the videos).
- **From a link (single post/reel, no login):**
  ```powershell
  yt-dlp --skip-download --write-info-json --write-pages --ignore-no-formats-error -o r "<post_url>"
  # -> r.info.json (caption) and *_api_graphql.dump (caption + comments + metrics)
  yt-dlp -o reel.mp4 "<reel_url>"                       # video, when the title text is burned in
  ffmpeg -i reel.mp4 -vf "fps=1/1.5,scale=360:-1" frames/f_%03d.jpg
  ```
  Then **Read the frames** (vision) to transcribe the title text — no OCR install needed. Tile a contact sheet for speed: `ffmpeg -i frames/f_%03d.jpg -vf "scale=200:-1,tile=5x5" sheet_%02d.jpg`.
- **From a profile grid / many posts:** use **agent-browser** when installed (`agent-browser open …; snapshot -i; screenshot --annotate; record start`), else Playwright (`playwright_browser_*`), else curate by hand. Note in the output which method was used.
- Save everything into a **swipe file** (vault table): `title_text | source (handle/url) | metric (views/likes) | category | format | power_phrases`.

### Step 2 — EXTRACT
Transcribe each title text **verbatim** (exact line breaks and caps). Tag each:
- `subject_repeater`? (the name/term)
- `category`: pain / dream / future-state / other
- `power_phrases`: the 1–3 word clusters
- `lines`: how it broke across 1–2 lines

### Step 3 — MINE (cluster)
- **Formats:** strip variables → the grammatical skeleton (e.g. `“[Subject] just changed [domain] forever”`, `“Stop [pain]. [Do X] instead.”`, `“How to [outcome] without [pain]”`). Rank by recurrence × performance.
- **Power phrases:** list recurring clusters, rank by recurrence × performance. Keep a running **Power-Word Bank** in the vault.

### Step 4 — REMIX
- **Level 1 (formats):** swap the variables for the current topic.
- **Level 2 (power words):** for each winning phrase, generate **5 alternative twists** that keep the psychology (e.g. *scientifically impossible to skip* → *neurochemically impossible to skip / psychologically impossible to resist*).
- **Combine:** twisted format × twisted power words. Never copy-paste a phrase verbatim — that reads as corny.

### Step 5 — GENERATE
For the given topic, emit **3–5 title-text options** (not one). Each must be data-backed (name the format + power words borrowed) and obey the design + writing rules.

### Step 6 — PERSIST
- Append new power phrases / formats to the **Power-Word Bank**.
- Log which phrases recur across **our own** top posts (the validation signal moves to our data once we have volume).

## 3. Design rules (apply to every output)
1. Font must be extremely readable.
2. Place it ~**a third of the way down** from the top (or above your head; wherever eyes hit first).
3. **Don't block eyes or mouth.**
4. **Two lines max** (3 only with premium type where one line dominates — never 3 equal lines).
5. Break the line where the phrasing **naturally groups** (never mid-phrase).

## 4. Writing rules (apply to every output)
1. **Be specific** — real numbers/dollars/days (`$2,700` > "a couple thousand"). `[INSERT]` if not real.
2. **Use power words** — 1–3 word heat-seeking clusters.
3. **No generic or transition words** (*and, or, that, but, therefore*).
4. **No punctuation** except quotation marks and parentheses.
- Timing note (creation side): the title text must stay on screen **~3 seconds** — don't cut it before it can be read.

## 5. Gate (run before presenting; own it)
- [ ] Subject identifiable instantly in line 1
- [ ] Exactly one of {pain / dream / future-state / other category} present
- [ ] ≥1 genuine power word/phrase
- [ ] Specific (real number or concrete noun) — no vague filler
- [ ] No banned transition words; no punctuation beyond quotes/parens
- [ ] ≤2 lines; breakpoint is on a natural phrase boundary
- [ ] Nothing fabricated (`[INSERT]` used where the fact isn't real yet)

## 6. Output format
1. **Mined winners** — top 5 formats + top 8 power phrases (with source + metric), 2-line table each.
2. **3–5 title-text options** for the topic. For each: the title text (with the line break shown) · category · format borrowed · power words used · one-line rationale.
3. **Gate result** — pass/fail per option.
4. **Design placement note** — where to put it on the frame; hold ~3s.
5. **Method used** — how the seed titles were collected; what was real vs `[INSERT]`.

## 7. Integration / routing
- `retention-toolkit` — the spoken-hook spine + beat map (this skill only owns the title text).
- `social-growth-science` — algorithm / reach mechanics.
- `motion-reel-pipeline`, `reel-production-pipeline`, `content-factory` — where the title text gets produced into a real reel.
- `marketing-psychology` — the psychology behind the power words.
- English-first for the personal brand; **Alwazour = Arabic/Levantine** — mine Arabic competitors' hooks, don't translate English ones (power phrases must be native).

## 8. Sources
- Kallaway, *The Psychology of Killer Hooks* (YT `pNIYikmYsyw`, 2026-08-05) + 5-slide "Text Hook Power Word Mining" IG carousel.
- Vault: `30 - Resources/Research/Kallaway_Text_Hook_System_2026-10-01.md` (full framework + utilization).
- Method precedent: `30 - Resources/Research/JEV_6_Projects_Instagram_Decode_2026-10-01.md` (yt-dlp → graphql dump → frames).

## 9. Open items
- Fill the **3 undocumented text-hook categories** (carousel says 6; only 3 named) from the original carousel video/post.
- Optionally wire an **agent-browser** collector once it is installed (see `SelfHosted_Agent_Stack_isaacdyor_reel_2026-10-01.md`).
