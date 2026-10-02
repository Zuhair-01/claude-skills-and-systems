---
name: free-tier-stack
description: Check for a free/open-source alternative before reaching for any paid SaaS, API, database, or hosting platform — and extend the vault's Free_Tier_Stack.md when a category isn't covered yet. Use before proposing a paid service on any project, when the user asks "is there a free option for X", "what's a free alternative to Y", or "add Z to the free stack", or when comparing infra choices (database, deploy platform, CDN, email, monitoring, CRM, billing, etc).
---

# Free-Tier Stack

Source of truth: `Second_Brain/Workflow/30 - Resources/Free_Tier_Stack.md`
— curated free/open-source picks per category, built from
github.com/ripienaar/free-for-dev plus dated research sweeps. This skill
is the habit of checking and growing that doc; the doc itself is the data.

Two narrower sibling skills already exist for their specific domains —
prefer them when the category fits:
- `free-oss-devops-stack` — dev-ops/automation SaaS (scraping, browser
  automation, workflow automation, monitoring)
- `oss-media-gen-stack` — AI media-gen (TTS/voice-clone, video-gen,
  avatar/lip-sync, bg-removal, upscaling, captions)

Use this skill for everything else the vault doc covers: databases,
deploy/hosting platforms, object storage/CDN, email sending, CI/CD,
search/data APIs, CRM/billing/support/accounting/HR/comms SaaS categories,
and any new category not yet in the doc.

## Protocol

1. **Read the vault doc first.** Check if the category (or the specific
   paid tool being considered) already has an entry. If yes, use the
   top-ranked pick unless its caveats rule it out for this project's
   specific need (read the caveat notes — several entries have one, e.g.
   Supabase's Nano-compute ceiling, Cohere's non-commercial-only free
   tier).
2. **If the category is missing or stale**, do a real research sweep
   (WebSearch, not memory — pricing/limits change) and produce ~5-10
   ranked alternatives the same way existing entries are structured:
   short line per pick, what makes it the free/OSS option, one concrete
   caveat if it has one (license restriction, non-commercial clause,
   rate limit, "needs its own re-plumbing"). Note self-hosted vs
   free-tier-hosted for each.
3. **Write findings back into the vault doc** in the matching section
   (or a new `###` section following the doc's existing pattern) — don't
   leave research only in chat. Fold into the existing doc rather than
   creating a new standalone file; this doc is the single source of
   truth on purpose so it doesn't drift into duplicates.
4. **Mark what's actually wired in vs just catalogued.** The doc
   distinguishes "made switch-ready" (installed/configured, ready to
   flip a project onto it) from a plain catalogue entry — don't blur the
   two. Only mark something switch-ready after actually installing/
   configuring/verifying it, not just finding it exists.
5. **Cross-check `Open_Source_Self_Host_Stack.md`** (same vault folder)
   before recommending a hosted-free-tier option when a self-hosted
   equivalent is already running in `Empire_Base/selfhost/docker-compose.yml`
   — several categories already have a self-hosted fallback wired in
   there (SearXNG, Firecrawl, PocketBase, Nextcloud, etc).
6. **Update the memory pointer** (`reference_db_deploy_alternatives.md`
   or a new topic-specific memory file, per the memory system's own
   rules) only when the finding is non-obvious enough to be worth
   recalling cold in a future session — not for every doc edit.

## When NOT to use
- The user names a specific paid tool with no interest in alternatives
  ("set up Stripe") — don't insert an unrequested free-alternative pitch.
- A dev-ops or media-gen category already covered by the two sibling
  skills above — route there instead, don't duplicate their lists here.
