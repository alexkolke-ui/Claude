"""Channel artwork: profile picture, banner, video watermark. Run from repo root."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path("output/brand")
OUT.mkdir(parents=True, exist_ok=True)
BG = (13, 19, 33)
FG = (236, 240, 247)
MUTED = (139, 150, 170)
GREEN = (52, 211, 153)
BLUE = (96, 165, 250)
GRAY = (120, 130, 150)
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"


def font(size, w="Black"):
    return ImageFont.truetype(F.format(w), size)


def curve(x0, y0, x1, y1, k=3.2, n=200):
    """Exponential curve from (x0,y0) to (x1,y1)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        f = (math.exp(k * t) - 1) / (math.exp(k) - 1)
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * f))
    return pts


def line(d, pts, col, w):
    """Stroke by stamping discs along a densely resampled path (clean joins at any width)."""
    r = w / 2
    step = max(1.0, w / 6)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n + 1):
            x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)


def logo(size, transparent=False, s=4):
    """Monogram: N + rising compound-interest curve. Rendered 4x and downsampled (anti-aliasing)."""
    S = size * s
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0) if transparent else BG + (255,))
    d = ImageDraw.Draw(img)
    if transparent:
        d.ellipse((0, 0, S, S), fill=BG + (230,))
    else:  # subtle glow behind the curve
        glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse((S * .35, S * .1, S * .95, S * .7), fill=GREEN + (40,))
        img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(S * .12)))
        d = ImageDraw.Draw(img)
    # baseline grid
    for i in range(1, 4):
        y = S * (0.25 + 0.17 * i)
        d.line((S * .2, y, S * .8, y), fill=(36, 46, 66, 255), width=max(2, S // 160))
    d.text((S * .5, S * .52), "N", font=font(int(S * .62)), fill=FG, anchor="mm")
    pts = curve(S * .17, S * .76, S * .80, S * .2, k=3.4)
    line(d, pts, BG + (255,), int(S * .085))  # cut-out outline
    line(d, pts, GREEN, int(S * .045))
    x, y = pts[-1]
    r = S * .055
    d.ellipse((x - r, y - r, x + r, y + r), fill=GREEN, outline=BG, width=int(S * .018))
    return img.resize((size, size), Image.LANCZOS)


def banner():
    W, H, s = 2560, 1440, 2
    img = Image.new("RGB", (W * s, H * s), BG)
    d = ImageDraw.Draw(img)
    # faint grid across the full (TV) area
    for x in range(0, W * s, 80 * s):
        d.line((x, 0, x, H * s), fill=(19, 27, 45), width=s)
    for y in range(0, H * s, 80 * s):
        d.line((0, y, W * s, y), fill=(19, 27, 45), width=s)
    # three growth lines (sparschwein / tagesgeld / ETF) spanning the width
    # lines live inside the desktop band (y 508..931) so they are visible on every device
    base = 905 * s
    line(d, [(0, base), (W * s, base - 110 * s)], GRAY, 5 * s)
    line(d, curve(0, base, W * s, base - 190 * s, k=1.2), BLUE, 5 * s)
    line(d, curve(0, base, W * s, 470 * s, k=3.0, n=400), GREEN, 8 * s)
    # dark panel behind text in the safe area (1546x423 centred)
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    panel = Image.new("L", (W * s, H * s), 0)
    ImageDraw.Draw(panel).rounded_rectangle(
        ((sx0 + 60) * s, (sy0 + 40) * s, (sx0 + 1546 - 60) * s, (sy0 + 400) * s), 40 * s, fill=225)
    panel = panel.filter(ImageFilter.GaussianBlur(45 * s))
    img = Image.composite(Image.new("RGB", img.size, BG), img, panel)
    d = ImageDraw.Draw(img)
    cx = W * s // 2
    d.text((cx, (sy0 + 150) * s), "Nachgerechnet", font=font(150 * s), fill=FG, anchor="mm")
    d.text((cx, (sy0 + 268) * s), "Geld & Wirtschaft – mit echten Zahlen statt Versprechen",
           font=font(48 * s, "SemiBold"), fill=MUTED, anchor="mm")
    tags = ["Sparen", "ETF", "Inflation", "Steuern", "Wirtschaft"]
    f = font(34 * s, "Bold")
    widths = [d.textlength(t, font=f) + 56 * s for t in tags]
    x = cx - (sum(widths) + 20 * s * (len(tags) - 1)) / 2
    y = (sy0 + 360) * s
    for t, w in zip(tags, widths):
        d.rounded_rectangle((x, y - 30 * s, x + w, y + 30 * s), 30 * s, fill=(26, 35, 56),
                            outline=(48, 60, 86), width=2 * s)
        d.text((x + w / 2, y), t, font=f, fill=GREEN, anchor="mm")
        x += w + 20 * s
    return img.resize((W, H), Image.LANCZOS)


logo(800).convert("RGB").save(OUT / "profilbild_800.png")
logo(150, transparent=True).save(OUT / "wasserzeichen_150.png")
b = banner()
b.save(OUT / "banner_2560x1440.jpg", quality=92)
# preview with YouTube crop zones
pv = b.copy()
d = ImageDraw.Draw(pv)
for (w, h, col) in ((2560, 423, (255, 200, 0)), (1546, 423, (255, 60, 60)), (1855, 423, (0, 200, 255))):
    d.rectangle(((2560 - w) // 2, (1440 - h) // 2, (2560 + w) // 2, (1440 + h) // 2), outline=col, width=4)
pv.resize((1280, 720)).save(OUT / "banner_vorschau_zonen.png")
# profile preview as circle
p = logo(800).convert("RGB")
m = Image.new("L", p.size, 0)
ImageDraw.Draw(m).ellipse((0, 0, 800, 800), fill=255)
c = Image.new("RGB", (800, 800), (255, 255, 255))
c.paste(p, (0, 0), m)
c.save(OUT / "profilbild_vorschau_rund.png")
print("ok")
