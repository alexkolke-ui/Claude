"""Video 007: Weihnachtsgeld – was netto bleibt (BMF-Programmablaufplan 2026, Differenzmethode)."""
from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, card, dot, ease_in_out, eur, fade,
                     lerp, prog, rrect, text, text_pop)
from lib.lohn2026 import lohnsteuer_jahr, netto_monat, sonderzahlung

B = 3500
Z = sonderzahlung(B, B)
M = netto_monat(B)
SV_Z = Z["RV"] + Z["AV"] + Z["KV"] + Z["PV"]
L0 = int(lohnsteuer_jahr(B * 12)[0])
L1 = int(lohnsteuer_jahr(B * 13)[0])
CASES = [(b, sonderzahlung(b, b), netto_monat(b)) for b in (2500, 3500, 5000, 7000)]
Q = lambda x, b: x / b * 100

# Every number spoken in the narration is checked here.
assert Z["Netto"] == 1915.75 and round(Q(Z["Netto"], B), 1) == 54.7          # "1.915,75", "knapp 55 %"
assert M["Netto"] == 2333.25 and round(Q(M["Netto"], B), 1) == 66.7          # "zwei Drittel"
assert Z["LSt"] == 823 and Z["Soli"] == 0 and L1 - L0 == 823                  # "823 €"
assert L0 == 4866 and L1 == 5689                                             # Jahressteuer ohne / mit
assert 23.5 < 823 / B * 100 < 23.6                                           # "gut 23 %"
assert 11.5 < M["LSt"] / B * 100 < 11.7                                    # "knapp zwölf"
assert SV_Z == 761.25                                                         # "761,25"
assert [round(z["Netto"]) for _, z, _ in CASES] == [1437, 1916, 2530, 3603]
assert [round(Q(z["Netto"], b), 1) for b, z, _ in CASES] == [57.5, 54.7, 50.6, 51.5]
assert CASES[3][1]["KV"] == 0 and CASES[3][1]["PV"] == 0                      # 7.000 €: über der KV-Grenze

SRC = "Berechnung nach BMF-Programmablaufplan Lohnsteuer 2026 · StKl. I, kinderlos, ohne Kirchensteuer, KV-Zusatz Ø 2,9 %"


def pct(v, dec=1):
    return f"{v:.{dec}f}".replace(".", ",") + " %"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 170), "3.500 € Weihnachtsgeld", t, S.c(0), 60, FG, "mm", "Black")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (300, 270, 900, 590), a, GREEN)
        text(d, (600, 330), "davon netto", 36, MUTED, a, "mm", "SemiBold")
        p = prog(t, S.c(1) + 0.2, 1.4, ease_in_out)
        text(d, (600, 440), eur(lerp(B, Z["Netto"], p), 2), 84, GREEN, a, "mm", "Black")
        text(d, (600, 530), pct(Q(Z["Netto"], B)), 40, FG, a, "mm", "Bold")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        card(d, (1020, 270, 1620, 590), a, BLUE)
        text(d, (1320, 330), "normales Monatsgehalt", 36, MUTED, a, "mm", "SemiBold")
        text(d, (1320, 440), eur(M["Netto"], 2), 84, BLUE, a, "mm", "Black")
        text(d, (1320, 530), pct(Q(M["Netto"], B)), 40, FG, a, "mm", "Bold")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 680, 1560, 800), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 740), "Gleiches Brutto – rund 418 € weniger netto. Warum?", 44, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6))


def draw_methode(img, d, t, S):
    title(d, t, "Wie Weihnachtsgeld versteuert wird", S.c(0), "Jahreslohn-Methode: Steuer mit minus Steuer ohne Sonderzahlung")
    rows = [(S.c(1), "Jahreslohnsteuer ohne Weihnachtsgeld", f"12 × {eur(B)}", eur(L0), FG),
            (S.c(2), "Jahreslohnsteuer mit Weihnachtsgeld", f"13 × {eur(B)}", eur(L1), FG),
            (S.c(3), "Steuer auf das Weihnachtsgeld", "Differenz", eur(L1 - L0), RED)]
    for i, (st, lab, sub, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 160
        card(d, (250, y, 1670, y + 135), a, col if i == 2 else None)
        text(d, (290, y + 50), lab, 38, FG, a, "lm", "Bold")
        text(d, (290, y + 100), sub, 28, MUTED, a, "lm", "Medium")
        text(d, (1630, y + 68), v, 56, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        text(d, (250, 820), f"= {pct(823 / B * 100)} des Weihnachtsgelds – mehr als die {pct(M['LSt'] / B * 100)} beim Monatsgehalt",
             36, AMBER, a, "lm", "Bold")
        text(d, (250, 880), "Der ganze Betrag wird mit dem höchsten Satz deines Einkommens besteuert.", 30, FG, a,
             "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5))


def draw_abzuege(img, d, t, S):
    title(d, t, "Alle Abzüge auf 3.500 € Weihnachtsgeld", S.c(0), "Sozialversicherung fällt voll an – bis zur Beitragsgrenze")
    parts = [("Lohnsteuer", Z["LSt"], RED, S.c(1)), ("Rentenversicherung", Z["RV"], VIOLET, S.c(2)),
             ("Arbeitslosenversicherung", Z["AV"], GRAY, S.c(2) + 0.4), ("Krankenversicherung", Z["KV"], BLUE, S.c(2) + 0.8),
             ("Pflegeversicherung", Z["PV"], (125, 211, 252), S.c(2) + 1.2)]
    for i, (lab, v, col, st) in enumerate(parts):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 270 + i * 90
        dot(d, (270, y), 12, fade(col, a))
        text(d, (300, y), lab, 36, FG, a, "lm", "SemiBold")
        text(d, (1050, y), "−" + eur(v, 2), 42, col, a, "rm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        d.line((270, 720, 1050, 720), fill=fade((70, 82, 108), a), width=2)
        text(d, (300, 775), "netto", 40, FG, a, "lm", "Bold")
        text(d, (1050, 775), eur(Z["Netto"], 2), 54, GREEN, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        card(d, (1180, 300, 1860, 620), a, AMBER)
        text(d, (1220, 360), "Sozialversicherung", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1220, 440), eur(SV_Z, 2), 64, BLUE, a, "lm", "Black")
        text(d, (1220, 510), "21,75 % – wie beim Gehalt", 30, FG, a, "lm", "SemiBold")
        text(d, (1220, 565), "Steuer: 823 € (23,5 %)", 30, RED, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5))


def draw_vergleich(img, d, t, S):
    title(d, t, "Ein volles Monatsgehalt als Weihnachtsgeld", S.c(0), "Wie viel Prozent bleiben – Weihnachtsgeld vs. Monatsgehalt")
    for i, (b, z, m) in enumerate(CASES):
        st = S.c(1) + i * 0.7 if i < 3 else S.c(3)
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        x0 = 250 + i * 360
        card(d, (x0, 260, x0 + 330, 760), a, AMBER if i == 3 else GREEN)
        cx = x0 + 165
        text(d, (cx, 320), eur(b), 46, FG, a, "mm", "Black")
        text(d, (cx, 400), "Weihnachtsgeld netto", 24, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 455), eur(z["Netto"]), 46, GREEN, a, "mm", "Black")
        text(d, (cx, 505), pct(Q(z["Netto"], b)), 34, GREEN, a, "mm", "Bold")
        d.line((x0 + 40, 555, x0 + 290, 555), fill=fade((70, 82, 108), a), width=2)
        text(d, (cx, 600), "Monatsgehalt netto", 24, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 655), pct(Q(m["Netto"], b)), 34, BLUE, a, "mm", "Bold")
        if i == 3:
            text(d, (cx, 720), "keine KV/PV-Beiträge", 22, AMBER, a, "mm", "Bold")
    a = prog(t, S.c(4), 0.5)
    text(d, (W / 2, 860), "Vom Weihnachtsgeld bleibt immer weniger als vom Gehalt.", 44, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5))


def draw_mythos(img, d, t, S):
    a0 = prog(t, S.c(0), 0.5)
    if a0 > 0:
        rrect(d, (660, 140, 1260, 210), 35, fill=fade((50, 26, 30), a0), outline=fade(RED, a0 * 0.7), width=2)
        text(d, (W / 2, 176), "MYTHOS", 34, RED, a0, "mm", "Black")
    text_pop(d, (W / 2, 290), "„Weihnachtsgeld wird mit Steuerklasse 6 versteuert.“", t, S.c(0) + 0.3, 50, FG, "mm", "Black")
    a1 = prog(t, S.c(1), 0.5)
    if a1 > 0:
        rrect(d, (660, 380, 1260, 450), 35, fill=fade((24, 48, 40), a1), outline=fade(GREEN, a1 * 0.7), width=2)
        text(d, (W / 2, 416), "RECHNUNG", 34, GREEN, a1, "mm", "Black")
    a2 = prog(t, S.c(2), 0.5)
    if a2 > 0:
        card(d, (300, 510, 1620, 760), a2)
        text(d, (340, 575), "Steuerklasse 6 gilt für einen zweiten Job.", 40, FG, a2, "lm", "Bold")
        text(d, (340, 650), "Weihnachtsgeld läuft über deine eigene Steuerklasse –", 34, MUTED, a2, "lm", "SemiBold")
        text(d, (340, 705), "nur eben mit dem Satz für den obersten Euro.", 34, MUTED, a2, "lm", "SemiBold")
    a3 = prog(t, S.c(3), 0.5)
    text(d, (W / 2, 850), "Und: Die Lohnsteuer ist nur eine Vorauszahlung.", 40, AMBER, a3, "mm", "Bold")


def draw_grenzen(img, d, t, S):
    title(d, t, "3 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Vereinfachte Rechnung",
              "Jahreslohn mit minus ohne Weihnachtsgeld – die Abrechnung kann leicht abweichen."),
             (S.c(2), "2", "Persönliche Lage", "Kirchensteuer, Kinder, Krankenkasse und Steuerklasse ändern das Ergebnis."),
             (S.c(3), "3", "Jahresausgleich", "Über die Steuererklärung wird am Ende die tatsächliche Jahressteuer fällig.")]
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
    text_pop(d, (W / 2, 220), "Frohe Weihnachten!", t, S.c(0), 64, AMBER, "mm", "Black")
    text_pop(d, (W / 2, 310), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(1), 40, FG, "mm", "Bold")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (360, 470, 900, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (630, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (630, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (630, 665), "echte Zahlen statt Versprechen", 26, MUTED, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1020, 450, 1600, 780), a, AMBER)
        text(d, (1060, 510), "NÄCHSTES VIDEO · 31.12.", 24, AMBER, a, "lm", "Bold")
        text(d, (1060, 580), "2026 in Zahlen:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "der Jahresrückblick", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "Inflation, Zinsen, Immobilien", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Dreitausendfünfhundert Euro Weihnachtsgeld, ein volles Monatsgehalt.",
            "Netto bleiben davon tausendneunhundertfünfzehn Euro fünfundsiebzig. Knapp fünfundfünfzig Prozent.",
            "Vom normalen Monatsgehalt in gleicher Höhe bleiben dagegen zweitausenddreihundertdreiunddreißig Euro, also zwei Drittel.",
            "Gleiches Brutto, aber über vierhundert Euro weniger netto. Woran liegt das?",
        ], draw_hook),
        Scene("methode", [
            "Weihnachtsgeld ist für das Finanzamt ein sonstiger Bezug. Die Steuer darauf wird über das ganze Jahr gerechnet.",
            "Zuerst die Lohnsteuer für das Jahr ohne Weihnachtsgeld: Bei zwölf Monatsgehältern sind das viertausendachthundertsechsundsechzig Euro.",
            "Dann mit Weihnachtsgeld, also dreizehn Gehältern: fünftausendsechshundertneunundachtzig Euro.",
            "Die Differenz, achthundertdreiundzwanzig Euro, ist die Steuer auf das Weihnachtsgeld.",
            "Das sind gut dreiundzwanzig Prozent. Beim normalen Gehalt sind es knapp zwölf. Denn das ganze Weihnachtsgeld wird mit dem Steuersatz deines obersten Euros besteuert.",
        ], draw_methode),
        Scene("abzuege", [
            "Und es bleibt nicht bei der Steuer.",
            "Achthundertdreiundzwanzig Euro Lohnsteuer.",
            "Dazu kommt die Sozialversicherung: Rente, Arbeitslosigkeit, Krankheit und Pflege, genau wie beim Gehalt.",
            "Übrig bleiben tausendneunhundertfünfzehn Euro fünfundsiebzig.",
            "Die Sozialversicherung macht hier mit siebenhunderteinundsechzig Euro fünfundzwanzig fast so viel aus wie die Steuer.",
        ], draw_abzuege),
        Scene("vergleich", [
            "Wie sieht das bei anderen Gehältern aus? Wir nehmen immer ein volles Monatsgehalt als Weihnachtsgeld.",
            "Bei zweitausendfünfhundert Euro bleiben siebenundfünfzig Komma fünf Prozent, bei dreitausendfünfhundert vierundfünfzig Komma sieben, bei fünftausend fünfzig Komma sechs Prozent.",
            "Je höher das Gehalt, desto höher der Steuersatz auf den obersten Euro.",
            "Bei siebentausend Euro sind es wieder etwas mehr, einundfünfzig Komma fünf Prozent. Weil das Gehalt hier schon über der Grenze für Kranken- und Pflegeversicherung liegt, fallen darauf keine Beiträge mehr an.",
            "Aber in jedem Fall bleibt vom Weihnachtsgeld weniger als vom normalen Gehalt.",
        ], draw_vergleich),
        Scene("mythos", [
            "Ein verbreiteter Mythos: Weihnachtsgeld wird mit Steuerklasse sechs versteuert.",
            "Das stimmt nicht.",
            "Steuerklasse sechs gilt für einen zweiten Job. Weihnachtsgeld läuft über deine eigene Steuerklasse, nur eben mit dem Steuersatz für den obersten Euro.",
            "Und die Lohnsteuer ist nur eine Vorauszahlung. Mit der Steuererklärung wird am Ende abgerechnet.",
        ], draw_mythos),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Wir rechnen vereinfacht mit dem Jahreslohn mit und ohne Weihnachtsgeld. Die echte Lohnabrechnung kann um ein paar Euro abweichen.",
            "Zweitens: Kirchensteuer, Kinder, die Krankenkasse und die Steuerklasse ändern das Ergebnis.",
            "Drittens: Über die Steuererklärung wird am Ende die tatsächliche Jahressteuer festgesetzt. Zu viel gezahlte Lohnsteuer kommt dann zurück.",
        ], draw_grenzen),
        Scene("outro", [
            "Frohe Weihnachten!",
            "Wie immer: keine Beratung, sondern Rechnen mit offiziellen Zahlen. Alle Werte stehen in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Am einunddreißigsten Dezember blicken wir zurück: zweitausendsechsundzwanzig in Zahlen. Inflation, Zinsen und Immobilienpreise.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
