"""Short 008 (1080x1920), Format „Zahl der Woche“: +722 € pro Monat beim Baukredit (aus Video 004)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, card, ease_in_out, eur, lerp, prog, text, text_pop
from videos.v004_kredite.scenes import B10_LOW, B10_NOW, BAU_LOW, BAU_NOW, HOUSE, pct

SIZE = (1080, 1920)
CX = 500

DIFF = BAU_NOW[0] - BAU_LOW[0]
assert HOUSE == 300000 and B10_NOW == 3.91 and B10_LOW == 1.02
assert BAU_NOW[0] == 1477.5 and BAU_LOW[0] == 755.0 and 720 < DIFF < 725
assert 103500 < BAU_NOW[2] < 104500 and 27000 < BAU_LOW[2] < 28000


def draw(img, d, t, S):
    text_pop(d, (CX, 230), "ZAHL DER WOCHE", t, S.c(0), 36, AMBER, "mm", "Black", rise=10)
    p = prog(t, S.c(0) + 0.3, 1.5, ease_in_out)
    text_pop(d, (CX, 380), "+" + eur(lerp(0, DIFF, p)), t, S.c(0) + 0.3, 150, AMBER, "mm", "Black")
    text_pop(d, (CX, 480), "pro Monat – nur durch den Zins", t, S.c(0) + 0.6, 42, FG, "mm", "Bold")
    text(d, (CX, 560), f"Baukredit {eur(HOUSE)} · 10 Jahre Zinsbindung · 2 % Tilgung", 28, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")
    for start, y, lab, z, (rate, _, paid), col in ((S.c(1) + 0.4, 630, "Dezember 2020", B10_LOW, BAU_LOW, GREEN),
                                                    (S.c(2), 920, "September 2026", B10_NOW, BAU_NOW, RED)):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        card(d, (110, y, 890, y + 250), a, col)
        text(d, (150, y + 60), lab, 38, FG, a, "lm", "Bold")
        text(d, (850, y + 60), pct(z), 42, col, a, "rm", "Black")
        text(d, (150, y + 140), "Monatsrate", 32, MUTED, a, "lm", "SemiBold")
        text(d, (850, y + 140), eur(rate, 2), 46, FG, a, "rm", "Black")
        text(d, (150, y + 205), "Zinsen in 10 Jahren", 32, MUTED, a, "lm", "SemiBold")
        text(d, (850, y + 205), "≈ " + eur(round(paid, -2)), 46, col, a, "rm", "Black")
    a4 = prog(t, S.c(4), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a4, "mm", "Bold")
    text(d, (CX, 1465), "Ø-Zinsen Bundesbank SUD118 · Modellrechnung ohne Nebenkosten", 22, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Siebenhundertzweiundzwanzig Euro. So viel mehr kostet ein Baukredit heute im Monat als Ende zweitausendzwanzig.",
        "Dreihunderttausend Euro, zehn Jahre Zinsbindung, zwei Prozent Tilgung. Im Dezember zweitausendzwanzig lag der Durchschnittszins bei eins Komma null zwei Prozent: siebenhundertfünfundfünfzig Euro Rate.",
        "Heute sind es drei Komma neun eins Prozent: eintausendvierhundertsiebenundsiebzig Euro fünfzig im Monat.",
        "In zehn Jahren zahlst du damit rund hundertviertausend Euro Zinsen statt rund siebenundzwanzigtausendfünfhundert.",
        "Die ganze Rechnung mit Dispo und Ratenkredit findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
