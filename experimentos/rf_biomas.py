#!/usr/bin/env python3
"""Metamodelo Random Forest no bloco por bioma (6 locais), versões original e calibrada.
Esquemas: k-fold 7 × 10 e deixa um local de fora (6 grupos). Dois conjuntos de variáveis:
  (a) como no TCC: intensidade, nº de eventos, mês do evento, ASWmax, FR, local (categórico), material;
  (b) com o clima descrito por números em vez do nome do local (temperatura média, chuva anual, meses com
      chuva média < 50 mm, ASWmax), para testar se a transferência para um clima não visto melhora.
Importância por permutação com 6 locais. Só tratamentos aptos (A1 em IMP, ALM e ARA = diagnóstico, fora)."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import LeaveOneGroupOut, RepeatedKFold

AQUI = Path(__file__).resolve().parent; sys.path.insert(0, str(AQUI))
from clima import SITIOS, clima_mensal  # noqa: E402
B = AQUI / "saida" / "biomas"; SEED = 20261030
CLI = {}
for s in SITIOS:
    m = clima_mensal(s)
    CLI[s] = dict(T_media=m.tmp_ave.mean(), chuva_anual=m.groupby("year").prcp.sum().mean(),
                  meses_secos=int((m.groupby("month").prcp.mean() < 50).sum()))
pd.DataFrame(CLI).T.round(2).to_csv(B / "clima_resumo_locais.csv")


def preparar(v):
    I = pd.read_csv(B / f"indicadores_{v}.csv"); I = I[I.apto_analise_principal].copy()
    I["Fn"] = I.nivel_FR.str[1:].astype(int)
    for k in ["T_media", "chuva_anual", "meses_secos"]:
        I[k] = I.sitio.map({s: CLI[s][k] for s in CLI})
    return I


BASE = ["desfolha", "n_eventos", "mes_evento", "asw_max", "Fn"]
CONJ = {"(a) local categórico": BASE + ["sitio", "material"], "(b) clima numérico": BASE + ["T_media", "chuva_anual", "meses_secos", "material"]}


def X_(d, cols):
    return pd.get_dummies(d[cols], columns=[c for c in ["sitio", "material"] if c in cols], dtype=float)


def met(y, yh):
    e = yh - y
    return dict(R2=1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(), RQEM_pct=100 / y.mean() * np.sqrt((e ** 2).mean()),
                vies_pct=100 * e.mean() / y.mean())


rf = lambda: RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=SEED, n_jobs=8)
linhas, imps = [], []
for v in ["original", "calibrado"]:
    I = preparar(v)
    for alvo in ["perda_volume_k72", "recup_rel95_meses_ev1"]:
        d = I[I[alvo].notna()].reset_index(drop=True); y = d[alvo].to_numpy()
        for nome_c, cols in CONJ.items():
            X = X_(d, cols)
            for nome_e, cv, grp in [("k-fold 7 × 10", RepeatedKFold(n_splits=7, n_repeats=10, random_state=SEED), None),
                                    ("deixa um local de fora", LeaveOneGroupOut(), d.sitio)]:
                for k, (tr, te) in enumerate(cv.split(X, y, grp)):
                    if nome_e.startswith("k-fold") and k >= 14:  # 2 repetições bastam para o resumo (custo)
                        break
                    m = rf().fit(X.iloc[tr], y[tr]); r = met(y[te], m.predict(X.iloc[te]))
                    r.update(versao=v, resposta=alvo, variaveis=nome_c, esquema=nome_e,
                             local_testado=d.sitio.iloc[te].iloc[0] if grp is not None else "")
                    linhas.append(r)
        # importância (conjunto a, 6 locais)
        X = X_(d, CONJ["(a) local categórico"]); m = rf().fit(X, y)
        pi = pd.Series(permutation_importance(m, X, y, n_repeats=5, random_state=SEED, n_jobs=8).importances_mean, index=X.columns)
        g = {"intensidade": ["desfolha"], "frequência": ["n_eventos"], "época": ["mes_evento"], "água (ASWmax)": ["asw_max"],
             "fertilidade (FR)": ["Fn"], "local": [c for c in X if c.startswith("sitio_")], "material": [c for c in X if c.startswith("material_")]}
        tot = sum(max(pi[c].sum(), 0) for c in g.values())
        for k_, c in g.items():
            imps.append(dict(versao=v, resposta=alvo, variavel=k_, importancia_pct=100 * max(pi[c].sum(), 0) / tot))
F = pd.DataFrame(linhas); F.to_csv(B / "rf_por_fold.csv", index=False)
R = F.groupby(["versao", "resposta", "variaveis", "esquema"]).agg(R2=("R2", "mean"), RQEM=("RQEM_pct", "mean"),
                                                                  RQEM_max=("RQEM_pct", "max")).round(3).reset_index()
R.to_csv(B / "rf_resumo.csv", index=False)
G = F[F.esquema != "k-fold 7 × 10"].pivot_table(index=["versao", "resposta", "variaveis", "local_testado"], values=["R2", "RQEM_pct", "vies_pct"]).round(2)
G.to_csv(B / "rf_por_local.csv")
P = pd.DataFrame(imps).round(1); P.to_csv(B / "rf_importancia.csv", index=False)
pd.set_option("display.width", 220)
print(R.to_string()); print(G.to_string()); print(P.pivot_table(index="variavel", columns=["versao", "resposta"], values="importancia_pct").to_string())
