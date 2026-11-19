# Progresso
## Feito
- Revisão documental de recuperação, persistência, interpretação dos ganhos simulados e limites de transferência incorporada em `tcc_docx/conteudo.js`.
- Simulador Akademia: interface e módulos atuais preservados; diferença máxima JS–Python registrada em `1,60075e-13`, abaixo do limite do comparador (`1e-9`).
- Fixture da auditoria numérica movido para `auditoria_final/controles_solo_antes_correcao_dossel.csv`; caminho da auditoria atualizado.
- Removidos snapshots do TCC, versões antigas de fontes e modelos, protótipos da plataforma substituídos e saídas antigas de experimentos/calibração. O histórico Git preserva versões anteriores; o protótipo 3D `plataforma/talhao_sorteado_3pg.html` foi mantido por ser uma interface distinta.
- `py -3 plataforma/construir.py` concluiu; a página `plataforma/docs/index.html` foi reconstruída. `git diff --check` e `git diff --cached --check` passaram.

## Falta
1. Reexecutar `python3 ferramentas/pipeline.py verificar`, auditoria numérica e testes após instalar as dependências Python ausentes; gerar o DOCX após disponibilizar Node.js.
2. Rodar crescimento sem desfolha para TECHS 9 e 22 somente após confirmar os metadados e inventários; reportar erros por variável e separar ajuste de avaliação independente.
3. Reavaliar a apresentação do simulador depois dos testes e da confirmação de todos os dados e alegações exibidos.
