#!/usr/bin/env python3
"""Sensibilidade exploratória das limitações identificadas no TCC.

Não altera o motor nem os parâmetros padrão. Perturbações ±10% são
numéricas, não faixas inferidas de fontes de campo.
"""
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "modelo"))

from clones import params
from clima import SITIOS, clima_mensal
from run_experimentos import SOLO_LOCAL
from threepg_pjs import run_3pg_pjs


SITIOS_TESTE = ("IND", "TB", "IMP")
ATIVO = ("thinPower", "mR", "mS", "Qa", "Qb")
ESTRUTURALMENTE_INATIVO = ("kF", "mF", "MinCond")
FOLHADA = ("gammaF1", "gammaF0", "tgammaF")


def sim(sitio, parametros):
    asw = SOLO_LOCAL[sitio]
    site = {
        "latitude": SITIOS[sitio]["lat"],
        "altitude": 0,
        "soil_class": -1,
        "asw_i": asw,
        "asw_min": 0,
        "asw_max": asw,
        "from": "2016-01",
        "to": "2023-01",
    }
    stand = {
        "planted": "2015-01",
        "fertility": 0.8,
        "stems_n": 10000 / 9,
        "biom_stem": 5.47,
        "biom_root": 1.09,
        "biom_foliage": 2.07,
    }
    clima = clima_mensal(sitio)
    return run_3pg_pjs(
        site,
        stand,
        clima,
        parametros,
        defoliation_events={"2017-01": 0.50},
    )


def metrica(sitio, parametros):
    parametros_controle = dict(parametros)
    asw = SOLO_LOCAL[sitio]
    site = {
        "latitude": SITIOS[sitio]["lat"],
        "altitude": 0,
        "soil_class": -1,
        "asw_i": asw,
        "asw_min": 0,
        "asw_max": asw,
        "from": "2016-01",
        "to": "2023-01",
    }
    stand = {
        "planted": "2015-01",
        "fertility": 0.8,
        "stems_n": 10000 / 9,
        "biom_stem": 5.47,
        "biom_root": 1.09,
        "biom_foliage": 2.07,
    }
    clima = clima_mensal(sitio)
    controle = run_3pg_pjs(site, stand, clima, parametros_controle)
    atacado = sim(sitio, parametros)
    k = 72
    perda = 100 * (1 - atacado.volume.iloc[k] / controle.volume.iloc[k])
    rec = next(
        (
            k - 24
            for k in range(24, 85)
            if atacado.biom_foliage.iloc[k] / controle.biom_foliage.iloc[k] >= 0.95
        ),
        float("nan"),
    )
    return perda, controle.volume.iloc[k], rec


def metrica_mortalidade(sitio, fracao):
    asw = SOLO_LOCAL[sitio]
    site = {
        "latitude": SITIOS[sitio]["lat"],
        "altitude": 0,
        "soil_class": -1,
        "asw_i": asw,
        "asw_min": 0,
        "asw_max": asw,
        "from": "2016-01",
        "to": "2023-01",
    }
    stand = {
        "planted": "2015-01",
        "fertility": 0.8,
        "stems_n": 10000 / 9,
        "biom_stem": 5.47,
        "biom_root": 1.09,
        "biom_foliage": 2.07,
    }
    clima = clima_mensal(sitio)
    base = params("A1")
    controle = run_3pg_pjs(site, stand, clima, base)
    atacado = run_3pg_pjs(
        site,
        stand,
        clima,
        base,
        mortality_events={"2017-01": fracao},
    )
    k = 72
    perda = 100 * (1 - atacado.volume.iloc[k] / controle.volume.iloc[k])
    return perda, controle.volume.iloc[k]


def main():
    base = params("A1")
    linhas = []
    parametros_mapeados = ATIVO + FOLHADA

    for sitio in SITIOS_TESTE:
        for fracao in (0.0, 0.05, 0.14, 0.15):
            perda, volume = metrica_mortalidade(sitio, fracao)
            linhas.append(
                dict(
                    sitio=sitio,
                    grupo="mortalidade",
                    parametro="mortalidade",
                    nivel=f"{round(100 * fracao):.0f}%",
                    valor=round(fracao, 4),
                    perda_volume_k72_pp=round(perda, 4),
                    volume_ctrl_k72=round(volume, 4),
                    recup_rel95_meses=None,
                )
            )

        for parametro in parametros_mapeados:
            valor_base = float(base[parametro])
            baixo = valor_base * 0.9
            alto = valor_base * 1.1
            for nivel, valor in (("baixo", baixo), ("base", valor_base), ("alto", alto)):
                P = dict(base)
                P[parametro] = valor
                perda, volume, recuperacao = metrica(sitio, P)
                linhas.append(
                    dict(
                        sitio=sitio,
                        grupo="globulus" if parametro in ATIVO else "folhada",
                        parametro=parametro,
                        nivel=nivel,
                        valor=round(valor, 6),
                        perda_volume_k72_pp=round(perda, 4),
                        volume_ctrl_k72=round(volume, 4),
                        recup_rel95_meses=(
                            round(recuperacao, 1)
                            if pd.notna(recuperacao)
                            else None
                        ),
                    )
                )

        for parametro in ESTRUTURALMENTE_INATIVO:
            linhas.append(
                dict(
                    sitio=sitio,
                    grupo="globulus",
                    parametro=parametro,
                    nivel="estruturalmente_inativo",
                    valor=0.0,
                    perda_volume_k72_pp=None,
                    volume_ctrl_k72=None,
                    recup_rel95_meses=None,
                    motivo="valor neutro ou processo desligado na configuração testada",
                )
            )

    saida = AQUI / "saida" / "sensibilidade_limitacoes.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(linhas).to_csv(saida, index=False)

    resumo = []
    for sitio in SITIOS_TESTE:
        dados = pd.read_csv(saida)
        dados = dados[dados.sitio == sitio]
        for grupo in ("globulus", "folhada", "mortalidade"):
            selecionados = dados[dados.grupo == grupo]
            for parametro in selecionados.parametro.dropna().unique():
                serie = selecionados[
                    (selecionados.parametro == parametro)
                    & selecionados.nivel.isin(("baixo", "alto"))
                ].perda_volume_k72_pp.dropna()
                if len(serie):
                    resumo.append(
                        dict(
                            sitio=sitio,
                            grupo=grupo,
                            parametro=parametro,
                            amplitude_perda_pp=round(serie.max() - serie.min(), 4),
                        )
                    )

    resumo_csv = AQUI / "saida" / "resumo_sensibilidade_limitacoes.csv"
    pd.DataFrame(resumo).sort_values(
        ["sitio", "grupo", "amplitude_perda_pp"],
        ascending=[True, True, False],
    ).to_csv(resumo_csv, index=False)

    print(saida)
    print(resumo_csv)
    print(pd.DataFrame(resumo).sort_values("amplitude_perda_pp", ascending=False).head(20).to_string(index=False))


if __name__ == "__main__":
    main()
