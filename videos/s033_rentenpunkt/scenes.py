"""Short 033 · Zahl der Woche: 42,52 € pro Rentenpunkt (aus Video 010)."""
from lib.engine import Scene
from lib.gfx import BLUE, FG, GREEN, eur
from lib.shorts import SIZE, zahl
from videos.v010_gesetzliche_rente.scenes import DE, RW, STD

assert RW == 42.52 and DE == 51944 and round(STD, 2) == 1913.40

draw = zahl("42,52 €", "Monatsrente pro Entgeltpunkt", "aktueller Rentenwert seit 1. Juli 2026",
            [(1, "1 Punkt = 1 Jahr mit", eur(DE), FG), (2, "45 Punkte (Standardrente)", eur(STD, 2), GREEN)],
            (3, [("Dein Gehalt ÷ Durchschnitt", None), ("= deine Punkte pro Jahr", BLUE)]),
            (4, "Gesetzliche Rente: Video am 14. Januar"), "Quellen: DRV, Rentenwertbestimmungsverordnung 2026", big_color=BLUE)


def scenes():
    return [Scene("short", [
        "Zweiundvierzig Euro zweiundfünfzig. So viel Monatsrente bringt ein Rentenpunkt seit Juli zweitausendsechsundzwanzig.",
        "Einen Punkt bekommst du für ein Jahr mit Durchschnittsverdienst, vorläufig einundfünfzigtausendneunhundertvierundvierzig Euro brutto.",
        "Fünfundvierzig Punkte ergeben die sogenannte Standardrente: tausendneunhundertdreizehn Euro vierzig im Monat.",
        "Deine Punkte pro Jahr: dein Gehalt geteilt durch den Durchschnitt.",
        "Was dein Gehalt bringt, rechnen wir im Video am vierzehnten Januar durch.",
    ], draw, extra=1.5)]
