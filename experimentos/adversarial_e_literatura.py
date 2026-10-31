#!/usr/bin/env python3
"""Auditoria adversarial (tentativas de refutar as hipóteses) e confronto com dados secundários."""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
S = AQUI / "saida"
import clima  # noqa: E402
from clones import params, MATERIAIS  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

clima.SITIOS["CV"] = dict(nome="Campo Verde-MT", arquivo="POWER_daily_campo_verde_20060101_20081231.csv",
                          lat=-15.5456, lon=-55.1664, papel="literatura")
CL = {s: clima.clima_mensal(s) for s in ["IND", "TB", "IMP", "CV"]}
LAT = {s: clima.SITIOS[s]["lat"] for s in CL}


def sim(sitio="IND", mat="A1", asw=190.6, asw0=None, fr=None, ev=None, frm="2016-01", to="2023-01", planted="2015-01",
        P=None):
    M = MATERIAIS[mat]
    frm = frm if mat == "A1" or frm != "2016-01" else "2015-04"
    site = dict(latitude=LAT[sitio], altitude=0, soil_class=-1, asw_i=asw if asw0 is None else asw0, asw_min=0,
                asw_max=asw, **{"from": frm, "to": to})
    sp = dict(planted=planted, fertility=M["FR_ref"] if fr is None else fr, stems_n=10000 / 9,
              biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    return run_3pg_pjs(site, sp, CL[sitio], P or params(mat), defoliation_events=ev)


def perda(c, t, v="volume", data="2022-01-31"):
    a = t.set_index(t.date.astype(str))[v][data]; b = c.set_index(c.date.astype(str))[v][data]
    return 100 * (1 - a / b)


ADV = []

def reg(teste, hipotese, resultado, veredito, **kw):
    ADV.append(dict(teste=teste, hipotese_testada=hipotese, resultado=resultado, veredito=veredito, **kw))


# A1 — ASWmax × ASW0
c = sim(); t = sim(ev={"2017-01": .5}); base = perda(c, t)
c2 = sim(asw0=95.3); t2 = sim(asw0=95.3, ev={"2017-01": .5})
reg("ASWmax × ASW0", "A perda depende da condição hídrica inicial (ASW0), não só de ASWmax",
    f"perda vol. 84 m: ASW0=ASWmax {base:.2f} %; ASW0=50 % de ASWmax {perda(c2, t2):.2f} %; "
    f"volume ctrl {c.volume.iloc[72]:.1f} vs {c2.volume.iloc[72]:.1f} m³/ha",
    "ASW0 quase não importa: início em janeiro (chuvoso) reabastece o perfil no 1º mês")

# A2 — época do pulso / clima no momento do evento
res = {}
for e in ["2017-01", "2017-04", "2017-07", "2017-10", "2018-01"]:
    res[e] = perda(c, sim(ev={e: .5}))
reg("Época do pulso", "A perda depende do mês do evento (estação chuvosa × seca)",
    "; ".join(f"{k}: {v:.2f} %" for k, v in res.items()),
    "Sim — a época muda a perda; o mês 12 (janeiro) é uma escolha, não um caso geral", detalhe=json.dumps(res))

# A3 — saturação dos modificadores (caso principal)
fsw = c.f_sw.iloc[1:]; fv = c.f_vpd.iloc[1:]; ft = c.f_tmp.iloc[1:]
reg("Saturação dos modificadores", "Com ASWmax = 190,6 mm a água limita pouco e os níveis W não discriminam",
    f"IND A1 W100: meses com fSW>0,95 = {int((fsw>.95).sum())}/84; fSW<0,5 = {int((fsw<.5).sum())}; "
    f"fVPD médio {fv.mean():.2f}; fT médio {ft.mean():.2f}",
    "Água limita sazonalmente (seca de maio–set.), não saturada")

# A4 — dupla penalização FR (Borges: fNutr e partição) × A1 (só partição)
for mat in ["A1", "C5"]:
    cc = sim(mat=mat, fr=0.5483); tt = sim(mat=mat, fr=0.5483, ev={"2017-01": .5})
    c1 = sim(mat=mat); t1 = sim(mat=mat, ev={"2017-01": .5})
    reg(f"Canal do FR ({mat})", "FR atua em GPP (fNutr) e em partição (m) — possível dupla penalização",
        f"volume ctrl FRref {c1.volume.iloc[72]:.1f} vs FRmin {cc.volume.iloc[72]:.1f} m³/ha; "
        f"perda d50 FRref {perda(c1, t1):.2f} % vs FRmin {perda(cc, tt):.2f} %",
        "A1: FR só altera partição (fN0=1) -> efeito pequeno; C*: fNutr=0,5+0,5·FR e partição -> efeito maior. "
        "Não é dupla contagem do mesmo processo, mas 'fertilidade' não tem o mesmo significado nas duas fontes")

# A5 — aplicação temporal do pulso: início vs fim do mês (convenção da planilha)
reg("Início × fim do mês", "Aplicar no fim do mês (após crescimento) muda a perda",
    f"início de jan/2017: {perda(c, sim(ev={'2017-01': .5})):.2f} %; equivalente a fim de jan = início de fev/2017: "
    f"{perda(c, sim(ev={'2017-02': .5})):.2f} %", "Diferença pequena; convenção única mantida (início do mês)")

# A6 — balanço da biomassa removida (todos os tratamentos da matriz)
D = pd.read_csv(S / "mensal.csv.gz", usecols=["id", "biom_foliage", "biom_defol", "wf_pre_defol", "biom_incr_foliage",
                                               "biom_loss_foliage", "defol_frac", "lai", "sla", "stems_n", "volume", "f_tmp", "gpp"])
ev = D[D.biom_defol > 0]
err_rem = np.abs(ev.biom_defol - ev.defol_frac * ev.wf_pre_defol).max()
D["prev"] = D.groupby("id").biom_foliage.shift(1)
fech = (D.prev - D.biom_defol + D.biom_incr_foliage - D.biom_loss_foliage - D.biom_foliage).abs()
reg("Balanço da biomassa removida", "A remoção pode não fechar o balanço",
    f"{len(ev)} eventos; máx |removida − d·Wf_pré| = {err_rem:.1e}; máx resíduo do fechamento mensal de Wf = {fech.max():.1e} t/ha",
    "Fecha (precisão de máquina)")

# A7 — LAI improvável
lai = D.groupby(D.id.str.split("_").str[:2].str.join("_")).lai.max()
reg("LAI improvável", "Algum material/sítio produz LAI fora do esperado para eucalipto (~2–6)",
    "; ".join(f"{k}: {v:.2f}" for k, v in lai.items()),
    "Ver valores: LAI máximos de Borges mais altos (SLA0 12,7–15,2); A1 baixo (SLA 8,4–9,4)")

# A8 — recuperação artificialmente rápida? comparar com literatura
R = pd.read_csv(S / "indicadores_por_tratamento.csv")
r50 = R[(R.experimento == "E1-E6") & (R.desfolha == .5) & (R.calendario == "P1") & R.apto_analise_principal]
reg("Recuperação rápida demais?", "O módulo recupera mais rápido que eucaliptos reais",
    f"d=50 %: recuperação relativa (95 % do controle) mediana {r50.recup_rel95_meses_ev1.median():.0f} meses "
    f"(faixa {r50.recup_rel95_meses_ev1.min():.0f}–{r50.recup_rel95_meses_ev1.max():.0f}); Barry et al. 2012: "
    "altura, diâmetro e área foliar sem diferença do controle aos 18 meses (≈40–55 % da copa superior, E. globulus)",
    "Refutado no sentido oposto: o módulo tende a recuperar MAIS DEVAGAR que o observado em E. globulus jovem "
    "(sem reservas, sem aumento de fotossíntese, sem realocação para folhas)")

# A9 — compensação via água (NPP do tratamento > controle)
reg("Compensação hídrica", "O ganho de NPP após a desfolha é artefato",
    f"meses com NPP_trat > NPP_ctrl (d=50 %): mediana {r50.meses_NPP_trat_maior_ctrl.median():.0f}; "
    f"ASW média pós-evento {r50.reducao_ASW_media_pct.median():.1f} % (negativo = mais água)",
    "Mecanismo do modelo: menos LAI -> menos transpiração -> mais água -> fSW maior. Quentin et al. 2011 observaram "
    "AUMENTO da transpiração por área foliar remanescente (não representado) -> a economia de água provavelmente é superestimada")

# A10 — mortalidade
stem_ini = D.groupby("id").stems_n.first(); stem_fim = D.groupby("id").stems_n.last()
reg("Ausência de mortalidade", "A desfolha não mata árvores no modelo",
    f"tratamentos com autodesbaste até 2023-01: {(stem_fim < stem_ini - 1e-6).sum()} de {len(stem_ini)}; "
    f"desfolha nunca reduz N abaixo do controle (teste automatizado)",
    "Correto por construção; resultados de 95 % NÃO informam risco de morte")

# A11 — extrapolação térmica IMP × A1
ci = sim(sitio="IMP"); m0 = int((ci.f_tmp.iloc[1:] == 0).sum())
reg("Extrapolação térmica", "Em Imperatriz o A1 para de crescer por fT = 0",
    f"meses com fT=0 em 84: {m0}; volume ctrl aos 84 m: IMP {ci.volume.iloc[72]:.1f} vs IND {c.volume.iloc[72]:.1f} m³/ha",
    "Confirmado — combinação marcada como diagnóstico, fora da análise principal")

# A12 — 100 % de desfolha e d próximo de 1
v = {}
for d in [0.95, 0.99, 0.999]:
    v[d] = perda(c, sim(ev={"2017-01": d}))
reg("Desfolha total", "O módulo não representa refolhamento após 100 %",
    "; ".join(f"d={k}: perda vol. {val:.1f} %" for k, val in v.items()) + "; d=1 é bloqueado (LAI=0 => GPP=0 para sempre)",
    "Limitação estrutural: sem reservas, Wf=0 é absorvente. Experimentos com 100 % (Bertulio, Matrangolo) não são simuláveis exatamente")

# A13 — recorrente < único (casos)
p = R[R.experimento == "E1-E6"].pivot_table(index=["sitio", "material", "nivel_agua", "nivel_FR", "desfolha"],
                                            columns="calendario", values="perda_volume_k72")
neg = p[p.P2 < p.P1]
reg("Recorrente < único", "Dois pulsos sempre perdem mais",
    f"{len(neg)} de {len(p)} combinações com perda de volume aos 84 m menor em P2; exemplos: " +
    "; ".join(f"{'/'.join(map(str, i))}: P1 {r.P1:.2f} P2 {r.P2:.2f}" for i, r in neg.head(4).iterrows()),
    "Contrário à hipótese: ver relatório (efeito via água/fT após o 2º pulso)" if len(neg) else "Hipótese mantida")

# A14 — incerteza de transferência
vol = {m: sim(mat=m).volume.iloc[72] for m in ["A1", "C5", "C2", "C4", "C1", "C3"]}
reg("Transferência de parâmetros", "Clones diferentes dão produtividades muito distintas no mesmo sítio",
    "volume ctrl IND 84 m: " + "; ".join(f"{k} {val:.0f}" for k, val in vol.items()) + " m³/ha",
    "Grande dispersão entre parametrizações: a incerteza de transferência supera o efeito do solo")

pd.DataFrame(ADV).to_csv(S / "auditoria_adversarial.csv", index=False)

# =================== LITERATURA: protocolo de Bertulio et al. (2008) ===================
# idade 14 meses em 2007-04 => plantio 2006-02; desfolhas 2007-04 e 2008-01; avaliação aos 26 meses (2008-04)
# e no fim das coletas (2008-03). 100 % não é simulável: usa-se 95 % e 99,9 %. Solo: referência (desconhecido).
obs = pd.read_csv(AQUI.parent / "revisao" / "dados_tratamentos_observados_verificado.csv")
ob = obs[(obs.study_id == "Bertulio_2008") & (obs.idade_meses == 26)]
LIT = []
for mat, alvo in [("C5", "E. urophylla × E. grandis (urograndis)"), ("A1", "E. urophylla × E. camaldulensis (urocam)")]:
    frm = "2007-02" if mat == "A1" else "2006-05"
    for d in [0.95, 0.999]:
        cc = sim(sitio="CV", mat=mat, frm=frm, to="2008-06", planted="2006-02")
        tt = sim(sitio="CV", mat=mat, frm=frm, to="2008-06", planted="2006-02", ev={"2007-04": d, "2008-01": d})
        for data in ["2008-03-31", "2008-04-30"]:
            for var_sim, var_obs in [("volume", "volume"), ("dbh", "CAP"), ("height", "altura")]:
                if var_sim == "height" and mat == "A1":
                    continue
                o = ob[(ob.especie_ou_clone == alvo) & (ob.variavel == var_obs)].iloc[0]
                Ls = perda(cc, tt, var_sim, data)
                for tipo, Lo in [("bruta", o.L_obs_pct_calculado), ("ajustada_linha_base", o.L_obs_pct_ajustado_linha_base)]:
                    LIT.append(dict(estudo="Bertulio_2008", material_sim=mat, alvo_obs=alvo, desfolha_sim=d,
                                    data_aval=data, variavel=var_obs, L_obs=Lo, tipo_L_obs=tipo, L_sim=round(Ls, 2),
                                    erro_pp=round(Ls - Lo, 2), acerto_heuristico=round(max(0, 100 - abs(Ls - Lo)), 1),
                                    comparabilidade=("híbrido relacionado; clima do município; solo e clone desconhecidos; "
                                                     "100 % aproximado por d<1; DAP vs CAP (razão equivalente)"
                                                     + ("; A1 é E. urophylla puro, alvo é urocam -> transferência fraca" if mat == "A1" else ""))))
L = pd.DataFrame(LIT); L.to_csv(S / "confronto_literatura_bertulio.csv", index=False)
sel = L[(L.data_aval == "2008-04-30") & (L.tipo_L_obs == "ajustada_linha_base")]
met = sel.groupby(["material_sim", "desfolha_sim"]).agg(n=("erro_pp", "size"), vies_pp=("erro_pp", "mean"),
                                                         MAE_pp=("erro_pp", lambda x: np.abs(x).mean()),
                                                         RMSE_pp=("erro_pp", lambda x: np.sqrt((x ** 2).mean()))).round(2)
met.to_csv(S / "confronto_literatura_metricas.csv")
print(pd.DataFrame(ADV)[["teste", "resultado"]].to_string(max_colwidth=160))
print(sel[["material_sim", "desfolha_sim", "variavel", "L_obs", "L_sim", "erro_pp"]].to_string())
print(met.to_string())
