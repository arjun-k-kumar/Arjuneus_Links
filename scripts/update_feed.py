#!/usr/bin/env python3
"""Pulls the latest Instagram posts + profile photo and saves them locally,
so the link page never shows expired images. Runs daily via GitHub Actions."""
import json, os, pathlib, urllib.request, urllib.parse

TOKEN = os.environ["IG_TOKEN"]
API = "https://graph.instagram.com"
OUT = pathlib.Path("feed"); OUT.mkdir(exist_ok=True)

def get(path, **params):
    params["access_token"] = TOKEN
    with urllib.request.urlopen(f"{API}/{path}?{urllib.parse.urlencode(params)}", timeout=30) as r:
        return json.load(r)

def save(url, name):
    with urllib.request.urlopen(url, timeout=30) as r:
        (OUT / name).write_bytes(r.read())
    return f"feed/{name}"

me = get("me", fields="username")   # profile photo is built into index.html

media = get("me/media", fields="id,caption,media_type,media_url,thumbnail_url,permalink,timestamp", limit=12)["data"]
posts = []
for m in media:
    img = m.get("thumbnail_url") if m["media_type"] == "VIDEO" else m.get("media_url")
    if not img:
        continue
    posts.append({"permalink": m["permalink"], "caption": m.get("caption", ""),
                  "timestamp": m["timestamp"], "image": save(img, f"post_{len(posts)}.jpg")})
    if len(posts) == 6:
        break

(OUT / "feed.json").write_text(json.dumps({"username": me.get("username"), "posts": posts}, indent=2))

# Keep the 60-day token alive (Instagram allows a refresh once it is 24h+ old).
try:
    new = get("refresh_access_token", grant_type="ig_refresh_token").get("access_token")
    if new and new != TOKEN:
        pathlib.Path(".newtoken").write_text(new)   # picked up by the workflow, never committed
except Exception as e:
    print("token refresh skipped:", e)
print(f"saved {len(posts)} posts")
