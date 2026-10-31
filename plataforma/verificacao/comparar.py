"""Verificação: motor JavaScript da plataforma (modelo3pg.js) × port Python verificado (threepg_pjs.py), v1–v3."""
import json, sys, subprocess
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parents[1]
sys.path.insert(0, str(RAIZ / "experimentos")); sys.path.insert(0, str(RAIZ / "modelo"))
from clones import MATERIAIS, params
from clima import SITIOS, clima_mensal
from threepg_pjs import run_3pg_pjs
import run_experimentos as RE
SOLO = dict(RE.SOLO_LOCAL, ALM=219.0, ARA=194.0, ELD=145.0)
C = json.load(open(AQUI / "cenarios.json"))
subprocess.run(["node", str(AQUI / "rodar_js.js"), str(AQUI.parent / "modelo3pg.js"), str(AQUI.parent / "dados_min.json"),
                str(AQUI / "cenarios.json"), str(AQUI / "saida_js.json")], check=True)
J = json.load(open(AQUI / "saida_js.json"))
mapa = dict(Wf="biom_foliage", Ws="biom_stem", Wr="biom_root", N="stems_n", vol="volume", lai="lai", dbh="dbh", asw="asw", compU="comp_U")
res = []
for c in C:
    M = MATERIAIS[c["m"]]; a = SOLO[c["s"]]
    site = dict(latitude=SITIOS[c["s"]]["lat"], altitude=0, soil_class=-1, asw_i=a, asw_min=0.0, asw_max=a,
                **{"from": RE.INICIO.get(c["m"], "2015-04"), "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = c["opt"]
    py = run_3pg_pjs(site, sp, clima_mensal(c["s"]), params(c["m"]), defoliation_events=c["defol"] or None,
                     efficiency_events=o.get("efic"), mortality_events=o.get("mort"), compensation=o.get("comp"))
    pior = 0.0
    for kj, kp in mapa.items():
        x = np.array(J[c["id"]][kj], float); y = py[kp].to_numpy(float)
        assert len(x) == len(y), (c["id"], kj, len(x), len(y))
        rel = np.abs(x - y) / np.maximum(np.abs(y), 1e-9)
        pior = max(pior, float(np.nanmax(rel)))
    res.append(dict(cenario=c["id"], meses=len(y), dif_rel_max=pior))
    print(f"{c['id']:20s} {len(y)} meses  diferença relativa máxima {pior:.2e}")
json.dump(res, open(AQUI / "resultado_verificacao.json", "w"), indent=1)
assert max(r["dif_rel_max"] for r in res) < 1e-9, "JS diverge do Python"
print("OK: JS = Python em", len(res), "cenários")
