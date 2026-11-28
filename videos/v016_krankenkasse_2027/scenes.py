"""Video 016: Krankenkasse 2027 – wer mehr zahlt, obwohl der Beitragssatz gleich bleibt."""
import numpy as np

from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, Chart, card, dot, ease_in_out, eur, fade, prog, text
from lib.longform import cards, fazit, footer, hook_two, numbered, outro, table, title

ALLG, ZUS = 14.6, 2.9                       # allgemeiner Beitragssatz, Ø-Zusatzbeitrag 2027 (BMG, 30.10.2026)
AN = (ALLG + ZUS) / 2 / 100                 # Arbeitnehmeranteil
BBG26, BBG27 = 5812.50, 6375.00             # Beitragsbemessungsgrenze KV pro Monat (2027 vorläufig)
RV26, RV27 = 8450, 8850                     # BBG Renten-/Arbeitslosenversicherung (2027 vorläufig)


def kv(brutto, bbg):
    return min(brutto, bbg) * AN


MAX26, MAX27 = kv(9999, BBG26), kv(9999, BBG27)
TAB = [(b, kv(b, BBG26), kv(b, BBG27)) for b in (3000, 5000, 6000, 7000)]
PP_3000 = 3000 * 0.01 / 2
PP_BBG = BBG27 * 0.01 / 2
XS = np.arange(2000, 8001, 50)

# Every number spoken in the narration is checked here.
assert abs(AN - 0.0875) < 1e-12 and round(ALLG + ZUS, 1) == 17.5
assert round(MAX26, 2) == 508.59 and round(MAX27, 2) == 557.81 and round(MAX27 - MAX26, 2) == 49.22
assert round(12 * (MAX27 - MAX26), 2) == 590.63
assert BBG27 - BBG26 == 562.5
assert [(round(a, 2), round(b, 2)) for _, a, b in TAB] == [(262.5, 262.5), (437.5, 437.5), (508.59, 525.0), (508.59, 557.81)]
assert round(TAB[2][2] - TAB[2][1], 2) == 16.41
assert PP_3000 == 15 and round(PP_BBG, 2) == 31.88 and 12 * PP_3000 == 180
assert round((RV27 - RV26) * 0.093, 2) == 37.2

SRC = "Ø-Zusatzbeitrag 2027: 2,9 % (BMG, 30.10.2026) · Beitragsbemessungsgrenze 2027 vorläufig (Kabinettsbeschluss)"


def draw_hook(img, d, t, S):
    hook_two(d, t, S, "Krankenkasse 2027", (1, "Ø-Beitragssatz", "17,5 %", "wie 2026", GREEN),
             (2, "Gutverdiener zahlen bis zu", "+49,22 €", "mehr im Monat", RED),
             (3, "Warum – und was ein Kassenwechsel bringen kann"), SRC)


def draw_satz(img, d, t, S):
    title(d, t, "Woraus sich der Beitrag zusammensetzt", S.c(0))
    cards(d, t, [(S.c(1), "Allgemeiner Beitragssatz: 14,6 %", "gilt bei allen gesetzlichen Kassen", BLUE),
                 (S.c(2), "Zusatzbeitrag: Ø 2,9 % für 2027", "jede Kasse legt ihren eigenen fest", VIOLET),
                 (S.c(3), "Zusammen 17,5 % – die Hälfte zahlst du", "8,75 % vom Brutto, den Rest der Arbeitgeber", GREEN)],
          y0=250, h=170, gap=30)
    footer(d, prog(t, S.c(1), 0.5), SRC)


def draw_bbg(img, d, t, S):
    title(d, t, "Der Grund: die Beitragsbemessungsgrenze", S.c(0), "Krankenversicherungsbeitrag (Arbeitnehmeranteil) je Monatsbrutto")
    ch = Chart((260, 270, 1300, 860), (2000, 8000), (0, 600))
    ax = prog(t, S.c(0) + 0.3, 0.8)
    ch.axes(d, ax, range(2000, 8001, 1000), range(0, 601, 100), lambda v: f"{v // 1000}.000 €", lambda v: f"{v} €", "Monatsbrutto")
    up = 2000 + 6000 * prog(t, S.c(1), S.e(2) - S.c(1), ease_in_out)
    if up > 2000:
        ch.line(d, XS, np.array([kv(x, BBG27) for x in XS]), RED, 6, up)
        ch.line(d, XS, np.array([kv(x, BBG26) for x in XS]), GRAY, 6, up)
    text(d, (1340, 330), "2026: bis 5.812,50 €", 30, GRAY, ax, "lm", "Bold")
    text(d, (1340, 380), "2027: bis 6.375,00 €", 30, RED, ax, "lm", "Bold")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        card(d, (1340, 450, 1870, 760), a, RED)
        text(d, (1370, 505), "Höchstbeitrag", 30, MUTED, a, "lm", "SemiBold")
        text(d, (1370, 580), f"{eur(MAX26, 2)} → {eur(MAX27, 2)}", 34, FG, a, "lm", "Black")
        text(d, (1370, 665), "+49,22 € / Monat", 44, RED, a, "lm", "Black")
        text(d, (1370, 725), "+590,63 € im Jahr", 30, FG, a, "lm", "Medium")
    footer(d, prog(t, S.c(1), 0.5), "BBG 2027: +562,50 € pro Monat, davon 300 € Sonderanhebung · vorläufige Rechengrößen")


def draw_tabelle(img, d, t, S):
    title(d, t, "Was sich je nach Gehalt ändert", S.c(0), "Krankenversicherung, Arbeitnehmeranteil, Ø-Zusatzbeitrag")
    cols = [(290, "Monatsbrutto", "lm"), (900, "2026", "mm"), (1250, "2027", "mm"), (1550, "Änderung", "mm")]
    rows = []
    for i, (b, a26, a27) in enumerate(TAB):
        diff = a27 - a26
        st = S.c(1) + i * 0.6 if i < 2 else S.c(2) + (i - 2) * 0.8
        rows.append((st, [(eur(b), FG), (eur(a26, 2), FG), (eur(a27, 2), FG),
                          ("±0 €" if diff < 0.005 else "+" + eur(diff, 2), GREEN if diff < 0.005 else RED)],
                     GREEN if diff < 0.005 else RED))
    table(d, t, rows, cols, y0=300, row_h=125)
    a = prog(t, S.c(3), 0.5)
    text(d, (250, 860), "Unter 5.812,50 € brutto ändert sich bei gleichem Zusatzbeitrag nichts.", 36, AMBER, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC)


def draw_zusatz(img, d, t, S):
    title(d, t, "Was ein Prozentpunkt Zusatzbeitrag kostet", S.c(0), "Du trägst die Hälfte des Zusatzbeitrags")
    for i, (st, lab, m, y, col) in enumerate(((S.c(1), "bei 3.000 € brutto", PP_3000, 12 * PP_3000, BLUE),
                                              (S.c(2), "ab 6.375 € brutto (Grenze 2027)", PP_BBG, 12 * PP_BBG, VIOLET))):
        a = prog(t, st, 0.6)
        if a <= 0:
            continue
        x0 = 250 + i * 720
        card(d, (x0, 270, x0 + 660, 600), a, col)
        text(d, (x0 + 40, 330), lab, 34, MUTED, a, "lm", "SemiBold")
        text(d, (x0 + 40, 440), eur(m, 2) + " / Monat", 64, col, a, "lm", "Black")
        text(d, (x0 + 40, 530), eur(y, 2) + " im Jahr", 36, FG, a, "lm", "Bold")
    a = prog(t, S.c(3), 0.5)
    text(d, (250, 700), "Pro 0,1 Prozentpunkte: 1,50 € im Monat bei 3.000 € brutto.", 36, AMBER, a, "lm", "Bold")
    footer(d, prog(t, S.c(1), 0.5), "Unterschied im Zusatzbeitrag × Brutto (bis zur Grenze) ÷ 2")


def draw_wechsel(img, d, t, S):
    title(d, t, "Wann man die Kasse wechseln kann", S.c(0))
    cards(d, t, [(S.c(1), "Nach 12 Monaten Mitgliedschaft", "Kündigungsfrist: zwei Monate zum Monatsende", BLUE),
                 (S.c(2), "Bei Erhöhung des Zusatzbeitrags sofort", "Sonderkündigung bis Ende des Monats, ab dem der höhere Beitrag gilt", AMBER),
                 (S.c(3), "Leistungen sind größtenteils gleich", "gesetzlich festgelegt – Unterschiede vor allem bei Extras", GREEN)],
          y0=250, h=170, gap=30)
    footer(d, prog(t, S.c(1), 0.5), "§ 175 SGB V (Kassenwahlrecht, Bindungsfrist, Sonderkündigungsrecht)")


def draw_grenzen(img, d, t, S):
    numbered(d, t, S, [(1, "Vorläufige Grenzen", "Die Rechengrößen 2027 standen bei Erstellung als Kabinettsbeschluss fest."),
                       (2, "Nur Krankenversicherung", "Auch die Grenze für Renten- und Arbeitslosenversicherung steigt (vorläufig 8.850 €)."),
                       (3, "Durchschnitt", "Deine Kasse kann einen höheren oder niedrigeren Zusatzbeitrag verlangen.")],
             "3 ehrliche Einschränkungen")


def draw_fazit(img, d, t, S):
    fazit(d, t, S, "Krankenkasse 2027", [
        (1, GREEN, "Bis 5.812,50 € brutto:", "bei gleichem Zusatzbeitrag keine Änderung"),
        (2, RED, "Darüber:", "bis zu 49,22 € mehr im Monat durch die höhere Grenze"),
        (3, AMBER, "Zusatzbeitrag vergleichen:", "1 Prozentpunkt = 15 € im Monat bei 3.000 €")])


def draw_outro(img, d, t, S):
    outro(d, t, S)


def scenes():
    return [
        Scene("hook", [
            "Der durchschnittliche Beitragssatz für die Krankenkasse bleibt zweitausendsiebenundzwanzig bei siebzehn Komma fünf Prozent.",
            "Trotzdem zahlen viele mehr.",
            "Wer gut verdient, bis zu neunundvierzig Euro zweiundzwanzig mehr im Monat.",
            "Wir rechnen nach, woran das liegt und was ein Kassenwechsel bringen kann.",
        ], draw_hook),
        Scene("satz", [
            "Zuerst: Woraus besteht der Beitrag?",
            "Aus dem allgemeinen Beitragssatz von vierzehn Komma sechs Prozent, der gilt bei allen gesetzlichen Kassen.",
            "Und dem Zusatzbeitrag, den jede Kasse selbst festlegt. Im Durchschnitt beträgt er zweitausendsiebenundzwanzig zwei Komma neun Prozent.",
            "Zusammen siebzehn Komma fünf Prozent. Die Hälfte davon, acht Komma sieben fünf Prozent, zahlst du, den Rest dein Arbeitgeber.",
        ], draw_satz),
        Scene("bbg", [
            "Der Grund für den Anstieg ist die Beitragsbemessungsgrenze.",
            "Beiträge werden nur bis zu einem bestimmten Gehalt berechnet. Zweitausendsechsundzwanzig waren das fünftausendachthundertzwölf Euro fünfzig im Monat.",
            "Zweitausendsiebenundzwanzig steigt die Grenze vorläufig auf sechstausenddreihundertfünfundsiebzig Euro, also um fünfhundertzweiundsechzig Euro fünfzig. Dreihundert Euro davon sind eine Sonderanhebung.",
            "Der Höchstbeitrag steigt damit von fünfhundertacht Euro neunundfünfzig auf fünfhundertsiebenundfünfzig Euro einundachtzig. Das sind neunundvierzig Euro zweiundzwanzig mehr im Monat, fünfhundertneunzig Euro im Jahr.",
        ], draw_bbg),
        Scene("tabelle", [
            "Was heißt das für verschiedene Gehälter?",
            "Bei dreitausend und bei fünftausend Euro brutto ändert sich nichts, wenn die Kasse ihren Zusatzbeitrag nicht erhöht.",
            "Bei sechstausend Euro sind es sechzehn Euro einundvierzig mehr, ab sechstausenddreihundertfünfundsiebzig Euro die vollen neunundvierzig Euro zweiundzwanzig.",
            "Wer unter fünftausendachthundertzwölf Euro fünfzig verdient, merkt von der neuen Grenze also nichts.",
        ], draw_tabelle),
        Scene("zusatz", [
            "Und was macht der Zusatzbeitrag deiner Kasse aus?",
            "Ein Prozentpunkt mehr oder weniger kostet dich bei dreitausend Euro brutto fünfzehn Euro im Monat, hundertachtzig Euro im Jahr.",
            "Ab der neuen Grenze sind es einunddreißig Euro achtundachtzig im Monat.",
            "Pro null Komma eins Prozentpunkte sind es bei dreitausend Euro brutto einen Euro fünfzig im Monat.",
        ], draw_zusatz),
        Scene("wechsel", [
            "Wann kann man die Krankenkasse wechseln?",
            "Nach zwölf Monaten Mitgliedschaft jederzeit, mit zwei Monaten Kündigungsfrist zum Monatsende.",
            "Erhöht deine Kasse den Zusatzbeitrag, kannst du sofort kündigen, und zwar bis zum Ende des Monats, ab dem der höhere Beitrag gilt.",
            "Die Leistungen sind größtenteils gesetzlich festgelegt. Unterschiede gibt es vor allem bei Extras.",
        ], draw_wechsel),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Die Grenzen für zweitausendsiebenundzwanzig standen bei Erstellung des Videos als Kabinettsbeschluss fest und waren noch vorläufig.",
            "Zweitens: Wir rechnen nur die Krankenversicherung. Auch die Grenze für Renten- und Arbeitslosenversicherung steigt, vorläufig auf achttausendachthundertfünfzig Euro.",
            "Drittens: Der Zusatzbeitrag ist ein Durchschnitt. Deine Kasse kann mehr oder weniger verlangen.",
        ], draw_grenzen),
        Scene("fazit", [
            "Die Krankenkasse zweitausendsiebenundzwanzig in drei Sätzen.",
            "Wer bis fünftausendachthundertzwölf Euro fünfzig verdient, zahlt bei gleichem Zusatzbeitrag nicht mehr.",
            "Darüber werden durch die höhere Grenze bis zu neunundvierzig Euro zweiundzwanzig mehr im Monat fällig.",
            "Und den Zusatzbeitrag zu vergleichen lohnt sich: Ein Prozentpunkt sind bei dreitausend Euro fünfzehn Euro im Monat.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung und keine Empfehlung für eine Kasse, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Werte und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal. Jeden Donnerstag kommt ein neues Video.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
