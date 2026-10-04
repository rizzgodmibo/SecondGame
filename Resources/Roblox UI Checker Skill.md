---
tags: [resources/tooling, visuals/ui, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: medium
---
# Roblox UI Checker Skill

A Claude Code skill (`roblox-ui-checker`) that checks Roblox UI automatically, using the engine's real layout, at four screen sizes.
Built 2026-10-04 at Holden's request, as the first skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.2 "the checker").

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-ui-checker\`. It's a user-level skill, so it's available in every project. Not in this vault's git.
- **What it flags:** small touch targets (< 44 px), overlaps, off-screen elements, off-centre elements (tagged > 1.5 px, near-misses 1.5–8 px),
  text under 14 px or clipped, default-grey boxes, stray boxes around buttons, and mixed border-stroke thickness.
- **How:** a temporary Studio-only runner prints `UICHECK` lines to Output during a playtest. Each UI layer is also copied into an exact-size frame
  (667×375, 844×390, 1024×768, 1920×1080) and re-fitted by a per-game adapter, so Roblox lays it out at that size.
- **Status: self-test PASSED in Studio (2026-10-04).** The good UI was clean at all 4 sizes; the broken UI flagged exactly its 11 planted issues. StyLua, Selene (0/0) and Rojo build also pass.
  Not yet run on a real game. No type checker is installed, so `--!strict` is unverified.
- **Paper Plane Toss is frozen** (released 2026-10-04, Holden's instruction). The checker has **not** been run on it and must not be without asking.

## Files (in the skill folder)
| File | Purpose |
|---|---|
| `SKILL.md` | When to use it, safety rules, procedure, report format, limitations, traps list |
| `scripts/UICheck.luau` | Checker module (`--!strict`); `check`, `live`, `virtual`, `print`, pure `Geometry` |
| `scripts/DevUICheck.client.luau` | Temporary runner template (Studio-only, Shift+U re-runs) |
| `scripts/adapters/UIKitFit.luau` | Fit adapter for UIKit-style UIs (Root + UIScale, 1280×720, ×1.25 touch, clamp 0.5–1.6) |
| `fixtures/` | Rojo fixture place on **port 34880**: GoodUI (must be clean at all sizes) + BadUI (one known bug per element) + self-test |
| `references/thresholds.md` | Every threshold with its source and ⚠️ verify status |
| `rokit.toml`, `stylua.toml`, `selene.toml` | Same tool versions/style as the game repos |

## Running the self-test
1. Open a **new Baseplate** in Studio (not a game) and make sure the Rojo plugin is installed.
2. Serve the fixture place on its own port:
```bash
cd "C:/Users/holde/.claude/skills/roblox-ui-checker/fixtures" && rojo serve
```
3. In the Rojo plugin, connect to `localhost:34880`, then press Play. Output should end with `UICHECK SELFTEST PASS`.
4. First run 2026-10-04: PASS. It confirmed the default Frame grey (163,162,165), `TextFits` on cloned UI and the TextScaled estimate (no false flag on a capped label).
5. Rojo gotchas: connect in **Edit** mode (in Play, the plugin errors "Http requests can only be executed by game server"); the host box is `localhost` and the port box is `34880` ("InvalidUrl" otherwise).

## How it maps to the video's checker
| Video (13:18–13:46) | This skill |
|---|---|
| 4 real screen sizes, small phone → full HD | `UICheck.ScreenSizes` virtual sizes + live run |
| Thumb-sized buttons | `touch-size` (44 px, Apple HIG; Roblox has no official minimum) |
| Nothing touches | `overlap` + `offscreen` |
| Centred to 1.5 px | `centre`: FAIL when tagged `UICheckCentre`, WARN on near-misses |
| No tiny text, no random boxes | `text-size`, `text-clipped`, `default-box`, `wrap-box` |
| (Depth stack: same outline thickness everywhere) | `outline-mix` WARN (added with Holden's approval) |

## Pitfalls
- Virtual sizes **delete scripts in the copy**, so code-driven phone layouts aren't re-run. Also run live under Studio's device emulator.
- Closed panels are skipped. Open them and press Shift+U.
- The heuristics (near-centre, wrap-box) can be wrong. Screenshot anything doubtful before reporting it as a bug.
- The runner is temporary in a game repo: delete it and confirm `git status` is clean afterwards.

## Related
- [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[AI-Assisted-Workflow]] · [[UI-Layout-And-Device-Scaling]] · [[Roblox Mobile UI Layout]]
- [[UI-Polish-And-Juice]] · [[Studio Only Dev Test Scripts]] · [[Roblox Studio MCP Quirks]] · [[Paper Plane Toss]]

## Sources
- SyphoDev video, 12:03–14:40: https://www.youtube.com/watch?v=afuKhenJldY
- Thresholds: see `references/thresholds.md` in the skill and [[UI-Layout-And-Device-Scaling]] (touch-target and text-size guidance).
