"""Video 014: Festgeld oder Tagesgeld? Zinsen nach Laufzeit, real nach Inflation (Bundesbank-Daten)."""
from pathlib import Path

import numpy as np

from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, Chart, card, dot, ease_in_out, eur, fade, prog, text
from lib.longform import cards, fazit, footer, hook_two, numbered, outro, table, title

DATA = Path(__file__).parent / "data"


def _bbk(name):
    out = {}
    for line in (DATA / name).read_text(encoding="utf-8-sig").splitlines():
        c = line.split(";")
        if len(c) > 1 and len(c[0]) == 7 and c[0][4] == "-" and c[1] not in ("", "."):
            out[c[0]] = float(c[1].replace(",", "."))
    return out


TG = _bbk("SUD101_tagesgeld_giro.csv")
F1 = _bbk("SUD102_festgeld_bis_1j.csv")
F2 = _bbk("SUD103_festgeld_1_2j.csv")
F3 = _bbk("SUD104_festgeld_ueber_2j.csv")
INF = _bbk("vpi_vorjahr.csv")
EZB = _bbk("ezb_einlagesatz.csv")
M = "2026-09"
RATES = [("Tagesgeld & Giro (Ø)", TG[M], GRAY), ("Festgeld bis 1 Jahr", F1[M], BLUE),
         ("Festgeld 1 bis 2 Jahre", F2[M], VIOLET), ("Festgeld über 2 Jahre", F3[M], GREEN)]
INF_AVG = sum(INF[f"2026-{i:02}"] for i in range(1, 11)) / 10
REAL = [(n, r, ((1 + r / 100) / (1 + INF_AVG / 100) - 1) * 100) for n, r, _ in RATES]
MONTHS = [m for m in sorted(TG) if "2022-01" <= m <= M]
MX = np.array([int(m[:4]) + (int(m[5:]) - 0.5) / 12 for m in MONTHS])
TG_AVG_2425 = sum(TG[m] for m in TG if "2024-01" <= m <= "2025-12") / 24
LOCK_GAIN = 10000 * (1.0325 ** 2 - 1)
TG_GAIN = 10000 * ((1 + TG_AVG_2425 / 100) ** 2 - 1)
FREI_BIS = 1000 / (F3[M] / 100)

# Every number spoken in the narration is checked here.
assert (TG[M], F1[M], F2[M], F3[M], EZB["2026-09"]) == (0.52, 2.39, 2.78, 2.83, 2.5)
assert round(100 * TG[M]) == 52 and round(100 * F3[M]) == 283 and round(100 * F1[M]) == 239
assert round(INF_AVG, 2) == 2.63
assert [round(r, 1) for _, _, r in REAL] == [-2.1, -0.2, 0.1, 0.2]
assert F2["2022-01"] == 0.22 and F2["2023-12"] == 3.25 and 0.52 < TG_AVG_2425 < 0.53
assert round(LOCK_GAIN) == 661 and round(TG_GAIN) == 106
assert 35300 < FREI_BIS < 35400
assert F2["2023-01"] > 2 and round(F3[M] * (1 - 0.26375), 2) == 2.08

SRC = "Quelle: Deutsche Bundesbank, MFI-Zinsstatistik, Neugeschäft, private Haushalte · Sept. 2026 vorläufig"


def pct(v, dec=2, sign=False):
    s = f"{v:+.{dec}f}" if sign else f"{v:.{dec}f}"
    return s.replace("-", "−").replace(".", ",") + " %"


def draw_hook(img, d, t, S):
    hook_two(d, t, S, "10.000 € für ein Jahr", (1, "Tagesgeld & Giro, Ø", "+52 €", "0,52 % Zins", GRAY),
             (2, "Festgeld über 2 Jahre, Ø", "+283 €", "2,83 % Zins", GREEN),
             (3, "Festgeld oder Tagesgeld – und was bleibt nach Inflation?"), SRC)


def draw_zinsen(img, d, t, S):
    title(d, t, "Zinsen nach Laufzeit", S.c(0), "Durchschnittszinsen im September 2026")
    for i, (n, r, col) in enumerate(RATES):
        st = S.c(1) if i == 0 else S.c(2) + (i - 1) * 0.7
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 270 + i * 120
        text(d, (690, y + 40), n, 36, FG, a, "rm", "SemiBold")
        w = r * 250 * prog(t, st, 0.9, ease_in_out)
        d.rounded_rectangle((720, y + 10, 720 + max(w, 6), y + 70), 12, fill=fade(col, a))
        text(d, (735 + w, y + 40), pct(r), 40, col, a, "lm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        y = 270 + 4 * 120
        text(d, (690, y + 40), "EZB-Einlagesatz", 36, MUTED, a, "rm", "SemiBold")
        dd = 2.5 * 250
        d.rounded_rectangle((720, y + 10, 720 + dd, y + 70), 12, outline=fade(AMBER, a), width=3)
        text(d, (735 + dd, y + 40), "2,50 %", 40, AMBER, a, "lm", "Black")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · SUD101–SUD104, SU0200")


def draw_verlauf(img, d, t, S):
    title(d, t, "Wie sich die Zinsen entwickelt haben", S.c(0), "Monatswerte Januar 2022 bis September 2026")
    ch = Chart((260, 270, 1400, 860), (2022, 2026.8), (0, 4))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(2022, 2027), range(0, 5), lambda y: str(y), lambda v: f"{v} %")
    footer(d, ax, SRC)
    up = 2022 + 4.8 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 2022:
        for ser, col in ((TG, GRAY), (F1, BLUE), (F2, VIOLET), (F3, GREEN)):
            ch.line(d, MX, np.array([ser[m] for m in MONTHS]), col, 5, up)
    for i, (n, _, col) in enumerate(RATES):
        text(d, (1440, 330 + i * 60), n, 28, col, ax, "lm", "Bold")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        p = ch.px(2023.96, F2["2023-12"])
        dot(d, p, 10, VIOLET)
        text(d, (p[0], p[1] - 18), "Dez. 2023: 3,25 %", 28, VIOLET, a, "mb", "Black")


def draw_real(img, d, t, S):
    title(d, t, "Was nach Inflation bleibt", S.c(0), f"Inflation Ø Januar–Oktober 2026: {pct(INF_AVG)}")
    cols = [(290, "Anlage", "lm"), (1050, "Zins", "mm"), (1450, "real", "mm")]
    rows = [(S.c(1) + i * 0.6 if i < 2 else S.c(2) + (i - 2) * 0.6,
             [(n, FG), (pct(r), FG), (pct(rr, 1, sign=True), RED if rr < 0 else GREEN)], RED if rr < 0 else GREEN)
            for i, (n, r, rr) in enumerate(REAL)]
    table(d, t, rows, cols, y0=300)
    a = prog(t, S.c(3), 0.5)
    text(d, (250, 860), "Erst lange Laufzeiten gleichen die Inflation ungefähr aus – vor Steuern.", 36, AMBER, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Realzins = (1 + Zins) ÷ (1 + Inflation) − 1 · " + SRC)


def draw_bindung(img, d, t, S):
    title(d, t, "Der Haken an Festgeld: die Bindung", S.c(0), "Der Zins steht fest – egal, was danach passiert")
    for i, (st, head, lines, col) in enumerate(((S.c(1), "Glück: Dezember 2023", [("Festgeld 1–2 J.", "3,25 %"), ("10.000 € in 2 Jahren", "+" + eur(LOCK_GAIN)),
                                                                                    ("Tagesgeld Ø 2024/25", "+" + eur(TG_GAIN))], GREEN),
                                                (S.c(3), "Pech: Januar 2022", [("Festgeld 1–2 J.", "0,22 %"), ("ein Jahr später", "über 2 %"),
                                                                               ("Ende 2023", "3,25 %")], RED))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 270, x0 + 660, 720), a, col)
        text(d, (x0 + 40, 330), head, 38, FG, a, "lm", "Bold")
        for j, (lab, v) in enumerate(lines):
            y = 430 + j * 95
            text(d, (x0 + 40, y), lab, 32, MUTED, a, "lm", "SemiBold")
            text(d, (x0 + 620, y), v, 44, col if j < 2 else FG, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (250, 820), "Vorzeitig kündigen geht bei Festgeld meist nicht.", 36, AMBER, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · Modellrechnung")


def draw_steuer(img, d, t, S):
    title(d, t, "Steuer und Sicherheit", S.c(0))
    cards(d, t, [(S.c(1), "Zinsen bis 1.000 € im Jahr steuerfrei", f"bei 2,83 % reicht das für rund 35.300 € Guthaben (Sparerpauschbetrag)", GREEN),
                 (S.c(2), "Darüber: 26,375 % Abgeltungsteuer + Soli", "aus 2,83 % werden dann netto rund 2,08 %", RED),
                 (S.c(3), "Einlagensicherung", "bis 100.000 € pro Person und Bank gesetzlich geschützt", BLUE)], y0=250, h=170, gap=30)
    footer(d, prog(t, S.c(1), 0.5), "§ 20 Abs. 9, § 32d EStG · gesetzliche Einlagensicherung (EU-weit harmonisiert)")


def draw_grenzen(img, d, t, S):
    numbered(d, t, S, [(1, "Durchschnitte", "Einzelne Angebote liegen darüber oder darunter – Tagesgeld-Schnitt enthält Girokonten."),
                       (2, "Zinsen ändern sich", "Tagesgeldzinsen sind variabel, Festgeld gilt nur für Neuabschlüsse zum jeweiligen Zeitpunkt."),
                       (3, "Vorläufige Werte", "Die Daten für September 2026 sind noch vorläufig.")], "3 ehrliche Einschränkungen")


def draw_fazit(img, d, t, S):
    fazit(d, t, S, "Festgeld oder Tagesgeld?", [
        (1, GREEN, "Festgeld:", "mehr Zins, dafür ist das Geld gebunden"),
        (2, GRAY, "Tagesgeld:", "jederzeit verfügbar, im Schnitt aber kaum Zins"),
        (3, AMBER, "Nach Inflation:", "erst lange Laufzeiten kommen ungefähr auf null")])


def draw_outro(img, d, t, S):
    outro(d, t, S, ["Sondertilgung", "oder sparen?", "Die Tilgungs-Leiter"])


def scenes():
    return [
        Scene("hook", [
            "Zehntausend Euro, ein Jahr lang angelegt.",
            "Auf Tagesgeld und Girokonto bringen sie im Schnitt zweiundfünfzig Euro Zinsen.",
            "Als Festgeld über mehr als zwei Jahre im Schnitt zweihundertdreiundachtzig Euro.",
            "Wir rechnen nach, welche Laufzeit was bringt und was nach Inflation übrig bleibt. Mit den Zahlen der Bundesbank.",
        ], draw_hook),
        Scene("zinsen", [
            "So sahen die Durchschnittszinsen im September zweitausendsechsundzwanzig aus.",
            "Täglich verfügbares Geld, also Tagesgeld und Girokonten zusammen: null Komma fünf zwei Prozent.",
            "Festgeld bis ein Jahr: zwei Komma drei neun Prozent. Ein bis zwei Jahre: zwei Komma sieben acht. Über zwei Jahre: zwei Komma acht drei.",
            "Zum Vergleich: Die EZB zahlt Banken zwei Komma fünf Prozent.",
        ], draw_zinsen),
        Scene("verlauf", [
            "Wie haben sich diese Zinsen entwickelt?",
            "Anfang zweitausendzweiundzwanzig gab es fast nirgends Zinsen. Mit den Zinserhöhungen der EZB stieg Festgeld schnell.",
            "Tagesgeld und Girokonten blieben im Schnitt dagegen fast unten.",
            "Ende zweitausenddreiundzwanzig gab es für ein bis zwei Jahre Festgeld im Schnitt drei Komma zwei fünf Prozent.",
        ], draw_verlauf),
        Scene("real", [
            "Und nach Inflation? Von Januar bis Oktober zweitausendsechsundzwanzig lag sie im Schnitt bei zwei Komma sechs drei Prozent.",
            "Tagesgeld und Girokonto verlieren damit real rund zwei Prozent. Festgeld bis ein Jahr liegt knapp darunter, bei minus null Komma zwei.",
            "Festgeld mit ein bis zwei Jahren kommt auf plus null Komma eins, über zwei Jahre auf plus null Komma zwei Prozent.",
            "Erst lange Laufzeiten gleichen die Inflation also ungefähr aus, und das noch vor Steuern.",
        ], draw_real),
        Scene("bindung", [
            "Der Haken an Festgeld: Der Zins ist für die ganze Laufzeit festgelegt.",
            "Das kann sich lohnen. Wer im Dezember zweitausenddreiundzwanzig für zwei Jahre festgelegt hat, bekam im Schnitt drei Komma zwei fünf Prozent. Auf zehntausend Euro rund sechshunderteinundsechzig Euro in zwei Jahren.",
            "Mit dem durchschnittlichen Tagesgeld- und Girozins wären es nur rund hundertsechs Euro gewesen.",
            "Es kann aber auch schiefgehen: Im Januar zweitausendzweiundzwanzig gab es nur null Komma zwei zwei Prozent, ein Jahr später schon über zwei Prozent.",
            "Und vorzeitig kündigen geht bei Festgeld meist nicht.",
        ], draw_bindung),
        Scene("steuer", [
            "Noch zwei wichtige Punkte.",
            "Zinsen bis tausend Euro im Jahr bleiben steuerfrei. Bei zwei Komma acht drei Prozent reicht das für rund fünfunddreißigtausenddreihundert Euro Guthaben.",
            "Darüber fallen fünfundzwanzig Prozent Abgeltungsteuer plus Soli an. Aus zwei Komma acht drei Prozent werden dann netto rund zwei Komma null acht.",
            "Und Einlagen sind bis hunderttausend Euro pro Person und Bank gesetzlich gesichert.",
        ], draw_steuer),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Das sind Durchschnitte. Einzelne Angebote liegen darüber oder darunter, und im Tagesgeld-Schnitt stecken auch Girokonten.",
            "Zweitens: Tagesgeldzinsen sind variabel. Festgeldzinsen gelten nur für Neuabschlüsse zum jeweiligen Zeitpunkt.",
            "Drittens: Die Werte für September zweitausendsechsundzwanzig sind noch vorläufig.",
        ], draw_grenzen),
        Scene("fazit", [
            "Festgeld oder Tagesgeld?",
            "Festgeld bringt mehr Zins, dafür ist das Geld gebunden.",
            "Tagesgeld ist jederzeit verfügbar, bringt im Schnitt aber kaum Zinsen.",
            "Und nach Inflation kommen erst lange Laufzeiten ungefähr auf null.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung und keine Produktempfehlung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Werte und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video: Sondertilgung oder sparen? Wir bauen die Tilgungs-Leiter vom Dispo bis zum Baukredit.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
