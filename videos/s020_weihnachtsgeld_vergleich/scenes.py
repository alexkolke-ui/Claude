"""Short 020 · Vergleich: Weihnachtsgeld netto bei 2.500 € und 5.000 € (aus Video 007)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GREEN, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v007_weihnachtsgeld.scenes import CASES, Q

(b1, z1, m1), _, (b3, z3, m3), _ = CASES
assert (b1, b3) == (2500, 5000) and round(z1["Netto"]) == 1437 and round(z3["Netto"]) == 2530
assert round(Q(z1["Netto"], b1), 1) == 57.5 and round(Q(z3["Netto"], b3), 1) == 50.6
assert round(Q(m1["Netto"], b1), 1) == 70.8 and round(Q(m3["Netto"], b3), 1) == 62.6

p = lambda v: f"{v:.1f} %".replace(".", ",")
draw = vergleich("Weihnachtsgeld netto", "Ein volles Monatsgehalt · Steuerklasse I · 2026",
                 [(1, eur(b1), GREEN, [("Weihnachtsgeld netto", eur(z1["Netto"]), GREEN), ("bleibt", p(Q(z1["Netto"], b1)), GREEN),
                                       ("vom Gehalt bleibt", p(Q(m1["Netto"], b1)), BLUE)]),
                  (2, eur(b3), RED, [("Weihnachtsgeld netto", eur(z3["Netto"]), GREEN), ("bleibt", p(Q(z3["Netto"], b3)), RED),
                                     ("vom Gehalt bleibt", p(Q(m3["Netto"], b3)), BLUE)])],
                 (3, [("Je höher das Gehalt,", None), ("desto weniger bleibt", AMBER)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"),
                 "BMF-Programmablaufplan Lohnsteuer 2026 · kinderlos, ohne Kirchensteuer")


def scenes():
    return [Scene("short", [
        "Wie viel bleibt vom Weihnachtsgeld, wenn es ein volles Monatsgehalt ist?",
        "Bei zweitausendfünfhundert Euro Gehalt bleiben netto rund tausendvierhundertsiebenunddreißig Euro, also siebenundfünfzig Komma fünf Prozent. Vom normalen Gehalt sind es siebzig Komma acht Prozent.",
        "Bei fünftausend Euro bleiben rund zweitausendfünfhundertdreißig Euro, nur fünfzig Komma sechs Prozent. Vom Gehalt zweiundsechzig Komma sechs.",
        "Je höher das Gehalt, desto höher der Steuersatz auf den obersten Euro, und desto weniger bleibt vom Weihnachtsgeld.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
