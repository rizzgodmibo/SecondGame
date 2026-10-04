---
tags: [operations/incident, growth/launch]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Bad Launch Response

## TL;DR
- **Diagnose before you change anything.** Walk the funnel in order: **impressions → CTR / play-through → first-session (onboarding funnel) → D1 → D7 → payer conversion → ARPPU**. Fix the **first** broken stage only, because downstream metrics are meaningless until upstream traffic is healthy.
- Thresholds (compare with your "similar experiences" P50 benchmark band on the dashboard; numbers below are rule-of-thumb ⚠️ verify against [[Growth-Metrics-And-Benchmarks]]): play-through **< 3%** → thumbnail/icon/title problem; onboarding step drop **> 25%** at a single step → tutorial problem; **D1 < 8–10%** → core loop / first 5 minutes; **D7 < 3%** → no mid-term goals; **payer conversion < 1%** with OK retention → offers/placement.
- **Data loss is a P0.** Stop the bleeding (kill switch / maintenance), find the window, restore from **DataStore version history** (hourly backups kept 30 days after being overwritten), compensate generously, and communicate within 1 h.
- **Rollback a bad update** by reverting the place version (Creator Hub → Place → Version History → Restore) **and** flipping configs off, then restart outdated servers. A data **schema** rollback needs a forward-fix, never a blind revert.
- **Pivot / relaunch rule:** after **3 iteration cycles (about 3–6 weeks)** on the broken stage with no movement toward P50, or if D1 stays **< 5%** with good CTR, rework the core loop or start a new game using what you learned. A relaunch on the same place keeps favorites and visits but not "new" status. ⚠️ verify how the algorithm treats relaunches.

## Triage table
| Symptom (first 72 h) | Where to look | Likely cause | Actions (in order) |
|---|---|---|---|
| Few impressions | Acquisition → impressions by source | Not yet in recommendations; no ads; no social seed | Run Sponsored/Search ads with a small budget to buy signal; influencer/Discord seed; make sure genre and description are set ([[Discovery-Algorithm]]) |
| Impressions OK, **low play-through** (impressions → plays) | Acquisition → play-through rate by source | Thumbnail/icon/title don't sell the fantasy; mismatched audience | Swap the icon first (biggest lever), then the title; test 3 icons over 3 days each; show gameplay, a face/character, and a single bright focal point |
| Plays OK, **players leave in < 2 min** | Onboarding funnel; session-milestone custom events; Performance (load time, crash) | Long load, confusing first 30 s, mobile UI broken, crash on low-end | Profile mobile load (target < 10 s to control); cut steps; first reward in < 30 s; fix the top error-report entries |
| Session OK, **D1 low** | Retention by source/platform; funnel past onboarding | No "come back" hook; progress not visible; no daily reward; data not saving | Add a daily reward plus a visible next goal; check save success rate; notifications/favorite prompt ([[Retention-Metrics-D1-D7-D30]]) |
| D1 OK, **D7 low** | Progression events; economy wallet balance | Content runs out; inflation trivialises goals; no social glue | Add mid-term goals (rebirth, collection book); fix economy sinks; groups/trading/co-op |
| Retention OK, **monetisation low** | Shop funnel; payer conversion by tier | Offers not seen; poor value; prices wrong | Starter pack at first-loop completion; contextual offers; A/B price ([[Conversion-Funnels]], [[AB-Testing]]) |
| Monetisation OK, **CCU falling week over week** | DAU new vs returning; acquisition mix | Algorithm traffic dropping as engagement metrics decay | Update cadence ([[Content-Cadence]]); events; refresh the thumbnail; ads in the update week |
| Sudden crash after an update | Error report, Performance, Alerts by place version | Regression | Roll back (below) |

Fix order logic: the recommendation system rewards engagement and retention of the players it sends you ([[Discovery-Algorithm]]). Buying traffic into a game with bad D1 wastes money and teaches the algorithm your game is bad. **Fix D1 before scaling acquisition.**

## The first 72 hours (playbook)
1. **T+0–2 h:** watch the error report, client crash rate, DataStore error rate, and **View Events** on the funnel and economy pages. Are saves working? Any infinite-currency bugs?
2. **T+24 h:** first daily data. Check onboarding funnel step drops, session time vs the benchmark, and play-through rate by source.
3. **T+48–72 h:** first D1 cohort. Pick **one** problem stage and make 1–3 changes. Ship as a MINOR update behind configs if possible ([[Live-Ops-Playbook]]).
4. **Weekly:** re-measure the same stage. Log each change and its result in `Projects/<game>/`.

Don't: change the icon, title, onboarding and prices on the same day. You won't know what worked.

## Data-loss incident response (P0)
Signs: players report reset progress; save error rate spikes; the profile loader logs `schemaVersion` mismatches; ProfileStore session-lock errors.

1. **Contain (≤ 10 min)**
   - Flip `maintenance_message` and the kill switches. If corruption is ongoing (bad writes), **make the game private** so no new bad writes happen. A restart alone lets players back in.
   - Stop any auto-migration code path via config.
2. **Scope (≤ 1 h)**
   - Find the start time: the place version publish time, or the first error. List affected users from logs, the analytics `DataLoadFailed` custom event, or by scanning keys (`DataStore:ListKeysAsync`) and comparing versions.
3. **Restore**
   - DataStores keep a **versioned backup from the first write of each UTC hour**. Backups expire **30 days after being overwritten**; the latest version never expires. Use `DataStore:ListVersionsAsync(key, sortDirection, minDate, maxDate, pageSize)` / `DataStore:GetVersionAtTimeAsync(key, timestampMs)` to fetch the last good version, then write it back with `UpdateAsync` (respect session locks if using ProfileStore).
   - Run the restore from a **one-off server script in a private server**, or through Open Cloud DataStore APIs, in batches, with a dry run first.
4. **Compensate**: restore plus a gift (currency, an exclusive cosmetic, a time-limited boost) for everyone online during the window, not only those who reported. Trading games: also freeze or roll back items created during the window, otherwise dupes stay in the economy.
5. **Communicate**: an in-game banner plus Discord/socials. Say what happened, who was affected, what you restored, and how to report missing items. Post an update every few hours until resolved.
6. **Post-mortem (48 h)**: root cause, why tests missed it, and a guardrail (e.g. "loader refuses to save if schemaVersion is newer", "save only when the load succeeded", "never save default data over existing data").

```lua
--!strict
-- ServerScriptService/Ops/RestoreProfile.lua (ModuleScript) — run from a private ops server / command bar.
-- Restores a key to the newest version written BEFORE `beforeUnixMs`.
local DataStoreService = game:GetService("DataStoreService")

local Restore = {}

function Restore.restoreKey(storeName: string, key: string, beforeUnixMs: number, dryRun: boolean): (boolean, string)
	local store = DataStoreService:GetDataStore(storeName)
	local okGet, value, info = pcall(function()
		return store:GetVersionAtTimeAsync(key, beforeUnixMs)
	end)
	if not okGet then return false, "get failed: " .. tostring(value) end
	if value == nil then return false, "no version before timestamp" end
	if dryRun then
		return true, `would restore version from {info and (info :: DataStoreKeyInfo).CreatedTime or "?"}`
	end
	local okSet, err = pcall(function()
		store:UpdateAsync(key, function(_current)
			return value -- ⚠️ if using ProfileStore, restore inside its session/metadata format instead
		end)
	end)
	return okSet, if okSet then "restored" else tostring(err)
end

return Restore
```
`GetVersionAtTimeAsync` returns `(value, DataStoreKeyInfo)`, or nil if no version existed at that time (checked against DataStore.yaml on 2026-10-02). Note that `UpdateAsync` in a restore creates a **new** version, so the bad version is still in history if you need it.

## Rolling back a bad update
| Situation | Action |
|---|---|
| Content/logic bug, no data impact | Config off → done. If not flag-gated: Place → Version History → **Restore** the previous version → Publish → Restart **outdated** servers |
| Exploit (currency/dupe) | Kill switch on the remote/feature; ban by server-side evidence; consider an **economy rollback only of the exploited currency/items**, never a full data rollback |
| Data schema change gone wrong | Don't revert code (old code can't read new data). Forward-fix the loader to accept both formats → publish → restart |
| Performance regression | Revert the place version; investigate in staging using Performance dashboard filters by place version |

Keep the previous production place version noted (number plus git tag) in every release note so rollback takes seconds.

## When to pivot, iterate or relaunch
| Signal after 3 iteration cycles | Decision |
|---|---|
| Play-through good, D1 ≥ P50, monetisation weak | **Iterate** on monetisation, then scale ads |
| Play-through good, D1 < P50 but improving each cycle | **Iterate** on onboarding/core loop |
| Play-through good, D1 flat at < ~5% despite changes | **Pivot the core loop** (keep theme/art) or **new game** |
| Play-through bad across 5+ icon/title variants | Theme/fantasy isn't appealing → **pivot concept**; test concepts with thumbnails/ads *before* building |
| Strong early spike then collapse (trend game) | **Iterate fast** (weekly updates, events) or accept the short life, and ship the next trend game using the same codebase |

Relaunch mechanics: a big update with a new name, icon and "[UPDATE]" or "[NEW]" tag on the same place keeps favorites, visit count and Continue-Play users. A brand-new place gets a clean slate in recommendations but zero social proof. Default: **relaunch in place** unless the game has moderation history or a toxic reputation.

## Checklist
- [ ] Analytics in place before launch ([[Analytics-And-Instrumentation]])
- [ ] Kill switches and `maintenance_message` config exist
- [ ] Previous place version number recorded per release
- [ ] Restore script tested in staging against real versioned keys
- [ ] Compensation item/currency pre-built (giftable via admin command)
- [ ] Incident comms template ready (Discord plus in-game banner)

## Pitfalls
- Changing everything at once makes it impossible to learn what helped.
- Buying ads with D1 < 8% wastes money.
- A full data rollback wipes legitimate progress and purchases. Robux purchases made during the window must be **re-granted** (check your receipt ledger, [[Data-Persistence-DataStores-And-ProfileStore]]).
- Silence during an incident does more lasting harm than the incident itself.
- Hourly versioning means writes within the same UTC hour overwrite each other, so the granularity is at best 1 h.

## Related
- [[Operations/_Index]] · [[KPI-Dashboard-Spec]] · [[Live-Ops-Playbook]] · [[Post-Mortems-Real-Games]] · [[AB-Testing]]
- [[Launch-Checklist]] · [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]] · [[Conversion-Funnels]] · [[Growth-Metrics-And-Benchmarks]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Content-Cadence]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `cloud-services/data-stores/versioning-listing-and-caching.md` (hourly versioning, 30-day expiry), `reference/engine/classes/DataStore.yaml` (`ListVersionsAsync`, `GetVersionAtTimeAsync`, `ListKeysAsync`), `projects/update-games.md`, `production/analytics/acquisition.md`, `analytics-dashboard.md` (benchmarks). Checked 2026-10-04.
- Roblox DataStores incident report (platform-side data loss example): https://devforum.roblox.com/t/datastores-incident-report/829962
- Benchmarks: https://devforum.roblox.com/t/analytics-similar-experience-benchmarks-broader-access/2210285 ; GameAnalytics 2026 Roblox report https://www.gameanalytics.com/reports/2026-roblox-report (search snippet: median D1 10.3% across 500+ experiences with ≥1M MAU, Aug 2025–Jul 2026; ⚠️ verify by reading the report)
