"""Short 056 · Zahl der Woche: bis 35.300 € Festgeld steuerfrei (aus Video 014)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED
from lib.shorts import SIZE, zahl
from videos.v014_festgeld_tagesgeld.scenes import F3, FREI_BIS, M

assert 35300 < FREI_BIS < 35400 and F3[M] == 2.83

draw = zahl("35.300 €", "Festgeld bleiben steuerfrei", "bei 2,83 % Zins und 1.000 € Sparerpauschbetrag",
            [(1, "Sparerpauschbetrag", "1.000 €/Jahr", FG), (2, "darüber: Steuer", "26,375 %", RED),
             (3, "für Paare (zusammen)", "≈ 70.600 €", GREEN)],
            None, (4, "Festgeld oder Tagesgeld: Video auf dem Kanal"), "§ 20 Abs. 9 EStG · Bundesbank SUD104", big_color=AMBER)


def scenes():
    return [Scene("short", [
        "Fünfunddreißigtausenddreihundert Euro. So viel Festgeld kannst du bei zwei Komma acht drei Prozent anlegen, ohne Steuern auf die Zinsen zu zahlen.",
        "Denn Zinsen bis tausend Euro im Jahr sind über den Sparerpauschbetrag steuerfrei.",
        "Darüber fallen sechsundzwanzig Komma vier Prozent Abgeltungsteuer und Soli an.",
        "Für zusammen veranlagte Paare gilt der doppelte Betrag, also rund siebzigtausendsechshundert Euro.",
        "Mehr dazu im Video auf dem Kanal.",
    ], draw, extra=1.5)]
