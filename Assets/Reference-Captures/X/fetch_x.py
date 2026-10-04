"""Fetch X/Twitter posts (text, stats, images, best-quality video) into the vault.

Uses X's public embed endpoint (cdn.syndication.twimg.com), so no login or API key is needed.
Run with Blender's bundled Python (stdlib only):
  "C:/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe" fetch_x.py ids.txt
ids.txt lines: <tweet id or URL> <category> [free-text note]
Output: X/<category>/<handle>-<id>/ with post.json, img-N.jpg, vid-N.mp4; and X/manifest.json.
Already-fetched posts are skipped.
"""
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "manifest.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def token(tid: str) -> str:
    # Mirrors react-tweet: ((id / 1e15) * PI).toString(36) with zeros and dot stripped.
    x = (int(tid) / 1e15) * 3.141592653589793
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    ip, fp = int(x), x - int(x)
    s = ""
    while ip:
        s = digits[ip % 36] + s
        ip //= 36
    s = (s or "0") + "."
    for _ in range(12):
        fp *= 36
        s += digits[int(fp)]
        fp -= int(fp)
    return re.sub(r"(0+|\.)", "", s)


def best_video(media: dict) -> str | None:
    vs = [v for v in media.get("video_info", {}).get("variants", []) if v.get("content_type") == "video/mp4"]
    if not vs:
        return None
    return max(vs, key=lambda v: v.get("bitrate", 0))["url"]


def load_manifest() -> dict:
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as f:
            return json.load(f)
    return {}


def fetch(tid: str, category: str, note: str, manifest: dict) -> None:
    if tid in manifest:
        print("skip", tid)
        return
    data = json.loads(get(f"https://cdn.syndication.twimg.com/tweet-result?id={tid}&lang=en&token={token(tid)}"))
    if data.get("__typename") != "Tweet":
        print("unavailable", tid, data.get("__typename"))
        return
    user = data["user"]["screen_name"]
    folder = os.path.join(ROOT, category, f"{user}-{tid}")
    os.makedirs(folder, exist_ok=True)
    files = []
    media = data.get("mediaDetails", [])
    for i, m in enumerate(media, 1):
        if m.get("type") == "photo":
            url, name = m["media_url_https"] + "?name=orig", f"img-{i}.jpg"
        else:
            url, name = best_video(m), f"vid-{i}.mp4"
            # Also keep the poster frame as a quick-look still.
            with open(os.path.join(folder, f"poster-{i}.jpg"), "wb") as f:
                f.write(get(m["media_url_https"] + "?name=orig"))
            files.append(f"poster-{i}.jpg")
        if url:
            with open(os.path.join(folder, name), "wb") as f:
                f.write(get(url))
            files.append(name)
    with open(os.path.join(folder, "post.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    manifest[tid] = {
        "url": f"https://x.com/{user}/status/{tid}",
        "author": user,
        "name": data["user"].get("name"),
        "date": data.get("created_at", "")[:10],
        "likes": data.get("favorite_count"),
        "replies": data.get("conversation_count"),
        "text": data.get("text"),
        "category": category,
        "note": note,
        "folder": os.path.relpath(folder, ROOT).replace("\\", "/"),
        "files": files,
    }
    print("ok", tid, user, data.get("favorite_count"), files)


def main() -> None:
    manifest = load_manifest()
    with open(sys.argv[1], encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    for line in lines:
        parts = line.split(maxsplit=2)
        m = re.search(r"status/(\d+)", parts[0]) or re.fullmatch(r"(\d{8,})", parts[0])
        if not m:
            continue
        try:
            fetch(m.group(1), parts[1] if len(parts) > 1 else "misc", parts[2] if len(parts) > 2 else "", manifest)
        except Exception as e:  # keep going; report at the end
            print("error", m.group(1), e)
        # Write-then-rename so readers never see a half-written manifest.
        with open(MANIFEST + ".tmp", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=1, ensure_ascii=False)
        os.replace(MANIFEST + ".tmp", MANIFEST)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
