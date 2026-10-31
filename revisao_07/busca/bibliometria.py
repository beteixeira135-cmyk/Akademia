"""Indicadores bibliométricos do corpus núcleo (equivalente em Python às funções descritivas do bibliometrix):
produção anual, periódicos, estudos e autores mais citados/produtivos, termos de título e assunto, coocorrência,
agrupamentos (modularidade gulosa), evolução temática por período, interseções entre grupos de descritores e lacunas.
Saídas: ../bibliometria/*.csv e *.png. Limitação: o Crossref não fornece palavras-chave de autor; usam-se termos
de título (e resumo, quando houver) e as interseções dos grupos de descritores do protocolo."""
import json, re, itertools, collections
from pathlib import Path
import pandas as pd, numpy as np, networkx as nx
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

C = Path(__file__).parent.parent / "corpus"; B = Path(__file__).parent.parent / "bibliometria"; B.mkdir(exist_ok=True)
N = pd.read_csv(C / "corpus_nucleo.csv").fillna("")
for k in "DEPFMAV": N[k] = N[k].astype(bool) if k in N else False
N["Mproc"] = N.Mproc.astype(bool); N["BR"] = N.BR.astype(bool)
res = {"n_nucleo": len(N)}
# 1. produção anual e por classe
ano = N.groupby("ano").size(); ano.to_csv(B / "producao_anual.csv", header=["n"])
plt.figure(figsize=(7, 3)); plt.bar(ano.index, ano.values, color="#5f6f34"); plt.title("Produção anual — corpus núcleo (Crossref)"); plt.ylabel("documentos")
plt.tight_layout(); plt.savefig(B / "fig_producao_anual.png", dpi=150); plt.close()
N.classe_doc.value_counts().to_csv(B / "por_classe.csv", header=["n"])
# 2. periódicos
N[N.periodico != ""].periodico.value_counts().head(20).to_csv(B / "periodicos_top20.csv", header=["n"])
# 3. estudos e autores
N.sort_values("citacoes", ascending=False)[["ano", "titulo", "periodico", "citacoes", "doi"]].head(25).to_csv(B / "estudos_mais_citados.csv", index=False)
nome = lambda a: (a.split(",")[0].strip().title() + ", " + (a.split(",")[1].strip()[:1] + ".") if "," in a else a.strip())
aut = collections.Counter(nome(a) for s in N.autores for a in s.split(";") if a.strip())
pd.Series(aut).sort_values(ascending=False).head(25).to_csv(B / "autores_mais_produtivos.csv", header=["n"])
# rede de coautoria
G = nx.Graph()
for s in N.autores:
    au = [nome(a) for a in s.split(";") if a.strip()]
    for a, b in itertools.combinations(sorted(set(au)), 2):
        G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
comp = sorted(nx.connected_components(G), key=len, reverse=True) if len(G) else []
res["coautoria"] = dict(autores=G.number_of_nodes(), ligacoes=G.number_of_edges(), componentes=len(comp), maior_componente=len(comp[0]) if comp else 0)
inst = collections.Counter(i.strip() for s in N.instituicoes for i in s.split(";") if i.strip())
pd.Series(inst, dtype=int).sort_values(ascending=False).head(20).to_csv(B / "instituicoes_top20.csv", header=["n"])
res["registros_com_afiliacao"] = int((N.instituicoes != "").sum())
# 4–5. termos e coocorrência
STOP = set("""a an the of in on and or to for with by from at as is are be into its their this that these those after under between
during effect effects study using use based new two three plant plants tree trees species growth de da do das dos e em no na nos nas
o os um uma para com por sobre entre sob ao à às pelo pela seus suas efeito efeitos was were not have has had been both however abstract also may most more can but all which than other such these results found within level levels significant significantly there our were while would could did does show showed shown using used high low""".split())
def termos(t):
    w = [x for x in re.findall(r"[a-záàâãéêíóôõúç\-]+", t.lower()) if len(x) > 2 and x not in STOP]
    return set(w)
TT = [termos(t + " " + r) for t, r in zip(N.titulo, N.resumo)]
freq = collections.Counter(w for s in TT for w in s)
top = [w for w, _ in freq.most_common(60)]
pd.Series(freq).sort_values(ascending=False).head(60).to_csv(B / "termos_frequentes.csv", header=["documentos"])
H = nx.Graph()
for s in TT:
    s = [w for w in s if w in top]
    for a, b in itertools.combinations(sorted(s), 2):
        H.add_edge(a, b, weight=H.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
H.remove_edges_from([(a, b) for a, b, d in H.edges(data=True) if d["weight"] < 2])
H.remove_nodes_from([n for n in list(H) if H.degree(n) == 0])
grupos = list(nx.algorithms.community.greedy_modularity_communities(H, weight="weight")) if len(H) else []
pd.DataFrame([dict(grupo=i + 1, termos=", ".join(sorted(g, key=lambda x: -freq[x])[:15]), n_termos=len(g)) for i, g in enumerate(grupos)]).to_csv(B / "agrupamentos_tematicos.csv", index=False)
if len(H):
    plt.figure(figsize=(9, 7)); pos = nx.spring_layout(H, seed=1, k=0.6)
    cor = {n: i for i, g in enumerate(grupos) for n in g}
    nx.draw_networkx(H, pos, node_size=[40 + 12 * freq[n] for n in H], node_color=[cor.get(n, 0) for n in H], cmap="tab10",
                     width=[0.3 + 0.3 * d["weight"] for *_, d in H.edges(data=True)], font_size=7, edge_color="#bbbbbb")
    plt.axis("off"); plt.title("Coocorrência de termos (título/resumo), corpus núcleo"); plt.tight_layout(); plt.savefig(B / "fig_coocorrencia.png", dpi=150); plt.close()
# 8. evolução temática por período
N["periodo"] = pd.cut(N.ano, [1996, 2006, 2016, 2026], labels=["1997–2006", "2007–2016", "2017–2026"])
ev = []
for p_, g in N.groupby("periodo", observed=True):
    f = collections.Counter(w for t, r in zip(g.titulo, g.resumo) for w in termos(t + " " + r))
    ev.append(dict(periodo=p_, n=len(g), termos=", ".join(w for w, _ in f.most_common(12))))
pd.DataFrame(ev).to_csv(B / "evolucao_tematica.csv", index=False)
# 9. interseções dos grupos do protocolo
inter = {"D∧E": int((N.D & N.E).sum()), "D∧E∧F (fisiologia)": int((N.D & N.E & N.F).sum()), "D∧E∧A (ambiente)": int((N.D & N.E & N.A).sum()),
         "D∧modelo processual": int((N.D & N.Mproc).sum()), "D∧modelo processual∧E": int((N.D & N.Mproc & N.E).sum()),
         "D∧modelo processual∧V (calibração/validação/incerteza)": int((N.D & N.Mproc & N.V).sum()),
         "D∧E∧BR (Brasil)": int((N.D & N.E & N.BR).sum()), "D∧E∧F∧A": int((N.D & N.E & N.F & N.A).sum())}
pd.Series(inter).to_csv(B / "intersecoes.csv", header=["documentos"]); res["intersecoes"] = inter
# listas para Q4, Q6, Q7
N[N.D & N.Mproc][["ano", "titulo", "periodico", "doi"]].to_csv(B / "Q4_modelos_processuais_e_dano.csv", index=False)
N[N.D & N.E & N.BR][["ano", "titulo", "periodico", "doi"]].to_csv(B / "Q6_brasil.csv", index=False)
N[N.D & N.V][["ano", "titulo", "periodico", "doi"]].to_csv(B / "Q7_calibracao_validacao.csv", index=False)
json.dump(res, open(B / "resumo_bibliometria.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
