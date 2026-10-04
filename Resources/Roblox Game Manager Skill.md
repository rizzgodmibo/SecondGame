---
tags: [resources/tooling, meta/playbook, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: high
---
# Roblox Game Manager Skill

A Claude Code skill (`roblox-game-manager`) that runs a whole game build through [[Game-Building-Playbook]], handing each phase to the right skill and stopping at Holden's approval gates.
Built 2026-10-04 as the last skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.8, the "create-roblox-game" manager).

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-game-manager\`. Per-game state lives in the vault: `Projects/<Game>/Build-Status.md` (from the skill's template).
- **Every session:** read Build-Status → say phase, open gates and the proposed next step → wait for Holden → do it with the right skill → record evidence.
- **Gates need evidence** quoted in Build-Status: a `GATE PASS` line, a self-test result, a playtest log, or Holden's words.
- **Decisions log** keeps `USER:` (Holden decided) apart from `PROPOSAL:` (Claude suggested). Mechanics and lore are never invented silently.
- **Phase 4's "spreadsheet sim" gate is runnable:** a pure economy module + a Lune spec that simulates a player and checks time-to-X (example in the skill's `templates/sim/`, with placeholder numbers).
- **Status: self-test PASSED 2026-10-04** (all vault links and skills resolve, the sim example runs). **No active game:** Holden has no idea yet, and phase 0 starts when he does.

## Phase → skill map
| Phase | Skills / notes |
|---|---|
| 0 Concept | [[Genre-Positioning]], [[Genre-Playbooks]], [[Thumbnails-And-Icons]] → `Concept.md` |
| 1 GDD | [[Game-Design-Doc-Template]], [[Core-Loops]], [[Onboarding-And-First-60-Seconds]] |
| 2 Bootstrap | `roblox-dev:setup`, [[Project-Bootstrap-Checklist]], [[Roblox Code Gate Skill]] (`--scaffold` must pass) |
| 3 Vertical slice | `roblox-dev:new-system`, [[Roblox Code Gate Skill]], [[Roblox Map Audit Skill]], [[Roblox Asset Pipeline Skill]], [[Roblox UI Checker Skill]] |
| 4 Meta + economy | [[Progression-Curves]], [[Economy-Design-Sinks-And-Faucets]], simulation specs |
| 5 Polish + art | [[Roblox VFX Review Skill]], [[Roblox Sound Library Skill]], [[Roblox UI Checker Skill]], Holden's art review |
| 6 Monetisation | [[Monetisation-Design-Checklist]], [[ProcessReceipt-Handling]] |
| 7–9 Launch | Checklists only. Publishing and ad spend are Holden's actions |

## The full skill set from the video (2026-10-04)
| Video skill | Here | Status |
|---|---|---|
| Code | [[Roblox Code Gate Skill]] | Self-test passed |
| UI | [[Roblox UI Checker Skill]] | Studio self-test passed |
| Maps | [[Roblox Map Audit Skill]] | Studio self-test passed |
| VFX | [[Roblox VFX Review Skill]] | Studio self-test passed |
| 3D models | [[Roblox Asset Pipeline Skill]] (Blender only, no AI) | Self-test passed |
| Sound | [[Roblox Sound Library Skill]] | Self-test passed |
| Animation | Parked (Holden: skip), plan kept in [[Gap-Tracker]] | — |
| Manager | this skill | Self-test passed |

None has run on a real game yet. Paper Plane Toss is frozen, and the next game hasn't been chosen.

## Related
- [[Game-Building-Playbook]] · [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[AI-Assisted-Workflow]] · [[Home]]

## Sources
- SyphoDev video, 23:36–24:03: https://www.youtube.com/watch?v=afuKhenJldY
- Self-test output, 2026-10-04.
