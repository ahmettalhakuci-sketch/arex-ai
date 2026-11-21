// AREX — premium koyu tema ve ortak sabitler
export const R = {
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

export const GRADYAN = ["#7c5cff", "#22d3ee"] as const;
export const ARKA_GRADYAN = ["#1a1550", "#0b1030", "#050816"] as const;

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
