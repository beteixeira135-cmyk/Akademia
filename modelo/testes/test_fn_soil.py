import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fn_soil import fN_bown  # noqa: E402


def test_fN_bown_aplica_equacao_publicada_sem_truncar():
    result = fN_bown([0.2, 0.5], [20.0, 30.0])
    assert result == pytest.approx([0.718, 0.615])
    assert fN_bown(0.5, 10.0).item() > 1.0


def test_fN_bown_preserva_ausencias_e_rejeita_entradas_invalidas():
    assert np.isnan(fN_bown([np.nan, 0.2], [15.0, np.nan])).all()
    with pytest.raises(ValueError, match="mesmo comprimento"):
        fN_bown([0.2], [15.0, 20.0])
    with pytest.raises(TypeError, match="N_pct deve ser numérico"):
        fN_bown(["0.2"], [15.0])
    with pytest.raises(ValueError, match="não pode ser negativo"):
        fN_bown([-0.2], [15.0])
