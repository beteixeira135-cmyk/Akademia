#!/usr/bin/env python3
"""Complemento da busca bibliográfica com o Semantic Scholar (API Graph, busca em lote com operadores booleanos),
substituindo o OpenAlex, cujo limite diário compartilhado sem chave estava esgotado em 31/10 e 02/11/2026.
O Semantic Scholar incorporou o Microsoft Academic Graph, a mesma origem do OpenAlex. Mesmas expressões booleanas do
protocolo (O01–O07), traduzidas para a sintaxe da API (+ = E, | = OU). Período 1997–2026.
Depois aplica o MESMO filtro do núcleo (filtrar.py: D e (E ou modelo processual de árvores)) sobre título + resumo e
compara com o núcleo do Crossref por DOI e por título normalizado.
Saídas: crus_s2/*.jsonl, ../corpus/s2_nucleo.csv, ../corpus/s2_novos_no_nucleo.csv, ../corpus/s2_resumo.json"""
import json, re, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path
import pandas as pd

AQUI = Path(__file__).parent; CRU = AQUI / "crus_s2"; CRU.mkdir(exist_ok=True); OUT = AQUI.parent / "corpus"
D = '(defoliation | defoliated | herbivory | "insect damage" | "leaf removal" | "foliar damage" | "leaf damage")'
E = '(Eucalyptus | eucalypt | eucalypts)'
F = '(photosynthesis | photosynthetic | "carbon allocation" | "canopy conductance" | transpiration | "leaf area index" | carbohydrate | regrowth | compensation | compensatory)'
M = '("3-PG" | 3PG | r3PG | "3-PGmix" | CABALA | "process-based" | "process based" | ecophysiological)'
A = '(drought | "water stress" | "soil water" | fertilisation | fertilization | nitrogen | temperature | "climate change")'
V = '(calibration | Bayesian | validation | "independent test" | uncertainty | "sensitivity analysis")'
CONSULTAS = {"O01_DxE": f"{D} + {E}", "O02_DxExF": f"{D} + {E} + {F}", "O03_DxM": f"{D} + {M}", "O04_DxExA": f"{D} + {E} + {A}",
             "O05_DxMxV": f"{D} + {M} + {V}", "O06_3PGxE": f'("3-PG" | r3PG | "3-PGmix") + {E}',
             "O07_PT": "(desfolha | desfolhamento | herbivoria) + (eucalipto | Eucalyptus)"}
CAMPOS = "title,abstract,year,externalIds,venue,authors,citationCount,publicationTypes"


def get(u):
    for t in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "TCC-UFU"}), timeout=60))
        except Exception as e:
            err = e; time.sleep(4 * (t + 1))
    raise RuntimeError(f"{u}: {err}")


def norm_titulo(t):
    t = unicodedata.normalize("NFD", (t or "").lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


log = []
for cid, q in CONSULTAS.items():
    tok, n, tot, out = None, 0, None, open(CRU / f"s2_{cid}.jsonl", "w")
    while True:
        par = {"query": q, "fields": CAMPOS, "year": "1997-2026"}
        if tok: par["token"] = tok
        r = get("https://api.semanticscholar.org/graph/v1/paper/search/bulk?" + urllib.parse.urlencode(par))
        tot = r.get("total", tot)
        for it in r.get("data", []):
            out.write(json.dumps(it, ensure_ascii=False) + "\n"); n += 1
        tok = r.get("token")
        if not tok or n >= 5000: break
        time.sleep(1.2)
    out.close(); log.append(dict(consulta=cid, expressao=q, total_relatado=tot, baixados=n)); print(cid, tot, n); time.sleep(1.5)
pd.DataFrame(log).to_csv(AQUI / "log_consultas_semantic.csv", index=False)

# ---------- filtro do núcleo (mesmos descritores de filtrar.py)
import importlib.util
src = (AQUI / "filtrar.py").read_text(encoding="utf8"); g_src = src[src.index("G = {"):src.index("RG = ")]
mp_src = src[src.index("MPROC = "):src.index("TREE = ")]; tr_src = src[src.index("TREE = "):src.index("TIPOS_OK")]
ns = {"re": re}; exec(g_src + mp_src + tr_src, ns)
RG = {k: re.compile(v, re.I) for k, v in ns["G"].items()}; MPROC, TREE = ns["MPROC"], ns["TREE"]
regs = []
for f in sorted(CRU.glob("*.jsonl")):
    for ln in open(f, encoding="utf8"):
        r = json.loads(ln); ex = r.get("externalIds") or {}
        regs.append(dict(consulta=f.stem[3:], s2=r.get("paperId"), doi=(ex.get("DOI") or "").lower(), titulo=r.get("title") or "",
                         resumo=r.get("abstract") or "", ano=r.get("year"), periodico=r.get("venue") or "", citacoes=r.get("citationCount"),
                         autores="; ".join(a.get("name", "") for a in (r.get("authors") or []))))
S = pd.DataFrame(regs); n_bruto = len(S)
S = S.drop_duplicates("s2"); n_unicos = len(S)
S["tnorm"] = S.titulo.map(norm_titulo); S = S.sort_values("citacoes", ascending=False).drop_duplicates("tnorm")
txt = S.titulo + " " + S.resumo
for k, rg in RG.items(): S[k] = txt.str.contains(rg)
S["Mproc"] = txt.str.contains(MPROC); S["arvore"] = txt.str.contains(TREE)
NUC = S[S.D & (S.E | (S.Mproc & S.arvore)) & S.ano.between(1997, 2026)].copy()
CR = pd.read_csv(OUT / "corpus_nucleo.csv"); cr_doi = set(CR.doi.dropna().str.lower()); cr_t = set(CR.titulo.map(norm_titulo))
NUC["no_crossref"] = NUC.doi.isin(cr_doi) | NUC.tnorm.isin(cr_t)
NOV = NUC[~NUC.no_crossref].copy()
NUC.drop(columns=["tnorm"]).to_csv(OUT / "s2_nucleo.csv", index=False); NOV.drop(columns=["tnorm"]).sort_values("citacoes", ascending=False).to_csv(OUT / "s2_novos_no_nucleo.csv", index=False)
res = dict(data="2026-11-02", registros_baixados=int(n_bruto), unicos=int(n_unicos), apos_titulos_repetidos=int(len(S)), nucleo_s2=int(len(NUC)),
           nucleo_s2_ja_no_crossref=int(NUC.no_crossref.sum()), novos=int(len(NOV)), nucleo_combinado=int(len(CR) + len(NOV)),
           novos_D_Mproc=int((NOV.D & NOV.Mproc).sum()), novos_D_Mproc_E=int((NOV.D & NOV.Mproc & NOV.E).sum()),
           novos_BR=int(NOV.BR.sum()), novos_D_E_F=int((NOV.D & NOV.E & NOV.F).sum()))
json.dump(res, open(OUT / "s2_resumo.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(res, indent=1, ensure_ascii=False))
