"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, BLUE, RED, GREEN, VIOLET, AMBER, font
from videos.v008_2026_in_zahlen.scenes import INF_AVG, VDP_YOY, pct

img = Image.new("RGB", (1280, 720), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 50), "2026", font=font(180, "Black"), fill=AMBER)
d.text((620, 95), "in Zahlen", font=font(96, "Black"), fill=FG)
d.text((620, 200), "der Jahresrückblick", font=font(48, "Bold"), fill=(170, 180, 200))
tiles = [("Inflation Ø", pct(INF_AVG), RED), ("EZB", "2,0→2,5 %", VIOLET), ("Bauzins", "3,91 %", BLUE),
         ("Immobilien", pct(100 * VDP_YOY, sign=True), GREEN)]
for i, (lab, v, col) in enumerate(tiles):
    x = 50 + i * 300
    d.rounded_rectangle((x, 380, x + 280, 640), 24, fill=(26, 35, 56))
    d.rounded_rectangle((x, 380, x + 280, 392), 6, fill=col)
    d.text((x + 140, 450), lab, font=font(38, "Bold"), fill=(170, 180, 200), anchor="mm")
    d.text((x + 140, 550), v, font=font(46 if len(v) > 6 else 72, "Black"), fill=col, anchor="mm")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v008_2026_in_zahlen/thumbnail.png")
