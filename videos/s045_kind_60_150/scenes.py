"""Short 045 · Vergleich: Günstigerprüfung bei 60.000 € vs. 150.000 € (aus Video 012)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, vergleich
from videos.v012_kindergeld_freibetrag.scenes import EX, KG_JAHR

(z1, s1), _, (z3, s3) = EX
assert (z1, s1, z3, s3) == (60000, 2668, 150000, 4098) and s3 - KG_JAHR == 990

draw = vergleich("Kindergeld oder Freibetrag?", "Eltern zusammen, ein Kind, zu versteuerndes Einkommen",
                 [(1, eur(z1), GREEN, [("Freibetrag spart", eur(s1), FG), ("Kindergeld", eur(KG_JAHR), GREEN), ("Ergebnis", "Kindergeld", GREEN)]),
                  (2, eur(z3), AMBER, [("Freibetrag spart", eur(s3), FG), ("Kindergeld", eur(KG_JAHR), GREEN), ("Ergebnis", "+990 €", AMBER)])],
                 (3, [("Hohes Einkommen:", None), ("Differenz über die Steuer", AMBER)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "Tarif 2026, Splitting · ohne Soli/Kirchensteuer")


def scenes():
    return [Scene("short", [
        "Kindergeld oder Kinderfreibetrag: Was bekommen Eltern mit unterschiedlichem Einkommen?",
        "Bei sechzigtausend Euro zu versteuerndem Einkommen spart der Freibetrag zweitausendsechshundertachtundsechzig Euro Steuer, weniger als das Kindergeld. Es bleibt beim Kindergeld.",
        "Bei hundertfünfzigtausend Euro spart er viertausendachtundneunzig Euro, also neunhundertneunzig Euro mehr als das Kindergeld.",
        "Diese Differenz kommt dann über die Steuererklärung.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
