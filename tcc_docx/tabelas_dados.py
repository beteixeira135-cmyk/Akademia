#!/usr/bin/env python3
"""Gera as linhas das tabelas completas (Material do TCC da Akademia e Figura N2) direto das saídas dos códigos,
para que nenhum número de tabela seja digitado à mão. Saída: tcc_docx/tabelas_dados.json, lida por gerar.js.
Rodar depois de qualquer reprocessamento e antes de gerar.js e plataforma/extrair_material_tcc.js."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]; X = R / "experimentos"; S = X / "saida"; CB = R / "calibracao/saida"; BB = S / "biomas"
sys.path.insert(0, str(X)); sys.path.insert(0, str(R / "modelo")); sys.path.insert(0, str(R / "calibracao"))


def f(x, d=1):
    s = f"{float(x):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s.replace("-", "−") if s.lstrip("-").strip("0,.") else s.replace("-", "")  # sem "−0,0"


def i(x): return f(round(float(x)), 0)


T = {}; NOTAS = {}
IND = pd.read_csv(S / "indicadores_por_tratamento.csv")
L = IND[(IND.experimento == "LOCAL") & (IND.nivel_FR == "F100")]
v = lambda s, m, cal, d, col="perda_volume_k72": L[(L.sitio == s) & (L.material == m) & (L.calendario == cal) & (L.desfolha == d)][col].iloc[0]
NOME = {"IND": "Indianópolis", "TB": "Telêmaco Borba", "IMP": "Imperatriz"}

# materiais (parâmetros do código)
from clones import params, MATERIAIS
mrow = lambda m, esp, uso, ini: [m, esp, ini, f(params(m)["alphaCx"], 3 if m == "A1" else 2), f(params(m)["Tmax"], 2 if m == "A1" else 0),
                                 f"{f(params(m)['SLA0'], 2)} → {f(params(m)['SLA1'], 2)}", f(params(m)["fN0"], 1), uso]
T["materiais"] = [mrow("A1", "*E. urophylla*; Caldeira et al. (2020a)", "Principal", "12 meses"),
                  mrow("C5", "*E. grandis* × *E. urophylla*, Cerrado-MG; Borges (2009)", "Comparativo", "3 meses"),
                  mrow("C2", "Clone 3336, Curvelo-MG; Borges (2009)", "Adicional", "3 meses"),
                  mrow("C4", "Clone 3336, Itacambira-MG; Borges (2009)", "Adicional", "3 meses")]

# controles
C = pd.read_csv(S / "controles_solo_local.csv").set_index(["sitio", "mat"])
T["controles"] = []
for s in ["TB", "IND", "IMP"]:
    for m in ["A1", "C5"]:
        r = C.loc[(s, m)]
        T["controles"].append(["" if m == "C5" else NOME[s], m + ("*" if (s, m) == ("IMP", "A1") else ""), i(r.vol84), i(r.IMA84), f(r.caule_24_36), f(r.LAI_24_36), i(r.meses_fT0),
                               "34 Mg ha^-1^ ano^-1^ (24–36 meses); IAF 3,8 (24 meses; TECHS 22)" if (s, m) == ("TB", "A1") else "–"])

# principal
T["principal"] = []
for s in ["IND", "TB", "IMP"]:
    st = "*" if s == "IMP" else ""
    for cal, nome in [("P1", "Pulso único"), ("P2", "Dois pulsos"), ("PA", "Pulsos anuais")]:
        T["principal"].append([NOME[s] if cal == "P1" else "", nome] + [f(v(s, "A1", cal, d)) + st for d in (.25, .5, .95)] + [f(v(s, "C5", cal, d)) for d in (.25, .5, .95)])
    T["principal"].append(["", "Recuperação (meses)"] + [i(v(s, "A1", "P1", d, "recup_rel95_meses_ev1")) + st for d in (.25, .5, .95)] +
                          [i(v(s, "C5", "P1", d, "recup_rel95_meses_ev1")) for d in (.25, .5, .95)])

# materialclima (16 cenários de água e fertilidade)
E = IND[(IND.experimento == "E1-E6") & (IND.calendario == "P1") & (IND.desfolha == 0.5)]
T["materialclima"] = []
for s in ["IND", "TB", "IMP"]:
    row = [NOME[s]]
    for m in ["A1", "C5", "C2", "C4"]:
        x = E[(E.sitio == s) & (E.material == m)].perda_volume_k72
        row.append(f"{f(x.mean())} ({f(x.min())}–{f(x.max())})" + ("*" if (s, m) == ("IMP", "A1") else ""))
    T["materialclima"].append(row)

# rf (metamodelo dos três locais)
K = pd.read_csv(S / "estatisticas/D_kfold_resumo.csv"); K = K[K.modelo == "Random Forest"]
TC = pd.read_csv(S / "estatisticas/C_metamodelo_validacao_cruzada.csv")
T["rf"] = []
for resp, nome in [("perda_volume_k72", "Perda de volume (84 meses)"), ("recup_rel95_meses_ev1", "Recuperação foliar (meses)")]:
    for es, en in [("k-fold 7 × 10 repetições", "*k*-fold 7 × 10 repetições"), ("deixa um sítio de fora", "Um local fora"), ("deixa um material de fora", "Um material fora")]:
        r = K[(K.resposta == resp) & (K.esquema == es)].iloc[0]
        T["rf"].append([nome if es.startswith("k") else "", en, i(r.folds), f"{f(r.R2_media, 3)} ± {f(r.R2_dp, 3)}", f(r.r_media, 3), f"{f(r.RQEM_media)} ± {f(r.RQEM_dp)}"])
NOTAS["rf_n"] = [i(TC[TC.resposta == "perda_volume_k72"].n.iloc[0]), i(TC[TC.resposta == "recup_rel95_meses_ev1"].n.iloc[0])]

# bertulio (módulo original, d = 0,95 e 0,999)
import protocolo as p
T["bertulio"] = []
for m, rot, vs in [("C5", "C5 → urograndis", ["volume", "CAP", "altura"]), ("A1", "A1 → urocam", ["volume", "CAP"])]:
    o = p.observado(m); a95 = p.perdas(m, None, d=0.95); a999 = p.perdas(m, None, d=0.999)
    for k, var in enumerate(vs):
        T["bertulio"].append([rot if k == 0 else "", {"volume": "Volume", "CAP": "Circunferência/DAP", "altura": "Altura"}[var], f(o[var]), f(a95[var]), f(a999[var])])

# danos
DN = pd.read_csv(S / "danos_v2.csv")
dn = lambda c, s, m: DN[(DN.cenario == c) & (DN.sitio == s) & (DN.material == m)].perda_volume_84
cols = [("IND", "A1"), ("TB", "A1"), ("IND", "C5"), ("TB", "C5"), ("IMP", "C5")]
lin = [("Lagartas", "Desfolha 50%, 1 mês", "Lagarta desfolhadora"), ("Psilídeo-de-concha", "Desfolha 25%, 1 mês", "Psilídeo-de-concha"),
       ("Formigas-cortadeiras", "Desfolha 95%, 18 meses", "Formigas-cortadeiras"), ("Mancha foliar*", "Desfolha 20%/mês, 3 meses", "Mancha foliar"),
       ("Percevejo-bronzeado*", "r = 0,20, 4 meses", "Percevejo-bronzeado 20%"), ("Percevejo-bronzeado*", "r = 0,40, 4 meses", "Percevejo-bronzeado 40%"),
       ("Murchas, cancros, seca de ponteiros", "m = 0,05, 24 meses", "Mortalidade 5%"), ("Murchas, cancros, seca de ponteiros", "m = 0,15, 24 meses", "Mortalidade 15%"),
       ("Ferrugem", "r calibrado, −25% DAP aos 12 meses", "Ferrugem juvenil −25% DAP"), ("Ferrugem", "r calibrado, −35% DAP aos 12 meses", "Ferrugem juvenil −35% DAP")]
T["danos"] = [[a, b] + [f(dn(c, s, m).iloc[0]) if len(dn(c, s, m)) else "—" for s, m in cols] for a, b, c in lin]
fg = DN[DN.cenario.str.startswith("Ferrugem")]
NOTAS["ferrugem_r"] = [f(fg.r_calibrado.min(), 2), f(fg.r_calibrado.max(), 2)]

# calibração e teste independente
J = json.load(open(CB / "calibracao_d0999.json")); V = J["validacao_A1_urocam"]
OL = json.load(open(CB / "teste_oliveira2014.json"))["resultados"]["T1 100%"]
pm = J["preditiva_media_C5"]
T["calibracao"] = [["Urograndis (C5)", "Ajuste", "Volume", f(J["observado_C5"]["volume"]), f(J["original_C5"]["volume"]), f(pm["volume"])],
                   ["Urograndis (C5)", "Ajuste", "Circunferência", f(J["observado_C5"]["CAP"]), f(J["original_C5"]["CAP"]), f(pm["CAP"])],
                   ["Urograndis (C5)", "Ajuste", "Altura", f(J["observado_C5"]["altura"]), f(J["original_C5"]["altura"]), f(pm["altura"])]]
for var, nome in [("volume", "Volume"), ("CAP", "Circunferência")]:
    T["calibracao"].append(["Urocam (A1)", "Teste", nome, f(V["observado"][var]), f(V["original"][var]),
                            f"{f(V['calibrado_media'][var])} ({f(V['calibrado_q05'][var])} a {f(V['calibrado_q95'][var])})"])
fx = OL["calibrado_faixa90_mediana_anos"]
T["calibracao"].append(["E. grandis (C5), Oliveira et al. (2014)", "Teste independente", "Volume", f(OL["observado"]["volume_publicado"]),
                        f(OL["original"]["volume"][1]), f"{f(OL['calibrado']['volume'][1])} ({f(fx[0])} a {f(fx[1])})"])

# possibilidades
PS = json.load(open(S / "possibilidades/resumo_possibilidades.json")); O_, C_ = PS["original"], PS["calibrada"]; G_ = PS["ganho_por_tipo"]
T["possibilidades"] = [["Cenários com ganho de volume (%)", f(O_["frac_ganho"]), f(C_["frac_ganho"])],
                       ["Maior ganho de volume (%)", f(O_["ganho_max"]), f(C_["ganho_max"])],
                       ["Cenários com ganho: só desfolha (%)", f(G_["só desfolha | original"]["frac"]), f(G_["só desfolha | calibrada"]["frac"])],
                       ["Cenários com ganho: só perda de eficiência (%)", f(G_["só perda de eficiência | original"]["frac"]), f(G_["só perda de eficiência | calibrada"]["frac"])],
                       ["Cenários com ganho: só mortalidade (%)", f(G_["só mortalidade | original"]["frac"]), f(G_["só mortalidade | calibrada"]["frac"])],
                       ["Perda de volume: mediana (%)", f(O_["perda_mediana"]), f(C_["perda_mediana"])],
                       ["Perda de volume: máxima (%)", f(O_["perda_max"]), f(C_["perda_max"])],
                       ["Folhagem atinge 95% do controle até 84 meses (% dos cenários com desfolha)", f(O_["frac_folhas_recuperam"]), f(C_["frac_folhas_recuperam"])],
                       ["Meses até 95% da folhagem do controle (mediana)", i(O_["recup_folhas_mediana"]), i(C_["recup_folhas_mediana"])],
                       ["NPP após o 1º ano maior que a do controle (% dos cenários com desfolha)", f(O_["frac_npp_pos_maior"]), f(C_["frac_npp_pos_maior"])]]

# validação cruzada
VC = json.load(open(CB / "validacao_cruzada.json"))
T["validacaocruzada"] = []
for k, nome in [("deixa uma observação de fora (k = 5)", "Deixa uma observação de fora (k = 5)"), ("ajusta no C5, prevê o A1 (k = 2)", "Ajusta no urograndis, prevê o urocam (k = 2)"),
                ("ajusta no A1, prevê o C5 (k = 2)", "Ajusta no urocam, prevê o urograndis (k = 2)")]:
    r = VC[k]; T["validacaocruzada"].append([nome, i(r["n"]), f(r["RQEM_original"]), f(r["RQEM_calibrado"]), f(r["vies_original"]), f(r["vies_calibrado"]), f"{r['melhorou']} de {r['n']}"])

# biomas
BO = pd.read_csv(BB / "indicadores_original.csv"); BC = pd.read_csv(BB / "indicadores_calibrado.csv"); BU = pd.read_csv(BB / "incerteza_posterior_d50.csv")
bget = lambda D, s_, cal_, col="perda_volume_k72": D[(D.sitio == s_) & (D.material == "C5") & (D.nivel_FR == "F100") & (D.desfolha == 0.5) & (D.calendario == cal_)][col].iloc[0]
CR = pd.read_csv(BB / "clima_resumo_locais.csv", index_col=0)
from run_experimentos import rodar as _r0, linha as _l0
T["biomas"] = []
for s, nome in [("IND", "Cerrado (Indianópolis)"), ("IMP", "Cerrado (Imperatriz)"), ("TB", "Mata Atlântica (Telêmaco Borba)"),
                ("ALM", "Amazônia (Almeirim)"), ("ARA", "Caatinga (Araripina)"), ("ELD", "Pampa (Eldorado do Sul)")]:
    o = _r0(_l0(s, "C5", None, MATERIAIS["C5"]["FR_ref"], "F100", 0.0, "P1", "X", asw={"IND": 215, "TB": 214, "IMP": 210, "ALM": 219, "ARA": 194, "ELD": 145}[s]))
    k84 = (o.idade_meses - 84).abs().idxmin(); u = BU[(BU.sitio == s) & (BU.material == "C5") & (BU.calendario == "PA")].iloc[0]
    T["biomas"].append([nome, i(o.volume[k84] / 7), f(bget(BO, s, "P1")), f(bget(BC, s, "P1")), f(bget(BO, s, "PA")), f(bget(BC, s, "PA")),
                        f"{f(u.q05)} a {f(u.q95)}", i(bget(BO, s, "P1", "recup_rel95_meses_ev1")), i(bget(BC, s, "P1", "recup_rel95_meses_ev1"))])

json.dump(dict(tabelas=T, notas=NOTAS), open(Path(__file__).parent / "tabelas_dados.json", "w"), ensure_ascii=False, indent=1)
print("ok", {k: len(v) for k, v in T.items()})
