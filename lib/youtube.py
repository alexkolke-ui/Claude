"""Minimal YouTube Data API v3 client (stdlib only): OAuth for installed apps, resumable
video upload, thumbnail and caption upload.

Usage:
  python3 -m lib.youtube auth-url                      # prints the consent URL
  python3 -m lib.youtube auth-code '<redirect URL or code>'
  python3 -m lib.youtube upload videos/v001_zinseszins [--publish-at "2026-12-03 17:30"]
  python3 -m lib.youtube schedule videos/v001_zinseszins "2026-12-03 17:30"   # bereits hochgeladenes Video
  (Zeiten in Europe/Berlin; das Video bleibt bis dahin privat und geht dann automatisch online)

Needs env YT_CLIENT_ID / YT_CLIENT_SECRET (OAuth client of type "Desktop app").
The refresh token is stored in build/.youtube_token.json (not committed).
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

REDIRECT = "http://127.0.0.1:8765"
SCOPES = ("https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.force-ssl "
          "https://www.googleapis.com/auth/yt-analytics.readonly")
TOKEN_FILE = Path("build/.youtube_token.json")


def _client():
    try:
        return os.environ["YT_CLIENT_ID"], os.environ["YT_CLIENT_SECRET"]
    except KeyError:
        sys.exit("YT_CLIENT_ID / YT_CLIENT_SECRET fehlen")


def _post_form(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"OAuth-Fehler {e.code}: {e.read().decode()[:400]}")


def auth_url():
    cid, _ = _client()
    q = dict(client_id=cid, redirect_uri=REDIRECT, response_type="code", scope=SCOPES,
             access_type="offline", prompt="consent")
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(q)


def exchange(code_or_url):
    m = re.search(r"[?&]code=([^&]+)", code_or_url)
    code = urllib.parse.unquote(m.group(1)) if m else code_or_url.strip()
    cid, sec = _client()
    tok = _post_form("https://oauth2.googleapis.com/token", dict(
        code=code, client_id=cid, client_secret=sec, redirect_uri=REDIRECT,
        grant_type="authorization_code"))
    if "refresh_token" not in tok:
        sys.exit(f"Kein Refresh-Token erhalten: {tok}")
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps({"refresh_token": tok["refresh_token"]}))
    os.chmod(TOKEN_FILE, 0o600)
    print("OK – Zugang gespeichert. Kanal:", channel()["snippet"]["title"])
    print(f"Neuen Token als Geheimnis YT_REFRESH_TOKEN übernehmen: Wert steht in {TOKEN_FILE}")


def access_token():
    # A token from a fresh auth-code in this container wins over the (possibly older) env secret.
    rt = (json.loads(TOKEN_FILE.read_text())["refresh_token"] if TOKEN_FILE.exists()
          else os.environ.get("YT_REFRESH_TOKEN"))
    if not rt:
        sys.exit("Kein Refresh-Token: YT_REFRESH_TOKEN setzen oder auth-url/auth-code ausführen")
    cid, sec = _client()
    return _post_form("https://oauth2.googleapis.com/token", dict(
        refresh_token=rt, client_id=cid, client_secret=sec, grant_type="refresh_token"))["access_token"]


def _api(method, url, body=None, headers=None, token=None, raw=False):
    h = {"Authorization": f"Bearer {token or access_token()}"}
    h.update(headers or {})
    data = body if isinstance(body, (bytes, type(None))) else json.dumps(body).encode()
    if data is not None and not isinstance(body, bytes):
        h.setdefault("Content-Type", "application/json; charset=UTF-8")
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        r = urllib.request.urlopen(req, timeout=600)
    except urllib.error.HTTPError as e:
        sys.exit(f"YouTube-API-Fehler {e.code} bei {url.split('?')[0]}: {e.read().decode()[:600]}")
    return r if raw else json.load(r)


def channel():
    return _api("GET", "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true")["items"][0]


def parse_metadata(md_path):
    md = Path(md_path).read_text(encoding="utf-8")
    sec = {m.group(1).strip(): m.group(2).strip()
           for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", md, re.S | re.M)}
    title = next(l for l in sec["Titel (max. 100 Zeichen)"].splitlines() if l.strip())
    tags = [t.strip() for t in sec["Tags"].split(",") if t.strip()]
    desc = sec["Beschreibung"]
    assert len(title) <= 100 and len(desc) <= 5000 and len(", ".join(tags)) <= 500
    return title, desc, tags


def publish_at_utc(local):
    """'YYYY-MM-DD HH:MM' in Europe/Berlin -> RFC3339 UTC, must lie in the future."""
    import datetime as dt
    from zoneinfo import ZoneInfo
    t = dt.datetime.strptime(local, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Europe/Berlin"))
    if t <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30):
        sys.exit(f"Veröffentlichungszeit {local} liegt nicht mindestens 30 min in der Zukunft")
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def schedule(video_dir, local):
    """Set publishAt on an already uploaded video (id from output/<slug>/youtube_id.txt)."""
    vid = (Path("output") / Path(video_dir).name / "youtube_id.txt").read_text().strip()
    token = access_token()
    cur = _api("GET", f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}", token=token)["items"][0]
    st = cur["status"]
    if st["privacyStatus"] != "private":
        sys.exit(f"{vid} ist {st['privacyStatus']} – nur private Videos werden eingeplant")
    keep = ("embeddable", "license", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")
    status = {k: st[k] for k in keep if k in st}
    status.update(privacyStatus="private", publishAt=publish_at_utc(local))
    res = _api("PUT", "https://www.googleapis.com/youtube/v3/videos?part=status", {"id": vid, "status": status},
               token=token)
    print(vid, "eingeplant:", res["status"].get("publishAt"), "Status:", res["status"]["privacyStatus"])


def upload(video_dir, public=False, publish_at=None):
    video_dir = Path(video_dir)
    slug = video_dir.name
    out = Path("output") / slug
    title, desc, tags = parse_metadata(video_dir / "metadata.md")
    token = access_token()
    meta = {
        "snippet": {"title": title, "description": desc, "tags": tags, "categoryId": "27",
                    "defaultLanguage": "de", "defaultAudioLanguage": "de"},
        "status": {"privacyStatus": "public" if public else "private",
                   **({"publishAt": publish_at_utc(publish_at)} if publish_at and not public else {}),
                   "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True,
                   "embeddable": True, "license": "youtube"},
    }
    video = out / "video.mp4"
    size = video.stat().st_size
    r = _api("POST", "https://www.googleapis.com/upload/youtube/v3/videos"
             "?uploadType=resumable&part=snippet,status", meta, token=token, raw=True,
             headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = r.headers["Location"]
    print(f"Lade {size / 1e6:.1f} MB hoch …")
    res = _api("PUT", loc, video.read_bytes(), token=token,
               headers={"Content-Type": "video/mp4"})
    vid = res["id"]
    print("Video:", f"https://youtu.be/{vid}", "Status:", res["status"]["privacyStatus"],
          "geplant:", res["status"].get("publishAt", "–"))

    thumb = out / "thumbnail.png"
    if thumb.exists():
        _api("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}"
             "&uploadType=media", thumb.read_bytes(), token=token,
             headers={"Content-Type": "image/png"})
        print("Thumbnail gesetzt")

    srt = out / "video.srt"
    if srt.exists():
        boundary = uuid.uuid4().hex
        part_meta = json.dumps({"snippet": {"videoId": vid, "language": "de", "name": "Deutsch"}})
        body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{part_meta}\r\n"
                f"--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() \
            + srt.read_bytes() + f"\r\n--{boundary}--".encode()
        _api("POST", "https://www.googleapis.com/upload/youtube/v3/captions"
             "?uploadType=multipart&part=snippet", body, token=token,
             headers={"Content-Type": f"multipart/related; boundary={boundary}"})
        print("Untertitel hochgeladen")
    (out / "youtube_id.txt").write_text(vid)
    return vid


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "auth-url":
        print(auth_url())
    elif cmd == "auth-code":
        exchange(sys.argv[2])
    elif cmd == "upload":
        pa = sys.argv[sys.argv.index("--publish-at") + 1] if "--publish-at" in sys.argv else None
        upload(sys.argv[2], public="--public" in sys.argv, publish_at=pa)
    elif cmd == "schedule":
        schedule(sys.argv[2], sys.argv[3])
    elif cmd == "check":
        print(parse_metadata(Path(sys.argv[2]) / "metadata.md"))
    else:
        print(__doc__)
