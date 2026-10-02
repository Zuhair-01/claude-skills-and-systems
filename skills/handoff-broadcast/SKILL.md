---
name: handoff-broadcast
description: Turns a Handoff Log entry into a live push, not just a file another account might read later. When you write an entry under the Multi-Account Handoff Protocol (CLAUDE.md Rule 2) and any peer Claude Code session is currently running, also SendMessage the full context to every live peer via ListAgents, with an explicit claim/dedup step so two sessions don't start the same work. Trigger on "handoff", "broadcast this", "let the other session(s) see it", "give it to the ai", "so it decides", a rate-limit warning, or any Rule 2 milestone moment where a peer session is live right now.
---

# Handoff Broadcast

The Handoff Log (`Second_Brain/Workflow/20 - Areas/Handoff Log.md`) is the durable record — it
survives a crash, a `/clear`, a new account switch next week. But it's pull-based: nobody sees a
new entry until they happen to read the log. When a peer session is live *right now*, that's slow
for no reason. This skill adds the push: the same handoff, delivered live via `SendMessage`,
on top of the file, not instead of it.

## When to use

- Any time CLAUDE.md's Multi-Account Handoff Protocol Rule 2 says to write a Handoff Log entry
  (milestone finished, ~20-30 min elapsed, rate-limit warning, explicit switch) **and** `ListAgents`
  shows at least one live peer session. The rate-limit case is the highest-value one — a session
  about to get cut off wants the other account picking this up now, not whenever it next opens the
  file.
- The user explicitly asks to hand off, broadcast, notify other sessions, or "let everyone see it."

Skip it when `ListAgents` shows no peers — write the file entry only, per Rule 2 as normal. A
broadcast to nobody is just a wasted tool call.

## Steps

1. **Write the Handoff Log entry first**, exactly per CLAUDE.md Rule 2's format (timestamp,
   project, delta since last entry, exact next step, blockers, files touched) and its continue-
   prompt requirement. The file stays the complete, durable record — the broadcast is a pointer
   into it, not a replacement for it.

2. **Discover live peers with `ListAgents`, every time.** Never hardcode session names — they
   change across restarts. If a session you'd expect (e.g. the "other account") isn't listed, it
   isn't running right now; that's fine, the file entry still covers it for later.

3. **Compose one self-contained broadcast message**, built from the entry you just wrote:
   - A pointer to the exact log entry (file path + entry title), so the peer can pull the full
     record if it wants more than the summary.
   - A condensed inline summary: what changed, what's verified (not just claimed), what's
     explicitly NOT done, and any concrete decision points the peer needs to weigh in on.
   - The **claim/dedup line** (see step 5) — this is what makes a live broadcast safe where the
     async file alone already relies on Rule 4 ("don't collide") holding by convention.
   - Keep it self-contained enough to act on without opening the file, but don't paste the whole
     entry — that's what the file is for.

4. **Filter to peers whose work could actually overlap, then send individually.** `ListAgents`
   rows don't carry a task description, so relevance has to come from what you already know about
   each peer this session:
   - A peer that has told you (via a prior `SendMessage`, a claim note it left in the log/Session
     Bus, or this session's own memory) it's working an **unrelated project/area** — different repo,
     different folder, no shared files with the entry you're broadcasting — gets **skipped**, not
     messaged. Don't rediscover this by asking; if you don't already know the peer is relevant,
     that itself is a reason to skip rather than default to sending.
   - A peer that has explicitly said "don't broadcast to me, I'm not involved" (see the standing-
     opt-out note below) is skipped unconditionally until it un-opts.
   - Everyone else — peers with unknown scope, or scope that plausibly touches the same
     project/files as the entry — still gets the message; the filter only removes *known*
     irrelevance, it never guesses relevance you don't have evidence for.
   `SendMessage`'s `to` is single-recipient, so loop across the surviving `ListAgents` rows (skip
   your own row; the tool already excludes it). Use one clear `summary` per send.
   - **Standing opt-out:** if a peer has told this session it isn't involved in this project/lane,
     remember that (session-local is enough — no file needed) and stop broadcasting to it for the
     rest of this session, across all future milestones, not just the one it flagged. Skip it
     silently rather than re-asking or re-notifying each time.

5. **Put the claim/dedup instruction directly in the message body**, not just in your own head:
   tell each recipient that if it decides to act, it should say so back (a short `SendMessage`
   reply naming which peer is taking it) or add a one-line "claimed by `<session>` at `<time>`"
   note to the Handoff Log entry *before* starting real work — whichever peer reacts first claims
   it, the other one stands down rather than duplicating. This operationalizes Rule 4 for the live
   case; the file-only version of Rule 4 assumes someone reads before starting, which a fast
   broadcast can race past if you skip this step.

6. **Optional: `notify_when_idle: true`** on the send if you specifically want to know when that
   peer finishes acting on the handoff (e.g. you're about to hit a limit and want confirmation the
   other account picked it up) — one-shot, no polling.

7. **Tell the user which sessions got the broadcast** (by name) after sending, same as reporting
   any other tool result — don't leave them to infer it happened.

## Why the claim step matters (the actual upgrade over an ad-hoc broadcast)

A broadcast without a claim step can cause the exact collision CLAUDE.md Rule 4 exists to prevent:
two sessions both read "here's an open decision," both decide to act, both start touching the same
files at once. The file-based protocol alone avoids this because reading is naturally staggered
(nobody's watching the file live). A live broadcast removes that natural staggering, so the claim
line has to do the job explicitly instead. This is the difference between "I sent a status update"
and "I handed off work safely" — always include it.

## Relationship to CLAUDE.md's Multi-Account Handoff Protocol

This skill doesn't replace any of Rules 1-9 — it's an addition to Rule 2's "write an entry"
behavior, active only at the moment a peer session happens to be live. Rules 1, 3, and 4 (read
first, reconstruct if stale, don't collide) still govern every session on the *receiving* end,
whether it got here via the broadcast or by reading the file cold later.
