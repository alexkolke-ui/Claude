"""1280x720 thumbnail."""
import sys
sys.path.insert(0, ".")
from lib.gfx import BLUE, GREEN
from lib.thumb import thumbnail

thumbnail(sys.argv[1] if len(sys.argv) > 1 else "output/v009_altersvorsorgedepot/thumbnail.png",
          "Altersvorsorge-", "depot 2027",
          [("10 €/Monat", "+50 %", GREEN), ("150 €/Monat", "+540 €", BLUE)],
          ("Zulage bis", "540 €", "pro Jahr vom Staat", (16, 150, 105)), ("neu ab 2027", "offizielle Regeln"))
