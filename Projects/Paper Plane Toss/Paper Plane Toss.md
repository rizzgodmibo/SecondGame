---
title: Paper Plane Toss
date: 2026-10-03
tags: [roblox, game, project-hub, active]
project: Paper Plane Toss
---
# +1 Paper Plane Toss

Holden's second Roblox game, started 2026-10-02 after [[Fish a Monster]] was parked. Press THROW; your paper plane bounces off cloud puffs for +Glide; distance pays Flight Tokens; buy better planes; race same-server ghosts.

- **Folder:** `C:\Users\holde\Downloads\SecondGame`
- **Name:** "+1 Paper Plane Toss" (approved by Holden on Oct 3)
- **Source of truth:** `MASTER_GAME_PLANNING_DOCUMENT.md`. Every line is tagged (USER), (DRAFT) or UNDECIDED, and only (USER) lines are approved. Phases are tracked in `ROADMAP.md`.
- **Live game:** https://www.roblox.com/games/100823596840978/1-Paper-Plane-Toss (group-owned)
- **Code:** git repo started at launch: `fab4e93` "Launch +1 Paper Plane Toss (Phases 0-12)". The SecondGame folder had a `.gitignore` but no repository before that.
- **Status (Oct 3, evening):** Phases 0–11 built (10: passes, products, codes + group chest, Galaxy featured egg; 11: sound & music). Two phone playtests done (see [[2026-10-03 Paper Plane Toss Phone Playtest]]); the mobile HUD v2 (edge-hugging, bottom-left PLANES/AUTO) and the Codex title logo are in. **Launched 2026-10-03** (group-owned; see [[Paper Plane Toss Release Prep]]). Next: ads test per [[Roblox Ads Strategy]], then Galaxy Egg off-sale on day 14.

## Phases
| Phase | What | Note |
|---|---|---|
| 0–1 | Setup, throw and flight | [[Deterministic Flight Sim and Ghosts]] |
| 2 | Same-server ghosts | [[Deterministic Flight Sim and Ghosts]] |
| 3–5 | Tokens, saving, levels, training pad, 12 planes | [[Paper Plane Toss Progression Numbers]] |
| 5b | Challenges and Coach NPC, 3 leaderboards | [[Challenges Instead of Wagers]] |
| 6 | UI redesign, sky island hub, throw lane, lighting | [[Paper Plane Toss UI Redesign]], [[Sky Island Hub and Throw Lane]], [[Shop Gauntlet Loop Plan]] (trial planned, not started) |
| 7 | Join cutscene and Jet's tutorial | [[Join Cutscene and Tutorial]] |
| 8 | Pets and eggs | [[Paper Plane Toss Pets and Eggs]] |
| 9 | Rebirth | [[Paper Plane Toss Rebirth]] |
| 10 | Monetization (passes, products, codes, group chest, Galaxy featured egg) | [[Paper Plane Toss Monetization]] |
| 11 | Sound & music, volume sliders | [[Roblox Audio Pipeline]] |
| Playtest | First phone playtest + mobile layout | [[2026-10-03 Paper Plane Toss Phone Playtest]], [[Roblox Mobile UI Layout]] |

## Design anchors
- [[Paper Plane Toss References and Core Loop]]
- [[Paper Plane Toss Image Gallery]]: every reference, screenshot, video and render

![[Hub Too Bright.webp|450]]
*The sky island hub in game (before the lighting was toned down).*

## Recurring lessons
- **Save the place file.** The first session's work was lost because Studio was an unsaved "Place1". The map, models and lighting live only in the place file, not in git.
- An old Rojo server from Fish a Monster was still running and offered to sync the wrong project into Studio. Click **Dismiss**. ![[Rojo Wrong Project Popup.png|220]]
- See [[Roblox Studio MCP Quirks]], [[Rojo Workflow Gotchas]], [[Studio Only Dev Test Scripts]].
- **Test on a real phone early:** the PC view in Studio hid every mobile layout problem ([[Roblox Mobile UI Layout]]).
- New textures can load grey in game even when approved: see [[Roblox Texture Upload Failures]].
- Logo: Holden's Codex-generated logo (`art/ui/logo_codex.png`, `rbxassetid://132608766133278`) is the arrival title. The Blender version ([[Blender 3D Logo Pipeline]], `rbxassetid://126534297266290`) is kept as a fallback.
