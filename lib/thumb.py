"""Einheitliches 1280x720-Thumbnail: zwei Titelzeilen, zwei Kacheln links, Hervorhebung rechts."""
from PIL import Image, ImageDraw

from .gfx import AMBER, FG, font


def thumbnail(path, line1, line2, tiles, box, corner=("Ø Deutschland", "offizielle Zahlen"), title_size=104):
    """tiles: [(label, value, color)] × 2; box: (oben, groß, unten, fill_rgb)."""
    img = Image.new("RGB", (1280, 720), (13, 19, 33))
    d = ImageDraw.Draw(img)
    d.text((50, 60), line1, font=font(title_size, "Black"), fill=FG)
    d.text((50, 190), line2, font=font(title_size, "Black"), fill=AMBER)
    for y, (label, val, col) in zip((370, 520), tiles):
        d.rounded_rectangle((50, y, 700, y + 125), 24, fill=(26, 35, 56))
        d.text((85, y + 62), label, font=font(44, "Bold"), fill=(170, 180, 200), anchor="lm")
        d.text((670, y + 62), val, font=font(64, "Black"), fill=col, anchor="rm")
    top, big, bottom, fill = box
    d.rounded_rectangle((760, 370, 1230, 645), 28, fill=fill)
    d.text((995, 432), top, font=font(42, "Bold"), fill=(255, 255, 255), anchor="mm")
    d.text((995, 525), big, font=font(100 if len(big) <= 7 else 80, "Black"), fill=(255, 255, 255), anchor="mm")
    if bottom:
        d.text((995, 608), bottom, font=font(34, "Bold"), fill=(255, 255, 255), anchor="mm")
    if corner:
        d.text((1230, 60), corner[0], font=font(44, "Bold"), fill=(170, 180, 200), anchor="ra")
        d.text((1230, 115), corner[1], font=font(34, "SemiBold"), fill=(120, 132, 156), anchor="ra")
    img.save(path)
