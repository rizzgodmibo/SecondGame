---
tags: [prompting/setup, systems/tooling]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Project Setup, Kickoff and Claude Code Configuration

Starting a new Roblox game with Claude Code: the kickoff prompt, the repo's `CLAUDE.md`, the scaffold and the tools. General rules: [[Prompting-Principles]].

## TL;DR
- **The first prompt reads, restates and stops.** Read the vault notes → summarise approved / draft / undecided → list conflicts → plan + file list for phases 0–1 → wait. [[Rubber-Tower-Claude-Code-Prompt]] is the working template.
- **The empty scaffold must pass the code gate before any game code** (`gate.sh --scaffold`). Otherwise real mistakes can't be told apart from setup noise ([[Roblox Code Gate Skill]], from the SyphoDev video).
- **A short repo `CLAUDE.md`** holds commands, traps and conventions; long knowledge stays in vault notes and skills (Anthropic: "would removing this line cause a mistake?").
- **Code lives in git, the world lives in the place file.** Tell Claude this every project; save the place (Paper Plane Toss lost its first session's map to an unsaved "Place1").
- **Secrets never go in chat.** Ask Claude how to store a key as a local secret file instead ([[Keeping API Keys Out of Git]]).

## What Claude needs from you
- Project folder location (or "make a new one"), game name, and where the vault hub lives.
- Which phases are approved, and the gate each must pass.
- Which Studio place to use (Claude must call `list_roblox_studios`, since IDs change every launch) and whether Holden is currently testing in it.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Project-Bootstrap-Checklist]] | Day-one foundations in order, with "done when" tests |
| [[Module-Architecture]] · [[Luau-Strict-Typing]] · [[Common-Libraries]] | Init/Start services + controllers, `--!strict`, the default library stack (ProfileStore, Trove, Signal…) |
| [[Tooling-Rojo-Wally-And-Studio-MCP]] · [[Rojo Workflow Gotchas]] · [[Roblox Studio MCP Quirks]] | Rojo/Wally/Rokit, the MCP loop, and every trap hit so far |
| [[Roblox Code Gate Skill]] · [[Studio Only Dev Test Scripts]] | The 4-step gate and the temporary `Dev*.luau` testing method |
| [[Keeping API Keys Out of Git]] | The secret-file setup that works |

## Prompts

### 1. Kickoff for a new game (paste into a fresh Claude Code session with the vault connected)
Use [[Rubber-Tower-Claude-Code-Prompt]] as the full example. The short form:
```text
You're helping me (Holden) build my Roblox game "[NAME]" in Claude Code. My vault (C:\Vault) is the source of truth.

STEP 1, READ (in order, before replying): C:\Vault\CLAUDE.md; Projects/[Game]/[Game].md (hub: my decisions and open questions); the GDD and build plan; then the vault notes each phase needs, found via Home.md. Search the vault before assuming anything.

SOURCE-OF-TRUTH RULES: only "Decisions from Holden" and (USER) lines are approved. Never turn a suggestion into an approval or invent mechanics or lore. Flag disagreements between the hub, GDD, plan and code. Mark anything unverified with "⚠️ verify:". This prompt doesn't authorise publishing, purchases, uploads, commits or messages to anyone.

STEP 2, REPLY WITH (no code yet): (a) what you understood, split into approved / draft / undecided; (b) conflicts or unclear points; (c) ask where to create the project; (d) the plan and file list for phases 0 and 1 only, with the gate each must pass. Then stop and wait for my approval.

END EVERY REPLY by updating the matching vault notes and the line "Vault: created/updated <path>" or "Vault: nothing to save".
```
Why: Claude Code doesn't see the planning chat, so everything that matters is in the vault; linking notes keeps the prompt short and current. The stop after step 2 is Holden's plan-first rule.

### 2. Scaffold (after approval)
```text
Build phase 0 only: the Rojo scaffold.
- Use the roblox-dev setup skill and the layout in Systems/Module-Architecture.md: one server and one client bootstrap, Services and Controllers with Init/Start, Shared with Config, Types and a remotes registry. --!strict on every file.
- rokit.toml (rojo, wally, selene, stylua, lune), stylua.toml, selene.toml, .gitattributes with "* text=auto eol=lf", .gitignore.
- default.project.json with globIgnorePaths ["**/Dev*.luau"] so dev scripts can never publish, plus dev.project.json without that ignore for testing (Resources/Rojo Workflow Gotchas.md).
- tests/ with one trivial Lune spec.
- A short CLAUDE.md for the repo (see below).
DONE WHEN: bash ~/.claude/skills/roblox-code-gate/scripts/gate.sh --scaffold <project> prints GATE PASS, and after rojo serve + Play, Output shows the boot lines with no errors. Quote both. Then stop for my review; I make the commits.
```

### 3. The repo's CLAUDE.md (ask Claude to write it from this outline)
```text
Write a CLAUDE.md for this repo, under 60 lines. Include only what you'd get wrong without it:
- Vault hub path and "read Build-Status first each session".
- Commands: rojo serve (dev.project.json), the code gate command, how to run one spec.
- Conventions: --!strict, Init/Start, every tunable number in Config, all remotes in the registry, client sends intent only.
- Traps: Dev*.luau scripts are Studio-only and never committed; MCP execute_luau caches required modules (require a clone); Studio deletions are listed for Holden; save the place file; Rojo-synced changes need a play restart.
- Holden's rules: plan + file list before code, no commits unless asked, end replies with the Vault line.
Leave out anything Claude can read from the code.
```
Why: Anthropic warns that long CLAUDE.md files get half-ignored. Holden's global and vault CLAUDE.md files already carry the general rules.

### 4. Connect Studio and store a secret
```text
Roblox Studio's MCP server is enabled (Assistant → … → Manage MCP Servers). Call list_roblox_studios and tell me which place you'll use. Don't stop or start a playtest without asking, because I may be testing.
I also have a Roblox Open Cloud key. Don't ask me to paste it. Tell me how to store it in a gitignored .secrets/ file that your scripts read, and check .gitignore really ignores it.
```
Why: the SyphoDev video and Holden's own near-misses both say never to paste keys into chat ([[Keeping API Keys Out of Git]]).

### 5. Turn a repeated correction into a skill or hook
```text
I've corrected you about [X] more than once. Write it down so it doesn't happen again:
- If it's a fact every session needs, add one line to the repo CLAUDE.md.
- If it's a procedure with steps or a script, add it to the [skill name] skill's traps list (or draft a new skill: description says what it does and when to use it, SKILL.md under 500 lines, tested script in scripts/).
- If it must happen every time with no exceptions (like running the gate before finishing), propose a hook and show me the config before adding it.
Tell me which you chose and why.
```
Why: the SyphoDev rule "every breakage becomes a rule with the reason", plus Anthropic's split between CLAUDE.md (advisory), skills (on demand) and hooks (guaranteed).

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### End-of-session handoff
```text
We're stopping for now. Update Projects/[Game]/Build-Status.md with: what was done this session (with evidence), what's half-done and its exact state, open decisions for me, the next proposed step, and any trap we hit (also add it to the repo CLAUDE.md or the skill's traps list). Keep it short enough to read in a minute.
```
Borrowed from the `handoff` skill idea in AshExplained/roblox-skills ([[Community-Prompt-Examples]]); the vault already keeps state in Build-Status.

### Resume in a fresh session
```text
Resume work on [Game]. Read C:\Vault\CLAUDE.md, the project hub, Build-Status.md and the repo CLAUDE.md, then `git log -10` and `git status`. Tell me in 5 lines where we are, what's uncommitted, and the next step you propose. Don't change anything yet.
```

### Map an unfamiliar codebase
```text
Before we change anything in [repo], map it: the boot flow, every Service and Controller with one line each, the remotes registry, where data is saved, and where Config lives. Use a subagent if it means reading many files. Write it as a short section in the repo CLAUDE.md only if it saves future sessions from re-reading; otherwise just tell me.
```

### Add a library (with approval)
```text
I want to use [ProfileStore / Trove / Signal] in [Game]. Check Systems/Common-Libraries.md, then tell me the Wally package and version to pin, where it goes (server-only packages vs shared), and what it replaces in our code. Wait for my OK before editing wally.toml. After installing, run the code gate.
```

### Separate test place
```text
Set up [Game] so tests can't touch live data: a Studio-only DataStore name (as in Config), dev.project.json for testing, and a note in the repo CLAUDE.md about which place is the test place. List anything that can still reach production (Studio API access, Open Cloud keys) and how we keep it safe.
```

## How to check the result
- `gate.sh --scaffold`: `GATE build PASS`, `tests PASS`, `lint PASS`, `format PASS`, `GATE PASS` (Rubber Tower's phase 0 evidence format, [[Rubber-Tower-Build-Status]]).
- Studio Output after Play: `[Boot] server ready`, `[Boot] client ready`, no errors.
- `git status` clean except intended files; no `Dev*.luau` tracked.

## Pitfalls
- **Wrong project syncing.** An old `rojo serve` from another game offers to sync into Studio: dismiss it ([[Paper Plane Toss]] lessons).
- **Background `rojo serve` dies** at the background-task limit or when the session ends; tell Claude to say so rather than pretend it's still running ([[Rojo Workflow Gotchas]]).
- **Gitignored ≠ not synced.** Rojo syncs every file in a mapped folder; only `globIgnorePaths` keeps dev scripts out of a publish.
- **Line endings** break `stylua --check` without the `.gitattributes` rule.
- **Studio access to API services** must be on for ProfileStore saving in Studio ([[Fish a Monster Saving and Offline Income]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Gameplay-Systems]] · [[Prompting-Debugging-And-Testing]] · [[Rubber-Tower-Claude-Code-Prompt]] · [[Project-Bootstrap-Checklist]]

## Sources
- Anthropic, Claude Code best practices (CLAUDE.md, skills, hooks, permissions): <https://code.claude.com/docs/en/best-practices>
- Anthropic, Skill authoring best practices: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Roblox, Studio MCP server doc: <https://github.com/Roblox/creator-docs/blob/main/content/en-us/studio/mcp.md>
- SyphoDev video (setup and secrets, 08:18–10:05): <https://www.youtube.com/watch?v=afuKhenJldY>
- Local: [[Rubber-Tower-Build-Status]], [[Fish a Monster Build Steps]], [[Rojo Workflow Gotchas]].
