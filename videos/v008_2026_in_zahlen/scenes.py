"""Video 008: 2026 in Zahlen – Jahresrückblick Inflation, Zinsen, Immobilien (Bundesbank-Daten, Stand 25.11.2026)."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card, dot, ease_in_out, eur,
                     fade, lerp, prog, rrect, text, text_pop, thick_line)

DATA = Path(__file__).parent / "data"


def _bbk(name):
    out = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and c[0][:4].isdigit() and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


INF = _bbk("vpi_vorjahr.csv")
VPI = _bbk("vpi_index.csv")
EZB = _bbk("ezb_einlagesatz.csv")
TG = _bbk("SUD101_tagesgeld_giro.csv")
DISPO = _bbk("SUD112_dispo.csv")
BAU = _bbk("SUD118_bauzins_5_10j.csv")
VDP = _bbk("vdp_wohneigentum_q.csv")
HPI = _bbk("destatis_haeuserpreise_q.csv")

M26 = [f"2026-{m:02}" for m in range(1, 11)]                     # Januar bis Oktober 2026
M2526 = [f"2025-{m:02}" for m in range(1, 13)] + M26
INF_AVG = sum(INF[m] for m in M26) / len(M26)
INF_MAX_M = max(M26, key=lambda m: INF[m])
VDP_YOY = VDP["2026-Q3"] / VDP["2025-Q3"] - 1
HPI_YOY = HPI["2026-Q2"] / HPI["2025-Q2"] - 1
RATE = lambda z: 300000 * (z / 100 + 0.02) / 12                   # Baukredit-Beispiel aus Video 004
REAL_TG = (1 + TG["2026-09"] / 100) / (1 + INF["2026-09"] / 100) - 1

# Every number spoken in the narration is checked here.
assert 2.6 < INF_AVG < 2.65 and INF_MAX_M == "2026-09" and INF["2026-09"] == 3.3   # "rund 2,6 %", "3,3 im September"
assert INF["2026-10"] == 2.8 and INF["2026-02"] == 1.9                            # "2,8 im Oktober", Tief 1,9
assert min(INF[m] for m in M26) == 1.9
assert EZB["2026-05"] == 2.0 and EZB["2026-06"] == 2.25 and EZB["2026-09"] == 2.5  # Zinsschritte
assert max(EZB[m] for m in EZB if "2023-10" <= m <= "2026-05") == 4.0
assert all(EZB[a] >= EZB[b] for a, b in zip(sorted(m for m in EZB if "2023-09" <= m <= "2026-05")[:-1],
                                             sorted(m for m in EZB if "2023-09" <= m <= "2026-05")[1:]))  # bis Mai 2026 nur Senkungen
assert TG["2026-01"] == 0.43 and TG["2026-09"] == 0.52
assert -2.75 < 100 * REAL_TG < -2.65                                               # "minus 2,7 %"
assert DISPO["2026-01"] == 9.30 and DISPO["2026-09"] == 9.59
assert BAU["2026-01"] == 3.58 and BAU["2026-09"] == 3.91
assert round(RATE(3.58), 2) == 1395.0 and round(RATE(3.91) - RATE(3.58), 2) == 82.5  # "+82,50 €"
assert max(VDP, key=VDP.get) == "2022-Q3" and min(VDP[q] for q in VDP if q >= "2022") == VDP["2024-Q1"]
assert VDP["2026-Q3"] < VDP["2022-Q3"]
assert 0.014 < VDP_YOY < 0.016 and 0.005 < HPI_YOY < 0.007                        # "+1,5 %", "+0,6 %"

SRC = "Quelle: Deutsche Bundesbank (Stand 25.11.2026) · Werte für September/Oktober 2026 teils vorläufig"


def pct(v, dec=1, sign=False):
    s = f"{v:+.{dec}f}" if sign else f"{v:.{dec}f}"
    return s.replace("-", "−").replace(".", ",") + " %"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def mx(m):
    return int(m[:4]) + (int(m[5:]) - 0.5) / 12


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 150), "2026 in Zahlen", t, S.c(0), 72, FG, "mm", "Black")
    tiles = [("Inflation Ø", pct(INF_AVG), "Jan.–Okt.", RED, S.c(1)),
             ("EZB-Einlagesatz", "2,0 → 2,5 %", "erste Erhöhung seit 2023", VIOLET, S.c(2)),
             ("Bauzins 5–10 J.", "3,58 → 3,91 %", "Jan. → Sept.", BLUE, S.c(3)),
             ("Wohneigentum", pct(100 * VDP_YOY, sign=True), "Q3 zum Vorjahr", GREEN, S.c(3) + 1.0)]
    for i, (lab, v, sub, col, st) in enumerate(tiles):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        x0 = 170 + (i % 2) * 810
        y0 = 260 + (i // 2) * 330
        card(d, (x0, y0, x0 + 760, y0 + 290), a, col)
        text(d, (x0 + 380, y0 + 65), lab, 36, MUTED, a, "mm", "SemiBold")
        text(d, (x0 + 380, y0 + 160), v, 76, col, a, "mm", "Black")
        text(d, (x0 + 380, y0 + 240), sub, 28, FG, a, "mm", "Medium")
    footer(d, prog(t, S.c(1), 0.6))


def draw_inflation(img, d, t, S):
    title(d, t, "Inflation 2025 und 2026", S.c(0), "Verbraucherpreise, Veränderung zum Vorjahresmonat")
    ch = Chart((260, 260, 1400, 860), (2025, 2026.84), (0, 4))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, (2025.04, 2025.5, 2026.04, 2026.5), range(0, 5), lambda x: {2025.04: "Jan. ’25", 2025.5: "Juli ’25",
            2026.04: "Jan. ’26", 2026.5: "Juli ’26"}[x], lambda v: f"{v} %")
    footer(d, ax, "Quelle: Verbraucherpreisindex, Bundesbank-Reihe BBDP1 auf Basis von Destatis-Daten")
    xs = np.array([mx(m) for m in M2526])
    ys = np.array([INF[m] for m in M2526])
    bw = (ch.x1 - ch.x0) / 22 * 0.6
    for i, m in enumerate(M2526):
        st = S.c(1) + i * 0.12 if m < "2026" else S.c(2) + (i - 12) * 0.15
        p = prog(t, st, 0.4)
        if p <= 0:
            continue
        cx, base = ch.px(xs[i], 0)
        _, top = ch.px(xs[i], ys[i] * p)
        col = GRAY if m < "2026" else (RED if ys[i] >= 3 else AMBER if ys[i] > 2 else BLUE)
        d.rectangle((cx - bw / 2, top, cx + bw / 2, base), fill=col)
        if m >= "2026":
            text(d, (cx, top - 10), pct(ys[i] * p), 22, FG, p, "mb", "Bold")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1460, 300, 1870, 560), a, RED)
        text(d, (1490, 355), "Ø Jan.–Okt. 2026", 28, MUTED, a, "lm", "SemiBold")
        text(d, (1490, 435), pct(INF_AVG), 70, RED, a, "lm", "Black")
        text(d, (1490, 510), "2025 im Jahresschnitt: 2,2 %", 26, FG, a, "lm", "Medium")


def draw_zinsen(img, d, t, S):
    title(d, t, "Zinsen: Januar vs. September 2026", S.c(0), "Durchschnittszinsen, private Haushalte, Neugeschäft")
    rows = [(S.c(1), "EZB-Einlagesatz", EZB["2026-01"], EZB["2026-09"], VIOLET),
            (S.c(2), "Tagesgeld & Giro (Ø)", TG["2026-01"], TG["2026-09"], GREEN),
            (S.c(3), "Dispo (Ø)", DISPO["2026-01"], DISPO["2026-09"], RED),
            (S.c(4), "Baukredit 5–10 J. (Ø)", BAU["2026-01"], BAU["2026-09"], BLUE)]
    a0 = prog(t, S.c(1), 0.5)
    text(d, (1150, 250), "Januar", 30, MUTED, a0, "mm", "SemiBold")
    text(d, (1500, 250), "September", 30, MUTED, a0, "mm", "SemiBold")
    for i, (st, lab, v0, v1, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 320 + i * 130
        card(d, (250, y, 1700, y + 105), a, col)
        text(d, (290, y + 53), lab, 38, FG, a, "lm", "Bold")
        text(d, (1150, y + 53), pct(v0, 2), 44, MUTED, a, "mm", "Black")
        text(d, (1325, y + 53), "→", 44, MUTED, a, "mm", "Black")
        text(d, (1500, y + 53), pct(v1, 2), 48, col, a, "mm", "Black")
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        text(d, (250, 880), f"Realzins Tagesgeld & Giro im September: {pct(100 * REAL_TG, sign=True)}", 40, RED, a,
             "lm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "Quelle: Deutsche Bundesbank · SU0200, SUD101, SUD112, SUD118 · Sept. 2026 vorläufig")


def draw_bau(img, d, t, S):
    title(d, t, "Was das beim Baukredit heißt", S.c(0), "300.000 €, 2 % Tilgung – Beispiel aus Video 4")
    for i, (st, lab, z, col) in enumerate(((S.c(1), "Januar 2026", BAU["2026-01"], GRAY),
                                           (S.c(2), "September 2026", BAU["2026-09"], RED))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 270, x0 + 660, 600), a, col)
        text(d, (x0 + 40, 330), lab, 36, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 620, 330), pct(z, 2), 44, col, a, "rm", "Black")
        text(d, (x0 + 40, 430), "Monatsrate", 32, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 520), eur(RATE(z), 2), 72, FG, a, "lm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        rrect(d, (250, 680, 1630, 800), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (940, 740), f"+{eur(RATE(3.91) - RATE(3.58), 2)} pro Monat – innerhalb von neun Monaten", 44, AMBER, a,
             "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "Modellrechnung: Rate = 300.000 € × (Zins + 2 %) ÷ 12 · Bundesbank SUD118")


def draw_immo(img, d, t, S):
    title(d, t, "Immobilienpreise 2025/2026", S.c(0), "Index selbst genutztes Wohneigentum (vdp), 2010 = 100, Quartale")
    qs = sorted(VDP)[-7:]
    ch = Chart((260, 260, 1300, 860), (-0.5, len(qs) - 0.5), (185, 196))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, range(len(qs)), range(186, 197, 2), lambda i: qs[i].replace("-", " "), str)
    footer(d, ax, "Quelle: Verband deutscher Pfandbriefbanken (vdp), via Bundesbank-Indikatorensystem · Destatis-Häuserpreisindex")
    bw = (ch.x1 - ch.x0) / len(qs) * 0.6
    for i, q in enumerate(qs):
        p = prog(t, S.c(1) + i * 0.25, 0.5)
        if p <= 0:
            continue
        cx, base = ch.px(i, 185)
        _, top = ch.px(i, lerp(185, VDP[q], p))
        d.rectangle((cx - bw / 2, top, cx + bw / 2, base), fill=GREEN if q.startswith("2026") else GRAY)
        text(d, (cx, top - 10), f"{VDP[q]:.1f}".replace(".", ","), 24, FG, p, "mb", "Bold")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        card(d, (1380, 300, 1870, 520), a, GREEN)
        text(d, (1410, 355), "vdp, Q3 2026 zum Vorjahr", 26, MUTED, a, "lm", "SemiBold")
        text(d, (1410, 440), pct(100 * VDP_YOY, sign=True), 70, GREEN, a, "lm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1380, 560, 1870, 780), a, BLUE)
        text(d, (1410, 615), "Destatis, Q2 2026 zum Vorjahr", 26, MUTED, a, "lm", "SemiBold")
        text(d, (1410, 700), pct(100 * HPI_YOY, sign=True), 70, BLUE, a, "lm", "Black")


def draw_fazit(img, d, t, S):
    text_pop(d, (W / 2, 170), "2026 in einem Satz pro Thema", t, S.c(0), 56, FG, "mm", "Black")
    rows = [(S.c(1), RED, "Preise:", "Inflation wieder etwas höher als 2025"),
            (S.c(2), VIOLET, "Zinsen:", "die EZB dreht erstmals seit 2023 wieder nach oben"),
            (S.c(3), GREEN, "Sparer:", "Ø-Zinsen steigen kaum – real weiter im Minus"),
            (S.c(4), BLUE, "Kredite & Immobilien:", "Baukredite teurer, Preise leicht steigend")]
    for i, (start, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 160
        card(d, (300, y, 1620, y + 135), a, col)
        text(d, (340, y + 48), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 98), b_txt, 40, FG, a, "lm", "Bold")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 220), "Einen guten Rutsch!", t, S.c(0), 64, AMBER, "mm", "Black")
    text_pop(d, (W / 2, 310), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(1), 40, FG, "mm", "Bold")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (690, 470, 1230, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (960, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (960, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (960, 665), "jeden Donnerstag ein neues Video", 26, MUTED, a, "mm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Zweitausendsechsundzwanzig in Zahlen. Was hat sich bei Preisen, Zinsen und Immobilien getan?",
            "Die Inflation lag von Januar bis Oktober im Schnitt bei rund zwei Komma sechs Prozent.",
            "Die Europäische Zentralbank hat die Zinsen zum ersten Mal seit zweitausenddreiundzwanzig wieder erhöht, von zwei auf zwei Komma fünf Prozent.",
            "Baukredite wurden teurer. Und die Preise für Wohneigentum sind leicht gestiegen, um eins Komma fünf Prozent.",
        ], draw_hook),
        Scene("inflation", [
            "Zuerst die Inflation.",
            "Zweitausendfünfundzwanzig lag sie fast durchgehend um zwei Prozent.",
            "Zweitausendsechsundzwanzig begann sie mit zwei Komma eins Prozent, im Februar sogar nur eins Komma neun. Ab März ging es nach oben.",
            "Im Schnitt der ersten zehn Monate: rund zwei Komma sechs Prozent. Mehr als die zwei Komma zwei Prozent im Jahr davor.",
            "Der höchste Wert kam im September mit drei Komma drei Prozent. Im Oktober waren es zwei Komma acht.",
        ], draw_inflation),
        Scene("zinsen", [
            "Dann die Zinsen.",
            "Die EZB hat den Einlagesatz im Juni auf zwei Komma zwei fünf und im September auf zwei Komma fünf Prozent erhöht. Davor hatte sie seit Herbst zweitausenddreiundzwanzig nur gesenkt.",
            "Bei Sparern kam davon wenig an: Auf täglich verfügbares Geld gab es im Januar im Schnitt null Komma vier drei Prozent, im September null Komma fünf zwei.",
            "Der Dispo stieg von neun Komma drei auf neun Komma fünf neun Prozent.",
            "Und Baukredite mit fünf bis zehn Jahren Zinsbindung von drei Komma fünf acht auf drei Komma neun eins Prozent.",
            "Bei drei Komma drei Prozent Inflation hieß das für Sparer im September: real minus zwei Komma sieben Prozent.",
        ], draw_zinsen),
        Scene("bau", [
            "Was heißt das für einen Baukredit?",
            "Dreihunderttausend Euro mit zwei Prozent Tilgung: Im Januar waren das beim Durchschnittszins tausenddreihundertfünfundneunzig Euro im Monat.",
            "Im September tausendvierhundertsiebenundsiebzig Euro fünfzig.",
            "Zweiundachtzig Euro fünfzig mehr pro Monat, innerhalb von nur neun Monaten.",
        ], draw_bau),
        Scene("immo", [
            "Und die Immobilienpreise?",
            "Von Ende zweitausendzweiundzwanzig bis Anfang zweitausendvierundzwanzig sind sie gefallen. Seitdem steigen sie wieder leicht, liegen aber noch unter dem Höchststand.",
            "Der Index der Pfandbriefbanken für selbst genutztes Wohneigentum lag im dritten Quartal eins Komma fünf Prozent über dem Vorjahr.",
            "Der Häuserpreisindex des Statistischen Bundesamts zeigt für das zweite Quartal ein Plus von null Komma sechs Prozent.",
        ], draw_immo),
        Scene("fazit", [
            "Zweitausendsechsundzwanzig in vier Sätzen.",
            "Die Inflation war wieder etwas höher als im Jahr davor.",
            "Die EZB hat zum ersten Mal seit zweitausenddreiundzwanzig die Zinsen erhöht.",
            "Bei Sparern kam davon kaum etwas an, real ging Kaufkraft verloren.",
            "Kredite für Immobilien wurden teurer, und die Preise sind leicht gestiegen. Die Werte für November und Dezember waren bei Redaktionsschluss noch nicht veröffentlicht.",
        ], draw_fazit),
        Scene("outro", [
            "Einen guten Rutsch ins neue Jahr!",
            "Wie immer: keine Beratung, sondern offizielle Zahlen. Alle Quellen stehen in der Beschreibung.",
            "Wenn du nächstes Jahr weiter mitrechnen willst, dann abonnier den Kanal. Jeden Donnerstag kommt ein neues Video.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
