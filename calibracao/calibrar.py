"""Calibração bayesiana da compensação (U, a) contra Bertulio et al. (2008), clone urograndis (simulado com C5).
Verossimilhança gaussiana nas perdas ajustadas pela linha de base (volume, CAP, altura; pontos percentuais),
com desvio σ desconhecido marginalizado numericamente (prior meia-normal, escala 10 p.p.). Priores uniformes:
U ~ U(1; 1,35) (aumento de até 35% da fotossíntese: Pinkard et al., 1998, citado por Quentin et al., 2011);
a ~ U(0; 1). γ (condutância) foi calibrado antes, com Quentin et al. (2011) (calibrar_gamma.py), e fica fixo aqui.
Correção de 02/11/2026: a versão anterior ajustava com γ = 0 e simulava com γ = 0,5, embora γ altere as perdas do C5.
Validação independente: urocam (Bertulio) simulado com A1, que não entra no ajuste."""
import json, sys, numpy as np, pandas as pd
import protocolo as p
GAMMA = json.load(open("saida/gamma_quentin2011.json"))["gamma_calibrado"]  # γ calibrado com Quentin et al. (2011), fixo na calibração de U e a
d_ev = float(sys.argv[1]) if len(sys.argv) > 1 else 0.999
U = np.round(np.arange(1.0, 1.3501, 0.01), 3); A = np.round(np.arange(0.0, 1.0001, 0.025), 3)
obs = p.observado("C5"); vs = ["volume", "CAP", "altura"]; y = np.array([obs[v] for v in vs])
SIG = np.linspace(0.5, 40, 160); prior_sig = np.exp(-0.5 * (SIG / 10) ** 2)
linhas = []
for u in U:
    for a in A:
        L = p.perdas("C5", {"U": u, "a": a, "gam": GAMMA}, d=d_ev); m = np.array([L[v] for v in vs])
        sse = float(((m - y) ** 2).sum())
        lik = (prior_sig * SIG ** -3 * np.exp(-sse / (2 * SIG ** 2))).sum()
        linhas.append(dict(U=u, a=a, sse=sse, lik=lik, **{f"L_{v}": L[v] for v in vs}))
G = pd.DataFrame(linhas); G["post"] = G.lik / G.lik.sum()
def resumo(col):
    s = G.groupby(col).post.sum(); c = s.cumsum()
    return dict(media=float((s.index * s).sum()), q05=float(s.index[(c >= 0.05).argmax()]), q50=float(s.index[(c >= 0.5).argmax()]),
                q95=float(s.index[(c >= 0.95).argmax()]))
best = G.loc[G.sse.idxmin()]
post_pred = {v: float((G[f"L_{v}"] * G.post).sum()) for v in vs}
# amostras do posterior para validação e propagação
rng = np.random.default_rng(2026); idx = rng.choice(len(G), size=200, p=G.post.values)
amostras = G.iloc[idx][["U", "a"]].reset_index(drop=True); amostras["gam"] = GAMMA
val = []
obsA = p.observado("A1")
for r in amostras.itertuples():
    L = p.perdas("A1", {"U": r.U, "a": r.a, "gam": r.gam}, d=d_ev); val.append(dict(volume=L["volume"], CAP=L["CAP"]))  # γ = GAMMA nas amostras
V = pd.DataFrame(val); L0 = p.perdas("A1", None, d=d_ev); L0c = p.perdas("C5", None, d=d_ev)
out = dict(d_evento=d_ev, observado_C5=obs, original_C5={v: L0c[v] for v in vs},
           U=resumo("U"), a=resumo("a"), corr_post=float(np.cov(np.vstack([G.U, G.a]), aweights=G.post)[0, 1] / np.sqrt(np.cov(G.U, aweights=G.post) * np.cov(G.a, aweights=G.post))),
           melhor_ajuste=dict(U=float(best.U), a=float(best.a), **{v: float(best[f"L_{v}"]) for v in vs}),
           preditiva_media_C5=post_pred,
           validacao_A1_urocam=dict(observado={k: obsA[k] for k in ["volume", "CAP"]}, original={k: L0[k] for k in ["volume", "CAP"]},
                                    calibrado_media={k: float(V[k].mean()) for k in V}, calibrado_q05={k: float(V[k].quantile(.05)) for k in V},
                                    calibrado_q95={k: float(V[k].quantile(.95)) for k in V}))
tag = str(d_ev).replace(".", "")
G.to_csv(f"saida/grade_posterior_d{tag}.csv", index=False); amostras.to_csv(f"saida/amostras_posterior_d{tag}.csv", index=False)
json.dump(out, open(f"saida/calibracao_d{tag}.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
