"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import GREEN, RED
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v016_krankenkasse_2027/thumbnail.png",
          "Krankenkasse", "2027: teurer?",
          [("Beitragssatz Ø", "17,5 %", GREEN), ("Beitragsgrenze", "+562 €", RED)],
          ("Gutverdiener zahlen", "+49 €", "mehr im Monat", (185, 28, 28)), ("2027", "nachgerechnet"))
