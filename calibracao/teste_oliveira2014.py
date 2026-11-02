#!/usr/bin/env python3
"""Teste independente da compensação calibrada com Oliveira et al. (2014), Chemical Engineering Transactions 39:1543-1548,
doi: 10.3303/CET1439258 (lido em https://www.aidic.it/cet/14/39/258.pdf em 02/11/2026).
Experimento: E. grandis de 6 meses em Mucuri-BA (Mata Atlântica), espaçamento 3,0 × 2,5 m, uma desfolha manual:
T1 100%; T2 75%, T3 50% e T4 25% da copa superior; T5 50% da copa inferior; T6 controle. Medições a cada 60 dias até
240 dias. Resultados publicados (T1 × controle, 240 dias): volume 64,6% do controle (perda de 35,4%); diâmetro a 20 cm
62,62 × 73,5 mm; altura 5,27 × 5,92 m. Só T1 diferiu do controle (Tukey 5%); desfolhas parciais sem efeito significativo.
As perdas de volume dos tratamentos parciais são DERIVADAS aqui dos incrementos da Tabela 1 do artigo (D²H, mesmo valor
inicial para todos, por serem blocos casualizados) e servem só como ordem de grandeza.

Simulação (adaptações declaradas): clone C5 (híbrido, não E. grandis seminal), clima NASA POWER 2015–2024 de Mucuri
(o ano do experimento não é informado), ASWmax 215 mm (assumido, sem solo local, como em Matrangolo), 1.333 árvores/ha,
desfolha no 6º mês e avaliação 8 meses depois (14 meses de idade). Para não depender de um único ano de clima, o plantio
foi repetido em jan de 2015 a 2022. O 3-PG não distingue copa superior de inferior: só a fração removida entra.
Saída: saida/teste_oliveira2014.json"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
import clima
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
clima.SITIOS["MUC"] = dict(nome="Mucuri-BA", arquivo="POWER_daily_mucuri_20150101_20241231.csv", lat=-18.0865, lon=-39.5513, papel="teste")
CL = clima.clima_mensal("MUC")
J = json.load(open(Path(__file__).parent / "saida/calibracao_d0999.json"))
GAMMA = json.load(open(Path(__file__).parent / "saida/gamma_quentin2011.json"))["gamma_calibrado"]
U_MESES = json.load(open(Path(__file__).parent / "saida/regra_compensacao.json"))["u_meses"]  # U só no mês do ataque (Turnbull et al., 2007; Quentin et al., 2012)
MED = dict(U=J["U"]["q50"], a=J["a"]["q50"], gam=GAMMA, u_meses=U_MESES)
AM = pd.read_csv(Path(__file__).parent / "saida/amostras_posterior_d0999.csv").iloc[::4]
M = MATERIAIS["C5"]

# observado (Oliveira et al., 2014)
D0, H0 = 73.5 - 43.25, 5.92 - 4.17  # valores iniciais do controle (final − incremento de 240 dias, Tabela 1)
INC = {"T1 100%": (32.45, 3.46), "T2 75% superior": (41.85, 3.83), "T3 50% superior": (41.95, 3.87),
       "T4 25% superior": (44.48, 4.07), "T5 50% inferior": (43.50, 3.93)}
DESF = {"T1 100%": 0.999, "T2 75% superior": 0.75, "T3 50% superior": 0.50, "T4 25% superior": 0.25, "T5 50% inferior": 0.50}
obs = {}
for k, (dd, hh) in INC.items():
    d, h = D0 + dd, H0 + hh
    obs[k] = dict(volume_derivado=100 * (1 - d ** 2 * h / (73.5 ** 2 * 5.92)), diametro_derivado=100 * (1 - d / 73.5), altura_derivada=100 * (1 - h / 5.92))
obs["T1 100%"].update(volume_publicado=35.4, diametro_publicado=100 * (1 - 62.62 / 73.5), altura_publicada=100 * (1 - 5.27 / 5.92))


def sim(ano, ev=None, comp=None):
    site = dict(latitude=-18.0865, altitude=0, soil_class=-1, asw_i=215.0, asw_min=0, asw_max=215.0,
                **{"from": f"{ano}-04", "to": f"{ano + 1}-06"})
    sp = dict(planted=f"{ano}-01", fertility=M["FR_ref"], stems_n=10000 / 7.5, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = run_3pg_pjs(site, sp, CL, params("C5"), defoliation_events=ev, compensation=comp)
    return o.set_index((o.age * 12).round().astype(int)).loc[14]


linhas = []
for ano in range(2015, 2023):
    c = sim(ano)
    for trat, d in DESF.items():
        if trat == "T5 50% inferior": continue  # mesma fração que T3 no 3-PG
        ev = {f"{ano}-07": d}
        perda = lambda o: {v: 100 * (1 - o[v] / c[v]) for v in ("volume", "dbh", "height")}
        o_, c_ = perda(sim(ano, ev)), perda(sim(ano, ev, MED))
        post = [perda(sim(ano, ev, dict(U=a.U, a=a.a, gam=GAMMA, u_meses=U_MESES)))["volume"] for a in AM.itertuples()] if trat == "T1 100%" else [np.nan]
        linhas.append(dict(ano_plantio=ano, tratamento=trat, d=d, original_volume=o_["volume"], original_dap=o_["dbh"], original_altura=o_["height"],
                           calibrado_volume=c_["volume"], calibrado_dap=c_["dbh"], calibrado_altura=c_["height"],
                           calibrado_q05=float(np.quantile(post, .05)) if trat == "T1 100%" else None, calibrado_q95=float(np.quantile(post, .95)) if trat == "T1 100%" else None))
P = pd.DataFrame(linhas); P.to_csv(Path(__file__).parent / "saida/teste_oliveira2014.csv", index=False)
res = {}
for trat, g in P.groupby("tratamento", sort=False):
    res[trat] = dict(observado={k: round(v, 1) for k, v in obs[trat].items()},
                     original={v: [round(g[f"original_{v}"].min(), 1), round(g[f"original_{v}"].median(), 1), round(g[f"original_{v}"].max(), 1)] for v in ("volume", "dap", "altura")},
                     calibrado={v: [round(g[f"calibrado_{v}"].min(), 1), round(g[f"calibrado_{v}"].median(), 1), round(g[f"calibrado_{v}"].max(), 1)] for v in ("volume", "dap", "altura")},
                     calibrado_faixa90_mediana_anos=[round(g.calibrado_q05.median(), 1), round(g.calibrado_q95.median(), 1)] if trat == "T1 100%" else None)
t1 = res["T1 100%"]; ob = t1["observado"]
eo = [t1["original"][v][1] - ob[k] for v, k in [("volume", "volume_publicado"), ("dap", "diametro_publicado"), ("altura", "altura_publicada")]]
ec = [t1["calibrado"][v][1] - ob[k] for v, k in [("volume", "volume_publicado"), ("dap", "diametro_publicado"), ("altura", "altura_publicada")]]
res["T1_metricas"] = dict(erros_original=[round(e, 1) for e in eo], erros_calibrado=[round(e, 1) for e in ec],
                          RQEM_original=round(float(np.sqrt(np.mean(np.square(eo)))), 1), RQEM_calibrado=round(float(np.sqrt(np.mean(np.square(ec)))), 1))
parc = P[P.tratamento != "T1 100%"]
res["parciais_max_mediana_entre_anos"] = dict(original=round(float(parc.groupby("tratamento").original_volume.median().max()), 1),
                                              calibrado=round(float(parc.groupby("tratamento").calibrado_volume.median().max()), 1))
out = dict(fonte="Oliveira et al. (2014), Chem. Eng. Trans. 39:1543-1548, doi 10.3303/CET1439258",
           nota="[mín, mediana, máx] entre 8 anos de plantio (2015–2022); perda (%) aos 14 meses, 8 meses após a desfolha", resultados=res)
json.dump(out, open(Path(__file__).parent / "saida/teste_oliveira2014.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
