---
name: shamcash-payments
description: Wire up ShamCash as a manual-payment method with admin reconciliation tracking on any project (student/customer pays a public ShamCash address manually, admin panel matches incoming transfers via shamcash-api.com's read-only API). Use when a project needs to accept ShamCash payments, or needs a "ShamCash Payments" admin tracking tab, or asks to reuse the Ostazi ShamCash integration pattern.
---

# ShamCash Payments (manual pay + reconciliation)

Reference implementation: `TutorLink-Syria` (ostazi-edu.com), commit
`d2da1a7` (2026-08-29). Read that repo's `apps/api/src/modules/payments/`
for working code before reinventing this.

## The fundamental constraint — read this first

**shamcash-api.com (and its sibling wrappers api-shamcash.com,
apisyria.com) are UNOFFICIAL third-party services, not a ShamCash
merchant API.** ShamCash itself has no public checkout/charge/webhook
endpoint. The wrapper only exposes three **read-only** endpoints against
one linked personal/business ShamCash account:

- `GET https://api.shamcash-api.com/v1/accounts`
- `GET https://api.shamcash-api.com/v1/balances`
- `GET https://api.shamcash-api.com/v1/transactions`

Getting a token requires linking a real ShamCash account via the
`@ShamCashAPI_AUTH_Bot` Telegram bot — treat that token as a live
financial credential (env var only, never commit, never log).

**Because there is no charge endpoint, "accepting ShamCash payments"
always means:** show the payer a public receive-address/QR → they pay
manually in their own ShamCash app, outside your app entirely → your
backend polls `/transactions` and matches incoming transfers to pending
orders/bookings by amount (+ a reference code in the note if your volume
needs it) → only THEN mark the order paid. There is no synchronous
"payment succeeded" callback. Set this expectation with whoever asked for
"ShamCash payment integration" before building — it is not a drop-in
Stripe-style checkout.

## Also flag before building, every time
- **No SLA / can vanish** — unofficial wrapper, subscription-gated,
  tokens expire and must be renewed manually on shamcash-api.com.
- **Sanctions-adjacent** — ShamCash is the vehicle Syria's transitional
  government uses to route public salaries outside the Central Bank of
  Syria / international banking rails. For a live paying business, that
  is a real compliance question depending on jurisdiction — surface it,
  don't silently build past it. See conversation precedent: this required
  an explicit, on-record override of a previously "architecture
  placeholder only, never integrated" locked decision.

## Build checklist (mirrors the Ostazi reference)

1. **Public receive-address**: not a secret — a wallet address/QR image
   shown to payers. Store as a plain (non-secret) env var, e.g.
   `SHAMCASH_ADDRESS`. Save the actual QR image asset into the frontend's
   public assets.
2. **API token**: `SHAMCASH_API_TOKEN`, secret env var, server-side only.
   Feature-gate on its presence (`isAvailable: () => Boolean(env.SHAMCASH_API_TOKEN)`)
   so it stays inert until configured, never a hard dependency.
3. **Reconciliation table**: one row per ShamCash transaction id (dedupe
   key = `shamCashTransactionId`, unique) with amount/currency/sender/
   note/occurredAt, nullable FK to whatever your "pending payment" row
   is. Never re-process a transaction id already seen.
4. **Match logic**: `GET /transactions` → for each unseen txn, find the
   oldest unpaid pending-payment row with the same amount+currency → link
   it → flip its status to a "confirmed by reconciliation" state. Known
   ceiling: amount-only matching collides if two payers send the exact
   same amount same day — upgrade to a per-order reference code in the
   ShamCash transfer note once volume makes that likely.
5. **CRITICAL — gate completion on confirmation, not on payment-method
   selection.** If your domain has a "mark as complete / settle" action
   that pays out a vendor/teacher/seller based on the order's payment
   method, it must check the reconciliation status is already confirmed
   before running — never let a ShamCash order auto-complete/auto-settle
   just because the customer *picked* ShamCash at checkout. (This exact
   bug existed in Ostazi's original scaffold — completion credited the
   teacher unconditionally regardless of whether money had actually
   arrived. Root-cause fix: gate in the one shared completion function,
   not in every caller.)
6. **Admin tracking tab**: list synced transactions (date/amount/sender/
   note/matched-or-not) + a manual "Sync now" button calling the same
   reconciliation function on demand (don't make admins wait for a cron).
7. **Payer-facing UI**: when ShamCash is the selected payment method,
   show the QR image + address + plain-language instructions ("pay this
   address manually, we confirm shortly after") — never claim "paid" at
   this point, only "awaiting confirmation".
8. **If the domain also pays a third party out** (e.g. a marketplace
   paying sellers/teachers): that payout address is a *different*,
   private field the seller/teacher enters themselves (their own
   ShamCash account) — never expose it to payers, who always pay the
   platform's own address. Don't conflate the two addresses.

## Testing
- Hit `/transactions` for real against a live token before trusting any
  of this — response shapes are informally documented at best.
- Confirm the dedupe key actually prevents double-processing (sync twice
  in a row, second run should show 0 new/0 matched).
- Verify the completion-gate (#5) with a test that tries to complete/
  settle before confirmation and expects a rejection.
