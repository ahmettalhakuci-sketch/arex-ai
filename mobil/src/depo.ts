// AREX — kalıcı depolama: API anahtarları (güvenli depo), sohbetler, profil, kitaplık
import AsyncStorage from "@react-native-async-storage/async-storage";
import Constants from "expo-constants";
import { Platform } from "react-native";

export type AnahtarAdi = "GROQ_API_KEY" | "GEMINI_API_KEY" | "OPENROUTER_API_KEY";
export const ANAHTAR_ADLARI: Record<AnahtarAdi, string> = {
  GROQ_API_KEY: "⚡ Groq",
  GEMINI_API_KEY: "💎 Google Gemini",
  OPENROUTER_API_KEY: "🔀 OpenRouter",
};

const VARSAYILAN: Partial<Record<AnahtarAdi, string>> = (Constants.expoConfig?.extra as any)?.anahtarlar || {};
const onbellek: Partial<Record<AnahtarAdi, string>> = {};

async function guvenliOku(ad: string): Promise<string | null> {
  if (Platform.OS === "web") {
    try { return globalThis.localStorage?.getItem("arex_" + ad) ?? null; } catch { return null; }
  }
  const SecureStore = await import("expo-secure-store");
  return SecureStore.getItemAsync(ad);
}

async function guvenliYaz(ad: string, deger: string | null) {
  if (Platform.OS === "web") {
    try { deger ? globalThis.localStorage?.setItem("arex_" + ad, deger) : globalThis.localStorage?.removeItem("arex_" + ad); } catch {}
    return;
  }
  const SecureStore = await import("expo-secure-store");
  if (deger) await SecureStore.setItemAsync(ad, deger);
  else await SecureStore.deleteItemAsync(ad);
}

export async function anahtarlariYukle() {
  for (const ad of Object.keys(ANAHTAR_ADLARI) as AnahtarAdi[]) {
    const kayitli = await guvenliOku(ad).catch(() => null);
    onbellek[ad] = (kayitli || VARSAYILAN[ad] || "").trim();
  }
  return { ...onbellek };
}

export function anahtar(ad: AnahtarAdi): string {
  return (onbellek[ad] || VARSAYILAN[ad] || "").trim();
}

export async function anahtarKaydet(ad: AnahtarAdi, deger: string) {
  const temiz = (deger || "").trim().replace(/^["']|["']$/g, "");
  onbellek[ad] = temiz || VARSAYILAN[ad] || "";
  await guvenliYaz(ad, temiz || null);
}

export const maskele = (d: string) => (d && d.length > 10 ? d.slice(0, 4) + "••••••••" + d.slice(-3) : d ? "••••" : "");

// ---------- Genel JSON depo ----------
export async function oku<T>(anahtarAd: string, varsayilan: T): Promise<T> {
  try {
    const v = await AsyncStorage.getItem(anahtarAd);
    return v ? (JSON.parse(v) as T) : varsayilan;
  } catch {
    return varsayilan;
  }
}
export async function yaz(anahtarAd: string, deger: unknown) {
  try { await AsyncStorage.setItem(anahtarAd, JSON.stringify(deger)); } catch {}
}

// ---------- Sohbet modeli ----------
export type Mesaj = {
  id: string;
  rol: "user" | "assistant";
  metin: string;
  gorsel?: string; // küçük önizleme (data URI veya dosya uri)
  video?: string;
  etiket?: string;
  zaman: number;
};
export type Sohbet = { id: string; baslik: string; mesajlar: Mesaj[]; guncel: number };

export const yeniId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

export async function sohbetleriOku(): Promise<Sohbet[]> {
  return oku<Sohbet[]>("arex_sohbetler", []);
}
export async function sohbetKaydet(s: Sohbet) {
  const liste = (await sohbetleriOku()).filter((x) => x.id !== s.id);
  const hafif = { ...s, mesajlar: s.mesajlar.slice(-120) };
  await yaz("arex_sohbetler", [hafif, ...liste].slice(0, 50));
}
export async function sohbetSil(id: string) {
  await yaz("arex_sohbetler", (await sohbetleriOku()).filter((x) => x.id !== id));
}

// ---------- Profil / hafıza ----------
export type Profil = {
  ad: string;
  hakkinda: string;
  ilgi: string;
  hedef: string;
  tarz: string;
  diller: string;
  notlar: { metin: string; tarih: string }[];
};
export const VARSAYILAN_PROFIL: Profil = {
  ad: "Ahmet",
  hakkinda: "İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi; TEKNOFEST İHA ve TÜBİTAK akıllı bebek arabası projeleri geliştiriyor.",
  ilgi: "yapay zekâ, İHA, robotik, matematik, yazılım",
  hedef: "",
  tarz: "samimi, net, gerektiğinde detaylı",
  diller: "Türkçe, İngilizce, Arapça, Bengalce",
  notlar: [],
};
export async function profilOku(): Promise<Profil> {
  return { ...VARSAYILAN_PROFIL, ...(await oku<Partial<Profil>>("arex_profil", {})) };
}
export async function profilKaydet(p: Profil) {
  await yaz("arex_profil", p);
}
export async function notEkle(metin: string): Promise<boolean> {
  const t = metin.replace(/\s+/g, " ").trim().replace(/[.!]+$/, "");
  if (t.length < 3) return false;
  const p = await profilOku();
  if (p.notlar.some((n) => n.metin.toLowerCase() === t.toLowerCase())) return false;
  p.notlar = [...p.notlar, { metin: t.slice(0, 200), tarih: new Date().toLocaleDateString("tr-TR") }].slice(-60);
  await profilKaydet(p);
  return true;
}

const OGRENME: [RegExp, (m: RegExpMatchArray) => string][] = [
  [/^(?:hatırla|hatirla|unutma|aklında tut)\s*[:\-,]?\s*(.{3,180})$/i, (m) => m[1]],
  [/\b(?:benim adım|adım)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,20})\b/, (m) => "Adı: " + m[1]],
  [/\b(?:doğum günüm)\s+(.{3,40}?)(?:[.!,]|$)/i, (m) => "Doğum günü: " + m[1]],
  [/^(?:ben\s+)?(.{3,40}?)\s+(?:çok\s+)?(?:seviyorum|bayılırım|bayılıyorum)(?:[.!]|$)/i, (m) => "Sevdiği şey: " + m[1]],
  [/^(?:ben\s+)?(.{3,40}?)\s+(?:sevmem|sevmiyorum)(?:[.!]|$)/i, (m) => "Sevmediği şey: " + m[1]],
  [/\b(\d{1,2})\s*yaşındayım\b/i, (m) => m[1] + " yaşında"],
];
export async function sohbettenOgren(mesaj: string): Promise<string> {
  const t = (mesaj || "").trim();
  if (!t || t.length > 220 || t.includes("?")) return "";
  for (const [re, f] of OGRENME) {
    const m = t.match(re);
    if (m) {
      const notu = f(m).trim();
      if (notu.startsWith("Adı: ")) {
        const p = await profilOku();
        p.ad = notu.slice(5);
        await profilKaydet(p);
      }
      return (await notEkle(notu)) ? notu : "";
    }
  }
  return "";
}
export async function profilOzeti(): Promise<string> {
  const p = await profilOku();
  const s: string[] = [];
  if (p.ad) s.push("Adı: " + p.ad);
  if (p.hakkinda) s.push("Hakkında: " + p.hakkinda);
  if (p.ilgi) s.push("İlgi alanları: " + p.ilgi);
  if (p.hedef) s.push("Hedefleri: " + p.hedef);
  if (p.diller) s.push("Diller: " + p.diller);
  if (p.tarz) s.push("Cevap tarzı: " + p.tarz);
  const n = p.notlar.slice(-15).map((x) => x.metin);
  if (n.length) s.push("Kendisi hakkında söyledikleri: " + n.join("; "));
  return s.join(" | ").slice(0, 900);
}

// ---------- Kitaplık (çocuk hikâyeleri) ----------
export type KitapKaydi = { id: string; baslik: string; metin: string; yas: string; dil: string; tur: string; tarih: string };
export async function kitaplikOku() {
  return oku<KitapKaydi[]>("arex_kitaplik", []);
}
export async function kitapligaEkle(k: Omit<KitapKaydi, "id" | "tarih">) {
  const l = await kitaplikOku();
  await yaz("arex_kitaplik", [{ ...k, id: yeniId(), tarih: new Date().toLocaleString("tr-TR") }, ...l].slice(0, 200));
}
export async function kitapliktanSil(id: string) {
  await yaz("arex_kitaplik", (await kitaplikOku()).filter((k) => k.id !== id));
}

// ---------- 📝 Notlarım ----------
export type Not = { no: number; metin: string; tarih: string; kaynak: string };
export async function notlariOku(): Promise<Not[]> {
  return oku<Not[]>("arex_notlarim", []);
}
export async function notKaydet(metin: string, kaynak = "sohbet"): Promise<Not> {
  const l = await notlariOku();
  const n: Not = { no: (l.reduce((m, x) => Math.max(m, x.no), 0) || 0) + 1, metin: metin.trim().slice(0, 4000), tarih: new Date().toLocaleString("tr-TR"), kaynak };
  await yaz("arex_notlarim", [...l, n]);
  return n;
}
export async function notuSil(no: number): Promise<boolean> {
  const l = await notlariOku();
  const y = l.filter((x) => x.no !== no);
  await yaz("arex_notlarim", y);
  return y.length !== l.length;
}
const kisalt = (t: string, n = 140) => { const s = t.replace(/[#*`>|]/g, "").replace(/\s+/g, " ").trim(); return s.length > n ? s.slice(0, n) + "…" : s; };

/** Sohbet not komutları: "notlarıma kaydet: …", "not al …", "bunu not al", "notlarım", "3. notu sil", "notlarımda X ara" */
export async function notKomutu(metin: string, sonCevap: string): Promise<string | null> {
  const t = metin.trim();
  const tl = t.toLocaleLowerCase("tr");
  if (/^(?:notlar[ıi]m|notlar[ıi]m[ıi]\s+(?:göster|listele|oku|aç)|notlar[ıi]ma\s+bak)[.!?]*$/.test(tl)) {
    const l = await notlariOku();
    if (!l.length) return "📝 Henüz notun yok. *\"notlarıma kaydet: …\"* yazarak ya da 🎙️ ile söyleyerek ekleyebilirsin.";
    return "### 📝 Notlarım\n\n" + l.slice(-25).reverse().map((n) => `**${n.no}.** ${kisalt(n.metin)}  _(${n.tarih})_`).join("\n\n") + "\n\n_Silmek için: \"3. notu sil\"_";
  }
  let m = tl.match(/notlar[ıi]mda\s+(.+?)\s+(?:ara|bul)/);
  if (m) {
    const b = (await notlariOku()).filter((n) => n.metin.toLocaleLowerCase("tr").includes(m![1]));
    return b.length ? "### 🔎 Bulunan notlar\n\n" + b.map((n) => `**${n.no}.** ${kisalt(n.metin, 200)}`).join("\n\n") : `🔎 Notlarında **${m[1]}** geçen bir şey yok.`;
  }
  m = tl.match(/(?:^|\s)(\d+)\s*\.?\s*not(?:u|umu)?\s+sil|not(?:u|umu)?\s+sil\s*(\d+)/);
  if (m && tl.includes("sil")) {
    const no = Number(m[1] || m[2]);
    return (await notuSil(no)) ? `🗑️ ${no}. notu sildim.` : `❓ ${no} numaralı not yok.`;
  }
  const bunu = /^(?:bunu|bunları|şunu|son cevabı|cevabı)?$/i;
  let icerik: string | null = null;
  const bas = t.match(/^(?:lütfen\s+)?(?:notlar[ıi]ma\s+(?:kaydet|ekle|yaz|al)|not(?:larıma)?\s+(?:al|et|ekle|kaydet|düş)|(?:şunu|bunu|bunları)\s+(?:notlar[ıi]ma\s+(?:kaydet|ekle)|not\s+(?:al|et))|yeni\s+not)\s*[:\-,]?\s*([\s\S]*)$/i);
  if (bas) icerik = bunu.test(bas[1].trim()) ? sonCevap : bas[1].trim();
  else {
    const son = t.match(/^([\s\S]+?)\s*(?:diye\s+)?(?:notlar[ıi]ma\s+(?:kaydet|ekle|yaz)|not\s+(?:al|et))[.!]?$/i);
    if (son) icerik = bunu.test(son[1].trim()) ? sonCevap : son[1].trim();
  }
  if (icerik === null) return null;
  if (!icerik) return "📝 Neyi not almamı istersin? Ör: *\"notlarıma kaydet: cuma fizik sınavı\"*";
  const n = await notKaydet(icerik);
  return `📝 **Notlarına kaydettim (#${n.no})**\n\n> ${kisalt(icerik, 300)}\n\n_Görmek için: "notlarım"_`;
}
