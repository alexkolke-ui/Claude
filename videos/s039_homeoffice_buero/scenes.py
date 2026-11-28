"""Short 039 · Vergleich: Homeoffice-Tag vs. Bürotag (aus Video 011)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, VIOLET
from lib.shorts import SIZE, vergleich
from videos.v011_steuererklaerung.scenes import HO_MAX, HO_TAG, HO_VS_KM, KM_SATZ

assert HO_TAG == 6 and HO_MAX == 1260 and 20 * KM_SATZ == 7.6 and 15.7 < HO_VS_KM < 15.8

draw = vergleich("Homeoffice oder Büro?", "Was ein Tag in der Steuererklärung 2026 zählt",
                 [(1, "Homeoffice", VIOLET, [("pro Tag", "6,00 €", VIOLET), ("maximal", "1.260 €/Jahr", FG)]),
                  (2, "Büro, 20 km", BLUE, [("pro Tag", "7,60 €", BLUE), ("Rechnung", "20 × 0,38 €", FG)])],
                 (3, [("Ab knapp 16 km", None), ("zählt der Bürotag mehr", AMBER)]),
                 (4, "Steuererklärung: Video auf dem Kanal"), "Homeoffice-Pauschale & Entfernungspauschale 2026 · nur eins pro Tag")


def scenes():
    return [Scene("short", [
        "Homeoffice oder Büro: Was bringt in der Steuererklärung mehr?",
        "Ein Homeoffice-Tag zählt sechs Euro, höchstens tausendzweihundertsechzig Euro im Jahr.",
        "Ein Bürotag bei zwanzig Kilometern zählt sieben Euro sechzig. Für denselben Tag gibt es nur eins von beidem.",
        "Ab knapp sechzehn Kilometern Arbeitsweg zählt der Bürotag also mehr.",
        "Was am Ende zurückkommt, rechnen wir im Video auf dem Kanal durch.",
    ], draw, extra=1.5)]
