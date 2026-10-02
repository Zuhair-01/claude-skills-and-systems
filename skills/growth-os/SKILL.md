---
name: growth-os
description: Use before any marketing/growth/acquisition work for any business (ours or a client's) — diagnoses the actual growth constraint before recommending channels or content, so effort goes where it moves revenue, not where it's easiest to produce output.
---

# Growth OS

A reusable diagnostic methodology, not a platform. Apply it inline — no separate database, no agent swarm, no new codebase. If a task needs software (a referral tracker, an analytics dashboard), build that as a normal feature in the target app's existing stack, per its own conventions. This skill is the *thinking process* that decides what to build and why.

## The one rule that matters most

**Never jump from "we need marketing" to "here are 10 posts."** Diagnose first. Marketing effort aimed at the wrong bottleneck is wasted regardless of execution quality.

Once the real constraint is identified, execute via `growth-engine` (tactical channel playbooks:
SEO, ASO, viral loops, email/CRM, referral) or a specific channel skill (`seo`, `email-sequence`,
`cold-email`, `social`) — this skill only decides *what* to build, not how.

## Step 1 — Classify the business

Don't default to SaaS/social-media playbooks. Identify the actual model: marketplace, SaaS, local service, ecommerce, creator, content platform, professional service, hybrid. The model determines which growth mechanics even apply (e.g. a marketplace has two sides to acquire, each independently; a SaaS has one funnel).

## Step 2 — Find the real constraint

Ask, in order, and stop at the first "no":

1. Do people who need this know it exists? → No = **awareness problem**
2. Do they understand why it's better than what they do today? → No = **positioning problem**
3. Is the offer actually worth what's being asked? → No = **offer problem**
4. Are the right people finding it but not converting? → No = **conversion/funnel problem**
5. Are they converting but not staying? → No = **retention/product problem**
6. Everything above is fine but there still aren't enough customers? → **acquisition channel/volume problem**

Whatever the answer, that becomes the entire focus. Don't spread effort across all six because "more marketing is good" — a strong content calendar doesn't fix a broken offer.

For marketplaces specifically: diagnose **each side separately**. A tutoring platform with plenty of demand and zero teacher supply has a supply problem — running student-facing ads makes it worse, not better (frustrated visitors, no inventory to show them).

## Step 2b — Grade your own confidence

Label every claim in the diagnosis as one of: **fact** (you have evidence — real usage data, a support ticket pattern, a direct customer quote), **observation** (you saw a pattern but haven't tested it), **hypothesis** (plausible, unverified), or **assumption** (no evidence, could be wrong). A plan built on assumptions dressed up as facts fails silently — you won't know why until money's spent. When the diagnosis is mostly assumptions, the next action should be a cheap way to get evidence (five customer conversations, a landing page test), not a full campaign.

## Step 3 — Who actually decides, and where do they already look

Don't pick channels because they're popular (Instagram, TikTok, SEO). Answer concretely: *where does this specific buyer already make this specific decision?* A Syrian parent choosing a tutor asks other parents in a WhatsApp group — that beats any Instagram ad. A SaaS founder evaluating a dev tool reads a GitHub README and Hacker News — that beats a TikTok. Get this wrong and even perfect execution fails.

## Step 4 — Sequence for cold start, don't launch broad

A two-sided or network product with thin density everywhere is worse than thick density in one segment. Concentrate: one city, one subject, one platform, one ICP — until there's enough real proof (reviews, case studies, word of mouth) to expand. Expanding before density exists resets the "empty room" problem in a new place.

## Step 5 — Say it plainly, skip the AI-marketing clichés

Never use: "elevate," "unleash," "seamless," "game-changer," "revolutionize," "the Uber of X." These read as generic and foreign, and actively hurt trust with skeptical buyers (parents, small business owners, anyone spending real money). Specific, plain, locally-worded copy that names the actual objection ("no hidden fees," "verified before they ever appear in search") consistently outperforms polished generic copy.

## Step 6 — Every result becomes reusable knowledge

After any campaign or growth push, write down: what was tried, what happened, why (best guess), and whether to repeat/kill/iterate. Don't let a result evaporate into a one-off report. Next time this skill runs for the same business, that history is the starting context — check for it before re-deriving strategy from scratch.

**Where to keep it:** a `GROWTH.md` (or similar) at the root of the target project, updated after each real push — not a separate system, just a file living next to the code it's about. Keep it short: constraint diagnosed → what was tried → result → next constraint.

## Step 7 — Referral/growth loops need real infrastructure, not just an idea

If the growth plan depends on referrals, credits, or viral loops, that's a real feature (tracking, qualifying events, a reward-review flow) — build it in the target app the same way any other feature gets built (migration → service → routes → UI → tests), not as a separate marketing tool bolted on. See `ostazi.sy`'s `ReferralRedemption` model for a working reference: code assigned at signup, reward only granted after a real qualifying action (not just signup — prevents gaming), admin manually honors since most early-stage products don't have a wallet/payment system to automate the reward itself.

## Output format when applying this skill

For a business getting looked at for the first time, produce a single dense brief, not a stack of documents:

```
BUSINESS: <name, one-line model classification>
CONSTRAINT: <the #1 thing from Step 2, with the evidence for why>
WHO: <the buyer, where they actually decide>
SEQUENCE: <the one segment/city/channel to concentrate on first, and why>
NEXT ACTION: <the single highest-leverage thing to do next, concrete and dated>
```

Everything else (channel lists, content calendars, ad copy) is downstream of this and should only be built once the brief is confirmed. Don't generate 38 strategy documents for a business that hasn't shipped its first campaign yet — that's activity, not progress.

## Works with the other installed marketing skills — in this order

This skill is the diagnostic layer that decides *what* to do before anything downstream decides *how*. Don't skip straight to a tactical skill — run this first, then hand off:

1. **`growth-os`** (this skill) → produces the brief: constraint, buyer, sequence, next action.
2. **`market-research`** → when Step 2b evidence is thin (mostly assumptions), use this for sourced competitor/market/customer evidence with explicit fact/inference/recommendation separation — don't eyeball market size or competitive positioning.
3. **`content-marketer`** / **`email-marketing`** → once the brief is confirmed, use these for execution: content calendars, SEO pieces, email sequences, launch emails. They're tactical production tools, not strategy — feed them the brief, don't let them set the direction.
4. **`growth-engine`** → tactical reference only (AARRR framework, K-factor math, generic onboarding/launch sequence shapes). It's a downloaded template still describing an unrelated product (a Portuguese-language Alexa skill called "Auri") — reuse its *frameworks and formulas*, never its filled-in specifics, and always re-derive the actual numbers for whichever business is in front of you.

If a downstream skill's output contradicts the brief (e.g. content-marketer suggests a channel Step 3 already ruled out), the brief wins — go back and update Step 2/3 rather than silently overriding it.

## Applying this to our two businesses

**ostazi.sy** (marketplace, two-sided): constraint was cold-start liquidity. Applied brief lives in the published GTM strategy artifact from this session — Damascus-first, baccalaureate subjects, teacher supply before any student-facing spend, WhatsApp/personal-network outreach over ads. Referral system is now live infrastructure (`ReferralRedemption`, `/me/referral`, admin honor queue) — this is Step 7 in practice.

**Kyros** (AI video clipping SaaS, per `KYROS_ARCHITECTURE_AUDIT.md`): diagnosed 2026-08-09, full brief in `clip-platform/GROWTH.md` — read that file before doing any Kyros growth work, don't re-derive. Constraint: pre-launch/awareness, with a positioning risk underneath (reads as an Opus Clip clone unless the campaign/payout ledger and bilingual captioning are foregrounded). Sequence: clipping-agency operators (Whop-style campaign buyers) first, not individual creators — smaller, reachable, and the payout-ledger feature is a real wedge there that competitors don't have. Next action logged in that file: 5 real conversations with agency operators before any landing page gets built, since the "differentiator" claim is still an observation, not a validated fact. Known product-side caveat (not a marketing fix): scoring is English-only, so don't lead with "Arabic clipping" — caption rendering for Arabic/RTL works, clip selection quality for Arabic source video doesn't.
