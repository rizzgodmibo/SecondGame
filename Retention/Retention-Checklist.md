---
tags: [retention/checklist]
status: draft
updated: 2026-10-04
confidence: medium
---
# Retention Checklist

## TL;DR
- Work through this list **in order of the retention window**: D0/D1 (first session), D7 (habit + progression), D30 (social + endgame + live ops). Do not build D30 systems before D1 is at your similar-games p50 ([[Retention-Metrics-D1-D7-D30]]).
- Every item links to the note with the code or decision rules. Copy this into `Projects/<name>/` and tick it per game.
- Pre-launch minimum: the D1 block, daily rewards, invite prompt + referral, group reward, leaderstats, opt-in prompt, analytics funnels.

## Gate 0: Measurement (before launch)
- [ ] Onboarding funnel (`LogOnboardingFunnelStepEvent`) and progression events instrumented ([[Analytics-And-Instrumentation]])
- [ ] Custom events for: daily claim, invite prompt shown, referral join, notification rejoin (launchData category), event participation
- [ ] Similar-games benchmark band recorded once ≥ 100 DAU (D1/D7/D30 p50 and p90, date)
- [ ] Every release annotated with date + version for cohort reading

## Gate 1: D1 (first session → next day)
- [ ] First core loop completed within 60 s. Fun within 5 min ([[Onboarding-And-First-60-Seconds]], [[Core-Loops]])
- [ ] Session goal visible (next zone/egg/rebirth) and achievable in the first session
- [ ] Performance pass on low-end phones. Crash rate checked per release.
- [ ] "Come back tomorrow" hook shown at session end: day-2 reward preview, timer running (egg/crop), countdown ([[Daily-Rewards-And-Streaks]])
- [ ] Notification opt-in prompted in a high-intent context, never gating ([[Notifications-And-Re-Engagement]])

## Gate 2: D7 (habit + progression)
- [ ] Daily login calendar (7-slot) + streak tiers + freezes/soft reset. Server-side UTC day index.
- [ ] Daily quests (3/day) that route through the core loop. Weekly challenge.
- [ ] Progression has no cliff. Level distribution checked weekly.
- [ ] Offline/async timers that end in personalised notifications (1/day max)
- [ ] Friend boost / co-op objective. Invite prompt at peak moments ([[Friend-And-Group-Play]], [[Sharing-And-Referral-Loops]])
- [ ] Referral rewards via `ReferredByPlayerId` with anti-abuse caps. Referral banner published.
- [ ] Group (Community) membership reward via `IsInGroupAsync`

## Gate 3: D30 (endgame + social + live ops)
- [ ] Weekly global leaderboard with rewards, own-rank display, friend board ([[Leaderboards]])
- [ ] Endgame: rebirth/prestige, collection index, trading or guilds ([[Core-Loops]])
- [ ] Update cadence: small update every 2–4 weeks, major every 2–3 months ([[Content-Cadence]], [[Live-Ops-Playbook]])
- [ ] Weekly beat: weekend boost or admin event at a fixed time. Events registered in Creator Hub for RSVPs ([[Events-And-Seasons]])
- [ ] Season/battle pass once there are ≥ 8 weeks of content planned
- [ ] Private servers enabled + owner perks

## Gate 4: Community and ops
- [ ] Community + Discord + social links (16+ verified owner). No links in-game ([[Community-Management]]).
- [ ] What's New panel, feedback button, weekly triage
- [ ] Outage template, compensation mechanism, Configs kill-switches
- [ ] Mod tools rank-gated. Ban logging.

## Weekly review (30 min)
- [ ] D1/D7/D30 vs benchmark band, by acquisition source and platform
- [ ] Cohort table: did last week's update move the new cohort?
- [ ] Notification analytics: click rate per category. Kill the worst category.
- [ ] Referral funnel: referral joins → qualified
- [ ] Feedback upvote % trend + top 5 complaints
- [ ] Next 2 weeks of events/updates scheduled in Configs

## Pitfalls
- Building events/seasons to fix a D1 problem. They don't work if the first session isn't fun.
- Shipping many retention systems in one update, which leaves no attribution.
- Optimising D1 with login bribes while playtime per user falls.

## Related
- [[Retention/_Index]] · [[Retention-Metrics-D1-D7-D30]] · [[Daily-Rewards-And-Streaks]] · [[Events-And-Seasons]] · [[Friend-And-Group-Play]] · [[Leaderboards]] · [[Sharing-And-Referral-Loops]] · [[Notifications-And-Re-Engagement]] · [[Community-Management]] · [[Onboarding-And-First-60-Seconds]] · [[Core-Loops]] · [[Discovery-Algorithm]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Content-Cadence]]

## Sources
- Compiled from the linked notes. Primary sources: Roblox Creator Docs "Retention", "Analytics dashboard", "Discovery", "Experience notifications", "Player invite prompts", "Friend referral system" (accessed 2026-10-04 via creator-docs mirror commit 2026-10-02).
