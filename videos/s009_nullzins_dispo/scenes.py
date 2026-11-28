"""Short 009 (1080x1920), Format „Mythos vs. Rechnung“: Nullzinsen = billiger Dispo? (aus Video 004)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, VIOLET, card, ease_in_out, fade, lerp, prog, rrect, text, text_pop
from videos.v004_kredite.scenes import DISPO, EZB, SPREAD_21, pct

SIZE = (1080, 1920)
CX = 500

assert EZB["2021-07"] == -0.5 and DISPO["2021-07"] == 6.9
assert EZB["2026-09"] == 2.5 and DISPO["2026-09"] == 9.59
assert 6.5 < min(SPREAD_21) and max(SPREAD_21) < 7.8


def pair(d, t, y, label, ezb, dispo, start):
    a = prog(t, start, 0.5)
    if a <= 0:
        return
    card(d, (110, y, 890, y + 300), a)
    text(d, (150, y + 55), label, 40, FG, a, "lm", "Black")
    for i, (name, val, col) in enumerate((("EZB-Einlagesatz", ezb, VIOLET), ("Dispo (Ø)", dispo, RED))):
        p = prog(t, start + 0.3 + i * 0.5, 0.9, ease_in_out)
        yy = y + 140 + i * 95
        text(d, (150, yy), name, 36, MUTED, a, "lm", "SemiBold")
        text(d, (850, yy), pct(lerp(0, val, p), 2 if val > 5 else 1), 54, col, a, "rm", "Black")


def draw(img, d, t, S):
    a0 = prog(t, S.c(0), 0.5)
    if a0 > 0:
        rrect(d, (110, 200, 890, 270), 35, fill=fade((50, 26, 30), a0), outline=fade(RED, a0 * 0.7), width=2)
        text(d, (CX, 236), "MYTHOS", 34, RED, a0, "mm", "Black")
    text_pop(d, (CX, 340), "Nullzinsen =", t, S.c(0) + 0.2, 64, FG, "mm", "Black")
    text_pop(d, (CX, 415), "billiger Dispo?", t, S.c(0) + 0.4, 64, FG, "mm", "Black")
    pair(d, t, 490, "Juli 2021", EZB["2021-07"], DISPO["2021-07"], S.c(1))
    pair(d, t, 830, "September 2026", EZB["2026-09"], DISPO["2026-09"], S.c(3))
    a2 = prog(t, S.c(2) + 0.6, 0.5)
    if a2 > 0:
        rrect(d, (110, 1160, 890, 1240), 40, fill=fade((24, 48, 40), a2), outline=fade(GREEN, a2 * 0.7), width=2)
        text(d, (CX, 1200), "Abstand seit 2021: 6,5 bis 7,8 Punkte", 36, GREEN, a2, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a5, "mm", "Bold")
    text(d, (CX, 1465), "Quelle: Deutsche Bundesbank (SU0200, SUD112)", 22, MUTED, prog(t, S.c(1), 0.5),
         "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Wenn die Zinsen bei null sind, ist doch auch der Dispo billig. Oder?",
        "Im Juli zweitausendeinundzwanzig lag der Einlagesatz der EZB bei minus null Komma fünf Prozent. Der Dispo kostete im Schnitt trotzdem sechs Komma neun Prozent.",
        "Seit zweitausendeinundzwanzig lag der Dispo jeden Monat sechseinhalb bis knapp acht Prozentpunkte über dem EZB-Satz.",
        "Heute: EZB zwei Komma fünf Prozent.",
        "Dispo im Schnitt neun Komma fünf neun Prozent.",
        "Was Kredite sonst noch kosten, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
