"""Wiederverwendbare Short-Formate (1080x1920, sicherer Bereich x 60–940, y 200–1470).

Formate: zahl() „Zahl der Woche“, mythos() „Mythos vs. Rechnung“, vergleich() „Was kostet X / A vs. B“.
Zeitangaben sind (Satzindex, Versatz in s) und werden gegen die Cues der Szene aufgelöst.
"""
from .gfx import AMBER, FG, GREEN, MUTED, RED, card, ease_in_out, fade, prog, rrect, text, text_pop

SIZE = (1080, 1920)
CX = 500


def _t(S, cue):
    i, off = cue if isinstance(cue, tuple) else (cue, 0.0)
    return S.c(i) + off


def pill(d, t, S, y, label, color, fill, cue):
    a = prog(t, _t(S, cue), 0.5)
    if a > 0:
        rrect(d, (110, y - 36, 890, y + 34), 35, fill=fade(fill, a), outline=fade(color, a * 0.7), width=2)
        text(d, (CX, y), label, 34, color, a, "mm", "Black")


def rows_card(d, t, S, y0, rows, accent=AMBER, head=None, head_cue=0, row_h=82):
    """rows: [(cue, label, value, color)] – a card with label/value lines."""
    a = prog(t, _t(S, rows[0][0] if not head else head_cue), 0.5)
    if a <= 0:
        return y0
    h = (70 if head else 20) + len(rows) * row_h + 20
    card(d, (110, y0, 890, y0 + h), a, accent)
    y = y0 + 20
    if head:
        text(d, (150, y + 40), head, 40, FG, a, "lm", "Bold")
        y += 70
    for cue, lab, val, col in rows:
        b = prog(t, _t(S, cue), 0.5)
        text(d, (150, y + row_h / 2), lab, 34, MUTED, b, "lm", "SemiBold")
        text(d, (850, y + row_h / 2), val, 46, col, b, "rm", "Black")
        y += row_h
    return y0 + h


def outro(d, t, S, cta_cue, cta, src, src_cue=1):
    text(d, (CX, 1420), cta, 36, AMBER, prog(t, _t(S, cta_cue), 0.5), "mm", "Bold")
    text(d, (CX, 1465), src, 22, MUTED, prog(t, _t(S, src_cue), 0.5), "mm", "Medium")


def conclusion(d, t, S, y, lines, cue, color=AMBER):
    for i, (s, col) in enumerate(lines):
        text(d, (CX, y + i * 70), s, 46, col or color, prog(t, _t(S, cue) + i * 0.3, 0.5), "mm", "Black")


def zahl(big, big_sub, context, rows, concl, cta, src, *, big_color=AMBER, rows_head=None, kicker="ZAHL DER WOCHE"):
    """Format „Zahl der Woche“. concl: (cue, [(text, color)])."""
    def draw(img, d, t, S):
        text_pop(d, (CX, 230), kicker, t, S.c(0), 36, AMBER, "mm", "Black", rise=10)
        text_pop(d, (CX, 380), big, t, S.c(0) + 0.3, 140 if len(big) <= 9 else 104, big_color, "mm", "Black")
        text_pop(d, (CX, 490), big_sub, t, S.c(0) + 0.6, 42, FG, "mm", "Bold")
        text(d, (CX, 560), context, 28, MUTED, prog(t, S.c(1), 0.5), "mm", "Medium")
        y = rows_card(d, t, S, 620, rows, head=rows_head, head_cue=rows[0][0]) if rows else 620
        if concl:
            conclusion(d, t, S, max(y + 90, 1130), concl[1], concl[0])
        outro(d, t, S, cta[0], cta[1], src)
    return draw


def mythos(myth, rows, verdict, cta, src, *, rows_head=None):
    """Format „Mythos vs. Rechnung“. myth: [line1, line2]; verdict: (cue, [(text, color)])."""
    def draw(img, d, t, S):
        pill(d, t, S, 236, "MYTHOS", RED, (50, 26, 30), 0)
        for i, s in enumerate(myth):
            text_pop(d, (CX, 340 + i * 75), s, t, S.c(0) + 0.2 + i * 0.2, 58 if len(s) < 26 else 46, FG, "mm", "Black")
        pill(d, t, S, 536, "RECHNUNG", GREEN, (24, 48, 40), 1)
        y = rows_card(d, t, S, 620, rows, head=rows_head, head_cue=rows[0][0])
        conclusion(d, t, S, max(y + 90, 1150), verdict[1], verdict[0])
        outro(d, t, S, cta[0], cta[1], src)
    return draw


def vergleich(title, sub, cards, concl, cta, src):
    """Format „A vs. B“. cards: [(cue, header, color, [(label, value, value_color)])]."""
    def draw(img, d, t, S):
        text_pop(d, (CX, 250), title, t, S.c(0), 66 if len(title) < 22 else 52, FG, "mm", "Black")
        text_pop(d, (CX, 325), sub, t, S.c(0) + 0.3, 32, MUTED, "mm", "SemiBold")
        for k, (cue, head, col, lines) in enumerate(cards):
            a = prog(t, _t(S, cue), 0.5)
            if a <= 0:
                continue
            x0 = 110 + k * 400
            card(d, (x0, 400, x0 + 380, 980), a, col)
            cx = x0 + 190
            text(d, (cx, 465), head, 42, FG, a, "mm", "Black")
            for j, (lab, val, vcol) in enumerate(lines):
                y = 560 + j * 135
                text(d, (cx, y), lab, 28, MUTED, a, "mm", "SemiBold")
                text(d, (cx, y + 55), val, 50, vcol, a, "mm", "Black")
        conclusion(d, t, S, 1090, concl[1], concl[0])
        outro(d, t, S, cta[0], cta[1], src)
    return draw
