// static/*.html → src/gomuluHtml.ts (canlı sohbet + yerel analiz sayfaları uygulamaya gömülür)
const fs = require("fs");
const path = require("path");
const kok = path.join(__dirname, "..", "..", "static");
const oku = (ad) => fs.readFileSync(path.join(kok, ad), "utf8");
const cikti = `// OTOMATİK ÜRETİLDİ (scripts/html-gom.js) — elle düzenleme; kaynak: ../static/*.html
export const CANLI_HTML = ${JSON.stringify(oku("canli.html"))};
export const YEREL_HTML = ${JSON.stringify(oku("yerel_analiz.html"))};
`;
fs.writeFileSync(path.join(__dirname, "..", "src", "gomuluHtml.ts"), cikti);
console.log("gomuluHtml.ts yazıldı:", (cikti.length / 1024).toFixed(0), "KB");
