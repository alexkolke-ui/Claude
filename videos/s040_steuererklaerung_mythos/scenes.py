"""Short 040 · Mythos: Die Steuererklärung lohnt sich für mich nicht (aus Video 011)."""
from lib.engine import Scene
from lib.gfx import AMBER, GRAY, GREEN, eur
from lib.shorts import SIZE, mythos
from videos.v011_steuererklaerung.scenes import KMS

r = {km: ref for km, _, ref, _ in KMS}
assert r == {10: 0, 20: 120, 30: 346, 40: 570}

draw = mythos(["„Die Steuererklärung", "lohnt sich für mich nicht.“"],
              [(2, "10 km Arbeitsweg", eur(r[10]), GRAY), (3, "20 km", "≈ " + eur(r[20]), GREEN),
               ((3, 1.0), "30 km", "≈ " + eur(r[30]), GREEN), ((3, 2.0), "40 km", "≈ " + eur(r[40]), GREEN)],
              (4, [("Es kommt auf deine", None), ("Kosten an", AMBER)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"), "3.000 € brutto, StKl. I, 220 Tage · Tarif 2026, vereinfacht",
              rows_head="zurück pro Jahr")


def scenes():
    return [Scene("short", [
        "Die Steuererklärung lohnt sich für mich nicht. Stimmt das?",
        "Kommt darauf an. Rechnen wir mit dreitausend Euro brutto und nur dem Arbeitsweg.",
        "Bei zehn Kilometern kommt nichts zurück, die Pauschale deckt das schon ab.",
        "Bei zwanzig Kilometern rund hundertzwanzig Euro, bei dreißig rund dreihundertsechsundvierzig und bei vierzig rund fünfhundertsiebzig Euro.",
        "Es hängt also an deinen Kosten. Weitere Werbungskosten kommen noch dazu.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
