# skill-creator

**Scaffold, validate, and package Claude Code skills.**

## What It Does

Three small Python utilities for the skill-authoring lifecycle:
initialize a new skill directory from a starter template, validate a
skill's `SKILL.md` frontmatter against the spec, and package a finished
skill folder into a distributable `.skill` file.

## When to Use

- Creating a new skill from scratch
- Checking whether a `SKILL.md`'s frontmatter is spec-valid
- Bundling a finished skill into a `.skill` file for distribution

## Usage

### Scaffold a new skill

```bash
python scripts/init_skill.py my-new-skill --path skills/public
```

Creates `<path>/<skill-name>/` with a starter `SKILL.md` (full of
`[TODO]` guidance) plus example `scripts/`, `references/`, and
`assets/` subfolders. Edit the `SKILL.md`, fill in the `description`
frontmatter, delete the guidance section once you've picked a
structure, and customize or delete the example resource files.

### Validate a skill

```bash
python scripts/quick_validate.py path/to/skill-folder
```

Checks that `SKILL.md` exists, has valid YAML frontmatter, uses only
allowed keys (`name`, `description`, `license`, `allowed-tools`,
`metadata`), and that `name`/`description` meet the spec's format and
length limits. Frontmatter-only — it does not check prose quality.

### Package a skill

```bash
python scripts/package_skill.py path/to/skill-folder [output-directory]
```

Validates the skill first (refuses to package on failure), then zips
the folder into `<skill-name>.skill` in the output directory (defaults
to the current directory).

## File Structure

A scaffolded skill looks like:

```
your-skill-name/
├── SKILL.md              # Main skill instructions
├── scripts/               # Executable code (Python/Bash/etc.)
├── references/             # Docs meant to be loaded into context
└── assets/                 # Files used in output, not loaded into context
```

## Writing Good Content

See `references/workflows.md` for sequential/conditional workflow
patterns, and `references/output-patterns.md` for template and
examples patterns — useful once the frontmatter is in place and you're
structuring the main body of `SKILL.md`.

## Support

Run `python scripts/quick_validate.py <path>` to see exactly what a
skill fails on before asking for help.
