"""Short 016 · Was kostet X: die Sozialversicherung 2026 (aus Video 006)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, VIOLET, eur
from lib.shorts import SIZE, zahl
from videos.v006_brutto_netto.scenes import M, SV, SV_RATE

assert abs(SV_RATE - 21.75) < 1e-9 and SV == 652.5

draw = zahl("21,75 %", "deines Bruttos: Sozialversicherung", "Arbeitnehmeranteile 2026, kinderlos, Ø-Zusatzbeitrag",
            [(1, "Rente", "9,3 %", VIOLET), ((1, 0.8), "Arbeitslosigkeit", "1,3 %", GRAY),
             ((2, 0.0), "Krankheit", "8,75 %", BLUE), ((2, 1.0), "Pflege (kinderlos)", "2,4 %", (125, 211, 252))],
            (3, [("Bei 3.000 € brutto:", None), (eur(SV, 2) + " im Monat", BLUE)]),
            (4, "Brutto, netto: Video auf dem Kanal"),
            "Beitragssätze 2026 · KV: 7,3 % + Ø-Zusatzbeitrag 1,45 % · PV: 1,8 % + 0,6 % kinderlos")


def scenes():
    return [Scene("short", [
        "Einundzwanzig Komma sieben fünf Prozent. So viel deines Bruttos geht zweitausendsechsundzwanzig an die Sozialversicherung.",
        "Neun Komma drei Prozent für die Rente und eins Komma drei für die Arbeitslosenversicherung.",
        "Für die Krankenversicherung im Schnitt acht Komma sieben fünf Prozent, und zwei Komma vier für die Pflege, wenn du keine Kinder hast.",
        "Bei dreitausend Euro brutto sind das sechshundertzweiundfünfzig Euro fünfzig im Monat. Und dein Arbeitgeber zahlt ungefähr noch einmal so viel.",
        "Was danach noch an Steuer abgeht, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
