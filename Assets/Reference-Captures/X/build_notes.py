"""Regenerate the catalogue blocks inside the Reference/X-*.md notes from manifest.json + takeaways.json.

Each note holds a block between `<!-- catalogue:start -->` and `<!-- catalogue:end -->`; only that block is rewritten,
so hand-written TL;DR / patterns / pitfalls above and below it are kept.
  "C:/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe" build_notes.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
REL = "Assets/Reference-Captures/X"

# note file → ordered (category, section heading) pairs
NOTES = {
    "X-Shop-And-Seasonal-UI.md": [
        ("ui-seasonal", "Seasonal and event shops"),
        ("ui-shop", "Shops, stores and starter packs"),
        ("ui-stud", "Stud-style and cartoony UI"),
    ],
    "X-HUD-And-Menus-UI.md": [
        ("ui-hud", "HUDs"),
        ("ui-menus", "Menus: rewards, battlepass, quests, results, inventory"),
    ],
    "X-Animated-UI-Lessons-And-Tools.md": [
        ("ui-anim", "Animated UI and motion"),
        ("ui-lessons", "Designer lessons"),
        ("ui-tools", "UI tools and plugins"),
    ],
    "X-VFX-Reference.md": [
        ("vfx", "VFX"),
        ("vfx-tools", "VFX tools"),
    ],
    "X-Thumbnails-And-Icons.md": [
        ("thumbnails", "Thumbnails, icons and the AI-thumbnail debate"),
    ],
    "X-Hatching-And-Pet-Systems.md": [
        ("hatching", "Egg hatching and pet systems"),
    ],
    "X-Low-Poly-Builds-And-Maps.md": [
        ("lowpoly", "Low-poly models and builds"),
        ("lobby", "Lobbies and maps"),
    ],
    "X-Animation-Reference.md": [
        ("animation", "Character animation"),
    ],
    "X-Fishing-And-Paper-References.md": [
        ("fishing", "Fishing games"),
        ("paper", "Paper and papercraft style"),
    ],
    "X-Game-Feel-And-Showcases.md": [
        ("gamefeel", "Game feel"),
        ("events", "Events"),
        ("showcase", "Game showcases and trailers"),
        ("growth", "Growth signals"),
        ("art", "Art and models"),
        ("art-lessons", "Art lessons"),
        ("tech", "Tech demos"),
        ("tools", "Tools and plugins"),
    ],
}


def load(name: str) -> dict:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def clean(text: str, words: int = 14) -> str:
    text = re.sub(r"https?://\S+", "", text or "")
    text = re.sub(r"#\w+", "", text)
    text = " ".join(text.split())
    w = text.split()
    return " ".join(w[:words]) + ("…" if len(w) > words else "")


def entry(tid: str, m: dict, take: dict) -> str:
    folder = f"{REL}/{m['folder']}"
    files = m["files"]
    # Contact sheets are rendered later by contact_sheets.py, so look for them on disk.
    sheets = sorted(f for f in os.listdir(os.path.join(ROOT, m["folder"])) if f.startswith("sheet-"))
    preview = sheets[0] if sheets else next((f for f in files if f.endswith(".jpg")), None)
    videos = [f for f in files if f.endswith(".mp4")]
    imgs = [f for f in files if f.startswith("img-")]
    lines = [f"#### {m['author']} — {m['note'] or clean(m['text'], 8)}",
             f"[post]({m['url']}) · ♥ {m['likes']:,} · {m['date']}"
             + (f" · " + " · ".join(f"[[{folder}/{v}|▶ video {i + 1}]]" for i, v in enumerate(videos)) if videos else "")
             + (f" · {len(imgs)} images" if len(imgs) > 1 else "")]
    if preview:
        lines.append(f"![[{folder}/{preview}|480]]")
    cap = clean(m["text"])
    if cap:
        lines.append(f"> {cap}")
    t = take.get(tid)
    if t:
        lines.append(f"**Take:** {t}")
    return "\n".join(lines)


def main() -> None:
    manifest, take = load("manifest.json"), load("takeaways.json")
    for note, sections in NOTES.items():
        path = os.path.join(VAULT, "Reference", note)
        if not os.path.exists(path):
            print("missing", note)
            continue
        out = []
        for cat, heading in sections:
            items = sorted(((t, m) for t, m in manifest.items() if m["category"] == cat),
                           key=lambda x: -(x[1]["likes"] or 0))
            if not items:
                continue
            out.append(f"### {heading} ({len(items)})\n")
            out.extend(entry(t, m, take) + "\n" for t, m in items)
        block = "<!-- catalogue:start -->\n" + "\n".join(out) + "<!-- catalogue:end -->"
        with open(path, encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r"<!-- catalogue:start -->.*?<!-- catalogue:end -->", lambda _: block, text, flags=re.S)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("updated", note, sum(1 for t, m in manifest.items() if m["category"] in dict(sections)))


if __name__ == "__main__":
    main()
