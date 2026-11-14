"""Scene engine: narration -> timing -> parallel frame rendering -> final MP4 + SRT."""
import json
import math
import subprocess
from dataclasses import dataclass, field
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import ImageDraw

from . import gfx, tts

LEAD = 0.45      # silence before first sentence of a scene
GAP = 0.38       # pause between sentences
TAIL = 0.75      # pause after last sentence
OUT_SR = 48000


@dataclass
class Scene:
    name: str
    sentences: list
    draw: callable
    cues: list = field(default_factory=list)   # sentence start times (scene-relative)
    ends: list = field(default_factory=list)   # sentence end times
    dur: float = 0.0
    start: float = 0.0                          # global start time
    extra: float = 0.0                          # extra hold time at the end

    def c(self, i):
        return self.cues[i]

    def e(self, i):
        return self.ends[i]


def build_audio(scenes, voice, workdir):
    sr = None
    tracks = []
    t_global = 0.0
    for sc in scenes:
        pieces, t = [], LEAD
        sc.cues, sc.ends = [], []
        for s in sc.sentences:
            a, sr = tts.synth(s, voice)
            sc.cues.append(t)
            t += len(a) / sr
            sc.ends.append(t)
            pieces.append(a)
            t += GAP
        t = t - GAP + TAIL + sc.extra
        frames = math.ceil(t * gfx.FPS)
        sc.dur = frames / gfx.FPS
        sc.start = t_global
        buf = np.zeros(int(round(sc.dur * sr)), np.float32)
        for a, c in zip(pieces, sc.cues):
            i = int(round(c * sr))
            buf[i:i + len(a)] += a[: len(buf) - i]
        tracks.append(buf)
        t_global += sc.dur
    audio = np.concatenate(tracks)
    peak = np.max(np.abs(audio)) or 1
    audio = audio / peak * 0.9
    path = Path(workdir) / "voice.wav"
    tts.write_wav(path, audio, sr)
    return path, t_global


def music_bed(duration, path, sr=OUT_SR):
    """Quiet, slowly evolving synth pad (generated, royalty-free)."""
    n = int(duration * sr)
    t = np.arange(n) / sr
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66],
              [164.81, 207.65, 246.94]]  # Am F G E
    seg = 8.0
    out = np.zeros(n, np.float32)
    for k in range(int(duration / seg) + 2):
        f = chords[k % len(chords)]
        s0 = k * seg - 1.5
        i0, i1 = max(0, int(s0 * sr)), min(n, int((s0 + seg + 3) * sr))
        if i0 >= i1:
            continue
        tt = t[i0:i1] - s0
        env = np.clip(tt / 2.5, 0, 1) * np.clip((seg + 3 - tt) / 2.5, 0, 1)
        sig = np.zeros_like(tt)
        for fr in f:
            for det in (-0.6, 0.6):
                sig += np.sin(2 * np.pi * (fr / 2 + det) * tt)
            sig += 0.3 * np.sin(2 * np.pi * fr * tt)
        out[i0:i1] += (sig * env).astype(np.float32)
    out *= 0.85 + 0.15 * np.sin(2 * np.pi * t / 11.0)
    fade = np.clip(np.minimum(t / 2.0, (duration - t) / 3.0), 0, 1)
    out = out * fade
    out = out / (np.max(np.abs(out)) or 1) * 0.9
    tts.write_wav(path, out, sr)


def _render_scene(args):
    module_name, idx, scene_meta, out = args
    import importlib
    mod = importlib.import_module(module_name)
    scenes = mod.scenes()
    sc = scenes[idx]
    for k, v in scene_meta.items():
        setattr(sc, k, v)
    bg = gfx.make_background()
    frames = int(round(sc.dur * gfx.FPS))
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{gfx.W}x{gfx.H}", "-r", str(gfx.FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out],
        stdin=subprocess.PIPE)
    for f in range(frames):
        t = f / gfx.FPS
        img = bg.copy()
        d = ImageDraw.Draw(img)
        sc.draw(img, d, t, sc)
        # short fade at scene borders
        a = min(1.0, t / 0.25, (sc.dur - t) / 0.25)
        if a < 1.0:
            img = gfx.Image.blend(bg, img, max(0.0, a))
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    return out


def srt_time(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def write_srt(scenes, path):
    lines, n = [], 1
    for sc in scenes:
        for s, c, e in zip(sc.sentences, sc.cues, sc.ends):
            lines += [str(n), f"{srt_time(sc.start + c)} --> {srt_time(sc.start + e + 0.2)}", s, ""]
            n += 1
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def build(module_name, voice, workdir, out_mp4, only=None, music_db=-30):
    from importlib import import_module
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    scenes = import_module(module_name).scenes()
    voice_wav, total = build_audio(scenes, voice, workdir)
    meta = [dict(cues=s.cues, ends=s.ends, dur=s.dur, start=s.start) for s in scenes]
    (workdir / "timing.json").write_text(json.dumps(
        [dict(name=s.name, **m) for s, m in zip(scenes, meta)], indent=1))
    write_srt(scenes, Path(out_mp4).with_suffix(".srt"))
    print(f"Narration: {total:.1f}s in {len(scenes)} scenes")

    idxs = range(len(scenes)) if only is None else only
    jobs = [(module_name, i, meta[i], str(workdir / f"scene_{i:02}.mp4")) for i in idxs]
    with Pool(4) as pool:
        for o in pool.imap_unordered(_render_scene, jobs):
            print("rendered", o)
    if only is not None:
        return

    listfile = workdir / "list.txt"
    listfile.write_text("".join(f"file 'scene_{i:02}.mp4'\n" for i in range(len(scenes))))
    music = workdir / "music.wav"
    music_bed(total, music)
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-i", str(voice_wav), "-i", str(music),
         "-filter_complex",
         "[1:a]aresample=48000,highpass=f=70,lowpass=f=7600,"
         "acompressor=threshold=-18dB:ratio=3:attack=5:release=120,"
         "aecho=0.8:0.5:35:0.08[v];"
         f"[2:a]volume={music_db}dB[m];"
         "[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
         "-movflags", "+faststart", str(out_mp4)], check=True)
    print("done:", out_mp4)
