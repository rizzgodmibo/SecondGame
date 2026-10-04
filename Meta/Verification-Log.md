---
tags: [meta/verification]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Verification Log

Append one row whenever a claim is checked against a source.

| Date | Note | Claim | Result | Source |
|---|---|---|---|---|
| 2026-10-04 | AI-Assisted-Workflow | Individual mesh max 20,000 triangles | Confirmed | https://create.roblox.com/docs/art/modeling/specifications |
| 2026-10-04 | AI-Assisted-Workflow | 8K textures improve in-game quality | Contradicted (max 4096, rec. ≤1024) — needs deeper check | https://create.roblox.com/docs/art/modeling/texture-specifications |
| 2026-10-04 | Robux-Economy-DevEx-And-Platform-Cuts | DevEx $0.0038/R$ since 2025-09-05; 30,000 R$ minimum | Confirmed via Roblox/creator-docs mirror | github.com/Roblox/creator-docs |
| 2026-10-04 | Subscriptions-And-Premium-Payouts | Premium Payouts deprecated 2025-07-24 → Creator Rewards | Confirmed via creator-docs mirror | github.com/Roblox/creator-docs |
| 2026-10-04 | Discovery-Algorithm | 2026-06-15: 28-day window; QPTR replaced by play-through rate + first-play bounce | Confirmed via creator-docs mirror | github.com/Roblox/creator-docs |
| 2026-10-04 | Data-Persistence-DataStores-And-ProfileStore | DataStore budgets 60+40×players/min; per-key 25 MB/min read, 4 MB/min write; storage 500 MB + 1 MB×lifetime users | Confirmed via creator-docs mirror | github.com/Roblox/creator-docs |
| 2026-10-04 | Remotes-And-Networking | UnreliableRemoteEvent payload >1000 bytes dropped | Confirmed via creator-docs mirror | github.com/Roblox/creator-docs |
| 2026-10-04 | Data-Persistence-DataStores-And-ProfileStore | ProfileStore v1.0.3: autosave 300 s, session steal 40 s, dead-session 630 s | Confirmed from library source | github.com/MadStudioRoblox/ProfileStore |
| 2026-10-04 | Physics-And-Network-Ownership | PhysicsService collision-group methods deprecated → workspace:RegisterCollisionGroup; 32-group cap | Confirmed via creator-docs mirror | github.com/Roblox/creator-docs |
