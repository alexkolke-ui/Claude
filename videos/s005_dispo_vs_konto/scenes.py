"""Short 005 (1080x1920): 2.000 € im Dispo vs. auf dem Konto (aus Video 004, Bundesbank-Daten)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, card, ease_in_out, eur, lerp, prog, text, text_pop
from videos.v004_kredite.scenes import DEPO_GAIN, DISPO_AMT, DISPO_COST, D_NOW, E_NOW, K_NOW, pct

SIZE = (1080, 1920)
CX = 500

assert DISPO_AMT == 2000 and DISPO_COST == 191.8 and round(DEPO_GAIN, 2) == 10.4
assert D_NOW == 9.59 and E_NOW == 0.52 and K_NOW == 17.56 and 18 < D_NOW / E_NOW < 19


def draw(img, d, t, S):
    text_pop(d, (CX, 250), "2.000 € für ein Jahr", t, S.c(0), 80, FG, "mm", "Black")
    text_pop(d, (CX, 325), "Durchschnittszinsen in Deutschland", t, S.c(0) + 0.3, 36, MUTED, "mm", "SemiBold")
    for start, y, lab, rate, val, col, sign in ((S.c(1), 420, "auf dem Konto", E_NOW, DEPO_GAIN, GREEN, "+"),
                                                (S.c(2), 760, "im Dispo", D_NOW, DISPO_COST, RED, "−")):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        card(d, (110, y, 890, y + 290), a, col)
        text(d, (150, y + 70), lab, 44, FG, a, "lm", "Bold")
        text(d, (850, y + 70), pct(rate), 44, col, a, "rm", "Black")
        p = prog(t, start + 0.4, 1.0, ease_in_out)
        text(d, (CX, y + 190), sign + eur(lerp(0, val, p), 2), 100, col, a, "mm", "Black")
    a3 = prog(t, S.c(3), 0.5)
    text(d, (CX, 1130), f"Dispo: mehr als {int(D_NOW / E_NOW)}-mal so viel", 48, AMBER, a3, "mm", "Black")
    a4 = prog(t, S.c(4), 0.5)
    text(d, (CX, 1230), f"Kreditkarte: {pct(K_NOW)}", 48, RED, a4, "mm", "Black")
    a5 = prog(t, S.c(5), 0.5)
    text(d, (CX, 1420), "Ganze Rechnung: Video auf dem Kanal", 36, AMBER, a5, "mm", "Bold")
    text(d, (CX, 1465), "Bundesbank SUD101, SUD112, SUD132 · Sept. 2026 · ohne Zinseszins", 22, MUTED,
         prog(t, S.c(1), 0.5), "mm", "Medium")


def scenes():
    return [Scene("short", [
        "Zweitausend Euro, ein Jahr lang. Einmal auf dem Konto, einmal im Dispo.",
        "Auf dem Konto bringen sie beim Durchschnittszins von null Komma fünf zwei Prozent zehn Euro vierzig.",
        "Im Dispo kosten sie beim Durchschnittszins von neun Komma fünf neun Prozent rund hunderteinundneunzig Euro achtzig.",
        "Das ist mehr als achtzehnmal so viel.",
        "Bei der Kreditkarte liegt der Durchschnittszins sogar bei siebzehn Komma fünf sechs Prozent.",
        "Was Ratenkredit und Baufinanzierung kosten, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=1.0)]
