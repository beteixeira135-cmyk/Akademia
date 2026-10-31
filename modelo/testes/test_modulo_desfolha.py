"""
Testes automatizados — tradução 3-PGpjs + módulo de desfolha.

ATENÇÃO: os testes usam o caso de exemplo do próprio r3PG (Pinus sylvestris / Fagus
sylvatica, Alemanha, 2001–2010). Eles verificam o CÓDIGO; não são simulações de
Eucalyptus urophylla nem resultados do TCC.

Executar:  cd modelo && python3 -m pytest -q testes/
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
NOME = "Pinus sylvestris"           # caso perenifólio (como o eucalipto)
SPEC = SP.loc[NOME].to_dict()
PARS = params_from_table(PAR, NOME)
ESTOQUES = ["biom_foliage", "biom_root", "biom_stem", "stems_n", "lai", "asw"]


def rodar(eventos=None, **kw):
    return run_3pg_pjs(SITE, SPEC, CLIM, PARS, defoliation_events=eventos, **kw)


@pytest.fixture(scope="module")
def controle():
    return rodar()


# ---------- 1. Reprodução do r3PG original (tests/testthat/test-vba.R) ----------
@pytest.mark.parametrize("nome,ref", [("Pinus sylvestris", (125.423, 39.146, 3.845)),
                                      ("Fagus sylvatica", (129.988, 31.350, 0.000))])
def test_reproduz_valores_de_referencia_r3pg(nome, ref):
    out = run_3pg_pjs(SITE, SP.loc[nome].to_dict(), CLIM, params_from_table(PAR, nome))
    obtido = np.round(out.iloc[119][["biom_stem", "biom_root", "biom_foliage"]].to_numpy(float), 3)
    assert np.array_equal(obtido, np.array(ref))


# ---------- 2. Desfolha 0% idêntica ao controle ----------
def test_desfolha_zero_identica_ao_controle(controle):
    zero = rodar(pulsos(SITE["from"], [12, 48], 0.0))
    cols = [c for c in controle.columns if c not in ("wf_pre_defol",)]
    pd.testing.assert_frame_equal(controle[cols], zero[cols], check_exact=True)
    assert (zero.biom_defol == 0).all()


# ---------- 3–4. Redução instantânea de Wf e atualização do LAI ----------
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
def test_reducao_instantanea_e_lai(controle, d):
    k = 12
    out = rodar(pulsos(SITE["from"], [k], d))
    wf_pre = controle.biom_foliage.iloc[k - 1]           # Wf no fim do mês anterior
    assert out.wf_pre_defol.iloc[k] == pytest.approx(wf_pre, rel=0, abs=0)
    assert out.biom_defol.iloc[k] == pytest.approx(d * wf_pre, rel=1e-14)
    # APAR do mês do evento deve usar o LAI pós-desfolha: LAI = Wf*(1-d)*SLA*0.1
    lai_pos = wf_pre * (1 - d) * out.sla.iloc[k] * 0.1
    cc = out.canopy_cover.iloc[k]
    mes = pd.Timestamp(out.date.iloc[k]).month
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1]
    srad = CLIM.set_index(["year", "month"]).loc[(pd.Timestamp(out.date.iloc[k]).year, mes), "srad"]
    apar_esp = srad * dias * (1 - np.exp(-PARS["k"] * lai_pos / cc)) * cc
    assert out.apar.iloc[k] == pytest.approx(apar_esp, rel=1e-12)
    assert out.apar.iloc[k] < controle.apar.iloc[k]


# ---------- 5. Não negatividade ----------
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
@pytest.mark.parametrize("idx", [[12], [12, 48]])
def test_nao_negatividade(d, idx):
    out = rodar(pulsos(SITE["from"], idx, d))
    assert (out[ESTOQUES + ["biom_defol", "gpp", "npp_f"]] >= 0).all().all()
    assert np.isfinite(out[ESTOQUES].to_numpy()).all()


# ---------- 6. Conservação da biomassa foliar removida ----------
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
def test_conservacao_massa_foliar(d):
    assert PARS["mF"] == 0  # no caso de teste a mortalidade não retira folhas
    out = rodar(pulsos(SITE["from"], [12, 48], d))
    wf = out.biom_foliage.to_numpy()
    fecho = wf[:-1] - out.biom_defol.to_numpy()[1:] + out.biom_incr_foliage.to_numpy()[1:] \
        - out.biom_loss_foliage.to_numpy()[1:] - wf[1:]
    assert np.abs(fecho).max() < 1e-12
    eventos = out[out.biom_defol > 0]
    assert np.allclose(eventos.biom_defol, d * eventos.wf_pre_defol, rtol=1e-14)


# ---------- 7–8. Calendário e ausência de duplicação ----------
def test_calendario_dos_pulsos(controle):
    ev = pulsos(SITE["from"], [12, 48], 0.5)
    assert list(ev) == ["2002-01", "2005-01"]           # from = 2001-01
    out = rodar(ev)
    idx = np.flatnonzero(out.biom_defol.to_numpy() > 0)
    assert idx.tolist() == [12, 48]
    # antes do 1º evento, tudo idêntico ao controle
    pd.testing.assert_frame_equal(controle.iloc[:12][ESTOQUES], out.iloc[:12][ESTOQUES], check_exact=True)


def test_sem_duplicacao_e_validacao():
    with pytest.raises(ValueError):
        pulsos(SITE["from"], [12, 12], 0.5)
    with pytest.raises(ValueError):
        rodar({"2001-01": 0.5})                           # mês do estado inicial
    with pytest.raises(ValueError):
        rodar({"1999-01": 0.5})                           # fora da simulação
    for d in (-0.1, 1.0, 1.5):
        with pytest.raises(ValueError):
            rodar({"2002-01": d})


# ---------- 9. Consistência de unidades (LAI = Wf[t/ha] * SLA[m2/kg] * 0.1) ----------
def test_unidades_lai(controle):
    out = rodar(pulsos(SITE["from"], [12, 48], 0.5))
    for df in (controle, out):
        assert np.allclose(df.lai, df.biom_foliage * df.sla * 0.1, rtol=1e-14, atol=0)


# ---------- 10. Reprodutibilidade ----------
def test_reprodutibilidade():
    ev = pulsos(SITE["from"], [12, 48], 0.95)
    pd.testing.assert_frame_equal(rodar(ev), rodar(ev), check_exact=True)


# ---------- 11. Recuperação calculada pelo modelo (sem taxa imposta) ----------
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
def test_recuperacao_emerge_das_equacoes(controle, d):
    k = 12
    out = rodar(pulsos(SITE["from"], [k], d))
    pos = out.wf_pre_defol.iloc[k] * (1 - d)
    assert out.biom_foliage.iloc[k + 12] > pos                     # folhagem volta a crescer
    assert (out.biom_foliage.iloc[k:] <= controle.biom_foliage.iloc[k:] + 1e-12).all()
    assert out.biom_stem.iloc[-1] < controle.biom_stem.iloc[-1]   # perda de crescimento acumulada


# ---------- 12. Mortalidade induzida desativada ----------
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
def test_sem_mortalidade_induzida(controle, d):
    out = rodar(pulsos(SITE["from"], [12, 48], d))
    # a desfolha não pode aumentar a mortalidade: o nº de árvores nunca fica abaixo do controle
    assert (out.stems_n.to_numpy() >= controle.stems_n.to_numpy() - 1e-9).all()


# ---------- 12b. Mortalidade induzida desativada, com autodesbaste ATIVO ----------
# No caso padrão o autodesbaste nunca dispara (stems_n = 800 constante), o que tornaria o
# teste 12 incapaz de detectar mortalidade induzida. Aqui wSx1000 é reduzido APENAS PARA
# O TESTE, de modo que a regra -3/2 atue durante toda a simulação.
@pytest.mark.parametrize("d", [0.25, 0.50, 0.95])
def test_sem_mortalidade_induzida_com_autodesbaste(d):
    p = dict(PARS, wSx1000=100.0)
    ctrl = run_3pg_pjs(SITE, SPEC, CLIM, p)
    assert ctrl.stems_n.iloc[-1] < ctrl.stems_n.iloc[0]          # autodesbaste realmente ativo
    out = run_3pg_pjs(SITE, SPEC, CLIM, p, defoliation_events=pulsos(SITE["from"], [12, 48], d))
    assert (out.stems_n.to_numpy() >= ctrl.stems_n.to_numpy() - 1e-9).all()
    assert (out.mort_thinn.to_numpy() <= ctrl.mort_thinn.to_numpy() + 1e-9).all()
