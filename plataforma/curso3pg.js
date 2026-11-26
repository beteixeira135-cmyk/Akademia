(function (root) {
  "use strict";

  const MODULES = [
    { id: "A", title: "Mapa e relógio", short: "A", have: "Um calendário mensal e cinco estados iniciais.", add: "A idade avança um mês (1/12 de ano), sem alterar biomassa, densidade ou água.", why: "Separar estados de fluxos torna explícito que o modelo só muda estoques quando processos são ativados.", depends: "Data de plantio e mês inicial da simulação.", affects: "Idade; WF, WR, WS, N e ASW permanecem constantes.", equations: [], units: "idade: ano; tempo: mês; biomassa: t ha⁻¹; N: árvores ha⁻¹; ASW: mm.", source: "Convenção temporal do r3PG documentada em modelo/threepg_pjs.py.", experiment: "Execute vários meses e compare cada estado com o mês inicial.", prediction: "A idade aumenta; os cinco estados não mudam.", explanation: "Ainda não há processo de produção nem alocação ativo.", test: "incremento mensal da idade e invariância de WF, WR, WS, N e ASW.", scope: "3-PGpjs, estágio pedagógico sem processos de crescimento." },
    { id: "B", title: "Condições iniciais", short: "B", have: "Idade e estados do módulo A.", add: "WF, WR, WS, N e ASW inicializados a partir do cenário; entradas podem ser alteradas.", why: "O estado inicial define de onde parte cada execução e precisa respeitar unidades e limites físicos.", depends: "Módulo A; material, local, plantio e ASWmax do cenário.", affects: "LAI, balanço de água, produção, partição e densidade nos estágios seguintes.", equations: ["state.wf", "state.wr", "state.ws", "state.n", "state.asw"], units: "WF, WR, WS: t ha⁻¹; N: árvores ha⁻¹; ASW e ASWmax: mm; idade: ano.", source: "Dados existentes em plataforma/dados_min.json e mapeamento em modelo/caldeira_indianopolis.py.", experiment: "Altere WF e execute; o estado inicial muda, mas não surge crescimento antes de D4.", prediction: "Entradas válidas são refletidas na linha inicial; valores inválidos são rejeitados.", explanation: "O motor registra os estoques fornecidos sem estimar valores ausentes.", test: "validação de não negatividade, N > 0, ASW dentro de [0, ASWmax] e preservação do estado.", scope: "Estado inicial do cenário 3-PGpjs." },
    { id: "C", title: "Clima", short: "C", have: "Estados iniciais do módulo B.", add: "Série mensal disponível para o local selecionado, com radiação, chuva, VPD, geada e temperatura.", why: "O clima fornece entradas temporais; seus dados não são estados da árvore.", depends: "Local e cobertura temporal da série incluída.", affects: "Dossel/radiação, restrições de água, GPP e NPP nos estágios seguintes.", equations: [], units: "temperatura: °C; precipitação: mm mês⁻¹; radiação: MJ m⁻² dia⁻¹; VPD: mbar; geada: dias mês⁻¹.", source: "Dados mensais existentes em plataforma/dados_min.json; agregação descrita em experimentos/clima.py.", experiment: "Inspecione meses extremos e altere uma entrada climática para análise de sensibilidade.", prediction: "A alteração afeta apenas a entrada climática escolhida e é rotulada como cenário exploratório.", test: "cobertura, comprimentos iguais, valores finitos e ordem Tmin ≤ Tmed ≤ Tmax.", scope: "Dados climáticos incluídos; não constitui validação de campo." },
    { id: "D1", title: "Dossel e radiação", short: "D1", have: "Estados iniciais, idade e clima.", add: "SLA, LAI, interceptação e APAR pela formulação implementada.", why: "A biomassa foliar controla a área de folhas e a fração de radiação absorvida.", depends: "WF, SLA, k, idade, radiação incidente e dias do mês.", affects: "APAR disponível para as restrições e a produção.", equations: ["eq.lai", "eq.beer"], units: "SLA: m² kg⁻¹; WF: t ha⁻¹; LAI: m² m⁻²; radiação: MJ m⁻² dia⁻¹; APAR: MJ m⁻² mês⁻¹.", source: "Implementação existente em plataforma/modelo3pg.js; conceitos em plataforma/conceitos.js.", experiment: "Compare LAI e APAR após alterar WF.", prediction: "LAI e APAR não negativos; LAI zero implica APAR zero; APAR não excede a radiação incidente mensal.", test: "invariantes de LAI/APAR e limite superior por mês.", scope: "Implementação 3-PGpjs; correspondência exata com a numeração do artigo de 1997 pendente." },
    { id: "D2", title: "Água e restrições", short: "D2", have: "Clima, dossel e APAR.", add: "Balanço de ASW, transpiração e modificadores ambientais implementados.", why: "As condições ambientais limitam a eficiência e alteram a água disponível no solo.", depends: "ASW, ASWmax, chuva, VPD, temperatura, geada, idade e parâmetros do cenário.", affects: "APAR utilizável, eficiência efetiva, GPP e partição nos estágios seguintes.", equations: ["eq.1997.1.vpd", "eq.1997.2.soil_water", "eq.1997.3.age", "eq.1997.frost", "eq.pm.canopy"], units: "modificadores: adimensionais [0,1]; ASW: mm; transpiração: mm mês⁻¹; VPD: mbar.", source: "Implementação existente em plataforma/modelo3pg.js; forma e ordem de atualização de Penman–Monteith permanecem pendentes de regressão independente.", experiment: "Compare dois valores de precipitação no mesmo mês, sem alterar parâmetros.", prediction: "ASW permanece entre 0 e ASWmax; modificadores ficam em [0,1].", test: "limites dos modificadores, armazenamento hídrico e transpiração não negativa.", scope: "3-PGpjs implementado; equivalência independente de Penman–Monteith não declarada." },
    { id: "D3", title: "GPP e NPP", short: "D3", have: "APAR e restrições ambientais.", add: "Produção primária bruta e líquida, sem atualizar os estoques.", why: "GPP representa a fixação bruta de carbono; NPP desconta respiração conforme a formulação do modelo.", depends: "APAR, eficiência efetiva, disponibilidade de água e rendimento y.", affects: "Fluxo que será distribuído entre folhas, raízes e fuste em D4.", equations: ["eq.1997.gpp", "eq.1997.npp"], units: "GPP e NPP: t ha⁻¹ mês⁻¹ na saída do motor.", source: "Implementação existente em plataforma/modelo3pg.js; origem normativa indicada na biblioteca de referências.", experiment: "Zere a radiação de um mês e compare GPP e NPP.", prediction: "Radiação zero implica GPP zero; GPP zero implica NPP zero.", test: "não negatividade e relação NPP = y × GPP.", scope: "Formulação executada pelo porte 3-PGpjs; validação empírica não inferida." },
    { id: "D4", title: "Partição", short: "D4", have: "NPP do módulo D3.", add: "Alocação do fluxo em folhagem, raízes e fuste; atualização dos estoques.", why: "A NPP não se converte em um único compartimento: o modelo distribui o incremento.", depends: "NPP, fertilidade, estado hídrico, alometria e parâmetros de partição.", affects: "WF, WR e WS do mês seguinte; N e ASW continuam estados do cenário.", equations: ["eq.1997.15.root_partition", "eq.1997.9.allometry"], units: "frações de partição: adimensionais; biomassa: t ha⁻¹.", source: "Implementação existente em plataforma/modelo3pg.js.", experiment: "Compare a soma das frações com 1 e observe os três estoques.", prediction: "As frações somam 1 e as atualizações não produzem estoques negativos.", test: "balanço de partição e não negatividade dos estados.", scope: "3-PGpjs; extensões de compensação não são executadas nos estágios A–D5." },
    { id: "D5", title: "Perdas e autodesbaste", short: "D5", have: "Estoques atualizados por produção e partição.", add: "Turnover, mortalidade e autodesbaste presentes no motor.", why: "Os estoques resultam de crescimento menos perdas; a densidade não deve aumentar por mortalidade.", depends: "WF, WR, WS, idade, parâmetros de mortalidade e condições do povoamento.", affects: "Biomassa e N que iniciam o próximo mês.", equations: ["eq.1997.7.litter", "eq.1997.8.self_thinning"], units: "biomassa: t ha⁻¹; N: árvores ha⁻¹; perdas: t ha⁻¹ mês⁻¹.", source: "Implementação existente em plataforma/modelo3pg.js; mapeamento da equação de autodesbaste para a referência de 1997 pendente.", experiment: "Acompanhe N e biomassa por vários meses.", prediction: "Estados não negativos; N não aumenta por mortalidade.", test: "não negatividade e monotonicidade não crescente de N.", scope: "3-PGpjs. Desfolha, compensação e outros danos são extensões separadas." },
    { id: "D6", title: "Saídas, testes e auditoria", short: "D6", have: "Processos dos módulos anteriores.", add: "Saídas mensais, testes de invariantes, comparação com linha-base e pacote de auditoria.", why: "Resultados precisam ser interpretáveis e reproduzíveis, não apenas visualizados.", depends: "Cenário, clima, parâmetros, equações, fontes e versão do motor.", affects: "Relato reproduzível da execução, sem converter verificação em validação.", equations: [], units: "Cada série conserva a unidade indicada na biblioteca de equações.", source: "Metadados e saídas do motor; commit só é informado quando disponível no build.", experiment: "Salve uma linha-base, altere uma entrada e compare as séries.", prediction: "Execuções iguais no mesmo cenário produzem as mesmas séries e o mesmo hash.", test: "determinismo, hash e completude do manifesto de auditoria.", scope: "Validação operacional; validação científica de campo permanece distinta e pendente." }
  ];

  const SOURCES = [
    { id: "source.lw1997", kind: "Fonte normativa", citation: "Landsberg, J. J.; Waring, R. H. (1997). A generalised model of forest productivity using simplified concepts of radiation-use efficiency, carbon balance and partitioning. Forest Ecology and Management, 95, 209–228. DOI: 10.1016/S0378-1127(97)00026-1.", note: "Referência normativa indicada para o núcleo original. O mapeamento individual das equações abaixo para a numeração do artigo continua pendente quando não comprovado no código/fontes." },
    { id: "source.r3pg", kind: "Implementação", citation: "Trotsiuk, Hartig & Forrester (2020), r3PG v0.1.7; código-fonte src/md_3PG.f95 no commit e39bd8e9.", note: "Porte 3-PGpjs usado pelo projeto; não é sinônimo de todas as formulações do 3-PG original." },
    { id: "source.excel", kind: "Implementação / auditoria", citation: "entradas/3PG_CALDEIRA_INDIANOPOLIS_PLANTIO_JAN2015.xlsx; abas 01_PARAMETROS e 02_CLIMA.", note: "O mapeamento de parâmetros disponível está em modelo/caldeira_indianopolis.py. Fórmulas/células não mapeadas são marcadas como pendentes." }
  ];

  const EXCEL_PENDING = "Pendente: célula ou fórmula não localizada no mapeamento existente.";
  const EQUATIONS = [
    { id: "state.wf", name: "Biomassa foliar inicial", description: "Estoque de folhas por área no início da execução.", equation: "WF₀", inputs: ["WF0"], outputs: ["WF"], units: "WF0: t ha⁻¹; WF: t ha⁻¹", source_ids: ["source.excel"], scope: "estado inicial", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: run → S.Wf; modelo/caldeira_indianopolis.py: entradas WF0", tests: ["B: preserva estado inicial"], excel_mapping: "01_PARAMETROS!C33, conforme modelo/caldeira_indianopolis.py", status: "mapped" },
    { id: "state.wr", name: "Biomassa radicular inicial", description: "Estoque de raízes por área no início da execução.", equation: "WR₀", inputs: ["WR0"], outputs: ["WR"], units: "WR0: t ha⁻¹; WR: t ha⁻¹", source_ids: ["source.excel"], scope: "estado inicial", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: run → S.Wr; modelo/caldeira_indianopolis.py: entradas WR0", tests: ["B: preserva estado inicial"], excel_mapping: "01_PARAMETROS!C35, conforme modelo/caldeira_indianopolis.py", status: "mapped" },
    { id: "state.ws", name: "Biomassa de fuste inicial", description: "Estoque de fuste por área no início da execução.", equation: "WS₀", inputs: ["WS0"], outputs: ["WS"], units: "WS0: t ha⁻¹; WS: t ha⁻¹", source_ids: ["source.excel"], scope: "estado inicial", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: run → S.Ws; modelo/caldeira_indianopolis.py: entradas WS0", tests: ["B: preserva estado inicial"], excel_mapping: "01_PARAMETROS!C34, conforme modelo/caldeira_indianopolis.py", status: "mapped" },
    { id: "state.n", name: "Densidade inicial", description: "Número de árvores por hectare no início da execução.", equation: "N₀ > 0", inputs: ["N0"], outputs: ["N"], units: "árvores ha⁻¹", source_ids: ["source.excel"], scope: "estado inicial", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: run → S.N; modelo/caldeira_indianopolis.py: entradas N0", tests: ["B: N > 0"], excel_mapping: "01_PARAMETROS!C30, conforme modelo/caldeira_indianopolis.py", status: "mapped" },
    { id: "state.asw", name: "Água disponível inicial", description: "Água armazenada no solo no início da execução.", equation: "0 ≤ ASW₀ ≤ ASWmax", inputs: ["ASW0", "ASWmax"], outputs: ["ASW"], units: "mm", source_ids: ["source.excel"], scope: "estado inicial", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: run → ASW; modelo/caldeira_indianopolis.py: entradas ASW0/ASWmax", tests: ["B: limite hídrico"], excel_mapping: "01_PARAMETROS!C41 (ASW0), C40 (ASWmax)", status: "mapped" },
    { id: "eq.lai", name: "Índice de área foliar", description: "Conversão da biomassa foliar em área foliar por área de terreno.", equation: "LAI = WF × SLA × 0,1", inputs: ["WF (t ha⁻¹)", "SLA (m² kg⁻¹)"], outputs: ["LAI"], units: "m² folha m⁻² solo", source_ids: ["source.r3pg", "source.lw1997"], scope: "implementação 3-PGpjs; vínculo original a verificar", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: S.lai = S.Wf * SLA[t] * 0.1", tests: ["D1: LAI ≥ 0"], excel_mapping: EXCEL_PENDING, status: "formula-mapped/source-numbering-pending" },
    { id: "eq.beer", name: "Absorção de radiação pelo dossel", description: "A fração absorvida cresce de forma não linear com o LAI.", equation: "APAR = srad × dias × [1 − exp(−k × LAI / cc)] × cc", inputs: ["srad", "dias no mês", "k", "LAI", "cc"], outputs: ["APAR"], units: "MJ m⁻² mês⁻¹", source_ids: ["source.r3pg", "source.lw1997"], scope: "implementação 3-PGpjs; vínculo original a verificar", model_version: "3-PGpjs r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: li e apar", tests: ["D1: APAR ≥ 0 e limitado pela radiação"], excel_mapping: EXCEL_PENDING, status: "formula-mapped/source-numbering-pending" },
    { id: "eq.1997.1.vpd", name: "Modificador de VPD implementado", description: "Forma executada no porte JavaScript; o identificador 1997 é provisório até conferência com a fonte normativa.", equation: "fVPD = exp(−CoeffCond × VPD)", inputs: ["CoeffCond", "VPD"], outputs: ["fVPD"], units: "adimensional; VPD em mbar", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento ao número da equação de 1997 pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: fvpd", tests: ["D2: fVPD ∈ [0,1]"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.2.soil_water", name: "Modificador de água no solo implementado", description: "Forma executada no porte JavaScript, com armazenamento relativo e parâmetros do cenário.", equation: "fSW = 1 / {1 + [(1 − ASW/ASWmax)/SWconst]^SWpower}", inputs: ["ASW", "ASWmax", "SWconst", "SWpower"], outputs: ["fSW"], units: "adimensional; ASW em mm", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento ao número da equação de 1997 pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: fsw", tests: ["D2: fSW ∈ [0,1]"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.3.age", name: "Modificador de idade implementado", description: "Forma executada no porte JavaScript; conferência com a numeração normativa pendente.", equation: "fAge = 1 / [1 + ((idade/MaxAge)/rAge)^nAge]", inputs: ["idade", "MaxAge", "rAge", "nAge"], outputs: ["fAge"], units: "adimensional; idade e MaxAge na mesma unidade", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento ao número da equação de 1997 pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: fage", tests: ["D2: fAge ∈ [0,1]"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.frost", name: "Modificador de geada implementado", description: "Forma executada no porte JavaScript; conferência com a numeração normativa pendente.", equation: "fFrost = 1 − kF × min(dias de geada, dias do mês)/dias do mês", inputs: ["kF", "frost_days", "dias no mês"], outputs: ["fFrost"], units: "adimensional; frost_days em dias mês⁻¹", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: ffrost", tests: ["D2: modificador dentro do domínio"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.pm.canopy", name: "Transpiração de dossel (Penman–Monteith)", description: "O porte contém um cálculo de transpiração; a forma, ordem de atualização, conversões e equivalência independente continuam pendentes de regressão.", equation: "Implementação em plataforma/modelo3pg.js; transcrição algébrica e equivalência com Excel pendentes.", inputs: ["radiação", "VPD", "condutância", "temperatura"], outputs: ["transpiração"], units: "mm mês⁻¹", source_ids: ["source.r3pg"], scope: "implementação 3-PGpjs; verificação independente pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: cálculo de tr", tests: ["D2: transpiração não negativa"], excel_mapping: EXCEL_PENDING, status: "pending-independent-regression" },
    { id: "eq.1997.gpp", name: "Produção primária bruta implementada", description: "Conversão da APAR em GPP conforme os fatores e unidades do porte.", equation: "GPP = gDM_mol × molPAR_MJ × α × APAR / 100 × fts", inputs: ["gDM_mol", "molPAR_MJ", "α", "APAR", "fts"], outputs: ["GPP"], units: "t ha⁻¹ mês⁻¹ (saída do motor)", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: GPP", tests: ["D3: GPP não negativa; radiação zero"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.npp", name: "Produção primária líquida implementada", description: "Fraçao líquida da produção primária bruta usada pelo modelo.", equation: "NPP = y × GPP", inputs: ["y", "GPP"], outputs: ["NPP"], units: "t ha⁻¹ mês⁻¹", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: NPP = GPP * P.y", tests: ["D3: NPP = y × GPP"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.7.litter", name: "Perda foliar por turnover implementada", description: "Fluxo mensal executado pelo porte; correspondência exata com a equação numerada do artigo pendente.", equation: "perda foliar = γF × WF (quando não dormente)", inputs: ["γF", "WF", "estado de dormência"], outputs: ["perda foliar"], units: "t ha⁻¹ mês⁻¹", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; numeração original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: lf_", tests: ["D5: estoques não negativos"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.8.self_thinning", name: "Autodesbaste implementado", description: "O porte inclui a função iterativa de mortalidade; transcrição e correspondência normativa pendentes.", equation: "Algoritmo implementado em mortality(); equação e mapeamento de referência pendentes.", inputs: ["N", "WS", "mS", "wSx1000", "thinPower"], outputs: ["N após autodesbaste"], units: "N: árvores ha⁻¹", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; equivalência com a equação original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: mortality e bloco btmax", tests: ["D5: N não aumenta"], excel_mapping: EXCEL_PENDING, status: "pending-original-equation-mapping" },
    { id: "eq.1997.9.allometry", name: "Alometria de fuste implementada", description: "Relação alométrica usada para obter o diâmetro a partir da biomassa de fuste por árvore.", equation: "WS/árvore = aWs × DAP^nWs; DAP = (WS/árvore ÷ aWs)^(1/nWs)", inputs: ["WS", "N", "aWs", "nWs"], outputs: ["DAP"], units: "WS: t ha⁻¹; N: árvores ha⁻¹; DAP: cm no parâmetro do porte", source_ids: ["source.r3pg", "source.lw1997"], scope: "implementação 3-PGpjs; numeração original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: S.dbh", tests: ["D4: estados não negativos"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "eq.1997.15.root_partition", name: "Partição para raízes implementada", description: "Forma executada no porte para a fração de NPP destinada às raízes.", equation: "ηR = pRx × pRn / [pRn + (pRx − pRn) × fphys × m]", inputs: ["pRx", "pRn", "fphys", "m"], outputs: ["ηR", "ηF", "ηS"], units: "frações adimensionais", source_ids: ["source.r3pg", "source.lw1997"], scope: "3-PGpjs; mapeamento original pendente", model_version: "r3PG v0.1.7", implementation: "plataforma/modelo3pg.js: fr, fs, ff", tests: ["D4: soma das frações = 1"], excel_mapping: EXCEL_PENDING, status: "implementation-mapped/original-equation-pending" },
    { id: "ext.defoliation", name: "Desfolha (extensão)", description: "Remoção explícita de Wf antes do cálculo da luz; não pertence ao 3-PG original.", equation: "WFpós = WFpré × (1 − d)", inputs: ["WF", "d", "mês do evento"], outputs: ["WF após remoção", "biomassa removida"], units: "WF: t ha⁻¹; d: fração [0,1)", source_ids: ["source.r3pg"], scope: "extensão do projeto, explicitamente opcional", model_version: "Akademia + 3-PGpjs", implementation: "plataforma/modelo3pg.js: ev[t]", tests: ["D6: extensão ativa apenas com cenário explícito"], excel_mapping: EXCEL_PENDING, status: "extension" }
  ];

  const MAP_NODES = [
    { id: "climate", label: "Clima", type: "input", module: "C", status: "FUTURE", dependencies: [], affected_by: ["cenário climático"], affects: ["canopy", "constraints"], scope: "3-PGpjs inputs", equation_ids: [], source_ids: ["source.r3pg"] },
    { id: "initial_state", label: "Estados iniciais", type: "state", module: "B", status: "FUTURE", dependencies: ["clock"], affected_by: ["condições iniciais"], affects: ["canopy", "constraints", "partition"], scope: "3-PGpjs state", equation_ids: ["state.wf", "state.wr", "state.ws", "state.n", "state.asw"], source_ids: ["source.excel"] },
    { id: "clock", label: "Relógio mensal", type: "time", module: "A", status: "FUTURE", dependencies: [], affected_by: ["data de plantio", "mês inicial"], affects: ["idade", "processos temporais"], scope: "r3PG time convention", equation_ids: [], source_ids: ["source.r3pg"] },
    { id: "wf", label: "Biomassa foliar (WF)", type: "state", module: "B", dependencies: ["initial_state"], affected_by: ["partição", "turnover", "desfolha (extensão)"], affects: ["lai"], scope: "3-PGpjs state", equation_ids: ["state.wf"], source_ids: ["source.excel", "source.r3pg"] },
    { id: "wr", label: "Biomassa radicular (WR)", type: "state", module: "B", status: "FUTURE", dependencies: ["initial_state"], affected_by: ["partição", "turnover"], affects: ["next_state"], scope: "3-PGpjs state", equation_ids: ["state.wr"], source_ids: ["source.excel", "source.r3pg"] },
    { id: "ws", label: "Biomassa de fuste (WS)", type: "state", module: "B", status: "FUTURE", dependencies: ["initial_state"], affected_by: ["partição", "mortalidade"], affects: ["allometry", "next_state"], scope: "3-PGpjs state", equation_ids: ["state.ws"], source_ids: ["source.excel", "source.r3pg"] },
    { id: "n", label: "Densidade (N)", type: "state", module: "B", status: "FUTURE", dependencies: ["initial_state"], affected_by: ["mortalidade", "autodesbaste"], affects: ["biomassa por árvore", "next_state"], scope: "3-PGpjs state", equation_ids: ["state.n"], source_ids: ["source.excel", "source.r3pg"] },
    { id: "asw", label: "Água disponível (ASW)", type: "state", module: "B", status: "FUTURE", dependencies: ["initial_state"], affected_by: ["chuva", "transpiração", "interceptação"], affects: ["constraints"], scope: "3-PGpjs state", equation_ids: ["state.asw"], source_ids: ["source.excel", "source.r3pg"] },
    { id: "fertility", label: "Fertilidade", type: "input", module: "B", status: "FUTURE", dependencies: ["initial_state"], affected_by: ["cenário"], affects: ["partition", "nutrição"], scope: "3-PGpjs input", equation_ids: [], source_ids: ["source.r3pg"] },
    { id: "canopy", label: "Dossel · SLA e LAI", type: "process", module: "D1", status: "FUTURE", dependencies: ["wf", "climate"], affected_by: ["WF", "SLA", "idade"], affects: ["apar"], scope: "3-PGpjs implementation", equation_ids: ["eq.lai"], source_ids: ["source.r3pg"] },
    { id: "apar", label: "Radiação absorvida (APAR)", type: "process", module: "D1", status: "FUTURE", dependencies: ["canopy", "climate"], affected_by: ["LAI", "radiação", "k"], affects: ["gpp"], scope: "3-PGpjs implementation", equation_ids: ["eq.beer"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "constraints", label: "Restrições ambientais", type: "process", module: "D2", status: "FUTURE", dependencies: ["climate", "asw", "canopy"], affected_by: ["água", "VPD", "temperatura", "geada", "idade"], affects: ["gpp", "partition"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.1.vpd", "eq.1997.2.soil_water", "eq.1997.3.age", "eq.1997.frost", "eq.pm.canopy"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "gpp", label: "GPP", type: "process", module: "D3", status: "FUTURE", dependencies: ["apar", "constraints"], affected_by: ["APAR", "eficiência", "água"], affects: ["npp"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.gpp"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "npp", label: "NPP", type: "process", module: "D3", status: "FUTURE", dependencies: ["gpp"], affected_by: ["GPP", "y"], affects: ["partition"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.npp"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "partition", label: "Partição", type: "process", module: "D4", status: "FUTURE", dependencies: ["npp", "fertility", "constraints"], affected_by: ["NPP", "fertilidade", "fphys", "alometria"], affects: ["wf", "wr", "ws"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.15.root_partition"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "allometry", label: "Alometria de fuste", type: "process", module: "D4", status: "FUTURE", dependencies: ["ws", "n"], affected_by: ["WS por árvore", "parâmetros alométricos"], affects: ["DAP", "partição"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.9.allometry"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "losses", label: "Perdas e autodesbaste", type: "process", module: "D5", status: "FUTURE", dependencies: ["wf", "wr", "ws", "n"], affected_by: ["turnover", "idade", "densidade"], affects: ["next_state"], scope: "3-PGpjs implementation", equation_ids: ["eq.1997.7.litter", "eq.1997.8.self_thinning"], source_ids: ["source.r3pg", "source.lw1997"] },
    { id: "next_state", label: "Novos estados · próximo mês", type: "state", module: "D5", status: "FUTURE", dependencies: ["partition", "losses"], affected_by: ["crescimento", "perdas", "mortalidade"], affects: ["canopy", "constraints", "gpp"], scope: "3-PGpjs state", equation_ids: ["state.wf", "state.wr", "state.ws", "state.n", "state.asw"], source_ids: ["source.r3pg"] },
    { id: "extension", label: "Desfolha e compensação", type: "extension", module: "D6", status: "EXTENSION", dependencies: ["wf"], affected_by: ["cenário explícito"], affects: ["canopy", "apar", "gpp", "partition"], scope: "extensão posterior; não original", equation_ids: ["ext.defoliation"], source_ids: ["source.r3pg"] }
  ];

  const FLOW_MODULE_IDS = MODULES.map(module => module.id);
  const DEFOLIATION_MODULE = {
    id: "EXT-D", title: "Desfolha", kind: "extension", equationId: "ext.defoliation",
    description: "Extensão opcional da Akademia: remove parte de WF no mês do evento e altera o estado foliar que alimenta o dossel.",
    scope: "Não integra o núcleo original do 3-PG; só atua quando há um cenário explícito de desfolha."
  };

  function validateInitial(initial, aswMax) {
    const errors = [];
    for (const key of ["WF0", "WR0", "WS0"]) if (!Number.isFinite(initial[key]) || initial[key] < 0) errors.push(`${key} deve ser finito e ≥ 0.`);
    if (!Number.isFinite(initial.stems_n) || initial.stems_n <= 0) errors.push("N deve ser finito e > 0.");
    if (!Number.isFinite(aswMax) || aswMax <= 0) errors.push("ASWmax deve ser finito e > 0.");
    if (!Number.isFinite(initial.asw_i) || initial.asw_i < 0 || initial.asw_i > aswMax) errors.push("ASW inicial deve estar entre 0 e ASWmax.");
    return errors;
  }

  const close = (a, b, tol = 1e-9) => Math.abs(a - b) <= tol * Math.max(1, Math.abs(a), Math.abs(b));
  const allFinite = values => values.slice(1).every(Number.isFinite);
  const allInRange = (values, lo, hi) => values.slice(1).every(v => Number.isFinite(v) && v >= lo - 1e-9 && v <= hi + 1e-9);
  const allNonnegative = values => values.slice(1).every(v => Number.isFinite(v) && v >= -1e-9);
  function seriesSame(values) { return values.every(v => close(v, values[0])); }
  function checkStage(stageId, output, context) {
    const checks = [];
    const add = (name, pass, detail) => checks.push({ name, pass: !!pass, detail });
    const stable = ["Wf", "Wr", "Ws", "N", "asw"];
    if (["A", "B", "C"].includes(stageId)) {
      add("Idade avança 1/12 ano por mês", output.age.slice(1).every((v, i) => close(v - output.age[i], 1 / 12, 1e-10)), "Variação mensal, não crescimento de biomassa.");
      for (const key of stable) add(`${key} permanece constante`, seriesSame(output[key]), "Verifica todos os meses do estágio.");
    }
    if (stageId === "B") {
      const errors = validateInitial(context.initial, context.aswMax);
      add("Validação das condições iniciais", errors.length === 0, errors.join(" ") || "Biomassas ≥ 0; N > 0; 0 ≤ ASW ≤ ASWmax.");
      for (const [key, outputKey] of [["WF0", "Wf"], ["WR0", "Wr"], ["WS0", "Ws"], ["stems_n", "N"], ["asw_i", "asw"]]) {
        add(`${key} registrado no estado inicial`, close(output[outputKey][0], context.initial[key]), "Compara entrada e linha inicial do motor.");
      }
    }
    if (stageId === "C") {
      const required = ["tmp_min", "tmp_max", "tmp_ave", "prcp", "srad", "frost_days", "vpd_day", "year", "month"];
      const valid = required.every(key => Array.isArray(context.climate[key]) && context.climate[key].length > 1 && context.climate[key].every(Number.isFinite));
      const ordered = context.climate.tmp_min.every((v, i) => v <= context.climate.tmp_ave[i] && context.climate.tmp_ave[i] <= context.climate.tmp_max[i]);
      add("Série climática completa e finita", valid, `Entradas mensais disponíveis: ${context.climate.year.length}.`);
      add("Temperaturas em ordem", valid && ordered, "Tmin ≤ Tmed ≤ Tmax.");
    }
    if (stageId === "D1") {
      add("LAI não negativo", allNonnegative(output.lai), "m² folha m⁻² solo.");
      const bounded = output.apar.slice(1).every((v, i) => {
        const climateIndex = context.climateStartIndex + i + 1;
        const month = context.climate.month[climateIndex];
        const days = new Date(Date.UTC(context.climate.year[climateIndex], month, 0)).getUTCDate();
        return Number.isFinite(v) && v >= -1e-9 && v <= context.climate.srad[climateIndex] * days + 1e-8;
      });
      add("APAR limitada pela radiação incidente", bounded, "Comparação mensal em MJ m⁻² mês⁻¹.");
      add("LAI zero implica APAR zero", output.lai.every((v, i) => !Number.isFinite(v) || v !== 0 || (Number.isFinite(output.apar[i]) && close(output.apar[i], 0))), "Invariante do dossel.");
    }
    if (stageId === "D2") {
      add("fVPD ∈ [0,1]", allInRange(output.fVPD, 0, 1), "Modificador adimensional.");
      add("fSW ∈ [0,1]", allInRange(output.fSW, 0, 1), "Modificador adimensional.");
      add("ASW dentro dos limites", output.asw.slice(1).every(v => Number.isFinite(v) && v >= -1e-9 && v <= context.aswMax + 1e-9), `0 a ${context.aswMax} mm.`);
      add("Transpiração não negativa", allNonnegative(output.transp), "mm mês⁻¹.");
    }
    if (stageId === "D3") {
      add("GPP não negativa", allNonnegative(output.gpp), "t ha⁻¹ mês⁻¹.");
      add("NPP não negativa", allNonnegative(output.npp), "t ha⁻¹ mês⁻¹.");
      add("NPP = y × GPP", output.gpp.slice(1).every((v, i) => close(output.npp[i + 1], context.y * v)), "Relação do porte executado.");
    }
    if (stageId === "D4") {
      const partition = output.etaF.slice(1).every((ff, i) => Number.isFinite(ff) && close(ff + output.etaS[i + 1] + output.etaR[i + 1], 1));
      add("Frações de partição somam 1", partition, "ηF + ηS + ηR.");
      for (const key of ["Wf", "Wr", "Ws"]) add(`${key} permanece não negativo`, allNonnegative(output[key]), "Estado após atualização por partição.");
    }
    if (stageId === "D5" || stageId === "D6") {
      for (const key of ["Wf", "Wr", "Ws", "N", "asw"]) add(`${key} não negativo`, allNonnegative(output[key]), "Estado em todos os meses.");
      add("Densidade não aumenta", output.N.slice(1).every((v, i) => v <= output.N[i] + 1e-8), "A mortalidade não cria árvores.");
    }
    if (stageId === "D6") {
      const deterministic = context.repeatOutput && JSON.stringify(output) === JSON.stringify(context.repeatOutput);
      add("Execução determinística", deterministic, "Duas execuções com as mesmas entradas devem coincidir exatamente.");
      add("Hash de cenário disponível", typeof context.scenarioHash === "string" && /^[a-f0-9]{64}$/.test(context.scenarioHash), "SHA-256 do cenário canônico.");
    }
    return { pass: checks.length > 0 && checks.every(x => x.pass), checks };
  }

  function canonical(value) {
    if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
    if (value && typeof value === "object") return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
    return JSON.stringify(value);
  }
  async function sha256(value) {
    if (!root.crypto || !root.crypto.subtle) throw new Error("SHA-256 indisponível neste contexto. Abra a Akademia via HTTPS para gerar o pacote.");
    const bytes = new TextEncoder().encode(typeof value === "string" ? value : canonical(value));
    const digest = await root.crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
  }

  const api = { MODULES, SOURCES, EQUATIONS, MAP_NODES, FLOW_MODULE_IDS, DEFOLIATION_MODULE, validateInitial, checkStage, canonical, sha256 };
  root.Curso3PG = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;

  let state = { mode: "learn", tab: "home", moduleId: "A", completed: {}, lastRun: null, baseline: null, overrides: null, initialKey: null, climateKey: null, climateOverrides: {}, selectedYear: null };
  let runtime = null;
  const STORAGE_KEY = "akademia-curso-3pg-v1";
  const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  const safeRead = () => {
    try { return JSON.parse(root.localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch (error) { console.warn("Não foi possível ler o progresso local da Akademia.", error); return {}; }
  };
  const safeWrite = () => {
    try { root.localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch (error) { console.warn("Não foi possível salvar o progresso local da Akademia.", error); }
  };
  const byId = id => document.getElementById(id);
  const moduleById = id => MODULES.find(module => module.id === id);
  const equationById = id => EQUATIONS.find(equation => equation.id === id);
  const sourceById = id => SOURCES.find(source => source.id === id);
  let stageRunPending = false;
  function showCourseError(message) {
    let node = byId("course-error");
    if (!node) {
      node = document.createElement("p");
      node.id = "course-error";
      node.setAttribute("role", "alert");
      byId("course-content").prepend(node);
    }
    node.textContent = message;
  }

  function defaultInitial(site, material, aswMax) {
    const m = runtime.data.materiais[material], s = runtime.data.sitios[site];
    return { WF0: m.WF0, WR0: m.WR0, WS0: m.WS0, stems_n: 10000 / 9, asw_i: Math.min(s.asw_local, aswMax ?? s.asw_local) };
  }
  function ensureScenario(site, material, aswMax) {
    const key = `${site}|${material}|${aswMax ?? runtime.data.sitios[site].asw_local}`;
    if (state.initialKey !== key) { state.initialKey = key; state.overrides = defaultInitial(site, material, aswMax); state.baseline = null; }
    if (state.climateKey !== site) { state.climateKey = site; state.climateOverrides = {}; state.selectedYear = null; }
  }
  function climateWithOverrides(site) {
    const original = runtime.data.sitios[site].clima;
    const climate = Object.fromEntries(Object.entries(original).map(([key, values]) => [key, [...values]]));
    for (const [date, changes] of Object.entries(state.climateOverrides)) {
      const [year, month] = date.split("-").map(Number);
      const i = climate.year.findIndex((y, index) => y === year && climate.month[index] === month);
      if (i < 0) continue;
      for (const [key, value] of Object.entries(changes)) if (Array.isArray(climate[key])) climate[key][i] = value;
      if (changes.tmp_min !== undefined || changes.tmp_max !== undefined) climate.tmp_ave[i] = (climate.tmp_min[i] + climate.tmp_max[i]) / 2;
    }
    return climate;
  }
  function scenarioOverrides(site, material, aswMax) {
    if (!runtime) return { initial: null, climate: null };
    ensureScenario(site, material, aswMax);
    return { initial: { ...state.overrides }, climate: climateWithOverrides(site) };
  }
  api.scenarioOverrides = scenarioOverrides;

  function moduleStatus(module) {
    if (state.completed[module.id]) return "LEARNED";
    if (state.lastRun && state.lastRun.moduleId === module.id && !state.lastRun.checks.pass) return "ERROR";
    if (module.id === state.moduleId) return "CURRENT";
    const index = MODULES.findIndex(item => item.id === module.id);
    const ready = index === 0 || MODULES.slice(0, index).every(item => state.completed[item.id]);
    return ready ? "FUTURE" : "FUTURE";
  }
  const STATUS_LABEL = { LEARNED: "Aprendido", CURRENT: "Atual", FUTURE: "Futuro", DEPENDENCY: "Dependência", EXTENSION: "Extensão", ERROR: "Erro" };

  function navHtml() {
    const primary = [["home", "Início"], ["learn", "Aprender"], ["map", "Mapa do fluxo"], ["defoliation", "Desfolha"], ["explore", "Explorar"], ["lab", "Laboratório"]];
    const more = [["equations", "Equações"], ["references", "Referências"], ["tests", "Testes"], ["progress", "Progresso"], ["tutor", "Ajuda / tutor"], ["audit", "Auditoria"]];
    const renderTabs = tabs => tabs.map(([id, label]) => `<button type="button" class="course-tab ${state.tab === id ? "active" : ""}" data-tab="${id}">${label}</button>`).join("");
    const moreActive = more.some(([id]) => state.tab === id);
    return `${renderTabs(primary)}<details class="course-more" ${moreActive ? "open" : ""}><summary class="course-tab ${moreActive ? "active" : ""}">Mais</summary><div class="course-more-menu">${renderTabs(more)}</div></details>`;
  }
  function statusClass(status) { return `status-${status.toLowerCase()}`; }
  function moduleButtons() {
    return MODULES.map(module => {
      const status = moduleStatus(module);
      const blocked = state.mode === "learn" && MODULES.findIndex(item => item.id === module.id) > MODULES.findIndex(item => item.id === state.moduleId) && !state.completed[module.id];
      return `<button type="button" class="module-chip ${statusClass(status)}" data-module="${module.id}" ${blocked ? "disabled" : ""}><b>${module.short}</b><span>${escapeHtml(module.title)}</span><small>${STATUS_LABEL[status]}</small></button>`;
    }).join("");
  }
  function renderHome() {
    return `<section class="course-home">
      <h2>Aprenda o 3-PG, um passo de cada vez</h2>
      <p>Comece pelo básico, mesmo sem experiência com modelagem. O simulador continua acessível; o mapa do fluxo é um guia opcional para quando quiser entender como os processos se conectam.</p>
      <div class="course-actions"><button class="course-primary" data-action="start-learning">Começar pelo módulo A</button><button data-tab="map">Ver o mapa do fluxo (opcional)</button><button data-tab="explore">Explorar o cenário</button></div>
      <div class="course-section academy-principle"><h3>O que você vai acompanhar</h3><p>Entradas e estados → processos mensais → produção e alocação → atualização dos estoques. A desfolha aparece em um módulo próprio, identificado como extensão opcional, sem confundi-la com o núcleo do 3-PG.</p></div>
      <details class="academy-catalog">
        <summary>Ver os módulos da academia</summary>
        <p>Os módulos A–D6 explicam etapas do 3-PGpjs. A extensão de desfolha fica separada do fluxo original.</p>
        <div class="module-strip">${moduleButtons()}</div>
        <button type="button" class="module-chip status-extension" data-tab="defoliation"><b>EXT.</b><span>Módulo de desfolha</span><small>Extensão opcional</small></button>
      </details>
      <div class="course-footnote">Base de cenário: dados incluídos na plataforma. Parâmetros sem proveniência individual, equações sem mapeamento confirmado e comparações independentes ausentes permanecem explicitamente pendentes.</div>
    </section>`;
  }
  function renderMap() {
    const flow = FLOW_MODULE_IDS.map(id => moduleById(id)).map((module, index) => {
      const equations = module.equations.map(id => `<button type="button" class="course-link" data-equation="${escapeHtml(id)}">${escapeHtml(id)}</button>`).join(" ");
      return `<li class="flow-step"><button type="button" class="flow-step-link" data-module="${escapeHtml(module.id)}"><b>${escapeHtml(module.id)}</b><span>${escapeHtml(module.title)}</span></button>
        <p class="flow-operation"><b>O que acontece:</b> ${escapeHtml(module.add)}</p><p class="flow-explanation">${escapeHtml(module.explanation || module.why)}</p>
        <small>Passo ${index + 1} · ${escapeHtml(module.affects)}</small>${equations ? `<div class="node-equations">${equations}</div>` : ""}</li>`;
    }).join("");
    const nodes = MAP_NODES.map(node => {
      const current = moduleById(state.moduleId);
      const required = current ? new Set(MAP_NODES.filter(item => item.module === current.id).flatMap(item => item.dependencies)) : new Set();
      const status = node.type === "extension" ? "EXTENSION" : node.id === state.lastErrorNode ? "ERROR"
        : required.has(node.id) ? "DEPENDENCY" : moduleStatus(moduleById(node.module));
      const eqButtons = node.equation_ids.map(id => `<button type="button" class="course-link" data-equation="${escapeHtml(id)}">${escapeHtml(id)}</button>`).join("");
      const target = node.type === "extension" ? `data-tab="defoliation"` : `data-module="${escapeHtml(node.module)}"`;
      return `<article class="map-node ${statusClass(status)}" data-node="${escapeHtml(node.id)}">
        <button type="button" class="map-node-title" ${target}><span>${escapeHtml(node.label)}</span><small>${STATUS_LABEL[status]} · ${escapeHtml(node.module)}</small></button>
        <div><b>Depende de</b><span>${escapeHtml(node.dependencies.join(", ") || "entrada")}</span></div>
        <div><b>Afetado por</b><span>${escapeHtml(node.affected_by.join(", "))}</span></div>
        <div><b>Afeta</b><span>${escapeHtml(node.affects.join(", "))}</span></div>
        <div><b>Escopo</b><span>${escapeHtml(node.scope)}</span></div><div class="node-equations">${eqButtons}</div></article>`;
    }).join("");
    return `<section><h2>Fluxo mensal do 3-PG</h2>
      <p>Guia opcional: siga os módulos na ordem para ver como as entradas alimentam os processos e como os estoques chegam ao mês seguinte. Se preferir, volte ao simulador sem percorrer o mapa.</p>
      <ol class="flow-steps">${flow}</ol>
      <p class="flow-loop"><b>O ciclo se repete:</b> D5 atualiza os estados do povoamento; no mês seguinte, o fluxo recomeça com dossel e condições ambientais. D6 reúne as saídas e verifica a execução.</p>
      <section class="extension-branch"><h3>Ramo opcional · extensão da Akademia</h3><p>A desfolha altera WF antes do cálculo do dossel; por isso, pode repercutir em LAI, APAR e nos processos seguintes. Ela não pertence ao fluxo original do 3-PG.</p><button type="button" class="module-chip status-extension" data-tab="defoliation"><b>EXT.</b><span>Entender o módulo de desfolha</span><small>Extensão opcional</small></button></section>
      <details class="map-details"><summary>Ver o mapa técnico de dependências</summary>
        <div class="map-legend"><span class="status-learned">Aprendido</span><span class="status-current">Atual</span><span class="status-future">Futuro</span><span class="status-dependency">Dependência</span><span class="status-extension">Extensão</span><span class="status-error">Erro</span></div>
        <div class="map-flow">${nodes}</div><p class="course-footnote">O mapa descreve relações presentes no porte 3-PGpjs da plataforma. A atribuição de números de equação ao artigo de 1997 só é afirmada quando verificada; os demais vínculos aparecem como pendentes na biblioteca.</p>
      </details></section>`;
  }
  function renderDefoliation() {
    const equation = equationById(DEFOLIATION_MODULE.equationId);
    const source = sourceById(equation.source_ids[0]);
    return `<section class="defoliation-module">
      <h2>Módulo de desfolha</h2>
      <p>${escapeHtml(DEFOLIATION_MODULE.description)}</p>
      <p class="extension-scope">${escapeHtml(DEFOLIATION_MODULE.scope)}</p>
      <div class="course-section extension-equation"><h3>O que muda no evento</h3><code>${escapeHtml(equation.equation)}</code>
        <dl><dt>Entradas</dt><dd>${escapeHtml(equation.inputs.join(", "))}</dd><dt>Saídas</dt><dd>${escapeHtml(equation.outputs.join(", "))}</dd><dt>Unidades</dt><dd>${escapeHtml(equation.units)}</dd></dl>
      </div>
      <div class="course-grid module-facts"><article><h3>Onde atua</h3><p>${escapeHtml(equation.implementation)}</p></article><article><h3>Consequência no fluxo</h3><p>WF menor altera o LAI calculado a partir da biomassa foliar e, em seguida, a radiação absorvida pelo dossel.</p></article><article><h3>Como interpretar</h3><p>A extensão só é ativada por um cenário explícito. Resultados simulados não são, por si, validação empírica.</p></article></div>
      <div class="course-section"><h3>Registro e proveniência</h3><p>${escapeHtml(source.citation)}</p><p>${escapeHtml(equation.scope)} · ${escapeHtml(equation.model_version)}.</p>
        <button type="button" class="course-link" data-equation="${escapeHtml(equation.id)}">Abrir registro da equação</button>
      </div>
      <div class="course-actions"><button type="button" class="course-primary" data-action="open-simulator">Abrir controles no simulador</button><button type="button" data-tab="map">Voltar ao mapa do fluxo</button></div>
    </section>`;
  }
  function renderModule(module) {
    const status = moduleStatus(module);
    const equations = module.equations.map(id => `<button type="button" class="course-link" data-equation="${escapeHtml(id)}">${escapeHtml(id)}</button>`).join(" ") || "—";
    const isClimate = module.id === "C";
    const currentScenario = runtime.getScenario();
    ensureScenario(currentScenario.site, currentScenario.material, currentScenario.aswMax);
    const controls = module.id === "B" ? initialControls(currentScenario) : isClimate ? climateControls(currentScenario.site) : "";
    const last = state.lastRun && state.lastRun.moduleId === module.id ? state.lastRun : null;
    const hasNextModule = MODULES.findIndex(item => item.id === module.id) < MODULES.length - 1;
    const nextLabel = hasNextModule
      ? state.completed[module.id] ? "Próximo módulo" : "Avançar após passar nos testes"
      : state.completed[module.id] ? "Trilha concluída" : "Último módulo";
    return `<section class="module-page">
      <div class="module-heading"><div><span class="status-pill ${statusClass(status)}">${STATUS_LABEL[status]}</span><h2>${escapeHtml(module.id)} · ${escapeHtml(module.title)}</h2></div>
        <label class="mode-switch"><span>Modo</span><select id="course-mode"><option value="learn" ${state.mode === "learn" ? "selected" : ""}>Aprender</option><option value="explore" ${state.mode === "explore" ? "selected" : ""}>Explorar</option></select></label></div>
      <div class="module-strip">${moduleButtons()}</div>
      <div class="course-grid module-facts">
        <article><h3>Já tenho</h3><p>${escapeHtml(module.have)}</p></article><article><h3>Adiciono agora</h3><p>${escapeHtml(module.add)}</p></article>
        <article><h3>Por que isso existe</h3><p>${escapeHtml(module.why)}</p></article><article><h3>Depende de</h3><p>${escapeHtml(module.depends)}</p></article>
        <article><h3>Afeta</h3><p>${escapeHtml(module.affects)}</p></article><article><h3>Unidades</h3><p>${escapeHtml(module.units)}</p></article>
        <article><h3>Escopo científico</h3><p>${escapeHtml(module.scope)}</p></article><article><h3>Fonte</h3><p>${escapeHtml(module.source)}</p></article>
      </div>
      <div class="module-equations"><b>Equações registradas:</b> ${equations}</div>
      ${controls}
      <p id="course-error" class="input-errors" role="alert"></p>
      <div class="course-section experiment-box"><h3>Experimento</h3><p>${escapeHtml(module.experiment)}</p><h3>Previsão</h3><p>${escapeHtml(module.prediction)}</p>
        <button type="button" class="course-primary" data-action="run-stage">Executar estágio e testar</button>
        <span class="mini-status">Conclusão exige interface, conteúdo, motor e testes aprovados.</span></div>
      ${last ? renderResult(last, module) : ""}
      <div class="course-section"><h3>Explicação</h3><p>${escapeHtml(module.explanation)}</p><h3>Testes</h3><p>${escapeHtml(module.test)}</p></div>
      <div class="module-nav"><button data-action="previous-module" ${MODULES[0].id === module.id ? "disabled" : ""}>Módulo anterior</button><button data-action="next-module" ${hasNextModule ? "" : "disabled"}>${nextLabel}</button></div>
    </section>`;
  }
  function initialControls(scenario) {
    const values = state.overrides || defaultInitial(scenario.site, scenario.material, scenario.aswMax);
    return `<div class="course-section"><h3>Condições iniciais do cenário atual</h3><p class="course-footnote">Valores iniciais vêm do cenário já existente. Ao alterá-los, a execução fica marcada como exploratória; não há faixa científica documentada para WF, WR, WS ou N neste formulário.</p>
      <div class="input-grid">
        ${[["WF0", "WF · folhas", "t ha⁻¹"], ["WR0", "WR · raízes", "t ha⁻¹"], ["WS0", "WS · fuste", "t ha⁻¹"], ["stems_n", "N · densidade", "árvores ha⁻¹"], ["asw_i", "ASW · água inicial", `mm (máx. ${scenario.aswMax})`]].map(([key, label, unit]) => `<label>${label}<span class="input-unit">${unit}</span><input type="number" step="any" ${key === "stems_n" ? "min=\"0.000001\"" : "min=\"0\""} data-initial="${key}" value="${escapeHtml(values[key])}"></label>`).join("")}
      </div><span id="initial-errors" class="input-errors"></span></div>`;
  }
  function climateControls(site) {
    const climate = climateWithOverrides(site);
    const years = [...new Set(climate.year)].sort((a, b) => a - b);
    const selected = years.includes(Number(state.selectedYear)) ? Number(state.selectedYear) : years[0];
    state.selectedYear = selected;
    const rows = climate.year.map((year, i) => ({ year, i })).filter(x => x.year === selected);
    const climateTable = rows.map(({ i }) => `<tr><td>${climate.year[i]}-${String(climate.month[i]).padStart(2, "0")}</td><td>${climate.tmp_min[i].toFixed(1)} / ${climate.tmp_ave[i].toFixed(1)} / ${climate.tmp_max[i].toFixed(1)} °C</td><td>${climate.prcp[i].toFixed(1)} mm</td><td>${climate.srad[i].toFixed(2)} MJ m⁻² d⁻¹</td><td>${climate.vpd_day[i].toFixed(2)} mbar</td><td>${climate.frost_days[i]} dias</td></tr>`).join("");
    const idx = rows.length ? rows[0].i : 0;
    const date = `${climate.year[idx]}-${String(climate.month[idx]).padStart(2, "0")}`;
    const edited = state.climateOverrides[date] || {};
    return `<div class="course-section"><h3>Série mensal · ${escapeHtml(runtime.data.sitios[site].nome)}</h3>
      <label class="select-label">Ano <select id="course-year">${years.map(year => `<option value="${year}" ${year === selected ? "selected" : ""}>${year}</option>`).join("")}</select></label>
      <div class="table-scroll"><table class="course-table"><thead><tr><th>Mês</th><th>Tmin / Tmed / Tmax</th><th>Chuva</th><th>Radiação média diária</th><th>VPD</th><th>Geada</th></tr></thead><tbody>${climateTable}</tbody></table></div>
      <h3>Editar mês ${date} para análise exploratória</h3><p class="course-footnote">O dado original permanece no repositório; esta alteração é local ao navegador e não é calibração nem validação.</p>
      <div class="input-grid climate-inputs">
        ${[["prcp", "Precipitação", "mm mês⁻¹", true], ["srad", "Radiação média", "MJ m⁻² dia⁻¹", true], ["vpd_day", "VPD diurno", "mbar", true], ["tmp_min", "Tmin", "°C", false], ["tmp_max", "Tmax", "°C", false], ["frost_days", "Dias de geada", "dias mês⁻¹", true]].map(([key, label, unit, nonnegative]) => `<label>${label}<span class="input-unit">${unit}</span><input type="number" step="any" ${nonnegative ? 'min="0"' : ""} data-climate="${key}" data-date="${date}" value="${escapeHtml(edited[key] ?? climate[key][idx])}"></label>`).join("")}
      </div></div>`;
  }
  function renderResult(run, module) {
    const output = run.output;
    const columns = module.id === "A" || module.id === "B" || module.id === "C" ? [["age", "Idade (ano)"], ["Wf", "WF (t ha⁻¹)"], ["Wr", "WR (t ha⁻¹)"], ["Ws", "WS (t ha⁻¹)"], ["N", "N (árvores ha⁻¹)"], ["asw", "ASW (mm)"]]
      : module.id === "D1" ? [["age", "Idade (ano)"], ["lai", "LAI (m² m⁻²)"], ["apar", "APAR (MJ m⁻² mês⁻¹)"]]
      : module.id === "D2" ? [["age", "Idade (ano)"], ["asw", "ASW (mm)"], ["fVPD", "fVPD"], ["fSW", "fSW"], ["transp", "Transpiração (mm mês⁻¹)"]]
      : module.id === "D3" ? [["age", "Idade (ano)"], ["apar", "APAR (MJ m⁻² mês⁻¹)"], ["gpp", "GPP (t ha⁻¹ mês⁻¹)"], ["npp", "NPP (t ha⁻¹ mês⁻¹)"]]
      : module.id === "D4" ? [["age", "Idade (ano)"], ["Wf", "WF (t ha⁻¹)"], ["Wr", "WR (t ha⁻¹)"], ["Ws", "WS (t ha⁻¹)"], ["etaF", "ηF"], ["etaS", "ηS"], ["etaR", "ηR"]]
      : [["age", "Idade (ano)"], ["Wf", "WF (t ha⁻¹)"], ["Wr", "WR (t ha⁻¹)"], ["Ws", "WS (t ha⁻¹)"], ["N", "N (árvores ha⁻¹)"], ["asw", "ASW (mm)"], ["lai", "LAI"], ["apar", "APAR"], ["gpp", "GPP"], ["npp", "NPP"], ["transp", "Transpiração"], ["mortInd", "Mortalidade da extensão"]];
    const head = columns.map(([, label]) => `<th>${label}</th>`).join("");
    const rows = output.age.map((_, i) => `<tr>${columns.map(([key]) => `<td>${Number.isFinite(output[key][i]) ? output[key][i].toLocaleString("pt-BR", { maximumFractionDigits: 4 }) : "—"}</td>`).join("")}</tr>`).join("");
    const checks = run.checks.checks.map(test => `<li class="${test.pass ? "check-pass" : "check-fail"}"><b>${test.pass ? "PASS" : "FAIL"}</b> · ${escapeHtml(test.name)} — ${escapeHtml(test.detail)}</li>`).join("");
    const hash = run.scenarioHash ? `<p class="course-footnote">SHA-256 do cenário: <code>${escapeHtml(run.scenarioHash)}</code></p>` : "";
    return `<div class="course-section result-panel"><h3>Resultado · ${escapeHtml(module.id)} ${run.checks.pass ? "PASS" : "ERROR"}</h3>
      <p>${run.checks.pass ? "Interface, conteúdo, motor e testes aprovados para este módulo." : "O módulo não foi marcado como aprendido: pelo menos um critério falhou."}</p>
      <ul class="test-list">${checks}</ul>${hash}<div class="table-scroll"><table class="course-table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div></div>`;
  }
  function renderExplore() {
    const scenario = runtime.getScenario();
    ensureScenario(scenario.site, scenario.material, scenario.aswMax);
    const sites = Object.entries(runtime.data.sitios).map(([id, item]) => `<option value="${id}" ${id === scenario.site ? "selected" : ""}>${escapeHtml(item.nome)} · ${escapeHtml(item.bioma)}</option>`).join("");
    const materials = Object.entries(runtime.data.materiais).map(([id, item]) => `<option value="${id}" ${id === scenario.material ? "selected" : ""}>${id} · ${escapeHtml(item.nome.nome)}</option>`).join("");
    return `<section><h2>Explorar cenários</h2>
      <div class="course-section"><label class="select-label">Local <select id="explore-site">${sites}</select></label><label class="select-label">Material <select id="explore-material">${materials}</select></label>
        <p>Os controles de desfolha, fertilidade, água e compensação permanecem no simulador principal. <button class="course-link" data-action="open-simulator">Abrir controles do simulador</button></p>
        <p class="course-footnote">O motor é Modelo3PG.run. A navegação altera somente quais processos pedagógicos estão ativos; fórmulas e parâmetros só mudam quando você modifica explicitamente o cenário.</p>
        <button class="course-primary" data-action="run-current">Executar estágio atual (${escapeHtml(state.moduleId)})</button></div>
      <div class="course-section"><h3>Comparar cenários</h3><p>Salve a linha-base em D6 e compare a execução atual. Alterações de entrada são rotuladas como exploratórias.</p>
        <button data-action="save-baseline">Salvar linha-base</button><button data-action="compare">Comparar com linha-base</button><div id="baseline-result">${renderBaseline()}</div></div>
    </section>`;
  }
  function renderBaseline() {
    if (!state.baseline || !state.lastRun || state.lastRun.moduleId !== "D6") return `<p class="course-footnote">Nenhuma linha-base D6 salva nesta sessão do navegador.</p>`;
    const base = state.baseline.output, current = state.lastRun.output;
    const pairs = [["Wf", "WF (t ha⁻¹)"], ["Wr", "WR (t ha⁻¹)"], ["Ws", "WS (t ha⁻¹)"], ["N", "N (árvores ha⁻¹)"], ["asw", "ASW (mm)"], ["gpp", "GPP"], ["npp", "NPP"]];
    const serialMonth = from => {
      const [year, month] = from.split("-").map(Number);
      return year * 12 + month - 1;
    };
    const baseStart = serialMonth(state.baseline.scenario.period.from);
    const currentStart = serialMonth(state.lastRun.scenarioRecord.period.from);
    const lastCommonMonth = Math.min(baseStart + base.age.length - 1, currentStart + current.age.length - 1);
    const commonMonth = Math.max(baseStart, currentStart);
    if (lastCommonMonth < commonMonth) return `<p class="course-footnote">Os cenários não têm meses em comum para comparação.</p>`;
    const baseIndex = lastCommonMonth - baseStart, currentIndex = lastCommonMonth - currentStart;
    const labelMonth = `${Math.floor(lastCommonMonth / 12)}-${String(lastCommonMonth % 12 + 1).padStart(2, "0")}`;
    return `<p>Último mês comum: ${labelMonth}. Comparação exploratória, não validação.</p><table class="course-table"><thead><tr><th>Saída final</th><th>Linha-base</th><th>Atual</th><th>Delta</th></tr></thead><tbody>${pairs.map(([key, label]) => {
      const before = base[key][baseIndex], after = current[key][currentIndex], delta = after - before;
      return `<tr><td>${label}</td><td>${before.toLocaleString("pt-BR", { maximumFractionDigits: 4 })}</td><td>${after.toLocaleString("pt-BR", { maximumFractionDigits: 4 })}</td><td>${delta.toLocaleString("pt-BR", { maximumFractionDigits: 4 })}</td></tr>`;
    }).join("")}</tbody></table>`;
  }
  function renderEquations() {
    const cards = EQUATIONS.map(item => `<details class="equation-card" id="equation-${escapeHtml(item.id)}"><summary><code>${escapeHtml(item.id)}</code> · ${escapeHtml(item.name)} <span class="equation-status">${escapeHtml(item.status)}</span></summary>
      <p>${escapeHtml(item.description)}</p><div class="equation-formula">${escapeHtml(item.equation)}</div>
      <dl><dt>Entradas</dt><dd>${escapeHtml(item.inputs.join(", "))}</dd><dt>Saídas</dt><dd>${escapeHtml(item.outputs.join(", "))}</dd><dt>Unidades</dt><dd>${escapeHtml(item.units)}</dd>
        <dt>Escopo / versão</dt><dd>${escapeHtml(item.scope)} · ${escapeHtml(item.model_version)}</dd><dt>Implementação</dt><dd><code>${escapeHtml(item.implementation)}</code></dd>
        <dt>Teste</dt><dd>${escapeHtml(item.tests.join("; "))}</dd><dt>Excel</dt><dd>${escapeHtml(item.excel_mapping)}</dd><dt>Fontes</dt><dd>${item.source_ids.map(id => { const source = sourceById(id); return source ? escapeHtml(source.id) : "Não localizado nas fontes aprovadas."; }).join(", ")}</dd></dl></details>`).join("");
    return `<section><h2>Biblioteca de equações e estados</h2><p class="course-footnote">Fórmulas executadas e atribuição bibliográfica são tratadas separadamente. O prefixo eq.1997 não confirma por si só a numeração do artigo. Cada item informa o escopo do porte e marca pendências de correspondência normativa ou Excel.</p>${cards}</section>`;
  }
  function renderReferences() {
    return `<section><h2>Referências</h2>${SOURCES.map(source => `<article class="reference-card"><span class="reference-kind">${escapeHtml(source.kind)}</span><p>${escapeHtml(source.citation)}</p><p class="course-footnote">${escapeHtml(source.note)}</p></article>`).join("")}
      <div class="course-section"><h3>Excel como auditoria</h3><p>Planilha localizada: <code>entradas/3PG_CALDEIRA_INDIANOPOLIS_PLANTIO_JAN2015.xlsx</code>. Mapeamentos de entradas iniciais e parâmetros disponíveis em <code>modelo/caldeira_indianopolis.py</code>. O restante permanece pendente; a planilha não é a interface principal.</p></div></section>`;
  }
  function renderTests() {
    const latest = state.lastRun;
    return `<section><h2>Testes</h2>
      <p>Verificação pedagógica não é validação científica. Os testes de estágio são executados contra o motor do navegador e o cenário presente. A comparação JS–Python existente é independente e permanece no diretório de verificação.</p>
      ${latest && moduleById(latest.moduleId) ? renderResult(latest, moduleById(latest.moduleId)) : `<p class="course-footnote">Execute um módulo para ver os testes e resultados registrados nesta sessão.</p>`}
      <div class="course-section"><h3>Regressão</h3><p>Não é criado golden file novo. A regressão de referência depende dos fixtures e dados já versionados; faltas de dados externos são registradas como pendentes.</p></div></section>`;
  }
  function renderProgress() {
    return `<section><h2>Progresso</h2><div class="module-strip">${moduleButtons()}</div>
      <table class="course-table"><thead><tr><th>Módulo</th><th>Status</th><th>Critério de conclusão</th></tr></thead><tbody>${MODULES.map(module => `<tr><td>${module.id} · ${escapeHtml(module.title)}</td><td>${STATUS_LABEL[moduleStatus(module)]}</td><td>Interface + conteúdo + motor + testes aprovados</td></tr>`).join("")}</tbody></table>
      <p class="course-footnote">O progresso é local ao navegador e não representa validação científica.</p></section>`;
  }
  function renderTutor() {
    return `<section><h2>Ajuda / tutor</h2>
      <p>Este protótipo não conecta uma IA generativa. A busca abaixo recupera conteúdo cadastrado; não altera parâmetros, equações ou resultados.</p>
      <label class="select-label">Pergunte por um conceito, símbolo ou unidade<input id="tutor-query" type="search" placeholder="Ex.: APAR, VPD, NPP, ASW"></label><button data-action="ask-tutor">Buscar no registro</button><div id="tutor-answer" class="course-section">As respostas vêm da biblioteca de equações, módulos e referências.</div></section>`;
  }
  function renderLab() {
    const scenario = runtime.getScenario();
    ensureScenario(scenario.site, scenario.material, scenario.aswMax);
    return `<section><h2>Laboratório</h2>
      <p>Cenário ativo: ${escapeHtml(runtime.data.sitios[scenario.site].nome)} · ${escapeHtml(scenario.material)} · água ${escapeHtml(scenario.water)} · fertilidade ${escapeHtml(scenario.fertility)}.</p>
      <div class="course-actions"><button class="course-primary" data-action="run-current">Executar ${escapeHtml(state.moduleId)}</button><button data-action="save-baseline">Salvar linha-base D6</button><button data-action="compare">Comparar</button><button data-action="export-audit">Exportar pacote de auditoria</button></div>
      <div id="baseline-result">${renderBaseline()}</div><div id="lab-output">${state.lastRun && moduleById(state.lastRun.moduleId) ? renderResult(state.lastRun, moduleById(state.lastRun.moduleId)) : ""}</div></section>`;
  }
  function renderAudit() {
    const refs = SOURCES.map(source => source.id).join(", ");
    const pending = EQUATIONS.filter(equation => equation.status.includes("pending")).length;
    return `<section><h2>Auditoria</h2>
      <p>Pacote reproduzível com cenário, hash SHA-256, clima, parâmetros, resultados, testes, referências, versão e mapa Excel. O commit do build é informado somente quando o gerador fornece esse dado.</p>
      <p><b>Fontes cadastradas:</b> ${escapeHtml(refs)}</p><p><b>Equações com mapeamento pendente:</b> ${pending} de ${EQUATIONS.length} registros.</p>
      <p><b>Status científico:</b> verificação operacional/pedagógica. Não declara validação independente.</p>
      <p><b>Excel:</b> mapeamento factual disponível para estados iniciais selecionados; fórmulas e células restantes pendentes.</p>
      <button class="course-primary" data-action="export-audit">Gerar pacote de auditoria JSON</button><span id="audit-status" role="status"></span></section>`;
  }
  function renderTab() {
    if (state.tab === "home") return renderHome();
    if (state.tab === "map") return renderMap();
    if (state.tab === "defoliation") return renderDefoliation();
    if (state.tab === "learn") return renderModule(moduleById(state.moduleId));
    if (state.tab === "explore") return renderExplore();
    if (state.tab === "lab") return renderLab();
    if (state.tab === "equations") return renderEquations();
    if (state.tab === "references") return renderReferences();
    if (state.tab === "tests") return renderTests();
    if (state.tab === "progress") return renderProgress();
    if (state.tab === "tutor") return renderTutor();
    if (state.tab === "audit") return renderAudit();
    return renderHome();
  }
  function render() {
    const modal = byId("m-curso");
    if (!modal) return;
    byId("course-nav").innerHTML = navHtml();
    byId("course-content").innerHTML = renderTab();
    const mode = byId("course-mode");
    if (mode) mode.value = state.mode;
    safeWrite();
  }
  function openTab(tab) {
    state.tab = tab; render();
    const content = byId("course-content");
    if (content) content.scrollTop = 0;
  }
  function currentContext(output, repeatOutput, scenarioHash) {
    const scenario = runtime.getScenario();
    ensureScenario(scenario.site, scenario.material, scenario.aswMax);
    const values = state.overrides || defaultInitial(scenario.site, scenario.material, scenario.aswMax);
    const climate = climateWithOverrides(scenario.site);
    const [startYear, startMonth] = runtime.data.materiais[scenario.material].inicio.split("-").map(Number);
    const climateStartIndex = climate.year.findIndex((year, index) => year === startYear && climate.month[index] === startMonth);
    if (climateStartIndex < 0) throw new Error("A série climática não contém o mês inicial do material selecionado.");
    return {
      initial: values, aswMax: scenario.aswMax,
      climate, climateStartIndex, y: runtime.data.materiais[scenario.material].params.y,
      repeatOutput, scenarioHash
    };
  }
  async function runStage(moduleId) {
    if (stageRunPending) return;
    stageRunPending = true;
    const content = byId("course-content");
    if (content) content.setAttribute("aria-busy", "true");
    try { await executeStage(moduleId); }
    finally {
      stageRunPending = false;
      if (content) content.removeAttribute("aria-busy");
    }
  }
  async function executeStage(moduleId) {
    const module = moduleById(moduleId);
    if (!module) { showCourseError(`Módulo desconhecido: ${moduleId}`); return; }
    const scenario = runtime.getScenario();
    ensureScenario(scenario.site, scenario.material, scenario.aswMax);
    const initial = state.overrides || defaultInitial(scenario.site, scenario.material, scenario.aswMax);
    const inputErrors = validateInitial(initial, scenario.aswMax);
    if (inputErrors.length) { showCourseError(inputErrors.join(" ")); return; }
    const errorNode = byId("course-error");
    if (errorNode) errorNode.textContent = "";
    const overrides = scenarioOverrides(scenario.site, scenario.material, scenario.aswMax);
    const output = runtime.runStage(moduleId, overrides);
    const scenarioRecord = runtime.describeScenario(overrides, moduleId);
    const scenarioHash = await sha256(scenarioRecord);
    const repeatOutput = moduleId === "D6" ? runtime.runStage(moduleId, overrides) : null;
    const checks = checkStage(moduleId, output, currentContext(output, repeatOutput, scenarioHash));
    state.lastRun = { moduleId, output, checks, scenarioHash, scenarioRecord, timestamp: new Date().toISOString() };
    if (checks.pass) state.completed[moduleId] = true;
    render();
    if (checks.pass && state.mode === "learn") {
      const index = MODULES.findIndex(item => item.id === moduleId);
      if (MODULES[index + 1]) state.moduleId = MODULES[index + 1].id;
      render();
    }
  }
  function csvFor(output) {
    const keys = ["age", "Wf", "Wr", "Ws", "N", "asw", "lai", "apar", "gpp", "npp", "transp", "fVPD", "fSW", "etaF", "etaS", "etaR", "mortInd"];
    return ["index;" + keys.join(";"), ...output.age.map((_, i) => [i, ...keys.map(key => Number.isFinite(output[key][i]) ? output[key][i] : "")].join(";"))].join("\n");
  }
  function climateCsv(climate) {
    const keys = ["year", "month", "tmp_min", "tmp_ave", "tmp_max", "prcp", "srad", "vpd_day", "frost_days"];
    return ["date;" + keys.slice(2).join(";"), ...climate.year.map((year, i) => [`${year}-${String(climate.month[i]).padStart(2, "0")}`, ...keys.slice(2).map(key => climate[key][i])].join(";"))].join("\n");
  }
  async function exportAudit() {
    if (!state.lastRun || state.lastRun.moduleId !== "D6") { throw new Error("Execute o estágio D6 antes de exportar o pacote de auditoria."); }
    const scenario = runtime.getScenario(), overrides = scenarioOverrides(scenario.site, scenario.material, scenario.aswMax);
    const climate = climateWithOverrides(scenario.site);
    const run = state.lastRun;
    const files = {
      "scenario.json": JSON.stringify({ ...run.scenarioRecord, scenario_hash: run.scenarioHash }, null, 2),
      "climate.csv": climateCsv(climate),
      "parameters.json": JSON.stringify({ material: scenario.material, parameters: runtime.data.materiais[scenario.material].params, provenance: "plataforma/dados_min.json; consultar modelo/caldeira_indianopolis.py para mapeamentos existentes e lacunas" }, null, 2),
      "results.csv": csvFor(run.output),
      "tests.json": JSON.stringify(run.checks, null, 2),
      "references.json": JSON.stringify(SOURCES, null, 2),
      "excel_audit_map.csv": ["scientific_id;python;excel;source;status",
        "state.wf;plataforma/modelo3pg.js;01_PARAMETROS!C33;modelo/caldeira_indianopolis.py;mapped",
        "state.wr;plataforma/modelo3pg.js;01_PARAMETROS!C35;modelo/caldeira_indianopolis.py;mapped",
        "state.ws;plataforma/modelo3pg.js;01_PARAMETROS!C34;modelo/caldeira_indianopolis.py;mapped",
        "state.n;plataforma/modelo3pg.js;01_PARAMETROS!C30;modelo/caldeira_indianopolis.py;mapped",
        "state.asw;plataforma/modelo3pg.js;01_PARAMETROS!C41;modelo/caldeira_indianopolis.py;mapped",
        ...EQUATIONS.filter(item => item.id.startsWith("eq.")).map(item => `${item.id};${item.implementation.replace(/;/g, ",")};Pendente;${item.source_ids.join(",")};pending`)].join("\n"),
      "version.json": JSON.stringify({ scientific_version: "3-PGpjs / r3PG v0.1.7", engine_version: "Akademia Modelo3PG", git_commit: root.AKADEMIA_BUILD_COMMIT || null, status: "pedagogical_and_operational_verification_only", timestamp: run.timestamp }, null, 2)
    };
    const hashes = {};
    for (const [name, content] of Object.entries(files)) hashes[name] = await sha256(content);
    const manifest = { scenario_hash: run.scenarioHash, scientific_version: "3-PGpjs / r3PG v0.1.7", engine_version: "Akademia Modelo3PG", git_commit: root.AKADEMIA_BUILD_COMMIT || null,
      equation_ids: EQUATIONS.filter(item => item.id.startsWith("eq.")).map(item => item.id), source_ids: SOURCES.map(source => source.id), tests: run.checks,
      scientific_status: "verificação operacional/pedagógica; não é validação científica independente", integrity: hashes, files: Object.keys(files) };
    files["manifest.json"] = JSON.stringify(manifest, null, 2);
    const bundle = JSON.stringify({ package_type: "akademia-3pg-audit-bundle", manifest, files }, null, 2);
    const blob = new Blob([bundle], { type: "application/json;charset=utf-8" }), url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url; a.download = `akademia-3pg-auditoria-${run.scenarioHash.slice(0, 12)}.json`; a.click(); URL.revokeObjectURL(url);
    const status = byId("audit-status"); if (status) status.textContent = "Pacote de auditoria JSON gerado.";
  }
  function answerTutor() {
    const query = byId("tutor-query").value.trim().toLocaleLowerCase("pt-BR");
    const matches = EQUATIONS.filter(item => `${item.id} ${item.name} ${item.description} ${item.inputs.join(" ")} ${item.outputs.join(" ")}`.toLocaleLowerCase("pt-BR").includes(query));
    const moduleMatches = MODULES.filter(item => `${item.id} ${item.title} ${item.have} ${item.add}`.toLocaleLowerCase("pt-BR").includes(query));
    const found = [...matches.map(item => `<article><b>${escapeHtml(item.id)} · ${escapeHtml(item.name)}</b><p>${escapeHtml(item.equation)}</p><p>Unidades: ${escapeHtml(item.units)}. Escopo: ${escapeHtml(item.scope)}.</p></article>`),
      ...moduleMatches.map(item => `<article><b>${escapeHtml(item.id)} · ${escapeHtml(item.title)}</b><p>${escapeHtml(item.explanation)}</p><p>Fonte: ${escapeHtml(item.source)}</p></article>`)];
    byId("tutor-answer").innerHTML = found.length ? found.join("") : "Não localizado nas fontes aprovadas.";
  }
  function setModule(id) {
    if (!moduleById(id)) return;
    if (state.mode === "learn") {
      const target = MODULES.findIndex(item => item.id === id), current = MODULES.findIndex(item => item.id === state.moduleId);
      if (target > current && !state.completed[state.moduleId]) return;
    }
    state.moduleId = id; state.tab = "learn"; render();
    const content = byId("course-content");
    if (content) content.scrollTop = 0;
  }
  function onClick(event) {
    const button = event.target.closest("button");
    if (!button) return;
    if (button.dataset.tab) { openTab(button.dataset.tab); return; }
    if (button.dataset.module) { setModule(button.dataset.module); return; }
    if (button.dataset.equation) { openTab("equations"); requestAnimationFrame(() => { const target = byId(`equation-${button.dataset.equation}`); if (target) { target.open = true; target.scrollIntoView({ block: "start" }); } }); return; }
    const action = button.dataset.action;
    if (action === "start-learning") { state.mode = "learn"; state.moduleId = "A"; openTab("learn"); }
    else if (action === "run-stage" || action === "run-current") { runStage(state.moduleId).catch(error => showCourseError(error.message)); }
    else if (action === "previous-module") { const i = MODULES.findIndex(item => item.id === state.moduleId); if (i > 0) setModule(MODULES[i - 1].id); }
    else if (action === "next-module") { const i = MODULES.findIndex(item => item.id === state.moduleId); if (state.completed[state.moduleId] && MODULES[i + 1]) setModule(MODULES[i + 1].id); }
    else if (action === "open-simulator") { byId("m-curso").hidden = true; byId("s-entradas").scrollIntoView({ block: "start" }); }
    else if (action === "save-baseline") {
      if (!state.lastRun || state.lastRun.moduleId !== "D6") { state.moduleId = "D6"; state.tab = "learn"; runStage("D6").catch(error => showCourseError(error.message)); return; }
      state.baseline = { scenario: state.lastRun.scenarioRecord, output: state.lastRun.output, scenarioHash: state.lastRun.scenarioHash };
      render();
    } else if (action === "compare") { if (state.lastRun && state.lastRun.moduleId === "D6") render(); }
    else if (action === "export-audit") { exportAudit().catch(error => { const status = byId("audit-status"); if (status) status.textContent = error.message; }); }
    else if (action === "ask-tutor") answerTutor();
  }
  function onChange(event) {
    const target = event.target;
    if (target.id === "course-mode") { state.mode = target.value; render(); return; }
    if (target.id === "course-year") { state.selectedYear = Number(target.value); render(); return; }
    if (target.dataset.initial) {
      const scenario = runtime.getScenario(); ensureScenario(scenario.site, scenario.material, scenario.aswMax);
      state.overrides[target.dataset.initial] = target.value === "" ? NaN : Number(target.value);
      const errors = validateInitial(state.overrides, scenario.aswMax);
      byId("initial-errors").textContent = errors.join(" ");
      if (!errors.length) { safeWrite(); runtime.refreshScenario(); }
      return;
    }
    if (target.dataset.climate) {
      const date = target.dataset.date, field = target.dataset.climate, value = Number(target.value);
      if (!Number.isFinite(value) || (field !== "tmp_min" && field !== "tmp_max" && value < 0)) { target.setCustomValidity("Informe um valor finito; os campos que não são temperatura devem ser não negativos."); target.reportValidity(); return; }
      target.setCustomValidity("");
      const changes = { ...(state.climateOverrides[date] || {}), [field]: value };
      const original = runtime.data.sitios[runtime.getScenario().site].clima;
      const index = original.year.findIndex((year, i) => `${year}-${String(original.month[i]).padStart(2, "0")}` === date);
      const tmin = changes.tmp_min ?? original.tmp_min[index], tmax = changes.tmp_max ?? original.tmp_max[index];
      if (tmin > tmax) { target.setCustomValidity("Tmin não pode superar Tmax."); target.reportValidity(); return; }
      state.climateOverrides[date] = changes;
      safeWrite(); runtime.refreshScenario(); render();
    }
    if (target.id === "explore-site" || target.id === "explore-material") {
      const current = runtime.getScenario();
      runtime.setScenario(target.id === "explore-site" ? { site: target.value } : { material: target.value });
      ensureScenario(runtime.getScenario().site, runtime.getScenario().material, runtime.getScenario().aswMax);
      runtime.refreshScenario();
      render();
    }
  }
  function init(config) {
    runtime = config;
    const saved = safeRead();
    state = { ...state, ...saved, completed: saved.completed || {}, climateOverrides: saved.climateOverrides || {} };
    if (!moduleById(state.moduleId)) state.moduleId = "A";
    if (!["learn", "explore"].includes(state.mode)) state.mode = "learn";
    ensureScenario(runtime.getScenario().site, runtime.getScenario().material, runtime.getScenario().aswMax);
    const modal = byId("m-curso");
    let opener = null;
    const close = () => {
      modal.hidden = true;
      if (opener && opener.isConnected) opener.focus();
    };
    byId("bt-curso").addEventListener("click", event => {
      opener = event.currentTarget;
      modal.hidden = false;
      render();
      byId("course-close").focus();
    });
    byId("course-close").addEventListener("click", close);
    modal.addEventListener("click", event => { if (event.target === modal) close(); });
    modal.addEventListener("keydown", event => {
      if (event.key !== "Tab") return;
      const focusable = [...modal.querySelectorAll('button:not(:disabled), select:not(:disabled), input:not(:disabled), summary, [tabindex]:not([tabindex="-1"])')];
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    document.addEventListener("keydown", event => { if (event.key === "Escape" && !modal.hidden) close(); });
    byId("course-nav").addEventListener("click", onClick);
    byId("course-content").addEventListener("click", onClick);
    byId("course-content").addEventListener("change", onChange);
    render();
  }
  api.init = init;
  api.invalidateRun = () => {
    if (!state.lastRun) return;
    state.lastRun = null;
    safeWrite();
  };
})(typeof window !== "undefined" ? window : globalThis);
