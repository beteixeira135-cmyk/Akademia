// Confere se cada número decimal do texto do TCC (resumo, corpo, conclusão) aparece entre os valores auditados.
const C = require("../tcc_docx/conteudo.js"); const fs = require("fs");
const A = fs.readFileSync(__dirname + "/../auditoria_final/auditoria_numeros.csv", "utf8").trim().split("\n").slice(1)
  .map(l => { const p = l.split(","); return parseFloat(p[p.length - 3]); });
const vals = new Set(); for (const v of A) for (const x of [v, -v, Math.abs(v)]) vals.add(x.toFixed(4));
const blocos = [["resumo", C.resumo], ...C.conclusao.map((t, i) => ["conclusão " + (i + 1), t]),
  ...C.corpo.filter(b => b.p).map(b => ["corpo", b.p])];
let n = 0, faltam = [];
for (const [onde, t] of blocos) for (const m of t.matchAll(/(?<![\d.,])(−?\d{1,3}(?:\.\d{3})*,\d+|−?\d+(?:\.\d{3})+)(?![\d])/g)) {
  n++; const v = parseFloat(m[1].replace(/\./g, "").replace(",", ".").replace("−", "-"));
  if (!vals.has(v.toFixed(4)) && !vals.has((-v).toFixed(4))) faltam.push(`${onde}: ${m[1]}  …${t.slice(Math.max(0, m.index - 50), m.index + 15).replace(/\s+/g, " ")}`);
}
console.log(`${n} números decimais no texto; ${faltam.length} sem item na auditoria`); faltam.forEach(x => console.log(" -", x));
