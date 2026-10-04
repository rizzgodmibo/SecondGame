---
title: Paper Plane Toss Rebirth
date: 2026-10-03
tags: [roblox, game-design, progression]
project: Paper Plane Toss
---
# Paper Plane Toss Rebirth (Phase 9)

Shaped like Stone Skipping's rebirth. The numbers are in `Config.Rebirth`.

- **Requirement:** a Glide level that rises with each rebirth: level 30 for the first, +10 per rebirth (USER: 30, 40, 50 ...).
- **Resets:** Glide (back to level 1) and Tokens. **Keeps:** planes, training tier, pets, the Index and trophies.
- **Reward:** a permanent multiplier on Glide and Tokens that stacks with the level, pet and pass multipliers. Observed values: ×1.5 at 1 rebirth, ×2.5 at 3.
- **Multiplier pads:** x2, x4 (needs 3 rebirths) and x8, next to a portal-arch **rebirth station** at `Island.Spots.Rebirth`.
- **HUD:** a chip under the level bar ("x2.5 Rebirth"), hidden until the first rebirth. Holden asked for gold text.
![[Render Rebirth.png|400]]

- `PetBoost` was generalised into a shared `Boosts` module that combines every multiplier source.

Tested: a rebirth at level 43 → 0 Glide and Tokens, rebirths = 1, with planes and pets kept. The server rejects a rebirth when not ready. Pad maths checked: 6 × 4 × 38.1 × 1.5 × 2.5 = 3,429 per tick. (Arithmetic corrected 2026-10-03; this correction does not re-run the historical Studio test.)

Related: [[Paper Plane Toss Progression Numbers]], [[Challenges Instead of Wagers]], [[Roblox Economy Modelling and Progression Tests]]

