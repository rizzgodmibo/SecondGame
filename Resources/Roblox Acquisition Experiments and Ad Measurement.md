---
title: Roblox Acquisition Experiments and Ad Measurement
date: 2026-10-03
updated: 2026-10-03
verified: 2026-10-03
review_after: 2026-11-02
tags: [roblox, acquisition, ads, thumbnails, experiments]
source: Roblox Creator Hub and labelled measurement recommendations
project: null
status: sourced-no-campaign-run
---
# Roblox Acquisition Experiments and Ad Measurement

Related: [[Roblox Discovery and Retention Measurement]], [[Roblox Monetisation Policy Pricing and Revenue]], [[Paper Plane Toss Thumbnails and Game Icon]], [[Roblox Vault Coverage and Maintenance]].

## Verified platform distinctions

**Home thumbnails:** Personalisation initially explores user groups, then allocates more impressions to each group's better-performing thumbnail while retaining exploration traffic. qPTR is qualified plays divided by Home recommendation impressions; reported average playtime is per qualified play. The guide recommends keeping multiple thumbnails active. It recommends 16:9 imagery, ideally 1920×1080, and keeping essential content away from the bottom overlay area. [S1]

**Ads Manager:** The guide describes up to ten campaign thumbnails distributed evenly. Reporting may lag up to 48 hours; attribution can continue for up to 30 days. New-user reports can attribute later returns through other sources to the original ad. Earnings exclude subscriptions but include ad revenue, Creator Rewards and in-game purchases. ROAS uses attributed USD earnings divided by spend; open windows may show an estimate. LaunchData is shareable and cannot prove an ad click. Robux-to-ad-credit conversion is irreversible. [S2]

**Acquisition dashboard:** Its 30-day revenue-per-user definition excludes subscriptions, engagement payouts and immersive ads. This differs from the Ads Manager earnings definition. Its table describes D7 using an eighth-day return after the initial session, whereas the Retention page uses a first-play-date cohort explanation. Preserve report-specific definitions and verify UI/export windows before merging these metrics. [S3]

These are dated documentation findings, not inspected account settings. No ad was purchased, campaign launched or artwork uploaded.

## Recommended experiment brief

Before a test record:
- Decision: what will change if the result supports the hypothesis?
- Audience and promise: which player need does the creative express, and where does actual gameplay deliver it?
- Versions: build, thumbnail/icon IDs, title/description, onboarding and offer versions.
- Surface: Home personalisation, sponsored campaign, search or share link.
- Outcome: exact metric definition, denominator, time zone and attribution window.
- Allocation: randomised fixed split, platform personalisation or observational comparison.
- Guardrails: early bounce, onboarding completion, errors, mature retention and buyer fulfilment.
- Planned duration, minimum useful effect, required evidence, spend ceiling and stop conditions.

Do not infer a causal creative winner from unequal personalised segments. Equal ad delivery also does not, by itself, establish independent random assignment or comparable audience composition. Keep a distinction between operational performance and a controlled causal experiment.

For Paper Plane Toss, progression versus distance-curiosity artwork is already a proposed comparison. Keep the actual game promise and first session consistent; do not simultaneously change tutorial, icon, prices and campaign audience and attribute all movement to the thumbnail.

## Metric contract

| Measure | Calculation or required definition | Common mistake |
|---|---|---|
| qPTR | Qualified plays / eligible Home impressions | Using clicks or all-source plays as numerator |
| CTR | Clicks / ad impressions, when those are the report's units | Treating a click as a satisfied player |
| CPP | Spend / attributed plays | Calling it cost per unique new user |
| Cost per acquired new user | Spend / unique attributed new users, if available | Counting repeat sessions as new customers |
| Observed ROAS | Attributed revenue in the same currency / spend | Calling it profit or incremental return |
| Incremental return | Revenue caused by the intervention versus a defensible counterfactual | Treating all attributed returning spend as caused by the ad |

Never subtract ad credits from USD or compare gross player spend with net creator proceeds. Use [[Roblox Monetisation Policy Pricing and Revenue]] for the conversion chain and document the ad-credit cost basis. Zero-denominator metrics are unavailable, not zero.

Illustrative arithmetic: spend USD 100, 500 attributed plays, 200 unique new users and USD 80 attributed earnings gives CPP USD 0.20, new-user acquisition cost USD 0.50 and observed ROAS 0.8. Those figures alone do not establish lifetime value, incremental revenue or profitability. They are synthetic examples, not campaign results.

## Practical sequence

1. Check that new players can join, understand the first action and retain progress on target devices. Buying more traffic does not identify or repair a broken first session.
2. Review each creative at its actual display size: clear action/subject, differentiated promise, honest reward depiction, legible optional text, unobscured focal area.
3. Save the baseline and configuration. Use only the approved campaign budget; separate research from spending authority.
4. During the test inspect safety/operational failures and budget use. Avoid repeatedly selecting whichever metric currently looks favourable.
5. Wait for the stated observation window and reporting delay; mark immature earnings or retention as pending.
6. Compare like-for-like audiences, windows and revenue definitions. Preserve absolute counts alongside rates and investigate audience-mix changes.
7. Decide keep, revise, retest or stop. Document what evidence would reverse that decision.

Statistical recommendations: predefine the primary outcome, analyse at the actual assignment unit, account for repeated users, and choose sample size from baseline variability and the smallest worthwhile effect. There is no universal number of impressions that proves a winner. Adaptive allocation requires appropriate analysis; do not attach a naive fixed-split significance claim to personalisation exports.

## Attribution and launch-data safety

Treat campaign/share-link launch data as descriptive input. Recommended: allowlist known values, enforce length/type limits, and never trust it as proof of spending or eligibility. If an approved campaign includes a reward, enforce server-owned eligibility and durable claim limits. A shared campaign URL can legitimately generate extra joins without matching platform ad counts.

For external creators or community links, record the link, content date and attribution limitations. A spike after coverage is correlation unless stronger evidence isolates the effect. Outreach, sponsorship agreements and spending remain separate authorised actions.

## Acceptance checks and remaining gaps

- Every saved report includes source, export date, campaign dates, reporting filter, spend units and metric definitions.
- The synthetic example above computes 0.20, 0.50 and 0.8 respectively.
- Reports with different revenue inclusions are not silently summed.
- Repeated sessions cannot inflate the unique-new-user denominator.
- Missing and immature outcomes remain labelled.
- Creative rejection, zero delivery and low conversion are diagnosed separately.
- A spend increase requires evidence and approval, not an automatic response to one good day.

Next acquisition work: current metadata/search practices, genre positioning, share-link reporting, influencer case studies and launch timing. A real account export is still needed for applied analysis; no audience or budget is invented.

## Sources

Checked 2026-10-03:
- [S1: Thumbnails and Home personalisation](https://create.roblox.com/docs/production/publishing/thumbnails)
- [S2: Ads Manager](https://create.roblox.com/docs/production/promotion/ads-manager)
- [S3: Acquisition analytics](https://create.roblox.com/docs/production/analytics/acquisition)
- [Retention analytics](https://create.roblox.com/docs/production/analytics/retention) — previously checked in [[Roblox Discovery and Retention Measurement]]; report-window discrepancy remains open.
