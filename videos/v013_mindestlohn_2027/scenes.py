"""Video 013: Mindestlohn 2027 – 14,60 €: was er bringt und wie stark er real gestiegen ist."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, Chart, card, dot, ease_in_out, eur, fade, prog, text
from lib.lohn2026 import netto_monat
from lib.longform import cards, fazit, footer, hook_two, numbered, outro, title

# Gesetzlicher Mindestlohn (MiLoG, Mindestlohnanpassungsverordnungen; 2026/2027 Beschluss der Kommission vom 27.06.2025)
STUFEN = [(2015.0, 8.50), (2017.0, 8.84), (2019.0, 9.19), (2020.0, 9.35), (2021.0, 9.50), (2021.5, 9.60),
          (2022.0, 9.82), (2022.5, 10.45), (2022.75, 12.00), (2024.0, 12.41), (2025.0, 12.82), (2026.0, 13.90),
          (2027.0, 14.60)]
STUNDEN = 40 * 52 / 12                     # Vollzeit 40 h/Woche, Monatsstunden


def _vpi():
    out = {}
    for line in Path("videos/v008_2026_in_zahlen/data/vpi_index.csv").read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and len(c[0]) == 7 and c[0][4] == "-" and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


VPI = _vpi()
ML26, ML27 = 13.90, 14.60
B26, B27 = round(ML26 * STUNDEN, 2), round(ML27 * STUNDEN, 2)
N26, N27 = netto_monat(B26), netto_monat(B27)           # Steuer: Tarif 2026 als Näherung (Tarif 2027 noch Entwurf)
SV27 = round(N27["RV"] + N27["AV"] + N27["KV"] + N27["PV"], 2)
NOM = ML26 / 8.50 - 1
PRICE = VPI["2026-10"] / VPI["2015-01"] - 1
REAL = (1 + NOM) / (1 + PRICE) - 1
NOM27 = ML27 / 8.50 - 1

# Every number spoken in the narration is checked here.
assert B27 == 2530.67 and B26 == 2409.33 and round(8.50 * STUNDEN, 2) == 1473.33
assert round(ML27 - ML26, 2) == 0.70 and round(B27 - B26) == 121
assert 0.635 < NOM < 0.636 and 0.358 < PRICE < 0.36 and 0.20 < REAL < 0.21 and 0.717 < NOM27 < 0.718
assert SV27 == 550.40 and N27["LSt"] == 193.58 and N27["Netto"] == 1786.69 and N26["Netto"] == 1716.49
assert round(N27["Netto"] - N26["Netto"]) == 70

SRC = "Mindestlohn: MiLoG / Mindestlohnkommission (Beschluss 27.06.2025) · Vollzeit 40 h/Woche angenommen"


def draw_hook(img, d, t, S):
    hook_two(d, t, S, "Mindestlohn 2027", (1, "pro Stunde", "14,60 €", "seit 1. Januar 2027", GREEN),
             (2, "Vollzeit, 40 h/Woche", eur(B27, 2), "brutto im Monat", BLUE),
             (3, "Wie viel davon bleibt – und wie viel mehr ist das wirklich?"), SRC)


def draw_verlauf(img, d, t, S):
    title(d, t, "Der Mindestlohn seit 2015", S.c(0), "Euro pro Stunde, gesetzlicher Mindestlohn")
    ch = Chart((260, 270, 1400, 860), (2015, 2027.9), (7, 16))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(2015, 2028, 2), range(8, 17, 2), lambda y: f"’{y % 100:02}", lambda v: f"{v} €")
    footer(d, ax, SRC)
    xs, ys = [], []
    for i, (x, v) in enumerate(STUFEN):
        nx = STUFEN[i + 1][0] if i + 1 < len(STUFEN) else 2027.9
        xs += [x, nx]
        ys += [v, v]
    up = 2015 + 12.9 * prog(t, S.c(1), S.e(3) - S.c(1), ease_in_out)
    if up > 2015:
        ch.line(d, np.array(xs), np.array(ys), GREEN, 6, up)
    for ci, (x, v) in ((1, STUFEN[0]), (2, STUFEN[8]), (3, STUFEN[11]), (3, STUFEN[12])):
        a = prog(t, S.c(ci) + 0.8, 0.5) if up >= x else 0
        if a > 0:
            p = ch.px(x, v)
            dot(d, p, 9, GREEN)
            text(d, (p[0] - 10, p[1] - 16), eur(v, 2), 30, FG, a, "rb", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        card(d, (1460, 300, 1870, 600), a, GREEN)
        text(d, (1490, 355), "2015 → 2027", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1490, 445), f"+{NOM27 * 100:.1f} %".replace(".", ","), 64, GREEN, a, "lm", "Black")
        text(d, (1490, 530), "8,50 € → 14,60 €", 30, FG, a, "lm", "Medium")


def draw_real(img, d, t, S):
    title(d, t, "Und nach Inflation?", S.c(0), "Januar 2015 bis Oktober 2026")
    rows = [(S.c(1), "Mindestlohn 2015 → 2026", "8,50 € → 13,90 €", f"+{NOM * 100:.1f} %".replace(".", ","), GREEN),
            (S.c(2), "Verbraucherpreise", "Index 93,1 → 126,5", f"+{PRICE * 100:.1f} %".replace(".", ","), RED),
            (S.c(3), "Kaufkraft des Mindestlohns", "1,635 ÷ 1,359 − 1", f"+{REAL * 100:.0f} %", AMBER)]
    for i, (st, lab, sub, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 190
        card(d, (250, y, 1670, y + 160), a, col)
        text(d, (290, y + 58), lab, 38, FG, a, "lm", "Bold")
        text(d, (290, y + 115), sub, 30, MUTED, a, "lm", "Medium")
        text(d, (1630, y + 80), v, 64, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (250, 880), "Der große Sprung kam im Oktober 2022 – mitten in der höchsten Inflation.", 34, FG, a, "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5), "Verbraucherpreisindex 2020 = 100 (Bundesbank-Reihe BBDP1, Destatis)")


def draw_netto(img, d, t, S):
    title(d, t, "Was netto bleibt", S.c(0), "Vollzeit, Steuerklasse I, kinderlos, ohne Kirchensteuer")
    rows = [(S.c(1), "Brutto", eur(B27, 2), FG), (S.c(2), "Sozialversicherung 21,75 %", "−" + eur(SV27, 2), BLUE),
            (S.c(3), "Lohnsteuer (Tarif 2026 als Näherung)", "−" + eur(N27["LSt"], 2), RED)]
    for i, (st, lab, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 290 + i * 95
        text(d, (250, y), lab, 36, FG if i == 0 else MUTED, a, "lm", "SemiBold")
        text(d, (1300, y), v, 46, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        d.line((250, 560, 1300, 560), fill=fade((70, 82, 108), a), width=2)
        text(d, (250, 620), "netto ≈", 40, FG, a, "lm", "Bold")
        text(d, (1300, 620), eur(N27["Netto"], 2), 60, GREEN, a, "rm", "Black")
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        card(d, (1380, 290, 1870, 640), a, AMBER)
        text(d, (1410, 345), "vs. 2026 (13,90 €)", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1410, 430), "+121 € brutto", 44, FG, a, "lm", "Black")
        text(d, (1410, 510), "≈ +70 € netto", 44, GREEN, a, "lm", "Black")
        text(d, (1410, 590), "pro Monat", 30, FG, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "Berechnung nach BMF-PAP 2026 · Sozialversicherung 2027 unverändert (Ø-Zusatzbeitrag 2,9 %)")


def draw_grenzen(img, d, t, S):
    numbered(d, t, S, [(1, "Vollzeit angenommen", "40 Stunden pro Woche – bei Teilzeit entsprechend weniger."),
                       (2, "Steuer 2027 genähert", "Der neue Einkommensteuertarif 2027 war bei Erstellung noch nicht beschlossen."),
                       (3, "Ausnahmen", "z. B. Azubis, Minderjährige ohne Ausbildung, Langzeitarbeitslose in den ersten 6 Monaten.")],
             "3 ehrliche Einschränkungen")


def draw_fazit(img, d, t, S):
    fazit(d, t, S, "Mindestlohn 2027 in drei Zahlen", [
        (1, GREEN, "Stundenlohn:", "14,60 € – 70 Cent mehr als 2026"),
        (2, BLUE, "Vollzeit:", f"{eur(B27, 2)} brutto, ≈ {eur(N27['Netto'])} netto"),
        (3, AMBER, "Seit 2015:", "rund 20 % mehr Kaufkraft trotz Inflation")])


def draw_outro(img, d, t, S):
    outro(d, t, S, ["Festgeld oder", "Tagesgeld?", "mit Bundesbank-Daten"])


def scenes():
    return [
        Scene("hook", [
            "Seit dem ersten Januar zweitausendsiebenundzwanzig gilt ein neuer Mindestlohn.",
            "Vierzehn Euro sechzig pro Stunde.",
            "Bei Vollzeit mit vierzig Stunden pro Woche sind das zweitausendfünfhundertdreißig Euro siebenundsechzig brutto im Monat.",
            "Wir rechnen nach, wie viel davon bleibt und wie viel mehr das nach Inflation wirklich ist.",
        ], draw_hook),
        Scene("verlauf", [
            "Ein kurzer Blick zurück.",
            "Eingeführt wurde der Mindestlohn zweitausendfünfzehn mit acht Euro fünfzig.",
            "Bis Mitte zweitausendzweiundzwanzig stieg er in kleinen Schritten, dann kam im Oktober der Sprung auf zwölf Euro.",
            "Zweitausendsechsundzwanzig waren es dreizehn Euro neunzig, jetzt vierzehn Euro sechzig.",
            "Seit zweitausendfünfzehn ist das ein Plus von gut einundsiebzig Prozent.",
        ], draw_verlauf),
        Scene("real", [
            "Aber was ist davon nach Inflation übrig?",
            "Von zweitausendfünfzehn bis zweitausendsechsundzwanzig stieg der Mindestlohn um dreiundsechzig Komma fünf Prozent.",
            "Die Verbraucherpreise stiegen von Januar zweitausendfünfzehn bis Oktober zweitausendsechsundzwanzig um fünfunddreißig Komma neun Prozent.",
            "Real bleibt also ein Plus von rund zwanzig Prozent Kaufkraft.",
            "Der große Sprung kam im Oktober zweitausendzweiundzwanzig, mitten in der höchsten Inflation.",
        ], draw_real),
        Scene("netto", [
            "Und was bleibt netto bei Vollzeit?",
            "Brutto zweitausendfünfhundertdreißig Euro siebenundsechzig.",
            "Davon gehen fünfhundertfünfzig Euro vierzig an die Sozialversicherung.",
            "Dazu rund hundertdreiundneunzig Euro Lohnsteuer, gerechnet mit dem Tarif zweitausendsechsundzwanzig als Näherung.",
            "Netto bleiben damit rund tausendsiebenhundertsechsundachtzig Euro.",
            "Gegenüber zweitausendsechsundzwanzig sind das hunderteinundzwanzig Euro mehr brutto und rund siebzig Euro mehr netto im Monat.",
        ], draw_netto),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Wir rechnen mit Vollzeit, vierzig Stunden pro Woche. Bei Teilzeit ist es entsprechend weniger.",
            "Zweitens: Der neue Einkommensteuertarif für zweitausendsiebenundzwanzig war bei Erstellung des Videos noch nicht beschlossen. Die Steuer ist deshalb eine Näherung.",
            "Drittens: Es gibt Ausnahmen, zum Beispiel für Auszubildende, Minderjährige ohne Berufsabschluss und Langzeitarbeitslose in den ersten sechs Monaten.",
        ], draw_grenzen),
        Scene("fazit", [
            "Der Mindestlohn zweitausendsiebenundzwanzig in drei Zahlen.",
            "Vierzehn Euro sechzig pro Stunde, siebzig Cent mehr als im Vorjahr.",
            "Bei Vollzeit rund zweitausendfünfhundertdreißig Euro brutto und rund tausendsiebenhundertsechsundachtzig netto.",
            "Und seit zweitausendfünfzehn rund zwanzig Prozent mehr Kaufkraft, trotz Inflation.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Werte und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video: Festgeld oder Tagesgeld? Mit den Zinsen der Bundesbank.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
