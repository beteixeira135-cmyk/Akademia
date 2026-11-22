#!/usr/bin/env bash
# 1) gera o DOCX; 2) renderiza em PDF; 3) lê a página de cada título; 4) regenera com o sumário
set -e
cd "$(dirname "$0")"
python3 gerar_tcc_ufu.py >/dev/null
rm -rf /tmp/render_tcc && mkdir -p /tmp/render_tcc
soffice --headless --convert-to pdf TCC_II_Bernardo_Castro_FINAL.docx --outdir /tmp/render_tcc >/dev/null 2>&1
python3 - <<'PY'
import json, re, subprocess
from pathlib import Path
pdf = "/tmp/render_tcc/TCC_II_Bernardo_Castro_FINAL.pdf"
from gerar_tcc_ufu import ler_corpo, ORIGEM
corpo = ler_corpo(ORIGEM)
titulos = []
for l in corpo.split("\n"):
    if l.startswith("## "): titulos.append((1, l[3:].strip()))
    elif l.startswith("### "): titulos.append((2, l[4:].strip()))
titulos.insert(0, (1, "RESUMO")); titulos.insert(1, (1, "ABSTRACT"))
n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
paginas = []
for k in range(1, n + 1):
    paginas.append(subprocess.run(["pdftotext", "-f", str(k), "-l", str(k), "-layout", pdf, "-"], capture_output=True, text=True).stdout)
achados = []
inicio = next(k for k, t in enumerate(paginas) if "SUMÁRIO" in t) + 1  # busca só depois do sumário
for nivel, t in titulos:
    chave = re.sub(r"\s+", " ", t).strip()
    for k in range(inicio, n):
        if chave in re.sub(r"\s+", " ", paginas[k]):
            # numeração: página física menos as páginas antes da Introdução (capa, rosto, aprovação, resumo, abstract, sumário)
            achados.append((nivel, t, k + 1)); inicio = k; break
intro = next(p for (nv, t, p) in achados if t == "1 INTRODUÇÃO")
# páginas a partir da Introdução são numeradas começando em 1 (decisão do modelo: contagem contínua a partir do rosto)
out = [(nv, t, p) for nv, t, p in achados if t not in ("RESUMO", "ABSTRACT")]
Path("sumario.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print("sumário:", len(out), "itens; introdução na página física", intro)
PY
python3 gerar_tcc_ufu.py
python3 - <<'PY'  # segunda passada não é necessária: páginas do sumário não mudam de tamanho
import zipfile, shutil, re
src = "TCC_II_Bernardo_Castro_FINAL.docx"; tmp = "tmp.docx"
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        d = zin.read(it.filename)
        if it.filename == "word/settings.xml":
            d = re.sub(rb"<w:zoom(?![^>]*w:percent)", b'<w:zoom w:percent="100"', d)
        zout.writestr(it, d)
shutil.move(tmp, src)
PY
python3 validar_docx.py TCC_II_Bernardo_Castro_FINAL.docx
