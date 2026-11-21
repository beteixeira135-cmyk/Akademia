# Progresso
## Feito
- Criada a skill Claude Code versionada `.claude/skills/akademia-tcc/SKILL.md` e ligada ao `CLAUDE.md` para leitura em tarefas substantivas. `AGENTS.md` e `CLAUDE.md` agora alertam que o pipeline pode publicar em `main`.
- Verificados frontmatter e caminhos da skill e `git diff --check`. Não foi possível testá-la em uma sessão Claude Code porque o executável não está disponível. `python3 ferramentas/gerar_passagem.py` falhou com exit 9009 (Python ausente), portanto `PASSAGEM_DE_BASTAO.md`/`CONTEXTO_EMPACOTADO.md` não foram regenerados.
- Revisão documental de recuperação, persistência, interpretação dos ganhos simulados e limites de transferência incorporada em `tcc_docx/conteudo.js`.
- Simulador Akademia: interface e módulos atuais preservados; diferença máxima JS–Python registrada em `1,60075e-13`, abaixo do limite do comparador (`1e-9`).
- Fixture da auditoria numérica movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`; caminho da auditoria atualizado.
- Removidos snapshots do TCC, versões antigas de fontes e modelos, protótipos da plataforma substituídos e saídas antigas de experimentos/calibração. O histórico Git preserva versões anteriores; o protótipo 3D `plataforma/talhao_sorteado_3pg.html` foi mantido por ser uma interface distinta.
- `py -3 plataforma/construir.py` concluiu; a página `plataforma/docs/index.html` foi reconstruída. `git diff --check` e `git diff --cached --check` passaram.
- Workspace VS Code configurado em `.vscode/`, dependências da calibração fixadas em `requirements-calibracao.txt` e ambiente `.venv` instalado.
- Reexecutada a calibração atual: U mediana 1,18 (IC90% 1,01–1,34), a mediana 0,625 (0,225–0,975), γ = 1. LOO no mesmo experimento: RQEM 15,72 → 4,31 p.p.; teste entre materiais no mesmo estudo: C5→A1 19,08 → 8,41 e A1→C5 13,01 → 4,30 p.p. Teste independente Oliveira: perda de volume observada 35,4%, mediana calibrada 33,0% (IC90% 28,1–45,8%).
- A fonte pública r3PG foi clonada na pasta irmã esperada; a matriz mensal foi regenerada localmente. Suítes do modelo e dos experimentos: 57 testes aprovados.
- Busca documental pública confirmou os locais TECHS 9 (Estrela do Sul; aproximadamente 35 km de Indianópolis) e 22 (Telêmaco Borba). Binkley et al. (2017) fornece metadados de sítio e resultados agregados de meia rotação, mas não localizei os inventários brutos para download na página do IPEF nem nas buscas em repositórios consultados. Site 9 é apenas referência próxima para Indianópolis, não validação direta.
- Benchmark adaptado executado para A1 no TECHS 22 com as saídas sem desfolha já calculadas: incremento de lenho simulado 37,06 contra 34 Mg ha⁻¹ ano⁻¹ publicado (+9,0%); IAF simulado aos 24 meses 4,89 contra 3,8 publicado. A segunda comparação é pontual aos 24 meses; a tabela do TCC reporta média simulada de 24–36 meses. Clima municipal e solo do sítio são usados; sobreposição com dados de ajuste A1 não confirmada, portanto não é validação independente.
- `auditoria_final/auditar_numeros.py` compilou após trocar caminhos absolutos por relativos, mas a execução parou por falta de Node.js. A auditoria e o DOCX ainda não foram gerados.
- Em 19/11/2026, corrigidos UTF-8, estrutura HTML e um erro de expressão regular que impedia a execução dos scripts da página. Corrigida também uma propriedade de material incompatível na cena Three.js. `plataforma/construir.py` regenerou o simulador e `docs/index.html`; o navegador abriu a cena 3D, confirmou `charset=UTF-8`, `lang=pt-BR`, `R` e `renderer` ativos e não registrou erro de JavaScript. A desfolha visual passou a ser refletida diretamente por folhas menores e o evento mensal, em conjunto com os números do modelo.

## Feito (21/11/2026 — 2ª passagem)
- Node.js disponível (`/opt/node22/bin/node v22.23.5`).
- Auditoria numérica: **528/528 conferem** (`python3 auditoria_final/auditar_numeros.py`). Zero falhas.
- Correção de 12 caminhos de figura em `entregavel_final/TCC_TEXTO_FINAL.md` (`figuras_padronizadas/` → `figuras/`).
- DOCX gerado: `entregavel_final/TCC_II_Bernardo_Castro_FINAL.docx` (3,1 MB).
- PDF gerado: `entregavel_final/TCC_II_Bernardo_Castro_FINAL.pdf` (2,2 MB).
- Memória, PENDENCIAS e contexto_ativo atualizados.
- Branch `tcc-ii-auditoria-21nov` commitada e enviada ao origin.

## Falta
1. **Matriz de 6 materiais (20.856 cenários):** recuperar `experimentos/saida/possibilidades_6mat/possibilidades.csv` ou reescrever seções 4.3 e 4.10 para refletir apenas os 5.688 cenários (2 materiais) disponíveis.
2. **Figuras N1/N2/N3:** `experimentos/figuras_novas.py` não executado nesta sessão; N2 requer `plataforma/material_tabelas.json`.
3. **Série climática TECHS 22:** download NASA POWER nas coordenadas −24,2/−50,5; script pronto em `auditoria_final/baixar_clima_techs_power.py`; API inacessível no ambiente de execução.
4. **Inventários TECHS 9 e 22:** para avaliação por variável com independência demonstrada.
5. **Upload ao Google Drive:** DOCX e PDF a enviar para a pasta "08 TCC II versão atual" e registrar no Diário.
