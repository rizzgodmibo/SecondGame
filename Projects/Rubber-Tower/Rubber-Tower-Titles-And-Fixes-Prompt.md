---
tags: [project/rubber-tower, design/titles]
status: final
updated: 2026-10-06
---
# Rubber Tower: batch (h) fixes + economy decisions + titles prompt

Paste the block into Claude Code.

```
Batch (h) review: good self-critique. Here's what's next.

PART 1: FIX WHAT'S STILL WEAK (batch h)
- Secret room: make the outside interesting too (a crooked door, a glowing keyhole, a duck-shaped window, vines), and render the inside (disco ball + duck shrine) with a cutaway shot.
- Segment gates: chunkier welcome arches, thick pillars, a big themed top piece per segment and a blank sign face.
- Hedge: rebuild as a puffy, clipped hedge with leaf clusters and a few flowers, not a log. Then give the hub decor a snowy version (not just the hedge) for the seasonal set.
- Moon lantern: make the face bigger and readable.
- Flags: add emblem-only versions for small icons.
- The 3 tri-budget overruns are fine as they are.

PART 2: ECONOMY DECISIONS (record as USER in [[Rubber-Tower]], [[Rubber-Tower-Squishies-Economy]] and Config)
1. Missed daily: RESTART at day 1. Keep it as it is in Config.
2. Replay reward: YES, +20 Squishies for reaching the summit again, once per day.
3. Titles: the full list is below. Add the title payouts and the replay reward to the economy model and re-run it. Tell me how much faster the hats get with titles included.

PART 3: TITLES
Rules:
- Rarity uses the same 6 tiers and colours as the hats. Payouts use the locked amounts: Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300. Every title pays once.
- Anything that can be cheated (summit without checkpoints, speed runs, falls) must be checked on the server (see reviewer note M1 in [[Rubber-Tower-Build-Status]]: climb trace + skippedCheckpoints flag).
- One title equipped at a time, picked in a Titles menu. Locked titles show how to unlock them.
- Names are drafts. Keep them short (max ~16 characters) so they fit above a head on a phone, and suggest better/funnier names if you have them.

| Title | How to get it | Rarity |
|---|---|---|
| Wobbly Beginner | Finish the tutorial / first jump | Common |
| Meadow Hopper | Reach CP1 | Common |
| Fresh Fit | Buy your first hat | Common |
| Millionaire | Skip a checkpoint with Robux (joke title) | Common |
| False Conqueror | Reach the summit after using a skip (joke title) | Common |
| Mushroom Muncher | Reach CP2 | Uncommon |
| Bonk Survivor | Fall 100 times | Uncommon |
| Helping Hand | Give 10 hand-ups | Uncommon |
| Mushroom Fashion | Buy a halfway-only hat | Uncommon |
| Loyal Squish | Finish a 7-day daily streak | Uncommon |
| Disco Duck | Dance (emote) in the secret room | Uncommon |
| Moonwalker | Reach a checkpoint during a low-gravity event | Uncommon |
| Frostbitten | Reach CP3 | Rare |
| Pro Faller | Fall 1,000 times | Rare |
| Long Way Down | Fall from segment 4 all the way to the ground floor | Rare |
| Pushy | Shove 5 different players off a ledge (approved) | Rare |
| Banana Bandit | 10 players slip on your banana peel (pass owners) | Rare |
| Hat Collector | Own 10 hats | Rare |
| Secret Finder | Find the secret room | Rare |
| Rubber Champion | Reach the summit | Epic |
| Party Starter | Invite 4+ friends (fallback approved: 3 friends in the server) | Epic |
| Daily Wobbler | Finish 4 full daily streaks | Epic |
| Duck Whisperer | Find every hidden rubber duck on the map | Epic |
| Squishmaster | Reach the summit 10 times | Legendary |
| Speedy Noodle | Reach the summit in under 12 minutes (tune by playtest) | Legendary |
| Checkpoint Who? | Reach the top without claiming any checkpoint (approved) | Mythic |
| Mad Hatter | Own every sold hat | Mythic |
- Hidden rubber ducks for Duck Whisperer: add a small Hidden_Duck prop (a few colour variants) to batch (h) if it isn't there.
- Rough total if a player gets everything: ~2,975 Squishies. Check that's okay against the economy.

TITLE ABOVE THE HEAD: REDO IT
I don't like how the current title model looks. Titles in real Roblox games are UI (BillboardGui), not a 3D plaque. Keep Title_Plaque only as a world prop.
- Research first: look at [[X-HUD-And-Menus-UI]], [[UI-And-Gameplay-Reference]], [[UI-Polish-And-Juice]] and Assets/Reference-Captures (Roblox-Games, X/ui-hud, X/ui-menus). The best one in the vault is the "Shiny Spotter" title in Projects/Fish a Monster/attachments/Ref Mossy Rocks and Curved Trees.png: a rounded banner with a rarity outline, a badge icon on the left, bold outlined text, and the player name underneath. Capture more in-game title/nameplate examples from top Roblox games (e.g. Pet Simulator 99, Bee Swarm Simulator, Blox Fruits, Grow a Garden, Islands) into Assets/Reference-Captures/Titles with sources, and say what you're taking from each.
- Design spec:
  - A banner above the head: title on top, player name below. A rarity-coloured border and badge icon on the left (a small icon per title category: climb, social, collection, secret, joke, daily).
  - Bold rounded font with a thick UIStroke, readable on a phone at about 30 studs.
  - Rarity effects: Common plain grey, Uncommon green, Rare blue with a soft shine, Epic purple animated gradient, Legendary gold shimmer + sparkles, Mythic animated rainbow/pink gradient + sparkles.
  - It must sit ABOVE tall hats (the tower hat, the castle, the planet): offset it by the equipped hat's height.
  - It has to behave during ragdoll: follow the body smoothly without spinning or jittering.
  - Fade out with distance (MaxDistance), stay small enough not to block the climb, and look fine with 16 players on screen.
- Make 2–3 style mockups first (render them as images over a real-looking scene with avatars), show me, and wait for my pick before building it in code.

PROCESS
- Fixes and mockups first, then stop for my review. Still no uploads.
- Log everything in [[Rubber-Tower]], [[Rubber-Tower-Squishies-Economy]] and [[Rubber-Tower-Valley-Kit]].
```
