---
title: Lighting Recipes
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, presets, luau, recipes]
---

# Lighting Recipes
Presets and scripts. Back to [[Lighting Overview]].

**Trust levels:** values marked *official* come straight from Roblox's outdoor lighting tutorial. Everything marked *starting point* is my suggestion from the general guidance, so tune it by eye and write down what works in your game.

## Golden hour / evening (official campfire scene)
| Where | Property | Value |
|---|---|---|
| Lighting | LightingStyle | Realistic |
| Lighting | ClockTime | 17 |
| Lighting | EnvironmentDiffuseScale / EnvironmentSpecularScale | 1 / 1 |
| Lighting | OutdoorAmbient and Ambient | 156,136,176 (purple evening sky; the "before" comparison image used a gray 70,70,70) |
| Atmosphere | Density / Haze / Color | 0.272 / 1 / 85,78,54 |
| PointLight (campfire) | Range / Brightness / Color / Shadows | 48 / 2 / 255,179,73 / on |

## Other moods (starting points, directional)
| Mood | Time | Ambient | Atmosphere | Clouds | Extras |
|---|---|---|---|---|---|
| Clear day | ClockTime 10 to 14 | light neutral or slightly blue | low Density, low Haze | Cover 0.4 to 0.65, low Density | light SunRays, small ColorCorrection contrast boost |
| Overcast / storm | any | gray-blue, lower Brightness | higher Density and Haze, gray Color | Cover 0.8+, Density 0.4+ | less saturation, no sun rays |
| Night | ClockTime 0 to 3 | dark blue, raise ExposureCompensation a little if too dark | cool blue Color, modest Density | Cover low | keep stars (default 3000), add warm local lights as pools of light |
| Horror | night or dusk | very dark, slightly desaturated | dense Haze, dark Color | thick or none | player SpotLight with narrow angle, fog-like Density, low Bloom |
| Alien / fantasy | any | tinted purple/teal | tinted Color and Decay, high Haze | Color like 75,50,255 | stronger ColorCorrection tint |

## Apply a preset with Luau (works from a script or Studio MCP `execute_luau`)
```lua
local Lighting = game:GetService("Lighting")

local function getOrCreate(parent: Instance, className: string): Instance
	local obj = parent:FindFirstChildOfClass(className)
	if not obj then
		obj = Instance.new(className)
		obj.Parent = parent
	end
	return obj
end

local presets = {
	GoldenHour = {
		lighting = {
			ClockTime = 17,
			Ambient = Color3.fromRGB(156, 136, 176),
			OutdoorAmbient = Color3.fromRGB(156, 136, 176),
			EnvironmentDiffuseScale = 1,
			EnvironmentSpecularScale = 1,
		},
		atmosphere = {
			Density = 0.272,
			Haze = 1,
			Color = Color3.fromRGB(85, 78, 54),
		},
	},
}

local function apply(name: string)
	local preset = presets[name]
	assert(preset, "unknown preset: " .. name)

	Lighting.LightingStyle = Enum.LightingStyle.Realistic
	for prop, value in preset.lighting do
		Lighting[prop] = value
	end

	local atmosphere = getOrCreate(Lighting, "Atmosphere")
	for prop, value in preset.atmosphere do
		atmosphere[prop] = value
	end
end

apply("GoldenHour")
```
Add clouds with `getOrCreate(workspace.Terrain, "Clouds")` (they must be under Terrain). `Lighting.Technology` cannot be set from code.

## Day night cycle
Official note: `ClockTime` does not move by itself; a script must change it. My version, run in a **LocalScript** (client) so you do not replicate a property change to everyone every frame:
```lua
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")

local REAL_SECONDS_PER_DAY = 20 * 60 -- a full 24 hour cycle in 20 real minutes

RunService.Heartbeat:Connect(function(dt)
	Lighting.ClockTime = (Lighting.ClockTime + dt * 24 / REAL_SECONDS_PER_DAY) % 24
end)
```
Next steps to make it feel good:
- Tween Atmosphere Color/Haze, ambient colors, and Clouds Cover/Density between "keyframes" (dawn, noon, dusk, night) with TweenService.
- `Lighting:SetMinutesAfterMidnight()` is the official numeric alternative to ClockTime.
- Keep `GeographicLatitude` fixed so the sun arc stays consistent.
- If time must be shared across players, replicate a start time from the server and let each client compute the current ClockTime itself.
