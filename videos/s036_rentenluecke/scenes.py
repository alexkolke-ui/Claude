"""Short 036 · Vergleich: Netto heute vs. Rente vor Steuern (aus Video 010)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v010_gesetzliche_rente.scenes import GEHALT_NET, R, R_NET

assert GEHALT_NET == 2054.42 and round(R, 2) == 1326.09 and round(R_NET, 2) == 1154.36

draw = vergleich("Die Rentenlücke", "3.000 € brutto, 45 Jahre, StKl. I, kinderlos",
                 [(1, "heute", GREEN, [("Brutto", eur(3000), FG), ("Netto", eur(GEHALT_NET, 2), GREEN)]),
                  (2, "Rente", BLUE, [("Brutto", eur(R, 2), FG), ("nach KV/PV", eur(R_NET, 2), BLUE)])],
                 (3, [("Lücke: rund 900 €", RED), ("im Monat", None)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "heutige Werte · Rente vor Steuern · KV/PV 12,95 %")


def scenes():
    return [Scene("short", [
        "Wie groß ist die Rentenlücke bei dreitausend Euro brutto?",
        "Heute bleiben davon zweitausendvierundfünfzig Euro netto.",
        "Nach fünfundvierzig Jahren gibt es rund tausenddreihundertsechsundzwanzig Euro Rente. Nach Kranken- und Pflegeversicherung bleiben tausendeinhundertvierundfünfzig Euro, noch vor Steuern.",
        "Die Lücke beträgt also rund neunhundert Euro im Monat.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
