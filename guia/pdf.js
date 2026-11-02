const { chromium } = require("playwright"); const path = require("path");
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + path.join(__dirname, "guia.html")); await p.waitForTimeout(800);
  await p.pdf({ path: path.join(__dirname, "Guia_ilustrado_TCC_II_passo_a_passo.pdf"), format: "A4", printBackground: true,
    displayHeaderFooter: true, headerTemplate: "<span></span>",
    footerTemplate: '<div style="font-size:8px;color:#5b6152;width:100%;text-align:center;font-family:Inter,sans-serif">Guia ilustrado do TCC II · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
    margin: { top: "16mm", bottom: "18mm", left: "17mm", right: "17mm" } });
  await b.close(); })();
