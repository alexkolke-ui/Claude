"""Short 057 · Vergleich: Festgeld-Bindung – Glück und Pech (aus Video 014)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v014_festgeld_tagesgeld.scenes import F2, LOCK_GAIN, TG_GAIN

assert F2["2023-12"] == 3.25 and F2["2022-01"] == 0.22 and round(LOCK_GAIN) == 661 and round(TG_GAIN) == 106

draw = vergleich("Festgeld festlegen", "1 bis 2 Jahre Laufzeit, Durchschnittszinsen",
                 [(1, "Dez. 2023", GREEN, [("Zins", "3,25 %", GREEN), ("10.000 € / 2 J.", "+" + eur(LOCK_GAIN), GREEN),
                                           ("Tagesgeld Ø", "+" + eur(TG_GAIN), FG)]),
                  (3, "Jan. 2022", RED, [("Zins", "0,22 %", RED), ("ein Jahr später", "über 2 %", FG), ("Ende 2023", "3,25 %", FG)])],
                 (4, [("Der Zeitpunkt", None), ("entscheidet", AMBER)]),
                 (5, "Ganze Rechnung: Video auf dem Kanal"), "Bundesbank SUD103, SUD101 · Modellrechnung")


def scenes():
    return [Scene("short", [
        "Festgeld legt den Zins fest. Das kann Glück oder Pech sein.",
        "Wer im Dezember zweitausenddreiundzwanzig für zwei Jahre festgelegt hat, bekam im Schnitt drei Komma zwei fünf Prozent. Auf zehntausend Euro rund sechshunderteinundsechzig Euro.",
        "Mit dem durchschnittlichen Tagesgeld- und Girozins wären es nur rund hundertsechs Euro gewesen.",
        "Wer im Januar zweitausendzweiundzwanzig festgelegt hat, bekam null Komma zwei zwei Prozent. Ein Jahr später gab es schon über zwei Prozent.",
        "Der Zeitpunkt entscheidet also.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
