"""
threepg_pjs.py — Tradução linha a linha do núcleo 3-PGpjs do pacote r3PG v0.1.7
(Trotsiuk, Hartig & Forrester 2020, doi:10.1111/2041-210X.13474; código-fonte
github.com/trotsiuk/r3PG, commit e39bd8e9, arquivo src/md_3PG.f95), acrescida de
uma EXTENSÃO documentada: o módulo de desfolha (ver `defoliation_events`).

Escopo traduzido (o que o TCC usa):
  * 1 espécie/coorte; light_model = 1, transp_model = 1, phys_model = 1 (3-PGpjs)
  * height_model 1 ou 2; correct_bias = 0; calculate_d13c = 0; sem desbaste
  * espécies perenifólias e decíduas (a lógica de dormência foi mantida para
    permitir o teste de referência "Broadleaf 3-PGpjs" do r3PG)
Fora do escopo (gera erro explícito): 3-PGmix, correção de viés por Weibull,
desbastes, múltiplas espécies, d13C.

Convenção temporal herdada do r3PG: a linha 0 da saída é o ESTADO INICIAL no fim do
mês `from`; o crescimento começa no mês seguinte. A linha t corresponde ao fim do
mês (from + t meses) e usa o clima desse mês.

EXTENSÃO — desfolha (não existe no r3PG original):
  defoliation_events = {"AAAA-MM": d, ...}, 0 <= d < 1.
  No início do passo do mês indicado, ANTES da interceptação de luz:
      Wf_pos = Wf_pre * (1 - d) ; LAI = Wf_pos * SLA(t) * 0.1
  A biomassa removida (Wf_pre * d) é registrada no fluxo `biom_defol`, separado da
  serapilheira (`biom_loss_foliage`). Nenhum outro parâmetro é alterado (SLA, alphaCx,
  alocação e mortalidade seguem as equações originais). O crescimento posterior é
  calculado pelas equações do modelo, sem taxa de recuperação imposta.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

# ---- constantes (src/md_decl_const.f95) ----
PI = 3.141592654
LN2 = 0.693147181
E20 = 2.2
MAX_SOIL_COND = 0.00250
LAMBDA = 2460000.0
RHO_AIR = 1.2
VPD_CONV = 0.000622
DAY_OF_YEAR = np.array([15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349], float)
DAYS_IN_MONTH = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], float)
B_N = 2  # iterações de correção (src/i_decl_var.h)

# ordem dos 82 parâmetros (src/i_read_param.h) — nomes internos do Fortran
PAR_FORTRAN = """pFS2 pFS20 aWs nWs pRx pRn gammaF1 gammaF0 tgammaF gammaR leafgrow leaffall
Tmin Topt Tmax kF SWconst0 SWpower0 fCalpha700 fCg700 m0 fN0 fNn MaxAge nAge rAge gammaN1
gammaN0 tgammaN ngammaN wSx1000 thinPower mF mR mS SLA0 SLA1 tSLA k fullCanAge MaxIntcptn
LAImaxIntcptn cVPD alphaCx y MinCond MaxCond LAIgcx CoeffCond BLcond RGcGW D13CTissueDif
aFracDiffu bFracRubi fracBB0 fracBB1 tBB rho0 rho1 tRho CrownShape aH nHB nHC aV nVB nVH
nVBH aK nKB nKH nKC nKrh aHL nHLB nHLL nHLC nHLrh Qa Qb gDM_mol molPAR_MJ""".split()
assert len(PAR_FORTRAN) == 82


def pulsos(from_ym: str, indices, d: float) -> dict:
    """Converte índices de mês da simulação em datas de evento.
    Convenção: índice k = linha k da saída = k-ésimo mês de crescimento após o estado
    inicial (`from`). Ex.: from='2014-12', k=12 -> '2015-12'; k=48 -> '2018-12'."""
    base = pd.Timestamp(from_ym + "-01")
    out = {}
    for k_ in indices:
        if int(k_) < 1:
            raise ValueError("O índice do pulso deve ser >= 1 (0 é o estado inicial).")
        out[(base + pd.DateOffset(months=int(k_))).strftime("%Y-%m")] = d
    if len(out) != len(list(indices)):
        raise ValueError("Índices de pulso repetidos.")
    return out


def params_from_table(table: pd.DataFrame, column: str) -> dict:
    """Converte a tabela de parâmetros do r3PG (82 linhas, na ordem oficial) num
    dicionário com os nomes internos do Fortran. `column` = coluna da espécie."""
    if len(table) != 82:
        raise ValueError("A tabela deve ter as 82 linhas de parâmetros do r3PG, na ordem oficial.")
    vals = table[column].astype(float).to_numpy()
    if np.isnan(vals).any():
        faltam = [table.iloc[i, 0] for i in np.where(np.isnan(vals))[0]]
        raise ValueError(f"Parâmetros sem valor (não serão inventados): {faltam}")
    return dict(zip(PAR_FORTRAN, vals))


def prepare_climate(climate: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Equivalente a r3PG::prepare_climate (caso com série completa, não 12 linhas)."""
    c = climate.copy()
    for col in ("tmp_min", "tmp_max", "prcp", "srad", "frost_days", "year", "month"):
        if col not in c:
            raise ValueError(f"Clima sem a coluna obrigatória '{col}'")
    if c[["tmp_min", "tmp_max", "prcp", "srad", "frost_days"]].isna().any().any():
        raise ValueError("Clima contém NA")
    c["date"] = pd.to_datetime(dict(year=c.year, month=c.month, day=1))
    d0, d1 = pd.Timestamp(start + "-01"), pd.Timestamp(end + "-01")
    if d0 < c.date.min() or d1 > c.date.max():
        raise ValueError("Período solicitado fora da cobertura do clima")
    c = c[(c.date >= d0) & (c.date <= d1)].copy()
    c["frost_days"] = np.minimum(c.frost_days, DAYS_IN_MONTH[c.month.to_numpy() - 1])
    if "tmp_ave" not in c:
        c["tmp_ave"] = (c.tmp_min + c.tmp_max) / 2
    if "vpd_day" not in c:
        es = lambda t: 6.10780 * np.exp(17.2690 * t / (237.30 + t))
        c["vpd_day"] = (es(c.tmp_max) - es(c.tmp_min)) / 2
    if "co2" not in c:
        c["co2"] = 350.0
    if "d13catm" not in c:
        c["d13catm"] = -7.1
    return c.reset_index(drop=True)


# ---------------- funções auxiliares (md_3PG.f95) ----------------
def f_dormant(month: int, leafgrow: int, leaffall: int) -> bool:
    if leafgrow > leaffall:
        return leaffall <= month <= leafgrow
    if leafgrow < leaffall:
        return month < leafgrow or month >= leaffall
    return False


def f_exp(x, g0, gx, tg, ng):
    if tg != 0:
        return gx + (g0 - gx) * np.exp(-LN2 * (x / tg) ** ng)
    return np.full_like(x, gx)


def f_exp_foliage(x, f1, f0, tg):
    if tg * f1 == 0:
        return np.full_like(x, f1)
    kg = 12.0 * np.log(1.0 + f1 / f0) / tg
    return f1 * f0 / (f0 + (f1 - f0) * np.exp(-kg * x))


def f_get_daylength(lat):
    slat, clat = np.sin(PI * lat / 180.0), np.cos(PI * lat / 180.0)
    sin_dec = 0.4 * np.sin(0.0172 * (DAY_OF_YEAR - 80.0))
    cos_h0 = -sin_dec * slat / (clat * np.sqrt(1.0 - sin_dec ** 2))
    dl = np.arccos(np.clip(cos_h0, -1, 1)) / PI
    dl = np.where(cos_h0 > 1, 0.0, dl)
    dl = np.where(cos_h0 < -1, 1.0, dl)
    return dl


def f_get_mortality(stems_n, ws, mS, wSx1000, thinPower):
    accuracy = 1.0 / 1000.0
    n = stems_n / 1000.0
    x1 = 1000.0 * mS * ws / stems_n
    i = 0
    while True:
        i += 1
        if n <= 0:
            break
        x2 = wSx1000 * n ** (1.0 - thinPower)
        fN = x2 - x1 * n - (1.0 - mS) * ws
        dfN = (1.0 - thinPower) * x2 / n - x1
        dN = -fN / dfN
        n = n + dN
        if abs(dN) <= accuracy or i >= 5:
            break
    return stems_n - 1000.0 * n


def run_3pg_pjs(site: dict, species: dict, climate: pd.DataFrame, params: dict,
                height_model: int = 1, defoliation_events: dict | None = None,
                settings: dict | None = None) -> pd.DataFrame:
    """Executa o 3-PGpjs. Retorna DataFrame mensal (linha 0 = estado inicial)."""
    if settings is not None:
        exig = dict(light_model=1, transp_model=1, phys_model=1, correct_bias=0, calculate_d13c=0)
        for k_, v_ in exig.items():
            if settings.get(k_, v_) != v_:
                raise NotImplementedError(f"Configuração não suportada nesta tradução: {k_}={settings[k_]}")
    np.seterr(all="ignore")
    P = {k_: np.float64(v_) for k_, v_ in params.items()}
    leafgrow, leaffall = int(P["leafgrow"]), int(P["leaffall"])

    clim = prepare_climate(climate, site["from"], site["to"])
    n_m = len(clim)
    tmin, tmax, tave = (clim[c].to_numpy(float) for c in ("tmp_min", "tmp_max", "tmp_ave"))
    prcp, srad, frost = (clim[c].to_numpy(float) for c in ("prcp", "srad", "frost_days"))
    vpd_day, co2 = clim.vpd_day.to_numpy(float), clim.co2.to_numpy(float)

    lat = float(site["latitude"])
    soil_class = int(site["soil_class"])
    ASW, asw_min, asw_max = float(site["asw_i"]), float(site["asw_min"]), float(site["asw_max"])
    year_i, month_i = map(int, site["from"].split("-"))
    year_p, month_p = map(int, species["planted"].split("-"))
    fertility = float(species["fertility"])

    # ---- eventos de desfolha (EXTENSÃO) ----
    dates = pd.date_range(pd.Timestamp(site["from"] + "-01"), periods=n_m, freq="MS")
    defol = np.zeros(n_m)
    for ym, frac in (defoliation_events or {}).items():
        frac = float(frac)
        if not (0.0 <= frac < 1.0):
            raise ValueError(f"Intensidade de desfolha deve estar em [0,1): {ym}={frac}")
        hit = np.where(dates == pd.Timestamp(ym + "-01"))[0]
        if len(hit) != 1:
            raise ValueError(f"Mês de desfolha fora da simulação: {ym}")
        if hit[0] == 0:
            raise ValueError("Desfolha no mês inicial não é permitida: a linha 0 é o estado inicial.")
        if defol[hit[0]] != 0.0:
            raise ValueError(f"Evento duplicado para {ym}")
        if f_dormant(int(dates[hit[0]].month), leafgrow, leaffall):
            raise ValueError("Desfolha em mês de dormência não é suportada.")
        defol[hit[0]] = frac

    # ---- INITIALISATION (age independent) ----
    day_length = 86400.0 * f_get_daylength(lat)
    fCalphax = P["fCalpha700"] / (2.0 - P["fCalpha700"])
    fCg0 = P["fCg700"] / (2.0 * P["fCg700"] - 1.0)
    month_vector = (np.arange(n_m) + month_i - 1) % 12 + 1

    Tmin_, Topt_, Tmax_ = P["Tmin"], P["Topt"], P["Tmax"]
    expo = (Tmax_ - Topt_) / (Topt_ - Tmin_)
    f_tmp = ((tave - Tmin_) / (Topt_ - Tmin_)) * ((Tmax_ - tave) / (Tmax_ - Topt_)) ** expo
    f_tmp = np.where((tave <= Tmin_) | (tave >= Tmax_), 0.0, f_tmp)
    tg_ = (tave + tmax) / 2
    f_tmp_gc = ((tg_ - Tmin_) / (Topt_ - Tmin_)) * ((Tmax_ - tg_) / (Tmax_ - Topt_)) ** expo
    f_tmp_gc = np.where((tg_ <= Tmin_) | (tg_ >= Tmax_), 0.0, f_tmp_gc)
    f_frost = 1.0 - P["kF"] * (frost / DAYS_IN_MONTH[month_vector - 1])
    f_calpha = fCalphax * co2 / (350.0 * (fCalphax - 1.0) + co2)
    f_cg = fCg0 / (1.0 + (fCg0 - 1.0) * co2 / 350.0)

    if soil_class > 0:
        SWconst, SWpower = 0.8 - 0.10 * soil_class, 11.0 - 2.0 * soil_class
    elif soil_class < 0:
        SWconst, SWpower = P["SWconst0"], P["SWpower0"]
    else:
        SWconst, SWpower = 999.0, P["SWpower0"]
    if asw_min > asw_max:
        asw_min = asw_max
    ASW = max(min(ASW, asw_max), asw_min)
    water_runoff_polled, poolFractn, Irrig = 0.0, 0.0, 0.0
    fN0 = 1.0 if P["fNn"] == 0 else P["fN0"]
    pfsPower = np.log(P["pFS20"] / P["pFS2"]) / np.log(20.0 / 2.0)
    pfsConst = P["pFS2"] / 2.0 ** pfsPower

    # ---- INITIALISATION (age dependent) ----
    age = (12.0 * (year_i - year_p) + month_i - month_p - 1.0 + np.arange(1, n_m + 1)) / 12.0
    age_m = age - 1.0 / 12.0
    age_m[0] = age[0]
    SLA = f_exp(age_m, P["SLA0"], P["SLA1"], P["tSLA"], 2.0)
    fracBB = f_exp(age_m, P["fracBB0"], P["fracBB1"], P["tBB"], 1.0)
    wood_density = f_exp(age_m, P["rho0"], P["rho1"], P["tRho"], 1.0)
    gammaN = f_exp(age, P["gammaN0"], P["gammaN1"], P["tgammaN"], P["ngammaN"])
    gammaF = f_exp_foliage(age_m, P["gammaF1"], P["gammaF0"], P["tgammaF"])
    if P["nAge"] == 0:
        f_age = np.ones(n_m)
    else:
        f_age = 1.0 / (1.0 + ((age_m / P["MaxAge"]) / P["rAge"]) ** P["nAge"])

    # ---- estado ----
    S = dict(stems_n=0.0, biom_stem=0.0, biom_foliage=0.0, biom_root=0.0, biom_foliage_debt=0.0,
             biom_tree=0.0, dbh=0.0, basal_area=0.0, height=0.0, lai=0.0, crown_length=0.0,
             crown_width=0.0, pFS=0.0, height_rel=0.0)

    def size_dist_correct(t):
        competition = wood_density[t] * S["basal_area"]
        h_rel = S["height"] / (S["height"] * S["stems_n"] / S["stems_n"])
        S["height_rel"] = h_rel
        dbh = (S["biom_tree"] / P["aWs"]) ** (1.0 / P["nWs"])
        S["dbh"] = dbh
        S["basal_area"] = dbh ** 2.0 / 4.0 * PI * S["stems_n"] / 10000.0
        if height_model == 1:
            S["height"] = P["aH"] * dbh ** P["nHB"] * competition ** P["nHC"]
            S["crown_length"] = (P["aHL"] * dbh ** P["nHLB"] * S["lai"] ** P["nHLL"] *
                                 competition ** P["nHLC"] * h_rel ** P["nHLrh"])
        elif height_model == 2:
            S["height"] = 1.3 + P["aH"] * np.exp(1.0) ** (-P["nHB"] / dbh) + P["nHC"] * competition * dbh
            S["crown_length"] = 1.3 + P["aHL"] * np.exp(1.0) ** (-P["nHLB"] / dbh) + P["nHLC"] * competition * dbh
        else:
            raise ValueError("height_model deve ser 1 ou 2")
        cw = (P["aK"] * dbh ** P["nKB"] * S["height"] ** P["nKH"] * competition ** P["nKC"] *
              h_rel ** P["nKrh"])
        S["crown_width"] = 0.0 if S["lai"] == 0 else cw
        S["pFS"] = pfsConst * dbh ** pfsPower
        if S["crown_length"] > S["height"]:
            S["crown_length"] = S["height"]

    def update_tree_lai(t):
        S["biom_tree"] = 0.0 if S["stems_n"] == 0 else S["biom_stem"] * 1000.0 / S["stems_n"]
        S["lai"] = S["biom_foliage"] * SLA[t] * 0.1

    def volume_now(t):
        if P["aV"] > 0:
            return (P["aV"] * S["dbh"] ** P["nVB"] * S["height"] ** P["nVH"] *
                    (S["dbh"] * S["dbh"] * S["height"]) ** P["nVBH"] * S["stems_n"])
        return S["biom_stem"] * (1.0 - fracBB[t]) / wood_density[t]

    rows = []
    month = month_i
    # ---- INITIALISATION (stand), ii = 1 ----
    t = 0
    if age[0] >= 0:
        S.update(stems_n=float(species["stems_n"]), biom_stem=float(species["biom_stem"]),
                 biom_foliage=float(species["biom_foliage"]), biom_root=float(species["biom_root"]))
    if f_dormant(month, leafgrow, leaffall):
        S["biom_foliage_debt"], S["biom_foliage"] = S["biom_foliage"], 0.0
    if age[0] >= 0:
        S["biom_tree"] = S["biom_stem"] * 1000.0 / S["stems_n"]
        S["dbh"] = (S["biom_tree"] / P["aWs"]) ** (1.0 / P["nWs"])
        S["basal_area"] = S["dbh"] ** 2.0 / 4.0 * PI * S["stems_n"] / 10000.0
        S["lai"] = S["biom_foliage"] * SLA[0] * 0.1
    competition = wood_density[0] * S["basal_area"]
    if height_model == 1:
        S["height"] = P["aH"] * S["dbh"] ** P["nHB"] * competition ** P["nHC"]
    else:
        S["height"] = 1.3 + P["aH"] * np.exp(1.0) ** (-P["nHB"] / S["dbh"]) + P["nHC"] * competition * S["dbh"]
    for _ in range(B_N):
        size_dist_correct(0)
    volume = volume_now(0)
    volume_cum = volume_old = volume
    volume_mai = volume_cum / age[0]
    volume_change = 0.0

    zero_flux = dict(gpp=0.0, npp_f=0.0, apar=0.0, alpha_c=0.0, f_vpd=0.0, f_sw=0.0, f_nutr=0.0,
                     f_phys=0.0, f_transp_scale=0.0, canopy_cover=0.0, transp_veg=0.0,
                     evapo_transp=0.0, prcp_interc=0.0, prcp_runoff=0.0, biom_loss_foliage=0.0,
                     biom_loss_root=0.0, biom_incr_foliage=0.0, biom_incr_root=0.0,
                     biom_incr_stem=0.0, mort_stress=0.0, mort_thinn=0.0,
                     wf_pre_defol=np.nan, biom_defol=0.0, defol_frac=0.0)
    F = dict(zero_flux)

    def record(t):
        rows.append(dict(
            date=(dates[t] + pd.offsets.MonthEnd(0)).date(), age=age[t], stems_n=S["stems_n"],
            basal_area=S["basal_area"], dbh=S["dbh"], height=S["height"], volume=volume,
            volume_mai=volume_mai, volume_change=volume_change, volume_cum=volume_cum,
            sla=SLA[t], lai=S["lai"], biom_stem=S["biom_stem"], biom_root=S["biom_root"],
            biom_foliage=S["biom_foliage"], biom_foliage_debt=S["biom_foliage_debt"],
            biom_tree=S["biom_tree"], wood_density=wood_density[t], fracBB=fracBB[t],
            f_age=f_age[t], f_tmp=f_tmp[t], f_frost=f_frost[t], f_calpha=f_calpha[t],
            gammaF=gammaF[t], asw=ASW, pFS=S["pFS"], **F))

    record(0)
    mort_stress = 0.0

    # ---- Monthly simulations, ii = 2..n_m ----
    for t in range(1, n_m):
        F = dict(zero_flux)
        month = month + 1
        if month > 12:
            month = 1
        b_cor = False
        if age[t] == 0.0:
            S.update(stems_n=float(species["stems_n"]), biom_stem=float(species["biom_stem"]),
                     biom_foliage=float(species["biom_foliage"]), biom_root=float(species["biom_root"]))
            b_cor = True
        dorm, dorm_prev = f_dormant(month, leafgrow, leaffall), f_dormant(month - 1, leafgrow, leaffall)
        if not dorm and dorm_prev:
            S["lai"] = S["biom_foliage_debt"] * SLA[t] * 0.1
            b_cor = True
        if dorm and not dorm_prev:
            S["biom_foliage_debt"], S["biom_foliage"], S["lai"] = S["biom_foliage"], 0.0, 0.0
            b_cor = True
        if b_cor:
            for _ in range(B_N):
                size_dist_correct(t)
            b_cor = False

        # ===== EXTENSÃO: evento de desfolha (início do mês, antes da luz) =====
        if defol[t] > 0.0 or (defoliation_events and dates[t].strftime("%Y-%m") in defoliation_events):
            wf_pre = S["biom_foliage"]
            removed = wf_pre * defol[t]
            S["biom_foliage"] = wf_pre - removed
            S["lai"] = S["biom_foliage"] * SLA[t] * 0.1
            F.update(wf_pre_defol=wf_pre, biom_defol=removed, defol_frac=defol[t])
        # =====================================================================

        # Radiation and assimilation (s_light_3pgpjs)
        cc = 1.0
        if P["fullCanAge"] > 0 and age_m[t] < P["fullCanAge"]:
            cc = (age_m[t] + 0.01) / P["fullCanAge"]
        light_int = 1.0 - np.exp(-P["k"] * S["lai"] / cc)
        apar = srad[t] * DAYS_IN_MONTH[month - 1] * light_int * cc
        vpd_sp = vpd_day[t]

        f_vpd = np.exp(-P["CoeffCond"] * vpd_sp)
        f_sw = 1.0 / (1.0 + ((1.0 - ASW / asw_max) / SWconst) ** SWpower)
        f_nutr = 1.0 if P["fNn"] == 0 else 1.0 - (1.0 - fN0) * (1.0 - fertility) ** P["fNn"]
        f_phys = min(f_vpd, f_sw) * f_age[t]
        f_tmp_gc_t = 1.0  # phys_model = 1

        alpha_c = P["alphaCx"] * f_nutr * f_tmp[t] * f_frost[t] * f_calpha[t] * f_phys
        if S["lai"] == 0:
            alpha_c = 0.0
        epsilon = P["gDM_mol"] * P["molPAR_MJ"] * alpha_c
        GPP = epsilon * apar / 100.0
        NPP = GPP * P["y"]

        # Water balance
        lai_total = S["lai"]
        lai_per = 0.0 if lai_total == 0 else S["lai"] / lai_total
        gC = P["MaxCond"]
        if lai_total <= P["LAIgcx"]:
            gC = P["MinCond"] + (P["MaxCond"] - P["MinCond"]) * lai_total / P["LAIgcx"]
        conduct_canopy = gC * lai_per * f_phys * f_tmp_gc_t * f_cg[t]
        if vpd_sp == 0:
            transp = 0.0
        else:
            dl = day_length[month - 1]
            net_rad = P["Qa"] + P["Qb"] * (srad[t] * 10.0 ** 6.0 / dl)
            def_term = RHO_AIR * LAMBDA * (VPD_CONV * vpd_sp) * P["BLcond"]
            div = conduct_canopy * (1.0 + E20) + P["BLcond"]
            transp = DAYS_IN_MONTH[month - 1] * conduct_canopy * (E20 * net_rad + def_term) / div / LAMBDA * dl
            transp = max(0.0, transp)
        transp_total = transp
        interc_fract = P["MaxIntcptn"]
        if P["LAImaxIntcptn"] > 0:
            interc_fract = P["MaxIntcptn"] * min(1.0, lai_total / P["LAImaxIntcptn"]) * lai_per
        prcp_interc = prcp[t] * interc_fract
        ASW = ASW + prcp[t] + (100.0 * Irrig / 12.0) + water_runoff_polled
        evapo_transp = min(ASW, transp_total + prcp_interc)
        excessSW = max(ASW - evapo_transp - asw_max, 0.0)
        ASW = ASW - evapo_transp - excessSW
        water_runoff_polled = poolFractn * excessSW
        prcp_runoff = (1.0 - poolFractn) * excessSW
        if ASW < asw_min:
            ASW = asw_min
        if (transp_total + prcp_interc) == 0:
            f_transp_scale = 1.0
        else:
            f_transp_scale = evapo_transp / (transp_total + prcp_interc)
        GPP *= f_transp_scale
        NPP *= f_transp_scale
        NPP_f = NPP
        if transp_total > 0 and f_transp_scale < 1:
            transp = (evapo_transp - prcp_interc) / transp_total * transp

        # Biomass increment and loss
        m = P["m0"] + (1.0 - P["m0"]) * fertility
        fr_root = P["pRx"] * P["pRn"] / (P["pRn"] + (P["pRx"] - P["pRn"]) * f_phys * m)
        fr_stem = (1.0 - fr_root) / (1.0 + S["pFS"])
        fr_fol = 1.0 - fr_root - fr_stem
        if dorm:
            loss_f = 0.0 if dorm_prev else S["biom_foliage_debt"]
            loss_r = inc_f = inc_r = inc_s = 0.0
        else:
            if S["biom_foliage"] == 0.0:
                S["biom_foliage"] = S["biom_foliage_debt"]
            if NPP >= S["biom_foliage_debt"]:
                NPP = NPP - S["biom_foliage_debt"]
                S["biom_foliage_debt"] = 0.0
            else:
                S["biom_foliage_debt"] = S["biom_foliage_debt"] - NPP
                NPP = 0.0
            loss_f = gammaF[t] * S["biom_foliage"]
            loss_r = P["gammaR"] * S["biom_root"]
            inc_f, inc_r, inc_s = NPP * fr_fol, NPP * fr_root, NPP * fr_stem
            S["biom_foliage"] = S["biom_foliage"] + inc_f - loss_f
            S["biom_root"] = S["biom_root"] + inc_r - loss_r
            S["biom_stem"] = S["biom_stem"] + inc_s

        update_tree_lai(t)
        for _ in range(B_N):
            size_dist_correct(t)
        volume = volume_now(t)
        volume_change = volume - volume_old
        if S["lai"] == 0 or volume_change <= 0:
            volume_change = 0.0
        volume_cum = volume_cum + volume_change
        volume_old = volume
        volume_mai = volume_cum / age[t]

        # Mortality — stress related
        if not dorm:
            if gammaN[t] > 0:
                mort_stress = min(gammaN[t] * S["stems_n"] / 12.0 / 100.0, S["stems_n"])
                for kk, mk in (("biom_foliage", "mF"), ("biom_root", "mR"), ("biom_stem", "mS")):
                    S[kk] = S[kk] - P[mk] * mort_stress * (S[kk] / S["stems_n"])
                S["stems_n"] -= mort_stress
                b_cor = True
        else:
            mort_stress = 0.0
        if b_cor:
            update_tree_lai(t)
            for _ in range(B_N):
                size_dist_correct(t)
            b_cor = False

        # Mortality — self-thinning
        ba_prop = S["basal_area"] / S["basal_area"]
        stems_n_ha = S["stems_n"] / ba_prop
        biom_tree_max = P["wSx1000"] * (1000.0 / stems_n_ha) ** P["thinPower"]
        mort_thinn = 0.0
        if not dorm:
            if biom_tree_max < S["biom_tree"]:
                mort_thinn = f_get_mortality(stems_n_ha, S["biom_stem"] / ba_prop, P["mS"],
                                             P["wSx1000"], P["thinPower"]) * ba_prop
                if mort_thinn < S["stems_n"]:
                    for kk, mk in (("biom_foliage", "mF"), ("biom_root", "mR"), ("biom_stem", "mS")):
                        S[kk] = S[kk] - P[mk] * mort_thinn * (S[kk] / S["stems_n"])
                    S["stems_n"] -= mort_thinn
                else:
                    S.update(biom_foliage=0.0, biom_root=0.0, biom_stem=0.0, stems_n=0.0)
                b_cor = True
        if b_cor:
            update_tree_lai(t)
            for _ in range(B_N):
                size_dist_correct(t)

        F.update(gpp=GPP, npp_f=NPP_f, apar=apar, alpha_c=alpha_c, f_vpd=f_vpd, f_sw=f_sw,
                 f_nutr=f_nutr, f_phys=f_phys, f_transp_scale=f_transp_scale, canopy_cover=cc,
                 transp_veg=transp, evapo_transp=evapo_transp, prcp_interc=prcp_interc,
                 prcp_runoff=prcp_runoff, biom_loss_foliage=loss_f, biom_loss_root=loss_r,
                 biom_incr_foliage=inc_f, biom_incr_root=inc_r, biom_incr_stem=inc_s,
                 mort_stress=mort_stress, mort_thinn=mort_thinn)
        record(t)

    return pd.DataFrame(rows)
