"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, GREEN, RED, AMBER, font
from videos.v004_kredite.scenes import D_NOW, E_NOW, K_NOW, pct

W, H = 1280, 720
img = Image.new("RGB", (W, H), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 60), "Was Kredite", font=font(112, "Black"), fill=FG)
d.text((50, 190), "wirklich kosten", font=font(112, "Black"), fill=AMBER)
for y, label, val, col in ((370, "Sparen", E_NOW, GREEN), (520, "Dispo", D_NOW, RED)):
    d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
    d.text((85, y + 62), label, font=font(54, "Bold"), fill=(170, 180, 200), anchor="lm")
    d.text((670, y + 62), pct(val), font=font(84, "Black"), fill=col, anchor="rm")
d.rounded_rectangle((760, 370, 1230, 645), 28, fill=(220, 38, 38))
d.text((995, 440), "Kreditkarte", font=font(50, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((995, 545), pct(K_NOW, 1), font=font(110, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((1230, 60), "Ø Deutschland", font=font(44, "Bold"), fill=(170, 180, 200), anchor="ra")
d.text((1230, 115), "Bundesbank-Daten", font=font(34, "SemiBold"), fill=(120, 132, 156), anchor="ra")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v004_kredite/thumbnail.png")
