---
tags: [design/difficulty]
status: draft
updated: 2026-10-04
confidence: medium
---
# Difficulty and Mastery

## TL;DR
- Keep players in the **flow channel**: challenge rises a little faster than skill, then a short relief beat follows. Use a **sawtooth** (ramp up, then an easy "victory lap" section after each spike), not a straight ramp.
- **Low skill floor, high skill ceiling.** Most of the Roblox audience is young and on mobile/touch, so the first 5 minutes must be beatable one-handed. Depth (combos, routes, tech) is optional and rewards mastery.
- **Retry cost is the main difficulty knob on Roblox.** Respawn-to-retry ≤ 3 s. Checkpoints every 1 obstacle early and every 3–5 later. Never lose more than 60 s of progress to one mistake in a casual game.
- Adapt difficulty **with the player's consent**: offer help after repeated failure (skip stage, a hint, a temporary buff), and never rubber-band silently against a payer.
- Measure difficulty with telemetry, not opinion: deaths and time per stage/wave, quit-after-death rate. Any step where more than 15% of the players who reach it quit there is a bug ([[Analytics-And-Instrumentation]]).

## Flow model
- Flow (Csikszentmihalyi) sits between anxiety (challenge ≫ skill) and boredom (skill ≫ challenge). Players move through the channel by learning. The designer moves the channel with content.
- Practical sawtooth: 3–5 escalating challenges → 1 relief or reward beat → a new mechanic introduced in a safe context → repeat.
- **Introduce → Test → Twist → Combine**: teach each mechanic alone with zero fail risk, test it, vary it, then combine it with earlier mechanics.

## Skill floor vs. ceiling
| Element | Floor (everyone) | Ceiling (mastery) |
|---|---|---|
| Inputs | 1 tap/click or move+jump | animation cancels, timing windows, movement tech |
| Information | big telegraphs, colour-coded danger | reading subtle tells, map knowledge |
| Optimisation | auto-equip best, recommended build | min-max builds, speedruns, routing |
| Social | can contribute in co-op while weak | carries, competitive ranks |

Decision rule: if the top 10% of players stop gaining an advantage after ~5 hours, add a ceiling (ranked, speedrun timer, harder modes). If the bottom 50% fail the first challenge more than twice, lower the floor.

## Obby difficulty design
Roblox defaults: `Humanoid.WalkSpeed` 16 studs/s, `JumpPower` 50 (`JumpHeight` 7.2 studs), `Workspace.Gravity` 196.2 studs/s². Changing any of these changes every jump in the game, so lock them before you build stages.

Gap guidelines, measured on default character settings. ⚠️ verify by measuring in Studio: max horizontal running-jump distance with defaults.

| Tier | Horizontal gap (edge to edge) | Platform width | Checkpoint spacing | Expected deaths/stage (median) |
|---|---|---|---|---|
| Tutorial | ≤ 4 studs | ≥ 6 studs | every stage | 0 |
| Easy | 4–6 | 4–6 | every stage | 0–1 |
| Medium | 6–8 | 2–4 | every 1–2 stages | 1–2 |
| Hard | 8–10 (near max) | 1–2, moving parts | every 2–3 | 3–5 |
| Extreme | max-jump, wraparounds, truss flicks | 1 | every 3–5 | 6+ (opt-in only) |

Rules:
- Difficulty numbers on stage signs ("Stage 37, Hard") set expectations and lower rage-quits.
- Use mobile-unfriendly tricks (shift-lock wraparounds, truss flicks) only in labelled optional paths.
- The **skip-stage developer product** is the standard obby monetisation and doubles as consented adaptive difficulty. Prompt it after 3+ deaths on the same stage, at most once per stage ([[Gamepasses-vs-Developer-Products]]).
- Every 10 stages: a reward (cosmetic trail, badge) plus a flat "lap" section.

## Combat difficulty design
| Knob | Casual default | Notes |
|---|---|---|
| Player TTK vs. trash mob | 1–3 hits | killing fast is the power fantasy |
| Mob TTK vs. player | 8–15 hits | low lethality early |
| Attack telegraph (wind-up) | ≥ 0.5 s early, 0.3 s late | add a VFX/sound cue for mobile players |
| Boss phases | 2–3, changing at 66/33% HP | each phase introduces one new pattern |
| Enemy count on screen | ≤ 6 early | readability on mobile |
| Network latency budget | design dodge windows ≥ 0.2 s | ping ~100–200 ms is common; hit detection authority: [[Anti-Exploit-And-Server-Authority]] |

**Power budget**: total player power from all sources (level, gear, pets, passes) should fall within a planned band per zone. Recommended enemy HP for zone z = expected player DPS(z) × target TTK. Paid power must not push players more than ~1 zone ahead ([[Balancing-Methods]]).

Tower defense difficulty works the same way: enemy HP per wave ≈ expected tower DPS at that wave × time-on-path. Add burst "check" waves (bosses, stealth, flying) every 5–10 waves to test composition, not just DPS.

## Adaptive difficulty (DDA)
| Technique | When | Transparency |
|---|---|---|
| Assist offer after N fails (skip, hint arrow, shield) | obby, puzzle, boss | explicit prompt, player chooses |
| Matchmaking by level/MMR | PvP, battlegrounds | invisible but fair |
| Mob scaling to party size/level | co-op PvE | visible ("Enemies scaled to 4 players") |
| Rubber-banding (racing) | casual races only | hidden; never in competitive or paid contexts |
| New-player protection (spawn shield, low-damage servers) | PvP, steal/raid games | visible timer |

Minimal server-side failure tracker (prompt assist after 3 deaths on the same stage):
```lua
--!strict
-- ServerScriptService/AssistService.server.lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ASSIST_AFTER_DEATHS = 3
local assistRemote = Instance.new("RemoteEvent")
assistRemote.Name = "OfferAssist"
assistRemote.Parent = ReplicatedStorage

type StageState = { stage: number, deaths: number, offered: boolean }
local state: { [Player]: StageState } = {}

local function getStage(player: Player): number
	local ls = player:FindFirstChild("leaderstats")
	if ls then
		local v = ls:FindFirstChild("Stage")
		if v and v:IsA("IntValue") then
			return v.Value
		end
	end
	return 1
end

Players.PlayerAdded:Connect(function(player: Player)
	state[player] = { stage = getStage(player), deaths = 0, offered = false }
	player.CharacterAdded:Connect(function(character: Model)
		local humanoid = character:WaitForChild("Humanoid") :: Humanoid
		humanoid.Died:Connect(function()
			local s = state[player]
			if not s then
				return
			end
			local stage = getStage(player)
			if stage ~= s.stage then
				s.stage, s.deaths, s.offered = stage, 0, false
			end
			s.deaths += 1
			if s.deaths >= ASSIST_AFTER_DEATHS and not s.offered then
				s.offered = true
				assistRemote:FireClient(player, stage, s.deaths) -- client shows "Skip stage?" / hint
			end
		end)
	end)
end)

Players.PlayerRemoving:Connect(function(player: Player)
	state[player] = nil
end)
```

## Mastery signals (give players proof they improved)
- Personal bests (time, wave, night survived) shown at session end. These also make good session-end hooks ([[Session-Length-And-Pacing]]).
- Ranks/divisions with visible progress. Badges for skill feats, not just playtime.
- Replayable content with modifiers (hard mode, nightmare, speedrun timer). Cheap content that extends the ceiling ([[Content-Cadence]]).

## Checklist
- [ ] Lock movement constants before level building; measure max jump and document it in the GDD
- [ ] Tier every obby stage, wave and boss, and record the expected deaths/time
- [ ] Respawn-to-retry ≤ 3 s; checkpoint spacing per tier table
- [ ] Assist or skip offer after N failures; log offers and acceptances
- [ ] Per-stage funnel: reached / completed / quit-at ([[Analytics-And-Instrumentation]])
- [ ] One optional mastery ceiling (hard mode, ranked, timer) by launch +30 days

## Pitfalls
- Difficulty spikes in the first 3 minutes. Roblox's first-play bounce signal punishes them directly ([[Discovery-Algorithm]]).
- Designers tuning on PC with keyboard. Most players are on touch. Test every stage on a phone.
- Selling power in PvP that makes free players' skill irrelevant. Retention collapses for the 95%+ who don't pay.
- Hidden rubber-banding discovered by the community. Trust loss is permanent.
- Long death animations or menus before respawn. Every second added to retry time raises quit rate.

## Related
- [[Core-Loops]] · [[Onboarding-And-First-60-Seconds]] · [[Balancing-Methods]] · [[Session-Length-And-Pacing]] · [[Genre-Playbooks]]
- [[Gamepasses-vs-Developer-Products]] · [[Anti-Exploit-And-Server-Authority]] · [[Analytics-And-Instrumentation]] · [[Discovery-Algorithm]]

## Sources
- Csikszentmihalyi, *Flow: The Psychology of Optimal Experience* (1990), the flow channel model
- Roblox Creator Docs, Humanoid (WalkSpeed 16, JumpPower 50, JumpHeight 7.2) and Workspace.Gravity 196.2 defaults: https://create.roblox.com/docs/reference/engine/classes/Humanoid ⚠️ verify: defaults unchanged as of 2026-10
- Roblox Creator Docs, Discovery (first-play bounce rate signal): https://create.roblox.com/docs/discovery (read 2026-10-04)
- Roblox Creator Docs, Onboarding techniques (timed hints after most players succeed): https://create.roblox.com/docs/production/game-design/onboarding-techniques (read 2026-10-04)
