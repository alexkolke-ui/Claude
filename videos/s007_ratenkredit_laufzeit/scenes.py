"""Short 007 (1080x1920), Format „Was kostet X wirklich?“: 10.000 € Ratenkredit, 3 vs. 7 Jahre (aus Video 004)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, card, ease_in_out, eur, lerp, prog, rrect, text, text_pop
from videos.v004_kredite.scenes import LOAN, RATEN_CASES, R_NOW, pct

SIZE = (1080, 1920)
CX = 500

(N1, RATE1, Z1), _, (N3, RATE3, Z3) = RATEN_CASES
assert LOAN == 10000 and R_NOW == 8.91 and (N1, N3) == (36, 84)
assert round(RATE1) == 316 and round(RATE3) == 159 and 1370 < Z1 < 1380 and 3325 < Z3 < 3335
assert 1950 < Z3 - Z1 < 1960 and Z3 / Z1 > 2.4


def draw(img, d, t, S):
    text_pop(d, (CX, 230), "Was kostet ein", t, S.c(0), 60, MUTED, "mm", "Bold")
    text_pop(d, (CX, 310), f"Kredit über {eur(LOAN)}?", t, S.c(0) + 0.2, 70, FG, "mm", "Black")
    text(d, (CX, 380), f"Ø effektiver Jahreszins {pct(R_NOW)} (Bundesbank, Sept. 2026)", 28, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")
    for start, x0, n, rate, z, col in ((S.c(1), 110, N1, RATE1, Z1, GREEN), (S.c(2), 510, N3, RATE3, Z3, RED)):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        card(d, (x0, 440, x0 + 380, 1000), a, col)
        cx = x0 + 190
        text(d, (cx, 510), f"{n // 12} Jahre", 52, FG, a, "mm", "Black")
        text(d, (cx, 600), "Monatsrate", 30, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 660), eur(rate), 58, FG, a, "mm", "Black")
        text(d, (cx, 760), "Zinsen gesamt", 30, MUTED, a, "mm", "SemiBold")
        p = prog(t, start + 0.4, 1.0, ease_in_out)
        text(d, (cx, 825), eur(lerp(0, z, p)), 58, col, a, "mm", "Black")
    a3 = prog(t, S.c(3), 0.5)
    text(d, (CX, 1100), "Kleinere Rate –", 50, FG, a3, "mm", "Black")
    text(d, (CX, 1170), f"≈ {eur(Z3 - Z1)} mehr Zinsen", 50, AMBER, a3, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1420), "Dispo & Baukredit: Video auf dem Kanal", 36, AMBER, a5, "mm", "Bold")
    text(d, (CX, 1465), "Modellrechnung: Annuität, gleicher Zins für beide Laufzeiten", 22, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Was kostet ein Kredit über zehntausend Euro wirklich?",
        "Zum durchschnittlichen effektiven Jahreszins von acht Komma neun eins Prozent zahlst du über drei Jahre rund dreihundertsechzehn Euro im Monat. Insgesamt rund tausenddreihundertfünfundsiebzig Euro Zinsen.",
        "Über sieben Jahre sinkt die Rate auf rund hundertneunundfünfzig Euro. Dafür zahlst du rund dreitausenddreihundertdreißig Euro Zinsen.",
        "Die kleinere Rate kostet also fast zweitausend Euro mehr.",
        "Gerechnet mit demselben Zinssatz für beide Laufzeiten.",
        "Was Dispo und Baukredit kosten, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
