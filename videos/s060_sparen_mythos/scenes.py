"""Short 060 · Mythos: Sparen ist immer besser als Schulden tilgen (aus Video 015)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GRAY, GREEN, RED
from lib.shorts import SIZE, mythos
from videos.v015_sondertilgung.scenes import B10_NOW, D_NOW, FG_NET, TG, M

assert (D_NOW, B10_NOW, TG[M]) == (9.59, 3.91, 0.52) and round(FG_NET, 2) == 2.08
p = lambda v: f"{v:.2f} %".replace(".", ",")

draw = mythos(["„Sparen ist immer besser", "als Schulden tilgen.“"],
              [(2, "Dispo tilgen spart", p(D_NOW), RED), ((2, 1.0), "Baukredit tilgen spart", p(B10_NOW), BLUE),
               (3, "Festgeld nach Steuer", p(FG_NET), GREEN), ((3, 1.0), "Tagesgeld & Giro", p(TG[M]), GRAY)],
              (4, [("Teure Schulden zuerst –", None), ("Notgroschen behalten", AMBER)]),
              (5, "Tilgungs-Leiter: Video auf dem Kanal"), "Durchschnittszinsen Sept. 2026 · Bundesbank · keine Beratung",
              rows_head="was ein Euro bringt")


def scenes():
    return [Scene("short", [
        "Sparen ist immer besser als Schulden tilgen. Stimmt das?",
        "Vergleichen wir, was ein Euro im Schnitt bringt.",
        "Einen Euro Dispo zurückzahlen spart neun Komma fünf neun Prozent, beim Baukredit drei Komma neun eins.",
        "Ein Euro als Festgeld bringt über dem Freibetrag nach Steuern zwei Komma null acht Prozent, auf Tagesgeld und Girokonto im Schnitt null Komma fünf zwei.",
        "Teure Schulden zu tilgen lohnt sich also meist mehr. Ein Notgroschen sollte aber immer bleiben.",
        "Die ganze Tilgungs-Leiter findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
