"""Carrega os dados de exemplo e os parâmetros padrão do r3PG v0.1.7 (data-raw/*.xlsx)."""
import os
from pathlib import Path
import pandas as pd
# fonte do r3PG v0.1.7 (git clone github.com/trotsiuk/r3PG); pode ser indicada por R3PG_SRC
RAIZ = Path(os.environ.get("R3PG_SRC", Path(__file__).resolve().parents[3] / "fontes_r3PG")) / "data-raw"

def carregar():
    x = pd.read_excel(RAIZ / "data.input.xlsx", sheet_name=None)
    dflt = pd.read_excel(RAIZ / "data.default.xlsx", sheet_name="parameters")
    site = x["site"].iloc[0].to_dict()
    sp = x["species"].set_index("species")
    par = dflt[["parameter", "default"]].copy()
    for s in sp.index:   # r3PG: valores fornecidos substituem os padrões
        par[s] = par["default"]
        m = dict(zip(x["parameters"].parameter, x["parameters"][s]))
        par[s] = [m.get(p, d) for p, d in zip(par.parameter, par["default"])]
    return site, sp, x["climate"], par
