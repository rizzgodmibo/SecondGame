---
tags: [prompting/ui, visuals/ui]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: UI (Menus, HUD, Shops)

How to get Roblox UI from Claude that looks like a top simulator and works on phones, not "UI built from primitives". General rules: [[Prompting-Principles]].

## TL;DR
- **Start from a reference image and make Claude analyse it before building:** layout, sizes, positions, hex colours, components. Then build in passes: layout → colours → icons/details, checking each pass ([[AI-Assisted-Workflow]] §1, community, confirmed locally).
- **Painted image assets, not primitives.** Holden called the primitive-built UI "lazy". The fix was a designed kit (frames, buttons, pills, tabs, cards) rendered to PNG and 9-sliced in game ([[Paper Plane Toss UI Redesign]], [[Art Direction Feedback]]).
- **Name the faults precisely** and name the patterns to avoid: mixed outline thickness (the "AI giveaway"), default grey boxes, stray boxes around buttons, text under 14 px ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]], Anthropic on naming patterns).
- **Give Claude its own checks:** the [[Roblox UI Checker Skill]] at four screen sizes, Studio screenshots compared with the reference, and finally Holden's phone.
- **For a polish push on one screen, run a capped blind critic loop.** The shop went from losing 0/4 to winning 4/4 blind comparisons in 3 build rounds ([[Shop Gauntlet Workbench]]).

## What Claude needs from you
- 1–3 reference screenshots, plus what to copy (structure, depth, colour logic) and what not to (their items, theme, text).
- The screens to build or redo, and the game's palette and fonts (or "propose a palette and stop").
- The UI kit and architecture in use (e.g. `UIKit.luau`, design space 1280×720 with UIScale), and the target devices: phone landscape first, then PC.
- Any approved layout decisions (e.g. Paper Plane Toss's touch layout: THROW! left of the jump button, nothing in the thumbstick corner).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[UI-Architecture]] · [[UI-Layout-And-Device-Scaling]] | One ScreenGui per layer, ResetOnSpawn off, state drives UI, Scale + aspect constraints, safe insets, 44 px touch targets |
| [[UI-Polish-And-Juice]] | Button hover/press numbers, easing defaults, reward count-up, ReducedMotion |
| [[Roblox Mobile UI Layout]] · [[2026-10-03 Paper Plane Toss Phone Playtest]] | The ×1.25 phone boost, thumbstick/jump zones, BillboardGui growth, notch margins |
| [[Paper Plane Toss UI Redesign]] · [[Shop Gauntlet Workbench]] | The painted-kit pipeline (headless Chrome renders, 9-slice), the 1024 px stored-image trap |
| [[X-Shop-And-Seasonal-UI]] · [[X-HUD-And-Menus-UI]] · [[X-Animated-UI-Lessons-And-Tools]] · [[UI-And-Gameplay-Reference]] | Captured real-game and designer references to use as the bar |
| [[Roblox UI Checker Skill]] | The automatic layout check |

## Prompts

### 1. Analyse the reference (no building)
```text
Analyse this reference UI. Don't build or change anything yet.
[attach screenshot(s)]
Describe: the canvas size and the layout grid; every element with its approximate position and size; the colours as hex values; the depth treatment (shadow colour and offset, face gradient, top highlight, outline colour and thickness); fonts and text sizes; and how the eye is led to the buy button.
Then tell me which parts fit [Game] and which don't (theme, items, text we must not copy). Keep it to one page.
```
Why: skipping the analyse step makes Claude guess the layout, and every later pass inherits the error ([[AI-Assisted-Workflow]] pitfalls).

### 2. Build the screen in passes
```text
Build the [SCREEN] for [Game] from your analysis, in three passes. Show me a Studio screenshot after each pass and wait for my OK before the next.
Pass 1, layout: sizes, positions, anchoring, scrolling, at the 1280×720 design size with our UIScale. Phone landscape first.
Pass 2, colour and depth: our palette, the depth stack on every panel and button (tinted drop shadow, face gradient, top highlight, the SAME outline thickness everywhere).
Pass 3, icons and detail: icons from [icon pack / existing UIAssets], badges, tags.
RULES: painted image assets from our kit (art/uikit), never plain Frames with UIStroke as the final look. UI built from code with ResetOnSpawn off; buttons only send requests, the server decides. Prices come from GetProductInfoAsync, never hard-coded. Don't use: default grey frames, emoji as icons, text under 20 design px, mixed outline thickness, boxes drawn around buttons.
```
Why: one pass at a time lets each be checked; the named "don't use" list follows Anthropic's advice to name specific patterns rather than "avoid a generic look".

### 3. Precise correction
```text
Fix these on [SCREEN] and nothing else:
1. [element] is [N] px too low; align its top with [other element].
2. [element]'s outline is 2 px; every other outline is 3 px.
3. [text] wraps onto a second line on phone; keep it on one line at 20 px or shorten the copy to "[new copy]".
Show before/after screenshots side by side.
```
Why: "make it better" wastes a pass; coordinates, sizes and hex values don't ([[AI-Assisted-Workflow]]).

### 4. Phone check
```text
Run the roblox-ui-checker skill on [SCREEN] (open the panel first; closed panels are skipped) at all four sizes, and run it live under Studio's device emulator. Then fix every FAIL and real WARN: touch targets under 44 px, overlaps, off-screen elements, clipped or tiny text, default boxes, mixed outlines.
Also check our phone rules: nothing in the bottom-left thumbstick area, primary button near (not under) the jump button, interactive UI inside CoreUISafeInsets.
Delete the temporary runner afterwards and confirm git status is clean. Then ask me to check on my phone; the checker doesn't replace that.
```

### 5. Blind critic loop for one screen (capped)
```text
Run a Gauntlet-style loop on [SCREEN], max [4] rounds, about [2] hours. Not a standing workflow.
BAR: [reference screenshot(s)] (kept local only; third-party).
ROUND: capture our screen in Studio in its buy state with a temporary Studio-only preview script; put ours and the reference side by side as pairX-A/B with sides shuffled, and keep the answers in a KEY file the critic must not open.
CRITIC: a fresh subagent sees only the image pairs. It picks the better screen for a young teen on a phone, with 2–3 reasons, and lists the loser's 3 most concrete fixable problems. Pick, don't score.
BUILDER: you fix the top gaps; gates (stylua, selene, rojo build) after every edit. Check each critic claim against the image before acting; critics misread small details.
LOCKED: prices, products, server code, odds display, PolicyService hiding. No publishing. New images allowed: list every new asset id.
Keep a workbench note with each round's screenshots and results. Stop when ours wins every pair or at the cap, then show me before/after.
```
Why: it worked once at that scale, and the screenshots exposed a game-wide 9-slice bug along the way ([[Shop Gauntlet Workbench]], [[Gauntlet-Loop]]).

### 6. Juice pass
```text
Add feedback to [SCREEN] using the numbers in Visuals/UI-Polish-And-Juice.md: hover 1.05–1.08 and press 0.90–0.94 through a UIScale child (never tween Size), Back/Out entrances 0.25–0.35 s and faster exits, a count-up on currency changes, a click sound from our sound catalogue. Respect GuiService.ReducedMotionEnabled (fades instead of movement). Scale the feedback to the reward size, so small actions stay subtle.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Phone HUD layout
```text
Lay out the HUD for [Game] for phone landscape first (Resources/Roblox Mobile UI Layout.md): currency top-left, [main action button] just left of the jump button, menu buttons in a right column against the edge, nothing in the bottom-left thumbstick area, everything inside CoreUISafeInsets. Then PC. Show a screenshot of each and run the UI checker.
```

### Inventory grid
```text
Build the inventory panel for [Game]: a scrolling grid (UIGridLayout + AutomaticCanvasSize) of item cards using our kit's rarity cards, each with icon, name, level and an equipped badge; tabs for [categories]; empty state text. Cards are cloned from one template and filled from data; tapping a card opens a details pane with Equip/Sell buttons that only send requests.
```

### Settings menu
```text
Add a settings panel to [Game]: Music and SFX sliders (save the value about 0.35 s after the last change, start both groups at 0 until saved settings arrive), a reduced-motion toggle, and a "reset tutorial" button gated behind a confirm. Touch-friendly sliders (track the input that started the drag). Show it on a phone-sized viewport.
```
The slider rules come from [[Roblox Audio Pipeline]] (Paper Plane Toss).

### Toasts and popups
```text
Add one notification system for [Game]: toasts (top-centre, stack up to 3, 2.5 s, fade out) and modal popups (one at a time, dim the world, queue the rest). Everything else calls Notify.toast(text, kind) or Notify.popup(def). No popup in a new player's first 60 seconds; max one unsolicited offer popup per session.
```

### Loading and title screen
```text
Make a loading screen and title card for [Game] in ReplicatedFirst: the logo (rbxassetid [id]), a progress bar driven by ContentProvider:PreloadAsync on the key UI images, a skip after [5] s, and a fade into the game. Must look right at phone and PC sizes and never block for more than [10] s.
```

### From a design mock to Roblox
```text
Here's the approved mock for [screen] from [Claude Design / Figma] (attached). Rebuild it in Roblox with our UIKit: map each mock element to a kit piece or a new piece (list any new images you'd need to render and upload; don't upload without my OK). Keep the mock's spacing and hierarchy; text sizes may go up for phones. Show the mock and the Studio screenshot side by side.
```

## How to check the result
- Studio screenshots after every pass, compared side by side with the reference.
- UI checker: no FAIL at 667×375, 844×390, 1024×768, 1920×1080.
- Holden's phone check; for big pushes, the blind critic's pick.
- Prices on screen match `GetProductInfoAsync`; odds still visible before buying.

## Pitfalls
- **Primitives as the final look:** rejected as "lazy" every time ([[Art Direction Feedback]]).
- **Designing at 1920×1080 on PC and never opening the emulator**, the #1 cause of unusable mobile UI ([[UI-Layout-And-Device-Scaling]]).
- **Uploaded images are stored smaller than the source** (seen at max 1024 px), so 9-slice rects in source pixels cut off borders. Scale the slice rect to the stored size ([[Shop Gauntlet Workbench]], ⚠️ verify).
- **ResetOnSpawn on** wipes UI state on death; **LocalScripts inside StarterGui** double-connect ([[UI-Architecture]]).
- **World signs grow to fill the screen** when sized in studs; set `DistanceLowerLimit` and `MaxDistance` ([[Roblox Mobile UI Layout]]).
- **Guilt or pressure copy** around purchases is a dark pattern for a young audience ([[X-Animated-UI-Lessons-And-Tools]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Monetisation]] · [[Prompting-Debugging-And-Testing]] · [[Prompt-Library]] §3 · [[Gauntlet-Loop]]

## Sources
- Anthropic, "Prompting Claude Opus 5.5" (name specific patterns to avoid in design work): <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5>
- Anthropic, Claude Code best practices ("paste screenshot, implement, screenshot the result, compare, fix"): <https://code.claude.com/docs/en/best-practices>
- SyphoDev video (depth stack, UI checker, 11:57–14:40): <https://www.youtube.com/watch?v=afuKhenJldY>
- Local: [[Paper Plane Toss UI Redesign]], [[Shop Gauntlet Workbench]], [[2026-10-03 Paper Plane Toss Phone Playtest]].
