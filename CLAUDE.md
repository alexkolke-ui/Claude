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
5. Upload: `python3 -m lib.youtube upload videos/vNNN_slug` → landet als **privat** (API-Projekt ungeprüft);
   der Nutzer veröffentlicht selbst. Nie ohne Rückfrage öffentlich schalten.

## Shorts
- `videos/sNNN_slug/scenes.py` mit `SIZE = (1080, 1920)` (Engine/Preview lesen das automatisch), eine Szene, 30–45 s.
- Inhalt nur im sicheren Bereich: x 60–940, y 200–1470 (rechts Buttons, unten Titel-Overlay).
- Zahlen aus dem Modell des Langvideos importieren (dessen `assert`s gelten mit), eigene `assert`s für Gesagtes.
- Rhythmus: Langvideo Do 17:30, Short Mo; Planen + „Verknüpftes Video“ macht der Nutzer im Studio.

## Inhaltliche Regeln
- Keine Anlageberatung, keine Produktempfehlungen; Annahmen + Formeln immer in die Beschreibung.
- Simulierte Daten als solche kennzeichnen; echte Daten mit Quelle.
- KI-Stimme offenlegen (Beschreibung + `containsSyntheticMedia`).
- Branding: `brand/make_brand.py`, Kanaltexte: `brand/kanal-setup.md`.
