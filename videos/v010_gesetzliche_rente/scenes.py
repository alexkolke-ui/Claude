"""Video 010: Gesetzliche Rente – wie viel Rente dein Gehalt bringt (offizielle Werte 2026)."""
import numpy as np

from lib.engine import Scene
from lib.gfx import (AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, H, Chart, card, dot, ease_in_out, eur,
                     fade, lerp, prog, rrect, text, text_pop)
from lib.lohn2026 import netto_monat

RW = 42.52            # aktueller Rentenwert ab 1.7.2026 (RWBestV 2026)
DE = 51944            # vorläufiges Durchschnittsentgelt 2026 (SV-Rechengrößenverordnung 2026)
BBG = 101400          # Beitragsbemessungsgrenze Rentenversicherung 2026, jährlich
JAHRE = 45
KVPV = 0.073 + 0.0145 + 0.036 + 0.006   # Rentner: KV 7,3 % + halber Ø-Zusatzbeitrag, PV 3,6 % + 0,6 % kinderlos


def ep(brutto_monat):
    return min(brutto_monat * 12, BBG) / DE


def rente(brutto_monat, jahre=JAHRE):
    return ep(brutto_monat) * jahre * RW


B = 3000
EP1 = ep(B)
EP45 = EP1 * JAHRE
R = rente(B)
R_NET = R * (1 - KVPV)
GEHALT_NET = netto_monat(B)["Netto"]
STD = JAHRE * RW
AVG_M = DE / 12
TAB = [(b, rente(b)) for b in (2000, 3000, AVG_M, 6000, 8450)]
CURVE_B = np.arange(1000, 9001, 50)
CURVE_R = np.array([rente(b) for b in CURVE_B])

# Every number spoken in the narration is checked here.
assert round(EP1, 4) == 0.6931 and round(EP45, 2) == 31.19 and round(R, 2) == 1326.09
assert abs(KVPV - 0.1295) < 1e-12 and round(R_NET, 2) == 1154.36
assert GEHALT_NET == 2054.42 and 0.56 < R_NET / GEHALT_NET < 0.565 and 895 < GEHALT_NET - R_NET < 905
assert round(STD, 2) == 1913.40 and round(AVG_M, 2) == 4328.67 and 0.44 < STD / AVG_M < 0.445
assert [round(r) for _, r in TAB] == [884, 1326, 1913, 2652, 3735]
assert round(BBG / DE, 2) == 1.95

SRC = "Rentenwert 42,52 € (ab 1.7.2026) · vorläufiges Durchschnittsentgelt 2026: 51.944 € · DRV / BMAS"


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha=1.0, s=SRC):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def dec(v, n=2):
    return f"{v:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def draw_hook(img, d, t, S):
    text_pop(d, (W / 2, 160), "3.000 € brutto, 45 Jahre lang", t, S.c(0), 56, FG, "mm", "Black")
    a = prog(t, S.c(1), 0.6)
    if a > 0:
        card(d, (560, 260, 1360, 560), a, BLUE)
        text(d, (W / 2, 320), "gesetzliche Rente (brutto)", 36, MUTED, a, "mm", "SemiBold")
        p = prog(t, S.c(1) + 0.2, 1.4, ease_in_out)
        text(d, (W / 2, 430), eur(R * p, 2), 100, BLUE, a, "mm", "Black")
        text(d, (W / 2, 515), "in heutigen Werten", 30, FG, a, "mm", "Medium")
    a = prog(t, S.c(2), 0.6)
    if a > 0:
        rrect(d, (460, 640, 1460, 760), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 700), "Wie das berechnet wird – und was netto übrig bleibt", 40, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6))


def draw_formel(img, d, t, S):
    title(d, t, "Die Rentenformel, vereinfacht", S.c(0), "Entgeltpunkte × aktueller Rentenwert")
    rows = [(S.c(1), "1. Entgeltpunkte pro Jahr", f"36.000 € ÷ {dec(DE, 0)} €", dec(EP1, 4), BLUE),
            (S.c(2), "2. nach 45 Jahren", f"{dec(EP1, 4)} × 45", dec(EP45, 2), VIOLET),
            (S.c(3), "3. × aktueller Rentenwert", f"{dec(EP45, 2)} × {dec(RW)} €", eur(R, 2), GREEN)]
    for i, (st, lab, f, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 190
        card(d, (250, y, 1670, y + 160), a, col)
        text(d, (290, y + 58), lab, 38, FG, a, "lm", "Bold")
        text(d, (290, y + 115), f, 30, MUTED, a, "lm", "Medium")
        text(d, (1630, y + 80), v, 60, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    text(d, (250, 870), "Wer genau so viel verdient wie der Durchschnitt, bekommt 1 Entgeltpunkt pro Jahr.", 32, AMBER, a,
         "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5))


def draw_tabelle(img, d, t, S):
    title(d, t, "Rente nach 45 Jahren – je nach Gehalt", S.c(0), "Monatsbrutto heute, Rente brutto in heutigen Werten")
    ch = Chart((260, 270, 1200, 860), (1000, 9000), (0, 4000))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(1000, 9001, 2000), range(0, 4001, 1000), lambda v: f"{v // 1000}.000 €",
            lambda v: f"{v // 1000}.000 €" if v else "0 €", "Monatsbrutto")
    up = 1000 + 8000 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 1000:
        ch.line(d, CURVE_B, CURVE_R, BLUE, 6, up)
    a = prog(t, S.c(1) + 0.5, 0.5)
    if a > 0:
        card(d, (1280, 270, 1870, 720), a)
        text(d, (1310, 320), "Brutto → Rente", 28, MUTED, a, "lm", "SemiBold")
        for i, (b, r) in enumerate(TAB):
            y = 390 + i * 70
            lab = "Ø " + eur(b) if i == 2 else ("≥ " if i == 4 else "") + eur(b)
            text(d, (1310, y), lab, 32, AMBER if i == 2 else FG, a, "lm", "SemiBold")
            text(d, (1840, y), eur(r), 36, BLUE, a, "rm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        p = ch.px(8450, rente(8450))
        dot(d, p, 10, RED)
        text(d, (p[0] - 14, p[1] - 18), "Grenze: 8.450 €", 26, RED, a, "rb", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC + " · BBG 8.450 €/Monat")


def draw_netto(img, d, t, S):
    title(d, t, "Was von der Rente netto bleibt", S.c(0), "Rentner zahlen Kranken- und Pflegeversicherung")
    rows = [(S.c(1), "Rente brutto", eur(R, 2), FG),
            (S.c(2), "Krankenversicherung 7,3 % + 1,45 %", "−" + eur(R * 0.0875, 2), BLUE),
            (S.c(3), "Pflegeversicherung 3,6 % + 0,6 % (kinderlos)", "−" + eur(R * 0.042, 2), BLUE)]
    for i, (st, lab, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 95
        text(d, (250, y), lab, 36, FG if i == 0 else MUTED, a, "lm", "SemiBold")
        text(d, (1400, y), v, 44, col, a, "rm", "Black")
    a = prog(t, S.c(4), 0.5)
    if a > 0:
        d.line((250, 560, 1400, 560), fill=fade((70, 82, 108), a), width=2)
        text(d, (250, 620), "vor Steuern", 38, FG, a, "lm", "Bold")
        text(d, (1400, 620), eur(R_NET, 2), 56, GREEN, a, "rm", "Black")
    a = prog(t, S.c(5), 0.5)
    if a > 0:
        rrect(d, (250, 720, 1670, 880), 20, fill=fade((50, 26, 30), a), outline=fade(RED, a * 0.6), width=2)
        text(d, (290, 770), f"Heutiges Nettogehalt bei 3.000 € brutto: {eur(GEHALT_NET, 2)}", 34, FG, a, "lm", "SemiBold")
        text(d, (290, 835), f"Rente vor Steuern: rund 56 % davon – Lücke ≈ {eur(round(GEHALT_NET - R_NET, -1))}", 38, RED, a,
             "lm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "Zusatzbeitrag Ø 2,9 % · Steuern nicht berücksichtigt · Nettogehalt StKl. I wie in Video 6")


def draw_niveau(img, d, t, S):
    title(d, t, "Und das Rentenniveau von 48 %?", S.c(0), "Gilt für die Standardrente: 45 Jahre Durchschnittsverdienst")
    for i, (st, lab, v, sub, col) in enumerate(((S.c(1), "Standardrente", eur(STD, 2), "45 Entgeltpunkte × 42,52 €", BLUE),
                                                (S.c(2), "Ø-Bruttoverdienst", eur(AVG_M, 2), "51.944 € ÷ 12", GRAY))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 270, x0 + 660, 560), a, col)
        text(d, (x0 + 40, 330), lab, 34, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 430), v, 72, col, a, "lm", "Black")
        text(d, (x0 + 40, 510), sub, 28, FG, a, "lm", "Medium")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        text(d, (250, 650), f"Brutto-Rente ÷ Brutto-Lohn = {dec(STD / AVG_M * 100, 1)} %", 44, AMBER, a, "lm", "Black")
        text(d, (250, 720), "Die 48 % vergleichen Beträge nach Sozialabgaben und vor Steuern.", 34, FG, a, "lm", "SemiBold")
    a = prog(t, S.c(4), 0.5)
    text(d, (250, 820), "Und sie gelten nur für 45 volle Jahre mit Durchschnittsgehalt.", 34, MUTED, a, "lm", "SemiBold")
    footer(d, prog(t, S.c(1), 0.5), "DRV: Rentenniveau vor Steuern 2026: 48,0 %")


def draw_grenzen(img, d, t, S):
    title(d, t, "4 ehrliche Einschränkungen", S.c(0))
    items = [(S.c(1), "1", "Heutige Werte", "Rentenwert und Löhne steigen – gerechnet ist in heutigen Euro."),
             (S.c(2), "2", "45 Jahre ohne Lücke", "Teilzeit, Studium oder Arbeitslosigkeit ändern die Punkte."),
             (S.c(3), "3", "Vereinfacht", "Ohne Kindererziehungszeiten, Abschläge oder Zurechnungszeiten."),
             (S.c(4), "4", "Steuern fehlen", "Je nach Einkommen kann auf die Rente noch Steuer anfallen.")]
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


def draw_fazit(img, d, t, S):
    text_pop(d, (W / 2, 170), "Was die gesetzliche Rente bringt", t, S.c(0), 56, FG, "mm", "Black")
    rows = [(S.c(1), BLUE, "Rechnung:", "Gehalt ÷ Durchschnitt × Jahre × 42,52 €"),
            (S.c(2), GREEN, "Bei 3.000 € brutto:", "rund 1.326 € brutto, 1.154 € vor Steuern"),
            (S.c(3), RED, "Lücke:", "rund 900 € weniger als das heutige Netto")]
    for i, (start, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, start, 0.5)
        if a <= 0:
            continue
        y = 280 + i * 170
        card(d, (300, y, 1620, y + 140), a, col)
        text(d, (340, y + 50), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 100), b_txt, 40, FG, a, "lm", "Bold")


def draw_outro(img, d, t, S):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Werte, nachgerechnet.", t, S.c(0), 52, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), "Formel, Werte & Quellen stehen in der Beschreibung.", t, S.c(1), 32, MUTED, "mm", "Medium")
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
        text(d, (1060, 580), "Steuererklärung 2026:", 40, FG, a, "lm", "Bold")
        text(d, (1060, 630), "Was zurückkommt", 40, FG, a, "lm", "Bold")
        text(d, (1060, 720), "Pendler, Homeoffice & Co.", 26, MUTED, a, "lm", "Medium")


def scenes():
    return [
        Scene("hook", [
            "Dreitausend Euro brutto im Monat, fünfundvierzig Jahre lang.",
            "Das bringt nach heutigen Werten eine gesetzliche Rente von rund tausenddreihundertsechsundzwanzig Euro brutto.",
            "Wir rechnen nach, wie diese Zahl entsteht und was davon netto übrig bleibt. Mit den offiziellen Werten der Rentenversicherung.",
        ], draw_hook),
        Scene("formel", [
            "Die Rentenformel ist im Kern ganz einfach.",
            "Erstens: Jedes Jahr bekommst du Entgeltpunkte. Dein Jahresbrutto geteilt durch das Durchschnittsentgelt, vorläufig einundfünfzigtausendneunhundertvierundvierzig Euro. Bei sechsunddreißigtausend Euro sind das null Komma sechs neun drei eins Punkte.",
            "Zweitens: Nach fünfundvierzig Jahren hast du einunddreißig Komma eins neun Punkte gesammelt.",
            "Drittens: Jeder Punkt ist seit Juli zweitausendsechsundzwanzig zweiundvierzig Euro zweiundfünfzig wert. Ergibt tausenddreihundertsechsundzwanzig Euro Rente im Monat.",
            "Wer genau so viel verdient wie der Durchschnitt, bekommt also einen Punkt pro Jahr.",
        ], draw_formel),
        Scene("tabelle", [
            "So sieht das bei anderen Gehältern aus, jeweils nach fünfundvierzig Jahren.",
            "Zweitausend Euro brutto bringen rund achthundertvierundachtzig Euro Rente. Wer mit rund viertausenddreihundertneunundzwanzig Euro genau den Durchschnitt verdient, bekommt rund tausendneunhundertdreizehn Euro.",
            "Sechstausend Euro bringen rund zweitausendsechshundertzweiundfünfzig Euro.",
            "Mehr als rund dreitausendsiebenhundertfünfunddreißig Euro geht nicht. Denn Beiträge zählen nur bis achttausendvierhundertfünfzig Euro im Monat, das sind höchstens eins Komma neun fünf Punkte pro Jahr.",
        ], draw_tabelle),
        Scene("netto", [
            "Und was bleibt netto?",
            "Von tausenddreihundertsechsundzwanzig Euro Rente",
            "gehen acht Komma sieben fünf Prozent an die Krankenversicherung,",
            "und vier Komma zwei Prozent an die Pflegeversicherung, wenn man keine Kinder hat.",
            "Übrig bleiben tausendeinhundertvierundfünfzig Euro, noch vor einer möglichen Steuer.",
            "Zum Vergleich: Bei dreitausend Euro brutto bleiben heute zweitausendvierundfünfzig Euro netto. Die Rente liegt also bei rund sechsundfünfzig Prozent davon, eine Lücke von rund neunhundert Euro im Monat.",
        ], draw_netto),
        Scene("niveau", [
            "Und was ist mit dem Rentenniveau von achtundvierzig Prozent, von dem oft die Rede ist?",
            "Es bezieht sich auf die Standardrente: fünfundvierzig Jahre mit Durchschnittsverdienst. Das sind tausendneunhundertdreizehn Euro vierzig.",
            "Der durchschnittliche Bruttoverdienst liegt bei rund viertausenddreihundertneunundzwanzig Euro im Monat.",
            "Brutto gerechnet sind das nur vierundvierzig Prozent. Die achtundvierzig Prozent vergleichen Beträge nach Sozialabgaben und vor Steuern.",
            "Und sie gelten nur für fünfundvierzig volle Jahre mit Durchschnittsgehalt.",
        ], draw_niveau),
        Scene("grenzen", [
            "Vier ehrliche Einschränkungen.",
            "Erstens: Wir rechnen in heutigen Werten. Rentenwert und Löhne steigen in der Regel, entscheidend ist das Verhältnis.",
            "Zweitens: Wir gehen von fünfundvierzig Jahren ohne Lücke aus. Teilzeit, Studium oder Arbeitslosigkeit ändern die Punkte.",
            "Drittens: Kindererziehungszeiten, Abschläge oder andere Sonderregeln sind nicht eingerechnet.",
            "Viertens: Steuern fehlen. Je nach Einkommen kann auf die Rente noch Einkommensteuer anfallen.",
        ], draw_grenzen),
        Scene("fazit", [
            "Was bringt die gesetzliche Rente also?",
            "Die Rechnung: Gehalt geteilt durch den Durchschnitt, mal Jahre, mal zweiundvierzig Euro zweiundfünfzig.",
            "Bei dreitausend Euro brutto sind das rund tausenddreihundertsechsundzwanzig Euro Rente, vor Steuern rund tausendeinhundertvierundfünfzig.",
            "Das sind rund neunhundert Euro weniger als das heutige Netto. Genau diese Lücke soll private Vorsorge schließen.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Werten.",
            "Formel, Werte und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video: die Steuererklärung für zweitausendsechsundzwanzig. Wann sie sich lohnt und was zurückkommt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
