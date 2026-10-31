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
for (s, m), vol, ima, lenho, lai, ft in [(("TB", "A1"), 429, 61, 37.1, 4.8, 0), (("TB", "C5"), 417, 60, 40.0, 10.3, 0), (("IND", "A1"), 352, 50, 25.9, 3.6, 0),
                                       (("IND", "C5"), 356, 51, 28.8, 8.5, 0), (("IMP", "A1"), 227, 32, 14.6, 2.1, 31), (("IMP", "C5"), 315, 45, 22.6, 7.2, 0)]:
    r = C.loc[(s, m)]
    chk(f"vol84 {s} {m}", vol, r.vol84, 0); chk(f"IMA {s} {m}", ima, r.IMA84, 0); chk(f"lenho {s} {m}", lenho, r.caule_24_36, 1)
    chk(f"IAF {s} {m}", lai, r.LAI_24_36, 1); chk(f"fT0 {s} {m}", ft, r.meses_fT0, 0)
chk("+9% lenho TB vs 34", 9, 100 * (C.loc[("TB", "A1")].caule_24_36 / 34 - 1), 0)
chk("+26% IAF TB vs 3,8", 26, 100 * (C.loc[("TB", "A1")].LAI_24_36 / 3.8 - 1), 0)
chk("ΔLenho IND→TB 11", 11, C.loc[("TB", "A1")].caule_24_36 - C.loc[("IND", "A1")].caule_24_36, 0)
chk("fSW IND 0,53", 0.53, C.loc[("IND", "A1")].fSW_med, 2); chk("fSW TB 0,73", 0.73, C.loc[("TB", "A1")].fSW_med, 2)
chk("IAF max Borges mín 8", 8, min(C.loc[(s, m)].LAImax for s in ["IND", "TB", "IMP"] for m in ["C2", "C4", "C5"]), 0)
chk("IAF max Borges máx 11", 11, max(C.loc[(s, m)].LAImax for s in ["IND", "TB", "IMP"] for m in ["C2", "C4", "C5"]), 0)
# tabela 5 e textos
T5 = {"IND": {"A1": [[1.6, 3.0, 9.5], [2.1, 4.4, 17.3], [6.7, 13.8, 58.0], [15, 23, 24]], "C5": [[0.6, 1.6, 8.9], [1.5, 4.3, 16.6], [4.2, 11.5, 47.0], [20, 28, 38]]},
      "TB": {"A1": [[1.2, 3.3, 15.2], [0.5, 2.7, 25.6], [1.8, 6.8, 67.8], [14, 24, 26]], "C5": [[0.3, 1.0, 9.5], [1.1, 3.3, 16.3], [3.5, 7.4, 47.6], [21, 33, 44]]},
      "IMP": {"A1": [[2.8, 6.2, 31.7], [6.0, 14.6, 60.5], [16.4, 37.5, 84.1], [23, 28, 47]], "C5": [[0.8, 2.3, 11.3], [2.0, 5.5, 25.4], [5.5, 16.3, 60.4], [15, 26, 38]]}}
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
chk("época Borges amplitude < 0,5", 0.5, max(0.5, Ep.groupby(["sitio", "material"]).perda_volume_k72.agg(lambda x: x.max() - x.min()).max()), 1)
# Q6
p = E.pivot_table(index=["sitio", "material", "W", "nivel_FR", "desfolha"], columns="calendario", values=["perda_volume_k72", "perda_NPP_acum_pct"])
chk("pares 576", 576, len(p), 0); chk("95% NPP P2>P1", 95, 100 * (p[("perda_NPP_acum_pct", "P2")] > p[("perda_NPP_acum_pct", "P1")]).mean(), 0)
chk("razão mediana 2,1", 2.1, (p[("perda_volume_k72", "P2")] / p[("perda_volume_k72", "P1")]).median(), 1)
mm = p[p[("perda_volume_k72", "P2")] < p[("perda_volume_k72", "P1")]].reset_index()
chk("28 pares P2<P1", 28, len(mm), 0); chk("25 do A1", 25, (mm.material == "A1").sum(), 0); chk("20 com 25%", 20, ((mm.material == "A1") & (mm.desfolha == .25)).sum(), 0)
# solo
chk("amplitude mín 0,4", 0.4, Q1.amplitude_perda_pp.min(), 1); chk("amplitude máx 2,3", 2.3, Q1.amplitude_perda_pp.max(), 1)
q = Q1.set_index(["sitio", "material"])
chk("A1 água IND 70", 70, q.loc[("IND", "A1")].pct_SQ_agua, 0); chk("A1 água TB ~100", 100, q.loc[("TB", "A1")].pct_SQ_agua, 0)
b = q.loc[[("IND", m) for m in ["C2", "C4", "C5"]] + [("IMP", m) for m in ["C2", "C4", "C5"]]].pct_SQ_FR
chk("FR Borges mín 89", 89, b.min(), 0); chk("FR Borges máx 94", 94, b.max(), 0)
tb = q.loc[[("TB", m) for m in ["C2", "C4", "C5"]]][["pct_SQ_agua", "pct_SQ_FR"]]
chk("TB Borges mín 44", 44, tb.min().min(), 0); chk("TB Borges máx 50", 50, tb.max().max(), 0)
d = DEC[DEC.resposta == "perda_volume_k72"].set_index("sitio").material
chk("material IND 45", 45, d["IND"], 0); chk("material TB 49", 49, d["TB"], 0); chk("material IMP 28", 28, d["IMP"], 0)
for s, a_, b_ in [("IND", 1.5, 4.8), ("TB", 0.9, 3.8), ("IMP", 2.1, 5.3)]:
    chk(f"FR C5 {s} 1,0", a_, Q3.loc[(s, "C5"), "1.0"], 1); chk(f"FR C5 {s} 0,2", b_, Q3.loc[(s, "C5"), "0.2"], 1)
chk("FR A1 IND 1,0 → 3,2", 3.2, Q3.loc[("IND", "A1"), "1.0"], 1); chk("FR A1 IND 0,2 → 2,5", 2.5, Q3.loc[("IND", "A1"), "0.2"], 1)
# Morris
for s, par, mu in [("IMP", "Tmax", 7.2), ("IMP", "Topt", 6.2)]:
    chk(f"Morris {s} {par}", mu, MOR[(MOR.sitio == s) & (MOR.parametro == par) & (MOR.resposta == "perda_volume_k72_pp")].mu_estrela.iloc[0], 1)
chk("Morris IND μ* máx < 1", 0.9, MOR[(MOR.sitio == "IND") & (MOR.resposta == "perda_volume_k72_pp")].mu_estrela.max(), 1)
chk("vol ctrl IND máx 424", 424, C.loc[[("IND", m) for m in ["A1", "C2", "C4", "C5"]]].vol84.max(), 0)
chk("vol ctrl TB máx 497", 497, C.loc[[("TB", m) for m in ["A1", "C2", "C4", "C5"]]].vol84.max(), 0)
# RF
g = lambda r, mo, es, col: K[(K.resposta == r) & (K.modelo == mo) & (K.esquema == es)][col].iloc[0]
RF = "Random Forest"
chk("RF kfold R2 0,996", .996, g("perda_volume_k72", RF, "k-fold 7 × 10 repetições", "R2_media"), 3)
chk("RF kfold RQEM 7,7", 7.7, g("perda_volume_k72", RF, "k-fold 7 × 10 repetições", "RQEM_media"), 1)
chk("RF LOSO R2 0,907", .907, g("perda_volume_k72", RF, "deixa um sítio de fora", "R2_media"), 3)
chk("RF LOSO RQEM 37,6", 37.6, g("perda_volume_k72", RF, "deixa um sítio de fora", "RQEM_media"), 1)
chk("RF LOMO R2 0,970", .970, g("perda_volume_k72", RF, "deixa um material de fora", "R2_media"), 3)
chk("RF rec LOSO 0,880", .880, g("recup_rel95_meses_ev1", RF, "deixa um sítio de fora", "R2_media"), 3)
chk("RF rec LOMO −1,149", -1.149, g("recup_rel95_meses_ev1", RF, "deixa um material de fora", "R2_media"), 3)
chk("MLP rec LOSO 0,30", .30, g("recup_rel95_meses_ev1", "RNA MLP (50, 30) ReLU", "deixa um sítio de fora", "R2_media"), 2)
gg = G[(G.modelo == RF) & (G.resposta == "perda_volume_k72")].set_index("grupo_testado")
chk("viés IMP −28", -28, gg.loc["IMP"].vies_pct, 0); chk("viés IND +13", 13, gg.loc["IND"].vies_pct, 0); chk("viés TB +14", 14, gg.loc["TB"].vies_pct, 0)
chk("A1 fora RQEM 40", 40, gg.loc["A1"].RQEM_pct, 0)
chk("n volume 1848", 1848, TC[TC.resposta == "perda_volume_k72"].n.iloc[0], 0); chk("n recup 1519", 1519, TC[TC.resposta == "recup_rel95_meses_ev1"].n.iloc[0], 0)
im = IMP[IMP.escopo == "3 locais"].set_index(["resposta", "variavel"]).importancia_relativa_pct
for var, val in [("intensidade", 57.0), ("frequência", 38.3), ("local", 2.5), ("material genético", 1.0)]:
    chk(f"imp vol {var}", val, im[("perda_volume_k72", var)], 1)
for var, val in [("intensidade", 58.2), ("material genético", 24.8), ("época", 10.8)]:
    chk(f"imp rec {var}", val, im[("recup_rel95_meses_ev1", var)], 1)
chk("imp época/água/fert < 0,5", 0.4, max(im[("perda_volume_k72", x)] for x in ["época", "água (ASWmax)", "fertilidade (FR)"]), 1)
# outros danos (seção 4.9, Tabela 9) — saida/danos_v2.csv
DN = pd.read_csv(S / "danos_v2.csv"); dv = lambda c: DN[DN.cenario == c].perda_volume_84
chk("psilídeo mín 0,4", 0.4, dv("Psilídeo-de-concha").min(), 1); chk("psilídeo máx 1,6", 1.6, dv("Psilídeo-de-concha").max(), 1)
chk("formigas mín 4,0", 4.0, dv("Formigas-cortadeiras").min(), 1); chk("formigas máx 14,6", 14.6, dv("Formigas-cortadeiras").max(), 1)
pv = DN[DN.cenario == "Percevejo-bronzeado 40%"]
chk("percevejo TB mín 2,1", 2.1, pv[pv.sitio == "TB"].perda_volume_84.min(), 1); chk("percevejo TB máx 2,6", 2.6, pv[pv.sitio == "TB"].perda_volume_84.max(), 1)
chk("percevejo IND/IMP mín 0,3", 0.3, pv[pv.sitio != "TB"].perda_volume_84.min(), 1); chk("percevejo IND/IMP máx 0,7", 0.7, pv[pv.sitio != "TB"].perda_volume_84.max(), 1)
fg = DN[DN.cenario.str.startswith("Ferrugem")]
chk("ferrugem r mín 63", 63, 100 * fg.r_calibrado.min(), 0); chk("ferrugem r máx 92", 92, 100 * fg.r_calibrado.max(), 0)
chk("ferrugem vol mín 1,3", 1.3, fg.perda_volume_84.min(), 1); chk("ferrugem vol máx 4,0", 4.0, fg.perda_volume_84.max(), 1)
chk("ferrugem DAP mín 0,4", 0.4, fg.perda_DAP_84.min(), 1); chk("ferrugem DAP máx 1,3", 1.3, fg.perda_DAP_84.max(), 1)
m15 = DN[DN.cenario == "Mortalidade 15%"]
chk("mort15 mín 1,4", 1.4, m15.perda_volume_84.min(), 1); chk("mort15 máx 3,4", 3.4, m15.perda_volume_84.max(), 1)
chk("vol/árvore mín +14%", 14, 100 * (m15.vol_arvore_ratio.min() - 1), 0); chk("vol/árvore máx +16%", 16, 100 * (m15.vol_arvore_ratio.max() - 1), 0)
mf = DN[DN.cenario == "Mancha foliar"].recup_rel95_meses
chk("mancha recup mín 24", 24, mf.min(), 0); chk("mancha recup máx 35", 35, mf.max(), 0)
# ===== calibração da compensação e biomas (31/10/2026) =====
CB = Path("/home/claude/tcc/calibracao/saida"); BB = S / "biomas"
J = json.load(open(CB / "calibracao_d0999.json")); J9 = json.load(open(CB / "calibracao_d099.json"))
for k_, t_, c_ in [("U q50", 1.16, J["U"]["q50"]), ("U q05", 1.02, J["U"]["q05"]), ("U q95", 1.33, J["U"]["q95"]),
                   ("a q50", 0.55, J["a"]["q50"]), ("a q05", 0.05, J["a"]["q05"]), ("a q95", 0.975, J["a"]["q95"] + 1e-9),
                   ("corr U-a", 0.09, J["corr_post"]), ("U q50 d0,99", 1.07, J9["U"]["q50"])]:
    chk(k_, t_, c_, 3 if k_ == "a q95" else 2)
for var, ob, orig, cal in [("volume", 52.9, 64.8, 50.4), ("CAP", 24.2, 28.5, 20.2), ("altura", 19.1, 34.7, 24.9)]:
    chk(f"C5 obs {var}", ob, J["observado_C5"][var]); chk(f"C5 orig {var}", orig, J["original_C5"][var]); chk(f"C5 cal {var}", cal, J["preditiva_media_C5"][var])
    chk(f"C5 erro orig {var}", {"volume": 12.0, "CAP": 4.3, "altura": 15.7}[var], J["original_C5"][var] - J["observado_C5"][var])
    chk(f"C5 erro cal {var}", round(cal - ob, 1), J["preditiva_media_C5"][var] - J["observado_C5"][var])
V = J["validacao_A1_urocam"]
for var, ob, orig, cal, lo, hi in [("volume", 59.0, 79.3, 64.8, 53.7, 78.6), ("CAP", 22.9, 40.7, 29.7, 22.5, 40.0)]:
    chk(f"A1 obs {var}", ob, V["observado"][var]); chk(f"A1 orig {var}", orig, V["original"][var]); chk(f"A1 cal {var}", cal, V["calibrado_media"][var])
    chk(f"A1 q05 {var}", lo, V["calibrado_q05"][var]); chk(f"A1 q95 {var}", hi, V["calibrado_q95"][var])
chk("A1 erro orig vol 20,3", 20.3, V["original"]["volume"] - V["observado"]["volume"]); chk("A1 erro cal vol 5,8", 5.8, V["calibrado_media"]["volume"] - V["observado"]["volume"])
chk("A1 erro orig CAP 17,7", 17.7, V["original"]["CAP"] - V["observado"]["CAP"]); chk("A1 erro cal CAP 6,8", 6.8, V["calibrado_media"]["CAP"] - V["observado"]["CAP"])
chk("d0,99 vol 56,0", 56.0, J9["validacao_A1_urocam"]["calibrado_media"]["volume"]); chk("d0,99 CAP 24,1", 24.1, J9["validacao_A1_urocam"]["calibrado_media"]["CAP"])
GL = pd.read_csv(CB / "validacao_globulus.csv")
gl = lambda caso, ver, var, col="perda_media": GL[GL.caso.str.startswith(caso) & (GL.versao == ver) & (GL.variavel == var)][col].iloc[0]
chk("Barry IAF orig 8,3", 8.3, gl("Barry", "original", "lai")); chk("Barry IAF cal 1,4", 1.4, gl("Barry", "calibrado", "lai"))
chk("Barry IAF q05 −2,4", -2.4, gl("Barry", "calibrado", "lai", "q05")); chk("Barry IAF q95 6,7", 6.7, gl("Barry", "calibrado", "lai", "q95"))
chk("globulus ganho máx 1,6", 1.6, -GL[GL.variavel.isin(["dbh", "height"])].perda_media.min())
chk("globulus sem perda (máx ≤ 0)", 0.0, max(0.0, GL[GL.variavel.isin(["dbh", "height"])].perda_media.max()), 1)
# biomas
BO = pd.read_csv(BB / "indicadores_original.csv"); BC = pd.read_csv(BB / "indicadores_calibrado.csv"); BU = pd.read_csv(BB / "incerteza_posterior_d50.csv")
MB = pd.read_csv(BB / "matriz_biomas.csv")
chk("tratamentos com desfolha por versão 1.728", 1728, (MB.desfolha > 0).sum(), 0)
chk("tratamentos por versão 1.728", 1728, len(BO), 0)
Lo = L.set_index(["sitio", "material", "calendario", "desfolha"]).perda_volume_k72
bo = BO[(BO.nivel_FR == "F100")].set_index(["sitio", "material", "calendario", "desfolha"]).perda_volume_k72
chk("original = TCC (dif máx < 1e-10)", 0.0, max(0.0, (bo.reindex(Lo.index) - Lo).abs().max() - 1e-10), 1)
bget = lambda D, s_, m_, cal_, col="perda_volume_k72": D[(D.sitio == s_) & (D.material == m_) & (D.nivel_FR == "F100") & (D.desfolha == 0.5) & (D.calendario == cal_)][col].iloc[0]
T11 = {"IND": (1.6, 0.7, 11.5, 4.6, -3.4, 9.6, 28, 12), "IMP": (2.3, 1.5, 16.3, 6.5, 1.0, 10.8, 26, 14), "TB": (1.0, 0.6, 7.4, 1.2, -7.2, 8.2, 33, 11),
       "ALM": (0.7, 0.4, 6.5, 1.4, -5.6, 4.9, 29, 13), "ARA": (-2.5, -0.4, 3.2, 1.4, -5.2, 8.2, 4, 2), "ELD": (1.1, 0.4, 6.4, 2.2, -9.0, 9.5, 34, 11)}
for s_, (p1o, p1c, pao, pac, lo_, hi_, ro, rc) in T11.items():
    chk(f"T11 {s_} P1 orig", p1o, bget(BO, s_, "C5", "P1")); chk(f"T11 {s_} P1 cal", p1c, bget(BC, s_, "C5", "P1"))
    chk(f"T11 {s_} PA orig", pao, bget(BO, s_, "C5", "PA")); chk(f"T11 {s_} PA cal", pac, bget(BC, s_, "C5", "PA"))
    u_ = BU[(BU.sitio == s_) & (BU.material == "C5") & (BU.calendario == "PA")].iloc[0]
    chk(f"T11 {s_} IC q05", lo_, u_.q05); chk(f"T11 {s_} IC q95", hi_, u_.q95)
    chk(f"T11 {s_} recup orig", ro, bget(BO, s_, "C5", "P1", "recup_rel95_meses_ev1"), 0); chk(f"T11 {s_} recup cal", rc, bget(BC, s_, "C5", "P1", "recup_rel95_meses_ev1"), 0)
k_ = ["sitio", "material", "nivel_FR", "desfolha", "calendario"]
XB = BO.merge(BC, on=k_, suffixes=("_o", "_c")); XB = XB[(XB.nivel_FR == "F100") & (XB.desfolha == 0.5) & XB.apto_analise_principal_o]
p1 = XB[(XB.calendario == "P1") & (XB.perda_volume_k72_o > 0)]; pa = XB[XB.calendario == "PA"]
chk("razão cal/orig P1 55%", 55, 100 * (p1.perda_volume_k72_c / p1.perda_volume_k72_o).median(), 0)
chk("razão cal/orig PA 34%", 34, 100 * (pa.perda_volume_k72_c / pa.perda_volume_k72_o).median(), 0)
r1 = XB[XB.calendario == "P1"]
chk("recup orig mín 4", 4, r1.recup_rel95_meses_ev1_o.min(), 0); chk("recup orig máx 35", 35, r1.recup_rel95_meses_ev1_o.max(), 0)
chk("recup cal mín 2", 2, r1.recup_rel95_meses_ev1_c.min(), 0); chk("recup cal máx 14", 14, r1.recup_rel95_meses_ev1_c.max(), 0)
chk("P1 cal C5 < 2% (máx)", 1.5, BC[(BC.material == "C5") & (BC.nivel_FR == "F100") & (BC.desfolha == 0.5) & (BC.calendario == "P1")].perda_volume_k72.max(), 1)
CR = pd.read_csv(BB / "clima_resumo_locais.csv", index_col=0)
chk("ARA chuva 572", 572, CR.at["ARA", "chuva_anual"], 0); chk("ARA meses secos 7", 7, CR.at["ARA", "meses_secos"], 0); chk("ALM chuva 1.862", 1862, CR.at["ALM", "chuva_anual"], 0)
DB = pd.read_csv(BB / "danos_6locais.csv")
fo = DB[(DB.cenario == "Formigas-cortadeiras")]; foA = fo[fo.sitio != "ARA"]
chk("formigas orig mín 2,5", 2.5, foA[foA.versao == "original"].perda_volume_84.min()); chk("formigas orig máx 6,6", 6.6, foA[foA.versao == "original"].perda_volume_84.max())
chk("formigas cal mín 0,5", 0.5, foA[foA.versao == "calibrado"].perda_volume_84.min()); chk("formigas cal máx 3,0", 3.0, foA[foA.versao == "calibrado"].perda_volume_84.max())
chk("formigas ARA mín −0,6", -0.6, fo[fo.sitio == "ARA"].perda_volume_84.min()); chk("formigas ARA máx 1,5", 1.5, fo[fo.sitio == "ARA"].perda_volume_84.max())
RFr = pd.read_csv(BB / "rf_resumo.csv"); RI = pd.read_csv(BB / "rf_importancia.csv")
rr = lambda v_, var_, col: RFr[(RFr.versao == v_) & (RFr.resposta == "perda_volume_k72") & (RFr.variaveis.str.startswith(var_)) & (RFr.esquema == "deixa um local de fora")][col].iloc[0]
chk("RF LOSO orig cat 63", 63, rr("original", "(a)", "RQEM"), 0); chk("RF LOSO cal cat 143", 143, rr("calibrado", "(a)", "RQEM"), 0)
chk("RF LOSO cal clim 69", 69, rr("calibrado", "(b)", "RQEM"), 0); chk("RF R2 cal cat 0,17", 0.17, rr("calibrado", "(a)", "R2"), 2); chk("RF R2 cal clim 0,83", 0.83, rr("calibrado", "(b)", "R2"), 2)
ri = lambda v_, var_: RI[(RI.versao == v_) & (RI.resposta == "perda_volume_k72") & (RI.variavel == var_)].importancia_pct.iloc[0]
chk("RF6 intens orig 50,6", 50.6, ri("original", "intensidade")); chk("RF6 intens cal 47,3", 47.3, ri("calibrado", "intensidade"))
chk("RF6 freq orig 44,3", 44.3, ri("original", "frequência")); chk("RF6 freq cal 42,1", 42.1, ri("calibrado", "frequência"))
MOB = pd.read_csv(BB / "morris_C5_6locais.csv"); mv = MOB[MOB.resposta == "perda_volume_84_pp"]
top = mv.loc[mv.groupby("sitio").mu_estrela.idxmax()]
chk("Morris nWs topo nos 6 locais", 6, (top.parametro == "nWs").sum(), 0)
chk("Morris nWs mín 0,69", 0.69, top.mu_estrela.min(), 2); chk("Morris nWs máx 1,86", 1.86, top.mu_estrela.max(), 2)
sys.path.insert(0, str(X)); sys.path.insert(0, "/home/claude/tcc/modelo")
from morris_danos_biomas import sim as _simb  # noqa: E402
aer = [(_simb("ARA", m_).loc[54, "biom_stem"] + _simb("ARA", m_).loc[54, "biom_foliage"]) for m_ in ["A1", "C5", "C2", "C4"]]
chk("ARA biomassa aérea mín 57", 57, min(aer), 0); chk("ARA biomassa aérea máx 62", 62, max(aer), 0)
from run_experimentos import rodar as _r0, linha as _l0  # noqa: E402
from clones import MATERIAIS as _MAT  # noqa: E402
_ima = lambda s_: _r0(_l0(s_, "C5", None, _MAT["C5"]["FR_ref"], "F100", 0.0, "P1", "X", asw={"IND": 215, "TB": 214, "IMP": 210, "ALM": 219, "ARA": 194, "ELD": 145}[s_]))
for s_, t_ in [("IND", 51), ("IMP", 45), ("TB", 60), ("ALM", 70), ("ARA", 20), ("ELD", 56)]:
    o_ = _ima(s_); k84 = (o_.idade_meses - 84).abs().idxmin(); chk(f"IMA C5 {s_}", t_, o_.volume[k84] / 7, 0)
# ===== Missão 07: auditoria da calibração e testes adicionais =====
AC = json.load(open(CB / "auditoria_calibracao.json")); TA = json.load(open(CB / "testes_adicionais.json"))
ua = AC["atribuicao_urocam"]
chk("urocam só U 79,1", 79.1, ua["so_U"]["volume"]); chk("urocam só a 70,1", 70.1, ua["so_a"]["volume"]); chk("urocam U e a 61,7", 61.7, ua["U_e_a"]["volume"])
p16 = AC["prior_U_ate_1_6"]
chk("prior 1,6 U q50 1,21", 1.21, p16["U"][1], 2); chk("prior 1,6 U q05 1,02", 1.02, p16["U"][0], 2); chk("prior 1,6 U q95 1,54", 1.54, p16["U"][2], 2)
chk("reexecução U q50 = publicado", 1.16, AC["reexecucao"]["U"][1], 2)
qa = {r["versao"]: r["razao_transpiracao_7meses"] for r in TA["quentin2011_transpiracao_A1"]}
chk("Quentin orig −21,5%", 21.5, 100 * (1 - qa["original"])); chk("Quentin γ0,5 −4,5%", 4.5, 100 * (1 - qa["calibrado γ=0,5"])); chk("Quentin γ1 −0,2%", 0.2, 100 * (1 - qa["calibrado γ=1"]))
MTt = pd.DataFrame(TA["matrangolo"])
chk("Matrangolo obs 1x 37,9", 37.9, MTt.observado.iloc[0]); chk("Matrangolo obs 3x 79,7", 79.7, MTt.observado.iloc[3])
chk("Matrangolo orig mín 2,6", 2.6, MTt.original.min()); chk("Matrangolo orig máx 12,7", 12.7, MTt.original.max())
chk("Matrangolo cal mín 1,1", 1.1, MTt.calibrado_mediana.min()); chk("Matrangolo cal máx 8,5", 8.5, MTt.calibrado_mediana.max())
chk("Matrangolo RQEM orig 54", 54, TA["matrangolo_metricas"]["rmse_original"], 0); chk("Matrangolo RQEM cal 56", 56, TA["matrangolo_metricas"]["rmse_calibrado"], 0)
fo_ = MTt.observado / MTt.original; fc_ = MTt.observado / MTt.calibrado_mediana
chk("fator orig mín 6", 6, fo_.min(), 0); chk("fator orig máx 15", 15, fo_.max(), 0); chk("fator cal mín 9", 9, fc_.min(), 0); chk("fator cal máx 34", 34, fc_.max(), 0)
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
_tc = _run(_site, _sp, _cl, _par("A1"), defoliation_events=_ev, compensation=dict(U=1.16, a=0.55, gam=0.5))
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
O = pd.DataFrame(ok); O.to_csv("/home/claude/tcc/auditoria_final/auditoria_numeros.csv", index=False)
print(len(O), "itens;", int(O.ok.sum()), "conferem"); print(O[~O.ok].to_string())
