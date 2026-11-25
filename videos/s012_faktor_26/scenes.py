"""Short 012 · Zahl der Woche: 26,1 Jahresmieten (aus Video 005)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, RED, VIOLET
from lib.shorts import SIZE, zahl
from videos.v005_mieten_kaufen.scenes import F, KPM127, KPM7, YIELD, dec, pct

assert F == 26.1 and KPM127[2025] == 27.1 and KPM7[2025] == 30.6 and 3.8 < YIELD[2025] < 3.85

draw = zahl("26,1", "Jahresmieten kostet eine Wohnung", "Kaufpreis ÷ Jahreskaltmiete, Eigentumswohnungen 2025",
            [(1, "Deutschland", dec(F), BLUE), ((2, 0.0), "127 Städte", dec(KPM127[2025]), VIOLET),
             ((2, 0.8), "7 Großstädte", dec(KPM7[2025]), RED)],
            (3, [("Mietrendite: 1 ÷ 26,1", None), (f"≈ {pct(YIELD[2025], 2)} pro Jahr", AMBER)]),
            (4, "Mieten oder kaufen? Video auf dem Kanal"),
            "Quelle: Deutsche Bundesbank, Indikatorensystem Wohnimmobilienmarkt")


def scenes():
    return [Scene("short", [
        "Sechsundzwanzig Komma eins. So viele Jahresmieten kostet eine Eigentumswohnung in Deutschland im Schnitt.",
        "Das ist der Kaufpreis-Miet-Faktor der Bundesbank für zweitausendfünfundzwanzig.",
        "In hundertsiebenundzwanzig Städten liegt er bei siebenundzwanzig Komma eins, in den sieben größten Städten sogar bei dreißig Komma sechs.",
        "Umgedreht heißt das: Eine Wohnung bringt im Schnitt rund drei Komma acht Prozent Miete pro Jahr, vor allen Kosten.",
        "Ob sich Kaufen damit lohnt, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=1.0)]
