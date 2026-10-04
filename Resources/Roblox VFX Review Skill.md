---
tags: [resources/tooling, visuals/vfx, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: medium
---
# Roblox VFX Review Skill

A Claude Code skill (`roblox-vfx-review`) that reviews particle effects with a budget lint plus the video's **phase freeze**: fire, wait an exact time, freeze, screenshot.
Built 2026-10-04 as the fourth skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.4).

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-vfx-review\`, a user-level skill.
- **Lint (deterministic):** caps (400/s, 100/s mobile, 20 s lifetime), burst budgets (hit 30, ability 150), ambient ≤ 20/s, streams inside hit effects, invisible emitters, flipbook mismatch, brightness, **timeline gaps**, and a live-particle estimate.
- **Phase freeze (judged):** works in Studio **Edit mode** over MCP. `Emit` → wait → `TimeScale = 0` → `screen_capture`. Timing lands about one frame late, and the report quotes the real time.
- **Library:** 17 building blocks mapped to [[VFX-Texture-Pack]] and Dragon's Hoard textures. They use built-in Studio textures until Holden approves an upload. No toolbox harvesting.
- **Recipes:** hit spark, fireball impact, level-up, ambient fire (numbers from [[VFX-Particles-Beams-Trails]] where a recipe existed).
- **Status: self-test PASSED 2026-10-04** (14 effects, each broken one flagged by exactly its check). **Not yet run on a real game.**

## First phase-freeze result: fireball impact (honest look review)
| Phase | Frozen at | What it showed |
|---|---|---|
| start | 0.065 s | Near-white puff: glow and flame overlap at full LightEmission, so there's little orange or red |
| middle | 0.866 s | Almost empty: flames die by 0.8 s, embers (size 0.3) unreadable from about 18 studs, smoke too dark and faint |
| end | 1.451 s | Empty |

The lint **passed** this effect, which shows why both halves are needed. Suggested retune, **pending Holden's call**:
flame lifetime 0.8–1.2 s, colour biased orange/red with less near-white, embers about 0.6, lighter smoke starting less transparent.

## Observed facts (2026-10-04, Studio Edit mode)
- `ParticleEmitter.Lifetime` accepts 25 and `Rate` accepts 450 when set. Nothing clamps them, so the lint must catch them.
- `require` via MCP `execute_luau` works in Edit mode (contradicts an older note in [[Roblox Studio MCP Quirks]]).
- `require` **caches across MCP calls**: after a Rojo sync you get the old module. Require a fresh clone instead.

## Pitfalls
- "Alive" isn't "visible": the timeline check can pass an effect that looks empty. That's what the screenshots are for.
- Three stills can't show motion problems between phases.
- After uploading the pack, flipbook blocks switch from placeholder (None) to Grid4x4. Re-run the self-test and re-review.

## Related
- [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[VFX-Particles-Beams-Trails]] · [[VFX-Texture-Pack]] · [[Dragons-Hoard-Set]] · [[X-VFX-Reference]]
- [[Roblox UI Checker Skill]] · [[Roblox Map Audit Skill]] · [[Roblox Code Gate Skill]] · [[Roblox Studio MCP Quirks]]

## Sources
- SyphoDev video, 18:08–20:12: https://www.youtube.com/watch?v=afuKhenJldY
- Studio feasibility spike and self-test output, 2026-10-04.
- Budgets: the skill's `references/budgets.md` (most limits come from [[VFX-Particles-Beams-Trails]]).
