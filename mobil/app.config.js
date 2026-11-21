// AREX AI — Expo yapılandırması.
// API anahtarları DERLEME ANINDA ~/.arex/anahtarlar.json kasasından okunur; koda/git'e girmez.
// (Uygulama içinden ⚙️ Ayarlar → Anahtarlar ile değiştirilebilir; cihazda güvenli depoda saklanır.)
const fs = require("fs");
const os = require("os");
const path = require("path");

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
    version: "15.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "dark",
    backgroundColor: "#050816",
    ios: { supportsTablet: true, bundleIdentifier: "com.arex.ai",
      infoPlist: { NSMicrophoneUsageDescription: "Sesli sohbet ve canlı konuşma için", NSCameraUsageDescription: "Canlı görüntülü sohbet ve fotoğraf analizi için" } },
    android: {
      package: "com.arex.ai",
      versionCode: 15,
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
      ["expo-build-properties", { android: { usesCleartextTraffic: false } }],
    ],
    extra: { anahtarlar: kasaOku() },
  },
};
