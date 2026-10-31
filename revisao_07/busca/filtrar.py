"""Deduplicação, filtro booleano documentado e classificação do corpus (Missão 07, etapa 3).
Entrada: crus/*.jsonl (Crossref; e OpenAlex, se houver). Saídas em ../corpus/:
  corpus_bruto_deduplicado.csv, corpus_nucleo.csv, corpus_contexto_3pg.csv, exclusoes.csv, corpus_nucleo.bib, resumo_filtro.json
Os campos pesquisados são título + resumo (quando o Crossref o fornece) + assuntos; isso é declarado como limitação."""
import json, re, html, unicodedata
from pathlib import Path
import pandas as pd

AQUI = Path(__file__).parent; OUT = AQUI.parent / "corpus"; OUT.mkdir(exist_ok=True)
# ---------------- grupos de descritores (expressões regulares; equivalentes aos operadores OR de cada grupo)
G = {
    "D": r"defoliat|desfolh|herbivor|insect damage|leaf removal|foliar damage|leaf damage|leaf loss|pest damage|"
         r"leaf.area loss|crown damage|defoliator|lagarta desfolhadora|leaf.feeding insect",
    "E": r"eucalypt|eucalipt|corymbia",
    "P": r"pest|praga|disease|doen[çc]a|psyllid|psil[ií]deo|rust\b|ferrugem|mycosphaerella|teratosphaeria|leaf.cutting ant|formiga|thaumastocoris|glycaspis|thyrinteina",
    "BR": r"brazil|brasil|minas gerais|s[ãa]o paulo|bahia|paran[áa]|mato grosso|cerrado",
    "F": r"photosynth|carbon allocation|carbon partition|biomass allocation|canopy conductance|stomatal|transpiration|"
         r"leaf area index|\blai\b|carbohydrate|non.structural|regrowth|refoliat|compensat|recovery|recupera",
    "M": r"\b3.?pg\b|r3pg|3.?pgmix|cabala|process.based|process based|ecophysiological model|physiological model|"
         r"forest growth model|growth model|simulation model|cenw|g.day|biome.bgc|forest.bgc|pnet|\blpj|cable model|modelagem|modelo",
    "A": r"drought|water stress|water deficit|water availab|soil water|fertili[sz]|nitrogen|nutrient|temperature|"
         r"climate change|vapou?r pressure|\bvpd\b|d[eé]ficit h[ií]drico|adubação",
    "V": r"calibrat|bayesian|validat|independent test|uncertaint|sensitivity analys|calibra[çc]|valida[çc]",
}
RG = {k: re.compile(v, re.I) for k, v in G.items()}
MPROC = re.compile(r"\b3.?pg\b|r3pg|3.?pgmix|cabala|process.based|process based|ecophysiological model|physiological model|"
                   r"cenw|g.day|biome.bgc|forest.bgc|pnet|\blpj|cable model|carbon.balance model", re.I)
TREE = re.compile(r"forest|tree|plantation|stand|eucalypt|pinus|pine|wood", re.I)
TIPOS_OK = {"journal-article", "proceedings-article", "book-chapter", "dissertation", "report", "monograph", "posted-content",
            "book", "edited-book", "reference-entry", "report-component"}


def limpa(x):
    x = html.unescape(re.sub(r"<[^>]+>", " ", x or "")); return re.sub(r"\s+", " ", x).strip()


def norm_titulo(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


regs = []
for f in sorted((AQUI / "crus").glob("*.jsonl")):
    base, cid = f.stem.split("_", 1)
    for ln in open(f, encoding="utf8"):
        r = json.loads(ln)
        regs.append(dict(base=base, consulta=cid, doi=(r.get("DOI") or "").lower(), titulo=limpa(" ".join(r.get("title") or [])),
                         resumo=limpa(r.get("abstract")), assuntos="; ".join(r.get("subject") or []),
                         ano=((r.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                         periodico=limpa(" ".join(r.get("container-title") or [])), tipo=r.get("type"), editora=r.get("publisher"),
                         citacoes=r.get("is-referenced-by-count"),
                         autores="; ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in (r.get("author") or [])),
                         instituicoes="; ".join(sorted({af.get("name", "") for a in (r.get("author") or []) for af in (a.get("affiliation") or []) if af.get("name")}))))
R = pd.DataFrame(regs)
n_bruto = len(R)
cons = R.groupby("doi").consulta.apply(lambda s: ";".join(sorted(set(s))))
R = R.drop_duplicates("doi").set_index("doi"); R["consultas"] = cons; R = R.reset_index()
n_doi = len(R)
R["tnorm"] = R.titulo.map(norm_titulo)
R = R.sort_values("citacoes", ascending=False).drop_duplicates("tnorm").copy()  # duplicatas de título (versões/preprints)
n_dedup = len(R)
txt = (R.titulo + " " + R.resumo + " " + R.assuntos)
for k, rg in RG.items():
    R[k] = txt.str.contains(rg)
R["Mproc"] = txt.str.contains(MPROC); R["arvore"] = txt.str.contains(TREE)
R["tem_resumo"] = R.resumo.str.len() > 0
R["classe_doc"] = R.tipo.map(lambda t: {"journal-article": "artigo", "dissertation": "tese/dissertação", "report": "literatura técnica",
                                         "monograph": "livro/literatura técnica", "book": "livro/literatura técnica", "book-chapter": "capítulo",
                                         "proceedings-article": "anais", "posted-content": "preprint"}.get(t, "outro"))
R.loc[R.titulo.str.contains(r"\breview\b|revis[aã]o|meta.analys", case=False) & (R.classe_doc == "artigo"), "classe_doc"] = "revisão"
# ---------------- critérios
def motivo(r):
    if r.tipo not in TIPOS_OK: return f"tipo excluído ({r.tipo})"
    if not r.titulo: return "sem título"
    if not (r.ano and 1997 <= r.ano <= 2026): return "fora do período"
    if r.D and (r.E or (r.Mproc and r.arvore)): return ""
    return "não atende à expressão booleana do núcleo"
R["motivo_exclusao"] = R.apply(motivo, axis=1)
NUC = R[R.motivo_exclusao == ""].copy()
CTX = R[(R.motivo_exclusao.isin(["", "não atende à expressão booleana do núcleo"])) & txt.loc[R.index].str.contains(r"\b3.?pg\b|r3pg|3.?pgmix", case=False)
        & (R.E | R.V)].copy()
cols = ["doi", "titulo", "ano", "periodico", "tipo", "classe_doc", "autores", "instituicoes", "citacoes", "assuntos", "consultas",
        "D", "E", "P", "BR", "F", "M", "Mproc", "A", "V", "tem_resumo", "resumo"]
R[cols + ["motivo_exclusao"]].to_csv(OUT / "corpus_bruto_deduplicado.csv", index=False)
NUC[cols].sort_values(["ano", "titulo"]).to_csv(OUT / "corpus_nucleo.csv", index=False)
CTX[cols].sort_values(["ano", "titulo"]).to_csv(OUT / "corpus_contexto_3pg.csv", index=False)
R[R.motivo_exclusao != ""].motivo_exclusao.value_counts().rename_axis("motivo").reset_index(name="n").to_csv(OUT / "exclusoes.csv", index=False)


def bib(r):
    chave = re.sub(r"[^A-Za-z]", "", (r.autores.split(",")[0] if r.autores else "anon")) + str(r.ano)
    campos = dict(title=r.titulo, author=" and ".join(a for a in r.autores.split("; ") if a), year=r.ano, journal=r.periodico, doi=r.doi)
    tipo = {"artigo": "article", "revisão": "article", "tese/dissertação": "phdthesis", "capítulo": "incollection", "anais": "inproceedings"}.get(r.classe_doc, "misc")
    return f"@{tipo}{{{chave}_{r.doi.split('/')[-1][:20]},\n" + ",\n".join(f"  {k} = {{{v}}}" for k, v in campos.items() if v) + "\n}\n"
(OUT / "corpus_nucleo.bib").write_text("".join(bib(r) for r in NUC.itertuples()), encoding="utf8")
resumo = dict(registros_baixados=n_bruto, unicos_por_doi=n_doi, apos_dedup_titulo=n_dedup, nucleo=len(NUC), contexto_3pg=len(CTX),
              nucleo_com_resumo=int(NUC.tem_resumo.sum()), nucleo_por_classe=NUC.classe_doc.value_counts().to_dict())
json.dump(resumo, open(OUT / "resumo_filtro.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(resumo, indent=1, ensure_ascii=False))
