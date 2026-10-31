# Protocolo das buscas bibliográficas (Missão 07, etapa 3)

Data de execução: 31/10/2026. Período: 1997-01-01 a 2026-10-31. Scripts em `revisao_07/busca/`.

## Bases e situação

| Base | Situação em 31/10/2026 | Uso |
|---|---|---|
| Crossref (api.crossref.org) | Acessível | Base principal desta execução |
| OpenAlex (api.openalex.org) | "Rate limit exceeded": orçamento diário compartilhado, sem chave, esgotado. Volta às 00h UTC. | `openalex_busca.py` pronto para rodar com as expressões booleanas abaixo |
| SciELO (search.scielo.org) | HTTP 403 no ambiente de execução | Não consultada |
| Scopus, Web of Science | Sem acesso institucional nesta sessão | Não consultadas |
| Repositórios institucionais e Embrapa | Sem API de busca em lote acessível | Trabalhos localizados por busca na web e citação em cadeia, registrados nas fichas |

## Grupos de descritores

| Grupo | Descritores |
|---|---|
| D — Desfolha | defoliation, defoliated, herbivory, insect damage, leaf removal, foliar damage, leaf damage, leaf loss, pest damage, crown damage, defoliator, desfolha, desfolhamento |
| E — Eucalipto | Eucalyptus, eucalypt, eucalipto, Corymbia |
| F — Fisiologia | photosynthesis, carbon allocation/partitioning, biomass allocation, canopy conductance, stomatal, transpiration, leaf area index, carbohydrate, non-structural, regrowth, compensation, recovery |
| M — Modelos | 3-PG, r3PG, 3-PGmix, CABALA, process-based, ecophysiological/physiological model, CenW, G'DAY, BIOME-BGC, Forest-BGC, PnET, LPJ, CABLE, growth model |
| A — Ambiente | drought, water stress/deficit/availability, soil water, fertilisation/fertilization, nitrogen, nutrient, temperature, climate change, VPD, vapour pressure |
| V — Avaliação | calibration, Bayesian, validation, independent test, uncertainty, sensitivity analysis |

## Expressões booleanas

**OpenAlex**, aplicadas a título e resumo:
- O01: D AND E
- O02: D AND E AND F
- O03: D AND M
- O04: D AND E AND A
- O05: D AND M AND V
- O06: ("3-PG" OR r3PG OR "3-PGmix") AND E
- O07: (desfolha OR desfolhamento OR herbivoria) AND (eucalipto OR Eucalyptus)

**Crossref.** Esta base não aceita booleanos. Por isso foram feitas 20 consultas de texto livre (C01–C20), ordenadas por relevância (`sort=score`), com os 500 primeiros registros de cada uma. Depois, o filtro booleano foi aplicado localmente (`filtrar.py`) sobre título, resumo (quando o Crossref fornece) e assuntos:
- **núcleo:** D AND (E OR (modelo processual AND árvore/floresta));
- **contexto 3-PG:** (3-PG OR r3PG OR 3-PGmix) AND (E OR V);
- **indicadores:** D, E, P (pragas e doenças), BR (Brasil), F, M, A e V, usados nas interseções.

Consultas Crossref: C01 eucalyptus defoliation growth · C02 eucalypt defoliation · C03 eucalyptus herbivory insect damage growth · C04 eucalyptus artificial defoliation leaf removal · C05 eucalyptus defoliation photosynthesis compensation · C06 defoliation photosynthetic upregulation carbon allocation trees · C07 defoliation canopy conductance transpiration trees · C08 defoliation carbohydrate reserves regrowth trees · C09 3-PG model defoliation · C10 3-PG forest growth model pest insect damage · C11 CABALA model defoliation eucalyptus · C12 process-based forest model insect defoliation net primary production · C13 eucalyptus defoliation drought water stress · C14 eucalyptus defoliation nitrogen fertilisation · C15 3-PG eucalyptus calibration validation · C16 3-PG Bayesian calibration · C17 desfolha eucalipto crescimento · C18 desfolhamento artificial eucalipto · C19 lagarta desfolhadora eucalipto perda · C20 forest model defoliation uncertainty sensitivity analysis.

O total relatado e o número baixado por consulta estão em `busca/log_consultas_crossref.csv`. O total relatado pelo Crossref inclui correspondências parciais de palavras e não equivale ao número de documentos relevantes.

## Fluxo de seleção

| Etapa | Registros |
|---|---|
| Baixados (20 × 500) | 10.000 |
| Únicos por DOI | 7.908 |
| Após remover títulos repetidos (versões e preprints) | 7.431 |
| Excluídos por tipo (dataset 422, peer-review 158, other 52, component 14, reference-book 3, proceedings 3, database 2, journal-issue 1) | 655 |
| Excluídos por não atenderem à expressão do núcleo | 6.683 |
| **Núcleo** | **93** (81 artigos, 2 revisões, 6 preprints, 3 capítulos, 1 em anais) |
| Contexto 3-PG | 20 |

Arquivos de saída:
- `corpus/corpus_bruto_deduplicado.csv`, com o motivo de exclusão de cada registro;
- `corpus/corpus_nucleo.csv` e `corpus/corpus_nucleo.bib`;
- `corpus/corpus_contexto_3pg.csv`;
- `corpus/exclusoes.csv`.

## Limitações do protocolo
1. O Crossref não indexa palavras-chave de autor e só tem resumo em 45 dos 93 documentos do núcleo, então o filtro depende muito do título.
2. Afiliações estão presentes em apenas 18 registros do núcleo, o que inviabiliza análise por instituição.
3. Teses, dissertações e literatura técnica brasileira sem DOI ficam sub-representadas. Por exemplo, Bertulio et al. (2008) não tem DOI e não aparece no corpus, mas foi lido diretamente.
4. A frequência de termos não prova ausência de pesquisa. As lacunas apontadas são da amostra, não da literatura.
5. A complementação com o OpenAlex é necessária para fechar a análise. O script está pronto e o resultado deve substituir os indicadores desta versão.
