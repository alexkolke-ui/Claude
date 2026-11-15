"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, GREEN, RED, AMBER, font
from videos.v002_inflation_gehalt.scenes import NOM_19_25, CPI_19_25, REAL_19_25, pct

W, H = 1280, 720
img = Image.new("RGB", (W, H), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 60), "Mehr Gehalt,", font=font(110, "Black"), fill=FG)
d.text((50, 190), "weniger drin?", font=font(110, "Black"), fill=AMBER)
for y, label, val, col in ((370, "Lohn", NOM_19_25, GREEN), (520, "Preise", CPI_19_25, RED)):
    d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
    d.text((85, y + 62), label, font=font(54, "Bold"), fill=(170, 180, 200), anchor="lm")
    d.text((670, y + 62), pct(100 * val), font=font(84, "Black"), fill=col, anchor="rm")
d.rounded_rectangle((760, 370, 1230, 645), 28, fill=(220, 38, 38))
d.text((995, 440), "real", font=font(52, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((995, 545), pct(100 * REAL_19_25), font=font(120, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((1230, 60), "2019 → 2025", font=font(44, "Bold"), fill=(170, 180, 200), anchor="ra")
d.text((1230, 115), "echte Daten", font=font(34, "SemiBold"), fill=(120, 132, 156), anchor="ra")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v002_inflation_gehalt/thumbnail.png")
