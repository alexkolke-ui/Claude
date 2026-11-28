"""Short 058 · Zahl der Woche: 9,59 % „Rendite“ durch Dispo-Tilgung (aus Video 015)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GRAY, GREEN, RED
from lib.shorts import SIZE, zahl
from videos.v015_sondertilgung.scenes import B10_NOW, D_NOW, FGZ, R_NOW, TG, M

assert (D_NOW, R_NOW, B10_NOW, FGZ, TG[M]) == (9.59, 8.91, 3.91, 2.83, 0.52)
p = lambda v: f"{v:.2f} %".replace(".", ",")

draw = zahl("9,59 %", "„Rendite“, wenn du den Dispo tilgst", "Jeder getilgte Euro spart den Kreditzins · Ø Sept. 2026",
            [(1, "Ratenkredit (Ø, eff.)", p(R_NOW), RED), ((1, 1.0), "Baukredit 5–10 J.", p(B10_NOW), BLUE),
             (2, "Festgeld > 2 J.", p(FGZ), GREEN), ((2, 1.0), "Tagesgeld & Giro", p(TG[M]), GRAY)],
            (3, [("Erst Schulden tilgen,", None), ("dann sparen", AMBER)]),
            (4, "Tilgungs-Leiter: Video am 18. Februar"), "Bundesbank MFI-Zinsstatistik · keine Beratung", big_color=RED)


def scenes():
    return [Scene("short", [
        "Neun Komma fünf neun Prozent, sicher und steuerfrei. So viel bringt es im Schnitt, wenn du deinen Dispo zurückzahlst.",
        "Denn jeder getilgte Euro spart genau den Zins, den er sonst kosten würde. Beim Ratenkredit sind das im Schnitt acht Komma neun eins Prozent, beim Baukredit drei Komma neun eins.",
        "Zum Vergleich: Festgeld bringt im Schnitt zwei Komma acht drei, Tagesgeld und Girokonto null Komma fünf zwei Prozent.",
        "Teure Schulden zu tilgen bringt also meist mehr als zu sparen. Ein Notgroschen sollte trotzdem bleiben.",
        "Die ganze Tilgungs-Leiter gibt es im Video am achtzehnten Februar.",
    ], draw, extra=1.0)]
