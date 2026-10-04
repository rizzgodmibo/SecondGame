---
tags: [retention/notifications]
status: draft
updated: 2026-10-04
confidence: medium
---
# Notifications and Re-Engagement

## TL;DR
- **Four Roblox-native channels:** (1) **Experience Notifications**, personalised, per user, sent from your server, 13+ opted-in users only. (2) **Update announcements**: 60 chars, once per 3 days, to all opted-in users including under-13s. (3) **Event RSVP notifications**, sent automatically when an event you created starts. (4) **Friend invites/referrals** ([[Sharing-And-Referral-Loops]]). Off-platform: Discord and community announcements ([[Community-Management]]).
- **Hard limit: 1 Experience Notification per user per day per experience**, plus an aggregate daily cap across all experiences. A spam filter scales your reach with engagement, so a low click rate means less delivery. Send **only the single most valuable, personal and actionable** message per user per day.
- **Eligibility:** the game needs ≥ 100 visits and must not be under moderation, and you need manage permission. Notification strings are created in Creator Hub (Engagement → Notifications), max **99 chars**, with `{params}` and the title auto-set to the game name.
- **Get opt-ins in context:** after a daily claim or when starting a long timer, call `ExperienceNotificationService:CanPromptOptInAsync()` then `:PromptOptIn()` (client). Roblox shows the prompt at most **once per 30 days** per user, never to under-13s or already-opted-in users, and its text is fixed. Never gate gameplay on opting in.
- **Content that works:** async state changes the user caused ("Your Golden Egg hatched"), social rivalry ("{userId-friend} beat your record"), near-complete goals ("2 races left for the weekly chest"), time-relevant events the user signed up for. **Banned:** disguised ads, false time pressure, bait-and-switch freebies, tricking users into purchases.
- **Timers need a server that's alive when they fire.** Queue due notifications in a MemoryStore SortedMap (`sortKey = dueAt`) that any live server drains each minute, or send from an external cron through Open Cloud `POST /cloud/v2/users/{userId}/notifications`.

## Channel comparison
| Channel | Audience | Limit | Content | Setup |
|---|---|---|---|---|
| Experience Notification | 13+, opted in | 1/user/day/experience (+ global cap) | Personal, parameterised, LaunchData, analytics category | Luau OpenCloud package or Open Cloud REST |
| Update announcement | All opted-in (incl. < 13) | 60 chars, once / 3 days | Broad "what's new" | Creator Hub → Events & Updates (legacy updates form) |
| Event start (RSVP) | Users who clicked Notify Me / RSVP'd | Per event | Automatic at event start | Create Event + in-game `PromptRsvpToEventAsync` ([[Events-And-Seasons]]) |
| Friend invite | Friends of the player | Platform-controlled | `{displayName}` + `{experienceName}` | `PromptGameInvite` + `InviteMessageId` |
| Discord/Community | Opted-in community | Your choice | Patch notes, events, outages | [[Community-Management]] |

## Notification content rules
Good (personal, actionable, caused by the user's own past action):
- "Your {eggName} hatched! Come meet your new pet." (timer the user started)
- "{userId-friend} just beat your record on {trackName}. Time for revenge?" (friend rivalry. Needs a friendship, and the mentioned user's privacy must allow activity updates.)
- "You're {n} quests away from the weekly chest!" (goal gradient, sent ~24 h before weekly reset)
- "Your crops are ready. They wilt in 6 h." (only if wilting is a real mechanic)

Bad (Roblox guideline examples): "New cars just dropped, check them out!" (generic ad), "Buy in the next 10 minutes…" (false urgency), "Play now and get a free dog bed!" if conditions apply (bait-and-switch), and purely informational "It's been a few days…".

Priority order when several are pending for one user on one day: **social rivalry > user-started timer completion > near-complete goal > event start**. Send nothing if none apply.

Timing heuristics (vault, not Roblox numbers): send in the user's typical play hour (store `LastSessionHourUtc` in the profile), never more than once per day, and stop after 3 unclicked notifications in a row (track via launch data on rejoin).

## Code

### Opt-in prompt (StarterPlayerScripts/NotificationOptIn, LocalScript)
```lua
--!strict
-- StarterPlayer/StarterPlayerScripts/NotificationOptIn (LocalScript)
local ExperienceNotificationService = game:GetService("ExperienceNotificationService")

local function tryPromptOptIn()
	local ok, canPrompt = pcall(function()
		return ExperienceNotificationService:CanPromptOptInAsync()
	end)
	if ok and canPrompt then
		pcall(function()
			ExperienceNotificationService:PromptOptIn()
		end)
	end
end

ExperienceNotificationService.OptInPromptClosed:Connect(function()
	-- Log an analytics event; you are not told whether they accepted.
end)

-- Call in context: after a daily-reward claim, or when the player starts a 4 h egg timer.
local _ = tryPromptOptIn
```

### Sending (ServerScriptService/Notify, ModuleScript)
Requires the official **Open Cloud** package from the Creator Store (Toolbox → Creator Store → Packages → "Open Cloud"). Move the `OpenCloud` model into ServerScriptService.
```lua
--!strict
-- ServerScriptService/Notify (ModuleScript)
local ServerScriptService = game:GetService("ServerScriptService")
local OCUserNotification = require(ServerScriptService:WaitForChild("OpenCloud").V2.UserNotification) :: any

local Notify = {}

export type Param = { stringValue: string? , int64Value: number? }

function Notify.send(
	userId: number,
	messageId: string,
	params: { [string]: Param }?,
	launchData: string?,
	category: string?
): (boolean, number?)
	local payload: { [string]: any } = { messageId = messageId, type = "MOMENT" }
	if params then
		payload.parameters = params
	end
	if launchData then
		payload.joinExperience = { launchData = launchData } -- <= 200 bytes
	end
	if category then
		payload.analyticsData = { category = category }
	end
	local ok, result = pcall(OCUserNotification.createUserNotification, userId, { payload = payload })
	if not ok then
		return false, nil
	end
	-- 429 = user's throttle reached (1/day). Treat as "done for today", not an error.
	return result.statusCode == 200, result.statusCode
end

return Notify
```

### Due-time queue so timers fire while the player is offline (ServerScriptService/NotificationQueue, ModuleScript)
```lua
--!strict
-- ServerScriptService/NotificationQueue (ModuleScript). Require it once from a bootstrap Script so the drain loop starts.
-- Enqueue: NotificationQueue.schedule(userId, dueAtUnix, messageId, params, launchData, category)
-- Every live server drains due items once a minute; a claim step prevents double-sends.
local MemoryStoreService = game:GetService("MemoryStoreService")
local ServerScriptService = game:GetService("ServerScriptService")
local HttpService = game:GetService("HttpService")

local Notify = require(ServerScriptService.Notify)

local queue = MemoryStoreService:GetSortedMap("NotifyQueue")
local MAX_TTL = 3_888_000 -- 45 days, MemoryStore max

local NotificationQueue = {}

function NotificationQueue.schedule(userId: number, dueAt: number, messageId: string, params: any?, launchData: string?, category: string?)
	-- One pending notification per user+category; a newer one replaces the older.
	local key = `{userId}:{category or "default"}`
	local value = { u = userId, m = messageId, p = params, l = launchData, c = category, claimed = false }
	local ttl = math.clamp(dueAt - os.time() + 86400, 60, MAX_TTL)
	pcall(function()
		queue:SetAsync(key, value, ttl, dueAt)
	end)
end

local function claim(key: string): any?
	local claimedValue: any = nil
	local ok = pcall(function()
		queue:UpdateAsync(key, function(old: any, sortKey: any)
			if old == nil or old.claimed then
				return nil -- someone else has it
			end
			old.claimed = true
			claimedValue = old
			return old, sortKey
		end, 300)
	end)
	return if ok then claimedValue else nil
end

local function drain()
	local now = os.time()
	local ok, items = pcall(function()
		-- Ascending by sortKey (dueAt); stop at items due now. Bounds use {key=, sortKey=}.
		return queue:GetRangeAsync(Enum.SortDirection.Ascending, 50, nil, { sortKey = now + 1 })
	end)
	if not ok then
		return
	end
	for _, item in items do
		local v = claim(item.key)
		if v then
			Notify.send(v.u, v.m, v.p, v.l, v.c)
			pcall(function()
				queue:RemoveAsync(item.key)
			end)
		end
	end
end

task.spawn(function()
	while true do
		task.wait(60 + math.random() * 10) -- jitter so servers don't stampede
		drain()
	end
end)

return NotificationQueue
```
Bounds are exclusive tables with `key` and/or `sortKey`. The docs example sets both. ⚠️ verify: that a `sortKey`-only upper bound is accepted (test in Studio). If it is not, pass `{ key = "", sortKey = now + 1 }`. Above ~5k CCU, shard the map (`NotifyQueue_<userId % N>`).

### Open Cloud (external cron, e.g. a daily "weekly challenge almost done" job)
```bash
curl -X POST "https://apis.roblox.com/cloud/v2/users/${USER_ID}/notifications" \
  -H "x-api-key: ${API_KEY}" -H "Content-Type: application/json" \
  -d '{"source":{"universe":"universes/'"${UNIVERSE_ID}"'"},
       "payload":{"message_id":"'"${ASSET_ID}"'","type":"MOMENT"},
       "analytics_data":{"category":"weekly_nudge"}}'
```
⚠️ verify: the API key permission scope name for user notifications in Creator Hub → API Keys.

## Analytics
- Creator Hub → Engagement → Notifications → **Analytics** tab: opted-in users (counts under-13s who only receive update announcements), plus impressions, clicks, etc. per string/category. Needs ≥ 100 aggregate impressions to show stats.
- Tag every send with `analyticsData.category`, and put `{n:"<category>"}` in `launchData` so rejoins are attributable in-game via `GetJoinData().LaunchData`.
- Success metric: reactivation of lapsed users (Analytics user segments: *Lapsed → Reactivated*) and D7 of opted-in vs non-opted-in.

## Roblox's own re-engagement surfaces
- **Continue Playing** row on Home, plus friends' activity (Friends list with Join). You influence these through session quality and co-play ([[Discovery-Algorithm]]).
- **Event tiles/RSVP** on the game page and the Trending Events chart ([[Events-And-Seasons]]).
- **Favourites/Follows:** players who favourite the game can find it easily. ⚠️ verify: whether favourites/follows still drive update notifications separately from the notification opt-in.

## Checklist
- [ ] Game ≥ 100 visits. Notification strings created (≤ 99 chars, params, `{experienceName}` if used).
- [ ] Opt-in prompt wired to 2–3 high-intent moments. No gating.
- [ ] Each string tagged with an analytics category. LaunchData routes the player to the relevant spot.
- [ ] Per-user daily priority selection (1/day). Unclicked back-off.
- [ ] Offline timer queue or external cron
- [ ] Update announcements for major updates only (≤ 1 per 3 days, specific copy, not "bug fixes")
- [ ] Copy reviewed against the deceptive-nudge rules

## Pitfalls
- Sending generic "come back!" pushes. Engagement-based throttling then cuts your reach for good messages too.
- Assuming delivery. Non-delivery happens for not opted in, throttled, moderated string, bad params, friend-mention rules, and more.
- User-mention strings to non-friends are silently dropped.
- Relying on notifications for under-13s. They only get update announcements and event notifications.
- Hardcoding an Open Cloud API key in a place file. Keep it in Secrets (`HttpService:GetSecret`) or off-platform.

## Related
- [[Retention/_Index]] · [[Daily-Rewards-And-Streaks]] · [[Events-And-Seasons]] · [[Sharing-And-Referral-Loops]] · [[Community-Management]] · [[Live-Ops-Playbook]] · [[Analytics-And-Instrumentation]] · [[Retention-Metrics-D1-D7-D30]]

## Sources
- Roblox Creator Docs, "Experience notifications" (eligibility, guidelines, delivery system, analytics, Luau package API), https://create.roblox.com/docs/production/promotion/experience-notifications (creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, Open Cloud "User notifications" guide, https://create.roblox.com/docs/cloud/guides/experience-notifications (accessed 2026-10-04)
- Roblox Engine API, `ExperienceNotificationService` (`CanPromptOptInAsync`, `PromptOptIn`, `OptInPromptClosed`) (accessed 2026-10-04)
- Roblox Creator Docs, "Experience events and updates" (update announcements: 60 chars, once / 3 days), https://create.roblox.com/docs/production/promotion/experience-events (accessed 2026-10-04)
- DevForum, "Updates to Notification Rate Limits" (relaxed from 1 per 3 days to 1 per day), https://devforum.roblox.com/t/updates-to-notification-rate-limits/3007106 (2024; via search snippet)
- DevForum, "Introducing In-Experience Notification Permission Prompts", https://devforum.roblox.com/t/introducing-in-experience-notification-permission-prompts/2909125
