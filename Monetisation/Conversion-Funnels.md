---
tags: [monetisation/funnels, operations/analytics]
status: draft
updated: 2026-10-04
confidence: medium
---
# Conversion Funnels and Monetisation KPIs

## TL;DR
- **ARPDAU = payer conversion × ARPPU.** Roblox's dashboard defines conversion as % of DAU who pay that day, ARPPU as revenue per paying user, and ARPDAU as revenue per DAU. Fix conversion first (shop visibility, starter pack, relevance), then ARPPU (ladders, bundles, subscriptions).
- Benchmarks (third-party, ⚠️ verify against the Creator Hub benchmark panel for your genre): **daily payer conversion <1% = broken, 1–3% = median, 3–5% = strong, >5% = top tier.** ARPDAU of about **$0.003–0.006 is conservative and $0.015–0.025 is well monetised** (USD after DevEx).
- Platform context: Roblox average bookings per DAU was **$12.66 for Q2 2026** (−2% YoY) on 123M DAU. That is what players spend platform-wide; your game captures a small slice of it.
- Where prompts convert: **at the moment of need** (wall, fail, locked door, inventory full), **after a win** (reward-moment upsell), and in a **persistent shop button**. Never on join, never mid-combat, max one unsolicited pop-up per session.
- First purchase timing: offer the starter pack **after the core loop clicks** (about 5–15 min, or the first wall). Day-1 payers are rare; most first purchases happen in sessions 2–5. ⚠️ verify with your own cohort data.
- Log a store funnel with `AnalyticsService:LogFunnelStepEvent`, currency flows with `LogEconomyEvent` (`IAP` source for Robux-bought currency), and purchases with `LogCustomEvent` carrying `CurrencySpent`.

## Metric definitions and formulas

| Metric | Formula | Where to read it |
|---|---|---|
| Payer conversion (daily) | paying users today ÷ DAU | Creator Hub → Analytics → Monetization |
| ARPPU | revenue ÷ paying users | same |
| ARPDAU | revenue ÷ DAU = conversion × ARPPU | same |
| First-time payer rate | new payers today ÷ never-paid DAU | Custom: log a `FirstPurchase` event |
| Repeat rate (30d) | payers with ≥2 purchases ÷ payers | Custom |
| Shop open rate | users opening the shop ÷ DAU | Funnel step 1 |
| Prompt→purchase | purchases ÷ prompts shown | `PromptProductPurchaseFinished` (isPurchased) vs prompts |
| LTV (simple) | ARPDAU × average lifetime days | Retention × ARPDAU |
| Creator Rewards per DAU | Daily-Engagement R$ ÷ DAU | Monetization → Creator Rewards |

**USD conversion:** Robux revenue figures in the dashboard are typically what you earned. ⚠️ verify: whether a given chart shows gross or net. Multiply net R$ by 0.0038 for USD.

### Worked example
DAU 20,000 · conversion 2.5% → 500 payers · ARPPU 280 R$ gross → 140,000 R$ gross/day → 98,000 R$ net → **$372/day**, ARPDAU **$0.0186**.
- Raising conversion to 3.5% (starter pack + better shop placement) → +$149/day.
- Raising ARPPU by 20% (ladder) → +$74/day.
- That is why conversion is the first lever.

## Funnel to instrument (minimum viable)

| Step | Event | API |
|---|---|---|
| 1 | Shop opened (source: button / NPC / prompt / wall) | `LogFunnelStepEvent(player, "Shop", sessionGuid, 1, "Opened")` |
| 2 | Item viewed | step 2 "Viewed" (custom field: itemId) |
| 3 | Purchase prompted | step 3 "Prompted" |
| 4 | Purchase completed (from the receipt handler or pass event) | step 4 "Purchased" + `LogCustomEvent(player, "RobuxSpent", CurrencySpent)` |
| — | Robux currency source | `LogEconomyEvent(player, Source, "Gems", amount, balanceAfter, IAP.Name, sku)` |
| — | Offer impressions | `LogCustomEvent(player, "OfferShown")` with custom field `offerId` |
| — | Wall hit / fail | `LogCustomEvent(player, "WallHit")` with field `gateId` |

```lua
--!strict
-- ServerScriptService/Monetisation/ShopFunnel.luau (ModuleScript)
local AnalyticsService = game:GetService("AnalyticsService")
local HttpService = game:GetService("HttpService")

local ShopFunnel = {}
local sessions: { [Player]: string } = {}

export type Step = "Opened" | "Viewed" | "Prompted" | "Purchased"
local STEP_INDEX: { [Step]: number } = { Opened = 1, Viewed = 2, Prompted = 3, Purchased = 4 }

function ShopFunnel.Step(player: Player, step: Step, source: string?, itemId: string?)
	if step == "Opened" or not sessions[player] then
		sessions[player] = HttpService:GenerateGUID(false) -- new funnel session per shop open
	end
	local fields: { [string]: string } = {}
	if source then fields[Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = source end
	if itemId then fields[Enum.AnalyticsCustomFieldKeys.CustomField02.Name] = itemId end
	AnalyticsService:LogFunnelStepEvent(player, "Shop", sessions[player], STEP_INDEX[step], step, fields)
end

function ShopFunnel.Clear(player: Player)
	sessions[player] = nil
end

return ShopFunnel
```
`LogFunnelStepEvent(player, funnelName, funnelSessionId, step, stepName, customFields)` takes custom fields as its 6th argument (API reference, 2026-10). Analytics only tracks the **10 most recent `funnelSessionId`s per user per funnel**, and there are daily event and cardinality limits, so use custom fields rather than unique event names. More in [[Analytics-And-Instrumentation]].

## Shop and prompt placement rules

| Placement | Do | Don't |
|---|---|---|
| HUD shop button | Always visible, left or right edge, with a notification dot only when there's a new offer | Hide it in a menu. Use more than 1 shop button |
| Contextual prompt | Inventory full → "+50 slots" pass. Locked VIP door → VIP pass. Fail at boss → revive product | Prompt for something unrelated to the moment |
| Reward moment | After an egg hatch or level-up: "2× luck for the next 10 hatches" | Interrupt the reward animation itself |
| Physical shop (NPC/zone) | Spawn-adjacent, on the path to the core loop | Put it behind a long walk |
| Roblox Shop overlay | Keep it enabled (Roblox ranks your items and may surface Robux packs including them); call `OpenShop` from your button for the long tail | Duplicate every item in both without a reason |
| Pop-ups | ≤1 unsolicited per session, never in the first 3 minutes, never during combat or trading | Chain pop-ups on join (the top reason for "cash grab" reviews) |
| Rewarded ad button | Lobby/menus and post-fail, "Watch ad for 2× coins" (reward ≈ 3–10 R$ value) | Force ads, or show to ineligible users (`GetAdAvailabilityNowAsync`) |

Use `RecommendTopProductsAsync` / `RankProductsAsync` (once at join) to order the shop per user. Roblox's ranking uses platform-wide signals.

## First-purchase playbook
1. Make the **free economy visible**. Players must see what paying would speed up: show the "Auto-collect" pass icon greyed out on the HUD.
2. Session 1, minute 5–15: starter pack (one auto pop-up, then a shop tile with a countdown).
3. First wall: wall-breaker offer, plus the free alternative path shown side by side. This keeps the free path honest and lowers backlash.
4. After the first purchase, wait 1–3 days and show the second-purchase bundle. Watch the repeat rate.
5. Payers with lifetime spend over 2,000 R$: surface the anchors and the subscription.

## Checklist
- [ ] Shop funnel (4 steps) + `RobuxSpent` + `FirstPurchase` events live **before** launch
- [ ] Economy events: every Robux-bought currency source tagged `IAP` with a SKU
- [ ] Shop button always visible. ≤1 unsolicited pop-up per session. None in the first 3 min
- [ ] Contextual prompts at walls, inventory-full and locked areas
- [ ] Dashboard reviewed weekly: conversion, ARPPU, ARPDAU, first-time payers, prompt→purchase per placement
- [ ] Changes tested via [[AB-Testing]], not shipped blind

## Pitfalls
- Optimising ARPPU (whale items) while conversion is under 1%. A high ARPPU with a low ARPDAU means revenue depends on a small group of players (Roblox's own guidance).
- Counting AdReward receipts as purchases: inflates conversion.
- Measuring prompt conversion with `PromptProductPurchaseFinished` but granting there too. Measure there, grant only in the receipt handler.
- Comparing against benchmarks from other genres. Simulators convert far better than social hangouts.

## Related
- [[Monetisation/_Index]] · [[Bundles-And-Starter-Packs]] · [[Pricing-Psychology]] · [[ProcessReceipt-Handling]] · [[Monetisation-Mistakes]]
- [[Analytics-And-Instrumentation]] · [[AB-Testing]] · [[Genre-Playbooks]] · [[Economy-Design-Sinks-And-Faucets]]

## Sources
- Roblox creator-docs (snapshot 2026-10-02): `production/analytics/monetization.md` (definitions, guidance), `funnel-events.md`, `economy-events.md`, `custom-events.md`, `custom-fields.md`, `event-types.md`; `production/monetization/shop.md`, `developer-products.md`; `promotion/rewarded-video-ads.md`. https://create.roblox.com/docs/production/analytics/monetization (accessed 2026-10-04)
- Roblox Q2 2026 results (DAU 123M, ABPDAU $12.66): https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Earnings-Shareholder-Letter.pdf and https://www.investing.com/news/company-news/roblox-q2-2026-slides-bookings-growth-slows-to-8-amid-user-decline-93CH-4826401 (2026-07/08)
- Conversion/ARPDAU benchmark ranges (third-party): https://zehn-studio26.com/glossary/conversion-rate/ and https://generalistprogrammer.com/tutorials/roblox-game-monetization-complete-revenue-strategy-guide (2026). ⚠️ verify
- DevForum, "Payer Conversion Rate and ARPDAU decreasing as game gains more popularity" (2025): https://devforum.roblox.com/t/payer-conversion-rate-and-arpdau-decreasing-as-game-gains-more-popularity/3898921
