"""Short 011 · Mythos: Miete ist rausgeworfenes Geld (aus Video 005)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN, RED, eur
from lib.shorts import SIZE, mythos
from videos.v005_mieten_kaufen.scenes import BE, CASES, RENTER, pct

assert 0.015 < BE < 0.016 and 175000 < RENTER < 176500
assert 123000 < CASES[0][1] < 124500 and 192000 < CASES[2][1] < 193000

draw = mythos(["„Miete ist rausgeworfenes", "Geld – Kaufen lohnt immer.“"],
              [(2, "Mieter", "≈ " + eur(round(RENTER, -2)), GREEN),
               (3, "Käufer, 0 % p. a.", "≈ " + eur(round(CASES[0][1], -2)), RED),
               (3.0 if False else (3, 1.2), "Käufer, 2 % p. a.", "≈ " + eur(round(CASES[2][1], -2)), BLUE)],
              (4, [("Gleichstand bei", FG), (f"≈ {pct(100 * BE)} Wertzuwachs p. a.", AMBER)]),
              (5, "Ganze Rechnung: Video auf dem Kanal"),
              "Modellrechnung, Annahmen in der Beschreibung · keine Beratung",
              rows_head="Vermögen nach 10 Jahren")


def scenes():
    return [Scene("short", [
        "Miete ist rausgeworfenes Geld, Kaufen lohnt sich immer. Stimmt das?",
        "Wir vergleichen zwei Menschen mit denselben monatlichen Ausgaben über zehn Jahre.",
        "Der Mieter legt sein Eigenkapital und die Differenz zur Miete an. Er hat am Ende rund hundertfünfundsiebzigtausendsiebenhundert Euro.",
        "Der Käufer hat bei gleichbleibendem Wohnungswert netto nur rund hundertdreiundzwanzigtausendachthundert Euro. Steigt der Wert um zwei Prozent pro Jahr, sind es rund hundertzweiundneunzigtausendvierhundert.",
        "Gleichstand gibt es in unserer Rechnung erst bei gut eineinhalb Prozent Wertsteigerung pro Jahr.",
        "Alle Annahmen und die ganze Rechnung findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
