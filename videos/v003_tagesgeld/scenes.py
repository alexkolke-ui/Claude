"""Video 003: Lohnt sich Tagesgeld nach Inflation noch? – mit Daten der Bundesbank und von Destatis."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     dot, ease_in_out, eur, fade, lerp, piecewise, prog, rrect, text, text_pop,
                     thick_line)

# ---------------------------------------------------------------- data (Stand 15.11.2026)
DATA = Path(__file__).parent / "data"


def _bbk(name):
    """Bundesbank-Zeitreihen-CSV (format=csv, lang=de) -> {'YYYY-MM': float}."""
    out = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and len(c[0]) == 7 and c[0][4] == "-" and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


def _destatis(name):
    rows = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        cells = line.split(";")
        if cells[0].isdigit() and len(cells[0]) == 4:
            rows[int(cells[0])] = [float(x.replace(",", ".")) for x in cells[1::2]]
    return rows


ZINS = _bbk("SUD101_zins_taeglich_faellig.csv")       # Effektivzins, täglich fällig, private Haushalte
REALZ = _bbk("SUR101_realzins_taeglich_faellig.csv")  # Realzins der Bundesbank (Fisher)
EZB = _bbk("SU0200_ezb_einlagefazilitaet.csv")        # EZB-Einlagesatz, Monatsende
INFL = _bbk("BBDP1_vpi_vorjahr.csv")                  # VPI, % gegen Vorjahresmonat
VPI = _bbk("BBDP1_vpi_index.csv")                     # VPI, 2020 = 100
VOL = _bbk("SUD201_volumen_taeglich_faellig.csv")     # Volumen, Mio. €
CPI_Y = {y: v[1] for y, v in _destatis("61111-0001_vpi.csv").items()}  # Jahresinflation (Destatis)

LAST = "2026-09"                                       # letzter Monat mit Zinsdaten (vorläufig)
MONTHS = [m for m in sorted(ZINS) if "2015-01" <= m <= LAST]


def mx(m):
    """'YYYY-MM' -> Jahr als Kommazahl (Monatsmitte)."""
    return int(m[:4]) + (int(m[5:]) - 0.5) / 12


MX = np.array([mx(m) for m in MONTHS])
Z = np.array([ZINS[m] for m in MONTHS])
I = np.array([INFL[m] for m in MONTHS])
E = np.array([EZB[m] for m in MONTHS])
EZB_LAST = EZB["2026-10"]

# ---------------------------------------------------------------- derived numbers
Z_NOW, I_NOW = ZINS[LAST], INFL[LAST]
REAL_NOW = (1 + Z_NOW / 100) / (1 + I_NOW / 100) - 1
LOSS_NOW = 10000 * REAL_NOW
VOL_NOW = VOL[LAST] / 1e6                              # Billionen €
NEG = [m for m in MONTHS if REALZ[m] < 0]
NONNEG = [m for m in MONTHS if REALZ[m] >= 0]
Z_PEAK_M = max((m for m in MONTHS if m >= "2022-01"), key=lambda m: ZINS[m])
Z_PEAK = ZINS[Z_PEAK_M]
EZB_PEAK = max(E)

# 10.000 € Ende Januar 2015 angelegt, Zinsen monatlich gutgeschrieben (Monatszins = Jahreszins / 12)
CAP = [10000.0]
for m in MONTHS[1:]:
    CAP.append(CAP[-1] * (1 + ZINS[m] / 100 / 12))
CAP = np.array(CAP)
PRICE = np.array([VPI[m] / VPI[MONTHS[0]] for m in MONTHS])
KAUF = CAP / PRICE
PRICE_UP = PRICE[-1] - 1

# Szenario: 1 Jahr, 10.000 €, Inflation wie im Jahresschnitt 2025
INF_S = CPI_Y[2025]
SCEN = [(0.0, "ohne Zinsen"), (Z_NOW, "Ø-Zins"), (EZB_LAST, "wie EZB-Satz")]
SCEN_R = [(r, lab, 100 * r, 10000 * ((1 + r / 100) / (1 + INF_S / 100) - 1)) for r, lab in SCEN]

# Steuer
PAUSCH, PAUSCH2 = 1000, 2000
TAX = 0.25 * 1.055
FREE_CAP = PAUSCH / (EZB_LAST / 100)
BIG = 100000
BIG_INT = BIG * EZB_LAST / 100
BIG_TAX = (BIG_INT - PAUSCH) * TAX
BIG_NET_RATE = (BIG_INT - BIG_TAX) / BIG * 100
BREAKEVEN = INF_S / (1 - TAX)

# Every number spoken in the narration is checked here.
assert Z_NOW == 0.52 and I_NOW == 3.3                       # "null Komma fünf zwei", "drei Komma drei"
assert REALZ[LAST] == -2.69 and -2.75 < 100 * REAL_NOW < -2.65  # "rund zwei Komma sieben"
assert 265 < -LOSS_NOW < 275                                 # "rund zweihundertsiebzig Euro"
assert 1.9 < VOL_NOW < 2.0                                   # "fast zwei Billionen Euro"
assert min(E[MX < 2022.5]) == -0.5 and all(E[MX < 2022.5] < 0)  # "negativ, bis zu minus null Komma fünf"
assert max(Z[MX < 2022.5]) <= 0.22                          # "praktisch nichts"
assert EZB_PEAK == 4.0 and EZB["2022-07"] == 0.0 and EZB["2023-09"] == 4.0  # "in gut einem Jahr auf vier Prozent"
assert Z_PEAK == 0.62 and Z_PEAK_M == "2024-01"             # "null Komma sechs zwei, Januar 2024"
assert Z_PEAK / EZB["2024-01"] < 1 / 6                       # "nicht einmal ein Sechstel"
assert EZB["2025-06"] == 2.0 and EZB["2026-09"] == EZB_LAST == 2.5 and EZB["2026-08"] < 2.5
assert all(0.4 < ZINS[m] < 0.65 for m in MONTHS if m >= "2023-08")  # "um ein halbes Prozent"
assert len(MONTHS) == 141 and len(NEG) == 132 and len(NONNEG) == 9  # "132 von 141", "neun Monate"
assert sum(m.startswith("2020") for m in NONNEG) == 5        # "vor allem 2020"
assert all(INFL[m] < 0 for m in ("2020-07", "2020-08", "2020-09", "2020-10", "2020-12"))
assert INFL["2022-10"] == INFL["2022-11"] == 8.8 and ZINS["2022-10"] <= 0.02  # "fast neun", "null"
assert 10150 < CAP[-1] < 10250                               # "rund zehntausendzweihundert"
assert 0.355 < PRICE_UP < 0.365                              # "sechsunddreißig Prozent"
assert 7450 < KAUF[-1] < 7550                                # "rund siebentausendfünfhundert"
assert 0.24 < 1 - KAUF[-1] / 10000 < 0.26                    # "ein Viertel"
assert INF_S == 2.2
assert 210 < -SCEN_R[0][3] < 220                             # "rund zweihundertfünfzehn"
assert round(100 * Z_NOW) == 52 and 162 < -SCEN_R[1][3] < 166  # "52 €", "rund hundertvierundsechzig"
assert round(100 * EZB_LAST) == 250 and 25 < SCEN_R[2][3] < 30  # "250 €", "knapp dreißig"
assert round(FREE_CAP) == 40000                              # "bis zu vierzigtausend Euro"
assert 26.35 < 100 * TAX < 26.4                              # "sechsundzwanzig Komma vier"
assert BIG_INT == 2500 and 390 < BIG_TAX < 400               # "zweitausendfünfhundert", "rund vierhundert"
assert 2.09 < BIG_NET_RATE < 2.12 and BIG_NET_RATE < INF_S   # "zwei Komma eins"
assert 2.9 < BREAKEVEN < 3.0                                 # "knapp drei Prozent"

SRC = "Quelle: Deutsche Bundesbank, MFI-Zinsstatistik"


def pct(v, dec=1, sign=False):
    s = f"{v:+.{dec}f}" if sign else f"{v:.{dec}f}"
    return s.replace("-", "−").replace(".", ",") + " %"


def dec(v, d=1):
    return f"{v:.{d}f}".replace(".", ",").replace("-", "−")


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


def legend(d, items, y, alpha):
    x = 260
    for name, col in items:
        thick_line(d, [(x, y), (x + 40, y)], fade(col, alpha), 6)
        text(d, (x + 52, y), name, 24, FG, alpha, "lm", "Medium")
        x += 52 + len(name) * 13 + 60


YT = range(2015, 2027)
YFMT = lambda y: f"’{y % 100:02}"


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 190), "September 2026", t, S.c(0), 56, MUTED, "mm", "Bold")
    cards = [((300, 290, 900, 650), "Ø-Zins täglich fällig", Z_NOW, 2, BLUE, S.c(0) + 0.5),
             ((1020, 290, 1620, 650), "Inflation", I_NOW, 1, RED, S.c(1))]
    for box, label, val, dd, col, start in cards:
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        card(d, box, a, col)
        cx = (box[0] + box[2]) / 2
        text(d, (cx, box[1] + 80), label, 38, MUTED, a, "mm", "SemiBold")
        p = prog(t, start + 0.2, 1.2, ease_in_out)
        text(d, (cx, box[1] + 210), pct(val * p, dd), 110, col, a, "mm", "Black")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        rrect(d, (360, 710, 1560, 810), 20, fill=fade((50, 26, 30), a), outline=fade(RED, a * 0.6), width=2)
        text(d, (400, 760), "Realzins", 40, FG, a, "lm", "SemiBold")
        text(d, (1520, 760), pct(100 * REAL_NOW, sign=True), 56, RED, a, "rm", "Black")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        text(d, (W / 2, 880), f"10.000 € → ≈ −{eur(round(-LOSS_NOW, -1))} Kaufkraft pro Jahr", 44, FG, a, "mm", "Bold")
    footer(d, prog(t, S.c(4), 0.6), "Quellen: Deutsche Bundesbank (SUD101), Destatis/Bundesbank (VPI) · Sept. 2026 vorläufig")


def draw_daten(img, d, t, S):
    title(d, t, "Woher kommt die Zahl?", S.c(0), "MFI-Zinsstatistik der Deutschen Bundesbank, monatlich")
    a2 = prog(t, S.c(2), 0.5)
    if a2 > 0:
        card(d, (250, 250, 1150, 380), a2, BLUE)
        text(d, (290, 300), "Einlagen privater Haushalte,", 38, FG, a2, "lm", "Bold")
        text(d, (290, 348), "täglich fällig", 38, BLUE, a2, "lm", "Bold")
    for i, (name, start) in enumerate((("Tagesgeld", S.c(3) + 0.3), ("Girokonto", S.c(3) + 1.3))):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        x0 = 250 + i * 470
        dy = (1 - a) * 25
        rrect(d, (x0, 430 + dy, x0 + 430, 560 + dy), 22, fill=fade((30, 42, 66), a),
              outline=fade((60, 76, 108), a), width=2)
        text(d, (x0 + 215, 495 + dy), name, 44, FG, a, "mm", "Bold")
    text(d, (710, 495), "+", 56, MUTED, prog(t, S.c(3) + 1.3, 0.4), "mm", "Black")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        text(d, (250, 640), "Volumen zusammen", 32, MUTED, a4, "lm", "Medium")
        text(d, (250, 710), f"≈ {dec(VOL_NOW, 2)} Billionen €", 64, FG, a4, "lm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        card(d, (1250, 430, 1860, 760), a5, AMBER)
        text(d, (1290, 490), "Durchschnittszins", 32, MUTED, a5, "lm", "SemiBold")
        text(d, (1290, 580), pct(Z_NOW, 2), 90, BLUE, a5, "lm", "Black")
        text(d, (1290, 665), "Girokonten zahlen meist", 28, FG, a5, "lm", "Medium")
        text(d, (1290, 705), "wenig oder nichts", 28, AMBER, a5, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.6), SRC + " · SUD101, SUD201 · Stand Sept. 2026 (vorläufig)")


def draw_ezb(img, d, t, S):
    title(d, t, "EZB-Einlagesatz vs. Ø-Zins", S.c(0), "Monatswerte, Januar 2015 bis Oktober 2026")
    ch = Chart((260, 260, 1400, 860), (2015, 2026.9), (-1, 4.5))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, YT, range(-1, 5), YFMT, lambda v: f"{v} %")
    legend(d, [("EZB-Einlagesatz", VIOLET), ("Ø-Zins täglich fällig", BLUE)], 225, ax)
    footer(d, ax, "Quelle: Deutsche Bundesbank · SU0200 (EZB-Einlagefazilität, Monatsende), SUD101")
    if ax > 0:
        _, py = ch.px(0, 0)
        d.line((ch.x0, py, ch.x1, py), fill=fade((90, 102, 128), ax), width=2)
    ex = np.array([mx(m) for m in sorted(EZB) if "2015-01" <= m <= "2026-10"])
    ey = np.array([EZB[m] for m in sorted(EZB) if "2015-01" <= m <= "2026-10"])
    up = piecewise(t, [(S.c(1) + 0.3, 2015), (S.e(3), 2022.5), (S.c(4), 2022.5), (S.e(5), 2024.2),
                       (S.c(6), 2024.2), (S.e(6), 2026.9)]) if t > S.c(1) + 0.3 else 2015
    if up > 2015:
        ch.line(d, ex, ey, VIOLET, 6, up)
        ch.line(d, MX, Z, BLUE, 6, min(up, MX[-1]))
    a2 = prog(t, S.c(2) + 0.5, 0.5) * (1 - prog(t, S.c(4), 0.5))
    if a2 > 0:
        p = ch.px(2018.7, -0.5)
        text(d, (p[0], p[1] + 30), "negativ: bis −0,5 %", 30, VIOLET, a2, "mt", "Bold")
    if up >= mx("2023-09"):
        pe = ch.px(mx("2023-09"), 4.0)
        dot(d, pe, 9, VIOLET)
        text(d, (pe[0] - 14, pe[1] - 14), "4,0 %", 30, VIOLET, 1.0, "rb", "Black")
    if up >= mx(Z_PEAK_M):
        pz = ch.px(mx(Z_PEAK_M), Z_PEAK)
        dot(d, pz, 10, BLUE)
        text(d, (pz[0], pz[1] - 22), pct(Z_PEAK, 2), 30, BLUE, 1.0, "mb", "Black")
    a6 = prog(t, S.c(6) + 1.5, 0.5) if up >= 2026.8 else 0
    if a6 > 0:
        pe = ch.px(2026.85, EZB_LAST)
        text(d, (pe[0] - 6, pe[1] - 16), pct(EZB_LAST, 2), 28, VIOLET, a6, "rb", "Bold")
    a5b = prog(t, S.c(5) + 1.2, 0.5)
    if a5b > 0:
        card(d, (1460, 330, 1870, 600), a5b, BLUE)
        text(d, (1490, 385), "Weitergegeben", 30, MUTED, a5b, "lm", "SemiBold")
        text(d, (1490, 455), "< 1/6", 76, BLUE, a5b, "lm", "Black")
        text(d, (1490, 530), f"{dec(Z_PEAK, 2)} von {dec(EZB['2024-01'], 2)} %", 28, FG, a5b, "lm", "Medium")
        text(d, (1490, 568), "(Januar 2024)", 24, MUTED, a5b, "lm", "Medium")


def draw_real(img, d, t, S):
    title(d, t, "Zins gegen Inflation", S.c(0), "Realzins = (1 + Zins) ÷ (1 + Inflation) − 1")
    ch = Chart((260, 300, 1400, 880), (2015, 2026.9), (-1.6, 9.5))
    ax = prog(t, S.c(3), 0.8)
    a2 = prog(t, S.c(2), 0.5) * (1 - prog(t, S.c(3), 0.5))
    if a2 > 0:
        card(d, (250, 290, 1500, 640), a2, VIOLET)
        text(d, (300, 360), "September 2026", 32, MUTED, a2, "lm", "SemiBold")
        text(d, (300, 450), f"(1 + {dec(Z_NOW / 100, 4)}) ÷ (1 + {dec(I_NOW / 100, 3)}) − 1", 52, FG, a2,
             "lm", "Bold")
        text(d, (300, 560), "= " + pct(100 * REAL_NOW, 2, sign=True) + " real", 60, RED, a2, "lm", "Black")
    if ax > 0:
        ch.axes(d, ax, YT, range(0, 10, 2), YFMT, lambda v: f"{v} %")
        legend(d, [("Inflation", RED), ("Ø-Zins täglich fällig", BLUE)], 245, ax)
        _, py = ch.px(0, 0)
        d.line((ch.x0, py, ch.x1, py), fill=fade((90, 102, 128), ax), width=2)
        footer(d, ax, "Quelle: Deutsche Bundesbank · SUD101, SUR101; VPI (Destatis/Bundesbank)")
    up = 2015 + (MX[-1] - 2015) * prog(t, S.c(3) + 0.5, S.e(3) - S.c(3), ease_in_out)
    if up > 2015:
        ch.band(d, MX, np.maximum(I, Z), Z, fade(RED, 0.3), up)
        ch.line(d, MX, I, RED, 5, up)
        ch.line(d, MX, Z, BLUE, 5, up)
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        card(d, (1460, 300, 1870, 560), a4, RED)
        text(d, (1490, 355), "Realzins negativ", 30, MUTED, a4, "lm", "SemiBold")
        text(d, (1490, 435), f"{len(NEG)} / {len(MONTHS)}", 64, RED, a4, "lm", "Black")
        text(d, (1490, 510), "Monaten seit 2015", 28, FG, a4, "lm", "Medium")
    a4b = prog(t, S.c(4) + 2.5, 0.5)
    if a4b > 0:
        x0, _ = ch.px(2020.4, 0)
        x1, _ = ch.px(2021.05, 0)
        _, yb = ch.px(0, -1.05)
        d.line((x0, yb, x1, yb), fill=fade(GREEN, a4b), width=4)
        text(d, (x0 - 10, yb), "2020: Preise gesunken", 24, GREEN, a4b, "rm", "Bold")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        p = ch.px(mx("2022-10"), 8.8)
        dot(d, p, 10, fade(RED, a5))
        text(d, (p[0] - 18, p[1]), "Okt. 2022: 8,8 % vs. 0,01 %", 28, FG, a5, "rm", "Bold")


def draw_seit2015(img, d, t, S):
    title(d, t, "10.000 € seit 2015 zum Durchschnittszins", S.c(0),
          "Angelegt Ende Januar 2015, Zinsen stehen gelassen, bis September 2026")
    ch = Chart((260, 270, 1300, 860), (2015, 2026.9), (7000, 10600))
    ax = prog(t, S.c(1), 0.8)
    ch.axes(d, ax, YT, range(7000, 10501, 1000), YFMT, lambda v: f"{v // 1000}.000 €")
    legend(d, [("Kontostand", BLUE), ("Kaufkraft (in Euro von 2015)", AMBER)], 235, ax)
    footer(d, ax, "Modellrechnung mit echten Daten: Bundesbank SUD101, VPI (Destatis/Bundesbank)")
    u1 = 2015 + (MX[-1] - 2015) * prog(t, S.c(1) + 0.5, S.e(2) - S.c(1) - 0.5, ease_in_out)
    if u1 > 2015:
        ch.line(d, MX, CAP, BLUE, 6, u1)
    u2 = 2015 + (MX[-1] - 2015) * prog(t, S.c(3), S.c(4) + 0.4 - S.c(3), ease_in_out)
    if u2 > 2015:
        ch.band(d, MX, CAP, KAUF, fade(RED, 0.25), u2)
        ch.line(d, MX, CAP, BLUE, 6, u1)
        ch.line(d, MX, KAUF, AMBER, 6, u2)
    for cue, y0, label, val, col in ((2, 300, "Kontostand", CAP[-1], BLUE),
                                     (4, 520, "Kaufkraft", KAUF[-1], AMBER)):
        a = prog(t, S.c(cue) + 0.5, 0.5)
        if a <= 0:
            continue
        card(d, (1380, y0, 1860, y0 + 180), a, col)
        text(d, (1410, y0 + 55), label + " Sept. 2026", 28, MUTED, a, "lm", "SemiBold")
        text(d, (1410, y0 + 125), "≈ " + eur(round(val, -1)), 60, col, a, "lm", "Black")
    a3 = prog(t, S.c(3), 0.5)
    text(d, (1380, 760), f"Preise: {pct(100 * PRICE_UP, 0, sign=True)}", 36, RED, a3, "lm", "Bold")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (1380, 820), "≈ ein Viertel weniger", 36, FG, a5, "lm", "Black")


def draw_szenarien(img, d, t, S):
    title(d, t, "3 Fälle für ein Jahr", S.c(0),
          f"Annahme: 10.000 €, Inflation {pct(INF_S)} (Jahresdurchschnitt 2025, Destatis)")
    cols = [GRAY, BLUE, GREEN]
    for i, ((rate, lab, zinsen, real), col) in enumerate(zip(SCEN_R, cols)):
        start = S.c(2 + i)
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 540
        dy = (1 - a) * 30
        card(d, (x0, 300 + dy, x0 + 500, 800 + dy), a, col)
        cx = x0 + 250
        text(d, (cx, 360 + dy), f"Zins {pct(rate, 2 if 0 < rate < 1 else (1 if rate else 0))}", 40, col, a, "mm", "Black")
        text(d, (cx, 405 + dy), lab, 26, MUTED, a, "mm", "Medium")
        text(d, (cx, 490 + dy), "Zinsen", 28, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 545 + dy), "+" + eur(zinsen), 52, FG, a, "mm", "Black")
        d.line((x0 + 50, 610 + dy, x0 + 450, 610 + dy), fill=fade((70, 82, 108), a), width=2)
        text(d, (cx, 660 + dy), "Kaufkraft", 28, MUTED, a, "mm", "SemiBold")
        sign = "+" if real >= 0 else "−"
        text(d, (cx, 725 + dy), sign + eur(abs(real)), 64, GREEN if real >= 0 else RED, a, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        text(d, (W / 2, 900), "Kaufkraft bleibt nur, wenn Zins ≥ Inflation", 46, AMBER, a5, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "Modellrechnung vor Steuern: 10.000 € × ((1 + Zins) ÷ (1 + Inflation) − 1)")


def draw_steuern(img, d, t, S):
    title(d, t, "Und die Steuer?", S.c(0), "Abgeltungsteuer auf Zinsen, Stand 2026")
    swap = prog(t, S.c(4), 0.5)
    a1 = prog(t, S.c(1), 0.5) * (1 - swap)
    if a1 > 0:
        card(d, (250, 250, 1000, 520), a1, GREEN)
        text(d, (290, 305), "Sparerpauschbetrag", 32, MUTED, a1, "lm", "SemiBold")
        text(d, (290, 390), "1.000 € / Jahr", 64, GREEN, a1, "lm", "Black")
        text(d, (290, 470), "2.000 € bei Zusammenveranlagung", 28, FG, a1, "lm", "Medium")
    a2 = prog(t, S.c(2), 0.5) * (1 - swap)
    if a2 > 0:
        text(d, (290, 590), f"bei {pct(EZB_LAST)} Zins steuerfrei bis", 32, FG, a2, "lm", "SemiBold")
        text(d, (290, 655), eur(FREE_CAP) + " Guthaben", 52, GREEN, a2, "lm", "Black")
    a3 = prog(t, S.c(3), 0.5) * (1 - swap)
    if a3 > 0:
        card(d, (1100, 250, 1860, 520), a3, RED)
        text(d, (1140, 305), "darüber", 32, MUTED, a3, "lm", "SemiBold")
        text(d, (1140, 380), "25 % + 5,5 % Soli darauf", 44, FG, a3, "lm", "Bold")
        text(d, (1140, 460), f"= {dec(100 * TAX, 3)} % (ohne Kirchensteuer)", 34, RED, a3, "lm", "Black")
    a4 = prog(t, S.c(4) + 0.3, 0.5)
    if a4 > 0:
        card(d, (250, 250, 1100, 760), a4, AMBER)
        text(d, (290, 305), f"Beispiel: {eur(BIG)} zu {pct(EZB_LAST)}", 36, FG, a4, "lm", "Bold")
        rows = [("Zinsen", "+" + eur(BIG_INT), FG, S.c(4) + 0.5),
                ("über Pauschbetrag", eur(BIG_INT - PAUSCH), MUTED, S.c(4) + 1.5),
                ("Steuer (26,375 %)", "−" + eur(BIG_TAX), RED, S.c(4) + 2.5),
                ("netto", eur(BIG_INT - BIG_TAX), GREEN, S.c(5))]
        for j, (lab, val, col, st) in enumerate(rows):
            b = prog(t, st, 0.5) * a4
            y = 390 + j * 75
            text(d, (290, y), lab, 34, MUTED if j < 3 else FG, b, "lm", "SemiBold")
            text(d, (1060, y), val, 40, col, b, "rm", "Black")
        b = prog(t, S.c(5), 0.5) * a4
        d.line((290, 660, 1060, 660), fill=fade((70, 82, 108), b), width=2)
        text(d, (290, 710), "Nettozins", 34, FG, b, "lm", "Bold")
        text(d, (1060, 710), f"{pct(BIG_NET_RATE, 2)} < {pct(INF_S)} Inflation", 38, AMBER, b, "rm", "Black")
    a6 = prog(t, S.c(6), 0.5)
    if a6 > 0:
        card(d, (1180, 250, 1860, 480), a6)
        text(d, (1220, 310), "Steuer auf den ganzen Zins –", 30, FG, a6, "lm", "SemiBold")
        text(d, (1220, 355), "auch auf den Teil, der nur", 30, FG, a6, "lm", "SemiBold")
        text(d, (1220, 400), "die Inflation ausgleicht", 30, AMBER, a6, "lm", "Bold")
    a7 = prog(t, S.c(7), 0.5)
    if a7 > 0:
        card(d, (1180, 530, 1860, 760), a7, VIOLET)
        text(d, (1220, 585), "Nötiger Zins für ±0 real", 30, MUTED, a7, "lm", "SemiBold")
        text(d, (1220, 665), f"≈ {pct(BREAKEVEN, 2)}", 64, VIOLET, a7, "lm", "Black")
        text(d, (1220, 725), f"{pct(INF_S)} ÷ (1 − 0,26375), über dem Pauschbetrag", 22, MUTED, a7, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "§ 20 Abs. 9 und § 32d EStG · Modellrechnung, keine Steuerberatung")


def draw_grenzen(img, d, t, S):
    title(d, t, "3 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Durchschnitt inkl. Girokonten",
              "Tagesgeld allein weist die Bundesbank hier nicht getrennt aus."),
             (S.c(2), "2", "Zinsen sind variabel",
              "Hohe Angebote gelten oft nur für Neukunden und befristet."),
             (S.c(3), "3", "Persönliche Inflation",
              "Hängt von deinem Warenkorb ab · Sept.-2026-Werte vorläufig.")]
    for i, (start, n, head, line) in enumerate(items):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 240 + i * 210
        card(d, (250, y, 1670, y + 180), a)
        dot(d, (320, y + 90), 38, fade(AMBER, a))
        text(d, (320, y + 92), n, 40, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + 55), head, 40, FG, a, "lm", "Bold")
        text(d, (400, y + 115), line, 30, MUTED, a, "lm", "Medium")


def draw_fazit(img, d, t, S):
    text_pop(d, (W / 2, 170), "Lohnt sich Tagesgeld nach Inflation?", t, S.c(0), 58, FG, "mm", "Black")
    rows = [(S.c(1), GREEN, "Gegenüber 0 % auf dem Girokonto:", "jeder Zehntelpunkt verringert den Verlust"),
            (S.c(2), RED, "Im Durchschnitt seit 2015:", "fast immer Kaufkraft verloren"),
            (S.c(3), BLUE, "Stärke von Tagesgeld:", "jederzeit verfügbar – nicht die Rendite")]
    for i, (start, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 170
        card(d, (300, y, 1620, y + 140), a, col)
        text(d, (340, y + 50), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 100), b_txt, 40, FG, a, "lm", "Bold")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        rrect(d, (300, 820, 1620, 930), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 875), "Messlatte: Zins nach Steuern  vs.  Inflation", 44, AMBER, a, "mm", "Black")


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
        text(d, (1060, 580), "Dispo, Ratenkredit, Bau:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Was Kredite kosten", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "mit Bundesbank-Daten", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Null Komma fünf zwei Prozent. So viel Zinsen gab es im September zweitausendsechsundzwanzig im Schnitt auf Geld, das täglich verfügbar ist.",
            "Die Inflation lag im selben Monat bei drei Komma drei Prozent.",
            "Real ist das ein Minus von rund zwei Komma sieben Prozent.",
            "Bliebe es ein Jahr lang dabei, verlieren zehntausend Euro rund zweihundertsiebzig Euro an Kaufkraft.",
            "Lohnt sich Tagesgeld also überhaupt noch? Wir rechnen es mit den Zahlen der Bundesbank durch.",
        ], draw_hook),
        Scene("daten", [
            "Erst einmal: Woher kommt diese Zahl?",
            "Die Bundesbank erhebt jeden Monat, welche Zinsen Banken ihren Kunden zahlen. Das ist die MFI-Zinsstatistik.",
            "Eine Kategorie darin heißt: Einlagen privater Haushalte, täglich fällig.",
            "Dazu zählt alles, worauf du jederzeit zugreifen kannst. Tagesgeld, aber auch das Girokonto.",
            "Zusammen sind das fast zwei Billionen Euro.",
            "Girokonten zahlen meist wenig oder gar keine Zinsen. Deshalb ist dieser Durchschnitt so niedrig, und ein reines Tagesgeldkonto bringt oft mehr.",
        ], draw_daten),
        Scene("ezb", [
            "Wovon hängen diese Zinsen ab? Vor allem von der Europäischen Zentralbank.",
            "Banken können überschüssiges Geld bei der EZB parken. Der Zins dafür heißt Einlagesatz.",
            "Von zweitausendfünfzehn bis Mitte zweitausendzweiundzwanzig war er negativ, bis zu minus null Komma fünf Prozent.",
            "Entsprechend gab es auf täglich fälliges Geld praktisch nichts.",
            "Dann kam die Inflation, und die EZB erhöhte innerhalb von gut einem Jahr auf vier Prozent.",
            "Der Durchschnittszins kletterte dagegen nur auf null Komma sechs zwei Prozent, im Januar zweitausendvierundzwanzig. Nicht einmal ein Sechstel davon.",
            "Zweitausendfünfundzwanzig senkte die EZB auf zwei Prozent, seit September zweitausendsechsundzwanzig sind es wieder zwei Komma fünf. Der Durchschnittszins blieb die ganze Zeit um ein halbes Prozent.",
        ], draw_ezb),
        Scene("realzins", [
            "Jetzt das Entscheidende: Zins gegen Inflation.",
            "Der Realzins ist das, was nach der Inflation vom Zins übrig bleibt.",
            "Die Rechnung für September zweitausendsechsundzwanzig: eins Komma null null fünf zwei, geteilt durch eins Komma null drei drei, minus eins. Ergibt minus zwei Komma sieben Prozent.",
            "Und so sieht das seit zweitausendfünfzehn aus. Rot die Inflation, blau der Durchschnittszins.",
            "In hundertzweiunddreißig von hunderteinundvierzig Monaten war der Realzins negativ. Nur in neun Monaten nicht, vor allem zweitausendzwanzig, als die Preise kurz gesunken sind.",
            "Am größten war die Lücke Ende zweitausendzweiundzwanzig: Inflation fast neun Prozent, Zins praktisch null.",
        ], draw_real),
        Scene("seit2015", [
            "Was bedeutet das über die ganze Zeit?",
            "Angenommen, du hättest Anfang zweitausendfünfzehn zehntausend Euro zum Durchschnittszins angelegt und die Zinsen stehen lassen.",
            "Bis September zweitausendsechsundzwanzig wären daraus rund zehntausendzweihundert Euro geworden.",
            "Die Preise sind im selben Zeitraum aber um sechsunddreißig Prozent gestiegen.",
            "Gemessen an den Preisen von damals sind deine zehntausend Euro nur noch rund siebentausendfünfhundert Euro wert.",
            "Ein Viertel der Kaufkraft ist weg, obwohl auf dem Konto mehr steht als am Anfang.",
        ], draw_seit2015),
        Scene("szenarien", [
            "Und wenn man einen besseren Zins bekommt? Rechnen wir drei Fälle für ein Jahr durch.",
            "Annahme: zehntausend Euro und eine Inflation von zwei Komma zwei Prozent, so viel wie im Jahresschnitt zweitausendfünfundzwanzig.",
            "Ohne Zinsen verlierst du rund zweihundertfünfzehn Euro an Kaufkraft.",
            "Mit dem Durchschnittszins von null Komma fünf zwei Prozent bekommst du zweiundfünfzig Euro Zinsen. Trotzdem fehlen real rund hundertvierundsechzig Euro.",
            "Mit zwei Komma fünf Prozent, so hoch wie der aktuelle EZB-Einlagesatz, sind es zweihundertfünfzig Euro Zinsen und ein kleines Plus von knapp dreißig Euro.",
            "Die Kaufkraft bleibt also nur erhalten, wenn der Zins mindestens so hoch ist wie die Inflation.",
        ], draw_szenarien),
        Scene("steuern", [
            "Aber Moment: Zinsen sind steuerpflichtig.",
            "Bis zum Sparerpauschbetrag von tausend Euro im Jahr bleiben sie steuerfrei. Für Paare, die zusammen veranlagt werden, sind es zweitausend Euro.",
            "Bei zwei Komma fünf Prozent Zins reicht das für ein Guthaben von bis zu vierzigtausend Euro.",
            "Darüber fallen fünfundzwanzig Prozent Abgeltungsteuer an, plus Solidaritätszuschlag. Zusammen rund sechsundzwanzig Komma vier Prozent, ohne Kirchensteuer.",
            "Ein Beispiel: hunderttausend Euro zu zwei Komma fünf Prozent. Das sind zweitausendfünfhundert Euro Zinsen. Davon liegen tausendfünfhundert über dem Pauschbetrag, darauf werden rund vierhundert Euro Steuer fällig.",
            "Netto bleiben zwei Komma eins Prozent. Weniger als die Inflation von zwei Komma zwei.",
            "Denn die Steuer wird auf den ganzen Zins fällig, auch auf den Teil, der nur die Inflation ausgleicht.",
            "Für Zinsen über dem Pauschbetrag gilt deshalb: Bei zwei Komma zwei Prozent Inflation braucht es knapp drei Prozent Zins, um real nicht zu verlieren.",
        ], draw_steuern),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Der Durchschnitt enthält auch Girokonten. Tagesgeld allein weist die Bundesbank in dieser Statistik nicht getrennt aus.",
            "Zweitens: Tagesgeldzinsen sind variabel. Banken können sie jederzeit ändern, und hohe Angebote gelten oft nur für Neukunden und nur ein paar Monate.",
            "Drittens: Auch die Inflation ist ein Durchschnitt. Deine persönliche Inflation hängt davon ab, wofür du dein Geld ausgibst. Und die Zinswerte für September zweitausendsechsundzwanzig sind noch vorläufig.",
        ], draw_grenzen),
        Scene("fazit", [
            "Lohnt sich Tagesgeld nach Inflation also noch?",
            "Gegenüber einem Girokonto ohne Zinsen schon: Jeder Zehntelprozentpunkt verringert den Verlust.",
            "Aber im Durchschnitt hat täglich verfügbares Geld seit zweitausendfünfzehn fast durchgehend an Kaufkraft verloren.",
            "Die Stärke von Tagesgeld ist, dass das Geld jederzeit verfügbar ist. Nicht die Rendite.",
            "Die Messlatte bleibt immer dieselbe: Zins nach Steuern gegen Inflation.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Daten, Quellen und Formeln findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Im nächsten Video rechnen wir nach, was Kredite in Deutschland wirklich kosten: vom Dispo bis zur Baufinanzierung.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
