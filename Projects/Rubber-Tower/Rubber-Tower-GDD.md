---
tags: [project/rubber-tower, design/gdd]
status: draft
updated: 2026-10-04
confidence: low
---
# Rubber Tower: GDD (draft v0.1)

Line tags: **(USER)** = Holden said it or approved it. **(DRAFT)** = Claude's proposal, not approved. **UNDECIDED** = needs Holden. Numbers tagged "guess ⚠️" are not measured. Template: [[Game-Design-Doc-Template]].

## 0. One-liner
- (DRAFT) "Climb a very tall wobbly tower as a ragdoll, shove your friends, and unlock new worlds."
- (DRAFT) For a 10-year-old: climb a giant jelly tower, fall down laughing, and push your friends.

## 1. Pillars (DRAFT, max 3)
| Pillar | Means we do | Means we don't |
|---|---|---|
| Funny falls | Falling is cheap and silly; respawn at the last checkpoint | Punish falls with a full restart |
| Shared silliness | Players share one world and can push each other | Make griefing the main way to win |
| Always a next world | Beat the first tower to unlock new worlds in later updates | Ship many worlds at launch |

## 2. Audience & market
- (USER) Young teens, mobile and PC first. Genre: obby / tower. Small game.
- (USER) References: games in Holden's screenshot plus other ragdoll obbies, see [[Rubber-Tower-Reference-Obbies]].
- (DRAFT) Our twist: every player's own avatar is the ragdoll, on a single very tall fixed tower, with a basic push move for everyone.
- Trend timing: UNDECIDED. ⚠️ verify with CCU trends before launch (Troll Ragdoll Tower shows demand for the ragdoll-tower niche; one data point).

## 3. Core loops
- (USER) One very tall fixed first map. 3 to 4 checkpoints. Falling respawns you at the latest checkpoint. Players unlock new maps/worlds after beating the first.
- Core (10 to 60 s) (DRAFT): move and jump on wobbly platforms → fall or land → keep climbing.
- Session (5 to 30 min) (DRAFT): reach the next checkpoint, then the summit.
- Meta (days to weeks) (DRAFT): beat world 1 → unlock world 2 and later worlds; collect cosmetics. What is collected: UNDECIDED.
- Social (USER): everyone shares the world; every player has a close-range shove with a 30-second cooldown that pushes the target a set distance and ragdolls them. Starting values accepted by Holden, editable later: about 10 studs and about 2 to 3 seconds of ragdoll (derived from research, ⚠️ verify in Studio; see [[Rubber-Tower-Reference-Obbies]]). Roblox measures in studs, so the number is in studs.
- Diagram: [climb] -> [fall / checkpoint] -> [retry or reach summit] -> [unlock next world]

## 4. First session (DRAFT)
| Time | Player sees/does |
|---|---|
| 0 to 5 s | Spawns at the tower base, other players visible, one clear first jump |
| ≤ 20 s | First wobble and first funny fall onto a soft landing |
| ≤ 60 s | Discovers the push move on a nearby player or prompt; first checkpoint in sight |
| 3 to 10 min | First checkpoint reached |
| session end | Checkpoint progress saved; hint of the next world |
Deferred until later: shop, cosmetics menu, settings. Details UNDECIDED.

## 5. Progression
- (USER) World 2+ unlock after beating world 1.
- (USER) Time-to-clear world 1, approved target (from research in [[Rubber-Tower-Reference-Obbies]]): about 4 big segments of 5 to 8 minutes each, so a first clear is roughly 20 to 40 minutes for a median player, usually over more than one session, and about 10 minutes for fast players. Tune by playtest ⚠️. Fits [[Session-Length-And-Pacing]]. Whether checkpoint progress saves between sessions is UNDECIDED.
- (USER) Unlockable **titles** shown above the player's head replace badges. Holden's unlock examples: reaching checkpoints, completing worlds, buying a first cosmetic, normal events; plus unique ones such as inviting 4 or more friends ("popular" or "life of the party"), pushing 5 or more people down, and reaching the top without claiming any checkpoints. Full list and names UNDECIDED. Decided: the push-down title counts distinct players only (the same player pushed twice counts once); if invited friends can't be verified, Holden agreed the invite title can become "3 friends in the server". ⚠️ Anti-abuse: push titles need rules against friends or alts farming each other (for example, count distinct non-friend players); invite titles need a way to verify invited players really joined (⚠️ verify what Roblox exposes via join data).
- (USER) **Friend boost:** a reward while invited friends are in the server (Holden's example was +10% XP, but he now wants a currency instead of XP). Assumption (DRAFT, confirm): the boost applies to the currency earned. Reference: [[Friend-And-Group-Play]] suggests +10% per friend capped at +30 to 50%.
- (USER) **Checkpoints are saved**, and a menu lists the checkpoints you have claimed so you can teleport to any of them, up or down (and to other worlds in future). You must reach a checkpoint before you can teleport to it. Teleporting does not change your respawn point: you still respawn at your latest checkpoint. Teleporting is free, with no cooldown (decided).
- (USER) **Currency: Squishies** (name chosen by Holden). Earned when reaching checkpoints, finishing a new level or world, and unlocking titles; can also be bought with Robux; spent on in-game cosmetics and more things in the future. It replaces XP. (USER) Every payout (checkpoint, level/world, title) can be earned only once per player. Levels and rebirth: N/A for v1.

## 6. Economy
- (USER) One currency (Squishies), earned in play and sold for Robux (developer products, so receipts must be handled idempotently; see [[ProcessReceipt-Handling]]). (USER, 2026-10-05) Amounts DECIDED: checkpoints 50/75/100/Summit 200; titles 25/75/150/300 by difficulty; daily 7-day streak 25/30/40/50/60/75/150; packs 99→400, 249→1,100, 499→2,500 (developer products); hats by rarity 30/75/175/400/900/2,250; Summit_Crown not sold. Full table, player-type model and open proposals (missed-day rule, repeat-summit faucet): [[Rubber-Tower-Squishies-Economy]]. Per [[Pay-To-Win-Boundaries]], any future random item bought with this currency (eggs and similar) needs disclosed odds and a restricted-player path; Holden wants those avoided for now.

## 7. Rewards & randomness
- N/A for v1 unless Holden wants eggs or crates. If added later, odds must be disclosed (see [[Reward-Schedules]]).

## 8. Difficulty
- (USER) Free falls with checkpoints; 3 to 4 big checkpoints on the whole map, plus a few free soft platforms between them: platforms you can fall onto, but you can never spawn or respawn at them.
- (DRAFT) Section difficulty ramps with height. ⚠️ With only 3 to 4 checkpoints, each segment is long; a fall near the end of a segment could lose a lot of progress. Playtest segment length and consider extra "soft" safe platforms that do not count as checkpoints.
- Movement constants (WalkSpeed, JumpPower, Gravity): UNDECIDED; measure before tuning ([[Difficulty-And-Mastery]]).
- Ragdoll rules (USER): the player's own avatar is the ragdoll. (USER) It ragdolls mainly on falls and pushes, plus certain parts or areas of the tower that make you wobble for a bit or bounce you. Which areas and how often: UNDECIDED.
- (USER, 2026-10-04) A fall ragdolls at 12 studs; you get up 1.5 s after landing (tune later). R6 and R15 avatars are both supported. 16 players per server.
- (USER, 2026-10-04) Bounce pads launch you and do not ragdoll. Other platforms and structures will have their own effects, for example ice that makes you slide a bit. Which effects and where: UNDECIDED.
- (DRAFT, built in the prototype) A fall is measured from where you left the ground, so normal jumps and pads that land at the same height never ragdoll. A ragdoll ends after 8 s at most. A shove on someone already ragdolled extends the ragdoll. Details: [[Avatar-Ragdoll]].

## 9. Idle/offline
- N/A: an active climbing game.

## 10. Monetisation
- (USER) Holden wants "trolly" gamepasses with extra interactions. His ideas: a slippery banana peel a player can leave behind; picking up a friend to carry or throw. Rules and prices: UNDECIDED. No prices proposed until Roblox's current price rules are checked. ⚠️ verify.
- (USER) Liked from the Ideas Bank: Buddy Carry (uses an accept prompt), banana peel (30-second cooldown after placing; one on the map per player; placing a new one after the cooldown removes the old one), cosmetics (more brainstorming later), skip-checkpoint pass. Paying to reach the top earns a joke or show-off title (examples "Millionaire", "False Conqueror"; names undecided); a skipper still unlocks the next worlds the same way. 3 basic emotes are free (which three: later, low priority) and other emotes are sold in an emote pack (⚠️ verify how paid emotes are sold). Eggs and other random items avoided for now (agreed).
- (DRAFT) Suggested guardrails: affect only players who opt in or friends, cooldowns, no effect near checkpoints or the summit, capped force. Carry/throw can throw players off the tower, so the receiving player needs a way out of the grab.
- (DRAFT) Prefer novelty and cosmetic passes (trails, ragdoll styles, funny effects and sounds) over passes that let payers grief other players. Free path to beating every world.
- Reference: Troll Ragdoll Tower sells cosmetic and convenience passes from 2 to 199 Robux (Rolimons, 2026-10-04), shown only as an example.

## 11. Retention systems
- (USER) Hooks: friend boost, unlockable titles, server-wide twist events such as low gravity, a unique mechanic per world. Speed boards: Holden unsure, not included for now. Targets not set.

## 12. Live ops & content plan
- (USER) Launch with one tall map; add new maps/worlds in future updates. Cadence: UNDECIDED.

## 13. Tech & data (DRAFT)
- Server-authoritative: checkpoint progress, world unlocks, push validation (range, cooldown, force cap). Client sends only intent.
- Data schema v1 (draft): `schemaVersion`, `highestCheckpoint`, `worldsUnlocked`, `clears`, `cosmetics`. See [[Data-Persistence-DataStores-And-ProfileStore]].
- Ragdoll: built in phase 1. Live avatars use AnimationConstraint joints with built-in sockets (verified in Studio 2026-10-04). The server decides, the owning client moves the body. See [[Avatar-Ragdoll]]. The phone test is still pending.

## 14. Analytics
- UNDECIDED. Minimum: checkpoint reached funnel, falls per segment, first-clear rate, session length. See [[Analytics-And-Instrumentation]].

Brainstormed options for wobble areas, interactions and passes: [[Rubber-Tower-Ideas-Bank]].

## 15. Risks & open questions
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Push move used to grief | High (guess) | Players quit | Cooldown, capped force, short range, optional friends-only or off toggle (UNDECIDED), checkpoint respawn |
| Avatar ragdoll inconsistent or costly on phones | Medium (guess) | Laggy or broken wobble | Prototype first, cap ragdolls, test low-end phone |
| Long checkpoint gaps frustrate | Medium (guess) | Early churn | Playtest, add soft safe platforms |
| Moderation for young teens | Medium | Policy or reputation | Keep interaction non-violent and silly; review Roblox policy ⚠️ verify |
| One map is thin for retention | Medium | Low return rate | Plan world 2 before launch, cosmetics |

Open questions are listed in [[Rubber-Tower]].

## 16. Milestones
See [[Rubber-Tower-Build-Plan]] (DRAFT, awaiting Holden's approval).

## Changelog
- 2026-10-04: v0.1 created from the brainstorm and Holden's answers; no mechanics approved beyond (USER) lines.
- 2026-10-04: added Holden's build answers (12-stud fall, 1.5 s recovery, R6 and R15, 16 players, bounce pads launch only, effect platforms such as ice later) and the prototype's draft ragdoll rules.
