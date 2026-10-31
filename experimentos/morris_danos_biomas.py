#!/usr/bin/env python3
"""Morris e catálogo de danos nos 6 locais. Usa o material C5 (Borges, 2009), válido em todos os locais
(o A1 é diagnóstico em IMP, ALM e ARA). Reaproveita sem alterar as definições de analise.py (morris_sitio)
e danos_v2.py (CENARIOS, indicadores); só o material, os locais e o solo mudam. Danos com remoção de
folhas rodam também com a compensação calibrada (mediana do posterior)."""
import json, sys
from multiprocessing import Pool
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent; sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
import run_experimentos as RE  # noqa: E402
from run_biomas import SOLO, COMP_MED  # noqa: E402
from clima import SITIOS, BIOMA, clima_mensal  # noqa: E402
from clones import params, MATERIAIS  # noqa: E402
import threepg_pjs as T  # noqa: E402
RE.SOLO_LOCAL.update(SOLO)
B = AQUI / "saida" / "biomas"
# --- definições copiadas por execução parcial dos scripts originais (sem rodar os experimentos deles) ---
src = (AQUI / "danos_v2.py").read_text(encoding="utf8"); ns = {"__file__": str(AQUI / "danos_v2.py")}
exec(src.split("linhas = []")[0], ns)
CENARIOS, meses, indic = ns["CENARIOS"], ns["meses"], ns["indicadores"]
PARS = ["alphaCx", "k", "y", "gammaFx", "SLA0", "SLA1", "pRx", "pRn", "pFS2", "pFS20", "aWs", "nWs", "Topt", "Tmax",
        "Tmin", "CoeffCond", "MaxCond", "fracBB1", "MaxAge", "gammaR", "LAIgcx"]


def sim(sitio, mat="C5", **ev):
    M = MATERIAIS[mat]; asw = SOLO[sitio]
    site = dict(latitude=SITIOS[sitio]["lat"], altitude=0, soil_class=-1, asw_i=asw, asw_min=0.0, asw_max=asw,
                **{"from": RE.INICIO.get(mat, "2015-04"), "to": "2023-01"})
    sp = dict(planted="2015-01", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    o = T.run_3pg_pjs(site, sp, clima_mensal(sitio), ev.pop("P", params(mat)), **ev)
    o["idade"] = (o.age * 12).round().astype(int)
    return o.set_index("idade")


def morris(sitio, r_traj=25, niveis=4):
    base = params("C5"); pars = [p for p in PARS if p in base and base[p] != 0]
    lo = {p: base[p] * 0.9 for p in pars}; hi = {p: base[p] * 1.1 for p in pars}
    rng = np.random.default_rng(20261030); delta = niveis / (2 * (niveis - 1)); grade = np.arange(niveis) / (niveis - 1)

    def avalia(x):
        P = dict(base); P.update({p: lo[p] + x[i] * (hi[p] - lo[p]) for i, p in enumerate(pars)})
        c = sim(sitio, P=dict(P)); t = sim(sitio, P=dict(P), defoliation_events={"2017-01": 0.5})
        return np.array([100 * (1 - t.volume[84] / c.volume[84]), c.volume[84]])
    EE = {p: [] for p in pars}
    for _ in range(r_traj):
        x = rng.choice(grade[:niveis // 2], size=len(pars)).astype(float); y0 = avalia(x)
        for i in rng.permutation(len(pars)):
            x2 = x.copy(); x2[i] = x[i] + delta; y1 = avalia(x2); EE[pars[i]].append((y1 - y0) / delta); x, y0 = x2, y1
    return [dict(sitio=sitio, bioma=BIOMA[sitio], parametro=p, resposta=n, mu_estrela=np.nanmean(np.abs(np.array(EE[p])[:, j])),
                 sigma=np.nanstd(np.array(EE[p])[:, j])) for p in pars for j, n in enumerate(["perda_volume_84_pp", "volume_ctrl_84"])]


def danos(sitio):
    c = sim(sitio); out = []
    for nome, praga, mec, ev, fonte, tipo in CENARIOS:
        for versao in ["original", "calibrado"]:
            if versao == "calibrado" and "defoliation_events" not in ev:
                continue
            e = dict(ev); e = {k: dict(v) for k, v in e.items()}
            if versao == "calibrado":
                e["compensation"] = COMP_MED
            t = sim(sitio, **e)
            out.append(dict(sitio=sitio, bioma=BIOMA[sitio], material="C5", cenario=nome, mecanismo=mec, versao=versao,
                            **indic(c, t, {k: v for k, v in ev.items()})))
    return out


if __name__ == "__main__":
    with Pool(6) as pool:
        MO = pd.DataFrame(sum(pool.map(morris, list(SITIOS)), [])).round(4)
        DA = pd.DataFrame(sum(pool.map(danos, list(SITIOS)), [])).round(3)
    MO.to_csv(B / "morris_C5_6locais.csv", index=False); DA.to_csv(B / "danos_6locais.csv", index=False)
    top = MO[MO.resposta == "perda_volume_84_pp"].sort_values("mu_estrela", ascending=False).groupby("sitio").head(3)
    print(top[["sitio", "parametro", "mu_estrela", "sigma"]].to_string(index=False))
    print(DA.pivot_table(index=["cenario", "versao"], columns="sitio", values="perda_volume_84", sort=False).round(1).to_string())
