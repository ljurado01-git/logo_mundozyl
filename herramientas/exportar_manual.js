// Exporta el manual a PDF (A4 horizontal) y los mockups a PNG.
// Uso: node herramientas/exportar_manual.js
// Requiere Playwright (npm i -g playwright) con Chromium disponible.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const raiz = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(raiz, "manual", "manual_de_marca_mundozyl.html"), "utf8");
const pagina = `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>${html}</body></html>`;

(async () => {
  const navegador = await chromium.launch();
  const p = await navegador.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });
  await p.setContent(pagina, { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);

  const dirMock = path.join(raiz, "manual", "mockups");
  fs.mkdirSync(dirMock, { recursive: true });
  for (const id of ["mock-web", "mock-tarjeta", "mock-redes", "mock-papeleria"]) {
    await p.locator(`#${id}`).screenshot({ path: path.join(dirMock, `${id.replace("mock-", "mockup_")}.png`) });
  }
  // vista previa de cada lámina
  const dirPrev = path.join(raiz, "manual", "laminas");
  fs.mkdirSync(dirPrev, { recursive: true });
  const laminas = p.locator(".lamina");
  const n = await laminas.count();
  for (let i = 0; i < n; i++) {
    await laminas.nth(i).screenshot({ path: path.join(dirPrev, `lamina_${String(i + 1).padStart(2, "0")}.png`) });
  }

  await p.emulateMedia({ media: "print" });
  await p.pdf({ path: path.join(raiz, "manual", "manual_de_marca_mundozyl.pdf"), preferCSSPageSize: true, printBackground: true });
  await navegador.close();
  console.log(`Listo: ${n} láminas, PDF y mockups`);
})();
