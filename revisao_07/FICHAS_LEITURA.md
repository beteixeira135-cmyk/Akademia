# Fichas de leitura dos estudos centrais (Missão 07, etapa 4)

Fonte: texto completo dos PDFs em `corpus_pdfs/` (R01–R21), extraído com `pdftotext`. Os valores foram transcritos do texto. Quando um valor só aparece em figura, a ficha diz isso e não estima nada. A coluna "Relevância" indica onde o estudo entra no TCC.

---

## Experimentos de desfolha em eucalipto

### F01 — Bertulio et al. (2008)
- **Referência:** BERTULIO, V. G.; PERES FILHO, O.; SILVA, E. G.; DORVAL, A. Crescimento de clones de *Eucalyptus* spp. submetidos a desfolha artificial sucessiva. *Revista de Agricultura*, Piracicaba, p. 119-124, 2008. (PDF R01; texto obtido por OCR.)
- **Material e local:**
  - clones urocam (*E. urophylla* × *E. camaldulensis*) e urograndis (*E. urophylla* × *E. grandis*);
  - Campo Verde-MT, plantio da Sadia S.A., 3 × 3 m;
  - blocos casualizados.
- **Idade e protocolo:**
  - início aos 14 meses;
  - duas desfolhas artificiais totais (abril/2007 e janeiro/2008);
  - avaliação aos 26 meses;
  - sem mortalidade em nenhum grupo (Tabelas 1 e 2).
- **Resultados quantitativos:**
  - volume da testemunha no fim do experimento 191,14% maior no urocam e 108,80% maior no urograndis (resumo);
  - Tabela 2 (26 meses), testemunha × desfolhado:

    | Clone | Volume (m³/árvore) | CAP (cm) | Altura (m) |
    |---|---|---|---|
    | urocam | 0,1221 × 0,0419 | 36,43 × 26,35 | 14,35 × 9,45 |
    | urograndis | 0,1734 × 0,0830 | 38,62 × 29,46 | 17,89 × 15,00 |

  - perdas ajustadas pela linha de base (Tabela 1, aos 14 meses):
    - urocam: volume 59,0%, CAP 22,9%, altura 33,2%;
    - urograndis: volume 52,9%, CAP 24,2%, altura 19,1%.
- **Conferência:** 0,1221/0,0419 = 2,914, ou seja, testemunha 191% maior, o que confere com o resumo. Para o urograndis, 0,1734/0,0830 = 2,089, ou seja, 108,9% maior; o resumo diz 108,80%.
- **Compensação fisiológica:** não medida.
- **Modelo, calibração e incerteza:** nenhum modelo processual; não informa erro-padrão das médias nas tabelas transcritas.
- **Limitações:**
  - desfolha total, fora do domínio do módulo (d < 1);
  - coordenadas e solo não informados;
  - um local e um ciclo;
  - volume por cubagem de Smalian.
- **Relevância:** é o dado de calibração (urograndis) e de teste (urocam) da seção 3.12. As duas observações vêm do mesmo experimento, local e datas, então o teste com o urocam não é independente do ajuste.

### F02 — Matrangolo et al. (2010)
- **Referência:** MATRANGOLO, C. A. R. et al. Crescimento de eucalipto sob efeito de desfolhamento artificial. *Pesquisa Agropecuária Brasileira*, v. 45, n. 9, p. 952-957, 2010. (PDF R02)
- **Material e local:**
  - *E. grandis* seminal;
  - Viçosa-MG (20°46'16" S; 42°52'41" O; 650 m);
  - 3,0 × 2,0 m;
  - mudas plantadas com cerca de 150 dias.
- **Protocolo:**
  - desfolha manual total aos 56 dias; aos 56 e 143; aos 56 e 267; e aos 56, 143 e 278 dias após o plantio;
  - 60 árvores por tratamento;
  - medições de 21 a 92 meses (1997–2003).
- **Resultados quantitativos (Tabela 2, 92 meses):**
  - Vt (m³/ha): testemunha 469,1; uma desfolha 291,4; duas (56 e 143 d) 178,8; duas (56 e 267 d) 180,0; três 95,4;
  - perdas: 37,9; 61,9; 61,6; 79,7%;
  - mortalidade de 6,9 a 8,8%, contra 8,0% na testemunha;
  - uma desfolha reduziu o crescimento em DAP em 18,9% e em altura em 12,0%.
- **Compensação fisiológica:** não medida. As perdas persistiram até 92 meses.
- **Limitações:**
  - desfolha total em mudas recém-plantadas;
  - árvores isoladas como repetição;
  - sem dados de clima e solo.
- **Relevância:** é uma **evidência brasileira contrária** à ideia de que o eucalipto compensa a desfolha. O TCC só dizia que o experimento "não foi comparável" e não registrava a magnitude. Teste adicional desta auditoria (calibracao/saida/testes_adicionais.json):
  - protocolo aproximado com C5, clima de Viçosa de 2015–2024 e eventos deslocados para 4, 7 e 11 meses;
  - perdas simuladas de 2,6 a 12,7% na versão original e de 1,1 a 8,5% na calibrada, contra 37,9 a 79,7% observadas;
  - RQEM de 54 e 56 pontos percentuais.

  O módulo, nas duas versões, **não reproduz** as perdas persistentes após desfolha total precoce.

---

## Experimentos com *E. globulus* (Tasmânia)

### F03 — Pinkard et al. (2006)
- **Referência:** PINKARD, E. A. et al. Growth responses of *Eucalyptus globulus* Labill. to nitrogen application and severity, pattern and frequency of artificial defoliation. *Forest Ecology and Management*, v. 229, p. 378-387, 2006. (R06)
- **Protocolo:**
  - plantio de *E. globulus*;
  - N a 100 ou 300 kg/ha, antes ou depois da desfolha;
  - desfolhas de 25% em toda a copa, 100% da metade superior ou da inferior, uma a três vezes.
- **Resultados quantitativos:**
  - sem adubação, 25% em toda a copa reduziu o incremento em diâmetro e altura em 20 meses;
  - desfolha "out–in" de primavera reduziu o diâmetro em 12% e a altura em 17%;
  - desfolha tripla reduziu o diâmetro em 15% e a altura em 26%;
  - desfolha única não teve efeito significativo;
  - N antes da desfolha manteve o crescimento;
  - árvores desfolhadas e adubadas ainda tiveram altura 15% menor.
- **Relevância:** sustenta a frequência como fator que amplia a perda e a interação entre desfolha e nutrição (seções 4.4 e 4.5).

### F04 — Pinkard, Battaglia e Mohammed (2007)
- **Referência:** PINKARD, E.; BATTAGLIA, M.; MOHAMMED, C. L. Defoliation and nitrogen effects on photosynthesis and growth of *Eucalyptus globulus*. *Tree Physiology*, v. 27, p. 1053-1063, 2007. (R07)
- **Protocolo:**
  - plantio de 9 meses;
  - desfolha da copa superior ou inferior;
  - uma, duas ou três vezes em 12 meses;
  - severidade de 25 ou 38%;
  - com ou sem N.
- **Resultados:**
  - Amax aumentou com a severidade e a frequência;
  - na desfolha de outono, o aumento só apareceu na primavera seguinte;
  - o aumento de Amax diante de árvores adubadas só foi significativo com 38%;
  - N antes da desfolha permitiu compensar o crescimento em diâmetro, o que não se explica só por Amax;
  - φ (rendimento quântico) subiu 96% no tratamento triplo, sem significância.
  - As magnitudes de Amax estão em figuras, e o texto não informa um percentual de aumento devido à desfolha.
- **Relevância:** sustenta a existência do aumento da fotossíntese (M2), mas **não fornece a faixa numérica** que o TCC lhe atribuía ("U dentro da faixa observada"). Além disso, mede Amax, que não é a eficiência quântica do dossel do 3-PG.

### F05 — Eyles, Pinkard e Mohammed (2009)
- **Referência:** EYLES, A.; PINKARD, E. A.; MOHAMMED, C. Shifts in biomass and resource allocation patterns following defoliation in *Eucalyptus globulus* growing with varying water and nutrient supplies. *Tree Physiology*, v. 29, p. 753-764, 2009. (R08)
- **Local e protocolo:**
  - Pittwater, perto de Hobart, com 500 mm/ano de chuva;
  - mudas de 8 meses, 2 × 2 m;
  - 40% de remoção foliar;
  - tratamentos de água e N.
- **Resultados:**
  - compensação dos 40% em 5 meses, exceto com pouca água e pouco N ao mesmo tempo;
  - nesse tratamento, as plantas desfolhadas alocaram 37% menos a folhas novas;
  - mecanismos: menor alocação a raízes grossas, mobilização de reservas, dinâmica de N e maior razão folha:lenho.
- **Relevância:** sustenta M4 (alocação) e mostra que a compensação **falha quando água e nutrientes faltam juntos** (M8). O módulo não representa essa interação.

### F06 — Barry et al. (2012)
- **Referência:** BARRY, K. M. et al. Consequences of resource limitation for recovery from repeated defoliation in *Eucalyptus globulus*. *Tree Physiology*, v. 32, p. 24-35, 2012. (R04)
- **Local e protocolo:**
  - Pittwater, 2007/2008;
  - desfolhas de cerca de 40% e 55% da copa superior aos 3 e 9 meses;
  - tratamentos de água e N.
- **Resultados:**
  - aos 18 meses, altura, diâmetro e área foliar sem diferença significativa;
  - **volume do tronco, volume de casca e número de galhos significativamente maiores** nas desfolhadas;
  - biomassa aérea cerca de 13% maior em média (sem efeito significativo no total);
  - quase o dobro no tratamento com pouca água (N + W−).
- **Relevância:** é evidência de **sobrecompensação** em plantas jovens com desfolha parcial. Concorda com os pequenos ganhos simulados na seção 4.10. O TCC citava só a "ausência de diferenças".

### F07 — Quentin et al. (2010)
- **Referência:** QUENTIN, A. et al. Do artificial and natural defoliation have similar effects on physiology of *Eucalyptus globulus* Labill. seedlings? *Annals of Forest Science*, v. 67, 203, 2010. (R10)
- **Protocolo:** casa de vegetação; 25% de desfolha artificial ou pela larva *Paropsisterna agricola*.
- **Resultados:**
  - aumento da capacidade fotossintética nos dois tipos, maior na desfolha por insetos;
  - biomassa total reduzida em 28,3% (artificial) e 16% (insetos);
  - aumento da área foliar específica.
- **Relevância:** a desfolha artificial (base de todos os experimentos de calibração) não equivale à causada por insetos. É uma limitação de transferência.

### F08 — Quentin et al. (2011)
- **Referência:** QUENTIN, A. G. et al. Responses of transpiration and canopy conductance to partial defoliation of *Eucalyptus globulus* trees. *Agricultural and Forest Meteorology*, v. 151, p. 356-364, 2011. (R09)
- **Protocolo:** árvores de 4 anos; cerca de 45% da área foliar removida da metade superior da copa (29–30/08/2006); fluxo de seiva por 215 dias.
- **Resultados:**
  - transpiração diária por área de alburno sem diferença significativa;
  - Emax e GCmax maiores nas desfolhadas;
  - potencial hídrico ao meio-dia maior.
  - Cita Pinkard et al. (1998): até 35% mais fotossíntese no dossel remanescente de *E. nitens* de 3 anos após remover até 55% da copa inferior.
- **Relevância:** sustenta M3 (γ). Teste adicional com o A1 em Indianópolis e 45% de desfolha (razão de transpiração em 7 meses):

  | Versão | Razão de transpiração |
  |---|---|
  | Original | 0,785 |
  | Calibrada, γ = 0 | 0,921 |
  | Calibrada, γ = 0,5 | 0,955 |
  | Calibrada, γ = 1 | 0,998 |

  A homeostase observada corresponde a γ próximo de 1. No C5, cujo IAF fica acima do LAIgcx (condutância saturada), o teste não é informativo.

### F09 — Quentin et al. (2012)
- **Referência:** QUENTIN, A. G. et al. Interactive effects of water supply and defoliation on photosynthesis, plant water status and growth of *Eucalyptus globulus* Labill. *Tree Physiology*, v. 32, p. 958-967, 2012. (R05)
- **Protocolo:** Pittwater; sequeiro (W−) ou irrigado (W+); 75% do comprimento da copa desfolhado (cerca de 60% da área foliar) aos 15 meses.
- **Resultados:**
  - **aumento transitório de cerca de 30% em Asat**, com pico cerca de 22 dias após o evento, só em W+;
  - em W−, sem aumento;
  - Emax, GCmax e condutância hidráulica maiores nos dois regimes;
  - altura e diâmetro não afetados.
- **Relevância:** sustenta a dependência de U em relação à água (Eq. 10) e a ordem de grandeza de U (cerca de 1,3). Mostra, porém, que o aumento é **transitório (semanas)**, enquanto no módulo dura enquanto a folhagem estiver abaixo da de referência. No teste adicional, 60% de desfolha ficaram ativos 2 meses no A1 e no C5.

---

## Revisões e modelos

### F10 — Pinkard et al. (2011)
- **Referência:** PINKARD, E. A. et al. Estimating forest net primary production under changing climate: adding pests into the equation. *Tree Physiology*, v. 31, p. 686-699, 2011. (R03)
- **Conteúdo:**
  - revisão sobre pragas e NPP;
  - modelos de NPP costumam assumir redução fixa de cerca de 10% (Roxburgh et al., 2004);
  - compara CenW, G'Day, PnET, 3-PG, CABLE, CABALA e Forest-BGC quanto à representação de pragas (tabela do artigo);
  - descreve a regra do CABALA (Battaglia et al., 2011): Pxd = U·Px enquanto B < B′, com B = W_f/(alburno + raízes finas), U "definido empiricamente" e B′ a razão "no momento da desfolha";
  - aponta como mais plausível um compartimento de reservas.
- **Relevância:**
  - fundamenta M2 e a regra de ativação;
  - reforça a limitação M6 (reservas);
  - mostra que já existe modelagem processual de desfolha em eucalipto (CABALA), então a originalidade do TCC deve se limitar ao r3PG/3-PG para eucaliptos brasileiros.

### F11 — Landsberg e Waring (1997); Landsberg e Sands (2011); Sands (2004)
- **Conteúdo:**
  - estrutura do 3-PG: radiação absorvida pela lei de Beer, eficiência quântica modificada por f_T, f_F, f_N, φ e f_CO2, NPP = y·GPP e partição alométrica;
  - não há compartimento de reservas nem representação de pragas.
- **Relevância:** fundamentam as Eq. 1, 14 e 15 e as limitações (a) e (b).

### F12 — Trotsiuk, Hartig e Forrester (2020)
- **Conteúdo:** pacote r3PG (3-PGpjs e 3-PGmix) em R/Fortran, com testes de referência.
- **Relevância:** base da tradução verificada (seção 3.2); 49 testes aprovados nesta auditoria.

### F13 — Caldeira et al. (2020a); Borges (2009)
- **Conteúdo:**
  - Caldeira: parametrização do clone A1 com a rede TECHS até 80 meses;
  - Borges: parametrizações C1–C5 do Cerrado mineiro, com validação gráfica e viés conhecido (altura do C5 subestimada).
- **Relevância:** materiais simulados. O IAF de 8 a 11 dos materiais de Borges já está declarado como implausível.

### F14 — Alves et al. (2007); McNabb e Wadouski (1999); Binkley et al. (2017)
- **Alves et al. (2007):** 15 clones no IPA (Araripina), 3 × 2 m, 4,5 anos, cerca de 650 mm; biomassa aérea de 50,87 a 132,13 t/ha, média de 88,00.
- **McNabb e Wadouski (1999):** Jari Celulose, 75 mil ha de *Pinus caribaea* e *Eucalyptus* spp. em rotações de 10 e 6 anos. Produtividade crescente nas rotações; os números de produtividade não foram acessados (texto pago).
- **Binkley et al. (2017):** rede TECHS (Tabela 2, solos e CAD de 27 sítios), fonte da CAD de Indianópolis, Telêmaco Borba e Eldorado do Sul.
