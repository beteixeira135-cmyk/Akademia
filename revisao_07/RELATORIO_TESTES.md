# Relatório de testes e reprodutibilidade (Missão 07)

Ambiente: Python 3.13; numpy, pandas, scikit-learn e networkx; Node 22 (docx); LibreOffice para o PDF. Repositório: github.com/beteixeira135-cmyk/akademia.

| Verificação | Comando | Resultado |
|---|---|---|
| Testes do modelo, versões 1 a 3 | `python3 -m pytest -q modelo/testes` | 49 aprovados |
| Testes do pipeline experimental | `python3 -m pytest -q experimentos/testes` | 8 aprovados |
| Auditoria numérica do texto | `python3 auditoria_final/auditar_numeros.py` | 363 de 363 conferidos (eram 336 antes da revisão) |
| Reexecução da calibração | `cd calibracao && python3 auditoria_calibracao.py` | Quantis idênticos aos publicados |
| Testes adicionais (Matrangolo, Quentin 2011 e 2012) | `cd calibracao && python3 testes_adicionais.py` | `saida/testes_adicionais.json` |
| Busca Crossref | `cd revisao_07/busca && python3 crossref_busca.py && python3 filtrar.py && python3 bibliometria.py` | 10.000 registros baixados → núcleo de 93 |
| Busca OpenAlex | `python3 openalex_busca.py` | **Pendente:** limite diário esgotado em 31/10/2026 |
| Geração do TCC | `cd tcc_docx && node gerar.js paginas.json`, conversão para PDF e `python3 paginas.py` (repetir até estabilizar) | 53 páginas; sumário e listas sem páginas faltando |

A busca Crossref usa `sort=score`, que depende do índice do dia, por isso não é determinística entre datas. Os registros baixados ficam em `revisao_07/busca/crus/` e garantem a reprodutibilidade das etapas seguintes.
