---
name: analysis-contract
description: The universal evidence and output contract for every analysis, research, study, teardown, audit, investigation, evaluation, and learn output — E1/E2/E3 evidence labels, [VERIFIED]/[CITED]/[ASSUMED] claim tags, the standard output shape (executive summary to sources), the 16-point quality rubric gate (score before vault promotion), the vault promotion rule, and volatility tags. Use whenever ANY analytical output is about to be written, scored, or promoted into the Second Brain vault.
metadata:
  version: 1.0.0
  written_by: opencode
  source_plan: Second_Brain\Workflow\30 - Resources\Capabilities\Analysis_Study_and_Agent_Capability_System_Plan_2026-10-01.md (Phase 2 — first install of the Quality OS)
  rubric_source: Second_Brain\Workflow\30 - Resources\Research\Upgrade_2026_09\23_Deep_Research_Methodology.md (§8, line 81 — 16-point rubric, 0-2 each, pass ≥10/16)
---

# Analysis Contract — the one quality layer for all analytical output

Applies to every lane (see `analysis-lane-router`). Any tool, any engine — the contract is engine-independent.

## 1. Evidence labels (every finding, every claim)

- **E1** — we did/verified it ourselves this session (measured, ran, read the real file)
- **E2** — reliable external source, cited with URL + capture date
- **E3** — plausible but unverified; `[ASSUMED]` until verified
- Fine-grained tags on load-bearing claims: `[VERIFIED: source]` / `[CITED]` / `[ASSUMED]`
- Never fabricate; remembered-but-unconfirmed = `[unverified]`; vendor claims = `vendor-claimed`

## 2. Output shape (recipe form — fill it, don't negotiate with it)

```text
# Title
> [tool] tag line + date
## Executive summary (5-7 bullets)
## Findings (each: labeled E1/E2/E3 + dated + cited)
## Conflicts / open questions (state limits honestly)
## What this means for the user (prioritized actions)
## Sources (URL — what it proved — capture date)
```

## 3. Quality gate — score before promotion

Score the output against the 16-point rubric (`Upgrade_2026_09\23_Deep_Research_Methodology.md` §8; 0-2 per point, pass ≥10/16). **<10/16 = draft, not vault-worthy** — redo or downgrade to draft status. Record the self-score in the output footer.

## 4. Promotion rule (vault hygiene)

Only rubric-passing, evidence-labeled outputs enter `30 - Resources/Research/` (or the matching PARA folder). Drafts go to `_Drafts/`. Tag volatility on every research note: `volatile` (re-verify before use, e.g. pricing/policies) / `semi-stable` (re-verify quarterly) / `stable` (methods, math, architecture).

## 5. After landing

State that `vault-search --reindex` is needed so the brain remembers its own research (the known forgetting gap — see plan Phase 3). Log the run (one line: lane, engine, cost/time, rubric score) so lane choice becomes empirical.
