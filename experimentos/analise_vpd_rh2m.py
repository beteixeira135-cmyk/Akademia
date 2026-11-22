"""Compara a entrada VPD padrão do 3-PG com uma estimativa alternativa baseada em RH2M."""
from pathlib import Path
import sys

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "modelo"))

import clima  # noqa: E402
from clones import MATERIAIS, params  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

SITIOS = ("IND", "TB", "IMP")
ASW_LOCAL = {"IND": 215.0, "TB": 214.0, "IMP": 210.0}
DATA_INICIO = "2016-01"
DATA_FIM = "2023-01"
DATA_PLANTIO = "2015-01"
ATAQUE = {"2017-01": 0.50}
DATA_AVALIACAO = "2022-01-31"


def perda_volume(controle, tratamento):
    c = controle.set_index(controle.date.astype(str))
    t = tratamento.set_index(tratamento.date.astype(str))
    if DATA_AVALIACAO not in c.index or DATA_AVALIACAO not in t.index:
        raise ValueError(f"Data de avaliação ausente: {DATA_AVALIACAO}")
    vc = float(c.loc[DATA_AVALIACAO, "volume"])
    vt = float(t.loc[DATA_AVALIACAO, "volume"])
    if vc <= 0:
        raise ValueError(f"Volume de controle não positivo em {DATA_AVALIACAO}: {vc}")
    return vc, vt, 100 * (1 - vt / vc)


def executar():
    linhas = []
    for sitio in SITIOS:
        clima_padrao = clima.clima_mensal(sitio)
        rh = clima.vpd_rh2m_mensal(sitio)
        mensal = clima_padrao.merge(rh, on=["year", "month"], validate="one_to_one")
        if mensal.vpd_rh2m.isna().any():
            raise ValueError(f"{sitio}: falha ao parear VPD mensal")
        mensal["date"] = pd.to_datetime(
            dict(year=mensal.year, month=mensal.month, day=1)
        )
        inicio = pd.Timestamp(DATA_INICIO + "-01")
        fim = pd.Timestamp(DATA_FIM + "-01")
        meses_processados = (mensal.date > inicio) & (mensal.date <= fim)

        latitude = clima.SITIOS[sitio]["lat"]
        material = MATERIAIS["A1"]
        solo = {
            "latitude": latitude,
            "altitude": 0,
            "soil_class": -1,
            "asw_i": ASW_LOCAL[sitio],
            "asw_min": 0,
            "asw_max": ASW_LOCAL[sitio],
            "from": DATA_INICIO,
            "to": DATA_FIM,
        }
        especie = {
            "planted": DATA_PLANTIO,
            "fertility": material["FR_ref"],
            "stems_n": 10000 / 9,
            "biom_stem": material["WS0"],
            "biom_root": material["WR0"],
            "biom_foliage": material["WF0"],
        }

        saidas = {}
        for metodo, coluna in (
            ("proxy_Tmin_Tmax", "vpd_day"),
            ("alternativa_Tmax_Tmin_RH2M", "vpd_rh2m"),
        ):
            entrada = mensal.drop(columns=["vpd_day", "vpd_rh2m"]).copy()
            entrada["vpd_day"] = mensal[coluna].to_numpy()
            controle = run_3pg_pjs(solo, especie, entrada, params("A1"))
            tratamento = run_3pg_pjs(
                solo, especie, entrada, params("A1"), defoliation_events=ATAQUE
            )
            vol_controle, vol_tratamento, perda = perda_volume(controle, tratamento)
            meses = controle.index > 0
            saidas[metodo] = {
                "vpd_medio_mbar": float(mensal.loc[meses_processados, coluna].mean()),
                "f_vpd_medio": float(controle.loc[meses, "f_vpd"].mean()),
                "volume_controle_m3_ha": vol_controle,
                "volume_desfolha_m3_ha": vol_tratamento,
                "perda_volume_pct": perda,
            }

        base = saidas["proxy_Tmin_Tmax"]
        alt = saidas["alternativa_Tmax_Tmin_RH2M"]
        linhas.append(
            {
                "sitio": sitio,
                "cenario": "A1; ataque isolado de 50% em 2017-01; sem compensacao",
                "status": "diagnóstico (fT=0; fora da análise principal)" if sitio == "IMP"
                else "análise principal",
                "periodo_entrada": "2016-01 a 2023-01",
                "data_avaliacao": DATA_AVALIACAO,
                "asw_max_mm": solo["asw_max"],
                "vpd_proxy_medio_mbar": base["vpd_medio_mbar"],
                "vpd_rh2m_medio_mbar": alt["vpd_medio_mbar"],
                "diferenca_vpd_media_mbar": alt["vpd_medio_mbar"] - base["vpd_medio_mbar"],
                "fvpd_proxy_medio": base["f_vpd_medio"],
                "fvpd_rh2m_medio": alt["f_vpd_medio"],
                "volume_controle_proxy_m3_ha": base["volume_controle_m3_ha"],
                "volume_controle_rh2m_m3_ha": alt["volume_controle_m3_ha"],
                "perda_volume_proxy_pct": base["perda_volume_pct"],
                "perda_volume_rh2m_pct": alt["perda_volume_pct"],
                "diferenca_perda_pp": alt["perda_volume_pct"] - base["perda_volume_pct"],
            }
        )

    resultado = pd.DataFrame(linhas)
    destino = HERE / "saida" / "analise_vpd_rh2m.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(destino, index=False, float_format="%.8f")
    print(resultado.to_string(index=False))
    print(f"\nSaída gravada em: {destino.relative_to(ROOT)}")


if __name__ == "__main__":
    executar()
