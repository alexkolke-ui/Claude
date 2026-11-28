"""Short 066 · Was kostet X: ein Prozentpunkt Zusatzbeitrag (aus Video 016)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, VIOLET, eur
from lib.shorts import SIZE, zahl
from videos.v016_krankenkasse_2027.scenes import PP_3000, PP_BBG

assert PP_3000 == 15 and round(PP_BBG, 2) == 31.88

draw = zahl("15 €", "pro Monat und Prozentpunkt", "Zusatzbeitrag bei 3.000 € brutto (du trägst die Hälfte)",
            [(1, "im Jahr", eur(12 * PP_3000), BLUE), (2, "ab 6.375 € brutto", eur(PP_BBG, 2) + "/Monat", VIOLET),
             (3, "pro 0,1 Punkte bei 3.000 €", "1,50 €", FG)],
            None, (4, "Krankenkasse 2027: Video auf dem Kanal"), "Unterschied Zusatzbeitrag × Brutto ÷ 2 · keine Kassenempfehlung",
            big_color=AMBER)


def scenes():
    return [Scene("short", [
        "Fünfzehn Euro im Monat. So viel macht ein Prozentpunkt Zusatzbeitrag bei dreitausend Euro brutto aus.",
        "Das sind hundertachtzig Euro im Jahr. Den anderen Teil zahlt dein Arbeitgeber.",
        "Ab der Beitragsgrenze zweitausendsiebenundzwanzig sind es einunddreißig Euro achtundachtzig im Monat.",
        "Pro null Komma eins Prozentpunkte sind es bei dreitausend Euro einen Euro fünfzig.",
        "Mehr dazu im Video auf dem Kanal.",
    ], draw, extra=1.5)]
