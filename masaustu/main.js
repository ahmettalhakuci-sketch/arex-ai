// AREX AI — masaüstü (Electron): mobil uygulamanın web paketini gömülü yerel sunucudan açar.
// localhost güvenli bağlam sayıldığı için mikrofon/kamera (Canlı, Yerel Analiz) çalışır.
const { app, BrowserWindow, session, shell, desktopCapturer, systemPreferences } = require("electron");
const http = require("http");
const fs = require("fs");
const path = require("path");

const KOK = path.join(__dirname, "web");
const TURLER = { ".html": "text/html; charset=utf-8", ".js": "application/javascript", ".css": "text/css", ".json": "application/json",
  ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".ico": "image/x-icon", ".ttf": "font/ttf", ".woff2": "font/woff2", ".wasm": "application/wasm" };

function sunucuBaslat() {
  return new Promise((ok) => {
    const sunucu = http.createServer((istek, yanit) => {
      let yol = decodeURIComponent((istek.url || "/").split("?")[0]);
      let dosya = path.normalize(path.join(KOK, yol));
      if (!dosya.startsWith(KOK)) { yanit.writeHead(403); return yanit.end(); }
      if (!fs.existsSync(dosya) || fs.statSync(dosya).isDirectory()) dosya = path.join(KOK, "index.html");  // tek sayfa uygulaması
      yanit.writeHead(200, { "Content-Type": TURLER[path.extname(dosya)] || "application/octet-stream", "Cache-Control": "no-cache" });
      fs.createReadStream(dosya).pipe(yanit);
    });
    sunucu.listen(0, "127.0.0.1", () => ok(sunucu.address().port));
  });
}

async function pencereAc() {
  if (process.platform === "darwin") {
    try { await systemPreferences.askForMediaAccess("microphone"); await systemPreferences.askForMediaAccess("camera"); } catch (e) {}
  }
  const izinli = new Set(["media", "microphone", "camera", "display-capture", "clipboard-sanitized-write", "clipboard-read", "notifications", "fullscreen"]);
  session.defaultSession.setPermissionRequestHandler((_wc, izin, cb) => cb(izinli.has(izin)));
  session.defaultSession.setPermissionCheckHandler((_wc, izin) => izinli.has(izin));
  session.defaultSession.setDisplayMediaRequestHandler((_istek, cb) => {
    desktopCapturer.getSources({ types: ["screen"] }).then((k) => cb(k.length ? { video: k[0] } : {})).catch(() => cb({}));
  });
  const port = await sunucuBaslat();
  const pencere = new BrowserWindow({
    width: 1180, height: 840, minWidth: 380, minHeight: 600, backgroundColor: "#050816", title: "AREX AI",
    titleBarStyle: process.platform === "darwin" ? "hiddenInset" : "default", show: false,
    webPreferences: { contextIsolation: true, sandbox: true, spellcheck: false },
  });
  pencere.once("ready-to-show", () => pencere.show());
  pencere.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: "deny" }; });  // bağlantılar tarayıcıda açılır
  pencere.loadURL(`http://127.0.0.1:${port}/`);
}

app.whenReady().then(pencereAc);
app.on("window-all-closed", () => app.quit());
app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) pencereAc(); });
