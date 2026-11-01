// Extrai as tabelas do TCC (tcc_docx/gerar.js, objeto TABS) para a plataforma, sem redigitar números.
const fs = require("fs"), path = require("path");
const g = fs.readFileSync(path.join(__dirname, "../tcc_docx/gerar.js"), "utf8");
const i = g.indexOf("const TABS = {"), j = g.indexOf("\n};", i);
const tabela = (titulo, cab, linhas, larg, nota) => ({ titulo, cab, linhas, nota: nota || "" });
const TABS = eval("(" + g.slice(i + "const TABS = ".length, j + 2) + ")");
const out = {};
for (const k of Object.keys(TABS)) out[k] = TABS[k]();
fs.writeFileSync(path.join(__dirname, "material_tabelas.json"), JSON.stringify(out));
console.log(Object.keys(out).join(", "));
