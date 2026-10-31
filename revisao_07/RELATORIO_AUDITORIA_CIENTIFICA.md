# Relatório da auditoria científica do TCC II (Missão 07)

Data: 31/10/2026. Versão auditada: TCC de 49 páginas (commit `035c58b`). Versão revisada: 53 páginas, 9 figuras, 14 tabelas (este commit).

## 1. Reprodutibilidade (etapas 1 e 9)
- **Testes do modelo:** 49 de 49 aprovados, reexecutados.
- **Testes do pipeline experimental:** 8 de 8 aprovados.
- **Auditoria numérica:**
  - antes da revisão: 336 de 336 números conferidos;
  - depois: 363 de 363, com 27 números novos da revisão.
- **Calibração:** reexecutada com resultado idêntico ao publicado (U de 1,02 a 1,33, mediana 1,16; a de 0,05 a 0,975, mediana 0,55).
- **Dados de Bertulio (2008):** conferidos no texto do artigo. A razão de volumes da Tabela 2 reproduz os percentuais do resumo.

## 2. Matriz de afirmações (etapa 1)
Arquivo `matriz_afirmacoes.csv`, com 32 afirmações centrais, cada uma com classe, evidência, fonte, limitação, gravidade e ação.

**Por classe:**

| Classe | Quantidade |
|---|---|
| Fundamentada por literatura | 5 |
| Fundamentada por resultado computacional | 7 |
| Sustentada por observação secundária | 3 |
| Parcialmente sustentada | 9 |
| Extrapolação declarada | 2 |
| Mistas | 2 |
| Incorreta ou contraditória | 4 |

**Por gravidade:** 3 altas, 7 médias e 8 baixas; as demais 14 não exigiram correção.

**As 4 afirmações incorretas ou contraditórias, todas corrigidas:**
- A04: Bertulio como "único experimento brasileiro com perdas publicadas", mas Matrangolo et al. (2010) também publicou perdas;
- A10 e A11: transpiração compensatória e realocação descritas como "ausentes no modelo", quando a versão 3 já as inclui;
- A16: IAF "de 7 a 11" na seção 4.2 contra "8 a 11" na seção 4.5.

## 3. Mecanismos (etapa 5)
Arquivo `matriz_mecanismos.csv`.

| Mecanismo | Situação | Observação |
|---|---|---|
| M1 Remoção de folhas | Sustentado | Conservação de massa verificada |
| M2 Fotossíntese (U) | Parcialmente sustentado | Ver abaixo |
| M3 Condutância (γ) | Sustentado na direção | γ ≈ 1 reproduz Quentin et al. (2011) |
| M4 Alocação (a) | Parcialmente sustentado | Pouco identificado |
| M5 Recuperação | Parcial | Melhor na versão calibrada, mas não reproduz Matrangolo |
| M6 Reservas | Omissão relevante | — |
| M7 Mortalidade | Cenário declarado | — |
| M8 Solo e clima | Parcial | A compensação não depende de N |

Problemas no M2:
- a literatura mede Amax/Asat da folha, e o módulo altera a eficiência quântica do dossel;
- o aumento observado é transitório, e no módulo dura enquanto a folhagem não se recompõe;
- o posterior depende do limite superior do prior.

Nenhuma equação nova foi incorporada: as lacunas foram declaradas como limitações (l), (m) e (n).

## 4. Calibração (etapa 6)
| Verificação | Resultado | Implicação |
|---|---|---|
| Reexecução | Idêntica | Reprodutível |
| Prior de U até 1,6 | Mediana 1,21; IC 90% de 1,02 a 1,54 | U fracamente identificado; resultado declarado no texto |
| Escala do prior de σ (5 e 20) | Sem mudança relevante | Robusto |
| Ajuste só com volume ou só com CAP | Medianas semelhantes | Os dados restringem pouco |
| Atribuição no urocam | Só U: 79,1%; só a: 70,1%; U e a: 61,7%; observado 59,0% | A melhora vem sobretudo de a, pouco identificado |
| Independência do teste | Mesmo experimento, local, datas e protocolo; A1 ≠ urocam | **Não é validação independente.** Termo corrigido no resumo, nos objetivos, nos métodos, nos resultados, na Tabela 10 e nas conclusões |
| Matrangolo et al. (2010), protocolo aproximado | Observado 37,9–79,7%; original 2,6–12,7%; calibrado 1,1–8,5% (RQEM 54 e 56 p.p.) | Evidência contrária forte; uso do módulo restrito a desfolhas parciais ou após o primeiro ano |
| Quentin et al. (2011), A1, 45% | Razão de transpiração: 0,785 (original), 0,955 (γ = 0,5), 0,998 (γ = 1) | γ = 0,5 subestima a homeostase |

Nenhum dado experimental foi alterado.

## 5. Concordância com a literatura (etapa 7)
Arquivo `matriz_concordancia.csv`, com 9 linhas e métricas onde a comparação é quantitativa.

| Comparação | Original | Calibrado | Observação |
|---|---|---|---|
| Urograndis (ajuste), RQEM nas 3 variáveis | 11,7 p.p. | 4,3 p.p. | Dentro da amostra |
| Urocam (teste), RQEM | 19,1 p.p. | 6,3 p.p. | — |
| Matrangolo, RQEM | 53,7 p.p. | 56,0 p.p. | Discordância |
| Barry e Eyles | Qualitativa | Melhor na calibrada | — |
| Quentin et al. (2011) | — | Concorda com γ ≈ 1 | — |
| Quentin et al. (2012) | — | Concorda na ordem de grandeza | Discorda na duração |

## 6. Correções no TCC (etapas 8 e 9)
Arquivo `matriz_correcoes.csv`.

**Introdução**
- Precedentes de modelagem: CABALA (Pinkard et al., 2011, 2014) e 3PG.d (Rua et al., 2020).
- Contribuição delimitada, sem alegar pioneirismo.

**Métodos**
- Bertulio descrito como o único experimento com idade compatível com as parametrizações.
- O urocam passou a ser "teste", não validação independente.
- Descritos os testes de robustez e os testes com Quentin (2011) e Matrangolo (2010).
- Pantanal: "não se localizaram registros" de plantio comercial.

**Resultados e discussão**
- Atribuição da melhora do urocam a cada mecanismo.
- U confrontado com Quentin et al. (2012) e Pinkard et al. (1998, citado por Quentin et al., 2011), com a ressalva de Amax e da duração transitória.
- Sensibilidade ao prior.
- Sobrecompensação observada por Barry et al. (2012).
- Teste de transpiração.
- Novo parágrafo com a evidência contrária de Matrangolo et al. (2010).
- Oliveira et al. (2014) e Rocha et al. (2021) na seção 4.8.
- Afirmações da versão original deixaram de ser apresentadas como gerais.
- IAF uniformizado; frase sobre Almeirim e sobre o Morris corrigidas.

**Limitações:** de (a)–(k) para (a)–(o). Entram o teste não independente, U aplicado à eficiência quântica e de forma persistente, a falta de modulação por N e a subestimação após desfolha total precoce.

**Resumo, abstract e conclusões:** "clone de teste, do mesmo experimento" e o limite de uso do módulo.

**Apêndice C:** protocolo da busca e precedentes.

## 7. Decisão editorial (etapa 11)
1. **O referencial sustenta o desenvolvimento do módulo?** Sim. Remover folhas, aumentar a fotossíntese, manter a condutância e realocar para as folhas são processos documentados. Há, porém, poucas evidências em clima tropical e em eucaliptos brasileiros.
2. **A compensação está suficientemente fundamentada?** Na direção, sim; na magnitude, não.
   - U vem de medições de Amax em *E. globulus* e *E. nitens*, e o aumento observado é transitório.
   - a é quase o prior.
   - γ tem apoio quantitativo (Quentin, 2011), mas foi fixado em 0,5.
3. **A calibração com Bertulio sustenta as conclusões?**
   - Sustenta que a compensação torna o módulo coerente com aquele experimento e com outro clone do mesmo experimento.
   - Não sustenta generalização: o teste não é independente, e um experimento brasileiro (Matrangolo) é fortemente contrariado.
   - As conclusões foram reescritas nesse sentido.
4. **Os resultados entre regiões foram interpretados com cautela?** Sim, após a revisão. Cada bioma tem um único local, Almeirim não tem comparação com medições acessadas e o A1 é tratado como diagnóstico onde o calor ultrapassa seu limite.
5. **Algum estudo contradiz a originalidade?** Sim, para uma alegação ampla: Rua et al. (2020, 3PG.d) e o CABALA. O TCC agora os cita e delimita a contribuição.
6. **Referências indispensáveis ausentes:**
   - incorporadas: Rua et al. (2020), Pinkard et al. (2014) e Oliveira et al. (2014);
   - incorporada como indicação de dados: Rocha et al. (2021);
   - recomendadas após leitura completa: Turnbull et al. (2007), Quentin et al. (2011b), Eyles et al. (2013), Collett e Neumann (2002).
7. **A cienciometria entra no corpo?** Não. Ela fica como Apêndice C resumido, mais este relatório independente. A busca foi incompleta (sem OpenAlex, Scopus e WoS), e os gráficos não respondem a nenhuma pergunta do TCC além da originalidade, já tratada na introdução.
8. **Há problemas científicos críticos não resolvidos?**
   - Nenhum erro de cálculo ou contradição ficou sem correção.
   - Permanecem como limitações científicas, não como erros:
     - falta de validação independente;
     - discrepância com Matrangolo sem explicação mecanística;
     - U e a fracamente identificados;
     - busca bibliográfica sem OpenAlex, Scopus e WoS.
9. **Pronto para os orientadores?** Sim, com ressalvas.

**Parecer: B — encaminhamento com ressalvas explícitas.**

Ressalvas a enviar junto:
- (i) a calibração usa um único experimento, e o teste não é independente;
- (ii) Matrangolo et al. (2010) contraria o módulo após desfolha total precoce;
- (iii) a busca bibliográfica será complementada pelo OpenAlex;
- (iv) recomenda-se ler os quatro estudos indicados no item 6 antes da defesa;
- (v) a escolha γ = 0,5 deve ser discutida com os orientadores (a literatura indica γ ≈ 1).
