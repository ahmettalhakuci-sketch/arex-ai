// AREX — telefon komutları: "YouTube aç", "YouTube'da Yasin tilaveti ara", "WhatsApp aç", "haritada cami göster",
// "05xx… ara", "Spotify'da X çal", "Google'da X ara", "ayarları aç" (uygulama bağlantıları / derin bağlantılar)
import { Linking, Platform } from "react-native";
import * as E from "../modules/arex-erisim";
import { sohbetTamamla } from "./ai";

export type Hedef = "youtube" | "whatsapp" | "instagram" | "telegram" | "spotify" | "gmail" | "harita" | "yol" | "telefon" | "sms" | "google" | "ayarlar";
export const HEDEFLER: Hedef[] = ["youtube", "whatsapp", "instagram", "telegram", "spotify", "gmail", "harita", "yol", "telefon", "sms", "google", "ayarlar"];

const q = (s: string) => encodeURIComponent(s.trim());

async function dene(adresler: string[]): Promise<boolean> {
  for (const a of adresler) {
    try {
      if (Platform.OS === "web") { window.open(a.startsWith("http") ? a : adresler[adresler.length - 1], "_blank"); return true; }
      await Linking.openURL(a);
      return true;
    } catch {}
  }
  return false;
}

/** Bir hedef uygulamayı (isteğe bağlı arama ile) açar. Dönüş: kullanıcıya gösterilecek mesaj. */
export async function acHedef(hedef: Hedef, sorgu = ""): Promise<string> {
  const s = sorgu.trim();
  const tablo: Record<Hedef, [string, string[]]> = {
    youtube: ["▶️ YouTube", s ? [`vnd.youtube://results?search_query=${q(s)}`, `https://www.youtube.com/results?search_query=${q(s)}`] : ["vnd.youtube://", "https://www.youtube.com"]],
    whatsapp: ["💬 WhatsApp", s && /^\+?\d[\d\s]{6,}$/.test(s) ? [`https://wa.me/${s.replace(/\D/g, "").replace(/^0/, "90")}`] : ["whatsapp://send", "https://web.whatsapp.com"]],
    instagram: ["📸 Instagram", ["instagram://app", "https://www.instagram.com"]],
    telegram: ["✈️ Telegram", ["tg://", "https://web.telegram.org"]],
    spotify: ["🎵 Spotify", s ? [`spotify:search:${q(s)}`, `https://open.spotify.com/search/${q(s)}`] : ["spotify://", "https://open.spotify.com"]],
    gmail: ["📧 Gmail", ["googlegmail://", "https://mail.google.com"]],
    harita: ["🗺️ Harita", Platform.OS === "android" ? [`geo:0,0?q=${q(s || "yakınımdaki yerler")}`, `https://www.google.com/maps/search/${q(s)}`] : [`https://www.google.com/maps/search/${q(s)}`]],
    yol: ["🧭 Yol tarifi", Platform.OS === "android" ? [`google.navigation:q=${q(s)}`, `https://www.google.com/maps/dir/?api=1&destination=${q(s)}`] : [`https://www.google.com/maps/dir/?api=1&destination=${q(s)}`]],
    telefon: ["📞 Arama", [`tel:${s.replace(/[^\d+]/g, "")}`]],
    sms: ["✉️ Mesaj", [`sms:${s.replace(/[^\d+]/g, "")}`]],
    google: ["🔎 Google", [`https://www.google.com/search?q=${q(s)}`]],
    ayarlar: ["⚙️ Ayarlar", []],
  };
  if (hedef === "ayarlar") { try { await Linking.openSettings(); return "⚙️ Telefon ayarlarında AREX sayfası açıldı."; } catch { return "⚙️ Ayarlar açılamadı."; } }
  const [ad, adresler] = tablo[hedef];
  const ok = await dene(adresler);
  return ok ? `${ad} açılıyor${s ? `: **${s}**` : ""} ✅` : `${ad} açılamadı — uygulama yüklü olmayabilir.`;
}

const ERISIM_YOK = "♿ Bunun için **AREX erişim izni** gerekli: ⚙️ Ayarlar → 📱 Telefon erişimi → **Erişimi aç** (Erişilebilirlik → AREX AI Asistan).";

/** Erişilebilirlik komutları: ekranı oku/özetle, X'e dokun, yaz, kaydır, geri, ana ekran, bildirimler, kilitle, uygulama aç. Komut değilse null. */
export async function erisimKomutu(metin: string): Promise<string | null> {
  if (Platform.OS !== "android" || !E.destekVar()) return null;
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "");
  let m: RegExpMatchArray | null;
  const gerek = () => E.etkinMi();
  if (/^(?:erişim(?:i)?|telefon erişimi(?:ni)?|erişilebilirlik(?:i)?)\s+(?:aç|ver|etkinleştir)/.test(t)) { E.ayarlariAc(); return "♿ Erişilebilirlik ayarları açıldı → **AREX AI Asistan** → aç."; }
  // Uygulama aç (servis gerekmez): "google aç", "saat uygulamasını aç", "hesap makinesini aç"
  if ((m = t.match(/^(.{2,30}?)(?:'?(?:[ıiuü]|y[ıiuü]|n[ıiuü]))?\s*(?:uygulamas[ıi]n[ıi]\s+)?(?:aç|başlat|açar mısın)$/)) && !/^(?:ekran|bildirim|erişim|sayfa|kur'?an|meal|ezber|pomodoro|kamera izn)/.test(m[1])) {
    const ad = m[1].replace(/\s*uygulama(?:s[ıi])?$/, "").replace(/'(?:[ıiuü]|y[ıiuü]|n[ıiuü])$/, "").trim();
    const acilan = E.uygulamaAc(ad);
    if (acilan) return `📱 **${acilan}** açılıyor ✅`;
    return null;  // bulunamadıysa eski derin bağlantı yoluna düşsün
  }
  const ekranMi = /^ekran(?:ı|da|daki)?\s*(?:ne var|ne yazıyor|oku|özetle|anlat|neler var)|^(?:bu )?ekranı (?:oku|özetle|anlat|açıkla)|^ekranda ne/.test(t);
  if (ekranMi) {
    if (!gerek()) return ERISIM_YOK;
    const metinEkran = E.ekranOku();
    if (!metinEkran.trim()) return "📱 Okunacak başka bir uygulama ekranı yok. Başka bir uygulamadayken **yan tuşa basılı tut** → kartta **📖 Ekranı özetle**.";
    if (/özetle|anlat|açıkla|ne var|neler/.test(t)) {
      const r = await sohbetTamamla([{ role: "user", content: "Telefon ekranındaki öğeler (🔘 dokunulabilir, ✏️ yazı alanı):\n" + metinEkran.slice(0, 5000) + "\n\nBu ekranda ne olduğunu Türkçe, kısa ve maddeler halinde özetle; önemli düğmeleri belirt." }], { sicaklik: 0.3, maks: 600 });
      if (r.metin) return "### 📱 Ekran özeti\n\n" + r.metin;
    }
    return "### 📱 Ekrandaki yazılar\n\n" + metinEkran.split("\n").slice(0, 80).join("\n\n");
  }
  const genel: [RegExp, Parameters<typeof E.genel>[0], string][] = [
    [/^(?:geri(?: git| dön| gel)?|geri tuşu)$/, "geri", "⬅️ Geri"], [/^ana ekran(?:a dön|a git)?$|^ana sayfaya dön$/, "ana", "🏠 Ana ekran"],
    [/^son uygulamalar|^açık uygulamalar/, "son", "🗂️ Son uygulamalar"], [/^bildirim(?:ler(?:i)?)?\s*(?:aç|göster|indir)?$/, "bildirim", "🔔 Bildirimler"],
    [/^hızlı ayarlar/, "hizli", "⚡ Hızlı ayarlar"], [/^(?:ekranı |telefonu )?kilitle$/, "kilit", "🔒 Ekran kilitlendi"], [/^ekran görüntüsü al/, "ekranGoruntusu", "📸 Ekran görüntüsü alındı"],
  ];
  for (const [re, e, ad] of genel) if (re.test(t)) { if (!gerek()) return ERISIM_YOK; return E.genel(e) ? ad + " ✅" : ad + " yapılamadı."; }
  if ((m = t.match(/^(?:aşağı|yukarı)\s*(?:kaydır|in|çık)$|^(?:kaydır)$/))) { if (!gerek()) return ERISIM_YOK; return E.kaydir(!/yukarı/.test(t)) ? "↕️ Kaydırıldı ✅" : "↕️ Kaydırılacak alan bulunamadı."; }
  if ((m = metin.trim().match(/^(.{1,40}?)\s*(?:'?(?:[ıiuü]|y[ıiuü]|[ae]|y[ae]))?\s+(?:dokun|tıkla|bas)$/i)) || (m = metin.trim().match(/^(?:dokun|tıkla|bas)\s*[:\-]?\s*(.{1,40})$/i))) {
    if (!gerek()) return null;  // servis kapalıyken gündelik cümleleri ("kalbime dokun") komut sanma
    const hedef = m[1].replace(/['’](?:[ıiuü]|y[ıiuü]|[ae]|y[ae])$/i, "").replace(/^["“]|["”]$/g, "").trim();
    return E.tikla(hedef) ? `👆 **${hedef}** öğesine dokunuldu ✅` : `👆 Ekranda **${hedef}** bulunamadı. "ekranı oku" diyerek yazıları görebilirsin.`;
  }
  if ((m = metin.trim().match(/^(?:yaz|şunu yaz)\s*[:\-]\s*(.+)$/i))) {
    if (!gerek()) return ERISIM_YOK;
    return E.yaz(m[1]) ? `⌨️ Yazıldı: **${m[1]}** ✅` : "⌨️ Yazı alanı bulunamadı (önce yazı alanına dokun).";
  }
  return null;
}

/** Sohbet metninden telefon komutu çıkarır ve çalıştırır; komut değilse null. */
export async function telefonKomutu(metin: string): Promise<string | null> {
  const er = await erisimKomutu(metin);
  if (er) return er;
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "");
  let m: RegExpMatchArray | null;
  if ((m = t.match(/^youtube'?(?:da|de|ta|te)?\s+(.+?)\s+(?:ara|aç|bul|izle|oynat|çal)$/))) return acHedef("youtube", m[1]);
  if ((m = t.match(/^(.+?)\s+(?:videosunu|videolarını)\s+(?:aç|bul|göster)$/))) return acHedef("youtube", m[1]);
  if (/^(?:youtube|yutup)(?:\s?'?(?:[ıiuü]|y?[ae]))?\s*(?:aç|başlat|açar mısın|geç|git|gir)$/.test(t)) return acHedef("youtube");
  if ((m = t.match(/^spotify'?(?:da|de|ta)?\s+(.+?)\s+(?:çal|aç|ara|dinle)$/))) return acHedef("spotify", m[1]);
  if ((m = t.match(/^google'?(?:da|de|ta)?\s+(.+?)\s+(?:ara|bul)$/))) return acHedef("google", m[1]);
  if ((m = t.match(/^(?:haritada|haritalarda|harita'?da)\s+(.+?)\s+(?:göster|bul|aç|ara)$/))) return acHedef("harita", m[1]);
  if ((m = t.match(/^(.+?)'?(?:ya|ye|a|e)\s+(?:yol tarifi|nasıl giderim|yol göster)/))) return acHedef("yol", m[1]);
  if ((m = t.match(/^((?:\+?90|0)?\s*5\d{2}[\s\d]{7,})\s*(?:'?[ıiuü]?\s*)?(?:numarasını\s+)?ara$/))) return acHedef("telefon", m[1]);
  const uyg: [RegExp, Hedef][] = [[/^whatsapp/, "whatsapp"], [/^instagram|^insta\b/, "instagram"], [/^telegram/, "telegram"], [/^spotify/, "spotify"],
    [/^gmail|^e-?posta/, "gmail"], [/^harita|^maps|^google maps/, "harita"], [/^(?:telefon )?ayarlar/, "ayarlar"]];
  if (/\s(?:aç|başlat|açar mısın|geç|git|gir)$/.test(t)) for (const [re, h] of uyg) if (re.test(t)) return acHedef(h);
  return null;
}
