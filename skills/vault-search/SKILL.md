---
name: vault-search
description: Semantic (meaning-based, not keyword) search over the user's entire Second_Brain vault, backed by turbovec + local Ollama embeddings. Use whenever the user asks about past decisions, project history, "what did we decide about X", "find where I wrote about Y", context that isn't in the current conversation, or before claiming "there's no record of that" / re-deriving something that may already be documented. Also use proactively at the start of ambiguous or context-dependent tasks to check if relevant prior context exists.
---

# Vault Search (turbovec)

A standalone semantic search index over `Second_Brain` (54+ markdown docs,
chunked). Finds documents by *meaning*, not exact words — catches things
grep/keyword search misses.

## When to use
- User references past work, decisions, or context not in this conversation.
- Before saying "I don't see that anywhere" — check here first, it's cheap.
- Any "what's the status of X" / "did we already solve Y" question.

## How to run
```
python "~\Desktop\Empire_Base\growth-os\vaultmind\turbovec_search.py" --reindex "<query text>"
```
`--reindex` is cheap and safe to always include — it only re-embeds files
that changed since the last run (mtime-cached), so on an unchanged vault it
adds ~0 cost. Never skip it to "save time."

## Ollama dependency — self-healing, no action needed
The script calls `http://localhost:11434` for embeddings (`nomic-embed-text`,
already pulled). It auto-detects if Ollama isn't running and starts it
itself before doing any work (waits up to 15s). Nothing to do here — just
run the command above.

## Mandatory: announce usage to the user
Every time this is invoked, say so **before** running it and summarize the
result after, e.g.:
> Searching vault memory (turbovec) for: "ostazi constraint"
> → top hits: `SESSION_SUMMARY_2026_08_16_17.md`, `Ostazi/TASKLIST.md`

Never run this silently — the user wants visibility into when/why it's used.

## Output format
Prints ranked `score  path (chunk N)` lines, deduped to one hit per file.
Higher score = more relevant. Open the top 1-3 paths with Read if the
content itself (not just the filename) is needed to answer the question.

## Scope / limits
- Covers `Second_Brain` only (not clip-platform code, not Alwazour product
  DB — this is notes/docs search, not a general project search).
- Not a substitute for `git log`/`grep` for code — use this for prose,
  decisions, plans, logs; use normal code tools for source files.

## Safe to call from multiple concurrent sessions
This is deliberately safe to invoke from more than one Claude Code /
OpenCode session at once (Rule 10 parallel-session workflow, or two
sessions both auto-triggering this skill independently) — stress-tested
2026-08-24 with 3 simultaneous `--reindex` calls, no corruption, no crash.
Cache state (sources+mtimes+vectors) lives in one atomically-replaced
file (`index_meta.npz`) specifically so concurrent writers can't leave it
inconsistent. Don't hesitate to call it just because a peer might be
using it too.
