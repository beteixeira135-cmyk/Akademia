"""Validação qualitativa independente com experimentos de E. globulus (outra espécie; só sinal e ordem de grandeza).
Material C5 (Borges, 2009), Indianópolis, solo local, plantio 2015-01 (início aos 3 meses, 2015-04).
  Barry et al. (2012): ~40% de desfolha aos 3 meses e ~55% aos 9 meses; aos 18 meses, altura, diâmetro e área foliar
    sem diferença significativa. Aqui o 1º evento vai para 4 meses (o mês inicial não admite evento).
  Eyles et al. (2009): 40% aos 8 meses; compensação do crescimento do tronco em 5 meses (aos 13 meses).
Compara o módulo original (v2) com 200 amostras do posterior da calibração (U, a; γ ~ prior)."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
from clima import SITIOS, clima_mensal
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
CL = clima_mensal("IND"); M = MATERIAIS["C5"]
def sim(ev=None, comp=None):
    site = dict(latitude=SITIOS["IND"]["lat"], altitude=0, soil_class=-1, asw_i=215.0, asw_min=0, asw_max=215.0,
                **{"from": "2015-04", "to": "2017-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = run_3pg_pjs(site, sp, CL, params("C5"), defoliation_events=ev, compensation=comp)
    return o.set_index((o.age * 12).round().astype(int))
C = sim()
CASOS = {"Barry 2012 (aos 18 meses)": ({"2015-05": 0.40, "2015-10": 0.55}, 18),
         "Eyles 2009 (aos 13 meses)": ({"2015-09": 0.40}, 13)}
A = pd.read_csv(Path(__file__).parent / "saida/amostras_posterior_d0999.csv")
out = []
for nome, (ev, idade) in CASOS.items():
    for rot, comps in [("original", [None]), ("calibrado", [dict(U=r.U, a=r.a, gam=r.gam) for r in A.itertuples()])]:
        L = []
        for cp in comps:
            t = sim(ev, cp)
            L.append({v: 100 * (1 - t.at[idade, v] / C.at[idade, v]) for v in ["dbh", "height", "lai", "biom_stem"]})
        L = pd.DataFrame(L)
        for v in L:
            out.append(dict(caso=nome, versao=rot, variavel=v, perda_media=L[v].mean(), q05=L[v].quantile(.05), q95=L[v].quantile(.95)))
O = pd.DataFrame(out).round(2); O.to_csv(Path(__file__).parent / "saida/validacao_globulus.csv", index=False)
print(O.to_string(index=False))
