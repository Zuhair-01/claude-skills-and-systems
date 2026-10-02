# PORTING.md — new-device setup

## 1. Clone and link

```bash
git clone https://github.com/<you>/claude-skills-and-systems.git
```

- **Claude Code:** copy or symlink `skills/*` into `~/.claude/skills/`
- **OpenCode:** symlink `skills/*` into `~/.config/opencode/skills/`
- Verify: `ls ~/.claude/skills | wc -l` should show ~360 entries.

## 2. Path conventions used in this repo

| Placeholder | Meaning | Set it to |
|---|---|---|
| `~` | Home dir of the installing user | automatic |
| `$SECOND_BRAIN` | Your knowledge-vault root (notes, playbooks, research packs) | your vault path, e.g. `~/Second_Brain` |
| `<you>` | Your GitHub username | — |

Skills that depend on a vault (`books-canon`, `BUNDLE-J-marketing`, `vault-search`) degrade gracefully without one — the skill text tells you which pack file it expects.

## 3. Per-skill requirements

- Most skills are **markdown-only**: zero install, work immediately.
- Skills needing runtimes say so at the top of their `SKILL.md`. Common ones:
  - `node` / `python3` for script-backed skills
  - `gh` CLI for GitHub skills
  - Playwright browsers for browser-automation skills
  - API keys (HeyGen, fal.ai, ElevenLabs…) — **never committed**; export as env vars per the skill's instructions.
- `gstack/*` ships as **source + markdown only**. The compiled helper binaries (`dist/*.exe`, `node_modules/`) are intentionally excluded from this repo — each gstack skill documents how to build or fetch them.

## 4. Updating

```bash
cd claude-skills-and-systems && git pull
```

If you symlinked (rather than copied), updates flow through immediately. If you copied, re-copy.
