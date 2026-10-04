---
tags: [retention/index]
status: draft
updated: 2026-10-04
confidence: medium
---
# Retention: Index

## TL;DR
- This folder covers **bringing players back**: D1/D7/D30 metrics, dailies and streaks, events and seasons, social and friend play, leaderboards, invites and referrals, notifications, and community.
- Start with [[Retention-Metrics-D1-D7-D30]] to diagnose, then use [[Retention-Checklist]] to decide what to build next.
- The first session and onboarding live in Design, see [[Onboarding-And-First-60-Seconds]]. Loop design is in [[Core-Loops]]. Ranking effects are in [[Discovery-Algorithm]].
- All code is `--!strict` Luau and server-authoritative. Persistent fields go into the profile described in [[Data-Persistence-DataStores-And-ProfileStore]].

## Notes
| Note | Use it when |
|---|---|
| [[Retention-Metrics-D1-D7-D30]] | Reading the dashboard, benchmarks, diagnosing a drop |
| [[Daily-Rewards-And-Streaks]] | Building login calendars, streaks, playtime gifts (code) |
| [[Events-And-Seasons]] | Planning limited-time events, admin abuse, global events, battle passes (code) |
| [[Friend-And-Group-Play]] | Friend boosts, parties, group rewards, private servers (code) |
| [[Leaderboards]] | leaderstats, OrderedDataStore weekly boards, MemoryStore real-time boards, anti-cheat (code) |
| [[Sharing-And-Referral-Loops]] | Invite prompts, referral rewards, share links, launch data (code) |
| [[Notifications-And-Re-Engagement]] | Experience notifications, opt-in prompts, offline timer queue (code) |
| [[Community-Management]] | Discord/Community, update logs, feedback, moderation, outages |
| [[Retention-Checklist]] | Gate-by-gate build list + weekly review |

## Cross-folder links
- [[Onboarding-And-First-60-Seconds]] · [[Core-Loops]] · [[Discovery-Algorithm]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Content-Cadence]] · [[Home]]

## Open questions / gaps (⚠️ verify)
- GameAnalytics 2025/2026 Roblox benchmark figures come from search snippets. Fetch the full report when network access allows.
- Analytics day boundary timezone for D1 (assumed UTC).
- Server-side `IsInGroupAsync` cache behaviour after a client-side `PromptJoinAsync` join.
- Whether `GetRangeAsync` accepts a `sortKey`-only bound table.
- Open Cloud API key scope name for user notifications.
- Whether favourites/follows still trigger update notifications separately from the notification opt-in.

## Sources
- See each note. Primary: Roblox Creator Docs (github.com/Roblox/creator-docs mirror, commit 2026-10-02), accessed 2026-10-04.
