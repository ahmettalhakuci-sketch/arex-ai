# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.8 — MODÜL 12: GÜNCEL FİYAT & ÜRÜN KARŞILAŞTIRMA MOTORU
Epey (epey.com), Cimri (cimri.com) ve Akakçe (akakce.com) Üzerinden
Canlı Fiyat Taraması, Doğrudan Arama Bağlantıları ve Elektronik Referans Fiyatları
==============================================================================
"""
import importlib.util
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import streamlit as st

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
if _MODUL_DIZINI not in sys.path:
    sys.path.insert(0, _MODUL_DIZINI)


def _guvenli_modul_yukle(modul_adi: str):
    if modul_adi in sys.modules and getattr(sys.modules[modul_adi], "__file__", None):
        return sys.modules[modul_adi]
    yol = os.path.join(_MODUL_DIZINI, f"{modul_adi}.py")
    if os.path.exists(yol):
        spec = importlib.util.spec_from_file_location(modul_adi, yol)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[modul_adi] = mod
            spec.loader.exec_module(mod)
            return mod
    return __import__(modul_adi)


_m1 = _guvenli_modul_yukle("modul_1_arayuz_ve_tema")
bilgi_karti_olustur = _m1.bilgi_karti_olustur

# Siteler bot korumasına (Cloudflare) takılırsa bile Ahmet'in projelerinde kullandığı
# donanımlar için yaklaşık piyasa referans aralıkları + doğrudan canlı linkler verilir.
REFERANS_FIYAT_ARALIKLARI = {
    "arduino uno": ("Arduino Uno R3 (CH340 / Orijinal)", "180 TL – 950 TL"),
    "arduino nano": ("Arduino Nano V3", "140 TL – 450 TL"),
    "esp32": ("ESP32 Wi-Fi + Bluetooth Geliştirme Kartı", "220 TL – 480 TL"),
    "raspberry pi 5": ("Raspberry Pi 5 (4GB / 8GB)", "3.100 TL – 4.600 TL"),
    "hc-sr04": ("HC-SR04 Ultrasonik Mesafe Sensörü", "45 TL – 95 TL"),
    "l298n": ("L298N Çift H-Köprüsü Motor Sürücü", "85 TL – 190 TL"),
}


def urun_adi_ayikla(kullanici_girdisi: str) -> str:
    """Sorgudan 'fiyat:', 'cimri:', 'epey:', 'ne kadar', 'kaç tl' gibi ekleri temizler."""
    temiz = kullanici_girdisi.strip()
    temiz = re.sub(
        r"^(?:fiyat|fiyatı|fiyati|cimri|epey|akakçe|akakce|piyasa|kaç para|kac para)\s*[:\-]?\s*",
        "",
        temiz,
        flags=re.IGNORECASE,
    ).strip()
    temiz = re.sub(
        r"\s+(?:fiyatı\s+ne\s+kadar|fiyati\s+ne\s+kadar|fiyatları|fiyatlari|fiyatı|fiyati|fiyat|ne\s+kadar|kaç\s+tl|kac\s+tl|kaç\s+para|kac\s+para|nerede\s+ucuz|en\s+ucuz)\s*\??$",
        "",
        temiz,
        flags=re.IGNORECASE,
    ).strip()
    return temiz.strip("?!.,;:\"' ")


def _html_fiyat_tara(url: str, timeout: int = 5) -> list:
    """Hedef fiyat sitesinden TL (₺) formatındaki güncel fiyatları çekmeyi dener."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        html_icerik = resp.read().decode("utf-8", errors="ignore")

    # 1. JSON-LD içindeki price alanlarını ara
    bulunanlar = []
    for m in re.findall(r'"(?:lowPrice|price)"\s*:\s*"?([0-9][0-9\.,]{1,12})"?', html_icerik):
        temiz_sayi = m.strip()
        if temiz_sayi and temiz_sayi not in bulunanlar:
            bulunanlar.append(f"{temiz_sayi} TL")
        if len(bulunanlar) >= 5:
            break

    # 2. Ekranda görünen "12.499,00 TL" veya "12.499 ₺" kalıplarını ara
    if not bulunanlar:
        for m in re.findall(r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(?:TL|₺)", html_icerik):
            if m not in bulunanlar:
                bulunanlar.append(f"{m} TL")
            if len(bulunanlar) >= 5:
                break
    return bulunanlar


def guncel_fiyat_arastir(sorgu: str) -> dict:
    """
    Epey, Cimri ve Akakçe üzerinden ürünün güncel fiyat bağlantılarını ve
    erişilebilen canlı fiyat etiketlerini toplar.
    """
    urun = urun_adi_ayikla(sorgu)
    if not urun:
        return {"basarili": False, "hata": "Lütfen fiyatını öğrenmek istediğiniz ürünün adını yazın."}

    q_plus = urllib.parse.quote_plus(urun)
    q_pct = urllib.parse.quote(urun)

    kaynaklar = [
        {
            "ad": "Cimri",
            "ikon": "🏷️",
            "url": f"https://www.cimri.com/arama?q={q_plus}",
            "rol": "Mağaza Fiyat Karşılaştırma",
        },
        {
            "ad": "Epey",
            "ikon": "📊",
            "url": f"https://www.epey.com/ara/?ara={q_plus}",
            "rol": "Teknik Özellik & Fiyat Puanı",
        },
        {
            "ad": "Akakçe",
            "ikon": "🛒",
            "url": f"https://www.akakce.com/arama/?q={q_pct}",
            "rol": "En Ucuz Satıcı Takibi",
        },
    ]

    canli_sonuclar = {}
    for k in kaynaklar:
        try:
            fiyatlar = _html_fiyat_tara(k["url"], timeout=4)
            if fiyatlar:
                canli_sonuclar[k["ad"]] = fiyatlar
        except Exception:
            pass

    urun_kucuk = urun.replace("İ", "i").replace("I", "ı").lower().strip()
    referans_bilgi = None
    for anahtar, (baslik, aralik) in REFERANS_FIYAT_ARALIKLARI.items():
        if anahtar in urun_kucuk or urun_kucuk in anahtar:
            referans_bilgi = (baslik, aralik)
            break

    return {
        "basarili": True,
        "urun": urun,
        "kaynaklar": kaynaklar,
        "canli_sonuclar": canli_sonuclar,
        "referans_bilgi": referans_bilgi,
    }


def fiyat_sonucunu_metne_formatla(sonuc: dict) -> str:
    """Sohbet penceresi için düzenli ve tıklanabilir Epey/Cimri/Akakçe fiyat kartı üretir."""
    if not sonuc.get("basarili"):
        return f"🏷️ **Fiyat Motoru:** {sonuc.get('hata', 'Ürün bulunamadı.')}"

    urun = sonuc["urun"]
    satirlar = [
        f"### 🏷️ Güncel Fiyat & Karşılaştırma: **{urun}**",
    ]

    canli = sonuc.get("canli_sonuclar", {})
    if canli:
        satirlar.append("**⚡ Canlı Yakalanan Fiyat Etiketleri:**")
        for site_adi, liste in canli.items():
            satirlar.append(f"- **{site_adi}:** " + " | ".join(f"`{f}`" for f in liste[:4]))
    else:
        satirlar.append(
            "ℹ️ *Cimri ve Epey gibi siteler bot koruması kullandığı için anlık en güncel satıcı fiyatını doğrudan aşağıdaki resmi arama sayfalarından açabilirsin:*"
        )

    if sonuc.get("referans_bilgi"):
        r_ad, r_aralik = sonuc["referans_bilgi"]
        satirlar.append(f"\n**🔧 Donanım Referans Bandı ({r_ad}):** `{r_aralik}`")

    satirlar.append("\n**🔗 Doğrudan Fiyat & Özellik Karşılaştırma Bağlantıları:**")
    for k in sonuc["kaynaklar"]:
        satirlar.append(f"- {k['ikon']} **[{k['ad']} — {urun} Ara]({k['url']})** *({k['rol']})*")

    return "\n".join(satirlar)


def fiyat_studyosu_goster():
    st.markdown("#### 🏷️ Güncel Fiyat & Teknik Karşılaştırma (Epey • Cimri • Akakçe)")
    st.caption("💡 İpucu: Bunu kullanabileceğin gibi doğrudan **Ana Sohbet Botuna** `fiyat: Samsung S25` veya `Arduino Uno ne kadar?` yazarak da sorabilirsin!")

    fh1, fh2, fh3, fh4 = st.columns(4)
    secili = None
    if fh1.button("📱 Samsung Galaxy S25", use_container_width=True):
        secili = "Samsung Galaxy S25"
    if fh2.button("🍓 Raspberry Pi 5", use_container_width=True):
        secili = "Raspberry Pi 5"
    if fh3.button("🔌 Arduino Uno", use_container_width=True):
        secili = "Arduino Uno"
    if fh4.button("🎮 PlayStation 5 Slim", use_container_width=True):
        secili = "PlayStation 5 Slim"

    aranan_urun = st.text_input(
        "Fiyatını ve Özelliklerini Karşılaştırmak İstediğin Ürün:",
        value=secili or st.session_state.get("son_fiyat_urunu", "Raspberry Pi 5"),
        placeholder="Örn: iPhone 15, RTX 4060, ESP32, Samsung Tab S10+...",
    )
    if st.button("🔍 Epey, Cimri ve Akakçe'de Araştır", use_container_width=True) or secili:
        hedef_urun = secili or aranan_urun
        st.session_state["son_fiyat_urunu"] = hedef_urun
        with st.spinner(f"🏷️ '{hedef_urun}' için Cimri, Epey ve Akakçe taranıyor..."):
            sonuc = guncel_fiyat_arastir(hedef_urun)
        st.session_state["son_fiyat_sonuc"] = sonuc

    aktif_fiyat = st.session_state.get("son_fiyat_sonuc")
    if aktif_fiyat and aktif_fiyat.get("basarili"):
        st.markdown(fiyat_sonucunu_metne_formatla(aktif_fiyat))
        c1, c2, c3 = st.columns(3)
        for idx, k in enumerate(aktif_fiyat["kaynaklar"]):
            with (c1 if idx == 0 else (c2 if idx == 1 else c3)):
                st.link_button(f"{k['ikon']} {k['ad']}'de Aç", k["url"], use_container_width=True)


# ==============================================================================
# 2. AÇIK KAYNAK ADRES & KONUM MOTORU (OpenStreetMap Nominatim + Photon Komoot)
#    Link açmaya zorlamaz; doğrudan neresi olduğunu, il/ilçe/mahalle/cadde/posta
#    kodunu ve açık adresini sohbetin içinde net Türkçe cümlelerle yazar!
# ==============================================================================
MEKAN_TURU_TR = {
    "place_of_worship": "İbadethane / Cami",
    "mosque": "Tarihi / Merkezi Cami",
    "attraction": "Turistik ve Tarihi Mekan",
    "museum": "Müze",
    "monument": "Anıt / Tarihi Yapı",
    "tower": "Tarihi Kule / Seyir Noktası",
    "square": "Meydan",
    "park": "Park ve Yeşil Alan",
    "aerodrome": "Havalimanı",
    "airport": "Havalimanı",
    "university": "Üniversite",
    "school": "Okul / Eğitim Kurumu",
    "hospital": "Hastane / Sağlık Kurumu",
    "stadium": "Stadyum / Spor Kompleksi",
    "mall": "Alışveriş Merkezi",
    "station": "Ulaşım İstasyonu",
    "city": "Şehir / İl Merkezi",
    "town": "İlçe / Kasaba",
    "suburb": "İlçe / Semt",
    "neighbourhood": "Mahalle",
    "administrative": "İdari Bölge (İl / İlçe)",
}

YEDEK_ADRESLER = {
    "ayasofya": {
        "ad": "Ayasofya-i Kebir Cami-i Şerifi",
        "tur": "Tarihi Cami ve Dünya Mirası",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Sultan Ahmet Mahallesi",
        "cadde": "Ayasofya Meydanı No:1",
        "posta_kodu": "34122",
        "aciklama": "İstanbul'un Tarihi Yarımada bölgesinde, Fatih ilçesi Sultanahmet Meydanı'nda yer alan; 537 yılında inşa edilip 1453'te Fatih Sultan Mehmet tarafından camiye çevrilen simge yapıdır.",
        "ulasim": "T1 Kabataş-Bağcılar Tramvay Hattı ile 'Sultanahmet' durağında inerek 2 dakikada yürüyerek ulaşılabilir.",
        "lat": "41.008583",
        "lon": "28.980175",
    },
    "galata kulesi": {
        "ad": "Galata Kulesi",
        "tur": "Tarihi Kule ve Müze",
        "il": "İstanbul",
        "ilce": "Beyoğlu",
        "mahalle": "Bereketzade Mahallesi",
        "cadde": "Büyük Hendek Caddesi",
        "posta_kodu": "34421",
        "aciklama": "İstanbul'un Beyoğlu ilçesinde, Karaköy ile İstiklal Caddesi arasında bulunan ve 1348 yılında Cenevizliler tarafından inşa edilen tarihi seyir kulesidir.",
        "ulasim": "M2 Yenikapı-Hacıosman Metrosu 'Şişhane' durağından 5 dakika yürüyerek veya Karaköy Tünel ile ulaşılabilir.",
        "lat": "41.025658",
        "lon": "28.974155",
    },
    "fatih camii": {
        "ad": "Fatih Camii ve Külliyesi",
        "tur": "Tarihi Selâtin Camii",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Ali Kuşçu Mahallesi",
        "cadde": "Hattat Nafiz Caddesi No:6 (Fevzipaşa Caddesi yanı)",
        "posta_kodu": "34083",
        "aciklama": "İstanbul'un Fatih ilçesinde, Fatih Sultan Mehmet tarafından 1463-1470 yılları arasında yaptırılan ve avlusunda Fatih Sultan Mehmet'in türbesinin bulunduğu büyük külliyedir.",
        "ulasim": "Fevzipaşa Caddesi üzerinden geçen İETT otobüsleriyle 'Fatih' durağında inerek doğrudan ulaşılabilir.",
        "lat": "41.019722",
        "lon": "28.949722",
    },
    "taksim": {
        "ad": "Taksim Meydanı",
        "tur": "Merkezi Meydan ve Ulaşım Noktası",
        "il": "İstanbul",
        "ilce": "Beyoğlu",
        "mahalle": "Gümüşsuyu / Kocatepe Mahallesi",
        "cadde": "Taksim Meydanı ve İstiklal Caddesi Başlangıcı",
        "posta_kodu": "34435",
        "aciklama": "İstanbul'un Beyoğlu ilçesinde yer alan, İstiklal Caddesi'nin başlangıcı ve Cumhuriyet Anıtı ile Atatürk Kültür Merkezi'ne ev sahipliği yapan en bilinen meydandır.",
        "ulasim": "M2 Metrosu 'Taksim' durağı veya F1 Kabataş-Taksim Füniküleri ile doğrudan çıkılabilir.",
        "lat": "41.036944",
        "lon": "28.985000",
    },
    "sultanahmet": {
        "ad": "Sultanahmet Camii ve Meydanı",
        "tur": "Tarihi Cami ve Meydan",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Binbirdirek / Sultan Ahmet Mahallesi",
        "cadde": "At Meydanı Caddesi No:7",
        "posta_kodu": "34122",
        "aciklama": "İstanbul Fatih'te, 1609-1617 yılları arasında Sultan I. Ahmed tarafından Mimar Sedefkâr Mehmed Ağa'ya yaptırılan 6 minareli tarihi cami ve meydandır.",
        "ulasim": "T1 Tramvay Hattı 'Sultanahmet' durağının hemen karşısındadır.",
        "lat": "41.005409",
        "lon": "28.976813",
    },
    "süleymaniye": {
        "ad": "Süleymaniye Camii ve Külliyesi",
        "tur": "Tarihi Selâtin Camii",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Süleymaniye Mahallesi",
        "cadde": "Prof. Sıddık Sami Onar Caddesi No:1",
        "posta_kodu": "34116",
        "aciklama": "Mimar Sinan'ın 'kalfalık eserim' dediği, Kanuni Sultan Süleyman adına 1551-1557 yıllarında İstanbul Fatih'te Haliç'e hâkim tepede inşa edilen görkemli külliyedir.",
        "ulasim": "M2 Metrosu 'Vezneciler' durağından veya T1 'Beyazıt-Kapalıçarşı' durağından yaklaşık 10 dakika yürüyerek ulaşılabilir.",
        "lat": "41.016111",
        "lon": "28.964167",
    },
    "topkapı sarayı": {
        "ad": "Topkapı Sarayı Müzesi",
        "tur": "Tarihi Osmanlı Sarayı ve Müze",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Cankurtaran Mahallesi",
        "cadde": "Bab-ı Hümayun Caddesi",
        "posta_kodu": "34122",
        "aciklama": "Osmanlı İmparatorluğu'nun yaklaşık 400 yıl boyunca yönetim merkezi ve padişahların ikametgâhı olmuş, Sarayburnu'nda Boğaz ile Haliç'e bakan tarihi saraydır.",
        "ulasim": "T1 Tramvay Hattı 'Gülhane' veya 'Sultanahmet' durağından yürüyerek ulaşılabilir.",
        "lat": "41.011519",
        "lon": "28.983379",
    },
    "kapalıçarşı": {
        "ad": "Kapalıçarşı (Grand Bazaar)",
        "tur": "Tarihi Kapalı Çarşı",
        "il": "İstanbul",
        "ilce": "Fatih",
        "mahalle": "Beyazıt Mahallesi",
        "cadde": "Kalpakçılar Caddesi No:22",
        "posta_kodu": "34126",
        "aciklama": "1461 yılında Fatih Sultan Mehmet döneminde kurulan, 4.000'e yakın dükkânıyla dünyanın en eski ve en büyük kapalı çarşılarından biridir.",
        "ulasim": "T1 Tramvay Hattı 'Beyazıt-Kapalıçarşı' durağında inilerek hemen giriş kapısına ulaşılır.",
        "lat": "41.010685",
        "lon": "28.968068",
    },
    "eyüp sultan": {
        "ad": "Eyüp Sultan Camii ve Türbesi",
        "tur": "Tarihi Cami ve Ziyaretgah",
        "il": "İstanbul",
        "ilce": "Eyüpsultan",
        "mahalle": "Merkez Mahallesi",
        "cadde": "Cami Kebir Caddesi No:1",
        "posta_kodu": "34050",
        "aciklama": "İstanbul'un fethinden sonra 1458'de inşa edilen ve Hz. Muhammed'in (s.a.v.) sahabesi Ebû Eyyûb el-Ensârî'nin türbesinin yer aldığı tarihi camidir.",
        "ulasim": "T5 Cibali-Alibeyköy Tramvayı 'Eyüpsultan Teleferik' durağından veya Haliç vapurlarıyla ulaşılabilir.",
        "lat": "41.048056",
        "lon": "28.933889",
    },
    "kız kulesi": {
        "ad": "Kız Kulesi",
        "tur": "Tarihi Deniz Kulesi ve Müze",
        "il": "İstanbul",
        "ilce": "Üsküdar",
        "mahalle": "Salacak Mahallesi",
        "cadde": "Salacak Mevkii (İstanbul Boğazı Adacığı)",
        "posta_kodu": "34668",
        "aciklama": "İstanbul Boğazı'nın Marmara Denizi'ne açılan noktasında, Üsküdar Salacak açıklarındaki küçük adacık üzerinde yer alan simge kuledir.",
        "ulasim": "Üsküdar Salacak iskelesinden veya Galataport'tan kalkan teknelerle geçilebilir.",
        "lat": "41.021111",
        "lon": "29.004167",
    },
    "anıtkabir": {
        "ad": "Anıtkabir",
        "tur": "Anıt Mezar ve Müze",
        "il": "Ankara",
        "ilce": "Çankaya",
        "mahalle": "Yücetepe Mahallesi",
        "cadde": "Akdeniz Caddesi No:31 (Anıttepe)",
        "posta_kodu": "06570",
        "aciklama": "Türkiye Cumhuriyeti'nin kurucusu Mustafa Kemal Atatürk'ün anıt mezarının ve Kurtuluş Savaşı Müzesi'nin bulunduğu, Ankara Çankaya Anıttepe'deki anıtsal komplekstir.",
        "ulasim": "Ankara Ankaray 'Anadolu/Anıtkabir' durağından 8 dakika yürüyerek ulaşılabilir.",
        "lat": "39.925054",
        "lon": "32.836944",
    },
    "atatürk havalimanı": {
        "ad": "Atatürk Havalimanı (TEKNOFEST & Millet Bahçesi Alanı)",
        "tur": "Havacılık ve Etkinlik Alanı",
        "il": "İstanbul",
        "ilce": "Bakırköy",
        "mahalle": "Yeşilköy Mahallesi",
        "cadde": "Atatürk Havalimanı Caddesi",
        "posta_kodu": "34149",
        "aciklama": "İstanbul Bakırköy Yeşilköy'de yer alan, TEKNOFEST havacılık ve teknoloji festivallerine ev sahipliği yapan tarihi havalimanı alanıdır.",
        "ulasim": "M1A Yenikapı-Atatürk Havalimanı Metrosu ile son durakta inilerek doğrudan ulaşılabilir.",
        "lat": "40.976922",
        "lon": "28.814606",
    },
    "mardin": {
        "ad": "Mardin Şehir Merkezi (Eski Mardin)",
        "tur": "Tarihi Şehir / İl Merkezi",
        "il": "Mardin",
        "ilce": "Artuklu",
        "mahalle": "1. Cadde (Tarihi Taş Evler Bölgesi)",
        "cadde": "Cumhuriyet Meydanı & 1. Cadde",
        "posta_kodu": "47100",
        "aciklama": "Güneydoğu Anadolu Bölgesi'nde Mezopotamya Ovası'na bakan yamaçta kurulu, sarı kalker taşından yapılmış tarihi evleri, medreseleri (Zinciriye, Kasımiye) ve kadim kültürüyle ünlü şehirdir.",
        "ulasim": "Mardin Prof. Dr. Aziz Sancar Havalimanı'ndan şehir merkezine yaklaşık 20 dakikada ulaşılabilir.",
        "lat": "37.312900",
        "lon": "40.733950",
    },
}


def yer_adi_ayikla(kullanici_girdisi: str) -> str:
    temiz = kullanici_girdisi.strip()
    temiz = re.sub(r"^(?:adres|konum|harita|yol tarifi|yer)\s*[:\-]?\s*", "", temiz, flags=re.IGNORECASE).strip()
    temiz = re.sub(
        r"\s+(?:adresini\s+ver|adresini\s+söyle|adresi\s+nedir|adresi\s+ne|adresi|konumunu\s+göster|konumu\s+nedir|konumu|nerededir|nerede\s+kalıyor|nerede\s+bulunur|nerede|nasıl\s+giderim|nasil\s+giderim|yol\s+tarifi|hangi\s+semtte|hangi\s+ilçede|hangi\s+ilde|neresi(?:dir)?)\s*\??$",
        "",
        temiz,
        flags=re.IGNORECASE,
    ).strip()
    temiz = re.sub(r"(?:'nin|'nın|'nun|'nün|'in|'ın|'un|'ün|'a|'e|'ya|'ye)$", "", temiz, flags=re.IGNORECASE).strip()
    return temiz.strip("?!.,;:\"' ")


def _nominatim_parcala(ilk: dict, aranan_yer: str) -> dict:
    """OpenStreetMap Nominatim JSON yanıtından il, ilçe, mahalle, cadde ve tür bilgisini çıkarır."""
    addr = ilk.get("address", {}) or {}
    ulke = addr.get("country", "")
    il = addr.get("province") or addr.get("city") or addr.get("state") or ""
    ilce = addr.get("town") or addr.get("county") or addr.get("city_district") or addr.get("district") or ""
    mahalle = addr.get("suburb") or addr.get("neighbourhood") or addr.get("quarter") or ""
    cadde = addr.get("road") or addr.get("pedestrian") or addr.get("square") or ""
    bina_no = addr.get("house_number", "")
    if cadde and bina_no:
        cadde = f"{cadde} No:{bina_no}"
    posta_kodu = addr.get("postcode", "")

    ham_tur = (ilk.get("type") or ilk.get("class") or "").lower()
    tur_tr = MEKAN_TURU_TR.get(ham_tur, "Konum / Mekan")
    yer_adi = ilk.get("name") or aranan_yer
    tam_adres = ilk.get("display_name", aranan_yer)

    konum_parcalari = [p for p in [mahalle, ilce, il, ulke] if p]
    if konum_parcalari:
        aciklama = f"{yer_adi}, {', '.join(konum_parcalari)} sınırları içerisinde bulunan bir {tur_tr.lower()} konumudur."
    else:
        aciklama = f"{yer_adi}, açık kaynak OpenStreetMap kayıtlarında yer alan bir {tur_tr.lower()} noktasıdır."

    return {
        "basarili": True,
        "yer": yer_adi,
        "tur": tur_tr,
        "il": il,
        "ilce": ilce,
        "mahalle": mahalle,
        "cadde": cadde,
        "posta_kodu": posta_kodu,
        "ulke": ulke,
        "tam_adres": tam_adres,
        "aciklama": aciklama,
        "ulasim": "",
        "lat": str(ilk.get("lat", "")),
        "lon": str(ilk.get("lon", "")),
        "kaynak": "OpenStreetMap Nominatim (Canlı Açık Kaynak)",
    }


def _photon_ile_ara(yer: str):
    """Yedek 2. canlı açık kaynak harita motoru: Komoot Photon API (photon.komoot.io)."""
    q = urllib.parse.quote(yer)
    url = f"https://photon.komoot.io/api/?q={q}&limit=3&lat=41.0082&lon=28.9784"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        veri = json.loads(resp.read().decode("utf-8"))
    ozellikler = veri.get("features", [])
    if not ozellikler:
        return None
    f0 = ozellikler[0]
    props = f0.get("properties", {})
    coords = f0.get("geometry", {}).get("coordinates", ["", ""])
    lon, lat = (str(coords[0]), str(coords[1])) if len(coords) >= 2 else ("", "")

    yer_adi = props.get("name") or yer
    il = props.get("city") or props.get("state") or ""
    ilce = props.get("district") or props.get("county") or ""
    cadde = props.get("street") or ""
    posta = props.get("postcode") or ""
    ulke = props.get("country") or ""
    ham_tur = str(props.get("osm_value") or "").lower()
    tur_tr = MEKAN_TURU_TR.get(ham_tur, "Konum / Mekan")

    parcalar = [p for p in [cadde, ilce, il, posta, ulke] if p]
    tam_adres = ", ".join(parcalar) if parcalar else yer_adi
    aciklama = f"{yer_adi}, {', '.join([p for p in [ilce, il, ulke] if p]) or 'harita'} bölgesinde yer alan bir {tur_tr.lower()} konumudur."

    return {
        "basarili": True,
        "yer": yer_adi,
        "tur": tur_tr,
        "il": il,
        "ilce": ilce,
        "mahalle": "",
        "cadde": cadde,
        "posta_kodu": posta,
        "ulke": ulke,
        "tam_adres": tam_adres,
        "aciklama": aciklama,
        "ulasim": "",
        "lat": lat,
        "lon": lon,
        "kaynak": "Photon / OpenStreetMap (Canlı Açık Kaynak)",
    }


def acik_kaynak_adres_bul(sorgu: str, sadece_yerel: bool = False) -> dict:
    """
    3 Katmanlı Doğrudan Adres & Konum Çözümleyici:
      1. Yerleşik detaylı Türkiye/İstanbul mekan belleği (tam ulaşım & açıklama dahil)
      2. Canlı OpenStreetMap Nominatim API (mahalle, cadde, ilçe, il, posta kodu, tür)
      3. Canlı Photon (Komoot) OpenStreetMap API (2. yedek canlı kaynak)
    Link verip geçmez; yerin neresi olduğunu ve açık adresini doğrudan metin olarak döndürür.
    """
    yer = yer_adi_ayikla(sorgu)
    if not yer:
        return {"basarili": False, "hata": "Lütfen adresini veya konumunu öğrenmek istediğiniz yeri yazın."}

    # 1. Yerleşik zengin Türkiye & İstanbul bellek kontrolü (en detaylı açıklama ve ulaşım bilgisi)
    yer_kucuk = yer.replace("İ", "i").replace("I", "ı").lower().strip()
    for anahtar, y in YEDEK_ADRESLER.items():
        if anahtar == yer_kucuk or anahtar in yer_kucuk or (len(yer_kucuk) >= 5 and yer_kucuk in anahtar):
            tam_adres = f"{y['mahalle']}, {y['cadde']}, {y['posta_kodu']} {y['ilce']} / {y['il']}, Türkiye"
            return {
                "basarili": True,
                "yer": y["ad"],
                "tur": y["tur"],
                "il": y["il"],
                "ilce": y["ilce"],
                "mahalle": y["mahalle"],
                "cadde": y["cadde"],
                "posta_kodu": y["posta_kodu"],
                "ulke": "Türkiye",
                "tam_adres": tam_adres,
                "aciklama": y["aciklama"],
                "ulasim": y.get("ulasim", ""),
                "lat": y["lat"],
                "lon": y["lon"],
                "kaynak": "AREX AI Konum Belleği (Doğrulanmış)",
            }

    if sadece_yerel:  # yalnızca yerleşik bellek istendi → ağa çıkma (hız)
        return {"basarili": False, "hata": "Yerleşik bellekte yok"}

    # 2. Canlı OpenStreetMap Nominatim API
    q_osm = urllib.parse.quote(yer)
    try:
        url = (
            f"https://nominatim.openstreetmap.org/search?"
            f"q={q_osm}&format=json&addressdetails=1&limit=3&accept-language=tr"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0 AREX-AI/12.1",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            sonuclar = json.loads(resp.read().decode("utf-8"))
        if isinstance(sonuclar, list) and len(sonuclar) > 0:
            return _nominatim_parcala(sonuclar[0], yer)
    except Exception:
        pass

    # 3. Canlı Photon (Komoot) OpenStreetMap Yedek API
    try:
        photon_sonuc = _photon_ile_ara(yer)
        if photon_sonuc:
            return photon_sonuc
    except Exception:
        pass

    # 4. Canlı Open-Meteo Geocoding 3. Yedek (Bulutta Nominatim/Photon yoğun olduğunda il/ilçe/yer bulur!)
    try:
        q_om = urllib.parse.quote(yer)
        req_om = urllib.request.Request(
            f"https://geocoding-api.open-meteo.com/v1/search?name={q_om}&count=1&language=tr&format=json",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/131.0.0.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req_om, timeout=5) as r_om:
            g_om = json.loads(r_om.read().decode("utf-8"))
        om_res = g_om.get("results", [])
        if om_res:
            g0 = om_res[0]
            il_ad = g0.get("admin1", "")
            ilce_ad = g0.get("admin2", "")
            ulke_ad = g0.get("country", "")
            yer_ad = g0.get("name", yer)
            parcalar = [p for p in [yer_ad, ilce_ad, il_ad, ulke_ad] if p]
            return {
                "basarili": True,
                "yer": yer_ad,
                "tur": "Yerleşim / Konum",
                "il": il_ad,
                "ilce": ilce_ad,
                "mahalle": "",
                "cadde": "",
                "posta_kodu": "",
                "ulke": ulke_ad,
                "tam_adres": ", ".join(parcalar),
                "aciklama": f"{yer_ad}, {', '.join(parcalar[1:])} bölgesinde yer alan doğrulanmış konumdur.",
                "ulasim": "",
                "lat": round(float(g0.get("latitude", 0)), 5),
                "lon": round(float(g0.get("longitude", 0)), 5),
                "kaynak": "Open-Meteo Geocoding (Canlı Yedek)",
            }
    except Exception:
        pass

    return {
        "basarili": False,
        "hata": (
            f"'{yer}' için şu an canlı OpenStreetMap sunucularına ulaşılamadı veya adres kaydı bulunamadı. "
            "Lütfen yer adını il/ilçe ile birlikte (örneğin: 'Fatih Camii İstanbul' veya 'Taksim Meydanı Beyoğlu') tekrar yaz."
        ),
    }


def adres_sonucunu_metne_formatla(sonuc: dict) -> str:
    """
    Harita linkine tıklamaya gerek bırakmadan; mekanın neresi olduğunu,
    il/ilçe/mahalle/cadde/posta kodunu, tam açık adresini ve varsa ulaşımını
    doğrudan sohbetin içinde net ve okunaklı biçimde yazar.
    """
    if not sonuc.get("basarili"):
        return f"📍 **Adres & Konum:** {sonuc.get('hata', 'Konum bulunamadı.')}"

    satirlar = [
        f"### 📍 {sonuc['yer']}",
        f"**ℹ️ Neresidir?** {sonuc.get('aciklama', '')}",
        "",
        f"**📫 Tam Açık Adres:** {sonuc['tam_adres']}",
    ]

    detaylar = []
    if sonuc.get("tur"):
        detaylar.append(f"**Mekan Türü:** {sonuc['tur']}")
    if sonuc.get("il") or sonuc.get("ilce"):
        il_ilce = " / ".join(p for p in [sonuc.get("ilce"), sonuc.get("il")] if p)
        detaylar.append(f"**İlçe / İl:** {il_ilce}")
    if sonuc.get("mahalle"):
        detaylar.append(f"**Mahalle:** {sonuc['mahalle']}")
    if sonuc.get("cadde"):
        detaylar.append(f"**Cadde / Sokak:** {sonuc['cadde']}")
    if sonuc.get("posta_kodu"):
        detaylar.append(f"**Posta Kodu:** `{sonuc['posta_kodu']}`")
    if sonuc.get("lat") and sonuc.get("lon"):
        _lat, _lon = sonuc["lat"], sonuc["lon"]
        _gmaps_url = f"https://www.google.com/maps/search/?api=1&query={_lat},{_lon}"
        _osm_url = f"https://www.openstreetmap.org/?mlat={_lat}&mlon={_lon}#map=16/{_lat}/{_lon}"
        detaylar.append(f"**GPS Koordinatı:** `{_lat}, {_lon}`")
        detaylar.append(f"**🗺️ Canlı Harita Linki:** [Google Haritalar'da Aç]({_gmaps_url}) • [OpenStreetMap'te Gör]({_osm_url})")

    if detaylar:
        satirlar.append("\n" + "\n".join(f"- {d}" for d in detaylar))

    if sonuc.get("ulasim"):
        satirlar.append(f"\n**🚇 Nasıl Gidilir?** {sonuc['ulasim']}")

    satirlar.append(f"\n*Kaynak: `{sonuc.get('kaynak', 'OpenStreetMap')}`*")
    return "\n".join(satirlar)
