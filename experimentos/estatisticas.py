#!/usr/bin/env python3
"""
Estatísticas de avaliação — mesmas métricas de Castro et al. (artigo RNA Khaya): R², r(yŷ), RQEM %.
Acrescidos: viés, viés %, MAE e teste F de Graybill (H0: β0 = 0 e β1 = 1) quando n permite.

Bloco A — VERIFICAÇÃO: port × r3PG original (260 controles) e port × 3-PG Excel/VBA (r3PG tests).
Bloco B — SIMULADO × OBSERVADO: Bertulio et al. (2008), valores absolutos (DAP, altura, volume por árvore)
          e perdas relativas. n pequeno, pares não independentes -> só descritivo.
Bloco C — METAMODELO da resposta do simulador: floresta aleatória com validação cruzada k = 7 e
          importância por permutação (mesmo formato do artigo). Caracteriza o simulador, não a realidade.
"""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
S = AQUI / "saida"; OUT = S / "estatisticas"; OUT.mkdir(exist_ok=True)


def metricas(y, yh):
    y, yh = np.asarray(y, float), np.asarray(yh, float)
    n = len(y); e = yh - y
    r2 = 1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum() if np.var(y) > 0 else np.nan
    r = np.corrcoef(y, yh)[0, 1] if n > 2 and np.std(yh) > 0 else np.nan
    rqem = 100 / y.mean() * np.sqrt((e ** 2).mean())
    out = dict(n=n, R2=r2, r_yyhat=r, RQEM_pct=rqem, vies=e.mean(), vies_pct=100 * e.mean() / y.mean(),
               MAE=np.abs(e).mean())
    if n >= 5 and np.std(yh) > 0:                     # Graybill (1976): y = β0 + β1·ŷ ; H0: β0=0, β1=1
        X = np.column_stack([np.ones(n), yh]); b, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ b; s2 = (res ** 2).sum() / (n - 2); d = b - np.array([0, 1])
        F = d @ (X.T @ X) @ d / (2 * s2) if s2 > 0 else np.inf
        out.update(graybill_F=F, graybill_p=1 - stats.f.cdf(F, 2, n - 2) if np.isfinite(F) else 0.0,
                   beta0=b[0], beta1=b[1])
    return out


RES = {}

# ---------------- A1: port × r3PG original ----------------
R = pd.read_csv(AQUI / "r_check/r3pg_controles.csv").pivot_table(index=["id", "date"], columns="variable",
                                                                    values="value").reset_index()
D = pd.read_csv(S / "mensal.csv.gz", usecols=["id", "date", "biom_stem", "biom_foliage", "biom_root", "volume", "lai", "dbh"])
J = R.merge(D, on=["id", "date"], suffixes=("_r3pg", "_port"))
A = []
for v in ["biom_stem", "biom_foliage", "biom_root", "volume", "lai", "dbh"]:
    m = metricas(J[f"{v}_r3pg"], J[f"{v}_port"]); m.update(comparacao="port × r3PG original (R)", variavel=v); A.append(m)

# ---------------- A2: port × 3-PG Excel/VBA ----------------
vba = pd.read_csv(AQUI.parent / "modelo/testes/saida_comparacao_vba.csv")  # resumo já existente
sys.path.insert(0, str(AQUI.parent / "modelo/testes"))
try:
    sys.path.insert(0, "/home/claude/libs_ext/xlrd")
    from comparar_vba import comparar  # noqa: E402
    import comparar_vba as CV  # noqa: E402
    x = pd.read_excel(CV.INP, sheet_name=None, engine="xlrd")
    dflt = pd.read_excel(CV.R / "data-raw/data.default.xlsx", sheet_name="parameters")
    from threepg_pjs import run_3pg_pjs, params_from_table  # noqa: E402
    for site_id, skip, nome in [("evergreen_pjs", 5, "Pinus sylvestris"), ("broadleaf_pjs", 235, "Fagus sylvatica")]:
        site = x["site"].set_index("site").loc[site_id].to_dict(); sp = x["species"].set_index("site").loc[site_id].to_dict()
        clim = x["climate"][x["climate"].climate_id == "eumixfor_clim"].drop(columns="climate_id").dropna(axis=1, how="all")
        mp = dict(zip(x["parameters"].parameter, x["parameters"][nome]))
        par = dflt[["parameter"]].copy(); par[nome] = [mp.get(p, d) for p, d in zip(dflt.parameter, dflt.default)]
        sim = run_3pg_pjs(site, sp, clim, params_from_table(par, nome))
        v = pd.read_excel(CV.OUT, sheet_name="Output", skiprows=skip, nrows=111, engine="xlrd")
        for cv, cs in {"Stem DM1": "biom_stem", "Foliage DM1": "biom_foliage", "Root DM1": "biom_root",
                       "Stand volume1": "volume", "LAI1": "lai", "Mean DBH1": "dbh"}.items():
            a = pd.to_numeric(v[cv], errors="coerce").to_numpy()[:110]; b = sim[cs].to_numpy()[:110]; ok = ~np.isnan(a)
            if np.std(a[ok]) == 0:
                continue
            m = metricas(a[ok], b[ok]); m.update(comparacao=f"port × 3-PG Excel/VBA ({site_id})", variavel=cs); A.append(m)
except Exception as ex:  # noqa: BLE001
    print("aviso VBA:", ex)
TA = pd.DataFrame(A); TA.to_csv(OUT / "A_verificacao.csv", index=False)

# ---------------- B: Bertulio — valores absolutos e perdas ----------------
import adversarial_e_literatura as AL  # noqa: E402  (reaproveita sim() e clima de Campo Verde)
obs = pd.read_csv(AQUI.parent / "revisao/dados_tratamentos_observados_verificado.csv")
ob = obs[obs.study_id == "Bertulio_2008"]
B = []
mapa = {"C5": "E. urophylla × E. grandis (urograndis)", "A1": "E. urophylla × E. camaldulensis (urocam)"}
for mat, alvo in mapa.items():
    frm = "2007-02" if mat == "A1" else "2006-05"
    for d in [0.95, 0.999]:
        c = AL.sim(sitio="CV", mat=mat, frm=frm, to="2008-06", planted="2006-02")
        t = AL.sim(sitio="CV", mat=mat, frm=frm, to="2008-06", planted="2006-02", ev={"2007-04": d, "2008-01": d})
        for idade, data in [(14, "2007-03-31"), (26, "2008-04-30")]:
            for grupo, g in [("testemunha", c), ("desfolha", t)]:
                row = g.set_index(g.date.astype(str)).loc[data]
                simv = {"CAP": row.dbh * np.pi, "altura": row.height, "volume": row.volume / row.stems_n}
                for var in ["CAP", "altura", "volume"]:
                    if var == "altura" and mat == "A1":
                        continue
                    o = ob[(ob.especie_ou_clone == alvo) & (ob.variavel == var) & (ob.idade_meses == idade)].iloc[0]
                    B.append(dict(material_sim=mat, alvo=alvo, desfolha_sim=d, idade=idade, grupo=grupo, variavel=var,
                                  observado=o.valor_controle if grupo == "testemunha" else o.valor_tratamento,
                                  simulado=simv[var]))
TB = pd.DataFrame(B); TB.to_csv(OUT / "B_bertulio_pares_absolutos.csv", index=False)
BM = []
for (mat, d, var), g in TB.groupby(["material_sim", "desfolha_sim", "variavel"]):
    m = metricas(g.observado, g.simulado); m.update(material_sim=mat, desfolha_sim=d, variavel=var); BM.append(m)
TBM = pd.DataFrame(BM); TBM.to_csv(OUT / "B_bertulio_metricas_absolutas.csv", index=False)
L = pd.read_csv(S / "confronto_literatura_bertulio.csv")
LP = L[(L.data_aval == "2008-04-30")]
LM = []
for (mat, d, tipo), g in LP.groupby(["material_sim", "desfolha_sim", "tipo_L_obs"]):
    m = metricas(g.L_obs, g.L_sim); m.update(material_sim=mat, desfolha_sim=d, tipo_L_obs=tipo); LM.append(m)
TLM = pd.DataFrame(LM); TLM.to_csv(OUT / "B_bertulio_metricas_perdas.csv", index=False)

# ---------------- C: metamodelo (RF, k = 7) + importância por permutação ----------------
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.model_selection import KFold, cross_val_predict  # noqa: E402
from sklearn.inspection import permutation_importance  # noqa: E402
I = pd.read_csv(S / "indicadores_por_tratamento.csv")
I = I[I.experimento.isin(["E1-E6", "LOCAL"]) & I.apto_analise_principal].copy()
I["Fn"] = I.nivel_FR.str[1:].astype(int)
FEAT = ["desfolha", "n_eventos", "mes_evento", "asw_max", "Fn", "sitio", "material"]
GRUPOS_BASE = {"intensidade": ["desfolha"], "frequência": ["n_eventos"], "época": ["mes_evento"], "água (ASWmax)": ["asw_max"],
               "fertilidade (FR)": ["Fn"]}


def importancia(Id, alvo, cols_extra=True):
    X = pd.get_dummies(Id[FEAT], columns=["sitio", "material"], dtype=float)
    m_ = Id[alvo].notna(); y = Id.loc[m_, alvo].to_numpy(); Xm = X[m_]
    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=20261030, n_jobs=4).fit(Xm, y)
    pi = permutation_importance(rf, Xm, y, n_repeats=10, random_state=20261030, n_jobs=4)
    imp = pd.Series(pi.importances_mean, index=Xm.columns)
    g = dict(GRUPOS_BASE); g["local"] = [c for c in Xm.columns if c.startswith("sitio_")]
    g["material genético"] = [c for c in Xm.columns if c.startswith("material_")]
    g = {k: v for k, v in g.items() if v}
    tot = sum(max(imp[c].sum(), 0) for c in g.values())
    return {k: 100 * max(imp[c].sum(), 0) / tot for k, c in g.items()}, rf, Xm, y


C = []; IMP = []
for alvo in ["perda_volume_k72", "perda_NPP_acum_pct", "recup_rel95_meses_ev1"]:
    imp, rf, Xm, y = importancia(I, alvo)
    yh = cross_val_predict(RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=20261030, n_jobs=4),
                           Xm, y, cv=KFold(7, shuffle=True, random_state=20261030))
    mm = metricas(y, yh); mm.update(resposta=alvo, modelo="Random Forest, validação cruzada k=7", escopo="3 locais"); C.append(mm)
    for k, v in imp.items():
        IMP.append(dict(escopo="3 locais", resposta=alvo, variavel=k, importancia_relativa_pct=v))
    for s_ in ["IND", "TB", "IMP"]:
        imp_s, *_ = importancia(I[I.sitio == s_], alvo)
        for k, v in imp_s.items():
            IMP.append(dict(escopo=s_, resposta=alvo, variavel=k, importancia_relativa_pct=v))
TC = pd.DataFrame(C); TC.to_csv(OUT / "C_metamodelo_validacao_cruzada.csv", index=False)
TI = pd.DataFrame(IMP); TI.to_csv(OUT / "C_importancia_variaveis.csv", index=False)
I["W"] = I.asw_max

# correlação de postos (monotonicidade) intensidade × perda, por combinação
mono = I.groupby(["sitio", "material", "asw_max", "Fn", "calendario", "experimento"]).apply(
    lambda g: stats.spearmanr(g.desfolha, g.perda_volume_k72)[0]).rename("rho_spearman").reset_index()
mono.to_csv(OUT / "C_monotonicidade_intensidade.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 20)
print("=== A verificação ===\n", TA[["comparacao", "variavel", "n", "R2", "r_yyhat", "RQEM_pct", "vies_pct"]].to_string(), sep="")
print("=== B absolutos ===\n", TBM.round(3).to_string(), sep="")
print("=== B perdas ===\n", TLM[["material_sim", "desfolha_sim", "tipo_L_obs", "n", "R2", "r_yyhat", "RQEM_pct", "vies", "MAE"]].round(2).to_string(), sep="")
print("=== C metamodelo ===\n", TC[["resposta", "escopo", "n", "R2", "r_yyhat", "RQEM_pct"]].round(3).to_string(), sep="")
print(TI.pivot_table(index=["resposta", "variavel"], columns="escopo", values="importancia_relativa_pct").round(1).to_string())
print("monotonicidade: rho=1 em", (mono.rho_spearman > 0.999).sum(), "de", len(mono))
