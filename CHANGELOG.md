# Changelog

## v1.1.1 — 2026-10-02 (Claude-only)

- Claude Code only: removed every OpenCode reference (README, installer flags, ROUTING.md, PORTING.md). Verified the 360 skills contain no OpenCode-exclusive content.

## v1.1.0 — 2026-10-02 (adopter level-up)

- One-command install: `install.sh` (macOS/Linux/WSL) + `install.ps1` (Windows) — symlink or copy, full or per-pack, into `~/.claude/skills`.
- 9 curated packs (`packs/`): starter, frontend, backend, ai-agents, video, marketing, devops, security, qa. Every entry verified installable.
- `ROUTING.md`: paste-into-CLAUDE.md snippet that makes the agent fire skill-router automatically.
- README 60-second quickstart.

## v1.0.0 — 2026-10-02 (initial public release)

- 360 curated skills across 14 categories (personal/context skills excluded).
- Sanitized for new-device bootstrap: no machine paths (`~` / `$SECOND_BRAIN`), no live secrets (verified + push-protection clean).
- Scaffolding: README, PORTING.md, SKILLS-INDEX.md (360/360 with descriptions), MIT LICENSE, .gitignore, .gitattributes.
