---
title: Paper Plane Toss Monetization
date: 2026-10-03
tags: [roblox, monetization, policy]
project: Paper Plane Toss
---
# Paper Plane Toss Monetization (Phase 10)

The strategy copies the reference games ("just as pay-to-win") — Holden's call.

## 10a: Game passes (created and on sale)
| Pass | R$ |
|---|---|
| x2 Tokens | 399 |
| x2 Glide | 449 |
| VIP (+50% Tokens, tag, gold trail) | 349 |
| Golden Pad (x10 training) | 249 |
| Auto Throw | 199 |
| +1 Pet Slot | 149 |

- **Historical test advice:** use a separate non-owner account to test buying. The earlier blanket statement that the creator automatically owns every pass is unverified here; do not generalise it to group-owned passes or other contexts.
- **Auto Throw pauses** during challenges and the tutorial (Holden's decision after the audit).

## 10b: Developer products (ids in `Config.Products`)
- 2x Glide and 2x Tokens potions: 15 min, 49 R$ each, stacking.
- Token packs that scale with level (49 / 199 / 799 R$). The floor is 25 Tokens per throw's worth (DRAFT).
- Storm Egg packs of 1 / 3 / 10 (99 / 249 / 749 R$).
- One-time starter pack, 99 R$.

![[Creator Hub Pass IDs.png|380]] ![[Creator Hub Product IDs.png|380]]
![[Render Golden Pad.png|250]]

## Rules followed
- **Historical implementation intent:** show paid-egg odds and hide restricted offers using PolicyService. This is a per-user policy result, not simply a country check. Current inspection found validation/enforcement review gaps; see [[Roblox Monetisation Policy Pricing and Revenue]]. Indirect paid-currency random rewards must also be considered. This note is not a compliance certification.
- **No paid skip for the intro cutscene.**
- Save v5 adds passes, receipt ids, potion timers and the starter-pack flag.

## 10c (in progress)
Free codes (for example RELEASE) and a group reward chest for the "Pocket Parade" group (id 232308005). Holden wants it to need a group join plus a like or favourite.

![[Render Chest.png|220]] ![[Group Chest In Game.png|260]]

Receipt-handling lessons from the audit: [[Roblox Purchase Receipt Handling]].

Related: [[Paper Plane Toss]], [[Challenges Instead of Wagers]]


Pricing, DevEx and policy reuse guidance: [[Roblox Monetisation Policy Pricing and Revenue]]. Listed prices above are historical configured prices, not a guarantee of each player’s current regional price.

