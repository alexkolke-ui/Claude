"""Short 003 (1080x1920): 10.000 € seit 2015 auf dem Konto (aus Video 003, Bundesbank-Daten)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, MUTED, RED, Chart, card, ease_in_out, eur, fade, prog, text, text_pop
from videos.v003_tagesgeld.scenes import CAP, KAUF, MX, PRICE_UP, pct

SIZE = (1080, 1920)
CX = 500

assert 10150 < CAP[-1] < 10250 and 7450 < KAUF[-1] < 7550 and 0.355 < PRICE_UP < 0.365
assert 0.24 < 1 - KAUF[-1] / 10000 < 0.26


def draw(img, d, t, S):
    text_pop(d, (CX, 250), "10.000 € seit 2015", t, S.c(0), 80, FG, "mm", "Black")
    text_pop(d, (CX, 325), "auf dem Konto, zum Durchschnittszins", t, S.c(0) + 0.3, 36, MUTED, "mm", "SemiBold")
    ch = Chart((190, 420, 900, 850), (2015, 2026.9), (7000, 10600))
    ax = prog(t, S.c(1), 0.6)
    ch.axes(d, ax, (2015, 2020, 2025), (7000, 8000, 9000, 10000), str, lambda v: f"{v // 1000}.000")
    u1 = 2015 + (MX[-1] - 2015) * prog(t, S.c(1) + 0.3, S.e(1) - S.c(1), ease_in_out)
    if u1 > 2015:
        ch.line(d, MX, CAP, BLUE, 7, u1)
    u2 = 2015 + (MX[-1] - 2015) * prog(t, S.c(3), S.e(3) - S.c(3), ease_in_out)
    if u2 > 2015:
        ch.band(d, MX, CAP, KAUF, fade(RED, 0.25), u2)
        ch.line(d, MX, CAP, BLUE, 7, u1)
        ch.line(d, MX, KAUF, AMBER, 7, u2)
    for start, y, lab, val, col in ((S.c(1) + 0.8, 1010, "Kontostand 2026", CAP[-1], BLUE),
                                    (S.c(3) + 0.8, 1160, "Kaufkraft 2026", KAUF[-1], AMBER)):
        a = prog(t, start, 0.5)
        if a > 0:
            card(d, (110, y, 890, y + 130), a, col)
            text(d, (150, y + 70), lab, 38, MUTED, a, "lm", "SemiBold")
            text(d, (860, y + 70), "≈ " + eur(round(val, -1)), 56, col, a, "rm", "Black")
    a2 = prog(t, S.c(2), 0.5)
    text(d, (CX, 950), f"Preise seit 2015: {pct(100 * PRICE_UP, 0, sign=True)}", 40, RED, a2, "mm", "Bold")
    a4 = prog(t, S.c(4), 0.5)
    text(d, (CX, 1350), "Ein Viertel der Kaufkraft weg", 48, FG, a4, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a5, "mm", "Bold")
    text(d, (CX, 1465), "Daten: Bundesbank (SUD101, VPI) · Modellrechnung", 22, MUTED, ax, "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Was ist aus zehntausend Euro geworden, die seit zweitausendfünfzehn auf dem Konto liegen?",
        "Zum Durchschnittszins der Banken wären daraus bis September zweitausendsechsundzwanzig rund zehntausendzweihundert Euro geworden.",
        "Die Preise sind im selben Zeitraum aber um sechsunddreißig Prozent gestiegen.",
        "Gemessen an den Preisen von damals sind die zehntausend Euro nur noch rund siebentausendfünfhundert Euro wert.",
        "Ein Viertel der Kaufkraft ist weg, obwohl auf dem Konto mehr steht.",
        "Die ganze Rechnung mit allen Daten findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
