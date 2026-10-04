---
tags: [operations/kpi, operations/analytics]
status: draft
updated: 2026-10-04
confidence: medium
---
# KPI Dashboard Spec

## TL;DR
- Check **5 numbers daily** (CCU curve, new users, play-through rate, D1 of the cohort 2 days ago, revenue) and **12 weekly**. Each metric has a target band and a **pre-decided action** when it leaves the band, so nobody has to improvise a response.
- Targets come first from the **Creator Hub "similar experiences" benchmark (P50–P90 band)**. Aim for ≥ P50 everywhere and ≥ P75 on the one metric your genre lives on (D1 for simulators, session time for social, payer conversion for tycoons). The fixed numbers below are fallbacks ⚠️ verify against [[Growth-Metrics-And-Benchmarks]].
- **Look at a metric's trend before its level**, and compare the same weekday week over week. Weekend vs weekday swings are large on Roblox.
- Segment every alarm by **platform** (mobile is usually 60–80% of players ⚠️ verify on your dashboard), **new vs returning**, and **acquisition source** before acting. Many "drops" turn out to be a mix shift.
- Instrumentation behind this spec: [[Analytics-And-Instrumentation]]. Response playbooks: [[Bad-Launch-Response]], [[Live-Ops-Playbook]].

## Daily (5 min, every morning)
| # | Metric | Where | Healthy band (fallback) | If outside band → action |
|---|---|---|---|---|
| 1 | **Peak CCU & CCU curve** (vs same weekday last week) | Overview | ≥ −10% WoW | −10–25%: check recommendations traffic share (Acquisition). Below −25%: check the error report and crash rate for a broken update; if healthy, bring the event or update forward |
| 2 | **New users with plays** by source | Acquisition | Home recommendations growing or stable | Recs falling → engagement metrics fell → see D1 and session; refresh icon/thumbnail ([[Discovery-Algorithm]]) |
| 3 | **Play-through rate** (impression → play) | Acquisition | ≥ benchmark P50; fallback ≥ 4–6% ⚠️ verify | Below P50 for 3 days → icon/thumbnail test |
| 4 | **D1 retention** (cohort from D-2) | Retention | ≥ P50 (docs example band 12.1–18.7%); GameAnalytics median 10.3% for ≥1M-MAU games (Aug 2025–Jul 2026) | Below P50 → onboarding funnel drill-down; below 8% → [[Bad-Launch-Response]] |
| 5 | **Revenue (Robux) & payers** | Monetization | ≥ −15% WoW | Check purchase prompt failures (custom event), shop funnel step drop, price/config changes |
| + | **Client crash rate / errors** | Performance, Alerts | < 2% sessions; alert at 5% for 5 min (docs example) | Roll back the last update ([[Live-Ops-Playbook]]) |

## Weekly (30–60 min, Sunday/Monday, write it down)
| Metric | Definition | Target (fallback) | Action trigger |
|---|---|---|---|
| DAU / MAU (stickiness) | DAU ÷ MAU | ≥ 15% ⚠️ verify | < 10% → no reason to return daily; add dailies/streaks ([[Retention-Metrics-D1-D7-D30]]) |
| D7 retention | Cohort return on day 7 | ≥ P50; fallback ≥ 4–5% ⚠️ verify | < P50 with OK D1 → mid-term goals, social systems |
| D30 retention | | ≥ P50; fallback ≥ 1.5–2% ⚠️ verify | Low → endgame/prestige/collection depth |
| Avg session length | Playtime ÷ sessions | ≥ P50; fallback 12–20 min ⚠️ verify | Short → check `SessionMilestone` drop-offs |
| Playtime per DAU | | ≥ P50 | Drives recommendations and engagement-based payouts |
| Onboarding completion | Last step ÷ step 1 | ≥ 60% | Largest single-step drop > 25% → fix that step first |
| Payer conversion (7-day) | Payers ÷ DAU | ≥ P50; fallback 1–3% ⚠️ verify | Low with good retention → first-purchase offer placement ([[Conversion-Funnels]]) |
| ARPPU | Revenue ÷ payers | ≥ P50 | Low → price ladder, bundles, high-tier offers |
| ARPDAU | Revenue ÷ DAU | ≥ P50 | Composite. Diagnose via conversion × ARPPU |
| Economy net flow | Σ sources − Σ sinks per currency | ≈ 0 to slightly positive | Growing wallets (especially payers) → add sinks |
| Shop funnel completion | Granted ÷ Opened | Track trend | Drop after an update → UI regression |
| New-user share of DAU | New ÷ DAU | 20–50% during growth | < 15% → acquisition stalling; > 70% → retention is weak |
| Experiment status | Running tests and early-harm flags | — | Decide on the decision date ([[AB-Testing]]) |

## Monthly / per update
- **Cohort retention curve** per update week (did update N improve D1/D7 of its cohort?).
- **LTV estimate** = ARPDAU × expected lifetime days (Σ retention curve). Compare against ad CPA before scaling ads.
- **Revenue mix**: game passes vs dev products vs subscriptions vs Premium Payouts / engagement rewards. ⚠️ verify the current engagement-payout programme name and rules in Monetisation notes.
- **Top 10 custom events** trend (feature adoption) and **dead features** (< 5% of DAU use them → cut or improve).
- **Server performance** by place version.

## Layout spec (if building an external dashboard)
1. Header row: CCU now, DAU (today vs same day last week), revenue today, crash rate.
2. Acquisition: stacked new users by source; play-through line with the benchmark band.
3. Retention: D1/D7/D30 cohort lines with the P50–P90 shaded band.
4. Funnel: onboarding bar chart (step % of step 1), highlighting the biggest drop.
5. Monetisation: payers, conversion, ARPPU, revenue by product.
6. Economy: sources vs sinks per currency; average wallet (payers vs non-payers).
7. Annotations: every update, config flip and event start time. Without these the charts can't be interpreted.

The Creator Hub **Explore** page supports formulas, benchmark overlays and prior-period overlays. Build these views there before reaching for an external tool.

## Decision rules summary
- **Never act on 1 day of data** except crashes, revenue collapse (> 40%) or data loss.
- **Fix in funnel order**: play-through → onboarding → D1 → D7 → monetisation.
- **One change per metric per week**, annotated.
- **Ship ads only if** D1 ≥ P50 and LTV > CPA × 1.3.

## Checklist
- [ ] Benchmarks noted for each metric (screenshot P50/P90 once a month into `Projects/<game>/`)
- [ ] Daily 5-metric check habit / automated summary
- [ ] Weekly KPI log (date, metric values, changes shipped, hypothesis)
- [ ] Alerts: crash rate, DataStore errors, server memory
- [ ] Annotations for every release and config change

## Pitfalls
- Comparing Saturday to Tuesday. Always compare the same weekday.
- Reading D1 for a cohort that's still incomplete.
- Global averages hide platform problems. A mobile UI bug shows up only in the mobile breakdown.
- Influencer spikes inflate new users and deflate D1 (low-intent traffic). Segment by source.
- Vanity metrics such as total visits and favorites don't drive decisions.

## Related
- [[Operations/_Index]] · [[Analytics-And-Instrumentation]] · [[Bad-Launch-Response]] · [[AB-Testing]] · [[Live-Ops-Playbook]]
- [[Retention-Metrics-D1-D7-D30]] · [[Conversion-Funnels]] · [[Growth-Metrics-And-Benchmarks]] · [[Discovery-Algorithm]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `production/analytics/analytics-dashboard.md` (benchmarks P50–P90; example D1 band 12.11–18.73%; payer segments), `acquisition.md`, `alerts.md` (crash rate 5% example), `economy-events.md`. Checked 2026-10-04.
- https://devforum.roblox.com/t/analytics-similar-experience-benchmarks-broader-access/2210285 (example D1 band 12.4–24.1%)
- GameAnalytics 2026 Roblox Benchmark Report: https://www.gameanalytics.com/reports/2026-roblox-report (median D1 10.3%, via search snippet; ⚠️ verify by reading the report)
