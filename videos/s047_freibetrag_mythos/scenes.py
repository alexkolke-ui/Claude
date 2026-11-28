"""Short 047 · Mythos: Der Kinderfreibetrag spart 9.756 € Steuern (aus Video 012)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, eur
from lib.shorts import SIZE, mythos
from videos.v012_kindergeld_freibetrag.scenes import EX, KFB

assert KFB == 9756 and [s for _, s in EX] == [2668, 3344, 4098]

draw = mythos(["„Der Kinderfreibetrag spart", "mir 9.756 € Steuern.“"],
              [(2, "bei 60.000 €", eur(EX[0][1]), FG), ((2, 1.0), "bei 100.000 €", eur(EX[1][1]), BLUE),
               ((2, 2.0), "bei 150.000 €", eur(EX[2][1]), GREEN)],
              (3, [("Freibetrag ≠ Steuer:", None), ("er senkt das Einkommen", AMBER)]),
              (4, "Ganze Rechnung: Video auf dem Kanal"), "Tarif 2026, Splitting · ohne Soli/Kirchensteuer",
              rows_head="tatsächliche Steuerersparnis")


def scenes():
    return [Scene("short", [
        "Der Kinderfreibetrag spart mir neuntausendsiebenhundertsechsundfünfzig Euro Steuern. Ein häufiges Missverständnis.",
        "Der Freibetrag senkt nur das Einkommen, auf das Steuer fällig wird. Gespart wird dein Steuersatz auf diesen Betrag.",
        "Für Eltern mit einem Kind: bei sechzigtausend Euro zu versteuerndem Einkommen zweitausendsechshundertachtundsechzig Euro, bei hunderttausend dreitausenddreihundertvierundvierzig, bei hundertfünfzigtausend viertausendachtundneunzig Euro.",
        "Ein Freibetrag ist also keine Steuer, sondern weniger Einkommen, auf das Steuer anfällt.",
        "Die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
