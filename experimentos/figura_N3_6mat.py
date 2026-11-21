"""Figura 10 (N3) regenerada a partir da matriz de seis materiais (possibilidades_6mat)."""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = Path(__file__).resolve().parent
D = pd.read_csv(A / "saida/possibilidades_6mat/possibilidades.csv")
D = D[D.apto.astype(str).str.lower().isin(["true", "1"])]
ORI, CAL, OBS = "#A6A89E", "#5E7035", "#8B4A2B"
S = {}
for v in ["original", "calibrada"]:
    d = D[D.versao == v]
    S[v] = dict(frac_folhas_recuperam=100 * (d[d.d > 0].recup_folhas_meses.notna()).mean(),
                frac_npp_pos_maior=100 * (d.npp_pos_rel > 0).mean(),
                frac_ganho=100 * (d.perda_volume < 0).mean())
fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.4), gridspec_kw=dict(width_ratios=[1.35, 1]))
bins = np.arange(-6, 88, 2)
for v, cor, n in [("original", ORI, "Sem compensação"), ("calibrada", CAL, "Calibrado")]:
    ax[0].hist(D[D.versao == v].perda_volume, bins=bins, color=cor, alpha=0.75 if v == "original" else 0.85, label=n)
ax[0].axvspan(-6, 0, color=OBS, alpha=0.15)
yt = ax[0].get_ylim()[1]
ax[0].annotate("perda negativa: o atacado\nsupera o controle", xy=(-2.5, yt * 0.55), xytext=(22, yt * 0.55),
               fontsize=7.5, color=OBS, va="center", arrowprops=dict(arrowstyle="->", color=OBS, lw=0.8))
ax[0].set_xlabel("Perda de volume aos 7 anos (%)")
ax[0].set_ylabel("Número de cenários")
ax[0].set_title(f"(a) {len(D)//2:,} cenários por versão, seis materiais".replace(",", "."), fontsize=10)
ax[0].legend(frameon=False, fontsize=8, loc="upper right")
ax[0].grid(axis="x", visible=False)
it = [("Folhagem volta a\n95% do controle", "frac_folhas_recuperam"),
      ("Crescimento após 1 ano\nsupera o controle", "frac_npp_pos_maior"),
      ("Volume final\nsupera o controle", "frac_ganho")]
yy = np.arange(len(it))[::-1]
for k, (v, cor, n) in enumerate([("original", ORI, "Sem compensação"), ("calibrada", CAL, "Calibrado")]):
    vals = [S[v][c] for _, c in it]
    pos = yy + (0.5 - k) * 0.38
    ax[1].barh(pos, vals, 0.38, color=cor, label=n)
    for yi, val in zip(pos, vals):
        ax[1].text(val + 1.5, yi, f"{val:.1f}".replace(".", ",") + "%", va="center", fontsize=7.5)
ax[1].set_yticks(yy)
ax[1].set_yticklabels([a for a, _ in it], fontsize=8)
ax[1].set_xlim(0, 108)
ax[1].set_xlabel("Cenários (%)")
ax[1].set_title("(b) O que se recupera", fontsize=10)
ax[1].grid(axis="y", visible=False)
fig.tight_layout()
out = A / "saida/figuras_6mat"
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "N3_possibilidades_6mat.png", dpi=220)
plt.close(fig)
print(S)
