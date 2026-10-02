---
name: gmaps-scraper
description: Scrape Google Maps businesses (name, phone, website, rating, address, lat/lng, emails, reviews) for lead generation. Use when the user wants local business leads, "scrape Google Maps", or a lead list for a niche+city. Native Windows binary, no Docker.
---

# Google Maps Scraper (gosom, Docker)

Image: `gosom/google-maps-scraper` (MIT). The native Windows exe (`~/tools/gmaps-scraper/gmaps-scraper.exe`) is BROKEN on this machine: Chromium crashes after page load (upstream issue #137). Use Docker only.
Docker Desktop must be running; if not: launch `C:\Program Files\Docker\Docker\Docker Desktop.exe` and wait until `docker info` works.

## Run (from a run folder holding queries.txt, one query per line)
```
export MSYS_NO_PATHCONV=1   # Git Bash otherwise mangles /work
docker run --rm -v "$(cygpath -w $PWD):/work" gosom/google-maps-scraper -input /work/queries.txt -results /work/results.csv -depth 3 -c 2 -lang ar -exit-on-inactivity 3m
```
Test with 1 query at `-depth 1` first (~20 rows). Background anything bigger.
Flags: `-json`, `-email` (site email extraction, slower), `-extra-reviews`, `-geo lat,lon`, `-grid-bbox minLat,minLon,maxLat,maxLon -grid-cell 1`, `-lang ar|en`.
Output columns include title, category, address, phone, website, review_rating, review_count, latitude, longitude, emails.
Past runs live in `~/tools/gmaps-scraper/runs/<project>/` (e.g. ostazi-syria: 45 Arabic queries, 9 governorates x 5 tutoring types).

## After every run (automatic, do not wait to be asked)
1. `python ~/.claude/skills/gmaps-scraper/scripts/enrich.py <run>` - visits each lead's website: emails, socials, extra phones (cache enrich.json).
2. `PYTHONIOENCODING=utf-8 python ~/.claude/skills/gmaps-scraper/scripts/build_report.py <run> "<title>"` - merges duplicates (cid, phone, name+city), classifies tier A (tutoring/educational centers, tutors) / B (language, training, institutes) / C (schools) / X (excluded: driving, universities, clubs...), builds per-lead contact channels + CLAIM opener + D+3 follow-up, writes leads.csv/json, `import.csv` (Ostazi OutreachLead format, A+B only, skips phones already in `~/tools/gmaps-scraper/ledger.json`) and report.html.
3. Open report.html in Brave ONLY ONCE, when the whole job is finished - never after intermediate edits/rebuilds (the user explicitly complained). Command: `powershell -Command 'Start-Process "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" "file:///<path>/report.html"'`.
4. Ostazi import: admin panel -> Lead Tracker -> import `import.csv` (POST /outreach/import; server dedupes by externalId + normalized phone, append-only). Prod admin login needs an OTP, so the user does the click (or he supplies the code). After a successful import run `build_report.py <run> --mark` so the ledger blocks re-import.
Ostazi OutreachLead has no website/email/social columns: they go in `source` (shown as "المصدر"), the channel/opener plan in `pitch_angle`. Real columns would need a Prisma migration + prod deploy - only if the user asks.

5. Ostazi runs also feed the social plan: vault `10 - Projects/Ostazi_Social/Supply_Leads_Social_Outreach.md` + `supply_leads_social.csv` (leads with FB/IG/Telegram, follow -> engage -> DM day 3 -> one follow-up). Regenerate from leads.json after each Ostazi run.

6. Leads with NO phone, email, social or website are not discarded: they go to the "زيارة ميدانية" tab in report.html and `field_visits.csv` (name, address, map link, lat/lng, visited/notes columns) for in-person trips. Never import them to the tracker. Leads with only a website/social/email (no phone) stay in the main tab as digital-only.

## Rules
- Leads must have a real dialable phone — drop rows without one (memory: feedback_leads_must_have_real_phone).
- Conservative concurrency (`-c 1-2`); no proxy needed for small runs. Proxy/grid/query-planning detail: `references/*.md` (written for the Docker flow; flags are the same).
- Write outputs to the project or vault (Rule 5), not here.
