---
name: replit-style-saas-build
description: A-to-Z venture pipeline for turning an app idea into a launched, attractive, legally clean SaaS, not just a build. Stages - validate the idea, position and name it, brand and color science, copy and offer, pricing, build (Replit-style stack distilled from FreshExpiry), protection (Clerk, Cloudflare WAF/rate limits/Turnstile, app and data hardening), IP and legal hygiene, landing and launch, growth, ops. Use for any new SaaS/B2B/web app idea, "make an app for X", or when migrating a Replit-built app. Picks only the stages the idea needs and routes each to the existing skill that owns it.
---

# Idea to launch, A to Z

Reference build: `Empire_Base/FreshExpiry` (private GitHub Zuhair-01/FreshExpiry) and `Second_Brain/Workflow/30 - Resources/Replit_Agent_Build_Playbook_FreshExpiry.md`. The build is Stage 6 of 10. Most failed apps were well built and badly chosen, so do not start at Stage 6.

**Leaving Replit / self-hosting a generated app:** load `platform-exit-and-self-host` (audit what the platform did, Render + Neon + Clerk recipe, direct-APK release). Reference exit doc: `FreshExpiry/docs/REPLIT_EXIT.md`.

## How to run it
1. Read the idea. Decide which stages it needs (a personal tool skips 3 to 5 and 8 to 9; a paid product needs all ten). Say the list in one line, do not narrate.
2. Each stage has a gate. Do not pass a failed gate, fix it or stop and tell the user why.
3. Stage output goes into one folder in the vault, `10 - Projects/<app>/`: `01_validation.md`, `02_positioning.md`, `03_brand.md`, `04_copy.md`, `05_pricing.md`, plus the repo. One canonical latest file per stage, delete superseded copies.
4. Load only the skills a stage names, drop them after it.

## Stage 1 - Validate (gate: a named starving crowd)
Skills: `market-research`, `competitors`, `billion-playbook`, `council` for a go/no-go. Also the vault's universal business validation framework (5-step, Arabic checklist).
Halbert order: market beats offer beats copy. Name the crowd, where it gathers, what it already pays for. Read real complaints of competitor users, quote them. Kill or reshape the idea here, not after the build. Zero fabricated stats.

## Stage 2 - Position and name (gate: one sentence a stranger repeats back)
Skills: `marketing-psychology` (read the Halbert, Legends, Schwartz docs it names, do not just cite them), `trust-calibrator`.
Output: who it is for, the painful job, the one USP, awareness level and market sophistication (Schwartz), the proof you can honestly show. Pick a name that is short, spellable, pronounceable in Arabic and English if the market is MENA, with a free .com/.app and free handles.

## Stage 3 - Brand and color science (gate: passes contrast and colorblind checks)
Skills: `color-expert` (OKLCH/OKLAB, palette generation, contrast, color naming), `brandkit`, `design-system`, `taste-skill`, `frontend-reference-sources` (Rule 7 frontend sub-rule: source real references first), `fixing-accessibility`.
Rules:
- Build palettes in OKLCH, not hex-by-eye. Keep lightness steps even so a scale looks even. Neutral ramp with a slight brand-hue tint, one brand color, semantic colors.
- 60/30/10: neutrals 60, surfaces or secondary 30, brand accent 10. The accent is for the one action per screen.
- Contrast: body text 4.5:1 minimum, large text and UI borders 3:1 (WCAG AA). Check every text-on-tint pair, not only black on white. Never rely on color alone, pair severity color with an icon or label. Test protanopia/deuteranopia simulation, roughly 1 in 12 men.
- Semantic set is fixed: success, warning, critical, info, each with a strong text shade and a pale surface shade (FreshExpiry pattern: green #176B45 on #E5F2EA, amber #A66300 on #FFF1D5, red #B64035 on #FBE9E6).
- Color psychology is a hypothesis, not a law. Use it for fit with the domain (green for fresh or safe, blue for finance trust) and check culture (red, white, green carry different meanings in MENA vs West). Do not justify a palette with "blue builds trust".
- Dark mode is a separate palette designed on purpose, not inverted. Print, low-vision and sun-glare screens (retail, warehouses) need the highest contrast.
- Define tokens once (CSS variables), no raw hex in components.
Fonts: pick a pair, verify the license, and for Arabic use the Arabic Font Pack and test in the real renderer.

## Stage 4 - Copy and offer (gate: Legends QA checklist passes)
Skills: `copywriting`, `marketing-psychology`, `clean-user-facing-text`, `brand-voice`.
Halbert: the lead carries the page. One CTA per page. P.S. is a second headline. Caples: a claim too good to be true is disbelieved, so prefer the believable specific number. Hopkins: instrument it or do not argue about it. Write from customer language collected in Stage 1. Zero fake scarcity, zero invented testimonials, no fabricated stats. Anti-AI-writing pass on all public prose (no em dash habit, no filler triplets). No vendor names in client-facing copy, describe the mechanism.

## Stage 5 - Pricing and offer structure (gate: a reason for every tier)
Skills: `pricing`, `pricing-strategy`, `payment-integration`, `stripe-integration`, `shamcash-payments` for Syria.
Price to the value the crowd already pays for, three tiers max, an honest free or trial path (Hopkins: trials lower risk more than arguments). Never charge before a real provider and webhook reconciliation exist (FreshExpiry's billing is dev-mode state only).

## Stage 6 - Build (gate: signed-in flow seen working in a real browser)
Skills: `secure-by-default` (while writing), `saas-multi-tenant`, `api-design`, `database-design`, `frontend-design`, `react-best-practices`.
Default stack: pnpm workspaces monorepo (`artifacts/<web>`, `artifacts/api-server`, `lib/db`, `lib/api-spec`, `lib/api-client-react`, `lib/api-zod`), React + Vite + shadcn + Tailwind + wouter + React Query, Express + pino, Postgres (Neon) + Drizzle, Clerk (cookies + proxy middleware before body parsers).
Non-negotiable patterns:
1. OpenAPI-first. `openapi.yaml` is the contract, Orval generates the React Query client and Zod schemas, server validates responses with the generated Zod. Never hand-edit generated files. `info.title` stays exactly `Api`.
2. Tenant boundary is `organization_id` on every business table, filtered server-side from the authenticated org. Never trust ids from the browser.
3. First-login provisioning in ONE transaction: app_user + organization + owner membership + trial. Demo data only behind an env flag.
4. Auditable mutations: movement or audit row for every state change.
5. Domain rules as pure functions in one timezone-explicit file. Money in integer cents, dates as `YYYY-MM-DD` strings.
6. Write `<APP>_HANDOFF.md` while building (architecture, env vars, commands, verification checklist, hardening backlog).
Verify in order: typecheck libs, api, web, build api, build web, `/api/healthz`, signed-out `/api/me` = 401, landing, then the signed-in flow (create, receive, use, waste, cross-tenant denied). Never claim done before the signed-in flow is seen working.

### Local-dev gotchas (all hit for real on this machine)
- Git Bash mangles `BASE_PATH=/` to `/Program Files/Git/`. `export MSYS_NO_PATHCONV=1`.
- pnpm `runDepsStatusCheck` trips the `preinstall` guard on Windows. Harmless, call `node_modules/.bin/<tool>` directly.
- Replit repos pin linux-x64 in `pnpm-workspace.yaml` `overrides`. Remove the `win32-x64` exclusions for native Windows and add `@clerk/shared` to `onlyBuiltDependencies`.
- Vite has no `/api` proxy outside Replit. Add `server.proxy` gated on `API_PROXY_TARGET`. Symptom: `/api/me` returns index.html and the UI crashes on `.name` of undefined.
- This machine's VPN blocks raw Postgres (5432). Use `@neondatabase/serverless` + `ws` with `drizzle-orm/neon-serverless` (WebSocket over 443), Pool not neon-http so `db.transaction()` works. `drizzle-kit push` still needs TCP, so `drizzle-kit generate` offline and apply the SQL through the WebSocket Pool split on `--> statement-breakpoint`. Pass `--schema=./src/schema/index.ts` explicitly on Windows.
- Replit `.gitignore` lacks `.env`. Add `.env`, `.env.*`, `!.env.example` before any secret is written.

## Stage 6b - Protect it (gate: security-audit Phase 0 clean, every item below either done or written down as accepted risk)
Skills: `clerk-auth`, `secure-by-default`, `security-audit`, `pentest-checklist`, `threat-modeling-expert`, `secrets-management`, `cloudflare-workers-expert` (edge work), `api-security-testing`. Local tools already installed: Gitleaks (secrets), Trivy (deps and images), Renovate (updates).
Defense in layers, cheapest first:
- **Clerk (identity).** Production instance before real users (dev keys are for dev only). Turn on bot protection and sign-up attack protection, email verification, and MFA for owner roles. Lock allowed redirect URLs and origins. Sessions via cookies, never put the secret key in Vite. Server checks membership and role on every request, never trusts client role or org id. Rotate keys if leaked, the dev secret pasted in chat or logs counts as leaked.
- **Cloudflare (edge).** Put the domain behind Cloudflare: proxied DNS hides the origin IP, SSL mode Full (strict), Always Use HTTPS, HSTS. Turn on the free managed WAF ruleset and Bot Fight Mode, add rate-limiting rules on `/api/*` and stricter ones on login and sign-up, Turnstile on public forms (contact, waitlist, sign-up) instead of CAPTCHAs, DDoS protection is on by default. Cloudflare Access for admin or staging URLs. Firewall the origin to Cloudflare only so the WAF cannot be bypassed. Cache static assets, never cache authenticated `/api` responses. Some hosts (Vercel, Replit) sit behind their own edge, check the combination before proxying.
- **App layer.** Rate limit and structured validation errors, response validation with generated Zod, role checks on every write, CORS to an explicit origin list (not `origin: true` with credentials), security headers (CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy) via helmet, request size limits, no stack traces to clients, audit log on sensitive actions. Note FreshExpiry currently ships `cors({credentials: true, origin: true})`, tighten it before production.
- **Data.** Org-scoped queries with a test that proves cross-tenant access is denied, least-privilege DB role, Neon branching and point-in-time restore as backup, migrations reviewed, PII minimised, export and delete paths.
- **Supply chain and secrets.** Gitleaks pre-commit, Trivy on dependencies, lockfile committed, only approved build scripts, `.env` never committed, secrets in the host's secret manager, separate dev and prod keys.
- **Monitor.** Error tracking, uptime check on `/api/healthz`, alerts on auth failures and 5xx spikes, Cloudflare security events reviewed weekly.
- **Abuse and payments.** Webhook signature verification, idempotency keys, server-side price only, trial and free-tier abuse limits.
Cloudflare or Clerk account creation and any key or DNS change is done by the user, Claude prepares the checklist and verifies the result.

## Stage 7 - IP and legal hygiene (gate: every asset has a known license or is ours)
Skills: `legal-advisor` (not a lawyer, flag for a human on real money or regulated data), `security-audit` Phase 0, `pentest-checklist`.
- Name: search trademark databases for the name in the target markets before committing, check domain and handles. A clash found after launch costs a rebrand.
- Assets: fonts, icons, stock photos, illustrations, music each need a license we can point to. Never reuse another creator's or competitor's images, copy, or UI (standing rule: no reusing others' videos or photos, and no photo reuse across projects). AI-generated assets follow the provider's commercial terms.
- Code: run a license audit on dependencies (MIT/Apache fine, AGPL/GPL needs a decision, no unlicensed snippets pasted from the web). Keep `LICENSE` and third-party notices.
- Legal pages before real users: privacy policy, terms, cookie notice, data deletion and export path (FreshExpiry has JSON export). Payments and PII escalate to a human.
- Do not copy a competitor's wording or layout. Learn the mechanism, make our own execution. Claims in copy need proof we hold.

## Stage 8 - Landing and launch (gate: one clear action above the fold, Lighthouse and a11y pass)
Skills: `saas-landing`, `landing-page-generator`, `seo`, `claude-seo:seo-page`, `vercel-deploy-preflight` (Rule 12 hard gate before any Vercel deploy), `document-generate`.
Landing follows Stage 2 to 4 output, not a template. Real product screenshots only. Then `security-audit` Phase 0 before "ready to ship".

## Stage 9 - Growth
Skills: `social-growth-science`, `content-factory`, `growth-engine`, `email-sequence`, `cold-email`, `motion-reel-pipeline`, `social-media-video`.
One channel first, the one Stage 1 found the crowd already using. Comment-CTA and educate-before-activate mechanics from the carousel swipe file. Instrument everything (Hopkins).

## Stage 10 - Operate and iterate
Skills: `observability-engineer`, `incident-responder`, `business-iq-owner-metrics`, `kaizen`.
Hardening backlog from the handoff doc: integration tests for tenant isolation, role checks on every write, rate limiting, migrations pipeline, notifications delivery, billing webhooks, pagination. Weekly review of the one metric that proves the Stage 1 promise.

## Account boundaries
Claude never creates accounts or types or submits passwords, even for the user's own local app when the browser autofills one. Hand sign-up clicks to the user. Never spend credits or money without asking.
