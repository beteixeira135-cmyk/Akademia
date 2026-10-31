"""Empacota o projeto num único Markdown para colar em outra IA (mesma ideia do Repomix/Gitingest, sem dependências).
Inclui AGENTS.md, a memória, os resultados resumidos e o código essencial; respeita um orçamento de tokens.
Uso: python3 ferramentas/empacotar.py [orcamento_tokens]   (padrão 100000)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tokens import contar

RAIZ = Path(__file__).resolve().parents[1]
# ordem = prioridade; o que não couber no orçamento é listado no fim como "não incluído"
ARQUIVOS = [
    "AGENTS.md", "memoria/projeto.md", "memoria/contexto_ativo.md", "memoria/progresso.md", "memoria/decisoes.md",
    "memoria/tecnico.md", "calibracao/saida/calibracao_d0999.json", "calibracao/saida/calibracao_d099.json",
    "calibracao/calibrar.py", "calibracao/protocolo.py", "experimentos/clima.py", "experimentos/clones.py",
    "biomas/ptf_zarc.py", "biomas/soilgrids_wcs.py", "modelo/threepg_pjs.py", "experimentos/run_experimentos.py",
    "experimentos/indicadores.py", "ferramentas/pipeline.py", "solos_fontes/SOLOS_LOCAIS.md",
]
LING = {".py": "python", ".js": "javascript", ".json": "json", ".md": "markdown"}


def empacotar(orcamento=100_000):
    partes, total, fora = [], 0, []
    cab = ("# Contexto empacotado — TCC II (3-PG + desfolha)\n\nGerado por ferramentas/empacotar.py. "
           "Leia primeiro AGENTS.md (regras) e memoria/contexto_ativo.md.\n\n")
    total += contar(cab)[0]
    for rel in ARQUIVOS:
        p = RAIZ / rel
        if not p.exists():
            fora.append(f"{rel} (não existe)"); continue
        txt = p.read_text(encoding="utf8", errors="replace")
        bloco = f"\n## {rel}\n\n```{LING.get(p.suffix, '')}\n{txt.rstrip()}\n```\n"
        n = contar(bloco)[0]
        if total + n > orcamento:
            fora.append(f"{rel} ({n} tokens)"); continue
        partes.append(bloco); total += n
    rod = "\n## Não incluído (orçamento)\n" + ("\n".join(f"- {f}" for f in fora) if fora else "- nada") + "\n"
    texto = cab + "".join(partes) + rod
    n, metodo = contar(texto)
    return texto, n, metodo, fora


if __name__ == "__main__":
    orc = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    texto, n, metodo, fora = empacotar(orc)
    (RAIZ / "CONTEXTO_EMPACOTADO.md").write_text(texto, encoding="utf8")
    print(f"CONTEXTO_EMPACOTADO.md: {n} tokens ({metodo}); fora do orçamento: {len(fora)}")
