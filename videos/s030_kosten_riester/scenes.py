"""Short 030 · Mythos: Das wird wieder so teuer wie Riester (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN
from lib.shorts import SIZE, mythos
from videos.v009_altersvorsorgedepot.scenes import KOSTEN_STD, WECHSEL_FREI_JAHRE, WECHSEL_GEBUEHR

assert KOSTEN_STD == 1.0 and WECHSEL_GEBUEHR == 150 and WECHSEL_FREI_JAHRE == 5

draw = mythos(["„Das wird wieder so", "teuer wie Riester.“"],
              [(2, "Standarddepot: Kosten", "max. 1,0 %", GREEN), (3, "Wechsel nach 5 Jahren", "kostenfrei", GREEN),
               ((3, 1.0), "neuer Anbieter darf", "max. 150 €", BLUE), (4, "Abschlusskosten", "verteilt", FG)],
              (5, [("Kostendeckel –", None), ("aber 1 % ist nicht wenig", AMBER)]),
              (6, "Was 1 % ausmacht: Video auf dem Kanal"), "Quelle: BMF-FAQ zur Reform der privaten Altersvorsorge",
              rows_head="neue Regeln ab 2027")


def scenes():
    return [Scene("short", [
        "Das neue Altersvorsorgedepot wird doch wieder so teuer wie Riester. Stimmt das?",
        "Es gibt neue Regeln gegen hohe Kosten.",
        "Im Standarddepot, das jeder Anbieter haben muss, dürfen die Kosten höchstens ein Prozent pro Jahr betragen.",
        "Nach fünf Jahren darf der alte Anbieter für einen Wechsel nichts mehr verlangen, der neue höchstens hundertfünfzig Euro.",
        "Und Abschlusskosten müssen auf die ganze Ansparzeit verteilt werden.",
        "Es gibt also einen Kostendeckel. Aber ein Prozent pro Jahr ist über Jahrzehnte nicht wenig.",
        "Was das ausmacht, rechnen wir im Video auf dem Kanal vor.",
    ], draw, extra=1.0)]
