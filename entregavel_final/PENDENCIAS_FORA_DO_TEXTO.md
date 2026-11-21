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

## Matriz de seis materiais — bloqueada por falta do arquivo fonte
- O arquivo solicitado `experimentos/saida/possibilidades_6mat/possibilidades.csv` não existe no workspace inspecionado e não está rastreado pelo Git. `git log --all --oneline --full-history -- experimentos/saida/possibilidades_6mat/possibilidades.csv` não retornou commits.
- O número “20.856” aparece no texto do commit `1997811` (`finalizacao: entregavel_final com DOCX UFU, texto-fonte, gerador e figuras`), mas isso não fornece a matriz nem permite recalcular os resultados. A busca `git log --all --oneline -S"20.856" -- entregavel_final/TCC_TEXTO_FINAL.md entregavel_final/PENDENCIAS_FORA_DO_TEXTO.md` encontrou somente esse commit.
- O único arquivo de possibilidades localizado no workspace é `experimentos/saida/possibilidades/possibilidades.csv`, em um diretório diferente. `Import-Csv` confirmou 7.584 linhas, 5.688 aptas, dois materiais (A1 e C5) e seis sítios (IND, TB, IMP, ALM, ARA e ELD); portanto, não corresponde à matriz alegada de seis materiais. Esses dados não comprovam os resultados novos. Não reconstruir nem substituir os dados ausentes.
- **Bloqueados até recuperar o CSV original e sua proveniência:** confirmar 22.752 cenários totais, 20.856 aptos, 10.428 por versão, os percentuais de recuperação/ganho atribuídos à matriz, as legendas e os dados da Figura 10. A figura não foi regenerada. A menção a 1.848 cenários do Random Forest continua pendente de verificação de aptidão, conforme item B7.

## Registro de auditoria desta etapa (21/11/2026)
- Branch criada a partir de `finalizacao-claude` limpa, no commit-base `199781183dd32c9bfe05985bcc25645e53cf6288`: `tcc-ii-finalizacao-auditoria`.
- Comandos: `git status --short --branch` confirmou `finalizacao-claude...origin/finalizacao-claude` sem alterações; `git log -1 --format="%H%n%h %s"` confirmou o commit-base; `git ls-files --error-unmatch experimentos/saida/possibilidades_6mat/possibilidades.csv` não encontrou o arquivo; buscas de histórico descritas acima; `Import-Csv` e o resumo JSON confirmaram as dimensões da saída antiga.
- `Test-Path` confirmou a ausência de `entregavel_final/TCC_II_Bernardo_Castro_FINAL.docx`, `entregavel_final/TCC_II_Bernardo_Castro_FINAL.pdf` e `entregavel_final/sumario.json`, bem como da figura no caminho `entregavel_final/figuras_padronizadas`; as imagens correspondentes existem em `entregavel_final/figuras`.
- `python3 ferramentas/pipeline.py verificar` não iniciou: o alias `python3` encaminha à Microsoft Store e não há interpretador Python instalado/disponível no PATH. Node.js e LibreOffice/soffice também não foram encontrados. DOCX, PDF e auditoria numérica não foram gerados. O `git diff --check` passou; a checagem de caminhos confirmou que todas as imagens referenciadas no manuscrito têm arquivo correspondente no caminho atual ou em `entregavel_final/figuras`.
- Correções independentes aplicadas nesta etapa: caminho de entrada do gerador para `TCC_TEXTO_FINAL.md` no diretório correto; resolução das figuras existentes em `entregavel_final/figuras`; descrição do TECHS 9 corrigida para não o tratar como parcela de Indianópolis; referências no texto à quantidade de materiais alinhadas às Tabelas 1 e 2. Nenhuma saída de cenário ou figura científica foi alterada e o motor científico não foi tocado.

## Decisões desta rodada
- MinCond: retirado da análise; declarado como limite aceito no texto (seção 4.7). Valor 0 mantido.
- Título: "Simulação da perda de madeira por desfolha em eucalipto com o modelo 3-PG".

## Decisões tomadas (autor, 20/11/2026)
- MinCond retirado da análise principal e declarado como limite aceito (valor 0; efeito de 28,8% com 0,1 registrado como implausível).
- Título adotado: "Simulação da desfolha em plantios de *Eucalyptus* com o modelo 3-PG: efeito no crescimento e na produção de madeira".
- Repositório acessado: github.com/beteixeira135-cmyk/Akademia (clone funcionou nesta rodada). PROMPT_CLAUDE.md e handoff_claude/ não existem nele.
