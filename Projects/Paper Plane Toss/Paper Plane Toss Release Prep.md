---
title: Paper Plane Toss Release Prep
date: 2026-10-03
tags: [roblox, paper-plane-toss, release, badges, audit]
project: Paper Plane Toss
---
# Paper Plane Toss Release Prep (Phase 12)

Holden wants to launch on 2026-10-03, the same day as this prep. Codex makes the two thumbnails and the game icon.

## Decisions (Holden)
- **Server size:** 8 players. It's set in the Creator Hub, not in code. The place file still says 60, and the Creator Hub setting overrides it.
- **Badges:** basic ones like Steal an Egg (welcome + top-rarity hatches + best items).
  - Created: Welcome, Hatched Epic, Hatched Legendary, Taco Jet, First Rebirth.
  - "Flight 1K" was skipped because creating more badges that day would cost Robux. Its id stays 0, and the code skips it.
- **Alt-account challenge farming:** left as is.

## Badges
![[Badges v1.png|700]]

- **Icons:** `art/make_badges.py` composites existing UI renders (pets, planes, rebirth, trophy) into round medals at 512×512. Roblox crops badge icons to a circle, so everything stays inside the ring.
- **How they're awarded:** `Systems/Badges` never hooks into the hatch, buy or rebirth code. Every 4 s it checks each player's save against `Config.Badges`, and checks owned badges once per session with `UserHasBadgeAsync`. This also awards players who reached a goal before badges existed.
- **When a lookup fails**, the badge counts as owned for that session, so a BadgeService outage can't cause an award spam loop.

```lua
Config.Badges = {
	Welcome = { id = 4352299945750583, kind = "join" },
	HatchedLegendary = { id = 2438940321753222, kind = "hatchRarity", value = "Legendary" },
	-- id 0 = not created yet: skipped
}
```

## Release audit (whole codebase, roblox-reviewer)
Saving, receipts, server authority and leaks were all clean. Fixed:
- **Training:** every tick pushed the *whole* profile to the client, making about 14 menus redraw every second per player on a pad. Glide is now added silently and synced every 4 s. In a Studio test the client got 2 updates in 10 s instead of 10.
- **Cloud puffs:** only drawn for your own flight. With 8 players on Auto Throw, other players' flights spawned hundreds of puffs on phones.
- **Landing cleanup:** scheduled before `onLanded`, and `onLanded` runs in a `pcall`, so a HUD error can't leave the camera stuck.
- **Smaller fixes:** a rate limiter on the last remote without one, a whole-number check on the challenge-invite user id, `WaitForChild` timeouts, and pets republish only when equipped pets change.
- **Launch blocker:** `Config.FeaturedEgg.launched` must be set to `true` in the build that goes public, or the Galaxy Egg never goes on sale.

## Launch checklist
1. Creator Hub: thumbnails and icon, description (`design/store_description.md`), genre Simulator, devices, server size 8, maturity questionnaire.
2. Phone check of every panel, then a test with 2+ players. Done 2026-10-03: both fine.
3. Transferred the experience to Holden's group (2026-10-03). All sounds and SFX checked on a live server: fine.
4. **LAUNCHED 2026-10-03:** `Config.FeaturedEgg.launched = true`, then published.
5. After 14 days: take Galaxy Egg 1 / 3 / 10 off sale.

Related: [[Paper Plane Toss]], [[Paper Plane Toss Monetization]], [[Paper Plane Toss Thumbnails and Game Icon]], [[2026-10-03 Paper Plane Toss Phone Playtest]]

Sources: [Steal An Egg badges](https://stealanegg.net/badges/)

## Launch-day catch: duplicate clothing
Just before publishing, each cutscene bully turned out to have **two** Shirts and two Pants: the old default ones plus the new outfit. That's why the Studio screenshots showed random mixes, like Kyle in a green jersey when he should wear a red hoodie.
- **Cause:** `Humanoid:ApplyDescription` on these pre-built rigs adds new clothing without removing the clothing instances that were already there.
- **Fix:** after `ApplyDescription` on a rig that already has clothes, delete any Shirt / Pants whose template doesn't match the description.
- **Also:** Studio edits to the place that weren't saved or published (like the Sensei name-tag fix) were gone when Studio reopened after the group transfer. Re-check place-file changes before publishing.

## Launch result (2026-10-03, Saturday)
- **Live:** https://www.roblox.com/games/100823596840978/1-Paper-Plane-Toss. Published from Studio; the Welcome badge fired and the Galaxy Egg shows on the live server.
- **Committed:** the first commit, `fab4e93`.
- **Next (Sunday 2026-10-04):**
  - Check Creator Hub → Monitoring → Error Report, plus Analytics (visits, session length) and one purchase.
  - Then start the ads test from [[Roblox Ads Strategy]]: one Plays campaign, both thumbnails, $5–10/day for 3–5 days.
  - Bring click rate, cost per play and D1 retention back to Claude.
- **Day 14 (about 2026-10-17):** take Galaxy Egg 1 / 3 / 10 off sale.
