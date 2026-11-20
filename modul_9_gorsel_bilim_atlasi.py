# -*- coding: utf-8 -*-
"""
==============================================================================
MODÜL 9: GÖRSEL BİLİM İNSANLARI & İSLAM ÂLİMLERİ ATLASI (102 KİŞİ - v8.1)
Kronolojik Zaman Çizelgesi, Mobil Uyumlu SVG İnfografik Kartlar,
İlgili Bilim İnsanı Önerileri ve Adım Adım Keşif Yürüyüşü
==============================================================================
"""
import importlib.util
import os
import re
import sys
import time
import streamlit as st
import streamlit.components.v1 as components


def _guvenli_modul_yukle(modul_adi: str):
    if modul_adi in sys.modules:
        return sys.modules[modul_adi]
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    hedef_yol = os.path.join(mevcut_dizin, f"{modul_adi}.py")
    if os.path.exists(hedef_yol):
        spec = importlib.util.spec_from_file_location(modul_adi, hedef_yol)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[modul_adi] = mod
            spec.loader.exec_module(mod)
            return mod
    return None


m2_alimler = _guvenli_modul_yukle("modul_2_islam_alimleri")
ISLAM_ALIMLERI = getattr(m2_alimler, "ISLAM_ALIMLERI", {})


def _alan_ikon_ve_renk(alan: str):
    a = alan.lower()
    if any(k in a for k in ["fizik", "kuantum", "radyoaktivite", "elektrik", "kozmoloji"]):
        return "⚛️", "#38bdf8", "#0284c7", "atom"
    if any(k in a for k in ["matematik", "cebir", "geometri", "istatistik", "topoloji"]):
        return "📐", "#a78bfa", "#7c3aed", "math"
    if any(k in a for k in ["bilgisayar", "yapay zeka", "yazılım", "ağ", "kriptoloji"]):
        return "💻", "#34d399", "#059669", "code"
    if any(k in a for k in ["tıp", "cerrahi", "anatomi", "biyoloji", "mikrobiyoloji", "kimya"]):
        return "🧬", "#f472b6", "#db2777", "bio"
    if any(k in a for k in ["astronomi", "harita", "denizcilik", "coğrafya", "havacılık", "mühendislik", "robotik"]):
        return "🔭", "#fbbf24", "#d97706", "astro"
    return "📜", "#f59e0b", "#b45309", "scroll"


def _donem_yili_cikar(donem_str: str) -> int:
    s = donem_str.strip()
    m = re.search(r"(MÖ\s*)?(\d{3,4})", s, flags=re.IGNORECASE)
    if not m:
        return 1000
    yil = int(m.group(2))
    return -yil if m.group(1) else yil


def _cag_belirle(yil: int):
    if yil < 500:
        return 0, "Antik Çağ"
    if yil < 1450:
        return 1, "İslam Altın Çağı"
    if yil < 1850:
        return 2, "Bilimsel Devrim"
    return 3, "Modern Çağ"


def _svg_ikon_uret(tip: str, renk1: str, renk2: str) -> str:
    if tip == "atom":
        return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{renk1}"/><stop offset="100%" stop-color="{renk2}"/></linearGradient></defs>
          <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="url(#g1)" stroke-width="2.5"/>
          <ellipse cx="50" cy="50" rx="32" ry="12" fill="none" stroke="{renk1}" stroke-width="2" transform="rotate(30 50 50)"/>
          <ellipse cx="50" cy="50" rx="32" ry="12" fill="none" stroke="{renk1}" stroke-width="2" transform="rotate(-30 50 50)"/>
          <ellipse cx="50" cy="50" rx="32" ry="12" fill="none" stroke="{renk2}" stroke-width="2" transform="rotate(90 50 50)"/>
          <circle cx="50" cy="50" r="6" fill="#fde047"/>
        </svg>'''
    if tip == "math":
        return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="{renk1}" stroke-width="2.5"/>
          <polygon points="26,72 74,72 26,28" fill="none" stroke="{renk1}" stroke-width="2.5"/>
          <rect x="26" y="60" width="12" height="12" fill="none" stroke="{renk2}" stroke-width="2"/>
          <text x="58" y="42" fill="#f8fafc" font-size="18" font-family="serif" font-weight="bold">π ∑</text>
        </svg>'''
    if tip == "code":
        return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="{renk1}" stroke-width="2.5"/>
          <rect x="22" y="28" width="56" height="40" rx="6" fill="none" stroke="{renk1}" stroke-width="2.2"/>
          <text x="50" y="54" text-anchor="middle" fill="{renk1}" font-size="19" font-family="monospace" font-weight="bold">&lt;/&gt;</text>
          <line x1="36" y1="74" x2="64" y2="74" stroke="{renk2}" stroke-width="3" stroke-linecap="round"/>
        </svg>'''
    if tip == "bio":
        return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="{renk1}" stroke-width="2.5"/>
          <path d="M34,24 C66,36 34,64 66,76" fill="none" stroke="{renk1}" stroke-width="3"/>
          <path d="M66,24 C34,36 66,64 34,76" fill="none" stroke="{renk2}" stroke-width="3"/>
          <line x1="39" y1="34" x2="61" y2="34" stroke="#f8fafc" stroke-width="2"/>
          <line x1="39" y1="50" x2="61" y2="50" stroke="#f8fafc" stroke-width="2"/>
          <line x1="39" y1="66" x2="61" y2="66" stroke="#f8fafc" stroke-width="2"/>
        </svg>'''
    if tip == "astro":
        return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="{renk1}" stroke-width="2.5"/>
          <circle cx="50" cy="50" r="26" fill="none" stroke="{renk1}" stroke-width="1.8" stroke-dasharray="4 3"/>
          <circle cx="50" cy="50" r="9" fill="#fde047"/>
          <circle cx="72" cy="36" r="4.5" fill="{renk1}"/>
          <circle cx="28" cy="64" r="3.5" fill="#38bdf8"/>
        </svg>'''
    return f'''<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="46" fill="rgba(15,23,42,0.85)" stroke="{renk1}" stroke-width="2.5"/>
      <rect x="30" y="26" width="40" height="48" rx="5" fill="none" stroke="{renk1}" stroke-width="2.3"/>
      <line x1="38" y1="38" x2="62" y2="38" stroke="#f8fafc" stroke-width="2"/>
      <line x1="38" y1="48" x2="62" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <line x1="38" y1="58" x2="54" y2="58" stroke="{renk2}" stroke-width="2"/>
    </svg>'''


def bilim_insani_adimlari_olustur(bilgi: dict):
    ad = bilgi["ad"]
    donem = bilgi["donem"]
    alan = bilgi["alan"]
    eserler = bilgi["eserler"]
    ozet = bilgi["bilgi"]
    return [
        ("1️⃣ Doğum & Dönem", f"{ad}, {donem} yılları arasında yaşayarak çağının bilimsel atmosferine yön verdi."),
        ("2️⃣ Uzmanlık Alanı", f"Temel çalışma alanları: {alan}."),
        ("3️⃣ Başlıca Eser & Keşif", f"İnsanlığa bıraktığı en önemli miras: {eserler}."),
        ("4️⃣ Tarihe Etkisi", ozet),
    ]


def bilim_insani_gorsel_karti_ciz(bilgi: dict, aktif_adim: int = 4):
    ikon, r1, r2, tip = _alan_ikon_ve_renk(bilgi["alan"])
    svg_kod = _svg_ikon_uret(tip, r1, r2)
    adimlar = bilim_insani_adimlari_olustur(bilgi)
    yil = _donem_yili_cikar(bilgi["donem"])
    cag_idx, cag_ad = _cag_belirle(yil)

    caglar = ["Antik Çağ", "İslam Altın Çağı", "Bilimsel Devrim", "Modern Çağ"]
    zaman_cizelgesi_html = '<div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin:12px 0 14px 0; flex-wrap:wrap;">'
    for idx_c, c_isim in enumerate(caglar):
        aktif_c = idx_c == cag_idx
        c_bg = r1 if aktif_c else "rgba(148,163,184,0.14)"
        c_fg = "#03091a" if aktif_c else "#cbd5e1"
        c_fw = "800" if aktif_c else "500"
        zaman_cizelgesi_html += (
            f'<div style="flex:1; min-width:95px; text-align:center; padding:6px 8px; border-radius:999px; '
            f'background:{c_bg}; color:{c_fg}; font-size:11px; font-weight:{c_fw};">'
            f'{"📍 " if aktif_c else ""}{c_isim}</div>'
        )
    zaman_cizelgesi_html += "</div>"

    adim_html = ""
    for i, (baslik, metin) in enumerate(adimlar, 1):
        acik = i <= aktif_adim
        op = "1" if acik else "0.26"
        bg = "rgba(56,189,248,0.13)" if acik else "rgba(15,23,42,0.45)"
        bd = r1 if acik else "rgba(148,163,184,0.18)"
        adim_html += f'''
        <div style="opacity:{op}; background:{bg}; border:1px solid {bd}; border-radius:12px; padding:10px 12px; margin-bottom:8px; transition:opacity 0.3s ease;">
            <div style="font-weight:700; color:{r1}; font-size:13px;">{baslik}</div>
            <div style="color:#e2e8f0; font-size:13px; margin-top:3px; line-height:1.45;">{metin}</div>
        </div>'''

    html_kart = f'''
    <div style="font-family:'Inter',sans-serif; background:linear-gradient(135deg,#071329,#0b1d3d); border:1.5px solid {r1}; border-radius:18px; padding:18px; color:#f8fafc; box-shadow:0 12px 30px rgba(0,0,0,0.45);">
        <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
            <div>{svg_kod}</div>
            <div style="flex:1; min-width:200px;">
                <div style="font-size:12px; color:{r1}; font-weight:700; letter-spacing:0.4px;">{ikon} {bilgi['donem']} · {cag_ad} · {bilgi['alan']}</div>
                <div style="font-size:21px; font-weight:800; color:#ffffff; margin:4px 0;">{bilgi['ad']}</div>
                <div style="font-size:13px; color:#cbd5e1;">📚 <b>Eserler / Keşifler:</b> {bilgi['eserler']}</div>
            </div>
        </div>
        {zaman_cizelgesi_html}
        <div>{adim_html}</div>
    </div>
    '''
    components.html(html_kart, height=495, scrolling=True)


def _ilgili_kisileri_bul(secili_kod: str, limit: int = 3):
    hedef_tip = _alan_ikon_ve_renk(ISLAM_ALIMLERI[secili_kod]["alan"])[3]
    benzerler = []
    for k, v in ISLAM_ALIMLERI.items():
        if k == secili_kod:
            continue
        if _alan_ikon_ve_renk(v["alan"])[3] == hedef_tip:
            benzerler.append(k)
        if len(benzerler) >= limit:
            break
    return benzerler


def gorsel_bilim_atlasi_studyosu_goster(sesli_soyle_fn):
    st.subheader(f"🌌 Görsel Bilim İnsanları & İslam Âlimleri Atlası ({len(ISLAM_ALIMLERI)} Kişi)")
    st.caption("Marie Curie, Einstein, İbn Sînâ veya El-Cezerî seç; kronolojik zaman çizelgesi ve SVG görsel infografiklerle adım adım keşif yürüyüşüne çık!")

    if not ISLAM_ALIMLERI:
        st.warning("Bilim insanı veritabanı yüklenemedi.")
        return

    if "atlas_adim" not in st.session_state:
        st.session_state.atlas_adim = 4
    if "atlas_secili_kod" not in st.session_state:
        st.session_state.atlas_secili_kod = "marie_curie" if "marie_curie" in ISLAM_ALIMLERI else next(iter(ISLAM_ALIMLERI))

    f1, f2 = st.columns([2, 1])
    with f1:
        arama_q = st.text_input("🔎 Atlas İçinde Ara:", placeholder="Örn: Marie Curie, Fizik, Matematik, İbn Sina...", key="atlas_arama_in")
    with f2:
        kat_sec = st.selectbox("Kategori Filtresi:", ["Tümü", "İslam & Türk Bilginleri", "Yabancı Bilim İnsanları"], key="atlas_kat_sec")

    uygun_kodlar = []
    for k, v in ISLAM_ALIMLERI.items():
        yabanci_mi = "Yabancı" in v["ad"]
        if kat_sec == "İslam & Türk Bilginleri" and yabanci_mi:
            continue
        if kat_sec == "Yabancı Bilim İnsanları" and not yabanci_mi:
            continue
        if arama_q.strip():
            birlesik = f"{v['ad']} {v['alan']} {v['eserler']} {v['bilgi']}".lower()
            if arama_q.strip().lower() not in birlesik:
                continue
        uygun_kodlar.append(k)

    if not uygun_kodlar:
        st.info("Arama kriterine uygun kayıt bulunamadı; tüm liste gösteriliyor.")
        uygun_kodlar = list(ISLAM_ALIMLERI.keys())

    if st.session_state.atlas_secili_kod not in uygun_kodlar:
        st.session_state.atlas_secili_kod = uygun_kodlar[0]

    c1, c2 = st.columns([2, 1])
    with c1:
        secili_kod = st.selectbox(
            "🔭 Görsel Hikâyesini İncelemek İstediğin Bilim İnsanını Seç:",
            options=uygun_kodlar,
            index=uygun_kodlar.index(st.session_state.atlas_secili_kod),
            format_func=lambda k: f"{_alan_ikon_ve_renk(ISLAM_ALIMLERI[k]['alan'])[0]} {ISLAM_ALIMLERI[k]['ad']} ({ISLAM_ALIMLERI[k]['donem']})",
            key="atlas_kisi_sec_box",
        )
        st.session_state.atlas_secili_kod = secili_kod
    with c2:
        islam_say = sum(1 for v in ISLAM_ALIMLERI.values() if "Yabancı" not in v["ad"])
        yabanci_say = len(ISLAM_ALIMLERI) - islam_say
        st.metric("Toplam Atlas Kaydı", f"{len(ISLAM_ALIMLERI)} Kişi", f"{islam_say} İslam + {yabanci_say} Yabancı")

    secili_bilgi = ISLAM_ALIMLERI[secili_kod]

    b1, b2, b3, b4 = st.columns(4)
    if b1.button("⏮️ 1. Adımdan Başla", use_container_width=True, key="atlas_b1"):
        st.session_state.atlas_adim = 1
    if b2.button("🚶‍♂️ Bir Adım İlerle", use_container_width=True, key="atlas_b2"):
        st.session_state.atlas_adim = min(4, st.session_state.atlas_adim + 1)
    if b3.button("🌟 Tüm Hikâyeyi Aç", use_container_width=True, key="atlas_b3"):
        st.session_state.atlas_adim = 4
    with b4:
        if st.button("🔊 Sesli Anlat", use_container_width=True, key="atlas_ses"):
            metin = (
                f"{secili_bilgi['ad']}. {secili_bilgi['donem']} yılları arasında yaşamıştır. "
                f"Çalışma alanı {secili_bilgi['alan']}. Başlıca eserleri {secili_bilgi['eserler']}. {secili_bilgi['bilgi']}"
            )
            ses = sesli_soyle_fn(metin, "tr")
            if ses:
                st.audio(ses, format="audio/mp3")

    bilim_insani_gorsel_karti_ciz(secili_bilgi, aktif_adim=st.session_state.atlas_adim)

    # Aynı alandaki ilgili bilim insanlarına tek tıkla geçiş
    benzerler = _ilgili_kisileri_bul(secili_kod, limit=3)
    if benzerler:
        st.markdown("#### 🔗 Aynı Alandaki Diğer Öncü İsimler")
        bc = st.columns(len(benzerler))
        for idx_b, b_kod in enumerate(benzerler):
            b_ad = ISLAM_ALIMLERI[b_kod]["ad"].split("(")[0].strip()
            if bc[idx_b].button(f"➡️ {b_ad}", key=f"atlas_jump_{b_kod}", use_container_width=True):
                st.session_state.atlas_secili_kod = b_kod
                st.session_state.atlas_adim = 1
                st.rerun()