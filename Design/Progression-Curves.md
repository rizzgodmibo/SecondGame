---
tags: [design/progression]
status: draft
updated: 2026-10-04
confidence: medium
---
# Progression Curves

## TL;DR
- Pick the curve by purchase type:
  - **Exponential** `cost = base·r^n` for infinitely repeatable upgrades and generators (r = 1.07–1.15).
  - **Polynomial** `xp = a·L^k` for levels (k = 1.5–2.2). It keeps late levels reachable.
  - **Geometric gates** (×4–×10 per zone) for area/egg tiers.
  - **Logistic** for anything with a hard cap (power vs. time to a level cap).
- Tune by **time-to-next-upgrade (TTN) = cost ÷ income**, not by raw prices. Targets: ≤ 20 s in minute 0–5, ≤ 90 s in minutes 5–30, ≤ 5 min in hours 1–2. Let TTN creep up to a **wall**, then hand players a new system or a rebirth ([[Prestige-And-Rebirth]]).
- Costs grow exponentially while income grows roughly linearly per unit. The resulting TTN climb, `r^n / n`, is the pacing engine. Periodic milestone multipliers (×2 at 25/50/100 owned) reset it into a sawtooth.
- Display big numbers with suffixes (K, M, B, T, Qa, Qi, Sx…) and **floor, never round up**, so "1M" never shows when the player has 999,999. Code below.
- Lua numbers are doubles. Integer precision ends at 2^53 ≈ 9.0 Qa, and they overflow at ~1.8e308. Plan the late game below ~1e300, or switch to a mantissa/exponent representation.

## Curve families

| Curve | Formula | Growth feel | Use for | Avoid for |
|---|---|---|---|---|
| Linear | `c(n) = a + b·n` | gets *easier* relative to income | tutorial steps, fixed-price cosmetics | anything income scales against |
| Polynomial | `c(n) = a·n^k` | slows down relative to exponential income | XP per level, quest requirements | idle generators (too flat) |
| Exponential | `c(n) = base·r^n` | always outruns linear income → walls | generators, upgrade levels, rebirth cost | levels with a fixed cap (too steep) |
| Geometric tiers | `gate(z) = g0·m^z`, m = 4–10 | big jumps between content blocks | area doors, egg tiers, worlds | small repeat purchases |
| Logistic (S-curve) | `P(t) = Pmax / (1 + e^{-k(t - t0)})` | slow start, fast middle, plateau | power vs. time to a cap, mastery | endless incremental games |

### Exponential cost math (idle/simulator standard)
From Kongregate's idle-math series (AdVenture Capitalist lemonade stand: base 4, r = 1.07):
- Next unit cost with `k` owned: `c_k = base · r^k`
- Cost to buy `n` more: `C = base · r^k · (r^n − 1) / (r − 1)`
- Max affordable with currency `M`: `n_max = floor( log_r( M·(r − 1) / (base·r^k) + 1 ) )`
- Income with `k` units at `p` per unit: `I = p · k · multipliers`

### Worked table: base 10, r = 1.15, each unit yields 1/s, no multipliers
| Owned n | Cost of next | Income/s (n·1) | TTN (s) |
|---|---|---|---|
| 1 | 11.5 | 1 | 11.5 |
| 5 | 20.1 | 5 | 4.0 |
| 10 | 40.5 | 10 | 4.0 |
| 20 | 163.7 | 20 | 8.2 |
| 30 | 662.1 | 30 | 22.1 |
| 40 | 2,678.6 | 40 | 67.0 |
| 50 | 10,836.6 | 50 | 216.7 |
| 100 | 11,743,134 | 100 | ~32 h (wall) |

Reading it: the curve feels great up to n ≈ 30 and hits a wall around 45–50. Insert a ×2 milestone at 25/50, a second generator tier (base ×12, yield ×8) around n ≈ 25, or a rebirth around n ≈ 45. Buying 10 from zero costs `10·(1.15^10 − 1)/0.15 ≈ 203`.

Picking r:
- **1.07**: slow wall. Suits many generators bought in bulk (AdCap).
- **1.10–1.12**: typical simulator upgrades.
- **1.15**: Cookie Clicker–style buildings, with walls arriving fast ⚠️ verify: exact Cookie Clicker multiplier (widely cited as 1.15).
- **≥ 1.25**: a deliberate hard cap on repeat purchases, e.g. a "backpack size" upgrade line you want to end in about 20 steps.

### Polynomial level curve: XP(L) = 100·L^1.5
| Level | XP for this level | Cumulative XP |
|---|---|---|
| 1 | 100 | 100 |
| 2 | 283 | 383 |
| 5 | 1,118 | 2,820 |
| 10 | 3,162 | 14,267 |
| 20 | 8,944 | 76,080 |
| 50 | 35,355 | 724,870 |
| 100 | 100,000 | 4,050,122 |

If the XP/min players earn rises with level (better zones), the time per level stays nearly flat, which is the goal for levels. Roblox's onboarding guidance agrees: keep early thresholds low so new players level up immediately. Tune these values live with Configs.

### Logistic power curve (capped games)
`P(t) = Pmax / (1 + e^{−k(t − t0)})`. Set `t0` to the hour when you want half of max power, and `k ≈ 4 / (duration of the steep middle)`. Example: Pmax 2,800 levels, half reached at 40 h, steep middle lasting 40 h → k = 0.1. Blox Fruits–style grinders behave roughly like this. Max level goes up with each update, which pushes Pmax and t0 out.

## Time-to-next-upgrade (TTN) targets
These are vault heuristics from idle/simulator practice. Validate them with [[Balancing-Methods]].

| Phase of player life | Target TTN | Target "big moment" (new zone/egg/tower) |
|---|---|---|
| Minute 0–1 | 5–15 s (first reward ≤ 15 s) | first upgrade bought in ≤ 60 s |
| Minute 1–5 | 10–30 s | first new area/egg by minute 3–5 |
| Minute 5–30 | 30–90 s | every 5–8 min |
| Hour 0.5–2 | 1–5 min | every 10–20 min; first rebirth by ~30–60 min |
| Day 2–7 | 5–20 min | 1–2 per session; rebirth tiers |
| Week 2+ | sessions, not minutes | weekly update content ([[Content-Cadence]]) |

Decision rules:
- If median TTN in telemetry is **over 2× target** for that phase, drop `base` by 30–50% or add a multiplier source. If it is **under 0.5×**, the content will burn out. Raise `r` by 0.01–0.02.
- Set zone gates at **8–15 minutes of income at that zone's expected multiplier**, so each zone lasts one "beat" ([[Session-Length-And-Pacing]]).
- A wall is acceptable only when the player can see the tool that breaks it: rebirth, a new system, an upgrade shop, or a paid boost ([[Gamepasses-vs-Developer-Products]]).

## Geometric zone gates: worked example
Gate out of zone z costs `500·m^(z−1)` with m = 6. Players carry ×3.5 more income into each new zone (pets + upgrades).

| Zone | Income/s on arrival | Gate to next zone | Minutes in zone |
|---|---|---|---|
| 1 | 1 | 500 | 8.3 |
| 2 | 3.5 | 3,000 | 14.3 |
| 3 | 12.25 | 18,000 | 24.5 |
| 4 | 42.9 | 108,000 | 42.0 |

Each zone takes 6 / 3.5 = 1.71× longer than the last. Rule: **minutes per zone grow by m ÷ (income step)**. For constant pacing, set m = the income step (3.5). For a gentle slowdown, set m = 1.1–1.3 × the income step. Accept steep growth only right before a rebirth wall.

## Big number formatting
Short-scale suffixes: K 1e3, M 1e6, B 1e9, T 1e12, Qa 1e15, Qi 1e18, Sx 1e21, Sp 1e24, Oc 1e27, No 1e30, Dc 1e33, then Ud, Dd, Td, Qad, Qid, Sxd, Spd, Ocd, Nod (1e60), Vg (1e63).

Precision facts:
- Doubles hold every integer exactly up to 2^53 = 9,007,199,254,740,992 (≈ 9.0 Qa). Beyond that, adding a small number to a large one can be lost (1e17 + 1 == 1e17).
- Max double ≈ 1.797e308. Past that you get `inf`.
- Above ~1e15, store currency as numbers and accept the float error, or store `{m: number, e: number}` (mantissa/exponent). Never store as strings you parse every frame.

```lua
--!strict
-- ReplicatedStorage/Shared/NumberFormat.lua
-- Formats large numbers for UI. Floors (never rounds up) so displayed value <= true value.
local NumberFormat = {}

local SUFFIXES: { string } = {
	"", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc",
	"Ud", "Dd", "Td", "Qad", "Qid", "Sxd", "Spd", "Ocd", "Nod", "Vg",
}

local function stripZeros(s: string): string
	if string.find(s, ".", 1, true) == nil then
		return s
	end
	local trimmed = (string.gsub(s, "0+$", ""))
	trimmed = (string.gsub(trimmed, "%.$", ""))
	return trimmed
end

local function floorTo(x: number, decimals: number): number
	local f = 10 ^ decimals
	-- small epsilon guards against 1.15*100 = 114.99999999
	return math.floor(x * f + 1e-9) / f
end

function NumberFormat.abbreviate(n: number, decimals: number?): string
	local d: number = decimals or 2
	if n ~= n then
		return "NaN"
	elseif n == math.huge then
		return "∞"
	elseif n == -math.huge then
		return "-∞"
	end

	local sign = if n < 0 then "-" else ""
	local a = math.abs(n)

	if a < 1000 then
		return sign .. stripZeros(string.format("%." .. d .. "f", floorTo(a, d)))
	end

	local tier = math.floor(math.log10(a) / 3)
	-- correct floating log10 error at exact powers (log10(1000) may be 2.9999999)
	if a >= 10 ^ ((tier + 1) * 3) then
		tier += 1
	elseif a < 10 ^ (tier * 3) then
		tier -= 1
	end

	if tier + 1 > #SUFFIXES then
		return sign .. string.format("%.2e", a)
	end

	local scaled = floorTo(a / 10 ^ (tier * 3), d)
	if scaled >= 1000 and tier + 2 <= #SUFFIXES then
		tier += 1
		scaled = floorTo(scaled / 1000, d)
	end

	return sign .. stripZeros(string.format("%." .. d .. "f", scaled)) .. SUFFIXES[tier + 1]
end

-- 1234567 -> "1,234,567" (use below 1e6 where exact values matter, e.g. prices)
function NumberFormat.commas(n: number): string
	local s = string.format("%d", math.floor(n))
	local sign = ""
	if string.sub(s, 1, 1) == "-" then
		sign = "-"
		s = string.sub(s, 2)
	end
	local out = (string.reverse((string.gsub(string.reverse(s), "(%d%d%d)", "%1,"))))
	if string.sub(out, 1, 1) == "," then
		out = string.sub(out, 2)
	end
	return sign .. out
end

-- Cost helpers (shared so client previews match server truth)
function NumberFormat.nextCost(base: number, r: number, owned: number): number
	return base * r ^ owned
end

function NumberFormat.bulkCost(base: number, r: number, owned: number, count: number): number
	return base * r ^ owned * (r ^ count - 1) / (r - 1)
end

function NumberFormat.maxAffordable(base: number, r: number, owned: number, money: number): number
	local x = money * (r - 1) / (base * r ^ owned) + 1
	if x <= 1 then
		return 0
	end
	return math.floor(math.log(x) / math.log(r) + 1e-9)
end

return NumberFormat
```
Expected outputs: `abbreviate(999999)` → "999.99K", `abbreviate(1e6)` → "1M", `abbreviate(1234567890)` → "1.23B", `abbreviate(2.5e15)` → "2.5Qa", `commas(1234567)` → "1,234,567".

Purchases are **validated on the server** with the same `bulkCost`. The client value is only a preview ([[Anti-Exploit-And-Server-Authority]]).

## Checklist
- [ ] For each upgrade line, choose the curve family from the table and record base, r or k in the GDD
- [ ] Build a TTN table for minutes 0–120 in a spreadsheet ([[Balancing-Methods]]) and check it against the targets
- [ ] Put milestone multipliers or new tiers before each predicted wall
- [ ] Keep the late-game ceiling below 1e300, or adopt mantissa/exponent storage
- [ ] Use `NumberFormat` everywhere. No ad-hoc `tostring(math.floor(x))` in UI
- [ ] Log TTN-related funnel steps (first upgrade, first zone, first rebirth) ([[Analytics-And-Instrumentation]])

## Pitfalls
- **Rounding up in UI**: "1M" shown with 999,999 in the bank makes players think the purchase button is broken.
- **Exponential levels**: XP = 100·1.2^L makes level 60 require ~5.6M XP for a single level, which is an unintentional hard cap.
- **Linear income against exponential costs with no new multiplier source**: a guaranteed wall at ~TTN 5 min that players read as "game over".
- **Too many suffixes too fast**: hitting "Qa" in session 1 numbs players to big numbers. Aim to reach B–T by the first rebirth.
- **Floating point in equality checks**: compare `money >= cost - 1e-6` server-side, or round costs to integers when < 2^53.

## Related
- [[Core-Loops]] · [[Prestige-And-Rebirth]] · [[Idle-And-Offline-Earning]] · [[Balancing-Methods]] · [[Economy-Design-Sinks-And-Faucets]]
- [[Session-Length-And-Pacing]] · [[Onboarding-And-First-60-Seconds]] · [[Anti-Exploit-And-Server-Authority]] · [[Gamepasses-vs-Developer-Products]]

## Sources
- Anthony Pecorella, "The Math of Idle Games, Part I" (Kongregate): https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i
- Pecorella, "Quest for Progress: The Math and Design of Idle Games" (GDC Europe 2016): https://www.gdcvault.com/play/1023876/Quest-for-Progress-The-Math
- Idle game worksheets: https://archive.org/details/idlegameworksheets
- Roblox Creator Docs, Onboarding (low early XP thresholds, Configs): https://create.roblox.com/docs/production/game-design/onboarding (read 2026-10-04)
- Blox Fruits max level 2,800: https://www.sportskeeda.com/roblox-news/what-max-level-blox-fruits
- IEEE-754 double precision (2^53 integer limit) is standard numeric behaviour; Luau numbers are doubles.
