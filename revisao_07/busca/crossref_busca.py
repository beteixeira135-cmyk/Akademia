"""Busca reproduzível no Crossref (api.crossref.org), 1997-01-01 a 2026-10-31.
O Crossref não aceita expressões booleanas: cada consulta é texto livre ordenado por relevância; o filtro booleano
documentado em protocolo.md é aplicado depois, localmente, sobre título + resumo + assunto (filtrar.py).
Saída: crus/crossref_<id>.jsonl (um registro por linha) e log_consultas.csv (data, consulta, filtros, total, baixados)."""
import json, time, csv, datetime as dt, urllib.parse, urllib.request
from pathlib import Path

AQUI = Path(__file__).parent; CRU = AQUI / "crus"; CRU.mkdir(exist_ok=True)
MAIL = "beteixeira135@gmail.com"  # polite pool do Crossref (identificação do autor da pesquisa)
FILTRO = "from-pub-date:1997-01-01,until-pub-date:2026-10-31"
LIM = 500  # registros por consulta (os mais relevantes)
CONSULTAS = {
    "C01": "eucalyptus defoliation growth",
    "C02": "eucalypt defoliation",
    "C03": "eucalyptus herbivory insect damage growth",
    "C04": "eucalyptus artificial defoliation leaf removal",
    "C05": "eucalyptus defoliation photosynthesis compensation",
    "C06": "defoliation photosynthetic upregulation carbon allocation trees",
    "C07": "defoliation canopy conductance transpiration trees",
    "C08": "defoliation carbohydrate reserves regrowth trees",
    "C09": "3-PG model defoliation",
    "C10": "3-PG forest growth model pest insect damage",
    "C11": "CABALA model defoliation eucalyptus",
    "C12": "process-based forest model insect defoliation net primary production",
    "C13": "eucalyptus defoliation drought water stress",
    "C14": "eucalyptus defoliation nitrogen fertilisation",
    "C15": "3-PG eucalyptus calibration validation",
    "C16": "3-PG Bayesian calibration",
    "C17": "desfolha eucalipto crescimento",
    "C18": "desfolhamento artificial eucalipto",
    "C19": "lagarta desfolhadora eucalipto perda",
    "C20": "forest model defoliation uncertainty sensitivity analysis",
}


def get(url):
    for t in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"TCC-UFU-cienciometria (mailto:{MAIL})"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            time.sleep(10 * (t + 1))
    raise RuntimeError(url)


if __name__ == "__main__":
    log = []
    for cid, q in CONSULTAS.items():
        n, tot, out = 0, None, open(CRU / f"crossref_{cid}.jsonl", "w")
        while n < LIM:
            url = ("https://api.crossref.org/works?" + urllib.parse.urlencode(
                dict(query=q, filter=FILTRO, rows=100, offset=n, sort="score", order="desc", mailto=MAIL,
                     select="DOI,title,author,issued,container-title,type,abstract,subject,is-referenced-by-count,publisher")))
            m = get(url)["message"]; tot = m["total-results"]; it = m["items"]
            if not it: break
            for r in it[: LIM - n]:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += len(it[: LIM - n])
            time.sleep(2.5)
        out.close()
        log.append(dict(base="Crossref", id=cid, consulta=q, filtros=FILTRO + "; sort=score desc (relevância), paginação por offset", data=dt.date.today().isoformat(),
                        total_relatado=tot, baixados=n))
        print(cid, tot, n, flush=True)
    with open(AQUI / "log_consultas_crossref.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)
