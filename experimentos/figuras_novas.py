#!/usr/bin/env python3
"""Gráficos do TCC que substituem tabelas densas (as tabelas completas ficam no 'Material do TCC' da Akademia).
N1: calibração e validação cruzada (Bertulio et al., 2008); N2: perda nos biomas; N3: espaço de possibilidades.
Fontes: calibracao/saida/validacao_cruzada_previsoes.csv, experimentos/saida/biomas (via tabela do TCC),
experimentos/saida/possibilidades/. Saída: saida/figuras/N*.png"""
import json
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = Path(__file__).resolve().parent; R = A.parent; F = A / "saida" / "figuras"
plt.rcParams.update({"font.family": "serif", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e3e5dc", "grid.linewidth": 0.6, "axes.axisbelow": True})
OBS, ORI, CAL = "#8a5a36", "#a3a89b", "#5f6f34"
br = lambda x: f"{x:.1f}".replace(".", ",")

# N1 — calibração e validação cruzada
V = pd.read_csv(R / "calibracao/saida/validacao_cruzada_previsoes.csv")
V = V[V.esquema.str.startswith("deixa uma")].reset_index(drop=True)
rot = [f"{'Volume' if v == 'volume' else 'Circunferência' if v == 'CAP' else 'Altura'}\n{'urograndis' if m == 'C5' else 'urocam'}" for m, v in zip(V.material, V.variavel)]
x = np.arange(len(V)); w = 0.27
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for k, (col, cor, nome) in enumerate([("observado", OBS, "Observado (Bertulio et al., 2008)"), ("original", ORI, "Módulo sem compensação"), ("calibrado", CAL, "Módulo calibrado, prevendo a observação escondida")]):
    b = ax.bar(x + (k - 1) * w, V[col], w, color=cor, label=nome)
    for xi, v in zip(x + (k - 1) * w, V[col]):
        ax.text(xi, v + 1, br(v), ha="center", fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(rot, fontsize=8.5); ax.set_ylabel("Perda após desfolha total (%)"); ax.set_ylim(0, 90)
ax.legend(frameon=False, fontsize=8, loc="upper left"); ax.grid(axis="x", visible=False)
fig.tight_layout(); fig.savefig(F / "N1_calibracao_validacao.png", dpi=220); plt.close(fig)

# N2 — biomas (mesmos números da tabela do TCC, extraídos sem redigitar)
T = json.load(open(R / "plataforma/material_tabelas.json"))["biomas"]["linhas"]
num = lambda s: float(s.replace("−", "-").replace(",", "."))
nome = [l[0].replace(" (", "\n(") for l in T]
p1o, p1c, pao, pac = [np.array([num(l[i]) for l in T]) for i in (2, 3, 4, 5)]
ic = [tuple(num(v) for v in l[6].split(" a ")) for l in T]
lo = pac - np.array([a for a, b in ic]); hi = np.array([b for a, b in ic]) - pac
y = np.arange(len(T))[::-1]; h = 0.36
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.9), sharey=True)
for a_, (o, c, tit) in zip(ax, [(p1o, p1c, "(a) Uma desfolha de 50%"), (pao, pac, "(b) Desfolha de 50% todo ano")]):
    a_.barh(y + h / 2, o, h, color=ORI, label="Sem compensação"); a_.barh(y - h / 2, c, h, color=CAL, label="Calibrado")
    a_.axvline(0, color="#23271f", lw=0.8); a_.set_title(tit, fontsize=10); a_.set_xlabel("Perda de volume aos 7 anos (%)")
    a_.grid(axis="y", visible=False)
ax[1].errorbar(pac, y - h / 2, xerr=[lo, hi], fmt="none", ecolor="#23271f", elinewidth=0.8, capsize=2, label="Faixa de 90%")
ax[0].set_yticks(y); ax[0].set_yticklabels(nome, fontsize=8)
hs, ls = [], []
for a_ in ax:
    for hh, ll in zip(*a_.get_legend_handles_labels()):
        if ll not in ls: hs.append(hh); ls.append(ll)
fig.legend(hs, ls, frameon=False, fontsize=8, loc="lower center", ncol=3)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(F / "N2_biomas.png", dpi=220); plt.close(fig)

# N3 — espaço de possibilidades
D = pd.read_csv(A / "saida/possibilidades/possibilidades.csv"); D = D[D.apto]
S = json.load(open(A / "saida/possibilidades/resumo_possibilidades.json"))
fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.4), gridspec_kw=dict(width_ratios=[1.35, 1]))
bins = np.arange(-6, 86, 2)
for v, cor, n in [("original", ORI, "Sem compensação"), ("calibrada", CAL, "Calibrado")]:
    ax[0].hist(D[D.versao == v].perda_volume, bins=bins, color=cor, alpha=0.75 if v == "original" else 0.85, label=n)
ax[0].axvspan(-6, 0, color=OBS, alpha=0.15); yt = ax[0].get_ylim()[1]
ax[0].annotate("perda negativa: o atacado\nsupera o controle", xy=(-2.5, yt * 0.55), xytext=(22, yt * 0.55), fontsize=7.5, color=OBS, va="center",
               arrowprops=dict(arrowstyle="->", color=OBS, lw=0.8))
ax[0].set_xlabel("Perda de volume aos 7 anos (%)"); ax[0].set_ylabel("Número de cenários"); ax[0].set_title("(a) 5.688 cenários de danos combinados", fontsize=10)
ax[0].legend(frameon=False, fontsize=8, loc="upper right"); ax[0].grid(axis="x", visible=False)
it = [("Folhagem volta a\n95% do controle", "frac_folhas_recuperam"), ("Crescimento após 1 ano\nsupera o controle", "frac_npp_pos_maior"), ("Volume final\nsupera o controle", "frac_ganho")]
yy = np.arange(len(it))[::-1]
for k, (v, cor, n) in enumerate([("original", ORI, "Sem compensação"), ("calibrada", CAL, "Calibrado")]):
    vals = [S[v][c] for _, c in it]
    ax[1].barh(yy + (0.5 - k) * 0.38, vals, 0.38, color=cor, label=n)
    for yi, val in zip(yy + (0.5 - k) * 0.38, vals):
        ax[1].text(val + 1.5, yi, br(val) + "%", va="center", fontsize=7.5)
ax[1].set_yticks(yy); ax[1].set_yticklabels([a for a, _ in it], fontsize=8); ax[1].set_xlim(0, 108)
ax[1].set_xlabel("Cenários (%)"); ax[1].set_title("(b) O que se recupera", fontsize=10); ax[1].grid(axis="y", visible=False)
fig.tight_layout(); fig.savefig(F / "N3_possibilidades.png", dpi=220); plt.close(fig)
print("ok")
