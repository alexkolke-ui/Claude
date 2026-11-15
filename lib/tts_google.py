"""Google Cloud Text-to-Speech backend (Chirp 3 HD voices).
Key: env GOOGLE_TTS_API_KEY, or injected by the session proxy as x-goog-api-key."""
import base64
import hashlib
import json
import os
import urllib.request
from pathlib import Path

import numpy as np

SR = 24000
CACHE = Path("build/tts_cache")


def synth(text, voice, speaking_rate=1.0):
    body = {"input": {"text": text},
            "voice": {"languageCode": voice[:5], "name": voice},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR,
                            "speakingRate": speaking_rate}}
    key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:24]
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"g_{key}.pcm"
    if not f.exists():   # cache: re-renders don't use quota again
        req = urllib.request.Request(
            "https://texttospeech.googleapis.com/v1/text:synthesize",
            data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "x-goog-api-key": os.environ.get("GOOGLE_TTS_API_KEY", "proxy-injected")})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                wav = base64.b64decode(json.load(r)["audioContent"])
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Google TTS {e.code}: {e.read()[:300]!r}") from None
        f.write_bytes(wav[44:])  # strip WAV header
    audio = np.frombuffer(f.read_bytes(), np.int16).astype(np.float32) / 32768
    idx = np.where(np.abs(audio) > 0.01)[0]
    if len(idx):
        audio = audio[max(0, idx[0] - 400): idx[-1] + 1200]
    return audio, SR
