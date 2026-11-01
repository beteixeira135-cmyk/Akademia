// ---------- Material do TCC: tabelas densas do TCC, replicadas aqui ----------
const mdHTML = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
  .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/\*(.+?)\*/g, "<i>$1</i>").replace(/~(.+?)~/g, "<sub>$1</sub>").replace(/\^(.+?)\^/g, "<sup>$1</sup>");
function tabelaMT(t) {
  return `<p class="mt-tit">${mdHTML(t.titulo)}</p><div class="tabs-wrap"><table class="tab"><thead><tr>${t.cab.map(c => `<th>${mdHTML(c)}</th>`).join("")}</tr></thead>
    <tbody>${t.linhas.map(l => `<tr>${l.map(c => `<td>${mdHTML(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>${t.nota ? `<p class="mini">${mdHTML(t.nota)}</p>` : ""}`;
}
function montarMaterial() {
  document.getElementById("mt-indice").innerHTML = MATERIAL_TCC.map(m => `<button type="button" class="c-filtro" data-mt="${m.id}">${m.titulo}</button>`).join("");
  document.getElementById("mt-corpo").innerHTML = MATERIAL_TCC.map(m => `<section class="secao" id="${m.id}"><h3>${m.titulo}</h3>
    <p class="mini"><b>No TCC: seção ${m.secao}.</b> ${m.intro}</p>${m.tabelas.map(tabelaMT).join("")}</section>`).join("");
  document.querySelectorAll("#mt-indice button").forEach(b => b.onclick = () => document.getElementById(b.dataset.mt).scrollIntoView({ behavior: "smooth", block: "start" }));
}
function abrirMaterial(id) { abrir("m-tcc"); if (id && document.getElementById(id)) setTimeout(() => document.getElementById(id).scrollIntoView({ block: "start" }), 50); }
document.getElementById("bt-material").onclick = () => abrirMaterial();
montarMaterial();
try { const h = location.hash.slice(1); if (h === "material" || h.startsWith("mt-")) setTimeout(() => abrirMaterial(h.startsWith("mt-") ? h : null), 300); } catch (e) {}
