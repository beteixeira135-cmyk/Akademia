# Estatísticas de avaliação — o que cada uma comprova

**Métricas:** as mesmas de Castro et al. (artigo RNA *Khaya*): R², r(yŷ) e RQEM %, acrescidas de viés e MAE. O teste de Graybill só foi calculado onde n ≥ 5 e há variação. Script: `estatisticas.py`.

## A — Verificação do código (a implementação faz o que o 3-PG faz)
| Comparação | n (pares mês-variável) | R² | r(yŷ) | RQEM % | Viés % |
|---|---|---|---|---|---|
| Port × **r3PG original** (R), 260 controles, Ws/Wf/Wr/volume/LAI/DAP | 23.873 por variável | 1,000000 | 1,000000 | ≤ 2×10⁻¹³ | ≤ 4×10⁻¹⁵ |
| Port × **3-PG Excel/VBA** (Pinus, perenifólia), 6 variáveis | 110 | 0,99964–0,99999 | ≥ 0,9998 | 0,007–0,13 | ≤ 0,04 |
| Port × **3-PG Excel/VBA** (Fagus, decídua), 6 variáveis | 110 | 1,0000 | 1,0000 | ≤ 0,021 | ≤ 0,003 |

**Comprova:** o modelo usado é numericamente o r3PG. A diferença pequena em relação ao VBA vem das diferenças conhecidas entre r3PG e VBA.
**Complementos:** 36 testes automatizados (conservação de massa, calendário, 0% = controle, sem dupla aplicação, não negatividade, sem mortalidade induzida) e teste de mutação.

## B — Simulado × observado (Bertulio et al. 2008, híbridos, Campo Verde-MT)
Valores absolutos. Testemunha e desfolha aos 14 e 26 meses, n = 4 por variável:

| Material sim. → alvo | d sim. | Variável | R² | r(yŷ) | RQEM % | Viés % |
|---|---|---|---|---|---|---|
| C5 → urograndis | 0,95 | CAP | 0,76 | 0,92 | 7,6 | −0,7 |
| C5 → urograndis | 0,95 | altura | 0,68 | 1,00 | 12,2 | −12,2 |
| C5 → urograndis | 0,95 | volume/árvore | −0,61 | 0,96 | 70,1 | −61,4 |
| A1 → urocam | 0,95 | CAP | 0,92 | 0,99 | 5,8 | −4,3 |
| A1 → urocam | 0,95 | volume/árvore | 0,32 | 0,99 | 55,8 | −47,5 |

Perdas relativas aos 26 meses (ajustadas pela linha de base):
- **C5, d = 0,95:** n = 3; viés −9,5 pontos; MAE 9,5 pontos.
- **A1, d = 0,95:** n = 2; viés +2,6 pontos; MAE 2,6 pontos.
- **Com d = 0,999:** MAE de 10,7 (C5) e 19,0 pontos (A1).

**Leitura honesta:**
- **CAP/DAP:** fica a 6–8% de RQEM, mesmo sem nenhuma calibração para Campo Verde.
- **Altura:** subestimada em 12%. É o mesmo viés que Borges (2009) relata para o C5 e para Itacambira.
- **Volume por árvore: subestimado em 47–66%, um viés grande.** Há duas causas prováveis:
  - o simulador calcula volume de lenho sem casca e galhos, por Ws(1 − pBB)/ρ, enquanto o observado é volume de Smalian;
  - as biomassas iniciais de Borges e Caldeira não são as desse plantio.

  Por isso não se deve comparar volume absoluto entre essas fontes.
- O r alto (0,92–1,00) só mostra que o modelo ordena corretamente testemunha < desfolha e 14 < 26 meses. Com n = 4, ele não sustenta inferência.
- **Isto não é validação.** É um estudo, com híbridos, 100% de desfolha aproximada por d < 1, e clima, solo e clone não equivalentes.

## C — Metamodelo da resposta à desfolha (o que governa a perda no simulador)
Floresta aleatória, validação cruzada k = 7 (como no artigo), 1.056 tratamentos aptos:

| Resposta | n | R² (VC) | r(yŷ) | RQEM % |
|---|---|---|---|---|
| Perda de volume aos 84 meses | 1.056 | 0,995 | 0,998 | 7,0 |
| Perda acumulada de NPP | 1.056 | 0,995 | 0,998 | 7,2 |
| Meses até Wf ≥ 95% do controle | 896 | 0,988 | 0,994 | 3,5 |

Importância por permutação, em % do total:

| Fator | Perda de volume | Recuperação foliar |
|---|---|---|
| Intensidade da desfolha | **76,6** | **63,1** |
| Frequência (recorrente) | 14,3 | 0,0 |
| Clima/sítio | 6,1 | 5,0 |
| Material genético | 1,8 | 27,2 |
| Fertilidade (FR) | 0,7 | 1,2 |
| Água (ASWmax) | 0,6 | 3,5 |

**Monotonicidade:** em 352 de 352 combinações (sítio × material × água × FR × calendário), a perda de volume cresce estritamente com a intensidade (ρ de Spearman = 1).

**Comprova:** a resposta do simulador é coerente, monotônica e explicada quase toda pela intensidade e pela frequência da desfolha. O solo tem papel secundário. **Não comprova** que essas perdas sejam as reais: isso dependeria de observações independentes.

## Parecer
| O que se quer afirmar | Comprovado? | Base |
|---|---|---|
| O código reproduz o 3-PG/r3PG | **Sim** | Bloco A |
| A desfolha é aplicada corretamente (massa, calendário, LAI) | **Sim** | Testes + bloco A |
| A resposta do módulo é coerente (monotônica, recorrência > único na maioria) | **Sim, como propriedade do modelo** | Bloco C, auditoria |
| As perdas simuladas correspondem às de campo | **Não** | Bloco B: n mínimo, transferência taxonômica, viés de volume |
| Validação em Indianópolis | **Não há dados** | — |
