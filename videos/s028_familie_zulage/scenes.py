"""Short 028 · Vergleich: Zulage Single vs. Familie mit zwei Kindern (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, vergleich
from videos.v009_altersvorsorgedepot.scenes import FAM, grundzulage, kinderzulage

assert grundzulage(300) == 150 and kinderzulage(300, 2) == 600 and FAM == 750

draw = vergleich("25 € im Monat", "Altersvorsorgedepot ab 2027 · Zulage pro Jahr",
                 [(1, "ohne Kind", BLUE, [("Eigenbeitrag", eur(300), FG), ("Grundzulage", eur(150), GREEN), ("Zulage gesamt", eur(150), BLUE)]),
                  (2, "2 Kinder", GREEN, [("Eigenbeitrag", eur(300), FG), ("Kinderzulage", eur(600), GREEN), ("Zulage gesamt", eur(FAM), GREEN)])],
                 (3, [("Familie: 250 % Zulage", AMBER), ("auf den eigenen Beitrag", None)]),
                 (4, "Alle Regeln: Video auf dem Kanal"), "Kinderzulage: 1 € je Euro, bis 300 € pro Kind · BMF-FAQ")


def scenes():
    return [Scene("short", [
        "Fünfundzwanzig Euro im Monat ins neue Altersvorsorgedepot. Wie viel legt der Staat drauf?",
        "Ohne Kind: dreihundert Euro Eigenbeitrag im Jahr, hundertfünfzig Euro Grundzulage.",
        "Mit zwei Kindern kommt für jedes Kind eine Kinderzulage von dreihundert Euro dazu. Zusammen siebenhundertfünfzig Euro.",
        "Für die Familie sind das zweihundertfünfzig Prozent Zulage auf den eigenen Beitrag.",
        "Alle Regeln findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
