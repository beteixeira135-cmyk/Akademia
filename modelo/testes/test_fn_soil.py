import warnings
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fn_soil import fN_soil, species_with_soil_fertility  # noqa: E402


def test_fN_sem_coeficientes_retorna_nan_e_avisa():
    with pytest.warns(RuntimeWarning, match="não disponíveis"):
        result = fN_soil([1.0, 2.0], [0.1, 0.2])
    assert result.shape == (2,)
    assert np.isnan(result).all()


def test_fN_preserva_na_sem_avisar_quando_tudo_esta_ausente():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = fN_soil([np.nan, 1.0], [0.1, np.nan])
    assert np.isnan(result).all()
    assert not caught


def test_fN_rejeita_comprimento_tipo_e_teores_negativos():
    with pytest.raises(ValueError, match="mesmo comprimento"):
        fN_soil([1.0], [0.1, 0.2])
    with pytest.raises(TypeError, match="C deve ser numérico"):
        fN_soil(["1"], [0.1])
    with pytest.raises(ValueError, match="não podem ser negativos"):
        fN_soil([-1.0], [0.1])


def test_adaptador_preserva_fertilidade_manual_por_padrao():
    species = {"fertility": 0.8, "planted": "2015-01"}
    adapted = species_with_soil_fertility(species, 1.0, 0.1)
    assert adapted == species
    assert adapted is not species


def test_adaptador_nao_ativa_sem_forma_e_coeficientes():
    with pytest.warns(RuntimeWarning, match="não disponíveis"):
        with pytest.raises(ValueError, match="mantenha a fertility manual"):
            species_with_soil_fertility(
                {"fertility": 0.8}, 1.0, 0.1, enabled=True
            )
