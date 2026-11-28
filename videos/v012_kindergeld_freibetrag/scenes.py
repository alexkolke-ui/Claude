"""Video 012: Kindergeld oder Kinderfreibetrag? Die Günstigerprüfung 2026 nachgerechnet."""
import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card, dot, ease_in_out, eur, fade,
                     lerp, prog, rrect, text, text_pop)
from lib.lohn2026 import uptab26

KG_MONAT = 259
KG_JAHR = KG_MONAT * 12
KFB = 9756            # Kinderfreibetrag 6.828 € + BEA-Freibetrag 2.928 € (Eltern zusammen), 2026


def est_split(zve):
    """Einkommensteuer 2026 bei Zusammenveranlagung (Splittingtarif), ohne Soli/Kirchensteuer."""
    return 2 * int(uptab26(int(zve / 2)))


def ersparnis(zve):
    return est_split(zve) - est_split(zve - KFB)


EX = [(z, ersparnis(z)) for z in (60000, 100000, 150000)]
BREAK = next(z for z in range(40000, 200000, 100) if ersparnis(z) > KG_JAHR)
XS = np.arange(30000, 200001, 1000)
YS = np.array([ersparnis(z) for z in XS])
SUMME_18 = 18 * KG_JAHR

# Every number spoken in the narration is checked here.
assert KG_JAHR == 3108 and KFB == 6828 + 2928
assert EX == [(60000, 2668), (100000, 3344), (150000, 4098)]
assert 3344 - KG_JAHR == 236 and 4098 - KG_JAHR == 990
assert BREAK == 86100                                                     # "rund 86.000 €"
assert SUMME_18 == 55944
assert round(KFB * 0.42) == 4098

SRC = "Kindergeld 2026: 259 €/Monat · Kinder- und BEA-Freibetrag 2026: 9.756 € je Kind (Eltern zusammen) · Tarif 2026"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 160), "Kindergeld oder Kinderfreibetrag?", t, S.c(0), 60, FG, "mm", "Black")
    for i, (st, lab, v, sub, col) in enumerate(((S.c(1), "Kindergeld", "3.108 €", "259 € × 12 Monate", GREEN),
                                                (S.c(2), "Kinderfreibeträge", "9.756 €", "weniger zu versteuern", BLUE))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 300 + i * 720
        card(d, (x0, 270, x0 + 600, 590), a, col)
        text(d, (x0 + 300, 330), lab, 38, MUTED, a, "mm", "SemiBold")
        text(d, (x0 + 300, 440), v, 90, col, a, "mm", "Black")
        text(d, (x0 + 300, 530), sub, 30, FG, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 680, 1560, 790), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 735), "Du bekommst nur eins davon – das Finanzamt rechnet für dich", 34, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6))


def draw_pruefung(img, d, t, S):
    title(d, t, "Die Günstigerprüfung", S.c(0), "läuft automatisch mit der Steuererklärung")
    rows = [(S.c(1), "1. Kindergeld kommt jeden Monat", "von der Familienkasse, 259 € je Kind", GREEN),
            (S.c(2), "2. Das Finanzamt rechnet nach", "Was spart der Freibetrag an Einkommensteuer?", BLUE),
            (S.c(3), "3. Ist die Ersparnis höher als das Kindergeld,", "bekommst du die Differenz über die Steuer zurück", AMBER)]
    for i, (st, head, line, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 200
        card(d, (250, y, 1670, y + 170), a, col)
        text(d, (290, y + 65), head, 40, FG, a, "lm", "Bold")
        text(d, (290, y + 125), line, 30, MUTED, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "§ 31 EStG · Beispiel: Eltern zusammen veranlagt, ein Kind")


def draw_beispiele(img, d, t, S):
    title(d, t, "Drei Beispiele: Eltern, ein Kind", S.c(0), "Zu versteuerndes Einkommen beider Eltern zusammen")
    cols = [GREEN, BLUE, VIOLET]
    for i, ((zve, sp), col) in enumerate(zip(EX, cols)):
        a = prog(t, S.c(1 + i), 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 480
        card(d, (x0, 270, x0 + 440, 780), a, col)
        cx = x0 + 220
        text(d, (cx, 330), eur(zve), 50, FG, a, "mm", "Black")
        text(d, (cx, 420), "Steuerersparnis", 28, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 475), eur(sp), 50, col, a, "mm", "Black")
        text(d, (cx, 560), "vs. Kindergeld", 28, MUTED, a, "mm", "SemiBold")
        text(d, (cx, 615), eur(KG_JAHR), 44, FG, a, "mm", "Black")
        win = "Kindergeld" if sp <= KG_JAHR else f"Freibetrag +{eur(sp - KG_JAHR)}"
        text(d, (cx, 720), win, 34, GREEN if sp <= KG_JAHR else AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · ohne Soli/Kirchensteuer")


def draw_schwelle(img, d, t, S):
    title(d, t, "Ab wann lohnt sich der Freibetrag?", S.c(0), "Steuerersparnis durch 9.756 € Freibetrag vs. 3.108 € Kindergeld")
    ch = Chart((260, 270, 1300, 860), (30000, 200000), (0, 4500))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(40000, 200001, 40000), range(0, 4501, 1000), lambda v: f"{v // 1000}.000 €",
            lambda v: f"{v // 1000}.000 €" if v else "0 €", "zu versteuerndes Einkommen (Eltern)")
    if ax > 0:
        _, py = ch.px(0, KG_JAHR)
        x = ch.x0
        while x < ch.x1:
            d.line((x, py, min(x + 14, ch.x1), py), fill=fade(GREEN, ax), width=3)
            x += 26
        text(d, (ch.x0 + 10, py - 10), "Kindergeld 3.108 €", 26, GREEN, ax, "lb", "Bold")
    up = 30000 + 170000 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 30000:
        ch.line(d, XS, YS, BLUE, 6, up)
    a = prog(t, S.c(2), 0.5) if up >= BREAK else 0
    if a > 0:
        p = ch.px(BREAK, ersparnis(BREAK))
        dot(d, p, 11, AMBER)
        text(d, (p[0] + 16, p[1] + 16), "≈ 86.100 €", 32, AMBER, a, "lt", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1380, 300, 1870, 640), a, AMBER)
        text(d, (1410, 355), "Darunter:", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1410, 420), "Kindergeld besser", 36, GREEN, a, "lm", "Black")
        text(d, (1410, 510), "Darüber:", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1410, 575), "Freibetrag besser", 36, AMBER, a, "lm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (1380, 720), "Beim Spitzensteuersatz", 30, FG, a, "lm", "SemiBold")
    text(d, (1380, 765), "(42 %): max. ≈ 4.098 €", 30, FG, a, "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · ohne Soli/Kirchensteuer")


def draw_summe(img, d, t, S):
    title(d, t, "Was Kindergeld über 18 Jahre ausmacht", S.c(0), "Beim heutigen Satz von 259 € im Monat")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (460, 280, 1460, 640), a, GREEN)
        text(d, (W / 2, 350), "18 Jahre × 3.108 €", 40, MUTED, a, "mm", "SemiBold")
        p = prog(t, S.c(1) + 0.2, 1.4, ease_in_out)
        text(d, (W / 2, 480), eur(SUMME_18 * p), 110, GREEN, a, "mm", "Black")
        text(d, (W / 2, 590), "je Kind – länger bei Ausbildung oder Studium", 30, FG, a, "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    text(d, (W / 2, 740), "Kindergeld wird in der Regel bis 18 gezahlt, in Ausbildung bis höchstens 25.", 34, MUTED, a, "mm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5), "Kindergeld 2026: 259 € je Kind und Monat · künftige Erhöhungen nicht eingerechnet")


def draw_grenzen(img, d, t, S):
    title(d, t, "4 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Zu versteuerndes Einkommen ≠ Brutto", "Es ist das Einkommen nach Abzügen wie Werbungskosten und Vorsorge."),
             (S.c(2), "2", "Ohne Soli & Kirchensteuer", "Für diese beiden zählt der Freibetrag immer – auch wenn Kindergeld besser ist."),
             (S.c(3), "3", "Jedes Kind einzeln", "Die Prüfung läuft pro Kind; bei mehreren Kindern verschiebt sich die Schwelle."),
             (S.c(4), "4", "Andere Familienformen", "Getrennte oder Alleinerziehende teilen die Freibeträge anders auf.")]
    for i, (start, n, head, line) in enumerate(items):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 220 + i * 175
        card(d, (250, y, 1670, y + 155), a)
        dot(d, (320, y + 78), 36, fade(AMBER, a))
        text(d, (320, y + 80), n, 38, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + 50), head, 38, FG, a, "lm", "Bold")
        text(d, (400, y + 105), line, 28, MUTED, a, "lm", "Medium")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Steuerberatung – sondern offizielle Werte, nachgerechnet.", t, S.c(0), 50, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), "Werte, Formeln & Quellen stehen in der Beschreibung.", t, S.c(1), 32, MUTED, "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    if a > 0:
        rrect(d, (690, 470, 1230, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (960, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (960, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (960, 665), "jeden Donnerstag ein neues Video", 26, MUTED, a, "mm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Kindergeld oder Kinderfreibetrag? Viele Eltern wissen nicht, was davon sie eigentlich bekommen.",
            "Das Kindergeld beträgt zweitausendsechsundzwanzig zweihundertneunundfünfzig Euro im Monat, also dreitausendeinhundertacht Euro im Jahr.",
            "Die Kinderfreibeträge zusammen betragen neuntausendsiebenhundertsechsundfünfzig Euro je Kind. So viel Einkommen bleibt steuerfrei.",
            "Du bekommst aber nur eins von beidem. Wir rechnen nach, ab wann sich was lohnt.",
        ], draw_hook),
        Scene("pruefung", [
            "Das Ganze heißt Günstigerprüfung und läuft automatisch mit der Steuererklärung.",
            "Erstens: Das Kindergeld bekommst du jeden Monat von der Familienkasse.",
            "Zweitens: Das Finanzamt rechnet nach, wie viel Einkommensteuer der Freibetrag sparen würde.",
            "Drittens: Ist die Ersparnis höher als das Kindergeld, bekommst du die Differenz über die Steuer zurück.",
        ], draw_pruefung),
        Scene("beispiele", [
            "Drei Beispiele für Eltern mit einem Kind, die zusammen veranlagt werden.",
            "Bei sechzigtausend Euro zu versteuerndem Einkommen spart der Freibetrag zweitausendsechshundertachtundsechzig Euro Steuer. Weniger als das Kindergeld, also bleibt es beim Kindergeld.",
            "Bei hunderttausend Euro spart er dreitausenddreihundertvierundvierzig Euro, zweihundertsechsunddreißig Euro mehr als das Kindergeld.",
            "Bei hundertfünfzigtausend Euro sind es viertausendachtundneunzig Euro, neunhundertneunzig Euro mehr.",
        ], draw_beispiele),
        Scene("schwelle", [
            "Wo genau liegt die Grenze?",
            "Je höher das Einkommen, desto mehr spart der Freibetrag, weil der Steuersatz steigt.",
            "Für Eltern mit einem Kind ist der Freibetrag ab rund sechsundachtzigtausend Euro zu versteuerndem Einkommen günstiger.",
            "Darunter bleibt es beim Kindergeld, darüber kommt die Differenz über die Steuer.",
            "Beim Spitzensteuersatz von zweiundvierzig Prozent sind es höchstens rund viertausendachtundneunzig Euro.",
        ], draw_schwelle),
        Scene("summe", [
            "Und was macht das Kindergeld über die Jahre aus?",
            "Bis zum achtzehnten Geburtstag sind das beim heutigen Satz fünfundfünfzigtausendneunhundertvierundvierzig Euro je Kind.",
            "Wer danach eine Ausbildung oder ein Studium macht, bekommt es unter Umständen bis fünfundzwanzig.",
        ], draw_summe),
        Scene("grenzen", [
            "Vier ehrliche Einschränkungen.",
            "Erstens: Das zu versteuernde Einkommen ist nicht das Brutto, sondern das Einkommen nach Abzügen wie Werbungskosten und Vorsorge.",
            "Zweitens: Solidaritätszuschlag und Kirchensteuer haben wir weggelassen. Für die beiden wird der Freibetrag immer berücksichtigt.",
            "Drittens: Die Prüfung läuft für jedes Kind einzeln. Bei mehreren Kindern verschiebt sich die Grenze.",
            "Viertens: Bei getrennten Eltern oder Alleinerziehenden werden die Freibeträge anders aufgeteilt.",
        ], draw_grenzen),
        Scene("outro", [
            "Das hier ist keine Steuerberatung, sondern Rechnen mit offiziellen Werten.",
            "Alle Werte, Formeln und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal. Jeden Donnerstag kommt ein neues Video.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
