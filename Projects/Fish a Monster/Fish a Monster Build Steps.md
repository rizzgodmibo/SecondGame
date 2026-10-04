---
title: Fish a Monster Build Steps
date: 2026-10-01
tags: [roblox, build-log]
project: Fish a Monster
---
# Fish a Monster Build Steps

Built in one session (Oct 1 evening into Oct 2), one system at a time: plan and file list, Holden's approval, build, Studio playtest, commit.

| Step | System | Commit |
|---|---|---|
| 1 | Rojo, Rokit, Selene, StyLua scaffold, `.gitattributes` forcing LF | e39b154, cfa1a90 |
| 2 | Types and Config: 10 placeholder species, 6 rarities, sizes, rods, bait; startup `ConfigCheck` | 636beeb |
| 3 | Server catch roll, checked with 100k simulated rolls | 929f610 |
| 4 | Cast, bite and reel minigame | 0f7e4e0 |
| 5 | Bucket inventory, sell and keep, reel difficulty scaling (34 checks) | 2b7edd0 |
| 6 | Aquarium income, 8 h offline cap | a1433a9 |
| 7 | Shop: rods, bait, aquarium slots with exact odds shown | 303586d |
| 8 | ProfileStore saving, plus a lastSeen fix | 25d1683, df29c63 |
| 9 | Collection book and per-species records (save v2) | 11c5d25 |
| Review | Pre-publish fixes | 583bf47 |

## Problems solved during setup
- **Rojo "needs to connect":** nothing to connect to until Rokit/Rojo were installed and a project existed.
- **"Script injection permission denied":** turn on Script Injection for Rojo in Manage Plugins.
- **Leftover template scripts** in the place (a second bootstrap) would have run alongside ours. Holden deleted them in Explorer, because Studio deletions through MCP are blocked.
- **Line endings:** git would convert files to CRLF and break `stylua --check`. Fixed with `* text=auto eol=lf`.

Testing approach: see [[Studio Only Dev Test Scripts]].

Related: [[Fish a Monster Catch and Reel Design]], [[Fish a Monster Saving and Offline Income]], [[Rojo Workflow Gotchas]]
