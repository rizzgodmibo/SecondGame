---
tags: [prompting/retention, design/onboarding, retention/systems]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Onboarding, Tutorials and Retention Systems

How to ask Claude for the first-session experience and the systems that bring players back. General rules: [[Prompting-Principles]].

## TL;DR
- **Lead every retention prompt with the order of the windows:** fix the first 60 seconds and D1 before dailies, events or seasons ([[Retention-Checklist]], [[Discovery-Algorithm]]). Ask Claude to say which window a feature serves.
- **Tutorials teach by doing.** No menus, chunky ground arrows, a bobbing hand, steps tracked and saved on the server. That's the Steal an Egg pattern Holden picked and Claude built for Paper Plane Toss from frames of a reference video ([[Join Cutscene and Tutorial]]).
- **Everything time-based is server-decided:** day index from `os.time()`, never client time; one UTC reset ([[Daily-Rewards-And-Streaks]]).
- **Name the anti-patterns:** popups before the first reward, login-only rewards that raise D1 but cut playtime, hard streak resets, invite prompts on spawn, rewards for unverifiable likes ([[Onboarding-And-First-60-Seconds]], [[Sharing-And-Referral-Loops]]).
- **Instrument as you build:** onboarding funnel steps logged from the server so the leak can be found later ([[Analytics-And-Instrumentation]]).

## What Claude needs from you
- The core loop and the exact first action/reward you want, plus a reference game's tutorial (a video helps; Claude can extract frames).
- Which retention features are approved and their reward sizes, or "propose sizes and stop".
- The audience constraints (under-13s get fewer notification types; Discord isn't where most players are).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Onboarding-And-First-60-Seconds]] · [[Core-Loops]] | ≤ 5 s / 15 s / 60 s timings, one-button first action, contextual and timed hints |
| [[Retention-Checklist]] · [[Retention-Metrics-D1-D7-D30]] | What to build per window; D1 ≥ 15% working target; segment by source |
| [[Daily-Rewards-And-Streaks]] · [[Events-And-Seasons]] · [[Leaderboards]] | Server day index, hybrid calendar + streak, freezes; Configs for schedules; weekly boards |
| [[Friend-And-Group-Play]] · [[Sharing-And-Referral-Loops]] · [[Notifications-And-Re-Engagement]] | Friend boost caps, `ReferredByPlayerId`, share links, 1 notification/user/day |
| [[Join Cutscene and Tutorial]] · [[Idle-And-Offline-Earning]] | A built tutorial and cutscene; offline income rules |

## Prompts

### 1. First-session flow
```text
Design the first 3 minutes of [Game] for a brand-new player on a phone. Plan only.
READ FIRST: Design/Onboarding-And-First-60-Seconds.md, Design/Core-Loops.md, the GDD, and [reference tutorial video/frames].
Write it as a second-by-second script: spawn, first action (one obvious input that works on touch, mouse and controller), first reward with feedback, first full loop (earn → spend → see the effect), then the first goal. No menus, popups, daily rewards or shop offers before the first reward.
For each step: what teaches it (arrow, glow, hand, world sign; no reading needed), when a hint appears if the player is stuck, and the analytics funnel step name.
Flag anything over the 5 s / 15 s / 60 s targets. Tag new mechanics as PROPOSAL.
```

### 2. Build the tutorial
```text
Build the approved tutorial steps for [Game]: [steps].
- Steps are tracked and saved on the server (tutorialStep in the profile, schema bump + migration); the client only shows guides.
- One reusable Guide module for ground arrows and the pointing hand, so later hints reuse it.
- Log each step with AnalyticsService:LogOnboardingFunnelStepEvent from the server (it only works in published games).
- Pause anything that would interfere (e.g. auto features) until the tutorial ends.
DONE WHEN: a fresh save runs every step in a Studio playtest with Output lines per step, a rejoin mid-tutorial resumes at the right step, and the code gate passes. Show screenshots of each step on a phone-sized viewport.
```
Why: Paper Plane Toss's tutorial used exactly this structure (server-tracked steps, a reusable `client/Guide`, Auto Throw paused) ([[Join Cutscene and Tutorial]]).

### 3. Daily rewards and streaks
```text
Add daily rewards to [Game] following Retention/Daily-Rewards-And-Streaks.md.
Server decides everything: day index = floor((os.time() - resetOffset) / 86400) with one UTC reset; store LastClaimDay, Streak, CalendarIndex, Freezes in the profile. A forgiving 7-day calendar plus a separate streak; one freeze per completed week (cap 2); soft reset (halve) instead of zero.
Reward sizes: propose them at about 10–25% of a typical session's earnings, day 7 worth 3–5× day 1, tagged DRAFT.
Show the claim popup only after onboarding is complete, with a "come back in HH:MM" countdown.
Test with a DevTest script that fakes the day index (never the device clock): claim, same-day re-claim (rejected), next day, a 2-day gap with and without a freeze. Quote PASS/FAIL lines.
```

### 4. Social and invite features
```text
Add [friend boost / invite rewards / group reward] to [Game]. READ FIRST: Retention/Friend-And-Group-Play.md and Retention/Sharing-And-Referral-Loops.md.
Rules: friendship and group checks on the server with the …Async APIs (cached); friend boost capped [+30–50%]; invite rewards use ReferredByPlayerId, pay the inviter only for a real new player who stays [5 min], one reward per invitee, a daily cap; ask to invite at a peak-joy moment, never on spawn; no rewards for likes or favourites (they can't be verified).
List the exploit cases (alts, rejoin farming) and how each is limited.
```

### 5. A timed event
```text
Plan a [weekend 2× / admin event / limited egg] event for [Game]. Schedule it from data: UTC timestamps in Experience Configs with a hardcoded fallback, every server computing "active?" from os.time(). Real deadlines only (no fake countdowns). Event currency converts or expires at the end. Include the Creator Hub event listing and the notification copy as text for me to enter (I post it). Give the plan and file list, then stop.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Codes
```text
Add a codes system to [Game]: codes live in Config (or Experience Configs so I can add them without publishing), each with a reward, an expiry date and a redeem-once flag saved in the profile; input validated and rate-limited on the server; friendly messages for invalid, expired and already used. Rewards are capped so codes can't break the economy.
```

### Daily and weekly quests
```text
Add [3] daily and [3] weekly quests to [Game], picked from a pool in Config, reset on the server's UTC day/week index, progress counted from real server events, rewards sized as a pull back into the core loop (not a replacement for playing). Show the pool and the reward sizes tagged DRAFT.
```

### Welcome back panel
```text
When a returning player joins [Game], show one "Welcome back! You earned [X] while away" panel after the world loads (never stacked with other popups), using the offline income computed on the server at load (Design/Idle-And-Offline-Earning.md: cap [4 h], 25–50% efficiency, minimum 60 s away). A claim animation, and an optional 2× claim only if I approve a product for it.
```

### What's new panel
```text
Add a "What's new" panel to [Game]: shown once on the first join after each version (LastSeenVersion in the profile), 3–5 short lines with icons, a "Go" button that teleports to the new thing, and never in a brand-new player's first session. The text lives in Config so each update only edits data.
```

### Friend leaderboard
```text
Add a friends leaderboard next to the global one in [Game]: the player's own rank with context ("You: #4,213, 1,200 to #4,000") on the global board, and a board of friends in the server plus friends' saved best scores. Global writes throttled (every ~120 s if changed); reads cached per server (Retention/Leaderboards.md).
```

## How to check the result
- A fresh-save playtest of the first 3 minutes at phone size, with timestamps for first action, first reward and first loop.
- DevTest PASS lines for every time-based edge case (faked day index, not device clock).
- After release: onboarding funnel and D1 in Creator Hub, compared with the similar-games P50 band ([[KPI-Dashboard-Spec]]).

## Pitfalls
- **Building D30 systems to fix a D1 problem** ([[Retention-Checklist]]).
- **Popup avalanche on join** (daily + offline + update + offer) reads as an ad; players leave ([[Onboarding-And-First-60-Seconds]]).
- **`tick()` or client timestamps** for days and offline income are exploitable ([[Daily-Rewards-And-Streaks]], [[Idle-And-Offline-Earning]]).
- **New profiles starting with `lastSeen = 0`** granted a full offline cap in Fish a Monster ([[Fish a Monster Saving and Offline Income]]).
- **Social links or Discord invites in game text** break Community Standards ([[Community-Management]]).
- **Cutscene camera paths** must be checked against real map geometry (Paper Plane Toss flew through a statue for 4.5 s of white screen) ([[2026-10-03 Paper Plane Toss Phone Playtest]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Concept-And-Design]] · [[Prompting-Analytics-And-Live-Ops]] · [[Retention/_Index|Retention index]]

## Sources
- Local: [[Join Cutscene and Tutorial]], [[2026-10-03 Paper Plane Toss Phone Playtest]], [[Fish a Monster Saving and Offline Income]].
- Platform rules: see the dated sources in each linked Retention and Design note.
