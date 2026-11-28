"""Short 024 · Zahl der Woche: Immobilienpreise 2026 (aus Video 008)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, RED
from lib.shorts import SIZE, zahl
from videos.v008_2026_in_zahlen.scenes import HPI_YOY, VDP, VDP_YOY, pct

BELOW = VDP["2026-Q3"] / VDP["2022-Q3"] - 1
assert 0.014 < VDP_YOY < 0.016 and 0.005 < HPI_YOY < 0.007 and -0.027 < BELOW < -0.026

draw = zahl("+1,5 %", "Preise für Wohneigentum", "3. Quartal 2026 zum Vorjahr (Index der Pfandbriefbanken)",
            [(1, "vdp-Index Q3 2026", pct(100 * VDP_YOY, sign=True), GREEN), ((1, 1.0), "Destatis Q2 2026", pct(100 * HPI_YOY, sign=True), BLUE),
             (2, "vs. Höchststand 2022", pct(100 * BELOW, sign=True), RED)],
            (3, [("Leicht steigend –", None), ("aber unter dem Hoch", RED)]),
            (4, "2026 in Zahlen: Video am 31.12."), "Quellen: vdp, Destatis, via Bundesbank-Indikatorensystem", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Plus eins Komma fünf Prozent. So viel teurer war selbst genutztes Wohneigentum im dritten Quartal zweitausendsechsundzwanzig als ein Jahr zuvor.",
        "Das zeigt der Index der Pfandbriefbanken. Der Häuserpreisindex des Statistischen Bundesamts meldet für das zweite Quartal plus null Komma sechs Prozent.",
        "Trotzdem liegen die Preise noch rund zweieinhalb Prozent unter dem Höchststand von zweitausendzweiundzwanzig.",
        "Die Preise steigen also leicht, aber vom alten Hoch sind sie noch entfernt.",
        "Den ganzen Jahresrückblick gibt es am einunddreißigsten Dezember auf dem Kanal.",
    ], draw, extra=1.0)]
