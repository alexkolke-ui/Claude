"""Short 050 · Vergleich: Mindestlohn 2026 vs. 2027 (aus Video 013)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, vergleich
from videos.v013_mindestlohn_2027.scenes import B26, B27, N26, N27

assert (B26, B27, N26["Netto"], N27["Netto"]) == (2409.33, 2530.67, 1716.49, 1786.69)

draw = vergleich("Mindestlohn: 2026 vs. 2027", "Vollzeit 40 h/Woche · StKl. I · Steuer 2026 als Näherung",
                 [(1, "2026", BLUE, [("pro Stunde", "13,90 €", FG), ("brutto", eur(B26, 2), FG), ("netto ≈", eur(N26["Netto"]), BLUE)]),
                  (2, "2027", GREEN, [("pro Stunde", "14,60 €", FG), ("brutto", eur(B27, 2), FG), ("netto ≈", eur(N27["Netto"]), GREEN)])],
                 (3, [("+121 € brutto", None), ("≈ +70 € netto im Monat", AMBER)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "Berechnung nach BMF-PAP 2026, Sozialversicherung 2027 unverändert")


def scenes():
    return [Scene("short", [
        "Was bringt der neue Mindestlohn im Monat?",
        "Zweitausendsechsundzwanzig: dreizehn Euro neunzig pro Stunde, bei Vollzeit zweitausendvierhundertneun Euro brutto und rund tausendsiebenhundertsechzehn netto.",
        "Zweitausendsiebenundzwanzig: vierzehn Euro sechzig, also zweitausendfünfhundertdreißig Euro brutto und rund tausendsiebenhundertsiebenundachtzig netto, gerechnet mit dem Steuertarif zweitausendsechsundzwanzig.",
        "Das sind hunderteinundzwanzig Euro mehr brutto und rund siebzig Euro mehr netto im Monat.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
