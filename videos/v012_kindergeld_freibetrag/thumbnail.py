"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v012_kindergeld_freibetrag/thumbnail.png",
          "Kindergeld oder", "Freibetrag?",
          [("Kindergeld", "3.108 €", GREEN), ("Freibeträge", "9.756 €", BLUE)],
          ("Freibetrag lohnt ab", "86.100 €", "zu verst. Einkommen", (202, 138, 4)), ("2026", "nachgerechnet"))
