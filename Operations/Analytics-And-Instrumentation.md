---
tags: [operations/analytics]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Analytics And Instrumentation

## TL;DR
- Instrument **before** launch. Roblox's built-in Creator Hub Analytics plus `AnalyticsService` cost nothing and need no backend. Day-one minimum: an onboarding funnel, a shop funnel, economy source/sink events for every currency, and about 10 custom events for the core loop.
- `AnalyticsService` calls work **only from the server and only in published games**. Calls from Studio or the client do nothing. Log **after** an action succeeds (purchase granted, step completed), not when it is attempted.
- Hard limits: **10 funnels × 100 steps**, **10 economy currencies**, **100 custom event names**, **3 custom fields** (8,000 combined values before the rest become "Other"). Rate limit: **120 + 20 × CCU requests/min**. Keep names few and put detail into custom fields.
- Wrap every call in one server module (code below) that validates input, budgets the rate limit and holds the event taxonomy. Never let gameplay code call `AnalyticsService` directly.
- Dashboard charts take **about 24 h** to populate. Use **View Events** on the Economy, Funnel and Custom pages to check events in near real time on launch day.
- Compare against the dashboard's "similar experiences" benchmark (50th–90th percentile band). Being under P50 on D1 is a design problem, not an analytics one (see [[Bad-Launch-Response]]).

## What Roblox gives you for free (Creator Hub → Analytics)
| Dashboard | Key metrics | Use for |
|---|---|---|
| Overview | DAU, MAU, CCU, playtime, D1/D7/D30, payer conversion, ARPPU, benchmarks | Daily health check ([[KPI-Dashboard-Spec]]) |
| Acquisition | New users by source (Home recs, Search, Charts, Friends, Sponsored/Search/Portal ads, Teleport…), impressions → **play-through rate**, cumulative new-user funnel | Diagnosing CTR and discovery ([[Discovery-Algorithm]]) |
| Engagement | Session time, playtime/DAU, sessions/user | Core loop health |
| Retention | D1/D7/D30 cohorts, breakdowns | [[Retention-Metrics-D1-D7-D30]] |
| Monetization | Revenue, payers, ARPPU, conversion, product breakdown | [[Conversion-Funnels]] |
| Economy / Funnel / Custom (Explore) | Unlocked by `AnalyticsService` events | This note |
| Performance | Client crash rate, FPS, memory, server heartbeat (eligible at 100+ DAU) | Live ops regressions |
| Alerts | Threshold alerts on performance and data store metrics, Discord/PagerDuty webhooks; up to **20 alerts/experience**; eligible at 100+ DAU | Paging on bad updates ([[Live-Ops-Playbook]]) |
| Error report | Script errors, including AnalyticsService errors | Post-update QA |

Breakdown and targeting segments that matter for decisions: **new vs returning**, **platform**, **country**, **age group**, **in-experience payer status** (percentile within your game: Top 15%, Intermediate 35%, Casual 50%, Lapsed, Never), and **platform spender status** ("Active" = spent ≥ $9.99 anywhere on Roblox in the last 60 days). Source: analytics-dashboard docs.

Benchmarks compare you with "experiences with similar players" (or genre, or all experiences), among games with ≥100 DAU, shown as a P50–P90 band. The docs' example D1 band is 12.11%–18.73%.

## AnalyticsService API (current, non-deprecated)
Verified against the creator-docs mirror, commit 9f840b1 (2026-10-02).

| Method | Signature (simplified) | Notes |
|---|---|---|
| `LogOnboardingFunnelStepEvent` | `(player, step: int, stepName: string?, customFields: {}?)` | One-time funnel. Repeated steps are ignored; skipped steps auto-complete. |
| `LogFunnelStepEvent` | `(player, funnelName, funnelSessionId: string?, step: int, stepName: string?, customFields?)` | Recurring funnels (shop, upgrade). Only the **10 most recent funnelSessionIds per user per funnel** are tracked. |
| `LogEconomyEvent` | `(player, flowType: Enum.AnalyticsEconomyFlowType, currencyType, amount: number (>0), endingBalance: number, transactionType: string, itemSku: string?, customFields?)` | `amount` is always positive; Sink shows as negative. |
| `LogProgressionEvent` | `(player, progressionPathName, status: Enum.AnalyticsProgressionType, level: int, levelName: string?, customFields?)` | Also the shorthands `LogProgressionStartEvent`, `LogProgressionCompleteEvent` and `LogProgressionFailEvent` (same args minus status). |
| `LogCustomEvent` | `(player, eventName, value: number = 1, customFields?)` | Counter or value. Use the value to batch ("10 kills"), not 10 calls. |
| `LogJourneyEvent` | `(player, journeyName, nodeName, journeySessionId, customFields?)` | Newer API. ⚠️ verify: dashboard support and limits; not on the limits page as of 2026-10-02. |
| `GetPlayerSegmentsAsync` | `(player) -> {}` | Yields. ⚠️ verify: returned keys before relying on them. |

Deprecated, do not use: `FireEvent`, `FireCustomEvent`, `FireInGameEconomyEvent`, `FirePlayerProgressionEvent`, `FireLogEvent`.

Default `Enum.AnalyticsEconomyTransactionType` values: `IAP`, `TimedReward`, `Onboarding`, `Shop`, `Gameplay`, `ContextualPurchase`. Pass `.Name`. Custom strings are allowed, but after 20 types the rest are grouped as "Other".

Custom field keys: `Enum.AnalyticsCustomFieldKeys.CustomField01.Name` … `CustomField03.Name`. Values must be **strings**; other keys are ignored.

### Limits (event-types doc, 2026-10-02)
| Limit | Value |
|---|---|
| Global rate | 120 + 20 × CCU requests/min (⚠️ verify: whether CCU means the server or the universe; budget per server to be safe) |
| Custom fields | 3; 8,000 combined unique values, then "Other" |
| Economy currencies | 10 |
| Economy transactionTypes | 20, then "Other" |
| Economy itemSkus | 100, then "Other" |
| Funnels | 10; 100 steps each |
| Custom event names | 100 |
| Retention | An event rolls off the dashboard 90 days after its last data |

## Day-one event taxonomy (copy this)
Rule: **events are verbs, fields are nouns**. Keep custom event names under 40 so later features have room within the 100.

**Funnels (max 10):**
1. `Onboarding` via `LogOnboardingFunnelStepEvent`, 8–15 steps from `PlayerAdded` to "completed first core loop twice". Example: 1 Joined → 2 Loaded/Spawned → 3 Moved → 4 FirstInteract → 5 FirstReward → 6 FirstUpgrade → 7 SecondLoop → 8 OpenedShop → 9 FirstQuestDone → 10 Session5Min.
2. `Shop` (recurring, GUID session): Opened → ViewedItem → PromptShown → PurchaseGranted.
3. `StarterPack` (recurring): OfferShown → Clicked → PromptShown → Granted.
4. `Rebirth` / `Prestige` (recurring; session = `userId-rebirthN`).
5. `Trade` (if trading exists): Requested → Accepted → Confirmed → Completed.
6. Spare slots go to the next big feature. Leave 3–4 free.

**Economy:** every currency (≤5 recommended) on every source and sink, with `itemSku` set to the product or item and CustomField01 = `Zone - <name>` or `Category - <x>`.

**Progression:** `LogProgressionEvent` for the main path (zones, levels, rebirths), with Start, Complete and Fail for challenge content.

**Custom events (start set):** `CoreLoopComplete` (value = seconds), `SessionMilestone` (field: 5/10/20/30 min), `FeatureUsed` (field: feature), `DeathOrFail` (field: cause), `RewardClaimed` (field: daily/streak/playtime), `SocialAction` (field: invite/friendJoin/partyForm), `SettingsChanged`, `ErrorShown` (field: code), `DataLoadFailed`, `PurchasePromptFailed`.

**Custom fields convention:** CF01 = context (zone/mode), CF02 = player tier (`Tier - New/Mid/End`), CF03 = experiment variant (`Exp - <key>=<value>`). Spending CF03 on the variant gives A/B breakdowns of every event for free ([[AB-Testing]]).

## Server module (ServerScriptService/Analytics.lua, ModuleScript)
```lua
--!strict
-- ServerScriptService/Analytics (ModuleScript). The ONLY place that calls AnalyticsService.
local AnalyticsService = game:GetService("AnalyticsService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

export type Fields = { [string]: string }?

local Analytics = {}

local CF1 = Enum.AnalyticsCustomFieldKeys.CustomField01.Name
local CF2 = Enum.AnalyticsCustomFieldKeys.CustomField02.Name
local CF3 = Enum.AnalyticsCustomFieldKeys.CustomField03.Name

-- Allow-lists keep cardinality under the limits (100 custom names, 10 currencies, 10 funnels).
local CUSTOM_EVENTS: { [string]: true } = {
	CoreLoopComplete = true, SessionMilestone = true, FeatureUsed = true, DeathOrFail = true,
	RewardClaimed = true, SocialAction = true, SettingsChanged = true, ErrorShown = true,
	DataLoadFailed = true, PurchasePromptFailed = true,
}
local CURRENCIES: { [string]: true } = { Coins = true, Gems = true }
local FUNNELS: { [string]: true } = { Shop = true, StarterPack = true, Rebirth = true, Trade = true }

-- Per-server token bucket sized to the documented 120 + 20*CCU per minute (we use server CCU, 80% headroom).
local tokens = 0
local lastRefill = os.clock()
local function take(): boolean
	local now = os.clock()
	local perMinute = (120 + 20 * #Players:GetPlayers()) * 0.8
	tokens = math.min(perMinute, tokens + (now - lastRefill) * perMinute / 60)
	lastRefill = now
	if tokens >= 1 then
		tokens -= 1
		return true
	end
	return false
end

local enabled = not RunService:IsStudio() -- events are dropped in Studio anyway

local function safe(fn: () -> ())
	if not enabled or not take() then return end
	local ok, err = pcall(fn)
	if not ok then warn("[Analytics]", err) end
end

-- Merges the experiment variant into CF03 automatically if the caller left it empty.
local variantTag: { [Player]: string } = {}
function Analytics.setVariantTag(player: Player, tag: string)
	variantTag[player] = tag
end
local function withFields(player: Player, f: Fields): { [string]: string }?
	local out: { [string]: string } = {}
	if f then for k, v in f do out[k] = v end end
	if out[CF3] == nil and variantTag[player] then out[CF3] = variantTag[player] end
	return if next(out) then out else nil
end

function Analytics.fields(context: string?, tier: string?, extra: string?): { [string]: string }
	local t: { [string]: string } = {}
	if context then t[CF1] = context end
	if tier then t[CF2] = tier end
	if extra then t[CF3] = extra end
	return t
end

function Analytics.onboarding(player: Player, step: number, name: string)
	safe(function()
		AnalyticsService:LogOnboardingFunnelStepEvent(player, step, name, withFields(player, nil))
	end)
end

function Analytics.funnel(player: Player, funnel: string, sessionId: string, step: number, name: string, f: Fields)
	assert(FUNNELS[funnel], "unknown funnel " .. funnel)
	safe(function()
		AnalyticsService:LogFunnelStepEvent(player, funnel, sessionId, step, name, withFields(player, f))
	end)
end

function Analytics.source(player: Player, currency: string, amount: number, balance: number,
	txType: Enum.AnalyticsEconomyTransactionType, sku: string?, f: Fields)
	assert(CURRENCIES[currency], "unknown currency " .. currency)
	if amount <= 0 then return end
	safe(function()
		AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Source, currency,
			amount, balance, txType.Name, sku or "", withFields(player, f))
	end)
end

function Analytics.sink(player: Player, currency: string, amount: number, balance: number,
	txType: Enum.AnalyticsEconomyTransactionType, sku: string?, f: Fields)
	assert(CURRENCIES[currency], "unknown currency " .. currency)
	if amount <= 0 then return end
	safe(function()
		AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Sink, currency,
			amount, balance, txType.Name, sku or "", withFields(player, f))
	end)
end

function Analytics.progression(player: Player, path: string, status: Enum.AnalyticsProgressionType,
	level: number, levelName: string?, f: Fields)
	safe(function()
		AnalyticsService:LogProgressionEvent(player, path, status, level, levelName, withFields(player, f))
	end)
end

function Analytics.custom(player: Player, name: string, value: number?, f: Fields)
	assert(CUSTOM_EVENTS[name], "add '" .. name .. "' to CUSTOM_EVENTS first")
	safe(function()
		AnalyticsService:LogCustomEvent(player, name, value or 1, withFields(player, f))
	end)
end

Players.PlayerRemoving:Connect(function(p) variantTag[p] = nil end)

return Analytics
```

Usage (server):
```lua
--!strict
-- ServerScriptService/Bootstrap.server.lua
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local Analytics = require(script.Parent.Analytics)

Players.PlayerAdded:Connect(function(player)
	Analytics.onboarding(player, 1, "Joined")
end)

-- In the shop handler, AFTER ProcessReceipt / currency deduction succeeds:
local function onShopOpened(player: Player): string
	local sid = HttpService:GenerateGUID(false)
	Analytics.funnel(player, "Shop", sid, 1, "Opened", Analytics.fields("Zone - Spawn"))
	return sid
end
```

Client-reported steps (UI opened, tutorial arrow followed) go through a RemoteEvent. The server must **validate** them: step within range, monotonic per player, rate-limited. The Roblox docs show exploiters can poison funnels otherwise.

## Session milestone pattern
Log `SessionMilestone` at 5, 10, 20 and 30 minutes. Comparing the share of players reaching each milestone against average session time shows whether a low average comes from a small group bouncing early or from everyone leaving at the same point.

## External analytics (when built-in is not enough)
| Option | When | Cost / notes |
|---|---|---|
| Built-in only | < ~5k DAU, solo dev | Free. Covers 90% of needs. |
| GameAnalytics Roblox SDK | Want cohort/raw-event views, real-time | Free tier. Uses `HttpService` from the server. ⚠️ verify: current SDK repo and maintenance status. |
| Own backend (HttpService → BigQuery/ClickHouse/PostHog) | Studios, raw SQL, LTV models | `HttpService` limit is 500 requests/min per server (⚠️ verify). Batch every 30–60 s. Never send PII; a UserId is fine, a username is not needed. |
| Open Cloud | Pull DataStore/MemoryStore state for offline analysis | API keys stored outside Roblox |

Decision rule: add external analytics only when you have a concrete question the Explore page cannot answer, such as per-user LTV curves, raw event joins or sub-hour latency.

## Checklist
- [ ] `Analytics` module in ServerScriptService; no other script requires AnalyticsService
- [ ] Onboarding funnel of 8–15 steps logged from `PlayerAdded`
- [ ] Shop funnel with GUID `funnelSessionId`
- [ ] Every currency source and sink logged with balance and SKU
- [ ] CF03 reserved for the experiment variant
- [ ] Client-originated steps validated server-side
- [ ] Day 0: open **View Events** on each page and confirm events arrive
- [ ] Day 1: Funnel, Economy and Explore pages populated; screenshot the baseline
- [ ] Alerts: client crash rate > 5% (5 min, critical) and DataStore error rate, wired to a Discord webhook

## Pitfalls
- Logging attempts instead of successes inflates purchase funnels.
- One event name per item (`PlantCabbage`, `PlantTurnip`) burns the 100-name cap. Use one event plus a field.
- Separate currencies per class (`WarriorXP`) burn the 10-currency cap. Use one currency plus a field.
- Changing funnel step numbers mid-flight breaks comparisons. Set the dashboard date range to start after the change.
- Funnel filters apply **only at the first step**, and funnels are attributed to the day the user **entered** (cohort).
- Testing in Studio and seeing nothing is expected. Test in a private published place.
- No numeric custom fields: `"Level - 10"` is a string, so bucket levels (`"Level - 10-19"`) to stay under the 8,000-value cap.

## Related
- [[Operations/_Index]] · [[KPI-Dashboard-Spec]] · [[AB-Testing]] · [[Live-Ops-Playbook]] · [[Bad-Launch-Response]]
- [[Retention-Metrics-D1-D7-D30]] · [[Conversion-Funnels]] · [[Discovery-Algorithm]] · [[Growth-Metrics-And-Benchmarks]]

## Sources
- Roblox creator-docs (mirror of create.roblox.com/docs), commit 9f840b1, 2026-10-02: `production/analytics/{event-types,custom-events,custom-fields,funnel-events,economy-events,analytics-dashboard,acquisition,alerts}.md`. Live URLs: https://create.roblox.com/docs/production/analytics/event-types and siblings. Checked 2026-10-04.
- API reference: `reference/engine/classes/AnalyticsService.yaml` (same commit), https://create.roblox.com/docs/reference/engine/classes/AnalyticsService
- Similar-experience benchmarks announcement: https://devforum.roblox.com/t/analytics-similar-experience-benchmarks-broader-access/2210285
