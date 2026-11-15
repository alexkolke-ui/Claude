# Nachgerechnet – YouTube-Produktionspipeline

Code-generierte Erklärvideos (Finanzen/Wirtschaft, deutsch): Skript → Offline-TTS (Piper) → Animationen (PIL) → ffmpeg.

```bash
pip install piper-tts pillow numpy
# Stimme nach voices/ legen (github.com/rhasspy/piper, Release v0.0.2: voice-de-thorsten-low.tar.gz)
python3 build.py videos.v001_zinseszins.scenes --preview   # Einzelbilder zur Kontrolle
python3 build.py videos.v001_zinseszins.scenes             # -> output/v001_zinseszins/video.mp4 + .srt
VOICE=elevenlabs:<voice_id> python3 build.py videos.v001_zinseszins.scenes   # mit ElevenLabs-Stimme (Key via Proxy oder ELEVENLABS_API_KEY)
python3 videos/v001_zinseszins/thumbnail.py
```

- `lib/` – TTS, Grafik-Toolkit, Szenen-Engine (Timing aus der Sprachspur, paralleles Rendern, Untertitel, Musikbett)
- `videos/vNNN_*/` – pro Video: `scenes.py` (Text + Animation), `thumbnail.py`, `metadata.md`

Kanalstimme: `VOICE=google:de-DE-Chirp3-HD-Iapetus` (Google Cloud TTS, Key via `GOOGLE_TTS_API_KEY` oder Network Secret für `texttospeech.googleapis.com`).
