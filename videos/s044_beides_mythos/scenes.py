"""Short 044 · Mythos: Kindergeld und Kinderfreibetrag gibt es beide (aus Video 012)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, mythos
from videos.v012_kindergeld_freibetrag.scenes import KG_JAHR, ersparnis

S60 = ersparnis(60000)
assert S60 == 2668 and KG_JAHR == 3108

draw = mythos(["„Kindergeld und Freibetrag", "bekomme ich beide.“"],
              [(2, "Kindergeld", eur(KG_JAHR), GREEN), (3, "Freibetrag spart", eur(S60), BLUE),
               ((3, 1.2), "es gilt", "Kindergeld", GREEN)],
              (4, [("Entweder – oder:", None), ("das Finanzamt prüft", AMBER)]),
              (5, "Ab wann der Freibetrag gilt: Video"), "Günstigerprüfung § 31 EStG · Eltern zusammen, 1 Kind · Tarif 2026",
              rows_head="Beispiel: 60.000 € Einkommen")


def scenes():
    return [Scene("short", [
        "Kindergeld und Kinderfreibetrag, das bekomme ich doch beides. Stimmt nicht.",
        "Das Finanzamt macht eine Günstigerprüfung und gibt dir nur das, was mehr bringt.",
        "Ein Beispiel für Eltern mit sechzigtausend Euro zu versteuerndem Einkommen: Das Kindergeld bringt dreitausendeinhundertacht Euro im Jahr.",
        "Der Freibetrag würde nur zweitausendsechshundertachtundsechzig Euro Steuer sparen. Also bleibt es beim Kindergeld.",
        "Es ist also entweder oder, und das Finanzamt prüft das automatisch.",
        "Ab wann der Freibetrag gewinnt, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
