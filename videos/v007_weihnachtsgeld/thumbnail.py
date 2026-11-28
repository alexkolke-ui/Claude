"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, BLUE, GREEN, AMBER, font, eur
from videos.v007_weihnachtsgeld.scenes import B, M, Q, Z

img = Image.new("RGB", (1280, 720), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 60), "Weihnachtsgeld:", font=font(104, "Black"), fill=FG)
d.text((50, 190), "was bleibt netto?", font=font(104, "Black"), fill=AMBER)
for y, label, val, col in ((370, "Weihnachtsgeld", "54,7 %", GREEN), (520, "Monatsgehalt", "66,7 %", BLUE)):
    d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
    d.text((85, y + 62), label, font=font(40, "Bold"), fill=(170, 180, 200), anchor="lm")
    d.text((670, y + 62), val, font=font(64, "Black"), fill=col, anchor="rm")
d.rounded_rectangle((760, 370, 1230, 645), 28, fill=(185, 28, 28))
d.text((995, 435), eur(B) + " brutto", font=font(44, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((995, 535), eur(Z["Netto"]), font=font(104, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((995, 610), "netto", font=font(40, "Bold"), fill=(255, 255, 255), anchor="mm")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v007_weihnachtsgeld/thumbnail.png")
