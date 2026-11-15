"""ElevenLabs TTS backend. The API key is injected by the session's network proxy
(header xi-api-key); locally, set ELEVENLABS_API_KEY instead."""
import hashlib
import json
import os
import subprocess
import urllib.request
from pathlib import Path

import numpy as np

SR = 44100
CACHE = Path("build/tts_cache")
MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")


def synth(text, voice_id, prev_text=None, next_text=None,
          stability=0.5, similarity=0.75, style=0.15, speed=1.0):
    body = {"text": text, "model_id": MODEL,
            "voice_settings": {"stability": stability, "similarity_boost": similarity,
                               "style": style, "use_speaker_boost": True, "speed": speed}}
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    key = hashlib.sha256(json.dumps([voice_id, body], sort_keys=True).encode()).hexdigest()[:24]
    CACHE.mkdir(parents=True, exist_ok=True)
    mp3 = CACHE / f"{key}.mp3"
    if not mp3.exists():   # cache: re-renders never cost characters twice
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                mp3.write_bytes(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"ElevenLabs {e.code}: {e.read()[:300]!r}") from None
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.float32).copy()
    # trim leading/trailing silence so sentence cues stay tight
    idx = np.where(np.abs(audio) > 0.01)[0]
    if len(idx):
        audio = audio[max(0, idx[0] - 800): idx[-1] + 2200]
    return audio, SR
