# Pendências do TCC II (reorganizada em 20/11/2026)

Distinção adotada:
- **A. Dados de entrada:** obtidos e tratados quando disponíveis. Não condicionam a avaliação do modelo.
- **B. Avaliação do modelo:** feita com os dados disponíveis.
- **C. Confirmação empírica:** condicional. Só executada com inventários independentes compatíveis. Sem eles, registra-se a limitação; não há substituto bibliográfico tratado como validação.

## A. Dados de entrada
1. TECHS 22: série diária NASA POWER (coordenadas −24,2 e −50,5; 2012–2018) e tratamento mensal, com VPD calculado com RH2M. Script `auditoria_final/baixar_clima_techs_power.py` pronto; download pendente (API inacessível no ambiente de execução).
2. TECHS 22: data de plantio, a confirmar no registro primário do TECHS (hoje: 29/02/2012 em metadados de dissertação).
3. Fonte para os oito parâmetros de *E. globulus* (kF, thinPower, mF, mR, mS, MinCond, Qa, Qb), ou decisão de substituí-los.

## B. Avaliação do modelo
1. MinCond: o cenário de 0,1 (ganho de 28,8% em IND) está reproduzível em `rodada_pendencias/sensibilidade_globulus_resumo.csv`. Decidir: manter como limitação documentada ou retirar o parâmetro. Não entra na análise principal.
2. Sensibilidade com faixas justificadas: a atual é exploratória. Refazer com faixas documentadas e cenários com desbaste.
3. Divergência do motor Python com o r3PG em R (RQEM máximo de 64,6% por registro, em biomassa foliar e IAF): investigar a origem antes de qualquer alegação de equivalência.
4. Auditor numérico: adotar a versão corrigida (`correcao_auditor.diff`), que não trunca os critérios. Estado: 527/528, com a falha do RQEM r3PG.
5. Efeito do VPD: refazer o teste com RH2M (a comparação municipal mostra diferença de −2,1 mbar em TB). Até lá, a conclusão vale só para o proxy usado.
6. Morris com faixas absolutas, após a decisão do item B1.
7. Random Forest: confirmar se o conjunto de 1.848 cenários da figura 6 inclui não aptos.

## C. Confirmação empírica (condicional)
1. Inventários independentes de TECHS 9 e 22 (DAP, altura, volume, idade, período), não usados na calibração. Só executada se disponíveis e compatíveis.
2. Dados de desfolha em campo com inventário repetido e área foliar. Não há no conjunto atual; a limitação é declarada.

## Registro
- Itens resolvidos (removidos): referência de Bertúlio; autores de Oliveira (2014); unidade dos volumes de Campo Verde; clones C2, C4 e C5; quadro de materiais; DOI do Matrangolo (10.1590/S1678-3921.pab2010.v45.8460); data de plantio do TECHS 9 (dez/2011, Almeida 2021); correção da equivalência com o r3PG no texto.

## Matriz de seis materiais (executada nesta rodada)
- Saída: `experimentos/saida/possibilidades_6mat/possibilidades.csv` (22.752 linhas); cópia em `fechamento_tcc/possibilidades_6materiais.csv`. Script: `experimentos/possibilidades_6mat.py`.
- Seção 4.3 atualizada com os números desta matriz.
- **Pendente:** Figura 10 (N3) e sua legenda ainda usam a matriz antiga de A1 e C5 (5.688 aptos); precisam ser regeradas a partir de `possibilidades_6mat`.
- **Pendente:** Figura 4 e a discussão da seção 4.10 e 4.5 ainda citam os números antigos; revisar com a matriz nova.
- **Pendente:** A1 não tem cenários em ALM e ARA; declarar em toda comparação entre materiais.

## Decisões desta rodada
- MinCond: retirado da análise; declarado como limite aceito no texto (seção 4.7). Valor 0 mantido.
- Título: "Simulação da perda de madeira por desfolha em eucalipto com o modelo 3-PG".

## Decisões tomadas (autor, 20/11/2026)
- MinCond retirado da análise principal e declarado como limite aceito (valor 0; efeito de 28,8% com 0,1 registrado como implausível).
- Título adotado: "Simulação da desfolha em plantios de *Eucalyptus* com o modelo 3-PG: efeito no crescimento e na produção de madeira".
- Repositório acessado: github.com/beteixeira135-cmyk/Akademia (clone funcionou nesta rodada). PROMPT_CLAUDE.md e handoff_claude/ não existem nele.
