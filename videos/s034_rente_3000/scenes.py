"""Short 034 · Was kostet X: Welche Rente bringen 3.000 € brutto? (aus Video 010)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, VIOLET, eur
from lib.shorts import SIZE, zahl
from videos.v010_gesetzliche_rente.scenes import EP1, EP45, R, RW

assert round(EP1, 4) == 0.6931 and round(EP45, 2) == 31.19 and round(R, 2) == 1326.09
d = lambda v, n: f"{v:.{n}f}".replace(".", ",")

draw = zahl(eur(R, 2), "Rente aus 3.000 € brutto", "nach 45 Jahren, in heutigen Werten, brutto",
            [(1, "Punkte pro Jahr", d(EP1, 4), BLUE), ((1, 1.5), "nach 45 Jahren", d(EP45, 2), VIOLET),
             (2, "× Rentenwert", eur(RW, 2), FG)],
            None, (3, "Und netto? Video auf dem Kanal"), "Rentenwert 42,52 € · vorl. Durchschnittsentgelt 2026: 51.944 €",
            big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Wie viel gesetzliche Rente bringen dreitausend Euro brutto im Monat?",
        "Dreitausend Euro sind sechsunddreißigtausend im Jahr, also null Komma sechs neun drei eins Rentenpunkte pro Jahr. Nach fünfundvierzig Jahren sind das einunddreißig Komma eins neun Punkte.",
        "Mal zweiundvierzig Euro zweiundfünfzig ergibt tausenddreihundertsechsundzwanzig Euro Rente im Monat, in heutigen Werten.",
        "Was davon netto bleibt, siehst du im Video auf dem Kanal.",
    ], draw, extra=2.0)]
