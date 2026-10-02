---
name: bundle-a-backend-api
description: Backend and API development bundle for Node.js, Python, FastAPI, Django, Rust, and Go workflows.
user-invocable: false
---

# BUNDLE A: Backend & API Development

**Orchestrates:** Node.js, Python, FastAPI, Django, NestJS, Rust, Go, and 7 other language-pro skills.
**Audited 2026-08-17:** removed two fictional skill names (`golang-patterns`, `rust-patterns` never
existed — use `golang-pro`/`rust-pro`). `nestjs-patterns` and `django-tdd` are confirmed real but kept
**off-context** (narrow, occasional use) — pull via `python3 ~/.claude/overseer/search.py <name>`
when a NestJS or Django-testing task actually comes up, rather than paying their token cost every
session.

## Quick Start

**I want to:**
- Build a Node.js API → `nodejs-best-practices` + `api-design`
- Build a Python FastAPI → `fastapi-patterns` + `python-pro`
- Build a Django app → `django-patterns` + `django-tdd` (off-context, pull via overseer search)
- Optimize database queries → BUNDLE-C (database skills)
- Deploy to serverless → BUNDLE-E (cloud skills)

## What's Inside

### Primary Skills (use first)
- `nodejs-best-practices` — Node/Express production patterns
- `fastapi-patterns` — Python FastAPI async patterns
- `python-pro` — Python 3.12+ deep patterns
- `backend-patterns` — Generic backend architecture
- `api-design` — REST/GraphQL API design

### Secondary Skills (available)
- `django-patterns` — Django web framework
- `laravel-patterns` — PHP Laravel
- `nestjs-patterns` — Node.js NestJS framework (off-context, pull via overseer search)
- `golang-pro`, `rust-pro` — Go / Rust backend development (this bundle previously also listed
  fictional `golang-patterns`/`rust-patterns` skills that never existed — removed 2026-08-17)
- `typescript-pro`, `java-pro`, `csharp-pro`, `php-pro`, `ruby-pro`

### Specialized Sub-bundles
- `authentication` → `auth-implementation-patterns`
- `databases` → BUNDLE-C (delegates to database-optimizer, postgres-patterns)
- `testing` → BUNDLE-G (delegates to test-driven-development)
- `deployment` → BUNDLE-E (delegates to deployment-patterns)
- `security` → BUNDLE-H (delegates to security-audit)

## Usage Example

```
User: "Build a Node.js REST API with authentication"

1. Load BUNDLE-A (Backend)
2. Primary: nodejs-best-practices
3. Secondary: auth-implementation-patterns (from sub-bundle)
4. Tertiary: api-design (API patterns)
5. Result: Production Node API with OAuth/JWT
```

## Token Cost
- Lookup: <1ms (cached)
- Primary skill: ~5 tok
- Sub-skills: ~0 tok (already cached)

## Fallback
If user needs something else:
- Database → delegate to BUNDLE-C
- Testing → delegate to BUNDLE-G
- DevOps → delegate to BUNDLE-E
- Security → delegate to BUNDLE-H

---

**Next:** Use this bundle's primary skill. Ask follow-up questions if needed.
