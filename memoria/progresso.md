# Progresso
## Feito
- TCC v. 31/10: 41 p., 9 figuras, 11 tabelas; auditoria 204/204; 36 testes.
- Plataforma: conceitos (49), modo explicar, cubagem e taper seccional.
- Calibração v3 (d = 0,999): U mediana 1,16 [IC90% 1,02–1,33]; a mediana 0,55 [0,05–0,975].
  Ajuste C5 (vol/CAP/alt, %): obs 52,9/24,2/19,1; original 64,8/28,5/34,7; calibrado 50,4/20,2/24,9.
  Validação A1-urocam (vol/CAP): obs 59,0/22,9; original 79,3/40,7; calibrado 64,8/29,7 (IC90% vol 53,7–78,6; CAP 22,5–40,0).
- Biomas: clima NASA POWER e solo (ALM 219 mm, ARA 194 mm, ELD 145 mm TECHS 6) prontos; controles rodados.
- Testes da v3: 13 novos (49 no total), todos aprovados (modelo/testes/test_compensacao_v3.py).
- Validação qualitativa E. globulus (calibracao/saida/validacao_globulus.csv): sem perda de DAP/altura nas duas versões
  (fraco para discriminar); IAF aos 18 meses (Barry): original −8,3%, calibrado −1,4% (IC90% −6,7 a +2,4) → mais próximo
  de "área foliar sem diferença".
- Bloco por bioma (experimentos/run_biomas.py → saida/biomas/): 1.728 tratamentos × 2 versões; a versão original reproduz
  o bloco LOCAL do TCC (diferença máx. 3e-14). Calibrado reduz perdas (ex.: IND A1 50% PA 13,8 → 8,8%) e a recuperação
  relativa de 23–35 para 8–15 meses (exceto ARA, 2–8). Incerteza (200 amostras) em incerteza_posterior_d50.csv.
- RF 6 locais (saida/biomas/rf_*.csv): importância perda de volume — intensidade 50,6/47,3%, frequência 44,3/42,1%
  (original/calibrado). Local fora, RQEM média: original 63% (local categórico) e 66% (clima numérico); calibrado 143% e 69%
  (descrever o clima por números melhora a transferência na versão calibrada; R² 0,17 → 0,83).
- Morris C5, 6 locais (morris_C5_6locais.csv): nWs, k e SLA1 dominam a perda de volume em todos os locais.
- Danos, 6 locais, C5 (danos_6locais.csv): formigas original 2,5–6,6% (−0,6 em ARA) → calibrado 0,5–3,0%; em ARA a desfolha
  economiza água e o original dá ganho (−2,5% lagarta), atenuado na calibrada (−0,4%).
- Plausibilidade ARA: biomassa aérea simulada aos 54 meses 57–62 t/ha × 51–132 t/ha (média 88) de 15 clones na estação do IPA
  (Alves et al., 2007, Rev. Ciênc. Agrár. 48:161-173; 3 × 2 m; ~650 mm). Dentro da faixa, abaixo da média. ELD: sem dado
  publicado de produtividade localizado (não independente de qualquer forma).
- TCC v. 31/10 noite: 49 p., 9 figuras, 13 tabelas. Novas seções 3.12 (compensação e calibração), 3.13 (biomas),
  4.10, 4.11 (Tabelas 10 e 11); plataforma → 3.14/4.12; limitações → 4.13 (b) e (j)/(k) revistas; objetivos (+2),
  introdução, resumo/abstract, palavras-chave, conclusões (+2), siglas e símbolos, 5 referências novas (Alves 2007,
  IBGE 2024, McNabb e Wadouski 1999, OpenStreetMap, Silva, Mauro e Almeida 2019), Apêndice B. Auditoria: 335/335.
## Falta (em ordem)
1. Drive: TCC docx/pdf novos, diário e passagem de bastão.
2. Plataforma: incluir os 3 novos locais e a opção "com compensação calibrada" (opcional).
3. Revisão do texto pelo autor e envio aos orientadores (1ª semana de novembro).
4. Defesa: documento de preparação e slides.
