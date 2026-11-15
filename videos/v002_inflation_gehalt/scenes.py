"""Video 002: Was Inflation wirklich mit deinem Gehalt macht – mit echten Destatis-Daten."""
import math
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     dot, ease_in_out, eur, fade, lerp, piecewise, prog, rrect, text, text_pop,
                     thick_line)

# ---------------------------------------------------------------- data (Destatis, Stand 15.11.2026)
DATA = Path(__file__).parent / "data"


def _read(name):
    rows = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        cells = line.split(";")
        if cells[0].isdigit() and len(cells[0]) == 4:
            vals = [0.0 if c == "-" else float(c.replace(",", ".")) for c in cells[1::2]]
            rows[int(cells[0])] = vals
    return rows


_vpi = _read("61111-0001_vpi.csv")          # [VPI 2020=100, Veränderung %]
_lohn = _read("62361-0020_lohnindex.csv")   # [Real 2025=100, %, Nominal 2025=100, %]

YEARS = list(range(2015, 2026))
assert sorted(_vpi) == YEARS and sorted(_lohn) == YEARS
CPI = {y: _vpi[y][0] for y in YEARS}
CPI_CH = {y: _vpi[y][1] for y in YEARS}
REAL = {y: _lohn[y][0] for y in YEARS}
REAL_CH = {y: _lohn[y][1] for y in YEARS}
NOM = {y: _lohn[y][2] for y in YEARS}
NOM_CH = {y: _lohn[y][3] for y in YEARS}

# ---------------------------------------------------------------- derived numbers
NOM_19_25 = NOM[2025] / NOM[2019] - 1          # Löhne seit 2019
CPI_19_25 = CPI[2025] / CPI[2019] - 1          # Preise seit 2019
REAL_19_25 = REAL[2025] / REAL[2019] - 1       # Reallohn seit 2019
COST_100 = 100 * CPI[2025] / CPI[2019]         # was 2019 100 € kostete
VALUE_100 = 100 * CPI[2019] / CPI[2025]        # 100 € von 2019 heute
CPI_20_23 = CPI[2023] / CPI[2020] - 1
W15 = {y: 100 * NOM[y] / NOM[2015] for y in YEARS}
P15 = {y: 100 * CPI[y] / CPI[2015] for y in YEARS}
REAL22 = (1 + NOM_CH[2022] / 100) / (1 + CPI_CH[2022] / 100) - 1
SALARY = 3000.0
EX_NEED = SALARY * CPI[2025] / CPI[2019]
EX_AVG = SALARY * NOM[2025] / NOM[2019]
HALF_2 = math.log(2) / math.log(1.02)
HALF_69 = math.log(2) / math.log(1 + CPI_CH[2022] / 100)

# Every number spoken in the narration is checked here.
assert 21.5 < 100 * NOM_19_25 < 22.5                        # "rund zweiundzwanzig Prozent"
assert 22.45 < 100 * CPI_19_25 < 22.55                      # "zweiundzwanzigeinhalb Prozent"
assert -0.55 < 100 * REAL_19_25 < -0.45                     # "ein halbes Prozent weniger"
assert CPI[2020] == 100.0 and CPI[2019] == 99.5 and CPI[2025] == 121.9
assert 122 < COST_100 < 123 and 81.5 < VALUE_100 < 82.5     # "gut 122 €", "rund 82 €"
assert all(CPI_CH[y] < 2 for y in range(2015, 2021))        # "jedes Jahr unter zwei Prozent"
assert (CPI_CH[2021], CPI_CH[2022], CPI_CH[2023]) == (3.1, 6.9, 5.9)
assert 16.5 < 100 * CPI_20_23 < 17.5                        # "rund siebzehn Prozent"
assert CPI_CH[2024] == CPI_CH[2025] == 2.2
assert W15[2019] - P15[2019] > 5                            # Löhne bis 2019 deutlich vorn
assert W15[2021] > P15[2021] and W15[2022] < P15[2022]      # 2022 Vorsprung aufgezehrt
assert W15[2023] < P15[2023] and W15[2024] > P15[2024]      # erst ab 2024 wieder vorn
assert round(W15[2025] - 100) == 35 and round(P15[2025] - 100) == 29
assert REAL_CH[2022] == -4.1 and NOM_CH[2022] == 2.5
assert -4.2 < 100 * REAL22 < -4.05                          # "gut vier Prozent minus"
assert NOM_CH[2023] == 6.0 and REAL_CH[2023] == 0.2
assert REAL_CH[2024] > 2.5 and REAL_CH[2025] > 1.5          # "spürbar nach oben"
assert REAL[2025] < REAL[2019]                              # "leicht unter 2019"
assert 3670 < EX_NEED < 3680                                # "rund 3.675 €"
assert 3655 < EX_AVG < 3665 and 655 < EX_AVG - SALARY < 665  # "rund 3.660", "rund 660 € mehr"
assert EX_AVG < EX_NEED
assert round(HALF_2) == 35 and round(70 / 2) == 35          # "fünfunddreißig Jahre"
assert 10 < HALF_69 < 10.5 and 10 < 70 / 6.9 < 10.5         # "gut zehn Jahre"

SRC = "Quelle: Statistisches Bundesamt (Destatis) · Tabellen 61111-0001 & 62361-0020"


def pct(v, dec=1, sign=True):
    s = f"{v:+.{dec}f}" if sign else f"{v:.{dec}f}"
    return s.replace("-", "−").replace(".", ",") + " %"


def dec(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def dashed_h(d, x0, x1, y, color, width=3, dash=14, gap=12):
    x = x0
    while x < x1:
        d.line((x, y, min(x + dash, x1), y), fill=color, width=width)
        x += dash + gap


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 200), "2019  →  2025", t, S.c(0), 64, MUTED, "mm", "Bold")
    cards = [((300, 300, 900, 680), "Löhne", 100 * NOM_19_25, GREEN, S.c(0) + 0.4),
             ((1020, 300, 1620, 680), "Preise", 100 * CPI_19_25, RED, S.c(2))]
    for box, label, val, col, start in cards:
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        card(d, box, a, col)
        cx = (box[0] + box[2]) / 2
        text(d, (cx, box[1] + 80), label, 40, MUTED, a, "mm", "SemiBold")
        p = prog(t, start + 0.2, 1.4, ease_in_out)
        text(d, (cx, box[1] + 210), pct(val * p), 110, col, a, "mm", "Black")
        text(d, (cx, box[1] + 320), "Durchschnitt Deutschland", 26, MUTED, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 740, 1560, 850), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6),
              width=2)
        text(d, (400, 795), "Kaufkraft eines Durchschnittslohns", 38, FG, a, "lm", "SemiBold")
        text(d, (1520, 795), pct(100 * REAL_19_25), 56, AMBER, a, "rm", "Black")
    footer(d, prog(t, S.c(4), 0.6), "Quelle: Statistisches Bundesamt (Destatis)")


def draw_vpi(img, d, t, S):
    title(d, t, "Wie misst man Inflation?", S.c(0), "Verbraucherpreisindex (VPI) des Statistischen Bundesamts")
    a1 = prog(t, S.c(1), 0.5)
    text(d, (250, 250), "Preise eines typischen Warenkorbs – jeden Monat erhoben", 32, FG, a1, "lm",
         "SemiBold")
    chips = ["Lebensmittel", "Miete", "Energie", "Kleidung", "Freizeit", "Verkehr", "…"]
    x = 250
    for i, s in enumerate(chips):
        a = prog(t, S.c(2) + i * 0.18, 0.4)
        w = 28 * len(s) * 0.62 + 50
        if a > 0:
            rrect(d, (x, 300, x + w, 356), 28, fill=fade((30, 42, 66), a), outline=fade((60, 76, 108), a),
                  width=2)
            text(d, (x + w / 2, 329), s, 28, FG, a, "mm", "Medium")
        x += w + 18
    text(d, (250, 395), "gewichtet nach den Ausgaben der Haushalte", 26, MUTED,
         prog(t, S.c(2) + 1.2, 0.5), "lm", "Medium")

    tiles = [(250, "2019", CPI[2019], GRAY, S.c(4)), (750, "2020", CPI[2020], BLUE, S.c(3)),
             (1250, "2025", CPI[2025], RED, lerp(S.c(4), S.e(4), 0.55))]
    for x0, yr, v, col, start in tiles:
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        dy = (1 - a) * 30
        card(d, (x0, 450 + dy, x0 + 420, 660 + dy), a, col)
        text(d, (x0 + 210, 505 + dy), yr, 34, MUTED, a, "mm", "SemiBold")
        text(d, (x0 + 210, 595 + dy), dec(v), 84, col, a, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        text(d, (250, 760), "Was 2019 100 € gekostet hat, kostet 2025", 38, FG, a5, "lm", "SemiBold")
        text(d, (1670, 760), "≈ " + eur(COST_100, 2), 48, RED, a5, "rm", "Black")
    a6 = prog(t, S.c(6), 0.5)
    if a6 > 0:
        text(d, (250, 850), "100 € von 2019 sind heute noch wert", 38, FG, a6, "lm", "SemiBold")
        text(d, (1670, 850), "≈ " + eur(VALUE_100, 2), 48, AMBER, a6, "rm", "Black")
    footer(d, prog(t, S.c(3), 0.6), "Quelle: Destatis, Tabelle 61111-0001 · Jahresdurchschnitte, 2020 = 100")


def draw_inflation(img, d, t, S):
    title(d, t, "Inflationsrate in Deutschland", 0.0, "Veränderung des Verbraucherpreisindex zum Vorjahr")
    ch = Chart((260, 260, 1380, 880), (2014.4, 2025.6), (0, 8))
    ch.axes(d, prog(t, 0, 0.8), YEARS, range(0, 9, 2), lambda y: f"’{y % 100:02}",
            lambda v: f"{v} %")
    footer(d, prog(t, 0, 1), "Quelle: Destatis, Tabelle 61111-0001")
    bw = (ch.x1 - ch.x0) / 11.2 * 0.62
    starts = {y: lerp(S.c(1), S.e(1) - 0.4, (y - 2015) / 5) for y in range(2015, 2021)}
    starts.update({2021: S.c(2) + 0.3, 2022: S.c(3) + 0.3, 2023: S.c(4) + 0.3,
                   2024: S.c(6) + 0.3, 2025: S.c(6) + 0.6})
    hot = prog(t, S.c(5), 0.5) * (1 - prog(t, S.c(6), 0.5))
    a2 = prog(t, S.c(1) + 0.5, 0.5)
    if a2 > 0:
        _, py = ch.px(0, 2)
        dashed_h(d, ch.x0, ch.x1, py, fade(FG, a2 * 0.5), 2)
        text(d, (ch.x0 + 10, py - 8), "2 %", 24, MUTED, a2, "lb", "SemiBold")
    for y in YEARS:
        p = prog(t, starts[y], 0.5)
        if p <= 0:
            continue
        v = CPI_CH[y]
        cx, base = ch.px(y, 0)
        _, top = ch.px(y, v * p)
        col = RED if v > 3 else (AMBER if v > 2 else BLUE)
        d.rectangle((cx - bw / 2, top, cx + bw / 2, base), fill=col)
        text(d, (cx, top - 12), dec(v * p), 26, FG, p, "mb", "Bold")
    if hot > 0:
        x0, _ = ch.px(2020.6, 0)
        x1, _ = ch.px(2023.4, 0)
        _, yb = ch.px(0, 7.6)
        d.line((x0, yb, x1, yb), fill=fade(AMBER, hot), width=4)
        d.line((x0, yb, x0, yb + 20), fill=fade(AMBER, hot), width=4)
        d.line((x1, yb, x1, yb + 20), fill=fade(AMBER, hot), width=4)
    a5 = prog(t, S.c(5), 0.5)
    text(d, (1440, 380), "2020 → 2023", 30, MUTED, a5, "lm", "SemiBold")
    text(d, (1440, 450), pct(100 * CPI_20_23), 72, AMBER, a5, "lm", "Black")
    text(d, (1440, 510), "Preise in nur 3 Jahren", 28, FG, a5, "lm", "Medium")
    a7 = prog(t, S.c(7), 0.5)
    if a7 > 0:
        card(d, (1430, 600, 1870, 800), a7, AMBER)
        text(d, (1460, 660), "Niedrigere Inflation", 30, FG, a7, "lm", "Bold")
        text(d, (1460, 705), "= Preise steigen", 30, FG, a7, "lm", "Medium")
        text(d, (1460, 750), "nur langsamer", 30, AMBER, a7, "lm", "Bold")


XS = np.linspace(2015, 2025, 401)
W15_I = np.interp(XS, YEARS, [W15[y] for y in YEARS])
P15_I = np.interp(XS, YEARS, [P15[y] for y in YEARS])


def draw_wages_prices(img, d, t, S):
    title(d, t, "Löhne vs. Preise", S.c(0), "Beide Reihen auf 2015 = 100 umgerechnet (Jahresdurchschnitte)")
    ch = Chart((260, 250, 1440, 880), (2015, 2025), (95, 140))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, YEARS, range(100, 141, 10), lambda y: f"’{y % 100:02}", str)
    footer(d, ax)
    # legend
    for x, name, col in ((260, "Löhne (Nominallohnindex)", GREEN),
                         (720, "Preise (Verbraucherpreisindex)", RED)):
        thick_line(d, [(x, 215), (x + 40, 215)], fade(col, ax), 6)
        text(d, (x + 52, 215), name, 24, FG, ax, "lm", "Medium")
    up = piecewise(t, [(S.c(1), 2015), (S.e(2), 2019), (S.c(3) + 0.2, 2019), (S.e(4), 2022),
                       (S.c(5), 2022), (S.e(5), 2025)]) if t > S.c(1) else 2015
    if up > 2015:
        # gap band, coloured by sign
        n = int(np.searchsorted(XS, up))
        for i in range(min(n, len(XS) - 1)):
            xa, xb = XS[i], XS[i + 1]
            pa, pb = ch.px(xa, W15_I[i]), ch.px(xb, W15_I[i + 1])
            qa, qb = ch.px(xa, P15_I[i]), ch.px(xb, P15_I[i + 1])
            col = fade(GREEN, 0.28) if W15_I[i] + W15_I[i + 1] >= P15_I[i] + P15_I[i + 1] else fade(RED, 0.35)
            d.polygon([pa, pb, qb, qa], fill=col)
        ch.line(d, XS, P15_I, RED, 6, up)
        ch.line(d, XS, W15_I, GREEN, 6, up)
    a2 = prog(t, S.c(2), 0.5) * (1 - prog(t, S.c(3), 0.5))
    if a2 > 0:
        p = ch.px(2017.6, 99.2)
        text(d, p, "Kaufkraft-Plus", 30, GREEN, a2, "mm", "Bold")
    a4 = prog(t, S.c(4) + 0.5, 0.5) * (1 - prog(t, S.c(6), 0.5))
    if a4 > 0:
        p = ch.px(2022, P15[2022])
        d.ellipse((p[0] - 26, p[1] - 26, p[0] + 26, p[1] + 26), outline=fade(AMBER, a4), width=4)
        text(d, (p[0], ch.px(0, 127)[1]), "2022: Vorsprung weg", 32, AMBER, a4, "mb", "Bold")
    a6 = prog(t, S.c(6), 0.5)
    for val, name, col in ((W15[2025], "Löhne", GREEN), (P15[2025], "Preise", RED)):
        _, py = ch.px(2025, val)
        text(d, (1470, py - 4), name, 26, col, a6, "ls", "SemiBold")
        text(d, (1470, py + 2), pct(val - 100), 40, FG, a6, "lt", "Black")


RX = np.array(YEARS, float)
RY = np.array([REAL[y] for y in YEARS])


def draw_real(img, d, t, S):
    title(d, t, "Reallohn = Lohn ÷ Preise", S.c(0), "Reallohnindex, 2025 = 100")
    ch = Chart((250, 250, 1170, 860), (2015, 2025), (94, 101.5))
    ax = prog(t, S.c(0), 0.6)
    ch.axes(d, ax, YEARS, range(94, 102, 2), lambda y: f"’{y % 100:02}", str)
    footer(d, ax, "Quelle: Destatis, Tabelle 62361-0020")
    up = 2015 + 10 * prog(t, S.c(0) + 0.5, S.e(0) - S.c(0), ease_in_out)
    a6 = prog(t, S.c(6), 0.5)
    if a6 > 0:
        _, py = ch.px(0, REAL[2019])
        dashed_h(d, ch.x0, ch.x1, py, fade(AMBER, a6 * 0.8), 3)
        text(d, (ch.x0 + 10, py - 10), f"Stand 2019: {dec(REAL[2019])}", 26, AMBER, a6, "lb", "Bold")
    if up > 2015:
        ch.line(d, RX, RY, VIOLET, 7, up)
        for y in YEARS:
            if y <= up:
                dot(d, ch.px(y, REAL[y]), 7, VIOLET)
    a1 = prog(t, S.c(1), 0.5)
    if a1 > 0:
        pa, pb = ch.px(2021, REAL[2021]), ch.px(2022, REAL[2022])
        thick_line(d, [pa, pb], fade(RED, a1), 9)
        dot(d, pb, 11, fade(RED, a1))
        text(d, (pb[0], pb[1] + 24), pct(REAL_CH[2022]), 34, RED, a1, "mt", "Black")
    labels = [(2023, S.c(4) + 1.0, GRAY), (2024, S.c(5) + 0.3, GREEN), (2025, S.c(5) + 0.8, GREEN)]
    for y, start, col in labels:
        a = prog(t, start, 0.5)
        if a > 0:
            p = ch.px(y, REAL[y])
            dot(d, p, 10, fade(col, a))
            if y == 2023:
                text(d, (p[0] + 14, p[1] + 14), pct(REAL_CH[y]), 30, FG, a, "lt", "Bold")
            else:
                text(d, (p[0] - 20, p[1] + 4), pct(REAL_CH[y]), 30, col, a, "rm", "Bold")

    # right panel: 2022 numbers + formula, then 2023
    swap = prog(t, S.c(4), 0.5)
    a2 = prog(t, S.c(2), 0.5) * (1 - swap)
    a3 = prog(t, S.c(3), 0.5) * (1 - swap)
    a4 = prog(t, S.c(4) + 0.3, 0.5)

    def year_card(alpha, yr, nom, cpi, real=None):
        if alpha <= 0:
            return
        card(d, (1250, 250, 1860, 580 if real is not None else 500), alpha)
        text(d, (1290, 300), yr, 34, MUTED, alpha, "lm", "Bold")
        text(d, (1290, 375), "Löhne", 34, FG, alpha, "lm", "SemiBold")
        text(d, (1820, 375), pct(nom), 48, GREEN, alpha, "rm", "Black")
        text(d, (1290, 450), "Preise", 34, FG, alpha, "lm", "SemiBold")
        text(d, (1820, 450), pct(cpi), 48, RED, alpha, "rm", "Black")
        if real is not None:
            d.line((1290, 495, 1820, 495), fill=fade((70, 82, 108), alpha), width=2)
            text(d, (1290, 528), "real", 34, FG, alpha, "lm", "SemiBold")
            text(d, (1820, 528), pct(real), 44, VIOLET, alpha, "rm", "Black")

    year_card(a2, "2022", NOM_CH[2022], CPI_CH[2022])
    year_card(a4, "2023", NOM_CH[2023], CPI_CH[2023], REAL_CH[2023])
    if a3 > 0:
        card(d, (1250, 540, 1860, 800), a3, VIOLET)
        text(d, (1290, 595), "1,025 ÷ 1,069 = " + dec(1 + REAL22, 3), 40, FG, a3, "lm", "Bold")
        text(d, (1290, 665), "→ " + pct(100 * REAL22) + " real", 44, VIOLET, a3, "lm", "Black")
        text(d, (1290, 740), "Reallohn = (1 + Lohn) ÷ (1 + Inflation) − 1", 24, MUTED, a3, "lm",
             "Medium")


def draw_example(img, d, t, S):
    title(d, t, "Beispiel: 3.000 € brutto im Jahr 2019", S.c(0), "Gleiche Kaufkraft – welches Gehalt 2025?")
    base, scale = 860, 0.14
    bars = [(260, ["2019"], SALARY, GRAY, S.c(1), None),
            (600, ["2025: nötig für", "gleiche Kaufkraft"], EX_NEED, RED, S.c(2) + 0.3,
             f"3.000 € × {dec(CPI[2025])} ÷ {dec(CPI[2019])}"),
            (940, ["2025: mit Ø-Lohnplus", f"({pct(100 * NOM_19_25)})"], EX_AVG, GREEN, S.c(3) + 0.3,
             f"3.000 € × {dec(NOM[2025])} ÷ {dec(NOM[2019])}")]
    for x, lines, val, col, start, formula in bars:
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        top = base - val * scale * prog(t, start, 0.9, ease_in_out)
        rrect(d, (x, top, x + 260, base), 14, fill=fade(col, a))
        text(d, (x + 130, top - 18), eur(val), 46, FG, a, "mb", "Black")
        for i, s in enumerate(lines):
            text(d, (x + 130, base + 24 + i * 34), s, 26, FG if i == 0 else MUTED, a, "mt", "SemiBold")
        if formula:
            text(d, (x + 130, base + 24 + len(lines) * 34 + 6), formula, 20, MUTED, a, "mt", "Medium")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        card(d, (1300, 300, 1860, 640), a4)
        text(d, (1340, 350), "auf dem Lohnzettel", 28, MUTED, a4, "lm", "Medium")
        text(d, (1340, 420), "+" + eur(EX_AVG - SALARY), 64, GREEN, a4, "lm", "Black")
        text(d, (1340, 510), "Kaufkraft vs. 2019", 28, MUTED, a4, "lm", "Medium")
        text(d, (1340, 580), "−" + eur(EX_NEED - EX_AVG) + " / Monat", 56, RED, a4, "lm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        rrect(d, (1300, 690, 1860, 860), 18, fill=fade((44, 38, 20), a5), outline=fade(AMBER, a5 * 0.6),
              width=2)
        text(d, (1330, 740), f"Erhöhung unter {pct(100 * CPI_19_25, sign=False)}", 30, AMBER, a5, "lm",
             "Bold")
        text(d, (1330, 790), "= weniger Kaufkraft", 30, FG, a5, "lm", "SemiBold")
        text(d, (1330, 830), "als 2019", 30, FG, a5, "lm", "SemiBold")
    footer(d, prog(t, S.c(2), 0.5), "Beispielrechnung, brutto · Daten: Destatis 61111-0001 & 62361-0020")


AX = np.linspace(0, 40, 401)
K2 = 100 / 1.02 ** AX
K69 = 100 / (1 + CPI_CH[2022] / 100) ** AX


def draw_rule70(img, d, t, S):
    title(d, t, "Die 70er-Regel", S.c(0))
    text_pop(d, (250, 185), "70 ÷ Inflationsrate ≈ Jahre, bis sich die Kaufkraft halbiert", t, S.c(1),
             34, AMBER, "ls", "Bold", rise=10)
    ch = Chart((260, 280, 1300, 880), (0, 40), (0, 100))
    ax = prog(t, S.c(1), 0.6)
    ch.axes(d, ax, range(0, 41, 10), range(0, 101, 25), str, lambda v: f"{v} €", "Jahre")
    text(d, (ch.x0, 250), "Kaufkraft von 100 €", 24, MUTED, ax, "lm", "Medium")
    footer(d, ax, "Modellrechnung: konstante Inflation, Geld ohne Zinsen")
    if ax > 0:
        _, py = ch.px(0, 50)
        dashed_h(d, ch.x0, ch.x1, py, fade(FG, ax * 0.5), 2)
    for cue, ys, half, col in ((2, K2, HALF_2, BLUE), (3, K69, HALF_69, RED)):
        up = 40 * prog(t, S.c(cue), S.e(cue) - S.c(cue), ease_in_out)
        if up > 0:
            ch.line(d, AX, ys, col, 6, up)
            if up >= half:
                dot(d, ch.px(half, 50), 10, col)
    for cue, y0, rate, years, exact, col in ((2, 330, "2 %", "35 Jahre", HALF_2, BLUE),
                                             (3, 560, f"{dec(CPI_CH[2022])} %", "≈ 10 Jahre", HALF_69, RED)):
        a = prog(t, S.c(cue) + 0.3, 0.5)
        if a <= 0:
            continue
        card(d, (1380, y0, 1860, y0 + 190), a, col)
        text(d, (1410, y0 + 55), f"Inflation {rate}", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1410, y0 + 115), years, 56, col, a, "lm", "Black")
        text(d, (1410, y0 + 165), f"genau: {dec(exact)} Jahre", 22, MUTED, a, "lm", "Medium")
    text(d, (1380, 820), "Gilt für jeden Euro,", 30, FG, prog(t, S.c(4), 0.5), "lm", "SemiBold")
    text(d, (1380, 862), "der ohne Zinsen liegt.", 30, FG, prog(t, S.c(4), 0.5), "lm", "SemiBold")


def draw_limits(img, d, t, S):
    title(d, t, "3 ehrliche Einschränkungen", S.c(0))
    out = prog(t, S.c(5), 0.5)
    items = [(S.c(1), "1", "Durchschnitt", ["Deine persönliche Inflation hängt von deinem Warenkorb ab."],
              (S.c(2), "2022 stiegen z. B. Energie & Lebensmittel besonders stark.")),
             (S.c(3), "2", "Brutto, nicht netto", ["Steuern & Sozialabgaben sind nicht eingerechnet."], None),
             (S.c(4), "3", "Alle Beschäftigten", ["Je nach Branche & Job sieht es anders aus."], None)]
    for i, (start, n, head, lines, extra) in enumerate(items):
        a = prog(t, start, 0.5) * (1 - out)
        if a <= 0:
            continue
        y = 240 + i * 200
        card(d, (250, y, 1670, y + 175), a)
        dot(d, (320, y + 87), 38, fade(AMBER, a))
        text(d, (320, y + 89), n, 40, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + 50), head, 38, FG, a, "lm", "Bold")
        text(d, (400, y + 100), lines[0], 30, MUTED, a, "lm", "Medium")
        if extra:
            text(d, (400, y + 142), extra[1], 30, AMBER, a * prog(t, extra[0], 0.5), "lm", "Medium")
    text_pop(d, (W / 2, 480), "Eine Gehaltserhöhung ist erst dann eine,", t, S.c(5) + 0.2, 64, FG, "mm",
             "Black")
    text_pop(d, (W / 2, 580), "wenn sie über der Inflation liegt.", t, S.c(5) + 0.5, 64, GREEN, "mm",
             "Black")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(0), 52, FG,
             "mm", "Bold")
    text_pop(d, (W / 2, 335), "Daten, Quellen & Formeln stehen in der Beschreibung.", t, S.c(1), 32, MUTED,
             "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (360, 470, 900, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (630, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (630, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (630, 665), "echte Zahlen statt Versprechen", 26, MUTED, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1020, 450, 1600, 780), a, AMBER)
        text(d, (1060, 510), "NÄCHSTES VIDEO", 24, AMBER, a, "lm", "Bold")
        text(d, (1060, 580), "Lohnt sich Tagesgeld", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "nach Inflation noch?", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "durchgerechnet", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Seit zweitausendneunzehn sind die Löhne in Deutschland im Schnitt um rund zweiundzwanzig Prozent gestiegen.",
            "Klingt gut.",
            "Aber die Preise sind im selben Zeitraum um zweiundzwanzigeinhalb Prozent gestiegen.",
            "Unterm Strich kann sich ein durchschnittlicher Lohn heute ein halbes Prozent weniger leisten als zweitausendneunzehn.",
            "Wir rechnen das mit den offiziellen Zahlen des Statistischen Bundesamts durch.",
        ], draw_hook),
        Scene("vpi", [
            "Zuerst: Wie misst man Inflation überhaupt?",
            "Das Statistische Bundesamt erfasst jeden Monat die Preise eines typischen Warenkorbs.",
            "Lebensmittel, Miete, Energie, Kleidung, Freizeit: alles gewichtet danach, wie viel Haushalte dafür ausgeben.",
            "Daraus entsteht der Verbraucherpreisindex. Im Jahr zweitausendzwanzig steht er auf hundert.",
            "Zweitausendneunzehn lag er bei neunundneunzig Komma fünf, zweitausendfünfundzwanzig bei hunderteinundzwanzig Komma neun.",
            "Was zweitausendneunzehn hundert Euro gekostet hat, kostet heute also gut hundertzweiundzwanzig Euro.",
            "Anders gesagt: Ein Hunderter von damals ist heute nur noch rund zweiundachtzig Euro wert.",
        ], draw_vpi),
        Scene("inflation", [
            "So sah die Inflation in den letzten elf Jahren aus.",
            "Von zweitausendfünfzehn bis zweitausendzwanzig lag sie jedes Jahr unter zwei Prozent. Kaum spürbar.",
            "Dann kam zweitausendeinundzwanzig: drei Komma eins Prozent.",
            "Zweitausendzweiundzwanzig: sechs Komma neun Prozent.",
            "Zweitausenddreiundzwanzig: noch einmal fünf Komma neun.",
            "In nur drei Jahren sind die Preise damit um rund siebzehn Prozent gestiegen.",
            "Seitdem liegt die Inflation wieder bei zwei Komma zwei Prozent.",
            "Aber Achtung: Die Preise sinken dadurch nicht. Sie steigen nur langsamer.",
        ], draw_inflation),
        Scene("loehne_preise", [
            "Jetzt legen wir Löhne und Preise übereinander. Beide starten zweitausendfünfzehn bei hundert.",
            "Bis zweitausendneunzehn wachsen die Löhne deutlich schneller als die Preise.",
            "Der Abstand dazwischen ist echter Kaufkraft-Gewinn.",
            "Dann holen die Preise auf.",
            "Zweitausendzweiundzwanzig ist der Vorsprung komplett aufgezehrt.",
            "Erst ab zweitausendvierundzwanzig ziehen die Löhne wieder davon.",
            "Über die ganzen zehn Jahre: Löhne plus fünfunddreißig Prozent, Preise plus neunundzwanzig Prozent.",
        ], draw_wages_prices),
        Scene("reallohn", [
            "Das Verhältnis aus beidem heißt Reallohn. Er zeigt, was du dir von deinem Lohn tatsächlich leisten kannst.",
            "Zweitausendzweiundzwanzig ist er um vier Komma eins Prozent gefallen.",
            "Die Löhne stiegen um zwei Komma fünf Prozent, die Preise aber um sechs Komma neun.",
            "Die Rechnung: eins Komma null zwei fünf, geteilt durch eins Komma null sechs neun. Das ergibt ein Minus von gut vier Prozent.",
            "Zweitausenddreiundzwanzig stiegen die Löhne sogar um sechs Prozent. Real blieb davon fast nichts übrig: plus null Komma zwei Prozent.",
            "Erst zweitausendvierundzwanzig und zweitausendfünfundzwanzig ging es spürbar nach oben.",
            "Und trotzdem liegt der Reallohn heute noch leicht unter dem Stand von zweitausendneunzehn.",
        ], draw_real),
        Scene("beispiel", [
            "Was heißt das für ein konkretes Gehalt?",
            "Nehmen wir dreitausend Euro brutto im Monat, im Jahr zweitausendneunzehn.",
            "Um sich zweitausendfünfundzwanzig genau dasselbe leisten zu können, bräuchtest du rund dreitausendsechshundertfünfundsiebzig Euro.",
            "Ist dein Gehalt so gestiegen wie der Durchschnitt, liegst du bei rund dreitausendsechshundertsechzig.",
            "Das sind rund sechshundertsechzig Euro mehr auf dem Lohnzettel. Und trotzdem real ein kleines Minus.",
            "Wer in dieser Zeit weniger Gehaltserhöhung bekommen hat, hat deutlich an Kaufkraft verloren.",
        ], draw_example),
        Scene("regel70", [
            "Noch eine Faustregel zum Merken: die Siebzig-Regel.",
            "Teile siebzig durch die Inflationsrate. Das Ergebnis ist ungefähr die Zahl der Jahre, bis sich die Kaufkraft deines Geldes halbiert.",
            "Bei zwei Prozent Inflation sind das fünfunddreißig Jahre.",
            "Bliebe die Inflation dauerhaft bei sechs Komma neun Prozent wie zweitausendzweiundzwanzig, wären es nur gut zehn Jahre.",
            "Das gilt für jeden Euro, der ohne Zinsen herumliegt.",
        ], draw_rule70),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Das sind Durchschnittswerte. Deine persönliche Inflation hängt davon ab, wofür du dein Geld ausgibst.",
            "Wer zum Beispiel viel für Energie und Lebensmittel ausgibt, hat zweitausendzweiundzwanzig mehr gespürt, denn die sind besonders stark gestiegen.",
            "Zweitens: Der Lohnindex misst Bruttoverdienste. Steuern und Sozialabgaben sind nicht eingerechnet.",
            "Drittens: Auch beim Lohn ist das der Durchschnitt aller Beschäftigten. Je nach Branche und Job sieht deine Entwicklung anders aus.",
            "Die Kernaussage bleibt: Eine Gehaltserhöhung ist erst dann eine, wenn sie über der Inflation liegt.",
        ], draw_limits),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Daten, Quellen und Formeln findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Im nächsten Video rechnen wir durch, ob sich Tagesgeld nach Inflation überhaupt noch lohnt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
