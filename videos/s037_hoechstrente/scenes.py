"""Short 037 · Zahl der Woche: 3.735 € Höchstrente (aus Video 010)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, RED, eur
from lib.shorts import SIZE, zahl
from videos.v010_gesetzliche_rente.scenes import BBG, DE, rente

MAX = rente(8450)
assert round(MAX) == 3735 and round(BBG / DE, 2) == 1.95

draw = zahl(eur(MAX), "mehr gesetzliche Rente geht nicht", "nach 45 Jahren, in heutigen Werten, brutto",
            [(1, "Beiträge nur bis", eur(8450) + "/Monat", FG), (2, "max. Punkte pro Jahr", "1,95", BLUE),
             (3, "Mehr Gehalt darüber", "kein Plus", RED)],
            None, (4, "Gesetzliche Rente: Video auf dem Kanal"), "Beitragsbemessungsgrenze 2026 · Rentenwert 42,52 €")


def scenes():
    return [Scene("short", [
        "Dreitausendsiebenhundertfünfunddreißig Euro. Mehr gesetzliche Rente geht nach fünfundvierzig Jahren nicht, in heutigen Werten.",
        "Denn Rentenbeiträge zählen nur bis achttausendvierhundertfünfzig Euro brutto im Monat.",
        "Das sind höchstens eins Komma neun fünf Rentenpunkte pro Jahr.",
        "Wer mehr verdient, bekommt dafür keine höhere Rente.",
        "Was dein Gehalt bringt, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
