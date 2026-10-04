---
title: Paper Plane Toss References and Core Loop
date: 2026-10-02
tags: [roblox, game-design, references]
project: Paper Plane Toss
---
# Paper Plane Toss References and Core Loop

## References (Holden's picks)
- **+1 Stone Skipping (Meow Labs):** *the* main reference. Copy its structure, graphics and UI closely. One Throw button, a stat-driven distance, +1 per bounce, training pads, collectible throwables on pedestals with LOCKED/UNLOCKED signs, pets and eggs, rebirth.
- **Steal an Egg:** UI style (chunky outlined text, green-header panels), leaderboards, treadmill tiers, tutorial style.
- **+1 Loot To Forge:** join cutscene style ("classic Roblox video").
- **Build the Pyramid:** visual style only, not its shared-goal mechanic.

![[Ref Stone Skipping Lobby.webp|600]]
*Stone Skipping's lobby: throwables on pedestals with "+N Skill / price", a CLAIM chest, a World 2 portal.*

![[Ref Steal an Egg Shop UI.webp|500]]
*Steal an Egg's shop: the source of the UI style.*

## Core loop (USER decisions)
- Throw → the plane bounces off air puffs → each bounce gives **+Glide**, which better planes multiply.
- Higher Glide means longer flights. Distance pays **Flight Tokens**.
- One world at launch; distance-unlocked worlds come later.
- **Ghosts are kept** as the differentiator from Stone Skipping, same server only.
- **Monetization:** "just as pay-to-win as the references." This is Holden's explicit choice; don't re-argue it.

## Early-review insight
Holden first described "almost no systems". Matching Stone Skipping made it a much bigger game. That scope change was flagged and then decided by Holden rather than slipped in.

Related: [[Paper Plane Toss]], [[Paper Plane Toss Progression Numbers]]
