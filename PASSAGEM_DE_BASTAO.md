# PASSAGEM DE BASTÃO — TCC II (2694 tokens, estimativa (caracteres ÷ 3,6); gerado em 31/10/2026 19:18)

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` (21009 tokens, estimativa (caracteres ÷ 3,6)).

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
- Feito agora: ambiente mecanizado. Repositório privado https://github.com/beteixeira135-cmyk/akademia é a fonte da verdade;
  o pipeline (`ferramentas/pipeline.py`) faz commit e push a cada etapa e regenera PASSAGEM_DE_BASTAO.md.
- Próximo: escrever 3.13/4.12 (calibração) e 3.14/4.13 (biomas) no tcc_docx/conteudo.js, depois auditoria e docx.
- Arquivos grandes reproduzíveis (experimentos/saida/mensal.csv.gz, PDFs, zips) não vão para o GitHub: regenerar com o pipeline ou buscar no Drive.

---
# Progresso
## Feito
- TCC v. 31/10: 41 p., 9 figuras, 11 tabelas; auditoria 204/204; 36 testes.
- Plataforma: conceitos (49), modo explicar, cubagem e taper seccional.
- Calibração v3 (d = 0,999): U mediana 1,16 [IC90% 1,02–1,33]; a mediana 0,55 [0,05–0,975].
  Ajuste C5 (vol/CAP/alt, %): obs 52,9/24,2/19,1; original 64,8/28,5/34,7; calibrado 50,4/20,2/24,9.
  Validação A1-urocam (vol/CAP): obs 59,0/22,9; original 79,3/40,7; calibrado 64,8/29,7 (IC90% vol 53,7–78,6; CAP 22,5–40,0).
- Biomas: clima NASA POWER e solo (ALM 219 mm, ARA 194 mm, ELD 145 mm TECHS 6) prontos; controles rodados.
- Testes da v3: 13 novos (49 no total), todos aprovados (modelo/testes/test_compensacao_v3.py).
- Validação qualitativa E. globulus (calibracao/saida/validacao_globulus.csv): sem perda de DAP/altura nas duas versões
  (fraco para discriminar); IAF aos 18 meses (Barry): original −8,3%, calibrado −1,4% (IC90% −6,7 a +2,4) → mais próximo
  de "área foliar sem diferença".
- Bloco por bioma (experimentos/run_biomas.py → saida/biomas/): 1.728 tratamentos × 2 versões; a versão original reproduz
  o bloco LOCAL do TCC (diferença máx. 3e-14). Calibrado reduz perdas (ex.: IND A1 50% PA 13,8 → 8,8%) e a recuperação
  relativa de 23–35 para 8–15 meses (exceto ARA, 2–8). Incerteza (200 amostras) em incerteza_posterior_d50.csv.
- RF 6 locais (saida/biomas/rf_*.csv): importância perda de volume — intensidade 50,6/47,3%, frequência 44,3/42,1%
  (original/calibrado). Local fora, RQEM média: original 63% (local categórico) e 66% (clima numérico); calibrado 143% e 69%
  (descrever o clima por números melhora a transferência na versão calibrada; R² 0,17 → 0,83).
- Morris C5, 6 locais (morris_C5_6locais.csv): nWs, k e SLA1 dominam a perda de volume em todos os locais.
- Danos, 6 locais, C5 (danos_6locais.csv): formigas original 2,5–6,6% (−0,6 em ARA) → calibrado 0,5–3,0%; em ARA a desfolha
  economiza água e o original dá ganho (−2,5% lagarta), atenuado na calibrada (−0,4%).
- Plausibilidade ARA: biomassa aérea simulada aos 54 meses 57–62 t/ha × 51–132 t/ha (média 88) de 15 clones na estação do IPA
  (Alves et al., 2007, Rev. Ciênc. Agrár. 48:161-173; 3 × 2 m; ~650 mm). Dentro da faixa, abaixo da média. ELD: sem dado
  publicado de produtividade localizado (não independente de qualquer forma).
## Falta (em ordem)
1. Texto: 3.13/4.12 calibração; 3.14/4.13 biomas; resumo, objetivos, limitações, conclusão; referências novas conferidas no PDF.
2. Auditoria com os números novos; gerar docx/pdf; Drive e diário.
3. Defesa: documento de preparação e slides.

---
## Calibração (lido de calibracao/saida/calibracao_d0999.json)
- U: mediana 1.16 (IC90% 1.02–1.33); a: mediana 0.55 (IC90% 0.05–0.97).
- Ajuste C5 — observado: CAP 24.2, altura 19.1, volume 52.9 | original: volume 64.8, CAP 28.5, altura 34.7 | calibrado: volume 50.4, CAP 20.2, altura 24.9.
- Validação A1/urocam — observado: volume 59.0, CAP 22.9 | original: volume 79.3, CAP 40.7 | calibrado: volume 64.8, CAP 29.7 (IC90% volume 53.7, CAP 22.5 a volume 78.6, CAP 40.0).

---
# Registro de decisões (mais recente no fim)
- 30/10: ampliar de Indianópolis para 3 locais; solo local do TECHS onde houver; FR em níveis ordinais.
- 31/10: incluir outros danos (eficiência, mortalidade) com fontes.
- 31/10: plataforma acessível a não especialistas (conceitos, modo explicar, cubagem, taper com Souza et al., 2016).
- 31/10: fazer calibração de verdade ("trabalhoso, defendo fácil"): compensação v3 calibrada contra Bertulio et al. (2008), urograndis (C5); validação com urocam (A1).
- 31/10: um local por bioma onde há eucalipto: Almeirim-PA (Amazônia), Araripina-PE (Caatinga), Eldorado do Sul-RS (Pampa); Pantanal excluído (sem plantio comercial; 3-PG não representa alagamento). Imperatriz é Cerrado (IBGE 2024).
- 31/10: mecanizar o ambiente: AGENTS.md, banco de memória, pipeline único e passagem de bastão gerada automaticamente; GitHub como fonte da verdade quando a conta for conectada.

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
