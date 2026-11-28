"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v015_sondertilgung/thumbnail.png",
          "Tilgen oder", "sparen?",
          [("Tilgen", "+4.775 €", BLUE), ("Festgeld", "+2.290 €", GREEN)],
          ("Dispo tilgen =", "9,59 %", "„Rendite“", (185, 28, 28)), ("10.000 €, 10 J.", "Bundesbank-Daten"))
