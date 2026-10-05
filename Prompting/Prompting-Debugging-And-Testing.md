---
tags: [prompting/debugging, systems/testing]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Bugs, Playtests, Code Review and Performance

How to report bugs to Claude, let it test in Studio, review code and chase performance. General rules: [[Prompting-Principles]].

## TL;DR
- **A good bug prompt has four parts: target, symptom, boundary, proof.** "Inspect `ServerScriptService.Checkpoints`. After touching Stage3 and resetting, I sometimes spawn at Stage1. Find the root cause, change only the checkpoint system, then playtest by touching Stage3 and resetting twice, and report the spawn each time" (vendor reading of OpenGameEval; matches Anthropic's "describe the symptom, the likely location and what fixed looks like").
- **Ask for the root cause, not a silenced error** ("don't wrap it in pcall to hide it") (Anthropic).
- **Let Claude test in Studio through the MCP:** start play → read Output → screenshot → fix → repeat. Exploit and flow tests go in temporary `Dev*.luau` scripts because `execute_luau` can't fire remotes ([[Roblox Studio MCP Quirks]]).
- **Real phone tests find what Studio hides.** Send Claude the phone recording; it breaks the video into frames and lists problems with causes ([[2026-10-03 Paper Plane Toss Phone Playtest]]).
- **After two failed fixes, start a fresh session** with a better prompt that includes what you learned (Anthropic).

## What Claude needs from you
- Exact steps to reproduce, how often it happens, device (phone/PC), and when it started (which change or build).
- Screenshots, a screen recording, or the Output/Error Report text, pasted as data.
- Whether Claude may start/stop a playtest right now (if you're testing in Studio, it will interrupt you).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Roblox Studio MCP Quirks]] · [[Studio Only Dev Test Scripts]] | What the MCP can and can't do; the DevTest method; timeouts, caching, white screenshots |
| [[Error-Handling-And-Logging]] · [[Performance-And-Profiling]] | `pcall` + backoff, structured logs, MicroProfiler/Script Profiler, frame budget 16.67 ms |
| [[Video Frame Extraction with Blender]] | How to turn a phone recording into frames without ffmpeg |
| [[Roblox Mobile UI Layout]] · [[Roblox Texture Upload Failures]] | Phone layout traps; textures loading grey |
| `Bugs/` folder (create it on the first logged bug) and the project notes | Past bugs and fixes; search before debugging |

## Prompts

### 1. Bug report
```text
Bug in [Game]: [SYMPTOM, e.g. "after I rebirth, my pets disappear from the equip bar until I rejoin"].
Steps: [1, 2, 3]. Happens [always / about 1 in 5]. Device: [phone / PC / both]. Started after [change/build, if known].
Likely area: [file or system, if known].
Search the vault (Bugs/ and the project notes) for anything similar first. Then find the root cause; don't hide the error with pcall or a retry. Change only what the fix needs.
DONE WHEN: you reproduce it first (show the failing Output or screenshot), then show the same steps passing after the fix, plus the code gate result. Log the bug and fix in Bugs/ with the cause.
```
Why: reproduce-then-fix with evidence is Anthropic's "write a failing test, then fix it" adapted to Studio; logging the cause is the vault's "write the fix down" rule.

### 2. Let Claude playtest a feature
```text
Test [FEATURE] in Studio. Ask me before starting play if I might be testing.
1. list_roblox_studios, then start play.
2. Drive the test with a temporary DevTest script (Studio-only, RunService:IsStudio()) that prints PASS/FAIL lines; set workspace attributes from execute_luau to trigger steps. Split anything longer than about 50 s, since MCP calls time out at about 60 s.
3. Read get_console_output and take screenshots at the key moments. If screenshots come back white, say so; don't claim you saw it.
4. Stop play, delete the DevTest script, confirm git status is clean.
Report: every PASS/FAIL line, the screenshots, and anything that looked wrong even if the test passed.
```
Why: every trap in that prompt cost time before: timeouts, cached modules, blank screenshots, and interrupting Holden's own test ([[Roblox Studio MCP Quirks]]). On Rubber Tower, Claude never actually saw its map because every screenshot was white ([[Rubber-Tower-Map-v3-Critique]]).

### 3. Review a phone playtest recording
```text
Here's my phone playtest: [video path], plus my notes: [notes]. Phone: [model], landscape.
Break the video into frames every 1.5 s (Resources/Video Frame Extraction with Blender.md) and review them with my notes.
Give me a table: what's wrong, the frame/time, the likely cause in code or layout, and the fix. Separately list things that look wrong but are fine, so I don't chase them. Don't change code yet; I'll pick what to fix.
```
Why: this exact flow found 7 extra problems in Paper Plane Toss's first phone test, with causes, and a "looked wrong but was fine" list ([[2026-10-03 Paper Plane Toss Phone Playtest]]).

### 4. Code review (fresh session or subagent)
```text
Use a subagent with fresh context to review [the diff / files] against [PLAN or the approved plan text].
Check: every requirement implemented; server authority and remote validation; data safety (no writes after session end, migrations); leaks (connections, LoadAnimation every call, tables per frame); mobile cost (per-frame work, whole-profile pushes, server-side particles); deprecated APIs; anything outside the task's scope that changed.
Report only gaps that affect correctness, safety or the plan, by severity with file:line and the smallest fix. Style preferences go in a short "optional" list.
```
Why: Anthropic recommends an adversarial reviewer in a fresh context and warns that reviewers always find "something", so restrict them to real gaps. The `roblox-dev:roblox-reviewer` agent does this read-only.

### 5. Performance on phones
```text
[Game] stutters on phones when [situation]. Don't guess: measure.
Add a temporary Studio-only dev panel or Output lines for frame time, server Heartbeat, instance count and remote traffic in that situation (Systems/Performance-And-Profiling.md). Find the top 3 costs with numbers, propose fixes in order of gain per effort, and say which need a real-phone re-test. Studio numbers on my PC are not phone numbers; label them.
```
Why: optimising from Studio numbers is a listed pitfall; Rubber Tower's ragdoll cost table is honest about "PC only, phone row missing" ([[Avatar-Ragdoll]]).

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Deprecated API sweep
```text
Search every script in src/ for deprecated APIs using Systems/Deprecated-API-Replacements.md (wait/spawn/delay, BodyVelocity and other BodyMovers, Humanoid:LoadAnimation, non-Async names, PhysicsService collision groups). List each hit with file:line and the replacement. Fix them in one batch only after I approve, then run the code gate and a playtest.
```
An example ask from the DevForum Studio MCP thread ([[Community-Prompt-Examples]] §8).

### Screenshot review
```text
Start play, open [screen/area], take screenshots at player-eye height and from [angle], and tell me what looks off: overlaps, clipping, floating parts, unreadable text, anything that doesn't match Resources/Art Direction Feedback.md. If the screenshot is blank or white, say so instead of guessing. Don't change anything; give me a list.
```

### Memory leak hunt
```text
Memory grows over time in [Game] when [situation]. Add a temporary Studio-only monitor that prints instance counts per folder, connection counts in our modules and Lua heap every 30 s during [N] cycles of [action]. Find what grows, show the numbers, then propose the fix (Trove cleanup, cached AnimationTracks, removed listeners). Remove the monitor afterwards.
```

### Works in Studio, broken live
```text
[Feature] works in Studio but not on the live server. Live symptom: [what players see / Error Report text]. List the differences that could explain it (asset ownership and permissions, analytics only in published games, DataStore names, test purchases, timing on slow phones, streaming) and the quickest way to check each. Rank them by likelihood for this symptom.
```

### Explain it to me
```text
Explain how [script/system] works so I can debug it myself next time: the flow from player input to server to client, every remote it uses, where its data lives, and the 2–3 places most likely to break. Plain language, under a page. Point to file:line for each step.
```

## How to check the result
- A failing reproduction before the fix and a passing run after, both quoted.
- Code gate PASS; DevTest scripts deleted; `git status` clean.
- For phone issues: Holden's re-test on the phone, not a Studio screenshot.

## Pitfalls
- **"Fix the bug" with no steps** makes Claude guess and often fix the wrong thing (Anthropic before/after examples).
- **Correcting the same mistake repeatedly** in one session fills it with failed attempts; clear and restate (Anthropic).
- **Play Here spawns at the editor camera:** a camera left off the map looks like a spawn bug ([[Sky Island Hub and Throw Lane]]).
- **ProfileStore needs about 8 s** after restoring a test save before stopping play, or it never writes ([[Roblox Studio MCP Quirks]]).
- **Rojo-synced script changes need a play restart** before they take effect.
- **"Fixed" in Studio ≠ fixed on a live server:** purchases, analytics and some asset permissions only behave for real in a published place ([[ProcessReceipt-Handling]], [[Analytics-And-Instrumentation]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Gameplay-Systems]] · [[Prompting-UI]] · [[Roblox Studio MCP Quirks]]

## Sources
- Anthropic, Claude Code best practices (verification, symptom prompts, adversarial review, two-corrections rule): <https://code.claude.com/docs/en/best-practices>
- BloxBot (vendor), bounded Roblox AI tasks from OpenGameEval: <https://www.bloxbot.ai/guide/opengameeval-fable-5-bounded-tasks>
- Local: [[2026-10-03 Paper Plane Toss Phone Playtest]], [[Roblox Studio MCP Quirks]], [[Fish a Monster Pre-Publish Review]], [[Rubber-Tower-Map-v3-Critique]].
