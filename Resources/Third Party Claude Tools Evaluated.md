---
title: Third Party Claude Tools Evaluated
date: 2026-10-02
tags: [tooling, claude-code, mcp, decisions]
---
# Third Party Claude Tools Evaluated

Reviewed from Holden's "CLAUDE ROBLOX SETUP.txt" list on 2026-10-02, and again at the start of [[Paper Plane Toss]]. **None were installed.**

| Tool | Verdict |
|---|---|
| `robloxstudio-mcp` (community) | Would be a second Studio bridge next to the official one. Unpinned `@latest` npm package. |
| ShiroKSH roblox-studio skill | Well built, but brings its own MCP, its own Studio plugin and an unpinned `npx github:` install. 1 star. |
| benhelland roblox-claude-skills | Harmless markdown, but written for tool names we don't have. Generic advice, no licence. |
| `uvx blender-mcp` | Older package name; uses the uv Python that's broken on this PC. See [[Blender MCP Setup]]. |
| Graphify, Superpowers, Ponytail | Not needed: the codebase is small, and CLAUDE.md already enforces plan-first. |

**Preferred instead:** a project-specific skill made with skill-creator (for example `fish-map-builder`), which uses only the tools we actually have.

Already in place: the roblox-dev plugin, the official Studio MCP, Blender MCP, skill-creator, and Figma and Claude Design for UI.

Related: [[Roblox Studio MCP Quirks]]
