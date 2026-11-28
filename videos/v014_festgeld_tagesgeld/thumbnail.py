"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import GRAY, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v014_festgeld_tagesgeld/thumbnail.png",
          "Festgeld oder", "Tagesgeld?",
          [("Tagesgeld (Ø)", "0,52 %", GRAY), ("Festgeld (Ø)", "2,83 %", GREEN)],
          ("nach Inflation", "+0,2 %", "bestenfalls, vor Steuern", (202, 138, 4)), ("Ø Deutschland", "Bundesbank-Daten"))
