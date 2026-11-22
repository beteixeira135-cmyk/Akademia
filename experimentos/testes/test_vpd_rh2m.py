import numpy as np
import pandas as pd
import pytest

import clima


def _dias(rh2m):
    return pd.DataFrame(
        {
            "date": pd.date_range("2020-01-01", periods=31, freq="D"),
            "T2M_MAX": 20.0,
            "T2M_MIN": 10.0,
            "RH2M": rh2m,
        }
    )


def test_vpd_rh2m_mensal_usa_media_diaria_de_umidade(monkeypatch):
    monkeypatch.setattr(clima, "ler_diario", lambda _: _dias(50.0))

    resultado = clima.vpd_rh2m_mensal("IND")
    es_medio = (
        6.10780 * np.exp(17.2690 * 20.0 / (237.30 + 20.0))
        + 6.10780 * np.exp(17.2690 * 10.0 / (237.30 + 10.0))
    ) / 2.0

    assert resultado.loc[0, "vpd_rh2m"] == pytest.approx(es_medio * 0.5)


@pytest.mark.parametrize("rh2m", [-0.1, 100.1])
def test_vpd_rh2m_rejeita_umidade_fora_da_faixa(monkeypatch, rh2m):
    monkeypatch.setattr(clima, "ler_diario", lambda _: _dias(rh2m))

    with pytest.raises(ValueError, match="RH2M fora do intervalo"):
        clima.vpd_rh2m_mensal("IND")
