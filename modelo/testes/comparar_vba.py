"""Compara a trajetória mensal do port com a saída do 3-PG original (Excel/VBA)
incluída no r3PG (tests/r_vba_compare). Gera testes/saida_comparacao_vba.csv"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from threepg_pjs import run_3pg_pjs, params_from_table
R = AQUI.parents[2] / "fontes_r3PG"
INP = R / "tests/r_vba_compare/r3PG_input.xls"
OUT = R / "tests/r_vba_compare/VBA_3PG_output.xls"

def comparar():
    x = pd.read_excel(INP, sheet_name=None, engine="xlrd")
    dflt = pd.read_excel(R / "data-raw/data.default.xlsx", sheet_name="parameters")
    res = []
    for site_id, skip, nome in [("evergreen_pjs", 5, "Pinus sylvestris"), ("broadleaf_pjs", 235, "Fagus sylvatica")]:
        site = x["site"].set_index("site").loc[site_id].to_dict(); site["from"], site["to"] = site["from"], site["to"]
        sp = x["species"].set_index("site").loc[site_id].to_dict()
        clim = x["climate"][x["climate"].climate_id == "eumixfor_clim"].drop(columns="climate_id").dropna(axis=1, how="all")
        m = dict(zip(x["parameters"].parameter, x["parameters"][nome]))
        par = dflt[["parameter"]].copy(); par[nome] = [m.get(p, d) for p, d in zip(dflt.parameter, dflt.default)]
        sim = run_3pg_pjs(site, sp, clim, params_from_table(par, nome))
        vba = pd.read_excel(OUT, sheet_name="Output", skiprows=skip, nrows=111, engine="xlrd")
        pares = {"Stems1": "stems_n", "Foliage DM1": "biom_foliage", "Root DM1": "biom_root",
                 "Stem DM1": "biom_stem", "Stand volume1": "volume", "LAI1": "lai", "Mean DBH1": "dbh"}
        n = min(len(vba), len(sim))
        for cv, cs in pares.items():
            a = pd.to_numeric(vba[cv], errors="coerce").to_numpy()[:n]; b = sim[cs].to_numpy()[:n]
            ok = ~np.isnan(a)
            dif = np.abs(a[ok] - b[ok]); rel = dif / np.maximum(np.abs(a[ok]), 1e-12)
            res.append(dict(site=site_id, variavel=cs, meses=int(ok.sum()), max_dif_abs=dif.max(),
                            max_dif_rel=rel[np.abs(a[ok]) > 1e-9].max() if (np.abs(a[ok]) > 1e-9).any() else 0.0,
                            valor_final_vba=a[ok][-1], valor_final_port=b[ok][-1]))
    return pd.DataFrame(res)

if __name__ == "__main__":
    df = comparar(); df.to_csv(AQUI / "saida_comparacao_vba.csv", index=False)
    pd.set_option("display.width", 200); print(df.to_string())
