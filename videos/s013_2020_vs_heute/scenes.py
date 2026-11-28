"""Short 013 · Vergleich: Mietrendite vs. Bauzins 2020 und heute (aus Video 005)."""
from lib.engine import Scene
from lib.gfx import AMBER, GREEN, RED
from lib.shorts import SIZE, vergleich
from videos.v005_mieten_kaufen.scenes import BAUZ, BAUZ_NOW, YIELD, pct

assert 3.5 < YIELD[2020] < 3.52 and 1.08 < BAUZ[2020] < 1.1
assert 3.8 < YIELD[2025] < 3.85 and BAUZ_NOW == 3.91

draw = vergleich("Kaufen: 2020 vs. heute", "Was die Wohnung an Miete bringt vs. was der Kredit kostet",
                 [(1, "2020", GREEN, [("Mietrendite", pct(YIELD[2020]), AMBER), ("Bauzins", pct(BAUZ[2020]), GREEN),
                                       ("Abstand", "+2,4 Pkt.", GREEN)]),
                  (3, "heute", RED, [("Mietrendite", pct(YIELD[2025]), AMBER), ("Bauzins", pct(BAUZ_NOW, 2), RED),
                                     ("Abstand", "≈ 0", RED)])],
                 (4, [("Der Kredit-Vorteil", None), ("ist verschwunden", RED)]),
                 (5, "Mieten oder kaufen? Video auf dem Kanal"),
                 "Bundesbank: Kaufpreis/Jahresmiete (Mietrendite 2025), Bauzins SUD118 (Sept. 2026)")


def scenes():
    return [Scene("short", [
        "Warum war Kaufen zweitausendzwanzig so attraktiv und heute nicht mehr?",
        "Zweitausendzwanzig brachte eine Wohnung im Schnitt drei Komma fünf Prozent Miete pro Jahr.",
        "Der Bauzins lag aber nur bei rund eins Komma eins Prozent. Der Kredit war also viel billiger als die Miete, die man spart.",
        "Heute liegt die Mietrendite bei drei Komma acht Prozent, der Bauzins bei drei Komma neun eins.",
        "Der Vorteil durch billige Kredite ist praktisch verschwunden.",
        "Was das für die Entscheidung heißt, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
