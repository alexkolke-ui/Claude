"""Short 065 · Mythos: Die Krankenkasse wird nur teurer, wenn der Beitragssatz steigt (aus Video 016)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, RED, eur
from lib.shorts import SIZE, mythos
from videos.v016_krankenkasse_2027.scenes import BBG26, BBG27, MAX26, MAX27

assert round(MAX27 - MAX26, 2) == 49.22 and BBG27 - BBG26 == 562.5

draw = mythos(["„Teurer wird es nur, wenn", "der Beitragssatz steigt.“"],
              [(2, "Ø-Beitragssatz", "17,5 % (gleich)", GREEN), (3, "Beitragsgrenze", "+562,50 €", RED),
               ((3, 1.2), "Höchstbeitrag", "+49,22 €", RED)],
              (4, [("Auch die Grenze", None), ("macht's teurer", AMBER)]),
              (5, "Krankenkasse 2027: Video auf dem Kanal"), "BBG 2027 vorläufig · Ø-Zusatzbeitrag 2,9 % (BMG)")


def scenes():
    return [Scene("short", [
        "Die Krankenkasse wird nur teurer, wenn der Beitragssatz steigt. Stimmt nicht.",
        "Zweitausendsiebenundzwanzig zeigt es.",
        "Der durchschnittliche Beitragssatz bleibt bei siebzehn Komma fünf Prozent.",
        "Aber die Beitragsgrenze steigt um fünfhundertzweiundsechzig Euro fünfzig im Monat. Wer gut verdient, zahlt dadurch bis zu neunundvierzig Euro zweiundzwanzig mehr.",
        "Auch die Grenze kann es also teurer machen.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
