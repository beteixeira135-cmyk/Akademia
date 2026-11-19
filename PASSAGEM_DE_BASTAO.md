# PASSAGEM DE BASTÃO — TCC II (3807 tokens, estimativa (caracteres ÷ 3,6); gerado em 19/11/2026 10:37)

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` (22692 tokens, estimativa (caracteres ÷ 3,6)).

# AGENTS.md — instruções para qualquer IA que trabalhe neste projeto (Claude, ChatGPT/Codex, Gemini, Cursor)

Projeto: TCC II de Bernardo Teixeira de Castro (Engenharia Florestal, UFU). Módulo de desfolha (pragas e doenças)
no modelo ecofisiológico 3-PG (r3PG v0.1.7, 3-PGpjs, porta Python verificada) para eucalipto. Defesa: dez/2026.

## Antes de qualquer coisa
1. Leia `memoria/contexto_ativo.md` (o que está sendo feito agora) e `memoria/progresso.md` (feito × falta).
2. Leia `PASSAGEM_DE_BASTAO.md` se existir (gerado por `python3 ferramentas/gerar_passagem.py`).
3. Rode `python3 ferramentas/pipeline.py verificar` para conferir que o ambiente funciona.

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
- Em 19/11, a revisão documental foi incorporada a `tcc_docx/conteudo.js`: Rua é precedente, não inovação; a contribuição é avaliar recuperação e perdas persistentes em condições brasileiras, com limites explícitos de transferência. Distinguir recuperação da área foliar, retomada do incremento e déficit de madeira.
- Os ganhos simulados acima do controle não têm causa biológica verificada. Não interpretar a inversão do indicador como benefício hídrico sem conferir fórmula, sinal, denominador e cenários pareados. Pizzi não foi recuperado na fonte primária; seus percentuais não foram incorporados.
- Próxima prioridade científica: rodar o crescimento sem desfolha nos alvos TECHS 9 e 22, após confirmar sítio, coordenadas, material, idades, unidades e inventários. Telêmaco Borba–sítio 22 tem apoio em Binkley et al. (2017); Indianópolis–sítio 9 e os rótulos S5–SA100 permanecem não verificados.
- Limpeza concluída: versões antigas, snapshots e saídas anteriores foram removidos; o histórico Git mantém a rastreabilidade. O CSV de controles necessário à auditoria foi preservado em `auditoria_final/controles_solo_antes_correcao_dossel.csv`. O protótipo separado `plataforma/talhao_sorteado_3pg.html` foi mantido por oferecer uma interface 3D distinta.
- A página da Akademia foi reconstruída com `py -3 plataforma/construir.py`. `pipeline.py verificar` falhou em 19/11 porque o Python 3.15 disponível não tem `numpy`; `pandas` e `sklearn` também não estão instalados. `node` não está no PATH. Auditoria numérica, testes e geração do DOCX permanecem pendentes até resolver as dependências.

- FALHA na etapa `verificar` (19/11 10:35): comando `C:\Users\aluno\AppData\Local\Programs\Python\Python315\python.exe -c import numpy, pandas, sklearn; print('python ok')`.

---
# Progresso
## Feito
- Revisão documental de recuperação, persistência, interpretação dos ganhos simulados e limites de transferência incorporada em `tcc_docx/conteudo.js`.
- Simulador Akademia: interface e módulos atuais preservados; diferença máxima JS–Python registrada em `1,60075e-13`, abaixo do limite do comparador (`1e-9`).
- Fixture da auditoria numérica movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`; caminho da auditoria atualizado.
- Removidos snapshots do TCC, versões antigas de fontes e modelos, protótipos da plataforma substituídos e saídas antigas de experimentos/calibração. O histórico Git preserva versões anteriores; o protótipo 3D `plataforma/talhao_sorteado_3pg.html` foi mantido por ser uma interface distinta.
- `py -3 plataforma/construir.py` concluiu; a página `plataforma/docs/index.html` foi reconstruída. `git diff --check` e `git diff --cached --check` passaram.

## Falta
1. Reexecutar `python3 ferramentas/pipeline.py verificar`, auditoria numérica e testes após instalar as dependências Python ausentes; gerar o DOCX após disponibilizar Node.js.
2. Rodar crescimento sem desfolha para TECHS 9 e 22 somente após confirmar os metadados e inventários; reportar erros por variável e separar ajuste de avaliação independente.
3. Reavaliar a apresentação do simulador depois dos testes e da confirmação de todos os dados e alegações exibidos.

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
- 19/11: repetição de desfolhas não será apresentada como inovação frente a Rua et al. (2020); a contribuição é avaliar recuperação e perdas persistentes em condições brasileiras, com limites explícitos de transferência entre materiais. Recuperação da área foliar, retomada do incremento e déficit de madeira são dimensões diferentes. Perda negativa significa apenas resultado simulado acima do controle segundo a fórmula pareada; não atribuir causa hídrica sem evidência. Não importar percentuais de Pizzi até recuperar e conferir a fonte primária. Rótulos S5–SA100 e associação Indianópolis–TECHS 9 permanecem não verificados; Telêmaco Borba–TECHS 22 é sustentado por Binkley et al. (2017).

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
- 19/11 10:20 Atualiza recuperação e limites do módulo
- 03/11 19:49 Resumo executivo ilustrado: da fonte ao número (PDF, 7 p.), para a coorientadora
- 02/11 16:23 Guia ilustrado do TCC II, passo a passo (PDF, 18 p.)
- 02/11 16:09 TCC VERSÃO FINAL v4: 5.1 Perspectivas na conclusão; passagem de bastão para o Astra; conferidor de referências no repositório
- 02/11 12:08 Cascata: dossel de Borges corrigido (TECHS), U só no mês do ataque, recalibração e reprocessamento completo; tabelas geradas dos resultados; pipeline completo; plataforma e capturas atualizadas; TCC VERSÃO FINAL v3 (37 p.), auditoria 528/528
- 02/11 12:02 pipeline: etapa plataforma concluída
- 02/11 12:02 pipeline: etapa tabelas concluída
- 02/11 11:42 pipeline: etapa danos concluída
- 02/11 11:42 pipeline: etapa analises concluída
- 02/11 11:31 pipeline: etapa indicadores concluída
- 02/11 11:31 pipeline: etapa experimentos concluída
- 02/11 11:19 Conferidor: números decimais do texto do TCC × itens da auditoria
- 02/11 11:15 Recalibração com γ = 1 (Quentin 2011), teste independente com Oliveira et al. (2014), busca no Semantic Scholar; TCC VERSÃO FINAL v2 (35 p.), auditoria 506/506
- 02/11 11:14 pipeline: etapa verificar concluída
- 02/11 10:43 Versão final do TCC (02/11): título, referências conferidas e completadas, siglas e símbolos, lista de ilustrações; auditoria 489/489

## Para a IA que continuar
1. Sem execução de código: redija o texto, marcando [CONFERIR] em números ainda não gerados. Nunca invente resultados.
2. Com código: siga "Falta (em ordem)" e rode `python3 ferramentas/pipeline.py <etapa>`.
3. Ao fim de cada passo: atualize `memoria/`, rode este gerador e faça commit.
