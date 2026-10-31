"""
Testes da EXTENSÃO v3 (compensação após a desfolha), no caso de referência do r3PG (Pinus sylvestris).
Verificam o código (ativação, desativação, sinal e limites dos efeitos), não a biologia do eucalipto.
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
EV = pulsos(SITE["from"], [K], 0.5)


@pytest.fixture(scope="module")
def v2():
    return rodar(defoliation_events=EV)


def test_sem_compensacao_identico_a_v2(v2):
    """compensation=None e compensação neutra (U=1, γ=0, a=0) reproduzem a v2 exatamente."""
    for comp in (None, {"U": 1.0, "gam": 0.0, "a": 0.0}):
        z = rodar(defoliation_events=EV, compensation=comp)
        cols = [c for c in v2.columns if not c.startswith("comp_")]
        pd.testing.assert_frame_equal(v2[cols], z[cols], check_exact=True)


def test_sem_desfolha_compensacao_nunca_ativa():
    c = rodar(compensation={"U": 1.3, "gam": 1.0, "a": 1.0})
    assert c.comp_ativa.sum() == 0
    pd.testing.assert_frame_equal(rodar().drop(columns=[x for x in c.columns if x.startswith("comp_")]),
                                  c.drop(columns=[x for x in c.columns if x.startswith("comp_")]), check_exact=True)


def test_ativa_no_evento_e_desliga_ao_recuperar():
    t = rodar(defoliation_events=EV, compensation={"U": 1.2, "a": 0.5})
    on = t.comp_ativa.to_numpy()
    assert on[K] == 1.0 and on[:K].sum() == 0          # liga no mês do evento, nunca antes
    fim = np.where(on[K:] == 0)[0]
    assert len(fim) > 0                                 # desliga em algum momento
    k_off = K + fim[0]
    wf_pre = t.wf_pre_defol[K]
    assert t.biom_foliage[k_off - 1] >= wf_pre * 0.999 or t.biom_foliage[k_off] >= wf_pre * 0.999


def test_U_aumenta_alpha_so_durante_deficit(v2):
    t = rodar(defoliation_events=EV, compensation={"U": 1.3})
    assert np.isclose(t.alpha_c[K] / v2.alpha_c[K], 1 + 0.3 * t.f_sw[K])
    assert (t.alpha_c[:K] == v2.alpha_c[:K]).all()


def test_a_desvia_particao_para_folhas_e_acelera_recuperacao(v2):
    t = rodar(defoliation_events=EV, compensation={"a": 1.0})
    assert t.biom_foliage[K + 1] > v2.biom_foliage[K + 1]
    assert t.biom_incr_stem[K] < v2.biom_incr_stem[K]


def test_gamma_aumenta_transpiracao_com_teto(v2):
    t = rodar(defoliation_events=EV, compensation={"gam": 1.0})
    assert t.transp_veg[K] >= v2.transp_veg[K]
    assert t.comp_gc.max() <= 1 / (1 - 0.45) + 1e-12


@pytest.mark.parametrize("comp", [{"U": 0.9}, {"U": 2.5}, {"gam": -0.1}, {"gam": 1.1}, {"a": -0.1}, {"a": 1.5}])
def test_parametros_fora_do_dominio(comp):
    with pytest.raises(ValueError):
        rodar(defoliation_events=EV, compensation=comp)


def test_compensacao_reduz_perda_de_lenho(v2):
    ctrl = rodar(); t = rodar(defoliation_events=EV, compensation={"U": 1.16, "a": 0.55, "gam": 0.5})
    perda_v2 = 1 - v2.biom_stem.iloc[-1] / ctrl.biom_stem.iloc[-1]
    perda_v3 = 1 - t.biom_stem.iloc[-1] / ctrl.biom_stem.iloc[-1]
    assert 0 <= perda_v3 < perda_v2
