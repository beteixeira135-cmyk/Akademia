// Trabalho completo da IC no formato do VII MENSUFLOR (molde: artigo M135, mogno-africano).
// Arial 12, A4, margens 1,9 cm, entrelinha 1,5, títulos PT/EN em negrito centralizados.
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell, WidthType, BorderStyle,
  ImageRun, Header, Footer, PageNumber, LineRuleType, VerticalAlign } = require("docx");
const FIG = "/home/claude/tcc/experimentos/saida/figuras/";
const F = "Arial";
const L15 = { line: 360, lineRule: LineRuleType.AUTO }, L10 = { line: 240, lineRule: LineRuleType.AUTO };
const LARG = 11906 - 1080 - 1080;

function runs(txt, base = {}) {
  const out = []; let i = 0, b = false, it = false, sup = false, sub = false, buf = "";
  const flush = () => { if (buf) out.push(new TextRun({ text: buf, font: F, bold: b || base.bold, italics: it || base.italics,
    superScript: sup, subScript: sub, size: base.size || 24, color: base.color })); buf = ""; };
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
const P = (t, o = {}) => new Paragraph({ alignment: o.align ?? AlignmentType.JUSTIFIED, spacing: { ...(o.sp ?? L15), before: o.before ?? 0, after: o.after ?? 0 },
  indent: o.indent === false ? undefined : { firstLine: o.indent ?? 851 }, keepNext: o.keepNext, children: runs(t, o.run || {}) });
const H = (t) => P(t, { align: AlignmentType.LEFT, indent: false, run: { bold: true }, before: 240, after: 0, keepNext: true });
const C = (t, o = {}) => P(t, { align: AlignmentType.CENTER, indent: false, sp: L10, ...o });
const EQ = (t) => P(t, { align: AlignmentType.CENTER, indent: false, before: 60, after: 60 });

// ---------- tabela com três traços ----------
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, LN = { style: BorderStyle.SINGLE, size: 8, color: "000000" };
function tabela(titulo, cab, linhas, larg, nota) {
  const tot = larg.reduce((a, b) => a + b, 0), w = larg.map(x => Math.round(x / tot * LARG)); w[w.length - 1] += LARG - w.reduce((a, b) => a + b, 0);
  const cel = (t, j, o = {}) => new TableCell({ width: { size: w[j], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 30, bottom: 30, left: 60, right: 60 }, borders: { left: NB, right: NB, top: o.top ? LN : NB, bottom: o.bot ? LN : NB },
    children: [new Paragraph({ keepNext: true, alignment: j === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, spacing: L10, children: runs(String(t), { size: 20, bold: o.bold }) })] });
  const rows = [new TableRow({ tableHeader: true, children: cab.map((t, j) => cel(t, j, { top: true, bot: true, bold: true })) }),
    ...linhas.map((l, k) => new TableRow({ cantSplit: true, children: l.map((t, j) => cel(t, j, { bot: k === linhas.length - 1 })) }))];
  return [P(titulo, { indent: false, sp: L10, before: 120, after: 120, keepNext: true }),
    new Table({ width: { size: LARG, type: WidthType.DXA }, columnWidths: w, borders: { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB }, rows }),
    P(nota, { indent: false, sp: L10, before: 60, after: 120, run: { size: 18 } })];
}
function pngSize(f) { const b = fs.readFileSync(f); return [b.readUInt32BE(16), b.readUInt32BE(20)]; }
function figura(arq, wcm, cap) {
  const [pw, ph] = pngSize(arq); const w = Math.round(wcm * 37.795), h = Math.round(w * ph / pw);
  return [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { ...L10, before: 120 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(arq), transformation: { width: w, height: h } })] }),
    P(cap, { indent: false, sp: L10, before: 60, after: 120 })];
}

// ---------- texto ----------
const titulo = "Intensidade, frequência e época da desfolha alteram o crescimento simulado de eucalipto em três climas brasileiros?";
const titleEN = "Do defoliation intensity, frequency and timing change simulated eucalyptus growth across three Brazilian climates?";
const autores = "Bernardo Teixeira de Castro^1^; Gabriela Cristina Costa Silva^2^; Álvaro Augusto Vieira Soares^3^";
const afil = [
  ["^1^Universidade Federal de Uberlândia (UFU), Monte Carmelo/MG", "beteixeira@ufu.br"],
  ["^2^[Instituição da coorientadora — preencher]", "[e-mail — preencher]"],
  ["^3^Universidade Federal de Uberlândia (UFU), Monte Carmelo/MG", "alvaro.soares@ufu.br"],
];
const resumo = "**Resumo:** Este trabalho avaliou, por simulação com o modelo ecofisiológico 3-PG, o efeito da intensidade, da frequência e da época da desfolha sobre o crescimento de eucalipto em Indianópolis-MG, Telêmaco Borba-PR e Imperatriz-MA. Um módulo de desfolha foi incorporado ao 3-PG, e quatro parametrizações publicadas foram simuladas com o clima e o solo de cada local, obtidos de fontes secundárias. Com pulso único, a perda de volume aos sete anos variou de 0,3 a 15,2%, conforme o local, o material e a intensidade (25 a 95%); com pulsos anuais, chegou a 68%. Um modelo Random Forest, avaliado por validação cruzada em sete *folds*, reproduziu as perdas simuladas (R² = 0,996; RQEM = 9,3%) e indicou que a intensidade (52%) e a frequência (45%) da desfolha governam a perda, enquanto local, material, época e fertilidade somaram menos de 4%. Os resultados mostram que a recorrência do ataque deve ser considerada no manejo de pragas desfolhadoras.";
const palavras = "**Palavras-chave:** Modelagem processual; 3-PG; Herbivoria; Random Forest.";
const abstract = "**Abstract:** This study evaluated, through simulation with the ecophysiological model 3-PG, the effect of defoliation intensity, frequency and timing on eucalyptus growth in Indianópolis-MG, Telêmaco Borba-PR and Imperatriz-MA, Brazil. A defoliation module was added to 3-PG, and four published parameterisations were simulated with the climate and soil of each site, obtained from secondary sources. With a single pulse, the stand volume loss at seven years ranged from 0.3 to 15.2%, depending on site, genetic material and intensity (25 to 95%); with annual pulses, it reached 68%. A Random Forest model, evaluated by seven-fold cross-validation, reproduced the simulated losses (R² = 0.996; RMSE = 9.3%) and showed that defoliation intensity (52%) and frequency (45%) govern the loss, whereas site, genetic material, timing and fertility together accounted for less than 4%. The results show that the recurrence of attacks must be considered in the management of defoliating pests.";
const keywords = "**Keywords:** Process-based modelling; 3-PG; Herbivory; Random Forest.";

const corpo = [
  H("INTRODUÇÃO"),
  P("Os plantios de eucalipto ocupam posição de destaque no setor florestal brasileiro e estão sujeitos ao ataque de insetos desfolhadores e a doenças foliares. A perda de folhas reduz a radiação interceptada pelo dossel e, consequentemente, a produção de madeira, mas a magnitude desse dano varia com a intensidade, a frequência e a época do ataque, com o material genético e com as condições de clima e solo (Pinkard et al., 2006; Matrangolo et al., 2010). Experimentos de campo que abranjam todas essas combinações são onerosos e demorados, e os poucos estudos brasileiros disponíveis aplicaram desfolha total em materiais e idades específicos (Bertulio et al., 2008; Matrangolo et al., 2010)."),
  P("Nesse contexto, os modelos ecofisiológicos surgem como ferramentas capazes de explorar muitos cenários a baixo custo. O 3-PG estima a produção primária a partir da radiação absorvida pelo dossel, modulada por temperatura, água no solo, déficit de pressão de vapor e idade, e distribui o carbono entre folhas, lenho e raízes (Landsberg; Waring, 1997). O modelo foi parametrizado para eucaliptos brasileiros (Borges, 2009; Caldeira et al., 2020) e está disponível no pacote r3PG (Trotsiuk et al., 2020), mas não representa a perda de folhas por pragas, lacuna já apontada por Pinkard et al. (2011). Além disso, a produtividade do eucalipto diminui com o aumento da temperatura e do déficit hídrico (Binkley et al., 2017), o que sugere que a resposta à desfolha também pode variar entre regiões. Diante do exposto, este trabalho tem como objetivo principal avaliar, por simulação com o modelo 3-PG, o efeito da intensidade, da frequência e da época da desfolha sobre o crescimento de eucalipto em três regiões climáticas brasileiras. Adicionalmente, busca-se investigar, por meio de um modelo Random Forest, a importância de cada fator na perda de volume."),
  H("MATERIAL E MÉTODOS"),
  P("As simulações foram realizadas para Indianópolis-MG (Cerrado, com estação seca de maio a setembro), Telêmaco Borba-PR (clima subtropical úmido, sem estação seca definida) e Imperatriz-MA (clima tropical quente, com estação seca de maio a setembro). As séries diárias de temperatura, precipitação e radiação de 2015 a 2024 foram obtidas do NASA POWER (NASA, 2026) e agregadas em valores mensais. A água disponível no solo até 2 m de profundidade foi de 215 mm em Indianópolis e de 214 mm em Telêmaco Borba, valores publicados para os sítios mais próximos da rede TECHS (Binkley et al., 2017), e de 210 mm em Imperatriz, estimada com a textura do SoilGrids (Poggio et al., 2021) e a função de pedotransferência do Zoneamento Agrícola de Risco Climático (Teixeira et al., 2021)."),
  P("Utilizou-se a versão 3-PGpjs do pacote r3PG (Trotsiuk et al., 2020), traduzida para Python, à qual se acrescentou um módulo de desfolha. Em cada evento, a biomassa foliar é reduzida no início do mês, antes do cálculo da interceptação de luz, conforme a equação 1, e o índice de área foliar é recalculado. Nenhuma equação original foi alterada, e a implementação reproduziu o r3PG original com coeficiente de determinação igual a 1,000 em todos os controles."),
  EQ("W~F,pós~ = W~F,pré~ · (1 − d)    [1]"),
  P("em que: *W*~F,pré~ e *W*~F,pós~ são a biomassa foliar antes e depois do evento (t ha^-1^) e *d* é a intensidade da desfolha (0 ≤ *d* < 1).", { indent: false }),
  P("Foram simulados quatro materiais genéticos: o clone A1 de *Eucalyptus urophylla* (Caldeira et al., 2020) e três parametrizações de híbridos *E. grandis* × *E. urophylla* para o Cerrado mineiro (C5, C2 e C4; Borges, 2009). Adotou-se plantio em janeiro de 2015, espaçamento de 3 × 3 m e rotação de sete anos. As intensidades de desfolha foram de 25, 50 e 95%, aplicadas em seis calendários: pulso único em janeiro de 2017 (24 meses de idade), dois pulsos (janeiro de 2017 e de 2020), pulsos anuais (janeiro de 2017 a 2022) e pulso único em abril, julho ou outubro de 2017, para avaliar a época. Cada tratamento foi comparado com um controle sem desfolha, e a perda relativa foi calculada pela equação 2. Em Imperatriz, o clone A1 foi tratado apenas como diagnóstico, pois a temperatura média mensal local supera a temperatura máxima de crescimento desse material (28,65 °C)."),
  EQ("L = 100 · (1 − Y~trat~ / Y~ctrl~)    [2]"),
  P("em que: *L* é a perda relativa (%) e *Y*~trat~ e *Y*~ctrl~ são o volume do tratamento e do controle aos 84 meses de idade.", { indent: false }),
  P("Para quantificar a importância de cada fator, a perda de volume foi modelada com o algoritmo Random Forest (Breiman, 2001), utilizando como variáveis de entrada a intensidade, o número de pulsos, o mês do pulso, o local, o material e o nível de fertilidade do solo. A implementação foi realizada com a biblioteca Scikit-learn (Pedregosa et al., 2011), em linguagem Python, com 400 árvores. As variáveis categóricas foram transformadas pelo OneHotEncoder. Realizou-se a validação cruzada do tipo K-*fold* (com k = 7), e foram calculados o coeficiente de determinação (R²), o coeficiente de correlação de Pearson entre os valores simulados e estimados (r~yŷ~) e a raiz quadrada do erro quadrático médio (RQEM), conforme as equações 3, 4 e 5. A importância das variáveis foi avaliada pelo método de *permutation importance*."),
  EQ("R² = 1 − Σ(y~i~ − ŷ~i~)² / Σ(y~i~ − ȳ)² [3];   r~yŷ~ = Σ(y~i~ − ȳ)(ŷ~i~ − ŷ̄) / √[Σ(y~i~ − ȳ)² Σ(ŷ~i~ − ŷ̄)²] [4];   RQEM = (100/ȳ) √[Σ(y~i~ − ŷ~i~)²/n] [5]"),
  P("em que: *y*~i~ e *ŷ*~i~ são as perdas simuladas pelo 3-PG e estimadas pela Random Forest, ȳ e ŷ̄ são suas respectivas médias e *n* é o número de observações.", { indent: false }),
  H("RESULTADOS E DISCUSSÃO"),
  P("Sem desfolha, o clone A1 produziu 429 m³ ha^-1^ aos 84 meses em Telêmaco Borba, 352 m³ ha^-1^ em Indianópolis e 227 m³ ha^-1^ em Imperatriz. Entre dois e três anos de idade, a produção de lenho simulada em Telêmaco Borba foi de 37 Mg ha^-1^ ano^-1^, próxima dos 34 Mg ha^-1^ ano^-1^ medidos para o mesmo clone e espaçamento no município (Binkley et al., 2017), e a ordem de produtividade entre os locais coincidiu com o gradiente climático observado por esses autores. Como esses dados também foram usados na calibração do clone, a comparação indica coerência das simulações, mas não constitui validação."),
  P("A perda de volume aumentou com a intensidade da desfolha em todos os locais e materiais (Tabela 1). Com pulso único, a desfolha de 25% causou perdas de até 1,6%, ao passo que a de 95% causou perdas de 8,8 a 15,2%, sem considerar o diagnóstico do clone A1 em Imperatriz. A desfolha intensa foi mais prejudicial em Telêmaco Borba do que em Indianópolis, porque, no clima sem estação seca, a menor transpiração do dossel desfolhado não resulta em economia de água aproveitável nos meses secos, mecanismo que atenuou as perdas em Indianópolis. Em Imperatriz, os materiais de Borges (2009) apresentaram perdas maiores que nos demais locais para a mesma intensidade. Após desfolha de 50%, a biomassa foliar do clone A1 levou de 23 a 24 meses para atingir 95% da biomassa do controle em Indianópolis e Telêmaco Borba."),
];
const tab1 = tabela("**Tabela 1:** Perda relativa de volume (%) aos 84 meses por local, material, frequência e intensidade da desfolha, para o clone A1 e a parametrização C5.",
  ["Local", "Frequência", "A1: 25%", "A1: 50%", "A1: 95%", "C5: 25%", "C5: 50%", "C5: 95%"],
  [["Indianópolis", "Pulso único", "1,6", "3,0", "9,5", "0,6", "1,6", "8,9"],
   ["", "Dois pulsos", "2,1", "4,4", "17,3", "1,5", "4,3", "16,6"],
   ["", "Pulsos anuais", "6,7", "13,8", "58,0", "4,2", "11,5", "47,0"],
   ["Telêmaco Borba", "Pulso único", "1,2", "3,3", "15,2", "0,3", "1,0", "9,5"],
   ["", "Dois pulsos", "0,5", "2,7", "25,6", "1,1", "3,3", "16,3"],
   ["", "Pulsos anuais", "1,8", "6,8", "67,8", "3,5", "7,4", "47,6"],
   ["Imperatriz", "Pulso único", "2,8*", "6,2*", "31,7*", "0,8", "2,3", "11,3"],
   ["", "Dois pulsos", "6,0*", "14,6*", "60,5*", "2,0", "5,5", "25,4"],
   ["", "Pulsos anuais", "16,4*", "37,5*", "84,1*", "5,5", "16,3", "60,4"]],
  [1.7, 1.5, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9], "*Diagnóstico de extrapolação térmica (temperatura média acima da temperatura máxima de crescimento do clone).");
const corpo2 = [
  P("A frequência foi o fator que mais ampliou as perdas (Figura 1). Com dois pulsos, a perda do clone A1 com 95% de desfolha chegou a 17,3% em Indianópolis e a 25,6% em Telêmaco Borba; com pulsos anuais, atingiu 58,0 e 67,8%, respectivamente, pois a biomassa foliar diminuiu a cada evento e não chegou a se recompor. Em alguns casos de desfolha leve, o segundo pulso resultou em perda ligeiramente menor que o pulso único, efeito atribuído à economia de água após o evento. A época teve efeito menor: nos materiais de Borges (2009), a perda com 50% de desfolha variou menos de 0,5 ponto percentual entre janeiro, abril, julho e outubro, enquanto no clone A1 variou de 1,7% (abril) a 3,7% (outubro) em Indianópolis e foi mínima em julho (1,9%) em Telêmaco Borba. A desfolha não aumentou a mortalidade em nenhum tratamento, pois o 3-PG só representa a mortalidade por autodesbaste; em povoamentos desfolhados, que crescem menos, ela foi igual ou menor que no controle."),
];
const fig1 = figura(FIG + "F3_frequencia_3sitios.png", 16.5, "**Figura 1:** Perda relativa de volume aos 84 meses por intensidade e frequência da desfolha nos três locais, para o clone A1 (linha cheia) e a parametrização C5 (linha tracejada). Em Imperatriz, o clone A1 é diagnóstico de extrapolação térmica.");
const corpo3 = [
  P("O modelo Random Forest apresentou R² de 0,996, r~yŷ~ de 0,998 e RQEM de 9,3% na validação cruzada, indicando que as perdas simuladas pelo 3-PG podem ser reproduzidas com elevada acurácia a partir dos fatores do delineamento. A análise de importância das variáveis evidenciou uma hierarquia clara (Tabela 2): a intensidade e o número de pulsos responderam juntos por 97% da importância, enquanto o local, o material, o mês do pulso e a fertilidade pouco contribuíram. Isso indica que, no modelo, a perda é determinada principalmente pelo próprio distúrbio, e o ambiente e o material modulam a sua magnitude."),
];
const tab2 = tabela("**Tabela 2:** Variáveis de entrada e sua importância relativa no modelo Random Forest para estimação da perda de volume aos 84 meses.",
  ["Variável", "Importância (%)"],
  [["Intensidade da desfolha", "52,16"], ["Número de pulsos (frequência)", "44,61"], ["Local (clima)", "1,67"],
   ["Material genético", "0,75"], ["Mês do pulso (época)", "0,56"], ["Fertilidade do solo", "0,24"]],
  [4, 2], "n = 792 tratamentos com desfolha (excluído o diagnóstico do clone A1 em Imperatriz).");
const corpo4 = [
  P("Esses resultados devem ser interpretados à luz das limitações do 3-PG. O modelo não representa as reservas de carboidratos, o aumento da fotossíntese das folhas remanescentes nem o aumento da transpiração por unidade de área foliar observado em árvores desfolhadas de *E. globulus* (Quentin et al., 2011), o que tende a superestimar a economia de água e a subestimar as perdas em locais com estação seca. Além disso, a ausência de mortalidade induzida impede avaliar o risco de morte de árvores sob desfolhas severas e recorrentes, e a inexistência de experimentos de desfolha nos três locais impede a validação dos resultados."),
  H("CONCLUSÃO"),
  P("A desfolha reduziu o volume simulado de eucalipto nos três locais, com perdas que cresceram com a intensidade e, sobretudo, com a frequência do ataque: com pulso único, as perdas variaram de 0,3 a 15,2%, e com pulsos anuais chegaram a 68%. A época do pulso, o material genético e o local alteraram a magnitude da resposta, mas tiveram importância secundária no modelo Random Forest, que reproduziu as simulações com elevada acurácia (R² = 0,996; RQEM = 9,3%). Os resultados indicam que o controle de pragas desfolhadoras deve priorizar a prevenção de ataques recorrentes. Sugere-se, em estudos futuros, incorporar ao módulo as reservas de carboidratos e a compensação fisiológica e realizar experimentos de desfolha nos locais simulados para validar as estimativas."),
  H("REFERÊNCIAS"),
];
const refs = [
  "BERTULIO, V. G. et al. Crescimento de clones de *Eucalyptus* spp. submetidos a desfolha artificial sucessiva. **Revista de Agricultura**, Piracicaba, p. 119-124, 2008.",
  "BINKLEY, D. et al. The interactions of climate, spacing and genetics on clonal *Eucalyptus* plantations across Brazil and Uruguay. **Forest Ecology and Management**, v. 405, p. 271-283, 2017. Disponível em: https://doi.org/10.1016/j.foreco.2017.09.050. Acesso em: 30 out. 2026.",
  "BORGES, J. S. **Parametrização, calibração e validação do modelo 3-PG para eucalipto na região do cerrado de Minas Gerais**. 2009. Dissertação (Mestrado em Solos e Nutrição de Plantas) – Universidade Federal de Viçosa, Viçosa, 2009.",
  "BREIMAN, L. Random forests. **Machine Learning**, v. 45, n. 1, p. 5-32, 2001.",
  "CALDEIRA, D. R. M. et al. Multisite evaluation of the 3-PG model for the highest phenotypic plasticity *Eucalyptus* clone in Brazil. **Forest Ecology and Management**, v. 462, 117989, 2020. Disponível em: https://doi.org/10.1016/j.foreco.2020.117989. Acesso em: 30 out. 2026.",
  "LANDSBERG, J. J.; WARING, R. H. A generalised model of forest productivity using simplified concepts of radiation-use efficiency, carbon balance and partitioning. **Forest Ecology and Management**, v. 95, p. 209-228, 1997.",
  "MATRANGOLO, C. A. R. et al. Crescimento de eucalipto sob efeito de desfolhamento artificial. **Pesquisa Agropecuária Brasileira**, Brasília, v. 45, n. 9, p. 952-957, 2010.",
  "NASA. **POWER**: Prediction of Worldwide Energy Resources. Hampton: NASA Langley Research Center, 2026. Disponível em: https://power.larc.nasa.gov/. Acesso em: 30 out. 2026.",
  "PEDREGOSA, F. et al. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825-2830, 2011.",
  "PINKARD, E. A. et al. Growth responses of *Eucalyptus globulus* Labill. to nitrogen application and severity, pattern and frequency of artificial defoliation. **Forest Ecology and Management**, v. 229, p. 378-387, 2006.",
  "PINKARD, E. A. et al. Estimating forest net primary production under changing climate: adding pests into the equation. **Tree Physiology**, v. 31, n. 7, p. 686-699, 2011.",
  "POGGIO, L. et al. SoilGrids 2.0: producing soil information for the globe with quantified spatial uncertainty. **SOIL**, v. 7, p. 217-240, 2021. Disponível em: https://doi.org/10.5194/soil-7-217-2021. Acesso em: 30 out. 2026.",
  "QUENTIN, A. G. et al. Responses of transpiration and canopy conductance to partial defoliation of *Eucalyptus globulus* trees. **Agricultural and Forest Meteorology**, v. 151, p. 356-364, 2011.",
  "TEIXEIRA, W. G. et al. **Predição da água disponível no solo em função da granulometria para uso nas análises de risco no Zoneamento Agrícola de Risco Climático**. Rio de Janeiro: Embrapa Solos, 2021. (Boletim de Pesquisa e Desenvolvimento, 272).",
  "TROTSIUK, V.; HARTIG, F.; FORRESTER, D. I. r3PG – An R package for simulating forest growth using the 3-PG process-based model. **Methods in Ecology and Evolution**, v. 11, n. 11, p. 1470-1475, 2020. Disponível em: https://doi.org/10.1111/2041-210X.13474. Acesso em: 30 out. 2026.",
].map(r => P(r, { align: AlignmentType.LEFT, indent: false, sp: L10, after: 200 }));

const cab = new Header({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: runs("[Cabeçalho do VIII MENSUFLOR — substituir pelo template oficial quando for divulgado]", { size: 18, color: "808080" }) })] });
const rod = new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: F, size: 20 })] })] });
const doc = new Document({
  creator: "Bernardo Teixeira de Castro", title: titulo,
  styles: { default: { document: { run: { font: F, size: 24 }, paragraph: { spacing: L15 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 2200, bottom: 1000, left: 1080, right: 1080, header: 500, footer: 500 } } },
    headers: { default: cab }, footers: { default: rod },
    children: [
      C(titulo, { run: { bold: true }, after: 160 }), C(titleEN, { run: { bold: true }, after: 240 }),
      C(autores, { after: 160 }),
      ...afil.flatMap(([a, e]) => [P(a, { align: AlignmentType.LEFT, indent: false, sp: L10, run: { size: 22 } }), P(e, { align: AlignmentType.LEFT, indent: false, sp: L10, run: { size: 22 }, after: 60 })]),
      P(resumo, { indent: false, sp: L10, before: 200 }), P(palavras, { indent: false, sp: L10, after: 240 }),
      P(abstract, { indent: false, sp: L10 }), P(keywords, { indent: false, sp: L10, after: 120 }),
      ...corpo, ...tab1, ...corpo2, ...fig1, ...corpo3, ...tab2, ...corpo4, ...refs,
    ],
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("/home/claude/tcc/mensuflor/MENSUFLOR_IC_desfolha_3PG.docx", b); console.log("ok"); });
