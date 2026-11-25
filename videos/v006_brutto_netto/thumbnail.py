"""1280x720 thumbnail."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, ".")
from lib.gfx import FG, BLUE, RED, GREEN, AMBER, font, eur
from videos.v006_brutto_netto.scenes import M, SV

img = Image.new("RGB", (1280, 720), (13, 19, 33))
d = ImageDraw.Draw(img)
d.text((50, 60), "Was bleibt", font=font(112, "Black"), fill=FG)
d.text((50, 190), "vom Brutto?", font=font(112, "Black"), fill=AMBER)
for y, label, val, col in ((370, "Sozialvers.", "−" + eur(SV), BLUE), (520, "Lohnsteuer", "−" + eur(M["LSt"]), RED)):
    d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
    d.text((85, y + 62), label, font=font(50, "Bold"), fill=(170, 180, 200), anchor="lm")
    d.text((670, y + 62), val, font=font(72, "Black"), fill=col, anchor="rm")
d.rounded_rectangle((760, 370, 1230, 645), 28, fill=(16, 150, 105))
d.text((995, 435), "3.000 € brutto", font=font(44, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((995, 535), eur(M["Netto"]), font=font(104, "Black"), fill=(255, 255, 255), anchor="mm")
d.text((995, 610), "netto", font=font(40, "Bold"), fill=(255, 255, 255), anchor="mm")
d.text((1230, 60), "2026", font=font(44, "Bold"), fill=(170, 180, 200), anchor="ra")
d.text((1230, 115), "offizieller Rechenweg", font=font(34, "SemiBold"), fill=(120, 132, 156), anchor="ra")
img.save(sys.argv[1] if len(sys.argv) > 1 else "output/v006_brutto_netto/thumbnail.png")
