---
tags: [monetisation/subscriptions, monetisation/premium]
status: draft
updated: 2026-10-04
confidence: high
---
# Subscriptions, Premium/Plus and the End of Premium Payouts

## TL;DR
- **Premium Payouts (Engagement-Based Payouts) ended 2025-07-24** and were replaced by **Creator Rewards**: 5 R$ per Active Spender per day, plus audience-expansion revenue share. **Roblox Premium closed to new sign-ups on 2026-04-30** and was replaced by **Roblox Plus** ($4.99/mo). Any guide built around "Premium playtime payouts" is obsolete.
- **Experience subscriptions** are monthly auto-renewing benefits. Price them in **local currency** ($2.99/4.99/7.99/9.99/14.99) where possible: you get 70% in month 1 and **100% from month 2**. Robux subscriptions (≥49 R$) pay 70% every month.
- Up to **50 subscriptions per game**. They can't be mutually exclusive tiers (no Bronze/Silver/Gold of the same perks). Robux prices can change once per 60 days, with 30 days' notice for increases. Local-currency prices can't be changed.
- Plus/Premium perks in your game: give **convenience and cosmetics, never tactical power**. Check Plus with `player.HasRobloxSubscription` and legacy Premium with `player.MembershipType == Enum.MembershipType.Premium`.
- Earn from Plus directly: **up to 750 R$ per new subscriber** via `PromptRobloxSubscriptionPurchase` (250 R$/mo × 3 paid months, 60-day hold), plus up to **100 R$/subscriber** for their time in your paid private servers.

## Experience subscriptions (creator-docs, 2026-10)

| Property | Robux | Local currency |
|---|---|---|
| Eligibility | All creators | Account verified by ID or phone |
| Platforms | All | Web, App Store, Google Play |
| Countries | All | **Not** available in AR, CN, CO, IN, ID, JP, RU, TW, TR, AE, UA, VN |
| Price | ≥49 R$, any amount | $2.99 / 4.99 / 7.99 / 9.99 / 14.99 |
| Regional pricing | Forced on | N/A |
| Payout | 70% every month | 70% in month 1, then **100%** |
| Price change | Once per 60 days. Increases need ≥30 days' notice | **Not possible** (delete + recreate) |
| Delete while active | No refunds (Robux) | **Must refund all current subscribers** |

Guidelines that get games taken down if broken:
- Same benefits on every platform.
- Honour the full term: no silent revocation.
- No directing users to buy off-platform.
- No extra gating after payment, such as "post on social media to unlock". Battle passes may be sold as subscriptions.
- Clear names with price and duration shown in-game.

### What makes a good subscription
- **Daily-value** subscriptions work best: "VIP Club: 2× daily reward, +1 daily spin, exclusive monthly cosmetic, VIP chat tag, 10% shop discount". The player feels the benefit **every session**, which supports renewal.
- **Monthly exclusive cosmetic** gives collectors a reason never to cancel. Tie it to "subscribed in month X" so it is honest FOMO.
- **Season/battle pass as a subscription** is explicitly allowed.
- Avoid putting core power in a subscription in PvP. Subscription revocation also causes a "lost my progress" perception: make anything **earned** during the subscription permanent, and make only the **ongoing rate** subscription-bound.
- Rough sizing (assumption): subscriptions convert lower than one-off passes but have the highest LTV per payer. ⚠️ verify: no Roblox-published benchmark. Measure with [[Conversion-Funnels]].

### Server integration (status + revocation-safe)

```lua
--!strict
-- ServerScriptService/Monetisation/SubscriptionService.server.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local VIP_SUB_ID = "EXP-0000000000" -- Creator Hub → Monetization → Subscriptions

local function applyVip(player: Player, active: boolean)
	-- Only the ONGOING benefit is toggled; anything already earned stays in saved data.
	player:SetAttribute("VipSub", active)
end

local function refresh(player: Player)
	for attempt = 1, 3 do
		local ok, res = pcall(MarketplaceService.GetUserSubscriptionStatusAsync, MarketplaceService, player, VIP_SUB_ID)
		if ok and type(res) == "table" then
			applyVip(player, (res :: any).IsSubscribed == true)
			return
		end
		task.wait(2 ^ attempt)
	end
	-- On repeated failure, keep the last known state rather than revoking (fail-open for paying users).
end

Players.PlayerAdded:Connect(refresh)
Players.UserSubscriptionStatusChanged:Connect(function(player: Player, subscriptionId: string)
	if subscriptionId == VIP_SUB_ID then refresh(player) end
end)
for _, p in Players:GetPlayers() do task.spawn(refresh, p) end

-- Prompt (from a server-validated RemoteEvent): MarketplaceService:PromptSubscriptionPurchase(player, VIP_SUB_ID)
```

Other APIs: `GetSubscriptionProductInfoAsync`, `GetUserSubscriptionDetailsAsync`, `GetUserSubscriptionPaymentHistoryAsync`, `PromptCancelSubscription`, `PromptSubscriptionPurchaseFinished`.

### Replacing a pass with a subscription
Take the pass off sale and keep honouring it **forever** for existing holders. Sell the subscription to new users. Never convert existing pass owners to a subscription (see [[Monetisation-Mistakes]]).

## Roblox Plus (successor to Premium, launched 2026-04-30)

| Plus benefit (to the user) | Effect on you |
|---|---|
| 10% off purchases (20% from month 3), including your products, passes, subscriptions, paid access | **Roblox pays the discount**: you still get 70 R$ per 100 R$ list. Effective share is 78–88% of the user's spend. Show prices via `GetProductInfoAsync` (`PriceDiscountDetails`, `UserBasePriceInRobux`) |
| Free paid private servers | You get up to 100 R$ per subscriber per renewal if they spent ≥60 min in their own paid PS in your game and it's in their top 5 |
| Fee-free Robux transfers | You get 10% of transfers prompted in your game (`PromptRobuxTransferAsync`, 10–500 R$) |
| Trading/resale, UGC publishing | — |
| Optional Robux bundles (Plus 500/1000/2000) | ⚠️ verify: availability and pricing |

**Plus sign-up bonus**: `MarketplaceService:PromptRobloxSubscriptionPurchase(player)` → listen to `PromptRobloxSubscriptionPurchaseFinished` → confirm via `player:GetPropertyChangedSignal("HasRobloxSubscription")` before granting your in-game reward. You earn 250 R$ per paid month for the first 3 months (trials excluded, 60-day hold). Only prompts **from your game** count; `GetRobloxSubscriptionDetailsAsync(...).IsOriginExperience` tells you attribution.

### Plus / Premium perk design (legacy Premium members still exist)
- Allowed and effective: a cosmetic "Plus" badge or nametag, a Plus-only lounge, +10–20% daily reward, a free daily spin, early access to cosmetics, an extra free private-server feature.
- **Avoid**: tactical weapons or stats, a paywall on join, or promising Robux or anything outside your control. Roblox's own Premium guidance said not to give "a tactical gameplay advantage", and the same principle applies to Plus.
- Treat `MembershipType == Premium` and `HasRobloxSubscription` the same for perk purposes during the transition. ⚠️ verify: whether Premium remains for grandfathered members after 2026 and how `MembershipType` reports Plus.
- `PromptPremiumPurchase` still exists in the API, but Premium is closed to new sign-ups. **Use `PromptRobloxSubscriptionPurchase` instead.** ⚠️ verify: current behaviour of `PromptPremiumPurchase`.

## Creator Rewards (what replaced Premium Payouts)
- **Daily Engagement**: 5 R$/day for each Active Spender (≥$9.99 qualifying purchases in 60 days) for whom your game is one of the **first 3 launched that day** with ≥10 min played. It started automatically on 2025-07-24.
- **Audience Expansion**: 35% of a new or reactivated (60-day-lapsed) user's first $100 of qualifying purchases across Roblox within 60 days, when they arrive via your Share Link, direct link or exact-name search. Requires 100+ average DAU and an ID-verified creator with a DevEx account.
- Design implications:
  1. A **daily habit loop** that makes you the first game of the day: daily rewards that reset at a fixed UTC time, streaks, morning energy refills.
  2. **Share Links** in every off-platform post.
  3. 10-minute minimum sessions: front-load fun so day-one users pass 10 min.
- 60-day hold on all Creator Rewards. Bots, alts and teleport manipulation lead to forfeiture or a ban.

## Checklist
- [ ] Decided between Robux and local-currency subscriptions (default local currency when the audience is outside the excluded countries)
- [ ] Subscription benefits felt every session. Earned items stay permanent after cancellation
- [ ] `UserSubscriptionStatusChanged` handled. Fail-open on API errors
- [ ] Plus perk + `PromptRobloxSubscriptionPurchase` placed at a natural moment (paid PS screen, discount callout), confirmed by property change before rewarding
- [ ] Prices displayed with Plus discount details
- [ ] Share Links created. Daily-first-session hooks designed ([[Analytics-And-Instrumentation]] tracks them)
- [ ] No references to Premium Payouts in docs or dashboards

## Pitfalls
- Deleting a local-currency subscription forces refunds to all subscribers. Take it off sale and cancel renewals instead.
- Tiered subscriptions of the same perks are not supported. Make each subscription a distinct benefit set.
- Revoking earned progress on lapse ("your VIP pets disappeared") causes reviews to tank.
- Rewarding the Plus prompt before `HasRobloxSubscription` flips lets exploiters fire the reward remote for free.
- Hard-coded prices show the wrong price to Plus users. Roblox explicitly warns about this.

## Related
- [[Monetisation/_Index]] · [[Robux-Economy-DevEx-And-Platform-Cuts]] · [[Gamepasses-vs-Developer-Products]] · [[Pay-To-Win-Boundaries]] · [[Conversion-Funnels]]
- [[Analytics-And-Instrumentation]] · [[Moderation-And-Policy-Compliance]]

## Sources
- Roblox creator-docs (snapshot 2026-10-02): `production/monetization/subscriptions.md`, `roblox-plus.md`, `engagement-based-payouts.md` (deprecation notice), `creator-rewards.md`, `reference/engine/classes/MarketplaceService.yaml`. https://create.roblox.com/docs/production/monetization/subscriptions (accessed 2026-10-04)
- Roblox Newsroom, "Introducing Roblox Plus" (2026-04-10): https://about.roblox.com/newsroom/2026/04/introducing-roblox-plus-subscription
- DevForum, "Introducing Roblox Plus" (2026-04): https://devforum.roblox.com/t/introducing-roblox-plus/4567894
- PCGamesN, "Roblox Plus is replacing the current Premium subscription" (2026-04): https://www.pcgamesn.com/roblox/plus-subscription
- Roblox creator-docs, Creator Rewards: https://create.roblox.com/docs/creator-rewards (accessed via repo 2026-10-04)
