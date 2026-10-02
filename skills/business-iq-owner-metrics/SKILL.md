---
name: business-iq-owner-metrics
description: >
  Owner-level financial fluency — the metrics a business owner (not a
  bookkeeper) uses to judge whether a company is actually healthy: unit
  economics (LTV, CAC, CAC payback, contribution margin), revenue quality
  (ARR, churn, net dollar retention, gross margin), and cash mechanics
  (cash conversion cycle, DSO/DPO, working capital, burn multiple,
  deferred-revenue float, cash vs accrual). Use whenever a task involves
  judging business health, building or reviewing a financial model /
  investor deck / KPI dashboard, setting pricing, sizing a raise or
  runway, evaluating a company to clone/acquire, or answering "how is
  this business doing / is this a good business". Source: IG reel
  "Business IQ (owner edition)" by bryson.bowman + standard definitions.
---

# Business IQ — Owner Edition

Distilled from the reel `source-reel.mp4` (bryson.bowman, "Business IQ –
owner edition", ~13k likes). The reel rattles off the terms an owner is
expected to know cold. This skill is the reference: what each means, the
formula, the healthy range, and the trap it exposes.

## How to use

- **Reviewing a model / deck / dashboard**: check every relevant metric
  below is present and internally consistent (e.g. LTV:CAC stated but CAC
  payback missing → flag it; ARR growth shown but NDR hidden → flag it).
- **"Is this a good business?"**: walk the three blocks in order — unit
  economics → revenue quality → cash mechanics. A business can pass one
  and fail another (great margins, dies on working capital).
- **Building something**: use the healthy ranges as defaults / targets,
  not the vibes.
- Always name the metric, give the number, give the benchmark, state the
  verdict. No hand-waving.

---

## Block 1 — Unit economics (does one customer make money?)

| Metric | Formula | Healthy | Trap it exposes |
|---|---|---|---|
| **CAC** (Customer Acquisition Cost) | total S&M spend ÷ new customers, same period | — | Loading only ad spend, ignoring salaries/tools/commissions understates it 2–3×. |
| **LTV** (Lifetime Value) | (ARPA × gross margin %) ÷ churn rate | — | Using revenue not gross-margin LTV inflates it. Long-dated LTV on a 2-yr-old company is a guess. |
| **LTV:CAC** | LTV ÷ CAC | **3:1+** (1:1 = you pay to lose money; >5:1 = underspending on growth) | High ratio can mean you're starving demand, not efficiency. |
| **CAC Payback** | CAC ÷ (ARPA × gross margin %) per month | **< 12 months** (< 6 elite; > 18 = cash-hungry) | LTV:CAC looks fine but you go broke waiting to recoup. This is the cash-timing check LTV:CAC hides. |
| **Contribution Margin** | revenue − all variable costs (COGS + payment fees + shipping + variable support) | positive, and rising with scale | Gross margin can look OK while per-order variable costs eat the unit. What's left to cover fixed costs + profit. |

## Block 2 — Revenue quality (how good is the revenue you have?)

| Metric | Formula | Healthy | Trap it exposes |
|---|---|---|---|
| **ARR / MRR** | recurring revenue × 12 (ARR) | — | Counting one-time / services / usage-spike revenue as "recurring". Only contractually recurring counts. |
| **Gross Margin** | (revenue − COGS) ÷ revenue | SaaS **75–85%+**; e-com 30–50%; services 40–60% | Leaving hosting, support, payment processing, or delivery out of COGS flatters it. |
| **Churn** (customer / revenue) | customers (or MRR) lost ÷ starting base, per month | logo < **2%/mo** SMB, < 1% mid-market; revenue churn lower still | Monthly looks tiny, annualizes brutally: 3%/mo ≈ 30%/yr gone. |
| **Net Dollar Retention (NDR)** | (starting MRR + expansion − contraction − churn) ÷ starting MRR, existing customers only | **> 100%** (110–120%+ elite) | < 100% means you grow only by outrunning a leaking bucket. The single best "is the product loved" number. |

## Block 3 — Cash mechanics (can it fund itself?)

| Metric | Formula | Healthy | Trap it exposes |
|---|---|---|---|
| **Working Capital** | current assets − current liabilities | positive, but see below | A pile of aged receivables counts as "assets" while cash is gone. |
| **Negative Working Capital** (as a *good* thing) | customers pay you before you pay suppliers | intentional in great retail/marketplace models (Amazon, Costco, insurance) | Growth *funds itself* — more sales = more free float. Opposite of a warning sign here. |
| **DSO** (Days Sales Outstanding) | (accounts receivable ÷ revenue) × days | as low as possible; < 45 for B2B | You booked the revenue but the cash is 60–90 days out. |
| **DPO** (Days Payable Outstanding) | (accounts payable ÷ COGS) × days | as high as suppliers tolerate | Paying suppliers faster than customers pay you = you're the bank. |
| **Cash Conversion Cycle (CCC)** | DSO + DIO (days inventory) − DPO | low or **negative** | Negative CCC = customers finance your operations. Positive & rising = growth eats cash. |
| **Deferred Revenue float** | cash collected for services not yet delivered (annual prepays) | large & growing = free working capital | It's a *liability* on the books but spendable cash in the bank — until you have to deliver. Over-reliance hides churn. |
| **Burn Multiple** | net cash burned ÷ net new ARR added | **< 1.5** good, < 1 great, > 2 bad, > 3 alarm | Revenue growing fast means nothing if you burn $3 to add $1 of ARR. The efficiency-of-growth number investors use now. |

## Cash vs Accrual (know which lens you're looking through)

- **Cash basis**: record revenue/expense when money moves. Simple, matches
  the bank balance, **hides** the shape of the business (a $120k annual
  prepay looks like a monster month then nothing).
- **Accrual basis**: record when *earned / incurred* regardless of cash.
  GAAP standard, shows true monthly economics, but the P&L can say
  "profit" while the account is empty (see: DSO, deferred revenue).
- **Owner move**: run the business on accrual for truth, watch cash
  separately for survival. Most founder blowups are accrual-profitable
  companies that ran out of cash.

---

## Quick verdict checklist

1. LTV:CAC ≥ 3 **and** CAC payback < 12 mo → unit economics work.
2. Gross margin in-band for the model **and** NDR > 100% → revenue is real.
3. Burn multiple < 1.5 **and** CCC low/negative **and** cash runway > 18 mo
   → it can fund its own growth.
4. Any block fails → that's the story. Say which one and by how much.
