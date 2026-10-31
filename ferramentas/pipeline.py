"""Pipeline único do TCC II. Cada etapa é um comando; `tudo` roda na ordem. Ao final de cada etapa bem-sucedida,
regenera a passagem de bastão e faz commit (se houver git).

Uso: python3 ferramentas/pipeline.py <etapa> [<etapa> ...]
Etapas: verificar, testes, calibracao, experimentos, indicadores, analises, danos, auditoria, tcc, plataforma, passagem, tudo
"""
import subprocess, sys, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PY = sys.executable
ETAPAS = {
    "verificar": [[PY, "-c", "import numpy, pandas, sklearn; print('python ok')"], ["node", "--version"]],
    "testes": [[PY, "-m", "pytest", "-q", "modelo/testes"]],
    "calibracao": [[PY, "calibrar.py", "0.999"], [PY, "calibrar.py", "0.99"]],
    "experimentos": [[PY, "experimentos/run_experimentos.py"]],
    "indicadores": [[PY, "experimentos/indicadores.py"]],
    "analises": [[PY, "experimentos/analise.py"], [PY, "experimentos/estatisticas.py"],
                 [PY, "experimentos/validacao_kfold.py"], [PY, "experimentos/rf_figuras.py"]],
    "danos": [[PY, "experimentos/danos_v2.py"]],
    "auditoria": [[PY, "auditoria_final/auditar_numeros.py"]],
    "tcc": [["node", "tcc_docx/gerar.js"]],
    "plataforma": [[PY, "plataforma/construir.py"]],
    "passagem": [[PY, "ferramentas/gerar_passagem.py"]],
}
CWD = {"calibracao": RAIZ / "calibracao"}
ORDEM = ["verificar", "testes", "calibracao", "experimentos", "indicadores", "analises", "danos", "auditoria", "tcc", "plataforma"]


def commit(msg):
    if (RAIZ / ".git").exists():
        subprocess.run(["git", "-C", str(RAIZ), "add", "-A"], capture_output=True)
        subprocess.run(["git", "-C", str(RAIZ), "commit", "-q", "-m", msg], capture_output=True)
        # salva no GitHub (repositório privado Akademia); falha de rede não interrompe o trabalho
        r = subprocess.run(["git", "-C", str(RAIZ), "push", "-q", "origin", "HEAD:main"], capture_output=True, text=True, timeout=600)
        print("[git] enviado ao GitHub" if r.returncode == 0 else f"[git] push falhou (fica salvo localmente): {r.stderr.strip()[:200]}")


def rodar(etapa):
    t0 = time.time()
    for cmd in ETAPAS[etapa]:
        print(f"[{etapa}] $ {' '.join(cmd)}", flush=True)
        r = subprocess.run(cmd, cwd=CWD.get(etapa, RAIZ))
        if r.returncode != 0:
            print(f"[{etapa}] FALHOU (código {r.returncode}). A passagem de bastão foi atualizada com a falha registrada.")
            (RAIZ / "memoria/contexto_ativo.md").open("a", encoding="utf8").write(
                f"\n- FALHA na etapa `{etapa}` ({time.strftime('%d/%m %H:%M')}): comando `{' '.join(cmd)}`.\n")
            subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
            sys.exit(r.returncode)
    print(f"[{etapa}] ok em {time.time() - t0:.0f} s")
    if etapa != "passagem":
        subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
        commit(f"pipeline: etapa {etapa} concluída")


if __name__ == "__main__":
    pedidas = sys.argv[1:] or ["verificar"]
    for e in (ORDEM if pedidas == ["tudo"] else pedidas):
        if e not in ETAPAS:
            sys.exit(f"Etapa desconhecida: {e}. Opções: {', '.join(ETAPAS)}, tudo")
        rodar(e)
