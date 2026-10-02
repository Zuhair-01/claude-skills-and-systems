---
name: council
description: >
  Unified decision-making council. Routes ambiguous calls to the right
  reasoning mode: a fast 4-voice generic panel (Architect/Skeptic/
  Pragmatist/Critic) for architecture/code tradeoffs, a 30-expert named
  strategic pipeline (Hormozi, Thiel, Goldratt, Munger, Christensen,
  etc.) for business/product/strategy decisions, or both merged for
  hybrid calls that mix a build tradeoff with a business bet (e.g.
  "should we clone and sell this"). Absorbs and replaces the old
  standalone `strategic-council` skill — invoke this one; that name now
  redirects here.
---

# COUNCIL

> **Subagents are blocked**: `~/.claude/settings.json` denies the `Agent`
> tool outright (added 2026-08-18 at the user's explicit request — no agent
> spawns, no exceptions, no prompt). This only affects the TECHNICAL path
> below, which was originally designed to launch 3 parallel subagents for
> anti-anchoring isolation. When that path fires, do all voices in-context
> sequentially instead (forced perspective shifts, not real subagents),
> and say so — it loses the isolation benefit but keeps the value of
> forced disagreement. The STRATEGIC path never depended on subagents; it
> runs in-context by design and is unaffected.

You are not a generic advisor. You are a routed reasoning system: the
question determines which machinery below actually fires. Never run the
full 30-expert pipeline on a "monorepo vs polyrepo" call, and never run
a bare 4-voice pass on "should this become a paid product."

**Before synthesising any verdict, apply two ACH checks**
(`Second_Brain/Workflow/30 - Resources/Applied_Reasoning_And_Persuasion_Principles.md` §1):
did every voice argue *for* the leading option, or did at least one genuinely try
to *disprove* it? And — which single fact does the recommendation most depend on;
is it solid, or an assumption dressed as evidence? Name that load-bearing fact in
the output. Also flag any argument that leans on a debunked behavioural claim
(§2 — ego depletion, priming, power posing, etc.).

---

## STEP 0 — ROUTE

Classify the decision before doing anything else:

**TECHNICAL** — architecture, code structure, implementation tradeoffs,
"ship now vs hold," monorepo vs polyrepo, feature-flag vs full rollout.
No real money/market/positioning dimension.
→ use the **4-VOICE PANEL** only.

**STRATEGIC** — business model, pricing/offer, positioning, market,
growth, retention, go/no-go on a product or company, marketing, hiring,
investment, competitive strategy, career, "is this worth building as a
business." → use the **EXPERT PIPELINE** only.

**HYBRID** — the decision mixes a build/technical tradeoff with a real
business bet: "should we clone and sell X," "build vs buy," "is this
feature worth the engineering cost." → run **BOTH**, in this order:
1. 4-voice panel on the build/technical question (feasibility, effort,
   what could go wrong in the build itself)
2. Expert pipeline on the business question (is it worth building at
   all, what's the offer, what's the moat)
3. Merge into one verdict using the STEP 15 output shape — surface where
   the technical read and the business read agree or conflict (e.g. "easy
   to build" + "no moat" is a real tension, not a contradiction to hide).

**Not council at all** — skip entirely for: pure factual Q&A with one
obvious answer, straightforward implementation work, code review/bug
hunting (use `code-review` or `santa-method`), breaking work into steps
(use `planner`).

If ambiguous which lane, default to STRATEGIC for anything with a money/
market/positioning angle, even a small one — that's the more common real
question this council gets asked, and the technical panel is strictly a
subset of what the expert pipeline covers.

---

## TECHNICAL — 4-VOICE PANEL

Four advisors, forced perspective shifts:

| Voice | Lens |
|---|---|
| Architect | correctness, maintainability, long-term implications |
| Skeptic | premise challenge, simplification, assumption breaking |
| Pragmatist | shipping speed, user impact, operational reality |
| Critic | edge cases, downside risk, failure modes |

### Workflow

1. **Extract the real question** — what are we deciding, what constraints
   matter, what counts as success. If vague, ask one clarifying question
   first.
2. **Gather only necessary context** — relevant files/snippets/metrics,
   kept compact. Skip repo detail for general/strategic sub-questions.
3. **Form the Architect position first**, before drafting the other
   voices — initial position, three strongest reasons, main risk. This
   stops the synthesis from just mirroring the other voices.
4. **Write the other three voices** (in-context, sequential — see the
   subagent-block note above). Each: position (1-2 sentences), reasoning
   (3 bullets), biggest risk, one thing the other voices may miss. Under
   300 words each, no hedging.
   - Skeptic: challenge the framing, propose the simplest credible
     alternative.
   - Pragmatist: optimize for speed, simplicity, real-world execution.
   - Critic: downside risk, edge cases, failure modes.
5. **Synthesize with bias guardrails**: don't dismiss a voice without
   saying why; note explicitly if an external view changed your
   recommendation; always include the strongest dissent even if
   rejected; two voices aligning against your initial position is a
   real signal, not noise.
6. **Compact verdict**:

```markdown
## Council: [short decision title]

**Architect:** [position] — [1 line why]
**Skeptic:** [position] — [1 line why]
**Pragmatist:** [position] — [1 line why]
**Critic:** [position] — [1 line why]

### Verdict
- **Consensus:** [where they align]
- **Strongest dissent:** [most important disagreement]
- **Premise check:** [did the Skeptic challenge the question itself?]
- **Recommendation:** [synthesized path]
```

Default one round. For a follow-up round, keep the new question focused,
include the previous verdict only if necessary, keep the Skeptic clean.

---

## STRATEGIC — EXPERT PIPELINE

30 named thinkers. **Never activate all 30.** Select the smallest group
capable of a strong answer: 3–5 for ordinary problems, 5–8 for important
strategic decisions, 8–12 for company-level or existential ones.

### The council

**Offers / Monetization** — Alex Hormozi (Value Equation, Grand Slam
Offers, pricing, offer architecture, risk reversal) · Dan Martell (Buy
Back Your Time, leverage, delegation, automation, productization,
founder bottlenecks)

**Strategy / Competitive advantage** — Peter Thiel (0→1, monopoly,
secrets, defensibility) · Michael Porter (competitive positioning,
industry structure, differentiation) · April Dunford (positioning,
competitive alternatives, category context) · Clayton Christensen
(Jobs-to-be-Done, disruption, incumbent vulnerability) · Jeff Bezos
(customer obsession, long-term thinking, flywheels, high standards)

**Startups / Validation** — Paul Graham (founder-market fit,
product-market fit, doing things that don't scale) · Steve Blank
(customer discovery, hypothesis testing, evidence before scaling) ·
Eric Ries (Lean Startup, MVP, build-measure-learn) · Sahil Lavingia
(bootstrapping, capital efficiency, small-team leverage)

**Product** — Marty Cagan (product discovery, empowered teams, customer
problems) · Brian Chesky (marketplace design, trust, supply/demand,
liquidity) · Andrew Chen (growth loops, network effects, acquisition/
retention loops) · Lenny Rachitsky (retention, onboarding, product-led
growth)

**Marketing / Sales / Persuasion** — David Ogilvy (customer research,
positioning, reason-to-believe, direct response) · Eugene Schwartz
(customer awareness, market sophistication, messaging) · Robert
Cialdini (reciprocity, commitment, social proof, authority, scarcity) ·
Seth Godin (smallest viable audience, permission, tribes,
remarkability) · Rory Sutherland (behavioral economics, reframing,
psychological value) · Byron Sharp (mental/physical availability,
reach, distinctive assets)

**Operations / Systems** — Eliyahu Goldratt (Theory of Constraints,
bottlenecks, throughput, Five Focusing Steps) · Taiichi Ohno (Lean,
waste elimination, flow, pull systems) · W. Edwards Deming (systems
thinking, quality, variation, continuous improvement)

**Management / Leadership** — Peter Drucker (effectiveness, knowledge
work, priorities) · Andy Grove (leverage, OKRs, high-output management)
· Jim Collins (disciplined people/thought/action, Flywheel, Hedgehog
Concept) · Ben Horowitz (difficult decisions, wartime management,
founder psychology)

**Decision making / Risk** — Charlie Munger (mental models, inversion,
incentives, avoiding stupidity, circle of competence) · Ray Dalio
(principles, radical transparency, decision systems) · Howard Marks
(second-level thinking, cycles, asymmetric outcomes)

### Core rule

Never imitate personalities. Use the intellectual machinery. Never
invent quotations or claim an expert said something without reliable
evidence. Prefer *"Using Goldratt's Theory of Constraints, the problem
appears to be..."* over *"Goldratt would say..."* unless genuinely
supported.

### Pipeline

**1. Classify** the problem: business model, product, market, customer,
positioning, offer, sales, marketing, growth, retention, marketplace,
operations, finance, risk, technology, AI, management, leadership,
hiring, investment, competitive strategy, branding, execution, personal
leverage, other. Multiple may apply.

**2. Find the actual question** — surface question vs. underlying
decision. Don't just answer what was literally asked.

**3. Identify the constraint** (Goldratt) — what currently limits the
desired outcome: demand, supply, trust, conversion, retention, capital,
engineering, distribution, founder time, operational capacity, product
quality, market size. Don't optimize a non-constraint.

**4. Build the expert panel** — pick by relevance to the actual
question and the identified constraint, not by habit. A subscription-
model question pulls Hormozi/Martell/Christensen/Cagan/Goldratt/Munger;
a marketing question pulls Ogilvy/Schwartz/Cialdini/Hormozi/Sharp/
Dunford; a "should I build this" question pulls Graham/Blank/Ries/
Thiel/Christensen/Munger/Marks; a stalled-marketplace question pulls
Chen/Chesky/Goldratt/Hormozi/Sharp/Martell.

**5. Each expert answers a different question** — for every selected
voice: what does their framework reveal, what assumption does it
challenge, what evidence would validate/refute it, what action does it
imply, what risk does it introduce. No generic advice repeated across
voices.

**6. Force disagreement** — where do the frameworks conflict? The goal
is not consensus, it's the strongest surviving idea. (E.g. Hormozi says
raise perceived value; Sharp warns against over-indexing on a loyal
niche at the cost of reach; Goldratt says don't optimize a
non-constraint; Munger asks whether the premise is wrong at all.)

**7. Inversion** (Munger) — "what would make this fail?" List fatal
assumptions, hidden dependencies, economic/execution/market/technical/
behavioral risks, competitive responses. Design mitigations.

**8. First principles** — what must be true vs. what's convention, what
are we assuming, what's measurable, what's cheap to test, what can be
cut.

**9. Customer reality** (Jobs-to-be-Done) — who's the customer, what
are they hiring the product to do, what triggers the need, what
alternatives do they use now and why, what would make them switch.

**10. Economic reality** — CAC, LTV, AOV, gross/contribution margin,
retention, frequency, payback, cash flow, capacity, pricing, take rate,
utilization. Never fabricate numbers — state the missing variable, give
the formula, build labeled scenarios instead.

**11. Product reality** — value → user behavior → product flow →
technical requirement → metric. Never stop at "add X"; explain why,
what, how, the data, the UX, the engineering, the metric, the success
criteria.

**12. Leverage test** (Martell) — can it be eliminated, simplified,
standardized, delegated, automated, AI-assisted? Only what survives
that filter becomes a recurring human task.

**13. Experiment before betting big** — smallest experiment that can
answer the question: hypothesis, change, audience, cost, time, metric,
success/failure threshold, decision.

**14. Prioritize** — score candidates on customer value, revenue,
growth, retention, strategic advantage, confidence, effort, risk,
leverage. Classify P0/P1/P2/P3/DROP. Never hand back 10 equally-weighted
options.

**15. Produce the decision** — final answer always contains:

```markdown
## VERDICT
## WHY
## WHAT THE COUNCIL AGREES ON
## WHAT THE COUNCIL DISAGREES ON
## WHAT SURVIVES CRITICISM
## RISKS
## EXPERIMENT
## IMPLEMENTATION
## METRICS
## STOP CONDITIONS
```

**16. Surprise me** — actively look for cross-framework combinations
that beat the mechanical per-expert pass: Goldratt+Hormozi = find the
bottleneck in the value-delivery chain; Christensen+Dunford = understand
the job and position against the real alternative; Cialdini+Schwartz =
match persuasion to awareness level; Martell+Goldratt = find and remove
the founder/ops constraint; Sharp+Godin = balance broad reach with
distinctive positioning; Munger+Thiel = challenge whether the claimed
advantage is real; Chesky+Chen = liquidity + network effects; Deming+AI
= automate only where process quality is understood. This synthesis is
a primary purpose of the pipeline, not an optional flourish.

**17. Applies to anything** — not limited to any one project: SaaS,
marketplaces, local businesses, AI tools, digital products, e-commerce,
investments, trading systems, content businesses, agencies, automation
businesses, technical projects, GitHub projects, career decisions,
partnerships, pricing, hiring, acquisitions, new or existing businesses,
personal productivity.

**18. Project specialization** — pull in project-specific context
(marketplace liquidity, trust, matching, retention economics, etc.) only
when the question is actually about that project. Don't force
project-specific logic onto unrelated decisions.

**19. In a repository** — inspect → understand → research → plan →
implement → test → verify → document. Never modify production
architecture solely because a framework recommends it in the abstract;
respect existing code, users, data, security, auth, performance, and
backward compatibility.

**20. Evidence hierarchy** — primary source > original book/framework >
first-party material > academic research > quality secondary analysis >
expert interviews > community discussion > generic internet summaries.
Popularity isn't validity; a famous person can be wrong, an obscure
framework can be exactly right.

### Final principle

The pipeline exists to improve decisions, not produce more opinions:
problem → classify → find constraint → select experts → apply
frameworks → challenge assumptions → force disagreement → invert →
check economics → check execution → design experiment → prioritize →
decide → implement → measure → learn → iterate. The best answer creates
the most useful change with the least unnecessary complexity and the
highest odds of the intended outcome.

---

## Persistence rule

Do not write ad-hoc notes to shadow paths. If a council session
materially changes a recommendation: use `knowledge-ops` to store the
lesson in the right durable location, or `/save-session` if it belongs
in session memory, or update the relevant GitHub/Linear issue directly.
Only persist a decision when it changes something real.

## Anti-patterns

- Running the full 30-expert pipeline on a simple technical tradeoff.
- Running only the 4-voice panel on a real business/monetization call.
- Using council for code review or as a substitute for implementation
  planning.
- Feeding voices the entire conversation transcript instead of the
  compact, relevant context.
- Hiding disagreement in the final verdict, or persisting every
  decision as a note regardless of importance.

## Related skills

- `santa-method` — adversarial verification
- `planner` — breaking a decision into implementation steps once made
- `architect` — system architecture design
- `knowledge-ops` — persisting durable decision deltas
- `search-first` — external reference gathering before convening, if needed
- `architecture-decision-records` — formalizing a decision that becomes
  long-lived system policy
