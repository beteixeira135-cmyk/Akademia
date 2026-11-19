# Retomada do projeto Akademia / TCC II

Este pacote contém um snapshot do projeto, o relatório de auditoria final e um
atalho para a conversa anterior. Extraia o ZIP para uma pasta com permissão de
escrita antes de executar qualquer comando.

## Conversa e continuidade

- Abra `ABRIR_CONVERSA.url` para tentar retomar a conversa registrada.
- Link da sessão: `agent-host-session://ahp-session/898c3834-62ae-4c9d-a940-617fc3b51010`
- O atalho depende da conta e da disponibilidade da sessão no serviço; não é uma
  cópia do histórico e pode não funcionar após formatação. Guarde também o
  identificador da sessão e entre na mesma conta.
- Estado e pendências: `memoria/contexto_ativo.md`, `memoria/progresso.md`,
  `PASSAGEM_DE_BASTAO.md` e `AUDITORIA_FINAL_NAO_VALIDADO_2026-11-19.txt`.

## Abrir o simulador

No PowerShell, na raiz extraída:

```powershell
Start-Process ".\docs\index.html"
```

O caminho é `docs\index.html`, na raiz do projeto.

## Ambiente e testes

O ZIP não contém `.git`, `.venv`, `node_modules`, caches nem o clone externo
`r3PG`. Em uma instalação nova:

1. Instale Git, Python compatível com `requirements-calibracao.txt` e Node.js.
2. Crie o ambiente Python e instale as dependências:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements-calibracao.txt
   ```

3. Instale as dependências do gerador do DOCX:

   ```powershell
   npm ci --prefix tcc_docx
   ```

4. Se os testes Python indicarem ausência da implementação de referência,
   consulte `.vscode/` e `AGENTS.md` para reconstruir o clone externo `r3PG`.
5. Teste o código:

   ```powershell
   .\.venv\Scripts\python.exe -m pytest -q modelo\testes experimentos\testes
   ```

Não execute `ferramentas\pipeline.py verificar` sem revisar o código: atualmente
essa etapa também tenta criar commit e enviar `HEAD:main`. A sincronização do
projeto com o Google Drive deve ser confirmada separadamente.

## Cópias e acessos

- Repositório privado: https://github.com/beteixeira135-cmyk/akademia
- Pasta 3-PG no Google Drive: https://drive.google.com/drive/folders/1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L

O ZIP não contém histórico Git nem credenciais. Guarde uma cópia fora do
computador antes de formatar e confirme seu acesso ao repositório, ao Drive e à
conta usada para abrir a conversa.
