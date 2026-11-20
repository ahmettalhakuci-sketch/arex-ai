# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 20: KİŞİSEL VERİ YEDEKLEME & GERİ YÜKLEME (modul_20_yedekleme.py)
==============================================================================
Streamlit Cloud uygulamayı yeniden başlattığında yerel dosyalar sıfırlanabilir. Bu modül
öğretilen cevapları, sohbetleri, notları, çalışma takibini ve hatırlatıcıları tek bir
.zip dosyasına yedekler ve geri yükler (telefondan tek dokunuş).

Güvenlik:
  • Yalnızca aşağıdaki beyaz listedeki dosya adları yedeklenir / geri yüklenir
    (zip içinde klasör, '..' veya başka ad → yok sayılır)
  • Her dosya geçerli JSON olmalı, tek dosya en fazla 20 MB
  • Geri yüklemeden önce mevcut dosyaların kopyası ar_acil_yedekler/ altına alınır
"""

import io
import json
import os
import shutil
import zipfile
from datetime import datetime

import streamlit as st

_KOK = os.path.dirname(os.path.abspath(__file__))

YEDEK_DOSYALARI = {
    "komutlar.json": "🎓 Öğrettiğin soru-cevaplar",
    "arex_sohbet_oturumlari.json": "💬 Sohbet oturumları",
    "ar_sohbet_oturumlari.json": "💬 Eski sohbet oturumları",
    "sohbet_gecmisi.json": "💬 Sohbet geçmişi",
    "ahmet_notlar.json": "📝 Notlar",
    "ahmet_ders_notlari.json": "📚 Ders notları",
    "ahmet_soru_takip.json": "📊 Çalışma takibi",
    "arex_calisma_ayarlari.json": "🎯 Günlük hedef",
    "arex_hatirlaticilar.json": "⏰ Hatırlatıcılar",
    "arex_sinavlar.json": "📅 Sınav takvimi",
    "arex_kartlar.json": "🃏 Kelime kartları",
    "arex_denemeler.json": "📈 Deneme sonuçları",
    "tdk_anlam_onbellek.json": "📕 TDK önbelleği",
}
_EN_FAZLA_BAYT = 20 * 1024 * 1024


def yedek_zip_olustur() -> tuple:
    """→ (zip_baytları, dahil_edilen_dosya_listesi)"""
    tampon = io.BytesIO()
    dahil = []
    with zipfile.ZipFile(tampon, "w", zipfile.ZIP_DEFLATED) as z:
        for ad in YEDEK_DOSYALARI:
            yol = os.path.join(_KOK, ad)
            if os.path.isfile(yol):
                z.write(yol, arcname=ad)
                dahil.append(ad)
        z.writestr("arex_yedek_bilgi.json", json.dumps(
            {"uygulama": "AREX AI Studio", "surum": "v14", "tarih": datetime.now().isoformat(timespec="seconds"),
             "dosyalar": dahil}, ensure_ascii=False, indent=2))
    return tampon.getvalue(), dahil


def yedekten_geri_yukle(zip_bayt: bytes) -> tuple:
    """Zip içindeki beyaz listedeki JSON dosyalarını geri yükler → (yüklenenler, atlananlar, hata)."""
    try:
        z = zipfile.ZipFile(io.BytesIO(zip_bayt))
    except zipfile.BadZipFile:
        return [], [], "Bu dosya geçerli bir AREX yedeği (.zip) değil."
    yuklenecek, atlanan = {}, []
    for bilgi in z.infolist():
        ad = bilgi.filename
        if ad == "arex_yedek_bilgi.json" or bilgi.is_dir():
            continue
        if ad not in YEDEK_DOSYALARI or "/" in ad or "\\" in ad:
            atlanan.append(f"{ad} (izin verilen dosyalardan değil)")
            continue
        if bilgi.file_size > _EN_FAZLA_BAYT:
            atlanan.append(f"{ad} (çok büyük)")
            continue
        ham = z.read(bilgi)
        try:
            json.loads(ham.decode("utf-8"))
        except Exception:
            atlanan.append(f"{ad} (bozuk JSON)")
            continue
        yuklenecek[ad] = ham
    if not yuklenecek:
        return [], atlanan, "Yedekte geri yüklenebilecek dosya bulunamadı."
    # Mevcut dosyaların güvenlik kopyası
    kopya_dir = os.path.join(_KOK, "ar_acil_yedekler", "geri_yukleme_oncesi_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(kopya_dir, exist_ok=True)
    for ad in yuklenecek:
        yol = os.path.join(_KOK, ad)
        if os.path.isfile(yol):
            shutil.copy2(yol, os.path.join(kopya_dir, ad))
    for ad, ham in yuklenecek.items():
        gecici = os.path.join(_KOK, ad + ".gecici")
        with open(gecici, "wb") as f:
            f.write(ham)
        os.replace(gecici, os.path.join(_KOK, ad))  # yarım yazılmış dosya kalmaz
    return list(yuklenecek), atlanan, None


def yedekleme_paneli():
    """Yan menüde gösterilen yedekle / geri yükle paneli."""
    with st.expander("💾 Verilerimi Yedekle / Geri Yükle", expanded=False):
        st.caption("Bulutta uygulama yeniden başlayınca kayıtlar sıfırlanabilir. Ara sıra yedek indir; "
                   "gerekirse aynı dosyayı geri yükle.")
        if st.button("📦 Yedek Hazırla", use_container_width=True, key="arex_yedek_hazirla"):
            veri, dahil = yedek_zip_olustur()
            st.session_state["_arex_yedek_veri"] = (veri, dahil)
        if st.session_state.get("_arex_yedek_veri"):
            veri, dahil = st.session_state["_arex_yedek_veri"]
            st.download_button("⬇️ Yedeği İndir", data=veri, use_container_width=True, mime="application/zip",
                               file_name=f"arex_yedek_{datetime.now():%Y%m%d_%H%M}.zip", key="arex_yedek_indir")
            st.caption("İçerik: " + (", ".join(YEDEK_DOSYALARI[d] for d in dahil) if dahil else "henüz kayıt yok"))
        st.divider()
        yuklenen = st.file_uploader("Yedekten geri yükle (.zip)", type=["zip"], key="arex_yedek_yukle")
        if yuklenen is not None and st.button("♻️ Geri Yükle", use_container_width=True, key="arex_yedek_geri"):
            tamam, atlanan, hata = yedekten_geri_yukle(yuklenen.getvalue())
            if hata:
                st.error(hata)
            else:
                st.success("✅ Geri yüklendi: " + ", ".join(YEDEK_DOSYALARI[d] for d in tamam)
                           + ". Değişikliklerin görünmesi için sayfayı yenile.")
            if atlanan:
                st.warning("Atlananlar: " + "; ".join(atlanan))
