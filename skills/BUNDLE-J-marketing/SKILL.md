---
name: bundle-j-marketing
description: Marketing, paid advertising, growth and the books canon — the auto-router for anything PPC, media buying, advertising or marketing. Covers paid ads on every platform (Google Ads / AI Max / PMax, Meta, Instagram, TikTok, YouTube, LinkedIn, X, Snapchat, Pinterest, Reddit, Amazon, Microsoft/Bing, WhatsApp & messaging, programmatic / CTV / audio / DOOH), ROAS, CPA, CPM, CTR, CPC, bidding, budgets, targeting, audiences, ad creative, copy, hooks, tracking, attribution, Consent Mode, incrementality, CRO, SEO/GEO/AEO, content, email/lifecycle, pricing, offers, positioning, funnels, sales outreach, social, analytics, Shopify and WooCommerce — AND every "which book / which framework / what does the research actually say" question (Hopkins, Ogilvy, Caples, Halbert, Sugarman, Schwartz, Cialdini, Kahneman, Ariely, Hormozi, Brunson, Ries, Trout, Aaker, Sharp, Moore, Thiel, Rackham, Voss, Gerber, Wickman, Michalowicz, Collins, Goldratt, Zinsser, McKee, Taleb, Naval, Aristotle, Cicero, Carnegie). Routes to two vault packs — Paid Marketing 2026 (22 files, 1,316 categories + 1,205 field tactics) and Books Canon 2026 (17 files, 361 works distilled, 948 frameworks extracted / 287 consolidated).
user-invocable: false
---

# BUNDLE J: Marketing, Paid Ads & Growth

**Orchestrates:** paid media across every ad platform (Google, Meta, Instagram, TikTok, YouTube,
LinkedIn, X, Snapchat, Pinterest, Reddit, Amazon, Microsoft, WhatsApp/messaging, programmatic/CTV/audio/DOOH),
plus the cross-cutting systems (algorithms, measurement/attribution, creative, compliance) and
e-commerce platform mastery (Shopify, WooCommerce A-Z) — alongside the existing marketing skills
(SEO/GEO, content, email/lifecycle, CRO, pricing, social, analytics, growth).

**Rebuilt 2026-09-16 by `opencode`** from a 21-agent research program: **1,316 categories + 1,205 field
tactics = 2,521 researched items**. This bundle is a *router*, not a duplicate — the depth lives in the
vault pack below (`Paid_Marketing_2026`), which is the single source of truth shared by Claude, Codex
and OpenCode. It deliberately does **not** overwrite the existing `ads` skill (Claude-owned canonical
content, `.claude/skills-library/ads`) — it sits beside it and supersedes it on breadth.

---

## Quick Start

**I want to:**
- **Run / fix / scale paid ads on any platform** → that platform's playbook in the vault pack (§B), then
  the skill `ads` for the general framework
- **Ask "which book / which framework / what does the research say?"** → §B2 (Books Canon). Start at its
  `00_MASTER_INDEX.md`; for a live problem go straight to `16_Reading_Paths_And_Application.md`;
  for a named framework go to `15_Frameworks_Compendium.md`
- **Know *why* an ad platform is behaving the way it is** → `15_Ad_Algorithms_Auction_Mechanics_A-Z.md`
  (read this before touching bids or audiences — 2026 platforms are retrieval systems, not audience filters)
- **Make ad creative / hooks / copy** → `17_Paid_Creative_Copy_A-Z.md` + skill `ad-creative`
- **Set up or debug tracking / attribution** → `16_Measurement_Attribution_Tracking_A-Z.md` + skill `analytics`
- **Check an ad is legal / policy-safe** (GDPR, special ad categories, regulated verticals) →
  `18_Ads_Compliance_Privacy_Policy_A-Z.md`
- **Run a Shopify store** → `19_Shopify_A-Z.md`
- **Run a WooCommerce store** → `20_WooCommerce_A-Z.md`
- **Run accounts for clients / scale an agency** → `21_Ads_Ops_Scaling_Agency_SOPs_A-Z.md`
- **Get more organic search / AI-search visibility** → skill `seo` / `seo-audit` + vault
  `Upgrade_2026_09\20_SEO_GEO_AEO_2026.md`
- **Build content / social plan** → skill `content-strategy` / `social` / `social-growth-science`
- **Write landing page or ad copy** → skill `copywriting` + `17_Paid_Creative_Copy`
- **Improve conversion post-click** → skill `cro` / `signup` / `onboarding` / `ab-testing`
- **Email / lifecycle / WhatsApp automation** → skill `email-marketing` / `email-sequence` +
  vault `Upgrade_2026_09\21_Lifecycle_Email_WhatsApp_2026.md`
- **Set pricing / offers** → skill `pricing-strategy` + vault `19_Pricing_Offer_Strategy_2026.md`
- **Choose a growth strategy / find the constraint** → skill `growth-os` (diagnose first) → `growth-engine`
- **Outbound / cold email / lead gen** → skill `cold-email` / `lead-intelligence` / `sales-automator`
- **Video ad production** → BUNDLE-F-video-media (`video-editing`, `remotion-video-creation`,
  `ugc-ads-workflow`, `seedance-*`, `heygen-*`)
- **Design a landing page UI** → BUNDLE-B-frontend-ui
- **Payments / subscriptions / checkout** → BUNDLE-K-commerce (`stripe-integration`, `payment-integration`)

---

## A. Marketing Skills (the live router)

### Primary — strategy & channels
- `ads` — general paid-media framework (platform selection, structure, copy frameworks, targeting,
  optimisation, retargeting, reporting). Claude-owned canonical skill; loaded via junction in OpenCode.
- `ad-creative` — bulk ad headline/description/creative generation and iteration (pairs with
  `17_Paid_Creative_Copy_A-Z.md`).
- `cro` — post-click conversion rate optimisation (the ad-to-landing-page gap).
- `analytics` — conversion-tracking setup and measurement planning (pairs with §B/16).
- `ab-testing` — experiment design, statistical validity, growth-experimentation programme.
- `copywriting` — landing page / homepage / ad copy.
- `content-strategy` — what content to make, topic clusters, editorial calendar.
- `social` + `social-growth-science` — platform-native social content and 2026 algorithm mechanics.
- `seo` + `seo-audit` — technical + on-page + AI-search (GEO/AEO) visibility.
- `email-marketing` + `email-sequence` — lifecycle, nurture, deliverability.
- `pricing-strategy` — pricing, packaging, monetisation.
- `growth-os` → `growth-engine` — diagnose the real growth constraint **before** picking channels.
- `marketing-psychology` — persuasion/behavioural science for any marketing artefact.
- `brand-voice` — source-derived writing-style profile for consistent messaging.
- `competitors` — comparison/alternative pages for SEO + sales enablement.
- `signup` + `onboarding` — registration flow and post-signup activation.
- `cold-email` + `lead-intelligence` + `sales-automator` — outbound prospecting and outreach.
- `community-marketing` — community-led growth.
- `landing-page-generator` / `web-prototype` — page build (see BUNDLE-B for full frontend routing).
- `trust-calibrator` — calibrating proof/credibility signals for sceptical audiences.

### Supporting (cost/product/legal)
- `free-tier-stack` — check for a free/open alternative before paying for any SaaS
- `public-apis-directory` — free data sources before building or buying
- `legal-advisor` — privacy policy, T&Cs, disclaimers
- `docx` / `pptx` / `pdf` / `xlsx` — deliverables (client decks, reports, audits)

---

## B. The Paid Marketing 2026 reference pack (the depth)

**Location (shared vault, all tools):**
`$SECOND_BRAIN\Workflow\30 - Resources\Research\Paid_Marketing_2026\`

**Start at `00_MASTER_INDEX.md`** — master comparison table, per-platform KPI/lever map, and
cross-references. Each numbered file has **40+ categories and 40+ numbered field tactics**, plus
benchmarks, checklists, decision trees, diagnostics tables and common-mistake lists.

| # | File | Covers | Cats | Tactics |
|---|------|--------|-----:|--------:|
| 00 | `00_MASTER_INDEX.md` | Index, comparison, KPI→lever map | — | — |
| 01 | `01_Google_Ads_A-Z.md` | Search, PMax, Demand Gen, Shopping, YouTube-in-Google, bids, feeds, conversions | 60 | 60 |
| 02 | `02_Meta_Ads_A-Z.md` | Advantage+, ASC, CAPI/AEM/EMQ, audiences, catalogs, lead ads, policy | 52 | 60 |
| 03 | `03_Instagram_Ads_A-Z.md` | Reels/Stories/Explore, partnership ads, IG Shop, native creative | 72 | 60 |
| 04 | `04_TikTok_Ads_A-Z.md` | Smart+, GMV Max, Spark Ads, TikTok Shop, Events API 2.0 | 78 | 60 |
| 05 | `05_YouTube_Ads_A-Z.md` | Skippable/bumper/Shorts, CTV, Demand Gen, brand lift, video creative | 85 | 52 |
| 06 | `06_LinkedIn_Ads_A-Z.md` | B2B targeting, Lead Gen Forms, Thought Leader Ads, ABM, CAPI | 70 | 60 |
| 07 | `07_X_Twitter_Ads_A-Z.md` | Objectives, formats, keyword/community targeting, brand-safety risk register | 67 | 50 |
| 08 | `08_Snapchat_Ads_A-Z.md` | AR Lenses, Story/Collection ads, pixel + CAPI, Gen Z playbook | 55 | 55 |
| 09 | `09_Pinterest_Ads_A-Z.md` | Visual search intent, Shopping/catalogs, seasonal calendar, Performance+ | 62 | 56 |
| 10 | `10_Reddit_Ads_A-Z.md` | Subreddit/interest targeting, native copy rules, LLM-citation angle | 62 | 58 |
| 11 | `11_Amazon_Ads_A-Z.md` | Sponsored Products/Brands/Display, DSP, ACOS/TACOS, keyword harvesting | 54 | 60 |
| 12 | `12_Microsoft_Ads_A-Z.md` | Bing/Copilot surfaces, LinkedIn profile targeting, Google import | 62 | 60 |
| 13 | `13_WhatsApp_Messaging_Ads_A-Z.md` | CTWA, templates, Flows, per-message pricing, MENA/Gulf playbook | 66 | 56 |
| 14 | `14_Programmatic_CTV_Audio_DOOH_A-Z.md` | DSPs, SPO, PMPs, CTV/OTT, podcast/audio, pDOOH, retail media | 72 | 56 |
| 15 | `15_Ad_Algorithms_Auction_Mechanics_A-Z.md` | **How every auction/retrieval/ranking system actually works** | 50 | 52 |
| 16 | `16_Measurement_Attribution_Tracking_A-Z.md` | GA4/GTM/sCAPI/Consent Mode v2, incrementality, MMM, clean rooms, blended CAC/MER | 65 | 55 |
| 17 | `17_Paid_Creative_Copy_A-Z.md` | Hook science, 36-pattern hooks swipe file, UGC, AI creative, testing matrix, fatigue | 60 | 55 |
| 18 | `18_Ads_Compliance_Privacy_Policy_A-Z.md` | GDPR/DMA/DSA/AI Act, special ad categories, regulated verticals, ban recovery | 55 | 58 |
| 19 | `19_Shopify_A-Z.md` | **Shopify end-to-end** — plans, Markets, checkout extensibility, apps, SEO, unit economics | 58 | 60 |
| 20 | `20_WooCommerce_A-Z.md` | **WooCommerce end-to-end** — HPOS, Blocks, WooPayments, hosting, plugins, TCO, scaling | 51 | 62 |
| 21 | `21_Ads_Ops_Scaling_Agency_SOPs_A-Z.md` | 100-pt audit, launch QA, scaling tree, reporting, 30/60/90 onboarding, incident runbook | 60 | 60 |
| | | **TOTAL** | **1316** | **1205** |

### Reading order for a cold operator
`15` (algorithms) → `17` (creative) → `16` (measurement) → target platform file → `18` (compliance) →
`21` (ops, if running accounts for others).

---

## B2. The Books Canon 2026 (the knowledge layer)

**Location (shared vault, all tools):**
`$SECOND_BRAIN\Workflow\30 - Resources\Curriculum\Books_Canon_2026\`

The marketing / advertising / copywriting / psychology / business / sales / growth / wealth /
rhetoric canon distilled into operator playbooks — not book reports. Each entry follows the
house format: **what it actually says → load-bearing ideas → named frameworks → what is dated →
where it lives in our skills → the gap it closes.**

**Entry point:** `00_MASTER_INDEX.md`. **Operating layer:** `16_Reading_Paths_And_Application.md`
(routes 50 live symptoms to one primary + one supporting book — use this when you have a *problem*,
not a curiosity). **Quick lookup:** `15_Frameworks_Compendium.md` (287 named frameworks A-Z with
origin + when-to-use + which skill).

| # | File | Covers | Works | Frameworks |
|---|------|--------|------:|-----------:|
| 00 | `00_MASTER_INDEX.md` | Index, bookmarks, five reading paths, re-read list | — | — |
| 01 | `01_Direct_Response_Advertising_Canon.md` | Hopkins, Caples, Ogilvy, Reeves, Collier, Halbert, Kennedy, Sugarman, Abraham | 26 | 52 |
| 02 | `02_Copywriting_Masters.md` | Sugarman's 31 triggers, Carlton, Makepeace, Whitman, Bly, Wiebe, conversion school | 24 | 64 |
| 03 | `03_Positioning_Strategy_Branding.md` | Ries/Trout, Aaker, Keller, Neumeier, **Sharp/Ehrenberg-Bass**, Porter, Blue Ocean, Dunford | 29 | 49 |
| 04 | `04_Persuasion_Psychology_Canon.md` | Cialdini, Kahneman, Ariely, Thaler, Fogg, Berger, Heath, Sutherland (ethics flags) | 27 | 80 |
| 05 | `05_Offers_Pricing_Monetization.md` | Hormozi, Ramanujam, Nagle, Baker, Poundstone, Enns + pricing worksheet | 23 | 54 |
| 06 | `06_Growth_Startups_Product.md` | Thiel, Ries, Moore, Ellis PMF, *Traction*'s 19 channels, Chen, Cagan | 24 | 62 |
| 07 | `07_Sales_Negotiation_Canon.md` | SPIN, Challenger, Gap Selling, Voss, Blount, Roberge + 12-touch sequence | 24 | 80 |
| 08 | `08_Business_Operations_Systems.md` | E-Myth, EOS, Profit First, Goldratt, Collins, Drucker + **one-person EOS** | 28 | 138 |
| 09 | `09_Funnels_DTC_Ecommerce_Canon.md` | Brunson, Deiss, RMBC, Todd Brown, DTC lifecycle (GDPR-aware) | 22 | 48 |
| 10 | `10_Paid_Ads_Platform_Books.md` | Marshall, Geddes, Loomer, Kusmich, Mandalia/BPM + "skip the UI walkthroughs" guide | 24 | 48 |
| 11 | `11_Content_Storytelling_Brand_Voice.md` | SB7, Made to Stick, Campbell, McKee, Zinsser, Pressfield + video-retention school | 30 | 62 |
| 12 | `12_Wealth_Entrepreneurship_Mindset.md` | Housel, DeMarco, Clear, Newport, Taleb, Naval, Attia, stoics + personal OS | 29 | 89 |
| 13 | `13_Behavioural_Economics_Marketing_Science.md` | Prospect theory, Prelec, **Binet & Field**, EBI — **with replication/confidence flags** | 27 | 60 |
| 14 | `14_Classical_Rhetoric_Influence_Lineage.md` | Aristotle, Cicero, Quintilian, Carnegie, Greene, Bernays, McLuhan + Arabic balagha | 24 | 62 |
| 15 | `15_Frameworks_Compendium.md` | **All named frameworks A-Z, consolidated** | — | **287** |
| 16 | `16_Reading_Paths_And_Application.md` | **Problem→book router (50), 5 curricula, extraction method, anti-library** | — | — |
| 17 | `17_Wider_Canon_By_Discipline.md` | 684 books / 38 disciplines with `[distilled]`/`[named]`/`[gap]` flags | 684 named | — |
| | **TOTAL** | | **361 deep** | **287 consolidated** |

**Rules for using it:**
- Read for a decision you are about to make — never for coverage. Unread canon is a cost, not an asset.
- File `13` is the honesty layer: it flags **retracted** (Wansink) and **dead** (ego-depletion) findings
  and gives every effect a confidence rating. Vet any claim there before it reaches a deck, an ad, or a price.
- Files `02`, `09`, `10`, `12` explicitly mark their **dated** tactics — do not ship those.
- Where the canon disagrees with itself (Sharp's empiricism vs Ries/Trout's differentiation imperative;
  Binet & Field's long-brand view vs the growth-hacking school), the files state the tension rather than
  picking a side. Hold both.
- **Do not duplicate** — the canon lives in the vault. Update the numbered file in place.

---

## C. Sub-bundles (delegate, don't duplicate)

- **Video ad production** → BUNDLE-F-video-media
- **Frontend / landing pages / UI** → BUNDLE-B-frontend-ui
- **Payments, subscriptions, checkout** → BUNDLE-K-commerce
- **Data stores, SQL, pipelines behind reporting** → BUNDLE-C-database-data
- **Analytics dashboards, data viz** → BUNDLE-N-analytics
- **Automation (n8n/Zapier) for campaign ops & reporting** → BUNDLE-L-automation
- **AI/LLM features inside marketing tools** → BUNDLE-D-ai-ml
- **Compliance/security deep dives** → BUNDLE-H-security

---

## D. Specialist agents available (invoke via the Task/Agent tool)

`paid-media-auditor` (200+ checkpoint ad-account audit) · `ppc-campaign-strategist` (large-scale
search/shopping/PMax architecture) · `paid-social-strategist` (Meta/TikTok/LinkedIn/Pinterest/X/Snap) ·
`tracking-measurement-specialist` (GTM, GA4, CAPI, server-side, attribution) ·
`seo-specialist` · `growth-hacker` · `trend-researcher` · `email-marketing-strategist` ·
`social-media-strategist` · `content-creator` · `paid-social-strategist` · `pricing-analyst` ·
`analytics-reporter` · `brand-guardian` · `ux-researcher`

---

## Usage Example

```
User: "My Meta campaigns are falling apart, CPA doubled last week"

1. Load BUNDLE-J-marketing
2. Diagnose cause first: 15_Ad_Algorithms (why delivery changed) → 02_Meta (diagnostics table)
3. Check the usual suspects: 16_Measurement (is the number even real? EMQ/CAPI health)
4. Fix creative if it's fatigue: 17_Paid_Creative_Copy (fatigue diagnostic + refresh cadence)
5. If structural: 21_Ads_Ops (scaling/plateau decision tree)
6. Verify compliance before relaunch: 18_Ads_Compliance
7. Optional: agent `paid-media-auditor` for an independent 200-point sweep
```

```
User: "Set up a Shopify store and run ads to it"

1. Load BUNDLE-J-marketing
2. Build the store: 19_Shopify (plans, app stack, fee/unit-economics math, launch checklist)
3. Tracking before spend: 16_Measurement (GA4 + Shopify + platform pixels/CAPI) + 18_Compliance (consent)
4. Creative: 17_Paid_Creative_Copy
5. Channel choice + build: 04_TikTok / 02_Meta / 01_Google / 09_Pinterest (per audience)
6. Scale + report: 21_Ads_Ops
```

---

## Maintenance note

Ad platforms ship changes weekly. This bundle and its pack are dated `2026-09`. When a platform
change materially alters an operator workflow, update the specific numbered file in the vault pack
(single source of truth) — **never fork the content into this SKILL.md**, and never edit Claude-owned
`.claude/skills-library/*` to mirror it. Log material revisions in `OpenCode Memory Log.md`.

`[opencode]`
