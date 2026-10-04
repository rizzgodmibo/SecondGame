---
tags: [resources/tooling, design/level, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: medium
---
# Roblox Map Audit Skill

A Claude Code skill (`roblox-map-audit`) that measures whether a map is playable. It uses the game's real movement numbers and raycasts instead of eyeballing.
Built 2026-10-04 as the second skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.3, "the map skill measures itself").

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-map-audit\`, a user-level skill available in every project.
- **How:** a temporary Studio-only server runner reads the real Humanoid numbers and finds every standable spot with downward raycasts on a 2-stud grid.
  It joins spots with walk, jump and drop moves using real jump physics (× 0.9 margin), then searches from the spawn(s): what's reachable, and what can get back.
- **Checks:** floating, no-footing, unreachable, shouldn't-reach, no-way-out, sight lines, overlap, uneven rings, short falls (only with a game fall band), and spawns with nowhere to stand.
- **Status: self-test PASSED in Studio (2026-10-04)** on a blank Baseplate: 12/12 planted flaws found, 0 false flags, 0.6 s for 4,225 grid columns.
  StyLua, Selene (0/0) and Rojo build pass. **Not yet run on a real game.** `--!strict` is unverified (no type checker installed).
- **Paper Plane Toss is frozen**, so the audit hasn't been run on it.

## What the run measured (fresh Baseplate, default R15 character)
| Number | Value | Source |
|---|---|---|
| WalkSpeed | 16 | `Humanoid.WalkSpeed` (measured) |
| JumpHeight | 7.2 (UseJumpPower off) | `Humanoid.JumpHeight` (measured) |
| Gravity | 196.2 | `Workspace.Gravity` (measured) |
| MaxSlopeAngle | 89 | measured |
| Character height | 5.75 studs | `GetExtentsSize()` (measured) |
| Level running-jump reach | ≈ 8.7 studs ideal, 7.4 with the 0.9 margin | **calculated** from the above, not a physical jump test |
| Auto-step height | 1.5 studs | **guess**, still to measure |

## Using it
- Tag intent before auditing: `MapNoReach` (roofs, out-of-bounds), `MapMustReach` (places players must get to), `MapViewpoint`, `MapRing`, `MapHazard`.
  Ask Holden where those are rather than guessing level design.
- Re-run during a playtest: `workspace:SetAttribute("RunMapAudit", true)` on the Server datamodel.
- Self-test: new Baseplate → `rojo serve` in `fixtures/` (port **34881**) → connect in Edit mode → Play → expect `MAPAUDIT SELFTEST PASS`.

## Pitfalls
- Moves are idealised (perfect running jumps × 0.9, no wall-hops or momentum tricks). Walls more than 2.5 studs above the higher floor block a move.
- Caves under terrain are missed. Water isn't standable. Meshes and wedges count as wide enough to stand on.
- Scripted doors and moving platforms are audited where they currently are.
- The runner is temporary in a game repo: delete it and confirm `git status` is clean.

## Related
- [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[Roblox UI Checker Skill]] · [[Difficulty-And-Mastery]] · [[AI-Assisted-Workflow]]
- [[Studio Only Dev Test Scripts]] · [[Roblox Studio MCP Quirks]] · [[Blender to Roblox Asset Pipeline]]

## Sources
- SyphoDev video, 14:40–18:08: https://www.youtube.com/watch?v=afuKhenJldY
- Physics and thresholds: `references/movement-and-thresholds.md` in the skill.
- Measured values: Studio self-test output, 2026-10-04.
