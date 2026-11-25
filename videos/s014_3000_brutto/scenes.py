"""Short 014 · Zahl der Woche: 3.000 € brutto → netto (aus Video 006)."""
from lib.engine import Scene
from lib.gfx import BLUE, GREEN, RED, eur
from lib.shorts import SIZE, zahl
from videos.v006_brutto_netto.scenes import M, SV

assert M["Netto"] == 2054.42 and SV == 652.5 and M["LSt"] == 293.08 and M["Soli"] == 0

draw = zahl(eur(M["Netto"], 2), "netto von 3.000 € brutto", "2026 · Steuerklasse I, kinderlos, ohne Kirchensteuer",
            [(1, "Sozialversicherung", "−" + eur(SV, 2), BLUE), ((2, 0.0), "Lohnsteuer", "−" + eur(M["LSt"], 2), RED),
             ((2, 1.0), "Solidaritätszuschlag", "0,00 €", GREEN)],
            (3, [("Mehr als zwei Drittel", None), ("der Abzüge: Sozialversicherung", BLUE)]),
            (4, "Ganze Rechnung: Video auf dem Kanal"),
            "Berechnung nach BMF-Programmablaufplan Lohnsteuer 2026 · KV-Zusatz Ø 2,9 %", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Dreitausend Euro brutto. Wie viel bleibt zweitausendsechsundzwanzig netto?",
        "Zuerst geht die Sozialversicherung ab: sechshundertzweiundfünfzig Euro fünfzig für Rente, Arbeitslosigkeit, Krankheit und Pflege.",
        "Dann zweihundertdreiundneunzig Euro Lohnsteuer. Solidaritätszuschlag fällt keiner an.",
        "Netto bleiben zweitausendvierundfünfzig Euro zweiundvierzig. Mehr als zwei Drittel der Abzüge gehen an die Sozialversicherung, nicht ans Finanzamt.",
        "Wie die Lohnsteuer genau entsteht, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
