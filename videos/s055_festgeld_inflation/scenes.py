"""Short 055 · Mythos: Mit Festgeld schlage ich die Inflation (aus Video 014)."""
from lib.engine import Scene
from lib.gfx import AMBER, GREEN, RED
from lib.shorts import SIZE, mythos
from videos.v014_festgeld_tagesgeld.scenes import F3, INF_AVG, M

NET = F3[M] * (1 - 0.26375)
REAL_PRE = ((1 + F3[M] / 100) / (1 + INF_AVG / 100) - 1) * 100
REAL_NET = ((1 + NET / 100) / (1 + INF_AVG / 100) - 1) * 100
assert round(REAL_PRE, 1) == 0.2 and round(NET, 2) == 2.08 and round(REAL_NET, 1) == -0.5 and round(INF_AVG, 2) == 2.63
p = lambda v: f"{v:+.1f} %".replace(".", ",").replace("-", "−")

draw = mythos(["„Mit Festgeld schlage", "ich die Inflation.“"],
              [(2, "Festgeld > 2 J. vor Steuer", p(REAL_PRE), GREEN), (3, "nach Steuer (2,08 %)", p(REAL_NET), RED)],
              (4, [("Knapp – und über dem", None), ("Freibetrag im Minus", AMBER)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"), "Inflation Ø Jan.–Okt. 2026: 2,63 % · Bundesbank SUD104",
              rows_head="real, nach Inflation")


def scenes():
    return [Scene("short", [
        "Mit Festgeld schlage ich die Inflation. Stimmt das?",
        "Festgeld über mehr als zwei Jahre brachte im Schnitt zwei Komma acht drei Prozent. Die Inflation lag zweitausendsechsundzwanzig bisher im Schnitt bei zwei Komma sechs drei.",
        "Vor Steuern bleibt real ein kleines Plus von null Komma zwei Prozent.",
        "Wer über dem Sparerpauschbetrag liegt, zahlt Steuer. Dann bleiben zwei Komma null acht Prozent, und real ein Minus von null Komma fünf.",
        "Es ist also knapp, und über dem Freibetrag reicht es nicht.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
