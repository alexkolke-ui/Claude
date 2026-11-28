"""Short 038 · Zahl der Woche: 38 Cent ab dem ersten Kilometer (aus Video 011)."""
from lib.engine import Scene
from lib.gfx import AMBER, GRAY, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v011_steuererklaerung.scenes import KMS

assert [round(w) for _, w, _, _ in KMS] == [836, 1672, 2508, 3344]

draw = zahl("38 Cent", "pro Kilometer – ab dem ersten", "Entfernungspauschale 2026 · einfache Strecke · 220 Tage",
            [(1, "10 km", eur(836), GRAY), ((1, 1.0), "20 km", eur(1672), GREEN), (2, "40 km", eur(3344), GREEN)],
            (3, [("Aber: Erst über 1.230 €", None), ("bringt es Geld zurück", AMBER)]),
            (4, "Steuererklärung: Video am 21. Januar"), "Entfernungspauschale 2026 · § 9 EStG", big_color=GREEN, rows_head="Werbungskosten im Jahr")


def scenes():
    return [Scene("short", [
        "Achtunddreißig Cent. So viel zählt seit zweitausendsechsundzwanzig jeder Kilometer zur Arbeit, ab dem ersten.",
        "Bei zweihundertzwanzig Arbeitstagen und zehn Kilometern sind das achthundertsechsunddreißig Euro, bei zwanzig Kilometern tausendsechshundertzweiundsiebzig.",
        "Bei vierzig Kilometern dreitausenddreihundertvierundvierzig Euro.",
        "Aber Geld zurück gibt es erst für den Teil über tausendzweihundertdreißig Euro, der Pauschale, die jeder ohnehin bekommt.",
        "Was das in Euro bringt, rechnen wir im Video am einundzwanzigsten Januar durch.",
    ], draw, extra=1.5)]
