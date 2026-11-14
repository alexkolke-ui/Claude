"""Video 001: 200 € im Monat, 30 Jahre – warum der Zeitpunkt wichtiger ist als der Betrag."""
import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     clamp, dot, ease_in_out, eur, fade, font, lerp, mix, num, piecewise, prog,
                     rrect, text, text_pop, thick_line, value_at)

# ---------------------------------------------------------------- model
RATE = 200.0
R_ETF, R_TG, INFL = 0.07, 0.02, 0.02


def fv(m, r, years):
    n = 12 * years
    if r == 0:
        return m * n
    i = r / 12
    return m * ((1 + i) ** n - 1) / i


X = np.linspace(0, 30, 361)
SP = np.array([fv(RATE, 0, x) for x in X])
TG = np.array([fv(RATE, R_TG, x) for x in X])
ETF = np.array([fv(RATE, R_ETF, x) for x in X])

F_SP, F_TG, F_ETF = fv(RATE, 0, 30), fv(RATE, R_TG, 30), fv(RATE, R_ETF, 30)
ETF10, ETF20 = fv(RATE, R_ETF, 10), fv(RATE, R_ETF, 20)
GROWTH = [fv(RATE, R_ETF, y) - fv(RATE, R_ETF, y - 1) for y in range(1, 31)]
ANNA, BEN = fv(RATE, R_ETF, 40), fv(RATE, R_ETF, 30)
BEN_NEEDS = RATE * ANNA / BEN
ANNA_REAL = ANNA / (1 + INFL) ** 40

# Numbers spoken in the narration must match the model (rounded).
assert round(F_SP) == 72000
assert 98000 < F_TG < 99000 and 26000 < F_TG - F_SP < 27000
assert 34000 < ETF10 < 35000 and 103500 < ETF20 < 104500 and 243500 < F_ETF < 244500
assert (F_ETF - F_SP) / F_ETF > 2 / 3
assert 18500 < GROWTH[-1] < 19000 and 7.5 < GROWTH[-1] / 2400 < 8
assert 520000 < ANNA < 530000 and 425 < BEN_NEEDS < 435 and 235000 < ANNA_REAL < 240000

AGES = np.linspace(25, 65, 481)
A_CURVE = np.array([fv(RATE, R_ETF, a - 25) for a in AGES])
B_CURVE = np.array([fv(RATE, R_ETF, max(0.0, a - 35)) for a in AGES])


def _sim_path():
    """Illustrative random path (NOT market data): yearly returns ~ N(7 %, 17 %)."""
    smooth = [0.0]
    for _ in range(40):
        smooth.append(smooth[-1] * 1.07 + 2400)
    for seed in range(1000):
        rng = np.random.default_rng(seed)
        r = rng.normal(0.07, 0.17, 40)
        v = [0.0]
        for k in range(40):
            v.append(v[-1] * (1 + r[k]) + 2400)
        if r.min() < -0.25 and r[25:].min() < -0.15 and abs(v[-1] / smooth[-1] - 1) < 0.08:
            return np.array(smooth), np.array(v)
    raise RuntimeError("no seed")


SMOOTH40, SIM40 = _sim_path()


def k(v):
    return "0" if v == 0 else f"{v / 1000:.0f}k €"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0):
    text(d, (1860, 1040), "Modellrechnung · keine Anlageberatung", 22, (90, 102, 128), alpha,
         "rs", "Medium")


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    up = prog(t, S.c(2), 0.8, ease_in_out)
    y0 = lerp(430, 230, up)
    text_pop(d, (W / 2, y0), "200 € im Monat", t, S.c(0), 120, FG, "mm", "Black", dur=0.6)
    text_pop(d, (W / 2, y0 + 120), "× 30 Jahre", t, S.c(1), 72, MUTED, "mm", "Bold")

    a = prog(t, S.c(2) + 0.2, 0.6)
    cards = [((300, 470, 900, 800), "Variante A", F_SP, GRAY, S.c(2) + 0.5),
             ((1020, 470, 1620, 800), "Variante B", F_ETF, GREEN,
              lerp(S.c(2), S.e(2), 0.55))]
    for box, label, val, col, start in cards:
        card(d, box, a, col)
        cx = (box[0] + box[2]) / 2
        text(d, (cx, box[1] + 80), label, 34, MUTED, a, "mm", "SemiBold")
        p = prog(t, start, 1.4, ease_in_out)
        if p > 0:
            text(d, (cx, box[1] + 190), eur(val * p), 84, col, a, "mm", "Black")
    p3 = prog(t, S.c(3), 0.5)
    text(d, (W / 2, 870), "gleicher Betrag  ·  gleiche Disziplin", 36, MUTED, p3, "mm", "Medium")
    text_pop(d, (W / 2, 950), "Der Unterschied: eine Entscheidung.", t, S.c(4), 46, AMBER,
             "mm", "Bold")


def draw_rules(img, d, t, S):
    title(d, t, "Die Spielregeln", S.c(0), "Drei Wege, 200 € pro Monat zu sparen")
    items = [("Sparschwein", "0 %", "keine Zinsen", GRAY, S.c(2)),
             ("Tagesgeld", "2 %", "Zinsen pro Jahr", BLUE, S.c(3)),
             ("Aktien-ETF", "7 %", "Rendite pro Jahr (Annahme)", GREEN, S.c(4))]
    for i, (name, rate, sub, col, start) in enumerate(items):
        x0 = 180 + i * 540
        a = prog(t, start, 0.6)
        dy = (1 - a) * 40
        box = (x0, 260 + dy, x0 + 480, 640 + dy)
        card(d, box, a, col)
        text(d, (x0 + 240, 340 + dy), name, 40, FG, a, "mm", "Bold")
        rate_a = a if i < 2 else a * (0.35 + 0.65 * prog(t, S.c(5), 0.5))
        text(d, (x0 + 240, 470 + dy), rate, 120, col, rate_a, "mm", "Black")
        text(d, (x0 + 240, 580 + dy), sub, 28, MUTED, a, "mm", "Medium")
    p = prog(t, S.c(6), 0.6)
    if p > 0:
        rrect(d, (180, 700, 1740, 800), 18, fill=fade((44, 38, 20), p), outline=fade(AMBER, p * 0.6),
              width=2)
        text(d, (220, 750), "7 % ≈ grob der langfristige Durchschnitt breiter Weltaktienindizes.",
             32, FG, p, "lm", "Medium")
        text(d, (1700, 750), "Annahme, keine Garantie", 32, AMBER, prog(t, S.c(7), 0.5), "rm", "Bold")
    p = prog(t, S.c(8), 0.6)
    text(d, (W / 2, 870), "Ohne Steuern & Kosten  ·  monatliche Einzahlung & Verzinsung",
         30, MUTED, p, "mm", "Medium")


def draw_growth(img, d, t, S):
    ch = Chart((260, 220, 1460, 900), (0, 30), (0, 260000))
    title(d, t, "200 € pro Monat, 30 Jahre lang", 0.0)
    ch.axes(d, prog(t, 0.0, 0.8), range(0, 31, 5), range(0, 260001, 50000), str, k, "Jahre")
    footer(d, prog(t, 0, 1))

    up1 = 30 * prog(t, S.c(1), S.e(3) - S.c(1), ease_in_out)
    up2 = 30 * prog(t, S.c(5), S.e(7) - S.c(5), ease_in_out)
    up3 = piecewise(t, [(S.c(10), 0), (S.c(11) + 0.4, 10), (S.c(12) + 0.4, 20),
                        (S.c(13) + 0.2, 23), (S.c(14) + 0.3, 30)]) if t > S.c(10) else 0

    # bands (behind lines)
    b1 = prog(t, S.c(8), 0.7)
    b2 = prog(t, S.c(15), 0.7)
    if b2 > 0:
        ch.band(d, X, ETF, SP, fade(GREEN, 0.25 * b2))
    if b1 > 0 and b2 < 1:
        ch.band(d, X, TG, SP, mix(fade(BLUE, 0.28 * b1), fade(GREEN, 0.25), b2))

    if up1 > 0:
        ch.line(d, X, SP, GRAY, 6, up1)
    if up2 > 0:
        ch.line(d, X, TG, BLUE, 6, up2)
    if up3 > 0:
        end = ch.line(d, X, ETF, GREEN, 8, up3)
        if up3 < 30:
            dot(d, end, 11, GREEN)
            text(d, (end[0] - 16, end[1] - 26), eur(value_at(X, ETF, up3)), 30, GREEN, 1, "rb",
                 "Bold")

    # milestones
    for cue, yr, val in ((11, 10, ETF10), (12, 20, ETF20)):
        a = prog(t, S.c(cue) + 0.4, 0.4) * (1 - prog(t, S.c(15), 0.5))
        if a > 0:
            p = ch.px(yr, val)
            dot(d, p, 8, fade(GREEN, a))
            text(d, (p[0], p[1] - 22), eur(val), 28, GREEN, a, "mb", "SemiBold")

    # end labels
    def label(y_val, name, col, a):
        if a <= 0:
            return
        _, py = ch.px(30, y_val)
        text(d, (1490, py - 4), name, 26, col, a, "ls", "SemiBold")
        text(d, (1490, py + 2), eur(y_val), 36, FG, a, "lt", "Bold")

    label(F_SP, "Sparschwein", GRAY, prog(t, S.c(2), 0.5))
    label(F_TG, "Tagesgeld 2 %", BLUE, prog(t, S.c(7) + 0.5, 0.5))
    label(F_ETF, "ETF 7 %", GREEN, prog(t, S.c(14) + 0.4, 0.5))

    if b1 > 0:
        p = ch.px(21, (value_at(X, TG, 21) + value_at(X, SP, 21)) / 2 + 4000)
        a = b1 * (1 - prog(t, S.c(9), 0.5))
        text(d, (p[0], p[1] - 70), f"+{eur(F_TG - F_SP)} Zinsen", 30, BLUE, a, "mm", "Bold")
    if b2 > 0:
        tx, ty = ch.px(2, 215000)
        target = ch.px(26, (value_at(X, ETF, 26) + value_at(X, SP, 26)) / 2)
        d.line((tx + 330, ty + 40, target[0], target[1]), fill=fade(GREEN, b2 * 0.7), width=3)
        dot(d, target, 7, fade(GREEN, b2))
        text(d, (tx, ty), f"{eur(F_ETF - F_SP)} Erträge", 38, GREEN, b2, "lm", "Black")
        text(d, (tx, ty + 46), f"= {100 * (F_ETF - F_SP) / F_ETF:.0f} % des Endbetrags",
             28, FG, b2, "lm", "Medium")


def draw_compound(img, d, t, S):
    ch = Chart((260, 240, 1500, 900), (0.3, 30.7), (0, 20000))
    title(d, t, "Zinseszins: Wachstum pro Jahr", 0.0, "Wie viel dein ETF-Depot in jedem Jahr dazugewinnt")
    ch.axes(d, prog(t, 0.0, 0.8), [1, 5, 10, 15, 20, 25, 30], range(0, 20001, 5000), str, k, "Jahr")
    footer(d)
    la = prog(t, 0.3, 0.6)
    rrect(d, (1540, 260, 1566, 286), 6, fill=fade(BLUE, la))
    text(d, (1580, 273), "selbst eingezahlt", 26, FG, la, "lm", "Medium")
    rrect(d, (1540, 310, 1566, 336), 6, fill=fade(GREEN, la))
    text(d, (1580, 323), "Erträge", 26, FG, la, "lm", "Medium")

    t0, t1 = S.c(1), S.e(2)
    bw = (ch.x1 - ch.x0) / 30.4 * 0.72
    hl = prog(t, S.c(3), 0.5)
    for y in range(1, 31):
        start = lerp(t0, t1 - 0.5, (y - 1) / 29)
        p = prog(t, start, 0.45)
        if p <= 0:
            continue
        g = GROWTH[y - 1]
        cx, base = ch.px(y, 0)
        _, ytop_c = ch.px(y, 2400 * p)
        _, ytop = ch.px(y, g * p)
        dim = 1 - 0.55 * hl if y < 30 else 1
        d.rectangle((cx - bw / 2, ytop_c, cx + bw / 2, base), fill=fade(BLUE, dim))
        d.rectangle((cx - bw / 2, ytop, cx + bw / 2, ytop_c), fill=fade(GREEN, dim))

    a1 = prog(t, t0 + 1.0, 0.5) * (1 - hl)
    p1 = ch.px(1, 2400)
    if a1 > 0:
        _, ly = ch.px(1, 7500)
        d.line((p1[0], ly + 8, p1[0], p1[1] - 8), fill=fade(FG, a1 * 0.6), width=2)
        text(d, (p1[0] - 10, ly), f"Jahr 1: nur {eur(GROWTH[0] - 2400)} Erträge", 28, FG, a1,
             "ls", "SemiBold")
    if hl > 0:
        px, py = ch.px(30, GROWTH[-1])
        d.rectangle((px - bw / 2 - 6, py - 6, px + bw / 2 + 6, ch.y1), outline=fade(AMBER, hl), width=4)
        text(d, (px + bw / 2 + 4, py - 20), f"+{eur(GROWTH[-1])}", 42, AMBER, hl, "rb", "Black")
        text(d, (px + bw / 2 + 4, py - 72), "Jahr 30", 28, MUTED, hl, "rb", "SemiBold")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        _, py = ch.px(0, 2400)
        x = ch.x0
        while x < ch.x1:
            d.line((x, py, min(x + 14, ch.x1), py), fill=fade(FG, a4 * 0.8), width=3)
            x += 26
        text(d, (ch.x0 + 20, py - 14), "2.400 € eingezahlt pro Jahr", 26, FG, a4, "lb", "SemiBold")
        text(d, (640, 420), f"≈ {GROWTH[-1] / 2400:.1f} ×".replace(".", ","), 96, AMBER, a4,
             "mm", "Black")
        text(d, (640, 490), "deine jährliche Einzahlung", 30, FG, a4, "mm", "Medium")


def draw_anna_ben(img, d, t, S):
    title(d, t, "Anna vs. Ben", S.c(0), "Beide sparen 200 € im Monat bis 65 – nur der Start ist anders")
    pa = prog(t, S.c(2), 0.5)
    pb = prog(t, lerp(S.c(2), S.e(2), 0.5), 0.5)
    for (x, name, sub, col, a) in ((1590, "Anna", "Start mit 25", VIOLET, pa),
                                   (1590, "Ben", "Start mit 35", AMBER, pb)):
        y = 250 if name == "Anna" else 340
        if a > 0:
            dot(d, (x + 30, y + 30), 30, fade(col, a))
            text(d, (x + 30, y + 31), name[0], 32, (13, 19, 33), a, "mm", "Black")
            text(d, (x + 76, y + 14), name, 32, FG, a, "lm", "Bold")
            text(d, (x + 76, y + 48), sub, 26, MUTED, a, "lm", "Medium")

    ch = Chart((260, 240, 1300, 900), (25, 65), (0, 560000))
    ax = prog(t, S.c(3), 0.6)
    ch.axes(d, ax, range(25, 66, 5), range(0, 500001, 100000), str, k, "Alter")
    if ax > 0:
        footer(d, ax)
    age = 25 + 40 * prog(t, S.c(3) + 0.3, S.c(5) - S.c(3), ease_in_out)
    if age > 25:
        ch.line(d, AGES, B_CURVE, AMBER, 7, age)
        e = ch.line(d, AGES, A_CURVE, VIOLET, 7, age)
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        card(d, (300, 270, 900, 420), a4)
        text(d, (330, 310), "Eingezahlt", 26, MUTED, a4, "lm", "Medium")
        text(d, (330, 355), f"Anna  {eur(96000)}", 32, VIOLET, a4, "lm", "Bold")
        text(d, (330, 395), f"Ben    {eur(72000)}", 32, AMBER, a4, "lm", "Bold")
        text(d, (880, 395), "Δ 24.000 €", 28, FG, a4, "rm", "SemiBold")
    for cue, val, col in ((5, ANNA, VIOLET), (6, BEN, AMBER)):
        a = prog(t, S.c(cue) + 0.3, 0.5)
        if a > 0:
            p = ch.px(65, val)
            dot(d, p, 11, fade(col, a))
            text(d, (p[0] + 26, p[1]), eur(val), 40, col, a, "lm", "Black")
    a7 = prog(t, S.c(7), 0.6)
    if a7 > 0:
        text(d, (1720, 780), f"{ANNA / BEN:.2f} ×".replace(".", ","), 84, FG, a7, "mm", "Black")
        text(d, (1720, 840), "mehr Endvermögen", 28, MUTED, a7, "mm", "Medium")


def draw_catchup(img, d, t, S):
    title(d, t, "Was müsste Ben sparen, um aufzuholen?", S.c(0), "Ziel: dieselben 525.000 € mit 65")
    base, scale = 900, 1.15
    bars = [(330, "Anna", "ab 25", VIOLET, RATE, S.c(0) + 0.5),
            (650, "Ben", "ab 35", AMBER, None, S.c(0) + 0.8)]
    for x, name, sub, col, val, start in bars:
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        if val is None:
            val = lerp(RATE, BEN_NEEDS, prog(t, S.c(1), 1.2, ease_in_out))
        top = base - val * scale * a
        rrect(d, (x, top, x + 220, base), 14, fill=fade(col, a))
        text(d, (x + 110, top - 20), f"{val:.0f} €", 48, FG, a, "mb", "Black")
        text(d, (x + 110, base + 30), name, 32, FG, a, "mt", "Bold")
        text(d, (x + 110, base + 72), f"{sub} · pro Monat", 24, MUTED, a, "mt", "Medium")
    a2 = prog(t, S.c(2), 0.5)
    text(d, (760, 300), f"{BEN_NEEDS / RATE:.2f} ×".replace(".", ","), 40, AMBER, a2, "mm", "Black")
    lines = [(3, "Jedes Jahr Warten kostet nicht nur", FG),
             (3, "ein Jahr Einzahlungen …", FG),
             (4, "… sondern das Wachstum,", GREEN),
             (4, "das ganz am Ende passiert wäre.", GREEN)]
    for i, (cue, s, col) in enumerate(lines):
        text_pop(d, (1040, 470 + i * 70 + (40 if i >= 2 else 0)), s, t, S.c(cue) + (i % 2) * 0.25,
                 44, col, "ls", "Bold")


def draw_reality(img, d, t, S):
    title(d, t, "3 ehrliche Punkte", S.c(0))
    tabs = [("1", "Inflation", S.c(1)), ("2", "Schwankungen", S.c(4)), ("3", "Steuern & Kosten", S.c(7))]
    if t < S.c(4):
        active = 0
    elif t < S.c(7):
        active = 1
    elif t < S.c(8):
        active = 2
    else:
        active = 3
    tab_a = 1 - prog(t, S.c(8), 0.5)
    for i, (n, name, start) in enumerate(tabs):
        a = prog(t, start, 0.4) * tab_a
        x = 250 + i * 470
        on = i == active
        rrect(d, (x, 190, x + 440, 250), 30, fill=fade((40, 52, 78) if on else (24, 32, 50), a))
        text(d, (x + 220, 221), f"{n}  {name}", 28, FG if on else MUTED, a, "mm", "Bold")

    if active == 0:
        a = prog(t, S.c(1), 0.5)
        bw = 1200
        y1, y2 = 420, 640
        text(d, (250, y1 - 30), "Annas Depot mit 65 (nominal)", 30, MUTED, a, "ls", "Medium")
        rrect(d, (250, y1, 250 + bw * a, y1 + 110), 14, fill=fade(VIOLET, a))
        text(d, (280, y1 + 55), eur(ANNA), 52, (13, 19, 33), a, "lm", "Black")
        p = prog(t, lerp(S.c(2), S.e(2), 0.55), 1.2, ease_in_out)
        a2 = prog(t, S.c(2), 0.5)
        text(d, (250, y2 - 30), "Kaufkraft in heutigem Geld (2 % Inflation p.a.)", 30, MUTED, a2,
             "ls", "Medium")
        w2 = bw * lerp(1, ANNA_REAL / ANNA, p)
        rrect(d, (250, y2, 250 + w2 * a2, y2 + 110), 14, fill=fade(mix(VIOLET, (90, 90, 120), p), a2))
        text(d, (280, y2 + 55), eur(lerp(ANNA, ANNA_REAL, p)), 52, (13, 19, 33), a2, "lm", "Black")
        text(d, (250, 860), "Immer noch viel – aber weniger, als es klingt.", 38, FG,
             prog(t, S.c(3), 0.5), "ls", "SemiBold")
    elif active == 1:
        ch = Chart((260, 320, 1500, 900), (0, 40), (0, 700000))
        a = prog(t, S.c(4), 0.5)
        ch.axes(d, a, range(0, 41, 10), range(0, 600001, 200000), str, k, "Jahre")
        xs = np.arange(41)
        up = 40 * prog(t, S.c(4) + 0.3, S.e(5) - S.c(4), ease_in_out)
        if up > 0:
            ch.line(d, xs, SMOOTH40, fade(GRAY, a), 5, up)
            ch.line(d, xs, SIM40, AMBER, 6, up)
        text(d, (1540, 400), "simulierter", 28, AMBER, a, "ls", "Bold")
        text(d, (1540, 436), "Beispielverlauf", 28, AMBER, a, "ls", "Bold")
        text(d, (1540, 476), "(keine echten Kursdaten)", 22, MUTED, a, "ls", "Medium")
        a6 = prog(t, S.c(6), 0.5)
        text(d, (1540, 560), "glatte Linie:", 28, GRAY, a6, "ls", "Bold")
        text(d, (1540, 596), "7 % jedes Jahr", 28, GRAY, a6, "ls", "Bold")
        text(d, (1540, 650), "= Durchschnitt,", 28, FG, a6, "ls", "SemiBold")
        text(d, (1540, 686), "kein Versprechen", 28, FG, a6, "ls", "SemiBold")
    elif active == 2:
        items = ["Abgeltungsteuer auf Erträge", "laufende Fondskosten (TER)",
                 "ggf. Depot- und Ordergebühren"]
        for i, s in enumerate(items):
            a = prog(t, S.c(7) + 0.3 + i * 0.35, 0.4)
            y = 420 + i * 130
            card(d, (250, y, 1300, y + 100), a)
            text(d, (300, y + 50), "–", 44, RED, a, "lm", "Black")
            text(d, (360, y + 50), s, 40, FG, a, "lm", "SemiBold")
        text(d, (250, 860), "→ die echte Rendite liegt unter der Bruttorendite.", 34, MUTED,
             prog(t, S.c(7) + 1.5, 0.5), "ls", "Medium")
    else:
        text_pop(d, (W / 2, 480), "Zeit ist der stärkste Hebel,", t, S.c(8) + 0.2, 80, FG, "mm", "Black")
        text_pop(d, (W / 2, 590), "den du hast.", t, S.c(8) + 0.5, 80, GREEN, "mm", "Black")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Anlageberatung – sondern Mathematik.", t, S.c(0), 56, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), "Annahmen & Formeln stehen in der Beschreibung.", t, S.c(1), 32, MUTED,
             "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (360, 470, 900, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (630, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (630, 620), "Nachgerechnet", 36, FG, a, "mm", "Bold")
        text(d, (630, 665), "echte Zahlen statt Versprechen", 26, MUTED, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1020, 450, 1600, 780), a, AMBER)
        text(d, (1060, 510), "NÄCHSTES VIDEO", 24, AMBER, a, "lm", "Bold")
        text(d, (1060, 580), "Was Inflation wirklich", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "mit deinem Gehalt macht", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "durchgerechnet mit echten Daten", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Zweihundert Euro im Monat.",
            "Dreißig Jahre lang.",
            "Am Ende hast du entweder zweiundsiebzigtausend Euro, oder rund zweihundertvierundvierzigtausend.",
            "Gleicher Betrag. Gleiche Disziplin.",
            "Der Unterschied ist eine einzige Entscheidung.",
            "Lass uns das durchrechnen.",
        ], draw_hook),
        Scene("regeln", [
            "Vorher kurz die Spielregeln.",
            "Wir vergleichen drei Wege.",
            "Das Sparschwein, ganz ohne Zinsen.",
            "Ein Tagesgeld mit zwei Prozent Zinsen pro Jahr.",
            "Und einen breit gestreuten Aktien-ETF.",
            "Für den ETF nehmen wir sieben Prozent pro Jahr an.",
            "Das liegt grob im Bereich dessen, was breite Weltaktienindizes langfristig im Schnitt gebracht haben.",
            "Aber das ist eine Annahme, keine Garantie.",
            "Steuern und Kosten lassen wir der Einfachheit halber weg.",
        ], draw_rules),
        Scene("wachstum", [
            "Fangen wir mit dem Sparschwein an.",
            "Zweihundert Euro, mal zwölf Monate, mal dreißig Jahre.",
            "Das sind zweiundsiebzigtausend Euro. Nicht mehr, nicht weniger.",
            "Die Linie wächst schnurgerade.",
            "Jetzt das Tagesgeld.",
            "Zwei Prozent klingen nach wenig.",
            "Aber die Zinsen werden selbst wieder verzinst.",
            "Nach dreißig Jahren stehen da rund achtundneunzigtausendfünfhundert Euro.",
            "Gut sechsundzwanzigtausend davon hast du nie selbst eingezahlt.",
            "Und jetzt der ETF.",
            "Am Anfang passiert kaum etwas.",
            "Nach zehn Jahren liegst du bei knapp fünfunddreißigtausend Euro.",
            "Nach zwanzig Jahren bei rund hundertviertausend.",
            "Und dann wird die Kurve steil.",
            "Nach dreißig Jahren: rund zweihundertvierundvierzigtausend Euro.",
            "Mehr als zwei Drittel davon sind Erträge, nicht deine Einzahlungen.",
        ], draw_growth),
        Scene("zinseszins", [
            "Warum die Kurve so aussieht, hat einen Namen: Zinseszins.",
            "Im ersten Jahr verdienst du Erträge nur auf das, was du gerade eingezahlt hast.",
            "Im dreißigsten Jahr verdienst du Erträge auf dreißig Jahre Einzahlungen, plus auf alle Erträge davor.",
            "Allein im letzten Jahr wächst dein Depot um knapp neunzehntausend Euro.",
            "Das ist fast achtmal so viel, wie du in diesem Jahr selbst einzahlst.",
        ], draw_compound),
        Scene("anna_ben", [
            "Jetzt der eigentlich spannende Teil.",
            "Stell dir zwei Personen vor.",
            "Anna fängt mit fünfundzwanzig an, Ben mit fünfunddreißig.",
            "Beide sparen zweihundert Euro im Monat, bis zur Rente mit fünfundsechzig.",
            "Anna zahlt also nur vierundzwanzigtausend Euro mehr ein als Ben.",
            "Am Ende hat Anna rund fünfhundertfünfundzwanzigtausend Euro.",
            "Ben: rund zweihundertvierundvierzigtausend.",
            "Zehn Jahre früher anfangen bedeutet hier: mehr als doppelt so viel.",
        ], draw_anna_ben),
        Scene("aufholen", [
            "Wie viel müsste Ben im Monat sparen, um Anna noch einzuholen?",
            "Rund vierhundertdreißig Euro.",
            "Mehr als das Doppelte.",
            "Jedes Jahr, das du wartest, kostet dich also nicht nur ein Jahr Einzahlungen.",
            "Es kostet dich das Wachstum, das ganz am Ende passiert wäre.",
        ], draw_catchup),
        Scene("realitaet", [
            "Bevor du jetzt euphorisch wirst: drei ehrliche Punkte.",
            "Erstens: Inflation.",
            "Bei zwei Prozent Inflation pro Jahr sind Annas fünfhundertfünfundzwanzigtausend Euro in vierzig Jahren nur so viel wert wie heute etwa zweihundertachtunddreißigtausend.",
            "Immer noch viel, aber weniger, als es klingt.",
            "Zweitens: Aktien schwanken.",
            "Es wird Jahre mit minus zwanzig oder minus dreißig Prozent geben.",
            "Die sieben Prozent sind ein Durchschnitt, kein Versprechen.",
            "Drittens: Steuern und Kosten fressen einen Teil der Rendite.",
            "Die Grundaussage bleibt trotzdem: Zeit ist der stärkste Hebel, den du hast.",
        ], draw_reality),
        Scene("outro", [
            "Das hier ist keine Anlageberatung, sondern Mathematik.",
            "Was du daraus machst, entscheidest du.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Im nächsten Video rechnen wir durch, was Inflation wirklich mit deinem Gehalt macht.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
