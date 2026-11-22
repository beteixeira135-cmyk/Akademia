#!/usr/bin/env python3
"""Gera a matriz água × fertilidade da Figura 4, sem depender das séries mensais."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
SAIDA = ROOT / "saida"
FIGURAS = SAIDA / "figuras"
SITIOS = {"IND": "Indianópolis-MG", "TB": "Telêmaco Borba-PR", "IMP": "Imperatriz-MA"}
MATERIAIS = ["A1", "C5", "C2", "C4"]


def gerar_figura_agua_fr(dados: pd.DataFrame, destino: Path) -> None:
    dados = dados.copy()
    if "W" not in dados:
        dados["W"] = pd.to_numeric(dados.nivel_agua).astype(int)
    if "Fn" not in dados:
        dados["Fn"] = dados.nivel_FR.str[1:].astype(int)

    sub = dados[(dados.desfolha == 0.5) & (dados.calendario == "P1")]
    vmax = int(np.ceil(sub.perda_volume_k72.max()))
    fig, ax = plt.subplots(3, 4, figsize=(11, 8))

    for i, sitio in enumerate(SITIOS):
        for j, material in enumerate(MATERIAIS):
            painel = ax[i, j]
            grupo = sub[(sub.sitio == sitio) & (sub.material == material)]
            grade = grupo.pivot_table(
                index="Fn", columns="W", values="perda_volume_k72"
            ).sort_index(ascending=False)
            if len(grupo) != 16 or grade.shape != (4, 4):
                raise ValueError(f"Figura 4: {sitio}/{material} não contém 16 combinações.")
            imagem = painel.imshow(grade.values, cmap="Blues", vmin=0, vmax=vmax)
            for linha in range(4):
                for coluna in range(4):
                    valor = grade.values[linha, coluna]
                    painel.text(
                        coluna,
                        linha,
                        f"{valor:.1f}".replace(".", ","),
                        ha="center",
                        va="center",
                        fontsize=7.5,
                        color="#0b0b0b" if valor < 0.6 * vmax else "#fcfcfb",
                    )
            painel.set_xticks(range(4))
            painel.set_xticklabels([f"W{agua}" for agua in grade.columns], fontsize=7.5)
            painel.set_yticks(range(4))
            painel.set_yticklabels([f"F{fertilidade}" for fertilidade in grade.index], fontsize=7.5)
            diagnostico = sitio == "IMP" and material == "A1"
            painel.set_title(
                f"{sitio} · {material}" + (" (diagn.)" if diagnostico else ""),
                fontsize=9,
            )

    fig.colorbar(
        imagem,
        ax=ax,
        label="perda de volume aos 84 meses (%)",
        ticks=range(vmax + 1),
        shrink=0.6,
    )
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    dados = pd.read_csv(SAIDA / "indicadores_por_tratamento.csv")
    dados = dados[dados.experimento == "E1-E6"]
    gerar_figura_agua_fr(dados, FIGURAS / "F2_matriz_agua_FR_3sitios.png")


if __name__ == "__main__":
    main()
