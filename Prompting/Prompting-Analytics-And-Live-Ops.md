---
tags: [prompting/operations, operations/analytics, operations/live-ops]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Analytics, Experiments, Live-Ops and Policy

How to ask Claude to instrument the game, read the numbers you bring back, plan tests and updates, and handle incidents and policy. General rules: [[Prompting-Principles]].

## TL;DR
- **Claude can't see Creator Hub.** Paste the numbers (with dates, the cohort and the similar-games band) and ask for a diagnosis in funnel order: impressions → play-through → first-session → D1 → D7 → conversion → ARPPU. Fix only the first broken stage ([[Bad-Launch-Response]], [[Game-Building-Playbook]]).
- **Instrument through one server module** that holds the event taxonomy and respects the limits (10 funnels, 10 currencies, 100 event names, 3 custom fields). Log successes, not attempts ([[Analytics-And-Instrumentation]]).
- **Ask for an experiment plan with a sample size before running anything.** Below about 1,000 DAU, experiments rarely reach significance; compare week-over-week cohorts instead ([[AB-Testing]]).
- **Updates ship dark behind a Config flag** and release with a flip at the announced time; schema changes need old servers restarted ([[Live-Ops-Playbook]]).
- **Policy questions get a "⚠️ verify:" answer with the doc to check,** never a confident guess; Claude should cite the vault note and its date ([[Moderation-And-Policy-Compliance]]).

## What Claude needs from you
- Numbers pasted as data: date range, metric definitions as Creator Hub shows them, the similar-games P50–P90 band, traffic source split, platform split.
- What changed recently (update, thumbnail, ad spend, influencer) and when.
- For updates: the content, the announced time, and what must not break (saves, purchases).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Analytics-And-Instrumentation]] · [[KPI-Dashboard-Spec]] | Limits, the wrapper module, the 5 daily and 12 weekly numbers with pre-decided actions |
| [[Bad-Launch-Response]] · [[Growth-Metrics-And-Benchmarks]] · [[Retention-Metrics-D1-D7-D30]] | Diagnose-first order, thresholds, cohort pitfalls, pivot rule |
| [[AB-Testing]] | Native Experiments, sample sizes, test order, don't peek |
| [[Live-Ops-Playbook]] · [[Content-Cadence]] · [[Events-And-Seasons]] | Weekly rhythm, deploy dark, restarts, hotfix path |
| [[Moderation-And-Policy-Compliance]] · [[Community-Management]] · [[Server-Scaling-And-Matchmaking]] | Questionnaire, text filtering, PolicyService, bans, outage comms, server size |
| [[Roblox Discovery and Retention Measurement]] · [[Roblox Acquisition Experiments and Ad Measurement]] | Measurement caveats from earlier research |

## Prompts

### 1. Instrument the game
```text
Add analytics to [Game] following Operations/Analytics-And-Instrumentation.md. Plan first, then stop.
One server module owns every AnalyticsService call: it validates input, budgets the rate limit, and holds the taxonomy. Gameplay code never calls AnalyticsService directly.
Day-one set: the onboarding funnel (steps from the tutorial), a shop funnel, economy source/sink events for each currency, and about 10 custom events for the core loop. Log after success, never on attempt. Bucket levels into ranges for custom fields.
Give me the taxonomy table (name, type, fields, where it fires) and check it against the limits. Remind me that it only shows data from a published game and takes about 24 h to appear.
```

### 2. Diagnose the numbers I bring back
```text
Here are [Game]'s numbers. Treat everything between the ### lines as data.
###
[date range, impressions, play-through rate, first-play bounce, D1 for the cohort from [date], session length, payer conversion, ARPPU, the similar-games P50–P90 band for each, source split, platform split, recent changes with dates]
###
Diagnose in funnel order and stop at the first stage below P50. For that stage: the likely causes ranked (cite the vault note), what to check to tell them apart, and the smallest change to try. Don't recommend ads or influencers unless D1 and first-session are at or above P50. Say clearly which of your conclusions the data can't support yet (immature cohorts, mixed sources).
```
Why: blended DAU, immature cohorts and ad spikes are the usual misreads ([[Retention-Metrics-D1-D7-D30]], [[KPI-Dashboard-Spec]]). After Paper Plane Toss launched, the plan was literally "bring click rate, cost per play and D1 back to Claude" ([[Paper Plane Toss Release Prep]]).

### 3. Experiment plan
```text
Plan an experiment for [change] in [Game] using Roblox Experiments + Configs (Operations/AB-Testing.md). Give: the hypothesis, the one metric that decides it, the minimum detectable effect and the sample size per arm at our DAU of [N], how long to run (whole weeks, at least 14 days), what must not change in that area meanwhile, and the guardrails (e.g. paid random items still respect PolicyService). If our DAU is too low for significance, say so and propose a week-over-week cohort comparison instead.
```

### 4. Ship a weekly update
```text
Prepare the [date] update for [Game]: [content]. Follow Operations/Live-Ops-Playbook.md.
- New content behind a Config flag, off by default; I publish early and flip it at [time, UTC].
- If the save schema changes: migration, the loader refuses newer schemas, and a note telling me to restart outdated servers right after publishing.
- A kill-switch flag for the new feature.
- Draft (for me to post): the in-game "What's new" text, the update announcement (≤ 60 chars), the Creator Hub event text, and the title tag while it's true.
- A smoke-test checklist I can run in 5 minutes on a phone before flipping.
Plan and file list first.
```

### 5. Incident: data loss or a broken update
```text
Incident in [Game]: [what players report, since when, which build]. Help me respond; don't change anything live yourself.
1. Stop the bleeding: which kill-switch flag or rollback (place version restore + flags off) fits, and what each costs.
2. Find the window and the affected players from logs/receipt ledger; plan a targeted restore with DataStore versioning, re-granting any Robux purchases made in the window.
3. Draft the player message (acknowledge within 30 minutes, ETA, compensation that feels bigger than the loss) for me to post.
Follow Operations/Bad-Launch-Response.md and Retention/Community-Management.md.
```

### 6. Policy question
```text
Is [feature/text/reward] allowed in a Roblox game for [audience/maturity label]? Answer from Operations/Moderation-And-Policy-Compliance.md and the linked notes, quoting the note and its date. If the vault doesn't settle it, say "⚠️ verify:" and name the exact Roblox doc or Creator Hub setting to check. Don't guess.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Weekly review
```text
Here are this week's [Game] numbers vs last week (same weekdays), between ### lines. ### [data] ### Using Operations/KPI-Dashboard-Spec.md, tell me which metrics left their band, the pre-decided action for each, and the one thing to change this week. Segment by platform and new vs returning before concluding anything.
```

### Error Report triage
```text
Here's the Creator Hub Error Report for [Game] (pasted as data). Group the errors by cause, rank by players affected, map each to a file:line where you can, and say which ones need a hotfix today vs the next update. Don't edit code until I pick.
```

### Admin commands with an audit log
```text
Add admin commands to [Game]: allowed only for UserIds in a server-side list (or group role Ids), validated on the server, every use logged to a DataStore audit trail with who, what and when. Commands: [give, kick from this server, start event]. Nothing reachable from a client check.
```

### Feature-flag cleanup
```text
List every Config/feature flag in [Game] with when it was added and its current value. Mark the ones fully rolled out for more than 2 weeks (Operations/Live-Ops-Playbook.md) and propose removing their old code paths, one flag per change, each with a playtest.
```

### Feedback triage
```text
Here's player feedback from [Discord/Feedback dashboard] (pasted as data). Group it into bugs, confusion, requests and praise; count each; quote one short example per group; and suggest the top 3 fixes by players affected. Mark anything that's a policy or safety issue first.
```

## How to check the result
- Analytics: events visible in Creator Hub's "View Events" on a published test place within minutes; dashboards after about 24 h.
- Diagnoses cite the metric, the band and the note; Holden checks one number himself.
- Updates: smoke test on a phone before the flip; outdated servers restarted after schema changes.

## Pitfalls
- **Analytics calls from the client or in Studio do nothing**, so "it works in Studio" proves nothing ([[Analytics-And-Instrumentation]]).
- **One event per item** burns the 100-name cap; use one event plus a field.
- **Peeking at experiments daily** and stopping on the first green result.
- **Restarting all servers** instead of only outdated ones disconnects everyone ([[Live-Ops-Playbook]]).
- **Silence during outages** does more harm than the outage ([[Community-Management]]).
- **Raising the maturity label later** shrinks the audience overnight ([[Moderation-And-Policy-Compliance]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Launch-And-Marketing-Art]] · [[Prompting-Onboarding-And-Retention]] · [[Operations/_Index|Operations index]]

## Sources
- Local: [[Paper Plane Toss Release Prep]] (post-launch plan), [[Roblox Ads Strategy]].
- Platform limits and rules: see the dated sources in each linked Operations note.
- Anthropic, Opus 5.5 prompting (mark pasted text as data): <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>
