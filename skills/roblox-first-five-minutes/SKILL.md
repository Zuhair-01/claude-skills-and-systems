---
name: roblox-first-five-minutes
description: Design and audit a Roblox game's first 5 minutes so new players don't leave, using real retention psychology (Self-Determination Theory, Flow, Fogg Behavior Model, first-session UX data) — not dark patterns. Use before shipping any Roblox game's onboarding, or when a game's D1 retention is low.
---

# Roblox: The First 5 Minutes

Most Roblox visitors decide whether to stay in under 30 seconds and whether to come back
tomorrow based on what happens in the first 5 minutes. This skill is the ethical, science-backed
version of "make them stay" — satisfying design that earns a return visit, not manipulation that
traps one. It explicitly does NOT cover: fake scarcity, guilt notifications, pay-gated basics,
or anything from `secure-by-default`'s banned dark-pattern list. See
`feedback_no_dark_patterns` reasoning already applied in the Gravebound plan (Section G).

## The science (cite this when a design choice is questioned)

**Self-Determination Theory (Deci & Ryan, 1985; validated extensively in game UX since)** — a
player stays intrinsically motivated when three needs are met:
- **Competence** — they feel effective, not helpless. First 60 seconds must guarantee a win.
- **Autonomy** — they feel their choices matter. Even a cosmetic choice (lantern color) works.
- **Relatedness** — they feel connected to others. A visible player count, a co-op prompt, a
  leaderboard — not required to progress, just present.

**Flow (Csikszentmihalyi, 1990)** — engagement peaks when challenge matches skill exactly: too
easy bores, too hard frustrates. A new player's first enemies must be trivially killable; the
challenge curve ramps only after competence is established (this is why Gravebound's Skeleton
has low HP/damage and the wave table starts at 0.5 spawns/sec).

**Fogg Behavior Model — B=MAT (Fogg, 2009)** — a Behavior happens when Motivation, Ability, and
a Trigger converge. A new player has uncertain motivation and low ability (doesn't know controls
yet) — so the *trigger* (the join button, the first objective) must require near-zero ability to
act on. This is why the join button is large, centered, and the only interactive thing visible
in the first screen — competing UI elements raise the ability bar and lose players.

**Operant conditioning / variable-ratio reinforcement (Skinner)** — unpredictable-but-fair
rewards are more engaging than fixed ones. This is real and powerful, which is exactly why it is
also the mechanism behind predatory gacha — the ethical line is whether the randomness affects
**cosmetic delight** (which enemy drops which particle color) vs **core progress or spend**
(never gate saved progress or a run's basic viability on RNG). Gravebound's upgrade offer (3
random passives) uses this ethically: the reward is a real, disclosed choice every time, never a
paywall.

**First-session drop-off data (industry-standard funnel, matches the game-factory spec's
onboarding phases):**
- Players who leave before 60s: the trigger-to-first-success loop was too slow or unclear.
- Players who leave at 2–5 min: the core loop's first reward wasn't compelling enough.
- Players who leave after 10–15 min but never return: no forward-momentum hook (an unlock
  preview, a daily reward) was shown before they left.

## The checklist (apply to every Roblox game this factory builds)

**0–15 seconds — Competence + Autonomy trigger:**
- [ ] Player spawns already able to see/do the core verb (no cutscene, no forced dialogue).
- [ ] Exactly one obvious interactive element on screen (Fogg: lowest possible ability bar).
- [ ] A single low-stakes personalization moment is visible or promised (autonomy).

**15–60 seconds — Guaranteed first competence:**
- [ ] First enemy/obstacle/challenge is unloseable. No failure state reachable this early.
- [ ] Immediate sensory feedback on the first success (particle, sound, number going up) —
  this is real "juice," not manipulation; see the VFXController/EnemyRenderController pattern.

**1–5 minutes — Core loop closes once, reward lands:**
- [ ] Player completes one full loop (Gravebound: reach first level-up) inside this window.
- [ ] The reward is disclosed and real (shown Embers/XP, not a vague "progress").
- [ ] A relatedness signal is visible (other players' presence, a co-op prompt) — never blocking.

**5–15 minutes — Forward-momentum hook before they can leave satisfied:**
- [ ] A next unlock is previewed ("Reach Level 5 to unlock the second hero") — creates an open
  loop (Zeigarnik effect: unfinished things are remembered better than finished ones).
- [ ] A natural, non-blocking favorite/return prompt appears after a genuine high point (a
  boss kill, a level-up), never immediately on join.

**Never (hard rule, same list `secure-by-default`/`security-audit` already enforce for this
project):** countdown-pressure timers, forced waiting/energy systems, progress loss on quit,
paywalled basics, fake near-misses, or any randomness that touches core progress or spend rather
than cosmetic flavor.

## Applying it — Gravebound audit (2026-09-18)

| Checklist item | Status | File |
|---|---|---|
| One obvious interactive element on join | ✅ | `HUDController.luau` — only the join button, no menu clutter |
| First enemy unloseable | ✅ | Skeleton: 20 HP, 5 dmg, 0.5 spawn rate at t=0 (`Gravebound.luau` wave table) |
| Immediate feedback on first hit/kill | ✅ | `VFXController` beam + `EnemyRenderController` hit-flash/death-burst |
| Full loop closes once (first level-up) in <5 min | ✅ | XP curve `5 + level*1.8`; first level-up lands well before minute 2 at current kill rate |
| Reward disclosed and real | ✅ | HP/XP/Embers bars broadcast at 5Hz, upgrade picker shows real named passives |
| Relatedness signal | ⚠️ gap | No visible player count / other-players-in-arena indicator yet — add a simple "N heroes in the graveyard" label |
| Forward-momentum hook (unlock preview) | ⚠️ gap | Hub exists but nothing tells a new player what's coming next — add a "Next unlock" teaser to the Hub button itself |
| Non-blocking favorite/return prompt | ❌ not built | No favorite prompt exists yet — add one firing once, after first level-up or first kill, never on join |
| No dark patterns | ✅ | Confirmed against Section G of the master plan; declined the "addicted players" ask on 2026-09-18 |

**Next concrete step:** close the two ⚠️ gaps and the ❌ (player-count label, next-unlock teaser
on the Hub button, a one-time post-first-kill favorite prompt) — small, additive, no architecture
change needed.
