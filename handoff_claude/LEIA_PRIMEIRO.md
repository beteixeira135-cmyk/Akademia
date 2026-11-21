# LEIA_PRIMEIRO — passagem de bastão Kimi → Claude

## Ordem de leitura
1. Este arquivo.
2. `ESTADO_ATUAL.md` — o que existe de verdade no repositório (commit, branches, arquivos).
3. `RELATORIO_AUDITORIA.md` — diagnóstico: o que bate, o que conflita, o que foi corrigido.
4. `DECISOES_E_LIMITACOES.md` — decisões tomadas nesta etapa e questões abertas.
5. `FLUXOGRAMAS_METODOS.md` — cinco fluxogramas prontos para o Material e Métodos.
6. `PROMPT_CLAUDE.md` — comando completo para continuar.

## Em uma frase
O Kimi (Kimi Chat, Moonshot AI) auditou o repositório em modo **somente leitura** nesta etapa:
verificou acesso, leu o estado real do projeto, confrontou o briefing de finalização com os
arquivos versionados e produziu este pacote. **Nenhum commit foi feito por ele** (sem
credencial de escrita). Os arquivos desta pasta devem ser commitados por quem tem acesso.

## O ponto crítico descoberto nesta etapa
O briefing de finalização ("INSTACOMANDO — AKADEMIA") cita uma "matriz atualizada de seis
materiais" (10.428 cenários, 180 ganhos, ganho máx. 7,5%, Imperatriz 103, Indianópolis 58,
66 ganhos só-desfolha, medianas calibradas C1…A1) e pastas/arquivos (`tcc_final/`,
`fechamento_tcc/`, `PENDENCIAS_FORA_DO_TEXTO.md`, `possibilidades_6mat.py`).
**Nada disso existe no repositório** (árvore completa verificada via API, commit 3fd3481).
Os números versionados e auditados são outros (7.584 cenários, 5.688 aptos, 1 ganho original,
1,3% calibrado com máx. 5,2%, 12 ganhos só-desfolha). Ver `RELATORIO_AUDITORIA.md`, achado F1.
**Não importar os números do briefing para o texto sem confirmar a origem deles com o autor.**

