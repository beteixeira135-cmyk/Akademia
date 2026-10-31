"""Gera as matrizes da Missão 07: afirmações (etapa 1), mecanismos (etapa 5), concordância (etapa 7) e correções.
Valores numéricos vêm dos arquivos de saída citados; a classificação é julgamento documentado do auditor."""
import json, csv
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[1]; O = Path(__file__).parent
J = json.load(open(R / "calibracao/saida/calibracao_d0999.json")); A = json.load(open(R / "calibracao/saida/auditoria_calibracao.json"))
T = json.load(open(R / "calibracao/saida/testes_adicionais.json"))


def w(nome, cab, linhas):
    with open(O / nome, "w", newline="", encoding="utf8") as f:
        x = csv.writer(f); x.writerow(cab); x.writerows(linhas)


# ---------------- métricas Bertulio
def met(obs, sim):
    e = np.array(sim) - np.array(obs); return round(float(np.abs(e).mean()), 1), round(float(np.sqrt((e ** 2).mean())), 1)
vs = ["volume", "CAP", "altura"]
c5o = met([J["observado_C5"][v] for v in vs], [J["original_C5"][v] for v in vs])
c5c = met([J["observado_C5"][v] for v in vs], [J["preditiva_media_C5"][v] for v in vs])
V = J["validacao_A1_urocam"]
a1o = met([V["observado"][v] for v in ["volume", "CAP"]], [V["original"][v] for v in ["volume", "CAP"]])
a1c = met([V["observado"][v] for v in ["volume", "CAP"]], [V["calibrado_media"][v] for v in ["volume", "CAP"]])
mm = T["matrangolo_metricas"]
q11 = {r["versao"]: r["razao_transpiracao_7meses"] for r in T["quentin2011_transpiracao_A1"]}

# ---------------- matriz de concordância (etapa 7)
CONC = [
 ["Perda de volume (desfolha total ×2, 14–26 meses)", "Bertulio et al. (2008), urograndis", "52,9% (ajustada pela linha de base)",
  f"64,8% (MAE {c5o[0]}; RQEM {c5o[1]} p.p. nas 3 variáveis)", f"50,4% (MAE {c5c[0]}; RQEM {c5c[1]} p.p.; dentro da amostra)",
  "Boa após o ajuste", "Altura: o calibrado ainda superestima (24,9 × 19,1%)", "É o próprio dado do ajuste: não mede previsão",
  "Mostra só que o modelo consegue reproduzir o dado com U e a plausíveis"],
 ["Perda de volume e CAP (mesmo protocolo, outro clone)", "Bertulio et al. (2008), urocam", "59,0% e 22,9%",
  f"79,3% e 40,7% (MAE {a1o[0]}; RQEM {a1o[1]} p.p.)", f"64,8% e 29,7% (MAE {a1c[0]}; RQEM {a1c[1]} p.p.)",
  "Melhorou; observado dentro do IC 90%", "A melhora vem sobretudo de a (só U: 79,1%; só a: 70,1%; os dois: 61,7%)",
  "Mesmo experimento, local, datas e protocolo; A1 (E. urophylla) ≠ urocam", "Teste fora do ajuste, mas não validação independente"],
 ["Perda de volume após desfolha total precoce (1–3 vezes, até 9 meses)", "Matrangolo et al. (2010), E. grandis, Viçosa",
  "37,9; 61,9; 61,6; 79,7% aos 92 meses", f"2,6 a 12,7% (viés {mm['vies_original']:.1f}; RQEM {mm['rmse_original']:.1f} p.p.)",
  f"1,1 a 8,5% (viés {mm['vies_calibrado']:.1f}; RQEM {mm['rmse_calibrado']:.1f} p.p.)", "Não",
  "As duas versões subestimam em cerca de 10 vezes; a calibrada piora", "C5 ≠ E. grandis seminal; eventos deslocados +2,2 meses; clima de 2015–2024; 3 × 3 m × 3 × 2 m",
  "Contraria a ideia de compensação após desfolha total em plantas muito jovens; limita o domínio de uso do módulo"],
 ["Recuperação foliar e crescimento após desfolha parcial", "Barry et al. (2012), E. globulus", "Altura, DAP e área foliar sem diferença aos 18 meses; volume do tronco maior nas desfolhadas",
  "IAF 8,3% abaixo do controle; DAP e altura com pequenos ganhos", "IAF 1,4% abaixo (IC 90%: −2,4 a 6,7%); pequenos ganhos",
  "Qualitativa (melhor na calibrada)", "O modelo não reproduz o aumento significativo do volume do tronco", "Outra espécie, outro clima, plantas de 3–18 meses",
  "Apoia a compensação de alocação/folhas em desfolha parcial"],
 ["Compensação em 5 meses", "Eyles, Pinkard e Mohammed (2009)", "Compensação de 40% em 5 meses, exceto com pouca água e pouco N",
  "IAF 8,1% abaixo aos 13 meses", "IAF 1,8% abaixo", "Qualitativa (melhor na calibrada)",
  "O módulo não suprime a compensação quando água e N faltam juntos", "Outra espécie; o C5 tem o FR fixo de referência", "Limitação para M8"],
 ["Resposta da fotossíntese das folhas remanescentes", "Quentin et al. (2012); Pinkard et al. (1998 apud QUENTIN et al., 2011); Pinkard et al. (2007)",
  "Asat cerca de +30%, transitório (pico em cerca de 22 dias), só irrigado; até +35% em E. nitens", "Sem aumento (U = 1)",
  f"U = {J['U']['q50']:.2f} (IC 90%: {J['U']['q05']:.2f}–{J['U']['q95']:.2f}), modulado por f_SW, ativo enquanto W_F < W_F,ref (2 meses após 60%)",
  "Ordem de grandeza compatível", "Medem Amax/Asat, não a eficiência quântica do dossel; o posterior de U depende do limite do prior (mediana 1,21 com limite 1,6)",
  "Folha × dossel; outra espécie", "U é fracamente identificado; o efeito existe, mas a magnitude não está restrita pelos dados brasileiros"],
 ["Transpiração após 45% de desfolha", "Quentin et al. (2011)", "Transpiração por área de alburno sem diferença em 215 dias",
  f"Razão tratamento/controle {q11['original']:.3f} (A1, 7 meses)", f"{q11['calibrado γ=0,5']:.3f} (γ = 0,5); {q11['calibrado γ=1']:.3f} (γ = 1)",
  "Calibrada com γ próximo de 1 concorda", "O original reduz a transpiração em 21%: superestima a economia de água", "Outra espécie; o C5 com IAF saturado não responde",
  "Apoia trocar γ = 0,5 por um prior informado próximo de 1 numa próxima versão"],
 ["Desfolha recorrente amplia a perda", "Pinkard et al. (2006); Matrangolo et al. (2010)", "Desfolha tripla: −15% em diâmetro e −26% em altura (E. globulus); 3 × total: −79,7% em volume (E. grandis)",
  "Pulsos anuais: até 58–68% (A1, 95%)", "Perdas cerca de 3 vezes menores com pulsos anuais; IC inclui sobrecompensação", "Direção concorda; magnitude incerta",
  "Com compensação calibrada, a perda recorrente fica bem menor que a de Matrangolo", "Protocolos e idades diferentes", "A conclusão de 'um terço' depende de a, pouco identificado"],
 ["Alocação de biomassa após a desfolha", "Eyles, Pinkard e Mohammed (2009); Barry et al. (2012)", "Mais alocação a folhas e galhos; menos a raízes grossas",
  "Partição fixa (alométrica)", "a = 0,55 (IC 90%: 0,05–0,975)", "Direção concorda", "a é quase o prior: dados insuficientes", "—", "Declarar baixa identificabilidade"],
]
w("matriz_concordancia.csv", ["Mecanismo/variável", "Referência", "Observação publicada", "3-PG original", "Módulo calibrado", "Concordância",
                              "Divergência", "Limite de comparação", "Implicação"], CONC)

# ---------------- mecanismos M1–M8 (etapa 5)
MEC = [
 ["M1 Remoção de folhas", "W_F·(1−d) no início do mês; IAF e APAR recalculados; fluxo próprio de biomassa removida",
  "Conservação de massa verificada (resíduo ≤ 5e-15 t/ha; 49 testes); queda de APAR menor que d pela lei de Beer", "Sustentado (computacional)",
  "Desfolha artificial ≠ por insetos (Quentin et al., 2010); padrão na copa (superior × inferior) não representado (Pinkard et al., 2006)", "Declarar limitação"],
 ["M2 Fotossíntese (U)", "α·[1+(U−1)·f_SW] enquanto W_F < W_F,ref", "Aumento de Amax/Asat de até cerca de 30–35% (Quentin 2012; Pinkard 1998 apud Quentin 2011); transitório",
  "Parcialmente sustentado", "Amax ≠ eficiência quântica; duração no modelo ≠ transitória; posterior sensível ao prior", "Corrigir o texto (4.10) e as limitações"],
 ["M3 Condutância (γ)", "gC·min[(gC_ref/gC)^γ; 1/(1−0,45)]", "Homeostase da transpiração com 45% (Quentin 2011): γ próximo de 1 no A1",
  "Sustentado na direção; não identificável com Bertulio", "Inativo quando o IAF > LAIgcx (materiais de Borges)", "Declarar; sugerir prior informado"],
 ["M4 Alocação (a)", "η_F' = η_F + a·δ·(η_S+η_R)", "Mais alocação a folhas/galhos (Eyles 2009; Barry 2012)", "Parcialmente sustentado",
  "a pouco identificado; não depende de N nem de água (Eyles: falha com pouca água e pouco N)", "Declarar"],
 ["M5 Recuperação", "Emergente de M1–M4 e das equações do 3-PG", "Recuperação em meses (Eyles: 5 meses; Barry: sem diferença aos 18 meses)",
  "Calibrado mais coerente (2–14 meses) que o original (4–35)", "Matrangolo: perdas persistentes após desfolha total precoce não reproduzidas", "Discutir evidência contrária"],
 ["M6 Reservas (carboidratos não estruturais)", "Ausente", "Mobilização de reservas (Eyles 2009); proposta de compartimento de reservas (Pinkard 2011)",
  "Omissão relevante", "Desfolha total irrecuperável; respostas precoces e transitórias mal representadas", "Manter na limitação (a); prioridade para pesquisa futura"],
 ["M7 Mortalidade", "Cenário N·(1−m), sem relação causal com o dano", "Bertulio: mortalidade nula; Matrangolo: 6,9–8,8% × 8,0% na testemunha; Santos et al. (2001): até 15%",
  "Cenário declarado", "Sem relação dose–resposta publicada para os locais", "Manter como cenário"],
 ["M8 Solo e clima", "Via f_SW, f_VPD, f_T, FR e balanço hídrico do 3-PG", "Interação da compensação com água e N (Eyles 2009; Quentin 2012; Pinkard 2006/2007)",
  "Parcialmente representado (U modulado por f_SW)", "Nutrição não modula a compensação; no A1 o FR não afeta a fotossíntese", "Declarar limitação"],
]
w("matriz_mecanismos.csv", ["Mecanismo", "Implementação", "Evidência publicada", "Situação", "Lacuna", "Ação"], MEC)
print("ok", c5o, c5c, a1o, a1c)
