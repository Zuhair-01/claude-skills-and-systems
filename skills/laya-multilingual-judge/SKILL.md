---
name: laya-multilingual-judge
description: Use the local Laya-multilingual classifier (convaiinnovations/laya-multilingual, mmBERT-based RLCD decision model) as a calibrated, de-biased judge/router for multilingual text — Kyros local-vs-escalate routing decisions, and rating/ranking ad copy or creative variants for Meta/Google/TikTok/Instagram/Facebook in Arabic or English. Trigger on "laya", "laya judge", "laya model", "escalate gate", "rate these ad variants", "which ad copy is better", "multilingual classifier", "score these captions/hooks", or any request to auto-pick the best of several text variants across languages. Do not use for generating copy (Laya cannot write text) or as a sole confidence gate (its raw confidence is documented as unreliable).
license: Personal use
metadata:
  owner: zoher
  status: weights-downloading
  model: convaiinnovations/laya-multilingual
---

# Laya Multilingual Judge

Wraps `convaiinnovations/laya-multilingual` — a 322M-param mmBERT encoder +
RLCD-trained decision head. It is **not generative**: it only answers typed
questions against a text (`choice` / `noul` / `score`), returning a
categorical answer with a confidence score in one forward pass.

## Known gaps (from the model card) and how this skill closes them

| Gap | Evidence | Fix this skill applies |
|---|---|---|
| Ships uncalibrated, overconfident | mean confidence 0.75–0.88 even when wrong; never drops below 0.885 on failures | `laya_judge.fit_temperature()` — per-(question_type, option_count) temperature scaling on a held-out labeled set before trusting any score |
| Position bias on `choice`/`score` | favors later-listed options | `laya_judge.predict_debiased()` — shuffles option order across N passes, majority vote, flags `position_consistent` |
| `noul` (boolean) under-reports true/yes | documented in model card | never trust a single `noul` call for a binary go/no-go; run it as a `choice` between exactly 2 named options instead, or corroborate with a second signal |
| Huge per-language variance | Arabic 0.400 @ 20-way intent, Swahili 0.210, Tamil 0.250, Amharic 0.110 | keep option sets small (2–4) for any language outside English; never trust 10+-way open-ended ranking directly — do pairwise/small-group comparisons and aggregate |
| Confidence can't be used to auto-gate | confidence stays high even on wrong answers | never build an "auto-trust if confidence > X" path; gate on `position_consistent` + calibrated score instead, and keep a human/second-model check on anything high-stakes |

If a specific language's accuracy proves too weak in real use (start
suspicious below ~40% on option sets you can verify by hand), the escalation
path is a LoRA fine-tune on our own labeled examples via
`hugging-face-model-trainer` or `unsloth-local-finetuning` — targeted at the
weak language/task pair, not a full retrain.

## Setup status

- `pip install laya huggingface_hub` — done
- Weights (`model.safetensors`, 644MB) — **COMPLETE and live** (blob 643,835,514 bytes, re-verified
  2026-09-25; two 0/67 MB `*.incomplete` stubs in blobs/ are harmless leftovers).
- **Eyes:** `laya_judge.describe_image()` / `judge_image()` — local `moondream` (Ollama) captions the
  image, Laya judges the caption. Laya never sees pixels; it cannot hear audio either.
- Harness: `~\Desktop\Empire_Base\laya-judge\laya_judge.py`
- Tokenizer-only pre-check (works today, no weights needed):
  `~\Desktop\Empire_Base\laya-judge\tokenize_demo.py`

## Workflow

1. **Pre-check the text.** Run `tokenize_demo.py "<text>"` on any brand name
   or key phrase before trusting it to the judge — if it shreds into garbage
   subword fragments, expect the judge to misread it too.
2. **Pick the right task type.** `noul` for yes/no (but corroborate — see
   table above), small `choice` (2–4 options) for categorical decisions,
   `score` only with position-swap de-biasing already wired in
   `predict_debiased()`.
3. **Never call the model directly for a real decision** — always go
   through `laya_judge.predict_debiased()` so position bias is handled, and
   through `fit_temperature()`/`apply_temperature()` before trusting the
   confidence number.
4. **Calibrate per use case before shipping it.** Log real (confidence,
   correct) pairs from a held-out labeled set for the specific
   (question_type, option_count) you're using, fit a temperature, apply it.
   Don't reuse a temperature fit for one task on a different one.
5. **Start with the Kyros escalate/no-escalate gate**, not open-ended
   Arabic ad-copy ranking — it matches Laya's actual RLCD training target
   (escalate-vs-answer with a cost penalty for wrong calls), so it's the
   highest-confidence starting point to validate the harness against real
   outcomes before extending to marketing judgment calls.
6. **Ad-copy/creative judging (secondary use)** — only after step 4's
   calibration, and only with small option sets (e.g. "which of these 3
   hooks is strongest" rather than ranking 10 at once). For Arabic, expect
   moderate-not-great accuracy (~40% at high option counts) — treat its
   verdict as one signal to combine with human review, not an autopilot.

## Example call shape

```python
from laya_judge import predict_debiased

result = predict_debiased(
    body="خصم 50% اليوم فقط على جميع المنتجات",
    question_name="which_hook",
    qspec={
        "type": "choice",
        "instructions": "Which hook is strongest for a Meta ad?",
        "criteria": {"hook_a": "urgency framing", "hook_b": "discount framing"},
    },
)
print(result["answer"], result["position_consistent"], result["vote_agreement"])
```

## Limitations

- Cannot generate or rewrite text — pair with `copywriting` /
  `marketing-psychology` for the variants themselves, this skill only judges.
- Do not treat any single raw prediction as ground truth — always run
  through the de-bias + calibration path, and keep human review on anything
  that affects real ad spend.
- Stop and ask before extending fine-tuning or wiring this into a
  production Kyros routing decision — that needs a labeled validation set
  first, not a one-shot integration.
