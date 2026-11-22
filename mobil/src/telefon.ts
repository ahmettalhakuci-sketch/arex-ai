// AREX — telefon komutları: "YouTube aç", "YouTube'da Yasin tilaveti ara", "WhatsApp aç", "haritada cami göster",
// "05xx… ara", "Spotify'da X çal", "Google'da X ara", "ayarları aç" (uygulama bağlantıları / derin bağlantılar)
import { Linking, Platform } from "react-native";
import * as E from "../modules/arex-erisim";
import { sohbetTamamla } from "./ai";
import { izinIste } from "./izin";

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

const GENEL_KOMUTLAR: [RegExp, Parameters<typeof E.genel>[0], string][] = [
  [/^(?:geri(?: git| dön| gel)?|geri tuşu)$/, "geri", "⬅️ Geri"], [/^ana ekran(?:a dön|a git)?$|^ana sayfaya dön$/, "ana", "🏠 Ana ekran"],
  [/^son uygulamalar|^açık uygulamalar/, "son", "🗂️ Son uygulamalar"], [/^bildirim(?:ler(?:i)?)?\s*(?:aç|göster|indir)?$/, "bildirim", "🔔 Bildirimler"],
  [/^hızlı ayarlar/, "hizli", "⚡ Hızlı ayarlar"], [/^(?:ekranı |telefonu )?kilitle$/, "kilit", "🔒 Ekran kilitlendi"], [/^ekran görüntüsü al/, "ekranGoruntusu", "📸 Ekran görüntüsü alındı"],
  ];
/** Metin bir genel eylem komutu mu ("geri", "ana ekran", "bildirimleri aç"…) → eylem adı ve etiket */
export function genelEylem(metin: string): { eylem: Parameters<typeof E.genel>[0]; ad: string } | null {
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "");
  for (const [re, e, ad] of GENEL_KOMUTLAR) if (re.test(t)) return { eylem: e, ad };
  return null;
}

/** Erişilebilirlik komutları: ekranı oku/özetle, X'e dokun, yaz, kaydır, geri, ana ekran, bildirimler, kilitle, uygulama aç. Komut değilse null. */
export async function erisimKomutu(metin: string): Promise<string | null> {
  if (Platform.OS !== "android" || !E.destekVar()) return null;
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "");
  let m: RegExpMatchArray | null;
  // Servis bağlantısı kopmuşsa (güncelleme/zorla durdurma sonrası) önce kendini onarmayı dener
  const gerek = async () => E.etkinMi() || (await E.onar()) === "onarildi";
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
    if (!(await gerek())) return ERISIM_YOK;
    const metinEkran = E.ekranOku();
    if (!metinEkran.trim()) return "📱 Okunacak başka bir uygulama ekranı yok. Başka bir uygulamadayken **yan tuşa basılı tut** → kartta **📖 Ekranı özetle**.";
    if (/özetle|anlat|açıkla|ne var|neler/.test(t)) {
      const r = await sohbetTamamla([{ role: "user", content: "Telefon ekranındaki öğeler (🔘 dokunulabilir, ✏️ yazı alanı):\n" + metinEkran.slice(0, 5000) + "\n\nBu ekranda ne olduğunu Türkçe, kısa ve maddeler halinde özetle; önemli düğmeleri belirt." }], { sicaklik: 0.3, maks: 600 });
      if (r.metin) return "### 📱 Ekran özeti\n\n" + r.metin;
    }
    return "### 📱 Ekrandaki yazılar\n\n" + metinEkran.split("\n").slice(0, 80).join("\n\n");
  }
  const genel = GENEL_KOMUTLAR;
  for (const [re, e, ad] of genel) if (re.test(t)) { if (!(await gerek())) return ERISIM_YOK; return E.genel(e) ? ad + " ✅" : ad + " yapılamadı."; }
  if ((m = t.match(/^(?:aşağı|yukarı)\s*(?:kaydır|in|çık)$|^(?:kaydır)$/))) { if (!(await gerek())) return ERISIM_YOK; return E.kaydir(!/yukarı/.test(t)) ? "↕️ Kaydırıldı ✅" : "↕️ Kaydırılacak alan bulunamadı."; }
  if ((m = metin.trim().match(/^(.{1,40}?)\s*(?:'?(?:[ıiuü]|y[ıiuü]|[ae]|y[ae]))?\s+(?:dokun|tıkla|bas)$/i)) || (m = metin.trim().match(/^(?:dokun|tıkla|bas)\s*[:\-]?\s*(.{1,40})$/i))) {
    if (!(await gerek())) return null;  // servis kapalıyken gündelik cümleleri ("kalbime dokun") komut sanma
    const hedef = m[1].replace(/['’](?:[ıiuü]|y[ıiuü]|[ae]|y[ae])$/i, "").replace(/^["“]|["”]$/g, "").trim();
    return E.tikla(hedef) ? `👆 **${hedef}** öğesine dokunuldu ✅` : `👆 Ekranda **${hedef}** bulunamadı. "ekranı oku" diyerek yazıları görebilirsin.`;
  }
  if ((m = metin.trim().match(/^(?:yaz|şunu yaz)\s*[:\-]\s*(.+)$/i))) {
    if (!(await gerek())) return ERISIM_YOK;
    return E.yaz(m[1]) ? `⌨️ Yazıldı: **${m[1]}** ✅` : "⌨️ Yazı alanı bulunamadı (önce yazı alanına dokun).";
  }
  return null;
}

// ---------- Rehber: "babamı ara", "babama WhatsApp'tan geliyorum yaz", "ablama SMS at: geç kalacağım" ----------
async function androidIzin(izin: string, ad: string): Promise<boolean> {
  const { PermissionsAndroid } = require("react-native");
  return izinIste(ad, async () => ({ granted: (await PermissionsAndroid.request(izin)) === "granted", canAskAgain: true }),
    async () => ({ granted: await PermissionsAndroid.check(izin) }));
}
/** "babamı"/"babama"/"ablamın" → kişi adayları: babam, baba */
function kisiAdaylari(ham: string): string[] {
  const k = ham.trim().replace(/['’]/g, "").replace(/\s+(?:numarasını|telefonunu|cebini)$/, "");
  const ekli = k.replace(/(?:y?[ıiuü]|y?[ae]|n[ıiuü]n|n[ae])$/, "");
  return Array.from(new Set([k, ekli, ekli.replace(/(?:[ıiuü])?m$/, ""), ekli.replace(/(?:[ıiuü])?m(?:[ıiuü]z)?$/, "")])).filter((x) => x.length >= 2);
}
function kisiSec(ham: string): E.Kisi | null {
  for (const a of kisiAdaylari(ham)) { const l = E.kisiBul(a); if (l.length) return l[0]; }
  return null;
}
/** Rehber komutları (Android). Komut değilse null. */
export async function kisiKomutu(metin: string): Promise<string | null> {
  if (Platform.OS !== "android" || !E.destekVar()) return null;
  const ham = metin.trim().replace(/[.!?]+$/, "");
  const t = ham.toLocaleLowerCase("tr");
  let islem: "ara" | "whatsapp" | "sms" | null = null, kisi = "", mesaj = "";
  let m: RegExpMatchArray | null;
  const ek = "(?:['’]?(?:y[ae]|[ae]|n[ae]))";
  if ((m = ham.match(new RegExp(`^(.{2,30}?)${ek}\\s+(?:whats?app|vatsap)['’]?(?:tan|dan|ten|den)?\\s+(?:mesaj\\s+)?(?:yaz|at|gönder)\\s*[:\\-]\\s*(.+)$`, "i")))
    || (m = ham.match(new RegExp(`^(.{2,30}?)${ek}\\s+(?:whats?app|vatsap)['’]?(?:tan|dan|ten|den)?\\s+(.+?)\\s+(?:diye\\s+)?(?:yaz|de|gönder|mesaj at)$`, "i")))
    || (m = ham.match(new RegExp(`^(.{2,30}?)${ek}\\s+mesaj\\s+(?:at|gönder|yaz)\\s*[:\\-]\\s*(.+)$`, "i")))) {
    islem = "whatsapp"; kisi = m[1]; mesaj = m[2];
  } else if ((m = ham.match(new RegExp(`^(.{2,30}?)${ek}\\s+(?:sms|kısa mesaj)\\s+(?:at|gönder|yaz)\\s*[:\\-]?\\s*(.+)$`, "i")))) {
    islem = "sms"; kisi = m[1]; mesaj = m[2];
  } else if ((m = t.match(/^(.{2,30}?)(?:['’]?(?:y[ıiuü]|[ıiuü]|n[ıiuü]))?\s+(?:ara|arar mısın|arasana|telefonla ara|çaldır)$/))
    && !/(?:['’]?(?:da|de|ta|te)\s|google|youtube|internette|haritada|spotify)/.test(m[1]) && !/^\+?\d/.test(m[1]) && m[1].split(/\s+/).length <= 3) {
    islem = "ara"; kisi = m[1];
  }
  if (!islem) return null;
  if (!(await androidIzin("android.permission.READ_CONTACTS", "Rehber"))) return "📇 Kişiyi bulmam için **Rehber** izni gerekli (🔐 İzinler).";
  const k = kisiSec(kisi);
  // "iş ara", "bir çözüm ara" gibi gündelik cümleler: rehberde yoksa komut sayma (sohbete bırak)
  if (!k) return islem === "ara" ? null : `📇 Rehberde **${kisi}** bulamadım. Rehberde nasıl kayıtlıysa öyle söyle (ör. "Babam'a WhatsApp'tan yaz: …").`;
  if (islem === "ara") {
    await androidIzin("android.permission.CALL_PHONE", "Telefon");
    return E.ara(k.numara) ? `📞 **${k.ad}** aranıyor…` : `📞 **${k.ad}** için çevirici açıldı — yeşil tuşa bas.`;
  }
  if (islem === "whatsapp") return E.whatsapp(k.numara, mesaj) ? `💬 WhatsApp'ta **${k.ad}** sohbeti mesajın yazılı açıldı — **Gönder**'e bas.\n\n> ${mesaj}` : `💬 WhatsApp yüklü değil; tarayıcıda açıldı.`;
  E.sms(k.numara, mesaj);
  return `✉️ **${k.ad}** için SMS yazılı açıldı — **Gönder**'e bas.\n\n> ${mesaj}`;
}

// ---------- Uygulama içi eylemler: "YouTube'da X aç/oynat" → ilk videoyu doğrudan oynatır; "Instagram'da X'i takip et" ----------
/** YouTube aramasında ilk videonun kimliği (anahtarsız; bilgisayar tarayıcısı kimliğiyle) */
export async function ilkVideo(sorgu: string): Promise<string | null> {
  try {
    const r = await fetch(`https://www.youtube.com/results?search_query=${encodeURIComponent(sorgu)}&hl=tr`, {
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "tr-TR", Cookie: "SOCS=CAI" } });
    const m = (await r.text()).match(/"videoId":"([A-Za-z0-9_-]{11})"/);
    return m ? m[1] : null;
  } catch { return null; }
}
export async function uygulamaIciKomut(metin: string): Promise<string | null> {
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "");
  let m: RegExpMatchArray | null;
  // YouTube: oynat/aç/izle/çal → ilk videoyu doğrudan oynat ("ara/bul" ise arama sayfası — eski yol)
  if ((m = t.match(/^(?:youtube|yutup)['’]?(?:da|dan|de|den|ta|tan)?\s+(.+?)\s+(?:videosunu\s+|şarkısını\s+|klibini\s+)?(?:aç|oynat|izle|çal|başlat|dinle)$/))
    || (m = t.match(/^(.+?)\s+(?:videosunu|şarkısını|klibini|türküsünü|ilahisini|neşidini|nasheedini|marşını)\s+(?:aç|oynat|izle|çal|dinle)$/))
    // "Yenileceksiniz youtubeden aç", "tarkan şımarık youtube'da oynat" (önce ad, sonra YouTube)
    || (m = t.match(/^(.+?)['’]?(?:y[ıiuü]|[ıiuü])?\s+(?:youtube|yutup|yutub)['’]?(?:dan|den|da|de|tan|ten|ta|te)?\s+(?:aç|oynat|izle|çal|dinle|başlat|açar mısın)$/))) {
    const sorgu = m[1].trim();
    const id = await ilkVideo(sorgu);
    if (id) {
      try { await Linking.openURL(`vnd.youtube://${id}`); } catch { await Linking.openURL(`https://www.youtube.com/watch?v=${id}`); }
      return `▶️ YouTube'da **${sorgu}** oynatılıyor ✅`;
    }
    return acHedef("youtube", sorgu);
  }
  // Instagram: "@ahmet'i takip et", "instagramda ahmet'i takip et"
  if ((m = t.match(/^(?:instagram['’]?(?:da|dan)\s+)?@?([a-z0-9._]{2,30})['’]?(?:y[ıiuü]|[ıiuü])?\s+(?:instagram['’]?(?:da|dan)\s+)?takip\s+et$/)) && (/instagram|@/.test(t))) {
    const kullanici = m[1];
    try { await Linking.openURL(`https://www.instagram.com/${kullanici}/`); } catch { return "📸 Instagram açılamadı."; }
    if (Platform.OS === "android" && E.destekVar() && (E.etkinMi() || (await E.onar()) === "onarildi")) {
      E.sonraTikla(["Takip Et", "Takip et", "Follow"], 3500, 7);
      return `📸 Instagram'da **@${kullanici}** açıldı, **Takip Et**'e basıyorum…`;
    }
    return `📸 Instagram'da **@${kullanici}** açıldı — **Takip Et**'e bas. (Kendim basmam için ♿ Telefon erişimini aç.)`;
  }
  // Genel: "instagramda X'e dokun" yerine zaten "X'e dokun" var; burada başka uygulama içi eylem yok
  return null;
}

// ---------- ⏰ Saat / sayaç / alarm: "saat kaç", "5 dakikalık sayaç kur", "sabah 7'ye alarm kur", "yarın 6.30'da uyandır" ----------
const SAYI: Record<string, number> = { bir: 1, iki: 2, üç: 3, dört: 4, beş: 5, altı: 6, yedi: 7, sekiz: 8, dokuz: 9, on: 10, "on beş": 15, yirmi: 20, otuz: 30, kırk: 40, "kırk beş": 45, elli: 50, yarım: 0.5, çeyrek: 0.25 };
const sayiOku = (x: string) => { const t = x.trim(); return /^\d+([.,]\d+)?$/.test(t) ? parseFloat(t.replace(",", ".")) : SAYI[t] ?? NaN; };
export async function saatKomutu(metin: string): Promise<string | null> {
  const t = metin.trim().toLocaleLowerCase("tr").replace(/[.!?]+$/, "").replace(/\s+/g, " ");
  let m: RegExpMatchArray | null;
  if (/^(?:şu an )?saat kaç|^saati söyle|^saat ne$/.test(t)) {
    const d = new Date(); return `🕒 Saat **${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}** — ${d.toLocaleDateString("tr-TR", { weekday: "long", day: "numeric", month: "long" })}`;
  }
  if (Platform.OS !== "android" || !E.destekVar()) return null;
  if (/^alarmlar(ı|ım|ımı)?\s*(göster|aç)?$/.test(t)) { E.alarmlariGoster(); return "⏰ Alarmların açıldı."; }
  // Sayaç: "5 dakikalık sayaç kur", "on dakika sayaç", "30 saniye geri sayım başlat", "yarım saat zamanlayıcı"
  if ((m = t.match(/^(\d+(?:[.,]\d+)?|[a-zçğıöşü]+(?: beş)?)\s*(saniye|sn|dakika|dk|saat)(?:l[ıi]k|luk|lük)?\s*(?:bir\s+)?(?:sayaç|zamanlayıcı|geri sayım|timer)(?:\s*(?:kur|başlat|ayarla|aç))?$/))
    || (m = t.match(/^(?:sayaç|zamanlayıcı|geri sayım)\s*(?:kur|başlat)?\s*[:\-]?\s*(\d+(?:[.,]\d+)?|[a-zçğıöşü]+(?: beş)?)\s*(saniye|sn|dakika|dk|saat)$/))) {
    const n = sayiOku(m[1]); if (!(n > 0)) return null;
    const sn = Math.round(n * (/^sa/.test(m[2]) && m[2] !== "saniye" ? 3600 : /^d/.test(m[2]) ? 60 : 1));
    if (sn > 24 * 3600) return "⏱️ En fazla 24 saatlik sayaç kurabilirim.";
    E.sayac(sn, "AREX sayaç");
    const yaz = sn >= 3600 ? `${+(sn / 3600).toFixed(2)} saat` : sn >= 60 ? `${+(sn / 60).toFixed(1)} dakika` : `${sn} saniye`;
    return `⏱️ **${yaz}**${/saniye|saat/.test(yaz) ? "lik" : "lık"} sayaç kuruldu ✅`;
  }
  // Alarm: "sabah 7'ye alarm kur", "7:30 alarm", "akşam 9'da uyandır", "yarın 6.15'te beni uyandır", "alarm kur 06:45"
  if ((m = t.match(/^(?:yarın\s+)?(sabah|öğlen|öğle|akşam|gece)?\s*(\d{1,2})(?:[:.](\d{2}))?\s*(?:['’]?(?:y?[ae]|d[ae]|t[ae]))?\s*(?:bir\s+)?(?:alarm(?:ı)?\s*(?:kur|ayarla|koy)?|(?:beni\s+)?uyandır)$/))
    || (m = t.match(/^(?:alarm|uyandır)\s*(?:kur|ayarla)?\s*[:\-]?\s*(sabah|öğlen|öğle|akşam|gece)?\s*(\d{1,2})(?:[:.](\d{2}))?$/))) {
    let saat = Number(m[2]); const dk = Number(m[3] || 0); const dilim = m[1] || "";
    if (saat > 23 || dk > 59) return null;
    if ((dilim === "akşam" || dilim === "öğlen" || dilim === "öğle") && saat < 12) saat += 12;
    if (dilim === "gece" && saat < 5) { /* gece 2 → 02:00 */ } else if (dilim === "gece" && saat < 12) saat += 12;
    E.alarm(saat, dk, "AREX");
    return `⏰ **${String(saat).padStart(2, "0")}:${String(dk).padStart(2, "0")}** alarmı kuruldu ✅`;
  }
  return null;
}

/** Sohbet metninden telefon komutu çıkarır ve çalıştırır; komut değilse null. */
export async function telefonKomutu(metin: string): Promise<string | null> {
  const saatCevap = await saatKomutu(metin);
  if (saatCevap) return saatCevap;
  const uygCevap = await uygulamaIciKomut(metin);
  if (uygCevap) return uygCevap;
  const kisiCevap = await kisiKomutu(metin);
  if (kisiCevap) return kisiCevap;
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
