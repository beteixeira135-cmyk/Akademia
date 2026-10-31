# Relatório cienciométrico — desfolha, eucalipto e modelagem processual (Missão 07, etapas 2 e 3)

Base desta versão: Crossref, 31/10/2026 (ver PROTOCOLO_BUSCAS.md). Núcleo: 93 documentos de 1998 a 2026. Indicadores calculados em Python (`busca/bibliometria.py`); a instalação do bibliometrix em R não terminou na sessão. Todos os números saem dos arquivos de `bibliometria/`.

## Indicadores calculados

**1. Produção anual** (`producao_anual.csv`, `fig_producao_anual.png`)
- Distribuição contínua de 1998 a 2026, de 1 a 7 documentos por ano.
- 34 documentos em 1997–2006, 33 em 2007–2016 e 26 em 2017–2026.
- Não há tendência de crescimento no núcleo. Isso contrasta com o crescimento geral da literatura florestal, mas pode refletir o viés do Crossref por títulos.

**2. Periódicos** (`periodicos_top20.csv`)

| Periódico | Documentos |
|---|---|
| Forest Ecology and Management | 12 |
| Australian Forestry | 7 |
| Tree Physiology | 6 |
| Australian Journal of Botany | 4 |
| Austral Ecology | 4 |

**3. Autores mais produtivos** (nomes normalizados)

| Autor | Documentos |
|---|---|
| Pinkard, E. | 16 |
| Mohammed, C. | 8 |
| Potts, B. | 7 |
| Eyles, A. | 6 |
| Quentin, A. | 6 |
| Stone, C. | 6 |
| Beadle, C. | 5 |
| O'Grady, A. | 5 |

**4. Estudos mais citados no Crossref**

| Estudo | Citações |
|---|---|
| Eyles, Pinkard e Mohammed (2009) | 115 |
| Turnbull, Adams e Warren (2007) | 82 |
| Reis et al. (2012), *Gonipterus* na Península Ibérica | 69 |
| Quentin et al. (2011) | 66 |
| Pinkard, Battaglia e Mohammed (2007) | 64 |
| Quentin et al. (2012) | 63 |

**5. Rede de coautoria**
- 246 autores, 622 ligações e 37 componentes.
- O maior componente tem 51 autores e corresponde ao grupo da Tasmânia (CSIRO e Universidade da Tasmânia).

**6. Termos e agrupamentos** (`termos_frequentes.csv`, `agrupamentos_tematicos.csv`, `fig_coocorrencia.png`). A modularidade separou três grupos:
1. herbivoria por insetos e folhagem;
2. desfolha de *E. globulus* e *Gonipterus*, com experimentos artificiais;
3. danos em plantações e controle.

**7. Evolução temática**
- 1997–2006: entomologia e herbivoria.
- 2007–2016: respostas fisiológicas (fotossíntese, copa, desfolha artificial).
- 2017–2026: impacto na produtividade e sensoriamento.

**8. Interseções** (`intersecoes.csv`)

| Interseção | Documentos |
|---|---|
| D∧E | 86 |
| D∧E∧F (fisiologia) | 16 |
| D∧E∧A (ambiente) | 15 |
| D∧E∧F∧A | 4 |
| D∧modelo processual | 9 |
| D∧modelo processual∧E | 2 |
| D∧modelo processual∧V | 1 |
| D∧E∧Brasil | 2 |

Nenhum gráfico cienciométrico foi incluído no corpo do TCC. O Apêndice C resume o protocolo e lista os precedentes de modelagem, que respondem à pergunta de originalidade.

## Respostas às perguntas

**Q1 — Evolução.**
- Produção estável, de 1 a 7 documentos por ano, sem crescimento evidente na amostra.
- O tema migrou da entomologia (anos 2000) para a fisiologia da compensação (2007–2013, grupo da Tasmânia) e depois para o impacto na produtividade, o sensoriamento e a modelagem.

**Q2 — Centrais.**
- Grupo Pinkard–Mohammed–Eyles–Quentin–Barry–Battaglia (CSIRO e Universidade da Tasmânia).
- Estudos-chave: Eyles et al. (2009); Turnbull et al. (2007); Pinkard et al. (2006, 2007, 2011, 2014); Quentin et al. (2010, 2011a, 2011b, 2012); Eyles et al. (2013, revisão); Barry et al. (2012); Barry e Pinkard (2013).
- Em modelagem: CABALA (Battaglia et al.) e 3PG.d (Rua, Barreiro, Branco e Tomé, Universidade de Lisboa).

**Q3 — Representação da compensação.**
- O aumento da fotossíntese é medido como Amax ou Asat da folha: +30% transitório em Quentin et al. (2012); até +35% em *E. nitens* (Pinkard et al., 1998, citado por Quentin et al., 2011); não causado por aumento de N foliar (Turnbull et al., 2007).
- A condutância e a transpiração mantêm a homeostase da árvore (Quentin et al., 2011a).
- A realocação vai para folhas e galhos, com menos raízes grossas e uso de reservas (Eyles et al., 2009; Barry et al., 2012).
- Em modelos, o CABALA aplica um fator U enquanto a razão tecido fotossintético:alburno estiver abaixo da do momento da desfolha (Pinkard et al., 2011).
- No 3PG.d, a desfolha é calculada mês a mês e aplicada nos meses de ataque (descrição da ferramenta). O tratamento da compensação não foi verificado, porque o texto completo não foi acessado.

**Q4 — Modelos processuais com dano foliar.**
- Nove documentos do núcleo cruzam desfolha e modelo processual. Dois são de eucalipto: Rua et al. (2020), 3PG.d; Pinkard et al. (2014), *E. globulus* e Mycosphaerella.
- Os demais tratam de ciclones e tufões, *Pinus* com 3-PG (Dreaden et al., 2026), herbivoria em florestas boreais e tropicais e um arcabouço processual para surtos de insetos (2026).
- Pela busca na web, o 3PG.d também foi aplicado a *E. dunnii* na África do Sul (conjunto de dados de Kombora, 2025, Universidade de Pretória).
- O número é um piso: depende da base e do filtro de título e resumo.

**Q5 — Respostas conjuntas.**
- Quatro documentos cruzam desfolha, eucalipto, fisiologia e ambiente.
- Os principais testam água e N: Eyles et al. (2009), Barry et al. (2012), Quentin et al. (2012) e Pinkard et al. (2006, 2007).
- Não foi encontrado estudo que teste a interação com temperatura em eucalipto, e nenhum em clima tropical.

**Q6 — Dados experimentais brasileiros.** Só dois documentos do núcleo têm marcador de Brasil no título ou resumo. Fora do corpus, por leitura direta e busca na web:
- Bertulio et al. (2008), Campo Verde-MT;
- Matrangolo et al. (2010), Viçosa-MG;
- Oliveira et al. (2014), *E. grandis*, desfolha parcial aos 6 meses;
- Rocha et al. (2021), plantios comerciais no Pará, por redes neurais;
- estudos de formigas citados por Matrangolo: Freitas et al. (1994) e Zanetti et al. (2000, 2003).

A literatura brasileira é pouco indexada com DOI e não foi captada pelo filtro.

**Q7 — Calibração e validação.**
- Só um documento cruza desfolha, modelo processual e avaliação.
- No contexto 3-PG há calibração e análise de incerteza (por exemplo, calibração bayesiana do 3-PG para *Quercus mongolica*, 2025; incerteza estocástica, 2022). Nenhum documento calibra a compensação após desfolha em eucalipto tropical.

**Q8 — Lacunas** (na amostra, não provadas para a literatura toda):
- dados brasileiros de desfolha parcial em idades posteriores ao primeiro ano;
- compensação em clima tropical e sob deficiência hídrica;
- recuperação foliar medida mês a mês;
- validação independente de módulos de desfolha;
- interação com temperatura;
- perda de volume até a colheita após desfolha parcial.

**Q9 — Fundamentais × acréscimos.**
- Fundamentais já no TCC: Pinkard et al. (2006, 2007, 2011), Eyles et al. (2009), Barry et al. (2012), Quentin et al. (2010, 2011, 2012), Bertulio et al. (2008), Matrangolo et al. (2010).
- Acrescentam informação e foram incorporados: Rua et al. (2020), Pinkard et al. (2014), Oliveira et al. (2014), Rocha et al. (2021).
- Recomendados para leitura completa antes da defesa (não citados no TCC, porque o texto completo não foi lido):
  - Turnbull et al. (2007);
  - Quentin et al. (2011b), copa fechada;
  - Eyles et al. (2013), revisão;
  - Barry e Pinkard (2013);
  - Collett e Neumann (2002), desfolha crônica e sobrevivência;
  - Eyles et al. (2009b), fotossíntese cortical;
  - Loch e Matsuki (2010).

**Q10 — Originalidade.** **Sim, há trabalhos que enfraquecem uma alegação ampla de originalidade:**
- o 3PG.d (Rua et al., 2020) já acrescentou um módulo de desfolha ao 3-PG para eucalipto;
- o CABALA já representa a desfolha com compensação.

O TCC não afirmava pioneirismo, mas não citava esses precedentes. O texto foi corrigido para delimitar a contribuição: implementação verificada contra o r3PG, aplicação a eucaliptos brasileiros, calibração com dados brasileiros e comparação entre climas.

## Evidências contrárias às hipóteses do módulo
1. **Matrangolo et al. (2010):** perdas de 37,9 a 79,7% persistentes até 92 meses após desfolha total precoce. O módulo, nas duas versões, subestima por um fator de 6 a 34.
2. **Oliveira et al. (2014):** só a desfolha total reduziu o crescimento aos 6 meses. Isso concorda com a tolerância a desfolhas parciais, mas indica um limiar que o módulo, por ser proporcional, não tem.
3. **Barry et al. (2012):** sobrecompensação (volume do tronco maior). O módulo calibrado dá ganhos pequenos e não significativos, o que é parcialmente concordante.
4. **Quentin et al. (2012):** aumento da fotossíntese transitório. No módulo, ele persiste até a folhagem se recompor.
