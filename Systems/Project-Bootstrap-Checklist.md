---
tags: [systems/bootstrap, systems/tooling]
status: draft
updated: 2026-10-04
confidence: medium
---
# Project Bootstrap Checklist

## TL;DR
- Day one is about **foundations that are expensive to retrofit**: Rojo repo + CI, strict typing, Init/Start architecture, ProfileStore data layer with versioning, guarded remotes layer, analytics hooks, StreamingEnabled, and game settings.
- Do it in the order below; each step has a "done when" test. Target: ~1 day for an experienced agent.
- Use a **separate test experience** (or test place in the same universe) for live-server testing; keep production DataStores clean.
- Create `Projects/<GameName>/` notes from `Templates/Project-Template.md` and record every decision there.

## Details

### 1. Repo and tooling (≈1 h)
- [ ] `git init`; `.gitignore`: `Packages/`, `ServerPackages/`, `sourcemap.json`, `*.rbxl`, `*.rbxlx`, `*.lock` (keep `wally.lock` committed ⚠️ verify team preference).
- [ ] `rokit init` + `rokit.toml` with rojo, wally, selene, stylua, luau-lsp, wally-package-types ([[Tooling-Rojo-Wally-And-Studio-MCP]]).
- [ ] `default.project.json`, `selene.toml`, `stylua.toml`, `wally.toml` (ProfileStore, Trove, Signal).
- [ ] `.github/workflows/ci.yml` (stylua --check, selene, luau-lsp analyze, rojo build, banned-API greps).
- [ ] Studio: install Rojo plugin; `rojo serve`; connect. Enable Studio MCP server and connect Claude Code.
- Done when: CI green on first commit; Studio shows synced `ServerScriptService.Server`.

### 2. Folder skeleton (≈30 min)
```
src/server/Main.server.luau
src/server/Services/{DataService,ReceiptService,ErrorReporter,AnalyticsService?}.luau
src/server/Net/{Guard,RateLimiter}.luau
src/client/Main.client.luau
src/client/Controllers/{UIController,InputController}.luau
src/shared/{Types,Net,Config}.luau
src/shared/Util/{Retry,Log,PartPool}.luau
src/first/LoadingScreen.client.luau
```
Name the analytics wrapper `Analytics.luau` (not `AnalyticsService`) to avoid confusion with the engine service.
- Done when: server and client bootstraps print "ready" with service counts; no type errors. See [[Module-Architecture]].

### 3. Data layer (≈1–2 h)
- [ ] ProfileStore via Wally (server realm); `DataService` with `TEMPLATE`, `Version`, `MIGRATIONS`, Mock in Studio, kick on failure ([[Data-Persistence-DataStores-And-ProfileStore]]).
- [ ] Key format `Player_<UserId>`; `AddUserId`.
- [ ] `ReceiptService` with idempotent `PurchaseIds` (even before products exist).
- [ ] Creator Hub → Data Stores Manager → RTBF templates for every user-keyed store.
- Done when: join → data loads, change coins, rejoin in a live test server → persisted; two-server test shows session lock handoff.

### 4. Remotes layer (≈1 h)
- [ ] All remotes defined in one module (`Shared/Net.luau` or Blink/Zap schema); server creates them.
- [ ] `Guard` + `RateLimiter` used by every handler; strike logging.
- [ ] Initial-state snapshot remote (server → client on data load) + delta events.
- [ ] Honeypot remote.
- Done when: fuzz test (`execute_luau` on Client firing random types/NaN/huge strings) produces no server errors and no state change. See [[Remotes-And-Networking]].

### 5. Analytics hooks (≈1 h)
Wrap `AnalyticsService` (engine) in `src/server/Services/Analytics.luau`:
```lua
--!strict
-- ServerScriptService/Server/Services/Analytics.luau
local AnalyticsService = game:GetService("AnalyticsService")
local Analytics = {}

function Analytics.Onboarding(self: typeof(Analytics), player: Player, step: number, name: string)
	pcall(AnalyticsService.LogOnboardingFunnelStepEvent, AnalyticsService, player, step, name)
end

function Analytics.Economy(
	self: typeof(Analytics),
	player: Player,
	source: boolean, -- true = earned, false = spent
	currency: string,
	amount: number,
	balance: number,
	transactionType: string, -- e.g. Enum.AnalyticsEconomyTransactionType.Gameplay.Name
	sku: string?
)
	local flow = if source then Enum.AnalyticsEconomyFlowType.Source else Enum.AnalyticsEconomyFlowType.Sink
	pcall(AnalyticsService.LogEconomyEvent, AnalyticsService, player, flow, currency, amount, balance, transactionType, sku)
end

function Analytics.Custom(self: typeof(Analytics), player: Player, event: string, value: number?)
	pcall(AnalyticsService.LogCustomEvent, AnalyticsService, player, event, value or 1)
end

return Analytics
```
- [ ] Onboarding funnel steps 1..N for the first session (spawn → first action → first reward → first upgrade …).
- [ ] Economy events at every currency source/sink.
- [ ] Custom events for core loop milestones.
- Exact event design lives in the Operations folder (analytics notes). ⚠️ verify: per-experience event-name/custom-field cardinality limits (custom fields limited to 8,000 unique combinations per experience, docs 2026-10-04).

### 6. Place/Workspace settings (≈15 min)
| Setting | Value |
|---|---|
| `Workspace.StreamingEnabled` | true; `ModelStreamingBehavior = Improved`; integrity `PauseOutsideLoadedArea` |
| `Workspace.SignalBehavior` | `Deferred` (Roblox's intended future default; required for Server Authority) |
| `Workspace.PhysicsSteppingMethod` | Adaptive |
| `SoundService.RespectFilteringEnabled` | true |
| `StarterGui` ScreenGuis | `ResetOnSpawn = false` |
| `Players.CharacterAutoLoads` | true unless you need a menu before spawn |
| `Players.BanningEnabled` | true (Ban API) |
| `Workspace.AuthorityMode` | `Server` only for competitive physics games ([[Client-Server-Boundary-And-Replication]]) |

### 7. Game settings (Creator Hub / Studio Game Settings)
- [ ] **Security**: Enable Studio Access to API Services (on for test experience only; ProfileStore Mock protects live data); Allow HTTP Requests only if needed; Allow Third-Party Sales/Teleports **off** unless required.
- [ ] **Avatar**: R15, collision/scale settings fitting gameplay; disable avatar body scale if hitboxes matter.
- [ ] **Places**: max players (start 12–20 for social sims, 6–12 for round-based), server fill = Roblox optimised.
- [ ] **Permissions/Access**: private until launch; set up a group if multiple people collaborate.
- [ ] **Maturity & compliance questionnaire** completed (required for discovery) ⚠️ verify: current questionnaire requirements.
- [ ] **Monetisation placeholders**: create dev products/game passes early for receipt testing.
- [ ] **Localization**: enable automatic translation / text capture ⚠️ verify settings name.
- [ ] Test place in the same universe for QA; teleport-free.

### 8. Quality gates before first public test
- [ ] Performance pass on a low-end phone ([[Performance-And-Profiling]]).
- [ ] Movement guard + remote fuzz passed ([[Anti-Exploit-And-Server-Authority]]).
- [ ] ErrorReporter running; Error Report empty after 30 min playtest ([[Error-Handling-And-Logging]]).
- [ ] Data survives server shutdown (`BindToClose` via ProfileStore) — test with "Shut down all servers".

## Pitfalls
- Building gameplay first and "adding data later" — retrofitting session locking and migrations is painful.
- Testing purchases only in Studio — test in a live private server with real (cheap) purchases or test products.
- Leaving Studio API access on with live keys and no Mock → corrupted production data during development.
- Skipping analytics until launch → no baseline for D1 retention/funnel fixes.

## Related
- [[Module-Architecture]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]]
- [[Data-Persistence-DataStores-And-ProfileStore]]
- [[Remotes-And-Networking]]
- [[Streaming-And-Instance-Streaming]]
- [[Common-Libraries]]
- [[_Index]]

## Sources
- https://create.roblox.com/docs/reference/engine/classes/AnalyticsService (method signatures read via github.com/Roblox/creator-docs, 2026-10-04)
- https://create.roblox.com/docs/reference/engine/enums/SignalBehavior (Default will eventually change to Deferred)
- https://create.roblox.com/docs/workspace/streaming
- https://create.roblox.com/docs/cloud-services/data-stores/right-to-be-forgotten
