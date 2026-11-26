"""Video 011: Steuererklärung 2026 – wann sie sich lohnt und was zurückkommt (Pendler, Homeoffice)."""
from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, card, dot, ease_in_out, eur, fade, lerp,
                     prog, rrect, text, text_pop)
from lib.lohn2026 import uptab26

KM_SATZ, HO_TAG, HO_MAX, ANP = 0.38, 6, 1260, 1230     # Werte 2026
TAGE = 220                                            # Annahme: Arbeitstage pro Jahr
ZVE = 27480                                           # 3.000 € brutto, StKl. I (Video 6)


def erstattung(werbungskosten):
    """Steuerersparnis gegenüber dem Pauschbetrag (Einkommensteuer 2026, ohne Soli/Kirchensteuer)."""
    extra = max(0, int(werbungskosten) - ANP)
    return int(uptab26(ZVE)) - int(uptab26(ZVE - extra)), extra


KMS = [(km, km * KM_SATZ * TAGE, *erstattung(km * KM_SATZ * TAGE)) for km in (10, 20, 30, 40)]
BREAK_KM = ANP / (KM_SATZ * TAGE)
HO_VS_KM = HO_TAG / KM_SATZ
MIX_WK = 132 * 20 * KM_SATZ + 88 * HO_TAG
MIX_REF, MIX_EXTRA = erstattung(MIX_WK)

# Every number spoken in the narration is checked here.
assert [(round(w), r) for _, w, r, _ in KMS] == [(836, 0), (1672, 120), (2508, 346), (3344, 570)]
assert 14.7 < BREAK_KM < 14.72 and 15.7 < HO_VS_KM < 15.8                      # "knapp fünfzehn", "knapp sechzehn"
assert 20 * KM_SATZ == 7.6
assert round(MIX_WK, 1) == 1531.2 and MIX_EXTRA == 301 and MIX_REF == 82
assert HO_MAX == 210 * HO_TAG

SRC = "Entfernungspauschale 2026: 0,38 €/km ab dem 1. km · Homeoffice-Pauschale 6 €/Tag, max. 1.260 € · Tarif 2026"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 160), "Steuererklärung 2026: Was kommt zurück?", t, S.c(0), 56, FG, "mm", "Black")
    for i, (st, km, r, col) in enumerate(((S.c(1), 20, KMS[1][2], GREEN), (S.c(2), 40, KMS[3][2], BLUE))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 300 + i * 720
        card(d, (x0, 270, x0 + 600, 590), a, col)
        text(d, (x0 + 300, 330), f"{km} km zur Arbeit", 38, MUTED, a, "mm", "SemiBold")
        p = prog(t, st + 0.2, 1.2, ease_in_out)
        text(d, (x0 + 300, 440), "≈ " + eur(r * p), 90, col, a, "mm", "Black")
        text(d, (x0 + 300, 530), "zurück pro Jahr", 30, FG, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 680, 1560, 790), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 735), "Bei 3.000 € brutto – und ab wann es sich überhaupt lohnt", 40, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6), SRC + " · 220 Arbeitstage angenommen")


def draw_pausch(img, d, t, S):
    title(d, t, "Die erste Hürde: 1.230 €", S.c(0), "Arbeitnehmer-Pauschbetrag – wird automatisch berücksichtigt")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (250, 270, 1670, 520), a, AMBER)
        text(d, (290, 340), "Jeder Arbeitnehmer bekommt pauschal", 38, FG, a, "lm", "SemiBold")
        text(d, (290, 440), "1.230 € Werbungskosten", 72, AMBER, a, "lm", "Black")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        card(d, (250, 580, 1670, 840), a, GREEN)
        text(d, (290, 650), "Geld zurück gibt es erst für den Teil darüber –", 38, FG, a, "lm", "SemiBold")
        text(d, (290, 750), "und zwar etwa in Höhe deines Steuersatzes", 54, GREEN, a, "lm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "§ 9a EStG · Ersparnis = zusätzliche Werbungskosten × persönlicher Grenzsteuersatz")


def draw_pendler(img, d, t, S):
    title(d, t, "Pendeln: 38 Cent ab dem ersten Kilometer", S.c(0), "Werbungskosten = Entfernung × 0,38 € × Arbeitstage")
    a0 = prog(t, S.c(1), 0.5)
    for x, h, anc in ((290, "Strecke", "lm"), (560, "Werbungskosten", "mm"), (890, "über 1.230 €", "mm"),
                      (1220, "zurück", "mm")):
        text(d, (x, 290), h, 28, MUTED, a0, anc, "SemiBold")
    for i, (km, wk, r, extra) in enumerate(KMS):
        a = prog(t, S.c(1) + 0.5 + i * 0.6 if i < 2 else S.c(2) + (i - 2) * 0.6, 0.5)
        if a <= 0:
            continue
        y = 320 + i * 120
        card(d, (250, y, 1670, y + 100), a, GREEN if r else GRAY)
        text(d, (290, y + 50), f"{km} km", 40, FG, a, "lm", "Black")
        text(d, (560, y + 50), eur(wk), 38, FG, a, "mm", "Bold")
        text(d, (890, y + 50), eur(extra), 38, MUTED, a, "mm", "Bold")
        text(d, (1220, y + 50), eur(r), 44, GREEN if r else GRAY, a, "mm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        text(d, (250, 860), f"Unter knapp 15 km (bei 220 Tagen) bringt die Pendlerpauschale allein nichts.", 36, AMBER, a,
             "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · 3.000 € brutto, StKl. I, ohne Kirchensteuer")


def draw_homeoffice(img, d, t, S):
    title(d, t, "Homeoffice oder Büro?", S.c(0), "Pro Tag zählt nur eins: Homeoffice-Pauschale oder Pendlerpauschale")
    for i, (st, lab, v, sub, col) in enumerate(((S.c(1), "Homeoffice-Tag", "6,00 €", "max. 1.260 € im Jahr (210 Tage)", VIOLET),
                                                (S.c(2), "Bürotag bei 20 km", "7,60 €", "20 km × 0,38 €", BLUE))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 260, x0 + 660, 520), a, col)
        text(d, (x0 + 40, 315), lab, 34, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 410), v, 76, col, a, "lm", "Black")
        text(d, (x0 + 40, 485), sub, 28, FG, a, "lm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        text(d, (250, 600), "Ab knapp 16 km bringt der Bürotag mehr.", 40, AMBER, a, "lm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        card(d, (250, 660, 1670, 880), a, GREEN)
        text(d, (290, 710), "Mix: 3 Tage Büro (20 km), 2 Tage Homeoffice", 36, FG, a, "lm", "Bold")
        text(d, (290, 780), f"132 × 20 × 0,38 € + 88 × 6 € = {eur(MIX_WK, 2)}", 32, MUTED, a, "lm", "Medium")
        text(d, (1630, 790), f"≈ {eur(MIX_REF)} zurück", 52, GREEN, a, "rm", "Black")
    footer(d, prog(t, S.c(1), 0.5))


def draw_weitere(img, d, t, S):
    title(d, t, "Was sonst noch zählen kann", S.c(0), "Beispiele – nur mit Nachweis und nur, wenn es beruflich veranlasst ist")
    items = [(S.c(1), "Arbeitsmittel", "z. B. Laptop, Fachliteratur, Arbeitskleidung", BLUE),
             (S.c(1) + 0.8, "Fortbildung", "Kurse, Prüfungsgebühren, Fahrten dorthin", BLUE),
             (S.c(2), "Bewerbungen & Umzug", "wenn beruflich bedingt", BLUE),
             (S.c(3), "Handwerker zu Hause", "20 % der Arbeitskosten direkt von der Steuer, bis 1.200 € pro Jahr", GREEN)]
    for i, (st, head, line, col) in enumerate(items):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 240 + i * 170
        card(d, (250, y, 1670, y + 145), a, col)
        text(d, (290, y + 52), head, 38, FG, a, "lm", "Bold")
        text(d, (290, y + 105), line, 28, MUTED, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "§ 9 EStG (Werbungskosten) · § 35a Abs. 3 EStG (Handwerkerleistungen)")


def draw_fristen(img, d, t, S):
    title(d, t, "Muss ich – und bis wann?", S.c(0))
    for i, (st, head, v, line, col) in enumerate(((S.c(1), "Freiwillig", "4 Jahre", ("Erklärung für 2026:", "bis Ende 2030"), GREEN),
                                                  (S.c(2), "Pflicht", "31.07.2027", ("z. B. Steuerklasse III/V oder", "Nebeneinkünfte · ohne Steuerberater"), RED))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 250, x0 + 660, 620), a, col)
        text(d, (x0 + 40, 310), head, 36, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 420), v, 80, col, a, "lm", "Black")
        text(d, (x0 + 40, 520), line[0], 28, FG, a, "lm", "Medium")
        text(d, (x0 + 40, 560), line[1], 28, FG, a, "lm", "Medium")
    a = prog(t, S.c(3), 0.5)
    text(d, (250, 720), "Wer nicht muss, riskiert bei einer freiwilligen Erklärung in der Regel nichts –", 34, FG, a, "lm", "SemiBold")
    text(d, (250, 775), "aber eine Nachzahlung ist möglich, z. B. bei Nebeneinkünften.", 34, MUTED, a, "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5), "§ 46 EStG, § 149 AO · Fristen für Erklärungen ohne Steuerberatung")


def draw_grenzen(img, d, t, S):
    title(d, t, "3 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Vereinfachte Rechnung", "Wir vergleichen die Einkommensteuer 2026 mit und ohne zusätzliche Werbungskosten."),
             (S.c(2), "2", "Dein Steuersatz zählt", "Mit höherem Einkommen kommt bei gleichen Kosten mehr zurück."),
             (S.c(3), "3", "Belege", "Das Finanzamt kann Nachweise verlangen – Fahrten, Homeoffice-Tage, Rechnungen.")]
    for i, (start, n, head, line) in enumerate(items):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 240 + i * 210
        card(d, (250, y, 1670, y + 180), a)
        dot(d, (320, y + 90), 38, fade(AMBER, a))
        text(d, (320, y + 92), n, 40, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + 55), head, 40, FG, a, "lm", "Bold")
        text(d, (400, y + 115), line, 28, MUTED, a, "lm", "Medium")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Steuerberatung – sondern offizielle Werte, nachgerechnet.", t, S.c(0), 50, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), "Werte, Annahmen & Quellen stehen in der Beschreibung.", t, S.c(1), 32, MUTED, "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (360, 470, 900, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (630, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (630, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (630, 665), "echte Zahlen statt Versprechen", 26, MUTED, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1020, 450, 1600, 780), a, AMBER)
        text(d, (1060, 510), "NÄCHSTES VIDEO", 24, AMBER, a, "lm", "Bold")
        text(d, (1060, 580), "Kindergeld oder", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Kinderfreibetrag?", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "Ab wann sich was lohnt", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Die Steuererklärung für zweitausendsechsundzwanzig. Lohnt sie sich für dich?",
            "Wer bei dreitausend Euro brutto zwanzig Kilometer zur Arbeit fährt, bekommt rund hundertzwanzig Euro zurück.",
            "Bei vierzig Kilometern sind es rund fünfhundertsiebzig Euro.",
            "Wir rechnen nach, wie diese Beträge entstehen und ab wann sich die Erklärung überhaupt lohnt.",
        ], draw_hook),
        Scene("pausch", [
            "Zuerst die wichtigste Hürde.",
            "Jeder Arbeitnehmer bekommt automatisch tausendzweihundertdreißig Euro Werbungskosten angerechnet, auch ohne Steuererklärung.",
            "Geld zurück gibt es erst für den Teil, der darüber liegt. Und zwar ungefähr in Höhe deines persönlichen Steuersatzes.",
        ], draw_pausch),
        Scene("pendler", [
            "Der größte Posten für die meisten: der Weg zur Arbeit.",
            "Seit zweitausendsechsundzwanzig gibt es achtunddreißig Cent für jeden Kilometer der einfachen Strecke, ab dem ersten Kilometer. Bei zweihundertzwanzig Arbeitstagen und zehn Kilometern sind das achthundertsechsunddreißig Euro, also weniger als die Pauschale.",
            "Bei zwanzig Kilometern sind es tausendsechshundertzweiundsiebzig Euro, vierhundertzweiundvierzig über der Pauschale. Das bringt rund hundertzwanzig Euro. Bei dreißig Kilometern rund dreihundertsechsundvierzig, bei vierzig rund fünfhundertsiebzig Euro.",
            "Bei zweihundertzwanzig Arbeitstagen lohnt sich die Pendlerpauschale allein also erst ab knapp fünfzehn Kilometern.",
        ], draw_pendler),
        Scene("homeoffice", [
            "Und das Homeoffice?",
            "Für jeden Homeoffice-Tag gibt es sechs Euro, höchstens tausendzweihundertsechzig Euro im Jahr.",
            "Ein Bürotag bei zwanzig Kilometern bringt dagegen sieben Euro sechzig. Für denselben Tag gibt es nur eins von beidem.",
            "Ab knapp sechzehn Kilometern zählt der Bürotag also mehr als der Homeoffice-Tag.",
            "Ein Mix aus drei Tagen Büro und zwei Tagen Homeoffice ergibt bei zwanzig Kilometern tausendfünfhunderteinunddreißig Euro zwanzig, und damit rund zweiundachtzig Euro zurück.",
        ], draw_homeoffice),
        Scene("weitere", [
            "Was kann sonst noch zählen?",
            "Arbeitsmittel wie ein Laptop oder Fachliteratur und Kosten für Fortbildungen.",
            "Auch Bewerbungen oder ein beruflich bedingter Umzug.",
            "Und Handwerker zu Hause: Zwanzig Prozent der Arbeitskosten werden direkt von der Steuer abgezogen, bis zwölfhundert Euro im Jahr.",
        ], draw_weitere),
        Scene("fristen", [
            "Musst du überhaupt eine Steuererklärung machen, und bis wann?",
            "Wer nicht muss, hat vier Jahre Zeit. Die Erklärung für zweitausendsechsundzwanzig geht also bis Ende zweitausenddreißig.",
            "Wer muss, zum Beispiel mit Steuerklasse drei oder fünf oder mit Nebeneinkünften, hat ohne Steuerberater bis zum einunddreißigsten Juli zweitausendsiebenundzwanzig Zeit.",
            "Eine freiwillige Erklärung kann aber auch zu einer Nachzahlung führen, zum Beispiel bei Nebeneinkünften.",
        ], draw_fristen),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Wir rechnen vereinfacht mit der Einkommensteuer zweitausendsechsundzwanzig mit und ohne zusätzliche Werbungskosten.",
            "Zweitens: Dein Steuersatz entscheidet. Mit höherem Einkommen kommt bei gleichen Kosten mehr zurück.",
            "Drittens: Das Finanzamt kann Belege verlangen, also Fahrten, Homeoffice-Tage und Rechnungen.",
        ], draw_grenzen),
        Scene("outro", [
            "Das hier ist keine Steuerberatung, sondern Rechnen mit offiziellen Werten.",
            "Alle Werte, Annahmen und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video: Kindergeld oder Kinderfreibetrag. Ab wann sich was lohnt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
