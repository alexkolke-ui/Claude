"""Short 059 · Vergleich: 10.000 € Sondertilgung vs. Festgeld über 10 Jahre (aus Video 015)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, vergleich
from videos.v015_sondertilgung.scenes import BETRAG, FG_NET_END, ST_END

assert round(ST_END - BETRAG) == 4775 and round(FG_NET_END - BETRAG) == 2290

draw = vergleich("10.000 € über 10 Jahre", "Durchschnittszinsen Sept. 2026, konstant angenommen",
                 [(1, "Sondertilgung", BLUE, [("Baukredit", "3,91 %", FG), ("gesparte Zinsen", "+" + eur(ST_END - BETRAG), BLUE)]),
                  (2, "Festgeld", GREEN, [("nach Steuer", "2,08 %", FG), ("Zinsen", "+" + eur(FG_NET_END - BETRAG), GREEN)])],
                 (3, [("Tilgen: gut doppelt so viel", AMBER), ("– wenn der Vertrag es erlaubt", None)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "Modellrechnung · Festgeld über dem Sparerpauschbetrag besteuert")


def scenes():
    return [Scene("short", [
        "Zehntausend Euro übrig und ein Baukredit. Tilgen oder anlegen?",
        "Als Sondertilgung bei drei Komma neun eins Prozent sparst du in zehn Jahren rund viertausendsiebenhundertfünfundsiebzig Euro Zinsen.",
        "Als Festgeld über dem Freibetrag bringen die zehntausend Euro nach Steuern rund zweitausendzweihundertneunzig Euro.",
        "Tilgen bringt hier also gut doppelt so viel. Aber nur, wenn dein Vertrag Sondertilgungen erlaubt.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
