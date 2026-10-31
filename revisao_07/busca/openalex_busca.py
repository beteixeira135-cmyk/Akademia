"""Busca booleana no OpenAlex (title_and_abstract.search aceita AND/OR/NOT e aspas), 1997-01-01 a 2026-10-31.
Complementa o Crossref, que não aceita booleanos. Saída: crus/openalex_<id>.jsonl e log_consultas_openalex.csv.
Observação: na execução de 31/10/2026 22h50 UTC, a API respondeu "Rate limit exceeded" (orçamento diário compartilhado
sem chave esgotado); rodar de novo após 00h UTC ou com chave (variável OPENALEX_KEY)."""
import json, os, time, csv, datetime as dt, urllib.parse, urllib.request
from pathlib import Path
AQUI = Path(__file__).parent; CRU = AQUI / "crus"; CRU.mkdir(exist_ok=True)
D = '(defoliation OR defoliated OR herbivory OR "insect damage" OR "leaf removal" OR "foliar damage" OR "leaf damage")'
E = '(Eucalyptus OR eucalypt OR eucalypts)'
F = '(photosynthesis OR photosynthetic OR "carbon allocation" OR "canopy conductance" OR transpiration OR "leaf area index" OR carbohydrate OR regrowth OR compensation OR compensatory)'
M = '("3-PG" OR 3PG OR r3PG OR "3-PGmix" OR CABALA OR "process-based" OR "process based" OR ecophysiological)'
A = '(drought OR "water stress" OR "soil water" OR fertilisation OR fertilization OR nitrogen OR temperature OR "climate change")'
V = '(calibration OR Bayesian OR validation OR "independent test" OR uncertainty OR "sensitivity analysis")'
CONSULTAS = {
    "O01_DxE": f"{D} AND {E}",
    "O02_DxExF": f"{D} AND {E} AND {F}",
    "O03_DxM": f"{D} AND {M}",
    "O04_DxExA": f"{D} AND {E} AND {A}",
    "O05_DxMxV": f"{D} AND {M} AND {V}",
    "O06_3PGxE": f'("3-PG" OR r3PG OR "3-PGmix") AND {E}',
    "O07_PT": "(desfolha OR desfolhamento OR herbivoria) AND (eucalipto OR Eucalyptus)",
}
FILTRO = "from_publication_date:1997-01-01,to_publication_date:2026-10-31"


def get(u):
    for t in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "TCC-UFU (mailto:beteixeira135@gmail.com)"}), timeout=60))
        except Exception as e:
            err = e; time.sleep(5 * (t + 1))
    raise RuntimeError(f"{u}: {err}")


if __name__ == "__main__":
    log = []; key = os.environ.get("OPENALEX_KEY")
    for cid, q in CONSULTAS.items():
        cursor, n, out, tot = "*", 0, open(CRU / f"openalex_{cid}.jsonl", "w"), None
        while cursor and n < 2000:
            par = {"filter": f"{FILTRO},title_and_abstract.search:{q}", "per-page": 200, "cursor": cursor, "mailto": "beteixeira135@gmail.com"}
            if key: par["api_key"] = key
            m = get("https://api.openalex.org/works?" + urllib.parse.urlencode(par)); tot = m["meta"]["count"]
            for r in m["results"]:
                out.write(json.dumps(r, ensure_ascii=False) + "\n"); n += 1
            cursor = m["meta"].get("next_cursor") if m["results"] else None; time.sleep(0.5)
        out.close(); log.append(dict(base="OpenAlex", id=cid, consulta=q, filtros=FILTRO, data=dt.date.today().isoformat(), total_relatado=tot, baixados=n))
        print(cid, tot, n, flush=True)
    with open(AQUI / "log_consultas_openalex.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)
