"""Parâmetros r3PG (82) montados a partir da planilha 3PG_CALDEIRA_INDIANOPOLIS_PLANTIO_JAN2015.xlsx
(aba 01_PARAMETROS), com a origem de cada valor. Nenhum valor novo foi criado aqui.
Classes: FONTE = Caldeira et al. 2020 (Tabela 1/texto, conferido no PDF);
ADAPTADO = coluna E. globulus do 3PGmix.Data.xls (conferido);
NEUTRO = valor sem efeito na configuração usada (documentado ao lado);
AUSENTE_ZERO = parâmetro MISSING cujo processo NÃO é aplicado (0 desliga o processo, igual à planilha)."""
P = {
 "pFS2": (0.50, "FONTE Tab.1"), "pFS20": (0.15, "FONTE Tab.1"),
 "aWs": (0.0249, "FONTE §2.7.2 texto (Tab.1 arredonda 0,025)"), "nWs": (3.021, "FONTE §2.7.2 texto (Tab.1: 3,02)"),
 "pRx": (0.23, "FONTE Tab.1"), "pRn": (0.06, "FONTE Tab.1"),
 "gammaF1": (0.13, "FONTE Tab.1"), "gammaF0": (0.06, "FONTE Tab.1 (texto: 0,062)"), "tgammaF": (4.0, "FONTE Tab.1 (meses)"),
 "gammaR": (0.015, "FONTE Tab.1 (L3)"), "leafgrow": (0, "ESTRUTURAL: perenifólia"), "leaffall": (0, "ESTRUTURAL: perenifólia"),
 "Tmin": (7.25, "FONTE Tab.1"), "Topt": (23.95, "FONTE Tab.1"), "Tmax": (28.65, "FONTE Tab.1"),
 "kF": (0.0, "ADAPTADO E. globulus; sem geada na série (Tmin>=4,3 °C)"),
 "SWconst0": (0.4, "ADAPTADO 3PGmix classe C (= soil_class 4 do r3PG)"), "SWpower0": (3.0, "ADAPTADO 3PGmix classe C"),
 "fCalpha700": (1.4, "NEUTRO: com CO2=350 ppm constante f_calpha=1 para qualquer valor"),
 "fCg700": (0.7, "NEUTRO: com CO2=350 ppm constante f_cg=1 para qualquer valor"),
 "m0": (0.0, "FONTE Tab.1 sk1m"), "fN0": (1.0, "FONTE Tab.1 sk2m"), "fNn": (0.0, "ADAPTADO E. globulus; irrelevante com fN0=1"),
 "MaxAge": (50.0, "ADAPTADO E. globulus (Borges 2009 no mesmo arquivo: 9)"), "nAge": (4.0, "ADAPTADO E. globulus"),
 "rAge": (0.95, "ADAPTADO E. globulus"),
 "gammaN1": (0.0, "AUSENTE_ZERO: mortalidade independente da densidade não aplicada"),
 "gammaN0": (0.0, "AUSENTE_ZERO"), "tgammaN": (0.0, "AUSENTE_ZERO"), "ngammaN": (1.0, "AUSENTE_ZERO"),
 "wSx1000": (300.0, "FONTE Tab.1"), "thinPower": (1.5, "ADAPTADO E. globulus"),
 "mF": (0.0, "ADAPTADO E. globulus"), "mR": (0.2, "ADAPTADO E. globulus"), "mS": (0.2, "ADAPTADO E. globulus"),
 "SLA0": (9.4, "FONTE Tab.1"), "SLA1": (8.4, "FONTE Tab.1"), "tSLA": (2.0, "FONTE Tab.1 (L4)"),
 "k": (0.5, "FONTE Tab.1 (L3)"), "fullCanAge": (0.0, "FONTE Tab.1 tfullCan"),
 "MaxIntcptn": (0.26, "FONTE Tab.1 cpir (L1)"), "LAImaxIntcptn": (0.0, "ADAPTADO E. globulus"),
 "cVPD": (5.0, "NEUTRO: só 3-PGmix"), "alphaCx": (0.068, "FONTE Tab.1 (L2)"), "y": (0.50, "FONTE Tab.1 (3PGmix.Data: 0,05 = erro)"),
 "MinCond": (0.0, "ADAPTADO E. globulus (0,0072 = gSx, não gCmin)"), "MaxCond": (0.0182, "FONTE Tab.1"),
 "LAIgcx": (3.33, "ADAPTADO E. globulus"), "CoeffCond": (0.05, "FONTE Tab.1 0,5 kPa-1 = 0,05 mbar-1"),
 "BLcond": (0.2, "FONTE Tab.1 (L3)"),
 "RGcGW": (0.66, "NEUTRO: só d13C"), "D13CTissueDif": (2.0, "NEUTRO: só d13C"), "aFracDiffu": (4.4, "NEUTRO: só d13C"),
 "bFracRubi": (27.0, "NEUTRO: só d13C"),
 "fracBB0": (0.35, "FONTE Tab.1"), "fracBB1": (0.15, "FONTE Tab.1 (texto: 0,12)"), "tBB": (2.0, "FONTE Tab.1"),
 "rho0": (0.44, "FONTE §2.7.3 440 kg m-3"), "rho1": (0.44, "FONTE (densidade constante)"), "tRho": (4.0, "NEUTRO: rho0=rho1"),
 "CrownShape": (3, "NEUTRO: só 3-PGmix"),
 "aH": (0.0, "AUSENTE_ZERO: altura MISSING -> saída de altura = 0"), "nHB": (0.0, "AUSENTE_ZERO"), "nHC": (0.0, "AUSENTE_ZERO"),
 "aV": (0.0, "ESTRUTURAL: volume pelo caminho de biomassa (Silva Eq.30)"), "nVB": (0.0, "ESTRUTURAL: idem"), "nVH": (0.0, "ESTRUTURAL: idem"), "nVBH": (0.0, "ESTRUTURAL: idem"),
 "aK": (0.0, "NEUTRO: só 3-PGmix"), "nKB": (0.0, "NEUTRO"), "nKH": (0.0, "NEUTRO"), "nKC": (0.0, "NEUTRO"), "nKrh": (0.0, "NEUTRO"),
 "aHL": (0.0, "NEUTRO"), "nHLB": (0.0, "NEUTRO"), "nHLL": (0.0, "NEUTRO"), "nHLC": (0.0, "NEUTRO"), "nHLrh": (0.0, "NEUTRO"),
 "Qa": (-90.0, "ADAPTADO E. globulus"), "Qb": (0.8, "ADAPTADO E. globulus"),
 "gDM_mol": (24.0, "ADAPTADO"), "molPAR_MJ": (2.3, "ADAPTADO"),
}
def params():
    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modelo"))
    from threepg_pjs import PAR_FORTRAN
    assert set(P) == set(PAR_FORTRAN), set(PAR_FORTRAN) ^ set(P)
    return {k: float(v[0]) for k, v in P.items()}
