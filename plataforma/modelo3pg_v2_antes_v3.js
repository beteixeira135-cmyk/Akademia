// 3-PGpjs (r3PG v0.1.7, src/md_3PG.f95) + módulo de desfolha — porte para JavaScript
// do port Python verificado (threepg_pjs.py). Escopo: 1 espécie, light/transp/phys_model = 1,
// height_model 1, sem correção de viés, sem desbaste.
(function (root) {
  const PI = 3.141592654, LN2 = 0.693147181, E20 = 2.2, LAMBDA = 2460000.0, RHO_AIR = 1.2, VPD_CONV = 0.000622;
  const DOY = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349];
  const DIM = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const B_N = 2;
  const dormant = (m, g, f) => g > f ? (f <= m && m <= g) : g < f ? (m < g || m >= f) : false;
  const fexp = (x, g0, gx, tg, ng) => tg !== 0 ? gx + (g0 - gx) * Math.exp(-LN2 * Math.pow(x / tg, ng)) : gx;
  const fexpF = (x, f1, f0, tg) => { if (tg * f1 === 0) return f1; const kg = 12 * Math.log(1 + f1 / f0) / tg; return f1 * f0 / (f0 + (f1 - f0) * Math.exp(-kg * x)); };
  function daylength(lat) {
    const sl = Math.sin(PI * lat / 180), cl = Math.cos(PI * lat / 180);
    return DOY.map(d => { const sd = 0.4 * Math.sin(0.0172 * (d - 80)); const c = -sd * sl / (cl * Math.sqrt(1 - sd * sd));
      return c > 1 ? 0 : c < -1 ? 1 : Math.acos(c) / PI; });
  }
  function mortality(stems, ws, mS, wSx1000, tp) {
    let n = stems / 1000, i = 0; const x1 = 1000 * mS * ws / stems;
    while (true) { i++; if (n <= 0) break; const x2 = wSx1000 * Math.pow(n, 1 - tp); const fN = x2 - x1 * n - (1 - mS) * ws;
      const dfN = (1 - tp) * x2 / n - x1; const dN = -fN / dfN; n += dN; if (Math.abs(dN) <= 0.001 || i >= 5) break; }
    return stems - 1000 * n;
  }
  const ym = (y, m) => y * 12 + (m - 1);

  // site: {lat, asw_max, asw_i, from:"YYYY-MM", to}; sp: {planted, fertility, stems_n, WS0, WR0, WF0}
  // clim: {year[], month[], tmp_min[], tmp_max[], tmp_ave[], prcp[], srad[], frost_days[], vpd_day[]}
  // defol: {"YYYY-MM": d}
  function run(site, sp, clim, P, defol) {
    const [yi, mi] = site.from.split("-").map(Number), [yt, mt] = site.to.split("-").map(Number), [yp, mp] = sp.planted.split("-").map(Number);
    const i0 = clim.year.findIndex((y, k) => ym(y, clim.month[k]) === ym(yi, mi));
    const n = ym(yt, mt) - ym(yi, mi) + 1;
    if (i0 < 0 || i0 + n > clim.year.length) throw new Error("Clima não cobre o período");
    const g = (k, t) => clim[k][i0 + t];
    const ev = new Float64Array(n);
    for (const [k, d] of Object.entries(defol || {})) {
      const [y, m] = k.split("-").map(Number); const t = ym(y, m) - ym(yi, mi);
      if (!(d >= 0 && d < 1)) throw new Error("Intensidade deve estar em [0,1)");
      if (t < 1 || t >= n) throw new Error("Evento fora da simulação: " + k);
      ev[t] = d;
    }
    const lg = Math.round(P.leafgrow), lf = Math.round(P.leaffall);
    const dl = daylength(site.lat).map(x => 86400 * x);
    const fCax = P.fCalpha700 / (2 - P.fCalpha700), fCg0 = P.fCg700 / (2 * P.fCg700 - 1);
    const expo = (P.Tmax - P.Topt) / (P.Topt - P.Tmin);
    const fT = t => { const ta = g("tmp_ave", t); return (ta <= P.Tmin || ta >= P.Tmax) ? 0 : ((ta - P.Tmin) / (P.Topt - P.Tmin)) * Math.pow((P.Tmax - ta) / (P.Tmax - P.Topt), expo); };
    const SWconst = P.SWconst0, SWpower = P.SWpower0; // soil_class = -1
    let asw_min = 0, asw_max = site.asw_max; let ASW = Math.max(Math.min(site.asw_i, asw_max), asw_min);
    const fN0 = P.fNn === 0 ? 1 : P.fN0;
    const pfsPower = Math.log(P.pFS20 / P.pFS2) / Math.log(10), pfsConst = P.pFS2 / Math.pow(2, pfsPower);
    const age = [], agem = [];
    for (let t = 0; t < n; t++) { age.push((12 * (yi - yp) + mi - mp - 1 + t + 1) / 12); agem.push(t === 0 ? age[0] : age[t] - 1 / 12); }
    const SLA = agem.map(a => fexp(a, P.SLA0, P.SLA1, P.tSLA, 2)), fBB = agem.map(a => fexp(a, P.fracBB0, P.fracBB1, P.tBB, 1));
    const rho = agem.map(a => fexp(a, P.rho0, P.rho1, P.tRho, 1)), gN = age.map(a => fexp(a, P.gammaN0, P.gammaN1, P.tgammaN, P.ngammaN));
    const gF = agem.map(a => fexpF(a, P.gammaF1, P.gammaF0, P.tgammaF));
    const fage = agem.map(a => P.nAge === 0 ? 1 : 1 / (1 + Math.pow((a / P.MaxAge) / P.rAge, P.nAge)));
    const S = { N: 0, Ws: 0, Wf: 0, Wr: 0, debt: 0, bt: 0, dbh: 0, ba: 0, h: 0, lai: 0, pFS: 0 };
    const sdc = t => { const comp = rho[t] * S.ba; S.dbh = Math.pow(S.bt / P.aWs, 1 / P.nWs); S.ba = S.dbh * S.dbh / 4 * PI * S.N / 10000;
      S.h = P.aH * Math.pow(S.dbh, P.nHB) * Math.pow(comp, P.nHC); S.pFS = pfsConst * Math.pow(S.dbh, pfsPower); };
    const upd = t => { S.bt = S.N === 0 ? 0 : S.Ws * 1000 / S.N; S.lai = S.Wf * SLA[t] * 0.1; };
    const vol = t => S.Ws * (1 - fBB[t]) / rho[t];
    const out = { mes: [], age: [], Wf: [], Ws: [], Wr: [], lai: [], dbh: [], h: [], vol: [], N: [], asw: [], fT: [], fSW: [], npp: [], removido: [], fracBB: [],
      gpp: [], apar: [], alpha: [], fVPD: [], fAge: [], phys: [], transp: [], et: [], prcp: [], etaR: [], etaS: [], etaF: [] };
    const rec = (t, x) => { out.mes.push(t); out.age.push(age[t]); out.Wf.push(S.Wf); out.Ws.push(S.Ws); out.Wr.push(S.Wr); out.lai.push(S.lai);
      out.dbh.push(S.dbh); out.h.push(S.h); out.vol.push(vol(t)); out.N.push(S.N); out.asw.push(ASW); out.fT.push(fT(t));
      out.fSW.push(x.fsw); out.npp.push(x.npp); out.removido.push(x.rem); out.fracBB.push(fBB[t]);
      for (const k of ["gpp","apar","alpha","fVPD","phys","transp","et","prcp","etaR","etaS","etaF"]) out[k].push(x[k] ?? NaN); out.fAge.push(fage[t]); };
    let month = mi;
    if (age[0] >= 0) Object.assign(S, { N: sp.stems_n, Ws: sp.WS0, Wf: sp.WF0, Wr: sp.WR0 });
    if (dormant(month, lg, lf)) { S.debt = S.Wf; S.Wf = 0; }
    S.bt = S.Ws * 1000 / S.N; S.dbh = Math.pow(S.bt / P.aWs, 1 / P.nWs); S.ba = S.dbh * S.dbh / 4 * PI * S.N / 10000; S.lai = S.Wf * SLA[0] * 0.1;
    S.h = P.aH * Math.pow(S.dbh, P.nHB) * Math.pow(rho[0] * S.ba, P.nHC);
    for (let k = 0; k < B_N; k++) sdc(0);
    rec(0, { fsw: NaN, npp: 0, rem: 0 });
    for (let t = 1; t < n; t++) {
      month = month + 1 > 12 ? 1 : month + 1;
      let bcor = false;
      const dorm = dormant(month, lg, lf), dprev = dormant(month - 1, lg, lf);
      if (!dorm && dprev) { S.lai = S.debt * SLA[t] * 0.1; bcor = true; }
      if (dorm && !dprev) { S.debt = S.Wf; S.Wf = 0; S.lai = 0; bcor = true; }
      if (bcor) { for (let k = 0; k < B_N; k++) sdc(t); bcor = false; }
      let rem = 0;
      if (ev[t] > 0) { rem = S.Wf * ev[t]; S.Wf -= rem; S.lai = S.Wf * SLA[t] * 0.1; }
      let cc = 1; if (P.fullCanAge > 0 && agem[t] < P.fullCanAge) cc = (agem[t] + 0.01) / P.fullCanAge;
      const li = 1 - Math.exp(-P.k * S.lai / cc), apar = g("srad", t) * DIM[month - 1] * li * cc, vpd = g("vpd_day", t);
      const fvpd = Math.exp(-P.CoeffCond * vpd), fsw = 1 / (1 + Math.pow((1 - ASW / asw_max) / SWconst, SWpower));
      const fnutr = P.fNn === 0 ? 1 : 1 - (1 - fN0) * Math.pow(1 - sp.fertility, P.fNn);
      const fphys = Math.min(fvpd, fsw) * fage[t];
      const ffrost = 1 - P.kF * (Math.min(g("frost_days", t), DIM[month - 1]) / DIM[month - 1]);
      const fcal = fCax * 350 / (350 * (fCax - 1) + 350), fcg = fCg0 / (1 + (fCg0 - 1) * 350 / 350);
      let ac = P.alphaCx * fnutr * fT(t) * ffrost * fcal * fphys; if (S.lai === 0) ac = 0;
      let GPP = P.gDM_mol * P.molPAR_MJ * ac * apar / 100, NPP = GPP * P.y;
      const lt = S.lai, lper = lt === 0 ? 0 : S.lai / lt;
      let gC = P.MaxCond; if (lt <= P.LAIgcx) gC = P.MinCond + (P.MaxCond - P.MinCond) * lt / P.LAIgcx;
      const cond = gC * lper * fphys * 1 * fcg;
      let tr = 0;
      if (vpd !== 0) { const d = dl[month - 1], nr = P.Qa + P.Qb * (g("srad", t) * 1e6 / d), def = RHO_AIR * LAMBDA * (VPD_CONV * vpd) * P.BLcond;
        tr = Math.max(0, DIM[month - 1] * cond * (E20 * nr + def) / (cond * (1 + E20) + P.BLcond) / LAMBDA * d); }
      let ifr = P.MaxIntcptn; if (P.LAImaxIntcptn > 0) ifr = P.MaxIntcptn * Math.min(1, lt / P.LAImaxIntcptn) * lper;
      const pint = g("prcp", t) * ifr;
      ASW = ASW + g("prcp", t);
      const et = Math.min(ASW, tr + pint), exc = Math.max(ASW - et - asw_max, 0);
      ASW = ASW - et - exc; if (ASW < asw_min) ASW = asw_min;
      const fts = (tr + pint) === 0 ? 1 : et / (tr + pint);
      GPP *= fts; NPP *= fts; const nppf = NPP, gppf = GPP;
      const trTot = tr; if (trTot > 0 && fts < 1) tr = (et - pint) / trTot * tr;
      const m = P.m0 + (1 - P.m0) * sp.fertility;
      const fr = P.pRx * P.pRn / (P.pRn + (P.pRx - P.pRn) * fphys * m), fs = (1 - fr) / (1 + S.pFS), ff = 1 - fr - fs;
      if (!dorm) {
        if (S.Wf === 0) S.Wf = S.debt;
        if (NPP >= S.debt) { NPP -= S.debt; S.debt = 0; } else { S.debt -= NPP; NPP = 0; }
        const lf_ = gF[t] * S.Wf, lr = P.gammaR * S.Wr;
        S.Wf += NPP * ff - lf_; S.Wr += NPP * fr - lr; S.Ws += NPP * fs;
      }
      upd(t); for (let k = 0; k < B_N; k++) sdc(t);
      if (!dorm && gN[t] > 0) { const ms = Math.min(gN[t] * S.N / 12 / 100, S.N);
        S.Wf -= P.mF * ms * S.Wf / S.N; S.Wr -= P.mR * ms * S.Wr / S.N; S.Ws -= P.mS * ms * S.Ws / S.N; S.N -= ms; bcor = true; }
      if (bcor) { upd(t); for (let k = 0; k < B_N; k++) sdc(t); bcor = false; }
      const btmax = P.wSx1000 * Math.pow(1000 / S.N, P.thinPower);
      if (!dorm && btmax < S.bt) {
        const mt_ = mortality(S.N, S.Ws, P.mS, P.wSx1000, P.thinPower);
        if (mt_ < S.N) { S.Wf -= P.mF * mt_ * S.Wf / S.N; S.Wr -= P.mR * mt_ * S.Wr / S.N; S.Ws -= P.mS * mt_ * S.Ws / S.N; S.N -= mt_; }
        else Object.assign(S, { Wf: 0, Wr: 0, Ws: 0, N: 0 });
        upd(t); for (let k = 0; k < B_N; k++) sdc(t);
      }
      rec(t, { fsw, npp: nppf, rem, gpp: gppf, apar, alpha: ac, fVPD: fvpd, phys: fphys, transp: tr, et, prcp: g("prcp", t), etaR: fr, etaS: fs, etaF: ff });
    }
    return out;
  }
  root.Modelo3PG = { run };
  if (typeof module !== "undefined") module.exports = { run };
})(typeof window !== "undefined" ? window : globalThis);
