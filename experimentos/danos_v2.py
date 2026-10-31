#!/usr/bin/env python3
"""Catálogo de danos de pragas e doenças do eucalipto, cada um representado pelo mecanismo que afeta no 3-PG.
Magnitudes tiradas da literatura quando existem; quando não existem, o cenário é marcado como exploratório.
Solo local, FR de referência, plantio jan/2015, 3 × 3 m. Saída: saida/danos_v2.csv"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
from clones import MATERIAIS, params  # noqa: E402
from clima import SITIOS, clima_mensal  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402
import run_experimentos as RE  # noqa: E402

CL = {s: clima_mensal(s) for s in SITIOS}


def sim(sitio, mat, **ev):
    M = MATERIAIS[mat]; asw = RE.SOLO_LOCAL[sitio]
    site = dict(latitude=SITIOS[sitio]["lat"], altitude=0, soil_class=-1, asw_i=asw, asw_min=0.0, asw_max=asw,
                **{"from": RE.INICIO.get(mat, "2015-04"), "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = run_3pg_pjs(site, sp, CL[sitio], params(mat), **ev)
    o["idade"] = (o.age * 12).round().astype(int)
    return o.set_index("idade")


def meses(a0, m0, n):
    out = []
    for i in range(n):
        mm = m0 - 1 + i; out.append(f"{a0 + mm // 12}-{mm % 12 + 1:02d}")
    return out


CENARIOS = [
    # nome, praga/doença, mecanismo, eventos, fonte da magnitude, tipo
    ("Lagarta desfolhadora", "lagartas (ex.: Thyrinteina arnobia)", "remoção de folhas",
     dict(defoliation_events={"2017-01": 0.50}), "50% em pulso único (cenário central do TCC)", "referência"),
    ("Psilídeo-de-concha", "Glycaspis brimblecombei", "remoção de folhas",
     dict(defoliation_events={"2017-07": 0.25}), "20–30% de desfolha em urograndis (Wilcken et al., 2003)", "literatura"),
    ("Formigas-cortadeiras", "Atta e Acromyrmex", "remoção de folhas",
     dict(defoliation_events={"2016-07": 0.95}), "desfolha total no inverno (Freitas; Berti Filho, 1994, em Zanetti et al., 2014); 95% = limite do módulo", "literatura"),
    ("Mancha foliar", "Calonectria (Cylindrocladium) spp.", "remoção gradual de folhas",
     dict(defoliation_events={m: 0.20 for m in meses(2016, 12, 3)}), "desfolha com recuperação em até 6 meses (Santos et al., 2001); 20%/mês por 3 meses = hipótese", "exploratório"),
    ("Percevejo-bronzeado 20%", "Thaumastocoris peregrinus", "perda de eficiência fotossintética",
     dict(efficiency_events={m: 0.20 for m in meses(2017, 7, 4)}), "queda de Fv/Fm e ETR (Almeida et al., 2018); perda em campo desconhecida (Barbosa et al., 2012)", "exploratório"),
    ("Percevejo-bronzeado 40%", "Thaumastocoris peregrinus", "perda de eficiência fotossintética",
     dict(efficiency_events={m: 0.40 for m in meses(2017, 7, 4)}), "idem, intensidade maior", "exploratório"),
    ("Mortalidade 5%", "murcha de Ceratocystis, cancro, seca de ponteiros", "morte de árvores",
     dict(mortality_events={"2017-01": 0.05}), "perdas de árvores de até 15% (Santos et al., 2001)", "literatura"),
    ("Mortalidade 15%", "murcha de Ceratocystis, cancro, seca de ponteiros", "morte de árvores",
     dict(mortality_events={"2017-01": 0.15}), "idem, limite superior", "literatura"),
]
CASOS = [("IND", "A1"), ("TB", "A1"), ("IND", "C5"), ("TB", "C5"), ("IMP", "C5")]


def indicadores(c, t, ev):
    k84 = 84
    datas = [k for d in ev.values() for k in d] if ev else []
    out = dict(perda_volume_84=100 * (1 - t.volume[k84] / c.volume[k84]),
               perda_DAP_84=100 * (1 - t.dbh[k84] / c.dbh[k84]),
               arvores_84_ctrl=c.stems_n[k84], arvores_84_trat=t.stems_n[k84],
               vol_arvore_ratio=(t.volume[k84] / t.stems_n[k84]) / (c.volume[k84] / c.stems_n[k84]))
    if datas:
        d0 = min(datas); ki = int(t.index[pd.to_datetime(t.date).dt.strftime("%Y-%m") == d0][0])
        rec = next((k - ki for k in range(ki, 97) if t.biom_foliage[k] / c.biom_foliage[k] >= .95 and k > ki), np.nan)
        out.update(idade_evento=ki, recup_rel95_meses=rec)
    return out


linhas = []
for s, m in CASOS:
    c = sim(s, m)
    for nome, praga, mec, ev, fonte, tipo in CENARIOS:
        t = sim(s, m, **ev)
        linhas.append(dict(sitio=s, material=m, cenario=nome, praga=praga, mecanismo=mec, fonte=fonte, tipo=tipo, **indicadores(c, t, ev)))

# Ferrugem (juvenil, 3 a 12 meses): só para C5 (inicializado aos 3 meses). Calibra r para que o DAP aos 12 meses
# caia 25% e 35% (Silveira et al., 1998, em Silveira; Higashi, 2003).
JUV = meses(2015, 5, 8)  # mai a dez/2015 (idades 4 a 11 meses; abr/2015 é o estado inicial)
for s in ["IND", "TB", "IMP"]:
    c = sim(s, "C5")
    for alvo in (0.25, 0.35):
        f = lambda r: 1 - sim(s, "C5", efficiency_events={mm: r for mm in JUV}).dbh[12] / c.dbh[12] - alvo
        r = brentq(f, 0.01, 0.99, xtol=1e-6)
        t = sim(s, "C5", efficiency_events={mm: r for mm in JUV})
        linhas.append(dict(sitio=s, material="C5", cenario=f"Ferrugem juvenil −{int(alvo*100)}% DAP", praga="Austropuccinia psidii",
                           mecanismo="perda de eficiência na fase juvenil (calibrada)", fonte="−25 a −35% em altura e diâmetro de plantas jovens (Silveira et al., 1998, em Silveira; Higashi, 2003)",
                           tipo="literatura (calibrado)", r_calibrado=r, perda_DAP_12=100 * (1 - t.dbh[12] / c.dbh[12]), **indicadores(c, t, {"x": JUV})))
D = pd.DataFrame(linhas); D.to_csv(AQUI / "saida/danos_v2.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 20)
print(D.pivot_table(index="cenario", columns=["sitio", "material"], values="perda_volume_84", sort=False).round(1).to_string())
print(D[D.cenario.str.startswith("Ferrugem")][["sitio", "cenario", "r_calibrado", "perda_DAP_12", "perda_volume_84", "perda_DAP_84"]].round(3).to_string())
print(D[D.cenario.str.startswith("Mortalidade")][["sitio", "material", "cenario", "perda_volume_84", "arvores_84_trat", "vol_arvore_ratio"]].round(3).to_string())
print(D[D.mecanismo.str.contains("folhas")][["sitio", "material", "cenario", "recup_rel95_meses"]].to_string())
