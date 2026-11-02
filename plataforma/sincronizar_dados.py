#!/usr/bin/env python3
"""Sincroniza dados_min.json com o código Python: parâmetros dos clones (experimentos/clones.py, inclusive a correção
do dossel) e calibração da compensação (calibracao/saida: medianas, 200 amostras, γ e regra u_meses).
Rodar antes de construir.py sempre que os clones ou a calibração mudarem."""
import json, sys
from pathlib import Path
import pandas as pd
A = Path(__file__).resolve().parent; R = A.parent
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
from clones import params, origem
CB = R / "calibracao/saida"
D = json.load(open(A / "dados_min.json"))
for m in D["materiais"]:
    p = params(m)
    D["materiais"][m]["params"] = {k: p[k] for k in D["materiais"][m]["params"]}
J = json.load(open(CB / "calibracao_d0999.json")); G = json.load(open(CB / "gamma_quentin2011.json"))["gamma_calibrado"]
UM = json.load(open(CB / "regra_compensacao.json"))["u_meses"]
AM = pd.read_csv(CB / "amostras_posterior_d0999.csv")
D["calibracao"] = dict(fonte="calibracao/saida/calibracao_d0999.json, amostras_posterior_d0999.csv (Bertulio et al., 2008; d = 0,999), "
                              "gamma_quentin2011.json (Quentin et al., 2011) e regra_compensacao.json (U só no mês do ataque)",
                       mediana=dict(U=round(J["U"]["q50"], 4), a=round(J["a"]["q50"], 4), gam=G, u_meses=UM),
                       amostras=[[round(r.U, 4), round(r.a, 4), G] for r in AM.itertuples()])
json.dump(D, open(A / "dados_min.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("ok", D["calibracao"]["mediana"], {m: (D["materiais"][m]["params"]["gammaF1"], D["materiais"][m]["params"]["pFS2"]) for m in D["materiais"]})
