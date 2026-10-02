---
name: user-media-moderation
description: Moderate user-uploaded images (and video frames) before they're stored or shown to other users — NSFW/nudity detection, circumvention-content detection (phone numbers, WhatsApp/social links, screenshots of chat apps, QR codes), and a time-limited-storage pattern (auto-delete after N days, download-before-delete). Use whenever a product accepts user-to-user image/video uploads and either legal-liability content or off-platform circumvention is a real risk.
---

# user-media-moderation — Screen user uploads, then age them out

**Type:** Backend / Trust & Safety
**Triggers:** "moderate uploads", "NSFW filter", "block nudity", "prevent circumvention via images", "auto-delete uploaded images", "image content moderation", "block WhatsApp screenshots/links in chat"
**Built from:** the Ostazi (`TutorLink-Syria`) chat-image feature, 2026-09-28 — a real
two-sided-marketplace messaging system that already text-scans for
disintermediation attempts (`detectCircumventionSignals` on message body text)
but had an image-upload path that bypassed that scan entirely, plus an
unbounded-growth storage bucket with no retention policy.

---

## When to reach for this

Any product where users exchange images/video with EACH OTHER (not just
uploading their own profile photo) and at least one of these is true:
- **Legal-liability risk:** nudity/CSAM/graphic content could get the platform
  sued, banned from an app store, or reported — marketplaces, tutoring/gig
  platforms, dating, social, anything with a messaging surface between
  strangers or near-strangers.
- **Disintermediation risk:** the business model depends on keeping
  transactions on-platform (a marketplace taking a cut, a booking platform,
  an agency) and users have an incentive to swap contact info to avoid fees —
  a phone number, WhatsApp link, or QR code sent AS AN IMAGE defeats a
  text-only keyword scan instantly.
- **Storage cost/liability creep:** user-uploaded media accumulates forever
  with no retention policy, becoming both a cost problem and a growing
  surface of stored content the platform is liable for.

**Not a fit:** a single admin/owner uploading their own content (a teacher's
profile photo, a product photo) — that's a normal file-upload validation
problem (`file-uploads` skill), not a moderation-between-strangers problem.
Also not a fit for read-only public content with its own existing moderation
(e.g. a CMS) — this is specifically for peer-to-peer upload paths.

## The real, verified stack (all free/self-hosted, no new cloud account needed)

Researched and confirmed current as of 2026-09-28 — don't re-litigate these
choices without a real reason, but do re-verify versions before installing,
libraries drift:

| Check | Library | Why this one | Real caveat |
|---|---|---|---|
| **NSFW/nudity** | `nsfwjs` (`infinitered/nsfwjs`) + `@tensorflow/tfjs-node` for server-side | Free, self-hosted, no per-call cost, ~90-93% accuracy depending on model size, 5-class output (`drawing`/`hentai`/`neutral`/`porn`/`sexy`) | It's a classifier, not a legal guarantee — false negatives/positives happen. Treat its `porn`/`hentai`/`sexy` score crossing a threshold (start ~0.6, tune from real flagged data) as "reject and log for human review," not as the only line of defense. A managed alternative exists if budget allows: **Azure AI Content Safety** (multi-severity, text+image) — costs money and needs an Azure account, so don't switch to it without the user's explicit go-ahead and a shown cost, same standing rule as any paid API. |
| **QR code / circumvention link in the image itself** | `jsqr` (pure JS decoder) fed raw pixel data via `sharp` | Free, no model download, catches "here's a QR code to my WhatsApp/Telegram" exactly | Only catches actual QR codes — doesn't catch a photographed phone number written in digits (that's the OCR check below) |
| **Text/phone-number/link inside the image** (a screenshot of a WhatsApp chat, a photo of a business card, a handwritten number) | `tesseract.js` (pure JS OCR) → feed the extracted text through **the exact same text-based circumvention detector the product already uses on message bodies** (don't build a second, divergent detector) | Reuses existing, already-tuned logic instead of duplicating it | OCR misses handwriting, stylized fonts, and Arabic-Indic digit variants (٠١٢٣٤ vs 01234) reliably less often than plain Latin digits — note this as a known gap, don't claim full coverage. OCR is also slow (seconds, not ms) — always run it async/queued, never block the upload response on it if avoidable (see fail-open vs fail-closed below). |

## Fail-closed vs fail-open — pick deliberately, don't default silently

- **Fail-closed (recommended for the NSFW + QR checks):** both are fast
  (sub-second), so reject the upload synchronously if either trips — the user
  gets an immediate "this image can't be sent" instead of it briefly existing
  anywhere.
- **OCR is the slow one.** Two real options: (a) still block synchronously and
  accept the latency (seconds) for a small image, simplest and safest; or
  (b) accept immediately, run OCR async, and retroactively pull the image +
  notify an admin if it trips after the fact — faster UX, but the image was
  briefly live. For anything with real legal exposure, prefer (a). Don't pick
  (b) without saying so explicitly — it's a real trade-off, not a default.

## The retention / auto-delete pattern

1. **No new "expires at" column needed if you already have `createdAt`** —
   compute the cutoff at sweep time (`createdAt < now() - retentionDays`)
   instead of storing a separate expiry timestamp per row. Simpler, one less
   thing to keep in sync.
2. **Reuse an existing scheduled-sweep endpoint if the product has one**
   (Ostazi already had `/system/cron/sweep`, a single Vercel Cron job that
   fans out to several independent sweep functions under one
   `CRON_SECRET`-gated route) — add one more sweep function to the list
   rather than provisioning a second cron schedule and a second secret.
3. **On sweep:** delete the object from storage, then null the URL field on
   the row (or the specific column holding it) — never delete the whole
   message/post/row just because its attached image expired, unless the row
   has no other content.
4. **Download-before-delete:** a real `<a href={url} download>` (or the
   platform's native-share/save equivalent) is the whole feature — don't
   build a separate "save" pipeline. If the UI wants to warn the user before
   expiry, that's a client-side countdown against `createdAt`, no new backend
   state required.
5. **Pick a retention window that's actually long enough to be useful**
   (days-to-weeks, not hours) — the point is controlling unbounded storage
   growth, not creating a race the user usually loses. Ask before assuming a
   number if the product owner hasn't given one.

## Standing rule this pairs with

If the product already scans message TEXT for a specific policy (circumvention,
profanity, PII, whatever) — the OCR path above must feed that exact same
detector, not a second one written from scratch. Two moderation systems for
"the same policy, different medium" drift apart over time and one of them
quietly rots.

## See also

- `secure-by-default` — the general build-time security gate this pairs with
  (fail-closed error paths, validate-at-boundary apply directly here)
- `security-audit` Phase 0 — run this on the finished feature before shipping
- `file-uploads` — general upload/storage patterns (S3/Supabase/etc.), this
  skill is the moderation layer on top, not a replacement for it
