"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, BLUE, RED, AMBER, font
from videos.v005_mieten_kaufen.scenes import BAUZ_NOW, BE, F, dec, pct

W, H = 1280, 720
img = Image.new("RGB", (W, H), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 60), "Mieten oder", font=font(112, "Black"), fill=FG)
d.text((50, 190), "kaufen?", font=font(112, "Black"), fill=AMBER)
for y, label, val, col in ((370, "Preis", f"{dec(F)} × Miete", BLUE), (520, "Bauzins", pct(BAUZ_NOW, 2), RED)):
    d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
    d.text((85, y + 62), label, font=font(50, "Bold"), fill=(170, 180, 200), anchor="lm")
    d.text((670, y + 62), val, font=font(64, "Black"), fill=col, anchor="rm")
d.rounded_rectangle((760, 370, 1230, 645), 28, fill=(202, 138, 4))
d.text((995, 435), "lohnt ab", font=font(50, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((995, 520), pct(100 * BE), font=font(110, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((995, 610), "Wertzuwachs p. a.", font=font(34, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((1230, 60), "Ø Deutschland", font=font(44, "Bold"), fill=(170, 180, 200), anchor="ra")
d.text((1230, 115), "Bundesbank-Daten", font=font(34, "SemiBold"), fill=(120, 132, 156), anchor="ra")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v005_mieten_kaufen/thumbnail.png")
