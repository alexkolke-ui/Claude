"""Short 017 · Mythos: Wer den Spitzensteuersatz erreicht, zahlt 42 % auf alles (aus Video 006)."""
from lib.engine import Scene
from lib.gfx import AMBER, FG, GREEN, MUTED, RED, eur
from lib.lohn2026 import uptab26
from lib.shorts import SIZE, mythos

ZVE = 80000
EST = int(uptab26(ZVE))
AVG = EST / ZVE * 100
assert EST == 22464 and 28.0 < AVG < 28.1
assert uptab26(80000) - uptab26(79000) == 420 and uptab26(69000) - uptab26(68000) < 420   # 42 % erst oberhalb der Grenze

draw = mythos(["„Ab dem Spitzensteuersatz", "gehen 42 % weg.“"],
              [(2, "Einkommen (zvE)", eur(ZVE), FG),
               (3, "Einkommensteuer 2026", eur(EST), RED),
               ((3, 1.2), "Durchschnittssteuersatz", f"{AVG:.1f} %".replace(".", ","), GREEN)],
              (4, [("42 % gelten nur für", None), ("den Teil über 69.878 €", AMBER)]),
              (5, "Brutto, netto: Video auf dem Kanal"),
              "§ 32a EStG, Grundtarif 2026 (BMF-Programmablaufplan) · ohne Soli")


def scenes():
    return [Scene("short", [
        "Wer den Spitzensteuersatz erreicht, muss zweiundvierzig Prozent seines Einkommens abgeben. Stimmt das?",
        "Nein. Rechnen wir mit dem Steuertarif für zweitausendsechsundzwanzig.",
        "Nehmen wir achtzigtausend Euro zu versteuerndes Einkommen, also schon über der Grenze zum Spitzensteuersatz.",
        "Die Einkommensteuer beträgt zweiundzwanzigtausendvierhundertvierundsechzig Euro. Das sind im Schnitt nur rund achtundzwanzig Prozent.",
        "Die zweiundvierzig Prozent gelten nur für den Teil des Einkommens über neunundsechzigtausendachthundertachtundsiebzig Euro.",
        "Was vom Brutto wirklich bleibt, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=1.0)]
