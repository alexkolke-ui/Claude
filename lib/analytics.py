"""Channel report from the YouTube Data API + YouTube Analytics API.

Usage:
  python3 -m lib.analytics [TAGE]        # default 28; writes reports/YYYY-MM-DD.md and prints it

Needs the scope yt-analytics.readonly (python3 -m lib.youtube auth-url / auth-code) and the
"YouTube Analytics API" enabled in the Google Cloud project. Analytics data lags ~2-3 days.
"""
import datetime as dt
import sys
import urllib.parse
from pathlib import Path

from .youtube import _api, access_token

ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports?"
DATA = "https://www.googleapis.com/youtube/v3/"
TRAFFIC = {"SHORTS": "Shorts-Feed", "YT_SEARCH": "YouTube-Suche", "RELATED_VIDEO": "Vorgeschlagene Videos",
           "BROWSE": "Startseite/Abos", "SUBSCRIBER": "Abo-Feed", "EXT_URL": "Externe Links",
           "NO_LINK_OTHER": "Direkt/Unbekannt", "YT_CHANNEL": "Kanalseite", "PLAYLIST": "Playlists",
           "NOTIFICATION": "Benachrichtigungen", "END_SCREEN": "Endcards", "YT_OTHER_PAGE": "Andere YouTube-Seiten"}


def report(token, start, end, metrics, dims=None, sort=None, max_results=None, filters=None):
    q = dict(ids="channel==MINE", startDate=str(start), endDate=str(end), metrics=metrics)
    if dims:
        q["dimensions"] = dims
    if sort:
        q["sort"] = sort
    if max_results:
        q["maxResults"] = max_results
    if filters:
        q["filters"] = filters
    r = _api("GET", ANALYTICS + urllib.parse.urlencode(q), token=token)
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]


def mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02}"


def n(v):
    return f"{v:,.0f}".replace(",", ".")


def build(days=28):
    tok = access_token()
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    ch = _api("GET", DATA + "channels?part=snippet,statistics,contentDetails&mine=true", token=tok)["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = _api("GET", DATA + f"playlistItems?part=contentDetails&maxResults=50&playlistId={uploads}",
                 token=tok)["items"]
    ids = ",".join(i["contentDetails"]["videoId"] for i in items)
    vids = {v["id"]: v for v in _api("GET", DATA + f"videos?part=snippet,statistics,status,contentDetails&id={ids}",
                                     token=tok)["items"]} if ids else {}

    tot = report(tok, start, end, "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,"
                 "subscribersLost,likes,comments,shares")
    per = report(tok, start, end, "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,"
                 "subscribersGained,likes,comments", "video", "-views", 50)
    src = report(tok, start, end, "views,estimatedMinutesWatched", "insightTrafficSourceType", "-views")
    geo = report(tok, start, end, "views", "country", "-views", 5)
    dev = report(tok, start, end, "views", "deviceType", "-views")

    L = [f"# Kanalbericht {ch['snippet']['title']} – {end}", "",
         f"Zeitraum: {start} bis {end} ({days} Tage). Analytics-Daten hängen ca. 2–3 Tage hinterher.", "",
         f"**Gesamt (Data API, live):** {n(int(ch['statistics']['subscriberCount']))} Abos · "
         f"{n(int(ch['statistics']['viewCount']))} Aufrufe · {ch['statistics']['videoCount']} öffentliche Videos", ""]
    if tot:
        t = tot[0]
        L += ["## Zeitraum", "",
              f"- Aufrufe: {n(t['views'])} · Wiedergabezeit: {n(t['estimatedMinutesWatched'] / 60)} h · "
              f"Ø Wiedergabedauer: {mmss(t['averageViewDuration'])}",
              f"- Abos: +{n(t['subscribersGained'])} / −{n(t['subscribersLost'])} · Likes {n(t['likes'])} · "
              f"Kommentare {n(t['comments'])} · Geteilt {n(t['shares'])}", ""]
    L += ["## Videos", "", "| Video | Status | Aufrufe | Ø Dauer | Ø gesehen | Abos+ | Likes | Komm. |",
          "|---|---|---:|---:|---:|---:|---:|---:|"]
    seen = set()
    for r in per:
        v = vids.get(r["video"])
        title = v["snippet"]["title"][:55] if v else r["video"]
        status = v["status"]["privacyStatus"] if v else "?"
        seen.add(r["video"])
        L.append(f"| {title} | {status} | {n(r['views'])} | {mmss(r['averageViewDuration'])} | "
                 f"{r['averageViewPercentage']:.0f} % | {n(r['subscribersGained'])} | {n(r['likes'])} | "
                 f"{n(r['comments'])} |")
    for vid, v in vids.items():
        if vid not in seen:
            st = v["status"]
            when = f" ({st['publishAt'][:16].replace('T', ' ')} UTC)" if st.get("publishAt") else ""
            L.append(f"| {v['snippet']['title'][:55]} | {st['privacyStatus']}{when} | "
                     f"{v['statistics'].get('viewCount', '0')} | – | – | – | – | – |")
    if src:
        total = sum(r["views"] for r in src) or 1
        L += ["", "## Zugriffsquellen", ""] + [
            f"- {TRAFFIC.get(r['insightTrafficSourceType'], r['insightTrafficSourceType'])}: "
            f"{n(r['views'])} ({100 * r['views'] / total:.0f} %)" for r in src]
    if geo:
        L += ["", "## Top-Länder", "", ", ".join(f"{r['country']} {n(r['views'])}" for r in geo)]
    if dev:
        L += ["", "## Geräte", "", ", ".join(f"{r['deviceType'].lower()} {n(r['views'])}" for r in dev)]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    md = build(days)
    out = Path("reports") / f"{dt.date.today()}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(md)
    print("gespeichert:", out)
