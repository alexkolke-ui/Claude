"""Short 026 · Zahl der Woche: 540 € Grundzulage (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v009_altersvorsorgedepot.scenes import grundzulage

assert grundzulage(120) == 60 and grundzulage(360) == 180 and grundzulage(1800) == 540

draw = zahl("540 €", "Zulage pro Jahr – maximal", "Altersvorsorgedepot ab 2027 · Grundzulage je Monatsbeitrag",
            [(1, "10 € im Monat", "+" + eur(60), GREEN), ((1, 1.0), "30 € im Monat", "+" + eur(180), GREEN),
             (2, "150 € im Monat", "+" + eur(540), GREEN)],
            (3, [("Kleine Beiträge:", None), ("bis zu 50 % Zulage", AMBER)]),
            (4, "Alle Regeln: Video am 7. Januar"), "Quelle: BMF-FAQ zur Reform der privaten Altersvorsorge", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Fünfhundertvierzig Euro. So viel Zulage gibt der Staat ab zweitausendsiebenundzwanzig maximal pro Jahr für das neue Altersvorsorgedepot.",
        "Wer zehn Euro im Monat einzahlt, bekommt sechzig Euro im Jahr dazu. Bei dreißig Euro sind es hundertachtzig.",
        "Für die vollen fünfhundertvierzig Euro braucht es hundertfünfzig Euro im Monat.",
        "Kleine Beiträge bekommen also bis zu fünfzig Prozent Zulage.",
        "Alle Regeln erklären wir im Video am siebten Januar auf dem Kanal.",
    ], draw, extra=1.5)]
