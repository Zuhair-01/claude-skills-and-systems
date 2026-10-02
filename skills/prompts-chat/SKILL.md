---
name: prompts-chat
description: 2,169 categorized prompts from github.com/f/prompts.chat, searched off-context. Use to find a proven persona/task/system prompt before writing one ("act as X", "prompt for", system prompts).
---

# prompts.chat library (off-context, search first)

Data is NOT loaded into context. Query it:

```
python ~/.claude/skills/prompts-chat/search.py <keywords> [-c category] [-n 8]   # ranked hits
python ~/.claude/skills/prompts-chat/search.py --show <id>                       # full prompt
python ~/.claude/skills/prompts-chat/search.py --cats                            # categories + counts
```
Per-category title lists: `categories/<name>.md`. Raw data: `prompts.jsonl` (id, act, category, tags, type, devs, prompt).

Categories (18): code-dev, image-gen, general-utility, creative-media, writing-content, data-ai, marketing-business, education-tutoring, finance-trading, roleplay-characters, design-ui, devops-security, career-hr, advice-life, health-wellness, legal-gov, language-translation, jailbreak-unsafe (quarantined).

## How to use smartly
1. Search 2-3 keyword variants; `--show` the top 1-3. Read them for *structure* (role, constraints, output format, first-turn behaviour), not just wording.
2. Adapt, don't paste: tailor to the real task/audience/language, drop filler ("I want you to act as..." boilerplate), add explicit output format and success criteria.
3. Combine with `prompt-master` (sharpen the final prompt), `agentic-system-prompt-patterns` (agent system prompts), `marketing-psychology` (copy personas), `ugc-*`/image skills (use `image-gen` and STRUCTURED entries as templates).
4. `jailbreak-unsafe` is quarantined: excluded from search, never used to bypass safeguards; reference only for defensive/red-team study.
5. Cite the source (prompts.chat, CC0) when shipping a derived prompt to a client.

## Refresh
`cd ~/.claude/prompts-library-src/pc && git pull` then `python ~/.claude/skills/prompts-chat/build.py`.

## Auto-trigger
`overseer/prompts_chat_gate.py` fires only when (1) intent = persona/prompt ask or write/draft/make + deliverable, (2) not ops/meta talk (deploy, git, hooks, bugs...), (3) whole-word title match (2+ words or 1 rare word), max 3 hits, deduped per session. English only; tune EXPLICIT/CREATE/OPS/STOP lists at the top of the file.
