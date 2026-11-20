# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 19: SORU GENİŞLETME & OLASILIKLI CEVAP VARYANTLARI
(modul_19_cevap_varyantlari.py)
==============================================================================
Ahmet'in yazdığı soru-cevapları (komutlar.json, özel kurallar, profil) genişletir:

  1. Soru genişletme  : Her kayda aynı soruyu farklı söyleyen yeni tetikleyiciler eklenir
                        ("kimim ben" → "beni tanıyor musun", "ben kimim biliyor musun" ...)
  2. Olasılıklı cevap : Kısa sohbet cevaplarında (selam, hal-hatır, veda, teşekkür, kimlik)
                        aynı anlamı taşıyan 4-6 cevap arasından rastgele seçilir; aynı cevap
                        art arda tekrar edilmez.
  3. Bilgi cevapları  : Bilgi/aile/profil cevaplarında İÇERİK DEĞİŞMEZ; yalnızca giriş cümlesi
                        olasılığa göre çeşitlenir (bilgi uydurulmaz).

Tüm varyantlar elle yazılmıştır (kişisel veriler hiçbir dış servise gönderilmez).
"""

import random
import re

__all__ = ["tablolari_genislet", "json_kayitlarini_genislet", "cevabi_cesitlendir"]

# ==============================================================================
# 1. EK TETİKLEYİCİLER (soru genişletme)
# ==============================================================================
EK_TETIKLEYICILER = {
    # --- Özel kurallar ---
    ("ozel", "ailem"): ["ailemi anlat", "ailem hakkında bilgi", "ailemde kimler var", "kaç kardeşim var", "kardeşlerim",
                        "aile bilgilerim", "ailemi tanıyor musun", "anne babam kim", "annem babam kim"],
    ("ozel", "edibe"): ["annemin adı ne", "annemi tanıyor musun", "annem hakkında", "annemi anlat", "anneni tanıyor musun"],
    ("ozel", "hadi"): ["babamın adı ne", "babamı tanıyor musun", "babam hakkında", "babamı anlat", "babam nerede doğdu"],
    ("ozel", "omer"): ["ömer kaç yaşında", "ömeri tanıyor musun", "ömer hakkında", "küçük ömer kim"],
    ("ozel", "kimim"): ["beni tanıyor musun", "ben kimim biliyor musun", "beni tanıyor musun ahmet", "kim olduğumu biliyor musun",
                        "benim hakkımda ne biliyorsun", "seni kim yarattı", "yaratıcın kim", "seni yapan kim", "seni kim tasarladı"],
    ("ozel", "kimsin_ozel"): ["kendini tanıt", "sen nesin", "sen bir robot musun", "sen yapay zeka mısın", "senin adın ne",
                              "adın neydi", "arex kim", "arex kimdir", "arex nedir", "sen kimsin arex"],
    ("ozel", "nasilsin_ozel"): ["nasılsın bakalım", "nasılsın bugün", "iyisin inşallah", "keyfin nasıl", "nasıl gidiyor senin için",
                                "her şey yolunda mı", "iyi misin bugün"],
    ("ozel", "ne_haber_ozel"): ["n'aber", "neler var", "neler oluyor", "ne var ne yok bugün", "hayırdır ne haber"],
    ("ozel", "alimler_ozel"): ["islam alimlerini say", "hangi alimleri biliyorsun", "müslüman bilim insanları", "islam bilginleri"],
    # --- Ahmet profili ---
    ("ahmet", "ahmet_spor"): ["hangi takımı tutuyorum", "tuttuğum takım hangisi", "en sevdiğim futbolcu", "hangi oyunları oynuyorum",
                              "boş zamanlarımda ne yapıyorum", "hobilerim neler"],
    ("ahmet", "ahmet_projeler"): ["hangi projeleri yapıyorum", "projelerim neler", "ne üzerinde çalışıyorum", "projelerimi anlat",
                                  "teknofest projem", "tübitak projem", "drone projem nasıl"],
    ("ahmet", "ahmet_donanim"): ["hangi cihazları kullanıyorum", "elimde hangi kartlar var", "hangi yazılımları kullanıyorum",
                                 "donanımlarımı say"],
    ("ahmet", "ahmet_kim"): ["kaç yaşındayım", "boyum ne kadar", "beni anlatır mısın", "hakkımda bildiklerin"],
    ("ahmet", "ahmet_zihinden_mat"): ["zihinden çarpma tekniğim", "25 ile çarpma tekniği", "hızlı çarpma yöntemim"],
    # --- komutlar.json (öğretilen hafıza) ---
    ("json", "hal_hatir"): ["nasılsın bakalım", "iyi misin bugün", "keyfin yerinde mi"],
    ("json", "kimlik"): ["kendini tanıtır mısın", "sen kimsin söyle", "adını söyler misin", "senin ismin ne"],
    ("json", "proje_durumu"): ["projeler nasıl gidiyor", "proje ne durumda", "çalışmalar ne durumda"],
    ("json", "vedalasma"): ["görüşmek üzere", "hoşçakal", "allaha ısmarladık", "kendine iyi bak", "sonra görüşürüz",
                            "bye", "güle güle"],
    ("json", "tanıtma"): ["ben kimim söyle", "kim olduğumu söyle"],
    ("json", "bilim_insanı_tanıtma"): ["harizmi kimdir", "harezmi kim", "harezmi kimdir", "el harizmi kim", "hârizmî kimdir",
                                       "cebirin kurucusu kim"],
    ("json", "dini_selam"): ["selamün aleyküm", "selamünaleykum", "esselamü aleyküm", "selamın aleyküm", "s.a."],
    ("json", "merhaba_selam"): ["merhaba arex", "merhabalar arex", "hey arex", "selam arex", "hi"],
    ("json", "gunluk_selam"): ["selamlar arex", "slm arex", "selam dostum"],
}

# Kişisel bağlamı olmayan tek kelimelik/geniş tetikleyiciler başka sorulara (kulüp, yarışma bilgisi)
# engel oluyordu → kişisel kalıplarla değiştirilir.
_KALDIRILACAK = {
    ("ahmet", "ahmet_spor"): {"galatasaray"},
    ("ahmet", "ahmet_projeler"): {"teknofest", "tübitak"},
}


def _ekle(liste, yeni):
    gorulen = {x.strip().lower() for x in liste}
    for y in yeni:
        if y.strip().lower() not in gorulen:
            liste.append(y)
            gorulen.add(y.strip().lower())


def tablolari_genislet(ozel_kurallar: dict, ahmet_tabani: dict):
    """Modül 3 tablolarına (yerinde) ek tetikleyiciler ekler; eklenen sayısını döndürür."""
    sayi = 0
    for (tur, anahtar), ekler in EK_TETIKLEYICILER.items():
        tablo, alan = {"ozel": (ozel_kurallar, "tetikleyiciler"), "ahmet": (ahmet_tabani, "kelimeler")}.get(tur, (None, None))
        if tablo is None or anahtar not in tablo:
            continue
        liste = tablo[anahtar][alan]
        once = len(liste)
        for kaldir in _KALDIRILACAK.get((tur, anahtar), ()):
            while kaldir in liste:
                liste.remove(kaldir)
        _ekle(liste, ekler)
        sayi += len(liste) - once
    return sayi


def json_kayitlarini_genislet(veri: dict) -> dict:
    """komutlar.json içeriğini (dosyayı değiştirmeden) ek tetikleyicilerle zenginleştirir."""
    if not isinstance(veri, dict):
        return veri
    for (tur, anahtar), ekler in EK_TETIKLEYICILER.items():
        if tur == "json" and anahtar in veri and isinstance(veri[anahtar].get("kelimeler"), list):
            kopya = dict(veri[anahtar])
            kopya["kelimeler"] = list(kopya["kelimeler"])
            _ekle(kopya["kelimeler"], ekler)
            veri[anahtar] = kopya
    return veri


# ==============================================================================
# 2. TAM CEVAP VARYANTLARI (kısa sohbet cevapları; orijinal metin → alternatifler)
# ==============================================================================
TAM_VARYANTLAR = {
    "Merhaba Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?": [
        "Merhaba Ahmet! 👋 Seni görmek güzel, bugün ne yapıyoruz?",
        "Merhaba! ⚡ Hazırım Ahmet; soru, ödev, proje… ne istersen.",
        "Hoş geldin Ahmet! 😊 Aklında ne var, birlikte bakalım mı?",
        "Merhaba Ahmet! ⚡ Bugün hangi konuda yardımcı olayım?",
    ],
    "Selam Ahmet! ⚡ Hoş geldin, bugün neler yapıyoruz?": [
        "Selam Ahmet! 👋 Bugün neye bakıyoruz?",
        "Selam! ⚡ Buradayım Ahmet, başlayalım mı?",
        "Selamlar Ahmet! 😊 Ders mi, proje mi, sohbet mi?",
        "Selam kardeşim! ⚡ Ne lazım, hemen hallederiz.",
    ],
    "Aleykümselam Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?": [
        "Aleykümselam ve rahmetullah Ahmet! 🌿 Hoş geldin, nasıl yardımcı olayım?",
        "Ve aleykümselam Ahmet! ⚡ Buyur, seni dinliyorum.",
        "Aleykümselam! 😊 Hoş geldin Ahmet, bugün neye bakalım?",
        "Aleykümselam kardeşim! 🌿 Hayırlı olsun, ne yapıyoruz bugün?",
    ],
    "Ben iyiyim elhamdülillah, sen nasılsın Ahmet? ⚡": [
        "Elhamdülillah iyiyim Ahmet, sen nasılsın? ⚡",
        "Çok iyiyim, sorduğun için sağ ol! 😊 Senin günün nasıl geçiyor?",
        "İyiyim elhamdülillah, sistemlerim tıkır tıkır çalışıyor ⚡ Sen nasılsın?",
        "Bomba gibiyim Ahmet! 💪 Sende durumlar nasıl?",
        "İyiyim, seninle konuşunca daha da iyi oldum 😊 Sen nasılsın?",
    ],
    "İyiyim elhamdülillah, senden ne haber Ahmet? ⚡": [
        "İyilik Ahmet, senden ne haber? ⚡",
        "Elhamdülillah iyiyim! 😊 Sende neler var, neler yok?",
        "Her şey yolunda burada ⚡ Sen ne yapıyorsun bakalım?",
        "Benden iyilik! Senden ne haber, ders mi proje mi? 😄",
    ],
    "Günaydın Ahmet! ☀️ Hayırlı, enerjik ve çok verimli bir gün dilerim.": [
        "Günaydın Ahmet! ☀️ Bugün harika şeyler yapacağız.",
        "Hayırlı sabahlar Ahmet! ☀️ Kahvaltını yaptın mı? Güne güçlü başla!",
        "Günaydın! 🌅 Yeni bir gün, yeni hedefler; hazırsan ben de hazırım.",
        "Günaydın Ahmet! ☀️ Bugün için bir planın var mı, birlikte yapalım mı?",
    ],
    "İyi geceler Ahmet! 🌙 Allah rahatlık versin, iyi dinlenmeler.": [
        "İyi geceler Ahmet! 🌙 Güzel uyu, yarın görüşürüz.",
        "Allah rahatlık versin Ahmet 🌙 Dinlen ki yarın enerjik ol!",
        "Hayırlı geceler! 🌙 Bugün çok çalıştın, şimdi dinlenme vakti.",
        "İyi uykular Ahmet 😴🌙 Erken yatmak yarınki sınavlara da iyi gelir.",
    ],
    "Rica ederim Ahmet! ⚡ Her zaman yanındayım, başka bir sorun olursa hemen yazabilirsin.": [
        "Ne demek Ahmet, her zaman! ⚡",
        "Rica ederim! 😊 Başka bir şey lazım olursa buradayım.",
        "Estağfurullah, görevim bu ⚡ Başka sorun var mı?",
        "Ne demek, ne zaman istersen yazabilirsin Ahmet! 🙌",
    ],
    "Rica ederim Ahmet, her zaman yanındayım! ⚡ Başka bir sorumuz veya araştıracağımız bir konu var mı?": [
        "Ne demek Ahmet! ⚡ Başka araştıracağımız bir şey var mı?",
        "Rica ederim! 😊 Sıradaki konu ne?",
        "Her zaman! ⚡ Başka bir sorun olursa çekinme.",
    ],
    "Görüşmek üzere Ahmet! ⚡ Kendine çok iyi bak, ihtiyaç duyduğunda buradayım.": [
        "Görüşürüz Ahmet! 👋 Kendine iyi bak.",
        "Hoşça kal Ahmet! ⚡ Ne zaman istersen buradayım.",
        "Allah'a emanet ol Ahmet 🌿 Görüşmek üzere!",
        "Görüşürüz! 😊 Derslerinde başarılar, yine bekliyorum.",
    ],
    "Benim adım Ar. Ahmet tarafından Python ve Streamlit kullanılarak geliştirilen akıllı bir yapay zeka asistanıyım.": [
        "Ben **AREX**! ⚡ Ahmet'in Python ve Streamlit ile geliştirdiği akıllı yapay zekâ asistanıyım.",
        "Adım **AREX**. Ahmet tarafından geliştirilmiş, matematikten çeviriye birçok işte yardımcı olan bir asistanım 🤖",
        "Merhaba, ben **AREX AI**! Ahmet'in Python ve Streamlit ile kodladığı Türkçe yapay zekâ asistanıyım ⚡",
        "Ben **AREX** — Ahmet'in eseri, senin yardımcın! Sohbet, ders, matematik, çeviri… hepsi bende 😊",
    ],
    "Ben **Ar** ⚡! Ahmet tarafından Python ve Streamlit ile geliştirilen 500.000+ kalıplı yapay zeka asistanı, matematik öğretmeni ve bilgi merkeziyim. Sana nasıl yardımcı olabilirim?": [
        "Ben **AREX** ⚡! Ahmet tarafından Python ve Streamlit ile geliştirilen 500.000+ kalıplı yapay zekâ asistanı, matematik öğretmeni ve bilgi merkeziyim. Sana nasıl yardımcı olabilirim?",
        "Ben **AREX AI** 🤖 Ahmet'in geliştirdiği; sohbet eden, matematik çözen, çeviri yapan ve güncel bilgi getiren bir asistanım. Ne yapalım?",
        "Adım **AREX**! ⚡ Ahmet'in Python ile kodladığı yapay zekâ asistanıyım; ders, proje, sohbet… hepsinde yanındayım.",
    ],
    "Aleykümselam Ahmet! ⚡ Hoş geldin, bugün sana nasıl yardımcı olabilirim?": [
        "Aleykümselam ve rahmetullah Ahmet! 🌿 Hoş geldin, nasıl yardımcı olayım?",
        "Ve aleykümselam Ahmet! ⚡ Buyur, seni dinliyorum.",
        "Aleykümselam! 😊 Hoş geldin Ahmet, bugün neye bakalım?",
        "Aleykümselam kardeşim! 🌿 Hayırlı olsun, ne yapıyoruz bugün?",
    ],
    "sen beni tasarlayan insansın ismin Ahmet": [
        "Sen beni tasarlayan kişisin, adın **Ahmet**! ⚡",
        "Sen **Ahmet**'sin, beni geliştiren yazılımcı 😊",
        "Seni nasıl tanımam! Beni tasarlayan **Ahmet**'sin 💙",
    ],
    "⚡ **Eyvallah Ahmet, cansın!** Beraber çok güzel işler başaracağız inşallah!": [
        "💙 **Ben de seni Ahmet!** Birlikte daha çok şey başaracağız inşallah!",
        "⚡ **Sağ ol kardeşim, cansın!** Seninle çalışmak çok keyifli.",
        "😊 **Eyvallah Ahmet!** Takımız biz, daha nice projeye!",
    ],
}

# ==============================================================================
# 3. BİLGİ CEVAPLARINA OLASILIKLI GİRİŞ CÜMLELERİ (içerik değişmez)
# ==============================================================================
_GIRISLER = {
    "Özel Kural: ailem": ["Ailenden bahsedeyim 💙", "Tabii, ailen hakkında bildiklerim:", "Hemen anlatayım:"],
    "Özel Kural: hadi": ["Baban Hadi Bey hakkında bildiklerim:", "Tabii, anlatayım:"],
    "Özel Kural: edibe": ["Annen Edibe Hanım hakkında bildiklerim 💙", "Tabii, anlatayım:"],
    "Özel Kural: omer": ["Küçük Ömer'i nasıl unuturum 😄", "Ömer hakkında bildiklerim:"],
    "Özel Kural: kimim": ["Seni nasıl tanımam! 😊", "Tabii ki biliyorum:", "Elbette!"],
    "Ahmet Profili": ["Senin hakkında bildiklerim:", "Hemen hatırlatayım:", "Tabii, işte:"],
    "Öğretilen Hafıza": ["Bana öğrettiğin bilgiye göre:", "Hafızamdaki bilgi şöyle:", "Hatırlıyorum, şöyle:"],
    "Bilgi Bankası": ["Hemen anlatayım:", "Kısaca şöyle:", "İşte bildiklerim:", "Tabii:"],
    "Âlim": ["Bu büyük âlimi anlatayım:", "Hafızamdaki bilgiler:"],
}
# Eski adı ("Ar") içeren orijinaller havuza alınmaz → kimlik cevapları hep "AREX" der
_ORIJINALI_KULLANMA = {k for k in TAM_VARYANTLAR if re.search(r"\bAr\b(?!\w)|\*\*Ar\*\*", k)}
_SELAM_BASI = re.compile(r"^(?:merhaba|selam|aleyküm|aleykum|günaydın|hoş geldin)", re.I)
_GIRIS_OLASILIGI = 0.55          # bilgi cevaplarının ~yarısında giriş cümlesi
_SON_SECIM = {}                  # aynı cevabın art arda gelmesini önler


def _sec(havuz, anahtar):
    if len(havuz) > 1 and _SON_SECIM.get(anahtar) in havuz:
        havuz = [h for h in havuz if h != _SON_SECIM[anahtar]]
    secim = random.choice(havuz)
    _SON_SECIM[anahtar] = secim
    return secim


def cevabi_cesitlendir(cevap: str, etiket: str = "") -> str:
    """Yerel kaynaklı cevabı olasılığa göre çeşitlendirir; AI/canlı kaynak cevaplarına dokunmaz."""
    if not cevap or not isinstance(cevap, str):
        return cevap
    # 1) Kısa sohbet cevapları: orijinal + varyantlar arasından rastgele (eşit olasılık)
    def havuz(orijinal):
        return (TAM_VARYANTLAR[orijinal] if orijinal in _ORIJINALI_KULLANMA
                else [orijinal] + TAM_VARYANTLAR[orijinal])
    if cevap in TAM_VARYANTLAR:
        return _sec(havuz(cevap), cevap)
    for orijinal in TAM_VARYANTLAR:  # selam öneki eklenmiş hâller
        if len(orijinal) > 30 and cevap.endswith(orijinal):
            onek = cevap[: -len(orijinal)]
            if _SELAM_BASI.match(orijinal) and _SELAM_BASI.match(onek.strip()):
                onek = ""  # "Merhaba Ahmet! Merhaba Ahmet!" gibi çift selamı önle
            return onek + _sec(havuz(orijinal), orijinal)
    # 2) Bilgi cevapları: içerik aynı, giriş cümlesi olasılıklı
    etiket = etiket or ""
    for onek, girisler in _GIRISLER.items():
        if onek in etiket:
            if (cevap.lstrip().startswith(("#", "|", "```")) or len(cevap) < 25
                    or random.random() > _GIRIS_OLASILIGI):
                return cevap
            return f"{_sec(girisler, onek)}\n\n{cevap}"
    return cevap
