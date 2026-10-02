---
name: platform-exit-and-self-host
description: Method for leaving a managed/AI app platform (Replit, Lovable, Bolt, v0, Vercel-hosted agent builds) and running the app on our own accounts and hosting, without losing anything the platform did silently. Audit first (what did it do, why), then replace, then cut over, then retire. Includes the FreshExpiry Render + Neon + Clerk recipe, free-tier facts verified 2026-09, direct-APK distribution, and the gotchas hit on Windows. Use for "move off Replit", "self-host this", "go public without X", "what does this platform actually do for us", or any first public launch of a generated app.
---

# Exit a platform, keep everything it did

Worked example and the full table: `Empire_Base/FreshExpiry/docs/REPLIT_EXIT.md` and `docs/DEPLOY_AND_DOMAIN.md`. Read them before repeating this on another app.

## 1. Audit before touching anything (this is the step people skip)
List every job the platform did, in a table: job, how, why it mattered, replacement. Sources of truth:
- config files (`.replit`, `artifact.toml`, `vercel.json`, `*.toml`): routing, build/run commands, health path, ports, post-merge hooks;
- `git log --format='%an %s'` on the main branch: agent commits, especially **"Published your App"**-style commits = a live deployment may already exist. Never tell the user "nothing is public" without checking this;
- code that mentions the platform (`grep -ri replit`, env like `REPL_ID`): often dev-only plugins, sometimes a real coupling (auth proxy);
- **provisioned services**: decode publishable keys (Clerk `pk_test_` base64 gives the instance domain), read the DB host and role. A platform-managed Clerk/DB instance is not yours: no dashboard, cannot be rotated. Plan new accounts, do not assume access;
- docs the agent wrote (`replit.md`, `.agents/`): context only, delete or archive.

## 2. Replace, smallest thing that keeps behaviour
- **One origin.** Let the API server serve the built site (`express.static` + SPA fallback that skips `/api` and any path with a file extension so a missing asset is 404, not the app shell). Mount it before auth middleware so static files never touch Clerk. Same origin means no CORS work and cookies just work.
- **Auth.** Own Clerk account. Platform-style Clerk *proxy* middleware is opt-in (`CLERK_PROXY_ENABLED=true`), only for a production instance on a domain you own; with `pk_test` keys it breaks sign-in.
- **DB.** Own Neon project in the same region as the host; schema by `drizzle-kit push`, migrations after. Do not rely on a post-merge hook that pushes schema.
- **Host.** Render free web service (`render.yaml` blueprint, `sync: false` for secrets, `healthCheckPath`, `region` next to the DB, `NODE_OPTIONS=--max-old-space-size=400` for the 512 MB build). Free tier sleeps after 15 min and wakes in ~1 min: pair with a free 5-minute uptime ping on the health route (750 h/month covers one always-on service). Alternatives checked 2026-09: Fly and Railway are no longer really free, Koyeb closed free signups after the Mistral acquisition, Oracle Always Free is best long term but needs a card and manual server work. Re-verify before quoting.
- **Dev tooling.** Delete platform Vite plugins and unused SDKs; regenerate the lockfile with `pnpm install --lockfile-only --ignore-scripts` and check the diff is removals only.
- Add `"packageManager": "pnpm@x.y.z"` so `corepack enable` on the host uses the same pnpm.

## 3. Cut over in this order
build + typecheck locally, run the server in `NODE_ENV=production` on a spare port, curl `/`, deep links, `/api/healthz`, a missing asset (404), run the security smoke test, then deploy, run the same smoke test against the public URL, **then** retire the old copy: disconnect the platform from GitHub (its agent can otherwise keep pushing to `main`), unpublish its deployment, only then merge to `main`. Rotate anything that lived only in the platform's secrets.

## 4. Public-site hygiene learned the hard way
- Never a personal email/phone on a public page. Contact address comes from a build env var (`VITE_SUPPORT_EMAIL`), unset = shown nowhere; real fix is `support@<domain>` via free Cloudflare Email Routing. The smoke test greps the JS bundle for personal-mailbox addresses.
- Account-deletion (Play requirement) lives inside the Privacy Policy; keep a stand-alone URL for the store form but not as a footer "tab".
- Direct APK download before Play: small **separate public** releases repo holding only the signed APK (source repo stays private), SHA-256 shown on the download page, build env `VITE_ANDROID_APK_URL/SHA256/VERSION`. Use ONE signing key and later upload it to Play App Signing so sideloaded installs can still update. No payment link inside the app.

## 5. Windows / this-machine gotchas
- `pnpm --filter <pkg> run codegen` may try an auto-install and die on the `preinstall` shell script. Call the tool directly: `lib/api-spec/node_modules/.bin/orval --config ./orval.config.ts`, and `tsc -b` in `lib/api-zod` and `lib/api-client-react` (api-server resolves those libs through `dist`, so rebuild them or new exports look missing).
- Bash tool `sed` with `\n` in JS strings silently no-ops: use Edit/Write. Verify with grep after every scripted edit.
- Android builds: keep Gradle/AVD/caches on D:, compileSdk may need to be raised when AndroidX libs demand it (`sdkmanager "platforms;android-37.0"`).
- Kill only exact PIDs (`Get-NetTCPConnection -LocalPort N` then `Stop-Process -Id`).

## Self-check before saying "done"
Every row of the audit table has a replacement or an explicit "dropped, because"; smoke test green locally and on the public URL; no platform files left; the human-only steps are listed with exact clicks.

## 6. Lessons from the 2026-09-27 host hunt (the user: Syria, no card)
- **Web-search claims about free tiers were wrong three times** (Render "no card", Zeabur "free plan", Google "always free"): open the real signup/deploy page and see whether it asks for a card BEFORE writing config around a host. A hands-on 5-minute probe beats a blog.
- **Billing-country lists exclude Syria** (Google Cloud, Stripe-based forms). Same sanctions pattern that bars WhatsApp Business Platform from +963. If the user is in Syria and has no card, plan for self-hosting.
- **Self-host recipe that worked:** service on his PC (Task Scheduler at logon, direct `Start-Process` of the executables in a supervisor loop, BelowNormal priority, `--max-old-space-size`), free Cloudflare quick tunnel to test, then a named tunnel on a free DigitalPlat domain via Cloudflare DNS for a stable address.
- **Neon from his network:** TCP 5432 connects but the Postgres handshake times out; Neon's WebSocket driver (`@neondatabase/serverless` + `ws`, port 443) works. Test with `pg` and the WS driver side by side before blaming config.
- **Tool-sandbox quirks:** a nested `powershell -File` started from the tool exits at once (start executables directly); `deploy\logs` was refused as a protected path (use another folder name); `tasklist //FI` twice is AND; `vercel env pull` of production secrets is blocked by the auto-mode classifier (credential materialization), do not retry it, feed keys from files without printing them; the Claude browser extension disconnects on account switch (reconnect in Brave: Extensions > Claude, same account).
- Something else already owned the default port (8080): check `netstat -ano | findstr :PORT` and pick a free port instead of killing an unknown process.
