"""
Mapeia a planilha 3PG_CALDEIRA_INDIANOPOLIS_PLANTIO_JAN2015.xlsx (aba 01_PARAMETROS) para os
82 parâmetros do r3PG, sem acrescentar valores novos. Cada linha registra a célula de origem.

Parâmetros que o r3PG exige mas que a planilha marca como MISSING recebem um valor que
DESLIGA o processo correspondente, com efeito numérico demonstrável:
  * CO2: co2 = 350 ppm  =>  f_calpha = f_cg = 1 para quaisquer fCalpha700/fCg700
    (fCg700 ≠ 0,5 para evitar divisão por zero; valores usados = padrões do r3PG, inertes).
  * gammaN0 = gammaN1 = 0, tgammaN = 0 => mortalidade independente da densidade desligada
    (mesma decisão da planilha: "não aplicada").
  * Altura e alometrias de copa/volume (aH, nHB, nHC, aV..., aK..., aHL...) = 0 => altura sai 0
    (planilha: MISSING) e volume = WS·(1−pBB)/ρ (mesma fórmula da planilha, Eq.30 de Silva).
  * Solo: soil_class = 4 => SWconst = 0,8−0,1·4 = 0,4 e SWpower = 11−2·4 = 3, idênticos a
    cθ = 0,4 e nθ = 3 da planilha (classe C, 3PGmix). SWconst0/SWpower0 ficam inertes.
  * d13C e 3-PGmix: parâmetros inertes no 3-PGpjs (padrões do r3PG).
"""
from pathlib import Path
import openpyxl
import pandas as pd
from threepg_pjs import PAR_FORTRAN

# r3PG -> (célula em 01_PARAMETROS ou constante, origem/observação)
MAPA = {
    "pFS2": ("C86", "Caldeira T1"), "pFS20": ("C87", "Caldeira T1"),
    "aWs": ("C90", "Caldeira §2.7.2 (0,0249)"), "nWs": ("C91", "Caldeira §2.7.2 (3,021)"),
    "pRx": ("C84", "Caldeira T1"), "pRn": ("C85", "Caldeira T1"),
    "gammaF1": ("C80", "Caldeira T1"), "gammaF0": ("C81", "Caldeira T1"), "tgammaF": ("C82", "Caldeira T1 (meses)"),
    "gammaR": ("C83", "Caldeira T1 (L3)"),
    "leafgrow": (0.0, "perenifólio"), "leaffall": (0.0, "perenifólio"),
    "Tmin": ("C62", "Caldeira T1"), "Topt": ("C63", "Caldeira T1"), "Tmax": ("C64", "Caldeira T1"),
    "kF": ("C65", "3PGmix E. globulus (ADAPTADO)"),
    "SWconst0": (0.7, "INERTE (soil_class>0)"), "SWpower0": (9.0, "INERTE (soil_class>0)"),
    "fCalpha700": (1.4, "INERTE com co2=350"), "fCg700": (0.7, "INERTE com co2=350"),
    "m0": ("C66", "Caldeira T1 sk1m"), "fN0": ("C67", "Caldeira T1 sk2m"), "fNn": ("C68", "3PGmix (ADAPTADO)"),
    "MaxAge": ("C69", "3PGmix (ADAPTADO)"), "nAge": ("C70", "3PGmix (ADAPTADO)"), "rAge": ("C71", "3PGmix (ADAPTADO)"),
    "gammaN1": (0.0, "DESLIGADO (MISSING)"), "gammaN0": (0.0, "DESLIGADO (MISSING)"),
    "tgammaN": (0.0, "DESLIGADO (MISSING)"), "ngammaN": (1.0, "INERTE"),
    "wSx1000": ("C92", "Caldeira T1"), "thinPower": ("C93", "3PGmix (ADAPTADO)"),
    "mF": ("C94", "3PGmix (ADAPTADO)"), "mR": ("C95", "3PGmix (ADAPTADO)"), "mS": ("C96", "3PGmix (ADAPTADO)"),
    "SLA0": ("C72", "Caldeira T1"), "SLA1": ("C73", "Caldeira T1"), "tSLA": ("C74", "Caldeira T1 (L4)"),
    "k": ("C75", "Caldeira T1 (L3)"), "fullCanAge": ("C76", "Caldeira T1 (L3)"),
    "MaxIntcptn": ("C77", "Caldeira T1 cpir (L1)"), "LAImaxIntcptn": ("C78", "3PGmix (ADAPTADO)"),
    "cVPD": (5.0, "INERTE (3-PGmix)"), "alphaCx": ("C59", "Caldeira T1 (L2)"), "y": ("C60", "Caldeira T1"),
    "MinCond": ("C97", "ADAPTADO (0)"), "MaxCond": ("C98", "Caldeira T1"), "LAIgcx": ("C100", "3PGmix (ADAPTADO)"),
    "CoeffCond": ("C102", "Caldeira 0,5 kPa⁻¹ → 0,05 mbar⁻¹"), "BLcond": ("C103", "Caldeira T1 (L3)"),
    "RGcGW": (0.66, "INERTE (d13C)"), "D13CTissueDif": (2.0, "INERTE"), "aFracDiffu": (4.4, "INERTE"),
    "bFracRubi": (27.0, "INERTE"),
    "fracBB0": ("C115", "Caldeira T1"), "fracBB1": ("C116", "Caldeira T1 (0,15)"), "tBB": ("C117", "Caldeira T1"),
    "rho0": ("C61", "Caldeira 440 kg m⁻³"), "rho1": ("C61", "Caldeira 440 kg m⁻³"), "tRho": (4.0, "INERTE (rho0=rho1)"),
    "CrownShape": (3.0, "INERTE"),
    **{p: (0.0, "MISSING → 0 (altura/volume/copa não usados na dinâmica 3-PGpjs)") for p in
       ["aH", "nHB", "nHC", "aV", "nVB", "nVH", "nVBH", "aK", "nKB", "nKH", "nKC", "nKrh",
        "aHL", "nHLB", "nHLL", "nHLC", "nHLrh"]},
    "Qa": ("C104", "3PGmix (ADAPTADO)"), "Qb": ("C105", "3PGmix (ADAPTADO)"),
    "gDM_mol": ("C107", "3PGmix (ADAPTADO)"), "molPAR_MJ": ("C106", "3PGmix (ADAPTADO)"),
}
assert set(MAPA) == set(PAR_FORTRAN)


def ler_planilha(path):
    """Lê parâmetros, entradas do talhão e clima (aba 02_CLIMA) de uma cópia RECALCULADA."""
    wb = openpyxl.load_workbook(path, data_only=True)
    p = wb["01_PARAMETROS"]
    val = lambda ref: p[ref].value
    pars, prov = {}, []
    for nome in PAR_FORTRAN:
        ref, origem = MAPA[nome]
        v = val(ref) if isinstance(ref, str) else ref
        if v is None:
            raise ValueError(f"{nome}: célula {ref} vazia — não será preenchida")
        pars[nome] = float(v)
        prov.append(dict(parametro_r3pg=nome, valor=float(v), celula=ref if isinstance(ref, str) else "constante",
                         origem=origem))
    entradas = dict(N0=val("C30"), WF0=val("C33"), WS0=val("C34"), WR0=val("C35"), ASWmin=val("C37"),
                    ASWmax=val("C40"), ASW0=val("C41"), FR=val("C46"), FR_mode=val("C45"),
                    soil_code=val("C42"), plantio=val("C27"), idade0_meses=val("C32"), n_meses=val("C31"),
                    VPDmode=val("C54"))
    c = wb["02_CLIMA"]
    linhas = []
    for r in range(5, c.max_row + 1):
        if c.cell(r, 2).value is None:
            continue
        linhas.append(dict(year=int(c.cell(r, 2).value), month=int(c.cell(r, 3).value),
                           tmp_max=float(c.cell(r, 5).value), tmp_min=float(c.cell(r, 6).value),
                           tmp_ave=float(c.cell(r, 7).value), prcp=float(c.cell(r, 9).value),
                           srad=float(c.cell(r, 10).value), vpd_day=float(c.cell(r, 19).value),
                           frost_days=float(c.cell(r, 20).value)))
    clima = pd.DataFrame(linhas)
    clima["co2"] = 350.0
    return pars, pd.DataFrame(prov), entradas, clima
