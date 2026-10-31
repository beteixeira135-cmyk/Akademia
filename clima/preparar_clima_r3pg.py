#!/usr/bin/env python3
"""
Auditoria e agregação mensal do NASA POWER diário para o r3PG.

Uso: python3 -I preparar_clima_r3pg.py <POWER_diario.csv> <PAR_mensal.csv> <pasta_saida>

Convenções verificadas no arquivo (ver relatório):
  separador ';', decimal ',', 1 linha final vazia, sem cabeçalho de metadados do POWER,
  sem códigos -999. Datas: YEAR + DOY (dia juliano, horário LST).

Agregação (segue as entradas exigidas por r3PG::prepare_climate):
  tmp_min, tmp_max : média mensal de T2M_MIN e T2M_MAX (°C)
  tmp_ave          : NÃO fornecido -> r3PG calcula (tmp_min+tmp_max)/2 ; aqui gravado igual
  prcp             : soma mensal de PRECTOTCORR (mm/mês)
  srad             : média mensal de ALLSKY_SFC_SW_DWN (MJ m-2 dia-1)
  frost_days       : nº de dias com T2M_MIN <= 0 °C
  vpd_day          : fórmula interna do r3PG (get_vpd) aplicada às médias mensais (mbar)
  vpd_rh_alt       : alternativa para sensibilidade = es(Tmédia)*(1-RH/100), média mensal (mbar)
Mês só é exportado se tiver 100% dos dias.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

f_dia, f_mes, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)

d = pd.read_csv(f_dia, sep=";", decimal=",")
d = d.loc[:, ~d.columns.str.startswith("Unnamed")].dropna(how="all")
d[["YEAR", "DOY"]] = d[["YEAR", "DOY"]].astype(int)
d["date"] = pd.to_datetime(d.YEAR.astype(str), format="%Y") + pd.to_timedelta(d.DOY - 1, unit="D")
vars_ = [c for c in d.columns if c not in ("YEAR", "DOY", "date")]

# ---------- auditoria ----------
full = pd.date_range(d.date.min(), d.date.max())
aud = dict(
    arquivo=f_dia.name, linhas_dados=int(len(d)),
    inicio=str(d.date.min().date()), fim=str(d.date.max().date()),
    dias_faltantes=int(len(full.difference(d.date))), datas_duplicadas=int(d.date.duplicated().sum()),
    codigos_menos999=int((d[vars_] <= -990).sum().sum()), nan=int(d[vars_].isna().sum().sum()),
    tmax_menor_que_tmin=int((d.T2M_MAX < d.T2M_MIN).sum()),
    dias_tmin_le_0=int((d.T2M_MIN <= 0).sum()),
    razao_PAR_SW_media=round(float((d.ALLSKY_SFC_PAR_TOT / d.ALLSKY_SFC_SW_DWN).mean()), 4),
    faixas={c: [round(float(d[c].min()), 2), round(float(d[c].max()), 2)] for c in vars_},
)

# ---------- agregação mensal ----------
def es(t):  # pressão de vapor de saturação (mbar), mesma forma de r3PG:::get_vpd
    return 6.10780 * np.exp(17.2690 * t / (237.30 + t))

d["year"], d["month"] = d.date.dt.year, d.date.dt.month
d["vpd_rh_dia"] = es((d.T2M_MAX + d.T2M_MIN) / 2) * (1 - d.RH2M / 100)
g = d.groupby(["year", "month"])
m = pd.DataFrame(dict(
    n_dias=g.size(),
    tmp_min=g.T2M_MIN.mean(), tmp_max=g.T2M_MAX.mean(),
    prcp=g.PRECTOTCORR.sum(), srad=g.ALLSKY_SFC_SW_DWN.mean(),
    frost_days=g.T2M_MIN.apply(lambda x: int((x <= 0).sum())),
    rh_media=g.RH2M.mean(), vpd_rh_alt=g.vpd_rh_dia.mean(),
)).reset_index()
m["dias_no_mes"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1)).dt.days_in_month
m["completo"] = m.n_dias == m.dias_no_mes
m["tmp_ave"] = (m.tmp_min + m.tmp_max) / 2
m["vpd_day"] = (es(m.tmp_max) - es(m.tmp_min)) / 2      # idêntico a r3PG:::get_vpd
m = m.round(4)
aud["meses_completos"] = int(m.completo.sum()); aud["meses_incompletos"] = int((~m.completo).sum())

cols_r3pg = ["year", "month", "tmp_min", "tmp_max", "tmp_ave", "prcp", "srad", "frost_days", "vpd_day"]
m[m.completo][cols_r3pg].to_csv(out / "clima_r3pg_mensal_POWER.csv", index=False)
m.to_csv(out / "clima_mensal_completo_com_controles.csv", index=False)

# ---------- consistência com o arquivo mensal de PAR ----------
p = pd.read_csv(f_mes, sep=";", encoding="utf-8"); p.columns = ["year", "mes_txt", "PAR_mensal"]
p = p[p.mes_txt != "ANN"].copy(); p["month"] = pd.to_datetime(p.mes_txt, format="%b").dt.month
pm = d.groupby(["year", "month"], as_index=False).ALLSKY_SFC_PAR_TOT.mean()
j = p.merge(pm, on=["year", "month"], how="left")
j["diferenca"] = (j.PAR_mensal - j.ALLSKY_SFC_PAR_TOT).round(4)
j.to_csv(out / "consistencia_PAR_mensal_vs_diario.csv", index=False)
aud["PAR_mensal_meses"] = int(len(p)); aud["PAR_meses_sobrepostos"] = int(j.ALLSKY_SFC_PAR_TOT.notna().sum())
aud["PAR_max_abs_diferenca"] = float(j.diferenca.abs().max())

# ---------- resumo anual (somente anos completos) ----------
def max_seca(x, lim=1.0):  # maior sequência de dias com prcp < 1 mm (convenção ETCCDI 'CDD')
    best = run = 0
    for v in x:
        run = run + 1 if v < lim else 0; best = max(best, run)
    return best

a = d.groupby("year").agg(n_dias=("date", "size"), tmean_C=("T2M_MAX", lambda s: np.nan),
                          tmin_C=("T2M_MIN", "mean"), tmax_C=("T2M_MAX", "mean"),
                          precip_mm=("PRECTOTCORR", "sum"), radiation_MJ_m2_day=("ALLSKY_SFC_SW_DWN", "mean"),
                          max_consecutive_dry_days=("PRECTOTCORR", max_seca)).reset_index()
a["tmean_C"] = (a.tmin_C + a.tmax_C) / 2
a["vpd_kPa_r3pg"] = d.groupby("year").apply(lambda x: ((es(x.T2M_MAX) - es(x.T2M_MIN)) / 2).mean() / 10).values
a["ano_completo"] = a.n_dias >= 365
a.round(3).to_csv(out / "resumo_anual_POWER.csv", index=False)

json.dump(aud, open(out / "auditoria_clima.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps({k: v for k, v in aud.items() if k != "faixas"}, indent=1, ensure_ascii=False))
