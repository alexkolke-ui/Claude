"""Video 004: Dispo, Ratenkredit, Baufinanzierung – was Kredite in Deutschland wirklich kosten (Bundesbank-Daten)."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     dot, ease_in_out, eur, fade, lerp, piecewise, prog, rrect, text, text_pop,
                     thick_line)

# ---------------------------------------------------------------- data (Bundesbank, Stand 02.11.2026)
DATA = Path(__file__).parent / "data"


def _bbk(name):
    out = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and len(c[0]) == 7 and c[0][4] == "-" and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


DISPO = _bbk("SUD112_dispo_revolvierend.csv")           # Überziehungs- & revolvierende Kredite, Neugeschäft
KARTE = _bbk("SUD132_kreditkarte.csv")                  # echte Kreditkartenkredite
RATEN = _bbk("SUD130_konsumentenkredit_effjz.csv")      # Konsumentenkredite, eff. Jahreszins inkl. Kosten
BAU = _bbk("SUD131_wohnungsbau_effjz.csv")              # Wohnungsbaukredite, eff. Jahreszins inkl. Kosten
BAU10 = _bbk("SUD118_wohnungsbau_5_10j.csv")            # Wohnungsbaukredite, Zinsbindung 5–10 Jahre
EINLAGE = _bbk("SUD101_zins_taeglich_faellig.csv")      # täglich fällige Einlagen
EZB = _bbk("SU0200_ezb_einlagefazilitaet.csv")          # EZB-Einlagesatz, Monatsende

LAST = "2026-09"
MONTHS = [m for m in sorted(DISPO) if "2015-01" <= m <= LAST]


def mx(m):
    return int(m[:4]) + (int(m[5:]) - 0.5) / 12


MX = np.array([mx(m) for m in MONTHS])

# ---------------------------------------------------------------- derived numbers
D_NOW, K_NOW, R_NOW, B_NOW, B10_NOW = DISPO[LAST], KARTE[LAST], RATEN[LAST], BAU[LAST], BAU10[LAST]
E_NOW, EZB_NOW = EINLAGE[LAST], EZB[LAST]
LADDER = [("Tagesgeld & Giro (Ø)", E_NOW, GREEN), ("EZB-Einlagesatz", EZB_NOW, VIOLET),
          ("Baukredit", B_NOW, BLUE), ("Ratenkredit", R_NOW, AMBER),
          ("Dispo", D_NOW, RED), ("Kreditkarte", K_NOW, RED)]
SPREAD_21 = [DISPO[m] - EZB[m] for m in MONTHS if m >= "2021-01"]

DISPO_AMT = 2000
DISPO_COST = DISPO_AMT * D_NOW / 100
DEPO_GAIN = DISPO_AMT * E_NOW / 100

LOAN = 10000
R_M = (1 + R_NOW / 100) ** (1 / 12) - 1                 # Monatszins aus effektivem Jahreszins


def annuity(n):
    rate = LOAN * R_M / (1 - (1 + R_M) ** -n)
    return rate, rate * n - LOAN


RATEN_CASES = [(n, *annuity(n)) for n in (36, 60, 84)]

HOUSE, TILG = 300000, 0.02
B10_LOW_M = min((m for m in BAU10 if "2015-01" <= m <= LAST), key=lambda m: BAU10[m])
B10_LOW = BAU10[B10_LOW_M]


def baufi(z, years=10):
    """Annuitätendarlehen: Rate = Darlehen × (Zins + Tilgung) ÷ 12, Monatszins = Zins ÷ 12."""
    rate = HOUSE * (z / 100 + TILG) / 12
    debt, paid = HOUSE, 0.0
    for _ in range(years * 12):
        i = debt * z / 100 / 12
        paid += i
        debt -= rate - i
    return rate, debt, paid


BAU_NOW = baufi(B10_NOW)
BAU_LOW = baufi(B10_LOW)

# Every number spoken in the narration is checked here.
assert E_NOW == 0.52 and D_NOW == 9.59 and K_NOW == 17.56       # Hook
assert EZB_NOW == 2.5 and B_NOW == 4.13 and R_NOW == 8.91          # Zinsleiter
assert sorted(v for _, v, _ in LADDER) == [v for _, v, _ in LADDER]
assert min(DISPO[m] for m in MONTHS if m.startswith("2021")) == 6.9 == DISPO["2021-07"]  # "knapp sieben"
assert EZB["2021-07"] == -0.5
assert BAU["2020-12"] == 1.21 == min(BAU[m] for m in MONTHS)    # "rund eins Komma zwei"
assert max(BAU[m] for m in MONTHS) == 4.27 and max(DISPO[m] for m in MONTHS) == 11.23  # "über vier", "über elf"
assert DISPO["2024-05"] == 11.23
assert 6.5 < min(SPREAD_21) and max(SPREAD_21) < 7.8              # "sechseinhalb bis knapp acht Punkte"
assert DISPO_COST == 191.8 and round(DEPO_GAIN, 2) == 10.4         # "hunderteinundneunzig Euro achtzig", "zehn Euro vierzig"
assert 18 < D_NOW / E_NOW < 19                                    # "mehr als achtzehnmal"
(n1, r1, z1), (n2, r2, z2), (n3, r3, z3) = RATEN_CASES
assert round(r1) == 316 and round(r2) == 205 and round(r3) == 159  # Monatsraten
assert 1370 < z1 < 1380 and 2325 < z2 < 2335 and 3325 < z3 < 3335  # "rund 1.375 / 2.330 / 3.330"
assert z3 / z1 > 2.4                                              # "fast zweieinhalbmal so viel"
assert B10_NOW == 3.91 and B10_LOW == 1.02 and B10_LOW_M == "2020-12"
assert BAU_NOW[0] == 1477.5 and BAU_LOW[0] == 755.0                # Monatsraten
assert 720 < BAU_NOW[0] - BAU_LOW[0] < 725                         # "gut siebenhundertzwanzig Euro"
assert 103500 < BAU_NOW[2] < 104500 and 27000 < BAU_LOW[2] < 28000  # "rund 104.000", "rund 27.500"
assert 226000 < BAU_NOW[1] < 227500                               # "knapp 227.000 Restschuld"

SRC = "Quelle: Deutsche Bundesbank, MFI-Zinsstatistik · Neugeschäft, private Haushalte"


def pct(v, dec=2, sign=False):
    s = f"{v:+.{dec}f}" if sign else f"{v:.{dec}f}"
    return s.replace("-", "−").replace(".", ",") + " %"


def dec(v, d=2):
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


YT = range(2015, 2027)
YFMT = lambda y: f"’{y % 100:02}"


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 170), "Was deine Bank zahlt – und was sie verlangt", t, S.c(0), 52, FG, "mm", "Black")
    items = [((200, 300, 720, 640), "Sie zahlt dir", "Tagesgeld & Giro, Ø", E_NOW, GREEN, S.c(0) + 0.6),
             ((780, 300, 1300, 640), "Sie verlangt", "Dispo, Ø", D_NOW, RED, S.c(1)),
             ((1360, 300, 1720, 640), "", "Kreditkarte, Ø", K_NOW, RED, S.c(2))]
    for box, head, label, val, col, start in items:
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        card(d, box, a, col)
        cx = (box[0] + box[2]) / 2
        if head:
            text(d, (cx, box[1] + 70), head, 36, FG, a, "mm", "Bold")
        text(d, (cx, box[1] + 125), label, 28, MUTED, a, "mm", "Medium")
        p = prog(t, start + 0.2, 1.2, ease_in_out)
        size = 96 if box[2] - box[0] > 400 else 72
        text(d, (cx, box[1] + 240), pct(val * p), size, col, a, "mm", "Black")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 720, 1560, 830), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 775), "Dispo, Ratenkredit, Baufinanzierung – durchgerechnet", 40, AMBER, a, "mm", "Bold")
    footer(d, prog(t, S.c(1), 0.6), SRC + " · Sept. 2026 (vorläufig)")


def draw_leiter(img, d, t, S):
    title(d, t, "Die Zinsleiter", S.c(0), "Durchschnittszinsen im Neugeschäft, September 2026")
    x0, x1, y0 = 640, 1700, 260
    scale = (x1 - x0) / 18
    for i, (name, val, col) in enumerate(LADDER):
        start = S.c(1) + i * 0.5 if i < 2 else S.c(2 + (i - 2) // 2) + (i % 2) * 0.6
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = y0 + i * 110
        text(d, (x0 - 30, y + 35), name, 34, FG, a, "rm", "SemiBold")
        w = max(4, val * scale * prog(t, start, 0.9, ease_in_out))
        rrect(d, (x0, y + 8, x0 + w, y + 62), 12, fill=fade(col, a))
        text(d, (x0 + w + 18, y + 35), pct(val), 38, col, a, "lm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        rrect(d, (250, 940, 1670, 1000), 16, fill=fade((30, 42, 66), a))
        text(d, (960, 970), "Je flexibler und je weniger Sicherheit, desto teurer", 32, AMBER, a, "mm", "Bold")
    footer(d, prog(t, S.c(1), 0.5),
           "Bundesbank SUD101, SU0200, SUD131, SUD130 (eff. Jahreszins inkl. Kosten), SUD112, SUD132")


def draw_effzins(img, d, t, S):
    title(d, t, "Effektiver Jahreszins", S.c(0), "Die Zahl, die man vergleichen kann")
    parts = [(S.c(1), "Sollzins", "der vereinbarte Zins", BLUE),
             (S.c(2), "+ Kosten", "z. B. Bearbeitungs- oder Kontoführungsgebühren für den Kredit", AMBER),
             (S.c(3), "= effektiver Jahreszins", "auf ein Jahr umgerechnet", GREEN)]
    for i, (start, head, sub, col) in enumerate(parts):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 190
        card(d, (250, y, 1670, y + 160), a, col)
        text(d, (300, y + 60), head, 48, col, a, "lm", "Black")
        text(d, (300, y + 118), sub, 30, MUTED, a, "lm", "Medium")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        text(d, (250, 880), f"Ratenkredite, Ø September 2026:  {pct(R_NOW)} effektiv", 40, FG, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Preisangabenverordnung (PAngV) · Bundesbank SUD130")


def draw_verlauf(img, d, t, S):
    title(d, t, "Kreditzinsen seit 2015", S.c(0), "Monatswerte, Januar 2015 bis September 2026")
    ch = Chart((260, 260, 1400, 870), (2015, 2026.9), (-2, 12))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, YT, range(0, 13, 2), YFMT, lambda v: f"{v} %")
    legend(d, [("Dispo", RED), ("Ratenkredit", AMBER), ("Baukredit", BLUE), ("EZB-Einlagesatz", VIOLET)], 225, ax)
    footer(d, ax, "Quelle: Deutsche Bundesbank · SUD112, SUD130, SUD131, SU0200")
    if ax > 0:
        _, py = ch.px(0, 0)
        d.line((ch.x0, py, ch.x1, py), fill=fade((90, 102, 128), ax), width=2)
    up = piecewise(t, [(S.c(1), 2015), (S.e(2), 2021.6), (S.c(3), 2021.6), (S.e(4), 2026.9)]) \
        if t > S.c(1) else 2015
    if up > 2015:
        for series, col in ((EZB, VIOLET), (BAU, BLUE), (RATEN, AMBER), (DISPO, RED)):
            ch.line(d, MX, np.array([series[m] for m in MONTHS]), col, 5, min(up, MX[-1]))
    a2 = prog(t, S.c(2) + 0.6, 0.5) if up >= 2021.55 else 0
    if a2 > 0:
        pd = ch.px(mx("2021-07"), DISPO["2021-07"])
        dot(d, pd, 9, RED)
        text(d, (pd[0], pd[1] - 20), pct(DISPO["2021-07"]), 28, RED, a2, "mb", "Black")
        pe = ch.px(mx("2021-07"), EZB["2021-07"])
        dot(d, pe, 9, VIOLET)
        text(d, (pe[0], pe[1] + 18), pct(EZB["2021-07"], 1), 28, VIOLET, a2, "mt", "Black")
        pb = ch.px(mx("2020-12"), BAU["2020-12"])
        dot(d, pb, 9, BLUE)
        text(d, (pb[0] - 14, pb[1] - 14), pct(BAU["2020-12"]), 26, BLUE, a2, "rb", "Black")
    a5 = prog(t, S.c(5), 0.5)
    if a5 > 0:
        card(d, (1460, 300, 1870, 600), a5, RED)
        text(d, (1490, 355), "Dispo minus EZB-Satz", 28, MUTED, a5, "lm", "SemiBold")
        text(d, (1490, 435), "6,5 – 7,8", 60, RED, a5, "lm", "Black")
        text(d, (1490, 505), "Prozentpunkte", 28, FG, a5, "lm", "Medium")
        text(d, (1490, 550), "seit 2021, jeden Monat", 24, MUTED, a5, "lm", "Medium")


def draw_dispo(img, d, t, S):
    title(d, t, "Beispiel Dispo: 2.000 € ein Jahr lang", S.c(0), "Durchschnittszinsen September 2026, vereinfacht ohne Zinseszins")
    rows = [(S.c(1), "2.000 € im Dispo", f"× {pct(D_NOW)}", "−" + eur(DISPO_COST, 2), RED),
            (S.c(2), "2.000 € auf Tagesgeld/Giro", f"× {pct(E_NOW)}", "+" + eur(DEPO_GAIN, 2), GREEN)]
    for i, (start, lab, f, val, col) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 230
        card(d, (250, y, 1670, y + 190), a, col)
        text(d, (300, y + 70), lab, 44, FG, a, "lm", "Bold")
        text(d, (300, y + 135), f, 34, MUTED, a, "lm", "SemiBold")
        text(d, (1620, y + 100), val, 80, col, a, "rm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        text(d, (W / 2, 830), f"Der Dispo kostet {dec(D_NOW / E_NOW, 0)}-mal so viel Zins,", 46, FG, a, "mm", "Bold")
        text(d, (W / 2, 895), "wie dasselbe Geld auf dem Konto bringt.", 46, AMBER, a, "mm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Modellrechnung: Betrag × Durchschnittszins · Bundesbank SUD112, SUD101")


def draw_raten(img, d, t, S):
    title(d, t, f"Ratenkredit: {eur(LOAN)} zu {pct(R_NOW)} effektiv", S.c(0),
          "Gleiche Summe, unterschiedliche Laufzeit")
    cols = [GREEN, AMBER, RED]
    starts = [S.c(1), S.c(2), S.c(3)]
    for i, ((n, rate, zins), col, start) in enumerate(zip(RATEN_CASES, cols, starts)):
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 540
        dy = (1 - a) * 30
        card(d, (x0, 270 + dy, x0 + 500, 760 + dy), a, col)
        cx = x0 + 250
        text(d, (cx, 335 + dy), f"{n} Monate", 44, FG, a, "mm", "Black")
        text(d, (cx, 380 + dy), f"= {n // 12} Jahre", 26, MUTED, a, "mm", "Medium")
        text(d, (cx, 460 + dy), "Monatsrate", 28, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 520 + dy), eur(rate), 60, FG, a, "mm", "Black")
        d.line((x0 + 50, 580 + dy, x0 + 450, 580 + dy), fill=fade((70, 82, 108), a), width=2)
        text(d, (cx, 630 + dy), "Zinsen gesamt", 28, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 690 + dy), eur(zins), 60, col, a, "mm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        text(d, (W / 2, 860), "Kleinere Rate = mehr als doppelt so viel Zinsen", 46, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5),
           "Modellrechnung: Annuität, Monatszins = (1 + eff. Jahreszins)^(1/12) − 1 · Bundesbank SUD130")


def draw_bau(img, d, t, S):
    title(d, t, f"Baufinanzierung: {eur(HOUSE)}", S.c(0),
          "Zinsbindung 5–10 Jahre, 2 % anfängliche Tilgung, Durchschnittszinsen")
    cases = [(S.c(1), "September 2026", B10_NOW, BAU_NOW, RED),
             (S.c(4), "Dezember 2020", B10_LOW, BAU_LOW, GREEN)]
    for i, (start, lab, z, (rate, debt, paid), col) in enumerate(cases):
        a = prog(t, start, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 260, x0 + 660, 800), a, col)
        text(d, (x0 + 40, 320), lab, 34, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 620, 320), pct(z), 48, col, a, "rm", "Black")
        rows = [("Monatsrate", eur(rate, 2), start + 0.3 if i else S.c(1) + 0.5),
                ("Zinsen in 10 Jahren", eur(round(paid, -2)), start + 1.0 if i else S.c(2))]
        if not i:
            rows.append(("Restschuld nach 10 Jahren", eur(round(debt, -2)), S.c(3)))
        for j, (rl, rv, st) in enumerate(rows):
            b = prog(t, st, 0.5) * a
            y = 430 + j * 125
            text(d, (x0 + 40, y), rl, 32, MUTED, b, "lm", "SemiBold")
            text(d, (x0 + 620, y + 50), rv, 54, FG, b, "rm", "Black")
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        text(d, (W / 2, 880), f"+{eur(BAU_NOW[0] - BAU_LOW[0])} pro Monat – nur durch den Zins", 46, AMBER, a,
             "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5),
           "Modellrechnung: Rate = Darlehen × (Zins + 2 %) ÷ 12 · Bundesbank SUD118 · ohne Kaufnebenkosten")


def draw_grenzen(img, d, t, S):
    title(d, t, "3 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Durchschnitte", "Dein Zins hängt von Bonität, Bank und Sicherheiten ab."),
             (S.c(2), "2", "Dispo-Wert inkl. Rahmenkredite",
              "Die Bundesbank zählt revolvierende Kredite mit – einzelne Dispos sind oft teurer."),
             (S.c(3), "3", "Vereinfachte Modelle",
              "Ohne Nebenkosten & Sondertilgung · Sept.-2026-Werte vorläufig.")]
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
    text_pop(d, (W / 2, 170), "Was Kredite wirklich kosten", t, S.c(0), 58, FG, "mm", "Black")
    rows = [(S.c(1), RED, "Dispo & Kreditkarte:", "die teuersten Kredite – rund 10 bis 18 %"),
            (S.c(2), AMBER, "Ratenkredit:", "längere Laufzeit = deutlich mehr Zinsen"),
            (S.c(3), BLUE, "Baukredit:", "günstigster Zins – aber riesige Summen")]
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
        text(d, (W / 2, 875), "Vergleichen: effektiver Jahreszins & Gesamtkosten", 44, AMBER, a, "mm", "Black")


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
        text(d, (1060, 580), "Mieten oder kaufen?", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Die Rechnung", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "mit echten Zahlen", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Auf täglich verfügbares Geld zahlen Banken in Deutschland im Schnitt null Komma fünf zwei Prozent Zinsen.",
            "Für den Dispo verlangen sie im Schnitt neun Komma fünf neun Prozent.",
            "Und bei der Kreditkarte sind es sogar siebzehn Komma fünf sechs Prozent.",
            "Wir rechnen nach, was Kredite in Deutschland wirklich kosten. Vom Dispo über den Ratenkredit bis zur Baufinanzierung. Mit den Zahlen der Bundesbank.",
        ], draw_hook),
        Scene("leiter", [
            "So sieht die Zinsleiter im September zweitausendsechsundzwanzig aus.",
            "Ganz unten: null Komma fünf zwei Prozent auf Tagesgeld und Girokonto. Darüber der Einlagesatz der EZB mit zwei Komma fünf Prozent.",
            "Baukredite kosten im Schnitt vier Komma eins drei Prozent, Ratenkredite acht Komma neun eins.",
            "Dann der Dispo mit neun Komma fünf neun und ganz oben die Kreditkarte mit siebzehn Komma fünf sechs Prozent.",
            "Das Muster: Je flexibler der Kredit und je weniger Sicherheit die Bank hat, desto teurer wird er. Beim Baukredit haftet die Immobilie, beim Dispo nur dein Versprechen.",
        ], draw_leiter),
        Scene("effzins", [
            "Kurz zu einem Begriff, der bei Krediten zählt: dem effektiven Jahreszins.",
            "Der Sollzins ist der Zins, der im Vertrag steht.",
            "Dazu können Kosten kommen, zum Beispiel Bearbeitungsgebühren oder Gebühren für ein Konto, das für den Kredit nötig ist.",
            "Der effektive Jahreszins rechnet das alles auf ein Jahr um. Banken müssen ihn bei Verbraucherkrediten angeben, und deshalb kann man damit vergleichen.",
            "Bei Ratenkrediten lag er im September im Schnitt bei acht Komma neun eins Prozent.",
        ], draw_effzins),
        Scene("verlauf", [
            "Wie haben sich diese Zinsen entwickelt?",
            "Von zweitausendfünfzehn bis zweitausendeinundzwanzig fielen fast alle Kreditzinsen. Baukredite kosteten Ende zweitausendzwanzig im Schnitt nur rund eins Komma zwei Prozent.",
            "Der Dispo blieb trotzdem teuer. Mitte zweitausendeinundzwanzig lag er bei knapp sieben Prozent, obwohl der EZB-Satz bei minus null Komma fünf Prozent lag.",
            "Dann stiegen die Leitzinsen.",
            "Baukredite kosteten Ende zweitausenddreiundzwanzig über vier Prozent, der Dispo kletterte bis Mai zweitausendvierundzwanzig auf über elf Prozent.",
            "Auffällig: Seit zweitausendeinundzwanzig lag der Dispo jeden Monat sechseinhalb bis knapp acht Prozentpunkte über dem EZB-Satz. Sinkt der Leitzins, sinkt der Dispo, aber er bleibt teuer.",
        ], draw_verlauf),
        Scene("dispo", [
            "Was heißt das konkret? Nehmen wir zweitausend Euro, ein Jahr lang.",
            "Im Dispo kosten sie beim Durchschnittszins rund hunderteinundneunzig Euro achtzig.",
            "Liegen dieselben zweitausend Euro auf dem Konto, bringen sie beim Durchschnittszins zehn Euro vierzig.",
            "Der Dispo kostet also mehr als achtzehnmal so viel Zins, wie dasselbe Geld auf dem Konto bringt.",
        ], draw_dispo),
        Scene("raten", [
            "Jetzt ein Ratenkredit: zehntausend Euro zum durchschnittlichen effektiven Jahreszins von acht Komma neun eins Prozent.",
            "Über drei Jahre zahlst du rund dreihundertsechzehn Euro im Monat, und insgesamt rund tausenddreihundertfünfundsiebzig Euro Zinsen.",
            "Über fünf Jahre sinkt die Rate auf rund zweihundertfünf Euro. Die Zinsen steigen aber auf rund zweitausenddreihundertdreißig Euro.",
            "Und über sieben Jahre: rund hundertneunundfünfzig Euro im Monat, aber rund dreitausenddreihundertdreißig Euro Zinsen.",
            "Die kleinere Rate kostet also fast zweieinhalbmal so viel Zinsen. Hier sogar mit demselben Zinssatz gerechnet, in der Praxis unterscheidet er sich je nach Laufzeit.",
        ], draw_raten),
        Scene("bau", [
            "Und die größte Summe: eine Baufinanzierung über dreihunderttausend Euro, mit zehn Jahren Zinsbindung und zwei Prozent anfänglicher Tilgung.",
            "Zum Durchschnittszins von drei Komma neun eins Prozent zahlst du eintausendvierhundertsiebenundsiebzig Euro fünfzig im Monat.",
            "In zehn Jahren sind das rund hundertviertausend Euro nur an Zinsen.",
            "Und danach sind immer noch knapp zweihundertsiebenundzwanzigtausend Euro offen.",
            "Zum Vergleich: Im Dezember zweitausendzwanzig lag derselbe Zins bei eins Komma null zwei Prozent. Die Rate wäre siebenhundertfünfundfünfzig Euro gewesen, die Zinsen in zehn Jahren rund siebenundzwanzigtausendfünfhundert Euro.",
            "Gut siebenhundertzwanzig Euro mehr im Monat, nur durch den Zins.",
        ], draw_bau),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Das sind Durchschnitte. Welchen Zins du bekommst, hängt von deiner Bonität, der Bank und den Sicherheiten ab.",
            "Zweitens: Die Bundesbank zählt beim Dispo auch andere Rahmenkredite mit. Einzelne Dispozinsen liegen oft höher als dieser Schnitt.",
            "Drittens: Die Beispiele sind vereinfacht, ohne Nebenkosten und ohne Sondertilgungen. Und die Werte für September zweitausendsechsundzwanzig sind noch vorläufig.",
        ], draw_grenzen),
        Scene("fazit", [
            "Was kosten Kredite also wirklich?",
            "Dispo und Kreditkarte sind die teuersten Kredite: rund zehn bis achtzehn Prozent im Schnitt.",
            "Beim Ratenkredit macht die Laufzeit einen großen Unterschied: Je länger, desto mehr Zinsen insgesamt.",
            "Der Baukredit hat den niedrigsten Zins, aber bei diesen Summen geht es trotzdem um sechsstellige Beträge.",
            "Zum Vergleichen taugen zwei Zahlen: der effektive Jahreszins und die Gesamtkosten.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Daten, Quellen und Formeln findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Im nächsten Video geht es um die große Frage: Mieten oder kaufen? Wir rechnen es mit echten Zahlen durch.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
