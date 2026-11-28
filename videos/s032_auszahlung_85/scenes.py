"""Short 032 · Zahl der Woche: Auszahlplan bis mindestens 85 (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, RED
from lib.shorts import SIZE, zahl

draw = zahl("bis 85", "läuft mindestens der Auszahlplan", "Altersvorsorgedepot ab 2027 · so kommt das Geld zurück",
            [(1, "Beginn", "65 bis 70", FG), (2, "Alternative", "lebenslange Rente", BLUE),
             ((2, 1.2), "Rest beim Auszahlplan", "vererbbar", GREEN), (3, "Steuer", "erst im Alter, voll", RED)],
            None, (4, "Alle Regeln: Video auf dem Kanal"), "Quelle: BMF-FAQ zur Reform der privaten Altersvorsorge",
            big_color=AMBER)


def scenes():
    return [Scene("short", [
        "Bis fünfundachtzig. So lange muss ein Auszahlplan beim neuen Altersvorsorgedepot mindestens laufen.",
        "Die Auszahlung beginnt zwischen fünfundsechzig und siebzig.",
        "Statt eines Auszahlplans kannst du auch eine lebenslange Rente wählen. Beim Auszahlplan ist das, was am Ende noch übrig ist, vererbbar.",
        "Versteuert wird erst im Alter, dann aber die ganze Auszahlung.",
        "Alle Regeln findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
