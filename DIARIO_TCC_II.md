# Diário do TCC II — Bernardo Teixeira de Castro

Módulo de desfolha para o modelo ecofisiológico 3-PG em povoamentos de eucalipto em Indianópolis-MG, Telêmaco Borba-PR e Imperatriz-MA.
Orientador: Álvaro Augusto Vieira Soares · Coorientadora: Gabriela Cristina Costa Silva · UFU, Engenharia Florestal.

Regra permanente: só dados secundários; nada de dados, parâmetros, referências ou validação inventados.

---

## Estado atual (31/10/2026)

- TCC II: 41 páginas, 9 figuras e 11 tabelas, já incluindo os outros danos de pragas e doenças. Sem buracos de página; auditoria numérica sem divergências; 36 testes do modelo aprovados.
- Plataforma Akademia Florestal publicada: https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc. Inclui biblioteca de 49 conceitos, modo explicar, cubagem explicativa e taper seccional com toras; pensada para ser usada por quem não é da área.
- Artigo da IC no formato MENSUFLOR (modelo do trabalho de mogno, M135), com 7 páginas.
- Documento de preparação da defesa criado, mas ainda sem as seções preenchidas: https://claude.ai/artifact/YX9RX245H1xYjufaCytW34
- Arquivos da versão atual: pasta **08 TCC II — versão atual (31-10-2026)** dentro de 3-PG (TCC .docx/.pdf, pacote de reprodutibilidade, MENSUFLOR .docx/.pdf, página da plataforma).

## Registro

### Até 30/10/2026
- **Escopo.** O TCC foi ampliado de Indianópolis para os 3 locais. A IC fez só Indianópolis, sem caracterização do local; o TCC faz a comprovação da IC com dados secundários.
- **Solos locais (CAD).**

  | Local | CAD | Fonte |
  |---|---|---|
  | Indianópolis | 215 mm | TECHS 9, Estrela do Sul |
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

## Pendências do autor
- Banca: ainda não definida. Defesa em dezembro de 2026.
- Resolvido: a Gabriela é da UFRB; a frase da IC foi confirmada ("foi a base; a partir dela auditamos, aprimoramos e corrigimos; agora estamos calibrando"); o link da plataforma fica no apêndice.
