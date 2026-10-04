---
title: Fish a Monster Catch and Reel Design
date: 2026-10-02
tags: [roblox, game-design, security]
project: Fish a Monster
---
# Fish a Monster Catch and Reel Design

## Catch roll
- Rarity odds 60 / 25 / 10 / 4 / 0.9 / 0.1 %. Rod luck plus bait luck multiplies Rare and above, then everything is renormalised to 100%.
- **First cast** is always a quick, easy Common. It's detected as "no species discovered yet", so no extra save field is needed.
- The odds math lives in a shared `RarityOdds` module, so the shop shows exactly the odds the server uses. This also covers Roblox's odds-disclosure rules.

## Reel minigame (Holden's choices)
- **Hits needed** come from the zone (`reelHits`); the Pro rod needs 1 fewer.
- **Rarer monsters shrink the green zone.** Because of this, the server rolls the catch **at the bite** instead of after the reel. The result stays secret on the server; the zone width is the only hint.
- Bait is used up at the bite, even if the monster escapes. Cancelling before a bite is free.

## Security calls
- The server owns timing and results, and rejects reel results faster than humanly possible or later than the time limit plus lag grace.
- **Accepted risk:** the minigame runs on the client, so an exploiter can always claim a win. They still can't fish faster than a perfect player.
- **Accepted (review #4):** zone width hints at rarity, so cancel-and-recast is possible.
- **Deferred (review #9):** validate cast position and zone on the server once there are several zones.

## Backlog Holden asked for
Reel UI and sound polish, deferred to a game-feel pass.

Related: [[Fish a Monster Build Steps]], [[Fish a Monster Pre-Publish Review]]
