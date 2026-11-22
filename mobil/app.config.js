// AREX AI — Expo yapılandırması.
// API anahtarları DERLEME ANINDA ~/.arex/anahtarlar.json kasasından okunur; koda/git'e girmez.
// (Uygulama içinden ⚙️ Ayarlar → Anahtarlar ile değiştirilebilir; cihazda güvenli depoda saklanır.)
const fs = require("fs");
const os = require("os");
const path = require("path");

// Anahtarlar APK'ya DÜZ METİN olarak girmez: her derlemede rastgele tuzla SHA-256 akış anahtarıyla XOR'lanıp base64 gömülür.
// Uygulama ilk açılışta çözer ve Android Keystore destekli şifreli depoya (SecureStore) taşır.
const crypto = require("crypto");
function karistir(anahtarlar) {
  const tuz = crypto.randomBytes(16).toString("base64");
  const akis = (uzunluk) => { let b = Buffer.alloc(0), i = 0; while (b.length < uzunluk) b = Buffer.concat([b, crypto.createHash("sha256").update(tuz + ":com.arex.ai:" + i++).digest()]); return b; };
  const out = {};
  for (const [ad, deger] of Object.entries(anahtarlar)) {
    const v = Buffer.from(String(deger), "utf8"), k = akis(v.length);
    out[ad] = Buffer.from(v.map((x, i) => x ^ k[i])).toString("base64");
  }
  return { t: tuz, a: out };
}

function kasaOku() {
  try {
    const veri = JSON.parse(fs.readFileSync(path.join(os.homedir(), ".arex", "anahtarlar.json"), "utf8"));
    const izinli = ["GROQ_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY"];
    return Object.fromEntries(Object.entries(veri).filter(([k]) => izinli.includes(k)));
  } catch (e) {
    return {};
  }
}

module.exports = {
  expo: {
    name: "AREX AI",
    slug: "arex-ai",
    scheme: "arex",
    version: "15.8.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "dark",
    backgroundColor: "#050816",
    ios: { supportsTablet: true, bundleIdentifier: "com.arex.ai",
      infoPlist: { NSMicrophoneUsageDescription: "Sesli sohbet ve canlı konuşma için", NSCameraUsageDescription: "Canlı görüntülü sohbet ve fotoğraf analizi için" } },
    android: {
      package: "com.arex.ai",
      versionCode: 158,
      adaptiveIcon: { backgroundColor: "#0b1030", foregroundImage: "./assets/android-icon-foreground.png" },
      permissions: ["android.permission.RECORD_AUDIO", "android.permission.CAMERA", "android.permission.MODIFY_AUDIO_SETTINGS", "android.permission.INTERNET"],
      predictiveBackGestureEnabled: false,
      softwareKeyboardLayoutMode: "resize",
    },
    web: { favicon: "./assets/favicon.png", name: "AREX AI", backgroundColor: "#050816", themeColor: "#7c5cff" },
    plugins: [
      ["expo-audio", { microphonePermission: "Sesli sohbet için mikrofon kullanılır." }],
      ["expo-camera", { cameraPermission: "Canlı görüntülü sohbet için kamera kullanılır.", microphonePermission: "Canlı sohbet için mikrofon kullanılır." }],
      ["expo-image-picker", { photosPermission: "Fotoğraf ve video analizi için galeri kullanılır.", cameraPermission: "Fotoğraf çekmek için kamera kullanılır." }],
      "expo-secure-store",
      "expo-local-authentication",
      "./plugins/asistan.js",
      "./plugins/ev-agi.js",
      ["expo-build-properties", { android: { usesCleartextTraffic: false } }],
    ],
    extra: { kasa: karistir(kasaOku()), surumKodu: 158 },
  },
};
