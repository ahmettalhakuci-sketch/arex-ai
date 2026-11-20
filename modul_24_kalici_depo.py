# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 24: KALICI BULUT DEPOSU (Supabase, ücretsiz) (modul_24_kalici_depo.py)
==============================================================================
Streamlit Cloud uygulamayı yeniden başlattığında yerel JSON dosyaları sıfırlanır. Bu modül, kişisel
veri dosyalarını (Modül 20'nin beyaz listesi) kullanıcının KENDİ Supabase veritabanında saklar:

  • Süreç ilk açıldığında  → veritabanındaki kayıtlar yerel dosyalara geri yazılır (veritabanı esastır;
                             farklı olan yerel dosyanın önce ar_acil_yedekler/bulut_oncesi_* kopyası alınır)
  • Her çalıştırmada       → değişen dosyalar arka planda veritabanına gönderilir (yalnızca değişenler)

Ek paket gerekmez (Supabase REST / PostgREST, urllib). Anahtarlar yalnızca sunucuda kullanılır.
Secrets:
    SUPABASE_URL = "https://xxxx.supabase.co"
    SUPABASE_KEY = "service_role anahtarı"   # Project Settings → API (tarayıcıya ASLA gönderilmez)
Tablo (Supabase → SQL Editor):
    create table if not exists arex_veri (
      ad text primary key,
      icerik text not null,
      guncelleme timestamptz not null default now()
    );
    alter table arex_veri enable row level security;   -- anonim erişim kapalı; service_role atlar
Tanımlı değilse modül hiçbir şey yapmaz.
"""

import json
import os
import shutil
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

_KOK = os.path.dirname(os.path.abspath(__file__))
TABLO = "arex_veri"
_EN_FAZLA_BAYT = 5 * 1024 * 1024
_HARIC = {"tdk_anlam_onbellek.json"}  # yeniden üretilebilir önbellek, saklamaya gerek yok

_KILIT = threading.Lock()
_DURUM = {"geri_yuklendi": False, "imzalar": {}, "son_esitleme": None, "son_hata": None, "gonderilen": 0}


def _ayar(ad: str) -> str:
    deger = os.environ.get(ad, "")
    if not deger:
        try:
            import streamlit as st
            deger = str(st.secrets.get(ad, "") or "")
        except Exception:
            deger = ""
    return deger.strip()


def yapilandirma():
    """→ (url, anahtar) ya da (None, None)."""
    url, anahtar = _ayar("SUPABASE_URL").rstrip("/"), _ayar("SUPABASE_KEY")
    if not url or not anahtar or not url.startswith(("https://", "http://127.0.0.1", "http://localhost")):
        return None, None
    return url, anahtar


def etkin_mi() -> bool:
    return yapilandirma()[0] is not None


def _dosyalar() -> list:
    try:
        import modul_20_yedekleme as m20
        adlar = list(m20.YEDEK_DOSYALARI)
    except Exception:
        adlar = []
    return [a for a in adlar if a not in _HARIC]


def _istek(yontem: str, yol: str, govde=None, ek_baslik=None, zaman_asimi=8):
    url, anahtar = yapilandirma()
    if not url:
        raise RuntimeError("Supabase yapılandırılmamış")
    basliklar = {"apikey": anahtar, "Authorization": f"Bearer {anahtar}", "Content-Type": "application/json",
                 "Accept": "application/json"}
    basliklar.update(ek_baslik or {})
    veri = json.dumps(govde, ensure_ascii=False).encode("utf-8") if govde is not None else None
    req = urllib.request.Request(f"{url}/rest/v1/{yol}", data=veri, headers=basliklar, method=yontem)
    with urllib.request.urlopen(req, timeout=zaman_asimi) as yanit:
        ham = yanit.read().decode("utf-8")
    return json.loads(ham) if ham.strip() else None


def _imza(yol: str):
    try:
        st_ = os.stat(yol)
        return (st_.st_mtime_ns, st_.st_size)
    except OSError:
        return None


def geri_yukle() -> dict:
    """Veritabanındaki kayıtları yerel dosyalara yazar (süreç başına bir kez). → {'yazilan': [...], 'hata': ...}"""
    sonuc = {"yazilan": [], "hata": None, "uzakta": set()}
    adlar = set(_dosyalar())
    try:
        satirlar = _istek("GET", f"{TABLO}?select=ad,icerik,guncelleme") or []
    except Exception as e:
        sonuc["hata"] = f"{type(e).__name__}: {str(e)[:120]}"
        return sonuc
    kopya_dir = None
    for satir in satirlar:
        ad, icerik = satir.get("ad"), satir.get("icerik")
        if ad not in adlar or not isinstance(icerik, str):
            continue  # beyaz liste dışı ad (ör. '../main.py') asla yazılmaz
        try:
            json.loads(icerik)
        except Exception:
            continue
        sonuc["uzakta"].add(ad)
        yol = os.path.join(_KOK, ad)
        try:
            with open(yol, "r", encoding="utf-8") as f:
                yerel = f.read()
        except OSError:
            yerel = None
        if yerel == icerik:
            continue
        if yerel is not None:  # farklı yerel dosyanın güvenlik kopyası
            if kopya_dir is None:
                kopya_dir = os.path.join(_KOK, "ar_acil_yedekler", "bulut_oncesi_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
                os.makedirs(kopya_dir, exist_ok=True)
            shutil.copy2(yol, os.path.join(kopya_dir, ad))
        gecici = yol + ".bulut"
        with open(gecici, "w", encoding="utf-8") as f:
            f.write(icerik)
        os.replace(gecici, yol)
        sonuc["yazilan"].append(ad)
    return sonuc


def degisenleri_gonder() -> list:
    """Son eşitlemeden beri değişen dosyaları veritabanına yazar (upsert). → gönderilen dosya adları"""
    gonderilecek = []
    for ad in _dosyalar():
        yol = os.path.join(_KOK, ad)
        imza = _imza(yol)
        if imza is None or imza == _DURUM["imzalar"].get(ad):
            continue
        if imza[1] > _EN_FAZLA_BAYT:
            continue
        try:
            with open(yol, "r", encoding="utf-8") as f:
                icerik = f.read()
            json.loads(icerik)  # yarım yazılmış dosyayı gönderme; sonraki turda tekrar denenir
        except Exception:
            continue
        gonderilecek.append((ad, icerik, imza))
    if not gonderilecek:
        return []
    zaman = datetime.now(timezone.utc).isoformat(timespec="seconds")
    _istek("POST", f"{TABLO}?on_conflict=ad",
           [{"ad": ad, "icerik": icerik, "guncelleme": zaman} for ad, icerik, _ in gonderilecek],
           ek_baslik={"Prefer": "resolution=merge-duplicates,return=minimal"})
    for ad, _, imza in gonderilecek:
        _DURUM["imzalar"][ad] = imza
    _DURUM["gonderilen"] += len(gonderilecek)
    return [ad for ad, _, _ in gonderilecek]


def esitle(arka_planda: bool = True):
    """Her çalıştırmada çağrılır: ilk kez geri yükler, sonra değişenleri gönderir. Hata uygulamayı durdurmaz."""
    if not etkin_mi():
        return

    def _calis():
        if not _KILIT.acquire(blocking=False):
            return  # önceki eşitleme sürüyor
        try:
            if not _DURUM["geri_yuklendi"]:
                s = geri_yukle()
                if s["hata"]:
                    _DURUM["son_hata"] = s["hata"]
                    return  # veritabanına ulaşılamadı → yerel dosyaları EZMEMEK için gönderme de yapma
                _DURUM["geri_yuklendi"] = True
                for ad in s["uzakta"]:  # veritabanındakiler taban; olmayanlar ilk turda yüklenir
                    _DURUM["imzalar"][ad] = _imza(os.path.join(_KOK, ad))
            degisenleri_gonder()
            _DURUM["son_esitleme"] = time.time()
            _DURUM["son_hata"] = None
        except Exception as e:
            _DURUM["son_hata"] = f"{type(e).__name__}: {str(e)[:120]}"
        finally:
            _KILIT.release()

    if arka_planda and _DURUM["geri_yuklendi"]:
        threading.Thread(target=_calis, daemon=True).start()
    else:
        _calis()  # ilk geri yükleme, sayfa veriyi okumadan ÖNCE bitmeli


def durum_metni() -> str:
    if not etkin_mi():
        return "☁️ Kalıcı bulut kaydı **kapalı** (Supabase tanımlı değil — README'ye bak)."
    if _DURUM["son_hata"]:
        return f"☁️ Kalıcı bulut kaydı: ⚠️ ulaşılamadı ({_DURUM['son_hata'][:60]})"
    if _DURUM["son_esitleme"]:
        return f"☁️ Kalıcı bulut kaydı **açık** · son eşitleme {datetime.fromtimestamp(_DURUM['son_esitleme']):%H:%M}"
    return "☁️ Kalıcı bulut kaydı **açık**"
