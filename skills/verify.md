# Verify

Lightweight post-action checker. Runs after any significant write, edit, or skill installation to confirm the output is correct, complete, and consistent with Empire Base Agency context.

Designed to be fast (T1, haiku-level thinking). Never blocks — it only flags.

---

## When this runs

- Automatically: after any Write or Edit tool call that touches a skill, memory file, or vault document
- Called by `/self-heal` during FIX-WITH-VERIFY phase
- Called by `/autopilot` after each Phase 3 execution action
- Manually: `/verify [file_path]` to check a specific file

---

## Token budget

Always T1 (haiku-level). This must be fast and cheap. If a verify check requires deep reasoning, hand off to `/self-heal` instead.

Max tokens per verify run: ~300

---

## What to check (run all that apply to the file type)

### Skill file (`~/.claude/skills/*.md`)

| Check | Pass condition |
|---|---|
| Has invocation syntax | File shows how to call the skill (e.g. `/skill-name [args]`) |
| Has Empire context | Mentions all 4 pillars by name |
| Has correct vault path | References active vault `~\Desktop\Empire_Base\...` not old `~\Empire_Base_Agency\` |
| Has output format | Specifies what the skill outputs / writes |
| No broken path references | Any path mentioned passes a quick existence check |
| Model tier stated | Uses correct tier labels (T1/T2/T3) or haiku/sonnet/opus |
| No infinite self-reference | Skill doesn't call itself without a termination condition |

### Memory file (`memory/*.md`)

| Check | Pass condition |
|---|---|
| Has frontmatter | `name`, `description`, `type` fields present |
| Pillar count correct | Says "4 pillars" not "3 pillars" |
| Paths exist | Spot-check 1-2 file paths mentioned |
| No contradictions | Doesn't directly contradict another memory file |
| Not stale | Doesn't reference something clearly outdated (check a key claim) |

### Vault document (Second Brain write)

| Check | Pass condition |
|---|---|
| File was actually written | Path exists on disk |
| Not empty | File has content beyond headers |
| Correct format | Matches expected format (log entry, eval card, verdict, etc.) |
| No garbled content | No truncated JSON, broken markdown, or placeholder text left in |

### n8n workflow JSON

| Check | Pass condition |
|---|---|
| Valid JSON | Parses without error |
| Has schedule triggers | At least one scheduleTrigger node present |
| Has API call | At least one httpRequest node present |
| Connections complete | Every node has at least one connection |

### Automaton config

| Check | Pass condition |
|---|---|
| Valid JSON | Parses without error |
| genesisPrompt present | Non-empty string |
| soulConfig present | Has `requireCreatorApprovalForPurposeChange: true` |
| treasuryPolicy present | Has daily spend limits |

---

## Output format

**If all checks pass:**
```
✓ VERIFY PASS — [file_path]
  Checks: [N]/[N] passed | Time: ~T1 | Tokens: minimal
```

**If any check fails:**
```
✗ VERIFY FAIL — [file_path]
  Failed checks:
    - [check name]: [what was expected] vs [what was found]
    - [...]
  Severity: [AUTO-FIX / FIX-WITH-VERIFY / NEEDS-HUMAN]
  Recommended action: [1 sentence]
```

**Then:**
- AUTO-FIX failures: queue to `.verify_queue` for self-heal to pick up
- NEEDS-HUMAN failures: write to ALERTS.md immediately

---

## Verify queue

Append failures to `~\.claude\skills\.verify_queue`:
```
[ISO timestamp]|[file_path]|[failed_checks]|[severity]
```

Self-heal reads this queue on every cycle and processes it.

---

## Rules

- Never modify files during verify — only read and report
- A passing verify is silent in the conversation (don't spam green checkmarks)
- Only output to conversation if something FAILS or if called manually
- If the file doesn't exist at all, that's a CRITICAL failure — alert immediately
- Verify must complete in under 5 tool calls — if it needs more, something is wrong with the file, hand off to self-heal
