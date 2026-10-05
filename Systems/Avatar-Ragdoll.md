---
tags: [systems/physics, systems/characters]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Avatar Ragdoll (player's own avatar)

## TL;DR
- **Verified in Studio (2026-10-04):** a live R15 player avatar uses the **avatar joint upgrade**. It has 15 `AnimationConstraint` joints (`IsKinematic = true`) and 14 always-on `BallSocketConstraint`s (for example `LeftShoulderBallSocket`: `UpperAngle` 110, twist ±85, friction about 22). It has **no Motor6Ds**. The old "swap Motor6D for BallSocket" guides don't apply to these avatars.
- **To ragdoll an upgraded rig, switch its non-root AnimationConstraints off.** Roblox's own sockets hold the body together. Keep the `Root` joint. For Motor6D rigs (R6 rigs from `CreateHumanoidModelFromDescription`, older R15), add your own disabled sockets and swap.
- **The server decides, the owning client moves.** The player's client simulates its own character. The server switches the joints and sets a `Ragdolled` attribute, and the client puts its Humanoid in `Physics`. Server-owned rigs (dummies) use `PlatformStand`.
- **Validating a fall:** the server's copy of a falling character lags behind. A fall that the client sees at 12 studs, the server saw at only 2.7 studs, moving at -32 studs/s. Remember the fastest recent fall speed for each player, rather than checking once when the request arrives.
- **Cost measured on Holden's PC in Studio:** 16 ragdolling dummies took about 1.4 ms of server physics per frame, or about 0.9 to 1.5 ms of client physics when the client owned them, at a steady 60 FPS. **Not measured on a phone yet.**
- Working code: Rubber Tower `src/server/Services/RagdollService.luau` (see [[Rubber-Tower-Build-Status]]).

## How it works (Rubber Tower implementation)
1. **Setup**, server side, once the avatar's appearance has loaded (body parts and joints get replaced while it loads):
   - `BreakJointsOnDeath = false` and `RequiresNeck = false`, so a disabled Neck joint never kills the player.
   - For each non-root joint: reuse the built-in socket (upgraded rig), or build a socket on two new attachments. Their X axis points down the limb, so "twist" is rotation around the bone.
   - A `NoCollisionConstraint` for each joint pair, so overlapping neighbouring limbs don't jitter.
   - Accessory handles are made `Massless`.
2. **Ragdoll on:**
   - Switch the joints off (and our own sockets on).
   - Limbs get `CanCollide = true`. The root gets `CanCollide = false`, otherwise it props up the body.
   - Set the network owner (the player for their own character).
   - Set the attribute `Ragdolled = true`. The owning client calls `ChangeState(Physics)`, stops its animation tracks, and re-asserts Physics every frame while the attribute is true.
3. **Recover:** once the minimum time is up and the torso has been still (under 4 studs/s) for the recovery time, or always at `MaxSeconds`. The client stands the root upright (pointing the way the body was facing, 2 studs up) and calls `GettingUp`.
4. **Timed ragdolls stack.** A timed ragdoll (a shove) on a body that is already ragdolled extends it, so being ragdolled never makes a player immune.

## Fall detection
- The client records the take-off height: the last floor height from the previous 0.3 s, else the height when Freefall starts. When the root has dropped at least `FallMinDropStuds` below it, the client fires `RagdollRequest` with no arguments.
- Measuring from take-off, not from the top of the jump, means normal jumps and bounce pads that land at the same height never ragdoll.
- The server accepts the request when the player is alive, rate-limited, and the replicated vertical speed is at least half the speed of a real 12-stud fall (`sqrt(2·g·12)` ≈ 68.6 studs/s). It checks over the next 0.5 s, or against the fastest speed from the last 0.4 s.
- **Test artifact:** if you teleport a character into the air, Freefall begins a few frames late, so the measured drop comes out short. Test the threshold by walking off ledges instead.

## Measurements (Studio on Holden's PC, 2026-10-04; local observation, not a phone)
| Case | Server physics per frame | Client physics per frame | FPS |
|---|---|---|---|
| Idle, no dummies | 0.00 ms | — | 60 |
| 16 dummies standing | 0.05 ms | — | 60 |
| 16 dummies ragdolling, server-owned | avg 1.37, max 1.60 ms | — | 60 |
| 16 dummies ragdolling, owned by the client | 0.04 ms | avg 0.91, max 1.28 ms | 60 |
| After recovery | 0.11 ms | — | 60 |

These are dummies with Holden's avatar, half R15 and half R6. A real server's players simulate their own bodies, so the client-owned row is closer to a player's device. Measure on a real phone before setting `MaxSimultaneous` below 16.

## Pitfalls
- **A gitignored dev script still syncs.** Rojo syncs every file in a mapped folder. Exclude dev tools with `globIgnorePaths` in the publishing project file, and serve a separate `dev.project.json` while testing ([[Rojo Workflow Gotchas]]).
- **Server-side velocity writes on a player's body get overwritten** by its owning client. A shove's knockback must be applied by the target's client, or the server must briefly take ownership. This matters for Rubber Tower phase 3.
- **The client controls its own body, so an exploiter can ignore a ragdoll.** A movement guard ([[Anti-Exploit-And-Server-Authority]]) should flag a player who is "Ragdolled but upright and walking".
- ⚠️ verify: whether every live avatar is now on the joint upgrade, or only some (only Holden's avatar in Studio was checked). The code handles both kinds.

## Related
- [[Physics-And-Network-Ownership]] · [[Anti-Exploit-And-Server-Authority]] · [[Rubber-Tower]] · [[Rubber-Tower-Reference-Obbies]] · [[Join Cutscene and Tutorial]] · [[Roblox Studio MCP Quirks]]

## Sources
- Local Studio observation and self-test output, Rubber Tower test place, 2026-10-04 (joints read from a live R15 player; 15/15 self-test PASS; walk-off and drop tests).
- Code review by the `roblox-dev:roblox-reviewer` agent, 2026-10-04 (no high-severity findings; fixes applied).
