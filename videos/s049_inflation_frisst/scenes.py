"""Short 049 · Mythos: Die Inflation hat die Mindestlohn-Erhöhungen aufgefressen (aus Video 013)."""
from lib.engine import Scene
from lib.gfx import AMBER, GREEN, RED
from lib.shorts import SIZE, mythos
from videos.v013_mindestlohn_2027.scenes import NOM, PRICE, REAL

assert 0.635 < NOM < 0.636 and 0.358 < PRICE < 0.36 and 0.20 < REAL < 0.21
p = lambda v: f"+{v * 100:.1f} %".replace(".", ",")

draw = mythos(["„Die Inflation hat den", "Mindestlohn aufgefressen.“"],
              [(2, "Mindestlohn 2015 → 2026", p(NOM), GREEN), (3, "Preise Jan. 2015 → Okt. 2026", p(PRICE), RED),
               ((3, 1.2), "Kaufkraft", f"+{REAL * 100:.0f} %", AMBER)],
              (4, [("Real: rund 20 %", GREEN), ("mehr Kaufkraft", None)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"), "Verbraucherpreisindex (Bundesbank BBDP1, Destatis) · MiLoG")


def scenes():
    return [Scene("short", [
        "Die Inflation hat die Erhöhungen beim Mindestlohn doch komplett aufgefressen. Stimmt das?",
        "Rechnen wir nach.",
        "Von zweitausendfünfzehn bis zweitausendsechsundzwanzig stieg der Mindestlohn von acht Euro fünfzig auf dreizehn Euro neunzig, ein Plus von dreiundsechzig Komma fünf Prozent.",
        "Die Preise stiegen im selben Zeitraum um fünfunddreißig Komma neun Prozent. Real bleibt ein Plus von rund zwanzig Prozent.",
        "Die Kaufkraft des Mindestlohns ist also deutlich gestiegen.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
