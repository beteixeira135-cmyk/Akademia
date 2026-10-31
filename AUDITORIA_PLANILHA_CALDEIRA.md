# Auditoria — `3PG_CALDEIRA_INDIANOPOLIS_PLANTIO_JAN2015.xlsx` (30/10/2026)

Planilha com 16 abas e cerca de 22 mil fórmulas, que implementa o 3-PG mensal com rastreabilidade (FONTE / ADAPTADO / MISSING). A auditoria verificou: (1) os parâmetros contra os PDFs; (2) a dinâmica, comparando com o r3PG (tradução já verificada contra os testes oficiais).

## 1. Parâmetros — conferidos
- **Todos os valores marcados como FONTE conferem com Caldeira et al. (2020)**, Tabela 1 (p. 5) e §2.7: biomassas iniciais aos 12 meses (2,07 / 5,47 / 1,09 t/ha), Y, ρ, wSx1000, αCx, gCx, gSx, kD, gB, Fbb0/Fbbm/tFbb, SLA0/SLAm/tSLA, k, tfullCan, cpir, γFx/γF0/tγF, γR, ηRx/ηRn, pFS2/pFS20, aS/nS, sk1m/sk2m, Tmin/Topt/Tmax, FR = 0,8 (§2.7.1), função FR(CTCe) (§2.10.4) e limite de 80 meses.
- **Os conflitos registrados na aba 12_CONFLITOS são reais e estão descritos corretamente:** aS/nS 0,0249/3,021 (texto) × 0,025/3,02 (tabela); Fbbm 0,12 (texto) × 0,15 (tabela); γF0 0,062 (texto) × 0,06 (tabela); a coluna "Eucalyptus urophylla — Caldeira et al., 2020" do `3PGmix.Data.xls` traz γF0 = 0,13, Y = 0,05 e MinCond = 0,0072, que são erros de transcrição.
- **Os valores ADAPTADOS conferem com a coluna *E. globulus* do `3PGmix.Data.xls`.** Ponto não discutido na planilha: o mesmo arquivo traz colunas de **Borges (2009)**, para híbrido *E. grandis × E. urophylla* no Cerrado de MG, com **MaxAge = 9 anos**, fNn = 1 e LAImaxIntcptn = 3,33, contra 50, 0 e 0 da coluna *E. globulus*. Aos 6 anos, fAge ≈ 0,80 com MaxAge = 9 contra ≈ 1,00 com MaxAge = 50. A escolha da fonte de preenchimento é uma decisão metodológica que precisa ser justificada no TCC.
- **Mapeamento para o r3PG:** `cenarios/tabela_parametros_r3pg_cenario_caldeira.csv` (82 parâmetros): 32 FONTE, 18 ADAPTADO, 19 NEUTRO (sem efeito na configuração usada, como CO₂ a 350 ppm constante, d13C e 3-PGmix), 7 AUSENTE_ZERO (γN e altura, processos desligados, como na planilha) e 6 ESTRUTURAL.

## 2. Dinâmica — planilha × r3PG (cenário da aba 14: N0 = 1.111, FR = 0,8, ASW = 190,6 mm, 72 meses a partir de 12 meses de idade)
Recalculei a planilha no LibreOffice (ela estava salva sem os valores calculados) e comparei mês a mês com o port do r3PG, usando a mesma convenção de tempo e o mesmo VPD.

| | Mês 1 (jan/2016) | Mês 24 | Mês 72 |
|---|---|---|---|
| Ws planilha (t/ha) | 9,040 | 51,2 | 147,7 |
| Ws r3PG | 9,040 | 61,0 | 191,2 |
| Volume planilha (m³/ha) | 14,6 | 90,8 | 279,4 |
| Volume r3PG | 14,6 | 107,7 | 361,4 |

No mês 1 as duas implementações coincidem. A diferença aparece a partir do primeiro mês seco e tem duas causas, ambas no balanço hídrico (aba 04_AGUA):

**D1 — Tempo de transpiração.** A planilha calcula Rn como média de 24 h e multiplica λE por 86.400 s. O 3-PG padrão usa radiação diurna e multiplica pelo fotoperíodo, calculado pela latitude (cerca de 13 h em janeiro). Fontes: Sands (2004, TR141, p. 13: "takes into account the fact that transpiration occurs only during daylight hours"); código do r3PG (`s_transpiration_3pgpjs`). Efeito: transpiração de jan/2016 = 83 mm na planilha contra 52 mm no 3-PG.

**D2 — ET sem limite pela água disponível.** Quando ET > água disponível (abril/2016: 214 mm), a planilha zera a ASW e repõe o déficit na coluna "Ajuste piso", **sem reduzir a ET nem o GPP/NPP**. Isso cria água no balanço. O 3-PG limita ET = min(ASW, transpiração + interceptação) e escala GPP e NPP na mesma razão. Fontes: **a própria tese de Silva (2021), p. 64 do PDF**, citada pela planilha como base estrutural: "A evapotranspiração considera o mínimo valor entre a quantidade de água disponível no solo e a soma da transpiração com a quantidade de chuva interceptada pelo dossel"; código do r3PG (`f_transp_scale`).

**Prova do diagnóstico:** apliquei D1 e D2 numa cópia do port (variante só de teste, não entregue como modelo). A trajetória da planilha passou a ser reproduzida: diferença máxima de 1,1% em Ws, contra 30% antes. O resíduo vem de duas convenções menores:
- a planilha usa fevereiro com 29 dias em 2016 e 2020, e o r3PG usa calendário fixo de 365 dias;
- a planilha usa o SLA na idade do início de cada mês.

Arquivo: `cenarios/comparacao_planilha_x_port_cenario_caldeira.csv`.

**Consequência:** a planilha **subestima o crescimento em cerca de 23% no volume aos 72 meses** neste cenário, por um desvio do 3-PG padrão e não por diferença de parâmetro. Recomendo adotar a convenção do 3-PG (r3PG). Em todo caso, a decisão é sua e do orientador, e deve ser registrada.

## 3. Outros pontos
- **VPD "modo 3" (padrão da planilha):** a média mensal de es_médio × (1 − UR) diário (reproduzida exatamente: 1,4109 kPa em jan/2015). É um VPD de 24 h. O 3-PG pede **VPD diurno** (Landsberg & Waring 1997, p. 212; Sands 2004, p. 9), e o manual do 3PGmix (p. 20) o estima como ½[es(Tmax) − es(Tmin)], que é o modo 1 e o padrão do r3PG. As médias são próximas (1,063 × 1,009 kPa), mas a escolha precisa ser justificada.
- **Testes internos 13 (ηR + ηS + ηF = 1) e 18 (ws/wSx ≤ 1):** retornam #VALUE! após o recálculo. A causa são as linhas inativas (meses 73–120), que contêm "" dentro de SUMPRODUCT/comparações. Não afeta a simulação, mas o teste 13 deve falhar também no Excel sempre que p_nMeses < 120. Correção: restringir os intervalos às linhas ativas.
- **Convenção de tempo:** a planilha usa o passo 1 = jan/2016 com idade de 12 meses no início. No r3PG isso equivale a `from = "2015-12"` e `planted = "2014-12"`. Registrar no método.
- **Desfolha na planilha:** aplicada *depois* da mortalidade, no fim do mês. No módulo do r3PG, aplicada *no início do mês, antes da interceptação de luz*. Isso muda em um mês o momento do efeito, e precisa ser uma única convenção no TCC.
- **Tmax = 28,65 °C (Caldeira):** a Tmédia mensal de Indianópolis chega a 26,2 °C, então fT fica baixo nos meses quentes. Não é erro, mas é um ponto sensível para a análise de sensibilidade.

## 4. O que continua pendente (inalterado)
Coordenadas e data de plantio do talhão (01/2015 é hipotética), N0 observado, ASWmax (190,6 × 310,85 mm), ASW0, modo de FR (CTCe ausente), altura (aH/nHB ausentes para o clone) e clima de fev–dez/2024.
