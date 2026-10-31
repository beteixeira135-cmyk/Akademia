"""Clima mensal para o r3PG a partir dos CSV diários NASA POWER (API, comunidade AG, 2015–2024).
Agregação: tmp_min/tmp_max = média mensal; prcp = soma; srad = média (MJ m-2 d-1);
frost_days = nº de dias com T2M_MIN <= 0 °C; tmp_ave e vpd_day = fórmulas internas do r3PG
(prepare_climate: (Tmin+Tmax)/2 e ½[es(Tmax)−es(Tmin)], VPD diurno do 3-PG, em mbar)."""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1] / "clima" / "power_api"
SITIOS = {
    "IND": dict(nome="Indianópolis-MG", arquivo="POWER_daily_indianopolis_20150101_20241231.csv",
                lat=-19.0389, lon=-47.9169, papel="estudo de caso principal"),
    "TB": dict(nome="Telêmaco Borba-PR", arquivo="POWER_daily_telemaco_borba_20150101_20241231.csv",
               lat=-24.3239, lon=-50.6158, papel="extrapolação (clima subtropical; 8 dias com Tmin<=0)"),
    "IMP": dict(nome="Imperatriz-MA", arquivo="POWER_daily_imperatriz_20150101_20241231.csv",
                lat=-5.52583, lon=-47.4758, papel="extrapolação (clima quente)"),
    # Locais por bioma (bioma predominante do município: IBGE, 2024). Coordenadas: OpenStreetMap (Nominatim).
    "ALM": dict(nome="Almeirim-PA (Monte Dourado)", arquivo="POWER_daily_almeirim_monte_dourado_20150101_20241231.csv",
                lat=-0.8654, lon=-52.5396, papel="Amazônia; plantios da Jari (McNabb e Wadouski, 1999)"),
    "ARA": dict(nome="Araripina-PE", arquivo="POWER_daily_araripina_20150101_20241231.csv",
                lat=-7.5769, lon=-40.5039, papel="Caatinga; clones do Polo Gesseiro do Araripe (IPA)"),
    "ELD": dict(nome="Eldorado do Sul-RS", arquivo="POWER_daily_eldorado_do_sul_20150101_20241231.csv",
                lat=-30.0232, lon=-51.3830, papel="Pampa; sítio TECHS 6 (Binkley et al., 2017)"),
}
BIOMA = {"IND": "Cerrado", "IMP": "Cerrado", "TB": "Mata Atlântica", "ALM": "Amazônia", "ARA": "Caatinga", "ELD": "Pampa"}


def ler_diario(caminho):
    linhas = open(caminho, encoding="utf-8").read().splitlines()
    ini = next(i for i, l in enumerate(linhas) if l.startswith("YEAR,"))
    d = pd.read_csv(caminho, skiprows=ini)
    if (d <= -990).any().any():
        raise ValueError(f"{caminho}: códigos -999 presentes")
    d["date"] = pd.to_datetime(d.YEAR.astype(str), format="%Y") + pd.to_timedelta(d.DOY - 1, unit="D")
    full = pd.date_range(d.date.min(), d.date.max())
    if len(full.difference(d.date)):
        raise ValueError(f"{caminho}: dias faltantes")
    return d


def clima_mensal(sitio):
    d = ler_diario(RAIZ / SITIOS[sitio]["arquivo"])
    g = d.groupby([d.date.dt.year.rename("year"), d.date.dt.month.rename("month")])
    m = pd.DataFrame(dict(tmp_min=g.T2M_MIN.mean(), tmp_max=g.T2M_MAX.mean(), prcp=g.PRECTOTCORR.sum(),
                          srad=g.ALLSKY_SFC_SW_DWN.mean(),
                          frost_days=g.T2M_MIN.apply(lambda x: int((x <= 0).sum())),
                          n=g.size())).reset_index()
    dim = pd.to_datetime(dict(year=m.year, month=m.month, day=1)).dt.days_in_month
    if (m.n != dim).any():
        raise ValueError("mês incompleto")
    es = lambda t: 6.10780 * np.exp(17.2690 * t / (237.30 + t))
    m["tmp_ave"] = (m.tmp_min + m.tmp_max) / 2
    m["vpd_day"] = (es(m.tmp_max) - es(m.tmp_min)) / 2
    return m.drop(columns="n")
