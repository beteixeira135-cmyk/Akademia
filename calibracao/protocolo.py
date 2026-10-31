"""Protocolo de Bertulio et al. (2008) no 3-PG: plantio 2006-02, desfolhas 2007-04 e 2008-01, avaliação 2008-04-30
(26 meses). Mesmo código do confronto do TCC (experimentos/adversarial_e_literatura.py), agora com compensação v3."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
import clima
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
clima.SITIOS["CV"] = dict(nome="Campo Verde-MT", arquivo="POWER_daily_campo_verde_20060101_20081231.csv",
                          lat=-15.5456, lon=-55.1664, papel="literatura")
CV = clima.clima_mensal("CV")
OBS = pd.read_csv(R / "revisao" / "dados_tratamentos_observados_verificado.csv")
OBS = OBS[(OBS.study_id == "Bertulio_2008") & (OBS.idade_meses == 26)]
ALVO = {"C5": "E. urophylla × E. grandis (urograndis)", "A1": "E. urophylla × E. camaldulensis (urocam)"}
VAR = [("volume", "volume"), ("dbh", "CAP"), ("height", "altura")]
def sim(mat, ev=None, comp=None):
    M = MATERIAIS[mat]; frm = "2007-02" if mat == "A1" else "2006-05"
    site = dict(latitude=-15.5456, altitude=0, soil_class=-1, asw_i=190.6, asw_min=0, asw_max=190.6, **{"from": frm, "to": "2008-06"})
    sp = dict(planted="2006-02", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    return run_3pg_pjs(site, sp, CV, params(mat), defoliation_events=ev, compensation=comp)
_CTRL = {}
def perdas(mat, comp=None, d=0.999, data="2008-04-30"):
    if mat not in _CTRL: _CTRL[mat] = sim(mat)
    c = _CTRL[mat]; t = sim(mat, {"2007-04": d, "2008-01": d}, comp)
    cc = c.set_index(c.date.astype(str)); tt = t.set_index(t.date.astype(str))
    return {vo: 100 * (1 - tt[vs][data] / cc[vs][data]) for vs, vo in VAR}
def observado(mat):
    o = OBS[OBS.especie_ou_clone == ALVO[mat]]
    return {r.variavel: r.L_obs_pct_ajustado_linha_base for r in o.itertuples()}
if __name__ == "__main__":
    for mat in ["C5", "A1"]:
        print(mat, "obs", {k: round(v, 1) for k, v in observado(mat).items()})
        for comp in [None, {"U": 1.35}, {"gam": 1}, {"a": 1}, {"U": 1.35, "gam": 1, "a": 1}]:
            print("  ", comp, {k: round(v, 1) for k, v in perdas(mat, comp).items()})
