#!/usr/bin/env python3
"""
Executa a matriz computacional (E1–E6) no port verificado do r3PG (3-PGpjs) com o módulo de desfolha.
Saídas em experimentos/saida/: matriz_tratamentos.csv, mensal.csv.gz, config_execucao.json.

CONVENÇÃO TEMPORAL (única):
  * plantio hipotético: 2015-01 (todos os materiais);
  * A1 (Caldeira) inicializa aos 12 meses (from = 2016-01); C* (Borges) aos 3 meses (from = 2015-04),
    cada um com as biomassas iniciais publicadas na sua fonte;
  * fim: 2023-01 (idade 96 meses) = mês 84 da simulação de referência (A1);
  * "mês k" = mês k da simulação de referência = data 2016-01 + k meses = idade 12 + k meses;
  * pulso único: k = 12 (2017-01, idade 24 meses, estação chuvosa); recorrente: k = 12 e 48 (2020-01);
  * evento aplicado no INÍCIO do passo mensal, antes da interceptação de luz (módulo verificado).
SOLO:
  * ASWmax_ref = 190,6 mm (Indianópolis, 0–200 cm a 33 kPa; planilha 01_PARAMETROS p_ASWmax_33);
    níveis W = 25/50/75/100 % de ASWmax_ref; ASW0 = ASWmax (perfil cheio no início, janeiro);
  * FR: S100 = FR original de cada parametrização (A1 0,8; Borges 0,9); S25 = 0,5483 = FR para
    CTCe = 0 na função de Caldeira 2020 §2.10.4 (Alvares 2011), limite inferior admissível dessa função;
    S50/S75 = pontos equidistantes. Níveis ORDINAIS, não equivalem a 25–100 % de produtividade.
  * E2 exploratório: FR = 0,2…1,0 (abaixo de 0,5483 fica fora da faixa da função de Caldeira).
"""
import itertools, json, platform, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
from clones import MATERIAIS, params  # noqa: E402
from clima import SITIOS, clima_mensal  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

SAIDA = AQUI / "saida"
ASW_REF = 190.6
FR_MIN_CTCE0 = 0.5483
PLANTIO = "2015-01"
FIM = "2023-01"
INICIO = {"A1": "2016-01"}  # Borges: 2015-04
EVENTOS = {"P1": ["2017-01"], "P2": ["2017-01", "2020-01"],
           "PA": [f"{a}-01" for a in range(2017, 2023)],          # anual: jan/2017 … jan/2022 (6 pulsos)
           "EA": ["2017-04"], "EJ": ["2017-07"], "EO": ["2017-10"]}  # épocas: abril, julho, outubro
# SOLO LOCAL (fontes secundárias; ver solos_fontes/SOLOS_LOCAIS.md)
SOLO_LOCAL = {"IND": 215.0,   # TECHS sítio 9 (Estrela do Sul-MG, ~35 km), CAD 0–2 m (Stape) — Binkley et al. 2017, Tab. 2
              "TB": 214.0,    # TECHS sítio 22 (Telêmaco Borba-PR), CAD 0–2 m (Stape) — Binkley et al. 2017, Tab. 2
              "IMP": 210.0}   # SoilGrids 2.0 (7 pontos a ~9 km) + PTF-ZARC (Teixeira et al. 2021), 0–2 m
CAL_LOCAL = ["P1", "P2", "PA", "EA", "EJ", "EO"]
DEFOL = [0.0, 0.25, 0.50, 0.95]
NIVEIS = [25, 50, 75, 100]
MAT_PRINCIPAIS = ["A1", "C5", "C2", "C4"]
MAT_COMPLEMENTARES = ["C1", "C3"]


def fr_nivel(mat, nivel):
    ref = MATERIAIS[mat]["FR_ref"]
    j = NIVEIS.index(nivel)
    return round(FR_MIN_CTCE0 + j / 3 * (ref - FR_MIN_CTCE0), 4)


def linha(sitio, mat, wn, fr, frrot, d, cal, exp, asw=None):
    wrot = "LOC" if asw is not None else wn
    pid = f"{sitio}_{mat}_W{wrot}_{frrot}_D{int(round(d*100)):02d}_{cal if d > 0 else 'CTRL'}"
    return dict(id=pid, experimento=exp, sitio=sitio, material=mat, nivel_agua=wrot,
                asw_max=round(asw if asw is not None else ASW_REF * wn / 100, 3),
                nivel_FR=frrot, FR=fr, desfolha=d, calendario=cal if d > 0 else "CTRL",
                eventos=";".join(EVENTOS[cal]) if d > 0 else "", plantio=PLANTIO,
                inicio=INICIO.get(mat, "2015-04"), fim=FIM,
                apto_analise_principal=not (sitio == "IMP" and mat == "A1"),
                modelo="r3PG v0.1.7 3-PGpjs (port Python verificado) + módulo de desfolha v1")


def montar_matriz():
    L = []
    for s, m, wn, fn in itertools.product(SITIOS, MAT_PRINCIPAIS, NIVEIS, NIVEIS):
        fr = fr_nivel(m, fn)
        L.append(linha(s, m, wn, fr, f"F{fn}", 0.0, "P1", "E1-E6"))
        for d, cal in itertools.product(DEFOL[1:], ["P1", "P2"]):
            L.append(linha(s, m, wn, fr, f"F{fn}", d, cal, "E1-E6"))
    for s, m, fr in itertools.product(SITIOS, MAT_PRINCIPAIS, [0.2, 0.4, 0.6, 0.8, 1.0]):  # E2 exploratório
        for d in (0.0, 0.50):
            L.append(linha(s, m, 100, fr, f"FX{int(fr*100):03d}", d, "P1", "E2x"))
    for m, n in itertools.product(MAT_COMPLEMENTARES, NIVEIS):  # complementares, Indianópolis, solo combinado
        for d in DEFOL:
            L.append(linha("IND", m, n, fr_nivel(m, n), f"F{n}", d, "P1", "COMPL"))
    for s, m, fn in itertools.product(SITIOS, MAT_PRINCIPAIS, NIVEIS):  # E7–E8: solo local, frequência anual e épocas
        fr = fr_nivel(m, fn)
        L.append(linha(s, m, None, fr, f"F{fn}", 0.0, "P1", "LOCAL", asw=SOLO_LOCAL[s]))
        for d, cal in itertools.product(DEFOL[1:], CAL_LOCAL):
            L.append(linha(s, m, None, fr, f"F{fn}", d, cal, "LOCAL", asw=SOLO_LOCAL[s]))
    M = pd.DataFrame(L).drop_duplicates("id").reset_index(drop=True)
    assert M.id.is_unique
    return M


_CLIMA = {}


def _clima(s):
    if s not in _CLIMA:
        _CLIMA[s] = clima_mensal(s)
    return _CLIMA[s]


def rodar(r):
    r = dict(r)
    mat = r["material"]; M = MATERIAIS[mat]
    site = dict(latitude=SITIOS[r["sitio"]]["lat"], altitude=0, soil_class=-1, asw_i=r["asw_max"], asw_min=0.0,
                asw_max=r["asw_max"], **{"from": r["inicio"], "to": r["fim"]})
    sp = dict(planted=r["plantio"], fertility=r["FR"], stems_n=10000 / 9,
              biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    ev = {e: r["desfolha"] for e in r["eventos"].split(";")} if r["eventos"] else None
    o = run_3pg_pjs(site, sp, _clima(r["sitio"]), params(mat), defoliation_events=ev)
    o.insert(0, "id", r["id"])
    o["idade_meses"] = (o.age * 12).round(6)
    o["mes_ref"] = (o.idade_meses - 12).round(6)          # mês k da simulação de referência
    o["biom_total"] = o.biom_stem + o.biom_foliage + o.biom_root
    o["lai_pos_defol"] = np.where(o.biom_defol > 0, (o.wf_pre_defol - o.biom_defol) * o.sla * 0.1, np.nan)
    return o


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    M = montar_matriz(); M.to_csv(SAIDA / "matriz_tratamentos.csv", index=False)
    t0 = time.time()
    with Pool(8) as p:
        res = p.map(rodar, M.to_dict("records"), chunksize=16)
    D = pd.concat(res, ignore_index=True)
    D.to_csv(SAIDA / "mensal.csv.gz", index=False, compression="gzip")
    json.dump(dict(n_tratamentos=len(M), n_linhas=len(D), segundos=round(time.time() - t0, 1),
                   python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                   asw_ref=ASW_REF, fr_min=FR_MIN_CTCE0, eventos=EVENTOS, plantio=PLANTIO, fim=FIM),
              open(SAIDA / "config_execucao.json", "w"), indent=2, ensure_ascii=False)
    print(len(M), "tratamentos;", len(D), "linhas;", round(time.time() - t0, 1), "s")
    print(M.groupby(["experimento"]).size().to_string())
