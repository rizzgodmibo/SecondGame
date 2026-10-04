---
title: Stray Claude Sessions in System32
date: 2026-10-02
tags: [claude-code, inbox, setup]
---
# Stray Claude Sessions in System32

Two Claude Code sessions on 2026-10-02 started in `C:\Windows\System32` instead of a project folder. They aren't a project, so they're filed here for sorting.

1. **Shell commands typed into Claude.** `cd /Fish A Monster` and `claude` were typed inside a running session, so they didn't run. Project skills (like `fish-map-builder`) only load when Claude starts in the project folder:
   ```powershell
   cd "C:\Users\holde\Downloads\Fish A Monster"
   claude --continue
   ```
2. **claude-obsidian setup.** README setup lines with a placeholder `--plugin-dir /absolute/path/to/claude-obsidian` were pasted in. Neither the plugin nor `Documents\MyKnowledgeVault` existed. The plugin has to be cloned first and `claude --plugin-dir` run from your own terminal. This vault (`C:\Vault`) appears to be what came of that.

Related: [[Rojo Workflow Gotchas]], [[Fish a Monster]]
