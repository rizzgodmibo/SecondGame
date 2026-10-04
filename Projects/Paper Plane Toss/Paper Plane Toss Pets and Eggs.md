---
title: Paper Plane Toss Pets and Eggs
date: 2026-10-03
tags: [roblox, pets, art, game-design]
project: Paper Plane Toss
---
# Paper Plane Toss Pets and Eggs (Phase 8)

## Decisions
- Pets boost **Glide**. Boosts add together and multiply bounces and training.
- **3 eggs × 5 sky animals**, 3 equip slots (4 with the pass).
- **Odds:** 50 / 30 / 14 / 5 / 1 % for every egg. Verified over 10,000 rolls.
- **Eggs:** Cloud (250 Tokens), Sky (5K), Storm (100K). Boosts range from +5% (Cloud Bunny) to +3000% (Storm Dragon).
- Inventory cap 100 (DRAFT).

## Art
- Chunky, rounded, cute low-poly animals with a sky twist (cloud tail, balloons, storm cloud). Holden: "loving this style".
- **To make the game match the renders,** the dark outline is **baked into each mesh** as an inverted hull, which works because Roblox only draws front faces. Blender previews need backface culling turned on to show the same thing.
- Weak points fixed after review: the Storm Frog's belly smudge, and Sky Whale and Storm Dragon looking too much like one colour.

![[Render Pets Cloud.png|400]] ![[Render Pets Sky.png|400]]
![[Render Pets Storm.png|400]] ![[Render Pets Eggs.png|400]]

## Systems
- Hatch screen: wobble, flash, rarity rays; sparkles for Epic and Legendary.
- Pets menu with My Pets and Index tabs; Equip Best.
- Pets follow their owner and everyone sees them, via an "EquippedPets" player attribute.
- Save v4 adds `pets`, `equippedPets`, `petIndex`, `nextPetUid`.
- Measured boost: exactly ×1.50 with +50% equipped, on both throws and training.

Related: [[Paper Plane Toss Progression Numbers]], [[Paper Plane Toss Monetization]]
