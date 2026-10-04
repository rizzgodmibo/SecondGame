---
title: Fish a Monster Saving and Offline Income
date: 2026-10-02
tags: [roblox, datastore, profilestore]
project: Fish a Monster
---
# Fish a Monster Saving and Offline Income

## Decisions
- **ProfileStore** (`lm-loleris/profilestore@1.0.3`, the official package), not a hand-written save. Holden approved installing it.
- **Separate stores:** `PlayerData_Studio` for testing and `PlayerData_Live` for real players, so tests never touch live saves.
- **Load failure kicks the player** ("Your data couldn't load"), rather than letting them play on a blank profile that would overwrite their real save.
- A **repair step** on load fixes references to removed rods and bait, negative coins, missing fields, duplicate ids and over-cap aquariums.
- **Offline income cap:** 8 hours (Holden's decision). Uses the server clock.

## Bug found in testing
New profiles started with `lastSeen = 0` (1970), so a fresh profile could collect the full 8 h of offline income. Fix: a missing, zero or future `lastSeen` counts as "now" on load.

## Migration
Step 9 introduced save v2: the `discovered` list became per-species records (times caught, best size). It was tested on a real v1 save made with the old code before the change.

Requires Studio's **Game Settings → Security → Enable Studio Access to API Services**.

Related: [[Fish a Monster Build Steps]], [[Roblox Purchase Receipt Handling]]
