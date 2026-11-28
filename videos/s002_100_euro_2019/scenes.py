"""Short 002 (1080x1920): Was sind 100 € von 2019 heute wert? (aus Video 002, Destatis-Daten)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, card, ease_in_out, eur, lerp, prog, rrect, text, text_pop
from videos.v002_inflation_gehalt.scenes import COST_100, CPI_19_25, NOM_19_25, VALUE_100, pct

SIZE = (1080, 1920)
CX = 500

assert 22.45 < 100 * CPI_19_25 < 22.55 and 122 < COST_100 < 123 and 81.5 < VALUE_100 < 82.5
assert 21.5 < 100 * NOM_19_25 < 22.5 and NOM_19_25 < CPI_19_25


def draw(img, d, t, S):
    text_pop(d, (CX, 250), "100 € von 2019", t, S.c(0), 84, FG, "mm", "Black")
    text_pop(d, (CX, 330), "Was sind sie heute noch wert?", t, S.c(0) + 0.3, 40, MUTED, "mm", "SemiBold")
    a = prog(t, S.c(0) + 0.5, 0.6)
    if a > 0:
        p = prog(t, S.c(3), 1.6, ease_in_out)
        card(d, (110, 420, 890, 760), a, AMBER if p > 0 else (156, 163, 175))
        text(d, (CX, 490), "Kaufkraft 2025" if p > 0.5 else "im Jahr 2019", 36, MUTED, a, "mm", "SemiBold")
        text(d, (CX, 620), eur(lerp(100, VALUE_100, p), 2), 130, AMBER if p > 0 else FG, a, "mm", "Black")
    a1 = prog(t, S.c(1), 0.5)
    text(d, (130, 850), "Preise 2019 → 2025", 36, FG, a1, "lm", "SemiBold")
    text(d, (870, 850), pct(100 * CPI_19_25), 48, RED, a1, "rm", "Black")
    a2 = prog(t, S.c(2), 0.5)
    text(d, (130, 930), "100 € Einkauf kostet heute", 36, FG, a2, "lm", "SemiBold")
    text(d, (870, 930), "≈ " + eur(COST_100, 2), 48, RED, a2, "rm", "Black")

    a4 = prog(t, S.c(4), 0.5)
    if a4 > 0:
        text(d, (130, 1040), "Und die Löhne?", 40, FG, a4, "lm", "Bold")
        for i, (name, val, col) in enumerate((("Löhne", NOM_19_25, GREEN), ("Preise", CPI_19_25, RED))):
            y = 1090 + i * 100
            w = 400 * prog(t, S.c(4) + 0.4 + i * 0.3, 0.8, ease_in_out) * val / CPI_19_25
            text(d, (130, y + 40), name, 32, MUTED, a4, "lm", "SemiBold")
            if w > 1:
                rrect(d, (260, y + 10, 260 + w, y + 70), 12, fill=col)
            text(d, (870, y + 40), pct(100 * val), 40, col, a4, "rm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1340), "Ganze Rechnung:", 44, FG, a5, "mm", "Bold")
    text(d, (CX, 1400), "Video auf dem Kanal", 44, AMBER, a5, "mm", "Black")
    text(d, (CX, 1460), "Quelle: Destatis, Tabellen 61111-0001 & 62361-0020", 22, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Was sind hundert Euro von zweitausendneunzehn heute noch wert?",
        "Laut Statistischem Bundesamt sind die Verbraucherpreise seit zweitausendneunzehn um zweiundzwanzigeinhalb Prozent gestiegen.",
        "Was damals hundert Euro gekostet hat, kostet heute gut hundertzweiundzwanzig Euro.",
        "Dein Hunderter von damals ist also nur noch rund zweiundachtzig Euro wert.",
        "Und die Löhne? Die sind im selben Zeitraum um rund zweiundzwanzig Prozent gestiegen. Knapp zu wenig.",
        "Die ganze Rechnung, mit allen Daten, findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
