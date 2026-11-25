"""Video 006: Brutto, netto – was vom Gehalt 2026 wirklich bleibt (offizieller BMF-Programmablaufplan 2026)."""
from decimal import Decimal as D

import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card,
                     dot, ease_in_out, eur, fade, lerp, piecewise, prog, rrect, text, text_pop,
                     thick_line)
from lib.lohn2026 import BBGKVPV, BBGRVALV, GFB, KVZ_AVG, lohnsteuer_jahr, netto_monat, uptab26

# ---------------------------------------------------------------- Modell (Steuerklasse I, kinderlos, ohne Kirchensteuer)
B = 3000
M = netto_monat(B)
SV = M["RV"] + M["AV"] + M["KV"] + M["PV"]
JL = B * 12
VSP = 7254                                   # Vorsorgepauschale laut PAP (RV 3.348 + KV/PV 3.906, aufgerundet)
ZVE = JL - 1230 - 36 - VSP
EST = int(uptab26(ZVE))
SV_RATE = 9.3 + 1.3 + 7.3 + float(KVZ_AVG) / 2 + 1.8 + 0.6
CURVE_B = np.arange(1500, 8001, 100)
CURVE_Q = np.array([netto_monat(int(b))["Netto"] / b * 100 for b in CURVE_B])
EX = [(b, netto_monat(b)) for b in (2500, 3000, 4000, 5000, 6000)]
RAISE_3000 = netto_monat(3100)["Netto"] - netto_monat(3000)["Netto"]
RAISE_5000 = netto_monat(5100)["Netto"] - netto_monat(5000)["Netto"]
SOLI_START = next(b for b in range(5000, 9000, 10) if netto_monat(b)["Soli"] > 0)
N4000, N4000_3 = netto_monat(4000), netto_monat(4000, stkl=3)

# Every number spoken in the narration is checked here.
assert M["Netto"] == 2054.42 and 945 < B - M["Netto"] < 946                     # "zweitausendvierundfünfzig", "945"
assert 0.31 < (B - M["Netto"]) / B < 0.32                                      # "fast ein Drittel"
assert SV == 652.5 and M["LSt"] == 293.08 and M["Soli"] == 0                    # Aufteilung
assert (M["RV"], M["AV"], M["KV"], M["PV"]) == (279.0, 39.0, 262.5, 72.0)
assert abs(SV_RATE - 21.75) < 1e-9                                             # "einundzwanzig Komma sieben fünf"
assert float(BBGKVPV) / 12 == 5812.5 and float(BBGRVALV) / 12 == 8450          # BBG
assert lohnsteuer_jahr(JL)[0] == EST == 3517 and ZVE == 27480 and GFB == 12348  # Rechenweg
assert round(CURVE_Q[0], 1) == 77.6 and round(CURVE_Q[-1], 1) == 58.5           # Nettoquote 1.500 / 8.000
assert [round(n["Netto"]) for _, n in EX] == [1769, 2054, 2606, 3130, 3642]
assert 56 < RAISE_3000 < 57 and 50.5 < RAISE_5000 < 51.5                        # "+56 €", "+51 €"
assert 7690 < SOLI_START <= 7700                                               # "rund 7.700 €"
assert round(N4000["Netto"]) == 2606 and round(N4000_3["Netto"]) == 2928

SRC = "Berechnung nach BMF-Programmablaufplan Lohnsteuer 2026 · StKl. I, kinderlos, ohne Kirchensteuer"


def pct(v, dec=1):
    return f"{v:.{dec}f}".replace(".", ",") + " %"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


PARTS = [("Rentenversicherung", M["RV"], VIOLET), ("Arbeitslosenvers.", M["AV"], GRAY),
         ("Krankenversicherung", M["KV"], BLUE), ("Pflegeversicherung", M["PV"], (125, 211, 252)),
         ("Lohnsteuer", M["LSt"], RED)]


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 170), "3.000 € brutto im Monat", t, S.c(0), 60, FG, "mm", "Black")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (560, 280, 1360, 560), a, GREEN)
        text(d, (W / 2, 340), "netto", 40, MUTED, a, "mm", "SemiBold")
        p = prog(t, S.c(1) + 0.2, 1.4, ease_in_out)
        text(d, (W / 2, 450), eur(lerp(B, M["Netto"], p), 2), 110, GREEN, a, "mm", "Black")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        rrect(d, (460, 640, 1460, 760), 20, fill=fade((50, 26, 30), a), outline=fade(RED, a * 0.6), width=2)
        text(d, (W / 2, 700), f"−{eur(B - M['Netto'], 2)}: fast ein Drittel", 48, RED, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6))


def draw_aufteilung(img, d, t, S):
    title(d, t, "Wohin gehen die 945,58 €?", S.c(0), "3.000 € brutto, Monat, 2026")
    x0, x1, y0, y1 = 250, 1670, 300, 400
    scale = (x1 - x0) / B
    x = x0
    cues = [S.c(1), S.c(1) + 0.6, S.c(2), S.c(2) + 0.8, S.c(3)]
    for i, ((lab, v, col), st) in enumerate(zip(PARTS, cues)):
        a = prog(t, st, 0.5)
        w = v * scale
        if a > 0:
            d.rectangle((x, y0, x + w * prog(t, st, 0.7, ease_in_out), y1), fill=fade(col, a))
            yy = 470 + i * 70
            dot(d, (x0 + 14, yy), 12, fade(col, a))
            text(d, (x0 + 44, yy), lab, 34, FG, a, "lm", "SemiBold")
            text(d, (1000, yy), eur(v, 2), 38, col, a, "rm", "Black")
        x += w
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        d.rectangle((x, y0, x1, y1), fill=fade(GREEN, a))
        text(d, ((x + x1) / 2, (y0 + y1) / 2), "netto " + eur(M["Netto"], 2), 34, (13, 19, 33), a, "mm", "Black")
        card(d, (1080, 460, 1780, 780), a)
        text(d, (1120, 520), "Sozialversicherung", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1740, 520), eur(SV, 2), 40, BLUE, a, "rm", "Black")
        text(d, (1120, 620), "Steuer", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1740, 620), eur(M["LSt"], 2), 40, RED, a, "rm", "Black")
        text(d, (1120, 720), "Soli", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1740, 720), "0,00 €", 40, FG, a, "rm", "Black")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · Zusatzbeitrag 2,9 % (Ø)")


def draw_sv(img, d, t, S):
    title(d, t, "Sozialversicherung 2026", S.c(0), "Dein Anteil als Arbeitnehmer – der Arbeitgeber zahlt etwa gleich viel dazu")
    rows = [(S.c(1), "Rente", "9,3 %", VIOLET), (S.c(1) + 0.5, "Arbeitslosigkeit", "1,3 %", GRAY),
            (S.c(2), "Krankheit", "7,3 % + 1,45 %", BLUE), (S.c(3), "Pflege (kinderlos)", "1,8 % + 0,6 %", (125, 211, 252))]
    for i, (st, lab, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 250 + i * 120
        card(d, (250, y, 1100, y + 100), a, col)
        text(d, (290, y + 52), lab, 38, FG, a, "lm", "Bold")
        text(d, (1060, y + 52), v, 40, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        text(d, (250, 790), "zusammen", 32, MUTED, a, "lm", "SemiBold")
        text(d, (250, 860), pct(SV_RATE, 2) + " vom Brutto", 56, AMBER, a, "lm", "Black")
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        card(d, (1180, 250, 1860, 610), a, AMBER)
        text(d, (1220, 305), "Beitragsbemessungsgrenzen", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1220, 385), "Kranken & Pflege", 30, FG, a, "lm", "SemiBold")
        text(d, (1820, 385), "5.812,50 €", 38, BLUE, a, "rm", "Black")
        text(d, (1220, 465), "Rente & Arbeitslos.", 30, FG, a, "lm", "SemiBold")
        text(d, (1820, 465), "8.450,00 €", 38, VIOLET, a, "rm", "Black")
        text(d, (1220, 550), "pro Monat – darüber keine Beiträge", 26, MUTED, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "Beitragssätze und Rechengrößen 2026 · KV-Zusatzbeitrag: Durchschnitt 2,9 %, kassenabhängig")


def draw_steuer(img, d, t, S):
    title(d, t, "Wie die Lohnsteuer entsteht", S.c(0), "3.000 € × 12, Steuerklasse I")
    rows = [(S.c(1), "Jahresbrutto", eur(JL), FG),
            (S.c(2), "− Arbeitnehmer-Pauschbetrag", "1.230 €", MUTED),
            (S.c(2) + 0.6, "− Sonderausgaben-Pauschbetrag", "36 €", MUTED),
            (S.c(3), "− Vorsorgepauschale (Sozialbeiträge)", eur(VSP), MUTED),
            (S.c(4), "= zu versteuerndes Einkommen", eur(ZVE), AMBER)]
    for i, (st, lab, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 85
        text(d, (250, y), lab, 34, FG if i in (0, 4) else MUTED, a, "lm", "Bold" if i in (0, 4) else "SemiBold")
        text(d, (1300, y), v, 40, col, a, "rm", "Black")
    a = prog(t, S.c(4) + 0.5, 0.5)
    if a > 0:
        d.line((250, 655, 1300, 655), fill=fade((70, 82, 108), a), width=2)
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        card(d, (250, 720, 1720, 900), a, RED)
        text(d, (290, 775), f"Tarif 2026: steuerfrei bis {eur(GFB)}, dann 14 % bis 42 % (45 % ganz oben)", 32, FG, a, "lm", "SemiBold")
        text(d, (290, 850), f"→ {eur(EST)} im Jahr = {eur(M['LSt'], 2)} im Monat", 44, RED, a, "lm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "§ 32a EStG, Grundtarif 2026 · Programmablaufplan Lohnsteuer 2026 (BMF)")


def draw_kurve(img, d, t, S):
    title(d, t, "Wie viel Prozent bleiben netto?", S.c(0), "Monatsbrutto 1.500 € bis 8.000 €, Steuerklasse I, kinderlos")
    ch = Chart((260, 260, 1300, 860), (1500, 8000), (50, 80))
    ax = prog(t, S.c(0), 0.8)
    ch.axes(d, ax, range(2000, 8001, 1000), range(50, 81, 10), lambda v: f"{v // 1000}.000 €", lambda v: f"{v} %")
    footer(d, ax)
    up = 1500 + 6500 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 1500:
        ch.line(d, CURVE_B, CURVE_Q, GREEN, 6, up)
    for st, b, n in ((S.c(1) + 0.5, 1500, None), (S.c(2) + 0.5, 8000, None)):
        a = prog(t, st, 0.5) if up >= b - 1 else 0
        if a > 0:
            q = CURVE_Q[0] if b == 1500 else CURVE_Q[-1]
            p = ch.px(b, q)
            dot(d, p, 10, GREEN)
            text(d, (p[0] + (18 if b == 1500 else -14), p[1] + (14 if b == 1500 else -18)), pct(q), 32, FG, a,
                 "lt" if b == 1500 else "rb", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1380, 270, 1870, 760), a)
        text(d, (1410, 320), "Brutto → Netto", 28, MUTED, a, "lm", "SemiBold")
        for i, (b, n) in enumerate(EX):
            y = 390 + i * 75
            text(d, (1410, y), eur(b), 34, FG, a, "lm", "SemiBold")
            text(d, (1840, y), eur(n["Netto"]), 38, GREEN, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (1380, 830), f"Soli erst ab ≈ {eur(round(SOLI_START, -2))} brutto", 30, AMBER, a, "lm", "Bold")


def draw_erhoehung(img, d, t, S):
    title(d, t, "Lohnt sich eine Gehaltserhöhung?", S.c(0), "Mythos: „Durch die höhere Steuer bleibt am Ende weniger.“")
    for i, (st, b, r) in enumerate(((S.c(1), 3000, RAISE_3000), (S.c(2), 5000, RAISE_5000))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 270, x0 + 660, 640), a, GREEN)
        text(d, (x0 + 40, 330), f"{eur(b)} → {eur(b + 100)} brutto", 38, FG, a, "lm", "Bold")
        text(d, (x0 + 40, 420), "netto mehr", 30, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 520), "+" + eur(r, 2), 84, GREEN, a, "lm", "Black")
        text(d, (x0 + 40, 600), f"von 100 € bleiben {round(r)} %", 28, MUTED, a, "lm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        rrect(d, (250, 720, 1630, 860), 20, fill=fade((24, 48, 40), a), outline=fade(GREEN, a * 0.6), width=2)
        text(d, (W / 2 - 20, 765), "Mehr brutto heißt immer mehr netto.", 44, GREEN, a, "mm", "Black")
        text(d, (W / 2 - 20, 820), "Der höhere Steuersatz gilt nur für den zusätzlichen Euro.", 30, FG, a, "mm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5))


def draw_grenzen(img, d, t, S):
    title(d, t, "4 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Kirchensteuer fehlt", "Mit Kirchensteuer (zusätzlich 8 bzw. 9 % der Lohnsteuer) bleibt etwas weniger."),
             (S.c(2), "2", "Krankenkasse", "Der Zusatzbeitrag hängt von der Kasse ab – wir rechnen mit Ø 2,9 %."),
             (S.c(3), "3", "Kinder & Steuerklasse", "Mit Kind ist die Pflegeversicherung günstiger, Steuerklasse III/V verteilt anders."),
             (S.c(4), "4", "Lohnsteuer ist Vorauszahlung", "Mit der Steuererklärung kann Geld zurückkommen.")]
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
    text_pop(d, (W / 2, 170), "Was vom Brutto bleibt", t, S.c(0), 58, FG, "mm", "Black")
    rows = [(S.c(1), BLUE, "Sozialversicherung:", "gut ein Fünftel – bis zur Beitragsgrenze"),
            (S.c(2), RED, "Lohnsteuer:", "steigt mit dem Einkommen – aber nur auf den Teil darüber"),
            (S.c(3), GREEN, "Netto bei 3.000 € brutto:", f"{eur(M['Netto'], 2)} (StKl. I, kinderlos)")]
    for i, (start, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 170
        card(d, (300, y, 1620, y + 140), a, col)
        text(d, (340, y + 50), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 100), b_txt, 40, FG, a, "lm", "Bold")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(0), 52, FG,
             "mm", "Bold")
    text_pop(d, (W / 2, 335), "Rechenweg, Sätze & Quellen stehen in der Beschreibung.", t, S.c(1), 32, MUTED,
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
        text(d, (1060, 580), "Weihnachtsgeld:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Was netto bleibt", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "am 24. Dezember", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Dreitausend Euro brutto im Monat.",
            "Auf dem Konto landen davon im Jahr zweitausendsechsundzwanzig zweitausendvierundfünfzig Euro und zweiundvierzig Cent.",
            "Rund neunhundertfünfundvierzig Euro sind weg, fast ein Drittel. Wir rechnen nach, wohin sie gehen. Mit dem offiziellen Rechenweg des Finanzministeriums.",
        ], draw_hook),
        Scene("aufteilung", [
            "Unser Beispiel: Steuerklasse eins, keine Kinder, keine Kirchensteuer.",
            "Zweihundertneunundsiebzig Euro gehen an die Rentenversicherung, neununddreißig Euro an die Arbeitslosenversicherung.",
            "Zweihundertzweiundsechzig Euro fünfzig an die Krankenversicherung und zweiundsiebzig Euro an die Pflegeversicherung.",
            "Und zweihundertdreiundneunzig Euro und acht Cent Lohnsteuer. Solidaritätszuschlag fällt hier keiner an.",
            "Zusammen sind das sechshundertzweiundfünfzig Euro fünfzig Sozialversicherung und zweihundertdreiundneunzig Euro Steuer. Der größere Teil geht also gar nicht ans Finanzamt.",
        ], draw_aufteilung),
        Scene("sv", [
            "Schauen wir uns die Sozialversicherung genauer an.",
            "Für die Rente zahlst du neun Komma drei Prozent deines Bruttos, für die Arbeitslosenversicherung eins Komma drei.",
            "Für die Krankenversicherung sieben Komma drei Prozent plus die Hälfte des Zusatzbeitrags deiner Kasse. Im Schnitt sind das eins Komma vier fünf Prozent.",
            "Für die Pflege eins Komma acht Prozent, wer über dreiundzwanzig ist und keine Kinder hat, zahlt null Komma sechs Prozent extra.",
            "Zusammen einundzwanzig Komma sieben fünf Prozent. Ungefähr genauso viel zahlt dein Arbeitgeber noch einmal obendrauf.",
            "Und es gibt Obergrenzen: Für Kranken- und Pflegeversicherung zählt nur das Gehalt bis fünftausendachthundertzwölf Euro fünfzig im Monat, für Rente und Arbeitslosenversicherung bis achttausendvierhundertfünfzig Euro.",
        ], draw_sv),
        Scene("steuer", [
            "Und wie entsteht die Lohnsteuer?",
            "Gerechnet wird aufs Jahr: zwölf mal dreitausend sind sechsunddreißigtausend Euro.",
            "Davon werden pauschal tausendzweihundertdreißig Euro für Werbungskosten und sechsunddreißig Euro für Sonderausgaben abgezogen.",
            "Dazu die Vorsorgepauschale: Ein großer Teil deiner Beiträge für Rente, Kranken- und Pflegeversicherung ist steuerfrei. Hier siebentausendzweihundertvierundfünfzig Euro.",
            "Übrig bleiben siebenundzwanzigtausendvierhundertachtzig Euro zu versteuerndes Einkommen.",
            "Die ersten zwölftausenddreihundertachtundvierzig Euro sind steuerfrei. Danach steigt der Steuersatz von vierzehn auf zweiundvierzig Prozent, bei sehr hohen Einkommen auf fünfundvierzig. Ergebnis: dreitausendfünfhundertsiebzehn Euro im Jahr, also zweihundertdreiundneunzig Euro im Monat.",
        ], draw_steuer),
        Scene("kurve", [
            "Je höher das Gehalt, desto kleiner der Anteil, der netto bleibt.",
            "Bei tausendfünfhundert Euro brutto sind es siebenundsiebzig Komma sechs Prozent.",
            "Bei achttausend Euro nur noch achtundfünfzig Komma fünf Prozent.",
            "Konkret: Zweitausendfünfhundert Euro brutto werden zu rund tausendsiebenhundertneunundsechzig Euro netto, fünftausend Euro zu rund dreitausendeinhundertdreißig.",
            "Den Solidaritätszuschlag zahlen Alleinstehende übrigens erst ab rund siebentausendsiebenhundert Euro brutto im Monat.",
        ], draw_kurve),
        Scene("erhoehung", [
            "Ein häufiger Mythos: Eine Gehaltserhöhung lohnt sich nicht, weil dann mehr Steuern fällig werden.",
            "Von dreitausend auf dreitausendeinhundert Euro brutto: netto bleiben rund sechsundfünfzig Euro mehr.",
            "Von fünftausend auf fünftausendeinhundert Euro: rund einundfünfzig Euro mehr.",
            "Mehr brutto heißt also immer mehr netto. Der höhere Steuersatz gilt nur für den zusätzlichen Euro, nicht für das ganze Gehalt.",
        ], draw_erhoehung),
        Scene("grenzen", [
            "Vier ehrliche Einschränkungen.",
            "Erstens: Kirchensteuer haben wir weggelassen. Wer sie zahlt, zahlt zusätzlich acht oder neun Prozent der Lohnsteuer.",
            "Zweitens: Der Zusatzbeitrag hängt von deiner Krankenkasse ab. Wir rechnen mit dem Durchschnitt von zwei Komma neun Prozent.",
            "Drittens: Mit Kindern ist die Pflegeversicherung günstiger, und in den Steuerklassen drei und fünf wird die Steuer anders verteilt.",
            "Viertens: Die Lohnsteuer ist nur eine Vorauszahlung. Mit der Steuererklärung kann Geld zurückkommen, zum Beispiel bei hohen Fahrtkosten.",
        ], draw_grenzen),
        Scene("fazit", [
            "Was bleibt also vom Brutto?",
            "Gut ein Fünftel geht an die Sozialversicherung, bis zu den Beitragsgrenzen.",
            "Die Lohnsteuer steigt mit dem Einkommen, aber der höhere Satz gilt immer nur für den Teil darüber.",
            "Bei dreitausend Euro brutto bleiben in Steuerklasse eins zweitausendvierundfünfzig Euro.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Den Rechenweg, alle Sätze und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, mit echten Zahlen statt Versprechen, dann abonnier den Kanal.",
            "Am vierundzwanzigsten Dezember rechnen wir nach, wie viel vom Weihnachtsgeld netto übrig bleibt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
