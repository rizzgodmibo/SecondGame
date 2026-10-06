---
tags: [systems/destruction, systems/security, reference/modules]
status: reviewed
updated: 2026-10-06
confidence: medium
---
# Destruction Modules Audit: VoxBreaker and VoxelDestruct (read only, nothing installed)

## TL;DR
- Holden (2026-10-06) allowed **reading and auditing** VoxBreaker and VoxelDestruct as references, with the audit shown **before any install**. **Nothing was installed.** Trap Your Friends uses its own small module instead ([[Trap-Your-Friends]], `src/shared/Rules/Fracture.luau` + `DestructionService`).
- **VoxBreaker:** MIT licence, open source on GitHub. The source scan found no HttpService, loadstring/getfenv, asset-id requires or remote creation. Its author tested it mainly on the client. **Clean to use as a reference; safe to install if ever needed.**
- **VoxelDestruct 2.1:** a Creator Store model only, **no public source and no explicit licence** found. It can't be audited without inserting the model, so it was **not audited**. Treat it as untrusted until someone reads the inserted code ([[Asset-Creation-Workflow-And-Marketplace]] backdoor checklist).
- Why our own module: it needs **server-authoritative collision** (anchored remainder pieces), **cuts on whole-stud lines** so legacy studs stay aligned, and **client-only lingering debris**. Neither module offers all three as is.

## VoxBreaker (Bartokens)
| Item | Finding |
|---|---|
| Source | https://github.com/Bartokens/VoxBreaker (files `VoxBreaker.lua` 1,406 lines, `PartCache.lua` 191, `PartCacheTable.lua` 106, `Documentation.lua`); Creator Store asset 17183252736 |
| Licence | **MIT** (`LICENSE`, © 2024 Bartokens); the devforum post says "free to use and you don't have to credit me" |
| Version | Thread from 2024-04-18, last update 2024-07-15 (per the thread) |
| How it works | Splits parts that carry a `Destroyable` attribute using quadtree/octree partitioning down to a minimum voxel size; quadtrees for thin-in-Y parts; no greedy meshing; reset timer; PartCache. Moveable hitboxes use `RenderStepped` (client); the author says server use is untested for performance |
| Security scan (local copy in the session scratchpad, 2026-10-06) | `grep` for `require(<number>)`, HttpService, loadstring, getfenv/setfenv, RemoteEvent/RemoteFunction, InsertService, MarketplaceService, TeleportService: **none** in code (only doc comments and `require(script.PartCache)` / `require(script:WaitForChild("Table"))`) |
| Known issues (thread) | Occasional oversized voxels with PartCache on the client; parts sometimes don't reset; a brief flash when first voxelising; "expect some issues with performance" for big destruction |
| Fit for Trap Your Friends | Its splitting is close to ours, but it voxelises to a size rather than to the stud grid (studs can misalign) and it targets client-side use (we want server-owned holes) |

## VoxelDestruct 2.1 (SalvatoreScripts)
| Item | Finding |
|---|---|
| Source | Creator Store asset 18228357194 (https://create.roblox.com/store/asset/18228357194/VoxelDestruction-OOP-Voxel-Destruction-Tool); **no GitHub / open source link** in the thread |
| Licence | **None stated**; only Creator Store terms |
| Version | 2.1, thread from 2024-06-28 |
| How it works (thread) | Server-side by default, `OnClient` option; greedy meshing; PartCache (10,000 pre-made parts by default); `destroy` / `hitbox` / `Repair` / `cleanup`; reset timers; `RecordDestruction` for late joiners |
| Security | **Not audited** (needs the model inserted to read it; not done). The thread mentions no HttpService/loadstring use, but that isn't evidence |
| Known issues (thread) | A latency pause when debris spawns (fix: server network owner); slower than VoxBreaker when spammed |
| Fit | Its server-side greedy-meshed debris conflicts with our rule "no unanchored server parts for destruction" |

## What Trap Your Friends took from them (ideas only)
- Mark breakable parts with a tag/attribute, use part caching, add a reset timer, and keep a record of breaks for late joiners (we get that free: broken state is plain instances).
- Use a bigger minimum piece for big hitboxes (performance). Our minimum stays 1 stud (USER 2026-10-06).

## Pitfalls
- Creator Store "free model" modules can hide backdoors in nested scripts. Read every script after inserting, before using one.
- Voxelising to a fixed size on a stud-textured part misaligns studs; split on the part's own grid instead.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Style-Test-v2-Plan]] · [[Trap-Your-Friends-Reference-Board]] · [[Anti-Exploit-And-Server-Authority]] · [[Asset-Creation-Workflow-And-Marketplace]]

## Sources
- VoxBreaker thread: https://devforum.roblox.com/t/voxbreaker-an-oop-voxel-destruction-module/2935099 (read 2026-10-06)
- VoxBreaker source: https://github.com/Bartokens/VoxBreaker (raw files fetched and scanned 2026-10-06)
- VoxelDestruct thread: https://devforum.roblox.com/t/voxeldestruct-21-voxelated-destruction-physics-with-greedy-meshing-hitboxes-and-more/3044264 (read 2026-10-06)
