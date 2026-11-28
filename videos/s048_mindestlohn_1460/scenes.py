"""Short 048 · Zahl der Woche: Mindestlohn 14,60 € (aus Video 013)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v013_mindestlohn_2027.scenes import B27, ML26, ML27

assert (ML26, ML27, B27) == (13.90, 14.60, 2530.67)

draw = zahl("14,60 €", "Mindestlohn pro Stunde", "seit 1. Januar 2027",
            [(1, "2026", eur(ML26, 2), FG), ((1, 1.0), "2015", eur(8.50, 2), FG), (2, "Vollzeit, 40 h/Woche", eur(B27, 2), BLUE)],
            None, (3, "Was netto bleibt: Video am 4. Februar"), "Mindestlohnkommission, Beschluss 27.06.2025", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Vierzehn Euro sechzig. So hoch ist der gesetzliche Mindestlohn seit dem ersten Januar zweitausendsiebenundzwanzig.",
        "Zweitausendsechsundzwanzig waren es dreizehn Euro neunzig, bei der Einführung zweitausendfünfzehn acht Euro fünfzig.",
        "Bei Vollzeit mit vierzig Stunden pro Woche sind das zweitausendfünfhundertdreißig Euro siebenundsechzig brutto im Monat.",
        "Was davon netto bleibt, rechnen wir im Video am vierten Februar durch.",
    ], draw, extra=2.0)]
