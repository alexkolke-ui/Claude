"""Video 009: Das neue Altersvorsorgedepot ab 2027 – so viel legt der Staat drauf.

Regeln laut BMF-FAQ „Reform der geförderten privaten Altersvorsorge“ (abgerufen 26.11.2026),
Steuerwerte mit dem Tarif 2026 als Näherung (Tarif 2027 noch nicht bekannt).
"""
import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card, dot, ease_in_out, eur,
                     fade, lerp, prog, rrect, text, text_pop)
from lib.lohn2026 import uptab26

# ---------------------------------------------------------------- Regeln (BMF-FAQ)
MIN_EIGEN, STUFE1, MAX_FOERDER, MAX_EINZAHLUNG = 120, 360, 1800, 6840
KIND_MAX, BONUS_U25, KOSTEN_STD = 300, 200, 1.0
WECHSEL_GEBUEHR, WECHSEL_FREI_JAHRE = 150, 5


def grundzulage(e):
    """Grundzulage pro Jahr für einen Eigenbeitrag e (Euro/Jahr)."""
    if e < MIN_EIGEN:
        return 0.0
    return 0.5 * min(e, STUFE1) + 0.25 * max(0.0, min(e, MAX_FOERDER) - STUFE1)


def kinderzulage(e, kinder):
    return kinder * min(e, KIND_MAX) if e >= MIN_EIGEN else 0.0


QUOTE = [(m, grundzulage(12 * m), grundzulage(12 * m) / (12 * m) * 100) for m in (10, 30, 50, 100, 150)]
FAM = grundzulage(300) + kinderzulage(300, 2)

# Günstigerprüfung: Sonderausgabenabzug (Eigenbeitrag + Zulage) vs. Zulage, Tarif 2026 als Näherung
SA = MAX_FOERDER + grundzulage(MAX_FOERDER)
ZVE_3000, ZVE_5000 = 27480, 46644            # zu versteuerndes Einkommen bei 3.000 € / 5.000 € brutto (StKl. I, Video 6)
SAVE_3000 = int(uptab26(ZVE_3000)) - int(uptab26(ZVE_3000 - SA))
SAVE_5000 = int(uptab26(ZVE_5000)) - int(uptab26(ZVE_5000 - SA))

# Modellrechnung 30 Jahre: 150 €/Monat + Zulage, Rendite vor Kosten 5 % p. a. (Annahme, keine Prognose)
YEARS, R_GROSS = 30, 0.05
EIGEN = 12 * 150
ZUL = grundzulage(EIGEN)


def endwert(einzahlung, r, n=YEARS):
    return einzahlung * ((1 + r) ** n - 1) / r


END_1 = endwert(EIGEN + ZUL, R_GROSS - 0.010)        # Effektivkosten 1,0 % (Obergrenze Standarddepot)
END_05 = endwert(EIGEN + ZUL, R_GROSS - 0.005)       # Effektivkosten 0,5 %
END_NOZ = endwert(EIGEN, R_GROSS - 0.010)            # ohne Zulage
PAID, ZUL_SUM = EIGEN * YEARS, ZUL * YEARS
XS = np.arange(0, YEARS + 1)
CURVE_EIGEN = EIGEN * XS
CURVE_ZUL = (EIGEN + ZUL) * XS
CURVE_END = np.array([endwert(EIGEN + ZUL, R_GROSS - 0.010, n) if n else 0 for n in XS])

# Every number spoken in the narration is checked here.
assert grundzulage(1800) == 540 and grundzulage(360) == 180 and grundzulage(120) == 60 and grundzulage(119) == 0
assert [round(q, 1) for _, _, q in QUOTE] == [50.0, 50.0, 40.0, 32.5, 30.0]
assert [z for _, z, _ in QUOTE] == [60, 180, 240, 390, 540]
assert FAM == 750 and kinderzulage(300, 1) == 300 and kinderzulage(600, 1) == 300
assert SA == 2340 and SAVE_3000 == 630 and SAVE_5000 == 785
assert SAVE_3000 - 540 == 90 and SAVE_5000 - 540 == 245                     # "rund 90 €", "rund 245 €"
assert PAID == 54000 and ZUL_SUM == 16200
assert 131000 < END_1 < 131500 and 142500 < END_05 < 143000 and 100500 < END_NOZ < 101500
assert 11000 < END_05 - END_1 < 11800                                          # "gut 11.000 € Unterschied"

SRC = "Regeln: BMF-FAQ zur Reform der geförderten privaten Altersvorsorge (Stand 26.11.2026)"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def pct(v, dec=1):
    return f"{v:.{dec}f}".replace(".", ",") + " %"


def items(d, t, S, rows, y0=240, h=150, gap=20, x1=1670):
    for i, (st, head, line, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = y0 + i * (h + gap)
        card(d, (250, y, x1, y + h), a, col)
        text(d, (290, y + h * 0.36), head, 38, FG, a, "lm", "Bold")
        text(d, (290, y + h * 0.72), line, 28, MUTED, a, "lm", "Medium")


# ---------------------------------------------------------------- scenes
def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 160), "Neu ab 2027: das Altersvorsorgedepot", t, S.c(0), 56, FG, "mm", "Black")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (300, 270, 900, 600), a, BLUE)
        text(d, (600, 330), "du zahlst", 36, MUTED, a, "mm", "SemiBold")
        text(d, (600, 440), "150 € / Monat", 72, BLUE, a, "mm", "Black")
        text(d, (600, 540), "= 1.800 € im Jahr", 32, FG, a, "mm", "Medium")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        card(d, (1020, 270, 1620, 600), a, GREEN)
        text(d, (1320, 330), "der Staat legt drauf", 36, MUTED, a, "mm", "SemiBold")
        p = prog(t, S.c(2) + 0.2, 1.2, ease_in_out)
        text(d, (1320, 440), "+" + eur(540 * p), 84, GREEN, a, "mm", "Black")
        text(d, (1320, 540), "Grundzulage pro Jahr", 32, FG, a, "mm", "Medium")
    a = prog(t, S.c(3), 0.6)
    if a > 0:
        rrect(d, (360, 690, 1560, 800), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 745), "Wie es funktioniert – und für wen es sich rechnet", 42, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6))


def draw_was(img, d, t, S):
    title(d, t, "Was ist das Altersvorsorgedepot?", S.c(0), "Neue geförderte private Altersvorsorge, Start 1. Januar 2027")
    items(d, t, S, [
        (S.c(1), "Depot ohne Garantie", "Fonds und ETFs aus einer gesetzlichen Positivliste – Kurse können auch fallen", BLUE),
        (S.c(2), "Standarddepot", "zwei Fonds, Umschichtung vor der Rente, Effektivkosten höchstens 1,0 % pro Jahr", GREEN),
        (S.c(3), "Garantieprodukte bleiben", "mit 100 % oder 80 % der Einzahlungen garantiert zum Rentenbeginn", VIOLET),
        (S.c(4), "Riester läuft aus", "neue Riester-Verträge gab es nur bis 31.12.2026 – alte laufen weiter", AMBER)])
    footer(d, prog(t, S.c(1), 0.5))


def draw_zulage(img, d, t, S):
    title(d, t, "So hoch ist die Grundzulage", S.c(0), "50 Cent je Euro bis 360 €, dann 25 Cent je Euro bis 1.800 € Eigenbeitrag")
    ch = Chart((260, 270, 1180, 860), (0, 2000), (0, 600))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(0, 2001, 400), range(0, 601, 100), lambda v: f"{v} €", lambda v: f"{v} €",
            "Eigenbeitrag pro Jahr")
    xs = np.arange(0, 2001, 10)
    ys = np.array([grundzulage(x) for x in xs])
    up = 2000 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 0:
        ch.line(d, xs, ys, GREEN, 6, up)
    for st, e in ((S.c(1) + 0.8, 360), (S.c(2) + 0.6, 1800)):
        a = prog(t, st, 0.5) if up >= e else 0
        if a > 0:
            p = ch.px(e, grundzulage(e))
            dot(d, p, 10, GREEN)
            text(d, (p[0] + (14 if e == 360 else -14), p[1] - 16), f"{eur(e)} → {eur(grundzulage(e))}", 28, FG, a,
                 "lb" if e == 360 else "rb", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1260, 270, 1860, 760), a, AMBER)
        text(d, (1290, 320), "Monatsbeitrag → Zulage", 28, MUTED, a, "lm", "SemiBold")
        for i, (m, z, q) in enumerate(QUOTE):
            y = 390 + i * 75
            text(d, (1290, y), f"{m} €", 34, FG, a, "lm", "SemiBold")
            text(d, (1600, y), eur(z), 36, GREEN, a, "rm", "Black")
            text(d, (1830, y), pct(q), 30, AMBER, a, "rm", "Bold")
    a = prog(t, S.c(4), 0.5)
    text(d, (1260, 820), "Mindestens 10 € im Monat (120 € im Jahr)", 30, FG, a, "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5))


def draw_kinder(img, d, t, S):
    title(d, t, "Kinder und junge Leute", S.c(0), "Kinderzulage: 1 € je eingezahltem Euro, bis 300 € pro Kind und Jahr")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (250, 260, 1100, 760), a, GREEN)
        text(d, (290, 320), "Beispiel: 25 € im Monat, zwei Kinder", 36, FG, a, "lm", "Bold")
        rows = [(S.c(1) + 0.5, "Eigenbeitrag", eur(300), FG), (S.c(2), "Grundzulage", "+" + eur(grundzulage(300)), GREEN),
                (S.c(2) + 0.8, "Kinderzulage 2 × 300 €", "+" + eur(kinderzulage(300, 2)), GREEN)]
        for i, (st, lab, v, col) in enumerate(rows):
            b = prog(t, st, 0.5)
            y = 420 + i * 80
            text(d, (290, y), lab, 34, MUTED, b, "lm", "SemiBold")
            text(d, (1060, y), v, 42, col, b, "rm", "Black")
        b = prog(t, S.c(3), 0.5)
        d.line((290, 640, 1060, 640), fill=fade((70, 82, 108), b), width=2)
        text(d, (290, 700), "Zulage pro Jahr", 36, FG, b, "lm", "Bold")
        text(d, (1060, 700), eur(FAM) + " = 250 %", 46, AMBER, b, "rm", "Black")
    a = prog(t, S.c(4), 0.6)
    if a > 0:
        card(d, (1180, 260, 1860, 560), a, BLUE)
        text(d, (1220, 320), "Berufseinsteigerbonus", 34, MUTED, a, "lm", "SemiBold")
        text(d, (1220, 420), "+200 €", 80, BLUE, a, "lm", "Black")
        text(d, (1220, 510), "einmalig, wer vor 25 abschließt", 28, FG, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5))


def draw_steuer(img, d, t, S):
    title(d, t, "Zulage oder Steuervorteil?", S.c(0), "Das Finanzamt prüft automatisch, was mehr bringt (Günstigerprüfung)")
    a = prog(t, S.c(1), 0.5)
    if a > 0:
        text(d, (250, 260), f"Absetzbar als Sonderausgabe: 1.800 € + Zulage = {eur(SA)}", 36, FG, a, "lm", "Bold")
    for i, (st, b, save, col) in enumerate(((S.c(2), 3000, SAVE_3000, GREEN), (S.c(3), 5000, SAVE_5000, BLUE))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 330, x0 + 660, 760), a, col)
        text(d, (x0 + 40, 390), f"{eur(b)} brutto im Monat", 36, FG, a, "lm", "Bold")
        text(d, (x0 + 40, 470), "Steuerersparnis", 30, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 620, 470), eur(save), 40, FG, a, "rm", "Black")
        text(d, (x0 + 40, 550), "− Zulage", 30, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 620, 550), eur(540), 40, FG, a, "rm", "Black")
        d.line((x0 + 40, 600, x0 + 620, 600), fill=fade((70, 82, 108), a), width=2)
        text(d, (x0 + 40, 670), "zusätzlich zurück", 32, FG, a, "lm", "Bold")
        text(d, (x0 + 620, 670), "+" + eur(save - 540), 54, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (250, 860), "Je höher dein Steuersatz, desto mehr kommt über die Steuererklärung dazu.", 34, AMBER, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Beitrag 1.800 €/Jahr · StKl. I, kinderlos · Einkommensteuer-Tarif 2026 als Näherung, ohne Soli")


def draw_modell(img, d, t, S):
    title(d, t, "Was nach 30 Jahren daraus werden kann", S.c(0),
          "Modellrechnung: 150 €/Monat + 540 € Zulage, 5 % Rendite vor Kosten angenommen – keine Prognose")
    ch = Chart((260, 270, 1200, 860), (0, YEARS), (0, 150000))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(0, 31, 5), range(0, 150001, 50000), lambda v: f"{v} J.", lambda v: f"{v // 1000}.000 €" if v else "0 €")
    up = YEARS * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 0:
        ch.band(d, XS, CURVE_END, CURVE_ZUL, fade(AMBER, 0.35), up)
        ch.band(d, XS, CURVE_ZUL, CURVE_EIGEN, fade(GREEN, 0.45), up)
        ch.band(d, XS, CURVE_EIGEN, XS * 0, fade(BLUE, 0.45), up)
        ch.line(d, XS, CURVE_END, AMBER, 5, up)
    rows = [(S.c(1) + 0.5, "eigene Einzahlungen", eur(PAID), BLUE), (S.c(2), "Zulagen", eur(ZUL_SUM), GREEN),
            (S.c(3), "bei 1,0 % Kosten", "≈ " + eur(round(END_1, -2)), AMBER),
            (S.c(4), "bei 0,5 % Kosten", "≈ " + eur(round(END_05, -2)), AMBER)]
    for i, (st, lab, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 300 + i * 120
        card(d, (1280, y, 1870, y + 100), a, col)
        text(d, (1310, y + 50), lab, 28, MUTED, a, "lm", "SemiBold")
        text(d, (1840, y + 50), v, 38, col, a, "rm", "Black")
    a = prog(t, S.c(5), 0.5)
    text(d, (1280, 820), "Kosten machen hier gut 11.000 € aus.", 32, RED, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Modellrechnung, jährliche Einzahlung, konstante Rendite – Kurse können auch fallen")


def draw_auszahlung(img, d, t, S):
    title(d, t, "Und im Alter?", S.c(0), "Auszahlung und Steuern")
    items(d, t, S, [
        (S.c(1), "Beginn zwischen 65 und 70", "früher nur, wenn schon eine gesetzliche Altersrente läuft", BLUE),
        (S.c(2), "Rente oder Auszahlplan", "lebenslange Rente – oder Auszahlplan bis mindestens 85, Rest ist vererbbar", GREEN),
        (S.c(3), "Steuer erst im Alter", "Auszahlungen werden voll versteuert – mit dem dann meist niedrigeren Steuersatz", RED),
        (S.c(4), "Keine Kranken- und Pflegebeiträge", "für Pflichtversicherte in der gesetzlichen Krankenversicherung", VIOLET)])
    footer(d, prog(t, S.c(1), 0.5))


def draw_grenzen(img, d, t, S):
    title(d, t, "4 ehrliche Einschränkungen", S.c(0))
    items(d, t, S, [
        (S.c(1), "Keine Garantie", "Im Depot ohne Garantie kann am Ende auch weniger stehen als eingezahlt.", RED),
        (S.c(2), "Annahmen", "Die 5 % Rendite sind eine Annahme für die Rechnung, keine Prognose.", AMBER),
        (S.c(3), "Gebunden bis zur Rente", "Vorher kommt man nur in Ausnahmen förderunschädlich an das Geld.", BLUE),
        (S.c(4), "Nicht jeder ist förderberechtigt", "z. B. befreite Minijobber oder freiwillig Versicherte ohne weitere Voraussetzung.", GRAY)],
          y0=220, h=145, gap=25)


def draw_fazit(img, d, t, S):
    text_pop(d, (W / 2, 170), "Das Altersvorsorgedepot in 3 Sätzen", t, S.c(0), 56, FG, "mm", "Black")
    rows = [(S.c(1), GREEN, "Zulage:", "bis 50 % auf kleine Beiträge, maximal 540 € pro Jahr"),
            (S.c(2), BLUE, "Familien & junge Leute:", "300 € je Kind, 200 € Bonus unter 25"),
            (S.c(3), AMBER, "Haken:", "Geld gebunden bis zur Rente, kein Schutz vor Kursverlusten")]
    for i, (start, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 170
        card(d, (300, y, 1620, y + 140), a, col)
        text(d, (340, y + 50), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 100), b_txt, 40, FG, a, "lm", "Bold")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Regeln, nachgerechnet.", t, S.c(0), 52, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), "Alle Regeln, Annahmen & Quellen stehen in der Beschreibung.", t, S.c(1), 32, MUTED, "mm", "Medium")
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
        text(d, (1060, 580), "Gesetzliche Rente:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Was dein Gehalt bringt", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "mit offiziellen Werten", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Seit dem ersten Januar zweitausendsiebenundzwanzig gibt es eine neue geförderte Altersvorsorge: das Altersvorsorgedepot.",
            "Wer hundertfünfzig Euro im Monat einzahlt, also tausendachthundert Euro im Jahr,",
            "bekommt vom Staat bis zu fünfhundertvierzig Euro Zulage pro Jahr dazu.",
            "Wir rechnen nach, wie die Förderung funktioniert und für wen sie sich besonders lohnt. Mit den offiziellen Regeln des Finanzministeriums.",
        ], draw_hook),
        Scene("was", [
            "Was ist das Altersvorsorgedepot überhaupt?",
            "Es ist ein Depot ohne Garantie. Angelegt wird in Fonds und ETFs aus einer gesetzlichen Liste. Die Kurse können steigen, aber auch fallen.",
            "Jeder Anbieter muss außerdem ein Standarddepot anbieten: zwei Fonds, vor der Rente wird automatisch in den vorsichtigeren umgeschichtet, und die Kosten dürfen höchstens ein Prozent pro Jahr betragen.",
            "Wer Sicherheit will, kann weiterhin ein Garantieprodukt wählen, mit hundert oder achtzig Prozent der Einzahlungen garantiert.",
            "Und Riester? Neue Riester-Verträge gab es nur bis Ende zweitausendsechsundzwanzig. Bestehende Verträge laufen weiter.",
        ], draw_was),
        Scene("zulage", [
            "Jetzt zur Förderung, der Grundzulage.",
            "Für jeden Euro, den du einzahlst, gibt der Staat fünfzig Cent dazu. Das gilt bis dreihundertsechzig Euro im Jahr.",
            "Für jeden weiteren Euro gibt es fünfundzwanzig Cent, bis zu einem Eigenbeitrag von tausendachthundert Euro. Mehr als fünfhundertvierzig Euro Grundzulage gibt es also nicht.",
            "Das heißt: Bei zehn oder dreißig Euro im Monat bekommst du fünfzig Prozent dazu, bei hundert Euro zweiunddreißig Komma fünf, bei hundertfünfzig Euro dreißig Prozent.",
            "Voraussetzung ist ein Eigenbeitrag von mindestens zehn Euro im Monat.",
        ], draw_zulage),
        Scene("kinder", [
            "Besonders stark gefördert werden Familien.",
            "Ein Beispiel: fünfundzwanzig Euro im Monat, also dreihundert Euro im Jahr, und zwei Kinder.",
            "Die Grundzulage beträgt hundertfünfzig Euro. Dazu kommt für jedes Kind eine Kinderzulage von einem Euro pro eingezahltem Euro, bis dreihundert Euro.",
            "Zusammen siebenhundertfünfzig Euro Zulage auf dreihundert Euro Eigenbeitrag.",
            "Und wer vor seinem fünfundzwanzigsten Geburtstag einen Vertrag abschließt, bekommt einmalig zweihundert Euro Berufseinsteigerbonus.",
        ], draw_kinder),
        Scene("steuer", [
            "Für Menschen mit höherem Einkommen gibt es noch einen zweiten Vorteil.",
            "Beiträge und Zulage kannst du in der Steuererklärung als Sonderausgabe absetzen, bis zu tausendachthundert Euro plus Zulage, also zweitausenddreihundertvierzig Euro.",
            "Bei dreitausend Euro brutto im Monat spart das rund sechshundertdreißig Euro Steuer. Die fünfhundertvierzig Euro Zulage werden abgezogen, rund neunzig Euro kommen zusätzlich zurück.",
            "Bei fünftausend Euro brutto sind es rund siebenhundertfünfundachtzig Euro Ersparnis, also rund zweihundertfünfundvierzig Euro zusätzlich.",
            "Das Finanzamt prüft das automatisch. Je höher dein Steuersatz, desto mehr kommt dazu.",
        ], draw_steuer),
        Scene("modell", [
            "Was kann daraus über dreißig Jahre werden? Wir rechnen ein Modell mit angenommenen fünf Prozent Rendite pro Jahr vor Kosten. Das ist keine Prognose.",
            "Du zahlst hundertfünfzig Euro im Monat ein, über dreißig Jahre insgesamt vierundfünfzigtausend Euro.",
            "Der Staat legt sechzehntausendzweihundert Euro Zulage dazu.",
            "Bei einem Prozent Kosten pro Jahr, der Obergrenze im Standarddepot, stünden am Ende rund hunderteinunddreißigtausend Euro im Depot.",
            "Bei einem halben Prozent Kosten wären es rund hundertzweiundvierzigtausendachthundert Euro.",
            "Allein die Kosten machen in diesem Modell also gut elftausend Euro Unterschied.",
        ], draw_modell),
        Scene("auszahlung", [
            "Und wie kommt das Geld im Alter zurück?",
            "Die Auszahlung beginnt frühestens mit fünfundsechzig und spätestens mit siebzig. Früher nur, wenn du schon eine gesetzliche Altersrente bekommst.",
            "Du kannst wählen: eine lebenslange Rente oder einen Auszahlplan, der mindestens bis zum fünfundachtzigsten Geburtstag läuft. Was dann noch übrig ist, kann vererbt werden.",
            "Besteuert wird erst im Alter, und dann die ganze Auszahlung. Im Ruhestand ist der Steuersatz aber meist niedriger.",
            "Kranken- und Pflegeversicherungsbeiträge fallen für Pflichtversicherte nicht an.",
        ], draw_auszahlung),
        Scene("grenzen", [
            "Vier ehrliche Einschränkungen.",
            "Erstens: Im Depot ohne Garantie kann am Ende auch weniger stehen, als du eingezahlt hast.",
            "Zweitens: Die fünf Prozent Rendite in unserer Rechnung sind eine Annahme, keine Prognose.",
            "Drittens: Das Geld ist bis zur Rente gebunden. Vorher kommst du nur in Ausnahmen ohne Verlust der Förderung heran.",
            "Viertens: Nicht jeder ist förderberechtigt. Wer zum Beispiel als Minijobber von der Rentenversicherung befreit ist, bekommt keine eigene Zulage.",
        ], draw_grenzen),
        Scene("fazit", [
            "Das Altersvorsorgedepot in drei Sätzen.",
            "Kleine Beiträge bekommen bis zu fünfzig Prozent Zulage, maximal gibt es fünfhundertvierzig Euro pro Jahr.",
            "Familien und junge Leute werden zusätzlich gefördert: dreihundert Euro je Kind und zweihundert Euro Bonus unter fünfundzwanzig.",
            "Der Haken: Das Geld ist bis zur Rente gebunden, und ohne Garantie gibt es keinen Schutz vor Kursverlusten.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit den offiziellen Regeln.",
            "Alle Regeln, Annahmen und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video rechnen wir nach, wie viel gesetzliche Rente dein Gehalt bringt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
