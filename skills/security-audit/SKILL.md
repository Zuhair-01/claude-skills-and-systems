---
name: security-audit
description: "Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening."
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Security Auditing Workflow Bundle

## Overview

Comprehensive security auditing workflow for web applications, APIs, and infrastructure. This bundle orchestrates skills for penetration testing, vulnerability assessment, security scanning, and remediation.

## When to Use This Workflow

Use this workflow when:
- Performing security audits on web applications
- Testing API security
- Conducting penetration tests
- Scanning for vulnerabilities
- Hardening application security
- Compliance security assessments

## The three security layers (this bundle covers the last two)

1. **Build-time — `secure-by-default` skill.** Applied WHILE code is written, per diff, so mistakes never land. Auto-fired by the `secure_build_gate.py` UserPromptSubmit hook on build/code prompts, and backed by the `secure-write-scan.js` PostToolUse hook that lints each Write/Edit for hardcoded secrets, string-built SQL, unsanitized HTML sinks, permissive CORS, unverified webhook handlers, and un-scoped id lookups (IDOR). Deep reasoning: curriculum "Deep Dive 1 — Security".
2. **Pre-ship — Phase 0 below.** Ship-blocking self-check before any build is called "done".
3. **Deep — Phases 1–7 below** + `pentest-checklist` / `threat-modeling-expert` for real payments / PII / regulated data.

## Workflow Phases

### Phase 0: Vibe-Code Pre-Ship Gate (MANDATORY for every app/web build)

Run this before calling any AI-generated or vibe-coded app/web project "done" —
ship-blocking, not optional. Faster and narrower than Phases 1-7: this is a
self-check against the common vulns AI-generated apps actually ship with, not
a full pentest engagement. Escalate to Phases 1-7 (or `pentest-checklist`,
`threat-modeling-expert`) for anything handling real payments/PII/regulated
data, or when this gate finds something serious enough to need deeper testing.

#### Secrets & Config Exposure
- [ ] No DB credentials, API keys, or tokens hardcoded in source
- [ ] `.env` / `.env.local` not committed, not publicly served, not in build output
- [ ] No secrets in client-side JS bundles or exposed source maps in production
- [ ] Build/CI logs don't print secrets
- [ ] No leaked secrets in git history (check with `git log -p` / a secrets scanner before making a repo public)
- [ ] No default/example credentials left unchanged (DB, admin panel, seed users)

#### Auth, Authz & Session
- [ ] Real authentication exists on every route that needs it (not "trust the frontend")
- [ ] Every API endpoint checks authorization server-side, not just auth
- [ ] IDOR: user-controlled IDs can't fetch/modify another user's data
- [ ] API endpoints don't trust a user-supplied role/permission field
- [ ] Password reset flow can't be used to take over an account (token expiry, single-use, no user enumeration)
- [ ] Sessions/JWTs: strong non-default secret, not leaked, not reused across envs, sane expiry
- [ ] Cookies set `HttpOnly`, `Secure`, `SameSite`
- [ ] Rate limiting on login, signup, password reset, and any paid/AI-cost endpoint
- [ ] Mass assignment: API can't bind extra client-supplied fields (e.g. `role`, `isAdmin`) onto a model

#### Data Access & Tenant Isolation
- [ ] Database has no open/public read-write permissions
- [ ] App's DB user has least-privilege access, not superuser/root
- [ ] Multi-tenant data is scoped by tenant/user at the query layer, not just in the UI
- [ ] Firebase/Supabase/S3 rules reviewed — not left on permissive defaults
- [ ] Sensitive fields (PII, tokens, payment data) encrypted at rest where applicable

#### Injection & Input Handling
- [ ] SQL/NoSQL injection: parameterized queries / ORM, no raw string concatenation
- [ ] Command injection: no unsanitized input passed to a shell
- [ ] XSS: user content escaped/sanitized before render, especially anything rendered as HTML
- [ ] CSRF protection on state-changing requests (or same-site cookies + verified origin)
- [ ] File uploads: type/size validated, stored outside webroot or behind signed URLs, not executable
- [ ] Path traversal: file paths built from user input are normalized/allowlisted
- [ ] SSRF: server-side requests can't be pointed at internal/metadata addresses by user input
- [ ] Open redirect: redirect targets are allowlisted, not raw user input

#### Network, Headers & Transport
- [ ] CORS is not `*` with credentials — explicit allowed origins only
- [ ] Security headers set: CSP, `X-Frame-Options`/frame-ancestors, `X-Content-Type-Options`, HSTS
- [ ] HTTPS enforced, no mixed content
- [ ] Webhook endpoints verify signatures (and reject stale/replayed timestamps)

#### Surface Area & Ops Hygiene
- [ ] Admin/internal routes and dashboards require auth and aren't linked from public pages
- [ ] Debug pages, `/api/debug`, GraphQL introspection, and verbose stack traces disabled in production
- [ ] Staging/test/preview environments aren't publicly indexable and don't share prod secrets
- [ ] Payment/subscription/entitlement checks are enforced server-side, not just gated in the frontend
- [ ] Dependencies scanned for known CVEs; no wildly outdated critical packages
- [ ] Logs don't contain tokens, passwords, full card numbers, or raw PII
- [ ] Basic audit log exists for sensitive actions (admin actions, payments, data deletion)
- [ ] Some monitoring/alerting exists for errors and auth failures (not silent-fail in prod)
- [ ] A backup/restore path exists for the primary datastore

#### AI-Feature Specific
- [ ] User input reaching a prompt can't be used to override system instructions in a way that breaks a security boundary (prompt injection)
- [ ] AI/agent tool-calls and data access are permission-checked the same as any other backend action — the model doesn't get an implicit bypass
- [ ] AI-generated output rendered to other users is sanitized before render (it's still user-influenced content)
- [ ] AI endpoints are rate-limited / cost-capped (an unauthenticated or abused endpoint can't run up unbounded inference spend)

#### Process
- [ ] Nothing shipped was AI-generated and merged without a human reading the diff — review every AI-authored change before it ships, especially anything touching auth, payments, or data access

#### Copy-Paste Prompt
```
Run the Phase 0 Vibe-Code Pre-Ship Gate from @security-audit against this app before we ship it.
```

### Phase 1: Reconnaissance

#### Skills to Invoke
- `scanning-tools` - Security scanning
- `shodan-reconnaissance` - Shodan searches
- `top-web-vulnerabilities` - OWASP Top 10

#### Actions
1. Identify target scope
2. Gather intelligence
3. Map attack surface
4. Identify technologies
5. Document findings

#### Copy-Paste Prompts
```
Use @scanning-tools to perform initial reconnaissance
```

```
Use @shodan-reconnaissance to find exposed services
```

### Phase 2: Vulnerability Scanning

#### Skills to Invoke
- `vulnerability-scanner` - Vulnerability analysis
- `security-scanning-security-sast` - Static analysis
- `security-scanning-security-dependencies` - Dependency scanning

#### Actions
1. Run automated scanners
2. Perform static analysis
3. Scan dependencies
4. Identify misconfigurations
5. Document vulnerabilities

#### Copy-Paste Prompts
```
Use @vulnerability-scanner to scan for OWASP Top 10 vulnerabilities
```

```
Use @security-scanning-security-dependencies to audit dependencies
```

### Phase 3: Web Application Testing

#### Skills to Invoke
- `top-web-vulnerabilities` - OWASP vulnerabilities
- `sql-injection-testing` - SQL injection
- `xss-html-injection` - XSS testing
- `broken-authentication` - Authentication testing
- `idor-testing` - IDOR testing
- `file-path-traversal` - Path traversal
- `burp-suite-testing` - Burp Suite testing

#### Actions
1. Test for injection flaws
2. Test authentication mechanisms
3. Test session management
4. Test access controls
5. Test input validation
6. Test security headers

#### Copy-Paste Prompts
```
Use @sql-injection-testing to test for SQL injection vulnerabilities
```

```
Use @xss-html-injection to test for cross-site scripting
```

```
Use @broken-authentication to test authentication security
```

### Phase 4: API Security Testing

#### Skills to Invoke
- `api-fuzzing-bug-bounty` - API fuzzing
- `api-security-best-practices` - API security

#### Actions
1. Enumerate API endpoints
2. Test authentication/authorization
3. Test rate limiting
4. Test input validation
5. Test error handling
6. Document API vulnerabilities

#### Copy-Paste Prompts
```
Use @api-fuzzing-bug-bounty to fuzz API endpoints
```

### Phase 5: Penetration Testing

#### Skills to Invoke
- `pentest-commands` - Penetration testing commands
- `pentest-checklist` - Pentest planning
- `ethical-hacking-methodology` - Ethical hacking
- `metasploit-framework` - Metasploit

#### Actions
1. Plan penetration test
2. Execute attack scenarios
3. Exploit vulnerabilities
4. Document proof of concept
5. Assess impact

#### Copy-Paste Prompts
```
Use @pentest-checklist to plan penetration test
```

```
Use @pentest-commands to execute penetration testing
```

### Phase 6: Security Hardening

#### Skills to Invoke
- `security-scanning-security-hardening` - Security hardening
- `auth-implementation-patterns` - Authentication
- `api-security-best-practices` - API security

#### Actions
1. Implement security controls
2. Configure security headers
3. Set up authentication
4. Implement authorization
5. Configure logging
6. Apply patches

#### Copy-Paste Prompts
```
Use @security-scanning-security-hardening to harden application security
```

### Phase 7: Reporting

#### Actions
1. Document findings
2. Assess risk levels
3. Provide remediation steps
4. Create executive summary
5. Generate technical report

## Security Testing Checklist

### OWASP Top 10
- [ ] Injection (SQL, NoSQL, OS, LDAP)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring

### API Security
- [ ] Authentication mechanisms
- [ ] Authorization checks
- [ ] Rate limiting
- [ ] Input validation
- [ ] Error handling
- [ ] Security headers

## Quality Gates

- [ ] All planned tests executed
- [ ] Vulnerabilities documented
- [ ] Proof of concepts captured
- [ ] Risk assessments completed
- [ ] Remediation steps provided
- [ ] Report generated

## Related Workflow Bundles

- `development` - Secure development practices
- `wordpress` - WordPress security
- `cloud-devops` - Cloud security
- `testing-qa` - Security testing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
