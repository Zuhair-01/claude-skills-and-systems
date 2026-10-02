---
name: autonomous-mode
description: >
  Hands-off working mode for when the user is asleep or away. On "turn on autonomous
  mode" / "autonomous mode on" / "I'm away, keep going" / "just do it bro", stop
  asking for confirmation: make every low/medium-risk call yourself (take the
  recommended option), work the current topic's backlog item-by-item in a loop
  until that topic is genuinely exhausted, build AROUND anything that truly needs
  the user instead of stopping, and hold a decision ledger + a NEEDS-YOU list for a
  single review when he's back. Turns off only on "autonomous mode off" / "I'm
  back" / an explicit stop.
---

# Autonomous Mode

the user switches this on when he's leaving (sleep, errand, day away) and wants work
to continue without him babysitting each step. The deal he's making: **you make
the decisions, you don't stop to ask "confirm this?", you don't settle for sloppy
work, and you hand him one clean review when he's back.** This layers on top of
CLAUDE.md — every rule there (handoff protocol, security gates, skill routing,
no-Agent, git discipline) still applies in full.

## 1. Turning it on

Triggers: "turn on autonomous mode", "autonomous mode on", "ox autonomous",
"I'm away / asleep / gone, keep going", "just do it bro", "don't ask me, just do it".

On activation, do this once:

1. **Fix the topic.** Write down, in one sentence, the goal in play right now
   (the project + objective of this session). This is the fence. Everything you
   do until shutoff must advance this goal, its sub-tasks, or adjacent cleanup
   that directly serves it. Starting an unrelated project, a different repo, or a
   new idea is out of bounds — when the topic is done, you STOP, you don't go
   find new territory.
2. **Build the backlog.** Gather every undone item for that topic: tracker/phase
   docs, TODOs the user gave, `git status`, failing tests, obvious gaps, review
   notes. Order it (blockers and foundations first). This is your queue.
3. **Open the session log** (see §5) in the vault and write the topic + backlog +
   activation time.
4. **Wrap yourself in `/loop` at a 4-minute interval** (the user's standing
   cadence — `/loop 4m <prompt>`, not self-paced, not 20m). The prompt points
   back to the session log so context resets resume cleanly. Each wake: work the
   next backlog item; if the backlog is momentarily empty but the topic isn't
   exhausted, do a quick re-scan (git status, tracker, peer messages) and pick up
   anything new. Only stop the loop on a §6 condition. If `/loop` is already
   active, proceed.
5. Confirm in one line what the topic is and that you're starting — then go. No
   further check-ins until a stop condition (§6) or he's back.

## 1b. Current session only

Autonomous mode applies to **this session only**. Do not broadcast it, do not
`SendMessage` other sessions to activate it, do not try to coordinate a crew.
If the user wants another session autonomous, he'll tell that session himself.
(Normal CLAUDE.md Rule 4 shared-tree git discipline still applies if a peer
happens to be live — that's unchanged.)

## 1c. Browser actions — act as the user, don't wait for him to click

While autonomous mode is active, the general rule that "the user drives
AI-gen tools / clicks buttons" is suspended for LOW/MED-tier actions —
that rule exists to keep a human in the loop turn-by-turn, which is exactly
what autonomous mode is switching off. Use `claude-in-chrome` directly to
navigate, click, type, and submit whatever a task needs (site UIs, web
tools, forms) as if you were the user at the keyboard, same risk gate as
everything else: LOW/MED → just do it, log MED calls to the ledger; HIGH
tier (a real purchase, sending something to a third party, an irreversible
submit, entering credentials) → stop, prep everything up to that point, add
it to NEEDS-YOU instead of clicking through it. This exception is scoped to
this session while autonomous mode is on — outside autonomous mode, the
normal user-drives rule is back in force.

## 2. The risk gate — how you decide alone

Every action gets a tier. Score it fast, in your head.

| Tier | What it is | What you do |
|---|---|---|
| **LOW** | Fully reversible, no spend, no external send, no prod/schema/DNS change, no security or legal surface. Code edits, tests, docs, local builds, drafts, refactors behind version control, research, file organization. | **Just do it.** Take the recommended option. No log entry needed beyond the normal work trail. |
| **MED** | Reversible but broader blast radius: new dependency, non-trivial refactor, a non-prod/preview deploy, content drafts that will be published later, config changes, a design direction pick, choosing between reasonable engineering options. | **Take the recommended option and do it** — but write the decision + the alternatives + your reasoning to the decision ledger (§5) so the user can veto it at review. |
| **HIGH** | Irreversible or outward-facing or costly: real money spent, anything sent to a third party (email, publish, post, API write to prod), prod deploy, `git push --force`, destructive ops (drop/delete/overwrite without backup), credential/secret changes, legal/compliance text going live, schema migrations on prod data, anything a security gate would block. | **Do NOT do it.** Do everything *around* it: build it, stage it, write the migration file, draft the email, prepare the PR — right up to the point of the irreversible step. Add a precise entry to the NEEDS-YOU list (§5) with exactly what's prepared and what one action he needs to take. Then move to the next backlog item. |

When you genuinely can't tell LOW from MED, treat it as MED (log it). When you
can't tell MED from HIGH, treat it as HIGH (don't do it, prep around it). The
ledger is cheap; an unwanted irreversible action is not.

**"Take the recommended option" when nothing obviously recommends itself:** pick
the simplest choice that's easiest to reverse, do it, and log it as a MED
decision with the alternatives — don't stall hunting for a perfect answer.

For a MED call that's close to the line or unusually consequential, run the
`council` skill's fast panel first and record the verdict in the ledger — but
still don't stall: decide and move.

## 3. The loop

Per backlog item, no pause between iterations:

1. Pick the next undone item (blockers/foundations first).
2. **Route it** — skill-router classify + score, cross-check OVERSEER
   (`python ~/.claude/overseer/search.py <terms>`), pick the best-fit skill
   stack. Autonomy means not stalling *after* routing, never skipping it.
   Frontend visual work still goes through `open-pinterest` first (Rule 7).
3. Build it. Match codebase conventions, surgical diffs (ponytail is active).
4. **Verify for real** — run the lint/typecheck/tests/build that actually prove
   it, or a live check appropriate to the change. Same bar as if the user were
   watching every keystroke. This is the trade for not asking permission.
5. **Record state durably** — update the tracker doc, commit (stage only files
   you touched, by name; `git status` first if a peer session might be live).
   Follow repo push rules: `alwazour-studio` auto-pushes each fix; Ostazi prod
   never auto-pushes; default is commit locally, don't push, unless the repo's
   memory says otherwise.
6. If you found new work while doing this item (a bug, a sibling that needs the
   same fix, a missing test), add it to the backlog — if it's on-topic.
7. Go to step 1. Do not write "let me know if you want me to continue."

If one item is blocked (HIGH tier, or missing credentials/data), that blocks
**that item only** — log it to NEEDS-YOU, then scan the rest of the backlog for
anything still doable and keep working. Only stop the run when *every* remaining
item is blocked.

## 4. The topic fence — staying on your own ground

Allowed without asking: the stated goal, its sub-tasks, tests/docs/CI for it,
bugs discovered in its code, adjacent cleanup that directly serves it, polishing
work already in progress (`project-shipready` pass when a build goes green).

Not allowed: a different project or repo, a new product/feature idea the user
hasn't asked for, speculative building "while I'm here", scope the user explicitly
deferred. If you think of these, write them to a "SUGGESTIONS FOR LATER" section
of the session log and keep moving.

When the backlog is genuinely empty and nothing on-topic remains: write the final
review (§7), note the run is complete and idle, and STOP. Waiting is the correct
behavior — don't manufacture work to stay busy.

**the user steering mid-run is not drift.** If he sends a new explicit task while
autonomous mode is on, that task extends or replaces the fence — do it, update
the session log's topic line, carry on. The fence only stops *you* from wandering;
it never stops him from redirecting.

## 5. State you keep (all in the vault, never terse)

**Handoff Log** (`Second_Brain/Workflow/20 - Areas/Handoff Log.md`) — normal
Rule 2 cadence: an entry at each milestone, every ~20-30 min, and *immediately*
on any usage/rate-limit warning (that can cut you off mid-response). Mark
`active`. Every entry carries its own continue-prompt block.

**Autonomous Session Log** — new file per run at
`Second_Brain/Workflow/20 - Areas/Autonomous Session Log.md` (append if it
exists). Structure:

```
## [DATE TIME] — Autonomous run: <topic>
**Topic / fence:** <the one-sentence goal>
**Backlog at start:** <ordered list>
**Activated by:** <the user's words>

### Decision ledger (MED calls — the user can veto any at review)
- [TIME] <decision> | options considered: <a / b / c> | chose: <x> | why: <reason> | reversible via: <how>

### NEEDS YOU (HIGH tier — prepared, waiting on one action from the user)
- <what's built and staged> → <the single action he must take (deploy / send / pay / approve / provide X)> | files: <paths>

### Done this run
- <item> — <what changed> — verified by <test/build/check> — commit <hash>

### Suggestions for later (off-topic, not acted on)
- <idea>

### Status: RUNNING | IDLE (backlog exhausted) | STOPPED (<reason>)
```

Update the ledger / NEEDS-YOU / Done lists as you go, not just at the end.

## 6. Stop conditions

- **the user returns** ("I'm back", "autonomous mode off", "stop") → go to §7.
- **Backlog exhausted**, nothing on-topic left → final review, set IDLE, stop.
- **Everything remaining is blocked** on HIGH-tier / credentials / missing data →
  final review listing every blocker, stop.
- **Usage/rate-limit warning** → write the Handoff Log entry *first* (with
  continue-prompt), finish the current atomic step cleanly, then stop.
- **A real blocker that changes the plan** (a failing test that's a genuine bug
  you can't fix on-topic, a conflict, information that invalidates the backlog) →
  log it, stop, surface it.

Never stop just because an item hit a natural checkpoint. Never push an
irreversible action through to avoid stopping.

## 7. The review when he's back

Present in the chat, and make sure the session log mirrors it:

1. **Topic + how far it got** — backlog at start vs. what's done vs. what's left.
2. **Everything done** — grouped, each with how it was verified and the commit.
3. **Decision ledger** — every MED call and why. Ask him to veto any; reverse
   the ones he rejects.
4. **NEEDS YOU** — the HIGH-tier list, each with the one action required. Walk
   through them together.
5. **Uncertainties** — anything you're not fully confident in, flagged honestly.
6. **Suggestions for later** — the off-topic ideas, for him to accept or drop.

Then do the changes that come out of the review. Autonomous mode stays off until
he switches it on again.

## Rules

- Take the recommended option on LOW/MED. Never ask "confirm this?" for them.
- Never take a HIGH-tier action. Prepare around it, list it, move on.
- Stay inside the topic fence. Exhausted topic = stop, not explore.
- Verify every item for real before marking it done — no exceptions for speed.
- Shared-state records (Handoff Log, session log, ledger) are always full detail,
  never terse, even with ponytail/ox active.
- One review, not a stream of updates. He reviews once, when he's back.
