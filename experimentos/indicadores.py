#!/usr/bin/env python3
"""Indicadores tratamento × controle (mesmo sítio, material, água, FR; só a desfolha muda).
Critérios operacionais (definidos ANTES do cálculo):
  * perda relativa (%) = 100·(1 − trat/ctrl), no fim do mês k da simulação de referência;
  * recuperação ABSOLUTA: nº de meses após o evento até Wf_trat >= Wf imediatamente antes do evento;
  * recuperação RELATIVA: nº de meses após o evento até Wf_trat/Wf_ctrl >= 0,95;
    (para P2, a 1ª recuperação é censurada se não ocorrer antes do 2º evento);
    0 = recupera no próprio mês do evento; NaN = não recupera até o fim (censurado);
  * perda acumulada de NPP: Σ(NPP_ctrl − NPP_trat) do mês do 1º evento ao fim (t/ha) e % do Σ NPP_ctrl;
  * disponibilidade hídrica: 100·(1 − média ASW_trat / média ASW_ctrl) no mesmo intervalo
    (valor NEGATIVO = solo mais úmido no tratamento).
"""
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
S = AQUI / "saida"
KS = [12, 24, 48, 60, 72, 84]
VARS = {"biom_foliage": "Wf", "biom_stem": "Ws", "biom_total": "Wtotal", "lai": "LAI", "dbh": "DAP",
        "height": "altura", "volume": "volume"}


def carregar():
    M = pd.read_csv(S / "matriz_tratamentos.csv")
    cols = ["id", "date", "mes_ref", "idade_meses", "biom_foliage", "biom_stem", "biom_root", "biom_total", "lai",
            "dbh", "height", "volume", "npp_f", "gpp", "apar", "asw", "f_sw", "stems_n", "biom_defol",
            "wf_pre_defol", "lai_pos_defol", "biom_incr_foliage", "biom_incr_stem", "biom_incr_root"]
    D = pd.read_csv(S / "mensal.csv.gz", usecols=cols)
    D["mes_ref"] = D.mes_ref.round().astype(int)
    return M, D


def chave(M):
    return M.sitio + "|" + M.material + "|" + M.nivel_agua.astype(str) + "|" + M.nivel_FR + "|" + M.experimento


def calcular(M, D):
    M = M.copy(); M["grupo"] = chave(M)
    ctrl_id = M[M.desfolha == 0].set_index("grupo").id
    G = {i: g.set_index("mes_ref") for i, g in D.groupby("id")}
    linhas = []
    for r in M[M.desfolha > 0].itertuples():
        t, c = G[r.id], G[ctrl_id[r.grupo]]
        ev = [int(round((pd.Timestamp(e + "-01") - pd.Timestamp("2016-01-01")).days / 30.4375)) for e in r.eventos.split(";")]
        e1 = ev[0]; fim2 = ev[1] if len(ev) > 1 else None; fim3 = ev[2] if len(ev) > 2 else None
        out = dict(id=r.id, sitio=r.sitio, material=r.material, nivel_agua=r.nivel_agua, asw_max=r.asw_max,
                   n_eventos=len(ev), mes_evento=int(r.eventos.split(";")[0][5:7]), nivel_FR=r.nivel_FR, FR=r.FR,
                   desfolha=r.desfolha, calendario=r.calendario, experimento=r.experimento,
                   apto_analise_principal=r.apto_analise_principal)
        for k in KS:
            for v, rot in VARS.items():
                a, b = t.at[k, v], c.at[k, v]
                out[f"perda_{rot}_k{k}"] = 100 * (1 - a / b) if b > 0 else np.nan
        # evento 1: registro
        out["Wf_pre_ev1"] = t.at[e1, "wf_pre_defol"]; out["Wf_pos_ev1"] = t.at[e1, "wf_pre_defol"] - t.at[e1, "biom_defol"]
        out["biomassa_removida_total"] = t.biom_defol.sum()
        out["LAI_pre_ev1"] = t.at[e1 - 1, "lai"]; out["LAI_pos_ev1"] = t.at[e1, "lai_pos_defol"]
        out["APAR_ev1_trat"] = t.at[e1, "apar"]; out["APAR_ev1_ctrl"] = c.at[e1, "apar"]
        # recuperação
        janela = range(e1, (fim2 if fim2 else max(t.index) + 1))
        wf_pre = t.at[e1, "wf_pre_defol"]
        ab = next((m - e1 for m in janela if t.at[m, "biom_foliage"] >= wf_pre), np.nan)
        rel = next((m - e1 for m in janela if t.at[m, "biom_foliage"] / c.at[m, "biom_foliage"] >= 0.95), np.nan)
        out["recup_abs_meses_ev1"] = ab; out["recup_rel95_meses_ev1"] = rel
        if fim2:
            wf2 = t.at[fim2, "wf_pre_defol"]
            j2 = range(fim2, fim3 if fim3 else max(t.index) + 1)
            out["recup_abs_meses_ev2"] = next((m - fim2 for m in j2 if t.at[m, "biom_foliage"] >= wf2), np.nan)
            out["recup_rel95_meses_ev2"] = next((m - fim2 for m in j2
                                                 if t.at[m, "biom_foliage"] / c.at[m, "biom_foliage"] >= 0.95), np.nan)
        post = slice(e1, max(t.index))
        dn = (c.loc[post, "npp_f"] - t.loc[post, "npp_f"])
        out["perda_NPP_acum_tha"] = dn.sum(); out["perda_NPP_acum_pct"] = 100 * dn.sum() / c.loc[post, "npp_f"].sum()
        out["meses_NPP_trat_maior_ctrl"] = int((dn < -1e-9).sum())
        out["reducao_ASW_media_pct"] = 100 * (1 - t.loc[post, "asw"].mean() / c.loc[post, "asw"].mean())
        out["fSW_medio_trat"] = t.loc[post, "f_sw"].mean(); out["fSW_medio_ctrl"] = c.loc[post, "f_sw"].mean()
        out["arvores_final_trat"] = t.at[84, "stems_n"]; out["arvores_final_ctrl"] = c.at[84, "stems_n"]
        out["volume_k72_ctrl"] = c.at[72, "volume"]; out["volume_k72_trat"] = t.at[72, "volume"]
        out["LAI_max_ctrl"] = c.lai.max()
        linhas.append(out)
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    M, D = carregar()
    R = calcular(M, D)
    R.to_csv(S / "indicadores_por_tratamento.csv", index=False)
    # tabela longa de perdas por idade
    long = []
    for k in KS:
        for rot in VARS.values():
            sub = R[["id", "sitio", "material", "nivel_agua", "nivel_FR", "desfolha", "calendario", "experimento",
                     "apto_analise_principal", f"perda_{rot}_k{k}"]].rename(columns={f"perda_{rot}_k{k}": "perda_pct"})
            sub.insert(1, "variavel", rot); sub.insert(2, "mes_ref", k); sub.insert(3, "idade_meses", 12 + k)
            long.append(sub)
    pd.concat(long).to_csv(S / "perdas_por_idade_longo.csv", index=False)
    print(len(R), "tratamentos com desfolha avaliados")
