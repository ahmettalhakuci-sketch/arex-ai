# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 23: ZORUNLU ERİŞİM ŞİFRESİ (modul_23_erisim.py)
==============================================================================
Streamlit Cloud adresi herkese açıktır; uygulamadaki notlar, sohbetler, kişisel bilgiler ve
yedek indirme herkese görünür. Bu modül, Secrets'a tanımlanan şifreyle uygulamayı kilitler.

  • Şifre kaynağı: st.secrets / ortam değişkeni  AREX_ERISIM_SIFRESI
    (kod içinde varsayılan şifre YOKTUR; tanımlı değilse kilit devre dışıdır)
  • Tanımlıysa kilit ZORUNLUDUR: oturum içinden kapatılamaz, ayarlardan değiştirilemez
  • Sabit zamanlı karşılaştırma (hmac.compare_digest), şifre düz metin saklanmaz
  • Kaba kuvvete karşı: 5 hatalı denemeden sonra artan bekleme (30 sn, 60 sn, …)
  • Bulutta çalışırken şifre tanımlı değilse yan menüde uyarı gösterilir

Secrets örneği (.streamlit/secrets.toml veya Streamlit Cloud → Settings → Secrets):
    AREX_ERISIM_SIFRESI = "en-az-8-karakter-uzun-bir-sifre"
"""

import hashlib
import hmac
import os
import time

import streamlit as st

_ANAHTAR = "AREX_ERISIM_SIFRESI"
_TUZ = "arex_erisim_v1"
_SERBEST_DENEME = 5
_YEREL_HOSTLAR = ("localhost", "127.0.0.1", "[::1]", "0.0.0.0")


def _ozet(ham: str) -> str:
    return hashlib.sha256(f"{_TUZ}:{ham}".encode("utf-8")).hexdigest()


def tanimli_sifre_ozeti() -> str:
    """Secrets / ortam değişkenindeki şifrenin özeti; tanımlı değilse boş."""
    ham = os.environ.get(_ANAHTAR, "")
    if not ham:
        try:
            ham = str(st.secrets.get(_ANAHTAR, "") or "")
        except Exception:
            ham = ""
    ham = ham.strip()
    return _ozet(ham) if ham else ""


def sifre_dogru_mu(girilen: str, hedef_ozet: str) -> bool:
    if not girilen or not hedef_ozet:
        return False
    return hmac.compare_digest(_ozet(girilen.strip()), hedef_ozet)


def bekleme_suresi(hata_sayisi: int) -> int:
    """İlk 5 deneme serbest; sonrasında her hatada 30 sn artan bekleme (en fazla 10 dk)."""
    if hata_sayisi < _SERBEST_DENEME:
        return 0
    return min(600, 30 * (hata_sayisi - _SERBEST_DENEME + 1))


def bulutta_mi() -> bool:
    try:
        host = (st.context.headers.get("host") or "").split(":")[0].lower()
    except Exception:
        return False
    return bool(host) and not host.startswith(_YEREL_HOSTLAR) and host not in _YEREL_HOSTLAR


def erisim_kapisi():
    """Şifre tanımlıysa ve oturum doğrulanmadıysa giriş ekranını gösterip st.stop() ile durdurur."""
    hedef = tanimli_sifre_ozeti()
    if not hedef or st.session_state.get("_arex_erisim_ok") == hedef:
        return
    ss = st.session_state
    hata = int(ss.get("_arex_erisim_hata", 0))
    kilit_bitis = float(ss.get("_arex_erisim_kilit", 0))

    st.markdown(
        """<div style="max-width:420px;margin:12vh auto 18px;text-align:center">
        <div style="font-size:54px;line-height:1">⚡</div>
        <h2 style="margin:10px 0 4px">AREX AI</h2>
        <p style="opacity:.75;margin:0">Bu uygulama şifre ile korunuyor.</p></div>""",
        unsafe_allow_html=True,
    )
    _, orta, _ = st.columns([1, 3, 1])
    with orta:
        kalan = int(kilit_bitis - time.time())
        if kalan > 0:
            st.error(f"⏳ Çok fazla hatalı deneme. {kalan} saniye sonra tekrar dene.")
            st.stop()
        with st.form("arex_erisim_formu", clear_on_submit=True):
            girilen = st.text_input("Erişim şifresi", type="password", placeholder="Şifreni yaz",
                                    label_visibility="collapsed")
            gonder = st.form_submit_button("🔓 Giriş", use_container_width=True, type="primary")
        if gonder:
            if sifre_dogru_mu(girilen, hedef):
                ss["_arex_erisim_ok"] = hedef
                ss["_arex_erisim_hata"] = 0
                st.rerun()
            hata += 1
            ss["_arex_erisim_hata"] = hata
            bekle = bekleme_suresi(hata)
            if bekle:
                ss["_arex_erisim_kilit"] = time.time() + bekle
                st.error(f"❌ Hatalı şifre. {bekle} saniye beklemen gerekiyor.")
            else:
                st.error(f"❌ Hatalı şifre. ({_SERBEST_DENEME - hata} deneme hakkın kaldı)")
    st.stop()


def korumasiz_bulut_uyarisi():
    """Bulutta çalışıp şifre tanımlı değilse yan menüde uyarı gösterir."""
    if tanimli_sifre_ozeti() or not bulutta_mi():
        return
    st.warning("🔓 **Uygulaman herkese açık!** Adresi bilen herkes notlarını ve sohbetlerini görebilir. "
               "Streamlit Cloud → **Settings → Secrets** kısmına `AREX_ERISIM_SIFRESI = \"...\"` ekle.")
