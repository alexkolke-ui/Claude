"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import AMBER, FG, VIOLET, RED, font, thick_line, dot
from videos.v001_zinseszins.scenes import ANNA, BEN, fv

W, H = 1280, 720
img = Image.new("RGB", (W, H), (13, 19, 33))
d = ImageDraw.Draw(img)
def px(age, v):
    return 640 + (age - 25) / 40 * 600, 660 - v / 540000 * 520
for f, start, col in ((lambda a: fv(200, .07, a - 25), 25, VIOLET), (lambda a: fv(200, .07, max(0, a - 35)), 25, AMBER)):
    pts = [px(a / 4, f(a / 4)) for a in range(100, 261)]
    thick_line(d, pts, col, 12)
    dot(d, pts[-1], 16, col)
d.text((1205, px(65, ANNA)[1]), "Start 25", font=font(38, "Black"), fill=VIOLET, anchor="rm")
d.text((1250, 560), "Start 35", font=font(38, "Black"), fill=AMBER, anchor="rt")
d.text((50, 70), "10 Jahre", font=font(130, "Black"), fill=FG)
d.text((50, 215), "zu spät:", font=font(130, "Black"), fill=FG)
d.rounded_rectangle((40, 400, 610, 560), 24, fill=(220, 38, 38))
d.text((325, 482), f"−{(ANNA - BEN) / 1000:.0f}.000 €", font=font(96, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((50, 600), "bei nur 200 € im Monat", font=font(44, "Bold"), fill=(170, 180, 200))
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v001_zinseszins/thumbnail.png")
