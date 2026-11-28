"""Short 001 (1080x1920): Anna vs. Ben – 10 Jahre früher anfangen (aus Video 001)."""
import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, FG, MUTED, VIOLET, Chart, card, dot, ease_in_out, eur, prog, text,
                     text_pop)
from videos.v001_zinseszins.scenes import AGES, A_CURVE, ANNA, B_CURVE, BEN, RATE, k

SIZE = (1080, 1920)
CX = 500   # visual centre, leaves room for the Shorts buttons on the right

PAID_A, PAID_B = RATE * 12 * 40, RATE * 12 * 30
assert PAID_A - PAID_B == 24000                      # "vierundzwanzigtausend Euro mehr"
assert 520000 < ANNA < 530000 and 243500 < BEN < 244500
assert ANNA / BEN > 2                                # "mehr als doppelt so viel"


def draw(img, d, t, S):
    text_pop(d, (CX, 250), "Anna vs. Ben", t, S.c(0), 84, FG, "mm", "Black")
    text(d, (CX, 318), "Modellrechnung · 7 % p. a. angenommen · keine Anlageberatung", 24, MUTED,
         prog(t, S.c(0) + 0.3, 0.5), "mm", "Medium")
    for x, name, sub, col, start in ((90, "Anna", "Start mit 25", VIOLET, S.c(0) + 0.4),
                                     (530, "Ben", "Start mit 35", AMBER, S.c(1))):
        a = prog(t, start, 0.5)
        if a > 0:
            card(d, (x, 365, x + 400, 465), a, col)
            dot(d, (x + 55, 418), 30, col)
            text(d, (x + 55, 419), name[0], 32, (13, 19, 33), a, "mm", "Black")
            text(d, (x + 105, 400), name, 34, FG, a, "lm", "Bold")
            text(d, (x + 105, 438), sub, 26, MUTED, a, "lm", "Medium")

    ch = Chart((180, 540, 880, 980), (25, 65), (0, 560000))
    ax = prog(t, S.c(2), 0.6)
    ch.axes(d, ax, range(25, 66, 10), range(0, 500001, 100000), str, k, "Alter")
    age = 25 + 40 * prog(t, S.c(4), S.e(5) - S.c(4), ease_in_out)
    if age > 25:
        ch.line(d, AGES, B_CURVE, AMBER, 8, age)
        ch.line(d, AGES, A_CURVE, VIOLET, 8, age)

    a3 = prog(t, S.c(3), 0.5)
    text(d, (CX, 1075), f"Eingezahlt: Anna {eur(PAID_A)} · Ben {eur(PAID_B)}", 28, MUTED, a3, "mm",
         "SemiBold")
    for x, name, val, col, start in ((90, "Anna mit 65", ANNA, VIOLET, S.c(4) + 1.0),
                                     (530, "Ben mit 65", BEN, AMBER, S.c(5) + 0.3)):
        a = prog(t, start, 0.5)
        if a > 0:
            card(d, (x, 1120, x + 400, 1250), a)
            text(d, (x + 200, 1158), name, 28, MUTED, a, "mm", "Medium")
            text(d, (x + 200, 1212), eur(val), 50, col, a, "mm", "Black")
    a6 = prog(t, S.c(6), 0.5) * (1 - prog(t, S.c(7), 0.4))
    text(d, (CX, 1340), f"{ANNA / BEN:.2f} ×".replace(".", ","), 96, FG, a6, "mm", "Black")
    text(d, (CX, 1410), "mehr Endvermögen – bei 24.000 € mehr Einzahlung", 28, MUTED, a6, "mm", "Medium")
    a7 = prog(t, S.c(7), 0.5)
    text(d, (CX, 1330), "Ganze Rechnung:", 44, FG, a7, "mm", "Bold")
    text(d, (CX, 1390), "Video auf dem Kanal", 44, AMBER, a7, "mm", "Black")


def scenes():
    return [Scene("short", [
        "Anna fängt mit fünfundzwanzig an, zweihundert Euro im Monat in einen ETF zu sparen.",
        "Ben macht genau dasselbe, aber erst ab fünfunddreißig.",
        "Beide sparen bis zur Rente mit fünfundsechzig.",
        "Anna zahlt also nur vierundzwanzigtausend Euro mehr ein.",
        "Bei angenommenen sieben Prozent pro Jahr hat Anna am Ende rund fünfhundertfünfundzwanzigtausend Euro.",
        "Ben: rund zweihundertvierundvierzigtausend.",
        "Zehn Jahre früher heißt hier: mehr als doppelt so viel.",
        "Die ganze Rechnung, mit allen Annahmen, findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
