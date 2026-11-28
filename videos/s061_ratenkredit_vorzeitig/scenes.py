"""Short 061 · Was kostet X: Ratenkredit vorzeitig zurückzahlen (aus Video 015)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED, eur
from lib.shorts import SIZE, zahl

draw = zahl("max. 1 %", "darf die Bank fürs vorzeitige Tilgen verlangen", "Ratenkredit (Verbraucherdarlehen), § 502 BGB",
            [(1, "Restlaufzeit über 1 Jahr", "max. 1 %", FG), ((1, 1.0), "Restlaufzeit unter 1 Jahr", "max. 0,5 %", FG),
             (2, "bei 10.000 € Restschuld", "max. " + eur(100), RED), (3, "Zinsen bei 8,91 % (1 Jahr)", "≈ " + eur(891), GREEN)],
            (4, [("Vorzeitig tilgen", None), ("ist jederzeit möglich", AMBER)]),
            (5, "Tilgungs-Leiter: Video auf dem Kanal"), "§ 500, § 502 BGB · Ø-Zins Bundesbank SUD130 · vereinfacht")


def scenes():
    return [Scene("short", [
        "Was kostet es, einen Ratenkredit vorzeitig zurückzuzahlen?",
        "Die Bank darf höchstens ein Prozent der Restschuld verlangen. Bei weniger als einem Jahr Restlaufzeit höchstens ein halbes Prozent.",
        "Bei zehntausend Euro Restschuld sind das maximal hundert Euro.",
        "Zum Vergleich: Beim durchschnittlichen Zins von acht Komma neun eins Prozent kosten zehntausend Euro in einem Jahr rund achthunderteinundneunzig Euro Zinsen.",
        "Und vorzeitig zurückzahlen darfst du einen Ratenkredit jederzeit.",
        "Mehr dazu im Video auf dem Kanal.",
    ], draw, extra=1.0)]
