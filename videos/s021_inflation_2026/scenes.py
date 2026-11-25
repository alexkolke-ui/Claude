"""Short 021 · Zahl der Woche: Inflation 2026 (aus Video 008)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GRAY, RED
from lib.shorts import SIZE, zahl
from videos.v008_2026_in_zahlen.scenes import INF, INF_AVG, pct

assert 2.6 < INF_AVG < 2.65 and INF["2026-02"] == 1.9 and INF["2026-09"] == 3.3 and INF["2026-10"] == 2.8

draw = zahl("2,6 %", "Inflation 2026 im Schnitt", "Januar bis Oktober 2026, Verbraucherpreise zum Vorjahresmonat",
            [(1, "Tiefster Wert: Februar", pct(INF["2026-02"]), BLUE), ((1, 1.2), "Höchster Wert: September", pct(INF["2026-09"]), RED),
             (2, "Oktober", pct(INF["2026-10"]), AMBER), ((2, 1.0), "2025 im Jahresschnitt", "2,2 %", GRAY)],
            (3, [("Preise steigen wieder", None), ("etwas schneller", RED)]),
            (4, "2026 in Zahlen: Video am 31.12."), "Quelle: Verbraucherpreisindex (Bundesbank BBDP1, Destatis)", big_color=RED)


def scenes():
    return [Scene("short", [
        "Zwei Komma sechs Prozent. So hoch war die Inflation zweitausendsechsundzwanzig von Januar bis Oktober im Schnitt.",
        "Der tiefste Wert kam im Februar mit eins Komma neun Prozent, der höchste im September mit drei Komma drei.",
        "Im Oktober lag sie bei zwei Komma acht Prozent. Zweitausendfünfundzwanzig waren es im Jahresschnitt zwei Komma zwei.",
        "Die Preise steigen also wieder etwas schneller.",
        "Den ganzen Jahresrückblick gibt es am einunddreißigsten Dezember auf dem Kanal.",
    ], draw, extra=2.0)]
