"""Short 019 · Mythos: Weihnachtsgeld wird mit Steuerklasse 6 versteuert (aus Video 007)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, RED, eur
from lib.shorts import SIZE, mythos
from videos.v007_weihnachtsgeld.scenes import B, L0, L1

assert L0 == 4866 and L1 == 5689 and L1 - L0 == 823 and B == 3500

draw = mythos(["„Weihnachtsgeld läuft über", "Steuerklasse 6.“"],
              [(2, "Jahressteuer ohne", eur(L0), FG), ((2, 1.0), "Jahressteuer mit", eur(L1), FG),
               (3, "Steuer aufs Weihnachtsgeld", eur(L1 - L0), RED)],
              (4, [("Eigene Steuerklasse –", None), ("Satz für den obersten Euro", AMBER)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"),
              "3.500 € Gehalt + 3.500 € Weihnachtsgeld · StKl. I · BMF-PAP 2026", rows_head="Jahreslohn-Methode")


def scenes():
    return [Scene("short", [
        "Weihnachtsgeld wird mit Steuerklasse sechs versteuert. Das hört man oft, aber es stimmt nicht.",
        "Steuerklasse sechs gilt für einen zweiten Job. Weihnachtsgeld wird mit der Jahreslohn-Methode versteuert.",
        "Bei dreitausendfünfhundert Euro Gehalt: Die Jahressteuer ohne Weihnachtsgeld beträgt viertausendachthundertsechsundsechzig Euro, mit Weihnachtsgeld fünftausendsechshundertneunundachtzig.",
        "Die Differenz, achthundertdreiundzwanzig Euro, ist die Steuer auf das Weihnachtsgeld.",
        "Es läuft also über deine eigene Steuerklasse, nur eben mit dem Satz für deinen obersten Euro.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
