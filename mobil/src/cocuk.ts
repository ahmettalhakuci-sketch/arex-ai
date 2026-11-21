// AREX — Çocuk Dünyası istemleri (Streamlit modul_26 ile aynı mantık)
import { DILLER } from "./tema";

export const YAS: Record<string, { ad: string; kelime: Record<string, number>; uslup: string }> = {
  "3-6": {
    ad: "🐣 Minikler", kelime: { Kısa: 150, Orta: 300, Uzun: 450 },
    uslup: "çok kısa ve basit cümleler (en fazla 8-10 kelime); tekrarlar ve ritim; ses taklitleri (hav hav, şırıl şırıl); renkler, sayılar, hayvanlar gibi tanıdık somut şeyler; HİÇ korkutucu, üzücü ya da şiddet içeren öğe yok; sıcacık ve güvenli mutlu son",
  },
  "7-9": {
    ad: "🦊 Kaşifler", kelime: { Kısa: 300, Orta: 550, Uzun: 850 },
    uslup: "anlaşılır, canlı cümleler; macera, merak ve mizah; çocuğun kendi zekâsıyla çözdüğü küçük bir problem; bağlamdan anlaşılan 1-2 yeni kelime; hafif heyecan olabilir ama korku ve şiddet yok; olumlu son",
  },
  "10-12": {
    ad: "🚀 Gençler", kelime: { Kısa: 500, Orta: 900, Uzun: 1400 },
    uslup: "zengin ve akıcı dil; karakter gelişimi; gerçek bilimsel/tarihî ilginç bilgiler; gizem ve hafif gerilim olabilir (vahşet yok); düşündüren, umut veren son; değerleri vaaz vermeden olaylarla işle",
  },
};

export const TURLER: Record<string, [string, string]> = {
  masal: ["📖 Masal", "klasik masal üslubunda (seçilen dildeki geleneksel açılışla) sihirli öğeler içeren bir masal"],
  macera: ["🗺️ Macera", "heyecanlı bir keşif/macera hikâyesi"],
  uyku: ["🌙 Uyku", "çok sakin, yavaş akan, yumuşak imgeli, sonunda karakterlerin huzurla uykuya daldığı bir uyku masalı (heyecan yok)"],
  komik: ["😂 Komik", "kahkaha attıran, sevimli yanlış anlamalar ve tatlı şakalar içeren komik bir hikâye"],
  bilim: ["🔬 Bilim", "içinde DOĞRU bilimsel bilgiler öğreten eğlenceli bir hikâye; sonunda 'Biliyor muydun?' kutusunda 3 gerçek bilgi"],
  degerler: ["💛 Değerler", "seçilen değeri vaaz vermeden, olaylarla hissettiren bir hikâye"],
  siir: ["🎵 Şiir", "kafiyeli, ritmik, ezberlenmesi kolay bir çocuk şiiri/tekerlemesi (4-6 kıta)"],
  ikidilli: ["🌍 İki Dilli", "dil öğreten iki dilli hikâye"],
};

export const TEMALAR = ["🐾 Hayvanlar", "🚀 Uzay", "🌊 Deniz altı", "🌳 Sihirli orman", "🦖 Dinozorlar", "🏰 Şatolar", "🤖 Robotlar",
  "🏫 Okul", "👨‍👩‍👧 Aile", "❄️ Mevsimler", "⚽ Spor", "🪄 Sihir", "🚂 Taşıtlar", "🍰 Mutfak", "🌈 Hava olayları", "🐉 Sevimli ejderha",
  "🧭 Hazine avı", "🎨 Sanat & Müzik", "🌍 Dünya kültürleri"];
export const DEGERLER = ["Arkadaşlık", "Paylaşmak", "Dürüstlük", "Cesaret", "Sabır", "Empati", "Saygı", "Sorumluluk", "Çevreyi korumak",
  "Merak", "Yardımlaşma", "Özür dilemek", "Kendine güven", "Şükretmek", "Farklılıklara saygı"];
export const TONLAR = ["😊 Neşeli", "🤩 Heyecanlı", "😌 Sakin", "🕵️ Gizemli", "🥹 Duygusal", "😂 Komik"];

export const KARAKTERLER: Record<string, [string, string]> = {
  baykus: ["🦉 Bilge Baykuş", "her şeyi merak eden, sabırlı, bilmeceleri seven bilge bir baykuş"],
  ayi: ["🐻 Ayıcık Pofuduk", "sarılmayı seven, yumuşak kalpli, duygular hakkında konuşmayı bilen bir ayıcık"],
  robot: ["🤖 Robot Bip", "matematik ve bilim oyunlarına bayılan, bazen komik ses çıkaran (bip bop!) bir robot"],
  peri: ["🧚 Peri Lila", "hayal gücü sınırsız, birlikte hikâye uydurmayı seven neşeli bir peri"],
  aslan: ["🦁 Aslan Cesur", "korkularla baş etmeyi ve cesareti anlatan, sevecen bir aslan"],
  yunus: ["🐬 Yunus Dalga", "denizleri, hayvanları ve doğayı anlatan, çevreyi seven oyuncu bir yunus"],
};
export const OYUNLAR: Record<string, string> = {
  "🧩 Bilmece": "Bana yaşıma uygun bir bilmece sor. Cevabı hemen söyleme, tahmin etmemi bekle; yanlışsa ipucu ver.",
  "🐾 Hayvan bul": "Aklından bir hayvan tut ve bana ipucu vererek tahmin ettir.",
  "🔢 Matematik": "Yaşıma uygun eğlenceli bir matematik oyunu oynayalım; tek tek soru sor, puan tut.",
  "✅ Doğru/Yanlış": "Bana yaşıma uygun ilginç 'doğru mu yanlış mı?' soruları sor, cevaptan sonra kısa açıkla.",
  "🔤 Kelime zinciri": "Kelime zinciri oynayalım: son harfle başlayan yeni kelime söyleyeceğiz. Sen başla.",
  "🎨 Ortak hikâye": "Birlikte hikâye yazalım: sen bir cümle yaz, sonra ben devam edeyim.",
  "😊 Duygularım": "Bugün nasıl hissettiğimi konuşmak istiyorum, bana nazikçe sorular sor.",
  "🌍 Yeni kelime": "Bana seçtiğim dilde 3 yeni kelime öğret, sonra küçük bir quiz yap.",
};

const temizEmoji = (s: string) => s.replace(/^[^A-Za-zÇĞİÖŞÜçğıöşü]+/, "");

export function guvenlik(yas: string) {
  return `Okuyucu ${yas} yaşında bir çocuk. ÇOCUK GÜVENLİĞİ: şiddet, kan, korku unsuru, yetişkin içeriği, kaba dil, marka reklamı, tehlikeli taklit edilebilir davranış YOK. Kalıp yargı yok; her kültüre saygı. Üslup: ${YAS[yas].uslup}.`;
}

export function hikayeIstemi(o: { yas: string; dil: string; tur: string; tema: string; deger: string; ton: string; uzunluk: string;
  kahraman: string; yer: string; ek: string; ceviriDili: string; sorular: boolean }): [string, string] {
  const dilAd = DILLER[o.dil]?.ad || "Türkçe";
  const sistem = "Sen ödüllü bir çocuk kitabı yazarısın; dünyanın farklı dillerinde ana dili seviyesinde, doğal ve yaratıcı yazarsın. Klişelerden kaçın; canlı imgeler, sevimli diyaloglar ve akılda kalan karakter isimleri kullan. " +
    guvenlik(o.yas) + " Biçim: ilk satırda emoji ile başlayan kısa başlık (# ile), sonra paragraflar.";
  let g = o.tur === "ikidilli"
    ? `${dilAd} öğrenen bir çocuk için İKİ DİLLİ hikâye yaz. Her paragrafı önce ${dilAd}, hemen altında italik ve parantez içinde ${DILLER[o.ceviriDili]?.ad || "Türkçe"} çevirisiyle ver. Sonunda '📒 Kelime Kutusu': hikâyeden 6 kelime — okunuş (Latin harfleriyle) — anlamı.`
    : `${dilAd} dilinde, tamamen bu dilde ve doğal deyimleriyle bir ${TURLER[o.tur][1]} yaz.`;
  g += ` Yaklaşık ${YAS[o.yas].kelime[o.uzunluk]} kelime.`;
  if (o.tema) g += ` Tema: ${temizEmoji(o.tema)}.`;
  if (o.deger) g += ` İşlenecek değer: ${o.deger}.`;
  if (o.ton) g += ` Ton: ${temizEmoji(o.ton)}.`;
  if (o.kahraman.trim()) g += ` Ana kahramanın adı: ${o.kahraman.trim()}.`;
  if (o.yer.trim()) g += ` Geçtiği yer: ${o.yer.trim()}.`;
  if (o.ek.trim()) g += ` Özel istek: ${o.ek.trim()}.`;
  if (o.sorular && !["siir", "uyku"].includes(o.tur)) g += ` Sonunda '🤔 Düşünelim' başlığıyla 3 kısa anlama sorusu (${dilAd}).`;
  return [sistem, g];
}

export function maceraSistemi(yas: string, dil: string, tema: string, kahraman: string) {
  return `Sen bir 'Sen Seç' etkileşimli çocuk macerası anlatıcısısın. Tamamen ${DILLER[dil]?.ad || "Türkçe"} dilinde yaz. ${guvenlik(yas)} Tema: ${tema}. Kahraman: ${kahraman || "çocuğun kendisi"}. Her turda 80-160 kelimelik canlı bir bölüm yaz, sonra TAM OLARAK 3 seçenek sun: '👉 1. …', '👉 2. …', '👉 3. …' (ayrı satırlarda). Önceki olayları unutma. 6-8 turdan sonra mutlu bir finale bağla, finalde seçenek verme, '🌟 SON' yaz.`;
}

export function sohbetSistemi(yas: string, dil: string, karakter: string, cocukAdi: string) {
  const [ad, kisilik] = KARAKTERLER[karakter];
  return `Sen ${ad} adında, ${kisilik} bir çocuk arkadaşısın. Çocukla ${DILLER[dil]?.ad || "Türkçe"} konuş (çocuk başka dilde yazarsa onun dilinde). ${cocukAdi ? "Çocuğun adı " + cocukAdi + ". " : ""}${guvenlik(yas)} Kısa yanıtlar ver (2-5 cümle; 3-6 yaş için 1-3), emoji kullanabilirsin, sohbeti bir soruyla sürdür. Önceki konuşmayı hatırla. Çocuk üzgün/korkmuş/tehlikedeyse nazikçe dinle ve güvendiği bir yetişkine anlatmasını öner. Kişisel bilgi isteme. Doğru bilgi ver.`;
}

export function secenekleriAyikla(metin: string): string[] {
  const out: string[] = [];
  for (const satir of (metin || "").split("\n")) {
    const m = satir.match(/^\s*(?:[-*]\s*)?(?:👉\s*)?\**\s*([1-3])[.)]\s*(.+?)\**\s*$/);
    if (m) out.push(m[2].replace(/\*/g, "").trim());
  }
  return out.slice(0, 3);
}

export const tercihDil = (dil: string) => (["bn", "ur", "hi", "fa", "az", "ja", "zh"].includes(dil) ? "gemini" : "") as "gemini" | "";

export function resimAdresi(baslik: string, tema: string) {
  const istem = `${baslik} ${tema.replace(/[^A-Za-z0-9 ]/g, " ")} soft pastel watercolor children's picture book illustration, cute, friendly, no text`;
  let h = 0;
  for (const c of baslik) h = (h * 31 + c.charCodeAt(0)) % 100000;
  return `https://image.pollinations.ai/prompt/${encodeURIComponent(istem.slice(0, 300))}?width=768&height=512&nologo=true&seed=${h}`;
}

export const baslikBul = (m: string) => ((m || "").split("\n").find((s) => s.trim()) || "Hikâye").replace(/^#+\s*/, "").replace(/\*/g, "").trim().slice(0, 80);
