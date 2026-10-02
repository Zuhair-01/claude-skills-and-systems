---
name: style-clone
description: "Clone a specific creator's editing and content style from their profile, then apply it to the user's own raw footage end to end. Pulls their recent videos, measures the mechanical fingerprint (cut rhythm, hook density, grade, loudness, speaking rate), watches the frames, writes a STYLE_DNA into a growing Style Library, tests it against held-out videos, then cuts the user's raw footage to match — jump cuts, punch-ins, b-roll sourced to fit the actual words, styled captions, grade, sound. Works for any creator, language, niche or format: talking-head, vlog, faceless, product, comedy. Use when: 'learn this guy's style', 'copy this editor', '@handle — analyze their editing', 'make my video look like theirs', 'apply <creator> style to this footage', 'find b-roll for this script', 'edit this raw video like <creator>', or any request to study a profile's content and reproduce how they work."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# style-clone

Watch a creator until you could cut like them with the lights off, write that down so it
survives the session, then actually cut the user's footage that way. Every creator you go
through leaves the next one easier, because what's genuinely universal gets moved out of
the individual templates and into one shared craft layer.

This is an editor's process with scripts underneath it, not a script with an editor
bolted on. The tools measure and execute; the judgment is yours and it is the part that
matters. Where this document gives you a number, it's because a number is the honest
answer. Where it doesn't, don't invent one — think.

**The library lives in the vault** (CLAUDE.md Rule 5), because it has to outlive this
session and be readable from either account:

```
Second_Brain/Workflow/30 - Resources/Style_Library/
  _INDEX.md              every template, one line each — read this first, always
  _CRAFT_LAYER.md        what turned out to be true across creators (the compounding part)
  <creator-slug>/
    STYLE_DNA.md         the written style (references/style_dna_template.md says how)
    dna.json             the handful of settings the scripts read
    metrics.json         measured evidence
    sheets/              contact sheets, one per video watched
    VALIDATION.md        what each round tested and what it found
Second_Brain/Workflow/30 - Resources/Broll_Library/   shared footage, grows forever
```

Corpus video files stay in the scratchpad. The vault holds knowledge, not gigabytes.

---

## Phase 0 — Orient

Read `_INDEX.md`. If this creator already has a template, load it and go straight to
Phase 6 — unless the user asked for another round, or the corpus is months old and the
creator has visibly moved on, which happens more than people expect.

Read `_CRAFT_LAYER.md` before forming any opinion. Its whole job is to stop you writing
down "bold captions, tight cuts" as if you'd discovered something personal about this
creator rather than described the platform.

Skim the vault's `Editing_Montage_Motion_Master_Reference.md` — §4–8 for grade, sound and
subtitle craft, §14 for how retention actually works in talking-head and ad footage. That
doc holds the craft; this skill applies it to one specific person.

Then get the profile, and the footage and script if they exist. Don't interview the user —
start.

## Phase 1 — Pull the corpus

```bash
S="$SCRATCH/style-clone/<creator-slug>"
python ~/.claude/skills/style-clone/scripts/pull.py "@handle" --out "$S" --n 12
```

Instagram profile pulls are unreliable in yt-dlp right now — its `instagram:user`
extractor is marked "CURRENTLY BROKEN" upstream (confirmed 2026-09-08, independent of
cookies or version). Don't burn time on `--cookies-from-browser`: go straight to browsing
the profile's reels tab yourself (`browse` per CLAUDE.md Rule 13), collect the individual
`/reel/...` URLs from the page (a JS query against `a[href*="/reel/"]`, dismiss the cookie
banner first), pair them with their view-count text for the hold-out split, then pass each
URL to `pull.py` as a repeated `--url` flag — yt-dlp downloads a single reel URL fine. If
the account requires login to see more than the first page of reels, that's a real ceiling,
not a bug — work with what's visible logged out. Don't analyse two videos and call it a
style — you'll be describing one video's mood and presenting it as a person.

Twelve is a comfortable read. Eight works with the thin spots flagged honestly. Below
five, say so up front and treat everything as provisional.

`corpus.json` is sorted by views, and the spread is informative: the outliers are where
the formula actually fired, the median is where they were on autopilot. Both are worth
watching, for different reasons.

**Hold two of the best performers and one weak one out of the analysis** and note their
ids in `VALIDATION.md` before you look at them. That's your test set later, and it only
works if you genuinely haven't studied them.

## Phase 2 — Measure

```bash
python ~/.claude/skills/style-clone/scripts/measure.py --dir "$S"
```

Per video and in aggregate: average shot length, cuts per minute, cuts inside the first
three seconds, share of shots under a second, integrated loudness and range, luma and
saturation, speaking rate where subtitles exist — plus a contact sheet per video, one
frame per shot, which is the thing you'll actually spend your time in.

Check the cut detection before you trust it. Count the cuts in one video's first ten
seconds by hand and compare. Hard-cutting high-motion work needs `--scene 0.35–0.40`;
soft, graded, slower work needs `0.20–0.25`. If you're off by much more than a fifth,
retune and re-run, because every rhythm claim downstream inherits this number.

And hold the numbers loosely. An average shot length of 1.4 seconds is a fact about
arithmetic. It tells you nothing about whether the cuts are landing on breaths or
running over them, and that difference is the entire style.

## Phase 3 — Watch

Read every contact sheet properly. Then go frame by frame through the first three
seconds of the three strongest performers, because that's where the density is —
whatever a creator believes about attention is written into their opening, and everything
after it is comparatively relaxed.

Watch for what you'd notice as an editor sitting in the room: where they cut and where
they refused to, what they let you see before they let you hear it, what they're
withholding, which shot they keep coming back to. Read their captions and descriptions
from `corpus.json` for the writing voice — the way someone writes is usually a cleaner
signal of their instincts than the way they cut, and it's the part that transfers to
the user's material most directly.

Write down one thing per video that surprised you. Those are almost always the real
findings; the rest is confirmation.

Never write a style claim from the metrics alone. The numbers give you the pulse. Only
the frames tell you what it's for.

## Phase 4 — Write it down

Follow `references/style_dna_template.md`: prose, three movements — what you saw, why it
works, how you'd cut it — with measured numbers cited inside the sentences that need
them, and a small settings block at the end that the scripts read.

The two sections that earn their keep later are the honest separation of *theirs* from
*the platform's*, and the build order someone could follow cold on a different subject.
Everything else is context for those two.

Save the settings as `dna.json` beside it. Mark the file `status: draft`.

## Phase 5 — Rounds

the user will ask for another round until he says stop. Each one has to find something the
last one couldn't, or it isn't a round — it's the same document with warmer adjectives.
Log what each round tested and what it changed in `VALIDATION.md`.

**First, does it hold?** Re-read what you wrote against all the sheets. Every "always"
and "never" has to survive contact with every video. What holds in most but not all
becomes "usually", with the exception named — and the exception is often more interesting
than the rule, because it shows you what makes them break their own pattern. Anything you
can't cite, cut.

**Then, does it predict?** This is the round that separates a template from a description.
Before measuring the held-out videos, write down what the DNA says they should be:
shot length, opening cut density, duration, loudness, speaking rate, hook device, whether
b-roll shows up early. Then measure them and compare. Where you missed, the template is
wrong — fix the template, not the prediction, and note what the miss taught you. A DNA
that has never been tested this way stays `draft`, no matter how good it reads.

**Then, does it survive contact with our own footage?** Cut twenty or thirty seconds of
the user's real material through Phase 6, measure the output, and put it next to the
creator's numbers. Then — and this matters more than the numbers — watch both at full
speed with sound. If ours matches on every measure and still feels like an imitation,
believe your eyes and go find out why. Usually it's timing inside the cut rather than
the cut count, or captions that are technically right and land a beat late.

**Later rounds go deeper, not louder.** Sound design density. B-roll semantics. The
rhetorical shapes in their writing. A wider corpus. A second apply-test on different
material. If a round has nothing new to test, say so and propose what would — that's a
more useful answer than another pass.

Mark `validated` once it predicts and survives an apply test. Then Phase 8.

## Phase 6 — Cut the user's footage

```bash
python .../transcribe.py raw.mp4 --model small        # use medium+ for Arabic
python .../edl.py --video raw.mp4 --transcript raw.transcript.json \
                  --dna "Style_Library/<slug>/dna.json"
```

That gives you a timeline with the dead air already gone, the beats where a visual change
has to happen to hit the target rhythm, caption chunks on real word timings, and empty
b-roll slots. It's an assistant's pass, not an edit. The edit is what you do to
`raw.edl.json` next.

**Start at the top, honestly.** Read the first block and ask whether it opens the way this
creator opens. If the strongest sentence in the take is ninety seconds in, move it to the
front — reordering the cuts is allowed and it is usually the single biggest improvement
available. A perfectly styled video that opens on throat-clearing is a wasted video, and
no amount of caption polish rescues it.

**Then the b-roll, which is where most clones go wrong.** For each slot, read the phrase
that will be on screen and decide what image would make that sentence hit harder. The
literal one almost never does. Someone says "I was losing money" — cash on a table is the
obvious answer and it's dead; an empty shop at midday, or a hand stopping short of a card
reader, is the same sentence with something at stake. `references/broll_sources.md` has
the sourcing:

```bash
python .../broll.py find "concept"                 # the local library first, always
python .../broll.py search "concept" --portrait    # then the free sources
python .../broll.py get "<url>" --concept "…" --tags "…" --license "…" --orientation portrait
```

Put the returned path in the slot and write one line saying why that shot earns its place.
If you can't write the line, delete the slot — a hole where b-roll was supposed to go is
invisible; a clip that doesn't mean anything is the thing that makes work look bought.

**When no sourced clip fits the concept** (a specific product, face, or action nothing
free/licensed shows), Hypit (`~/.claude/skills/.agents/skills/hypit`, installed +
HypiHub-connected, see [[project_hypit_viral_clone_tool]]) can generate that exact shot
instead of settling for a near-miss stock clip — still write the one-line justification,
and still prefer a real sourced clip when one actually fits.

**When the DNA calls for a self-built card instead of sourced footage** — a headline,
a stat, a CTA card, the pattern `_CRAFT_LAYER.md` flags as showing up across most
creators — build it, don't source it:

```bash
python .../graphics.py --title "Every *word* gets the accent treatment" \
                       --subtitle "optional smaller line" --out slot.png \
                       --bg '#0E1013' --accent '#E3A857'   # match the DNA's palette
```

Set that slot's `kind` to `"graphic"` (render.py then loops it as a still, not a video)
and `clip` to the PNG path. If the loaded DNA says the presenter stays visible under
graphics — check its PiP note before assuming either way — set `pip: true` too;
`render.py` composites the talking-head take as a small corner box on top of the card
automatically (`--pip-corner`, `--pip-width-pct` control it, default bottom-left/30%).
This covers static title/stat/CTA cards. It does **not** cover an animated diagram that
fills in as narrated (a line chart drawing itself, a bar building bar-by-bar) — that's
still the Phase 6b gap; building a static card as a stand-in for one of those is exactly
the kind of approximation Phase 6b exists to prevent, so leave the slot unfilled and flag
it rather than fake the motion.

Timing: the image arrives *on* the word, not ahead of it, and it leaves before the viewer
has finished reading it. Come back to a different framing than you left on, so the return
feels like a decision. And check the grade — stock footage cut against graded A-roll at
its native look is the most common tell there is, which is what `grade.broll_match` is for.

**Captions** get emphasis where the meaning turns — the number, the reversal, the payoff —
one per chunk at most. Emphasis on everything is emphasis on nothing.

**Sound** last: local SFX packs before anything downloaded, music bed via `--music`, and
the ducking is handled. If the creator uses silence, use silence — it's free and almost
nobody has the nerve. Check `30 - Resources/Editing_Toolkit_Reference.md` first for the
moment→SFX decision map and any brand's caption-style preset already written for
`render.py`'s `style` dict — don't re-derive an SFX choice or a caption colour scheme that's
already been decided there.

```bash
python .../render.py --edl raw.edl.json --out final.mp4 --punch --music bed.mp3
python .../measure.py --dir "$(dirname final.mp4)"
```

`--punch` turns the beats that didn't get b-roll into real angle changes, alternating a
gentle push-in. Skip it when the creator sits locked off; on them it would read as fidget.

## Phase 6b — When they do something you don't know how to do

This will happen on almost every serious creator, and it's the moment the whole thing
either gets better or turns into slop. You'll see a move — a speed ramp into the beat, a
masked transition where they walk through the cut, motion-tracked text stuck to a moving
object, a whip-pan match cut, a screen replacement, a hold-frame with the subject cut out
and pushed forward, a light-leak transition timed to a snare — and you won't have a
recipe for it.

**Do not approximate it, and do not quietly drop it.** An approximation of a signature
move is worse than not attempting it, because it reads as a failed attempt at exactly the
thing you were trying to clone. And "we skipped their best move" is not a clone.

Go and learn it properly, in this order:

**Watch it happen.** Find a real tutorial where someone performs the technique, not an
article describing it. `video-download` pulls it; `reel-intent-analyzer`'s frame-by-frame
approach reads it. Step through the frames on both the creator's version and the
tutorial's until you can say what happens on each frame — where the speed changes, what
the mask is following, how many frames the transition actually takes. Most of these moves
are three or four frames long and every guess about them is wrong.

For anything you need to look up on the web, use gstack `/browse` (CLAUDE.md Rule 13),
never the Chrome extension tools.

**Then check what we already have** before building anything: `python
~/.claude/overseer/search.py <technique>` across the off-context library, the vault's
editing master reference, and the shot-card gallery in `video-shotcraft` — 152 cards
covering most repeatable camera and transition moves, with source you can read rather
than reinvent.

**Then build it in isolation.** Not inside the user's video — in a throwaway test with
whatever footage is handy. Render it. Look at the actual frames. Iterate until it matches
the reference frame for frame, not "close enough". If it never gets there, you've learned
something real: say precisely what the gap is (a tool we don't have, a plate we can't
shoot, something that needs manual masking in a real NLE) and propose the honest
alternative rather than shipping the mushy version.

**Then keep it.** Write the working recipe to
`Style_Library/_TECHNIQUES/<technique>.md`: what the move is, what it's for, the exact
commands or filter graph that produced it, the frame counts, what made it fail on the way,
and a link to the test render. Next creator who uses it, you already know it. This is how
the pipeline gets a wider vocabulary instead of the same three moves forever — and it's
the list Phase 8 turns into the next script.

## Phase 7 — Judge it

Put the output's numbers next to the creator's and see where they diverge. Then close the
spreadsheet and watch the thing at full speed, with sound, once, without pausing — the way
somebody on a phone will. The measurements can tell you the rhythm is right; only that
watch tells you whether it's any good, and if the two disagree, the watch wins.

When something's off, name the specific thing and fix that. Re-rendering and hoping is how
an afternoon disappears.

Before it goes to the user, look for the tells that mark automated work, because they're
specific and they're always the same handful. Captions a frame or two behind the voice.
A b-roll clip that's obviously stock — a stranger's face, a different colour temperature,
a fake-looking office. Every cut the same length, so the piece drones. Text that says
exactly what the audio just said, adding nothing. A push-in that starts and stops for no
reason. An ending that just stops because the transcript ran out. Music at a constant
level under everything, including the moment that should have been silent. Any of those
present, it isn't done, whatever the numbers say — and none of them are hard to fix once
you've admitted they're there.

If the honest verdict is that the result is mediocre, say that to the user along with what
it would take to make it good, instead of handing over something dressed up as finished.

If it's Arabic, pull a frame and actually look at the burned captions — connected
letterforms, right-to-left order. Text pipelines fail at Arabic quietly and often
(see memory `reference_pdf_arabic_form_field_shaping_bug` for the same class of bug), and
it is not the kind of thing to assume worked.

## Phase 8 — Let it compound

Do this after every template, or the library is just a folder.

Compare the new DNA against the ones already there. Anything now showing up in three or
more creators isn't a signature, it's the medium — move it to `_CRAFT_LAYER.md` with the
count, and take it out of the individual templates. Good templates get *shorter* over
time, and what's left is the actual person.

Write down anything the style needed that our scripts couldn't do — speed ramps, masked
transitions, screen replacement, motion-tracked text. That running list is what the next
script gets built from, and it's more valuable than another template.

Update `_INDEX.md` with the slug, the one-line signature, the status and when to reach
for it. Write a Handoff Log entry when a template reaches `validated`, per Rule 2.

**And record the clock, because that's the only honest proof this is getting better.**
Every run gets a line in `_LEDGER.md`: which creator, roughly how long each phase took,
what you reused from the library, and what you had to work out from scratch. The first
time you learn a technique it might cost an hour; the second time it should cost minutes,
because the recipe is written down and the test render is sitting there to compare against.

If a second run *isn't* meaningfully faster, that's not bad luck — it means the write-up
failed. Something was recorded as prose when it needed to be a command, or the recipe left
out the one parameter that took forty minutes to find, or the technique file describes the
result instead of the steps. Go back and fix that file immediately, while you still
remember what you had to re-derive. That correction is worth more than the video you're
working on.

Same applies to whole templates. The first creator is slow — corpus, tuning the cut
detection, learning what to look at. By the third, Phases 0–4 should be substantially
quicker, because the craft layer already covers the platform norms and you're only hunting
for what's actually personal to them. If it isn't quicker, the craft layer is too thin or
too vague, and that's the thing to fix before starting another creator.

## Non-negotiables

Copy the grammar, never the assets — their rhythm, their hook shape, their grade
direction, their b-roll logic; not their footage, script, music or voice.

Every number in a DNA came from `measure.py` or from you counting. Nothing else.

A template that has never predicted a held-out video is a draft, whatever it reads like.

The library is the product. An edit that leaves nothing behind in `Style_Library/` or
`Broll_Library/` was half the job.

And when a style rests on something we don't have — a face people trust, a studio, a
location, years of audience — say it plainly and early, and plan around it. Quietly
shipping a thinner version of someone else's thing helps nobody.

## Files

`scripts/pull.py` corpus · `scripts/measure.py` fingerprint + contact sheets ·
`scripts/transcribe.py` word timings · `scripts/edl.py` timeline · `scripts/broll.py`
footage library · `scripts/graphics.py` title/CTA card renderer · `scripts/render.py`
final cut (jump cuts, punch-in, b-roll/graphic overlay, PiP compositing, captions, grade,
sound) · `references/style_dna_template.md` · `references/broll_sources.md`. Non-trivial
scripts carry `--selfcheck`; run it after edits — and for anything touching an ffmpeg
filter graph, that's necessary but not sufficient: render something real and look at the
output frames before trusting it (this pipeline has shipped two real filter-graph bugs
that only a selfcheck's assertions, with no actual render, would have missed).

## Neighbouring skills

One video, "what is this and what's it for" → `reel-intent-analyzer`. Writing the content
once the style exists → `content-factory`, `social-growth-science`. Cinematic product film
rather than a person talking → `video-shotcraft`. Sourcing a look for UI rather than video
→ `frontend-reference-sources`. Craft theory → the vault's editing master reference.
