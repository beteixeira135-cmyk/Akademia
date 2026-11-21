# RELATORIO_AUDITORIA — diagnóstico da etapa Kimi (somente leitura, 20/11/2026)

Escopo: inspeção do estado real do repositório (branch main @ 3fd3481) e auditoria de
consistência do briefing de finalização contra os arquivos versionados. Nenhum número novo
foi inventado; onde a leitura foi truncada, está marcado [não verificado].

## F1 — CRÍTICO: os números de referência do briefing não existem no repositório
O briefing manda usar como referência: 180 ganhos em 10.428 cenários (~1,7%); ganho máx. 7,5%;
Imperatriz 103; Indianópolis 58; 66 ganhos só-desfolha; medianas calibradas C1 8,6% … A1 10,2%.
O que o repositório versiona e audita (`auditoria_final/auditar_numeros.py`, que recalcula cada
número do texto):

| Grandeza | Briefing | Repositório (auditado) |
|---|---|---|
| Cenários do espaço de possibilidades | 10.428 | 7.584 totais; 5.688 aptos (2.844/versão) |
| Casos com ganho (calibrada) | 180 (~1,7%) | 1,3% dos aptos; original: 1 cenário (0,1%) |
| Ganho máximo | 7,5% | 5,2% (calibrada); 0,1% (original) |
| Ganhos só-desfolha | 66, em todos os materiais | 12 (calibrada), 10 com d 25–50%; original: 1, só em TB |
| Materiais | "seis" (C1…C5, A1) | 4 (A1, C2, C4, C5); 6 locais |
| Medianas calibradas C1…A1 | 8,6–10,2% | não constam em arquivo versionado |

Conclusão: não há commit alcançável da "matriz de seis materiais". Os números do briefing
podem vir de trabalho local não commitado, de outra máquina/sessão, ou estar defasados.
**Ação: confirmar origem com o autor ANTES de qualquer alteração no texto. O padrão do
projeto (AGENTS.md) proíbe número sem fonte recalculável.**

## F2 — CONFIRMADO: números do manuscrito batem com a auditoria versionada
O `resumo`/`abstract` e o corpo de `tcc_docx/conteudo.js` foram lidos e confrontados com
`auditar_numeros.py`. Consistentes: perdas A1 IND 1,6–9,5% e TB 1,2–15,2%; ataques anuais até
58/68%; R² = 1,000 nos 308 controles; erro A1 20,3 → 7,5 p.p.; LOO 15,7 → 4,3 p.p.; Oliveira
33,0% (28,1–45,8%) vs 35,4% medidos, 77,6% original; Matrangolo 37,9–79,7% observado vs
7,4–32,1% (original) e 3,8–11,5% (calibrado); 5.688 cenários; ganho máx. 5,2% (Fig. 10a);
"perda de eficiência e mortalidade, sozinhas, nunca deram ganho" — bate com o chk
"só eficiência ganho 0,0" e "só mortalidade ganho 0". A redação do §4.6 já trata os ganhos
como resultado simulado, sem causa biológica — conforme exigido.

## F3 — CONFIRMADO: caminho absoluto hard-coded no manuscrito
`conteudo.js`, linha do cabeçalho: `const FIG = "/home/claude/tcc/experimentos/saida/figuras/"`
(e `FIGD = FIG`; há ainda figuras com `/home/claude/tcc/plataforma/...`). É resíduo da
máquina do Claude: em outro computador o `gerar.js` não encontra as figuras.
**Correção proposta (não aplicada — sem escrita): parametrizar FIG via variável de ambiente
ou caminho relativo ao repo.** É a única alteração de código identificada como necessária
na leitura feita.

## F4 — Estrutura do manuscrito vs. briefing
- §4.5 existe ("OUTROS DANOS E BIOMAS") e está coerente com os chk de biomas (T11, razões
  cal/orig 43%/53%, faixa 90% 3,0–12,0).
- **Não existe §4.10** — a numeração vai até §4.8 (LIMITAÇÕES) + conclusão. O briefing pede
  "atualizar 4.3, 4.5 e 4.10": 4.5 existe; 4.10 não existe no documento versionado.
  [não verificado: §§4.3–4.4 inteiriços — a leitura web truncou o meio do arquivo; conferir
  localmente o trecho entre a Figura 1 e a Figura N1.]
- "Figura 10" do texto = `N3_possibilidades.png` (espaço de possibilidades), gerada por
  `experimentos/figuras_novas.py`/possibilidades — corresponde à §4.6. "Figura 4" não pôde
  ser localizada na leitura truncada [não verificado].

## F5 — O que NÃO pôde ser verificado nesta etapa (limitações de ambiente)
- Conteúdo binário das figuras (F1…, N1…N3) — não regenerável aqui: faltam `mensal.csv.gz`,
  `fontes_r3PG/data-raw` e Node.js, todos locais/ignorados pelo Git.
- Execução de `auditar_numeros.py` (exige Node para `numeros_plataforma.js` e as saídas locais).
- Trecho intermediário de `conteudo.js` (~16,9 mil caracteres não exibidos pela leitura web).

## Correções aplicadas nesta etapa
Nenhuma no repositório (acesso somente leitura). Entregue: este diagnóstico + pacote de
handoff + correção F3 especificada para aplicação pelo Claude com escrita.

