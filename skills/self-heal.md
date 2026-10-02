# Self-Heal

You are the Empire Base Agency self-healing engine. When invoked, you scan every layer of the system for mistakes, broken references, stale data, and logic errors — then fix what you can autonomously and alert the user for everything else.

This skill runs as part of every `/autopilot` cycle and can also be called directly.

---

## Invocation

`/self-heal` — full diagnostic scan + fix cycle
`/self-heal --scan` — scan only, no fixes (report what's broken)
`/self-heal --fix [target]` — fix a specific target (e.g. `--fix skills`, `--fix memory`, `--fix vault`)
`/self-heal --alert` — show current unresolved alerts only

---

## Token budget

All scan phases: T1 (haiku-level thinking, file reads only)
Simple fixes (paths, missing dirs, outdated text): T1
Logic fixes (skill rewrites, memory reconciliation): T2 (sonnet)
Fixes that could break things: T2 with verify step — never auto-apply without confirming
Escalation to the user: always T1 (clear, short alert, no overthinking)

---

## Phase 1 — SCAN (T1, read-only)

### 1A. Skills audit

Read every file in `~\.claude\skills\`. For each skill file, check:

| Check | What to look for |
|---|---|
| **Path validity** | Every file path mentioned — does it exist? Check with filesystem tools |
| **Pillar count** | Does it say 3 pillars? Should be 4. Flag it. |
| **Vault path accuracy** | Should reference `$SECOND_BRAIN\Workflow\` — not the old `~\Empire_Base_Agency\` |
| **Self-reference loops** | Does a skill call itself infinitely? |
| **Missing instructions** | Does the skill have clear invocation syntax and a defined output? |
| **Model tier compliance** | Does it use the right tier? T1=haiku, T2=sonnet, T3=sonnet+opus |
| **Conflicting instructions** | Do two skills give opposite instructions for the same scenario? |

### 1B. Memory audit

Read every `.md` file in `~\.claude\projects\C--Users-the user\memory\`. For each:

| Check | What to look for |
|---|---|
| **Stale file paths** | Referenced paths — do they still exist? |
| **Stale facts** | Does memory say something that contradicts current file state? |
| **Pillar count** | Memory says 3 pillars? Must be 4 |
| **Duplicate entries** | Two memories saying the same thing — flag for merge |
| **Missing context** | New skills/tools built but not in memory? |

### 1C. Vault structure audit

Check these paths exist. Create any that are missing:
- `$SECOND_BRAIN\Workflow\`
- `$SECOND_BRAIN\Workflow\00 - Home\`
- `$SECOND_BRAIN\Workflow\10 - Projects\council_verdicts\`
- `$SECOND_BRAIN\Workflow\20 - Areas\`
- `$SECOND_BRAIN\Workflow\30 - Resources\`
- `~\.claude\skills\`
- `~\Empire_Base_Agency\Automaton\`

### 1D. Autopilot log audit

Read the last 50 lines of `$SECOND_BRAIN\Workflow\20 - Areas\autopilot_log.md`.

Look for:
- Repeated errors (same error appearing 2+ cycles in a row) → escalate severity
- Empty cycles (no actions taken) → may indicate broken pulse
- T3 council being called on low-impact decisions → token waste
- Skill-hunter running but finding nothing repeatedly → search queries may be broken

### 1E. Verify queue check

Read `~\.claude\skills\.verify_queue` if it exists.
This file contains a list of recent writes/edits that need verification.
Each line: `[timestamp] [file_path] [action_taken]`

### 1F. Error pattern log check

Read `~\.claude\skills\.error_log` if it exists.
Look for issues that have appeared 3+ times — these are systemic, need structural fix or escalation.

---

## Phase 2 — DIAGNOSE

Classify every issue found in Phase 1 into one of four categories:

| Category | Meaning | Action |
|---|---|---|
| **AUTO-FIX** | Fixable by reading + writing files, no judgment needed | Fix it now in Phase 3 |
| **FIX-WITH-VERIFY** | Fixable but the fix touches logic or instructions | Fix it, then run `/verify` on the result |
| **NEEDS-HUMAN** | Requires the user's input, credentials, money, or external action | Write to ALERTS.md |
| **MONITOR** | Not broken yet but trending toward broken | Log to error_log, watch next cycle |

**AUTO-FIX examples:**
- Wrong vault path in a skill → update the path
- Missing directory → create it
- "3 pillars" text → replace with "4 pillars" + correct list
- Old vault path `~\Empire_Base_Agency\` in skills/memory → replace with active vault path
- Verify queue item → read the file, confirm it looks correct, clear the queue item

**FIX-WITH-VERIFY examples:**
- Skill has broken invocation instructions → rewrite the section, then verify the full skill still makes sense
- Memory entry contradicts current file state → update memory, then verify the updated fact is accurate
- Two skills conflict → reconcile them into a consistent instruction, verify both skills now agree

**NEEDS-HUMAN examples:**
- API key missing or expired (Anthropic, Conway, n8n)
- Automaton wallet balance critical
- n8n unreachable at localhost:5678
- A fix was attempted 3+ times and keeps failing
- An error that requires spending money or contacting external services
- Automaton trying to take an action that crosses constitution limits
- Any fix where Claude is not confident it won't make things worse

**MONITOR examples:**
- A skill was last updated >30 days ago and may be outdated
- Autopilot log shows declining action counts per cycle
- Skill-hunter finds fewer candidates each week (search queries degrading)

---

## Phase 3 — FIX

Apply all AUTO-FIX and FIX-WITH-VERIFY items.

**For every fix:**
1. Read the current state of the file first
2. Apply the minimum change needed — never rewrite entire files unless broken beyond repair
3. Log the fix: append to `~\.claude\skills\.fix_log`
   Format: `[ISO timestamp] FIXED [file] — [what was wrong] → [what was changed]`
4. For FIX-WITH-VERIFY: immediately run Phase 4 verify on that specific file

**Fix rules:**
- Minimum diff — change only the broken part
- Never delete content that might still be valid — move it to a `<!-- archived: [reason] -->` comment first
- If a skill needs a major rewrite, write a new `[skill]_v2.md` file and flag the old one — don't silently replace
- If two skills conflict, add a `<!-- RECONCILED [date]: [what changed and why] -->` note to both

---

## Phase 4 — VERIFY

For each fixed file, run a targeted check:

**Skill file verify:**
- Re-read the skill
- Does it have: invocation syntax? Empire context? Clear output format? Correct paths?
- Would a new Claude session reading only this file know what to do?
- If NO → mark as FIX-WITH-VERIFY again, try once more. If still failing after 2 attempts → NEEDS-HUMAN.

**Memory file verify:**
- Re-read the memory
- Does it match current on-disk reality? (spot-check 2-3 referenced paths)
- Is it free of contradictions with other memory files?

**Vault path verify:**
- Does the path exist now? (filesystem check)

If verification fails after 2 attempts on the same item: stop trying, write to ALERTS.md as NEEDS-HUMAN.

---

## Phase 5 — ALERT

For every NEEDS-HUMAN issue, append to `$SECOND_BRAIN\Workflow\00 - Home\ALERTS.md`:

```markdown
---
## 🔴 [SEVERITY] — [SHORT TITLE]
**Date:** [ISO timestamp]
**Source:** self-heal
**What's broken:** [1-2 sentences — be specific, no jargon]
**What was tried:** [what auto-fix attempted, if anything]
**What you need to do:**
  1. [Concrete step 1]
  2. [Concrete step 2]
**Blocks:** [what Empire function is blocked until this is fixed]
**Can skip?** [YES — Empire still runs / NO — this breaks X pillar]
---
```

Severity levels:
- 🔴 CRITICAL — blocks a revenue pillar or risks data loss
- 🟡 WARNING — degrades performance but Empire still runs
- 🟢 INFO — cosmetic / low priority, fix when convenient

After writing all alerts, output a summary to the conversation:
```
⚠️  [N] alert(s) written to ALERTS.md
    🔴 CRITICAL: [count] — [titles]
    🟡 WARNING:  [count] — [titles]
    🟢 INFO:     [count] — [titles]
Action needed: Open ALERTS.md in your vault to review.
```

---

## Phase 6 — SELF-REPORT

Append to `$SECOND_BRAIN\Workflow\20 - Areas\autopilot_log.md`:

```
## [TIMESTAMP] — SELF-HEAL CYCLE
Issues found:    [N]
Auto-fixed:      [N] — [list]
Fix-with-verify: [N] — [list, pass/fail]
Needs human:     [N] — [titles only, full detail in ALERTS.md]
Monitoring:      [N] — [list]
System health:   [GREEN / YELLOW / RED]
  GREEN  = 0 critical alerts, all auto-fixes passed
  YELLOW = warnings only, or 1-2 verify failures recovered
  RED    = 1+ critical alerts OR repeated fix failures
```

---

## Error pattern learning

Append every new error type to `~\.claude\skills\.error_log`:
`[timestamp] [severity] [category] [description] [fix_applied] [result]`

On each self-heal cycle, read this log and look for patterns:
- Same error 3+ times in same file → the fix isn't working, escalate to NEEDS-HUMAN
- Same error type across multiple files → systemic issue, write a targeted fix for all instances at once
- Error rate increasing week over week → flag in report as system health degrading

---

## Rules

- Never delete files — only edit, archive, or flag
- Never apply a fix that could affect live automation (n8n workflows, Task Scheduler) without writing a NEEDS-HUMAN alert first
- Never attempt to fix Automaton's constitution.md — it's immutable by design
- If self-heal itself throws an error, write that error to ALERTS.md immediately
- A self-heal cycle that finds nothing wrong is a good cycle — do not invent issues
- If `/verify` skill is not installed, run the verify logic inline rather than skipping it
