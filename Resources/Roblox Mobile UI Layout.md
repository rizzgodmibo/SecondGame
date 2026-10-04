---
title: Roblox Mobile UI Layout
date: 2026-10-03
tags: [roblox, ui, mobile, how-to]
updated: 2026-10-03
verified: 2026-10-03
review_after: 2027-01-01
source: Roblox documentation and local playtest history
project: null
status: sourced-with-historical-examples
---
# Roblox Mobile UI Layout

Lessons from the [[2026-10-03 Paper Plane Toss Phone Playtest]]. Holden's games are mobile + PC first, so build for both from day one.

## Reuse guidance verified 2026-10-03

The historical examples below explain Paper Plane Toss's phone iterations. They are not a portable UI framework or proof of correctness on every phone.

- **Separate screen size, input capability and preferred input.** Roblox documents PreferredInput for the likely primary input and change notifications during play. A phone can have a keyboard or controller attached; TouchEnabled and KeyboardEnabled alone do not establish its form factor. Use available geometry for layout and preferred input for prompts/navigation; preserve usable fallback actions. [S1]
- **Start interactive UI inside CoreUISafeInsets.** Roblox recommends that setting for interactive controls, protecting them from top-bar controls and screen cutouts. An edge-to-edge decorative layer can be separate from the interactive layer. The latter separation is a design recommendation. [S2]
- **Do not halve safe margins as a general rule.** That was a local visual adjustment, not evidence that all remaining content is accessible. Check actual hit areas as well as artwork in both supported landscape orientations.
- **Do not infer rendering coordinates from a phone's advertised resolution or iOS points.** Measure ViewportSize, container AbsoluteSize and the current UIScale in the client. The 0.54 example is arithmetic for an assumed 844×390 layout viewport, not a device-independent conversion.
- **Treat TouchGui/JumpButton lookup as optional compatibility code.** The hierarchy is not established as a public contract by the sources checked here. A lookup may be absent, late, hidden or recreated. Check existence, class, visibility and usable bounds before reading it; provide a tested fallback and clean up observers on teardown.
- **Reflow before shrinking everything.** Recommended: preserve primary action readability, shorten or wrap labels, use scrolling for dense content, and adjust groups for narrow layouts. The boost and clamp below are local tuning values, not universal accessibility thresholds.

## Roblox's own touch controls (historical observations)
- **Thumbstick:** bottom-left. With the dynamic thumbstick, the stick appears wherever you touch the left side, and rests near the bottom-left corner.
- **Jump button:** historical dimensions, not a current API guarantee. On small screens (shortest side ≤ 500 px) it's about 70 px, around 95 px from the right edge and 20 px from the bottom. Larger screens get a 120 px button.
- **Historical placement sketch, incomplete and not drop-in code.** It omits nil/class/visibility guards and fallback handling. Do not access jump.AbsolutePosition unless a valid control was found:

```lua
local touchGui = playerGui:FindFirstChild("TouchGui")
local jump = touchGui and touchGui:FindFirstChild("JumpButton", true)
-- convert screen px -> your UI's design px (root frame with a UIScale s)
local jumpLeft = (jump.AbsolutePosition.X - root.AbsolutePosition.X) / s
local jumpBottom = (jump.AbsolutePosition.Y + jump.AbsoluteSize.Y - root.AbsolutePosition.Y) / s
throwButton.AnchorPoint = Vector2.new(1, 1)
throwButton.Position = UDim2.fromOffset(jumpLeft - 12, jumpBottom)
```

  Re-run this on ViewportSize changes and every couple of seconds, because the jump button appears after your HUD is built.

## Historical touch-first heuristic (do not reuse as a general detector)
```lua
local touch = UserInputService.TouchEnabled and not UserInputService.KeyboardEnabled
```

## Paper Plane Toss scale tuning (historical)
- Designing at 1280×720 and scaling with `min(w/1280, h/720)` makes a landscape phone (~844×390 points) render at about **0.54**. That's too small for kids to read.
- The project gave touch screens an extra **×1.25**, and keep a clamp of 0.5–1.6.
- **Check the vertical space afterwards.** At that scale the design height is only about 575 px, so tall stacks (menu column + THROW!) collide.

## The Paper Plane Toss touch layout (v2, after the 2nd phone playtest)
- **THROW!:** just left of the jump button.
- **PLANES / CHALLENGE:** top of the screen, right of BEST and left of the gear, smaller icons (72 px) and a smaller "!" badge. The bottom-left looked fine in screenshots but the thumbstick sits right there in play: **keep the whole bottom-left corner empty on phones.**
- **AUTO:** bottom-middle, slightly right of centre.
- **BEST pill:** top-centre. The flight distance text moves 64 px down on phones so it sits under the top row.
- **Right column (gear, PETS, REBIRTH, SHOP):** hugs the right edge, about 20% smaller.
- **Potion timers:** below the Glide pill.

## World signs (BillboardGui)
- A BillboardGui sized in studs (`UDim2.fromScale`) keeps growing as the camera approaches, and fills the screen.
- **Historical tuning:** DistanceLowerLimit around 18–24 studs was used to address near-camera growth. Reverify current BillboardGui behaviour and test near/far readability before reuse; this pass did not verify its API semantics.
- **Use `MaxDistance`** to keep clusters of small signs (shop pedestals) from piling up from far away.

Related: [[Paper Plane Toss UI Redesign]], [[Roblox Studio MCP Quirks]]

## Safe area (notch) margins
- **v1 problem:** on an iPhone in landscape the whole HUD sat about one notch-width in from **both** sides. The historical interpretation was symmetric reported insets; this pass has not verified that as a universal iOS or Roblox behaviour. It looked "all over the place" with empty strips at each edge.
- **Historical project adjustment, not reusable safe-area guidance (HUD layer only, phones only):** set `ScreenInsets = None` on the HUD ScreenGui and keep **half** the safe inset as a side margin. A second ScreenGui with `ScreenInsets = DeviceSafeInsets` and a full-size Frame works as a probe to measure the inset.
- **Historical coordinate observation:** a ScreenInsets=None GUI reported negative Y around -58 in the tested Studio setup. Do not hard-code that value or assume a universal origin. Convert between the actual source and destination containers consistently.
- **Testing a touch layout in Studio:** temporarily force `UIKit.touch = true`, play, screenshot, then revert. No jump button exists there, so THROW uses its fallback spot.

```lua
gui.ScreenInsets = Enum.ScreenInsets.None
local probe -- Frame (size 1,1) in a ScreenGui with ScreenInsets.DeviceSafeInsets
local left = probe.AbsolutePosition.X - gui.AbsolutePosition.X
local right = gui.AbsoluteSize.X - left - probe.AbsoluteSize.X
root.Position = UDim2.fromOffset(left * 0.5, top)
root.Size = UDim2.fromOffset((gui.AbsoluteSize.X - (left + right) * 0.5) / s, height / s)
```

## Luau gotcha found here
`local a, b = if cond then f() else g()` keeps only **one** value: `b` is nil. An `if` expression is a single value. Put the condition inside the arguments instead: `f(if cond then 76 else 92)`. selene flags it as `unbalanced_assignments`.

## Local source inspection

On 2026-10-03, C:\Users\holde\Downloads\SecondGame\src\client\UI\UIKit.luau still assigns UIKit.touch once using TouchEnabled and not KeyboardEnabled, and uses half of measured horizontal device-safe margins for MainUI. Its fit function responds to viewport/probe changes, but the inspected section does not update UIKit.touch on PreferredInput changes. This is a reuse finding, not a newly reproduced device bug.

UIKit SHA256: 50C789D8BC8ECAED37C89038870A6C3DCB670AAD235F6291FC792066D603EFAE. No project code was changed.

## Device and interaction acceptance matrix

Recommended tests; none were executed in this research pass.

| Case | What to exercise | Acceptance evidence |
|---|---|---|
| Narrow phone, supported landscape orientations | HUD, tutorial, shop, close buttons, purchases | Text readable; all hit areas outside cutouts and platform controls |
| Tablet / wide phone | Dense inventory and menus | No excessive empty space or unreachable primary action |
| Keyboard attached to phone/tablet | Connect, disconnect, switch interaction during a session | Correct prompts; touch fallback remains usable; layout does not assume a desktop viewport |
| Controller attached where supported | Focus, confirm, back, close, return to touch | No focus trap or action requiring an unavailable pointer |
| Desktop resized window | Narrow/wide aspect changes, modal open | Reflow without clipped labels or off-screen dismissal |
| On-screen keyboard visible | Codes/search/text fields, submit/cancel | Field and exit remain reachable; gameplay input does not fire through typing |
| Movement plus action | Thumbstick drag, camera drag, jump and game button | Actions do not steal required movement touches or trigger twice |
| Long/localised labels and large values | Price, balance, item title, reward message | Content stays legible and complete; no hidden price or overlaid button |
| Respawn/rejoin/control recreation | HUD and open/close loops | No duplicate listeners, orphaned probes or stale control references |
| Representative real phone | Full gameplay with UI/VFX load | Responsiveness and readability observed on device, not inferred from desktop timing |

Roblox's Studio testing documentation describes device simulation, touch/keyboard simulation and text elongation through player emulation. Use these for repeatable layout checks; actual phone testing remains the acceptance step for real interaction and performance. [S3]

Record build, client/Studio version, device, measured viewport, orientation, input devices, tested UI state, screenshot/video evidence and pass/fail. Forcing UIKit.touch=true tests a branch only; it does not emulate touch controls, safe areas, mixed input or a phone's performance.

## Remaining gaps

BillboardGui sizing behaviour needs a dedicated verified pass. The old Luau multiple-return statement above is retained from project history and was not re-tested here. Further visuals work should cover accessible contrast/text sizing, reduced motion, modal focus, UI memory/listener ownership and asset-loading failure states.

Related: [[Roblox Development Playbook]], [[Roblox Vault Coverage and Maintenance]].

## Sources

Checked 2026-10-03:
- [S1: Roblox input](https://create.roblox.com/docs/input) — mixed-device input and PreferredInput changes.
- [UserInputService](https://create.roblox.com/docs/reference/engine/classes/UserInputService) — input capability and preferred-input API.
- [S2: On-screen UI containers](https://create.roblox.com/docs/ui/on-screen-containers) — recommended interactive safe-area setting.
- [S3: Studio testing modes](https://create.roblox.com/docs/studio/testing-modes) — device simulation and player-emulation text expansion.
- Local evidence: [[2026-10-03 Paper Plane Toss Phone Playtest]] and C:\Users\holde\Downloads\SecondGame\src\client\UI\UIKit.luau. Historical observations are not new playtest results.
