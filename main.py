# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v13.0 — SADELEŞTİRİLMİŞ & BİRLEŞTİRİLMİŞ ANA KONTROL MERKEZİ (main.py)
Yenilikler (v13.0):
  • Doğrudan Sohbet Botundan Wikipedia Araştırması ("🔍 Araştırılıyor, Wikipedia'ya gidiliyor...")
  • Karmaşık 9 Menü Yerine Birbirinin İçine Katılmış 5 Düzenli Merkez
  • Tam Genişlikli Ferah Sohbet Ekranı (Gereksiz Yandaki Kalabalık Kutular Birleştirildi)
  • Açık Kaynak Yapay Zeka Siteleri Entegrasyonu (Pollinations Anahtarsız, Groq Llama 3.3 70B,
    Hugging Face Qwen 2.5 72B, OpenRouter DeepSeek-R1 ve Yerel Ollama)
  • Tek Dosya (main.py) Yapıştırıldığında 10 Modülü Otomatik Kuran Mekanizma
Çalıştırma Komutu: streamlit run main.py
==============================================================================
"""
from datetime import datetime
import importlib.util
import json
import os
import re
import sys
import time

# 🇹🇷 Saat dilimini sabitle: Streamlit Cloud sunucuları UTC'de çalışır; bu satır olmadan mesaj saatleri,
# hatırlatıcılar, çalışma kayıtları ve yedek adları 3 saat geri (gece yarısı → önceki gün) olurdu.
os.environ["TZ"] = "Europe/Istanbul"
if hasattr(time, "tzset"):
    time.tzset()

import streamlit as st

# 1. PROJE DİZİNİNİ EN YÜKSEK ÖNCELİKLE BAĞLA
PROJE_KOK_DIZINI = os.path.dirname(os.path.abspath(__file__))
for _ana in [PROJE_KOK_DIZINI]:
    for _kok, _altlar, _ in os.walk(_ana):
        _altlar[:] = [d for d in _altlar if not d.startswith(".") and d not in ("__pycache__", "venv", ".venv")]
        if _kok not in sys.path:
            sys.path.append(_kok)
if PROJE_KOK_DIZINI in sys.path:
    sys.path.remove(PROJE_KOK_DIZINI)
sys.path.insert(0, PROJE_KOK_DIZINI)

# 2. OTOMATİK KOYU LACİVERT STREAMLIT TEMA KİLİDİ (.streamlit/config.toml + Runtime)
_STREAMLIT_TEMA_TOML = """[theme]
base = "dark"
primaryColor = "#38bdf8"
backgroundColor = "#03091a"
secondaryBackgroundColor = "#07142e"
textColor = "#ffffff"

[server]
enableStaticServing = true

[browser]
gatherUsageStats = false
"""
for _hedef_kok in {PROJE_KOK_DIZINI, os.getcwd()}:
    try:
        _st_klasor = os.path.join(_hedef_kok, ".streamlit")
        os.makedirs(_st_klasor, exist_ok=True)
        with open(os.path.join(_st_klasor, "config.toml"), "w", encoding="utf-8") as _tf:
            _tf.write(_STREAMLIT_TEMA_TOML)
    except Exception:
        pass

try:
    st._config.set_option("theme.base", "dark")
    st._config.set_option("theme.primaryColor", "#38bdf8")
    st._config.set_option("theme.backgroundColor", "#03091a")
    st._config.set_option("theme.secondaryBackgroundColor", "#07142e")
    st._config.set_option("theme.textColor", "#ffffff")
except Exception:
    pass

# 3. SAYFA YAPILANDIRMASI (İlk Streamlit Komutu)
st.set_page_config(
    page_title="AREX AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",  # telefonda kapalı, bilgisayarda açık başlar
)

# Mobil premium arayüz + açılış kapağı + PWA (Modül 15)
try:
    import modul_17_medya_ve_grafik as m17_medya
except Exception:
    m17_medya = None

try:
    import modul_19_cevap_varyantlari as m19_varyant
except Exception:
    m19_varyant = None

try:
    import modul_15_mobil_arayuz as m15_mobil
    m15_mobil.kapak_ekrani_goster()
    m15_mobil.pwa_baglantilarini_ekle()
except Exception:
    m15_mobil = None

# 4. MODÜL BAĞLAYICI
# (Eski sürümdeki "gömülü modül arşivi" kaldırıldı: bir modülde hata olunca güncel dosyayı aylar önceki
#  sürümle SESSİZCE eziyordu. Modüller artık yalnızca git'teki güncel dosyalardan yüklenir.)
try:
    import modul_25_ai_cekirdek as m25_ai
    m25_ai.anahtarlari_yukle()  # ~/.arex/anahtarlar.json → ortam değişkenleri (kalıcı anahtar kasası)
except Exception:
    m25_ai = None


def modulu_bagla(modul_adi: str):
    """Modülü proje kökünden yükler; hata olursa gerçek hatayı yükseltir (gizlemez, dosyayı ezmez)."""
    if modul_adi in sys.modules and getattr(sys.modules[modul_adi], "__file__", None):
        return sys.modules[modul_adi]
    ana_yol = os.path.join(PROJE_KOK_DIZINI, f"{modul_adi}.py")
    spec = importlib.util.spec_from_file_location(modul_adi, ana_yol)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modul_adi] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(modul_adi, None)
        raise
    return mod


m1_arayuz = modulu_bagla("modul_1_arayuz_ve_tema")
m2_alimler = modulu_bagla("modul_2_islam_alimleri")
m3_veri = modulu_bagla("modul_3_veri_ve_kisiler")
m4_matematik = modulu_bagla("modul_4_matematik_motoru")
m5_dil = modulu_bagla("modul_5_dil_ve_cevirmeli_kartlar")
m6_muhendislik = modulu_bagla("modul_6_iha_ve_bebek_arabasi")
m7_ders = modulu_bagla("modul_7_ders_ve_notlar")
m8_zeka = modulu_bagla("modul_8_zeka_ve_hibrit_ai")
m9_ollama_tdk = modulu_bagla("modul_9_ollama_ve_tdk")
m10_wikipedia = modulu_bagla("modul_10_wikipedia")
m11_guvenlik = modulu_bagla("modul_11_guvenlik_kalkani")
m12_fiyat = modulu_bagla("modul_12_fiyat_motoru")
m13_dunya = modulu_bagla("modul_13_acik_kaynak_bilgi_agi")

MODUL_DURUM_LISTESI = [
    ("Modül 1", "modul_1_arayuz_ve_tema.py", "Koyu Lacivert Tema & 3D Flip Card CSS", m1_arayuz is not None),
    ("Modül 2", "modul_2_islam_alimleri.py", "Canlı Türkiye Saati (UTC+3), Pomodoro & Geri Sayım Sayacı", m2_alimler is not None),
    ("Modül 3", "modul_3_veri_ve_kisiler.py", "Ahmet Profili, Kişiler ('Kim') & JSON Hafıza", m3_veri is not None),
    ("Modül 4", "modul_4_matematik_motoru.py", "Matematik, Geometri & 154 Çözümlü Soru", m4_matematik is not None),
    ("Modül 5", "modul_5_dil_ve_cevirmeli_kartlar.py", "A1-A2 3D Çevirmeli Kartlar (EN-AR-BN) & Ses/STT", m5_dil is not None),
    ("Modül 6", "modul_6_iha_ve_bebek_arabasi.py", "TEKNOFEST İHA & Akıllı Bebek Arabası Hesaplayıcı", m6_muhendislik is not None),
    ("Modül 7", "modul_7_ders_ve_notlar.py", "9. Sınıf Ders Özetleri, Notlar & Soru Takibi", m7_ders is not None),
    ("Modül 8", "modul_8_zeka_ve_hibrit_ai.py", "530.000+ Kalıp, 5N1K, Wikipedia & Açık Kaynak AI Motoru", m8_zeka is not None),
    ("Modül 9", "modul_9_ollama_ve_tdk.py", "Açık Kaynak AI Siteleri, Yerel Ollama & TDK Sözlük", m9_ollama_tdk is not None),
    ("Modül 10", "modul_10_wikipedia.py", "Doğrudan Sohbet Entegreli Wikipedia Ansiklopedisi", m10_wikipedia is not None),
    ("Modül 11", "modul_11_guvenlik_kalkani.py", "Sunucu Koruma, Rate Limit (Fazla Limit) & Bug Kalkanı", m11_guvenlik is not None),
    ("Modül 12", "modul_12_fiyat_motoru.py", "Epey, Cimri, Akakçe Fiyat & OpenStreetMap Adres Motoru", m12_fiyat is not None),
    ("Modül 13", "modul_13_acik_kaynak_bilgi_agi.py", "81 İl, 195+ Ülke (REST Countries), Tarif (TheMealDB), Hava (Open-Meteo)", m13_dunya is not None),
]



OTURUMLAR_DOSYASI = os.path.join(PROJE_KOK_DIZINI, "arex_sohbet_oturumlari.json")


def sohbet_oturumlarini_yukle() -> dict:
    try:
        if os.path.exists(OTURUMLAR_DOSYASI):
            with open(OTURUMLAR_DOSYASI, "r", encoding="utf-8") as f:
                veri = json.load(f)
            if isinstance(veri, dict):
                return veri
    except Exception:
        pass
    return {}


def sohbet_oturumlarini_kaydet(oturumlar: dict):
    try:
        with open(OTURUMLAR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(oturumlar, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def yeni_temiz_sohbet_baslat():
    """Sayfa açıldığında veya 'Yeni Sohbet'e basıldığında tertemiz, hızlı bir oturum açar."""
    simdi = m2_alimler.turkiye_saati_al()
    yeni_id = f"sohbet_{int(time.time() * 1000)}"
    st.session_state["aktif_sohbet_id"] = yeni_id
    st.session_state["aktif_konu"] = ""
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Merhaba Ahmet! ⚡ Yeni bir sohbete başladık. Şehirler, ülkeler, yemek tarifleri, adres, fiyat, matematik veya sohbet için doğrudan yazabilirsin.",
            "zaman": simdi.strftime("%H:%M:%S"),
            "tarih": simdi.strftime("%Y-%m-%d"),
            "etiket": "Yeni Sohbet",
        }
    ]


def aktif_sohbeti_oturuma_kaydet():
    """Aktif sohbeti başlığıyla birlikte sohbet geçmişi arşivine kaydeder."""
    oturum_id = st.session_state.get("aktif_sohbet_id")
    mesajlar = st.session_state.get("messages", [])
    kullanici_msj = [m["content"] for m in mesajlar if m.get("role") == "user"]
    if not oturum_id or not kullanici_msj:
        return
    oturumlar = sohbet_oturumlarini_yukle()
    ilk_baslik = kullanici_msj[0].strip()[:34]
    oturumlar[oturum_id] = {
        "baslik": ilk_baslik + ("..." if len(kullanici_msj[0]) > 34 else ""),
        "tarih": m2_alimler.turkiye_saati_al().strftime("%d.%m %H:%M"),
        "mesajlar": mesajlar[-80:],
    }
    # En son 40 sohbet oturumunu sakla
    if len(oturumlar) > 40:
        for eski_k in list(oturumlar.keys())[:-40]:
            del oturumlar[eski_k]
    sohbet_oturumlarini_kaydet(oturumlar)


def oturum_durumunu_hazirla():
    varsayilanlar = {
        "messages": None,
        "aktif_sohbet_id": "",
        "aktif_konu": "",
        "tum_mesajlari_goster": False,
        "sessiz_mod": False,
        "ses_aktif": True,
        "pygame_aktif": False,
        "ses_cinsiyet": "Erkek",
        "secili_tema": "Derin Lacivert (Klasik Ar)",
        "quiz_soru": None,
        "quiz_puan": 0,
        "son_ses_bayt": None,
        "acik_kaynak_ai_aktif": True,
        "sohbet_oncelik_modu": "ai_once",
        "acik_kaynak_saglayici": (m9_ollama_tdk._buluttan_anahtar_bul()[0] or "pollinations_free"),
        "acik_kaynak_api_key": (m9_ollama_tdk._buluttan_anahtar_bul()[1] or ""),
        "ortak_akil_aktif": False,
        "cocuk_dostu_mod": False,
        "ollama_aktif": False,
        "ollama_secili_model": "llama3.2",
        "ollama_url": "http://127.0.0.1:11434",
        "tdk_aktif": True,
        "wikipedia_aktif": True,
        "gemini_api_key": "",
        "son_mikrofon_hash": None,
        "dil_quiz_indeks": 0,
        "dil_quiz_puan": 0,
        "aktif_flip_indeks": 0,
        "kart_ters_mi": False,
        "ogrenilen_kart_idleri": [],
        "guvenlik_sadece_yerel": False,
        "guvenlik_izinli_hostlar": "",
        "guvenlik_pin_aktif": False,
        "guvenlik_pin_ozeti": "",
        "guvenlik_pin_dogrulandi": False,
        "guvenlik_dakika_limit": 120,
        "guvenlik_patlama_limit": 15,
        "guvenlik_bekleme_sn": 5,
        "guvenlik_oturum_id": f"ahmet_{int(time.time())}",
    }
    for k, v in varsayilanlar.items():
        if k not in st.session_state:
            st.session_state[k] = v
    # Eski açık sekmelerde kalan düşük limitleri otomatik yükselt (3-5 soruda takılmayı önler)
    if int(st.session_state.get("guvenlik_dakika_limit", 120)) < 60:
        st.session_state["guvenlik_dakika_limit"] = 120
    if int(st.session_state.get("guvenlik_patlama_limit", 15)) < 10:
        st.session_state["guvenlik_patlama_limit"] = 15
    if not st.session_state.get("messages"):
        yeni_temiz_sohbet_baslat()


def _sohbeti_markdowna_cevir(mesajlar) -> str:
    """Aktif sohbeti okunabilir Markdown metnine çevirir (telefonda paylaşmak / ders notu olarak saklamak için)."""
    satirlar = [f"# AREX AI Sohbeti — {datetime.now():%d.%m.%Y %H:%M}", ""]
    for m in mesajlar or []:
        icerik = re.sub(r"<!--AREX_SVG:[A-Za-z0-9+/=]+-->", "", str(m.get("content", ""))).strip()
        if not icerik:
            continue
        satirlar.append("**🧑 Sen:**" if m.get("role") == "user" else "**⚡ AREX:**")
        satirlar += [icerik, "", "---", ""]
    return "\n".join(satirlar)


def _sesi_yaziya_dok(ses_bayt: bytes):
    """Önce Groq Whisper (çok daha isabetli Türkçe), olmazsa Google ücretsiz tanıma."""
    groq_key = ""
    try:
        groq_key = m9_ollama_tdk._saglayici_icin_anahtar_bul("groq_cloud", "")
    except Exception:
        pass
    if m17_medya is not None and groq_key:
        metin, _hata = m17_medya.sesi_metne_cevir(ses_bayt, groq_key, dil="tr")
        if metin:
            return metin, None
    return m5_dil.mikrofon_sesini_metne_cevir(ses_bayt, dil="tr-TR")


def _dogrudan_sohbete_ekle(kullanici_metni: str, cevap: str, etiket: str):
    """Fotoğraf gibi sohbet motoru dışı yanıtları geçmişe ekler."""
    simdi = m2_alimler.turkiye_saati_al()
    ortak = {"zaman": simdi.strftime("%H:%M:%S"), "tarih": simdi.strftime("%Y-%m-%d"), "etiket": etiket}
    st.session_state.messages.append({"role": "user", "content": kullanici_metni, **ortak})
    st.session_state.messages.append({"role": "assistant", "content": cevap, **ortak})
    aktif_sohbeti_oturuma_kaydet()


def mesaji_isle_ve_arastir(girdi_metni: str, hedef_dil: str):
    """
    Kullanıcı sohbette bir soru sorduğunda:
    1. Eğer konu ansiklopedik bir araştırma ise ekranda canlı olarak
       '🔍 Araştırılıyor, Wikipedia'ya gidiliyor...' durum kutusunu gösterir.
    2. Yanıtı üretir, sohbet geçmişine kaydeder ve döndürür.
    """
    simdi = m2_alimler.turkiye_saati_al()
    su_an = simdi.strftime("%H:%M:%S")
    bugun_str = simdi.strftime("%Y-%m-%d")

    # 1. Fazla İstek Limiti (Rate Limit) Kontrolü
    rl_ok, rl_uyari, _ = m11_guvenlik.rate_limit_kontrol(
        oturum_anahtari=st.session_state.get("guvenlik_oturum_id", "varsayilan"),
        dakikalik_limit=int(st.session_state.get("guvenlik_dakika_limit", 120)),
        ani_patlama_limit=int(st.session_state.get("guvenlik_patlama_limit", 15)),
        bekleme_saniyesi=int(st.session_state.get("guvenlik_bekleme_sn", 5)),
    )
    if not rl_ok:
        st.session_state.messages.append(
            {"role": "assistant", "content": rl_uyari, "zaman": su_an, "tarih": bugun_str, "etiket": "⏳ Rate Limit"}
        )
        aktif_sohbeti_oturuma_kaydet()
        return rl_uyari, hedef_dil

    # 2. Girdi Bug & Güvenlik Taraması
    g_ok, temiz_girdi, g_uyari = m11_guvenlik.girdi_guvenlik_ve_bug_kontrol(girdi_metni)
    if not g_ok:
        st.session_state.messages.append(
            {"role": "assistant", "content": g_uyari, "zaman": su_an, "tarih": bugun_str, "etiket": "🛡️ Güvenlik Kalkanı"}
        )
        aktif_sohbeti_oturuma_kaydet()
        return g_uyari, hedef_dil
    girdi_metni = temiz_girdi

    # 🌍 Kullanıcı başka dilde yazdıysa / çeviri ya da yabancı dilde içerik istediyse Türkçe kilidi bu istek için kapalı
    try:
        import modul_28_kisisel_hafiza as _m28
        st.session_state["_yabanci_dil_serbest"] = _m28.yabanci_dil_serbest_mi(girdi_metni, hedef_dil)
        _ogrenilen = _m28.sohbetten_ogren(girdi_metni)
        if _ogrenilen:
            st.toast(f"🧠 Hafızama ekledim: {_ogrenilen}", icon="💙")
    except Exception:
        st.session_state["_yabanci_dil_serbest"] = hedef_dil != "tr"

    otonom_mi, plan_ozeti = m8_zeka.wikipedia_arastirma_gerekiyor_mu(girdi_metni)
    if otonom_mi and hasattr(st, "status"):
        with st.status("🧠 AREX Otonom Ajanı kaynaklara gidip bağlam kuruyor...", expanded=True) as durum:
            st.write(f"🧭 **Otonom Plan:** {plan_ozeti}")
            cevap, dil_kodu, islem_etiketi = m8_zeka.akilli_yanit_uret(girdi_metni, hedef_dil=hedef_dil)
            st.write("✅ Veriler toplandı ve en mantıklı yanıt sentezlendi.")
            durum.update(label=f"✅ Tamamlandı — {islem_etiketi}", state="complete", expanded=False)
    else:
        with st.spinner("⚡ AREX düşünüyor ve yanıt hazırlıyor..."):
            cevap, dil_kodu, islem_etiketi = m8_zeka.akilli_yanit_uret(girdi_metni, hedef_dil=hedef_dil)

    _yanit_svg = None
    if m17_medya is not None:
        cevap, _yanit_svg = m17_medya.svg_ayikla(cevap)
    if m19_varyant is not None:  # yerel cevaplarda olasılıklı çeşitlilik (AI cevaplarına dokunmaz)
        cevap = m19_varyant.cevabi_cesitlendir(cevap, islem_etiketi)
    st.session_state.messages.append(
        {"role": "user", "content": girdi_metni, "zaman": su_an, "tarih": bugun_str, "etiket": islem_etiketi}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": cevap, "zaman": su_an, "tarih": bugun_str, "etiket": islem_etiketi,
         **({"svg": _yanit_svg} if _yanit_svg else {})}
    )
    aktif_sohbeti_oturuma_kaydet()
    return cevap, dil_kodu


def _canli_bolumu_goster():
    """Gemini Live: gerçek zamanlı sesli + görüntülü sohbet (geçici token; asıl anahtar tarayıcıya gitmez)."""
    import streamlit.components.v1 as _bilesen
    st.markdown("### 🎙️ Canlı Sohbet — Ses & Kamera")
    st.caption("Gemini Live ile gerçek zamanlı, doğal sesli konuşma. Sözünü kesebilir, kamerayı açıp gösterebilir, "
               "modu (asistan, çocuk arkadaşı, masalcı, tercüman, dil pratiği, kamera analizi) anında değiştirebilirsin.")
    if m25_ai is None or not m25_ai.anahtar("GEMINI_API_KEY"):
        st.warning("Canlı sohbet için Gemini anahtarı gerekli → yan menü 🔑 API Anahtarlarım.")
        return
    c1, c2 = st.columns(2)
    _mod = c1.selectbox("Başlangıç modu", ["asistan", "cocuk", "masal", "ceviri", "dil", "analiz"], key="canli_mod",
                        format_func=lambda k: {"asistan": "🤖 Asistan", "cocuk": "🧸 Çocuk Arkadaşı", "masal": "📖 Canlı Masalcı",
                                               "ceviri": "🌐 Canlı Tercüman", "dil": "🗣️ Dil Pratiği",
                                               "analiz": "🔬 Kamera Analizi"}[k])
    _dil = c2.selectbox("Dil", ["tr", "en", "bn", "ar", "ru", "de", "fr", "es", "az", "ur", "hi", "zh", "ja", "fa"],
                        key="canli_dil")
    if st.button("🔄 Yeni canlı oturum hazırla", key="canli_yenile") or "canli_html" not in st.session_state \
            or st.session_state.get("canli_html_ayar") != (_mod, _dil):
        _profil, _ad = "", ""
        try:
            import modul_28_kisisel_hafiza as _m28
            _profil, _ad = _m28.profil_ozeti(), _m28.profil_oku().get("ad", "")
        except Exception:
            pass
        st.session_state["canli_html"] = m25_ai.canli_sayfa_html(
            mod=_mod, dil=_dil, yas=st.session_state.get("cocuk_yas_grubu", "7-9"), profil=_profil, ad=_ad)
        st.session_state["canli_html_ayar"] = (_mod, _dil)
    _bilesen.html(st.session_state["canli_html"], height=720, scrolling=False)
    st.caption("🔐 Tarayıcıya yalnızca 30 dakikalık geçici bir anahtar gönderilir. Telefonda mikrofon için https "
               "(Streamlit Cloud) veya AREX APK'sı gerekir; yerel ağ adresinde (http) tarayıcı mikrofonu engeller.")


def _kucuk_resim_b64(veri: bytes, kenar: int = 360) -> str:
    """Sohbet balonunda gösterilecek küçük JPEG önizleme (data URI)."""
    try:
        import io
        from PIL import Image, ImageOps
        g = ImageOps.exif_transpose(Image.open(io.BytesIO(veri))).convert("RGB")
        g.thumbnail((kenar, kenar))
        tampon = io.BytesIO()
        g.save(tampon, "JPEG", quality=72)
        import base64 as _b64
        return "data:image/jpeg;base64," + _b64.b64encode(tampon.getvalue()).decode()
    except Exception:
        return ""


def medyali_mesaji_isle(metin: str, dosyalar: list, hedef_dil: str):
    """Sohbet kutusuna eklenen fotoğraf/video: Gemini ile sohbet bağlamında analiz edilir."""
    import modul_27_gorsel_analiz as _m27
    simdi = m2_alimler.turkiye_saati_al()
    ortak = {"zaman": simdi.strftime("%H:%M:%S"), "tarih": simdi.strftime("%Y-%m-%d")}
    dosya = dosyalar[0]
    veri, ad = dosya.getvalue(), dosya.name
    video_mu = (getattr(dosya, "type", "") or "").startswith("video") or ad.lower().endswith((".mp4", ".mov", ".webm", ".3gp"))
    turler = _m27.analiz_turu_tahmin_et(metin, video_mu)
    if not turler and not metin.strip():
        turler = ["video_genel"] if video_mu else ["genel"]
    dil_ad = {"tr": "Türkçe", "en": "English", "ar": "Arapça", "bn": "Bengalce", "ru": "Rusça"}.get(hedef_dil, "Türkçe")
    if m25_ai is not None:
        _tahmin = m25_ai.yazidan_dil_tahmin(metin)
        if _tahmin and _tahmin != "tr":
            dil_ad = m25_ai.DIL_ADLARI.get(_tahmin, dil_ad)
    gecmis = [{"role": m["role"], "content": str(m.get("content", ""))[:1200]}
              for m in st.session_state.messages[-6:] if m.get("role") in ("user", "assistant")]
    with st.spinner("🔬 " + ("Video izleniyor ve analiz ediliyor… (20-60 sn)" if video_mu else "Fotoğraf inceleniyor…")):
        cevap, etiket = _m27.analiz_yap(veri, ad, turler, metin, dil_ad, gecmis=gecmis)
    kullanici = {"role": "user", "content": (metin.strip() or ("🎬 Bu videoyu analiz et" if video_mu else "📸 Bu fotoğrafı analiz et")),
                 "etiket": "🎬 Video" if video_mu else "📸 Fotoğraf", **ortak}
    if not video_mu:
        _kucuk = _kucuk_resim_b64(veri)
        if _kucuk:
            kullanici["gorsel"] = _kucuk
    else:
        kullanici["content"] = f"🎬 *{ad}*\n\n" + kullanici["content"]
    st.session_state.messages.append(kullanici)
    st.session_state.messages.append({"role": "assistant", "content": cevap or f"⚠️ {etiket}",
                                      "etiket": f"🔬 {etiket}" if cevap else "⚠️ Görsel Analiz", **ortak})
    aktif_sohbeti_oturuma_kaydet()
    return cevap


def sistemi_baslat():
    oturum_durumunu_hazirla()
    m1_arayuz.arayuz_stillerini_yukle(st.session_state.secili_tema)
    if m15_mobil is not None:
        m15_mobil.mobil_stilleri_yukle()

    # 🔐 Zorunlu erişim şifresi: Secrets'ta AREX_ERISIM_SIFRESI tanımlıysa her ziyaretçiden istenir
    # (veriler, hatırlatıcılar ve yan menü dahil hiçbir şey şifre girilmeden yüklenmez)
    import modul_23_erisim as _m23_erisim
    _m23_erisim.erisim_kapisi()

    # ☁️ Kalıcı bulut deposu (Supabase tanımlıysa): ilk çalıştırmada veriler geri yüklenir (sayfa okumadan ÖNCE),
    # sonraki her çalıştırmada değişen dosyalar arka planda gönderilir. Tanımlı değilse hiçbir şey yapmaz.
    try:
        import modul_24_kalici_depo as _m24_depo
        _m24_depo.esitle(arka_planda=True)
    except Exception:
        _m24_depo = None

    # ⏰ Hatırlatıcı denetleyicisi: uygulama açıkken 30 sn'de bir zamanı gelenleri ekranda bildirir
    if hasattr(st, "fragment"):
        @st.fragment(run_every="30s")
        def _hatirlatici_denetle():
            try:
                import modul_18_calisma_kocu as _m18k
                for _h in _m18k.zamani_gelen_hatirlaticilar():
                    st.toast(f"⏰ **Hatırlatma:** {_h['baslik']}", icon="🔔")
            except Exception:
                pass
            try:
                if _m24_depo is not None:
                    _m24_depo.esitle(arka_planda=True)  # sohbet dışı değişiklikler de 30 sn içinde buluta gider
            except Exception:
                pass
        _hatirlatici_denetle()

    # GÜVENLİK KATMANI 0: Harici Siber Güvenlik Datası & FAIL-CLOSED Acil Kilit Kontrolü
    m11_guvenlik.siber_guvenlik_datasini_yukle()
    acil_kilit = m11_guvenlik.acil_kilit_durumu_oku()
    if acil_kilit.get("kilitli"):
        st.error("🔒 **Sistem Acil Koruma Kilidinde!** Verileriniz güvenli bir şekilde yedeklendi ve dış erişim kapatıldı.")
        with st.expander("🔑 Yönetici Kilidi Aç (Sadece Ahmet)", expanded=False):
            kurtarma_pin = st.text_input("Yönetici PIN Kodu:", type="password", key="acil_kurtarma_pin")
            if st.button("🔓 Kilidi Kaldır ve Sistemi Başlat", use_container_width=True):
                if m11_guvenlik.pin_dogrula(kurtarma_pin):
                    m11_guvenlik.acil_kilidi_kaldir()
                    st.rerun()
                else:
                    st.error("❌ Hatalı PIN.")
        st.stop()

    # GÜVENLİK KATMANI 1: Başka Sunuculardan Yetkisiz Giriş ve Zararlı Bot Engelleme
    ek_hostlar = [h.strip() for h in st.session_state.get("guvenlik_izinli_hostlar", "").split(",") if h.strip()]
    sunucu_ok, sunucu_msj, _ = m11_guvenlik.sunucu_giris_katmani_kontrol(
        ek_izinli_hostlar=ek_hostlar,
        sadece_yerel_ag=st.session_state.get("guvenlik_sadece_yerel", False),
    )
    if not sunucu_ok:
        st.error(sunucu_msj)
        st.stop()

    # GÜVENLİK KATMANI 2: İsteğe Bağlı Giriş PIN Kilidi
    if st.session_state.get("guvenlik_pin_aktif", False) and not st.session_state.get("guvenlik_pin_dogrulandi", False):
        st.markdown("## 🔒 AREX AI Studio — Güvenlik PIN Doğrulaması")
        girilen_pin = st.text_input("Erişim PIN Kodunu Girin:", type="password")
        if st.button("🔓 Kilidi Aç", use_container_width=True):
            if m11_guvenlik.pin_dogrula(girilen_pin):
                st.session_state.guvenlik_pin_dogrulandi = True
                st.rerun()
            else:
                m11_guvenlik.guvenlik_olayi_kaydet("Hatalı PIN Denemesi", "Giriş ekranında yanlış PIN girildi.", "UYARI")
                st.error("❌ Hatalı PIN kodu! Bu deneme güvenlik günlüğüne kaydedildi.")
        st.stop()
    m3_veri.json_veritabani_hazirla()
    kalip_havuzu = m8_zeka.kalip_havuzu_olustur()

    # ==========================================================================
    # SADELEŞTİRİLMİŞ YAN MENÜ (9 Dağınık Sekme -> 5 Birleştirilmiş Merkez)
    # ==========================================================================
    # ÜST HERO BANNER + ÜSTTE YAPIŞIK BÖLÜM ÇUBUĞU (mobilde yatay kaydırılır)
    m1_arayuz.hero_banner_goster(len(kalip_havuzu), st.session_state.secili_tema)
    _BOLUMLER = {
        "💬 Sohbet": "💬 Sohbet & Wikipedia Araştırma Botu",
        "🎙️ Canlı": "🎙️ Canlı Sohbet (Ses & Kamera)",
        "🧸 Çocuk": "🧸 Çocuk Dünyası",
        "🔬 Analiz": "🔬 Fotoğraf & Video Analizi",
        "📚 Eğitim": "📚 Eğitim, Matematik & Ansiklopedi",
        "🌐 Dil": "🌐 Dil & 3D Çevirmeli Kart Stüdyosu",
        "🍅 Odak": "🍅 Pomodoro & Canlı Çalışma Yeri",
        "🚀 Mühendislik": "🚀 Mühendislik (İHA / Bebek Arabası)",
        "🔌 API": "🔌 Çoklu API, DeepSeek & Canlı Bağlantı",
        "⚙️ Ayarlar": "⚙️ Açık Kaynak AI & Sistem Ayarları",
    }
    if m15_mobil is not None:
        bolum = m15_mobil.ust_gezinme(_BOLUMLER, "💬 Sohbet & Wikipedia Araştırma Botu")
    else:
        bolum = st.radio("Çalışma Alanı Seçin:", list(_BOLUMLER.values()), horizontal=True)

    with st.sidebar:
        st.markdown("### ⚡ AREX-1 Studio")
        st.caption("v14 • Mobil Premium • Mantık Motoru • 23 Modül")

        _aktif_sag_kod = st.session_state.get("acik_kaynak_saglayici", "pollinations_free")
        _aktif_anahtar_var = bool(st.session_state.get("acik_kaynak_api_key", "").strip())
        _rozet_metin = "⚡ GROQ GPT-OSS 120B + OTONOM AJAN" if (_aktif_sag_kod == "groq_cloud" and _aktif_anahtar_var) else "🧠 TAM OTONOM AJAN AKTİF"
        st.markdown(f'<span class="live-badge">{_rozet_metin}</span>', unsafe_allow_html=True)
        st.caption("Tuş seçmene gerek yok; AREX kendisi Wikipedia, Harita, Fiyat, TDK ve Çoklu AI arasında gidip gelerek en mantıklı yanıtı kurar.")
        st.markdown("#### 🔌 Zeka Kaynakları")
        st.session_state.wikipedia_aktif = st.toggle(
            "🌐 Sohbette Wikipedia Araştırma",
            value=st.session_state.wikipedia_aktif,
            help="Sohbette sorduğun konuları doğrudan Wikipedia'ya gidip araştırır.",
        )
        st.session_state.acik_kaynak_ai_aktif = st.toggle(
            "🤖 Açık Kaynak AI Sohbet Motoru",
            value=st.session_state.acik_kaynak_ai_aktif,
            help="Açık olduğunda normal sohbetlerde candan ve akıllı yanıtlar için Açık Kaynak AI (Pollinations, Groq, HuggingFace) birincil olarak çalışır.",
        )
        st.session_state.tdk_aktif = st.toggle(
            "📕 TDK Türkçe Sözlük",
            value=st.session_state.tdk_aktif,
            help="Kelime anlamlarını resmi TDK Sözlük'ten getirir.",
        )
        st.session_state.cocuk_dostu_mod = st.toggle(
            "🧒 Çocuk Dostu & İçten Sohbet Modu",
            value=st.session_state.cocuk_dostu_mod,
            help="Açık olduğunda küçük yaş gruplarıyla da neşeli, yumuşak, güvenli ve masal/bilmece destekli sohbet eder.",
        )
        if st.session_state.cocuk_dostu_mod:
            st.session_state["cocuk_yas_grubu"] = st.radio(
                "Yaş grubu", ["3-6", "7-9", "10-12"], horizontal=True,
                index=["3-6", "7-9", "10-12"].index(st.session_state.get("cocuk_yas_grubu", "7-9")),
                format_func=lambda k: {"3-6": "🐣 3-6", "7-9": "🦊 7-9", "10-12": "🚀 10-12"}[k])
            st.caption("Masal, macera, oyun ve sohbet arkadaşları için üstteki **🧸 Çocuk** bölümüne geç.")
        st.session_state.ortak_akil_aktif = st.toggle(
            "🧠 Ortak Akıl (Tüm AI'ları Birleştir)",
            value=st.session_state.ortak_akil_aktif,
            help="Açık olduğunda tek bir modele bağlı kalmaz: Yerel Ollama + Bulut Açık Kaynak AI'lardan paralel görüş alır, doğrulanmış açık kaynak verileriyle karşılaştırıp en mantıklı tek cevabı üretir.",
        )
        st.session_state.ollama_aktif = st.toggle(
            "🦙 Yerel Ollama Modeli",
            value=st.session_state.ollama_aktif,
            help="Açık olduğunda yerel Ollama, toplanan açık kaynak verileriyle (Wikipedia, TDK, Hava, Tarif, Piyasa) birlikte birincil yanıt verir. Kapalı olsa bile bulut kotası dolduğunda Ollama açıksa otomatik yedek olarak devreye girer.",
        )

        with st.expander("🎛️ Ses, Yanıt Dili & Tema Ayarları", expanded=False):
            st.session_state.sessiz_mod = st.toggle("🤫 Sessiz Mod", value=st.session_state.sessiz_mod)
            st.session_state.ses_aktif = st.toggle(
                "🔊 Sesli Okuma (Neural TTS)",
                value=st.session_state.ses_aktif,
                disabled=st.session_state.sessiz_mod,
            )
            st.session_state.ses_cinsiyet = st.selectbox(
                "🎙️ Ses Karakteri:",
                options=["Erkek", "Kadın"],
                format_func=lambda x: "👨 Ahmet Neural" if x == "Erkek" else "👩 Emel Neural",
            )
            _dil_kodlari = list(m5_dil.DESTEKLENEN_DILLER.keys())
            _tr_indeks = _dil_kodlari.index("tr") if "tr" in _dil_kodlari else 0
            sohbet_dili = st.selectbox(
                f"🌐 Yanıt Dili ({len(m5_dil.DESTEKLENEN_DILLER)} Dil — Varsayılan Türkçe):",
                options=_dil_kodlari,
                index=_tr_indeks,
                format_func=lambda x: m5_dil.DESTEKLENEN_DILLER[x],
            )
            tema_listesi = list(m1_arayuz.TEMA_PALETLERI.keys())
            if st.session_state.secili_tema not in tema_listesi:
                st.session_state.secili_tema = tema_listesi[0]
            secilen_tema = st.selectbox(
                "🎨 Tema Paleti:",
                options=tema_listesi,
                index=tema_listesi.index(st.session_state.secili_tema),
            )
            if secilen_tema != st.session_state.secili_tema:
                st.session_state.secili_tema = secilen_tema
                _yeni_p = m1_arayuz.tema_paleti_getir(secilen_tema)
                try:
                    st._config.set_option("theme.primaryColor", _yeni_p["accent_neon"])
                    st._config.set_option("theme.backgroundColor", _yeni_p["bg_primary"])
                    st._config.set_option("theme.secondaryBackgroundColor", _yeni_p["bg_secondary"])
                    st._config.set_option("theme.textColor", _yeni_p["text_main"])
                except Exception:
                    pass
                st.rerun()
            st.markdown(m1_arayuz.tema_renk_onizleme_karti_olustur(st.session_state.secili_tema), unsafe_allow_html=True)

        if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
            aktif_sohbeti_oturuma_kaydet()
            yeni_temiz_sohbet_baslat()
            st.rerun()

        if st.button("🩺 Bağlantı Doktoru (Canlı Test)", use_container_width=True, key="sidebar_baglanti_doktoru"):
            with st.spinner("🩺 Groq, Pollinations, Wikipedia ve Hava test ediliyor..."):
                _sb_tani = m9_ollama_tdk.canli_baglanti_doktoru_calistir()
            for _t_ad, _t_ok, _t_msj in _sb_tani:
                if _t_ok:
                    st.success(f"✅ **{_t_ad}:** {_t_msj}")
                else:
                    st.error(f"❌ **{_t_ad}:** {_t_msj}")

        try:
            _m23_erisim.korumasiz_bulut_uyarisi()
        except Exception:
            pass
        try:
            import modul_20_yedekleme as _m20_yedek
            _m20_yedek.yedekleme_paneli()
        except Exception:
            pass

        _anahtar_durumu = {ad: bool(m25_ai.anahtar(ad)) for ad in m25_ai.ANAHTAR_ADLARI} if m25_ai else {}
        with st.expander("🔑 API Anahtarlarım (kalıcı) " + "".join("🟢" if v else "⚪" for v in _anahtar_durumu.values()),
                         expanded=not any(_anahtar_durumu.values())):
            st.caption("Anahtarlar proje klasörünün DIŞINDA (~/.arex) saklanır; güncelleme, git veya yeniden "
                       "başlatma silemez. Boş bırakılan alan mevcut anahtarı değiştirmez.")
            with st.form("anahtar_kasasi_formu", clear_on_submit=True):
                _yeni_anahtarlar = {}
                for _ad, _etiket in (m25_ai.ANAHTAR_ADLARI.items() if m25_ai else []):
                    _mevcut = m25_ai.anahtar(_ad)
                    _yeni_anahtarlar[_ad] = st.text_input(
                        f"{_etiket} {'🟢 ' + m25_ai.maskele(_mevcut) if _mevcut else '⚪ yok'}",
                        type="password", key=f"kasa_{_ad}")
                if st.form_submit_button("💾 Kaydet", use_container_width=True, type="primary"):
                    _kaydedilen = [a for a, v in _yeni_anahtarlar.items() if v.strip() and m25_ai.anahtar_kaydet(a, v)]
                    if _kaydedilen:
                        st.session_state.pop("coklu_api_anahtarlari", None)
                        _kod, _key = m9_ollama_tdk._buluttan_anahtar_bul()
                        if _key:
                            st.session_state["acik_kaynak_saglayici"], st.session_state["acik_kaynak_api_key"] = _kod, _key
                        st.success(f"✅ Kalıcı olarak kaydedildi: {', '.join(m25_ai.ANAHTAR_ADLARI[a] for a in _kaydedilen)}")
                        st.rerun()

        with st.expander("💬 Sohbet Geçmişi (Kayıtlı Oturumlar)", expanded=False):
            kayitli_oturumlar = sohbet_oturumlarini_yukle()
            if kayitli_oturumlar:
                for o_id, o_veri in list(reversed(list(kayitli_oturumlar.items())))[:12]:
                    oc1, oc2 = st.columns([4, 1])
                    with oc1:
                        if st.button(f"💬 {o_veri.get('baslik', 'Sohbet')} ({o_veri.get('tarih', '')})", key=f"ac_{o_id}", use_container_width=True):
                            st.session_state.aktif_sohbet_id = o_id
                            st.session_state.messages = o_veri.get("mesajlar", [])
                            st.session_state["aktif_konu"] = ""
                            st.rerun()
                    with oc2:
                        if st.button("🗑️", key=f"sil_{o_id}", use_container_width=True):
                            del kayitli_oturumlar[o_id]
                            sohbet_oturumlarini_kaydet(kayitli_oturumlar)
                            st.rerun()
            else:
                st.caption("Henüz kayıtlı eski sohbet yok. Mesaj yazdığında otomatik kaydedilir.")

            st.download_button(
                label="📥 Aktif Sohbeti Yedekle (JSON)",
                data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                file_name=f"arex_sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
            )
            st.download_button(
                label="📄 Sohbeti Metin Olarak İndir (.md)",
                data=_sohbeti_markdowna_cevir(st.session_state.messages),
                file_name=f"arex_sohbet_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )


    # ==========================================================================
    # MERKEZ 1: TAM GENİŞLİKLİ SOHBET & DOĞRUDAN WIKIPEDIA ARAŞTIRMA BOTU
    # ==========================================================================
    if bolum == "💬 Sohbet & Wikipedia Araştırma Botu":
        # Ultra Sade 4 Kısayol (Göz Yormayan Tek Satır)
        hizli_girdi = None
        # Hızlı öneriler (telefonda 2'li ızgara): v14 yeni kaynaklarını tek dokunuşla tanıtır
        _HIZLI_ONERILER = [
            ("🌍 Son Depremler", "son depremler"),
            ("🌤️ Hava Durumu", "İstanbul hava durumu ve hava kalitesi"),
            ("📝 Mini Test", "bana 5 matematik sorusu sor"),
            ("📊 Haftalık Rapor", "bu hafta ne kadar çalıştım"),
            ("🎯 Panelim", "panelim"),
            ("🤝 Neler Yapabilirim?", "help"),
        ]
        with st.container(key="arex_hizli"):
            _h_sutunlar = st.columns(len(_HIZLI_ONERILER))
            for _h_sutun, (_h_etiket, _h_soru) in zip(_h_sutunlar, _HIZLI_ONERILER):
                if _h_sutun.button(_h_etiket, use_container_width=True, key=f"hizli_{_h_etiket}"):
                    hizli_girdi = _h_soru

        # Tam Genişlikli Ferah Sohbet Penceresi
        chat_penceresi = st.container(height=525, key="arex_sohbet")
        with chat_penceresi:
            tum_msj = st.session_state.messages
            if len(tum_msj) > 24 and not st.session_state.get("tum_mesajlari_goster", False):
                if st.button(f"📜 Daha eski {len(tum_msj) - 24} mesajı göster", use_container_width=True):
                    st.session_state.tum_mesajlari_goster = True
                    st.rerun()
                gorunecek_msj = tum_msj[-24:]
            else:
                gorunecek_msj = tum_msj
            _akis_bekliyor = bool(st.session_state.pop("yeni_yanit_akisi", False))
            _son_idx = len(gorunecek_msj) - 1
            for _m_idx, msg in enumerate(gorunecek_msj):
                avatar = "👤" if msg["role"] == "user" else "⚡"
                with st.chat_message(msg["role"], avatar=avatar):
                    if _akis_bekliyor and _m_idx == _son_idx and msg["role"] == "assistant" and hasattr(st, "write_stream"):
                        def _kelime_akisi(metin_str: str):
                            parcalar = re.findall(r"\S+\s*", metin_str)
                            # Uzun metinlerde 2-3 kelimelik paketlerle çok akıcı ve hızlı akış (1-2 sn)
                            adim = 2 if len(parcalar) <= 80 else (4 if len(parcalar) <= 200 else 8)
                            for i in range(0, len(parcalar), adim):
                                yield "".join(parcalar[i:i + adim])
                                time.sleep(0.008)
                        st.write_stream(_kelime_akisi(msg["content"]))
                    else:
                        st.markdown(msg["content"])
                    if msg.get("gorsel"):
                        st.markdown(f'<img class="arex-kucuk-gorsel" src="{msg["gorsel"]}" alt="eklenen fotoğraf">',
                                    unsafe_allow_html=True)
                    if msg.get("svg"):
                        st.markdown(msg["svg"], unsafe_allow_html=True)
                    saat_bilgi = msg.get("zaman", "")
                    etiket_bilgi = msg.get("etiket", "")
                    if saat_bilgi or etiket_bilgi:
                        st.caption(f"🕒 {saat_bilgi}  |  🏷️ {etiket_bilgi}")

        # 🎤 Sesli soru + 📸 Fotoğraftan soru (telefonda tek dokunuşla)
        with st.container(key="arex_medya"):
            with st.container():
                if hasattr(st, "audio_input"):
                    _kayit = st.audio_input("🎤 Sesli sor", label_visibility="collapsed", key="arex_ana_mikrofon")
                    if _kayit is not None:
                        _ses = _kayit.getvalue()
                        _ses_hash = hash(_ses)
                        if _ses_hash != st.session_state.get("son_mikrofon_hash"):
                            st.session_state["son_mikrofon_hash"] = _ses_hash
                            with st.spinner("🎤 Sesin yazıya dökülüyor..."):
                                _soz, _soz_hata = _sesi_yaziya_dok(_ses)
                            if _soz:
                                st.session_state["sesli_girdi"] = _soz
                            elif _soz_hata:
                                st.warning(_soz_hata)
            with st.container():
                with st.expander("🎧 Uzun Video / Ses Kaydını Yazıya Dök & Özetle", expanded=False):
                    _groq_key = ""
                    try:
                        _groq_key = m9_ollama_tdk._saglayici_icin_anahtar_bul("groq_cloud", "")
                    except Exception:
                        pass
                    _sek_video = st.container()
                    with _sek_video:
                        st.caption("Ders videosu, ses kaydı veya sesli not yükle; konuşmayı yazıya döküp özetleyeyim "
                                   "(Groq Whisper, ücretsiz). YouTube için bağlantıyı sohbete yapıştırman yeterli.")
                        _medya = st.file_uploader("Video / ses", type=["mp4", "mov", "m4a", "mp3", "wav", "ogg", "webm", "3gp", "aac", "flac"],
                                                  label_visibility="collapsed", key="arex_medya_dosya")
                        if _medya is not None and st.button("🎬 Özetle", type="primary", use_container_width=True,
                                                            key="arex_medya_ozetle"):
                            with st.spinner("🎧 Konuşma yazıya dökülüyor ve özetleniyor..."):
                                _m_cevap, _m_hata = m17_medya.medya_dosyasini_ozetle(_medya.getvalue(), _medya.name, _groq_key)
                            if _m_cevap:
                                _dogrudan_sohbete_ekle(f"🎬 Bu kaydı özetle: {_medya.name}", _m_cevap, "🎬 Video / Ses Özeti")
                                st.session_state["yeni_yanit_akisi"] = True
                                st.rerun()
                            else:
                                st.error(f"Özetlenemedi: {_m_hata}")

        # Sesli okuma: Önce metin ekranda ANINDA görünür, ses hemen ardından hazırlanır (arayüzü kilitlemez!)
        if st.session_state.get("bekleyen_ses"):
            _b_metin, _b_dil = st.session_state.pop("bekleyen_ses")
            if st.session_state.get("ses_aktif", True) and not st.session_state.get("sessiz_mod", False):
                m5_dil.sesli_soyle(_b_metin, dil=_b_dil, rerun_sonrasi=True)

        if st.session_state.get("son_ses_bayt"):
            st.audio(st.session_state.son_ses_bayt, format="audio/mp3", autoplay=True)
            st.session_state.son_ses_bayt = None

        try:
            prompt = st.chat_input("AREX'e bir şey sor… (📎 fotoğraf / video ekleyebilirsin)", accept_file=True,
                                   file_type=["png", "jpg", "jpeg", "webp", "heic", "mp4", "mov", "webm", "3gp"])
        except TypeError:  # çok eski Streamlit
            prompt = st.chat_input("AREX'e bir şey sor…")
        if prompt is not None and not isinstance(prompt, str):
            _p_metin = (getattr(prompt, "text", "") or "").strip()
            _p_dosyalar = list(getattr(prompt, "files", []) or [])
            if _p_dosyalar:
                medyali_mesaji_isle(_p_metin, _p_dosyalar, sohbet_dili)
                st.session_state["yeni_yanit_akisi"] = True
                st.rerun()
            prompt = _p_metin
        aktif_girdi = hizli_girdi or prompt or st.session_state.pop("sesli_girdi", None)
        if aktif_girdi is not None and aktif_girdi.strip() != "":
            cevap, dil_kodu = mesaji_isle_ve_arastir(aktif_girdi.strip(), sohbet_dili)
            st.session_state["yeni_yanit_akisi"] = True
            if st.session_state.get("ses_aktif", True) and not st.session_state.get("sessiz_mod", False):
                st.session_state["bekleyen_ses"] = (cevap, dil_kodu)
            st.rerun()

        # Tüm yardımcı araçlar ("Mikrofon", "Bana Öğret", "Açık Kaynak AI Seçimi") tek bir düzenli çekmecenin içinde!
        bekleyen_soru = st.session_state.get("bekleyen_ogret_sorusu", "")
        with st.expander(
            f"🛠️ Sohbet Araçları (🎙️ Sesli Sor • 🎓 Bana Öğret • 🤖 Açık Kaynak AI Seçimi){' — Yeni Soru: ' + bekleyen_soru if bekleyen_soru else ''}",
            expanded=bool(bekleyen_soru),
        ):
            arac_tab1, arac_tab2, arac_tab3 = st.tabs([
                "🎓 Bana Öğret (Kodsuz Hafıza)",
                "🎙️ Mikrofonla Sesli Sor",
                "🤖 Açık Kaynak AI Motoru Seç",
            ])
            with arac_tab1:
                with st.form("hizli_bana_ogret_formu", clear_on_submit=True):
                    c_og1, c_og2 = st.columns([1, 1.6])
                    with c_og1:
                        ogret_soru_input = st.text_input("Öğretilecek Soru veya Kelime:", value=bekleyen_soru)
                    with c_og2:
                        ogret_cevap_input = st.text_input("AREX'in Vereceği Doğru Cevap:")
                    if st.form_submit_button("💾 Hafızaya Kaydet (Kod Yazmadan Öğret)", use_container_width=True):
                        if ogret_soru_input.strip() and ogret_cevap_input.strip():
                            kat_kodu = f"ogrenilen_{int(time.time())}"
                            m3_veri.json_komut_ekle(kat_kodu, ogret_soru_input.strip(), ogret_cevap_input.strip())
                            st.session_state["bekleyen_ogret_sorusu"] = ""
                            simdi_z = m2_alimler.turkiye_saati_al()
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"✅ **Teşekkür ederim Ahmet, hemen öğrendim!** Artık **'{ogret_soru_input.strip()}'** dediğinde şu cevabı vereceğim:\n> {ogret_cevap_input.strip()}",
                                "zaman": simdi_z.strftime("%H:%M:%S"),
                                "tarih": simdi_z.strftime("%Y-%m-%d"),
                                "etiket": "Yeni Öğrenildi",
                            })
                            aktif_sohbeti_oturuma_kaydet()
                            st.rerun()

            with arac_tab2:
                if hasattr(st, "audio_input"):
                    mikrofon_kaydi = st.audio_input("🎙️ Mikrofona dokunup sorunu söyle:")
                    if mikrofon_kaydi is not None:
                        ses_bayt_m = mikrofon_kaydi.getvalue()
                        ses_hash = hash(ses_bayt_m)
                        if ses_hash != st.session_state.get("son_mikrofon_hash"):
                            st.session_state["son_mikrofon_hash"] = ses_hash
                            cozulen_metin, hata_m = m5_dil.mikrofon_sesini_metne_cevir(ses_bayt_m, dil="tr-TR")
                            if cozulen_metin:
                                cevap_m, dil_m = mesaji_isle_ve_arastir(cozulen_metin, sohbet_dili)
                                m5_dil.sesli_soyle(cevap_m, dil=dil_m, rerun_sonrasi=True)
                                st.rerun()
                            elif hata_m:
                                st.warning(hata_m)

            with arac_tab3:
                saglayicilar = m9_ollama_tdk.ACIK_KAYNAK_AI_SAGLAYICILARI
                sec_kod = st.selectbox(
                    "Sohbet Botunun Kullanacağı Açık Kaynak AI Sitesi:",
                    options=list(saglayicilar.keys()),
                    index=list(saglayicilar.keys()).index(st.session_state.get("acik_kaynak_saglayici", "pollinations_free")),
                    format_func=lambda k: saglayicilar[k]["ad"],
                )
                st.session_state.acik_kaynak_saglayici = sec_kod
                st.caption(f"ℹ️ {saglayicilar[sec_kod]['aciklama']}")
                if saglayicilar[sec_kod].get("anahtar_gerekli"):
                    st.session_state.acik_kaynak_api_key = st.text_input(
                        f"🔑 {saglayicilar[sec_kod]['ad']} API Anahtarı ({saglayicilar[sec_kod].get('site', '')}):",
                        value=st.session_state.get("acik_kaynak_api_key", ""),
                        type="password",
                    )
                _o_canli, _o_modeller = m9_ollama_tdk.ollama_hizli_durum_kontrol(st.session_state.get("ollama_url", "http://127.0.0.1:11434"))
                if _o_canli:
                    st.success(f"🦙 Yerel Ollama bağlı ve açık kaynak akışına entegre ({len(_o_modeller)} sohbet modeli hazır).")
                    _secenek_modeller = _o_modeller if _o_modeller else [st.session_state.get("ollama_secili_model", "llama3.2")]
                    _mevcut_m = st.session_state.get("ollama_secili_model", _secenek_modeller[0])
                    _idx_m = _secenek_modeller.index(_mevcut_m) if _mevcut_m in _secenek_modeller else 0
                    st.session_state.ollama_secili_model = st.selectbox(
                        "🦙 Ollama Sohbet Modeli:",
                        options=_secenek_modeller,
                        index=_idx_m,
                        key="hizli_ollama_model_sec",
                    )
                else:
                    if m9_ollama_tdk._bulut_ortami_mi():
                        st.info("☁️ Bulut Modu Aktif — Pollinations, Groq, Cerebras, NVIDIA NIM, GitHub Models, SambaNova & OpenRouter akışı hazır.")
                    else:
                        st.info("🦙 Yerel Ollama şu an kapalı — bulut açık kaynak AI aktif. Ollama'yı açtığında otomatik olarak akışa bağlanır.")
                if st.button("🩺 Canlı Bağlantı Doktorunu Çalıştır (Groq • Pollinations • Wikipedia • Hava)", use_container_width=True):
                    with st.spinner("🩺 Tüm canlı bağlantılar test ediliyor (3 sn)..."):
                        _tani_list = m9_ollama_tdk.canli_baglanti_doktoru_calistir()
                    for _t_ad, _t_ok, _t_msj in _tani_list:
                        if _t_ok:
                            st.success(f"✅ **{_t_ad}:** {_t_msj}")
                        else:
                            st.error(f"❌ **{_t_ad}:** {_t_msj}")

    # ==========================================================================
    # MERKEZ 2: EĞİTİM, MATEMATİK & ANSİKLOPEDİ (4 Bölüm Birbirinin İçine Katıldı!)
    # ==========================================================================
    elif bolum == "🎙️ Canlı Sohbet (Ses & Kamera)":
        _canli_bolumu_goster()

    elif bolum == "🧸 Çocuk Dünyası":
        import modul_26_cocuk_dunyasi as _m26
        _m26.cocuk_dunyasi_paneli()

    elif bolum == "🔬 Fotoğraf & Video Analizi":
        import modul_27_gorsel_analiz as _m27
        _m27.analiz_paneli(sohbete_ekle_fn=_dogrudan_sohbete_ekle)

    elif bolum == "🍅 Pomodoro & Canlı Çalışma Yeri":
        m7_ders.pomodoro_ve_canli_calisma_yeri_goster()

    elif bolum == "🔌 Çoklu API, DeepSeek & Canlı Bağlantı":
        m9_ollama_tdk.coklu_api_ve_canli_baglanti_paneli_goster()

    elif bolum == "📚 Eğitim, Matematik & Ansiklopedi":
        t_mat, t_ders, t_alim, t_wiki_tdk, t_fiyat = st.tabs([
            "🧮 Matematik & Fen Laboratuvarı",
            "📖 9. Sınıf Ders & Notlar",
            "⏰ Canlı Saat & Sayaç",
            "🌐 Wikipedia & 📕 TDK",
            "🏷️ Güncel Fiyat (Epey & Cimri)",
        ])
        with t_mat:
            m4_matematik.matematik_studyosu_goster(m5_dil.sesli_soyle)
        with t_ders:
            m7_ders.ders_ve_notlar_studyosu_goster(m5_dil.sesli_soyle)
        with t_alim:
            m2_alimler.zaman_ve_sayac_studyosu_goster()
        with t_wiki_tdk:
            alt_w, alt_t = st.tabs(["🌐 Wikipedia Ansiklopedi Ekranı", "📕 TDK Sözlük & Ollama Ekranı"])
            with alt_w:
                m10_wikipedia.wikipedia_studyosu_goster(m5_dil.sesli_soyle)
            with alt_t:
                m9_ollama_tdk.ollama_ve_tdk_studyosu_goster(m5_dil.sesli_soyle)
        with t_fiyat:
            m12_fiyat.fiyat_studyosu_goster()

    # ==========================================================================
    # MERKEZ 3: DİL & 3D ÇEVİRMELİ KART STÜDYOSU
    # ==========================================================================
    elif bolum == "🌐 Dil & 3D Çevirmeli Kart Stüdyosu":
        m5_dil.dil_ve_cevirmeli_kart_studyosu_goster()

    # ==========================================================================
    # MERKEZ 4: MÜHENDİSLİK (İHA & BEBEK ARABASI)
    # ==========================================================================
    elif bolum == "🚀 Mühendislik (İHA / Bebek Arabası)":
        m6_muhendislik.iha_ve_bebek_arabasi_studyosu_goster()

    # ==========================================================================
    # MERKEZ 5: AÇIK KAYNAK AI, JSON HAFIZA & SİSTEM AYARLARI (Birleştirilmiş Merkez)
    # ==========================================================================
    elif bolum == "⚙️ Açık Kaynak AI & Sistem Ayarları":
        ay_tab0, ay_tab1, ay_tab2, ay_tab3, ay_tab4 = st.tabs([
            "🧠 Beni Tanı (Hafıza)",
            "🤖 Açık Kaynak AI & Ollama",
            "🛡️ Güvenlik Kalkanı & Rate Limit",
            "🧠 JSON Hafıza & Öğretilenler",
            "📊 Modül Sistem Durumu",
        ])
        with ay_tab0:
            import modul_28_kisisel_hafiza as _m28p
            _m28p.hafiza_paneli()

        with ay_tab1:
            st.subheader("🤖 Sohbet Botu İçin Açık Kaynaklı Yapay Zeka Siteleri")
            saglayicilar = m9_ollama_tdk.ACIK_KAYNAK_AI_SAGLAYICILARI
            for k_kod, k_veri in saglayicilar.items():
                st.markdown(
                    m1_arayuz.bilgi_karti_olustur(
                        k_veri["ad"],
                        f"Model: {k_veri['model']} | {'Anahtarsız Ücretsiz' if not k_veri['anahtar_gerekli'] else 'Ücretsiz API Anahtarlı'}",
                        k_veri["aciklama"],
                    ),
                    unsafe_allow_html=True,
                )
            st.markdown("---")
            m9_ollama_tdk.ollama_ve_tdk_studyosu_goster(m5_dil.sesli_soyle)

        with ay_tab2:
            m11_guvenlik.guvenlik_studyosu_goster()

        with ay_tab3:
            st.subheader("🧠 JSON Komut ve Hafıza Yönetimi")
            col_j1, col_j2 = st.columns(2, gap="large")
            with col_j1:
                with st.form("yeni_komut_formu", clear_on_submit=True):
                    kat_input = st.text_input("Kategori Adı:", placeholder="Örn: ozel_bilgiler")
                    kelime_input = st.text_input("Anahtar Kelimeler (Virgülle):", placeholder="Örn: okulum, favori ders")
                    yanit_input = st.text_area("Verilecek Cevap:", height=110)
                    if st.form_submit_button("💾 JSON Dosyasına Kaydet", use_container_width=True):
                        if kat_input and kelime_input and yanit_input:
                            m3_veri.json_komut_ekle(kat_input, kelime_input, yanit_input)
                            st.success(f"'{kat_input}' başarıyla kaydedildi!")
                            st.rerun()
            with col_j2:
                guncel_json = m3_veri.json_oku()
                if guncel_json:
                    sil_secim = st.selectbox("Silinecek Kategori:", options=list(guncel_json.keys()))
                    if st.button("🗑️ Seçili Kategoriyi Sil", use_container_width=True):
                        m3_veri.json_kategori_sil(sil_secim)
                        st.rerun()
                st.json(guncel_json)

        with ay_tab4:
            st.subheader("📊 Modüler Mimari ve Canlı Bağlantı Kontrolü")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Hazır AI Kalıbı", f"{len(kalip_havuzu):,}".replace(",", "."), "O(1) İndeks")
            m2.metric("Bağlı Modül Sayısı", "13 / 13 Modül", "Tam Entegre")
            m3.metric("İslam Âlimleri", f"{len(m2_alimler.ISLAM_ALIMLERI)} Âlim", "Tam Ansiklopedi")
            m4.metric("3D Çevirmeli Kart", f"{len(m5_dil.A1_A2_DIL_PRATIK_KARTLARI)} Kart", "A1 & A2 (EN/AR/BN)")

            if st.button("🔄 13 Modül Dosyasını Proje Klasöründe Otomatik Onar / Güncelle", use_container_width=True):
                eksik_modulleri_otomatik_olustur(zorla_yenile=True)
                st.success("13 modül dosyası proje klasörüne başarıyla yazıldı ve güncellendi!")
                st.rerun()

            for m_no, m_dosya, m_aciklama, m_aktif in MODUL_DURUM_LISTESI:
                durum = "✅ AKTİF " if m_aktif else "❌ BULUNAMADI"
                st.markdown(
                    m1_arayuz.bilgi_karti_olustur(f"📦 {m_no}: {m_dosya}", durum, m_aciklama),
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    try:
        sistemi_baslat()
    except Exception as _kritik_hata:
        # Streamlit'in normal akış kontrol sinyallerini (st.rerun / st.stop) ASLA hata sayma!
        if type(_kritik_hata).__name__ in ("RerunException", "StopException", "ScriptControlException"):
            raise
        # Karşı tarafa HİÇBİR traceback, kod veya dosya yolu vermeden verileri yedekle ve güvenli mesaj göster!
        try:
            m11_guvenlik.guvenlik_olayi_kaydet("Kritik Çalışma Hatası Yakalandı", type(_kritik_hata).__name__, "KRİTİK")
            m11_guvenlik.acil_yedek_olustur("Kritik Hata Koruması")
        except Exception:
            pass
        st.error("🛡️ Sistem beklenmeyen bir durum algıladı, verileriniz otomatik yedeklendi ve koruma moduna geçildi. Lütfen sayfayı yenileyin.")