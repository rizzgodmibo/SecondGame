---
title: Keeping API Keys Out of Git
date: 2026-10-02
tags: [security, secrets, roblox]
---
# Keeping API Keys Out of Git

Two near-misses during [[Fish a Monster]]:

1. **A Roblox Open Cloud key was pasted into `.claude/settings.json` as `ANTHROPIC_API_KEY`.** That's the wrong service (Anthropic keys start with `sk-ant-`), and settings.json is usually committed. Claude refused to write it. Because the key had been pasted into chat, **treat it as exposed and regenerate it.**
2. **A key was pasted onto the end of the `.secrets/` line in `.gitignore`.** That un-ignored the folder and put the key in a tracked file. It was fixed before any commit, and the git history was checked clean.

## The setup that works
- The key goes in a gitignored `.secrets/roblox_open_cloud_key.txt`, containing the key only. Watch for Windows saving it as `.txt.txt`.
- Never paste keys into chat. Claude reads the file and never prints it.
- Personal env settings go in `.claude/settings.local.json` (gitignored) or a Windows user environment variable, not `settings.json`.
- Open Cloud key permissions: Assets read and write, restricted by IP.

Related: [[Blender to Roblox Asset Pipeline]]
