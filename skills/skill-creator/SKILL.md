---
name: skill-creator
description: "Scaffold, validate, and package a new Claude Code skill. Use when the user wants to create a new skill, check an existing SKILL.md for spec compliance, or bundle a skill folder into a distributable .skill file."
category: meta
risk: safe
source: community
tags: "[automation, scaffolding, skill-creation, meta-skill]"
date_added: "2026-02-27"
---

# skill-creator

## Purpose

Scaffold a new skill directory with a starter `SKILL.md` and example
resource folders, validate a skill's frontmatter against the spec, and
package a finished skill into a distributable `.skill` file (a zip
archive). This skill wraps three small Python utilities in `scripts/` —
it does not require any external repository, template files, or
platform-detection step.

## When to Use This Skill

- User wants to create a new skill from scratch
- User wants to check whether a `SKILL.md`'s frontmatter is spec-valid
- User wants to bundle a finished skill folder into a `.skill` file for distribution

## Core Capabilities

1. **Initialize** — `scripts/init_skill.py` creates a new skill directory with a
   starter `SKILL.md` (full of `[TODO]` guidance on how to structure the skill)
   plus example `scripts/`, `references/`, and `assets/` subfolders.
2. **Validate** — `scripts/quick_validate.py` checks a skill's `SKILL.md`
   frontmatter: required fields, allowed keys, naming convention, and length limits.
3. **Package** — `scripts/package_skill.py` validates a skill, then zips its
   folder into a `<skill-name>.skill` file for distribution.

## Workflow

### 1. Scaffold a new skill

```bash
python scripts/init_skill.py <skill-name> --path <path>

# Examples
python scripts/init_skill.py my-new-skill --path skills/public
python scripts/init_skill.py custom-skill --path /custom/location
```

Skill name requirements: hyphen-case, lowercase letters/digits/hyphens only, max 40 characters, must match the directory name exactly.

This creates:
```
<path>/<skill-name>/
├── SKILL.md              # Starter file — full of [TODO] sections to fill in
├── scripts/example.py    # Placeholder executable script
├── references/api_reference.md  # Placeholder reference doc
└── assets/example_asset.txt     # Placeholder asset file
```

Next steps after scaffolding:
1. Edit `SKILL.md`: fill in the `description` frontmatter field and every `[TODO]` block. The generated file's own "Structuring This Skill" section lists four content patterns (workflow-based, task-based, reference/guidelines, capabilities-based) with examples — pick one, then delete that guidance section.
2. Customize or delete the example files in `scripts/`, `references/`, and `assets/` — not every skill needs all three. Use `scripts/` for executable code, `references/` for material meant to be loaded into context, `assets/` for files used in the output but not loaded into context (templates, boilerplate, fonts, images).
3. Validate before considering it done (see below).

### 2. Validate a skill

```bash
python scripts/quick_validate.py <skill_directory>
```

Checks:
- `SKILL.md` exists and has YAML frontmatter
- Only allowed frontmatter keys are present: `name`, `description`, `license`, `allowed-tools`, `metadata`
- `name` and `description` are both present
- `name` is hyphen-case, no leading/trailing/double hyphens, ≤ 64 characters
- `description` has no angle brackets, ≤ 1024 characters

This is a frontmatter-only check — it does not lint prose content, word count, or writing style. Prints `"Skill is valid!"` and exits 0 on success; otherwise prints the specific failure and exits 1.

### 3. Package a skill for distribution

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Runs `quick_validate.py` first and refuses to package on validation failure. On success, zips the entire skill folder (all files, preserving the folder name as the zip root) into `<skill-name>.skill` in the output directory (defaults to the current directory).

## Writing Good SKILL.md Content

Two reference docs cover content-quality patterns beyond frontmatter validity — read them when structuring the main body:

- `references/workflows.md` — sequential vs. conditional workflow patterns for multi-step skills
- `references/output-patterns.md` — template and examples patterns for skills whose output quality depends on consistent formatting

## Limitations
- This skill only validates frontmatter shape, not prose quality, word count, or whether the skill actually works — read the generated content critically before shipping.
- Packaging produces a zip archive; it does not publish, register, or install the skill anywhere.
- Use this skill only when the task clearly matches the scope described above.
- Stop and ask for clarification if required inputs, permissions, or success criteria are missing.
