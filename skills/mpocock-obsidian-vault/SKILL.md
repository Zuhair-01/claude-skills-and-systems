---
name: obsidian-vault
description: Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Vault location

`$SECOND_BRAIN\Workflow\`

Corrected from the original `/c/Users/the user/Desktop/Empire_Base/Second_Brain/Workflow/` (a stale WSL path from this
skill's upstream source — never valid on this Windows box). This is a **PARA-structured** vault,
not flat: `00 - Home`, `10 - Projects`, `20 - Areas`, `30 - Resources`, `40 - Archive`, plus
`Daily Notes` and `Templates`. The cross-account Handoff Log lives at
`20 - Areas\Handoff Log.md` — see `~/.claude/CLAUDE.md` for its protocol.

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- File under the correct PARA folder (Project = active with a deadline, Area = ongoing
  responsibility, Resource = reference material, Archive = inactive) — see CLAUDE.md Rule 5.
  Use index notes for cross-linking *within* a folder, not as a substitute for PARA placement.

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of `[[wikilinks]]`

## Workflows

### Search for notes

```bash
# Search by filename
find "/c/Users/the user/Desktop/Empire_Base/Second_Brain/Workflow/" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "/c/Users/the user/Desktop/Empire_Base/Second_Brain/Workflow/" --include="*.md"
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Use **Title Case** for filename
2. Write content as a unit of learning (per vault rules)
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks:

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/c/Users/the user/Desktop/Empire_Base/Second_Brain/Workflow/"
```

### Find index notes

```bash
find "/c/Users/the user/Desktop/Empire_Base/Second_Brain/Workflow/" -name "*Index*"
```
