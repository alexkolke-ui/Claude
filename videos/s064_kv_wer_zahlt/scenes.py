"""Short 064 · Vergleich: Krankenversicherung 2027 bei 5.000 € vs. 7.000 € brutto (aus Video 016)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED, eur
from lib.shorts import SIZE, vergleich
from videos.v016_krankenkasse_2027.scenes import TAB

(_, _, _), (b5, a5, c5), _, (b7, a7, c7) = TAB
assert (b5, round(a5, 2), round(c5, 2)) == (5000, 437.5, 437.5) and (b7, round(a7, 2), round(c7, 2)) == (7000, 508.59, 557.81)

draw = vergleich("Wer 2027 mehr zahlt", "Krankenversicherung, Arbeitnehmeranteil, Ø-Zusatzbeitrag",
                 [(1, "5.000 € brutto", GREEN, [("2026", eur(a5, 2), FG), ("2027", eur(c5, 2), FG), ("Änderung", "±0 €", GREEN)]),
                  (2, "7.000 € brutto", RED, [("2026", eur(a7, 2), FG), ("2027", eur(c7, 2), FG), ("Änderung", "+49,22 €", RED)])],
                 (3, [("Betroffen nur über", None), ("5.812,50 € brutto", AMBER)]),
                 (4, "Ganze Rechnung: Video auf dem Kanal"), "BBG 2027 vorläufig · Ø-Zusatzbeitrag 2,9 %")


def scenes():
    return [Scene("short", [
        "Wer zahlt zweitausendsiebenundzwanzig mehr für die Krankenkasse?",
        "Bei fünftausend Euro brutto bleibt der Beitrag gleich: vierhundertsiebenunddreißig Euro fünfzig im Monat, wenn deine Kasse den Zusatzbeitrag nicht erhöht.",
        "Bei siebentausend Euro brutto steigt er von fünfhundertacht Euro neunundfünfzig auf fünfhundertsiebenundfünfzig Euro einundachtzig.",
        "Betroffen sind also nur Gehälter über fünftausendachthundertzwölf Euro fünfzig.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
