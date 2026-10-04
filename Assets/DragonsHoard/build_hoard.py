# Dragon's Hoard set — builds all 11 models from scratch, exports OBJ+MTL per model,
# a shared colour atlas, particle textures, preview renders and build_report.json.
#
# Run headless:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --factory-startup --python build_hoard.py
#
# Units: 1 Blender unit = 1 stud. Blender Z-up; OBJ export maps to Roblox as (x, z, -y).
# Front of every model faces Blender +Y (= Roblox -Z, the LookVector).

import bpy, bmesh, math, random, os, json
import numpy as np
from mathutils import Vector, Matrix

OUT = os.path.dirname(os.path.abspath(__file__))
ATLAS = 512
GRID = 8

# ---------------------------------------------------------------- palette (8x8 atlas cells)
PALETTE = [
    ("gold_dark", (178, 112, 20)), ("gold", (242, 180, 36)), ("gold_light", (255, 214, 76)), ("gold_pale", (255, 238, 150)),
    ("ember_dark", (112, 22, 18)), ("ember", (196, 46, 26)), ("ember_orange", (240, 112, 32)), ("ember_tip", (255, 172, 64)),
    ("frost_dark", (44, 92, 164)), ("frost", (92, 162, 224)), ("frost_light", (172, 216, 246)), ("frost_white", (236, 248, 255)),
    ("venom_dark", (28, 74, 40)), ("venom", (62, 152, 62)), ("venom_lime", (156, 214, 70)), ("venom_purple", (104, 48, 138)),
    ("venom_purple_light", (166, 96, 196)), ("wood_dark", (88, 50, 26)), ("wood", (140, 86, 46)), ("wood_light", (182, 122, 66)),
    ("wood_inside", (58, 34, 20)), ("steel_dark", (104, 114, 130)), ("steel", (172, 182, 198)), ("steel_light", (226, 233, 242)),
    ("grip", (156, 32, 36)), ("grip_dark", (98, 20, 26)), ("ruby_dark", (130, 14, 40)), ("ruby", (212, 34, 64)),
    ("ruby_light", (255, 112, 130)), ("sapphire_dark", (24, 50, 150)), ("sapphire", (44, 96, 226)), ("sapphire_light", (120, 170, 255)),
    ("emerald_dark", (12, 104, 58)), ("emerald", (30, 172, 92)), ("emerald_light", (120, 232, 160)), ("amethyst_dark", (84, 32, 136)),
    ("amethyst", (142, 62, 206)), ("amethyst_light", (202, 146, 255)), ("velvet", (150, 28, 52)), ("velvet_dark", (96, 16, 36)),
    ("wine", (120, 10, 34)), ("keyhole", (28, 20, 16)),
]
C = {name: i for i, (name, _) in enumerate(PALETTE)}
GEMS = {
    "ruby": (C["ruby"], C["ruby_light"], C["ruby_dark"]),
    "sapphire": (C["sapphire"], C["sapphire_light"], C["sapphire_dark"]),
    "emerald": (C["emerald"], C["emerald_light"], C["emerald_dark"]),
    "amethyst": (C["amethyst"], C["amethyst_light"], C["amethyst_dark"]),
}
GEM_ORDER = ["ruby", "sapphire", "emerald", "amethyst"]


def by_normal(top, side, bottom=None, thresh=0.6):
    bottom = side if bottom is None else bottom
    def fn(n, c):
        if n.z > thresh:
            return top
        if n.z < -thresh:
            return bottom
        return side
    return fn


# ---------------------------------------------------------------- bmesh helpers
def new_bm():
    bm = bmesh.new()
    return bm, bm.faces.layers.int.new("col")


def add_face(bm, lay, verts, col, interior=None):
    f = bm.faces.new(verts)
    f.normal_update()
    if interior is not None and f.normal.dot(f.calc_center_median() - interior) < 0:
        f.normal_flip()
    f[lay] = col
    return f


def lathe(bm, lay, profile, segs, cols, M=None, theta0=0.0, col_fn=None, closed=False):
    """Revolve (r, z) profile around Z. Profile must trace the solid's outline so that the
    outside is on the right of travel (bottom-centre -> out -> up -> top-centre)."""
    rings = []
    for r, z in profile:
        if r < 1e-6:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(theta0 + 2 * math.pi * j / segs),
                                        r * math.sin(theta0 + 2 * math.pi * j / segs), z)) for j in range(segs)])
    pairs = list(range(len(rings) - 1))
    if closed:
        pairs.append(-1)
    for i in pairs:
        a, b = rings[i], rings[i + 1] if i >= 0 else rings[0]
        ci = i if i >= 0 else len(rings) - 1
        for j in range(segs):
            j2 = (j + 1) % segs
            col = col_fn(ci, j) if col_fn else cols[ci]
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                vs = [a[0], b[j2], b[j]]
            elif len(b) == 1:
                vs = [a[j], a[j2], b[0]]
            else:
                vs = [a[j], a[j2], b[j2], b[j]]
            f = bm.faces.new(vs)
            f[lay] = col
    allv = [v for ring in rings for v in ring]
    if M is not None:
        bmesh.ops.transform(bm, matrix=M, verts=allv)
    return rings


def hull(bm, lay, points, col, M=None):
    M = M or Matrix.Identity(4)
    pts = [M @ Vector(p) for p in points]
    centre = sum(pts, Vector()) / len(pts)
    verts = [bm.verts.new(p) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=verts, use_existing_faces=False)
    faces = [g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)]
    unused = [g for g in res["geom_interior"] + res["geom_unused"] if isinstance(g, bmesh.types.BMVert)]
    if unused:
        bmesh.ops.delete(bm, geom=unused, context="VERTS")
    for f in faces:
        if not f.is_valid:
            continue
        f.normal_update()
        if f.normal.dot(f.calc_center_median() - centre) < 0:
            f.normal_flip()
        f[lay] = col(f.normal, f.calc_center_median()) if callable(col) else col
    return faces


def box(bm, lay, mn, mx, col, M=None):
    pts = [(x, y, z) for x in (mn[0], mx[0]) for y in (mn[1], mx[1]) for z in (mn[2], mx[2])]
    return hull(bm, lay, pts, col, M)


def align_z(d):
    d = Vector(d).normalized()
    up = "X" if abs(d.y) > 0.95 else "Y"
    return d.to_track_quat("Z", up).to_matrix().to_4x4()


def gem(bm, lay, M, s, kind, sides=6):
    main, light, dark = GEMS[kind]
    pts = []
    for k in range(sides):
        a = 2 * math.pi * (k + 0.5) / sides
        pts.append((0.55 * s * math.cos(a), 0.55 * s * math.sin(a), 0.32 * s))
        a2 = 2 * math.pi * k / sides
        pts.append((s * math.cos(a2), s * math.sin(a2), 0.05 * s))
    pts.append((0, 0, -0.75 * s))

    def fn(n, c):
        ln = (M.to_3x3().inverted() @ n).normalized()
        if ln.z > 0.95:
            return light
        if ln.z > 0.05:
            return light if int(round(math.atan2(ln.y, ln.x) / (math.pi / sides))) % 2 else main
        return dark
    return hull(bm, lay, pts, fn, M)


def coin(bm, lay, M, rng, segs=8, r=0.25, t=0.06):
    top = rng.choice([C["gold"], C["gold_light"], C["gold_light"], C["gold_light"], C["gold_pale"]])
    lathe(bm, lay, [(0, 0), (r, 0), (r, t), (0, t)], segs, [C["gold_dark"], C["gold"], top], M=M,
          theta0=rng.uniform(0, 1))


# ---------------------------------------------------------------- object + UV + material
def make_atlas():
    px = np.zeros((ATLAS, ATLAS, 4), dtype=np.float32)
    px[..., 3] = 1.0
    cell = ATLAS // GRID
    for i, (_, rgb) in enumerate(PALETTE):
        cx, cy = i % GRID, i // GRID
        px[cy * cell:(cy + 1) * cell, cx * cell:(cx + 1) * cell, :3] = np.array(rgb) / 255.0
    # unused cells: neutral grey so a stray UV is obvious
    for i in range(len(PALETTE), GRID * GRID):
        cx, cy = i % GRID, i // GRID
        px[cy * cell:(cy + 1) * cell, cx * cell:(cx + 1) * cell, :3] = 0.5
    path = os.path.join(OUT, "textures", "HoardAtlas.png")
    save_png(px, path, "HoardAtlas_tmp")
    img = bpy.data.images.load(path)
    img.name = "HoardAtlas"
    return img


def save_png(px, path, name):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    h, w = px.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=True)
    img.colorspace_settings.name = "sRGB"
    img.pixels.foreach_set(px.ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def make_material(img):
    mat = bpy.data.materials.new("HoardAtlas")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
    bsdf.inputs["Roughness"].default_value = 0.6
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def uv_atlas(bm, lay):
    uv = bm.loops.layers.uv.new("UVMap")
    pad, inner = 0.2, 0.6
    for f in bm.faces:
        col = f[lay]
        cx, cy = col % GRID, col // GRID
        n = f.normal if f.normal.length > 0.5 else Vector((0, 0, 1))
        t = n.orthogonal().normalized()
        b = n.cross(t)
        co = [(l.vert.co.dot(t), l.vert.co.dot(b)) for l in f.loops]
        us, vs = [c[0] for c in co], [c[1] for c in co]
        du, dv = max(us) - min(us), max(vs) - min(vs)
        for l, (a, c) in zip(f.loops, co):
            nu = (a - min(us)) / du if du > 1e-6 else 0.5
            nv = (c - min(vs)) / dv if dv > 1e-6 else 0.5
            l[uv].uv = ((cx + pad + nu * inner) / GRID, (cy + pad + nv * inner) / GRID)


def finish(name, bm, lay, mat):
    bm.normal_update()
    uv_atlas(bm, lay)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False
    me.validate()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


# ---------------------------------------------------------------- models
def make_egg(name, style, seed, mat):
    rng = random.Random(seed)
    bm, lay = new_bm()
    H, R = 1.6, 0.55
    body = style["body"]

    def surf(phi, th):
        u = (1 - math.cos(phi)) / 2
        r = R * math.sin(phi) * (1.06 - 0.24 * u)
        return Vector((r * math.cos(th), r * math.sin(th), H * u))

    def nrm(phi, th):
        e = 1e-3
        n = (surf(phi, th + e) - surf(phi, th - e)).cross(surf(phi + e, th) - surf(phi - e, th)).normalized()
        p = surf(phi, th)
        if n.dot(p - Vector((0, 0, H * 0.45))) < 0:
            n = -n
        return n

    phis = [0.45 + (math.pi - 0.45) * k / 8 for k in range(9)]
    prof = [(0, 0), (0.2, 0)] + [((lambda p: (p.xy.length, p.z))(surf(ph, 0))) for ph in phis]
    prof[-1] = (0, H)
    lathe(bm, lay, prof, 12, [body] * len(prof))

    rows = 8
    for i in range(rows):
        pt = 0.95 + (2.85 - 0.95) * i / (rows - 1)
        pb, pm = pt - 0.45, pt - 0.24
        n = max(5, round(13 * math.sin((pt + pb) / 2)))
        hw = math.pi / n * 1.08
        off = math.pi / n if i % 2 else 0.0
        for j in range(n):
            th = off + 2 * math.pi * j / n + rng.uniform(-0.05, 0.05)
            main, tip = style["plate"](i, j, rng)
            hint = surf(pm, th) - nrm(pm, th) * 0.15

            def lift(phi, a, out):
                return surf(phi, a) + nrm(phi, a) * out

            # rounded shingle: top edge tucked under the row above, free edge lifted
            p2 = pb + 0.11
            outline = [(pt, th - hw * 0.8, -0.006), (pm, th - hw, 0.032), (p2, th - hw * 0.62, 0.044),
                       (pb, th, 0.052), (p2, th + hw * 0.62, 0.044), (pm, th + hw, 0.032), (pt, th + hw * 0.8, -0.006)]
            o = [bm.verts.new(lift(*q)) for q in outline]
            inn = [bm.verts.new(lift(q[0], q[1], -0.012)) for q in outline[1:-1]]
            TL, L1, L2, TP, R2, R1, TR = o
            add_face(bm, lay, [TL, L1, R1, TR], main, hint)
            add_face(bm, lay, [L1, L2, R2, R1], main, hint)
            add_face(bm, lay, [L2, TP, R2], tip, hint)
            add_face(bm, lay, [TL, inn[0], L1], body, hint)
            add_face(bm, lay, [R1, inn[-1], TR], body, hint)
            for a, b, ia, ib in ((L1, L2, inn[0], inn[1]), (L2, TP, inn[1], inn[2]),
                                 (TP, R2, inn[2], inn[3]), (R2, R1, inn[3], inn[4])):
                add_face(bm, lay, [a, ia, ib, b], body, hint)
    return finish(name, bm, lay, mat)


def ember_plate(i, j, rng):
    main = C["ember_orange"] if rng.random() < 0.12 else C["ember"]
    tip = C["gold_light"] if rng.random() < 0.18 else (C["ember_tip"] if i >= 6 else C["ember_orange"])
    return main, tip


def frost_plate(i, j, rng):
    main = C["frost_light"] if i >= 6 else C["frost"]
    tip = C["frost_white"] if (rng.random() < 0.22 or i >= 6) else C["frost_light"]
    return main, tip


def venom_plate(i, j, rng):
    # green at the base blending to purple at the crown, mixed per scale (no row stripes)
    if rng.random() < 0.1 + 0.75 * i / 7:
        return C["venom_purple"], (C["venom_purple_light"] if rng.random() < 0.8 else C["venom_lime"])
    return C["venom"], C["venom_lime"]


def make_coin(mat):
    rng = random.Random(4)
    bm, lay = new_bm()
    prof = [(0, 0.012), (0.19, 0.012), (0.25, 0.0), (0.25, 0.08), (0.2, 0.068), (0, 0.068)]
    lathe(bm, lay, prof, 10, [C["gold_dark"], C["gold_dark"], C["gold"], C["gold_light"], C["gold"]])
    em = [(0.08, 0, 0.066), (-0.08, 0, 0.066), (0, 0.11, 0.066), (0, -0.11, 0.066),
          (0.045, 0, 0.086), (-0.045, 0, 0.086), (0, 0.065, 0.086), (0, -0.065, 0.086)]
    hull(bm, lay, em, by_normal(C["gold_pale"], C["gold_light"], C["gold"]))
    return finish("Coin_Gold", bm, lay, mat)


def mound(bm, lay, rng, R, H, segs, rings):
    h = lambda r: H * max(0.0, 1 - (r / R) ** 2) ** 0.75
    prof = [(R * (1 - k / rings), h(R * (1 - k / rings))) for k in range(rings)] + [(0, H)]
    pal = [C["gold"], C["gold_dark"], C["gold_dark"], C["gold_light"]]
    rr = lathe(bm, lay, prof, segs, None, col_fn=lambda i, j: rng.choice(pal))
    for ring in rr[1:-1]:
        for v in ring:
            v.co.z += rng.uniform(-0.03, 0.03) * H
    return h


def scatter_coins(bm, lay, rng, h, R, count, rmin, rmax_f, base_z=0.0, xy_box=None, tilt=28, segs=8):
    for _ in range(count):
        if xy_box:
            p = Vector((rng.uniform(-xy_box[0], xy_box[0]), rng.uniform(-xy_box[1], xy_box[1]), base_z))
            n = Vector((0, 0, 1))
        else:
            r = R * (rmin + (rmax_f - rmin) * rng.random() ** 0.4)
            th = rng.uniform(0, 2 * math.pi)
            e = 1e-3
            slope = (h(r + e) - h(max(0, r - e))) / (2 * e)
            radial = Vector((math.cos(th), math.sin(th), 0))
            n = (Vector((0, 0, 1)) - radial * slope).normalized()
            p = radial * r + Vector((0, 0, h(r) + base_z)) - n * 0.02
        M = (Matrix.Translation(p) @ align_z(n) @ Matrix.Rotation(math.radians(rng.uniform(-tilt, tilt)), 4, "X")
             @ Matrix.Rotation(rng.uniform(0, 6.3), 4, "Z"))
        coin(bm, lay, M, rng, segs=segs)


def make_small_pile(mat):
    rng = random.Random(11)
    bm, lay = new_bm()
    R, H = 0.6, 0.38
    h = mound(bm, lay, rng, R, H, 10, 3)
    scatter_coins(bm, lay, rng, h, R, 11, 0.0, 0.9)
    for k in range(4):  # loose coins on the ground around the pile
        a = rng.uniform(0, 6.3)
        p = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(0.62, 0.72)
        coin(bm, lay, Matrix.Translation(p) @ Matrix.Rotation(rng.uniform(0, 6.3), 4, "Z"), rng)
    return finish("CoinPile_Small", bm, lay, mat)


def make_large_pile(mat):
    rng = random.Random(23)
    bm, lay = new_bm()
    R, H = 1.5, 1.15
    h = mound(bm, lay, rng, R, H, 16, 6)
    scatter_coins(bm, lay, rng, h, R, 50, 0.18, 0.98, segs=7)
    for k in range(6):  # loose ground coins
        a = 2 * math.pi * k / 6 + rng.uniform(-0.3, 0.3)
        p = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(1.45, 1.65)
        coin(bm, lay, Matrix.Translation(p) @ Matrix.Rotation(rng.uniform(0, 6.3), 4, "Z"), rng)
    for k in range(6):  # gems pushed into the pile
        r = R * rng.uniform(0.25, 0.8)
        a = 2 * math.pi * k / 6 + 0.4
        radial = Vector((math.cos(a), math.sin(a), 0))
        slope = (h(r + 1e-3) - h(r - 1e-3)) / 2e-3
        n = (Vector((0, 0, 1)) - radial * slope).normalized()
        p = radial * r + Vector((0, 0, h(r) + 0.04))
        M = Matrix.Translation(p) @ align_z(n) @ Matrix.Rotation(math.radians(rng.uniform(-30, 30)), 4, "X")
        gem(bm, lay, M, rng.uniform(0.09, 0.13), GEM_ORDER[k % 4])
    ob = finish("CoinPile_Large", bm, lay, mat)
    return ob, Vector((0, 0, H))


def make_goblet(mat):
    bm, lay = new_bm()
    P = [(0, 0), (0.28, 0), (0.28, 0.05), (0.2, 0.09), (0.07, 0.14), (0.06, 0.32), (0.11, 0.37), (0.11, 0.42),
         (0.06, 0.47), (0.09, 0.56), (0.27, 0.68), (0.33, 0.95), (0.33, 1.0), (0.30, 1.0), (0.285, 0.88), (0, 0.88)]
    g = C
    cols = [g["gold_dark"], g["gold_dark"], g["gold"], g["gold_light"], g["gold"], g["gold_light"], g["gold_pale"],
            g["gold_light"], g["gold"], g["gold_dark"], g["gold"], g["gold_pale"], g["gold_light"], g["gold_dark"], g["wine"]]
    lathe(bm, lay, P, 10, cols, theta0=math.pi / 10)
    t = (0.8 - 0.68) / 0.27
    r = 0.27 + 0.06 * t
    for k in range(5):
        a = 2 * math.pi * k / 5
        radial = Vector((math.cos(a), math.sin(a), 0))
        d = (radial * 0.27 + Vector((0, 0, -0.06))).normalized()
        M = Matrix.Translation(radial * (r + 0.004) + Vector((0, 0, 0.8))) @ align_z(d)
        gem(bm, lay, M, 0.055, GEM_ORDER[k % 4])
    return finish("Goblet_Jewelled", bm, lay, mat)


def make_crown(mat):
    bm, lay = new_bm()
    g = C
    lathe(bm, lay, [(0.5, 0), (0.56, 0), (0.56, 0.28), (0.5, 0.28)], 16,
          [g["gold_dark"], g["gold"], g["gold_light"], g["gold_dark"]], closed=True)
    lathe(bm, lay, [(0.555, 0.0), (0.6, 0.0), (0.6, 0.07), (0.555, 0.07)], 16,
          [g["gold_dark"], g["gold_light"], g["gold_light"], g["gold_dark"]], closed=True)
    lathe(bm, lay, [(0.555, 0.235), (0.59, 0.235), (0.59, 0.295), (0.555, 0.295)], 16,
          [g["gold_dark"], g["gold_light"], g["gold_pale"], g["gold_dark"]], closed=True)
    lathe(bm, lay, [(0.5, 0.06), (0.46, 0.2), (0.36, 0.3), (0.2, 0.355), (0, 0.375)], 12,
          [g["velvet_dark"], g["velvet"], g["velvet"], g["velvet"]])
    hull(bm, lay, [(x, y, z) for x in (-0.05, 0.05) for y in (-0.05, 0.05) for z in (0.36, 0.43)] + [(0, 0, 0.49)],
         by_normal(g["gold_pale"], g["gold"]))
    for k in range(8):
        a = 2 * math.pi * k / 8
        tall = k % 2 == 0
        hgt = 0.6 if tall else 0.46
        pts = []
        for da in (-0.26, 0.26):
            for rr in (0.5, 0.56):
                pts.append((rr * math.cos(a + da), rr * math.sin(a + da), 0.28))
        for rr in (0.515, 0.545):
            pts.append((rr * math.cos(a), rr * math.sin(a), hgt))
        radial = Vector((math.cos(a), math.sin(a), 0))
        hull(bm, lay, pts, lambda n, c, rd=radial: g["gold"] if n.dot(rd) > 0.3 else (g["gold_dark"] if n.dot(rd) < -0.3 else g["gold_light"]))
        top = radial * 0.53 + Vector((0, 0, hgt + 0.035))
        if tall:
            gem(bm, lay, Matrix.Translation(top) @ align_z((0, 0, 1)), 0.06, GEM_ORDER[(k // 2) % 4])
        else:
            hull(bm, lay, [top + Vector(v) * 0.035 for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))],
                 by_normal(g["gold_pale"], g["gold_light"]))
        M = Matrix.Translation(radial * 0.565 + Vector((0, 0, 0.15))) @ align_z(radial)
        gem(bm, lay, M, 0.06, GEM_ORDER[(k + 1) % 4])
    return finish("Crown_Gold", bm, lay, mat)


CH_W, CH_D, CH_H, CH_T = 3.0, 2.0, 1.3, 0.14


def make_chest_base(mat):
    rng = random.Random(31)
    bm, lay = new_bm()
    g = C
    hx, hy, H, T = CH_W / 2, CH_D / 2, CH_H, CH_T
    bands = [(0, 0.43), (0.43, 0.87), (0.87, H)]

    def plank(axis, sign, k):
        out = g["wood"] if k % 2 == 0 else g["wood_light"]
        def fn(n, c):
            v = n.y if axis == "y" else n.x
            if v * sign > 0.5:
                return out
            if v * sign < -0.5:
                return g["wood_inside"]
            if n.z > 0.5:
                return g["wood_light"]
            return g["wood_dark"]
        return fn

    for k, (z0, z1) in enumerate(bands):
        ins = 0.0 if k % 2 == 0 else 0.018
        box(bm, lay, (-hx, hy - T, z0), (hx, hy - ins, z1), plank("y", 1, k))
        box(bm, lay, (-hx, -hy + ins, z0), (hx, -hy + T, z1), plank("y", -1, k))
        box(bm, lay, (hx - T, -hy + T, z0), (hx - ins, hy - T, z1), plank("x", 1, k))
        box(bm, lay, (-hx + ins, -hy + T, z0), (-hx + T, hy - T, z1), plank("x", -1, k))
    box(bm, lay, (-hx + T, -hy + T, 0), (hx - T, hy - T, 0.12), g["wood_inside"])
    box(bm, lay, (-hx + T, -hy + T, 0.12), (hx - T, hy - T, 1.0), by_normal(g["gold"], g["gold_dark"]))
    scatter_coins(bm, lay, rng, None, None, 10, 0, 0, base_z=1.0 - 0.015, xy_box=(hx - T - 0.3, hy - T - 0.3), tilt=22)
    for k, kind in enumerate(["ruby", "emerald", "sapphire"]):
        p = Vector((rng.uniform(-0.9, 0.9), rng.uniform(-0.4, 0.4), 1.03))
        gem(bm, lay, Matrix.Translation(p) @ Matrix.Rotation(rng.uniform(-0.5, 0.5), 4, "X"), 0.1, kind)
    gold = by_normal(g["gold_light"], g["gold"], g["gold_dark"])
    for sx in (-1, 1):
        for sy in (-1, 1):
            xs = sorted((sx * (hx - 0.17), sx * (hx + 0.03)))
            ys = sorted((sy * (hy - 0.17), sy * (hy + 0.03)))
            box(bm, lay, (xs[0], ys[0], 0), (xs[1], ys[1], H + 0.01), gold)
    for x0 in (-0.85, 0.85):
        box(bm, lay, (x0 - 0.09, hy - 0.02, 0), (x0 + 0.09, hy + 0.03, H), gold)
        box(bm, lay, (x0 - 0.09, -hy - 0.03, 0), (x0 + 0.09, -hy + 0.02, H), gold)
        box(bm, lay, (x0 - 0.12, -hy - 0.07, H - 0.1), (x0 + 0.12, -hy + 0.01, H + 0.05),
            by_normal(g["gold"], g["gold_dark"]))  # hinge knuckles
    box(bm, lay, (-hx + 0.17, hy - T, H - 0.08), (hx - 0.17, hy + 0.022, H + 0.015), gold)
    box(bm, lay, (-hx + 0.17, -hy - 0.022, H - 0.08), (hx - 0.17, -hy + T, H + 0.015), gold)
    box(bm, lay, (hx - T, -hy + 0.17, H - 0.08), (hx + 0.022, hy - 0.17, H + 0.015), gold)
    box(bm, lay, (-hx - 0.022, -hy + 0.17, H - 0.08), (-hx + T, hy - 0.17, H + 0.015), gold)
    box(bm, lay, (-0.19, hy, 0.78), (0.19, hy + 0.045, 1.2),
        lambda n, c: g["gold_light"] if n.y > 0.5 else g["gold_dark"])
    box(bm, lay, (-0.035, hy + 0.045, 0.9), (0.035, hy + 0.055, 1.04), g["keyhole"])
    ob = finish("Chest_Base", bm, lay, mat)
    return ob, Vector((0, -hy, H))


def make_chest_lid(mat):
    bm, lay = new_bm()
    g = C
    hx, D = CH_W / 2, CH_D

    def xs(off):
        pts = [(-off, 0.025 - off), (D + off, 0.025 - off)]
        for k in range(7):
            a = math.pi * k / 6
            pts.append((D / 2 - (D / 2 + off) * math.cos(a), 0.12 + (0.62 + off) * math.sin(a)))
        return pts

    def slab(x0, x1, off):
        return [(x, y, z) for x in (x0, x1) for (y, z) in xs(off)]

    def barrel(n, c):
        if n.z < -0.9:
            return g["wood_inside"]
        if abs(n.x) > 0.9:
            return g["wood_dark"]
        k = int(round(math.atan2(n.z, n.y) / (math.pi / 6)))
        return g["wood"] if k % 2 == 0 else g["wood_light"]

    def trim(n, c):
        if n.z < -0.9:
            return g["gold_dark"]
        return g["gold_light"] if n.z > 0.7 else g["gold"]

    hull(bm, lay, slab(-hx, hx, 0.0), barrel)
    for s in (-1, 1):
        x0, x1 = sorted((s * (hx - 0.1), s * (hx + 0.03)))
        hull(bm, lay, slab(x0, x1, 0.035), trim)
    for x0 in (-0.85, 0.85):
        hull(bm, lay, slab(x0 - 0.09, x0 + 0.09, 0.03), trim)
    box(bm, lay, (-hx, D, 0), (hx, D + 0.035, 0.14), by_normal(g["gold_light"], g["gold"], g["gold_dark"]))
    box(bm, lay, (-0.12, D + 0.035, -0.16), (0.12, D + 0.075, 0.3),
        lambda n, c: g["gold_light"] if n.y > 0.5 else g["gold_dark"])
    top = Vector((0, D / 2, 0.12 + 0.62 + 0.03))
    gem(bm, lay, Matrix.Translation(top + Vector((0, 0.0, -0.0))), 0.13, "ruby")
    return finish("Chest_Lid", bm, lay, mat)


def make_sword(mat):
    bm, lay = new_bm()
    g = C

    def section(z, w, t, bev):
        return [(w, 0, z), (-w, 0, z), (bev, t, z), (-bev, t, z), (bev, -t, z), (-bev, -t, z)]

    blade = [(0, 0, 0)] + section(0.4, 0.15, 0.045, 0.09) + section(3.02, 0.19, 0.05, 0.12)
    hull(bm, lay, blade, lambda n, c: g["steel_light"] if abs(n.x) > 0.45 else g["steel"])
    for s in (-1, 1):
        t0, t1 = 0.0452, 0.0497
        pts = []
        for z, t in ((0.6, t0), (2.85, t1)):
            for x in (-0.025, 0.025):
                for dy in (-0.004, 0.006):
                    pts.append((x, s * (t + dy), z))
        hull(bm, lay, pts, g["steel_dark"])
    gold = by_normal(g["gold_light"], g["gold"], g["gold_dark"], thresh=0.5)
    box(bm, lay, (-0.24, -0.09, 3.0), (0.24, 0.09, 3.17), gold)
    for s in (-1, 1):
        seg1 = [(s * 0.22, y, z) for y in (-0.07, 0.07) for z in (3.02, 3.16)] + \
               [(s * 0.5, y, z) for y in (-0.06, 0.06) for z in (3.08, 3.24)]
        seg2 = [(s * 0.5, y, z) for y in (-0.06, 0.06) for z in (3.08, 3.24)] + \
               [(s * 0.78, y, z) for y in (-0.03, 0.03) for z in (3.33, 3.41)]
        hull(bm, lay, seg1, gold)
        hull(bm, lay, seg2, gold)
        gem(bm, lay, Matrix.Translation((0, s * 0.09, 3.085)) @ align_z((0, s, 0)), 0.06, "ruby")
    prof = [(0.066 if i % 2 == 0 else 0.078, 3.16 + i * 0.128) for i in range(8)]
    lathe(bm, lay, prof, 6, [g["grip"] if i % 2 == 0 else g["grip_dark"] for i in range(7)], theta0=math.pi / 6)
    lathe(bm, lay, [(0, 4.03), (0.1, 4.04), (0.13, 4.15), (0.12, 4.28), (0.08, 4.38), (0, 4.44)], 8,
          [g["gold_dark"], g["gold"], g["gold_light"], g["gold"], g["gold_pale"]], theta0=math.pi / 8)
    for s in (-1, 1):
        gem(bm, lay, Matrix.Translation((0, s * 0.125, 4.2)) @ align_z((0, s, 0)), 0.065, "ruby")
    return finish("Sword_Ornate", bm, lay, mat)


# ---------------------------------------------------------------- particle textures
def particle_textures():
    def grid(n):
        y, x = np.mgrid[0:n, 0:n]
        u = (x + 0.5) / n * 2 - 1
        v = (y + 0.5) / n * 2 - 1
        return u, v, np.sqrt(u * u + v * v)

    def write(name, alpha, n):
        a = np.clip(alpha, 0, 1).astype(np.float32)
        px = np.ones((n, n, 4), dtype=np.float32)
        px[..., 3] = a
        save_png(px, os.path.join(OUT, "vfx", name + ".png"), name)

    def seg_dist(u, v, p0, p1):
        p0, p1 = np.array(p0), np.array(p1)
        d = p1 - p0
        t = np.clip(((u - p0[0]) * d[0] + (v - p0[1]) * d[1]) / (d @ d), 0, 1)
        return np.hypot(u - (p0[0] + t * d[0]), v - (p0[1] + t * d[1]))

    n = 128
    u, v, r = grid(n)
    edge = np.clip((1 - r) * 4, 0, 1)
    star = (np.exp(-np.abs(v) * 30) * np.clip(1 - np.abs(u), 0, 1) ** 1.5 +
            np.exp(-np.abs(u) * 30) * np.clip(1 - np.abs(v), 0, 1) ** 1.5)
    diag = (np.exp(-np.abs(u - v) * 40) + np.exp(-np.abs(u + v) * 40)) * np.clip(1 - r * 1.8, 0, 1) * 0.6
    write("Sparkle", (star + diag + np.exp(-r * r * 40) + 0.3 * np.exp(-r * r * 6)) * edge, n)
    write("Ember", (np.exp(-r * r * 9) + 0.6 * np.exp(-r * r * 40)) * edge, n)
    write("Glow", np.clip(1 - r, 0, 1) ** 2.2, n)

    segs = []
    for k in range(6):
        a = math.pi / 3 * k + math.pi / 6
        d = np.array([math.cos(a), math.sin(a)])
        segs.append(((0, 0), tuple(d * 0.88)))
        for b in (math.pi / 3, -math.pi / 3):
            db = np.array([math.cos(a + b), math.sin(a + b)])
            for t, ln in ((0.45, 0.26), (0.68, 0.16)):
                segs.append((tuple(d * t), tuple(d * t + db * ln)))
    dist = np.min([seg_dist(u, v, p0, p1) for p0, p1 in segs], axis=0)
    write("FrostFlake", (np.exp(-(dist / 0.045) ** 2) + 0.5 * np.exp(-r * r * 30)) * edge, n)

    ring = np.exp(-((r - 0.82) / 0.07) ** 2)
    hi = np.exp(-((u + 0.35) ** 2 + (v - 0.38) ** 2) * 45)
    write("Bubble", (0.9 * ring + 0.14 * (r < 0.82) + hi) * edge, n)

    disc = np.clip((0.86 - r) * 40, 0, 1) * 0.75 + np.exp(-((r - 0.78) / 0.05) ** 2) * 0.25
    write("CoinGlint", np.clip(disc, 0, 0.85) + star * 0.9 * edge, n)

    band = np.exp(-(v / 0.32) ** 2) * np.clip(np.sin((u + 1) / 2 * math.pi), 0, 1) ** 0.5
    write("Shine", band, n)


# ---------------------------------------------------------------- export + render
def export_obj(ob):
    folder = os.path.join(OUT, "models", ob.name)
    os.makedirs(folder, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.wm.obj_export(filepath=os.path.join(folder, ob.name + ".obj"), export_selected_objects=True,
                          export_uv=True, export_normals=True, export_colors=False, export_materials=True,
                          export_triangulated_mesh=True, export_smooth_groups=False, path_mode="COPY",
                          forward_axis="NEGATIVE_Z", up_axis="Y", global_scale=1.0, apply_modifiers=True)


def rbx(v):
    return [round(v.x, 4), round(v.z, 4), round(-v.y, 4)]


def bbox(ob):
    vs = [v.co for v in ob.data.vertices]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    return mn, mx


def setup_render():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "TEXTURE"
    sc.display.shading.show_specular_highlight = False
    sc.display.shading.show_cavity = False
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = sc.render.resolution_y = 640
    sc.render.film_transparent = False
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.color = (0.80, 0.77, 0.72)
    cam = bpy.data.objects.new("PreviewCam", bpy.data.cameras.new("PreviewCam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def render(cam, visible, path, direction=Vector((0.75, 1.5, 0.85)), margin=1.0):
    sc = bpy.context.scene
    for ob in sc.objects:
        if ob.type == "MESH":
            ob.hide_render = ob not in visible
    pts = [ob.matrix_world @ Vector(c) for ob in visible for c in ob.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centre, size = (mn + mx) / 2, (mx - mn).length
    cam.data.lens = 50
    dist = (size / 2) / math.sin(math.radians(17)) * margin
    cam.location = centre + direction.normalized() * dist
    cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    img = make_atlas()
    mat = make_material(img)
    particle_textures()

    styles = {
        "Egg_Ember": {"body": C["ember_dark"], "plate": ember_plate},
        "Egg_Frost": {"body": C["frost_dark"], "plate": frost_plate},
        "Egg_Venom": {"body": C["venom_dark"], "plate": venom_plate},
    }
    objs = [make_egg(n, s, i + 1, mat) for i, (n, s) in enumerate(styles.items())]
    objs.append(make_coin(mat))
    objs.append(make_small_pile(mat))
    large, socket = make_large_pile(mat)
    objs.append(large)
    objs.append(make_goblet(mat))
    objs.append(make_crown(mat))
    base, hinge = make_chest_base(mat)
    objs.append(base)
    lid = make_chest_lid(mat)
    objs.append(lid)
    sword = make_sword(mat)
    objs.append(sword)

    report = {}
    for ob in objs:
        export_obj(ob)
        mn, mx = bbox(ob)
        centre = (mn + mx) / 2
        report[ob.name] = {
            "tris": sum(len(p.vertices) - 2 for p in ob.data.polygons),
            "size_studs": [round(abs(x), 3) for x in rbx(mx - mn)],
            "pivot_from_centre": rbx(-centre),
        }
    report["CoinPile_Large"]["sword_socket_from_centre"] = rbx(socket - sum(bbox(large), Vector()) / 2)
    report["Chest_Base"]["lid_hinge_from_centre"] = rbx(hinge - sum(bbox(base), Vector()) / 2)
    report["Chest_Base"]["lid_hinge_from_pivot"] = rbx(hinge)
    with open(os.path.join(OUT, "build_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    cam = setup_render()
    prev = os.path.join(OUT, "previews")
    for ob in objs:
        render(cam, [ob], os.path.join(prev, ob.name + ".png"))

    # showcase: everything in a row, then the assembled chest + sword in the pile
    show = []
    layout = {"Egg_Ember": (-2.3, 1.3), "Egg_Frost": (-1.1, 1.5), "Egg_Venom": (0.1, 1.3), "Coin_Gold": (3.9, 1.6),
              "CoinPile_Small": (-3.4, -0.6), "Goblet_Jewelled": (1.4, 1.5), "Crown_Gold": (2.7, 1.3),
              "CoinPile_Large": (3.6, -1.4), "Sword_Ornate": None, "Chest_Base": (0.0, -1.6), "Chest_Lid": None}
    for ob in objs:
        if layout.get(ob.name) is None:
            continue
        d = ob.copy()
        d.name = ob.name + "_show"
        d.location = (layout[ob.name][0], layout[ob.name][1], 0)
        bpy.context.scene.collection.objects.link(d)
        show.append(d)
    lid_s = lid.copy(); lid_s.name = "Chest_Lid_show"
    lid_s.matrix_world = (Matrix.Translation((0.0, -1.6, 0)) @ Matrix.Translation(hinge)
                          @ Matrix.Rotation(math.radians(105), 4, "X"))
    sw = sword.copy(); sw.name = "Sword_show"
    sw.matrix_world = (Matrix.Translation((3.6, -1.4, 0)) @ Matrix.Translation(socket)
                       @ Matrix.Rotation(math.radians(8), 4, "X") @ Matrix.Translation((0, 0, -0.9)))
    for d in (lid_s, sw):
        bpy.context.scene.collection.objects.link(d)
        show.append(d)
    render(cam, show, os.path.join(prev, "_Showcase.png"), direction=Vector((0.12, 1.6, 0.8)), margin=0.72)

    for ob in show:
        ob.hide_render = True
        ob.hide_set(True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "DragonsHoard.blend"))
    print("HOARD_REPORT", json.dumps(report))


main()
