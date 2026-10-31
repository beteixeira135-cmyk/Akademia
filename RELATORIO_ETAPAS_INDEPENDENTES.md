# TCC II — Relatório das etapas independentes (30/10/2026)

Projeto: módulo de desfolha para o 3-PG — *Eucalyptus urophylla*, Indianópolis (MG).
Situação: **verificação de código e de dados secundários concluída; nenhuma simulação de Indianópolis foi executada** (faltam parâmetros e condições iniciais — seção 5).

---

## 1. Auditoria da metodologia da revisão recebida (`Revisao_Desfolha_Clima_3PG_Parcial.zip`)

| Aspecto | Situação encontrada | Avaliação |
|---|---|---|
| Natureza | O próprio LEIA_ME declara "revisão sistematizada preliminar", sem PRISMA nem dupla triagem | Correto declarar. **Não pode ser chamada de revisão sistemática no TCC.** |
| Estratégia de busca | Não documentada (bases, termos, datas, critérios de inclusão/exclusão ausentes) | Não reproduzível. Precisa de um protocolo mínimo (seção 1.1). |
| Leitura | 6 dos 7 estudos foram lidos só pelo resumo | Insuficiente para extração. **Corrigido agora:** os 9 estudos de desfolha foram conferidos no PDF completo. |
| Extração numérica | Apenas Bertulio (2008): 12 pares | As 24 médias **conferem com as Tabelas 1–2 do artigo** (conferência visual nas imagens das páginas). |
| Interpretação de Bertulio | O pacote já alertava que a Tabela 1 poderia ser linha de base | **Confirmado no texto do Material e Métodos:** "idade inicial de 14 meses"; coletas de 12/4/2007 a 12/3/2008; 1ª desfolha em abril/2007. A Tabela 1 (14 meses) é o início do experimento. |
| Desequilíbrio inicial | — | Aos 14 meses as letras "a"/"b" indicam diferença significativa (teste F, 1%) entre desfolha e testemunha **já no início**, nos dois clones. Isso compromete a perda bruta aos 26 meses. |
| Inconsistências internas do artigo | — | (i) Métodos citam Tukey a 5%; o rodapé das tabelas cita teste F a 1%. (ii) 14 meses + 11 meses de coleta = 25, mas a Tabela 2 diz 26 meses. (iii) O resumo diz volume da testemunha 191,14% maior (urocam); as médias da Tabela 2 dão 191,4% (provável inversão de dígitos). Para urograndis, 108,80% declarado contra 108,9% calculado. |
| Volume | Pacote tratava volume como 3ª variável | V (Smalian) é quase determinado por CAP²·H. **Não é evidência independente.** |
| Classificação da evidência | Coluna `evidence_level` presente | Adequada. Mantida a distinção: verificação de código ≠ plausibilidade biológica ≠ validação externa secundária ≠ validação local futura. |
| Métrica "Acerto" | Definida como heurística | Correto. Manter "pontuação operacional própria, em pontos percentuais, não probabilidade". |
| Clima | Template vazio; regras de classificação seca/úmida exigem período de referência pré-fixado | Regra correta. **Nenhum ano foi classificado nesta etapa**, porque o período de referência ainda não foi definido. |

### 1.1 Protocolo mínimo recomendado para o capítulo de revisão
Registrar: bases consultadas (ex.: Scopus, Web of Science, SciELO, Google Acadêmico, repositórios de teses), string de busca, período, idiomas, critérios de inclusão (gênero *Eucalyptus*; desfolha artificial ou natural com controle; variável de crescimento numérica), critérios de exclusão e um fluxograma simples (encontrados → triados → lidos na íntegra → incluídos). A LSA já feita pode entrar como análise descritiva do corpus, não como critério de seleção.

---

## 2. Verificação das referências e dos valores extraídos

Arquivos: `revisao/estudos_anos_fontes_verificado.csv` e `revisao/dados_tratamentos_observados_verificado.csv` (gerado por `revisao/extrair_pares_observados.py`).

**Correções em relação ao pacote anterior:**
- Bertulio et al. (2008): autores identificados (Bertulio, Peres Filho, Silva e Dorval, UFMT). O DOI não existe no artigo. O artigo deriva da dissertação de Bertulio (2008, UFMT).
- Os valores com 4 casas decimais (36,4275; 38,6225; 17,885; 29,4625) **estão impressos no artigo**. Minha hipótese anterior de que teriam sido calculados estava errada.
- "Grandis_2010" = **Matrangolo et al. (2010)**, PAB 45(9):952–957, Viçosa-MG (20°46′S, 42°52′W), *E. grandis* seminal, medições de 1997 a 2003. O DOI não está impresso no PDF, e há dois DOIs em circulação (pacote anterior × site da Embrapa), a conferir.
- Matrangolo, Tabela 2 (92 meses): **12 novos pares controle/tratamento** (DAP, volume por árvore e volume por hectare; 1, 2 e 3 desfolhas totais). Mortalidade de 6,9–8,8% em todos os tratamentos e 8,0% no controle. O texto informa redução de 37,9% em volume por árvore com uma desfolha, mas a tabela dá 38,6% (outra pequena inconsistência do próprio artigo).
- Pinkard 2006: título e 9 autores conferidos. Pinkard 2007 e Quentin 2010 entram como estudos novos.
- Quentin 2012: a intensidade (folhas de 75% do comprimento da copa) foi registrada.

**Perda observada de Bertulio aos 26 meses: bruta × ajustada pela linha de base (14 meses)**
L_ajustada = 100 × [1 − (T26/C26)/(T14/C14)]. É um cálculo próprio, a declarar como tal.

| Clone | Variável | L bruta (%) | L ajustada (%) |
|---|---|---|---|
| urocam | CAP | 27,7 | 22,9 |
| urocam | altura | 34,1 | 33,2 |
| urocam | volume | 65,7 | 59,0 |
| urograndis | CAP | 23,7 | 24,2 |
| urograndis | altura | 16,1 | 19,1 |
| urograndis | volume | 52,1 | 52,9 |

**Limites para a comparação futura (FASE 9):**
- Nenhum estudo usa *E. urophylla* puro.
- Bertulio e Matrangolo usam **100%** de desfolha, acima do máximo de 95% previsto nos cenários do TCC.
- O espaçamento entre eventos é de ~9 meses (Bertulio) ou 3–7 meses (Matrangolo), e não 36 meses.
- Para comparar, será preciso **simular o protocolo de cada estudo** (intensidade, datas e idade) com o clima do respectivo local, sem recalibrar parâmetros. Como Bertulio não informa coordenadas, o clima de Campo Verde só pode ser atribuído pelo município, com essa limitação declarada.

---

## 3. Estrutura computacional do 3-PG e do módulo de desfolha

### 3.1 Por que uma tradução em Python
Neste ambiente não é possível instalar R nem um compilador Fortran (CRAN, conda, apt e PyPI bloqueados; só o GitHub responde). Por isso o núcleo **3-PGpjs** do r3PG v0.1.7 (commit `e39bd8e9`, arquivo `src/md_3PG.f95`) foi traduzido linha a linha para Python (`modelo/threepg_pjs.py`). A tradução cobre exatamente o que o TCC usa (1 espécie, 3-PGpjs, sem correção de viés por Weibull, sem desbaste). Configurações fora do escopo geram erro explícito.

### 3.2 Verificação da tradução contra o r3PG original
| Referência | Resultado |
|---|---|
| Teste oficial do r3PG "Evergreen 3-PGpjs" (Pinus, 120 meses): Ws, Wr, Wf = 125,423; 39,146; 3,845 | **Idêntico nas 3 casas decimais** |
| Teste oficial "Broadleaf 3-PGpjs" (Fagus decíduo): 129,988; 31,350; 0,000 | **Idêntico nas 3 casas decimais** |
| Trajetória mensal × 3-PG original em Excel/VBA (110 meses, 7 variáveis) | Diferença máxima: 0,07% em Ws e 1,2% em Wf. Como a tradução bate exatamente com os testes do r3PG, atribuo essa diferença, **por inferência**, à diferença entre o r3PG e o VBA (os autores do r3PG mantêm um script de comparação, mas não publicam a tolerância). Não pude rodar o r3PG aqui para confirmar mês a mês. |

### 3.3 Extensão: módulo de desfolha (alteração documentada)
- **Entrada:** `defoliation_events = {"AAAA-MM": d}`, com 0 ≤ d < 1. A função `pulsos(from, [12, 48], d)` converte meses da simulação em datas.
- **Momento:** início do passo mensal, **antes** da interceptação de luz. O mês do evento já cresce com o LAI reduzido.
- **Regra:** Wf_pós = Wf_pré × (1 − d); LAI = Wf_pós × SLA(t) × 0,1.
- **Fluxo separado:** `biom_defol` = Wf_pré × d. Não entra na serapilheira (`biom_loss_foliage`), o que evita dupla contagem.
- **O que não muda:** SLA, αCx, partição, γF e mortalidade. Não há mortalidade induzida nem taxa de recuperação imposta; a recuperação sai das equações originais.
- **Proteções:** erro se d ∉ [0,1), se o mês estiver fora da simulação, se for o mês inicial (linha 0 = estado inicial), se o evento estiver repetido ou se cair em mês de dormência.
- **Convenção temporal herdada do r3PG:** a linha 0 é o estado inicial no fim do mês `from`, e o crescimento começa no mês seguinte. **Decisão pendente:** para "mês 12 = dez/2015", usar `from = "2014-12"`; com `from = "2015-01"`, o mês 12 cai em jan/2016.

### 3.4 Testes automatizados (`modelo/testes/`, 28 testes, todos aprovados)
Os testes rodam no caso de exemplo do r3PG (Pinus/Fagus, Alemanha). **Verificam o código e não são resultados de eucalipto.**

| Exigência do projeto | Teste |
|---|---|
| Reproduzir o controle original | 2 testes de referência do r3PG |
| 0% igual ao controle | igualdade **bit a bit** em todas as colunas |
| Redução instantânea de Wf | `biom_defol` = d × Wf do fim do mês anterior (d = 25/50/95%) |
| LAI atualizado | APAR do mês do evento = fórmula com o LAI pós-desfolha |
| Não negatividade | estoques ≥ 0 e finitos, para pulso único e duplo, nas 3 intensidades |
| Conservação | fechamento mensal de Wf: Wf(t−1) − desfolha + incremento − queda = Wf(t), erro < 1e-12 |
| Calendário | eventos só nos meses 12 e 48; antes do 1º evento, igual ao controle |
| Sem duplicação / entradas inválidas | erros para mês repetido, d = 1, d < 0, mês inicial ou fora do período |
| Unidades | LAI = Wf × SLA × 0,1 em todos os meses |
| Reprodutibilidade | duas execuções idênticas bit a bit |
| Recuperação | Wf volta a crescer, fica ≤ controle, e Ws final < controle |
| Mortalidade induzida desligada | nº de árvores ≥ controle, inclusive com autodesbaste forçado (wSx1000 = 100 **só no teste**) |

**Teste de mutação** (defeitos inseridos de propósito para provar que os testes detectam erro):
- LAI não atualizado após a desfolha: detectado (3 falhas).
- Remoção 0,1% menor: detectado (6).
- Desfolha aplicada duas vezes: detectado (9).
- Calendário do clima deslocado: detectado (8).
- Evento um mês atrasado: detectado (5).
- Mortalidade induzida no evento: detectado (6–7).
- Uma mutação de mortalidade aplicada só no ramo de autodesbaste não teve efeito real, porque o autodesbaste não dispara no mês do evento. Ela continua não detectada. É uma mutação sem efeito, e não uma falha dos testes.

---

## 4. Clima (NASA POWER) — auditoria
Arquivos: `clima/preparar_clima_r3pg.py` e `clima/saida/`.

| Item | Resultado |
|---|---|
| Formato | `;` como separador, vírgula decimal, 1 linha final vazia. **Sem o cabeçalho de metadados do POWER** (coordenadas, altitude, unidades e código de ausente não constam no arquivo). |
| Cobertura diária | 01/01/2015 a **31/01/2024** (3.318 dias). Nenhum dia faltante ou duplicado, nenhum −999, nenhum NaN, Tmax ≥ Tmin em todos os dias. |
| Fevereiro a dezembro de 2024 | **Ausentes no diário.** O arquivo mensal cobre 2024, mas só tem PAR. |
| Arquivo mensal | Só ALLSKY_SFC_PAR_TOT. Confere com a média do diário em 109 meses (diferença máxima de 0,006). Há erro de codificação no cabeçalho ("Męs"). |
| Unidades | ALLSKY_SFC_SW_DWN entre 3,9 e 31,1. Pela faixa de valores, só pode ser MJ m⁻² dia⁻¹ (em W m⁻² ou kWh m⁻² dia⁻¹ os números seriam outros); a razão PAR/SW = 0,46 é coerente. Isso é **inferência pela faixa**, porque o cabeçalho foi removido. |
| Geada | Tmin mínima de 4,3 °C. Nenhum dia ≤ 0 °C, então frost_days = 0 em todos os meses. |
| **Coordenadas** | O ponto do arquivo (−18,68; −47,77) fica a ~40 km da sede de Indianópolis (≈ −19,04; −47,92). Na grade de meteorologia do POWER (0,5° × 0,625°), os dois pontos podem cair em células diferentes. **É preciso confirmar onde fica o povoamento de referência.** |
| Precipitação anual | 842 mm (2023) a 1.298 mm (2018). Isso deve ser comparado com uma estação do INMET próxima antes do uso, porque reanálises podem subestimar a chuva no Cerrado. **Não verificado.** |
| Saída para o r3PG | `clima_r3pg_mensal_POWER.csv`: 109 meses (jan/2015–jan/2024) com tmp_min, tmp_max, tmp_ave, prcp, srad, frost_days e vpd_day (fórmula interna do r3PG). Uma alternativa de VPD pela umidade relativa fica em `clima_mensal_completo_com_controles.csv`, para análise de sensibilidade. |

---

## 5. Entradas que impedem a execução para Indianópolis

| Entrada (r3PG) | Situação | Onde pode estar |
|---|---|---|
| **82 parâmetros da espécie** | Ausentes. Não serão substituídos pelos padrões genéricos do r3PG. | `3PG_CENARIO_CALDEIRA_INDIANOPOLIS.xlsx`, `3PG_FINAL_INDIANOPOLIS_COM_ROTEIRO.xlsx`. **Caldeira et al. (2020) é a única fonte do corpus com *E. urophylla* puro (clone A1).** Borges (2009) e a tese de Silva usam híbridos *E. grandis × E. urophylla*. |
| Alometrias de altura e volume (aH, nHB, nHC; aV, nVB, nVH, nVBH) | Ausentes. Sem elas, a altura sai zero e o volume vem de Ws/densidade. | `ajuste_altura_dap.csv` |
| Biomassas iniciais Wf, Ws, Wr (t/ha) e data de plantio | Ausentes | planilhas acima |
| Densidade inicial (`stems_n`) | 1.111 árv./ha é o valor teórico (3 × 3 m); o observado não está documentado | a decidir: teórico declarado ou observado |
| Solo: `soil_class`, `asw_i`, `asw_min`, `asw_max`, `fertility` | Ausentes | planilhas; fonte pedológica a citar |
| Latitude e altitude do povoamento | Não confirmadas (ver coordenadas na seção 4) | informar o local |
| Clima de fev a dez/2024 | Ausente no diário | baixar de novo do POWER (jan–dez/2024) ou limitar a jan/2024 |
| CO₂ | Ausente; o r3PG usa 350 ppm por padrão | decidir: padrão declarado ou série observada (ex.: Mauna Loa) |

**Pode ser feito antes de esses arquivos chegarem:** extrair do PDF de Caldeira et al. (2020) a tabela de parâmetros publicada, com página e tabela de origem de cada valor, para conferir depois com as planilhas.

---

## 6. Decisões pendentes (suas e do orientador)
1. Convenção do mês do pulso (seção 3.3) e mês do pulso único.
2. "SLA constante": SLA0 = SLA1 (fixo ao longo da idade) ou apenas "a desfolha não altera o SLA" (já é assim no módulo).
3. Período de referência para classificar anos secos e úmidos, e definições de dia seco e onda de calor, antes de qualquer cálculo.
4. Se a perda de Bertulio usada na comparação será a bruta, a ajustada pela linha de base, ou ambas.

## Arquivos
`modelo/` (tradução + desfolha + 28 testes + comparação com VBA) · `clima/` (script + saídas auditadas) · `revisao/` (estudos e pares verificados) · `lsa/` · `corpus_pdfs/` (não incluso no pacote; já está com você)
