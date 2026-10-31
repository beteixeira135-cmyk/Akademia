# PASSAGEM DE BASTÃO — TCC II (3824 tokens, estimativa (caracteres ÷ 3,6); gerado em 31/10/2026 20:32)

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` (21912 tokens, estimativa (caracteres ÷ 3,6)).

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
- Feito (31/10 noite): Missão 07 — auditoria científica e cienciométrica; TCC revisado (53 p.); relatórios em revisao_07/.
- Próximo: OpenAlex (após 00h UTC) → atualizar a cienciometria; o autor lê o TCC revisado e envia aos orientadores com as 5 ressalvas do parecer.
- Arquivos grandes (PDFs, docx, mensal.csv.gz, zips) não vão para o GitHub: ficam no Drive.
- Drive (31/10, fim da noite): relatórios da Missão 07 em Docs na pasta 11; Diário recriado com a entrada da Missão 07; passagem atualizada. Autor arrasta TCC rev07 (pasta 08) e zip (pasta 11).
- Feito (31/10, 20h): plataforma v8 (artifact versão 8). Motor JS com compensação v3, perda de eficiência e mortalidade, conferido contra o Python em 7 cenários (dif. rel. máx 1,4e-14; plataforma/verificacao/comparar.py). Corrigido: volume registrado antes da mortalidade (como no r3PG). 6 locais por bioma; fisiologia original × calibrada; faixa de 90% com 200 amostras do posterior; catálogo de agentes; perda por produto; quadro de domínio de validade; prancha 'Precedentes' (3PG.d, CABALA). TCC rev08 (53 p.): 3.14, 4.12 e conclusão atualizados; auditoria 367/367.
- Feito (31/10, 21h): 'tudo no TCC' — TCC rev09 (55 p., 10 figuras, 14 tabelas): 3.14 descreve a biblioteca de 52 conceitos, modo explicar, cubagem (Smalian/Huber/Newton), taper e sortimentos; 4.12 traz a perda por produto (serraria −33,6%, celulose +5,9%, energia +36,8%) e a figura v8; Apêndice A com tutorial de 13 passos e figura das toras; Apêndice B com controle de versões, roteiro automatizado, auditorias numérica e científica, verificacao/, revisao_07/, ferramentas/. Auditoria 379/379. Pendente: perguntar ao autor sobre declaração de uso de IA.

---
# Progresso
## Feito
- TCC v. 31/10 (manhã): 41 p., 9 figuras, 11 tabelas; auditoria 204/204; 36 testes (substituída pela versão da noite, abaixo).
- Plataforma: conceitos (49), modo explicar, cubagem e taper seccional.
- Calibração v3 (d = 0,999): U mediana 1,16 [IC90% 1,02–1,33]; a mediana 0,55 [0,05–0,975].
  Ajuste C5 (vol/CAP/alt, %): obs 52,9/24,2/19,1; original 64,8/28,5/34,7; calibrado 50,4/20,2/24,9.
  Teste A1-urocam, mesmo experimento, não independente (vol/CAP): obs 59,0/22,9; original 79,3/40,7; calibrado 64,8/29,7 (IC90% vol 53,7–78,6; CAP 22,5–40,0).
- Biomas: clima NASA POWER e solo (ALM 219 mm, ARA 194 mm, ELD 145 mm TECHS 6) prontos; controles rodados.
- Testes da v3: 13 novos (49 no total), todos aprovados (modelo/testes/test_compensacao_v3.py).
- Validação qualitativa E. globulus (calibracao/saida/validacao_globulus.csv): sem perda de DAP/altura nas duas versões
  (fraco para discriminar); IAF aos 18 meses (Barry), perda em relação ao controle: original 8,3%, calibrado 1,4% (IC90% −2,4 a 6,7) → mais próximo
  de "área foliar sem diferença".
- Bloco por bioma (experimentos/run_biomas.py → saida/biomas/): 1.728 tratamentos × 2 versões; a versão original reproduz
  o bloco LOCAL do TCC (diferença máx. 3e-14). Calibrado reduz perdas (ex.: IND A1 50% PA 13,8 → 8,8%) e a recuperação
  relativa de 23–35 para 8–15 meses (exceto ARA, 2–8). Incerteza (200 amostras) em incerteza_posterior_d50.csv.
- RF 6 locais (saida/biomas/rf_*.csv): importância perda de volume — intensidade 50,6/47,3%, frequência 44,3/42,1%
  (original/calibrado). Local fora, RQEM média: original 63% (local categórico) e 66% (clima numérico); calibrado 143% e 69%
  (descrever o clima por números melhora a transferência na versão calibrada; R² 0,17 → 0,83).
- Morris C5, 6 locais (morris_C5_6locais.csv): nWs é o mais influente em todos; depois k, y ou SLA1, conforme o local; dominam a perda de volume em todos os locais.
- Danos, 6 locais, C5 (danos_6locais.csv): formigas original 2,5–6,6% (−0,6 em ARA) → calibrado 0,5–3,0%; em ARA a desfolha
  economiza água e o original dá ganho (−2,5% lagarta), atenuado na calibrada (−0,4%).
- Plausibilidade ARA: biomassa aérea simulada aos 54 meses 57–62 t/ha × 51–132 t/ha (média 88) de 15 clones na estação do IPA
  (Alves et al., 2007, Rev. Ciênc. Agrár. 48:161-173; 3 × 2 m; ~650 mm). Dentro da faixa, abaixo da média. ELD: sem dado
  publicado de produtividade localizado (não independente de qualquer forma).
- TCC v. 31/10 noite: 49 p., 9 figuras, 13 tabelas. Novas seções 3.12 (compensação e calibração), 3.13 (biomas),
  4.10, 4.11 (Tabelas 10 e 11); plataforma → 3.14/4.12; limitações → 4.13 (b) e (j)/(k) revistas; objetivos (+2),
  introdução, resumo/abstract, palavras-chave, conclusões (+2), siglas e símbolos, 5 referências novas (Alves 2007,
  IBGE 2024, McNabb e Wadouski 1999, OpenStreetMap, Silva, Mauro e Almeida 2019), Apêndice B. Auditoria: 336/336.
- Missão 07 (auditoria científica e cienciométrica), concluída em 31/10: revisao_07/. Parecer B (encaminhar com ressalvas).
  Correções: o urocam passou de "validação" a "teste do mesmo experimento"; Bertulio deixou de ser descrito como único
  experimento; precedentes 3PG.d (Rua et al., 2020) e CABALA (Pinkard 2011/2014); evidência contrária de Matrangolo (2010):
  o módulo subestima perdas após desfolha total precoce por fator de 6 a 34; Quentin (2011): γ ≈ 1; U sensível ao prior
  (1,21 com limite 1,6); limitações (a)–(o); Apêndice C (busca). TCC com 53 p., 14 tabelas; auditoria 363/363.
- Plataforma v8 (31/10): diferenciais em relação ao 3PG.d — compensação calibrada com incerteza, 6 biomas, outros danos com catálogo, perda por produto, domínio de validade; JS = Python (7 cenários, 1,4e-14). TCC rev08 com 3.14/4.12 atualizados; auditoria 367/367.
- TCC rev09 (31/10): todo o trabalho descrito no texto (plataforma didática, cubagem e toras, perda por produto, reprodutibilidade e auditorias). 55 p.; auditoria 379/379.
## Falta (em ordem)
1. OpenAlex: rodar revisao_07/busca/openalex_busca.py após o reset do limite e atualizar a cienciometria.
3. Revisão do texto pelo autor e envio aos orientadores (1ª semana de novembro).
4. Defesa: documento de preparação e slides.

---
## Calibração (lido de calibracao/saida/calibracao_d0999.json)
- U: mediana 1.16 (IC90% 1.02–1.33); a: mediana 0.550 (IC90% 0.050–0.975).
- Ajuste C5 — observado: CAP 24.2, altura 19.1, volume 52.9 | original: volume 64.8, CAP 28.5, altura 34.7 | calibrado: volume 50.4, CAP 20.2, altura 24.9.
- Teste A1/urocam (mesmo experimento; não é validação independente) — observado: volume 59.0, CAP 22.9 | original: volume 79.3, CAP 40.7 | calibrado: volume 64.8, CAP 29.7 (IC90% volume 53.7, CAP 22.5 a volume 78.6, CAP 40.0).

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
- 31/10 20:24 Plataforma v8: compensação calibrada com incerteza, 6 biomas, outros danos, perda por produto e domínio de validade; JS = Python (7 cenários); TCC rev08; auditoria 367/367
- 31/10 20:04 Missão 07: Drive atualizado (relatórios, diário, passagem); urocam como teste na memória
- 31/10 20:01 Missão 07: auditoria científica e cienciométrica; TCC revisado (53 p.), relatórios, corpus, matrizes; auditoria 363/363
- 31/10 19:25 Memória e passagem de bastão revisadas
- 31/10 19:24 Diário e memória atualizados
- 31/10 19:24 TCC: seções de calibração (3.12/4.10) e biomas (3.13/4.11), Tabelas 10-11, resumo, conclusões e referências; auditoria 335/335
- 31/10 19:18 Biomas: RF com local fora (6 grupos), Morris e danos nos 6 locais, plausibilidade em Araripina
- 31/10 19:10 Compensação v3: testes (49), validação E. globulus e bloco por bioma (6 locais × original/calibrado + incerteza)
- 31/10 19:05 Memória: GitHub conectado como fonte da verdade
- 31/10 19:05 README, passagem de bastão automática e push automático no pipeline
- 31/10 19:05 Une com o README inicial do repositório
- 31/10 19:02 Initial commit
- 31/10 18:53 Akademia/TCC II: estado de 31/10/2026 (modelo v3 com compensação, calibração, biomas, plataforma, memória e pipeline)

## Para a IA que continuar
1. Sem execução de código: redija o texto, marcando [CONFERIR] em números ainda não gerados. Nunca invente resultados.
2. Com código: siga "Falta (em ordem)" e rode `python3 ferramentas/pipeline.py <etapa>`.
3. Ao fim de cada passo: atualize `memoria/`, rode este gerador e faça commit.
