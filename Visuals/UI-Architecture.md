---
tags: [visuals/ui, systems/architecture]
status: draft
updated: 2026-10-04
confidence: medium
---
# UI Architecture

How to organise Roblox UI so it scales from a 5-screen prototype to a 60-screen live game without rewrites: container layout, ScreenGui properties, state-driven rendering, and component patterns.

## TL;DR
- **One ScreenGui per layer, not per screen**: `HUD` (DisplayOrder 0), `Menus` (10), `Popups` (20), `Toasts` (30), `Overlay/Transitions` (100). Every ScreenGui: `ResetOnSpawn = false`, `ZIndexBehavior = Sibling`, `ScreenInsets = CoreUISafeInsets`.
- **Build UI from code or from templates in ReplicatedStorage**, mounted by a LocalScript in `StarterPlayerScripts`. Do **not** keep live UI in `StarterGui` with `ResetOnSpawn = true` (state is wiped every death).
- **State drives UI, never the reverse.** Server data → client store → UI observes. A button only *requests* an action (RemoteEvent); it never mutates the displayed balance itself.
- **Library choice**: React-lua for big teams/long-lived games (mature, used internally by Roblox); Fusion or Vide for small teams wanting less boilerplate; a ~40-line `Value`/observe helper (below) is enough for games with < ~15 screens.
- **One router owns "which menu is open"** — opening a menu closes others, blurs/dims the world, disables gameplay input, and sets gamepad selection.
- Use engine **UI Styling** (`StyleSheet` / `StyleRule` / `StyleLink` + tokens) for colours, fonts and per-device sizes instead of hard-coding them in each component.

## Container hierarchy

```
StarterPlayerScripts/
  UIClient.client.luau        -- boots the app, owns the router
ReplicatedStorage/
  Shared/UI/
    Value.luau                 -- reactive state primitive (below)
    Router.luau                -- open/close menus, history, input lock
    Components/                -- Button, CurrencyCounter, Modal, Toast...
    Screens/                   -- ShopScreen, InventoryScreen... (functions returning instances)
  UITemplates/                 -- designer-built Frames cloned by components (optional)
PlayerGui (runtime)
  HUD        DisplayOrder 0
  Menus      DisplayOrder 10
  Popups     DisplayOrder 20
  Toasts     DisplayOrder 30
  Overlay    DisplayOrder 100  -- fades, loading screen, cutscene bars
```

Decision rules:
- **Few ScreenGuis**: each ScreenGui is a separate render layer and ordering scope; >10 visible ScreenGuis makes ordering bugs likely. Toggle `Enabled` on a ScreenGui, or `Visible` on a frame — both stop rendering descendants.
- **Hide, don't destroy**, menus that are reopened often (shop, inventory) — reuse instances, rebuild only list contents. Destroy one-shot popups.
- **Loading screen** goes in `ReplicatedFirst` and is parented to PlayerGui immediately; call `ReplicatedFirst:RemoveDefaultLoadingScreen()`.

## Key ScreenGui / LayerCollector properties (verified against API reference, 2026-10-04)

| Property | Set to | Why |
|---|---|---|
| `ResetOnSpawn` | `false` | Default `true` deletes and re-clones the GUI on every respawn — loses state, re-runs scripts, and causes flicker. Only leave `true` for death-screen style UI. |
| `ZIndexBehavior` | `Sibling` | `Sibling`: ZIndex only orders siblings, children always draw above parents — predictable. `Global` is legacy. |
| `DisplayOrder` | per layer (0/10/20/30/100) | Orders ScreenGuis relative to each other. Leave gaps so new layers fit. |
| `IgnoreGuiInset` | `false` for HUD, `true` for full-bleed backgrounds/overlays | Controls overlap with the top-bar inset. |
| `ScreenInsets` | `CoreUISafeInsets` (HUD/menus), `None` (full-bleed bg), `DeviceSafeInsets` (art that may sit under Roblox buttons but not notches) | Enum values: `None`, `DeviceSafeInsets`, `CoreUISafeInsets`, `TopbarSafeInsets`. |
| `ClipToDeviceSafeArea` | `true` (default) | Clips content to the safe area. |
| `SafeAreaCompatibility` | `FullscreenExtension` (default) | Lets the engine stretch legacy full-screen frames under notches. |

`GuiService:GetInsetArea(Enum.ScreenInsets.X)` returns the `Rect` for a given inset mode; `GuiService.TopbarInset` gives the unobstructed top-bar area (useful to put a custom button next to Roblox's buttons). See [[UI-Layout-And-Device-Scaling]].

## State-driven vs imperative

| Approach | Use when | Cost |
|---|---|---|
| Imperative (`label.Text = ...` scattered in handlers) | Game jam, < 5 screens | Desyncs grow quadratically with screens; avoid for anything you'll live-op |
| Minimal reactive helper (`Value` + `observe`) | Solo / small team, < ~15 screens | ~40 lines, no dependency |
| **Fusion** (0.3) | Small–mid team, likes declarative `New`/`Computed`/`Spring` | Smaller community; API changed between 0.2→0.3 |
| **Vide** | Small team, wants SolidJS-style fine-grained reactivity, very fast | Single maintainer (bus factor) |
| **React-lua** (`jsdotlua/react-lua`) | Mid–large team, long-lived game, devs know React | Most boilerplate; most mature; used by Roblox internally |

⚠️ verify: library versions/maintenance status (Fusion 0.3 release state, Vide maintainer activity) — check each repo's latest release before adopting. Install via Wally/pesde; see [[Module-Architecture]].

Rules regardless of library:
1. **Single source of truth**: client keeps a mirror of server-replicated player data (via attributes, a replication module, or a remote snapshot). UI reads only from that mirror.
2. **Optimistic UI only for cosmetic feedback** (button press, sound). Never show a purchase or currency change as done until the server confirms — see [[Anti-Exploit-And-Server-Authority]] and [[Remotes-And-Networking]].
3. **Components are functions** `(props) -> (Instance, cleanup)`; every connection made by a component is disconnected by its cleanup.
4. **Derived values** (e.g. "can afford") are computed from state, never stored separately.

## Minimal reactive primitive (no dependency)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Value.luau
-- Tiny observable. Tables compare by reference: call set() with a NEW table to trigger observers.
local Value = {}

export type Value<T> = {
	get: () -> T,
	set: (T) -> (),
	observe: (callback: (T) -> ()) -> () -> (), -- returns disconnect
}

function Value.new<T>(initial: T): Value<T>
	local current: T = initial
	local listeners: { [number]: (T) -> () } = {}
	local nextId = 0

	local function get(): T
		return current
	end

	local function set(newValue: T)
		if newValue == current then
			return
		end
		current = newValue
		for _, callback in listeners do
			task.spawn(callback, newValue)
		end
	end

	local function observe(callback: (T) -> ()): () -> ()
		nextId += 1
		local id = nextId
		listeners[id] = callback
		task.spawn(callback, current) -- fire immediately so UI renders initial state
		return function()
			listeners[id] = nil
		end
	end

	return { get = get, set = set, observe = observe }
end

return Value
```

## Router (one menu at a time)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Router.luau
local GuiService = game:GetService("GuiService")
local Lighting = game:GetService("Lighting")

local Value = require(script.Parent.Value)

export type Screen = {
	root: GuiObject,
	firstSelectable: GuiObject?, -- gamepad focus target
	onOpen: (() -> ())?,
	onClose: (() -> ())?,
}

local Router = {}
local screens: { [string]: Screen } = {}
Router.current = Value.new(nil :: string?)

local blur = Instance.new("BlurEffect")
blur.Name = "MenuBlur"
blur.Size = 0
blur.Parent = Lighting

function Router.register(name: string, screen: Screen)
	screens[name] = screen
	screen.root.Visible = false
end

function Router.open(name: string)
	local currentName = Router.current.get()
	if currentName == name then
		return
	end
	if currentName then
		Router.close()
	end
	local screen = screens[name]
	assert(screen, `Unknown screen {name}`)
	screen.root.Visible = true
	blur.Size = 12
	if screen.firstSelectable then
		GuiService.SelectedObject = screen.firstSelectable
	end
	if screen.onOpen then
		screen.onOpen()
	end
	Router.current.set(name)
end

function Router.close()
	local currentName = Router.current.get()
	if not currentName then
		return
	end
	local screen = screens[currentName]
	screen.root.Visible = false
	blur.Size = 0
	GuiService.SelectedObject = nil
	if screen.onClose then
		screen.onClose()
	end
	Router.current.set(nil)
end

function Router.toggle(name: string)
	if Router.current.get() == name then
		Router.close()
	else
		Router.open(name)
	end
end

return Router
```

Gameplay scripts observe `Router.current` to suppress attacks/camera input while a menu is open. Bind a "Back" action (B on gamepad, Esc-alternative like `Backspace` on keyboard — Esc is reserved for the Roblox menu) to `Router.close`.

## Component pattern (counter bound to state)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Components/CurrencyCounter.luau
local Value = require(script.Parent.Parent.Value)

return function(parent: GuiObject, coins: Value.Value<number>): () -> ()
	local label = Instance.new("TextLabel")
	label.Name = "Coins"
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.TextScaled = true
	label.FontFace = Font.fromEnum(Enum.Font.FredokaOne)
	label.Parent = parent

	local disconnect = coins.observe(function(amount: number)
		label.Text = string.format("%d", amount)
	end)

	return function()
		disconnect()
		label:Destroy()
	end
end
```

For animated count-up and reward popups, see [[UI-Polish-And-Juice]].

## UI Styling (engine stylesheets)

- `StyleSheet` holds `StyleRule`s; a `StyleLink` under a ScreenGui applies one sheet to that tree (one sheet per tree).
- **Tokens** = attributes on a token StyleSheet (e.g. `ColorPrimary`, `TextSizeBody`); **themes** = swappable token sets; **style queries** like `@ViewportDisplaySizeSmall` / `@PreferredInputTouch` swap tokens per device.
- Use for: palette, fonts, corner radius, stroke thickness, per-device text sizes. Keep layout logic (what is visible) in code.

## Checklist
- [ ] Every ScreenGui: `ResetOnSpawn=false`, `ZIndexBehavior=Sibling`, deliberate `DisplayOrder` and `ScreenInsets`
- [ ] UI mounted from `StarterPlayerScripts`, templates in `ReplicatedStorage`
- [ ] All displayed numbers come from a single client mirror of server state
- [ ] One router controls menus; opening a menu sets `GuiService.SelectedObject`
- [ ] Every component returns a cleanup that disconnects its connections
- [ ] Colours/fonts come from style tokens, not literals
- [ ] Custom loading screen in `ReplicatedFirst`

## Pitfalls
- `ResetOnSpawn = true` (the default) on a shop GUI: purchase-in-progress state lost on death, LocalScripts inside re-run and double-connect remotes.
- Putting LocalScripts *inside* GUIs in StarterGui: they're cloned per respawn → duplicated listeners, memory leaks.
- Mixing `Global` and `Sibling` ZIndexBehavior across ScreenGuis — confusing overlap bugs.
- Two systems both setting `Visible` on the same frame (e.g. tutorial + router) — route through one owner.
- Trusting client UI for prices/balances; exploiters can edit any client UI.
- Creating new tables each frame and passing them to `Value.set` — triggers observers every frame.

## Related
- [[Visuals/_Index]] · [[UI-Layout-And-Device-Scaling]] · [[UI-Polish-And-Juice]] · [[Art-Direction]]
- [[Module-Architecture]] · [[Remotes-And-Networking]] · [[Anti-Exploit-And-Server-Authority]] · [[Luau-Strict-Typing]]
- [[Onboarding-And-First-60-Seconds]]

## Sources
- ScreenGui / LayerCollector / GuiService API (ScreenInsets, SafeAreaCompatibility, ClipToDeviceSafeArea, GetInsetArea, TopbarInset) — https://create.roblox.com/docs/reference/engine/classes/ScreenGui , https://create.roblox.com/docs/reference/engine/classes/GuiService (checked via Roblox/creator-docs GitHub source, commit of 2026-10-02)
- On-screen containers — https://create.roblox.com/docs/ui/on-screen-containers
- UI styling (StyleSheet, StyleLink, tokens, themes, queries) — https://create.roblox.com/docs/ui/styling , https://create.roblox.com/docs/ui/styling/editor
- Cross-platform UI guidance — https://create.roblox.com/docs/projects/cross-platform
- Fusion vs React-lua discussion — https://devforum.roblox.com/t/fusion-vs-react-lua-which-one-to-use-for-long-term-development/2781328
- Use case for Fusion / React — https://devforum.roblox.com/t/use-case-for-fusion-react-etc/3663300
