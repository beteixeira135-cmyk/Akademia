"""
Conjuntos de parâmetros r3PG (82) por material genético, com origem de cada valor.

A1  = Eucalyptus urophylla, clone A1 — Caldeira et al. (2020), Tabela 1 e §2.7 (conferido no PDF).
C1..C5 = híbridos E. grandis × E. urophylla — Borges (2009, dissertação UFV), Tabela 9, pp. 43–44
         (conferida no PDF; idêntica às colunas 'Eucalyptus grandis x urophylla2..6' do 3PGmix.Data.xls).
         C1 = clone 3334 Curvelo; C2 = 3336 Curvelo; C3 = 3334 Itacambira; C4 = 3336 Itacambira;
         C5 = modelo geral para o Cerrado (dados de 3334/3336 Itacambira + 3336 Curvelo).

Lacunas (parâmetros ausentes nas duas fontes) são preenchidas com o MESMO critério para todos os
materiais: coluna E. globulus do 3PGmix.Data.xls (= padrão Sands & Landsberg 2002), ou valor neutro.
Nenhum valor de um clone foi usado em outro.

Exceções documentadas:
 * Volume: Borges (Tab. 4) ajusta V em m3/ha diretamente de dap; a fórmula do r3PG (aV·dap^nVB·N) é
   por árvore -> incompatível. Para todos os materiais o volume usa o caminho de biomassa (aV = 0):
   V = Ws·(1 − fracBB)/ρ.
 * Altura: Caldeira não publica alometria de altura (aH = 0 -> altura indisponível); Borges publica
   H = aH·dap^nHB (Tab. 4/9), usada com nHC = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cenarios"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modelo"))
from parametros_caldeira_r3pg import P as P_CALDEIRA  # noqa: E402
from threepg_pjs import PAR_FORTRAN  # noqa: E402

# ---------- Borges (2009), Tabela 9 — transcrição conferida na imagem das páginas 43–44 ----------
B9 = {  #            C1      C2      C3      C4      C5
    "WF0":       (0.110, 0.170, 0.162, 0.170, 0.168),
    "WS0":       (0.064, 0.116, 0.075, 0.116, 0.106),
    "WR0":       (0.080, 0.100, 0.093, 0.100, 0.099),
    "pFS2":      (0.95, 1.72, 1.00, 1.00, 1.64),
    "pFS20":     (0.10, 0.11, 0.17, 0.17, 0.15),
    "aWs":       (0.007, 0.011, 0.013, 0.043, 0.020),
    "nWs":       (3.60, 3.35, 3.27, 2.82, 3.11),
    "pRx":       (0.5,) * 5, "pRn": (0.1,) * 5,
    "gammaF1":   (0.07,) * 5, "gammaF0": (0.001,) * 5, "tgammaF": (4.0,) * 5,
    "gammaR":    (0.025,) * 5,
    "Tmin":      (8.0,) * 5, "Topt": (25.0,) * 5, "Tmax": (40.0,) * 5,
    "m0":        (0.0,) * 5, "fN0": (0.5,) * 5, "fNn": (1.0,) * 5,
    "FR":        (0.9,) * 5,
    "MaxAge":    (9.0,) * 5, "nAge": (4.0,) * 5, "rAge": (0.95,) * 5,
    "SLA0":      (15.17, 12.69, 14.09, 14.43, 13.74),
    "SLA1":      (6.11, 8.60, 6.60, 7.48, 7.56),
    "tSLA":      (1.13, 0.73, 1.49, 1.42, 1.23),
    "k":         (0.5,) * 5, "fullCanAge": (2.0,) * 5,
    "MaxIntcptn": (0.15,) * 5, "LAImaxIntcptn": (3.33,) * 5,
    "alphaCx":   (0.09, 0.08, 0.08, 0.08, 0.08),
    "y":         (0.5,) * 5,
    "MaxCond":   (0.01, 0.02, 0.02, 0.02, 0.02),
    "LAIgcx":    (3.33,) * 5, "CoeffCond": (0.0324,) * 5, "BLcond": (0.2,) * 5,
    "wSx1000":   (300.0,) * 5,
    "fracBB0":   (0.54, 0.60, 0.53, 0.62, 0.59),
    "fracBB1":   (0.14, 0.14, 0.23, 0.15, 0.19),
    "tBB":       (2.19, 1.68, 2.85, 2.47, 2.17),
    "rho0":      (0.430, 0.409, 0.391, 0.345, 0.382),
    "rho1":      (0.580, 0.473, 0.539, 0.502, 0.505),
    "tRho":      (3.892, 2.917, 2.202, 2.175, 2.264),
    "aH":        (0.62, 0.50, 0.56, 0.57, 0.67),
    "nHB":       (1.36, 1.42, 1.34, 1.31, 1.27),
}

# lacunas: mesmo critério aplicado a Caldeira (coluna E. globulus / neutro / processo desligado)
LACUNAS = {
    "leafgrow": (0, "ESTRUTURAL: perenifólia"), "leaffall": (0, "ESTRUTURAL: perenifólia"),
    "kF": (0.0, "ADAPTADO E. globulus (ausente na fonte)"),
    "SWconst0": (0.4, "soil_class=4 (classe C, muito argiloso, Borges Tab.9) -> 0,4"),
    "SWpower0": (3.0, "soil_class=4 -> 3"),
    "fCalpha700": (1.4, "NEUTRO com CO2=350"), "fCg700": (0.7, "NEUTRO com CO2=350"),
    "gammaN1": (0.0, "AUSENTE_ZERO"), "gammaN0": (0.0, "AUSENTE_ZERO"), "tgammaN": (0.0, "AUSENTE_ZERO"),
    "ngammaN": (1.0, "AUSENTE_ZERO"),
    "thinPower": (1.5, "ADAPTADO E. globulus"), "mF": (0.0, "ADAPTADO E. globulus"),
    "mR": (0.2, "ADAPTADO E. globulus"), "mS": (0.2, "ADAPTADO E. globulus"),
    "cVPD": (5.0, "NEUTRO: só 3-PGmix"), "MinCond": (0.0, "ADAPTADO E. globulus"),
    "RGcGW": (0.66, "NEUTRO d13C"), "D13CTissueDif": (2.0, "NEUTRO d13C"), "aFracDiffu": (4.4, "NEUTRO d13C"),
    "bFracRubi": (27.0, "NEUTRO d13C"), "CrownShape": (3, "NEUTRO 3-PGmix"),
    "nHC": (0.0, "Borges Tab.4: H = aH·dap^nHB (sem termo de competição)"),
    "aV": (0.0, "ESTRUTURAL: volume por biomassa (ver docstring)"), "nVB": (0.0, "idem"), "nVH": (0.0, "idem"),
    "nVBH": (0.0, "idem"),
    "aK": (0.0, "NEUTRO"), "nKB": (0.0, "NEUTRO"), "nKH": (0.0, "NEUTRO"), "nKC": (0.0, "NEUTRO"),
    "nKrh": (0.0, "NEUTRO"), "aHL": (0.0, "NEUTRO"), "nHLB": (0.0, "NEUTRO"), "nHLL": (0.0, "NEUTRO"),
    "nHLC": (0.0, "NEUTRO"), "nHLrh": (0.0, "NEUTRO"),
    "Qa": (-90.0, "ADAPTADO E. globulus"), "Qb": (0.8, "ADAPTADO E. globulus"),
    "gDM_mol": (24.0, "ADAPTADO"), "molPAR_MJ": (2.3, "ADAPTADO"),
}


def _borges(i):
    P = {}
    for k_, v in B9.items():
        if k_ in ("WF0", "WS0", "WR0", "FR"):
            continue
        P[k_] = (float(v[i]), f"FONTE Borges 2009 Tab.9 (C{i+1})")
    for k_, v in LACUNAS.items():
        P.setdefault(k_, v)
    assert set(P) == set(PAR_FORTRAN), set(PAR_FORTRAN) ^ set(P)
    return P


MATERIAIS = {
    "A1": dict(nome="E. urophylla clone A1 (Caldeira et al. 2020)", P=P_CALDEIRA,
               idade_inicial_meses=12, WF0=2.07, WS0=5.47, WR0=1.09, FR_ref=0.8,
               regiao="multissítio Brasil (TECHS); calibrado/validado até 80 meses"),
}
for i, rot in enumerate(["C1", "C2", "C3", "C4", "C5"]):
    desc = ["clone 3334, Curvelo-MG", "clone 3336, Curvelo-MG", "clone 3334, Itacambira-MG",
            "clone 3336, Itacambira-MG", "modelo geral Cerrado-MG"][i]
    MATERIAIS[rot] = dict(nome=f"E. grandis × E. urophylla {desc} (Borges 2009)", P=_borges(i),
                          idade_inicial_meses=3, WF0=B9["WF0"][i], WS0=B9["WS0"][i], WR0=B9["WR0"][i],
                          FR_ref=B9["FR"][i], regiao=desc)


def params(material):
    return {k_: float(v[0]) for k_, v in MATERIAIS[material]["P"].items()}


def origem(material):
    return {k_: v[1] for k_, v in MATERIAIS[material]["P"].items()}
