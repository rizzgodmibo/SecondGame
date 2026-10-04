---
tags: [resources/tooling, systems/tooling, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: high
---
# Roblox Code Gate Skill

A Claude Code skill (`roblox-code-gate`): one read-only command that must pass before Roblox code is synced to Studio or called done.
Built 2026-10-04 as the third skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.1, "4 checks before Studio").

## TL;DR
- **Run:** `bash ~/.claude/skills/roblox-code-gate/scripts/gate.sh <project-dir>`, or add `--scaffold` for a new project, where a missing spec is a FAIL.
- **Steps:** `rojo build` (to a temp file) → **Lune** specs (`tests/**/*.spec.luau`) → **Selene**, where warnings fail too → **StyLua** `--check`. All four always run, so one report shows everything.
- **Read-only:** it never edits a project or syncs a place. Tools come from the project's `rokit.toml`, falling back to the skill's pins (rojo 7.7.0, selene 0.32.0, stylua 2.5.2, **lune 0.10.5**).
- **Status: self-test PASSED 2026-10-04** (8/8 cases: good, one broken fixture per step, no-tests SKIPPED, `--scaffold` FAIL, and tool fallback).
  The first run caught a real gate bug (fallbacks weren't reported), now fixed. **Not yet run on a real game.**
- **Lune** was installed with Holden's approval (2026-10-04), pinned only in the skill's own `rokit.toml`. It isn't in any game's.

## Pure rules modules
Formulas such as costs, rewards, drop rolls, damage and level curves go in `src/shared/Rules/*.luau`, with no `game`/`Instance`/Roblox datatypes.
Specs live in `tests/` (outside `src/`, so they never sync into the game) and run on the PC in about a second. Randomness is passed in as a number, so specs can pin it.
Worked examples, `Economy` and `Drops`, are in the skill's `references/pure-rules.md`. Both were run through the spec runner.

## Video rules mapped to Holden's conventions
| Video rule | Here |
|---|---|
| Code lives in files, never Studio | Rojo (already standard) |
| Every tweakable number in one config | `Config.luau` / `src/shared/Rules/` |
| All messages through one file | One remotes registry per game (see [[Remotes-And-Networking]]) |
| A list of traps that cost days | Per-game traps in `Projects/<game>/` or `Bugs/`, with the reason |
| Empty project passes all four first | `gate.sh --scaffold` before any game code |

## Pitfalls
- New Rokit tools must be trusted first: `rokit trust lune-org/lune`.
- Strict types aren't checked (no luau-lsp on this PC). That's a candidate fifth step.
- `stylua` without `--check` rewrites files. The gate only checks.

## Related
- [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[Roblox UI Checker Skill]] · [[Roblox Map Audit Skill]] · [[Tooling-Rojo-Wally-And-Studio-MCP]]
- [[Rojo Workflow Gotchas]] · [[Studio Only Dev Test Scripts]] · [[Balancing-Methods]]

## Sources
- SyphoDev video, 10:05–11:57: https://www.youtube.com/watch?v=afuKhenJldY
- Lune: https://github.com/lune-org/lune (0.10.5 installed via Rokit)
- Self-test output, 2026-10-04 (`scripts/selftest.sh`).
