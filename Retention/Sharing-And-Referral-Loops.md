---
tags: [retention/social, growth/referral]
status: draft
updated: 2026-10-04
confidence: high
---
# Sharing and Referral Loops

## TL;DR
- **Four entry points, one reader.** In-game invite (`SocialService:PromptGameInvite` + `ExperienceInviteOptions`), share sheet (`SocialService:PromptLinkSharingAsync`, server-only), Creator Hub **share links** (trackable, custom LaunchData), and event/notification links. All of them land in `Player:GetJoinData()` on the server: `ReferredByPlayerId`, `LaunchData` and `GameJoinContext`.
- **Use `ReferredByPlayerId` for referral rewards.** It populates automatically for all invitation types. Use `LaunchData` (≤ 200 chars, JSON) only for routing ("spawn at my plot"). Launch data can arrive a few seconds late, is not 100% reliable and is user-editable in URLs, so never trust it for value.
- **Reward both sides, but pay the inviter only for a *real* new player:** invitee is a first-time player, stays ≥ 5 min (or finishes onboarding), one reward per invitee ever, inviter cap (e.g. 5/day, 50 total). Store state in DataStore with `UpdateAsync` and deliver offline inviter rewards through a pending-rewards key.
- **Publish a Referral Rewards banner** (Creator Hub → Engagement → Referral Rewards). It shows on top of the friend-invite modal with your reward text and optional per-inviter limit. Only one banner can be live at a time, and it must match what the code grants.
- **Ask at peak-joy moments,** not on spawn: right after a rare drop, a boss kill, a level-up, or a co-op goal that needs 2 players. Gate `PromptGameInvite` behind `CanSendGameInviteAsync` (pcall).
- **Use a separate share link per channel** (YouTube description, TikTok bio, Discord, each creator). The Acquisition page then shows new users and D7 by link ([[Retention-Metrics-D1-D7-D30]]). Deep links are **deprecated** in favour of share links.

## API facts (verified 2026-10-04)
| API | Where | Key facts |
|---|---|---|
| `SocialService:CanSendGameInviteAsync(player, recipientId?)` | Client (LocalScript) | Yields. Wrap in pcall. Ability varies by platform/player. |
| `SocialService:PromptGameInvite(player, options?)` | Client | Opens friend picker, or a single friend if `InviteUser` is set |
| `ExperienceInviteOptions` (Instance) | Client | `PromptMessage` (hidden if too long), `InviteUser` (UserId), `InviteMessageId` (Notification asset ID; text must include `{experienceName}`, may include `{displayName}`), `LaunchData` (≤ 200 chars) |
| `SocialService.GameInvitePromptClosed(player, recipientIds)` | Event | `recipientIds` is **no longer populated** (empty array). You cannot tell whom they invited. |
| `SocialService:PromptLinkSharingAsync(player, options?)` | **Server only** | Generates an expiring link and opens the share sheet (or copies to clipboard). Options: `ExpirationSeconds` (default 86,400), `PreviewTitle`, `PreviewDescription`, `PreviewAssetId`, `LaunchData`, `FallbackLinkId`. Returns `Enum.PromptLinkSharingResult`. `PromptLinkSharing` (non-Async) is deprecated. |
| `SocialService.ShareSheetClosed` | Server event | Fires when the share sheet is dismissed |
| `Player:GetJoinData()` | Server | `ReferredByPlayerId`, `LaunchData`, `SourcePlaceId`, `SourceGameId`, `TeleportData`, `GameJoinContext` (e.g. `EventId`) |
| Share links | Creator Hub → Creations → Share Links | Unlimited per game. Optional custom LaunchData. Group games need the "Create and configure share links" permission. |
| Deep links (`roblox.com/games/start?placeId=&launchData=`) | Web | **Deprecated** for public use. Launch data ≤ 200 bytes decoded, URL-encode it. |

## Code

### Client invite button (StarterPlayerScripts/InvitePrompt, LocalScript)
```lua
--!strict
-- StarterPlayer/StarterPlayerScripts/InvitePrompt (LocalScript)
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local SocialService = game:GetService("SocialService")

local player = Players.LocalPlayer
local INVITE_MESSAGE_ID = "" -- Notification asset ID from Creator Hub (optional)

local function canInvite(recipientId: number?): boolean
	local ok, result = pcall(function()
		if recipientId then
			return SocialService:CanSendGameInviteAsync(player, recipientId)
		end
		return SocialService:CanSendGameInviteAsync(player)
	end)
	return ok and result == true
end

-- Call at peak moments (rare drop, boss kill) or from an "Invite friends" button.
local function promptInvite(recipientId: number?)
	if not canInvite(recipientId) then
		return
	end
	local options = Instance.new("ExperienceInviteOptions")
	options.PromptMessage = "Invite friends — you both get a Starter Crate!"
	if INVITE_MESSAGE_ID ~= "" then
		options.InviteMessageId = INVITE_MESSAGE_ID
	end
	if recipientId then
		options.InviteUser = recipientId
	end
	-- Routing only (spawn near inviter). Rewards use ReferredByPlayerId server-side.
	options.LaunchData = HttpService:JSONEncode({ r = "plot", u = player.UserId })
	SocialService:PromptGameInvite(player, options)
end

local _ = promptInvite -- wire to UI
```

### Server referral handling (ServerScriptService/Referrals, Script)
```lua
--!strict
-- ServerScriptService/Referrals (Script)
local DataStoreService = game:GetService("DataStoreService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")

local PlayerData = require(ServerScriptService.Data.PlayerData) :: any -- GetProfile(player)

local referralStore = DataStoreService:GetDataStore("Referrals_v1")
local pendingStore = DataStoreService:GetDataStore("PendingRewards_v1")

local QUALIFY_SECONDS = 300 -- invitee must play 5 min
local INVITER_DAILY_CAP = 5
local INVITER_TOTAL_CAP = 50
local INVITEE_REWARD = { Coins = 500 }
local INVITER_REWARD = { Coins = 1000 }

local function readJoinData(player: Player): (number, { [string]: any }?)
	-- Launch data can lag a few seconds; poll briefly.
	local referrer = 0
	local launch: { [string]: any }? = nil
	for _ = 1, 10 do
		local jd = player:GetJoinData()
		referrer = tonumber(jd.ReferredByPlayerId) or 0
		local raw = jd.LaunchData
		if typeof(raw) == "string" and raw ~= "" then
			local ok, decoded = pcall(HttpService.JSONDecode, HttpService, raw)
			if ok and typeof(decoded) == "table" then
				launch = decoded
			end
		end
		if referrer ~= 0 or launch then
			break
		end
		task.wait(1)
	end
	return referrer, launch
end

local function grant(player: Player, reward: { Coins: number })
	local profile = PlayerData.GetProfile(player)
	if profile then
		profile.Data.Coins += reward.Coins
	end
end

-- Atomically decide whether this invitee->inviter pair pays out.
local function claimReferral(inviteeId: number, inviterId: number): boolean
	local today = math.floor(os.time() / 86400)
	local inviteeOk, inviteeFresh = pcall(function()
		local fresh = false
		referralStore:UpdateAsync(`invitee_{inviteeId}`, function(old: any)
			if old ~= nil then
				return nil -- already referred once: cancel
			end
			fresh = true
			return { by = inviterId, at = os.time() }
		end)
		return fresh
	end)
	if not inviteeOk or not inviteeFresh then
		return false
	end
	local inviterOk, allowed = pcall(function()
		local ok = false
		referralStore:UpdateAsync(`inviter_{inviterId}`, function(old: any)
			local s = if typeof(old) == "table" then old else { total = 0, day = today, dayCount = 0 }
			if s.day ~= today then
				s.day = today
				s.dayCount = 0
			end
			if s.total >= INVITER_TOTAL_CAP or s.dayCount >= INVITER_DAILY_CAP then
				return nil
			end
			s.total += 1
			s.dayCount += 1
			ok = true
			return s
		end)
		return ok
	end)
	return inviterOk and allowed == true
end

local function rewardInviter(inviterId: number)
	local inviter = Players:GetPlayerByUserId(inviterId)
	if inviter then
		grant(inviter, INVITER_REWARD)
		return
	end
	-- Offline or in another server: queue it; their server grants on next join.
	pcall(function()
		pendingStore:UpdateAsync(tostring(inviterId), function(old: any)
			local coins = (if typeof(old) == "table" then old.Coins else 0) + INVITER_REWARD.Coins
			return { Coins = coins }
		end)
	end)
end

local function deliverPending(player: Player)
	local value: any = nil
	local ok = pcall(function()
		pendingStore:UpdateAsync(tostring(player.UserId), function(old: any)
			value = old
			return nil -- read-only pass
		end)
	end)
	if ok and typeof(value) == "table" and (value.Coins or 0) > 0 then
		-- Remove first, then grant (at-most-once beats dupes).
		local removed = pcall(function()
			pendingStore:RemoveAsync(tostring(player.UserId))
		end)
		if removed then
			grant(player, { Coins = value.Coins })
		end
	end
end

Players.PlayerAdded:Connect(function(player)
	task.spawn(deliverPending, player)

	local referrer, launch = readJoinData(player)
	if launch and launch.r == "plot" then
		player:SetAttribute("SpawnNearUserId", tonumber(launch.u) or 0) -- routing only
	end
	if referrer == 0 or referrer == player.UserId then
		return
	end
	local profile = PlayerData.GetProfile(player)
	-- Only brand-new players qualify (your data layer sets IsNewPlayer on first-ever load).
	if not profile or profile.Data.IsNewPlayer ~= true then
		return
	end
	task.delay(QUALIFY_SECONDS, function()
		if player.Parent ~= Players then
			return -- left early: no payout
		end
		if claimReferral(player.UserId, referrer) then
			grant(player, INVITEE_REWARD)
			rewardInviter(referrer)
		end
	end)
end)
```
Notes:
- `IsNewPlayer` is a profile flag your data layer sets when the profile is created ([[Data-Persistence-DataStores-And-ProfileStore]]).
- The pending-reward flow is at-most-once: a crash between `RemoveAsync` and the grant loses that reward rather than duplicating it. For valuable rewards, write the reward into the profile inside a ProfileStore session instead.

### Share sheet from server (ServerScriptService, called on a client request)
```lua
--!strict
-- ServerScriptService/ShareLinks (ModuleScript)
local HttpService = game:GetService("HttpService")
local SocialService = game:GetService("SocialService")

local ShareLinks = {}

function ShareLinks.promptShare(player: Player, previewAssetId: number?)
	local options = {
		ExpirationSeconds = 7 * 86400,
		PreviewTitle = "Come raid my base!",
		PreviewDescription = "Join me and get a free Starter Crate",
		PreviewAssetId = previewAssetId,
		LaunchData = HttpService:JSONEncode({ r = "plot", u = player.UserId }),
	}
	local ok, result = pcall(function()
		return SocialService:PromptLinkSharingAsync(player, options)
	end)
	if not ok then
		warn("PromptLinkSharingAsync failed:", result)
	end
	return ok
end

return ShareLinks
```

## Loop design
1. **Trigger:** a peak moment or a co-op need ("This boss needs 2 players. Invite a friend?").
2. **Ask:** invite prompt with a clear mutual reward. The referral banner shows the same text.
3. **Land:** the invitee spawns next to the inviter (LaunchData/`SpawnNearUserId`) and skips straight into a shortened onboarding ([[Onboarding-And-First-60-Seconds]]).
4. **Bond:** the first 5 minutes are co-op (shared quest). This is also when the invitee qualifies.
5. **Reward + repeat:** both get rewarded with a toast. The inviter sees "2/5 friends invited today".

Benchmarks: Roblox publishes no invite-conversion benchmarks. ⚠️ verify: measure your own funnel (prompts shown → prompts sent [not observable per recipient] → `ReferredByPlayerId` joins → qualified) with custom events.

## Checklist
- [ ] Invite button in HUD/menu + contextual prompts at 2–3 peak moments (cap ~1 auto-prompt per session)
- [ ] Custom Notification string (`InviteMessageId`) created and localized
- [ ] Referral rewards via `ReferredByPlayerId`, with one-per-invitee, new-player-only, qualify timer and inviter caps
- [ ] Referral Rewards banner published and matching code
- [ ] Share links created per channel/creator. LaunchData perks only cosmetic/low value.
- [ ] Join routing: spawn invitee near inviter
- [ ] Funnel events logged ([[Analytics-And-Instrumentation]])

## Pitfalls
- Rewarding on `GameInvitePromptClosed`. Recipients are no longer reported, so this rewards spam-closing.
- Trusting LaunchData for rewards. It is spoofable and sometimes missing, and a `%` character can truncate it (DevForum reports).
- Rewarding the inviter for alts. Require a new player + qualify time + caps. Consider `Player.AccountAge` ≥ 1 day for high-value rewards. ⚠️ verify: whether this hurts genuine brand-new Roblox signups, which are prime referral targets.
- Showing the invite prompt on spawn. Players dismiss it and learn to ignore it.
- Using the deprecated `PromptLinkSharing`, or deep links instead of share links.
- Copy promising rewards for likes/favourites. These cannot be verified, and the sentiment backlash is real.

## Related
- [[Retention/_Index]] · [[Friend-And-Group-Play]] · [[Notifications-And-Re-Engagement]] · [[Onboarding-And-First-60-Seconds]] · [[Discovery-Algorithm]] · [[Analytics-And-Instrumentation]] · [[Data-Persistence-DataStores-And-ProfileStore]]

## Sources
- Roblox Creator Docs, "Player invite prompts", https://create.roblox.com/docs/production/promotion/invite-prompts (creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, "Friend referral system", https://create.roblox.com/docs/production/promotion/referral-system (accessed 2026-10-04)
- Roblox Creator Docs, "Share links", https://create.roblox.com/docs/production/promotion/share-links, and "Deep links" (deprecated), https://create.roblox.com/docs/production/promotion/deeplinks (accessed 2026-10-04)
- Roblox Engine API, `SocialService`, `ExperienceInviteOptions`, `Player:GetJoinData` (accessed 2026-10-04)
- DevForum, "SocialService:PromptGameInvite()'s LaunchData is unreliable", https://devforum.roblox.com/t/socialservicepromptgameinvites-launchdata-is-unreliable/2712751 (via search snippet, 2026-10-04)
