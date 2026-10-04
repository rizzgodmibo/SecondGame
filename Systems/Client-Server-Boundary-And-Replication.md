---
tags: [systems/networking, systems/security]
status: draft
updated: 2026-10-04
confidence: high
---
# Client-Server Boundary and Replication

## TL;DR
- The server is the **only** source of truth for anything that matters (currency, inventory, damage, progression, purchases). The client renders, predicts, and sends **intents** ("I pressed attack at target X"), never **results** ("I dealt 50 damage").
- Changes made on the server to replicated containers replicate to clients. Changes made by a client **do not** replicate (FilteringEnabled is always on) — except physics of parts it network-owns, its character (Humanoid state, animations), and a few input-driven properties.
- Anything in ReplicatedStorage, ReplicatedFirst, Workspace, StarterGui/StarterPack/StarterPlayer is downloadable and decompilable by exploiters. Server-only code/data → ServerScriptService / ServerStorage.
- Use **Attributes** for small replicated per-instance state (e.g. `Player:SetAttribute("Coins", n)` for HUD). Use remotes for events and larger/structured payloads. Avoid `IntValue`/`StringValue` objects for new code.
- Replicate the **minimum** each client needs; per-player private data goes via `FireClient`, not attributes on shared instances.

## Details

### What replicates (server → client)
| Server action | Replicates? |
|---|---|
| Create/destroy/modify instances under Workspace, ReplicatedStorage, ReplicatedFirst, Lighting, SoundService, Teams, Players (player objects), StarterGui etc. | Yes (Workspace content subject to [[Streaming-And-Instance-Streaming]]) |
| Anything under ServerScriptService / ServerStorage | **Never** |
| Attributes on replicated instances | Yes |
| Tags (`CollectionService`) on replicated instances | Yes |
| Changes to `PlayerGui` from the server | Yes, to that player only — but avoid; let the client own its UI |
| Lua variables / module state | No — each side has its own Luau VM; modules required on both sides are **separate copies** |

### What a client can change that the server/others see
| Client action | Effect |
|---|---|
| Move its own character (CFrame/physics) | Replicates — client network-owns its character. **This is why speed/fly/teleport hacks exist.** See [[Anti-Exploit-And-Server-Authority]] |
| Physics of unanchored parts it network-owns | Replicates (position/velocity) — see [[Physics-And-Network-Ownership]] |
| Play animations on its own character via Animator | Replicates |
| Humanoid state changes on own character (e.g. jump, sit) | Replicate in practice ⚠️ verify: exact list of replicated Humanoid properties |
| Fire remotes | Server receives — the **only** legitimate client→server data channel |
| Create/destroy/modify anything else (incl. deleting parts of its own character, local UI) | Local only, except that destroying own character parts/tools may replicate ⚠️ verify: current behaviour for character descendant deletion |
| Sound playback with `SoundService.RespectFilteringEnabled = false` | Replicates → set it **true** |

### Attributes vs Value objects vs remotes
| Use | Choose |
|---|---|
| Small state on an instance that all clients may see (door open, NPC health, player level) | Attribute (`SetAttribute`, `GetAttributeChangedSignal`) |
| Per-player private numbers shown in HUD (coins) | Attribute on the `Player` object is fine (other players can read it — acceptable for coins, not for secrets) |
| Structured/private data (inventory, quest state) | Remote: send full snapshot on join, then deltas |
| Grouping/marking instances for systems | `CollectionService` tags |
| Legacy `IntValue`/`ObjectValue` | Only for `ObjectValue` references or legacy tooling (leaderstats needs `IntValue`s in a `leaderstats` folder) |

Attribute limits: supported types include string, boolean, number, UDim, UDim2, BrickColor, Color3, Vector2, Vector3, CFrame, NumberSequence, ColorSequence, NumberRange, Rect, Font, EnumItem ⚠️ verify: full list and per-name constraints (name ≤100 chars, alnum/underscore, no `RBX` prefix).

### Replication order and timing
- Initial replication: the client receives the DataModel snapshot before `game.Loaded`; with streaming, Workspace content arrives progressively — always `WaitForChild` / stream-aware code on the client.
- Property changes made in the same server frame arrive together, but **ordering between remotes and property replication is not something to rely on** — if a remote references an instance created the same frame, the client may need `WaitForChild` or the instance passed as an argument may arrive as `nil` if not yet replicated/streamed.
- Instances passed through remotes arrive as `nil` if the receiver can't see them (server-only containers or not streamed in).

### Client-side ownership rules (what to let the client do)
Let the client own: camera, UI, input handling, local VFX/sounds, cosmetic tweens, client prediction of its own actions, non-authoritative interpolation of other entities.
Never let the client own: currency/inventory mutations, cooldown truth, damage, hit confirmation, purchases, quest completion, matchmaking decisions, admin actions.

### Server authority model (engine feature)
Roblox ships a **Server Authority** mode (`Workspace.AuthorityMode = Server`) that runs a deterministic simulation on server and client with client prediction and rollback, preventing client-reported position cheats. Requires `NextGenerationReplication`, `PlayerScriptsUseInputActionSystem`, `SignalBehavior = Deferred`, `UseFixedSimulation`, `StreamingEnabled`; logic goes in `RunService:BindToSimulation()` and input via the Input Action System. ⚠️ verify: release status (beta vs GA) and platform limitations before using in production. Use it for competitive FPS/combat/racing; classic games (simulators, tycoons, obbies) don't need it.

## Checklist
- [ ] No ModuleScript in ReplicatedStorage contains secrets (API keys, admin IDs you care about, unreleased loot tables).
- [ ] `SoundService.RespectFilteringEnabled = true`.
- [ ] Every client→server path is a remote with validation ([[Remotes-And-Networking]]).
- [ ] Client code tolerant of instances not being present (`WaitForChild` with timeout or `ChildAdded`).
- [ ] Per-player private data sent with `FireClient`, not attributes on shared objects.

## Pitfalls
- Assuming a server-side `print` of a client-made change means it replicated — it doesn't; the server never sees client-side edits.
- Treating `LocalScript` checks ("only fire if player has enough coins") as security. They're UX only.
- Putting a `RemoteFunction` result into a module cache on the client and trusting it later on the server.
- Using `workspace:FindFirstChild` in client code that runs before streaming delivered the part.
- Exposing per-player data via attributes on a shared instance (anyone can read).

## Related
- [[Remotes-And-Networking]]
- [[Anti-Exploit-And-Server-Authority]]
- [[Physics-And-Network-Ownership]]
- [[Streaming-And-Instance-Streaming]]
- [[Module-Architecture]]

## Sources
- https://create.roblox.com/docs/projects/client-server (via github.com/Roblox/creator-docs, 2026-10-04)
- https://create.roblox.com/docs/scripting/security/client-server-boundary
- https://create.roblox.com/docs/scripting/attributes
- https://create.roblox.com/docs/projects/server-authority (setup requirements read 2026-10-04)
