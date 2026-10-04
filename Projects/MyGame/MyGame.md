---
title: MyGame
date: 2026-10-01
tags: [roblox, scaffold, abandoned]
project: MyGame
---
# MyGame

A one-session Rojo scaffold at `E:\MyGame` made on 2026-10-01 with `/roblox-dev:setup`. There is no game design behind it, and no work followed. Holden moved on to [[Fish a Monster]] the same evening.

## What was created
- `default.project.json`, mapping `src/shared`, `src/server` and `src/client`
- `wally.toml` (no packages), `selene.toml`, `stylua.toml`, `rokit.toml`
- A CI workflow
- Starter `--!strict` bootstraps with an `init()` then `start()` two-phase load

## Problems found
- None of the tools (Rokit, Rojo, Selene, StyLua, Wally) were installed yet, so lint and format couldn't run.
- **Git wasn't installed** either at that point, so `git init` failed. Fix: `winget install --id Git.Git -e`. Git 2.55 was present by the Fish a Monster session.
- The instructions file was named `CLAUDE.md.md`, so Claude Code wouldn't load it. It needs to be renamed to `CLAUDE.md`.

The same scaffold pattern was reused for [[Fish a Monster]] and [[Paper Plane Toss]]. See [[Rojo Workflow Gotchas]].
