#!/usr/bin/env python3
"""Espaço de possibilidades do módulo (v2 + v3): danos combinados nos seis locais.

Pergunta: o talhão atacado pode recuperar e produzir mais que o controle? Em que condições? Os danos se somam?
Fatorial: 6 locais × 2 materiais (A1, C5) × d {0, 25, 50, 75, 95%} × frequência {pulso único em 2017, pulsos anuais
2017–2022} × época {jan, jul} × perda de eficiência r {0, 20, 40, 60%} × mortalidade m {0, 5, 15, 25%} × fisiologia
{original, calibrada (mediana do posterior; γ = 0,5)}. Convenções iguais às da plataforma Akademia (fonte2.html):
r reduz α nos 4 meses a partir de cada pulso; m mata árvores uma vez, no primeiro pulso. Solo local, FR de referência,
plantio jan/2015, 3 × 3 m, avaliação aos 84 meses de idade (k72). A1 em IMP, ALM e ARA = diagnóstico (f_T = 0).
Saídas: saida/possibilidades/."""
import itertools, json, sys
from multiprocessing import Pool
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
import run_experimentos as RE  # noqa: E402
from clima import SITIOS, BIOMA  # noqa: E402
from clones import MATERIAIS, params  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

OUT = AQUI / "saida" / "possibilidades"; OUT.mkdir(parents=True, exist_ok=True)
SOLO = dict(RE.SOLO_LOCAL, ALM=219.0, ARA=194.0, ELD=145.0)
CAL = json.load(open(AQUI.parent / "calibracao/saida/calibracao_d0999.json"))
COMP = dict(U=CAL["U"]["q50"], a=CAL["a"]["q50"], gam=0.5)
DIAG = {("IMP", "A1"), ("ALM", "A1"), ("ARA", "A1")}
MATS = ["A1", "C5"]; DS = [0, 25, 50, 75, 95]; RS = [0, 20, 40, 60]; MS = [0, 5, 15, 25]
FREQ = {"P1": [2017], "PA": list(range(2017, 2023))}; EPOCAS = [1, 7]
CL = {}


def mes(a, m):
    return f"{a + (m - 1) // 12}-{(m - 1) % 12 + 1:02d}"


def rodar(args):
    s, mat, d, fq, ep, r, m, versao = args
    if s not in CL:
        CL[s] = RE._clima(s)
    Mt = MATERIAIS[mat]; a = SOLO[s]
    site = dict(latitude=SITIOS[s]["lat"], altitude=0, soil_class=-1, asw_i=a, asw_min=0.0, asw_max=a,
                **{"from": RE.INICIO.get(mat, "2015-04"), "to": RE.FIM})
    sp = dict(planted="2015-01", fertility=Mt["FR_ref"], stems_n=10000 / 9, biom_stem=Mt["WS0"], biom_root=Mt["WR0"], biom_foliage=Mt["WF0"])
    anos = FREQ[fq]
    dv = {mes(y, ep): d / 100 for y in anos} if d else None
    ef = {mes(y, ep + i): r / 100 for y in anos for i in range(4)} if r else None
    mo = {mes(anos[0], ep): m / 100} if m else None
    o = run_3pg_pjs(site, sp, CL[s], params(mat), defoliation_events=dv, efficiency_events=ef, mortality_events=mo,
                    compensation=COMP if (versao == "calibrada" and d) else None)
    o["idade"] = (o.age * 12).round().astype(int); o = o.set_index("idade")
    k = 84; ev0 = 12 * (anos[0] - 2015) + ep - 1  # idade (meses) no mês do 1º evento (jan/2017 = 24)
    return dict(sitio=s, material=mat, d=d, freq=fq, epoca=ep, r=r, m=m, versao=versao,
                vol=o.volume[k], N=o.stems_n[k], dap=o.dbh[k], wf=o.biom_foliage[k],
                npp_serie=o.npp_f, ev0=ev0, wf_serie=o.biom_foliage)


def main():
    casos = [(s, mt, d, fq, ep, r, m, v) for s, mt, d, fq, ep, r, m, v in
             itertools.product(SITIOS, MATS, DS, FREQ, EPOCAS, RS, MS, ["original", "calibrada"])
             if (d or r or m)]  # sem desfolha, a versão calibrada coincide com a original (compensação só após desfolha)
    ctrl = [(s, mt, 0, "P1", 1, 0, 0, "original") for s, mt in itertools.product(SITIOS, MATS)]
    with Pool(2) as pool:
        C = {(x["sitio"], x["material"]): x for x in pool.map(rodar, ctrl)}
        T = pool.map(rodar, casos, chunksize=40)
    L = []
    for t in T:
        c = C[(t["sitio"], t["material"])]
        e0 = t["ev0"]; rel = (t["wf_serie"].loc[e0:84] / c["wf_serie"].loc[e0:84]).to_numpy(); ok = np.where(rel >= 0.95)[0]
        npp_t, npp_c = t["npp_serie"].loc[e0 + 12:84].sum(), c["npp_serie"].loc[e0 + 12:84].sum()
        L.append(dict({k: t[k] for k in ["sitio", "material", "d", "freq", "epoca", "r", "m", "versao"]},
                      bioma=BIOMA[t["sitio"]], apto=(t["sitio"], t["material"]) not in DIAG,
                      perda_volume=100 * (1 - t["vol"] / c["vol"]),
                      perda_por_arvore=100 * (1 - (t["vol"] / t["N"]) / (c["vol"] / c["N"])),
                      ganho_dap=100 * (t["dap"] / c["dap"] - 1),
                      npp_pos_rel=100 * (npp_t / npp_c - 1),
                      folhagem_84_rel=100 * (t["wf"] / c["wf"] - 1),
                      recup_folhas_meses=float(ok[ok > 0][0]) if (t["d"] and (ok > 0).any()) else np.nan))
    D = pd.DataFrame(L)
    # aditividade: perda combinada × soma das perdas de cada dano isolado (mesmas condições)
    chave = ["sitio", "material", "freq", "epoca", "versao"]
    so = lambda col, cond: D[cond].set_index(chave + [col]).perda_volume
    Sd = so("d", (D.r == 0) & (D.m == 0)); Sr = so("r", (D.d == 0) & (D.m == 0)); Sm = so("m", (D.d == 0) & (D.r == 0))
    def soma(row):
        k = tuple(row[c] for c in chave)
        g = lambda S, col: 0.0 if row[col] == 0 else S.get(k + (row[col],), np.nan)
        return g(Sd, "d") + g(Sr, "r") + g(Sm, "m")
    D["soma_isolados"] = D.apply(soma, axis=1)
    D["n_danos"] = (D[["d", "r", "m"]] > 0).sum(axis=1)
    D["interacao"] = D.perda_volume - D.soma_isolados
    D.to_csv(OUT / "possibilidades.csv", index=False)
    print(len(D), "cenários")


if __name__ == "__main__":
    main()
