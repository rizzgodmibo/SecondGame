---
tags: [project/rubber-tower, design/level]
status: final
updated: 2026-10-05
---
# Rubber Tower: Option B picked → detail + build (prompt)

Paste the block into Claude Code.

```
I pick Option B, "Through the Middle". Record it as USER in [[Rubber-Tower]] and [[Rubber-Tower-Map-Build-Plan]]. I want MORE DETAIL before and while you build, then move forward with it.

STEP 1: DETAILED SPEC FOR OPTION B (write it into [[Rubber-Tower-Map-Build-Plan]], short and clear)
For each of the 6 places (Lily Lake, Village Rooftops, Windmill Climb, Crystal Skyway, Waterfall Ledges + Cave, Treetop Return) give me:
- The beat list: every jump/section in order, which kit piece it uses (exact model names), start/end height, and the gap (keep within default movement and fair on a phone).
- Teach → test → twist: what's taught, where it's tested, what the twist is, and where the soft rest is.
- Where you land when you fall from each part. In a ragdoll game falls are the fun: falls should usually drop you onto a lower part of the route, a soft pad, water or a bouncy thing, not all the way back to spawn. Mark the few places where a fall costs more.
- The side path (harder shortcut or scenic detour), where it rejoins, and what's on it (a duck, a view, a secret).
- Dressing: which props and decor make it feel like a place (trees, critters, signs, lanterns, shops, NPC spots), and 1–2 goofy details.
- What you can SEE from there: the next landmark, the other crossing of the figure-8, players above/below, CP1.
- Mood: lighting/colour accents (glow crystals, waterfall mist, lantern light) within the obby lighting preset.
- Time estimate per place, adding up to the 5–8 minute S1 target.
Also:
- The figure-8 crossing: make sure the Treetop Return bridge (~y90) and the Crystal Skyway (~y55) can't be used to skip the route (no bounce pad that reaches the upper path from the lower one), and that falling from the upper crossing onto the skyway feels like a funny catch, not a softlock.
- The Crystal Skyway passes UNDER the CP1 island: keep enough headroom so you don't bonk your head or get stuck.
- Windmill blades: build them STATIC first. Then add a slow spin behind a Config toggle if it stays fair; I'll decide after playing it.
- List any kit pieces you're missing for this layout (e.g. a lake shore, a cave tunnel piece, a big trunk, a skyway platform) and make them in the v5 style, with the same pipeline and preflight.

STEP 2: BUILD
- Build the ground floor (plaza, shops placed, splash pond, Lily Lake, trees, decor) and places 1–3 (Lily Lake, Village Rooftops, Windmill Climb) first. Then show me a quick check-in: 4 screenshots (spawn view, rooftops, windmill, looking back across the middle) and the timer so far. Keep going unless I say stop.
- Then places 4–6 and the CP1 landmark, with the 5 hidden ducks and the secret room behind the waterfall.
- Use the manifest's invisible colliders for walkable tops, keep checkpoint tags/heights unchanged, and keep the Leap of Faith lane to the splash pond clear at every height (test a real leap).
- Lighting: the obby preset from the vault.

STEP 3: CHECKS, THEN STOP
- Map audit (every place reachable with default movement), the dev segment timer, walk-test every bounce/wobble/ice/mover piece, falls land where the spec says, the skip check at the figure-8 crossing, tri/instance counts, client FPS with Studio visible.
- Show me: the 4 angles (spawn, CP1 looking up, outside overview from a corner, 150 px shrunk), one screenshot per place, a short fly-through of the route, before/after next to the v2 map, and an honest self-critique against [[Art Direction Feedback]] and "does it feel like climbing through a world?". Then stop for my review.
- Keep the vault updated with today's real date.
```
