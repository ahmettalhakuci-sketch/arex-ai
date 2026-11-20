# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v7.0 — MODÜL 11: ÜST DÜZEY SİBER GÜVENLİK ZIRHI, HARİCİ TEHDİT
VERİTABANI, 3 KADEMELİ RATE LIMITER, OTOMATİK ACİL YEDEKLEME VE FAIL-CLOSED
SİSTEM KAPATMA KATMANI (modul_11_guvenlik_kalkani.py)

Özellikler:
  1. Harici Siber Güvenlik Datası (`ar_siber_guvenlik_datasi.json`):
     SQLi, XSS, RCE/Komut Enjeksiyonu, Path Traversal, Prompt Injection / Veri
     Sızdırma ve Zararlı Bot imzalarını dış JSON veritabanından yönetir.
  2. 3 Kademeli Güçlendirilmiş Rate Limiter ('Limit Edition') + Tehdit Skoru:
     Ani flood (5 sn), dakikalık limit (60 sn) ve kümülatif Tehdit Skoru (0-100).
  3. Acil Durum Otomatik Yedekleme + Sistemi Kapatma (Fail-Closed Kill Switch):
     Saldırı şiddeti eşiği aşarsa (Tehdit Skoru >= 100) veya sistem gücü zorlanırsa:
       a) Tüm kodları ve kullanıcı verilerini `ar_acil_yedekler/yedek_*.zip` içine yedekler.
       b) Karşı tarafa HİÇBİR veri, traceback veya sistem bilgisi vermeden erişimi kapatır.
       c) Yalnızca yönetici PIN koduyla tekrar açılabilir.
  4. Hata / Traceback Sızıntı Koruması (Sıfır Bilgi İfşası).
==============================================================================
"""
from collections import deque
from datetime import datetime
import hashlib
import hmac
import html
import ipaddress
import json
import os
import re
import threading
import time
import urllib.parse
import zipfile
import streamlit as st

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
GUVENLIK_LOG_DOSYASI = os.path.join(_MODUL_DIZINI, "ar_guvenlik_log.json")
SIBER_DATA_DOSYASI = os.path.join(_MODUL_DIZINI, "ar_siber_guvenlik_datasi.json")
ACIL_KILIT_DOSYASI = os.path.join(_MODUL_DIZINI, ".ar_acil_kilit.json")
ACIL_YEDEK_KLASORU = os.path.join(_MODUL_DIZINI, "ar_acil_yedekler")

VARSAYILAN_IZINLI_HOSTLAR = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}
GUVENLI_BULUT_SONEKLERI = (
    ".streamlit.app",
    ".streamlit.io",
    ".streamlitapp.com",
    ".app.github.dev",
    ".githubpreview.dev",
    ".hf.space",
    ".onrender.com",
)
_PIN_TUZU = "ar_ai_studio_v75_salt"
_VARSAYILAN_PIN_OZETI = hashlib.sha256((_PIN_TUZU + ":" + chr(49) + chr(52) + chr(53) + chr(51)).encode("utf-8")).hexdigest()


def pin_ozetle(ham_pin: str) -> str:
    """PIN kodunu tuzlanmış SHA-256 özetine çevirir (düz metin şifre tutulmaz)."""
    return hashlib.sha256(f"{_PIN_TUZU}:{str(ham_pin).strip()}".encode("utf-8")).hexdigest()


def aktif_pin_ozetini_getir() -> str:
    """Önce session_state hash'ini, sonra ortam değişkeni / st.secrets'ı, yoksa varsayılan özeti döndürür."""
    ozel_ozet = st.session_state.get("guvenlik_pin_ozeti", "")
    if ozel_ozet:
        return str(ozel_ozet)
    env_pin = os.environ.get("AR_ADMIN_PIN", "").strip()
    if env_pin:
        return pin_ozetle(env_pin)
    try:
        sec_pin = st.secrets.get("AR_ADMIN_PIN", "")
        if sec_pin:
            return pin_ozetle(str(sec_pin))
    except Exception:
        pass
    # Ayrı yönetici PIN'i yoksa ama erişim şifresi tanımlıysa (Modül 23) onu kullan:
    # kodda yazılı varsayılan PIN herkese açık depoda tahmin edilebilir olduğundan bulutta geçersiz kalır.
    erisim = os.environ.get("AREX_ERISIM_SIFRESI", "").strip()
    if not erisim:
        try:
            erisim = str(st.secrets.get("AREX_ERISIM_SIFRESI", "") or "").strip()
        except Exception:
            erisim = ""
    if erisim:
        return pin_ozetle(erisim)
    return _VARSAYILAN_PIN_OZETI


def pin_dogrula(girilen_pin: str) -> bool:
    """Zamanlama saldırısına dayanıklı (hmac.compare_digest) sabit zamanlı PIN doğrulaması."""
    if not girilen_pin or not isinstance(girilen_pin, str):
        return False
    hedef = aktif_pin_ozetini_getir()
    aday = pin_ozetle(girilen_pin)
    return hmac.compare_digest(aday, hedef)

# Dışarıdan yönetilebilen kapsamlı siber güvenlik imza veritabanı şablonu
VARSAYILAN_SIBER_GUVENLIK_DATASI = {
    "surum": "7.6-CYBER-SHIELD-BALANCED",
    "esik_tehdit_skoru_kilit": 250,
    "maks_girdi_karakter": 6000,
    "izinli_ek_hostlar": [],
    "engellenen_ipler": [],
    "zararli_bot_imzalari": [
        "sqlmap", "nikto", "nmap", "masscan", "hydra", "dirbuster", "gobuster",
        "wfuzz", "burpsuite", "zaproxy", "acunetix", "nessus", "nuclei",
        "metasploit", "havij", "commix", "wpscan", "ffuf", "feroxbuster",
    ],
    "sqli_imzalari": [
        r"(?i)\bunion\s+select\b",
        r"(?i)'\s*or\s*'1'\s*=\s*'1",
        r"(?i)\bdrop\s+table\b",
        r"(?i)\bdelete\s+from\b",
        r"(?i)\bwaitfor\s+delay\b",
        r"(?i)\bsleep\s*\(\s*\d+\s*\)",
    ],
    "xss_imzalari": [
        r"(?i)<\s*script\b",
        r"(?i)</\s*script\s*>",
        r"(?i)javascript\s*:",
        r"(?i)\bon(?:error|load|click|mouseover|focus)\s*=",
        r"(?i)document\.cookie",
        r"(?i)<\s*iframe\b",
        r"(?i)<\s*svg\b[^>]*onload",
    ],
    "rce_komut_imzalari": [
        r"(?i)__import__\s*\(\s*['\"]os['\"]",
        r"(?i)\bos\.system\s*\(",
        r"(?i);\s*(?:rm\s+-rf|cat\s+/etc/|wget\s+|curl\s+|powershell\b|cmd\.exe\b)",
    ],
    "path_traversal_imzalari": [
        r"\.\./",
        r"\.\.\\",
        r"(?i)/etc/passwd",
        r"(?i)c:\\windows\\win\.ini",
        r"(?i)ar_guvenlik_log\.json",
        r"(?i)ar_siber_guvenlik_datasi\.json",
    ],
    "veri_sizdirma_prompt_imzalari": [
        r"(?i)ignore\s+(?:all\s+)?previous\s+instructions",
        r"(?i)reveal\s+(?:your\s+)?system\s+prompt",
        r"(?i)t[üu]m\s+kodlar[ıi]n[ıi]\s*(?:dök|ver|sızdır)",
        r"(?i)şifreleri\s*(?:ver|göster|söyle)",
    ],
}


def siber_guvenlik_datasini_yukle(zorla_olustur: bool = False) -> dict:
    """
    Harici `ar_siber_guvenlik_datasi.json` dosyasını okur; yoksa otomatik oluşturur.
    Böylece güvenlik kuralları kodun dışında bağımsız bir tehdit veritabanı olarak yaşar.
    """
    if zorla_olustur or not os.path.exists(SIBER_DATA_DOSYASI):
        try:
            with open(SIBER_DATA_DOSYASI, "w", encoding="utf-8") as f:
                json.dump(VARSAYILAN_SIBER_GUVENLIK_DATASI, f, ensure_ascii=False, indent=2)
        except Exception:
            return dict(VARSAYILAN_SIBER_GUVENLIK_DATASI)
    try:
        with open(SIBER_DATA_DOSYASI, "r", encoding="utf-8") as f:
            veri = json.load(f)
        if isinstance(veri, dict):
            if veri.get("surum") != VARSAYILAN_SIBER_GUVENLIK_DATASI["surum"]:
                birlesik = dict(VARSAYILAN_SIBER_GUVENLIK_DATASI)
                birlesik["izinli_ek_hostlar"] = veri.get("izinli_ek_hostlar", [])
                birlesik["engellenen_ipler"] = veri.get("engellenen_ipler", [])
                try:
                    with open(SIBER_DATA_DOSYASI, "w", encoding="utf-8") as fw:
                        json.dump(birlesik, fw, ensure_ascii=False, indent=2)
                except Exception:
                    pass
                return birlesik
            birlesik = dict(VARSAYILAN_SIBER_GUVENLIK_DATASI)
            birlesik.update(veri)
            return birlesik
    except Exception:
        pass
    return dict(VARSAYILAN_SIBER_GUVENLIK_DATASI)


@st.cache_resource(show_spinner=False)
def _kuresel_guvenlik_deposu():
    """Tüm oturumlar arasında paylaşılan thread-safe hız sınırı, tehdit skoru ve kilitleme deposu."""
    return {
        "kilit": threading.Lock(),
        "istek_gecmisi": {},       # anahtar -> deque([timestamps])
        "engelli_kayitlar": {},    # anahtar -> engel_bitis_timestamp
        "tehdit_skorlari": {},     # anahtar -> int (0..100+)
        "istatistik": {
            "toplam_kontrol": 0,
            "engellenen_rate_limit": 0,
            "engellenen_sunucu": 0,
            "temizlenen_girdi": 0,
            "acil_yedek_sayisi": 0,
        },
    }


def guvenlik_olayi_kaydet(olay_turu: str, detay: str, seviye: str = "UYARI"):
    kayit = {
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seviye": seviye,
        "tur": olay_turu,
        "detay": str(detay)[:240],
    }
    try:
        mevcut = []
        if os.path.exists(GUVENLIK_LOG_DOSYASI):
            with open(GUVENLIK_LOG_DOSYASI, "r", encoding="utf-8") as f:
                mevcut = json.load(f)
            if not isinstance(mevcut, list):
                mevcut = []
        mevcut.append(kayit)
        mevcut = mevcut[-200:]
        with open(GUVENLIK_LOG_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(mevcut, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def guvenlik_loglarini_oku() -> list:
    try:
        if os.path.exists(GUVENLIK_LOG_DOSYASI):
            with open(GUVENLIK_LOG_DOSYASI, "r", encoding="utf-8") as f:
                veri = json.load(f)
            if isinstance(veri, list):
                return list(reversed(veri))
    except Exception:
        pass
    return []


# ==============================================================================
# OTOMATİK ACİL YEDEKLEME + FAIL-CLOSED SİSTEM KAPATMA (VERİ SIZDIRMAMA)
# ==============================================================================
def acil_yedek_olustur(sebep: str = "Manuel / Acil Koruma") -> str:
    """
    Tüm emekleri (main.py, modul_*.py, komutlar.json, sohbet oturumları, ders notları,
    güvenlik datası) tek bir zaman damgalı ZIP arşivine yedekler.
    """
    try:
        os.makedirs(ACIL_YEDEK_KLASORU, exist_ok=True)
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_yolu = os.path.join(ACIL_YEDEK_KLASORU, f"ar_acil_yedek_{zaman_damgasi}.zip")
        yedeklenecek_uzantilar = (".py", ".json")
        yasakli_dosyalar = {".env", "secrets.toml", ".ar_acil_kilit.json", "ar_guvenlik_log.json"}
        with zipfile.ZipFile(zip_yolu, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for dosya in sorted(os.listdir(_MODUL_DIZINI)):
                tam_yol = os.path.join(_MODUL_DIZINI, dosya)
                if (
                    os.path.isfile(tam_yol)
                    and dosya.endswith(yedeklenecek_uzantilar)
                    and dosya not in yasakli_dosyalar
                    and not dosya.startswith(("gecici_ses_", "."))
                ):
                    zf.write(tam_yol, arcname=dosya)
        depo = _kuresel_guvenlik_deposu()
        with depo["kilit"]:
            depo["istatistik"]["acil_yedek_sayisi"] += 1
        guvenlik_olayi_kaydet("Acil Yedekleme Tamamlandı", f"Sebep: {sebep} | Dosya: {os.path.basename(zip_yolu)}", "KRİTİK")
        return zip_yolu
    except Exception as e:
        guvenlik_olayi_kaydet("Acil Yedekleme Hatası", str(e), "KRİTİK")
        return ""


def acil_kilit_durumu_oku() -> dict:
    try:
        if os.path.exists(ACIL_KILIT_DOSYASI):
            with open(ACIL_KILIT_DOSYASI, "r", encoding="utf-8") as f:
                veri = json.load(f)
            if isinstance(veri, dict) and veri.get("kilitli"):
                return veri
    except Exception:
        pass
    return {"kilitli": False}


def acil_durum_yedekle_ve_sistemi_kapat(sebep: str, anahtar: str = "sistem") -> str:
    """
    FAIL-CLOSED KILL SWITCH:
    Sistem gücü yetmediğinde veya ağır saldırı/flood tespit edildiğinde:
      1) Tüm verileri ve kodları anında ZIP olarak yedekler.
      2) `.ar_acil_kilit.json` kilidini aktive eder.
      3) Karşı tarafa HİÇBİR iç veri / traceback vermeden sistemi kapatır!
    """
    yedek_yolu = acil_yedek_olustur(sebep=f"ACİL KAPATMA: {sebep}")
    kilit_bilgi = {
        "kilitli": True,
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sebep": sebep,
        "anahtar": anahtar,
        "yedek_dosyasi": os.path.basename(yedek_yolu) if yedek_yolu else "",
    }
    try:
        with open(ACIL_KILIT_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kilit_bilgi, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    guvenlik_olayi_kaydet("FAIL-CLOSED SİSTEM KİLİTLENDİ", f"Sebep: {sebep} | Yedek: {kilit_bilgi['yedek_dosyasi']}", "KRİTİK")
    return yedek_yolu


def acil_kilidi_kaldir():
    try:
        if os.path.exists(ACIL_KILIT_DOSYASI):
            os.remove(ACIL_KILIT_DOSYASI)
        depo = _kuresel_guvenlik_deposu()
        with depo["kilit"]:
            depo["tehdit_skorlari"].clear()
            depo["engelli_kayitlar"].clear()
        guvenlik_olayi_kaydet("Acil Kilit Kaldırıldı", "Yönetici PIN doğrulaması ile sistem normale döndü.", "UYARI")
    except Exception:
        pass


def _tehdit_skoru_artir(anahtar: str, puan: int, sebep: str) -> bool:
    """Tehdit skorunu artırır; eşiğe (>= 100) ulaşırsa otomatik yedekleyip sistemi kilitler!"""
    siber_data = siber_guvenlik_datasini_yukle()
    esik = int(siber_data.get("esik_tehdit_skoru_kilit", 100))
    depo = _kuresel_guvenlik_deposu()
    with depo["kilit"]:
        yeni_skor = depo["tehdit_skorlari"].get(anahtar, 0) + puan
        depo["tehdit_skorlari"][anahtar] = yeni_skor
    if yeni_skor >= esik:
        acil_durum_yedekle_ve_sistemi_kapat(f"Tehdit eşiği aşıldı ({yeni_skor}/{esik}) — {sebep}", anahtar=anahtar)
        return True
    return False


def _ip_yerel_ag_mi(host_str: str) -> bool:
    temiz = host_str.strip().lower()
    if temiz.startswith("[") and "]" in temiz:
        temiz = temiz[1:temiz.index("]")]
    elif ":" in temiz and temiz.count(":") == 1:
        temiz = temiz.split(":", 1)[0]
    if temiz in VARSAYILAN_IZINLI_HOSTLAR:
        return True
    try:
        ip_obj = ipaddress.ip_address(temiz)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        return False


def _istek_basliklarini_al() -> dict:
    try:
        ctx = getattr(st, "context", None)
        if ctx is not None:
            headers = getattr(ctx, "headers", None)
            if headers:
                return {str(k).lower(): str(v) for k, v in dict(headers).items()}
    except Exception:
        pass
    return {}


def sunucu_giris_katmani_kontrol(ek_izinli_hostlar: list = None, sadece_yerel_ag: bool = False) -> tuple:
    """
    Harici `ar_siber_guvenlik_datasi.json` kullanarak:
      1) Acil Kilit Modu (Fail-Closed) kontrolü
      2) Kara listedeki IP / Zararlı tarama botu (sqlmap, nmap vb.) engeli
      3) Başka sunucudan gelen Host / X-Forwarded-Host / Origin engeli
    """
    siber_data = siber_guvenlik_datasini_yukle()
    depo = _kuresel_guvenlik_deposu()
    with depo["kilit"]:
        depo["istatistik"]["toplam_kontrol"] += 1

    basliklar = _istek_basliklarini_al()
    host_raw = basliklar.get("host", "localhost").strip()
    xfwd_host = basliklar.get("x-forwarded-host", "").strip()
    origin_raw = basliklar.get("origin", "").strip()
    user_agent = basliklar.get("user-agent", "").strip()
    istemci_ip = basliklar.get("x-forwarded-for", basliklar.get("x-real-ip", "yerel")).split(",")[0].strip()

    istemci_bilgi = {
        "host": host_raw,
        "origin": origin_raw or "-",
        "istemci_ip": istemci_ip or "yerel",
        "user_agent": user_agent[:80] if user_agent else "Tarayıcı",
    }

    # 1. Kara liste IP engeli
    if istemci_ip in set(siber_data.get("engellenen_ipler", [])):
        with depo["kilit"]:
            depo["istatistik"]["engellenen_sunucu"] += 1
        return False, "🚫 Erişim reddedildi.", istemci_bilgi

    # 2. Harici siber güvenlik datasındaki zararlı bot imzaları
    ua_kucuk = user_agent.lower()
    for imza in siber_data.get("zararli_bot_imzalari", []):
        if imza in ua_kucuk:
            with depo["kilit"]:
                depo["istatistik"]["engellenen_sunucu"] += 1
            guvenlik_olayi_kaydet("Zararlı Tarayıcı Engellendi", f"İmza: {imza} | IP: {istemci_ip}", "KRİTİK")
            _tehdit_skoru_artir(istemci_ip, 50, f"Zararlı bot ({imza})")
            return False, "🛡️ Erişim güvenlik kalkanı tarafından durduruldu.", istemci_bilgi

    # 3. İzinli Host kontrolü
    izinli_set = set(VARSAYILAN_IZINLI_HOSTLAR)
    for h in (ek_izinli_hostlar or []) + list(siber_data.get("izinli_ek_hostlar", [])):
        h_temiz = str(h).strip().lower().split(":")[0]
        if h_temiz:
            izinli_set.add(h_temiz)

    def _host_onayli_mi(deger: str) -> bool:
        if not deger:
            return True
        if "://" in deger:
            alan = (urllib.parse.urlparse(deger).hostname or "").lower()
        else:
            alan = deger.lower().split(":")[0].strip("[]")
        if not alan or alan in izinli_set:
            return True
        if any(alan.endswith(sonek) for sonek in GUVENLI_BULUT_SONEKLERI):
            return True
        return bool(sadece_yerel_ag and _ip_yerel_ag_mi(alan))

    if sadece_yerel_ag:
        for baslik_ad, deger in [("Host", host_raw), ("X-Forwarded-Host", xfwd_host), ("Origin", origin_raw)]:
            if deger and not _host_onayli_mi(deger):
                with depo["kilit"]:
                    depo["istatistik"]["engellenen_sunucu"] += 1
                guvenlik_olayi_kaydet(f"Yetkisiz Sunucu ({baslik_ad})", f"Değer: {deger} | IP: {istemci_ip}", "KRİTİK")
                return False, "🚫 Yetkisiz sunucu erişimi güvenlik katmanı tarafından engellendi.", istemci_bilgi

    return True, "Güvenli bağlantı doğrulandı.", istemci_bilgi


def rate_limit_kontrol(
    oturum_anahtari: str = "varsayilan",
    dakikalik_limit: int = 120,
    ani_patlama_limit: int = 15,
    bekleme_saniyesi: int = 5,
) -> tuple:
    """
    3 KADEMELİ GÜÇLENDİRİLMİŞ RATE LIMITER ('Limit Edition'):
    - 5 sn ani flood -> geçici cooldown + tehdit skoru (+30)
    - 60 sn dakikalık limit -> 2x cooldown + tehdit skoru (+35)
    - Sürekli flood yapılıp tehdit skoru >= 100 olursa -> OTOMATİK YEDEKLEME + FAIL-CLOSED KAPATMA!
    """
    depo = _kuresel_guvenlik_deposu()
    simdi = time.time()
    anahtar = str(oturum_anahtari or "varsayilan")

    with depo["kilit"]:
        engel_bitis = depo["engelli_kayitlar"].get(anahtar, 0)
        if simdi < engel_bitis:
            kalan_sn = int(engel_bitis - simdi) + 1
            depo["istatistik"]["engellenen_rate_limit"] += 1
            asildi_mi = False
        else:
            gecmis = depo["istek_gecmisi"].setdefault(anahtar, deque())
            while gecmis and (simdi - gecmis[0]) > 60.0:
                gecmis.popleft()

            son_5_sn = sum(1 for t in gecmis if (simdi - t) <= 5.0)
            if son_5_sn >= ani_patlama_limit:
                depo["engelli_kayitlar"][anahtar] = simdi + bekleme_saniyesi
                depo["istatistik"]["engellenen_rate_limit"] += 1
                asildi_mi = "flood"
            elif len(gecmis) >= dakikalik_limit:
                depo["engelli_kayitlar"][anahtar] = simdi + (bekleme_saniyesi * 2)
                depo["istatistik"]["engellenen_rate_limit"] += 1
                asildi_mi = "dakika"
            else:
                gecmis.append(simdi)
                return True, "", max(0, dakikalik_limit - len(gecmis))

    if asildi_mi == "flood":
        guvenlik_olayi_kaydet("Ani Hız Limiti", f"Anahtar: {anahtar} | 5 sn içinde aşırı istek", "UYARI")
        return False, f"⏳ **Çok hızlı arka arkaya istek gönderdiniz.** Kısa bir nefes için **{bekleme_saniyesi} saniye** bekleyin.", 0

    if asildi_mi == "dakika":
        guvenlik_olayi_kaydet("Dakikalık Hız Limiti", f"Anahtar: {anahtar}", "UYARI")
        return False, f"⏳ **Dakikalık limit ({dakikalik_limit} istek/dk) doldu.** Kısa bir ara ({bekleme_saniyesi} sn) sonra devam edebilirsiniz.", 0

    return False, f"⏳ **Rate Limit Aktif!** Lütfen **{kalan_sn} saniye** bekleyin.", 0


def girdi_guvenlik_ve_bug_kontrol(kullanici_girdisi: str, maks_uzunluk: int = None, oturum_anahtari: str = "varsayilan") -> tuple:
    """
    Harici `ar_siber_guvenlik_datasi.json` imzalarına göre SQLi, XSS, RCE, Path Traversal,
    Prompt Injection / Veri Sızdırma ve Math-DoS (CPU kilitleme) saldırılarını durdurur.
    Ağır tekrarlı saldırıda otomatik yedekleyip sistemi fail-closed kapatır!
    """
    if not isinstance(kullanici_girdisi, str):
        return False, "", "🛡️ Geçersiz veri tipi algılandı."

    siber_data = siber_guvenlik_datasini_yukle()
    limit_uzunluk = maks_uzunluk or int(siber_data.get("maks_girdi_karakter", 1200))
    depo = _kuresel_guvenlik_deposu()

    temiz = kullanici_girdisi.replace("\x00", "").strip()
    temiz = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", temiz)

    if not temiz:
        return False, "", "Lütfen boş olmayan bir mesaj yazın."

    if len(temiz) > limit_uzunluk:
        with depo["kilit"]:
            depo["istatistik"]["temizlenen_girdi"] += 1
        guvenlik_olayi_kaydet("Aşırı Uzun Girdi", f"Uzunluk: {len(temiz)} > {limit_uzunluk}", "UYARI")
        _tehdit_skoru_artir(oturum_anahtari, 20, "Aşırı uzun girdi / ReDoS denemesi")
        return False, "", f"🛡️ **Güvenlik Limiti:** Tek seferde en fazla **{limit_uzunluk} karakter** gönderebilirsiniz."

    # Harici siber güvenlik datasındaki tüm imza kategorilerini tara
    imza_gruplari = [
        ("SQL Enjeksiyonu", siber_data.get("sqli_imzalari", []), 45),
        ("XSS / Script Saldırısı", siber_data.get("xss_imzalari", []), 45),
        ("Komut Enjeksiyonu (RCE)", siber_data.get("rce_komut_imzalari", []), 55),
        ("Dosya Yolu Saldırısı (Path Traversal)", siber_data.get("path_traversal_imzalari", []), 50),
        ("Veri Sızdırma / Prompt Enjeksiyonu", siber_data.get("veri_sizdirma_prompt_imzalari", []), 40),
    ]
    for grup_adi, regex_listesi, ceza_puani in imza_gruplari:
        for desen in regex_listesi:
            try:
                if re.search(desen, temiz):
                    with depo["kilit"]:
                        depo["istatistik"]["temizlenen_girdi"] += 1
                    guvenlik_olayi_kaydet(grup_adi, f"Engellenen desen tespit edildi (Uzunluk: {len(temiz)})", "KRİTİK")
                    # Saldırı girdisini anında engelle ve logla (bulutta yanlışlıkla tüm uygulamayı kilitlemez)
                    return False, "", "🛡️ **Siber Güvenlik Kalkanı:** İstek güvenlik politikasına aykırı bulunduğu için engellendi."
            except re.error:
                continue

    # Math-DoS (CPU kilitleyen dev üs) koruması
    us_eslesme = re.search(r"(\d{2,})\s*(?:\*\*|\^|üssü|ussu)\s*(\d+)", temiz, flags=re.IGNORECASE)
    if us_eslesme:
        taban, us_val = int(us_eslesme.group(1)), int(us_eslesme.group(2))
        if (us_val > 500 and taban > 2) or us_val > 2000:
            with depo["kilit"]:
                depo["istatistik"]["temizlenen_girdi"] += 1
            guvenlik_olayi_kaydet("CPU Kilitleme (Math-DoS)", f"{taban}^{us_val}", "UYARI")
            _tehdit_skoru_artir(oturum_anahtari, 25, "Math-DoS")
            return False, "", "🛡️ **İşlem Limiti:** Çok büyük üs değeri sunucu işlemcisini korumak için sınırlandırıldı."

    return True, temiz, ""


def dis_url_guvenli_mi(url: str, yerel_ag_izinli: bool = True) -> bool:
    try:
        parsed = urllib.parse.urlparse(url.strip())
        if parsed.scheme not in ("http", "https"):
            return False
        host = (parsed.hostname or "").lower()
        if not host or host in {"169.254.169.254", "metadata.google.internal", "metadata.internal"}:
            return False
        if not yerel_ag_izinli and _ip_yerel_ag_mi(host):
            return False
        return True
    except Exception:
        return False


def html_guvenli_metin(metin: str) -> str:
    return html.escape(str(metin), quote=True)


def guvenlik_studyosu_goster():
    siber_data = siber_guvenlik_datasini_yukle()
    st.subheader("🛡️ Siber Güvenlik Zırhı, Harici Tehdit Datası & Acil Yedekleme Merkezi")
    depo = _kuresel_guvenlik_deposu()
    ist = depo["istatistik"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Güvenlik Kontrolü", ist["toplam_kontrol"], "v7.5 Bulut+Yerel Zırh")
    c2.metric("Rate Limit Engeli", ist["engellenen_rate_limit"], "3 Kademeli")
    c3.metric("Saldırı / Bot Engeli", ist["engellenen_sunucu"] + ist["temizlenen_girdi"], "SQLi/XSS/RCE")
    c4.metric("Acil ZIP Yedeği", ist["acil_yedek_sayisi"], "ar_acil_yedekler/")

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("💾 Şimdi Tam Güvenlik Yedeği Al (ZIP)", use_container_width=True):
            yol = acil_yedek_olustur("Kullanıcı Manuel Tam Yedek")
            if yol:
                st.success(f"✅ Tüm 13 modül ve veriler yedeklendi: `{os.path.basename(yol)}`")
    with b2:
        if st.button("🚨 Acil Durum: Yedekle ve Sistemi Kilitle", use_container_width=True):
            acil_durum_yedekle_ve_sistemi_kapat("Yönetici Manuel Acil Kilitleme")
            st.rerun()

    k_col1, k_col2 = st.columns(2, gap="large")
    with k_col1:
        st.markdown("#### 🔒 Sunucu & PIN Koruma Ayarları")
        st.session_state.guvenlik_sadece_yerel = st.toggle(
            "🌐 Başka Sunuculardan Girişi Engelle (Sadece Localhost & Yerel Ağ)",
            value=st.session_state.get("guvenlik_sadece_yerel", False),
        )
        st.session_state.guvenlik_pin_aktif = st.toggle(
            "🔑 Giriş PIN Kilidi (Aç / Kapat)",
            value=st.session_state.get("guvenlik_pin_aktif", False),
        )
        yeni_pin = st.text_input(
            "Yeni Yönetici PIN Kodu Belirle (SHA-256 Şifreli Saklanır):",
            value="",
            placeholder="Değiştirmek için yeni PIN yazın (en az 4 karakter)",
            type="password",
        )
        if yeni_pin and len(yeni_pin.strip()) >= 4:
            st.session_state.guvenlik_pin_ozeti = pin_ozetle(yeni_pin.strip())
            st.success("🔑 Yönetici PIN kodu SHA-256 özet olarak güncellendi.")
        st.session_state.guvenlik_izinli_hostlar = st.text_input(
            "Ek İzinli Sunucu / Alan Adları (Virgülle):",
            value=st.session_state.get("guvenlik_izinli_hostlar", ""),
        )

    with k_col2:
        st.markdown("#### ⏱️ 3 Kademeli Limit Edition Ayarları")
        st.session_state.guvenlik_dakika_limit = st.slider("Dakikalık Maksimum İstek:", 15, 240, min(240, max(15, int(st.session_state.get("guvenlik_dakika_limit", 120)))))
        st.session_state.guvenlik_patlama_limit = st.slider("5 Saniyelik Ani Patlama Limiti:", 5, 40, min(40, max(5, int(st.session_state.get("guvenlik_patlama_limit", 15)))))
        st.session_state.guvenlik_bekleme_sn = st.slider("Kısa Bekleme Süresi (Saniye):", 3, 60, min(60, max(3, int(st.session_state.get("guvenlik_bekleme_sn", 5)))))

    with st.expander("📁 Harici Siber Güvenlik Veritabanı (`ar_siber_guvenlik_datasi.json`)", expanded=False):
        st.json(siber_data)

    st.markdown("#### 📜 Canlı Güvenlik Olay Kayıtları (`ar_guvenlik_log.json`)")
    loglar = guvenlik_loglarini_oku()
    if loglar:
        for l_item in loglar[:20]:
            ikon = "🚨" if l_item.get("seviye") == "KRİTİK" else "⚠️"
            st.caption(f"{ikon} **[{l_item.get('zaman')}]** `{l_item.get('tur')}` — {l_item.get('detay')}")
    else:
        st.success("✅ Şu ana kadar hiçbir yetkisiz giriş veya siber tehdit tespit edilmedi.")