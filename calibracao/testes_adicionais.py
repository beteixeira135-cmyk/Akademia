"""Testes adicionais da Missão 07 (etapa 6/7), feitos só para decidir se conclusões do TCC se sustentam.
(1) Protocolo aproximado de Matrangolo et al. (2010): E. grandis seminal, Viçosa-MG, desfolhas totais aos 56, 143 e
    267/278 dias; volume aos 92 meses (Tabela 2 do artigo: 469,1; 291,4; 178,8; 180,0; 95,4 m³/ha). Simulado com C5
    (híbrido, não E. grandis seminal), clima NASA POWER 2015–2024 de Viçosa (não o do período do experimento),
    ASWmax 215 mm (assumido, sem solo local) e eventos deslocados +2,2 meses (o C5 só começa aos 3 meses):
    4, 7 e 11 meses de idade. É um teste de ordem de grandeza, não de ajuste.
(2) Quentin et al. (2011): ~45% de desfolha da copa superior em E. globulus de 4 anos; transpiração por área de
    alburno sem diferença significativa em 215 dias. Simulado: C5 em Indianópolis, 45% aos 48 meses; razão da
    transpiração do dossel tratamento/controle nos 7 meses seguintes, versões original e calibrada (γ = 0; 0,5; 1).
(3) Quentin et al. (2012): aumento transitório (~30%, pico ~22 dias) da fotossíntese saturada só com irrigação.
    Simulado: duração (meses) em que a compensação fica ativa após 60% de desfolha (C5, Indianópolis)."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
import clima
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
clima.SITIOS["VIC"] = dict(nome="Viçosa-MG", arquivo="POWER_daily_vicosa_20150101_20241231.csv", lat=-20.7546, lon=-42.8825, papel="teste")
J = json.load(open(Path(__file__).parent / "saida/calibracao_d0999.json"))
GAMMA = json.load(open(Path(__file__).resolve().parent / "saida/gamma_quentin2011.json"))["gamma_calibrado"]  # γ calibrado com Quentin et al. (2011)
MED = dict(U=J["U"]["q50"], a=J["a"]["q50"], gam=GAMMA)
M = MATERIAIS["C5"]


def sim(sitio, ev=None, comp=None, asw=215.0):
    site = dict(latitude=clima.SITIOS[sitio]["lat"], altitude=0, soil_class=-1, asw_i=asw, asw_min=0, asw_max=asw,
                **{"from": "2015-04", "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = run_3pg_pjs(site, sp, clima.clima_mensal(sitio), params("C5"), defoliation_events=ev, compensation=comp)
    return o.set_index((o.age * 12).round().astype(int))


out = {}
# (1) Matrangolo
obs = {"1x (56 d)": 469.1 - 291.4, "2x (56 e 143 d)": 469.1 - 178.8, "2x (56 e 267 d)": 469.1 - 180.0, "3x (56, 143 e 278 d)": 469.1 - 95.4}
obs = {k: 100 * v / 469.1 for k, v in obs.items()}
ev = {"1x (56 d)": ["2015-05"], "2x (56 e 143 d)": ["2015-05", "2015-08"], "2x (56 e 267 d)": ["2015-05", "2015-12"],
      "3x (56, 143 e 278 d)": ["2015-05", "2015-08", "2015-12"]}
c = sim("VIC"); A = pd.read_csv(Path(__file__).parent / "saida/amostras_posterior_d0999.csv")
mt = []
for k, ms in ev.items():
    e = {m: 0.999 for m in ms}
    lo = 100 * (1 - sim("VIC", e).volume[92] / c.volume[92])
    lc = 100 * (1 - sim("VIC", e, MED).volume[92] / c.volume[92])
    post = [100 * (1 - sim("VIC", e, dict(U=a.U, a=a.a, gam=GAMMA)).volume[92] / c.volume[92]) for a in A.iloc[::4].itertuples()]
    mt.append(dict(tratamento=k, observado=obs[k], original=lo, calibrado_mediana=lc, calibrado_q05=np.quantile(post, .05),
                   calibrado_q95=np.quantile(post, .95)))
MT = pd.DataFrame(mt); out["matrangolo"] = MT.round(1).to_dict("records")
e_o = MT.original - MT.observado; e_c = MT.calibrado_mediana - MT.observado
out["matrangolo_metricas"] = dict(vies_original=float(e_o.mean()), rmse_original=float(np.sqrt((e_o ** 2).mean())),
                                  vies_calibrado=float(e_c.mean()), rmse_calibrado=float(np.sqrt((e_c ** 2).mean())))
# (2) Quentin 2011
c = sim("IND"); rows = []
for nome, comp in [("original", None), ("calibrado γ=0", dict(MED, gam=0.0)), ("calibrado γ=0,5", MED), ("calibrado γ=1", dict(MED, gam=1.0))]:
    t = sim("IND", {"2019-01": 0.45}, comp)
    rows.append(dict(versao=nome, razao_transpiracao_7meses=float(t.transp_veg.loc[48:54].sum() / c.transp_veg.loc[48:54].sum())))
out["quentin2011_transpiracao"] = rows
# (3) Quentin 2012
t = sim("IND", {"2018-01": 0.6}, MED)
on = t.comp_ativa.loc[36:]; out["quentin2012_meses_compensacao_ativa"] = int(on.sum())
out["quentin2012_U_ef_medio_quando_ativa"] = float(t.comp_U.loc[36:][on > 0].mean())
json.dump(out, open(Path(__file__).parent / "saida/testes_adicionais.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
