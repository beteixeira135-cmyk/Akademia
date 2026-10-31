// Recalcula os números da plataforma citados no TCC (usado por auditoria_final/auditar_numeros.py).
const fs = require("fs"), path = require("path"), vm = require("vm");
const P = path.resolve(__dirname, "..");
const stub = new Proxy(function () {}, { get: (t, k) => k === Symbol.toPrimitive ? () => "" : stub, set: () => true, apply: () => stub });
const ctx = { console, Math, Object, Array, Number, JSON, fmt: x => String(x), document: stub };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(P + "/conceitos.js", "utf8") + "\n;this.CONCEITOS=CONCEITOS;this.GRUPOS=GRUPOS;this.TRILHA=TRILHA;this.PONTES=PONTES;", ctx);
vm.runInContext(fs.readFileSync(P + "/cubagem.js", "utf8") + "\n;this.toras=toras;this.SORT=SORT;", ctx);
const html = fs.readFileSync(P + "/fonte2.html", "utf8");
const passos = (html.split("const PASSOS = [")[1].split("\n];")[0].match(/^\s*\{ t: "/gm) || []).length;
const agentes = (html.split("const AGENTES = {")[1].split("\n};")[0].match(/^\s*[a-z0-9]+: \{ nome:/gm) || []).length;
const M = require(P + "/modelo3pg.js"), D = JSON.parse(fs.readFileSync(P + "/dados_min.json"));
const m = D.materiais.A1, s = D.sitios.IND, ALT = { aH: 3.313814, nHB: 0.715203 };
const run = (ev, o) => M.run({ lat: s.lat, asw_max: s.asw_local, asw_i: s.asw_local, from: m.inicio, to: "2023-01" },
  { planted: "2015-01", fertility: m.FR_ref, stems_n: 10000 / 9, WS0: m.WS0, WR0: m.WR0, WF0: m.WF0 }, s.clima, m.params, ev, o);
const ev = { "2017-01": .95, "2020-01": .95 }, c = run({}), t = run(ev, { comp: D.calibracao.mediana });
const k = c.age.map(a => Math.round(a * 12)).indexOf(84);
const prod = o => { const T = ctx.toras(o.dbh[k], ALT.aH * Math.pow(o.dbh[k], ALT.nHB)); const r = {};
  for (const x of ctx.SORT) r[x.id] = T.lista.filter(y => y.s === x).reduce((a, y) => a + y.v, 0) * o.N[k]; return r; };
const pc = prod(c), pt = prod(t), dif = id => 100 * (pt[id] / pc[id] - 1);
console.log(JSON.stringify({ conceitos: ctx.CONCEITOS.length, grupos: ctx.GRUPOS.length, trilha: ctx.TRILHA.length, pontes: Object.keys(ctx.PONTES).length,
  passos, agentes, amostras: D.calibracao.amostras.length, locais: Object.keys(D.sitios).length,
  serraria_c: pc.serraria, serraria_t: pt.serraria, celulose_c: pc.celulose, celulose_t: pt.celulose, energia_c: pc.energia, energia_t: pt.energia,
  dif_serraria: dif("serraria"), dif_celulose: dif("celulose"), dif_energia: dif("energia") }));
