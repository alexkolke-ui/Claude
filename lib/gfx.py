"""Small PIL toolkit for code-generated explainer animations (1920x1080)."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30

BG = (13, 19, 33)
FG = (236, 240, 247)
MUTED = (139, 150, 170)
GRID = (36, 46, 66)
GRAY = (156, 163, 175)
BLUE = (96, 165, 250)
GREEN = (52, 211, 153)
AMBER = (251, 191, 36)
RED = (248, 113, 113)
VIOLET = (167, 139, 250)

FONT_DIR = "/usr/share/fonts/opentype/inter/"
_fonts = {}


def font(size, weight="SemiBold"):
    key = (size, weight)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", size)
    return _fonts[key]


# ---------- timing helpers ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def prog(t, start, dur=0.6, ease=ease_out):
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return ease((t - start) / dur)


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(round(lerp(a, b, clamp(t)))) for a, b in zip(c1, c2))


def fade(color, alpha):
    """Simulate opacity on the flat background colour."""
    return mix(BG, color, alpha)


def eur(v, decimals=0):
    s = f"{v:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s + " €"


def num(v):
    return f"{v:,.0f}".replace(",", ".")


# ---------- background ----------
def make_background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H / 2) / H) ** 2)
    v = np.clip(1.0 - d * 0.55, 0.7, 1.0)[..., None]
    base = np.array(BG, np.float32)[None, None, :] * (0.75 + 0.25 * v) + 6 * (v - 0.7)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(img)
    d.text((60, 44), "R E C H N E T  S I C H  D A S ?", font=font(22, "Bold"), fill=(70, 84, 110))
    return img


# ---------- drawing primitives ----------
def text(d, xy, s, size=48, color=FG, alpha=1.0, anchor="la", weight="SemiBold"):
    if alpha <= 0.01:
        return
    d.text(xy, s, font=font(size, weight), fill=fade(color, alpha), anchor=anchor)


def text_pop(d, xy, s, t, start, size=48, color=FG, anchor="mm", weight="Bold", rise=30, dur=0.5):
    p = prog(t, start, dur)
    if p <= 0:
        return
    x, y = xy
    text(d, (x, y + (1 - p) * rise), s, size, color, p, anchor, weight)


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def card(d, box, alpha, accent=None, radius=22):
    if alpha <= 0.01:
        return
    rrect(d, box, radius, fill=fade((26, 35, 56), alpha), outline=fade((48, 60, 86), alpha), width=2)
    if accent:
        x0, y0, x1, _ = box
        d.rounded_rectangle((x0, y0, x1, y0 + 8), radius=4, fill=fade(accent, alpha))


def thick_line(d, pts, color, width):
    if len(pts) < 2:
        return
    d.line(pts, fill=color, width=width, joint="curve")
    r = width / 2
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=color)


def dot(d, xy, r, color):
    x, y = xy
    d.ellipse((x - r, y - r, x + r, y + r), fill=color)


class Chart:
    def __init__(self, box, xr, yr):
        self.x0, self.y0, self.x1, self.y1 = box
        self.xmin, self.xmax = xr
        self.ymin, self.ymax = yr

    def px(self, x, y):
        fx = (x - self.xmin) / (self.xmax - self.xmin)
        fy = (y - self.ymin) / (self.ymax - self.ymin)
        return (self.x0 + fx * (self.x1 - self.x0), self.y1 - fy * (self.y1 - self.y0))

    def axes(self, d, alpha, xticks, yticks, xfmt=str, yfmt=str, xlabel=None):
        if alpha <= 0.01:
            return
        for yv in yticks:
            _, py = self.px(self.xmin, yv)
            d.line((self.x0, py, self.x1, py), fill=fade(GRID, alpha), width=2)
            text(d, (self.x0 - 18, py), yfmt(yv), 26, MUTED, alpha, "rm", "Medium")
        for xv in xticks:
            px, _ = self.px(xv, self.ymin)
            text(d, (px, self.y1 + 22), xfmt(xv), 26, MUTED, alpha, "mt", "Medium")
        d.line((self.x0, self.y1, self.x1, self.y1), fill=fade((70, 82, 108), alpha), width=3)
        if xlabel:
            text(d, (self.x1, self.y1 + 62), xlabel, 24, MUTED, alpha, "rt", "Medium")

    def points(self, xs, ys, upto):
        """Polyline points up to x=upto (with interpolated end point)."""
        pts = []
        for i, (x, y) in enumerate(zip(xs, ys)):
            if x <= upto:
                pts.append(self.px(x, y))
            else:
                if i > 0:
                    xa, ya = xs[i - 1], ys[i - 1]
                    f = (upto - xa) / (x - xa)
                    pts.append(self.px(upto, lerp(ya, y, f)))
                break
        return pts

    def line(self, d, xs, ys, color, width=7, upto=None):
        upto = self.xmax if upto is None else upto
        pts = self.points(xs, ys, upto)
        thick_line(d, pts, color, width)
        return pts[-1] if pts else None

    def band(self, d, xs, top, bot, color, upto=None):
        upto = self.xmax if upto is None else upto
        a = self.points(xs, top, upto)
        b = self.points(xs, bot, upto)
        if len(a) >= 2:
            d.polygon(a + b[::-1], fill=color)


def value_at(xs, ys, x):
    return float(np.interp(x, xs, ys))


def piecewise(t, keys):
    """keys: list of (time, value); linear interpolation with ease between keys."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 1
            return lerp(v0, v1, ease_in_out(f))
    return keys[-1][1]
