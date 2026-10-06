---
tags: [prompting/agents, meta/ai-workflow, systems/tooling]
status: reviewed
updated: 2026-10-05
confidence: medium
---
# Subagents for Roblox Development

How Claude subagents work, which Roblox jobs they suit and which they don't, the hazards specific to one Studio and one Rojo sync, Roblox's own Studio MCP subagents, and how community "agent studios" are set up.
**Setting them up** (step by step, tested 2026-10-06), ready-to-copy agent files and delegation prompts are in [[Roblox-Subagent-Definitions-And-Prompts]].
Already covered elsewhere (not repeated here): the fresh-context reviewer and blind critic ([[Prompting-Principles]] rules 10–11, [[Gauntlet-Loop]]), the code-review subagent prompt ([[Prompting-Debugging-And-Testing]]), and the per-area verifier prompt ([[One-Shot-Spec-Prompts]]).

## TL;DR
- **A subagent is a separate Claude worker with its own context window, tools and model.** It gets a written brief and returns **only a summary**. It never sees the main conversation, unless it's a *fork*. Use it to keep logs, searches and file dumps out of the main session, to restrict tools, or to run cheap work on a cheaper model. *(Official docs, 2026-10-05.)*
- **Multi-agent is expensive and suits breadth, not most coding.** Anthropic measured multi-agent research at **+90.2%** over one agent but about **15× the tokens of a chat**, and calls it a poor fit for "most coding tasks" and work with shared context or many dependencies. For Roblox: fan out for **research, audits, mapping and test runs**; keep **building a system** in one session.
- **One Studio is a shared, single-threaded resource.** Since 2026-08-19 every Studio MCP call carries a `studio_id`, but a playtest takes over the whole Studio and Edit-mode tools fail while it runs. Rule: **at most one agent drives a given Studio at a time.** Parallel builders work in **separate git worktrees, Rojo ports and throwaway places**, never the live game.
- **Background subagents can't ask you anything.** No questions and no plan mode. So anything that needs Holden's approval (his plan-first rule) stays in the main conversation, and subagents only research, check or execute pre-approved steps.
- **Roblox has its own subagents** inside the Studio MCP (`explore`; a `playtest` agent in Studio beta that runs on Roblox's servers, not your tokens). They can't nest and can give **false passes**, so their PASS is a hint, never gate evidence on its own.

## 1. How Claude Code subagents work (verified against the official docs, 2026-10-05)
| Topic | Fact |
|---|---|
| Built-in types | **Explore** (read-only search, skips CLAUDE.md and git status), **Plan** (read-only research for plan mode), **general-purpose** (all tools, can edit) |
| Custom agents | Markdown file with YAML frontmatter, in `.claude/agents/` (project, commit it with the game) or `~/.claude/agents/` (all projects). Plugins ship them too (the roblox-dev plugin's `roblox-reviewer`) |
| Key frontmatter | `name`, `description` (how Claude decides to delegate), `tools` / `disallowedTools`, `model` (`haiku`, `sonnet`, `opus`, `inherit`…), `permissionMode`, `maxTurns`, `skills` (preloaded in full), `mcpServers`, `hooks`, `memory` (`user` / `project` / `local`), `isolation: worktree`, `background`, `effort`, `omitClaudeMd`, `color` |
| MCP tool patterns | `mcp__Roblox_Studio__*` grants (or, in `disallowedTools`, removes) every Studio MCP tool. `mcp__*` covers all MCP servers |
| Delegation | Automatic (Claude matches the task to `description`), by name in your prompt, guaranteed with `@"name (agent)"`, or the whole session as one agent with `claude --agent name` |
| What it sees | Its own system prompt + the task brief + the CLAUDE.md hierarchy + a git status snapshot + preloaded skills. **Not** the conversation, auto memory or output style. A **fork** (`/subtask`) inherits the full conversation instead |
| What comes back | One final summary. Built-in Explore and Plan are one-shot; custom subagents can be **resumed** with `SendMessage` and keep their history |
| Limits | Up to **20** running at once (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), nesting **3** levels deep (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), and a startup warning if all agent descriptions together exceed about 15,000 tokens |
| Background | Default in interactive mode; runs while you keep working. **Loses** `AskUserQuestion`, plan mode, `Agent` (no further nesting) and scheduling. Permission grants it receives **apply to the whole session** |
| Model choice | Per-call `model` → agent `model` → `CLAUDE_CODE_SUBAGENT_MODEL` → main model. Route read-only and log-reading agents to cheaper models |

**Other ways to run work in parallel** (official "Run agents in parallel" page): **agent view** (`claude agents`, dispatch background sessions, research preview), **agent teams** (a lead plus teammates with a shared task list and messaging; **experimental, off by default**, and teammates are *not* worktree-isolated), **dynamic workflows** (a script runs many subagents and cross-checks results, e.g. a codebase-wide audit), **projects** (cloud threads, public beta), and **`/batch`** (splits one big change into 5–30 worktree-isolated subagents). Every one multiplies token use.

## 2. When to use subagents in Roblox work
| Job | Fit | Why |
|---|---|---|
| Map an unfamiliar repo or a big place tree (services, remotes, DataStore keys, Config) | **Good** | Lots of reading, small summary. Built-in Explore, or the Studio MCP `explore` subagent for the live DataModel |
| Research several independent questions (API behaviour, competitor games, platform rules) | **Good** | Breadth-first, independent. Anthropic's scale rule: 1 agent for a fact, 2–4 for a comparison, 10+ only for big research |
| Read-only audits (remotes security, DataStore safety, performance) | **Good** | `roblox-dev:roblox-reviewer` exists for this; run several audits in parallel on different folders |
| Run the code gate, a self-test or long logs | **Good** | Verbose output stays out of the main context; only failures come back |
| Batch asset or sound checks (preflight, soundcheck on many files) | **Good** | Independent files, mechanical |
| Build one gameplay system | **Poor** | Shared context and dependencies: the "most coding tasks" case. One session, plan → build → gate |
| Two systems built at the same time | **Only with isolation** | Separate worktrees, Rojo ports and test places; merge, gate, then test in Studio one at a time |
| Live Studio editing or playtesting by several agents | **Avoid** | One Studio is effectively single-threaded (playtest takes over; Edit tools fail meanwhile) |
| Game feel, art or UI tuning with Holden | **Poor** | Iterative back-and-forth. Official guidance: keep frequent back-and-forth in the main conversation |
| Anything that needs Holden's decision mid-way | **Main session only** | Background subagents can't ask questions or enter plan mode |

**Rule of thumb:** delegate when the work is **wide, read-heavy or noisy, and independent**. Keep it in the main session when it's **deep, shared or conversational**.

## 3. Roblox-specific hazards (and the fix)
| Hazard | Evidence | Fix |
|---|---|---|
| Calls land in the wrong Studio when two are open | rbx-mcp-hub was built for this (DevForum, 2026-04-17). Roblox made `studio_id` mandatory on every call (2026-08-19) | Agents call `list_roblox_studios` first and pick by **place id/name**. State the target Studio in the brief. With two Studios open, have the agent confirm before editing |
| A playtest blocks every other agent on that Studio | Developer report on the 2026-08-19 announcement: Play mode takes over Studio; Edit-datamodel tools fail during it | One "studio tester" agent per Studio, run serially. Other agents never touch Studio |
| Parallel builders overwrite each other or one Rojo sync | Rojo serves one project per port into one place; agent teams aren't worktree-isolated (official) | `isolation: worktree` per builder, a unique Rojo port each, a throwaway Baseplate each (Rojo renames the place, see [[Roblox Studio MCP Quirks]]). Never `rojo serve` into the live game |
| Studio MCP search caps results | Developer report: about 25–50 items per search call | Explore agents page through results and summarise per folder |
| A Claude subagent calling the Studio MCP's own subagent times out | Reported for Codex subagents (DevForum) | ⚠️ verify for Claude. Prefer calling the Studio `explore` subagent from the **main** session, or give the Claude subagent the plain MCP tools instead |
| Playtest agent says PASS when it's broken | Roblox lists "false passes" as a known limitation (beta, 2026-04-09) | Treat PASS as a lead. Gate evidence needs your own check (logs, the map audit, the UI checker, a screenshot) |
| Background permission grants spread to the whole session | Official docs | Give agents the **narrowest** `tools` list; read-only agents get `Read, Grep, Glob` only |
| Costs climb fast | Official docs note on cost; Anthropic's 15× figure | Cheap model for read-only work, `maxTurns` caps, and no fan-out for single facts |
| Released game (Paper Plane Toss) | Holden's freeze rule ([[Studio Only Dev Test Scripts]], memory) | No agent touches a live game's repo, place or Studio without Holden asking in chat |

## 4. Roblox's own Studio MCP subagents
| Type | What it does | Status / caveats |
|---|---|---|
| `explore` | Searches scripts and the DataModel and can query game state via Luau, then returns a summary | In the docs and in the tool installed on Holden's PC |
| `playtest` | Spawns a test character, runs a scenario ("players can buy the apple from the shop"), returns Pass / Fail / Inconclusive / Error with a report. **Runs on Roblox infrastructure, not your tokens** | Studio **beta**: File > Beta Features > Playtest Agent. Daily usage cap, 50-turn limit, false passes, no fast-reaction tests (combat, steering), loop detection can stop it early (announcement, 2026-04-09) |
| `screen_capture`, `unit_test` | Listed as subagent types by the tool installed on Holden's PC on 2026-10-05 | ⚠️ verify: not in the public docs; behaviour not tested here |

All of them: one final summary, no back-and-forth, **no nesting** (tool description).
This closes part of the old Gap-Tracker question about whether the Studio subagents change the DevTest method: use the playtest agent for **quick scenario smoke tests**, but keep [[Studio Only Dev Test Scripts]] for anything that must be proven, because of the false passes.

## 5. Community agent studios (examples, not recommendations)
| Project | Shape | Notes |
|---|---|---|
| **claude-roblox-game-studio** ("FoG Roblox Studio", MIT, 2026) | 36 agents in 3 tiers: Opus **directors** (creative, technical, producer) → Sonnet **leads** (design, programming, art, audio, QA, release, monetisation) → Sonnet/Haiku **specialists** (gameplay programmer, DataStore architect, remotes/networking, UI, exploit security, analytics…). Slash commands such as `/remotes-audit`, `/datastore-review`, `/exploit-check`, `/team-ui` | Good idea worth copying: a **"Question → Options → Decision → Draft → Approval"** protocol so the human makes every binding decision, and escalation instead of specialists deciding across domains. ⚠️ Ships hooks that run automatically on tool use; read them before cloning |
| **ClaudeBlox** (MIT, about 17 stars) | 21 agents in a **pipeline**: architect → scripter/world builders → parallel room agents → lighting/sound/VFX → art-director review → MCP playtester and "computer player" → publisher | Claims fully autonomous games from a prompt (unverified). Builds with parts via the Studio MCP, which Holden's art rules reject for final props |
| **roblox-dev plugin** (installed) | One read-only `roblox-reviewer` agent (Read, Grep, Glob) used after systems change | The model for a safe Roblox agent: narrow tools, one job, findings only |

Lesson from both studios: **the value is in the narrow roles and approval gates, not the agent count.** Holden's [[Roblox Game Manager Skill]] already keeps the approval gates. Add agents only where a phase has wide, independent work.

## Checklist
- [ ] Is the work wide/read-heavy/noisy **and** independent? If not, stay in the main session.
- [ ] Does it need Holden's decision? Keep it in the main session (background agents can't ask).
- [ ] Narrowest tools, a cheap model for read-only work, and a `maxTurns` cap.
- [ ] Any Studio use: one agent per Studio, target picked by place via `list_roblox_studios`, never a live game.
- [ ] Parallel builders: worktree + own Rojo port + throwaway place each, then merge → code gate → serial Studio test.
- [ ] Every brief has objective, the context it lacks, tools/sources, boundaries, an output format and a stop condition ([[Roblox-Subagent-Definitions-And-Prompts]]).
- [ ] Verify what comes back before acting: subagent summaries and playtest PASSes are claims, not proof.

## Pitfalls
- Fanning out for a one-line fact wastes tokens and time (Anthropic's 1-agent rule for simple lookups).
- A subagent can't see what you discussed. A brief that says "fix the bug we talked about" fails; spell it out.
- Many overlapping agent descriptions confuse automatic delegation. Keep descriptions short and distinct, and @-mention when it matters.
- The numbers in community studios (agent counts, "fully autonomous") aren't evidence of quality.

## Related
- [[Roblox-Subagent-Definitions-And-Prompts]] · [[Prompting-Principles]] · [[Gauntlet-Loop]] · [[Prompting-Debugging-And-Testing]] · [[One-Shot-Spec-Prompts]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]] · [[Roblox Studio MCP Quirks]] · [[Studio Only Dev Test Scripts]] · [[Roblox Game Manager Skill]] · [[AI-Assisted-Workflow]]

## Sources
- Claude Code docs, "Create custom subagents": https://code.claude.com/docs/en/sub-agents (read 2026-10-05)
- Claude Code docs, "Run agents in parallel": https://code.claude.com/docs/en/agents (read 2026-10-05)
- Anthropic Engineering, "How we built our multi-agent research system": https://www.anthropic.com/engineering/multi-agent-research-system (+90.2%, ~4× / ~15× tokens, scale rules, poor fit for most coding)
- Roblox docs, Studio MCP server: https://create.roblox.com/docs/studio/mcp (subagent types `explore`, `playtest`; no date shown)
- Roblox DevForum, "[Studio Beta] Studio Assistant & MCP Playtest Agent" (2026-04-09): https://devforum.roblox.com/t/studio-beta-studio-assistant-mcp-playtest-agent/4566767
- Roblox DevForum, "Studio MCP: Multi-Agent Improvements and Connected AI Clients" (2026-08-19) and replies: https://devforum.roblox.com/t/studio-mcp-multi-agent-improvements-and-connected-ai-clients/4820583
- Roblox DevForum, rbx-mcp-hub (2026-04-17): https://devforum.roblox.com/t/tool-rbx-mcp-hub-%E2%80%94-work-on-multiple-roblox-games-at-once-with-claude-code-cursor-codex-and-other-ai-agents/4582579
- GitHub: https://github.com/CodePhobiia/claude-roblox-game-studio · https://github.com/Claudeblox · roblox-dev plugin agent file `agents/roblox-reviewer.md` (local)
- The Studio MCP `subagent` tool description on Holden's PC (2026-10-05): types `explore`, `screen_capture`, `unit_test`; no nesting
