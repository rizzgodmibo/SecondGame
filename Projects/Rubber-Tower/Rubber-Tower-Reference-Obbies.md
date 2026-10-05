---
tags: [project/rubber-tower, reference/obbies]
status: draft
updated: 2026-10-04
confidence: medium
---
# Rubber Tower: Reference Obbies

## TL;DR
- Holden's references: the 15 top "Obby & Platformer" games by active players in his screenshot (2026-10-04, of 1,354 games in that genre), plus any other ragdoll obbies. This note records what each does so far, from public game pages, wiki guides and Rolimons.
- Six of the 15 have "Tower" in the title and most use a troll, ASMR or "together" hook. The strongest ragdoll comparable is **Troll Ragdoll Tower** (created 2025-12-21, 35.7M visits, 84% rating on Rolimons).
- **Tower of Hell** (the "shared server" model Holden named) has **no checkpoints** and runs 8-minute rounds, so it conflicts with Holden's "endless + checkpoints" choices. Rubber Tower borrows its shared-server idea only.
- Ragdolling every player's own avatar is a documented technique (swap Motor6D joints for BallSocketConstraints, set Humanoid to Physics state), but cost scales with player count. Needs an early phone test.
- Everything here is **observation of other games or documented third-party guidance**. Nothing was tested in Studio, and none of it is an approved mechanic.

## Evidence key
- **Obs (page):** read on the game's Roblox page or Rolimons on 2026-10-04.
- **Obs (guide):** from a third-party guide or wiki on 2026-10-04. ⚠️ verify if a number matters.
- **Obs (screenshot):** from Holden's screenshot.
- **Not researched / fetch failed:** listed so nobody assumes it was checked.

## Screenshot snapshot (Holden, 2026-10-04, Obby & Platformer, sorted by active players)
Tower of Hell (74%, 20.9k) · TROLL Hug Tower (86%, 14.7k) · Barry's Prison Run (61%, 12.8k) · [1 & 2 Player] Grapple Cart Obby (93%, 11.5k) · [Aura] Phonk Edit Tower (95%, 7.1k) · [PRO] Kart of Hell (75%, 5.8k) · Wax ASMR Tower (89%, 7.6k) · Obby But You're on a Scooter (72%, 6.3k) · [HELL] Spiral Difficulty Chart Obby (81%, 6.2k) · Together [Party Game] (85%, 5.8k) · ASMR Auto Wallhop Tower 2 (72%, 1.5k) · Carry the Glass Together [2 Player] (88%, 5.5k) · +1 Speed Controller Escape (99%, 5.6k) · Team School Breakout (68%, 2.9k) · Squishy Troll Tower [BETA] (86%, 3.3k).
- Obs (screenshot): player counts are a one-moment snapshot, not averages.
- Obs (screenshot): titles lean on tags such as [1 & 2 PLAYER], [PRO], [HELL], [BETA], [UPDATE], and emoji. "Tower" appears in 6 of 15.

## Per-game notes
| Game | What it does | Relevance to Rubber Tower | Source |
|---|---|---|---|
| Tower of Hell | Randomly generated tower each round, **no checkpoints** (fall = back to bottom), 8-minute round whose timer speeds up for each finisher, up to 20 players, coins buy gears and mutators, XP and skill tree. Created 2018-06-18, avg playtime 4.69 min, rating 73.6%. | The shared-server race model Holden named. Our "endless + checkpoints" is the opposite on failure and round structure. | Obs (page) Rolimons; Obs (guide) bloxbonuses.com |
| Troll Ragdoll Tower | Ragdoll physics, randomized gear and tools through the tower, buttons that trigger "troll" effects on other players, 20 max players. Created 2025-12-21, 35.7M visits, 1.6M favorites, 84% rating, peak 7,975 CCU, 90+ badges; gamepasses priced 2 to 199 Robux (2x currency, gear retention, cosmetics). | Closest ragdoll comparable. Shows that gear plus trolling plus badges drives engagement. | Obs (page) Rolimons, Roblox page |
| TROLL Hug Tower | Competitive platformer: catch other players, carry them, throw them into lava. | PvP-style chaos. A moderation and young-teen concern if copied. | Obs (page) Roblox page |
| Squishy Troll Tower [BETA] | Squishy, deformable platforms with ASMR sound; checkpoints; free tools and cosmetics; console support in testing. | Sound and squish feel as the hook, and a checkpoint model like ours. | Obs (page) Roblox page |
| Carry the Glass Together [2 Player] | Two players carry one fragile glass pane up a tower; it shatters on hazards or if they separate; **Rewind** resets to the last safe point; partner leaving removes the pane. | Strong example of low-frustration retry (rewind) and a forced-cooperation hook. | Obs (guide) allthings.how |
| Phonk Edit Tower | Climb synced to phonk music, screen shake on beats, "aura" styling. | Presentation and music as the hook; not a mechanic. | Obs (page) Roblox page |
| Ragdoll Physics Tower | "Ragdoll Stack" used to climb walls, slippery banana hazards, multiplayer. No active players at snapshot. | Ragdoll-stacking idea; low activity, so a weak comparable. | Obs (page) Roblox page |
| Grapple Cart Obby [1 & 2 Player] | Roblox page and a guide fetch failed (403). Title says 1 and 2 player; carts are a theme. | Not researched. | Fetch failed |
| Together [Party Game], Wax ASMR Tower, Auto Wallhop Tower 2, Kart of Hell, Team School Breakout, others | Only the screenshot title and stats are known. | Not researched. | Screenshot only |

## Patterns worth noting (recommendations, not tested)
- A **single strong hook in the title and thumbnail** (troll, ASMR, 2-player, music) appears in most top games. Rubber Tower's hook is "everything wobbles and you ragdoll".
- **Soft failure** (Carry the Glass rewind, Squishy Tower checkpoints) coexists with high ratings in this sample. Tower of Hell's harsh no-checkpoint model has a 74% rating. Correlation in a tiny sample, not causal.
- **Gear and trolling** drive the biggest ragdoll comparable. Whether Rubber Tower has any interaction between players is an open decision.
- **Sound feel** (ASMR squish) is a cheap way to make wobble feel good. See [[Roblox Audio Pipeline]].

## Chained-together obbies (researched 2026-10-04, after Holden's map critique)
Holden asked for the world to feel open and wide like the chained-together multiplayer obbies he remembers. Observations only, none approved:
| Game | What is known | Source |
|---|---|---|
| Chained Together (Steam original, the template for the Roblox versions) | A cooperative vertical climb 3,600 m tall through 10 themed worlds stacked every ~300–500 m: Hell Cliffs, Car Race, Whispering Vault, Subway, City, Harbor, Temple, Shrine, Deities, Garden. Platforms are a "random assortment of objects hovering" (cars, girders, cargo ships, pagodas, statues). The world looks open but you can't explore beyond the path. An on-screen altimeter shows height. Beginner mode teleports you back to your furthest point. | Obs (guide) thegamer.com, Wikipedia |
| Chained [2 Player Obby] (1-Day, Roblox) | Created 2024-07-04, 434M+ visits. 2 players chained together, with a hold-to-pull button. Named maps include ScrubLand and Dusty Valley, plus a World 2. The thumbnail shows a grey wall climb. | Obs (page) Rolimons, Roblox page |
| Chained Together [2-3-4-5 PLAYER] (Archive Experiences, Roblox) | 192M+ visits, server size 30. You climb by jumping into objects, with sprint and roll, and you hold E to pull a partner up. | Obs (page) Roblox page, 2026-10-04 |
- **Not researched in detail:** I couldn't watch full gameplay. Video frames were too small and some guide sites blocked fetches (402/403). ⚠️ verify by watching a walkthrough before copying any layout idea.
- **Takeaways (recommendations, not approved):**
  1. Each height band is its own themed world, so progress feels like travelling.
  2. Platforms are themed objects rather than plain slabs, which sells "a world".
  3. Open sky and a view of everything below and above (the goal visible overhead).
  4. A height meter.
  5. Beginner-style "back to your furthest point" matches our checkpoints.

## Play-time data for first-clear target (2026-10-04)
- Obs (page, Rolimons): average playtime per session: Tower of Hell 4.69 min; Grapple Cart Obby 8.20 min (created 2026-08-26); Troll Ragdoll Tower 11.08 min; Carry the Glass Together 11.99 min (created 2026-06-29).
- Obs (forum): one small obby developer reported an average session of 2.7 minutes, with players leaving after two levels.
- These are **average session lengths, not clear times**. No source found for how long a first clear takes in any of these games, so none is claimed.
- Vault guidance: obby median session target 10 to 25 min, beats of 3 to 8 min ([[Session-Length-And-Pacing]], vault estimate ⚠️ verify).
- Target approved by Holden (2026-10-04), still a hypothesis to tune by playtest: about 4 big segments of 5 to 8 minutes, first clear 20 to 40 minutes over more than one session, fast players about 10 minutes. Tune by playtest.

## Shove distance research (2026-10-04)
- Obs (search): no source gives typical push or knockback distances for obby interactions or gamepasses. Troll Ragdoll Tower's page only says players are "launched, pushed, exploded, and sabotaged" with no numbers; the Gear Slap Tower page has none either.
- Obs (forum): a DevForum thread suggests knockback by applying a LinearVelocity of about 25 studs/s for 0.35 s (or 0.5 s with BodyVelocity). Derived, not measured: 25 × 0.35 to 0.5 gives roughly 9 to 12 studs of travel before friction. ⚠️ verify in Studio.
- Obs (vault, measured 2026-10-04): default jump height 7.2 studs, level running-jump reach about 8.7 studs ([[Difficulty-And-Mastery]]).
- Obs (guides): default character about 5 studs tall (some say 5 to 6). The stud-to-metre ratio is not official: 20 studs per metre (physics-derived, 2012) or 0.28 m per stud (2019 change), so "metres" in Roblox is ambiguous; use studs.
- Draft for Rubber Tower (recommendation, hypothesis): shove travel of about 10 studs (roughly two character heights, about one jump gap) with 2 to 3 seconds of ragdoll. It can knock someone off a ledge or a bounce pad but not across the map. Expose the numbers in Config for playtest tuning; have the server validate range, cooldown and force.

## Technical notes: ragdolling the player's own avatar (decided by Holden)
- **Update 2026-10-04 (verified in Studio):** live R15 avatars now use AnimationConstraint joints with built-in BallSocketConstraints. There are no Motor6Ds, so the Motor6D swap below only applies to R6 rigs and older rigs. The built prototype and its PC measurements are in [[Avatar-Ragdoll]].
- Obs (guide, simplified.media): ragdoll replaces Motor6D joints with BallSocketConstraints plus attachment pairs and sets the Humanoid to the Physics state; build constraints at spawn, not at fall time, to avoid frame spikes; disable rather than destroy Motor6Ds; R15 limbs may need CanCollide on while ragdolled; set network ownership deliberately.
- Obs (guide): the same source gives rough server cost tiers (about 1 to 8 ragdolls negligible, 9 to 24 about 1 to 3 ms, 25 to 50 needs client offloading). ⚠️ verify: vendor guide, not Roblox documentation; measure on a real phone.
- Obs (forum): a DevForum thread recommends keeping an invisible real character for locomotion and a separate visible ragdoll model for wobble. ⚠️ verify: forum advice, one thread.
- ⚠️ verify: the Roblox Creator Docs ragdoll page URL I tried returned 404, so no official source was read.
- Risk: R6 and R15 avatars and accessories vary, so wobble consistency is unproven.

## Open questions for Holden
1. What does "endless" mean: a procedurally generated infinite tower, or a very tall fixed tower you can keep climbing past?
2. "Free falls with checkpoints": after a fall, do players land back at the last checkpoint, or only drop to the platform below? How often do checkpoints appear?
3. With other players in the same server, do they only share the space (like Tower of Hell), race each other, or interact (grab, push, troll)? Interaction raises moderation questions for a young-teen audience.
4. Which of the references matter most to you (Troll Ragdoll Tower, Carry the Glass, Squishy Tower, others)? Any specific mechanic you liked?

## Pitfalls
- Do not copy another game's characters, art, names or exact levels; use them for mechanics and feel only.
- Visit and player numbers are snapshots and change daily.

## Related
- [[Rubber-Tower]] · [[Game-Concept-Shortlist-2026-10-04]] · [[Genre-Playbooks]] · [[Roblox Mobile UI Layout]]

## Sources
- [Tower of Hell on Rolimons](https://www.rolimons.com/game/1962086868) (read 2026-10-04)
- [Tower of Hell guide, bloxbonuses.com](https://bloxbonuses.com/articles/tower-of-hell-guide/) (2026-10-04)
- [Troll Ragdoll Tower on Rolimons](https://www.rolimons.com/game/86374876468143) and [Roblox page](https://www.roblox.com/games/139788637490504/Troll-Ragdoll-Tower) (2026-10-04)
- [TROLL Hug Tower](https://www.roblox.com/games/103037106396302/TROLL-Hug-Tower) (2026-10-04)
- [Squishy Troll Tower](https://www.roblox.com/games/82648796375761/Squishy-Troll-Tower) (2026-10-04)
- [Carry the Glass Together guide, allthings.how](https://allthings.how/carry-the-glass-together-how-to-play-the-roblox-2-player-obby/) (2026-10-04)
- [Phonk Edit Tower](https://www.roblox.com/games/101480963912212/Phonk-Edit-Tower) (2026-10-04)
- [Ragdoll Physics Tower](https://www.roblox.com/games/81823526068423/Ragdoll-Physics-Tower) (2026-10-04)
- [Carry the Glass Together on Rolimons](https://www.rolimons.com/game/81734857983173) and [Grapple Cart Obby on Rolimons](https://www.rolimons.com/game/117448312570314) (2026-10-04)
- [DevForum: improving session playtime for obbies](https://devforum.roblox.com/t/improving-session-playtime-for-obbies/3795766) (2026-10-04)
- [DevForum: knockback with a tool like Slap Battles](https://devforum.roblox.com/t/how-to-do-knockback-using-a-tool-like-in-slap-battles/2077895) and [DevForum: studs in a metre](https://devforum.roblox.com/t/how-many-studs-is-there-in-a-meter/103417) (2026-10-04)
- [How tall is a Roblox character](https://progameguides.com/roblox/how-tall-is-a-roblox-character/) (2026-10-04)
- [Roblox ragdoll physics guide, simplified.media](https://simplified.media/guides/roblox-ragdoll-physics) (2026-10-04)
- [DevForum: ragdoll/walking physics thread](https://devforum.roblox.com/t/how-would-i-make-ragdollwalking-physics-like-ragdoll-universe/1385625) (2026-10-04)
- Holden's screenshot of the Obby & Platformer list (2026-10-04)
- [How tall is the Chained Together map, thegamer.com](https://www.thegamer.com/how-tall-is-the-chained-together-map/) and [Chained Together on Wikipedia](https://en.wikipedia.org/wiki/Chained_Together) (2026-10-04)
- [Chained [2 Player Obby] on Rolimons](https://www.rolimons.com/game/18334179599) and [Roblox page](https://www.roblox.com/games/18334179599) (2026-10-04)
- [Chained Together [2-3-4-5 PLAYER], Roblox page](https://www.roblox.com/games/18152595062/Chained-Together) (2026-10-04)
