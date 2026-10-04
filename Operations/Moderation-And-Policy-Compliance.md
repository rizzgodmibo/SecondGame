---
tags: [operations/policy, operations/moderation]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Moderation And Policy Compliance

## TL;DR
- **Fill out the Maturity & Compliance Questionnaire before launch, honestly, based on the most extreme content in the game.** Without it, Roblox restricts playability for everyone. The label decides your audience: **Minimal/Mild → Roblox Kids (5–8) + Select (9–15) + 16+**, **Moderate → Select + 16+**, **Restricted → age-verified 18+ only**. Re-submit whenever an update changes an answer.
- **2026 publishing gate for under-16s:** to reach Kids/Select accounts the owner must be **age-checked + ID/face verified + 2-Step Verification on**, must **pay a refundable 1,000 R$ per-game fee or hold Roblox Plus/Premium for 2+ months**, and the game must pass evaluation (**250 unique plays by "highly engaged" age-checked 16+ users within 60 days**). The alternative is a **50,000 R$ refundable expedited review**. Plan launch timing around this ([[Launch-Checklist]]).
- **Filter every piece of user-authored text you display** (pet names, signs, guild names, custom chat UIs) with `TextService:FilterStringAsync` on the server. Games that don't filter get **removed until fixed**. `TextChatService` chat is filtered automatically.
- **Respect `PolicyService:GetPolicyInfoForPlayerAsync`.** If `ArePaidRandomItemsRestricted` is true, hide or replace Robux-bought loot boxes/eggs. If `IsPaidItemTradingAllowed` is false, block trading of paid items. Gate UGC-sharing, endless feeds and ads with their flags.
- Ban with **`Players:BanAsync`** (universe-wide, alt-account propagation by default). Publish your rules, keep the private reason, and offer an appeal path. No links or handles in the public ban message.
- Off-platform links are allowed only for approved socials (social media links on the game page, which need the owner to be age-verified 16+). **Never** put links or Discord invites in game text, chat or images.

## The rulebooks (read once, re-check quarterly)
| Document | What it governs | URL |
|---|---|---|
| Community Standards | All content and behaviour (violence, sexual content, hate, scams, off-platform, real-world harm) | https://en.help.roblox.com/hc/en-us/articles/203313410 |
| Terms of Use | Account, IP, Robux, liability; **no selling of game items for real money off-platform** | https://en.help.roblox.com/hc/articles/115004647846 |
| Restricted Content Policy | What is allowed in 18+ Restricted games | https://en.help.roblox.com/hc/en-us/articles/15869919570708 |
| Commerce Standards | Pricing and sales practices, misleading offers | https://en.help.roblox.com/hc/en-us/articles/36495190721172 |
| Advertising Standards | Ads, sponsored content | create.roblox.com/docs/production/promotion/comply-with-advertising-standards |
| Experience Guidelines / Content maturity | Labels, descriptors | create.roblox.com/docs/production/promotion/content-maturity |

## Content maturity questionnaire (Creator Hub → Configure → Questionnaire)
| Label | Contains (max) | Audiences |
|---|---|---|
| Minimal | Occasional mild violence, light unrealistic blood | Kids, Select, 16+ |
| Mild | Repeated mild violence, heavy unrealistic blood, mild fear, mild crude humour | Kids, Select, 16+ |
| Moderate | Moderate violence, light realistic blood, moderate fear, moderate crude humour, unplayable gambling content | Select, 16+ |
| Restricted | Strong violence, heavy realistic blood, romantic themes, alcohol, strong language | **Age-verified 18+**; unplayable in some regions (e.g. Korea, Saudi Arabia, Türkiye) |

Descriptor gotchas that silently shrink your audience:
- **Social hangout** as the primary theme: **16+ only**; with private spaces, **18+ verified**. Words like "hangout" or "vibe" in the title or description get you classified as one.
- **Free-form user creation** (drawing, free text on surfaces, uploaded images visible to others): **16+ only**. Assembling 3D assets (building a house, outfits) doesn't count.
- **Sensitive issues** as the primary theme: 16+ and not recommended unless the player is age-verified.
- Disclose **paid random items**, **paid item trading**, media sharing, endless feeds/autoplay, and **generative AI interaction** (limited vs extended).
- Playable gambling (betting Robux or items of value on chance) is **never allowed**. Only "unplayable" depictions are.
- Misrepresenting answers leads to moderation of the game and, if repeated, the account.

Decision rule for a broad-audience game: design to **Mild**. Use cartoon violence where bodies disappear, no realistic blood, no romance, and no free-form drawing visible to others (or gate it to 16+ via your own logic).

## Age checks and chat (2025–2026)
- From **January 2026** (global rollout after a December 2025 pilot in AU/NZ/NL), **an age check is required to use chat**: facial age estimation via Persona or ID. Checked users are placed in brackets (**<9, 9–12, 13–15, 16–17, 18–20, 21+**) and can only chat with similar ages. Sources: Roblox newsroom 2025-11, press.
- Account tiers (creator-docs 2026): **Roblox Kids** (5–8; chat off by default), **Roblox Select** (9–15; chat off until age-checked, then introduced gradually), **Roblox** (age-checked 16+).
- Implications for design: **many players can't chat**. Never make chat necessary for core gameplay. Provide quick-chat/emotes/pings (non-text) and party UIs that don't need chat. Use `TextChatService:CanUserChatAsync(userId)` and `CanUsersChatAsync(a, b)` before showing any text-chat-dependent UI (e.g. trade negotiation boxes).
- Social media links on the game page are **visible only to age-verified 16+ users**, and the adding creator must also be verified 16+.

## Text filtering (mandatory)
`TextChatService` filters its own chat per recipient. **You** must filter everything else that came from a user, server-side, and never show unfiltered text to anyone, including the author on other clients.

```lua
--!strict
-- ServerScriptService/TextFilter.lua (ModuleScript)
local TextService = game:GetService("TextService")

local TextFilter = {}

-- For text everyone sees (pet names, plot signs, guild names). Fails CLOSED.
function TextFilter.forBroadcast(text: string, fromUserId: number): string?
	if #text == 0 or #text > 100 then return nil end
	local ok, result = pcall(function()
		return TextService:FilterStringAsync(text, fromUserId, Enum.TextFilterContext.PublicChat)
	end)
	if not ok then return nil end
	local ok2, filtered = pcall(function()
		return (result :: TextFilterResult):GetNonChatStringForBroadcastAsync()
	end)
	return if ok2 then filtered else nil
end

-- For text shown to one specific recipient (e.g. a private note/DM-like UI).
function TextFilter.forUser(text: string, fromUserId: number, toUserId: number): string?
	local ok, result = pcall(function()
		return TextService:FilterStringAsync(text, fromUserId, Enum.TextFilterContext.PrivateChat)
	end)
	if not ok then return nil end
	local ok2, filtered = pcall(function()
		return (result :: TextFilterResult):GetNonChatStringForUserAsync(toUserId)
	end)
	return if ok2 then filtered else nil
end

return TextFilter
```
Rules:
- Store the **raw** text if you must, but **re-filter on every display** (filters change), or store and show only the broadcast-filtered version.
- On filter failure, show nothing or a placeholder ("Unnamed"). Never fall back to raw text.
- Developer-authored constants don't need filtering. Text from another player, a DataStore written by players, or a web API does.
- Rate-limit text input remotes (see `chat/examples/rate-limit-public-text-inputs.md`).

## PolicyService (per-player compliance)
`PolicyService:GetPolicyInfoForPlayerAsync(player)` (yields; pcall; ≤100 in-flight) returns:

| Key | If true/false → do |
|---|---|
| `ArePaidRandomItemsRestricted` | **true** → hide or disable Robux (or Robux-bought currency) loot boxes/eggs/spins; offer direct-purchase alternatives |
| `IsPaidItemTradingAllowed` | **false** → block trading of items bought with Robux or premium currency |
| `AreAdsAllowed` | **false** → don't show immersive ads |
| `IsContentSharingAllowed` | **false** → disable UGC sharing (screenshots/images/video posted for others) |
| `IsEndlessContentLoadAllowed` / `IsEndlessContentAutoplayAllowed` | **false** → paginate feeds / no autoplay |
| `IsEligibleToPurchaseSubscription` / `IsEligibleToPurchaseCommerceProduct` | **false** → hide those offers |
| `IsSubjectToChinaPolicies` | **true** → China compliance changes |
| `AllowedExternalLinkReferences` | Legacy; always empty |

```lua
--!strict
-- ServerScriptService/Policy.lua (ModuleScript)
local PolicyService = game:GetService("PolicyService")
local Players = game:GetService("Players")

export type Policy = {
	paidRandomRestricted: boolean,
	paidTradingAllowed: boolean,
	adsAllowed: boolean,
	contentSharingAllowed: boolean,
}

local cache: { [Player]: Policy } = {}
-- Fail SAFE: the most restrictive defaults until we know otherwise.
local RESTRICTIVE: Policy = {
	paidRandomRestricted = true, paidTradingAllowed = false, adsAllowed = false, contentSharingAllowed = false,
}

local Policy = {}

function Policy.get(player: Player): Policy
	local cached = cache[player]
	if cached then return cached end
	for attempt = 1, 3 do
		local ok, info = pcall(function() return PolicyService:GetPolicyInfoForPlayerAsync(player) end)
		if ok and type(info) == "table" then
			local p: Policy = {
				paidRandomRestricted = info.ArePaidRandomItemsRestricted == true,
				paidTradingAllowed = info.IsPaidItemTradingAllowed == true,
				adsAllowed = info.AreAdsAllowed == true,
				contentSharingAllowed = info.IsContentSharingAllowed == true,
			}
			cache[player] = p
			player:SetAttribute("PaidRandomRestricted", p.paidRandomRestricted) -- client UI hint only
			return p
		end
		task.wait(attempt)
	end
	return RESTRICTIVE
end

Players.PlayerAdded:Connect(function(p) task.spawn(Policy.get, p) end)
Players.PlayerRemoving:Connect(function(p) cache[p] = nil end)

return Policy
```
Enforce on the **server** in the purchase or trade handler, not just the UI. Game design for random items: [[Pay-To-Win-Boundaries]].

## Bans (Players:BanAsync)
- Config: `UserIds` (≤50), `Duration` seconds (`-1` = permanent), `DisplayReason` (≤400 chars, filtered, shown to the user), `PrivateReason` (≤1,000 chars, never shown), `ApplyToUniverse` (default true), `ExcludeAltAccounts` (default false, so alts are banned too), `ApplyDeviceBlock` (blocks the device for 24 h; only `UnbanAsync` lifts it).
- Server-only; works only on production servers (validated but not applied in Studio). Requires `Players.BanningEnabled`. Also available through the Creator Hub → Moderation → **Bans** dashboard and the Open Cloud User Restrictions API (useful for a Discord moderation bot).
- **Escalate** by history: `Players:GetBanHistoryAsync(userId)`. Example ladder: 1 day → 7 days → 30 days → permanent.
- Roblox ban guidelines: post your rules where everyone can see them, enforce them consistently, and **offer an appeal**. Ban messages may name a platform ("appeal in our community server", "message us on X") but **not** a handle or link.
- Exploiters: ban on **server-detected** impossible state (teleport distance, currency delta, remote spam), not on client reports.

## UGC and user-generated content risks
| Feature | Risk | Mitigation |
|---|---|---|
| Custom names/signs/bios | Slurs, PII, links | Filter (above); length cap; report button |
| Drawing/canvas, image IDs | Explicit or hateful images; counts as free-form creation (16+) | Gate to 16+ yourself, or use preset stamps only; `IsContentSharingAllowed` |
| Building with parts | Swastikas, inappropriate shapes | Grid/size limits, plot-only visibility, report → delete plot, owner-only edit |
| Trading | Scams, real-money trading (RMT) | Two-step confirm UI, value display, trade logs, ban RMT advertisers |
| Voice | Harassment | Roblox handles voice moderation; respect `VoiceChatService` eligibility |
| AI NPCs | Unsafe output | Disclose in the questionnaire; filter outputs; no cross-session memory unless declared |

Add an in-game **report** flow for game-rule violations (store it in a DataStore or send it via webhook to a moderated Discord). Roblox's own report button covers Community Standards.

## Off-platform links and promotion
- Allowed on the **game page** as social media links (up to 3, owner age-verified 16+, visible only to verified 16+ viewers). Group/community: at least one verified 16+ collaborator.
- Not allowed: links in game text, signs, images, chat, or partial or obfuscated links ("disc0rd dot gg/…"). Directing players to off-platform sales of game items or Robux is a ToU violation.
- Ban messages: platform names are OK; links and handles are not.
- Don't prompt players to "join our Discord for codes" with an in-game URL. Say "codes in our community (see game page)".

## DMCA / IP
- **If you're accused:** Roblox notifies you by message and email. You can file a **counter notice** to copyright_agent@roblox.com (or through the Rights Manager "Claims Against Me" tab). Roblox generally restores content **within 14 business days** unless the claimant files suit. Repeat infringers are suspended.
- **If you're copied:** register as a rights holder → **Rights Manager** → removal request (up to 250 links per request). The DMCA route is also open; knowingly false notices create 512(f) liability. Note the community backlash when big studios DMCA'd lookalikes (Pet Simulator X, 2023), so use it on asset rips, not genre clones.
- Don't use real brands, songs, characters or likenesses without a licence (Roblox has an IP licensing programme). Audio: only use assets you own or that are in the Creator Store.

## Checklist
- [ ] Questionnaire completed; label matches the intended audience; resubmit after content changes
- [ ] Kids/Select path decided (fee or Plus/Premium, verification, 2SV) and the Audience Reach dashboard monitored
- [ ] All user text filtered server-side; fail closed
- [ ] `Policy` module gates paid random items, paid trading, ads and UGC sharing on the server
- [ ] Rules page (in game plus description); appeal path; BanAsync with escalation
- [ ] No in-game links; socials only in game-page links
- [ ] Core gameplay works with chat disabled

## Pitfalls
- "Hangout" in the title → classified as a social hangout → 16+ only, losing most of the audience.
- Checking PolicyService on the client only. Exploiters, and timing gaps, bypass it.
- Showing the author their own unfiltered text locally while others see it filtered is fine **only** on the author's own client. Never replicate raw text.
- Robux-bought currency that is then spent on eggs still counts as a **paid random item**.
- Raising the content label later shrinks your audience overnight (e.g. Mild → Moderate loses Kids). Model the impact before adding gore or fear.

## Related
- [[Operations/_Index]] · [[Live-Ops-Playbook]] · [[Bad-Launch-Response]] · [[Post-Mortems-Real-Games]]
- [[Pay-To-Win-Boundaries]] · [[Launch-Checklist]] · [[Data-Persistence-DataStores-And-ProfileStore]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `production/promotion/content-maturity.md`, `production/publishing/kids-and-select.md`, `production/publishing/publish-games-and-places.md` (1,000 R$ publishing fee, 50,000 R$ expedited fee), `production/promotion/social-media-links.md`, `includes/text-filtering/text-filtering.md`, `chat/in-experience-text-chat.md`, `PolicyService.yaml`, `Players.yaml` (BanAsync/UnbanAsync/GetBanHistoryAsync), `production/bans.md`, `players/index.md` (ban/message guidelines), `production/publishing/ip-guidelines.md`, `rights-manager.md`. Live: https://create.roblox.com/docs/production/promotion/content-maturity and https://create.roblox.com/docs/production/publishing/kids-and-select. Checked 2026-10-04.
- Age checks for chat: https://about.roblox.com/newsroom/2025/11/roblox-requires-age-checks-limits-minor-and-adult-chat ; https://www.biometricupdate.com/202511/roblox-to-make-age-assurance-for-chat-mandatory-as-of-january-2026 ; https://www.pcgamer.com/gaming-industry/roblox-to-make-facial-age-checks-mandatory-to-access-any-chat-features-and-will-put-common-sense-limits-on-the-age-ranges-users-can-chat-within/
- Permissible links: https://devforum.roblox.com/t/reminder-regarding-permissible-links/61736 ; Community Standards https://about.roblox.com/community-standards (⚠️ verify: the current approved-link list; the older list was YouTube, Facebook, Discord, Twitter/X, Twitch and has since moved to social-link fields)
- Pet Simulator X DMCA backlash: https://www.dexerto.com/roblox/pet-simulator-x-creator-under-fire-for-hypocritical-dmca-on-roblox-games-2284798/
