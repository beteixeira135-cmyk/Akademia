# PASSAGEM DE BASTÃO — TCC II (para o Astra; atualizado 02-11-2026 16h)

Este relatório serve para outra IA (o Astra ou qualquer outra) continuar o trabalho sem o histórico da conversa. Todo número aqui sai de um arquivo de saída citado ou do texto do TCC. Se algo divergir, o arquivo vale mais que este texto.

## 1. Quem e o quê

- **Autor:** Bernardo Teixeira de Castro, Engenharia Florestal, Universidade Federal de Uberlândia (UFU), campus Monte Carmelo.
- **Orientador:** Álvaro Augusto Vieira Soares.
- **Coorientadora:** Dra. Gabriela Cristina Costa Silva, da Universidade Federal do Recôncavo da Bahia (UFRB).
- **Defesa:** dezembro de 2026, com banca ainda não definida.
- **Título:** "Desenvolvimento e avaliação de um módulo de desfolha para o modelo ecofisiológico 3-PG em povoamentos de eucalipto nos biomas brasileiros". Antes do título novo ser usado, o autor precisa confirmar com a coordenação.
- **Tema:** um módulo de danos para o 3-PG, que é um modelo de crescimento florestal mensal, rodado com a implementação r3PG v0.1.7 e com uma porta Python conferida contra ela. O módulo representa quatro coisas:
  - remoção de folhas (desfolha);
  - perda de eficiência da fotossíntese;
  - morte de árvores;
  - reação da árvore ao ataque, chamada "compensação".
- **Locais:** seis, um por bioma com eucalipto. Indianópolis-MG e Imperatriz-MA (Cerrado), Telêmaco Borba-PR (Mata Atlântica), Almeirim-PA (Amazônia), Araripina-PE (Caatinga) e Eldorado do Sul-RS (Pampa).
- **Origem:** o TCC parte da iniciação científica (IC) do autor, ainda em andamento, que simulou desfolha em Indianópolis. A partir dela, o trabalho foi auditado, corrigido, calibrado e ampliado.
- **Links:**
  - Pasta do Google Drive "3-PG": id 1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L. Subpastas: 08 (versão atual do TCC) e 09 (fontes).
  - Diário: Google Doc "Diário do TCC II", na raiz da pasta.
  - Plataforma Akademia Florestal (simulador web): https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc
  - Código, dados e texto: GitHub privado https://github.com/beteixeira135-cmyk/Akademia

## 2. Regras inegociáveis

1. Só dados secundários. Nunca inventar dado, parâmetro, referência, DOI ou resultado. Sem fonte, escrever que não há.
2. Distinguir as três coisas:
   - **verificação:** o código faz o que as equações dizem;
   - **calibração:** ajuste a dados;
   - **validação:** teste com dados independentes.
3. Todo número do TCC precisa ser recalculável. `python3 auditoria_final/auditar_numeros.py` deve terminar com todos os itens conferindo (hoje são 528 de 528), e `node ferramentas/conferir_texto_auditoria.js` não pode apontar número novo sem item. Os 3 itens que ele aponta hoje são dados de entrada: 1.111, 28,65 e 1,35.
4. O módulo original deve continuar reproduzível. Com `compensation=None`, os resultados são idênticos ao r3PG, e os testes em `modelo/testes` (49) devem passar.
5. Escrita em português do Brasil, ABNT, frases claras, voz ativa e linguagem que qualquer leitor entenda.
   - Regra do autor: o que chama atenção fica no TCC como gráfico; o que ocupa muito espaço mental vai para a Akademia, e o TCC leva o leitor até lá.
   - Ele não quer apêndice com conteúdo que já estava no texto.
6. Tudo o que for entregue vai para a pasta 3-PG do Drive, com uma entrada no Diário do TCC II.
   - O conector do Drive só cria arquivos: crie a versão nova e mande a antiga para a lixeira.
   - Nunca deixe arquivo solto fora da pasta 3-PG.
   - Não sobrescreva versões anteriores; dê um nome novo.
7. RESILIA e o mestrado só aparecem como perspectiva futura.
8. O autor costuma trabalhar pelo celular. Entregue o arquivo pronto, não instruções de terminal.

## 3. Estado atual

### Pronto

1. **TCC II, VERSÃO FINAL v4** (37 páginas, 12 figuras, 3 tabelas, 7 quadros "Na Akademia" com QR code). Arquivos em `entregas/TCC_II_Bernardo_Castro_VERSAO_FINAL_v4_02-11-2026.docx` e `.pdf`.
   - A conclusão tem a subseção 5.1 Perspectivas. Cada perspectiva está presa a um limite: persistência da perda, validação no campo, clones atuais, resiliência com clima futuro (RESILIA, ODS 15, condicionada a mestrado) e ensino.
2. **Verificação.** O código bate com o r3PG nos 308 talhões sem ataque (R² = 1,000). A plataforma em JavaScript bate com o Python em 8 cenários: diferença relativa máxima de 1,6 × 10⁻¹³ (`plataforma/verificacao/comparar.py`).
3. **Calibração da compensação.** Os parâmetros são:
   - **U:** aumento da fotossíntese das folhas que sobram, aplicado só no mês do ataque;
   - **γ:** quanto da transpiração perdida a árvore recupera;
   - **a:** desvio do crescimento para refazer as folhas.

   Resultados (arquivos em `calibracao/saida/`):
   - γ = 1, calibrado com Quentin et al. (2011): a razão de transpiração no modelo ficou em 1,000 (`gamma_quentin2011.json`).
   - U e *a* foram calibrados com Bertulio et al. (2008), Campo Verde-MT, clone urograndis simulado com o C5 (`calibracao_d0999.json`):
     - U = 1,18 (faixa de 90%: 1,01 a 1,34). Em desfolha total quase não sobra folha no mês do ataque, então o experimento não define U, e o valor vem da faixa da literatura.
     - *a* = 0,625 (0,225 a 0,975), pouco definido.
   - Teste no urocam (clone A1, mesmo experimento): o erro caiu de 20,3 para 7,5 pontos percentuais (p.p.).
   - Validação cruzada deixando uma medição de fora: 15,7 para 4,3 p.p. (`validacao_cruzada.json`).
4. **Teste independente** com Oliveira et al. (2014): *E. grandis* em Mucuri-BA, uma desfolha total aos 6 meses, medição 8 meses depois.
   - Medido: 35,4% de perda de volume.
   - Módulo calibrado: 33,0% (faixa de 90%: 28,1 a 45,8%).
   - Módulo original: 77,6%.
   - Erro médio (volume, diâmetro e altura): de 34,3 para 3,2 p.p.
   - Script e saída: `calibracao/teste_oliveira2014.py` e `saida/teste_oliveira2014.json`.
5. **Matriz de três locais** (2.408 tratamentos), biomas (1.728 tratamentos por versão) e espaço de possibilidades (5.688 cenários aptos). O talhão atacado supera o controle em 1,3% dos cenários na versão calibrada (ganho máximo de 5,2%) e em um único cenário na original (`experimentos/saida/possibilidades/resumo_possibilidades.json`).
6. **Plataforma Akademia Florestal (versão 12).** Tem o Material do TCC com as tabelas geradas dos resultados, o quadro de domínio de validade, a cubagem e as toras.
7. **Infraestrutura.**
   - `ferramentas/pipeline.py tudo` refaz tudo, na ordem: verificar, testes, calibração, experimentos, indicadores, análises, danos, biomas, possibilidades, tabelas, plataforma, auditoria e TCC.
   - As tabelas completas são geradas por `tcc_docx/tabelas_dados.py`, sem nenhum número digitado à mão.

### Falta (em ordem)

1. **Autor:** colocar a v4 na pasta 08 e enviá-la ao Álvaro com a ressalva única: o módulo acerta a perda nos meses após a desfolha total, mas não a persistência dela por anos (Matrangolo et al., 2010: 37,9 a 79,7% aos 92 meses, contra 3,8 a 32,1% simulados; `calibracao/saida/testes_adicionais.json`).
2. **Autor:** confirmar o título com a coordenação e pedir à Gabriela uma revisão da calibração.
3. **Preparar a defesa:** roteiro e slides, a partir das figuras N1, N2 e N3 e do teste com Oliveira.
4. **Opcional:** atualizar a cienciometria quando o OpenAlex voltar a responder. O limite gratuito estava esgotado, e o Semantic Scholar já complementou a busca: 469 trabalhos no núcleo.
5. **Opcional:** o artigo da IC para o MENSUFLOR, que usa o trabalho de 2025 do autor como modelo de formato.

## 4. Decisões do autor e suas justificativas

- **Calibração de verdade, e não só reescrita do texto.** Com um local por bioma (o Pantanal ficou fora por não ter plantio comercial).
- **γ calibrado com Quentin et al. (2011).** Isso corrigiu um erro: a calibração rodava com γ = 0, e as simulações usavam 0,5.
- **Copas dos clones de Borges (2009) corrigidas** (`experimentos/clones.py`). A queda de folhas (γF) e a partição para folhas (pFS2) passaram a ser as da TECHS (Caldeira et al., 2020a), porque os valores de Borges davam índice de área foliar (IAF) de 8 a 11, contra 3,0 a 3,8 medidos. O IAF corrigido ficou entre 2,4 e 5,6. A versão antiga continua reproduzível com a variável de ambiente `TCC_DOSSEL=borges`.
- **U só no mês do ataque** (`u_meses = 1`, em `calibracao/saida/regra_compensacao.json`). O aumento medido some em 3 a 5 semanas (Turnbull et al., 2007), e as regras testadas deram ajuste equivalente.
- **Oliveira et al. (2014) nunca entra no ajuste.** Ele é só teste.
- **Precedentes sem conteúdo conferido ficam fora.** Kautz et al. (2018) e Krause et al. (2025) não entraram na tabela de precedentes por esse motivo.
- **TCC curto e acessível** (cerca de 35 páginas), com o material denso na Akademia.

## 5. Limitações a declarar (já estão na seção 4.8)

- (a) O modelo não tem reservas de açúcar.
- (b) O investimento em folhas (*a*) vem de um único experimento e ficou pouco definido; o teste independente cobre 8 meses.
- (c) O teste e a validação cruzada usam medições do mesmo experimento.
- (d) U não é definido por desfolha total e vem da literatura.
- (e) O módulo subestima a persistência da perda (Matrangolo et al., 2010).
- (f) A morte de árvores e o percevejo-bronzeado são cenários sem medição de campo.
- (g) A copa dos clones de Borges vem de outro clone, e o A1 passa do seu limite de temperatura em três locais.
- (h) Cada bioma é representado por um único local.
- (i) Não há experimento de desfolha nos locais simulados.

## 6. Mapa de arquivos e como rodar

A raiz é o repositório GitHub (no ambiente de origem, `/home/claude/tcc`). Leia primeiro `AGENTS.md`, `memoria/contexto_ativo.md` e `memoria/decisoes.md`.

| Caminho | Conteúdo |
|---|---|
| `modelo/threepg_pjs.py` | O 3-PG com o módulo; testes em `modelo/testes` |
| `experimentos/` | Matriz, controles, danos, biomas, possibilidades, Random Forest, Morris, figuras |
| `calibracao/` | γ, U e *a*, validação cruzada, testes com Matrangolo, Quentin, Barry/Eyles e Oliveira |
| `tcc_docx/conteudo.js` | Texto do TCC |
| `tcc_docx/gerar.js` | Gerador do .docx; usar `node gerar.js paginas.json` |
| `tcc_docx/tabelas_dados.py` | Gera as tabelas a partir dos resultados |
| `auditoria_final/auditar_numeros.py` | Auditoria dos números citados |
| `ferramentas/` | Pipeline, conferidor texto × auditoria, conferidor de referências, gerador de passagem |
| `plataforma/` | Akademia; `sincronizar_dados.py` puxa parâmetros e calibração do Python; `construir.py` monta a página |
| `entregas/` | Versões do TCC; nunca sobrescreva |

Comandos:

```
python3 ferramentas/pipeline.py tudo                      # refaz tudo (~15 min, 2 núcleos)
python3 auditoria_final/auditar_numeros.py                 # deve conferir todos os itens
node ferramentas/conferir_texto_auditoria.js               # número do texto sem item na auditoria
node ferramentas/conferir_referencias.js                   # referência sem citação = 0
cd tcc_docx && node gerar.js paginas.json                  # .docx
# PDF: LibreOffice com --outdir para outra pasta (o PDF dentro de tcc_docx/ fica bloqueado);
# depois python3 paginas.py <pdf> e gere de novo, até o sumário ficar estável (2 a 3 passadas)
```

## 7. Instruções para o Astra (ou outra IA)

- **Sem execução de código:** só redija texto (por exemplo, slides da defesa). Use os números deste relatório ou do TCC v4 e marque [CONFERIR] em qualquer número que ainda não exista num arquivo de saída.
- **Com execução de código:** siga a lista "Falta". Depois de qualquer mudança no modelo, rode `pipeline.py tudo`, a auditoria e os dois conferidores antes de tocar no texto.
- **A cada etapa:**
  - atualize `memoria/contexto_ativo.md`, `memoria/progresso.md` e, se houve escolha, `memoria/decisoes.md`;
  - rode `python3 ferramentas/gerar_passagem.py`;
  - faça commit;
  - recrie no Drive o "Diário do TCC II" e esta passagem, mandando as versões antigas para a lixeira.
- **Nunca invente resultado,** nem para "fechar" um texto. Se faltar dado, escreva que falta.
- **Ao falar com o autor:** seja direto e sincero. Ele prefere saber de um problema a receber um elogio.
