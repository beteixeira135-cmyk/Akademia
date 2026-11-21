# ESTADO_ATUAL — estado real do projeto (verificado em 20/11/2026)

## Repositório e commits
- Repo: https://github.com/beteixeira135-cmyk/Akademia (privado)
- Branch padrão: `main`, HEAD = `3fd3481` ("Merge pull request #1 from
  beteixeira135-cmyk/beteixeira135-cmyk-recuperacao-e-persistencia", 19/11/2026).
- Outra branch: `beteixeira135-cmyk-recuperacao-e-persistencia` (já mesclada na main via PR #1).
- Últimos commits: 3fd3481 (merge PR#1), f786c46 (Record simulator display verification),
  9db14c9 (Improve Akademia simulator page rendering), 776d5d2, 71bfe9f, 68a6bd8, 2b475e9,
  c7cbbc5, 824aaf7 (todos de 19/11/2026; os anteriores são de 02–03/11).

## O que EXISTE no HEAD (árvore completa conferida)
- `AGENTS.md` (= `CLAUDE.md`), `README.md`, `PASSAGEM_DE_BASTAO.md` (gerado 19/11/2026 11:56),
  `CONTEXTO_EMPACOTADO.md`, `DIARIO_TCC_II.md`, `RELATORIO_ETAPAS_INDEPENDENTES.md`,
  `AUDITORIA_PLANILHA_CALDEIRA.md`.
- `modelo/` (threepg_pjs.py v3 com compensação opcional + testes), `experimentos/`
  (matriz, indicadores, RF, Morris, danos; `possibilidades.py` e `possibilidades_analise.py`),
  `calibracao/` (bayesiana, saídas d099/d0999, validação cruzada, Oliveira, globulus),
  `biomas/`, `clima/power_api/`, `solos_fontes/`, `cenarios/`, `revisao_07/` (busca bibliográfica),
  `auditoria_final/` (`auditar_numeros.py`, `auditoria_numeros.csv`, fixture de controles),
  `tcc_docx/` (`conteudo.js`, `gerar.js`, `tabelas_dados.py`, estrutura/paginas),
  `plataforma/`, `memoria/` (contexto_ativo, progresso, decisoes), `tcc1/`, `ferramentas/`.

## O que NÃO existe no HEAD (procurado, não encontrado)
- `tcc_final/`, `fechamento_tcc/` (erro 404 na árvore).
- `PENDENCIAS_FORA_DO_TEXTO.md` em nenhum nível.
- `possibilidades_6mat.py` — existe `possibilidades.py` + `possibilidades_analise.py`.
- CSV de "matriz de seis materiais" e qualquer rastro de 10.428 cenários / 180 ganhos / 66
  ganhos só-desfolha nos arquivos versionados.
- "Skill akademia-research-engine-v2" — nenhum arquivo de skill no repo.
- Materiais "C1, C3" — os materiais versionados são **A1, C2, C4, C5** (A1 = Caldeira et al.
  2020a; C5/C2/C4 = Borges 2009). "Seis" no projeto refere-se aos **seis locais**
  (IND, TB, IMP, ALM, ARA, ELD), não a seis materiais.

## Estado funcional (de `memoria/progresso.md` e `contexto_ativo.md`, 19/11)
- Calibração reexecutada: U = 1,18 (IC90% 1,01–1,34), a = 0,625 (0,225–0,975), γ = 1.
- Suítes: 57 testes aprovados; verificação JS×Python ok (dif. máx 1,6e-13).
- **Pendências registradas pelo próprio projeto**: (1) Node.js fora do PATH — auditoria
  numérica (`auditar_numeros.py`) e geração do DOCX **não concluídas**; (2) DOCX/PDF finais
  não gerados; (3) inventários TECHS 9/22 não obtidos — benchmark adaptado, sem validação
  independente; (4) `experimentos/saida/mensal.csv.gz` e `fontes_r3PG/data-raw` são locais
  e gitignored, necessários para reprocessar tudo.
- `ferramentas/pipeline.py` faz commit e push para main ao final de cada etapa — não usar
  sem revisar (alerta do próprio README).

