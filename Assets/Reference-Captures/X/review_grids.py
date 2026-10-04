"""Build review grids: one JPEG per category page with 12 thumbnails (first image, or video poster) in manifest order.
Writes X/_review/<category>-<page>.jpg and prints the index → post mapping. Local review aid only.
  blender.exe -b --factory-startup --python review_grids.py
"""
import json
import os

import bpy
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_review")
COLS, ROWS, TW, TH = 4, 3, 480, 300
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

by_cat: dict[str, list] = {}
for tid, m in manifest.items():
    by_cat.setdefault(m["category"], []).append((tid, m))


def thumb(path: str) -> np.ndarray:
    img = bpy.data.images.load(path)
    w, h = img.size
    s = min(TW / w, TH / h)
    img.scale(max(1, int(w * s)), max(1, int(h * s)))
    w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    bpy.data.images.remove(img)
    tile = np.full((TH, TW, 4), 0.08, dtype=np.float32)
    tile[..., 3] = 1
    y0, x0 = (TH - h) // 2, (TW - w) // 2
    tile[y0:y0 + h, x0:x0 + w] = px
    return tile


for cat, items in by_cat.items():
    for p in range(0, len(items), COLS * ROWS):
        page = items[p:p + COLS * ROWS]
        sheet = np.zeros((TH * ROWS, TW * COLS, 4), dtype=np.float32)
        sheet[..., 3] = 1
        for i, (tid, m) in enumerate(page):
            files = [x for x in m["files"] if x.endswith(".jpg")]
            if not files:
                continue
            t = thumb(os.path.join(ROOT, m["folder"], files[0]))
            r, c = divmod(i, COLS)
            y0 = (ROWS - 1 - r) * TH
            sheet[y0:y0 + TH, c * TW:(c + 1) * TW] = t
            print(f"{cat}-{p // 12 + 1} #{i + 1}: {m['author']} {tid} ({m['likes']})")
        img = bpy.data.images.new("g", TW * COLS, TH * ROWS, alpha=False)
        img.pixels[:] = sheet.ravel()
        img.filepath_raw = os.path.join(OUT, f"{cat}-{p // 12 + 1}.jpg")
        img.file_format = "JPEG"
        img.save()
        bpy.data.images.remove(img)
