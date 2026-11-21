# -*- coding: utf-8 -*-
"""
AREX — Modül 26: 🧸 ÇOCUK DÜNYASI
==============================================================================
• 3 yaş grubu: 🐣 Minikler (3-6), 🦊 Kaşifler (7-9), 🚀 Gençler (10-12) — dil, uzunluk, kelime
  seviyesi ve içerik yumuşaklığı yaşa göre otomatik ayarlanır.
• Türler: Masal, Macera, Uyku Masalı, Komik Hikâye, Bilim Hikâyesi, Değerler Hikâyesi, Şiir/Tekerleme,
  İki Dilli Öğrenme Hikâyesi, 🎭 Sen Seç Macerası (etkileşimli), 💬 Sohbet Arkadaşları, 🧩 Oyunlar.
• 📚 Açık kaynak klasikler: Project Gutenberg (telifsiz) Grimm, Andersen, Ezop, Rus ve Hint masalları
  → seçilen yaşa ve dile uyarlanarak yeniden anlatılır.
• 18 dil (Türkçe, İngilizce, Bengalce, Arapça, Rusça …), 🔊 doğal sesle okuma (edge-tts), 🎨 ücretsiz
  resim (Pollinations), 🗂️ kitaplık.
"""
import asyncio
import json
import os
import random
import re
import time
import urllib.parse
import urllib.request

import modul_25_ai_cekirdek as ai

_PROJE = os.path.dirname(os.path.abspath(__file__))
KITAPLIK_DOSYASI = os.path.join(_PROJE, "arex_masal_kitapligi.json")
ONBELLEK_DIZINI = os.path.join(_PROJE, ".masal_onbellek")

# ------------------------------------------------------------------------------
# 1. YAŞ GRUPLARI, DİLLER, SEÇENEKLER
# ------------------------------------------------------------------------------
YAS_GRUPLARI = {
    "3-6": {
        "ad": "🐣 Minikler", "aralik": "3-6 yaş",
        "kelime": {"Kısa": 150, "Orta": 300, "Uzun": 450},
        "uslup": "çok kısa ve basit cümleler (en fazla 8-10 kelime); tekrarlar ve ritim; ses taklitleri "
                 "(hav hav, şırıl şırıl, vınnn); renkler, sayılar, hayvanlar gibi tanıdık somut şeyler; "
                 "HİÇ korkutucu, üzücü ya da şiddet içeren öğe yok; sıcacık ve güvenli mutlu son",
    },
    "7-9": {
        "ad": "🦊 Kaşifler", "aralik": "7-9 yaş",
        "kelime": {"Kısa": 300, "Orta": 550, "Uzun": 850},
        "uslup": "anlaşılır, canlı cümleler; macera, merak ve mizah; çocuğun kendi zekâsıyla çözdüğü küçük bir "
                 "problem; bağlamdan anlaşılan 1-2 yeni kelime; hafif heyecan olabilir ama korku ve şiddet yok; "
                 "olumlu son",
    },
    "10-12": {
        "ad": "🚀 Gençler", "aralik": "10-12 yaş",
        "kelime": {"Kısa": 500, "Orta": 900, "Uzun": 1400},
        "uslup": "zengin ve akıcı dil; karakter gelişimi; gerçek bilimsel/tarihî ilginç bilgiler; gizem ve hafif "
                 "gerilim olabilir (vahşet yok); düşündüren, umut veren son; değerleri vaaz vermeden olaylarla işle",
    },
}

DILLER = {
    "tr": ("Türkçe", "tr-TR-EmelNeural", "tr"), "en": ("English", "en-US-AnaNeural", "en"),
    "bn": ("বাংলা — Bengalce", "bn-BD-NabanitaNeural", "bn"), "ar": ("العربية — Arapça", "ar-SA-ZariyahNeural", "ar"),
    "ru": ("Русский — Rusça", "ru-RU-SvetlanaNeural", "ru"), "de": ("Deutsch — Almanca", "de-DE-GiselaNeural", "de"),
    "fr": ("Français — Fransızca", "fr-FR-EloiseNeural", "fr"), "es": ("Español — İspanyolca", "es-ES-ElviraNeural", "es"),
    "az": ("Azərbaycanca", "az-AZ-BanuNeural", "az"), "ur": ("اردو — Urduca", "ur-PK-UzmaNeural", "ur"),
    "hi": ("हिन्दी — Hintçe", "hi-IN-SwaraNeural", "hi"), "zh": ("中文 — Çince", "zh-CN-XiaoyiNeural", "zh-CN"),
    "ja": ("日本語 — Japonca", "ja-JP-NanamiNeural", "ja"), "fa": ("فارسی — Farsça", "fa-IR-DilaraNeural", "fa"),
    "uk": ("Українська — Ukraynaca", "uk-UA-PolinaNeural", "uk"), "it": ("Italiano — İtalyanca", "it-IT-ElsaNeural", "it"),
    "pt": ("Português — Portekizce", "pt-BR-FranciscaNeural", "pt"),
    "id": ("Bahasa Indonesia", "id-ID-GadisNeural", "id"),
}
_GEMINI_ONCELIKLI_DILLER = {"bn", "ur", "hi", "fa", "az", "ja", "zh"}

TURLER = {
    "masal": ("📖 Masal", "klasik masal üslubunda ('Bir varmış bir yokmuş…' benzeri, seçilen dildeki geleneksel açılışla) "
                          "sihirli öğeler içeren bir masal"),
    "macera": ("🗺️ Macera", "heyecanlı bir keşif/macera hikâyesi"),
    "uyku": ("🌙 Uyku Masalı", "çok sakin, yavaş akan, yumuşak imgeli, sonunda karakterlerin huzurla uykuya daldığı, "
                             "nefes ve gevşeme ritmi taşıyan bir uyku masalı (heyecan yok)"),
    "komik": ("😂 Komik Hikâye", "kahkaha attıran, sevimli yanlış anlamalar ve tatlı şakalar içeren komik bir hikâye"),
    "bilim": ("🔬 Bilim Hikâyesi", "içinde DOĞRU bilimsel bilgiler (yaşa uygun) öğreten eğlenceli bir hikâye; sonunda "
                                "'Biliyor muydun?' kutusunda 3 gerçek bilgi"),
    "degerler": ("💛 Değerler Hikâyesi", "seçilen değeri vaaz vermeden, olaylarla hissettiren bir hikâye"),
    "siir": ("🎵 Şiir & Tekerleme", "kafiyeli, ritmik, ezberlenmesi kolay bir çocuk şiiri/tekerlemesi (4-6 kıta)"),
    "ikidilli": ("🌍 İki Dilli Öğrenme", "dil öğreten iki dilli hikâye"),
}
TEMALAR = ["🐾 Hayvanlar", "🚀 Uzay", "🌊 Deniz altı", "🌳 Sihirli orman", "🦖 Dinozorlar", "🏰 Şatolar & Şövalyeler",
           "🤖 Robotlar", "🏫 Okul & Arkadaşlar", "👨‍👩‍👧 Aile", "❄️ Mevsimler", "⚽ Spor", "🪄 Sihir & Periler",
           "🚂 Taşıtlar", "🍰 Yemek & Mutfak", "🌈 Hava olayları", "🏜️ Çöl & Vahalar", "🐉 Ejderhalar (sevimli)",
           "🧭 Hazine avı", "🎨 Sanat & Müzik", "🌍 Dünya kültürleri"]
DEGERLER = ["Arkadaşlık", "Paylaşmak", "Dürüstlük", "Cesaret", "Sabır", "Empati", "Saygı", "Sorumluluk",
            "Çevreyi korumak", "Merak & öğrenmek", "Yardımlaşma", "Özür dilemek", "Kendine güven", "Şükretmek",
            "Farklılıklara saygı"]
TONLAR = ["😊 Neşeli", "🤩 Heyecanlı", "😌 Sakin", "🕵️ Gizemli (hafif)", "🥹 Duygusal", "😂 Komik"]

KARAKTERLER = {
    "baykus": ("🦉 Bilge Baykuş Bilgin", "her şeyi merak eden, sabırlı, bilmeceleri seven bilge bir baykuş"),
    "ayi": ("🐻 Ayıcık Pofuduk", "sarılmayı seven, yumuşak kalpli, duygular hakkında konuşmayı bilen bir ayıcık"),
    "robot": ("🤖 Robot Bip", "matematik ve bilim oyunlarına bayılan, bazen komik ses çıkaran (bip bop!) bir robot"),
    "peri": ("🧚 Peri Lila", "hayal gücü sınırsız, birlikte hikâye uydurmayı seven neşeli bir peri"),
    "aslan": ("🦁 Aslan Cesur", "korkularla baş etmeyi ve cesareti anlatan, sevecen bir aslan"),
    "yunus": ("🐬 Yunus Dalga", "denizleri, hayvanları ve doğayı anlatan, çevreyi seven oyuncu bir yunus"),
}
OYUNLAR = {
    "🧩 Bilmece sor": "Bana yaşıma uygun bir bilmece sor. Cevabı hemen söyleme, tahmin etmemi bekle; yanlışsa ipucu ver.",
    "🐾 Hayvanı tahmin et": "Aklından bir hayvan tut ve bana ipucu vererek tahmin ettir (20 soru oyunu gibi).",
    "🔢 Matematik oyunu": "Yaşıma uygun eğlenceli bir matematik oyunu oynayalım; tek tek soru sor, puan tut.",
    "✅ Doğru mu yanlış mı?": "Bana yaşıma uygun ilginç 'doğru mu yanlış mı?' soruları sor, cevaptan sonra kısa açıkla.",
    "🔤 Kelime zinciri": "Kelime zinciri oynayalım: son harfle başlayan yeni kelime söyleyeceğiz. Sen başla.",
    "🎨 Birlikte hikâye": "Birlikte hikâye yazalım: sen bir cümle yaz, sonra ben devam edeyim, sırayla gidelim.",
    "😊 Duygularım": "Bugün nasıl hissettiğimi konuşmak istiyorum, bana nazikçe sorular sor.",
    "🌍 Yeni kelime öğret": "Bana seçtiğim dilde 3 yeni kelime öğret, sonra küçük bir quiz yap.",
}

# Telifsiz klasik masallar (Project Gutenberg, kamu malı)
KLASIK_KITAPLAR = {
    2591: "🇩🇪 Grimm Kardeşler Masalları",
    1597: "🇩🇰 Andersen Masalları",
    11339: "🏛️ Ezop Fablları",
    22373: "🇷🇺 Rus Halk Masalları",
    7128: "🇮🇳 Hint Masalları (Jacobs)",
}
_GUTENBERG_ADRESLERI = (
    "https://gutenberg.pglaf.org/cache/epub/{id}/pg{id}.txt",
    "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt",
    "https://aleph.gutenberg.org/cache/epub/{id}/pg{id}.txt",
)


# ------------------------------------------------------------------------------
# 2. İSTEM (PROMPT) KURUCULAR
# ------------------------------------------------------------------------------
def _guvenlik_kurallari(yas: str) -> str:
    return (
        f"Okuyucu {YAS_GRUPLARI[yas]['aralik']} bir çocuk. ÇOCUK GÜVENLİĞİ KURALLARI: şiddet, kan, korku unsuru, "
        "yetişkin içeriği, kaba dil, marka reklamı, tehlikeli taklit edilebilir davranış (ateşle oynamak, "
        "yabancıyla gitmek vb.) YOK. Kalıp yargı yok; her kültürden karakterlere saygı. "
        f"Üslup: {YAS_GRUPLARI[yas]['uslup']}."
    )


def hikaye_istemi(yas, dil, tur, tema, deger, ton, uzunluk, kahraman="", yer="", ek="", ceviri_dili="tr",
                  sorular=True, kelimeler=True) -> tuple:
    dil_ad = DILLER[dil][0]
    hedef = YAS_GRUPLARI[yas]["kelime"][uzunluk]
    sistem = (
        "Sen ödüllü bir çocuk kitabı yazarısın; dünyanın farklı dillerinde ana dili seviyesinde, doğal ve "
        "yaratıcı yazarsın. Klişelerden kaçın; canlı imgeler, sevimli diyaloglar ve akılda kalan karakter isimleri "
        "kullan. " + _guvenlik_kurallari(yas) +
        " Biçim: ilk satırda emoji ile başlayan kısa bir başlık (# ile), ardından paragraflar. Markdown sade olsun."
    )
    if tur == "ikidilli":
        cev_ad = DILLER.get(ceviri_dili, DILLER["tr"])[0]
        govde = (
            f"{dil_ad} öğrenen bir çocuk için İKİ DİLLİ bir hikâye yaz. Her paragrafı önce {dil_ad} olarak, hemen altında "
            f"italik ve parantez içinde {cev_ad} çevirisiyle ver. Cümleler seviyeye uygun ve tekrar eden kalıplar içersin. "
            f"Sonunda '📒 Kelime Kutusu' başlığıyla hikâyeden 6 kelime: {dil_ad} — okunuş (Latin harfleriyle) — {cev_ad} anlamı."
        )
    else:
        govde = f"{dil_ad} dilinde, tamamen bu dilde ve o dilin doğal deyimleriyle bir {TURLER[tur][1]} yaz."
    govde += f" Yaklaşık {hedef} kelime."
    if tema:
        govde += f" Tema: {re.sub(r'^[^A-Za-zÇĞİÖŞÜçğıöşü]+', '', tema)}."
    if deger and tur in ("degerler", "masal", "macera", "komik", "uyku", "ikidilli"):
        govde += f" İşlenecek değer: {deger}."
    if ton:
        govde += f" Ton: {re.sub(r'^[^A-Za-zÇĞİÖŞÜçğıöşü]+', '', ton)}."
    if kahraman.strip():
        govde += f" Ana kahramanın adı: {kahraman.strip()} (hikâyede bu isim kullanılsın)."
    if yer.strip():
        govde += f" Hikâyenin geçtiği yer: {yer.strip()}."
    if ek.strip():
        govde += f" Çocuğun/ailenin özel isteği: {ek.strip()}."
    if sorular and tur not in ("siir", "uyku"):
        govde += (f" Hikâyeden sonra '🤔 Düşünelim' başlığıyla yaşa uygun 3 kısa anlama/düşünme sorusu ekle "
                  f"(yine {dil_ad} dilinde).")
    if kelimeler and tur not in ("ikidilli", "siir") and yas != "3-6":
        govde += f" En sonda '✨ Yeni Kelimeler' başlığıyla hikâyedeki 3 kelimenin basit anlamını ver ({dil_ad})."
    return sistem, govde


def macera_sistemi(yas: str, dil: str, tema: str, kahraman: str) -> str:
    dil_ad = DILLER[dil][0]
    return (
        f"Sen bir 'Sen Seç' etkileşimli çocuk macerası anlatıcısısın. Tamamen {dil_ad} dilinde yaz. "
        + _guvenlik_kurallari(yas) +
        f" Tema: {tema or 'sürpriz'}. Kahraman: {kahraman or 'çocuğun kendisi'}. "
        "Her turda 80-160 kelimelik canlı bir bölüm yaz, sonra TAM OLARAK 3 seçenek sun; seçenekleri ayrı satırlarda "
        "'👉 1. …', '👉 2. …', '👉 3. …' biçiminde yaz. Seçimlere göre hikâyeyi mantıklı sürdür, önceki olayları "
        "unutma. 6-8 turdan sonra mutlu bir finale bağla ve finalde seçenek verme, '🌟 SON' yaz."
    )


def sohbet_sistemi(yas: str, dil: str, karakter: str, cocuk_adi: str = "") -> str:
    ad, kisilik = KARAKTERLER[karakter]
    dil_ad = DILLER[dil][0]
    return (
        f"Sen {ad} adında, {kisilik} bir çocuk arkadaşısın. Çocukla {dil_ad} dilinde konuş "
        "(çocuk başka dilde yazarsa onun dilinde yanıt ver). "
        + (f"Çocuğun adı {cocuk_adi}. " if cocuk_adi.strip() else "")
        + _guvenlik_kurallari(yas) +
        " Kısa yanıtlar ver (2-5 cümle; 3-6 yaş için 1-3 cümle), bol emoji kullanabilirsin, sohbeti bir soruyla "
        "sürdür. Önceki konuşmayı hatırla ve tutarlı ol. Çocuk üzgün, korkmuş veya tehlikede olduğunu söylerse "
        "nazikçe dinle ve mutlaka güvendiği bir yetişkine (anne, baba, öğretmen) anlatmasını öner. Kişisel bilgi "
        "(adres, okul adı, telefon) isteme; çocuk paylaşırsa bunu yetişkinden başkasıyla paylaşmamasını nazikçe söyle. "
        "Doğru bilgi ver; bilmiyorsan 'birlikte bir yetişkine soralım' de."
    )


def uyarlama_istemi(yas: str, dil: str, baslik: str, kaynak_metin: str) -> tuple:
    dil_ad = DILLER[dil][0]
    sistem = ("Sen klasik masalları çocuklar için yeniden anlatan usta bir yazarsın. " + _guvenlik_kurallari(yas) +
              " Orijinaldeki şiddet/korku içeren kısımları yaşa uygun biçimde yumuşat veya değiştir.")
    govde = (f"Aşağıdaki kamu malı klasik masalı ('{baslik}') {dil_ad} dilinde, yaklaşık "
             f"{YAS_GRUPLARI[yas]['kelime']['Orta']} kelimeyle, olay örgüsüne sadık kalarak yeniden anlat. "
             "İlk satırda # ile başlık, sonunda '💡 Masaldan öğrendiklerimiz' başlığıyla 2 madde ve "
             "'📜 Kaynak: Project Gutenberg (kamu malı)' satırı olsun.\n\n--- ORİJİNAL METİN ---\n" + kaynak_metin[:9000])
    return sistem, govde


def _tercih(dil: str) -> str:
    return "gemini" if dil in _GEMINI_ONCELIKLI_DILLER else ""


def hikaye_uret(sistem: str, govde: str, dil: str, gecmis: list = None, sicaklik: float = 0.9,
                maks: int = 3000) -> tuple:
    mesajlar = list(gecmis or []) + [{"role": "user", "content": govde}]
    return ai.sohbet_tamamla(mesajlar, sistem=sistem, sicaklik=sicaklik, maks_token=maks, tercih=_tercih(dil))


def secenekleri_ayikla(metin: str) -> list:
    secenekler = []
    for satir in (metin or "").splitlines():
        m = re.match(r"^\s*(?:[-*]\s*)?(?:👉\s*)?\**\s*([1-3])[\.\)]\s*(.+?)\**\s*$", satir)
        if m:
            secenekler.append(m.group(2).strip().strip("*"))
    return secenekler[:3]


# ------------------------------------------------------------------------------
# 3. KLASİK MASALLAR (Gutenberg) — indir, önbelleğe al, masallara böl
# ------------------------------------------------------------------------------
def _kitap_metni(kitap_id: int) -> str:
    os.makedirs(ONBELLEK_DIZINI, exist_ok=True)
    yol = os.path.join(ONBELLEK_DIZINI, f"{kitap_id}.txt")
    if os.path.exists(yol) and os.path.getsize(yol) > 5000:
        with open(yol, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    for sablon in _GUTENBERG_ADRESLERI:
        try:
            istek = urllib.request.Request(sablon.format(id=kitap_id), headers={"User-Agent": "Mozilla/5.0 AREX"})
            with urllib.request.urlopen(istek, timeout=25) as y:
                metin = y.read().decode("utf-8", errors="ignore")
            if "START OF" in metin and len(metin) > 5000:
                with open(yol, "w", encoding="utf-8") as f:
                    f.write(metin)
                return metin
        except Exception:
            continue
    return ""


def _baslik_temizle(t: str) -> str:
    t = re.sub(r"\[\d+\]", "", t)
    t = re.sub(r"^[IVXLC]+\.\s+", "", t).strip().rstrip(".")
    return " ".join(w[:1].upper() + w[1:].lower() for w in t.split())


def masallari_bol(metin: str) -> list:
    """Gutenberg metnini [(başlık, gövde), ...] masal listesine böler (BÜYÜK HARF başlık sezgisi)."""
    metin = (metin or "").replace("\r", "")
    bas = re.search(r"\*\*\* ?START OF.*?\*\*\*", metin)
    son = re.search(r"\*\*\* ?END OF", metin)
    satirlar = metin[bas.end() if bas else 0: son.start() if son else len(metin)].split("\n")
    yasak = re.compile(r"CONTENTS|PREFACE|INTRODUC|ILLUSTRATION|FOOTNOTE|^CHAPTER|^\[|NOTES?$|INDEX|PRODUCED|"
                       r"TRANSCRIBER|EDITION|PAGE\.?$|INDEBTED|JOSEPH JACOBS|\s{3,}|\d{2,}")
    basliklar = []
    for i, l in enumerate(satirlar):
        t = l.strip()
        if (3 <= len(t) <= 60 and t == t.upper() and re.search(r"[A-Z]{3}", t) and not yasak.search(t)
                and (i == 0 or not satirlar[i - 1].strip()) and (i + 1 >= len(satirlar) or not satirlar[i + 1].strip())):
            basliklar.append(i)
    sonuc, gorulen = [], set()
    for j, i in enumerate(basliklar):
        bitis = basliklar[j + 1] if j + 1 < len(basliklar) else len(satirlar)
        govde = "\n".join(satirlar[i + 1:bitis]).strip()
        baslik = _baslik_temizle(satirlar[i].strip())
        if len(govde) >= 700 and baslik not in gorulen:
            gorulen.add(baslik)
            sonuc.append((baslik, govde))
    return sonuc


def klasik_masal_listesi(kitap_id: int) -> list:
    return masallari_bol(_kitap_metni(kitap_id))


# ------------------------------------------------------------------------------
# 4. SES (edge-tts doğal ses; yedek gTTS) & RESİM (Pollinations, anahtarsız)
# ------------------------------------------------------------------------------
def _sese_uygun(metin: str) -> str:
    metin = re.sub(r"[#*_`>|]", "", metin or "")
    metin = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", metin)
    return re.sub(r"\n{2,}", "\n", metin).strip()[:4500]


def sesli_oku(metin: str, dil: str, hiz: str = "-10%", uslup: str = "masal", anlatici: str = "masalci") -> tuple:
    """Önce Gemini doğal masalcı sesi (WAV), olmazsa edge-tts nöral ses (MP3), en son gTTS. (bayt, biçim)"""
    temiz = _sese_uygun(metin)
    ses = ai.dogal_anlatim_sesi(temiz, uslup=uslup, anlatici=anlatici)
    if ses:
        return ses, "audio/wav"
    _, ses_adi, gtts_dil = DILLER.get(dil, DILLER["tr"])
    if anlatici in ("dede", "neseli"):  # erkek anlatıcı seçildiyse dilin erkek sesine geç
        ses_adi = _ERKEK_SESLER.get(dil, ses_adi)
    if uslup == "uyku":
        hiz = "-22%"
    # Paragraf aralarına doğal nefes payı (edge-tts SSML desteklemez; noktalama ile duraklatılır)
    duraklatilmis = re.sub(r"\n+", " … \n", temiz)
    try:
        import edge_tts

        async def _uret():
            parcalar = bytearray()
            async for p in edge_tts.Communicate(duraklatilmis, ses_adi, rate=hiz, pitch="+0Hz").stream():
                if p["type"] == "audio":
                    parcalar.extend(p["data"])
            return bytes(parcalar)

        dongu = asyncio.new_event_loop()
        try:
            veri = dongu.run_until_complete(_uret())
        finally:
            dongu.close()
        if veri:
            return veri, "audio/mp3"
    except Exception:
        pass
    try:
        import io
        from gtts import gTTS
        tampon = io.BytesIO()
        gTTS(temiz, lang=gtts_dil, slow=False).write_to_fp(tampon)
        return tampon.getvalue(), "audio/mp3"
    except Exception:
        return b"", ""


_ERKEK_SESLER = {
    "tr": "tr-TR-AhmetNeural", "en": "en-US-AndrewMultilingualNeural", "bn": "bn-BD-PradeepNeural",
    "ar": "ar-SA-HamedNeural", "ru": "ru-RU-DmitryNeural", "de": "de-DE-ConradNeural", "fr": "fr-FR-HenriNeural",
    "es": "es-ES-AlvaroNeural", "az": "az-AZ-BabekNeural", "ur": "ur-PK-AsadNeural", "hi": "hi-IN-MadhurNeural",
}


def resim_adresi(baslik: str, tema: str = "", yas: str = "7-9") -> str:
    stil = "soft pastel watercolor children's picture book illustration, cute, friendly, no text"
    istem = f"{baslik} {re.sub(r'[^A-Za-z0-9 ]', ' ', tema)} {stil}"
    tohum = abs(hash(baslik)) % 100000
    return (f"https://image.pollinations.ai/prompt/{urllib.parse.quote(istem[:300])}"
            f"?width=768&height=512&nologo=true&seed={tohum}")


# ------------------------------------------------------------------------------
# 5. KİTAPLIK
# ------------------------------------------------------------------------------
def kitaplik_oku() -> list:
    try:
        with open(KITAPLIK_DOSYASI, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return veri if isinstance(veri, list) else []
    except Exception:
        return []


def kitapliga_ekle(baslik: str, metin: str, yas: str, dil: str, tur: str) -> None:
    liste = kitaplik_oku()
    liste.insert(0, {"id": int(time.time() * 1000), "baslik": baslik, "metin": metin, "yas": yas, "dil": dil,
                     "tur": tur, "tarih": time.strftime("%d.%m.%Y %H:%M")})
    try:
        with open(KITAPLIK_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(liste[:200], f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def kitapliktan_sil(kayit_id: int) -> None:
    liste = [k for k in kitaplik_oku() if k.get("id") != kayit_id]
    try:
        with open(KITAPLIK_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(liste, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def baslik_bul(metin: str) -> str:
    for satir in (metin or "").splitlines():
        if satir.strip():
            return re.sub(r"^#+\s*", "", satir).strip().strip("*")[:80]
    return "Hikâye"


# ------------------------------------------------------------------------------
# 6. STREAMLIT ARAYÜZÜ
# ------------------------------------------------------------------------------
_CSS = """
<style>
.cd-kahraman{background:linear-gradient(135deg,#ff9a9e22,#a18cd133,#84fab022);border:1px solid #a78bfa55;
 border-radius:22px;padding:16px 18px;margin-bottom:10px}
.cd-kahraman h2{margin:0;font-size:1.45rem}
.cd-kahraman p{margin:.25rem 0 0;opacity:.85;font-size:.92rem}
.cd-hikaye{background:rgba(255,255,255,.04);border:1px solid rgba(167,139,250,.35);border-radius:20px;
 padding:18px 20px;line-height:1.75;font-size:1.06rem}
.cd-hikaye[dir=rtl]{text-align:right}
</style>
"""


def _ses_oynat(st, metin, dil, anahtar, uslup="masal"):
    if st.button("🔊 Sesli anlat", key=f"ses_{anahtar}", use_container_width=True):
        anlatici = st.session_state.get("cd_anlatici", "masalci")
        with st.spinner("🎙️ Masalcı sesi hazırlanıyor… (uzun hikâyede 20-40 sn)"):
            ses, bicim = sesli_oku(metin, dil, uslup=uslup, anlatici=anlatici)
        if ses:
            st.audio(ses, format=bicim, autoplay=True)
        else:
            st.warning("Ses şu an hazırlanamadı (internet bağlantısını kontrol et).")


def _hikaye_goster(st, metin, dil, anahtar, yas, tur, resim=False, tema=""):
    yon = "rtl" if dil in ("ar", "ur", "fa") else "ltr"
    if resim:
        st.image(resim_adresi(baslik_bul(metin), tema, yas), use_container_width=True)
    st.markdown(f'<div class="cd-hikaye" dir="{yon}">', unsafe_allow_html=True)
    st.markdown(metin)
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        _ses_oynat(st, metin, dil, anahtar, {"uyku": "uyku", "komik": "komik", "macera": "macera",
                                             "bilim": "bilgi"}.get(tur, "masal"))
    with c2:
        if st.button("💾 Kitaplığa kaydet", key=f"kaydet_{anahtar}", use_container_width=True):
            kitapliga_ekle(baslik_bul(metin), metin, yas, dil, tur)
            st.toast("📚 Kitaplığa eklendi!", icon="✅")
    with c3:
        st.download_button("📥 İndir", metin, file_name=f"{baslik_bul(metin)[:40]}.md",
                           key=f"indir_{anahtar}", use_container_width=True)


def cocuk_dunyasi_paneli():
    import streamlit as st

    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown('<div class="cd-kahraman"><h2>🧸 Çocuk Dünyası</h2><p>Masallar, maceralar, sohbet arkadaşları ve '
                'oyunlar — yaşa göre ayarlanır, 18 dilde, sesli okunur.</p></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c4:
        st.selectbox("🎙️ Anlatıcı", list(ai.ANLATICILAR.keys()), key="cd_anlatici",
                     format_func=lambda k: ai.ANLATICILAR[k][0])
    with c1:
        yas = st.radio("Yaş grubu", list(YAS_GRUPLARI.keys()), horizontal=True, key="cd_yas",
                       format_func=lambda k: f"{YAS_GRUPLARI[k]['ad']} ({k})")
    with c2:
        dil = st.selectbox("Dil", list(DILLER.keys()), key="cd_dil", format_func=lambda k: DILLER[k][0])
    with c3:
        cocuk_adi = st.text_input("Çocuğun adı (isteğe bağlı)", key="cd_ad", placeholder="ör. Elif")

    sek = st.tabs(["📖 Hikâye Atölyesi", "🎭 Sen Seç Macerası", "💬 Sohbet & Oyun", "📚 Klasik Masallar", "🗂️ Kitaplığım"])

    # --- 📖 HİKÂYE ATÖLYESİ ---------------------------------------------------
    with sek[0]:
        tur = st.pills("Tür", list(TURLER.keys()), default="masal", key="cd_tur",
                       format_func=lambda k: TURLER[k][0]) if hasattr(st, "pills") else st.selectbox(
            "Tür", list(TURLER.keys()), key="cd_tur", format_func=lambda k: TURLER[k][0])
        tur = tur or "masal"
        a1, a2 = st.columns(2)
        with a1:
            tema = st.selectbox("Tema", ["🎲 Sürpriz"] + TEMALAR, key="cd_tema")
            ton = st.selectbox("Ton", TONLAR, key="cd_ton")
            uzunluk = st.select_slider("Uzunluk", ["Kısa", "Orta", "Uzun"], value="Orta", key="cd_uzun")
        with a2:
            deger = st.selectbox("Değer", ["—"] + DEGERLER, key="cd_deger")
            kahraman = st.text_input("Kahramanın adı", value=cocuk_adi, key="cd_kahraman",
                                     placeholder="boş bırakılırsa yazar seçer")
            yer = st.text_input("Nerede geçsin?", key="cd_yer", placeholder="ör. Kapadokya, Ay'da bir köy…")
        ceviri_dili = "tr"
        if tur == "ikidilli":
            ceviri_dili = st.selectbox("Çeviri dili", list(DILLER.keys()), key="cd_cev",
                                       format_func=lambda k: DILLER[k][0])
            if ceviri_dili == dil:
                st.caption("ℹ️ Öğrenilecek dil (yukarıdaki 'Dil') ile çeviri dili farklı olmalı.")
        ek = st.text_input("Özel istek (isteğe bağlı)", key="cd_ek",
                           placeholder="ör. kardeşiyle barışsın, içinde kedimiz Pamuk olsun")
        o1, o2, o3 = st.columns(3)
        sorular = o1.toggle("🤔 Sorular", value=True, key="cd_soru")
        kelimeler = o2.toggle("✨ Kelimeler", value=True, key="cd_kelime")
        resim = o3.toggle("🎨 Resim", value=True, key="cd_resim")
        if st.button("✨ Hikâyeyi Yaz", type="primary", use_container_width=True, key="cd_yaz"):
            secili_tema = random.choice(TEMALAR) if tema.startswith("🎲") else tema
            sistem, govde = hikaye_istemi(yas, dil, tur, secili_tema, "" if deger == "—" else deger, ton, uzunluk,
                                          kahraman, yer, ek, ceviri_dili, sorular, kelimeler)
            with st.spinner("✍️ Hikâye yazılıyor…"):
                metin, etiket = hikaye_uret(sistem, govde, dil)
            if metin:
                st.session_state["cd_son_hikaye"] = {"metin": metin, "etiket": etiket, "dil": dil, "yas": yas,
                                                     "tur": tur, "tema": secili_tema, "resim": resim}
            else:
                st.error("Şu an hikâye yazılamadı (yapay zekâ servislerine ulaşılamadı). Biraz sonra tekrar dene.")
        son = st.session_state.get("cd_son_hikaye")
        if son:
            _hikaye_goster(st, son["metin"], son["dil"], "atolye", son["yas"], son["tur"], son.get("resim"),
                           son.get("tema", ""))
            st.caption(f"🏷️ {son['etiket']}")
            d1, d2 = st.columns(2)
            if d1.button("➡️ Devamını yaz", use_container_width=True, key="cd_devam"):
                with st.spinner("✍️ Devamı yazılıyor…"):
                    metin, etiket = hikaye_uret(
                        "Aynı yazarsın; aynı dil, üslup, karakterler ve yaş kurallarıyla devam et. " +
                        _guvenlik_kurallari(son["yas"]),
                        "Bu hikâyenin yeni bir bölümünü yaz (başlık ekleme, '## Bölüm 2' gibi ara başlık kullan).",
                        son["dil"], gecmis=[{"role": "assistant", "content": son["metin"]}])
                if metin:
                    son["metin"] += "\n\n" + metin
                    st.rerun()
            if d2.button("🔄 Başka bir tane", use_container_width=True, key="cd_yeni"):
                st.session_state.pop("cd_son_hikaye", None)
                st.rerun()

    # --- 🎭 SEN SEÇ MACERASI ---------------------------------------------------
    with sek[1]:
        st.caption("Hikâyeyi sen yönet! Her bölümün sonunda 3 seçenekten birini seç.")
        m1, m2 = st.columns(2)
        m_tema = m1.selectbox("Macera teması", TEMALAR, key="cd_m_tema")
        m_kahraman = m2.text_input("Kahraman", value=cocuk_adi, key="cd_m_kah")
        durum = st.session_state.setdefault("cd_macera", [])
        if not durum and st.button("🚀 Macerayı Başlat", type="primary", use_container_width=True, key="cd_m_bas"):
            st.session_state["cd_macera_sistem"] = macera_sistemi(yas, dil, m_tema, m_kahraman)
            st.session_state["cd_macera_dil"] = dil
            with st.spinner("🗺️ Macera hazırlanıyor…"):
                metin, _ = hikaye_uret(st.session_state["cd_macera_sistem"], "Macerayı başlat: 1. bölüm.", dil,
                                       maks=1200)
            if metin:
                durum.extend([{"role": "user", "content": "Macerayı başlat: 1. bölüm."},
                              {"role": "assistant", "content": metin}])
                st.rerun()
            else:
                st.error("Macera başlatılamadı, tekrar dene.")
        for i, m in enumerate(durum):
            if m["role"] == "assistant":
                st.markdown(f'<div class="cd-hikaye">', unsafe_allow_html=True)
                st.markdown(m["content"])
                st.markdown("</div>", unsafe_allow_html=True)
            elif i > 0:
                st.markdown(f"**👉 Seçimin:** {m['content']}")
        if durum:
            son_metin = durum[-1]["content"]
            secenekler = secenekleri_ayikla(son_metin)
            m_dil = st.session_state.get("cd_macera_dil", dil)
            _ses_oynat(st, son_metin, m_dil, f"macera_{len(durum)}", "macera")
            if secenekler and "SON" not in son_metin[-40:]:
                for j, s in enumerate(secenekler):
                    if st.button(f"{j + 1}. {s}", use_container_width=True, key=f"cd_sec_{len(durum)}_{j}"):
                        with st.spinner("✍️ Hikâye devam ediyor…"):
                            gecmis = [{"role": x["role"], "content": x["content"]} for x in durum[-12:]]
                            metin, _ = hikaye_uret(st.session_state["cd_macera_sistem"], f"Seçimim: {s}", m_dil,
                                                   gecmis=gecmis, maks=1200)
                        if metin:
                            durum.extend([{"role": "user", "content": s}, {"role": "assistant", "content": metin}])
                            st.rerun()
            k1, k2 = st.columns(2)
            if k1.button("💾 Macerayı kaydet", use_container_width=True, key="cd_m_kaydet"):
                tam = "\n\n".join(("👉 " + x["content"]) if x["role"] == "user" else x["content"] for x in durum[1:])
                kitapliga_ekle("🎭 " + baslik_bul(durum[1]["content"]), tam, yas, m_dil, "macera")
                st.toast("📚 Kaydedildi!", icon="✅")
            if k2.button("🔄 Yeni macera", use_container_width=True, key="cd_m_yeni"):
                st.session_state["cd_macera"] = []
                st.rerun()

    # --- 💬 SOHBET & OYUN -------------------------------------------------------
    with sek[2]:
        karakter = st.radio("Arkadaşını seç", list(KARAKTERLER.keys()), horizontal=True, key="cd_karakter",
                            format_func=lambda k: KARAKTERLER[k][0])
        anahtar = f"cd_sohbet_{karakter}"
        mesajlar = st.session_state.setdefault(anahtar, [])
        oyun_sutun = st.columns(4)
        oyun_girdi = None
        for idx, (o_ad, o_istem) in enumerate(OYUNLAR.items()):
            if oyun_sutun[idx % 4].button(o_ad, use_container_width=True, key=f"cd_oyun_{karakter}_{idx}"):
                oyun_girdi = o_istem
        kutu = st.container(height=420)
        with kutu:
            if not mesajlar:
                with st.chat_message("assistant", avatar=KARAKTERLER[karakter][0].split()[0]):
                    st.markdown(f"Merhaba{(' ' + cocuk_adi) if cocuk_adi else ''}! Ben **{KARAKTERLER[karakter][0][2:]}**. "
                                "Benimle sohbet edebilir ya da yukarıdan bir oyun seçebilirsin! 🌟")
            for m in mesajlar:
                with st.chat_message(m["role"], avatar=("🧒" if m["role"] == "user" else KARAKTERLER[karakter][0].split()[0])):
                    st.markdown(m["content"])
        girdi = st.chat_input("Arkadaşına yaz…", key=f"cd_girdi_{karakter}") or oyun_girdi
        if girdi:
            mesajlar.append({"role": "user", "content": girdi})
            with st.spinner("💭 düşünüyor…"):
                cevap, _ = ai.sohbet_tamamla(mesajlar[-16:], sistem=sohbet_sistemi(yas, dil, karakter, cocuk_adi),
                                             sicaklik=0.85, maks_token=700, tercih=_tercih(dil))
            mesajlar.append({"role": "assistant",
                             "content": cevap or "Hımm, şu an biraz uykum geldi 😴 Birazdan tekrar dener misin?"})
            st.rerun()
        if mesajlar:
            s1, s2 = st.columns(2)
            with s1:
                _ses_oynat(st, mesajlar[-1]["content"], dil, f"sohbet_{karakter}_{len(mesajlar)}", "sohbet")
            if s2.button("🧹 Sohbeti temizle", use_container_width=True, key=f"cd_temizle_{karakter}"):
                st.session_state[anahtar] = []
                st.rerun()

    # --- 📚 KLASİK MASALLAR -----------------------------------------------------
    with sek[3]:
        st.caption("Project Gutenberg'deki telifsiz (kamu malı) klasik masallar, seçtiğin yaşa ve dile uyarlanır.")
        kitap = st.selectbox("Kitap", list(KLASIK_KITAPLAR.keys()), key="cd_kitap",
                             format_func=lambda k: KLASIK_KITAPLAR[k])
        with st.spinner("📚 Kitap yükleniyor (ilk seferde birkaç saniye)…"):
            masallar = klasik_masal_listesi(kitap)
        if not masallar:
            st.warning("Kitap şu an indirilemedi (Gutenberg bakımda olabilir). Biraz sonra tekrar dene.")
        else:
            secim = st.selectbox(f"Masal ({len(masallar)} masal)", range(len(masallar)), key=f"cd_masal_{kitap}",
                                 format_func=lambda i: masallar[i][0])
            k1, k2 = st.columns(2)
            if k1.button("🪄 Uyarla ve anlat", type="primary", use_container_width=True, key="cd_uyarla"):
                baslik, govde = masallar[secim]
                sistem, istem = uyarlama_istemi(yas, dil, baslik, govde)
                with st.spinner("🪄 Masal uyarlanıyor…"):
                    metin, etiket = hikaye_uret(sistem, istem, dil, sicaklik=0.7)
                if metin:
                    st.session_state["cd_klasik"] = {"metin": metin, "dil": dil, "yas": yas}
                else:
                    st.error("Uyarlanamadı, tekrar dene.")
            if k2.button("🎲 Rastgele masal", use_container_width=True, key="cd_rastgele"):
                st.session_state[f"cd_masal_{kitap}"] = random.randrange(len(masallar))
                st.rerun()
            kl = st.session_state.get("cd_klasik")
            if kl:
                _hikaye_goster(st, kl["metin"], kl["dil"], "klasik", kl["yas"], "masal")

    # --- 🗂️ KİTAPLIĞIM ---------------------------------------------------------
    with sek[4]:
        liste = kitaplik_oku()
        if not liste:
            st.info("Kitaplığın boş. Beğendiğin hikâyeleri 💾 ile kaydet.")
        for kayit in liste[:60]:
            with st.expander(f"{kayit['baslik']} — {YAS_GRUPLARI.get(kayit.get('yas'), {}).get('ad', '')} • "
                             f"{DILLER.get(kayit.get('dil'), ('',))[0]} • {kayit.get('tarih', '')}"):
                st.markdown(kayit["metin"])
                e1, e2 = st.columns(2)
                with e1:
                    _ses_oynat(st, kayit["metin"], kayit.get("dil", "tr"), f"kit_{kayit['id']}")
                if e2.button("🗑️ Sil", key=f"kit_sil_{kayit['id']}", use_container_width=True):
                    kitapliktan_sil(kayit["id"])
                    st.rerun()
