---
tags: [reference/game, design/teardown, monetisation/benchmarks]
status: draft
updated: 2026-10-05
confidence: medium
---
# Steal an Egg: Design and Monetisation Teardown

Steal an Egg (Roblox place 107778070777162, created 2026-07-25) is the game Holden has used as a style and UX reference since Paper Plane Toss (shop, tutorial, leaderboards, badges). This note condenses the game's design from the community one-shot recreation spec in [[Discord-Prompt-Pack-2026-10-05]]. That spec says its [VERIFIED] values were read off the live game on 2026-09-29; **I have not re-checked them**, so treat every number as "per a third-party spec, 2026-09-29". ⚠️ verify anything before relying on it, especially prices (Roblox prices change, and regional pricing applies).

## TL;DR
- **The loop mixes three hits:** train a Speed stat on a treadmill (+1 Speed games) → run down 12 walled biome lanes to steal an egg past a sleeping guardian (Steal a Brainrot's steal-and-run) → hatch it in your pen, where pets earn $/s (Grow a Garden-style timers and mutations).
- **Shared, global rhythm:** a 300 s UTC cycle on every server; a 10 s night teleports everyone home, empties the nests and grows placed eggs ×30, then "ALL EGG RESET!" and fresh eggs; rare spawns are announced server-wide. A built-in reason to check back every 5 minutes.
- **Small servers (7 players), no rebirth, no trading, no codes,** and no raiding bases: PvP only in the field (bat and traps make carriers drop eggs).
- **Shop = featured limited egg (with odds) → 2 passes → speed (a R$3 first multiplier tier, treadmill upgrade, 6 packs) → money (5 packs).** Every Robux item also has a money path or is a pure accelerator.
- **Tutorial:** 7 steps taught with painted ground arrows; a guaranteed Golden tutorial egg that hatches in 5 s; the first goal "Reach the Lake! (900 Speed)". It's the one Paper Plane Toss copied ([[Join Cutscene and Tutorial]]).

## Core loop (per the spec)
1. Train Speed on your own treadmill ("+N/step"; treadmill factor × (trail + Robux multiplier + boosts)).
2. Run down the lane line; each zone has a recommended-Speed sign (red under, green over); it's a soft gate, not a wall.
3. Hold E on an egg in the zone's 5 nests → the sleeping guardian wakes and chases; bigger eggs are heavier and slow you; caught = ragdoll fling, egg returns to the nest.
4. Cross the painted SAFE ZONE line → "You stole an EGG!".
5. Place eggs in your pen; they grow (10 s to 18 h+, scaled by size; ×30 at night; ×2 with a pass); offline growth continues at ×1.
6. Hatch → a pet with random weight (kg), gender and possible mutation; pets roam the pen and pay $/s with "+$" popups.
7. Spend money on pen levels (+1 active pet slot each), treadmill tiers, trails, the fuse machine; complete the Pet Index for cash, Speed and bat skins.

**Zones and speed gates:** Forest 0 · Lake 900 · Desert 10K · Jungle 40K · Snow 170K · Volcano 700K · Abyss Ocean 2.5M · Prehistoric 18M · Cosmic 700M · Cherry Blossom 2.5B · Titan Temple 7B · Angels & Demons 20B (each with a themed voxel guardian: chicken, swan, scorpion, tiger, yeti, Cerberus, whale, T-Rex, skeleton boss, oni tiger, gorilla king, angel/demon). The guardian models in the pack's `Animals` file match 9 of these.

**Pen levels:** 13 levels from $1K (unlocks the treadmill) to $5Qa; active pets 7 → 19; each level enlarges the pen and upgrades the fence (wood → iron → gold → diamond). "+1 EQUIP" is just a shortcut to buy the next level. Max 30 eggs growing at once, 4 studs apart.

**Numbers go big fast:** Speed into the trillions and money into the quadrillions (K, M, B, T, Qa); walk speed from Speed on a log curve, capped.

## Shop (per the spec's "VERIFIED" screenshots, 2026-09-29) ⚠️ verify
| Section | Items and prices |
|---|---|
| Featured (limited egg) | "EXTINCTION EGG", "Limited Time!" countdown, odds tiles 39 / 24 / 18 / 11 / 6.5 / 0.5% + a rainbow "SKELETAL 1%"; R$99 (1) · R$249 (3) · R$799 (10) · R$3,499 (50, struck-through R$5,959); purple gift buttons on each |
| Passes | x2 Growth R$467 · x2 Money R$399 (both giftable) |
| Speed | "DOUBLE Your SPEED x1 ▶ x2" for **R$3** (12 sequential multiplier tiers); "UPGRADE TREADMILL!" R$299 or $75B in-game money; packs +150K R$79 · +1M R$249 · +10M R$699 · +50M R$1,499 · +500M R$1,999 · +1B R$2,999 |
| Money | $24K R$49 · $200K R$99 · $800K R$249 · $4M R$499 · $8M R$799 |
| Elsewhere | instant hatch tiers, INSTANT GROW ALL R$199, 2× earnings 15 min R$99, timed boosts; event luck boosters 49/99/199 |

Patterns worth noting: a **R$3 entry product** to make a first purchase trivial ([[Bundles-And-Starter-Packs]] makes the same argument for starter packs); a **struck-through anchor** on the biggest egg bundle; **gift buttons on everything**; **pack art that grows** with the tier; **money and speed paths for every Robux item** ([[Pay-To-Win-Boundaries]]). The shop layout matches the templates captured in [[X-Shop-And-Seasonal-UI]].

## Systems and UX details worth borrowing
- **A global cycle** computed from `os.time() / 300` on every server, so all resets line up with no messaging ([[Events-And-Seasons]] recommends the same deterministic approach).
- **Server-wide rare announcements** ("A Secret … Egg spawned in Angels!") and a top-left list of recent rare spawns: free excitement and a reason to stay.
- **Per-player instanced nest eggs** (each player sees their own), while carried and dropped eggs are shared, so stealing stays social without griefing beginners.
- **Disconnect while carrying returns the egg** (no disconnect exploit); server-side position sanity (implied speed and teleport checks) because the real game had teleport and auto-steal exploiters ([[Anti-Exploit-And-Server-Authority]]).
- **UI style:** Fredoka One everywhere, a black UIStroke on all text, saturated gradient buttons with a darker stroke, window header colour per window (Shop lime green, Index cyan), red square close button, red "!" badges ([[UI-Polish-And-Juice]]).
- **Purchase intents** for contextual products (instant hatch for a specific egg, gifts): the client registers the intent with the server before the prompt, and the receipt handler resolves it ([[ProcessReceipt-Handling]]).

## What not to copy
- The game itself: clones are deprioritised ([[Discovery-Algorithm]]); take mechanisms, add a twist ([[Genre-Positioning]]).
- Data from decompiled client code (the spec credits a fan wiki's decompiled config for some formulas). IP and ToS risk.
- The voxel part-built art style for Holden's games ([[Art Direction Feedback]]).

## Related
[[One-Shot-Spec-Prompts]] · [[Discord-Prompt-Pack-2026-10-05]] · [[X-Shop-And-Seasonal-UI]] · [[UI-And-Gameplay-Reference]] · [[Join Cutscene and Tutorial]] · [[Post-Mortems-Real-Games]] · [[Pricing-Psychology]]

## Sources
- `STEAL_AN_EGG_ONE_SHOT_PROMPT.md` (community recreation spec; claims live-game screenshots from 2026-09-29, the Roblox API, a fan wiki, Fandom and YouTube guides), in [[Discord-Prompt-Pack-2026-10-05]]. Not independently verified.
