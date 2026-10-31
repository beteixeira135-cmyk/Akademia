// Gera o TCC II no modelo UFU/ICIAG (ABNT). Uso: node gerar.js [paginas.json]
const fs = require("fs");
const D = require("docx");
const C = require("./conteudo.js");
const { Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell, WidthType, BorderStyle,
  ImageRun, Header, PageNumber, PageBreak, TabStopType, PositionalTab, PositionalTabAlignment, PositionalTabLeader,
  PositionalTabRelativeTo, SectionType, VerticalAlign, LineRuleType } = D;

const PG = process.argv[2] && fs.existsSync(process.argv[2]) ? JSON.parse(fs.readFileSync(process.argv[2])) : {};
const LARG = 11906 - 1701 - 1134; // largura útil (twips)
const FONTE = "Times New Roman";
const L15 = { line: 360, lineRule: LineRuleType.AUTO }, L10 = { line: 240, lineRule: LineRuleType.AUTO };

// ---------- texto com marcação inline ----------
function runs(txt, base = {}) {
  const out = []; let i = 0, b = false, it = false, sup = false, sub = false, buf = "";
  const flush = () => { if (buf) out.push(new TextRun({ text: buf, font: FONTE, bold: b || base.bold, italics: it || base.italics,
      superScript: sup, subScript: sub, size: base.size || 24, allCaps: base.allCaps })); buf = ""; };
  while (i < txt.length) {
    if (txt.startsWith("**", i)) { flush(); b = !b; i += 2; continue; }
    const c = txt[i];
    if (c === "*") { flush(); it = !it; i++; continue; }
    if (c === "^") { flush(); sup = !sup; i++; continue; }
    if (c === "~") { flush(); sub = !sub; i++; continue; }
    buf += c; i++;
  }
  flush(); return out;
}
const P = (txt, o = {}) => new Paragraph({ alignment: o.align ?? AlignmentType.JUSTIFIED, spacing: { ...(o.sp ?? L15), before: o.before ?? 0, after: o.after ?? 0 },
  indent: o.indent === false ? undefined : { firstLine: o.indent ?? 851 }, keepNext: o.keepNext, pageBreakBefore: o.pageBreakBefore,
  children: runs(txt, o.run || {}) });
const vazio = (n = 1, sp = L15) => Array.from({ length: n }, () => new Paragraph({ spacing: sp, children: [] }));
const centro = (txt, o = {}) => P(txt, { align: AlignmentType.CENTER, indent: false, sp: o.sp ?? L10, run: o.run ?? { bold: true }, ...o });
const tituloPre = (txt, quebra = true) => P(txt, { align: AlignmentType.CENTER, indent: false, sp: L10, run: { bold: true }, after: 240, pageBreakBefore: quebra });

// ---------- contadores ----------
let nFig = 0, nTab = 0; const LFIG = [], LTAB = [], SUM = [];

// ---------- tabelas (3 traços horizontais, abertas nas laterais) ----------
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, LN = { style: BorderStyle.SINGLE, size: 8, color: "000000" };
function tabela(titulo, cab, linhas, larguras, nota) {
  nTab++; LTAB.push(titulo);
  const tot = larguras.reduce((a, b) => a + b, 0), w = larguras.map(x => Math.round(x / tot * LARG));
  w[w.length - 1] += LARG - w.reduce((a, b) => a + b, 0);
  const cel = (t, j, o = {}) => new TableCell({ width: { size: w[j], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: 60, right: 60 },
    borders: { left: NB, right: NB, top: o.top ? LN : NB, bottom: o.bot ? LN : NB },
    children: [new Paragraph({ alignment: j === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: L10, children: runs(String(t), { size: 20, bold: o.bold }) })] });
  const rows = [new TableRow({ tableHeader: true, children: cab.map((t, j) => cel(t, j, { top: true, bot: true, bold: true })) })];
  linhas.forEach((l, k) => rows.push(new TableRow({ cantSplit: true, children: l.map((t, j) => cel(t, j, { bot: k === linhas.length - 1 })) })));
  const out = [
    new Paragraph({ keepNext: true, spacing: { ...L10, before: 240, after: 120 }, alignment: AlignmentType.JUSTIFIED,
      children: [new TextRun({ text: `Tabela ${nTab}. `, bold: true, font: FONTE, size: 24 }), ...runs(titulo)] }),
    new Table({ width: { size: LARG, type: WidthType.DXA }, columnWidths: w, borders: { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB }, rows }),
  ];
  out.push(new Paragraph({ spacing: { ...L10, before: 60, after: 240 }, children: runs(nota || "Fonte: o autor (2026).", { size: 20 }) }));
  return out;
}

// ---------- figuras ----------
function pngSize(f) { const b = fs.readFileSync(f); return [b.readUInt32BE(16), b.readUInt32BE(20)]; }
function figura(arq, wcm, cap) {
  nFig++; LFIG.push(cap);
  const [pw, ph] = pngSize(arq); const w = Math.round(wcm * 37.795), h = Math.round(w * ph / pw);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { ...L10, before: 240 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(arq), transformation: { width: w, height: h } })] }),
    new Paragraph({ alignment: AlignmentType.JUSTIFIED, keepNext: true, spacing: { ...L10, before: 120, after: 240 },
      children: [new TextRun({ text: `Figura ${nFig}. `, bold: true, font: FONTE, size: 24 }), ...runs(cap)] }),
    new Paragraph({ spacing: { ...L10, after: 240 }, children: runs("Fonte: o autor (2026).", { size: 20 }) }),
  ];
}

// ---------- equações ----------
const eq = (txt, n) => new Paragraph({ spacing: { ...L15, before: 120, after: 120 },
  tabStops: [{ type: TabStopType.CENTER, position: Math.round(LARG / 2) }, { type: TabStopType.RIGHT, position: LARG }],
  children: [new TextRun({ text: "\t", font: FONTE }), ...runs(txt.replace(/([A-Za-z])~/g, "$1~")), new TextRun({ text: `\t(${n})`, font: FONTE, size: 24 })] });

// ---------- dados das tabelas ----------
const TABS = {
  clima: () => tabela("Caracterização climática dos locais de simulação (NASA POWER, 2015–2024)",
    ["Local", "T~méd~ (°C)", "T~mín~ (°C)", "T~máx~ (°C)", "Precipitação anual (mm)", "Radiação (MJ m^-2^ d^-1^)", "Dias de geada", "Papel no estudo"],
    [["Indianópolis-MG", "23,2", "17,6", "28,9", "1.129 (943–1.384)", "19,2", "0", "Caso principal"],
     ["Telêmaco Borba-PR", "20,4", "15,1", "25,8", "1.398 (1.053–1.830)", "17,3", "8", "Extrapolação"],
     ["Imperatriz-MA", "28,7", "23,8", "33,6", "1.151 (757–1.627)", "19,1", "0", "Extrapolação"]],
    [2.2, 1, 1, 1, 1.9, 1.4, 1, 1.5], "Precipitação: média anual (mínimo–máximo). Geada: dias com T~mín~ ≤ 0 °C. Fonte: o autor (2026), com dados de NASA (2026)."),
  materiais: () => tabela("Parametrizações genéticas utilizadas e principais parâmetros que as diferenciam",
    ["Material", "Espécie / origem", "Idade inicial", "α~Cx~", "T~máx~ (°C)", "SLA~0~ → SLA~1~ (m^2^ kg^-1^)", "f~N0~", "Uso"],
    [["A1", "*E. urophylla*; Caldeira et al. (2020)", "12 meses", "0,068", "28,65", "9,40 → 8,40", "1,0", "Principal"],
     ["C5", "*E. grandis* × *E. urophylla*, Cerrado-MG; Borges (2009)", "3 meses", "0,08", "40", "13,74 → 7,56", "0,5", "Comparativo"],
     ["C2", "Clone 3336, Curvelo-MG; Borges (2009)", "3 meses", "0,08", "40", "12,69 → 8,60", "0,5", "Adicional"],
     ["C4", "Clone 3336, Itacambira-MG; Borges (2009)", "3 meses", "0,08", "40", "14,43 → 7,48", "0,5", "Adicional"],
     ["C1 / C3", "Clone 3334, Curvelo / Itacambira; Borges (2009)", "3 meses", "0,09 / 0,08", "40", "15,17 → 6,11 / 14,09 → 6,60", "0,5", "Complementar"]],
    [1, 3, 1.1, 0.9, 0.9, 2.1, 0.7, 1.3], "α~Cx~: eficiência quântica máxima; T~máx~: temperatura máxima de crescimento; f~N0~: valor do modificador nutricional com FR = 0. Fonte: o autor (2026), com base nas fontes citadas."),
  verificacao: () => tabela("Estatísticas de verificação da implementação em relação ao r3PG original e ao 3-PG em planilha (VBA)",
    ["Comparação", "n", "R²", "r~yŷ~", "RQEM (%)", "Viés (%)"],
    [["r3PG original (260 controles; W~S~, W~F~, W~R~, volume, IAF, DAP)", "23.873", "1,000000", "1,000000", "< 2 × 10^-13^", "< 5 × 10^-15^"],
     ["3-PG VBA, perenifólia (*Pinus sylvestris*), 6 variáveis", "110", "0,9996–1,0000", "≥ 0,9998", "0,007–0,13", "≤ 0,04"],
     ["3-PG VBA, decídua (*Fagus sylvatica*), 6 variáveis", "110", "1,0000", "1,0000", "≤ 0,021", "≤ 0,003"]],
    [4.4, 1, 1.4, 1.2, 1.3, 1.3]),
  principal: () => tabela("Perda relativa (%) em relação ao controle em Indianópolis, clone A1 e solo de referência, por intensidade de desfolha e calendário",
    ["Idade (meses)", "Variável", "25% único", "25% recorrente", "50% único", "50% recorrente", "95% único", "95% recorrente"],
    [["24 (evento)", "W~F~ e IAF", "22,0", "22,0", "45,5", "45,5", "93,9", "93,9"],
     ["36", "W~F~", "7,4", "7,4", "13,2", "13,2", "25,7", "25,7"],
     ["36", "Volume", "3,5", "3,5", "6,4", "6,4", "23,5", "23,5"],
     ["72", "Volume", "2,0", "2,6", "3,6", "5,0", "11,4", "19,4"],
     ["84", "Volume", "1,7", "2,3", "3,1", "4,5", "9,7", "17,3"],
     ["84", "Biomassa total", "1,7", "2,2", "3,0", "4,5", "9,3", "17,1"],
     ["84", "DAP", "0,6", "0,8", "1,0", "1,5", "3,3", "6,1"],
     ["84", "NPP acumulada", "1,7", "2,3", "3,1", "4,6", "9,8", "17,6"]],
    [1.3, 1.6, 1, 1.2, 1, 1.2, 1, 1.2], "Único: pulso no mês 12 (24 meses de idade); recorrente: pulsos nos meses 12 e 48. NPP acumulada: do evento até 96 meses. Fonte: o autor (2026)."),
  materialclima: () => tabela("Perda relativa de volume (%) aos 84 meses com desfolha de 50% em pulso único: média e amplitude entre os 16 cenários de solo, por local e material",
    ["Local", "A1", "C5", "C2", "C4"],
    [["Indianópolis", "3,1 (2,9–3,3)", "2,3 (1,7–3,3)", "3,1 (2,3–4,2)", "2,3 (1,6–3,3)"],
     ["Telêmaco Borba", "3,0 (2,3–3,4)", "1,9 (1,1–3,3)", "2,5 (1,6–3,6)", "1,7 (1,0–3,2)"],
     ["Imperatriz", "6,2 (5,5–6,8)*", "3,1 (2,4–4,1)", "3,9 (3,0–5,0)", "3,2 (2,4–4,2)"]],
    [2, 1.5, 1.5, 1.5, 1.5], "*Diagnóstico de extrapolação térmica (temperatura média acima da T~máx~ do clone). Fonte: o autor (2026)."),
  rf: () => tabela("Desempenho do metamodelo Random Forest em três esquemas de validação cruzada (média entre os folds)",
    ["Resposta", "Esquema", "Folds", "R²", "r~yŷ~", "RQEM (%)"],
    [["Perda de volume (84 meses)", "*k*-fold 7 × 10 repetições", "70", "0,995 ± 0,001", "0,998", "7,0 ± 0,9"],
     ["", "Um local fora", "3", "0,848 ± 0,074", "0,975", "38,2 ± 9,0"],
     ["", "Um material fora", "4", "0,952 ± 0,060", "0,989", "19,8 ± 12,8"],
     ["Recuperação foliar (meses)", "*k*-fold 7 × 10 repetições", "70", "0,988 ± 0,004", "0,994", "3,4 ± 0,5"],
     ["", "Um local fora", "3", "0,801 ± 0,175", "0,960", "13,2 ± 5,7"],
     ["", "Um material fora", "4", "−1,220 ± 4,348", "0,966", "20,4 ± 28,3"]],
    [2.4, 2.2, 0.8, 1.5, 1, 1.4], "± desvio-padrão entre os folds. n = 1.056 (perda de volume) e 896 (recuperação). Fonte: o autor (2026)."),
  bertulio: () => tabela("Perdas observadas por Bertulio et al. (2008) aos 26 meses e perdas simuladas para o mesmo protocolo em Campo Verde-MT",
    ["Material simulado → observado", "Variável", "L observada (%)", "L simulada, d = 0,95 (%)", "L simulada, d = 0,999 (%)"],
    [["C5 → urograndis", "Volume", "52,9", "36,8", "64,8"],
     ["", "Circunferência/DAP", "24,2", "13,7", "28,5"],
     ["", "Altura", "19,1", "17,1", "34,7"],
     ["A1 → urocam", "Volume", "59,0", "60,6", "79,3"],
     ["", "Circunferência/DAP", "22,9", "26,5", "40,7"]],
    [2.6, 2, 1.5, 1.8, 1.8], "L observada: perda ajustada pela linha de base (14 meses). A1 é *E. urophylla* puro e urocam é *E. urophylla* × *E. camaldulensis*: transferência fraca. Fonte: o autor (2026), com dados de Bertulio et al. (2008)."),
};

// ---------- corpo ----------
const corpo = [];
for (const b of C.corpo) {
  if (b.h1) { SUM.push([b.h1, 1]); corpo.push(P(b.h1, { align: AlignmentType.LEFT, indent: false, run: { bold: true }, after: 240, pageBreakBefore: corpo.length > 0 || true, keepNext: true })); }
  else if (b.h2) { SUM.push([b.h2, 2]); corpo.push(P(b.h2, { align: AlignmentType.LEFT, indent: false, run: { bold: true }, before: 240, after: 240, keepNext: true })); }
  else if (b.p) corpo.push(P(b.p));
  else if (b.li) corpo.push(P("– " + b.li, { indent: 851 }));
  else if (b.eq) corpo.push(eq(b.eq, b.n));
  else if (b.table) corpo.push(...TABS[b.table]());
  else if (b.fig) corpo.push(...figura(b.fig, b.w, b.cap));
}
SUM.push(["5 CONCLUSÃO", 1]);
corpo.push(P("5 CONCLUSÃO", { align: AlignmentType.LEFT, indent: false, run: { bold: true }, after: 240, pageBreakBefore: true }));
C.conclusao.forEach(t => corpo.push(P(t)));
SUM.push(["REFERÊNCIAS", 0]);
corpo.push(tituloPre("REFERÊNCIAS"));
C.referencias.forEach(r => corpo.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { ...L10, after: 240 }, children: runs(r) })));
SUM.push(["APÊNDICE A – REPRODUTIBILIDADE COMPUTACIONAL", 0]);
corpo.push(tituloPre("APÊNDICE A – REPRODUTIBILIDADE COMPUTACIONAL"));
[
  "Os códigos, dados de entrada e saídas deste trabalho estão organizados em um pacote de arquivos que acompanha a versão digital do TCC. A tabela a seguir descreve os componentes necessários para reproduzir os resultados.",
].forEach(t => corpo.push(P(t, { sp: L10, after: 240 })));
corpo.push(...tabela("Componentes do pacote de reprodutibilidade",
  ["Arquivo", "Conteúdo"],
  [["modelo/threepg_pjs.py", "Tradução do núcleo 3-PGpjs do r3PG v0.1.7 e módulo de desfolha"],
   ["modelo/testes/", "28 testes automatizados do módulo"],
   ["experimentos/clones.py", "Parâmetros dos materiais, com a origem de cada valor"],
   ["experimentos/clima.py", "Agregação mensal das séries NASA POWER"],
   ["experimentos/run_experimentos.py", "Matriz de 1.496 tratamentos e execução"],
   ["experimentos/r_check/", "Execução dos controles no r3PG original (R) e comparação"],
   ["experimentos/indicadores.py", "Perdas, recuperação, NPP acumulada e água"],
   ["experimentos/analise.py", "Decomposição fatorial, método de Morris e figuras"],
   ["experimentos/validacao_kfold.py", "Metamodelos e validação cruzada"],
   ["experimentos/adversarial_e_literatura.py", "Auditoria adversarial e confronto com Bertulio et al. (2008)"],
   ["experimentos/testes/", "8 testes automatizados do pipeline experimental"]],
  [3.2, 5]));

// ---------- pré-textuais ----------
const tit = C.meta.titulo.map(x => new TextRun({ text: x.t, bold: true, italics: x.i, font: FONTE, size: 24 }));
const capa = [centro(C.meta.universidade), ...vazio(2, L10), centro(C.meta.autor), ...vazio(12, L10),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: L15, children: tit }), ...vazio(17, L10), centro(C.meta.cidade), centro(C.meta.ano)];
const naturezaTxt = "Trabalho de Conclusão de Curso apresentado ao curso de Engenharia Florestal, Campus Monte Carmelo, da Universidade Federal de Uberlândia, como parte dos requisitos necessários para obtenção do grau de Bacharel em Engenharia Florestal.";
const natureza = (extra = []) => [new Paragraph({ indent: { left: 4535 }, alignment: AlignmentType.JUSTIFIED, spacing: L10, children: runs(naturezaTxt) }), ...extra];
const rosto = [centro(C.meta.universidade), ...vazio(2, L10), centro(C.meta.autor), ...vazio(10, L10),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: L15, children: tit }), ...vazio(4, L10),
  ...natureza([...vazio(1, L10), new Paragraph({ indent: { left: 4535 }, spacing: L10, children: runs(C.meta.orientador) }),
    new Paragraph({ indent: { left: 4535 }, spacing: L10, children: runs(C.meta.coorientador) })]),
  ...vazio(10, L10), centro(C.meta.cidade), centro(C.meta.ano)];
const assin = (nome, papel) => [...vazio(2, L10), centro("_____________________________________", { run: {} }), centro(nome, { run: {} }), centro(papel, { run: {} })];
const aprov = [new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: L10, children: runs(C.meta.autor, { bold: true }) }), ...vazio(3, L10),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: L15, children: tit }), ...vazio(2, L10), ...natureza(), ...vazio(2, L10),
  P("Monte Carmelo, __ de ______________ de 2026.", { align: AlignmentType.RIGHT, indent: false, sp: L10 }), ...vazio(1, L10),
  centro("Banca Examinadora", { run: {} }),
  ...assin("Prof. Álvaro Augusto Vieira Soares", "Orientador"),
  ...assin("Prof. Dr. ou Ms. (Nome completo)", "Membro da Banca"),
  ...assin("Prof. Dr. ou Ms. (Nome completo)", "Membro da Banca"),
  ...vazio(3, L10), centro(C.meta.cidade), centro(C.meta.ano)];

const resumo = [tituloPre("RESUMO"), P(C.resumo, { indent: false, sp: L10 }), ...vazio(1, L10), P(C.palavras, { indent: false, sp: L10 })];
const abstract = [tituloPre("ABSTRACT"), P(C.abstract, { indent: false, sp: L10 }), ...vazio(1, L10), P(C.keywords, { indent: false, sp: L10 })];

const pg = (k) => (PG[k] !== undefined ? String(PG[k]) : "0");
const TABDOT = [{ type: TabStopType.RIGHT, position: LARG, leader: "dot" }];
const linhaLista = (txt, pagina, nivel = 0) => new Paragraph({ spacing: { ...L10, after: 120 }, tabStops: TABDOT, indent: { left: nivel * 284, right: 0 },
  children: [...runs(txt), new TextRun({ text: "\t" + pagina, font: FONTE, size: 24 })] });
const curta = (s) => s.split(/(?<=[a-z\)])\. /)[0].replace(/\.$/, "");
const listaFig = [tituloPre("LISTA DE ILUSTRAÇÕES"), ...LFIG.map((c, i) => linhaLista(`Figura ${i + 1}. ${curta(c)}`, pg(`fig${i + 1}`)))];
const listaTab = [tituloPre("LISTA DE TABELAS"), ...LTAB.map((c, i) => linhaLista(`Tabela ${i + 1}. ${c}`, pg(`tab${i + 1}`)))];
const parLista = (pares) => pares.map(([a, b]) => new Paragraph({ spacing: { ...L10, after: 80 }, tabStops: [{ type: TabStopType.LEFT, position: 2600 }],
  indent: { left: 2600, hanging: 2600 }, children: [...runs(a), new TextRun({ text: "\t", font: FONTE }), ...runs(b)] }));
const siglas = [tituloPre("LISTA DE ABREVIATURAS E SIGLAS"), ...parLista(C.siglas)];
const simb = [tituloPre("LISTA DE SÍMBOLOS"), ...parLista(C.simbolos)];
const sumario = [tituloPre("SUMÁRIO"), ...SUM.map(([t, n], i) => new Paragraph({ spacing: { ...L10, after: 120 }, indent: { left: n === 2 ? 284 : 0 },
  tabStops: TABDOT, children: [...runs(t, { bold: n === 1 || n === 0 }), new TextRun({ text: "\t" + pg(`sum${i}`), font: FONTE, size: 24 })] }))];

fs.writeFileSync("estrutura.json", JSON.stringify({ sum: SUM.map(s => s[0]), nfig: LFIG.length, ntab: LTAB.length }, null, 1));

const page = { size: { width: 11906, height: 16838 }, margin: { top: 1701, left: 1701, bottom: 1134, right: 1134, header: 709 } };
const cab = new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONTE, size: 24 })] })] });
const vazioH = new Header({ children: [new Paragraph({ children: [] })] });
const doc = new Document({
  creator: "Bernardo Teixeira de Castro", title: "TCC II — Módulo de desfolha para o 3-PG",
  styles: { default: { document: { run: { font: FONTE, size: 24 }, paragraph: { spacing: L15 } } } },
  sections: [
    { properties: { page }, headers: { default: vazioH }, children: capa },
    { properties: { page: { ...page, pageNumbers: { start: 1 } }, type: SectionType.NEXT_PAGE }, headers: { default: vazioH },
      children: [...rosto, ...aprov, ...resumo, ...abstract, ...listaFig, ...listaTab, ...siglas, ...simb, ...sumario] },
    { properties: { page, type: SectionType.NEXT_PAGE }, headers: { default: cab }, children: corpo },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("TCC_II_Bernardo_Castro.docx", b); console.log("ok", LFIG.length, "figuras", LTAB.length, "tabelas"); });
