"""Auditoria: cada número citado no TCC é recalculado a partir das saídas e comparado ao texto (arredondado como no texto)."""
import json, sys, re
from pathlib import Path
import numpy as np, pandas as pd
X = Path("/home/claude/tcc/experimentos"); S = X / "saida"; sys.path.insert(0, str(X))
R = pd.read_csv(S / "indicadores_por_tratamento.csv")
L = R[(R.experimento == "LOCAL") & (R.nivel_FR == "F100")]
E = R[R.experimento == "E1-E6"].copy(); E["W"] = pd.to_numeric(E.nivel_agua)
C = pd.read_csv(S / "controles_solo_local.csv").set_index(["sitio", "mat"])
K = pd.read_csv(S / "estatisticas/D_kfold_resumo.csv"); G = pd.read_csv(S / "estatisticas/D_kfold_por_grupo.csv")
IMP = pd.read_csv(S / "estatisticas/C_importancia_variaveis.csv"); TC = pd.read_csv(S / "estatisticas/C_metamodelo_validacao_cruzada.csv")
A = pd.read_csv(S / "estatisticas/A_verificacao.csv"); MOR = pd.read_csv(S / "sensibilidade_morris_A1_3sitios.csv")
Q1 = pd.read_csv(S / "Q1_Q4_agua_vs_fertilidade.csv"); DEC = pd.read_csv(S / "sensibilidade_decomposicao_fatorial.csv")
Q3 = pd.read_csv(S / "Q3_FR_exploratorio.csv", header=[0, 1], index_col=[0, 1])["perda_volume_k72"]
M = pd.read_csv(S / "matriz_tratamentos.csv")
v = lambda s, m, cal, d, col="perda_volume_k72": L[(L.sitio == s) & (L.material == m) & (L.calendario == cal) & (L.desfolha == d)][col].iloc[0]
ok = []; 
def chk(rot, texto, calc, dec=1):
    c = round(float(calc), dec); t = float(str(texto).replace(",", "."))
    ok.append(dict(item=rot, texto=texto, calculado=c, ok=abs(c - t) <= 10 ** -dec * 0.51 + 1e-9))
# matriz
chk("total de tratamentos", 2408, len(M), 0); chk("bloco solo", 1344, (M.experimento == "E1-E6").sum(), 0)
chk("bloco local", 912, (M.experimento == "LOCAL").sum(), 0); chk("controles", 308, (M.desfolha == 0).sum(), 0)
# verificação
chk("registros por variável r3PG", 28277, A.n.iloc[0], 0)
chk("RQEM máx r3PG < 2e-13 (x1e13)", 2.0, min(2.0, A[A.comparacao.str.contains("r3PG")].RQEM_pct.max() * 1e13), 1)
chk("R2 VBA mínimo >= 0,9996", 0.9996, max(0.9996, A[A.comparacao.str.contains("VBA")].R2.min()) if A[A.comparacao.str.contains("VBA")].R2.min() >= 0.9996 else 0, 4)
chk("RQEM VBA máx < 0,14", 0.13, A[A.comparacao.str.contains("VBA")].RQEM_pct.max(), 2)
# controles
for (s, m), vol, ima, lenho, lai, ft in [(("TB", "A1"), 429, 61, 37.1, 4.8, 0), (("TB", "C5"), 386, 55, 37.7, 4.7, 0), (("IND", "A1"), 352, 50, 25.9, 3.6, 0),
                                       (("IND", "C5"), 309, 44, 25.3, 3.5, 0), (("IMP", "A1"), 227, 32, 14.6, 2.1, 31), (("IMP", "C5"), 255, 36, 18.9, 2.7, 0)]:
    r = C.loc[(s, m)]
    chk(f"vol84 {s} {m}", vol, r.vol84, 0); chk(f"IMA {s} {m}", ima, r.IMA84, 0); chk(f"lenho {s} {m}", lenho, r.caule_24_36, 1)
    chk(f"IAF {s} {m}", lai, r.LAI_24_36, 1); chk(f"fT0 {s} {m}", ft, r.meses_fT0, 0)
chk("+9% lenho TB vs 34", 9, 100 * (C.loc[("TB", "A1")].caule_24_36 / 34 - 1), 0)
chk("+26% IAF TB vs 3,8", 26, 100 * (C.loc[("TB", "A1")].LAI_24_36 / 3.8 - 1), 0)
chk("ΔLenho IND→TB 11", 11, C.loc[("TB", "A1")].caule_24_36 - C.loc[("IND", "A1")].caule_24_36, 0)
chk("fSW IND 0,53", 0.53, C.loc[("IND", "A1")].fSW_med, 2); chk("fSW TB 0,73", 0.73, C.loc[("TB", "A1")].fSW_med, 2)
CO = pd.read_csv(S.parent / "saida_antes_dossel_u1/controles_solo_local.csv").set_index(["sitio", "mat"]); BG = [(s_, m_) for s_ in ["IND", "TB", "IMP"] for m_ in ["C2", "C4", "C5"]]
chk("IAF max Borges original mín 8", 8, CO.loc[BG].LAImax.min(), 0); chk("IAF max Borges original máx 11", 11, CO.loc[BG].LAImax.max(), 0)
chk("IAF 2-3 anos Borges corrigido mín 2,4", 2.4, C.loc[BG].LAI_24_36.min(), 1); chk("IAF 2-3 anos Borges corrigido máx 5,6", 5.6, C.loc[BG].LAI_24_36.max(), 1)
chk("IMA Borges corrigido mín 36", 36, C.loc[BG].IMA84.min(), 0); chk("IMA Borges corrigido máx 65", 65, C.loc[BG].IMA84.max(), 0)
chk("perda C5 IND P1 50% 2,7", 2.7, v("IND", "C5", "P1", .5), 1); chk("perda A1 IND P1 50% 3,0", 3.0, v("IND", "A1", "P1", .5), 1)
chk("queda APAR C5 IND 33", 33, 100 * (1 - v("IND", "C5", "P1", .5, "APAR_ev1_trat") / v("IND", "C5", "P1", .5, "APAR_ev1_ctrl")), 0)
# tabela 5 e textos
T5 = {"IND": {"A1": [[1.6, 3.0, 9.5], [2.1, 4.4, 17.3], [6.7, 13.8, 58.0], [15, 23, 24]], "C5": [[1.7, 2.7, 9.2], [2.1, 4.2, 17.5], [6.5, 13.8, 53.7], [15, 22, 24]]},
      "TB": {"A1": [[1.2, 3.3, 15.2], [0.5, 2.7, 25.6], [1.8, 6.8, 67.8], [14, 24, 26]], "C5": [[1.3, 3.1, 14.5], [0.9, 3.0, 28.1], [2.1, 8.0, 64.3], [14, 23, 26]]},
      "IMP": {"A1": [[2.8, 6.2, 31.7], [6.0, 14.6, 60.5], [16.4, 37.5, 84.1], [23, 28, 47]], "C5": [[1.2, 2.8, 9.6], [2.8, 6.5, 26.3], [7.7, 19.4, 64.5], [14, 17, 17]]}}
for s, dm in T5.items():
    for m, rows in dm.items():
        for cal, row in zip(["P1", "P2", "PA"], rows[:3]):
            for d, val in zip([0.25, 0.5, 0.95], row):
                chk(f"T5 {s} {m} {cal} {d}", val, v(s, m, cal, d), 1)
        for d, val in zip([0.25, 0.5, 0.95], rows[3]):
            chk(f"T5 recup {s} {m} {d}", val, v(s, m, "P1", d, "recup_rel95_meses_ev1"), 0)
for s, pre, pos in [("IND", 2.93, 1.46), ("TB", 4.42, 2.20)]:
    chk(f"IAF pré {s}", pre, v(s, "A1", "P1", 0.5, "LAI_pre_ev1"), 2); chk(f"IAF pós {s}", pos, v(s, "A1", "P1", 0.5, "LAI_pos_ev1"), 2)
for s, q in [("IND", 33), ("TB", 25)]:
    chk(f"queda APAR {s}", q, 100 * (1 - v(s, "A1", "P1", .5, "APAR_ev1_trat") / v(s, "A1", "P1", .5, "APAR_ev1_ctrl")), 0)
chk("recup abs IND 3", 3, v("IND", "A1", "P1", .5, "recup_abs_meses_ev1"), 0); chk("recup abs TB 13", 13, v("TB", "A1", "P1", .5, "recup_abs_meses_ev1"), 0)
chk("ASW +9,3% IND d95", 9.3, -v("IND", "A1", "P1", .95, "reducao_ASW_media_pct"), 1); chk("NPP comp 30 meses IND", 30, v("IND", "A1", "P1", .95, "meses_NPP_trat_maior_ctrl"), 0)
chk("ASW +3,5% TB d95", 3.5, -v("TB", "A1", "P1", .95, "reducao_ASW_media_pct"), 1)
for s, cal, val in [("IND", "EA", 1.7), ("IND", "EO", 3.7), ("TB", "EJ", 1.9)]:
    chk(f"época A1 {s} {cal}", val, v(s, "A1", cal, .5), 1)
Ep = L[(L.desfolha == .5) & L.calendario.isin(["P1", "EA", "EJ", "EO"]) & (L.material != "A1")]
chk("época Borges amplitude <", 3.5, max(0.5, Ep.groupby(["sitio", "material"]).perda_volume_k72.agg(lambda x: x.max() - x.min()).max()), 1)
# Q6
p = E.pivot_table(index=["sitio", "material", "W", "nivel_FR", "desfolha"], columns="calendario", values=["perda_volume_k72", "perda_NPP_acum_pct"])
chk("pares 576", 576, len(p), 0); chk("95% NPP P2>P1", 93, 100 * (p[("perda_NPP_acum_pct", "P2")] > p[("perda_NPP_acum_pct", "P1")]).mean(), 0)
chk("razão mediana", 1.9, (p[("perda_volume_k72", "P2")] / p[("perda_volume_k72", "P1")]).median(), 1)
mm = p[p[("perda_volume_k72", "P2")] < p[("perda_volume_k72", "P1")]].reset_index()
chk("28 pares P2<P1", 46, len(mm), 0); chk("25 do A1", 25, (mm.material == "A1").sum(), 0); chk("20 com 25%", 20, ((mm.material == "A1") & (mm.desfolha == .25)).sum(), 0)
# solo
chk("amplitude mín 0,4", 0.4, Q1.amplitude_perda_pp.min(), 1); chk("amplitude máx", 4.1, Q1.amplitude_perda_pp.max(), 1)
q = Q1.set_index(["sitio", "material"])
chk("A1 água IND 70", 70, q.loc[("IND", "A1")].pct_SQ_agua, 0); chk("A1 água TB ~100", 100, q.loc[("TB", "A1")].pct_SQ_agua, 0)
b = q.loc[[("IND", m) for m in ["C2", "C4", "C5"]] + [("IMP", m) for m in ["C2", "C4", "C5"]]].pct_SQ_FR
chk("FR Borges mín", 22, b.min(), 0); chk("FR Borges máx", 62, b.max(), 0)
tb = q.loc[[("TB", m) for m in ["C2", "C4", "C5"]]][["pct_SQ_agua", "pct_SQ_FR"]]
chk("TB Borges mín", 1, tb.min().min(), 0); chk("TB Borges máx", 91, tb.max().max(), 0)
d = DEC[DEC.resposta == "perda_volume_k72"].set_index("sitio").material
chk("material IND", 27, d["IND"], 0); chk("material TB", 20, d["TB"], 0); chk("material IMP", 22, d["IMP"], 0)
for s, a_, b_ in [("IND", 3.0, 5.1), ("TB", 2.8, 5.6), ("IMP", 3.3, 5.3)]:
    chk(f"FR C5 {s} 1,0", a_, Q3.loc[(s, "C5"), "1.0"], 1); chk(f"FR C5 {s} 0,2", b_, Q3.loc[(s, "C5"), "0.2"], 1)
chk("FR A1 IND 1,0 → 3,2", 3.2, Q3.loc[("IND", "A1"), "1.0"], 1); chk("FR A1 IND 0,2 → 2,5", 2.5, Q3.loc[("IND", "A1"), "0.2"], 1)
# Morris
for s, par, mu in [("IMP", "Tmax", 7.2), ("IMP", "Topt", 6.2)]:
    chk(f"Morris {s} {par}", mu, MOR[(MOR.sitio == s) & (MOR.parametro == par) & (MOR.resposta == "perda_volume_k72_pp")].mu_estrela.iloc[0], 1)
chk("Morris IND μ* máx < 1", 0.9, MOR[(MOR.sitio == "IND") & (MOR.resposta == "perda_volume_k72_pp")].mu_estrela.max(), 1)
chk("vol ctrl IND máx", 358, C.loc[[("IND", m) for m in ["A1", "C2", "C4", "C5"]]].vol84.max(), 0)
chk("vol ctrl TB máx", 456, C.loc[[("TB", m) for m in ["A1", "C2", "C4", "C5"]]].vol84.max(), 0)
# RF
g = lambda r, mo, es, col: K[(K.resposta == r) & (K.modelo == mo) & (K.esquema == es)][col].iloc[0]
RF = "Random Forest"
chk("RF 3 locais kfold R2", 0.992, g("perda_volume_k72", RF, "k-fold 7 × 10 repetições", "R2_media"), 3)
chk("RF kfold RQEM", 11.6, g("perda_volume_k72", RF, "k-fold 7 × 10 repetições", "RQEM_media"), 1)
chk("RF 3 locais LOSO R2", 0.93, g("perda_volume_k72", RF, "deixa um sítio de fora", "R2_media"), 3)
chk("RF 3 locais LOSO RQEM (texto: 34%)", 34.0, g("perda_volume_k72", RF, "deixa um sítio de fora", "RQEM_media"), 1)
chk("RF LOMO R2", 0.961, g("perda_volume_k72", RF, "deixa um material de fora", "R2_media"), 3)
chk("RF rec LOSO", 0.645, g("recup_rel95_meses_ev1", RF, "deixa um sítio de fora", "R2_media"), 3)
chk("RF rec LOMO", 0.691, g("recup_rel95_meses_ev1", RF, "deixa um material de fora", "R2_media"), 3)
chk("MLP rec LOSO", -0.28, g("recup_rel95_meses_ev1", "RNA MLP (50, 30) ReLU", "deixa um sítio de fora", "R2_media"), 2)
gg = G[(G.modelo == RF) & (G.resposta == "perda_volume_k72")].set_index("grupo_testado")
chk("viés IMP", -21, gg.loc["IMP"].vies_pct, 0); chk("viés IND +13", 19, gg.loc["IND"].vies_pct, 0); chk("viés TB +14", 6, gg.loc["TB"].vies_pct, 0)
chk("A1 fora RQEM", 27, gg.loc["A1"].RQEM_pct, 0)
chk("n volume 1848", 1848, TC[TC.resposta == "perda_volume_k72"].n.iloc[0], 0); chk("n recup", 1720, TC[TC.resposta == "recup_rel95_meses_ev1"].n.iloc[0], 0)
im = IMP[IMP.escopo == "3 locais"].set_index(["resposta", "variavel"]).importancia_relativa_pct
for var, val in [("intensidade", 58.8), ("frequência", 36.6), ("local", 1.7), ("material genético", 1.2)]:
    chk(f"imp vol {var}", val, im[("perda_volume_k72", var)], 1)
for var, val in [("intensidade", 64.7), ("material genético", 7.6), ("época", 9.4)]:
    chk(f"imp rec {var}", val, im[("recup_rel95_meses_ev1", var)], 1)
chk("imp época/água/fert <", 0.9, max(im[("perda_volume_k72", x)] for x in ["época", "água (ASWmax)", "fertilidade (FR)"]), 1)
# outros danos (seção 4.9, Tabela 9) — saida/danos_v2.csv
DN = pd.read_csv(S / "danos_v2.csv"); dv = lambda c: DN[DN.cenario == c].perda_volume_84
chk("psilídeo mín", 0.8, dv("Psilídeo-de-concha").min(), 1); chk("psilídeo máx 1,6", 1.6, dv("Psilídeo-de-concha").max(), 1)
chk("formigas mín", 8.4, dv("Formigas-cortadeiras").min(), 1); chk("formigas máx 14,6", 14.6, dv("Formigas-cortadeiras").max(), 1)
pv = DN[DN.cenario == "Percevejo-bronzeado 40%"]
chk("percevejo TB mín", 2.5, pv[pv.sitio == "TB"].perda_volume_84.min(), 1); chk("percevejo TB máx 2,6", 2.6, pv[pv.sitio == "TB"].perda_volume_84.max(), 1)
chk("percevejo IND/IMP mín", 0.4, pv[pv.sitio != "TB"].perda_volume_84.min(), 1); chk("percevejo IND/IMP máx 0,7", 0.7, pv[pv.sitio != "TB"].perda_volume_84.max(), 1)
fg = DN[DN.cenario.str.startswith("Ferrugem")]
chk("ferrugem r mín", 55, 100 * fg.r_calibrado.min(), 0); chk("ferrugem r máx", 82, 100 * fg.r_calibrado.max(), 0)
chk("ferrugem vol mín", 2.5, fg.perda_volume_84.min(), 1); chk("ferrugem vol máx", 5.1, fg.perda_volume_84.max(), 1)
chk("ferrugem DAP mín", 0.8, fg.perda_DAP_84.min(), 1); chk("ferrugem DAP máx", 1.7, fg.perda_DAP_84.max(), 1)
m15 = DN[DN.cenario == "Mortalidade 15%"]
chk("mort15 mín", 2.9, m15.perda_volume_84.min(), 1); chk("mort15 máx", 3.8, m15.perda_volume_84.max(), 1)
chk("vol/árvore mín +13%", 13, 100 * (m15.vol_arvore_ratio.min() - 1), 0); chk("vol/árvore máx +14%", 14, 100 * (m15.vol_arvore_ratio.max() - 1), 0)
mf = DN[DN.cenario == "Mancha foliar"].recup_rel95_meses
chk("mancha recup mín 18", 18, mf.min(), 0); chk("mancha recup máx 25", 25, mf.max(), 0)
# ===== calibração da compensação e biomas (31/10/2026) =====
CB = Path("/home/claude/tcc/calibracao/saida"); BB = S / "biomas"
J = json.load(open(CB / "calibracao_d0999.json")); J9 = json.load(open(CB / "calibracao_d099.json"))
for k_, t_, c_ in [("U q50", 1.18, J["U"]["q50"]), ("U q05", 1.01, J["U"]["q05"]), ("U q95", 1.34, J["U"]["q95"]),
                   ("a q50", 0.625, J["a"]["q50"]), ("a q05", 0.23, J["a"]["q05"]), ("a q95", 0.975, J["a"]["q95"] + 1e-9),
                   ("corr U-a", -0.01, J["corr_post"]), ("U q50 d0,99", 1.17, J9["U"]["q50"])]:
    chk(k_, t_, c_, 3 if k_ in ("a q95", "a q50") else 2)
for var, ob, orig, cal in [("volume", 52.9, 66.6, 50.9), ("CAP", 24.2, 29.7, 20.5), ("altura", 19.1, 36.1, 25.2)]:
    chk(f"C5 obs {var}", ob, J["observado_C5"][var]); chk(f"C5 orig {var}", orig, J["original_C5"][var]); chk(f"C5 cal {var}", cal, J["preditiva_media_C5"][var])
    chk(f"C5 erro orig {var}", {"volume": 13.7, "CAP": 5.5, "altura": 17.0}[var], J["original_C5"][var] - J["observado_C5"][var])
    chk(f"C5 erro cal {var}", round(cal - ob, 1), J["preditiva_media_C5"][var] - J["observado_C5"][var])
V = J["validacao_A1_urocam"]
for var, ob, orig, cal, lo, hi in [("volume", 59.0, 79.3, 66.5, 59.6, 76.9), ("CAP", 22.9, 40.7, 30.6, 25.9, 38.4)]:
    chk(f"A1 obs {var}", ob, V["observado"][var]); chk(f"A1 orig {var}", orig, V["original"][var]); chk(f"A1 cal {var}", cal, V["calibrado_media"][var])
    chk(f"A1 q05 {var}", lo, V["calibrado_q05"][var]); chk(f"A1 q95 {var}", hi, V["calibrado_q95"][var])
chk("A1 erro orig vol 20,3", 20.3, V["original"]["volume"] - V["observado"]["volume"]); chk("A1 erro cal vol", 7.5, V["calibrado_media"]["volume"] - V["observado"]["volume"])
chk("A1 erro orig CAP 17,7", 17.7, V["original"]["CAP"] - V["observado"]["CAP"]); chk("A1 erro cal CAP", 7.7, V["calibrado_media"]["CAP"] - V["observado"]["CAP"])
chk("d0,99 vol", 62.2, J9["validacao_A1_urocam"]["calibrado_media"]["volume"]); chk("d0,99 CAP", 27.9, J9["validacao_A1_urocam"]["calibrado_media"]["CAP"])
GL = pd.read_csv(CB / "validacao_globulus.csv")
gl = lambda caso, ver, var, col="perda_media": GL[GL.caso.str.startswith(caso) & (GL.versao == ver) & (GL.variavel == var)][col].iloc[0]
chk("Barry IAF orig", 6.6, gl("Barry", "original", "lai")); chk("Barry IAF cal", -0.2, gl("Barry", "calibrado", "lai"))
chk("Barry IAF q05", -3.6, gl("Barry", "calibrado", "lai", "q05")); chk("Barry IAF q95", 3.4, gl("Barry", "calibrado", "lai", "q95"))
chk("globulus ganho máx", 2.8, -GL[GL.variavel.isin(["dbh", "height"])].perda_media.min())
chk("globulus sem perda (máx ≤ 0)", 1, max(0.0, GL[GL.variavel.isin(["dbh", "height"])].perda_media.max()), 1)
# biomas
BO = pd.read_csv(BB / "indicadores_original.csv"); BC = pd.read_csv(BB / "indicadores_calibrado.csv"); BU = pd.read_csv(BB / "incerteza_posterior_d50.csv")
MB = pd.read_csv(BB / "matriz_biomas.csv")
chk("tratamentos com desfolha por versão 1.728", 1728, (MB.desfolha > 0).sum(), 0)
chk("tratamentos por versão 1.728", 1728, len(BO), 0)
Lo = L.set_index(["sitio", "material", "calendario", "desfolha"]).perda_volume_k72
bo = BO[(BO.nivel_FR == "F100")].set_index(["sitio", "material", "calendario", "desfolha"]).perda_volume_k72
chk("original = TCC (dif máx < 1e-10)", 0.0, max(0.0, (bo.reindex(Lo.index) - Lo).abs().max() - 1e-10), 1)
bget = lambda D, s_, m_, cal_, col="perda_volume_k72": D[(D.sitio == s_) & (D.material == m_) & (D.nivel_FR == "F100") & (D.desfolha == 0.5) & (D.calendario == cal_)][col].iloc[0]
T11 = {"IND": (2.7, 1.3, 13.8, 7.3, 3.5, 10.6, 22, 0), "IMP": (2.8, 1.4, 19.4, 8.3, 4.3, 12.0, 17, 2), "TB": (3.1, 1.1, 8.0, 5.8, 4.7, 11.8, 23, 0), "ALM": (3.2, 1.0, 17.4, 5.1, 3.0, 8.7, 24, 1), "ARA": (1.3, 1.0, 15.0, 8.9, 6.9, 11.4, 13, 2), "ELD": (3.2, 1.4, 5.9, 8.3, 7.6, 10.7, 23, 2)}
for s_, (p1o, p1c, pao, pac, lo_, hi_, ro, rc) in T11.items():
    chk(f"T11 {s_} P1 orig", p1o, bget(BO, s_, "C5", "P1")); chk(f"T11 {s_} P1 cal", p1c, bget(BC, s_, "C5", "P1"))
    chk(f"T11 {s_} PA orig", pao, bget(BO, s_, "C5", "PA")); chk(f"T11 {s_} PA cal", pac, bget(BC, s_, "C5", "PA"))
    u_ = BU[(BU.sitio == s_) & (BU.material == "C5") & (BU.calendario == "PA")].iloc[0]
    chk(f"T11 {s_} IC q05", lo_, u_.q05); chk(f"T11 {s_} IC q95", hi_, u_.q95)
    chk(f"T11 {s_} recup orig", ro, bget(BO, s_, "C5", "P1", "recup_rel95_meses_ev1"), 0); chk(f"T11 {s_} recup cal", rc, bget(BC, s_, "C5", "P1", "recup_rel95_meses_ev1"), 0)
# texto 4.5 (biomas, C5, 50%)
T11d = pd.DataFrame(T11, index=["p1o", "p1c", "pao", "pac", "lo", "hi", "ro", "rc"]).T
chk("biomas P1 orig mín 1,3", 1.3, T11d.p1o.min()); chk("biomas P1 orig máx 3,2", 3.2, T11d.p1o.max())
chk("biomas P1 cal mín 1,0", 1.0, T11d.p1c.min()); chk("biomas P1 cal máx 1,4", 1.4, T11d.p1c.max())
chk("biomas recup orig mín 13", 13, T11d.ro.min(), 0); chk("biomas recup orig máx 24", 24, T11d.ro.max(), 0); chk("biomas recup cal máx 2", 2, T11d.rc.max(), 0)
x5 = T11d.drop("ELD")
chk("biomas PA orig mín (sem ELD) 8,0", 8.0, x5.pao.min()); chk("biomas PA orig máx (sem ELD) 19,4", 19.4, x5.pao.max())
chk("biomas PA cal mín (sem ELD) 5,1", 5.1, x5.pac.min()); chk("biomas PA cal máx (sem ELD) 8,9", 8.9, x5.pac.max())
chk("cal < orig PA em 5 locais", 5, int((x5.pac < x5.pao).sum()), 0)
chk("ELD PA orig 5,9", 5.9, T11d.at["ELD", "pao"]); chk("ELD PA cal 8,3", 8.3, T11d.at["ELD", "pac"])
chk("faixa 90% PA mín 3,0", 3.0, T11d.lo.min()); chk("faixa 90% PA máx 12,0", 12.0, T11d.hi.max())
k_ = ["sitio", "material", "nivel_FR", "desfolha", "calendario"]
XB = BO.merge(BC, on=k_, suffixes=("_o", "_c")); XB = XB[(XB.nivel_FR == "F100") & (XB.desfolha == 0.5) & XB.apto_analise_principal_o]
p1 = XB[(XB.calendario == "P1") & (XB.perda_volume_k72_o > 0)]; pa = XB[XB.calendario == "PA"]
chk("razão cal/orig P1", 43, 100 * (p1.perda_volume_k72_c / p1.perda_volume_k72_o).median(), 0)
chk("razão cal/orig PA", 53, 100 * (pa.perda_volume_k72_c / pa.perda_volume_k72_o).median(), 0)
r1 = XB[XB.calendario == "P1"]
chk("recup orig mín", 9, r1.recup_rel95_meses_ev1_o.min(), 0); chk("recup orig máx", 24, r1.recup_rel95_meses_ev1_o.max(), 0)
chk("recup cal mín", 0, r1.recup_rel95_meses_ev1_c.min(), 0); chk("recup cal máx", 7, r1.recup_rel95_meses_ev1_c.max(), 0)
chk("P1 cal C5 < 2% (máx)", 1.4, BC[(BC.material == "C5") & (BC.nivel_FR == "F100") & (BC.desfolha == 0.5) & (BC.calendario == "P1")].perda_volume_k72.max(), 1)
CR = pd.read_csv(BB / "clima_resumo_locais.csv", index_col=0)
chk("ARA chuva 572", 572, CR.at["ARA", "chuva_anual"], 0); chk("ARA meses secos 7", 7, CR.at["ARA", "meses_secos"], 0); chk("ALM chuva 1.862", 1862, CR.at["ALM", "chuva_anual"], 0)
DB = pd.read_csv(BB / "danos_6locais.csv")
fo = DB[(DB.cenario == "Formigas-cortadeiras")]; foA = fo[fo.sitio != "ARA"]
chk("formigas orig mín", 6.6, foA[foA.versao == "original"].perda_volume_84.min()); chk("formigas orig máx", 14.6, foA[foA.versao == "original"].perda_volume_84.max())
chk("formigas cal mín", -1.2, foA[foA.versao == "calibrado"].perda_volume_84.min()); chk("formigas cal máx", 3.6, foA[foA.versao == "calibrado"].perda_volume_84.max())
chk("formigas ARA mín", 1.8, fo[fo.sitio == "ARA"].perda_volume_84.min()); chk("formigas ARA máx", 3.3, fo[fo.sitio == "ARA"].perda_volume_84.max())
RFr = pd.read_csv(BB / "rf_resumo.csv"); RI = pd.read_csv(BB / "rf_importancia.csv")
rr = lambda v_, var_, col: RFr[(RFr.versao == v_) & (RFr.resposta == "perda_volume_k72") & (RFr.variaveis.str.startswith(var_)) & (RFr.esquema == "deixa um local de fora")][col].iloc[0]
chk("RF LOSO orig cat", 39, rr("original", "(a)", "RQEM"), 0); chk("RF LOSO cal cat", 45, rr("calibrado", "(a)", "RQEM"), 0)
chk("RF LOSO cal clim", 43, rr("calibrado", "(b)", "RQEM"), 0); chk("RF R2 orig→cal LOSO cat", 0.88, rr("calibrado", "(a)", "R2"), 2); chk("RF R2 cal clim", 0.9, rr("calibrado", "(b)", "R2"), 2)
ri = lambda v_, var_: RI[(RI.versao == v_) & (RI.resposta == "perda_volume_k72") & (RI.variavel == var_)].importancia_pct.iloc[0]
chk("RF6 intens orig", 51.7, ri("original", "intensidade")); chk("RF6 intens cal", 48.1, ri("calibrado", "intensidade"))
chk("RF6 freq orig", 44.8, ri("original", "frequência")); chk("RF6 freq cal", 48, ri("calibrado", "frequência"))
MOB = pd.read_csv(BB / "morris_C5_6locais.csv"); mv = MOB[MOB.resposta == "perda_volume_84_pp"]
top = mv.loc[mv.groupby("sitio").mu_estrela.idxmax()]
chk("Morris k topo em 5 locais", 5, (top.parametro == "k").sum(), 0)
sys.path.insert(0, str(X)); sys.path.insert(0, "/home/claude/tcc/modelo")
from morris_danos_biomas import sim as _simb  # noqa: E402
aer = [(_simb("ARA", m_).loc[54, "biom_stem"] + _simb("ARA", m_).loc[54, "biom_foliage"]) for m_ in ["A1", "C5", "C2", "C4"]]
chk("ARA biomassa aérea mín 57", 57, min(aer), 0); chk("ARA biomassa aérea máx (faixa medida 51–132)", 71, max(aer), 0)
from run_experimentos import rodar as _r0, linha as _l0  # noqa: E402
from clones import MATERIAIS as _MAT  # noqa: E402
_ima = lambda s_: _r0(_l0(s_, "C5", None, _MAT["C5"]["FR_ref"], "F100", 0.0, "P1", "X", asw={"IND": 215, "TB": 214, "IMP": 210, "ALM": 219, "ARA": 194, "ELD": 145}[s_]))
for s_, t_ in [("IND", 44), ("IMP", 36), ("TB", 55), ("ALM", 64), ("ARA", 22), ("ELD", 52)]:
    o_ = _ima(s_); k84 = (o_.idade_meses - 84).abs().idxmin(); chk(f"IMA C5 {s_}", t_, o_.volume[k84] / 7, 0)
# ===== Missão 07: auditoria da calibração e testes adicionais =====
AC = json.load(open(CB / "auditoria_calibracao.json")); TA = json.load(open(CB / "testes_adicionais.json"))
ua = AC["atribuicao_urocam"]
chk("urocam só U", 79.3, ua["so_U"]["volume"]); chk("urocam só a", 67.3, ua["so_a"]["volume"]); chk("urocam U e a", 66.3, ua["U_e_a"]["volume"])
p16 = AC["prior_U_ate_1_6"]
chk("prior 1,6 U q50 1,30", 1.30, p16["U"][1], 2); chk("prior 1,6 U q05", 1.03, p16["U"][0], 2); chk("prior 1,6 U q95", 1.58, p16["U"][2], 2)
chk("reexecução U q50 = publicado", 1.18, AC["reexecucao"]["U"][1], 2)
GQ = json.load(open(CB / "gamma_quentin2011.json")); gq = {r["gam"]: r["razao"] for r in GQ["grade"]}
chk("γ calibrado com Quentin 2011 = 1", 1.0, GQ["gamma_calibrado"], 1)
chk("Quentin orig −21,5%", 21.5, 100 * (1 - GQ["razao_original"])); chk("Quentin γ0,5", 4.3, 100 * (1 - gq[0.5])); chk("Quentin γ1", 0, 100 * (1 - gq[1.0]))
MTt = pd.DataFrame(TA["matrangolo"])
chk("Matrangolo obs 1x 37,9", 37.9, MTt.observado.iloc[0]); chk("Matrangolo obs 3x 79,7", 79.7, MTt.observado.iloc[3])
chk("Matrangolo orig mín", 7.4, MTt.original.min()); chk("Matrangolo orig máx", 32.1, MTt.original.max())
chk("Matrangolo cal mín", 3.8, MTt.calibrado_mediana.min()); chk("Matrangolo cal máx", 11.5, MTt.calibrado_mediana.max())
chk("Matrangolo RQEM orig", 42, TA["matrangolo_metricas"]["rmse_original"], 0); chk("Matrangolo RQEM cal", 54, TA["matrangolo_metricas"]["rmse_calibrado"], 0)
fo_ = MTt.observado / MTt.original; fc_ = MTt.observado / MTt.calibrado_mediana
chk("fator orig mín", 2, fo_.min(), 0); chk("fator orig máx", 5, fo_.max(), 0); chk("fator cal mín", 7, fc_.min(), 0); chk("fator cal máx", 10, fc_.max(), 0)
OL = json.load(open(CB / "teste_oliveira2014.json"))["resultados"]; o1 = OL["T1 100%"]
chk("Oliveira obs vol 35,4", 35.4, o1["observado"]["volume_publicado"]); chk("Oliveira orig vol", 77.6, o1["original"]["volume"][1]); chk("Oliveira cal vol", 33, o1["calibrado"]["volume"][1])
chk("Oliveira cal q05", 28.1, o1["calibrado_faixa90_mediana_anos"][0]); chk("Oliveira cal q95", 45.8, o1["calibrado_faixa90_mediana_anos"][1])
chk("Oliveira obs DAP 14,8", 14.8, o1["observado"]["diametro_publicado"]); chk("Oliveira obs altura 11,0", 11.0, o1["observado"]["altura_publicada"])
chk("Oliveira orig DAP", 38.2, o1["original"]["dap"][1]); chk("Oliveira cal DAP", 12.1, o1["calibrado"]["dap"][1])
chk("Oliveira orig altura", 45.7, o1["original"]["altura"][1]); chk("Oliveira cal altura", 15.1, o1["calibrado"]["altura"][1])
chk("Oliveira RQEM orig", 34.3, OL["T1_metricas"]["RQEM_original"]); chk("Oliveira RQEM cal", 3.2, OL["T1_metricas"]["RQEM_calibrado"])
chk("Oliveira parciais orig ≤", 8.1, OL["parciais_max_mediana_entre_anos"]["original"]); chk("Oliveira parciais cal ≤", 4.5, OL["parciais_max_mediana_entre_anos"]["calibrado"])
RF_ = json.load(open("/home/claude/tcc/revisao_07/corpus/resumo_filtro.json"))
chk("busca registros 10.000", 10000, RF_["registros_baixados"], 0); chk("busca DOI únicos 7.908", 7908, RF_["unicos_por_doi"], 0)
chk("busca dedup 7.431", 7431, RF_["apos_dedup_titulo"], 0); chk("núcleo 93", 93, RF_["nucleo"], 0); chk("contexto 3-PG 20", 20, RF_["contexto_3pg"], 0)

# Plataforma v8 (Akademia): verificação JS × Python e valor calibrado citado na seção 4.12
import json as _j
_V = _j.load(open(Path(__file__).resolve().parents[1] / "plataforma/verificacao/resultado_verificacao.json"))
chk("cenários JS × Python", 7, len(_V), 0)
chk("dif. rel. máx JS × Python (x1e14)", 1.4, max(v["dif_rel_max"] for v in _V) * 1e14, 1)
sys.path.insert(0, "/home/claude/tcc/modelo")
from threepg_pjs import run_3pg_pjs as _run
from clones import MATERIAIS as _MAT, params as _par
from clima import SITIOS as _SIT, clima_mensal as _cm
import run_experimentos as _RE
_M = _MAT["A1"]; _a = _RE.SOLO_LOCAL["IND"]
_site = dict(latitude=_SIT["IND"]["lat"], altitude=0, soil_class=-1, asw_i=_a, asw_min=0.0, asw_max=_a, **{"from": "2016-01", "to": "2023-01"})
_sp = dict(planted="2015-01", fertility=_M["FR_ref"], stems_n=10000 / 9, biom_stem=_M["WS0"], biom_root=_M["WR0"], biom_foliage=_M["WF0"])
_cl = _cm("IND"); _ev = {"2017-01": .95, "2020-01": .95}
_c = _run(_site, _sp, _cl, _par("A1")); _k = int(np.where(np.round(_c.age * 12) == 84)[0][0])
_t = _run(_site, _sp, _cl, _par("A1"), defoliation_events=_ev)
_tc = _run(_site, _sp, _cl, _par("A1"), defoliation_events=_ev, compensation=dict(U=J["U"]["q50"], a=J["a"]["q50"], gam=json.load(open(CB / "gamma_quentin2011.json"))["gamma_calibrado"], u_meses=json.load(open(CB / "regra_compensacao.json"))["u_meses"]))
chk("plataforma IND A1 2x95 original", 17.3, 100 * (1 - _t.volume[_k] / _c.volume[_k]), 1)
chk("plataforma IND A1 2x95 calibrado", 11.6, 100 * (1 - _tc.volume[_k] / _c.volume[_k]), 1)

# Plataforma: didática e perda por produto (recalculado de plataforma/verificacao/numeros_plataforma.js)
import subprocess as _sp
_NP = _j.loads(_sp.run(["node", "/home/claude/tcc/plataforma/verificacao/numeros_plataforma.js"], capture_output=True, text=True, check=True).stdout)
chk("conceitos", 52, _NP["conceitos"], 0); chk("grupos de conceitos", 7, _NP["grupos"], 0)
chk("pontes biologia", 21, _NP["pontes"], 0); chk("trilha", 15, _NP["trilha"], 0); chk("passos do tutorial", 13, _NP["passos"], 0)
chk("amostras do posterior na plataforma", 200, _NP["amostras"], 0); chk("locais na plataforma", 6, _NP["locais"], 0)
chk("serraria -33,6%", -33.6, _NP["dif_serraria"], 1); chk("serraria ctrl 165", 165, _NP["serraria_c"], 0); chk("serraria desf 110", 110, _NP["serraria_t"], 0)
chk("celulose +5,9%", 5.9, _NP["dif_celulose"], 1); chk("energia +36,8%", 36.8, _NP["dif_energia"], 1)
# Espaço de possibilidades (experimentos/possibilidades*.py) e validação cruzada da calibração
_PS = _j.load(open("/home/claude/tcc/experimentos/saida/possibilidades/resumo_possibilidades.json"))
_O, _C, _T, _K = _PS["original"], _PS["calibrada"], _PS["teste_autor"], _PS["kfold"]; _G = _PS["ganho_por_tipo"]
chk("cenários totais", 7584, _PS["n_cenarios"], 0); chk("cenários aptos", 5688, _PS["n_aptos"], 0); chk("aptos por versão", 2844, _O["n"], 0)
chk("ganho orig %", 0, _O["frac_ganho"], 1); chk("ganho calib %", 1.3, _C["frac_ganho"], 1)
chk("ganho máx orig", 0.1, _O["ganho_max"], 1); chk("ganho máx calib", 5.2, _C["ganho_max"], 1)
chk("só desfolha ganho orig %", 0.7, _G["só desfolha | original"]["frac"], 1); chk("só desfolha ganho calib %", 8.3, _G["só desfolha | calibrada"]["frac"], 1)
chk("só desfolha ganhos calib n", 12, _G["só desfolha | calibrada"]["n_ganho"], 0)
chk("ganhos calib com", 6, _PS["ganho_so_desfolha_calibrada"]["d25_P1"] + _PS["ganho_so_desfolha_calibrada"]["d25_PA"], 0)
chk("ganhos só desfolha calib com até", 10, sum(v for k, v in _PS["ganho_so_desfolha_calibrada"].items() if k[:3] in ("d25", "d50")), 0)
chk("só eficiência ganho", 0.0, _G["só perda de eficiência | calibrada"]["frac"] + _G["só perda de eficiência | original"]["frac"], 1)
chk("só mortalidade ganho %", 0, _G["só mortalidade | original"]["frac"], 1); chk("só mortalidade ganho máx", 0, _G["só mortalidade | original"]["ganho_max"], 1)
chk("mortalidade sozinha sem ganho (locais)", 0, len(_PS["ganho_mortalidade_sitios"]), 0)
chk("desfolha orig: único ganho em TB", 1, 1 if _PS["ganho_so_desfolha_original_sitios"] == ["TB"] else 0, 0); chk("ganho orig: 1 cenário", 1, _O["n_ganho"], 0)
chk("maior ganho IMP C5 25 PA jul calib", 5.2, -_PS["maior_ganho"]["perda_volume"] if (_PS["maior_ganho"]["sitio"], _PS["maior_ganho"]["material"], _PS["maior_ganho"]["d"], _PS["maior_ganho"]["freq"], _PS["maior_ganho"]["epoca"], _PS["maior_ganho"]["versao"]) == ("IMP", "C5", 25, "PA", 7, "calibrada") else 0, 1)
chk("perda mediana orig", 12.7, _O["perda_mediana"], 1); chk("perda mediana calib", 9.6, _C["perda_mediana"], 1)
chk("perda máx orig", 84.4, _O["perda_max"], 1); chk("perda máx calib", 60.3, _C["perda_max"], 1)
chk("folhas recuperam orig %", 52.6, _O["frac_folhas_recuperam"], 1); chk("folhas recuperam calib %", 92.6, _C["frac_folhas_recuperam"], 1)
chk("meses recup orig", 26, _O["recup_folhas_mediana"], 0); chk("meses recup calib", 6, _C["recup_folhas_mediana"], 0)
chk("NPP pós maior orig %", 9.5, _O["frac_npp_pos_maior"], 1); chk("NPP pós maior calib %", 33.3, _C["frac_npp_pos_maior"], 1)
chk("árvore maior com mortalidade %", 54.4, _PS["mortalidade"]["frac_arvore_maior"], 1); chk("árvore maior e talhão menor %", 54.2, _PS["mortalidade"]["frac_arvore_maior_e_talhao_menor"], 1)
chk("teste: vol trat", 268, _T["vol_trat"], 0); chk("teste: vol ctrl 352", 352, _T["vol_ctrl"], 0); chk("teste: perda", 23.8, _T["combinado"], 1)
chk("teste: 4 m pulso1 trat", 2.9, _T["cresc_4m_pos_pulso1_trat"], 1); chk("teste: 4 m pulso2 trat", 3.7, _T["cresc_4m_pos_pulso2_trat"], 1)
chk("teste: 4 m pulso1 ctrl", 31.2, _T["cresc_4m_pos_pulso1_ctrl"], 1); chk("teste: 4 m pulso2 ctrl", 29.7, _T["cresc_4m_pos_pulso2_ctrl"], 1)
chk("teste: IAF trat jan21", 2.9, _T["iaf_jan2021_trat"], 1); chk("teste: IAF ctrl jan21", 1.9, _T["iaf_jan2021_ctrl"], 1)
chk("teste: NPP trat jan21", 4.8, _T["npp_jan2021_trat"], 1); chk("teste: NPP ctrl jan21", 4.4, _T["npp_jan2021_ctrl"], 1)
chk("teste: 72-84 trat", 54.1, _T["cresc_72_84_trat"], 1); chk("teste: 72-84 ctrl", 56.8, _T["cresc_72_84_ctrl"], 1)
chk("teste: DAP trat", 18.6, _T["dap_trat"], 1); chk("teste: DAP ctrl", 18.5, _T["dap_ctrl"], 1); chk("teste: vol/árvore", 1.6, _T["vol_arvore_rel"], 1)
chk("teste: só desfolha", 13.1, _T["so_desfolha"], 1); chk("teste: só eficiência", 12.8, _T["so_eficiencia"], 1); chk("teste: só mortalidade", 5.7, _T["so_mortalidade"], 1)
chk("teste: soma", 31.7, _T["soma_isolados"], 1)
chk("interação mediana", -0.29, _PS["aditividade"]["interacao_mediana"], 2); chk("interação q05", -6, _PS["aditividade"]["interacao_q05"], 1); chk("interação q95", 2.9, _PS["aditividade"]["interacao_q95"], 1)
chk("possib RF kfold R2", 0.992, _K["k-fold 10 × 3"]["R2"], 3); chk("possib RF kfold RQEM", 1.5, _K["k-fold 10 × 3"]["RQEM_pp"], 1)
chk("possib RF LOSO R2", 0.95, _K["deixa um local de fora"]["R2"], 2); chk("possib RF LOSO RQEM", 3.6, _K["deixa um local de fora"]["RQEM_pp"], 1)
_cl = _K["classificacao ganho × perda (k-fold estratificado 10 × 3)"]
chk("classif acurácia", 99.4, _cl["acuracia"], 1); chk("classif balanceada", 89.8, _cl["acuracia_balanceada"], 1); chk("frac ganho", 0.7, _cl["frac_ganho"], 1)
_I = _PS["importancia_pct"]
chk("imp frequência", 38, _I["pulsos anuais"], 1); chk("imp intensidade", 34.8, _I["intensidade d"], 1); chk("imp versão", 11.7, _I["fisiologia calibrada"], 1)
chk("imp eficiência", 7.1, _I["perda de eficiência r"], 1); chk("imp época", 5.2, _I["época"], 1)
chk("clima+solo < 3", 3, 3 if _I["T média"] + _I["chuva anual"] + _I["meses secos"] + _I["CAD"] < 3 else 0, 0)
_VC = _j.load(open("/home/claude/tcc/calibracao/saida/validacao_cruzada.json")); _L5 = _VC["deixa uma observação de fora (k = 5)"]
_K2a, _K2b = _VC["ajusta no C5, prevê o A1 (k = 2)"], _VC["ajusta no A1, prevê o C5 (k = 2)"]
chk("LOO RQEM orig", 15.7, _L5["RQEM_original"], 1); chk("LOO RQEM calib", 4.3, _L5["RQEM_calibrado"], 1)
chk("LOO viés orig", 14.9, _L5["vies_original"], 1); chk("LOO viés calib", 1.7, _L5["vies_calibrado"], 1); chk("LOO melhorou", 5, _L5["melhorou"], 0)
chk("C5→A1 RQEM orig", 19.1, _K2a["RQEM_original"], 1); chk("C5→A1 RQEM calib", 8.4, _K2a["RQEM_calibrado"], 1)
chk("C5→A1 viés orig", 19.0, _K2a["vies_original"], 1); chk("C5→A1 viés calib", 8.4, _K2a["vies_calibrado"], 1)
chk("A1→C5 RQEM orig", 13, _K2b["RQEM_original"], 1); chk("A1→C5 RQEM calib", 4.3, _K2b["RQEM_calibrado"], 1)
chk("A1→C5 viés orig", 12.1, _K2b["vies_original"], 1); chk("A1→C5 viés calib", 0.1, _K2b["vies_calibrado"], 1)
_PV = pd.read_csv("/home/claude/tcc/calibracao/saida/validacao_cruzada_previsoes.csv")
chk("U post mín", 1.18, _PV.U_post.min(), 2); chk("U post máx", 1.18, _PV.U_post.max(), 2)
chk("a post mín", 0.61, _PV.a_post.min(), 2); chk("a post máx", 0.86, _PV.a_post.max(), 2)
# Tabela 1 (clima e solo dos seis locais) — recalculada de clima/power_api e biomas/log_*.txt
from clima import clima_mensal as _cm2
for _s, (_tm, _tn, _tx, _pa, _p0, _p1, _ns) in {"ALM": (27.3, 23.7, 31.0, 1862, 1398, 2449, 2), "ARA": (26.9, 20.7, 33.1, 572, 418, 922, 7), "ELD": (19.9, 15.1, 24.8, 1459, 1104, 1699, 0)}.items():
    _m = _cm2(_s); _m = _m[_m.year <= 2024]; _a = _m.groupby("year").prcp.sum(); _sec = _m.groupby("month").prcp.mean()
    chk(f"T1 {_s} Tméd", _tm, _m.tmp_ave.mean(), 1); chk(f"T1 {_s} Tmín", _tn, _m.tmp_min.mean(), 1); chk(f"T1 {_s} Tmáx", _tx, _m.tmp_max.mean(), 1)
    chk(f"T1 {_s} chuva", _pa, _a.mean(), 0); chk(f"T1 {_s} chuva mín", _p0, _a.min(), 0); chk(f"T1 {_s} chuva máx", _p1, _a.max(), 0)
    chk(f"T1 {_s} meses secos", _ns, int((_sec < 50).sum()), 0); chk(f"T1 {_s} geada", 0, int(_m.frost_days.sum()), 0)
for _s, (_lo, _hi) in {"ALM": (215, 224), "ARA": (188, 198)}.items():
    _v = [float(l.split()[3]) for l in open(f"/home/claude/tcc/biomas/log_{_s}.txt") if l.startswith(_s + " ") and l.split()[3] != "None"]
    chk(f"T1 {_s} ASW mín", _lo, min(_v), 0); chk(f"T1 {_s} ASW máx", _hi, max(_v), 0)
O = pd.DataFrame(ok); O.to_csv("/home/claude/tcc/auditoria_final/auditoria_numeros.csv", index=False)
print(len(O), "itens;", int(O.ok.sum()), "conferem"); print(O[~O.ok].to_string())
