---
tags: [design/progression, design/prestige]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prestige and Rebirth

## TL;DR
- Unlock rebirth **when time-to-next-upgrade (TTN) passes ~3–5 min and the player has cleared 3+ zones/tiers**. In practice that is the first 30–60 min of play. Show the rebirth button, grayed out with its requirement, from minute ~5 so players know it exists.
- A rebirth must make the next run **visibly faster**. Target: the player re-reaches their old wall in **≤ 40% of the previous run's time**, then pushes 1–2 zones further.
- Match the multiplier growth to the cost growth. Cost ×g per rebirth with multiplier ×m per rebirth gives run lengths that grow ×(g/m) per rebirth. Choose g/m ≈ 1.05–1.15. A **linear multiplier against an exponential cost explodes** by rebirth 4–5.
- **Reset**: the run currency and its upgrades. **Keep**: collection (pets/units), cosmetics, gamepass perks, rebirth-tier unlocks, quests/achievements. Never reset anything bought with Robux.
- Add a second prestige layer (Super Rebirth / Ascension) once players reach the first layer's soft cap, and add new layers in updates ([[Content-Cadence]]).

## Why rebirth works
- It turns a wall (exponential cost overtaking income, see [[Progression-Curves]]) into a **choice**: keep grinding slowly, or reset for a permanent multiplier.
- It replays the best part of the game (the fast early ramp) at a higher speed. It is cheap content, often 10–20 hours of play from existing zones.
- It gives the meta loop a counter (Rebirths: 12) that works as a status symbol on leaderboards and overhead tags ([[Core-Loops]]).

## When to unlock: decision rules
| Signal | Unlock rebirth when… |
|---|---|
| TTN | median TTN in the current zone > 3–5 min ([[Progression-Curves]]) |
| Content seen | player has visited ≥ 3 zones or bought ≥ 3 egg tiers |
| Time | first rebirth affordable at **30–60 min** cumulative playtime (simulators); 2–4 h (deeper RPG/idle) |
| Comprehension | player understands the loop (onboarding funnel complete) |

Pet Simulator 99's community guides describe the mid-game rhythm as "push to the area you can no longer break, rebirth, return much faster, push 1–2 areas further". PS99 also gates rebirths by area and added a **Super Rebirth** layer in Update 87. ⚠️ verify: PS99 rebirth counts (fan wiki states max 9 as of Update 79).

## Multiplier formulas
| Model | Formula | Feel | Use |
|---|---|---|---|
| Linear per rebirth | `M = 1 + a·R` (a = 0.25–1.0) | readable ("+50% per rebirth") | only with **linear/polynomial** rebirth costs |
| Multiplicative per rebirth | `M = m^R` (m = 1.5–3) | big numbers, sim-friendly | with exponential rebirth costs |
| Prestige currency (lifetime-based) | `P = floor(k·(E_life / E0)^(1/q))`, q = 2–3, then `M = 1 + b·P` | rewards longer runs, self-balancing | idle/incremental |
| Hybrid tier unlocks | `M` plus a new feature at rebirth 1, 3, 5, 10… | adds novelty, not just numbers | all genres; strongly recommended |

Cookie Clicker's heavenly chips use a cube-root relationship to cookies baked. ⚠️ verify: exact formula in the current version.

### Run-length law
If rebirth R costs `C_R = C0·g^R` and income at rebirth R is `I0·M_R`, the time to afford the next rebirth is roughly `T_R ≈ C_R / (I0·M_R)`.

**Naive (bad): g = 3, M = 1 + 0.75R, C0 = 100k, I0 = 50/s**
| R | Cost | Mult | Run (min) |
|---|---|---|---|
| 0 | 100,000 | 1.0 | 33 |
| 1 | 300,000 | 1.75 | 57 |
| 2 | 900,000 | 2.5 | 120 |
| 3 | 2.7M | 3.25 | 277 |
| 4 | 8.1M | 4.0 | 675 (dead) |

**Balanced (good): g = 2, M = 1.8^R, C0 = 100k, I0 = 50/s**
| R | Cost | Mult | Run (min) |
|---|---|---|---|
| 0 | 100K | 1.0 | 33 |
| 2 | 400K | 3.24 | 41 |
| 4 | 1.6M | 10.5 | 51 |
| 6 | 6.4M | 34.0 | 63 |
| 8 | 25.6M | 110 | 77 |
| 10 | 102.4M | 357 | 96 |

g/m = 2/1.8 = 1.11, so each run is ~11% longer than the last. Ten rebirths come to ~10.5 h of play, which is a week of D7 content for an engaged player. Real runs are shorter than `T_R` because in-run upgrades also compound. Simulate it ([[Balancing-Methods]]).

### Optimal reset point (prestige-currency games)
Reset when **prestige earned per minute of run, `P(t)/(t + overhead)`, peaks**. Example: `P = √(E/1e6)`, 2 min overhead, earnings slow after a 40-min wall:

| Run time | Earnings | P | P per min |
|---|---|---|---|
| 20 | 8M | 2.83 | 0.129 |
| 30 | 27M | 5.20 | 0.162 |
| **40** | **64M** | **8.00** | **0.190 (reset here)** |
| 60 | 90M | 9.49 | 0.153 |
| 90 | 110M | 10.49 | 0.114 |

Show players a "Rebirth now: +8 ★ (best rate)" hint once P/min starts falling. Experts enjoy optimising this. Casual players need the hint.

## What resets vs. persists
| Category | Default | Notes |
|---|---|---|
| Run currency (coins/cash) | **Reset** | the point of the system |
| Upgrades bought with run currency | **Reset** | |
| Zones/areas unlocked | **Reset** (or keep the first N as a rebirth perk) | keeping early zones avoids re-walking tutorial content |
| Pets/units/towers (collection) | **Keep** | resetting the collection kills retention and trading |
| Premium currency (gems) | **Keep** | |
| Anything bought with Robux | **Always keep** | resetting paid items = refunds and rage ([[Gamepasses-vs-Developer-Products]]) |
| Cosmetics, titles, badges | **Keep** | |
| Rebirth count + multiplier | **Keep** (it *is* the reward) | |
| Quests/achievements/index | **Keep** | |
| Pity counters | **Keep** | ([[Reward-Schedules]]) |
| Offline-earning accumulator | settle *before* reset | otherwise players lose earnings ([[Idle-And-Offline-Earning]]) |

## Rebirth UX
- Show a confirmation screen with **before/after**: "You lose: 4.2M coins, 7 upgrades, Zones 2–5. You keep: 38 pets, gems. You gain: ×1.8 coins (→ ×5.83 total), unlocks Auto-Collect."
- Play a celebration VFX and SFX, update the overhead rebirth tag, and announce server-wide at milestones (10, 25, 50, 100). This creates a social moment.
- Offer a "Rebirth skip"/"+1 rebirth" developer product only if it doesn't break the multiplier economy. Price it from the hours it saves. Gate it behind the first manual rebirth.
- Save immediately after a rebirth, because it is a high-value state change ([[Data-Persistence-DataStores-And-ProfileStore]]).

## Server-side rebirth handler sketch
```lua
--!strict
-- ServerScriptService/RebirthService.server.lua (data access abstracted; plug into your ProfileStore wrapper)
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local C0, G, M_STEP = 100_000, 2, 1.8

type Data = { coins: number, rebirths: number, upgrades: { [string]: number }, zone: number }
local getData: (Player) -> Data? = function(_p) return nil end -- replace with profile lookup

local function rebirthCost(r: number): number
	return C0 * G ^ r
end

local function multiplier(r: number): number
	return M_STEP ^ r
end

local remote = Instance.new("RemoteFunction")
remote.Name = "RequestRebirth"
remote.Parent = ReplicatedStorage

remote.OnServerInvoke = function(player: Player): (boolean, number?)
	local data = getData(player)
	if not data then
		return false, nil
	end
	local cost = rebirthCost(data.rebirths)
	if data.coins < cost then
		return false, nil -- server is the authority; never trust a client "canRebirth"
	end
	data.rebirths += 1
	data.coins = 0
	data.upgrades = {}
	data.zone = 1
	return true, multiplier(data.rebirths)
end
```

## Checklist
- [ ] Pick a multiplier model and check g/m ≈ 1.05–1.15 in the sheet
- [ ] First rebirth affordable at 30–60 min for a median player (telemetry funnel step "Rebirth 1")
- [ ] Reset/persist table written into the GDD; paid items always persist
- [ ] Confirmation UI with before/after and a "best time to rebirth" hint
- [ ] A new feature unlock at rebirth 1, 3, 5, 10
- [ ] Second layer designed (unlock at ~rebirth 10–25) and kept in the backlog

## Pitfalls
- Linear multiplier with exponential cost, which dead-ends at ~rebirth 4.
- Rebirth resetting pets or other collection items, which destroys trading value and retention.
- Rebirth that isn't faster: if re-reaching the old wall takes > 60% of the previous run, players feel punished.
- Unlocking rebirth too early (< 10 min), before players value what they lose.
- Hidden requirements. Always show the cost and progress toward it on the HUD.

## Related
- [[Progression-Curves]] · [[Core-Loops]] · [[Economy-Design-Sinks-And-Faucets]] · [[Balancing-Methods]] · [[Idle-And-Offline-Earning]]
- [[Reward-Schedules]] · [[Genre-Playbooks]] · [[Gamepasses-vs-Developer-Products]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Anti-Exploit-And-Server-Authority]]

## Sources
- Pecorella, Math of Idle Games (prestige design): https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i ; Part III: https://blog.kongregate.com/the-math-of-idle-games-part-iii/amp/
- Pet Simulator 99 Rebirth (fan wiki): https://pet-simulator.fandom.com/wiki/Rebirth_(Pet_Simulator_99)
- BIG Games, PS99 Update 87 (Super Rebirth): https://www.biggames.io/post/pet-simulator-99-update-87
- PS99 rebirth cadence guide: https://bloxtoolbox.com/pages/guides/pet-sim-99-rebirth.html
