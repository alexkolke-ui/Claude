"""Short 043 · Zahl der Woche: 259 € Kindergeld (aus Video 012)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v012_kindergeld_freibetrag.scenes import KG_JAHR, KG_MONAT, SUMME_18

assert KG_MONAT == 259 and KG_JAHR == 3108 and SUMME_18 == 55944

draw = zahl("259 €", "Kindergeld pro Monat", "2026, je Kind",
            [(1, "pro Jahr", eur(KG_JAHR), GREEN), (2, "bis zum 18. Geburtstag", eur(SUMME_18), GREEN)],
            (3, [("Oder Kinderfreibetrag?", None), ("Nur eins davon!", AMBER)]),
            (4, "Was sich lohnt: Video am 28. Januar"), "Kindergeld 2026 · beim heutigen Satz gerechnet", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Zweihundertneunundfünfzig Euro Kindergeld gibt es zweitausendsechsundzwanzig pro Kind und Monat.",
        "Das sind dreitausendeinhundertacht Euro im Jahr.",
        "Bis zum achtzehnten Geburtstag kommen beim heutigen Satz fünfundfünfzigtausendneunhundertvierundvierzig Euro zusammen.",
        "Aber es gibt auch den Kinderfreibetrag. Und du bekommst nur eins von beidem.",
        "Was sich lohnt, rechnen wir im Video am achtundzwanzigsten Januar durch.",
    ], draw, extra=1.5)]
