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

## Matriz de seis materiais — GERADA EM 21/11/2026
- **Gerado em 21/11/2026 (3ª passagem):** `experimentos/saida/possibilidades_6mat/possibilidades.csv` gerado executando script baseado em `possibilidades.py` com MATS=[“A1”,”C1”,”C2”,”C3”,”C4”,”C5”] e OUT=saida/possibilidades_6mat/. Parâmetros de C1–C5 de Borges (2009) em `clones.py`; parâmetros de compensação da calibração em `calibracao/saida/`.
- **Verificações realizadas:** total=22.752 (316 × 6 mat × 6 sit × 2 ver), aptos=20.856 (exclui 1.896 não aptos: DIAG IMP/A1, ALM/A1, ARA/A1 × 316 × 2 ver). Materiais: A1, C1, C2, C3, C4, C5. Sítios: ALM, ARA, ELD, IMP, IND, TB. Versões: original, calibrada. Colunas: 19 (idênticas ao CSV de 2 materiais).
- **Commit:** `d7ddca6`, branch `tcc-ii-auditoria-21nov`. Arquivo: 4,1 MB.
- **Desbloqueado:** seções 4.3 e 4.10 e Figura 10 do TCC confirmadas com os números 22.752 e 20.856 agora recalculáveis.
- Pendência remanescente: a menção a 1.848 cenários do Random Forest continua dependente de verificação de aptidão (item B7).

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

## Registro de auditoria — 2ª passagem (21/11/2026)

**Branch:** `tcc-ii-auditoria-21nov` a partir de `main` HEAD `985fe00` (merge do PR #4; estado equivalente ao `finalizacao-claude` mesclado).

**Correções aplicadas:**
- `entregavel_final/TCC_TEXTO_FINAL.md`: 12 ocorrências de `figuras_padronizadas/fig*.png` substituídas por `figuras/fig*.png` (caminho real das imagens). Auditado com `grep -c figuras_padronizadas` antes (12) e depois (0) da substituição.

**Verificações executadas:**
- Node.js: `/opt/node22/bin/node v22.23.5` — disponível nesta sessão (ausente na 1ª passagem de 19/11).
- Auditoria numérica: `python3 auditoria_final/auditar_numeros.py` → **528 itens; 528 conferem**. DataFrame vazio (zero falhas).
- Geração do DOCX: `python3 entregavel_final/gerar_tcc_ufu.py` → `entregavel_final/TCC_II_Bernardo_Castro_FINAL.docx` (3,1 MB). Sem erros de figura; fallback interno do gerador já resolvia `figuras/`; a correção no Markdown garante consistência documental.
- Geração do PDF: `soffice --headless --convert-to pdf TCC_II_Bernardo_Castro_FINAL.docx --outdir .` → `entregavel_final/TCC_II_Bernardo_Castro_FINAL.pdf` (2,2 MB).
- Figuras novas (N1/N2/N3 de `experimentos/figuras_novas.py`): **não executadas** nesta sessão (N2 requer `plataforma/material_tabelas.json`; pendente verificação de dependências).

**Matriz de seis materiais:** continua bloqueada. `experimentos/saida/possibilidades_6mat/possibilidades.csv` não existe no workspace nem no histórico Git. Somente a matriz de 2 materiais/5.688 cenários aptos está disponível. As seções 4.3 e 4.10 e a Figura 10 (20.856 cenários) permanecem como pendências científicas não resolvíveis sem o CSV original.

**Motor científico:** não alterado. `compensation=None` preservado; 57 testes continuam passando (confirmado na sessão anterior).
