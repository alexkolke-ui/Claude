"""Short 015 · Mythos: Gehaltserhöhung lohnt sich nicht (aus Video 006)."""
from lib.engine import Scene
from lib.gfx import AMBER, GREEN, eur
from lib.shorts import SIZE, mythos
from videos.v006_brutto_netto.scenes import RAISE_3000, RAISE_5000

assert 56 < RAISE_3000 < 57 and 50.5 < RAISE_5000 < 51.5

draw = mythos(["„Eine Gehaltserhöhung", "lohnt sich nicht.“"],
              [(2, "3.000 → 3.100 € brutto", "+" + eur(RAISE_3000, 2), GREEN),
               (3, "5.000 → 5.100 € brutto", "+" + eur(RAISE_5000, 2), GREEN)],
              (4, [("Mehr brutto =", None), ("immer mehr netto", GREEN)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"),
              "BMF-Programmablaufplan Lohnsteuer 2026 · StKl. I, kinderlos", rows_head="netto mehr im Monat")


def scenes():
    return [Scene("short", [
        "Eine Gehaltserhöhung lohnt sich nicht, weil dann mehr Steuern fällig werden. Stimmt das?",
        "Rechnen wir mit den Werten für zweitausendsechsundzwanzig.",
        "Von dreitausend auf dreitausendeinhundert Euro brutto bleiben netto rund sechsundfünfzig Euro mehr.",
        "Von fünftausend auf fünftausendeinhundert Euro rund einundfünfzig Euro mehr.",
        "Der höhere Steuersatz gilt nur für den zusätzlichen Euro. Mehr brutto heißt deshalb immer mehr netto.",
        "Die ganze Brutto-Netto-Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
