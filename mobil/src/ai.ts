// AREX — yapay zekâ istemcisi: Groq → Gemini → OpenRouter(:free) → Pollinations zinciri,
// Gemini görsel/video analizi, doğal anlatıcı sesi (Gemini TTS), Whisper ses tanıma, Live geçici token.
import { Platform } from "react-native";
import { anahtar } from "./depo";

export type Rol = { role: "system" | "user" | "assistant"; content: string };

const kota: Record<string, number> = {};
export const sonHatalar: Record<string, string> = {};

async function zamanliFetch(url: string, init: RequestInit, ms: number) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { ...init, signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

const temizle = (t: string) =>
  (t || "").replace(/<think>[\s\S]*?<\/think>/g, "").replace(/^\s*(?:🤖|🧠)\s*\*\*AREX AI[^*\n]*\*\*\s*/gm, "").trim();

async function openaiUyumlu(saglayici: string, url: string, key: string, model: string, mesajlar: any[], sicaklik: number,
  maks: number, ms: number, ek: Record<string, string> = {}): Promise<string | null> {
  const k = saglayici + ":" + model;
  if ((kota[k] || 0) > Date.now()) return null;
  const govde: any = { model, messages: mesajlar, temperature: sicaklik, max_tokens: maks };
  if (model.includes("gpt-oss")) govde.reasoning_effort = "low";
  try {
    const r = await zamanliFetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + key, ...ek },
      body: JSON.stringify(govde),
    }, ms);
    if (!r.ok) {
      sonHatalar[saglayici] = `HTTP ${r.status} (${model})`;
      if (r.status === 429) kota[k] = Date.now() + 60_000;
      if (r.status === 401 || r.status === 403) kota[k] = Date.now() + 600_000;
      return null;
    }
    const j = await r.json();
    const metin = temizle(j?.choices?.[0]?.message?.content || "");
    if (metin) sonHatalar[saglayici] = "OK " + model;
    return metin || null;
  } catch (e: any) {
    sonHatalar[saglayici] = (e?.name || "hata") + " " + model;
    return null;
  }
}

const GROQ = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"];
const GEMINI_METIN = ["gemini-3.5-flash-lite", "gemini-3.5-flash"];
const OPENROUTER = ["openrouter/free", "nvidia/nemotron-3-ultra-550b-a55b:free", "google/gemma-4-31b-it:free"];

export async function sohbetTamamla(mesajlar: Rol[], opt: { sistem?: string; sicaklik?: number; maks?: number; tercih?: "gemini" | "groq" | "" } = {}):
  Promise<{ metin: string | null; motor: string }> {
  const { sistem = "", sicaklik = 0.75, maks = 1800, tercih = "" } = opt;
  const tam = [...(sistem ? [{ role: "system", content: sistem }] : []), ...mesajlar.filter((m) => m.content)];
  const groq = async () => {
    const k = anahtar("GROQ_API_KEY");
    if (!k) return null;
    for (const m of GROQ) {
      const t = await openaiUyumlu("groq", "https://api.groq.com/openai/v1/chat/completions", k, m, tam, sicaklik, Math.min(maks, 2500), 30_000);
      if (t) return { metin: t, motor: "Groq " + m.split("/").pop() };
    }
    return null;
  };
  const gemini = async () => {
    const k = anahtar("GEMINI_API_KEY");
    if (!k) return null;
    for (const m of GEMINI_METIN) {
      const t = await openaiUyumlu("gemini", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", k, m, tam, sicaklik, maks, 45_000);
      if (t) return { metin: t, motor: "Gemini " + m.replace("gemini-", "") };
    }
    return null;
  };
  const openrouter = async () => {
    const k = anahtar("OPENROUTER_API_KEY");
    if (!k) return null;
    for (const m of OPENROUTER) {
      const t = await openaiUyumlu("openrouter", "https://openrouter.ai/api/v1/chat/completions", k, m, tam, sicaklik, maks, 40_000, { "X-Title": "AREX AI" });
      if (t) return { metin: t, motor: "OpenRouter " + m.split("/").pop()!.replace(":free", "") };
    }
    return null;
  };
  const pollinations = async () => {
    const t = await openaiUyumlu("pollinations", "https://text.pollinations.ai/openai", "anon", "openai-fast", tam, sicaklik, maks, 40_000);
    return t ? { metin: t, motor: "Pollinations" } : null;
  };
  const sira = tercih === "gemini" ? [gemini, groq, openrouter, pollinations] : [groq, gemini, openrouter, pollinations];
  for (const f of sira) {
    const s = await f();
    if (s) return s;
  }
  return { metin: null, motor: "" };
}

// ---------- Görsel / video analizi (Gemini, yedek OpenRouter görsel) ----------
export async function medyaAnaliz(b64: string, mime: string, talimat: string, opt: { sistem?: string; gecmis?: Rol[]; derin?: boolean; maks?: number } = {}):
  Promise<{ metin: string | null; motor: string }> {
  const { sistem = "", gecmis = [], derin = false, maks = 2500 } = opt;
  const k = anahtar("GEMINI_API_KEY");
  if (k) {
    const icerik: any[] = gecmis.slice(-6).filter((m) => m.role !== "system").map((m) => ({
      role: m.role === "user" ? "user" : "model", parts: [{ text: m.content.slice(0, 1500) }],
    }));
    icerik.push({ role: "user", parts: [{ inline_data: { mime_type: mime, data: b64 } }, { text: talimat }] });
    const govde: any = { contents: icerik, generationConfig: { temperature: 0.4, maxOutputTokens: maks } };
    if (sistem) govde.systemInstruction = { parts: [{ text: sistem }] };
    const modeller = derin ? ["gemini-3.5-flash", "gemini-3.5-flash-lite"] : ["gemini-3.5-flash-lite", "gemini-3.5-flash"];
    for (const m of modeller) {
      if ((kota["gemini:" + m] || 0) > Date.now()) continue;
      try {
        const r = await zamanliFetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, {
          method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": k }, body: JSON.stringify(govde),
        }, mime.startsWith("video") ? 120_000 : 70_000);
        if (r.status === 429) { kota["gemini:" + m] = Date.now() + 60_000; continue; }
        if (!r.ok) { sonHatalar.gemini = "HTTP " + r.status; continue; }
        const j = await r.json();
        const t = temizle((j?.candidates?.[0]?.content?.parts || []).map((p: any) => p.text || "").join(""));
        if (t) return { metin: t, motor: "Gemini " + m.replace("gemini-", "") };
      } catch (e: any) {
        sonHatalar.gemini = e?.name || "hata";
      }
    }
  }
  const ork = anahtar("OPENROUTER_API_KEY");
  if (ork && mime.startsWith("image")) {
    const mesaj = [...(sistem ? [{ role: "system", content: sistem }] : []), {
      role: "user", content: [{ type: "text", text: talimat }, { type: "image_url", image_url: { url: `data:${mime};base64,${b64}` } }],
    }];
    for (const m of ["nvidia/nemotron-3.5-super-vl:free", "google/gemma-4-31b-it:free"]) {
      const t = await openaiUyumlu("openrouter", "https://openrouter.ai/api/v1/chat/completions", ork, m, mesaj, 0.4, maks, 70_000);
      if (t) return { metin: t, motor: "OpenRouter görsel" };
    }
  }
  return { metin: null, motor: k || ork ? "Görsel analiz servisine şu an ulaşılamadı." : "Gemini anahtarı gerekli (⚙️ Ayarlar)." };
}

// ---------- Doğal anlatıcı sesi (Gemini TTS → WAV base64) ----------
export const ANLATICILAR: Record<string, { ad: string; ses: string }> = {
  masalci: { ad: "🧚 Masal Perisi", ses: "Leda" },
  anne: { ad: "👩 Sıcak Anne", ses: "Sulafat" },
  dede: { ad: "👴 Dede Masalcı", ses: "Algieba" },
  neseli: { ad: "😄 Neşeli", ses: "Puck" },
  fisilti: { ad: "🌙 Uyku Fısıltısı", ses: "Achernar" },
  abla: { ad: "👧 Abla", ses: "Aoede" },
};
export const USLUPLAR: Record<string, string> = {
  masal: "Sıcak, merak uyandıran, usta bir masalcı gibi; cümle aralarında doğal duraksamalarla, karakterlerin konuşmalarında hafifçe farklı ses tonları kullanarak, gülümseyerek anlat",
  uyku: "Çok yavaş, yumuşacık, fısıltıya yakın ve huzurlu bir sesle; uzun nefesli duraksamalarla, uyutacak gibi anlat",
  komik: "Neşeli, enerjik ve şakacı; komik yerlerde gülümseyen bir tonla, karakterlere eğlenceli sesler vererek anlat",
  macera: "Heyecanlı ama sevecen; merak anlarında yavaşlayıp, sürprizlerde canlanan bir tonla anlat",
  sohbet: "Doğal, samimi ve sevecen bir arkadaş gibi konuş",
  bilgi: "Açık, anlaşılır, sıcak bir öğretmen gibi anlat",
};

function parcala(metin: string, sinir = 1400): string[] {
  const out: string[] = [];
  let cur = "";
  for (let p of metin.split(/\n+/)) {
    p = p.trim();
    if (!p) continue;
    if (cur.length + p.length + 2 > sinir && cur) { out.push(cur); cur = ""; }
    while (p.length > sinir) {
      let kes = p.lastIndexOf(". ", sinir);
      kes = kes > 200 ? kes + 1 : sinir;
      out.push(p.slice(0, kes));
      p = p.slice(kes).trim();
    }
    cur = (cur + "\n\n" + p).trim();
  }
  if (cur) out.push(cur);
  return out.slice(0, 8);
}

function b64Bayt(b64: string): Uint8Array {
  const bin = globalThis.atob(b64);
  const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  return u;
}
export function baytB64(u: Uint8Array): string {
  let s = "";
  for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, Array.from(u.subarray(i, i + 0x8000)));
  return globalThis.btoa(s);
}
function wavBaslik(pcmUzunluk: number, hz = 24000): Uint8Array {
  const b = new ArrayBuffer(44);
  const v = new DataView(b);
  const yaz = (o: number, s: string) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  yaz(0, "RIFF"); v.setUint32(4, 36 + pcmUzunluk, true); yaz(8, "WAVE"); yaz(12, "fmt ");
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true); v.setUint32(24, hz, true);
  v.setUint32(28, hz * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); yaz(36, "data"); v.setUint32(40, pcmUzunluk, true);
  return new Uint8Array(b);
}

export function seseUygun(metin: string) {
  return (metin || "").replace(/[#*_`>|]/g, "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/\n{2,}/g, "\n").trim().slice(0, 4500);
}

/** Gemini doğal ses → WAV baytları; olmazsa null (çağıran cihaz sesine düşer). */
export async function dogalSes(metin: string, uslup = "masal", anlatici = "masalci"): Promise<Uint8Array | null> {
  const k = anahtar("GEMINI_API_KEY");
  if (!k || (kota["gemini:tts"] || 0) > Date.now()) return null;
  const ses = (ANLATICILAR[anlatici] || ANLATICILAR.masalci).ses;
  const talimat = USLUPLAR[uslup] || USLUPLAR.masal;
  try {
    const parcalar = await Promise.all(parcala(seseUygun(metin)).map(async (p) => {
      const r = await zamanliFetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent", {
        method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": k },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `${talimat}:\n\n${p}` }] }],
          generationConfig: { responseModalities: ["AUDIO"], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: ses } } } },
        }),
      }, 120_000);
      if (r.status === 429) { kota["gemini:tts"] = Date.now() + 300_000; throw new Error("kota"); }
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      return b64Bayt(j.candidates[0].content.parts[0].inlineData.data);
    }));
    const sessizlik = new Uint8Array(24000); // 0,5 sn nefes
    const toplam = parcalar.reduce((a, p) => a + p.length, 0) + sessizlik.length * (parcalar.length - 1);
    const out = new Uint8Array(44 + toplam);
    out.set(wavBaslik(toplam), 0);
    let o = 44;
    parcalar.forEach((p, i) => { out.set(p, o); o += p.length; if (i < parcalar.length - 1) o += sessizlik.length; });
    return out;
  } catch (e: any) {
    sonHatalar.tts = e?.message || "hata";
    return null;
  }
}

// ---------- Ses → yazı (Groq Whisper) ----------
export async function sesiYaziyaDok(uri: string): Promise<string> {
  const k = anahtar("GROQ_API_KEY");
  if (!k) return "";
  const form = new FormData();
  if (Platform.OS === "web") {
    const blob = await (await fetch(uri)).blob();
    form.append("file", blob, "ses.webm");
  } else {
    form.append("file", { uri, name: "ses.m4a", type: "audio/m4a" } as any);
  }
  form.append("model", "whisper-large-v3-turbo");
  try {
    const r = await zamanliFetch("https://api.groq.com/openai/v1/audio/transcriptions", {
      method: "POST", headers: { Authorization: "Bearer " + k }, body: form,
    }, 60_000);
    if (!r.ok) return "";
    return ((await r.json()).text || "").trim();
  } catch {
    return "";
  }
}

// ---------- Gemini Live geçici token ----------
export async function canliToken(dakika = 30): Promise<string> {
  const k = anahtar("GEMINI_API_KEY");
  if (!k) return "";
  const bitis = new Date(Date.now() + dakika * 60_000).toISOString().replace(/\.\d+Z$/, "Z");
  try {
    const r = await zamanliFetch("https://generativelanguage.googleapis.com/v1alpha/auth_tokens", {
      method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": k },
      body: JSON.stringify({ uses: 20, expireTime: bitis, newSessionExpireTime: bitis }),
    }, 20_000);
    if (!r.ok) return "";
    return (await r.json()).name || "";
  } catch {
    return "";
  }
}

// ---------- Ücretsiz açık kaynak bağlam araçları ----------
export async function wikipediaOzet(konu: string, dil = "tr"): Promise<string> {
  try {
    const r = await zamanliFetch(`https://${dil}.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(konu.trim().replace(/\s+/g, "_"))}`,
      { headers: { Accept: "application/json" } }, 8000);
    if (!r.ok) return "";
    const j = await r.json();
    return j.extract ? `Wikipedia (${j.title}): ${j.extract}` : "";
  } catch {
    return "";
  }
}

export async function havaDurumu(sehir: string): Promise<string> {
  try {
    const g = await (await zamanliFetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(sehir)}&count=1&language=tr`, {}, 8000)).json();
    const y = g?.results?.[0];
    if (!y) return "";
    const h = await (await zamanliFetch(`https://api.open-meteo.com/v1/forecast?latitude=${y.latitude}&longitude=${y.longitude}&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=3`, {}, 8000)).json();
    return `Open-Meteo canlı veri — ${y.name} (${y.country}): şu an ${h.current.temperature_2m}°C (hissedilen ${h.current.apparent_temperature}°C), nem %${h.current.relative_humidity_2m}, rüzgâr ${h.current.wind_speed_10m} km/s, hava kodu ${h.current.weather_code}. 3 gün: ` +
      h.daily.time.map((t: string, i: number) => `${t}: ${h.daily.temperature_2m_min[i]}–${h.daily.temperature_2m_max[i]}°C, yağış ihtimali %${h.daily.precipitation_probability_max[i]}`).join("; ");
  } catch {
    return "";
  }
}
