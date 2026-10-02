---
name: secure-by-default
description: >-
  Build-time security guardrail — apply WHILE writing code, not after. When a task
  involves creating or editing an endpoint/route, a DB query, auth, a payment or
  webhook handler, file upload, an external/user-supplied URL fetch, an AI/agent
  tool call, CORS/headers, or anything touching secrets or user data, load this and
  hold every rule as you write the diff. Pairs with security-audit Phase 0 (the
  pre-ship gate) and the curriculum deep dive. Triggers: "build", "add endpoint",
  "API route", "auth", "login", "checkout", "webhook", "upload", "new feature",
  "new project", "scaffold", plus the secure-build hook fires it automatically.
triggers:
  - new project
  - build a
  - add an endpoint
  - api route
  - auth / login / signup
  - payment / checkout / webhook
  - file upload
  - fetch a url
  - cors / headers
  - handle user input
---

# secure-by-default

The full reasoning is in `Second_Brain/30-Resources/Curriculum/Product_Business_5_Pillars_Mastery.md`
→ "Deep Dive 1 — Security". This skill is the **live checklist you run per diff**.
When the build is "done", run `security-audit` Phase 0. For payments/PII/regulated data, escalate to `pentest-checklist` + `threat-modeling-expert`.

## How to use
Before writing or editing code, identify which surfaces the change touches, then hold the matching rules **while typing the diff** — don't defer to a later pass. After the diff, run the 10-second self-scan at the bottom.

## Rules by surface

### Any new endpoint / route / handler
- **Deny by default.** New routes are forbidden until explicitly opened. Auth check + authorization check, both, server-side, from the session — never a client-sent role.
- **Ownership in the query, not after.** `WHERE id = :id AND org_id = :session.org_id`. Not fetch-then-`if`.
- Return **404 not 403** for "not yours" (don't confirm the resource exists).
- Leave one test behind: "user A cannot touch user B's resource → 404".

### Database query
- Parameterized / ORM builder only. Never string-concatenate user input — including `ORDER BY` / identifiers (allow-list those).
- `SELECT` only needed columns; always a `LIMIT` on lists; keyset pagination not `OFFSET`.
- Money = integer minor units or `NUMERIC`. Timestamps = `timestamptz`.
- Multi-tenant: `tenant_id` in the query **and** RLS enabled + `FORCE`.

### Auth / session / tokens
- Passwords: `argon2id` or `bcrypt` (cost ≥ 12). Never a fast hash.
- JWT: short-lived access (5–15 min) + rotating refresh in an `HttpOnly; Secure; SameSite` cookie (not localStorage). Pin the alg server-side. Verify only issuer-set claims.
- Regenerate session ID on login; invalidate server-side on logout / password change.
- Rate-limit login / reset / OTP / signup with backoff + lockout.

### Secrets
- Nothing hardcoded, nothing in a committed `.env`, nothing in client bundles / source maps / CI logs.
- Read from the platform secret store / env at runtime. Separate per environment. Rotate on any leak.

### Input handling
- Validate at the boundary: type, length, format, allow-list. Reject, don't coerce silently.
- **XSS:** framework escaping on; no `dangerouslySetInnerHTML` / `v-html` / `innerHTML` on user data; DOMPurify for rich text; strict CSP.
- **NoSQL:** cast to string — reject `{$ne:...}` shaped inputs.
- **Command exec:** avoid; else `execFile` + args array + allow-list, no shell.
- **Deserialization:** JSON only. No `pickle` / native deserialization of untrusted data.

### File upload
- Type by magic bytes not extension; size cap; random filename; store in object storage / outside webroot; serve via a controlled endpoint. Never executable.

### External / user-supplied URL fetch (SSRF)
- Block private IP ranges, `169.254.169.254`, non-http schemes. Resolve DNS and check the **resolved** IP. Allow-list hosts if possible.
- Open redirect: redirect targets allow-listed, never raw user input.

### Payment / webhook handler
- **Verify the signature** (reject + log on failure). Reject stale/replayed timestamps.
- **Idempotency:** dedupe by event ID; duplicate = no-op.
- Grant access on the **verified webhook**, never the browser redirect.
- Price/amount server-side only. Entitlement checks server-side, never frontend-only.
- Re-fetch the live object from the processor API; don't trust event ordering or payload snapshots.

### CORS / headers
- CORS: explicit origin allow-list, never `*` with credentials.
- Set: CSP, HSTS, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` / `frame-ancestors 'none'`, `Referrer-Policy`.
- Cookies: `HttpOnly; Secure; SameSite`.

### AI / agent feature
- Model output and user prompts are untrusted. An AI tool-call gets the **same** permission checks as any backend action — no implicit bypass.
- Prompt injection can't cross a security boundary (exfiltrate data, escalate, act on another user's resource).
- AI endpoints rate-limited + cost-capped. AI output rendered to other users is sanitized.

### Dependencies
- Pin exact versions, commit the lockfile. Scan in CI (Renovate / Trivy / `npm audit`), fail on high severity. New dep → check maintainer/downloads/CVEs, or write the few lines yourself.

### Errors & logging
- **Fail closed:** on an unexpected exception, deny + generic 500, no stack trace to the client. Never fail open (timeout ≠ authenticated).
- Log auth events, authz denials, payment events, validation failures — **never** passwords, tokens, session IDs, card numbers, raw PII.

## 10-second self-scan (run after every code diff)
```
1. New route/query in this diff? → ownership check IN the query? deny-by-default?
2. Any user input? → validated at the boundary? escaped on output?
3. Any secret? → from env/secret store, not literal, not logged?
4. External call / URL / upload / redirect? → SSRF + allow-list guard?
5. Payment/webhook? → signature verified + idempotent + server-side price?
6. Error path? → fails closed, no stack trace, no secret in the log?
```
Any "no" → fix it in this diff before moving on. Don't accumulate a security backlog.
