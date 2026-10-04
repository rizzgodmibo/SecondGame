---
tags: [design/onboarding]
status: draft
updated: 2026-10-04
confidence: medium
---
# Onboarding and the First 60 Seconds

> The vault's **single home** for onboarding / FTUE / first session. Other notes link here instead of repeating it.

## TL;DR
- Roblox ranks games on **first-play bounce rate**, the share of new players who leave after a short first session, measured over a **61–180 s** window. It is in the "most important" signal tier. The first 60 seconds decide your discovery ([[Discovery-Algorithm]]).
- **Spawn → first action ≤ 5 s, first reward ≤ 15 s, first full loop (earn → spend → see effect) ≤ 60 s.** No menus, popups, shop, daily-reward modal or update log before the first reward.
- **One button first.** The first action is a single obvious input (tap/click a glowing thing, or walk into a pad) that works identically on touch, mouse and controller.
- Teach with **visuals, not text**:
  - bouncing arrows, glowing trails, in-world signs;
  - **contextual tutorials** when a feature is first met;
  - **timed hints** that appear only after most players would have succeeded (e.g. 11 s when 90% succeed within 10 s).
- Instrument every step with `AnalyticsService:LogOnboardingFunnelStepEvent` from the server. Fix the biggest leak first, A/B test with Experiments, ship the winner with Configs.

## What the platform measures
| Signal | Window | Direction | Source |
|---|---|---|---|
| Play-through rate (impression → play) | — | higher is better | thumbnail/title ([[Discovery-Algorithm]]) |
| **First play bounce rate** | 61–180 s average rate | **negative signal** | the first minutes of your FTUE |
| Playtime per user | capped 60 min/user/game/day | higher is better | [[Session-Length-And-Pacing]] |
| Play days per user (D1, D2–7, D8–28) | — | higher is better | [[Retention-Metrics-D1-D7-D30]] |

Roblox's onboarding guidance names **D1 retention** and **onboarding-goal completion** as the success metrics of an FTUE.

## Before the first second: promise and loading
- **Metadata promise = spawn view.** The thumbnail and title must match what's on screen at spawn. Mismatched metadata is explicitly de-prioritised in recommendations.
- **Loading**:
  - Use a `ReplicatedFirst` loading screen that shows the game's art and a progress bar. Keep custom loading ≤ 5 s on mid-range mobile.
  - Preload only what's visible at spawn. Stream the rest (StreamingEnabled).
  - Players who fail to load within 120 s get kicked. ⚠️ verify: the 120 s join timeout (DevForum report, old) still applies.
- **Skip button** on any intro or cutscene after 2 s. Better: no cutscene at all.

```lua
--!strict
-- ReplicatedFirst/LoadingScreen.client.lua — minimal, fast, skippable
local ReplicatedFirst = game:GetService("ReplicatedFirst")
local Players = game:GetService("Players")
local ContentProvider = game:GetService("ContentProvider")

ReplicatedFirst:RemoveDefaultLoadingScreen()
local player = Players.LocalPlayer
local gui = Instance.new("ScreenGui")
gui.IgnoreGuiInset = true
gui.ResetOnSpawn = false
local bg = Instance.new("Frame")
bg.Size = UDim2.fromScale(1, 1)
bg.BackgroundColor3 = Color3.fromRGB(20, 20, 28)
bg.Parent = gui
local label = Instance.new("TextLabel")
label.Size = UDim2.fromScale(1, 0.1)
label.Position = UDim2.fromScale(0, 0.45)
label.BackgroundTransparency = 1
label.TextScaled = true
label.TextColor3 = Color3.new(1, 1, 1)
label.Text = "Loading..."
label.Parent = bg
gui.Parent = player:WaitForChild("PlayerGui")

-- Preload only spawn-critical assets (fill with your spawn-area decals/sounds/UI images)
local critical: { Instance } = {}
local MAX_WAIT = 5 -- seconds; never hold players longer for cosmetics
local start = os.clock()
task.spawn(function()
	if #critical > 0 then
		ContentProvider:PreloadAsync(critical)
	end
end)
while not game:IsLoaded() and os.clock() - start < MAX_WAIT do
	task.wait(0.1)
end
gui:Destroy()
```

## The first 60 seconds: second-by-second script
| Time | What happens | Rule |
|---|---|---|
| 0–2 s | spawn facing the core action; other players visible nearby | camera framed on the "one thing"; no UI wall |
| 2–5 s | a pulsing arrow/trail points to the one button or object | visuals, ≤ 5 words of text |
| ≤ 5 s | **first input** (tap the glowing rock / step on pad / click "Hatch") | one input, works on touch |
| ≤ 15 s | **first reward**: currency burst, sound, number pop, bar fills | generous; juice > value |
| 15–40 s | the reward visibly enables the next step ("You can afford: Better Shovel!") | goal tracker appears |
| ≤ 60 s | **first purchase/upgrade**, and the player *feels* the improvement (faster, bigger number) | core loop closed once ([[Core-Loops]]) |
| 60–180 s | second goal revealed (next zone gate, egg, round start); one new mechanic | this is the bounce window: pace it with variety |
| 3–10 min | first "big moment" (new zone/pet/tower), social hook (see others' stuff, trade/co-op prompt) | [[Progression-Curves]] targets |
| End of session 1 | moment of joy + visible short/mid/long goals | "leave players wanting more" |

### What to show before the first reward
**Show**: the world, the one action, a tiny goal ("Collect 10 coins"), other players.
**Hide or defer**:
- shop and gamepass prompts (defer to minute 3+ for new players) ([[Gamepasses-vs-Developer-Products]]),
- daily-reward/streak modal (show from session 2) ([[Daily-Rewards-And-Streaks]]),
- update logs, codes, settings, group-join asks, the trade menu, and any long dialogue.

### The one-button first action
- One **verb** (collect, hit, plant, place, jump). The control must be discoverable without reading: a big on-screen button on mobile, or auto-trigger on proximity.
- It must succeed on the first try (no fail state in the first 15 s).
- Its result must be **audible and visible**, with clear feedback for every action (Roblox UX guidance).

## FTUE funnel (log every step)
Typical simulator funnel. Name steps clearly and keep the numbering stable across versions.

| # | Step | Healthy completion vs. previous step |
|---|---|---|
| 1 | Joined (PlayerAdded) | 100% |
| 2 | Loaded / character spawned | ≥ 97% |
| 3 | First action | ≥ 95% |
| 4 | First reward | ≥ 93% |
| 5 | First purchase | ≥ 85% |
| 6 | Second area / egg / round | ≥ 75% |
| 7 | Tutorial complete | ≥ 70% |
| 8 | Session ≥ 10 min | ≥ 50% |

⚠️ verify: the per-step "healthy" percentages are vault heuristics, not Roblox-published benchmarks. Compare with your genre benchmarks in Creator Analytics.

```lua
--!strict
-- ServerScriptService/Onboarding/OnboardingFunnel.lua (ModuleScript, server-only)
-- Events only send from server in published games (not Studio).
local AnalyticsService = game:GetService("AnalyticsService")

local OnboardingFunnel = {}

local STEPS: { string } = {
	"Joined", "Spawned", "FirstAction", "FirstReward",
	"FirstPurchase", "SecondArea", "TutorialComplete", "Session10Min",
}
local INDEX: { [string]: number } = {}
for i, name in STEPS do
	INDEX[name] = i
end

local logged: { [Player]: { [number]: boolean } } = {}

-- isNewPlayer: only log for first-session players (check your saved data flag)
function OnboardingFunnel.step(player: Player, stepName: string, isNewPlayer: boolean)
	if not isNewPlayer then
		return
	end
	local idx = INDEX[stepName]
	assert(idx, "unknown onboarding step " .. stepName)
	local set = logged[player]
	if not set then
		set = {}
		logged[player] = set
	end
	if set[idx] then
		return
	end
	set[idx] = true
	local ok, err = pcall(function()
		AnalyticsService:LogOnboardingFunnelStepEvent(player, idx, stepName)
	end)
	if not ok then
		warn("Onboarding funnel log failed:", err)
	end
end

function OnboardingFunnel.clear(player: Player)
	logged[player] = nil
end

return OnboardingFunnel
```

## Tutorial patterns that work on Roblox
| Pattern | Use when | Example |
|---|---|---|
| **Visual elements** (arrows, trails, highlights, in-world signs) | always: the default teaching tool | Hello Kitty Cafe spotlight + arrow on the button; Color or Die sign in line of sight |
| **Contextual / just-in-time tutorial** | features not needed in minute 1 (fusing, trading, marketplace) | Squishmallows triggers the combine tutorial when the player owns duplicates |
| **Timed hints** | step where most succeed alone | Plant reference: highlight "Plant" after 11 s if most press it within 10 s; show once |
| **Goal tracker** (top-centre "Next: buy Better Shovel 0/50") | every progression game | persistent until the step is done |
| **Diegetic NPC guide** | RP/story games | ≤ 1 line per beat, skippable |
| **Learn-by-doing first round** | round-based games (DTI, MM2) | first round is the tutorial; no separate mode |

Anti-patterns: text walls, forced 2–3 min linear tutorials, UI-locking modals, and teaching every system up front. Contextual tutorials exist to defer non-essentials.

## Starter kit
- Give starter currency/items so players touch systems early. **A/B test the amount** (Roblox docs suggest exactly this). Lock in the winner with Configs.
- Keep early XP thresholds low so level 2–3 arrives within minutes ([[Progression-Curves]]).
- Social onboarding: spawn new players where others are active. For social games, test matchmaking groupings in the FTUE.

## Returning players
- Skip the tutorial entirely for anyone with saved progress. A "Welcome back" panel bundles offline gains, daily reward and what's new (one modal) ([[Idle-And-Offline-Earning]]).
- On update day, returning players see a 1-screen "New: X" with a button that teleports to it ([[Content-Cadence]]).

## Checklist
- [ ] Spawn camera faces the core action; thumbnail matches the spawn view
- [ ] Custom loading ≤ 5 s; no unskippable intro
- [ ] First input ≤ 5 s, first reward ≤ 15 s, first purchase ≤ 60 s (measured on a fresh account on mobile)
- [ ] Zero popups or prompts before the first reward; shop prompts deferred to minute 3+
- [ ] Every FTUE step logged with `LogOnboardingFunnelStepEvent`; funnel reviewed weekly
- [ ] Timed hints at the points where playtesters stall, shown once
- [ ] Session 1 ends with a joy moment + visible next goals
- [ ] Starter currency/hint timing exposed as Configs and A/B tested

## Pitfalls
- Starting with character customisation, a class pick or a story cutscene. Choices before fun increase the bounce rate.
- Testing only on PC. Touch players miss keyboard prompts ("Press E").
- Popup avalanche on join (daily, offline, update, starter pack). Players read it as an ad and leave.
- A first reward too small to notice (+1 coin with no VFX).
- Changing funnel step numbers between versions, which makes analytics incomparable.
- Spawning new players alone in an empty area of a large map.

## Related
- [[Core-Loops]] · [[Progression-Curves]] · [[Session-Length-And-Pacing]] · [[Difficulty-And-Mastery]] · [[Balancing-Methods]] · [[Genre-Playbooks]]
- [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]] · [[Analytics-And-Instrumentation]] · [[Daily-Rewards-And-Streaks]] · [[Gamepasses-vs-Developer-Products]] · [[Idle-And-Offline-Earning]]

## Sources
- Roblox Creator Docs, Onboarding: https://create.roblox.com/docs/production/game-design/onboarding (via github.com/Roblox/creator-docs, read 2026-10-04)
- Roblox Creator Docs, Onboarding techniques (visual elements, contextual tutorials, timed hints, 11 s example): https://create.roblox.com/docs/production/game-design/onboarding-techniques (read 2026-10-04)
- Roblox Creator Docs, Funnel events: https://create.roblox.com/docs/production/analytics/funnel-events (read 2026-10-04)
- Roblox Creator Docs, Discovery (first play bounce 61–180 s; mismatched metadata): https://create.roblox.com/docs/discovery (read 2026-10-04)
- DevForum, Learn More About FTUE & Onboarding: https://devforum.roblox.com/t/learn-more-about-first-time-user-experience-onboarding/2621940
- DevForum, 120 second loading time kicks connecting players: https://devforum.roblox.com/t/120-second-loading-time-kicks-connecting-players-from-games/14571
