# PROMPT_CLAUDE — comando para continuar a finalização do TCC II (AKADEMIA)

Você está assumindo a etapa de finalização do TCC II (AKADEMIA), repositório
https://github.com/beteixeira135-cmyk/Akademia. O Kimi fez uma auditoria SOMENTE LEITURA
(ver `handoff_claude/RELATORIO_AUDITORIA.md`). Não repita cegamente o trabalho dele: confira
os resultados, verifique as alterações e conclua a revisão editorial e científica com
independência.

## Regras inegociáveis (de AGENTS.md — releia-o na íntegra)
- Só dados secundários; NUNCA inventar dado, parâmetro, referência, DOI ou resultado.
- Distinguir verificação (código = equações), calibração (ajuste a dados) e validação
  (dados independentes). Não transformar ganhos simulados em benefício fisiológico real;
  não interpretar diferenças pequenas entre medianas como superioridade genética.
- Todo número do TCC precisa ser recalculável: `auditoria_final/auditar_numeros.py` deve
  passar após qualquer mudança.
- Preserve resultados, equações, parâmetros e arquivos originais; não altere o motor
  científico para melhorar a apresentação.
- Não faça alterações diretas na `main`: crie branch própria (ex.: `finalizacao-claude`),
  registre arquivos modificados, e faça merge apenas com autorização.
- `ferramentas/pipeline.py` faz commit e push para main ao final de cada etapa — não o use
  sem revisar esse comportamento.

## Antes de editar — verificação independente obrigatória
1. Confirme acesso; identifique branch padrão e HEAD exatos; registre o commit de origem.
2. LEIA `memoria/contexto_ativo.md`, `memoria/progresso.md`, `PASSAGEM_DE_BASTAO.md`.
3. Resolva a questão F1 do relatório do Kimi: os números do briefing anterior (10.428
   cenários, 180 ganhos, máx. 7,5%, 66 só-desfolha, medianas C1…A1 8,6–10,2%) NÃO existem
   no repo versionado. PERGUNTE AO AUTOR de onde vêm antes de usá-los. Se não houver
   confirmação e fonte recalculável, mantenha os números já auditados (7.584 cenários;
   ganho máx. 5,2%; 12 ganhos só-desfolha; materiais A1/C2/C4/C5; 6 locais).
4. Disponibilize Node.js, `fontes_r3PG/data-raw` e `experimentos/saida/mensal.csv.gz`;
   rode `python3 ferramentas/pipeline.py verificar`.

## Tarefas
1. Corrigir `tcc_docx/conteudo.js`: parametrizar o caminho `FIG` (hoje hard-coded
   `/home/claude/tcc/...`, achado F3) e conferir todas as `fig:` com caminhos absolutos.
2. Conferir a Figura 10 (`N3_possibilidades.png`) e sua origem em
   `experimentos/figuras_novas.py`; localizar e conferir a "Figura 4" citada no briefing
   (o Kimi não a localizou — a leitura dele truncou o miolo do conteudo.js).
3. Ler o miolo de `conteudo.js` (trecho entre a Figura 1 e a Figura N1) e as seções 4.3,
   4.5, 4.8: o briefing pedia "4.3, 4.5 e 4.10", mas 4.10 NÃO existe no documento —
   confirmar com o autor a que seção ele se refere.
4. Pesquisar afirmações antigas no documento inteiro (ex.: "seis materiais", "C1", "C3",
   "10.428", "180 ganhos", "66") e remover/corrigir o que não tiver fonte no repo.
5. Conferir resumo, resultados, discussão e conclusão contra `auditar_numeros.py`;
   revisar tabelas, legendas, quantis e referências cruzadas (tabelas geradas por
   `tcc_docx/tabelas_dados.py`, sem número digitado).
6. Distinguir, no texto, simulação / comparação com literatura / validação empírica
   (o texto atual já o faz em vários pontos — manter o padrão).
7. Rodar a auditoria numérica completa e só então gerar DOCX (`gerar.js`) e PDF
   (LibreOffice), na branch de finalização.
8. Ao terminar: atualize `memoria/`, rode `ferramentas/gerar_passagem.py`, faça commit
   descritivo na branch de finalização (não na main) e atualize esta pasta `handoff_claude/`
   com o estado final, branch, commit e links.

## Critérios de conclusão
- DOCX e PDF finais gerados na branch de finalização; Figura 10 conferida/regenerada;
  auditoria numérica passando; relatório de auditoria atualizado; pendências remanescentes
  listadas; pacote de handoff atualizado. Merge na main somente com autorização expressa.

