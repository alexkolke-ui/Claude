"""Gemeinsame Bausteine für Langvideos (1920x1080): Titel, Fußzeile, Kartenlisten, Einschränkungen, Fazit, Outro."""
from .gfx import AMBER, FG, MUTED, W, card, dot, ease_in_out, fade, prog, rrect, text, text_pop


def title(d, t, s, start=0.0, sub=None):
    text_pop(d, (250, 120), s, t, start, 50, FG, "ls", "Bold", rise=20)
    if sub:
        text_pop(d, (250, 165), sub, t, start + 0.15, 28, MUTED, "ls", "Medium", rise=10)


def footer(d, alpha, s):
    text(d, (1860, 1040), s, 22, (90, 102, 128), alpha, "rs", "Medium")


def cards(d, t, rows, y0=240, h=150, gap=20, x0=250, x1=1670):
    """rows: [(start, head, line, color)] – Karten untereinander."""
    for i, (st, head, line, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = y0 + i * (h + gap)
        card(d, (x0, y, x1, y + h), a, col)
        text(d, (x0 + 40, y + h * 0.36), head, 38, FG, a, "lm", "Bold")
        text(d, (x0 + 40, y + h * 0.72), line, 28, MUTED, a, "lm", "Medium")


def numbered(d, t, S, items, heading):
    """Einschränkungen: items = [(cue_index, head, line)]."""
    title(d, t, heading, S.c(0))
    n = len(items)
    h, gap = (180, 30) if n <= 3 else (155, 20)
    for i, (ci, head, line) in enumerate(items):
        a = prog(t, S.c(ci), 0.5)
        if a <= 0:
            continue
        y = 230 + i * (h + gap)
        card(d, (250, y, 1670, y + h), a)
        dot(d, (320, y + h / 2), 37, fade(AMBER, a))
        text(d, (320, y + h / 2 + 2), str(i + 1), 39, (13, 19, 33), a, "mm", "Black")
        text(d, (400, y + h * 0.33), head, 39, FG, a, "lm", "Bold")
        text(d, (400, y + h * 0.68), line, 28, MUTED, a, "lm", "Medium")


def fazit(d, t, S, heading, rows):
    """rows: [(cue_index, color, label, text)]."""
    text_pop(d, (W / 2, 170), heading, t, S.c(0), 56, FG, "mm", "Black")
    for i, (ci, col, a_txt, b_txt) in enumerate(rows):
        a = prog(t, S.c(ci), 0.5)
        if a <= 0:
            continue
        y = 280 + i * 170
        card(d, (300, y, 1620, y + 140), a, col)
        text(d, (340, y + 50), a_txt, 32, MUTED, a, "lm", "SemiBold")
        text(d, (340, y + 100), b_txt, 40, FG, a, "lm", "Bold")


def outro(d, t, S, next_lines=None, sub="Werte, Annahmen & Quellen stehen in der Beschreibung."):
    text_pop(d, (W / 2, 260), "Keine Beratung – sondern offizielle Zahlen, nachgerechnet.", t, S.c(0), 52, FG, "mm", "Bold")
    text_pop(d, (W / 2, 335), sub, t, S.c(1), 32, MUTED, "mm", "Medium")
    a = prog(t, S.c(2), 0.5)
    x = 630 if next_lines else 960
    if a > 0:
        rrect(d, (x - 270, 470, x + 270, 570), 50, fill=fade((204, 0, 0), a))
        text(d, (x, 521), "ABONNIEREN", 44, (255, 255, 255), a, "mm", "Black")
        text(d, (x, 620), "Rechenweg", 36, FG, a, "mm", "Bold")
        text(d, (x, 665), "jeden Donnerstag ein neues Video", 26, MUTED, a, "mm", "Medium")
    if next_lines:
        a = prog(t, S.c(3), 0.5)
        if a > 0:
            card(d, (1020, 450, 1600, 780), a, AMBER)
            text(d, (1060, 510), "NÄCHSTES VIDEO", 24, AMBER, a, "lm", "Bold")
            for i, s in enumerate(next_lines[:2]):
                text(d, (1060, 580 + i * 50), s, 40, FG, a, "lm", "Bold")
            if len(next_lines) > 2:
                text(d, (1060, 720), next_lines[2], 26, MUTED, a, "lm", "Medium")


def hook_two(d, t, S, heading, left, right, banner, src):
    """Zwei große Karten + Banner. left/right: (cue, label, value, sub, color)."""
    text_pop(d, (W / 2, 160), heading, t, S.c(0), 56, FG, "mm", "Black")
    for i, (ci, lab, v, sub, col) in enumerate((left, right)):
        a = prog(t, S.c(ci), 0.6)
        if a <= 0:
            continue
        x0 = 300 + i * 720
        card(d, (x0, 270, x0 + 600, 590), a, col)
        text(d, (x0 + 300, 330), lab, 36, MUTED, a, "mm", "SemiBold")
        text(d, (x0 + 300, 440), v, 84 if len(v) <= 9 else 66, col, a, "mm", "Black")
        text(d, (x0 + 300, 530), sub, 30, FG, a, "mm", "Medium")
    ci, s = banner
    a = prog(t, S.c(ci), 0.6)
    if a > 0:
        rrect(d, (300, 680, 1620, 790), 20, fill=fade((44, 38, 20), a), outline=fade(AMBER, a * 0.6), width=2)
        text(d, (W / 2, 735), s, 38, AMBER, a, "mm", "Black")
    footer(d, prog(t, S.c(1), 0.6), src)


def table(d, t, rows, cols, y0=300, row_h=110, x0=250, x1=1670):
    """Tabelle: cols = [(x, header, anchor)], rows = [(start, [cells], color)] – Zellen als (text, color)."""
    a0 = prog(t, rows[0][0], 0.5)
    for x, hd, anc in cols:
        text(d, (x, y0 - 30), hd, 28, MUTED, a0, anc, "SemiBold")
    for i, (st, cells, col) in enumerate(rows):
        a = prog(t, st, 0.5)
        if a <= 0:
            continue
        y = y0 + i * row_h
        card(d, (x0, y, x1, y + row_h - 15), a, col)
        for (x, _, anc), (s, c) in zip(cols, cells):
            text(d, (x, y + (row_h - 15) / 2), s, 40 if anc == "lm" else 38, c, a, anc, "Black" if anc != "mm" else "Bold")
