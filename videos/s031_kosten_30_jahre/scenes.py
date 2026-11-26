"""Short 031 · Vergleich: 1,0 % vs. 0,5 % Kosten über 30 Jahre (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v009_altersvorsorgedepot.scenes import END_05, END_1, PAID, ZUL_SUM

assert PAID == 54000 and ZUL_SUM == 16200 and 131000 < END_1 < 131500 and 142500 < END_05 < 143000

draw = vergleich("Was Kosten ausmachen", "150 €/Monat + Zulage, 30 Jahre, 5 % Rendite angenommen",
                 [(2, "1,0 % Kosten", RED, [("eingezahlt + Zulage", eur(PAID + ZUL_SUM), FG), ("Depot nach 30 J.", "≈ " + eur(round(END_1, -2)), RED)]),
                  (3, "0,5 % Kosten", GREEN, [("eingezahlt + Zulage", eur(PAID + ZUL_SUM), FG), ("Depot nach 30 J.", "≈ " + eur(round(END_05, -2)), GREEN)])],
                 (4, [("Ein halbes Prozent:", None), ("gut 11.000 € Unterschied", AMBER)]),
                 (5, "Ganze Rechnung: Video auf dem Kanal"), "Modellrechnung, keine Prognose · Kurse können auch fallen")


def scenes():
    return [Scene("short", [
        "Was machen ein halbes Prozent Kosten im neuen Altersvorsorgedepot aus?",
        "Hundertfünfzig Euro im Monat plus Zulage, dreißig Jahre lang. Wir nehmen fünf Prozent Rendite pro Jahr an, das ist keine Prognose.",
        "Bei einem Prozent Kosten, der Obergrenze im Standarddepot, stünden am Ende rund hunderteinunddreißigtausend Euro im Depot.",
        "Bei einem halben Prozent Kosten rund hundertzweiundvierzigtausendachthundert Euro.",
        "Ein halbes Prozent macht also gut elftausend Euro Unterschied.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
