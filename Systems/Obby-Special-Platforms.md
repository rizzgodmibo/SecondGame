---
tags: [systems/physics, design/obby]
status: reviewed
updated: 2026-10-05
confidence: medium
---
# Obby Special Platforms (ice, wobble, bounce)

## TL;DR
- **Ice:** no code needed. Give the platform `CustomPhysicalProperties` with Friction near 0 and FrictionWeight 100, and a walking Humanoid slides. Measured slide after stopping from a full walk (WalkSpeed 16): friction 0 → 20.3 studs, 0.005 → 7.5, **0.01 → 4.6**, 0.02 → 2.6, 0.05 → 0.9, normal floor → 0.2.
- **Wobble:** a standing Humanoid puts **no weight** on the part under it (measured: 0° of tilt on a free platform). Each client must push the platform down under every character itself (`ApplyImpulseAtPosition(mass × gravity × dt)` in `PreSimulation`).
- **Wobble restoring force:** use four corner `SpringConstraint`s, not `AlignOrientation`. AlignOrientation holds dead level until its MaxTorque is exceeded, then flops to the limit (measured 0° → 25°, nothing in between).
- **Wobble ownership:** simulate a local copy on each client. The anchored original is hidden locally, and the copy is unanchored and owned by that client. A server-owned physics platform stutters while network ownership hands over (DevForum).
- **Bounce:** the owning client sets its own root's velocity along the pad's up vector. Measured apex: 90 studs/s → 20.3 studs, 140 → 50.4 (theory v²/2g = 20.6 and 49.9).
- Working code: Rubber Tower `SurfaceService.luau`, `WobbleController.luau`, `BounceController.luau`, with numbers in `Config.luau`.
- **Added 2026-10-05 (USER-approved, the map v3 combos):**
  - **Water hazard:** mesh water (CanCollide off, CanTouch on). On touch the client splashes, asks the server to ragdoll + count the fall (`HazardService` checks the claim), bobs, then glides ~1 s back to the last combo-start zone and holds the body still until the ragdoll ends.
  - **Seesaw:** the wobble local-copy pattern on a `HingeConstraint` servo that rests at `RestAngle`.
  - **Jelly stiffness per cube:** a `WobbleStiffness` attribute. Scale it by 1/size² for smaller pads, or they tilt far more.
  - **Swing hazards:** anchored, animated on each client from `workspace:GetServerTimeNow()` (`Rules/Movers.swingAngle`); a touch knocks you and the server ragdolls you.
  - **Fan vents and slingshot:** coded and spec-tested, not placed yet.
- **Lessons (2026-10-05):**
  - With **StreamingEnabled** a tagged Model can arrive before its parts: set `ModelStreamingMode = Atomic` and retry on `DescendantAdded`.
  - The server's copy of a falling body lags ~9 studs, so allow claims from above a hazard.
  - In MCP play sessions **`Humanoid.Jump = true` is ignored**: bots must use `ChangeState(Jumping)`.

## Measurements (Studio, Holden's R15 avatar, default gravity 196.2, 2026-10-04)
| Wobble setup (12×12 platform, ball socket at centre, ±25° limit) | Tilt with player 2.5 studs out | at 5 studs |
|---|---|---|
| AlignOrientation, MaxTorque 60,000 | 0° | 0° |
| AlignOrientation, MaxTorque 8,000 | — | 25° (flops) |
| Corner springs k=400 (with client weight) | 19.6° | 25° (limit) |
| Corner springs **k=800**, damping 40 | **8.7°** | **15.5°** |
| Corner springs k=1400 | 4.5° | 9.8° |
The player's mass was 10.8 units; other avatars vary, so tilt varies too. ⚠️ verify with a few different avatars.

## How to build them
1. Tag parts in the place (`IcePlatform`, `WobblePlatform`, `BouncePad`) and keep every number in a Config module.
2. Ice: a server service applies the friction from Config to tagged parts, so tuning never means editing parts by hand.
3. Wobble: on each client, clone the anchored original and remove the tag from the clone. Unanchor it and add a ball socket to an invisible anchored anchor part, plus 4 springs hanging 4 studs down from 80% of the way to each corner. Hide the original locally (Transparency 1, CanCollide/CanQuery/CanTouch false). Then push each copy down where any character's root raycast hits it.
4. Bounce: on the client, a `Touched` on the pad by your own character applies the launch along the pad's up vector, with a short cooldown.

## Pitfalls
- Other players see their own local copy of a wobble platform, so someone else's feet may not line up exactly with the tilt on your screen. That's acceptable for a fun obby, not for competitive play.
- Wobble platforms placed near the walls need room to tilt; the springs hang below them.
- The map audit treats a wobble platform as a flat static part (the anchored original). Bounce launches are not modelled ([[Roblox Map Audit Skill]]).

## Related
- [[Avatar-Ragdoll]] · [[Physics-And-Network-Ownership]] · [[Rubber-Tower]] · [[Difficulty-And-Mastery]]

## Sources
- Local Studio measurements, Rubber Tower test place, 2026-10-04.
- [DevForum: making a character slide on ice](https://devforum.roblox.com/t/making-a-specific-default-character-slide-on-ice/1896896) (friction 0, weight 100).
- [DevForum: wobbly platform and network ownership](https://devforum.roblox.com/t/how-do-i-make-a-platformpart-that-is-wobbly/1506231) (client copy or hand ownership to the toucher).
