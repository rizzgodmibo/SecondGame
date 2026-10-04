---
title: Roblox Discovery and Retention Measurement
date: 2026-10-03
updated: 2026-10-03
verified: 2026-10-03
review_after: 2026-11-02
tags: [roblox, discovery, retention, analytics]
source: Roblox Creator Hub and labelled synthesis
project: null
status: sourced-not-locally-tested
---
# Roblox Discovery and Retention Measurement

Related: [[Roblox Development Playbook]], [[Roblox Vault Coverage and Maintenance]], [[Paper Plane Toss Thumbnails and Game Icon]], [[Join Cutscene and Tutorial]].

## Verified discovery facts

Roblox describes retrieval followed by personalised ranking. Other acquisition sources can help a game enter consideration; ranking evaluates users acquired organically through Home recommendations.

The current priority table places play-through rate, early first-play bounce, play days per user and playtime per user above intentional co-play days, qualified sessions, spending days and Robux per user. Playtime contribution is capped at 60 minutes per user/game/day. The documented early bounce segments are under 60 seconds and 61–180 seconds.

This is a dated priority list, not published numerical model weights. Roblox can change signals and influence. Benchmark games are comparison aids, not algorithm inputs. Accurate, original metadata matters; mismatched or copied presentation can reduce exposure. Source: Discovery below.

## Verified retention facts

D1, D7 and D30 describe return on the corresponding day after first play; cohort charts are indexed by first-play date. Recent cohorts cannot yet supply D7/D30 outcomes. Cohort tables also expose cumulative playtime, payer conversion and revenue measures.

Roblox recommends improving the core loop, first-time experience and performance, and examining completion/drop-off through initial loop steps. Source: Retention below.

## Recommended diagnosis procedure (synthesis, not a platform guarantee)

1. Record build, release time, campaign/creative version, acquisition source, device segment and cohort size before interpreting a change.
2. Separate Home, sponsored, search and social traffic. A changed audience mix can move aggregate outcomes without a gameplay regression.
3. Trace exposure → play → initial interaction → first loop completion → next goal → return → fulfilled purchase. Define each denominator and time window.
4. If exposure-to-play is weak, test whether the promise is clear and accurate. If early exits are high, observe load failures, controls, device performance and time to meaningful action before adding rewards.
5. If initial play is healthy but return weak, interview/playtest the return motivation and progression. If purchases occur but trust declines, investigate delivery and offer clarity.
6. Compare mature cohorts over comparable windows. Document uncertainty and possible seasonality. Change one primary hypothesis at a time and record a guardrail such as crashes, early exits or purchase failures.
7. Do not declare an ad profitable from visits alone: define attributable net revenue, acquisition cost and the observation horizon in consistent units. A Robux booking is not automatically cash profit.

## Acceptance checks for a future dashboard

- A made-up cohort of 100 first-time players with 20 returning on D1 displays 20%, not 20 divided by all current active users.
- Immature D30 is unavailable, not zero.
- A campaign traffic surge remains visible separately from organic cohorts.
- Event duplication and renamed funnel steps cannot silently inflate completion.
- Experiment results include sample sizes, run dates, primary outcome and guardrails.

These checks have not been implemented or run. No account analytics were accessed. Open work: analytics event contracts/API verification, experiment statistics, ad attribution, actual benchmark interpretation and social-loop evidence.

## Report-specific qualification (2026-10-03)

Use [[Roblox Acquisition Experiments and Ad Measurement]] for campaign attribution and creative testing. The Acquisition page uses different revenue inclusions and D7 wording from other reports; preserve each report's cohort/window definition rather than forcing them into one metric. No account export has resolved the timing difference yet.

## Sources

Checked 2026-10-03:
- [Roblox Discovery](https://create.roblox.com/docs/discovery) — retrieval/ranking, source separation, signal priorities and metadata.
- [Roblox Retention](https://create.roblox.com/docs/production/analytics/retention) — cohort interpretation and first-time experience.

