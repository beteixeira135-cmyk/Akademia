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
    children: [new Paragraph({ keepNext: !o.bot || o.top, keepLines: true, alignment: j === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: L10, children: runs(String(t), { size: 20, bold: o.bold }) })] });
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
  clima: () => tabela("Clima (NASA POWER, 2015–2024) e capacidade de água disponível do solo (0–2 m) adotada para os locais de simulação",
    ["Local", "T~méd~ (°C)", "T~mín~ (°C)", "T~máx~ (°C)", "Precipitação anual (mm)", "Meses secos", "Dias de geada", "ASW~max~ (mm)", "Fonte do solo"],
    [["Indianópolis-MG", "23,2", "17,6", "28,9", "1.129 (943–1.384)", "mai–set", "0", "215 (160–311)", "TECHS 9, Estrela do Sul-MG; Latossolo, 80% argila"],
     ["Telêmaco Borba-PR", "20,4", "15,1", "25,8", "1.398 (1.053–1.830)", "nenhum", "8", "214 (213–231)", "TECHS 22, Telêmaco Borba-PR; Latossolo, 56% argila"],
     ["Imperatriz-MA", "28,7", "23,8", "33,6", "1.151 (757–1.627)", "mai–set", "0", "210 (207–220)", "SoilGrids + PTF-ZARC; 35% argila"]],
    [1.9, 0.9, 0.9, 0.9, 1.6, 1.0, 0.8, 1.3, 2.6], "Precipitação: média anual (mínimo–máximo). Meses secos: chuva média mensal < 50 mm. Geada: dias com T~mín~ ≤ 0 °C. ASW~max~: valor adotado (faixa das verificações cruzadas). Fonte: o autor (2026), com dados de NASA (2026), Binkley et al. (2017), Poggio et al. (2021) e Teixeira et al. (2021)."),
  materiais: () => tabela("Parametrizações genéticas utilizadas e principais parâmetros que as diferenciam",
    ["Material", "Espécie / origem", "Idade inicial", "α~Cx~", "T~máx~ (°C)", "SLA~0~ → SLA~1~ (m^2^ kg^-1^)", "f~N0~", "Uso"],
    [["A1", "*E. urophylla*; Caldeira et al. (2020a)", "12 meses", "0,068", "28,65", "9,40 → 8,40", "1,0", "Principal"],
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
  controles: () => tabela("Crescimento simulado sem desfolha com solo local e dados secundários de referência",
    ["Local", "Material", "Volume aos 84 meses (m^3^ ha^-1^)", "IMA (m^3^ ha^-1^ ano^-1^)", "Lenho, 2–3 anos (Mg ha^-1^ ano^-1^)", "IAF médio, 2–3 anos", "Meses com f~T~ = 0", "Referência medida"],
    [["Telêmaco Borba", "A1", "429", "61", "37,1", "4,8", "0", "34 Mg ha^-1^ ano^-1^; IAF 3,8 (TECHS 22)"],
     ["", "C5", "417", "60", "40,0", "10,3", "0", "–"],
     ["Indianópolis", "A1", "352", "50", "25,9", "3,6", "0", "–"],
     ["", "C5", "356", "51", "28,8", "8,5", "0", "–"],
     ["Imperatriz", "A1*", "227", "32", "14,6", "2,1", "31", "–"],
     ["", "C5", "315", "45", "22,6", "7,2", "0", "–"]],
    [1.6, 0.9, 1.3, 1.2, 1.4, 1.1, 1.0, 2.4], "Lenho: incremento de W~S~(1 − p~BB~) entre 24 e 36 meses. Referência: Binkley et al. (2017), clone A1, mesmo município, mesmo espaçamento; dado não independente da calibração do A1. *Diagnóstico de extrapolação térmica. Fonte: o autor (2026)."),
  principal: () => tabela("Perda relativa de volume (%) aos 84 meses por local, material, intensidade e frequência da desfolha, com solo local, e tempo para a biomassa foliar atingir 95% do controle após pulso único",
    ["Local", "Frequência", "A1: 25%", "A1: 50%", "A1: 95%", "C5: 25%", "C5: 50%", "C5: 95%"],
    [["Indianópolis", "Pulso único", "1,6", "3,0", "9,5", "0,6", "1,6", "8,9"],
     ["", "Dois pulsos", "2,1", "4,4", "17,3", "1,5", "4,3", "16,6"],
     ["", "Pulsos anuais", "6,7", "13,8", "58,0", "4,2", "11,5", "47,0"],
     ["", "Recuperação (meses)", "15", "23", "24", "20", "28", "38"],
     ["Telêmaco Borba", "Pulso único", "1,2", "3,3", "15,2", "0,3", "1,0", "9,5"],
     ["", "Dois pulsos", "0,5", "2,7", "25,6", "1,1", "3,3", "16,3"],
     ["", "Pulsos anuais", "1,8", "6,8", "67,8", "3,5", "7,4", "47,6"],
     ["", "Recuperação (meses)", "14", "24", "26", "21", "33", "44"],
     ["Imperatriz", "Pulso único", "2,8*", "6,2*", "31,7*", "0,8", "2,3", "11,3"],
     ["", "Dois pulsos", "6,0*", "14,6*", "60,5*", "2,0", "5,5", "25,4"],
     ["", "Pulsos anuais", "16,4*", "37,5*", "84,1*", "5,5", "16,3", "60,4"],
     ["", "Recuperação (meses)", "23*", "28*", "47*", "15", "26", "38"]],
    [1.6, 1.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9], "Pulso único: janeiro de 2017 (24 meses de idade); dois pulsos: janeiro de 2017 e 2020; pulsos anuais: janeiro de 2017 a 2022. Recuperação: meses até W~F~ ≥ 95% do controle após pulso único. Fertilidade F100. *Diagnóstico de extrapolação térmica. Fonte: o autor (2026)."),
  materialclima: () => tabela("Perda relativa de volume (%) aos 84 meses com desfolha de 50% em pulso único: média e amplitude entre os 16 cenários de água e fertilidade, por local e material",
    ["Local", "A1", "C5", "C2", "C4"],
    [["Indianópolis", "3,1 (2,9–3,3)", "2,3 (1,7–3,3)", "3,1 (2,3–4,2)", "2,3 (1,6–3,3)"],
     ["Telêmaco Borba", "3,0 (2,3–3,4)", "1,9 (1,1–3,3)", "2,5 (1,6–3,6)", "1,7 (1,0–3,2)"],
     ["Imperatriz", "6,2 (5,5–6,8)*", "3,1 (2,4–4,1)", "3,9 (3,0–5,0)", "3,2 (2,4–4,2)"]],
    [2, 1.5, 1.5, 1.5, 1.5], "*Diagnóstico de extrapolação térmica (temperatura média acima da T~máx~ do clone). Fonte: o autor (2026)."),
  rf: () => tabela("Desempenho do metamodelo Random Forest em três esquemas de validação cruzada (média entre os folds)",
    ["Resposta", "Esquema", "Folds", "R²", "r~yŷ~", "RQEM (%)"],
    [["Perda de volume (84 meses)", "*k*-fold 7 × 10 repetições", "70", "0,996 ± 0,001", "0,998", "7,7 ± 1,2"],
     ["", "Um local fora", "3", "0,907 ± 0,043", "0,979", "37,6 ± 6,9"],
     ["", "Um material fora", "4", "0,970 ± 0,039", "0,994", "19,7 ± 13,6"],
     ["Recuperação foliar (meses)", "*k*-fold 7 × 10 repetições", "70", "0,991 ± 0,003", "0,996", "3,2 ± 0,4"],
     ["", "Um local fora", "3", "0,880 ± 0,074", "0,964", "11,6 ± 3,6"],
     ["", "Um material fora", "4", "−1,149 ± 4,228", "0,965", "20,6 ± 29,5"]],
    [2.4, 2.2, 0.8, 1.5, 1, 1.4], "± desvio-padrão entre os folds. n = 1.848 (perda de volume) e 1.519 (recuperação), nos três locais, excluído o diagnóstico do clone A1 em Imperatriz. Fonte: o autor (2026)."),
  bertulio: () => tabela("Perdas observadas por Bertulio et al. (2008) aos 26 meses e perdas simuladas para o mesmo protocolo em Campo Verde-MT",
    ["Material simulado → observado", "Variável", "L observada (%)", "L simulada, d = 0,95 (%)", "L simulada, d = 0,999 (%)"],
    [["C5 → urograndis", "Volume", "52,9", "36,8", "64,8"],
     ["", "Circunferência/DAP", "24,2", "13,7", "28,5"],
     ["", "Altura", "19,1", "17,1", "34,7"],
     ["A1 → urocam", "Volume", "59,0", "60,6", "79,3"],
     ["", "Circunferência/DAP", "22,9", "26,5", "40,7"]],
    [2.6, 2, 1.5, 1.8, 1.8], "L observada: perda ajustada pela linha de base (14 meses). A1 é *E. urophylla* puro e urocam é *E. urophylla* × *E. camaldulensis*: transferência fraca. Fonte: o autor (2026), com dados de Bertulio et al. (2008)."),
  danos: () => tabela("Perda relativa de volume (%) aos 84 meses para danos de pragas e doenças representados por remoção de folhas, perda de eficiência fotossintética (r) e morte de árvores (m), com solo local",
    ["Praga ou doença", "Cenário", "IND A1", "TB A1", "IND C5", "TB C5", "IMP C5"],
    [["Lagartas", "Desfolha 50%, 1 mês", "3,0", "3,3", "1,6", "1,0", "2,3"],
     ["Psilídeo-de-concha", "Desfolha 25%, 1 mês", "1,6", "1,2", "0,7", "0,4", "0,9"],
     ["Formigas-cortadeiras", "Desfolha 95%, 18 meses", "9,9", "14,6", "6,2", "4,0", "6,0"],
     ["Mancha foliar*", "Desfolha 20%/mês, 3 meses", "3,0", "3,0", "1,5", "0,9", "2,2"],
     ["Percevejo-bronzeado*", "r = 0,20, 4 meses", "0,4", "1,3", "0,2", "1,0", "0,2"],
     ["Percevejo-bronzeado*", "r = 0,40, 4 meses", "0,7", "2,6", "0,4", "2,1", "0,3"],
     ["Murchas, cancros, seca de ponteiros", "m = 0,05, 24 meses", "1,1", "1,0", "0,6", "0,8", "0,5"],
     ["Murchas, cancros, seca de ponteiros", "m = 0,15, 24 meses", "3,4", "3,1", "1,9", "2,3", "1,4"],
     ["Ferrugem", "r calibrado, −25% DAP aos 12 meses", "—", "—", "2,9", "3,1", "1,3"],
     ["Ferrugem", "r calibrado, −35% DAP aos 12 meses", "—", "—", "3,8", "4,0", "2,0"]],
    [3.2, 3.4, 1.1, 1.1, 1.1, 1.1, 1.1], "* Cenário exploratório: sem magnitude de campo publicada. Ferrugem só para C5, iniciado aos 3 meses (r de 0,63 a 0,92). Idades dos eventos contadas a partir do plantio. Fonte: o autor (2026), com magnitudes de Wilcken et al. (2003), Zanetti et al. (2014), Santos, Auer e Grigoletti Júnior (2001) e Silveira e Higashi (2003)."),
  calibracao: () => tabela("Perdas observadas por Bertulio et al. (2008) aos 26 meses e perdas simuladas pelo módulo original e pelo módulo com compensação calibrada",
    ["Clone (material simulado)", "Uso", "Variável", "Observado (%)", "Original (%)", "Calibrado (%)"],
    [["Urograndis (C5)", "Ajuste", "Volume", "52,9", "64,8", "50,4"],
     ["Urograndis (C5)", "Ajuste", "Circunferência", "24,2", "28,5", "20,2"],
     ["Urograndis (C5)", "Ajuste", "Altura", "19,1", "34,7", "24,9"],
     ["Urocam (A1)", "Teste", "Volume", "59,0", "79,3", "64,8 (53,7 a 78,6)"],
     ["Urocam (A1)", "Teste", "Circunferência", "22,9", "40,7", "29,7 (22,5 a 40,0)"]],
    [3.2, 1.8, 2.4, 1.8, 1.8, 2.8], "Perdas ajustadas pela linha de base; desfolha total representada por d = 0,999. Calibrado: média da distribuição preditiva (ajuste) ou de 200 amostras da distribuição a posteriori (teste), com intervalo de 90% entre parênteses. O teste usa outro clone do mesmo experimento e não é validação independente. Altura não comparada no urocam, pois o A1 não tem relação hipsométrica própria. Fonte: o autor (2026), com dados observados de Bertulio et al. (2008)."),
  possibilidades: () => tabela("Possibilidades do módulo nos 5.688 cenários aptos de danos combinados: ganhos, perdas e recuperação aos 84 meses, nas versões original e calibrada",
    ["Indicador", "Original", "Calibrada"],
    [["Cenários com ganho de volume (%)", "1,9", "3,1"],
     ["Maior ganho de volume (%)", "3,5", "5,0"],
     ["Cenários com ganho: só desfolha (%)", "4,9", "19,4"],
     ["Cenários com ganho: só perda de eficiência (%)", "0,0", "0,0"],
     ["Cenários com ganho: só mortalidade (%)", "11,1", "11,1"],
     ["Perda de volume: mediana (%)", "11,1", "7,4"],
     ["Perda de volume: máxima (%)", "82,8", "63,6"],
     ["Folhagem atinge 95% do controle até 84 meses (% dos cenários com desfolha)", "41,1", "88,8"],
     ["Meses até 95% da folhagem do controle (mediana)", "32", "8"],
     ["NPP após o 1º ano maior que a do controle (% dos cenários com desfolha)", "7,7", "42,3"]],
    [9.5, 2.5, 2.5], "Ganho: volume do povoamento aos 84 meses maior que o do controle. Exclui o clone A1 em Imperatriz, Almeirim e Araripina (diagnóstico). Sem desfolha, as duas versões coincidem. Fonte: o autor (2026)."),
  validacaocruzada: () => tabela("Validação cruzada da compensação com as cinco observações de Bertulio et al. (2008): erro da perda prevista para as observações deixadas fora do ajuste",
    ["Esquema", "n", "RQEM original (p.p.)", "RQEM calibrado (p.p.)", "Viés original (p.p.)", "Viés calibrado (p.p.)", "Melhoraram"],
    [["Deixa uma observação de fora (k = 5)", "5", "15,1", "4,2", "14,0", "0,6", "5 de 5"],
     ["Ajusta no urograndis, prevê o urocam (k = 2)", "2", "19,1", "6,4", "19,0", "6,3", "2 de 2"],
     ["Ajusta no urocam, prevê o urograndis (k = 2)", "3", "11,7", "4,3", "10,7", "0,1", "3 de 3"]],
    [4.4, 0.6, 1.8, 1.8, 1.8, 1.8, 2.3], "Observações: perdas de volume, circunferência e altura do urograndis (C5) e de volume e circunferência do urocam (A1), aos 26 meses, d = 0,999. Previsão: média preditiva da distribuição a posteriori recalculada sem a observação ou sem o clone. As observações são do mesmo experimento: validação cruzada interna, não independente. Fonte: o autor (2026)."),
  biomas: () => tabela("Produtividade sem desfolha e perda de volume aos 84 meses com 50% de desfolha no material C5, um local por bioma, nas versões original e calibrada do módulo",
    ["Bioma (local)", "IMA (m³ ha⁻¹ ano⁻¹)", "Pulso único: orig.", "Pulso único: calib.", "Anual: orig.", "Anual: calib.", "Anual: IC 90%", "Recup.: orig.", "Recup.: calib."],
    [["Cerrado (Indianópolis)", "51", "1,6", "0,7", "11,5", "4,6", "−3,4 a 9,6", "28", "12"],
     ["Cerrado (Imperatriz)", "45", "2,3", "1,5", "16,3", "6,5", "1,0 a 10,8", "26", "14"],
     ["Mata Atlântica (Telêmaco Borba)", "60", "1,0", "0,6", "7,4", "1,2", "−7,2 a 8,2", "33", "11"],
     ["Amazônia (Almeirim)", "70", "0,7", "0,4", "6,5", "1,4", "−5,6 a 4,9", "29", "13"],
     ["Caatinga (Araripina)", "20", "−2,5", "−0,4", "3,2", "1,4", "−5,2 a 8,2", "4", "2"],
     ["Pampa (Eldorado do Sul)", "56", "1,1", "0,4", "6,4", "2,2", "−9,0 a 9,5", "34", "11"]],
    [3.4, 1.5, 1.3, 1.3, 1.3, 1.3, 1.9, 1.2, 1.2], "Perdas em %; valores negativos indicam ganho em relação ao controle. Solo local e fertilidade de referência. Calibrado: medianas a posteriori de U e a, com γ = 0,5; IC 90%: 200 amostras da distribuição a posteriori. Recup.: meses até a biomassa foliar atingir 95% do controle após o pulso único. Fonte: o autor (2026).")
};

// ---------- corpo ----------
const corpo = [];
for (const b of C.corpo) {
  if (b.h1) { SUM.push([b.h1, 1]); corpo.push(P(b.h1, { align: AlignmentType.LEFT, indent: false, run: { bold: true }, before: corpo.length > 0 ? 360 : 0, after: 240, keepNext: true })); }
  else if (b.h2) { SUM.push([b.h2, 2]); corpo.push(P(b.h2, { align: AlignmentType.LEFT, indent: false, run: { bold: true }, before: 240, after: 240, keepNext: true })); }
  else if (b.p) corpo.push(P(b.p));
  else if (b.li) corpo.push(P("– " + b.li, { indent: 851 }));
  else if (b.eq) corpo.push(eq(b.eq, b.n));
  else if (b.table) corpo.push(...TABS[b.table]());
  else if (b.fig) corpo.push(...figura(b.fig, b.w, b.cap));
}
SUM.push(["5 CONCLUSÃO", 1]);
corpo.push(P("5 CONCLUSÃO", { align: AlignmentType.LEFT, indent: false, run: { bold: true }, before: 360, after: 240, keepNext: true }));
C.conclusao.forEach(t => corpo.push(P(t)));
SUM.push(["REFERÊNCIAS", 0]);
corpo.push(P("REFERÊNCIAS", { align: AlignmentType.CENTER, indent: false, sp: L10, run: { bold: true }, before: 480, after: 240, keepNext: true }));
C.referencias.forEach(r => corpo.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { ...L10, after: 240 }, children: runs(r) })));
SUM.push(["APÊNDICE A – PLATAFORMA AKADEMIA FLORESTAL", 0]);
corpo.push(P("APÊNDICE A – PLATAFORMA AKADEMIA FLORESTAL", { align: AlignmentType.CENTER, indent: false, sp: L10, run: { bold: true }, before: 480, after: 240, keepNext: true }));
corpo.push(P("Acesso: https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc, ou o arquivo simulador_3pg_eucalyptus.html do pacote de reprodutibilidade (Apêndice B), aberto em qualquer navegador. Não é preciso instalar programas; a internet é necessária só para carregar as fontes e a biblioteca 3D. O tutorial abre na primeira visita e segue o roteiro abaixo.", { sp: L10, after: 160, align: AlignmentType.LEFT }));
corpo.push(...tabela("Roteiro do tutorial guiado da plataforma Akademia Florestal",
  ["Passo", "Conteúdo e ação na plataforma"],
  [["1. Objetivo", "Apresenta o problema e os talhões controle e desfolhado"],
   ["2. Conceitos", "Apresenta a biblioteca de conceitos e o modo explicar"],
   ["3. Painel de fisiologia", "Mostra as entradas do talhão e os parâmetros de cada material"],
   ["4. Módulo de desfolha", "Aplica 50% em jan/2017 e explica W~F,pós~ = W~F,pré~ · (1 − d)"],
   ["5. Simular", "Anima a rotação: a folhagem se recupera, o lenho não"],
   ["6. Partição e estresse", "Explica η~R~ e o modificador φ no painel de métricas"],
   ["7. Água e eficiência", "Apresenta a transpiração, a WUE e a eficiência quântica efetiva"],
   ["8. Frequência, época e clima", "Compara pulsos anuais, épocas e locais"],
   ["9. Compensação calibrada", "Liga a fisiologia calibrada e mostra a faixa de 90% no gráfico de volume"],
   ["10. Outros danos e domínio", "Escolhe um agente do catálogo e lê o quadro de domínio de validade"],
   ["11. Validação e métricas", "Abre o painel com verificação, calibração, evidência contrária e precedentes"],
   ["12. Cubagem e toras", "Abre a cubagem (Smalian, Huber e Newton) e o taper seccional com as toras"],
   ["13. Exportar e ajustar", "Mostra a exportação da série mensal e os ajustes de exibição"]],
  [2.2, 5]));
corpo.push(...figura("/home/claude/tcc/plataforma/fig_akademia_tutorial.png", 10.5, "Primeiro passo do tutorial guiado da plataforma Akademia Florestal."));
corpo.push(...figura("/home/claude/tcc/plataforma/fig_akademia_toras.png", 12, "Taper seccional e toras na plataforma Akademia Florestal: fuste médio do talhão desfolhado (clone A1, Indianópolis-MG, dois pulsos de 95%, fisiologia calibrada) dividido em toras de serraria, celulose e energia pelos critérios de Soares et al. (2003), com afilamento de Souza et al. (2016)."));


SUM.push(["APÊNDICE B – REPRODUTIBILIDADE COMPUTACIONAL", 0]);
corpo.push(P("APÊNDICE B – REPRODUTIBILIDADE COMPUTACIONAL", { align: AlignmentType.CENTER, indent: false, sp: L10, run: { bold: true }, before: 480, after: 240, keepNext: true }));
[
  "Os códigos, dados de entrada e saídas deste trabalho estão organizados em um pacote de arquivos que acompanha a versão digital do TCC. O mesmo conteúdo, com a explicação de cada arquivo, está disponível em https://drive.google.com/drive/folders/1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L. Todo o projeto é mantido sob controle de versões (Git), em repositório privado cujo acesso pode ser concedido à banca, e cada etapa do trabalho corresponde a um registro datado no histórico. Um roteiro automatizado executa, em ordem, os testes, a calibração, os experimentos, as análises, a auditoria numérica, a geração deste texto e a montagem da plataforma.",
  "Duas auditorias acompanham o texto. A auditoria numérica recalcula, a partir das saídas dos códigos, os números citados no TCC e falha se algum deles divergir. A auditoria científica classificou 32 afirmações centrais do trabalho segundo o tipo de evidência que as sustenta, avaliou os mecanismos da compensação, a robustez da calibração e a concordância com a literatura, e as correções resultantes foram incorporadas ao texto; seus relatórios, matrizes e o protocolo da busca bibliográfica do Apêndice C fazem parte do pacote. A tabela a seguir descreve os componentes necessários para reproduzir os resultados.",
].forEach(t => corpo.push(P(t, { sp: L10, after: 240 })));
corpo.push(...tabela("Componentes do pacote de reprodutibilidade",
  ["Arquivo", "Conteúdo"],
  [["modelo/threepg_pjs.py", "Tradução do núcleo 3-PGpjs do r3PG v0.1.7, módulo de desfolha e extensões de perda de eficiência e mortalidade"],
   ["modelo/testes/", "49 testes automatizados do módulo (28 da desfolha, 8 das extensões de dano e 13 da compensação)"],
   ["solos_fontes/", "Dados do SoilGrids, função PTF-ZARC e documentação do solo de cada local"],
   ["experimentos/clones.py", "Parâmetros dos materiais, com a origem de cada valor"],
   ["experimentos/clima.py", "Agregação mensal das séries NASA POWER"],
   ["experimentos/run_experimentos.py", "Matriz de 2.408 tratamentos e execução"],
   ["experimentos/r_check/", "Execução dos controles no r3PG original (R) e comparação"],
   ["experimentos/indicadores.py", "Perdas, recuperação, NPP acumulada e água"],
   ["experimentos/analise.py", "Decomposição fatorial, método de Morris nos três locais e figuras"],
   ["experimentos/estatisticas.py", "Estatísticas de verificação, confronto e Random Forest"],
   ["experimentos/validacao_kfold.py", "Metamodelos e validação cruzada"],
   ["experimentos/adversarial_e_literatura.py", "Auditoria adversarial e confronto com Bertulio et al. (2008)"],
   ["experimentos/danos_v2.py", "Catálogo de danos de pragas e doenças e calibração da ferrugem"],
   ["calibracao/", "Protocolo de Bertulio et al. (2008), calibração bayesiana da compensação e validação com E. globulus"],
   ["biomas/", "Bioma por município (IBGE, 2024), textura do SoilGrids por WCS e PTF-ZARC dos novos locais"],
   ["experimentos/run_biomas.py", "Bloco por bioma (seis locais, versões original e calibrada) e propagação da incerteza"],
   ["experimentos/rf_biomas.py", "Random Forest com seis locais e validação deixando um local de fora"],
   ["experimentos/possibilidades.py e possibilidades_analise.py", "Fatorial de danos combinados (7.584 cenários), aditividade, teste da plataforma e k-fold do metamodelo"],
   ["calibracao/validacao_cruzada.py", "Validação cruzada da calibração com as observações de Bertulio et al. (2008)"],
   ["experimentos/morris_danos_biomas.py", "Método de Morris e catálogo de danos nos seis locais"],
   ["experimentos/testes/", "8 testes automatizados do pipeline experimental"],
   ["auditoria_final/auditar_numeros.py", "Recálculo dos números citados no texto a partir das saídas"],
   ["plataforma/", "Akademia Florestal: modelo em JavaScript, dados incorporados, biblioteca de conceitos, cubagem e toras e página da plataforma"],
   ["plataforma/verificacao/", "Comparação da plataforma (JavaScript) com a implementação em Python e recálculo dos números da plataforma citados no texto"],
   ["revisao_07/", "Auditoria científica: matriz de afirmações, mecanismos e concordância, fichas de leitura, busca bibliográfica, corpus e indicadores"],
   ["ferramentas/", "Roteiro automatizado de execução e registro das etapas"]],
  [3.2, 5]));
SUM.push(["APÊNDICE C – BUSCA BIBLIOGRÁFICA E PRECEDENTES", 0]);
corpo.push(P("APÊNDICE C – BUSCA BIBLIOGRÁFICA E PRECEDENTES", { align: AlignmentType.CENTER, indent: false, sp: L10, run: { bold: true }, before: 480, after: 240, keepNext: true }));
corpo.push(P("A busca foi feita em 31 de outubro de 2026 na API do Crossref, com 20 consultas em inglês e português que combinaram descritores de desfolha, eucalipto, fisiologia, modelos processuais, ambiente e avaliação de modelos, de 1997 a 31 de outubro de 2026, com os 500 registros mais relevantes de cada uma. Como o Crossref não aceita operadores booleanos, as expressões booleanas do protocolo foram aplicadas depois, sobre título, resumo e assuntos. Dos 10.000 registros, restaram 7.908 com DOI único e 7.431 após a remoção de títulos repetidos; 93 atenderam à expressão do núcleo (desfolha e eucalipto, ou desfolha e modelo processual de árvores) e 20 formaram o subconjunto de contexto sobre o 3-PG. O OpenAlex e o SciELO não puderam ser consultados nessa data (limite diário de acesso esgotado e acesso bloqueado), e Scopus e Web of Science não estavam disponíveis. O protocolo, as expressões, o corpus em CSV e BibTeX e os indicadores estão no relatório cienciométrico do pacote de reprodutibilidade."));
corpo.push(...tabela("Trabalhos que representam desfolha ou doenças foliares em modelos processuais de crescimento florestal, identificados na busca",
  ["Trabalho", "Modelo", "Espécie e local", "Relação com este TCC"],
  [["Pinkard et al. (2011)", "Revisão; CABALA, CenW e outros", "Florestas australianas", "Regra de compensação adaptada na seção 3.12"],
   ["Pinkard et al. (2014)", "Modelo processual", "E. globulus, Austrália, clima atual e futuro", "Desfolha por Mycosphaerella e estoques de carbono"],
   ["Rua et al. (2020)", "3PG.d (3-PG com módulo de desfolha)", "E. globulus, Portugal", "Precedente direto de desfolha no 3-PG"]],
  [3, 3.4, 3.4, 4.4], "Fonte: o autor (2026). A lista completa, com outros modelos e espécies, está no relatório cienciométrico."));
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
  P("Monte Carmelo, __ de dezembro de 2026.", { align: AlignmentType.RIGHT, indent: false, sp: L10 }), ...vazio(1, L10),
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
