---
tags: [design/core-loops]
status: draft
updated: 2026-10-04
confidence: medium
---
# Core Loops

## TL;DR
- Design three nested loops, in this order: the **core loop** (10–60 s, the verb you repeat), the **session loop** (5–30 min, the goal one session closes) and the **meta loop** (days to weeks: collection, rebirth, trading, events). Add a **social loop** on top. If any layer is missing, a Roblox game stalls at D1 (no core), at average session length (no session goal) or at D7+ (no meta).
- A new player must **finish one full core loop within 60 s of spawning** and see the reward land. Roblox counts a quick exit as a negative ranking signal, "first play bounce rate", measured over the 61–180 s window. See [[Onboarding-And-First-60-Seconds]].
- Every loop has to close. The reward from loop N must make loop N+1 visibly faster, bigger or new. A reward that changes nothing in the loop is a dead faucet.
- Express the loop as **Action → Reward → Upgrade → (stronger) Action**, and name the stat each upgrade changes. If you cannot name the stat, the loop is not designed yet.
- On Roblox the social loop drives growth: co-play days are a ranking signal ("intentional co-play days per user"). Every genre needs a show-off, trade, help or steal interaction ([[Discovery-Algorithm]]).

## Definitions (Roblox creator docs framing)
Roblox splits a core loop into three parts:
1. **Minute-to-minute interaction**: the constant baseline (explore, run, click).
2. **Most repeated set of actions**: the defining mechanic (fight, hatch, plant, place tower).
3. **Progression engine**: where the gains show up (levels, upgrades, new zones), feeding back into 1 and 2.

The vault extends this to four time scales:

| Layer | Period | Player question it answers | Typical Roblox implementation |
|---|---|---|---|
| Micro / moment | 0.5–5 s | "Does this feel good?" | Click/swing feedback, coin pop, sound, damage numbers |
| Core loop | 10–60 s | "What do I do?" | Collect → sell → upgrade; plant → wait → harvest; fight → loot |
| Session loop | 5–30 min | "What am I working toward today?" | Next zone, next egg tier, next rebirth, quest list, round win |
| Meta loop | days–months | "Why come back tomorrow / next week?" | Index/collection, rebirth tiers, trading value, seasonal pass, weekly update content |
| Social loop | any | "Why bring / stay with friends?" | Trade, gift, co-op boss, raid, steal, rate outfits, server-wide events |

## Loop diagrams (text)
Simulator (Pet Simulator–style):
```
[Click/break coins] --coins--> [Buy egg] --pet--> [Equip best pets] --+multiplier--> [Break bigger coins]
        ^                                                                                  |
        +-------------------------- unlock next area (coin gate) <-------------------------+
Meta: rebirth (reset coins/areas, keep pets, +x% coins) -> collection index -> trading -> huge/limited pets
```
Grow a Garden–style (timer loop with real-time waits):
```
[Buy seeds from rotating shop] -> [Plant] -> (real-time growth) -> [Harvest] -> [Sell] -> [More/better seeds]
   ^ shop restocks every few minutes (variable availability)       | mutations (weather events) = variable reward
   +---------------------------------------------------------------+
Social: visit/steal-adjacent interaction, trading pets/fruit, server-wide weather events
```
Tower defense:
```
[Wave starts] -> [Place/upgrade towers with in-match cash] -> [Survive wave] -> ... -> [Win/lose]
      -> [Match rewards: coins/XP] -> [Unlock/buy towers, level up] -> [Harder mode/map]
```
Round-based social (Dress to Impress / Murder Mystery 2):
```
[Lobby/intermission + theme reveal] -> [Timed round (~6 min dressing in DTI)] -> [Judging/resolution]
      -> [Currency + rank/XP] -> [Unlock cosmetics] -> [Next round with better expression]
```

## How top Roblox genres loop

| Genre | Core loop (≤60 s) | Session goal | Meta / long-term | Social hook |
|---|---|---|---|---|
| Simulator | click/collect → sell → upgrade | next area / egg tier | rebirth, pet index, huges | trade, show-off pets, leaderboards |
| Tycoon | collect dropper cash → buy button | finish the base / next floor | rebirth, multiple bases | visit, raid, PvP |
| Obby | jump → checkpoint | reach stage N | stage count, skips, cosmetics | race friends, help |
| Tower defense | place → upgrade → wave | clear map/mode | tower collection, levels, events | co-op 4-player matches |
| Horror (Doors-like) | explore room → avoid entity | survive to floor N | achievements, revives, unlocks | squad co-op, rescue |
| Roleplay/hangout (Brookhaven, Adopt Me) | self-directed play | home build, pet age | pet collection, trading value | everything is social |
| Battlegrounds | combo → KO | streak / kills | characters, emotes, ranks | 1v1 and FFA servers |
| Anime grinder (Blox Fruits) | fight NPC → XP/loot | level band / island / boss | max level (2,800 as of Mar 2026), fruits, raids | PvP, trading fruits |
| Trend / "brainrot" (Steal a Brainrot) | buy/steal unit → base income | best base | rare units, rebirth | **stealing from other players** is the core |
| Survival (99 Nights in the Forest) | gather → fuel camp → defend | survive night N | classes, best-night records | squad co-op |

Full genre detail: [[Genre-Playbooks]].

## Design rules
1. **Verb count**: the core loop uses 1–3 verbs. Beginners on mobile get one obvious button (see [[Onboarding-And-First-60-Seconds]]).
2. **Loop period targets**: the core loop completes in 10–60 s. The session goal takes 5–30 min ([[Session-Length-And-Pacing]]). The next meta milestone sits ≤ 1 day away for D1 retention and ≤ 7 days for D7 ([[Retention-Metrics-D1-D7-D30]]).
3. **Visible next goal**: at any moment the HUD or world shows the next gate (door price, egg cost, level bar). Decision rule: if a playtester can't say "I'm trying to get X" within 3 s of being asked, add a goal tracker.
4. **Multiplicative upgrades come late.** Early upgrades are additive and easy to read ("+1 per click"). Bring in multipliers (pets, rebirth) once the player has the base loop, at 5–15 min. Formulas: [[Progression-Curves]].
5. **Variable reward in the loop**: put one random element (egg hatch, mutation, crit, rare drop) in the core or session loop. Set its odds with [[Reward-Schedules]], and follow the odds disclosure rules if it is paid.
6. **Sink every faucet**: each currency the loop produces needs a spend inside the same loop ([[Economy-Design-Sinks-And-Faucets]]).
7. **Social by default**: the play space is shared. Others see your pets, base and outfit (passive show-off), and you get at least one active interaction (trade, gift, steal, co-op).
8. **Wait timers belong to the session or meta layer only**: real-time waits (growth, offline income) give players a reason to come back but must never block the first core loop ([[Idle-And-Offline-Earning]]).

## Loop validation test (run on a prototype)
| Test | Pass threshold |
|---|---|
| Time from spawn to first reward | ≤ 15 s |
| Time to complete first full loop (earn → spend → see effect) | ≤ 60 s |
| % of playtesters who can explain the loop after 2 min | ≥ 80% |
| Time between "upgrade" moments in first 10 min | ≤ 90 s ([[Progression-Curves]]) |
| Does session 1 end with an unfinished visible goal? | Yes ([[Session-Length-And-Pacing]]) |
| Is there a reason to invite a friend? | Yes, with a named interaction |

## Checklist
- [ ] Write the core loop as Action → Reward → Upgrade → Action and name the stat each upgrade raises
- [ ] Define a session goal and a meta goal, with expected time-to-reach for each
- [ ] Add one variable-reward element and one social interaction
- [ ] Prototype the core loop with graybox art and pass the validation table before building content
- [ ] Log onboarding funnel steps for each loop step ([[Analytics-And-Instrumentation]])

## Pitfalls
- **A meta loop with no core loop under it**: a deep pet index can't save a boring click.
- **An open loop**: rewards that don't feed back in (cosmetic-only currency in a power game) leave players with nothing to do.
- **The loop explained in text**: players skip text. Show it with arrows and world signs.
- **Multiplier soup too early**: five stacked multipliers in the first 5 minutes is unreadable.
- **Copying a trend's surface** (art, title) without its loop. The Recommended-for-You algorithm deprioritises near-duplicate games ([[Discovery-Algorithm]]).

## Related
- [[Progression-Curves]] · [[Reward-Schedules]] · [[Prestige-And-Rebirth]] · [[Economy-Design-Sinks-And-Faucets]]
- [[Onboarding-And-First-60-Seconds]] · [[Session-Length-And-Pacing]] · [[Genre-Playbooks]] · [[Game-Design-Doc-Template]]
- [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox Creator Docs, Core loops: https://create.roblox.com/docs/production/game-design/core-loops (via github.com/Roblox/creator-docs, read 2026-10-04)
- Roblox Creator Docs, Discovery (signals incl. first-play bounce 61–180 s, co-play days): https://create.roblox.com/docs/discovery (read 2026-10-04)
- Dress to Impress round structure (360 s dressing): https://dti-dress-to-impress.fandom.com/wiki/Dress_To_Impress/Game_Mode
- Blox Fruits max level 2,800 (Update 31, Mar 2026): https://www.sportskeeda.com/roblox-news/what-max-level-blox-fruits
- John Hopson, Behavioral Game Design (2001): https://www.gamedeveloper.com/design/behavioral-game-design
