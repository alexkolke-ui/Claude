"""Short 023 · Was kostet X: Baukredit Januar vs. September 2026 (aus Video 008)."""
from lib.engine import Scene
from lib.gfx import AMBER, GRAY, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v008_2026_in_zahlen.scenes import BAU, RATE, pct

assert BAU["2026-01"] == 3.58 and BAU["2026-09"] == 3.91
assert round(RATE(3.58), 2) == 1395.0 and round(RATE(3.91), 2) == 1477.5

draw = vergleich("300.000 € Baukredit", "10 Jahre Zinsbindung · 2 % Tilgung · Ø-Zinsen",
                 [(1, "Januar", GRAY, [("Bauzins", pct(BAU["2026-01"], 2), GRAY), ("Monatsrate", eur(RATE(3.58)), GRAY)]),
                  (2, "September", RED, [("Bauzins", pct(BAU["2026-09"], 2), RED), ("Monatsrate", eur(RATE(3.91), 2), RED)])],
                 (3, [("+82,50 € pro Monat", AMBER), ("in neun Monaten", None)]),
                 (4, "2026 in Zahlen: Video am 31.12."),
                 "Modellrechnung · Bundesbank SUD118 · Sept. 2026 vorläufig")


def scenes():
    return [Scene("short", [
        "Was hat ein Baukredit zweitausendsechsundzwanzig mehr gekostet?",
        "Dreihunderttausend Euro, zehn Jahre Zinsbindung, zwei Prozent Tilgung. Im Januar lag der Durchschnittszins bei drei Komma fünf acht Prozent: tausenddreihundertfünfundneunzig Euro im Monat.",
        "Im September waren es drei Komma neun eins Prozent: tausendvierhundertsiebenundsiebzig Euro fünfzig.",
        "Zweiundachtzig Euro fünfzig mehr pro Monat, innerhalb von nur neun Monaten.",
        "Den ganzen Jahresrückblick gibt es am einunddreißigsten Dezember auf dem Kanal.",
    ], draw, extra=1.0)]
