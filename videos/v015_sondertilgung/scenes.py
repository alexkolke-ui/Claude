"""Video 015: Sondertilgung oder sparen? Die Tilgungs-Leiter vom Dispo bis zum Baukredit (Bundesbank-Daten)."""
from lib.engine import Scene
from lib.gfx import AMBER, BLUE, FG, GRAY, GREEN, MUTED, RED, VIOLET, W, card, ease_in_out, eur, fade, prog, text
from lib.longform import cards, fazit, footer, hook_two, numbered, outro, title
from videos.v004_kredite.scenes import B10_NOW, D_NOW, R_NOW
from videos.v014_festgeld_tagesgeld.scenes import F3, M, TG

TAX = 0.25 * 1.055
BETRAG, JAHRE = 10000, 10
FGZ = F3[M]
FG_NET = FGZ * (1 - TAX)
ST_END = BETRAG * (1 + B10_NOW / 100 / 12) ** (12 * JAHRE)      # Restschuld sinkt um diesen Betrag (Annuität bleibt gleich)
FG_END = BETRAG * (1 + FGZ / 100) ** JAHRE
FG_NET_END = BETRAG * (1 + FG_NET / 100) ** JAHRE
TG_END = BETRAG * (1 + TG[M] / 100) ** JAHRE
LEITER = [("Dispo (Ø)", D_NOW, RED), ("Ratenkredit (Ø, effektiv)", R_NOW, RED), ("Baukredit 5–10 J. (Ø)", B10_NOW, BLUE),
          ("Festgeld über 2 J. (Ø)", FGZ, GREEN), ("Tagesgeld & Giro (Ø)", TG[M], GRAY)]

# Every number spoken in the narration is checked here.
assert (D_NOW, R_NOW, B10_NOW, FGZ, TG[M]) == (9.59, 8.91, 3.91, 2.83, 0.52)
assert round(ST_END - BETRAG) == 4775 and round(FG_END - BETRAG) == 3219
assert round(FG_NET_END - BETRAG) == 2290 and round(TG_END - BETRAG) == 532
assert round(FG_NET, 2) == 2.08 and round(100 * D_NOW) == 959 and round(100 * TG[M]) == 52

SRC = "Durchschnittszinsen Sept. 2026: Deutsche Bundesbank, MFI-Zinsstatistik (SUD112, SUD130, SUD118, SUD104, SUD101)"


def pct(v, dec=2):
    return f"{v:.{dec}f}".replace(".", ",") + " %"


def draw_hook(img, d, t, S):
    hook_two(d, t, S, "10.000 € übrig – was tun?", (1, "Sondertilgung Baukredit", "+" + eur(ST_END - BETRAG),
                                                     "gesparte Zinsen in 10 Jahren", BLUE),
             (2, "Festgeld (nach Steuer)", "+" + eur(round(FG_NET_END - BETRAG, -1)), "Zinsen in 10 Jahren", GREEN),
             (3, "Warum Tilgen oft mehr bringt als Sparen – und wann nicht"), SRC)


def draw_leiter(img, d, t, S):
    title(d, t, "Die Tilgungs-Leiter", S.c(0), "Jeder zurückgezahlte Euro „verdient“ den Zins, den er nicht mehr kostet")
    for i, (n, r, col) in enumerate(LEITER):
        st = S.c(1) + i * 0.6 if i < 3 else S.c(2) + (i - 3) * 0.7
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 120
        text(d, (690, y + 40), n, 34, FG, a, "rm", "SemiBold")
        w = r * 95 * prog(t, st, 0.9, ease_in_out)
        d.rounded_rectangle((720, y + 10, 720 + max(w, 6), y + 70), 12, fill=fade(col, a))
        text(d, (735 + w, y + 40), pct(r), 40, col, a, "lm", "Black")
    a = prog(t, S.c(3), 0.5)
    if a > 0:
        d.line((250, 600, 1700, 600), fill=fade(AMBER, a), width=3)
        text(d, (1700, 585), "oben: Schulden  ·  unten: Sparen", 26, AMBER, a, "rb", "Bold")
    footer(d, prog(t, S.c(1), 0.5), SRC)


def draw_steuer(img, d, t, S):
    title(d, t, "Ein Vorteil, den man leicht übersieht", S.c(0), "Gesparte Kreditzinsen werden nicht besteuert")
    cards(d, t, [(S.c(1), "Sparzinsen über 1.000 € im Jahr", "werden mit 26,375 % besteuert (Abgeltungsteuer + Soli)", RED),
                 (S.c(2), f"Festgeld {pct(FGZ)} → netto {pct(FG_NET)}", "wer den Sparerpauschbetrag schon ausschöpft", GREEN),
                 (S.c(3), f"Baukredit {pct(B10_NOW)} getilgt → {pct(B10_NOW)} gespart", "ohne Steuer, ohne Kursrisiko", BLUE)],
          y0=250, h=170, gap=30)
    footer(d, prog(t, S.c(1), 0.5), "§ 20 Abs. 9, § 32d EStG · Durchschnittszinsen Sept. 2026")


def draw_beispiel(img, d, t, S):
    title(d, t, "10.000 € über 10 Jahre", S.c(0), "Modellrechnung mit konstanten Durchschnittszinsen von September 2026")
    rows = [(S.c(1), "Sondertilgung Baukredit (3,91 %)", "Restschuld sinkt um", ST_END - BETRAG, BLUE),
            (S.c(2), "Festgeld 2,83 % vor Steuer", "Zinsen", FG_END - BETRAG, GREEN),
            (S.c(2) + 1.0, "Festgeld nach Steuer (2,08 %)", "Zinsen", FG_NET_END - BETRAG, GREEN),
            (S.c(3), "Tagesgeld & Giro (0,52 %)", "Zinsen", TG_END - BETRAG, GRAY)]
    for i, (st, lab, sub, v, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = 260 + i * 140
        card(d, (250, y, 1670, y + 120), a, col)
        text(d, (290, y + 45), lab, 36, FG, a, "lm", "Bold")
        text(d, (290, y + 92), sub, 26, MUTED, a, "lm", "Medium")
        p = prog(t, st + 0.2, 1.0, ease_in_out)
        text(d, (1630, y + 60), "+" + eur(v * p), 54, col, a, "rm", "Black")
    footer(d, prog(t, S.c(1), 0.5), "Sondertilgung: Rate bleibt gleich, Restschuld nach 10 J. sinkt um 10.000 € × (1 + 3,91 %/12)^120 − 10.000 €")


def draw_aber(img, d, t, S):
    title(d, t, "Aber: drei Dinge vorher prüfen", S.c(0))
    cards(d, t, [(S.c(1), "Notgroschen behalten", "Getilgtes Geld ist weg – bei Bedarf gibt es dafür keinen günstigen Kredit", AMBER),
                 (S.c(2), "Baukredit: nur wenn vereinbart", "Sondertilgungen während der Zinsbindung nur, wenn der Vertrag sie erlaubt", BLUE),
                 (S.c(3), "Ratenkredit: jederzeit möglich", "Vorfälligkeitsentschädigung höchstens 1 % (0,5 % bei unter 1 Jahr Restlaufzeit)", RED)],
          y0=250, h=170, gap=30)
    footer(d, prog(t, S.c(1), 0.5), "§ 500, § 502 BGB (Verbraucherdarlehen)")


def draw_grenzen(img, d, t, S):
    numbered(d, t, S, [(1, "Durchschnittszinsen", "Dein eigener Kredit- und Sparzins kann deutlich abweichen."),
                       (2, "Konstante Zinsen angenommen", "Festgeld über 10 Jahre zum heutigen Satz ist eine Vereinfachung."),
                       (3, "Steuer nur über dem Pauschbetrag", "Bis 1.000 € Zinsen im Jahr fällt keine Steuer an.")], "3 ehrliche Einschränkungen")


def draw_fazit(img, d, t, S):
    fazit(d, t, S, "Tilgen oder sparen?", [
        (1, RED, "Zuerst:", "Dispo und Ratenkredite – die teuersten Schulden"),
        (2, BLUE, "Baukredit:", "Sondertilgung schlägt im Schnitt Festgeld und Tagesgeld"),
        (3, AMBER, "Aber:", "immer erst einen Notgroschen behalten")])


def draw_outro(img, d, t, S):
    outro(d, t, S, ["Krankenkasse 2027:", "Wer jetzt mehr zahlt", "Zusatzbeitrag & Beitragsgrenze"])


def scenes():
    return [
        Scene("hook", [
            "Du hast zehntausend Euro übrig und einen Baukredit. Tilgen oder anlegen?",
            "Als Sondertilgung spart das Geld beim Durchschnittszins in zehn Jahren rund viertausendsiebenhundertfünfundsiebzig Euro Zinsen.",
            "Als Festgeld bringt es nach Steuern rund zweitausendzweihundertneunzig Euro.",
            "Wir rechnen nach, warum Tilgen oft mehr bringt als Sparen und wann nicht. Mit den Durchschnittszinsen der Bundesbank.",
        ], draw_hook),
        Scene("leiter", [
            "Die wichtigste Idee: Jeder zurückgezahlte Euro verdient genau den Zins, den er nicht mehr kostet.",
            "Ganz oben stehen der Dispo mit neun Komma fünf neun Prozent, Ratenkredite mit acht Komma neun eins und Baukredite mit drei Komma neun eins Prozent.",
            "Darunter das Sparen: Festgeld über zwei Jahre mit zwei Komma acht drei, Tagesgeld und Girokonto mit null Komma fünf zwei Prozent.",
            "Solange ein Kredit teurer ist als das, was das Ersparte bringt, lohnt sich Tilgen im Schnitt mehr.",
        ], draw_leiter),
        Scene("steuer", [
            "Dazu kommt ein Vorteil, den man leicht übersieht.",
            "Zinsen auf Erspartes über tausend Euro im Jahr werden mit sechsundzwanzig Komma vier Prozent besteuert.",
            "Aus zwei Komma acht drei Prozent Festgeld werden dann netto rund zwei Komma null acht.",
            "Gesparte Kreditzinsen werden dagegen nicht besteuert. Eine Tilgung beim Baukredit bringt also die vollen drei Komma neun eins Prozent, ohne Kursrisiko.",
        ], draw_steuer),
        Scene("beispiel", [
            "Rechnen wir zehntausend Euro über zehn Jahre, mit den heutigen Durchschnittszinsen.",
            "Als Sondertilgung beim Baukredit sinkt die Restschuld nach zehn Jahren um rund vierzehntausendsiebenhundertfünfundsiebzig Euro. Das sind rund viertausendsiebenhundertfünfundsiebzig Euro gesparte Zinsen.",
            "Als Festgeld bringt das Geld vor Steuern rund dreitausendzweihundertneunzehn Euro, nach Steuern rund zweitausendzweihundertneunzig.",
            "Auf Tagesgeld und Girokonto beim Durchschnittszins nur rund fünfhundertzweiunddreißig Euro.",
        ], draw_beispiel),
        Scene("aber", [
            "Aber drei Dinge solltest du vorher prüfen.",
            "Erstens: Behalte einen Notgroschen. Getilgtes Geld ist weg, und im Notfall gibt es dafür keinen günstigen Kredit.",
            "Zweitens: Beim Baukredit geht eine Sondertilgung während der Zinsbindung nur, wenn sie im Vertrag vereinbart ist.",
            "Drittens: Ratenkredite kann man jederzeit vorzeitig zurückzahlen. Die Bank darf dafür höchstens ein Prozent verlangen, bei weniger als einem Jahr Restlaufzeit ein halbes Prozent.",
        ], draw_aber),
        Scene("grenzen", [
            "Drei ehrliche Einschränkungen.",
            "Erstens: Das sind Durchschnittszinsen. Dein eigener Kredit- und Sparzins kann deutlich abweichen.",
            "Zweitens: Wir rechnen mit konstanten Zinsen über zehn Jahre. Das ist eine Vereinfachung.",
            "Drittens: Steuer fällt nur an, wenn deine Zinsen über tausend Euro im Jahr liegen.",
        ], draw_grenzen),
        Scene("fazit", [
            "Tilgen oder sparen?",
            "Zuerst kommen Dispo und Ratenkredite, das sind die teuersten Schulden.",
            "Beim Baukredit schlägt eine Sondertilgung im Schnitt Festgeld und Tagesgeld.",
            "Aber immer erst einen Notgroschen behalten.",
        ], draw_fazit),
        Scene("outro", [
            "Das hier ist keine Beratung, sondern Rechnen mit offiziellen Zahlen.",
            "Alle Werte, Formeln und Quellen findest du in der Beschreibung.",
            "Wenn du solche Rechnungen magst, dann abonnier den Kanal.",
            "Im nächsten Video: Krankenkasse zweitausendsiebenundzwanzig. Wer jetzt mehr zahlt, obwohl der Beitragssatz gleich bleibt.",
            "Bis dann.",
        ], draw_outro, extra=6.0),
    ]
