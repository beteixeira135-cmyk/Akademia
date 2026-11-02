"""Auditoria da calibração (Missão 07, etapa 6). Não altera dados nem a calibração publicada no TCC; só testa
se as conclusões resistem a: (1) reexecução; (2) priores e escala de σ diferentes; (3) ajuste com uma única
variável; (4) atribuição da melhora no urocam a cada mecanismo. Saída: saida/auditoria_calibracao.json."""
import json, numpy as np
import protocolo as p

obs = p.observado("C5"); VS = ["volume", "CAP", "altura"]
obsA = p.observado("A1")


def grade(Umax=1.35, sig_esc=10.0, vars_=VS, d=0.999, nU=36, nA=41):
    U = np.linspace(1.0, Umax, nU); A = np.linspace(0.0, 1.0, nA)
    SIG = np.linspace(0.5, 40, 160); ps = np.exp(-0.5 * (SIG / sig_esc) ** 2)
    y = np.array([obs[v] for v in vars_]); G = []
    for u in U:
        for a in A:
            L = p.perdas("C5", {"U": u, "a": a}, d=d); m = np.array([L[v] for v in vars_])
            sse = ((m - y) ** 2).sum()
            G.append((u, a, (ps * SIG ** (-len(vars_)) * np.exp(-sse / (2 * SIG ** 2))).sum()))
    G = np.array(G); w = G[:, 2] / G[:, 2].sum()

    def q(col, qq):
        o = np.argsort(G[:, col]); c = np.cumsum(w[o]); return float(G[o, col][np.searchsorted(c, qq)])
    return dict(U=[q(0, .05), q(0, .5), q(0, .95)], a=[q(1, .05), q(1, .5), q(1, .95)],
                U_massa_no_limite=float(w[G[:, 0] >= Umax - 1e-9].sum()))


out = {}
J = json.load(open("saida/calibracao_d0999.json"))
r = grade(); out["reexecucao"] = dict(U=r["U"], a=r["a"], publicado_U=[J["U"]["q05"], J["U"]["q50"], J["U"]["q95"]],
                                      publicado_a=[J["a"]["q05"], J["a"]["q50"], J["a"]["q95"]])
out["prior_U_ate_1_6"] = grade(Umax=1.6, nU=61)
out["sigma_escala_5"] = grade(sig_esc=5.0); out["sigma_escala_20"] = grade(sig_esc=20.0)
out["so_volume"] = grade(vars_=["volume"])
out["so_CAP"] = grade(vars_=["CAP"])
med = dict(U=J["U"]["q50"], a=J["a"]["q50"])
attr = {}
for nome, comp in [("original", None), ("so_U", {"U": med["U"]}), ("so_a", {"a": med["a"]}), ("U_e_a", med),
                   ("U_e_a_gama1", dict(med, gam=1.0))]:
    attr[nome] = {k: v for k, v in p.perdas("A1", comp).items() if k != "altura"}
out["atribuicao_urocam"] = dict(observado={k: obsA[k] for k in ["volume", "CAP"]}, **attr)
c5 = {}
for nome, comp in [("so_U", {"U": med["U"]}), ("so_a", {"a": med["a"]})]:
    c5[nome] = p.perdas("C5", comp)
out["atribuicao_urograndis"] = c5
json.dump(out, open("saida/auditoria_calibracao.json", "w"), indent=1)
print(json.dumps(out, indent=1))
