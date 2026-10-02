---
name: public-apis-directory
description: Directory of 1,597 free/public APIs across 52 categories (dev, geocoding, finance, crypto, video, weather, government, health, ML, social, sports...). Use when a project needs a data source or third-party API - check here for a free option BEFORE proposing a paid service or building from scratch.
---

# Public APIs — 1,597 free APIs, 52 categories

Source: [github.com/public-apis/public-apis](https://github.com/public-apis/public-apis).
Pairs with the standing **free-for-dev** rule: check free options before proposing anything paid.

## How to use — grep, don't read

`reference/apis.md` is 223 KB. **Never read it whole.** Search it:

```bash
grep -i "weather"  ~/.claude/skills/public-apis-directory/reference/apis.md
grep -i -A2 "### Geocoding" ~/.claude/skills/public-apis-directory/reference/apis.md
sed -n '/^### Cryptocurrency/,/^### /p' ~/.claude/skills/public-apis-directory/reference/apis.md
cat ~/.claude/skills/public-apis-directory/reference/categories.txt   # all 52 + counts
```

Each row: **API · description · auth · HTTPS · CORS**. `auth: No` means no key needed — fastest to prototype with.

## Categories (largest first)

`Development` 135 · `Games & Comics` 97 · `Government` 97 · `Geocoding` 94 · `Transportation` 74 ·
`Cryptocurrency` 70 · `Finance` 54 · `Open Data` 45 · `Video` 45 · `Social` 43 · `Security` 42 ·
`Sports & Fitness` 41 · `Science & Math` · `Music` · `News` · `Weather` · `Health` · `Jobs` ·
`Machine Learning` · `Food & Drink` · `Books` · `Business` · `Email` · `Currency Exchange` ·
`Data Validation` · `Text Analysis` · `Photography` · `Anime` · `Art & Design` · `Animals` ·
`Authentication` · `Blockchain` · `Calendar` · `Cloud Storage` · `CI` · `Dictionaries` ·
`Documents & Productivity` · `Entertainment` · `Environment` · `Events` · `Patent` · `Personality` ·
`Phone` · `Programming` · `Shopping` · `Test Data` · `Tracking` · `URL Shorteners` · `Vehicle` ·
`Anti-Malware` · `Open Source Projects` · `Government`

Full list with counts: `reference/categories.txt`

## Workflow

1. Need a data source → grep the category or keyword here first.
2. Prefer `auth: No` / `HTTPS: Yes` for prototypes; check CORS for browser-side calls.
3. Verify the API is still live before building on it — this list is community-maintained and entries go stale.
4. Need an *integration* rather than raw data? Check the library too — there are ~875 `*-automation`
   connector skills: `python3 ~/.claude/overseer/search.py <service> --kind skill`
