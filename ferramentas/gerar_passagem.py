"""Gera PASSAGEM_DE_BASTAO.md a partir da memória do projeto, dos resultados salvos e do histórico do git,
e o CONTEXTO_EMPACOTADO.md (código + memória) com contagem de tokens. Nenhum número é digitado aqui:
tudo vem dos arquivos de memória (escritos ao fim de cada etapa) ou dos JSON de saída."""
import datetime as dt, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tokens import contar
from empacotar import empacotar

RAIZ = Path(__file__).resolve().parents[1]
ler = lambda r: (RAIZ / r).read_text(encoding="utf8") if (RAIZ / r).exists() else f"_(arquivo {r} não encontrado)_\n"


def git_log(n=15):
    try:
        return subprocess.run(["git", "-C", str(RAIZ), "log", f"-{n}", "--pretty=format:- %ad %s", "--date=format:%d/%m %H:%M"],
                              capture_output=True, text=True, timeout=20).stdout or "- (sem commits)"
    except Exception:
        return "- (git indisponível)"


def resumo_calibracao():
    p = RAIZ / "calibracao/saida/calibracao_d0999.json"
    if not p.exists():
        return "_(calibração ainda não executada)_"
    j = json.loads(p.read_text())
    f = lambda d: ", ".join(f"{k} {v:.1f}" for k, v in d.items())
    v = j["validacao_A1_urocam"]
    return (f"- U: mediana {j['U']['q50']:.2f} (IC90% {j['U']['q05']:.2f}–{j['U']['q95']:.2f}); "
            f"a: mediana {j['a']['q50']:.2f} (IC90% {j['a']['q05']:.2f}–{j['a']['q95']:.2f}).\n"
            f"- Ajuste C5 — observado: {f(j['observado_C5'])} | original: {f(j['original_C5'])} | calibrado: {f(j['preditiva_media_C5'])}.\n"
            f"- Validação A1/urocam — observado: {f(v['observado'])} | original: {f(v['original'])} | "
            f"calibrado: {f(v['calibrado_media'])} (IC90% {f(v['calibrado_q05'])} a {f(v['calibrado_q95'])}).")


def gerar():
    agora = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    ctx, n_ctx, met, fora = empacotar(100_000)
    (RAIZ / "CONTEXTO_EMPACOTADO.md").write_text(ctx, encoding="utf8")
    corpo = f"""# PASSAGEM DE BASTÃO — TCC II (gerado em {agora})

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` ({n_ctx} tokens, {met}).

{ler('AGENTS.md')}
---
{ler('memoria/projeto.md')}
---
{ler('memoria/contexto_ativo.md')}
---
{ler('memoria/progresso.md')}
---
## Calibração (lido de calibracao/saida/calibracao_d0999.json)
{resumo_calibracao()}

---
{ler('memoria/decisoes.md')}
---
{ler('memoria/tecnico.md')}
---
## Últimos commits
{git_log()}

## Para a IA que continuar
1. Sem execução de código: redija o texto, marcando [CONFERIR] em números ainda não gerados. Nunca invente resultados.
2. Com código: siga "Falta (em ordem)" e rode `python3 ferramentas/pipeline.py <etapa>`.
3. Ao fim de cada passo: atualize `memoria/`, rode este gerador e faça commit.
"""
    n, metodo = contar(corpo)
    corpo = corpo.replace("(gerado em", f"({n} tokens, {metodo}; gerado em", 1)
    (RAIZ / "PASSAGEM_DE_BASTAO.md").write_text(corpo, encoding="utf8")
    return n, n_ctx, metodo


if __name__ == "__main__":
    n, n_ctx, metodo = gerar()
    print(f"PASSAGEM_DE_BASTAO.md: {n} tokens; CONTEXTO_EMPACOTADO.md: {n_ctx} tokens ({metodo})")
