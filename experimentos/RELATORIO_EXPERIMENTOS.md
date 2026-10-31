# Experimento computacional — módulo de desfolha no 3-PG (r3PG)
**TCC II · Bernardo T. de Castro · execução de 30/10/2026**

> Todos os números deste relatório vêm dos arquivos em `saida/`. Não há réplicas: o delineamento é determinístico, e nenhuma diferença é chamada de "significativa".

## 0. O que foi executado
| Item | Situação |
|---|---|
| Modelo | r3PG v0.1.7 (3-PGpjs), port Python verificado + módulo de desfolha v1 |
| Verificação contra o r3PG original (R 4.3.3, compilado do código-fonte; 7/7 testes oficiais passam) | **260 controles da matriz idênticos**: diferença relativa máxima de 5×10⁻¹⁵ em 23.873 pares mês-variável |
| Tratamentos | **1.496** (1.344 da matriz E1–E6, 120 do E2 exploratório e 32 complementares) |
| Testes automatizados | 28 do módulo + 8 do pipeline, todos aprovados |
| Clima | NASA POWER diário 2015–2024 (API, com cabeçalho): Indianópolis, Telêmaco Borba, Imperatriz; Campo Verde 2006–2008 só para o confronto com a literatura |

## 1. Auditoria dos clones de Borges (2009) — confirmada no PDF
- **Identificação (Tabela 9, pp. 43–44):** C1 = 3334 Curvelo, C2 = 3336 Curvelo, C3 = 3334 Itacambira, C4 = 3336 Itacambira, C5 = modelo geral do Cerrado (dados de 3334/3336 Itacambira + 3336 Curvelo). Os valores conferem com as colunas do `3PGmix.Data.xls`.
- **Desempenho:**
  - **Tabela 8 (calibração):** C1 tem viés significativo em altura, stem e volume; C2 e C5 praticamente sem viés; C4 tem viés no DAP e o menor r² de volume (0,876).
  - **Validação:** só gráfica, com IC de 1% de inventário independente (Plantar S.A.). A altura é subestimada em Itacambira e no C5. C1 só tem dados até 4 anos.
- **Escolha (por documentação e desempenho, não por produtividade):** A1 principal, C5 comparativo, C2 e C4 adicionais. C1 e C3 complementares, só em Indianópolis. C1 teria o maior volume (453 m³/ha) e **não** foi escolhido por isso.
- **Diferenças estruturais entre as fontes:**
  - **Fertilidade:** no A1, fN0 = 1, então o FR só altera a partição para raízes. Nos clones de Borges, fN0 = 0,5 e fNn = 1, então fNutr = 0,5 + 0,5·FR e o FR também altera o GPP.
  - **Ponto de partida:** Borges inicializa aos 3 meses; Caldeira, aos 12.
- Tabela completa: `tabela_materiais.csv`. Parâmetros com origem: `clones.py`.

## 2. Os quatro níveis de solo — como foram representados
- **Água (ASWmax):** 25/50/75/100% de 190,6 mm (Indianópolis, 0–200 cm, 33 kPa, valor da sua planilha). Como contexto documentado, Borges (Tab. 3A) mede 198–300 mm até 2 m, a 10 kPa. ASW0 = ASWmax, porque a simulação começa em janeiro, na estação chuvosa. O teste A1 da auditoria mostra que isso quase não importa.
- **Capacidade produtiva → FR: conversão parcialmente impossível, e isso precisa ser dito.**
  1. Não há base empírica para transformar "25% de capacidade produtiva" em FR.
  2. No A1 (Caldeira), o FR **não altera a fotossíntese**, só a partição. Com essa parametrização, o 3-PG não consegue representar capacidade produtiva via FR.
  3. Para ter níveis admissíveis, usei o limite inferior da função FR(CTCe) do próprio Caldeira (§2.10.4): FR = 0,5483 com CTCe = 0. Daí: F25 = 0,548, F100 = FR original (0,8 no A1; 0,9 em Borges), e F50/F75 equidistantes entre os dois. **São níveis ordinais, e não 25–100% de produtividade.**
  4. O E2 exploratório usa FR de 0,2 a 1,0; abaixo de 0,548 fica fora da faixa da função de Caldeira.
- Mudar αCx, fN0 ou m0 para representar capacidade produtiva seria calibração sem dados, e não foi feito.

## 3. Delineamento e convenção temporal (única)
- **Datas:** plantio hipotético em jan/2015. O A1 começa aos 12 meses (jan/2016); os clones de Borges, aos 3 meses (abr/2015). A simulação vai até jan/2023, com 96 meses de idade.
- **"Mês k":** mês k da simulação de referência, ou seja, idade = 12 + k meses.
- **Pulso único:** k = 12 (jan/2017, estação chuvosa). **Recorrente:** k = 12 e 48 (jan/2020).
- **Aplicação:** no **início** do passo mensal, antes da interceptação de luz, aplicando Wf × (1 − d). A remoção é registrada em `biom_defol`.
- **Fatores:**
  - **E1:** água isolada (FR de referência);
  - **E2:** FR isolado (níveis admissíveis + exploratório);
  - **E3:** água × FR (4 × 4);
  - **E4:** solo combinado S25–S100 × desfolha (0, 25, 50, 95%);
  - **E5:** P1 × P2;
  - **E6:** 3 climas.
- **IDs:** `SITIO_MATERIAL_Wxx_Fxx_Dxx_CAL` (`matriz_tratamentos.csv`).
- Para além de 80 meses de idade (k > 68), o A1 está em extrapolação em relação a Caldeira. A rotação de 7 anos corresponde a k = 72 (84 meses de idade).

## 4. Resultados principais — Indianópolis, A1, solo de referência (W100/F100)

Perda relativa (%) em relação ao controle. P1 = pulso único; P2 = meses 12 e 48.

| Idade (meses) | Variável | 25% P1 | 25% P2 | 50% P1 | 50% P2 | 95% P1 | 95% P2 |
|---|---|---|---|---|---|---|---|
| 24 (evento) | Wf / LAI | 22,0 | 22,0 | 45,5 | 45,5 | 93,9 | 93,9 |
| 36 | Wf | 7,4 | 7,4 | 13,2 | 13,2 | 25,7 | 25,7 |
| 36 | volume | 3,5 | 3,5 | 6,4 | 6,4 | 23,5 | 23,5 |
| 72 | volume | 2,0 | 2,6 | 3,6 | 5,0 | 11,4 | 19,4 |
| **84 (rotação)** | **volume** | **1,7** | **2,3** | **3,1** | **4,5** | **9,7** | **17,3** |
| 84 | DAP | 0,6 | 0,8 | 1,0 | 1,5 | 3,3 | 6,1 |
| 84 | biomassa total | 1,7 | 2,2 | 3,0 | 4,5 | 9,3 | 17,1 |
| 84 | NPP acumulada após o evento | 1,7 | 2,3 | 3,1 | 4,6 | 9,8 | 17,6 |

- **No evento:** com 50% de desfolha, Wf cai de 3,26 para 1,63 t/ha, o LAI de 2,92 para 1,46 e a APAR do mês de 470 para 316 MJ/m².
- **Recuperação:**
  - **absoluta** (Wf volta ao valor de antes do evento): 1, 3 e 14 meses para 25, 50 e 95%;
  - **relativa** (Wf ≥ 95% do controle): 15, 23 e 25 meses.

  Voltar ao valor anterior **não** significa voltar à trajetória do controle. A perda de lenho persiste até a rotação.
- **Água:** o tratamento fica com o solo **mais úmido** (ASW média pós-evento entre −0,2% e −25% em relação ao controle). O NPP do tratamento supera o do controle em 20 a 31 meses depois do evento (ver a seção 6).
- **Altura:** não é calculável para o A1, porque Caldeira não publica alometria de altura. No C5 (Borges), a perda aos 84 meses é de 0,2 / 0,7 / 3,8% para 25 / 50 / 95%.
- **Mortalidade:** não há mortalidade induzida. A desfolha nunca reduz o número de árvores abaixo do controle; o autodesbaste ocorreu em 36 de 1.496 tratamentos.

## 5. Respostas às perguntas
1. **Qual variável edáfica mais influencia a perda após a desfolha?** Depende da parametrização.
   - No A1, a água responde por 70% (IND) e 99,8% (TB) da variação da perda de volume. O FR quase não atua, pelo canal descrito na seção 2.
   - Em Borges, o FR domina em IND e IMP (88–94%), e água e FR se dividem em TB.
   - **A amplitude é pequena:** com 50% de desfolha, a perda de volume varia no máximo 0,4 a 2,3 pontos percentuais entre os 16 solos. O fator que mais pesa é o **material genético** (28–49% da soma de quadrados).
2. **Menos água muda a velocidade de recuperação?**
   - **A1:** não; 23–25 meses em todos os níveis de água.
   - **Borges:** sim; 28 → 34–35 meses (50%) e 38 → 46 meses (95%) de W100 para W25.
3. **A fertilidade altera a capacidade de compensação?**
   - **Borges:** sim. A perda de volume com 50% de desfolha cai de 4,8% (FR 0,2) para 1,5% (FR 1,0).
   - **A1:** o efeito é **inverso e pequeno** (2,5% → 3,2%). FR maior manda menos carbono para as raízes, o lenho cresce mais no controle, e a perda relativa fica um pouco maior.
4. **A interação água × FR é relevante?** Não. Fica em 0,2–2,6% da soma de quadrados, com exceção de 11% no C2 em TB.
5. **Qual clone tem menor perda relativa em cada clima (50%, P1, média dos 16 solos)?**
   - IND: C4 2,3% ≈ C5 2,3% < A1 3,1% ≈ C2 3,1%.
   - TB: C4 1,7% < C5 1,9% < C2 2,5% < A1 3,0%.
   - IMP: C5 3,1% ≈ C4 3,2% < C2 3,9% (A1 = diagnóstico, 6,2%).

   **Ressalva decisiva (seção 6):** a menor perda dos clones de Borges vem do LAI simulado de 8,5–11, um dossel saturado em que tirar folhas reduz pouco a luz absorvida. Isso não é tolerância genética representada pelo modelo.
6. **O pulso recorrente perde mais?** Em 95% dos 576 pares, sim, na NPP acumulada; a perda de volume mediana dobra (razão P2/P1 = 2,06). **Contra a hipótese:** em 28 pares, P2 perde *menos* que P1. São todos com A1 e quase todos com 25% de desfolha (TB em todos os níveis de água; IND em W25).
7. **Há respostas biologicamente questionáveis?** Sim — seção 6.
8. **Que parâmetros dominam a incerteza?** Pelo método de Morris (±10%, 25 trajetórias, A1/IND):
   - **na perda por desfolha:** αCx, k, Y, γF1, SLA1, nS e Topt;
   - **no volume do controle:** Y, αCx, Topt e Tmax.

   Topt e Tmax têm σ maior que μ*, o que indica forte não linearidade, porque a Tmédia de Indianópolis fica perto do Topt/Tmax do A1. A incerteza de transferência entre parametrizações (279–453 m³/ha no controle, conforme o clone) é **muito maior** que o efeito do solo.

## 6. Auditoria adversarial — resultados contrários com o mesmo destaque
| Teste | Resultado | Implicação |
|---|---|---|
| **LAI improvável** | LAI máximo de 8,5–10,8 nos clones C2, C4 e C5 (IND/IMP); 3,2–5,3 no A1 | **Implausível para eucalipto.** Explica as perdas menores de Borges: dossel saturado, APAR cai só 15% com 50% de desfolha (A1: 33%). Comparar clones fica comprometido. |
| **Compensação via água** | Menos folha → menos transpiração → solo mais úmido → fSW maior → NPP do tratamento acima do controle por meses | Quentin et al. (2011) observaram **aumento** da transpiração nas folhas remanescentes, o que o modelo não tem. A economia de água deve estar **superestimada**, e as perdas, **subestimadas** em períodos secos. |
| **Recuperação** | Recuperação relativa mediana de 32 meses (21–37) com 50% de desfolha | **Mais lenta** que o observado em *E. globulus* jovem (Barry et al. 2012: sem diferença aos 18 meses). Não há reservas, nem aumento de fotossíntese, nem realocação para as folhas. |
| **Desfolha total** | d = 0,95 → 9,7%; 0,99 → 19,7%; 0,999 → 31,1%; d = 1 é bloqueado | Sem reservas, Wf = 0 é um estado sem volta. **Desfolhas de 100% (Bertulio, Matrangolo) não são simuláveis exatamente**, e o resultado perto de 100% depende da fração residual arbitrada. |
| **Época do pulso** | jan 3,1% · abr 1,7% · jul 3,3% · out 3,9% · jan/2018 3,3% | A época muda a perda em até 2,2 pontos. O mês 12 (janeiro) é uma escolha, não um caso geral. |
| **Início × fim do mês** | 3,1% contra 2,4% | Convenção única mantida (início do mês). |
| **ASWmax × ASW0** | ASW0 = 50% muda a perda em 0,04 ponto | Não há confusão relevante; o início chuvoso reabastece o perfil. |
| **Saturação dos modificadores** | fSW < 0,5 em 43 de 84 meses; fVPD médio 0,62; fT médio 0,97 | A água limita bastante na seca, mas o efeito sobre a *perda relativa* continua pequeno. |
| **Canal do FR** | A1: FR mínimo reduz o volume do controle em 3%; C5: em 27% | O "solo" não significa a mesma coisa nas duas fontes. |
| **Balanço da biomassa removida** | 1.812 eventos; erro máximo ≤ 6×10⁻¹⁵ | Fecha. |
| **Mortalidade** | Nenhuma morte induzida | Resultados de 95% não dizem nada sobre risco de morte. |
| **Extrapolação térmica** | IMP-A1: fT = 0 em 31 de 84 meses; volume 227 contra 345 m³/ha em IND | Combinação marcada como diagnóstico, fora da análise principal. |
| **Geada (TB)** | 8 dias com Tmin ≤ 0 °C; kF = 0 | Não se conclui resistência ao frio; o dano por geada não está representado. |

## 7. Confronto com a literatura (só dados secundários)
- **Evidência direta da espécie-alvo (*E. urophylla* puro): não existe** no corpus.
- **Híbridos relacionados — Bertulio et al. (2008):**
  - **Protocolo reproduzido:** Campo Verde-MT, 3 × 3 m, desfolha aos 14 e 23 meses, avaliação aos 26 meses. Como 100% não é simulável, usei d = 0,95 e 0,999 como limites. Solo e clone exatos são desconhecidos.
  - **C5 contra urograndis** (perda ajustada pela linha de base):
    - volume observado 52,9%; simulado 36,8% (d = 0,95) a 64,8% (d = 0,999);
    - CAP observado 24,2%; simulado 13,7% a 28,5%;
    - altura observada 19,1%; simulada 17,1% a 34,7%.
  - **Leitura:** o valor observado fica **dentro do intervalo** entre d = 0,95 e 0,999, mas o intervalo é largo e é a fração residual arbitrada que define o resultado. Erros com d = 0,95: viés de −9,5 pontos e MAE de 9,5 pontos (n = 3).
  - **A1 contra urocam:** erros de 1,6 e 3,6 pontos com d = 0,95, mas é transferência fraca (*E. urophylla* puro contra *urophylla × camaldulensis*), com n = 2.
  - **Isto não é validação.** O "acerto" (100 − |erro|) é uma métrica heurística própria, e os pares não são independentes (volume ≈ CAP² × H).
- **Matrangolo et al. (2010, *E. grandis*):** **não comparável.** A primeira desfolha foi aos 56 dias, antes da idade inicial de qualquer parametrização disponível (3 e 12 meses).
- **Outras espécies (*E. globulus*: Pinkard 2006/2007, Barry 2012, Eyles 2009, Quentin 2010–2012):** só confronto qualitativo. Esses estudos mostram compensação (fotossíntese, realocação, transpiração), que o módulo **não** tem. A expectativa é que o módulo superestime perdas moderadas e subestime o efeito de seca combinada.
- **Resultados apenas simulados:** Pinkard et al. (2011) também incorporaram desfolha num modelo de produção. É precedente metodológico, não validação.

## 8. Parecer — o que já é validável
| Nível | Situação |
|---|---|
| **Verificação de código** | **Concluída.** Equivalência com o r3PG original, conservação de massa, calendário, ausência de dupla aplicação, 0% = controle, não negatividade, testes de mutação. |
| **Plausibilidade biológica** | **Parcial.** Perdas crescem com intensidade e frequência e há recuperação foliar. Mas: LAI implausível em Borges, compensação hídrica sem contrapartida fisiológica, ausência de reservas e de mortalidade. |
| **Validação externa secundária** | **Não alcançada.** Um único estudo com híbridos e 100% de desfolha, que fica fora do domínio do módulo; o resultado depende da fração residual. |
| **Validação local** | **Inexistente.** Não há inventário de Indianópolis. É uma proposta futura, condicionada ao mestrado na UNIR, que ainda não está autorizado nem financiado. |

**O que dá para defender no TCC II:** o módulo está verificado e se comporta de forma coerente com a estrutura do 3-PG. No caso principal, a perda de volume na rotação é de 1,7 a 17,3% conforme intensidade e frequência. A perda é pouco sensível ao solo e muito sensível à parametrização do material e à intensidade/frequência. Os mecanismos ausentes (reservas, compensação fisiológica, mortalidade) são as principais lacunas para a próxima versão.

## 9. Próximos passos sugeridos
1. Restringir a comparação entre clones aos casos com LAI plausível, ou documentar o LAI de Borges como limitação central.
2. Testar, como análise de sensibilidade rotulada, um mecanismo simples de transpiração compensatória.
3. Repetir o pulso único nas outras épocas (abril, julho, outubro) para a parte de "épocas" da IC.
4. Para a IC: a matriz já cobre os 3 locais, os 4 materiais, os 4 solos e as intensidades. Faltam apenas as frequências "anuais" (um pulso por ano), que podem ser adicionadas ao `EVENTOS` sem mudar o código.

## Arquivos (`experimentos/`)
- **Código:**
  - `run_experimentos.py` (matriz e execução)
  - `indicadores.py`
  - `analise.py` (sensibilidade e figuras)
  - `adversarial_e_literatura.py`
  - `clones.py`, `clima.py`
  - `r_check/rodar_controles_r3pg.R`
- **Dados (`saida/`):**
  - `matriz_tratamentos.csv`
  - `mensal.csv.gz` (137.330 linhas mensais)
  - `indicadores_por_tratamento.csv`
  - `perdas_por_idade_longo.csv`
  - `config_execucao.json`
- **Sensibilidade:**
  - `sensibilidade_decomposicao_fatorial.csv`
  - `sensibilidade_morris_A1_IND.csv`
  - `Q1_Q4_*.csv`, `Q2_*.csv`, `Q3_*.csv`, `Q5_*.csv`, `Q6_*.csv`
- **Auditoria e literatura:**
  - `auditoria_adversarial.csv`
  - `confronto_literatura_bertulio.csv`
  - `confronto_literatura_metricas.csv`
- **Figuras (`saida/figuras/`):** F1 (trajetórias), F2 (matriz água × FR), F3 (sítios × materiais), F4 (recuperação × água), F5 (Morris), F6 (decomposição)
- **Testes:**
  - `testes/test_experimentos.py` (8)
  - `../modelo/testes/` (28)
  - `r_check/resultado_crosscheck.csv`
