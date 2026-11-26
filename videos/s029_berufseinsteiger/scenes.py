"""Short 029 · Zahl der Woche: 200 € Berufseinsteigerbonus (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v009_altersvorsorgedepot.scenes import BONUS_U25, grundzulage

assert BONUS_U25 == 200 and grundzulage(360) == 180

draw = zahl("+200 €", "Bonus für alle unter 25", "Altersvorsorgedepot ab 2027 · Berufseinsteigerbonus",
            [(1, "Abschluss unter 25", "einmalig", FG), (2, "dazu bei 30 € im Monat", "+" + eur(180) + "/Jahr", GREEN)],
            (3, [("Im ersten Jahr: 380 €", BLUE), ("auf 360 € Eigenbeitrag", None)]),
            (4, "Alle Regeln: Video auf dem Kanal"), "Quelle: BMF-FAQ zur Reform der privaten Altersvorsorge", big_color=BLUE)


def scenes():
    return [Scene("short", [
        "Zweihundert Euro geschenkt, für alle unter fünfundzwanzig.",
        "Wer vor seinem fünfundzwanzigsten Geburtstag ein Altersvorsorgedepot oder einen anderen geförderten Vertrag abschließt, bekommt einmalig zweihundert Euro Berufseinsteigerbonus.",
        "Dazu kommt die normale Zulage: Bei dreißig Euro im Monat sind das hundertachtzig Euro im Jahr.",
        "Im ersten Jahr also dreihundertachtzig Euro vom Staat auf dreihundertsechzig Euro Eigenbeitrag.",
        "Alle Regeln findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
