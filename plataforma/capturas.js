// Capturas da plataforma para o TCC (Figuras 11 e 12): IND, A1, dois ataques de 95%, compensação calibrada.
const { chromium } = require("playwright"); const path = require("path");
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 1.5 });
  await pg.goto("file://" + path.join(__dirname, "simulador_3pg_eucalyptus.html")); await pg.waitForTimeout(1500);
  await pg.evaluate(() => { const b = document.querySelector("#tour-sair"); if (b) b.click(); });
  await pg.evaluate(() => { document.querySelectorAll("dialog[open]").forEach(d => d.close());
    Object.assign(E, { sitio: "IND", mat: "A1", agua: "LOC", fert: 100, d: 95, freq: "P2", epoca: 1, comp: "C", r: 0, m: 0, ag: "" }); atualizar(); irPara(54); });
  await pg.waitForTimeout(2500);
  await pg.screenshot({ path: path.join(__dirname, "fig_akademia_v8.png") });
  await pg.evaluate(() => irPara(84)); await pg.waitForTimeout(800);
  await pg.click("#bt-toras"); await pg.waitForTimeout(800);
  await pg.evaluate(() => document.querySelector('#cub-abas [data-a="tor"]').click());
  await pg.evaluate(() => document.querySelector('#tor-tal [data-t="t"]').click());
  await pg.waitForTimeout(800);
  const dlg = pg.locator("#m-cubagem > .pr");
  await pg.setViewportSize({ width: 900, height: 1400 }); await pg.waitForTimeout(500);
  await dlg.screenshot({ path: path.join(__dirname, "fig_akademia_toras.png") });  // recortado a 1320 px de altura depois (PIL)
  console.log(await pg.evaluate(() => [R.t.vol[R.idade.indexOf(84)], R.c.vol[R.idade.indexOf(84)]]));
  await b.close();
})();
