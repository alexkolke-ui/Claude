"""Short 046 · Zahl der Woche: ab 86.100 € lohnt sich der Kinderfreibetrag (aus Video 012)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v012_kindergeld_freibetrag.scenes import BREAK, KFB, KG_JAHR

assert BREAK == 86100 and KFB == 9756 and KG_JAHR == 3108

draw = zahl("86.100 €", "ab hier gewinnt der Kinderfreibetrag", "zu versteuerndes Einkommen, Eltern zusammen, ein Kind",
            [(1, "Kindergeld pro Jahr", eur(KG_JAHR), GREEN), (2, "Freibeträge je Kind", eur(KFB), BLUE)],
            (3, [("Darunter: Kindergeld", GREEN), ("Darüber: Freibetrag", AMBER)]),
            (4, "Ganze Rechnung: Video auf dem Kanal"), "Tarif 2026, Splitting · ohne Soli/Kirchensteuer")


def scenes():
    return [Scene("short", [
        "Sechsundachtzigtausendeinhundert Euro. Ab diesem zu versteuernden Einkommen lohnt sich für Eltern mit einem Kind der Kinderfreibetrag.",
        "Das Kindergeld bringt dreitausendeinhundertacht Euro im Jahr.",
        "Die Freibeträge senken das zu versteuernde Einkommen um neuntausendsiebenhundertsechsundfünfzig Euro. Erst ab dieser Einkommensgrenze spart das mehr Steuer als das Kindergeld bringt.",
        "Darunter bleibt es beim Kindergeld, darüber gibt es die Differenz zurück.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
