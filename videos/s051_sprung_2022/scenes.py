"""Short 051 · Zahl der Woche: der Sprung auf 12 € im Oktober 2022 (aus Video 013)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED, eur
from lib.shorts import SIZE, zahl
from videos.v013_mindestlohn_2027.scenes import STUFEN

S = dict(STUFEN)
JUMP = S[2022.75] / S[2022.5] - 1
assert S[2022.5] == 10.45 and S[2022.75] == 12.00 and 0.148 < JUMP < 0.149

draw = zahl("+14,8 %", "auf einen Schlag", "Mindestlohn Oktober 2022: von 10,45 € auf 12,00 €",
            [(1, "Juli 2022", eur(10.45, 2), FG), ((1, 1.0), "Oktober 2022", eur(12.00, 2), GREEN),
             (2, "Inflation Okt. 2022", "8,8 %", RED)],
            (2, [("Größter Sprung", None), ("seit der Einführung", AMBER)]),
            (3, "Mindestlohn 2027: Video auf dem Kanal"), "MiLoG · Inflation: Verbraucherpreisindex (Destatis/Bundesbank)", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Plus vierzehn Komma acht Prozent, auf einen Schlag. So stark stieg der Mindestlohn im Oktober zweitausendzweiundzwanzig.",
        "Von zehn Euro fünfundvierzig auf zwölf Euro. Und zwar mitten in der höchsten Inflation, die lag damals bei acht Komma acht Prozent.",
        "Das war der größte Sprung seit der Einführung des Mindestlohns.",
        "Wie viel davon nach Inflation übrig ist, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=2.0)]
