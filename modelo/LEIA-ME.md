# Modelo — 3-PGpjs (tradução do r3PG v0.1.7) + módulo de desfolha

## Arquivos
- `threepg_pjs.py`: tradução do núcleo 3-PGpjs (`src/md_3PG.f95`, r3PG commit e39bd8e9) mais a EXTENSÃO de desfolha.
- `testes/test_modulo_desfolha.py`: 28 testes automatizados (pytest).
- `testes/dados_referencia_r3pg.py`: carrega os dados de exemplo do r3PG (`data-raw/*.xlsx`).
- `testes/comparar_vba.py` e `testes/saida_comparacao_vba.csv`: comparação mensal com o 3-PG original em Excel/VBA.

## Como executar
```bash
git clone https://github.com/trotsiuk/r3PG.git fontes_r3PG     # dados de referência
export R3PG_SRC=$PWD/fontes_r3PG
cd modelo && python3 -m pytest -q testes/                      # 28 passed
```
Requisitos: Python ≥ 3.10, numpy, pandas, openpyxl, pytest. Para `comparar_vba.py`, também xlrd.

## Uso
```python
from threepg_pjs import run_3pg_pjs, params_from_table, pulsos
ev = pulsos("2014-12", [12, 48], 0.50)          # {'2015-12': 0.5, '2018-12': 0.5}
out = run_3pg_pjs(site, species, clima, params, defoliation_events=ev)
```
`params_from_table` recusa qualquer parâmetro sem valor: lacunas não são preenchidas.

## Registro de alterações em relação ao r3PG original
| # | Alteração | Tipo |
|---|---|---|
| 1 | Tradução Fortran para Python restrita a 3-PGpjs, 1 espécie, sem viés/desbaste/d13C | reimplementação; verificada contra os testes oficiais |
| 2 | Evento de desfolha no início do mês, antes da luz: Wf ← Wf(1−d); LAI recalculado | **extensão do modelo** |
| 3 | Novo fluxo de saída `biom_defol`, mais `wf_pre_defol` e `defol_frac` | **extensão (somente saída)** |
| 4 | Saída `mort_thinn` = 0 nos meses sem autodesbaste (no Fortran ela mantém o valor do mês anterior) | só afeta a variável de saída; não altera a dinâmica |
Nenhuma equação original foi modificada.
