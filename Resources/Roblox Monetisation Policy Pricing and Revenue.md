---
title: Roblox Monetisation Policy Pricing and Revenue
date: 2026-10-03
updated: 2026-10-03
verified: 2026-10-03
review_after: 2026-11-02
tags: [roblox, monetisation, policy, pricing, devex]
source: Roblox Creator Hub and labelled local inspection
project: null
status: sourced-not-purchase-tested
---
# Roblox Monetisation Policy Pricing and Revenue

Related: [[Paper Plane Toss Monetization]], [[Roblox Purchase Receipt Handling]], [[Roblox Economy Modelling and Progression Tests]], [[Roblox Vault Coverage and Maintenance]].

Recheck platform rules immediately before launch or changing offers. This note records platform guidance and engineering recommendations; no purchase, payout or compliance test was executed.

## Choose the entitlement contract

Passes are suited to one-time privileges; developer products support repeat purchases. Roblox's pass guide assigns privileges on the server and checks ownership when players join. [S1, S2] Design the grant, persistence and recovery contract before designing the purchase button.

Recommended offer record: product ID/type, exact benefit, duration, offline behaviour, stacking rule, prerequisites, limits, duplicate-purchase treatment, random components, applicable policy checks, current price lookup and support recovery path. A one-time starter offer implemented as a repeatable developer product needs explicit repeat-purchase handling. Merely hiding the button is not a durable entitlement rule.

A purchase prompt closing is not a persistent reward acknowledgement. Use [[Roblox Purchase Receipt Handling]] and test deferred/duplicate receipts.

## Paid randomness: verified policy scope

Paid randomness includes direct Robux purchases and indirect purchases using currency purchasable with Robux. Disclose all final outcomes and numerical odds before purchase; rarity labels alone may be insufficient. Where itemised details use a pop-up, the policy requires an accessible labelled Info/Details control. Paid luck modifiers need numerical explanation and updated displayed odds. Per-user restrictions come from PolicyService, including ArePaidRandomItemsRestricted and IsPaidItemTradingAllowed. Restricted users cannot interact with paid random generators; approved alternative treatments include removing the offer or offering guaranteed outcomes. [S3]

Recommended implementation review:
- Map every path from Robux to random rewards, including starter bundles, token packs, keys and boost purchases. Do not stop at egg products.
- Unknown policy response means unavailable until resolved; accept only an explicit valid response.
- Protect relevant server interactions as well as presentation. Review platform prompts, outside-game sales and deferred receipt paths separately.
- Do not invent a substitute for a purchase already charged. Define a compliant fulfilment/support policy before enabling the offer.
- Verify the exact distribution shown matches the server roll after luck, pity, exclusions and ownership changes.

These recommendations do not certify the existing project.

## Regional prices

Roblox's current guide says managed regional prices are enabled by default for passes; developer products have an enablement workflow. Economic location can differ from account location. Custom UI should retrieve runtime prices on the client; the guide names GetProductInfoAsync for individual items and provides Dynamic Price Check tooling. Price differences can create gifting/trading arbitrage, for which GetUsersPriceLevelsAsync is documented. [S4]

Recommended: while a price request is pending or fails, show a loading/unavailable state rather than confidently showing a configured price. Test every purchase surface and bundle label. Do not treat a client-provided price as authority for the reward. No change to regional-pricing settings is authorised by this note.

## Robux and cash are different quantities

Verified on 2026-10-03:
- Standard DevEx: USD 0.0038 per eligible Earned Robux.
- Balances earned before 2025-09-05 at 10 a.m. Pacific retain USD 0.0035.
- The conditional U.S. 18+ category is USD 0.0054; it is not a general uplift for every sale. Eligibility depends on qualifying spend, player verification/location and the game's character requirements. NPCs are excluded from that character assessment. [S5, S6]
- DevEx participation includes age 13+, at least 30,000 Earned Robux, verified email, portal/tax requirements and platform compliance. Dashboard estimates do not guarantee approval. Bought Robux is not automatically Earned Robux. [S5]

At the standard rate, 30,000 eligible Earned Robux corresponds to USD 114 before applicable deductions. Do not apply DevEx directly to the sticker price paid by players.

Recommended accounting chain:
1. Gross transaction Robux at actual sale prices.
2. Creator proceeds after the applicable transaction splits/fees and adjustments.
3. Eligible Earned Robux allocated to the actual DevEx categories.
4. Estimated cash = sum(eligible category balance × its applicable rate).
5. Net result after acquisition spend, production/operations expenses and applicable payout/tax costs.

Use transaction reports as evidence. This pass did not verify a universal platform-fee percentage; **do not fill every row with an assumed 30% cut**. Product type, sale context and reporting definitions must be verified before forecasting. Likewise, never deduct a platform fee twice from proceeds already reported net.

## Local source findings: Paper Plane Toss

Inspected 2026-10-03, not runtime-tested:
- Products.luau asks PolicyService on join and reports blocked status to the client. The expression ArePaidRandomItemsRestricted == true makes a missing/nonboolean flag count as unblocked after a successful table response. This is a defensive-validation gap, not evidence Roblox normally omits the field.
- The inspected Products.process path grants by product definition without consulting that policy result. Full outside-sale and receipt behaviour remains unaudited; do not call the project compliant solely because UI is hidden.
- Purchase.luau fetches PriceInRobux on the client, but first displays a Config fallback and retains it after lookup failure. The shared product prompt helper does not itself check paidRandomBlocked. Call-site enforcement and purchased-currency egg paths need a complete review.
- Current code uses GetProductInfo; the current regional-price guide names GetProductInfoAsync. API migration needs a separate implementation review.

## Buyer trust and acceptance checks (recommendations)

Explain the benefit and restrictions before prompting. Avoid misleading discounts, restartable fake scarcity and promises the grant system cannot fulfil. Evaluate paid advantages against the approved game design and observed player experience; competitor pricing is not proof a similar offer will retain buyers.

Test: restricted/unrestricted/unknown policy; indirect currency purchase; changed odds; duplicate starter purchase; off-sale product; missing or changed price; interrupted receipt; rejoin with entitlement; buyer inventory full; delayed fulfilment; and matching displayed versus prompt price. Record product IDs, build, account role, actual outcome and remediation.

Still open: verified fee schedule by transaction context, pass creator-ownership semantics, refund/ownership caching, pricing experiments, offer conversion and payer-retention evidence. No spend or project code was changed.

## Sources

Checked 2026-10-03:
- [S1: Passes](https://create.roblox.com/docs/production/monetization/passes)
- [S2: Developer products](https://create.roblox.com/docs/production/monetization/developer-products)
- [S3: Paid random items](https://create.roblox.com/docs/production/monetization/paid-random-items)
- [S4: Regional pricing](https://create.roblox.com/docs/production/monetization/regional-pricing)
- [S5: Developer Exchange](https://create.roblox.com/docs/production/monetization/developer-exchange)
- [S6: U.S. 18+ rate eligibility](https://create.roblox.com/docs/production/monetization/18-plus-devex-rate)
- Local: C:\Users\holde\Downloads\SecondGame\src\server\Systems\Products.luau and C:\Users\holde\Downloads\SecondGame\src\client\Purchase.luau.
