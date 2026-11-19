# Akademia

Repositório privado do TCC II de Bernardo Teixeira de Castro (Engenharia Florestal, UFU): **módulo de desfolha
(pragas e doenças) no modelo ecofisiológico 3-PG para eucalipto**, com calibração bayesiana da compensação
fisiológica, um local por bioma onde há eucalipto e a plataforma web **Akademia Florestal**.

- Regras do projeto e mapa de pastas: [`AGENTS.md`](AGENTS.md) (vale para qualquer IA).
- Estado atual: [`memoria/contexto_ativo.md`](memoria/contexto_ativo.md) e [`memoria/progresso.md`](memoria/progresso.md).
- Passagem de bastão: [`PASSAGEM_DE_BASTAO.md`](PASSAGEM_DE_BASTAO.md) (gerada por `python3 ferramentas/gerar_passagem.py`).
- **VS Code:** abra esta pasta, execute `Python: criar ambiente virtual` e depois `Python: instalar dependências de calibração`. Use `Calibração: recalcular e avaliar pacote atual` para a calibração, ou `Testes: modelo e experimentos` para gerar a matriz e rodar as suítes.
- Para os testes completos, disponibilize `fontes_r3PG/data-raw/data.input.xlsx` e `data.default.xlsx` (ou configure `R3PG_SRC`) e `experimentos/saida/mensal.csv.gz`.
- **Atenção:** `ferramentas/pipeline.py` faz commit e tenta enviar `HEAD:main` ao fim de cada etapa; não o use para rodar análises sem revisar esse comportamento.

Só dados secundários. PDFs de artigos e arquivos grandes ficam no Google Drive (pasta 3-PG), não aqui.
