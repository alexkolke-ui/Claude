"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v010_gesetzliche_rente/thumbnail.png",
          "Wie viel Rente", "bringt dein Gehalt?",
          [("Brutto heute", "3.000 €", GREEN), ("Rentenwert", "42,52 €", BLUE)],
          ("Rente nach 45 J.", "1.326 €", "brutto, heutige Werte", (37, 99, 235)), ("2026", "offizielle Werte"))
