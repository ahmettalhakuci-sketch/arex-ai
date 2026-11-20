# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.3 — MODÜL 9: OLLAMA YEREL YAPAY ZEKA & TDK (TÜRK DİL KURUMU)
SÖZLÜK ENTEGRASYONU VE AÇ/KAPAT KONTROL MERKEZİ (modul_9_ollama_ve_tdk.py)
Ana Kontrol: main.py tarafından otomatik import edilir.
==============================================================================
"""
import importlib.util
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, as_completed, wait
from datetime import datetime, timedelta, timezone
import json
import time
import os
import re
import sys
import urllib.parse
import urllib.request
import streamlit as st

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
if _MODUL_DIZINI not in sys.path:
    sys.path.insert(0, _MODUL_DIZINI)



# ==============================================================================
# v14 — MOBİL YANIT ÜSLUBU (tüm AI sağlayıcılarına giden sistem mesajına bir kez eklenir)
# ==============================================================================
YANIT_USLUBU = (
    "\n\nYANIT ÜSLUBU (ÖNEMLİ): Kullanıcı çoğunlukla TELEFONDAN yazıyor. "
    "1) İlk 1-2 cümlede sorunun doğrudan cevabını ver; ayrıntıyı sonra ekle. "
    "2) Uzunluğu soruya göre ayarla: basit soruya kısa ve net cevap; 'detaylı anlat' denirse uzun. "
    "3) Kısa başlıklar ve madde işaretleri kullan; tablo gerekiyorsa EN FAZLA 3 sütun olsun, geniş tablo kullanma. "
    "4) Duygusal veya kişisel mesajlarda (stres, üzüntü, sevinç) rapor/tablo YAZMA: önce duyguyu anla, "
    "sıcak ve samimi 4-6 cümleyle 2-3 somut öneri ver, gerekirse güvendiği bir yetişkinle konuşmayı öner. "
    "5) Önceki mesajlarla bağlantılı sorularda ('peki...', 'bunun...') konuşmanın akışını sürdür. "
    "6) Emin olmadığın bilgide bunu açıkça söyle; sayı, tarih ve isim uydurma."
)


def _uslup_ekle(sistem: str) -> str:
    sistem = sistem or ""
    return sistem if "YANIT ÜSLUBU (ÖNEMLİ)" in sistem else sistem + YANIT_USLUBU

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
_m5_cevir = _guvenli_modul_yukle("modul_5_dil_ve_cevirmeli_kartlar")
bilgi_karti_olustur = _m1.bilgi_karti_olustur


def _turkiye_simdi() -> datetime:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Istanbul"))
    except Exception:
        return datetime.now(timezone(timedelta(hours=3)))


def _guncel_tarih_etiketi() -> str:
    """Tüm yapay zeka istemlerine kesin İstanbul / Türkiye tarih ve saatini (UTC+3) verir."""
    _aylar = [
        "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
    ]
    _gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    simdi = _turkiye_simdi()
    return f"{simdi.day} {_aylar[simdi.month]} {simdi.year} {_gunler[simdi.weekday()]}, saat {simdi.strftime('%H:%M')} (Türkiye Saati UTC+3)"

OLLAMA_VARSAYILAN_URL = "http://127.0.0.1:11434"
_OLLAMA_YEREL_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# Çevrimdışı / Hızlı Yedek TDK Sözlük Tabanı (İnternet kesikse bile anında anlam verir)
YEDEK_TDK_SOZLUK = {
    "mühendislik": {
        "anlamlar": [
            "1. (isim) İnsanların her türlü ihtiyacını karşılamaya dayalı yol, köprü, bina, makine, elektrik, elektronik, yazılım ve havacılık gibi teknik işleri matematik ve fen bilimleri ilkeleriyle tasarlama ve uygulama mesleği.",
        ],
        "atasozu_deyim": ["Mühendislik harikası", "Tersine mühendislik"],
        "birlesikler": ["yazılım mühendisliği", "uçak mühendisliği", "mekatronik mühendisliği", "bilgisayar mühendisliği"],
    },
    "yazılım": {
        "anlamlar": [
            "1. (isim, bilişim) Bir bilgisayarda donanıma hayat veren ve bilgi işlemde kullanılan programlar, yordamlar, programlama dilleri ve belgelerin tümü.",
        ],
        "atasozu_deyim": ["Açık kaynak yazılım", "Gömülü yazılım"],
        "birlesikler": ["yazılım mühendisi", "yazılım geliştirici", "sistem yazılımı"],
    },
    "algoritma": {
        "anlamlar": [
            "1. (isim, matematik ve bilişim) Belli bir problemi çözmek veya belirli bir amaca ulaşmak için tasarlanan sıralı ve mantıksal işlem basamakları (Adını İslam âlimi El-Hârizmî'den alır).",
        ],
        "atasozu_deyim": ["Algoritma kurmak", "Arama algoritması"],
        "birlesikler": ["yapay zeka algoritması", "sıralama algoritması"],
    },
    "akıl": {
        "anlamlar": [
            "1. (isim) Düşünme, anlama ve kavrama gücü, us, خرد (hıred).",
            "2. (isim) Hafıza, bellek, zihin.",
            "3. (isim) Öğüt, salık, tavsiye.",
        ],
        "atasozu_deyim": ["Akıl akıldan üstündür", "Aklı başına gelmek", "Akıl yürütmek", "Aklına yatmak"],
        "birlesikler": ["akılcı", "akıl sağlığı", "akıl oyunu", "sağduyu"],
    },
    "bilim": {
        "anlamlar": [
            "1. (isim) Evrenin veya olayların bir bölümünü konu olarak seçen, deneye dayanan yöntemler ve gerçeklikten yararlanarak sonuç çıkarmaya çalışan düzenli bilgi, ilim.",
            "2. (isim) Belli bir konuyu bilme isteğinden yola çıkan, belli bir amaca yönelen bilgi edinme ve yöntemli araştırma süreci.",
        ],
        "atasozu_deyim": ["Bilim adamı", "Bilim dalı", "Bilim kurgu"],
        "birlesikler": ["bilim insanı", "bilgisayar bilimi", "doğa bilimleri", "fen bilimleri"],
    },
    "otonom": {
        "anlamlar": [
            "1. (sıfat, Fransızca autonome) Özerk; kendi kendini yöneten veya dışarıdan müdahale olmadan kendi kararlarını verebilen sistem.",
        ],
        "atasozu_deyim": ["Otonom sürüş", "Otonom uçuş", "Otonom sistem"],
        "birlesikler": ["otonom İHA", "otonom araç", "otonom sinir sistemi"],
    },
    "tork": {
        "anlamlar": [
            "1. (isim, fizik) Bir kuvvetin bir nesneyi bir eksen etrafında döndürme eğiliminin ölçüsü; döndürme momenti (N·m).",
        ],
        "atasozu_deyim": ["Motor torku", "Tork üretmek"],
        "birlesikler": ["tork anahtarı", "tork konvertörü"],
    },
    "irfan": {
        "anlamlar": [
            "1. (isim, Arapça) Bilme, anlama, sezme, kültür ve manevi derinlik.",
            "2. (isim, tasavvuf) Evrenin sırlarını bilme gücü.",
        ],
        "atasozu_deyim": ["İrfan sahibi", "İlim ve irfan"],
        "birlesikler": ["irfan meclisi"],
    },
}


# ==============================================================================
# 1. OLLAMA YEREL YAPAY ZEKA ENTEGRASYONU (v7.7 — PROXY-FREE, IPv4, THREAD-SAFE)
# ==============================================================================
_OLLAMA_DURUM_ONBELLEK = {"zaman": 0.0, "url": "", "aktif": False, "modeller": [], "hata": ""}
_OLLAMA_EMBED_ANAHTARLARI = ("embed", "bge-", "minilm", "snowflake-arctic-embed", "mxbai", "nomic-embed")
_OLLAMA_TURKCE_MODEL_ONCELIK = (
    "qwen2.5",
    "qwen3",
    "gemma3",
    "gemma2",
    "llama3.3",
    "llama3.1",
    "llama3.2",
    "mistral",
    "deepseek-r1",
    "phi4",
    "phi3",
)


def _ollama_url_normallestir(base_url: str = None) -> str:
    """
    Ollama adresini temizler; Windows'ta IPv6 (::1) beklemesini önlemek için
    'localhost' adresini doğrudan hızlı IPv4 '127.0.0.1'e çevirir.
    """
    ham = (base_url or OLLAMA_VARSAYILAN_URL).strip()
    if not ham:
        return OLLAMA_VARSAYILAN_URL
    if not ham.startswith(("http://", "https://")):
        ham = "http://" + ham
    ham = ham.rstrip("/")
    ham = re.sub(r"^(https?://)localhost(?=[:/]|$)", r"\g<1>127.0.0.1", ham, flags=re.IGNORECASE)
    return ham


def _ollama_http_istek(url: str, veri_dict: dict = None, timeout: float = 2.0) -> dict:
    """Sistem proxy'sini baypas ederek yerel Ollama'ya doğrudan HTTP isteği gönderir."""
    if veri_dict is not None:
        req = urllib.request.Request(
            url,
            data=json.dumps(veri_dict).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    else:
        req = urllib.request.Request(url, method="GET")
    with _OLLAMA_YEREL_OPENER.open(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _ollama_sohbet_modellerini_filtrele(modeller: list) -> list:
    """Embedding (vektör) modellerini ayıklar, yalnızca sohbet yetenekli modelleri döndürür."""
    uygun = []
    for m in modeller or []:
        ad = str(m).strip()
        if not ad:
            continue
        ad_kucuk = ad.lower()
        if any(emb in ad_kucuk for emb in _OLLAMA_EMBED_ANAHTARLARI):
            continue
        uygun.append(ad)
    return uygun


def _bulut_ortami_mi() -> bool:
    """Streamlit Community Cloud / HuggingFace / Render üzerinde çalışıyorsa True döner."""
    if os.environ.get("STREAMLIT_SHARING_MODE") or os.environ.get("STREAMLIT_CLOUD"):
        return True
    kok = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").lower()
    return kok.startswith("/mount/src/") or os.path.exists("/mount/src")


# ------------------------------------------------------------------------------
# v12.2 — BULUT API ANAHTAR ÖNCELİK HARİTASI (10 Anahtarlı + Pollinations + Ollama = 12 Motor)
# • Anahtarlar ASLA kod içine gömülmez; yalnızca .streamlit/secrets.toml veya
#   ortam değişkenlerinden (os.environ) güvenli biçimde okunur.
# • İlk sağlayıcı 429 hız limitine veya 5xx hatasına takılırsa sıradaki anahtarlı
#   bulut sağlayıcıya milisaniyeler içinde otomatik kaskad geçiş yapılır.
# ------------------------------------------------------------------------------
_BULUT_ENV_HARITASI = [
    ("groq_cloud", ("GROQ_API_KEY",)),
    ("deepseek_cloud", ("DEEPSEEK_API_KEY",)),
    ("gemini_free", ("GEMINI_API_KEY", "GOOGLE_API_KEY")),
    ("openrouter", ("OPENROUTER_API_KEY",)),
    ("cerebras_cloud", ("CEREBRAS_API_KEY",)),
    ("nvidia_nim", ("NVIDIA_API_KEY", "NVIDIA_NIM_API_KEY")),
    ("github_models", ("GITHUB_MODELS_TOKEN", "GITHUB_TOKEN")),
    ("sambanova_cloud", ("SAMBANOVA_API_KEY",)),
    ("together_cloud", ("TOGETHER_API_KEY",)),
    ("huggingface", ("HF_TOKEN", "HUGGINGFACE_API_KEY")),
    ("mistral_cloud", ("MISTRAL_API_KEY",)),
]


_UCRETLI_SAGLAYICILAR = {"deepseek_cloud", "together_cloud", "mistral_cloud"}


def _tum_bulut_anahtarlarini_topla(oncelikli_kod: str = "") -> list:
    """
    Streamlit Secrets ve ortam değişkenlerindeki (env) TÜM geçerli bulut AI anahtarlarını
    öncelik sırasına göre [(saglayici_kodu, api_key), ...] listesi olarak toplar.
    Bir sağlayıcı 429 kotasına takılırsa anında sıradakine kaskad geçiş yapılır!
    """
    bulunan = []
    gorulen = set()
    sirali = sorted(
        _BULUT_ENV_HARITASI,
        key=lambda item: (0 if item[0] == oncelikli_kod else 1),
    )
    # 1. Önce kullanıcının UI'daki Çoklu API Bağlantı Merkezi'nden girdiği anahtarları oku
    try:
        ui_havuz = st.session_state.get("coklu_api_anahtarlari") or {}
        if isinstance(ui_havuz, dict):
            ui_sirali = sorted(ui_havuz.items(), key=lambda kv: (0 if kv[0] == oncelikli_kod else 1))
            for u_kod, u_val in ui_sirali:
                u_temiz = str(u_val or "").strip()
                if u_temiz and u_kod in ACIK_KAYNAK_AI_SAGLAYICILARI and u_kod not in gorulen:
                    bulunan.append((u_kod, u_temiz))
                    gorulen.add(u_kod)
    except Exception:
        pass

    # 2. Ardından ortam değişkenleri (os.environ) ve .streamlit/secrets.toml anahtarlarını ekle
    for kod, env_adlari in sirali:
        if kod in gorulen:
            continue
        if kod in _UCRETLI_SAGLAYICILAR and kod != oncelikli_kod:
            continue  # ücretli sağlayıcı yalnızca açıkça seçilirse
        for e_ad in env_adlari:
            val = os.environ.get(e_ad, "").strip()
            if not val:
                try:
                    val = str(st.secrets.get(e_ad, "")).strip()
                except Exception:
                    val = ""
            if val and kod not in gorulen:
                bulunan.append((kod, val))
                gorulen.add(kod)
                break
    return bulunan


def _buluttan_anahtar_bul(secili: str = "") -> tuple:
    """Seçili (veya ilk mevcut) bulut AI API anahtarını Streamlit Secrets / env üzerinden okur."""
    liste = _tum_bulut_anahtarlarini_topla(oncelikli_kod=secili)
    return liste[0] if liste else ("", "")


def ollama_hizli_durum_kontrol(base_url: str = OLLAMA_VARSAYILAN_URL, zorla: bool = False) -> tuple:
    """
    Ollama sunucusunun canlı olup olmadığını proxy baypaslı IPv4 127.0.0.1 üzerinden
    1.0 sn zaman aşımı ve akıllı önbellek ile kontrol eder.
    """
    temiz_url = _ollama_url_normallestir(base_url)
    if _bulut_ortami_mi() and ("127.0.0.1" in temiz_url or "localhost" in temiz_url):
        return False, []
    simdi = time.time()
    _onbellek_suresi = 20.0 if _OLLAMA_DURUM_ONBELLEK["aktif"] else 45.0
    if (
        not zorla
        and _OLLAMA_DURUM_ONBELLEK["url"] == temiz_url
        and (simdi - _OLLAMA_DURUM_ONBELLEK["zaman"]) < _onbellek_suresi
    ):
        return _OLLAMA_DURUM_ONBELLEK["aktif"], list(_OLLAMA_DURUM_ONBELLEK["modeller"])

    try:
        veri = _ollama_http_istek(f"{temiz_url}/api/tags", timeout=1.0)
        ham_modeller = [m.get("name") for m in veri.get("models", []) if m.get("name")]
        sohbet_modelleri = _ollama_sohbet_modellerini_filtrele(ham_modeller)
        _OLLAMA_DURUM_ONBELLEK.update(
            {"zaman": simdi, "url": temiz_url, "aktif": True, "modeller": sohbet_modelleri, "hata": ""}
        )
        return True, sohbet_modelleri
    except Exception as e:
        _OLLAMA_DURUM_ONBELLEK.update(
            {"zaman": simdi, "url": temiz_url, "aktif": False, "modeller": [], "hata": str(e)}
        )
        return False, []


def ollama_en_iyi_modeli_sec(base_url: str = OLLAMA_VARSAYILAN_URL, tercih_edilen: str = None) -> str:
    """Yüklü Ollama sohbet modelleri arasından en uygun Türkçe sohbet modelini seçer."""
    aktif, yuklu_modeller = ollama_hizli_durum_kontrol(base_url)
    tercih = (tercih_edilen or "").strip()
    if not aktif or not yuklu_modeller:
        return tercih or "llama3.2"

    if tercih and not any(emb in tercih.lower() for emb in _OLLAMA_EMBED_ANAHTARLARI):
        for m in yuklu_modeller:
            if m == tercih or m.split(":")[0].lower() == tercih.split(":")[0].lower():
                return m

    for oncelik in _OLLAMA_TURKCE_MODEL_ONCELIK:
        for m in yuklu_modeller:
            if oncelik in m.lower():
                return m

    return yuklu_modeller[0]


def _ollama_yanit_temizle(ham_metin: str) -> str:
    """Ollama/AI yanıtlarındaki <think>...</think> bloklarını ve rol öneklerini temizler."""
    if not ham_metin:
        return ""
    temiz = str(ham_metin).strip()
    temiz = re.sub(r"<think>.*?</think>", "", temiz, flags=re.IGNORECASE | re.DOTALL).strip()
    if "<think>" in temiz.lower():
        temiz = re.sub(r"<think>.*$", "", temiz, flags=re.IGNORECASE | re.DOTALL).strip()
    temiz = re.sub(r"^(?:Asistan|Assistant|Ollama|Ar\s*AI)\s*:\s*", "", temiz, flags=re.IGNORECASE).strip()
    temiz = re.sub(r"\n{3,}", "\n\n", temiz).strip()

    if len(temiz) < 4:
        return ""
    cjk_sayisi = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff]", temiz))
    if cjk_sayisi > 12 and cjk_sayisi > len(temiz) * 0.25:
        return ""
    return temiz


_INGILIZCE_DURAK_KELIMELER = {
    "the", "and", "that", "this", "with", "from", "have", "which", "would", "could",
    "should", "there", "their", "about", "because", "however", "therefore", "between",
    "through", "without", "within", "using", "important", "different", "following",
    "example", "answer", "question", "please", "here", "sure", "certainly", "understand",
    "provide", "explain", "means", "allows", "helps", "works", "used", "make", "also",
    "into", "your", "they", "them", "been", "being", "where", "when", "what", "will",
}


def _ingilizce_sizinti_var_mi(metin: str) -> bool:
    """
    Kod bloklarını (```...```) hariç tutarak düz metinde İngilizce veya yarı-İngilizce
    sızıntı olup olmadığını tespit eder.
    """
    if not metin or len(metin.strip()) < 20:
        return False
    # Kod bloklarını ve satır içi kodları hariç tut
    duz = re.sub(r"```.*?```", " ", metin, flags=re.DOTALL)
    duz = re.sub(r"`[^`]+`", " ", duz)
    kelimeler = re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ]+", duz)
    if len(kelimeler) < 5:
        return False
    en_eslesen = sum(1 for k in kelimeler if k.lower() in _INGILIZCE_DURAK_KELIMELER)
    oran = en_eslesen / max(len(kelimeler), 1)
    return en_eslesen >= 3 and (oran >= 0.12 or en_eslesen >= 5)


def _turkce_dil_kilidi_uygula(metin: str, gtx_url_ozel: str = None) -> str:
    """
    Yanıtta İngilizce karışması tespit edilirse kod bloklarını (```...```) %100 koruyarak
    yalnızca düz metin kısımlarını akıcı Türkçeye çevirir.
    """
    if not _ingilizce_sizinti_var_mi(metin):
        return metin

    # Kod bloklarını yer tutucularla koru
    kod_bloklari = []
    def _kod_sakla(es):
        kod_bloklari.append(es.group(0))
        return f"[[KOD_BLOK_{len(kod_bloklari) - 1}]]"

    korunmus = re.sub(r"```.*?```", _kod_sakla, metin, flags=re.DOTALL)

    try:
        cevir_fn = getattr(_m5_cevir, "guvenli_cevir", None)
        if cevir_fn:
            # Paragraf bazlı çeviri (kod yer tutucularını bozmadan)
            yeni_parcalar = []
            for satir in korunmus.split("\n"):
                if not satir.strip() or "[[KOD_BLOK_" in satir:
                    yeni_parcalar.append(satir)
                elif _ingilizce_sizinti_var_mi(satir) or re.search(r"\b(the|is|are|and|here is|sure|because|however|you can)\b", satir.lower()):
                    cev = cevir_fn(satir, src="auto", dest="tr", gtx_url_ozel=gtx_url_ozel)
                    yeni_parcalar.append(cev if cev else satir)
                else:
                    yeni_parcalar.append(satir)
            sonuc = "\n".join(yeni_parcalar)
            for idx, kb in enumerate(kod_bloklari):
                sonuc = sonuc.replace(f"[[KOD_BLOK_{idx}]]", kb)
            return sonuc.strip()
    except Exception:
        pass
    return metin


def ollama_modelleri_getir(base_url: str = OLLAMA_VARSAYILAN_URL) -> list:
    """Bilgisayarda çalışan Ollama servisindeki yüklü sohbet modellerini listeler."""
    aktif, modeller = ollama_hizli_durum_kontrol(base_url, zorla=True)
    if aktif and modeller:
        return modeller
    return ["qwen2.5", "llama3.2", "llama3.1", "gemma2", "mistral", "deepseek-r1"]


def ollama_baglanti_kontrol(base_url: str = OLLAMA_VARSAYILAN_URL) -> tuple:
    """Ollama servisinin açık olup olmadığını ve yüklü sohbet modellerini proxy baypaslı kontrol eder."""
    temiz_url = _ollama_url_normallestir(base_url)
    try:
        veri = _ollama_http_istek(f"{temiz_url}/api/tags", timeout=2.0)
        ham_modeller = [m.get("name") for m in veri.get("models", []) if m.get("name")]
        modeller = _ollama_sohbet_modellerini_filtrele(ham_modeller) or ham_modeller
        _OLLAMA_DURUM_ONBELLEK.update(
            {"zaman": time.time(), "url": temiz_url, "aktif": True, "modeller": modeller, "hata": ""}
        )
        return True, modeller
    except Exception as e:
        _OLLAMA_DURUM_ONBELLEK.update(
            {"zaman": time.time(), "url": temiz_url, "aktif": False, "modeller": [], "hata": str(e)}
        )
        return False, str(e)


def ollama_soru_sor(
    soru: str,
    model_adi: str = None,
    base_url: str = None,
    sicaklik: float = None,
    ek_baglam: str = "",
    gecmis_mesajlar: list = None,
    sistem_prompt_ozel: str = None,
) -> tuple:
    """
    v7.7 — Thread-safe, proxy-free, IPv4 öncelikli Ollama motoru.
    İş parçacığı (ThreadPoolExecutor) içinde çağrıldığında st.session_state'e dokunmaz.
    """
    try:
        ss_url = st.session_state.get("ollama_url", OLLAMA_VARSAYILAN_URL)
        ss_model = st.session_state.get("ollama_secili_model", "llama3.2")
        ss_mesajlar = st.session_state.get("messages") or []
    except Exception:
        ss_url, ss_model, ss_mesajlar = OLLAMA_VARSAYILAN_URL, "llama3.2", []

    hedef_url = _ollama_url_normallestir(base_url or ss_url)
    tercih_model = model_adi or ss_model
    secili_model = ollama_en_iyi_modeli_sec(hedef_url, tercih_model)

    baglam_var = bool(ek_baglam and ek_baglam.strip())
    aktif_sicaklik = float(sicaklik) if sicaklik is not None else (0.35 if baglam_var else 0.45)

    if sistem_prompt_ozel and sistem_prompt_ozel.strip():
        sistem_mesaji = sistem_prompt_ozel.strip()
    else:
        sistem_mesaji = (
            "Sen Ahmet tarafından geliştirilen 'AREX AI Studio' adlı Türkçe yapay zeka asistanısın. "
            "Ahmet İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi; "
            f"TEKNOFEST İHA ve TÜBİTAK akıllı bebek arabası projeleri geliştiriyor. BUGÜNÜN GERÇEK TARİHİ: {_guncel_tarih_etiketi()}. Güncel açık kaynak verilerini her zaman esas al.\n"
            "KESİN KURALLAR:\n"
            "1. YALNIZCA akıcı, doğal, düzgün ve anlaşılır Türkçe yaz; rastgele İngilizce kelime, garip sembol veya iç düşünce (<think>) metni yazma.\n"
            "2. Bilmediğin veya emin olmadığın bir sayıyı, tarihi ya da kulüp/fiyat bilgisini ASLA uydurma; dürüstçe belirt.\n"
            "3. Kısa, düzenli paragraflar veya temiz madde işaretleriyle doğrudan soruya odaklan."
        )

    if baglam_var:
        sistem_mesaji += (
            "\n\nAŞAĞIDA AÇIK KAYNAKLARDAN (Wikipedia, TDK, Hava Durumu, Yemek Tarifleri, "
            "81 İl & 195+ Ülke, Harita, Piyasa/Kur) TOPLANMIŞ DOĞRULANMIŞ VERİLER VAR. "
            "Bu gerçek verileri asla çarpıtmadan ve uydurma eklemeden, Ahmet'e akıcı ve samimi tek bir Türkçe yanıt olarak sentezle:\n"
            f"{ek_baglam.strip()[:3200]}"
        )

    mesaj_listesi = [{"role": "system", "content": _uslup_ekle(sistem_mesaji)}]
    kaynak_gecmis = gecmis_mesajlar if gecmis_mesajlar is not None else ss_mesajlar
    for m in kaynak_gecmis[-6:]:
        rol = m.get("role", "")
        icerik = str(m.get("content", "")).strip()
        if rol in ("user", "assistant") and icerik:
            if rol == "user" and icerik == soru.strip():
                continue
            mesaj_listesi.append({"role": rol, "content": icerik[:600]})
    _tr_kilit_notu = "\n\n[ÖNEMLİ: Yanıtını YALNIZCA akıcı ve doğal Türkçe yaz; kesinlikle İngilizce cümle karıştırma.]"
    mesaj_listesi.append({"role": "user", "content": soru.strip() + _tr_kilit_notu})

    ollama_secenekleri = {
        "temperature": aktif_sicaklik,
        "top_p": 0.85,
        "top_k": 40,
        "repeat_penalty": 1.18,
        "num_ctx": 8192,
        "num_predict": 2048,
    }

    son_hata = ""
    # Hızlı ön-kontrol: Ollama kapalıysa 1 sn içinde çıkıp Groq/Pollinations/Wikipedia'ya geç!
    o_acik, _ = ollama_hizli_durum_kontrol(hedef_url)
    if not o_acik:
        return (
            None,
            f"Ollama kapalı ({hedef_url}) — otomatik olarak diğer açık kaynaklara geçiliyor.",
        )

    # 1. /api/chat uç noktası (proxy-free + 18 sn üst sınır: asla uygulamayı kilitlemez!)
    chat_404 = False
    try:
        sonuc = _ollama_http_istek(
            f"{hedef_url}/api/chat",
            veri_dict={
                "model": secili_model,
                "messages": mesaj_listesi,
                "stream": False,
                "keep_alive": "10m",
                "options": ollama_secenekleri,
            },
            timeout=18,
        )
        yanit_metni = _ollama_yanit_temizle(sonuc.get("message", {}).get("content", ""))
        if yanit_metni:
            try:
                _gtx_t = st.session_state.get("test_gtx_url")
            except Exception:
                _gtx_t = None
            yanit_metni = _turkce_dil_kilidi_uygula(yanit_metni, gtx_url_ozel=_gtx_t)
            return f"🦙 **Ollama ({secili_model}):**\n\n{yanit_metni}", f"Ollama ({secili_model})"
    except urllib.error.HTTPError as he:
        son_hata = str(he)
        chat_404 = he.code in (404, 405)
    except Exception as e:
        son_hata = str(e)

    # 2. /api/generate yedek uç noktası (sadece eski Ollama 404/405 verdiyse dene — 90 sn donmayı önler!)
    if chat_404:
        try:
            sonuc = _ollama_http_istek(
                f"{hedef_url}/api/generate",
                veri_dict={
                    "model": secili_model,
                    "system": sistem_mesaji,
                    "prompt": soru.strip() + _tr_kilit_notu,
                    "stream": False,
                    "keep_alive": "10m",
                    "options": ollama_secenekleri,
                },
                timeout=12,
            )
            yanit_metni = _ollama_yanit_temizle(sonuc.get("response", ""))
            if yanit_metni:
                try:
                    _gtx_t = st.session_state.get("test_gtx_url")
                except Exception:
                    _gtx_t = None
                yanit_metni = _turkce_dil_kilidi_uygula(yanit_metni, gtx_url_ozel=_gtx_t)
                return f"🦙 **Ollama ({secili_model}):**\n\n{yanit_metni}", f"Ollama ({secili_model})"
        except Exception as e:
            son_hata = str(e)

    return (
        None,
        f"Ollama bağlantısı kurulamadı (`{hedef_url}` — Model: `{secili_model}`). "
        f"Ollama uygulamasının açık olduğundan ve en az bir sohbet modelinin (`ollama pull qwen2.5:3b`) yüklü olduğundan emin ol. ({son_hata})",
    )


# ==============================================================================
# 2. TDK (TÜRK DİL KURUMU) GÜNCEL TÜRKÇE SÖZLÜK ENTEGRASYONU (sozluk.gov.tr)
# ==============================================================================
def tdk_kelime_cikar(kullanici_girdisi: str) -> str:
    """
    Kullanıcının cümlesinden TDK'da aranacak kelimeyi ayıklar.
    Örn: 'tdk: mühendislik', 'mütefekkir ne demek?', 'irfan kelimesinin anlamı nedir' -> 'mütefekkir', 'irfan'
    """
    temiz = kullanici_girdisi.strip()
    # Başındaki 'tdk:', 'tdk', 'sözlük:' öneklerini temizle
    temiz = re.sub(r"^(?:tdk|sozluk|sözlük)\s*[:\-]?\s*", "", temiz, flags=re.IGNORECASE).strip()
    # Sonundaki 'ne demek', 'anlamı nedir', 'tdk anlamı' vb. ekleri temizle
    temiz = re.sub(
        r"\s+(?:kelimesinin\s+anlamı\s+nedir|kelimesinin\s+anlamı|kelimesi\s+ne\s+demek|tdk\s+anlamı\s+nedir|tdk\s+anlamı|anlamı\s+nedir|anlamı\s+ne|ne\s+demektir|ne\s+demek|nedir)\s*\??$",
        "",
        temiz,
        flags=re.IGNORECASE,
    ).strip()
    temiz = temiz.strip("?!.,;:\"' ")
    return temiz.replace("İ", "i").replace("I", "ı").lower()


def tdk_sozluk_sorgula(kelime: str) -> dict:
    """
    Resmi Türk Dil Kurumu (https://sozluk.gov.tr/gts?ara=...) API'sinden kelimenin
    anlamlarını, örnek cümlelerini, atasözü/deyimlerini ve birleşik kelimelerini çeker.
    """
    aranan = tdk_kelime_cikar(kelime)
    if not aranan:
        return {"basarili": False, "kelime": kelime, "hata": "Lütfen aranacak bir kelime girin."}

    try:
        kodlu_kelime = urllib.parse.quote(aranan)
        url = f"https://sozluk.gov.tr/gts?ara={kodlu_kelime}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            veri = json.loads(resp.read().decode("utf-8"))

        if isinstance(veri, list) and len(veri) > 0 and isinstance(veri[0], dict):
            madde = veri[0]
            anlamlar = []
            ornekler = []
            for idx, a_obj in enumerate(madde.get("anlamlarListe", []), 1):
                anlam_metin = a_obj.get("anlam", "").strip()
                ozellikler = [
                    oz.get("tam_adi", "")
                    for oz in a_obj.get("ozelliklerListe", [])
                    if oz.get("tam_adi")
                ]
                oz_str = f" *({', '.join(ozellikler)})*" if ozellikler else ""
                if anlam_metin:
                    anlamlar.append(f"{idx}. {oz_str} {anlam_metin}".strip())
                for orn in a_obj.get("orneklerListe", [])[:2]:
                    orn_metin = orn.get("ornek", "").strip()
                    yazar_liste = orn.get("yazar", [])
                    yazar_adi = yazar_liste[0].get("tam_adi", "") if isinstance(yazar_liste, list) and yazar_liste else ""
                    if orn_metin:
                        ornekler.append(f'"{orn_metin}"' + (f" — *{yazar_adi}*" if yazar_adi else ""))

            atasozleri = [a.get("madde", "") for a in madde.get("atasozu", []) if a.get("madde")][:8]
            birlesikler = (
                [b.strip() for b in madde.get("birlesikler", "").split(",") if b.strip()][:10]
                if madde.get("birlesikler")
                else []
            )
            lisan = madde.get("lisan", "").strip()

            if anlamlar:
                return {
                    "basarili": True,
                    "kelime": madde.get("madde", aranan),
                    "koken": lisan or "Türkçe",
                    "anlamlar": anlamlar,
                    "ornekler": ornekler,
                    "atasozu_deyim": atasozleri,
                    "birlesikler": birlesikler,
                    "kaynak": "TDK Güncel Türkçe Sözlük (Canlı)",
                }
    except Exception:
        pass

    # Çevrimdışı Yedek Sözlük Kontrolü
    if aranan in YEDEK_TDK_SOZLUK:
        y_veri = YEDEK_TDK_SOZLUK[aranan]
        return {
            "basarili": True,
            "kelime": aranan,
            "koken": "Türkçe / Köken Bilgisi",
            "anlamlar": y_veri["anlamlar"],
            "ornekler": [],
            "atasozu_deyim": y_veri["atasozu_deyim"],
            "birlesikler": y_veri["birlesikler"],
            "kaynak": "TDK Yerleşik Yedek Sözlük",
        }

    return {
        "basarili": False,
        "kelime": aranan,
        "hata": f"TDK Güncel Türkçe Sözlük'te '{aranan}' maddesi bulunamadı veya yazımı farklı olabilir.",
    }


def tdk_sonucunu_metne_formatla(sonuc: dict) -> str:
    """TDK sözlük sonucunu şık bir Markdown metnine dönüştürür."""
    if not sonuc.get("basarili"):
        return f"📕 **TDK Sözlük:** {sonuc.get('hata', 'Kelime bulunamadı.')}"

    satirlar = [
        f"### 📕 TDK Güncel Türkçe Sözlük: **{sonuc['kelime'].upper()}**",
        f"**Köken / Dil Bilgisi:** `{sonuc.get('koken', 'Türkçe')}` | **Kaynak:** `{sonuc.get('kaynak', 'TDK')}`\n",
        "**📌 Anlamları:**",
    ]
    for a in sonuc.get("anlamlar", []):
        satirlar.append(f"- {a}")

    if sonuc.get("ornekler"):
        satirlar.append("\n**📝 Edebiyatımızdan Örnek Cümleler:**")
        for o in sonuc["ornekler"]:
            satirlar.append(f"> {o}")

    if sonuc.get("atasozu_deyim"):
        satirlar.append("\n**🗣️ Atasözleri ve Deyimler:** " + " • ".join(f"`{x}`" for x in sonuc["atasozu_deyim"]))

    if sonuc.get("birlesikler"):
        satirlar.append("\n**🔗 Birleşik Kelimeler:** " + ", ".join(sonuc["birlesikler"]))

    return "\n".join(satirlar)


# ==============================================================================
# 3. OLLAMA & TDK BÖLÜMÜ ARAYÜZ STÜDYOSU (main.py Tarafından Çağrılır)
# ==============================================================================
def ollama_ve_tdk_studyosu_goster(sesli_soyle_fn):
    st.subheader("🦙 Ollama Yerel Yapay Zeka & 📕 TDK Güncel Türkçe Sözlük Merkezi")

    # Üst Aç / Kapat Kontrol Çubuğu
    ust1, ust2, ust3 = st.columns([1.2, 1.2, 1.2])
    with ust1:
        st.session_state.ollama_aktif = st.toggle(
            "🦙 Ollama Modu (Aç / Kapat)",
            value=st.session_state.get("ollama_aktif", False),
            key="studio_ollama_toggle",
        )
    with ust2:
        st.session_state.tdk_aktif = st.toggle(
            "📕 TDK Sözlük Modu (Aç / Kapat)",
            value=st.session_state.get("tdk_aktif", True),
            key="studio_tdk_toggle",
        )
    with ust3:
        bagli_mi, modeller_veya_hata = ollama_baglanti_kontrol(st.session_state.get("ollama_url", OLLAMA_VARSAYILAN_URL))
        if bagli_mi:
            st.markdown('<span class="live-badge">🦙 OLLAMA SERVİSİ AÇIK</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="silent-badge">🦙 OLLAMA BEKLEMEDE (localhost:11434)</span>', unsafe_allow_html=True)

    tab_ollama, tab_tdk = st.tabs([
        "🦙 Ollama Yapay Zeka Bölümü",
        "📕 TDK (Türk Dil Kurumu) Sözlük Bölümü",
    ])

    # --- BÖLÜM 1: OLLAMA YAPAY ZEKA BÖLÜMÜ ---
    with tab_ollama:
        col_o1, col_o2 = st.columns([1.05, 1.65], gap="large")
        with col_o1:
            st.markdown("#### ⚙️ Ollama Bağlantı & Model Merkezi")
            girilen_url = st.text_input(
                "Ollama Sunucu Adresi (IPv4 Önerilir):",
                value=st.session_state.get("ollama_url", OLLAMA_VARSAYILAN_URL),
                help="Windows'ta en hızlı bağlantı için http://127.0.0.1:11434 kullanılır (localhost otomatik çevrilir).",
            )
            st.session_state.ollama_url = _ollama_url_normallestir(girilen_url)

            mevcut_modeller = ollama_modelleri_getir(st.session_state.ollama_url)
            varsayilan_m = st.session_state.get("ollama_secili_model", mevcut_modeller[0])
            if varsayilan_m not in mevcut_modeller:
                mevcut_modeller.insert(0, varsayilan_m)
            st.session_state.ollama_secili_model = st.selectbox(
                "Aktif Sohbet Modeli:",
                options=mevcut_modeller,
                index=mevcut_modeller.index(varsayilan_m),
            )
            ozel_model = st.text_input("Veya Model Adını Elle Yaz:", placeholder="Örn: qwen2.5:3b, gemma2, llama3.2", value="")
            if ozel_model.strip():
                st.session_state.ollama_secili_model = ozel_model.strip()

            sicaklik_val = st.slider("Tutarlılık / Yaratıcılık (Temperature):", 0.1, 0.9, 0.4, 0.05)

            if st.button("🔄 Bağlantıyı Yenile ve Test Et", use_container_width=True):
                ok_mu, m_list = ollama_baglanti_kontrol(st.session_state.ollama_url)
                if ok_mu:
                    if m_list:
                        st.success(f"✅ Bağlantı aktif (`{st.session_state.ollama_url}`) — Modeller: {', '.join(m_list)}")
                    else:
                        st.warning("✅ Ollama servisi açık ancak hiç sohbet modeli yüklü değil. Terminalde `ollama pull qwen2.5:3b` çalıştır.")
                else:
                    st.error(
                        f"⚠️ Ollama'ya ulaşılamadı (`{st.session_state.ollama_url}`). "
                        f"Ollama uygulamasını aç veya terminalde `ollama serve` komutunu çalıştır. (Detay: {m_list})"
                    )

        with col_o2:
            st.markdown(f"#### 💬 Doğrudan Ollama'ya Sor (`{st.session_state.ollama_secili_model}`)")
            ollama_soru_input = st.text_area(
                "Ollama'ya sormak istediğin soru veya yazdırmak istediğin kod:",
                height=130,
                placeholder="Örn: Akıllı bebek arabasında yokuş aşağı inerken otomatik frenleme algoritmasını nasıl kurmalıyım?",
            )
            ob1, ob2 = st.columns(2)
            btn_ollama_sor = ob1.button("🦙 Ollama'dan Cevap Al", use_container_width=True)
            btn_ollama_sesli = ob2.button("🔊 Ollama'dan Cevap Al ve Sesli Oku", use_container_width=True)

            if btn_ollama_sor or btn_ollama_sesli:
                if ollama_soru_input.strip():
                    with st.spinner(f"🦙 Ollama ({st.session_state.ollama_secili_model}) düşünüyor..."):
                        o_yanit, o_bilgi = ollama_soru_sor(
                            ollama_soru_input.strip(),
                            model_adi=st.session_state.ollama_secili_model,
                            base_url=st.session_state.ollama_url,
                            sicaklik=sicaklik_val,
                        )
                    if o_yanit:
                        st.session_state["son_ollama_yaniti"] = o_yanit
                        if btn_ollama_sesli:
                            sesli_soyle_fn(o_yanit, dil="tr")
                    else:
                        st.warning(o_bilgi)
                else:
                    st.warning("Lütfen Ollama'ya sormak için bir soru yaz Ahmet.")

            if st.session_state.get("son_ollama_yaniti"):
                st.markdown(
                    bilgi_karti_olustur(
                        f"🦙 Ollama Yanıtı ({st.session_state.ollama_secili_model})",
                        "Yerel Yapay Zeka Motoru",
                        st.session_state["son_ollama_yaniti"].replace("\n", "<br>"),
                    ),
                    unsafe_allow_html=True,
                )

    # --- BÖLÜM 2: TDK (TÜRK DİL KURUMU) SÖZLÜK BÖLÜMÜ ---
    with tab_tdk:
        st.markdown("#### 📕 Türk Dil Kurumu (TDK) Güncel Türkçe Sözlük, Atasözleri & Deyimler")
        # Hızlı Türkçe Karakter Ekleme ve Örnek Kelimeler
        hk1, hk2, hk3, hk4, hk5 = st.columns(5)
        hizli_kelime = None
        if hk1.button("📕 bilim", use_container_width=True):
            hizli_kelime = "bilim"
        if hk2.button("📕 akıl", use_container_width=True):
            hizli_kelime = "akıl"
        if hk3.button("📕 otonom", use_container_width=True):
            hizli_kelime = "otonom"
        if hk4.button("📕 irfan", use_container_width=True):
            hizli_kelime = "irfan"
        if hk5.button("📕 mühendislik", use_container_width=True):
            hizli_kelime = "mühendislik"

        tdk_aranan = st.text_input(
            "TDK Sözlük'te Aranacak Kelimeyi Yaz:",
            value=hizli_kelime or st.session_state.get("son_tdk_kelime", "bilim"),
            placeholder="Örn: merhamet, adalet, yazılım, özerk, tefekkür...",
        )
        tb1, tb2 = st.columns(2)
        btn_tdk_ara = tb1.button("🔍 TDK Sözlük'te Ara", use_container_width=True)
        btn_tdk_ses = tb2.button("🔊 Anlamını Bul ve Sesli Oku", use_container_width=True)

        if btn_tdk_ara or btn_tdk_ses or hizli_kelime:
            secilen_k = hizli_kelime or tdk_aranan
            st.session_state["son_tdk_kelime"] = secilen_k
            sonuc = tdk_sozluk_sorgula(secilen_k)
            st.session_state["son_tdk_sonuc"] = sonuc
            if btn_tdk_ses and sonuc.get("basarili"):
                ses_metin = f"{sonuc['kelime']} kelimesinin TDK anlamı: " + " ".join(sonuc["anlamlar"])
                sesli_soyle_fn(ses_metin, dil="tr")

        aktif_tdk = st.session_state.get("son_tdk_sonuc") or tdk_sozluk_sorgula("bilim")
        if aktif_tdk.get("basarili"):
            anlam_html = "<br>".join(aktif_tdk["anlamlar"])
            ornek_html = ("<br><br><strong>📝 Örnek Cümleler:</strong><br>" + "<br>".join(aktif_tdk["ornekler"])) if aktif_tdk.get("ornekler") else ""
            atasozu_html = ("<br><br><strong>🗣️ Atasözleri & Deyimler:</strong> " + " • ".join(aktif_tdk["atasozu_deyim"])) if aktif_tdk.get("atasozu_deyim") else ""
            birlesik_html = ("<br><br><strong>🔗 Birleşik Kelimeler:</strong> " + ", ".join(aktif_tdk["birlesikler"])) if aktif_tdk.get("birlesikler") else ""
            st.markdown(
                bilgi_karti_olustur(
                    f"📕 {aktif_tdk['kelime'].upper()} — TDK Sözlük Maddesi",
                    f"Köken: {aktif_tdk.get('koken', 'Türkçe')} | {aktif_tdk.get('kaynak', 'TDK')}",
                    f"<strong>📌 Anlamları:</strong><br>{anlam_html}{ornek_html}{atasozu_html}{birlesik_html}",
                ),
                unsafe_allow_html=True,
            )
        else:
            st.warning(aktif_tdk.get("hata", "Kelime bulunamadı."))


# ==============================================================================
# 4. AÇIK KAYNAKLI YAPAY ZEKA SİTELERİ KÖPRÜSÜ (ANAHTARSIZ POLLINATIONS, GROQ,
#    HUGGING FACE, OPENROUTER VE YEREL OLLAMA TEK MERKEZDE)
# ==============================================================================
ACIK_KAYNAK_AI_SAGLAYICILARI = {
    "pollinations_free": {
        "ad": "🌐 Pollinations Açık Kaynak AI (Ücretsiz & API Anahtarsız!)",
        "url": "https://text.pollinations.ai/openai",
        "model": "openai",
        "anahtar_gerekli": False,
        "aciklama": "Hiçbir üyelik veya API anahtarı gerektirmeden internete bağlıyken doğrudan açık kaynak dil modelleriyle Türkçe sohbet üretir.",
    },
    "groq_cloud": {
        "ad": "⚡ Groq Cloud — GPT-OSS 120B (Ücretsiz, Açık Ağırlıklı, Çok Hızlı)",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "openai/gpt-oss-120b",
        "anahtar_gerekli": True,
        "site": "https://console.groq.com/keys",
        "aciklama": "Açık kaynaklı Meta Llama 3.3 70B ve Qwen 2.5 modellerini saniyede 300 kelime hızla ücretsiz çalıştıran en popüler geliştirici sitesidir.",
    },
    "huggingface": {
        "ad": "🤗 Hugging Face — Qwen 2.5 72B / Llama 3 (Açık Kaynak Merkezi)",
        "url": "https://router.huggingface.co/v1/chat/completions",
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "anahtar_gerekli": True,
        "site": "https://huggingface.co/settings/tokens",
        "aciklama": "Dünyanın en büyük açık kaynak yapay zeka sitesidir. Ücretsiz 'hf_...' token alarak yüz binlerce modeli kullanabilirsin.",
    },
    "deepseek_cloud": {
        "ad": "🐋 DeepSeek — V4.1-Flash & V4-Pro (1M Bağlam & Derin Muhakeme)",
        "url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-flash",
        "anahtar_gerekli": True,
        "site": "https://platform.deepseek.com/api_keys",
        "aciklama": "DeepSeek resmi API'si üzerinden 1 milyon token bağlamlı deepseek-flash (V4.1-Flash) ve deepseek-v4-pro modellerini çalıştırır.",
    },
    "gemini_free": {
        "ad": "💎 Google AI Studio — Gemini 4 Hydrogen (Ücretsiz 1M Bağlam)",
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "model": "gemini-4-hydrogen",
        "anahtar_gerekli": True,
        "site": "https://aistudio.google.com/apikey",
        "aciklama": "Google AI Studio ücretsiz katmanı üzerinden 1 milyon token bağlam penceresiyle hızlı, derin ve akıcı Türkçe yanıt üretir.",
    },
    "openrouter": {
        "ad": "🔀 OpenRouter — Oto-Ücretsiz & 550B Nemotron (openrouter/free)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "openrouter/free",
        "anahtar_gerekli": True,
        "site": "https://openrouter.ai/keys",
        "aciklama": "openrouter/free otomatik yönlendiricisiyle (Nemotron 3 Ultra 550B, Gemma 4 31B, Qwen 3.8 dahil) her zaman aktif ücretsiz modellere bağlanır.",
    },
    "mistral_cloud": {
        "ad": "🌪️ Mistral AI — Mistral Small (Ücretsiz Geliştirici Katmanı)",
        "url": "https://api.mistral.ai/v1/chat/completions",
        "model": "mistral-small-latest",
        "anahtar_gerekli": True,
        "site": "https://console.mistral.ai/api-keys/",
        "aciklama": "Avrupa'nın lider açık ağırlıklı yapay zeka geliştiricisi Mistral'in hızlı ve akıcı Türkçe destekli ücretsiz katmanı.",
    },
    "cerebras_cloud": {
        "ad": "⚡ Cerebras Cloud — Llama 3.3 70B (Ultra Hızlı Ücretsiz API)",
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "model": "llama-3.3-70b",
        "anahtar_gerekli": True,
        "site": "https://cloud.cerebras.ai/",
        "aciklama": "Saniyede 1000+ token hızıyla çalışan ultra hızlı ücretsiz Llama 3.3 70B açık kaynak API.",
    },
    "nvidia_nim": {
        "ad": "🟢 NVIDIA NIM — Llama 3.1 70B / Nemotron (Ücretsiz Geliştirici API)",
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "meta/llama-3.1-70b-instruct",
        "anahtar_gerekli": True,
        "site": "https://build.nvidia.com/settings/api-keys",
        "aciklama": "NVIDIA Build (NIM) üzerinden ücretsiz nvapi-... anahtarıyla Llama 3.1 70B, Nemotron ve açık kaynak modelleri çalıştırır.",
    },
    "github_models": {
        "ad": "🐙 GitHub Models — GPT-4o / Llama 3.3 (Ücretsiz GitHub PAT)",
        "url": "https://models.github.ai/inference/chat/completions",
        "model": "openai/gpt-4o",
        "anahtar_gerekli": True,
        "site": "https://github.com/marketplace/models",
        "aciklama": "GitHub hesabından models:read yetkili ücretsiz token (ghp_... / github_pat_...) ile doğrudan yüksek kaliteli sohbet ve kod üretir.",
    },
    "sambanova_cloud": {
        "ad": "🚀 SambaNova Cloud — DeepSeek & Llama (Ücretsiz Hızlı Katman)",
        "url": "https://api.sambanova.ai/v1/chat/completions",
        "model": "DeepSeek-V3.1",
        "anahtar_gerekli": True,
        "site": "https://cloud.sambanova.ai/",
        "aciklama": "Ücretsiz geliştirici hesabıyla DeepSeek-V3.1 ve açık kaynak modelleri bulutta çok yüksek hızda çalıştırır.",
    },
    "together_cloud": {
        "ad": "🤝 Together AI — Açık Kaynak Bulut (Ücretsiz Kredi)",
        "url": "https://api.together.xyz/v1/chat/completions",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "anahtar_gerekli": True,
        "site": "https://api.together.xyz/",
        "aciklama": "Llama 3.3, Qwen ve DeepSeek açık kaynak modellerini tek API üzerinden yüksek kelime kapasitesiyle sunar.",
    },
    "ollama_local": {
        "ad": "🦙 Ollama Yerel AI (Bilgisayarında İnternetsiz Çalışır)",
        "url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "anahtar_gerekli": False,
        "site": "https://ollama.com",
        "aciklama": "Bilgisayarına indirdiğin açık kaynak modelleri (llama3.2, qwen2.5, gemma2, deepseek-r1) tamamen çevrimdışı çalıştırır.",
    },
}


def _aday_yanit_puanla(metin: str, ek_baglam: str = "") -> float:
    """
    Hakem sentezi zaman aşımına uğrarsa aday yanıtlar arasından en mantıklı,
    akıcı ve açık kaynak verisiyle en uyumlu Türkçe cevabı puanlayarak seçer.
    """
    if not metin or len(metin.strip()) < 10:
        return -10.0
    m = metin.strip()
    puan = min(len(m) / 40.0, 12.0)

    # Türkçe karakter ve doğal dil yoğunluğu bonusu
    tr_karakterler = sum(1 for c in m if c in "çğıöşüÇĞİÖŞÜ")
    if tr_karakterler >= 3:
        puan += 4.0

    # Hata/sızıntı cezaları
    if "<think>" in m.lower() or "sorry, i cannot" in m.lower() or "as an ai language model" in m.lower():
        puan -= 15.0

    # Doğrulanmış açık kaynak verisiyle (ek_baglam) kelime örtüşmesi bonusu
    if ek_baglam and ek_baglam.strip():
        baglam_kelimeler = {
            k.lower() for k in re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ0-9]{4,}", ek_baglam)
        }
        if baglam_kelimeler:
            metin_kelimeler = {
                k.lower() for k in re.findall(r"[a-zA-ZçğıöşüÇĞİÖŞÜ0-9]{4,}", m)
            }
            ortak = len(baglam_kelimeler & metin_kelimeler)
            puan += min(ortak * 0.8, 14.0)

    return puan


# ------------------------------------------------------------------------------
# v12.2 — DESTEKLENEN ANAHTARLI BULUT SAĞLAYICI KODLARI & GÜVENLİ ANAHTAR TANIYICI
# ------------------------------------------------------------------------------
_BULUT_SAGLAYICI_KODLARI = (
    "groq_cloud", "deepseek_cloud", "gemini_free", "openrouter", "cerebras_cloud", "nvidia_nim",
    "github_models", "sambanova_cloud", "together_cloud", "huggingface", "mistral_cloud",
)


def bulut_anahtar_formati_dogrula(anahtar: str, secili: str = "") -> dict:
    """
    Girilen API anahtarını temizler, bilinen sağlayıcı öneklerinden (gsk_, AIza, sk-or-,
    csk-, nvapi-, ghp_, hf_) hangi servise ait olduğunu otomatik tespit eder ve
    eksik/önek-dışı anahtarlarda kullanıcıya anlaşılır Türkçe yönlendirme üretir.
    """
    temiz = (anahtar or "").strip().strip('"').strip("'")
    if not temiz or len(temiz) < 6:
        return {
            "gecerli": False,
            "saglayici": "",
            "temiz_anahtar": temiz,
            "mesaj": "API anahtarı çok kısa veya boş görünüyor; lütfen sağlayıcı panelinden tam anahtarı kopyala.",
        }
    on_ekler = (
        ("gsk_", "groq_cloud", "Groq Cloud"),
        ("AIza", "gemini_free", "Google AI Studio (Gemini)"),
        ("sk-or-", "openrouter", "OpenRouter"),
        ("csk-", "cerebras_cloud", "Cerebras Cloud"),
        ("nvapi-", "nvidia_nim", "NVIDIA NIM"),
        ("ghp_", "github_models", "GitHub Models"),
        ("github_pat_", "github_models", "GitHub Models"),
        ("hf_", "huggingface", "Hugging Face"),
    )
    for onek, kod, ad in on_ekler:
        if temiz.startswith(onek):
            return {
                "gecerli": True,
                "saglayici": kod,
                "temiz_anahtar": temiz,
                "mesaj": f"{ad} anahtarı otomatik olarak tanındı ve bağlanmaya hazır.",
            }
    if secili in _BULUT_SAGLAYICI_KODLARI:
        return {
            "gecerli": True,
            "saglayici": secili,
            "temiz_anahtar": temiz,
            "mesaj": f"Özel biçimli anahtar seçili sağlayıcı ({secili}) ile eşleştirildi.",
        }
    return {
        "gecerli": False,
        "saglayici": "",
        "temiz_anahtar": temiz,
        "mesaj": (
            "Bu anahtar standart Groq (gsk_), Google AI Studio (AIza) veya OpenRouter (sk-or-) öneki taşımıyor. "
            "Hangi servise aitse yan menüden o sağlayıcıyı seçip anahtarı Secrets veya Hızlı Anahtar kutusuna gir."
        ),
    }


def _saglayici_icin_anahtar_bul(hedef_kod: str, verilen_anahtar: str = "") -> str:
    """
    v12.4 ÇAPRAZ ANAHTAR KORUMASI:
    İstenen sağlayıcı (örn. 'deepseek_cloud' veya 'gemini_free') için YALNIZCA
    o sağlayıcıya ait doğru API anahtarını döndürür. Groq anahtarının (gsk_)
    yanlışlıkla DeepSeek veya Gemini sunucusuna gidip HTTP 401 üretmesini engeller!
    """
    def _onek_cakismasi_var_mi(kod: str, key: str) -> bool:
        k_t = (key or "").strip()
        if not k_t:
            return True
        dog = bulut_anahtar_formati_dogrula(k_t)
        algilanan = dog.get("saglayici", "")
        # Anahtar kesin olarak BAŞKA bir sağlayıcıya ait önek taşıyorsa çakışma vardır
        return bool(algilanan and kod and algilanan != kod)

    # 1. Kullanıcının Çoklu API Havuzu'nda hedef sağlayıcının kendi anahtarı varsa öncelikle onu al
    try:
        ui_havuz = st.session_state.get("coklu_api_anahtarlari") or {}
        if isinstance(ui_havuz, dict) and hedef_kod in ui_havuz:
            u_key = str(ui_havuz[hedef_kod] or "").strip()
            if u_key and not _onek_cakismasi_var_mi(hedef_kod, u_key):
                return u_key
    except Exception:
        pass

    # 2. Ortam değişkeni / Streamlit Secrets havuzunda tam eşleşen sağlayıcı anahtarını ara
    for t_kod, t_key in _tum_bulut_anahtarlarini_topla(oncelikli_kod=hedef_kod):
        if t_kod == hedef_kod and t_key and not _onek_cakismasi_var_mi(hedef_kod, t_key):
            return t_key

    # 3. Açıkça verilen anahtar veya tekli kutudaki anahtar hedef sağlayıcıyla çakışmıyorsa kullan
    aday = (verilen_anahtar or "").strip()
    if aday and not _onek_cakismasi_var_mi(hedef_kod, aday):
        return aday

    try:
        tekli = str(st.session_state.get("acik_kaynak_api_key", "")).strip()
        if tekli and not _onek_cakismasi_var_mi(hedef_kod, tekli):
            return tekli
    except Exception:
        pass

    return ""


def _anahtardan_bulut_saglayici_bul(secili: str, anahtar: str) -> str:
    """
    Kullanıcı Ollama veya Pollinations seçili bırakmış olsa bile girilmiş Groq / Gemini /
    OpenRouter / Cerebras / NVIDIA NIM / GitHub / HuggingFace anahtarından doğru bulut
    sağlayıcısını otomatik olarak tanır.
    """
    if secili in _BULUT_SAGLAYICI_KODLARI and anahtar:
        return secili
    if not anahtar:
        return ""
    dogrulama = bulut_anahtar_formati_dogrula(anahtar, secili=secili)
    if dogrulama["saglayici"]:
        return dogrulama["saglayici"]
    return "groq_cloud" if secili == "ollama_local" else ""


_STANDART_TARAYICI_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
)
_SON_AI_HATA_KAYDI = {}


def _hata_kaydet(kod: str, mesaj: str):
    _SON_AI_HATA_KAYDI[kod] = str(mesaj)[:180]
    try:
        tani = st.session_state.get("son_ai_tani")
        if not isinstance(tani, dict):
            tani = {}
        tani[kod] = str(mesaj)[:180]
        st.session_state["son_ai_tani"] = tani
    except Exception:
        pass


_GROQ_MODEL_ONBELLEK = {"liste": None, "zaman": 0.0}
# Kota (HTTP 429) alan model → bu zamana kadar atlanır (her mesajda boşa yeniden denenmez)
_KOTA_BEKLEME = {}


def _kota_bekleme_suresi(hata) -> float:
    """429 yanıtındaki Retry-After başlığını okur (yoksa 60 sn; en az 10 sn, en fazla 1 saat)."""
    try:
        deger = float(hata.headers.get("retry-after") or 60)
    except Exception:
        deger = 60.0
    return max(10.0, min(3600.0, deger))


def ai_kotasi_dolu_mu() -> bool:
    """Groq'un tüm bilinen modelleri şu an kota beklemesindeyse True."""
    simdi = time.time()
    aktif = [m for m, bitis in _KOTA_BEKLEME.items() if bitis > simdi]
    return len(aktif) >= 2


def _groq_aktif_model_kesfet(anahtar: str, models_url_ozel: str = None) -> list:
    """Groq /openai/v1/models ucundan hesabın şu an aktif olan sohbet modellerini canlı çeker (404 kendi kendini onarır!).
    Sonuç 1 saat önbellekte tutulur (her soruda tekrar çekilmez)."""
    if _GROQ_MODEL_ONBELLEK["liste"] and time.time() - _GROQ_MODEL_ONBELLEK["zaman"] < 3600 and not models_url_ozel:
        return list(_GROQ_MODEL_ONBELLEK["liste"])
    try:
        url = models_url_ozel or "https://api.groq.com/openai/v1/models"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {anahtar}",
                "Accept": "application/json",
                "User-Agent": _STANDART_TARAYICI_UA,
            },
        )
        with urllib.request.urlopen(req, timeout=5.0) as r:
            veri = json.loads(r.read().decode("utf-8"))
        tum = [m.get("id", "") for m in veri.get("data", []) if m.get("id")]
        # Yalnızca sohbet modelleri (whisper, guard, tts, embed hariç)
        sohbet = [
            mid for mid in tum
            if not any(x in mid.lower() for x in ("whisper", "guard", "tts", "orpheus", "playai", "embed", "safeguard", "prompt-guard", "allam"))
        ]
        oncelik = ["gpt-oss-120b", "llama-3.3-70b", "gpt-oss-20b", "qwen", "llama-4", "llama-3.1-8b-instant", "gemma"]
        sirali = []
        for on in oncelik:
            for mid in sohbet:
                if on in mid.lower() and mid not in sirali:
                    sirali.append(mid)
        for mid in sohbet:
            if mid not in sirali:
                sirali.append(mid)
        if sirali and not models_url_ozel:
            _GROQ_MODEL_ONBELLEK.update(liste=sirali[:4], zaman=time.time())
        return sirali[:4]
    except Exception:
        return []


def canli_baglanti_doktoru_calistir() -> list:
    """
    Groq/Seçili Bulut AI, Pollinations, Wikipedia TR ve Open-Meteo'yu paralel test eder;
    gizli hata bırakmadan tam HTTP durumunu ve süresini döndürür.
    """
    secili = st.session_state.get("acik_kaynak_saglayici", "pollinations_free")
    anahtar = st.session_state.get("acik_kaynak_api_key", "").strip()
    if not anahtar:
        k_oto, a_oto = _buluttan_anahtar_bul(secili)
        if a_oto:
            secili, anahtar = k_oto, a_oto

    sonuclar = []

    def _tek_bulut_test_et(kod: str, key: str):
        bilgi = ACIK_KAYNAK_AI_SAGLAYICILARI[kod]
        t0 = time.time()
        try:
            payload = {"model": bilgi["model"], "messages": [{"role": "user", "content": "Merhaba, tek kelime yaz."}], "max_tokens": 16}
            hdrs = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {key}",
                "User-Agent": _STANDART_TARAYICI_UA,
            }
            if kod == "github_models":
                hdrs["Accept"] = "application/vnd.github+json"
                hdrs["X-GitHub-Api-Version"] = "2022-11-28"
            elif kod == "openrouter":
                hdrs["HTTP-Referer"] = "https://arex-ai-studio.streamlit.app"
                hdrs["X-Title"] = "AREX AI Studio"
            req = urllib.request.Request(bilgi["url"], data=json.dumps(payload).encode("utf-8"), headers=hdrs, method="POST")
            with urllib.request.urlopen(req, timeout=6.0) as r:
                json.loads(r.read().decode("utf-8"))
            return (f"⚡ {bilgi['ad'].split('—')[0].strip()} ({bilgi['model']})", True, f"HTTP 200 OK ({time.time() - t0:.2f} sn)")
        except urllib.error.HTTPError as he:
            if he.code == 401:
                return (f"⚡ {kod}", False, "HTTP 401 — Anahtar geçersiz veya iptal edilmiş")
            if he.code == 403:
                return (f"⚡ {kod}", False, "HTTP 403 — Erişim engeli veya yetki eksik")
            if he.code == 429:
                return (f"⚡ {kod}", False, "HTTP 429 — Dakikalık kota dolu (yedek modele geçer)")
            _detay = ""
            try:
                _detay = he.read().decode("utf-8", errors="ignore")[:120]
            except Exception:
                pass
            # v12.5 GROQ 404 OTOMATİK ONARIM: Model 404 verirse /openai/v1/models ucundan canlı aktif modeli bulur!
            if he.code == 404 and kod == "groq_cloud":
                _aday_canli = _groq_aktif_model_kesfet(key)
                for _ek_m in ("llama-3.3-70b-versatile", "openai/gpt-oss-120b", "llama-3.1-8b-instant", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"):
                    if _ek_m not in _aday_canli:
                        _aday_canli.append(_ek_m)
                for _cm in _aday_canli[:4]:
                    try:
                        p2 = {"model": _cm, "messages": [{"role": "user", "content": "Merhaba"}], "max_tokens": 16}
                        r2 = urllib.request.Request(bilgi["url"], data=json.dumps(p2).encode("utf-8"), headers=hdrs, method="POST")
                        with urllib.request.urlopen(r2, timeout=6.0) as resp2:
                            json.loads(resp2.read().decode("utf-8"))
                        ACIK_KAYNAK_AI_SAGLAYICILARI["groq_cloud"]["model"] = _cm
                        return (f"⚡ Groq Cloud ({_cm})", True, f"HTTP 200 OK — 404 otomatik onarıldı ({time.time() - t0:.2f} sn)")
                    except Exception:
                        continue
            return (f"⚡ {kod}", False, f"HTTP {he.code}: {he.reason} {_detay}")
        except Exception as e:
            return (f"⚡ {kod}", False, f"Bağlantı hatası: {str(e)[:90]}")

    def _test_bulut():
        tum_ciftler = _tum_bulut_anahtarlarini_topla(oncelikli_kod=secili)
        if anahtar:
            birincil_kod = _anahtardan_bulut_saglayici_bul(secili, anahtar) or "groq_cloud"
            if birincil_kod not in [c[0] for c in tum_ciftler]:
                tum_ciftler.insert(0, (birincil_kod, anahtar))
        if not tum_ciftler:
            return ("🔑 Bulut API Anahtarı", False, "Anahtar girilmemiş (Çoklu API Bağlantı Merkezi veya Secrets kontrol et)")
        if len(tum_ciftler) == 1:
            return _tek_bulut_test_et(tum_ciftler[0][0], tum_ciftler[0][1])
        ozetler = []
        hepsi_ok = True
        for k_item, a_item in tum_ciftler[:4]:
            ad_i, ok_i, msj_i = _tek_bulut_test_et(k_item, a_item)
            if not ok_i:
                hepsi_ok = False
            ozetler.append(f"{'✅' if ok_i else '❌'} {ad_i}: {msj_i}")
        return (f"🔌 Çoklu Bulut API ({len(tum_ciftler)} Bağlı)", hepsi_ok, " | ".join(ozetler))

    def _test_url(ad: str, url: str):
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _STANDART_TARAYICI_UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=5.0) as r:
                r.read(256)
            return (ad, True, f"HTTP 200 OK ({time.time() - t0:.2f} sn)")
        except urllib.error.HTTPError as he:
            return (ad, False, f"HTTP {he.code}: {he.reason}")
        except Exception as e:
            return (ad, False, f"Bağlantı hatası: {str(e)[:90]}")

    tum_ciftler = _tum_bulut_anahtarlarini_topla(oncelikli_kod=secili)
    if anahtar:
        birincil_kod = _anahtardan_bulut_saglayici_bul(secili, anahtar) or "groq_cloud"
        if birincil_kod not in [c[0] for c in tum_ciftler]:
            tum_ciftler.insert(0, (birincil_kod, anahtar))

    gorevler = []
    if not tum_ciftler:
        gorevler.append(lambda: ("🔑 Bulut API Anahtarı", False, "Anahtar girilmemiş (Çoklu API Bağlantı Merkezi veya Secrets kontrol et)"))
    else:
        for _tk, _ta in tum_ciftler[:5]:
            gorevler.append(lambda _k=_tk, _a=_ta: _tek_bulut_test_et(_k, _a))

    gorevler.extend([
        lambda: _test_url("🌐 Pollinations AI", "https://text.pollinations.ai/merhaba?model=openai-fast"),
        lambda: _test_url("📖 Wikipedia TR", "https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch=Istanbul&srlimit=1&format=json"),
        lambda: _test_url("🌤️ Open-Meteo Hava", "https://api.open-meteo.com/v1/forecast?latitude=41.0082&longitude=28.9784&current=temperature_2m"),
    ])
    with ThreadPoolExecutor(max_workers=min(8, len(gorevler))) as havuz:
        futs = [havuz.submit(g) for g in gorevler]
        for f in futs:
            try:
                sonuclar.append(f.result(timeout=7.5))
            except Exception as e:
                sonuclar.append(("⚠️ Test", False, str(e)[:80]))
    return sonuclar


def _bulut_anahtarli_ai_cagir(
    soru: str,
    secili: str,
    anahtar: str,
    sistem_prompt: str,
    gecmis_mesajlar: list,
    ek_baglam: str = "",
    ozel_url: str = None,
) -> tuple:
    """
    v11.3 — Cloudflare-uyumlu tarayıcı başlıkları, 6.5 sn hızlı zaman aşımı,
    HTTP 401/403 anında çıkış (takılmayı önler) ve tam hata günlüğü.
    """
    hedef_kod = _anahtardan_bulut_saglayici_bul(secili, anahtar)
    if not hedef_kod or not anahtar:
        return None, None
    bilgi = ACIK_KAYNAK_AI_SAGLAYICILARI[hedef_kod]
    try:
        hedef_url = ozel_url or st.session_state.get("test_bulut_url") or bilgi["url"]
    except Exception:
        hedef_url = ozel_url or bilgi["url"]
    # v12.2 Çoklu Model Kaskadı: Bir model geçici olarak 404/429 verirse
    # kullanıcıya hata göstermeden anında sıradaki güçlü modele geçilir.
    _model_adaylari = [bilgi["model"]]
    if hedef_kod == "groq_cloud":
        # Önbellekteki canlı model listesi (varsa) → 404 turu yaşanmaz
        for _yedek_m in (_GROQ_MODEL_ONBELLEK.get("liste") or ("openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b")):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)
    elif hedef_kod == "openrouter":
        for _yedek_m in (
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "google/gemma-4-31b-it:free",
            "qwen/qwen3.8-27b:free",
        ):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)
    elif hedef_kod == "deepseek_cloud":
        for _yedek_m in ("deepseek-v4-pro", "deepseek-v4-flash"):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)
    elif hedef_kod == "gemini_free":
        for _yedek_m in ("gemini-2.5-flash", "gemini-2.0-flash"):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)
    elif hedef_kod == "cerebras_cloud":
        for _yedek_m in ("qwen-3.8-27b", "llama3.1-8b"):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)
    elif hedef_kod == "together_cloud":
        for _yedek_m in ("meta-llama/Llama-4-Scout-17B-16E-Instruct", "Qwen/Qwen2.5-72B-Instruct-Turbo"):
            if _yedek_m not in _model_adaylari:
                _model_adaylari.append(_yedek_m)

    _bekleyen = [m for m in _model_adaylari if _KOTA_BEKLEME.get(f"{hedef_kod}:{m}", 0) > time.time()]
    if _bekleyen and len(_bekleyen) == len(_model_adaylari):
        return None, None  # tüm modeller kota beklemesinde → anında sıradaki ücretsiz kaynağa geç
    _model_adaylari = [m for m in _model_adaylari if m not in _bekleyen]  # kotası dolu modelleri atla
    for _aktif_model in _model_adaylari:
        try:
            payload = {
                "model": _aktif_model,
                "messages": (
                    [{"role": "system", "content": _uslup_ekle(sistem_prompt)}]
                    + [
                        {"role": m.get("role", "user"), "content": str(m.get("content", ""))[:2200]}
                        for m in gecmis_mesajlar[-12:]
                        if m.get("role") in ("user", "assistant") and m.get("content")
                    ]
                    + [{"role": "user", "content": soru}]
                ),
                "temperature": 0.45 if not ek_baglam else 0.35,
                "max_tokens": 4096,
            }
            if "gpt-oss" in _aktif_model:
                # Akıl yürütme gerekmeyen sohbette kısa düşünme → ~%30 daha hızlı; muhakeme isteğinde orta
                payload["reasoning_effort"] = "medium" if "AKIL YÜRÜTME TALİMATI" in (ek_baglam or "") else "low"
            hdrs = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {anahtar}",
                "User-Agent": _STANDART_TARAYICI_UA,
            }
            if hedef_kod == "github_models":
                hdrs["Accept"] = "application/vnd.github+json"
                hdrs["X-GitHub-Api-Version"] = "2022-11-28"
            elif hedef_kod == "openrouter":
                hdrs["HTTP-Referer"] = "https://arex-ai-studio.streamlit.app"
                hdrs["X-Title"] = "AREX AI Studio"
            req = urllib.request.Request(
                hedef_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=hdrs,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=(15 if hedef_kod == "groq_cloud" else 6.5)) as resp:
                veri = json.loads(resp.read().decode("utf-8"))
                cevap = _ollama_yanit_temizle(veri["choices"][0]["message"]["content"])
                if cevap:
                    _hata_kaydet(hedef_kod, f"OK ({_aktif_model})")
                    try:
                        _gtx_t = st.session_state.get("test_gtx_url")
                    except Exception:
                        _gtx_t = None
                    cevap = _turkce_dil_kilidi_uygula(cevap, gtx_url_ozel=_gtx_t)
                    return cevap, f"{_aktif_model}"
        except urllib.error.HTTPError as he:
            _hata_kaydet(hedef_kod, f"HTTP {he.code} ({_aktif_model}): {he.reason}")
            if he.code == 429:
                _KOTA_BEKLEME[f"{hedef_kod}:{_aktif_model}"] = time.time() + _kota_bekleme_suresi(he)
            if he.code in (401, 403):
                break
            if he.code == 404 and hedef_kod == "groq_cloud":
                try:
                    _m_url = st.session_state.get("test_groq_models_url")
                except Exception:
                    _m_url = None
                for _kesif_m in _groq_aktif_model_kesfet(anahtar, models_url_ozel=_m_url):
                    if _kesif_m not in _model_adaylari:
                        _model_adaylari.append(_kesif_m)
            continue
        except Exception as e:
            _hata_kaydet(hedef_kod, f"Hata ({_aktif_model}): {str(e)[:100]}")
            continue
    return None, None


def _pollinations_ai_cagir(
    soru: str,
    sistem_prompt: str,
    gecmis_mesajlar: list,
    ek_baglam: str = "",
    endpoint_url: str = "https://text.pollinations.ai/openai",
) -> tuple:
    """Anahtarsız ücretsiz Pollinations açık kaynak AI köprüsünü çağırır."""
    try:
        payload = {
            "model": "openai-fast",  # anonim ücretsiz katman (2026: "openai" modeli ücretli → HTTP 402)
            "messages": (
                [{"role": "system", "content": _uslup_ekle(sistem_prompt)}]
                + [
                    {"role": m.get("role", "user"), "content": str(m.get("content", ""))[:2200]}
                    for m in gecmis_mesajlar[-12:]
                    if m.get("role") in ("user", "assistant") and m.get("content")
                ]
                + [{"role": "user", "content": soru}]
            ),
            "temperature": 0.45 if not ek_baglam else 0.35,
            "max_tokens": 2048,
        }
        _poll_uclar = [endpoint_url]
        if "gen.pollinations.ai" not in endpoint_url and "127.0.0.1" not in endpoint_url and "localhost" not in endpoint_url:
            _poll_uclar.append("https://gen.pollinations.ai/v1/chat/completions")
        for _p_url in _poll_uclar:
            try:
                req = urllib.request.Request(
                    _p_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": _STANDART_TARAYICI_UA,
                        "Referer": "https://arex-ai.streamlit.app/",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=5.5) as resp:
                    ham = resp.read().decode("utf-8").strip()
                    if ham.startswith("{"):
                        veri = json.loads(ham)
                        cevap = _ollama_yanit_temizle(veri.get("choices", [{}])[0].get("message", {}).get("content", ""))
                    else:
                        cevap = _ollama_yanit_temizle(ham)
                    if cevap and len(cevap) > 10:
                        return cevap, "Pollinations AI"
            except Exception:
                continue
    except Exception:
        pass
    # Yedek 1B: Pollinations Mistral modeli (openai yoğun olduğunda anında devreye girer)
    if endpoint_url == "https://text.pollinations.ai/openai":
        try:
            payload_m = {
                "model": "mistral",
                "messages": [
                    {"role": "system", "content": _uslup_ekle(sistem_prompt)},
                    {"role": "user", "content": soru},
                ],
                "temperature": 0.4,
            }
            req_m = urllib.request.Request(
                endpoint_url,
                data=json.dumps(payload_m).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": _STANDART_TARAYICI_UA},
                method="POST",
            )
            with urllib.request.urlopen(req_m, timeout=4.5) as resp_m:
                veri_m = json.loads(resp_m.read().decode("utf-8"))
                cevap_m = _ollama_yanit_temizle(veri_m.get("choices", [{}])[0].get("message", {}).get("content", ""))
                if cevap_m and len(cevap_m) > 10:
                    return _turkce_dil_kilidi_uygula(cevap_m), "Pollinations (Mistral)"
        except Exception:
            pass
    # Yedek 1C: Pollinations DeepSeek V3 (Zengin kelime verimliliği ve mantık yedeği)
    if endpoint_url == "https://text.pollinations.ai/openai":
        try:
            payload_d = {
                "model": "deepseek",
                "messages": [
                    {"role": "system", "content": _uslup_ekle(sistem_prompt)},
                    {"role": "user", "content": soru},
                ],
                "temperature": 0.4,
                "max_tokens": 2048,
            }
            req_d = urllib.request.Request(
                endpoint_url,
                data=json.dumps(payload_d).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": _STANDART_TARAYICI_UA, "Referer": "https://arex-ai.streamlit.app/"},
                method="POST",
            )
            with urllib.request.urlopen(req_d, timeout=4.5) as resp_d:
                veri_d = json.loads(resp_d.read().decode("utf-8"))
                cevap_d = _ollama_yanit_temizle(veri_d.get("choices", [{}])[0].get("message", {}).get("content", ""))
                if cevap_d and len(cevap_d) > 10:
                    return _turkce_dil_kilidi_uygula(cevap_d), "Pollinations (DeepSeek)"
        except Exception:
            pass
    # Yedek 2: Bağlantı kopmasına karşı Pollinations hafif GET uç noktası (openai-fast)
    if endpoint_url == "https://text.pollinations.ai/openai":
        try:
            kisa_istek = urllib.parse.quote(f"Türkçe ve samimi cevapla: {soru[:350]}")
            req2 = urllib.request.Request(
                f"https://text.pollinations.ai/{kisa_istek}?model=openai-fast",
                headers={"User-Agent": _STANDART_TARAYICI_UA},
            )
            with urllib.request.urlopen(req2, timeout=4.5) as resp2:
                ham2 = _ollama_yanit_temizle(resp2.read().decode("utf-8"))
            if ham2 and len(ham2) > 10:
                return ham2, "Pollinations Hızlı Yedek"
        except Exception:
            pass
    return None, None


def _ollama_ham_cagir(
    soru: str,
    ollama_url: str,
    ek_baglam: str = "",
    gecmis_mesajlar: list = None,
    sistem_prompt_ozel: str = None,
    model_adi: str = None,
) -> tuple:
    """Ollama'dan başlık öneki olmadan saf, temizlenmiş Türkçe yanıt ve etiket döndürür (thread-safe)."""
    o_yanit, o_etiket = ollama_soru_sor(
        soru,
        model_adi=model_adi,
        base_url=ollama_url,
        ek_baglam=ek_baglam,
        gecmis_mesajlar=gecmis_mesajlar,
        sistem_prompt_ozel=sistem_prompt_ozel,
    )
    if not o_yanit:
        return None, None
    saf = re.sub(r"^🦙\s*\*\*Ollama\s*\([^)]+\):\*\*\s*", "", o_yanit).strip()
    return (saf if saf else o_yanit), o_etiket


def coklu_ai_ortak_akil_sor(
    soru: str,
    saglayici_kodu: str = None,
    api_key: str = "",
    ek_baglam: str = "",
    gecmis_kullan: bool = True,
) -> tuple:
    """
    v10.3 — TUZAKSIZ, MANTIK ÖNCELİKLİ ÇOKLU AI & OLLAMA ORTAK AKIL KONSEYİ:
      • Ollama seçili olsa bile girilmiş Groq/OpenRouter/HF/Mistral/Cerebras anahtarı varsa
        bulut sağlayıcı konseye OTOMATİK dahil edilir.
      • ollama_aktif kapalıysa (ve kullanıcı özellikle ollama_local seçmediyse) Ollama zorla çağrılmaz.
      • Toplam bekleme süresi en fazla 6.0 sn ile sınırlandırılır; hiçbir model akışı kilitleyemez.
    """
    secili = saglayici_kodu or st.session_state.get("acik_kaynak_saglayici", "pollinations_free")
    if saglayici_kodu and saglayici_kodu in _BULUT_SAGLAYICI_KODLARI:
        # Doğrudan 'deepseek:', 'groq:', 'gemini:', 'openrouter:' istendiyse YALNIZCA o sağlayıcının anahtarını al!
        anahtar = _saglayici_icin_anahtar_bul(saglayici_kodu, api_key)
    else:
        anahtar = (api_key or _saglayici_icin_anahtar_bul(secili, "") or st.session_state.get("acik_kaynak_api_key", "")).strip()
    if not anahtar:
        _sec_oto_kod, _sec_oto_key = _buluttan_anahtar_bul(secili)
        if _sec_oto_key:
            secili, anahtar = _sec_oto_kod, _sec_oto_key
    bulut_kod = _anahtardan_bulut_saglayici_bul(secili, anahtar)
    ollama_url = _ollama_url_normallestir(st.session_state.get("ollama_url", OLLAMA_VARSAYILAN_URL))
    ollama_model = st.session_state.get("ollama_secili_model", "llama3.2")
    pollinations_url = st.session_state.get("pollinations_url_ozel", "https://text.pollinations.ai/openai")
    gecmis_mesajlar = ((st.session_state.get("messages") or [])[-10:] if gecmis_kullan else [])
    ollama_izinli = bool(st.session_state.get("ollama_aktif", False)) or secili == "ollama_local" or saglayici_kodu == "ollama_local"

    sistem_prompt = (
        "Sen Ahmet tarafından geliştirilen 'AREX AI Studio' adlı Türkçe yapay zeka asistanısın. "
        "Ahmet İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi; "
        f"TEKNOFEST İHA ve TÜBİTAK akıllı bebek arabası projeleri geliştiriyor. BUGÜNÜN GERÇEK TARİHİ: {_guncel_tarih_etiketi()}. Güncel açık kaynak verilerini her zaman esas al. "
        "Ahmet ile candan, samimi ve anlaşılır ama bilgi verirken son derece net, düzenli ve bozuksuz Türkçeyle konuş. "
        "Bilmediğin bir veriyi asla uydurma; <think> gibi iç düşünce etiketleri yazma."
        + (
            " ÇOCUK DOSTU MOD AKTİF: Karşında meraklı bir çocuk var! Çok yumuşak, neşeli, basit, güvenli ve eğitici bir Türkçe ile konuş."
            if st.session_state.get("cocuk_dostu_mod", False)
            else ""
        )
    )
    if ek_baglam and ek_baglam.strip():
        sistem_prompt += (
            "\n\nAşağıda açık kaynaklardan (Wikipedia, TDK, Hava Durumu, Yemek Tarifleri, "
            "81 İl & 195+ Ülke, Harita, Piyasa/Kur veya Fiyat) toplanmış doğrulanmış gerçek veriler var. "
            "Bu verileri çarpıtmadan ve uydurma eklemeden kullan:\n"
            f"{ek_baglam.strip()[:6500]}"
        )

    _uzun_mod_mu = bool(ek_baglam and ("BÖLÜM #" in ek_baglam or "UZUN ANLATIM" in ek_baglam))
    _konsey_zaman_limiti = 10.5 if _uzun_mod_mu else 6.5

    gorevler = {}
    _bulut_ciftleri = []
    if bulut_kod and anahtar:
        _bulut_ciftleri.append((bulut_kod, anahtar))
    for _ek_kod, _ek_key in _tum_bulut_anahtarlarini_topla(oncelikli_kod=bulut_kod or ""):
        if _ek_kod not in [c[0] for c in _bulut_ciftleri]:
            _bulut_ciftleri.append((_ek_kod, _ek_key))
        if len(_bulut_ciftleri) >= 3:
            break

    for _b_idx, (_b_kod, _b_key) in enumerate(_bulut_ciftleri):
        gorevler[f"bulut_{_b_idx}_{_b_kod}"] = (
            lambda _k=_b_kod, _a=_b_key: _bulut_anahtarli_ai_cagir(
                soru, _k, _a, sistem_prompt, gecmis_mesajlar, ek_baglam=ek_baglam
            )
        )

    if st.session_state.get("acik_kaynak_ai_aktif", True):
        gorevler["pollinations"] = lambda: _pollinations_ai_cagir(
            soru, sistem_prompt, gecmis_mesajlar, ek_baglam=ek_baglam, endpoint_url=pollinations_url
        )

    o_canli = False
    if ollama_izinli:
        o_canli, _ = ollama_hizli_durum_kontrol(ollama_url)
        if o_canli:
            gorevler["ollama"] = lambda: _ollama_ham_cagir(
                soru, ollama_url, ek_baglam=ek_baglam, gecmis_mesajlar=gecmis_mesajlar, model_adi=ollama_model
            )

    if not gorevler:
        return None, None

    adaylar = []
    baslangic_t = time.time()
    ilk_yanit_t = None
    havuz = ThreadPoolExecutor(max_workers=len(gorevler))
    gelecekler = {havuz.submit(fn): ad for ad, fn in gorevler.items()}
    bekleyen = set(gelecekler.keys())
    try:
        while bekleyen:
            simdi = time.time()
            if ilk_yanit_t is not None:
                en_yuksek_puan = max((a[0] for a in adaylar), default=0.0)
                ek_bekleme = 2.4 if _uzun_mod_mu else (1.8 if en_yuksek_puan >= 14.0 else 3.0)
                kalan = min(ek_bekleme - (simdi - ilk_yanit_t), _konsey_zaman_limiti - (simdi - baslangic_t))
            else:
                kalan = _konsey_zaman_limiti - (simdi - baslangic_t)
            if kalan <= 0.05:
                break
            bitenler, bekleyen = wait(bekleyen, timeout=kalan, return_when=FIRST_COMPLETED)
            if not bitenler:
                break
            for fut in bitenler:
                try:
                    metin, etiket = fut.result(timeout=0.1)
                    if metin and etiket:
                        puan = _aday_yanit_puanla(metin, ek_baglam)
                        if puan > 0:
                            adaylar.append((puan, etiket, metin))
                            if ilk_yanit_t is None:
                                ilk_yanit_t = time.time()
                except Exception:
                    pass
    except Exception:
        pass
    finally:
        havuz.shutdown(wait=False, cancel_futures=True)

    if not adaylar:
        return None, None

    adaylar.sort(key=lambda x: x[0], reverse=True)

    if len(adaylar) == 1:
        _, tek_etiket, tek_metin = adaylar[0]
        return f"🤖 **AREX AI:**\n\n{tek_metin}", tek_etiket

    en_iyi_puan, en_iyi_etiket, en_iyi_metin = adaylar[0]
    ikinci_puan = adaylar[1][0]
    if (en_iyi_puan - ikinci_puan) >= 6.5:
        return (
            f"🧠 **AREX AI (En Mantıklı Seçim — {en_iyi_etiket}):**\n\n{en_iyi_metin}",
            f"Ortak Akıl (Öncelikli: {en_iyi_etiket})",
        )

    guclu_adaylar = [a for a in adaylar if (en_iyi_puan - a[0]) < 6.5]
    katilanlar = [e for _, e, _ in guclu_adaylar]
    _aday_kesim = 4500 if _uzun_mod_mu else 2600
    aday_bloklari = [
        f"### Kaynak {idx} ({etiket}):\n{metin[:_aday_kesim]}"
        for idx, (_, etiket, metin) in enumerate(guclu_adaylar, 1)
    ]
    aday_metni = "\n\n".join(aday_bloklari)

    hakem_sistem = (
        "Sen AREX AI Studio'nun Baş Hakem (Kaptan / Ortak Akıl) Sentez Motorusun. "
        "Görevin: Farklı açık kaynak yapay zekalardan gelen yanıtları ve varsa doğrulanmış "
        "açık kaynak verilerini karşılaştırmak; çelişkili veya uydurma kısımları elemek "
        "ve en doğru bilgileri tek bir akıcı, samimi Türkçe cevapta birleştirmek.\n"
        "KESİN KURALLAR: 'Kaynak 1' gibi teknik ifadeler yazma; yalnızca temiz Türkçe yaz; <think> bırakma. "
        "Doğrulanmış verilerde tıklanabilir [Başlık](URL) kaynak linkleri veya harita linkleri varsa onları ASLA silme, aynen koru."
        + (" UZUN ANLATIM MODU AKTİF: Yanıtı kesinlikle kısaltma; en az 5-6 zengin paragrafla sürükleyici ve derin anlat!" if _uzun_mod_mu else "")
    )
    hakem_soru = (
        f"Ahmet'in Sorusu: {soru}\n\n"
        + (f"Doğrulanmış Açık Kaynak Verisi:\n{ek_baglam.strip()[:4500]}\n\n" if (ek_baglam and ek_baglam.strip()) else "")
        + f"Aday Yanıtlar:\n{aday_metni}\n\n"
        "En mantıklı, en doğru ve en anlaşılır tek Türkçe yanıtı yaz:"
    )

    nihai_cevap = None
    for _hb_kod, _hb_key in _bulut_ciftleri:
        nihai_cevap, _ = _bulut_anahtarli_ai_cagir(hakem_soru, _hb_kod, _hb_key, hakem_sistem, [], ek_baglam="")
        if nihai_cevap:
            break
    if not nihai_cevap and st.session_state.get("acik_kaynak_ai_aktif", True):
        nihai_cevap, _ = _pollinations_ai_cagir(hakem_soru, hakem_sistem, [], ek_baglam="", endpoint_url=pollinations_url)
    if not nihai_cevap and o_canli:
        nihai_cevap, _ = _ollama_ham_cagir(
            hakem_soru, ollama_url, ek_baglam="", gecmis_mesajlar=[], sistem_prompt_ozel=hakem_sistem, model_adi=ollama_model
        )

    birlesik_etiket = " + ".join(katilanlar)
    if nihai_cevap:
        return f"🧠 **AREX AI (Ortak Akıl):**\n\n{nihai_cevap}", f"Ortak Akıl ({birlesik_etiket})"

    return f"🧠 **AREX AI (En Mantıklı Seçim):**\n\n{en_iyi_metin}", f"Ortak Akıl ({en_iyi_etiket})"


def acik_kaynak_ai_sor(soru: str, saglayici_kodu: str = None, api_key: str = "", ek_baglam: str = "", gecmis_kullan: bool = True) -> tuple:
    """
    v10.3 — TUZAKSIZ VE KESİNTİSİZ AÇIK KAYNAK AI & OLLAMA YÖNLENDİRME ZİNCİRİ:
      1. Kullanıcı Groq / OpenRouter / HuggingFace / Mistral / Cerebras seçtiyse (veya API anahtarı girdiyse)
         Ollama açık olsa bile seçili bulut AI ÖNCE çalışır — Ollama asla Groq'u kilitlemez!
      2. Kullanıcı açıkça 'ollama:' yazdıysa veya sağlayıcı olarak 'ollama_local' seçtiyse:
         • Önce Ollama denenir (1 sn hızlı canlılık kontrolü + 18 sn üst sınır).
         • Ollama kapalıysa, hata verirse veya boş dönerse TAKILMAZ — anında Groq/Bulut AI -> Pollinations -> Wikipedia akışına çıkar!
      3. Ortak Akıl Konseyi açıksa (ve zorla 'ollama:' öneki yazılmadıysa) tüm aktif kaynaklar paralel yarışır.
    """
    secili = saglayici_kodu or st.session_state.get("acik_kaynak_saglayici", "pollinations_free")
    if saglayici_kodu and saglayici_kodu in _BULUT_SAGLAYICI_KODLARI:
        anahtar = _saglayici_icin_anahtar_bul(saglayici_kodu, api_key)
    else:
        anahtar = (api_key or _saglayici_icin_anahtar_bul(secili, "") or st.session_state.get("acik_kaynak_api_key", "")).strip()
    if not anahtar:
        _sec_oto_kod, _sec_oto_key = _buluttan_anahtar_bul(secili)
        if _sec_oto_key:
            secili, anahtar = _sec_oto_kod, _sec_oto_key
    bulut_kod = _anahtardan_bulut_saglayici_bul(secili, anahtar)
    ollama_url = _ollama_url_normallestir(st.session_state.get("ollama_url", OLLAMA_VARSAYILAN_URL))
    pollinations_url = st.session_state.get("pollinations_url_ozel", "https://text.pollinations.ai/openai")
    gecmis_mesajlar = ((st.session_state.get("messages") or [])[-10:] if gecmis_kullan else [])
    ollama_izinli = bool(st.session_state.get("ollama_aktif", False)) or secili == "ollama_local" or saglayici_kodu == "ollama_local"

    # 0. Çoklu AI + Ollama Ortak Akıl Konseyi
    if st.session_state.get("ortak_akil_aktif", False) and saglayici_kodu != "ollama_local":
        konsey_yanit, konsey_etiket = coklu_ai_ortak_akil_sor(
            soru, saglayici_kodu=secili, api_key=anahtar, ek_baglam=ek_baglam, gecmis_kullan=gecmis_kullan
        )
        if konsey_yanit:
            return konsey_yanit, konsey_etiket

    sistem_prompt = (
        "Sen Ahmet tarafından geliştirilen 'AREX AI Studio' adlı Türkçe yapay zeka asistanısın. "
        "Ahmet İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi, "
        f"TEKNOFEST İHA ve TÜBİTAK akıllı bebek arabası projeleri geliştiriyor. BUGÜNÜN GERÇEK TARİHİ: {_guncel_tarih_etiketi()}. Güncel açık kaynak verilerini her zaman esas al. "
        "Ahmet ile candan, samimi ve sıcakkanlı sohbet et; bilgi veya açıklama verirken soruya uygun derinlikte, akıcı ve doyurucu bir Türkçe ile anlat. "
        "Bilmediğin bir veriyi asla uydurma; <think> gibi iç düşünce etiketleri kullanma."
        + (
            " ÇOCUK DOSTU MOD AKTİF: Karşında meraklı bir çocuk var! Çok yumuşak, neşeli, basit, güvenli, eğitici ve hayal gücünü destekleyen bir Türkçe ile konuş; gerekirse kısa örnekler veya minik hikayeler kullan."
            if st.session_state.get("cocuk_dostu_mod", False)
            else ""
        )
    )
    if ek_baglam and ek_baglam.strip():
        sistem_prompt += (
            "\n\nAşağıda AREX AI otonom ajanının açık kaynaklardan (Wikipedia, TDK, Hava Durumu, "
            "Yemek Tarifleri, 81 İl & 195+ Ülke, Harita, Piyasa/Kur veya Fiyat) senin için topladığı "
            "doğrulanmış güncel veriler var. Bu verileri çarpıtmadan, kopyala-yapıştır yapmadan "
            "Ahmet'e çok akıcı, candan ve mantıklı tek bir Türkçe cevap olarak sentezle:\n"
            f"{ek_baglam[:8000]}"
        )

    # A. Kullanıcı açıkça 'ollama:' yazdıysa veya sağlayıcı olarak özellikle 'ollama_local' seçtiyse
    if saglayici_kodu == "ollama_local" or secili == "ollama_local":
        o_canli, _ = ollama_hizli_durum_kontrol(ollama_url)
        if o_canli:
            o_yanit, o_etiket = ollama_soru_sor(
                soru,
                base_url=ollama_url,
                ek_baglam=ek_baglam,
                gecmis_mesajlar=gecmis_mesajlar,
            )
            if o_yanit:
                return o_yanit, o_etiket
        # Ollama kapalı veya başarısız oldu -> ASLA TAKILMA, Groq / Bulut / Pollinations'a geç!

    # B. Çoklu Bulut Kaskad Zinciri (Groq -> Cerebras -> NVIDIA NIM -> GitHub Models -> SambaNova -> OpenRouter -> Together -> HF -> Mistral)
    _bulut_adaylari = []
    if bulut_kod and anahtar:
        _bulut_adaylari.append((bulut_kod, anahtar))
    for _ek_kod, _ek_key in _tum_bulut_anahtarlarini_topla(oncelikli_kod=bulut_kod):
        if _ek_kod not in {k for k, _ in _bulut_adaylari}:
            _bulut_adaylari.append((_ek_kod, _ek_key))

    for _b_kod, _b_key in _bulut_adaylari:
        c_metin, c_etiket = _bulut_anahtarli_ai_cagir(
            soru, _b_kod, _b_key, sistem_prompt, gecmis_mesajlar, ek_baglam=ek_baglam
        )
        if c_metin:
            return f"🤖 **AREX AI ({c_etiket}):**\n\n{c_metin}", f"Açık Kaynak AI ({_b_kod})"

    # C. Anahtarsız Pollinations Açık Kaynak AI
    if st.session_state.get("acik_kaynak_ai_aktif", True):
        p_metin, p_etiket = _pollinations_ai_cagir(
            soru, sistem_prompt, gecmis_mesajlar, ek_baglam=ek_baglam, endpoint_url=pollinations_url
        )
        if p_metin:
            return f"🤖 **AREX AI:**\n\n{p_metin}", p_etiket or "Açık Kaynak AI (Canlı)"

    # D. Yerel Ollama Yedeği (Sadece izinliyse ve yukarıda zaten denenmediyse)
    if ollama_izinli and saglayici_kodu != "ollama_local" and secili != "ollama_local":
        o_canli, _ = ollama_hizli_durum_kontrol(ollama_url)
        if o_canli:
            o_yanit, o_etiket = ollama_soru_sor(
                soru,
                base_url=ollama_url,
                ek_baglam=ek_baglam,
                gecmis_mesajlar=gecmis_mesajlar,
            )
            if o_yanit:
                return o_yanit, f"{o_etiket} (Yerel Yedek)"

    return None, None


def coklu_api_ve_canli_baglanti_paneli_goster():
    """
    v12.3 — ÇOKLU API BAĞLANTI MERKEZİ (2+ API AYNI ANDA), DEEPSEEK & CANLI BAĞLANTI PANELİ:
      • Kullanıcı Groq, DeepSeek, Google AI Studio (Gemini), OpenRouter, Cerebras ve
        NVIDIA NIM anahtarlarını aynı anda yan yana girebilir.
      • Girilen tüm anahtarlar oturum havuzuna (coklu_api_anahtarlari) eklenir;
        Ortak Akıl açıkken en fazla 3 bulut AI + Pollinations PARALEL çalışır,
        kapalıyken otomatik kaskad yedekleme yapar.
      • Canlı API Bağlantı Doktoru her bağlı sağlayıcıyı tek tek canlı test eder.
    """
    st.markdown("## 🔌 Çoklu API Bağlantı Merkezi, DeepSeek & Canlı Durum")
    st.caption(
        "Buradan **2 veya daha fazla AI API anahtarını aynı anda** bağlayabilir, "
        "**DeepSeek V4.1-Flash**, **Groq**, **Google AI Studio (Gemini)** ve **OpenRouter** "
        "bağlantılarını tek tıkla canlı test edebilirsin."
    )

    if "coklu_api_anahtarlari" not in st.session_state or not isinstance(st.session_state.get("coklu_api_anahtarlari"), dict):
        st.session_state["coklu_api_anahtarlari"] = {}

    # Mevcut tüm aktif anahtarları özetle
    aktif_liste = _tum_bulut_anahtarlarini_topla(
        oncelikli_kod=st.session_state.get("acik_kaynak_saglayici", "groq_cloud")
    )
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("🔌 Bağlı Bulut API", f"{len(aktif_liste)} Adet")
    c_m2.metric("🧠 Toplam Desteklenen Motor", f"{len(ACIK_KAYNAK_AI_SAGLAYICILARI)} Sağlayıcı")
    _mod_txt = "Paralel Konsey (2-3 API)" if st.session_state.get("ortak_akil_aktif", False) else "Otomatik Kaskad Yedek"
    c_m3.metric("⚙️ Çalışma Modu", _mod_txt)

    st.session_state.ortak_akil_aktif = st.toggle(
        "🧠 İki veya Daha Fazla API'yi Aynı Anda Paralel Çalıştır (Ortak Akıl / Kaptan)",
        value=bool(st.session_state.get("ortak_akil_aktif", False)),
        key="coklu_api_ortak_akil_toggle",
        help="Açıkken bağlı en fazla 3 bulut API + Pollinations aynı anda çalışır ve Baş Hakem en doğru yanıtı birleştirir.",
    )

    tab_groq, tab_bagla, tab_deepseek, tab_canli = st.tabs([
        "⚡ Groq Özel (Tek API ile Hemen Çalışır)",
        "🔑 Çoklu API (İsteğe Bağlı 2+ API)",
        "🐋 DeepSeek Özel Bölümü",
        "📡 Canlı API Bağlantı Testi",
    ])

    with tab_groq:
        st.markdown("### ⚡ Groq Cloud Özel Merkezi (Tek API ile Kesintisiz Çalışır)")
        st.caption(
            "En az 2 API gerekmez — **sadece Groq anahtarını (`gsk_...`)** girip kaydetmen yeterli. "
            "Model 404 verirse sistem `/openai/v1/models` ucundan hesabındaki aktif modeli otomatik bulup kendini onarır."
        )
        _groq_mevcut = (
            st.session_state["coklu_api_anahtarlari"].get("groq_cloud", "")
            or (st.session_state.get("acik_kaynak_api_key", "") if str(st.session_state.get("acik_kaynak_api_key", "")).startswith("gsk_") else "")
        )
        _groq_girdi = st.text_input(
            "🔑 Groq API Anahtarı (console.groq.com/keys):",
            value=_groq_mevcut,
            type="password",
            placeholder="gsk_...",
            key="groq_ozel_anahtar_inp",
        )
        _groq_model_sec = st.selectbox(
            "⚡ Groq Birincil Modeli:",
            options=["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "llama-3.1-8b-instant", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"],
            index=0,
            key="groq_ozel_model_sec",
        )
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            if st.button("💾 Groq'u Bağla & Birincil Motor Yap", use_container_width=True, key="groq_ozel_bagla_btn"):
                _gk = (_groq_girdi or "").strip().strip('"').strip("'")
                if _gk:
                    ACIK_KAYNAK_AI_SAGLAYICILARI["groq_cloud"]["model"] = _groq_model_sec
                    st.session_state["coklu_api_anahtarlari"]["groq_cloud"] = _gk
                    st.session_state["acik_kaynak_saglayici"] = "groq_cloud"
                    st.session_state["acik_kaynak_api_key"] = _gk
                    st.session_state["acik_kaynak_ai_aktif"] = True
                    if not _bulut_ortami_mi():
                        try:
                            sec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit")
                            os.makedirs(sec_dir, exist_ok=True)
                            sec_file = os.path.join(sec_dir, "secrets.toml")
                            mevcut_s = open(sec_file, "r", encoding="utf-8").readlines() if os.path.exists(sec_file) else []
                            mevcut_s = [s for s in mevcut_s if not s.strip().startswith("GROQ_API_KEY")]
                            mevcut_s.append(f'GROQ_API_KEY = "{_gk}"\n')
                            with open(sec_file, "w", encoding="utf-8") as sf:
                                sf.writelines(mevcut_s)
                        except Exception:
                            pass
                    st.success(f"✅ Groq ({_groq_model_sec}) tek başına çalışmaya hazır! Şimdi sağdaki tuşla canlı test edebilirsin.")
                    st.rerun()
                else:
                    st.warning("Lütfen console.groq.com/keys adresinden aldığın gsk_... anahtarını gir.")
        with g_c2:
            if st.button("🧪 Groq'u Canlı Test Et (404 Oto-Onarımlı)", use_container_width=True, key="groq_ozel_test_btn"):
                _gk = (_groq_girdi or "").strip() or _saglayici_icin_anahtar_bul("groq_cloud")
                if not _gk:
                    st.error("❌ Groq anahtarı girilmemiş.")
                else:
                    ACIK_KAYNAK_AI_SAGLAYICILARI["groq_cloud"]["model"] = _groq_model_sec
                    with st.spinner("⚡ Groq canlı test ediliyor (404 olursa otomatik aktif model aranır)..."):
                        _gy, _ge = _bulut_anahtarli_ai_cagir(
                            "Merhaba, tek cümleyle Türkçe selam ver.",
                            "groq_cloud",
                            _gk,
                            "Sen AREX AI Studio asistanısın. Kısa ve temiz Türkçe cevap ver.",
                            [],
                        )
                    if _gy:
                        st.success(f"✅ **Groq Bağlantısı Başarılı ({_ge}):**\n\n{_gy}")
                    else:
                        st.error(f"❌ Groq yanıt vermedi: {_SON_AI_HATA_KAYDI.get('groq_cloud', 'Anahtarı veya internet bağlantısını kontrol et')}")

    with tab_bagla:
        st.info(
            "💡 İstediğin kadar API anahtarını aşağıya girip **'💾 Tüm Bağlı API'leri Kaydet'** tuşuna bas. "
            "Boş bıraktığın kutular pasif kalır; dolu olanların **hepsi birlikte** çalışır."
        )
        havuz = dict(st.session_state.get("coklu_api_anahtarlari", {}))
        # Env/Secrets'taki mevcutları sadece gösterge amaçlı işaretle
        env_harita = {k: v for k, v in aktif_liste}
        slotlar = [
            ("groq_cloud", "⚡ Groq Cloud (Llama 3.3 70B & GPT-OSS 120B)", "gsk_...", "https://console.groq.com/keys"),
            ("deepseek_cloud", "🐋 DeepSeek (V4.1-Flash & V4-Pro)", "sk-...", "https://platform.deepseek.com/api_keys"),
            ("gemini_free", "💎 Google AI Studio (Gemini 4 Hydrogen — 1M Bağlam)", "AIza...", "https://aistudio.google.com/apikey"),
            ("openrouter", "🔀 OpenRouter (openrouter/free & 550B Nemotron)", "sk-or-v1-...", "https://openrouter.ai/keys"),
            ("cerebras_cloud", "🧠 Cerebras Cloud (Llama 3.3 70B — Ultra Hızlı)", "csk-...", "https://cloud.cerebras.ai/"),
            ("nvidia_nim", "🟩 NVIDIA NIM (Llama 3.1 70B)", "nvapi-...", "https://build.nvidia.com/settings/api-keys"),
        ]
        yeni_girdiler = {}
        col_a, col_b = st.columns(2)
        for idx, (kod, baslik, ph, site_url) in enumerate(slotlar):
            hedef_col = col_a if idx % 2 == 0 else col_b
            with hedef_col:
                mevcut_val = havuz.get(kod, "")
                durum_rozet = "🟢 Bağlı" if (mevcut_val or kod in env_harita) else "⚪ Boş"
                yeni_girdiler[kod] = st.text_input(
                    f"{baslik} — {durum_rozet}",
                    value=mevcut_val,
                    type="password",
                    placeholder=ph,
                    key=f"multi_api_inp_{kod}",
                    help=f"Anahtar alma adresi: {site_url}",
                )

        if st.button("💾 Tüm Bağlı API'leri Kaydet & Etkinleştir", use_container_width=True, key="multi_api_kaydet_btn"):
            kaydedilen = 0
            for kod, val in yeni_girdiler.items():
                temiz = (val or "").strip().strip('"').strip("'")
                if temiz:
                    st.session_state["coklu_api_anahtarlari"][kod] = temiz
                    kaydedilen += 1
                elif kod in st.session_state["coklu_api_anahtarlari"]:
                    del st.session_state["coklu_api_anahtarlari"][kod]

            # Birincil sağlayıcıyı otomatik ayarla
            if st.session_state["coklu_api_anahtarlari"]:
                ilk_kod = next(iter(st.session_state["coklu_api_anahtarlari"]))
                st.session_state["acik_kaynak_saglayici"] = ilk_kod
                st.session_state["acik_kaynak_api_key"] = st.session_state["coklu_api_anahtarlari"][ilk_kod]
                st.session_state["acik_kaynak_ai_aktif"] = True

            # Yerel PC'de .streamlit/secrets.toml dosyasına da güvenli kaydet
            if not _bulut_ortami_mi() and st.session_state["coklu_api_anahtarlari"]:
                try:
                    env_ad_map = {k: v[0] for k, v in _BULUT_ENV_HARITASI}
                    sec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit")
                    os.makedirs(sec_dir, exist_ok=True)
                    sec_file = os.path.join(sec_dir, "secrets.toml")
                    mevcut_satirlar = []
                    if os.path.exists(sec_file):
                        with open(sec_file, "r", encoding="utf-8") as sf:
                            mevcut_satirlar = sf.readlines()
                    guncel_anahtar_adlari = {env_ad_map[k] for k in st.session_state["coklu_api_anahtarlari"] if k in env_ad_map}
                    temiz_satirlar = [
                        s for s in mevcut_satirlar
                        if not any(s.strip().startswith(f"{ea} ") or s.strip().startswith(f"{ea}=") for ea in guncel_anahtar_adlari)
                    ]
                    for k, v in st.session_state["coklu_api_anahtarlari"].items():
                        if k in env_ad_map:
                            temiz_satirlar.append(f'{env_ad_map[k]} = "{v}"\n')
                    with open(sec_file, "w", encoding="utf-8") as sf:
                        sf.writelines(temiz_satirlar)
                except Exception:
                    pass

            st.success(f"✅ Toplam **{kaydedilen} bulut API** aynı anda aktif edildi! Şimdi '📡 Canlı API Bağlantı Testi' sekmesinden test edebilirsin.")
            st.rerun()

    with tab_deepseek:
        st.markdown("### 🐋 DeepSeek V4.1-Flash & V4-Pro Özel Merkezi")
        st.markdown(
            "- **Resmi Uç Nokta:** `https://api.deepseek.com/chat/completions`\n"
            "- **Aktif Modeller:** `deepseek-flash` (DeepSeek-V4.1-Flash, 1M bağlam, hızlı & çoklu ortam) ve yedek `deepseek-v4-pro` (derin muhakeme)\n"
            "- **Sohbette Doğrudan Çağırma:** Sohbete **`deepseek: ...`** yazarak herhangi bir soruyu doğrudan DeepSeek'e yönlendirebilirsin."
        )
        ds_mevcut = st.session_state["coklu_api_anahtarlari"].get("deepseek_cloud", "")
        ds_girdi = st.text_input(
            "🔑 DeepSeek API Anahtarı (platform.deepseek.com):",
            value=ds_mevcut,
            type="password",
            placeholder="sk-...",
            key="deepseek_ozel_anahtar_inp",
        )
        ds_col1, ds_col2 = st.columns(2)
        with ds_col1:
            if st.button("💾 DeepSeek Anahtarını Bağla & Birincil Yap", use_container_width=True, key="ds_bagla_btn"):
                if ds_girdi.strip():
                    st.session_state["coklu_api_anahtarlari"]["deepseek_cloud"] = ds_girdi.strip()
                    st.session_state["acik_kaynak_saglayici"] = "deepseek_cloud"
                    st.session_state["acik_kaynak_api_key"] = ds_girdi.strip()
                    st.session_state["acik_kaynak_ai_aktif"] = True
                    st.success("✅ DeepSeek bağlandı ve birincil motor yapıldı!")
                    st.rerun()
                else:
                    st.warning("Lütfen geçerli bir DeepSeek API anahtarı gir.")
        with ds_col2:
            ds_test_soru = st.text_input("Hızlı DeepSeek Test Sorusu:", value="Merhaba, kendini 1 cümleyle tanıt.", key="ds_test_soru")
        if st.button("🧪 DeepSeek'i Canlı Test Et", use_container_width=True, key="ds_canli_test_btn"):
            ds_key = ds_girdi.strip() or st.session_state["coklu_api_anahtarlari"].get("deepseek_cloud", "") or os.environ.get("DEEPSEEK_API_KEY", "")
            if not ds_key:
                st.error("❌ DeepSeek API anahtarı girilmemiş. Üstteki kutuya anahtarını girip tekrar dene.")
            else:
                with st.spinner("🐋 DeepSeek V4.1-Flash yanıt üretiyor..."):
                    ds_yanit, ds_etiket = _bulut_anahtarli_ai_cagir(
                        ds_test_soru, "deepseek_cloud", ds_key,
                        "Sen AREX AI Studio asistanısın. Kısa ve temiz Türkçe cevap ver.", [],
                    )
                if ds_yanit:
                    st.success(f"✅ **Bağlantı Başarılı ({ds_etiket}):**\n\n{ds_yanit}")
                else:
                    st.error(f"❌ DeepSeek yanıt vermedi: {_SON_AI_HATA_KAYDI.get('deepseek_cloud', 'Anahtar veya bakiye/bağlantı kontrol et')}")

    with tab_canli:
        st.markdown("### 📡 Canlı API Bağlantı & Gecikme Monitörü")
        st.caption("Bağlı tüm bulut AI anahtarlarını (Groq, DeepSeek, Gemini, OpenRouter vb.) ve açık kaynak veri servislerini paralel olarak test eder.")
        if st.button("🚀 Tüm Canlı API Bağlantılarını Şimdi Test Et", use_container_width=True, key="tum_canli_api_test_btn"):
            with st.spinner("📡 Tüm bağlı API'ler ve açık kaynak servisler canlı test ediliyor..."):
                tani_list = canli_baglanti_doktoru_calistir()
            basarili_say = sum(1 for _, ok, _ in tani_list if ok)
            st.progress(basarili_say / max(1, len(tani_list)), text=f"Canlı Sağlık Skoru: {basarili_say}/{len(tani_list)} Servis Aktif")
            for t_ad, t_ok, t_msj in tani_list:
                if t_ok:
                    st.success(f"✅ **{t_ad}:** {t_msj}")
                else:
                    st.error(f"❌ **{t_ad}:** {t_msj}")
