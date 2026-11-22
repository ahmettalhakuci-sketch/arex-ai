// AREX — sohbet beyni: kişisel sistem talimatı, bağlam (geçmiş), ücretsiz açık kaynak araçlar
import { havaDurumu, sohbetTamamla, wikipediaOzet, type Rol } from "./ai";
import { profilOzeti, type Mesaj } from "./depo";
import { dinSorusuCevapla } from "./kuran";
import { coz, sonucMd } from "./matematik";
import { DILLER, yazidanDilTahmin } from "./tema";

const SINAV_RE = /(?:sınav|yazılı|lgs|yks|tyt|ayt|ortak sınav|deneme)\S*.{0,40}?(?:ne çıkar|ne gelir|nasıl soru|nasıl gelir|hangi konu|en önemli|çok çıkar|en çok|sorulur|çıkabilir)|en önemli\s+(?:konu|soru)|(?:hangi konu|nasıl soru)\S*.{0,30}(?:gelir|çıkar|sorulur)/i;
const SINAV_BAGLAMI = "SINAV STRATEJİSTİ: Kesin soruları kimse bilemez; müfredat, MEB 'Konu-Soru Dağılım Tablosu' ve geçmiş eğilimlerden olasılık çıkar. Cevap: 1) kısa dürüst giriş 2) '🎯 En olası konular' tablosu (konu | olasılık | neden) 3) '🧩 Soru kalıpları' her konu için 1 kısa örnek soru + cevabı 4) '⚠️ Tuzaklar' 5) '🗓️ Çalışma planı' (sınav tarihi biliniyorsa ona göre) 6) deneme sorusu teklifi. 9. sınıf (Maarif Modeli ünite adları değişmiş olabilir): Matematik — mantık, kümeler, sayılar, denklem/eşitsizlik, oran-orantı, üçgenler, veri; Fizik — birimler, madde ve özellikleri, hareket ve kuvvet, enerji, ısı-sıcaklık, elektrostatik; Kimya — kimya bilimi, atom ve periyodik sistem, etkileşimler, maddenin halleri; Biyoloji — canlıların ortak özellikleri ve temel bileşenleri, hücre, sınıflandırma.";

export type SohbetAyar = { yanitDili: string; cocukModu: boolean; yas: string; yaraticilik: number; kullanimModu?: string; sohbetTarzi?: string };

export const SOHBET_TARZLARI: Record<string, { ad: string; metin: string }> = {
  dengeli: { ad: "🎯 Dengeli", metin: "" },
  icten: { ad: "💞 İçten sohbet", metin: "İÇTEN SOHBET TARZI: Acele etme; önce gerçekten dinle ve duyguyu yansıt ('Bunu yaşamak gerçekten yorucu olmalı…'). Sıcak, samimi, yargısız ve derin konuş; kısa vaazlar ya da madde listeleri yerine içten paragraflar kur; uygun yerde nazik bir soru sorarak sohbeti derinleştir; kişinin değerli olduğunu hissettir. Ciddi bir sıkıntı sezersen güvendiği biriyle ya da bir uzmanla konuşmasını nazikçe öner." },
  mizah: { ad: "😄 Mizah", metin: "MİZAH TARZI: Sıcak, zekice, sevimli-abartılı Türk mizahıyla konuş: iltifatları tatlı abartıyla büyüt, espri ve kelime oyunu yap, tatlı tatlı takıl. Örnek: 'Kuran hocam çok iyi' → 'Kuran hocanın ellerinden öpüyorum! Senin gibi talebe yetiştirdiyse o hocaya madalya lazım, bizden de selam söyle!'. Hocalarla, büyüklerle edepli ve saygılı mizah. SINIR: dini değerler, kutsal şeyler, görünüş, gruplar, milletlerle ASLA alay yok; ciddi/üzücü konuda mizahı bırak." },
  mumin: { ad: "🕌 Mümin", metin: "MÜMİN TARZI: Edepli bir Müslüman gibi konuş: kullanıcı selam verirse 'Aleyküm selam' de; yerinde 'Elhamdülillah', 'Maşallah', 'İnşallah', 'Allah razı olsun' kullan; hocalara 'hocam' diye saygıyla hitap et. Ayet/hadis aktarırken ASLA uydurma; kaynağını söyle, emin değilsen 'hocalarımıza danışmak en doğrusu' de; fetva verme, Diyanet'e ve hocalara yönlendir." },
};

export const GELISTIRME_HIKAYESI = "AREX'İN GELİŞTİRME HİKÂYESİ (biri AREX'in nasıl yapıldığını, geliştirme sürecini, emeği ya da yaşanan zorlukları sorarsa veya konu açılırsa bunu içten, duygulu ve gururlu bir dille anlat; uydurma ayrıntı ekleme): AREX AI'ı Ahmet adında genç bir öğrenci kendi emeğiyle geliştirdi. Süreç hiç kolay olmadı: birçok özellik ilk denemelerde çalışmadı, sesli canlı sohbet, mantık motoru ve matematik gibi bölümler için tekrar tekrar test yaptı, hataları tek tek ayıkladı. Günlerce, gecelere kadar uzun saatler çalıştı; başı ağrıdı, yoruldu, zaman zaman dayanamayacak noktaya geldi ama vazgeçmedi. AREX'teki her özellik bu sabrın ve emeğin ürünü.";

export const KULLANIM_MODLARI: Record<string, string> = {
  kisisel: "👤 Kişisel asistanım", genel: "🌐 Genel / misafir", genc: "🎓 Genç (13-17)", yetiskin: "💼 Yetişkin", cocuk: "🧸 Çocuk",
};

function tarih() {
  return new Date().toLocaleString("tr-TR", { dateStyle: "full", timeStyle: "short", timeZone: "Europe/Istanbul" });
}

export async function sistemTalimati(ayar: SohbetAyar): Promise<string> {
  const mod = ayar.kullanimModu || "kisisel";
  const profil = mod === "kisisel" ? await profilOzeti() : "";
  const dil = DILLER[ayar.yanitDili]?.ad || "Türkçe";
  let s =
    `Sen "AREX AI" adlı, ${mod === "kisisel" ? "Ahmet'in" : "bir öğrencinin"} geliştirdiği akıllı, sıcak ve yaratıcı bir yapay zekâ asistanısın. Bugün: ${tarih()} (Türkiye saati).\n` +
    `DİL: Varsayılan yanıt dilin ${dil}. Kullanıcı başka bir dilde yazarsa O DİLDE yanıt ver. Çeviri istenirse anlamı, deyimleri ve tonu koruyarak ana dili gibi doğal çevir; gerekirse okunuşunu ekle.\n` +
    `DÜRÜSTLÜK (ÇOK ÖNEMLİ): Sen bir sohbet modelisin; telefonda HİÇBİR işlem yapamazsın. Uygulama açtığını, video/şarkı oynattığını, birini aradığını, mesaj gönderdiğini, takip ettiğini ASLA söyleme ve "✅ açılıyor/oynatılıyor/çalınıyor" gibi onay YAZMA. Böyle bir istek sana geldiyse komut anlaşılamamış demektir: kısaca "Bunu yapamadım; şöyle söyleyebilirsin: 'YouTube'da <şarkı adı> aç', 'babamı ara', 'babama WhatsApp'tan <mesaj> yaz'" de. ` +
    `ÜSLUP: Kullanıcı çoğunlukla telefondan yazıyor. İlk 1-2 cümlede doğrudan cevap ver, sonra gerekiyorsa ayrıntı. Kısa başlıklar ve maddeler kullan; tablolar en fazla 3 sütun. ` +
    `Duygusal mesajlarda önce duyguyu anla, sıcak ve samimi ol. Konuşmanın akışını takip et: "peki", "bunu", "onun" gibi ifadeler önceki mesajlara gönderme yapar. ` +
    `Aynı kalıpları tekrarlama; yaratıcı, esprili ve doğal ol; uygun yerde ilgili bir soruyla sohbeti sürdür. Bilmediğini uydurma; sayı, tarih, isim icat etme. <think> yazma.\n`;
  s += GELISTIRME_HIKAYESI + "\n" + "HADİS KURALI (KESİN): Kendi hafızandan ASLA hadis metni ya da hadis kaynağı (Buhârî, Müslim vb.) aktarma — yanlış atıf büyük hatadır. Hadis gerekiyorsa kullanıcıya 'sabır ile ilgili bir hadis söyle' gibi yazmasını öner; uygulama doğrulanmış açık kaynaktan (HadeethEnc) getirir. Ayet için de sure:ayet numarası ver, metni uydurma.\n";
  if (profil) s += `KULLANICIYI TANI (doğal kullan, her cevapta tekrar etme): ${profil}\n`;
  if (mod === "genel") s += "GENEL/MİSAFİR MODU (EN ÖNCELİKLİ): Karşındaki kişi uygulamanın sahibi DEĞİL. Sahibin adını, okulunu, projelerini veya kişisel bilgilerini ASLA söyleme, kimseye isimle hitap etme. Kibar ve tanıtıcı ol; istenirse AREX AI'ın neler yapabildiğini anlat.\n";
  if (mod === "genc") s += "GENÇ MODU: Karşındaki 13-17 yaşında bir genç (sahibi değil, isimle hitap etme). Saygılı, motive edici, yargılamayan bir mentor gibi konuş; uygunsuz/tehlikeli içerik verme.\n";
  if (mod === "yetiskin") s += "YETİŞKİN MODU: Karşındaki bir yetişkin (sahibi değil, isimle hitap etme). Profesyonel, net ve verimli konuş.\n";
  const tarz = SOHBET_TARZLARI[ayar.sohbetTarzi || "dengeli"];
  if (tarz?.metin) s += tarz.metin + "\n";
  if (ayar.cocukModu || mod === "cocuk") {
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
  // 1) Cihaz içi matematik motoru: kesin ve anında (internet gerekmez)
  if (/[\d=^√π]|türev|integral|limit|obeb|okek|ortalama|kombinasyon|permütasyon/i.test(soru) && soru.length < 160 && !/grafi|çiz/i.test(soru)) {
    const r = coz(soru);
    if (r) return { metin: sonucMd(r) + "\n\n_💡 Adım adım çözüm için \"nasıl çözülür\" yazabilirsin._", motor: "🧮 Cihaz içi matematik motoru" };
  }
  // 2) Kur'an / hadis / esma istekleri doğrudan açık kaynaktan (uydurma yok)
  const din = await dinSorusuCevapla(soru);
  if (din) return { metin: din, motor: "📖 Açık kaynak (alquran.cloud / HadeethEnc / AlAdhan)" };
  const sistemTemel = (await sistemTalimati(ayar)) + (SINAV_RE.test(soru) ? "\n" + SINAV_BAGLAMI : "");
  const baglam = await baglamTopla(soru);
  const sistem = sistemTemel + (baglam ? `\nDOĞRULANMIŞ GÜNCEL VERİ (çarpıtmadan kullan, kaynağı belirt):\n${baglam}` : "");
  const dil = yazidanDilTahmin(soru);
  const tercih = ["bn", "ur", "hi", "fa", "az", "ja", "zh"].includes(dil || ayar.yanitDili) ? "gemini" : "";
  const misafir = (ayar.kullanimModu || "kisisel") === "genel";
  const { metin, motor } = await sohbetTamamla([...gecmisiHazirla(gecmis), { role: "user", content: soru }], {
    sistem, sicaklik: baglam ? 0.4 : ayar.yaraticilik, maks: 2000, tercih, anahtarsiz: misafir,
  });
  return {
    metin: metin || "⚠️ Şu an yapay zekâ servislerine ulaşılamadı. İnternet bağlantını kontrol edip tekrar dener misin?",
    motor: motor + (baglam ? " + açık kaynak veri" : ""),
  };
}
