"""Short 052 · Was kostet X: Was vom Mindestlohn netto bleibt (aus Video 013)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, RED, eur
from lib.shorts import SIZE, zahl
from videos.v013_mindestlohn_2027.scenes import B27, N27, SV27

assert (B27, SV27, N27["LSt"], N27["Netto"]) == (2530.67, 550.40, 193.58, 1786.69)

draw = zahl("≈ " + eur(N27["Netto"]), "netto vom Mindestlohn", "Vollzeit 2027 · StKl. I, kinderlos · Steuer nach Tarif 2026 (Näherung)",
            [(1, "brutto", eur(B27, 2), FG), (2, "Sozialversicherung", "−" + eur(SV27, 2), BLUE),
             ((2, 1.2), "Lohnsteuer ≈", "−" + eur(N27["LSt"], 2), RED)],
            None, (3, "Ganze Rechnung: Video auf dem Kanal"), "BMF-PAP 2026 · Ø-Zusatzbeitrag 2,9 %", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Was bleibt vom Mindestlohn zweitausendsiebenundzwanzig netto?",
        "Bei Vollzeit sind es zweitausendfünfhundertdreißig Euro siebenundsechzig brutto.",
        "Fünfhundertfünfzig Euro vierzig gehen an die Sozialversicherung, dazu rund hundertdreiundneunzig Euro Lohnsteuer, gerechnet mit dem Tarif zweitausendsechsundzwanzig.",
        "Netto bleiben rund tausendsiebenhundertsechsundachtzig Euro. Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=2.0)]
