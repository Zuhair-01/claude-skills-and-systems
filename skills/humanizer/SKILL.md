---
name: humanizer
description: >-
  Humanize outward-facing copy — remove AI writing tells via the two-pass
  pipeline (surface pass then structural pass). Use whenever writing or
  reviewing captions, carousel copy, reel scripts, product copy, listings,
  posts, emails, or lessons that must read as human — or when text sounds
  like AI, needs de-slopping, or must pass the pre-post copy gate.
  Triggers include humanize, de-slop, AI tells, caption copy, slide copy,
  reel script, product copy, pre-post check, copy gate.
metadata:
  version: 1.0.0
  written_by: opencode
  stack: Empire_Base\external-repos\humanizer-stack (cloned 2026-10-01, MIT own-work + CC BY-SA upstream portions — internal use OK, NOT for factory resale per the rights gate)
  wiring_doc: Second_Brain\Workflow\30 - Resources\Research\Humanizer_Stack_Wiring_2026-10-01.md
---

# Humanizer — always-on copy gate (pointer skill, 1 context slot)

The heavy bodies live in the cloned repo — this skill is the router + the order of operations. Never fork their content here.

## When to run (always, for outward-facing text)
Any caption, carousel slide copy, reel script, product description, listing, post, email, or lesson **before it ships**. Internal docs/notes are exempt (the scanners will fire constantly on text nobody needs to be human).

## The pipeline (in order — surface first, structural second, voice last)
Source of truth: `Empire_Base\external-repos\humanizer-stack\docs\PIPELINE.md`.

1. **Pass 1 — surface** (`skills/humanizer/SKILL.md` in the clone): vocab, punctuation, phrasing, hype copy, rule of three, negative parallelism. English tells — applies directly to EN copy; for Arabic copy use `Capabilities\Arabic_Copy_Tells.md` instead (same job, Arabic fingerprints).
2. **Pass 2 — structural** (`skills/structural-humanizer/SKILL.md` in the clone): the 6 audits, one at a time, against the SKELETON not the prose (theme explicitness, tidiness, emotion mode, reference specificity, reader engagement, shape convergence). Transfers across languages — run on Arabic too.
3. **Voice layer (ours, additive, last):** house register + banned phrases (`Capabilities\Arabic_Copy_Tells.md`; Alwazour visual system copy rules; brand locks).

## The trap (from the study — hold it every run)
Do not trade one default for another. Pick **1–2 interventions per piece, vary them across pieces**, and compare against the last 3 pieces before shipping (the carousel tracker makes this checkable for IG).

## Mechanical gate (run it — 0 context cost, exit 1 on any hit)
```powershell
python "~\Desktop\Empire_Base\external-repos\humanizer-stack\scripts\copy_scan.py" --strict <caption-or-copy.txt>
python "~\Desktop\Empire_Base\external-repos\humanizer-stack\skills\structural-humanizer\scripts\structural_scan.py" --strict <file>
```
Scanners catch ~half (mechanical slice). Cadence, formulaic shape, and polished-but-empty filler need human eyes — the skills above are that pair of eyes. Verified 2026-10-01: both scanners are stdlib-only (zero supply-chain risk) and run clean on the real posted IEC-power caption.

## Rights boundary
MIT own-work + CC BY-SA 4.0 upstream portions (see clone's `ATTRIBUTION.md`). Internal + client-delivery use: fine. Factory resale/repackaging: forbidden — the `Digital_Product_Factory_Playbook.md` rights gate applies; our Arabic supplement is original work and unaffected.
