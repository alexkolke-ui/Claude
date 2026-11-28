"""Short 062 · Zahl der Woche: 2,08 % – Festgeld nach Steuer vs. steuerfreie Tilgung (aus Video 015)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, RED
from lib.shorts import SIZE, zahl
from videos.v015_sondertilgung.scenes import B10_NOW, FG_NET, FGZ

assert FGZ == 2.83 and round(FG_NET, 2) == 2.08 and B10_NOW == 3.91

draw = zahl("2,08 %", "bleiben von 2,83 % Festgeld", "nach Abgeltungsteuer + Soli, über dem Sparerpauschbetrag",
            [(1, "Festgeld vor Steuer", "2,83 %", FG), ((1, 1.0), "Steuer 26,375 %", "−0,75 Pkt.", RED),
             (2, "Baukredit tilgen", "3,91 % steuerfrei", BLUE)],
            (3, [("Gesparte Zinsen", None), ("werden nicht besteuert", AMBER)]),
            (3, "Tilgungs-Leiter: Video auf dem Kanal"), "§ 32d EStG · Durchschnittszinsen Bundesbank, Sept. 2026", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Zwei Komma null acht Prozent. So viel bleibt von zwei Komma acht drei Prozent Festgeld, wenn deine Zinsen über dem Freibetrag liegen.",
        "Denn auf Zinsen fallen sechsundzwanzig Komma vier Prozent Abgeltungsteuer und Soli an.",
        "Wer stattdessen einen Baukredit zu drei Komma neun eins Prozent tilgt, spart diese Zinsen komplett, ohne Steuer.",
        "Gesparte Kreditzinsen werden also nicht besteuert. Mehr dazu im Video auf dem Kanal.",
    ], draw, extra=2.0)]
