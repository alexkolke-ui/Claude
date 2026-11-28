"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v011_steuererklaerung/thumbnail.png",
          "Steuererklärung:", "Was kommt zurück?",
          [("Pendeln/km", "0,38 €", GREEN), ("Homeoffice/Tag", "6 €", BLUE)],
          ("bei 40 km", "≈ 570 €", "zurück pro Jahr", (16, 150, 105)), ("2026", "nachgerechnet"))
