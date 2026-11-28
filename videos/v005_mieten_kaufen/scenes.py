"""Video 005: Mieten oder kaufen? Die Rechnung mit echten Zahlen (Bundesbank-Indikatoren Wohnimmobilienmarkt)."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     dot, ease_in_out, eur, fade, lerp, piecewise, prog, rrect, text, text_pop,
                     thick_line)

# ---------------------------------------------------------------- data (Bundesbank, Stand 25.11.2026)
DATA = Path(__file__).parent / "data"


def _bbk(name):
    out = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and c[0][:4].isdigit() and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


KPM = {int(k): v for k, v in _bbk("BBDY1_kpm_deutschland.csv").items()}      # Kaufpreis ÷ Jahresmiete
KPM127 = {int(k): v for k, v in _bbk("BBDY1_kpm_127_staedte.csv").items()}
KPM7 = {int(k): v for k, v in _bbk("BBDY1_kpm_7_grossstaedte.csv").items()}
PRICE = {int(k): v for k, v in _bbk("BBDY1_preisindex_wohnen.csv").items()}   # 2010 = 100
RENT = {int(k): v for k, v in _bbk("BBDY1_mietindex_wohnen.csv").items()}     # 2010 = 100
_bz = _bbk("SUD118_wohnungsbau_5_10j.csv")                                     # monatlich
BAUZ = {y: sum(_bz[f"{y}-{m:02}"] for m in range(1, 13)) / 12 for y in range(2010, 2026)}
BAUZ_NOW = _bz["2026-09"]

YEARS = list(range(2010, 2026))
YIELD = {y: 100 / KPM[y] for y in YEARS}                                       # Brutto-Mietrendite in %

# ---------------------------------------------------------------- Beispiel (Modellrechnung mit Annahmen)
F = KPM[2025]
RENT_M = 1000.0                       # Kaltmiete pro Monat
PRICE_W = F * RENT_M * 12             # Kaufpreis
NK_RATE, EK_RATE, TILG, INST = 0.10, 0.20, 0.02, 0.01   # Annahmen
R_SAVE, RENT_UP = 0.025, 0.02                             # Annahmen Mieter
Z = BAUZ_NOW / 100
NK = NK_RATE * PRICE_W
EK = EK_RATE * PRICE_W + NK
LOAN = PRICE_W - EK_RATE * PRICE_W
RATE = LOAN * (Z + TILG) / 12
INST_M = INST * PRICE_W / 12
OUT = RATE + INST_M
INT_M1 = LOAN * Z / 12
TILG_M1 = RATE - INT_M1
OPP_M1 = EK * R_SAVE / 12
LOST_M1 = INT_M1 + INST_M + OPP_M1


def ten_years(g):
    """Vermögen nach 10 Jahren: Käufer (Wohnung − Restschuld) vs. Mieter (Eigenkapital + Differenz angelegt)."""
    debt, acc, rent = LOAN, EK, RENT_M
    for k in range(120):
        if k and k % 12 == 0:
            rent *= 1 + RENT_UP
        debt -= RATE - debt * Z / 12
        acc = acc * (1 + R_SAVE / 12) + (OUT - rent)
    return PRICE_W * (1 + g) ** 10 - debt, acc, debt


def breakeven():
    lo, hi = -0.05, 0.10
    for _ in range(60):
        mid = (lo + hi) / 2
        b, a, _ = ten_years(mid)
        lo, hi = (mid, hi) if b < a else (lo, mid)
    return mid


BE = breakeven()
CASES = [(g, ten_years(g)[0]) for g in (0.0, 0.01, 0.02, 0.03)]
RENTER = ten_years(0)[1]
DEBT10 = ten_years(0)[2]
P_15_25 = (PRICE[2025] / PRICE[2015]) ** 0.1 - 1
P_22_25 = PRICE[2025] / PRICE[2022] - 1
R_22_25 = RENT[2025] / RENT[2022] - 1

# Every number spoken in the narration is checked here.
assert KPM[2025] == 26.1 and KPM127[2025] == 27.1 and KPM7[2025] == 30.6     # Faktoren 2025
assert 3.8 < YIELD[2025] < 3.85                                              # "rund drei Komma acht Prozent"
assert 3.25 < 100 / KPM7[2025] < 3.3                                          # "knapp drei Komma drei"
assert KPM[2010] == 20.0 and KPM[2022] == 30.4 == max(KPM[y] for y in YEARS)  # "zwanzig", "dreißig Komma vier"
assert round(PRICE[2025] - 100) == 108 and round(RENT[2025] - 100) == 76     # "+108 %", "+76 %"
assert PRICE[2022] == max(PRICE[y] for y in YEARS) and -0.015 < P_22_25 < -0.005  # "gut ein Prozent weniger"
assert 0.12 < R_22_25 < 0.13                                                  # "rund dreizehn Prozent"
assert 3.5 < YIELD[2020] < 3.52 and 1.08 < BAUZ[2020] < 1.1                   # "drei Komma fünf", "eins Komma eins"
assert all(YIELD[y] > BAUZ[y] for y in range(2010, 2023))                     # bis 2022 Mietrendite über Bauzins
assert BAUZ[2023] > YIELD[2023] and abs(YIELD[2025] - BAUZ[2025]) < 0.4       # seit 2023 nah beieinander
assert BAUZ_NOW == 3.91 and BAUZ_NOW > YIELD[2025]
assert PRICE_W == 313200 and NK == 31320 and EK == 93960 and LOAN == 250560
assert round(RATE) == 1234 and INST_M == 261 and round(OUT) == 1495
assert round(INT_M1) == 816 and round(TILG_M1) == 418 and round(OPP_M1) == 196 and round(LOST_M1) == 1273
assert 175000 < RENTER < 176500                                               # "rund 175.700"
assert 123000 < CASES[0][1] < 124500 and 192000 < CASES[2][1] < 193000         # "rund 123.800", "rund 192.400"
assert 0.015 < BE < 0.016                                                     # "gut eineinhalb Prozent"
assert 0.05 < P_15_25 < 0.052                                                 # "gut fünf Prozent pro Jahr"
assert 189000 < DEBT10 < 190000                                               # Restschuld nach 10 Jahren

SRC = "Quelle: Deutsche Bundesbank, Indikatorensystem Wohnimmobilienmarkt"


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


def legend(d, items, y, alpha, x=260):
    for name, col in items:
        thick_line(d, [(x, y), (x + 40, y)], fade(col, alpha), 6)
        text(d, (x + 52, y), name, 24, FG, alpha, "lm", "Medium")
        x += 52 + len(name) * 13 + 60


YFMT = lambda y: f"’{y % 100:02}"
XS = np.array(YEARS, float)


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 160), "Mieten oder kaufen?", t, S.c(0), 64, FG, "mm", "Black")
    cards = [((260, 270, 860, 600), "Kaufpreis einer Wohnung", f"{dec(F)} ×", "Jahresmiete", BLUE, S.c(0) + 0.6),
             ((1060, 270, 1660, 600), "Bauzins, 5–10 Jahre fest", pct(BAUZ_NOW, 2), "September 2026", RED, S.c(1))]
    for box, head, val, sub, col, start in cards:
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        card(d, box, a, col)
        cx = (box[0] + box[2]) / 2
        text(d, (cx, box[1] + 70), head, 34, MUTED, a, "mm", "SemiBold")
        text(d, (cx, box[1] + 190), val, 100, col, a, "mm", "Black")
        text(d, (cx, box[1] + 285), sub, 30, FG, a, "mm", "Medium")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        rrect(d, (260, 680, 1660, 820), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 730), "Kaufen lohnt sich in unserer Rechnung erst ab", 36, FG, a, "mm", "SemiBold")
        text(d, (W / 2, 785), f"≈ {pct(100 * BE)} Wertsteigerung pro Jahr", 46, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6), SRC + " (2025) · MFI-Zinsstatistik SUD118 · Modellrechnung mit Annahmen")


def draw_faktor(img, d, t, S):
    title(d, t, "Der Kaufpreis-Miet-Faktor", S.c(0), "Kaufpreis ÷ Jahreskaltmiete, Eigentumswohnungen, 2025")
    bars = [("Deutschland", KPM[2025], BLUE, S.c(1)), ("127 Städte", KPM127[2025], VIOLET, S.c(2)),
            ("7 Großstädte", KPM7[2025], RED, S.c(2) + 0.6)]
    for i, (lab, v, col, start) in enumerate(bars):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 130
        text(d, (600, y + 40), lab, 36, FG, a, "rm", "SemiBold")
        w = v * 26 * prog(t, start, 0.9, ease_in_out)
        rrect(d, (630, y + 8, 630 + w, y + 72), 12, fill=fade(col, a))
        text(d, (630 + w + 18, y + 40), f"{dec(v)} Jahresmieten", 36, col, a, "lm", "Black")
    a3 = prog(t, S.c(3), 0.5)
    if a3 > 0:
        card(d, (250, 700, 1670, 900), a3, AMBER)
        text(d, (300, 760), "Umgekehrt: Mietrendite = 1 ÷ Faktor", 36, FG, a3, "lm", "Bold")
        text(d, (300, 840), f"1 ÷ {dec(F)} = {pct(YIELD[2025], 2)} pro Jahr, vor Kosten", 44, AMBER, a3, "lm",
             "Black")
    footer(d, prog(t, S.c(1), 0.5), SRC + " (bulwiengesa-Daten)")


def draw_verlauf(img, d, t, S):
    title(d, t, "Kaufpreise vs. Mieten", S.c(0), "Eigentumswohnungen, Deutschland, 2010 = 100")
    ch = Chart((260, 260, 1400, 870), (2010, 2025), (90, 220))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, range(2010, 2026, 3), range(100, 221, 40), YFMT, str)
    legend(d, [("Kaufpreise", BLUE), ("Mieten (Neuvermietung)", GREEN)], 225, ax)
    footer(d, ax, SRC + " · Preis- und Mietindex")
    up = piecewise(t, [(S.c(1), 2010), (S.e(2), 2022), (S.c(3), 2022), (S.e(3), 2025)]) if t > S.c(1) else 2010
    if up > 2010:
        ch.line(d, XS, np.array([PRICE[y] for y in YEARS]), BLUE, 6, up)
        ch.line(d, XS, np.array([RENT[y] for y in YEARS]), GREEN, 6, up)
    a2 = prog(t, S.c(2) + 0.5, 0.5) if up >= 2021.9 else 0
    if a2 > 0:
        p = ch.px(2022, PRICE[2022])
        dot(d, p, 10, BLUE)
        text(d, (p[0], p[1] - 20), "Höchststand 2022", 28, BLUE, a2, "mb", "Bold")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        card(d, (1460, 300, 1870, 620), a4)
        text(d, (1490, 350), "2010 → 2025", 28, MUTED, a4, "lm", "SemiBold")
        text(d, (1490, 425), pct(PRICE[2025] - 100, 0, sign=True), 56, BLUE, a4, "lm", "Black")
        text(d, (1490, 475), "Kaufpreise", 26, FG, a4, "lm", "Medium")
        text(d, (1490, 545), pct(RENT[2025] - 100, 0, sign=True), 56, GREEN, a4, "lm", "Black")
        text(d, (1490, 595), "Mieten", 26, FG, a4, "lm", "Medium")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        card(d, (1460, 660, 1870, 860), a5, AMBER)
        text(d, (1490, 710), "Faktor", 28, MUTED, a5, "lm", "SemiBold")
        text(d, (1490, 780), f"{dec(KPM[2010], 0)} → {dec(KPM[2022])} → {dec(KPM[2025])}", 40, AMBER, a5, "lm",
             "Black")
        text(d, (1490, 830), "2010 · 2022 · 2025", 24, MUTED, a5, "lm", "Medium")


def draw_zins(img, d, t, S):
    title(d, t, "Mietrendite vs. Bauzins", S.c(0), "Was die Wohnung an Miete „bringt“ vs. was der Kredit kostet")
    ch = Chart((260, 260, 1400, 870), (2010, 2026.9), (0, 5.5))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, range(2010, 2027, 2), range(0, 6), YFMT, lambda v: f"{v} %")
    legend(d, [("Mietrendite (1 ÷ Faktor)", AMBER), ("Bauzins 5–10 J. (Jahresschnitt)", RED)], 225, ax)
    footer(d, ax, SRC + " · MFI-Zinsstatistik SUD118")
    up = piecewise(t, [(S.c(1), 2010), (S.e(2), 2021), (S.c(3), 2021), (S.e(3), 2025)]) if t > S.c(1) else 2010
    ys = np.array([YIELD[y] for y in YEARS])
    zs = np.array([BAUZ[y] for y in YEARS])
    if up > 2010:
        ch.band(d, XS, ys, np.minimum(ys, zs), fade(GREEN, 0.25), up)
        ch.line(d, XS, ys, AMBER, 6, up)
        ch.line(d, XS, zs, RED, 6, up)
    a2 = prog(t, S.c(2), 0.5) if up >= 2020 else 0
    if a2 > 0:
        pa, pb = ch.px(2020, YIELD[2020]), ch.px(2020, BAUZ[2020])
        dot(d, pa, 9, AMBER)
        dot(d, pb, 9, RED)
        text(d, (pa[0], pa[1] - 18), pct(YIELD[2020]), 28, AMBER, a2, "mb", "Black")
        text(d, (pb[0], pb[1] + 18), pct(BAUZ[2020]), 28, RED, a2, "mt", "Black")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        p = ch.px(2026.7, BAUZ_NOW)
        dot(d, p, 10, RED)
        text(d, (p[0] - 14, p[1] - 16), f"Sept. 2026: {pct(BAUZ_NOW, 2)}", 26, RED, a4, "rb", "Bold")
        card(d, (1460, 330, 1870, 600), a4, AMBER)
        text(d, (1490, 385), "heute", 28, MUTED, a4, "lm", "SemiBold")
        text(d, (1490, 450), f"{pct(YIELD[2025], 2)} vs.", 40, AMBER, a4, "lm", "Black")
        text(d, (1490, 510), pct(BAUZ_NOW, 2), 40, RED, a4, "lm", "Black")
        text(d, (1490, 560), "fast gleichauf", 26, FG, a4, "lm", "Medium")


def draw_beispiel(img, d, t, S):
    title(d, t, f"Beispiel: Wohnung mit {eur(RENT_M)} Kaltmiete", S.c(0), "Modellrechnung mit Durchschnittswerten und Annahmen")
    rows = [(S.c(1), "Kaufpreis", f"{dec(F)} × 12.000 €", eur(PRICE_W), FG),
            (S.c(2), "Kaufnebenkosten (Annahme 10 %)", "Grunderwerbsteuer, Notar, Grundbuch, ggf. Makler", eur(NK), RED),
            (S.c(3), "Eigenkapital", "20 % des Kaufpreises + Nebenkosten", eur(EK), VIOLET),
            (S.c(3) + 1.5, "Kredit", f"{pct(BAUZ_NOW, 2)} Zins, 2 % Tilgung", eur(LOAN), BLUE)]
    for i, (start, lab, sub, val, col) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 250 + i * 150
        card(d, (250, y, 1670, y + 130), a, col)
        text(d, (290, y + 48), lab, 38, FG, a, "lm", "Bold")
        text(d, (290, y + 98), sub, 26, MUTED, a, "lm", "Medium")
        text(d, (1630, y + 68), val, 52, col, a, "rm", "Black")
    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        text(d, (250, 900), f"Monatlich: {eur(RATE)} Kreditrate + {eur(INST_M)} Rücklage (1 % p. a.) = {eur(OUT)}",
             38, AMBER, a4, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Modellrechnung · Faktor 2025 Deutschland · Bauzins SUD118 Sept. 2026")


def draw_monat(img, d, t, S):
    title(d, t, "Was ist wirklich weg?", S.c(0), "Erster Monat: Kosten, die nicht zurückkommen")
    base, scale = 860, 0.42
    # Miete
    a1 = prog(t, S.c(1), 0.5)
    if a1 > 0:
        h = RENT_M * scale * prog(t, S.c(1), 0.9, ease_in_out)
        rrect(d, (380, base - h, 680, base), 12, fill=fade(GREEN, a1))
        text(d, (530, base - h - 20), eur(RENT_M), 46, FG, a1, "mb", "Black")
        text(d, (530, base + 24), "Mieten", 34, FG, a1, "mt", "Bold")
        text(d, (530, base + 66), "Kaltmiete", 26, MUTED, a1, "mt", "Medium")
    parts = [("Zinsen", INT_M1, RED, S.c(2)), ("Rücklage", INST_M, AMBER, S.c(3)),
             ("entgangene Zinsen aufs Eigenkapital", OPP_M1, VIOLET, S.c(4))]
    top = base
    for lab, v, col, start in parts:
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        h = v * scale * prog(t, start, 0.8, ease_in_out)
        rrect(d, (900, top - h, 1200, top), 8, fill=fade(col, a))
        text(d, (1230, top - h / 2), f"{lab}: {eur(v)}", 28, col, a, "lm", "Bold")
        top -= h
    a5 = prog(t, S.c(4) + 1.0, 0.5)
    if a5 > 0:
        text(d, (1050, top - 20), "≈ " + eur(LOST_M1), 46, FG, a5, "mb", "Black")
        text(d, (1050, base + 24), "Kaufen", 34, FG, a5, "mt", "Bold")
        text(d, (1050, base + 66), "ohne Tilgung", 26, MUTED, a5, "mt", "Medium")
    a6 = prog(t, S.c(5), 0.5)
    if a6 > 0:
        card(d, (1300, 860, 1860, 1000), a6, BLUE)
        text(d, (1330, 905), f"Tilgung {eur(TILG_M1)}", 36, BLUE, a6, "lm", "Black")
        text(d, (1330, 962), "ist kein Verlust – das ist Vermögen", 28, FG, a6, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), f"Annahmen: Rücklage 1 % des Kaufpreises p. a., Eigenkapital sonst zu {pct(100 * R_SAVE)} angelegt")


def draw_zehn(img, d, t, S):
    title(d, t, "Vermögen nach 10 Jahren", S.c(0), "Gleiche monatliche Ausgaben, Mieter legt Eigenkapital und Differenz an")
    base, scale = 860, 0.0024
    a1 = prog(t, S.c(2), 0.5)
    bars = [("Mieter", RENTER, GREEN, S.c(2), "")]
    bars += [(f"Käufer {pct(100 * g, 0)}", v, BLUE if v > RENTER else RED, S.c(3) + i * 0.5, "Wertsteigerung p. a.")
             for i, (g, v) in enumerate(CASES)]
    for i, (lab, v, col, start, sub) in enumerate(bars):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        x = 260 + i * 260
        h = v * scale * prog(t, start, 0.9, ease_in_out)
        rrect(d, (x, base - h, x + 210, base), 12, fill=fade(col, a))
        text(d, (x + 105, base - h - 16), "≈ " + eur(round(v, -2)), 30, FG, a, "mb", "Black")
        text(d, (x + 105, base + 22), lab, 30, FG, a, "mt", "Bold")
        if sub:
            text(d, (x + 105, base + 60), sub, 20, MUTED, a, "mt", "Medium")
    a1 = prog(t, S.c(2), 0.5)
    if a1 > 0:
        _, py = 0, base - RENTER * scale
        x = 260
        while x < 1510:
            d.line((x, py, min(x + 14, 1510), py), fill=fade(GREEN, a1 * 0.8), width=3)
            x += 26
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        rrect(d, (1580, 400, 1870, 610), 18, fill=fade((44, 38, 20), a5), outline=fade(AMBER, a5 * 0.6), width=2)
        text(d, (1725, 450), "Gleichstand bei", 28, FG, a5, "mm", "SemiBold")
        text(d, (1725, 525), "≈ " + pct(100 * BE), 60, AMBER, a5, "mm", "Black")
        text(d, (1725, 580), "pro Jahr", 28, FG, a5, "mm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5),
           f"Annahmen: Miete +{pct(100 * RENT_UP, 0)} p. a., Anlage {pct(100 * R_SAVE)} vor Steuern, ohne Verkaufskosten")


def draw_einordnung(img, d, t, S):
    title(d, t, "Und wie viel Wertsteigerung ist realistisch?", S.c(0))
    items = [(S.c(1), "2015 → 2025", f"{pct(100 * P_15_25)} pro Jahr", BLUE),
             (S.c(2), "2022 → 2025", pct(100 * P_22_25, sign=True) + " insgesamt", RED),
             (S.c(3), "Gleichstand in der Rechnung", "≈ " + pct(100 * BE) + " pro Jahr", AMBER)]
    for i, (start, lab, val, col) in enumerate(items):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 250 + i * 190
        card(d, (250, y, 1670, y + 160), a, col)
        text(d, (300, y + 80), lab, 40, FG, a, "lm", "Bold")
        text(d, (1620, y + 80), val, 56, col, a, "rm", "Black")
    a4 = prog(t, S.c(4), 0.5)
    text(d, (W / 2, 880), "Vergangene Preise sagen nichts Sicheres über die Zukunft.", 40, FG, a4, "mm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · Preisindex Eigentumswohnungen, Deutschland")


def draw_grenzen(img, d, t, S):
    title(d, t, "4 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Ort entscheidet", f"In den 7 Großstädten liegt der Faktor bei {dec(KPM7[2025])}, nicht {dec(F)}."),
             (S.c(2), "2", "Annahmen", "Nebenkosten, Rücklage, Anlagezins, Mietsteigerung – alles verschiebbar."),
             (S.c(3), "3", "Vereinfacht", "Ohne Steuern auf Zinsen, Verkaufskosten und Zinsänderung nach 10 Jahren."),
             (S.c(4), "4", "Nicht nur Geld", "Sicherheit, Freiheit beim Umbau – oder Flexibilität beim Umzug.")]
    for i, (start, n, head, line) in enumerate(items):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 220 + i * 175
        card(d, (250, y, 1670, y + 155), a)
        dot(d, (320, y + 78), 36, fade(AMBER, a))
        text(d, (320, y + 80), n, 38, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + 50), head, 38, FG, a, "lm", "Bold")
        text(d, (400, y + 105), line, 28, MUTED, a, "lm", "Medium")


def draw_fazit(img, d, t, S):
    text_pop(d, (W / 2, 170), "Deine eigene Rechnung in 3 Schritten", t, S.c(0), 56, FG, "mm", "Black")
    rows = [(S.c(1), BLUE, "1. Faktor:", "Kaufpreis ÷ Jahreskaltmiete"),
            (S.c(2), AMBER, "2. Mietrendite vs. Bauzins:", "1 ÷ Faktor gegen deinen Kreditzins"),
            (S.c(3), GREEN, "3. Wertsteigerung:", "Wie viel müsste die Wohnung zulegen?")]
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
        text(d, (W / 2, 875), "Heute: knapper als 2020 – es hängt am Preis vor Ort", 42, AMBER, a, "mm", "Black")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(0), 52, FG,
             "mm", "Bold")
    text_pop(d, (W / 2, 335), "Daten, Annahmen & Formeln stehen in der Beschreibung.", t, S.c(1), 32, MUTED,
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
        text(d, (1060, 580), "Brutto, netto:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Was vom Gehalt bleibt", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "durchgerechnet", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Eine Eigentumswohnung kostet in Deutschland im Schnitt das Sechsundzwanzigfache ihrer Jahresmiete.",
            "Und für den Kredit zahlt man im Schnitt drei Komma neun eins Prozent Zinsen.",
            "Lohnt sich Kaufen da noch? In unserer Rechnung erst dann, wenn die Wohnung um gut eineinhalb Prozent pro Jahr im Wert steigt.",
            "Wir rechnen das mit den Daten der Bundesbank Schritt für Schritt durch. Mit allen Annahmen offen auf dem Tisch.",
        ], draw_hook),
        Scene("faktor", [
            "Die wichtigste Zahl heißt Kaufpreis-Miet-Faktor: Kaufpreis geteilt durch die Jahreskaltmiete.",
            "Für Eigentumswohnungen in ganz Deutschland lag er zweitausendfünfundzwanzig bei sechsundzwanzig Komma eins. Eine Wohnung kostet also so viel wie sechsundzwanzig Jahre Miete.",
            "In hundertsiebenundzwanzig Städten waren es siebenundzwanzig Komma eins, in den sieben größten Städten sogar dreißig Komma sechs.",
            "Umgedreht ergibt sich die Mietrendite: eins geteilt durch sechsundzwanzig Komma eins, also rund drei Komma acht Prozent pro Jahr. Vor allen Kosten. In den Großstädten sind es nur knapp drei Komma drei Prozent.",
        ], draw_faktor),
        Scene("verlauf", [
            "Wie ist es dazu gekommen?",
            "Seit zweitausendzehn sind die Kaufpreise für Wohnungen deutlich schneller gestiegen als die Mieten.",
            "Ihren Höchststand erreichten die Preise zweitausendzweiundzwanzig.",
            "Seitdem sind sie gut ein Prozent gesunken, während die Mieten um rund dreizehn Prozent zugelegt haben.",
            "Über die ganze Zeit: Kaufpreise plus hundertacht Prozent, Mieten plus sechsundsiebzig Prozent.",
            "Der Faktor stieg deshalb von zwanzig auf dreißig Komma vier im Jahr zweitausendzweiundzwanzig und ist seitdem auf sechsundzwanzig Komma eins gefallen.",
        ], draw_verlauf),
        Scene("zins", [
            "Jetzt der entscheidende Vergleich: Mietrendite gegen Bauzins.",
            "Ist der Bauzins niedriger als die Mietrendite, kostet der Kredit weniger, als die Wohnung an Miete einspart.",
            "Zweitausendzwanzig war das extrem: drei Komma fünf Prozent Mietrendite, aber nur eins Komma eins Prozent Bauzins.",
            "Bis zweitausendzweiundzwanzig lag die Mietrendite jedes Jahr über dem Bauzins. Seit zweitausenddreiundzwanzig liegen beide nah beieinander.",
            "Im September zweitausendsechsundzwanzig lag der Bauzins mit drei Komma neun eins Prozent sogar knapp über der Mietrendite.",
        ], draw_zins),
        Scene("beispiel", [
            "Rechnen wir ein Beispiel. Eine Wohnung, die tausend Euro Kaltmiete im Monat kosten würde.",
            "Beim Faktor sechsundzwanzig Komma eins kostet sie dreihundertdreizehntausendzweihundert Euro.",
            "Dazu kommen Kaufnebenkosten. Wir nehmen zehn Prozent an, also einunddreißigtausenddreihundertzwanzig Euro. Je nach Bundesland liegt allein die Grunderwerbsteuer zwischen drei Komma fünf und sechs Komma fünf Prozent.",
            "Als Eigenkapital rechnen wir zwanzig Prozent des Kaufpreises plus die Nebenkosten: dreiundneunzigtausendneunhundertsechzig Euro. Der Rest ist ein Kredit über zweihundertfünfzigtausendfünfhundertsechzig Euro.",
            "Bei drei Komma neun eins Prozent Zins und zwei Prozent Tilgung sind das zwölfhundertvierunddreißig Euro im Monat. Dazu eine Rücklage für Reparaturen von einem Prozent des Kaufpreises pro Jahr. Macht zusammen rund vierzehnhundertfünfundneunzig Euro.",
        ], draw_beispiel),
        Scene("monat", [
            "Vierzehnhundertfünfundneunzig Euro gegen tausend Euro Miete. Aber das ist nicht der faire Vergleich.",
            "Wer mietet, zahlt tausend Euro, und die sind weg.",
            "Wer kauft, zahlt im ersten Monat rund achthundertsechzehn Euro Zinsen.",
            "Dazu zweihunderteinundsechzig Euro Rücklage für Reparaturen.",
            "Und das Eigenkapital könnte sonst Zinsen bringen. Bei angenommenen zwei Komma fünf Prozent sind das rund hundertsechsundneunzig Euro im Monat. Zusammen rund zwölfhundertdreiundsiebzig Euro, die nicht zurückkommen.",
            "Die Tilgung von rund vierhundertachtzehn Euro zählt nicht dazu. Die baut Vermögen auf.",
        ], draw_monat),
        Scene("zehn", [
            "Und nach zehn Jahren? Dafür vergleichen wir zwei Menschen mit denselben monatlichen Ausgaben.",
            "Der Mieter legt sein Eigenkapital und jeden Monat die Differenz zur Miete zu zwei Komma fünf Prozent an. Die Miete steigt um zwei Prozent pro Jahr.",
            "Nach zehn Jahren hat er rund hundertfünfundsiebzigtausendsiebenhundert Euro.",
            "Der Käufer hat eine Wohnung und noch rund hundertneunundachtzigtausend Euro Schulden. Bleibt der Wert gleich, besitzt er netto rund hundertdreiundzwanzigtausendachthundert Euro. Steigt der Wert um zwei Prozent pro Jahr, sind es rund hundertzweiundneunzigtausendvierhundert.",
            "Damit ist klar, worauf es ankommt.",
            "Gleichstand gibt es bei gut eineinhalb Prozent Wertsteigerung pro Jahr. Darunter liegt der Mieter vorn, darüber der Käufer.",
        ], draw_zehn),
        Scene("einordnung", [
            "Ist das realistisch?",
            "Von zweitausendfünfzehn bis zweitausendfünfundzwanzig sind Wohnungspreise im Schnitt um gut fünf Prozent pro Jahr gestiegen.",
            "Seit dem Höchststand zweitausendzweiundzwanzig sind sie aber leicht gesunken.",
            "Die Schwelle in unserer Rechnung liegt bei gut eineinhalb Prozent pro Jahr.",
            "Ob die Preise in Zukunft so steigen, weiß niemand. Vergangene Preise sind keine Garantie.",
        ], draw_einordnung),
        Scene("grenzen", [
            "Vier ehrliche Einschränkungen.",
            "Erstens: Der Ort entscheidet. In den sieben größten Städten liegt der Faktor bei dreißig Komma sechs, dort sieht die Rechnung schlechter aus.",
            "Zweitens: Die Annahmen. Nebenkosten, Rücklage, Anlagezins und Mietsteigerung verschieben das Ergebnis deutlich.",
            "Drittens: Wir haben vereinfacht. Ohne Steuern auf Zinsen, ohne Verkaufskosten und ohne zu wissen, wie hoch der Bauzins nach zehn Jahren ist.",
            "Viertens: Es geht nicht nur um Geld. Eigentum bringt Sicherheit und Freiheit beim Umbau. Mieten bringt Flexibilität, wenn man umziehen will.",
        ], draw_grenzen),
        Scene("fazit", [
            "Wie rechnest du das für dich?",
            "Erstens: Teile den Kaufpreis durch die Jahreskaltmiete einer vergleichbaren Wohnung.",
            "Zweitens: Vergleiche die Mietrendite, also eins geteilt durch diesen Faktor, mit deinem Kreditzins.",
            "Drittens: Frag dich, wie viel Wertsteigerung nötig wäre, damit Kaufen vorne liegt.",
            "Heute ist die Rechnung deutlich knapper als zweitausendzwanzig. Und sie hängt stark davon ab, wo du kaufen willst.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Daten, Annahmen und Formeln findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Im nächsten Video rechnen wir nach, was vom Brutto wirklich übrig bleibt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
