---
name: polsia
description: >
  "Become Polsia" mode — the AI-runs-the-whole-company platform pattern
  (chat-strategist → task router → specialized execution agents → overnight
  autonomous loop → morning report), reproduced using the user's own stack
  instead of a new SaaS. Trigger: "polsia mode", "activate polsia", "run this
  like polsia", "be polsia for X". Runs a business/project end-to-end: plans
  it, builds it, markets it, handles support, keeps iterating on a loop,
  reports back — without the user babysitting each step.
---

# Polsia Mode

Polsia (Ben Broca, launched late 2025) is a multi-agent SaaS that runs an
entire company: you give it a business idea, it plans the MVP, writes and
deploys the code, sets up marketing/ads/outbound, handles customer support,
and keeps doing recurring work on a schedule — waking up, working overnight,
reporting in the morning — all without a human in the loop.

**Its architecture (confirmed via research, sources below):**
1. **Chat agent / strategist** — the single interface. Takes the business
   direction (problem, audience, offer, constraints) and turns it into a plan
   (what to build first, MVP scope, infra, positioning).
2. **Task router** — assigns each planned task to a specialized agent, routed
   partly on cost, so no single agent runs away with unbounded autonomy.
3. **Specialized execution agents** — engineering (codes + deploys via
   Docker/K8s), marketing (creates assets, runs campaigns, sends outbound),
   support (responds to customers), research.
4. **Recurring autonomous loop** — works on a schedule/overnight even with no
   user input, reports back ("wake up, do work, send an update in the
   morning").
5. **Integrations** — GitHub, email, ad platforms, payment processors.

Sources: [timfrin.substack.com](https://timfrin.substack.com/p/how-polsia-builds-and-runs-companies), [backlinkmanagement.io](https://backlinkmanagement.io/blog/how-does-polsia-work), [b12.io](https://www.b12.io/ai-directory/polsia/), [toolcenter.ai](https://www.toolcenter.ai/en/tools/polsia)

**You don't need Polsia's SaaS to run this pattern — you already have every
layer, built and tested, as Claude Code skills/infra.** This skill is the
glue: it maps each Polsia layer to what you already have and defines the
activation sequence.

## Layer mapping — reuse, don't rebuild

| Polsia layer | What you already have | Notes |
|---|---|---|
| Chat agent / strategist | This session, acting as planner | Do the planning yourself first (§1) — don't skip straight to execution |
| Task router | `skill-router` + OVERSEER (CLAUDE.md Rule 7) | Classify + score every task, cross-check `python3 ~/.claude/overseer/search.py <terms>` before building anything custom |
| Cost-aware agent dispatch | `kyros-orchestrator` | Master tier keeps judgment; offload mechanical/repetitive work to local Ollama fleet instead of burning Claude tokens on grunt work |
| Engineering agent | Whichever language/framework skill fits (BUNDLE-A-backend, BUNDLE-B-frontend, database-design, etc.) + `secure-by-default` while writing + `vercel-deploy-preflight` before any deploy | |
| Marketing/growth agent | `social-growth-science`, `content-factory`, `growth-os`, `growth-engine`, `marketing-psychology`, `cold-email`, `wa-campaigns` | |
| Support agent | `customer-support` skill | |
| Recurring/overnight loop | `autonomous-mode` skill (risk-tiered LOW/MED/HIGH gate, decision ledger, NEEDS-YOU list) + `/loop` for the wake cadence | This IS Polsia's "works while you sleep" loop — already built |
| Morning report | `autonomous-mode` §7 review format | Already defined — reuse verbatim |
| Cross-session state | Handoff Log + memory system | Polsia has no equivalent; yours is stronger for a multi-account setup |

**Net: "Polsia mode" = `autonomous-mode`'s loop, aimed at a full
plan→build→market→support cycle instead of a single dev backlog, with
`skill-router`+`kyros-orchestrator` doing Polsia's task-routing/cost-dispatch
job.** Nothing new to build except the sequencing below.

## 1. Activation

Trigger phrases: "polsia mode", "activate polsia", "run this like polsia",
"be polsia for <project>".

On activation, ask (once, briefly) for whatever of these the user hasn't already
given: the business/project direction, the problem it solves, the target
audience, the offer, and any hard constraints (budget, brand, must-use-X).
If he's already described it in the conversation, don't re-ask — restate your
read of it back in one line and proceed.

Then, in order:

1. **Plan** (chat-agent/strategist step). Produce: MVP scope, build order,
   infra needs, positioning/offer, first marketing motion, support surface.
   Keep it tight — a plan, not a deck.
2. **Route** every planned task through `skill-router` + OVERSEER cross-check
   (Rule 7). Build the ordered backlog exactly like `autonomous-mode` §1.2 —
   this backlog spans build + marketing + support, not just code.
3. **Hand off to `autonomous-mode`'s loop machinery** for execution — same
   risk gate (LOW/MED/HIGH), same decision ledger, same NEEDS-YOU list, same
   `/loop` cadence, same Handoff Log discipline. Polsia mode does not
   reimplement any of this; it just feeds `autonomous-mode` a
   build+market+support backlog instead of a pure-dev one.
4. Confirm the plan + backlog to the user in one message, then go quiet until a
   stop condition (autonomous-mode §6) or he checks in.

## 2. What's different from plain `autonomous-mode`

- Backlog includes marketing/support/growth tasks alongside engineering, not
  just code.
- Frontend/marketing visual work still goes through `open-pinterest` /
  `frontend-reference-sources` first (Rule 7 frontend sub-rule) — Polsia mode
  doesn't skip the taste bar for speed.
- Anything Polsia's real product would do irreversibly and outward-facing —
  sending real emails/DMs, spending ad budget, taking real payments, posting
  publicly — is HIGH tier per `autonomous-mode` §2: build/stage/draft it,
  never fire it, always list it in NEEDS-YOU. This is the one deliberate gap
  from the real Polsia (which does act autonomously on these) — the user's
  standing rule (`feedback_user_drives_ai_gen_tools.md`, CLAUDE.md HIGH tier)
  overrides matching Polsia feature-for-feature here.
- Cost-routing: prefer `kyros-orchestrator`'s local Ollama dispatch for
  mechanical work (boilerplate, repetitive content variants, data cleanup)
  the way Polsia's router avoids running its expensive agent on cheap tasks.

## 2b. Quality gate — mandatory, not optional

Polsia's real edge isn't a smarter model, it's that every output hits real
production/real users immediately, forcing a verify-or-fail loop you don't
get for free. Reproduce that discipline explicitly — no backlog item is
markable "done" without its matching check actually run (not claimed):

| Output type | Required check before "done" |
|---|---|
| Frontend/UI/design | `design-review` or `taste-skill` monitor pass + a real browser screenshot (Playwright/claude-in-chrome) — `feedback_no_blind_frontend_claims.md` |
| Backend/code | `secure-by-default` self-scan + actual lint/typecheck/test run |
| Marketing/copy | Run your own draft back through `marketing-psychology` + `social-growth-science` as a critique pass, not just as the generator |
| Deploy | `vercel-deploy-preflight` clean pass |

If a check can't be run (no browser, no test harness), say so explicitly —
never claim a check passed that wasn't run.

**Throughput:** route mechanical/repetitive sub-tasks (boilerplate, content
variants, data cleanup, batch renames) through `kyros-orchestrator`'s local
Ollama dispatch instead of spending judgment-tier turns on them — this is
the cost-routing Polsia's real task-router does.

## 3. Ending it

Same stop conditions as `autonomous-mode` §6, plus: the plan's MVP milestone
is reached and shipped. Review format = `autonomous-mode` §7.
