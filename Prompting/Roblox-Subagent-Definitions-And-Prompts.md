---
tags: [prompting/agents, prompting/examples, meta/ai-workflow]
status: draft
updated: 2026-10-06
confidence: medium
---
# Roblox Subagent Definitions and Delegation Prompts

How to **set up** subagents for Roblox Studio development (step by step, tested), copy-paste agent files for a Roblox game repo, and prompts for handing work to subagents. The why and when is in [[Subagents-For-Roblox-Development]].
**Status:** field names follow the official subagent docs (2026-10-05). **`roblox-explorer` was tested on 2026-10-06** (setup section below). The other three agent files haven't been run yet; test each once and note the result here.
Not repeated here: the code-review prompt ([[Prompting-Debugging-And-Testing]] §4), the blind critic ([[Gauntlet-Loop]], [[Prompting-UI]]) and the per-area verifier ([[One-Shot-Spec-Prompts]]). For read-only code audits use the installed `roblox-dev:roblox-reviewer` agent rather than writing a new one.

## TL;DR
- Put agent files in the game repo's `.claude/agents/` (committed with the game) or `~/.claude/agents/` (every project). Restart the session or ask Claude to load them.
- Four roles cover the good-fit jobs: **explorer** (read-only map), **docs researcher** (web, with sources and dates), **gate runner** (runs checks, returns only failures), **studio tester** (the only agent allowed to touch Studio, one at a time).
- Every brief to a subagent needs: **objective, the context it lacks, tools/sources, boundaries, output format, stop condition.** Subagents never see the conversation.
- Builders stay in the main session. Approvals stay in the main session. Background agents can't ask Holden anything.

## Setup: step by step (tested 2026-10-06 with Claude Code 2.1.289)
1. **Choose where the agent lives.**
   - **Game-specific** (explorer, studio tester): `<game repo>/.claude/agents/`. It's committed with the game, so every session in that repo gets it.
   - **Every project** (docs researcher, gate runner): `C:\Users\holde\.claude\agents\`. On 2026-10-06 that folder didn't exist yet, so create it.
2. **Create one `.md` file per agent**, named after the agent (e.g. `.claude/agents/roblox-explorer.md`), and paste the agent block from below.
   The file must start with `---` on line 1, and `name` and `description` are required. Copy the block as is, including the closing `---`.
3. **Give Studio access only to agents that need it.** Subagents can use the MCP servers registered for that repo. Holden's game repos register `Roblox_Studio` (and Blender) in a gitignored `.mcp.json`.
   Grant it per agent in `tools:` with `mcp__Roblox_Studio__*` (as `roblox-studio-tester` does). Read-only agents get `Read, Grep, Glob` only. ⚠️ Not tested yet with a live Studio.
4. **Start a new Claude Code session in the repo** (Code tab or terminal). In the test, a fresh session picked up the agent file. ⚠️ Whether an already-running session sees a new file without restarting is unverified, so restart to be safe.
5. **Call it.**
   - `@"roblox-explorer (agent)" map this repo` guarantees the agent runs.
   - Naming the agent in a prompt lets Claude decide, and a good `description` lets Claude delegate on its own.
   - `/agents` points to the agent folders.
6. **Test once with a known answer** before trusting it. Put a deliberate flaw in a scratch repo and check the agent reports it with file:line (see the test result below).
7. **Optional, scripted (headless) runs:**
   ```bash
   claude -p '@"roblox-explorer (agent)" map this repo using your standard report' --allowedTools "Agent,Read,Grep,Glob" --max-turns 12 < /dev/null
   ```
8. **Commit `.claude/agents/` with the game** (Holden commits). Keep `.mcp.json` out of git.

**Test result (2026-10-06):**
- **Setup:** a throwaway Rojo repo with one server Service containing a planted flaw: a RemoteEvent that adds whatever amount the client sends. The `roblox-explorer` file was copied exactly from this note into `.claude/agents/`.
- **Run:** a headless `claude -p` run with the @-mention.
- **Result:** the agent was used (the run confirmed it by name) and followed the report format. It found the flaw at `CoinService.luau:10`, plus the missing rate limit and an unused Config value, and edited nothing.
- **Lessons:**
  - Headless runs print a stdin warning unless you add `< /dev/null`.
  - Headless runs still load `~/.claude/CLAUDE.md`, so Holden's global rules (such as the "Vault:" closing line) apply to scripted runs too.

**Troubleshooting**
| Symptom | Check |
|---|---|
| Claude doesn't use the agent | Use the `@"name (agent)"` form. Make the `description` say *when* to use it. Remove overlapping agents with similar descriptions |
| Agent missing from the session | File in the right folder? Frontmatter on line 1, with `name` and `description`? Restart the session |
| Agent can't touch Studio | Is `Roblox_Studio` in the repo's `.mcp.json`? Does `tools:` include `mcp__Roblox_Studio__*`? Is Studio open, with the agent picking it via `list_roblox_studios`? |
| Agent edits things it shouldn't | Narrow `tools:`. Read-only agents get `Read, Grep, Glob` only |
| Costs climb | Set `model: haiku` for read-only and log-reading agents. Add `maxTurns` |

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
