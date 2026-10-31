"""Figura da Random Forest para o TCC (perda de volume aos 84 meses): importância global, por local e previsão com um local fora."""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict
S = Path(__file__).resolve().parent / "saida"; F = S / "figuras"; SEED = 20261030
plt.rcParams.update({"font.family": "serif", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": .6})
I = pd.read_csv(S / "indicadores_por_tratamento.csv")
I = I[I.experimento.isin(["E1-E6", "LOCAL"]) & I.apto_analise_principal].copy(); I["Fn"] = I.nivel_FR.str[1:].astype(int)
X = pd.get_dummies(I[["desfolha", "n_eventos", "mes_evento", "asw_max", "Fn", "sitio", "material"]], columns=["sitio", "material"], dtype=float)
y = I.perda_volume_k72.to_numpy()
rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=SEED, n_jobs=4)
ys = cross_val_predict(rf, X, y, cv=LeaveOneGroupOut(), groups=I.sitio)
imp = pd.read_csv(S / "estatisticas/C_importancia_variaveis.csv")
ordem = ["intensidade", "frequência", "época", "local", "material genético", "água (ASWmax)", "fertilidade (FR)"]
fig, ax = plt.subplots(1, 3, figsize=(13, 4.0), gridspec_kw=dict(width_ratios=[1, 1.25, 1]))
for a, alvo, tit in [(ax[0], "recup_rel95_meses_ev1", "(a) Recuperação foliar relativa, 3 locais")]:
    s = imp[(imp.escopo == "3 locais") & (imp.resposta == alvo)].set_index("variavel").loc[ordem[::-1]]
    a.barh(s.index, s.importancia_relativa_pct, color="#4d4d4d", edgecolor="white"); a.grid(axis="y", visible=False)
    for i, v in enumerate(s.importancia_relativa_pct):
        a.text(v + 1, i, f"{v:.1f}".replace(".", ","), va="center", fontsize=8)
    a.set_xlim(0, 80); a.set_xlabel("Importância relativa por permutação (%)"); a.set_title(tit, fontsize=10)
P = imp[imp.resposta == "perda_volume_k72"].pivot_table(index="variavel", columns="escopo", values="importancia_relativa_pct").loc[ordem[::-1]]
cores = {"3 locais": "#4d4d4d", "IND": "#2a78d6", "TB": "#eb6834", "IMP": "#1baf7a"}
h = 0.2
for k, esc in enumerate(["3 locais", "IND", "TB", "IMP"]):
    ax[1].barh(np.arange(len(P)) + (k - 1.5) * h, P[esc], height=h, color=cores[esc], label=esc)
ax[1].set_yticks(range(len(P))); ax[1].set_yticklabels(P.index); ax[1].grid(axis="y", visible=False)
ax[1].set_xlabel("Importância relativa por permutação (%)"); ax[1].set_title("(b) Perda de volume: 3 locais e cada local", fontsize=10)
ax[1].legend(frameon=False, fontsize=8, loc="lower right")
mk = {"IND": "o", "TB": "s", "IMP": "^"}
for s_, m_ in mk.items():
    sel = (I.sitio == s_).to_numpy()
    ax[2].scatter(y[sel], ys[sel], s=9, marker=m_, facecolors="none", edgecolors=cores[s_], linewidths=.6, label=f"{s_} fora do treino")
lim = [0, max(y.max(), ys.max()) * 1.05]; ax[2].plot(lim, lim, color="#999", lw=1)
ax[2].set_xlim(lim); ax[2].set_ylim(lim); ax[2].set_xlabel("Perda simulada pelo 3-PG (%)"); ax[2].set_ylabel("Perda prevista pela RF (%)")
ax[2].set_title("(c) RF com um local fora do treino", fontsize=10); ax[2].legend(frameon=False, fontsize=7.5)
fig.tight_layout(); fig.savefig(F / "F8_random_forest.png", dpi=220); plt.close(fig)
print("ok n =", len(y), "r LOSO =", round(np.corrcoef(y, ys)[0, 1], 3))
