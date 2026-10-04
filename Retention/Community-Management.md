---
tags: [retention/community]
status: draft
updated: 2026-10-04
confidence: medium
---
# Community Management

## TL;DR
- **Own three channels from day one:** the Roblox **Community** (formerly Groups, renamed Nov 2024: shouts, events tab, membership perks), a **Discord** server (13+, for your core players and testers), and the **game page** (description changelog, social links, events). Under-13 players mostly see only Roblox-native surfaces, so never put critical info only on Discord.
- **Social links:** up to 7 types (Facebook, X/Twitter, YouTube, Twitch, Discord, Guilded, Roblox community), each once, set in Creator Hub → Engagement → Social Links. Adding or seeing them requires age verification as **16+**. **You may not show social links inside the game.** Only "links on our game's page" phrasing is allowed.
- **Close the feedback loop weekly:** read the Feedback dashboard (votes + filtered comments), add an in-game feedback button (`SocialService:PromptFeedbackSubmissionAsync`, 1 submission/day/player), triage the Discord bug channel, then ship and credit it in the update log ("Fixed X, reported by the community").
- **Use an in-game "What's new" panel** on the first join after each version (store `LastSeenVersion` in the profile), mirrored to Discord #updates and the game description. Use update announcements only for big updates (60 chars, ≤ 1 per 3 days).
- **Outages/rollbacks:** acknowledge within 30 min on every channel, give an ETA or next-update time, never blame Roblox without checking status.roblox.com, and compensate in a predictable way (a global gift via Configs). Restore individual data with DataStore versioning (`ListVersionsAsync`/`GetVersionAtTimeAsync`) or ProfileStore version queries.
- **Toxicity:** rely on platform filtering (TextChatService), add in-game mute/report UX, give trusted moderators rank-gated tools (`GetRankInGroupAsync`), and ban with `Players:BanAsync` (supports `ExcludeAltAccounts`). Publish clear rules and an appeals path.

## Channel roles
| Channel | Audience | Use for | Cadence |
|---|---|---|---|
| In-game (What's new, banners, NPC board) | Everyone, all ages | Patch notes, events, outage notices, codes | Every update |
| Game page description + Events | Everyone browsing | Changelog top 3 lines, upcoming event tiles | Every update |
| Roblox Community (group) | Members (all ages) | Shouts, events, member perks, roles for testers/mods | 1–3×/week |
| Update announcement notification | Opted-in users | Major updates only | ≤ 1 per 3 days ([[Notifications-And-Re-Engagement]]) |
| Discord | 13+ core fans | Sneak peeks, polls, bug reports, trading, tester access | Daily presence |
| YouTube/TikTok/X | Acquisition + hype | Trailers, update teasers, creator collabs | Per update |

Decision rules:
- < 1k CCU: one dev runs Discord. Set 3 channels (#announcements, #bug-reports, #suggestions) and 1–2 volunteer mods.
- 1k–20k CCU: 1 volunteer mod per ~1–2k active Discord members, plus a community manager role. ⚠️ verify: heuristic, not a platform number.
- Large: paid community manager, structured QA tester group, a status channel, a support-ticket bot.

## Update logs that retain
- Lead with **player-visible** changes ("New zone: Frost Peaks, 12 pets, ice boss"). Fixes go last. "Bug fixes" alone is useless (Roblox's own announcement guidance).
- Version string in a shared module (`ReplicatedStorage/Shared/Version`). On join, compare it with `profile.Data.LastSeenVersion` and show the panel once.
- Countdown to the next update on the game page title or thumbnail, e.g. "[UPDATE 12]". ⚠️ verify: current title-tag rules in Growth/Discovery notes ([[Discovery-Algorithm]]).
- Keep a fixed release day/time (e.g. Saturday 10:00 US-East) so the community gathers ([[Content-Cadence]], [[Live-Ops-Playbook]]).

## Feedback loops
1. **Collect:** Feedback dashboard (Creator Hub → Audience → Feedback; votes since 2025-02-01, comments since 2025-03-17, comments are text-filtered), the in-game feedback prompt, Discord #suggestions with reaction voting, and analytics funnels ([[Analytics-And-Instrumentation]]).
2. **Triage weekly:** tag crash / data loss / exploit / balance / content request. Data loss and exploits are P0.
3. **Decide publicly:** a "Planned / Considering / Not planned" board in Discord.
4. **Ship + credit** in the update log. Players who see their suggestion shipped become advocates.
5. **Measure:** upvote % trend after each update (Feedback chart), plus D1/D7 cohort change ([[Retention-Metrics-D1-D7-D30]]).

```lua
--!strict
-- StarterPlayer/StarterPlayerScripts/FeedbackButton (LocalScript)
-- Opens Roblox's native feedback dialog. Does not work in Studio; test in a published game.
local SocialService = game:GetService("SocialService")

local function openFeedback()
	task.spawn(function()
		local ok, err = pcall(function()
			SocialService:PromptFeedbackSubmissionAsync({ FeedbackType = Enum.FeedbackType.Feedback })
		end)
		if not ok then
			warn("Feedback prompt failed:", err)
		end
	end)
end

local _ = openFeedback -- wire to a "Send feedback" button in settings
```
`Enum.FeedbackType.PlayerSupport` (support tickets: bug, data restore, purchasing) is **alpha, select experiences only** (2026-10).

## Moderation and toxicity
- **Chat:** keep TextChatService with Roblox filtering. Any user-generated text you display (pet names, sign text) must go through `TextService:FilterStringAsync`. Policy details live in the Operations moderation notes.
- **In-game tools for mods:** gate commands on group rank, checked server-side:
```lua
--!strict
-- ServerScriptService/ModTools (Script)
local Players = game:GetService("Players")
local GROUP_ID = 0
local GroupService = game:GetService("GroupService")
local MOD_ROLE_IDS: { [number]: true } = {} -- role Ids of your Moderator/Admin roles (Rank no longer defines hierarchy)

local function isMod(player: Player): boolean
	-- GroupService:GetRolesInGroupAsync supersedes Player:GetRankInGroupAsync (multi-role groups)
	local ok, info = pcall(function()
		return GroupService:GetRolesInGroupAsync(player.UserId, GROUP_ID)
	end)
	if not ok or not info.IsMember then return false end
	for _, role in info.Roles do
		if MOD_ROLE_IDS[role.Id] then return true end
	end
	return false
end

Players.PlayerAdded:Connect(function(player)
	player:SetAttribute("IsMod", isMod(player))
end)
-- Every mod remote/command checks player:GetAttribute("IsMod") == true on the server.
```
- **Bans:** `Players:BanAsync` (universe-wide, duration, display reason + private reason, `ExcludeAltAccounts`). Log every ban with the moderator ID. Offer appeals via Discord or the support ticket flow.
- **Discord:** AutoMod keyword and link filters, verification level ≥ "Medium", no DMs-from-server-members by default for minors' safety, and a strict no-off-platform-trading / no-account-sharing rule (scams).
- **Never** run giveaways that require following external accounts or that involve Robux transfers outside Roblox systems. ⚠️ verify: current Roblox Terms/Community Standards on off-platform giveaways and promo codes.

## Communicating outages and rollbacks
**Template (post on Discord, Community shout, in-game banner via Configs):**
> ⚠️ We know about [symptom: data not loading / purchases delayed] since [time UTC]. Your data is safe. [If a rollback:] we restored all players to [time UTC]. Anything bought with Robux after that will be re-granted automatically. Next update by [time UTC]. Everyone online during [window] gets [compensation] on the next join.

Playbook:
1. **Detect:** analytics alerts on DAU/CCU/errors (Creator Hub → Analytics → Alerts), DataStore error-rate dashboards, Discord reports.
2. **Check platform:** status.roblox.com and DevForum announcements. If Roblox is down, say so plainly and don't promise ETAs you don't control.
3. **Stop the bleeding:** a feature kill-switch via **Configs** (`ConfigService`, publish in ~15 s–1 min, no server restart) ([[Events-And-Seasons]] shows the pattern). Close trading if dupes are suspected.
4. **Restore:** per-player restore from DataStore versions (`DataStore:GetVersionAtTimeAsync`) or ProfileStore version queries ([[Data-Persistence-DataStores-And-ProfileStore]]). Re-grant Robux purchases from your purchase-history records, which are the source of truth for receipts.
5. **Compensate:** a global gift keyed by an incident ID (`ClaimedCompensations[incidentId] = true`) so it is granted once per player.
6. **Post-mortem** within 72 h, posted publicly in short form (Operations post-mortem notes).

Server restarts for updates: announce in-game 2–5 min ahead (MessagingService broadcast, a 1 kB message), then use Creator Hub "Restart servers" or migrate-to-latest. ⚠️ verify: current name of the "Migrate to latest update" option and soft-shutdown best practice.

## Checklist
- [ ] Community created and linked. Roles: Owner, Dev, Mod, Tester, Member.
- [ ] Social links configured (requires a 16+ age-verified owner/collaborator). No links in-game.
- [ ] Discord with #announcements, #updates, #bug-reports, #suggestions, #trading (if applicable). AutoMod on. Mod team briefed.
- [ ] In-game What's New panel + feedback button + version string
- [ ] Weekly feedback triage ritual. Public roadmap board.
- [ ] Outage template + compensation mechanism + kill-switch configs prepared before launch
- [ ] Mod tools gated by group rank. Ban logging.

## Pitfalls
- Putting "join our Discord discord.gg/…" text or QR codes in-game. That violates the Community Standards guideline on social links.
- Running the community only on Discord. Most of a young audience never sees it.
- Silence during outages. Rumours ("game deleted", "everyone wiped") spread faster than fixes.
- Promising features with dates you miss. Say "next update" or "soon™" only when confident.
- Volunteer mods with in-game power and no audit log. Abuse scandals destroy trust.
- Leaking unreleased content to testers without an NDA-style rule and role separation.

## Related
- [[Retention/_Index]] · [[Notifications-And-Re-Engagement]] · [[Events-And-Seasons]] · [[Live-Ops-Playbook]] · [[Content-Cadence]] · [[Friend-And-Group-Play]] · [[Analytics-And-Instrumentation]] · [[Data-Persistence-DataStores-And-ProfileStore]]

## Sources
- Roblox Creator Docs, "Social media links" (16+ verification, in-game prohibition, 7 types), https://create.roblox.com/docs/production/promotion/social-media-links (creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, "Feedback" dashboard, https://create.roblox.com/docs/production/analytics/feedback (accessed 2026-10-04)
- Roblox Engine API, `SocialService:PromptFeedbackSubmissionAsync` (1/day, PlayerSupport alpha), `Players:BanAsync` (`ExcludeAltAccounts`), `Player:GetRankInGroupAsync`, `DataStore:GetVersionAtTimeAsync`/`ListVersionsAsync` (accessed 2026-10-04)
- Roblox Creator Docs, "Experience configs", https://create.roblox.com/docs/production/configs (accessed 2026-10-04)
- Roblox Creator Docs, "Experience events and updates" (update announcement guidance), https://create.roblox.com/docs/production/promotion/experience-events (accessed 2026-10-04)
- DevForum, "Introducing Roblox Communities", https://devforum.roblox.com/t/introducing-roblox-communities/3268307 (2024-11)
