---
tags: [systems/api, systems/luau]
status: verified
updated: 2026-10-04
confidence: high
---
# Deprecated API Replacements

Generated from the deprecation tags and messages in the official `Roblox/creator-docs` engine reference (snapshot 2026-10-02).
Most tutorials, free models and AI training data still use the old calls. **Before writing or pasting any Roblox code,
check it against this table.** The repo had 423 deprecated members in total. Below are the ones a game is likely to touch.

## TL;DR
- Many yielding web calls gained an **`…Async`** name in 2025–26: group, friends, badges, character loading, product info, teleport
  reservations, humanoid descriptions, emotes. The old names are superseded, so always use the `Async` form.
- **Groups are multi-role now.** `GroupService:GetRolesInGroupAsync(userId, groupId)` supersedes `GetRankInGroupAsync` and
  `GetRoleInGroupAsync`. `Rank` no longer defines hierarchy, so gate admin and mod tools by **role `Id`**.
- **Premium → Roblox Plus:** use `MarketplaceService:PromptRobloxSubscriptionPurchase()` rather than `PromptPremiumPurchase`.
- Old engine globals `wait`/`spawn`/`delay` → `task.wait`/`task.spawn`/`task.delay`. Region3 and ray queries → `Raycast`/`GetPartBoundsInBox`.
- **Group membership caching:** results are cached per peer. After `GroupService:PromptJoinAsync` succeeds, only the **client's** cache is
  cleared, so the server still sees the old value. Re-check membership on rejoin, or keep a server-side cap.

## Players, social, groups
| Deprecated | Use instead |
|---|---|
| `Player:IsInGroup` | `Player:IsInGroupAsync` |
| `Player:GetRankInGroup` / `GetRankInGroupAsync` | `GroupService:GetRolesInGroupAsync(userId, groupId)` → `{ IsMember, Roles = { {Id, Name, Rank} } }` (highest role first) |
| `Player:GetRoleInGroup` / `GetRoleInGroupAsync` | `GroupService:GetRolesInGroupAsync` |
| `Player:IsFriendsWith` / `IsBestFriendsWith` | `Player:IsFriendsWithAsync` |
| `Player:GetFriendsOnline` | `Player:GetFriendsOnlineAsync` |
| `Player:LoadCharacter` | `Player:LoadCharacterAsync` |
| `Player:LoadCharacterWithHumanoidDescription` | `Player:LoadCharacterWithHumanoidDescriptionAsync` |
| `Player:Save*/Load*`, `DataReady`, `WaitForDataReady` | `DataStoreService` (see [[Data-Persistence-DataStores-And-ProfileStore]]) |
| `Players:GetHumanoidDescriptionFromUserId` / `FromOutfitId` | `…Async` versions |
| `Players:CreateHumanoidModelFromUserId` / `FromDescription` | `…Async` versions |
| `Players.NumPlayers` | `#Players:GetPlayers()` |
| `SocialService:PromptLinkSharing` | `SocialService:PromptLinkSharingAsync` (server-only) |

## Monetisation, badges, teleport
| Deprecated | Use instead |
|---|---|
| `MarketplaceService:GetProductInfo` | `MarketplaceService:GetProductInfoAsync` |
| `MarketplaceService:PlayerOwnsAsset` / `PlayerOwnsBundle` | `…Async` versions |
| `MarketplaceService:PromptPremiumPurchase` | `MarketplaceService:PromptRobloxSubscriptionPurchase` |
| `BadgeService:AwardBadge` / `UserHasBadge` | `AwardBadgeAsync` / `UserHasBadgeAsync` |
| `BadgeService:IsDisabled` | `GetBadgeInfoAsync(...).IsEnabled` |
| `TeleportService:ReserveServer` | `TeleportService:ReserveServerAsync` |
| `TeleportToPlaceInstance` / `TeleportToPrivateServer` / `TeleportToSpawnByName` / `TeleportPartyAsync` | `TeleportService:TeleportAsync` + `TeleportOptions` |
| `game.VIPServerId` / `VIPServerOwnerId` | `game.PrivateServerId` / `PrivateServerOwnerId` |
| `GlobalDataStore:OnUpdate` | `MessagingService` |
| `game.OnClose` | `game:BindToClose` |

## Characters, animation, physics
| Deprecated | Use instead |
|---|---|
| `Humanoid:LoadAnimation` / `AnimationController:LoadAnimation` | `Animator:LoadAnimation` |
| `Humanoid:ApplyDescription` / `ApplyDescriptionReset` | `…Async` versions |
| `Humanoid:PlayEmote` | `Humanoid:PlayEmoteAsync` |
| `BasePart.Velocity` / `RotVelocity` | `AssemblyLinearVelocity` / `AssemblyAngularVelocity` |
| `BasePart.Friction` / `Elasticity` / `SpecificGravity` | `CustomPhysicalProperties` |
| `BasePart:MakeJoints` / `BreakJoints` | `WeldConstraint` etc.; `GetJoints()` + `Destroy()` |
| `Model:SetPrimaryPartCFrame` / `GetPrimaryPartCFrame` / `GetModelCFrame` | `Model:PivotTo` / `GetPivot` |
| `Model:GetModelSize` | `Model:GetExtentsSize` |
| `PhysicsService:CreateCollisionGroup` / `RemoveCollisionGroup` / `GetCollisionGroups` | `workspace:RegisterCollisionGroup` / `UnregisterCollisionGroup` / `GetRegisteredCollisionGroups` |
| `PhysicsService:SetPartCollisionGroup` | `part.CollisionGroup = "Name"` |
| `FindPartOnRay*` | `workspace:Raycast(origin, dir, RaycastParams)` |
| `FindPartsInRegion3*` / `IsRegion3Empty*` | `workspace:GetPartBoundsInBox(cf, size, OverlapParams)` |
| `BodyVelocity` / `BodyGyro` / `BodyPosition` (legacy movers) | `LinearVelocity` / `AlignOrientation` / `AlignPosition` |

## UI, camera, audio, misc
| Deprecated | Use instead |
|---|---|
| `GuiObject:TweenPosition` / `TweenSize` / `TweenSizeAndPosition` | `TweenService` |
| `GuiObject.Draggable` / `DragBegin` / `DragStopped` | `UIDragDetector` |
| `GuiObject.Transparency` / `BackgroundColor` / `BorderColor` | `BackgroundTransparency` / `BackgroundColor3` / `BorderColor3` |
| `Camera:Interpolate` / `CoordinateFrame` | `TweenService` on `Camera.CFrame` / `Camera.CFrame` |
| `Sound.Pitch` | `Sound.PlaybackSpeed` |
| `Sound.MinDistance` / `MaxDistance` / `EmitterSize` | `RollOffMinDistance` / `RollOffMaxDistance` |
| `ContentProvider:Preload` | `ContentProvider:PreloadAsync` |
| `LocalizationService:GetTranslatorForPlayer` | `GetTranslatorForPlayerAsync` |
| `InsertService:Insert` | `InsertService:LoadAsset` |
| `Chat:FilterStringForPlayerAsync` | `TextService:FilterStringAsync` (TextChatService games) |
| `Instance:Remove` | `Instance:Destroy` |
| `UserInputService.ModalEnabled` | `GuiService.TouchControlsEnabled` |
| Global `wait` / `spawn` / `delay` | `task.wait` / `task.spawn` / `task.delay` |

## Admin and mod check (multi-role groups)
```lua
--!strict
-- ServerScriptService (shared helper)
local GroupService = game:GetService("GroupService")

local function hasAnyRole(player: Player, groupId: number, allowedRoleIds: { [number]: true }): boolean
	local ok, info = pcall(function()
		return GroupService:GetRolesInGroupAsync(player.UserId, groupId)
	end)
	if not ok or not info.IsMember then return false end
	for _, role in info.Roles do
		if allowedRoleIds[role.Id] then return true end
	end
	return false
end
```

## Regenerating this list
Clone `Roblox/creator-docs` (sparse checkout of `content/en-us/reference/engine`). Then collect every member that is tagged `Deprecated`
or has a non-empty `deprecation_message`, and grep the vault for those names.
As of 2026-10-04 the vault is clean, apart from mentions that explain the deprecation.

## Related
- [[Luau-Strict-Typing]] · [[Common-Libraries]] · [[Friend-And-Group-Play]] · [[Live-Ops-Playbook]] · [[Community-Management]] · [[Systems/_Index]]

## Sources
- Roblox/creator-docs engine reference YAML (`Player.yaml`, `GroupService.yaml`, `MarketplaceService.yaml`, `TeleportService.yaml`, etc.), snapshot 2026-10-02, read 2026-10-04. Mirrors https://create.roblox.com/docs/reference/engine
