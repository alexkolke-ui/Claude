"""Playlists anlegen/ergänzen nach brand/playlists.json (idempotent: legt nur Fehlendes an).

Usage: python3 -m lib.playlists [--dry-run]
"""
import json
import sys
import time
from pathlib import Path

from .youtube import _api, access_token

API = "https://www.googleapis.com/youtube/v3/"


def _try(fn, tries=4, wait=3):
    """YouTube meldet bei frisch angelegten Playlists kurz 404/409 – mehrfach versuchen."""
    for i in range(tries):
        try:
            return fn()
        except SystemExit as e:
            if i == tries - 1:
                raise
            print("   (wiederhole:", str(e)[:60].replace("\n", " "), ")")
            time.sleep(wait * (i + 1))


def _vid(entry):
    p = Path("output") / entry / "youtube_id.txt"
    return p.read_text().strip() if p.exists() else (entry if len(entry) == 11 else None)


def main(dry=False):
    cfg = json.loads(Path("brand/playlists.json").read_text(encoding="utf-8"))
    tok = access_token()
    have = {p["snippet"]["title"]: p["id"] for p in
            _api("GET", API + "playlists?part=snippet&mine=true&maxResults=50", token=tok).get("items", [])}
    for pl in cfg["playlists"]:
        pid = have.get(pl["title"])
        if not pid:
            print("neu:", pl["title"])
            if dry:
                continue
            body = {"snippet": {"title": pl["title"], "description": pl["description"], "defaultLanguage": "de"},
                    "status": {"privacyStatus": "public"}}
            pid = _api("POST", API + "playlists?part=snippet,status", body, token=tok)["id"]
        new = pl["title"] not in have
        items = {"items": []} if (new or not pid) else _try(
            lambda: _api("GET", API + f"playlistItems?part=contentDetails&maxResults=50&playlistId={pid}", token=tok))
        present = {i["contentDetails"]["videoId"] for i in items.get("items", [])}
        for entry in pl["videos"]:
            vid = _vid(entry)
            if not vid:
                print("  fehlt (noch nicht hochgeladen):", entry)
                continue
            if vid in present:
                continue
            print("  +", entry)
            if not dry:
                _try(lambda: _api("POST", API + "playlistItems?part=snippet",
                                  {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}},
                                  token=tok))
        if pid:
            print(f"  https://www.youtube.com/playlist?list={pid}")


if __name__ == "__main__":
    main(dry="--dry-run" in sys.argv)
