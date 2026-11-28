"""Short 035 · Mythos: 48 % Rentenniveau = fast der halbe Lohn (aus Video 010)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, eur
from lib.shorts import SIZE, mythos
from videos.v010_gesetzliche_rente.scenes import AVG_M, STD

assert round(STD, 2) == 1913.40 and round(AVG_M, 2) == 4328.67 and 0.44 < STD / AVG_M < 0.445

draw = mythos(["„48 % Rentenniveau heißt:", "Ich bekomme fast die Hälfte.“"],
              [(2, "Standardrente (45 J.)", eur(STD, 2), BLUE), ((2, 1.2), "Ø-Bruttoverdienst", eur(AVG_M, 2), GRAY),
               (3, "brutto gerechnet", "44,2 %", AMBER)],
              (4, [("Nur mit 45 Jahren", None), ("Durchschnittsgehalt", AMBER)]),
              (5, "Gesetzliche Rente: Video auf dem Kanal"), "DRV: Rentenniveau vor Steuern 48 % · Werte 2026")


def scenes():
    return [Scene("short", [
        "Achtundvierzig Prozent Rentenniveau. Heißt das, ich bekomme fast die Hälfte meines Gehalts als Rente?",
        "Nein. Das Rentenniveau gilt für einen ganz bestimmten Fall.",
        "Die Standardrente nach fünfundvierzig Jahren mit Durchschnittsverdienst beträgt tausendneunhundertdreizehn Euro. Der durchschnittliche Bruttoverdienst liegt bei rund viertausenddreihundertneunundzwanzig Euro.",
        "Brutto gerechnet sind das vierundvierzig Komma zwei Prozent. Die achtundvierzig Prozent vergleichen Beträge nach Sozialabgaben und vor Steuern.",
        "Und das gilt nur mit fünfundvierzig vollen Jahren und Durchschnittsgehalt.",
        "Was dein Gehalt wirklich bringt, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
