# Solo local de cada sítio: fontes secundárias e valores adotados

| Sítio | ASWmax adotado (0–2 m) | Fonte do valor adotado | Verificações cruzadas |
|---|---|---|---|
| Indianópolis-MG | 215 mm | Binkley et al. (2017), Tab. 2: TECHS sítio 9, Estrela do Sul-MG (−18,73; −47,92; ~35 km de Indianópolis). Latossolo (Oxisol), argila 80%, silte 9%, areia 11% (0–40 cm). CAD 0–2 m por Stape et al. (2004). | PTF-ZARC (Teixeira et al., 2021) com a textura do TECHS 9: 160 mm. SoilGrids 2.0 + PTF-ZARC (8 pontos a ~9 km): 209 mm (205–215). Planilha do projeto: 190,6 mm (33 kPa) e 310,9 mm (10 kPa). |
| Telêmaco Borba-PR | 214 mm | Binkley et al. (2017), Tab. 2: TECHS sítio 22, Telêmaco Borba-PR (Latossolo; argila 56%, silte 23%, areia 21%). CAD 0–2 m por Stape et al. (2004). | PTF-ZARC com a textura do TECHS 22: 213 mm. SoilGrids + PTF-ZARC: 231 mm (229–237). |
| Imperatriz-MA | 210 mm | SoilGrids 2.0 (Poggio et al., 2021), média de 7 pontos a ~9 km da sede, textura de 0–200 cm (argila média 35%) + PTF-ZARC (Teixeira et al., 2021, Eq. 9). | Nenhum sítio TECHS próximo. Os mais próximos (Urbano Santos-MA; Brejinho de Nazaré-TO) ficam a mais de 450 km e têm solos arenosos (Entisol). |

## Fertilidade
- **TECHS 9 (perto de IND):** soma de bases (K + Ca + Mg) = 3,8 mmolc dm⁻³. Pela função FR(CTCe) de Caldeira et al. (2020), FR ≥ 0,59. O Al trocável não foi publicado, então esse valor é um limite inferior.
- **TECHS 22 (TB):** soma de bases = 52,3 mmolc dm⁻³. FR(CTCe) = 1,09, limitado a 1,0.
- **IMP:** não há CTCe publicada. A CTC a pH 7 do SoilGrids não substitui a CTCe.
- **Decisão:** o FR local não foi imposto. Mantiveram-se os quatro níveis ordinais (F25–F100), que cobrem o intervalo 0,55–0,80/0,90. A condição de referência é F100, o FR usado nas calibrações originais com plantios adubados (todos os sítios TECHS foram adubados intensivamente).

## Arquivos
- `soilgrids_vizinhanca.json`, `soilgrids_pontos.csv`, `asw_ptfzarc_por_ponto.csv`
- `teixeira2021_zarc.pdf` (Equação 9)
- `binkley2017.pdf` (Tabelas 1 e 2; A1 em TB: 34 Mg ha⁻¹ ano⁻¹ de lenho entre 2 e 3 anos, IAF 3,8)
- `campoe2020.pdf`
