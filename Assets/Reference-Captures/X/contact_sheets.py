"""Make a 4x3 contact sheet (12 evenly spaced frames) for every vid-N.mp4 under X/ that lacks sheet-N.jpg.

No ffmpeg on this PC, so this runs in headless Blender (see [[Video Frame Extraction with Blender]]):
  blender.exe -b --factory-startup --python contact_sheets.py
"""
import glob
import os

import bpy
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
COLS, ROWS = 4, 3
TILE_W = 480  # output tile width in px; height follows the video aspect


def frame_pixels(path: str) -> np.ndarray:
    img = bpy.data.images.load(path)
    w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    bpy.data.images.remove(img)
    return px


def make_sheet(video: str, out: str) -> None:
    scene = bpy.context.scene
    seq = scene.sequence_editor_create()
    for s in list(seq.strips_all if hasattr(seq, "strips_all") else seq.sequences_all):
        (seq.strips if hasattr(seq, "strips") else seq.sequences).remove(s)
    strips = seq.strips if hasattr(seq, "strips") else seq.sequences
    strip = strips.new_movie("clip", video, channel=1, frame_start=1)
    w, h = strip.elements[0].orig_width, strip.elements[0].orig_height
    n = strip.frame_final_duration
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = max(1, min(100, int(TILE_W * 100 / w)))
    scene.render.fps = int(round(strip.fps)) if getattr(strip, "fps", 0) else 30
    scene.render.image_settings.file_format = "PNG"
    tmp = os.path.join(bpy.app.tempdir, "f.png")
    tiles = []
    for i in range(COLS * ROWS):
        scene.frame_set(1 + int((n - 1) * (i + 0.5) / (COLS * ROWS)))
        scene.render.filepath = tmp
        bpy.ops.render.render(write_still=True)
        tiles.append(frame_pixels(tmp))
    th, tw = tiles[0].shape[:2]
    sheet = np.zeros((th * ROWS, tw * COLS, 4), dtype=np.float32)
    for i, t in enumerate(tiles):
        r, c = divmod(i, COLS)
        # Blender pixel rows start at the bottom, so fill rows from the bottom of the sheet up.
        y0 = (ROWS - 1 - r) * th
        sheet[y0:y0 + th, c * tw:(c + 1) * tw] = t[:th, :tw]
    img = bpy.data.images.new("sheet", tw * COLS, th * ROWS, alpha=False)
    img.pixels[:] = sheet.ravel()
    img.filepath_raw = out
    img.file_format = "JPEG"
    img.save()
    bpy.data.images.remove(img)
    print("sheet", out, f"{n} frames")


for video in sorted(glob.glob(os.path.join(ROOT, "**", "vid-*.mp4"), recursive=True)):
    out = video.replace("vid-", "sheet-").replace(".mp4", ".jpg")
    if not os.path.exists(out):
        try:
            make_sheet(video, out)
        except Exception as e:
            print("error", video, e)
