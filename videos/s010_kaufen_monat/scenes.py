"""Short 010 · Was kostet X: Wohnung mit 1.000 € Miete kaufen statt mieten (aus Video 005)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, RED, VIOLET, eur
from lib.shorts import SIZE, vergleich
from videos.v005_mieten_kaufen.scenes import INST_M, INT_M1, LOST_M1, OPP_M1, RENT_M, TILG_M1

assert RENT_M == 1000 and round(INT_M1) == 816 and INST_M == 261 and round(OPP_M1) == 196
assert round(LOST_M1) == 1273 and round(TILG_M1) == 418

draw = vergleich("Mieten oder kaufen?", "Wohnung mit 1.000 € Kaltmiete · erster Monat",
                 [(1, "Mieten", GREEN, [("Kaltmiete", eur(RENT_M), FG), ("", "", FG), ("weg pro Monat", eur(RENT_M), GREEN)]),
                  (2, "Kaufen", RED, [("Zinsen", eur(INT_M1), RED), ("Rücklage", eur(INST_M), AMBER),
                                      ("entgangene Zinsen", eur(OPP_M1), VIOLET)])],
                 (3, [(f"Kaufen: ≈ {eur(LOST_M1)} weg", RED), (f"+ {eur(TILG_M1)} Tilgung = Vermögen", BLUE)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"),
                 "Modellrechnung · Faktor 26,1 · Bauzins 3,91 % · Annahmen in der Beschreibung")


def scenes():
    return [Scene("short", [
        "Eine Wohnung, die tausend Euro Kaltmiete kosten würde. Was ist im Monat wirklich weg, wenn du sie mietest oder kaufst?",
        "Beim Mieten: tausend Euro.",
        "Beim Kaufen zum Durchschnittspreis: rund achthundertsechzehn Euro Zinsen, zweihunderteinundsechzig Euro Rücklage für Reparaturen und rund hundertsechsundneunzig Euro Zinsen, die dein Eigenkapital sonst bringen könnte.",
        "Zusammen rund zwölfhundertdreiundsiebzig Euro. Dazu kommen rund vierhundertachtzehn Euro Tilgung, aber die sind Vermögen, nicht weg.",
        "Ab wann sich Kaufen lohnt, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=1.0)]
