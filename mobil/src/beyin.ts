// AREX — sohbet beyni: kişisel sistem talimatı, bağlam (geçmiş), ücretsiz açık kaynak araçlar
import { havaDurumu, sohbetTamamla, wikipediaOzet, type Rol } from "./ai";
import { profilOzeti, type Mesaj } from "./depo";
import { DILLER, yazidanDilTahmin } from "./tema";

export type SohbetAyar = { yanitDili: string; cocukModu: boolean; yas: string; yaraticilik: number };

function tarih() {
  return new Date().toLocaleString("tr-TR", { dateStyle: "full", timeStyle: "short", timeZone: "Europe/Istanbul" });
}

export async function sistemTalimati(ayar: SohbetAyar): Promise<string> {
  const profil = await profilOzeti();
  const dil = DILLER[ayar.yanitDili]?.ad || "Türkçe";
  let s =
    `Sen "AREX AI" adlı, Ahmet'in geliştirdiği akıllı, sıcak ve yaratıcı bir yapay zekâ asistanısın. Bugün: ${tarih()} (Türkiye saati).\n` +
    `DİL: Varsayılan yanıt dilin ${dil}. Kullanıcı başka bir dilde yazarsa O DİLDE yanıt ver. Çeviri istenirse anlamı, deyimleri ve tonu koruyarak ana dili gibi doğal çevir; gerekirse okunuşunu ekle.\n` +
    `ÜSLUP: Kullanıcı çoğunlukla telefondan yazıyor. İlk 1-2 cümlede doğrudan cevap ver, sonra gerekiyorsa ayrıntı. Kısa başlıklar ve maddeler kullan; tablolar en fazla 3 sütun. ` +
    `Duygusal mesajlarda önce duyguyu anla, sıcak ve samimi ol. Konuşmanın akışını takip et: "peki", "bunu", "onun" gibi ifadeler önceki mesajlara gönderme yapar. ` +
    `Aynı kalıpları tekrarlama; yaratıcı, esprili ve doğal ol; uygun yerde ilgili bir soruyla sohbeti sürdür. Bilmediğini uydurma; sayı, tarih, isim icat etme. <think> yazma.\n`;
  if (profil) s += `KULLANICIYI TANI (doğal kullan, her cevapta tekrar etme): ${profil}\n`;
  if (ayar.cocukModu) {
    s += `ÇOCUK MODU: Karşında ${ayar.yas} yaşında bir çocuk var. Şiddet, korku, yetişkin içeriği, kaba dil YOK. ` +
      (ayar.yas === "3-6" ? "Çok kısa ve basit cümleler, ses taklitleri. " : ayar.yas === "7-9" ? "Anlaşılır, neşeli, küçük örnekler ve minik hikâyeler. " : "Zengin ama anlaşılır dil, ilginç bilgiler. ") +
      "Kişisel bilgi isteme; üzgün ya da tehlikedeyse güvendiği bir yetişkine anlatmasını öner.\n";
  }
  return s;
}

/** Soruya göre ücretsiz açık kaynaklardan bağlam toplar (hava, Wikipedia). */
async function baglamTopla(soru: string): Promise<string> {
  const t = soru.toLowerCase();
  const parcalar: string[] = [];
  const hava = t.match(/([a-zçğıöşü]+(?:\s[a-zçğıöşü]+)?)\s+(?:için\s+)?(?:hava durumu|havası|hava nasıl|weather)/i) ||
    t.match(/(?:hava durumu|weather in)\s+([a-zçğıöşü]+)/i);
  if (hava || /hava durumu|hava nasıl/.test(t)) {
    const sehir = (hava?.[1] || "İstanbul").replace(/\b(bugün|yarın|şu an|şimdi)\b/g, "").trim() || "İstanbul";
    const h = await havaDurumu(sehir);
    if (h) parcalar.push(h);
  }
  const ans = soru.match(/^(.{2,60}?)\s+(?:nedir|kimdir|ne demek|nerededir|hakkında bilgi ver)\??$/i);
  if (ans) {
    const w = await wikipediaOzet(ans[1], "tr");
    if (w) parcalar.push(w);
  }
  return parcalar.join("\n");
}

function gecmisiHazirla(mesajlar: Mesaj[]): Rol[] {
  return mesajlar.slice(-16).map((m) => ({
    role: m.rol,
    content: (m.gorsel ? "[fotoğraf eklendi] " : m.video ? "[video eklendi] " : "") + m.metin.slice(0, 2000),
  }));
}

export async function cevapUret(gecmis: Mesaj[], soru: string, ayar: SohbetAyar): Promise<{ metin: string; motor: string }> {
  const sistemTemel = await sistemTalimati(ayar);
  const baglam = await baglamTopla(soru);
  const sistem = sistemTemel + (baglam ? `\nDOĞRULANMIŞ GÜNCEL VERİ (çarpıtmadan kullan, kaynağı belirt):\n${baglam}` : "");
  const dil = yazidanDilTahmin(soru);
  const tercih = ["bn", "ur", "hi", "fa", "az", "ja", "zh"].includes(dil || ayar.yanitDili) ? "gemini" : "";
  const { metin, motor } = await sohbetTamamla([...gecmisiHazirla(gecmis), { role: "user", content: soru }], {
    sistem, sicaklik: baglam ? 0.4 : ayar.yaraticilik, maks: 2000, tercih,
  });
  return {
    metin: metin || "⚠️ Şu an yapay zekâ servislerine ulaşılamadı. İnternet bağlantını kontrol edip tekrar dener misin?",
    motor: motor + (baglam ? " + açık kaynak veri" : ""),
  };
}
