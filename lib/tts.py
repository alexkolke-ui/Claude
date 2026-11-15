"""Offline German TTS via Piper, with a fix for the 'ç' phoneme (e.g. '-zig')."""
import wave
from pathlib import Path

import numpy as np

_VOICE = None


def _voice(model_path):
    global _VOICE
    if _VOICE is None:
        from piper import PiperVoice  # optional dependency (offline fallback voice)
        _VOICE = PiperVoice.load(str(model_path))
    return _VOICE


def _fix(phonemes):
    out = []
    for p in phonemes:
        if p == "̧" and out and out[-1] == "c":  # c + combining cedilla -> ç
            out[-1] = "ç"
        else:
            out.append(p)
    return out


def synth(text, model_path, length_scale=1.08):
    """Return float32 mono audio and sample rate for one sentence."""
    from piper.config import SynthesisConfig
    v = _voice(model_path)
    cfg = SynthesisConfig(length_scale=length_scale, noise_scale=0.6, noise_w_scale=0.7,
                          normalize_audio=False)
    parts = []
    for ph in v.phonemize(text):
        if not ph:
            continue
        a = v.phoneme_ids_to_audio(v.phonemes_to_ids(_fix(ph)), cfg)
        if isinstance(a, tuple):
            a = a[0]
        parts.append(np.asarray(a, dtype=np.float32))
    audio = np.concatenate(parts) if parts else np.zeros(1, np.float32)
    return audio, v.config.sample_rate


def write_wav(path, audio, sr):
    pcm = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
