"""Short 006 (1080x1920), Format „Mythos vs. Rechnung“: 2,5 % Tagesgeld schlägt 2,2 % Inflation? (aus Video 003)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, card, eur, prog, rrect, text, text_pop
from lib.gfx import fade
from videos.v003_tagesgeld.scenes import (BIG, BIG_INT, BIG_NET_RATE, BIG_TAX, BREAKEVEN, EZB_LAST, INF_S, PAUSCH,
                                          TAX, pct)

SIZE = (1080, 1920)
CX = 500

assert EZB_LAST == 2.5 and INF_S == 2.2 and BIG == 100000 and BIG_INT == 2500 and PAUSCH == 1000
assert 390 < BIG_TAX < 400 and 2.09 < BIG_NET_RATE < 2.12 < 2.2 and 2.9 < BREAKEVEN < 3.0
assert 26.35 < 100 * TAX < 26.4


def draw(img, d, t, S):
    a0 = prog(t, S.c(0), 0.5)
    if a0 > 0:
        rrect(d, (110, 200, 890, 270), 35, fill=fade((50, 26, 30), a0), outline=fade(RED, a0 * 0.7), width=2)
        text(d, (CX, 236), "MYTHOS", 34, RED, a0, "mm", "Black")
    text_pop(d, (CX, 340), f"{pct(EZB_LAST)} Zins schlägt", t, S.c(0) + 0.2, 64, FG, "mm", "Black")
    text_pop(d, (CX, 415), f"{pct(INF_S)} Inflation?", t, S.c(0) + 0.4, 64, FG, "mm", "Black")
    a1 = prog(t, S.c(1), 0.5)
    if a1 > 0:
        rrect(d, (110, 500, 890, 570), 35, fill=fade((24, 48, 40), a1), outline=fade(GREEN, a1 * 0.7), width=2)
        text(d, (CX, 536), "RECHNUNG", 34, GREEN, a1, "mm", "Black")
    a2 = prog(t, S.c(2), 0.5)
    if a2 > 0:
        card(d, (110, 620, 890, 1080), a2, AMBER)
        text(d, (150, 680), f"{eur(BIG)} zu {pct(EZB_LAST)}", 40, FG, a2, "lm", "Bold")
        rows = [("Zinsen", "+" + eur(BIG_INT), FG, S.c(2) + 0.4),
                ("davon steuerfrei", eur(PAUSCH), MUTED, S.c(3)),
                ("Steuer 26,375 %", "−" + eur(BIG_TAX), RED, S.c(3) + 1.2),
                ("Nettozins", pct(BIG_NET_RATE, 2), AMBER, S.c(4))]
        for j, (lab, val, col, st) in enumerate(rows):
            b = prog(t, st, 0.5)
            y = 770 + j * 80
            text(d, (150, y), lab, 36, MUTED, b, "lm", "SemiBold")
            text(d, (850, y), val, 46, col, b, "rm", "Black")
    a4 = prog(t, S.c(4) + 0.8, 0.5)
    text(d, (CX, 1150), f"{pct(BIG_NET_RATE, 2)} < {pct(INF_S)} → real im Minus", 44, RED, a4, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1240), f"Nötig: knapp {pct(BREAKEVEN, 0)} Zins", 48, AMBER, a5, "mm", "Black")
    a6 = prog(t, S.c(6), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a6, "mm", "Bold")
    text(d, (CX, 1465), "Modellrechnung · ohne Kirchensteuer · keine Steuerberatung", 22, MUTED,
         prog(t, S.c(2), 0.5), "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Zwei Komma fünf Prozent Zinsen, zwei Komma zwei Prozent Inflation. Also ein Plus? Nicht unbedingt.",
        "Rechnen wir nach.",
        "Hunderttausend Euro zu zwei Komma fünf Prozent bringen zweitausendfünfhundert Euro Zinsen.",
        "Tausend Euro davon sind über den Sparerpauschbetrag steuerfrei. Auf den Rest fallen rund vierhundert Euro Steuer an.",
        "Netto bleiben zwei Komma eins Prozent. Weniger als die Inflation.",
        "Wer über dem Pauschbetrag liegt, braucht bei zwei Komma zwei Prozent Inflation knapp drei Prozent Zins, um real nicht zu verlieren.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
