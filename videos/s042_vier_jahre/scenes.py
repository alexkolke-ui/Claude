"""Short 042 · Zahl der Woche: 4 Jahre Zeit für die freiwillige Steuererklärung (aus Video 011)."""
from lib.engine import Scene
from lib.gfx import FG, GREEN, RED
from lib.shorts import SIZE, zahl

draw = zahl("4 Jahre", "Zeit für die freiwillige Erklärung", "Steuererklärung 2026",
            [(1, "freiwillig für 2026", "bis Ende 2030", GREEN), (2, "Pflicht bis", "31.07.2027", RED),
             (3, "Pflicht z. B. bei", "StKl. III/V", FG)],
            None, (4, "Steuererklärung: Video auf dem Kanal"), "§ 46 EStG, § 149 AO, Festsetzungsfrist 4 Jahre", big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Vier Jahre. So lange hast du Zeit für eine freiwillige Steuererklärung.",
        "Die Erklärung für zweitausendsechsundzwanzig kannst du also noch bis Ende zweitausenddreißig abgeben.",
        "Wer eine Erklärung abgeben muss, hat ohne Steuerberater bis zum einunddreißigsten Juli zweitausendsiebenundzwanzig Zeit.",
        "Pflicht ist sie zum Beispiel in den Steuerklassen drei und fünf.",
        "Was zurückkommen kann, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
