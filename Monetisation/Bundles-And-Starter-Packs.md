---
tags: [monetisation/offers]
status: draft
updated: 2026-10-04
confidence: medium
---
# Bundles and Starter Packs

## TL;DR
- The **first purchase is the hardest one**. A starter pack exists to turn a non-payer into a payer, not to make money directly. Payers who bought once buy again at a far higher rate than non-payers.
- Starter pack: **one-time developer product, 49–149 R$, perceived value ≥5× price**. Show it **after the player has felt the core loop** (about 5–15 min, or after the first progression wall). Never show it on join.
- Contents: soft currency + one visible, permanent cosmetic or pet + one short boost. Choose items the player **already wanted** from the shop they just browsed.
- Limited-time offers (LTOs) must be **genuinely limited**: a server-authoritative expiry stored per player, a visible countdown, and no immediate re-run. Fake urgency burns trust.
- Value framing: list every item with its standalone price and show the total ("Worth 1,250 R$ → 99 R$"). Use the same bundle art style each time so players learn to recognise "deal" offers.
- Track `offer_shown → offer_opened → prompt → purchased` funnels per offer. See [[Conversion-Funnels]].

## Starter pack spec (default)

| Field | Default | Rule |
|---|---|---|
| Product type | Developer product + saved `StarterPackOwned` flag | A product, not a pass, so you can re-issue it per season and gift it |
| Price | 49–99 R$ (core), up to 149 R$ for midcore | ≤ the smallest Robux pack. DevForum consensus: low price (25–100 R$) maximises first-purchase conversion |
| Value | 5–10× price when items are bought separately | Show the "Worth X" total |
| Contents | Currency ≈ 2× what the price buys in the currency ladder, + exclusive permanent cosmetic, + 30-min 2× boost | The cosmetic is the social signal: other players see it and ask about it |
| Trigger | First of: session minute 8, first fail/wall, first visit to the shop, level 3 | One automatic pop-up per session, max 2 lifetime. After that it lives as a shop tile |
| Expiry | 48–72 h from first show (per-player, server time) | Then it moves to a permanent but worse "Beginner Bundle" (higher price) |
| Eligibility | Never paid in this game | Also skip players who already own everything in it |

## Offer types and when to use them

| Offer | Target | Price | Trigger | Notes |
|---|---|---|---|---|
| Starter pack | Non-payers | 49–149 | Early session | One-time |
| Second-purchase bundle | Payers with exactly 1 purchase | 199–399 | 1–3 days after the first purchase | Bridges a 99 R$ first buyer into the 2× pass |
| Wall-breaker | Player stuck at a progression gate | 99–299 | On fail #2–3 at the same gate | Contains exactly what's needed to pass. Tight relevance converts best |
| Weekend / event LTO | All | 199–999 | Event start | Themed cosmetics. Real deadline |
| Comeback bundle | Lapsed 7+ days | 49–199 | First session after return | Pairs with free comeback rewards |
| Whale bundle | Top spenders (lifetime ≥ 5,000 R$) | 2,499–9,999 | Shop tile only, never a pop-up | Anchors prices |
| Mega "all passes" bundle | Players owning ≥2 passes | ~60–70% of the remaining pass prices | Shop | Products can't grant Roblox passes, so it grants your own flags. Make sure the pass checks also read those flags |

## Implementation notes
- **Eligibility checks happen on the server before prompting**: one-time flags, expiry, owned contents. Once Roblox charges, you must grant (see [[ProcessReceipt-Handling]]).
- Store `offers[offerId] = {firstShownAt, expiresAt, shownCount, purchased}` in player data. Compute countdowns from server `os.time()`, not the client clock.
- Bundles that contain items **also sold as passes** can't grant the Roblox pass itself. Grant an internal entitlement and make `Owns()` check `pass OR entitlement`.
- Do **not** sell bundles with paid random contents externally, or as promoted passes. Any random content needs odds disclosure. See [[Pay-To-Win-Boundaries]].
- Fetch the displayed price with `GetProductInfoAsync`. The "Worth X R$" figure is your own number, so compute it from current list prices to stay honest.

```lua
--!strict
-- ServerScriptService/Monetisation/OfferService.luau (ModuleScript) — eligibility + expiry core
local OfferService = {}

export type OfferState = { firstShownAt: number?, expiresAt: number?, shownCount: number, purchased: boolean }
export type OfferDef = { id: string, productId: number, durationSec: number, maxAutoShows: number,
	eligible: (data: { [string]: any }) -> boolean }

local OFFERS: { [string]: OfferDef } = {
	Starter = {
		id = "Starter", productId = 0000002, durationSec = 72 * 3600, maxAutoShows = 2,
		eligible = function(data) return (data.LifetimeRobuxSpent or 0) == 0 and not data.StarterPackOwned end,
	},
}

local function state(data: { [string]: any }, id: string): OfferState
	data.Offers = data.Offers or {}
	local s = data.Offers[id]
	if not s then
		s = { shownCount = 0, purchased = false }
		data.Offers[id] = s
	end
	return s :: OfferState
end

-- Returns seconds remaining if the offer may be shown now, else nil. Call on the server.
function OfferService.TryShow(data: { [string]: any }, id: string, auto: boolean): number?
	local def = OFFERS[id]
	if not def or not def.eligible(data) then return nil end
	local s = state(data, id)
	if s.purchased then return nil end
	local now = os.time()
	if not s.firstShownAt then
		s.firstShownAt = now
		s.expiresAt = now + def.durationSec
	end
	local remaining = (s.expiresAt :: number) - now
	if remaining <= 0 then return nil end
	if auto then
		if s.shownCount >= def.maxAutoShows then return nil end
		s.shownCount += 1
	end
	return remaining
end

-- Server check immediately before PromptProductPurchase.
function OfferService.CanPrompt(data: { [string]: any }, id: string): boolean
	local def = OFFERS[id]
	if not def or not def.eligible(data) then return false end
	local s = state(data, id)
	return not s.purchased and s.expiresAt ~= nil and os.time() < (s.expiresAt :: number)
end

function OfferService.MarkPurchased(data: { [string]: any }, id: string) -- call inside the receipt grant
	state(data, id).purchased = true
end

function OfferService.Get(id: string): OfferDef?
	return OFFERS[id]
end

return OfferService
```

## Value-framing copy rules
- Lead with the **hero item** (the visible cosmetic or pet), not the currency.
- Show "Worth 1,250 R$" (sum of current standalone prices) and "92% OFF" only when both are true.
- One adjective at most ("Exclusive", "Limited"). Kids' audiences respond to clear item pictures over text.
- Show the purchase count socially ("1,204 players got this today") only if the number is real.

## Checklist
- [ ] Starter pack: one-time, 49–149 R$, ≥5× value, server-side expiry, ≤2 auto pop-ups lifetime
- [ ] Second-purchase and wall-breaker offers defined
- [ ] Offer funnels instrumented (shown/opened/prompted/purchased) with an `offerId` field
- [ ] No offer pops during combat, on join, or more than once per session
- [ ] Bundle entitlements honoured by pass checks
- [ ] "Worth" values computed from live prices

## Pitfalls
- **Starter pack too strong** (permanent power in PvP) → P2W backlash. Keep its power temporary or cosmetic.
- **Starter pack too weak** → it fails its only job. Value must be obvious within 2 seconds of looking.
- **Fake countdowns** that reset on rejoin: players screenshot them and trust drops.
- Re-offering the starter pack to people who bought it (flag not saved) → refunds and angry reviews.
- Offering a cheaper bundle **after** someone just paid full price for its contents. Give owners a pro-rated version or exclude them.

## Related
- [[Monetisation/_Index]] · [[Pricing-Psychology]] · [[Conversion-Funnels]] · [[ProcessReceipt-Handling]] · [[Monetisation-Mistakes]]
- [[Economy-Design-Sinks-And-Faucets]] · [[AB-Testing]] · [[Analytics-And-Instrumentation]] · [[Genre-Playbooks]]

## Sources
- DevForum, "[POLL] Starter pack price points" (2019, still cited): https://devforum.roblox.com/t/poll-starter-pack-price-points/397653
- DevForum, "How can I get people to purchase my starter pack?" (2025): https://devforum.roblox.com/t/how-can-i-get-people-to-purchase-my-starter-pack/4032577
- Roblox creator-docs (snapshot 2026-10-02): `production/monetization/developer-products.md` (external sale limits: no random or limited items), `passes.md` (promoted pass rules), `paid-random-items.md`
- Offer timing and value multipliers: author heuristics from mobile F2P practice adapted to Roblox. ⚠️ verify with your own A/B tests ([[AB-Testing]])
