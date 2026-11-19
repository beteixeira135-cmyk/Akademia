#!/usr/bin/env python3
"""Crescimento sem desfolha com solo local: volume e IMA aos 84 meses, lenho/IAF entre 24 e 36 meses e IAF aos 24 meses
para comparação com o valor pontual publicado para TECHS 22. Saída: saida/controles_solo_local.csv."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modelo"))
import run_experimentos as RE
from clones import MATERIAIS
L = []
for s in RE.SITIOS_MATRIZ:
    for m in ["A1", "C2", "C4", "C5"]:
        o = RE.rodar(RE.linha(s, m, None, MATERIAIS[m]["FR_ref"], "F100", 0.0, "P1", "LOCAL", asw=RE.SOLO_LOCAL[s]))
        o = o.set_index(o.idade_meses.round().astype(int))
        lenho = o.biom_stem * (1 - o.fracBB)
        j = o  # simulação inteira (até jan/2023), como na versão original da tabela
        L.append(dict(sitio=s, mat=m, vol84=o.volume[84], IMA84=o.volume[84] / 7, caule_24_36=lenho[36] - lenho[24],
                      Ws_24_36=o.biom_stem[36] - o.biom_stem[24], LAI_24=o.lai.loc[24],
                      LAI_24_36=o.lai.loc[24:36].mean(), LAImax=j.lai.max(),
                      meses_fT0=int((j.f_tmp == 0).sum()), fT_med=j.f_tmp.mean(), fSW_med=j.f_sw.mean()))
pd.DataFrame(L).round(2).sort_values(["sitio", "mat"]).to_csv(Path(__file__).parent / "saida/controles_solo_local.csv", index=False)
print(pd.DataFrame(L).round(2).to_string())
