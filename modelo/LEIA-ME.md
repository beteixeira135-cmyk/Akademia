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

## Transferência exploratória do modificador de Bown et al. (2013)
`fn_soil.py` implementa, somente como cálculo candidato, a equação publicada para
`fN` a partir do nitrogênio total do solo (%) e da razão C:N, medidos nos primeiros 10 cm:
`fN = 1.32 + 0.99 * N_pct - 0.04 * C:N`.
O estudo original usou 10 miniparcelas de *Pinus radiata* na Nova Zelândia. A
aplicação a eucalipto brasileiro é uma transferência não validada. A função retorna
a equação sem truncar valores. Ela ainda não é ligada ao motor: `species["fertility"]`
é um FR que o 3-PG transforma internamente em `f_nutr`, portanto a correspondência
entre esse FR e o `fN` estimado por Bown precisa ser estabelecida antes da integração.
```python
from fn_soil import fN_bown
fN_candidate = fN_bown(N_pct, cn_ratio)
```
Os dados brasileiros reunidos no TCC não incluem N total e C:N pareados, na mesma
profundidade, com produtividade observada; portanto, a equação não foi usada nas
simulações nem calibrada ou validada para o Brasil. O módulo principal permanece
inalterado.

## Registro de alterações em relação ao r3PG original
| # | Alteração | Tipo |
|---|---|---|
| 1 | Tradução Fortran para Python restrita a 3-PGpjs, 1 espécie, sem viés/desbaste/d13C | reimplementação; verificada contra os testes oficiais |
| 2 | Evento de desfolha no início do mês, antes da luz: Wf ← Wf(1−d); LAI recalculado | **extensão do modelo** |
| 3 | Novo fluxo de saída `biom_defol`, mais `wf_pre_defol` e `defol_frac` | **extensão (somente saída)** |
| 4 | Saída `mort_thinn` = 0 nos meses sem autodesbaste (no Fortran ela mantém o valor do mês anterior) | só afeta a variável de saída; não altera a dinâmica |
Nenhuma equação original foi modificada.
