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
O = pd.DataFrame(ok); O.to_csv("/home/claude/tcc/auditoria_final/auditoria_numeros.csv", index=False)
print(len(O), "itens;", int(O.ok.sum()), "conferem"); print(O[~O.ok].to_string())
