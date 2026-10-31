#!/usr/bin/env python3
"""Análise do espaço de possibilidades (saida/possibilidades/possibilidades.csv) e comprovação por k-fold.
(1) Quando o atacado produz mais que o controle; recuperação das folhas, da árvore individual e do crescimento.
(2) Aditividade dos danos (perda combinada × soma das perdas isoladas).
(3) Teste do autor na plataforma: A1, Indianópolis, dois pulsos de 95% (jan/2017 e jan/2020), r = 60%, m = 25%,
    fisiologia calibrada, decomposto por dano.
(4) Metamodelo Random Forest da perda de volume: k-fold 10 × 3 e deixa um local de fora; classificador ganho × perda
    com k-fold estratificado 10 × 3. Mede se os padrões são sistemáticos (o metamodelo imita o 3-PG), não se o 3-PG
    acerta o campo. Só cenários aptos (exclui A1 em IMP, ALM e ARA)."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold, LeaveOneGroupOut
from sklearn.inspection import permutation_importance

AQUI = Path(__file__).resolve().parent; sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
import possibilidades as PS  # noqa: E402
from clima import clima_mensal  # noqa: E402
OUT = PS.OUT; SEED = 2026
D = pd.read_csv(OUT / "possibilidades.csv"); A = D[D.apto].copy()
R = {"n_cenarios": len(D), "n_aptos": len(A)}

# (1) ganhos e recuperação
for v, g in A.groupby("versao"):
    gd = g[g.d > 0]
    R[f"{v}"] = dict(
        n=len(g), frac_ganho=float((g.perda_volume < 0).mean() * 100), ganho_max=float(-g.perda_volume.min()),
        n_ganho=int((g.perda_volume < 0).sum()),
        frac_ganho_so_desfolha=float((g[(g.r == 0) & (g.m == 0)].perda_volume < 0).mean() * 100),
        frac_folhas_recuperam=float(gd.recup_folhas_meses.notna().mean() * 100),
        recup_folhas_mediana=float(gd.recup_folhas_meses.median()),
        frac_npp_pos_maior=float((gd.npp_pos_rel > 0).mean() * 100),
        perda_mediana=float(g.perda_volume.median()), perda_max=float(g.perda_volume.max()))
    G = g[g.perda_volume < 0]
    if len(G):
        R[v]["ganho_condicoes"] = dict(d=sorted(G.d.unique().tolist()), r=sorted(G.r.unique().tolist()), m=sorted(G.m.unique().tolist()),
                                     freq=sorted(G.freq.unique().tolist()), sitios=sorted(G.sitio.unique().tolist()),
                                     materiais=sorted(G.material.unique().tolist()))
# ganhos por tipo de dano isolado
tipos = {"só desfolha": (A.d > 0) & (A.r == 0) & (A.m == 0), "só perda de eficiência": (A.d == 0) & (A.r > 0) & (A.m == 0),
         "só mortalidade": (A.d == 0) & (A.r == 0) & (A.m > 0), "danos combinados": A.n_danos >= 2}
R["ganho_por_tipo"] = {f"{t} | {v}": dict(n=int(len(g)), n_ganho=int((g.perda_volume < 0).sum()), frac=float((g.perda_volume < 0).mean() * 100),
                                          ganho_max=float(max(0, -g.perda_volume.min())))
                       for t, cond in tipos.items() for v, g in A[cond].groupby("versao")}
SD = A[tipos["só desfolha"] & (A.perda_volume < 0)]
R["ganho_so_desfolha_calibrada"] = {f"d{d}_{f}": int(n) for (d, f), n in SD[SD.versao == "calibrada"].groupby(["d", "freq"]).size().items()}
R["ganho_so_desfolha_original_sitios"] = sorted(SD[SD.versao == "original"].sitio.unique().tolist())
R["ganho_mortalidade_sitios"] = sorted(A[tipos["só mortalidade"] & (A.perda_volume < 0)].sitio.unique().tolist())
top = A.loc[A.perda_volume.idxmin()]; R["maior_ganho"] = {k: (top[k].item() if hasattr(top[k], "item") else top[k]) for k in ["sitio", "material", "d", "freq", "epoca", "r", "m", "versao", "perda_volume"]}
M_ = A[A.m > 0]
R["mortalidade"] = dict(n=len(M_), frac_arvore_maior=float((M_.perda_por_arvore < 0).mean() * 100),
                        frac_arvore_maior_e_talhao_menor=float(((M_.perda_por_arvore < 0) & (M_.perda_volume > 0)).mean() * 100))
# perda por desfolha isolada, por intensidade e versão (pulso único, jan)
T = A[(A.r == 0) & (A.m == 0) & (A.freq == "P1") & (A.epoca == 1)].groupby(["versao", "d"]).perda_volume.agg(["min", "median", "max"])
T.to_csv(OUT / "perda_por_intensidade.csv"); R["perda_por_intensidade_P1_jan"] = {f"{v}_{d}": dict(r) for (v, d), r in T.round(2).iterrows()}
# (2) aditividade
C = A[(A.n_danos >= 2) & A.soma_isolados.notna()]
R["aditividade"] = dict(n=len(C), frac_subaditivo=float((C.interacao < 0).mean() * 100), interacao_mediana=float(C.interacao.median()),
                        interacao_q05=float(C.interacao.quantile(.05)), interacao_q95=float(C.interacao.quantile(.95)))


# (3) teste do autor
def perda(dv=None, ef=None, mo=None, comp=None):
    s, mat = "IND", "A1"; Mt = PS.MATERIAIS[mat]; a = PS.SOLO[s]
    site = dict(latitude=PS.SITIOS[s]["lat"], altitude=0, soil_class=-1, asw_i=a, asw_min=0.0, asw_max=a, **{"from": "2016-01", "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=Mt["FR_ref"], stems_n=10000 / 9, biom_stem=Mt["WS0"], biom_root=Mt["WR0"], biom_foliage=Mt["WF0"])
    o = PS.run_3pg_pjs(site, sp, PS.RE._clima(s), PS.params(mat), defoliation_events=dv, efficiency_events=ef, mortality_events=mo, compensation=comp)
    o["idade"] = (o.age * 12).round().astype(int); return o.set_index("idade")
c = perda(); dv = {"2017-01": .95, "2020-01": .95}; ef = {PS.mes(y, 1 + i): .6 for y in (2017, 2020) for i in range(4)}; mo = {"2017-01": .25}
t = perda(dv, ef, mo, PS.COMP); L = lambda o: 100 * (1 - o.volume[84] / c.volume[84])
R["teste_autor"] = dict(combinado=L(t), so_desfolha=L(perda(dv, comp=PS.COMP)), so_eficiencia=L(perda(ef=ef)), so_mortalidade=L(perda(mo=mo)),
                        vol_ctrl=float(c.volume[84]), vol_trat=float(t.volume[84]), arv_trat=float(t.stems_n[84]),
                        dap_ctrl=float(c.dbh[84]), dap_trat=float(t.dbh[84]),
                        vol_arvore_rel=100 * ((t.volume[84] / t.stems_n[84]) / (c.volume[84] / c.stems_n[84]) - 1),
                        iaf_jan2021_ctrl=float(c.lai[72]), iaf_jan2021_trat=float(t.lai[72]),
                        npp_jan2021_ctrl=float(c.npp_f[72]), npp_jan2021_trat=float(t.npp_f[72]))
R["teste_autor"]["soma_isolados"] = R["teste_autor"]["so_desfolha"] + R["teste_autor"]["so_eficiencia"] + R["teste_autor"]["so_mortalidade"]
R["teste_autor"]["cresc_4m_pos_pulso1_ctrl"] = float(c.volume[28] - c.volume[24]); R["teste_autor"]["cresc_4m_pos_pulso1_trat"] = float(t.volume[28] - t.volume[24])
R["teste_autor"]["cresc_4m_pos_pulso2_ctrl"] = float(c.volume[64] - c.volume[60]); R["teste_autor"]["cresc_4m_pos_pulso2_trat"] = float(t.volume[64] - t.volume[60])
R["teste_autor"]["cresc_72_84_ctrl"] = float(c.volume[84] - c.volume[72]); R["teste_autor"]["cresc_72_84_trat"] = float(t.volume[84] - t.volume[72])

# (4) k-fold
CLI = {}
for s in PS.SITIOS:
    m = clima_mensal(s); CLI[s] = dict(T_media=m.tmp_ave.mean(), chuva_anual=m.groupby("year").prcp.sum().mean(), meses_secos=int((m.groupby("month").prcp.mean() < 50).sum()))
for k in ["T_media", "chuva_anual", "meses_secos"]:
    A[k] = A.sitio.map({s: CLI[s][k] for s in CLI})
A["calibrada"] = (A.versao == "calibrada").astype(float); A["anual"] = (A.freq == "PA").astype(float); A["C5"] = (A.material == "C5").astype(float)
A["solo"] = A.sitio.map(PS.SOLO)
X = A[["d", "anual", "epoca", "r", "m", "calibrada", "C5", "T_media", "chuva_anual", "meses_secos", "solo"]].to_numpy(); y = A.perda_volume.to_numpy()
met = lambda y, yh: dict(R2=float(1 - ((yh - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()), RQEM_pp=float(np.sqrt(((yh - y) ** 2).mean())))
KF = {}
for nome, cv, grp in [("k-fold 10 × 3", RepeatedKFold(n_splits=10, n_repeats=3, random_state=SEED), None), ("deixa um local de fora", LeaveOneGroupOut(), A.sitio.to_numpy())]:
    ys, yh = [], []
    for tr, te in cv.split(X, y, grp):
        m = RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=SEED, n_jobs=2).fit(X[tr], y[tr])
        ys.append(y[te]); yh.append(m.predict(X[te]))
    KF[nome] = met(np.concatenate(ys), np.concatenate(yh))
yc = (y < 0).astype(int); acc, bacc = [], []
for tr, te in RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=SEED).split(X, yc):
    m = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=SEED, n_jobs=2, class_weight="balanced").fit(X[tr], yc[tr]); p = m.predict(X[te])
    acc.append((p == yc[te]).mean()); bacc.append(((p[yc[te] == 1] == 1).mean() + (p[yc[te] == 0] == 0).mean()) / 2 if yc[te].sum() else np.nan)
KF["classificacao ganho × perda (k-fold estratificado 10 × 3)"] = dict(acuracia=float(np.mean(acc)) * 100, acuracia_balanceada=float(np.nanmean(bacc)) * 100,
                                                                     frac_ganho=float(yc.mean() * 100))
mfull = RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=SEED, n_jobs=2).fit(X, y)
pi = permutation_importance(mfull, X, y, n_repeats=5, random_state=SEED, n_jobs=2)
nomes = ["intensidade d", "pulsos anuais", "época", "perda de eficiência r", "mortalidade m", "fisiologia calibrada", "material C5", "T média", "chuva anual", "meses secos", "CAD"]
imp = pd.Series(pi.importances_mean, index=nomes); imp = 100 * imp / imp.sum()
R["kfold"] = KF; R["importancia_pct"] = imp.sort_values(ascending=False).round(1).to_dict()
json.dump(R, open(OUT / "resumo_possibilidades.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps(R, indent=1, ensure_ascii=False, default=float))
