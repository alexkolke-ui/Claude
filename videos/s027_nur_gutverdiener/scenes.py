"""Short 027 · Mythos: Die Förderung lohnt nur für Gutverdiener (aus Video 009)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, GREEN
from lib.shorts import SIZE, mythos
from videos.v009_altersvorsorgedepot.scenes import QUOTE

q = {m: p for m, _, p in QUOTE}
assert q[10] == 50 and q[50] == 40 and q[150] == 30
p = lambda v: f"{v:.0f} %"

draw = mythos(["„Die Förderung bringt", "nur Gutverdienern was.“"],
              [(2, "10 € im Monat", p(q[10]) + " Zulage", GREEN), ((2, 1.0), "50 € im Monat", p(q[50]) + " Zulage", GREEN),
               (3, "150 € im Monat", p(q[150]) + " Zulage", BLUE)],
              (4, [("Kleine Beiträge:", None), ("höchster Fördersatz", AMBER)]),
              (5, "Alle Regeln: Video auf dem Kanal"), "Grundzulage Altersvorsorgedepot ab 2027 · BMF-FAQ",
              rows_head="Grundzulage in Prozent")


def scenes():
    return [Scene("short", [
        "Die neue Förderung fürs Altersvorsorgedepot bringt nur Gutverdienern etwas. Stimmt das?",
        "Schauen wir auf die Zulage im Verhältnis zum Beitrag.",
        "Wer zehn Euro im Monat einzahlt, bekommt fünfzig Prozent dazu. Bei fünfzig Euro im Monat sind es vierzig Prozent.",
        "Bei hundertfünfzig Euro im Monat sind es nur noch dreißig Prozent.",
        "Den höchsten Fördersatz bekommen also kleine Beiträge. Gutverdiener profitieren eher über die Steuer.",
        "Alle Regeln findest du im Video auf dem Kanal.",
    ], draw, extra=1.0)]
