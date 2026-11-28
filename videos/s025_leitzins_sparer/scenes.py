"""Short 025 · Mythos: Höhere Leitzinsen = mehr Zinsen fürs Konto (aus Video 008)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GREEN, RED, VIOLET
from lib.shorts import SIZE, mythos
from videos.v008_2026_in_zahlen.scenes import BAU, DISPO, EZB, TG

d = lambda s: s["2026-09"] - s["2026-01"]
assert round(d(EZB), 2) == 0.5 and round(d(TG), 2) == 0.09 and round(d(DISPO), 2) == 0.29 and round(d(BAU), 2) == 0.33
pp = lambda v: f"+{v:.2f}".replace(".", ",") + " Pkt."

draw = mythos(["„Steigt der Leitzins,", "steigen auch meine Zinsen.“"],
              [(2, "EZB-Einlagesatz", pp(d(EZB)), VIOLET), (3, "Ø Tagesgeld & Giro", pp(d(TG)), GREEN),
               ((4, 0.0), "Ø Dispo", pp(d(DISPO)), RED), ((4, 0.8), "Ø Baukredit", pp(d(BAU)), BLUE)],
              (5, [("Kredite steigen schneller", None), ("als Sparzinsen", AMBER)]),
              (6, "2026 in Zahlen: Video am 31.12."),
              "Januar → September 2026 · Bundesbank SU0200, SUD101, SUD112, SUD118",
              rows_head="Januar → September 2026")


def scenes():
    return [Scene("short", [
        "Steigt der Leitzins, steigen auch die Zinsen auf meinem Konto. Stimmt das?",
        "Zweitausendsechsundzwanzig hat die EZB die Zinsen erhöht. Schauen wir, was wo ankam.",
        "Der Einlagesatz der EZB stieg von Januar bis September um null Komma fünf Prozentpunkte.",
        "Der Durchschnittszins auf Tagesgeld und Girokonto nur um null Komma null neun.",
        "Der Dispo stieg dagegen um null Komma zwei neun Punkte und der Baukredit um null Komma drei drei.",
        "Kreditzinsen sind also schneller gestiegen als Sparzinsen.",
        "Den ganzen Jahresrückblick gibt es am einunddreißigsten Dezember auf dem Kanal.",
    ], draw, extra=1.0)]
