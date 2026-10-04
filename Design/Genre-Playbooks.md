---
tags: [design/genres]
status: draft
updated: 2026-10-04
confidence: medium
---
# Genre Playbooks

## TL;DR
- Pick a genre by **team strength × trend timing**:
  - Small team, fast iteration → simulator, tycoon, obby or trend game.
  - Strong scripters → TD, battlegrounds or survival.
  - Strong artists/social designers → roleplay or round-based social.
- Every genre below lists **core loop → session goal → meta → social → monetisation hooks → pitfalls → reference games**. Use it as the starting skeleton of the GDD ([[Game-Design-Doc-Template]]).
- Trend genres ("brainrot", steal-a, grow-a) peak and fade within months. Win them with **speed + a distinct twist + weekly updates**, then convert the audience into a durable meta (trading, collection) ([[Content-Cadence]]).
- Near-copies are deprioritised by Recommended-for-You ("non-unique games"). Take the loop, not the look ([[Discovery-Algorithm]]).
- Monetisation hooks named here are detailed in [[Gamepasses-vs-Developer-Products]]. Paid random items need disclosed odds ([[Reward-Schedules]]).

## Genre comparison
| Genre | Build cost | Content burn | Retention driver | Revenue driver | Social engine |
|---|---|---|---|---|---|
| Simulator | low–med | fast | collection + rebirth | boosts, eggs, auto | trading, show-off |
| Tycoon | low | med | build completion | 2× cash, auto-collect | visiting, PvP raids |
| Obby | very low | very fast | stage count | skips, cosmetics | racing friends |
| Tower defense | med–high | med | unit collection + modes | units/summons, VIP | 4-player co-op |
| Horror | med (art-heavy) | fast | squad runs, secrets | revives, cosmetics | squad co-op, streamers |
| Roleplay/hangout | high (art/world) | slow | self-expression, friends | cosmetics, houses, pets | everything |
| Battlegrounds | high (combat) | slow | mastery, characters | characters, emotes, private servers | PvP |
| Anime grinder | high | med | levels, fruits/powers | rerolls, boosts, fruits | PvP, raids, trading |
| Trend / brainrot | low | very fast | collection + stealing | luck, units, protection | stealing, trading |
| Incremental | low | med | numbers + layers | multipliers, auto | leaderboards |
| Survival | med–high | med | run records, classes | classes, revives, cosmetics | squad co-op |
| Round-based social | med | slow | rank + cosmetics | cosmetics, VIP, item slots | voting/rating others |

---

## 1. Simulator (pet / click / collect)
- **Core loop**: break/collect → currency → buy egg/upgrade → stronger pets → bigger collectibles. ([[Core-Loops]] diagram)
- **Session goal**: next zone gate or egg tier. **Meta**: rebirth layers, pet index, huge/limited pets, trading ([[Prestige-And-Rebirth]]).
- **Social**: visible pets following players, trade plaza, server-wide boosts, leaderboards.
- **Monetisation**: 2× coins, auto-hatch/triple hatch, extra pet slots, luck potions (disclose odds), VIP area, limited-time exclusive eggs (paid random → odds + PolicyService).
- **Pitfalls**: inflation from weekly power creep; dupes once trading opens ([[Economy-Design-Sinks-And-Faucets]]); big numbers too early.
- **References**: Pet Simulator 99, Bee Swarm Simulator, Muscle Legends.

## 2. Tycoon
- **Core loop**: dropper produces cash → collect → buy next button (machine/wall/floor) → more income.
- **Session goal**: finish the floor/building. **Meta**: rebirth into a better plot, multiple themes, cosmetics.
- **Social**: neighbours' plots visible, visiting, optional PvP/raid, co-op owners.
- **Monetisation**: 2× cash gamepass, auto-collect, VIP decor, extra floors, cash packs (sparingly).
- **Pitfalls**: dead time waiting for droppers (keep TTN ≤ 60 s early, see [[Progression-Curves]]); a linear button path with no choices; finishing in 2 h with nothing left (add rebirth + decor).
- **References**: Restaurant Tycoon 2, Retail Tycoon 2, Theme Park Tycoon 2.

## 3. Obby
- **Core loop**: jump → checkpoint → next stage.
- **Session goal**: reach stage N. **Meta**: total stages, difficulty tiers, cosmetics/trails, speedrun times.
- **Social**: race friends, see others fail, stage leaderboard.
- **Monetisation**: **skip stage** dev product (prompt after 3+ deaths), speed/gravity coils, trails, VIP, "skip to end" ([[Difficulty-And-Mastery]]).
- **Pitfalls**: hard stages too early; PC-only tricks; content burns in hours (plan weekly stage packs).
- **References**: Tower of Hell (procedural rotating tower = infinite content), Escape-style obbies.

## 4. Tower defense
- **Core loop**: place/upgrade towers with in-match cash → survive waves → match rewards → unlock/level towers.
- **Session goal**: clear a map/difficulty. **Meta**: tower collection (summon banners in anime TDs), modes (hardcore, endless), events.
- **Social**: 4-player co-op, shared cash/economy roles, trading units (anime TDs).
- **Monetisation**: tower unlocks (direct buy = no odds issue), summon currency (odds + pity), VIP, 2× speed, private servers.
- **Pitfalls**: one meta tower dominating (power budget); summon pity absent; long matches without a mid-match save or reconnect.
- **References**: Tower Defense Simulator, All Star Tower Defense, Anime Vanguards ⚠️ verify: current relevance of anime TD titles.

## 5. Horror (co-op run-based)
- **Core loop**: explore room → read/avoid entity → survive → next room.
- **Session goal**: reach floor/door N. **Meta**: achievements, unlockable modifiers/modes, lore secrets.
- **Social**: squads of 2–6, revive teammates, streamer reactions (huge acquisition channel).
- **Monetisation**: revives (dev product), cosmetics, modifiers, private servers. Avoid pay-to-skip fear.
- **Pitfalls**: content consumed in 1–2 runs (add randomised rooms + entities); jump-scare fatigue; age-appropriateness (content maturity labels) ⚠️ verify: current Roblox content maturity labels for horror.
- **References**: Doors, Piggy, The Mimic.

## 6. Roleplay / hangout
- **Core loop**: choose role/outfit → interact (house, car, job, pets) → express.
- **Session goal**: self-directed (decorate, raise a pet, host a party). **Meta**: pet ageing/collection, house building, trading (Adopt Me).
- **Social**: the entire product. Voice, emotes, friends, private servers.
- **Monetisation**: houses, vehicles, premium cosmetics, pets (Adopt Me eggs, with odds disclosure), VIP servers, gamepasses for tools.
- **Pitfalls**: high art/world cost; moderation load (safety policies); empty servers feel dead (tune server size for density).
- **References**: Brookhaven RP, Adopt Me!, Berry Avenue, Welcome to Bloxburg.

## 7. Fighting / battlegrounds
- **Core loop**: engage → combo → KO → respawn quickly.
- **Session goal**: kill streak, rank-up. **Meta**: characters/movesets, mastery, ranked, emotes.
- **Social**: FFA servers, 1v1 duels, spectating, clips for TikTok.
- **Monetisation**: characters (sidegrades), emotes, cosmetics, private servers, "ultimates" cosmetics. Keep paid power ≤ ~10% ([[Balancing-Methods]]).
- **Pitfalls**: netcode/hit-reg complaints (server authority vs. responsiveness, see [[Anti-Exploit-And-Server-Authority]]); new-player stomping (add spawn protection and skill-based servers); balance whiplash.
- **References**: The Strongest Battlegrounds, Jujutsu Shenanigans, Rivals.

## 8. Anime grinder / RPG
- **Core loop**: quest → fight NPCs → XP/loot → level/stat points → harder island.
- **Session goal**: level band, boss drop, new island. **Meta**: max level (Blox Fruits 2,800 as of Mar 2026, raised by updates), powers/fruits, raids, PvP bounty.
- **Social**: PvP, crews, raids, fruit trading.
- **Monetisation**: permanent power/fruit purchase, 2× XP/drop, storage, rerolls (odds), fast travel.
- **Pitfalls**: grind walls with no variety; level caps reached faster than updates; paid fruits trivialising PvP.
- **References**: Blox Fruits, King Legacy.

## 9. Trend / "brainrot" (steal-a, meme-unit collectors)
- **Core loop**: buy/collect meme units → place in base → passive income → **steal** others' units or defend your own.
- **Session goal**: get a rarer unit and a fuller base. **Meta**: rarity collection, rebirth, rare spawns at timed events.
- **Social**: stealing/defending is the core conflict. Server events and admin events create spikes. Steal a Brainrot hit a 25.2M CCU record (Oct 2025).
- **Monetisation**: luck boosts (disclose), base protection/lock time, direct buy of units, server luck, admin-style events.
- **Pitfalls**: trend decay (meme fatigue in weeks to months); IP and originality concerns; griefing frustration for weak players (add protection timers); copycat flood ("non-unique games" deprioritised).
- **References**: Steal a Brainrot; Grow a Garden (adjacent: farming + steal/visit + weather events).

## 10. Incremental / idle
- **Core loop**: earn → buy generator/multiplier → earn faster. Offline gains.
- **Session goal**: next layer unlock. **Meta**: prestige layers, achievements, challenge runs ([[Idle-And-Offline-Earning]]).
- **Social**: leaderboards, visible avatars/bases, competitive server events.
- **Monetisation**: permanent multipliers, auto-buyers, offline cap extensions, time warps.
- **Pitfalls**: number overflow (see [[Progression-Curves]]); too passive (playtime ok, fun low); thin visuals. Roblox players expect a 3D avatar presence.
- **References**: "+1 Speed per second"-style games, Clicker Simulator ⚠️ verify: current top incremental titles.

## 11. Survival (co-op)
- **Core loop**: gather → craft/fuel → defend at night → day/night cycle.
- **Session goal**: survive night N. **Meta**: classes/kits, best-night records, unlocks, achievements.
- **Social**: squads, roles (gatherer/defender), rescuing teammates.
- **Monetisation**: classes/kits (sidegrade), revives, cosmetics, private servers.
- **Pitfalls**: runs too long for mobile sessions (target 20–45 min, see [[Session-Length-And-Pacing]]); solo players stranded (matchmake squads); performance with many entities.
- **References**: 99 Nights in the Forest (14.2M peak CCU, 2025), Dead Rails, Natural Disaster Survival.

## 12. Round-based social (bonus)
- **Core loop**: lobby → timed round (DTI: ~6 min dressing) → reveal/vote/judge → rewards.
- **Session goal**: win a round, rank up. **Meta**: wardrobe/cosmetic unlocks, ranks, seasonal themes.
- **Monetisation**: VIP, extra item slots (DTI: 18 → 24 with a pass), cosmetics, theme picks.
- **References**: Dress to Impress, Murder Mystery 2.

## Checklist
- [ ] Choose a genre with the comparison table; write the 7-field skeleton into the GDD
- [ ] Identify 3 reference games; time their first 10 minutes and note each one's first reward and first purchase ([[Onboarding-And-First-60-Seconds]])
- [ ] Name the twist that makes the game non-duplicate
- [ ] Map monetisation hooks to passes vs. products ([[Gamepasses-vs-Developer-Products]])
- [ ] Plan the first 4 weekly updates before launch ([[Content-Cadence]])

## Pitfalls
- Chasing a trend that has already peaked. Check CCU trajectories (RoMonitor/Rolimons) before committing ⚠️ verify: the third-party tracker sites you use are current.
- Mixing genres without one dominant core loop.
- Copying monetisation from the top game without its retention base. Monetisation multiplies retention and doesn't replace it.

## Related
- [[Core-Loops]] · [[Progression-Curves]] · [[Prestige-And-Rebirth]] · [[Economy-Design-Sinks-And-Faucets]] · [[Difficulty-And-Mastery]] · [[Session-Length-And-Pacing]] · [[Content-Cadence]] · [[Game-Design-Doc-Template]]
- [[Gamepasses-vs-Developer-Products]] · [[Discovery-Algorithm]] · [[Live-Ops-Playbook]] · [[Anti-Exploit-And-Server-Authority]]

## Sources
- Steal a Brainrot 25.2M CCU: https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/
- Grow a Garden records: https://insider-gaming.com/roblox-grow-a-garden-shatters-all-time-player-record-for-second-week-in-a-row/
- 99 Nights in the Forest 14.2M peak: https://games.gg/news/99-nights-forest-14-million-roblox/
- Dress to Impress game mode (360 s, 18/24 item limit): https://dti-dress-to-impress.fandom.com/wiki/Dress_To_Impress/Game_Mode
- Blox Fruits max level: https://www.sportskeeda.com/roblox-news/what-max-level-blox-fruits
- Pet Simulator 99 rebirth: https://pet-simulator.fandom.com/wiki/Rebirth_(Pet_Simulator_99)
- Adopt Me weekly updates: https://allthings.how/adopt-me-new-update-schedule/
- Roblox Creator Docs, Discovery (non-unique games deprioritised): https://create.roblox.com/docs/discovery (read 2026-10-04)
- Roblox Creator Docs, Paid random items: https://create.roblox.com/docs/production/monetization/paid-random-items (read 2026-10-04)
