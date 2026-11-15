"""Usage: [VOICE=elevenlabs:<voice_id>] python build.py videos.v001_zinseszins.scenes [--preview]"""
import json, sys
from pathlib import Path
from PIL import ImageDraw
from lib import engine, gfx

mod = sys.argv[1]
slug = mod.split(".")[1]
work = Path("build") / slug
out = Path("output") / slug
out.mkdir(parents=True, exist_ok=True)
import os
# VOICE=google:de-DE-Chirp3-HD-<Name> or VOICE=elevenlabs:<voice_id>, otherwise the offline Piper voice
voice = os.environ.get("VOICE", "google:de-DE-Chirp3-HD-Iapetus")

if "--preview" in sys.argv:
    from importlib import import_module
    scenes = import_module(mod).scenes()
    tj = work / "timing.json"
    if tj.exists():
        for s, m in zip(scenes, json.loads(tj.read_text())):
            s.cues, s.ends, s.dur, s.start = m["cues"], m["ends"], m["dur"], m["start"]
    else:
        work.mkdir(parents=True, exist_ok=True)
        engine.build_audio(scenes, voice, work)
        tj.write_text(json.dumps([dict(name=s.name, cues=s.cues, ends=s.ends, dur=s.dur, start=s.start) for s in scenes]))
    bg = gfx.make_background()
    pv = work / "preview"; pv.mkdir(exist_ok=True)
    for i, s in enumerate(scenes):
        img = bg.copy(); s.draw(img, ImageDraw.Draw(img), s.dur - 0.4, s)
        img.save(pv / f"{i:02}_{s.name}_end.png")
        img = bg.copy(); s.draw(img, ImageDraw.Draw(img), s.dur * 0.55, s)
        img.save(pv / f"{i:02}_{s.name}_mid.png")
    print("previews in", pv)
else:
    engine.build(mod, voice, work, out / "video.mp4")
