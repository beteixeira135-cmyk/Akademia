#!/usr/bin/env python3
"""Calibração de γ (condutância compensatória) com Quentin et al. (2011), experimento independente de Bertulio et al. (2008).
Quentin et al. (2011): ~45% de desfolha da metade superior da copa de E. globulus de 4 anos; a transpiração por área de
alburno das árvores desfolhadas não diferiu da do controle em 215 dias (homeostase: razão tratamento/controle ≈ 1).
Protocolo simulado: clone A1 em Indianópolis, solo local, 45% de desfolha em jan/2019 (48 meses), razão da transpiração
do dossel tratamento/controle nos 7 meses seguintes; U e a nas medianas a posteriori (γ não altera as perdas de Bertulio).
γ calibrado = valor da grade 0–1 cuja razão fica mais perto de 1. Saída: saida/gamma_quentin2011.json"""
import json, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
import run_experimentos as RE
from clima import SITIOS, clima_mensal
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
J = json.load(open(Path(__file__).parent / "saida/calibracao_d0999.json"))
U_MESES = json.load(open(Path(__file__).parent / "saida/regra_compensacao.json"))["u_meses"]
M = MATERIAIS["A1"]; a = RE.SOLO_LOCAL["IND"]; CL = clima_mensal("IND")


def sim(ev=None, comp=None):
    site = dict(latitude=SITIOS["IND"]["lat"], altitude=0, soil_class=-1, asw_i=a, asw_min=0, asw_max=a, **{"from": "2016-01", "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = run_3pg_pjs(site, sp, CL, params("A1"), defoliation_events=ev, compensation=comp)
    return o.set_index((o.age * 12).round().astype(int))


c = sim(); tc = c.transp_veg.loc[48:54].sum()
razao = lambda comp: float(sim({"2019-01": 0.45}, comp).transp_veg.loc[48:54].sum() / tc)
grade = [dict(gam=float(g), razao=razao(dict(U=J["U"]["q50"], a=J["a"]["q50"], gam=float(g), u_meses=U_MESES))) for g in np.round(np.arange(0, 1.0001, 0.05), 2)]
orig = razao(None)
best = min(grade, key=lambda r: abs(r["razao"] - 1))
out = dict(fonte="Quentin et al. (2011), Agricultural and Forest Meteorology 151:356-364", observado="sem diferença significativa (razão ≈ 1)",
           razao_original=orig, grade=grade, gamma_calibrado=best["gam"], razao_no_gamma=best["razao"])
json.dump(out, open(Path(__file__).parent / "saida/gamma_quentin2011.json", "w"), indent=1, ensure_ascii=False)
print("original", round(orig, 3), "| γ:", {r["gam"]: round(r["razao"], 3) for r in grade if r["gam"] in (0, 0.5, 1)}, "| γ calibrado =", best["gam"], round(best["razao"], 3))
