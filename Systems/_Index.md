---
tags: [systems/index]
status: draft
updated: 2026-10-04
confidence: high
---
# Systems — Index

Engineering knowledge for building a Roblox game: Luau, architecture, networking, data, security, performance, tooling.

## TL;DR
- New game? Start with [[Project-Bootstrap-Checklist]], then [[Module-Architecture]] and [[Data-Persistence-DataStores-And-ProfileStore]].
- Writing any remote? Read [[Remotes-And-Networking]] and [[Anti-Exploit-And-Server-Authority]] first.
- Something slow? [[Performance-And-Profiling]] → then [[Streaming-And-Instance-Streaming]] / [[Parallel-Luau]] / [[Physics-And-Network-Ownership]].
- Driving Studio from Claude? [[Tooling-Rojo-Wally-And-Studio-MCP]].

## Notes
| Note | One-line summary |
|---|---|
| [[Project-Bootstrap-Checklist]] | Day-one ordered setup: repo/CI, skeleton, data, remotes, analytics, workspace & game settings, quality gates |
| [[Module-Architecture]] | Single-script architecture, services/controllers with Init/Start, folder layout, Rojo project file, avoiding circular requires |
| [[Luau-Strict-Typing]] | `--!strict` everywhere, annotations, generics, exported types, typeof, common errors and fixes, `--!native`/`@native` |
| [[Client-Server-Boundary-And-Replication]] | What replicates, what clients can change, attributes vs values vs remotes, server authority mode |
| [[Remotes-And-Networking]] | RemoteEvent/Function/Unreliable choice, limits (≈500 req/s/client, 1,000-byte unreliable), guards, token-bucket limiter, batching, Blink/Zap/ByteNet |
| [[Data-Persistence-DataStores-And-ProfileStore]] | DataStore budgets & limits, UpdateAsync vs SetAsync, ProfileStore DataService + receipts, migrations, OrderedDataStore, MemoryStore, RTBF |
| [[Anti-Exploit-And-Server-Authority]] | Threat model, server-authoritative rules, movement guard code, hit validation, honeypots, Ban API, Hyperion limits |
| [[Performance-And-Profiling]] | MicroProfiler/Dev Console/Script Profiler workflow, budgets, memory categories, perf killers, object pooling |
| [[Parallel-Luau]] | Actors, desynchronize/synchronize, SharedTable, actor messaging, when it's worth it |
| [[Streaming-And-Instance-Streaming]] | StreamingEnabled settings, ModelStreamingMode, persistent models, client stream-safe patterns, RequestStreamAroundAsync |
| [[Physics-And-Network-Ownership]] | Assemblies, ownership rules, SetNetworkOwner patterns, mover constraints, collision groups (WorldRoot API), exploit risks |
| [[Obby-Special-Platforms]] | Ice (friction 0.01 → 4.6-stud slide, measured), wobble platforms (client copy, corner springs, Humanoids put no weight on floors), bounce pads |
| [[Avatar-Ragdoll]] | Ragdolling the player's own avatar: joint-upgrade rigs (AnimationConstraint + built-in sockets, verified), server decides/client moves, lag-tolerant fall validation, measured PC cost |
| [[Error-Handling-And-Logging]] | pcall/xpcall, retry with backoff, task library, ScriptContext.Error reporter, structured logs, Promise libs |
| [[Tooling-Rojo-Wally-And-Studio-MCP]] | Rojo, Wally, Rokit, Selene, StyLua, luau-lsp, GitHub Actions CI, built-in Roblox Studio MCP server and how Claude drives it |
| [[Roblox Code Gate Skill]] | Claude Code skill: read-only gate (rojo build, Lune specs for pure rules modules, Selene, StyLua) before every sync; scaffold rule |
| [[Deprecated-API-Replacements]] | Old → new API table generated from the official reference (…Async renames, multi-role groups, Plus purchase prompt, legacy movers) — check before writing any code |
| [[Common-Libraries]] | Vetted libraries with status/versions (ProfileStore, Trove, Signal, Promise, Fusion/Vide/React-lua, Knit archived, Blink/Zap/ByteNet, TopbarPlus) |

## Reading order for an agent building a game
1. [[Project-Bootstrap-Checklist]]
2. [[Module-Architecture]] → [[Luau-Strict-Typing]]
3. [[Client-Server-Boundary-And-Replication]] → [[Remotes-And-Networking]] → [[Anti-Exploit-And-Server-Authority]]
4. [[Data-Persistence-DataStores-And-ProfileStore]] → [[Error-Handling-And-Logging]]
5. [[Streaming-And-Instance-Streaming]] → [[Physics-And-Network-Ownership]] → [[Performance-And-Profiling]] → [[Parallel-Luau]]
6. [[Tooling-Rojo-Wally-And-Studio-MCP]] → [[Common-Libraries]]

## Related
- [[Home]]

## Sources
- See each note. Most facts verified 2026-10-04 against the Roblox creator-docs source (github.com/Roblox/creator-docs, mirror of create.roblox.com/docs) and library repositories.
