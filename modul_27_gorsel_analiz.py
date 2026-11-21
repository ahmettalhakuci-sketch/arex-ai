# -*- coding: utf-8 -*-
"""
AREX — Modül 27: SİSTEMATİK FOTOĞRAF & VİDEO ANALİZ LABORATUVARI
==============================================================================
Gemini çok kipli modeliyle fotoğraf / kısa video için yapılandırılmış analizler:
yüz ifadesi & görünen duygu (tedirginlik/gerginlik işaretleri dahil), yüz şekli & oranlar,
beden dili, sahne, yazı okuma, ders sorusu, kalite/kompozisyon, nesne sayımı, güvenlik riski,
yemek, bitki/hayvan ve video zaman çizelgesi.

Etik sınırlar (sistem talimatına gömülü): kişi tanıma YOK; etnik köken, din, sağlık, cinsel yönelim
gibi hassas özellikler çıkarılmaz; duygu = "görünen ifade" olarak raporlanır, kanıt + güven düzeyiyle.
"""
import re

import modul_25_ai_cekirdek as ai

ETIK_SISTEM = (
    "Sen AREX AI Studio'nun görsel analiz uzmanısın. Analizi SİSTEMATİK yap: başlıklar, maddeler, "
    "her çıkarım için gözlemlenen KANIT ve güven düzeyi (düşük / orta / yüksek). "
    "KESİN KURALLAR: 1) Görseldeki kişiyi asla tanımlama, isim tahmini yapma (ünlü olsa bile). "
    "2) Etnik köken, ırk, din, sağlık durumu, cinsel yönelim, siyasi görüş gibi hassas özellikleri ÇIKARMA. "
    "3) Duygular için yalnızca GÖRÜNEN YÜZ İFADESİ ve beden dili işaretlerini raporla; bunların kişinin gerçek iç "
    "durumunu kesin göstermediğini, ışık/açı/kültür/anlık hareketten etkilenebileceğini kısaca belirt. "
    "Yalan, suç, karakter veya zekâ yargısı verme. 4) Görselde olmayan şeyi uydurma; emin değilsen söyle. "
    "5) Görselde birden çok kişi varsa onları 'Kişi 1 (soldaki)', 'Kişi 2' diye numarala. "
    "6) Yanıt dili: {dil}. Telefonda okunacak; kısa başlıklar, en fazla 3 sütunlu tablolar kullan."
)

ANALIZLER = {
    "genel": {
        "ad": "🔎 Genel Sahne Analizi",
        "talimat": "Bu görseli genel olarak analiz et: ne görülüyor, ortam/mekân, ana nesneler ve kişiler (kimlik "
                   "tahmini olmadan), yapılan eylem, ışık ve zaman ipuçları, dikkat çeken ayrıntılar. Sonunda 2-3 "
                   "cümlelik özet ver.",
    },
    "duygu": {
        "ad": "🙂 Yüz İfadesi & Görünen Duygu",
        "talimat": "Her görünen yüz için SİSTEMATİK ifade analizi yap:\n"
                   "1. **Yüz bölgeleri (gözlem):** kaşlar (kalkık/çatık/iç uçlar), alın, gözler (açıklık, bakış yönü, "
                   "göz kırpma/kısma), burun kanatları, dudaklar (gerilme, sıkma, köşeler), çene/çene kası, baş eğimi.\n"
                   "2. **Kas hareketi kodları (yaklaşık FACS AU):** gözlenen olası AU'ları listele (ör. AU1+AU2, AU4, AU12, AU24).\n"
                   "3. **Görünen duygu dağılımı:** mutluluk, şaşkınlık, üzüntü, öfke, korku, iğrenme, nötr — yüzde "
                   "tahmini tablo.\n"
                   "4. **Tedirginlik / gerginlik / stres işaretleri:** dudak sıkma-ısırma, kaş iç uçlarının kalkması, "
                   "çene gerginliği, kaçamak bakış, omuz kasılması, kendine dokunma, el ovuşturma gibi işaretleri "
                   "VAR/YOK/BELİRSİZ olarak işaretle ve 0-10 arası 'görünen gerginlik skoru' ver.\n"
                   "5. **Alternatif açıklamalar:** aynı ifadeyi açıklayabilecek başka nedenler (güneş, yorgunluk, "
                   "konsantrasyon, poz verme).\n"
                   "6. **Güven düzeyi ve sınırlılıklar.**",
    },
    "yuz_sekli": {
        "ad": "📐 Yüz Şekli & Oranlar",
        "talimat": "Görünen yüz(ler) için yüz tipi analizi yap:\n"
                   "1. **Yüz şekli sınıfı:** oval, yuvarlak, kare, dikdörtgen/uzun, kalp, elmas, üçgen — en olası 1-2 "
                   "sınıf ve neden.\n"
                   "2. **Oran gözlemleri:** alın genişliği, elmacık kemiği genişliği, çene hattı genişliği, yüz "
                   "uzunluğu/genişliği oranı (yaklaşık), çene ucu biçimi, yüz üçte bir bölümleri (alın/burun/alt yüz) "
                   "dengesi, genel simetri (yaklaşık; çekim açısının etkisini belirt).\n"
                   "3. **Özellik notları:** kaş biçimi, göz aralığı (yakın/ortalama/geniş), burun ve dudak oranı — "
                   "yargısız, betimleyici.\n"
                   "4. **Öneriler:** bu yüz şekline uygun saç kesimi, gözlük çerçevesi, (varsa) sakal/kaş şekli önerileri.\n"
                   "Güzellik puanı veya kişiler arası çekicilik karşılaştırması YAPMA. Açı/lens etkisi varsa uyar.",
    },
    "beden": {
        "ad": "🧍 Beden Dili & Duruş",
        "talimat": "Beden dilini sistematik incele: duruş (dik/çökük), omuzlar, kol-el konumu (açık/kapalı, kavuşturma, "
                   "kendine dokunma), bacak/ayak yönü, kişiler arası mesafe ve yönelim, genel enerji. Her işaret için "
                   "olası anlam + alternatif açıklama + güven düzeyi ver. Kesin yargı verme.",
    },
    "catisma": {
        "ad": "⚠️ Çatışma / Kavga Riski (durumsal, olasılıksal)",
        "talimat": "Sahnedeki DURUMUN çatışmaya / fiziksel kavgaya dönüşme olasılığını sistematik değerlendir. "
                   "Yalnızca GÖZLENEBİLİR DAVRANIŞ ve BAĞLAM işaretlerine dayan; kişinin yüzüne, görünüşüne, yaşına, "
                   "kıyafetine veya grubuna bakarak 'kavgacı biri' yargısı VERME.\n"
                   "1. **Gözlenen işaretler tablosu** (işaret | var/yok/belirsiz | kanıt): sıkılmış yumruk, öne eğilme / "
                   "üstüne yürüme, kişiler arası mesafenin çok daralması, işaret parmağıyla gösterme, bağırıyor gibi açık "
                   "ağız + gergin yüz, itme/tutma/temas, kalabalık toplanması/çevreleme, ellerde tehlikeli nesne, "
                   "kaçma/geri çekilme, ayıran/araya giren kişi, sakinleştirici jestler (açık avuç, geri adım).\n"
                   "2. **Tırmanma aşaması:** sakin → gergin tartışma → sözlü saldırganlık → fiziksel temas.\n"
                   "3. **Olasılık tahmini:** önümüzdeki kısa sürede fiziksel çatışma olasılığı — düşük (%0-25) / orta "
                   "(%25-60) / yüksek (%60+) ve tek bir yaklaşık yüzde; bu yüzdenin TAHMİN olduğunu, tek kareden "
                   "belirsizliğin yüksek olduğunu belirt.\n"
                   "4. **Alternatif açıklamalar:** şaka/oyun kavgası, spor, heyecanlı sohbet, poz, sahne/film.\n"
                   "5. **Ne yapılmalı:** güvenli mesafe, sakinleştirme (de-eskalasyon) adımları, gerekiyorsa yetişkin/"
                   "güvenlik/112 çağırma; asla araya fiziksel olarak girmeyi önermeden önce güvenliği vurgula.",
    },
    "yazi": {
        "ad": "📝 Yazı Okuma (OCR) & Özet",
        "talimat": "Görseldeki tüm yazıları olduğu gibi, düzenini koruyarak çıkar (başlık, paragraf, tablo). Ardından "
                   "kısa bir özet ve varsa önemli tarih/sayı/isimleri madde madde listele.",
    },
    "ders": {
        "ad": "🧮 Ders Sorusu Çözümü",
        "talimat": "Görseldeki TÜM soru(lar)ı dikkatle oku (şıklar dahil). Her soru için: önce soruyu aynen yaz, sonra adım "
                   "adım çöz, kullanılan formül/kuralı belirt, sonucu ve doğru şıkkı kalın yaz, tek cümlelik 'akılda kalsın' "
                   "ipucu ver. Birden fazla soru varsa numarala. El yazısı veya bulanık kısım varsa varsayımını belirt.",
    },
    "kalite": {
        "ad": "📷 Fotoğraf Kalitesi, Kompozisyon & Renk",
        "talimat": "Fotoğrafı teknik olarak değerlendir: netlik/odak, pozlama, beyaz dengesi, gürültü, kompozisyon "
                   "(üçler kuralı, öncü çizgiler, denge), arka plan, ışık yönü. Baskın 5 rengi yaklaşık HEX kodlarıyla ver. "
                   "10 üzerinden puanla ve 3 somut iyileştirme önerisi (çekim + düzenleme) yaz.",
    },
    "sayim": {
        "ad": "🔢 Nesne Sayımı & Envanter",
        "talimat": "Görseldeki nesneleri kategorilere ayırıp say ve tablo halinde ver (nesne | adet | konum). Emin "
                   "olunmayan sayımlar için aralık ver.",
    },
    "guvenlik": {
        "ad": "🛡️ Güvenlik & Risk Taraması",
        "talimat": "Ortamı güvenlik açısından tara (özellikle çocuklar için): keskin/sıcak nesneler, kablo, devrilme, "
                   "düşme, boğulma riski taşıyan küçük parçalar, kimyasallar, trafik vb. Her risk için seviye "
                   "(düşük/orta/yüksek) ve somut önlem yaz.",
    },
    "yemek": {
        "ad": "🍽️ Yemek & Besin Tahmini",
        "talimat": "Yemeği/yiyecekleri tanı, porsiyonu tahmin et, yaklaşık kalori ve makro (protein/karbonhidrat/yağ) "
                   "aralığını tablo olarak ver; tahmin olduğunu belirt. Daha dengeli olması için 2 öneri ekle.",
    },
    "doga": {
        "ad": "🌿 Bitki / Hayvan / Nesne Tanıma",
        "talimat": "Görseldeki bitki, hayvan veya nesneyi tanı: en olası 3 tür/model (olasılıkla), ayırt edici "
                   "özellikler, ilginç bilgiler ve (bitkiyse) bakım, (hayvansa) güvenlik notları.",
    },
}

VIDEO_ANALIZLERI = {
    "video_genel": {
        "ad": "🎬 Video Zaman Çizelgesi & Özet",
        "talimat": "Videoyu analiz et: zaman damgalı (dd:ss) olay akışı, ana konu, konuşma varsa özeti, önemli anlar "
                   "ve sonunda 3 maddelik özet.",
    },
    "video_duygu": {
        "ad": "🙂 Videoda İfade & Gerginlik Değişimi",
        "talimat": "Videodaki kişi(ler)in görünen yüz ifadesini ve beden dilini ZAMAN İÇİNDE analiz et: dd:ss "
                   "damgalı tablo (zaman | görünen ifade | gerginlik işaretleri | 0-10 görünen gerginlik). Ses varsa "
                   "ses tonu (hız, duraklama, titreme) gözlemlerini ekle. Sonunda eğilim özeti, alternatif açıklamalar "
                   "ve güven düzeyi ver. Kimlik tahmini ve tanı koyma yapma.",
    },
    "video_catisma": {
        "ad": "⚠️ Videoda Çatışma / Kavga Riski",
        "talimat": "Videodaki durumun çatışmaya dönüşme riskini ZAMAN İÇİNDE değerlendir; yalnızca davranış ve bağlam "
                   "işaretlerine dayan, görünüşe göre kişi yargılama. dd:ss damgalı tablo: zaman | gözlenen davranış "
                   "(yaklaşma, yumruk sıkma, itme, bağırma, kalabalık, araya girme, geri çekilme) | tırmanma aşaması | "
                   "o andaki tahmini risk %. Ses varsa ses yüksekliği/tonu artışını ekle. Sonunda: eğilim (artıyor/"
                   "azalıyor), genel olasılık (düşük/orta/yüksek + %), alternatif açıklamalar (oyun, spor, şaka), "
                   "güvenlik ve sakinleştirme önerileri.",
    },
    "video_beden": {
        "ad": "🧍 Videoda Beden Dili & Hareket",
        "talimat": "Videodaki hareketleri ve beden dilini zaman damgalı olarak çıkar: jest, duruş değişimi, tekrar eden "
                   "hareketler, kişiler arası etkileşim. Her gözlem için olası anlam + alternatif + güven düzeyi.",
    },
}

TAM_RAPOR_ANAHTARLARI = ("genel", "duygu", "yuz_sekli", "beden", "catisma", "kalite")


def analiz_turu_tahmin_et(metin: str, video_mu: bool = False) -> list:
    """Kullanıcının yazdığı nottan uygun analiz türlerini seçer (sohbete fotoğraf eklenince)."""
    t = (metin or "").lower()
    if video_mu:
        if re.search(r"kavga|çatışma|catisma|saldır|dövüş|tartış|kavgaya|tehlikeli mi", t):
            return ["video_catisma"]
        if re.search(r"tedirgin|gergin|stres|duygu|ifade|mimik|heyecan|korku|endişe|sinir|yalan", t):
            return ["video_duygu"]
        if re.search(r"beden dili|hareket|jest|duruş", t):
            return ["video_beden"]
        return ["video_genel"]
    secim = []
    kurallar = [
        ("duygu", r"tedirgin|gergin|stres|duygu|ifade|mimik|mutlu|üzgün|uzgun|korku|endişe|kızgın|psikoloj|ruh hal"),
        ("yuz_sekli", r"yüz (tipi|şekli|sekli|yapısı|hatları|oran)|yuz (tipi|sekli)|hangi saç|gözlük çerçeve|simetri"),
        ("catisma", r"kavga|çatışma|catisma|saldır|dövüş|tartışma|kavgaya|tehlikeli bir durum"),
        ("beden", r"beden dili|duruş|durus|jest|el kol"),
        ("yazi", r"yazıyı oku|metni oku|ocr|ne yazıyor|yazıları çıkar|özetle"),
        ("ders", r"soru|çöz|cevabı ne|cevap ne|işlem|denklem|test|ödev|matematik|fizik|kimya|türev|integral|problem"),
        ("kalite", r"kalite|kompozisyon|fotoğraf nasıl|renk paleti|ışık nasıl|netlik"),
        ("sayim", r"kaç tane|say\b|sayısı|envanter"),
        ("guvenlik", r"güvenli mi|tehlike|risk"),
        ("yemek", r"kalori|yemek|besin|protein"),
        ("doga", r"bu ne bitki|hangi bitki|hangi hayvan|bu hayvan|türü ne|cinsi ne"),
    ]
    for anahtar, desen in kurallar:
        if re.search(desen, t):
            secim.append(anahtar)
    if re.search(r"tam (analiz|rapor)|her şeyi|detaylı analiz|sistematik", t):
        secim = list(TAM_RAPOR_ANAHTARLARI)
    return secim


SYMPY_KURALI = (
    "\n\nÖNEMLİ — DOĞRULAMA SATIRI: Görselde matematik sorusu varsa, cevabının EN SONUNA her matematik sorusu için ayrı "
    "bir satırda bilgisayar cebir sistemi için düz metin ifade yaz: `SYMPY: <ifade>`. Örnekler: `SYMPY: 3x+7=22`, "
    "`SYMPY: x^3-6x^2+11x-6=0`, `SYMPY: x+y=5, x-y=1`, `SYMPY: türev x^2*sin(x)`, `SYMPY: 0'dan 2'ye integral x^2`, "
    "`SYMPY: limit x->0 sin(x)/x`, `SYMPY: (3/4+1/2)*8`, `SYMPY: 2x-3>5`. Sözel problemlerde kurduğun denklemi yaz. "
    "Matematik sorusu yoksa bu satırı yazma."
)


def _matematik_dogrula(metin: str) -> str:
    """Yanıttaki SYMPY satırlarını AREX'in kendi motorlarıyla (Modül 29 + 14) yeniden hesaplar."""
    satirlar = re.findall(r"(?im)^\s*`?SYMPY:\s*(.+?)`?\s*$", metin or "")
    temiz = re.sub(r"(?im)^\s*`?SYMPY:.*$\n?", "", metin or "").rstrip()
    temiz = re.sub(r"(?im)^#+[^\n]*doğrulama satır[^\n]*$", "", temiz).rstrip()
    temiz = re.sub(r"(?:\n\s*---\s*)+$", "", temiz).rstrip()
    if not satirlar:
        return temiz
    dogrulamalar = []
    for i, ifade in enumerate(satirlar[:8], 1):
        sonuc = None
        try:
            import modul_29_ileri_matematik as _m29
            sonuc, _ = _m29.ileri_matematik_coz(ifade)
        except Exception:
            pass
        if not sonuc:
            try:
                import modul_14_pro_matematik as _m14
                sonuc, _ = _m14.pro_matematik_coz(ifade if "=" in ifade else ifade + " kaç")
            except Exception:
                sonuc = None
        if sonuc:
            ozet = re.sub(r"^#+.*\n+", "", sonuc.strip()).strip()
            dogrulamalar.append(f"**{i}.** `{ifade}`\n\n{ozet}")
        else:
            dogrulamalar.append(f"**{i}.** `{ifade}` — otomatik doğrulama yapılamadı (sözel/şekilli soru); çözümü kontrol et.")
    return temiz + "\n\n---\n### ✅ AREX Matematik Motoru Doğrulaması (SymPy)\n" + \
        "_Aşağıdaki sonuçlar yapay zekâdan bağımsız, kesin sembolik hesapla yeniden bulundu. Yukarıdaki çözümle " \
        "farklıysa bu sonuç esas alınmalı._\n\n" + "\n\n".join(dogrulamalar)


def analiz_yap(veri: bytes, dosya_adi: str, turler: list, not_metni: str = "", dil: str = "Türkçe",
               gecmis: list = None) -> tuple:
    """Seçilen analiz türlerini tek istekte birleştirip çalıştırır. (metin|None, etiket|hata)"""
    tum = {**ANALIZLER, **VIDEO_ANALIZLERI}
    turler = [t for t in (turler or []) if t in tum]
    if turler:
        bolumler = []
        for i, t in enumerate(turler, 1):
            bolumler.append(f"## {i}. {tum[t]['ad']}\n{tum[t]['talimat']}")
        talimat = ("Aşağıdaki analizleri SIRAYLA, her birini kendi başlığı altında yap:\n\n" + "\n\n".join(bolumler))
    else:
        talimat = ("Bu medyayı kullanıcının sorusuna göre yanıtla. Görselde bir ders/sınav sorusu veya ödev varsa onu "
                   "çöz (soruyu yaz, adım adım çöz, sonucu ve doğru şıkkı kalın yaz). Soru yoksa kısa ve faydalı bir "
                   "genel analiz yap.")
    if not_metni.strip():
        talimat += f"\n\nKullanıcının notu / sorusu: {not_metni.strip()}"
    maks = 1800 + 900 * max(0, len(turler) - 1)
    if not any(t.startswith("video") for t in turler):
        talimat += SYMPY_KURALI
    derin = any(t in DERIN_TURLER or t.startswith("video") for t in turler) or len(turler) > 2 or "ders" in turler
    metin, etiket = ai.medya_analiz_et(veri, dosya_adi, talimat, sistem=ETIK_SISTEM.format(dil=dil), gecmis=gecmis,
                                       maks_token=min(maks, 6000), derin=derin)
    if metin:
        metin = _matematik_dogrula(metin)
    return metin, etiket


DERIN_TURLER = {"duygu", "yuz_sekli", "beden", "catisma"}


# ------------------------------------------------------------------------------
# STREAMLIT PANELİ
# ------------------------------------------------------------------------------
def analiz_paneli(sohbete_ekle_fn=None):
    import streamlit as st

    st.markdown("### 🔬 Fotoğraf & Video Analiz Laboratuvarı")
    st.caption("Gemini görsel zekâsıyla sistematik analiz. Kişi tanıma yapılmaz; duygular **görünen ifade** olarak, "
               "kanıt ve güven düzeyiyle raporlanır.")
    dosya = st.file_uploader("Fotoğraf veya kısa video (≤18 MB)",
                             type=["png", "jpg", "jpeg", "webp", "heic", "mp4", "mov", "webm", "3gp"],
                             key="m27_dosya")
    if dosya is None:
        st.info("📸 Bir fotoğraf ya da kısa video seç. Ardından analiz türlerini işaretle.")
        return
    video_mu = (dosya.type or "").startswith("video") or dosya.name.lower().endswith((".mp4", ".mov", ".webm", ".3gp"))
    c1, c2 = st.columns([1, 1.4])
    with c1:
        if video_mu:
            st.video(dosya)
        else:
            st.image(dosya, width=260)
    with c2:
        kaynak = VIDEO_ANALIZLERI if video_mu else ANALIZLER
        varsayilan = ["video_genel"] if video_mu else ["genel"]
        tam = (not video_mu) and st.toggle("🧩 Tam Sistematik Rapor (genel + ifade + yüz şekli + beden + risk + kalite)",
                                          key="m27_tam")
        turler = list(TAM_RAPOR_ANAHTARLARI) if tam else st.multiselect(
            "Analiz türleri", options=list(kaynak.keys()), default=varsayilan,
            format_func=lambda k: kaynak[k]["ad"], key="m27_turler")
        dil = st.selectbox("Rapor dili", list(ai.DIL_ADLARI.values()), index=0, key="m27_dil")
        not_metni = st.text_input("Not / soru (isteğe bağlı)", placeholder="ör. soldaki kişi tedirgin görünüyor mu?",
                                  key="m27_not")
    if st.button("🔬 Analizi Başlat", type="primary", use_container_width=True, key="m27_basla"):
        with st.spinner("🔬 Görsel inceleniyor… (video ise 20-60 sn sürebilir)"):
            metin, etiket = analiz_yap(dosya.getvalue(), dosya.name, turler, not_metni, dil)
        if metin:
            st.session_state["m27_son"] = (metin, etiket, dosya.name)
        else:
            st.error(etiket)
    son = st.session_state.get("m27_son")
    if son and son[2] == dosya.name:
        st.markdown(son[0])
        st.caption(f"🏷️ {son[1]}")
        b1, b2 = st.columns(2)
        b1.download_button("📥 Raporu indir (.md)", son[0], file_name="arex_analiz_raporu.md",
                           use_container_width=True, key="m27_indir")
        if sohbete_ekle_fn and b2.button("💬 Sohbete ekle", use_container_width=True, key="m27_sohbet"):
            sohbete_ekle_fn(f"🔬 {dosya.name} analizi", son[0], f"🔬 {son[1]}")
            st.success("Sohbete eklendi — Sohbet bölümünden devam edebilirsin.")
