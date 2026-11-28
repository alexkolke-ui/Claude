"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v013_mindestlohn_2027/thumbnail.png",
          "Mindestlohn", "2027: 14,60 €",
          [("Vollzeit brutto", "2.531 €", BLUE), ("netto ≈", "1.787 €", GREEN)],
          ("seit 2015 real", "+20 %", "mehr Kaufkraft", (16, 150, 105)), ("2027", "nachgerechnet"))
