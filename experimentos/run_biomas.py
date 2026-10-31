#!/usr/bin/env python3
"""Bloco LOCAL nos 6 locais (um por bioma onde há eucalipto + os 3 originais), módulo original (v2) e calibrado (v3).
Mesma convenção, materiais, níveis de FR, intensidades e calendários do bloco LOCAL do TCC (run_experimentos.py).
Calibrado = mediana do posterior (calibracao/saida/calibracao_d0999.json): U, a; γ = 0,5 (mediana do prior,
não identificável). Incerteza: 200 amostras do posterior para d = 50% (P1 e PA), FR de referência.
Saídas em experimentos/saida/biomas/."""
import itertools, json, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
import run_experimentos as RE  # noqa: E402
import indicadores as IN  # noqa: E402
from clima import SITIOS, BIOMA  # noqa: E402
from clones import MATERIAIS, params  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

OUT = AQUI / "saida" / "biomas"; OUT.mkdir(parents=True, exist_ok=True)
SOLO = dict(RE.SOLO_LOCAL, ALM=219.0, ARA=194.0, ELD=145.0)
# ALM e ARA: SoilGrids 2.0 (WCS, 8 pontos a ~9 km) + PTF-ZARC; ELD: TECHS 6 (Binkley et al., 2017, Tab. 2)
CAL = json.load(open(AQUI.parent / "calibracao/saida/calibracao_d0999.json"))
COMP_MED = dict(U=CAL["U"]["q50"], a=CAL["a"]["q50"], gam=0.5)
DIAG = {("IMP", "A1"), ("ALM", "A1"), ("ARA", "A1")}  # f_T = 0 em vários meses: diagnóstico de extrapolação


def matriz():
    L = []
    for s, m, fn in itertools.product(SITIOS, RE.MAT_PRINCIPAIS, RE.NIVEIS):
        fr = RE.fr_nivel(m, fn)
        L.append(RE.linha(s, m, None, fr, f"F{fn}", 0.0, "P1", "BIOMA", asw=SOLO[s]))
        for d, cal in itertools.product(RE.DEFOL[1:], RE.CAL_LOCAL):
            L.append(RE.linha(s, m, None, fr, f"F{fn}", d, cal, "BIOMA", asw=SOLO[s]))
    M = pd.DataFrame(L)
    M["apto_analise_principal"] = [(s, m) not in DIAG for s, m in zip(M.sitio, M.material)]
    M["bioma"] = M.sitio.map(BIOMA)
    return M


def rodar(args):
    r, comp = args
    mat = r["material"]; Mt = MATERIAIS[mat]
    site = dict(latitude=SITIOS[r["sitio"]]["lat"], altitude=0, soil_class=-1, asw_i=r["asw_max"], asw_min=0.0,
                asw_max=r["asw_max"], **{"from": r["inicio"], "to": r["fim"]})
    sp = dict(planted=r["plantio"], fertility=r["FR"], stems_n=10000 / 9, biom_stem=Mt["WS0"], biom_root=Mt["WR0"], biom_foliage=Mt["WF0"])
    ev = {e: r["desfolha"] for e in r["eventos"].split(";")} if r["eventos"] else None
    o = run_3pg_pjs(site, sp, RE._clima(r["sitio"]), params(mat), defoliation_events=ev,
                    compensation=comp if r["eventos"] else None)
    o.insert(0, "id", r["id"])
    o["idade_meses"] = (o.age * 12).round(6); o["mes_ref"] = (o.idade_meses - 12).round().astype(int)
    o["biom_total"] = o.biom_stem + o.biom_foliage + o.biom_root
    o["lai_pos_defol"] = np.where(o.biom_defol > 0, (o.wf_pre_defol - o.biom_defol) * o.sla * 0.1, np.nan)
    return o[["id", "date", "mes_ref", "idade_meses", "biom_foliage", "biom_stem", "biom_root", "biom_total", "lai", "dbh",
              "height", "volume", "npp_f", "gpp", "apar", "asw", "f_sw", "stems_n", "biom_defol", "wf_pre_defol",
              "lai_pos_defol", "biom_incr_foliage", "biom_incr_stem", "biom_incr_root"]]


def incerteza(pool, M):
    A = pd.read_csv(AQUI.parent / "calibracao/saida/amostras_posterior_d0999.csv")
    base = M[(M.nivel_FR == "F100") & (((M.desfolha == 0.5) & M.calendario.isin(["P1", "PA"])) | (M.desfolha == 0))]
    ctrl = {r["id"]: o for r, o in zip(base[base.desfolha == 0].to_dict("records"),
                                       pool.map(rodar, [(r, None) for r in base[base.desfolha == 0].to_dict("records")]))}
    linhas = []
    trat = base[base.desfolha > 0].to_dict("records")
    for r in trat:
        cid = r["id"].rsplit("_D", 1)[0] + "_D00_CTRL"
        c = ctrl[cid].set_index("mes_ref")
        outs = pool.map(rodar, [(r, dict(U=a.U, a=a.a, gam=a.gam)) for a in A.itertuples()], chunksize=10)
        perdas = [100 * (1 - o.set_index("mes_ref").at[72, "volume"] / c.at[72, "volume"]) for o in outs]
        linhas.append(dict(sitio=r["sitio"], bioma=BIOMA[r["sitio"]], material=r["material"], calendario=r["calendario"],
                           apto=r["apto_analise_principal"], perda_vol_k72_media=np.mean(perdas),
                           q05=np.quantile(perdas, .05), q50=np.median(perdas), q95=np.quantile(perdas, .95)))
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    t0 = time.time(); M = matriz(); M.to_csv(OUT / "matriz_biomas.csv", index=False)
    with Pool(8) as pool:
        for versao, comp in [("original", None), ("calibrado", COMP_MED)]:
            res = pool.map(rodar, [(r, comp) for r in M.to_dict("records")], chunksize=16)
            D = pd.concat(res, ignore_index=True)
            R = IN.calcular(M.drop(columns=["bioma"]), D)
            R.insert(1, "versao", versao); R.insert(2, "bioma", R.sitio.map(BIOMA))
            R.to_csv(OUT / f"indicadores_{versao}.csv", index=False)
            print(versao, len(R), "tratamentos", round(time.time() - t0), "s", flush=True)
        U = incerteza(pool, M); U.to_csv(OUT / "incerteza_posterior_d50.csv", index=False)
    json.dump(dict(n_tratamentos=len(M), comp_mediana=COMP_MED, solo=SOLO, diagnostico=sorted(map(list, DIAG)),
                   segundos=round(time.time() - t0)), open(OUT / "config_biomas.json", "w"), indent=1, ensure_ascii=False)
    print("total", round(time.time() - t0), "s")
