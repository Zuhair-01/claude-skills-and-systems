# B-roll source registry — where professional footage actually comes from

Researched for `style-clone`. The rule: **never let a b-roll shot be decorative.**
A clip earns its place only if it makes the sentence under it land harder or faster.
Sourcing is the easy half; the fit is the whole job (see SKILL.md Phase 6).

## Tier 1 — free, API, use by default

| Source | Key | Quality | Best for | Notes |
|---|---|---|---|---|
| **Pexels Video** | free key, instant | High — real cinema-grade uploads | People, lifestyle, city, work/desk, nature, abstract | Best free API. `videos/search`, filter `size=large`, `orientation=portrait` for reels. CC0-ish Pexels licence, no attribution required |
| **Pixabay Video** | free key, instant | Mixed — some great, some 2015 stock-looking | Nature, tech loops, backgrounds, abstract | Second query when Pexels is thin. Always eyeball before use |
| **Openverse** | none | Images + audio ONLY | Stills for Ken-Burns b-roll | **Does not index video** — don't waste a call looking |
| **Internet Archive** | none | Archival / public domain | Retro, historical, news-era, NASA, film grain | `advancedsearch.php` + `mediatype:movies` + `licenseurl` filter. Mixed resolution, always check |
| **Wikimedia Commons** | none | Documentary | Real places, science, aircraft, animals | Keyless API, correctly licensed, attribution usually required (CC-BY) |
| **NASA Image & Video Library** | none | Broadcast | Space, earth, launch, science | `images-api.nasa.gov`, public domain |

**Get the two keys once (2 min, free, no card):**
- Pexels → https://www.pexels.com/api/ → put in env as `PEXELS_API_KEY`
- Pixabay → https://pixabay.com/api/docs/ → env `PIXABAY_API_KEY`

Without them `broll.py` still runs (Archive + Wikimedia + NASA), but the hit rate
for modern lifestyle/business footage drops hard. Get the keys.

## Tier 2 — free, no API (browse + download manually, or `/browse`)

Use when Tier 1 has nothing that fits and the shot matters. Pull manually,
then register into the library with `broll.py --register`.

- **Mixkit** (mixkit.co/free-stock-video) — curated, genuinely modern-looking, free licence
- **Coverr** (coverr.co) — the best free source for *background/hero* motion loops
- **Videvo** — huge, mixed licences (check per clip: some need attribution)
- **Mazwai** — small, cinematic, CC-BY; strong for moody/atmosphere
- **Dareful** — 4K, CC-BY, landscapes and city
- **Life of Vids** — free, no attribution, quirky/lifestyle
- **Pond5 Public Domain** — free PD section
- **Vimeo / YouTube CC-BY** — last resort. Legal only if the uploader really set
  CC-BY and you attribute. Verify the licence field, don't assume

## Tier 3 — paid, name them only when the piece justifies it

Not needed for organic social. Worth it for a paid ad or a client film:
- **Artgrid** — best-in-class, story-shot-based, per-year sub
- **Filmsupply** — real film-grade, expensive per clip
- **Storyblocks** — volume subscription, quality varies
- **Envato Elements** — footage + SFX + templates in one sub, good value if you also need motion templates

Per CLAUDE.md's free-first rule (`free-tier-stack`), never propose Tier 3 unless
Tier 1+2 have been actually tried for the specific shot and failed.

## Motion/graphics/SFX we already own locally — check BEFORE downloading anything

- `~/.claude/skills/video-shotcraft/assets/audio/` — 149 SFX + 5 BGM, free, on disk
- `Second_Brain/Workflow/30 - Resources/Free_Asset_Libraries/soundfx-rse/` — 67 more CC0/CC-BY SFX
- `Second_Brain/Workflow/30 - Resources/Free_Asset_Libraries/viewcci-sfx/` — the pack with a documented
  hook/reveal/transition/caption/whip-pan/CTA/glitch mapping (see memory `reference_viewcci_sfx_pack`)

## The local b-roll library (this is the part that compounds)

Everything `broll.py` downloads lands in one shared library, not per-project:

```
Second_Brain/Workflow/30 - Resources/Broll_Library/
  manifest.json          # every clip: tags, concept, duration, orientation, res, source, licence, sha1
  clips/<sha1>.mp4
```

Rules that keep it useful instead of a junk drawer:
1. **Concept tags, not filename nouns.** A clip of hands on a laptop is tagged
   `work, focus, typing, solo, desk, indoor, cool-grade` — because you'll search it
   later by what a *sentence* needs, not by what's literally in frame.
2. **Portrait/landscape recorded per clip.** A 16:9 clip in a 9:16 reel needs a
   punch-in or a blurred backplate; the library must tell you which it is up front.
3. **Never delete on project end.** The library is the asset; projects are temporary.
4. **Dedupe by sha1** — the same Pexels clip will surface across many searches.
5. **Licence recorded at download time**, never reconstructed later. CC-BY clips
   carry the attribution string in the manifest so the caption can credit correctly.

## Choosing the actual clip

The literal image is nearly always the wrong one. Someone says "money" and the obvious
move is cash on a table, which viewers have seen ten thousand times and skip past without
registering. The image that works is the one carrying the *consequence* of the sentence —
the empty till, the hand that stops short of the card reader, the phone face-down going
unanswered. Same words, suddenly something at stake. That's the whole difference between
b-roll that does work and b-roll that fills a gap.

Once you've got a candidate, the practical things that sink a shot: a colour temperature
that doesn't belong with the A-roll (grade it to match, always — `render.py` handles it,
and unmatched grade is the loudest tell that footage was bought); motion running the
opposite way across a cut, which reads as a mistake unless you land it on a hard beat and
own it; a recognisable stranger's face, which pulls attention away from the person actually
talking; and length — past two and a half seconds the viewer has forgotten who was
speaking, so a longer hold has to be earning something.

Last check is the style one: would this shot appear in the creator's own videos? Their
b-roll vocabulary is narrower than you'd think, and drifting outside it is how a clone
stops reading as a clone.
