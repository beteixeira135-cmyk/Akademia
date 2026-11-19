# Diário do TCC II — Bernardo Teixeira de Castro

Módulo de desfolha para o modelo ecofisiológico 3-PG em povoamentos de eucalipto em Indianópolis-MG, Telêmaco Borba-PR e Imperatriz-MA.
Orientador: Álvaro Augusto Vieira Soares · Coorientadora: Gabriela Cristina Costa Silva · UFU, Engenharia Florestal.

Regra permanente: só dados secundários; nada de dados, parâmetros, referências ou validação inventados.

---

## Estado atual (19/11/2026)

- O código-fonte atual do TCC está em `tcc_docx/conteudo.js`; a revisão textual de recuperação, persistência e limites foi registrada em 19/11. O DOCX foi gerado com 12 figuras e 3 tabelas; a auditoria numérica passou em 528/528 verificações cadastradas, sem cobrir automaticamente toda entrada, parâmetro, referência e número do tutorial.
- Repositório privado no GitHub (fonte da verdade, salvo a cada etapa): https://github.com/beteixeira135-cmyk/akademia
- A plataforma registrada no projeto é a Akademia Florestal v8, com conceitos, modo explicar, tutorial, cenários de desfolha e outros danos, compensação, faixa de incerteza, domínio de validade, exportação e cubagem/toras. A equivalência JS–Python foi reexecutada em oito cenários, com diferença relativa máxima de 6,16 × 10⁻¹⁴; a fonte foi reconstruída em `docs/index.html`. Antes da defesa, confirmar que a URL publicada aponta para essa versão.
- Artigo da IC no formato MENSUFLOR (modelo do trabalho de mogno, M135), com 7 páginas.
- Documento de preparação da defesa criado, mas ainda sem as seções preenchidas: https://claude.ai/artifact/YX9RX245H1xYjufaCytW34
- O simulador está verificado contra a implementação Python, mas não validado em campo nos seis locais. O teste independente com Oliveira et al. cobre oito meses após desfolha total; persistência por anos e transferência entre materiais seguem limites explícitos.
- Ambiente VS Code preparado em `.vscode/` com `.venv` e dependências da calibração. A calibração, validação cruzada interna, testes adicionais e o teste de Oliveira foram reexecutados. Medianas: U = 1,18 (IC90% 1,01–1,34), a = 0,625 (0,225–0,975), γ = 1; LOO no mesmo estudo: RQEM 15,72 → 4,31 p.p.; Oliveira: 35,4% observado contra 33,0% calibrado (IC90% 28,1–45,8%).
- As suítes do modelo e dos experimentos passaram (57 testes). A fonte r3PG foi clonada na pasta de dependências e `experimentos/saida/mensal.csv.gz` foi gerado localmente. Node.js v26.13.1 está instalado e consta no PATH do usuário, mas este terminal não herdou a pasta; foi usado o caminho completo. Rótulos S5–SA100 seguem sem correspondência verificada. Binkley et al. (2017) identifica TECHS 9 como Estrela do Sul, a cerca de 35 km de Indianópolis; não é uma observação direta do município.
- Limpeza do repositório: removidos snapshots do TCC, versões antigas dos modelos e da plataforma, arquivos de backup e saídas anteriores de experimentos/calibração. O fixture de controle exigido pela auditoria foi preservado em `auditoria_final/controles_solo_antes_correcao_dossel.csv`; o protótipo 3D separado `plataforma/talhao_sorteado_3pg.html` foi mantido. A página atual foi reconstruída com `plataforma/construir.py`.
- As pendências listadas nas entradas datadas abaixo descrevem o estado naquela data, não necessariamente o estado atual.

### 19/11/2026 — Busca de inventários públicos TECHS
- Binkley et al. (2017), DOI [10.1016/j.foreco.2017.09.050](https://doi.org/10.1016/j.foreco.2017.09.050), está disponível no [Repositório Institucional da UNESP](http://hdl.handle.net/11449/163435). As tabelas 1 e 2 confirmam TECHS 9 em Estrela do Sul (−18,73; −47,92) e TECHS 22 em Telêmaco Borba. A tabela 3 identifica A1 como *E. urophylla*; o artigo informa medições semestrais de DAP, altura e profundidade da copa e apresenta produtividade de meia rotação, incluindo A1 no sítio 22 (34 Mg ha⁻¹ ano⁻¹; IAF 3,8).
- A publicação não fornece, nos materiais consultados, as séries brutas de inventário. A página do [IPEF/TECHS](https://www.ipef.br/techs/) descreve a rede e o delineamento, mas não oferece download dos inventários. Buscas no Zenodo, DataCite, Dryad, DataONE e OpenAlex também não localizaram um conjunto de dados diretamente correspondente; isso não prova que os dados não existam em acesso restrito ou sob solicitação.
- Consequência: TECHS 9 não representa Indianópolis; a distância aproximada de 35 km torna seus dados de solo uma referência próxima, mas não uma validação local. Os resultados publicados podem sustentar somente um benchmark adaptado, não reprodução estrita nem validação empírica. Para avaliar o motor por variável, ainda é necessário obter inventários e metadados dos responsáveis pelo TECHS.
- O benchmark adaptado A1/TECHS 22 foi calculado a partir das saídas atuais: incremento simulado de lenho 37,06 Mg ha⁻¹ ano⁻¹ versus 34 publicado entre 24–36 meses (+9,0%); IAF simulado aos 24 meses 4,89 versus 3,8 publicado. A simulação usa NASA POWER nas coordenadas municipais e solo do sítio. Não foi possível confirmar se a observação participou do ajuste A1; não chamar de validação independente. A tabela mostra IAF médio simulado de 24–36 meses, diferente da observação pontual publicada aos 24 meses.

### 19/11/2026 — Auditoria final de validação e tutorial
- Auditoria interna registrada em `AUDITORIA_FINAL_NAO_VALIDADO_2026-11-19.txt`, com cópia na Área de Trabalho. O documento separa erros confirmados, limites de validação, métricas e contramedidas; não substitui conferência de todas as fontes primárias nem validação de campo.
- Reexecuções: auditoria numérica 528/528; 57 testes; equivalência JS–Python em oito cenários (diferença relativa máxima 6,16 × 10⁻¹⁴). O scanner textual encontrou 115 números decimais e três sem item auditado; o verificador de referências encontrou seis candidatos para triagem manual, não seis erros confirmados.
- Correções prioritárias pendentes: seis locais em cinco biomas; tutorial deve usar faixa conjunta de 1,2–15,2% para um ataque, separar Matrangolo original (7,4–32,1%) e calibrado (3,8–11,5%) e informar que a série climática consultada termina em 31/01/2024.
- Validação biológica nos seis locais não existe ainda. A validação cruzada usa o experimento de Bertulio; Oliveira é um teste externo curto e adaptado; Matrangolo mostra subestimação da persistência de longo prazo. Os números de cenários e R² do metamodelo descrevem simulações, não observações de campo.
- `ferramentas/pipeline.py verificar` faz commit e tenta push após a checagem; não foi executado para evitar publicação automática. A verificação equivalente foi feita diretamente. A sincronização do TXT com o Google Drive ainda não foi confirmada.

## Registro

### Até 30/10/2026
- **Escopo.** O TCC foi ampliado de Indianópolis para os 3 locais. A IC fez só Indianópolis, sem caracterização do local; o TCC faz a comprovação da IC com dados secundários.
- **Solos locais (CAD).**

  | Local | CAD | Fonte |
  |---|---|---|
  | Indianópolis | 215 mm | TECHS 9, Estrela do Sul (~35 km; referência de solo próxima) |
  | Telêmaco Borba | 214 mm | TECHS 22 |
  | Imperatriz | 210 mm | SoilGrids + PTF-ZARC (Teixeira et al., 2021) |

- **Experimentos.** São 2.408 tratamentos, incluindo um bloco com solo local de 912 tratamentos (calendários P1, P2 e PA; épocas EA, EJ e EO).
- **Análises.** Random Forest com validação k-fold, por local (LOSO) e por material (LOMO); método de Morris por local; testes de robustez para solo, clima e FR.
- **Texto.**
  - Reescrito no estilo do TCC I.
  - A introdução passou a antecipar os objetivos.
  - Removidas as quebras de página entre seções.
- **Plataforma Akademia Florestal.**
  - Porta do 3-PG em JavaScript, conferida contra o Python (diferença ≤ 2,5e-13).
  - Interface acadêmica, com botões em madeira (ipê, aroeira, pau-mulato), WUE, eficiência quântica efetiva e modal de validação.
  - Incluída no TCC: seções 3.11 e 4.9 e Apêndice A.
- **Publicação da IC.** Formatada para o MENSUFLOR do próximo ano.

### 31/10/2026 — Outras pragas e doenças além da lagarta
- **Novos mecanismos no 3-PG**, com 8 testes novos (36 no total no módulo):
  - perda de eficiência fotossintética: α_C·(1 − r);
  - mortalidade induzida: remove a fração m de árvores com a biomassa média.
- **Catálogo de danos** (experimentos/danos_v2.py → saida/danos_v2.csv):
  - Psilídeo-de-concha: desfolha de 25% (Wilcken et al., 2003).
  - Formigas-cortadeiras: desfolha de 95% aos 18 meses (Zanetti et al., 2014).
  - Mancha foliar: 20% ao mês por 3 meses (cenário exploratório).
  - Percevejo-bronzeado: r = 0,20 e 0,40 por 4 meses (Almeida et al., 2018; Barbosa et al., 2012); cenário exploratório.
  - Murchas, cancros e seca de ponteiros: mortalidade de 5 e 15% (Santos, Auer e Grigoletti Júnior, 2001).
  - Ferrugem: r calibrado para −25 e −35% de DAP aos 12 meses (Silveira e Higashi, 2003).
- **Resultados** (perda de volume aos 84 meses):
  - Formigas causam a maior perda: 4,0 a 14,6%.
  - Psilídeo: 0,4 a 1,6%.
  - Percevejo a 40%: 2,1 a 2,6% em Telêmaco Borba, mas só 0,3 a 0,7% nos locais com estação seca.
  - Ferrugem: exigiu r de 0,63 a 0,92 e deu 1,3 a 4,0% de perda de volume.
  - Mortalidade de 15%: 1,4 a 3,4%, porque as sobreviventes compensam; leia como limite inferior.
  - Recuperação foliar no modelo: 24 a 35 meses, contra cerca de 6 meses no campo para a mancha foliar.
- **Texto atualizado no TCC:**
  - novo objetivo;
  - seções 3.11 e 4.9 (Outros danos);
  - a plataforma passou para 3.12 e 4.10, e as Limitações para 4.11;
  - equações 8 a 11;
  - Tabela 9;
  - 6 referências novas;
  - limitações (c) e (d);
  - conclusão.
- TCC recompilado: 41 páginas. Conferido que não há buracos de página e a auditoria não apontou divergências.
- Pacote de reprodutibilidade atualizado com danos_v2.py, danos_v2.csv e os novos testes.
- Organização no Drive: tudo do TCC II fica na pasta **3-PG**. Este diário fica na raiz dessa pasta.
- **Pendente:**
  - levar os novos danos (perda de eficiência e mortalidade) para a plataforma Akademia Florestal;
  - preencher o documento da defesa.

### 31/10/2026 — Akademia Florestal acessível (conceitos)
- **Pedido.** Explicar todos os conceitos florestais da plataforma, da lei de Beer e da fotossíntese até a RNA e o taper, imaginando um graduando de Biologia como usuário.
- **Biblioteca de conceitos.** Novo link "Conceitos":
  - 46 conceitos em 7 grupos;
  - busca, filtros e trilha para iniciantes (13 conceitos);
  - 11 figuras;
  - 20 quadros "Da biologia para a floresta".
- **Modo explicar.** Com ele ligado, tocar em qualquer parte do simulador abre o conceito correspondente.
- **Tutorial.** Novo passo 2, e os termos do tutorial ficam clicáveis.
- **Honestidade, escrita nos próprios cartões:**
  - o 3-PG não calcula o taper; o perfil do fuste na tela é ilustrativo;
  - a plataforma não usa RNA; no TCC, a RNA só foi comparada como metamodelo;
  - o módulo de desfolha está verificado, mas não validado.
- **Números conferidos** no TCC e nos dados. Corrigidos durante a conferência:
  - α_Cx dos materiais de Borges: 0,08;
  - RQEM do k-fold: 7,7%.
- **Teste em tela de celular:** sem erros; o modo explicar acertou os conceitos testados.
- **Drive, pasta 09 plataforma:** LEIA-ME — Conceitos e modo explicar, e construir.py.
- **Pendente:**
  - arrastar conceitos.js e conceitos_ui.js (enviados no chat) para a pasta 09 plataforma;
  - levar a perda de eficiência e a mortalidade para a plataforma;
  - preencher o documento da defesa.

### 31/10/2026 — Cubagem explicativa e taper seccional
- **Nova janela "Cubagem e toras"**, aberta pelo link no topo ou pelo botão "Toras".
- **Aba Cubagem:**
  - Smalian, Huber e Newton, comparados ao volume exato;
  - fator de forma;
  - cálculo com uma cubagem própria.
- **Aba Taper seccional:**
  - toras da árvore média para serraria (≥ 15 cm), celulose (≥ 8 cm) e energia (≥ 4 cm), com critérios editáveis;
  - comparação controle × desfolhado por hectare.
- **Fontes verificadas:**
  - taper: Schöepfer, T5 (3 × 3 m), de Souza et al. (2016, Scientia Forestalis 44(109):33-40), clone E. grandis × E. camaldulensis;
  - sortimentos: Soares et al. (2003, Revista Árvore 27(6):811-820).
- **Exemplo** (Indianópolis, A1, 50% anual):
  - serraria −35%, contra −12,5% no volume pelo taper e −13,8% no volume do 3-PG;
  - a desfolha rebaixa toras para celulose e lenha.
- **Limitações declaradas:**
  - taper emprestado de outro clone;
  - altura do A1 esquemática;
  - só a árvore média.
- **Também:** 3 conceitos novos (49 no total) e um passo novo no tutorial.
- **Drive, pasta 09 plataforma:**
  - LEIA-ME — Cubagem e taper seccional;
  - construir.py atualizado.
- **Pendente:**
  - arrastar cubagem.js, conceitos.js e conceitos_ui.js para a pasta 09 plataforma;
  - avaliar se o taper entra no TCC; se entrar, nova seção e as 2 referências.

### 31/10/2026 (noite) — Calibração, biomas e ambiente mecanizado
- **Ambiente mecanizado.**
  - Repositório privado Akademia no GitHub.
  - AGENTS.md (regras para qualquer IA), pasta memoria/ e pipeline único (ferramentas/pipeline.py).
  - Commit e envio ao GitHub automáticos a cada etapa.
  - PASSAGEM_DE_BASTAO.md e CONTEXTO_EMPACOTADO.md gerados automaticamente para outra IA continuar.
- **Compensação fisiológica (módulo v3).** Três mecanismos ativos enquanto as folhas estão abaixo do nível anterior à desfolha:
  - mais fotossíntese nas folhas remanescentes (U);
  - mais condutância do dossel (γ);
  - mais alocação às folhas (a).

  Regra adaptada do CABALA (Pinkard et al., 2011). 13 testes novos, 49 no total.
- **Calibração bayesiana** com Bertulio et al. (2008):
  - ajuste no urograndis (C5); validação no urocam (A1), que não entrou no ajuste;
  - U = 1,16 (intervalo de 90%: 1,02 a 1,33); a = 0,55 (0,05 a 0,975);
  - na validação, o erro da perda de volume caiu de 20,3 para 5,8 pontos.
  - Teste com E. globulus (Barry, 2012): o IAF aos 18 meses ficou 8,3% abaixo do controle na versão original e 1,4% na calibrada.
- **Um local por bioma com eucalipto** (bioma pelo IBGE, 2024):
  - Almeirim-PA (Amazônia, Jari);
  - Araripina-PE (Caatinga, IPA);
  - Eldorado do Sul-RS (Pampa, sítio TECHS 6);
  - Pantanal excluído: sem plantio comercial e alagamento não representado;
  - Imperatriz é Cerrado.

  Clima do NASA POWER. Solo: TECHS 6 (145 mm) em Eldorado do Sul; SoilGrids + PTF-ZARC em Almeirim (219 mm) e Araripina (194 mm).
- **Resultados nos biomas:**
  - a calibração reduziu as perdas para cerca de metade com pulso único e um terço com pulsos anuais;
  - a recuperação foliar caiu de 4 a 35 para 2 a 14 meses;
  - incerteza grande com pulsos anuais;
  - em Araripina, a desfolha deu ganho de volume na versão original (economia de água);
  - Random Forest com 6 locais: descrever o clima por números melhorou a transferência (R² de 0,17 para 0,83 na versão calibrada);
  - Morris: nWs é o parâmetro mais influente nos 6 locais;
  - Araripina simulada: 57 a 62 t/ha de biomassa aérea, contra 51 a 132 t/ha medidos pelo IPA (Alves et al., 2007).
- **Texto:**
  - novas seções 3.12, 3.13, 4.10 e 4.11 e Tabelas 10 e 11;
  - objetivos, introdução, resumo, abstract, conclusões, limitações, siglas, símbolos e Apêndice B atualizados;
  - 5 referências novas.

## Pendências do autor
- Banca: ainda não definida. Defesa em dezembro de 2026.
- Resolvido: a Gabriela é da UFRB; a frase da IC foi confirmada ("foi a base; a partir dela auditamos, aprimoramos e corrigimos; agora estamos calibrando"); o link da plataforma fica no apêndice.
