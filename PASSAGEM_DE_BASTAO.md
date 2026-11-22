# PASSAGEM DE BASTÃO — TCC II (10717 tokens, estimativa (caracteres ÷ 3,6); gerado em 22/11/2026 07:10)

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` (29721 tokens, estimativa (caracteres ÷ 3,6)).

# AGENTS.md — instruções para qualquer IA que trabalhe neste projeto (Claude, ChatGPT/Codex, Gemini, Cursor)

Projeto: TCC II de Bernardo Teixeira de Castro (Engenharia Florestal, UFU). Módulo de desfolha (pragas e doenças)
no modelo ecofisiológico 3-PG (r3PG v0.1.7, 3-PGpjs, porta Python verificada) para eucalipto. Defesa: dez/2026.

## Antes de qualquer coisa
1. Leia `memoria/contexto_ativo.md` (o que está sendo feito agora) e `memoria/progresso.md` (feito × falta).
2. Leia `PASSAGEM_DE_BASTAO.md` se existir (gerado por `python3 ferramentas/gerar_passagem.py`).
3. Revise os efeitos de `ferramentas/pipeline.py` antes de executá-lo. Na implementação atual, toda etapa bem-sucedida exceto `passagem` faz `git add -A`, cria commit e executa `git push origin HEAD:main`, inclusive `verificar`. Não rode o pipeline enquanto esse comportamento existir sem autorização explícita; faça verificações equivalentes diretamente e sem efeitos no Git.

## Regras inegociáveis
- Só dados secundários. NUNCA inventar dado, parâmetro, referência, DOI ou resultado. Sem fonte → escrever que não há.
- Distinguir verificação (código = equações), calibração (ajuste a dados) e validação (dados independentes).
- Todo número do TCC precisa ser recalculável: `auditoria_final/auditar_numeros.py` deve passar após qualquer mudança.
- O módulo original (v2) deve continuar reproduzível: `compensation=None` ⇒ resultados idênticos; testes em `modelo/testes`.
- Escrita: português do Brasil, estilo do TCC I, ABNT, frases claras e voz ativa.
- Tudo o que for entregue vai para o Google Drive, pasta 3-PG, com registro no Diário do TCC II.

## Ao terminar cada etapa
1. Atualize `memoria/contexto_ativo.md`, `memoria/progresso.md` e, se houve escolha, `memoria/decisoes.md`.
2. Rode `python3 ferramentas/gerar_passagem.py` (regenera PASSAGEM_DE_BASTAO.md e CONTEXTO_EMPACOTADO.md com contagem de tokens).
3. Faça commit com mensagem descritiva.

## Mapa
- `modelo/` 3-PG (threepg_pjs.py: v3 com compensação opcional) e testes.
- `experimentos/` matriz de simulações, indicadores, Random Forest, Morris, danos.
- `calibracao/` calibração bayesiana da compensação contra Bertulio et al. (2008).
- `biomas/` solo (SoilGrids + PTF-ZARC) e bioma (IBGE 2024) dos locais novos.
- `clima/power_api/` séries diárias NASA POWER.
- `tcc_docx/` texto (conteudo.js) e gerador do .docx (gerar.js).
- `auditoria_final/` auditoria dos números citados.
- `plataforma/` simulador web Akademia Florestal.
- `memoria/` banco de memória do projeto (padrão "memory bank").

---
# Projeto (estável)
- Autor: Bernardo Teixeira de Castro (UFU, Eng. Florestal). Orientador: Álvaro Augusto Vieira Soares. Coorientadora: Dra. Gabriela Cristina Costa Silva (UFRB). Banca: não definida (deixar em branco). Defesa: dezembro/2026.
- IC (frase do autor): a iniciação científica, ainda em andamento, foi a base; a partir dela auditamos, aprimoramos e corrigimos; a etapa atual é a calibração.
- Objetivo: estender o 3-PG com desfolha (e outros danos), simular intensidade, frequência e época em vários climas e solos, e quantificar o que pode e o que não pode ser afirmado sobre a validade biológica.
- Drive: pasta 3-PG https://drive.google.com/drive/folders/1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L (o link vai no Apêndice B).
- Plataforma: https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc
- O autor trabalha pelo celular.

---
# Contexto ativo
- Em 22/11/2026, foi corrigida a revisão do DOCX: a seção 4.13 explica a conversão mensal dos quatro tratamentos de Matrangolo e os resultados calibrados de 3,8%, 8,1%, 8,3% e 11,5%, com as limitações da comparação; a seção 4.10 distingue corretamente 8.448 cenários com desfolha e 10.428 cenários aptos; a seção 4.3 identifica os sítios comuns IND, TB e ELD e discrimina os 180 ganhos calibrados, inclusive o cenário máximo. A auditoria passou em 611/611 itens e o DOCX foi regenerado. Para TB, o modelo usa a série municipal NASA POWER de 2015–2024, sem lacunas; a série meteorológica específica da parcela TECHS 22 (2012–2018) não está disponível publicamente, e não tivemos acesso a ela. Não houve atualização do PDF, validação oficial do DOCX, upload ao Drive ou registro no Diário nesta etapa.
- A finalização foi integrada à `main` pelo PR #5; o PDF entregue tem 28 páginas. A matriz do commit `fde2780` tem 22.752 linhas e 20.856 aptas; os percentuais da Figura 10 são 51,6%/93,2%, 9,1%/27,4% e 0,02%/1,7%. O DOCX passou nas verificações estruturais (integridade ZIP, XML e 12 imagens), mas o validador oficial indicado no script não existe neste ambiente; não se afirma “All validations PASSED!”. A legenda da Figura 9 foi corrigida (seis sítios em cinco biomas, dois no Cerrado). A confirmação empírica por inventários independentes continua pendente. Google Drive/Diário não foram atualizados.
- Em 21/11/2026, o Google Drive foi autenticado para `beteixeira135@gmail.com`. Na pasta `3-PG/08 TCC II versão atual`, o PDF final foi atualizado em `TCC_II_Bernardo_Castro_FINAL_21-11-2026.pdf` (2.282.051 bytes) e o DOCX final foi enviado como `TCC_II_Bernardo_Castro_FINAL_21-11-2026.docx` (3.127.347 bytes). O Diário existente recebeu registro da entrega, da auditoria ampliada e da discrepância r3PG.
- Limitações estruturais avançadas por sensibilidade exploratória: criado `experimentos/sensibilidade_limitacoes.py` e saídas em `experimentos/saida/sensibilidade_limitacoes.csv`. Variação ±10% de γF1 mudou a perda em até 0,95 p.p.; mortalidade de 0 a 15% em até 4,30 p.p. Os oito parâmetros adaptados de E. globulus foram separados entre neutros/structurally inactive e perturbáveis. Isso reduz incerteza de leitura, mas não cria validação empírica nem substitui inventários.
- A validação automatizada ampliada ficou parcialmente bloqueada: o fixture externo `fontes_r3PG/data-raw/data.input.xlsx` não existe nesta sessão e `experimentos/saida/mensal.csv.gz` não está disponível. A sensibilidade das limitações foi compilada e executada; a auditoria cobriu todos os novos números decimais.
- Auditoria numérica atualizada em 21/11/2026: o check inválido baseado no merge mensal foi substituído por leitura direta de `experimentos/r_check/resultado_crosscheck.csv`. Foram 552 checagens, todas aprovadas. O crosscheck registra 23.873 pares por variável e diferença relativa máxima de 5,288160964744036e-15, abaixo do limite de 2e-13. O registro mensal que produzia RQEM de 64,6148% não está disponível nesta sessão e não é tratado como evidência atual.
- A integração de Google Drive não está disponível nesta sessão; não houve upload dos entregáveis nem registro no Diário do TCC II. A mudança de auditoria pós-PR ainda não foi enviada; não houve push para `main`.
- Em 21/11/2026, foi criada a skill Claude Code do projeto em `.claude/skills/akademia-tcc/SKILL.md`; `CLAUDE.md` orienta a lê-la antes de tarefas substantivas. A skill inclui evidências reproduzíveis, distinção entre verificação/calibração/validação e salvaguardas de dados e Git. O Claude Code CLI não está disponível nesta máquina; a estrutura foi validada estaticamente. Skill de repositório se aplica ao Claude Code; Claude.ai web/Desktop/Projects exigem habilitação separada.
- A instrução de executar `ferramentas/pipeline.py verificar` foi substituída em `AGENTS.md` e `CLAUDE.md`: o pipeline atualmente faz `git add -A`, commit e push para `HEAD:main` nas etapas bem-sucedidas, exceto `passagem`; não executar sem autorização explícita.
- Em 19/11, a revisão documental foi incorporada a `tcc_docx/conteudo.js`: Rua é precedente, não inovação; a contribuição é avaliar recuperação e perdas persistentes em condições brasileiras, com limites explícitos de transferência. Distinguir recuperação da área foliar, retomada do incremento e déficit de madeira.
- Os ganhos simulados acima do controle não têm causa biológica verificada. Não interpretar a inversão do indicador como benefício hídrico sem conferir fórmula, sinal, denominador e cenários pareados. Pizzi não foi recuperado na fonte primária; seus percentuais não foram incorporados.
- Busca de fontes públicas: Binkley et al. (2017) confirma TECHS 9 em Estrela do Sul (−18,73; −47,92), a cerca de 35 km de Indianópolis, e TECHS 22 em Telêmaco Borba. Portanto, o sítio 9 não fornece observações diretas de Indianópolis. Não localizei séries brutas de inventários para baixar. O artigo apresenta para A1/TECHS 22 produtividade agregada de lenho (34 Mg ha⁻¹ ano⁻¹ entre 24–36 meses) e IAF 3,8 aos 24 meses.
- Benchmark adaptado já calculado para A1/TECHS 22: o modelo produziu 37,06 Mg ha⁻¹ ano⁻¹ de lenho entre 24–36 meses (+9,0% sobre o valor publicado) e IAF 4,89 aos 24 meses, ante 3,8 publicados. A simulação usa clima NASA POWER nas coordenadas municipais e solo TECHS 22; o artigo não permite confirmar se essa observação participou do ajuste A1, então a independência não está demonstrada. A coluna IAF da tabela do TCC é a média simulada de 24–36 meses e não deve ser comparada como erro à observação pontual aos 24 meses. Tratar os dois resultados como benchmark adaptado, não validação.
- Limpeza concluída: versões antigas, snapshots e saídas anteriores foram removidos; o histórico Git mantém a rastreabilidade. O CSV de controles necessário à auditoria foi preservado em `auditoria_final/controles_solo_antes_correcao_dossel.csv`. O protótipo separado `plataforma/talhao_sorteado_3pg.html` foi mantido por oferecer uma interface 3D distinta.
- VS Code preparado com `.vscode/` e `requirements-calibracao.txt`; o ambiente `.venv` foi criado em Python 3.15 e as dependências foram instaladas.
- Reexecutadas com sucesso calibração C5, estimação de γ, validação cruzada interna, auditoria da calibração, testes adicionais, avaliação qualitativa de *E. globulus* e teste independente de Oliveira. Medianas: U = 1,18 (IC90% 1,01–1,34), a = 0,625 (0,225–0,975), γ = 1. A validação cruzada permanece dentro do experimento Bertulio; o teste Oliveira cobre a resposta em outro estudo, não valida persistência de longo prazo.
- VS Code usa `.vscode/` para preparar ambiente, recalcular calibração e executar as suítes. A fonte pública `trotsiuk/r3PG` está clonada na pasta irmã esperada; `experimentos/saida/mensal.csv.gz` foi regenerado localmente (ignorado pelo Git). As suítes do modelo e dos experimentos passaram: 57 testes.
- O validador DOCX oficial referido em `gerar_com_paginas.sh` não está disponível; as verificações estruturais anteriores não substituem a validação oficial.
- Próxima prioridade científica: obter os inventários e metadados de TECHS 9 e 22 para avaliação por variável e confirmar o subconjunto de dados usado no ajuste A1. A associação direta Indianópolis–TECHS 9 foi descartada; os rótulos S5–SA100 continuam sem correspondência verificada.

- Node.js 26.13.1 está instalado em `C:\Program Files\nodejs`; em processos PowerShell novos, incluir essa pasta no `PATH` para executar auditoria e geração do DOCX.

- Em 19/11/2026, a apresentação web voltou a executar: foi declarado `<!doctype html>`, `<html lang="pt-BR">`, UTF-8, `<head>` e `<body>`; o script que remove acentos passou de uma faixa Unicode mal codificada para `\p{M}`; a cena Three.js deixou de usar a propriedade incompatível `flatShading`. O simulador foi reconstruído e recarregado no navegador sem erros de JavaScript. Em um teste visual com desfolha de 95%, aos 24 meses, o talhão desfolhado mostrou W_F = 0,58 t ha^-1 contra 3,84 t ha^-1 no controle e volume = 48,38 m³ ha^-1 contra 55,83 m³ ha^-1 no controle.
- Em 21/11/2026, a versão textual entregue foi sincronizada com a revisão das limitações já feita em `tcc_docx/conteudo.js`: as referências Borzak et al. (2016), Eyles et al. (2009, 2016) e Firmino (2011) foram incorporadas ao texto de 4.14 e/ou à lista de referências; o DOI incorreto de Matrangolo foi corrigido para 10.1590/S0100-204X2010000900003. A redação separa reservas, persistência, sobrevivência, queda de folhada e confirmação empírica sem alterar números ou conclusões.
- Em 21/11/2026, a redação tabular removeu o termo “pulso” das tabelas principais: os calendários passaram a ser chamados ataque isolado, dois ataques e ataques anuais. Os números 5.688 e 20.856 permanecem distintos: o primeiro descreve danos combinados com dois materiais; o segundo, a matriz completa de seis materiais.
- Em 21/11/2026, o simulador deixou de mostrar “pulso/pulsos” nos rótulos visíveis e passou a usar “ataque isolado”, “dois ataques” e “ataques anuais”. `docs/index.html` e os arquivos-fonte foram reconstruídos. O pacote `handoff_claude/PROMPT_CLAUDE.md` recebeu instruções para diagramar o Material e Métodos como infográfico Notelm encadeado.
- Em 21/11/2026, ficou explícito no pacote de handoff que o Claude não deve criar clones Git nem repositórios paralelos: a tarefa deve ser realizada no checkout já disponibilizado pela sessão, preservando o repositório e usando uma branch de trabalho apropriada.
- Em 21/11/2026, foi preparado `handoff_claude/FLUXOGRAMAS_METODOS.md` com cinco fluxogramas do Material e Métodos e uma tabela de usos permitidos das referências. Os diagramas distinguem verificação, calibração, validação cruzada interna, comparação bibliográfica e confirmação empírica pendente.
- Em 21/11/2026, os cinco fluxogramas foram renderizados com Mermaid CLI para arquivos PNG e SVG em `handoff_claude/diagramas/`, acompanhados das fontes `.mmd`. As imagens foram conferidas visualmente e registradas no arquivo de handoff.
- Em 21/11/2026, o texto de verificação foi corrigido para não apresentar o RQEM mensal como crosscheck e passou a declarar o crosscheck direto disponível: 23.873 pares por variável e diferença relativa máxima de 5,288 × 10⁻¹⁵. A pendência duplicada foi reduzida a um único item de reexecução do R. Nenhum push foi realizado.
- Em 21/11/2026, os cinco fluxogramas do Material e Métodos foram incorporados ao texto do TCC e embutidos no DOCX nas seções 3.1, 3.4, 3.5 e 3.6. Arquitetura geral e ciclo mensal explicam o processo; cenários mostram intensidade, época e frequência; calibração/evidências separa verificação, validação cruzada interna e comparação adaptada; a escada de interpretação termina em confirmação empírica pendente. O DOCX final contém 17 imagens e o PDF 33 páginas. Auditoria numérica: 552/552 itens.
- Em 21/11/2026, o Fluxograma 2 foi convertido de ciclo vertical para leitura horizontal com três módulos: entradas, processo mensal e atualização/saída. Fonte PNG/SVG e `.mmd` foram atualizados, o DOCX foi regenerado e o PDF ficou com 31 páginas. A página 9 contém o diagrama completo e legível na largura da página; o DOCX contém 17 imagens e uma das mídias incorporadas corresponde exatamente ao PNG novo. Auditoria numérica: 552/552 itens.
- Em 22/11/2026, foi criado `.venv` local no worktree e instalado `python-docx`, NumPy, pandas e SciPy para executar a auditoria e regenerar o DOCX sem dependências do perfil global. A auditoria confirmou 552/552 itens. `entregavel_final/TCC_II_Bernardo_Castro_FINAL.docx` foi regenerado a partir de `gerar_tcc_ufu.py`; o ZIP passou na integridade, o documento abriu com 359 parágrafos, 5 tabelas, 2 seções e 17 imagens.

---
# Progresso
## Feito
- Em 22/11/2026, corrigida a revisão do DOCX com base na matriz versionada e nos scripts do repositório: 4.13 descreve a conversão mensal de Matrangolo e os quatro resultados simulados; 4.10 explica os denominadores distintos de recuperação foliar e volume; 4.3 identifica o conjunto comum apto (IND, TB, ELD) e detalha a distribuição dos 180 ganhos calibrados e o cenário máximo. A auditoria numérica passou em 611/611 itens; o DOCX foi regenerado e conferido estruturalmente, inclusive com a Figura 10 atualizada incorporada. Sem renderizador disponível, paginação do sumário e PDF não foram atualizados. A série climática municipal NASA POWER de TB cobre 2015–2024 sem lacunas; a série específica da parcela TECHS 22 (2012–2018) não está disponível publicamente e não tivemos acesso a ela. Google Drive e Diário não foram atualizados nesta etapa.
- Em 21/11/2026, renderizados cinco fluxogramas reais do Material e Métodos em PNG e SVG: arquitetura geral, ciclo mensal, cenários, calibração/evidências e escada de interpretação. Fontes Mermaid preservadas em `handoff_claude/diagramas/` e a lista vinculada em `handoff_claude/FLUXOGRAMAS_METODOS.md`.
- Em 21/11/2026, criado o pacote `handoff_claude/FLUXOGRAMAS_METODOS.md`: arquitetura geral, ciclo mensal do 3-PG, cenários de ataque, calibração/evidências e escada de interpretação. Incluída tabela que condiciona o uso das referências a comparação, benchmark ou limite do estudo.
- Em 21/11/2026, registrado no handoff e nas decisões que o Claude não precisa criar clones Git nem repositórios paralelos; ele deve usar o checkout já disponibilizado pela sessão.
- Em 21/11/2026, removidos os rótulos visíveis “pulso/pulsos” do simulador: fonte principal, conceitos, dados das tabelas e protótipo 3D passaram a usar “ataque isolado”, “dois ataques” e “ataques anuais”. `docs/index.html` foi reconstruído por `plataforma/construir.py`.
- Em 21/11/2026, `handoff_claude/PROMPT_CLAUDE.md` recebeu uma seção dedicada ao infográfico Notelm do Material e Métodos, com encadeamento objetivo → entradas → 3-PG → desfolha → cenários → calibração → simulações → metamodelo → indicadores → interpretação e distinções entre verificação, calibração, validação cruzada e confirmação empírica.
- Em 21/11/2026, substituídas em `tcc_docx/gerar.js`, no gerador de dados das tabelas e no JSON das tabelas as expressões “pulso único”, “dois pulsos” e “pulsos anuais” por “ataque isolado”, “dois ataques” e “ataques anuais”. Conferidos os arquivos JS e o JSON; não restou a palavra “pulso” nas fontes do TCC e a sintaxe passou em `node --check`.
- Em 21/11/2026, sincronizada a versão textual `entregavel_final/TCC_TEXTO_FINAL.md` com as nove referências já revisadas em `tcc_docx/conteudo.js`, corrigido o DOI de Matrangolo e adicionadas Borzak e Eyles às referências textuais. `conferir_referencias.js` confirmou 0 referências sem citação no objeto JavaScript; `conferir_texto_auditoria.js` confirmou 117 números decimais cobertos e 0 sem item. A auditoria numérica executada no ambiente disponível confirmou 551/552 itens e manteve a divergência RQEM r3PG como falha real.
- Revisão final integrada à `main` pelo PR #5. DOCX/PDF regenerados; PDF com 28 páginas. Matriz de seis materiais: 22.752 linhas, 20.856 aptas, 10.428 por versão. Percentuais da Figura 10 (original/calibrada): folhagem 51,6%/93,2%; NPP 9,1%/27,4%; volume 0,02%/1,7%. Figuras 1, 2, 3, 7, 9 e 10 conferidas; legenda da Figura 9 corrigida para seis sítios em cinco biomas. Em `TCC_TEXTO_FINAL.md`, `5.688` = 0, `Lagartas` = 0 e a legenda da Figura 10 cita 20.856 cenários. O DOCX passou verificações estruturais, mas o validador oficial indicado não está disponível; não se afirma “All validations PASSED!”. Google Drive e Diário não atualizados.
- Em 21/11/2026, o auditor passou a usar `experimentos/r_check/resultado_crosscheck.csv`: 552/552 checagens aprovadas, 23.873 pares por variável e diferença relativa máxima de 5,288160964744036e-15. A alegação de RQEM 64,6% foi retirada do texto; era produto de um merge mensal cuja saída não está disponível nesta sessão. O texto e a pendência foram alinhados sem alterar o motor.
- Google Drive autorizado em 21/11/2026 para `beteixeira135@gmail.com`. PDF atual atualizado e DOCX atual enviado à pasta `3-PG/08 TCC II versão atual`; ambos confirmados com tamanho e link no Drive. Registro atualizado no Diário do TCC II.
- Criada sensibilidade das limitações sem alterar o motor: ±10% em parâmetros adaptados de E. globulus, perda de folhada e mortalidade 0–15%. A análise quantificou amplitudes máximas de 0,95 p.p. para γF1 e 4,30 p.p. para mortalidade em IMP. kF, mF e MinCond são neutros/desligados na configuração testada. O TCC foi atualizado para distinguir esse exercício numérico de validação empírica.
- Validação ampliada parcialmente bloqueada por arquivos externos/saídas locais ausentes: `fontes_r3PG/data-raw/data.input.xlsx` e `experimentos/saida/mensal.csv.gz`. Compilação e execução da nova sensibilidade passaram; 117 números decimais do texto têm item na auditoria, restando apenas a divergência r3PG registrada.
- Criada a skill Claude Code versionada `.claude/skills/akademia-tcc/SKILL.md` e ligada ao `CLAUDE.md` para leitura em tarefas substantivas. `AGENTS.md` e `CLAUDE.md` agora alertam que o pipeline pode publicar em `main`.
- Verificados frontmatter e caminhos da skill e `git diff --check`. Não foi possível testá-la em uma sessão Claude Code porque o executável não está disponível. A passagem e o contexto empacotado foram regenerados com o Python isolado da sessão; o alias do sistema `python3` permanece indisponível.
- Revisão documental de recuperação, persistência, interpretação dos ganhos simulados e limites de transferência incorporada em `tcc_docx/conteudo.js`.
- Simulador Akademia: interface e módulos atuais preservados; diferença máxima JS–Python registrada em `1,60075e-13`, abaixo do limite do comparador (`1e-9`).
- Fixture da auditoria numérica movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`; caminho da auditoria atualizado.
- Removidos snapshots do TCC, versões antigas de fontes e modelos, protótipos da plataforma substituídos e saídas antigas de experimentos/calibração. O histórico Git preserva versões anteriores; o protótipo 3D `plataforma/talhao_sorteado_3pg.html` foi mantido por ser uma interface distinta.
- `py -3 plataforma/construir.py` concluiu; a página `plataforma/docs/index.html` foi reconstruída. `git diff --check` e `git diff --cached --check` passaram.
- Workspace VS Code configurado em `.vscode/`, dependências da calibração fixadas em `requirements-calibracao.txt` e ambiente `.venv` instalado.
- Reexecutada a calibração atual: U mediana 1,18 (IC90% 1,01–1,34), a mediana 0,625 (0,225–0,975), γ = 1. LOO no mesmo experimento: RQEM 15,72 → 4,31 p.p.; teste entre materiais no mesmo estudo: C5→A1 19,08 → 8,41 e A1→C5 13,01 → 4,30 p.p. Teste independente Oliveira: perda de volume observada 35,4%, mediana calibrada 33,0% (IC90% 28,1–45,8%).
- A fonte pública r3PG foi clonada na pasta irmã esperada; a matriz mensal foi regenerada localmente. Suítes do modelo e dos experimentos: 57 testes aprovados.
- Busca documental pública confirmou os locais TECHS 9 (Estrela do Sul; aproximadamente 35 km de Indianópolis) e 22 (Telêmaco Borba). Binkley et al. (2017) fornece metadados de sítio e resultados agregados de meia rotação, mas não localizei os inventários brutos para download na página do IPEF nem nas buscas em repositórios consultados. Site 9 é apenas referência próxima para Indianópolis, não validação direta.
- Benchmark adaptado executado para A1 no TECHS 22 com as saídas sem desfolha já calculadas: incremento de lenho simulado 37,06 contra 34 Mg ha⁻¹ ano⁻¹ publicado (+9,0%); IAF simulado aos 24 meses 4,89 contra 3,8 publicado. A segunda comparação é pontual aos 24 meses; a tabela do TCC reporta média simulada de 24–36 meses. Clima municipal e solo do sítio são usados; sobreposição com dados de ajuste A1 não confirmada, portanto não é validação independente.
- As alterações pós-integração na auditoria estão locais na branch `finalizacao-claude`; ainda não foram publicadas em novo PR.
- Em 19/11/2026, corrigidos UTF-8, estrutura HTML e um erro de expressão regular que impedia a execução dos scripts da página. Corrigida também uma propriedade de material incompatível na cena Three.js. `plataforma/construir.py` regenerou o simulador e `docs/index.html`; o navegador abriu a cena 3D, confirmou `charset=UTF-8`, `lang=pt-BR`, `R` e `renderer` ativos e não registrou erro de JavaScript. A desfolha visual passou a ser refletida diretamente por folhas menores e o evento mensal, em conjunto com os números do modelo.

## Falta
1. Investigar a discrepância de RQEM entre o motor Python e o r3PG em R, sem ajustar o modelo para contornar o auditor.
2. Obter o validador DOCX indicado em `gerar_com_paginas.sh` e executar a validação oficial; o arquivo não existe neste ambiente.
3. Solicitar ou obter inventários e metadados TECHS 9 e 22 e confirmar quais observações entraram no ajuste A1; então avaliar por variável. O benchmark agregado do TECHS 22 não constitui reprodução estrita nem validação empírica.
4. Configurar acesso aprovado ao Google Drive e ao Diário do TCC II para entregar os arquivos e registrar a etapa.
5. Confirmar se a auditoria pós-PR deve ser publicada em um PR de acompanhamento; preservar a falha de RQEM enquanto sua origem não for investigada.

- Em 21/11/2026, fechada nesta sessão a correção da alegação r3PG: auditor ajustado ao crosscheck direto, 552/552 checagens aprovadas e uma única pendência de reexecução do R. Nenhum arquivo foi enviado ao Google Drive ou registrado no Diário nesta sessão.
- Em 21/11/2026, incorporados ao `TCC_TEXTO_FINAL.md` e ao DOCX final os fluxogramas 1–5 dos diagramas em `handoff_claude/diagramas/`. O PDF foi regenerado em 33 páginas. Verificação estrutural confirmou cinco legendas dos fluxogramas e 17 imagens no DOCX; `git diff --check` passou e a auditoria numérica confirmou 552/552 itens.
- Em 21/11/2026, o Fluxograma 2 foi fechado em leitura horizontal, com três módulos encadeados. `02-ciclo-mensal.mmd`, `.png` e `.svg` foram atualizados; o DOCX foi regenerado sem cortes e o PDF foi convertido com 31 páginas. Inspeção visual da página 9 confirmou o diagrama completo; o arquivo DOCX possui 17 imagens e contém o novo PNG por SHA-256 equivalente. A reorganização do Drive continua pendente de confirmação por postcondição.
- Em 22/11/2026, a auditoria numérica foi executada no ambiente virtual local e aprovou 552/552 itens. O DOCX final foi regenerado em `entregavel_final/TCC_II_Bernardo_Castro_FINAL.docx`, com integridade ZIP confirmada e 17 imagens incorporadas. Não houve regeneração de PDF nesta etapa e não houve upload ao Google Drive nem registro no Diário.

---
## Calibração (lido de calibracao/saida/calibracao_d0999.json)
- U: mediana 1.18 (IC90% 1.01–1.34); a: mediana 0.625 (IC90% 0.225–0.975).
- Ajuste C5 — observado: CAP 24.2, altura 19.1, volume 52.9 | original: volume 66.6, CAP 29.7, altura 36.1 | calibrado: volume 50.9, CAP 20.5, altura 25.2.
- Teste A1/urocam (mesmo experimento; não é validação independente) — observado: volume 59.0, CAP 22.9 | original: volume 79.3, CAP 40.7 | calibrado: volume 66.5, CAP 30.6 (IC90% volume 59.6, CAP 25.9 a volume 76.9, CAP 38.4).

---
# Registro de decisões (mais recente no fim)
- 30/10: ampliar de Indianópolis para 3 locais; solo local do TECHS onde houver; FR em níveis ordinais.
- 31/10: incluir outros danos (eficiência, mortalidade) com fontes.
- 31/10: plataforma acessível a não especialistas (conceitos, modo explicar, cubagem, taper com Souza et al., 2016).
- 31/10: fazer calibração de verdade ("trabalhoso, defendo fácil"): compensação v3 calibrada contra Bertulio et al. (2008), urograndis (C5); teste com urocam (A1).
- 31/10: um local por bioma onde há eucalipto: Almeirim-PA (Amazônia), Araripina-PE (Caatinga), Eldorado do Sul-RS (Pampa); Pantanal excluído (sem plantio comercial; 3-PG não representa alagamento). Imperatriz é Cerrado (IBGE 2024).
- 31/10: mecanizar o ambiente: AGENTS.md, banco de memória, pipeline único e passagem de bastão gerada automaticamente; GitHub como fonte da verdade quando a conta for conectada.
- 31/10: Missão 07 — auditoria integrada. Parecer B. Recomendação aos orientadores: discutir γ (literatura indica ≈ 1) e o domínio de uso (sem desfolha total no 1º ano).
- 31/10: diferenciar a plataforma do 3PG.d (Rua et al., 2020) sem alegar pioneirismo: incerteza propagada, compensação calibrada, outros danos, perda por produto e domínio de validade explícito. A comparação usa só a descrição pública do 3PG.d.
- 31/10: comprovar com validação cruzada: LOO (k=5) e por clone (k=2) na calibração (dado real, mesmo experimento) e k-fold do metamodelo no espaço de possibilidades (mede regularidade do modelo, não acerto em campo).
- 01/11: o autor pediu um TCC realista: corpo enxuto (~19 p.), detalhes nos apêndices e no pacote; nenhum resultado removido do trabalho, só do corpo.
- 01/11: TCC para qualquer leitor entender; gráficos no TCC, tabelas densas replicadas no 'Material do TCC' da Akademia; quadros com QR code levam à plataforma. Sem apêndice de plataforma nem de resultados complementares.
- 02/11: γ deixa de ser escolha (0,5) e passa a ser calibrado com experimento independente (Quentin et al., 2011): γ = 1; U e a recalibrados com γ fixo. Oliveira et al. (2014) usado só como teste independente, nunca no ajuste. Krause 2025 e Kautz 2018 fora da tabela de precedentes (conteúdo não conferido).
- 02/11 (tarde): cascata "sem falhas escondidas". (1) Dossel dos clones de Borges corrigido: γF1, γF0 e pFS2 trocados pelos da TECHS (Caldeira et al., 2020a), porque os de Borges davam IAF 8–11 contra 3,0–3,8 medidos; TCC_DOSSEL=borges reproduz a versão anterior. (2) U só no mês do ataque (u_meses = 1; Turnbull et al., 2007; Quentin et al., 2012): as regras testadas deram ajuste equivalente, escolhida a sustentada pela fisiologia; em desfolha total o U não é identificado e vem da faixa da literatura. (3) Matriz principal fixada nos 3 locais (SITIOS_MATRIZ), pois passara a ler os 6 locais. (4) Tabelas completas geradas dos resultados (tcc_docx/tabelas_dados.py), sem números digitados. (5) Auditoria numérica com fixture reproduzível; o controle anterior à correção do dossel foi movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`. (6) Pipeline com todas as etapas (calibração completa, biomas, possibilidades, tabelas, plataforma).
- 19/11: repetição de desfolhas não será apresentada como inovação frente a Rua et al. (2020); a contribuição é avaliar recuperação e perdas persistentes em condições brasileiras, com limites explícitos de transferência entre materiais. Recuperação da área foliar, retomada do incremento e déficit de madeira são dimensões diferentes. Perda negativa significa apenas resultado simulado acima do controle segundo a fórmula pareada; não atribuir causa hídrica sem evidência. Não importar percentuais de Pizzi até recuperar e conferir a fonte primária. Binkley et al. (2017) localiza TECHS 9 em Estrela do Sul, a cerca de 35 km de Indianópolis, e TECHS 22 em Telêmaco Borba; não tratar Indianópolis como sítio TECHS 9. Os rótulos S5–SA100 seguem sem correspondência verificada.
- 19/11: preparar execução no VS Code com `.venv` e tarefas que chamam diretamente os scripts de calibração. Não usar `ferramentas/pipeline.py` para essas tarefas: ele faz commit e tenta enviar `HEAD:main`. A calibração LOO e por material é validação cruzada no mesmo experimento; Oliveira et al. (2014) é o teste em estudo independente disponível, limitado ao horizonte observado.
- 19/11: não tratar Indianópolis como TECHS 9. Binkley et al. (2017) localiza o sítio 9 em Estrela do Sul, a ~35 km; o valor de solo é uma referência próxima. O resultado agregado de A1/TECHS 22 pode ser usado como benchmark adaptado, com diferenças de clima/coordenadas e sem independência demonstrada em relação ao ajuste A1; não chamar de validação empírica. A IAF publicada é aos 24 meses e não é diretamente comparável à média simulada de 24–36 meses. Solicitar dados e metadados para avaliação por variável.
- 19/11/2026: manter `plataforma/fonte2.html` como fonte única de estrutura/visualização e `plataforma/construir.py` para regenerar o simulador e `docs/index.html`. Corrigir problemas de codificação e execução na fonte, não só nos arquivos gerados. Na cena 3D, a copa do talhão desfolhado deve diminuir pela biomassa foliar mensal do modelo e o dano deve marcar também a passagem dos eventos; o resultado visual é ilustrativo e não substitui as métricas científicas.
- 21/11/2026: adotar formato híbrido para a orientação do Claude no Akademia: skill Claude Code de projeto para procedimentos aprofundados e referência obrigatória no `CLAUDE.md` para tarefas substantivas. O `AGENTS.md` e o `CLAUDE.md` avisam que o pipeline pode commitar e enviar `HEAD:main`; não o executar sem autorização explícita. A skill versionada não se aplica automaticamente ao Claude.ai web/Desktop/Projects.
- Auditoria pós-PR: não truncar RQEM/R² para transformar limites em igualdade; registrar a divergência r3PG como falha real até investigar sua origem. Não alterar o modelo para fazer o auditor passar.
- Entrega ao Google Drive em 21/11/2026: preservar o PDF existente pelo mesmo ID, atualizando o conteúdo local atual, e enviar o DOCX atual como arquivo novo datado. Registrar links e limitações no Diário do TCC II.
- Limitações: não substituir dados de campo por sensibilidades; usar perturbações ±10% apenas como exercícios exploratórios de robustez e manter 4.15 explícita como condições para confirmação empírica futura.
- 21/11/2026: integrar as nove referências ao texto por fatos verificáveis e sem chamar comparações bibliográficas de validação. Matrangolo, Oliveira e o benchmark TECHS permanecem comparações adaptadas; Caldeira valida crescimento sem desfolha; reservas, lignotúber, queda de folhada e persistência plural anual são tratadas como limites ou dados de espécies/sítios não equivalentes.
- 21/11/2026: usar linguagem direta para os calendários de desfolha nas tabelas e legendas. “Ataque isolado” substitui “pulso único”, “dois ataques” substitui “dois pulsos” e “ataques anuais” substitui “pulsos anuais”.
- 21/11/2026: o Material e Métodos do TCC terá instrução específica para o Claude construir uma explicação em formato de infográfico Notelm: encadeamento visual objetivo → dados e locais → 3-PG → desfolha → cenários → calibração → simulações → metamodelo → indicadores → interpretação. O simulador não deve usar “pulso/pulsos” em rótulos visíveis.
- 21/11/2026: o Claude não precisa nem deve criar clones Git desta tarefa. O trabalho deve começar no checkout já disponibilizado pela sessão, preservando o repositório existente e usando uma branch de trabalho apropriada, sem inicializar ou duplicar o projeto em diretórios paralelos.
- 21/11/2026: preparar no handoff cinco fluxogramas do Material e Métodos em formato Mermaid: arquitetura geral, ciclo mensal, construção dos cenários, calibração/evidências e escada de interpretação. A tabela de referências limita cada uso à evidência disponível e mantém pendentes inventários, metadados TECHS e confirmação empírica independente.
- 21/11/2026: manter em `handoff_claude/diagramas/` as fontes Mermaid auditáveis e exportações PNG/SVG dos cinco fluxogramas. As imagens acompanham a distinção científica entre verificação, calibração, comparação bibliográfica e confirmação empírica pendente.
- 21/11/2026: fechar a regeneração local do DOCX/PDF completo nesta branch sem publicar ou mascarar divergências. Preservar o crosscheck direto de r3PG e declarar explicitamente que o validador oficial DOCX continua indisponível.
- 21/11/2026: corrigir o auditor para ler `experimentos/r_check/resultado_crosscheck.csv`, com 23.873 pares por variável e limite de diferença relativa de 2e-13. Não usar o merge mensal como RQEM sem saída disponível.
- 21/11/2026: incorporar ao corpo do TCC os cinco fluxogramas reais do Material e Métodos, posicionados nas seções pertinentes. Os nomes visíveis seguem “ataque isolado”, “dois ataques” e “ataques anuais”; a cadeia mantém distinção entre verificação, calibração, comparação bibliográfica e confirmação empírica pendente.
- 21/11/2026: apresentar o Fluxograma 2 como leitura horizontal em três módulos (“Entradas do mês”, “Processo mensal” e “Atualização e saída”), preservando o ciclo visual de retorno ao próximo mês. Não considerar a reorganização do Google Drive concluída sem confirmação direta da pasta 10 e da pasta de referências.
- 22/11/2026: usar o `.venv` local do worktree para auditoria e geração do DOCX, mantendo `.venv` fora do Git e sem alterar o motor científico ou publicar em `main`.

---
# Contexto técnico
- Python 3.11+ (numpy, pandas, scikit-learn, SALib opcional); Node 18+ com `docx` para gerar o TCC; LibreOffice para PDF.
- Modelo: `modelo/threepg_pjs.py`, `run_3pg_pjs(site, species, climate, params, defoliation_events=, efficiency_events=, mortality_events=, compensation=)`.
  - v1/v2: desfolha W_F·(1−d) no início do mês; perda de eficiência α·(1−r); mortalidade N·(1−m).
  - v3 (compensação, opcional): enquanto W_F < W_F,ref: U_ef = 1+(U−1)·f_SW sobre α; condutância ×(gC_ref/gC)^γ (teto 1/(1−0,45)); partição η_F' = η_F + a·déficit·(η_S+η_R).
- Convenção temporal: plantio 2015-01; A1 começa aos 12 meses (2016-01), materiais de Borges aos 3 (2015-04); fim 2023-01; "k" = mês da simulação de referência; rotação = k72 (84 meses de idade).
- Materiais: A1 (Caldeira et al., 2020); C5, C2, C4 (Borges, 2009). A1 em Imperatriz, Almeirim e Araripina = diagnóstico (f_T = 0 em vários meses).
- Locais: IND, TB, IMP (originais); ALM (Amazônia), ARA (Caatinga), ELD (Pampa). Bioma: IBGE 2024 (`biomas/bioma2024.csv`).

---
## Últimos commits
- 22/11 07:06 docs: corrigir revisÃ£o final do TCC
- 22/11 04:55 Finalizar DOCX do TCC II
- 22/11 04:11 Merge pull request #9 from beteixeira135-cmyk/finalizacao-secao-3-8
- 22/11 07:11 tcc: secao 3.8 trajetoria metodologica e reutilizacao; Quadro 2 de evidencias; DOCX e PDF regenerados a partir da main
- 21/11 19:35 Merge pull request #8 from beteixeira135-cmyk/finalizacao-claude
- 21/11 18:26 Corrige leitura horizontal do Fluxograma 2
- 21/11 17:27 incorpora fluxogramas ao TCC final
- 21/11 17:22 corrige crosscheck r3PG no TCC final
- 21/11 17:11 docs: renderizar fluxogramas do metodo
- 21/11 17:07 docs: adicionar fluxogramas do Material e Metodos
- 21/11 16:58 Merge remote-tracking branch 'origin/main' into finalizacao-claude
- 21/11 16:56 docs: informar Claude para nao criar clones
- 21/11 16:52 docs: orientar infografico do metodo e retirar pulso do simulador
- 21/11 16:46 docs: reescrever tabelas em linguagem direta
- 21/11 16:37 docs: integrar referencias das limitacoes do TCC

## Para a IA que continuar
1. Sem execução de código: redija o texto, marcando [CONFERIR] em números ainda não gerados. Nunca invente resultados.
2. Com código: siga "Falta (em ordem)" e rode `python3 ferramentas/pipeline.py <etapa>`.
3. Ao fim de cada passo: atualize `memoria/`, rode este gerador e faça commit.
