# Pendências do TCC II (reorganizada em 20/11/2026)

Distinção adotada:
- **A. Dados de entrada:** obtidos e tratados quando disponíveis. Não condicionam a avaliação do modelo.
- **B. Avaliação do modelo:** feita com os dados disponíveis.
- **C. Confirmação empírica:** condicional. Só executada com inventários independentes compatíveis. Sem eles, registra-se a limitação; não há substituto bibliográfico tratado como validação.

## A. Dados de entrada
1. TECHS 22: a série meteorológica diária específica da parcela para 2012–2018 não está disponível publicamente, e não tivemos acesso a esses dados. Essa ausência é uma limitação de dados, não um download pendente. As simulações usam a série diária NASA POWER municipal de Telêmaco Borba, nas coordenadas −24,3239; −50,6158, de 2015 a 2024, versionada em `clima/power_api/POWER_daily_telemaco_borba_20150101_20241231.csv`.
2. TECHS 22: data de plantio, a confirmar no registro primário do TECHS (hoje: 29/02/2012 em metadados de dissertação).
3. Fonte para os oito parâmetros de *E. globulus* (kF, thinPower, mF, mR, mS, MinCond, Qa, Qb), ou decisão de substituí-los.

## B. Avaliação do modelo
1. MinCond: o cenário de 0,1 (ganho de 28,8% em IND) está reproduzível em `rodada_pendencias/sensibilidade_globulus_resumo.csv`. Decidir: manter como limitação documentada ou retirar o parâmetro. Não entra na análise principal.
2. Sensibilidade com faixas justificadas: a atual é exploratória. Refazer com faixas documentadas e cenários com desbaste.
3. Crosscheck r3PG em R: manter o resultado direto de 23.873 pares por variável e diferença relativa máxima de 5,288 × 10⁻¹⁵. Reexecutar o R somente com os mesmos dados e confirmar que o registro não depende de comparação mensal. Não alterar o modelo nem o limitador para mascarar divergências.
4. Efeito do VPD: refazer o teste com RH2M (a comparação municipal mostra diferença de −2,1 mbar em TB). Até lá, a conclusão vale só para o proxy usado.
5. Morris com faixas absolutas, após a decisão do item B1.
6. Random Forest: confirmar se o conjunto de 1.848 cenários da figura 6 inclui não aptos.

## C. Confirmação empírica (condicional)
1. Inventários independentes de TECHS 9 e 22 (DAP, altura, volume, idade, período), não usados na calibração. Só executada se disponíveis e compatíveis.
2. Dados de desfolha em campo com inventário repetido e área foliar. Não há no conjunto atual; a limitação é declarada.

## Registro
- Itens resolvidos (removidos): referência de Bertúlio; autores de Oliveira (2014); unidade dos volumes de Campo Verde; clones C2, C4 e C5; quadro de materiais; DOI do Matrangolo (10.1590/S0100-204X2010000900003); data de plantio do TECHS 9 (dez/2011, Almeida 2021); correção da equivalência com o r3PG no texto.

## Matriz de seis materiais
- Fonte e CSV estão no commit `fde2780` (`dados: matriz de seis materiais (22.752 cenários) e script que a gera`): `experimentos/possibilidades_6mat.py` e `experimentos/saida/possibilidades_6mat/possibilidades.csv`. O CSV tem 22.752 linhas, 20.856 aptas (10.428 por versão).
- A partir dos registros aptos e das fórmulas de `experimentos/figura_N3_6mat.py`, a conferência independente no CSV retornou: folhagem 51,5625%/93,1700% entre os 8.448 cenários com desfolha positiva por versão; NPP 9,0717%/27,3686% e volume 0,0192%/1,7261% entre os 10.428 cenários aptos por versão (original/calibrada). Os ganhos de volume calibrados são 180/10.428 = 1,7% no total apto e 180/8.448 = 2,1% condicionado à desfolha positiva; os dois ganhos originais são 2/10.428 = 0,02%.
- Seção 4.3 atualizada com os números desta matriz.
- Figura 10 (N3) regenerada da matriz verificada e copiada para o entregável; a conferência visual está registrada abaixo.
- **Pendente:** conferir a Figura 4 e a seção 4.5 com a matriz fatorial de solo de quatro materiais; ela não é a matriz completa de seis materiais desta revisão.
- A1 em IMP, ALM e ARA tem apenas cenários diagnósticos, pois f_T = 0. A seção 4.3 agora explicita essa exclusão e define IND, TB e ELD como o conjunto comum apto para comparar os seis materiais.

## Decisões desta rodada
- MinCond: retirado da análise; declarado como limite aceito no texto (seção 4.7). Valor 0 mantido.
- Título: "Simulação da perda de madeira por desfolha em eucalipto com o modelo 3-PG".

## Decisões tomadas (autor, 20/11/2026)
- MinCond retirado da análise principal e declarado como limite aceito (valor 0; efeito de 28,8% com 0,1 registrado como implausível).
- Título adotado: "Simulação da desfolha em plantios de *Eucalyptus* com o modelo 3-PG: efeito no crescimento e na produção de madeira".
- Repositório acessado: github.com/beteixeira135-cmyk/Akademia (clone funcionou nesta rodada). PROMPT_CLAUDE.md e handoff_claude/ não existem nele.

## Auditoria de finalização (21/11/2026)
- Branch confirmada: `finalizacao-claude`. Os dois arquivos da matriz não estavam no checkout inicial; após indicação do usuário, o commit remoto `fde2780` foi buscado e a branch local foi rebaseada sobre ele, sem merge ou push. O CSV foi contado e conferido diretamente.
- Conferência visual contra as legendas: `fig01_trajetoria_A1.png` (F1) — OK; `fig02_frequencia.png` (F3) — OK; `fig03_epoca.png` (F4) — OK; `fig07_morris.png` (F6) — OK. `fig09_biomas.png` (N2) — a legenda dizia “um local por bioma”, mas a imagem mostra seis sítios em cinco biomas, com dois sítios no Cerrado (Indianópolis e Imperatriz); texto e legenda foram corrigidos, sem alterar a imagem. `fig10_possibilidades.png` (N3) — regenerada da matriz verificada e copiada para `entregavel_final/figuras/`; a imagem mostra 10.428 cenários por versão e os valores arredondados 51,6%/93,2% para folhagem, 9,1%/27,4% para crescimento e 0,0%/1,7% para volume (original/calibrada; 0,0% é o arredondamento visual de 0,02% a uma casa decimal).
- Em `TCC_TEXTO_FINAL.md`, as buscas literais por `5.688` e `Lagartas` retornaram zero ocorrências. A legenda da Figura 10 já cita 20.856 cenários. O objetivo e a seção de confirmação empírica foram ajustados para não alegar comparação com inventários inexistentes; TECHS 9 foi descrito como referência regional próxima de Indianópolis, não como parcela equivalente. O gerador do DOCX também foi corrigido para ler esse texto e resolver as imagens existentes em `entregavel_final/figuras`.
- O gerador `experimentos/figura_N3_6mat.py` foi criado conforme o anexo; após instalar Python 3.12 e dependências no ambiente isolado da sessão, foi executado com sucesso. DOCX e PDF foram regenerados. O mapa do sumário foi produzido executando o bloco Python de `gerar_com_paginas.sh` com Poppler no Windows, pois Bash não está disponível. O PDF final tem 28 páginas.
- Verificação estrutural do DOCX: arquivo ZIP íntegro, 18 partes XML/XML-relacionadas parseáveis, 12 imagens e 28 entradas no sumário. O validador oficial referenciado pelo script (`/mnt/skills/public/docx/scripts/office/validate.py`) não está instalado neste ambiente; portanto, não se afirma “All validations PASSED!”.
- `ferramentas/gerar_passagem.py` foi executado com o Python do ambiente isolado, regenerando `PASSAGEM_DE_BASTAO.md` e `CONTEXTO_EMPACOTADO.md`. O envio ao Google Drive e o registro no Diário do TCC II não foram realizados nesta sessão.
- A Figura 10 foi atualizada com a matriz de seis materiais; as outras figuras não foram alteradas. Permanece pendente a validação oficial do DOCX. A série meteorológica específica da parcela TECHS 22 para 2012–2018 não está disponível publicamente, e não tivemos acesso a ela; a série municipal de TB usada nas simulações está disponível.
- Em 22/11/2026, a auditoria foi ampliada para conferir separadamente os denominadores da Figura 10, o conjunto comum apto de sítios, os quatro tratamentos de Matrangolo, os limites da distribuição da Figura 10 e a cobertura da série municipal de TB. A execução nesta revisão confirmou 580 verificações aprovadas.
- Em 22/11/2026, o texto revisado foi regenerado no DOCX. A auditoria ampliada confirmou 611/611 itens, incluindo os tratamentos mensais de Matrangolo, os denominadores da Figura 10, a aptidão comum dos sítios e a distribuição dos 180 ganhos calibrados. A série municipal de TB está versionada para 2015–2024 sem lacunas; a série específica da parcela TECHS 22 (2012–2018) não está disponível publicamente e não tivemos acesso a ela. A validação oficial do DOCX, atualização de PDF/sumário, envio ao Drive e registro no Diário seguem pendentes.
- Resolvido nesta revisão: seção 4.10 distingue os 8.448 cenários aptos com desfolha positiva dos 10.428 cenários aptos por versão. A Figura 4 e a seção 4.5 permanecem fora deste escopo e devem ser conferidas com a matriz fatorial de solo correspondente.
