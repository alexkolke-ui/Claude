"""Short 067 · Zahl der Woche: 12 Monate – wann man die Krankenkasse wechseln kann (aus Video 016)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GREEN
from lib.shorts import SIZE, zahl

draw = zahl("12 Monate", "Mindestdauer bei einer Krankenkasse", "danach jederzeit wechseln",
            [(1, "Kündigungsfrist", "2 Monate", FG),
             (2, "bei Erhöhung", "Sonderkündigung", AMBER), ((2, 1.2), "Frist dafür", "bis Ende des Monats", BLUE)],
            None, (3, "Krankenkasse 2027: Video auf dem Kanal"), "§ 175 SGB V · Leistungen größtenteils gesetzlich gleich",
            big_color=GREEN)


def scenes():
    return [Scene("short", [
        "Zwölf Monate. So lange musst du mindestens bei deiner Krankenkasse bleiben. Danach kannst du jederzeit wechseln.",
        "Die Kündigungsfrist beträgt zwei Monate zum Monatsende.",
        "Erhöht deine Kasse den Zusatzbeitrag, kannst du sofort kündigen, und zwar bis zum Ende des Monats, ab dem der höhere Beitrag gilt.",
        "Mehr dazu im Video auf dem Kanal.",
    ], draw, extra=2.0)]
