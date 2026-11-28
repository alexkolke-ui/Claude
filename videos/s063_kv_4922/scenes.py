"""Short 063 · Zahl der Woche: +49,22 € Krankenversicherung (aus Video 016)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, RED, eur
from lib.shorts import SIZE, zahl
from videos.v016_krankenkasse_2027.scenes import BBG26, BBG27, MAX26, MAX27

assert round(MAX27 - MAX26, 2) == 49.22 and (BBG26, BBG27) == (5812.50, 6375.00)

draw = zahl("+49,22 €", "mehr Krankenkasse im Monat", "für Gutverdiener 2027 – bei gleichem Beitragssatz",
            [(1, "Beitragsgrenze 2026", eur(BBG26, 2), FG), ((1, 1.0), "Beitragsgrenze 2027", eur(BBG27, 2), RED),
             (2, "Höchstbeitrag 2027", eur(MAX27, 2), RED)],
            (3, [("Beitragssatz gleich –", None), ("Grenze höher", AMBER)]),
            (4, "Krankenkasse 2027: Video am 25. Februar"), "BBG 2027 vorläufig · Ø-Zusatzbeitrag 2,9 % (BMG)", big_color=RED)


def scenes():
    return [Scene("short", [
        "Neunundvierzig Euro zweiundzwanzig. So viel mehr zahlen Gutverdiener zweitausendsiebenundzwanzig im Monat für die Krankenkasse.",
        "Der Grund: Die Beitragsgrenze steigt vorläufig von fünftausendachthundertzwölf Euro fünfzig auf sechstausenddreihundertfünfundsiebzig Euro.",
        "Der Höchstbeitrag steigt damit von fünfhundertacht auf fünfhundertsiebenundfünfzig Euro.",
        "Und das, obwohl der durchschnittliche Beitragssatz gleich bleibt.",
        "Wer betroffen ist, siehst du im Video am fünfundzwanzigsten Februar.",
    ], draw, extra=1.5)]
