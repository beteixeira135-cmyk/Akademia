# Contexto empacotado — TCC II (3-PG + desfolha)

Gerado por ferramentas/empacotar.py. Leia primeiro AGENTS.md (regras) e memoria/contexto_ativo.md.


## AGENTS.md

```markdown
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
```

## memoria/projeto.md

```markdown
# Projeto (estável)
- Autor: Bernardo Teixeira de Castro (UFU, Eng. Florestal). Orientador: Álvaro Augusto Vieira Soares. Coorientadora: Dra. Gabriela Cristina Costa Silva (UFRB). Banca: não definida (deixar em branco). Defesa: dezembro/2026.
- IC (frase do autor): a iniciação científica, ainda em andamento, foi a base; a partir dela auditamos, aprimoramos e corrigimos; a etapa atual é a calibração.
- Objetivo: estender o 3-PG com desfolha (e outros danos), simular intensidade, frequência e época em vários climas e solos, e quantificar o que pode e o que não pode ser afirmado sobre a validade biológica.
- Drive: pasta 3-PG https://drive.google.com/drive/folders/1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L (o link vai no Apêndice B).
- Plataforma: https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc
- O autor trabalha pelo celular.
```

## memoria/contexto_ativo.md

```markdown
# Contexto ativo
- Feito (31/10 noite): Missão 07 — auditoria científica e cienciométrica; TCC revisado (53 p.); relatórios em revisao_07/.
- Próximo: OpenAlex (após 00h UTC) → atualizar a cienciometria; o autor lê o TCC revisado e envia aos orientadores com as 5 ressalvas do parecer.
- Arquivos grandes (PDFs, docx, mensal.csv.gz, zips) não vão para o GitHub: ficam no Drive.
- Drive (31/10, fim da noite): relatórios da Missão 07 em Docs na pasta 11; Diário recriado com a entrada da Missão 07; passagem atualizada. Autor arrasta TCC rev07 (pasta 08) e zip (pasta 11).
- Feito (31/10, 20h): plataforma v8 (artifact versão 8). Motor JS com compensação v3, perda de eficiência e mortalidade, conferido contra o Python em 7 cenários (dif. rel. máx 1,4e-14; plataforma/verificacao/comparar.py). Corrigido: volume registrado antes da mortalidade (como no r3PG). 6 locais por bioma; fisiologia original × calibrada; faixa de 90% com 200 amostras do posterior; catálogo de agentes; perda por produto; quadro de domínio de validade; prancha 'Precedentes' (3PG.d, CABALA). TCC rev08 (53 p.): 3.14, 4.12 e conclusão atualizados; auditoria 367/367.
- Feito (31/10, 21h): 'tudo no TCC' — TCC rev09 (55 p., 10 figuras, 14 tabelas): 3.14 descreve a biblioteca de 52 conceitos, modo explicar, cubagem (Smalian/Huber/Newton), taper e sortimentos; 4.12 traz a perda por produto (serraria −33,6%, celulose +5,9%, energia +36,8%) e a figura v8; Apêndice A com tutorial de 13 passos e figura das toras; Apêndice B com controle de versões, roteiro automatizado, auditorias numérica e científica, verificacao/, revisao_07/, ferramentas/. Auditoria 379/379. Pendente: perguntar ao autor sobre declaração de uso de IA.
- Feito (31/10, 21h30): espaço de possibilidades (experimentos/possibilidades.py, 7.584 cenários; 5.688 aptos) e validação cruzada da calibração (calibracao/validacao_cruzada.py: LOO k=5 RQEM 15,1→4,2 p.p.; k=2 C5→A1 19,1→6,4; A1→C5 11,7→4,3). RF k-fold 10×3 R² 0,991; LOSO 0,912; classificador ganho×perda 98,3% (bal. 93,7%). Ganho sobre o controle em 1,9% (orig.) e 3,1% (calib.) dos cenários, quase sempre com 25% de desfolha. TCC rev10: 3.15, 4.13 (Tabelas 12–13), Limitações → 4.14; 59 p.; auditoria 461/461.
- Feito (31/10, 22h): declaração de uso de IA (3.16) e referência ANTHROPIC (2026); TCC rev11, 60 p.; auditoria 461/461.

- Feito (01/11, madrugada): TCC enxugado de 60 para 40 páginas (rev12). Corpo 12.924 → 4.362 palavras; métodos 3.1–3.8, resultados 4.1–4.7; resumo 244 palavras; conclusão 6 parágrafos; plataforma detalhada no Apêndice A; Apêndice D novo (efeito do solo, recuperação × água, Morris). Corrigida a Tabela de verificação (308 controles, 28.277 registros; antes 260/23.873). Tabela 1 com os seis locais. Auditoria 489/489. Versão de 60 p. guardada (conteudo_v11_60p_antes_enxugar.js; entregas/rev11).
- Feito (01/11, 3h): regra do autor — 'tudo que chama atenção fica no TCC (gráficos); tudo que ocupa espaço mental vai para a Akademia'. TCC rev13 (34 p.): linguagem acessível; 12 figuras (3 novas: N1 calibração/validação cruzada, N2 biomas, N3 possibilidades); 1 tabela no corpo (locais); 7 quadros 'Na Akademia' com QR code (plataforma/qr, decodificado e conferido); apêndices A (reprodutibilidade) e B (busca). Akademia v9: 'Material do TCC' com 16 tabelas completas extraídas de gerar.js (extrair_material_tcc.js + material_tcc.py). Auditoria 489/489.
- Feito (02/11): acabamento e VERSÃO FINAL para o Álvaro (34 p.). Título atualizado para 'NOS BIOMAS BRASILEIROS'; referências conferidas nos dois sentidos (5 citações restauradas, incl. SILVA 2021; Souza et al. 2016 e Soares et al. 2003 incluídas, DOIs via Crossref); siglas e símbolos refeitos; lista de ilustrações corrigida (et al.); Apêndice A → B corrigido. Auditoria 489/489; 57 testes.
- Feito (02/11, tarde): ressalvas do parecer resolvidas, sobra 1. (5) γ calibrado com Quentin et al. (2011): γ = 1 (calibracao/calibrar_gamma.py); erro corrigido: calibrar.py ajustava U e a com γ = 0, e as simulações usavam 0,5. Recalibrado com γ = 1: U 1,22 (1,03–1,34), a 0,475; teste urocam 20,3→7,4 p.p.; LOO 15,1→4,1; k=2 19,1→7,2 e 11,7→4,9. Tudo refeito (biomas, possibilidades, RF, Morris). (3) busca complementada no Semantic Scholar (revisao_07/busca/semantic_busca.py: 469 no núcleo combinado; nenhum experimento brasileiro novo). (4) leituras: Battaglia 2011 (fonte primária do CABALA), Turnbull 2007; Collett e Neumann 2002 inacessível. (1) teste independente com Oliveira et al. (2014), Mucuri-BA (calibracao/teste_oliveira2014.py): desfolha total aos 6 meses, perda de volume 8 meses depois 35,4% observada; calibrado 29,2% (26,4–33,5), original 38,7%; parciais ≤1,5%, como no campo (n.s.). (2) Matrangolo vira a única ressalva: o módulo acerta a perda de curto prazo, mas não a persistência por anos (sem reservas nem morte de ramos; o CABALA falha igual, Battaglia 2011).
- TCC VERSÃO FINAL v2 (02/11, 35 p.): entregas/TCC_II_Bernardo_Castro_VERSAO_FINAL_v2_02-11-2026. Auditoria 506/506; 49 testes; referências 0 sem citação. Akademia reconstruída (Material do TCC e domínio de validade com Oliveira).
- Atenção: converter o PDF com --outdir (o PDF em tcc_docx/ fica bloqueado) e rodar `node gerar.js paginas.json` para o sumário ter páginas.
```

## memoria/progresso.md

```markdown
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
- TCC rev10 (31/10): seções 3.15/4.13 — possibilidades do módulo (ganho raro, recuperação de folhas ≠ de volume, aditividade) e validação cruzada (k-fold do metamodelo; LOO da calibração). 59 p.; auditoria 461/461.
## Falta (em ordem)
1. OpenAlex: rodar revisao_07/busca/openalex_busca.py após o reset do limite e atualizar a cienciometria.
3. Revisão do texto pelo autor e envio aos orientadores (1ª semana de novembro).
4. Defesa: documento de preparação e slides.
- 02/11: ressalvas do parecer reduzidas a 1 (persistência das perdas após desfolha total precoce, Matrangolo). TCC VERSÃO FINAL v2, 35 p.; auditoria 506/506.
```

## memoria/decisoes.md

```markdown
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
- 02/11 (tarde): cascata "sem falhas escondidas". (1) Dossel dos clones de Borges corrigido: γF1, γF0 e pFS2 trocados pelos da TECHS (Caldeira et al., 2020a), porque os de Borges davam IAF 8–11 contra 3,0–3,8 medidos; TCC_DOSSEL=borges reproduz a versão anterior. (2) U só no mês do ataque (u_meses = 1; Turnbull et al., 2007; Quentin et al., 2012): as regras testadas deram ajuste equivalente, escolhida a sustentada pela fisiologia; em desfolha total o U não é identificado e vem da faixa da literatura. (3) Matriz principal fixada nos 3 locais (SITIOS_MATRIZ), pois passara a ler os 6 locais. (4) Tabelas completas geradas dos resultados (tcc_docx/tabelas_dados.py), sem números digitados. (5) controles_solo_local.csv ganhou script (experimentos/controles.py). (6) Pipeline com todas as etapas (calibração completa, biomas, possibilidades, tabelas, plataforma).
```

## memoria/tecnico.md

```markdown
# Contexto técnico
- Python 3.11+ (numpy, pandas, scikit-learn, SALib opcional); Node 18+ com `docx` para gerar o TCC; LibreOffice para PDF.
- Modelo: `modelo/threepg_pjs.py`, `run_3pg_pjs(site, species, climate, params, defoliation_events=, efficiency_events=, mortality_events=, compensation=)`.
  - v1/v2: desfolha W_F·(1−d) no início do mês; perda de eficiência α·(1−r); mortalidade N·(1−m).
  - v3 (compensação, opcional): enquanto W_F < W_F,ref: U_ef = 1+(U−1)·f_SW sobre α; condutância ×(gC_ref/gC)^γ (teto 1/(1−0,45)); partição η_F' = η_F + a·déficit·(η_S+η_R).
- Convenção temporal: plantio 2015-01; A1 começa aos 12 meses (2016-01), materiais de Borges aos 3 (2015-04); fim 2023-01; "k" = mês da simulação de referência; rotação = k72 (84 meses de idade).
- Materiais: A1 (Caldeira et al., 2020); C5, C2, C4 (Borges, 2009). A1 em Imperatriz, Almeirim e Araripina = diagnóstico (f_T = 0 em vários meses).
- Locais: IND, TB, IMP (originais); ALM (Amazônia), ARA (Caatinga), ELD (Pampa). Bioma: IBGE 2024 (`biomas/bioma2024.csv`).
```

## calibracao/saida/calibracao_d0999.json

```json
{
 "d_evento": 0.999,
 "gam": 1.0,
 "u_meses": 1,
 "dossel_borges": "techs",
 "observado_C5": {
  "CAP": 24.194,
  "altura": 19.078,
  "volume": 52.866
 },
 "original_C5": {
  "volume": 66.57994824108157,
  "CAP": 29.701246174629624,
  "altura": 36.081954647713275
 },
 "U": {
  "media": 1.1759669864514157,
  "q05": 1.01,
  "q50": 1.18,
  "q95": 1.34
 },
 "a": {
  "media": 0.6123917401127345,
  "q05": 0.225,
  "q50": 0.625,
  "q95": 0.975
 },
 "corr_post": -0.014687414245374574,
 "melhor_ajuste": {
  "U": 1.03,
  "a": 0.65,
  "volume": 50.96194824035661,
  "CAP": 20.47695652997796,
  "altura": 25.24743472348574
 },
 "preditiva_media_C5": {
  "volume": 50.88072978285085,
  "CAP": 20.454425584021205,
  "altura": 25.217394556332568
 },
 "validacao_A1_urocam": {
  "observado": {
   "volume": 58.991,
   "CAP": 22.939
  },
  "original": {
   "volume": 79.34091434001425,
   "CAP": 40.66777101660624
  },
  "calibrado_media": {
   "volume": 66.45733670942239,
   "CAP": 30.634108219520602
  },
  "calibrado_q05": {
   "volume": 59.607542064401876,
   "CAP": 25.92374681210576
  },
  "calibrado_q95": {
   "volume": 76.87871631715122,
   "CAP": 38.41461843730944
  }
 }
}
```

## calibracao/saida/calibracao_d099.json

```json
{
 "d_evento": 0.99,
 "gam": 1.0,
 "u_meses": 1,
 "dossel_borges": "techs",
 "observado_C5": {
  "CAP": 24.194,
  "altura": 19.078,
  "volume": 52.866
 },
 "original_C5": {
  "volume": 56.188224998580104,
  "CAP": 23.30696936312777,
  "altura": 28.609570815040474
 },
 "U": {
  "media": 1.1692527587799855,
  "q05": 1.01,
  "q50": 1.17,
  "q95": 1.34
 },
 "a": {
  "media": 0.38033133292120713,
  "q05": 0.025,
  "q50": 0.35,
  "q95": 0.875
 },
 "corr_post": -0.044727832999155975,
 "melhor_ajuste": {
  "U": 1.32,
  "a": 0.05,
  "volume": 50.95518860578192,
  "CAP": 20.47343199108054,
  "altura": 25.243227052867155
 },
 "preditiva_media_C5": {
  "volume": 46.901995282552505,
  "CAP": 18.44325080119818,
  "altura": 22.807123448665408
 },
 "validacao_A1_urocam": {
  "observado": {
   "volume": 58.991,
   "CAP": 22.939
  },
  "original": {
   "volume": 75.45035813846103,
   "CAP": 37.18041617470538
  },
  "calibrado_media": {
   "volume": 62.23964912142403,
   "CAP": 27.861630238924473
  },
  "calibrado_q05": {
   "volume": 54.45644365139538,
   "CAP": 22.921407394792382
  },
  "calibrado_q95": {
   "volume": 74.22730966056018,
   "CAP": 36.16125781202758
  }
 }
}
```

## calibracao/calibrar.py

```python
"""Calibração bayesiana da compensação (U, a) contra Bertulio et al. (2008), clone urograndis (simulado com C5).
Verossimilhança gaussiana nas perdas ajustadas pela linha de base (volume, CAP, altura; pontos percentuais),
com desvio σ desconhecido marginalizado numericamente (prior meia-normal, escala 10 p.p.). Priores uniformes:
U ~ U(1; 1,35) (aumento de até 35% da fotossíntese: Pinkard et al., 1998, citado por Quentin et al., 2011);
a ~ U(0; 1). γ (condutância) foi calibrado antes, com Quentin et al. (2011) (calibrar_gamma.py), e fica fixo aqui.
Correção de 02/11/2026: a versão anterior ajustava com γ = 0 e simulava com γ = 0,5, embora γ altere as perdas do C5.
Validação independente: urocam (Bertulio) simulado com A1, que não entra no ajuste."""
import json, sys, numpy as np, pandas as pd
import protocolo as p
GAMMA = json.load(open("saida/gamma_quentin2011.json"))["gamma_calibrado"]  # γ calibrado com Quentin et al. (2011), fixo na calibração de U e a
U_MESES = json.load(open("saida/regra_compensacao.json"))["u_meses"]  # U só no mês do ataque (Turnbull et al., 2007; Quentin et al., 2012)
d_ev = float(sys.argv[1]) if len(sys.argv) > 1 else 0.999
U = np.round(np.arange(1.0, 1.3501, 0.01), 3); A = np.round(np.arange(0.0, 1.0001, 0.025), 3)
obs = p.observado("C5"); vs = ["volume", "CAP", "altura"]; y = np.array([obs[v] for v in vs])
SIG = np.linspace(0.5, 40, 160); prior_sig = np.exp(-0.5 * (SIG / 10) ** 2)
linhas = []
for u in U:
    for a in A:
        L = p.perdas("C5", {"U": u, "a": a, "gam": GAMMA, "u_meses": U_MESES}, d=d_ev); m = np.array([L[v] for v in vs])
        sse = float(((m - y) ** 2).sum())
        lik = (prior_sig * SIG ** -3 * np.exp(-sse / (2 * SIG ** 2))).sum()
        linhas.append(dict(U=u, a=a, sse=sse, lik=lik, **{f"L_{v}": L[v] for v in vs}))
G = pd.DataFrame(linhas); G["post"] = G.lik / G.lik.sum()
def resumo(col):
    s = G.groupby(col).post.sum(); c = s.cumsum()
    return dict(media=float((s.index * s).sum()), q05=float(s.index[(c >= 0.05).argmax()]), q50=float(s.index[(c >= 0.5).argmax()]),
                q95=float(s.index[(c >= 0.95).argmax()]))
best = G.loc[G.sse.idxmin()]
post_pred = {v: float((G[f"L_{v}"] * G.post).sum()) for v in vs}
# amostras do posterior para validação e propagação
rng = np.random.default_rng(2026); idx = rng.choice(len(G), size=200, p=G.post.values)
amostras = G.iloc[idx][["U", "a"]].reset_index(drop=True); amostras["gam"] = GAMMA; amostras["u_meses"] = U_MESES
val = []
obsA = p.observado("A1")
for r in amostras.itertuples():
    L = p.perdas("A1", {"U": r.U, "a": r.a, "gam": r.gam, "u_meses": U_MESES}, d=d_ev); val.append(dict(volume=L["volume"], CAP=L["CAP"]))  # γ = GAMMA nas amostras
V = pd.DataFrame(val); L0 = p.perdas("A1", None, d=d_ev); L0c = p.perdas("C5", None, d=d_ev)
import clones as _cl
out = dict(d_evento=d_ev, gam=GAMMA, u_meses=U_MESES, dossel_borges=_cl.DOSSEL, observado_C5=obs, original_C5={v: L0c[v] for v in vs},
           U=resumo("U"), a=resumo("a"), corr_post=float(np.cov(np.vstack([G.U, G.a]), aweights=G.post)[0, 1] / np.sqrt(np.cov(G.U, aweights=G.post) * np.cov(G.a, aweights=G.post))),
           melhor_ajuste=dict(U=float(best.U), a=float(best.a), **{v: float(best[f"L_{v}"]) for v in vs}),
           preditiva_media_C5=post_pred,
           validacao_A1_urocam=dict(observado={k: obsA[k] for k in ["volume", "CAP"]}, original={k: L0[k] for k in ["volume", "CAP"]},
                                    calibrado_media={k: float(V[k].mean()) for k in V}, calibrado_q05={k: float(V[k].quantile(.05)) for k in V},
                                    calibrado_q95={k: float(V[k].quantile(.95)) for k in V}))
tag = str(d_ev).replace(".", "")
G.to_csv(f"saida/grade_posterior_d{tag}.csv", index=False); amostras.to_csv(f"saida/amostras_posterior_d{tag}.csv", index=False)
json.dump(out, open(f"saida/calibracao_d{tag}.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
```

## calibracao/protocolo.py

```python
"""Protocolo de Bertulio et al. (2008) no 3-PG: plantio 2006-02, desfolhas 2007-04 e 2008-01, avaliação 2008-04-30
(26 meses). Mesmo código do confronto do TCC (experimentos/adversarial_e_literatura.py), agora com compensação v3."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "experimentos")); sys.path.insert(0, str(R / "modelo"))
import clima
from clones import params, MATERIAIS
from threepg_pjs import run_3pg_pjs
clima.SITIOS["CV"] = dict(nome="Campo Verde-MT", arquivo="POWER_daily_campo_verde_20060101_20081231.csv",
                          lat=-15.5456, lon=-55.1664, papel="literatura")
CV = clima.clima_mensal("CV")
OBS = pd.read_csv(R / "revisao" / "dados_tratamentos_observados_verificado.csv")
OBS = OBS[(OBS.study_id == "Bertulio_2008") & (OBS.idade_meses == 26)]
ALVO = {"C5": "E. urophylla × E. grandis (urograndis)", "A1": "E. urophylla × E. camaldulensis (urocam)"}
VAR = [("volume", "volume"), ("dbh", "CAP"), ("height", "altura")]
def sim(mat, ev=None, comp=None):
    M = MATERIAIS[mat]; frm = "2007-02" if mat == "A1" else "2006-05"
    site = dict(latitude=-15.5456, altitude=0, soil_class=-1, asw_i=190.6, asw_min=0, asw_max=190.6, **{"from": frm, "to": "2008-06"})
    sp = dict(planted="2006-02", fertility=M["FR_ref"], stems_n=10000 / 9, biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    return run_3pg_pjs(site, sp, CV, params(mat), defoliation_events=ev, compensation=comp)
_CTRL = {}
def perdas(mat, comp=None, d=0.999, data="2008-04-30"):
    if mat not in _CTRL: _CTRL[mat] = sim(mat)
    c = _CTRL[mat]; t = sim(mat, {"2007-04": d, "2008-01": d}, comp)
    cc = c.set_index(c.date.astype(str)); tt = t.set_index(t.date.astype(str))
    return {vo: 100 * (1 - tt[vs][data] / cc[vs][data]) for vs, vo in VAR}
def observado(mat):
    o = OBS[OBS.especie_ou_clone == ALVO[mat]]
    return {r.variavel: r.L_obs_pct_ajustado_linha_base for r in o.itertuples()}
if __name__ == "__main__":
    for mat in ["C5", "A1"]:
        print(mat, "obs", {k: round(v, 1) for k, v in observado(mat).items()})
        for comp in [None, {"U": 1.35}, {"gam": 1}, {"a": 1}, {"U": 1.35, "gam": 1, "a": 1}]:
            print("  ", comp, {k: round(v, 1) for k, v in perdas(mat, comp).items()})
```

## experimentos/clima.py

```python
"""Clima mensal para o r3PG a partir dos CSV diários NASA POWER (API, comunidade AG, 2015–2024).
Agregação: tmp_min/tmp_max = média mensal; prcp = soma; srad = média (MJ m-2 d-1);
frost_days = nº de dias com T2M_MIN <= 0 °C; tmp_ave e vpd_day = fórmulas internas do r3PG
(prepare_climate: (Tmin+Tmax)/2 e ½[es(Tmax)−es(Tmin)], VPD diurno do 3-PG, em mbar)."""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1] / "clima" / "power_api"
SITIOS = {
    "IND": dict(nome="Indianópolis-MG", arquivo="POWER_daily_indianopolis_20150101_20241231.csv",
                lat=-19.0389, lon=-47.9169, papel="estudo de caso principal"),
    "TB": dict(nome="Telêmaco Borba-PR", arquivo="POWER_daily_telemaco_borba_20150101_20241231.csv",
               lat=-24.3239, lon=-50.6158, papel="extrapolação (clima subtropical; 8 dias com Tmin<=0)"),
    "IMP": dict(nome="Imperatriz-MA", arquivo="POWER_daily_imperatriz_20150101_20241231.csv",
                lat=-5.52583, lon=-47.4758, papel="extrapolação (clima quente)"),
    # Locais por bioma (bioma predominante do município: IBGE, 2024). Coordenadas: OpenStreetMap (Nominatim).
    "ALM": dict(nome="Almeirim-PA (Monte Dourado)", arquivo="POWER_daily_almeirim_monte_dourado_20150101_20241231.csv",
                lat=-0.8654, lon=-52.5396, papel="Amazônia; plantios da Jari (McNabb e Wadouski, 1999)"),
    "ARA": dict(nome="Araripina-PE", arquivo="POWER_daily_araripina_20150101_20241231.csv",
                lat=-7.5769, lon=-40.5039, papel="Caatinga; clones do Polo Gesseiro do Araripe (IPA)"),
    "ELD": dict(nome="Eldorado do Sul-RS", arquivo="POWER_daily_eldorado_do_sul_20150101_20241231.csv",
                lat=-30.0232, lon=-51.3830, papel="Pampa; sítio TECHS 6 (Binkley et al., 2017)"),
}
BIOMA = {"IND": "Cerrado", "IMP": "Cerrado", "TB": "Mata Atlântica", "ALM": "Amazônia", "ARA": "Caatinga", "ELD": "Pampa"}


def ler_diario(caminho):
    linhas = open(caminho, encoding="utf-8").read().splitlines()
    ini = next(i for i, l in enumerate(linhas) if l.startswith("YEAR,"))
    d = pd.read_csv(caminho, skiprows=ini)
    if (d <= -990).any().any():
        raise ValueError(f"{caminho}: códigos -999 presentes")
    d["date"] = pd.to_datetime(d.YEAR.astype(str), format="%Y") + pd.to_timedelta(d.DOY - 1, unit="D")
    full = pd.date_range(d.date.min(), d.date.max())
    if len(full.difference(d.date)):
        raise ValueError(f"{caminho}: dias faltantes")
    return d


def clima_mensal(sitio):
    d = ler_diario(RAIZ / SITIOS[sitio]["arquivo"])
    g = d.groupby([d.date.dt.year.rename("year"), d.date.dt.month.rename("month")])
    m = pd.DataFrame(dict(tmp_min=g.T2M_MIN.mean(), tmp_max=g.T2M_MAX.mean(), prcp=g.PRECTOTCORR.sum(),
                          srad=g.ALLSKY_SFC_SW_DWN.mean(),
                          frost_days=g.T2M_MIN.apply(lambda x: int((x <= 0).sum())),
                          n=g.size())).reset_index()
    dim = pd.to_datetime(dict(year=m.year, month=m.month, day=1)).dt.days_in_month
    if (m.n != dim).any():
        raise ValueError("mês incompleto")
    es = lambda t: 6.10780 * np.exp(17.2690 * t / (237.30 + t))
    m["tmp_ave"] = (m.tmp_min + m.tmp_max) / 2
    m["vpd_day"] = (es(m.tmp_max) - es(m.tmp_min)) / 2
    return m.drop(columns="n")
```

## experimentos/clones.py

```python
"""
Conjuntos de parâmetros r3PG (82) por material genético, com origem de cada valor.

A1  = Eucalyptus urophylla, clone A1 — Caldeira et al. (2020), Tabela 1 e §2.7 (conferido no PDF).
C1..C5 = híbridos E. grandis × E. urophylla — Borges (2009, dissertação UFV), Tabela 9, pp. 43–44
         (conferida no PDF; idêntica às colunas 'Eucalyptus grandis x urophylla2..6' do 3PGmix.Data.xls).
         C1 = clone 3334 Curvelo; C2 = 3336 Curvelo; C3 = 3334 Itacambira; C4 = 3336 Itacambira;
         C5 = modelo geral para o Cerrado (dados de 3334/3336 Itacambira + 3336 Curvelo).

Lacunas (parâmetros ausentes nas duas fontes) são preenchidas com o MESMO critério para todos os
materiais: coluna E. globulus do 3PGmix.Data.xls (= padrão Sands & Landsberg 2002), ou valor neutro.
Nenhum valor de um clone foi usado em outro.

Exceções documentadas:
 * Volume: Borges (Tab. 4) ajusta V em m3/ha diretamente de dap; a fórmula do r3PG (aV·dap^nVB·N) é
   por árvore -> incompatível. Para todos os materiais o volume usa o caminho de biomassa (aV = 0):
   V = Ws·(1 − fracBB)/ρ.
 * Altura: Caldeira não publica alometria de altura (aH = 0 -> altura indisponível); Borges publica
   H = aH·dap^nHB (Tab. 4/9), usada com nHC = 0.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cenarios"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modelo"))
from parametros_caldeira_r3pg import P as P_CALDEIRA  # noqa: E402
from threepg_pjs import PAR_FORTRAN  # noqa: E402

# ---------- Borges (2009), Tabela 9 — transcrição conferida na imagem das páginas 43–44 ----------
B9 = {  #            C1      C2      C3      C4      C5
    "WF0":       (0.110, 0.170, 0.162, 0.170, 0.168),
    "WS0":       (0.064, 0.116, 0.075, 0.116, 0.106),
    "WR0":       (0.080, 0.100, 0.093, 0.100, 0.099),
    "pFS2":      (0.95, 1.72, 1.00, 1.00, 1.64),
    "pFS20":     (0.10, 0.11, 0.17, 0.17, 0.15),
    "aWs":       (0.007, 0.011, 0.013, 0.043, 0.020),
    "nWs":       (3.60, 3.35, 3.27, 2.82, 3.11),
    "pRx":       (0.5,) * 5, "pRn": (0.1,) * 5,
    "gammaF1":   (0.07,) * 5, "gammaF0": (0.001,) * 5, "tgammaF": (4.0,) * 5,
    "gammaR":    (0.025,) * 5,
    "Tmin":      (8.0,) * 5, "Topt": (25.0,) * 5, "Tmax": (40.0,) * 5,
    "m0":        (0.0,) * 5, "fN0": (0.5,) * 5, "fNn": (1.0,) * 5,
    "FR":        (0.9,) * 5,
    "MaxAge":    (9.0,) * 5, "nAge": (4.0,) * 5, "rAge": (0.95,) * 5,
    "SLA0":      (15.17, 12.69, 14.09, 14.43, 13.74),
    "SLA1":      (6.11, 8.60, 6.60, 7.48, 7.56),
    "tSLA":      (1.13, 0.73, 1.49, 1.42, 1.23),
    "k":         (0.5,) * 5, "fullCanAge": (2.0,) * 5,
    "MaxIntcptn": (0.15,) * 5, "LAImaxIntcptn": (3.33,) * 5,
    "alphaCx":   (0.09, 0.08, 0.08, 0.08, 0.08),
    "y":         (0.5,) * 5,
    "MaxCond":   (0.01, 0.02, 0.02, 0.02, 0.02),
    "LAIgcx":    (3.33,) * 5, "CoeffCond": (0.0324,) * 5, "BLcond": (0.2,) * 5,
    "wSx1000":   (300.0,) * 5,
    "fracBB0":   (0.54, 0.60, 0.53, 0.62, 0.59),
    "fracBB1":   (0.14, 0.14, 0.23, 0.15, 0.19),
    "tBB":       (2.19, 1.68, 2.85, 2.47, 2.17),
    "rho0":      (0.430, 0.409, 0.391, 0.345, 0.382),
    "rho1":      (0.580, 0.473, 0.539, 0.502, 0.505),
    "tRho":      (3.892, 2.917, 2.202, 2.175, 2.264),
    "aH":        (0.62, 0.50, 0.56, 0.57, 0.67),
    "nHB":       (1.36, 1.42, 1.34, 1.31, 1.27),
}

# lacunas: mesmo critério aplicado a Caldeira (coluna E. globulus / neutro / processo desligado)
LACUNAS = {
    "leafgrow": (0, "ESTRUTURAL: perenifólia"), "leaffall": (0, "ESTRUTURAL: perenifólia"),
    "kF": (0.0, "ADAPTADO E. globulus (ausente na fonte)"),
    "SWconst0": (0.4, "soil_class=4 (classe C, muito argiloso, Borges Tab.9) -> 0,4"),
    "SWpower0": (3.0, "soil_class=4 -> 3"),
    "fCalpha700": (1.4, "NEUTRO com CO2=350"), "fCg700": (0.7, "NEUTRO com CO2=350"),
    "gammaN1": (0.0, "AUSENTE_ZERO"), "gammaN0": (0.0, "AUSENTE_ZERO"), "tgammaN": (0.0, "AUSENTE_ZERO"),
    "ngammaN": (1.0, "AUSENTE_ZERO"),
    "thinPower": (1.5, "ADAPTADO E. globulus"), "mF": (0.0, "ADAPTADO E. globulus"),
    "mR": (0.2, "ADAPTADO E. globulus"), "mS": (0.2, "ADAPTADO E. globulus"),
    "cVPD": (5.0, "NEUTRO: só 3-PGmix"), "MinCond": (0.0, "ADAPTADO E. globulus"),
    "RGcGW": (0.66, "NEUTRO d13C"), "D13CTissueDif": (2.0, "NEUTRO d13C"), "aFracDiffu": (4.4, "NEUTRO d13C"),
    "bFracRubi": (27.0, "NEUTRO d13C"), "CrownShape": (3, "NEUTRO 3-PGmix"),
    "nHC": (0.0, "Borges Tab.4: H = aH·dap^nHB (sem termo de competição)"),
    "aV": (0.0, "ESTRUTURAL: volume por biomassa (ver docstring)"), "nVB": (0.0, "idem"), "nVH": (0.0, "idem"),
    "nVBH": (0.0, "idem"),
    "aK": (0.0, "NEUTRO"), "nKB": (0.0, "NEUTRO"), "nKH": (0.0, "NEUTRO"), "nKC": (0.0, "NEUTRO"),
    "nKrh": (0.0, "NEUTRO"), "aHL": (0.0, "NEUTRO"), "nHLB": (0.0, "NEUTRO"), "nHLL": (0.0, "NEUTRO"),
    "nHLC": (0.0, "NEUTRO"), "nHLrh": (0.0, "NEUTRO"),
    "Qa": (-90.0, "ADAPTADO E. globulus"), "Qb": (0.8, "ADAPTADO E. globulus"),
    "gDM_mol": (24.0, "ADAPTADO"), "molPAR_MJ": (2.3, "ADAPTADO"),
}


# Correção do dossel (02/11/2026): com a queda de folhas e a partição para folhas de Borges (2009), os clones formam
# IAF de 8 a 11 entre 2 e 3 anos, contra 3,0 a 3,8 medidos na rede TECHS. Esses três parâmetros passam a ser os da
# parametrização TECHS (Caldeira et al., 2020, clone A1); o resto continua de Borges. Para reproduzir a versão
# anterior: variável de ambiente TCC_DOSSEL=borges.
import os as _os
DOSSEL = _os.environ.get("TCC_DOSSEL", "techs")
DOSSEL_TECHS = ("gammaF1", "gammaF0", "pFS2")


def _borges(i):
    P = {}
    for k_, v in B9.items():
        if k_ in ("WF0", "WS0", "WR0", "FR"):
            continue
        P[k_] = (float(v[i]), f"FONTE Borges 2009 Tab.9 (C{i+1})")
    if DOSSEL == "techs":
        for k_ in DOSSEL_TECHS:
            P[k_] = (float(P_CALDEIRA[k_][0]), "FONTE Caldeira et al. 2020 (TECHS): dossel corrigido, IAF de Borges irreal")
    for k_, v in LACUNAS.items():
        P.setdefault(k_, v)
    assert set(P) == set(PAR_FORTRAN), set(PAR_FORTRAN) ^ set(P)
    return P


MATERIAIS = {
    "A1": dict(nome="E. urophylla clone A1 (Caldeira et al. 2020)", P=P_CALDEIRA,
               idade_inicial_meses=12, WF0=2.07, WS0=5.47, WR0=1.09, FR_ref=0.8,
               regiao="multissítio Brasil (TECHS); calibrado/validado até 80 meses"),
}
for i, rot in enumerate(["C1", "C2", "C3", "C4", "C5"]):
    desc = ["clone 3334, Curvelo-MG", "clone 3336, Curvelo-MG", "clone 3334, Itacambira-MG",
            "clone 3336, Itacambira-MG", "modelo geral Cerrado-MG"][i]
    MATERIAIS[rot] = dict(nome=f"E. grandis × E. urophylla {desc} (Borges 2009)", P=_borges(i),
                          idade_inicial_meses=3, WF0=B9["WF0"][i], WS0=B9["WS0"][i], WR0=B9["WR0"][i],
                          FR_ref=B9["FR"][i], regiao=desc)


def params(material):
    return {k_: float(v[0]) for k_, v in MATERIAIS[material]["P"].items()}


def origem(material):
    return {k_: v[1] for k_, v in MATERIAIS[material]["P"].items()}
```

## biomas/ptf_zarc.py

```python
"""PTF-ZARC (Teixeira et al., 2021, Equação 9): água disponível AD (mm cm-1) a partir de areia total (AT),
silte (SIL) e argila (ARG), em %. CAD 0–2 m = AD × 200 cm."""
def ad_mm_cm(at, sil, arg):
    x = (-0.02128887 * at - 0.01005814 * sil - 0.01901894 * arg + 0.0001171219 * at * sil
         + 0.0002073924 * at * arg + 0.00006118707 * sil * arg - 0.000006373789 * at * sil * arg)
    return (1 + 0.35941 * x) ** 2.78474 * 10
def cad_2m(at, sil, arg):
    return ad_mm_cm(at, sil, arg) * 200
if __name__ == "__main__":
    # conferência com SOLOS_LOCAIS.md: TECHS 22 (21/23/56) -> 213 mm; TECHS 9 (11/9/80) -> 160 mm
    print(round(cad_2m(21, 23, 56)), round(cad_2m(11, 9, 80)))
```

## biomas/soilgrids_wcs.py

```python
"""Textura SoilGrids 2.0 (Poggio et al., 2021) por WCS (maps.isric.org), 6 camadas 0–200 cm, em 8 pontos a
±0,08° (~9 km) da sede (grade 3×3 sem o centro), mesmo desenho usado para Imperatriz. Unidade WCS: g/kg -> %.
CAD 0–2 m = Σ AD_PTF-ZARC(camada) × espessura."""
import sys, io, json, time, urllib.request
import numpy as np, tifffile
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from ptf_zarc import ad_mm_cm
CAM = [("0-5cm", 0, 5), ("5-15cm", 5, 15), ("15-30cm", 15, 30), ("30-60cm", 30, 60), ("60-100cm", 60, 100), ("100-200cm", 100, 200)]
def valor(prop, prof, lon, lat, d=0.003):
    url = (f"https://maps.isric.org/mapserv?map=/map/{prop}.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage"
           f"&COVERAGEID={prop}_{prof}_mean&FORMAT=image/tiff&SUBSET=long({lon-d},{lon+d})&SUBSET=lat({lat-d},{lat+d})"
           "&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326&OUTPUTCRS=http://www.opengis.net/def/crs/EPSG/0/4326")
    for t in range(4):
        try:
            a = tifffile.imread(io.BytesIO(urllib.request.urlopen(url, timeout=90).read())).astype(float)
            a = a[(a > 0) & (a < 1000)]
            return float(np.median(a)) / 10 if a.size else None
        except Exception as e:
            time.sleep(5)
    return None
def sitio(cod, lon0, lat0):
    out = []
    for i, dx in enumerate([-0.08, 0, 0.08]):
        for j, dy in enumerate([-0.08, 0, 0.08]):
            if dx == 0 and dy == 0: continue
            lon, lat = round(lon0 + dx, 4), round(lat0 + dy, 4); cam = []
            for prof, a, b in CAM:
                v = {p: valor(p, prof, lon, lat) for p in ("clay", "sand", "silt")}
                cam.append(dict(prof=prof, top=a, bot=b, **v))
            ok = all(None not in (c["clay"], c["sand"], c["silt"]) for c in cam)
            asw = sum(ad_mm_cm(c["sand"], c["silt"], c["clay"]) * (c["bot"] - c["top"]) for c in cam) if ok else None
            out.append(dict(sitio=cod, lon=lon, lat=lat, camadas=cam, asw=asw))
            print(cod, lon, lat, None if asw is None else round(asw, 1), [c["clay"] for c in cam], flush=True)
    return out
if __name__ == "__main__":
    res = sitio(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
    json.dump(res, open(f"/home/claude/tcc/solos_fontes/soilgrids_wcs_{sys.argv[1]}.json", "w"), indent=1)
```

## modelo/threepg_pjs.py

```python
"""
threepg_pjs.py — Tradução linha a linha do núcleo 3-PGpjs do pacote r3PG v0.1.7
(Trotsiuk, Hartig & Forrester 2020, doi:10.1111/2041-210X.13474; código-fonte
github.com/trotsiuk/r3PG, commit e39bd8e9, arquivo src/md_3PG.f95), acrescida de
uma EXTENSÃO documentada: o módulo de desfolha (ver `defoliation_events`).

Escopo traduzido (o que o TCC usa):
  * 1 espécie/coorte; light_model = 1, transp_model = 1, phys_model = 1 (3-PGpjs)
  * height_model 1 ou 2; correct_bias = 0; calculate_d13c = 0; sem desbaste
  * espécies perenifólias e decíduas (a lógica de dormência foi mantida para
    permitir o teste de referência "Broadleaf 3-PGpjs" do r3PG)
Fora do escopo (gera erro explícito): 3-PGmix, correção de viés por Weibull,
desbastes, múltiplas espécies, d13C.

Convenção temporal herdada do r3PG: a linha 0 da saída é o ESTADO INICIAL no fim do
mês `from`; o crescimento começa no mês seguinte. A linha t corresponde ao fim do
mês (from + t meses) e usa o clima desse mês.

EXTENSÃO — desfolha (não existe no r3PG original):
  defoliation_events = {"AAAA-MM": d, ...}, 0 <= d < 1.
  No início do passo do mês indicado, ANTES da interceptação de luz:
      Wf_pos = Wf_pre * (1 - d) ; LAI = Wf_pos * SLA(t) * 0.1
  A biomassa removida (Wf_pre * d) é registrada no fluxo `biom_defol`, separado da
  serapilheira (`biom_loss_foliage`). Nenhum outro parâmetro é alterado (SLA, alphaCx,
  alocação e mortalidade seguem as equações originais). O crescimento posterior é
  calculado pelas equações do modelo, sem taxa de recuperação imposta.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

# ---- constantes (src/md_decl_const.f95) ----
PI = 3.141592654
LN2 = 0.693147181
E20 = 2.2
MAX_SOIL_COND = 0.00250
LAMBDA = 2460000.0
RHO_AIR = 1.2
VPD_CONV = 0.000622
DAY_OF_YEAR = np.array([15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349], float)
DAYS_IN_MONTH = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], float)
B_N = 2  # iterações de correção (src/i_decl_var.h)

# ordem dos 82 parâmetros (src/i_read_param.h) — nomes internos do Fortran
PAR_FORTRAN = """pFS2 pFS20 aWs nWs pRx pRn gammaF1 gammaF0 tgammaF gammaR leafgrow leaffall
Tmin Topt Tmax kF SWconst0 SWpower0 fCalpha700 fCg700 m0 fN0 fNn MaxAge nAge rAge gammaN1
gammaN0 tgammaN ngammaN wSx1000 thinPower mF mR mS SLA0 SLA1 tSLA k fullCanAge MaxIntcptn
LAImaxIntcptn cVPD alphaCx y MinCond MaxCond LAIgcx CoeffCond BLcond RGcGW D13CTissueDif
aFracDiffu bFracRubi fracBB0 fracBB1 tBB rho0 rho1 tRho CrownShape aH nHB nHC aV nVB nVH
nVBH aK nKB nKH nKC nKrh aHL nHLB nHLL nHLC nHLrh Qa Qb gDM_mol molPAR_MJ""".split()
assert len(PAR_FORTRAN) == 82


def pulsos(from_ym: str, indices, d: float) -> dict:
    """Converte índices de mês da simulação em datas de evento.
    Convenção: índice k = linha k da saída = k-ésimo mês de crescimento após o estado
    inicial (`from`). Ex.: from='2014-12', k=12 -> '2015-12'; k=48 -> '2018-12'."""
    base = pd.Timestamp(from_ym + "-01")
    out = {}
    for k_ in indices:
        if int(k_) < 1:
            raise ValueError("O índice do pulso deve ser >= 1 (0 é o estado inicial).")
        out[(base + pd.DateOffset(months=int(k_))).strftime("%Y-%m")] = d
    if len(out) != len(list(indices)):
        raise ValueError("Índices de pulso repetidos.")
    return out


def params_from_table(table: pd.DataFrame, column: str) -> dict:
    """Converte a tabela de parâmetros do r3PG (82 linhas, na ordem oficial) num
    dicionário com os nomes internos do Fortran. `column` = coluna da espécie."""
    if len(table) != 82:
        raise ValueError("A tabela deve ter as 82 linhas de parâmetros do r3PG, na ordem oficial.")
    vals = table[column].astype(float).to_numpy()
    if np.isnan(vals).any():
        faltam = [table.iloc[i, 0] for i in np.where(np.isnan(vals))[0]]
        raise ValueError(f"Parâmetros sem valor (não serão inventados): {faltam}")
    return dict(zip(PAR_FORTRAN, vals))


def prepare_climate(climate: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Equivalente a r3PG::prepare_climate (caso com série completa, não 12 linhas)."""
    c = climate.copy()
    for col in ("tmp_min", "tmp_max", "prcp", "srad", "frost_days", "year", "month"):
        if col not in c:
            raise ValueError(f"Clima sem a coluna obrigatória '{col}'")
    if c[["tmp_min", "tmp_max", "prcp", "srad", "frost_days"]].isna().any().any():
        raise ValueError("Clima contém NA")
    c["date"] = pd.to_datetime(dict(year=c.year, month=c.month, day=1))
    d0, d1 = pd.Timestamp(start + "-01"), pd.Timestamp(end + "-01")
    if d0 < c.date.min() or d1 > c.date.max():
        raise ValueError("Período solicitado fora da cobertura do clima")
    c = c[(c.date >= d0) & (c.date <= d1)].copy()
    c["frost_days"] = np.minimum(c.frost_days, DAYS_IN_MONTH[c.month.to_numpy() - 1])
    if "tmp_ave" not in c:
        c["tmp_ave"] = (c.tmp_min + c.tmp_max) / 2
    if "vpd_day" not in c:
        es = lambda t: 6.10780 * np.exp(17.2690 * t / (237.30 + t))
        c["vpd_day"] = (es(c.tmp_max) - es(c.tmp_min)) / 2
    if "co2" not in c:
        c["co2"] = 350.0
    if "d13catm" not in c:
        c["d13catm"] = -7.1
    return c.reset_index(drop=True)


# ---------------- funções auxiliares (md_3PG.f95) ----------------
def f_dormant(month: int, leafgrow: int, leaffall: int) -> bool:
    if leafgrow > leaffall:
        return leaffall <= month <= leafgrow
    if leafgrow < leaffall:
        return month < leafgrow or month >= leaffall
    return False


def f_exp(x, g0, gx, tg, ng):
    if tg != 0:
        return gx + (g0 - gx) * np.exp(-LN2 * (x / tg) ** ng)
    return np.full_like(x, gx)


def f_exp_foliage(x, f1, f0, tg):
    if tg * f1 == 0:
        return np.full_like(x, f1)
    kg = 12.0 * np.log(1.0 + f1 / f0) / tg
    return f1 * f0 / (f0 + (f1 - f0) * np.exp(-kg * x))


def f_get_daylength(lat):
    slat, clat = np.sin(PI * lat / 180.0), np.cos(PI * lat / 180.0)
    sin_dec = 0.4 * np.sin(0.0172 * (DAY_OF_YEAR - 80.0))
    cos_h0 = -sin_dec * slat / (clat * np.sqrt(1.0 - sin_dec ** 2))
    dl = np.arccos(np.clip(cos_h0, -1, 1)) / PI
    dl = np.where(cos_h0 > 1, 0.0, dl)
    dl = np.where(cos_h0 < -1, 1.0, dl)
    return dl


def f_get_mortality(stems_n, ws, mS, wSx1000, thinPower):
    accuracy = 1.0 / 1000.0
    n = stems_n / 1000.0
    x1 = 1000.0 * mS * ws / stems_n
    i = 0
    while True:
        i += 1
        if n <= 0:
            break
        x2 = wSx1000 * n ** (1.0 - thinPower)
        fN = x2 - x1 * n - (1.0 - mS) * ws
        dfN = (1.0 - thinPower) * x2 / n - x1
        dN = -fN / dfN
        n = n + dN
        if abs(dN) <= accuracy or i >= 5:
            break
    return stems_n - 1000.0 * n


def run_3pg_pjs(site: dict, species: dict, climate: pd.DataFrame, params: dict,
                height_model: int = 1, defoliation_events: dict | None = None,
                settings: dict | None = None, efficiency_events: dict | None = None,
                mortality_events: dict | None = None, compensation: dict | None = None) -> pd.DataFrame:
    """Executa o 3-PGpjs. Retorna DataFrame mensal (linha 0 = estado inicial)."""
    if settings is not None:
        exig = dict(light_model=1, transp_model=1, phys_model=1, correct_bias=0, calculate_d13c=0)
        for k_, v_ in exig.items():
            if settings.get(k_, v_) != v_:
                raise NotImplementedError(f"Configuração não suportada nesta tradução: {k_}={settings[k_]}")
    np.seterr(all="ignore")
    P = {k_: np.float64(v_) for k_, v_ in params.items()}
    leafgrow, leaffall = int(P["leafgrow"]), int(P["leaffall"])

    clim = prepare_climate(climate, site["from"], site["to"])
    n_m = len(clim)
    tmin, tmax, tave = (clim[c].to_numpy(float) for c in ("tmp_min", "tmp_max", "tmp_ave"))
    prcp, srad, frost = (clim[c].to_numpy(float) for c in ("prcp", "srad", "frost_days"))
    vpd_day, co2 = clim.vpd_day.to_numpy(float), clim.co2.to_numpy(float)

    lat = float(site["latitude"])
    soil_class = int(site["soil_class"])
    ASW, asw_min, asw_max = float(site["asw_i"]), float(site["asw_min"]), float(site["asw_max"])
    year_i, month_i = map(int, site["from"].split("-"))
    year_p, month_p = map(int, species["planted"].split("-"))
    fertility = float(species["fertility"])

    # ---- eventos de desfolha (EXTENSÃO) ----
    dates = pd.date_range(pd.Timestamp(site["from"] + "-01"), periods=n_m, freq="MS")
    defol = np.zeros(n_m)
    for ym, frac in (defoliation_events or {}).items():
        frac = float(frac)
        if not (0.0 <= frac < 1.0):
            raise ValueError(f"Intensidade de desfolha deve estar em [0,1): {ym}={frac}")
        hit = np.where(dates == pd.Timestamp(ym + "-01"))[0]
        if len(hit) != 1:
            raise ValueError(f"Mês de desfolha fora da simulação: {ym}")
        if hit[0] == 0:
            raise ValueError("Desfolha no mês inicial não é permitida: a linha 0 é o estado inicial.")
        if defol[hit[0]] != 0.0:
            raise ValueError(f"Evento duplicado para {ym}")
        if f_dormant(int(dates[hit[0]].month), leafgrow, leaffall):
            raise ValueError("Desfolha em mês de dormência não é suportada.")
        defol[hit[0]] = frac

    # ---- EXTENSÃO v2: perda de eficiência fotossintética e mortalidade induzida ----
    def _serie(evts, nome):
        arr = np.zeros(n_m)
        for ym_, fr_ in (evts or {}).items():
            fr_ = float(fr_)
            if not (0.0 <= fr_ < 1.0):
                raise ValueError(f"{nome} deve estar em [0,1): {ym_}={fr_}")
            h_ = np.where(dates == pd.Timestamp(ym_ + "-01"))[0]
            if len(h_) != 1 or h_[0] == 0:
                raise ValueError(f"Mês de {nome} fora da simulação ou no mês inicial: {ym_}")
            arr[h_[0]] = fr_
        return arr
    effic = _serie(efficiency_events, "perda de eficiência")
    # ---- EXTENSÃO v3: compensação fisiológica após a desfolha (opcional; None = v2 idêntica) ----
    # Ativa enquanto a biomassa foliar estiver abaixo da biomassa anterior ao último evento (W_F < W_F,ref),
    # adaptação da regra do CABALA (Battaglia et al., 2011, em Pinkard et al., 2011: P = U·P enquanto B < B').
    #   U    : fator de aumento da eficiência quântica das folhas remanescentes (Pinkard et al., 2007; 1998);
    #          expresso só com água disponível: U_ef = 1 + (U − 1)·f_SW (Quentin et al., 2012).
    #   gam  : fração da condutância de dossel perdida que é restabelecida, (gC_ref/gC)^gam, limitada a
    #          1/(1 − 0,45) (homeostase observada com 45% de desfolha; Quentin et al., 2011).
    #   a    : desvio da partição para folhas, η_F' = η_F + a·def·(η_S + η_R), def = 1 − W_F/W_F,ref
    #          (aumento da razão folha:lenho e menor alocação a raízes; Eyles et al., 2009).
    #   u_meses (opcional, 02/11/2026): U só atua no mês do ataque e nos (u_meses − 1) seguintes; o aumento medido
    #          some em 3 a 5 semanas (Turnbull; Adams; Warren, 2007; Quentin et al., 2012). None = até a copa se refazer.
    comp = None
    if compensation:
        comp = dict(U=float(compensation.get("U", 1.0)), gam=float(compensation.get("gam", 0.0)),
                    a=float(compensation.get("a", 0.0)), u_meses=compensation.get("u_meses"))
        if comp["u_meses"] is not None:
            comp["u_meses"] = int(comp["u_meses"])
            if comp["u_meses"] < 1:
                raise ValueError("u_meses deve ser >= 1")
        if not (1.0 <= comp["U"] <= 2.0 and 0.0 <= comp["gam"] <= 1.0 and 0.0 <= comp["a"] <= 1.0):
            raise ValueError(f"Parâmetros de compensação fora do domínio: {comp}")
    GC_CAP = 1.0 / (1.0 - 0.45)
    wf_ref = 0.0
    t_ev = -10 ** 6
    mortind = _serie(mortality_events, "mortalidade induzida")

    # ---- INITIALISATION (age independent) ----
    day_length = 86400.0 * f_get_daylength(lat)
    fCalphax = P["fCalpha700"] / (2.0 - P["fCalpha700"])
    fCg0 = P["fCg700"] / (2.0 * P["fCg700"] - 1.0)
    month_vector = (np.arange(n_m) + month_i - 1) % 12 + 1

    Tmin_, Topt_, Tmax_ = P["Tmin"], P["Topt"], P["Tmax"]
    expo = (Tmax_ - Topt_) / (Topt_ - Tmin_)
    f_tmp = ((tave - Tmin_) / (Topt_ - Tmin_)) * ((Tmax_ - tave) / (Tmax_ - Topt_)) ** expo
    f_tmp = np.where((tave <= Tmin_) | (tave >= Tmax_), 0.0, f_tmp)
    tg_ = (tave + tmax) / 2
    f_tmp_gc = ((tg_ - Tmin_) / (Topt_ - Tmin_)) * ((Tmax_ - tg_) / (Tmax_ - Topt_)) ** expo
    f_tmp_gc = np.where((tg_ <= Tmin_) | (tg_ >= Tmax_), 0.0, f_tmp_gc)
    f_frost = 1.0 - P["kF"] * (frost / DAYS_IN_MONTH[month_vector - 1])
    f_calpha = fCalphax * co2 / (350.0 * (fCalphax - 1.0) + co2)
    f_cg = fCg0 / (1.0 + (fCg0 - 1.0) * co2 / 350.0)

    if soil_class > 0:
        SWconst, SWpower = 0.8 - 0.10 * soil_class, 11.0 - 2.0 * soil_class
    elif soil_class < 0:
        SWconst, SWpower = P["SWconst0"], P["SWpower0"]
    else:
        SWconst, SWpower = 999.0, P["SWpower0"]
    if asw_min > asw_max:
        asw_min = asw_max
    ASW = max(min(ASW, asw_max), asw_min)
    water_runoff_polled, poolFractn, Irrig = 0.0, 0.0, 0.0
    fN0 = 1.0 if P["fNn"] == 0 else P["fN0"]
    pfsPower = np.log(P["pFS20"] / P["pFS2"]) / np.log(20.0 / 2.0)
    pfsConst = P["pFS2"] / 2.0 ** pfsPower

    # ---- INITIALISATION (age dependent) ----
    age = (12.0 * (year_i - year_p) + month_i - month_p - 1.0 + np.arange(1, n_m + 1)) / 12.0
    age_m = age - 1.0 / 12.0
    age_m[0] = age[0]
    SLA = f_exp(age_m, P["SLA0"], P["SLA1"], P["tSLA"], 2.0)
    fracBB = f_exp(age_m, P["fracBB0"], P["fracBB1"], P["tBB"], 1.0)
    wood_density = f_exp(age_m, P["rho0"], P["rho1"], P["tRho"], 1.0)
    gammaN = f_exp(age, P["gammaN0"], P["gammaN1"], P["tgammaN"], P["ngammaN"])
    gammaF = f_exp_foliage(age_m, P["gammaF1"], P["gammaF0"], P["tgammaF"])
    if P["nAge"] == 0:
        f_age = np.ones(n_m)
    else:
        f_age = 1.0 / (1.0 + ((age_m / P["MaxAge"]) / P["rAge"]) ** P["nAge"])

    # ---- estado ----
    S = dict(stems_n=0.0, biom_stem=0.0, biom_foliage=0.0, biom_root=0.0, biom_foliage_debt=0.0,
             biom_tree=0.0, dbh=0.0, basal_area=0.0, height=0.0, lai=0.0, crown_length=0.0,
             crown_width=0.0, pFS=0.0, height_rel=0.0)

    def size_dist_correct(t):
        competition = wood_density[t] * S["basal_area"]
        h_rel = S["height"] / (S["height"] * S["stems_n"] / S["stems_n"])
        S["height_rel"] = h_rel
        dbh = (S["biom_tree"] / P["aWs"]) ** (1.0 / P["nWs"])
        S["dbh"] = dbh
        S["basal_area"] = dbh ** 2.0 / 4.0 * PI * S["stems_n"] / 10000.0
        if height_model == 1:
            S["height"] = P["aH"] * dbh ** P["nHB"] * competition ** P["nHC"]
            S["crown_length"] = (P["aHL"] * dbh ** P["nHLB"] * S["lai"] ** P["nHLL"] *
                                 competition ** P["nHLC"] * h_rel ** P["nHLrh"])
        elif height_model == 2:
            S["height"] = 1.3 + P["aH"] * np.exp(1.0) ** (-P["nHB"] / dbh) + P["nHC"] * competition * dbh
            S["crown_length"] = 1.3 + P["aHL"] * np.exp(1.0) ** (-P["nHLB"] / dbh) + P["nHLC"] * competition * dbh
        else:
            raise ValueError("height_model deve ser 1 ou 2")
        cw = (P["aK"] * dbh ** P["nKB"] * S["height"] ** P["nKH"] * competition ** P["nKC"] *
              h_rel ** P["nKrh"])
        S["crown_width"] = 0.0 if S["lai"] == 0 else cw
        S["pFS"] = pfsConst * dbh ** pfsPower
        if S["crown_length"] > S["height"]:
            S["crown_length"] = S["height"]

    def update_tree_lai(t):
        S["biom_tree"] = 0.0 if S["stems_n"] == 0 else S["biom_stem"] * 1000.0 / S["stems_n"]
        S["lai"] = S["biom_foliage"] * SLA[t] * 0.1

    def volume_now(t):
        if P["aV"] > 0:
            return (P["aV"] * S["dbh"] ** P["nVB"] * S["height"] ** P["nVH"] *
                    (S["dbh"] * S["dbh"] * S["height"]) ** P["nVBH"] * S["stems_n"])
        return S["biom_stem"] * (1.0 - fracBB[t]) / wood_density[t]

    rows = []
    month = month_i
    # ---- INITIALISATION (stand), ii = 1 ----
    t = 0
    if age[0] >= 0:
        S.update(stems_n=float(species["stems_n"]), biom_stem=float(species["biom_stem"]),
                 biom_foliage=float(species["biom_foliage"]), biom_root=float(species["biom_root"]))
    if f_dormant(month, leafgrow, leaffall):
        S["biom_foliage_debt"], S["biom_foliage"] = S["biom_foliage"], 0.0
    if age[0] >= 0:
        S["biom_tree"] = S["biom_stem"] * 1000.0 / S["stems_n"]
        S["dbh"] = (S["biom_tree"] / P["aWs"]) ** (1.0 / P["nWs"])
        S["basal_area"] = S["dbh"] ** 2.0 / 4.0 * PI * S["stems_n"] / 10000.0
        S["lai"] = S["biom_foliage"] * SLA[0] * 0.1
    competition = wood_density[0] * S["basal_area"]
    if height_model == 1:
        S["height"] = P["aH"] * S["dbh"] ** P["nHB"] * competition ** P["nHC"]
    else:
        S["height"] = 1.3 + P["aH"] * np.exp(1.0) ** (-P["nHB"] / S["dbh"]) + P["nHC"] * competition * S["dbh"]
    for _ in range(B_N):
        size_dist_correct(0)
    volume = volume_now(0)
    volume_cum = volume_old = volume
    volume_mai = volume_cum / age[0]
    volume_change = 0.0

    zero_flux = dict(gpp=0.0, npp_f=0.0, apar=0.0, alpha_c=0.0, f_vpd=0.0, f_sw=0.0, f_nutr=0.0,
                     f_phys=0.0, f_transp_scale=0.0, canopy_cover=0.0, transp_veg=0.0,
                     evapo_transp=0.0, prcp_interc=0.0, prcp_runoff=0.0, biom_loss_foliage=0.0,
                     biom_loss_root=0.0, biom_incr_foliage=0.0, biom_incr_root=0.0,
                     biom_incr_stem=0.0, mort_stress=0.0, mort_thinn=0.0,
                     wf_pre_defol=np.nan, biom_defol=0.0, defol_frac=0.0,
                     effic_loss=0.0, mort_induced=0.0, biom_mort_induced=0.0,
                     comp_ativa=0.0, comp_deficit=0.0, comp_U=1.0, comp_gc=1.0)
    F = dict(zero_flux)

    def record(t):
        rows.append(dict(
            date=(dates[t] + pd.offsets.MonthEnd(0)).date(), age=age[t], stems_n=S["stems_n"],
            basal_area=S["basal_area"], dbh=S["dbh"], height=S["height"], volume=volume,
            volume_mai=volume_mai, volume_change=volume_change, volume_cum=volume_cum,
            sla=SLA[t], lai=S["lai"], biom_stem=S["biom_stem"], biom_root=S["biom_root"],
            biom_foliage=S["biom_foliage"], biom_foliage_debt=S["biom_foliage_debt"],
            biom_tree=S["biom_tree"], wood_density=wood_density[t], fracBB=fracBB[t],
            f_age=f_age[t], f_tmp=f_tmp[t], f_frost=f_frost[t], f_calpha=f_calpha[t],
            gammaF=gammaF[t], asw=ASW, pFS=S["pFS"], **F))

    record(0)
    mort_stress = 0.0

    # ---- Monthly simulations, ii = 2..n_m ----
    for t in range(1, n_m):
        F = dict(zero_flux)
        month = month + 1
        if month > 12:
            month = 1
        b_cor = False
        if age[t] == 0.0:
            S.update(stems_n=float(species["stems_n"]), biom_stem=float(species["biom_stem"]),
                     biom_foliage=float(species["biom_foliage"]), biom_root=float(species["biom_root"]))
            b_cor = True
        dorm, dorm_prev = f_dormant(month, leafgrow, leaffall), f_dormant(month - 1, leafgrow, leaffall)
        if not dorm and dorm_prev:
            S["lai"] = S["biom_foliage_debt"] * SLA[t] * 0.1
            b_cor = True
        if dorm and not dorm_prev:
            S["biom_foliage_debt"], S["biom_foliage"], S["lai"] = S["biom_foliage"], 0.0, 0.0
            b_cor = True
        if b_cor:
            for _ in range(B_N):
                size_dist_correct(t)
            b_cor = False

        # ===== EXTENSÃO: evento de desfolha (início do mês, antes da luz) =====
        if defol[t] > 0.0 or (defoliation_events and dates[t].strftime("%Y-%m") in defoliation_events):
            wf_pre = S["biom_foliage"]
            removed = wf_pre * defol[t]
            S["biom_foliage"] = wf_pre - removed
            S["lai"] = S["biom_foliage"] * SLA[t] * 0.1
            F.update(wf_pre_defol=wf_pre, biom_defol=removed, defol_frac=defol[t])
            if comp is not None and removed > 0:
                wf_ref = max(wf_pre, wf_ref)
                t_ev = t
        # ===== EXTENSÃO v2: mortalidade induzida (início do mês) =====
        if mortind[t] > 0.0 and S["stems_n"] > 0:
            mk_ = mortind[t]
            rem_ = (S["biom_foliage"] + S["biom_root"] + S["biom_stem"]) * mk_
            for kk in ("biom_foliage", "biom_root", "biom_stem", "biom_foliage_debt"):
                S[kk] = S[kk] * (1.0 - mk_)
            dead_ = S["stems_n"] * mk_
            S["stems_n"] -= dead_
            update_tree_lai(t)
            for _ in range(B_N):
                size_dist_correct(t)
            F.update(mort_induced=dead_, biom_mort_induced=rem_)
        # =====================================================================

        comp_on = comp is not None and wf_ref > 0 and S["biom_foliage"] < wf_ref
        deficit = (1.0 - S["biom_foliage"] / wf_ref) if comp_on else 0.0
        if comp is not None and not comp_on:
            wf_ref = 0.0
        # Radiation and assimilation (s_light_3pgpjs)
        cc = 1.0
        if P["fullCanAge"] > 0 and age_m[t] < P["fullCanAge"]:
            cc = (age_m[t] + 0.01) / P["fullCanAge"]
        light_int = 1.0 - np.exp(-P["k"] * S["lai"] / cc)
        apar = srad[t] * DAYS_IN_MONTH[month - 1] * light_int * cc
        vpd_sp = vpd_day[t]

        f_vpd = np.exp(-P["CoeffCond"] * vpd_sp)
        f_sw = 1.0 / (1.0 + ((1.0 - ASW / asw_max) / SWconst) ** SWpower)
        f_nutr = 1.0 if P["fNn"] == 0 else 1.0 - (1.0 - fN0) * (1.0 - fertility) ** P["fNn"]
        f_phys = min(f_vpd, f_sw) * f_age[t]
        f_tmp_gc_t = 1.0  # phys_model = 1

        alpha_c = P["alphaCx"] * f_nutr * f_tmp[t] * f_frost[t] * f_calpha[t] * f_phys
        if S["lai"] == 0:
            alpha_c = 0.0
        if effic[t] > 0.0:  # EXTENSÃO v2: dano que reduz a eficiência sem remover folhas
            alpha_c = alpha_c * (1.0 - effic[t])
            F.update(effic_loss=effic[t])
        U_ef = 1.0
        if comp_on and alpha_c > 0 and (comp["u_meses"] is None or t - t_ev < comp["u_meses"]):  # EXTENSÃO v3: aumento da fotossíntese das folhas remanescentes
            U_ef = 1.0 + (comp["U"] - 1.0) * f_sw
            alpha_c = alpha_c * U_ef
        epsilon = P["gDM_mol"] * P["molPAR_MJ"] * alpha_c
        GPP = epsilon * apar / 100.0
        NPP = GPP * P["y"]

        # Water balance
        lai_total = S["lai"]
        lai_per = 0.0 if lai_total == 0 else S["lai"] / lai_total
        gC = P["MaxCond"]
        if lai_total <= P["LAIgcx"]:
            gC = P["MinCond"] + (P["MaxCond"] - P["MinCond"]) * lai_total / P["LAIgcx"]
        conduct_canopy = gC * lai_per * f_phys * f_tmp_gc_t * f_cg[t]
        gc_fac = 1.0
        if comp_on and comp["gam"] > 0 and gC > 0:  # EXTENSÃO v3: maior condutância por área foliar remanescente
            lai_ref = wf_ref * SLA[t] * 0.1
            gC_ref = P["MaxCond"] if lai_ref > P["LAIgcx"] else P["MinCond"] + (P["MaxCond"] - P["MinCond"]) * lai_ref / P["LAIgcx"]
            gc_fac = min((gC_ref / gC) ** comp["gam"], GC_CAP)
            conduct_canopy = conduct_canopy * gc_fac
        if vpd_sp == 0:
            transp = 0.0
        else:
            dl = day_length[month - 1]
            net_rad = P["Qa"] + P["Qb"] * (srad[t] * 10.0 ** 6.0 / dl)
            def_term = RHO_AIR * LAMBDA * (VPD_CONV * vpd_sp) * P["BLcond"]
            div = conduct_canopy * (1.0 + E20) + P["BLcond"]
            transp = DAYS_IN_MONTH[month - 1] * conduct_canopy * (E20 * net_rad + def_term) / div / LAMBDA * dl
            transp = max(0.0, transp)
        transp_total = transp
        interc_fract = P["MaxIntcptn"]
        if P["LAImaxIntcptn"] > 0:
            interc_fract = P["MaxIntcptn"] * min(1.0, lai_total / P["LAImaxIntcptn"]) * lai_per
        prcp_interc = prcp[t] * interc_fract
        ASW = ASW + prcp[t] + (100.0 * Irrig / 12.0) + water_runoff_polled
        evapo_transp = min(ASW, transp_total + prcp_interc)
        excessSW = max(ASW - evapo_transp - asw_max, 0.0)
        ASW = ASW - evapo_transp - excessSW
        water_runoff_polled = poolFractn * excessSW
        prcp_runoff = (1.0 - poolFractn) * excessSW
        if ASW < asw_min:
            ASW = asw_min
        if (transp_total + prcp_interc) == 0:
            f_transp_scale = 1.0
        else:
            f_transp_scale = evapo_transp / (transp_total + prcp_interc)
        GPP *= f_transp_scale
        NPP *= f_transp_scale
        NPP_f = NPP
        if transp_total > 0 and f_transp_scale < 1:
            transp = (evapo_transp - prcp_interc) / transp_total * transp

        # Biomass increment and loss
        m = P["m0"] + (1.0 - P["m0"]) * fertility
        fr_root = P["pRx"] * P["pRn"] / (P["pRn"] + (P["pRx"] - P["pRn"]) * f_phys * m)
        fr_stem = (1.0 - fr_root) / (1.0 + S["pFS"])
        fr_fol = 1.0 - fr_root - fr_stem
        if comp_on and comp["a"] > 0:  # EXTENSÃO v3: partição desviada para folhas durante o déficit
            mv = comp["a"] * deficit
            fr_fol = fr_fol + mv * (fr_stem + fr_root)
            fr_stem, fr_root = fr_stem * (1.0 - mv), fr_root * (1.0 - mv)
        if dorm:
            loss_f = 0.0 if dorm_prev else S["biom_foliage_debt"]
            loss_r = inc_f = inc_r = inc_s = 0.0
        else:
            if S["biom_foliage"] == 0.0:
                S["biom_foliage"] = S["biom_foliage_debt"]
            if NPP >= S["biom_foliage_debt"]:
                NPP = NPP - S["biom_foliage_debt"]
                S["biom_foliage_debt"] = 0.0
            else:
                S["biom_foliage_debt"] = S["biom_foliage_debt"] - NPP
                NPP = 0.0
            loss_f = gammaF[t] * S["biom_foliage"]
            loss_r = P["gammaR"] * S["biom_root"]
            inc_f, inc_r, inc_s = NPP * fr_fol, NPP * fr_root, NPP * fr_stem
            S["biom_foliage"] = S["biom_foliage"] + inc_f - loss_f
            S["biom_root"] = S["biom_root"] + inc_r - loss_r
            S["biom_stem"] = S["biom_stem"] + inc_s

        update_tree_lai(t)
        for _ in range(B_N):
            size_dist_correct(t)
        volume = volume_now(t)
        volume_change = volume - volume_old
        if S["lai"] == 0 or volume_change <= 0:
            volume_change = 0.0
        volume_cum = volume_cum + volume_change
        volume_old = volume
        volume_mai = volume_cum / age[t]

        # Mortality — stress related
        if not dorm:
            if gammaN[t] > 0:
                mort_stress = min(gammaN[t] * S["stems_n"] / 12.0 / 100.0, S["stems_n"])
                for kk, mk in (("biom_foliage", "mF"), ("biom_root", "mR"), ("biom_stem", "mS")):
                    S[kk] = S[kk] - P[mk] * mort_stress * (S[kk] / S["stems_n"])
                S["stems_n"] -= mort_stress
                b_cor = True
        else:
            mort_stress = 0.0
        if b_cor:
            update_tree_lai(t)
            for _ in range(B_N):
                size_dist_correct(t)
            b_cor = False

        # Mortality — self-thinning
        ba_prop = S["basal_area"] / S["basal_area"]
        stems_n_ha = S["stems_n"] / ba_prop
        biom_tree_max = P["wSx1000"] * (1000.0 / stems_n_ha) ** P["thinPower"]
        mort_thinn = 0.0
        if not dorm:
            if biom_tree_max < S["biom_tree"]:
                mort_thinn = f_get_mortality(stems_n_ha, S["biom_stem"] / ba_prop, P["mS"],
                                             P["wSx1000"], P["thinPower"]) * ba_prop
                if mort_thinn < S["stems_n"]:
                    for kk, mk in (("biom_foliage", "mF"), ("biom_root", "mR"), ("biom_stem", "mS")):
                        S[kk] = S[kk] - P[mk] * mort_thinn * (S[kk] / S["stems_n"])
                    S["stems_n"] -= mort_thinn
                else:
                    S.update(biom_foliage=0.0, biom_root=0.0, biom_stem=0.0, stems_n=0.0)
                b_cor = True
        if b_cor:
            update_tree_lai(t)
            for _ in range(B_N):
                size_dist_correct(t)

        F.update(gpp=GPP, npp_f=NPP_f, apar=apar, alpha_c=alpha_c, f_vpd=f_vpd, f_sw=f_sw,
                 f_nutr=f_nutr, f_phys=f_phys, f_transp_scale=f_transp_scale, canopy_cover=cc,
                 transp_veg=transp, evapo_transp=evapo_transp, prcp_interc=prcp_interc,
                 prcp_runoff=prcp_runoff, biom_loss_foliage=loss_f, biom_loss_root=loss_r,
                 biom_incr_foliage=inc_f, biom_incr_root=inc_r, biom_incr_stem=inc_s,
                 mort_stress=mort_stress, mort_thinn=mort_thinn,
                 comp_ativa=float(comp_on), comp_deficit=deficit, comp_U=U_ef, comp_gc=gc_fac)
        record(t)

    return pd.DataFrame(rows)
```

## experimentos/run_experimentos.py

```python
#!/usr/bin/env python3
"""
Executa a matriz computacional (E1–E6) no port verificado do r3PG (3-PGpjs) com o módulo de desfolha.
Saídas em experimentos/saida/: matriz_tratamentos.csv, mensal.csv.gz, config_execucao.json.

CONVENÇÃO TEMPORAL (única):
  * plantio hipotético: 2015-01 (todos os materiais);
  * A1 (Caldeira) inicializa aos 12 meses (from = 2016-01); C* (Borges) aos 3 meses (from = 2015-04),
    cada um com as biomassas iniciais publicadas na sua fonte;
  * fim: 2023-01 (idade 96 meses) = mês 84 da simulação de referência (A1);
  * "mês k" = mês k da simulação de referência = data 2016-01 + k meses = idade 12 + k meses;
  * pulso único: k = 12 (2017-01, idade 24 meses, estação chuvosa); recorrente: k = 12 e 48 (2020-01);
  * evento aplicado no INÍCIO do passo mensal, antes da interceptação de luz (módulo verificado).
SOLO:
  * ASWmax_ref = 190,6 mm (Indianópolis, 0–200 cm a 33 kPa; planilha 01_PARAMETROS p_ASWmax_33);
    níveis W = 25/50/75/100 % de ASWmax_ref; ASW0 = ASWmax (perfil cheio no início, janeiro);
  * FR: S100 = FR original de cada parametrização (A1 0,8; Borges 0,9); S25 = 0,5483 = FR para
    CTCe = 0 na função de Caldeira 2020 §2.10.4 (Alvares 2011), limite inferior admissível dessa função;
    S50/S75 = pontos equidistantes. Níveis ORDINAIS, não equivalem a 25–100 % de produtividade.
  * E2 exploratório: FR = 0,2…1,0 (abaixo de 0,5483 fica fora da faixa da função de Caldeira).
"""
import itertools, json, platform, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent / "modelo"))
from clones import MATERIAIS, params  # noqa: E402
from clima import SITIOS, clima_mensal  # noqa: E402
from threepg_pjs import run_3pg_pjs  # noqa: E402

SAIDA = AQUI / "saida"
ASW_REF = 190.6
FR_MIN_CTCE0 = 0.5483
PLANTIO = "2015-01"
FIM = "2023-01"
INICIO = {"A1": "2016-01"}  # Borges: 2015-04
EVENTOS = {"P1": ["2017-01"], "P2": ["2017-01", "2020-01"],
           "PA": [f"{a}-01" for a in range(2017, 2023)],          # anual: jan/2017 … jan/2022 (6 pulsos)
           "EA": ["2017-04"], "EJ": ["2017-07"], "EO": ["2017-10"]}  # épocas: abril, julho, outubro
# SOLO LOCAL (fontes secundárias; ver solos_fontes/SOLOS_LOCAIS.md)
SITIOS_MATRIZ = ["IND", "TB", "IMP"]  # matriz principal: os três locais originais (os locais por bioma rodam em run_biomas.py)
SOLO_LOCAL = {"IND": 215.0,   # TECHS sítio 9 (Estrela do Sul-MG, ~35 km), CAD 0–2 m (Stape) — Binkley et al. 2017, Tab. 2
              "TB": 214.0,    # TECHS sítio 22 (Telêmaco Borba-PR), CAD 0–2 m (Stape) — Binkley et al. 2017, Tab. 2
              "IMP": 210.0}   # SoilGrids 2.0 (7 pontos a ~9 km) + PTF-ZARC (Teixeira et al. 2021), 0–2 m
CAL_LOCAL = ["P1", "P2", "PA", "EA", "EJ", "EO"]
DEFOL = [0.0, 0.25, 0.50, 0.95]
NIVEIS = [25, 50, 75, 100]
MAT_PRINCIPAIS = ["A1", "C5", "C2", "C4"]
MAT_COMPLEMENTARES = ["C1", "C3"]


def fr_nivel(mat, nivel):
    ref = MATERIAIS[mat]["FR_ref"]
    j = NIVEIS.index(nivel)
    return round(FR_MIN_CTCE0 + j / 3 * (ref - FR_MIN_CTCE0), 4)


def linha(sitio, mat, wn, fr, frrot, d, cal, exp, asw=None):
    wrot = "LOC" if asw is not None else wn
    pid = f"{sitio}_{mat}_W{wrot}_{frrot}_D{int(round(d*100)):02d}_{cal if d > 0 else 'CTRL'}"
    return dict(id=pid, experimento=exp, sitio=sitio, material=mat, nivel_agua=wrot,
                asw_max=round(asw if asw is not None else ASW_REF * wn / 100, 3),
                nivel_FR=frrot, FR=fr, desfolha=d, calendario=cal if d > 0 else "CTRL",
                eventos=";".join(EVENTOS[cal]) if d > 0 else "", plantio=PLANTIO,
                inicio=INICIO.get(mat, "2015-04"), fim=FIM,
                apto_analise_principal=not (sitio == "IMP" and mat == "A1"),
                modelo="r3PG v0.1.7 3-PGpjs (port Python verificado) + módulo de desfolha v1")


def montar_matriz():
    L = []
    for s, m, wn, fn in itertools.product(SITIOS_MATRIZ, MAT_PRINCIPAIS, NIVEIS, NIVEIS):
        fr = fr_nivel(m, fn)
        L.append(linha(s, m, wn, fr, f"F{fn}", 0.0, "P1", "E1-E6"))
        for d, cal in itertools.product(DEFOL[1:], ["P1", "P2"]):
            L.append(linha(s, m, wn, fr, f"F{fn}", d, cal, "E1-E6"))
    for s, m, fr in itertools.product(SITIOS_MATRIZ, MAT_PRINCIPAIS, [0.2, 0.4, 0.6, 0.8, 1.0]):  # E2 exploratório
        for d in (0.0, 0.50):
            L.append(linha(s, m, 100, fr, f"FX{int(fr*100):03d}", d, "P1", "E2x"))
    for m, n in itertools.product(MAT_COMPLEMENTARES, NIVEIS):  # complementares, Indianópolis, solo combinado
        for d in DEFOL:
            L.append(linha("IND", m, n, fr_nivel(m, n), f"F{n}", d, "P1", "COMPL"))
    for s, m, fn in itertools.product(SITIOS_MATRIZ, MAT_PRINCIPAIS, NIVEIS):  # E7–E8: solo local, frequência anual e épocas
        fr = fr_nivel(m, fn)
        L.append(linha(s, m, None, fr, f"F{fn}", 0.0, "P1", "LOCAL", asw=SOLO_LOCAL[s]))
        for d, cal in itertools.product(DEFOL[1:], CAL_LOCAL):
            L.append(linha(s, m, None, fr, f"F{fn}", d, cal, "LOCAL", asw=SOLO_LOCAL[s]))
    M = pd.DataFrame(L).drop_duplicates("id").reset_index(drop=True)
    assert M.id.is_unique
    return M


_CLIMA = {}


def _clima(s):
    if s not in _CLIMA:
        _CLIMA[s] = clima_mensal(s)
    return _CLIMA[s]


def rodar(r):
    r = dict(r)
    mat = r["material"]; M = MATERIAIS[mat]
    site = dict(latitude=SITIOS[r["sitio"]]["lat"], altitude=0, soil_class=-1, asw_i=r["asw_max"], asw_min=0.0,
                asw_max=r["asw_max"], **{"from": r["inicio"], "to": r["fim"]})
    sp = dict(planted=r["plantio"], fertility=r["FR"], stems_n=10000 / 9,
              biom_stem=M["WS0"], biom_root=M["WR0"], biom_foliage=M["WF0"])
    ev = {e: r["desfolha"] for e in r["eventos"].split(";")} if r["eventos"] else None
    o = run_3pg_pjs(site, sp, _clima(r["sitio"]), params(mat), defoliation_events=ev)
    o.insert(0, "id", r["id"])
    o["idade_meses"] = (o.age * 12).round(6)
    o["mes_ref"] = (o.idade_meses - 12).round(6)          # mês k da simulação de referência
    o["biom_total"] = o.biom_stem + o.biom_foliage + o.biom_root
    o["lai_pos_defol"] = np.where(o.biom_defol > 0, (o.wf_pre_defol - o.biom_defol) * o.sla * 0.1, np.nan)
    return o


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    M = montar_matriz(); M.to_csv(SAIDA / "matriz_tratamentos.csv", index=False)
    t0 = time.time()
    with Pool(8) as p:
        res = p.map(rodar, M.to_dict("records"), chunksize=16)
    D = pd.concat(res, ignore_index=True)
    D.to_csv(SAIDA / "mensal.csv.gz", index=False, compression="gzip")
    json.dump(dict(n_tratamentos=len(M), n_linhas=len(D), segundos=round(time.time() - t0, 1),
                   python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                   asw_ref=ASW_REF, fr_min=FR_MIN_CTCE0, eventos=EVENTOS, plantio=PLANTIO, fim=FIM),
              open(SAIDA / "config_execucao.json", "w"), indent=2, ensure_ascii=False)
    print(len(M), "tratamentos;", len(D), "linhas;", round(time.time() - t0, 1), "s")
    print(M.groupby(["experimento"]).size().to_string())
```

## experimentos/indicadores.py

```python
#!/usr/bin/env python3
"""Indicadores tratamento × controle (mesmo sítio, material, água, FR; só a desfolha muda).
Critérios operacionais (definidos ANTES do cálculo):
  * perda relativa (%) = 100·(1 − trat/ctrl), no fim do mês k da simulação de referência;
  * recuperação ABSOLUTA: nº de meses após o evento até Wf_trat >= Wf imediatamente antes do evento;
  * recuperação RELATIVA: nº de meses após o evento até Wf_trat/Wf_ctrl >= 0,95;
    (para P2, a 1ª recuperação é censurada se não ocorrer antes do 2º evento);
    0 = recupera no próprio mês do evento; NaN = não recupera até o fim (censurado);
  * perda acumulada de NPP: Σ(NPP_ctrl − NPP_trat) do mês do 1º evento ao fim (t/ha) e % do Σ NPP_ctrl;
  * disponibilidade hídrica: 100·(1 − média ASW_trat / média ASW_ctrl) no mesmo intervalo
    (valor NEGATIVO = solo mais úmido no tratamento).
"""
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
S = AQUI / "saida"
KS = [12, 24, 48, 60, 72, 84]
VARS = {"biom_foliage": "Wf", "biom_stem": "Ws", "biom_total": "Wtotal", "lai": "LAI", "dbh": "DAP",
        "height": "altura", "volume": "volume"}


def carregar():
    M = pd.read_csv(S / "matriz_tratamentos.csv")
    cols = ["id", "date", "mes_ref", "idade_meses", "biom_foliage", "biom_stem", "biom_root", "biom_total", "lai",
            "dbh", "height", "volume", "npp_f", "gpp", "apar", "asw", "f_sw", "stems_n", "biom_defol",
            "wf_pre_defol", "lai_pos_defol", "biom_incr_foliage", "biom_incr_stem", "biom_incr_root"]
    D = pd.read_csv(S / "mensal.csv.gz", usecols=cols)
    D["mes_ref"] = D.mes_ref.round().astype(int)
    return M, D


def chave(M):
    return M.sitio + "|" + M.material + "|" + M.nivel_agua.astype(str) + "|" + M.nivel_FR + "|" + M.experimento


def calcular(M, D):
    M = M.copy(); M["grupo"] = chave(M)
    ctrl_id = M[M.desfolha == 0].set_index("grupo").id
    G = {i: g.set_index("mes_ref") for i, g in D.groupby("id")}
    linhas = []
    for r in M[M.desfolha > 0].itertuples():
        t, c = G[r.id], G[ctrl_id[r.grupo]]
        ev = [int(round((pd.Timestamp(e + "-01") - pd.Timestamp("2016-01-01")).days / 30.4375)) for e in r.eventos.split(";")]
        e1 = ev[0]; fim2 = ev[1] if len(ev) > 1 else None; fim3 = ev[2] if len(ev) > 2 else None
        out = dict(id=r.id, sitio=r.sitio, material=r.material, nivel_agua=r.nivel_agua, asw_max=r.asw_max,
                   n_eventos=len(ev), mes_evento=int(r.eventos.split(";")[0][5:7]), nivel_FR=r.nivel_FR, FR=r.FR,
                   desfolha=r.desfolha, calendario=r.calendario, experimento=r.experimento,
                   apto_analise_principal=r.apto_analise_principal)
        for k in KS:
            for v, rot in VARS.items():
                a, b = t.at[k, v], c.at[k, v]
                out[f"perda_{rot}_k{k}"] = 100 * (1 - a / b) if b > 0 else np.nan
        # evento 1: registro
        out["Wf_pre_ev1"] = t.at[e1, "wf_pre_defol"]; out["Wf_pos_ev1"] = t.at[e1, "wf_pre_defol"] - t.at[e1, "biom_defol"]
        out["biomassa_removida_total"] = t.biom_defol.sum()
        out["LAI_pre_ev1"] = t.at[e1 - 1, "lai"]; out["LAI_pos_ev1"] = t.at[e1, "lai_pos_defol"]
        out["APAR_ev1_trat"] = t.at[e1, "apar"]; out["APAR_ev1_ctrl"] = c.at[e1, "apar"]
        # recuperação
        janela = range(e1, (fim2 if fim2 else max(t.index) + 1))
        wf_pre = t.at[e1, "wf_pre_defol"]
        ab = next((m - e1 for m in janela if t.at[m, "biom_foliage"] >= wf_pre), np.nan)
        rel = next((m - e1 for m in janela if t.at[m, "biom_foliage"] / c.at[m, "biom_foliage"] >= 0.95), np.nan)
        out["recup_abs_meses_ev1"] = ab; out["recup_rel95_meses_ev1"] = rel
        if fim2:
            wf2 = t.at[fim2, "wf_pre_defol"]
            j2 = range(fim2, fim3 if fim3 else max(t.index) + 1)
            out["recup_abs_meses_ev2"] = next((m - fim2 for m in j2 if t.at[m, "biom_foliage"] >= wf2), np.nan)
            out["recup_rel95_meses_ev2"] = next((m - fim2 for m in j2
                                                 if t.at[m, "biom_foliage"] / c.at[m, "biom_foliage"] >= 0.95), np.nan)
        post = slice(e1, max(t.index))
        dn = (c.loc[post, "npp_f"] - t.loc[post, "npp_f"])
        out["perda_NPP_acum_tha"] = dn.sum(); out["perda_NPP_acum_pct"] = 100 * dn.sum() / c.loc[post, "npp_f"].sum()
        out["meses_NPP_trat_maior_ctrl"] = int((dn < -1e-9).sum())
        out["reducao_ASW_media_pct"] = 100 * (1 - t.loc[post, "asw"].mean() / c.loc[post, "asw"].mean())
        out["fSW_medio_trat"] = t.loc[post, "f_sw"].mean(); out["fSW_medio_ctrl"] = c.loc[post, "f_sw"].mean()
        out["arvores_final_trat"] = t.at[84, "stems_n"]; out["arvores_final_ctrl"] = c.at[84, "stems_n"]
        out["volume_k72_ctrl"] = c.at[72, "volume"]; out["volume_k72_trat"] = t.at[72, "volume"]
        out["LAI_max_ctrl"] = c.lai.max()
        linhas.append(out)
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    M, D = carregar()
    R = calcular(M, D)
    R.to_csv(S / "indicadores_por_tratamento.csv", index=False)
    # tabela longa de perdas por idade
    long = []
    for k in KS:
        for rot in VARS.values():
            sub = R[["id", "sitio", "material", "nivel_agua", "nivel_FR", "desfolha", "calendario", "experimento",
                     "apto_analise_principal", f"perda_{rot}_k{k}"]].rename(columns={f"perda_{rot}_k{k}": "perda_pct"})
            sub.insert(1, "variavel", rot); sub.insert(2, "mes_ref", k); sub.insert(3, "idade_meses", 12 + k)
            long.append(sub)
    pd.concat(long).to_csv(S / "perdas_por_idade_longo.csv", index=False)
    print(len(R), "tratamentos com desfolha avaliados")
```

## ferramentas/pipeline.py

```python
"""Pipeline único do TCC II. Cada etapa é um comando; `tudo` roda na ordem. Ao final de cada etapa bem-sucedida,
regenera a passagem de bastão e faz commit (se houver git).

Uso: python3 ferramentas/pipeline.py <etapa> [<etapa> ...]
Etapas: verificar, testes, calibracao, experimentos, indicadores, analises, danos, auditoria, tcc, plataforma, passagem, tudo
"""
import subprocess, sys, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PY = sys.executable
ETAPAS = {
    "verificar": [[PY, "-c", "import numpy, pandas, sklearn; print('python ok')"], ["node", "--version"]],
    "testes": [[PY, "-m", "pytest", "-q", "modelo/testes"]],
    "calibracao": [[PY, "calibrar.py", "0.999"], [PY, "calibrar.py", "0.99"], [PY, "calibrar_gamma.py"], [PY, "validacao_cruzada.py"],
                   [PY, "auditoria_calibracao.py"], [PY, "testes_adicionais.py"], [PY, "validacao_globulus.py"], [PY, "teste_oliveira2014.py"]],
    "experimentos": [[PY, "experimentos/run_experimentos.py"], [PY, "experimentos/controles.py"]],
    "indicadores": [[PY, "experimentos/indicadores.py"]],
    "analises": [[PY, "experimentos/analise.py"], [PY, "experimentos/estatisticas.py"],
                 [PY, "experimentos/validacao_kfold.py"], [PY, "experimentos/rf_figuras.py"]],
    "danos": [[PY, "experimentos/danos_v2.py"]],
    "biomas": [[PY, "experimentos/run_biomas.py"], [PY, "experimentos/rf_biomas.py"], [PY, "experimentos/morris_danos_biomas.py"]],
    "possibilidades": [[PY, "experimentos/possibilidades.py"], [PY, "experimentos/possibilidades_analise.py"]],
    "tabelas": [[PY, "tcc_docx/tabelas_dados.py"], ["node", "plataforma/extrair_material_tcc.js"], [PY, "plataforma/material_tcc.py"], [PY, "experimentos/figuras_novas.py"]],
    "auditoria": [[PY, "auditoria_final/auditar_numeros.py"]],
    "tcc": [["node", "gerar.js", "paginas.json"], ["node", "../ferramentas/conferir_texto_auditoria.js"]],
    "plataforma": [[PY, "plataforma/sincronizar_dados.py"], [PY, "plataforma/verificacao/comparar.py"], [PY, "plataforma/construir.py"]],
    "passagem": [[PY, "ferramentas/gerar_passagem.py"]],
}
CWD = {"calibracao": RAIZ / "calibracao", "tcc": RAIZ / "tcc_docx"}
ORDEM = ["verificar", "testes", "calibracao", "experimentos", "indicadores", "analises", "danos", "biomas", "possibilidades", "tabelas", "plataforma", "auditoria", "tcc"]


def commit(msg):
    if (RAIZ / ".git").exists():
        subprocess.run(["git", "-C", str(RAIZ), "add", "-A"], capture_output=True)
        subprocess.run(["git", "-C", str(RAIZ), "commit", "-q", "-m", msg], capture_output=True)
        # salva no GitHub (repositório privado Akademia); falha de rede não interrompe o trabalho
        r = subprocess.run(["git", "-C", str(RAIZ), "push", "-q", "origin", "HEAD:main"], capture_output=True, text=True, timeout=600)
        print("[git] enviado ao GitHub" if r.returncode == 0 else f"[git] push falhou (fica salvo localmente): {r.stderr.strip()[:200]}")


def rodar(etapa):
    t0 = time.time()
    for cmd in ETAPAS[etapa]:
        print(f"[{etapa}] $ {' '.join(cmd)}", flush=True)
        r = subprocess.run(cmd, cwd=CWD.get(etapa, RAIZ))
        if r.returncode != 0:
            print(f"[{etapa}] FALHOU (código {r.returncode}). A passagem de bastão foi atualizada com a falha registrada.")
            (RAIZ / "memoria/contexto_ativo.md").open("a", encoding="utf8").write(
                f"\n- FALHA na etapa `{etapa}` ({time.strftime('%d/%m %H:%M')}): comando `{' '.join(cmd)}`.\n")
            subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
            sys.exit(r.returncode)
    print(f"[{etapa}] ok em {time.time() - t0:.0f} s")
    if etapa != "passagem":
        subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
        commit(f"pipeline: etapa {etapa} concluída")


if __name__ == "__main__":
    pedidas = sys.argv[1:] or ["verificar"]
    for e in (ORDEM if pedidas == ["tudo"] else pedidas):
        if e not in ETAPAS:
            sys.exit(f"Etapa desconhecida: {e}. Opções: {', '.join(ETAPAS)}, tudo")
        rodar(e)
```

## solos_fontes/SOLOS_LOCAIS.md

```markdown
# Solo local de cada sítio: fontes secundárias e valores adotados

| Sítio | ASWmax adotado (0–2 m) | Fonte do valor adotado | Verificações cruzadas |
|---|---|---|---|
| Indianópolis-MG | 215 mm | Binkley et al. (2017), Tab. 2: TECHS sítio 9, Estrela do Sul-MG (−18,73; −47,92; ~35 km de Indianópolis). Latossolo (Oxisol), argila 80%, silte 9%, areia 11% (0–40 cm). CAD 0–2 m por Stape et al. (2004). | PTF-ZARC (Teixeira et al., 2021) com a textura do TECHS 9: 160 mm. SoilGrids 2.0 + PTF-ZARC (8 pontos a ~9 km): 209 mm (205–215). Planilha do projeto: 190,6 mm (33 kPa) e 310,9 mm (10 kPa). |
| Telêmaco Borba-PR | 214 mm | Binkley et al. (2017), Tab. 2: TECHS sítio 22, Telêmaco Borba-PR (Latossolo; argila 56%, silte 23%, areia 21%). CAD 0–2 m por Stape et al. (2004). | PTF-ZARC com a textura do TECHS 22: 213 mm. SoilGrids + PTF-ZARC: 231 mm (229–237). |
| Imperatriz-MA | 210 mm | SoilGrids 2.0 (Poggio et al., 2021), média de 7 pontos a ~9 km da sede, textura de 0–200 cm (argila média 35%) + PTF-ZARC (Teixeira et al., 2021, Eq. 9). | Nenhum sítio TECHS próximo. Os mais próximos (Urbano Santos-MA; Brejinho de Nazaré-TO) ficam a mais de 450 km e têm solos arenosos (Entisol). |

## Fertilidade
- **TECHS 9 (perto de IND):** soma de bases (K + Ca + Mg) = 3,8 mmolc dm⁻³. Pela função FR(CTCe) de Caldeira et al. (2020), FR ≥ 0,59. O Al trocável não foi publicado, então esse valor é um limite inferior.
- **TECHS 22 (TB):** soma de bases = 52,3 mmolc dm⁻³. FR(CTCe) = 1,09, limitado a 1,0.
- **IMP:** não há CTCe publicada. A CTC a pH 7 do SoilGrids não substitui a CTCe.
- **Decisão:** o FR local não foi imposto. Mantiveram-se os quatro níveis ordinais (F25–F100), que cobrem o intervalo 0,55–0,80/0,90. A condição de referência é F100, o FR usado nas calibrações originais com plantios adubados (todos os sítios TECHS foram adubados intensivamente).

## Arquivos
- `soilgrids_vizinhanca.json`, `soilgrids_pontos.csv`, `asw_ptfzarc_por_ponto.csv`
- `teixeira2021_zarc.pdf` (Equação 9)
- `binkley2017.pdf` (Tabelas 1 e 2; A1 em TB: 34 Mg ha⁻¹ ano⁻¹ de lenho entre 2 e 3 anos, IAF 3,8)
- `campoe2020.pdf`
```

## Não incluído (orçamento)
- nada
