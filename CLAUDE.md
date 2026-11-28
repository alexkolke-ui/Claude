# Rechenweg – YouTube-Kanal (@derrechenweg)

Deutschsprachiger Erklärkanal zu Geld & Wirtschaft. Videos werden komplett per Code erzeugt:
Skript → Google-TTS (Stimme `de-DE-Chirp3-HD-Iapetus`) → PIL-Animationen → ffmpeg → Upload per YouTube Data API.

## Umgebung (Cloud-Umgebung „Claude (Rechenweg)“)
- Variablen: `VOICE`, `YT_CLIENT_ID` (gesetzt); `GOOGLE_TTS_API_KEY`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (vom Nutzer als Geheimnisse hinterlegt).
- Fehlt eine davon, den Nutzer bitten, sie in den Umgebungseinstellungen einzutragen – nie im Chat erfragen, nie committen.
- Nicht verfügbar: ElevenLabs (Free-Tier blockiert Cloud-IPs), Edge-TTS.

## Workflow für ein neues Video
1. `videos/vNNN_slug/scenes.py` anlegen (Vorlage: `videos/v001_zinseszins/scenes.py`). Jede gesprochene Zahl
   muss per `assert` gegen das Modell geprüft werden. Zahlen in der Narration als Wörter schreiben.
2. `python3 build.py videos.vNNN_slug.scenes --preview` → Einzelbilder in `build/vNNN_slug/preview/` prüfen (Überlappungen!).
3. `python3 build.py videos.vNNN_slug.scenes` → `output/vNNN_slug/video.mp4` + `video.srt`.
   TTS wird in `build/tts_cache/` zwischengespeichert (kostet beim Neu-Rendern kein Kontingent).
4. Thumbnail-Skript + `metadata.md` (Struktur wie v001; Kapitel aus `build/<slug>/timing.json`).
   Neues Langvideo in die passende Themen-Playlist in `brand/playlists.json` eintragen, nach dem Upload
   `python3 -m lib.playlists` (idempotent).
5. Upload: `python3 -m lib.youtube upload videos/vNNN_slug` → landet als **privat** (API-Projekt ungeprüft);
   der Nutzer veröffentlicht selbst. Nie ohne Rückfrage öffentlich schalten.
   Einplanen nur mit vom Nutzer bestätigtem Termin: `--publish-at "YYYY-MM-DD HH:MM"` beim Upload oder
   `python3 -m lib.youtube schedule videos/<slug> "YYYY-MM-DD HH:MM"` (Europe/Berlin, bleibt bis dahin privat).
   Keine `<` oder `>` in der Beschreibung (YouTube lehnt sie ab: invalidDescription).
   `invalid_grant` = Refresh-Token abgelaufen → `auth-url`/`auth-code`, Nutzer trägt neuen `YT_REFRESH_TOKEN` ein.
   `quotaExceeded` = Tageskontingent der API weg (Reset 0:00 Pacific = 9:00 MEZ). Fehlende Untertitel mit
   `python3 -m lib.youtube captions videos/<slug>` nachholen; die Video-ID steht in `output/<slug>/youtube_id.txt`.

## Shorts
- Formate in `lib/shorts.py` (`zahl`, `mythos`, `vergleich`); Brutto-Netto 2026 nach BMF-PAP in `lib/lohn2026.py`.
- `videos/sNNN_slug/scenes.py` mit `SIZE = (1080, 1920)` (Engine/Preview lesen das automatisch), eine Szene, 30–45 s.
- Inhalt nur im sicheren Bereich: x 60–940, y 200–1470 (rechts Buttons, unten Titel-Overlay).
- Zahlen aus dem Modell des Langvideos importieren (dessen `assert`s gelten mit), eigene `assert`s für Gesagtes.
- Rhythmus (ab 30.11.2026): 1 Langvideo Do 17:30 + 4–5 Shorts (Mo, Di, Mi, Sa, So, je 17:00).
  „Verknüpftes Video“ geht nicht per API – setzt der Nutzer im Studio (Checkliste: `docs/verknuepfte-videos.md`).
  Jede Short-Beschreibung bekommt unter dem ersten Absatz „▶ Ganzes Video: https://youtu.be/<ID des Langvideos>“.
- Formate abwechseln, nicht 5× dieselbe Kartenoptik: „Zahl der Woche“, „Mythos vs. Rechnung“, „Was kostet X wirklich?“.

## Inhaltliche Regeln
- Keine Anlageberatung, keine Produktempfehlungen; Annahmen + Formeln immer in die Beschreibung.
- Simulierte Daten als solche kennzeichnen; echte Daten mit Quelle.
- KI-Stimme offenlegen (Beschreibung + `containsSyntheticMedia`).
- Branding: `brand/make_brand.py`, Kanaltexte: `brand/kanal-setup.md`.
