---
tags: [visuals/art-direction, visuals/3d, assets/creatures]
status: draft
updated: 2026-10-04
confidence: medium
---
# Creature Anatomy and Proportions

How to judge and fix the limb proportions of four-legged creatures (dragons, beasts, golems), with real-animal numbers.

Written after Holden said the Cinder Drake's legs "feel a bit skinny" (2026-10-04). See [[Fantasy-Creatures-Set]].

## TL;DR
- **Measure, don't eyeball.** Slice the high-res mesh at fixed heights and compare each limb's average thickness ((width + depth) / 2) with shoulder height. Game meshes are too sparsely decimated to measure.
- **Big-cat benchmark.** A lion's forearm girth averages about 48 cm at about 110 cm shoulder height; a tiger's is about 49 cm.
  - That means the forearm's average diameter at its thickest point (just below the elbow) is about **0.14 × shoulder height**.
  - ⚠️ verify: these are community-compiled measurements, not a peer-reviewed table.
- **Heavier animals have proportionally stouter legs** ("elastic similarity": bone diameter grows faster than bone length as mass rises).
  - A big, armoured, winged predator should be at or above lion ratios.
  - Target **0.14–0.17** for the forearm.
- **Keep the joints readable.**
  - The upper arm (deltoid + triceps) is thicker than the forearm; the forearm is "ropey" rather than bulky.
  - The wrist is about **0.7–0.75 ×** the top of the forearm.
  - The thigh is broad, and the calf (gastrocnemius) ends in a tendon groove to the heel.
- **Landmarks:**
  - elbow about level with the knee;
  - middle toe longest;
  - forelegs leave the bottom-front of the chest;
  - a flier's wings are at least as long as its body.
- **Feet scale with the legs.** Foot width is about 1.8–2.0 × wrist width, and the toes must stay thick enough to read on a phone.

## Worked example: Cinder Drake v3 → v3.1
Shoulder height is 4.3 studs. Measured on the high-res clay OBJ (`review/drake3_clay.obj`), average of width and depth, in studs.

| Slice | v3 | v3.1 | v3.1 ÷ shoulder height |
|---|---|---|---|
| Forearm top (just below the elbow) | 0.49 | **0.64** | 0.149 (lion ≈ 0.14) |
| Mid forearm | 0.45 | 0.60 | 0.138 |
| Wrist | 0.37 | 0.48 | 0.11 (wrist ÷ forearm top = 0.74) |
| Front foot width | 0.68 | 0.84 | — |
| Hind metatarsus (between ankle and toes) | 0.31 | **0.45** | 0.105 |
| Hind foot width | 0.68 | 0.84 | — |

**What changed** (`build_creatures.py`: `d3_front_leg`, `d3_hind_leg`, `D3_FTOES`/`D3_BTOES`, `D3_TAIL`):
- **Bone cores:** forearm 0.24→0.31 at the top, 0.16→0.20 at the wrist; metatarsus 0.17→0.22.
- **Muscle bellies** grew about 25–35% and sit in the upper half of each segment, so the joints below stay narrower.
- **Toes:** radius +20% and length +10%, with wider spacing.
- **Claws** +10–15%.
- **Tail** radii +12–20%, so the heavier legs aren't balanced by a whip-thin tail.
- **Feet** moved about 0.06 studs outward, so the thicker legs don't make the stance look pinched from the front.

## Checklist for a new creature
- [ ] Note the shoulder height and the hip height.
- [ ] Measure the forearm top, wrist, shank and metatarsus on the high-res mesh (script below), and compare them with the targets above.
- [ ] Check the taper: wrist ÷ forearm top between 0.7 and 0.8. Below 0.65 looks spindly; above 0.85 looks like a column or sausage.
- [ ] Check the feet against the wrist (width about 1.8–2.0 ×) and look at the toes at phone size.
- [ ] Look at the front view: thicker legs narrow the stance, so move the feet out if needed.
- [ ] Look at the tail: heavier limbs need a heavier tail base.
- [ ] Compare before/after clay renders side by side (`review/drake3_clay_*.png`) before any texture work.

Measuring (Blender's bundled Python, numpy; run on the high-res OBJ, which is Y-up with front = -Z):

```python
# scratch script: slice a limb at height h and report its width (X) and depth (Z)
import numpy as np
V = np.array([l.split()[1:4] for l in open("drake3_clay.obj") if l.startswith("v ")], dtype=np.float32)
def slice_limb(h, zr, dh=0.012, xmin=0.45):
    p = V[(abs(V[:, 1] - h) < dh) & (V[:, 0] > xmin) & (V[:, 2] > zr[0]) & (V[:, 2] < zr[1])]
    return np.ptp(p[:, 0]), np.ptp(p[:, 2])
```

## Pitfalls
- **Balloon muscles and sausage legs** (Holden's rule, [[Art Direction Feedback]]):
  - thickening by adding round muscle balls outside the limb reads as beads;
  - thickening the whole limb evenly reads as a tube.
  - Grow the bone core, keep long muscle bellies mostly inside it, and keep bony landmarks (elbow point, heel, carpal spur).
- **Long legs read as skinny.** If the legs still look thin at the right thickness, check that the lower segments (forearm, metatarsus) aren't also too long.
- **Lion-only numbers undersell a dragon.** A winged, armoured animal several times a lion's mass needs more than 0.14. Stop around 0.17, or it turns into a cartoon.
- **Slices of slanted limbs over-read depth.** Compare like for like (same heights, same mesh) instead of trusting single absolute values.

## Related
- [[Fantasy-Creatures-Set]] · [[Art Direction Feedback]] · [[Art-Direction]] · [[Blender-To-Roblox-Pipeline]] · [[Animation-Rigging-And-IK]]

## Sources
- Lion and tiger forearm girth (lion average 18.88 in ≈ 48 cm, tiger 19.43 in ≈ 49.4 cm, about 53 cm maximum). These are community-compiled forum figures, ⚠️ not peer-reviewed: "Lion and tiger forearm/upper arm data", Animal Untamed forum — https://www.tapatalk.com/groups/animaluntamed/lion-and-tiger-forearm-upper-arm-data-t451.html (accessed 2026-10-04 via search summary).
- Lion shoulder height about 110 cm (Addis Ababa zoo average) and tigers 99–130 cm, from the same forums — https://www.tapatalk.com/groups/animalsversesanimals/shoulder-height-of-lions-and-tigers-t2578-s30.html (accessed 2026-10-04).
- Elastic similarity, and proximal limb bone circumference scaling with body mass in quadrupeds: Campione & Evans 2012, BMC Biology 10:60 — https://bmcbiol.biomedcentral.com/articles/10.1186/1741-7007-10-60 ; "Where Have All the Giants Gone?", PLOS Biology 2017 — https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.2000473
- Big-cat leg drawing guidance (thick deltoid and triceps, ropey forearm, calf with a tendon divot, low wrist and heel): John Muir Laws, "How to Draw a Mountain Lion: anatomy" — https://johnmuirlaws.com/draw-mountain-lion-anatomy/
- Dragon proportion rules (elbow level with knee, middle toe longest, wings at least body length): Monika Zagrobelna, "How to Draw an Anatomically Correct Dragon", Envato Tuts+ — https://design.tutsplus.com/articles/rawr-how-to-draw-an-anatomically-correct-dragon--vector-16561
- Forelegs from the bottom-front of the chest, and monitor lizards as a limb reference — https://skyryedesign.com/art/dragon-drawing/
- Local measurements: `Assets/FantasyCreatures/review/drake3_clay.obj`, before (13:05) and after (16:12) the 2026-10-04 proportions pass.
