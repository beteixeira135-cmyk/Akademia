"""Gera o DOCX do TCC II no modelo da UFU (Monte Carmelo).

Entrada: TCC_TEXTO_FINAL.md (corpo) e os textos do resumo e do abstract abaixo.
Saída: TCC_II_Bernardo_Castro_FINAL.docx
Formatação (norma do modelo): Times New Roman 12; corpo 1,5; pré e pós-textuais 1,0;
margens sup 3 cm, esq 3 cm, dir 2 cm, inf 2 cm; recuo de 1,5 cm no parágrafo;
subtítulos dos elementos textuais alinhados à esquerda, caixa alta e negrito;
subtítulos dos elementos pré e pós-textuais centralizados, caixa alta e negrito;
paginação no canto superior direito; sem número nos elementos antes da Introdução.
"""
import re, sys
from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

AQUI = Path(__file__).resolve().parent
ORIGEM = AQUI.parent / "tcc_final" / "TCC_TEXTO_FINAL.md"
SAIDA = AQUI / "TCC_II_Bernardo_Castro_FINAL.docx"

TITULO = "SIMULAÇÃO DA DESFOLHA EM PLANTIOS DE *Eucalyptus* COM O MODELO 3-PG: EFEITO NO CRESCIMENTO E NA PRODUÇÃO DE MADEIRA"
AUTOR = "BERNARDO TEIXEIRA DE CASTRO"
ORIENTADOR = "Prof. Álvaro Augusto Soares"
CIDADE = "MONTE CARMELO"
ANO = "2026"

RESUMO = ("Insetos desfolhadores e doenças foliares retiram folhas de plantios de eucalipto, mas o modelo de crescimento 3-PG não representa esse dano, e a produtividade simulada não reflete a perda. "
 "Este trabalho pergunta quanto de madeira se perde com a desfolha em *Eucalyptus urophylla* e como essa perda muda com a intensidade, a frequência e a época do ataque. "
 "Para responder, o trabalho (i) cria um módulo de desfolha acoplado ao 3-PG, com compensação fisiológica e recuperação da copa; (ii) calibra o módulo com parâmetros e dados de campo brasileiros; "
 "(iii) testa o resultado em um experimento externo e mede a sensibilidade a intensidade e frequência. "
 "No teste contra Oliveira et al. (2014), em *Eucalyptus grandis*, a perda observada de 35,4% foi reproduzida com 33,0% após a calibração, contra 77,6% do modelo original. "
 "Em Indianópolis e Telêmaco Borba, um ataque de 25 a 95% gerou perda simulada de 1,2 a 15,2% no volume; são cenários simulados, não medições de campo. "
 "O módulo acompanha a perda nos meses seguintes ao ataque, mas subestima a perda que persiste por anos: em Matrangolo et al. (2010), a perda observada aos 92 meses foi de 37,9 a 79,7%, contra 3,8 a 11,5% do módulo calibrado. "
 "Por isso, o módulo não deve ser usado para prever a produtividade final após uma desfolha total no primeiro ano.")
PALAVRAS_CHAVE = "3-PG. Desfolha. *Eucalyptus urophylla*. Modelagem de processos. Calibração."

ABSTRACT = ("Defoliating insects and foliar diseases remove leaves from eucalyptus plantations, but the 3-PG growth model does not represent this damage, so simulated productivity does not reflect the loss. "
 "This study asks how much wood is lost to defoliation in *Eucalyptus urophylla* and how that loss changes with the intensity, frequency and timing of the attack. "
 "To answer this, the study (i) builds a defoliation module coupled to 3-PG, with physiological compensation and canopy recovery; (ii) calibrates the module with Brazilian parameters and field data; "
 "and (iii) tests the result in an external experiment and measures sensitivity to intensity and frequency. "
 "In the test against Oliveira et al. (2014), in *Eucalyptus grandis*, the observed volume loss of 35.4% was reproduced with 33.0% after calibration, against 77.6% for the original model. "
 "In Indianópolis and Telêmaco Borba, an attack of 25 to 95% produced a simulated volume loss of 1.2 to 15.2%; these are simulated scenarios, not field measurements. "
 "The module follows the loss in the months after the attack but underestimates loss that persists for years: in Matrangolo et al. (2010), the observed loss at 92 months was 37.9 to 79.7%, against 3.8 to 11.5% for the calibrated module. "
 "For this reason, the module should not be used to predict final productivity after total defoliation in the first year.")
KEYWORDS = "3-PG. Defoliation. *Eucalyptus urophylla*. Process-based modelling. Calibration."

# ---------------------------------------------------------------- utilidades
def fonte_base(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    pf = st.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

def configurar_secao(sec):
    sec.top_margin = Cm(3); sec.left_margin = Cm(3)
    sec.right_margin = Cm(2); sec.bottom_margin = Cm(2)
    sec.page_width = Cm(21); sec.page_height = Cm(29.7)

def paragrafo(doc, texto="", alinh=WD_ALIGN_PARAGRAPH.JUSTIFY, recuo=True, espaco=1.5,
              negrito=False, caixa_alta=False, depois=0):
    p = doc.add_paragraph()
    p.alignment = alinh
    pf = p.paragraph_format
    pf.line_spacing = espaco
    pf.first_line_indent = Cm(1.5) if recuo else None
    pf.space_after = Pt(depois)
    adicionar_runs(p, texto.upper() if caixa_alta else texto, negrito)
    return p

def adicionar_runs(p, texto, negrito=False):
    """Trata **negrito** e *itálico* (inclusive itálico dentro de negrito)."""
    for bloco in re.split(r"(\*\*.+?\*\*)", texto):
        if not bloco:
            continue
        neg = negrito
        if bloco.startswith("**") and bloco.endswith("**") and len(bloco) > 4:
            bloco, neg = bloco[2:-2], True
        for parte in re.split(r"(\*[^*]+\*)", bloco):
            if not parte:
                continue
            it = parte.startswith("*") and parte.endswith("*") and len(parte) > 2
            t = parte[1:-1] if it else parte
            r = p.add_run(t)
            r.italic = it
            r.bold = neg
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

def quebra(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def campo_paginacao(sec):
    """Número de página no canto superior direito."""
    hdr = sec.header
    hdr.is_linked_to_previous = False
    p = hdr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run()
    for tag, txt in [("begin", None), (None, "PAGE"), ("end", None)]:
        if tag:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag); r._r.append(el)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = txt; r._r.append(el)
    r.font.name = "Times New Roman"; r.font.size = Pt(12)

def tabela_norma(doc, linhas):
    """Tabela com três traços horizontais (topo, cabeçalho, rodapé), abertas nas laterais."""
    cab, corpo = linhas[0], linhas[2:]
    t = doc.add_table(rows=0, cols=len(cab))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    def bordas(linha, topo=False, base=False):
        for c in linha.cells:
            tcPr = c._tc.get_or_add_tcPr()
            b = OxmlElement("w:tcBorders")
            for lado in ("top", "bottom"):
                e = OxmlElement(f"w:{lado}")
                ativo = (lado == "top" and topo) or (lado == "bottom" and base)
                e.set(qn("w:val"), "single" if ativo else "nil")
                e.set(qn("w:sz"), "6"); e.set(qn("w:color"), "000000")
                b.append(e)
            tcPr.append(b)
    def linha(vals, topo=False, base=False):
        row = t.add_row()
        for i, v in enumerate(vals):
            cell = row.cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i else WD_ALIGN_PARAGRAPH.LEFT
            adicionar_runs(p, v.strip(), False)
            for r in p.runs: r.font.size = Pt(10)
        bordas(row, topo, base)
    linha(cab, topo=True, base=True)
    for l in corpo[:-1]:
        linha(l)
    linha(corpo[-1], base=True) if corpo else None

# ---------------------------------------------------------------- leitura do corpo
def ler_corpo(caminho):
    texto = caminho.read_text(encoding="utf-8")
    texto = texto.replace("## 4 RESULTADOS\n", "## 4 RESULTADOS E DISCUSSÃO\n")
    texto = texto.replace("## 6 CONCLUSÃO", "## 5 CONCLUSÃO")
    # título e bloco de autoria saem do corpo (a capa e a folha de rosto os trazem)
    texto = re.sub(r"^# .*?\n---\n", "", texto, flags=re.S)
    # Anexo A (tutorial e glossário), depois das referências
    anexo = (AQUI.parent / "tcc_docx" / "ANEXO_A_TUTORIAL_E_GLOSSARIO.md")
    if anexo.exists():
        a = anexo.read_text(encoding="utf-8")
        a = re.sub(r"^# .*?\n", "", a, count=1)           # título do anexo tratado à parte
        a = "\n".join(l[2:] if l.startswith("> ") else l for l in a.split("\n"))
        a = re.sub(r"^---\s*$", "", a, flags=re.M)
        texto = texto.rstrip() + "\n\n## ANEXO A – TUTORIAL DO SIMULADOR E GLOSSÁRIO\n" + a
    return texto

def carregar_sumario():
    """Lê o arquivo sumario.json (gerado a partir do PDF renderizado)."""
    import json
    caminho = AQUI / "sumario.json"
    if caminho.exists():
        return [tuple(x) for x in json.loads(caminho.read_text(encoding="utf-8"))]
    return []

def main():
    doc = Document()
    fonte_base(doc)
    sec = doc.sections[0]
    configurar_secao(sec)

    # ----- CAPA (1 página, conta como a folha de rosto)
    paragrafo(doc, "UNIVERSIDADE FEDERAL DE UBERLÂNDIA", WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(8): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, AUTOR, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(6): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, TITULO, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(8): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, CIDADE, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0)
    paragrafo(doc, ANO, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0)
    quebra(doc)

    # ----- FOLHA DE ROSTO
    paragrafo(doc, AUTOR, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(6): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, TITULO, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(4): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, "Trabalho de Conclusão de Curso apresentado ao curso de Engenharia Florestal, Campus Monte Carmelo, da Universidade Federal de Uberlândia, como parte dos requisitos necessários para obtenção do grau de Bacharel em Engenharia Florestal.",
              WD_ALIGN_PARAGRAPH.JUSTIFY, False, 1.0)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, f"Orientador: {ORIENTADOR}", WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
    for _ in range(6): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, CIDADE, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0)
    paragrafo(doc, ANO, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0)
    quebra(doc)

    # ----- FOLHA DE APROVAÇÃO
    paragrafo(doc, AUTOR, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(3): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, TITULO, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    for _ in range(3): paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, "Trabalho de Conclusão de Curso apresentado ao curso de Engenharia Florestal, Campus Monte Carmelo, da Universidade Federal de Uberlândia, como parte dos requisitos necessários para obtenção do grau de Bacharel em Engenharia Florestal.",
              WD_ALIGN_PARAGRAPH.JUSTIFY, False, 1.0)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, f"{CIDADE}, ____ de ______________ de {ANO}.", WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
    paragrafo(doc, "Banca Examinadora", WD_ALIGN_PARAGRAPH.LEFT, False, 1.0, True)
    for papel in ["Prof. Dr. ou Ms. (Nome completo) – Orientador(a)",
                  "Prof. Dr. ou Ms. (Nome completo) – Membro da banca",
                  "Prof. Dr. ou Ms. (Nome completo) – Membro da banca"]:
        paragrafo(doc, "", espaco=1.0)
        paragrafo(doc, "_____________________________________", WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
        paragrafo(doc, papel, WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
    quebra(doc)

    # ----- RESUMO
    paragrafo(doc, "RESUMO", WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, RESUMO, WD_ALIGN_PARAGRAPH.JUSTIFY, True, 1.0)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, "Palavras-chave: " + PALAVRAS_CHAVE, WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
    quebra(doc)

    # ----- ABSTRACT
    paragrafo(doc, "ABSTRACT", WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, ABSTRACT, WD_ALIGN_PARAGRAPH.JUSTIFY, True, 1.0)
    paragrafo(doc, "", espaco=1.0)
    paragrafo(doc, "Key words: " + KEYWORDS, WD_ALIGN_PARAGRAPH.LEFT, False, 1.0)
    quebra(doc)

    # ----- SUMÁRIO estático (páginas lidas do PDF renderizado; ver gerar_com_paginas.sh)
    paragrafo(doc, "SUMÁRIO", WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
    paragrafo(doc, "", espaco=1.0)
    for nivel, titulo, pag in carregar_sumario():
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Cm(0 if nivel == 1 else 0.8)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16), alignment=2, leader=1)  # direita, pontilhado
        adicionar_runs(p, f"{titulo}\t{pag}", nivel == 1)
    quebra(doc)

    # ----- CORPO (nova seção: paginação aparece a partir da Introdução)
    nova = doc.add_section(WD_SECTION.NEW_PAGE)
    configurar_secao(nova)
    corpo = ler_corpo(ORIGEM)
    numerado = False
    linhas = corpo.split("\n")
    i = 0
    dentro_tabela = []
    while i < len(linhas):
        l = linhas[i].rstrip()
        if l.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith("|"):
                bloco.append([c for c in linhas[i].strip().strip("|").split("|")])
                i += 1
            # legenda da tabela (linha anterior "**Tabela ...**") já foi escrita
            tabela_norma(doc, bloco)
            paragrafo(doc, "", espaco=1.0)
            continue
        if not l.strip():
            i += 1; continue
        mf = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", l)
        if mf:
            caminho = AQUI / mf.group(2)
            pic = doc.add_paragraph(); pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pic.paragraph_format.line_spacing = 1.0; pic.paragraph_format.keep_with_next = True
            pic.add_run().add_picture(str(caminho), width=Cm(15))
            cap = mf.group(1)
            m2 = re.match(r"^(Figura \d+)\. (.*)$", cap)
            cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            cp.paragraph_format.line_spacing = 1.0; cp.paragraph_format.space_after = Pt(12)
            if m2:
                r1 = cp.add_run(m2.group(1) + ". "); r1.bold = True; r1.font.size = Pt(10); r1.font.name = "Times New Roman"
                adicionar_runs(cp, m2.group(2), False)
                for r in cp.runs: r.font.size = Pt(10)
            else:
                adicionar_runs(cp, cap, False)
            i += 1; continue
        if l.startswith("## "):
            titulo = l[3:].strip()
            if titulo.startswith("ANEXO A"):
                quebra(doc)
                paragrafo(doc, titulo, WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
                paragrafo(doc, "", espaco=1.0)
            elif titulo == "REFERÊNCIAS":
                quebra(doc)
                paragrafo(doc, "REFERÊNCIAS", WD_ALIGN_PARAGRAPH.CENTER, False, 1.0, True)
                paragrafo(doc, "", espaco=1.0)
            else:
                paragrafo(doc, titulo, WD_ALIGN_PARAGRAPH.LEFT, False, 1.5, True, depois=6)
            i += 1; continue
        if l.startswith("### "):
            paragrafo(doc, l[4:].strip(), WD_ALIGN_PARAGRAPH.LEFT, False, 1.5, True, depois=6)
            i += 1; continue
        if l.startswith("**Tabela") or l.startswith("**Tabela"):
            paragrafo(doc, re.sub(r"\*\*", "", l), WD_ALIGN_PARAGRAPH.LEFT, False, 1.0, True, depois=6)
            i += 1; continue
        if l.startswith("- "):
            p = paragrafo(doc, "• " + l[2:], WD_ALIGN_PARAGRAPH.JUSTIFY, False, 1.5)
            p.paragraph_format.left_indent = Cm(1.0)
            i += 1; continue
        m = re.match(r"^(\d+)\. (.*)", l)
        if m:
            p = paragrafo(doc, f"{m.group(1)}. {m.group(2)}", WD_ALIGN_PARAGRAPH.JUSTIFY, False, 1.5)
            p.paragraph_format.left_indent = Cm(1.0)
            i += 1; continue
        # referências: entrada sem recuo, espaço simples, separadas por linha em branco
        if corpo_referencias(linhas, i):
            paragrafo(doc, l, WD_ALIGN_PARAGRAPH.LEFT, False, 1.0, depois=12)
            i += 1; continue
        paragrafo(doc, l, WD_ALIGN_PARAGRAPH.JUSTIFY, True, 1.5)
        i += 1

    # rodapé de paginação: a partir da Introdução (cabeçalho com número nas seções seguintes)
    sem = doc.sections[0].header; sem.is_linked_to_previous = False
    sem.paragraphs[0].text = ""
    campo_paginacao(doc.sections[1])
    # atualizar campos ao abrir
    doc.save(SAIDA)
    print("gerado:", SAIDA)

def corpo_referencias(linhas, i):
    """Dentro da seção REFERÊNCIAS, parágrafos são referências (até o anexo)."""
    for j in range(i, -1, -1):
        if linhas[j].startswith("## "):
            return linhas[j].strip() == "## REFERÊNCIAS"
    return False

if __name__ == "__main__":
    main()
