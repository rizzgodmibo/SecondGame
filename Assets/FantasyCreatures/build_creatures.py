# Fantasy Creatures: builds the creatures in Blender from code and renders every image the
# reference sheets need (hero, orthographic views, poses, parts, materials, scale).
#
# Run headless (GPU / OptiX):
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --factory-startup ^
#       --python build_creatures.py -- drake ortho hero
#   creatures: drake golem wolf      render sets: ortho hero poses parts mats scale vfx habitat all
#
# Modelling: organic bodies are signed-distance fields (smooth-blended ellipsoids / round cones,
# like sculpting with clay), meshed with surface nets and Taubin-smoothed. Hard parts (horns,
# plates, claws, teeth, wings) are explicit meshes. A tiny FK rig (rotations about rest-pose
# joints) poses the SDF primitives and the hard parts together, so every pose is re-meshed cleanly.
#
# Units: 1 Blender unit = 1 stud. Z up. Creatures face +Y (= Roblox -Z after OBJ export).

import bpy, bmesh, math, os, sys, json, time, random
import numpy as np
from mathutils import Vector, Matrix, Euler
from mathutils.bvhtree import BVHTree
from collections import defaultdict

OUT = os.path.dirname(os.path.abspath(__file__))
REN = os.path.join(OUT, "design", "renders")
os.makedirs(REN, exist_ok=True)

# colour management: AgX desaturates hot oranges toward pink; PBR Neutral keeps saturated hues (override: vt=<name>)
VIEW_TRANSFORM = "Standard"
VIEW_EXPOSURE = {"AgX": 0.25, "Standard": -0.15, "Khronos PBR Neutral": 0.0}
for _a in sys.argv:
    if _a.startswith("vt="):
        VIEW_TRANSFORM = _a[3:].replace("_", " ")
SUFFIX = ""
for _a in sys.argv:
    if _a.startswith("suffix="):
        SUFFIX = _a[7:]


def log(*a):
    print("[creatures]", *a, flush=True)


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (lin[0], lin[1], lin[2], a)


# ============================================================ SDF primitives (numpy)
def _dot(a, b):
    return np.einsum("...i,...i->...", a, b)


def _len(v):
    return np.sqrt(_dot(v, v))


def sd_sphere(p, c, r):
    return _len(p - c) - r


def sd_ellipsoid(p, c, rad, R):
    q = (p - c) @ R  # R: local->world rotation, so world->local is q @ R
    k0 = _len(q / rad)
    k1 = _len(q / (rad * rad))
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def sd_round_cone(p, a, b, r1, r2):
    ba = b - a
    l2 = float(ba @ ba)
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = p - a
    y = pa @ ba
    z = y - l2
    t = pa * l2 - y[..., None] * ba
    x2 = _dot(t, t)
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    d1 = np.sqrt(x2 + z2) * il2 - r2
    d2 = np.sqrt(x2 + y2) * il2 - r1
    d3 = (np.sqrt(np.maximum(x2 * a2 * il2, 0.0)) + y * rr) * il2 - r1
    return np.where(np.sign(z) * a2 * z2 > k, d1, np.where(np.sign(y) * a2 * y2 < k, d2, d3))


def sd_box(p, c, half, R, rnd=0.0):
    q = np.abs((p - c) @ R) - (np.asarray(half, np.float32) - rnd)
    return _len(np.maximum(q, 0.0)) + np.minimum(np.max(q, axis=-1), 0.0) - rnd


def smin(a, b, k):
    if k <= 1e-6:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


def rotm(rx=0.0, ry=0.0, rz=0.0):
    return np.array(Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ").to_matrix(), np.float32)


# Primitive description: dict(kind, bone, k, mode, + params). Points are rest-pose world coords.
def P_ell(bone, c, rad, rot=(0, 0, 0), k=0.3, mode="add"):
    return dict(kind="ell", bone=bone, c=np.array(c, np.float32), rad=np.array(rad, np.float32), R=rotm(*rot), k=k, mode=mode)


def P_sph(bone, c, r, k=0.3, mode="add"):
    return dict(kind="sph", bone=bone, c=np.array(c, np.float32), r=float(r), k=k, mode=mode)


def P_cone(bone, a, b, r1, r2, k=0.3, mode="add"):
    return dict(kind="cone", bone=bone, a=np.array(a, np.float32), b=np.array(b, np.float32), r1=float(r1), r2=float(r2), k=k, mode=mode)


def P_box(bone, c, half, rot=(0, 0, 0), rnd=0.05, k=0.1, mode="add"):
    return dict(kind="box", bone=bone, c=np.array(c, np.float32), half=np.array(half, np.float32), R=rotm(*rot), rnd=rnd, k=k, mode=mode)


def P_hull(bone, pts, edge=0.02, k=0.08, mode="add"):
    """Convex polytope (hull of pts) with softened edges - angular bone forms: brows, cheekbones, snout, jaw."""
    bm = bmesh.new()
    vs = [bm.verts.new(Vector(p)) for p in pts]
    bmesh.ops.convex_hull(bm, input=vs)
    for v in [v for v in bm.verts if not v.link_faces]:
        bm.verts.remove(v)
    bm.normal_update()
    cen = sum((Vector(p) for p in pts), Vector()) / len(pts)
    planes = {}
    for f in bm.faces:
        n = f.normal.normalized()
        if n.length < 0.5:
            continue
        o = n.dot(f.verts[0].co)
        if n.dot(cen) > o:                       # make every plane face outward
            n, o = -n, -o
        planes[(round(n.x, 3), round(n.y, 3), round(n.z, 3), round(o, 3))] = (n, o)
    bm.free()
    N = np.array([tuple(n) for n, o in planes.values()], np.float32)
    O = np.array([o for n, o in planes.values()], np.float32)
    return dict(kind="hull", bone=bone, pts=np.array([tuple(p) for p in pts], np.float32), N=N, O=O,
                edge=float(edge), k=k, mode=mode)


def sd_hull(p, N, O, edge):
    d = p @ N[0] - O[0]
    for i in range(1, len(N)):
        d = smax(d, p @ N[i] - O[i], edge)
    return d


def frame_ab(a, b, lat=(1, 0, 0)):
    a, b = Vector(a), Vector(b)
    e2 = (b - a).normalized()
    e1 = Vector(lat)
    e1 = e1 - e2 * e1.dot(e2)
    e1 = e1.normalized() if e1.length > 1e-6 else e2.orthogonal().normalized()
    return e1, e2, e1.cross(e2)


def P_ell_ab(bone, a, b, w, d, k=0.12, mode="add", lat=(1, 0, 0), over=1.0):
    """Ellipsoid spanning a->b: half-length |ab|/2*over, radius w along `lat`, radius d across (muscle bellies)."""
    e1, e2, e3 = frame_ab(a, b, lat)
    R = np.array([[e1[i], e2[i], e3[i]] for i in range(3)], np.float32)
    c = (Vector(a) + Vector(b)) / 2
    L = (Vector(b) - Vector(a)).length / 2 * over
    return dict(kind="ell", bone=bone, c=np.array(tuple(c), np.float32), rad=np.array((w, L, d), np.float32), R=R, k=k, mode=mode)


def mirror_x(prims):
    out = []
    for p in prims:
        q = dict(p)
        for key in ("c", "a", "b", "pts", "N"):
            if key in q:
                v = q[key].copy()
                v[..., 0] = -v[..., 0]
                q[key] = v
        if "R" in q:
            S = np.diag([-1.0, 1.0, 1.0]).astype(np.float32)
            q["R"] = (S @ q["R"] @ S).astype(np.float32)
        if q.get("bone", "").endswith("_L"):
            q["bone"] = q["bone"][:-2] + "_R"
        out.append(q)
    return out


def xform_prim(p, M):
    """Apply a 4x4 bone matrix to a primitive (rotation + translation, uniform)."""
    q = dict(p)
    A = np.array(M, np.float32)
    R3 = A[:3, :3]
    t = A[:3, 3]
    for key in ("c", "a", "b"):
        if key in q:
            q[key] = (R3 @ q[key] + t).astype(np.float32)
    if "R" in q:
        q["R"] = (R3 @ q["R"]).astype(np.float32)
    if "pts" in q:
        q["pts"] = (q["pts"] @ R3.T + t).astype(np.float32)
        q["N"] = (q["N"] @ R3.T).astype(np.float32)
        q["O"] = (q["O"] + q["N"] @ t).astype(np.float32)
    return q


def prim_aabb(p):
    if p["kind"] == "sph":
        return p["c"] - p["r"], p["c"] + p["r"]
    if p["kind"] == "ell":
        m = float(np.max(p["rad"]))
        return p["c"] - m, p["c"] + m
    if p["kind"] == "cone":
        lo = np.minimum(p["a"] - p["r1"], p["b"] - p["r2"])
        hi = np.maximum(p["a"] + p["r1"], p["b"] + p["r2"])
        return lo, hi
    if p["kind"] == "box":
        e = np.abs(p["R"]) @ p["half"]
        return p["c"] - e, p["c"] + e
    if p["kind"] == "hull":
        return p["pts"].min(axis=0), p["pts"].max(axis=0)
    raise ValueError(p["kind"])


def prim_eval(p, P):
    k = p["kind"]
    if k == "sph":
        return sd_sphere(P, p["c"], p["r"])
    if k == "ell":
        return sd_ellipsoid(P, p["c"], p["rad"], p["R"])
    if k == "cone":
        return sd_round_cone(P, p["a"], p["b"], p["r1"], p["r2"])
    if k == "box":
        return sd_box(P, p["c"], p["half"], p["R"], p["rnd"])
    if k == "hull":
        return sd_hull(P, p["N"], p["O"], p["edge"])
    raise ValueError(k)


def sdf_mesh(prims, h):
    adds = [p for p in prims if p["mode"] == "add"]
    lo = np.min([prim_aabb(p)[0] for p in adds], axis=0) - 0.25
    hi = np.max([prim_aabb(p)[1] for p in adds], axis=0) + 0.25
    n = (np.ceil((hi - lo) / h).astype(int) + 1)
    F = np.full(tuple(n), 10.0, np.float32)
    for p in prims:
        a0, a1 = prim_aabb(p)
        m = p["k"] + 2.5 * h
        i0 = np.clip(np.floor((a0 - m - lo) / h).astype(int), 0, n - 1)
        i1 = np.clip(np.ceil((a1 + m - lo) / h).astype(int) + 1, 0, n)
        if np.any(i1 <= i0):
            continue
        axes = [lo[d] + h * np.arange(i0[d], i1[d], dtype=np.float32) for d in range(3)]
        P = np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1)
        d = prim_eval(p, P).astype(np.float32)
        sl = tuple(slice(i0[d_], i1[d_]) for d_ in range(3))
        if p["mode"] == "add":
            F[sl] = smin(F[sl], d, p["k"])
        else:
            F[sl] = smax(F[sl], -d, p["k"])
    return surface_nets(F, lo.astype(np.float32), h)


def surface_nets(F, origin, h):
    s = F < 0
    C = [F[:-1, :-1, :-1], F[1:, :-1, :-1], F[:-1, 1:, :-1], F[1:, 1:, :-1],
         F[:-1, :-1, 1:], F[1:, :-1, 1:], F[:-1, 1:, 1:], F[1:, 1:, 1:]]
    offs = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)], np.float32)
    mn = np.minimum.reduce(C)
    mx = np.maximum.reduce(C)
    active = (mn < 0) & (mx >= 0)
    ai = np.nonzero(active)
    acc = np.zeros((len(ai[0]), 3), np.float32)
    cnt = np.zeros(len(ai[0]), np.float32)
    for a, b in ((0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)):
        fa = C[a][ai]
        fb = C[b][ai]
        cross = (fa < 0) != (fb < 0)
        t = np.where(cross, fa / np.where(cross, fa - fb, 1.0), 0.0)
        pos = offs[a] + (offs[b] - offs[a]) * t[:, None]
        acc += np.where(cross[:, None], pos, 0.0)
        cnt += cross
    idx = np.full(active.shape, -1, np.int64)
    idx[ai] = np.arange(len(ai[0]))
    verts = (np.stack(ai, axis=1).astype(np.float32) + acc / np.maximum(cnt, 1)[:, None]) * h + origin
    quads = []
    e = s[:-1, 1:-1, 1:-1] != s[1:, 1:-1, 1:-1]
    i, j, k = np.nonzero(e)
    j += 1
    k += 1
    q = np.stack([idx[i, j - 1, k - 1], idx[i, j, k - 1], idx[i, j, k], idx[i, j - 1, k]], 1)
    f = ~s[i, j, k]
    q[f] = q[f][:, ::-1]
    quads.append(q)
    e = s[1:-1, :-1, 1:-1] != s[1:-1, 1:, 1:-1]
    i, j, k = np.nonzero(e)
    i += 1
    k += 1
    q = np.stack([idx[i - 1, j, k - 1], idx[i - 1, j, k], idx[i, j, k], idx[i, j, k - 1]], 1)
    f = ~s[i, j, k]
    q[f] = q[f][:, ::-1]
    quads.append(q)
    e = s[1:-1, 1:-1, :-1] != s[1:-1, 1:-1, 1:]
    i, j, k = np.nonzero(e)
    i += 1
    j += 1
    q = np.stack([idx[i - 1, j - 1, k], idx[i, j - 1, k], idx[i, j, k], idx[i - 1, j, k]], 1)
    f = ~s[i, j, k]
    q[f] = q[f][:, ::-1]
    quads.append(q)
    faces = np.concatenate(quads)
    faces = faces[np.all(faces >= 0, axis=1)]
    return verts, faces


def taubin(verts, faces, iters=5, lam=0.5, mu=-0.53):
    e = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 3]], faces[:, [3, 0]]])
    e = np.concatenate([e, e[:, ::-1]])
    deg = np.bincount(e[:, 0], minlength=len(verts)).astype(np.float32)
    deg[deg == 0] = 1
    v = verts.astype(np.float64).copy()
    for _ in range(iters):
        for fct in (lam, mu):
            s = np.zeros_like(v)
            np.add.at(s, e[:, 0], v[e[:, 1]])
            v = v + fct * (s / deg[:, None] - v)
    return v.astype(np.float32)


def signed_volume(v, faces):
    a, b, c, d = v[faces[:, 0]], v[faces[:, 1]], v[faces[:, 2]], v[faces[:, 3]]
    return (np.einsum("ij,ij->i", a, np.cross(b, c)).sum() + np.einsum("ij,ij->i", a, np.cross(c, d)).sum()) / 6.0


# ============================================================ Blender helpers
def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def mesh_from_np(name, verts, faces):
    me = bpy.data.meshes.new(name)
    nv, nf = len(verts), len(faces)
    nl = faces.shape[1]
    try:
        me.vertices.add(nv)
        me.vertices.foreach_set("co", verts.astype(np.float32).ravel())
        me.loops.add(nf * nl)
        me.loops.foreach_set("vertex_index", faces.astype(np.int32).ravel())
        me.polygons.add(nf)
        me.polygons.foreach_set("loop_start", np.arange(0, nf * nl, nl, dtype=np.int32))
        me.update(calc_edges=True)
    except Exception as ex:
        log("fast mesh path failed, using from_pydata:", ex)
        bpy.data.meshes.remove(me)
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts.tolist(), [], faces.tolist())
        me.update(calc_edges=True)
    me.validate(clean_customdata=False)
    me.shade_smooth()
    return me


def set_point_attr(me, name, values):
    a = me.attributes.get(name) or me.attributes.new(name, "FLOAT", "POINT")
    a.data.foreach_set("value", np.asarray(values, np.float32).ravel())


def vnormals(me):
    n = np.zeros(len(me.vertices) * 3, np.float32)
    me.vertex_normals.foreach_get("vector", n)
    return n.reshape(-1, 3)


def vcoords(me):
    c = np.zeros(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", c)
    return c.reshape(-1, 3)


def bm_to_obj(bm, name, mat, attrs=None, smooth=True, coll=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        me.shade_smooth()
    if mat is not None:
        me.materials.append(mat)
    if attrs:
        for k, v in attrs.items():
            set_point_attr(me, k, v)
    ob = bpy.data.objects.new(name, me)
    link(ob, coll)
    return ob


def frames_along(points):
    """Parallel-transport frames (tangent, normal, binormal) for a polyline."""
    pts = [Vector(p) for p in points]
    T = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        T.append((b - a).normalized())
    up = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    N = [(up - T[0] * up.dot(T[0])).normalized()]
    for i in range(1, len(pts)):
        n = N[-1] - T[i] * N[-1].dot(T[i])
        N.append(n.normalized() if n.length > 1e-6 else N[-1])
    B = [T[i].cross(N[i]) for i in range(len(pts))]
    return pts, T, N, B


def sweep(points, radii, segs=10, cap_end=True, flat=1.0, name="sweep", mat=None, tparam=True, coll=None, tattr="t"):
    """Tube along points with per-point radius; flat squashes the cross-section along the normal."""
    pts, T, N, B = frames_along(points)
    bm = bmesh.new()
    rings = []
    tv = []
    L = len(pts)
    for i, p in enumerate(pts):
        r = radii[i]
        if r <= 1e-5:
            rings.append([bm.verts.new(p)])
            tv.append(i / (L - 1))
            continue
        ring = []
        for j in range(segs):
            a = 2 * math.pi * j / segs
            ring.append(bm.verts.new(p + (N[i] * math.cos(a) * flat + B[i] * math.sin(a)) * r))
            tv.append(i / (L - 1))
        rings.append(ring)
    for i in range(L - 1):
        A, Bq = rings[i], rings[i + 1]
        for j in range(segs):
            j2 = (j + 1) % segs
            if len(A) == 1 and len(Bq) == 1:
                continue
            if len(Bq) == 1:
                bm.faces.new((A[j], A[j2], Bq[0]))
            elif len(A) == 1:
                bm.faces.new((A[0], Bq[j2], Bq[j]))
            else:
                bm.faces.new((A[j], A[j2], Bq[j2], Bq[j]))
    if len(rings[0]) > 1:
        bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    attrs = {tattr: tv} if tparam else None
    return bm_to_obj(bm, name, mat, attrs, coll=coll)


def spike(name, base, direction, length, radius, mat, curve=0.0, up=Vector((0, 0, 1)), segs=8, tattr="t", steps=5):
    """Tapered (optionally curved) spike along direction; curve bends the tip toward `up`."""
    d = Vector(direction).normalized()
    u = Vector(up)
    u = (u - d * u.dot(d))
    u = u.normalized() if u.length > 1e-6 else Vector((0, 0, 0))
    pts, rad = [], []
    for i in range(steps + 1):
        t = i / steps
        pts.append(Vector(base) + d * (length * t) + u * (curve * length * t * t))
        rad.append(radius * (1.0 - t) ** 0.9)
    rad[-1] = 0.0
    return sweep(pts, rad, segs, name=name, mat=mat, tattr=tattr)


def bezier3(p0, p1, p2, p3, n):
    out = []
    for i in range(n):
        t = i / (n - 1)
        a = (1 - t) ** 3
        b = 3 * t * (1 - t) ** 2
        c = 3 * t * t * (1 - t)
        e = t ** 3
        out.append(Vector(p0) * a + Vector(p1) * b + Vector(p2) * c + Vector(p3) * e)
    return out


def hull_obj(points, name, mat, attr_fn=None, smooth=True, subdiv=0, coll=None):
    bm = bmesh.new()
    vs = [bm.verts.new(Vector(p)) for p in points]
    bmesh.ops.convex_hull(bm, input=vs)
    for v in [v for v in bm.verts if not v.link_faces]:
        bm.verts.remove(v)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if subdiv:
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=subdiv, use_grid_fill=True, smooth=0.0)
    attrs = None
    if attr_fn:
        attrs = {}
        vals = [attr_fn(v.co) for v in bm.verts]
        for key in vals[0]:
            attrs[key] = [d[key] for d in vals]
    return bm_to_obj(bm, name, mat, attrs, smooth=smooth, coll=coll)


def basis_from(fwd, up):
    f = Vector(fwd).normalized()
    u = Vector(up)
    u = (u - f * u.dot(f)).normalized()
    s = f.cross(u)
    return f, u, s


# ============================================================ materials (Cycles node helpers)
class NT:
    def __init__(self, mat):
        self.nt = mat.node_tree
        self.n = self.nt.nodes
        self.l = self.nt.links
        self.x = -1200

    def node(self, t, **kw):
        nd = self.n.new(t)
        nd.location = (self.x, 0)
        self.x += 160
        for k, v in kw.items():
            setattr(nd, k, v)
        return nd

    def link(self, a, b):
        self.l.new(a, b)

    def inp(self, nd, name, val=None, src=None):
        s = nd.inputs[name] if isinstance(name, (str, int)) else name
        if src is not None:
            self.l.new(src, s)
        elif val is not None:
            s.default_value = val
        return s

    def attr(self, name):
        nd = self.node("ShaderNodeAttribute")
        nd.attribute_name = name
        return nd.outputs["Fac"]

    def math(self, op, a, b=None, clamp=False):
        nd = self.node("ShaderNodeMath")
        nd.operation = op
        nd.use_clamp = clamp
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                nd.inputs[i].default_value = v
            else:
                self.l.new(v, nd.inputs[i])
        return nd.outputs[0]

    def maprange(self, v, a, b, c, d, clamp=True):
        nd = self.node("ShaderNodeMapRange")
        nd.clamp = clamp
        self.l.new(v, nd.inputs["Value"])
        nd.inputs["From Min"].default_value = a
        nd.inputs["From Max"].default_value = b
        nd.inputs["To Min"].default_value = c
        nd.inputs["To Max"].default_value = d
        return nd.outputs["Result"]

    def mix(self, fac, a, b, blend="MIX"):
        nd = self.node("ShaderNodeMix")
        nd.data_type = "RGBA"
        nd.blend_type = blend
        ins = [s for s in nd.inputs if s.enabled]
        fs = ins[0]
        A = [s for s in ins if s.name == "A"][0]
        B = [s for s in ins if s.name == "B"][0]
        for sock, v in ((fs, fac), (A, a), (B, b)):
            if isinstance(v, (int, float)):
                sock.default_value = v
            elif isinstance(v, tuple):
                sock.default_value = v
            else:
                self.l.new(v, sock)
        out = [s for s in nd.outputs if s.enabled and s.type == "RGBA"][0]
        return out

    def ramp(self, v, stops):
        nd = self.node("ShaderNodeValToRGB")
        self.l.new(v, nd.inputs["Fac"])
        els = nd.color_ramp.elements
        while len(els) > 1:
            els.remove(els[-1])
        els[0].position = stops[0][0]
        els[0].color = stops[0][1]
        for pos, col in stops[1:]:
            e = els.new(pos)
            e.color = col
        return nd.outputs["Color"]

    def objco(self):
        return self.node("ShaderNodeTexCoord").outputs["Object"]

    def voronoi(self, vec, scale, feature="F1", rand=1.0):
        nd = self.node("ShaderNodeTexVoronoi")
        nd.feature = feature
        self.l.new(vec, nd.inputs["Vector"])
        nd.inputs["Scale"].default_value = scale
        if "Randomness" in nd.inputs:
            nd.inputs["Randomness"].default_value = rand
        return nd

    def noise(self, vec, scale, detail=2.0, rough=0.5):
        nd = self.node("ShaderNodeTexNoise")
        self.l.new(vec, nd.inputs["Vector"])
        nd.inputs["Scale"].default_value = scale
        nd.inputs["Detail"].default_value = detail
        nd.inputs["Roughness"].default_value = rough
        return nd

    def ao(self, dist=0.4):
        nd = self.node("ShaderNodeAmbientOcclusion")
        nd.inputs["Distance"].default_value = dist
        nd.samples = 16
        return nd.outputs["AO"]

    def bump(self, height, strength=0.3, dist=0.02):
        nd = self.node("ShaderNodeBump")
        self.l.new(height, nd.inputs["Height"])
        nd.inputs["Strength"].default_value = strength
        nd.inputs["Distance"].default_value = dist
        return nd.outputs["Normal"]

    def bsdf(self, base, rough=0.5, spec=0.5, normal=None, emit_col=None, emit_str=None, coat=0.0, sss=0.0, metal=0.0):
        nd = self.n.get("Principled BSDF")
        for k_, v in (("Base Color", base), ("Roughness", rough), ("Specular IOR Level", spec), ("Normal", normal),
                      ("Emission Color", emit_col), ("Emission Strength", emit_str), ("Coat Weight", coat),
                      ("Subsurface Weight", sss), ("Metallic", metal)):
            if v is None or k_ not in nd.inputs:
                continue
            if isinstance(v, (int, float, tuple)):
                nd.inputs[k_].default_value = v
            else:
                self.l.new(v, nd.inputs[k_])
        return nd


def new_mat(name):
    m = bpy.data.materials.get(name)
    if m:
        return m, None
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    return m, NT(m)


def mat_simple(name, col, rough=0.5, spec=0.5, emit=None, estr=0.0, metal=0.0, aodark=0.35):
    m, t = new_mat(name)
    if t is None:
        return m
    c = hexcol(col) if isinstance(col, str) else col
    base = t.mix(t.maprange(t.ao(0.3), 0.0, 1.0, aodark, 0.0), c, (0.0, 0.0, 0.0, 1.0)) if aodark > 0 else c
    t.bsdf(base, rough=rough, spec=spec, metal=metal,
           emit_col=hexcol(emit) if emit else None, emit_str=estr if emit else None)
    return m


def mat_emit(name, col, strength, soft=1.5):
    """Pure emission with see-through grazing edges (stylised fire / glow shells). soft=None: solid."""
    m, t = new_mat(name)
    if t is None:
        return m
    out = t.n.get("Material Output")
    bs = t.n.get("Principled BSDF")
    if bs:
        t.n.remove(bs)
    em = t.node("ShaderNodeEmission")
    em.inputs["Color"].default_value = hexcol(col)
    em.inputs["Strength"].default_value = strength
    if soft is None:
        t.link(em.outputs[0], out.inputs["Surface"])
        return m
    tr = t.node("ShaderNodeBsdfTransparent")
    lw = t.node("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    fac = t.math("POWER", lw.outputs["Facing"], soft)
    mx = t.node("ShaderNodeMixShader")
    t.link(fac, mx.inputs[0])
    t.link(em.outputs[0], mx.inputs[1])
    t.link(tr.outputs[0], mx.inputs[2])
    t.link(mx.outputs[0], out.inputs["Surface"])
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    return m


# ============================================================ tiny FK rig
class Rig:
    def __init__(self):
        self.bones = {}

    def add(self, name, parent, head):
        self.bones[name] = dict(parent=parent, head=Vector(head))

    def mats(self, pose):
        M = {}

        def get(n):
            if n in M:
                return M[n]
            b = self.bones[n]
            P = get(b["parent"]) if b["parent"] else Matrix.Identity(4)
            r = pose.get(n)
            if r is None:
                L = Matrix.Identity(4)
            else:
                R = Euler([math.radians(a) for a in r], "XYZ").to_matrix().to_4x4()
                L = Matrix.Translation(b["head"]) @ R @ Matrix.Translation(-b["head"])
            M[n] = P @ L
            return M[n]

        for n in self.bones:
            get(n)
        return M


# ============================================================ scene / render
def reset():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.cameras, bpy.data.curves):
        for d in list(coll):
            coll.remove(d)


def setup_render(samples=160):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        pr.compute_device_type = "OPTIX"
        pr.get_devices()
        for d in pr.devices:
            d.use = d.type == "OPTIX"
        sc.cycles.device = "GPU"
    except Exception as ex:
        log("GPU setup failed, CPU render:", ex)
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPTIX"
    except Exception:
        pass
    sc.cycles.max_bounces = 8
    sc.cycles.transparent_max_bounces = 16
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.image_settings.color_depth = "8"
    vt = VIEW_TRANSFORM
    sc.view_settings.view_transform = vt
    if vt == "AgX":
        for look in ("AgX - Punchy", "Punchy", "AgX - Medium High Contrast"):
            try:
                sc.view_settings.look = look
                break
            except Exception:
                continue
    sc.view_settings.exposure = VIEW_EXPOSURE.get(vt, 0.0)
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    w = sc.world
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = hexcol("#1a2c55")
    bg.inputs["Strength"].default_value = 0.55


def light(name, kind, loc, target, energy, color="#ffffff", size=3.0, coll=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.color = hexcol(color)[:3]
    if kind == "AREA":
        ld.size = size
        ld.shape = "DISK"
    elif kind in ("POINT", "SPOT"):
        ld.shadow_soft_size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = Vector(loc)
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    link(ob, coll)
    return ob


def studio_lights(c, R, warm="#fff1dc", rim1="#cfe0ff", rim2="#ffb070", fill="#8fb0ff", scale=1.0):
    """3-point rig around centre c with radius R (creature size)."""
    c = Vector(c)
    k = R * R * scale
    L = []
    L.append(light("Key", "AREA", c + Vector((-0.9, 1.2, 1.1)) * R * 1.6, c, 95 * k, warm, size=R * 1.2))
    L.append(light("Fill", "AREA", c + Vector((1.3, 0.9, 0.2)) * R * 1.8, c, 22 * k, fill, size=R * 1.5))
    L.append(light("RimR", "AREA", c + Vector((1.1, -1.2, 0.9)) * R * 1.5, c, 120 * k, rim1, size=R * 0.6))
    L.append(light("RimL", "AREA", c + Vector((-1.2, -1.1, 0.5)) * R * 1.5, c, 90 * k, rim2, size=R * 0.6))
    L.append(light("Top", "AREA", c + Vector((0.0, 0.0, 1.6)) * R * 1.6, c, 25 * k, "#ffffff", size=R * 2.0))
    return L


def shadow_catcher(size=60.0):
    me = bpy.data.meshes.new("Catcher")
    s = size / 2
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("Catcher", me)
    link(ob)
    ob.is_shadow_catcher = True
    return ob


def camera(name="Cam"):
    cd = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, cd)
    link(ob)
    bpy.context.scene.camera = ob
    cd.clip_start = 0.05
    cd.clip_end = 500
    return ob


def world_bbox(objs, include_hidden=False):
    pts = []
    for ob in objs:
        if ob.type != "MESH" or (ob.hide_render and not include_hidden):
            continue
        mw = ob.matrix_world
        pts.extend(mw @ Vector(c) for c in ob.bound_box)
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def render_to(path, w, h, samples=None):
    sc = bpy.context.scene
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = 100
    if samples:
        sc.cycles.samples = samples
    sc.render.filepath = path
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    log("rendered", os.path.basename(path), f"{w}x{h}", f"{time.time() - t0:.1f}s")


def ortho_view(cam, view, center, ppu, w, h, ground=0.0, dist=40.0):
    """view: front (+Y looks -Y), back, side (+X looks -X), side_l. ppu = pixels per stud."""
    cd = cam.data
    cd.type = "ORTHO"
    cd.ortho_scale = max(w, h) / ppu
    c = Vector(center)
    dirs = {"front": Vector((0, 1, 0)), "back": Vector((0, -1, 0)), "side": Vector((1, 0, 0)), "side_l": Vector((-1, 0, 0))}
    d = dirs[view]
    cam.location = c + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    return cam


def persp_view(cam, loc, target, lens=50.0):
    cd = cam.data
    cd.type = "PERSP"
    cd.lens = lens
    cd.sensor_width = 36
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def hide_all_but(objs):
    keep = set(o.name for o in objs)
    for ob in bpy.context.scene.objects:
        if ob.type in ("MESH",):
            ob.hide_render = ob.name not in keep


# ============================================================ CREATURE: CINDER DRAKE
DRAKE_COLS = dict(
    skin="#C8321E", skin_dark="#8E1F17", skin_hi="#E24A30", belly="#F2C77A", belly_dark="#C28A45",
    plate="#2E2A33", plate_hi="#575063", bone="#F2C77A", horn_tip="#3E2A1E", membrane="#9E2A1F",
    membrane_dark="#5E1612", wingbone="#5A1A14", lava="#FF9A1F", lava_core="#FFE066", eye="#FFD84A",
    claw="#2E262C", teeth="#F4E6C4",
)


def drake_materials():
    C = DRAKE_COLS
    mats = {}
    # --- skin with scales, belly plates and lava cracks
    m, t = new_mat("D_Skin")
    if t:
        co = t.objco()
        dors = t.maprange(t.attr("dorsal"), 0.15, 0.6, 0.0, 1.0)
        vor_s = t.voronoi(co, 8.0)
        vor_b = t.voronoi(co, 2.8)
        # small scales on flanks/limbs, big plated scales over the back
        dist = t.math("ADD", t.math("MULTIPLY", vor_s.outputs["Distance"], t.math("SUBTRACT", 1.0, dors)),
                      t.math("MULTIPLY", vor_b.outputs["Distance"], dors))
        edge = t.maprange(dist, 0.44, 0.58, 0.0, 1.0)

        def shingle(vor, scale):
            # overlapping-scale profile: each cell rises toward its back-bottom edge (scales overlap tailward/down)
            sc_ = t.node("ShaderNodeVectorMath")
            sc_.operation = "SCALE"
            t.link(co, sc_.inputs[0])
            sc_.inputs["Scale"].default_value = scale
            off = t.node("ShaderNodeVectorMath")
            off.operation = "SUBTRACT"
            t.link(sc_.outputs[0], off.inputs[0])
            t.link(vor.outputs["Position"], off.inputs[1])
            dp = t.node("ShaderNodeVectorMath")
            dp.operation = "DOT_PRODUCT"
            t.link(off.outputs[0], dp.inputs[0])
            dp.inputs[1].default_value = (0.0, -0.45, -0.89)
            return t.maprange(dp.outputs["Value"], -0.45, 0.45, 0.0, 1.0)

        sh = t.math("ADD", t.math("MULTIPLY", shingle(vor_s, 8.0), t.math("SUBTRACT", 1.0, dors)),
                    t.math("MULTIPLY", shingle(vor_b, 2.8), dors))
        dome = t.math("MULTIPLY", sh, t.math("SUBTRACT", 1.0, t.math("MULTIPLY", edge, 0.85)))
        sepc = t.node("ShaderNodeSeparateColor")
        t.link(vor_s.outputs["Color"], sepc.inputs[0])
        nz = t.noise(co, 1.1, 3.0, 0.55)
        base = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.7, 0, 1), hexcol("#A52617"), hexcol("#C9381F"))
        base = t.mix(t.math("MULTIPLY", sepc.outputs[0], 0.15), base, hexcol("#7E1A10"))
        geo = t.node("ShaderNodeNewGeometry")
        sepn = t.node("ShaderNodeSeparateXYZ")
        t.link(geo.outputs["Normal"], sepn.inputs[0])
        toplit = t.maprange(sepn.outputs["Z"], 0.2, 1.0, 0.0, 1.0)
        base = t.mix(t.math("MULTIPLY", toplit, 0.22), base, hexcol("#E0552F"))
        base = t.mix(t.math("MULTIPLY", sh, 0.16), base, hexcol("#D8502E"))
        base = t.mix(t.math("MULTIPLY", dors, 0.9), base, hexcol("#26090A"))
        base = t.mix(t.math("MULTIPLY", edge, 0.42), base, hexcol("#1E0404"))
        belly = t.maprange(t.attr("belly"), 0.42, 0.56, 0.0, 1.0)
        vs = t.attr("vs")
        band = t.maprange(t.math("SINE", t.math("MULTIPLY", vs, 20.0)), 0.72, 1.0, 0.0, 1.0)
        bellycol = t.mix(t.maprange(sepn.outputs["Z"], -1.0, 0.3, 0.0, 1.0), hexcol("#C48A42"), hexcol("#E6B66E"))
        bellycol = t.mix(band, bellycol, hexcol("#8A5A26"))
        col = t.mix(belly, base, bellycol)
        crackmask = t.attr("crack")
        nzc = t.noise(co, 2.2, 2.0, 0.5)
        warped = t.node("ShaderNodeVectorMath")
        warped.operation = "ADD"
        t.link(co, warped.inputs[0])
        t.link(nzc.outputs["Color"], warped.inputs[1])
        vc = t.voronoi(warped.outputs[0], 1.25, "DISTANCE_TO_EDGE")
        line = t.maprange(vc.outputs["Distance"], 0.0, 0.075, 1.0, 0.0)
        core = t.maprange(vc.outputs["Distance"], 0.0, 0.03, 1.0, 0.0)
        patch = t.maprange(t.noise(co, 0.75, 1.0, 0.5).outputs["Fac"], 0.44, 0.54, 0.0, 1.0)
        crack = t.math("MULTIPLY", t.math("MULTIPLY", line, crackmask), patch)
        col = t.mix(crack, col, hexcol("#160402"))
        aof = t.maprange(t.ao(0.45), 0.0, 1.0, 0.38, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        ecol = t.mix(core, hexcol("#ff3200"), hexcol("#ffc040"))
        estr = t.math("MULTIPLY", crack, 5.5)
        height = t.math("SUBTRACT", t.math("MULTIPLY", dome, t.math("SUBTRACT", 1.0, belly)),
                        t.math("ADD", t.math("MULTIPLY", band, t.math("MULTIPLY", belly, 0.8)), t.math("MULTIPLY", crack, 1.3)))
        t.bsdf(col, rough=0.5, spec=0.35, normal=t.bump(height, 0.38, 0.03), emit_col=ecol, emit_str=estr, coat=0.0)
    mats["skin"] = m
    # --- horn / claws / spikes: bone fading to black, ridged
    m, t = new_mat("D_Horn")
    if t:
        tt = t.attr("t")
        col = t.ramp(tt, [(0.0, hexcol("#E6BE7E")), (0.4, hexcol("#C08A4C")), (0.7, hexcol("#4E301E")), (0.9, hexcol("#1A1210")),
                          (1.0, hexcol("#0A0808"))])
        rid = t.maprange(t.math("SINE", t.math("MULTIPLY", tt, 70.0)), 0.6, 1.0, 0.0, 1.0)
        col = t.mix(t.math("MULTIPLY", rid, 0.45), col, hexcol("#4A2C18"))
        aof = t.maprange(t.ao(0.3), 0.0, 1.0, 0.45, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        t.bsdf(col, rough=0.3, spec=0.62, normal=t.bump(t.math("SUBTRACT", 1.0, rid), 0.32, 0.02), coat=0.3)
    mats["horn"] = m
    # --- dorsal plates + armour: glossy obsidian, red-hot tips
    m, t = new_mat("D_Plate")
    if t:
        ph = t.attr("ph")
        col = t.ramp(ph, [(0.0, hexcol("#0D0B10")), (0.55, hexcol("#1C1820")), (0.84, hexcol("#3A2C30")), (0.93, hexcol("#B4401A")),
                          (1.0, hexcol("#FF8A2A"))])
        aof = t.maprange(t.ao(0.25), 0.0, 1.0, 0.45, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        t.bsdf(col, rough=0.28, spec=0.65, coat=0.35, emit_col=hexcol("#ff5a14"), emit_str=t.maprange(ph, 0.86, 1.0, 0.0, 4.5))
    mats["plate"] = m
    # --- shoulder/thigh armour plates: matte charcoal-red, worn lighter rim, thin hot seam at the edge
    m, t = new_mat("D_Armor")
    if t:
        ph = t.attr("ph")
        co = t.objco()
        nz = t.noise(co, 4.0, 4.0, 0.6)
        rim = t.maprange(ph, 0.36, 0.52, 1.0, 0.0)
        keel = t.maprange(ph, 0.62, 0.8, 0.0, 1.0)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#2A100D"), hexcol("#43191A"))
        col = t.mix(t.math("MULTIPLY", keel, 0.55), col, hexcol("#6A3424"))
        col = t.mix(t.math("MULTIPLY", rim, 0.85), col, hexcol("#B0683E"))
        aof = t.maprange(t.ao(0.3), 0.0, 1.0, 0.45, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        t.bsdf(col, rough=0.42, spec=0.45, coat=0.12, normal=t.bump(nz.outputs["Fac"], 0.25, 0.02),
               emit_col=hexcol("#ff4a10"), emit_str=t.maprange(ph, 0.35, 0.39, 2.2, 0.0))
    mats["armor"] = m
    # --- membrane: dark, glowing veins along the finger bones, burning trailing edge, translucent
    m, t = new_mat("D_Membrane")
    if t:
        edge = t.attr("edge")
        bone = t.attr("bonefac")
        co = t.objco()
        nz = t.noise(co, 3.0, 3.0, 0.6)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.3, 0.7, 0, 1), hexcol("#5E140F"), hexcol("#7C1E16"))
        col = t.mix(bone, col, hexcol("#2E0A07"))
        glow = t.maprange(edge, 0.8, 1.0, 0.0, 1.0)
        vein = t.maprange(bone, 0.55, 1.0, 0.0, 1.0)
        col = t.mix(glow, col, hexcol("#d4401a"))
        bs = t.bsdf(col, rough=0.62, spec=0.3, emit_col=hexcol("#ff4410"),
                    emit_str=t.math("ADD", t.math("MULTIPLY", glow, 1.8), t.math("MULTIPLY", vein, 0.7)))
        tr = t.node("ShaderNodeBsdfTranslucent")
        tr.inputs["Color"].default_value = hexcol("#ff4a1e")
        mixs = t.node("ShaderNodeMixShader")
        mixs.inputs[0].default_value = 0.22
        out = t.n.get("Material Output")
        t.link(bs.outputs[0], mixs.inputs[1])
        t.link(tr.outputs[0], mixs.inputs[2])
        t.link(mixs.outputs[0], out.inputs["Surface"])
    mats["membrane"] = m
    mats["wingbone"] = mat_simple("D_WingBone", "#3E120E", rough=0.42)
    mats["claw"] = mat_simple("D_Claw", C["claw"], rough=0.28, spec=0.7)
    mats["teeth"] = mat_simple("D_Teeth", C["teeth"], rough=0.3, spec=0.6)
    mats["eye"] = mat_simple("D_Eye", "#FFC23A", rough=0.15, spec=0.8, emit="#FFC23A", estr=7.0, aodark=0.0)
    mats["pupil"] = mat_simple("D_Pupil", "#120606", rough=0.12, spec=0.9)
    m, t = new_mat("D_MouthGlow")
    if t:
        co = t.objco()
        sep = t.node("ShaderNodeSeparateXYZ")
        t.link(co, sep.inputs[0])
        g = t.maprange(sep.outputs["Y"], 3.95, 3.1, 0.0, 1.0)
        t.bsdf(hexcol("#2A0806"), rough=0.6, spec=0.3, emit_col=hexcol("#ff4a08"), emit_str=t.math("MULTIPLY", g, 7.0))
    mats["mouth"] = m
    mats["tongue"] = mat_simple("D_Tongue", "#C2403C", rough=0.35)
    mats["flame_o"] = mat_emit("D_FlameOuter", "#ff2a04", 2.4, soft=2.2)
    mats["flame_m"] = mat_emit("D_FlameMid", "#ff6a0a", 3.0, soft=1.6)
    mats["flame_c"] = mat_emit("D_FlameCore", "#ffb030", 3.6, soft=0.9)
    return mats


def drake_rig():
    r = Rig()
    r.add("root", None, (0, -0.4, 2.3))
    r.add("chest", "root", (0, 0.6, 2.5))
    r.add("neck", "chest", (0, 1.2, 3.2))
    r.add("head", "neck", (0, 2.45, 4.62))
    r.add("jaw", "head", (0, 2.45 + 0.37 * HEAD_SCALE, 4.62 - 0.02 * HEAD_SCALE))
    r.add("tail1", "root", (0, -2.1, 2.3))
    r.add("tail2", "tail1", (0, -3.25, 1.62))
    r.add("tail3", "tail2", (0, -4.35, 1.25))
    r.add("tail4", "tail3", (0, -5.0, 1.42))
    r.add("wing_L", "chest", (0.82, 0.72, 3.42))
    r.add("wing_R", "chest", (-0.82, 0.72, 3.42))
    return r


def drake_body_prims():
    P = []
    # torso mass: big chest + shoulders, slimmer waist, strong haunches
    P += [P_ell("root", (0, -0.3, 2.36), (1.1, 1.85, 1.2), (-4, 0, 0), k=0.45),
          P_ell("root", (0, -1.45, 2.42), (1.14, 1.1, 1.16), k=0.45),
          P_ell("root", (0, -0.1, 1.8), (0.95, 1.45, 0.7), k=0.45),
          P_ell("chest", (0, 0.95, 2.6), (1.26, 1.22, 1.38), (8, 0, 0), k=0.45),
          P_ell("chest", (0, 0.55, 3.25), (0.95, 1.0, 0.7), k=0.4)]
    # v2 muscle forms: pecs, deltoids, haunches, ribcage
    musc = [P_ell("chest", (0.56, 1.62, 2.2), (0.5, 0.42, 0.62), (12, 0, 10), k=0.3),
            P_ell("chest", (1.0, 1.05, 2.98), (0.46, 0.62, 0.5), (0, 20, 0), k=0.3),
            P_ell("root", (1.04, -1.22, 2.3), (0.44, 0.78, 0.72), (-20, 0, 0), k=0.3),
            P_ell("root", (0.72, -0.25, 2.35), (0.5, 1.05, 0.78), k=0.35)]
    P += musc + mirror_x(musc)
    # neck: thicker, muscular
    P += [P_cone("neck", (0, 1.15, 3.2), (0, 1.95, 4.05), 0.86, 0.64, k=0.3),
          P_cone("neck", (0, 1.95, 4.05), (0, 2.5, 4.62), 0.64, 0.54, k=0.22)]
    # head v2: flat brutal skull, long snout with a nasal ridge, scowling brows over narrow slanted sockets
    hd = [P_ell("head", (0, 2.98, 4.97), (0.74, 0.86, 0.56), (6, 0, 0), k=0.25),
          P_cone("head", (0, 3.15, 4.95), (0, 4.88, 4.83), 0.55, 0.35, k=0.25),
          P_ell("head", (0, 2.45, 5.0), (0.5, 0.52, 0.45), k=0.25),
          P_cone("head", (0, 3.45, 5.3), (0, 4.75, 5.07), 0.18, 0.1, k=0.1),
          P_ell("head", (0, 2.72, 5.38), (0.44, 0.52, 0.17), k=0.12),
          P_box("head", (0, 4.0, 4.43), (0.9, 1.25, 0.12), rnd=0.05, k=0.06, mode="sub")]
    hs = [P_cone("head", (0.68, 3.0, 5.48), (0.2, 3.95, 5.2), 0.21, 0.12, k=0.07),
          P_cone("head", (0.62, 2.75, 4.86), (0.5, 3.75, 4.86), 0.24, 0.13, k=0.1),
          P_ell("head", (0.55, 2.7, 4.68), (0.32, 0.42, 0.34), k=0.14),
          P_sph("head", (0.21, 4.8, 5.0), 0.13, k=0.07),
          P_ell("head", (0.58, 3.52, 5.12), (0.11, 0.21, 0.085), (-22, 0, -20), k=0.04, mode="sub"),
          P_sph("head", (0.21, 4.92, 5.02), 0.05, k=0.03, mode="sub")]
    P += hd + hs + mirror_x(hs)
    # front legs (L, mirrored): thick, chunky paws, elbow knob, toes
    fl = [P_ell("chest", (0.92, 1.12, 2.62), (0.56, 0.76, 0.82), k=0.3),
          P_cone("chest", (1.02, 1.2, 2.3), (1.07, 1.02, 1.12), 0.58, 0.45, k=0.22),
          P_cone("chest", (1.07, 1.02, 1.12), (1.08, 1.34, 0.36), 0.45, 0.36, k=0.15),
          P_ell("chest", (1.08, 1.56, 0.22), (0.46, 0.62, 0.24), k=0.16),
          P_sph("chest", (1.08, 0.88, 1.15), 0.34, k=0.15)]
    fl += [P_ell("chest", (1.08 + dx, 1.98, 0.17), (0.14, 0.24, 0.15), k=0.08) for dx in (-0.25, 0.0, 0.25)]
    # back legs
    bl = [P_ell("root", (0.98, -1.45, 1.96), (0.62, 1.02, 0.98), (-15, 0, 0), k=0.32),
          P_cone("root", (1.05, -1.02, 1.32), (1.08, -1.55, 0.55), 0.5, 0.36, k=0.18),
          P_cone("root", (1.08, -1.55, 0.52), (1.09, -0.98, 0.22), 0.36, 0.3, k=0.12),
          P_ell("root", (1.09, -0.9, 0.22), (0.46, 0.6, 0.24), k=0.14)]
    bl += [P_ell("root", (1.09 + dx, -0.48, 0.17), (0.14, 0.24, 0.15), k=0.08) for dx in (-0.25, 0.0, 0.25)]
    P += fl + mirror_x(fl) + bl + mirror_x(bl)
    # tail chain
    P += [P_cone("tail1", (0, -2.1, 2.3), (0, -3.25, 1.62), 0.7, 0.5, k=0.25),
          P_cone("tail2", (0, -3.25, 1.62), (0, -4.35, 1.25), 0.5, 0.36, k=0.15),
          P_cone("tail3", (0, -4.35, 1.25), (0, -5.0, 1.42), 0.36, 0.26, k=0.12),
          P_cone("tail4", (0, -5.0, 1.42), (0, -5.28, 2.1), 0.26, 0.17, k=0.1),
          P_cone("tail4", (0, -5.28, 2.1), (0, -5.2, 2.62), 0.17, 0.1, k=0.08)]
    return scale_prims_about(P, ("head",), HEAD_PIVOT, HEAD_SCALE)


def drake_jaw_prims():
    P = [P_cone("jaw", (0, 2.9, 4.5), (0, 4.62, 4.48), 0.47, 0.3, k=0.2),
         P_ell("jaw", (0, 4.52, 4.36), (0.3, 0.32, 0.19), k=0.1),
         P_ell("jaw", (0.38, 3.1, 4.42), (0.17, 0.55, 0.24), k=0.1),
         P_ell("jaw", (-0.38, 3.1, 4.42), (0.17, 0.55, 0.24), k=0.1),
         P_box("jaw", (0, 3.7, 4.98), (0.9, 1.35, 0.36), rnd=0.05, k=0.08, mode="sub")]
    return scale_prims_about(P, ("jaw",), HEAD_PIVOT, HEAD_SCALE)


def wing_points(side, spread):
    """Wing joint positions in rest world coords for one side (+1 = left/+X)."""
    s = side
    fold = dict(S=(0.82, 0.72, 3.42), W=(1.8, -0.3, 6.0), F1=(1.6, -2.55, 5.5), F2=(1.45, -2.25, 4.35),
                F3=(1.24, -1.35, 3.7), B=(0.9, -0.62, 3.35))
    open_ = dict(S=(0.82, 0.72, 3.42), W=(3.35, 0.2, 6.45), F1=(6.1, -1.1, 5.7), F2=(5.6, -2.45, 4.1),
                 F3=(3.7, -2.45, 3.0), B=(1.0, -0.95, 3.2))
    out = {}
    for k in fold:
        a = np.array(fold[k]); b = np.array(open_[k])
        v = a + (b - a) * spread
        v[0] *= s
        out[k] = Vector(v)
    return out


def build_wing(side, spread, mats, name):
    wp = wing_points(side, spread)
    S, W, B = wp["S"], wp["W"], wp["B"]
    tips = [wp["F1"], wp["F2"], wp["F3"]]
    objs = []
    # membrane = fans from the wrist W: F1-F2, F2-F3, F3-B (scalloped, glowing trailing edge) and B-S (body side)
    chain = tips + [B, S]
    bm = bmesh.new()
    ev, bv = [], []
    nrad, nalong = 8, 10
    for pi in range(len(chain) - 1):
        A, Bt = chain[pi], chain[pi + 1]
        trailing = pi < 3
        nrm = (A - W).cross(Bt - W)
        nrm = nrm.normalized() if nrm.length > 1e-6 else Vector((0, 0, 1))
        wv = bm.verts.new(W)
        ev.append(0.0)
        bv.append(1.0)
        rows = []
        for i in range(nalong):
            u = i / (nalong - 1)
            e = A + (Bt - A) * u
            if trailing:
                e = e + (W - (A + Bt) * 0.5) * (math.sin(math.pi * u) ** 0.8 * 0.34)
            row = []
            for j in range(1, nrad):
                v = j / (nrad - 1)
                pt = W + (e - W) * v + nrm * (math.sin(math.pi * v) * math.sin(math.pi * u) * 0.07)
                row.append(bm.verts.new(pt))
                ev.append(v if trailing else 0.0)
                bv.append(max(0.0, 1.0 - min(u, 1 - u) * 7.0) * (1 - 0.3 * v))
            rows.append(row)
        for i in range(nalong - 1):
            bm.faces.new((wv, rows[i + 1][0], rows[i][0]))
            for j in range(nrad - 2):
                bm.faces.new((rows[i][j], rows[i + 1][j], rows[i + 1][j + 1], rows[i][j + 1]))
    me_obj = bm_to_obj(bm, name + "_Membrane", mats["membrane"], {"edge": ev, "bonefac": bv})
    mod = me_obj.modifiers.new("Solid", "SOLIDIFY")
    mod.thickness = 0.035
    mod.offset = 0.0
    objs.append(me_obj)
    # bones: arm, fingers running past the membrane, hooked claws at the finger tips
    objs.append(sweep([S, S + (W - S) * 0.5, W], [0.2, 0.15, 0.105], 12, name=name + "_Arm", mat=mats["wingbone"]))
    for i, q in enumerate(tips):
        q2 = q + (q - W) * 0.1
        pts = [W + (q2 - W) * (k / 6) for k in range(7)]
        objs.append(sweep(pts, [0.095 - 0.07 * k / 6 for k in range(7)], 8, name=name + f"_Finger{i}", mat=mats["wingbone"]))
        objs.append(spike(name + f"_FingerClaw{i}", q2 - (q - W).normalized() * 0.04, (q - W), 0.2, 0.045, mats["horn"], curve=-0.35))
    # wrist hook + leading-edge spikes
    up = (W - S).normalized()
    objs.append(spike(name + "_Thumb", W, up + Vector((0, 0.35, 0.2)), 0.46, 0.08, mats["horn"], curve=0.3))
    for k, fr in enumerate((0.42, 0.7)):
        base = S + (W - S) * fr
        objs.append(spike(name + f"_ArmSpike{k}", base, Vector((0, 0.75, 0.6)) + up * 0.25, 0.24, 0.06, mats["horn"], curve=0.2))
    return objs


def place_plates(body_obj, mats, rig):
    """Raycast the rest body along the spine; build dorsal plates; return (obj, bone) pairs."""
    me = body_obj.data
    verts = vcoords(me)
    polys = [tuple(p.vertices) for p in me.polygons]
    bvh = BVHTree.FromPolygons([tuple(v) for v in verts], polys)
    out = []

    def bone_for(y):
        if y > 2.0:
            return "head"
        if y > 1.25:
            return "neck"
        if y > 0.4:
            return "chest"
        if y > -2.1:
            return "root"
        if y > -3.25:
            return "tail1"
        if y > -4.35:
            return "tail2"
        return "tail3"

    def plate_size(y):
        # small on the neck, tallest over the shoulders/back, shrinking down the tail (v2: ~35% taller)
        if y > 1.3:
            return 0.36 + (2.3 - y) * 0.2
        if y > -1.8:
            return 0.84 + 0.12 * math.cos((y + 0.25) * 1.1)
        return max(0.2, 0.8 - (-1.8 - y) * 0.2)

    ys = list(np.linspace(2.3, -4.6, 17))
    for i, y in enumerate(ys):
        hit = bvh.ray_cast(Vector((0, y, 12)), Vector((0, 0, -1)))
        if hit[0] is None:
            continue
        loc, nrm = hit[0], hit[1]
        hgt = plate_size(y)
        L = hgt * 0.92
        f, u, s = basis_from(Vector((0, 1, 0)), nrm)
        T = 0.06 + hgt * 0.05
        pts = []
        for a in range(12):
            ang = 2 * math.pi * a / 12
            pts.append(loc + f * (math.cos(ang) * L * 0.5) + s * (math.sin(ang) * T) - u * 0.14)
        for a in range(8):
            ang = 2 * math.pi * a / 8
            pts.append(loc + f * (math.cos(ang) * L * 0.28 - L * 0.16) + s * (math.sin(ang) * T * 0.55) + u * hgt * 0.5)
        pts.append(loc + u * hgt - f * L * 0.48)
        base_c = loc - u * 0.14

        def af(co, base_c=base_c, u=u, hgt=hgt):
            return {"ph": max(0.0, min(1.0, (co - base_c).dot(u) / (hgt + 0.14)))}

        ob = hull_obj(pts, f"D_Plate{i:02d}", mats["plate"], af)
        mod = ob.modifiers.new("Sub", "SUBSURF")
        mod.levels = mod.render_levels = 1
        out.append((ob, bone_for(y)))
        # two side spike rows flanking the plates over the back
        if -2.6 < y < 1.5:
            for sx in (1, -1):
                h2 = bvh.ray_cast(Vector((0.44 * sx, y - 0.2, 12)), Vector((0, 0, -1)))
                if h2[0] is None:
                    continue
                d = (h2[1] + Vector((0.55 * sx, -0.35, 0.25))).normalized()
                sp = spike(f"D_SideSpike{i:02d}{'L' if sx > 0 else 'R'}", h2[0] - d * 0.06, d, hgt * 0.42 + 0.1, 0.075 + hgt * 0.03,
                           mats["plate"], curve=-0.1, tattr="ph")
                out.append((sp, bone_for(y)))
    # armour: large curved plates that hug the shoulders and thighs, overlapping like shingles (back-down)
    specs = [("chest", 1.5, 3.0, 0.95, 0.72), ("chest", 1.0, 2.62, 0.9, 0.7), ("chest", 1.5, 2.35, 0.8, 0.62),
             ("root", -1.15, 2.55, 0.95, 0.72), ("root", -1.7, 2.2, 0.85, 0.66), ("root", -1.2, 1.95, 0.75, 0.58)]
    for j, (bone, y, z, a, b) in enumerate(specs):
        for sx in (1, -1):
            res = conforming_plate(bvh, f"D_Armor{j}{'L' if sx > 0 else 'R'}", Vector((3.0 * sx, y, z)), Vector((-sx, 0, 0)),
                                   a, b, mats["armor"], thick=0.06)
            if res is None:
                continue
            ob, loc, nrm, d1 = res
            out.append((ob, bone))
            sp = spike(f"D_ArmorSpike{j}{'L' if sx > 0 else 'R'}", loc + nrm * 0.05 + d1 * (a * 0.12), nrm * 0.65 + d1 * 0.75,
                       0.3 * a + 0.05, 0.075, mats["horn"], curve=0.2, up=nrm)
            out.append((sp, bone))
    return out


def conforming_plate(bvh, name, origin, direction, a, b, mat, thick=0.07, dvec=Vector((0, -0.75, -0.65)), nu=9, nv=7):
    """Armour plate that follows the body: grid points raycast onto the surface, domed outward, pointed at
    the trailing (back-down) end, given thickness with Solidify. Attribute ph peaks along the raised keel."""
    hit = bvh.ray_cast(origin, direction)
    if hit[0] is None:
        return None
    loc, nrm = hit[0], hit[1]
    d1 = (dvec - nrm * dvec.dot(nrm)).normalized()
    d2 = nrm.cross(d1).normalized()
    bm = bmesh.new()
    grid, phs = [], []
    for i in range(nu):
        u = -1.0 + 2.0 * i / (nu - 1)
        half_w = math.sqrt(max(0.0, 1.0 - (max(u, 0.0) ** 1.6) * 0.95)) * (1.0 - 0.12 * max(-u, 0.0) ** 2)
        row = []
        for k in range(nv):
            v = (-1.0 + 2.0 * k / (nv - 1)) * half_w
            p0 = loc + d1 * (u * a * 0.5) + d2 * (v * b * 0.5)
            h = bvh.ray_cast(p0 + nrm * 0.8, -nrm, 2.0)
            if h[0] is None:
                sp, sn = p0, nrm
            else:
                sp, sn = h[0], h[1]
            vn = abs(v / max(half_w, 1e-3))
            r2 = min(1.0, u * u * 0.5 + vn * vn * 0.7)
            # scute profile: flat plate with a sharp keel ridge along its length (not a pillowy dome)
            keel = (1.0 - vn ** 1.4) * (0.55 + 0.45 * (1.0 - u * u))
            lift = 0.022 + thick * keel
            row.append(bm.verts.new(sp + sn * lift))
            phs.append(0.35 + 0.45 * min(1.0, keel * 0.9 + (1.0 - r2) * 0.2))
        grid.append(row)
    for i in range(nu - 1):
        for k in range(nv - 1):
            bm.faces.new((grid[i][k], grid[i + 1][k], grid[i + 1][k + 1], grid[i][k + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    f0 = bm.faces[0]
    f0.normal_update()
    if f0.normal.dot(nrm) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    ob = bm_to_obj(bm, name, mat, {"ph": phs}, smooth=False)
    md = ob.modifiers.new("Solid", "SOLIDIFY")
    md.thickness = 0.05
    md.offset = -1.0
    md2 = ob.modifiers.new("Bevel", "BEVEL")
    md2.width = 0.012
    md2.segments = 1
    md2.limit_method = "ANGLE"
    return ob, loc, nrm, d1


def drake_parts(mats):
    """Hard parts in rest pose: list of (object, bone). v2: horns, frill, spikes, fangs, glowing throat."""
    parts = []
    H = mats["horn"]
    for s in (1, -1):
        sd = "L" if s > 0 else "R"
        # main horns: cubic sweep up and back, curling down at the tip (ram-like)
        pts = bezier3((0.42 * s, 2.66, 5.42), (0.92 * s, 2.0, 6.3), (1.5 * s, 1.0, 6.42), (1.4 * s, 0.42, 5.78), 22)
        rad = [0.31 * (1 - i / 21) ** 0.8 + 0.01 for i in range(22)]
        rad[-1] = 0.0
        parts.append((sweep(pts, rad, 16, name=f"D_Horn{sd}", mat=H), "head"))
        # secondary horn pair under the main horns
        pts = bezier3((0.6 * s, 2.55, 5.05), (0.95 * s, 2.1, 5.3), (1.22 * s, 1.75, 5.2), (1.3 * s, 1.5, 4.95), 12)
        rad = [0.17 * (1 - i / 11) ** 0.85 for i in range(12)]
        parts.append((sweep(pts, rad, 12, name=f"D_Horn2{sd}", mat=H), "head"))
        # frill: three spikes fanning back behind the jaw hinge
        for j, (base, dvec, ln, r) in enumerate((((0.55 * s, 2.35, 5.0), (0.5 * s, -0.85, 0.2), 0.52, 0.11),
                                                  ((0.6 * s, 2.42, 4.75), (0.55 * s, -0.82, -0.05), 0.44, 0.1),
                                                  ((0.55 * s, 2.48, 4.5), (0.5 * s, -0.8, -0.3), 0.36, 0.085))):
            parts.append((spike(f"D_Frill{j}{sd}", base, dvec, ln, r, H, curve=0.12), "head"))
        # jaw-line spikes
        for j, (base, ln, r) in enumerate((((0.62 * s, 2.72, 4.55), 0.38, 0.1), ((0.64 * s, 3.02, 4.5), 0.3, 0.085),
                                            ((0.6 * s, 3.32, 4.46), 0.22, 0.07))):
            parts.append((spike(f"D_JawSpike{j}{sd}", base, (0.55 * s, -0.78, -0.2), ln, r, H, curve=0.1), "head"))
        # narrow, slanted, glowing eye with a vertical slit
        ec = Vector((0.6 * s, 3.52, 5.12))
        parts.append((ellipsoid_obj(f"D_Eye{s}", ec, (0.12, 0.2, 0.095), mats["eye"], rot=(-22, 0, -20 * s), segs=(20, 12)), "head"))
        out_dir = Vector((0.85 * s, 0.45, 0.22)).normalized()
        parts.append((ellipsoid_obj(f"D_Pupil{s}", ec + out_dir * 0.085, (0.022, 0.03, 0.085), mats["pupil"], rot=(-10, 0, -20 * s)), "head"))
        # teeth: upper row with a long overbite fang that hangs past the jaw, lower row on the jaw
        for k, (y, ln) in enumerate(((3.72, 0.1), (3.95, 0.13), (4.18, 0.34), (4.4, 0.15), (4.62, 0.12), (4.8, 0.09))):
            xr = 0.36 - (y - 3.5) * 0.12
            b = Vector((xr * s, y, 4.58))
            parts.append((sweep([b, b + Vector((0, 0.01, -ln * 0.6)), b + Vector((0.01 * s, 0.03, -ln))], [0.05 + ln * 0.14, 0.032, 0.0], 8,
                                name=f"D_ToothU{k}{s}", mat=mats["teeth"]), "head"))
        for k, (y, ln) in enumerate(((3.82, 0.1), (4.05, 0.16), (4.3, 0.1), (4.5, 0.09))):
            xr = 0.31 - (y - 3.5) * 0.1
            b = Vector((xr * s, y, 4.6))
            parts.append((sweep([b, b + Vector((0, 0.01, ln * 0.6)), b + Vector((0, 0.02, ln))], [0.045, 0.028, 0.0], 7,
                                name=f"D_ToothL{k}{s}", mat=mats["teeth"]), "jaw"))
        # claws: 3 per paw, long and hooked, bone -> black (horn ramp)
        for bone, py in (("chest", 1.56), ("root", -0.9)):
            for c, dx in enumerate((-0.25, 0.0, 0.25)):
                b = Vector((1.08 * s + dx, py + 0.5, 0.2))
                pts = [b, b + Vector((0, 0.2, 0.03)), b + Vector((0, 0.36, -0.06)), b + Vector((0, 0.45, -0.2))]
                parts.append((sweep(pts, [0.1, 0.075, 0.04, 0.0], 8, name=f"D_Claw{bone}{c}{s}", mat=H), bone))
        # elbow + heel spikes
        parts.append((spike(f"D_Elbow{sd}", (1.1 * s, 0.86, 1.2), (0.22 * s, -0.8, -0.35), 0.44, 0.12, H, curve=0.15), "chest"))
        parts.append((spike(f"D_Elbow2{sd}", (1.07 * s, 0.92, 1.58), (0.2 * s, -0.88, 0.05), 0.3, 0.09, H, curve=0.12), "chest"))
        parts.append((spike(f"D_Heel{sd}", (1.1 * s, -1.72, 0.72), (0.16 * s, -0.9, 0.18), 0.36, 0.1, H, curve=0.12), "root"))
        # tail side spikes and the tail-tip blades
        for j, (base, dvec, ln, bone) in enumerate((((0.24 * s, -4.45, 1.3), (0.85 * s, -0.5, 0.15), 0.32, "tail3"),
                                                      ((0.2 * s, -4.82, 1.38), (0.85 * s, -0.45, 0.25), 0.27, "tail3"),
                                                      ((0.17 * s, -5.1, 1.72), (0.9 * s, -0.3, 0.35), 0.22, "tail4"))):
            parts.append((spike(f"D_TailSpike{j}{sd}", base, dvec, ln, 0.08, H, curve=0.15), bone))
        parts.append((spike(f"D_TailBlade{sd}", (0.08 * s, -5.24, 2.42), (0.65 * s, -0.5, 0.55), 0.42, 0.1, H, curve=0.18), "tail4"))
    # midline crest, nose horn, chin spike, centre tail blade
    for j, (base, ln, r) in enumerate((((0, 2.55, 5.44), 0.44, 0.11), ((0, 2.28, 5.3), 0.38, 0.1), ((0, 2.02, 5.12), 0.32, 0.09))):
        parts.append((spike(f"D_Crest{j}", base, (0, -0.55, 0.83), ln, r, H, curve=-0.1), "head"))
    parts.append((sweep([Vector((0, 4.42, 5.16)), Vector((0, 4.56, 5.4)), Vector((0, 4.64, 5.58)), Vector((0, 4.62, 5.7))],
                        [0.13, 0.08, 0.035, 0.0], 10, name="D_NoseHorn", mat=H), "head"))
    parts.append((spike("D_ChinSpike", (0, 4.45, 4.25), (0, 0.45, -0.9), 0.24, 0.08, H, curve=0.1), "jaw"))
    parts.append((spike("D_TailBladeC", (0, -5.26, 2.45), (0, -0.85, 0.5), 0.48, 0.11, H, curve=0.15), "tail4"))
    # mouth interior (glows hot toward the throat) + tongue
    parts.append((ellipsoid_obj("D_Mouth", (0, 3.7, 4.58), (0.36, 0.85, 0.2), mats["mouth"], segs=(18, 10)), "head"))
    parts.append((ellipsoid_obj("D_Tongue", (0, 3.75, 4.66), (0.22, 0.6, 0.07), mats["tongue"], segs=(16, 8)), "jaw"))
    # tail flame (3 nested flame shells)
    tip = Vector((0, -5.2, 2.58))
    for name_, mat_, sc_ in (("D_FlameO", mats["flame_o"], 1.0), ("D_FlameM", mats["flame_m"], 0.68), ("D_FlameC", mats["flame_c"], 0.4)):
        bm = bmesh.new()
        rings = []
        segs = 14
        prof = [(0.0, -0.05), (0.2, 0.05), (0.27, 0.2), (0.24, 0.4), (0.17, 0.62), (0.09, 0.85), (0.0, 1.05)]
        for r_, z_ in prof:
            if r_ < 1e-4:
                rings.append([bm.verts.new(tip + Vector((0, 0, z_ * sc_ * 1.2)))])
                continue
            ring = []
            for j in range(segs):
                a = 2 * math.pi * j / segs
                wob = 1.0 + 0.18 * math.sin(a * 3 + z_ * 6)
                ring.append(bm.verts.new(tip + Vector((math.cos(a) * r_ * wob * sc_, math.sin(a) * r_ * wob * sc_ * 0.8 - z_ * 0.12 * sc_, z_ * sc_ * 1.2))))
            rings.append(ring)
        for i in range(len(rings) - 1):
            A, Bq = rings[i], rings[i + 1]
            for j in range(segs):
                j2 = (j + 1) % segs
                if len(A) == 1:
                    bm.faces.new((A[0], Bq[j2], Bq[j]))
                elif len(Bq) == 1:
                    bm.faces.new((A[j], A[j2], Bq[0]))
                else:
                    bm.faces.new((A[j], A[j2], Bq[j2], Bq[j]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        ob = bm_to_obj(bm, name_, mat_)
        ob.visible_shadow = False
        parts.append((ob, "tail4"))
    return parts


VENTRAL = [((0, 3.35, 4.42), "head"), ((0, 2.75, 4.22), "head"), ((0, 2.25, 3.75), "neck"), ((0, 1.65, 3.0), "neck"),
           ((0, 1.25, 2.1), "chest"), ((0, 0.75, 1.4), "chest"), ((0, -0.2, 1.1), "root"), ((0, -1.3, 1.25), "root"),
           ((0, -2.25, 1.68), "tail1"), ((0, -3.3, 1.18), "tail2"), ((0, -4.35, 0.92), "tail3"), ((0, -5.0, 1.18), "tail4"),
           ((0, -5.38, 1.95), "tail4")]


def polyline_param(v, pts):
    best_d = np.full(len(v), 1e9, np.float32)
    best_s = np.zeros(len(v), np.float32)
    acc = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        ab = b - a
        L = float(np.linalg.norm(ab))
        t = np.clip(((v - a) @ ab) / (L * L), 0.0, 1.0)
        d = np.linalg.norm(v - (a + t[:, None] * ab), axis=1)
        m = d < best_d
        best_d[m] = d[m]
        best_s[m] = acc + t[m] * L
        acc += L
    return best_s


HEAD_PIVOT = Vector((0, 2.45, 4.62))
HEAD_SCALE = 1.04  # v1 used 1.12; a slightly smaller head reads less cute, more dangerous


def scale_prims_about(prims, bones, pivot, s):
    out = []
    pv = np.array(pivot, np.float32)
    for p in prims:
        if p["bone"] not in bones:
            out.append(p)
            continue
        q = dict(p)
        for key in ("c", "a", "b"):
            if key in q:
                q[key] = (pv + (q[key] - pv) * s).astype(np.float32)
        for key in ("rad", "half"):
            if key in q:
                q[key] = (q[key] * s).astype(np.float32)
        for key in ("r", "r1", "r2", "rnd"):
            if key in q:
                q[key] = q[key] * s
        q["k"] = q["k"] * s
        out.append(q)
    return out


def drake_attrs(me, M):
    """Per-vertex zone masks for the body shader (belly, cracks, ventral band coordinate)."""
    v = vcoords(me)
    n = vnormals(me)
    pts = [np.array(M[b] @ Vector(p), np.float32) for p, b in VENTRAL]
    set_point_attr(me, "vs", polyline_param(v, pts))
    x, y, z = v[:, 0], v[:, 1], v[:, 2]
    nx, ny, nz = n[:, 0], n[:, 1], n[:, 2]
    belly = np.zeros(len(v), np.float32)
    # underside of torso/neck/tail and throat/chest front
    under = np.clip((-nz - 0.15) / 0.35, 0, 1) * np.clip(1.0 - (np.abs(x) - 0.55) / 0.35, 0, 1)
    under *= (z > 0.9).astype(np.float32) * (z < 4.75).astype(np.float32)
    throat = np.clip((ny - 0.25) / 0.35, 0, 1) * np.clip(1.0 - (np.abs(x) - 0.42) / 0.3, 0, 1) * ((y > 0.9) & (y < 3.3) & (z > 1.6) & (z < 4.7)).astype(np.float32)
    tail_under = np.clip((-nz - 0.1) / 0.35, 0, 1) * (y < -2.0).astype(np.float32) * np.clip(1.0 - (np.abs(x) - 0.25) / 0.2, 0, 1)
    belly = np.maximum.reduce([under, throat, tail_under])
    belly[z < 0.75] = 0.0  # feet
    notbelly = np.clip(1.0 - belly * 2, 0, 1)
    # v2: dark charcoal back (also the top of the head), fading to crimson flanks
    dorsal = np.clip((nz - 0.1) / 0.4, 0, 1) * (z > 1.7).astype(np.float32) * notbelly
    # v2: wider lava-crack coverage over back, shoulders, thighs, neck and tail base
    crack = np.clip((nz + 0.15) / 0.5, 0, 1) * ((y > -3.2) & (y < 2.5) & (z > 1.6)).astype(np.float32)
    thigh = np.clip((np.abs(nx) - 0.3) / 0.3, 0, 1) * ((y > -2.3) & (y < -0.7) & (z > 1.2) & (z < 2.8)).astype(np.float32)
    shoulder = np.clip((np.abs(nx) - 0.3) / 0.3, 0, 1) * ((y > 0.6) & (y < 1.8) & (z > 1.6) & (z < 3.3)).astype(np.float32)
    neck = ((y > 1.2) & (y < 2.5) & (z > 3.0)).astype(np.float32) * np.clip(np.abs(nx) - 0.25, 0, 1)
    crack = np.maximum.reduce([crack, thigh, shoulder, neck * 0.9]) * notbelly
    set_point_attr(me, "belly", belly)
    set_point_attr(me, "crack", crack)
    set_point_attr(me, "dorsal", dorsal)


class Creature:
    def __init__(self, key):
        self.key = key
        self.objs = []
        self.parts = []  # (obj, bone)


def build_drake_pose(pose, mats, rig, plates_cache, coll_name="Drake", wing_spread=0.0, h=0.04):
    t0 = time.time()
    M = rig.mats(pose)
    cr = Creature("drake")
    # body
    prims = [xform_prim(p, M[p["bone"]]) for p in drake_body_prims()]
    v, f = sdf_mesh(prims, h)
    v = taubin(v, f, 6)
    if signed_volume(v, f) < 0:
        f = f[:, ::-1]
    me = mesh_from_np("D_Body", v, f)
    drake_attrs(me, M)
    me.materials.append(mats["skin"])
    body = bpy.data.objects.new("D_Body", me)
    link(body)
    cr.objs.append(body)
    # jaw
    prims = [xform_prim(p, M[p["bone"]]) for p in drake_jaw_prims()]
    v, f = sdf_mesh(prims, h * 0.8)
    v = taubin(v, f, 5)
    if signed_volume(v, f) < 0:
        f = f[:, ::-1]
    me = mesh_from_np("D_Jaw", v, f)
    nrm = vnormals(me)
    vv = vcoords(me)
    Minv = M["jaw"].inverted()
    rest = np.array([Minv @ Vector(p) for p in vv], np.float32)
    set_point_attr(me, "belly", np.clip((-(np.array([(Minv.to_3x3() @ Vector(q)) for q in nrm])[:, 2]) - 0.2) / 0.4, 0, 1))
    set_point_attr(me, "crack", np.zeros(len(vv), np.float32))
    set_point_attr(me, "dorsal", np.zeros(len(vv), np.float32))
    set_point_attr(me, "vs", 6.0 - rest[:, 1])
    me.materials.append(mats["skin"])
    jaw = bpy.data.objects.new("D_Jaw", me)
    link(jaw)
    cr.objs.append(jaw)
    # hard parts (head parts share the head scale-up)
    MS = Matrix.Translation(HEAD_PIVOT) @ Matrix.Scale(HEAD_SCALE, 4) @ Matrix.Translation(-HEAD_PIVOT)
    for ob, bone in drake_parts(mats):
        if bone in ("head", "jaw"):
            ob.data.transform(MS)
        ob.matrix_world = M[bone]
        cr.objs.append(ob)
    for ob, bone in plates_cache(M):
        cr.objs.append(ob)
    for side, bone in ((1, "wing_L"), (-1, "wing_R")):
        for ob in build_wing(side, wing_spread, mats, f"D_Wing{'L' if side > 0 else 'R'}"):
            ob.matrix_world = M[bone]
            cr.objs.append(ob)
    log(f"drake pose built in {time.time() - t0:.1f}s, body verts {len(body.data.vertices)}")
    return cr


def make_plate_cache(mats, rig, h=0.04):
    """Build plates once on the rest body; return a function that instantiates them for a pose."""
    prims = drake_body_prims()
    v, f = sdf_mesh(prims, h)
    v = taubin(v, f, 6)
    if signed_volume(v, f) < 0:
        f = f[:, ::-1]
    me = mesh_from_np("D_RestBody", v, f)
    tmp = bpy.data.objects.new("D_RestBody", me)
    link(tmp)
    plates = place_plates(tmp, mats, rig)
    bpy.data.objects.remove(tmp, do_unlink=True)
    for ob, _ in plates:
        ob.hide_render = True
        ob.hide_viewport = True

    def inst(M):
        out = []
        for ob, bone in plates:
            d = ob.copy()
            d.data = ob.data
            d.hide_render = False
            d.hide_viewport = False
            link(d)
            d.matrix_world = M[bone]
            out.append((d, bone))
        return out

    return inst, plates


# ============================================================ poses
# Sign convention (rotations about world X at rest, creature faces +Y):
#   +X rotation lifts anything pointing forward (head/neck up), lowers anything pointing back (tail down);
#   jaw opens with a NEGATIVE X rotation; tail rises with a NEGATIVE X rotation.
DRAKE_POSES = {
    # v2: idle keeps the jaw a little open so the overbite fangs and the glowing throat read
    "idle": dict(pose={"neck": (-4, 0, 0), "head": (2, 0, 0), "jaw": (-7, 0, 0), "tail1": (-4, 0, 0)}, spread=0.1),
    "alert": dict(pose={"neck": (8, 0, 0), "head": (4, 0, 0), "jaw": (-12, 0, 0), "tail1": (-12, 0, 0), "tail2": (-8, 0, 0),
                        "wing_L": (0, -14, 0), "wing_R": (0, 14, 0)}, spread=0.45),
    "roar": dict(pose={"chest": (6, 0, 0), "neck": (16, 0, 0), "head": (12, 0, 0), "jaw": (-40, 0, 0),
                       "tail1": (-12, 0, 0), "tail2": (-10, 0, 0), "tail3": (-8, 0, 0),
                       "wing_L": (0, -30, 0), "wing_R": (0, 30, 0)}, spread=1.0),
    "breath": dict(pose={"chest": (-4, 0, 0), "neck": (-6, 0, 0), "head": (-2, 0, 0), "jaw": (-34, 0, 0),
                         "tail1": (-6, 0, 0), "tail2": (-8, 0, 0), "wing_L": (0, -8, 0), "wing_R": (0, 8, 0)}, spread=0.6),
    # hero: low, head thrust forward, jaws wide, wings raised like a cape
    "menace": dict(pose={"chest": (-5, 0, 0), "neck": (-3, 0, 0), "head": (6, 0, 0), "jaw": (-38, 0, 0),
                         "tail1": (-14, 0, 0), "tail2": (-10, 0, 0), "tail3": (-6, 0, 0),
                         "wing_L": (0, -36, 0), "wing_R": (0, 36, 0)}, spread=1.0),
}


def clear_creature():
    for ob in list(bpy.data.objects):
        if ob.type == "MESH" and (ob.name.startswith("D_") or ob.name.startswith("G_") or ob.name.startswith("W_")):
            bpy.data.objects.remove(ob, do_unlink=True)


def render_drake(sets):
    reset()
    setup_render()
    mats = drake_materials()
    rig = drake_rig()
    plate_inst, plate_src = make_plate_cache(mats, rig)
    cam = camera()

    def build(name):
        clear_creature_keep = None
        for ob in list(bpy.context.scene.objects):
            if ob.type == "MESH" and ob.name.startswith("D_") and ob not in [p for p, _ in plate_src]:
                bpy.data.objects.remove(ob, do_unlink=True)
        spec = DRAKE_POSES[name]
        return build_drake_pose(spec["pose"], mats, rig, plate_inst, wing_spread=spec["spread"])

    def lights_for(objs, scale=1.0, **kw):
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT":
                bpy.data.objects.remove(ob, do_unlink=True)
        mn, mx = world_bbox(objs)
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        studio_lights(c, R, scale=scale, **kw)
        return mn, mx

    if "ortho" in sets or "scale" in sets or "vfx" in sets:
        cr = build("idle")
        mn, mx = lights_for(cr.objs)
        catcher = shadow_catcher()
        ppu = 90
        H = 7.3
        hpx = int(H * ppu)
        cz = H / 2 - 0.12
        cxy = (mn + mx) / 2
        if "ortho" in sets:
            ortho_view(cam, "side", (0, cxy.y, cz), ppu, int((mx.y - mn.y + 0.8) * ppu), hpx)
            render_to(os.path.join(REN, "drake_side.png"), int((mx.y - mn.y + 0.8) * ppu), hpx)
            wfront = int((mx.x - mn.x + 0.8) * ppu)
            ortho_view(cam, "front", (0, 0, cz), ppu, wfront, hpx)
            render_to(os.path.join(REN, "drake_front.png"), wfront, hpx)
            ortho_view(cam, "back", (0, 0, cz), ppu, wfront, hpx)
            render_to(os.path.join(REN, "drake_back.png"), wfront, hpx)
        bpy.data.objects.remove(catcher, do_unlink=True)
        json.dump({"ppu": ppu, "H": H, "bbox_min": list(mn), "bbox_max": list(mx)},
                  open(os.path.join(REN, "drake_ortho.json"), "w"), indent=1)

    if "hero" in sets:
        cr = build("menace")
        mn, mx = lights_for(cr.objs, scale=1.15, warm="#ffe2c0", rim2="#ff8a3a", rim1="#bcd4ff")
        catcher = shadow_catcher()
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        W_, H_ = 872, 1192
        lens = 35.0
        half = math.atan(18.0 * min(W_, H_) / max(W_, H_) / lens)
        dirv = Vector((0.55, 0.83, 0.04)).normalized()
        dist = R / math.sin(half) * 0.6
        persp_view(cam, c + dirv * dist, c + Vector((0, 0.9, -0.4)), lens=lens)
        render_to(os.path.join(REN, f"drake_hero{SUFFIX}.png"), W_, H_)
        bpy.data.objects.remove(catcher, do_unlink=True)

    if "poses" in sets:
        cr = build("roar")
        mnR, mxR = lights_for(cr.objs)
        c = (mnR + mxR) / 2
        R = (mxR - mnR).length / 2
        W_, H_ = 640, 500
        lens = 45.0
        half = math.atan(18.0 * min(W_, H_) / max(W_, H_) / lens)
        dirv = Vector((0.78, 0.6, 0.2)).normalized()
        camloc = c + dirv * (R / math.sin(half) * 0.74)
        target = c + Vector((0, 0.5, -0.35))
        for nm in ("idle", "alert", "roar", "breath"):
            cr = build(nm)
            catcher = shadow_catcher()
            extra = []
            if nm == "breath":
                M = rig.mats(DRAKE_POSES[nm]["pose"])
                mouth = M["head"] @ (HEAD_PIVOT + (Vector((0, 4.75, 4.62)) - HEAD_PIVOT) * HEAD_SCALE)
                d = (M["head"].to_3x3() @ Vector((0, 1, -0.32))).normalized()
                extra = breath_cone(mouth, d, mats)
            persp_view(cam, camloc, target, lens)
            render_to(os.path.join(REN, f"drake_pose_{nm}.png"), W_, H_, samples=110)
            for ob in extra + [catcher]:
                bpy.data.objects.remove(ob, do_unlink=True)

    if "parts" in sets:
        cr = build("idle")
        lights_for(cr.objs)
        byname = {ob.name: ob for ob in cr.objs}
        W_, H_ = 480, 380

        def shot(path, target, offset, lens=50.0):
            persp_view(cam, Vector(target) + Vector(offset), target, lens)
            render_to(os.path.join(REN, path), W_, H_, samples=110)

        hs = HEAD_SCALE
        shot("drake_part_head.png", Vector((0, 3.75, 5.05)), Vector((3.6, 4.6, 1.3)))
        shot("drake_part_tail.png", Vector((0, -4.75, 1.9)), Vector((5.2, 2.2, 1.2)))
        shot("drake_part_feet.png", Vector((1.1, 1.75, 0.35)), Vector((2.4, 2.8, 0.9)))
        shot("drake_part_belly.png", Vector((0, 1.7, 2.6)), Vector((2.8, 6.0, -0.4)))
        # isolated pieces
        hide_all_but([byname["D_HornL"]])
        bb0, bb1 = world_bbox([byname["D_HornL"]])
        cc = (bb0 + bb1) / 2
        shot("drake_part_horn.png", cc, Vector((3.4, 1.6, 0.6)) * ((bb1 - bb0).length / 2.6))
        plates = [ob for ob in cr.objs if ob.name.startswith("D_Plate")]
        plates.sort(key=lambda o: -world_bbox([o], True)[0].y)
        pick = plates[5:8]
        hide_all_but(pick)
        bb0, bb1 = world_bbox(pick, True)
        cc = (bb0 + bb1) / 2
        shot("drake_part_plates.png", cc, Vector((3.2, 1.2, 0.8)) * ((bb1 - bb0).length / 2.2))
        for ob in bpy.context.scene.objects:
            if ob.type == "MESH":
                ob.hide_render = True
        wing = build_wing(1, 0.8, mats, "D_WingShow")
        bb0, bb1 = world_bbox(wing)
        cc = (bb0 + bb1) / 2
        shot("drake_part_wing.png", cc, Vector((3.2, 1.6, 0.8)) * ((bb1 - bb0).length / 2.4))
        for ob in wing:
            bpy.data.objects.remove(ob, do_unlink=True)
        # glow parts: the creature in low light so the emissive cracks / eyes / tail flame read
        for ob in bpy.context.scene.objects:
            if ob.type == "MESH" and not ob.name.startswith("D_Plate") or ob in cr.objs:
                ob.hide_render = False
        for ob in [p for p, _ in plate_src]:
            ob.hide_render = True
        for ob in bpy.context.scene.objects:
            if ob.type == "LIGHT":
                ob.data.energy *= 0.12
        bpy.context.scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.08
        shot("drake_part_glow.png", Vector((0, 0.9, 3.4)), Vector((6.8, 4.5, 1.6)), lens=40)
        bpy.context.scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55

    if "mats" in sets:
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT":
                bpy.data.objects.remove(ob, do_unlink=True)
            elif ob.type == "MESH":
                ob.hide_render = True
        studio_lights(Vector((0, 0, 0)), 1.6)
        specs = [("skin", mats["skin"], {"belly": 0, "crack": 0}), ("belly", mats["skin"], {"belly": 1, "crack": 0, "vs": "z"}),
                 ("lava", mats["skin"], {"belly": 0, "crack": 1}), ("plate", mats["plate"], {"ph": "z01"}),
                 ("horn", mats["horn"], {"t": "z01"}), ("membrane", mats["membrane"], {"edge": "z01", "bonefac": 0}),
                 ("claw", mats["claw"], {}), ("eye", mats["eye"], {})]
        persp_view(cam, Vector((0, 3.6, 0.7)), Vector((0, 0, 0)), lens=50)
        for nm, mat, at in specs:
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=1.0)
            zs = [v.co.z for v in bm.verts]
            attrs = {}
            for k_, val in at.items():
                if val == "z":
                    attrs[k_] = [z_ * 1.0 for z_ in zs]
                elif val == "z01":
                    attrs[k_] = [(z_ + 1) / 2 for z_ in zs]
                else:
                    attrs[k_] = [float(val)] * len(zs)
            for k_ in ("belly", "crack", "vs", "t", "ph", "edge", "bonefac"):
                attrs.setdefault(k_, [0.0] * len(zs))
            ob = bm_to_obj(bm, f"MatBall_{nm}", mat, attrs)
            render_to(os.path.join(REN, f"drake_mat_{nm}.png"), 220, 220, samples=96)
            bpy.data.objects.remove(ob, do_unlink=True)

    if "scale" in sets:
        cr = build("idle")
        mn, mx = world_bbox(cr.objs)
        av = build_avatar(Vector((0, mx.y + 1.9, 0)))
        lights_for(cr.objs + av)
        catcher = shadow_catcher()
        ppu = 60
        y0, y1 = mn.y - 0.4, mx.y + 3.4
        W_ = int((y1 - y0) * ppu)
        H_ = int(7.4 * ppu)
        ortho_view(cam, "side", (0, (y0 + y1) / 2, 7.4 / 2 - 0.15), ppu, W_, H_)
        render_to(os.path.join(REN, "drake_scale.png"), W_, H_, samples=110)
        json.dump({"ppu": ppu, "y0": y0, "y1": y1, "avatar_y": mx.y + 1.9, "H": 7.4},
                  open(os.path.join(REN, "drake_scale.json"), "w"), indent=1)
        for ob in av + [catcher]:
            bpy.data.objects.remove(ob, do_unlink=True)

    if "vfx" in sets:
        cr = build("idle")
        mn, mx = lights_for(cr.objs)
        catcher = shadow_catcher()
        info = json.load(open(os.path.join(REN, "drake_ortho.json")))
        ppu, H = info["ppu"], info["H"]
        M = rig.mats({})
        fx = []
        rng = random.Random(7)
        hp = lambda p: HEAD_PIVOT + (Vector(p) - HEAD_PIVOT) * HEAD_SCALE
        nos = hp((0.25, 4.95, 5.05))
        for i, (dy, dz, s_, a_) in enumerate(((0.25, 0.25, 0.7, 0.75), (0.5, 0.75, 1.05, 0.5), (0.65, 1.35, 1.4, 0.3))):
            fx.append(billboard("VFX_smoke_puff.png", nos + Vector((1.2, dy, dz)), s_, s_, "#d9d0cf", 0.9, alpha=a_, name=f"FX_Smoke{i}"))
        for i in range(18):
            p = Vector((1.6, rng.uniform(-1.6, 1.7), rng.uniform(3.6, 5.6)))
            s_ = rng.uniform(0.16, 0.32)
            fx.append(billboard("VFX_spark_dot.png", p, s_, s_, "#ffb040", 6.0, name=f"FX_Ember{i}"))
        tip = Vector((0, -5.2, 2.6))
        fx.append(billboard("VFX_fire_flip4x4.png", tip + Vector((1.4, 0.05, 0.55)), 1.0, 1.7, "#ff5a10", 2.2, cell=(0, 0), name="FX_Fire0"))
        fx.append(billboard("VFX_fire_flip4x4.png", tip + Vector((1.45, -0.12, 0.42)), 0.7, 1.2, "#ffa030", 2.6, cell=(1, 0), name="FX_Fire1"))
        cam_w = int((mx.y - mn.y + 0.8) * ppu)
        ortho_view(cam, "side", (0, (mn.y + mx.y) / 2, H / 2 - 0.12), ppu, cam_w, int(H * ppu))
        render_to(os.path.join(REN, "drake_vfx.png"), cam_w, int(H * ppu), samples=110)
        for ob in fx + [catcher]:
            bpy.data.objects.remove(ob, do_unlink=True)

    if "habitat" in sets:
        cr = build("idle")
        hab = habitat_volcanic()
        ledge = [o for o in hab if o.name == "HAB_Rock0"][0]
        top = world_bbox([ledge])[1].z
        for ob in cr.objs:
            ob.matrix_world = Matrix.Translation((-6.3, 3.0, top - 0.35)) @ Matrix.Rotation(math.radians(52), 4, "Z") @ ob.matrix_world
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT" and not ob.name.startswith("Hab"):
                bpy.data.objects.remove(ob, do_unlink=True)
        light("HabKey", "AREA", (-30, 30, 30), (-6, 3, 3), 4200, "#ffd7b0", size=12)
        light("HabRim", "AREA", (0, -40, 18), (-6, 3, 4), 9000, "#ff7a30", size=10)
        persp_view(cam, Vector((1.5, 24.0, 6.0)), Vector((-4.0, -6.0, 4.4)), lens=26)
        render_to(os.path.join(REN, "drake_habitat.png"), 1320, 504, samples=160)
        for ob in hab:
            bpy.data.objects.remove(ob, do_unlink=True)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FantasyCreatures_drake.blend"))


VFX_DIR = os.path.normpath(os.path.join(OUT, "..", "VFX", "TexturePack"))


def billboard(tex, loc, w, h, tint, strength, alpha=1.0, cell=None, name="FX", facing=Vector((1, 0, 0)), rot=0.0):
    """Camera-facing card textured with one of Holden's VFX pack PNGs (white-on-alpha sprites); rot = roll in radians."""
    key = f"FXM_{tex}_{tint}_{strength}_{alpha}_{cell}"
    m = bpy.data.materials.get(key)
    if m is None:
        m, t = new_mat(key)
        out = t.n.get("Material Output")
        bs = t.n.get("Principled BSDF")
        if bs:
            t.n.remove(bs)
        img = bpy.data.images.load(tex if os.path.isabs(tex) else os.path.join(VFX_DIR, tex), check_existing=True)
        it = t.node("ShaderNodeTexImage")
        it.image = img
        uv = t.node("ShaderNodeTexCoord")
        if cell is not None:
            mp = t.node("ShaderNodeMapping")
            mp.inputs["Scale"].default_value = (0.25, 0.25, 1.0)
            mp.inputs["Location"].default_value = (cell[0] * 0.25, 0.75 - cell[1] * 0.25, 0.0)
            t.link(uv.outputs["UV"], mp.inputs["Vector"])
            t.link(mp.outputs["Vector"], it.inputs["Vector"])
        else:
            t.link(uv.outputs["UV"], it.inputs["Vector"])
        em = t.node("ShaderNodeEmission")
        tintc = t.mix(1.0, it.outputs["Color"], hexcol(tint), blend="MULTIPLY")
        t.link(tintc, em.inputs["Color"])
        em.inputs["Strength"].default_value = strength
        tr = t.node("ShaderNodeBsdfTransparent")
        a = t.math("MULTIPLY", it.outputs["Alpha"], alpha)
        mx = t.node("ShaderNodeMixShader")
        t.link(a, mx.inputs[0])
        t.link(tr.outputs[0], mx.inputs[1])
        t.link(em.outputs[0], mx.inputs[2])
        t.link(mx.outputs[0], out.inputs["Surface"])
    me = bpy.data.meshes.new(name)
    f_, u_, s_ = basis_from(-facing, Vector((0, 0, 1)))
    if rot:
        s_, u_ = s_ * math.cos(rot) + u_ * math.sin(rot), -s_ * math.sin(rot) + u_ * math.cos(rot)
    hw, hh = w / 2, h / 2
    vs = [loc - s_ * hw - u_ * hh, loc + s_ * hw - u_ * hh, loc + s_ * hw + u_ * hh, loc - s_ * hw + u_ * hh]
    me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for i, uvv in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
        uvl.data[i].uv = uvv
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    ob.visible_shadow = False
    link(ob)
    return ob


def rock_hull(name, center, size, seed, mat, squash=1.0, n=26, rot=None):
    rng = random.Random(seed)
    R = Euler([math.radians(a) for a in rot], "XYZ").to_matrix() if rot else None
    pts = []
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi)
        z = rng.uniform(-1, 1)
        r = math.sqrt(max(0.0, 1 - z * z))
        d = Vector((r * math.cos(a), r * math.sin(a), z))
        off = Vector((d.x * size[0], d.y * size[1], d.z * size[2] * squash)) * rng.uniform(0.82, 1.0)
        if R is not None:
            off = R @ off
        pts.append(Vector(center) + off)
    return hull_obj(pts, name, mat, smooth=False)


def torus_obj(name, center, axis, R, r, mat, segs=24, tube=8, squash=(1.0, 1.0)):
    """Ring around `axis` (e.g. a bronze band clamped around a limb); squash = ellipse radii factors."""
    A = Vector(axis).normalized()
    ref = Vector((0, 0, 1)) if abs(A.z) < 0.9 else Vector((1, 0, 0))
    U = (ref - A * ref.dot(A)).normalized()
    V = A.cross(U)
    bm = bmesh.new()
    rings = []
    for i in range(segs):
        th = 2 * math.pi * i / segs
        radial = (U * math.cos(th) * squash[0] + V * math.sin(th) * squash[1])
        rdir = radial.normalized()
        ring = []
        for j in range(tube):
            ph = 2 * math.pi * j / tube
            p = Vector(center) + radial * R + (rdir * math.cos(ph) + A * math.sin(ph) * 1.6) * r
            ring.append(bm.verts.new(p))
        rings.append(ring)
    for i in range(segs):
        i2 = (i + 1) % segs
        for j in range(tube):
            j2 = (j + 1) % tube
            bm.faces.new((rings[i][j], rings[i2][j], rings[i2][j2], rings[i][j2]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm_to_obj(bm, name, mat, smooth=True)


def habitat_volcanic():
    objs = []
    basalt = new_mat("HAB_Basalt")[0]
    if basalt.node_tree.nodes.get("Principled BSDF") and not basalt.get("built"):
        t = NT(basalt)
        co = t.objco()
        nz = t.noise(co, 0.35, 4.0, 0.6)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.7, 0, 1), hexcol("#1c1418"), hexcol("#3a2a2c"))
        geo = t.node("ShaderNodeNewGeometry")
        sep = t.node("ShaderNodeSeparateXYZ")
        t.link(geo.outputs["Normal"], sep.inputs[0])
        col = t.mix(t.maprange(sep.outputs["Z"], 0.4, 0.95, 0.0, 1.0), col, hexcol("#4a3a3a"))
        t.bsdf(col, rough=0.8, spec=0.25, normal=t.bump(nz.outputs["Fac"], 0.6, 0.2))
        basalt["built"] = 1
    lava = mat_emit("HAB_Lava", "#ff5a0a", 7.0, soft=None)
    # ground
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=120, y_segments=90, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal((60, 45, 1, 1)), verts=bm.verts)
    rng = random.Random(3)
    for v in bm.verts:
        x, y = v.co.x, v.co.y
        h = 0.6 * math.sin(x * 0.21 + 1.3) * math.cos(y * 0.17) + 0.35 * math.sin(x * 0.6 + y * 0.4)
        river = abs(y + 2.0 + 3.0 * math.sin(x * 0.12))
        if river < 2.2:
            h -= (2.2 - river) * 0.7
        v.co.z = h
    ground = bm_to_obj(bm, "HAB_Ground", basalt)
    objs.append(ground)
    # lava river ribbon
    bm = bmesh.new()
    prev = None
    for i in range(121):
        x = -60 + i
        yc = -2.0 - 3.0 * math.sin(x * 0.12)
        a = bm.verts.new((x, yc - 1.5, -0.9))
        b = bm.verts.new((x, yc + 1.5, -0.9))
        if prev:
            bm.faces.new((prev[0], a, b, prev[1]))
        prev = (a, b)
    lv = bm_to_obj(bm, "HAB_LavaRiver", lava, smooth=False)
    objs.append(lv)
    # spires and ledges
    specs = [((-6.5, 3.0, 0.0), (3.4, 3.0, 2.2), 1), ((-15, -6, 0), (2.4, 2.4, 7.5), 2), ((9, -9, 0), (3.0, 2.6, 9.5), 3),
             ((16, -3, 0), (2.0, 2.0, 5.0), 4), ((-24, -14, 0), (5.0, 4.0, 11.0), 5), ((2, -22, 0), (4.0, 3.5, 6.0), 6)]
    for i, (c, s_, seed) in enumerate(specs):
        objs.append(rock_hull(f"HAB_Rock{i}", c, s_, seed, basalt))
    # distant volcano
    bm = bmesh.new()
    rings = []
    for k, (r, z) in enumerate(((26, 0), (18, 9), (8, 19), (5.5, 21.5))):
        rings.append([bm.verts.new((-6 + r * math.cos(2 * math.pi * j / 18), -60 + r * math.sin(2 * math.pi * j / 18), z + rng.uniform(-0.8, 0.8))) for j in range(18)])
    for i in range(len(rings) - 1):
        for j in range(18):
            j2 = (j + 1) % 18
            bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
    objs.append(bm_to_obj(bm, "HAB_Volcano", basalt, smooth=False))
    glow = bmesh.new()
    bmesh.ops.create_circle(glow, cap_ends=True, segments=18, radius=5.4)
    bmesh.ops.translate(glow, verts=glow.verts, vec=Vector((-6, -60, 21.2)))
    objs.append(bm_to_obj(glow, "HAB_Crater", lava, smooth=False))
    for i, x in enumerate((-30, -12, 6, 24)):
        ld = bpy.data.lights.new(f"HabLava{i}", "POINT")
        ld.energy = 2500
        ld.color = hexcol("#ff6a1a")[:3]
        ld.shadow_soft_size = 3.0
        lo = bpy.data.objects.new(f"HabLava{i}", ld)
        lo.location = (x, -2.0 - 3.0 * math.sin(x * 0.12), 1.0)
        link(lo)
        objs.append(lo)
    # sky gradient + light haze
    w = bpy.context.scene.world
    nt = w.node_tree
    for nd in list(nt.nodes):
        if nd.type not in ("OUTPUT_WORLD", "BACKGROUND"):
            nt.nodes.remove(nd)
    bg = nt.nodes.get("Background")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    els = ramp.color_ramp.elements
    els[0].position = 0.0
    els[0].color = hexcol("#ffa04a")
    els[1].position = 0.32
    els[1].color = hexcol("#24123a")
    e = els.new(0.1)
    e.color = hexcol("#c8442a")
    e = els.new(0.2)
    e.color = hexcol("#5a1e3c")
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0
    bpy.context.scene.render.film_transparent = False
    return objs


def breath_cone(mouth, d, mats):
    """Stylised fire breath: three nested emissive cones with a wobbly flame profile."""
    out = []
    f, u, s = basis_from(d, Vector((0, 0, 1)))
    for name_, mat_, sc_ in (("BreathO", mats["flame_o"], 1.0), ("BreathM", mats["flame_m"], 0.7), ("BreathC", mats["flame_c"], 0.42)):
        bm = bmesh.new()
        rings = []
        segs, steps, L = 18, 16, 4.2 * (0.85 + 0.15 * sc_)
        for i in range(steps + 1):
            t = i / steps
            r = (0.12 + 1.25 * t ** 0.8) * sc_ * (1.0 - max(0.0, t - 0.8) * 3.5)
            ring = []
            for j in range(segs):
                a = 2 * math.pi * j / segs
                wob = 1.0 + 0.22 * math.sin(a * 5 + t * 9) * t
                p = mouth + f * (t * L) + (u * math.cos(a) + s * math.sin(a)) * max(r, 0.02) * wob
                ring.append(bm.verts.new(p))
            rings.append(ring)
        for i in range(steps):
            for j in range(segs):
                j2 = (j + 1) % segs
                bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
        bm.faces.new(list(reversed(rings[0])))
        bm.faces.new(rings[-1])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        ob = bm_to_obj(bm, name_, mat_)
        ob.visible_shadow = False
        out.append(ob)
    ld = bpy.data.lights.new("BreathLight", "POINT")
    ld.energy = 900
    ld.color = hexcol("#ff8a30")[:3]
    ld.shadow_soft_size = 1.0
    lo = bpy.data.objects.new("BreathLight", ld)
    lo.location = mouth + f * 2.0
    link(lo)
    out.append(lo)
    return out


def build_avatar(base):
    """Standard blocky Roblox-style reference figure (~5.5 studs), facing +X (the side camera)."""
    grey = mat_simple("AV_Grey", "#A9B2C2", rough=0.55)
    dark = mat_simple("AV_Dark", "#6C7690", rough=0.55)
    mid = mat_simple("AV_Mid", "#8C97AD", rough=0.55)
    face = mat_simple("AV_Face", "#1b2438", rough=0.4)
    parts = []

    def box(name, c, half, mat):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.transform(bm, matrix=Matrix.Diagonal((half[0] * 2, half[1] * 2, half[2] * 2, 1.0)), verts=bm.verts)
        bmesh.ops.translate(bm, verts=bm.verts, vec=base + Vector(c))
        ob = bm_to_obj(bm, name, mat, smooth=False)
        md = ob.modifiers.new("Bevel", "BEVEL")
        md.width = 0.07
        md.segments = 3
        parts.append(ob)
        return ob

    box("AV_LegL", (0, -0.5, 1.05), (0.48, 0.47, 1.05), dark)
    box("AV_LegR", (0, 0.5, 1.05), (0.48, 0.47, 1.05), dark)
    box("AV_Torso", (0, 0, 3.15), (0.5, 1.0, 1.05), mid)
    box("AV_ArmL", (0, -1.5, 3.12), (0.48, 0.47, 1.02), grey)
    box("AV_ArmR", (0, 1.5, 3.12), (0.48, 0.47, 1.02), grey)
    h = box("AV_Head", (0, 0, 4.88), (0.6, 0.6, 0.6), grey)
    h.modifiers["Bevel"].width = 0.22
    for dy in (-0.2, 0.2):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.07)
        bmesh.ops.translate(bm, verts=bm.verts, vec=base + Vector((0.6, dy, 5.0)))
        parts.append(bm_to_obj(bm, "AV_Eye", face))
    return parts


# ============================================================ shared builders for golem / wolf
def crystal(name, base, axis, h, r, mat, seed, sides=6, embed=0.22):
    """Pointed hex crystal along axis; attribute t = 0 at the base -> 1 at the tip."""
    rng = random.Random(seed)
    A = Vector(axis).normalized()
    ref = Vector((0, 0, 1)) if abs(A.z) < 0.9 else Vector((1, 0, 0))
    U = (ref - A * ref.dot(A)).normalized()
    V = A.cross(U)
    tw = rng.uniform(0, math.pi)
    b0 = Vector(base) - A * (h * embed)
    bm = bmesh.new()
    rings, tv = [], []
    for frac, rad in ((0.0, r * 0.92), (0.7, r), (0.78, r * 0.96)):
        ring = []
        for j in range(sides):
            a = tw + 2 * math.pi * j / sides
            jit = 1.0 + rng.uniform(-0.06, 0.06)
            ring.append(bm.verts.new(b0 + A * (h * frac) + (U * math.cos(a) + V * math.sin(a)) * rad * jit))
            tv.append(frac)
        rings.append(ring)
    tip = bm.verts.new(b0 + A * h + (U * rng.uniform(-0.05, 0.05) + V * rng.uniform(-0.05, 0.05)) * r)
    tv.append(1.0)
    for i in range(len(rings) - 1):
        for j in range(sides):
            j2 = (j + 1) % sides
            bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
    for j in range(sides):
        bm.faces.new((rings[-1][j], rings[-1][(j + 1) % sides], tip))
    bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm_to_obj(bm, name, mat, {"t": tv}, smooth=False)


def boulder(name, c, s, seed, mat, n=20, bevel=0.07, rot=None):
    ob = rock_hull(name, c, s, seed, mat, n=n, rot=rot)
    md = ob.modifiers.new("Bevel", "BEVEL")
    md.width = bevel
    md.segments = 2
    md.limit_method = "ANGLE"
    md.angle_limit = math.radians(20)
    return ob


def lathe_obj(name, profile, segs, mat, center, scale=1.0, smooth=True):
    bm = bmesh.new()
    rings = []
    for r_, z_ in profile:
        if r_ < 1e-5:
            rings.append([bm.verts.new(Vector(center) + Vector((0, 0, z_ * scale)))])
            continue
        rings.append([bm.verts.new(Vector(center) + Vector((r_ * scale * math.cos(2 * math.pi * j / segs),
                                                             r_ * scale * math.sin(2 * math.pi * j / segs), z_ * scale)))
                      for j in range(segs)])
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        for j in range(segs):
            j2 = (j + 1) % segs
            if len(A) == 1 and len(B) == 1:
                continue
            if len(A) == 1:
                bm.faces.new((A[0], B[j2], B[j]))
            elif len(B) == 1:
                bm.faces.new((A[j], A[j2], B[0]))
            else:
                bm.faces.new((A[j], A[j2], B[j2], B[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm_to_obj(bm, name, mat, smooth=smooth)


def ellipsoid_obj(name, c, rad, mat, rot=(0, 0, 0), segs=(16, 10)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs[0], v_segments=segs[1], radius=1.0)
    R = Euler([math.radians(a) for a in rot], "XYZ").to_matrix().to_4x4()
    M = Matrix.Translation(Vector(c)) @ R @ Matrix.Diagonal((rad[0], rad[1], rad[2], 1.0))
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return bm_to_obj(bm, name, mat)


def vert_normals_np(v, f):
    n = np.zeros_like(v)
    fn = np.cross(v[f[:, 2]] - v[f[:, 0]], v[f[:, 3]] - v[f[:, 1]])
    for i in range(4):
        np.add.at(n, f[:, i], fn)
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)


def sdf_obj(name, prims, M, mat, h=0.045, smooth_iters=5, post=None):
    """post(v, n) -> per-vertex offsets along the normal (sculpted surface detail on the final shape)."""
    P = [xform_prim(p, M[p["bone"]]) for p in prims]
    v, f = sdf_mesh(P, h)
    v = taubin(v, f, smooth_iters)
    if signed_volume(v, f) < 0:
        f = f[:, ::-1]
    if post is not None:
        n = vert_normals_np(v, f)
        v = (v + n * post(v, n)[:, None]).astype(np.float32)
        v = taubin(v, f, 1)
    me = mesh_from_np(name, v, f)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    link(ob)
    return ob


# ============================================================ CREATURE: MOSSBACK GOLEM
def golem_materials():
    mats = {}
    m, t = new_mat("G_Stone")
    if t:
        co = t.objco()
        oi = t.node("ShaderNodeObjectInfo")
        rnd = oi.outputs["Random"]
        base = t.mix(rnd, hexcol("#56606D"), hexcol("#7E8894"))
        base = t.mix(t.math("MULTIPLY", t.maprange(rnd, 0.7, 1.0, 0.0, 1.0), 0.6), base, hexcol("#736B62"))
        nz = t.noise(co, 2.0, 4.0, 0.6)
        base = t.mix(t.maprange(nz.outputs["Fac"], 0.3, 0.7, 0, 1), t.mix(0.3, base, hexcol("#363D47")), base)
        vc = t.voronoi(co, 0.8, "DISTANCE_TO_EDGE")
        crack = t.math("MULTIPLY", t.maprange(vc.outputs["Distance"], 0.0, 0.02, 1.0, 0.0),
                       t.maprange(t.noise(co, 1.4, 1.0, 0.5).outputs["Fac"], 0.5, 0.56, 0.0, 1.0))
        base = t.mix(t.math("MULTIPLY", crack, 0.45), base, hexcol("#22272F"))
        geo = t.node("ShaderNodeNewGeometry")
        vt = t.node("ShaderNodeVectorTransform")
        vt.vector_type = "NORMAL"
        vt.convert_from = "WORLD"
        vt.convert_to = "OBJECT"
        t.link(geo.outputs["Normal"], vt.inputs["Vector"])
        sep = t.node("ShaderNodeSeparateXYZ")
        t.link(vt.outputs["Vector"], sep.inputs[0])
        # v2: power leaking from the heart - crack lines glow violet within ~3 studs of the heart crystal
        dn = t.node("ShaderNodeVectorMath")
        dn.operation = "DISTANCE"
        t.link(co, dn.inputs[0])
        dn.inputs[1].default_value = (0.0, 1.2, 6.0)
        near = t.maprange(dn.outputs["Value"], 1.3, 3.0, 1.0, 0.0)
        vc2 = t.voronoi(co, 1.7, "DISTANCE_TO_EDGE")
        leak = t.math("MULTIPLY", t.maprange(vc2.outputs["Distance"], 0.0, 0.03, 1.0, 0.0), near)
        base = t.mix(leak, base, hexcol("#140a22"))
        # v2: rune sigil (Holden's VFX_magic_circle) carved into the chest rocks around the heart (object prop "runes")
        rn = t.node("ShaderNodeAttribute")
        rn.attribute_type = "OBJECT"
        rn.attribute_name = "runes"
        sepc = t.node("ShaderNodeSeparateXYZ")
        t.link(co, sepc.inputs[0])
        uu = t.math("ADD", t.math("DIVIDE", sepc.outputs["X"], 3.0), 0.5)
        vv = t.math("ADD", t.math("DIVIDE", t.math("SUBTRACT", sepc.outputs["Z"], 5.75), 3.0), 0.5)
        cmb = t.node("ShaderNodeCombineXYZ")
        t.link(uu, cmb.inputs[0])
        t.link(vv, cmb.inputs[1])
        img = t.node("ShaderNodeTexImage")
        try:
            img.image = bpy.data.images.load(os.path.join(VFX_DIR, "VFX_magic_circle.png"), check_existing=True)
        except Exception as ex:
            log("magic circle texture missing:", ex)
        img.extension = "CLIP"
        t.link(cmb.outputs[0], img.inputs["Vector"])
        front = t.maprange(sep.outputs["Y"], 0.1, 0.35, 0.0, 1.0)
        sig = t.math("MULTIPLY", t.math("MULTIPLY", img.outputs["Alpha"], rn.outputs["Fac"]), front)
        base = t.mix(sig, base, hexcol("#1a0f2a"))
        nzm = t.noise(co, 0.85, 2.0, 0.5)
        moss = t.math("MULTIPLY", t.maprange(sep.outputs["Z"], 0.48, 0.54, 0.0, 1.0), t.maprange(nzm.outputs["Fac"], 0.34, 0.40, 0.0, 1.0))
        moss = t.math("MULTIPLY", moss, t.math("SUBTRACT", 1.0, sig))
        mfine = t.noise(co, 5.0, 3.0, 0.6)
        mossc = t.mix(t.maprange(mfine.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#3E7A26"), hexcol("#84BE44"))
        col = t.mix(moss, base, mossc)
        aof = t.maprange(t.ao(0.5), 0.0, 1.0, 0.38, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        height = t.math("ADD", t.math("SUBTRACT", t.math("MULTIPLY", nz.outputs["Fac"], 0.5), t.math("MULTIPLY", crack, 0.9)),
                        t.math("MULTIPLY", moss, t.math("MULTIPLY", mfine.outputs["Fac"], 1.2)))
        height = t.math("SUBTRACT", height, t.math("ADD", t.math("MULTIPLY", sig, 0.8), t.math("MULTIPLY", leak, 0.6)))
        estr = t.math("ADD", t.math("MULTIPLY", leak, 3.5), t.math("MULTIPLY", sig, 4.0))
        t.bsdf(col, rough=0.8, spec=0.22, normal=t.bump(height, 0.4, 0.05), emit_col=hexcol("#a35bff"), emit_str=estr)
    mats["stone"] = m
    m, t = new_mat("G_Bronze")
    if t:
        co = t.objco()
        nz = t.noise(co, 6.0, 4.0, 0.6)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#6B3E1C"), hexcol("#B07A3C"))
        patina = t.maprange(t.noise(co, 2.5, 3.0, 0.6).outputs["Fac"], 0.55, 0.65, 0.0, 1.0)
        col = t.mix(t.math("MULTIPLY", patina, 0.6), col, hexcol("#3F7F6A"))
        vd = t.voronoi(co, 7.0)
        rune = t.maprange(vd.outputs["Distance"], 0.1, 0.16, 1.0, 0.0)
        col = t.mix(rune, col, hexcol("#2a1640"))
        aof = t.maprange(t.ao(0.25), 0.0, 1.0, 0.45, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        t.bsdf(col, rough=0.38, spec=0.6, metal=0.85, normal=t.bump(nz.outputs["Fac"], 0.2, 0.02),
               emit_col=hexcol("#b070ff"), emit_str=t.math("MULTIPLY", rune, 3.0))
    mats["bronze"] = m
    m, t = new_mat("G_Vine")
    if t:
        co = t.objco()
        nz = t.noise(co, 8.0, 3.0, 0.6)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#24461C"), hexcol("#4C8232"))
        t.bsdf(col, rough=0.7, spec=0.25)
    mats["vine"] = m
    m, t = new_mat("G_Core")
    if t:
        co = t.objco()
        vc = t.voronoi(co, 1.15, "DISTANCE_TO_EDGE")
        line = t.maprange(vc.outputs["Distance"], 0.0, 0.045, 1.0, 0.0)
        core = t.maprange(vc.outputs["Distance"], 0.0, 0.015, 1.0, 0.0)
        ecol = t.mix(core, hexcol("#7a2cff"), hexcol("#c9a0ff"))
        t.bsdf(hexcol("#1d1a26"), rough=0.55, spec=0.3, emit_col=ecol, emit_str=t.math("MULTIPLY", line, 3.0))
    mats["core"] = m
    m, t = new_mat("G_Crystal")
    if t:
        tt = t.attr("t")
        col = t.ramp(tt, [(0.0, hexcol("#2E1468")), (0.55, hexcol("#7A3BE0")), (1.0, hexcol("#C8A6FF"))])
        ecol = t.ramp(tt, [(0.0, hexcol("#5a1ec8")), (1.0, hexcol("#b98cff"))])
        nd = t.bsdf(col, rough=0.12, spec=0.75, coat=0.5, emit_col=ecol, emit_str=t.math("ADD", 0.2, t.math("MULTIPLY", tt, 0.9)))
        if "Transmission Weight" in nd.inputs:
            nd.inputs["Transmission Weight"].default_value = 0.12
    mats["crystal"] = m
    mats["heart"] = mat_simple("G_Heart", "#8A44F0", rough=0.08, spec=0.9, emit="#9a50ff", estr=2.4, aodark=0.0)
    mats["eye"] = mat_emit("G_Eye", "#d9b8ff", 9.0, soft=None)
    m, t = new_mat("G_ShroomCap")
    if t:
        co = t.objco()
        vd = t.voronoi(co, 22.0)
        dots = t.maprange(vd.outputs["Distance"], 0.16, 0.22, 1.0, 0.0)
        col = t.mix(dots, hexcol("#E0452F"), hexcol("#FFF0D6"))
        t.bsdf(col, rough=0.4, spec=0.45)
    mats["cap"] = m
    mats["stem"] = mat_simple("G_ShroomStem", "#EFE3C6", rough=0.5)
    return mats


def golem_rig():
    r = Rig()
    r.add("root", None, (0, 0, 3.3))
    r.add("chest", "root", (0, 0, 4.4))
    r.add("head", "chest", (0, 0.8, 6.8))
    for s, sd in ((1, "L"), (-1, "R")):
        r.add(f"upperarm_{sd}", "chest", (2.75 * s, 0.1, 6.7))
        r.add(f"forearm_{sd}", f"upperarm_{sd}", (3.3 * s, 0.5, 4.6))
        r.add(f"fist_{sd}", f"forearm_{sd}", (3.5 * s, 1.0, 2.3))
    return r


GOLEM_ROCKS = [
    ("Pelvis", "root", (0, -0.05, 3.35), (1.85, 1.35, 1.15), 11),
    ("Belly", "chest", (0, 0.3, 4.6), (1.75, 1.3, 1.1), 12),
    ("Back", "chest", (0, -0.9, 6.5), (2.55, 1.4, 1.8), 13),
    ("LowBack", "chest", (0, -0.95, 4.75), (1.85, 1.15, 1.2), 18),
    ("Hump", "chest", (0, -0.35, 7.75), (1.7, 1.25, 0.9), 14),
    # v2: smaller head sunk low between the shoulders; jaw carries crystal tusks
    ("Head", "head", (0, 1.0, 7.1), (0.82, 0.76, 0.68), 15),
    ("Jaw", "head", (0, 1.38, 6.62), (0.7, 0.58, 0.34), 17),
]
GOLEM_ROCKS_SIDE = [  # (name, bone, centre, size, seed[, rot]) left side, mirrored for the right
    ("Brow", "head", (0.3, 1.52, 7.42), (0.52, 0.34, 0.22), 16, (0, -25, 0)),
    ("Chest", "chest", (1.08, 0.5, 6.05), (1.22, 1.22, 1.45), 21),
    ("Rib", "chest", (1.62, -0.05, 4.95), (0.95, 1.05, 1.05), 28),
    ("Shoulder", "upperarm", (2.75, 0.05, 7.3), (1.75, 1.6, 1.5), 22),
    ("UpperArm", "upperarm", (3.2, 0.35, 5.45), (1.08, 1.08, 1.35), 23),
    ("Elbow", "forearm", (3.36, 0.55, 4.55), (0.82, 0.82, 0.75), 29),
    ("Forearm", "forearm", (3.45, 0.85, 3.6), (1.38, 1.3, 1.5), 24),
    ("Fist", "fist", (3.55, 1.25, 1.18), (1.38, 1.32, 1.18), 25),
    ("Thigh", "root", (1.25, -0.05, 2.35), (1.02, 1.08, 1.1), 26),
    ("Knee", "root", (1.32, 0.35, 1.65), (0.75, 0.75, 0.62), 30),
    ("Foot", "root", (1.35, 0.25, 0.85), (1.18, 1.42, 0.95), 27),
]
GOLEM_CRYSTALS = [  # (name, bone, base, axis, h, r, seed)
    ("Back0", "chest", (0, -1.0, 8.0), (0, -0.3, 1), 2.5, 0.34, 1),
    ("Back1", "chest", (0.55, -1.2, 7.85), (0.5, -0.3, 1), 1.85, 0.28, 2),
    ("Back2", "chest", (-0.6, -1.15, 7.85), (-0.5, -0.2, 1), 2.0, 0.29, 3),
    ("Back3", "chest", (0.25, -1.65, 7.55), (0.2, -0.8, 0.8), 1.4, 0.24, 4),
    ("Back4", "chest", (-0.3, -1.75, 7.45), (-0.3, -0.9, 0.7), 1.15, 0.21, 5),
    ("Back5", "chest", (1.05, -0.9, 7.7), (0.8, -0.1, 0.9), 1.05, 0.19, 6),
    ("Back6", "chest", (-1.1, -0.8, 7.65), (-0.8, 0, 0.9), 1.1, 0.19, 7),
    ("Crown0", "head", (0, 0.85, 7.62), (0, -0.25, 1), 0.78, 0.13, 8),
]
GOLEM_CRYSTALS_SIDE = [
    ("Sh0", "upperarm", (2.85, -0.1, 8.35), (0.4, -0.2, 1), 1.75, 0.3, 11),
    ("Sh1", "upperarm", (3.3, 0.2, 8.2), (0.8, 0.2, 0.8), 1.2, 0.24, 12),
    ("Sh2", "upperarm", (2.45, -0.45, 8.25), (-0.1, -0.6, 1), 1.1, 0.22, 13),
    ("Sh3", "upperarm", (3.2, -0.5, 8.15), (0.6, -0.6, 0.7), 0.85, 0.18, 14),
    ("ShBig", "upperarm", (3.75, 0.05, 7.6), (1.0, -0.12, 0.5), 2.1, 0.36, 17),
    ("Fa0", "forearm", (3.95, 0.6, 4.55), (1, -0.2, 0.5), 0.8, 0.16, 15),
    ("Fa1", "forearm", (3.85, 1.2, 4.25), (0.9, 0.4, 0.4), 0.6, 0.13, 16),
    ("Kn0", "fist", (3.15, 2.25, 1.55), (-0.1, 1, 0.3), 0.6, 0.13, 18),
    ("Kn1", "fist", (3.55, 2.32, 1.6), (0, 1, 0.3), 0.72, 0.14, 19),
    ("Kn2", "fist", (3.95, 2.25, 1.55), (0.1, 1, 0.3), 0.6, 0.13, 20),
    ("Tusk", "head", (0.36, 1.78, 6.72), (0.25, 0.45, 1), 0.55, 0.1, 21),
    ("Crown1", "head", (0.33, 0.85, 7.52), (0.45, -0.2, 1), 0.55, 0.11, 22),
]
GOLEM_POSES = {
    "idle": {"chest": (-4, 0, 0), "head": (-6, 0, 0)},
    "roar": {"chest": (6, 0, 0), "head": (14, 0, 0), "upperarm_L": (0, -80, 0), "forearm_L": (0, -45, 0),
             "upperarm_R": (0, 80, 0), "forearm_R": (0, 45, 0)},
    "smash": {"chest": (8, 0, 0), "head": (-6, 0, 0), "upperarm_L": (150, -22, 0), "forearm_L": (-25, 0, 0),
              "upperarm_R": (150, 22, 0), "forearm_R": (-25, 0, 0)},
    "punch": {"chest": (-10, 0, 0), "head": (-4, 0, 0), "upperarm_R": (82, 0, 0), "forearm_R": (-8, 0, 0),
              "upperarm_L": (-18, 0, 0), "forearm_L": (-20, 0, 0)},
}


def golem_core_prims():
    P = [P_ell("chest", (0, -0.1, 5.4), (1.45, 0.95, 1.95), k=0.4),
         P_ell("root", (0, 0, 3.3), (1.25, 0.9, 0.85), k=0.4),
         P_cone("head", (0, 0.4, 6.5), (0, 0.95, 7.0), 0.55, 0.45, k=0.25)]
    side = [P_cone("upperarm_L", (2.55, 0.1, 6.6), (3.3, 0.5, 4.6), 0.52, 0.45, k=0.25),
            P_cone("forearm_L", (3.3, 0.5, 4.6), (3.5, 1.0, 2.3), 0.45, 0.42, k=0.2),
            P_sph("fist_L", (3.55, 1.2, 1.25), 0.6, k=0.2),
            P_cone("root", (1.1, 0, 3.0), (1.3, 0.1, 1.8), 0.48, 0.42, k=0.2),
            P_cone("root", (1.3, 0.1, 1.8), (1.35, 0.2, 0.9), 0.42, 0.4, k=0.15)]
    return P + side + mirror_x(side)


def build_golem(M, mats):
    objs = []
    objs.append(sdf_obj("G_Core", golem_core_prims(), M, mats["core"], h=0.05))

    def place(ob, bone):
        ob.matrix_world = M[bone]
        objs.append(ob)

    for nm, bone, c, s, seed in GOLEM_ROCKS:
        place(boulder(f"G_{nm}", c, s, seed, mats["stone"], n=15), bone)
    for entry in GOLEM_ROCKS_SIDE:
        nm, bone, c, s, seed = entry[:5]
        rot = entry[5] if len(entry) > 5 else None
        for sx, sd in ((1, "L"), (-1, "R")):
            b = bone + f"_{sd}" if bone not in ("root", "chest", "head") else bone
            r_ = (rot[0], rot[1] * sx, rot[2] * sx) if rot else None
            place(boulder(f"G_{nm}{sd}", (c[0] * sx, c[1], c[2]), s, seed + (0 if sx > 0 else 100), mats["stone"], n=15, rot=r_), b)
    for ob in objs:
        if ob.name in ("G_ChestL", "G_ChestR", "G_Belly"):
            ob["runes"] = 1.0
    for nm, bone, base, axis, h, r, seed in GOLEM_CRYSTALS:
        place(crystal(f"G_Crystal{nm}", base, axis, h, r, mats["crystal"], seed), bone)
    for nm, bone, base, axis, h, r, seed in GOLEM_CRYSTALS_SIDE:
        for sx, sd in ((1, "L"), (-1, "R")):
            b = f"{bone}_{sd}" if bone not in ("root", "chest", "head") else bone
            place(crystal(f"G_Crystal{nm}{sd}", (base[0] * sx, base[1], base[2]), (axis[0] * sx, axis[1], axis[2]), h, r,
                          mats["crystal"], seed + (0 if sx > 0 else 50)), b)
    # v2: bronze rune bands clamped around forearms and upper arms, and a belt
    for sx, sd in ((1, "L"), (-1, "R")):
        el, wr, sh = Vector((3.3 * sx, 0.5, 4.6)), Vector((3.5 * sx, 1.0, 2.3)), Vector((2.75 * sx, 0.1, 6.7))
        place(torus_obj(f"G_BandFore{sd}", el + (wr - el) * 0.5, wr - el, 1.22, 0.11, mats["bronze"], squash=(1.1, 1.0)), f"forearm_{sd}")
        place(torus_obj(f"G_BandUpper{sd}", sh + (el - sh) * 0.6, el - sh, 1.0, 0.1, mats["bronze"]), f"upperarm_{sd}")
    place(torus_obj("G_Belt", Vector((0, 0.1, 3.95)), Vector((0, 0, 1)), 1.0, 0.13, mats["bronze"], segs=32, squash=(1.95, 1.42)), "root")
    # v2: floating pebbles and hanging leafy vines
    for i, (c, s_) in enumerate((((3.95, 0.6, 9.2), 0.3), ((-3.9, 0.5, 9.05), 0.28), ((2.1, 1.75, 9.45), 0.22),
                                 ((-2.0, 1.7, 9.35), 0.24), ((0.2, 2.1, 8.95), 0.2), ((4.45, -0.6, 7.3), 0.3), ((-4.4, -0.7, 7.15), 0.27))):
        place(boulder(f"G_Pebble{i}", c, (s_, s_ * 0.9, s_ * 0.8), 60 + i, mats["stone"], n=10, bevel=0.02), "chest")
    rngv = random.Random(31)
    for sx, sd in ((1, "L"), (-1, "R")):
        for k, (p0, p1, p2, bone) in enumerate((((2.0, 1.1, 7.75), (2.3, 1.75, 6.7), (2.15, 1.6, 5.55), "upperarm"),
                                                 ((3.5, -0.9, 7.4), (3.85, -1.3, 6.3), (3.7, -1.15, 5.35), "upperarm"),
                                                 ((4.2, 0.95, 4.3), (4.6, 1.1, 3.4), (4.45, 1.0, 2.6), "forearm"))):
            P0, P1, P2 = [Vector((a * sx, b, c)) for a, b, c in (p0, p1, p2)]
            pts = [P0 * (1 - u) ** 2 + P1 * 2 * u * (1 - u) + P2 * u * u for u in [i / 8 for i in range(9)]]
            place(sweep(pts, [0.06 - 0.045 * i / 8 for i in range(9)], 6, name=f"G_Vine{k}{sd}", mat=mats["vine"]), f"{bone}_{sd}")
            for li in (2, 4, 6, 7):
                q = pts[li]
                d = Vector((rngv.uniform(0.3, 1.0) * sx, rngv.uniform(-0.5, 0.8), rngv.uniform(-0.3, 0.3))).normalized()
                place(ellipsoid_obj(f"G_Leaf{k}{li}{sd}", q + d * 0.1, (0.14, 0.07, 0.02), mats["vine"],
                                    rot=(rngv.uniform(-40, 40), rngv.uniform(-40, 40), math.degrees(math.atan2(d.y, d.x))), segs=(8, 4)),
                      f"{bone}_{sd}")
    place(crystal("G_Heart", (0, 1.2, 6.0), (0, 1, 0.2), 1.0, 0.36, mats["heart"], 99, embed=0.35), "chest")
    hl = bpy.data.lights.new("G_HeartLight", "POINT")
    hl.energy = 220
    hl.color = hexcol("#b878ff")[:3]
    hl.shadow_soft_size = 0.6
    ho = bpy.data.objects.new("G_HeartLight", hl)
    ho.location = M["chest"] @ Vector((0, 2.0, 6.1))
    link(ho)
    for sx in (1, -1):
        # angry slit eyes: inner ends lower (matches the V brow)
        place(ellipsoid_obj(f"G_Eye{sx}", (0.3 * sx, 1.72, 7.2), (0.15, 0.05, 0.055), mats["eye"], rot=(0, -20 * sx, -10 * sx)), "head")
    for i, (c, sc, bone) in enumerate((((2.2, 0.45, 8.55), 0.4, "upperarm_L"), ((2.62, 0.75, 8.47), 0.28, "upperarm_L"),
                                       ((-2.35, 0.55, 8.55), 0.34, "upperarm_R"), ((1.6, 0.75, 1.68), 0.26, "root"),
                                       ((0.8, 0.0, 8.45), 0.3, "chest"))):
        stem = lathe_obj(f"G_ShroomStem{i}", [(0, 0), (0.18, 0), (0.15, 0.5), (0.13, 0.85), (0, 0.85)], 10, mats["stem"], c, sc)
        cap = lathe_obj(f"G_ShroomCap{i}", [(0, 0.7), (0.62, 0.66), (0.6, 0.8), (0.42, 1.08), (0.0, 1.2)], 16, mats["cap"], c, sc)
        place(stem, bone)
        place(cap, bone)
    return objs


class GolemSpec:
    key = "golem"
    prefix = "G_"
    poses = GOLEM_POSES
    pose_names = ["idle", "roar", "smash", "punch"]
    hero_pose = "smash"
    hero_dir = Vector((-0.5, 0.86, -0.02))
    hero_lens = 35.0
    hero_fit = 0.66
    hero_light = dict(warm="#fff0dc", rim1="#d6c2ff", rim2="#9be37a", fill="#8fb0ff")
    pose_dir = Vector((0.62, 0.76, 0.16))
    pose_fit = 0.5
    ppu, H = 60, 11.0

    def setup(self):
        self.mats = golem_materials()
        self.rig = golem_rig()

    def build(self, name):
        return build_golem(self.rig.mats(self.poses[name]), self.mats)

    def pose_extra(self, name, objs):
        return []

    def parts(self, shot, objs, hide_all_but, iso_shot):
        shot("golem_part_head.png", Vector((0, 1.5, 7.1)), Vector((1.9, 3.3, 0.5)))
        iso_shot("golem_part_crystals.png", [o for o in objs if o.name.startswith("G_CrystalBack")], Vector((2.6, -1.6, 1.2)))
        iso_shot("golem_part_shoulder.png", [o for o in objs if o.name in ("G_ShoulderL", "G_CrystalSh0L", "G_CrystalSh1L", "G_CrystalSh2L",
                                                                            "G_CrystalSh3L", "G_CrystalShBigL", "G_ShroomStem0", "G_ShroomCap0",
                                                                            "G_ShroomStem1", "G_ShroomCap1")], Vector((2.4, 2.4, 1.4)))
        shot("golem_part_fist.png", Vector((3.6, 1.9, 1.35)), Vector((2.6, 3.4, 1.0)))
        shot("golem_part_heart.png", Vector((0, 1.5, 5.9)), Vector((0.9, 4.2, 0.4)))
        shot("golem_part_core.png", Vector((3.42, 0.72, 3.45)), Vector((2.9, 2.6, 0.7)))
        shot("golem_part_moss.png", Vector((2.45, 0.55, 8.5)), Vector((1.3, 2.2, 1.1)))

    def balls(self):
        m = self.mats
        return [("stone", m["stone"], {}, True), ("moss", m["stone"], {}, False), ("crystal", m["crystal"], {"t": "z01"}, False),
                ("heart", m["heart"], {}, False), ("core", m["core"], {}, False), ("cap", m["cap"], {}, False),
                ("stem", m["stem"], {}, False), ("eye", m["eye"], {}, False)]

    vfx_view = "front"

    def vfx(self, objs, M):
        fx = []
        rng = random.Random(5)
        F = Vector((0, 1, 0))
        for i, nm in enumerate(("G_CrystalBack0", "G_CrystalBack1", "G_CrystalSh0L", "G_CrystalSh0R", "G_CrystalBack2")):
            ob = [o for o in objs if o.name == nm][0]
            tip = max((ob.matrix_world @ v.co for v in ob.data.vertices), key=lambda p: p.z)
            fx.append(billboard("VFX_spark_dot.png", tip + Vector((0, 3.2, 0.05)), 0.6, 0.6, "#efe0ff", 7.0, name=f"FX_Glint{i}", facing=F))
        fx.append(billboard("VFX_flare.png", M["chest"] @ Vector((0, 2.4, 6.05)), 2.2, 2.2, "#b878ff", 2.2, name="FX_Heart", facing=F))
        for i, (x, z, s_) in enumerate(((1.4, 0.4, 1.5), (-1.3, 0.35, 1.3), (3.6, 0.45, 1.1), (-3.5, 0.4, 1.2))):
            fx.append(billboard("VFX_smoke_puff.png", Vector((x, 2.6, z)), s_ * 1.5, s_, "#c9b79c", 1.0, alpha=0.75, name=f"FX_Dust{i}", facing=F))
        for i in range(12):
            p = Vector((rng.choice((-1, 1)) * rng.uniform(1.6, 3.8), 3.0, rng.uniform(6.8, 9.6)))
            s_ = rng.uniform(0.14, 0.28)
            fx.append(billboard("VFX_spark_dot.png", p, s_, s_, "#a8f070", 5.0, name=f"FX_Spore{i}", facing=F))
        fx.append(billboard("VFX_shockwave_ring.png", Vector((-3.55, 3.2, 0.25)), 3.6, 1.0, "#d9c2ff", 2.5, alpha=0.9, name="FX_Shock", facing=F))
        return fx

    def habitat(self, objs, cam):
        return habitat_ruins(objs, cam)


def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return new


ASSET_LIB = r"C:\Users\holde\Documents\GameDev\AssetLibrary"


def habitat_ruins(creature_objs, cam):
    """Elderwood Ruins: grassy clearing, broken pillars, Holden's own low-poly trees."""
    objs = []
    grass = new_mat("HAB_Grass")[0]
    if not grass.get("built"):
        t = NT(grass)
        co = t.objco()
        nz = t.noise(co, 0.12, 3.0, 0.55)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#4E9A34"), hexcol("#7CC24A"))
        t.bsdf(col, rough=0.85, spec=0.2)
        grass["built"] = 1
    ruin = new_mat("HAB_RuinStone")[0]
    if not ruin.get("built"):
        t = NT(ruin)
        co = t.objco()
        nz = t.noise(co, 1.2, 4.0, 0.6)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.3, 0.7, 0, 1), hexcol("#8E8A80"), hexcol("#B8B2A4"))
        geo = t.node("ShaderNodeNewGeometry")
        sep = t.node("ShaderNodeSeparateXYZ")
        t.link(geo.outputs["Normal"], sep.inputs[0])
        col = t.mix(t.math("MULTIPLY", t.maprange(sep.outputs["Z"], 0.55, 0.6, 0, 1), t.maprange(nz.outputs["Fac"], 0.4, 0.45, 0, 1)), col, hexcol("#6FAE3C"))
        t.bsdf(col, rough=0.8, spec=0.2, normal=t.bump(nz.outputs["Fac"], 0.4, 0.1))
        ruin["built"] = 1
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=80, y_segments=80, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal((70, 70, 1, 1)), verts=bm.verts)
    for v in bm.verts:
        x, y = v.co.x, v.co.y
        v.co.z = 0.35 * math.sin(x * 0.18) * math.cos(y * 0.15) + 0.2 * math.sin(x * 0.5 + y * 0.31) - (0.0 if abs(x) < 9 and abs(y) < 9 else 0.0)
    ground = bm_to_obj(bm, "HAB_Ground", grass)
    objs.append(ground)
    rng = random.Random(9)
    pillars = [(-11, -6, 7.5, 0.0), (9, -9, 5.5, 12.0), (14, -2, 9.0, -6.0), (-16, -14, 6.5, 4.0), (4, -18, 10.0, 0.0)]
    for i, (x, y, hgt, tilt) in enumerate(pillars):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=1.15, radius2=1.0, depth=hgt)
        for v in bm.verts:
            if v.co.z > hgt / 2 - 0.01:
                v.co.z += rng.uniform(-1.4, 0.0)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, hgt / 2)))
        ob = bm_to_obj(bm, f"HAB_Pillar{i}", ruin, smooth=False)
        ob.matrix_world = Matrix.Translation((x, y, -0.1)) @ Matrix.Rotation(math.radians(tilt), 4, "X")
        md = ob.modifiers.new("Bevel", "BEVEL")
        md.width = 0.08
        md.segments = 2
        objs.append(ob)
    for i in range(7):
        objs.append(boulder(f"HAB_Block{i}", (rng.uniform(-18, 18), rng.uniform(-16, -2), 0.4), (rng.uniform(0.8, 1.6), rng.uniform(0.8, 1.6), rng.uniform(0.5, 1.0)),
                            40 + i, ruin))
    tree_files = [os.path.join(ASSET_LIB, "models", "trees", f"Tree_Green_{k}.glb") for k in (1, 2, 3, 4, 5)]
    spots = [(-20, -10, 0.0, 4.2), (-7, -22, 1.0, 5.0), (12, -20, 2.0, 4.6), (22, -9, 3.0, 4.0), (-28, -24, 4.0, 5.2), (26, -26, 1.0, 4.8)]
    for i, (x, y, rot, sc) in enumerate(spots):
        path = tree_files[i % len(tree_files)]
        if not os.path.exists(path):
            continue
        new = import_glb(path)
        roots = [o for o in new if o.parent is None]
        for o in roots:
            o.matrix_world = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(rot, 4, "Z") @ Matrix.Scale(sc, 4) @ o.matrix_world
        objs.extend(new)
    w = bpy.context.scene.world
    nt = w.node_tree
    for nd in list(nt.nodes):
        if nd.type not in ("OUTPUT_WORLD", "BACKGROUND"):
            nt.nodes.remove(nd)
    bg = nt.nodes.get("Background")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    els = ramp.color_ramp.elements
    els[0].position = 0.0
    els[0].color = hexcol("#fff0c8")
    els[1].position = 0.35
    els[1].color = hexcol("#5aa8e8")
    bg.inputs["Strength"].default_value = 1.2
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bpy.context.scene.render.film_transparent = False
    for ob in creature_objs:
        ob.matrix_world = Matrix.Translation((-1.0, -2.0, 0.0)) @ Matrix.Rotation(math.radians(-28), 4, "Z") @ ob.matrix_world
    for ob in list(bpy.context.scene.objects):
        if ob.type == "LIGHT" and not ob.name.startswith("G_"):
            bpy.data.objects.remove(ob, do_unlink=True)
    objs.append(light("HabSun", "SUN", (30, 20, 40), (0, 0, 0), 4.5, "#fff1d6"))
    objs[-1].data.angle = math.radians(4)
    objs.append(light("HabFill", "AREA", (-20, 25, 12), (-1, -2, 5), 2500, "#a8c8ff", size=14))
    persp_view(cam, Vector((7.0, 26.0, 6.5)), Vector((-1.5, -6.0, 5.0)), lens=26)
    return objs


# ============================================================ CREATURE: FROSTFANG WOLF
def wolf_materials():
    mats = {}
    m, t = new_mat("W_Fur")
    if t:
        co = t.objco()
        sad = t.maprange(t.attr("saddle"), 0.44, 0.56, 0.0, 1.0)
        nz = t.noise(co, 1.6, 3.0, 0.55)
        base = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.68, 0, 1), hexcol("#C9D7E7"), hexcol("#EAF1F9"))
        geo = t.node("ShaderNodeNewGeometry")
        sepn = t.node("ShaderNodeSeparateXYZ")
        t.link(geo.outputs["Normal"], sepn.inputs[0])
        under = t.maprange(sepn.outputs["Z"], -0.1, -0.8, 0.0, 1.0)
        base = t.mix(t.math("MULTIPLY", under, 0.7), base, hexcol("#94A9C6"))
        sadc = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.68, 0, 1), hexcol("#28375A"), hexcol("#435A82"))
        col = t.mix(sad, base, sadc)
        clump = t.voronoi(co, 9.0)
        cl = t.maprange(clump.outputs["Distance"], 0.3, 0.62, 0.0, 1.0)
        col = t.mix(t.math("MULTIPLY", cl, 0.08), col, hexcol("#6F86A8"))
        strand = t.noise(t.mix(1.0, co, (1.0, 1.0, 0.25, 1.0), blend="MULTIPLY"), 42.0, 6.0, 0.7)
        aof = t.maprange(t.ao(0.35), 0.0, 1.0, 0.45, 1.0)
        col = t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        height = t.math("ADD", t.math("MULTIPLY", strand.outputs["Fac"], 0.8), t.math("MULTIPLY", t.math("SUBTRACT", 1.0, cl), 0.6))
        nd = t.bsdf(col, rough=0.72, spec=0.25, normal=t.bump(height, 0.32, 0.02))
        if "Sheen Weight" in nd.inputs:
            nd.inputs["Sheen Weight"].default_value = 0.4
    mats["fur"] = m
    m, t = new_mat("W_Ice")
    if t:
        tt = t.attr("t")
        col = t.ramp(tt, [(0.0, hexcol("#145A9E")), (0.55, hexcol("#55C4F5")), (1.0, hexcol("#E2F8FF"))])
        ecol = t.ramp(tt, [(0.0, hexcol("#1d7ad0")), (1.0, hexcol("#a8ecff"))])
        nd = t.bsdf(col, rough=0.08, spec=0.8, coat=0.6, emit_col=ecol, emit_str=t.math("ADD", 0.15, t.math("MULTIPLY", tt, 0.9)))
        if "Transmission Weight" in nd.inputs:
            nd.inputs["Transmission Weight"].default_value = 0.15
    mats["ice"] = m
    mats["eye"] = mat_emit("W_Eye", "#9BF0FF", 8.0, soft=None)
    mats["nose"] = mat_simple("W_Nose", "#1E2129", rough=0.25, spec=0.7)
    mats["inner"] = mat_simple("W_InnerEar", "#E39AAC", rough=0.6)
    mats["teeth"] = mat_simple("W_Teeth", "#F4F0E6", rough=0.3, spec=0.6)
    mats["claw"] = mat_simple("W_Claw", "#2B2F3A", rough=0.3, spec=0.6)
    mats["mouth"] = mat_simple("W_Mouth", "#3A1218", rough=0.6)
    mats["tongue"] = mat_simple("W_Tongue", "#D85A6A", rough=0.35)
    return mats


def wolf_rig():
    r = Rig()
    r.add("root", None, (0, -1.0, 2.7))
    r.add("chest", "root", (0, 0.3, 2.8))
    r.add("neck", "chest", (0, 1.15, 3.15))
    r.add("head", "neck", (0, 2.0, 3.85))
    r.add("jaw", "head", (0, 2.55, 3.66))
    r.add("tail1", "root", (0, -2.0, 2.95))
    r.add("tail2", "tail1", (0, -2.9, 2.75))
    r.add("tail3", "tail2", (0, -3.6, 2.3))
    return r


def wolf_body_prims():
    P = [P_ell("chest", (0, 0.75, 2.78), (0.82, 1.02, 0.95), k=0.4),
         P_ell("root", (0, -0.25, 2.8), (0.7, 1.3, 0.66), k=0.4),
         P_ell("root", (0, -1.35, 2.78), (0.68, 0.82, 0.7), k=0.4),
         P_ell("root", (0, -0.1, 3.25), (0.58, 1.75, 0.34), k=0.35),
         P_cone("neck", (0, 1.2, 3.18), (0, 2.05, 3.85), 0.64, 0.48, k=0.28),
         P_ell("head", (0, 2.45, 4.0), (0.55, 0.62, 0.5), k=0.22),
         P_cone("head", (0, 2.75, 3.96), (0, 3.62, 3.78), 0.36, 0.2, k=0.2),
         P_ell("head", (0, 3.15, 4.02), (0.2, 0.55, 0.12), k=0.1),
         P_ell("head", (0.24, 2.85, 4.25), (0.2, 0.32, 0.12), (0, 0, -16), k=0.08),
         P_ell("head", (-0.24, 2.85, 4.25), (0.2, 0.32, 0.12), (0, 0, 16), k=0.08),
         P_ell("head", (0.4, 2.35, 3.78), (0.28, 0.4, 0.32), k=0.12),
         P_ell("head", (-0.4, 2.35, 3.78), (0.28, 0.4, 0.32), k=0.12),
         P_sph("head", (0.33, 2.95, 4.05), 0.1, k=0.04, mode="sub"),
         P_sph("head", (-0.33, 2.95, 4.05), 0.1, k=0.04, mode="sub"),
         P_box("head", (0, 3.2, 3.62), (0.5, 0.6, 0.05), rnd=0.03, k=0.04, mode="sub")]
    fl = [P_ell("chest", (0.55, 1.0, 2.55), (0.42, 0.58, 0.74), k=0.25),
          P_cone("chest", (0.58, 1.05, 2.2), (0.6, 0.95, 1.2), 0.36, 0.25, k=0.18),
          P_cone("chest", (0.6, 0.95, 1.2), (0.6, 1.05, 0.25), 0.25, 0.19, k=0.12),
          P_ell("chest", (0.6, 1.22, 0.15), (0.25, 0.34, 0.15), k=0.1)]
    bl = [P_ell("root", (0.58, -1.45, 2.3), (0.45, 0.7, 0.8), (-20, 0, 0), k=0.25),
          P_cone("root", (0.62, -1.15, 1.75), (0.62, -1.75, 0.95), 0.32, 0.21, k=0.15),
          P_cone("root", (0.62, -1.75, 0.95), (0.62, -1.55, 0.22), 0.2, 0.18, k=0.1),
          P_ell("root", (0.62, -1.4, 0.15), (0.25, 0.34, 0.15), k=0.1)]
    P += fl + mirror_x(fl) + bl + mirror_x(bl)
    P += [P_cone("tail1", (0, -2.05, 2.95), (0, -2.9, 2.75), 0.27, 0.38, k=0.15),
          P_cone("tail2", (0, -2.9, 2.75), (0, -3.6, 2.3), 0.38, 0.33, k=0.12),
          P_cone("tail3", (0, -3.6, 2.3), (0, -4.1, 1.78), 0.33, 0.16, k=0.1)]
    # fur tufts: chest ruff, neck mane, cheeks, elbows, hips, tail
    tufts = []
    for row, (yb, zb, sp, ln) in enumerate(((1.62, 2.98, 0.2, 0.55), (1.82, 3.32, 0.22, 0.48), (1.45, 2.62, 0.18, 0.45))):
        for i in range(-3, 4):
            x = i * sp
            base = (x, yb - 0.06 * abs(i), zb - 0.06 * abs(i))
            tip = (x * 1.35, yb + 0.22 - 0.05 * abs(i), zb - ln)
            tufts.append(P_cone("chest" if row != 1 else "neck", base, tip, 0.15, 0.02, k=0.05))
    for s in (1, -1):
        for j, (y, z) in enumerate(((1.5, 3.5), (1.25, 3.3), (1.75, 3.7))):
            tufts.append(P_cone("neck", (0.5 * s, y, z), (0.82 * s, y - 0.3, z - 0.15), 0.15, 0.02, k=0.05))
        tufts.append(P_cone("head", (0.5 * s, 2.25, 3.75), (0.8 * s, 2.0, 3.62), 0.13, 0.02, k=0.05))
        tufts.append(P_cone("head", (0.45 * s, 2.15, 3.95), (0.72 * s, 1.92, 3.95), 0.11, 0.02, k=0.05))
        tufts.append(P_cone("chest", (0.6 * s, 0.75, 1.65), (0.62 * s, 0.45, 1.48), 0.1, 0.02, k=0.04))
        tufts.append(P_cone("root", (0.64 * s, -1.95, 2.4), (0.7 * s, -2.3, 2.12), 0.13, 0.02, k=0.05))
        for k_, (y, z) in enumerate(((-2.6, 2.9), (-3.15, 2.7), (-3.6, 2.4))):
            bone = "tail1" if y > -2.9 else ("tail2" if y > -3.6 else "tail3")
            tufts.append(P_cone(bone, (0.28 * s, y, z), (0.5 * s, y - 0.32, z - 0.08), 0.14, 0.02, k=0.05))
    tufts.append(P_cone("tail3", (0, -4.0, 1.85), (0, -4.38, 1.6), 0.15, 0.02, k=0.05))
    return P + tufts


def wolf_jaw_prims():
    return [P_cone("jaw", (0, 2.5, 3.62), (0, 3.45, 3.6), 0.3, 0.16, k=0.15),
            P_box("jaw", (0, 3.0, 3.9), (0.5, 0.8, 0.22), rnd=0.03, k=0.05, mode="sub")]


WOLF_ICE = [  # (name, bone, base, axis, h, r, seed)
    ("Sp0", "chest", (0, 1.05, 3.6), (0, -0.35, 1), 0.85, 0.15, 1),
    ("Sp1", "chest", (0, 0.55, 3.56), (0, -0.4, 1), 1.05, 0.17, 2),
    ("Sp2", "root", (0, 0.05, 3.55), (0, -0.45, 1), 0.85, 0.15, 3),
    ("Sp3", "root", (0, -0.45, 3.52), (0, -0.5, 1), 0.65, 0.13, 4),
    ("Sp4", "root", (0, -0.95, 3.45), (0, -0.55, 1), 0.48, 0.11, 5),
    ("Horn", "head", (0, 2.62, 4.42), (0, -0.25, 1), 0.36, 0.08, 6),
    ("TailTip", "tail3", (0, -4.15, 1.72), (0, -0.7, -0.5), 0.5, 0.11, 7),
]
WOLF_ICE_SIDE = [
    ("Sh0", "chest", (0.42, 1.0, 3.4), (0.6, -0.3, 0.8), 0.55, 0.12, 11),
    ("Sh1", "chest", (0.6, 0.72, 3.15), (0.9, -0.2, 0.4), 0.4, 0.1, 12),
    ("Hip", "root", (0.5, -1.25, 3.3), (0.7, -0.4, 0.7), 0.42, 0.1, 13),
]
WOLF_POSES = {
    "idle": {},
    "alert": {"neck": (8, 0, 0), "head": (6, 0, 0), "tail1": (-22, 0, 0), "tail2": (-10, 0, 0)},
    "howl": {"chest": (6, 0, 0), "neck": (30, 0, 0), "head": (28, 0, 0), "jaw": (-24, 0, 0), "tail1": (6, 0, 0)},
    "snarl": {"chest": (-7, 0, 0), "neck": (-14, 0, 0), "head": (-4, 0, 0), "jaw": (-22, 0, 0), "tail1": (-26, 0, 0), "tail2": (-12, 0, 0)},
}


def wolf_attrs(me, M):
    v = vcoords(me)
    n = vnormals(me)
    x, y, z = v[:, 0], v[:, 1], v[:, 2]
    nz = n[:, 2]
    Minv = {k: M[k].inverted() for k in ("head", "tail1")}
    hp = np.array([Minv["head"] @ Vector(p) for p in v], np.float32)
    saddle = np.clip((nz - 0.3) / 0.25, 0, 1) * ((y > -2.2) & (y < 1.5) & (z > 2.9)).astype(np.float32)
    saddle *= np.clip(1.0 - (np.abs(x) - 0.45) / 0.2, 0, 1)
    head_top = np.clip((nz - 0.35) / 0.25, 0, 1) * ((hp[:, 1] > 2.1) & (hp[:, 1] < 3.3) & (hp[:, 2] > 4.0)).astype(np.float32)
    tail_top = np.clip((nz - 0.1) / 0.3, 0, 1) * (y < -2.0).astype(np.float32) * (z > 1.9).astype(np.float32)
    s = np.maximum.reduce([saddle, head_top, tail_top])
    set_point_attr(me, "saddle", s)


def build_wolf(M, mats, h=0.032):
    objs = []
    body = sdf_obj("W_Body", wolf_body_prims(), M, mats["fur"], h=h)
    wolf_attrs(body.data, M)
    objs.append(body)
    jaw = sdf_obj("W_Jaw", wolf_jaw_prims(), M, mats["fur"], h=h * 0.85)
    set_point_attr(jaw.data, "saddle", np.zeros(len(jaw.data.vertices), np.float32))
    objs.append(jaw)

    def place(ob, bone):
        ob.matrix_world = M[bone]
        objs.append(ob)

    for nm, bone, base, axis, hh, r, seed in WOLF_ICE:
        place(crystal(f"W_Ice{nm}", base, axis, hh, r, mats["ice"], seed), bone)
    for nm, bone, base, axis, hh, r, seed in WOLF_ICE_SIDE:
        for sx in (1, -1):
            place(crystal(f"W_Ice{nm}{'L' if sx > 0 else 'R'}", (base[0] * sx, base[1], base[2]), (axis[0] * sx, axis[1], axis[2]), hh, r,
                          mats["ice"], seed + (0 if sx > 0 else 40)), bone)
    for sx in (1, -1):
        # ears: outer fur pyramid + pink inner
        b0 = Vector((0.3 * sx, 2.28, 4.3))
        tip = Vector((0.46 * sx, 2.16, 5.08))
        pts = [b0 + Vector((0.26 * sx, 0.06, 0)), b0 + Vector((-0.22 * sx, 0.1, 0)), b0 + Vector((0.02 * sx, -0.22, -0.02)),
               b0 + Vector((0.04 * sx, 0.14, -0.06)), b0 + Vector((0.2 * sx, -0.1, 0.0)), b0 + Vector((-0.16 * sx, -0.08, 0.0)), tip]
        place(hull_obj(pts, f"W_Ear{sx}", mats["fur"], lambda co: {"saddle": 1.0 if co.z > 4.72 else 0.0}, smooth=False), "head")
        ip = [b0 + Vector((0.17 * sx, 0.15, 0.06)), b0 + Vector((-0.13 * sx, 0.17, 0.06)), b0 + Vector((0.02 * sx, 0.19, -0.02)),
              tip + Vector((-0.01 * sx, 0.06, -0.16))]
        place(hull_obj(ip, f"W_EarIn{sx}", mats["inner"], smooth=False), "head")
        place(ellipsoid_obj(f"W_Eye{sx}", (0.34 * sx, 3.0, 4.06), (0.1, 0.065, 0.07), mats["eye"], rot=(0, 0, -28 * sx)), "head")
        place(sweep([Vector((0.17 * sx, 3.36, 3.62)), Vector((0.17 * sx, 3.37, 3.5)), Vector((0.16 * sx, 3.38, 3.4))], [0.045, 0.03, 0.0], 7,
                    name=f"W_FangU{sx}", mat=mats["teeth"]), "head")
        place(sweep([Vector((0.13 * sx, 3.18, 3.62)), Vector((0.13 * sx, 3.19, 3.72)), Vector((0.12 * sx, 3.2, 3.8))], [0.035, 0.024, 0.0], 7,
                    name=f"W_FangL{sx}", mat=mats["teeth"]), "jaw")
        for bone, py, px in (("chest", 1.2, 0.6), ("root", -1.4, 0.62)):
            for c, dx in enumerate((-0.09, 0.0, 0.09)):
                b = Vector((px * sx + dx, py + 0.22, 0.08))
                place(sweep([b, b + Vector((0, 0.08, 0.0)), b + Vector((0, 0.13, -0.06))], [0.035, 0.022, 0.0], 6,
                            name=f"W_Claw{bone}{c}{sx}", mat=mats["claw"]), bone)
    place(ellipsoid_obj("W_Nose", (0, 3.7, 3.85), (0.14, 0.11, 0.1), mats["nose"]), "head")
    place(ellipsoid_obj("W_Mouth", (0, 3.0, 3.62), (0.24, 0.6, 0.1), mats["mouth"]), "head")
    place(ellipsoid_obj("W_Tongue", (0, 3.0, 3.66), (0.15, 0.48, 0.05), mats["tongue"]), "jaw")
    return objs


def habitat_frost(creature_objs, cam):
    """Frostmarch: snowfield, low-poly pines with snow caps, ice spires, cold sky."""
    objs = []
    snow = new_mat("HAB_Snow")[0]
    if not snow.get("built"):
        t = NT(snow)
        co = t.objco()
        nz = t.noise(co, 0.25, 3.0, 0.55)
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0, 1), hexcol("#D6E6F6"), hexcol("#F7FBFF"))
        t.bsdf(col, rough=0.6, spec=0.35, normal=t.bump(t.noise(co, 3.0, 4.0, 0.6).outputs["Fac"], 0.15, 0.1))
        snow["built"] = 1
    pine = mat_simple("HAB_Pine", "#1F5A4E", rough=0.8)
    trunk = mat_simple("HAB_Trunk", "#5A3A2A", rough=0.8)
    ice = bpy.data.materials.get("W_Ice")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=90, y_segments=90, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal((70, 70, 1, 1)), verts=bm.verts)
    for v in bm.verts:
        x, y = v.co.x, v.co.y
        v.co.z = 0.5 * math.sin(x * 0.15 + 0.7) * math.cos(y * 0.12) + 0.25 * math.sin(x * 0.42 + y * 0.33)
        if y < -25:
            v.co.z += (-25 - y) * 0.9
    objs.append(bm_to_obj(bm, "HAB_Snowfield", snow))
    rng = random.Random(21)
    spots = [(-14, -8), (-19, -16), (-9, -20), (11, -11), (17, -18), (24, -7), (-26, -6), (5, -27), (-4, -32), (30, -24), (-31, -22)]
    for i, (x, y) in enumerate(spots):
        hgt = rng.uniform(7, 12)
        objs.append(lathe_obj(f"HAB_Trunk{i}", [(0.35, 0), (0.28, hgt * 0.3), (0, hgt * 0.3)], 8, trunk, (x, y, -0.2), smooth=False))
        for k in range(4):
            z0 = hgt * (0.18 + k * 0.2)
            r0 = (1.0 - k * 0.2) * hgt * 0.32
            objs.append(lathe_obj(f"HAB_Pine{i}_{k}", [(0, z0 - 0.2), (r0, z0), (0, z0 + hgt * 0.32)], 9, pine, (x, y, 0), smooth=False))
            objs.append(lathe_obj(f"HAB_PineSnow{i}_{k}", [(r0 * 0.55, z0 + hgt * 0.14), (0, z0 + hgt * 0.33)], 9, snow, (x, y, 0.02), smooth=False))
    if ice:
        for i, (x, y, hh) in enumerate(((-6.5, -7, 3.5), (8, -6, 2.6), (13.5, -4, 4.2), (-11, -3, 2.2), (3, -13, 5.0))):
            for k in range(3):
                objs.append(crystal(f"HAB_Ice{i}_{k}", (x + rng.uniform(-0.8, 0.8), y + rng.uniform(-0.8, 0.8), 0.0),
                                    (rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), 1), hh * (1.0 - 0.25 * k), 0.45 * (1.0 - 0.2 * k), ice, 70 + i * 3 + k))
    for i in range(40):
        p = Vector((rng.uniform(-18, 18), rng.uniform(-6, 14), rng.uniform(0.5, 11)))
        s_ = rng.uniform(0.25, 0.6)
        objs.append(billboard(os.path.join(OUT, "..", "DragonsHoard", "vfx", "FrostFlake.png"), p, s_, s_, "#ffffff", 1.6,
                              name=f"HAB_Flake{i}", facing=Vector((0, 1, 0))))
    w = bpy.context.scene.world
    nt = w.node_tree
    for nd in list(nt.nodes):
        if nd.type not in ("OUTPUT_WORLD", "BACKGROUND"):
            nt.nodes.remove(nd)
    bg = nt.nodes.get("Background")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    els = ramp.color_ramp.elements
    els[0].position = 0.0
    els[0].color = hexcol("#ffe2c4")
    els[1].position = 0.3
    els[1].color = hexcol("#3a6ab8")
    e = els.new(0.08)
    e.color = hexcol("#b9d4f2")
    bg.inputs["Strength"].default_value = 1.1
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bpy.context.scene.render.film_transparent = False
    for ob in creature_objs:
        ob.matrix_world = Matrix.Translation((-1.0, -1.5, 0.0)) @ Matrix.Rotation(math.radians(55), 4, "Z") @ ob.matrix_world
    for ob in list(bpy.context.scene.objects):
        if ob.type == "LIGHT" and not ob.name.startswith("W_"):
            bpy.data.objects.remove(ob, do_unlink=True)
    objs.append(light("HabSun", "SUN", (-30, 10, 12), (0, 0, 0), 3.6, "#ffd2a8"))
    objs[-1].data.angle = math.radians(3)
    objs.append(light("HabSky", "AREA", (20, 25, 18), (-1, -1.5, 2.5), 2600, "#9cc4ff", size=16))
    persp_view(cam, Vector((4.5, 17.0, 3.6)), Vector((-1.5, -4.0, 3.0)), lens=26)
    return objs


class WolfSpec:
    key = "wolf"
    prefix = "W_"
    poses = WOLF_POSES
    pose_names = ["idle", "alert", "howl", "snarl"]
    hero_pose = "howl"
    hero_dir = Vector((0.66, 0.74, 0.08))
    hero_lens = 40.0
    hero_fit = 0.66
    hero_light = dict(warm="#fff2e2", rim1="#9fe6ff", rim2="#c8d8ff", fill="#7aa8ff")
    pose_dir = Vector((0.78, 0.6, 0.18))
    pose_fit = 0.6
    light_scale = 0.72
    ppu, H = 90, 6.2
    vfx_view = "side"

    def setup(self):
        self.mats = wolf_materials()
        self.rig = wolf_rig()

    def build(self, name):
        return build_wolf(self.rig.mats(self.poses[name]), self.mats)

    def pose_extra(self, name, objs):
        return []

    def parts(self, shot, objs, hide_all_but, iso_shot):
        shot("wolf_part_head.png", Vector((0, 2.95, 4.05)), Vector((2.2, 2.6, 0.7)))
        shot("wolf_part_ruff.png", Vector((0, 1.65, 3.0)), Vector((1.6, 3.0, 0.2)))
        iso_shot("wolf_part_ice.png", [o for o in objs if o.name.startswith("W_IceSp")], Vector((2.8, 0.6, 0.9)))
        iso_shot("wolf_part_ears.png", [o for o in objs if o.name.startswith("W_Ear")], Vector((1.2, 2.6, 0.5)))
        shot("wolf_part_tail.png", Vector((0, -3.3, 2.3)), Vector((3.2, 0.8, 0.8)))
        shot("wolf_part_paws.png", Vector((0.6, 1.25, 0.35)), Vector((1.4, 1.9, 0.6)))
        shot("wolf_part_saddle.png", Vector((0, -0.2, 3.3)), Vector((2.0, 1.6, 2.2)))

    def balls(self):
        m = self.mats
        return [("fur", m["fur"], {"saddle": 0}, False), ("saddle", m["fur"], {"saddle": 1}, False), ("ice", m["ice"], {"t": "z01"}, False),
                ("eye", m["eye"], {}, False), ("inner", m["inner"], {}, False), ("nose", m["nose"], {}, False),
                ("teeth", m["teeth"], {}, False), ("tongue", m["tongue"], {}, False)]

    def vfx(self, objs, M):
        fx = []
        rng = random.Random(8)
        flake = os.path.join(OUT, "..", "DragonsHoard", "vfx", "FrostFlake.png")
        mouth = M["head"] @ Vector((0, 3.8, 3.7))
        for i, (dy, dz, s_, a_) in enumerate(((0.35, 0.05, 0.55, 0.8), (0.7, 0.25, 0.8, 0.55), (1.0, 0.5, 1.05, 0.32))):
            fx.append(billboard("VFX_smoke_puff.png", mouth + Vector((1.2, dy, dz)), s_, s_, "#d8f4ff", 1.3, alpha=a_, name=f"FX_Breath{i}"))
        for i in range(16):
            p = Vector((1.4, rng.uniform(-4.2, 3.6), rng.uniform(0.6, 5.2)))
            s_ = rng.uniform(0.16, 0.32)
            fx.append(billboard(flake, p, s_, s_, "#e6faff", 2.2, name=f"FX_Flake{i}"))
        for i, nm in enumerate(("W_IceSp1", "W_IceSp0", "W_IceSp2", "W_IceHorn")):
            ob = [o for o in objs if o.name == nm][0]
            tip = max((ob.matrix_world @ v.co for v in ob.data.vertices), key=lambda p: p.z)
            fx.append(billboard("VFX_spark_dot.png", tip + Vector((1.2, 0, 0.04)), 0.42, 0.42, "#e8fbff", 7.0, name=f"FX_Glint{i}"))
        for i, (y, s_) in enumerate(((1.35, 0.8), (-1.25, 0.7))):
            fx.append(billboard("VFX_smoke_puff.png", Vector((1.3, y, 0.25)), s_ * 1.6, s_, "#ffffff", 1.4, alpha=0.6, name=f"FX_Step{i}"))
        return fx

    def habitat(self, objs, cam):
        return habitat_frost(objs, cam)


# ============================================================ generic sheet renderer (golem, wolf)
def render_creature(spec, sets):
    reset()
    setup_render()
    spec.setup()
    cam = camera()
    key = spec.key

    def build(name):
        for ob in list(bpy.context.scene.objects):
            if ob.name.startswith(spec.prefix) and ob.type in ("MESH", "LIGHT"):
                bpy.data.objects.remove(ob, do_unlink=True)
        return spec.build(name)

    def lights_for(objs, scale=1.0, **kw):
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT" and not ob.name.startswith(spec.prefix):
                bpy.data.objects.remove(ob, do_unlink=True)
        mn, mx = world_bbox(objs)
        studio_lights((mn + mx) / 2, (mx - mn).length / 2, scale=scale * getattr(spec, "light_scale", 1.0), **kw)
        return mn, mx

    def shot(path, target, offset, lens=50.0, W_=480, H_=380):
        persp_view(cam, Vector(target) + Vector(offset), target, lens)
        render_to(os.path.join(REN, path), W_, H_, samples=110)

    def iso_shot(path, keep, direction, lens=50.0):
        hide_all_but(keep)
        bb0, bb1 = world_bbox(keep, True)
        cc = (bb0 + bb1) / 2
        R = (bb1 - bb0).length / 2
        half = math.atan(18.0 * 380 / 480 / lens)
        persp_view(cam, cc + direction.normalized() * (R / math.sin(half) * 1.02), cc, lens)
        render_to(os.path.join(REN, path), 480, 380, samples=110)
        for ob in bpy.context.scene.objects:
            if ob.type == "MESH":
                ob.hide_render = False

    if "ortho" in sets or "vfx" in sets:
        objs = build("idle")
        mn, mx = lights_for(objs)
        catcher = shadow_catcher()
        ppu, H = spec.ppu, spec.H
        hpx = int(H * ppu)
        cz = H / 2 - 0.12
        c = (mn + mx) / 2
        ws = int((mx.y - mn.y + 0.8) * ppu)
        wf = int((mx.x - mn.x + 0.8) * ppu)
        if "ortho" in sets:
            ortho_view(cam, "side", (0, c.y, cz), ppu, ws, hpx)
            render_to(os.path.join(REN, f"{key}_side.png"), ws, hpx)
            ortho_view(cam, "front", (c.x, 0, cz), ppu, wf, hpx)
            render_to(os.path.join(REN, f"{key}_front.png"), wf, hpx)
            ortho_view(cam, "back", (c.x, 0, cz), ppu, wf, hpx)
            render_to(os.path.join(REN, f"{key}_back.png"), wf, hpx)
            json.dump({"ppu": ppu, "H": H, "bbox_min": list(mn), "bbox_max": list(mx), "side_w": ws, "front_w": wf},
                      open(os.path.join(REN, f"{key}_ortho.json"), "w"), indent=1)
        if "vfx" in sets:
            fx = spec.vfx(objs, spec.rig.mats({}))
            view = getattr(spec, "vfx_view", "side")
            if view == "front":
                ortho_view(cam, "front", (c.x, 0, cz), ppu, wf, hpx)
                render_to(os.path.join(REN, f"{key}_vfx.png"), wf, hpx, samples=110)
            else:
                ortho_view(cam, "side", (0, c.y, cz), ppu, ws, hpx)
                render_to(os.path.join(REN, f"{key}_vfx.png"), ws, hpx, samples=110)
            for ob in fx:
                bpy.data.objects.remove(ob, do_unlink=True)
        bpy.data.objects.remove(catcher, do_unlink=True)

    if "hero" in sets:
        objs = build(spec.hero_pose)
        mn, mx = lights_for(objs, scale=1.15, **spec.hero_light)
        catcher = shadow_catcher()
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        W_, H_ = 872, 1192
        half = math.atan(18.0 * W_ / H_ / spec.hero_lens)
        persp_view(cam, c + spec.hero_dir.normalized() * (R / math.sin(half) * spec.hero_fit), c + Vector((0, 0, -0.3)), lens=spec.hero_lens)
        render_to(os.path.join(REN, f"{key}_hero.png"), W_, H_)
        bpy.data.objects.remove(catcher, do_unlink=True)

    if "poses" in sets:
        boxes = []
        for nm in spec.pose_names:
            objs = build(nm)
            boxes.append(world_bbox(objs))
        mn = Vector((min(b[0].x for b in boxes), min(b[0].y for b in boxes), min(b[0].z for b in boxes)))
        mx = Vector((max(b[1].x for b in boxes), max(b[1].y for b in boxes), max(b[1].z for b in boxes)))
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        W_, H_ = 640, 500
        lens = 45.0
        half = math.atan(18.0 * H_ / W_ / lens)
        camloc = c + spec.pose_dir.normalized() * (R / math.sin(half) * getattr(spec, "pose_fit", 0.62))
        for nm in spec.pose_names:
            objs = build(nm)
            lights_for(objs)
            catcher = shadow_catcher()
            extra = spec.pose_extra(nm, objs)
            persp_view(cam, camloc, c + Vector((0, 0, -0.2)), lens)
            render_to(os.path.join(REN, f"{key}_pose_{nm}.png"), W_, H_, samples=110)
            for ob in extra + [catcher]:
                bpy.data.objects.remove(ob, do_unlink=True)

    if "parts" in sets:
        objs = build("idle")
        lights_for(objs)
        spec.parts(shot, objs, hide_all_but, iso_shot)
        for ob in bpy.context.scene.objects:
            if ob.type == "LIGHT":
                ob.data.energy *= 0.1
        bg = bpy.context.scene.world.node_tree.nodes["Background"]
        bg.inputs["Strength"].default_value = 0.06
        mn, mx = world_bbox(objs)
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        persp_view(cam, c + spec.pose_dir.normalized() * R * 2.1, c, 40)
        render_to(os.path.join(REN, f"{key}_part_glow.png"), 480, 380, samples=110)
        bg.inputs["Strength"].default_value = 0.55

    if "mats" in sets:
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT":
                bpy.data.objects.remove(ob, do_unlink=True)
            elif ob.type == "MESH":
                ob.hide_render = True
        studio_lights(Vector((0, 0, 0)), 1.6)
        persp_view(cam, Vector((0, 3.6, 0.7)), Vector((0, 0, 0)), lens=50)
        for nm, mat, at, flip in spec.balls():
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=1.0)
            zs = [v.co.z for v in bm.verts]
            attrs = {}
            for k_, val in at.items():
                attrs[k_] = [(z_ + 1) / 2 for z_ in zs] if val == "z01" else [float(val)] * len(zs)
            for k_ in ("belly", "crack", "vs", "t", "ph", "edge", "bonefac", "saddle", "fur"):
                attrs.setdefault(k_, [0.0] * len(zs))
            ob = bm_to_obj(bm, f"MatBall_{nm}", mat, attrs)
            if flip:
                ob.rotation_euler = (math.pi, 0, 0)
            render_to(os.path.join(REN, f"{key}_mat_{nm}.png"), 220, 220, samples=96)
            bpy.data.objects.remove(ob, do_unlink=True)

    if "scale" in sets:
        objs = build("idle")
        mn, mx = world_bbox(objs)
        av = build_avatar(Vector((0, mx.y + 1.9, 0)))
        lights_for(objs + av)
        catcher = shadow_catcher()
        ppu = 52 if spec.H > 9 else 60
        y0, y1 = mn.y - 0.4, mx.y + 3.4
        W_ = int((y1 - y0) * ppu)
        H_ = int((spec.H + 0.1) * ppu)
        ortho_view(cam, "side", (0, (y0 + y1) / 2, (spec.H + 0.1) / 2 - 0.15), ppu, W_, H_)
        render_to(os.path.join(REN, f"{key}_scale.png"), W_, H_, samples=110)
        json.dump({"ppu": ppu, "y0": y0, "y1": y1, "avatar_y": mx.y + 1.9, "H": spec.H + 0.1, "height": mx.z, "length": mx.y - mn.y,
                   "width": mx.x - mn.x}, open(os.path.join(REN, f"{key}_scale.json"), "w"), indent=1)
        for ob in av + [catcher]:
            bpy.data.objects.remove(ob, do_unlink=True)

    if "habitat" in sets:
        objs = build("idle")
        hab = spec.habitat(objs, cam)
        render_to(os.path.join(REN, f"{key}_habitat.png"), 1320, 504, samples=160)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"FantasyCreatures_{key}.blend"))


# ============================================================ CINDER DRAKE v3: anatomy pass (grey review model)
# Holden's direction (2026-10-04): believable, intimidating dark-fantasy dragon. Anatomy/proportion/silhouette first:
# angular reptilian skull, small recessed eyes under a bony brow, cheekbones, jaw muscles + hinge, nostrils, closed
# un-grinning mouth with varied curved teeth; ribcage, scapulae, pelvis, tucked waist; jointed legs with separated
# toes and gripping claws; large wings with a real shoulder attachment, jointed fingers and thin tensioned membranes;
# grounded predator stance (head low, shoulders high, weight forward). Modelled directly in the stance.
# Method (v3.1): big masses blended wide so muscles never read as balloons; angular bone from convex hulls (P_hull);
# muscle bellies as long ellipsoids sunk into the limb core (P_ell_ab); ribs displaced onto the final surface (post).

def lerpv(a, b, t):
    a, b = Vector(a), Vector(b)
    return a + (b - a) * t


def tup(v):
    return (float(v[0]), float(v[1]), float(v[2]))


D3_HEAD_B = Vector((0, 3.5, 2.97))      # occiput / head pivot (neck shortened 0.28 after the anatomy review)
D3_HEAD_PITCH = -18.0                    # skull axis points forward-down (head lowered, eyes level)


def d3_head_frame():
    a = math.radians(D3_HEAD_PITCH)
    return Vector((0, math.cos(a), math.sin(a))), Vector((0, -math.sin(a), math.cos(a)))


D3_HEAD_SCALE = 1.12                     # whole head (skull, jaw, eyes, teeth, horns) relative to the body


def HP(s, x, w):
    """Head-local point: s along the skull axis (from the occiput), x lateral, w up along the skull."""
    d, u = d3_head_frame()
    return D3_HEAD_B + (d * s + Vector((x, 0, 0)) + u * w) * D3_HEAD_SCALE


def HR(*v):
    """Head-scaled size(s)."""
    return tuple(x * D3_HEAD_SCALE for x in v) if len(v) > 1 else v[0] * D3_HEAD_SCALE


# proportions pass (2026-10-04, Holden: "the legs feel a bit skinny"): limbs, feet and tail thickened against big-cat
# references - lion forearm girth ~48 cm at ~110 cm shoulder height = mean diameter ~0.14 x shoulder height, and heavier
# animals need stouter legs (elastic similarity) - while keeping wrists/ankles narrower than the muscle masses.
D3_TAIL = [((0, -2.55, 3.18), 0.58), ((0, -3.7, 2.82), 0.49), ((0, -4.9, 2.22), 0.39), ((0, -6.1, 1.62), 0.29),
           ((0, -7.2, 1.12), 0.2), ((0, -8.2, 0.78), 0.12), ((0, -9.0, 0.58), 0.05)]
# limb landmarks (left side = +X, mirrored). Front: scapula top, shoulder joint, elbow (points back), wrist, knuckles.
D3_FRONT = dict(top=(0.4, 0.82, 3.98), sh=(0.97, 1.62, 2.52), el=(1.13, 0.92, 1.44), wr=(1.15, 1.4, 0.5), kn=(1.17, 1.68, 0.18))
# Back: hip socket, knee (points forward), hock (points back), ball of the foot (digitigrade).
D3_BACK = dict(hip=(0.82, -2.1, 2.72), knee=(1.05, -1.25, 1.56), hock=(1.06, -2.32, 0.88), ball=(1.08, -1.98, 0.18))
D3_FTOES = dict(len=(0.33, 0.44, 0.42, 0.33), off=(-0.24, -0.08, 0.08, 0.24))
D3_BTOES = dict(len=(0.46, 0.57, 0.48), off=(-0.23, 0.0, 0.23))
# wing: shoulder joint, elbow, wrist, four fingers (knuckle, tip), trailing-edge attachment on the flank
D3_WING = dict(S=(0.72, 0.5, 4.06), E=(2.0, 0.05, 4.5), W=(2.35, 1.0, 6.55),
               digits=[((3.05, 0.25, 7.25), (3.95, -1.75, 7.6)), ((3.0, -0.35, 6.55), (3.7, -3.05, 6.0)),
                       ((2.75, -0.5, 5.75), (3.05, -3.6, 4.55)), ((2.45, -0.4, 5.15), (2.25, -3.15, 3.75))],
               A=(0.75, -2.05, 3.3))


def drake3_rig():
    r = Rig()
    r.add("root", None, (0, -2.0, 3.05))
    r.add("chest", "root", (0, 0.4, 3.0))
    r.add("neck", "chest", (0, 1.7, 3.3))
    r.add("neck2", "neck", (0, 2.7, 3.2))
    r.add("head", "neck2", tup(D3_HEAD_B))
    r.add("jaw", "head", tup(HP(0.1, 0, -0.25)))
    for i in range(5):
        r.add(f"tail{i + 1}", "root" if i == 0 else f"tail{i}", D3_TAIL[i][0])
    r.add("wing_L", "chest", D3_WING["S"])
    r.add("wing_R", "chest", (-D3_WING["S"][0], D3_WING["S"][1], D3_WING["S"][2]))
    return r


def d3_toe(base, L, ox, arch=0.075, ground=0.075, splay=0.5):
    """One gripping toe: base on the knuckle line, raised middle knuckle, tip pressed to the ground."""
    b = Vector(base)
    b0 = b + Vector((ox, 0.02, 0.0))
    m = b + Vector((ox * (1 + splay * 0.5), L * 0.47, arch))
    t = b + Vector((ox * (1 + splay), L, 0.0))
    t.z = ground
    return b0, m, t


def d3_toe_prims(bone, base, spec, r0):
    P = []
    for L, ox in zip(spec["len"], spec["off"]):
        b0, m, t = d3_toe(base, L, ox)
        P += [P_cone(bone, tup(b0), tup(m), r0, r0 * 0.86, k=0.045),
              P_sph(bone, tup(m), r0 * 0.9, k=0.025),
              P_cone(bone, tup(m), tup(t), r0 * 0.84, r0 * 0.6, k=0.03)]
    return P


def d3_front_leg():
    f = {k: Vector(v) for k, v in D3_FRONT.items()}
    top, sh, el, wr, kn = f["top"], f["sh"], f["el"], f["wr"], f["kn"]
    B = "chest"
    P = [
        # scapula blade lying on the ribcage; its top edge stands proud of the spine (high shoulders)
        P_ell_ab(B, top + Vector((0.0, 0.02, 0.06)), sh + Vector((-0.05, -0.12, 0.3)), 0.13, 0.3, k=0.2, lat=(0.9, 0, 0.45)),
        P_cone(B, tup(top + Vector((0.07, -0.02, 0.03))), tup(sh + Vector((0.06, -0.02, 0.26))), 0.065, 0.06, k=0.07),
        # upper arm: bone core, triceps (back), biceps (front), deltoid cap, pectoral web to the sternum
        P_cone(B, tup(sh), tup(el), 0.33, 0.21, k=0.16),
        P_ell_ab(B, sh + Vector((-0.03, -0.3, 0.06)), el + Vector((-0.02, -0.17, 0.12)), 0.25, 0.23, k=0.15),
        P_ell_ab(B, sh + Vector((0.05, 0.17, -0.25)), el + Vector((0.03, 0.21, 0.18)), 0.14, 0.13, k=0.12),
        P_ell_ab(B, sh + Vector((0.05, -0.06, 0.28)), lerpv(sh, el, 0.55) + Vector((0.08, 0.04, 0)), 0.19, 0.23, k=0.13),
        P_cone(B, tup(el), tup(el + Vector((0.0, -0.24, 0.13))), 0.17, 0.085, k=0.06),               # olecranon
        # forearm: heavy tapering core; the extensor mass is a ropey ridge on the front-outer side and the flexors fill
        # the back - both sit in the upper half so the forearm tapers to a narrower, bony wrist with a carpal spur
        P_cone(B, tup(el), tup(wr), 0.31, 0.2, k=0.1),
        P_ell_ab(B, el + Vector((0.07, 0.08, -0.05)), lerpv(el, wr, 0.62) + Vector((0.06, 0.04, 0)), 0.24, 0.22, k=0.1),
        P_ell_ab(B, el + Vector((-0.05, -0.09, -0.08)), lerpv(el, wr, 0.55) + Vector((-0.03, -0.07, 0)), 0.19, 0.2, k=0.1),
        P_ell(B, tup(wr), (0.23, 0.19, 0.17), k=0.05),
        P_cone(B, tup(wr + Vector((0, -0.07, 0.03))), tup(wr + Vector((0.0, -0.3, 0.12))), 0.085, 0.028, k=0.04),
        # broad hand down to the knuckle line, inner dewclaw
        P_ell_ab(B, wr, kn, 0.31, 0.15, k=0.07),
        P_cone(B, tup(wr + Vector((-0.15, 0.0, -0.12))), tup(wr + Vector((-0.22, 0.14, -0.3))), 0.075, 0.05, k=0.04),
    ]
    return P + d3_toe_prims(B, kn, D3_FTOES, 0.135)


def d3_hind_leg():
    b = {k: Vector(v) for k, v in D3_BACK.items()}
    hip, knee, hock, ball = b["hip"], b["knee"], b["hock"], b["ball"]
    B = "root"
    P = [
        # thigh grows out of the flank (wide blend, flat outer face) instead of hanging off it like a ball
        P_ell_ab(B, Vector((0.55, -2.05, 3.2)), knee + Vector((-0.05, -0.1, 0.12)), 0.34, 0.66, k=0.3),
        P_ell_ab(B, Vector((0.5, -2.85, 3.05)), knee + Vector((-0.06, -0.4, -0.05)), 0.27, 0.25, k=0.16),   # hamstrings
        P_ell_ab(B, Vector((0.74, -1.55, 2.95)), knee + Vector((0.0, 0.07, 0.12)), 0.26, 0.23, k=0.16),     # quadriceps
        P_cone(B, tup(hip), tup(knee), 0.33, 0.22, k=0.16),
        P_sph(B, tup(knee + Vector((0.02, 0.11, 0.03))), 0.14, k=0.06),                                     # kneecap
        # shank: calf belly high at the back, Achilles cord to the heel point, a metatarsus strong enough to carry it
        P_cone(B, tup(knee), tup(hock), 0.3, 0.19, k=0.1),
        P_ell_ab(B, knee + Vector((0, -0.13, -0.04)), lerpv(knee, hock, 0.55) + Vector((0, -0.11, 0.03)), 0.22, 0.25, k=0.12),
        P_cone(B, tup(lerpv(knee, hock, 0.5) + Vector((0, -0.15, 0))), tup(hock + Vector((0, -0.2, 0.05))), 0.09, 0.07, k=0.06),
        P_cone(B, tup(hock), tup(hock + Vector((0, -0.24, 0.07))), 0.15, 0.075, k=0.05),                    # heel
        P_cone(B, tup(hock), tup(ball), 0.22, 0.19, k=0.07),
        P_cone(B, tup(ball + Vector((-0.08, -0.07, 0.05))), tup(ball + Vector((-0.15, -0.32, -0.04))), 0.08, 0.055, k=0.03),
    ]
    return P + d3_toe_prims(B, ball, D3_BTOES, 0.145)


# upper skull base: convex wedge, widest at the cheeks, straight top line occiput -> nose (the brow masses sit on
# top of it, so the profile steps down from the brow to a shorter, deep muzzle); (s, [(x, w)...]) +x half-sections
D3_SKULL = [(0.0, [(0.2, 0.3), (0.32, 0.18), (0.34, -0.08), (0.22, -0.2)]),
            (0.4, [(0.24, 0.27), (0.4, 0.16), (0.46, -0.06), (0.42, -0.21)]),
            (0.9, [(0.2, 0.24), (0.34, 0.15), (0.37, -0.21)]),
            (1.42, [(0.14, 0.2), (0.23, 0.135), (0.25, -0.21)]),
            (1.75, [(0.1, 0.175), (0.17, 0.1), (0.18, -0.2)]),
            (1.83, [(0.08, 0.06), (0.12, -0.17)])]
# lower jaw: deep at the angle behind the mouth corner, straight bottom line to a squared chin
D3_JAW = [(0.05, [(0.4, -0.225), (0.38, -0.4)]),
          (0.4, [(0.4, -0.225), (0.34, -0.72)]),
          (1.0, [(0.31, -0.225), (0.26, -0.58)]),
          (1.66, [(0.15, -0.225), (0.12, -0.42)]),
          (1.72, [(0.105, -0.24), (0.08, -0.37)])]
D3_EYE = (0.74, 0.335, 0.165)            # head-local eye centre (s, x, w)
D3_EYE_RAD = (0.03, 0.075, 0.036)        # eye radii: outward, along the slit, across the slit (head-scaled)


def d3_eye_frame(s):
    """World centre + axes of the left (s=1) / right (s=-1) eye: slanted slit (front corner low), looking forward-out."""
    d, u = d3_head_frame()
    X = Vector((1, 0, 0))
    out = (X * s * math.cos(math.radians(22)) + d * math.sin(math.radians(22))).normalized()
    lng = (d - out * d.dot(out)).normalized()
    lng = (lng * math.cos(math.radians(14)) - u * math.sin(math.radians(14))).normalized()
    return HP(D3_EYE[0], D3_EYE[1] * s, D3_EYE[2]), out, lng, out.cross(lng).normalized()


def d3_eyelid_prims(s):
    """Upper + lower lid rims hugging the eyeball so it reads as a narrowed slit, not a button."""
    c, out, lng, up = d3_eye_frame(s)
    ro, rl, ru = HR(*D3_EYE_RAD)
    P = []
    for sgn, thick in ((1, 0.024), (-1, 0.018)):
        mid = c + up * (sgn * ru * 0.92) + out * (ro * 0.35)
        P.append(P_ell_ab("head", mid - lng * (rl * 1.05), mid + lng * (rl * 1.05), HR(thick), HR(thick * 0.9), k=HR(0.02), lat=tuple(out)))
    return P


def d3_section_pts(sections):
    pts = []
    for s_, half in sections:
        for x_, w_ in half:
            pts += [HP(s_, x_, w_), HP(s_, -x_, w_)]
    return pts


def d3_lip_x(s):
    return float(np.interp(s, [0.4, 0.9, 1.42, 1.75], [0.42, 0.37, 0.25, 0.18]))


def d3_jaw_x(s):
    return float(np.interp(s, [0.4, 1.0, 1.66], [0.4, 0.31, 0.15]))


def d3_head_prims():
    hr = (D3_HEAD_PITCH, 0, 0)
    B = "head"
    X = (1, 0, 0)
    es, ex, ew = D3_EYE
    P = [P_hull(B, d3_section_pts(D3_SKULL), edge=HR(0.05), k=HR(0.12)),
         P_ell_ab(B, HP(1.0, 0, 0.22), HP(-0.02, 0, 0.3), HR(0.065), HR(0.06), k=HR(0.07))]         # sagittal crest (round)
    side = [
        # heavy brow ridge: the highest point of the head, overhanging the eye, ramping down into the muzzle; its top is a
        # ridge (two planes meeting along a crest line) rather than a flat slab
        P_hull(B, [HP(0.33, 0.18, 0.33), HP(0.33, 0.33, 0.39), HP(0.33, 0.43, 0.3), HP(0.33, 0.39, 0.22), HP(0.33, 0.2, 0.25),
                   HP(0.72, 0.16, 0.36), HP(0.72, 0.32, 0.43), HP(0.72, 0.47, 0.32), HP(0.72, 0.43, 0.24),
                   HP(1.1, 0.13, 0.25), HP(1.1, 0.22, 0.28), HP(1.1, 0.3, 0.23), HP(1.1, 0.29, 0.18), HP(1.1, 0.14, 0.22)],
               edge=HR(0.03), k=HR(0.09)),
        # supraorbital bar from the brow back into the horn base
        P_hull(B, [HP(0.4, 0.4, 0.32), HP(0.4, 0.26, 0.38), HP(0.4, 0.36, 0.23),
                   HP(0.04, 0.34, 0.32), HP(0.04, 0.24, 0.36), HP(0.04, 0.31, 0.22)], edge=HR(0.03), k=HR(0.08)),
        # cheekbone: sharp outer edge under the eye, flaring wide toward the jaw hinge
        P_hull(B, [HP(0.88, 0.33, 0.07), HP(0.88, 0.395, 0.02), HP(0.88, 0.33, -0.05),
                   HP(0.15, 0.48, 0.01), HP(0.15, 0.6, -0.08), HP(0.15, 0.47, -0.18)], edge=HR(0.02), k=HR(0.06)),
        # paired nasal ridges running into the nostril bosses
        P_hull(B, [HP(0.98, 0.09, 0.235), HP(0.98, 0.18, 0.235), HP(0.98, 0.135, 0.3),
                   HP(1.55, 0.065, 0.185), HP(1.55, 0.145, 0.185), HP(1.55, 0.105, 0.24)], edge=HR(0.025), k=HR(0.06)),
        P_ell_ab(B, HP(1.5, 0.11, 0.2), HP(1.76, 0.105, 0.15), HR(0.05), HR(0.045), k=HR(0.04), lat=X),           # nostril boss
        P_ell(B, tup(HP(0.32, 0.42, 0.1)), HR(0.06, 0.12, 0.06), hr, k=HR(0.05), mode="sub"),                     # temporal hollow
        P_ell(B, tup(HP(es, 0.42, ew)), HR(0.08, 0.13, 0.075), hr, k=HR(0.04), mode="sub"),                       # deep eye socket
        P_ell(B, tup(HP(1.74, 0.11, 0.15)), HR(0.02, 0.05, 0.018), (D3_HEAD_PITCH, 0, 20), k=HR(0.015), mode="sub"),
        P_ell(B, tup(HP(1.6, 0.21, -0.17)), HR(0.045, 0.05, 0.06), hr, k=HR(0.03), mode="sub")]                    # fang notch
    # palate vault: a shallow pocket in the roof of the mouth (seen only when the jaw opens: roar / fire breath)
    palate = [P_ell_ab(B, HP(0.55, 0, -0.205), HP(1.62, 0, -0.205), HR(0.2), HR(0.06), k=HR(0.03), mode="sub", lat=X)]
    return P + side + mirror_x(side) + palate + d3_eyelid_prims(1) + d3_eyelid_prims(-1)


def drake3_body_prims():
    P = []
    # --- torso: deep egg-shaped ribcage with a sternum keel, tucked waist, broad pelvis
    P += [P_ell("chest", (0, 0.6, 2.62), (0.8, 1.35, 1.05), (-6, 0, 0), k=0.3),
          P_ell("chest", (0, 1.0, 1.98), (0.36, 0.85, 0.4), (-10, 0, 0), k=0.3),            # keel: lowest between the elbows
          P_ell("chest", (0, 1.8, 2.68), (0.44, 0.32, 0.5), (25, 0, 0), k=0.25),            # prow under the neck
          P_ell("root", (0, -1.05, 3.0), (0.57, 0.95, 0.63), k=0.38),
          P_ell("root", (0, -2.05, 3.08), (0.66, 0.85, 0.58), k=0.3),
          P_ell("chest", (0, 2.0, 2.25), (0.045, 0.22, 0.42), (25, 0, 0), k=0.05, mode="sub")]   # groove between the pecs
    side = [P_ell_ab("chest", (0.1, 1.98, 2.0), (0.8, 1.62, 2.75), 0.11, 0.19, k=0.16, lat=(0, 1, 0)),   # pectoral (V to the arm)
            P_ell_ab("root", (0.2, 1.15, 3.5), (0.2, -2.75, 3.5), 0.22, 0.17, k=0.2),          # epaxial (spine valley)
            P_ell("root", (0.47, -1.68, 3.48), (0.15, 0.3, 0.12), k=0.12),                       # iliac crest
            P_cone("chest", (0.22, 0.65, 3.62), D3_WING["S"], 0.36, 0.17, k=0.22),                # wing-root mound
            P_ell("chest", (0.42, 0.5, 3.86), (0.3, 0.5, 0.2), k=0.22)]
    side += d3_front_leg() + d3_hind_leg()
    P += side + mirror_x(side)
    # --- neck: thick at the shoulders, arched top line, cords from the jaw hinge to the chest, throat
    P += [P_cone("neck", (0, 1.3, 3.1), (0, 2.4, 3.25), 0.7, 0.5, k=0.3),
          P_cone("neck2", (0, 2.4, 3.25), (0, 3.2, 3.12), 0.48, 0.36, k=0.22),
          P_cone("neck2", (0, 3.2, 3.12), tup(HP(0.15, 0, -0.08)), 0.36, 0.3, k=0.2),
          P_ell_ab("neck", (0, 1.4, 3.85), (0, 3.15, 3.42), 0.28, 0.18, k=0.22),
          P_ell_ab("neck2", (0, 2.15, 2.7), HP(0.35, 0, -0.5), 0.22, 0.15, k=0.2)]
    cord = [P_cone("neck2", tup(HP(0.18, 0.3, -0.36)), (0.32, 1.85, 2.35), 0.12, 0.17, k=0.15)]
    P += cord + mirror_x(cord)
    P += d3_head_prims()
    # --- tail: long taper, held low
    for i in range(len(D3_TAIL) - 1):
        (a, ra), (bb, rb) = D3_TAIL[i], D3_TAIL[i + 1]
        P.append(P_cone(f"tail{min(i + 1, 5)}", a, bb, ra, rb, k=0.16 if i < 2 else 0.1))
    return P


def drake3_jaw_prims():
    B = "jaw"
    side = [P_ell_ab(B, HP(0.1, 0.36, -0.32), HP(0.8, 0.31, -0.43), HR(0.09), HR(0.15), k=HR(0.1))]   # masseter, flat
    X = (1, 0, 0)
    # mouth floor: a trough inside the jaw with a tongue lying in it (hidden while the mouth is closed)
    mouth = [P_ell_ab(B, HP(0.5, 0, -0.225), HP(1.62, 0, -0.225), HR(0.19), HR(0.07), k=HR(0.03), mode="sub", lat=X),
             P_ell_ab(B, HP(0.55, 0, -0.29), HP(1.42, 0, -0.27), HR(0.12), HR(0.045), k=HR(0.03), lat=X)]
    return [P_hull(B, d3_section_pts(D3_JAW), edge=HR(0.05), k=HR(0.1))] + side + mirror_x(side) + mouth


def d3_body_detail(v, n):
    """Displacement on the final body surface: rib bands on the flank between the elbow and the waist."""
    def ramp(a, lo, hi):
        return np.clip((a - lo) / (hi - lo), 0.0, 1.0)
    x, y, z = v[:, 0], v[:, 1], v[:, 2]
    w = ramp(np.abs(x), 0.42, 0.62) * ramp(y, -0.75, -0.45) * (1 - ramp(y, 0.3, 0.55)) * \
        ramp(z, 1.8, 2.1) * (1 - ramp(z, 3.0, 3.3)) * np.clip(np.abs(n[:, 0]) * 1.3, 0, 1)
    s = y - 0.38 * (z - 2.6)
    band = (0.5 + 0.5 * np.cos(s * (2 * math.pi / 0.3))) ** 2
    return (0.022 * w * (band - 0.35)).astype(np.float32)


def d3_poly_point(poly, t):
    L = [0.0]
    for i in range(len(poly) - 1):
        L.append(L[-1] + (poly[i + 1] - poly[i]).length)
    s = t * L[-1]
    for i in range(len(poly) - 1):
        if s <= L[i + 1] or i == len(poly) - 2:
            seg = max(L[i + 1] - L[i], 1e-9)
            return poly[i] + (poly[i + 1] - poly[i]) * ((s - L[i]) / seg)
    return poly[-1]


def d3_membrane_panel(bm, polyA, polyB, scallop, sag, nrm_hint, ev, bv, nU=12, nT=14, ripple=0.012):
    tipA, tipB = polyA[-1], polyB[-1]
    W = polyA[0]
    nrm = (tipA - W).cross(tipB - W)
    nrm = nrm.normalized() if nrm.length > 1e-6 else Vector((0, 0, 1))
    if nrm.dot(nrm_hint) < 0:
        nrm = -nrm
    grid = []
    for iu in range(nU + 1):
        u = iu / nU
        tmax = 1.0 - scallop * math.sin(math.pi * u)
        row = []
        for it in range(nT + 1):
            tt = (it / nT) * tmax
            pa, pb = d3_poly_point(polyA, tt), d3_poly_point(polyB, tt)
            p = pa + (pb - pa) * u
            p = p + nrm * (sag * math.sin(math.pi * u) * tt ** 1.2 + ripple * tt * math.sin(u * math.pi * 6.0))
            row.append(bm.verts.new(p))
            ev.append(tt)
            bv.append(max(0.0, 1.0 - min(u, 1.0 - u) * 7.0))
        grid.append(row)
    for iu in range(nU):
        for it in range(nT):
            bm.faces.new((grid[iu][it], grid[iu + 1][it], grid[iu + 1][it + 1], grid[iu][it + 1]))


def d3_wing_points(sx):
    def V(p):
        return Vector((p[0] * sx, p[1], p[2]))
    return V(D3_WING["S"]), V(D3_WING["E"]), V(D3_WING["W"]), V(D3_WING["A"]), [(V(k), V(t)) for k, t in D3_WING["digits"]]


def d3_wing_arm_prims(sx):
    """Wing arm as its own SDF: humerus + biceps, pointed elbow, forearm belly, wrist, metacarpals, knuckles, thumb."""
    S, E, W, A, digits = d3_wing_points(sx)
    B = "wing_L" if sx > 0 else "wing_R"
    ept = E + ((E - S).normalized() + (E - W).normalized()).normalized() * 0.15
    P = [P_cone(B, tup(S), tup(E), 0.19, 0.105, k=0.08),
         P_ell_ab(B, lerpv(S, E, -0.05), lerpv(S, E, 0.6) + Vector((0, 0.05, 0.03)), 0.15, 0.19, k=0.1),    # flight muscle
         P_ell_ab(B, lerpv(S, E, 0.3) + Vector((0, -0.05, 0.02)), lerpv(S, E, 0.95), 0.085, 0.1, k=0.07),     # triceps cord
         P_cone(B, tup(E), tup(ept), 0.095, 0.05, k=0.05),
         P_cone(B, tup(E), tup(W), 0.1, 0.07, k=0.07),
         P_ell_ab(B, lerpv(E, W, 0.04), lerpv(E, W, 0.48), 0.09, 0.1, k=0.07),
         P_sph(B, tup(W), 0.085, k=0.05),
         P_cone(B, tup(W), tup(W + Vector((0.06 * sx, 0.34, 0.2))), 0.06, 0.03, k=0.04)]
    for k_, t_ in digits:
        P += [P_cone(B, tup(W), tup(k_), 0.06, 0.045, k=0.045), P_sph(B, tup(k_), 0.05, k=0.03)]
    # leading-edge skin web along humerus and forearm, flattened in the wing plane toward the propatagium: the arm merges
    # into the membrane with a teardrop section instead of reading as a round tube
    nw = (E - S).cross(W - S).normalized()
    for a_, b_, toward, w_ in ((S, E, W, 0.13), (E, W, S, 0.11)):
        ab = (b_ - a_).normalized()
        perp = toward - (a_ + b_) * 0.5
        perp = perp - ab * perp.dot(ab) - nw * perp.dot(nw)
        perp.normalize()
        P.append(P_ell_ab(B, lerpv(a_, b_, 0.06) + perp * 0.05, lerpv(a_, b_, 0.94) + perp * 0.05, w_, 0.035, k=0.05,
                          lat=tuple(perp)))
    # knobbly wrist: two carpal knuckles on the top of the joint
    P += [P_sph(B, tup(W + nw * 0.05 + (W - E).normalized() * 0.03), 0.06, k=0.03),
          P_sph(B, tup(W + nw * 0.04 - (W - E).normalized() * 0.06), 0.055, k=0.03)]
    return P


def d3_wing_top(sx):
    """Unit normal of the wing plane pointing to the wing's top (dorsal) side."""
    S, E, W, A, digits = d3_wing_points(sx)
    nw = (E - S).cross(W - S).normalized()
    return nw if nw.z > 0 else -nw


def build_wing3(sx, mats, name, M, bvh):
    """Large articulated wing: SDF arm, two-phalanx fingers, thin sagging membranes attached along the flank."""
    S, E, W, A, digits = d3_wing_points(sx)
    # the wing arm is a skin-covered limb (scaled skin shader), not a bare black tube; fine scales at elbow and wrist
    arm = sdf_obj(name + "_Arm", d3_wing_arm_prims(sx), M, mats["skin"], h=0.016, smooth_iters=4)
    av = vcoords(arm.data)
    jd = np.minimum(np.linalg.norm(av - np.array(tuple(E), np.float32), axis=1), np.linalg.norm(av - np.array(tuple(W), np.float32), axis=1))
    set_point_attr(arm.data, "dors", np.full(len(av), 0.8, np.float32))
    set_point_attr(arm.data, "joint", np.clip(1.0 - jd / 0.3, 0.0, 1.0))
    objs = [arm]
    flank = []
    for i in range(1, 8):
        t = i / 7
        y, z = S.y - 0.25 + (A.y - S.y + 0.25) * t, S.z - 0.35 + (A.z - S.z + 0.35) * t
        hit = bvh.ray_cast(Vector((3.5 * sx, y, z)), Vector((-sx, 0, 0)))
        flank.append(hit[0] - Vector((0.03 * sx, 0, 0)) if hit[0] is not None else Vector((A.x, y, z)))
    fingers = []
    for i, (k_, t_) in enumerate(digits):
        j = lerpv(k_, t_, 0.46) + (k_ - W).normalized() * 0.04
        fingers.append([W, k_, j, t_])
        objs.append(sweep([k_, lerpv(k_, j, 0.5), j], [0.042, 0.037, 0.032], 8, name=name + f"_Digit{i}a", mat=mats["wingbone"]))
        objs.append(ellipsoid_obj(name + f"_Joint{i}", j, (0.036, 0.036, 0.036), mats["wingbone"], segs=(10, 6)))
        tip2 = t_ + (t_ - j).normalized() * 0.1
        objs.append(sweep([j, lerpv(j, t_, 0.5), t_, tip2], [0.032, 0.024, 0.013, 0.0], 8, name=name + f"_Digit{i}b",
                          mat=mats["wingbone"]))
    bm = bmesh.new()
    ev, bv = [], []
    hint = Vector((0.3 * sx, 0.2, 1.0))
    for i in range(len(fingers) - 1):
        d3_membrane_panel(bm, fingers[i], fingers[i + 1], 0.3, -0.12, hint, ev, bv)
    d3_membrane_panel(bm, fingers[-1], [W, E, S] + flank, 0.2, -0.1, hint, ev, bv, nU=14, nT=18)
    d3_membrane_panel(bm, [S, lerpv(S, W, 0.5), W], [S, E, W], 0.0, 0.0, Vector((0, 1, 0.3)), ev, bv, nU=6, nT=8, ripple=0.0)
    mem = bm_to_obj(bm, name + "_Membrane", mats["membrane"], {"edge": ev, "bonefac": bv})
    md = mem.modifiers.new("Solid", "SOLIDIFY")
    md.thickness = 0.018
    md.offset = 0.0
    objs.append(mem)
    objs.append(d3_claw(name + "_ThumbClaw", W + Vector((0.06 * sx, 0.34, 0.2)), W, 0.24, 0.042, mats["claw"], ground=False))
    # elbow spur (a short horn off the elbow point) and a row of keeled scutes down the top of the humerus and forearm,
    # overlapping toward the wrist like limb scales
    ept = E + ((E - S).normalized() + (E - W).normalized()).normalized() * 0.12
    objs.append(spike(name + "_ElbowSpur", ept, (ept - E).normalized() - Vector((0, 0, 0.25)), 0.3, 0.06, mats["horn"],
                      curve=0.15, up=Vector((0, 0, -1))))
    top = d3_wing_top(sx)
    abvh = BVHTree.FromPolygons([tuple(v) for v in vcoords(arm.data)], [tuple(p.vertices) for p in arm.data.polygons])
    k = 0
    for a_, b_, n_, sa, sb in ((S, E, 3, 0.24, 0.17), (E, W, 6, 0.22, 0.14)):
        for i in range(n_):
            t = (i + 0.6) / (n_ + 0.2)
            p = lerpv(a_, b_, t)
            ob = d3_scute(abvh, f"{name}_ArmScute{k:02d}", p + top * 1.0, -top, sa * (1.0 - 0.25 * t), sb * (1.0 - 0.25 * t),
                          mats["plate"], keel=0.02, tilt=0.018, dvec=(b_ - a_).normalized(), nu=6, nv=5, thick=0.025)
            if ob is not None:
                objs.append(ob)
                k += 1
    return objs


def ellipsoid_axes(name, c, axes, rad, mat, segs=(16, 10)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs[0], v_segments=segs[1], radius=1.0)
    e1, e2, e3 = axes
    M = Matrix(((e1.x * rad[0], e2.x * rad[1], e3.x * rad[2], c[0]),
                (e1.y * rad[0], e2.y * rad[1], e3.y * rad[2], c[1]),
                (e1.z * rad[0], e2.z * rad[1], e3.z * rad[2], c[2]),
                (0, 0, 0, 1)))
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm_to_obj(bm, name, mat)


def d3_claw(name, t, m, Lc, r, mat, ground=True):
    """Curved claw continuing the toe (m -> t); with ground=True the tip hooks down into the ground."""
    t, m = Vector(t), Vector(m)
    dv = (t - m).normalized()
    if ground:
        fw = Vector((dv.x, dv.y, 0)).normalized()
        tip = t + fw * (Lc * 0.8)
        tip.z = 0.006
        p1 = t + dv * (Lc * 0.4)
        p2 = tip + Vector((0, 0, Lc * 0.32)) - fw * (Lc * 0.04)
    else:
        tip = t + dv * Lc - Vector((0, 0, Lc * 0.25))
        p1 = t + dv * (Lc * 0.45)
        p2 = t + dv * (Lc * 0.85) - Vector((0, 0, Lc * 0.05))
    pts = bezier3(t - dv * 0.03, p1, p2, tip, 7)
    return sweep(pts, [r * (1 - i / 6) ** 0.8 for i in range(7)], 8, name=name, mat=mat)


def d3_dorsal_height(y):
    prof = [(-7.6, 0.02), (-6.5, 0.045), (-4.5, 0.08), (-2.8, 0.12), (-1.9, 0.16), (-1.0, 0.13), (0.1, 0.17),
            (0.9, 0.2), (1.7, 0.15), (2.6, 0.1), (3.4, 0.06)]
    return float(np.interp(y, [p[0] for p in prof], [p[1] for p in prof]))


def drake3_parts(mats, bvh):
    parts = []
    C = mats["claw"]
    d, u = d3_head_frame()
    X = Vector((1, 0, 0))
    for s in (1, -1):
        sd = "L" if s > 0 else "R"
        # main horns sweep back from the skull corners along the neck with a slight lift at the tips; cheek horns below
        pts = bezier3(HP(0.42, 0.24 * s, 0.25), HP(-0.15, 0.42 * s, 0.42), HP(-0.8, 0.55 * s, 0.3), HP(-1.45, 0.64 * s, 0.42), 18)
        parts.append((sweep(pts, [HR(0.16) * min(1.0, 0.5 + i * 0.25) * (1 - i / 17) ** 0.8 for i in range(18)], 14, name=f"D3_Horn{sd}", mat=mats["horn"]), "head"))
        pts = bezier3(HP(0.24, 0.44 * s, -0.04), HP(-0.12, 0.66 * s, -0.1), HP(-0.45, 0.76 * s, -0.17), HP(-0.75, 0.82 * s, -0.1), 10)
        parts.append((sweep(pts, [HR(0.1) * min(1.0, 0.5 + i * 0.25) * (1 - i / 9) ** 0.9 for i in range(10)], 10, name=f"D3_Horn2{sd}", mat=mats["horn"]), "head"))
        # three short spines along the back edge of the jaw angle, raking back
        for j, (t_, ln) in enumerate(((0.2, 0.14), (0.55, 0.18), (0.9, 0.22))):
            base = HP(0.05 + 0.35 * t_, 0.35 * s, -0.4 - 0.32 * t_)
            parts.append((spike(f"D3_JawSpine{j}{sd}", base, -d - u * 0.45 + X * (0.35 * s), HR(ln), HR(0.045), mats["horn"],
                                curve=0.12, up=u), "jaw"))
        # two bony knobs on the outer slope of the brow ridge, raking back (supraorbital tubercles)
        for j, (sv, ln) in enumerate(((0.52, 0.13), (0.36, 0.1))):
            parts.append((spike(f"D3_BrowKnob{j}{sd}", HP(sv, 0.4 * s, 0.33), -d * 0.8 + X * (0.45 * s) + u * 0.35, HR(ln), HR(0.045),
                                mats["horn"], curve=0.1, up=u), "head"))
        # small almond eye deep under the brow, slanted (front corner low), looking forward-out; lids are in the SDF.
        # A thin vertical slit pupil sits on its outer surface.
        ec, out, lng, up = d3_eye_frame(s)
        ro, rl, ru = HR(*D3_EYE_RAD)
        parts.append((ellipsoid_axes(f"D3_Eye{sd}", ec, (out, lng, up), (ro, rl, ru), mats["eye"], segs=(16, 10)), "head"))
        parts.append((ellipsoid_axes(f"D3_Pupil{sd}", ec + out * (ro * 0.9), (out, lng, up), (ro * 0.2, rl * 0.16, ru * 0.82),
                                     mats["pupil"], segs=(10, 8)), "head"))
        # teeth: varied, curved back, tips hanging over the lower jaw (overbite); big canine + lower fang in its notch
        for k, (sv, ln) in enumerate(((0.58, 0.06), (0.7, 0.075), (0.82, 0.07), (0.94, 0.095), (1.06, 0.075), (1.18, 0.1),
                                      (1.3, 0.085), (1.44, 0.19), (1.55, 0.085), (1.7, 0.11))):
            base = HP(sv, (d3_lip_x(sv) - 0.03) * s, -0.2)
            parts.append((spike(f"D3_ToothU{k}{sd}", base, -u + X * (0.18 * s) - d * 0.1, HR(ln + 0.02), HR(0.022 + ln * 0.13),
                                mats["teeth"], curve=0.25, up=-d), "head"))
        base = HP(1.6, (d3_jaw_x(1.6) - 0.005) * s, -0.24)
        parts.append((spike(f"D3_FangL{sd}", base, u + X * (0.25 * s) + d * 0.04, HR(0.19), HR(0.04), mats["teeth"], curve=0.2, up=-d),
                      "jaw"))
        # lower tooth row just inside the upper one: hidden in the closed mouth, bared when the jaw opens
        for k, (sv, ln) in enumerate(((0.7, 0.05), (0.84, 0.065), (0.98, 0.055), (1.12, 0.07), (1.26, 0.06), (1.4, 0.075),
                                      (1.52, 0.06))):
            base = HP(sv, (d3_jaw_x(sv) - 0.04) * s, -0.235)
            parts.append((spike(f"D3_ToothL{k}{sd}", base, u + X * (0.08 * s) + d * 0.05, HR(ln + 0.02), HR(0.018 + ln * 0.12),
                                mats["teeth"], curve=0.15, up=-d), "jaw"))
        # claws: curved, hooked into the ground from every toe; dewclaws/halluces smaller
        for bone, base, spec, Lc, r in (("chest", D3_FRONT["kn"], D3_FTOES, 0.31, 0.084), ("root", D3_BACK["ball"], D3_BTOES, 0.34, 0.09)):
            bb = Vector((base[0] * s, base[1], base[2]))
            for c, (L, ox) in enumerate(zip(spec["len"], spec["off"])):
                b0, m, t = d3_toe(bb, L, ox * s)
                parts.append((d3_claw(f"D3_Claw{bone}{c}{sd}", t, m, Lc, r, C), bone))
        wr = Vector((D3_FRONT["wr"][0] * s, D3_FRONT["wr"][1], D3_FRONT["wr"][2]))
        a_, b_ = wr + Vector((-0.14 * s, 0.0, -0.12)), wr + Vector((-0.21 * s, 0.14, -0.3))
        parts.append((d3_claw(f"D3_Dewclaw{sd}", b_, a_, 0.13, 0.045, C, ground=False), "chest"))
        ball = Vector((D3_BACK["ball"][0] * s, D3_BACK["ball"][1], D3_BACK["ball"][2]))
        a_, b_ = ball + Vector((-0.08 * s, -0.07, 0.05)), ball + Vector((-0.15 * s, -0.32, -0.04))
        parts.append((d3_claw(f"D3_Hallux{sd}", b_, a_, 0.17, 0.05, C), "root"))
    # dorsal blades: overlapping, swept back, graduated (neck -> shoulder peak -> back -> hips -> tail tip)
    y = D3_HEAD_B.y - 0.45
    i = 0
    while y > -2.9:                                   # central crest stops at the hips; paired scutes run on
        hgt = d3_dorsal_height(y)
        hit = bvh.ray_cast(Vector((0, y, 12)), Vector((0, 0, -1)))
        L = max(0.16, hgt * 3.0)                       # long low scutes, each overlapping the next by ~45%
        step = max(0.11, L * 0.55)
        if hit[0] is not None:
            loc, nrm = hit[0], hit[1]
            T = 0.02 + hgt * 0.1
            f, uu, sv = basis_from(Vector((0, 1, 0)), nrm)
            pts = [loc + f * (math.cos(2 * math.pi * a / 12) * L * 0.5) + sv * (math.sin(2 * math.pi * a / 12) * T) - uu * 0.06
                   for a in range(12)]
            pts += [loc + uu * hgt - f * (L * 0.55), loc + uu * (hgt * 0.5) + f * (L * 0.12) + sv * (T * 0.3),
                    loc + uu * (hgt * 0.5) + f * (L * 0.12) - sv * (T * 0.3)]
            ob = hull_obj(pts, f"D3_Plate{i:02d}", mats["plate"],
                          lambda co, loc=loc, uu=uu, hgt=hgt: {"ph": max(0.0, min(1.0, (co - loc).dot(uu) / hgt)),
                                                               "wear": max(0.0, min(1.0, (co - loc).dot(uu) / hgt)) ** 3})
            bone = ("neck2" if y > 2.4 else "neck" if y > 1.35 else "chest" if y > 0.0 else "root" if y > -2.5
                    else f"tail{min(5, int((-2.5 - y) / 1.2) + 1)}")
            parts.append((ob, bone))
            i += 1
        y -= step
    # ember glow inside the closed mouth, seen only through the slit between the lips and the gaps between teeth
    bm = bmesh.new()
    rows, tv = [], []
    for i in range(13):
        sv = 0.55 + (1.62 - 0.55) * i / 12
        xw = d3_lip_x(sv) - 0.05
        rows.append([bm.verts.new(HP(sv, -xw, -0.212)), bm.verts.new(HP(sv, 0.0, -0.212)), bm.verts.new(HP(sv, xw, -0.212))])
        tv += [1.0 - i / 12] * 3
    for i in range(12):
        for k in range(2):
            bm.faces.new((rows[i][k], rows[i + 1][k], rows[i + 1][k + 1], rows[i][k + 1]))
    mg = bm_to_obj(bm, "D3_MouthGlow", mats["mouth"], {"t": tv})
    sol = mg.modifiers.new("Solid", "SOLIDIFY")          # a closed sliver bakes a consistent normal (single-sided: inverted)
    sol.thickness = 0.006
    sol.offset = 0.0
    parts.append((mg, "head"))
    return parts


# ---------------------------------------------------------------- drake v3: surface + colour pass (after anatomy approval)
# Holden (2026-10-04): scales and armour follow the anatomy - overlapping plates on the back and shoulders, finer scales
# at the joints, restrained wear, no random spikes or noisy all-over pattern. Palette: charcoal, dark crimson, muted bone;
# orange ember cracks only in a few deliberate places (throat furnace + chest, eyes, mouth seam); keep dark quiet areas.
D3_COLS = dict(char_dk="#141213", char_warm="#2a2221", crimson_dk="#2c0d0e", belly="#3b1817", belly_hi="#4d211d",
               bone="#b2a489", bone_dk="#6c6253", ember="#ff4a0e", ember_hot="#ffb341")


def d3_shingle(t, co, vor, scale):
    """Overlapping-scale height: each Voronoi cell rises toward its back-bottom edge (scales overlap tailward/down)."""
    sc_ = t.node("ShaderNodeVectorMath")
    sc_.operation = "SCALE"
    t.link(co, sc_.inputs[0])
    sc_.inputs["Scale"].default_value = scale
    off = t.node("ShaderNodeVectorMath")
    off.operation = "SUBTRACT"
    t.link(sc_.outputs[0], off.inputs[0])
    t.link(vor.outputs["Position"], off.inputs[1])
    dp = t.node("ShaderNodeVectorMath")
    dp.operation = "DOT_PRODUCT"
    t.link(off.outputs[0], dp.inputs[0])
    dp.inputs[1].default_value = (0.0, -0.45, -0.89)
    return t.maprange(dp.outputs["Value"], -0.45, 0.45, 0.0, 1.0)


def d3_ao_mul(t, col, dist=0.4, lo=0.4):
    aof = t.maprange(t.ao(dist), 0.0, 1.0, lo, 1.0)
    return t.mix(1.0, col, t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")


def drake3_materials():
    C = D3_COLS
    mats = {}
    # --- skin: anatomical scales (big over back/flanks, fine at joints and face), ventral scutes, crimson seams
    m, t = new_mat("D3_Skin")
    if t:
        co0 = t.objco()
        stretch = t.node("ShaderNodeVectorMath")                  # scales elongated along the body axis, not round dots
        stretch.operation = "MULTIPLY"
        t.link(co0, stretch.inputs[0])
        stretch.inputs[1].default_value = (1.0, 0.72, 1.0)
        co = stretch.outputs[0]
        dors = t.maprange(t.attr("dors"), 0.1, 0.75, 0.0, 1.0)
        vent = t.maprange(t.attr("vent"), 0.35, 0.6, 0.0, 1.0)
        fine = t.math("MAXIMUM", t.attr("joint"), t.attr("face"), clamp=True)
        coarse = t.math("SUBTRACT", 1.0, fine)
        vb, vf = t.voronoi(co, 6.0), t.voronoi(co, 13.0)

        def blend(a, b):
            return t.math("ADD", t.math("MULTIPLY", a, coarse), t.math("MULTIPLY", b, fine))

        # seams from distance-to-EDGE (thin lines between cells). F1 distance (to the cell's feature point) made wide dark
        # rings around round light centres - that was the polka-dot look
        veb, vef = t.voronoi(co, 6.0, "DISTANCE_TO_EDGE"), t.voronoi(co, 13.0, "DISTANCE_TO_EDGE")
        seam = t.maprange(blend(veb.outputs["Distance"], vef.outputs["Distance"]), 0.0, 0.07, 1.0, 0.0)
        sh = blend(d3_shingle(t, co, vb, 6.0), d3_shingle(t, co, vf, 13.0))
        sepb, sepf = t.node("ShaderNodeSeparateColor"), t.node("ShaderNodeSeparateColor")
        t.link(vb.outputs["Color"], sepb.inputs[0])
        t.link(vf.outputs["Color"], sepf.inputs[0])
        crand = blend(sepb.outputs[0], sepf.outputs[0])
        ndors, nvent = t.math("SUBTRACT", 1.0, dors), t.math("SUBTRACT", 1.0, vent)
        col = t.mix(dors, hexcol(C["char_warm"]), hexcol(C["char_dk"]))                      # charcoal back, warmer flanks
        lowflank = t.maprange(t.math("MULTIPLY", ndors, nvent), 0.72, 1.0, 0.0, 1.0)
        lowflank = t.math("MULTIPLY", lowflank, t.maprange(t.attr("face"), 0.3, 0.9, 1.0, 0.25))     # keep the face charcoal
        col = t.mix(t.math("MULTIPLY", lowflank, 0.55), col, hexcol("#3d0f0e"))             # dark crimson low on the flanks
        # per-scale value: darken-only and multiplicative - on near-black skin a mix toward grey made some cells ~25%
        # brighter (the grey blotches); seams must stay darker than the darkest charcoal or they glow
        col = t.mix(1.0, col, t.mix(crand, (0.84, 0.84, 0.84, 1.0), (1.0, 1.0, 1.0, 1.0)), blend="MULTIPLY")
        col = t.mix(t.math("MULTIPLY", seam, 0.55), col, hexcol("#0d0505"))                  # near-black crimson seams
        # ventral scutes: transverse bands along the belly line
        bandc = t.math("SINE", t.math("MULTIPLY", t.attr("vs"), 2 * math.pi / 0.15))
        bseam = t.maprange(bandc, 0.75, 1.0, 0.0, 1.0)
        bdome = t.maprange(bandc, 1.0, -1.0, 0.0, 1.0)
        vcol = t.mix(t.math("MULTIPLY", bdome, 0.6), hexcol(C["belly"]), hexcol(C["belly_hi"]))
        vcol = t.mix(bseam, vcol, hexcol("#1a0909"))
        col = t.mix(vent, col, vcol)
        # (no wear on the skin itself: pointiness scuffs read as grey leopard blotches; wear lives on plates/horns/claws)
        # ember: only inside the 'ember' mask (throat furnace + chest), glowing in the seams between ventral scutes
        em = t.attr("ember")
        epatch = t.maprange(t.noise(co, 1.6, 2.0, 0.5).outputs["Fac"], 0.4, 0.55, 0.0, 1.0)
        ember = t.math("MULTIPLY", t.math("MULTIPLY", t.math("MULTIPLY", bseam, vent), em), epatch)
        hot = t.maprange(bandc, 0.93, 1.0, 0.0, 1.0)
        col = t.mix(ember, col, hexcol("#120403"))
        # mouth interior: wet dark-crimson flesh, no scales (only seen when the jaw opens)
        mouth = t.maprange(t.attr("mouth"), 0.3, 0.8, 0.0, 1.0)
        fleshn = t.noise(co, 9.0, 3.0, 0.6)
        flesh = t.mix(t.maprange(fleshn.outputs["Fac"], 0.35, 0.65, 0.0, 1.0), hexcol("#3a0b0d"), hexcol("#5a161a"))
        col = t.mix(mouth, col, flesh)
        col = d3_ao_mul(t, col, 0.4, 0.4)
        ecol = t.mix(t.math("MULTIPLY", hot, em), hexcol(C["ember"]), hexcol(C["ember_hot"]))
        # each scale: a rounded dome (from the F1 distance - fine for height, never for colour) tilted by the shingle slope
        dome = t.maprange(blend(vb.outputs["Distance"], vf.outputs["Distance"]), 0.0, 0.75, 1.0, 0.0)
        scale_h = t.math("MULTIPLY", t.math("ADD", t.math("MULTIPLY", dome, 0.6), t.math("MULTIPLY", sh, 0.4)),
                         t.math("SUBTRACT", 1.0, t.math("MULTIPLY", seam, 0.9)))
        height = t.math("ADD", t.math("MULTIPLY", scale_h, nvent),
                        t.math("MULTIPLY", t.math("SUBTRACT", bdome, t.math("MULTIPLY", bseam, 0.8)), t.math("MULTIPLY", vent, 0.6)))
        height = t.math("ADD", t.math("MULTIPLY", height, t.math("SUBTRACT", 1.0, mouth)),
                        t.math("MULTIPLY", fleshn.outputs["Fac"], t.math("MULTIPLY", mouth, 0.3)))
        rough = t.math("ADD", t.math("MULTIPLY", t.maprange(seam, 0.0, 1.0, 0.58, 0.82), t.math("SUBTRACT", 1.0, mouth)),
                       t.math("MULTIPLY", mouth, 0.28))
        t.bsdf(col, rough=rough, spec=0.3, normal=t.bump(height, 0.22, 0.025),
               emit_col=ecol, emit_str=t.math("MULTIPLY", ember, 2.6))
    mats["skin"] = m
    # --- plates (dorsal crest, paired scutes, shoulder pauldron): charcoal keratin, growth lines, chipped bone rims
    m, t = new_mat("D3_Plate")
    if t:
        co = t.objco()
        ph, wr = t.attr("ph"), t.attr("wear")
        nz = t.noise(co, 7.0, 4.0, 0.6)
        col = t.ramp(ph, [(0.0, hexcol("#171415")), (0.55, hexcol("#211d1d")), (0.9, hexcol("#2f2928")), (1.0, hexcol("#3a3230"))])
        col = t.mix(t.maprange(nz.outputs["Fac"], 0.35, 0.65, 0.0, 0.25), col, hexcol("#2e2928"))
        rings = t.maprange(t.math("SINE", t.math("MULTIPLY", ph, 40.0)), 0.7, 1.0, 0.0, 1.0)
        col = t.mix(t.math("MULTIPLY", rings, 0.18), col, hexcol("#0b0909"))
        # chipped rims only in patches (every rim outlined in bone read like a comic outline)
        wpatch = t.maprange(t.noise(co, 3.2, 2.0, 0.6).outputs["Fac"], 0.52, 0.64, 0.0, 1.0)
        w = t.math("MULTIPLY", t.maprange(wr, 0.7, 1.0, 0.0, 1.0), wpatch)
        col = t.mix(t.math("MULTIPLY", w, 0.7), col, hexcol(C["bone"]))
        col = d3_ao_mul(t, col, 0.25, 0.45)
        # matte keratin, not lacquer: the first pass (rough 0.36 + coat) read as chrome under the studio rims
        t.bsdf(col, rough=t.maprange(nz.outputs["Fac"], 0.3, 0.7, 0.5, 0.66), spec=0.32,
               normal=t.bump(t.math("ADD", nz.outputs["Fac"], t.math("MULTIPLY", rings, -0.3)), 0.25, 0.01))
    mats["plate"] = m

    def keratin(name, stops, ridges=0.0, rough=0.5, sss=0.0):
        m_, t_ = new_mat(name)
        if t_:
            tt = t_.attr("t")
            co_ = t_.objco()
            c_ = t_.ramp(tt, [(p, hexcol(h)) for p, h in stops])
            nrm = None
            if ridges:
                rid = t_.math("MULTIPLY", t_.maprange(t_.math("SINE", t_.math("MULTIPLY", tt, ridges)), 0.55, 1.0, 0.0, 1.0),
                              t_.maprange(tt, 0.0, 0.7, 1.0, 0.2))
                c_ = t_.mix(t_.math("MULTIPLY", rid, 0.35), c_, hexcol("#0e0c0c"))
                nrm = t_.bump(t_.math("SUBTRACT", 1.0, rid), 0.3, 0.015)
            c_ = t_.mix(t_.maprange(t_.noise(co_, 14.0, 3.0, 0.6).outputs["Fac"], 0.4, 0.7, 0.0, 0.2), c_, hexcol("#3a332d"))
            c_ = d3_ao_mul(t_, c_, 0.25, 0.45)
            t_.bsdf(c_, rough=rough, spec=0.38, normal=nrm, sss=sss)
        return m_

    # horns/knobs/spines: charcoal base growing into worn muted bone at the tips, growth ridges near the base
    mats["horn"] = keratin("D3_Horn", [(0.0, "#141212"), (0.3, "#2a2422"), (0.62, "#5e5346"), (0.88, "#a39478"), (1.0, "#bcae93")],
                           ridges=60.0)
    mats["claw"] = keratin("D3_Claw", [(0.0, "#191615"), (0.5, "#4a4137"), (1.0, "#b8aa8e")], rough=0.45)
    mats["teeth"] = keratin("D3_Teeth", [(0.0, "#5a4e40"), (0.35, "#9d8f74"), (1.0, "#cbbd9f")], rough=0.42, sss=0.08)
    # --- membrane: thin dark crimson, darker along the bones and trailing edge, faint vein network, red when backlit
    m, t = new_mat("D3_Membrane")
    if t:
        co = t.objco()
        edge, bone = t.attr("edge"), t.attr("bonefac")
        col = t.mix(t.maprange(t.noise(co, 2.5, 3.0, 0.6).outputs["Fac"], 0.3, 0.7, 0, 1), hexcol("#2e0c0d"), hexcol("#42120f"))
        col = t.mix(t.math("MULTIPLY", bone, 0.8), col, hexcol("#1a0708"))
        col = t.mix(t.maprange(edge, 0.85, 1.0, 0.0, 0.7), col, hexcol("#160606"))
        vein = t.maprange(t.voronoi(co, 3.5, "DISTANCE_TO_EDGE").outputs["Distance"], 0.0, 0.02, 1.0, 0.0)
        col = t.mix(t.math("MULTIPLY", vein, 0.4), col, hexcol("#140505"))
        col = d3_ao_mul(t, col, 0.3, 0.5)
        bs = t.bsdf(col, rough=0.55, spec=0.3)
        tr = t.node("ShaderNodeBsdfTranslucent")
        tr.inputs["Color"].default_value = hexcol("#8a1a12")
        mixs = t.node("ShaderNodeMixShader")
        mixs.inputs[0].default_value = 0.3
        out = t.n.get("Material Output")
        t.link(bs.outputs[0], mixs.inputs[1])
        t.link(tr.outputs[0], mixs.inputs[2])
        t.link(mixs.outputs[0], out.inputs["Surface"])
    mats["membrane"] = m
    mats["wingbone"] = mat_simple("D3_WingBone", "#1a1717", rough=0.58, spec=0.32)
    mats["eye"] = mat_simple("D3_Eye", "#FF7A14", rough=0.1, spec=0.8, emit="#FF8A1E", estr=4.5, aodark=0.0)
    mats["pupil"] = mat_simple("D3_Pupil", "#090404", rough=0.1, spec=0.9, aodark=0.0)
    m, t = new_mat("D3_MouthGlow")
    if t:
        g = t.maprange(t.attr("t"), 0.35, 1.0, 0.0, 1.0)            # dark at the front of the mouth, warm at the back
        t.bsdf(hexcol("#1a0504"), rough=0.6, spec=0.2, emit_col=hexcol("#ff5a12"), emit_str=t.math("MULTIPLY", g, 0.9))
    mats["mouth"] = m
    return mats


def d3_skin_attrs(me, M=None, part="body"):
    """Zone masks for the skin shader on the body/jaw: vs (belly-line coordinate), vent (ventral scutes), dors (back),
    joint (fine scales at joints/folds/feet/tail tip), face (fine scales on the head), ember (throat furnace + chest),
    mouth (flesh inside the mouth). With a pose M, head/jaw vertices are mapped back to rest space through their bone so
    the head masks stay put when the head or jaw moves."""
    v = vcoords(me)
    n = vnormals(me)
    if M is not None:
        def to_rest(mask, Mb):
            Mi = np.array(Mb.inverted(), np.float32)
            v[mask] = v[mask] @ Mi[:3, :3].T + Mi[:3, 3]
            nn = n[mask] @ Mi[:3, :3].T
            n[mask] = nn / np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
        if part == "jaw":
            to_rest(np.ones(len(v), bool), M["jaw"])
        else:
            hcp = np.array(tuple(M["head"] @ HP(0.9, 0, 0.0)), np.float32)
            to_rest(np.linalg.norm(v - hcp, axis=1) < HR(1.5), M["head"])
    x, y, z = v[:, 0], v[:, 1], v[:, 2]
    nx, ny, nz = n[:, 0], n[:, 1], n[:, 2]
    ax = np.abs(x)

    def cl(a):
        return np.clip(a, 0.0, 1.0).astype(np.float32)

    pts = [HP(1.75, 0, -0.42), HP(1.0, 0, -0.56), HP(0.4, 0, -0.68), Vector((0, 2.15, 2.5)), Vector((0, 1.85, 2.0)),
           Vector((0, 1.0, 1.58)), Vector((0, 0.0, 1.95)), Vector((0, -1.05, 2.42)), Vector((0, -2.05, 2.52))]
    pts += [Vector((0, p[1], p[2] - r * 0.92)) for p, r in D3_TAIL]
    vs = polyline_param(v, [np.array(tuple(p), np.float32) for p in pts])
    tail_r = np.interp(-y, [-p[0][1] for p in D3_TAIL], [p[1] for p in D3_TAIL])
    width = np.where(y < -2.5, 0.12 + 0.35 * tail_r, 0.34)
    under = cl((-nz - 0.12) / 0.35) * cl(1.0 - (ax - width) / 0.14)
    # throat/chest front faces forward but never up (the lowered neck's top also faces forward)
    throat = cl((ny - 0.3) / 0.3) * cl((0.15 - nz) / 0.3) * cl(1.0 - (ax - 0.26) / 0.12) * ((y > 1.3) & (z > 1.5)).astype(np.float32)
    vent = np.maximum(under, throat)
    vent[(z < 1.35) & (ax > 0.45)] = 0.0
    vent[(ax > 0.55) & (y > -2.4)] = 0.0
    dors = cl((nz + 0.05) / 0.6) * (1.0 - vent)
    joint = np.zeros(len(v), np.float32)
    J = [(D3_FRONT["el"], 0.34), (D3_FRONT["wr"], 0.28), (D3_FRONT["kn"], 0.38), (D3_BACK["knee"], 0.34), (D3_BACK["hock"], 0.3),
         (D3_BACK["ball"], 0.4), ((0.85, 1.45, 2.2), 0.35), ((0.75, -1.45, 2.3), 0.35), ((0.42, 1.8, 3.05), 0.4)]
    for c, r in J:
        for sx in (1, -1):
            cc = np.array((c[0] * sx, c[1], c[2]), np.float32)
            joint = np.maximum(joint, cl(1.0 - np.linalg.norm(v - cc, axis=1) / r))
    joint = np.maximum(joint, cl((-7.0 - y) / 1.0))
    hc = np.array(tuple(HP(0.9, 0, 0.0)), np.float32)
    face = cl(1.0 - (np.linalg.norm(v - hc, axis=1) - HR(1.0)) / 0.35)
    # the top of the skull, brow and muzzle keeps the large scales (bigger plates read as bone); fine scales on the sides
    hd, hu = d3_head_frame()
    top = cl((n @ np.array(tuple(hu), np.float32) - 0.25) / 0.45)
    face = face * (1.0 - top)
    hb = float(D3_HEAD_B.y)
    # ember: a narrow strip down the throat to the upper chest (the fire gland showing between ventral scutes)
    ember = vent * cl(1.0 - (ax - 0.08) / 0.16) * cl((y - 1.7) / 0.35) * cl((hb + 0.45 - y) / 0.45)
    chest = cl((ny - 0.35) / 0.3) * cl((0.2 - nz) / 0.3) * cl(1.0 - (ax - 0.08) / 0.16) * cl(1.0 - np.abs(y - 1.95) / 0.3) * \
        cl(1.0 - np.abs(z - 2.2) / 0.4)
    ember = np.maximum(ember, chest)
    # mouth interior (rest head-local coords): palate vault on the upper skull, trough + tongue on the jaw
    hb_, hu_ = np.array(tuple(D3_HEAD_B), np.float32), np.array(tuple(hu), np.float32)
    hd_ = np.array(tuple(hd), np.float32)
    s_l = ((v - hb_) @ hd_) / D3_HEAD_SCALE
    w_l = ((v - hb_) @ hu_) / D3_HEAD_SCALE
    x_l = ax / D3_HEAD_SCALE
    nu_ = n @ hu_
    if part == "jaw":
        lim = np.interp(s_l, [0.4, 1.0, 1.66], [0.4, 0.31, 0.15]) - 0.045
        mouth = cl((w_l + 0.34) / 0.03) * cl((lim - x_l) / 0.03) * cl((s_l - 0.42) / 0.06) * cl((1.7 - s_l) / 0.06) * cl((nu_ - 0.1) / 0.3)
    else:
        lim = np.interp(s_l, [0.4, 0.9, 1.42, 1.75], [0.42, 0.37, 0.25, 0.18]) - 0.05
        mouth = cl((-0.12 - w_l) / 0.03) * cl((w_l + 0.25) / 0.03) * cl((lim - x_l) / 0.03) * cl((s_l - 0.48) / 0.06) * \
            cl((1.76 - s_l) / 0.06) * cl((-nu_ - 0.1) / 0.3)
    ember = ember * (1.0 - mouth)
    for k_, a_ in (("vs", vs), ("vent", vent), ("dors", dors), ("joint", joint), ("face", face), ("ember", ember),
                   ("mouth", mouth)):
        set_point_attr(me, k_, a_)


def d3_scute(bvh, name, origin, direction, a, b, mat, keel=0.035, tilt=0.03, dvec=Vector((0, -1, 0)), nu=7, nv=5, thick=0.035,
             dome=0.0, shape="scute"):
    """Keeled scute hugging the body: a grid raycast onto the surface, front edge tucked in, trailing edge lifted (so a row
    shingles like roof tiles), sharp keel along its length. Attributes: ph (keel 0..1), wear (rim + trailing tip).
    shape="shield" gives a rounded armour-plate outline; dome lifts the middle so big plates read curved, not flat."""
    hit = bvh.ray_cast(Vector(origin), Vector(direction))
    if hit[0] is None:
        return None
    loc, nrm = hit[0], hit[1]
    d1 = (dvec - nrm * dvec.dot(nrm)).normalized()
    d2 = nrm.cross(d1).normalized()
    bm = bmesh.new()
    grid, phs, wears = [], [], []
    for i in range(nu):
        u = -1.0 + 2.0 * i / (nu - 1)
        if shape == "shield":
            half_w = math.sqrt(max(0.02, 1.0 - 0.8 * max(u, 0.0) ** 2)) * math.sqrt(max(0.02, 1.0 - 0.6 * max(-u, 0.0) ** 2))
        else:
            half_w = (1.0 - 0.45 * max(u, 0.0) ** 2.2) * (1.0 - 0.2 * max(-u, 0.0) ** 2)  # squarish, blunt-tipped scute
        row = []
        for k in range(nv):
            v = (-1.0 + 2.0 * k / (nv - 1)) * half_w
            p0 = loc + d1 * (u * a * 0.5) + d2 * (v * b * 0.5)
            h = bvh.ray_cast(p0 + nrm * 0.8, -nrm, 2.0)
            sp, sn = (p0, nrm) if h[0] is None else (h[0], h[1])
            vn = abs(v / max(half_w, 1e-3))
            kl = 1.0 - vn ** 1.3
            lift = 0.012 + tilt * (u + 1.0) * 0.5 + keel * kl * (0.6 + 0.4 * (1.0 - u * u)) + \
                dome * (1.0 - vn * vn) * math.sqrt(max(0.0, 1.0 - 0.7 * u * u))
            row.append(bm.verts.new(sp + sn * lift))
            phs.append(kl)
            wears.append(max(vn ** 3, max(u, 0.0) ** 4))
        grid.append(row)
    for i in range(nu - 1):
        for k in range(nv - 1):
            bm.faces.new((grid[i][k], grid[i + 1][k], grid[i + 1][k + 1], grid[i][k + 1]))
    # rim: the boundary extruded down into the body. No bottom face - it is never visible, and on the game mesh the hidden
    # undersides of ~150 plates were eating a big share of the 1024 texture
    ret = bmesh.ops.extrude_edge_only(bm, edges=[e for e in bm.edges if e.is_boundary])
    for v in [g for g in ret["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co -= nrm * thick
        phs.append(0.0)
        wears.append(1.0)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    f0 = bm.faces[(nu - 1) * (nv - 1) // 2]
    f0.normal_update()
    if f0.normal.dot(nrm) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    ob = bm_to_obj(bm, name, mat, {"ph": phs, "wear": wears}, smooth=True)
    md2 = ob.modifiers.new("Bevel", "BEVEL")
    md2.width = min(0.012, thick * 0.3)
    md2.segments = 2
    md2.limit_method = "ANGLE"
    return ob


def d3_tail_r(y):
    return float(np.interp(-y, [-p[0][1] for p in D3_TAIL], [p[1] for p in D3_TAIL]))


def d3_scute_rows(y):
    """[(length, width, lateral offset, keel), ...] for the scute rows at y on one side: one row on the neck and tail,
    two staggered rows over the back and shoulders (crocodile-style osteoderm armour)."""
    if y > 1.4:
        return [(0.22, 0.19, 0.19, 0.028)]
    if y > -2.5:
        k = max(0.0, 1.0 - abs(y - 0.8) / 1.0)
        a = 0.29 + 0.04 * k
        return [(a, a * 0.88, 0.21, 0.035), (a * 0.82, a * 0.75, 0.46, 0.028)]
    r = d3_tail_r(y)
    a = 0.08 + 0.42 * r
    return [(a, a * 0.8, 0.02 + 0.5 * r, 0.012 + 0.045 * r)]


def d3_bone_for(y):
    return ("neck2" if y > 2.4 else "neck" if y > 1.35 else "chest" if y > 0.0 else "root" if y > -2.5
            else f"tail{min(5, int((-2.5 - y) / 1.2) + 1)}")


def d3_surface_parts(bvh, mats):
    """Armour that follows the anatomy: paired keeled scute rows either side of the spine (neck -> tail tip) and a
    three-plate pauldron down each scapula."""
    parts = []
    P = mats["plate"]
    for s in (1, -1):
        sd = "L" if s > 0 else "R"
        y, i = D3_HEAD_B.y - 0.5, 0
        while y > -8.4:
            rows = d3_scute_rows(y)
            for r_, (a, b, xo, keel) in enumerate(rows):
                yy = y - r_ * rows[0][0] * 0.39                     # outer row staggered half a scute back
                ob = d3_scute(bvh, f"D3_Scute{sd}{i:03d}", (xo * s, yy, 12.0), (0, 0, -1), a, b, P, keel=keel, tilt=0.6 * keel,
                              dvec=Vector((0.0, -1.0, -0.1)))
                if ob is not None:
                    parts.append((ob, d3_bone_for(yy)))
                    i += 1
            y -= rows[0][0] * 0.78
        # pauldron: four domed shield plates cascading down the scapula onto the deltoid, each tucked under the one above
        for j, (yy, zz, a, b) in enumerate(((0.95, 3.82, 0.56, 0.48), (1.15, 3.44, 0.52, 0.45), (1.34, 3.06, 0.46, 0.4),
                                            (1.5, 2.7, 0.38, 0.33))):
            ob = d3_scute(bvh, f"D3_Shoulder{sd}{j}", (3.0 * s, yy, zz), (-s, 0, 0), a, b, P, keel=0.045, tilt=0.06,
                          dvec=Vector((0.0, -0.35, -1.0)), nu=9, nv=8, thick=0.05, dome=0.05, shape="shield")
            if ob is not None:
                parts.append((ob, "chest"))
    return parts


def d3_head_plates(bvh, jbvh, mats):
    """Larger bony plates on the head: brow crest, nasal ridges, crown, cheekbones and lower jaw (overlapping backward)."""
    parts = []
    P = mats["plate"]
    d, u = d3_head_frame()
    X = Vector((1, 0, 0))

    def brow_x(s_):
        return float(np.interp(s_, [0.33, 0.72, 1.1], [0.33, 0.32, 0.22]))

    def nose_x(s_):
        return float(np.interp(s_, [0.98, 1.55], [0.135, 0.105]))

    def add(name, tree, origin, direction, a, b, keel, bone, nu=6, nv=5):
        ob = d3_scute(tree, name, origin, direction, HR(a), HR(b), P, keel=HR(keel), tilt=HR(keel * 0.7), dvec=-d, nu=nu, nv=nv,
                      thick=HR(0.022))
        if ob is not None:
            parts.append((ob, bone))

    for j, s_ in enumerate((0.85, 0.63, 0.42, 0.22)):
        add(f"D3_CrownPlate{j}", bvh, HP(s_, 0.0, 1.5), -u, 0.17, 0.15, 0.018, "head")
    for side in (1, -1):
        sd = "L" if side > 0 else "R"
        for j, s_ in enumerate((0.95, 0.74, 0.52)):
            add(f"D3_BrowPlate{sd}{j}", bvh, HP(s_, brow_x(s_) * side, 1.5), -u, 0.2, 0.15, 0.02, "head")
        for j, s_ in enumerate((1.5, 1.3, 1.1)):
            add(f"D3_NosePlate{sd}{j}", bvh, HP(s_, nose_x(s_) * side, 1.5), -u, 0.15, 0.1, 0.014, "head")
    # (cheek and jaw plates were tried and removed: on the steep sides they read as stuck-on buttons; the jaw stays quiet)
    return parts


def render_drake3_colour(sets):
    """Surface + colour review: hero 3/4, side, front, head, back detail, throat. 'fast' = quick preview."""
    fast = "fast" in sets
    reset()
    setup_render(samples=48 if fast else 192)
    mats = drake3_materials()
    rig = drake3_rig()
    objs = build_drake3({}, mats, rig)
    sc = bpy.context.scene
    sc.render.film_transparent = False
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexcol("#26282c")
    bg.inputs["Strength"].default_value = 0.5
    floor_m = mat_simple("D3_Floor", "#303236", rough=0.92, spec=0.2, aodark=0.0)
    me = bpy.data.meshes.new("Floor")
    me.from_pydata([(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)])
    me.materials.append(floor_m)
    link(bpy.data.objects.new("Floor", me))
    mn, mx = world_bbox(objs)
    c = (mn + mx) / 2
    R = (mx - mn).length / 2
    studio_lights(c, R, warm="#fff3e2", rim1="#eef2ff", rim2="#ffd8b0", fill="#e6ebf2", scale=float(sets_value(sets, "light", 1.2)))
    cam = camera()
    out = os.path.join(OUT, "review")
    os.makedirs(out, exist_ok=True)
    tag = "_fast" if fast else ""
    W_, H_ = 1600, 1000
    d34 = Vector((0.62, 0.78, 0.28)).normalized()
    half = math.atan(18.0 * H_ / W_ / 40.0)
    persp_view(cam, c + d34 * (R / math.sin(half) * 0.6), c + Vector((0, 0.3, -0.5)), lens=40)
    render_to(os.path.join(out, f"drake3_col_hero{tag}.png"), W_, H_)
    ppu = W_ / ((mx.y - mn.y) + 1.2)
    ortho_view(cam, "side", (0, c.y, (mx.z + mn.z) / 2), ppu, W_, H_)
    render_to(os.path.join(out, f"drake3_col_side{tag}.png"), W_, H_)
    ortho_view(cam, "front", (0, 0, (mx.z + mn.z) / 2), min(ppu * 1.25, H_ / ((mx.z - mn.z) + 0.8)), W_, H_)
    render_to(os.path.join(out, f"drake3_col_front{tag}.png"), W_, H_)
    hc = HP(0.8, 0, -0.05)
    persp_view(cam, hc + Vector((3.6, 3.0, 1.0)), hc, lens=50)
    render_to(os.path.join(out, f"drake3_col_head{tag}.png"), 1200, 900)
    bc = Vector((0, -0.6, 3.4))
    persp_view(cam, bc + Vector((4.2, -4.6, 4.2)), bc, lens=42)
    render_to(os.path.join(out, f"drake3_col_back{tag}.png"), 1200, 900)
    tc = Vector((0, 2.6, 2.3))
    persp_view(cam, tc + Vector((2.2, 4.4, -1.4)), tc + Vector((0, 0, 0.1)), lens=40)
    render_to(os.path.join(out, f"drake3_col_throat{tag}.png"), 1200, 900)
    if not fast:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FantasyCreatures_drake3_colour.blend"))


# ---------------------------------------------------------------- drake v3: VFX previews + presentation-sheet renders
# Poses move only neck / neck2 / head / jaw / tail bones (see build_drake3). Sign convention: +X lifts the head,
# negative X opens the jaw and raises the tail.
D3_POSES = {
    "idle": {},
    "alert": {"neck": (14, 0, 0), "neck2": (10, 0, 0), "head": (6, 0, 0), "jaw": (-6, 0, 0), "tail1": (-10, 0, 0),
              "tail2": (-10, 0, 0), "tail3": (-8, 0, 0)},
    "roar": {"neck": (18, 0, 0), "neck2": (14, 0, 0), "head": (22, 0, 0), "jaw": (-40, 0, 0), "tail1": (-14, 0, 0),
             "tail2": (-10, 0, 0), "tail3": (-6, 0, 0)},
    "breath": {"neck": (-2, 0, 0), "neck2": (3, 0, 0), "head": (5, 0, 0), "jaw": (-28, 0, 0), "tail1": (-4, 0, 0)},
}


def d3_mouth(M):
    """Mouth opening and breath direction for a pose."""
    d, u = d3_head_frame()
    mouth = M["head"] @ HP(1.7, 0, -0.26)
    fwd = (M["head"].to_3x3() @ (d - u * 0.12)).normalized()
    return mouth, fwd


def d3_nostrils(M):
    return [M["head"] @ HP(1.74, 0.11 * s, 0.17) for s in (1, -1)]


def d3_lerp_hex(a, b, t):
    ca, cb = hexcol(a), hexcol(b)
    c = [ca[i] + (cb[i] - ca[i]) * t for i in range(3)]
    return "#%02x%02x%02x" % tuple(int(round(max(0.0, min(1.0, v)) ** (1 / 2.2) * 255)) for v in c)


D3_GLOW_TEX = os.path.normpath(os.path.join(OUT, "..", "DragonsHoard", "vfx", "Glow.png"))
D3_FLAME_TEX = os.path.join(OUT, "models", "CinderDrake", "CinderDrake_FlameFlip4x4.png")    # make_flame_flipbook()


def d3_fire_breath(mouth, fwd, cam_loc, seed=3, length=4.8):
    """Fire breath, mirroring models/CinderDrake/vfx_spec.json (v3): cards of our own flame flipbook
    (make_flame_flipbook, frames picked in OneShot order by age, random roll) tinted along a widening cone (white-yellow at
    the mouth, orange, then dark red), a Glow core at the lips, spark dots, smoke-flipbook cards in OneShot order off the
    far end, and a light. VFX_fire_flip4x4 is NOT used: its frames are torch flames cut flat at the base, which stacked
    into a hard-edged slab at the end of the jet."""
    out = []
    rng = random.Random(seed)
    f, uu, ss = basis_from(fwd, Vector((0, 0, 1)))

    def face(p):
        return (Vector(cam_loc) - p).normalized()

    # continuous soft core so the cone reads as one roaring jet, then the flipbook flame cards over it
    faint = mat_emit("D3_FlameFaint", "#ff7a1e", 1.1, soft=2.6)
    core = breath_cone(mouth, fwd, {"flame_o": faint, "flame_m": faint, "flame_c": mat_emit("D3_FlameCore", "#ffc860", 1.8, soft=1.8)})
    for ob in core:
        if ob.type == "MESH" and ob.name.startswith("BreathC"):   # keep only the slim inner jet; the cards carry the look
            ob.name = "FX_" + ob.name
            out.append(ob)
        else:
            bpy.data.objects.remove(ob, do_unlink=True)
    for i in range(56):
        t = (i + rng.random()) / 56
        ang = rng.uniform(0, 2 * math.pi)
        rad = (0.06 + 0.85 * t ** 0.9) * math.sqrt(rng.random())
        p = mouth + f * (0.12 + length * t) + (uu * math.cos(ang) + ss * math.sin(ang)) * rad + Vector((0, 0, 0.45 * t * t))
        size = 0.45 + 1.9 * t
        tint = d3_lerp_hex("#ffe7a0", "#ff9a2a", min(1.0, t / 0.45)) if t < 0.45 else d3_lerp_hex("#ff9a2a", "#c2300c", (t - 0.45) / 0.55)
        fr = max(0, min(15, int(round(t * 15 + rng.uniform(-1.2, 1.2)))))      # OneShot: frame follows particle age
        out.append(billboard(D3_FLAME_TEX, p, size * 1.15, size * 1.15, tint, 4.6 - 2.2 * t, alpha=1.0,
                             cell=(fr % 4, fr // 4), name=f"FX_Breath{i:02d}", facing=face(p), rot=rng.uniform(0, 2 * math.pi)))
    for i in range(7):
        t = rng.uniform(0.0, 0.18)
        p = mouth + f * (0.08 + length * t)
        s_ = 0.5 + 0.7 * t
        out.append(billboard(D3_GLOW_TEX, p, s_, s_, "#fff2c0", 5.0, name=f"FX_BreathCore{i}", facing=face(p)))
    for i in range(16):
        t = rng.uniform(0.15, 1.0)
        ang = rng.uniform(0, 2 * math.pi)
        p = mouth + f * (length * t) + (uu * math.cos(ang) + ss * math.sin(ang)) * (0.3 + 1.1 * t) + Vector((0, 0, 0.6 * t))
        s_ = rng.uniform(0.07, 0.15)
        out.append(billboard("VFX_spark_dot.png", p, s_, s_, "#ffb347", 7.0, name=f"FX_BreathSpark{i:02d}", facing=face(p)))
    for i in range(6):
        t = rng.uniform(0.85, 1.12)
        p = mouth + f * (length * t) + Vector((rng.uniform(-0.3, 0.3), 0, 0.5 + 0.9 * (t - 0.8)))
        s_ = rng.uniform(1.3, 2.1)
        fr = int(max(0.0, min(1.0, (t - 0.85) / 0.27)) * 9)      # OneShot: the sheet dissipates over its 16 frames
        out.append(billboard("VFX_smoke_flip4x4.png", p, s_, s_, "#4a4240", 0.55, alpha=0.7,
                             cell=(fr % 4, fr // 4), name=f"FX_BreathSmoke{i}", facing=face(p)))
    out.append(light("FX_BreathLight", "POINT", mouth + f * 1.4, mouth + f * 2.0, 1400, "#ff8a30", size=1.2))
    return out


def _vnoise3(x, y, z, perm):
    """Smooth 3D value noise in [0, 1] (vectorised; hashed lattice, smoothstep interpolation)."""
    xi, yi, zi = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64), np.floor(z).astype(np.int64)
    xf, yf, zf = x - xi, y - yi, z - zi
    u, v, w = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf), zf * zf * (3 - 2 * zf)

    def h(i, j, k):
        return perm[(perm[(perm[i & 255] + j) & 255] + k) & 255] / 255.0
    x0 = h(xi, yi, zi) * (1 - u) + h(xi + 1, yi, zi) * u
    x1 = h(xi, yi + 1, zi) * (1 - u) + h(xi + 1, yi + 1, zi) * u
    x2 = h(xi, yi, zi + 1) * (1 - u) + h(xi + 1, yi, zi + 1) * u
    x3 = h(xi, yi + 1, zi + 1) * (1 - u) + h(xi + 1, yi + 1, zi + 1) * u
    return (x0 * (1 - v) + x1 * v) * (1 - w) + (x2 * (1 - v) + x3 * v) * w


def _fbm3(x, y, z, perm, octaves=5):
    """Fractal value noise; each octave is rotated ~37 deg so lattice-aligned (flat, straight) edges don't show."""
    tot, amp, norm = 0.0, 1.0, 0.0
    ca, sa = math.cos(0.65), math.sin(0.65)
    for o in range(octaves):
        f = 2.0 ** o
        tot = tot + amp * _vnoise3(x * f + o * 17.3, y * f - o * 9.1, z * f + o * 3.7, perm)
        norm += amp
        amp *= 0.5
        x, y = x * ca - y * sa, x * sa + y * ca
    return tot / norm


def make_flame_flipbook(path, size=512, seed=11):
    """Own 4x4 flame flipbook for flying fire (breath jets, fireballs): billowing, turbulent flame puffs whose alpha fades
    to zero on EVERY side of each cell, so particles can fly and rotate freely (the pack's VFX_fire_flip4x4 frames are
    torch flames cut flat at the base). Frames play OneShot: compact and white-hot -> larger, tongued -> broken up and
    faint. Greyscale RGB (tint with ParticleEmitter.Color) + alpha. Rendered at 2x and box-filtered down."""
    perm = np.random.RandomState(seed).permutation(256).astype(np.int64)
    perm = np.concatenate([perm, perm])
    ss = 2
    n = size // 4 * ss
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float64)
    u = (xx + 0.5) / n * 2 - 1
    v = 1 - (yy + 0.5) / n * 2
    sheet = np.zeros((n * 4, n * 4, 4), np.float64)

    def sstep(e0, e1, x):
        t_ = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
        return t_ * t_ * (3 - 2 * t_)
    for i in range(16):
        t = i / 15.0
        R = 0.5 + 0.22 * t ** 0.8                                      # the puff grows inside its cell
        wx = _fbm3(u * 1.6 + 3.1, v * 1.6 - t * 1.4, t * 0.9, perm, 4) - 0.5        # domain warp: billowing lobes
        wy = _fbm3(u * 1.6 - 7.4, v * 1.6 - t * 1.4, t * 0.9 + 5.0, perm, 4) - 0.5
        pu, pv = u + 0.7 * wx, v + 0.7 * wy
        r = np.sqrt(pu * pu + (pv * 0.92 + 0.16) ** 2)
        heat = 1.0 - r / R                                             # > 0 inside the warped puff
        heat = heat + 0.9 * (_fbm3(pu * 2.6, pv * 2.6 - t * 2.0, t * 1.3, perm) - 0.5)
        # tongues: vertically stretched noise, stronger toward the top, so flames lick upward and taper to tips
        streak = _fbm3(pu * 3.8, pv * 0.95 - t * 2.8, t * 2.0 + 9.0, perm) - 0.5
        heat = heat + 2.1 * streak * np.clip(pv + 0.45, 0.0, 1.3) - 0.12 * np.clip(pv, 0.0, None)
        det = _fbm3(pu * 6.0, pv * 6.0 - t * 2.4, t * 1.7 + 2.0, perm)
        heat = heat + 0.25 * (det - 0.5)
        heat = heat - 0.95 * t ** 1.6 * _fbm3(pu * 3.0 + 11.0, pv * 3.0 - t * 1.5, t + 4.0, perm)   # late frames break up
        a = sstep(0.0, 0.32, heat) * (1.0 - 0.25 * t)
        a = a * sstep(1.0, 0.84, np.maximum(np.abs(u), np.abs(v)))                     # zero on every cell edge
        g = np.clip(0.3 + 0.7 * sstep(0.25, 1.05, heat) * (1.0 - 0.4 * t) + 0.1 * (det - 0.5), 0.0, 1.0)
        cy, cx = divmod(i, 4)
        sheet[cy * n:(cy + 1) * n, cx * n:(cx + 1) * n] = np.stack([g, g, g, a], axis=-1)
    out = sheet.reshape(size, ss, size, ss, 4).mean(axis=(1, 3))
    write_png(path, np.round(np.clip(out, 0, 1) * 255))
    log("flame flipbook", path, f"{size}x{size}")
    return out


def d3_nostril_smoke(nostrils, cam_loc, seed=5, scale=1.0, alpha=1.0):
    out = []
    rng = random.Random(seed)
    for n_i, n in enumerate(nostrils):
        for k in range(3):
            p = n + Vector((rng.uniform(-0.05, 0.05), -0.12 * (k + 0.5), 0.22 * (k + 0.6)))
            s_ = (0.22 + 0.22 * k) * scale
            out.append(billboard("VFX_smoke_puff.png", p, s_, s_, "#c9c0bd", 0.7, alpha=(0.6 - 0.15 * k) * alpha,
                                 name=f"FX_NoseSmoke{n_i}{k}", facing=(Vector(cam_loc) - p).normalized()))
    return out


def d3_embers(M, cam_loc, seed=9, n=22):
    """Ember drift: sparks lifting off the throat furnace and drifting up past the neck."""
    out = []
    rng = random.Random(seed)
    base = M["neck2"] @ Vector((0, 2.5, 2.55))
    for i in range(n):
        p = base + Vector((rng.uniform(-0.6, 0.6), rng.uniform(-0.9, 0.9), rng.uniform(0.0, 2.6)))
        s_ = rng.uniform(0.07, 0.16)
        out.append(billboard("VFX_spark_dot.png", p, s_, s_, "#ffa23a", 6.0, name=f"FX_Ember{i:02d}",
                             facing=(Vector(cam_loc) - p).normalized()))
    return out


def d3_throat_light(M, energy=90):
    p = M["neck2"] @ Vector((0, 2.55, 2.45))
    return [light("FX_ThroatLight", "POINT", p, p + Vector((0, 0.3, -0.5)), energy, "#ff6a1a", size=0.35)]


def d3_sheet_lights(objs, scale=1.3, **kw):
    for ob in list(bpy.context.scene.objects):
        if ob.type == "LIGHT" and not ob.name.startswith("FX_"):
            bpy.data.objects.remove(ob, do_unlink=True)
    mn, mx = world_bbox(objs)
    c = (mn + mx) / 2
    R = (mx - mn).length / 2
    args = dict(warm="#ffe9d0", rim1="#c8dcff", rim2="#ff9a4a", fill="#9fb8ff")
    args.update(kw)
    studio_lights(c, R, scale=scale, **args)
    return mn, mx


def d3_clear_build():
    for ob in list(bpy.data.objects):
        if ob.type in ("MESH", "LIGHT") and (ob.name.startswith("D3_") or ob.name.startswith("FX_")):
            bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):                 # each posed build leaves ~300k-vert orphans behind
        if me.users == 0:
            bpy.data.meshes.remove(me)


def d3_project(cam, p, W_, H_):
    """World point -> sheet image pixel (x right, y down)."""
    from bpy_extras.object_utils import world_to_camera_view
    co = world_to_camera_view(bpy.context.scene, cam, Vector(p))
    return [round(co.x * W_, 1), round((1.0 - co.y) * H_, 1)]


def render_drake3_sheet(sets):
    """v3 presentation-sheet renders into design/renders/ (same file names as the v2 board, v2 kept in renders/_v2/)."""
    import shutil
    old = os.path.join(REN, "_v2")
    if not os.path.isdir(old):
        os.makedirs(old)
        for fn in os.listdir(REN):
            if fn.startswith("drake_"):
                shutil.copy2(os.path.join(REN, fn), os.path.join(old, fn))
    reset()
    setup_render(samples=128)
    mats = drake3_materials()
    rig = drake3_rig()
    cam = camera()
    info = {}

    def build(pose_name):
        d3_clear_build()
        return build_drake3(D3_POSES[pose_name], mats, rig), rig.mats(D3_POSES[pose_name])

    if "ortho" in sets or "scale" in sets:
        objs, M = build("idle")
        mn, mx = d3_sheet_lights(objs)
        catcher = shadow_catcher()
        ppu, H = 64, 8.4
        hpx = int(H * ppu)
        cz = H / 2 - 0.15
        if "ortho" in sets:
            ws = int((mx.y - mn.y + 0.8) * ppu)
            ortho_view(cam, "side", (0, (mn.y + mx.y) / 2, cz), ppu, ws, hpx)
            render_to(os.path.join(REN, "drake_side.png"), ws, hpx)
            wf = int((mx.x - mn.x + 0.8) * ppu)
            ortho_view(cam, "front", (0, 0, cz), ppu, wf, hpx)
            render_to(os.path.join(REN, "drake_front.png"), wf, hpx)
            ortho_view(cam, "back", (0, 0, cz), ppu, wf, hpx)
            render_to(os.path.join(REN, "drake_back.png"), wf, hpx)
            info["ortho"] = {"ppu": ppu, "H": H, "ground_px": round(hpx - (0.15 + 0.0) * ppu - (H / 2 - cz) * 0, 1),
                             "side_w": ws, "front_w": wf, "h": hpx, "bbox_min": list(mn), "bbox_max": list(mx)}
            json.dump(info["ortho"], open(os.path.join(REN, "drake_ortho.json"), "w"), indent=1)
        if "scale" in sets:
            av = build_avatar(Vector((0, mx.y + 2.0, 0)))
            d3_sheet_lights(objs + av)
            ppu2 = 44
            y0, y1 = mn.y - 0.4, mx.y + 4.4
            W2, H2 = int((y1 - y0) * ppu2), int(H * ppu2)
            ortho_view(cam, "side", (0, (y0 + y1) / 2, cz), ppu2, W2, H2)
            render_to(os.path.join(REN, "drake_scale.png"), W2, H2, samples=110)
            json.dump({"ppu": ppu2, "y0": y0, "y1": y1, "H": H, "cz": cz, "w": W2, "h": H2, "top": mx.z,
                       "shoulder": 4.3, "length": mx.y - mn.y},
                      open(os.path.join(REN, "drake_scale.json"), "w"), indent=1)
            for ob in av:
                bpy.data.objects.remove(ob, do_unlink=True)
        bpy.data.objects.remove(catcher, do_unlink=True)

    if "hero" in sets:
        objs, M = build("idle")
        mn, mx = d3_sheet_lights(objs, scale=1.35, rim2="#ff8a3a", warm="#ffe2c0")
        catcher = shadow_catcher()
        c = (mn + mx) / 2
        R = (mx - mn).length / 2
        W_, H_ = 872, 1192
        lens = 32.0
        half = math.atan(18.0 * min(W_, H_) / max(W_, H_) / lens)
        camloc = c + Vector((0.42, 0.9, 0.12)).normalized() * (R / math.sin(half) * 0.64)   # head toward camera, tail recedes
        persp_view(cam, camloc, c + Vector((0.5, 2.6, -0.4)), lens=lens)
        fx = d3_nostril_smoke(d3_nostrils(M), camloc, scale=0.55, alpha=0.4) + d3_embers(M, camloc, n=16) + d3_throat_light(M)
        render_to(os.path.join(REN, "drake_hero.png"), W_, H_)
        for ob in fx + [catcher]:
            bpy.data.objects.remove(ob, do_unlink=True)

    if "poses" in sets:
        objs, M = build("roar")
        mnR, mxR = d3_sheet_lights(objs)
        # one camera for the row: portrait cards (~137 px wide on the board), front three-quarter like the hero so the
        # head - the expressive part - is big and the tail recedes; the breath flame comes out toward camera-right
        c = (mnR + mxR) / 2
        R = (mxR - mnR).length / 2
        W_, H_ = 400, 520
        lens = 34.0
        half = math.atan(18.0 * min(W_, H_) / max(W_, H_) / lens)
        camloc = c + Vector((0.5, 0.86, 0.14)).normalized() * (R / math.sin(half) * 0.6)     # tighter: fill the card
        target = c + Vector((0.0, 3.2, -0.35))            # panned toward the head so the snout (and breath) stay in frame
        for nm in ("idle", "alert", "roar", "breath"):
            objs, M = build(nm)
            d3_sheet_lights(objs)
            catcher = shadow_catcher()
            fx = d3_throat_light(M, 140 if nm in ("roar", "breath") else 90)
            if nm == "breath":
                mouth, fwd = d3_mouth(M)
                fx += d3_fire_breath(mouth, fwd, camloc)
            if nm == "idle":
                fx += d3_nostril_smoke(d3_nostrils(M), camloc)
            persp_view(cam, camloc, target, lens)
            render_to(os.path.join(REN, f"drake_pose_{nm}.png"), W_, H_, samples=110)
            for ob in fx + [catcher]:
                bpy.data.objects.remove(ob, do_unlink=True)

    if "parts" in sets:
        objs, M = build("idle")
        d3_sheet_lights(objs)
        W_, H_ = 480, 380

        def shot(path, target, offset, lens=50.0, keep=None):
            if keep is not None:
                hide_all_but(keep)
            persp_view(cam, Vector(target) + Vector(offset), target, lens)
            render_to(os.path.join(REN, path), W_, H_, samples=110)
            for ob in bpy.context.scene.objects:
                if ob.type == "MESH":
                    ob.hide_render = False

        hc = HP(0.85, 0, 0.0)
        shot("drake_part_head.png", hc, Vector((3.0, 2.6, 0.9)))
        horns = [o for o in objs if o.name in ("D3_HornL", "D3_Horn2L")]
        b0, b1 = world_bbox(horns)
        shot("drake_part_horn.png", (b0 + b1) / 2, Vector((2.6, 1.4, 1.2)) * ((b1 - b0).length / 2.0), keep=horns)
        wing = [o for o in objs if o.name.startswith("D3_WingL")]
        b0, b1 = world_bbox(wing)
        shot("drake_part_wing.png", (b0 + b1) / 2, Vector((3.4, 1.5, 0.6)).normalized() * ((b1 - b0).length * 1.05), keep=wing)
        shot("drake_part_pauldron.png", Vector((0.85, 1.15, 3.3)), Vector((2.7, 1.9, 0.9)))
        shot("drake_part_plates.png", Vector((0, -0.4, 3.7)), Vector((2.4, -3.2, 2.8)))
        shot("drake_part_feet.png", Vector((1.1, 1.75, 0.35)), Vector((2.2, 2.6, 0.9)))
        tl = d3_throat_light(M, 140)
        shot("drake_part_belly.png", Vector((0, 2.3, 2.3)), Vector((1.8, 3.6, -1.3)), lens=42)
        for ob in tl:
            bpy.data.objects.remove(ob, do_unlink=True)
        # glow: the whole front in low light so the eyes, throat furnace and mouth seam read
        for ob in bpy.context.scene.objects:
            if ob.type == "LIGHT":
                ob.data.energy *= 0.1
        bg = bpy.context.scene.world.node_tree.nodes["Background"]
        bg.inputs["Strength"].default_value = 0.06
        tl = d3_throat_light(M, 160)
        shot("drake_part_glow.png", HP(0.3, 0, -0.4), Vector((3.4, 3.4, 0.4)), lens=40)
        for ob in tl:
            bpy.data.objects.remove(ob, do_unlink=True)
        bg.inputs["Strength"].default_value = 0.55

    if "mats" in sets:
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT":
                bpy.data.objects.remove(ob, do_unlink=True)
            elif ob.type == "MESH":
                ob.hide_render = True
        studio_lights(Vector((0, 0, 0)), 1.6, warm="#ffe9d0", rim1="#c8dcff", rim2="#ff9a4a", fill="#9fb8ff")
        specs = [("skin", mats["skin"], {"dors": 1.0}), ("flank", mats["skin"], {"dors": 0.0}),
                 ("belly", mats["skin"], {"vent": 1.0, "vs": "z"}), ("lava", mats["skin"], {"vent": 1.0, "ember": 1.0, "vs": "z"}),
                 ("plate", mats["plate"], {"ph": "z01", "wear": "rim"}), ("horn", mats["horn"], {"t": "z01"}),
                 ("membrane", mats["membrane"], {"edge": "z01", "bonefac": 0.0}), ("eye", mats["eye"], {})]
        persp_view(cam, Vector((0, 3.6, 0.7)), Vector((0, 0, 0)), lens=50)
        for nm, mat, at in specs:
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=1.0)
            zs = [v.co.z for v in bm.verts]
            attrs = {}
            for k_, val in at.items():
                if val == "z":
                    attrs[k_] = [z_ * 1.0 for z_ in zs]
                elif val == "z01":
                    attrs[k_] = [(z_ + 1) / 2 for z_ in zs]
                elif val == "rim":
                    attrs[k_] = [max(0.0, abs(z_) - 0.6) * 2.5 for z_ in zs]
                else:
                    attrs[k_] = [float(val)] * len(zs)
            for k_ in ("dors", "vent", "vs", "ember", "joint", "face", "mouth", "t", "ph", "wear", "edge", "bonefac"):
                attrs.setdefault(k_, [0.0] * len(zs))
            ob = bm_to_obj(bm, f"MatBall_{nm}", mat, attrs)
            render_to(os.path.join(REN, f"drake_mat_{nm}.png"), 220, 220, samples=96)
            bpy.data.objects.remove(ob, do_unlink=True)

    if "vfx" in sets:
        objs, M = build("breath")
        mn, mx = d3_sheet_lights(objs)
        catcher = shadow_catcher()
        ppu, H = 40, 8.4
        mouth, fwd = d3_mouth(M)
        x0, x1 = mn.y - 0.4, max(mx.y, mouth.y + 6.9) + 0.3       # room for the whole jet and its smoke
        W_, H_ = int((x1 - x0) * ppu), int(H * ppu)
        ortho_view(cam, "side", (0, (x0 + x1) / 2, H / 2 - 0.15), ppu, W_, H_)
        camloc = cam.location.copy()
        fx = d3_fire_breath(mouth, fwd, camloc) + d3_nostril_smoke(d3_nostrils(M), camloc) + d3_embers(M, camloc) + \
            d3_throat_light(M, 140)
        render_to(os.path.join(REN, "drake_vfx.png"), W_, H_, samples=110)
        anchors = {"nostril": d3_nostrils(M)[0] + Vector((0, -0.1, 0.35)), "ember": M["neck2"] @ Vector((0, 2.5, 4.2)),
                   "throat": M["neck2"] @ Vector((0, 2.55, 2.4)), "breath": mouth + fwd * 2.4,
                   "eye": M["head"] @ HP(D3_EYE[0], D3_EYE[1], D3_EYE[2])}
        info["vfx"] = {"w": W_, "h": H_, "anchors": {k: d3_project(cam, v, W_, H_) for k, v in anchors.items()}}
        json.dump(info["vfx"], open(os.path.join(REN, "drake_vfx.json"), "w"), indent=1)
        for ob in fx + [catcher]:
            bpy.data.objects.remove(ob, do_unlink=True)

    if "habitat" in sets:
        objs, M = build("idle")
        hab = habitat_volcanic()
        ledge = [o for o in hab if o.name == "HAB_Rock0"][0]
        top = world_bbox([ledge])[1].z
        T = Matrix.Translation((-6.6, 3.2, top - 0.3)) @ Matrix.Rotation(math.radians(52), 4, "Z") @ Matrix.Scale(0.82, 4)
        for ob in objs:
            ob.matrix_world = T @ ob.matrix_world
        for ob in list(bpy.context.scene.objects):
            if ob.type == "LIGHT" and not ob.name.startswith("Hab"):
                bpy.data.objects.remove(ob, do_unlink=True)
        light("HabKey", "AREA", (-30, 30, 30), (-6, 3, 3), 4600, "#ffd7b0", size=12)
        light("HabRim", "AREA", (0, -40, 18), (-6, 3, 4), 11000, "#ff7a30", size=10)
        light("HabFill", "AREA", (10, 24, 10), (-6, 3, 3), 1400, "#9fb8ff", size=14)
        persp_view(cam, Vector((1.5, 24.0, 6.0)), Vector((-4.0, -6.0, 4.4)), lens=26)
        render_to(os.path.join(REN, "drake_habitat.png"), 1320, 504, samples=160)
        for ob in hab:
            bpy.data.objects.remove(ob, do_unlink=True)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FantasyCreatures_drake3_sheet.blend"))


def sets_value(sets, key, default):
    for a in sets:
        if a.startswith(key + ":"):
            return a.split(":", 1)[1]
    return default


def build_drake3(pose, mats, rig, h=0.02):
    """Build the v3 drake in a pose. Parts that are raycast onto the body (scutes, plates, head plates, wing flank line)
    are always placed on the REST body and then carried by their bone; only the SDF body and jaw are re-meshed posed.
    Poses may move neck/neck2/head/jaw/tail bones; chest and wing bones stay at rest (the membrane's flank attachment is
    rest-space)."""
    t0 = time.time()
    M0 = rig.mats({})
    M = rig.mats(pose)
    posed = bool(pose)
    objs = []
    rest = sdf_obj("D3_Body", drake3_body_prims(), M0, mats["skin"], h=h, smooth_iters=6, post=d3_body_detail)
    rme = rest.data
    bvh = BVHTree.FromPolygons([tuple(v) for v in vcoords(rme)], [tuple(p.vertices) for p in rme.polygons])
    if posed:
        body = sdf_obj("D3_BodyPosed", drake3_body_prims(), M, mats["skin"], h=h, smooth_iters=6, post=d3_body_detail)
    else:
        body = rest
    jaw = sdf_obj("D3_Jaw", drake3_jaw_prims(), M, mats["skin"], h=h * 0.8, smooth_iters=5)
    jaw["bone"] = "jaw"                                 # the game export splits jaw-bound parts into a hinged Jaw part
    d3_skin_attrs(body.data, M if posed else None, "body")
    d3_skin_attrs(jaw.data, M if posed else None, "jaw")
    objs += [body, jaw]
    log(f"drake3 SDF built in {time.time() - t0:.1f}s, body verts {len(body.data.vertices)}")
    for ob, bone in drake3_parts(mats, bvh) + d3_surface_parts(bvh, mats) + d3_head_plates(bvh, None, mats):
        ob.matrix_world = M[bone]
        ob["bone"] = bone
        objs.append(ob)
    for side in (1, -1):
        for ob in build_wing3(side, mats, f"D3_Wing{'L' if side > 0 else 'R'}", M, bvh):
            if not ob.name.endswith("_Arm"):
                ob.matrix_world = M["wing_L" if side > 0 else "wing_R"]
            objs.append(ob)
    if posed:
        bpy.data.objects.remove(rest, do_unlink=True)
        bpy.data.meshes.remove(rme)
        body.name = "D3_Body"
    log(f"drake3 total {time.time() - t0:.1f}s")
    return objs


def clay_material():
    m, t = new_mat("CLAY")
    if t:
        aof = t.maprange(t.ao(0.35), 0.0, 1.0, 0.55, 1.0)
        col = t.mix(1.0, (0.36, 0.36, 0.37, 1.0), t.mix(aof, (0, 0, 0, 1), (1, 1, 1, 1)), blend="MULTIPLY")
        t.bsdf(col, rough=0.62, spec=0.35)
    return m


def render_drake3(sets):
    """Grey clay review: side / front / three-quarter (+ head close-up). 'fast' = quick preview, no exports."""
    fast = "fast" in sets
    reset()
    setup_render(samples=40 if fast else 128)
    clay = clay_material()
    mats = {k: clay for k in ("skin", "horn", "claw", "teeth", "eye", "pupil", "mouth", "plate", "membrane", "wingbone")}
    rig = drake3_rig()
    objs = build_drake3({}, mats, rig)
    sc = bpy.context.scene
    sc.render.film_transparent = False
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = hexcol("#3d4046")
    sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    floor_m = mat_simple("CLAY_Floor", "#55585e", rough=0.9, aodark=0.0)
    me = bpy.data.meshes.new("Floor")
    me.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    me.materials.append(floor_m)
    link(bpy.data.objects.new("Floor", me))
    mn, mx = world_bbox(objs)
    c = (mn + mx) / 2
    R = (mx - mn).length / 2
    light("Key", "AREA", c + Vector((-0.8, 1.0, 1.2)) * R * 1.6, c, 60 * R * R, "#ffffff", size=R * 1.4)
    light("Fill", "AREA", c + Vector((1.2, 0.8, 0.4)) * R * 1.8, c, 22 * R * R, "#ffffff", size=R * 1.6)
    light("Rim", "AREA", c + Vector((0.4, -1.4, 0.9)) * R * 1.6, c, 40 * R * R, "#ffffff", size=R * 1.0)
    cam = camera()
    out = os.path.join(OUT, "review")
    os.makedirs(out, exist_ok=True)
    tag = "_fast" if fast else ""
    if "headonly" in sets:                      # quick head turnaround for sculpt iterations
        hc = HP(0.55, 0, 0.0)
        ortho_view(cam, "side", tup(hc), 240, 1000, 800)
        render_to(os.path.join(out, "drake3_hd_side.png"), 1000, 800)
        ortho_view(cam, "front", tup(hc), 300, 1000, 800)
        render_to(os.path.join(out, "drake3_hd_front.png"), 1000, 800)
        hc2 = HP(0.9, 0, -0.1)
        persp_view(cam, hc2 + Vector((3.4, 3.0, 1.3)), hc2, lens=55)
        render_to(os.path.join(out, "drake3_hd_34.png"), 1000, 800)
        persp_view(cam, hc2 + Vector((0.2, 1.2, 5.0)), hc2, lens=55)
        render_to(os.path.join(out, "drake3_hd_top.png"), 1000, 800)
        return
    W_, H_ = 1500, 1000
    ppu = W_ / ((mx.y - mn.y) + 1.2)
    ortho_view(cam, "side", (0, c.y, (mx.z + mn.z) / 2), ppu, W_, H_)
    render_to(os.path.join(out, f"drake3_clay_side{tag}.png"), W_, H_)
    ortho_view(cam, "front", (0, 0, (mx.z + mn.z) / 2), min(ppu * 1.25, H_ / ((mx.z - mn.z) + 0.8)), W_, H_)
    render_to(os.path.join(out, f"drake3_clay_front{tag}.png"), W_, H_)
    d34 = Vector((0.62, 0.78, 0.28)).normalized()
    half = math.atan(18.0 * H_ / W_ / 40.0)
    persp_view(cam, c + d34 * (R / math.sin(half) * 0.62), c + Vector((0, 0.3, -0.4)), lens=40)
    render_to(os.path.join(out, f"drake3_clay_34{tag}.png"), W_, H_)
    hc = HP(0.8, 0, -0.05)
    persp_view(cam, hc + Vector((3.6, 3.0, 1.0)), hc, lens=50)
    render_to(os.path.join(out, f"drake3_clay_head{tag}.png"), 1200, 900)
    if "headfront" in sets or not fast:
        ortho_view(cam, "front", tup(HP(0.55, 0, 0.0)), 270, 1200, 900)
        render_to(os.path.join(out, f"drake3_clay_headfront{tag}.png"), 1200, 900)
    if fast:
        return
    # export the clay model for live inspection in Holden's Blender (OBJ, no textures)
    for ob in bpy.context.scene.objects:
        ob.select_set(ob in objs)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.wm.obj_export(filepath=os.path.join(out, "drake3_clay.obj"), export_selected_objects=True, export_uv=False,
                          export_normals=True, export_materials=False, export_triangulated_mesh=False,
                          forward_axis="NEGATIVE_Z", up_axis="Y", apply_modifiers=True)
    json.dump({"bbox_min": list(mn), "bbox_max": list(mx)}, open(os.path.join(out, "drake3_dims.json"), "w"), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FantasyCreatures_drake3_clay.blend"))


# ============================================================ game export (OBJ + MTL + baked 1024 colour map)
class DrakeExport:
    key = "drake"
    prefix = "D_"

    def setup(self):
        self.mats = drake_materials()
        self.rig = drake_rig()
        self.plate_inst, self.plate_src = make_plate_cache(self.mats, self.rig)

    def build(self, name):
        spec = DRAKE_POSES[name]
        cr = build_drake_pose(spec["pose"], self.mats, self.rig, self.plate_inst, wing_spread=spec["spread"])
        return cr.objs


EXPORT_INFO = {
    "drake": dict(name="CinderDrake", tex=1024),
    "golem": dict(name="MossbackGolem", tex=1024),
    "wolf": dict(name="FrostfangWolf", tex=1024),
}


def export_groups(key, objs):
    """Map each creature's render objects onto Roblox MeshParts: name -> (objects, kind, colour)."""
    def pick(fn):
        return [o for o in objs if o.type == "MESH" and fn(o.name)]
    if key == "drake":
        body = pick(lambda n: n.startswith("D_") and not any(n.startswith(p) for p in ("D_Eye", "D_Flame", "D_Mouth", "D_Tongue")))
        return {"Body": (body, "tex", None),
                "Glow": (pick(lambda n: n.startswith("D_Eye") or n.startswith("D_FlameO")), "neon", "#FFB43A")}
    if key == "golem":
        body = pick(lambda n: n.startswith("G_") and not any(n.startswith(p) for p in ("G_Crystal", "G_Heart", "G_Eye")))
        return {"Body": (body, "tex", None),
                "Crystals": (pick(lambda n: n.startswith("G_Crystal")), "tex", None),
                "Glow": (pick(lambda n: n.startswith("G_Heart") or n.startswith("G_Eye")), "neon", "#B57CFF")}
    if key == "wolf":
        body = pick(lambda n: n.startswith("W_") and not any(n.startswith(p) for p in ("W_Ice", "W_Eye", "W_Mouth", "W_Tongue")))
        return {"Body": (body, "tex", None),
                "Ice": (pick(lambda n: n.startswith("W_Ice")), "tex", None),
                "Glow": (pick(lambda n: n.startswith("W_Eye")), "neon", "#9BF0FF")}
    raise ValueError(key)


DECIMATE_TARGETS = {"D_Body": 3400, "D_Jaw": 380, "D_HornL": 260, "D_HornR": 260, "D_WingL_Membrane": 320, "D_WingR_Membrane": 320,
                    "D_Eye1": 110, "D_Eye-1": 110, "D_FlameO": 120,
                    "G_Core": 1200, "W_Body": 4600, "W_Jaw": 380, "W_Eye1": 90, "W_Eye-1": 90, "G_Eye1": 60, "G_Eye-1": 60}


# per-part export budgets by name fragment (first match wins); keeps the v2 detail inside ~10k tris
DECIMATE_RULES = [("Band", 140), ("Belt", 180), ("Leaf", 16), ("Vine", 60),
                  ("ArmorSpike", 24), ("SideSpike", 24), ("Spike", 26), ("Frill", 30), ("Crest", 28), ("Blade", 30),
                  ("Thumb", 26), ("FingerClaw", 18), ("Claw", 24), ("Tooth", 20), ("Fang", 20), ("Horn2", 120),
                  ("NoseHorn", 40), ("Horn", 240), ("Armor", 60), ("Elbow", 26), ("Heel", 26)]


def export_target(name):
    if name in DECIMATE_TARGETS:
        return DECIMATE_TARGETS[name]
    for frag, tgt in DECIMATE_RULES:
        if frag in name:
            return tgt
    return None


def evaluated_mesh(ob, drop_subsurf=True):
    """World-space copy of an object's evaluated mesh (modifiers applied, optionally without Subsurf)."""
    saved = []
    bev = []
    if drop_subsurf:
        for md in ob.modifiers:
            if md.type == "SUBSURF":
                saved.append((md, md.show_render, md.show_viewport))
                md.show_render = md.show_viewport = False
            elif md.type == "BEVEL" and md.segments > 1:
                bev.append((md, md.segments))
                md.segments = 1
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    for md, r, v in saved:
        md.show_render, md.show_viewport = r, v
    for md, s in bev:
        md.segments = s
    me.transform(ob.matrix_world)
    return me


def decimated_copy(ob, target):
    me = evaluated_mesh(ob)
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    tmp = bpy.data.objects.new(ob.name + "_dec", me)
    link(tmp)
    if target and tris > target:
        md = tmp.modifiers.new("Dec", "DECIMATE")
        md.decimate_type = "COLLAPSE"
        md.ratio = target / tris
        md.use_collapse_triangulate = True
        me2 = evaluated_mesh(tmp, drop_subsurf=False)
        bpy.data.objects.remove(tmp, do_unlink=True)
        bpy.data.meshes.remove(me)
        me2.transform(Matrix.Identity(4))
        return me2
    bpy.data.objects.remove(tmp, do_unlink=True)
    return me


def join_meshes(name, meshes, smooth_names=None):
    bm = bmesh.new()
    for me in meshes:
        bm.from_mesh(me)
    for me in meshes:
        bpy.data.meshes.remove(me)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    out = bpy.data.meshes.new(name)
    bm.to_mesh(out)
    bm.free()
    ob = bpy.data.objects.new(name, out)
    link(ob)
    return ob


def export_creature(key):
    reset()
    setup_render()
    spec = {"drake": DrakeExport, "golem": GolemSpec, "wolf": WolfSpec}[key]()
    spec.setup()
    objs = spec.build("idle")
    info = EXPORT_INFO[key]
    cname = info["name"]
    folder = os.path.join(OUT, "models", cname)
    os.makedirs(folder, exist_ok=True)
    groups = export_groups(key, objs)
    lows, neons = {}, {}
    for part, (highs, kind, col) in groups.items():
        meshes = []
        for ob in highs:
            meshes.append(decimated_copy(ob, export_target(ob.name)))
        low = join_meshes(f"{cname}_{part}", meshes)
        (lows if kind == "tex" else neons)[part] = (low, highs, col)
        log(part, "tris", len(low.data.polygons))
    # shared UV space for every textured part
    for ob in bpy.context.scene.objects:
        ob.select_set(False)
    tex_objs = [v[0] for v in lows.values()]
    for ob in tex_objs:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = tex_objs[0]
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(62), island_margin=0.003, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    try:
        bpy.ops.uv.pack_islands(margin=0.004, rotate=True)
    except Exception as ex:
        log("pack_islands skipped:", ex)
    bpy.ops.object.mode_set(mode="OBJECT")
    # bake targets
    size = info["tex"]
    img_c = bpy.data.images.new(f"{cname}_Color", size, size, alpha=False)
    img_e = bpy.data.images.new(f"{cname}_Emit", size, size, alpha=False)
    bake_nodes = []
    for part, (low, highs, _) in lows.items():
        m = bpy.data.materials.new(f"{cname}_{part}")
        try:
            m.use_nodes = True
        except Exception:
            pass
        nt = m.node_tree
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = img_c
        nt.nodes.active = tn
        nt.links.new(tn.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
        low.data.materials.clear()
        low.data.materials.append(m)
        bake_nodes.append(tn)
    sc = bpy.context.scene
    sc.cycles.samples = 48
    bk = sc.render.bake
    bk.use_selected_to_active = True
    bk.cage_extrusion = 0.08
    bk.max_ray_distance = 0.3
    bk.margin = 8
    for pass_type, img in (("DIFFUSE", img_c), ("EMIT", img_e)):
        for tn in bake_nodes:
            tn.image = img
        first = True
        for part, (low, highs, _) in lows.items():
            for ob in bpy.context.scene.objects:
                ob.select_set(False)
            for h in highs:
                h.hide_render = False
                h.select_set(True)
            low.select_set(True)
            bpy.context.view_layer.objects.active = low
            t0 = time.time()
            if pass_type == "DIFFUSE":
                bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_selected_to_active=True, cage_extrusion=0.08,
                                    max_ray_distance=0.3, margin=8, use_clear=first)
            else:
                bpy.ops.object.bake(type="EMIT", use_selected_to_active=True, cage_extrusion=0.08, max_ray_distance=0.3, margin=8,
                                    use_clear=first)
            first = False
            log("baked", pass_type, part, f"{time.time() - t0:.1f}s")
    for tn in bake_nodes:
        tn.image = img_c
    c = np.array(img_c.pixels[:], np.float32).reshape(size, size, 4)
    e = np.array(img_e.pixels[:], np.float32).reshape(size, size, 4)
    c[..., :3] = np.clip(c[..., :3] + e[..., :3] * 0.55, 0.0, 1.0)
    c[..., 3] = 1.0
    out_img = bpy.data.images.new(f"{cname}_Tex", size, size, alpha=False)
    out_img.pixels.foreach_set(c.ravel())
    tex_path = os.path.join(folder, f"{cname}_Color.png")
    out_img.filepath_raw = tex_path
    out_img.file_format = "PNG"
    out_img.save()
    for tn in bake_nodes:
        tn.image = out_img
    # neon parts: flat colour material (MTL Kd)
    for part, (low, highs, col) in neons.items():
        m = bpy.data.materials.new(f"{cname}_{part}Neon")
        try:
            m.use_nodes = True
        except Exception:
            pass
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = hexcol(col)
        m.diffuse_color = hexcol(col)
        low.data.materials.clear()
        low.data.materials.append(m)
    # shading: flat for faceted parts, smooth for organic
    for part, (low, _, _) in list(lows.items()) + list(neons.items()):
        if part in ("Crystals", "Ice") or (key == "golem" and part == "Body"):
            for p in low.data.polygons:
                p.use_smooth = False
        else:
            low.data.shade_smooth()
    # OBJ export
    exp = [v[0] for v in lows.values()] + [v[0] for v in neons.values()]
    for ob in bpy.context.scene.objects:
        ob.select_set(False)
    for ob in exp:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = exp[0]
    bpy.ops.wm.obj_export(filepath=os.path.join(folder, f"{cname}.obj"), export_selected_objects=True, export_uv=True,
                          export_normals=True, export_colors=False, export_materials=True, export_triangulated_mesh=True,
                          export_smooth_groups=False, path_mode="STRIP", forward_axis="NEGATIVE_Z", up_axis="Y",
                          global_scale=1.0, apply_modifiers=True)
    # report: sizes, tris, pivot, attachments (Roblox axes: x, z, -y), relative to the file origin (= model pivot)
    def rbx(v):
        return [round(v.x, 3), round(v.z, 3), round(-v.y, 3)]
    mn, mx = world_bbox(exp)
    report = {"model": cname, "units": "studs", "pivot": "file origin = ground under the creature, front faces -Z",
              "bbox_min_rbx": rbx(Vector((mn.x, mx.y, mn.z))), "bbox_max_rbx": rbx(Vector((mx.x, mn.y, mx.z))),
              "size_studs": [round(mx.x - mn.x, 2), round(mx.z - mn.z, 2), round(mx.y - mn.y, 2)], "parts": {}}
    for ob in exp:
        report["parts"][ob.name] = {"tris": len(ob.data.polygons),
                                    "material": "Neon" if ob.name.endswith("Glow") else ("Glass" if ob.name.endswith(("Crystals", "Ice")) else "SmoothPlastic")}
    report["attachments"] = {k: rbx(v) for k, v in attachment_points(key, spec, objs).items()}
    report["texture"] = os.path.basename(tex_path)
    with open(os.path.join(folder, "build_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    log("EXPORT", json.dumps(report["parts"]), report["size_studs"])
    # preview of the actual game mesh (baked texture, simple studio light)
    for ob in list(bpy.context.scene.objects):
        if ob.type == "MESH" and ob not in exp:
            ob.hide_render = True
        if ob.type == "LIGHT":
            bpy.data.objects.remove(ob, do_unlink=True)
    for part, (low, _, col) in neons.items():
        m = low.data.materials[0]
        bs = m.node_tree.nodes["Principled BSDF"]
        bs.inputs["Emission Color"].default_value = hexcol(col)
        bs.inputs["Emission Strength"].default_value = 3.0
    c3 = (mn + mx) / 2
    R = (mx - mn).length / 2
    studio_lights(c3, R)
    cam = camera("PreviewCam")
    for nm, d in (("front34", Vector((0.7, 0.85, 0.25))), ("back34", Vector((-0.75, -0.7, 0.3)))):
        persp_view(cam, c3 + d.normalized() * R * 2.3, c3, 45)
        render_to(os.path.join(folder, f"preview_{nm}.png"), 900, 700, samples=96)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"FantasyCreatures_{key}_export.blend"))


def attachment_points(key, spec, objs):
    def tip(name):
        ob = [o for o in objs if o.name == name][0]
        return max((ob.matrix_world @ v.co for v in ob.data.vertices), key=lambda p: p.z)
    if key == "drake":
        hp = lambda p: HEAD_PIVOT + (Vector(p) - HEAD_PIVOT) * HEAD_SCALE
        return {"Mouth": hp((0, 4.8, 4.62)), "NostrilL": hp((0.2, 4.78, 5.02)), "NostrilR": hp((-0.2, 4.78, 5.02)),
                "TailTip": Vector((0, -5.2, 2.75)), "Back1": Vector((0, 0.9, 3.9)), "Back2": Vector((0, -0.3, 3.75)),
                "Back3": Vector((0, -1.5, 3.7)), "Chest": Vector((0, 1.7, 2.9)), "Root": Vector((0, 0, 0))}
    if key == "golem":
        return {"Heart": Vector((0, 1.9, 6.05)), "EyeL": Vector((0.33, 1.85, 7.56)), "EyeR": Vector((-0.33, 1.85, 7.56)),
                "Crystal1": tip("G_CrystalBack0"), "Crystal2": tip("G_CrystalBack1"), "Crystal3": tip("G_CrystalBack2"),
                "Crystal4": tip("G_CrystalSh0L"), "Crystal5": tip("G_CrystalSh0R"), "FistL": Vector((3.55, 1.3, 0.1)),
                "FistR": Vector((-3.55, 1.3, 0.1)), "FootL": Vector((1.35, 0.3, 0.05)), "FootR": Vector((-1.35, 0.3, 0.05)),
                "ShoulderL": Vector((2.75, 0.0, 8.3)), "ShoulderR": Vector((-2.75, 0.0, 8.3)), "Root": Vector((0, 0, 0))}
    if key == "wolf":
        return {"Mouth": Vector((0, 3.8, 3.68)), "EyeL": Vector((0.34, 3.02, 4.06)), "EyeR": Vector((-0.34, 3.02, 4.06)),
                "Spine1": tip("W_IceSp0"), "Spine2": tip("W_IceSp1"), "Spine3": tip("W_IceSp2"), "Spine4": tip("W_IceSp3"),
                "Spine5": tip("W_IceSp4"), "PawFL": Vector((0.6, 1.25, 0.04)), "PawFR": Vector((-0.6, 1.25, 0.04)),
                "PawBL": Vector((0.62, -1.4, 0.04)), "PawBR": Vector((-0.62, -1.4, 0.04)), "TailTip": tip("W_IceTailTip"),
                "Chest": Vector((0, 1.6, 2.8)), "Root": Vector((0, 0, 0))}
    return {}


# ============================================================ drake v3 game export: OBJ + SurfaceAppearance texture sets
# Roblox (docs + DevForum, checked 2026-10-04): SurfaceAppearance takes ColorMap, NormalMap (OpenGL tangent space only),
# RoughnessMap, MetalnessMap and EmissiveMaskContent (single channel; red is read) with EmissiveStrength / EmissiveTint.
# Emissive is computed as (mask * strength * tint + light) * ColorMap, so glowing texels must be ember-coloured in the
# ColorMap. Max 20,000 tris per MeshPart; 1024^2 is the UV-space guideline for characters. The importer only builds a
# SurfaceAppearance automatically for FBX, so for OBJ the maps are attached in Studio (see IMPORT.md next to the OBJ).
D3_EXPORT = dict(name="CinderDrake", tex=1024, emissive_strength=6.0)
# the jaw ships as its own MeshPart hinged at the jaw bone (no rig needed: a script turns it about X at its pivot).
# It shares the Body texture set; the Body bake is done with the jaw wide open so the palate, tongue and lower teeth
# bake cleanly instead of baking each other through the closed mouth.
D3_JAW_OPEN = dict(bake=-40.0, breath=-28.0, roar=-40.0)

# per-object triangle budgets (prefix match, first wins); the normal map carries the sculpt detail
D3_BUDGET = [("D3_Body", 6800), ("D3_Jaw", 900), ("_ArmScute", 16), ("_Arm", 900), ("_ElbowSpur", 24), ("_ThumbClaw", 24),
             ("_Membrane", 1400), ("_Digit", 44), ("_Joint", 24), ("D3_Horn2", 110), ("D3_Horn", 220), ("D3_ToothU", 16), ("D3_ToothL", 16),
             ("D3_FangL", 24), ("D3_Claw", 30), ("D3_Dewclaw", 24), ("D3_Hallux", 24), ("D3_JawSpine", 24), ("D3_BrowKnob", 24),
             ("D3_Scute", 16), ("D3_Shoulder", 70), ("D3_Plate", 24), ("D3_CrownPlate", 20), ("D3_BrowPlate", 20),
             ("D3_NosePlate", 20), ("D3_Pupil", 24), ("D3_Eye", 80), ("D3_MouthGlow", 0)]


def d3_budget(name):
    for frag, n in D3_BUDGET:
        if frag in name:
            return n
    return 60


# share of texture space per part type (relative texel density): skin first, small hard parts last
D3_UVW = [("D3_Body", 1.0), ("D3_Jaw", 1.0), ("_ArmScute", 0.5), ("_Arm", 0.9), ("_Membrane", 1.0), ("_Digit", 0.6),
          ("_Joint", 0.4), ("D3_Horn", 0.7), ("D3_Shoulder", 0.7), ("D3_Scute", 0.5), ("D3_Plate", 0.6), ("Plate", 0.6),
          ("D3_Pupil", 0.3), ("D3_MouthGlow", 0.15)]


def d3_uv_weight(name):
    for frag, w in D3_UVW:
        if frag in name:
            return w
    return 0.45                                   # teeth, claws, spines, knobs, spurs


def batch_decimated(pairs):
    """[(object, tri_target)] -> world-space decimated meshes using two depsgraph updates in total (decimated_copy does
    two per object, which took >10 min for the ~350-part drake)."""
    saved = []
    for ob, _ in pairs:
        for md in ob.modifiers:
            if md.type == "SUBSURF":
                saved.append((md, "sub", (md.show_render, md.show_viewport)))
                md.show_render = md.show_viewport = False
            elif md.type == "BEVEL" and md.segments > 1:
                saved.append((md, "bev", md.segments))
                md.segments = 1
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    temps = []
    for ob, tgt in pairs:
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        me.transform(ob.matrix_world)
        tris = sum(len(p.vertices) - 2 for p in me.polygons)
        tmp = bpy.data.objects.new(ob.name + "_dec", me)
        link(tmp)
        if tgt and tris > tgt:
            md = tmp.modifiers.new("Dec", "DECIMATE")
            md.decimate_type = "COLLAPSE"
            md.ratio = tgt / tris
            md.use_collapse_triangulate = True
        temps.append(tmp)
    dg.update()
    out = []
    for tmp in temps:
        src = tmp.data
        out.append(bpy.data.meshes.new_from_object(tmp.evaluated_get(dg)))
        bpy.data.objects.remove(tmp, do_unlink=True)
        bpy.data.meshes.remove(src)
    for md, kind, val in saved:
        if kind == "sub":
            md.show_render, md.show_viewport = val
        else:
            md.segments = val
    return out


def d3_bake_proxy(name, highs):
    """Join a group's high-res parts (modifiers applied; materials and shader attributes kept) into ONE bake source.
    Selected-to-active raycasts every selected object per texel, so ~300 separate parts made one 1024 pass take 5+ min."""
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    parts = []
    for h in highs:
        me = bpy.data.meshes.new_from_object(h.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        me.transform(h.matrix_world)
        o = bpy.data.objects.new(h.name + "_bk", me)
        link(o)
        parts.append(o)
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    proxy = bpy.context.view_layer.objects.active
    proxy.name = name
    for h in highs:
        h.hide_render = True
    log(name, "bake proxy verts", len(proxy.data.vertices), "materials", len(proxy.data.materials))
    return proxy


def d3_faces_of(ob, pids):
    """Boolean face mask of a joined low mesh: faces whose 'pid' (source high object index) is in pids."""
    me = ob.data
    pid = np.zeros(len(me.polygons), np.int32)
    me.attributes["pid"].data.foreach_get("value", pid)
    return np.isin(pid, np.array(sorted(pids), np.int32))


def d3_move_faces(ob, pids, mat):
    """Rigidly transform the vertices of the faces from the given source parts (the jaw opening around its hinge)."""
    me = ob.data
    sel = d3_faces_of(ob, pids)
    vidx = sorted({v for p in np.nonzero(sel)[0] for v in me.polygons[int(p)].vertices})
    co = np.zeros(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    R = np.array(mat.to_3x3(), np.float32)
    T = np.array(mat.translation, np.float32)
    co[vidx] = co[vidx] @ R.T + T
    me.vertices.foreach_set("co", co.ravel())
    me.update()


def d3_split_faces(ob, pids, name):
    """Move the faces of the given source parts into a new object (same mesh data layers: UVs, materials, sharp edges)."""
    sel = d3_faces_of(ob, pids)
    part = bpy.data.objects.new(name, ob.data.copy())
    link(part)
    for o, keep in ((part, sel), (ob, ~sel)):
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep[f.index]], context="FACES")
        bm.to_mesh(o.data)
        bm.free()
    return part


def d3_export_groups(objs):
    meshes = [o for o in objs if o.type == "MESH"]
    wings = [o for o in meshes if o.name.startswith("D3_Wing") and any(k in o.name for k in ("_Membrane", "_Digit", "_Joint"))]
    glow = [o for o in meshes if o.name.startswith("D3_Eye")]      # mouth glow is baked into the Body emissive mask
    body = [o for o in meshes if o not in wings and o not in glow]
    return {"Body": body, "Wings": wings, "Glow": glow}


def write_png(path, arr):
    """Exact 8-bit PNG (grey HxW or RGB HxWx3, row 0 = top) - no colour management on data maps."""
    import zlib
    import struct
    a = np.ascontiguousarray(np.asarray(arr, np.uint8))
    h, w = a.shape[:2]
    ctype = 0 if a.ndim == 2 else (6 if a.shape[2] == 4 else 2)          # grey / RGBA / RGB
    raw = b"".join(b"\x00" + a[y].tobytes() for y in range(h))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ctype, 0, 0, 0)) +
                chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def img_array(img):
    """Blender image pixels -> HxWx4 float array, row 0 = top (PNG order)."""
    s = img.size
    return np.array(img.pixels[:], np.float32).reshape(s[1], s[0], 4)[::-1]


D3_PLATE_KEYS = ("D3_Scute", "_ArmScute", "D3_Shoulder", "D3_CrownPlate", "D3_BrowPlate", "D3_NosePlate", "D3_Plate")


def d3_planar_uv(me):
    """One planar island per plate: project on the plate's mean plane (stud units); rim vertices get pushed outward by
    their depth so the rim becomes a skirt band instead of zero-area slivers (degenerate UVs break tangents)."""
    n = len(me.vertices)
    co = np.zeros(n * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    fn = np.zeros(len(me.polygons) * 3, np.float32)
    me.polygons.foreach_get("normal", fn)
    fa = np.zeros(len(me.polygons), np.float32)
    me.polygons.foreach_get("area", fa)
    nrm = (fn.reshape(-1, 3) * fa[:, None]).sum(axis=0)
    nrm /= max(np.linalg.norm(nrm), 1e-9)
    t1 = np.cross(nrm, [0.0, 0.0, 1.0] if abs(nrm[2]) < 0.9 else [1.0, 0.0, 0.0])
    t1 /= np.linalg.norm(t1)
    t2 = np.cross(nrm, t1)
    uv = np.stack([co @ t1, co @ t2], axis=1)
    h = co @ nrm
    depth = np.clip(h.max() - h - 0.004, 0.0, None)
    cen = uv.mean(axis=0)
    out = uv - cen
    out /= np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-6)
    uv = uv + out * depth[:, None]
    lv = np.zeros(len(me.loops), np.int32)
    me.loops.foreach_get("vertex_index", lv)
    layer = me.uv_layers.new(name="UVMap")
    layer.data.foreach_set("uv", uv[lv].ravel())


def d3_region(c):
    """Anatomical UV region of a body-face centroid: torso 0, legs 1-4, neck+head left/right 5/7 (one island each, like a
    face mask - unwrapped whole it folded over itself and put throat embers on the face), tail 6, feet -1 (smart UV:
    toes fold under a pelt unwrap)."""
    x, y, z = c
    ax = abs(x)
    if ax > 0.6 and z < 0.42:
        return -1
    if ax > 0.62 and 0.35 < y < 2.3 and z < 2.25:
        return 1 if x > 0 else 2
    if ax > 0.62 and -3.0 < y < -0.55 and z < 2.35:
        return 3 if x > 0 else 4
    if y > 2.05:
        return 5 if x >= 0 else 7
    if y < -2.85:
        return 6
    return 0


def d3_mark_body_seams(bm, faces):
    """Creature UV layout for the low-poly body: ring seams between regions, plus one seam per region along its hidden
    underside (shortest path that avoids up-facing / outward-facing surfaces) so each region unrolls into one island."""
    import heapq
    reg = {f.index: d3_region(f.calc_center_median()) for f in faces}
    fset = set(reg)
    # majority-vote smoothing: thresholds on a decimated mesh leave single faces in the wrong region, which became
    # hundreds of 1-2 face islands
    for _ in range(4):
        new = {}
        for f in faces:
            votes = defaultdict(int)
            votes[reg[f.index]] += 1
            for e in f.edges:
                for g in e.link_faces:
                    if g.index != f.index and g.index in fset:
                        votes[reg[g.index]] += 1
            new[f.index] = max(votes.items(), key=lambda kv: (kv[1], kv[0] == reg[f.index]))[0]
        reg = new
    for f in faces:
        for e in f.edges:
            other = [g for g in e.link_faces if g.index != f.index and g.index in fset]
            if other and reg[other[0].index] != reg[f.index]:
                e.seam = True

    def vreg(v):
        rs = {reg[f.index] for f in v.link_faces if f.index in fset}
        return rs

    def path(r, start, goal):
        verts = {v for f in faces if reg[f.index] == r for v in f.verts}
        dist = {start: 0.0}
        prev = {}
        pq = [(0.0, start.index, start)]
        seen = set()
        while pq:
            d_, _, v = heapq.heappop(pq)
            if v in seen:
                continue
            seen.add(v)
            if v is goal:
                break
            for e in v.link_edges:
                w = e.other_vert(v)
                if w not in verts:
                    continue
                ns = [f.normal for f in e.link_faces]
                nz = sum(n_.z for n_ in ns) / len(ns)
                nx = sum(n_.x for n_ in ns) / len(ns) * (1 if w.co.x >= 0 else -1)
                cost = e.calc_length() * (1.0 + 4.0 * max(0.0, nz + 0.2) + (2.0 * max(0.0, nx) if r in (1, 2, 3, 4) else 0.0))
                nd = d_ + cost
                if nd < dist.get(w, 1e18):
                    dist[w] = nd
                    prev[w] = (v, e)
                    heapq.heappush(pq, (nd, w.index, w))
        v = goal
        while v in prev:
            pv, e = prev[v]
            e.seam = True
            v = pv

    for r in (0, 1, 2, 3, 4, 6):                      # neck/head halves (5, 7) are already disks: no extra cut
        rv = [v for f in faces if reg[f.index] == r for v in f.verts]
        if len(rv) < 20:
            continue
        ring = [v for v in rv if len(vreg(v)) > 1]
        if r == 0:                                    # torso: belly line from the neck ring to the tail ring
            a = min((v for v in ring if vreg(v) & {5, 7}), key=lambda v: v.co.z, default=None)
            b = min((v for v in ring if 6 in vreg(v)), key=lambda v: v.co.z, default=None)
        elif r == 6:                                  # tail: base ring underside to the tip
            a = min(ring, key=lambda v: v.co.z, default=None)
            b = min(rv, key=lambda v: v.co.y)
        else:                                         # legs: inner side of the top ring down to the back of the ankle ring
            a = min((v for v in ring if 0 in vreg(v)), key=lambda v: abs(v.co.x), default=None)
            b = min((v for v in ring if -1 in vreg(v)), key=lambda v: v.co.z + 0.6 * v.co.y, default=None)
        if a is not None and b is not None and a is not b:
            path(r, a, b)
    return reg


def d3_mark_arm_seam(faces, S, W, top):
    """One seam along the underside of a wing arm, shoulder -> wrist, so the arm unrolls as a single island."""
    import heapq
    verts = {v for f in faces for v in f.verts}
    if not verts:
        return
    start = min(verts, key=lambda v: (v.co - S).length)
    goal = min(verts, key=lambda v: (v.co - W).length)
    dist, prev, seen = {start: 0.0}, {}, set()
    pq = [(0.0, start.index, start)]
    while pq:
        d_, _, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        if v is goal:
            break
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in verts:
                continue
            nt = sum(f.normal.dot(top) for f in e.link_faces) / max(1, len(e.link_faces))
            nd = d_ + e.calc_length() * (1.0 + 4.0 * max(0.0, nt + 0.2))
            if nd < dist.get(w, 1e18):
                dist[w] = nd
                prev[w] = (v, e)
                heapq.heappush(pq, (nd, w.index, w))
    v = goal
    while v in prev:
        pv, e = prev[v]
        e.seam = True
        v = pv


def d3_unwrap(ob, body_pid=None, arm_pids=None):
    """UVs for a joined game mesh: creature layout for the body (seams + angle-based unwrap), one underside seam per
    wing arm, planar islands for plates (precomputed per part before the join), smart UV for the rest; then uniform
    density, per-part weights, pack."""
    arm_pids = arm_pids or {}
    me = ob.data
    nf = len(me.polygons)
    pid = np.zeros(nf, np.int32)
    me.attributes["pid"].data.foreach_get("value", pid)
    planar = np.zeros(nf, np.int32)
    if "planar" in me.attributes:
        me.attributes["planar"].data.foreach_get("value", planar)

    def select_faces(mask):
        """Select exactly these faces (in edit mode, face-select mode). Setting polygon flags in object mode is not
        enough: entering edit mode rebuilds the selection from the vertex flags, which were all still selected."""
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        if ob.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
        bm_ = bmesh.from_edit_mesh(me)
        bm_.faces.ensure_lookup_table()
        for f in bm_.faces:
            f.select_set(False)
        for f in bm_.faces:
            if mask[f.index]:
                f.select_set(True)
        bmesh.update_edit_mesh(me)
        bpy.ops.object.mode_set(mode="OBJECT")

    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    organic = np.zeros(nf, bool)
    if body_pid is not None or arm_pids:
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        if body_pid is not None:
            reg = d3_mark_body_seams(bm, [f for f in bm.faces if pid[f.index] == body_pid])
            for fi, r in reg.items():
                organic[fi] = r >= 0                  # feet (-1) go to smart UV with the small parts
        for ap, sx in arm_pids.items():
            S, E, W, A, digits = d3_wing_points(sx)
            afaces = [f for f in bm.faces if pid[f.index] == ap]
            ew = W - E
            arm_part = [f for f in afaces if (f.calc_center_median() - E).dot(ew) / ew.length_squared < 0.9]
            hand = set(f.index for f in afaces) - set(f.index for f in arm_part)
            for f in afaces:                          # seam between the arm and the hand (wrist + finger bases)
                for e in f.edges:
                    if any((g.index in hand) != (f.index in hand) for g in e.link_faces if pid[g.index] == ap):
                        e.seam = True
            d3_mark_arm_seam(arm_part, S, W, d3_wing_top(sx))
            for f in arm_part:
                organic[f.index] = True
        bm.to_mesh(me)
        bm.free()
        select_faces(organic)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.uv.unwrap(method="ANGLE_BASED", fill_holes=True, correct_aspect=True, margin=0.002)
        bpy.ops.object.mode_set(mode="OBJECT")
    rest = (planar == 0) & ~organic
    select_faces(rest)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.002, area_weight=0.0, correct_aspect=True,
                             scale_to_bounds=False)
    bpy.ops.mesh.select_all(action="SELECT")
    try:
        bpy.ops.uv.average_islands_scale()
    except Exception as ex:
        log("average_islands_scale skipped:", ex)
    bpy.ops.object.mode_set(mode="OBJECT")
    nl = len(me.loops)
    uvs = np.zeros(nl * 2, np.float32)
    me.uv_layers.active.data.foreach_get("uv", uvs)
    uvs = uvs.reshape(-1, 2)
    w = np.zeros(nf, np.float32)
    me.attributes["uvw"].data.foreach_get("value", w)
    tot = np.zeros(nf, np.int32)
    me.polygons.foreach_get("loop_total", tot)
    lface = np.repeat(np.arange(nf), tot)
    lp, lw = pid[lface], w[lface]
    for p in np.unique(lp):
        sel = lp == p
        c = uvs[sel].mean(axis=0)
        uvs[sel] = c + (uvs[sel] - c) * lw[sel][0]
    me.uv_layers.active.data.foreach_set("uv", uvs.ravel())
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    try:
        bpy.ops.uv.pack_islands(margin=0.003, rotate=True, scale=True, shape_method="CONCAVE")
    except Exception as ex:
        log("pack_islands (concave) failed, retry default:", ex)
        bpy.ops.uv.pack_islands(margin=0.003, rotate=True, scale=True)
    bpy.ops.object.mode_set(mode="OBJECT")


def d3_bake(low, highs, pass_type, img, samples, extrusion, ray, margin=16):
    sc = bpy.context.scene
    sc.cycles.samples = samples
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for h in highs:
        h.hide_render = False
        h.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    low.data.materials[0].node_tree.nodes.active.image = img
    kw = dict(use_selected_to_active=True, cage_extrusion=extrusion, max_ray_distance=ray, margin=margin, use_clear=True)
    t0 = time.time()
    if pass_type == "DIFFUSE":
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, **kw)
    elif pass_type == "NORMAL":
        bpy.ops.object.bake(type="NORMAL", normal_space="TANGENT", normal_r="POS_X", normal_g="POS_Y", normal_b="POS_Z", **kw)
    else:
        bpy.ops.object.bake(type=pass_type, **kw)
    log("baked", low.name, pass_type, f"{time.time() - t0:.1f}s")


def export_drake3(sets):
    """High-res v3 drake -> Roblox game meshes (Body / Wings / Glow) + 1024 SurfaceAppearance maps + previews."""
    reset()
    setup_render(samples=64)
    mats = drake3_materials()
    rig = drake3_rig()
    objs = build_drake3({}, mats, rig)
    info = D3_EXPORT
    cname = info["name"]
    folder = os.path.join(OUT, "models", cname)
    os.makedirs(folder, exist_ok=True)
    groups = d3_export_groups(objs)
    # bake the membrane as pure surface colour (its translucent mix would darken the diffuse-colour pass)
    mem = bpy.data.materials.get("D3_Membrane")
    if mem:
        for nd in mem.node_tree.nodes:
            if nd.type == "MIX_SHADER":
                nd.inputs[0].default_value = 0.0
    lows, body_pids, arm_pids = {}, {}, {}
    for part, highs in groups.items():
        t0 = time.time()
        meshes = batch_decimated([(ob, d3_budget(ob.name)) for ob in highs])
        for pid_, (me_, ob_) in enumerate(zip(meshes, highs)):
            nf = len(me_.polygons)
            is_plate = any(k in ob_.name for k in D3_PLATE_KEYS)
            if is_plate:
                d3_planar_uv(me_)
            me_.attributes.new("pid", "INT", "FACE").data.foreach_set("value", np.full(nf, pid_, np.int32))
            me_.attributes.new("uvw", "FLOAT", "FACE").data.foreach_set("value", np.full(nf, d3_uv_weight(ob_.name), np.float32))
            me_.attributes.new("planar", "INT", "FACE").data.foreach_set("value", np.full(nf, 1 if is_plate else 0, np.int32))
        body_pids[part] = next((i for i, o in enumerate(highs) if o.name == "D3_Body"), None)
        arm_pids[part] = {i: (1 if "WingL" in o.name else -1) for i, o in enumerate(highs) if o.name.endswith("_Arm")}
        low = join_meshes(f"{cname}_{part}", meshes)
        log(part, f"decimated + joined in {time.time() - t0:.1f}s")
        low.data.shade_smooth()
        try:
            low.data.set_sharp_from_angle(angle=math.radians(60))       # crisp plate/claw edges, smooth organic skin
        except Exception as ex:
            log("set_sharp_from_angle unavailable:", ex)
        lows[part] = (low, highs)
        log(part, "tris", len(low.data.polygons), "from", len(highs), "objects")
    size = info["tex"]
    maps = {}
    # AO inside the materials must only see the bake source, not the low-poly game mesh lying almost on top of it
    for m_ in bpy.data.materials:
        if m_.node_tree:
            for nd in m_.node_tree.nodes:
                if nd.type == "AMBIENT_OCCLUSION":
                    nd.only_local = True
    jaw_pids = [i for i, o in enumerate(lows["Body"][1]) if o.get("bone") == "jaw"]
    J_bake = rig.mats({"jaw": (D3_JAW_OPEN["bake"], 0, 0)})["jaw"]
    log("jaw parts", len(jaw_pids), [o.name for o in lows["Body"][1] if o.get("bone") == "jaw"][:4], "...")
    for part in ("Body", "Wings"):
        low, highs = lows[part]
        if part == "Body":                                # open the high-res jaw before it is merged into the bake source
            for o in highs:
                if o.get("bone") == "jaw":
                    o.matrix_world = J_bake @ o.matrix_world
        highs = [d3_bake_proxy(f"{cname}_{part}_High", highs)]
        d3_unwrap(low, body_pids.get(part), arm_pids.get(part))
        if part == "Body" and jaw_pids:                   # unwrap closed, bake open (a rigid turn keeps the UVs valid)
            d3_move_faces(low, jaw_pids, J_bake)
        m = bpy.data.materials.new(f"{cname}_{part}_Bake")
        try:
            m.use_nodes = True
        except Exception:
            pass
        tn = m.node_tree.nodes.new("ShaderNodeTexImage")
        m.node_tree.nodes.active = tn
        low.data.materials.clear()
        low.data.materials.append(m)
        ext, ray = (0.05, 0.22) if part == "Body" else (0.02, 0.07)
        imgs = {}
        for key, ptype, smp, noncolor in (("color", "DIFFUSE", 16, False), ("normal", "NORMAL", 8, True),
                                          ("rough", "ROUGHNESS", 8, True)) + ((("emit", "EMIT", 8, False),) if part == "Body" else ()):
            img = bpy.data.images.new(f"{cname}_{part}_{key}", size, size, alpha=False)
            if noncolor:
                img.colorspace_settings.name = "Non-Color"
            boost = []
            if ptype == "NORMAL":                 # stronger relief for the game map: scale seams must survive 1024 + distance
                for mn_, f_ in (("D3_Skin", 2.0), ("D3_Plate", 1.5), ("D3_Horn", 1.5), ("D3_Membrane", 1.5)):
                    m_ = bpy.data.materials.get(mn_)
                    for nd in (m_.node_tree.nodes if m_ and m_.node_tree else []):
                        if nd.type == "BUMP":
                            boost.append((nd, nd.inputs["Strength"].default_value))
                            nd.inputs["Strength"].default_value *= f_
            d3_bake(low, highs, ptype, img, smp, ext, ray)
            for nd, s_ in boost:
                nd.inputs["Strength"].default_value = s_
            imgs[key] = img_array(img)
        # ColorMap: albedo, with ember-coloured texels where it glows (Roblox multiplies emissive by the ColorMap)
        col = imgs["color"][..., :3]
        if "emit" in imgs:
            e = imgs["emit"][..., :3]
            lum = e.max(axis=2)
            p98 = float(np.percentile(lum[lum > 0.02], 98)) if np.any(lum > 0.02) else 1.0
            mask = np.clip((lum / max(1e-4, p98) - 0.12) / 0.88, 0.0, 1.0)        # tightened: seams stay thin at 80 px/stud
            hue = e / np.maximum(lum[..., None], 1e-4)
            col = col * (1.0 - mask[..., None]) + hue * mask[..., None]
            write_png(os.path.join(folder, f"{cname}_{part}_Emissive.png"), np.round(mask * 255))
            maps[part + "_Emissive"] = mask
        write_png(os.path.join(folder, f"{cname}_{part}_Color.png"), np.round(np.clip(col, 0, 1) * 255))
        write_png(os.path.join(folder, f"{cname}_{part}_Normal.png"), np.round(np.clip(imgs["normal"][..., :3], 0, 1) * 255))
        write_png(os.path.join(folder, f"{cname}_{part}_Roughness.png"), np.round(np.clip(imgs["rough"][..., 0], 0, 1) * 255))
        maps[part] = True
        if part == "Body" and jaw_pids:
            d3_move_faces(low, jaw_pids, J_bake.inverted())          # back to the closed rest pose for export
    # export materials: colour map only in the MTL (the other maps go on the SurfaceAppearance in Studio)
    for part in ("Body", "Wings"):
        low, _ = lows[part]
        m = bpy.data.materials.new(f"{cname}_{part}")
        try:
            m.use_nodes = True
        except Exception:
            pass
        tn = m.node_tree.nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(os.path.join(folder, f"{cname}_{part}_Color.png"))
        m.node_tree.links.new(tn.outputs["Color"], next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"])
        low.data.materials.clear()
        low.data.materials.append(m)
    glow, _ = lows["Glow"]
    gm = bpy.data.materials.new(f"{cname}_GlowNeon")
    try:
        gm.use_nodes = True
    except Exception:
        pass
    next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = hexcol("#FF7A1E")
    gm.diffuse_color = hexcol("#FF7A1E")
    glow.data.materials.clear()
    glow.data.materials.append(gm)
    jaw_low = d3_split_faces(lows["Body"][0], jaw_pids, f"{cname}_Jaw") if jaw_pids else None
    exp = [lows["Body"][0]] + ([jaw_low] if jaw_low else []) + [lows[p][0] for p in ("Wings", "Glow")]
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in exp:
        o.select_set(True)
    bpy.context.view_layer.objects.active = exp[0]
    bpy.ops.wm.obj_export(filepath=os.path.join(folder, f"{cname}.obj"), export_selected_objects=True, export_uv=True,
                          export_normals=True, export_colors=False, export_materials=True, export_triangulated_mesh=True,
                          export_smooth_groups=False, path_mode="STRIP", forward_axis="NEGATIVE_Z", up_axis="Y",
                          global_scale=1.0, apply_modifiers=True)

    def rbx(v):
        return [round(v.x, 3), round(v.z, 3), round(-v.y, 3)]

    mn, mx = world_bbox(exp)
    d, u = d3_head_frame()
    att = {"Mouth": HP(1.6, 0, -0.22), "NostrilL": HP(1.74, 0.11, 0.15), "NostrilR": HP(1.74, -0.11, 0.15),
           "EyeL": d3_eye_frame(1)[0], "EyeR": d3_eye_frame(-1)[0], "Throat": Vector((0, 2.3, 2.6)), "Chest": Vector((0, 1.95, 2.2)),
           "Back1": Vector((0, 0.9, 4.0)), "Back2": Vector((0, -0.6, 3.8)), "Back3": Vector((0, -2.0, 3.8)),
           "TailTip": Vector(D3_TAIL[-1][0]), "WingTipL": d3_wing_points(1)[4][0][1], "WingTipR": d3_wing_points(-1)[4][0][1],
           "Root": Vector((0, 0, 0))}
    body_sa = {"ColorMap": f"{cname}_Body_Color.png", "NormalMap": f"{cname}_Body_Normal.png",
               "RoughnessMap": f"{cname}_Body_Roughness.png", "EmissiveMaskContent": f"{cname}_Body_Emissive.png",
               "EmissiveStrength": info["emissive_strength"], "EmissiveTint": [255, 255, 255], "AlphaMode": "Overlay"}
    report = {"model": cname, "version": "v3.1 (proportions pass + hinged jaw, 2026-10-04)", "units": "studs",
              "pivot": "file origin = ground under the creature; it faces -Z (Roblox front) after import",
              "size_studs": [round(mx.x - mn.x, 2), round(mx.z - mn.z, 2), round(mx.y - mn.y, 2)],
              "parts": {o.name: {"tris": len(o.data.polygons)} for o in exp},
              "total_tris": sum(len(o.data.polygons) for o in exp),
              "part_centres_rbx": {o.name: rbx((world_bbox([o])[0] + world_bbox([o])[1]) / 2) for o in exp},
              "surface_appearance": {
                  f"{cname}_Body": body_sa,
                  f"{cname}_Wings": {"ColorMap": f"{cname}_Wings_Color.png", "NormalMap": f"{cname}_Wings_Normal.png",
                                      "RoughnessMap": f"{cname}_Wings_Roughness.png", "AlphaMode": "Overlay"}},
              "glow_part": {f"{cname}_Glow": {"Material": "Neon", "Color": [255, 122, 30]}},
              "attachments_rbx": {k: rbx(v) for k, v in att.items()}}
    if jaw_low:
        hinge = rig.bones["jaw"]["head"]
        jc = (world_bbox([jaw_low])[0] + world_bbox([jaw_low])[1]) / 2
        report["surface_appearance"][f"{cname}_Jaw"] = dict(body_sa, note="same images as the Body (one shared texture set)")
        report["jaw"] = {"part": f"{cname}_Jaw", "hinge_rbx": rbx(hinge),
                         "pivot_offset_from_part_centre": [round(a - b, 3) for a, b in zip(rbx(hinge), rbx(jc))],
                         "axis": "X (the part's own X; pivot orientation stays identity)",
                         "open_deg": {"breath": D3_JAW_OPEN["breath"], "roar": D3_JAW_OPEN["roar"]},
                         "note": "negative = mouth opens (Blender sign; same axis in Roblox axes). Baked at "
                                 f"{D3_JAW_OPEN['bake']} deg open, so the mouth interior is textured for any opening."}
    with open(os.path.join(folder, "build_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    log("EXPORT", json.dumps(report["parts"]), "total", report["total_tris"], report["size_studs"])
    # preview: the game meshes with the baked maps, approximating Roblox (emissive = mask * strength * ColorMap)
    for o in list(bpy.context.scene.objects):
        if o.type == "MESH" and o not in exp:
            o.hide_render = True
        if o.type == "LIGHT":
            bpy.data.objects.remove(o, do_unlink=True)
    for part in ("Body", "Wings"):
        low, _ = lows[part]
        m = low.data.materials[0]
        nt = m.node_tree
        bs = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        cimg = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
        rn = nt.nodes.new("ShaderNodeTexImage")
        rn.image = bpy.data.images.load(os.path.join(folder, f"{cname}_{part}_Roughness.png"))
        rn.image.colorspace_settings.name = "Non-Color"
        nt.links.new(rn.outputs["Color"], bs.inputs["Roughness"])
        nn = nt.nodes.new("ShaderNodeTexImage")
        nn.image = bpy.data.images.load(os.path.join(folder, f"{cname}_{part}_Normal.png"))
        nn.image.colorspace_settings.name = "Non-Color"
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(nn.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bs.inputs["Normal"])
        bs.inputs["Specular IOR Level"].default_value = 0.4
        if part == "Body":
            en = nt.nodes.new("ShaderNodeTexImage")
            en.image = bpy.data.images.load(os.path.join(folder, f"{cname}_Body_Emissive.png"))
            en.image.colorspace_settings.name = "Non-Color"
            mul = nt.nodes.new("ShaderNodeMix")
            mul.data_type = "RGBA"
            mul.blend_type = "MULTIPLY"
            ins = [s for s in mul.inputs if s.enabled]
            ins[0].default_value = 1.0
            nt.links.new(cimg.outputs["Color"], [s for s in ins if s.name == "A"][0])
            nt.links.new(en.outputs["Color"], [s for s in ins if s.name == "B"][0])
            nt.links.new([s for s in mul.outputs if s.enabled and s.type == "RGBA"][0], bs.inputs["Emission Color"])
            bs.inputs["Emission Strength"].default_value = info["emissive_strength"] * 0.5
    gbs = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    gbs.inputs["Emission Color"].default_value = hexcol("#FF7A1E")
    gbs.inputs["Emission Strength"].default_value = 4.0
    sc = bpy.context.scene
    sc.render.film_transparent = False
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = hexcol("#26282c")
    sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
    c3 = (mn + mx) / 2
    R = (mx - mn).length / 2
    studio_lights(c3, R, warm="#fff3e2", rim1="#eef2ff", rim2="#ffd8b0", fill="#e6ebf2", scale=1.2)
    cam = camera("PreviewCam")
    d34 = Vector((0.62, 0.78, 0.28)).normalized()
    half = math.atan(18.0 * 1000 / 1600 / 40.0)
    persp_view(cam, c3 + d34 * (R / math.sin(half) * 0.6), c3 + Vector((0, 0.3, -0.5)), lens=40)
    render_to(os.path.join(folder, "preview_game_hero.png"), 1600, 1000, samples=128)
    hc = HP(0.8, 0, -0.05)
    persp_view(cam, hc + Vector((3.6, 3.0, 1.0)), hc, lens=50)
    render_to(os.path.join(folder, "preview_game_head.png"), 1200, 900, samples=128)
    if jaw_low:                                         # the hinged jaw opened as a script would (breath angle)
        jaw_low.matrix_world = rig.mats({"jaw": (D3_JAW_OPEN["breath"], 0, 0)})["jaw"]
        persp_view(cam, hc + Vector((3.3, 3.4, 0.2)), hc + Vector((0, 0.2, -0.25)), lens=50)
        render_to(os.path.join(folder, "preview_game_jaw_open.png"), 1200, 900, samples=128)
        jaw_low.matrix_world = Matrix.Identity(4)
    persp_view(cam, c3 + Vector((-0.75, -0.7, 0.45)).normalized() * R * 2.2, c3, 45)
    render_to(os.path.join(folder, "preview_game_back34.png"), 1200, 900, samples=128)
    for o in exp:                      # wireframe-free flat check of the silhouette at game distance
        pass
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "FantasyCreatures_drake3_export.blend"))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "flameflip" in argv:
        make_flame_flipbook(D3_FLAME_TEX)
        return
    if "drake3col" in argv:
        render_drake3_colour(set(argv))
        return
    if "export3" in argv:
        export_drake3(set(argv))
        return
    if "drake3sheet" in argv:
        s3 = set(argv)
        if "all" in s3:
            s3 |= {"ortho", "hero", "poses", "parts", "mats", "scale", "vfx", "habitat"}
        render_drake3_sheet(s3)
        return
    if "drake3" in argv:
        render_drake3(set(argv))
        return
    if "export" in argv:
        for c in [a for a in argv if a in ("drake", "golem", "wolf")]:
            export_creature(c)
        return
    creatures = [a for a in argv if a in ("drake", "golem", "wolf")] or ["drake"]
    sets = set(a for a in argv if a not in ("drake", "golem", "wolf") and "=" not in a) or {"ortho", "hero"}
    if "all" in sets:
        sets = {"ortho", "hero", "poses", "parts", "mats", "scale", "vfx", "habitat"}
    for c in creatures:
        if c == "drake":
            render_drake(sets)
        elif c == "golem":
            render_creature(GolemSpec(), sets)
        elif c == "wolf":
            render_creature(WolfSpec(), sets)


main()
