"""Short 053 · Zahl der Woche: 2,83 % Festgeld (aus Video 014)."""
from lib.engine import Scene
from lib.gfx import BLUE, GRAY, GREEN, VIOLET
from lib.shorts import SIZE, zahl
from videos.v014_festgeld_tagesgeld.scenes import F1, F2, F3, M, TG

assert (TG[M], F1[M], F2[M], F3[M]) == (0.52, 2.39, 2.78, 2.83)
p = lambda v: f"{v:.2f} %".replace(".", ",")

draw = zahl("2,83 %", "Festgeld über 2 Jahre, Ø", "Durchschnittszinsen September 2026",
            [(1, "Tagesgeld & Giro (Ø)", p(TG[M]), GRAY), (2, "Festgeld bis 1 Jahr", p(F1[M]), BLUE),
             ((2, 1.0), "Festgeld 1 bis 2 Jahre", p(F2[M]), VIOLET)],
            None, (3, "Festgeld oder Tagesgeld: Video am 11. Februar"), "Bundesbank, MFI-Zinsstatistik · vorläufig", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Zwei Komma acht drei Prozent. So viel brachte Festgeld über mehr als zwei Jahre im September zweitausendsechsundzwanzig im Schnitt.",
        "Täglich verfügbares Geld, also Tagesgeld und Girokonten, brachte im Schnitt nur null Komma fünf zwei Prozent.",
        "Festgeld bis ein Jahr lag bei zwei Komma drei neun, ein bis zwei Jahre bei zwei Komma sieben acht Prozent.",
        "Was davon nach Inflation bleibt, siehst du im Video am elften Februar.",
    ], draw, extra=2.0)]
