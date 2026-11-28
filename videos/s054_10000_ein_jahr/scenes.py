"""Short 054 · Vergleich: 10.000 € ein Jahr Tagesgeld vs. Festgeld (aus Video 014)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GRAY, GREEN
from lib.shorts import SIZE, vergleich
from videos.v014_festgeld_tagesgeld.scenes import F3, M, TG

assert round(100 * TG[M]) == 52 and round(100 * F3[M]) == 283

draw = vergleich("10.000 € für ein Jahr", "Durchschnittszinsen September 2026",
                 [(1, "Tagesgeld & Giro", GRAY, [("Zins (Ø)", "0,52 %", FG), ("Zinsen", "+52 €", GRAY)]),
                  (2, "Festgeld > 2 J.", GREEN, [("Zins (Ø)", "2,83 %", FG), ("Zinsen", "+283 €", GREEN)])],
                 (3, [("Mehr Zins –", None), ("dafür ist das Geld gebunden", AMBER)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "Bundesbank SUD101, SUD104 · vor Steuern · keine Produktempfehlung")


def scenes():
    return [Scene("short", [
        "Zehntausend Euro, ein Jahr lang. Wie viel Zinsen bringt das?",
        "Auf Tagesgeld und Girokonto im Schnitt zweiundfünfzig Euro.",
        "Als Festgeld über mehr als zwei Jahre im Schnitt zweihundertdreiundachtzig Euro.",
        "Mehr Zins, aber dafür ist das Geld gebunden. Meist kommt man vorher nicht heran.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
