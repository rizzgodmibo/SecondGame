---
tags: [assets/3d, visuals/art-direction, visuals/vfx]
status: draft
updated: 2026-10-04
confidence: medium
---

# Fantasy Creatures Set (practice set 01)

Three original practice creatures, each with a Kingshot-style reference sheet ("creature design bible") and a game-ready
OBJ export. They are for practice, not tied to a game. Files are in `Assets/FantasyCreatures/`.

| Creature | Element | Body | Size (studs, W × H × L) | Game mesh tris |
|---|---|---|---|---|
| **Cinder Drake** (v3) | fire | winged quadruped | 8.0 × 7.6 × 14.5 | 16,490 body + 3,648 wings + 160 glow |
| **Mossback Golem** | earth + crystal | stone brute, knuckle-walker | 9.3 × 9.7 × 4.7 | 5,804 body + 646 crystals + 154 glow |
| **Frostfang Wolf** | ice | swift quadruped | 2.1 × 5.1 × 8.3 | 5,664 body + 442 ice + 180 glow |

## TL;DR
- **Rebuild everything with one script.** `build_creatures.py` runs headless on Blender 5.2 with GPU/OptiX. It builds the creatures, renders every sheet image into `design/renders/`, and exports the OBJs.
  - Render: `blender -b --factory-startup -P build_creatures.py -- golem all`
  - Export: `... -- export drake golem wolf`
- **Sheets.** They are a Claude Design canvas, **published privately** at https://claude.ai/artifact/4WGMTGvh8jcdEW5SANNFMW (version 7, 2026-10-04: drake board on v3; golem and wolf still v1).
  - Local source: `design/canvas.json`, `Main.dc.html` (drake, the entry board), `MossbackGolem.dc.html`, `FrostfangWolf.dc.html`, shared `sheet.css`, `vfx/` (mask textures) and `renders/`.
  - To republish, copy them to a `project/` tree and publish to the same URL. The type wants a `data-dc-script` block in each board and no inline `url()`.
  - Full-sheet PNGs are in `design/png/` (headless Chrome). `*_v1.png` are the first 3D versions, kept for before/after.
  - Preview locally with the `creature-sheets` server in `.claude/launch.json` (Blender's Python `http.server`, port 8777, serving `Assets/`).
- **Export per creature.** `models/<Name>/<Name>.obj` + `.mtl` + `<Name>_Color.png` (1024², baked) + `build_report.json` (sizes, tris, VFX attachment points in Roblox axes) + two preview renders of the actual game mesh.
- **Parts.** Every OBJ holds separate objects: `_Body` (textured, SmoothPlastic), `_Crystals`/`_Ice` (textured with the same PNG, Glass) and `_Glow` (flat colour, Neon).
- **Status (2026-10-04, later):**
  - **Drake.** A v2 detail pass (more spikes, brows, armour) was built and exported. Holden's new art direction replaced it: the drake was cute and toy-like, so anatomy comes first.
  - **Drake v3 (anatomy pass).** Built as a grey clay review model and **approved by Holden**. See [[#Drake v3 anatomy pass (2026-10-04)]].
  - **Drake v3 surface + colour pass.** Built and shown. Holden: "fix weak points, colour plus normal and roughness map, we want this high quality". See [[#Drake v3 surface + colour pass (2026-10-04)]].
  - **Drake v3 game export.** Done: `models/CinderDrake/` holds the OBJ, seven 1024² SurfaceAppearance maps and `IMPORT.md`. See [[#Drake v3 game export: SurfaceAppearance maps (2026-10-04)]].
  - **Drake v3 VFX + sheet update.** Done and **waiting for Holden's review**:
    - the v3 board is republished;
    - the OBJ was re-exported with the mouth interior;
    - a data-only Roblox VFX spec (`VFX.md` + `vfx_spec.json`) is written.
    - See [[#Drake v3 VFX + sheet update (2026-10-04)]].
  - **Golem and wolf.** Golem v2 is half done; its renders have not been reviewed. Wolf v2 has not started. Both are paused until the drake is approved.
  - **Scripts and rig.** Roblox scripts: **not yet**. Rig: **static OBJ only** (decided).
  - The OBJs have not been imported into Studio.

## Gallery (2026-10-04)
![[Assets/FantasyCreatures/design/png/CinderDrake.png|960]]
![[Assets/FantasyCreatures/design/png/MossbackGolem.png|960]]
![[Assets/FantasyCreatures/design/png/FrostfangWolf.png|960]]

The actual game meshes with their baked textures (what Roblox will get):

![[Assets/FantasyCreatures/models/CinderDrake/preview_front34.png|300]] ![[Assets/FantasyCreatures/models/MossbackGolem/preview_front34.png|300]] ![[Assets/FantasyCreatures/models/FrostfangWolf/preview_front34.png|300]]

## Folder
| Path | What |
|---|---|
| `build_creatures.py` | The whole pipeline: SDF sculpting, rig, materials, render sets (`ortho hero poses parts mats scale vfx habitat`), export |
| `design/` | Claude Design canvas: `canvas.json`, `Main.dc.html` (Cinder Drake), `MossbackGolem.dc.html`, `FrostfangWolf.dc.html`, `sheet.css`, `vfx/`; `renders/` (81 PNGs), `png/` (full sheets, `*_v1.png` = first 3D pass) |
| `models/<Name>/` | OBJ + MTL + baked colour PNG + `build_report.json` + `preview_front34/back34.png`. Drake v3: 7 SurfaceAppearance maps, `IMPORT.md`, `VFX.md` + `vfx_spec.json`, `preview_game_*.png` |
| `vfx/` | Copies of the 10 VFX textures the creatures use (8 from [[VFX-Texture-Pack]], `FrostFlake` + `Sparkle` from [[Dragons-Hoard-Set]]) |
| `*.blend` | Saved scenes per creature and export (gitignored) |

## Reusable technique (local observations)
- **Sculpting with signed-distance fields.** Bodies are smooth unions of ellipsoids, round cones (Inigo Quilez's `sdRoundCone`) and rounded boxes:
  - Evaluate each primitive only inside its own bounding box, in numpy on a 0.032–0.05 stud grid.
  - Mesh the field with surface nets (quads), then smooth with 5–6 Taubin passes (λ 0.5 / μ −0.53).
  - A body takes about 1.2 s. It looks hand-sculpted, and smooth subtraction carves eye sockets and the mouth line.
- **Posing without skinning.** A ~15-line FK rig rotates the SDF primitives and the hard parts about rest-pose joints, and each pose is re-meshed. Joints blend cleanly because the field re-forms at every joint.
  - **Rotation sign convention** (rotations about world X, creature faces +Y): **+X lifts anything pointing forward** (head up). The jaw opens with a **negative** X rotation, and the tail rises with a **negative** one. The first renders had these backwards.
- **Hard parts are plain meshes:** horns (swept tubes with a `t` attribute for the dark tip), plates/crystals/rocks (convex hulls, bevel for a chiselled look), wings (fans of quads from the wrist, plus Solidify).
- **Zone masks as point attributes.** Belly, crack, saddle and the ventral band coordinate (`vs` = arc length along a spine polyline) are computed per vertex in numpy and read by Attribute nodes. That keeps the zone edges crisp: map range them over a narrow 0.42–0.56 window. It also follows the pose.
- **Sheet renders:**
  - **Engine and colour:** Cycles + OptiX denoise, AgX "Punchy" view, exposure +0.25, transparent film plus a shadow catcher.
  - **Light rig:** a three-point setup with two coloured rims, scaled to the creature's bounding sphere.
  - **Orthographic cameras:** must use `to_track_quat("-Z", "Y")`. With `"Z"` the view comes out rolled 90°.
  - **Timing:** about 1–5 s per image on the RTX 4060 Ti. The first render of a session spends ~80 s compiling OptiX kernels.
- **VFX previews with real textures:** camera-facing cards (Emission × texture, mixed with Transparent by the texture alpha). Flipbook cells come from a Mapping node (scale 0.25, offset per cell).
- **Bake to the game mesh:**
  - **Decimate:** COLLAPSE to per-object targets. Drop Subsurf and set bevels to 1 segment for export (the golem went from 10.5k to 5.8k).
  - **Shared UV space:** multi-object Smart UV Project + pack, so the `_Body` and `_Crystals` parts share one 1024² PNG.
  - **Bake passes:** selected-to-active DIFFUSE (colour only, AO node included) plus EMIT, then combine them in numpy (`colour + emit × 0.55`). About 33 s per pass.

## Pitfalls hit
- **Flat SVG concept art was the wrong call.** The reference sheet's power is 3D-rendered art. Render the actual model for every view (hero, orthos, parts, poses, scale), so the sheet and the model match.
- **Voronoi scales read as polka dots or leopard spots** when cell colours vary or the seams are wide. Keep the colour contrast low (≤ 0.12), seams thin (0.44–0.58 of F1) and let bump do the work.
- **Emissive fire under AgX turns pale pink** when the flame has a lit base colour. Use pure Emission shells, with transparency at grazing angles (Layer Weight facing^k).
- **A flat lava ribbon disappeared** because the "soft edge" emission material is transparent at grazing angles. Ground-level emitters need solid emission.
- **The golem's core was too visible.** Bigger rocks plus a thinner core, so the violet seams show only in the gaps.
- **Background renders can't see** objects with `hide_render`. `world_bbox` needs an include-hidden flag for framing.
- **Headless Chrome path quoting in bash:** `"C:\\...\\$s.png"` writes a literal `png$s.png`. Use forward slashes and `${s}`.

## Decisions and feedback (2026-10-04)
- Holden's brief: "three fantasy creatures in the style of" a Kingshot unit design sheet (Mercenary Lancer), made with Claude Design + Blender, not blocky Roblox style. Practice only, no rig, OBJ + MTL + textures (not GLB), visuals-only scripts, plus an asset/import list.
- The creature picks (fire drake, moss/crystal golem, ice wolf), names and habitat blurbs are **Claude's proposals**. Holden said "keep working" after the style correction but has not approved them explicitly.
- Holden's style correction: the flat vector sheet "looks nothing like the reference, I want it in that style". Logged in [[Art Direction Feedback]].
- The first Claude Design publish was blocked by the auto-mode permission check. Holden then approved it, and the canvas was published privately (link in the TL;DR).
- Holden's answers (2026-10-04):
  - publish: yes
  - designs: "the bases are alright, but i want more detail and a more intimidating/detailed look"
  - Roblox scripts + zip: **not yet**
  - rig: **static OBJ only**
- Blender MCP: Holden will fix the connection for the next session. It is only registered in `Downloads\Fish A Monster\.mcp.json`, so a gitignored `C:\Vault\.mcp.json` with the same `blender` entry, plus the add-on server running, loads it in a new session. Its safe mode blocks numpy, so `build_creatures.py` stays headless. The MCP is for live viewing and tweaks.

## Next steps: v2 "more detail, more intimidating" (planned 2026-10-04, not started)
These are Claude's proposals; confirm them with Holden before building.
- **Drake:**
  - head: scowling brows (round cones from outer-back to inner-front over narrower slanted eyes), nasal ridge + nose horn, chin spike, three jaw-line spikes per side, a second smaller horn pair, longer and more curved main horns, crest spikes on the back of the skull
  - mouth: longer fangs visible with the mouth shut, an emissive throat glow, idle jaw slightly open
  - body: obsidian shoulder/thigh armour plates (raycast-placed shingles), taller blade plates plus two side spike rows, elbow/heel spikes, a spiked tail tip, longer curved claws, pectoral/haunch muscle forms
  - wings: jagged, deeper scallops, finger-tip claws
  - colour: darker crimson-to-black dorsal gradient, bigger back scales, hotter and wider lava cracks, plates with glowing tips
  - hero: a low "menace" pose
- **Golem:**
  - head: smaller and sunk lower, V-shaped brow over angled slit eyes, crystal tusks, a crystal crown
  - shoulders: hunched and higher, with big outward crystal spikes; knuckle crystals
  - glowing bronze rune bands on the arms; the `VFX_magic_circle` sigil projected onto the chest rocks around the heart; violet cracks leaking near the heart
  - more faceted rocks (fewer hull points), floating pebbles, hanging vines, darker stone
- **Wolf:**
  - dire-wolf bulk: head ×1.12, broader chest, shoulder hump, thicker legs, lowered head carriage
  - face: heavy scowl brows, snarl wrinkles, saber fangs with the jaw slightly open, ears pinned back with one torn, claw scars, a dark eye mask
  - fur: raised hackles, darker slate fur with a near-black saddle and frosted lower legs
  - ice: bigger jagged spine ice, shoulder ice pauldrons, elbow spikes, chest icicles, ice claws
  - hero: snarl pose instead of howl
- Then re-render all sheets, republish the canvas (same URL), re-export the OBJs (keep 6–10k tris each) and update this note.
- Roblox scripts (CreatureVFX / CreatureSetup / DevCreatureDemo / IMPORT.md / zip) only when Holden says go.

## Screenshot critique: more realistic and scary (2026-10-04)
- User request: the attached Cinder Drake model should look more realistic and scary. This is creature-specific feedback, not a replacement for other projects' low-poly art direction. The user describes the assets as for a Roblox game; the earlier practice-only context above may no longer describe intended use. No specific game was identified.
- Visual observations: rounded head and muzzle, large bright eyes, even exposed teeth, barrel torso, short soft legs, small wings, and thick rounded wing struts make it read as a friendly mascot. Orange surface noise competes with the silhouette; armour looks attached rather than anatomically integrated.
- Recommendations (not yet approved implementation): mature predator proportions; angular skull and recessed smaller eyes; articulated shoulders, elbows, wrists and toes; tapered torso; larger wings with visible finger structure and thinner membranes; overlapping scales following anatomy; predominantly dark charcoal/crimson surfaces with sparse ember fissures.
- Correct the silhouette and anatomy before adding detail. Extra spikes, larger glow areas and angry brows alone will retain the toy-like base. In particular, reconsider the older proposal for hotter/wider cracks everywhere.
- Suggested Claude review gate: revise the drake first and show neutral-lit untextured front, side and three-quarter views before materials, effects, sheet redesign or work on other creatures. Keep geometry readable without dramatic lighting.
- Source: Holden's two attached screenshots and request in Codex, 2026-10-04. No mesh inspection or implementation performed. Related: [[Art Direction Feedback]], [[Art-Direction]].

## Drake v3 anatomy pass (2026-10-04)
Holden's direction in Claude (same session, same intent as the critique above): "believable, intimidating dark-fantasy creature", abandon "young drake / big head / small wings", fix anatomy, proportions and silhouette first. He asked to see "an untextured grey model in front, side, and three-quarter views under neutral lighting" and to approve the anatomy before textures, VFX or the sheet.

**Status: built, shown to Holden, not yet approved.** No textures, VFX, sheet or export changes have been made for v3.

![[Assets/FantasyCreatures/review/drake3_clay_side.png|480]] ![[Assets/FantasyCreatures/review/drake3_clay_34.png|480]]
![[Assets/FantasyCreatures/review/drake3_clay_front.png|480]] ![[Assets/FantasyCreatures/review/drake3_clay_head.png|480]]

The review OBJ and the `*_fast.png` previews are gitignored, because they are regenerated by the run below.

- **Run:** `blender -b --factory-startup -P build_creatures.py -- drake3`
  - Add `fast` for 40-sample previews with no export.
  - Add `headonly` for a four-view head turnaround (`review/drake3_hd_*.png`).
- **Output** (`Assets/FantasyCreatures/review/`):
  - `drake3_clay_side/front/34.png` (the three review views), `drake3_clay_head.png`, `drake3_clay_headfront.png`;
  - `drake3_clay.obj` (high-res review mesh, ~746k tris, not a game mesh);
  - `drake3_dims.json`, plus a gitignored `FantasyCreatures_drake3_clay.blend`.
  - The OBJ was imported into Holden's live Blender (scene "FantasyCreatures", collection `Drake_v3_clay`). The v2 objects there are hidden, not deleted.
- **Anatomy as built:**
  - **Body:** deep keeled ribcage, displaced rib bands, tucked waist, pelvis with iliac crests, paired back muscles with a spine valley, scapulae standing above the back.
  - **Front legs:** a pointed elbow (olecranon) and a carpal spur.
  - **Hind legs:** a thigh blended into the flank, kneecap, calf, Achilles cord and heel spur.
  - **Toes:** gripping, with raised knuckles and claws hooked into the ground.
  - **Pose:** head lowered about 0.8 below the withers, skull pitched −18°, horns sweeping back along the neck.
  - **Wings:** about 7.9 units span against a 15-unit body. Each wing arm is its own SDF (humerus, pointed elbow, wrist, metacarpals) with two-phalanx fingers, and the membranes are 0.018 thick. The trailing membrane is raycast onto the flank, so it attaches along the body instead of floating.
  - **Back:** long, low overlapping dorsal scutes that are tallest over the shoulders, with a smooth tail tip.
- **Head** (the hardest part; three redesigns): a convex wedge skull, widest at the cheekbones. The brow ridge is the highest point and overhangs a small slit eye that has upper and lower lid rims.
  - Also: sagittal crest, temporal hollow, flared cheekbones, paired nasal ridges, nostril bosses with slits.
  - The jaw is deep at its back corner, has a flat masseter, and three jaw-angle spines.
  - The mouth is closed with an overbite, and its line does not turn up into a grin. Teeth are varied and curved back, with a big upper canine and a lower fang in a notch.
  - The whole head is scaled ×1.12 (`D3_HEAD_SCALE`).
- **Techniques added** (local observations):
  - `P_hull`: a convex-polytope SDF built from points (smooth max of the hull planes), for hard bony planes.
  - `P_ell_ab`: an ellipsoid between two points, for muscle bellies sunk into the limb core.
  - `sdf_obj(post=)`: displacement along the normal on the final surface, for ribs.
- **What fixed the "balloon" look:** muscle ellipsoids placed outside the limb with k ≈ 0.2 read as separate balls, and joint spheres read as beads. Large masses with k ≈ 0.3, long muscle bellies mostly inside the bone cone, and pointed bony landmarks (elbow, heel) fixed it.
- **Head lessons:**
  - A box skull with a long flat snout reads as a crocodile or duck. A wedge (wide cheeks, narrow deep muzzle) plus a brow that steps down to the muzzle reads as a dragon.
  - A smooth eyeball reads as a button in clay until lid rims are added.
  - Thin hull ridges below about 2 grid cells alias into "beads", so make them round (an ellipsoid ridge) or wider.
- **Known weak points** (told to Holden):
  - In profile the wing's upper arm still reads a little like a cone rising from the shoulder.
  - The brow plates are flat slabs.
  - The tail scutes still look slightly serrated.
  - The forearms and toes are leaner than ideal.
  - The neck is long.
- **Next, only after approval:**
  - surface pass: plates over the back and shoulders following the anatomy, finer joint scales, restrained wear;
  - colour: charcoal, dark crimson and muted bone, with a few deliberate ember cracks and quiet dark areas;
  - then VFX, sheet re-render and text (remove "young drake / big head / small wings"), republish the canvas to the same URL, and a decimated game OBJ (about 10k tris).

## Drake v3 surface + colour pass (2026-10-04)
Holden approved the v3 anatomy: "approved, fix weak points then start the surface and colour pass".

**Status: colour pass built and shown to Holden, waiting for his critique.** VFX, the sheet update and the game export have not been done yet.

- **Run:** `blender -b --factory-startup -P build_creatures.py -- drake3col`
  - Add `fast` for 48-sample previews; `light:1.5` scales the studio rig.
  - Output: `review/drake3_col_{hero,side,front,head,back,throat}.png`, plus a gitignored `FantasyCreatures_drake3_colour.blend`. Open that file in Blender to orbit with the materials, since the MCP's safe mode cannot load external .blend data.
- **Weak points fixed first:**
  - neck shortened 0.28;
  - wing elbow moved out to (2.0, 0.05, 4.5), with a bigger flight muscle and a triceps cord;
  - brow ridge has a crest line instead of a flat slab, plus two bony knobs per side;
  - central crest stops at the hips, and paired scutes run down the tail;
  - forearms, wrists, hands, shanks, toes and claws thickened.
- **Surface pass (geometry):**
  - `d3_surface_parts` builds keeled scutes that are raycast onto the body, with the front edge tucked in and the trailing edge lifted so rows shingle (`d3_scute`).
  - Rows: one on the neck, two staggered rows per side over the back and shoulders, and one down the tail, tapering to the tip.
  - Each scapula gets a three-plate pauldron.
  - Each eye gets a slit pupil, and an ember ribbon sits inside the closed mouth.
- **Colour pass (materials):**
  - **Skin:** `D3_Skin` reads per-vertex masks from `d3_skin_attrs`: `vs`, `vent`, `dors`, `joint`, `face`, `ember`.
  - **Scales:** large over the back and flanks, fine at joints, feet, the tail tip and the face, stretched ×1.4 along the body. They are domed (F1 height) with thin near-black crimson seams.
  - **Palette:** charcoal back, dark crimson low on the flanks and on the ventral scutes.
  - **Ember** in only three places: the seams between throat and chest scutes, the eyes, and a faint mouth seam.
  - **Plates and keratin:** matte charcoal keratin with growth lines and patchy chipped bone rims (restrained wear). Horns, claws and teeth grade from charcoal to muted bone.
  - **Membranes:** dark crimson, darker along the bones, with a faint vein network; translucent so they show red when backlit.
- **Lessons** (local observations):
  - **Polka dots, root cause:** the seams used Voronoi **F1 distance** (to the cell's centre point), which leaves round light centres inside wide dark rings. Use the **DISTANCE_TO_EDGE** feature for seams. F1 is fine for height (domes), never for colour.
  - **Per-cell variation on near-black skin must be multiplicative and darken-only.** A 6% mix toward grey made cells about 25% brighter, and seams lighter than the charcoal glowed.
  - **Pointiness-based skin wear reads as grey leopard blotches.** Keep wear on plates, horns and claws.
  - **A "throat" mask must exclude upward-facing normals.** On a lowered neck the top surface also faces forward, so ember spread over the whole neck.
  - **Chrome look:** plates and horns at roughness 0.35 with clearcoat read as chrome under studio rims. Use roughness 0.5–0.66 with no coat.
  - **Ember as a Voronoi crack network everywhere read as lava skin.** Glow in the scute seams is the restrained version.
- **Known weak points** (told to Holden):
  - the wing arms still read a little like tubes from some angles;
  - the shoulder plates look like flat panels;
  - scale size is uniform within each zone (there are no larger head plates);
  - all of this is procedural shading. The 1024 game texture will carry the colour and seams, but bump/relief needs a baked normal map (a SurfaceAppearance) to survive in Roblox.
  - All four were addressed in the next round (below).

## Drake v3 game export: SurfaceAppearance maps (2026-10-04)
Holden chose "colour plus normal and roughness map, we want this high quality". **Status: exported and previewed, waiting for Holden's review.** It has not been imported into Studio.

- **Weak points fixed first:**
  - **Wing arms:** a leading-edge skin web (flattened in the wing plane), knobbly carpals, an elbow spur, and nine small keeled scutes down each humerus and forearm. They no longer read as tubes.
  - **Shoulder pauldron:** four domed "shield" plates with a cascade overlap (`d3_scute(shape="shield", dome=…)`).
  - **Head plates:** bony plates on the brow crest, crown and nasal ridges. The top of the skull keeps large scales and the sides get fine ones (the `face` mask × head-up normal).
    - Cheek and jaw plates were tried and removed: on steep sides they read as stuck-on buttons.
  - **Scutes:** now top + rim only. The never-seen undersides had been wasting UV space.
- **Run:** `blender -b --factory-startup -P build_creatures.py -- export3`. About 1.5 minutes in total; each bake pass takes 1–2 s.
- **Output** (`models/CinderDrake/`):
  - `CinderDrake.obj/.mtl` with objects `CinderDrake_Body` (16,490 tris since the re-export with the mouth interior; first export 16,266), `CinderDrake_Wings` (3,648) and `CinderDrake_Glow` (160, Neon eyes). Total 20,298. The 20k cap is per MeshPart, so that's fine. Size 8 × 7.6 × 14.5 studs.
  - `CinderDrake_Body_{Color,Normal,Roughness,Emissive}.png` and `CinderDrake_Wings_{Color,Normal,Roughness}.png`, all 1024².
  - `build_report.json` (SurfaceAppearance values, attachments in Roblox axes), `IMPORT.md` (every file, where it goes, importer settings, SurfaceAppearance steps), `preview_game_{hero,head,back34}.png`.
  - The v2 export moved to `models/CinderDrake/_v2/`.
- **Texture quality** (measured from the UVs):
  - skin at **80 px/stud**; 61% of the texture is used by islands;
  - 10 body islands (they started at 559);
  - each part type gets a weighted share: skin 1.0, wing arm 0.9, horns and shoulder plates 0.7, head plates 0.6, scutes 0.5, teeth and claws 0.45.
- **Emissive:** Roblox multiplies emissive by the ColorMap, so glowing texels are painted ember orange in the ColorMap. The mask is the normalised EMIT bake with a 0.12 threshold. Recommended EmissiveStrength is 6 (tune 3–8).
- **Lessons** (local observations):
  - **Bake speed:** selected-to-active with ~300 high objects took **323 s per pass**, because Blender raycasts every selected object per texel on the CPU. Joining the high-res parts into one proxy (`d3_bake_proxy`, `preserve_all_data_layers=True` keeps the shader attributes) brought it to **1.5 s**.
  - **Decimation speed:** `decimated_copy` runs two full depsgraph updates per object, which took over 10 minutes for 300 parts. `batch_decimated` does it in two updates total (~3 s).
  - **AO nodes in the bake:** set `only_local` on AO nodes, or AO sees the low-poly lying on the high-res.
  - **Selecting faces for UV operators:** setting `polygon.select` in object mode is ignored. Entering edit mode rebuilds the selection from the vertex flags. Select through `bmesh.from_edit_mesh` in face-select mode.
  - **Creature UV layout:**
    - anatomical regions from face centroids, majority-vote smoothed (raw thresholds made 287 one-face islands);
    - ring seams at region changes, plus one Dijkstra seam per region along its underside (cost rises on up-facing or outward-facing edges);
    - angle-based unwrap. SLIM "minimum stretch" failed on 27 of 41 islands;
    - neck+head unwrapped whole folded over itself (2,881 overlap px at 512²) and put throat embers on the face. Splitting it into left/right halves dropped that to 113 px;
    - feet and toes, and the wing hand beyond 90% of the forearm, go to smart UV;
    - plates get one planar island each, with the rim pushed out as a skirt (zero-area rim UVs break tangents).
  - **Normal bake:** double the skin bump for the NORMAL pass only (plates ×1.5) so scale seams survive 80 px/stud.
  - **The mouth-glow ribbon** must be a closed sliver (Solidify 0.006). Single-sided, it baked an inverted normal.
- **Known limits:**
  - the palate vault, tongue and lower teeth are modelled, but with the jaw shut the edges of the roof and floor of the mouth bake each other's surface. This is invisible while closed; an open-mouth pose needs a rig and a re-bake;
  - teeth and arm hands have small UV folds (harmless at one colour);
  - ⚠️ verify in Studio: MikkTSpace match, the emissive look, and low-quality / mobile appearance.

## Drake v3 VFX + sheet update (2026-10-04)
Holden: "go ahead with the VFX and sheet update". **Status: done, waiting for Holden's review.** Nothing has been built or tested in Studio.

- **Sheet.**
  - **Render set:** `build_creatures.py -- drake3sheet all` renders the v3 set into `design/renders/`:
    - hero;
    - side/front/back orthos at 64 px/stud;
    - four portrait pose cards: STALK, ALERT, ROAR, FIRE BREATH;
    - eight part cards (new: pauldrons) and eight material balls (new: crimson flank);
    - the VFX key with projected anchor points;
    - scale panel and volcanic habitat diorama.
  - **Board and canvas:** `Main.dc.html` was rewritten around this set. The v2 renders are kept in `design/renders/_v2/`, and the canvas was republished to the same URL (version 7).
- **VFX previews (Blender).** Camera-facing cards with [[VFX-Texture-Pack]] textures:
  - nostril smoke (smoke_puff);
  - ember drift (spark_dot);
  - a throat point light;
  - fire breath: fire-flipbook cards along a widening cone going white-yellow → orange → dark red, a slim faint emissive core, sparks, smoke-flipbook cards off the far end, and a point light.
- **Game re-export.** `export3` was re-run so the OBJ matches the sheet: the palate vault, tongue trough and lower tooth row are now in.
  - Body 16,490 tris; total 20,298 (the 20k cap is per MeshPart).
  - The whole export, including the bakes and three previews, now takes about 40 s.
  - The previous export is in the session scratchpad, not the vault.
- **Roblox VFX spec (data only; scripts are "not yet").** `models/CinderDrake/VFX.md` + `vfx_spec.json`:
  - **4 attachments on the Body:** NostrilL/R, ThroatFX (just under the throat) and BreathFX (just in front of the lips, tilted −12°).
  - **7 emitter instances:** NostrilSmoke ×2, EmberDrift, and BreathFlame/BreathCore/BreathSparks/BreathSmoke.
  - **2 PointLights:** ThroatLight (ambient) and BreathLight (trigger).
  - **Budget:** ambient 9 particles/s (about 19 live). Breath 124/s over 4 emitters, the largest 60/s (about 66 live). Both are inside the [[VFX-Particles-Beams-Trails]] budgets.
  - **Textures (spec v2):** 4 unique: smoke_flip 1024², smoke_puff 256², spark_dot 128², and Hoard `Glow.png` 128². The breath flames are smoke_puff tinted fire colours with additive blending, and the breath smoke plays OneShot.
  - **Lint:** checked by hand against the roblox-vfx-review rules. Everything passes except an expected `stream-in-burst` warning, because the breath is channelled. The Studio lint and phase freeze haven't been run.
- **Lessons (local observations):**
  - **Posed builds:** place the parts against the rest-pose body (BVH), then pose. Compute the skin masks in rest space: head and jaw vertices are mapped back through the bone inverse, so the throat ember strip and face zones don't slide when the neck moves.
  - **Pose cards are portrait** (400×520, front-3/4, lens 34). Landscape side renders made a sliver of a drake in a narrow card, and the card CSS cropped the head.
  - **Fire breath:** a full flame cone reads as a solid horn. Keep only a slim faint core and let the cards carry the look. The first framing also clipped the jet at the frame edge.
  - **Pack fire flipbook:** `VFX_fire_flip4x4` frames are torch flames cut flat at the base, so the breath's cards stacked into a hard-edged slab.
    - Spec v2 and the re-rendered previews use soft smoke_puff cards tinted hot-to-cool, plus a Glow core.
    - The smoke flipbook fades over its 16 frames, so it plays OneShot; the preview picks frames in that order.
    - See [[VFX-Texture-Pack]] → Pitfalls.
  - **Board cards:**
    - captions must fit one line (about 28 characters at 11 px Barlow Condensed in a 156 px card); longer ones wrapped into a clipped second line;
    - card tags (`.pill`) were drawn under opaque renders.
    - `sheet.css` now forces one line with an ellipsis and puts the tags on `z-index: 2`. This applies to all three boards; two golem captions were shortened.
  - **Attachment frame:** an Attachment's Position is relative to the MeshPart's centre, which is the centre of its bounding box (0.003, 3.647, 1.789 from the drake's pivot), not the imported pivot. The spec gives both frames. ⚠️ verify in Studio with `Visible` attachments.
  - **Emitters on Attachments spawn from a point.** Shape doesn't spread them, so EmberDrift fires down and sideways (SpreadAngle 70) and then rises. Pointing it straight up would hide the sparks inside the neck.
  - **Static-mesh limit:** the jaw can't open. The breath starts in front of the closed lips and is hidden by BreathCore's white-hot flare (ZOffset 0.8). A rig would parent BreathFX to the head/jaw.
  - **Breath aim:** the head is pitched about 25° down, so a breath along the head axis would hit the ground about 4.6 studs out. −12° keeps the roughly 6-stud jet above flat ground.

## Open questions / to verify in Studio
- ⚠️ verify (drake VFX): the attachment markers land on the nostrils, throat and lips; the breath reaches about 6 studs (Drag semantics); the additive fire doesn't wash out on bright skies; frame time on a low-end phone with the breath running. Full list in `models/CinderDrake/VFX.md`.
- ⚠️ verify: whether the 3D Importer turns a multi-object OBJ into one Model with three MeshParts (expected) and keeps the object names.
- ⚠️ verify: whether `_Body` and `_Crystals` (two MTL materials with the same `map_Kd`) upload the PNG twice. The Hoard notes say per-model copies do, so repoint to one TextureID.
- ⚠️ verify: whether the Neon parts take the MTL `Kd` as `Color` (otherwise the setup script sets it), and how Glass crystals look on low-end mobile (no refraction there).
- ⚠️ verify: OBJ unit handling (authored 1 unit = 1 stud). Compare the import sizes against `size_studs` in each `build_report.json`.
- Still to build after Holden approves the plan: `CreatureVFX.luau` (client module), `CreatureSetup.luau` (command bar: pivots, attachments from the report, materials, collision), `DevCreatureDemo.client.luau` (Studio only), and the zip. The drake's `IMPORT.md` exists. `vfx_spec.json` is laid out so a setup script can build every attachment, emitter and light from it.

## Related
- [[Dragons-Hoard-Set]] · [[VFX-Texture-Pack]] · [[Blender-To-Roblox-Pipeline]] · [[Blender to Roblox Asset Pipeline]] · [[VFX-Particles-Beams-Trails]]
- [[Art Direction Feedback]] · [[AI-Assisted-Workflow]] · [[Prompt-Library]] · [[Shaders-Materials-And-Surfaces]] · [[Animation-Rigging-And-IK]]

## Sources
- Holden's brief, the Kingshot reference-sheet screenshot and Discord advice ("will"), Claude session 2026-10-04.
- Pipeline and art rules: `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md`; the golem habitat uses `models/trees/Tree_Green_1–5.glb` from that library.
- Build output: `Assets/FantasyCreatures/models/*/build_report.json`.
- Round-cone and ellipsoid SDF formulas: Inigo Quilez, "distance functions" — https://iquilezles.org/articles/distfunctions/

