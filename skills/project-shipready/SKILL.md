---
name: project-shipready
description: Finished-project sweep — when a build is functionally done, run the full "ready for the real world" pass (SEO/GEO, security gate, accessibility, analytics, legal, performance, monitoring, deploy checks) PLUS the public-presence/career pass (polished GitHub repo, portfolio entry, LinkedIn/X/socials post, documentation as a legacy artifact) before calling it shipped. Trigger proactively — don't wait to be asked — whenever the user says a project/feature/phase is done, working, ready, or finished; when a milestone matches a Handoff Log "resolved" entry; or when a build passes its tests/verification for the first time.
---

# Project Ship-Ready Sweep

Not a builder — a router + checklist. Each item is already owned by an
existing skill; invoke that skill for the real work, don't reimplement it
here. Only hand-build for a gap nothing below covers, and only after
`overseer/search.py` confirms nothing already does it.

## Execution algorithm — exactly what to do, in order

1. Notice the trigger (see frontmatter) → say the one-line offer from
   Step -1. If declined, still run step 1 of the Sequence (security gate)
   silently — it's non-negotiable — and stop there.
2. If accepted: run Step 0 (scope the project), state the type + which
   numbered steps you're skipping and why, in one message.
3. Walk the Sequence **in the numbered order** — order matters (security
   before anything ships, tests before monitoring is meaningful, ship
   quality gates before the public-presence pass, since you don't want to
   publicize something with an open gap). For each step:
   a. `Skill(<name>)` to invoke the owning skill.
   b. Let it do its actual work (audit/fix/build) — don't summarize what
      it "would" do, actually run it.
   c. Record one checklist line per step per the Report format below.
   d. If a step surfaces a ❌ blocker, keep going through the rest of the
      technical steps (2-11) so the user gets the full picture in one pass —
      but do NOT start step 12 (public-presence) until every ❌ from
      steps 1-11 is resolved or explicitly waived by the user. Shipping the
      marketing pass for a project with known open gaps misrepresents it.
4. Only after steps 1-11 are clean (or waived): run step 12. Draft the
   README/case-study/post copy, show it to the user, wait for his go before
   any actual publish/post/apply action.
5. End with the Report format's ship/no-ship verdict line, plus — once
   step 12 ran — a one-line list of what's now public/updated and where
   (repo made public, portfolio entry added, LinkedIn post drafted/sent).
6. If this sweep took real time/produced a milestone, follow CLAUDE.md
   Rule 2 (Handoff Log entry) as normal — this skill doesn't replace that,
   it's a candidate trigger for it.

## Step -1 — Don't wait to be invoked

This is a standing reminder, not just an on-demand tool: the moment a
project/feature reaches "it works" (tests pass, verified live per
[[feedback_no_blind_frontend_claims]]), proactively say so and offer this
sweep — don't sit on it until the user separately asks. One line is enough:
"X is working — want the ship-ready + public-presence sweep before we
call it done?" Proceed solo only once he confirms (same opt-in bar as
Rule 10's parallel-session suggestion), except for the security gate
(step 1), which always runs regardless of whether the rest is wanted.

## Step 0 — Scope the project (before running anything)

Name the project type out loud, it decides which steps apply:
- **Public web app/site** (has visitors) → all steps below apply.
- **API-only/backend service** (no UI) → skip 5/6/9, keep the rest.
- **Internal tool** (no public traffic) → skip 2/3/7 (SEO/GEO/analytics
  don't apply), keep security/accessibility/monitoring/deploy.
- **Mobile app** → swap step 2 for App Store/Play listing ASO instead of
  web SEO; keep the rest.

State which type it is and which steps are skipped, in one line, before
starting — don't silently drop a step.

## Sequence

1. **Security gate (mandatory, CLAUDE.md Rule 8)** — `Skill("security-audit")`
   Phase 0 Vibe-Code Pre-Ship Gate, run first, always: secrets, auth/authz,
   IDOR, injection, CORS/headers/cookies, admin/debug routes exposed,
   webhook signature checks.
2. **SEO + GEO** — `Skill("seo")`: technical SEO, on-page, schema,
   sitemap/robots.txt, AI-search readiness (GEO — llms.txt, structured
   answer-friendly content). Include social/share meta (OG tags,
   Twitter card, favicon, title/description per page) — commonly missed.
3. **Analytics** — `Skill("analytics")`: confirm tracking/events actually
   fire (GA4/conversion events), not just installed.
4. **Accessibility** — `Skill("accessibility")` WCAG 2.2 AA pass.
5. **Performance** — `Skill("performance-optimizer")`: bundle size, Core
   Web Vitals, image optimization, caching headers.
6. **Design final pass** — `Skill("design-review")`: visual audit +
   before/after screenshots.
7. **Legal** — `Skill("legal-advisor")`: privacy policy/ToS/cookie notice
   present if the project collects any user data, analytics, or payment.
8. **Test coverage** — `Skill("e2e-testing")` (or the project's existing
   suite): golden path + critical edge cases actually pass, not just unit
   tests. Then `Skill("run")` to launch it live and click through the
   golden path yourself — don't claim done on tests alone
   ([[feedback_no_blind_frontend_claims]]).
9. **Monitoring & recovery** — error tracking/alerting wired (Sentry or
   equivalent), uptime check exists, and there's an actual rollback path
   (previous deploy/tag, DB backup) if the ship goes wrong. A project
   with no way to know it broke, or no way back, isn't ship-ready even if
   it passes everything else.
10. **Release hygiene** — changelog/README updated
    (`Skill("technical-change-tracker")` or manual), version bumped,
    git tag cut if the project uses them ([[project_ostazi_deploy_workflow]]
    style: preview first, prod only when explicitly told).
11. **Regulated-data escalation** — if real payments/PII/health data:
    `Skill("pentest-checklist")` / `Skill("threat-modeling-expert")`
    (Rule 8 escalation, phases 1-7).
12. **Public presence & legacy pass** — this is the part that turns a
    finished project into career capital, not just a working build. Do
    this for every project unless the user says keep it private:
    - **GitHub, made to sell you**: `Skill("readme")` for an "absurdly
      thorough" README (problem, architecture, real screenshots/GIF/demo
      link, tech stack, what you built vs. used, notable engineering
      decisions). Pin the repo, add topics/tags, a clean commit history
      (this is already covered by [[feedback_ostazi_deploy_workflow]]-style
      discipline — don't rewrite history to make it look better, let real
      work speak). `Skill("logo-branding")` only if the project has no
      visual identity yet and warrants one.
    - **Portfolio**: `Skill("interactive-portfolio")` — add/update the
      project as a case study (problem → approach → outcome → what you'd
      do differently), not just a link dump.
    - **LinkedIn**: `Skill("linkedin-profile-optimizer")` to keep the
      profile itself current (headline/about/experience reflect this
      body of work), then a real post about the project via
      `Skill("linkedin-cli")` or `Skill("linkedin-automation")` — what
      was built, what problem it solved, one real technical detail worth
      knowing, not generic hype copy (`Skill("copywriting")` /
      `Skill("brand-voice")` for tone if needed).
    - **Other socials / dev community**: X/Twitter, and where relevant
      Dev.to/Hacker News/relevant subreddit — same real-substance angle,
      adapted per platform's norms, not copy-pasted.
    - **Career pipeline**: `Skill("career-ops")` to log the project as
      evidence in whatever CV/application tracking is active, if job
      search is currently a live goal.
    - Always draft the post/README copy and show the user before actually
      publishing to LinkedIn/X/GitHub-public or applying anywhere — these
      are public/irreversible-ish actions per the standing executing-
      actions-with-care rule, not something to auto-fire.

## Report format

One flat checklist, most-severe first, no essay per item:
- ✅ done — nothing needed
- ⚠️ gap found + fixed inline (say what)
- ❌ gap found, needs the user's call (say what and why it can't be auto-fixed)

End with one line: overall ship/no-ship verdict and the top blocker if not
ship-ready.

## Rules

- Skip a step only per Step 0's scoping, and say why in one line — never
  silently drop it.
- Run OVERSEER (`python3 ~/.claude/overseer/search.py <topic>`) for any
  domain-specific concern not covered above (e-commerce → payment
  security, blockchain → solidity-security, i18n → i18n-localization)
  before assuming this checklist is exhaustive.
- This skill layers on top of Rule 8's gate, not around it — security
  still runs first, always, even on internal tools.
- Never push to prod / tag a release / flip a live flag without the user's
  explicit go — this skill finds and fixes gaps, it doesn't self-authorize
  the actual launch action.
