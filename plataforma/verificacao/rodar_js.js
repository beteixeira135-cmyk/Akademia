const fs = require("fs"), path = require("path");
const M = require(path.resolve(process.argv[2]));
const D = JSON.parse(fs.readFileSync(process.argv[3]));
const C = JSON.parse(fs.readFileSync(process.argv[4]));
const out = {};
for (const c of C) { const m = D.materiais[c.m], s = D.sitios[c.s];
  const o = M.run({ lat: s.lat, asw_max: s.asw_local, asw_i: s.asw_local, from: m.inicio, to: "2023-01" },
    { planted: "2015-01", fertility: m.FR_ref, stems_n: 10000 / 9, WS0: m.WS0, WR0: m.WR0, WF0: m.WF0 }, s.clima, m.params, c.defol, c.opt);
  out[c.id] = { Wf: o.Wf, Ws: o.Ws, Wr: o.Wr, N: o.N, vol: o.vol, lai: o.lai, dbh: o.dbh, asw: o.asw, compU: o.compU }; }
fs.writeFileSync(process.argv[5], JSON.stringify(out));
