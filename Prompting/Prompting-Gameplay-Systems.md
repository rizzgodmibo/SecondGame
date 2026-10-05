---
tags: [prompting/systems, systems/architecture]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Gameplay Systems, Networking, Data and Security

How to ask Claude for a new game system (combat, shop, pets, checkpoints, saving) so it comes back server-authoritative, typed, testable and in the project's existing style. General rules: [[Prompting-Principles]].

## TL;DR
- **One system per request, built in small steps that each have a check.** Roblox's OpenGameEval found agents near-perfect on atomic tasks and weak on multi-step ones across the hierarchy and client/server split. Fish a Monster was built as 9 one-system steps, each planned, approved, built, playtested and committed (local).
- **State the security model in the prompt:** client sends intent only; every remote is rate-limited → type-checked as `unknown` → validated → acted on; the server recomputes rewards, prices and cooldowns ([[Remotes-And-Networking]], [[Anti-Exploit-And-Server-Authority]]).
- **Point at existing patterns** ("follow how `PlayerData` and the remotes registry already work"), so Claude doesn't invent a second framework (Anthropic; [[Roblox Development Playbook]]).
- **Ask for formulas as pure modules with specs, and numbers in Config**, so balance is data and logic is testable off Roblox ([[Roblox Code Gate Skill]]).
- **Ask for an exploit test, not just a happy path:** a temporary Studio-only `Dev*.luau` script that fires the real remotes with junk arguments, other players' ids and spam ([[Studio Only Dev Test Scripts]]).

## What Claude needs from you
- The behaviour in player terms, including edge cases you care about (leaving mid-action, dying, rejoining, two servers).
- Which numbers are decided (`USER`) and which Claude may propose.
- What already exists: data module, remotes registry, Config, UI kit, and which files it may touch.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Client-Server-Boundary-And-Replication]] · [[Remotes-And-Networking]] · [[Anti-Exploit-And-Server-Authority]] | Intent vs result, the 4-step remote guard, NaN checks, never `InvokeClient`, score-based detection |
| [[Data-Persistence-DataStores-And-ProfileStore]] · [[Roblox Persistence and Session Failure Runbook]] | ProfileStore, versions and migrations, budgets, session-failure decisions |
| [[ProcessReceipt-Handling]] · [[Roblox Purchase Receipt Handling]] | Idempotent grants keyed on `PurchaseId` (for any system that sells something) |
| [[Physics-And-Network-Ownership]] · [[Avatar-Ragdoll]] · [[Obby-Special-Platforms]] | Ownership rules and measured, working patterns |
| [[Module-Architecture]] · [[Luau-Strict-Typing]] · [[Error-Handling-And-Logging]] · [[Deprecated-API-Replacements]] | Structure, types, `pcall` + backoff, current API names |
| [[Idle-And-Offline-Earning]] · [[Daily-Rewards-And-Streaks]] · [[Leaderboards]] | Server-time patterns that resist clock exploits |

## Prompts

### 1. Plan a new system
```text
Plan the [SYSTEM] system for [Game]. Plan only: no code until I approve.

READ FIRST: the project hub and GDD section for [SYSTEM]; Systems/Remotes-And-Networking.md; Systems/Anti-Exploit-And-Server-Authority.md; Systems/Data-Persistence-DataStores-And-ProfileStore.md; and the existing code in src/ (how PlayerData, Config and the remotes registry work now). Follow those patterns; don't add a new framework or library without asking.

BEHAVIOUR: [what the player does and sees, step by step, including edge cases: leaves mid-action, dies, rejoins, spams the button].
DECIDED NUMBERS (USER): [list]. Anything else you propose goes in Config and is tagged DRAFT.

Give me:
1. Server vs client split: what the client sends (intent only) and what the server decides.
2. Every remote: name, direction, payload type, rate limit, validation steps.
3. Saved data changes: new fields, schema version bump, migration for old saves.
4. Pure rules (formulas, rolls) that go in src/shared/Rules with Lune specs.
5. The file list (new / changed), and how you'll test it, including an exploit test.
6. Risks and anything you'd accept as a known limitation.
```
Why: "plan + file list, then wait" is Holden's rule and Anthropic's explore-plan-code workflow; listing remotes and data up front is where most security and save bugs are caught.

### 2. Build it (after approval)
```text
Build the [SYSTEM] plan you gave me (approved, with these changes: [changes]).
- --!strict everywhere; treat every remote argument and attribute as unknown and narrow it (typeof, NaN and inf checks, length caps).
- Use current APIs only (check Systems/Deprecated-API-Replacements.md): task.*, Animator:LoadAnimation, LinearVelocity etc.
- Numbers in Config; formulas in src/shared/Rules with specs.
- Write a temporary src/server/DevTest[System].server.luau (or .client), gated by RunService:IsStudio(), that prints PASS/FAIL lines for: the happy path, junk arguments, another player's id, spamming past the rate limit, and leaving mid-action.
DONE WHEN: the code gate prints GATE PASS, and a Studio playtest shows every DevTest line PASS. Quote both. Then delete the DevTest script, confirm git status is clean, and stop for my review.
```

### 3. Saving and migrations
```text
Add these fields to the player profile for [SYSTEM]: [fields].
Bump the schema version and write a migration that upgrades a real old save (not a hand-made table). Test it by loading a save made with the current code before your change (Resources/Studio Only Dev Test Scripts.md), and show the before/after data.
Rules from Systems/Data-Persistence-DataStores-And-ProfileStore.md: no saving on every change, never write after the session ends, reject saves with a newer schema, and the loader never replaces an unreadable profile with defaults.
List any field a rollback to the previous build would break.
```
Why: Fish a Monster's v2 migration was tested on a real v1 save; the runbook lists the failure cases ([[Fish a Monster Saving and Offline Income]]).

### 4. Security review of an existing system (fresh session)
```text
Review [files] as an exploiter would. Assume the client runs any Luau and can fire any remote with any arguments.
For each remote handler: is it rate-limited, are all args validated as unknown (including NaN, inf, negative, huge strings), does the server recompute the result, can a player affect another player, and what happens if they leave mid-call?
Also check: InvokeClient use, trusting client-sent Player/UserId, data written before the profile loads, and server-side effects that should be client-side.
Report findings by severity with file:line and the smallest fix. Report real gaps, not style.
```
Why: the read-only `roblox-dev:roblox-reviewer` audits found real medium issues in Fish a Monster and Paper Plane Toss before release ([[Fish a Monster Pre-Publish Review]], [[Paper Plane Toss Release Prep]]).

### 5. Physics and movement features
```text
I want [FEATURE: e.g. a shove / knockback / moving platform]. Before writing code, tell me who owns the physics of each part involved (Systems/Physics-And-Network-Ownership.md) and where the force must be applied so it's visible (the owning client vs the server). Measure, don't guess: use a DevTest script to print the real numbers (distance, height, time) and compare with your predicted values, like the bounce-pad test in Systems/Obby-Special-Platforms.md.
```
Why: server velocity writes on a player's body are overwritten by the owning client ([[Avatar-Ragdoll]]); measured numbers beat theory.

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Melee combat (server-validated)
```text
Plan melee combat for [Game]: the client sends "swing" with its aim; the server checks the cooldown ([0.5 s]), finds targets in a box in front of the attacker with GetPartBoundsInBox, applies damage from Config, and tells clients to play hit VFX and sound. Validate the swing rate, distance and line of sight on the server. List the remotes and the exploit cases (spam, reach, hitting through walls) and the DevTest checks for each. Plan only.
```
The vendor example on Obby's blog used Region3; current API is `GetPartBoundsInBox` ([[Deprecated-API-Replacements]]).

### Inventory with unique ids
```text
Add an inventory to [Game]: each item has a unique id, a type from Config and per-item data ([level, size]); a capacity of [N] with a clear "full" message; equip/unequip requests validated on the server; saved in the profile with a schema bump. Show the data shape, the remotes and how the UI reads it (it never edits items itself). Plan first.
```

### NPC behaviour as a state machine
```text
Make an NPC for [Game] that [patrols between waypoints and chases players within 10 studs, giving up after 30 studs]. Write it as a state machine (Idle, Patrol, Chase, Return) with the transition rules in Config. Animations on the server-created Animator; pathfinding with PathfindingService and a fallback when no path. Test it with a DevTest script that logs each state change, including when the target dies or leaves.
```
Roblox's own Assistant examples include a patrol-and-chase NPC ([[Community-Prompt-Examples]] §10).

### Quests with a state table
```text
Add quests to [Game]. States: available, accepted, active, completed, claimed (plus abandoned if I approve it). Progress is counted on the server from real events (never a client message). Rewards granted once, saved with the quest id. Give me the state table, the data shape, which events advance which quest types, and the DevTest cases (double-claim, rejoin mid-quest, quest list changed in an update).
```

### Rounds and a lobby
```text
Plan a round system for [Game]: lobby → intermission [20 s] → round [3 min] → results → lobby, with a minimum of [2] players. One server-side round controller owns the state; clients get the state and time left. Handle players joining mid-round, leaving, and everyone leaving. Plan only; list the files.
```

### Pets that follow and give a boost
```text
Add pet following to [Game]: equipped pets (up to [3], plus the pass slot) follow their owner on the owner's client (smooth, no server physics), the server only stores which pets are equipped and computes the boost. Other players see your pets via a replicated list, rendered on their clients. Show me the cost with [8] players × [3] pets on a phone-sized test.
```

### Trading (plan only, high risk)
```text
Plan a trading system for [Game]. Don't build it yet. Requirements from Design/Economy-Design-Sinks-And-Faucets.md: unique item ids, both players confirm twice, an atomic swap with both profiles session-locked and no yields, a trade log, IsPaidItemTradingAllowed respected per player, and a cooldown. List every way it could dupe or scam and how the plan prevents each. Tell me what you'd test before it ever goes live.
```

## How to check the result
- Code gate `GATE PASS` (build, specs, selene with warnings failing, stylua).
- DevTest PASS lines in Output, including the exploit cases; then the script is deleted and git is clean.
- For saves: a real old save upgrades; a forced load failure doesn't overwrite data.
- A fresh-context security review with no high-severity findings.

## Pitfalls
- **Huge one-shot requests** ("make the whole pet system") fail more often; split into roll → inventory → equip → UI ([[Fish a Monster Build Steps]]).
- **Client-side "security".** LocalScript checks are UX only ([[Client-Server-Boundary-And-Replication]]).
- **Whole-profile pushes** every tick redrew 14 menus per second in Paper Plane Toss; ask for targeted updates ([[Paper Plane Toss Release Prep]]).
- **Server-side cosmetic effects** (bobber shake every frame) replicate to everyone; ask for a flag + client animation ([[Fish a Monster Pre-Publish Review]]).
- **`execute_luau` can't fire remotes** and caches modules; exploit tests must run through DevTest scripts ([[Roblox Studio MCP Quirks]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Debugging-And-Testing]] · [[Prompting-Monetisation]] · [[Systems/_Index|Systems index]]

## Sources
- Roblox, OpenGameEval announcement (atomic vs multi-step tasks), 2025-12-17: <https://about.roblox.com/newsroom/2025/12/opengameeval-benchmark-agentic-ai-assistants-roblox-studio>
- Anthropic, Claude Code best practices (explore-plan-code, reference existing patterns): <https://code.claude.com/docs/en/best-practices>
- Local: [[Fish a Monster Build Steps]], [[Fish a Monster Pre-Publish Review]], [[Paper Plane Toss Release Prep]], [[Rubber-Tower-Build-Status]].
