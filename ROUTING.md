# Paste this into your CLAUDE.md (or AGENTS.md) so the agent routes every
# task through this library automatically instead of improvising.
#
# Requires: skills installed (see install.sh / install.ps1) + skill-router loaded.

## Skill routing (mandatory, silent, every substantive task)

0. Before ANY non-trivial task, apply `skill-router` logic: classify domain
   x action, score candidates (75% to load full instructions, 45% to apply
   patterns silently), pick the smallest useful stack (one primary + at most
   two supporting), ordered by phase (orient -> plan -> execute -> validate).
1. When no loaded skill fits, search the offline library BEFORE building
   anything from scratch:
   `python <repo>/skills/overseer/search.py <keywords>`
   (Notion: the index covers everything in SKILLS-INDEX.md at zero context cost.)
2. For analysis-shaped work, run `analysis-lane-router` first (pick the lane),
   then hold the output to `analysis-contract`.
3. Gate every user-facing word through `humanizer` before calling it done.

## Path conventions

- `$SECOND_BRAIN` = your knowledge-vault root (only some skills need it).
- `~` = whoever installed the repo. No machine-specific paths are assumed.
