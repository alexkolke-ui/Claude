"""Short 022 · Was kostet X: Was 100 € von Oktober 2025 ein Jahr später noch wert sind (aus Video 008)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, RED, eur
from lib.shorts import SIZE, zahl
from videos.v008_2026_in_zahlen.scenes import INF, VPI

COST = 100 * VPI["2026-10"] / VPI["2025-10"]
VALUE = 100 * VPI["2025-10"] / VPI["2026-10"]
assert VPI["2025-10"] == 123.0 and VPI["2026-10"] == 126.5 and INF["2026-10"] == 2.8
assert round(COST, 2) == 102.85 and round(VALUE, 2) == 97.23

draw = zahl(eur(VALUE, 2), "sind 100 € von Oktober 2025 noch wert", "Kaufkraft im Oktober 2026, gemessen am Verbraucherpreisindex",
            [(1, "Preisindex Okt. 2025", "123,0", FG), ((1, 1.0), "Preisindex Okt. 2026", "126,5", FG),
             (2, "Einkauf von 100 € kostet jetzt", eur(COST, 2), RED)],
            (3, [("Ohne Zinsen:", None), ("fast 3 € weniger wert", RED)]),
            (4, "2026 in Zahlen: Video am 31.12."), "Quelle: VPI 2020 = 100 (Bundesbank BBDP1, Destatis)")


def scenes():
    return [Scene("short", [
        "Was sind hundert Euro vom Oktober zweitausendfünfundzwanzig ein Jahr später noch wert?",
        "Der Verbraucherpreisindex stieg in dieser Zeit von hundertdreiundzwanzig auf hundertsechsundzwanzig Komma fünf.",
        "Ein Einkauf, der damals hundert Euro gekostet hat, kostet jetzt rund hundertzwei Euro fünfundachtzig.",
        "Deine hundert Euro sind also nur noch rund siebenundneunzig Euro dreiundzwanzig wert, wenn sie ohne Zinsen herumliegen.",
        "Den ganzen Jahresrückblick gibt es am einunddreißigsten Dezember auf dem Kanal.",
    ], draw, extra=2.0)]
