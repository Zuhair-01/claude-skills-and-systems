# STYLE_DNA — how to write one

One document per creator, at
`Second_Brain/Workflow/30 - Resources/Style_Library/<creator-slug>/STYLE_DNA.md`.

This is not a form to fill in. It is what a good editor writes down after watching
someone's work for two hours — the thing they'd hand another editor who has to cut in
that style tomorrow morning and won't have time to watch anything.

**Write it in prose, in your own voice, as an editor.** Three movements, in this order:
what you saw, what's actually driving it, and how you'd rebuild it. Numbers appear
inside the prose as evidence for a sentence, never as a table you point at instead of
having a thought. The one place a table belongs is the small block of hard settings at
the end that `edl.py` and `render.py` actually read.

It works the same whether the creator is a talking-head coach, a faceless documentary
channel, a fashion vlogger, a product studio, or a comedian — the questions below are
about the craft, not about a format. Answer only what's true for this person; a section
that doesn't apply gets one honest line saying so, not a "N/A".

---

## Movement 1 — What you saw

Open with the sentence you'd say if someone asked "what's their thing?" and you had
five seconds. Not "fast cuts and bold captions" — that describes half the internet.
The real answer is usually about *tension*: how they create it, how long they hold it,
and what they make you wait for.

Then walk through the work the way you'd walk another editor through it:

**The opening.** This is where most of the style lives, so spend the most words here.
What is on screen at frame one, and what has already happened before it? Are they mid-sentence,
mid-motion, mid-argument? Does the first line make a promise, pick a fight, or state a
result? Quote three of their actual first lines verbatim — the pattern will be visible in
the wording itself, and that pattern is more reproducible than any cut count. Note the
race between spoken and written: which hits first, and by how long.

**The rhythm.** Describe how it moves. Metronomic, or bursts and holds? Where do the
holds fall — and this is the important one, because a hold is a decision. Somebody who
cuts every 1.2 seconds for forty seconds and then sits on a single shot for four is
telling you exactly what they think the point of the video is. Say what the cuts are
motivated by: the word, the beat, the gesture, the breath, or nothing (which is its own
style, and reads as impatience). Say how much dead air they tolerate — the jump-cut
policy is a personality trait, not a setting.

**The frame.** How they sit in it, how close, where the eyeline goes, whether the camera
is alive or locked. Is there a shot they use in almost every video? Most creators have
one, and it is usually the thing people picture when they think of them.

**The look.** Describe the grade the way a colourist would to another colourist: where
the blacks sit, what's happening in the skin, whether the highlights are protected or
blown on purpose, what's been done to saturation and where. Then say whether the b-roll
was graded to match or obviously wasn't. If they change the look between hook and body,
that's a deliberate move — name it.

**The text.** Not just the font. What is the text *doing*? Reinforcing the spoken word,
saying something different from it, or making a joke on top of it? When does emphasis
appear and what triggers it? Where does the text sit and does it move? Is the caption
carrying the video for a sound-off viewer, or is it decoration for someone already listening?

**The sound.** Music choice and how hard it works. Whether cuts land on the beat or
ignore it — both are valid, but they're different films. SFX density and what earns one.
Whether they use silence, which is the most under-used tool on the platform and an
immediate tell of a confident editor. How the voice is treated.

**The b-roll.** What triggers a cut away from the face, how long they stay away, and
whether the image illustrates the word literally or reaches for the feeling behind it.
The second one is much harder and much better, and it's usually what separates a creator
who looks expensive from one who looks stocky.

**The voice.** How they write, not just how they speak. Sentence lengths, register,
the rhetorical moves that repeat, the five phrases they genuinely reuse. Their speaking
rate and how it changes — most good ones speed up into the hook and slow down into the payoff.

**What they never do.** Half the style is refusal. List the things you noticed they will
not do, because those constraints are easier to follow than any positive instruction and
they're what keeps a clone from drifting back into generic.

## Movement 2 — Why it works

Now stop describing and think. Take the three or four choices that carry the most weight
and say what they're actually for. A pattern you can't explain, you'll misapply the moment
the material is different — and the user's material will always be different.

Separate two things carefully here:

- **What is theirs.** The choices that would still be recognisably them on any subject.
- **What is just the platform in 2026.** Loud captions, tight cuts, a hook in the first
  second. Check `_CRAFT_LAYER.md` before crediting anything to this person — most
  "signature" traits turn out to be the medium, and cloning the medium is worthless.

Then the honest part: what of this depends on something we don't have? A face people
already trust, a studio, a location, a voice, a three-year archive, a niche where the
audience arrives pre-sold. Name it. A style built on a thing we can't reproduce needs a
different plan, not a weaker imitation, and saying so early is worth more than any
amount of matching.

## Movement 3 — How I'd cut it

Write the build order the way you'd talk a competent editor through it — first this,
then this, watch out for that. Concrete about parameters where a parameter is the honest
answer, and concrete about judgment where judgment is. Reference our scripts by name
where they do the work. Someone should be able to follow it cold, on a video about a
completely different subject, and land in the neighbourhood.

Include what you'd check before calling it done — the specific things that would make
*this* style feel wrong if they slipped, which is different for every creator. For one
it's caption timing; for another it's that the grade drifted warm; for another it's that
the piece got too polite and lost the edge.

## The settings block

At the bottom, the small mechanical part — the numbers the pipeline reads, in
`dna.json` beside this file:

```json
{"asl": 1.6, "max_gap": 0.28, "pad": 0.10,
 "caption_max_words": 3, "caption_max_chars": 22,
 "broll_share": 0.30, "broll_len": 1.6, "cuts_first_3s": 2, "lufs": -14.0,
 "caption_style": {"font": "…", "size_pct": 5.2, "primary": "&H00FFFFFF",
                   "highlight": "&H0000E5FF", "uppercase": true, "margin_v_pct": 22,
                   "karaoke": true}}
```

These are a starting position, not the style. They get you into the right room; the
prose above is what makes it the right room.

## Front matter

```yaml
---
creator: <@handle>
platform: <where their work lives>
slug: <creator-slug>
corpus: <n> videos, pulled <YYYY-MM-DD>, <n> held out
niche: <what they actually make>
version: v1
status: draft | validated | production
confidence: what you'd stake, and where the corpus was too thin to say
---
```

## Two rules about writing it

**Cite as you go.** `(m: ASL 1.4s)` for something measured, `(v03 @0:04)` for something
seen. A claim with neither is a guess, and a guess in a template becomes a mistake in
every video built from it.

**Cut anything you're padding.** A short DNA that is entirely true beats a complete-looking
one with three paragraphs of hedging. If the corpus couldn't answer something, end with
the open questions and what you'd pull next time to answer them.
