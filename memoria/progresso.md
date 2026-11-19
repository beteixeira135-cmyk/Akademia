# Progresso
## Feito
- Revisão documental de recuperação, persistência, interpretação dos ganhos simulados e limites de transferência incorporada em `tcc_docx/conteudo.js`.
- Simulador Akademia: interface e módulos atuais preservados; diferença máxima JS–Python registrada em `1,60075e-13`, abaixo do limite do comparador (`1e-9`).
- Fixture da auditoria numérica movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`; caminho da auditoria atualizado.
- Removidos snapshots do TCC, versões antigas de fontes e modelos, protótipos da plataforma substituídos e saídas antigas de experimentos/calibração. O histórico Git preserva versões anteriores; o protótipo 3D `plataforma/talhao_sorteado_3pg.html` foi mantido por ser uma interface distinta.
- `py -3 plataforma/construir.py` concluiu; a página `plataforma/docs/index.html` foi reconstruída. `git diff --check` e `git diff --cached --check` passaram.
- Workspace VS Code configurado em `.vscode/`, dependências da calibração fixadas em `requirements-calibracao.txt` e ambiente `.venv` instalado.
- Reexecutada a calibração atual: U mediana 1,18 (IC90% 1,01–1,34), a mediana 0,625 (0,225–0,975), γ = 1. LOO no mesmo experimento: RQEM 15,72 → 4,31 p.p.; teste entre materiais no mesmo estudo: C5→A1 19,08 → 8,41 e A1→C5 13,01 → 4,30 p.p. Teste independente Oliveira: perda de volume observada 35,4%, mediana calibrada 33,0% (IC90% 28,1–45,8%).
- `auditoria_final/auditar_numeros.py` compilou após trocar caminhos absolutos por relativos, mas a execução parou por falta de Node.js. Os testes do modelo e experimentos não completaram: faltam a fonte externa r3PG (`data.input.xlsx`, `data.default.xlsx`) e `experimentos/saida/mensal.csv.gz`.

## Falta
1. Disponibilizar Node.js, fonte de dados r3PG e `experimentos/saida/mensal.csv.gz`; então executar a auditoria numérica e completar as suítes de testes.
2. Gerar o DOCX atualizado após disponibilizar Node.js.
3. Confirmar os metadados e inventários TECHS 9 e 22; só então rodar controles sem desfolha e avaliar erros por variável, separando ajuste de avaliação independente.
4. Reavaliar a apresentação do simulador após as verificações e confirmar a URL publicada.
