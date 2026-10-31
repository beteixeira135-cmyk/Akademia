#!/usr/bin/env python3
"""Sensibilidade (decomposição fatorial determinística + Morris), respostas às perguntas 1–8 e figuras.
Nenhum teste de significância estatística é feito: o delineamento é determinístico, sem réplicas."""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
S = AQUI / "saida"; F = S / "figuras"; F.mkdir(exist_ok=True)
from run_experimentos import rodar, linha, fr_nivel  # noqa: E402
import run_experimentos as RE  # noqa: E402
from clones import params, MATERIAIS  # noqa: E402

R = pd.read_csv(S / "indicadores_por_tratamento.csv")
E = R[R.experimento == "E1-E6"].copy()
E["W"] = E.nivel_agua; E["Fn"] = E.nivel_FR.str[1:].astype(int)
ANS = {}

# cores (paleta categórica validada: slots 1–4) e rampa ordinal azul para intensidades
CAT = {"A1": "#2a78d6", "C5": "#eb6834", "C2": "#1baf7a", "C4": "#eda100"}
SIT = {"IND": "#2a78d6", "TB": "#eb6834", "IMP": "#1baf7a"}
DEF = {0.0: "#52514e", 0.25: "#86b6ef", 0.50: "#3987e5", 0.95: "#184f95"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6, "lines.linewidth": 2,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "axes.edgecolor": "#9a998f"})


def decomp(df, y, fatores):
    """Decomposição ortogonal da soma de quadrados (delineamento balanceado completo)."""
    d = df.dropna(subset=[y]); mu = d[y].mean(); sst = ((d[y] - mu) ** 2).sum()
    out = {}
    for f in fatores:
        out[f] = (d.groupby(f)[y].transform("mean") - mu).pow(2).sum()
    for i, a in enumerate(fatores):
        for b in fatores[i + 1:]:
            ab = d.groupby([a, b])[y].transform("mean")
            out[f"{a}×{b}"] = (ab - d.groupby(a)[y].transform("mean") - d.groupby(b)[y].transform("mean") + mu).pow(2).sum()
    out["ordem≥3"] = sst - sum(out.values())
    return {k: 100 * v / sst for k, v in out.items()}, sst


# ---------- Decomposição por sítio (d = 50 %, pulso único, perda de volume aos 84 meses de idade) ----------
dec = []
for s in ["IND", "TB", "IMP"]:
    for alvo in ["perda_volume_k72", "recup_rel95_meses_ev1", "perda_NPP_acum_pct"]:
        sub = E[(E.sitio == s) & (E.desfolha == 0.5) & (E.calendario == "P1") & E.apto_analise_principal]
        pct, sst = decomp(sub, alvo, ["material", "W", "Fn"])
        dec.append(dict(sitio=s, resposta=alvo, SQ_total=sst, **{k: round(v, 2) for k, v in pct.items()}))
DEC = pd.DataFrame(dec); DEC.to_csv(S / "sensibilidade_decomposicao_fatorial.csv", index=False)

# ---------- Q1/Q4: água vs fertilidade por material (E3, 4×4) ----------
q1 = []
for (s, m), sub in E[(E.desfolha == 0.5) & (E.calendario == "P1") & E.apto_analise_principal].groupby(["sitio", "material"]):
    pct, _ = decomp(sub, "perda_volume_k72", ["W", "Fn"])
    rng = sub.perda_volume_k72.max() - sub.perda_volume_k72.min()
    q1.append(dict(sitio=s, material=m, pct_SQ_agua=pct["W"], pct_SQ_FR=pct["Fn"], pct_SQ_interacao=pct["W×Fn"],
                   amplitude_perda_pp=rng, perda_min=sub.perda_volume_k72.min(), perda_max=sub.perda_volume_k72.max()))
Q1 = pd.DataFrame(q1).round(2); Q1.to_csv(S / "Q1_Q4_agua_vs_fertilidade.csv", index=False)
ANS["Q1"] = Q1.to_dict("records")

# ---------- Q2: água × velocidade de recuperação (FR de referência) ----------
Q2 = (E[(E.Fn == 100) & (E.calendario == "P1") & E.apto_analise_principal]
      .pivot_table(index=["sitio", "material", "desfolha"], columns="W",
                   values=["recup_abs_meses_ev1", "recup_rel95_meses_ev1"]).round(1))
Q2.to_csv(S / "Q2_agua_recuperacao.csv"); ANS["Q2_csv"] = "Q2_agua_recuperacao.csv"

# ---------- Q3: fertilidade × compensação (E2 exploratório + E3) ----------
X = R[R.experimento == "E2x"]
Q3 = X.pivot_table(index=["sitio", "material"], columns="FR", values=["perda_volume_k72", "recup_rel95_meses_ev1",
                   "meses_NPP_trat_maior_ctrl"]).round(2)
Q3.to_csv(S / "Q3_FR_exploratorio.csv")

# ---------- Q5: material com menor perda por clima ----------
Q5 = (E[(E.desfolha == 0.5) & (E.calendario == "P1")]
      .groupby(["sitio", "material"]).agg(perda_vol_media=("perda_volume_k72", "mean"),
                                          perda_vol_min=("perda_volume_k72", "min"),
                                          perda_vol_max=("perda_volume_k72", "max"),
                                          apto=("apto_analise_principal", "first")).round(2).reset_index())
Q5.to_csv(S / "Q5_material_por_clima.csv", index=False)

# ---------- Q6: recorrente vs único ----------
p = E.pivot_table(index=["sitio", "material", "W", "Fn", "desfolha"], columns="calendario",
                  values=["perda_NPP_acum_pct", "perda_volume_k72", "perda_volume_k84"])
Q6 = pd.DataFrame({"pares": [len(p)],
                   "P2_maior_P1_NPPacum_%pares": [100 * (p[("perda_NPP_acum_pct", "P2")] > p[("perda_NPP_acum_pct", "P1")]).mean()],
                   "razao_mediana_volume_k72_P2/P1": [(p[("perda_volume_k72", "P2")] / p[("perda_volume_k72", "P1")]).median()],
                   "razao_min": [(p[("perda_volume_k72", "P2")] / p[("perda_volume_k72", "P1")]).min()],
                   "razao_max": [(p[("perda_volume_k72", "P2")] / p[("perda_volume_k72", "P1")]).max()]}).round(3)
Q6.to_csv(S / "Q6_recorrente_vs_unico.csv", index=False)

# ---------- Q8: Morris (efeitos elementares) — parâmetros do material A1, IND, W100/F100 ----------
PARS = ["alphaCx", "y", "k", "SLA0", "SLA1", "tSLA", "gammaF1", "gammaF0", "tgammaF", "pRx", "pRn", "pFS2", "pFS20",
        "aWs", "nWs", "Topt", "Tmax", "CoeffCond", "MaxCond", "fracBB1", "MaxAge"]
base = params("A1")
lo = {p_: base[p_] * 0.9 for p_ in PARS}; hi = {p_: base[p_] * 1.1 for p_ in PARS}
rng = np.random.default_rng(20261030); r_traj, niveis = 25, 4
delta = niveis / (2 * (niveis - 1))
import threepg_pjs as T  # noqa: E402
from clima import clima_mensal  # noqa: E402
CL = clima_mensal("IND")


def avalia(x):
    P = dict(base); P.update({p_: lo[p_] + x[i] * (hi[p_] - lo[p_]) for i, p_ in enumerate(PARS)})
    site = dict(latitude=-19.0389, altitude=0, soil_class=-1, asw_i=190.6, asw_min=0, asw_max=190.6,
                **{"from": "2016-01", "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=0.8, stems_n=10000 / 9, biom_stem=5.47, biom_root=1.09, biom_foliage=2.07)
    c = T.run_3pg_pjs(site, sp, CL, P); t = T.run_3pg_pjs(site, sp, CL, P, defoliation_events={"2017-01": 0.5})
    vc, vt = c.volume.iloc[72], t.volume.iloc[72]
    ab = next((m for m in range(12, 85) if t.biom_foliage.iloc[m] / c.biom_foliage.iloc[m] >= 0.95), np.nan) - 12
    return np.array([100 * (1 - vt / vc), vc, ab])


EE = {p_: [] for p_ in PARS}
grade = np.arange(niveis) / (niveis - 1)
for _ in range(r_traj):
    x = rng.choice(grade[:niveis // 2], size=len(PARS)).astype(float)
    y0 = avalia(x)
    for i in rng.permutation(len(PARS)):
        x2 = x.copy(); x2[i] = x[i] + delta
        y1 = avalia(x2); EE[PARS[i]].append((y1 - y0) / delta); x, y0 = x2, y1
MOR = []
for p_ in PARS:
    a = np.array(EE[p_])
    for j, nome in enumerate(["perda_volume_k72_pp", "volume_ctrl_k72_m3ha", "recup_rel95_meses"]):
        MOR.append(dict(parametro=p_, resposta=nome, mu_estrela=np.nanmean(np.abs(a[:, j])), sigma=np.nanstd(a[:, j]),
                        mu=np.nanmean(a[:, j])))
MOR = pd.DataFrame(MOR).round(4); MOR.to_csv(S / "sensibilidade_morris_A1_IND.csv", index=False)

# ---------- FIGURAS ----------
D = pd.read_csv(S / "mensal.csv.gz", usecols=["id", "mes_ref", "idade_meses", "biom_foliage", "lai", "biom_stem", "volume",
                                               "npp_f", "asw", "dbh"])
D["mes_ref"] = D.mes_ref.round().astype(int)


def serie(pid):
    return D[D.id == pid]


# F1 — trajetórias do caso principal
fig, ax = plt.subplots(2, 3, figsize=(11, 6), sharex=True)
for cal, linha_ax in (("P1", 0), ("P2", 1)):
    for d in [0.0, 0.25, 0.50, 0.95]:
        pid = f"IND_A1_W100_F100_D{int(d*100):02d}_{cal if d > 0 else 'CTRL'}"
        g = serie(pid); lab = "controle" if d == 0 else f"{int(d*100)} %"
        for j, (v, tit) in enumerate([("biom_foliage", "Wf (t/ha)"), ("biom_stem", "Ws (t/ha)"), ("asw", "ASW (mm)")]):
            ax[linha_ax, j].plot(g.mes_ref, g[v], color=DEF[d], label=lab, lw=2 if d else 1.6, ls="-" if d else "--")
            ax[linha_ax, j].set_title(f"{tit} — {'pulso único (mês 12)' if cal=='P1' else 'pulsos nos meses 12 e 48'}", fontsize=8.5)
for a in ax[1]:
    a.set_xlabel("mês da simulação (idade = 12 + mês)")
ax[0, 0].legend(frameon=False, title="desfolha", fontsize=8)
for a in ax.flat:
    for e in (12, 48):
        a.axvline(e, color="#c3c2b7", lw=0.8, zorder=0)
fig.suptitle("Indianópolis · E. urophylla A1 (Caldeira 2020) · solo de referência (ASWmax 190,6 mm, FR 0,8)", fontsize=10)
fig.tight_layout(); fig.savefig(F / "F1_trajetorias_IND_A1.png", dpi=200); plt.close(fig)

# F2 — matriz água × FR (perda de volume aos 84 meses de idade, d=50 %, P1) por material, IND
fig, ax = plt.subplots(1, 4, figsize=(12, 3.2))
for a, m in zip(ax, ["A1", "C5", "C2", "C4"]):
    sub = E[(E.sitio == "IND") & (E.material == m) & (E.desfolha == 0.5) & (E.calendario == "P1")]
    Z = sub.pivot_table(index="Fn", columns="W", values="perda_volume_k72").sort_index(ascending=False)
    im = a.imshow(Z.values, cmap="Blues", vmin=0, vmax=E[(E.sitio == "IND") & (E.desfolha == 0.5) & (E.calendario == "P1")].perda_volume_k72.max())
    for i in range(4):
        for j in range(4):
            a.text(j, i, f"{Z.values[i, j]:.1f}", ha="center", va="center", fontsize=7.5,
                   color="#0b0b0b" if Z.values[i, j] < 0.6 * im.get_clim()[1] else "#fcfcfb")
    a.set_xticks(range(4)); a.set_xticklabels([f"W{w}" for w in Z.columns]); a.set_yticks(range(4))
    a.set_yticklabels([f"F{f}" for f in Z.index]); a.set_title(m); a.grid(False)
fig.colorbar(im, ax=ax, label="perda de volume (%)", shrink=0.8)
fig.suptitle("Indianópolis · desfolha 50 % (pulso único) · perda relativa de volume aos 84 meses de idade", fontsize=10)
fig.savefig(F / "F2_matriz_agua_FR_IND.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# F3 — perda de volume por intensidade, material e sítio (solo de referência, P1 e P2)
fig, ax = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)
for a, s in zip(ax, ["IND", "TB", "IMP"]):
    sub = E[(E.sitio == s) & (E.W == 100) & (E.Fn == 100)]
    for m in ["A1", "C5", "C2", "C4"]:
        for cal, ls in (("P1", "-"), ("P2", ":")):
            g = sub[(sub.material == m) & (sub.calendario == cal)].sort_values("desfolha")
            a.plot(g.desfolha * 100, g.perda_volume_k72, ls=ls, marker="o", ms=4, color=CAT[m],
                   label=f"{m} {cal}" if s == "IND" else None, alpha=0.45 if (s == "IMP" and m == "A1") else 1)
    a.set_title(f"{s}" + (" (A1 = diagnóstico de extrapolação)" if s == "IMP" else ""), fontsize=9)
    a.set_xlabel("desfolha (%)")
ax[0].set_ylabel("perda de volume aos 84 meses (%)"); ax[0].legend(frameon=False, fontsize=7, ncol=2)
fig.suptitle("Solo de referência (W100, F100) · linha cheia = pulso único; pontilhada = pulsos 12 e 48", fontsize=10)
fig.tight_layout(); fig.savefig(F / "F3_perda_volume_sitios_materiais.png", dpi=200); plt.close(fig)

# F4 — recuperação relativa vs água
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
for a, d in zip(ax, [0.5, 0.95]):
    sub = E[(E.sitio == "IND") & (E.Fn == 100) & (E.calendario == "P1") & (E.desfolha == d)]
    for m in ["A1", "C5", "C2", "C4"]:
        g = sub[sub.material == m].sort_values("W")
        a.plot(g.W, g.recup_rel95_meses_ev1, marker="o", color=CAT[m], label=m)
    a.set_title(f"Indianópolis · desfolha {int(d*100)} %"); a.set_xlabel("água (% de ASWmax_ref)")
ax[0].set_ylabel("meses até Wf ≥ 95 % do controle"); ax[0].legend(frameon=False)
fig.tight_layout(); fig.savefig(F / "F4_recuperacao_vs_agua.png", dpi=200); plt.close(fig)

# F5 — Morris
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, resp, tit in zip(ax, ["perda_volume_k72_pp", "volume_ctrl_k72_m3ha"], ["perda de volume (p.p.)", "volume do controle (m³/ha)"]):
    s = MOR[MOR.resposta == resp]
    a.scatter(s.mu_estrela, s.sigma, color="#2a78d6", s=24, edgecolor="#fcfcfb", linewidth=1)
    for _, r in s.nlargest(7, "mu_estrela").iterrows():
        a.annotate(r.parametro, (r.mu_estrela, r.sigma), fontsize=7.5, xytext=(3, 3), textcoords="offset points")
    a.set_xlabel("μ* (efeito médio absoluto)"); a.set_ylabel("σ (não linearidade/interação)"); a.set_title(tit)
fig.suptitle("Morris · A1, Indianópolis, W100/F100, desfolha 50 % · parâmetros variados ±10 %", fontsize=10)
fig.tight_layout(); fig.savefig(F / "F5_morris.png", dpi=200); plt.close(fig)

# F6 — decomposição
fig, ax = plt.subplots(figsize=(8, 3.2))
sub = DEC[DEC.resposta == "perda_volume_k72"].set_index("sitio")[["material", "W", "Fn", "material×W", "material×Fn", "W×Fn", "ordem≥3"]]
left = np.zeros(len(sub)); cores = ["#2a78d6", "#eb6834", "#1baf7a", "#86b6ef", "#f4b09a", "#9fdcc3", "#c3c2b7"]
for c, col in zip(sub.columns, cores):
    ax.barh(sub.index, sub[c], left=left, color=col, label=c, edgecolor="#fcfcfb", linewidth=2); left += sub[c].values
ax.set_xlabel("% da soma de quadrados da perda de volume (84 meses)"); ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3))
ax.set_title("Desfolha 50 %, pulso único · contribuição de cada fator (decomposição determinística)", fontsize=9)
fig.tight_layout(); fig.savefig(F / "F6_decomposicao.png", dpi=200); plt.close(fig)

json.dump({"Q6": Q6.to_dict("records")}, open(S / "respostas_resumo.json", "w"), indent=2, ensure_ascii=False)
print(DEC.round(1).to_string()); print(Q1.to_string()); print(Q5.to_string()); print(Q6.to_string())
print(MOR[MOR.resposta == "perda_volume_k72_pp"].sort_values("mu_estrela", ascending=False).head(8).to_string())
print(MOR[MOR.resposta == "volume_ctrl_k72_m3ha"].sort_values("mu_estrela", ascending=False).head(6).to_string())
