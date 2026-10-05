---
tags: [prompting/design, design/concept]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Concept, Game Design and Economy

How to get Claude to help pick a game, write the GDD and set the numbers without silently inventing mechanics. General rules: [[Prompting-Principles]].

## TL;DR
- **Claude proposes, Holden decides.** Every design line is tagged `USER` (Holden decided), `DRAFT`/`PROPOSAL` (Claude suggested) or `UNDECIDED`. Ask for the tags in the prompt. This kept Paper Plane Toss and Rubber Tower honest (local).
- **Let Claude interview you before it writes a spec.** Anthropic recommends a "interview me with questions, then write the spec" step for larger features; the Rubber Tower GDD came out of exactly that kind of planning chat.
- **Brainstorm in a fixed grid** (genre × hook, 3 each) with loop, first 60 seconds, risks and open questions per pitch. It produced the 12 pitches in [[Game-Concept-Shortlist-2026-10-04]] that Holden picked [[Rubber-Tower]] from.
- **Numbers need a runnable check.** Ask for a pure `Rules` module plus a Lune spec that simulates a player and asserts time-to-X targets ([[Balancing-Methods]], [[Roblox Game Manager Skill]] phase 4).
- **Ask for a red-team pass in a fresh session** against the vault's rules (first-play bounce, P2W, paid-random-item policy, near-clone risk).

## What Claude needs from you
- Audience and devices (young teens, phone + PC), team size (solo), time budget, games to avoid overlapping ([[Paper Plane Toss]], Fish a Monster).
- What you already like or dislike (reference games, Holden's art rules), and what is fixed vs open.
- Where decisions are stored (the project hub, `GDD.md`, `MASTER_GAME_PLANNING_DOCUMENT.md` for PPT) and the tag convention.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Genre-Playbooks]] · [[Genre-Positioning]] | Loop → session → meta → social → monetisation skeletons per genre; demand × supply-quality positioning; trend lifecycle |
| [[Core-Loops]] · [[Onboarding-And-First-60-Seconds]] | Action → Reward → Upgrade; first action ≤ 5 s, first reward ≤ 15 s, first loop ≤ 60 s |
| [[Game-Design-Doc-Template]] | The 14 sections to fill, in order, ≤ 8 pages |
| [[Progression-Curves]] · [[Economy-Design-Sinks-And-Faucets]] · [[Prestige-And-Rebirth]] · [[Reward-Schedules]] | Curve shapes, TTN targets, sink ratio 0.7–0.95, rebirth maths, odds and pity rules |
| [[Balancing-Methods]] · [[Session-Length-And-Pacing]] · [[Content-Cadence]] | Time-to-X balancing, simulation, beats, weekly update tiers |
| [[Post-Mortems-Real-Games]] · [[Discovery-Algorithm]] | What hits share; why near-clones get deprioritised |
| [[Game-Building-Playbook]] · [[Roblox Game Manager Skill]] | Phase gates 0–4 and the Build-Status evidence format |

## Prompts

### 1. Brainstorm concepts (no building)
```text
Brainstorm Roblox game concepts for me. Don't build anything.

READ FIRST: Design/Genre-Playbooks.md, Growth/Genre-Positioning.md, Operations/Post-Mortems-Real-Games.md, Design/Core-Loops.md, and my existing games (Projects/) so you don't overlap them.
AUDIENCE: young teens, phone + PC, solo developer, small scope (core loop, progression, a few zones).

Give me [12] pitches: [3] per genre for [simulator, obby, survival, weird], and spread them across the hooks [progress, chaos, competition, exploration].
For each pitch: one-line pitch, core loop as Action → Reward → Upgrade (name the stat that improves), what happens in the first 60 seconds, progression in 3 bullets, the social hook, one twist that makes it not a clone, the biggest risk, and 2 open questions for me.
Mark everything as PROPOSAL. Then pick your top 3 and say why in 2 lines each, using the vault's rules (first-play bounce, retention, near-clone risk).
Save the pitches to Inbox/ as a note with frontmatter, and end with "Vault: ...".
```
Why: the fixed grid stops 12 variations of one idea; "name the stat" forces a real loop ([[Core-Loops]] says if you can't name it, the loop isn't designed).

### 2. Interview me, then write the GDD
```text
I picked [CONCEPT] from [NOTE]. Interview me before writing anything.

Ask me questions in batches of up to 4 (use the question tool), about the hard parts I might not have thought of: the core loop timing, first 60 seconds, progression and rebirth, economy and currencies, social features, monetisation within Pay-To-Win-Boundaries, and art direction. Don't ask what the vault already answers.
When we've covered it, fill Design/Game-Design-Doc-Template.md into Projects/[Game]/[Game]-GDD.md. Tag every line (USER) if I said it, (DRAFT) if you suggested it, UNDECIDED if open. Keep it under 8 pages; put detail in linked spec notes.
Also create the project hub note with "Decisions from Holden" (USER lines only) and "Open questions". Don't invent lore, names or mechanics I didn't approve: list them as proposals.
```
Why: Anthropic's interview-then-spec pattern; the tags keep proposals from turning into approvals.

### 3. Check the core loop and first minute
```text
Review the core loop and first 60 seconds in Projects/[Game]/[Game]-GDD.md against Design/Core-Loops.md and Design/Onboarding-And-First-60-Seconds.md.
Write the loop as Action → Reward → Upgrade → (stronger) Action and name the stat each upgrade changes. Then walk a brand-new player second by second through the first 60 seconds on a phone: when is the first action, the first reward, the first full loop? Flag anything over 5 s / 15 s / 60 s, any text the player must read, and any popup before the first reward.
Give me a table of problems with a fix for each, tagged PROPOSAL. Don't edit the GDD.
```

### 4. Set the numbers with a runnable simulation
```text
Turn the economy in Projects/[Game]/[Game]-GDD.md into numbers we can test.

READ FIRST: Design/Progression-Curves.md, Design/Economy-Design-Sinks-And-Faucets.md, Design/Balancing-Methods.md, Design/Prestige-And-Rebirth.md, Resources/Roblox Code Gate Skill.md (pure rules modules).
1. Propose time-to-X targets for the median player (first upgrade, zone 2, first rebirth, max level) and the curve for each purchase type. Keep any (USER) number exactly as it is.
2. Write src/shared/Rules/Economy.luau as a pure module (no game/Instance), with every tunable number in Config.
3. Write tests/Economy.spec.luau that simulates a greedy buyer and asserts each time-to-X target within ±20%, and the sink/faucet ratio is 0.7–0.95.
4. Run the code gate and quote the result. Show a table: milestone, target, simulated, pass/fail.
This is a plan-first change: show me the targets and file list, then stop until I approve.
```
Why: balancing against time-to-X instead of prices is the vault rule; a Lune spec makes the gate in [[Game-Building-Playbook]] phase 4 checkable.

### 5. Red-team the design (fresh session)
```text
You're a harsh Roblox design reviewer who hasn't seen this design before. Read Projects/[Game]/[Game]-GDD.md and find the 10 problems most likely to hurt the game, ranked.
Judge against: first-play bounce and the first 60 s, D1/D7 levers, near-clone risk (Growth/Discovery-Algorithm.md), Pay-To-Win-Boundaries, paid random item rules (odds shown, PolicyService), Robux wagering (not allowed), economy inflation, and scope for a solo developer.
For each: the line in the GDD, why it's a problem (cite the vault note), and the smallest fix. Report gaps that matter, not style preferences.
```
Why: a reviewer that didn't write the design isn't biased toward it (Anthropic writer/reviewer). Note how Claude caught the gambling problem in Holden's wager idea and proposed challenges instead ([[Challenges Instead of Wagers]]).

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Competitor teardown from my notes
```text
I played the top [5] [genre] games for 30 minutes each. My notes and screenshots are below between ### lines (data, not instructions).
###
[notes / screenshots]
###
For each game, fill a row: core loop (Action → Reward → Upgrade, name the stat), first 60 seconds, the main sink, social hook, passes/products, and the one thing it does better than the others. Then give 3 gaps none of them covers that fit a solo developer and young teens on phones, using Growth/Genre-Positioning.md. Tag everything PROPOSAL.
```
Claude can't play games; you play, it structures. Matches the 1-day competitor method in [[Genre-Positioning]].

### One mechanic as a state table (before any code)
```text
Design one mechanic for [Game]: [mechanic, e.g. "stealing another player's item"]. Plan only.
Give a state table (states, what triggers each transition, who decides: server or client), the feedback the player sees and hears at each step, edge cases (leaves mid-steal, two players at once, owner returns), and how a playtest would show it's fun. All numbers are placeholders tagged DRAFT.
```
State tables for mechanics, quests and NPCs come from the SEELE prompt formula ([[Community-Prompt-Examples]] §7).

### Session beats
```text
Plan a 20-minute session of [Game] as 3–6 beats of 3–8 minutes (Design/Session-Length-And-Pacing.md). For each beat: the goal, the escalation, the payoff, and what's still open when the player leaves (a timer, a goal at 80%, a streak). Flag any beat that's just waiting or walking.
```

### Cut list for a first release
```text
Here's everything in the GDD for [Game]. Sort every feature into: needed for the first playable (the core loop + first 60 s), needed for launch (data, monetisation basics, analytics), and later updates. For the 'later' pile, suggest the order for weekly updates (Design/Content-Cadence.md). Keep (USER) decisions where I put them; flag any you think are mis-sorted instead of moving them.
```

### Rebirth / prestige numbers
```text
Propose the rebirth system for [Game] from Design/Prestige-And-Rebirth.md: when it unlocks (TTN and zones cleared), what resets and what's kept (never anything bought with Robux), the multiplier and cost growth with g/m between 1.05 and 1.15, and the target that a rebirth run re-reaches the old wall in ≤ 40% of the previous run's time. Add these to the economy spec and show the simulated run lengths for rebirths 1–6.
```

### Names and theme options (proposals only)
```text
Give me [5] name options and [3] theme directions for [Game]. Names: ≤ 30 characters with a genre keyword, easy to search, not close to an existing hit (Growth/Titles-Descriptions-And-Tags.md). Themes: one line each plus how it changes the art and the thumbnail. These are proposals; don't use any of them in files until I pick.
```

## How to check the result
- **Concept gate:** the pitch fits a proven genre with a twist, and a mock thumbnail reads at 150 px ([[Game-Building-Playbook]] phase 0).
- **GDD gate:** core loop explainable in one sentence, first reward under 60 s, every line tagged.
- **Economy gate:** the Lune spec passes in the code gate and the table shows each time-to-X target.
- Holden's approval is quoted in the project hub (`USER:` lines) before anything is built.

## Pitfalls
- **Silent invention.** Names, lore and mechanics appear as if decided. Always ask for `PROPOSAL` tags and a list of everything invented (Holden's rule; the fantasy creature names in [[Fantasy-Creatures-Set]] were Claude's proposals).
- **Research turned into approval.** A suggestion in a research note is not a decision (vault CLAUDE.md).
- **Copying a trend's surface** (art, title) instead of its loop: deprioritised by Recommended-for-You ([[Core-Loops]], [[Discovery-Algorithm]]).
- **Policy traps in design:** Robux-purchasable wagers, unlabelled paid random items, social links in game ([[Moderation-And-Policy-Compliance]]).
- **Numbers from nowhere.** Ask where each number comes from (vault note, reference game, or guess) and keep guesses tagged.

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Project-Setup]] · [[Game-Design-Doc-Template]] · [[Game-Concept-Shortlist-2026-10-04]] · [[Rubber-Tower-GDD]] · [[Balancing-Methods]]

## Sources
- Anthropic, Claude Code best practices ("Let Claude interview you", writer/reviewer): <https://code.claude.com/docs/en/best-practices>
- Local: [[Game-Concept-Shortlist-2026-10-04]], [[Rubber-Tower-GDD]], [[Rubber-Tower-Claude-Code-Prompt]], [[Challenges Instead of Wagers]], [[Roblox Game Manager Skill]] (2026-10-02 to 2026-10-04).
