---
tags: [visuals/ui, visuals/cross-platform]
status: draft
updated: 2026-10-04
confidence: medium
---
# UI Layout and Device Scaling

Roblox traffic is majority mobile (⚠️ verify: current device split in your game's Analytics → Audience; historically ~55–65% phone/tablet). Design for a **landscape phone first**, then check tablet, PC, and console (10-foot UI).

## TL;DR
- **Size with Scale, lock shape with `UIAspectRatioConstraint`**, fine-tune with Offset only for paddings/strokes. Position via `AnchorPoint` + Scale (e.g. `AnchorPoint (1,1)`, `Position (1,-16,1,-16)` for a bottom-right element).
- **One `UIScale` per ScreenGui**, driven by viewport size and `GuiService.ViewportDisplaySize` (Small/Medium/Large), clamped so touch targets never drop below ~44 px and TV UI doesn't balloon.
- **Lay out with `UIListLayout` + `UIFlexItem`** (flex grow/shrink/fill) instead of manual positions; use `UIGridLayout` for inventories, `AutomaticSize` for text-driven boxes.
- **Respect safe areas**: `ScreenInsets = CoreUISafeInsets` for anything interactive; keep primary buttons out of the bottom-left (thumbstick) and bottom-right (jump) reserved zones but **near** them (thumb reach).
- **Gamepad**: every interactive element `Selectable = true`, set `GuiService.SelectedObject` when a menu opens, use `SelectionGroup` on containers; test with the Studio Controller Emulator.
- **Text**: `TextScaled = true` + `UITextSizeConstraint` (min ~14, max ~48) for labels; body text min ~14 px on phone. Honour `GuiService.PreferredTextSize`.

## Scale vs Offset decision table

| Need | Use |
|---|---|
| Panel that should cover X% of screen | `Size = UDim2.fromScale(0.5, 0.6)` + `UIAspectRatioConstraint` |
| Square icon/button | `Size = UDim2.fromScale(0.08, 0.08)` + `UIAspectRatioConstraint{AspectRatio=1, DominantAxis=Height}` (Height-dominant keeps size tied to the short side in landscape) |
| Padding, gaps, strokes, corner radius | Offset (`UDim.new(0, 8)`) — then scaled globally by `UIScale` |
| Lists whose length varies | `UIListLayout` + `AutomaticSize = Y` on the container, or a `ScrollingFrame` with `AutomaticCanvasSize = Y` |
| Element pinned to a corner | `AnchorPoint` equal to the corner (0/1) + matching Scale position + small negative Offset margin |

`UIAspectRatioConstraint` properties: `AspectRatio` (width/height), `AspectType` (`FitWithinMaxSize` / `ScaleWithParentSize`), `DominantAxis` (`Width`/`Height`). Use `UISizeConstraint` (MinSize/MaxSize in px) to cap panels on 4K TVs.

## Layout components

| Component | Use for | Key props |
|---|---|---|
| `UIListLayout` | Rows/columns, toolbars, menus | `FillDirection`, `Padding`, `HorizontalAlignment`/`VerticalAlignment`, `SortOrder = LayoutOrder`, **flex**: `HorizontalFlex`/`VerticalFlex` (`None/Fill/SpaceAround/SpaceBetween/SpaceEvenly`), `ItemLineAlignment`, `Wraps` |
| `UIFlexItem` (child of an item in a list layout) | Make one item grow/shrink | `FlexMode` (`None/Grow/Shrink/Fill/Custom`), `GrowRatio`, `ShrinkRatio`, `ItemLineAlignment` |
| `UIGridLayout` | Inventory/shop grids | `CellSize` (use Scale), `CellPadding`, `FillDirectionMaxCells`; pair with `UIAspectRatioConstraint` on the grid itself for square cells |
| `UITableLayout` | Leaderboards/stat tables | rows = children, columns = grandchildren |
| `UIPageLayout` | Swipeable tutorial pages, shop tabs | `Animated`, `TweenTime`, `:JumpTo()` |
| `UIPadding` | Inner margins | Offset values, scaled by UIScale |

Rule: a container has **one** layout object; nest frames for mixed layouts. Always set `LayoutOrder` explicitly (don't rely on Name sort).

## Device scaling module

```lua
--!strict
-- StarterPlayerScripts/UIScaleController.client.luau
-- Applies a UIScale to every ScreenGui tagged "AutoScale". Design all Offset values at 1280x720.
local CollectionService = game:GetService("CollectionService")
local GuiService = game:GetService("GuiService")
local Workspace = game:GetService("Workspace")

local REFERENCE = Vector2.new(1280, 720)
local MIN_SCALE = 0.75 -- below this, 44px touch targets designed at 1280x720 become too small
local MAX_SCALE = 1.6 -- cap for 4K / TV

local DISPLAY_MULTIPLIER: { [Enum.DisplaySize]: number } = {
	[Enum.DisplaySize.Small] = 1.15, -- phones/tablets: slightly larger for fingers
	[Enum.DisplaySize.Medium] = 1.0, -- laptops/monitors
	[Enum.DisplaySize.Large] = 1.1, -- TVs: viewed from far away
}

local function computeScale(): number
	local camera = Workspace.CurrentCamera
	if not camera then
		return 1
	end
	local viewport = camera.ViewportSize
	local raw = math.min(viewport.X / REFERENCE.X, viewport.Y / REFERENCE.Y)
	local multiplier = DISPLAY_MULTIPLIER[GuiService.ViewportDisplaySize] or 1
	return math.clamp(raw * multiplier, MIN_SCALE, MAX_SCALE)
end

local function apply(gui: Instance)
	local uiScale = gui:FindFirstChildOfClass("UIScale")
	if not uiScale then
		local created = Instance.new("UIScale")
		created.Parent = gui
		uiScale = created
	end
	(uiScale :: UIScale).Scale = computeScale()
end

local function applyAll()
	for _, gui in CollectionService:GetTagged("AutoScale") do
		apply(gui)
	end
end

CollectionService:GetInstanceAddedSignal("AutoScale"):Connect(apply)
GuiService:GetPropertyChangedSignal("ViewportDisplaySize"):Connect(applyAll)

local function hookCamera()
	local camera = Workspace.CurrentCamera
	if camera then
		camera:GetPropertyChangedSignal("ViewportSize"):Connect(applyAll)
	end
	applyAll()
end
Workspace:GetPropertyChangedSignal("CurrentCamera"):Connect(hookCamera)
hookCamera()
```

Notes:
- Apply `UIScale` only to **Offset-designed** trees. Scale-sized elements are already proportional; scaling them again double-scales. A common hybrid: Scale for big panels, Offset (× UIScale) for buttons/icons/text.
- Alternative without code: UI Styling **style queries** (`@ViewportDisplaySizeSmall`, `@PreferredInputTouch`) swapping size tokens — see [[UI-Architecture]].

## Safe areas, insets, reserved zones
- `ScreenGui.ScreenInsets`: `None` (full screen incl. notch), `DeviceSafeInsets` (avoid notches/rounded corners), `CoreUISafeInsets` (also avoid Roblox top-bar buttons) — **default for interactive UI**, `TopbarSafeInsets` (area inside the top bar, for buttons that sit beside Roblox's).
- `GuiService:GetGuiInset()` returns top-left/bottom-right inset `Vector2`s; `GuiService:GetInsetArea(Enum.ScreenInsets.CoreUISafeInsets)` returns a `Rect`.
- Mobile default controls occupy the **bottom-left (thumbstick) and bottom-right (jump)** — never put info there. Place custom action buttons in an arc *around* the jump button (Roblox's docs show positioning relative to `PlayerGui...JumpButton`).
- **Thumb reach**: a button 40% from the top is reachable on a phone but not on a tablet → anchor gameplay buttons to the bottom-right corner with Offset, not a screen percentage.
- Use `UserInputService.PreferredInput` (`KeyboardAndMouse`, `Gamepad`, `Touch`, `MicroGamepad`) to switch button prompts/glyphs; listen for changes (players plug in controllers mid-session). Prefer it over `TouchEnabled` checks.

## Touch target sizes
- Roblox docs give no official minimum. Use platform norms: **≥44×44 pt** (Apple HIG) / **≥48×48 dp** (Material) with **≥8 px** spacing. ⚠️ verify: that Roblox `AbsoluteSize` on iOS/Android is in logical points (DPI-independent), so these numbers map 1:1 — test on a real device with `print(camera.ViewportSize)`.
- Primary CTAs (Play, Buy, Claim): ≥64 px tall on phone. Close buttons: ≥44 px hit area even if the X icon is smaller (wrap the icon in a larger transparent `ImageButton`).

## Console / gamepad selection
- `GuiObject.Selectable`, `SelectionOrder` (lower first), `NextSelectionUp/Down/Left/Right` for explicit links, `SelectionImageObject` for a custom highlight (reuse one styled Frame), `GuiBase2d.SelectionGroup = true` + `SelectionBehavior*` (`Escape`/`Stop`) to trap focus in a modal.
- On menu open: `GuiService.SelectedObject = firstButton`; on close: `nil`. `GuiService:Select(container)` picks the best child.
- `GuiService.GuiNavigationEnabled`, `AutoSelectGuiEnabled` control the default navigation; `GuiService:IsTenFootInterface()` → true on console.
- Console text: body ≥ 24 px at 1080p (10-foot UI). Avoid hover-only affordances (no hover on gamepad/touch).

## Text scaling
- Labels: `TextScaled = true` **plus** `UITextSizeConstraint` (`MinTextSize` 14, `MaxTextSize` 36–48) so text doesn't become unreadable or huge.
- Paragraphs: fixed `TextSize` × UIScale + `TextWrapped = true` + `AutomaticSize = Y` (TextScaled on paragraphs causes inconsistent sizes between boxes).
- Keep all text in a family at the **same size**: TextScaled per-label gives "ransom-note" size mismatch; group them under one constraint value.
- Accessibility: `GuiService.PreferredTextSize` (`Medium` default, `Large`, `Larger`, `Largest`) scales engine text; a `UITextSizeConstraint` will clamp it, so set Max high enough. `GuiService.PreferredTransparency` — multiply background transparency by it. `GuiService.ReducedMotionEnabled` — skip positional tweens (see [[UI-Polish-And-Juice]]).
- Localisation: leave ~30% horizontal slack for German/Portuguese; `AutoLocalize = true` by default.
- Contrast: text vs background ≥ 4.5:1 (WCAG AA) — Roblox accessibility docs ask for "sufficient contrast"; add a `UIStroke` (Thickness 1.5–2, `ApplyStrokeMode = Contextual`) on text over 3D world.

## Checklist
- [ ] Tested in Device Emulator: iPhone SE-class (small landscape), modern phone, iPad, 1080p, 4K TV, portrait if `ScreenOrientation` allows
- [ ] All interactive UI uses `CoreUISafeInsets`; nothing under thumbstick/jump zones
- [ ] Touch targets ≥44 px, primary CTAs ≥64 px on phone
- [ ] Every menu gamepad-navigable with an initial selection and a Back binding
- [ ] Text has min/max constraints; no TextScaled paragraphs
- [ ] UI works when PreferredTextSize = Largest

## Pitfalls
- Pure Scale sizing without aspect constraints → squashed square icons on ultrawide/tall phones.
- UIScale on a Scale-sized tree → double-scaling, giant UI on TVs.
- `IgnoreGuiInset = true` on the HUD → coins counter hidden under the Roblox menu button.
- Hover-only tooltips → invisible to ~60% of players (touch) and console players.
- Designing at 1920×1080 on a PC monitor and never opening the emulator — the #1 cause of unusable mobile UI.
- `ScrollingFrame` without `AutomaticCanvasSize` → contents cut off on small screens.

## Related
- [[Visuals/_Index]] · [[UI-Architecture]] · [[UI-Polish-And-Juice]] · [[Art-Direction]]
- [[Onboarding-And-First-60-Seconds]]

## Sources
- Position and size, reserved zones, thumb zones — https://create.roblox.com/docs/ui/position-and-size
- Size modifiers (UIAspectRatioConstraint, UISizeConstraint, UITextSizeConstraint, UIScale) — https://create.roblox.com/docs/ui/size-modifiers
- List and flex layouts — https://create.roblox.com/docs/ui/list-flex-layouts ; grid/table — https://create.roblox.com/docs/ui/grid-table-layouts
- Cross-platform design (ViewportDisplaySize, PreferredInput, style queries) — https://create.roblox.com/docs/projects/cross-platform
- Accessibility (PreferredTextSize, PreferredTransparency, ReducedMotionEnabled, contrast) — https://create.roblox.com/docs/production/publishing/accessibility
- API: GuiService, ScreenGui, GuiObject, UIFlexItem, enums ScreenInsets/DisplaySize/PreferredInput/UIFlexMode — https://create.roblox.com/docs/reference/engine/classes/GuiService (all checked via Roblox/creator-docs GitHub source, 2026-10-02 commit)
- Apple HIG hit targets (44pt) — https://developer.apple.com/design/human-interface-guidelines/accessibility ; Material touch targets (48dp) — https://m3.material.io/foundations/designing/structure
