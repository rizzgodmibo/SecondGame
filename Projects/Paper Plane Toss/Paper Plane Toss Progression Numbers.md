---
title: Paper Plane Toss Progression Numbers
date: 2026-10-02
tags: [roblox, game-design, economy, balancing]
project: Paper Plane Toss
---
# Paper Plane Toss Progression Numbers

All numbers were approved by Holden unless marked DRAFT. The values live in `Config.luau`.

## Tokens
`max(1, floor(distance / 10 × multipliers))`. The first throw pays about 17.

## Glide levels (copy of Stone Skipping)
- Total Glide is your XP.
- **Multiplier:** +0.02 per level up to ×1.1 at level 6, then **+1 per level** (×81.1 at level 86, ×110.1 at level 115). It's global: it boosts bounces, training and Tokens.
- **Cumulative Glide to reach level L (not the marginal cost of one level-up):** `10 × (1.25^(L−1) − 1) / 0.25`, so each level needs **25% more** than the last.

## Training pad (like Steal an Egg's treadmills)
Stand on the pad to gain Glide every second. Tier gains are Steal an Egg's halved: +1, 2.5, 6, 15, 40… Tier costs are free, 150, 2.5K, 50K, 1.2M. Tiers 6–10 wait for later multipliers.

## 12 planes in 6 tiers
Paper (free) → Notebook → Newspaper → Sticky Note → Comic Page → Origami Crane → Pizza Box → Homework → Golden Ticket → Toast → Dragon Scroll → Taco Jet. Glide per bounce goes from +1 up to +300K. Prices are **Stone Skipping's ×5**.

![[Render Planes.png|450]]

## Lesson: simulate before approving a curve
With a 15% level curve, a simulated player who buys every plane as soon as they can afford it got all 12 in about an hour (level 151). The compounding loop is planes → levels → multiplier → everything. At 25% growth with ×5 prices, the top plane takes about 6 hours. Run a progression sim whenever a new multiplier source is added (pets, rebirth, passes).

## Bug
`Format.number` stripped zeros from whole numbers, so "300K" showed as "3K". Fixed with a `trimDecimals` helper.

Related: [[Paper Plane Toss Pets and Eggs]], [[Paper Plane Toss Rebirth]], [[Paper Plane Toss Monetization]]

## Reuse qualification (2026-10-03)

The one-hour and six-hour simulation results above are historical reports. This pass did not locate or run their simulator or verify its complete assumptions. Do not treat six hours as a measured current-player completion time after pets, passes and rebirth changes. Record configuration, action timing, purchase policy and boost combinations for a reproducible rerun.

The cumulative-threshold interpretation was checked in C:\Users\holde\Downloads\SecondGame\src\shared\Levels.luau. Use [[Roblox Economy Modelling and Progression Tests]] to distinguish marginal costs, cumulative XP and compounding earning rates.
