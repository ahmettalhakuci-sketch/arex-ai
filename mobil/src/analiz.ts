// AREX — sistematik fotoğraf & video analizi (Streamlit modul_27 ile aynı mantık)
export const ETIK = (dil: string) =>
  "Sen AREX AI'ın görsel analiz uzmanısın. Analizi SİSTEMATİK yap: başlıklar, maddeler, her çıkarım için gözlemlenen KANIT ve güven düzeyi (düşük/orta/yüksek). " +
  "KURALLAR: 1) Kişiyi asla tanımlama, isim tahmini yapma. 2) Etnik köken, din, sağlık, cinsel yönelim, siyasi görüş gibi hassas özellik ÇIKARMA. " +
  "3) Duyguları yalnızca GÖRÜNEN İFADE ve beden dili olarak raporla; iç durumu kesin göstermediğini kısaca belirt. Yalan/suç/karakter yargısı verme; görünüşe göre kişi yargılama. " +
  `4) Olmayanı uydurma. 5) Birden çok kişiyi 'Kişi 1 (soldaki)' diye numarala. 6) Yanıt dili: ${dil}. Telefonda okunacak; en fazla 3 sütunlu tablolar.`;

export const ANALIZLER: Record<string, { ad: string; talimat: string; derin?: boolean; video?: boolean }> = {
  genel: { ad: "🔎 Genel Sahne", talimat: "Genel analiz: ne görülüyor, ortam, ana nesneler ve kişiler (kimlik tahmini olmadan), eylem, ışık/zaman ipuçları, dikkat çeken ayrıntılar; sonunda 2-3 cümlelik özet." },
  duygu: { ad: "🙂 İfade & Duygu", derin: true, talimat: "Her yüz için SİSTEMATİK ifade analizi: 1) Yüz bölgeleri gözlemi (kaş, alın, göz, bakış, dudak, çene, baş eğimi). 2) Yaklaşık FACS AU kodları. 3) Görünen duygu dağılımı tablosu (mutluluk, şaşkınlık, üzüntü, öfke, korku, iğrenme, nötr — %). 4) Tedirginlik/gerginlik/stres işaretleri VAR/YOK/BELİRSİZ ve 0-10 görünen gerginlik skoru. 5) Alternatif açıklamalar. 6) Güven düzeyi ve sınırlılıklar." },
  yuz: { ad: "📐 Yüz Şekli", derin: true, talimat: "Yüz tipi analizi: 1) Yüz şekli sınıfı (oval, yuvarlak, kare, dikdörtgen, kalp, elmas, üçgen) en olası 1-2 ve nedeni. 2) Oranlar: alın/elmacık/çene genişliği, uzunluk/genişlik oranı, çene ucu, üçte bir bölümler, genel simetri (açı etkisini belirt). 3) Betimleyici özellik notları. 4) Uygun saç kesimi, gözlük çerçevesi, sakal/kaş önerileri. Güzellik puanı verme." },
  beden: { ad: "🧍 Beden Dili", derin: true, talimat: "Beden dili: duruş, omuz, kol-el konumu, bacak/ayak yönü, kişiler arası mesafe/yönelim, enerji. Her işaret için olası anlam + alternatif + güven düzeyi." },
  catisma: { ad: "⚠️ Kavga Riski", derin: true, talimat: "Durumun fiziksel çatışmaya dönüşme olasılığını yalnızca GÖZLENEBİLİR DAVRANIŞ ve BAĞLAMA göre değerlendir (görünüşe göre kişi yargılama): 1) İşaret tablosu (sıkılmış yumruk, öne eğilme/üstüne yürüme, mesafe daralması, parmakla gösterme, bağırma ifadesi, itme/tutma, kalabalık toplanması, tehlikeli nesne, geri çekilme, araya giren kişi, sakinleştirici jestler) — var/yok/belirsiz + kanıt. 2) Tırmanma aşaması. 3) Olasılık: düşük/orta/yüksek + yaklaşık % (tahmin olduğunu belirt). 4) Alternatif açıklamalar (oyun, spor, şaka). 5) Güvenlik ve sakinleştirme önerileri." },
  yazi: { ad: "📝 Yazı Oku", talimat: "Görseldeki tüm yazıları düzenini koruyarak çıkar; sonra kısa özet ve önemli tarih/sayı/isimler." },
  ders: { ad: "🧮 Soru Çöz", talimat: "Soruyu yaz, adım adım çöz, kullanılan kuralı belirt, sonucu kalın yaz, 'akılda kalsın' ipucu ver." },
  kalite: { ad: "📷 Kalite & Renk", talimat: "Netlik, pozlama, beyaz dengesi, gürültü, kompozisyon, ışık; baskın 5 renk (HEX); 10 üzerinden puan; 3 iyileştirme önerisi." },
  sayim: { ad: "🔢 Nesne Sayımı", talimat: "Nesneleri kategorilere ayırıp say: nesne | adet | konum tablosu; emin olunmayanlarda aralık ver." },
  guvenlik: { ad: "🛡️ Ev Güvenliği", talimat: "Ortamı çocuk güvenliği açısından tara: keskin/sıcak nesneler, kablo, devrilme, küçük parçalar, kimyasallar; her risk için seviye ve önlem." },
  yemek: { ad: "🍽️ Yemek & Kalori", talimat: "Yiyecekleri tanı, porsiyon, yaklaşık kalori ve makro aralığı tablosu; tahmin olduğunu belirt; 2 öneri." },
  doga: { ad: "🌿 Bitki / Hayvan", talimat: "En olası 3 tür (olasılıkla), ayırt edici özellikler, ilginç bilgiler, bakım/güvenlik notları." },
  v_genel: { ad: "🎬 Video Özeti", video: true, derin: true, talimat: "Zaman damgalı (dd:ss) olay akışı, ana konu, konuşma özeti, önemli anlar ve 3 maddelik özet." },
  v_duygu: { ad: "🙂 Videoda Gerginlik", video: true, derin: true, talimat: "Görünen ifade ve beden dilini ZAMAN İÇİNDE analiz et: dd:ss | ifade | gerginlik işaretleri | 0-10 görünen gerginlik tablosu; ses tonu gözlemleri; eğilim, alternatif açıklamalar, güven düzeyi." },
  v_catisma: { ad: "⚠️ Videoda Kavga Riski", video: true, derin: true, talimat: "Çatışma riskini zaman içinde değerlendir (yalnızca davranış/bağlam): dd:ss | davranış | tırmanma aşaması | risk % tablosu; eğilim, genel olasılık, alternatif açıklamalar, güvenlik önerileri." },
};

export const TAM_RAPOR = ["genel", "duygu", "yuz", "beden", "catisma", "kalite"];

export function turTahmin(metin: string, video: boolean): string[] {
  const t = (metin || "").toLowerCase();
  if (video) {
    if (/kavga|çatışma|saldır|dövüş|tartış/.test(t)) return ["v_catisma"];
    if (/tedirgin|gergin|stres|duygu|ifade|mimik|korku|endişe/.test(t)) return ["v_duygu"];
    return ["v_genel"];
  }
  if (/tam (analiz|rapor)|sistematik|her şeyi/.test(t)) return TAM_RAPOR;
  const k: [string, RegExp][] = [
    ["catisma", /kavga|çatışma|saldır|dövüş|tartışma/], ["duygu", /tedirgin|gergin|stres|duygu|ifade|mimik|mutlu|üzgün|korku|endişe/],
    ["yuz", /yüz (tipi|şekli|yapısı|oran)|hangi saç|gözlük çerçeve|simetri/], ["beden", /beden dili|duruş|jest/],
    ["yazi", /yazıyı oku|metni oku|ne yazıyor|ocr/], ["ders", /çöz|cevabı ne|denklem|test sorusu/],
    ["kalite", /kalite|kompozisyon|renk paleti|netlik/], ["sayim", /kaç tane|sayısı/], ["guvenlik", /güvenli mi|tehlike|risk/],
    ["yemek", /kalori|besin|protein/], ["doga", /hangi bitki|bu bitki|hangi hayvan|türü ne|cinsi ne/],
  ];
  return k.filter(([, re]) => re.test(t)).map(([a]) => a);
}

export function analizTalimati(turler: string[], not: string): { talimat: string; derin: boolean; maks: number } {
  let talimat = turler.length
    ? "Aşağıdaki analizleri SIRAYLA, her birini kendi başlığı altında yap:\n\n" + turler.map((t, i) => `## ${i + 1}. ${ANALIZLER[t].ad}\n${ANALIZLER[t].talimat}`).join("\n\n")
    : "Bu medyayı kullanıcının sorusuna göre yanıtla. Soru yoksa kısa ve faydalı bir genel analiz yap.";
  if (not.trim()) talimat += `\n\nKullanıcının notu / sorusu: ${not.trim()}`;
  const derin = turler.some((t) => ANALIZLER[t]?.derin) || turler.length > 2;
  return { talimat, derin, maks: Math.min(6000, 1800 + 900 * Math.max(0, turler.length - 1)) };
}
