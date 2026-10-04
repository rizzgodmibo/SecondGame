---
tags: [retention/events]
status: draft
updated: 2026-10-04
confidence: medium
---
# Events and Seasons

## TL;DR
- **Run a cadence of nested time windows:** a weekly beat (weekend 2× / admin event / weekly leaderboard reset), a 2–4 week small update, a 2–3 month major update or season. The two update cadences come straight from Roblox's retention docs ([[Content-Cadence]], [[Live-Ops-Playbook]]).
- **Schedule from data, not code.** Keep event windows as UTC timestamps in **Experience Configs** (`ConfigService`), with a hardcoded fallback. Every server computes "is it active?" from `os.time()`. A deterministic schedule needs no cross-server messaging.
- **Use MessagingService only for ad-hoc live triggers** (admin abuse, surprise meteor). Broadcast `startsAt = os.time() + 10` so all servers start together, and write the active event to a MemoryStore HashMap so servers that boot mid-event join in. MessagingService messages are 1 kB max and delivery is best effort.
- **Register every event in Creator Hub → Events & Updates.** Events appear on the game page, players can RSVP ("Notify me") and get a stream/push notification at start, and joins carry `GetJoinData().GameJoinContext.EventId`. **1,000+ RSVPs and a start within the last 7 days** make the event eligible for the *Trending Events in Experiences* chart.
- **Season/battle pass:** 4–8 weeks, free and premium tracks, XP from dailies/weeklies, so a regular player finishes the premium track with about 1 week to spare. Rewards are cosmetic or convenience, and players can always catch up.
- **FOMO with ethics:** real deadlines only, no fake countdowns, no "buy in 10 minutes". Rotate limited items back eventually, or say plainly that they are exclusive. Roblox explicitly bans false time pressure in notifications.

## Event types and when to use them
| Type | Length | Primary goal | Notes |
|---|---|---|---|
| Weekend boost (2× XP/coins/luck) | Fri 00:00 → Mon 00:00 UTC | Weekend DAU, reactivation | Cheapest event. Announce through an update notification. |
| Admin abuse (live dev session) | 30–60 min, weekly, fixed time | CCU spikes, social buzz, RSVP growth | Grow a Garden vs Steal a Brainrot "Admin Abuse War" (2025-08-23) peaked at ~22.3M CCU for GaG, and Roblox hit a 47.3M platform record (Tubefilter, 2025-08-25) |
| Global timed event (meteor, boss, blood moon) | 5–15 min, every 1–2 h | Session length, "stay for the next one" | Deterministic schedule from `os.time()` |
| Limited-time holiday/seasonal | 7–30 days | New-user acquisition + returning users | Roblox: "best events run for 7–30 days" (Off-Platform Featuring guidance) |
| Collab / IP event | 1–3 weeks | Acquisition | Needs licensing. Submit for Off-Platform Featuring ≥ 7 days before start. |
| Season (pass + themed content) | 4–8 weeks | D30, monetisation | Weekly content drip inside the season |
| Competitive (weekly leaderboard) | 7 days | Engagement of top 10% | See [[Leaderboards]] |

Decision rules:
- Pre-launch / < 1k CCU → weekend boosts + one hourly global event. Admin abuse only once you can fill many servers (it cannibalises otherwise).
- 1k–20k CCU → weekly admin event at a fixed time (e.g. Sat 15:00 US-East), registered as a Roblox Event to collect RSVPs. Monthly themed event.
- Big games → seasons + weekly updates + admin events. Use Configs targeting and experiments for tuning ([[Live-Ops-Playbook]]).

## Roblox platform event features (verified 2026-10)
- **Create:** Creator Hub → Engagement → Events & Updates. Max **10 ongoing or upcoming** events. You can set the event place, and players joining from event surfaces spawn there.
- **Discovery:** game page Events section, event details page (shareable link), group/community page Events tab (can feature one in About), and the Trending Events chart (active event, started ≤ 7 days ago, ≥ 1,000 RSVPs, public).
- **Notifications:** RSVP'd players get a stream notification at start (plus optional push).
- **Update announcements:** 60 characters, max once every 3 days, sent to everyone who enabled notifications (including under-13s). See [[Notifications-And-Re-Engagement]].
- **In-game APIs** (`SocialService`): `GetUpcomingExperienceEventsAsync()` (active and upcoming events, soonest first), `GetExperienceEventAsync(eventId)`, `GetEventRsvpStatusAsync(eventId)`, `PromptRsvpToEventAsync(eventId)` (local player, event must not have started). Discover IDs at runtime and never hardcode them.
- **Attribution:** `player:GetJoinData().GameJoinContext.EventId` is present when the player joined via an event surface.
- **Off-Platform Featuring:** toggle "Submit for Featuring" when creating the event, ≥ 7 days before start. Roblox selects on DAU growth, playtime, retention and monetisation, and may feature it on App Store/Play Store.

## Code

### 1. Config-driven schedule + deterministic global event (ServerScriptService/EventScheduler, Script)
```lua
--!strict
-- ServerScriptService/EventScheduler (Script)
-- Publishes the current event state to clients via ReplicatedStorage attributes.
local ConfigService = game:GetService("ConfigService")
local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

type EventDef = { id: string, startUtc: number, endUtc: number, multiplier: number? }

-- Fallback if Configs are unreachable. DateTime.fromUniversalTime(y, m, d, h, min, s) -> UnixTimestamp
local FALLBACK_EVENTS: { EventDef } = {
	{
		id = "halloween_2026",
		startUtc = DateTime.fromUniversalTime(2026, 10, 24, 0, 0, 0).UnixTimestamp,
		endUtc = DateTime.fromUniversalTime(2026, 11, 7, 0, 0, 0).UnixTimestamp,
	},
}

-- Hourly meteor: starts at minute 0 of every hour, lasts 10 minutes.
local METEOR_PERIOD = 3600
local METEOR_DURATION = 600

local events: { EventDef } = FALLBACK_EVENTS

local function loadEventsFromConfig()
	local ok, snapshot = pcall(function()
		return ConfigService:GetConfigAsync()
	end)
	if not ok then
		warn("ConfigService unavailable, using fallback events")
		return
	end
	local function apply()
		-- Config key "event_schedule" (JSON): [{"id":"...","startUtc":..., "endUtc":..., "multiplier":2}]
		local raw = snapshot:GetValue("event_schedule")
		if typeof(raw) == "string" then
			local decodedOk, decoded = pcall(HttpService.JSONDecode, HttpService, raw)
			if decodedOk and typeof(decoded) == "table" then
				events = decoded :: { EventDef }
			end
		elseif typeof(raw) == "table" then
			events = raw :: { EventDef }
		end
	end
	apply()
	snapshot.UpdateAvailable:Connect(function()
		snapshot:Refresh()
		apply()
	end)
end

local function activeEvent(now: number): EventDef?
	for _, e in events do
		if now >= e.startUtc and now < e.endUtc then
			return e
		end
	end
	return nil
end

local function meteorState(now: number): (boolean, number)
	local intoPeriod = now % METEOR_PERIOD
	if intoPeriod < METEOR_DURATION then
		return true, METEOR_DURATION - intoPeriod -- active, seconds left
	end
	return false, METEOR_PERIOD - intoPeriod -- inactive, seconds until next
end

loadEventsFromConfig()

while true do
	local now = os.time()
	local e = activeEvent(now)
	ReplicatedStorage:SetAttribute("ActiveEventId", if e then e.id else "")
	ReplicatedStorage:SetAttribute("ActiveEventEndsAt", if e then e.endUtc else 0)
	ReplicatedStorage:SetAttribute("EventMultiplier", if e and e.multiplier then e.multiplier else 1)
	local meteorActive, secs = meteorState(now)
	ReplicatedStorage:SetAttribute("MeteorActive", meteorActive)
	ReplicatedStorage:SetAttribute("MeteorSeconds", secs)
	task.wait(1)
end
```
Clients read the attributes (`GetAttributeChangedSignal`) for banners and countdowns. Gameplay code on the server reads `EventMultiplier`, never a value from the client.

### 2. Admin-triggered global event (ServerScriptService/GlobalEvents, Script)
```lua
--!strict
-- ServerScriptService/GlobalEvents (Script)
local MessagingService = game:GetService("MessagingService")
local MemoryStoreService = game:GetService("MemoryStoreService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local TOPIC = "GlobalEvent"
local ADMINS: { [number]: boolean } = { [123456789] = true } -- replace with real UserIds
local stateMap = MemoryStoreService:GetHashMap("GlobalEventState")

type GlobalEvent = { id: string, startsAt: number, endsAt: number }

local function runEvent(ev: GlobalEvent)
	local delaySecs = math.max(0, ev.startsAt - os.time())
	task.delay(delaySecs, function()
		if os.time() >= ev.endsAt then
			return
		end
		ReplicatedStorage:SetAttribute("GlobalEventId", ev.id)
		ReplicatedStorage:SetAttribute("GlobalEventEndsAt", ev.endsAt)
		-- Spawn content here (boss, luck boost, weather...) based on ev.id
		task.delay(ev.endsAt - os.time(), function()
			if ReplicatedStorage:GetAttribute("GlobalEventId") == ev.id then
				ReplicatedStorage:SetAttribute("GlobalEventId", "")
			end
		end)
	end)
end

-- Late-joining servers: pick up an event that is already running.
task.spawn(function()
	local ok, ev = pcall(function()
		return stateMap:GetAsync("current")
	end)
	if ok and typeof(ev) == "table" and os.time() < (ev :: any).endsAt then
		runEvent(ev :: GlobalEvent)
	end
end)

local subOk, subErr = pcall(function()
	MessagingService:SubscribeAsync(TOPIC, function(message)
		local data = message.Data
		if typeof(data) == "table" and typeof(data.id) == "string" then
			runEvent(data :: GlobalEvent)
		end
	end)
end)
if not subOk then
	warn("GlobalEvent subscribe failed:", subErr)
end

-- Trigger (call from your admin command handler; verify sender server-side).
local function triggerGlobalEvent(sender: Player, id: string, durationSecs: number)
	if not ADMINS[sender.UserId] then
		return
	end
	local ev: GlobalEvent = {
		id = id,
		startsAt = os.time() + 10, -- give every server time to receive
		endsAt = os.time() + 10 + durationSecs,
	}
	pcall(function()
		stateMap:SetAsync("current", ev, durationSecs + 60)
	end)
	local ok, err = pcall(function()
		MessagingService:PublishAsync(TOPIC, ev)
	end)
	if not ok then
		warn("Publish failed:", err)
	end
end

Players.PlayerAdded:Connect(function(player)
	player.Chatted:Connect(function(msg)
		local dur = string.match(msg, "^/meteor (%d+)$")
		if dur then
			triggerGlobalEvent(player, "meteor", tonumber(dur) :: number)
		end
	end)
end)
```
`Player.Chatted` works with legacy and TextChatService chat for simple commands. ⚠️ verify: on TextChatService-only games, prefer `TextChatCommand` instances for admin commands.

MessagingService limits (docs, 2026-10): message ≤ **1 kB**; sends per server **600 + 240 × players/min**; receives per topic **40 + 80 × servers/min**; subscriptions per server **20 + 8 × players**. Keep topics few and messages tiny.

## Season / battle pass design
- **Length:** 4–8 weeks. Shorter seasons need more content, longer ones lose urgency. (Vault heuristic.)
- **Tracks:** a free track (every 2–3 tiers) and a premium track (every tier). Premium is a Game Pass or Developer Product scoped to the season ID. Store `SeasonId`, `SeasonXP` and `ClaimedTiers` (bitset/array) in the profile and reset lazily when `SeasonId` changes.
- **XP sources:** daily quests (largest), weekly challenges and plain play. Cap daily XP so no-lifers don't finish in 3 days. Target: a 4-day/week player finishes the premium track at ~85% of season length.
- **Catch-up:** XP boost in the last 2 weeks and purchasable tier skips (cosmetic-only seasons only).
- **Rewards:** exclusive cosmetics, titles, trails and pets with ≤ 1.1× power. Pay-to-win season rewards break the [[Leaderboards]] and PvP.
- Monetisation specifics (pricing, receipts) belong in the Monetisation folder. ⚠️ verify: Roblox Subscriptions eligibility if you sell a recurring pass.

## FOMO ethics (policy + practice)
- Roblox notification guidelines prohibit **false time pressure**, **disguised ads**, **bait-and-switch freebies** and **tricking users into purchases**. Apply the same bar to in-game UI, because a young audience amplifies the backlash.
- Countdown timers must match the real end time. Don't extend "last chance" events silently. Announce extensions.
- Limited paid items: either commit to "never returning" (a trading-value promise you must keep) or use a published rotation ("returns next year"). Breaking that promise destroys economy trust.
- Paid random items (crates/eggs bought with Robux) must respect `PolicyService:GetPolicyInfoForPlayerAsync().ArePaidRandomItemsRestricted` and disclosure rules. See the Monetisation notes.
- Give free players a meaningful slice of every event (free track, event currency from play).

## Checklist
- [ ] Event calendar for the next 8 weeks in the project doc (UTC times)
- [ ] Schedule stored in Configs with fallback constants. Tested with `ConfigService:SetTestingValue`.
- [ ] Each public event registered in Events & Updates with a unique thumbnail. RSVP prompt in-game before start.
- [ ] `GameJoinContext.EventId` read on join → spawn/route to event content
- [ ] Global triggers use `startsAt` + MemoryStore state for late servers
- [ ] Admin commands gated by a server-side UserId allowlist
- [ ] Event metrics: DAU, CCU peak, new-user D1 for the event cohort (cohort table), revenue per user
- [ ] FOMO copy reviewed against the guidelines above

## Pitfalls
- Hardcoding event IDs for `PromptRsvpToEventAsync`. They go stale when the event ends. Fetch them with `GetUpcomingExperienceEventsAsync()`.
- Assuming MessagingService reaches every server. New servers miss past messages, and delivery is not guaranteed.
- Starting events on `os.time()` in a local timezone mindset. All timestamps are UTC.
- Admin abuse events with no RSVP/notification funnel. You get the spike from players already in game and none from returning ones.
- Event currency that persists forever, which inflates the economy. Convert or expire at event end ([[Core-Loops]] economy notes).
- Too many simultaneous events. One headline event at a time, plus background weekly beats.

## Related
- [[Retention/_Index]] · [[Live-Ops-Playbook]] · [[Content-Cadence]] · [[Notifications-And-Re-Engagement]] · [[Leaderboards]] · [[Daily-Rewards-And-Streaks]] · [[Community-Management]] · [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]]

## Sources
- Roblox Creator Docs, "Experience events and updates", https://create.roblox.com/docs/production/promotion/experience-events (via creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, "Experience configs", https://create.roblox.com/docs/production/configs (accessed 2026-10-04)
- Roblox Engine API, `SocialService` (event RSVP APIs), `MessagingService` (limits table), `MemoryStoreHashMap`, `ConfigService`/`ConfigSnapshot` (accessed 2026-10-04)
- Roblox Creator Docs, "Retention → Improve day 30 retention" (2–4 week small updates, 2–3 month big updates), https://create.roblox.com/docs/production/analytics/retention (accessed 2026-10-04)
- Roblox Creator Docs, experience notification guidelines (deceptive nudge tactics), https://create.roblox.com/docs/production/promotion/experience-notifications (accessed 2026-10-04)
- Tubefilter, "Developer beef just helped Roblox set a 47-million-player record", https://www.tubefilter.com/2025/08/25/roblox-grow-garden-steal-brainrot-admin-war-record/ (2025-08-25). RTC on X, GaG peak 22,346,725 CCU.
