#!/usr/bin/env python3
"""Validação cruzada ampliada do METAMODELO da resposta à desfolha (não do 3-PG contra o campo).
Algoritmos: regressão linear (com interações de 2ª ordem), Random Forest, Gradient Boosting e
MLP (50, 30; ReLU; como em Castro et al.). Esquemas: k-fold 7 repetido 10×; leave-one-site-out;
leave-one-material-out. Métricas por fold: R², r(yŷ), RQEM %, viés %."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneGroupOut, RepeatedKFold
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

S = Path(__file__).resolve().parent / "saida"; OUT = S / "estatisticas"
SEED = 20261030
I = pd.read_csv(S / "indicadores_por_tratamento.csv")
I = I[I.experimento.isin(["E1-E6", "LOCAL"]) & I.apto_analise_principal].copy()
I["Fn"] = I.nivel_FR.str[1:].astype(int)
NUM = ["desfolha", "n_eventos", "mes_evento", "asw_max", "Fn"]; CAT = ["sitio", "material"]


def prep(scale=True):
    return ColumnTransformer([("num", StandardScaler() if scale else "passthrough", NUM),
                              ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])


MODELOS = {
    "Linear + interações 2ª ordem": lambda: make_pipeline(prep(), PolynomialFeatures(2, include_bias=False), LinearRegression()),
    "Random Forest": lambda: make_pipeline(prep(False), RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=SEED, n_jobs=2)),
    "Gradient Boosting": lambda: make_pipeline(prep(False), GradientBoostingRegressor(n_estimators=500, max_depth=3, learning_rate=0.05, random_state=SEED)),
    "RNA MLP (50, 30) ReLU": lambda: make_pipeline(prep(), MLPRegressor(hidden_layer_sizes=(50, 30), activation="relu", max_iter=3000,
                                                                      early_stopping=True, random_state=SEED)),
}


def met(y, yh):
    e = yh - y
    return dict(R2=1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(),
                r=np.corrcoef(y, yh)[0, 1] if np.std(yh) > 0 else np.nan,
                RQEM_pct=100 / y.mean() * np.sqrt((e ** 2).mean()), vies_pct=100 * e.mean() / y.mean())


linhas = []
for alvo in ["perda_volume_k72", "recup_rel95_meses_ev1"]:
    d = I[I[alvo].notna()].reset_index(drop=True); X = d[NUM + CAT]; y = d[alvo].to_numpy()
    esquemas = {"k-fold 7 × 10 repetições": (RepeatedKFold(n_splits=7, n_repeats=10, random_state=SEED), None),
                "deixa um sítio de fora": (LeaveOneGroupOut(), d.sitio),
                "deixa um material de fora": (LeaveOneGroupOut(), d.material)}
    for nome_m, fab in MODELOS.items():
        for nome_e, (cv, grp) in esquemas.items():
            for k, (tr, te) in enumerate(cv.split(X, y, grp)):
                m = fab().fit(X.iloc[tr], y[tr])
                r = met(y[te], m.predict(X.iloc[te]))
                r.update(resposta=alvo, modelo=nome_m, esquema=nome_e, fold=k,
                         grupo_testado=(grp.iloc[te].iloc[0] if grp is not None else ""))
                linhas.append(r)
F = pd.DataFrame(linhas); F.to_csv(OUT / "D_kfold_por_fold.csv", index=False)
RES = (F.groupby(["resposta", "modelo", "esquema"])
         .agg(folds=("R2", "size"), R2_media=("R2", "mean"), R2_dp=("R2", "std"), R2_min=("R2", "min"),
              r_media=("r", "mean"), RQEM_media=("RQEM_pct", "mean"), RQEM_dp=("RQEM_pct", "std"),
              RQEM_max=("RQEM_pct", "max")).round(3).reset_index())
RES.to_csv(OUT / "D_kfold_resumo.csv", index=False)
G = F[F.esquema != "k-fold 7 × 10 repetições"].pivot_table(index=["resposta", "modelo", "esquema", "grupo_testado"],
                                                           values=["R2", "RQEM_pct", "vies_pct"]).round(3)
G.to_csv(OUT / "D_kfold_por_grupo.csv")
pd.set_option("display.width", 250)
print(RES.to_string()); print(G.to_string())
