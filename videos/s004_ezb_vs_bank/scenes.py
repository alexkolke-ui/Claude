"""Short 004 (1080x1920): EZB 4 %, bei Sparern 0,62 % (aus Video 003, Bundesbank-Daten)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, MUTED, VIOLET, card, ease_in_out, prog, rrect, text, text_pop
from videos.v003_tagesgeld.scenes import EZB, EZB_LAST, Z_NOW, Z_PEAK, Z_PEAK_M, ZINS, pct

SIZE = (1080, 1920)
CX = 500

assert EZB["2024-01"] == 4.0 and Z_PEAK == 0.62 and Z_PEAK_M == "2024-01"
assert Z_PEAK / EZB["2024-01"] < 1 / 6
assert EZB_LAST == 2.5 and Z_NOW == 0.52 and ZINS["2026-09"] == Z_NOW


def bars(d, t, y, label, ezb, bank, start):
    a = prog(t, start, 0.5)
    if a <= 0:
        return
    card(d, (90, y, 910, y + 420), a)
    text(d, (130, y + 55), label, 40, FG, a, "lm", "Black")
    scale = 520 / 4.0
    for i, (name, val, col) in enumerate((("EZB", ezb, VIOLET), ("Sparer (Ø)", bank, BLUE))):
        yy = y + 130 + i * 140
        p = prog(t, start + 0.3 + i * 0.6, 0.9, ease_in_out)
        text(d, (130, yy), name, 32, MUTED, a, "lm", "SemiBold")
        w = max(6, val * scale * p)
        rrect(d, (130, yy + 30, 130 + w, yy + 90), 12, fill=col)
        text(d, (130 + w + 16, yy + 60), pct(val * p, 2), 44, col, a, "lm", "Black")


def draw(img, d, t, S):
    text_pop(d, (CX, 250), "EZB-Zins vs. dein Zins", t, S.c(0), 76, FG, "mm", "Black")
    text_pop(d, (CX, 322), "Einlagesatz der EZB vs. Ø-Zins auf Tagesgeld & Giro", t, S.c(0) + 0.3, 30, MUTED,
             "mm", "SemiBold")
    bars(d, t, 400, "Januar 2024", EZB["2024-01"], Z_PEAK, S.c(1))
    a = prog(t, S.c(2) + 0.5, 0.5)
    text(d, (CX, 870), "Weitergegeben: weniger als 1/6", 44, AMBER, a, "mm", "Black")
    bars(d, t, 940, "September 2026", EZB_LAST, Z_NOW, S.c(3))
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a5, "mm", "Bold")
    text(d, (CX, 1465), "Quelle: Deutsche Bundesbank (SU0200, SUD101)", 22, MUTED, prog(t, S.c(1), 0.5),
         "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Die EZB hat die Zinsen auf vier Prozent erhöht. Wie viel davon kam bei Sparern an?",
        "Banken bekamen im Januar zweitausendvierundzwanzig vier Prozent, wenn sie Geld bei der EZB geparkt haben.",
        "Auf täglich verfügbares Geld zahlten sie ihren Kunden im Schnitt null Komma sechs zwei Prozent. Nicht einmal ein Sechstel.",
        "Und heute? Die EZB zahlt zwei Komma fünf Prozent.",
        "Sparer bekommen im Schnitt null Komma fünf zwei Prozent.",
        "Warum das so ist und was es für dein Geld bedeutet, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
