---
name: roblox-game-factory
description: Build Roblox games using the verified free/OSS toolchain (Rojo, Wally, Remodel, Knit, ProfileStore) and the Game Factory architecture spec. Use for any Roblox game build, package install, or category (gacha/roguelite/obby/battlegrounds/horror) decision.
---

# Roblox Game Factory

Project root: `~\Documents\Roblox-Game-Factory`
Architecture spec: `~\Documents\Codex\2026-09-18\1-rojo-the-bridge-link-rojo\outputs\Roblox_Game_Factory_Architecture.docx`
Category analysis (trend/saturation/monetization per category): published artifact from 2026-09-18 session — regenerate via `python3 ~/.claude/overseer/search.py roblox` + market knowledge if not found.

## CLI tools (installed, on PATH)
- `rojo` 7.4.4 — `~\RobloxTools\rojo.exe` — `rojo serve` (dev sync), `rojo build -o game.rbxlx` (artifact)
- `wally` 0.3.2 — package manager, `wally install` from project root
- `remodel` 0.11.0 — deterministic map generation from seed+config, `remodel run remodel-scripts/generate_map.lua`

## Verified free/OSS packages (wally.toml, all MIT, checked against api.wally.run 2026-09-18 — names drift, re-verify before reuse)
```toml
[dependencies]
Knit = "sleitnick/knit@1.7.0"           # client-server framework
Signal = "sleitnick/signal@2.0.3"
Promise = "evaera/promise@4.0.0"
Sift = "csqrl/sift@0.0.11"              # immutable table utils
ZonePlus = "mattschrubb/zoneplus@3.2.0" # zone/region detection

[server-dependencies]
ProfileStore = "ddashdev/profilestore@1.1.0"     # successor to ProfileService, same author (loleris)
ReplicaService = "etheroit/replicaservice@1.0.2" # state replication, pairs with ProfileStore

[dev-dependencies]
TestEZ = "roblox/testez@0.4.1"
```
`ProfileService` itself has no canonical Wally listing (dozens of unofficial forks) — use `ProfileStore`, the maintained successor, instead. Don't reinstall from a forked scope without checking `curl -s https://api.wally.run/v1/package-metadata/<scope>/<name>` first — package availability changes.

Linting: **Selene** 0.31.0 installed at `~\RobloxTools\selene.exe` (on PATH). Needs `selene.toml` with `std = "roblox"` in the project root or it parses as plain Lua and panics on every type annotation. TestEZ spec files need `-- selene: allow(undefined_variable)` as their first line (describe/it/expect are runtime globals Selene can't see statically). **StyLua** (formatter) not yet installed — same GitHub-release pattern as Selene if needed.

**Blender 5.2.1 LTS is installed** at `D:\blender.exe` (not on PATH, not in Program Files — found via its Start Menu shortcut's target, `D:\blender-launcher.exe` launches the GUI, `D:\blender.exe` is the CLI/scriptable binary). Headless asset generation: `D:\blender.exe --background --python script.py`. `blender-assets/generate_gravebound_assets.py` in the project root generates procedural low-poly FBX props (enemies, weapons, arena props) — real, tested, exports to `blender-assets/exports/`. Re-run pattern for a new theme: copy that script, swap the geometry-building functions, keep the `export_fbx` helper.

**Remodel 0.11.0 has a real limitation, verified 2026-09-18:** its bundled offline reflection database only exposes base `Instance` properties (Name, Parent, ClassName) on freshly created instances — setting `Size`, `CFrame`, `Color`, `Anchored`, `Transparency` etc. on an `Instance.new("Part")` throws `'X' is not a valid member of Instance` even though the class itself is correctly named "Part". This is NOT true inside live Roblox (full reflection database there) — only in this offline Remodel binary. **Consequence: procedural map/prop generation must run in-engine** (a server-side Luau module using real `Instance.new`, like `src/server/Services/ArenaGenerator.luau`), not via a Remodel script, until a Remodel version/build with full reflection is confirmed. Remodel remains useful for reading/converting/inspecting existing `.rbxlx`/`.rbxm` files, which doesn't hit this limitation.

## Reference repos to study/adapt (verified via `gh api search/repositories`, all MIT/Apache, 2026-09-18)
Not drop-in dependencies — read the code, adapt patterns into our own `src/`, credit in docs if code is copied.
- **tralfa42real/roblox-rpg-core-systems** (MIT) — modular RPG backend: persistent profiles, inventory, equipment, economy, secure trading, vendors, loot, pets, guilds, area progression, combat hooks, enemy AI. Closest existing match to the factory's "universal game systems" section — study first before writing any of our own inventory/economy/trading code.
- **1Axen/Secure-Cast** (MIT, 30★) — server-authoritative projectile system. Matches Category B/D's "server-side hit confirmation" requirement exactly.
- **Echolewron/rbx-enemy-ai** (MIT) — modular enemy AI: patrol, chase, hiding states. Starting point for Category B's director/enemy pooling.
- **Bryan0-0AG/Procedural-Dungeon-Generator_Roblox-Studio** (MIT) — modular procedural dungeon generator. Reference for `remodel-scripts/generate_map.lua`.
- **buildthomas/MockDataStoreService** (Apache-2.0, 84★) — emulates DataStoreService for offline local testing without touching live data. Use in `tests/` so ProfileStore logic can be exercised without a live Roblox server.
- **ShakAsante/vfx-lib** (MIT) — lightweight VFX/particle utility library, complements native ParticleEmitter/Beam.

Re-run `gh api "search/repositories?q=<terms>+language:Lua&sort=stars&order=desc"` for other categories (A/C/D) when one is chosen — `gh` is authenticated (5000 req/hr) so prefer it over the unauthenticated `curl` GitHub API (60 req/hr, rate-limits fast).

## Real bugs found via actual Studio testing (2026-09-18) — check these first before deep debugging

1. **Never put `$className` on a `default.project.json` key that already names a real DataModel service** (`ReplicatedStorage`, `ServerScriptService`, etc.). Doing so makes Rojo's live-sync silently refuse to push children into that service — no error, it just never appears, and every module requiring it crashes with `"X is not a valid member of ReplicatedStorage"`. Only give `$className` to genuinely new instances Rojo is creating from scratch.
2. **A `require(script.X)` path only works if X is a real child of that exact file in the Rojo-synced tree** — a plain leaf `.luau` file has zero children; a sibling folder next to it is NOT reachable via `script.X`, only via `script.Parent.X`. This is easy to get wrong when a folder groups related files logically (e.g. `Config/GameConfig.luau` + `Config/Themes/`) — check the actual on-disk layout, not the logical grouping. The one exception: `init.server.luau`/`init.client.luau` make their sibling files real children via Rojo's init convention, so `script.Services.X` from an `init.server.luau` is correct.
3. **Debugging tool: Windows UI Automation via `pywinauto`** (`pip install pywinauto`, already done) is a real way to drive Roblox Studio directly — screenshot the window, click by pixel coordinate, read the Output log — when Studio's own MCP integration isn't available yet. `studio_control.py` in the project root has a working `find_studio()`/`screenshot()`/click pattern. Coordinates drift because the Studio window resizes/moves between actions — always re-fetch `win.rectangle()` right before clicking, don't reuse old coordinates.
4. **A crash inside a `require()` chain gives almost no detail in the one-line Output error** ("Requested module experienced an error while loading — Line N"). Click that error line in Studio to jump to the actual failing file, then read what's really on that line — the outer error's line number refers to the *outer* script, not where the real problem is.

## Roblox specialist agents (use via Agent tool for deep dives, not routine edits)
- `roblox-systems-scripter` — Luau, client-server security, RemoteEvents/Functions, DataStore
- `roblox-experience-designer` — engagement loops, monetization (Passes/DevProducts), progression tuning
- `roblox-avatar-creator` — UGC/avatar pipeline, accessory rigging, Creator Marketplace

## Category decision framework
Five options (A: Gacha, B: Roguelite, C: Escape/Obby, D: Battlegrounds, D: Horror) — score on trend, saturation, monetization, dev complexity before picking. Current read (2026-09-18): **B (Roguelite) is the strongest signal** — trending, medium saturation, strong non-predatory monetization (cosmetics/passes). Re-check trend before reusing this verdict; Roblox trends shift over months.

## Build protocol (from the architecture spec — do not skip)
Work in bounded slices, never generate all files at once:
1. **Concept** — one-page brief, core loop, audience, success metrics → gate: theme/category accepted
2. **Vertical slice** — one map zone, one complete loop, test checklist → gate: local build + playtest evidence
3. **Alpha** — progression, accessibility, analytics, economy tuning → gate: economy/content review
4. **Release candidate** — publishing config, policy checklist, rollback plan → gate: explicit publish approval
5. **Live ops** — versioned content, measured experiments, incident log → gate: no dark patterns/unreviewed price changes

Non-negotiables regardless of category: server-authoritative gameplay (never trust client for currency/inventory), typed remote contracts with per-action rate limits, profile data as source of truth with migration/reconciliation, no fake odds/hidden timers/forced scarcity, accessibility (motion/sound/contrast controls), publishing is a separate explicit step from building.
