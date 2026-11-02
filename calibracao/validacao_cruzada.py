#!/usr/bin/env python3
"""Validação cruzada da calibração da compensação com as cinco observações de Bertulio et al. (2008):
urograndis (C5) — perda de volume, CAP e altura; urocam (A1) — perda de volume e CAP (d = 0,999).

(1) k = 5, deixa uma observação de fora: o posterior de (U, a) é recalculado com as outras quatro, com a mesma
    verossimilhança gaussiana e σ marginalizado (prior meia-normal, escala 10 p.p.) de calibrar.py, e a observação
    deixada de fora é prevista pela média preditiva do posterior.
(2) k = 2, deixa um material de fora: ajusta no C5 e prevê o A1 (desenho do TCC) e o inverso.
Comparação: o modelo original (sem compensação) com as mesmas observações. As cinco observações vêm do mesmo experimento
(local, datas e protocolo), portanto isto mede a capacidade preditiva dentro do experimento, não a validação independente.
Saída: saida/validacao_cruzada.json e saida/validacao_cruzada_previsoes.csv"""
import json
import numpy as np, pandas as pd
import protocolo as p
GAMMA = json.load(open("saida/gamma_quentin2011.json"))["gamma_calibrado"]  # γ calibrado com Quentin et al. (2011), fixo na calibração de U e a
U_MESES = json.load(open("saida/regra_compensacao.json"))["u_meses"]  # U só no mês do ataque (Turnbull et al., 2007; Quentin et al., 2012)

D_EV = 0.999
U = np.round(np.arange(1.0, 1.3501, 0.01), 3); A = np.round(np.arange(0.0, 1.0001, 0.025), 3)
SIG = np.linspace(0.5, 40, 160); PRIOR_SIG = np.exp(-0.5 * (SIG / 10) ** 2)
ROT = [("C5", "volume"), ("C5", "CAP"), ("C5", "altura"), ("A1", "volume"), ("A1", "CAP")]
y = np.array([p.observado(m)[v] for m, v in ROT])

G = pd.read_csv("saida/grade_posterior_d0999.csv")[["U", "a", "L_volume", "L_CAP", "L_altura"]]
G = G.rename(columns={"L_volume": "C5_volume", "L_CAP": "C5_CAP", "L_altura": "C5_altura"})
a1 = []
for r in G.itertuples():  # A1 com o mesmo γ calibrado (Quentin et al., 2011)
    L = p.perdas("A1", {"U": r.U, "a": r.a, "gam": GAMMA, "u_meses": U_MESES}, d=D_EV); a1.append((L["volume"], L["CAP"]))
G["A1_volume"], G["A1_CAP"] = zip(*a1)
M = G[[f"{m}_{v}" for m, v in ROT]].to_numpy()
orig = np.array([p.perdas(m, None, d=D_EV)[v] for m, v in ROT])  # módulo original (sem compensação)


def posterior(idx):
    sse = ((M[:, idx] - y[idx]) ** 2).sum(axis=1)
    n = len(idx)
    lik = (PRIOR_SIG[None, :] * SIG[None, :] ** (-n) * np.exp(-sse[:, None] / (2 * SIG[None, :] ** 2))).sum(axis=1)
    return lik / lik.sum()


linhas = []
for i in range(5):
    w = posterior([j for j in range(5) if j != i])
    linhas.append(dict(esquema="deixa uma observação de fora (k = 5)", material=ROT[i][0], variavel=ROT[i][1], observado=y[i],
                       original=orig[i], calibrado=float(w @ M[:, i]), U_post=float(w @ G.U), a_post=float(w @ G.a)))
for treino, teste in [("C5", "A1"), ("A1", "C5")]:
    tr = [j for j, (m, _) in enumerate(ROT) if m == treino]
    w = posterior(tr)
    for i, (m, v) in enumerate(ROT):
        if m == teste:
            linhas.append(dict(esquema=f"ajusta no {treino}, prevê o {teste} (k = 2)", material=m, variavel=v, observado=y[i],
                               original=orig[i], calibrado=float(w @ M[:, i]), U_post=float(w @ G.U), a_post=float(w @ G.a)))
P = pd.DataFrame(linhas)
P["erro_original"] = P.original - P.observado; P["erro_calibrado"] = P.calibrado - P.observado
P.to_csv("saida/validacao_cruzada_previsoes.csv", index=False)
res = {}
for esq, g in P.groupby("esquema", sort=False):
    rq = lambda e: float(np.sqrt((e ** 2).mean()))
    res[esq] = dict(n=len(g), RQEM_original=rq(g.erro_original), RQEM_calibrado=rq(g.erro_calibrado),
                    vies_original=float(g.erro_original.mean()), vies_calibrado=float(g.erro_calibrado.mean()),
                    melhorou=int((g.erro_calibrado.abs() < g.erro_original.abs()).sum()))
json.dump(res, open("saida/validacao_cruzada.json", "w"), indent=1, ensure_ascii=False)
print(P.round(2).to_string()); print(json.dumps(res, indent=1, ensure_ascii=False))
