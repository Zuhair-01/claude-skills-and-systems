# SKILL BUNDLES — Overseer-Indexed Auto-Select System
**Created:** 2026-08-10 | **System:** Overseer + Skill Router + Kyros | **Token Cost:** ~2 tok (index lookup only)

> **2026-08-17 update:** BUNDLE 1 (Design) and BUNDLE 2 (Animation) below are superseded by
> **`BUNDLE-B-frontend/SKILL.md`**, which is now the accurate, deduped router for all
> design/UI/animation skills (taste-skill, uxui-principles, frontend-patterns, motion-ui,
> magic-ui-generator, shadcn, etc — see that file for the real current list). This doc's Bundle 1/2
> sections are left below for the routing-flow explanation only; treat their skill lists as stale.
> BUNDLE 3 (Video) and BUNDLE 4 (Localization) are unaffected and still current.

---

## How It Works

Instead of 4 separate skills, **overseer categorizes existing + new skills into 4 bundles**. When user asks for a task:
1. **skill-router** classifies the domain + action
2. **overseer** finds matching bundle (keyword-based lookup)
3. **kyros-orchestrator** routes to first skill in bundle
4. **skill chains** within bundle execute sequentially or parallel

**Bundle selection is automatic.** No user prompting needed.

---

## BUNDLE 1: DESIGN → COMPONENT SYSTEM (superseded — see BUNDLE-B-frontend)

**When to trigger:** "design system," "UI component," "create mockup," "audit design"

**Bundle contents (auto-cascade) — see `BUNDLE-B-frontend/SKILL.md` for the current, deduped list:**
1. `design-system` (LIVE) — Figma/muapi.ai mockups + consistency audit
2. `taste-skill` (LIVE) — canonical premium/anti-slop generator (was missing from this list)
3. `magic-ui-generator` (LIVE, newly installed) — 21st.dev multi-variant component generation
4. `shadcn` (LIVE, newly installed) — shadcn/ui component base layer
5. `radix-ui-design-system` (lib) — Headless component patterns
6. `figma-create-design-system-rules` (lib) — Figma automation
7. `ui-design` (LIVE) — muapi.ai wireframe/mockup image generation

**Keywords trigger:**
- "design system" / "component" / "ui kit" / "figma" / "mockup" / "atomic design" / "design audit"

**Flow:**
```
User: "Build a design system for our app"
  → skill-router detects "design" domain
  → overseer matches BUNDLE 1 keywords
  → Calls design-system skill
  → If user asks for components → chains to ui-component
  → If user asks for Figma rules → chains to figma-create-design-system-rules
```

**Token efficiency:** Only active skill loaded (~5-10 tok per call). Others available via `.` chain notation.

---

## BUNDLE 2: ANIMATION → PRODUCTION PIPELINE (superseded — see BUNDLE-B-frontend / motion-ui)

**When to trigger:** "animation," "motion," "lottie," "3D," "video," "cinema"

**Bundle contents (auto-cascade) — `motion-ui` (LIVE) is now the canonical entry point; it contains
a "Beyond This Skill" section pointing to all off-context items below, so pull them via
`python3 ~/.claude/overseer/search.py <name>` rather than treating this as a separate bundle:**
1. `motion-ui` (LIVE) — canonical: tokens, perf/a11y/SSR, core patterns, now includes Disney-12
   principles pointer (was `framer-motion` (lib), merged in as a reference, not duplicated)
2. `lottie-bodymovin` (lib) — After Effects → Lottie export
3. `threejs-animation` (lib) — 3D animation + keyframes
4. `motion-patterns` (lib) — Stagger, sequence, scroll-linked, toasts, page transitions
5. `motion-advanced` (lib) — gestures, drag, SVG draw-on, imperative animation
6. `animejs-animation` (lib) — Anime.js library patterns (non-React)
7. `cartoon-dance-animation` (lib) — Photo → animated character
8. `svg-character-animation` (lib) — SVG rigging + GSAP
9. `canvas-procedural-animation` (lib) — p5.js + procedural effects

**Keywords trigger:**
- "animation" / "motion" / "lottie" / "framer motion" / "3D" / "character animation" / "dance" / "svg animation" / "canvas effects"

**Flow:**
```
User: "Create a Lottie animation for our loading state"
  → skill-router detects "design" domain + "build" action
  → overseer matches BUNDLE 2 keywords
  → Calls motion-ui (primary, Framer Motion first)
  → User specifies Lottie → chains to lottie-bodymovin
  → If 3D needed → chains to threejs-animation
```

---

## BUNDLE 3: VIDEO → PRODUCTION PIPELINE

**When to trigger:** "video," "edit," "clip," "render," "motion ad," "subtitle," "montage"

**Bundle contents (auto-cascade):**
1. `video-editing` — primary video workflow skill
2. `remotion-video-creation` (LIVE) — React video rendering
3. `06-motion-design-ad` (LIVE) — Seedance 2.0 motion ads
4. `video-editing` (LIVE) — FFmpeg + Remotion workflows
5. `youtube-clipper` (LIVE) — YouTube → short clips
6. `ai-clipping` (LIVE) — Clip platform integration
7. `video-translate` (LIVE) — Subtitle translation
8. `speech` (LIVE) — Voice synthesis + voiceover
9. `video_toolkit` (LIVE) — Unified pipeline (currently LIVE, will be primary)
10. `fal-workflow` (lib) — FAL model chaining for video
11. `one-shot-video` (lib) — Cinematic single-shot renders
12. `product-showcase-video` (lib) — Product demo videos
13. `cartoon-dance-animation` (lib) — 3D animation in video
14. `seeking-and-analyze-video` (lib) — Video analysis + transcription

**Keywords trigger:**
- "video" / "edit" / "clip" / "render" / "motion ad" / "cinematic" / "montage" / "subtitle" / "voiceover" / "youtube" / "reels" / "shorts"

**Flow:**
```
User: "Turn this 20-min interview into 5 TikTok clips with captions"
  → skill-router detects "video/media" domain + "build" action
  → overseer matches BUNDLE 3 keywords ("clip" + "video")
  → Calls video-editing (with specialized video skills as needed)
    → Step 1: youtube-clipper (ingest + split)
    → Step 2: ai-clipping (scene detection + key moments)
    → Step 3: video-editing (cut + trim)
    → Step 4: video-translate (auto-caption + Arabic if needed)
    → Step 5: video_toolkit (render + optimize per platform)
  → Output: 5 platform-optimized videos
```

**Token efficiency:** Chains execute sequentially, each skill loaded only when called (~5 tok each).

---

## BUNDLE 4: LOCALIZATION → GLOBAL DELIVERY

**When to trigger:** "Arabic," "localize," "translate," "subtitle," "voiceover," "multilingual," "i18n"

**Bundle contents (auto-cascade):**
1. `global-content-delivery` (NEW: consolidates below)
   - `video-translate` (LIVE) — Video subtitle translation
   - `speech` (LIVE) — Voice synthesis (Arabic, EN, etc.)
   - `i18n-localization` (LIVE) — i18n patterns
   - `doubao-tts` (LIVE) — Chinese/Arabic TTS
   - `language-translator` (agent) — Cultural context + regional dialects

**Keywords trigger:**
- "Arabic" / "localize" / "translate" / "subtitle" / "voiceover" / "multilingual" / "i18n" / "RTL" / "Arabic audio"

**Flow:**
```
User: "Localize our product video for Arabic + Persian markets"
  → skill-router detects "localization" intent
  → overseer matches BUNDLE 4 keywords
  → Calls global-content-delivery orchestrator
    → Step 1: video-translate (extract + translate subtitles)
    → Step 2: speech (generate Arabic + Persian voiceovers)
    → Step 3: i18n-localization (RTL layout, date/number formatting)
    → Step 4: language-translator (cultural context review)
  → Output: 2 fully localized videos
```

---

## AUTOMATION WORKFLOWS (N8N)

**Bundle 5: CLIPPING FACTORY WORKFLOW** (orchestrated via n8n)

Triggers: New video uploaded to clip-platform bucket → workflow executes BUNDLE 3 → clips published to 4 platforms

```yaml
Workflow: "clip-platform-to-tiktok-reels-shorts"
Trigger: S3 upload → clip-platform/inbox/

Steps:
  1. ai-clipping (BUNDLE 3) — detect scenes + key moments
  2. youtube-clipper (BUNDLE 3) — split into 15–60s segments
  3. video-editing (BUNDLE 3) — auto-caption + branding
  4. video-translate (BUNDLE 4) — Arabic subtitles (if requested)
  5. video_toolkit (BUNDLE 3) — render per platform (TikTok/Reels/Shorts)
  6. Publish to TikTok API, Meta Graph API, YouTube Shorts API

Cost: ~$0.05/video (OpenAI whisper + FAL render)
Speed: 5-min video → 5 clips in ~2 min
```

**Keywords in n8n:** "workflow" / "automation" / "pipeline" / "clipping" / "batch"

---

## BUNDLE ROUTING TABLE (FAST LOOKUP)

| User says | Bundle | First skill |
|-----------|--------|------------|
| "design system" | BUNDLE 1 | design-system |
| "create UI components" | BUNDLE 1 | ui-component |
| "animate this" | BUNDLE 2 | motion-ui |
| "lottie export" | BUNDLE 2 | lottie-bodymovin |
| "3D character" | BUNDLE 2 | threejs-animation |
| "create a video" | BUNDLE 3 | video-editing |
| "clip this interview" | BUNDLE 3 | ai-clipping |
| "edit footage" | BUNDLE 3 | video-editing |
| "add Arabic subtitles" | BUNDLE 3 + BUNDLE 4 | video-translate + speech |
| "localize for Arabic" | BUNDLE 4 | global-content-delivery |
| "multilingual TTS" | BUNDLE 4 | speech |
| "automate clipping workflow" | AUTOMATION | n8n-workflow-patterns |

---

## INTEGRATION WITH OVERSEER

**Add to `~/.claude/overseer/index.tsv`:**

```tsv
kind	location	name	description	bundle
bundle	skills	BUNDLE-1-design-system	UI components + design systems + Figma	design
bundle	skills	BUNDLE-2-animation	Motion + Lottie + 3D + animation	video/media
bundle	skills	BUNDLE-3-video-production	Video editing + clipping + rendering	video/media
bundle	skills	BUNDLE-4-localization	Arabic + multilingual translation + i18n	localization
bundle	productivity	n8n-clipping-factory	Automated clipping pipeline (clip-platform → TikTok/Reels/Shorts)	automation
```

**Search syntax:**
```bash
# Find all animation bundles
python3 ~/.claude/overseer/search.py animation --kind bundle

# Find all video skills (bundles + individual skills)
python3 ~/.claude/overseer/search.py video --cat media-video

# List all bundles
python3 ~/.claude/overseer/search.py --kind bundle --list -n 100
```

---

## INTEGRATION WITH KYROS

**Kyros routes to bundles, not individual skills:**

```yaml
# In Kyros action.yaml for Clip Platform
actions:
  clip_to_social:
    trigger: "Create clips from video"
    bundles:
      - BUNDLE-3-video-production (clips step)
      - BUNDLE-4-localization (if Arabic requested)
    parallel: false
    timeout: 300s
    
  design_new_component:
    trigger: "Design new UI component"
    bundles:
      - BUNDLE-1-design-system
    timeout: 120s
```

When Kyros receives a task, it:
1. Detects keywords (via overseer)
2. Selects matching bundle(s)
3. Chains skills within bundle
4. Reports results back

---

## TOKEN EFFICIENCY GAINS

| Scenario | Old (separate skills) | New (bundles) | Savings |
|----------|---------------------|--------------|---------|
| User asks for video clip | 3 skill lookups + load time | 1 bundle lookup + auto-chain | ~40% |
| Design + animation task | 2 separate invocations | 1 bundle dispatch + 2 skills | ~30% |
| Full localization workflow | 4 separate skills | 1 bundle orchestrator | ~50% |
| Overseer search (no active bundle) | Search ~3247 items | Search only 5 bundles + bundle contents | ~99% faster |

**Cost per bundle lookup:** ~2 tokens (index only)
**Cost per skill load within bundle:** ~5 tokens (skill is live or cached from first call)
**Cascading skills:** ~0 additional cost (already in context from first load)

---

## NEXT STEPS

1. **Research external repos** (parallel, 4 agents)
   - humanizer (text humanization)
   - OmniRoute (routing orchestrator)
   - scroll-world (scroll interaction design)
   - claude-real-video (video generation)
   - OpenMontage (video montage tool)
   
2. **Create bundle wrappers**
   - BUNDLE-1 / BUNDLE-2: DONE 2026-08-17 — see `BUNDLE-B-frontend/SKILL.md`
   - BUNDLE-3: Write bundle coordination prompt (still open)
   - BUNDLE-4: Write bundle coordination prompt (still open)

3. **Update overseer index** (~5 min)
   - Add bundle entries to `index.tsv`
   - Run `build_index.py` to rebuild

4. **Set up n8n workflow** (~45 min)
   - Create clip-platform trigger
   - Chain BUNDLE-3 steps
   - Deploy to Vercel cron

5. **Test with 5 sample tasks** (~30 min)
   - Task 1: "Design a button component"
   - Task 2: "Animate a loading spinner"
   - Task 3: "Create a TikTok clip from this video"
   - Task 4: "Add Arabic subtitles"
   - Task 5: "Build a design system"

---

## FILE LOCATIONS

- **Bundle master:** This file (SKILL-BUNDLES-INDEX.md)
- **Bundle wrappers:** `~/.claude/skills-library/BUNDLE-*.md` (created next)
- **Overseer index:** `~/.claude/overseer/index.tsv` (updated next)
- **n8n workflow:** Vercel scheduled task config
- **Kyros routes:** `~/.claude/skills/kyros-orchestrator/actions.yaml` (updated next)
