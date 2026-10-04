---
title: Fish a Monster Pre-Publish Review
date: 2026-10-02
tags: [roblox, code-review, performance]
project: Fish a Monster
---
# Fish a Monster Pre-Publish Review

A read-only `roblox-reviewer` audit after step 9 found no critical or high issues: 3 medium and 7 low. Fixes committed as 583bf47 and verified with 13 playtest checks.

## Worth remembering
- **Server-side bobber shake** replicated every frame to everyone. Fix: the server sets a "biting" flag and each client animates the bobber locally.
- **Panels rebuilt every row on each 5 s payout**, so a Sell tap on mobile could land on a row that had just been deleted. Fix: rebuild rows only when their content changes.
- **Calling a module from the command bar** loads a separate copy and can create a duplicate Remotes folder. `Remotes` now reuses an existing folder.
- **Rate limiter leak** when a request arrives right after a player leaves.
- Fishing remotes got a rate limiter for consistency; the save session got ProfileStore's real type instead of `any`.

## Not fixed, by choice
- #4: zone width hints at rarity (accepted).
- #9: server-side cast position check (deferred until more zones exist).

Related: [[Fish a Monster Catch and Reel Design]], [[Roblox Studio MCP Quirks]]
