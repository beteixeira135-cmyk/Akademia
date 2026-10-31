# Validação cruzada ampliada do metamodelo da resposta à desfolha

**O que é validado:** a capacidade de um modelo estatístico prever as perdas que o 3-PG simula a partir dos fatores do experimento. **Não** é validação do 3-PG contra o campo: não há observações para isso.

**Dados:** 1.056 tratamentos aptos (896 com recuperação definida).
**Algoritmos:**
- regressão linear com interações de 2ª ordem;
- Random Forest;
- Gradient Boosting;
- RNA MLP com camadas (50, 30) e ReLU, como em Castro et al.

**Esquemas:** k-fold 7 repetido 10 vezes (70 folds); deixando um sítio de fora (3 folds); deixando um material de fora (4 folds). Script: `validacao_kfold.py`.

## Perda de volume aos 84 meses
| Modelo | k-fold 7×10: R² (dp) | RQEM % | Deixa sítio fora: R² | RQEM % | Deixa material fora: R² | RQEM % |
|---|---|---|---|---|---|---|
| Random Forest | **0,995** (0,001) | **7,0** | 0,85 | 38,2 | 0,95 | 19,8 |
| Gradient Boosting | 0,992 (0,002) | 9,3 | 0,83 | 41,5 | 0,95 | 20,8 |
| RNA MLP (50, 30) | 0,989 (0,004) | 10,5 | 0,80 | 43,6 | 0,95 | 21,4 |
| Linear + interações | 0,972 (0,004) | 17,2 | 0,81 | 42,4 | 0,92 | 27,6 |

Viés quando o sítio fica de fora (Random Forest):
- **Imperatriz:** −31% (o metamodelo **subestima** as perdas no clima quente);
- **Indianópolis:** +17%;
- **Telêmaco Borba:** +17%.

Quando o material fica de fora, **o A1 é o pior caso** (RQEM 38–43%, viés −13 a −23%). C2, C4 e C5 ficam em 12–24%.

## Meses até Wf ≥ 95% do controle
| Modelo | k-fold 7×10: R² | RQEM % | Deixa sítio fora: R² | Deixa material fora: R² |
|---|---|---|---|---|
| Random Forest | 0,988 | 3,4 | 0,80 | −1,22 |
| Gradient Boosting | 0,980 | 4,5 | 0,80 | −1,14 |
| Linear + interações | 0,967 | 5,7 | 0,74 | −0,91 |
| RNA MLP (50, 30) | 0,968 | 5,6 | 0,10 | −0,54 |

Com o A1 de fora, o R² vai de −5,7 a −7,7: a recuperação do A1 **não pode ser prevista** a partir dos clones de Borges.

## Interpretação
1. **O k-fold aleatório é otimista.** Ele dá R² ≈ 0,99, mas o delineamento é fatorial e determinístico: tratamentos quase idênticos (mesmo sítio e material, solo vizinho) caem no treino e no teste ao mesmo tempo. Sozinho, esse número não deve ser apresentado como "acurácia".
2. **Deixando o sítio de fora, a resposta não se transfere bem entre climas.** O RQEM fica em 38–44% e o viés chega a ±31%. A resposta à desfolha depende do clima de um jeito que dois climas não ensinam sobre o terceiro, sobretudo para Imperatriz. Isso **reforça** que Telêmaco Borba e Imperatriz são extrapolações, e não validação regional.
3. **Deixando o material de fora, o A1 se comporta de forma distinta dos clones de Borges.** É coerente com as diferenças estruturais já identificadas: o FR só atua na partição no A1, o LAI de Borges é muito alto e o Tmax é diferente. Conclusões sobre um clone não se generalizam para outro.
4. **A RNA do artigo (50, 30, ReLU) não supera a Random Forest** com esses dados e falha na recuperação quando um grupo fica de fora. Com poucos fatores tabulares, a floresta aleatória é mais estável.

## Parecer
O esquema que vale reportar no TCC é o de **validação por grupos** (deixa um sítio de fora e deixa um material de fora), acompanhado do k-fold aleatório com a ressalva do item 1. A mensagem que ele sustenta é que a perda causada pela desfolha é previsível dentro do mesmo clima e material, mas **específica do contexto**, e que a transferência de parâmetros entre clones e climas é a maior fonte de incerteza. Isso coincide com o resultado de Morris e da auditoria adversarial.
