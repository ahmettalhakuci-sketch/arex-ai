// AREX — premium koyu tema ve ortak sabitler
export const R: Record<string, any> = {
  balon: "rgba(124,92,255,0.42)",
  hap: "rgba(124,92,255,0.45)",
  olcek: 1,
  bg1: "#050816",
  bg2: "#0b1030",
  bg3: "#151a45",
  kart: "rgba(255,255,255,0.06)",
  kartKoyu: "rgba(10,14,40,0.72)",
  cizgi: "rgba(255,255,255,0.12)",
  yazi: "#eef2ff",
  soluk: "#9aa3c7",
  acc: "#7c5cff",
  acc2: "#22d3ee",
  yesil: "#2ee59d",
  kirmizi: "#ff4d6d",
  sari: "#ffc145",
};

export const GRADYAN: [string, string] = ["#7c5cff", "#22d3ee"];
export const ARKA_GRADYAN: [string, string, string] = ["#1a1550", "#0b1030", "#050816"];

export const DILLER: Record<string, { ad: string; bayrak: string; speech: string }> = {
  tr: { ad: "Türkçe", bayrak: "🇹🇷", speech: "tr-TR" },
  en: { ad: "English", bayrak: "🇬🇧", speech: "en-US" },
  bn: { ad: "বাংলা", bayrak: "🇧🇩", speech: "bn-BD" },
  ar: { ad: "العربية", bayrak: "🇸🇦", speech: "ar-SA" },
  ru: { ad: "Русский", bayrak: "🇷🇺", speech: "ru-RU" },
  de: { ad: "Deutsch", bayrak: "🇩🇪", speech: "de-DE" },
  fr: { ad: "Français", bayrak: "🇫🇷", speech: "fr-FR" },
  es: { ad: "Español", bayrak: "🇪🇸", speech: "es-ES" },
  az: { ad: "Azərbaycan", bayrak: "🇦🇿", speech: "az-AZ" },
  ur: { ad: "اردو", bayrak: "🇵🇰", speech: "ur-PK" },
  hi: { ad: "हिन्दी", bayrak: "🇮🇳", speech: "hi-IN" },
  zh: { ad: "中文", bayrak: "🇨🇳", speech: "zh-CN" },
  ja: { ad: "日本語", bayrak: "🇯🇵", speech: "ja-JP" },
  fa: { ad: "فارسی", bayrak: "🇮🇷", speech: "fa-IR" },
  uk: { ad: "Українська", bayrak: "🇺🇦", speech: "uk-UA" },
  it: { ad: "Italiano", bayrak: "🇮🇹", speech: "it-IT" },
  pt: { ad: "Português", bayrak: "🇧🇷", speech: "pt-BR" },
  id: { ad: "Indonesia", bayrak: "🇮🇩", speech: "id-ID" },
};

export const RTL_DILLER = new Set(["ar", "ur", "fa"]);

export function yazidanDilTahmin(metin: string): string {
  const t = metin || "";
  if (/[ঀ-৿]/.test(t)) return "bn";
  if (/[؀-ۿ]/.test(t)) return /[پچژگ]/.test(t) ? "fa" : "ar";
  if (/[Ѐ-ӿ]/.test(t)) return /[іїєґ]/i.test(t) ? "uk" : "ru";
  if (/[ऀ-ॿ]/.test(t)) return "hi";
  if (/[぀-ヿ]/.test(t)) return "ja";
  if (/[一-鿿]/.test(t)) return "zh";
  if (/[çğıöşüÇĞİÖŞÜ]/.test(t) || /\b(ve|bir|bu|ne|nasıl|mı|mi|için|ben|sen)\b/i.test(t)) return "tr";
  const k = t.toLowerCase().match(/[a-z']+/g) || [];
  const ing = new Set(["the", "is", "are", "what", "how", "you", "i", "my", "can", "please", "tell", "me", "a", "an", "and", "story", "write", "why", "do", "hello", "hi"]);
  if (k.length >= 3 && k.filter((x) => ing.has(x)).length / k.length >= 0.25) return "en";
  return "";
}

// ---------- Renk temaları (tutarlı ton: arka plan + vurgu + balon aynı aileden) ----------
export const TEMALAR: Record<string, { ad: string; acc: string; acc2: string; arka: [string, string, string]; balon: string; hap: string }> = {
  gece: { ad: "🌌 Gece Moru", acc: "#7c5cff", acc2: "#22d3ee", arka: ["#1a1550", "#0b1030", "#050816"], balon: "rgba(124,92,255,0.42)", hap: "rgba(124,92,255,0.45)" },
  okyanus: { ad: "🌊 Okyanus", acc: "#0ea5e9", acc2: "#2dd4bf", arka: ["#0c2a43", "#071a2c", "#030b14"], balon: "rgba(14,165,233,0.38)", hap: "rgba(14,165,233,0.42)" },
  gul: { ad: "🌸 Gül Altın", acc: "#ec4899", acc2: "#fbbf24", arka: ["#3a1230", "#1c0b1d", "#0b0510"], balon: "rgba(236,72,153,0.36)", hap: "rgba(236,72,153,0.42)" },
  zumrut: { ad: "🌿 Zümrüt", acc: "#10b981", acc2: "#a3e635", arka: ["#0b3327", "#071d17", "#03100c"], balon: "rgba(16,185,129,0.36)", hap: "rgba(16,185,129,0.42)" },
  gunbatimi: { ad: "🌅 Gün Batımı", acc: "#f97316", acc2: "#f43f5e", arka: ["#3d1a0c", "#1f0d08", "#0d0604"], balon: "rgba(249,115,22,0.36)", hap: "rgba(249,115,22,0.42)" },
  safir: { ad: "💎 Safir", acc: "#3b82f6", acc2: "#a78bfa", arka: ["#121d4a", "#0a1230", "#050818"], balon: "rgba(59,130,246,0.40)", hap: "rgba(59,130,246,0.45)" },
};

/** Temayı uygular: ortak renk nesnelerini yerinde günceller (bileşenler yeniden çizildiğinde yeni tonu alır). */
export function temaUygula(kod: string, yaziOlcek = 1) {
  const t = TEMALAR[kod] || TEMALAR.gece;
  R.acc = t.acc; R.acc2 = t.acc2; R.balon = t.balon; R.hap = t.hap; R.olcek = yaziOlcek;
  R.bg1 = t.arka[2]; R.bg2 = t.arka[1]; R.bg3 = t.arka[0];
  GRADYAN[0] = t.acc; GRADYAN[1] = t.acc2;
  ARKA_GRADYAN[0] = t.arka[0]; ARKA_GRADYAN[1] = t.arka[1]; ARKA_GRADYAN[2] = t.arka[2];
}
