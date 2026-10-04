---
title: Deterministic Flight Sim and Ghosts
date: 2026-10-02
tags: [roblox, architecture, security, networking]
project: Paper Plane Toss
---
# Deterministic Flight Sim and Ghosts

**Key idea:** a flight is *calculated*, not recorded. `FlightSim.simulate(glide, planeId, seed)` is deterministic. The server runs it and awards the result; each client replays the same three numbers as an animation.

Why it works:
- **Anti-cheat:** the client never reports a distance.
- **Saving:** almost no data to store.
- **Ghosts:** cheap to send, even on phones. A ghost is just `(glide, planeId, seed)`.

## Ghost decisions (Holden)
- 3 translucent ghosts race you in side lanes: the server's best flight (★) plus the newest flights from other players.
- **Your plane always has a yellow outline** and flies in the middle lane.
- There's no reward for beating a ghost.
- The server keeps the last 10 flights plus the best one for late joiners.

![[Render Plane.png|250]]

## Fixes along the way
- **Plane flew tail-first:** imported GLBs face backwards; fixed with `PivotOffset = CFrame.Angles(0, π, 0)`.
- **"Get some air before bouncing":** added a launch arc (climbs about 16 studs, 1.8× the distance before the first bounce).
- **Rewards** are saved when the throw starts and shown on landing, so leaving mid-flight loses nothing.

Related: [[Paper Plane Toss]], [[Paper Plane Toss Progression Numbers]], [[Blender to Roblox Asset Pipeline]]
