// ---------- Cubagem explicativa e taper seccional (toras e sortimentos) ----------
// Afilamento: polinômio de 5º grau de Schöepfer, d/DAP = Σ βi (h/Ht)^i, diâmetros com casca.
// Coeficientes de Souza et al. (2016, Scientia Forestalis 44(109):33-40), Tabela 2, tratamento T5 (3,0 × 3,0 m):
// clone E. grandis × E. camaldulensis, Itamarandiba-MG, 8 anos, 180 árvores cubadas por Smalian.
// Aqui a forma é EMPRESTADA para os materiais do simulador: serve para explicar, não está validada para eles.
const TAPER = { b: [1.16763760, -3.27135930, 14.22874988, -33.96062159, 35.94747372, -14.11411271],
  fonte: "Souza et al. (2016), clone E. grandis × E. camaldulensis, Itamarandiba-MG, 8 anos, espaçamento 3 × 3 m" };
// Sortimentos: Soares et al. (2003, Revista Árvore 27(6):811-820): diâmetro mínimo na ponta fina, com casca,
// e comprimentos ótimos de tora encontrados naquele estudo. São editáveis, porque cada empresa usa os seus.
const SORT_PAD = [
  { id: "serraria", nome: "Serraria", cor: "#7c3b26", dmin: 15, L: 2.0, uso: "tábuas, vigas, caibros e móveis" },
  { id: "celulose", nome: "Celulose", cor: "#a96c36", dmin: 8, L: 2.2, uso: "polpa para papel e papelão" },
  { id: "energia", nome: "Energia", cor: "#c19767", dmin: 4, L: 1.1, uso: "lenha e carvão" },
];
let SORT = SORT_PAD.map(s => ({ ...s })), TOCO = 0.1, CUB_TAL = "c", CUB_PASSO = 1;
const dTaper = (h, dap, H) => { if (h >= H) return 0; const r = h / H; let s = 0, p = 1; for (const b of TAPER.b) { s += b * p; p *= r; } return Math.max(0, dap * s); };
const gArea = d => Math.PI * d * d / 40000;              // área seccional (m²) com d em cm
function volExato(h1, h2, dap, H) {                      // integral de g(h) por Simpson (400 passos)
  const n = 400, dh = (h2 - h1) / n; let s = 0;
  for (let i = 0; i <= n; i++) { const w = i === 0 || i === n ? 1 : i % 2 ? 4 : 2; s += w * gArea(dTaper(h1 + i * dh, dap, H)); }
  return s * dh / 3;
}
function alturaDoDiametro(dmin, dap, H) {                 // altura onde o tronco afina até dmin (busca por bisseção)
  let a = 1.3, b = H; if (dTaper(a, dap, H) < dmin) return a;
  for (let i = 0; i < 50; i++) { const m = (a + b) / 2; dTaper(m, dap, H) >= dmin ? a = m : b = m; } return a;
}
function toras(dap, H) {                                  // corte da base para a ponta, priorizando o produto mais nobre
  const out = []; let h = TOCO;
  while (h < H) {
    let feito = false;
    for (const s of SORT) { if (!(s.L > 0)) continue; const hs = h + s.L;
      if (hs <= H && dTaper(hs, dap, H) >= s.dmin) { out.push({ s, h1: h, h2: hs, d1: dTaper(h, dap, H), d2: dTaper(hs, dap, H), v: volExato(h, hs, dap, H) }); h = hs; feito = true; break; } }
    if (!feito) break;
  }
  return { lista: out, hFim: h, ponta: volExato(h, H, dap, H), toco: volExato(0, TOCO, dap, H), total: volExato(0, H, dap, H) };
}
function arvoreDoTalhao(qual) { const o = qual === "t" ? R.t : R.c, k = R.k84; return { dap: o.dbh[k], H: R.alt(o, k), N: o.N[k], vol3pg: o.vol[k] }; }

// ---- desenho do fuste seccionado ----
function svgFuste(dap, H, tr, alvo) {
  const W = 340, Hs = 330, mx = 26, base = Hs - 22, esc = (base - 14) / H, larg = 70 / Math.max(dap, 10) * 0.9;
  const y = h => base - h * esc, x = d => d * larg / 2;
  const pts = Array.from({ length: 81 }, (_, i) => { const h = H * i / 80; return [x(dTaper(h, dap, H)), y(h)]; });
  const perfil = (dx) => pts.map(([w, yy], i) => (i ? "L" : "M") + (dx + w).toFixed(1) + " " + yy.toFixed(1)).join("") + pts.slice().reverse().map(([w, yy]) => "L" + (dx - w).toFixed(1) + " " + yy.toFixed(1)).join("") + "Z";
  const cx = 100, secs = tr.lista.map((t, i) => {
    const sub = Array.from({ length: 11 }, (_, j) => { const h = t.h1 + (t.h2 - t.h1) * j / 10; return [x(dTaper(h, dap, H)), y(h)]; });
    const d = sub.map(([w, yy], j) => (j ? "L" : "M") + (cx + w).toFixed(1) + " " + yy.toFixed(1)).join("") + sub.slice().reverse().map(([w, yy]) => "L" + (cx - w).toFixed(1) + " " + yy.toFixed(1)).join("") + "Z";
    return `<path d="${d}" fill="${t.s.cor}" stroke="var(--prancha)" stroke-width="1.2"><title>Tora ${i + 1}: ${t.s.nome}, ${fmt(t.h1, 1)}–${fmt(t.h2, 1)} m, ponta fina ${fmt(t.d2, 1)} cm</title></path>`; }).join("");
  const marcas = [0, 5, 10, 15, 20, 25, 30, 35].filter(h => h <= H).map(h => `<path d="M${mx} ${y(h)} h5" stroke="var(--tinta-3)"/><text x="${mx - 3}" y="${y(h) + 3}" text-anchor="end">${h}</text>`).join("");
  const leg = [...SORT, { nome: "Ponteira (resíduo)", cor: "var(--oliva-3)" }, { nome: "Toco", cor: "var(--tinta-3)" }].map((s, i) => `<rect x="196" y="${30 + i * 18}" width="12" height="12" fill="${s.cor}" stroke="var(--linha-2)"/><text x="213" y="${40 + i * 18}">${s.nome}${s.dmin ? ` (≥ ${fmt(s.dmin, 0)} cm)` : ""}</text>`).join("");
  const y13 = y(1.3);
  document.getElementById(alvo).innerHTML = `<svg viewBox="0 0 ${W} ${Hs}" width="100%" role="img" aria-label="Fuste dividido em toras"><g font-family="var(--f-sans)" font-size="10" fill="var(--tinta)">
    <path d="${perfil(cx)}" fill="var(--oliva-3)" stroke="var(--oliva)"/>${secs}
    <rect x="${cx - x(dTaper(0, dap, H))}" y="${y(TOCO)}" width="${2 * x(dTaper(0, dap, H))}" height="${Math.max(1.5, TOCO * esc)}" fill="var(--tinta-3)"/>
    <path d="M${cx - 45} ${base} H${cx + 45}" stroke="var(--terra)" stroke-width="1.5"/>
    <path d="M${mx + 5} 14 V${base}" stroke="var(--linha-2)"/>${marcas}<text x="${mx - 20}" y="9">altura (m)</text>
    <path d="M${cx + x(dap) + 2} ${y13} h28" stroke="var(--alerta)"/><text x="${cx + x(dap) + 32}" y="${y13 + 3}" fill="var(--alerta)">DAP ${fmt(dap, 1)} cm</text>
    <text x="196" y="18" font-weight="600">Destino de cada tora</text>${leg}
    <text x="196" y="138" fill="var(--tinta-2)">largura exagerada</text><text x="196" y="151" fill="var(--tinta-2)">${fmt(100 * larg / esc, 0)}× para caber na tela</text></g></svg>`;
}

// ---- aba 1: cubagem ----
function posicoesCubagem(H) {
  if (CUB_PASSO === 0) { const p = [0.1, 0.3, 0.7, 1.0, 1.3, 2.0]; for (let h = 3; h < H; h++) p.push(h); return p; }
  const p = [0.1, 1.3]; for (let h = 2; h < H; h += CUB_PASSO) p.push(h); return p.filter((v, i, a) => a.indexOf(v) === i).sort((a, b) => a - b);
}
function montarCubagem() {
  const a = arvoreDoTalhao(CUB_TAL), { dap, H } = a, pos = posicoesCubagem(H), hTopo = alturaDoDiametro(2, dap, H);
  const med = pos.filter(h => h <= hTopo).map(h => ({ h, d: dTaper(h, dap, H) }));
  let vS = 0, vH = 0, vN = 0, linhas = "";
  for (let i = 0; i < med.length - 1; i++) {
    const A = med[i], B = med[i + 1], L = B.h - A.h, dm = dTaper((A.h + B.h) / 2, dap, H);
    const s = (gArea(A.d) + gArea(B.d)) / 2 * L, hu = gArea(dm) * L, nw = (gArea(A.d) + 4 * gArea(dm) + gArea(B.d)) / 6 * L;
    vS += s; vH += hu; vN += nw;
    if (i < 8 || i === med.length - 2) linhas += `<tr><td class="num">${fmt(A.h, 1)}–${fmt(B.h, 1)}</td><td class="num">${fmt(A.d, 1)}</td><td class="num">${fmt(B.d, 1)}</td><td class="num">${fmt(s * 1000, 2)}</td></tr>`;
    else if (i === 8) linhas += `<tr><td colspan="4" class="mini">… (seções intermediárias omitidas na tabela, mas incluídas na soma)</td></tr>`;
  }
  const ult = med[med.length - 1], cone = gArea(ult.d) * (H - ult.h) / 3, ex = volExato(0, H, dap, H), toco = volExato(0, med[0].h, dap, H);
  const tot = v => v + cone + toco, err = v => 100 * (tot(v) / ex - 1), f = ex / (gArea(dap) * H);
  document.getElementById("cub-arvore").innerHTML = `Árvore média do talhão <b>${CUB_TAL === "c" ? "referência 3-PG" : "simulação atual"}</b> aos 84 meses (${SIT[E.sitio]}, ${E.mat}): DAP = <b class="num">${fmt(dap, 1)} cm</b>, altura total = <b class="num">${fmt(H, 1)} m</b>.`;
  document.getElementById("cub-tab").innerHTML = `<thead><tr><th>Seção (m)</th><th>d base (cm)</th><th>d topo (cm)</th><th>V Smalian (dm³)</th></tr></thead><tbody>${linhas}</tbody>`;
  document.getElementById("cub-res").innerHTML = `<table class="tab"><thead><tr><th>Método</th><th>Volume da árvore (m³)</th><th>Erro vs. volume exato</th></tr></thead><tbody>
    <tr><td>Smalian (média das pontas)</td><td class="num">${fmt(tot(vS), 4)}</td><td class="num">${fmt(err(vS), 2)}%</td></tr>
    <tr><td>Huber (meio da seção)</td><td class="num">${fmt(tot(vH), 4)}</td><td class="num">${fmt(err(vH), 2)}%</td></tr>
    <tr><td>Newton (pontas + meio)</td><td class="num">${fmt(tot(vN), 4)}</td><td class="num">${fmt(err(vN), 2)}%</td></tr>
    <tr><td><b>Exato</b> (integral da curva)</td><td class="num"><b>${fmt(ex, 4)}</b></td><td>–</td></tr></tbody></table>
    <p class="mini">Inclui o toco (0 a ${fmt(med[0].h, 1)} m) e a ponta acima do último diâmetro medido (${fmt(ult.h, 1)} m), tratada como cone. Fator de forma f = V / (g · H) = <b class="num">${fmt(f, 3)}</b>: o tronco tem ${fmt(100 * f, 0)}% do volume de um cilindro com o mesmo DAP e altura.</p>`;
}

// ---- aba 2: toras ----
function montarToras() {
  const linhaS = SORT.map((s, i) => `<tr><td><i class="cub-cor" style="background:${s.cor}"></i>${s.nome}<div class="mini">${s.uso}</div></td>
    <td><input class="cub-in num" type="number" min="1" max="60" step="1" value="${s.dmin}" data-i="${i}" data-k="dmin" aria-label="Diâmetro mínimo ${s.nome}"></td>
    <td><input class="cub-in num" type="number" min="0" max="12" step="0.1" value="${s.L}" data-i="${i}" data-k="L" aria-label="Comprimento ${s.nome}"></td></tr>`).join("");
  document.getElementById("tor-crit").innerHTML = `<thead><tr><th>Produto</th><th>Ponta fina mín. (cm)</th><th>Comprimento (m)</th></tr></thead><tbody>${linhaS}</tbody>`;
  document.querySelectorAll("#tor-crit .cub-in").forEach(inp => inp.onchange = () => { const v = parseFloat(inp.value); if (Number.isFinite(v) && v >= 0) SORT[+inp.dataset.i][inp.dataset.k] = v; calcularToras(); });
  calcularToras();
}
function calcularToras() {
  const ac = arvoreDoTalhao("c"), at = arvoreDoTalhao("t"), qual = document.querySelector("#tor-tal .on")?.dataset.t || "c", a = qual === "c" ? ac : at;
  const trC = toras(ac.dap, ac.H), trT = toras(at.dap, at.H), tr = qual === "c" ? trC : trT;
  svgFuste(a.dap, a.H, tr, "tor-svg");
  document.getElementById("tor-lista").innerHTML = `<thead><tr><th>Tora</th><th>Trecho (m)</th><th>Ponta grossa → fina (cm)</th><th>Volume (dm³)</th><th>Destino</th></tr></thead><tbody>` +
    (tr.lista.map((t, i) => `<tr><td class="num">${i + 1}</td><td class="num">${fmt(t.h1, 1)}–${fmt(t.h2, 1)}</td><td class="num">${fmt(t.d1, 1)} → ${fmt(t.d2, 1)}</td><td class="num">${fmt(t.v * 1000, 1)}</td><td><i class="cub-cor" style="background:${t.s.cor}"></i>${t.s.nome}</td></tr>`).join("") || `<tr><td colspan="5" class="mini">Nenhuma tora atende aos critérios.</td></tr>`) +
    `<tr><td>–</td><td class="num">${fmt(tr.hFim, 1)}–${fmt(a.H, 1)}</td><td class="num">${fmt(dTaper(tr.hFim, a.dap, a.H), 1)} → 0</td><td class="num">${fmt(tr.ponta * 1000, 1)}</td><td>Ponteira (fica no campo)</td></tr></tbody>`;
  const porS = trx => Object.fromEntries([...SORT.map(s => [s.id, trx.lista.filter(t => t.s === s).reduce((x, t) => x + t.v, 0)]), ["ponta", trx.ponta + trx.toco]]);
  const pc = porS(trC), pt = porS(trT), lin = (nome, cor, vc, vt) => { const hc = vc * ac.N, ht = vt * at.N, dif = hc > 0 ? 100 * (ht / hc - 1) : NaN;
    return `<tr><td><i class="cub-cor" style="background:${cor}"></i>${nome}</td><td class="num">${fmt(hc, 0)}</td><td class="num">${fmt(ht, 0)}</td><td class="num">${Number.isFinite(dif) ? (dif > 0 ? "+" : "") + fmt(dif, 1) + "%" : "–"}</td></tr>`; };
  document.getElementById("tor-ha").innerHTML = `<thead><tr><th>Destino</th><th>Referência 3-PG (m³/ha)</th><th>Simulação atual (m³/ha)</th><th>Diferença</th></tr></thead><tbody>` +
    SORT.map(s => lin(s.nome, s.cor, pc[s.id], pt[s.id])).join("") + lin("Toco + ponteira", "var(--oliva-3)", pc.ponta, pt.ponta) +
    `<tr><td><b>Total pelo taper</b></td><td class="num"><b>${fmt(trC.total * ac.N, 0)}</b></td><td class="num"><b>${fmt(trT.total * at.N, 0)}</b></td><td class="num">${fmt(100 * (trT.total * at.N / (trC.total * ac.N) - 1), 1)}%</td></tr>
     <tr><td class="mini">Volume do 3-PG, para comparar</td><td class="num mini">${fmt(ac.vol3pg, 0)}</td><td class="num mini">${fmt(at.vol3pg, 0)}</td><td class="num mini">${fmt(100 * (at.vol3pg / ac.vol3pg - 1), 1)}%</td></tr></tbody>`;
  document.getElementById("tor-cena").textContent = `${SIT[E.sitio]} · ${E.mat} · ${E.d}% ${FREQ_L[E.freq]} em ${EPOCA[E.epoca]} · 84 meses · ${fmt(ac.N, 0)} árvores/ha`;
}

function abrirCubagem(aba) {
  if (aba) document.querySelectorAll("#cub-abas button").forEach(b => b.classList.toggle("on", b.dataset.a === aba));
  const a = document.querySelector("#cub-abas .on").dataset.a;
  document.getElementById("cub-a1").hidden = a !== "cub"; document.getElementById("cub-a2").hidden = a !== "tor";
  if (a === "cub") montarCubagem(); else montarToras();
  abrir("m-cubagem");
}
document.getElementById("cub-abas").onclick = e => { const b = e.target.closest("button"); if (!b) return; document.querySelectorAll("#cub-abas button").forEach(x => x.classList.toggle("on", x === b)); abrirCubagem(); document.querySelector("#m-cubagem .pr").scrollTop = 0; };
document.getElementById("cub-tal").onclick = e => { const b = e.target.closest("button"); if (!b) return; CUB_TAL = b.dataset.t; document.querySelectorAll("#cub-tal button").forEach(x => x.classList.toggle("on", x === b)); montarCubagem(); };
document.getElementById("cub-passo").onchange = e => { CUB_PASSO = +e.target.value; montarCubagem(); };
document.getElementById("tor-tal").onclick = e => { const b = e.target.closest("button"); if (!b) return; document.querySelectorAll("#tor-tal button").forEach(x => x.classList.toggle("on", x === b)); calcularToras(); };
document.getElementById("tor-toco").onchange = e => { const v = parseFloat(e.target.value); if (v >= 0 && v < 1) TOCO = v; calcularToras(); };
document.getElementById("tor-pad").onclick = () => { SORT = SORT_PAD.map(s => ({ ...s })); TOCO = 0.1; document.getElementById("tor-toco").value = 0.1; montarToras(); };
document.getElementById("bt-cubagem").onclick = () => abrirCubagem();
document.getElementById("bt-toras").onclick = () => abrirCubagem("tor");
// cálculo com dados próprios de cubagem (altura; diâmetro)
document.getElementById("cub-calc").onclick = () => {
  const lin = document.getElementById("cub-dados").value.split(/\n/).map(l => l.trim().replace(/,/g, ".").split(/[;\s\t]+/).map(Number)).filter(p => p.length >= 2 && p.every(Number.isFinite)).sort((a, b) => a[0] - b[0]);
  const out = document.getElementById("cub-saida");
  if (lin.length < 2) { out.textContent = "Cole pelo menos duas linhas no formato altura;diâmetro (por exemplo 0,1;21,5)."; return; }
  let v = 0; for (let i = 0; i < lin.length - 1; i++) v += (gArea(lin[i][1]) + gArea(lin[i + 1][1])) / 2 * (lin[i + 1][0] - lin[i][0]);
  out.innerHTML = `Volume por Smalian entre ${fmt(lin[0][0], 2)} e ${fmt(lin[lin.length - 1][0], 2)} m: <b class="num">${fmt(v, 4)} m³</b> (${lin.length - 1} seções).`;
};
