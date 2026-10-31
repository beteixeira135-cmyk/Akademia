"""
Testes dos módulos de dano v2: perda de eficiência fotossintética (α_C · (1 − r)) e
mortalidade induzida (remoção da fração m de árvores com a biomassa média).
Usam o caso de referência do r3PG (Pinus sylvestris); verificam o código, não o eucalipto.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from threepg_pjs import run_3pg_pjs, params_from_table, pulsos  # noqa: E402
from dados_referencia_r3pg import carregar  # noqa: E402

SITE, SP, CLIM, PAR = carregar()
SPEC = SP.loc["Pinus sylvestris"].to_dict()
PARS = params_from_table(PAR, "Pinus sylvestris")
rodar = lambda **kw: run_3pg_pjs(SITE, SPEC, CLIM, PARS, **kw)
K = 30


@pytest.fixture(scope="module")
def ctrl():
    return rodar()


def ym(k):
    return list(pulsos(SITE["from"], [k], 0.1))[0]


def test_eventos_nulos_identicos(ctrl):
    z = rodar(efficiency_events={ym(K): 0.0}, mortality_events={ym(K): 0.0})
    cols = [c for c in ctrl.columns if c != "wf_pre_defol"]
    pd.testing.assert_frame_equal(ctrl[cols], z[cols], check_exact=True)


@pytest.mark.parametrize("r", [0.1, 0.3, 0.6])
def test_eficiencia_reduz_alpha_e_gpp_no_mes(ctrl, r):
    o = rodar(efficiency_events={ym(K): r})
    assert o.alpha_c.iloc[K] == pytest.approx(ctrl.alpha_c.iloc[K] * (1 - r), rel=1e-12)
    # estado igual até o mês anterior -> GPP potencial igual; a água pode limitar só depois
    pd.testing.assert_series_equal(o.biom_stem.iloc[:K], ctrl.biom_stem.iloc[:K], check_exact=True)
    assert o.gpp.iloc[K] <= ctrl.gpp.iloc[K] * (1 - r) + 1e-12
    assert o.effic_loss.iloc[K] == r and (o.effic_loss.drop(index=K) == 0).all()


@pytest.mark.parametrize("m", [0.05, 0.15, 0.5])
def test_mortalidade_remove_fracao_e_conserva_arvore_media(ctrl, m):
    o = rodar(mortality_events={ym(K): m})
    n_antes = ctrl.stems_n.iloc[K - 1]
    b_antes = ctrl[["biom_foliage", "biom_root", "biom_stem"]].iloc[K - 1].sum()
    assert o.mort_induced.iloc[K] == pytest.approx(m * n_antes, rel=1e-12)
    assert o.biom_mort_induced.iloc[K] == pytest.approx(m * b_antes, rel=1e-12)
    assert (o.stems_n.iloc[K:] <= ctrl.stems_n.iloc[K:] + 1e-9).all()
    for c in ["biom_foliage", "biom_root", "biom_stem", "stems_n"]:
        assert (o[c] >= 0).all()


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        rodar(efficiency_events={ym(K): 1.0})
    with pytest.raises(ValueError):
        rodar(mortality_events={ym(K): -0.1})
    with pytest.raises(ValueError):
        rodar(mortality_events={"1900-01": 0.1})
