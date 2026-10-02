---
name: skill-router
description: >
  Autonomous proactive skill orchestrator. Runs silently before EVERY substantive task response.
  Classifies domain + action type, scores skills by confidence, outputs an ordered 2-5 skill
  stack with invocation mode (INVOKE/REF) and specific commands. Trigger: ANY task involving
  coding, debugging, design, marketing, video/UGC, data, agents/AI, devops, security,
  writing, automation, research, trading, or analysis. Do NOT wait to be asked — fire first.
---

# Skill Router v2.0

**Proactive. Silent by default. Always first.**

Classify → Score → Stack → Execute. Zero interviews. Zero yapping.

---

## Weak Points Fixed (vs old version)

| Old weakness | Fix |
|---|---|
| Reactive only (user had to ask) | Fires before every task |
| Single-skill recommendations | 2-5 skill stacks, phase-ordered |
| Keyword matching at 30% confidence | 75% threshold to INVOKE, 45% for REF |
| No phase ordering | Phase 0-ORIENT → 1-PLAN → 2-EXECUTE → 3-VALIDATE → 4-SHIP |
| General over specific | Most specific skill wins (django-tdd > tdd-workflow for Django) |
| No cross-domain handling | Two domains detected → stack merges both |
| Sub-skills ignored | Surface the right sub-skill (threejs-shaders not just threejs) |
| No INVOKE vs REF distinction | INVOKE = load full instructions; REF = apply patterns silently |

---

## Classification

**Primary domain** (pick one or two for cross-domain tasks):
`engineering` · `design` · `marketing` · `video/media` · `data/ML` · `agent/AI` · `devops/infra` · `security` · `writing/docs` · `automation/integration` · `research` · `trading/finance`

**Action type:**
`build` · `debug` · `design` · `analyze` · `write` · `optimize` · `research` · `automate` · `deploy` · `review` · `plan`

**Complexity:**
`simple` (1 skill) · `standard` (1-3 skills) · `complex` (normally 2-4; exceed only for distinct phases or high-risk gates)`

---

## Confidence Thresholds

- **≥75%** → **INVOKE** via Skill tool (load full instructions, follow them completely)
- **45–74%** → **REF** (apply the skill's patterns without calling the Skill tool)
- **<45%** → **SKIP** (mention briefly if it's tempting but doesn't fit)

Use the smallest stack that materially improves the result. Normally choose one primary skill and at most two supporting skills. Exceed three only when separate phases or a high-risk validation gate genuinely require it; every extra skill must earn its context cost.

---

## OVERSEER Integration (this IS the unified system — read before routing)

`~/.claude/overseer/` ships several Python modules (`task_interceptor.py`,
`smart_selector.py`, `persistent_activation.py`) that *describe* a pipeline
where skill-router feeds OVERSEER automatically. **None of that Python is
wired into a hook** (`settings.json` has no `UserPromptSubmit`/`PreToolUse`
entry calling any of it) — it has never executed on its own. Don't treat
those files as live infrastructure or assume routing already happens
through them.

The only two pieces of this system that are actually live are **this
SKILL.md** (loaded and followed whenever skill-router fires) and
**OVERSEER's `search.py`** (runs when a command explicitly calls it). The
real merge is making Step 2 below always include OVERSEER, not just the
static tables:

**Step 2 — Score, every time:**
1. Check the current available-skills listing (already in context) first —
   free, no shell call.
2. Cross-check against `~/.claude/overseer/index.tsv` — grep it directly,
   or run `python ~/.claude/overseer/search.py <keywords>` — for the
   ~3,650 skills/agents kept off-context (per CLAUDE.md Rule 6). This
   covers cases the static Domain Routing Tables below don't, and catches
   entries in those tables that may have drifted from what's actually
   installed.
3. Merge both sources into the stack. Never invoke a skill name you
   haven't confirmed exists in one of the two checks above — a routing
   table entry is a pointer to the right capability, not a guaranteed
   literal name.

---

## Phase Ordering (always respect this sequence)

| Phase | Purpose | Key skills |
|---|---|---|
| 0-ORIENT | Understand unfamiliar codebase/domain | `codebase-onboarding`, `mpocock-zoom-out`, `mpocock-diagnose` |
| 1-PLAN | Spec, architecture, PRD, issues | `mpocock-to-prd`, `plan-orchestrate`, `software-architecture`, `mpocock-to-issues` |
| 2-EXECUTE | Build, implement, automate | domain-specific skill (see tables below) |
| 3-VALIDATE | Test, QA, review, audit, security | `mpocock-tdd`, `mpocock-review`, `security-review`, `mpocock-qa` |
| 4-SHIP | Deploy, PR, commit, handoff | `mpocock-git-guardrails-claude-code`, `caveman-commit` REF, `mpocock-handoff` |

Skip phases that don't apply. Never reorder — always plan before build.

---

## Output Format

Routing is internal and silent by default. Emit this block only when the user explicitly asks how the task was routed, which skills are being used, or requests interactive consultation:

```
▸ ROUTER [domain × action] [complexity]
  1. [skill-name]   INVOKE — [specific thing to extract or do]
  2. [skill-name]   INVOKE — [specific thing to extract or do]  
  3. [skill-name]   REF   — [which specific pattern to apply]
  ✗ [skill-name]   SKIP  — [one-line reason]
```

List only the selected skills. Then proceed immediately — no transition phrases.

---

## MCP Servers — live tool routing (installed, use proactively)

These are live tools, not skills — no INVOKE needed, just use them when the task fits.
Installed at user scope 2026-08-30 (`claude mcp list` to confirm connected).

```
navigate/read/edit an unfamiliar codebase → serena (mcp__serena__*): symbol-level
    find_symbol / find_referencing_symbols / get_symbols_overview / replace_symbol_body.
    Use INSTEAD OF blind grep+Read sweeps on any repo >~15 files. Big token saver.
    Complements Kyros (Kyros plans/routes, serena navigates). First use per repo:
    it auto-activates the cwd project under --context ide-assistant.
whole-repo context for an audit/review/ship-gate → repomix (mcp__repomix__*):
    pack_codebase → one structured token-budgeted blob. Pair with project-shipready,
    security-audit, mpocock-review, code-review on a fresh repo.
browser automation / e2e / "see the page" → playwright MCP (mcp__playwright__*):
    headless, scriptable, accessibility-tree (no screenshot-to-vision loop).
    Use for webapp-testing / e2e-testing / browser-qa. claude-in-chrome stays the
    pick when the LIVE logged-in profile is needed; playwright MCP for clean headless.
docs/library API lookup → context7 (already wired). hard multi-step reasoning →
    sequential-thinking (already wired).
```

## Domain Routing Tables

### Engineering — Debug / Diagnose
```
any bug/regression  → mpocock-diagnose INVOKE (phase-gated feedback loop) + serena for symbol tracing
unfamiliar codebase → serena (mcp__serena__*) FIRST — map symbols before editing
perf regression     → mpocock-diagnose + performance-optimizer
db slow queries     → database-optimizer + sql-optimization-patterns  
error tracing       → error-handling + distributed-tracing REF
```

### Engineering — Build (by stack)
```
react               → react-best-practices, react-patterns
nextjs              → nextjs-app-router-patterns, nextjs-best-practices
fastapi/python      → fastapi-patterns, python-testing-patterns
django              → django-patterns, django-tdd, django-security
typescript          → typescript-pro, typescript-advanced-types
node/express        → nodejs-best-practices, nodejs-backend-patterns
rust                → rust-pro, rust-async-patterns
golang              → golang-patterns, golang-pro
laravel/php         → laravel-expert, laravel-tdd
react-native        → react-native-architecture, mobile-design
swift/iOS           → ios-developer, swiftui-expert-skill
nestjs              → nestjs-expert, nestjs-patterns
```

### Engineering — Review / Audit
```
code review         → mpocock-review INVOKE + repomix (mcp__repomix__*) for whole-repo context
arch review         → mpocock-zoom-out INVOKE + architect-review + serena for symbol map
diagram the arch    → archify INVOKE (render architecture/workflow/sequence/dataflow/lifecycle diagram as standalone HTML+SVG)
security audit      → security-review + mpocock-qa
pre-push            → codebase-audit-pre-push
PR review           → differential-review
```

### Engineering — Plan / Spec / Issues
```
feature spec/PRD    → mpocock-to-prd INVOKE → mpocock-to-issues INVOKE
new project arch    → software-architecture + plan-orchestrate
refactor plan       → mpocock-improve-codebase-architecture INVOKE
issue triage        → mpocock-triage INVOKE
prototype/PoC       → mpocock-prototype INVOKE
```

### Design
```
published Artifact  → artifact-quality INVOKE (single-file HTML on claude.ai; medium constraints + per-category playbook), then taste-skill 4/6/9 + artifact-design
UI component        → frontend-design-direction, shadcn-ui, make-interfaces-feel-better
design system       → design-system, figma-generate-library
UX/flow             → ux-flow, ux-audit, mpocock-design-an-interface INVOKE
landing page        → frontend-design, landing-page-generator
mobile UI           → mobile-design, swiftui-design (iOS) / android-jetpack-compose-expert (Android)
motion/animation    → motion-ui (components) · GSAP for scroll/pin/timeline/SplitText/SVG-morph (gsap-scrolltrigger, gsap-plugins, gsap-core — all free since Apr 2025) · source feel via frontend-reference-sources
3D web              → threejs / threejs-shaders / threejs-animation (raw) · Spline (spline-3d-integration) for no-code designer scenes
charts / data-viz   → bklit UI via shadcn (bklit.com registry + ui.bklit.com/studio) — over hand-rolled Recharts
arch/system diagram → archify INVOKE (architecture, workflow, sequence, dataflow, lifecycle/state; also "beautify/convert this Mermaid")
```

### Marketing
```
social/short-form   → READ Second_Brain/.../30-Resources/Social_Content_Skill_Ecosystem.md FIRST, then stack per lane (A strategy/copy · B script/format · C produce-pick-one · D post/repurpose). content-factory = orchestrator.
ad copy             → ad-creative, ads, copywriting
SEO content         → ai-seo, seo-content-writer, programmatic-seo
email campaign      → emails, cold-email, email-sequence
CRO                 → cro, signup, onboarding-cro, popups
competitor intel    → competitor-profiling, competitors
social content      → social, content-strategy, content-creator
growth/referral     → referrals, lead-magnets, free-tools
lead gen / local biz → gmaps-scraper INVOKE (Google Maps: name/phone/website/rating/email for niche+city; native exe, no Docker) → then lead-intelligence for scoring/outreach, wa-campaigns for WhatsApp
launch              → launch, launch-strategy, product-marketing
pricing page        → pricing, pricing-page, paywalls
analytics           → analytics, ab-testing, analytics-tracking
```

### Video / Media / UGC
```
social video (any)  → READ Social_Content_Skill_Ecosystem.md (30-Resources) — lane C picks ONE produce sub-lane, never stack
UGC video           → ugc-video-auto, ugc-ads-workflow, 07-ecommerce-ad
cinematic           → 01-cinematic, cinema-director, storyboard
AI video gen        → seedance-2-0, ai-video-gen, fal-video-edit
short-form ads      → 11-social-hook, 06-motion-design-ad, video-shortform
product video       → 09-product-360, product-showcase-video, product-video-ad-maker
3D / CGI            → 02-3d-cgi, 3d-logo-animation, fal-3d
music video         → 10-music-video, ai-music-album
social clips        → youtube-clipper, youtube-shorts, ai-clipping
```

### Agent / AI Architecture
```
agent design        → agentic-os, agent-architecture-audit, plan-orchestrate
multi-agent         → multi-agent-patterns, agent-orchestrator, dispatching-parallel-agents
MCP server          → mcp-builder, mcp-server-patterns
LLM app             → llm-app-patterns, pydantic-ai
agent memory        → agent-memory-systems, agent-memory-mcp
evaluation          → agent-eval, advanced-evaluation, eval-harness
```

### Data / ML
```
data pipeline       → data-engineer, airflow-dag-patterns, dbt-transformation-patterns
ML engineering      → mle-workflow, ml-pipeline-workflow, pytorch-patterns
analytics dash      → analytics-product, dashboard-builder, d3-visualization
database            → database-optimizer, postgres-patterns, mysql-patterns
RAG                 → rag-engineer, rag-implementation, embedding-strategies
```

### DevOps / Infra
```
CI/CD               → github-actions-templates, devops-deploy
docker/k8s          → docker-expert, kubernetes-architect
terraform           → terraform-specialist, terraform-infrastructure
monitoring          → grafana-dashboards, observability-engineer
cloud               → aws-serverless, gcp-cloud-run, azure-functions
```

### Security
```
code security       → security-review, security-scanning-security-sast
penetration         → pentest-checklist, ethical-hacking-methodology
compliance          → hipaa-compliance, pci-compliance, gdpr-data-handling
secrets             → secrets-management
```

### Automation / Integration
```
n8n workflow        → n8n-workflow-patterns, n8n-mcp-tools-expert
SaaS connector      → [name]-automation (direct name match)
cross-platform      → zapier-make-patterns, workflow-automation
offload autonomous  → OpenCode (self-contained/mechanical, saves tokens) · Kyros (local Ollama fleet) · manus.im (cloud sandbox: open-ended web research across many sites + structured deliverable, e.g. "research 10 competitors → pricing spreadsheet"; credit-based, no team workspace/persistent memory, needs oversight). Suggest, don't auto-open (CLAUDE.md Rule 10).
```

### AI CLI Tool Management (CC Switch)
```
switch API provider → cc-switch INVOKE
manage skills GUI   → cc-switch INVOKE
browse/resume sess  → cc-switch INVOKE
MCP management      → cc-switch INVOKE
usage/cost tracking → cc-switch INVOKE
provider failover   → cc-switch INVOKE
```

### Token / Usage Optimization
```
hit usage limits    → usage-limit-reducer INVOKE (diagnose + apply Dubi's 11 rules)
chat too long       → usage-limit-reducer INVOKE (Rule #2: fresh chat / /compact)
burning tokens fast → usage-limit-reducer INVOKE
wrong model in use  → usage-limit-reducer INVOKE (Rule #8: switch to Haiku)
save tokens         → usage-limit-reducer INVOKE
```

### Trading / Finance
```
TradingView         → opentrade-* skills
market data         → alpha-vantage, polygon-io-automation
backtesting         → backtesting-frameworks, quant-analyst
```

### Writing / Documentation
```
technical docs      → documentation, api-documentation-generator
blog/article        → blog-post, content-creator, mpocock-edit-article INVOKE
PRD/spec            → mpocock-to-prd INVOKE
commit messages     → caveman-commit REF (always)
```

---

## Mandatory Pairings (always apply these)

| Task type | Always add |
|---|---|
| Any build | + test skill (`mpocock-tdd`, `laravel-tdd`, `django-tdd`, etc.) |
| Any deploy | + `mpocock-git-guardrails-claude-code` REF |
| Any security-sensitive | + `security-review` |
| Any agent task | + `superpowers:verification-before-completion` |
| Complex plan | + `superpowers:executing-plans` |
| Any commit | + `caveman-commit` REF |
| Editing an unfamiliar / large codebase | + `serena` (mcp__serena__* symbol tools) instead of grep+Read sweeps |
| Any full-repo audit / review / ship-gate | + `repomix` (mcp__repomix__pack_codebase) for context |
| Any browser e2e / webapp test | + `playwright` MCP (headless) unless the live profile is needed |

---

## Conflict Resolution

1. Two skills do same thing → pick more specific, SKIP the general
2. Two skills cover different phases → both valid, order by phase
3. Skill exists but depth not needed → REF not INVOKE
4. Cross-domain task → merge stacks, interleave by phase, no arbitrary cap

---

## Anti-Patterns

- Invoking skills below <45% confidence with no clear reason
- Invoking skills that overlap without phase distinction
- Picking `tdd-workflow` when `django-tdd` exists for a Django task
- Skipping PLAN phase for complex tasks
- Using `-automation` suffix skills for non-integration tasks (they're SaaS connectors)
- Running mpocock-diagnose AND systematic-debugging on same bug (pick one)

---

## Explicit Consultation Mode

Everything above is the **default, silent, proactive mode** — fires before
every substantive task, no interview, just routes and proceeds. The
sections below are a **separate, opt-in mode**: only use this interview
flow when the user directly asks skill-router to help them pick a skill
interactively (e.g. "which skill should I use for X, walk me through it")
rather than just working on a task. Do not use this mode as a substitute
for the silent default — most tasks should never reach this section.

### Step 1 — Acknowledge and open the interview

Respond warmly and tell the user you'll ask a few quick questions to find
the right skill for them. Do NOT suggest any skills yet.

Example opener:
> "No problem — let me ask you a few quick questions so I can point you to
> exactly the right skill."

---

### Step 2 — Ask the Funnel Questions (one at a time, in order)

Ask only what you need. If an earlier answer makes a later question
irrelevant, skip it.

**Q1 — What is the broad area of the task?**
Present these as numbered options:
1. Building / coding something (app, feature, component, script)
2. Fixing or debugging something that's broken
3. Security, pentesting, or vulnerability assessment
4. AI agents, LLMs, or automation pipelines
5. Marketing, SEO, content, or growth
6. DevOps, infrastructure, deployment, or git
7. Design, UI/UX, or creative output
8. Planning, strategy, or documentation
9. Something else (ask them to describe it)

**Q2 — How specific is the task?**
1. I have a clear spec / I know exactly what I want built
2. I have a rough idea but need help shaping it
3. I'm totally starting from scratch with no clear direction

**Q3 — What tech stack or domain is involved?** (only ask if relevant)
Examples: React / Next.js, Node.js, Python, AWS, Stripe, AI/LLM, no-code, etc.
If they say "not sure" or "any", that's fine — move on.

**Q4 — Do you want to work autonomously (agent does everything) or
collaboratively (you stay in the loop)?**
1. Fully autonomous — just go
2. Collaborative — I want to review/approve steps
3. Not sure yet

---

### Step 3 — Recommend skills

Based on their answers, recommend **1 primary skill** and up to **2 secondary
skills**. Structure your recommendation exactly like this:

**✅ Primary Skill: `@skill-name`**
*Why:* [1–2 sentences explaining why this is the best fit for what they described]
*Invoke it like this:*
```
@skill-name [paste their goal here]
```

**🔁 Also consider:**
- `@skill-name-2` — [one sentence on when to layer this in]
- `@skill-name-3` — [one sentence on when to layer this in]

---

### Step 4 — Offer a ready-made prompt

After the recommendation, offer to write them a ready-to-use prompt they
can paste directly into Antigravity. Ask:

> "Want me to write the full prompt for you so you can just paste it in?"

If yes, compose a complete, specific prompt using the recommended skill and
everything you learned about their goal from the interview.

---

## Example Interaction

```
User: @skill-router I want to build something but I'm not sure where to start

Agent: No problem — let me ask a few quick questions.
       What is the broad area?
       (1) Building  (2) Debugging  (3) Security  (4) AI/LLM
       (5) Marketing  (6) DevOps  (7) Design  (8) Planning

User: 1 - building something

Agent: How specific is the task?
       (1) Clear spec  (2) Rough idea  (3) Starting from scratch

User: 2 - rough idea

Agent: What tech stack? (React, Node, Python, etc. — or "not sure")

User: Next.js

Agent: ✅ Primary Skill: @brainstorming
       Why: You have a rough idea that needs shaping before building.
       Brainstorming asks structured questions and produces a clear spec.

       @brainstorming help me design a [your app idea] using Next.js

       🔁 Also consider:
       - @plan-writing — once brainstorming produces a spec, break it into tasks
       - @senior-fullstack — when you are ready to start building

       Want me to write the full prompt for you?
```

---

## Skill Routing Reference

### Building a full product or app from scratch
- Primary: `@app-builder`
- If they want to plan first: `@brainstorming` → `@plan-writing` → `@app-builder`
- If they want it fully autonomous: `@loki-mode`

### Building a specific frontend feature / UI
- Primary: `@senior-fullstack` or `@frontend-design`
- Stack-specific: `@react-patterns`, `@nextjs-best-practices`, `@tailwind-patterns`
- If they want a full design system: `@ui-ux-pro-max` + `@core-components`

### Building a backend API or service
- Primary: `@backend-dev-guidelines`
- Stack-specific: `@nodejs-best-practices`, `@python-patterns`, `@nestjs-expert`
- API design: `@api-patterns`
- Database: `@database-design` + `@prisma-expert`

### Debugging something broken
- Primary: `@systematic-debugging`
- If tests are failing: `@test-fixing`
- If it's a code quality issue: `@clean-code`

### Writing tests / TDD
- Primary: `@tdd`
- For Playwright/browser tests: `@playwright-skill` + drive via `playwright` MCP (mcp__playwright__*, headless)
- For Jest patterns: `@testing-patterns`

### Integrating a third-party service
- Payments: `@stripe-integration`
- Auth: `@clerk-auth` or `@nextjs-supabase-auth`
- Database: `@neon-postgres` or `@firebase`
- Messaging: `@twilio-communications`
- Bots: `@slack-bot-builder`, `@discord-bot-architect`, `@telegram-bot-builder`
- File storage: `@file-uploads`
- Analytics: `@analytics-tracking`

### AI / LLM / agents
- Architecture: `@ai-agents-architect`
- RAG pipelines: `@rag-engineer`
- Prompts: `@prompt-engineer`
- Multi-agent: `@langgraph` or `@crewai`
- Observability: `@langfuse`
- Voice: `@voice-agents`

### Security / pentesting
- Start here: `@ethical-hacking-methodology` + `@pentest-checklist`
- Web app testing: `@burp-suite-testing`, `@sql-injection-testing`, `@xss-html-injection`
- Network/infra: `@aws-penetration-testing`, `@linux-privilege-escalation`
- Reference: `@top-web-vulnerabilities`

### DevOps / infrastructure / deployment
- Docker: `@docker-expert`
- Cloud: `@aws-serverless`, `@gcp-cloud-run`, `@vercel-deployment`
- Git workflow: `@git-pushing`, `@using-git-worktrees`, `@github-workflow-automation`
- Scripting: `@linux-shell-scripting`

### Marketing / growth / SEO
- Copy: `@copywriting`
- Landing pages: `@page-cro`
- SEO: `@seo-fundamentals` + `@seo-audit`
- Email: `@email-sequence`
- Ads: `@paid-ads`
- Launch: `@launch-strategy`

### Planning / architecture / strategy
- Quick plan: `@concise-planning`
- Full plan: `@plan-writing` → `@executing-plans`
- Architecture: `@software-architecture` or `@senior-architect`
- Product strategy: `@product-manager-toolkit`

### Creative / design / visuals
- UI: `@frontend-design`
- Real-world visual/motion look wanted (before any UI build) → `@frontend-reference-sources` FIRST
  (routes to open-pinterest / refero.design / supahero.io / 60fps.design / 21st.dev / motion.dev)
- Data viz: `@claude-d3js-skill`
- Generative art: `@algorithmic-art`
- Presentations: `@pptx-official`

### Fully autonomous / parallel execution
- Full startup mode: `@loki-mode`
- Independent parallel tasks: `@dispatching-parallel-agents`
- Plan then execute: `@subagent-driven-development`

### Document creation
- Word doc: `@docx-official`
- PDF: `@pdf-official`
- Spreadsheet: `@xlsx-official`
- Presentation: `@pptx-official`

---

## Constraints

- In explicit consultation mode, never recommend more than 1 primary skill and 2 secondary skills at a time.
- Always include the exact `@invoke` syntax so users can copy-paste it.
- If the user's goal spans multiple categories, pick the most upstream skill
  (e.g. `@brainstorming` before `@senior-fullstack`).
- Do not overwhelm the user with the full skill list. Recommend only what is
  relevant to their specific answers.
- If the user is totally lost, default to `@brainstorming` for open-ended
  goals, or `@app-builder` for anything involving building something.
- After recommending, always offer to write a ready-made prompt for them.

---

## Limitations

- Only recommends skills from the installed library. If a skill is not
  installed, the recommendation may not work.
- Routing is based on natural language matching. Highly ambiguous goals
  may require follow-up clarification.
- Does not execute the recommended skill — it only recommends it. The user
  must invoke the skill themselves.
- The routing reference covers the most common skills but does not include
  every skill in the library.
