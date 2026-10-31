"""Testes automatizados do pipeline experimental (rodar após run_experimentos.py, indicadores.py e o
script R r_check/rodar_controles_r3pg.R).   cd experimentos && python3 -m pytest -q testes/"""
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

S = Path(__file__).resolve().parents[1] / "saida"
RC = Path(__file__).resolve().parents[1] / "r_check"


@pytest.fixture(scope="module")
def M():
    return pd.read_csv(S / "matriz_tratamentos.csv")


@pytest.fixture(scope="module")
def D():
    return pd.read_csv(S / "mensal.csv.gz", usecols=["id", "date", "mes_ref", "biom_foliage", "biom_stem", "biom_root",
                                                     "lai", "sla", "biom_defol", "wf_pre_defol", "defol_frac",
                                                     "biom_incr_foliage", "biom_loss_foliage", "stems_n", "volume", "asw"])


def test_ids_unicos_e_completos(M, D):
    assert M.id.is_unique
    assert set(D.id.unique()) == set(M.id)
    assert (D.groupby("id").size().groupby(M.set_index("id").material).nunique() == 1).all()


def test_controles_identicos_ao_r3pg_original():
    r = pd.read_csv(RC / "resultado_crosscheck.csv")
    assert (r.pares == r.pares.iloc[0]).all() and r.pares.iloc[0] > 20000
    assert r.max_dif_rel.max() < 1e-10


def test_eventos_somente_nos_meses_previstos(M, D):
    ev = D[D.biom_defol > 0].merge(M[["id", "eventos"]], on="id")
    assert all(str(d)[:7] in e.split(";") for d, e in zip(ev.date, ev.eventos))
    n_esp = M[M.desfolha > 0].eventos.str.count(";").add(1).sum()
    assert len(ev) == n_esp                        # cada evento aplicado exatamente uma vez


def test_igual_ao_controle_antes_do_primeiro_evento(M, D):
    M = M.assign(g=M.sitio + M.material + M.nivel_agua.astype(str) + M.nivel_FR + M.experimento)
    ctrl = M[M.desfolha == 0].set_index("g").id
    G = dict(tuple(D.groupby("id")))
    for r in M[M.desfolha > 0].sample(200, random_state=1).itertuples():
        t, c = G[r.id], G[ctrl[r.g]]
        pre = t.date < r.eventos.split(";")[0]
        assert np.array_equal(t.loc[pre, "volume"].to_numpy(), c.loc[c.date < r.eventos.split(";")[0], "volume"].to_numpy())


def test_remocao_e_fechamento_de_massa(D):
    ev = D[D.biom_defol > 0]
    assert np.allclose(ev.biom_defol, ev.defol_frac * ev.wf_pre_defol, rtol=1e-13, atol=0)
    prev = D.groupby("id").biom_foliage.shift(1)
    res = (prev - D.biom_defol + D.biom_incr_foliage - D.biom_loss_foliage - D.biom_foliage).abs()
    assert res.max() < 1e-10                        # mF = 0 em todos os materiais


def test_nao_negatividade_e_lai(D):
    assert (D[["biom_foliage", "biom_stem", "biom_root", "lai", "volume", "asw", "stems_n"]] >= 0).all().all()
    assert np.allclose(D.lai, D.biom_foliage * D.sla * 0.1, rtol=1e-12)


def test_sem_mortalidade_induzida(M, D):
    M = M.assign(g=M.sitio + M.material + M.nivel_agua.astype(str) + M.nivel_FR + M.experimento)
    ctrl = M[M.desfolha == 0].set_index("g").id
    fim = D.groupby("id").stems_n.last()
    t = M[M.desfolha > 0]
    assert (fim[t.id].to_numpy() >= fim[ctrl[t.g]].to_numpy() - 1e-9).all()


def test_imperatriz_A1_marcado_como_diagnostico(M):
    assert not M[(M.sitio == "IMP") & (M.material == "A1")].apto_analise_principal.any()
    assert M[~((M.sitio == "IMP") & (M.material == "A1"))].apto_analise_principal.all()
