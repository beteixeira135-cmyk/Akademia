// ---------- Conceitos: biblioteca, figuras e modo explicar ----------
const C_ID = Object.fromEntries(CONCEITOS.map(c => [c.id, c]));
const C_GR = Object.fromEntries(GRUPOS);
const semAcento = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
// termos ordenados do mais longo ao mais curto, para "lei de Beer" vencer "Beer" e "área basal" vencer "área"
const C_TERMOS = CONCEITOS.flatMap(c => c.termos.map(t => ({ t, n: semAcento(t), id: c.id }))).sort((a, b) => b.n.length - a.n.length);
const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const C_RE = C_TERMOS.map(x => ({ ...x, re: new RegExp(`(^|[^\\p{L}\\p{N}_])${escRe(x.n)}(?=$|[^\\p{L}\\p{N}_])`, "u") }));
function acharConceito(texto) {
  const n = semAcento(texto || ""); let best = null;
  for (const x of C_RE) { const m = x.re.exec(n); if (m) { const pos = m.index + m[1].length; if (!best || pos < best.pos) best = { id: x.id, pos }; } }
  return best && best.id;
}

// figuras (SVG desenhado aqui; cores da plataforma)
const FIG = {
  beer() {
    const k = 0.5, W = 300, H = 170, x0 = 38, y0 = 140, sx = 30, sy = 110, pt = L => [x0 + L * sx, y0 - (1 - Math.exp(-k * L)) * sy];
    const d = Array.from({ length: 81 }, (_, i) => pt(i / 10)).map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1)).join("");
    const [ax, ay] = pt(2.93), [bx, by] = pt(1.46);
    return `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Curva da lei de Beer"><g font-size="10" fill="var(--tinta-2)" font-family="var(--f-sans)">
      <path d="M${x0} 30 V${y0} H${x0 + 8 * sx}" fill="none" stroke="var(--linha-2)"/>
      ${[0, 2, 4, 6, 8].map(L => `<text x="${x0 + L * sx}" y="${y0 + 13}" text-anchor="middle">${L}</text>`).join("")}
      ${[0, .5, 1].map(f => `<text x="${x0 - 5}" y="${y0 - f * sy + 3}" text-anchor="end">${String(f).replace(".", ",")}</text>`).join("")}
      <text x="${x0 + 4 * sx}" y="${H - 2}" text-anchor="middle">IAF (m² de folha por m² de chão)</text>
      <text x="${x0 + 4}" y="24">fração da luz absorvida, k = 0,5</text>
      <path d="${d}" fill="none" stroke="var(--oliva)" stroke-width="2"/>
      <path d="M${bx} ${by} V${y0} M${ax} ${ay} V${y0}" stroke="var(--alerta)" stroke-dasharray="3 3"/>
      <circle cx="${ax}" cy="${ay}" r="3.5" fill="var(--oliva)"/><circle cx="${bx}" cy="${by}" r="3.5" fill="var(--alerta)"/>
      <text x="${ax + 8}" y="${ay + 16}" fill="var(--tinta)">antes: IAF 2,93 → 77%</text>
      <text x="${bx + 6}" y="${by + 26}" fill="var(--alerta)">após 50%: IAF 1,46 → 52%</text>
      <text x="296" y="${y0 - 22}" text-anchor="end" fill="var(--tinta)" font-weight="600">metade das folhas,</text><text x="296" y="${y0 - 9}" text-anchor="end" fill="var(--tinta)" font-weight="600">só 1/3 a menos de luz</text></g></svg>
      <p class="fig-leg">Curva calculada com a equação acima. Os pontos são o caso de Indianópolis (clone A1, janeiro de 2017).</p>`;
  },
  fotossintese() {
    return `<svg viewBox="0 0 300 150" width="100%" role="img" aria-label="Esquema da fotossíntese"><g font-family="var(--f-sans)" font-size="10.5" fill="var(--tinta)">
      <circle cx="40" cy="30" r="13" fill="#e9c46a" stroke="var(--terra)"/><text x="40" y="58" text-anchor="middle">luz (PAR)</text>
      <path d="M100 85 C140 40 210 40 250 85 C210 115 140 115 100 85Z" fill="var(--oliva-3)" stroke="var(--oliva)"/><path d="M100 85 H250" stroke="var(--oliva)"/>
      <text x="175" y="78" text-anchor="middle" font-weight="600">folha</text><text x="175" y="100" text-anchor="middle" fill="var(--tinta-2)">açúcar → folhas, lenho, raízes</text>
      <path d="M52 40 L118 70" stroke="var(--terra)" stroke-width="1.5" marker-end="url(#sa)"/>
      <path d="M60 128 H118 L130 96" fill="none" stroke="var(--agua)" stroke-width="1.5" marker-end="url(#sa)"/><text x="10" y="132">água (raiz)</text>
      <path d="M270 25 L232 60" stroke="var(--tinta-2)" stroke-width="1.5" marker-end="url(#sa)"/><text x="248" y="20">CO₂ do ar</text>
      <path d="M232 108 L268 136" stroke="var(--oliva)" stroke-width="1.5" marker-end="url(#sa)"/><text x="232" y="148">O₂ sai</text>
      <defs><marker id="sa" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="var(--tinta-2)"/></marker></defs></g></svg>`;
  },
  particao() {
    const b = (y, w, c, t) => `<rect x="120" y="${y}" width="${w}" height="20" fill="${c}"/><text x="${126 + w}" y="${y + 14}">${t}</text>`;
    return `<svg viewBox="0 0 300 120" width="100%" role="img" aria-label="Partição do carbono"><g font-family="var(--f-sans)" font-size="10.5" fill="var(--tinta)">
      <rect x="6" y="38" width="80" height="40" fill="var(--prancha)" stroke="var(--tinta-2)"/><text x="46" y="55" text-anchor="middle">NPP</text><text x="46" y="69" text-anchor="middle" fill="var(--tinta-2)">do mês</text>
      <path d="M86 58 L118 22 M86 58 L118 58 M86 58 L118 94" stroke="var(--tinta-3)" fill="none"/>
      ${b(12, 40, "var(--oliva-2)", "folhas η_F")}${b(48, 80, "var(--argila)", "lenho η_S")}${b(84, 50, "var(--terra)", "raízes η_R")}
      </g></svg><p class="fig-leg">Proporções ilustrativas. Com seca, a barra das raízes cresce e a do lenho encolhe.</p>`;
  },
  solo() {
    return `<svg viewBox="0 0 300 130" width="100%" role="img" aria-label="Solo como caixa d'água"><g font-family="var(--f-sans)" font-size="10.5" fill="var(--tinta)">
      <rect x="110" y="20" width="80" height="96" fill="none" stroke="var(--tinta-2)" stroke-width="1.5"/><rect x="111" y="62" width="78" height="53" fill="var(--agua)" opacity=".45"/>
      <text x="150" y="94" text-anchor="middle">ASW</text><text x="200" y="26">CAD (cheia)</text><path d="M108 20 H196" stroke="var(--tinta-3)" stroke-dasharray="3 3"/>
      <text x="16" y="16">chuva entra</text><path d="M50 22 V40 L108 40" fill="none" stroke="var(--agua)" stroke-width="1.5" marker-end="url(#sb)"/>
      <text x="200" y="66">transpiração e</text><text x="200" y="79">evaporação saem</text><path d="M190 70 H198" stroke="var(--oliva)" stroke-width="1.5"/>
      <text x="200" y="112">excesso escorre</text><path d="M190 108 H198" stroke="var(--tinta-3)" stroke-width="1.5"/>
      <defs><marker id="sb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="var(--agua)"/></marker></defs></g></svg>`;
  },
  taper() {
    // perfil pelo polinômio de Schöepfer de Souza et al. (2016), T5; ver cubagem.js
    const bb = [1.16763760, -3.27135930, 14.22874988, -33.96062159, 35.94747372, -14.11411271], f = r => bb.reduce((s, b, i) => s + b * r ** i, 0);
    const pts = Array.from({ length: 41 }, (_, i) => { const r = i / 40; return [Math.max(0, f(r)) * 22, 140 - r * 128]; });
    const dir = pts.map(([d, y], i) => (i ? "L" : "M") + (80 + d).toFixed(1) + " " + y.toFixed(1)).join("");
    const esq = pts.slice().reverse().map(([d, y]) => "L" + (80 - d).toFixed(1) + " " + y.toFixed(1)).join("");
    const y13 = 140 - (1.3 / 25) * 128;
    return `<svg viewBox="0 0 300 160" width="100%" role="img" aria-label="Perfil do fuste"><g font-family="var(--f-sans)" font-size="10.5" fill="var(--tinta)">
      <path d="${dir}${esq}Z" fill="var(--argila)" stroke="var(--terra)"/><path d="M30 140 H130" stroke="var(--tinta-3)"/>
      <path d="M50 ${y13} H110" stroke="var(--alerta)"/><text x="114" y="${y13 + 4}" fill="var(--alerta)">DAP (1,30 m)</text>
      <text x="150" y="20">base grossa → serraria</text><text x="150" y="36">meio → celulose</text><text x="150" y="52">ponta fina → lenha</text>
      <text x="150" y="96" fill="var(--tinta-2)">d/DAP de Souza et al. (2016);</text><text x="150" y="109" fill="var(--tinta-2)">largura exagerada</text></g></svg>`;
  },
  desfolha() {
    const arv = (x, f) => `<path d="M${x} 120 V70" stroke="var(--terra)" stroke-width="4"/><ellipse cx="${x}" cy="55" rx="${26 * f}" ry="${30 * f}" fill="var(--oliva-2)" stroke="var(--oliva)"/>`;
    return `<svg viewBox="0 0 300 140" width="100%" role="img" aria-label="Desfolha"><g font-family="var(--f-sans)" font-size="10.5" fill="var(--tinta)">
      ${arv(50, 1)}${arv(150, .7)}${arv(250, .95)}<path d="M20 120 H280" stroke="var(--linha-2)"/>
      <text x="50" y="135" text-anchor="middle">antes</text><text x="150" y="135" text-anchor="middle">mês do ataque (−d)</text><text x="250" y="135" text-anchor="middle">folhas voltam</text>
      <path d="M86 55 H112 M186 55 H212" stroke="var(--tinta-3)" marker-end="url(#sc)"/>
      <defs><marker id="sc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="var(--tinta-3)"/></marker></defs></g></svg>
      <p class="fig-leg">As folhas voltam, mas o tronco que deixou de crescer durante a recuperação não volta.</p>`;
  },
  cadeia() {
    const cx = ["Clima e solo", "Folhas (IAF)", "Luz absorvida", "Fotossíntese", "Partição", "Madeira"];
    return `<svg viewBox="0 0 300 70" width="100%" role="img" aria-label="Cadeia do 3-PG"><g font-family="var(--f-sans)" font-size="9" fill="var(--tinta)">
      ${cx.map((t, i) => `<rect x="${2 + i * 50}" y="18" width="44" height="34" fill="var(--prancha)" stroke="var(--oliva)"/>${t.split(" ").map((w, j, a) => `<text x="${24 + i * 50}" y="${37 + (j - (a.length - 1) / 2) * 10}" text-anchor="middle">${w}</text>`).join("")}${i < 5 ? `<path d="M${46 + i * 50} 35 h6" stroke="var(--tinta-2)"/>` : ""}`).join("")}
      <text x="150" y="66" text-anchor="middle" fill="var(--tinta-2)">repetido a cada mês da rotação</text></g></svg>`;
  },
  validacao() {
    const cel = (x, c, t) => `<rect x="${x}" y="0" width="54" height="22" fill="${c}" stroke="var(--prancha)"/><text x="${x + 27}" y="15" text-anchor="middle">${t}</text>`;
    const lin = (y, k) => `<g transform="translate(60 ${y})">${[0, 1, 2, 3, 4].map(i => cel(i * 56, i === k ? "var(--argila)" : "var(--oliva-3)", i === k ? "teste" : "treino")).join("")}</g>`;
    return `<svg viewBox="0 0 345 92" width="100%" role="img" aria-label="Validação cruzada"><g font-family="var(--f-sans)" font-size="10" fill="var(--tinta)">
      ${[0, 1, 2].map(k => `<text x="0" y="${k * 30 + 15}">rodada ${k + 1}</text>${lin(k * 30, k)}`).join("")}</g></svg>
      <p class="fig-leg">Cada rodada esconde uma parte diferente dos dados, que serve só para testar.</p>`;
  },
  rf() {
    const arv = x => `<circle cx="${x}" cy="16" r="6" fill="var(--oliva-2)"/><path d="M${x} 22 L${x - 14} 44 M${x} 22 L${x + 14} 44" stroke="var(--tinta-3)"/><circle cx="${x - 14}" cy="48" r="5" fill="var(--oliva-3)" stroke="var(--oliva)"/><circle cx="${x + 14}" cy="48" r="5" fill="var(--oliva-3)" stroke="var(--oliva)"/>`;
    return `<svg viewBox="0 0 300 100" width="100%" role="img" aria-label="Random Forest"><g font-family="var(--f-sans)" font-size="10" fill="var(--tinta)">
      ${[40, 100, 160, 220].map(arv).join("")}<text x="262" y="34" font-size="16">…</text>
      ${[40, 100, 160, 220].map((x, i) => `<text x="${x}" y="70" text-anchor="middle" fill="var(--tinta-2)">voto ${i + 1}</text>`).join("")}
      <text x="150" y="92" text-anchor="middle">previsão = média das árvores (ilustrativo)</text></g></svg>`;
  },
  rna() {
    const cam = [3, 5, 4, 1], xs = [30, 110, 190, 270], ys = n => Array.from({ length: n }, (_, i) => 50 + (i - (n - 1) / 2) * 18);
    let ln = ""; for (let c = 0; c < 3; c++) for (const a of ys(cam[c])) for (const b of ys(cam[c + 1])) ln += `<path d="M${xs[c]} ${a} L${xs[c + 1]} ${b}" stroke="var(--linha-2)" stroke-width=".7"/>`;
    const nos = cam.map((n, c) => ys(n).map(y => `<circle cx="${xs[c]}" cy="${y}" r="6" fill="${c === 0 ? "var(--agua)" : c === 3 ? "var(--alerta)" : "var(--oliva-2)"}"/>`).join("")).join("");
    return `<svg viewBox="0 0 300 115" width="100%" role="img" aria-label="Rede neural"><g font-family="var(--f-sans)" font-size="10" fill="var(--tinta)">${ln}${nos}
      <text x="30" y="108" text-anchor="middle">entradas</text><text x="150" y="108" text-anchor="middle">camadas ocultas</text><text x="270" y="108" text-anchor="middle">saída</text></g></svg>
      <p class="fig-leg">Esquema com poucos neurônios. A rede testada no TCC tinha camadas de 50 e 30.</p>`;
  },
};

// biblioteca
let cGrupo = "todos";
function cardHTML(c, aberto) {
  const ponte = PONTES[c.id] ? `<div class="c-ponte"><b>Da biologia para a floresta.</b> ${PONTES[c.id]}</div>` : "";
  const ver = (c.ver || []).filter(v => C_ID[v]).map(v => `<button class="c-tag" data-c="${v}" type="button">${C_ID[v].titulo}</button>`).join("");
  return `<details class="c-card" id="c-${c.id}" ${aberto ? "open" : ""}><summary><span class="c-tit">${c.titulo}</span><span class="c-curto">${c.curto}</span></summary>
    <div class="c-corpo">${c.texto}${c.formula ? `<div class="eq">${c.formula}</div>` : ""}${c.fig && FIG[c.fig] ? `<figure class="c-fig">${FIG[c.fig]()}</figure>` : ""}${ponte}
    <p class="mini"><b>Onde aparece:</b> ${c.onde}</p>${ver ? `<div class="c-ver"><span class="mini">Veja também:</span> ${ver}</div>` : ""}</div></details>`;
}
function montarConceitos(foco) {
  const q = semAcento(document.getElementById("c-busca").value.trim());
  const lista = CONCEITOS.filter(c => (cGrupo === "todos" || c.grupo === cGrupo) && (!q || semAcento(c.titulo + " " + c.termos.join(" ") + " " + c.curto + " " + c.texto).includes(q)));
  const corpo = document.getElementById("c-lista");
  if (!lista.length) { corpo.innerHTML = `<p class="mini">Nenhum conceito encontrado. Tente outra palavra, como "folha", "água" ou "erro".</p>`; return; }
  corpo.innerHTML = GRUPOS.filter(([g]) => lista.some(c => c.grupo === g)).map(([g, nome]) => `<h3 class="c-gr">${nome}</h3>` + lista.filter(c => c.grupo === g).map(c => cardHTML(c, c.id === foco || !!q)).join("")).join("");
}
function abrirConceito(id) {
  document.getElementById("c-sem").hidden = true;
  const ini = document.getElementById("c-inicio");
  if (id) { cGrupo = "todos"; document.getElementById("c-busca").value = ""; ini.open = false; }
  document.querySelectorAll("#c-grupos button").forEach(b => b.classList.toggle("on", b.dataset.g === cGrupo));
  montarConceitos(id); abrir("m-conceitos");
  if (id) { const el = document.getElementById("c-" + id); if (el) { el.open = true; requestAnimationFrame(() => el.scrollIntoView({ block: "start" })); } }
  else document.querySelector("#m-conceitos .pr").scrollTop = 0;
}
document.getElementById("c-grupos").innerHTML = [["todos", "Todos"], ...GRUPOS.map(([g, n]) => [g, n.replace(/^\d+\.\s*/, "")])].map(([g, n]) => `<button type="button" class="c-filtro" data-g="${g}">${n}</button>`).join("");
document.getElementById("c-grupos").onclick = e => { const b = e.target.closest("button"); if (!b) return; cGrupo = b.dataset.g; document.querySelectorAll("#c-grupos button").forEach(x => x.classList.toggle("on", x === b)); montarConceitos(); };
document.getElementById("c-busca").oninput = () => montarConceitos();
document.getElementById("c-trilha").innerHTML = TRILHA.map((id, i) => `<button class="c-tag" data-c="${id}" type="button">${i + 1}. ${C_ID[id].titulo.replace(/\s*\(.*\)$/, "")}</button>`).join(" ");
document.getElementById("m-conceitos").addEventListener("click", e => { const b = e.target.closest("[data-c]"); if (b) { e.preventDefault(); abrirConceito(b.dataset.c); } });
document.getElementById("bt-conceitos").onclick = () => abrirConceito();

// termos clicáveis dentro de textos (tutorial): envolve a primeira ocorrência de cada conceito
function linkarTermos(raiz) {
  const usados = new Set(), walker = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT), nos = [];
  while (walker.nextNode()) if (!walker.currentNode.parentElement.closest(".eq,.termo,button")) nos.push(walker.currentNode);
  for (const no of nos) {
    const txt = no.nodeValue, n = semAcento(txt); let achado = null;
    for (const x of C_RE) { if (usados.has(x.id)) continue; const m = x.re.exec(n); if (m) { const pos = m.index + m[1].length; if (!achado || pos < achado.pos) achado = { pos, len: x.n.length, id: x.id }; } }
    if (!achado) continue; usados.add(achado.id);
    const b = document.createElement("button"); b.type = "button"; b.className = "termo"; b.dataset.c = achado.id; b.title = "O que é isto?"; b.textContent = txt.substr(achado.pos, achado.len);
    const resto = no.splitText(achado.pos); resto.nodeValue = resto.nodeValue.slice(achado.len); no.parentNode.insertBefore(b, resto);
    nos.push(resto);
  }
}
document.getElementById("tour").addEventListener("click", e => { const b = e.target.closest(".termo"); if (b) abrirConceito(b.dataset.c); });

// modo explicar: com ele ligado, tocar em qualquer parte da tela abre o conceito correspondente
const C_AREA = { janela: "modelo-3pg", cena: "desfolha", "s-desfolha": "desfolha", "s-particao": "particao", "s-wue": "wue", "s-solo": "agua-solo", "s-estresse": "modificadores",
  "s-estrutura": "biomassa", "g-bio": "biomassa", "g-vol": "taper", "tor-svg": "sortimento", "cub-tab": "cubagem", "tab-par": "parametrizacao", "s-entradas": "parametrizacao", "barras-estresse": "modificadores", resumo: "perda-relativa", marcas: "desfolha", "s-resposta": "compensacao", "seg-comp": "compensacao", dominio: "dominio-validade", "in-r": "perda-eficiencia", "in-m": "mortalidade-induzida", "sel-agente": "desfolha" };
let explicando = false;
function modoExplicar(on) {
  explicando = on; document.body.classList.toggle("explicar", on);
  const b = document.getElementById("bt-explicar"); b.setAttribute("aria-pressed", on); b.textContent = on ? "Sair do modo explicar" : "Modo explicar";
  document.getElementById("aviso-explicar").hidden = !on;
}
document.getElementById("bt-explicar").onclick = () => modoExplicar(!explicando);
document.getElementById("aviso-sair").onclick = () => modoExplicar(false);
document.addEventListener("click", e => {
  if (!explicando || e.target.closest("#m-conceitos,#bt-explicar,#aviso-explicar,.tour,.cab nav")) return;
  e.preventDefault(); e.stopPropagation();
  let el = e.target, id = null;
  for (let i = 0; el && el !== document.body && i < 6 && !id; i++, el = el.parentElement) {
    const proprio = [el.getAttribute("aria-label"), el.tagName === "SELECT" ? "" : el.innerText].filter(Boolean).join(" ").slice(0, 400);
    id = (el.id && C_AREA[el.id]) || (el.id && document.querySelector(`label[for="${el.id}"]`) ? acharConceito(document.querySelector(`label[for="${el.id}"]`).innerText) : null) || acharConceito(proprio);
  }
  abrirConceito(id || undefined);
  if (!id) document.getElementById("c-sem").hidden = false;
}, true);
// no celular, o seletor nativo abre antes do clique; no modo explicar ele é bloqueado
document.addEventListener("pointerdown", e => { if (explicando && e.target.closest("select,input") && !e.target.closest("#m-conceitos")) e.preventDefault(); }, true);
