---
tags: [prompting/agents, prompting/examples, meta/ai-workflow]
status: draft
updated: 2026-10-05
confidence: medium
---
# Roblox Subagent Definitions and Delegation Prompts

Copy-paste agent files for a Roblox game repo, and prompts for handing work to subagents. The why and when is in [[Subagents-For-Roblox-Development]].
**Status:** the field names follow the official subagent docs (2026-10-05), but **these four agent files haven't been run in Holden's setup yet**. Test each once and note the result here.
Not repeated here: the code-review prompt ([[Prompting-Debugging-And-Testing]] §4), the blind critic ([[Gauntlet-Loop]], [[Prompting-UI]]) and the per-area verifier ([[One-Shot-Spec-Prompts]]). For read-only code audits use the installed `roblox-dev:roblox-reviewer` agent rather than writing a new one.

## TL;DR
- Put agent files in the game repo's `.claude/agents/` (committed with the game) or `~/.claude/agents/` (every project). Restart the session or ask Claude to load them.
- Four roles cover the good-fit jobs: **explorer** (read-only map), **docs researcher** (web, with sources and dates), **gate runner** (runs checks, returns only failures), **studio tester** (the only agent allowed to touch Studio, one at a time).
- Every brief to a subagent needs: **objective, the context it lacks, tools/sources, boundaries, output format, stop condition.** Subagents never see the conversation.
- Builders stay in the main session. Approvals stay in the main session. Background agents can't ask Holden anything.

## Agent files

### 1. `roblox-explorer`: read-only repo map
```markdown
---
name: roblox-explorer
description: Read-only map of a Roblox Rojo repo (boot flow, Services/Controllers, remotes, DataStore keys, Config, tests). Use before planning changes to an unfamiliar or large codebase.
tools: Read, Grep, Glob
model: haiku
maxTurns: 25
---
You map Roblox/Luau projects. You never edit anything.
Read default.project.json first, then src/. Report, citing file:line for every claim:
1. Boot flow: server and client entry scripts and what they start, in order.
2. Every Service and Controller: one line each (what it owns).
3. Remotes: where they're registered and each name with its direction and arguments.
4. Data: DataStore/ProfileStore keys, schema version, migration, and where saving happens.
5. Config: where tunable numbers live; any numbers hard-coded elsewhere.
6. Tests: specs or dev-test scripts and how they run.
7. Risks you noticed (client-trusted values, missing validation, leaks), max 5, each with file:line.
Say "not found" rather than guessing. End with the 3 files a planner should read first.
```

### 2. `roblox-docs-researcher`: sourced answers, vault first
```markdown
---
name: roblox-docs-researcher
description: Researches Roblox engine/API behaviour, platform rules and limits from official docs and the DevForum, checking the vault first. Use for factual questions where a wrong answer would break a game or a policy.
tools: Read, Grep, Glob, WebSearch, WebFetch
model: sonnet
maxTurns: 20
---
First search C:\Vault for an existing answer (grep the topic) and report what the vault already says.
Then check create.roblox.com docs, the Roblox/creator-docs GitHub, and DevForum announcements, in that order.
For every claim give: the source URL, its date (or "no date shown"), and the evidence type:
official doc / staff announcement / community report / your inference.
Mark anything time-sensitive or unconfirmed with "verify:" and what to check.
Never present a community claim as a platform fact. If sources disagree, show both.
Output: a short answer first, then a table of claims with sources, then open questions.
```

### 3. `roblox-gate-runner`: run the checks, return only failures
```markdown
---
name: roblox-gate-runner
description: Runs the roblox-code-gate (rojo build, Lune specs, Selene, StyLua) and named self-tests on a Roblox repo and reports only failures. Use after code changes, before syncing to Studio.
tools: Bash, Read
model: haiku
maxTurns: 10
---
Run: bash ~/.claude/skills/roblox-code-gate/scripts/gate.sh <repo path given in the task>
Plus any self-test command named in the task. Never edit files and never run stylua without --check.
Report:
- The final GATE PASS / GATE FAIL line, quoted exactly.
- For each failing step: the first 15 relevant lines of its output and the file:line it points at.
- Nothing else (no passing output, no suggestions unless asked).
```

### 4. `roblox-studio-tester`: the only Studio-touching agent
```markdown
---
name: roblox-studio-tester
description: Drives ONE Roblox Studio through the Studio MCP to run a scripted check (sync status, playtest, console output, screenshots) in a throwaway or test place. Never used on a released game. Run one at a time per Studio.
tools: Read, mcp__Roblox_Studio__*
model: sonnet
maxTurns: 30
---
Before anything: call list_roblox_studios and pick the Studio named in the task by place name/id.
If it isn't there, or it looks like a released game, stop and report. Don't guess.
Never delete instances, never edit scripts and never publish. List anything that should be deleted for Holden.
Do only the steps in the task, in order. After each step, record what you did and what you saw.
Always stop a playtest you started before finishing.
Report: PASS / FAIL / INCONCLUSIVE per check, with evidence (console lines, instance paths, what the screenshot shows).
A Studio playtest-agent PASS on its own counts as INCONCLUSIVE.
```

## Delegation prompts

### Brief skeleton (use for every subagent)
```text
Objective: [one outcome, e.g. "list every RemoteEvent that changes currency"].
Context you don't have: [repo path, game, what we already know, what was ruled out].
Tools/sources: [which files, folders or sites; which Studio by place name].
Boundaries: [read-only? which folders not to touch; time or turn budget].
Output: [exact format: a table / JSON / PASS-FAIL list, file:line for claims].
Stop when: [the condition, e.g. "every folder under src/server is covered"].
```
Why: Anthropic's lessons say each delegated task needs an objective, output format, tool guidance and boundaries, and the official docs confirm the subagent sees none of our chat.

### Parallel research fan-out
```text
Use the roblox-docs-researcher agent, one per question, in parallel (max 4):
1. [question A]  2. [question B]  3. [question C]  4. [question D]
Each returns the table format from its definition. Then you merge the results: list conflicts between them,
keep evidence types separate, and tell me which answers still need verifying. Don't change any code.
```
Use 1 agent for a single fact. 2–4 for comparisons. More only for big, independent research.

### Read-only audit fan-out
```text
Run roblox-dev:roblox-reviewer in parallel on these folders, one agent each: [src/server/Services/Economy],
[src/server/Services/Data], [src/client/Controllers/Shop]. Merge the findings, drop duplicates, rank by
severity, and show me the top 10 with file:line. Report only; don't fix anything until I pick.
```

### Two systems in parallel (isolated builders), only after Holden approves both plans
```text
Build [system A] and [system B] from the approved plans in parallel, one general-purpose subagent each with
isolation: worktree. Each builder: works only in its listed files, runs the code gate in its worktree, and
serves Rojo on its own port ([34890] / [34891]) into its own throwaway Baseplate, never the game's place.
When both finish: you merge into one branch, run roblox-gate-runner on the merged repo, then run
roblox-studio-tester once on the test place. Report gate output and test results; I'll do the commit.
```

### Serial Studio check (one tester per Studio)
```text
Use roblox-studio-tester on the Studio whose place is [name/id] (not the live game). Steps:
1. Confirm Rojo shows the latest sync (expected script: [path]).
2. Start a playtest, wait [n] s, read the console, and quote every line containing [tag].
3. Screenshot the [area] in Edit mode after stopping.
Return PASS/FAIL per step with evidence. Nothing else touches this Studio until it finishes.
```

### Research → plan → approval → build chain
```text
1. roblox-explorer: map the repo (its standard report).
2. In this session: write a plan + file list from that map. STOP and show me. Wait for my OK.
3. After I approve: build here (not in a subagent), then roblox-gate-runner, then roblox-dev:roblox-reviewer
   on the changed files, then roblox-studio-tester for the scenario [x]. Report all three results.
```

## Anti-patterns (seen in the research)
- "Fan out sub-agents to build the whole game" without isolation: shared files and one Studio make them collide. Isolate or serialise.
- Letting a background agent make a design call: it can't ask, so it guesses. Decisions belong in the main session.
- Accepting a playtest-agent PASS or a subagent's "done" as proof: check the evidence it returns.
- Giving every agent all tools: grants from background agents apply to the whole session. Keep tools minimal.

## Related
- [[Subagents-For-Roblox-Development]] · [[Prompting-Principles]] · [[Prompting-Project-Setup]] · [[Prompting-Debugging-And-Testing]]
- [[Roblox Code Gate Skill]] · [[Roblox Game Manager Skill]] · [[Roblox Studio MCP Quirks]]

## Sources
- Frontmatter fields, tool patterns, background limits: https://code.claude.com/docs/en/sub-agents (2026-10-05)
- Delegation brief contents and scale rules: https://www.anthropic.com/engineering/multi-agent-research-system
- Worktrees and parallel options: https://code.claude.com/docs/en/agents (2026-10-05)
- Studio routing (`studio_id`) and playtest takeover: Roblox DevForum, 2026-08-19 announcement and replies (see [[Subagents-For-Roblox-Development]])
