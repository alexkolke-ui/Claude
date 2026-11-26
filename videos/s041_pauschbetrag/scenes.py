"""Short 041 · Zahl der Woche: 1.230 € Arbeitnehmer-Pauschbetrag (aus Video 011)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN
from lib.shorts import SIZE, zahl
from videos.v011_steuererklaerung.scenes import ANP, BREAK_KM

assert ANP == 1230 and 14.7 < BREAK_KM < 14.72

draw = zahl("1.230 €", "bekommt jeder automatisch", "Arbeitnehmer-Pauschbetrag für Werbungskosten",
            [(1, "auch ohne Steuererklärung", "✓", GREEN), (2, "Pendeln lohnt sich ab", "≈ 15 km", BLUE),
             (3, "je Euro darüber zurück", "≈ Steuersatz", FG)],
            None, (4, "Steuererklärung: Video auf dem Kanal"), "§ 9a EStG · Entfernungspauschale 0,38 € · 220 Tage")


def scenes():
    return [Scene("short", [
        "Tausendzweihundertdreißig Euro. So viel Werbungskosten bekommt jeder Arbeitnehmer automatisch angerechnet.",
        "Auch ohne Steuererklärung.",
        "Mit dem Arbeitsweg allein liegst du bei zweihundertzwanzig Arbeitstagen erst ab knapp fünfzehn Kilometern darüber.",
        "Und für jeden Euro darüber bekommst du ungefähr deinen persönlichen Steuersatz zurück.",
        "Was das in Euro bringt, siehst du im Video auf dem Kanal.",
    ], draw, extra=1.5)]
