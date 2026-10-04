---
title: Challenges Instead of Wagers
date: 2026-10-02
tags: [roblox, game-design, policy, leaderboards]
project: Paper Plane Toss
---
# Challenges Instead of Wagers

Holden wanted players to **bet** against each other on who throws further. That isn't allowed: Roblox bans wagering anything that can be bought with Robux, and a throw is partly luck. Flight Tokens can be bought, so a wager would count as gambling, which is extra risky with a young-teen audience.

**Built instead (Phase 5b):** a challenge with a prize paid by the game. The loser loses nothing.

- **Coach NPC** unlocks challenges at **Level 20**. Level was chosen over Tokens because Glide only goes up, while Tokens get spent.
- Click a player's name. The invite shows top-middle of their screen (the design later moved it to the centre, always on top) with **30 s** to accept.
- Both players get 20 s to throw; the longer flight wins. If only one throws, they win; a tie is a draw; if someone leaves, it's cancelled.
- **Prize:** the winner's challenge throw's Tokens again, plus 1 Trophy, which can't be bought. The prize size is still DRAFT.
- **Auto Throw pauses during matches** (decided in Phase 10).

## Leaderboards
Three global top-50 boards as 3D signs in the hub: **Trophies, Rebirths, Glide**. They refresh every 2 min; Glide is written at most once a minute per player to stay within DataStore limits. Each row shows the player's avatar headshot. On the island they sit in an arc on the rim, angled so all three can be read from the plaza (Holden's sketch).

| Reference | Holden's sketch | Our boards |
|---|---|---|
| ![[Ref Steal an Egg Leaderboard.png\|180]] | ![[Sketch Leaderboard Arc.png\|220]] | ![[Render Leaderboards.png\|260]] |

Related: [[Paper Plane Toss]], [[Paper Plane Toss Monetization]]
