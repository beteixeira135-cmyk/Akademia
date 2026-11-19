# Progresso
## Feito
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
- Ambiente completado: Node.js v26.13.1 instalado no perfil do usuário, PATH de usuário configurado e dependência `docx` declarada em `tcc_docx/package.json`/lockfile. Dependências Python da `.venv` conferidas.
- Corrigidos caminhos absolutos de Linux nas figuras e no QR do gerador do TCC. Auditoria numérica passou (528 itens); `modelo/testes` e `experimentos/testes` passaram (57 testes); DOCX gerado com 12 figuras e 3 tabelas.
- A conferência automática do texto encontrou três números sem correspondência na tabela de resultados (1.111, 28,65 °C e 1,35); são densidade de plantio, limite térmico e limite de U citados com fórmula ou fonte e precisam de checagem específica.
- Em 19/11/2026, corrigidos UTF-8, estrutura HTML e um erro de expressão regular que impedia a execução dos scripts da página. Corrigida também uma propriedade de material incompatível na cena Three.js. `plataforma/construir.py` regenerou o simulador e `docs/index.html`; o navegador abriu a cena 3D, confirmou `charset=UTF-8`, `lang=pt-BR`, `R` e `renderer` ativos e não registrou erro de JavaScript. A desfolha visual passou a ser refletida diretamente por folhas menores e o evento mensal, em conjunto com os números do modelo.
- Em 19/11/2026, adicionada ao cabeçalho a aba "Diferenças x Rua 3PG.d", com tabela comparativa de 10 aspectos e limites explícitos sobre o que se sabe pela descrição pública.

## Falta
1. Conferir a fórmula/fonte dos três números que a conferência textual não encontrou na tabela de resultados e, se necessário, ampliar a auditoria para entradas e parâmetros citados.
2. Solicitar ou obter inventários e metadados TECHS 9 e 22 e confirmar quais observações entraram no ajuste A1; então avaliar por variável. O benchmark agregado do TECHS 22 já foi calculado, mas não constitui reprodução estrita nem validação empírica.
3. Reavaliar a apresentação do simulador após as verificações e confirmar a URL publicada.
4. Reiniciar o VS Code para que os terminais existentes herdem o PATH atualizado do Node.js.
