const C = require(__dirname + "/../tcc_docx/conteudo.js"); const fs = require("fs");
const g = fs.readFileSync(__dirname + "/../tcc_docx/gerar.js", "utf8");
const ap = g.slice(g.indexOf('SUM.push(["APÊNDICE A'), g.indexOf("// ---------- pré-textuais"));
const ti = g.indexOf("const TABS"), TABS = g.slice(ti, g.indexOf("\n};", ti));
let notas = ""; for (const b of C.corpo) if (b.table) { const j = TABS.indexOf("  " + b.table + ": () =>"); notas += TABS.slice(j, j + 3000); }
const txt = [C.resumo, ...C.conclusao, ...C.corpo.map(b => [b.p, b.li, b.cap, (b.caixa || []).join(" ")].filter(Boolean).join(" ")), ap, notas].join(" ");
const norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toUpperCase(); const T = norm(txt);
const semCit = [];
for (const r of C.referencias) {
  const au = norm(r.split(/[.,;]/)[0].trim()).split(/\s+/)[0].replace(/[^A-Z]/g, "");
  const anos = r.match(/\b(19|20)\d{2}[a-z]?\b/g) || [];
  if (!anos.some(y => new RegExp(au + "[\\s\\S]{0,90}?" + y.slice(0, 4)).test(T))) semCit.push(r.slice(0, 100));
}
console.log("Referências sem citação:", semCit.length); semCit.forEach(x => console.log(" -", x));
// citações no texto sem referência
const cits = new Set();
for (const m of txt.matchAll(/\(([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ .;&a-z,\-]+?), (\d{4}[a-z]?)/g)) cits.add(m[1].split(";")[0].trim().split(" ")[0] + " " + m[2]);
for (const m of txt.matchAll(/([A-Z][a-zçãéíóú]+)(?: et al\.)?(?:,| e) ?[^()]{0,40}?\((\d{4}[a-z]?)/g)) cits.add(m[1].toUpperCase() + " " + m[2]);
const R = norm(C.referencias.join(" | "));
const falta = [...cits].filter(c => { const [a, y] = c.split(" "); return !new RegExp(norm(a).replace(/[^A-Z]/g, "") + "[^|]{0,400}" + y.slice(0, 4)).test(R); });
console.log("Citações sem referência (verificar):", falta.join(", "));
