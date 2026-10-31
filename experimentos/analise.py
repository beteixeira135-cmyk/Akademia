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
E["W"] = pd.to_numeric(E.nivel_agua).astype(int); E["Fn"] = E.nivel_FR.str[1:].astype(int)
LOC = R[(R.experimento == "LOCAL")].copy(); LOC["Fn"] = LOC.nivel_FR.str[1:].astype(int)
ANS = {}

# cores (paleta categórica validada: slots 1–4) e rampa ordinal azul para intensidades
DEFOL_ = [0.0, 0.25, 0.50, 0.95]
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

# ---------- Q8: Morris (efeitos elementares) — material A1, solo local de cada sítio, F100, d = 50 % ----------
PARS = ["alphaCx", "y", "k", "SLA0", "SLA1", "tSLA", "gammaF1", "gammaF0", "tgammaF", "pRx", "pRn", "pFS2", "pFS20",
        "aWs", "nWs", "Topt", "Tmax", "CoeffCond", "MaxCond", "fracBB1", "MaxAge"]
import threepg_pjs as T  # noqa: E402
from clima import clima_mensal, SITIOS  # noqa: E402
from multiprocessing import Pool  # noqa: E402


def morris_sitio(sitio, r_traj=25, niveis=4):
    base = params("A1"); CL = clima_mensal(sitio); asw = RE.SOLO_LOCAL[sitio]
    lo = {p_: base[p_] * 0.9 for p_ in PARS}; hi = {p_: base[p_] * 1.1 for p_ in PARS}
    rng = np.random.default_rng(20261030); delta = niveis / (2 * (niveis - 1))
    site = dict(latitude=SITIOS[sitio]["lat"], altitude=0, soil_class=-1, asw_i=asw, asw_min=0, asw_max=asw,
                **{"from": "2016-01", "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=0.8, stems_n=10000 / 9, biom_stem=5.47, biom_root=1.09, biom_foliage=2.07)

    def avalia(x):
        P = dict(base); P.update({p_: lo[p_] + x[i] * (hi[p_] - lo[p_]) for i, p_ in enumerate(PARS)})
        c = T.run_3pg_pjs(site, sp, CL, P); t = T.run_3pg_pjs(site, sp, CL, P, defoliation_events={"2017-01": 0.5})
        vc, vt = c.volume.iloc[72], t.volume.iloc[72]
        ab = next((m for m in range(12, 85) if t.biom_foliage.iloc[m] / c.biom_foliage.iloc[m] >= 0.95), np.nan) - 12
        return np.array([100 * (1 - vt / vc), vc, ab])
    EE = {p_: [] for p_ in PARS}; grade = np.arange(niveis) / (niveis - 1)
    for _ in range(r_traj):
        x = rng.choice(grade[:niveis // 2], size=len(PARS)).astype(float); y0 = avalia(x)
        for i in rng.permutation(len(PARS)):
            x2 = x.copy(); x2[i] = x[i] + delta; y1 = avalia(x2); EE[PARS[i]].append((y1 - y0) / delta); x, y0 = x2, y1
    out = []
    for p_ in PARS:
        a_ = np.array(EE[p_])
        for j, nome in enumerate(["perda_volume_k72_pp", "volume_ctrl_k72_m3ha", "recup_rel95_meses"]):
            out.append(dict(sitio=sitio, parametro=p_, resposta=nome, mu_estrela=np.nanmean(np.abs(a_[:, j])),
                            sigma=np.nanstd(a_[:, j]), mu=np.nanmean(a_[:, j])))
    return out


with Pool(3) as pool:
    MOR = pd.DataFrame(sum(pool.map(morris_sitio, ["IND", "TB", "IMP"]), [])).round(4)
MOR.to_csv(S / "sensibilidade_morris_A1_3sitios.csv", index=False)

# ---------- FIGURAS ----------
plt.rcParams.update({"font.family": "serif"})
SITN = {"IND": "Indianópolis-MG", "TB": "Telêmaco Borba-PR", "IMP": "Imperatriz-MA"}
CALC = {"P1": "#2a78d6", "P2": "#eb6834", "PA": "#1baf7a"}
CALN = {"P1": "pulso único", "P2": "dois pulsos", "PA": "pulsos anuais"}
D = pd.read_csv(S / "mensal.csv.gz", usecols=["id", "mes_ref", "biom_foliage", "biom_stem", "volume", "asw"])
D["mes_ref"] = D.mes_ref.round().astype(int)
serie = lambda pid: D[D.id == pid]
for f_ in F.glob("F*.png"):
    f_.unlink()

# F1 — trajetórias (solo local, A1, F100, dois pulsos)
fig, ax = plt.subplots(2, 3, figsize=(11.5, 5.6), sharex=True)
for j, s_ in enumerate(SITN):
    for d in DEFOL_:
        pid = f"{s_}_A1_WLOC_F100_D{int(d*100):02d}_{'P2' if d > 0 else 'CTRL'}"
        g = serie(pid); lab = "controle" if d == 0 else f"{int(d*100)}%"
        for i, (v, tit) in enumerate([("biom_foliage", "W$_F$ (t ha$^{-1}$)"), ("biom_stem", "W$_S$ (t ha$^{-1}$)")]):
            ax[i, j].plot(g.mes_ref, g[v], color=DEF[d], label=lab, lw=1.8 if d else 1.4, ls="-" if d else "--")
            ax[i, j].set_ylabel(tit if j == 0 else "")
    ax[0, j].set_title(SITN[s_] + (" (diagnóstico)" if s_ == "IMP" else ""), fontsize=10)
    ax[1, j].set_xlabel("mês da simulação (idade = 12 + mês)")
    for a in ax[:, j]:
        for e in (12, 48):
            a.axvline(e, color="#c3c2b7", lw=0.8, zorder=0)
ax[0, 0].legend(frameon=False, title="desfolha", fontsize=8)
fig.tight_layout(); fig.savefig(F / "F1_trajetorias_3sitios.png", dpi=200); plt.close(fig)

# F2 — matriz água × FR, 3 sítios × 4 materiais (d = 50 %, P1)
sub0 = E[(E.desfolha == 0.5) & (E.calendario == "P1")]
vmax = sub0[sub0.apto_analise_principal].perda_volume_k72.max()
fig, ax = plt.subplots(3, 4, figsize=(11, 8))
for i, s_ in enumerate(SITN):
    for j, m in enumerate(["A1", "C5", "C2", "C4"]):
        a = ax[i, j]; sub = sub0[(sub0.sitio == s_) & (sub0.material == m)]
        Z = sub.pivot_table(index="Fn", columns="W", values="perda_volume_k72").sort_index(ascending=False)
        im = a.imshow(Z.values, cmap="Blues", vmin=0, vmax=vmax)
        for r_ in range(4):
            for c_ in range(4):
                val = Z.values[r_, c_]
                a.text(c_, r_, f"{val:.1f}".replace(".", ","), ha="center", va="center", fontsize=7.5,
                       color="#0b0b0b" if val < 0.6 * vmax else "#fcfcfb")
        a.set_xticks(range(4)); a.set_xticklabels([f"W{w}" for w in Z.columns], fontsize=7.5); a.set_yticks(range(4))
        a.set_yticklabels([f"F{f}" for f in Z.index], fontsize=7.5); a.grid(False)
        a.set_title(f"{s_} · {m}" + (" (diagn.)" if (s_ == "IMP" and m == "A1") else ""), fontsize=9)
fig.colorbar(im, ax=ax, label="perda de volume aos 84 meses (%)", shrink=0.6)
fig.savefig(F / "F2_matriz_agua_FR_3sitios.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# F3 — frequência (solo local, F100)
L100 = LOC[LOC.Fn == 100]
fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.7), sharey=True)
for a, s_ in zip(ax, SITN):
    for cal in ["P1", "P2", "PA"]:
        for m, ls in (("A1", "-"), ("C5", "--")):
            g = L100[(L100.sitio == s_) & (L100.material == m) & (L100.calendario == cal)].sort_values("desfolha")
            x = np.r_[0, g.desfolha * 100]; y = np.r_[0, g.perda_volume_k72]
            a.plot(x, y, ls=ls, marker="o", ms=3.5, color=CALC[cal], label=f"{CALN[cal]} · {m}" if s_ == "IND" else None)
    a.set_title(SITN[s_], fontsize=10); a.set_xlabel("desfolha (%)")
ax[0].set_ylabel("perda de volume aos 84 meses (%)"); ax[0].legend(frameon=False, fontsize=7.5)
fig.tight_layout(); fig.savefig(F / "F3_frequencia_3sitios.png", dpi=200); plt.close(fig)

# F4 — época do pulso (solo local, F100, d = 50 %) + chuva nos 3 meses após o evento
from clima import clima_mensal as _cm  # noqa: E402
MESES = {"P1": 1, "EA": 4, "EJ": 7, "EO": 10}
fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.8), sharey=True)
for a, s_ in zip(ax, SITN):
    cl = _cm(s_); cl = cl[cl.year == 2017].set_index("month").prcp
    chuva = [cl.loc[mm:mm + 2].sum() for mm in MESES.values()]
    b = a.twinx(); b.bar(list(MESES.values()), chuva, width=1.6, color="#e6e5e0", zorder=0); b.set_ylim(0, 1200)
    b.set_ylabel("chuva nos 3 meses após o pulso (mm)" if s_ == "IMP" else "", fontsize=8); b.tick_params(labelsize=7.5)
    if s_ != "IMP": b.set_yticklabels([])
    a.set_zorder(b.get_zorder() + 1); a.patch.set_visible(False)
    for m in ["A1", "C5", "C2", "C4"]:
        g = L100[(L100.sitio == s_) & (L100.material == m) & (L100.desfolha == 0.5) & L100.calendario.isin(MESES)]
        g = g.assign(mes=g.calendario.map(MESES)).sort_values("mes")
        a.plot(g.mes, g.perda_volume_k72, marker="o", color=CAT[m], label=m, alpha=0.5 if (s_ == "IMP" and m == "A1") else 1)
    a.set_xticks(list(MESES.values())); a.set_xticklabels(["jan", "abr", "jul", "out"]); a.set_title(SITN[s_], fontsize=10)
    a.set_xlabel("mês do pulso (2017)")
ax[0].set_ylabel("perda de volume aos 84 meses (%)"); ax[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(F / "F4_epoca_3sitios.png", dpi=200); plt.close(fig)

# F5 — recuperação × água (E1-E6, F100, P1, d = 50 %)
fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.5), sharey=True)
for a, s_ in zip(ax, SITN):
    sub = E[(E.sitio == s_) & (E.Fn == 100) & (E.calendario == "P1") & (E.desfolha == 0.5)]
    for m in ["A1", "C5", "C2", "C4"]:
        g = sub[sub.material == m].sort_values("W")
        a.plot(g.W, g.recup_rel95_meses_ev1, marker="o", color=CAT[m], label=m, alpha=0.5 if (s_ == "IMP" and m == "A1") else 1)
    a.set_title(SITN[s_], fontsize=10); a.set_xlabel("água (% de ASW$_{max}$ de referência)")
ax[0].set_ylabel("meses até W$_F$ ≥ 95% do controle"); ax[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(F / "F5_recuperacao_agua_3sitios.png", dpi=200); plt.close(fig)

# F6 — Morris por sítio (perda de volume)
fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.6), sharex=True)
for a, s_ in zip(ax, SITN):
    t_ = MOR[(MOR.sitio == s_) & (MOR.resposta == "perda_volume_k72_pp")].nlargest(8, "mu_estrela").iloc[::-1]
    a.barh(t_.parametro, t_.mu_estrela, color="#4d4d4d", edgecolor="white")
    a.scatter(t_.sigma, t_.parametro, color="#eb6834", s=14, zorder=3, label="σ")
    a.set_title(SITN[s_] + (" (diagnóstico)" if s_ == "IMP" else ""), fontsize=10); a.set_xlabel("μ∗ (barras) e σ (pontos), p.p.")
    a.grid(axis="y", visible=False)
ax[0].legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(F / "F6_morris_3sitios.png", dpi=200); plt.close(fig)

# F7 — decomposição
fig, ax = plt.subplots(figsize=(8, 3.2))
sub = DEC[DEC.resposta == "perda_volume_k72"].set_index("sitio")[["material", "W", "Fn", "material×W", "material×Fn", "W×Fn", "ordem≥3"]]
sub.index = [SITN[i] for i in sub.index]
sub = sub.rename(columns={"W": "água", "Fn": "fertilidade", "material×W": "material×água", "material×Fn": "material×fert.", "W×Fn": "água×fert."})
left = np.zeros(len(sub)); cores = ["#2a78d6", "#eb6834", "#1baf7a", "#86b6ef", "#f4b09a", "#9fdcc3", "#c3c2b7"]
for c, col in zip(sub.columns, cores):
    ax.barh(sub.index, sub[c], left=left, color=col, label=c, edgecolor="#fcfcfb", linewidth=2); left += sub[c].values
ax.set_xlabel("% da soma de quadrados da perda de volume (84 meses)")
ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3))
fig.tight_layout(); fig.savefig(F / "F7_decomposicao.png", dpi=200); plt.close(fig)

json.dump({"Q6": Q6.to_dict("records")}, open(S / "respostas_resumo.json", "w"), indent=2, ensure_ascii=False)
print(DEC.round(1).to_string()); print(Q5.to_string()); print(Q6.to_string())
for s_ in SITN:
    print(s_, MOR[(MOR.sitio == s_) & (MOR.resposta == "perda_volume_k72_pp")].nlargest(7, "mu_estrela")[["parametro", "mu_estrela", "sigma"]].to_string())
