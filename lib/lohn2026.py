"""Brutto-Netto 2026 nach dem offiziellen Programmablaufplan (PAP) des BMF „Lohnsteuer2026“.

Übersetzt ist nur der Pfad, den die Videos brauchen: laufender Arbeitslohn, Steuerklasse I oder III,
keine Versorgungsbezüge/Freibeträge/Kinderfreibeträge, gesetzlich kranken- und pflegeversichert,
rentenversicherungspflichtig, ohne Kirchensteuer. Rundungen wie im PAP (Decimal, ROUND_DOWN/UP).
Quelle PAP: https://www.bmf-steuerrechner.de (javax.faces.resource/daten/xmls/Lohnsteuer2026.xml)

Sozialversicherung 2026 (Arbeitnehmeranteile): RV 9,3 %, AV 1,3 %, KV 7,3 % + halber Zusatzbeitrag,
PV 1,8 % (+0,6 % kinderlos ab 23); BBG KV/PV 69.750 €/Jahr, RV/AV 101.400 €/Jahr.
"""
from decimal import ROUND_DOWN, ROUND_UP, Decimal as D

GFB = D(12348)
SOLZFREI = D(20350)
BBGRVALV, BBGKVPV = D(101400), D(69750)
RVSATZAN, AVSATZAN = D("0.093"), D("0.013")
KVZ_AVG = D("2.9")                     # durchschnittlicher Zusatzbeitrag 2026 in %


def _down(x, n=0):
    return x.quantize(D(1).scaleb(-n), rounding=ROUND_DOWN)


def _up(x, n=0):
    return x.quantize(D(1).scaleb(-n), rounding=ROUND_UP)


def uptab26(x):
    """Einkommensteuer-Grundtarif 2026 (§ 32a EStG) für zu versteuerndes Einkommen x (volle Euro)."""
    x = D(x)
    if x < GFB + 1:
        return D(0)
    if x < 17800:
        y = _down((x - GFB) / 10000, 6)
        return _down((y * D("914.51") + 1400) * y)
    if x < 69879:
        y = _down((x - 17799) / 10000, 6)
        return _down((y * D("173.1") + 2397) * y + D("1034.87"))
    if x < 277826:
        return _down(x * D("0.42") - D("11135.63"))
    return _down(x * D("0.45") - D("19470.38"))


def lohnsteuer_jahr(jahreslohn, stkl=1, kvz=KVZ_AVG, kinderlos=True):
    """Jahreslohnsteuer und Solidaritätszuschlag (Euro) für einen Jahresarbeitslohn."""
    zre4 = _down(D(jahreslohn), 2)
    anp = D(1230) if zre4 >= 1230 else _up(zre4)
    ztabfb = _down(anp + D(36), 2)
    # Vorsorgepauschale (UPEVP / MVSPKVPV / MVSPHB)
    vspr = _down(min(zre4, BBGRVALV) * RVSATZAN, 2)
    kvsatzan = D(kvz) / 2 / 100 + D("0.07")
    pvsatzan = D("0.018") + (D("0.006") if kinderlos else 0)
    vspkvpv = _down(min(zre4, BBGKVPV) * (kvsatzan + pvsatzan), 2)
    vsp = _up(vspkvpv + vspr)
    vsphb = min(_down(_down(AVSATZAN * min(zre4, BBGRVALV), 2) + vspkvpv, 2), D(1900))
    vsp = max(vsp, _up(vspr + vsphb))
    zve = zre4 - ztabfb - vsp
    kztab = 2 if stkl == 3 else 1
    x = D(0) if zve < 1 else _down(zve / kztab)
    lst = uptab26(x) * kztab
    # Solidaritätszuschlag (MSOLZ), Freigrenze 20.350 € (×2 bei Steuerklasse III)
    frei = SOLZFREI * kztab
    soli = D(0)
    if lst > frei:
        soli = min(_down(lst * D("5.5") / 100, 2), _down((lst - frei) * D("11.9") / 100, 2))
    return lst, soli


def sv_jahr(jahreslohn, kvz=KVZ_AVG, kinderlos=True):
    """Arbeitnehmeranteile Sozialversicherung pro Jahr: dict RV, AV, KV, PV."""
    b = D(jahreslohn)
    kv = min(b, BBGKVPV)
    rv = min(b, BBGRVALV)
    return {"RV": rv * RVSATZAN, "AV": rv * AVSATZAN,
            "KV": kv * (D("0.073") + D(kvz) / 200),
            "PV": kv * (D("0.018") + (D("0.006") if kinderlos else 0))}


def netto_monat(brutto, stkl=1, kvz=KVZ_AVG, kinderlos=True):
    """Monatliche Aufteilung bei gleichbleibendem Monatslohn (12 Gehälter): dict in Euro (float)."""
    lst, soli = lohnsteuer_jahr(D(brutto) * 12, stkl, kvz, kinderlos)
    m = {"LSt": _down(lst * 100 / 12) / 100, "Soli": _down(soli * 100 / 12) / 100}
    m.update({k: v / 12 for k, v in sv_jahr(D(brutto) * 12, kvz, kinderlos).items()})
    m = {k: float(_down(D(v), 2)) for k, v in m.items()}
    m["Brutto"] = float(brutto)
    m["Netto"] = round(float(brutto) - sum(v for k, v in m.items() if k not in ("Brutto",)), 2)
    return m


def sonderzahlung(monatslohn, betrag, stkl=1, kvz=KVZ_AVG, kinderlos=True):
    """Netto einer Einmalzahlung (z. B. Weihnachtsgeld): Mehrsteuer + Mehr-SV gegenüber Jahr ohne Zahlung.

    Vereinfachung des PAP-Teils MSONST: Jahreslohn mit vs. ohne Sonderzahlung (Differenzmethode);
    SV auf die Einmalzahlung nur bis zur anteiligen Jahres-BBG.
    """
    jl = D(monatslohn) * 12
    l0, s0 = lohnsteuer_jahr(jl, stkl, kvz, kinderlos)
    l1, s1 = lohnsteuer_jahr(jl + D(betrag), stkl, kvz, kinderlos)
    sv0, sv1 = sv_jahr(jl, kvz, kinderlos), sv_jahr(jl + D(betrag), kvz, kinderlos)
    d = {"LSt": float(l1 - l0), "Soli": float(s1 - s0)}
    d.update({k: float(sv1[k] - sv0[k]) for k in sv0})
    d = {k: round(v, 2) for k, v in d.items()}
    d["Brutto"] = float(betrag)
    d["Netto"] = round(float(betrag) - sum(v for k, v in d.items() if k != "Brutto"), 2)
    return d


# Selbsttest: Beispielwert des Grundtarifs 2026 (zvE 30.000 € → 4.217 € ESt)
assert uptab26(30000) == 4217 and uptab26(12348) == 0 and uptab26(12349) == 0
