---
tags: [design/economy]
status: draft
updated: 2026-10-04
confidence: medium
---
# Economy Design: Sinks and Faucets

## TL;DR
- Model the economy as **faucets (currency in) vs. sinks (currency out) per player-hour**. Target a sink ratio `S/F` of **0.7–0.95** for soft currency. Below ~0.6, prices stop meaning anything (inflation). Above 1.0, players feel poor and churn.
- Use **2–3 currencies max at launch**:
  - **soft** (earned, inflationary by design, reset by rebirth),
  - **premium/hard** (gems; scarce, earnable slowly, also sold),
  - optionally a **time-limited event** currency that expires or converts.
  Every currency has a written purpose, a faucet list and a sink list.
- **Exponential progression games inflate by design.** Control it with resetting sinks (rebirth), consumables and new tiers, not by fighting the numbers ([[Progression-Curves]], [[Prestige-And-Rebirth]]).
- **Trading economies multiply retention and risk.** Every tradable item needs a unique ID, atomic server-side trades on session-locked profiles, and audit logs. One dupe can collapse the value of a whole collection ([[Data-Persistence-DataStores-And-ProfileStore]]).
- Check `PolicyService` `IsPaidItemTradingAllowed`. Players for whom it is false must not trade items obtained with Robux or with currency bought with Robux.

## Currency architecture
| Currency | Purpose | Faucets | Sinks | Resets on rebirth? | Sold for Robux? |
|---|---|---|---|---|---|
| Soft (Coins/Cash) | moment-to-moment progress | core loop, offline, quests | upgrades, eggs, zone gates | yes | indirectly (boosts); selling it directly is cheap and devalues grind |
| Premium (Gems/Diamonds) | cross-run progress, convenience | dailies, achievements, rare drops, purchase | premium eggs, slots, rerolls, cosmetics | no | yes (dev products) ([[Gamepasses-vs-Developer-Products]]) |
| Event tokens | live-ops engagement | event activities only | event shop | expires or converts at event end | sometimes (passes) |
| Social/rank (Trophies, Stars) | status, matchmaking | wins, ratings | none (not spent) or cosmetic | no | never |

Decision rule: add a currency only if it creates **a new decision**. Three currencies that all buy "+stats" is just a spreadsheet chore.

## Faucets (catalogue)
- Core action payout (click, kill, harvest, sell)
- Passive/idle income and offline earnings ([[Idle-And-Offline-Earning]])
- Quests/missions, achievements, index completion
- Daily rewards, streaks, playtime gifts ([[Daily-Rewards-And-Streaks]])
- Event rewards, codes, group-join rewards
- Selling items back to NPC (also a sink for *items*)
- Purchases (premium only)
- Trading **does not create value**. It moves it. Dupes and exploits are unplanned faucets.

## Sinks (catalogue)
| Sink | Type | Strength | Notes |
|---|---|---|---|
| Upgrades with exponential cost | permanent progression | strong | the main soft sink |
| Zone/door gates | progression | strong, one-time | |
| Eggs/crates (random) | gamble-like | very strong | odds rules if paid ([[Reward-Schedules]]) |
| Rebirth (resets wallet) | reset | strongest for soft | |
| Consumables (potions, boosts, fertiliser, ammo) | consumption | steady, repeatable | best long-term sink |
| Crafting/fusing (5 commons → 1 rare) | item sink | strong for item supply | key to collection economies |
| Repair/upkeep, durability | upkeep | disliked; use sparingly | |
| Trading tax (5–10%) / listing fees | transaction | medium | also slows bot/alt trading |
| Cosmetics, housing, decor | vanity | unlimited ceiling | good for late-game wealth |
| Re-rolls (traits, enchant, stats) | gamble | very strong | odds disclosure if paid |
| Leaderboard donations/"burn for rank" | status | niche | |
| Event shops with expiring currency | time-limited | strong, controllable | |

## Spreadsheet model (minimum viable)
Rows are player-hours (0, 0.5, 1, 2, 4, 8, 16, 32…) along an expected median path. Columns:

| Column | Formula |
|---|---|
| `income/h` | Σ faucet rates at this stage (from [[Progression-Curves]]) |
| `spend/h` | Σ sink purchases the median player makes at this stage |
| `wallet` | previous wallet + income − spend |
| `sink ratio` | spend / income (target 0.7–0.95) |
| `wallet ÷ next big price` | how close the next goal is (target 0.3–0.8 most of the time) |
| `premium earned/h (free)` | free gem drip, e.g. 50–150 gems/day ⚠️ verify: compare with your premium price points |
| `items created/h` and `items destroyed/h` | per rarity, for item economies |

Worked example: hour 2. Faucets 1.8M/h. Upgrades 1.2M, eggs 0.4M, potions 0.1M → spend 1.7M → sink ratio 0.94 ✅. Hour 6: faucets 40M/h, spend 18M → ratio 0.45 ❌. Wallets pile up and nothing feels expensive. Fix: insert the next egg tier at hour 5 (cost ~15M each) or a consumable that scales with income (potion price = 5 min of income).

**Income-scaled sinks** (price = k × current income/s) never go stale. Use them for consumables and rerolls.

## Inflation: signals and fixes
| Signal (telemetry) | Meaning | Fix |
|---|---|---|
| median wallet / price of next upgrade > 3 | sinks too weak | new tier, consumables, rebirth incentive |
| traded item values rising across the board | currency debasement or dupes | audit faucets/dupes; add item sinks (fusing) |
| top 1% wallets ≫ 100× median | runaway compounding | soft caps, diminishing returns on stacking multipliers |
| premium stock per player rising and unspent | premium sinks too few | new premium sink (slots, limited cosmetics) |
| players hoarding event currency at event end | event shop weak | better items; announce conversion rate |

Deflation (prices rise faster than income) shows up as TTN spikes and quit-after-purchase-fail. Treat it with the [[Progression-Curves]] TTN rules.

## Trading economies
Top Roblox examples: Adopt Me (pets), Pet Simulator 99 (pets incl. Huges/Titanics), Blox Fruits (fruits), Murder Mystery 2 (knives/guns), Grow a Garden (pets/fruit). Trading creates:
- **Retention**: a meta goal that never ends (value climbing) and community value lists.
- **Acquisition**: trading content on YouTube/TikTok.
- **Risk**: scams, dupes, real-money trading (RMT), and policy exposure for items obtained with Robux.

Design rules:
1. **Unique item IDs** (`HttpService:GenerateGUID(false)`) for every tradable instance. Stackables track counts only if they are low value.
2. **Atomic trades on one server**: both players are in the same server with session-locked profiles. Remove from A and add to B in one step, then save both. Never trade across servers through plain DataStore writes without a transactional design.
3. **Two-step confirm**: both accept → 5 s countdown → re-confirm. Any change resets the countdown (anti-bait-and-switch).
4. **Trade log**: every trade (ids, both user ids, timestamp, server job id) goes to an append-only store, for dupe forensics and rollbacks ([[Analytics-And-Instrumentation]]).
5. **Gating**: minimum playtime/account age before trading, a per-day trade limit, and a fresh-hatch untradeable period (e.g. 24 h) to slow alt farming. ⚠️ verify: whether any Roblox policy mandates account-age gating (believed not; it is a design choice).
6. **Policy**: honour `IsPaidItemTradingAllowed` per player for paid items. Never let items be sold for Robux off-platform (ToS) ([[Gamepasses-vs-Developer-Products]]).
7. **Dupe detection**: periodic scan of trade logs for the same GUID owned by two users. Auto-freeze the newer copy.

The classic dupe: a player trades, then rejoins quickly so an older save overwrites the newer data. The partner keeps the items and the duper gets theirs back. Session locking plus saving both profiles right after the trade closes it ([[Data-Persistence-DataStores-And-ProfileStore]], [[Anti-Exploit-And-Server-Authority]]).

```lua
--!strict
-- ServerScriptService/Economy/TradeCommit.lua (ModuleScript). Both profiles must be loaded + session-locked in THIS server.
local TradeCommit = {}

export type Item = { uid: string, kind: string, tradeLockUntil: number }
export type Inventory = { items: { [string]: Item } } -- keyed by uid

-- Returns false without mutating anything if any offered item is missing or locked.
function TradeCommit.commit(a: Inventory, b: Inventory, aOffer: { string }, bOffer: { string }): boolean
	local now = os.time()
	for _, uid in aOffer do
		local it = a.items[uid]
		if not it or it.tradeLockUntil > now then
			return false
		end
	end
	for _, uid in bOffer do
		local it = b.items[uid]
		if not it or it.tradeLockUntil > now then
			return false
		end
	end
	-- validation passed: mutate (single-threaded Luau; no yield between checks and writes)
	for _, uid in aOffer do
		b.items[uid] = a.items[uid]
		a.items[uid] = nil
	end
	for _, uid in bOffer do
		a.items[uid] = b.items[uid]
		b.items[uid] = nil
	end
	return true -- caller: log trade, then force-save both profiles immediately
end

return TradeCommit
```

## Checklist
- [ ] Currency table (purpose, faucets, sinks, reset, sold?) in the GDD ([[Game-Design-Doc-Template]])
- [ ] Spreadsheet with sink ratio per player-hour; every stage between 0.7 and 0.95
- [ ] At least one income-scaled consumable sink
- [ ] Item economy: created vs. destroyed per rarity per day tracked
- [ ] Trading: GUIDs, atomic commit, countdown confirm, trade log, gating, PolicyService checks
- [ ] Weekly dashboard: median wallet / next price, top-1% wallet, trade volume ([[Analytics-And-Instrumentation]])

## Pitfalls
- Adding faucets in every update (bigger event rewards) without matching sinks. That is the slow-inflation death spiral.
- Selling soft currency for Robux at prices that make grinding pointless.
- Making premium currency too easy to earn, so there is no reason to buy, or impossible, so free players see a paywall.
- Launching trading before data persistence is battle-tested. Dupes in week 1 poison the economy permanently.
- Rollbacks that wipe innocent trade partners' items. Prefer targeted removal using trade logs.

## Related
- [[Progression-Curves]] · [[Prestige-And-Rebirth]] · [[Reward-Schedules]] · [[Idle-And-Offline-Earning]] · [[Balancing-Methods]] · [[Core-Loops]]
- [[Gamepasses-vs-Developer-Products]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Anti-Exploit-And-Server-Authority]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Daily-Rewards-And-Streaks]]

## Sources
- Roblox Creator Docs, Paid random items (IsPaidItemTradingAllowed, ArePaidRandomItemsRestricted): https://create.roblox.com/docs/production/monetization/paid-random-items (read 2026-10-04)
- DevForum, Preventing duplication glitches in your game: https://devforum.roblox.com/t/preventing-duplication-glitches-in-your-game/288916
- DevForum, Trading Dupe Glitch: https://devforum.roblox.com/t/trading-dupe-glitch/1026853
- Pecorella, Math of Idle Games: https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i
