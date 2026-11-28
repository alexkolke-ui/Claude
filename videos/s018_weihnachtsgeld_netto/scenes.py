"""Short 018 · Zahl der Woche: Weihnachtsgeld netto (aus Video 007)."""
from lib.engine import Scene
from lib.gfx import BLUE, GREEN, RED, eur
from lib.shorts import SIZE, zahl
from videos.v007_weihnachtsgeld.scenes import B, M, Q, SV_Z, Z

assert Z["Netto"] == 1915.75 and round(Q(Z["Netto"], B), 1) == 54.7 and round(Q(M["Netto"], B), 1) == 66.7
assert Z["LSt"] == 823 and SV_Z == 761.25

draw = zahl(eur(Z["Netto"], 2), "bleiben von 3.500 € Weihnachtsgeld", "2026 · Steuerklasse I, kinderlos, ohne Kirchensteuer",
            [(1, "Lohnsteuer", "−" + eur(Z["LSt"], 2), RED), ((1, 1.0), "Sozialversicherung", "−" + eur(SV_Z, 2), BLUE),
             (2, "netto", "54,7 %", GREEN), ((2, 1.0), "zum Vergleich: Monatsgehalt", "66,7 %", BLUE)],
            None, (3, "Warum? Video auf dem Kanal"),
            "Berechnung nach BMF-Programmablaufplan Lohnsteuer 2026, Jahreslohn-Methode", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Dreitausendfünfhundert Euro Weihnachtsgeld. Netto bleiben davon tausendneunhundertfünfzehn Euro fünfundsiebzig.",
        "Achthundertdreiundzwanzig Euro gehen an Lohnsteuer, siebenhunderteinundsechzig Euro fünfundzwanzig an die Sozialversicherung.",
        "Das sind nur vierundfünfzig Komma sieben Prozent. Vom normalen Monatsgehalt in gleicher Höhe bleiben sechsundsechzig Komma sieben Prozent.",
        "Warum vom Weihnachtsgeld weniger übrig bleibt, erklären wir im Video auf dem Kanal.",
    ], draw, extra=2.0)]
