---
title: Studio Only Dev Test Scripts
date: 2026-10-02
tags: [roblox, testing, qa]
---
# Studio Only Dev Test Scripts

The testing method that worked once `execute_luau` couldn't fire remotes (see [[Roblox Studio MCP Quirks]]):

1. Write a temporary `src/client/Dev*.client.luau` (or a server `DevCheats` / `DevGrant` script) gated by `RunService:IsStudio()`.
2. Rojo syncs it in. Playtest and read PASS/FAIL lines from Output. Tests fire the **real remotes**, the way an exploiter's client would: junk args, other players' ids, spam.
3. **Delete it, and confirm git is clean.** Never commit it.
4. If it changed Holden's Studio save (granting coins or passes, rewinding the tutorial), restore the save and confirm it survives a restart.

Other habits:
- Check odds with 10k–100k simulated rolls.
- Test a real old-version save upgrading, not a hand-made table.
- Studio saves go to a separate DataStore, so live data is never touched.

Used in [[Fish a Monster Build Steps]] and every [[Paper Plane Toss]] phase.
