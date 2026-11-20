# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v4.0 — MODÜL 7: 9. SINIF TÜM DERS ÖZETLERİ, KİŞİSEL DERS NOTLARI VE
GÜNLÜK SORU ÇÖZÜM TAKİP MERKEZİ (modul_7_ders_ve_notlar.py)
==============================================================================
"""
from datetime import datetime
import json
import streamlit as st
import importlib.util
import os
import sys

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
if _MODUL_DIZINI not in sys.path:
    sys.path.insert(0, _MODUL_DIZINI)


def _guvenli_modul_yukle(modul_adi: str):
    if modul_adi in sys.modules and getattr(sys.modules[modul_adi], "__file__", None):
        return sys.modules[modul_adi]
    aday_yollar = [os.path.join(_MODUL_DIZINI, f"{modul_adi}.py")]
    for _ana in [_MODUL_DIZINI, os.path.dirname(_MODUL_DIZINI)]:
        for _kok, _altlar, _dosyalar in os.walk(_ana):
            _altlar[:] = [d for d in _altlar if not d.startswith(".") and d not in ("__pycache__", "venv", ".venv")]
            if f"{modul_adi}.py" in _dosyalar:
                tam = os.path.join(_kok, f"{modul_adi}.py")
                if tam not in aday_yollar:
                    aday_yollar.append(tam)
    for yol in aday_yollar:
        if os.path.exists(yol):
            spec = importlib.util.spec_from_file_location(modul_adi, yol)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[modul_adi] = mod
                spec.loader.exec_module(mod)
                return mod
    return __import__(modul_adi)

_m1 = _guvenli_modul_yukle("modul_1_arayuz_ve_tema")
DERS_NOTLARI_DOSYASI = _m1.DERS_NOTLARI_DOSYASI
SORU_TAKIP_DOSYASI = _m1.SORU_TAKIP_DOSYASI
bilgi_karti_olustur = _m1.bilgi_karti_olustur

DOKUZUNCU_SINIF_DERS_OZETLERI = {   '⚗️ Kimya (9. Sınıf)': {   'konular': 'Kimya Bilimi, Atom ve Periyodik Sistem, Kimyasal Türler '
                                          'Arası Etkileşimler, Maddenin Halleri',
                               'ozet': '• **Atom Yapısı:** `Kütle Numarası (A) = Proton (Z) + '
                                       'Nötrön (n)`. Nötr atomda `Proton = Elektron`.\n'
                                       '• **Periyodik Cetvel:** Soldan sağa gidildikçe atom çapı '
                                       'küçülür, iyonlaşma enerjisi (3A-2A ve 6A-5A küresel '
                                       'simetri istisnası hariç) ve elektronegatiflik artar.\n'
                                       '• **Güçlü Etkileşimler (Kimyasal Bağlar):** İyonik bağ '
                                       '(metal + ametal, elektron alışverişi), Kovalent bağ '
                                       '(ametal + ametal, elektron ortaklaşması) ve Metalik bağ.\n'
                                       '• **Zayıf Etkileşimler:** Hidrojen bağı (`H` atomunun `F, '
                                       'O, N` ile yaptığı güçlü fiziksel bağ) ve Van der Waals '
                                       'kuvvetleri.'},
    '⚡ Fizik (9. Sınıf)': {   'konular': 'Fizik Bilimine Giriş, Madde ve Özellikleri, Hareket ve '
                                         'Kuvvet, Enerji, Isı ve Sıcaklık, Elektrostatik',
                              'ozet': '• **Kuvvet & Hareket:** Yer değiştirme `Δx = x_son - '
                                      "x_ilk`, Hız `v = Δx / Δt`, İvme `a = Δv / Δt`, Newton'un 2. "
                                      'Yasası `F_net = m · a`.\n'
                                      '• **Madde ve Özkütle:** Özkütle `d = m / V` (Kütle / '
                                      'Hacim). Dayanıklılık `Kesit Alanı / Hacim` (`1/h`) ile '
                                      'orantılıdır.\n'
                                      '• **İş, Güç ve Enerji:** İş `W = F · Δx`, Güç `P = W / t`, '
                                      'Kinetik Enerji `E_k = ½ m v²`, Potansiyel Enerji `E_p = m g '
                                      'h`.\n'
                                      '• **Isı ve Sıcaklık:** `Q = m · c · ΔT` (Hal değişiminde `Q '
                                      '= m · L`).'},
    '🌍 Coğrafya (9. Sınıf)': {   'konular': "Doğa ve İnsan, Dünya'nın Şekli ve Hareketleri, "
                                            'Coğrafi Konum, Harita Bilgisi, İklim Bilgisi',
                                 'ozet': '• **Coğrafi Konum:** Paraleller (1° arası 111 km) ve '
                                         'Meridyenler (ardışık iki meridyen arası 4 dakika yerel '
                                         'saat farkı).\n'
                                         '• **Harita Bilgisi:** `Gerçek Uzunluk = Harita Uzunluğu '
                                         '× Ölçek Paydası`. Payda büyüdükçe ölçek küçülür.\n'
                                         '• **İklim Elemanları:** Sıcaklık, basınç ve rüzgârlar '
                                         '(Kayıp Sakal: Karayel, Yıldız, Poyraz - Samyeli, Kıble, '
                                         'Lodos), nem ve yağış.'},
    '💻 Bilişim Teknolojileri & Yazılım Mühendisliği (Proje Özel)': {   'konular': 'Algoritma '
                                                                                  'Tasarımı, '
                                                                                  'Python Veri '
                                                                                  'Yapıları, Nesne '
                                                                                  'Yönelimli '
                                                                                  'Programlama '
                                                                                  '(OOP), Gömülü '
                                                                                  'Sistemler '
                                                                                  '(Arduino/ESP32)',
                                                                       'ozet': '• **Veri '
                                                                               'Yapıları:** `dict` '
                                                                               '(Hash tablosu, '
                                                                               '`O(1)` arama '
                                                                               'hızı), `list` '
                                                                               '(dinamik dizi), '
                                                                               '`set` (benzersiz '
                                                                               'küme), `tuple` '
                                                                               '(değişmez dizi).\n'
                                                                               '• **Sensör & '
                                                                               'Kontrol:** HC-SR04 '
                                                                               'ultrasonik mesafe '
                                                                               '`d = (t × 0.034) / '
                                                                               '2`, PID kontrol '
                                                                               '`u(t) = Kp·e + '
                                                                               'Ki·∫e·dt + '
                                                                               'Kd·de/dt`.'},
    '📐 Matematik (9. Sınıf Proje Okulu)': {   'konular': 'Mantık, Kümeler, Denklemler ve '
                                                         'Eşitsizlikler, Üslü ve Köklü İfadeler, '
                                                         'Oran-Orantı, Üçgenler',
                                              'ozet': '• **Mantık:** `p ∧ q` (ve) sadece ikisi de '
                                                      "1 iken 1'dir; `p ∨ q` (veya) ikisi de 0 "
                                                      "iken 0'dır; `p ⇒ q ≡ p' ∨ q`.\n"
                                                      '• **Kümeler:** `s(A ∪ B) = s(A) + s(B) - '
                                                      's(A ∩ B)`. Alt küme sayısı `2ⁿ`, öz alt '
                                                      'küme sayısı `2ⁿ - 1`.\n'
                                                      '• **Üslü & Köklü Sayılar:** `aⁿ · aᵐ = '
                                                      'aⁿ⁺ᵐ`, `√(a²·b) = |a|√b`. Paydada kök varsa '
                                                      'eşleniğiyle çarpılır.\n'
                                                      '• **Üçgenler:** Pisagor `a² + b² = c²`; '
                                                      'açıortay, kenarortay (ağırlık merkezi `G`, '
                                                      '`k` ve `2k` oranı) ve benzerlik '
                                                      'teoremleri.'},
    '📖 Türk Dili ve Edebiyatı & Tarih (9. Sınıf)': {   'konular': 'Hikâye, Şiir, Masal/Fabl, '
                                                                  'Roman, İslamiyet Öncesi ve İlk '
                                                                  'Türk-İslam Devletleri Tarihi',
                                                       'ozet': '• **Edebiyat:** Olay hikâyesi '
                                                               '(Maupassant tarzı - Ömer '
                                                               'Seyfettin) ve Durum hikâyesi '
                                                               '(Çehov tarzı - Sait Faik, Memduh '
                                                               "Şevket Esendal). Mustafa Kutlu'nun "
                                                               '*Uzun Hikâye* eseri.\n'
                                                               '• **Tarih:** Tarih biliminin '
                                                               'yöntemi (Tarama, Tasnif, Tahlil, '
                                                               'Tenkit, Terkip), İlk Çağ '
                                                               'medeniyetleri, İslamiyet öncesi '
                                                               'Türk devletleri (Hun, Göktürk, '
                                                               'Uygur) ve Karahanlılar / '
                                                               'Gazneliler / Büyük Selçuklu '
                                                               'Devleti.'},
    '🕌 Din Kültürü ve Ahlak Bilgisi & Arapça (9. Sınıf)': {   'konular': "Bilgi ve İnanç, İslam'da "
                                                                         'Bilgi Kaynakları (Selim '
                                                                         'Akıl, Sadık Haber, Salim '
                                                                         'Duyular), İbadet, Ahlak '
                                                                         've Değerler',
                                                              'ozet': "• **İslam'da Bilgi "
                                                                      'Kaynakları:** 1) **Sadık '
                                                                      'Haber** (Vahiy ve Mütevatir '
                                                                      'Haber), 2) **Selim Akıl**, '
                                                                      '3) **Salim Duyular**.\n'
                                                                      '• **İman Esasları '
                                                                      "(Âmentü):** Allah'a, "
                                                                      'meleklerine, kitaplarına, '
                                                                      'peygamberlerine, ahiret '
                                                                      'gününe ve kaza/kadere '
                                                                      'iman.\n'
                                                                      "• **Mükellefiyet ve Ef'âl-i "
                                                                      'Mükellefîn:** Farz '
                                                                      '(Ayn/Kifaye), Vacip, Sünnet '
                                                                      '(Müekked/Gayri Müekked), '
                                                                      'Müstehap, Mübah, Mekruh, '
                                                                      'Haram.'},
    '🧬 Biyoloji (9. Sınıf)': {   'konular': 'Yaşam Bilimi Biyoloji, Canlıların Ortak Özellikleri, '
                                            'İnorganik/Organik Bileşikler, Hücre, Canlılar Dünyası',
                                 'ozet': '• **Organik Bileşikler:** Karbonhidratlar (glikozit '
                                         'bağı, 1. sırada enerji), Lipitler (ester bağı), '
                                         'Proteinler (amino asit + peptit bağı, yapıcı-onarıcı), '
                                         'Enzimler (aktivasyon enerjisini düşüren biyolojik '
                                         'katalizörler), ATP ve DNA/RNA.\n'
                                         '• **Hücre Organelleri:** **Ribozom** (zarsız, protein '
                                         'sentezi), **Mitokondri** (çift zarlı, oksijenli '
                                         'solunumla ATP üretimi), **Kloroplast** (fotosentez), '
                                         '**Golgi** (salgı ve paketleme), **Lizozom** (hücre içi '
                                         'sindirim).'}}

def ders_notlarini_oku():
    if os.path.exists(DERS_NOTLARI_DOSYASI):
        try:
            with open(DERS_NOTLARI_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {
            "ders": "Matematik",
            "baslik": "Köklü Sayılar ve Eşlenik Kuralları",
            "etiket": "Önemli Formül",
            "icerik": "√72 = 6√2. Paydada √a varsa √a ile, (√a - √b) varsa (√a + √b) ile çarpılır.",
            "tarih": "2026-11-16 14:00",
        },
        {
            "ders": "Fizik",
            "baslik": "Newton'un Hareket Yasaları & İHA Kuvvet Analizi",
            "etiket": "Sınav Notu",
            "icerik": "F_net = m.a formülünde İHA'nın yukarı ivmelenmesi için Toplam İtki > m.g olmalıdır.",
            "tarih": "2026-11-16 14:15",
        },
    ]


def ders_notu_kaydet(ders: str, baslik: str, etiket: str, icerik: str):
    mevcut = ders_notlarini_oku()
    mevcut.insert(
        0,
        {
            "ders": ders,
            "baslik": baslik.strip(),
            "etiket": etiket,
            "icerik": icerik.strip(),
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )
    with open(DERS_NOTLARI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(mevcut, f, ensure_ascii=False, indent=4)


def soru_takip_oku():
    if os.path.exists(SORU_TAKIP_DOSYASI):
        try:
            with open(SORU_TAKIP_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {"ders": "Matematik", "konu": "Köklü ve Üslü Sayılar", "soru_sayisi": 40, "sure_dk": 50, "tarih": "2026-11-16"},
        {"ders": "Fizik", "konu": "Hareket ve Kuvvet", "soru_sayisi": 25, "sure_dk": 35, "tarih": "2026-11-16"},
    ]


def soru_takip_ekle(ders: str, konu: str, soru_sayisi: int, sure_dk: int):
    kayitlar = soru_takip_oku()
    kayitlar.insert(
        0,
        {
            "ders": ders,
            "konu": konu.strip(),
            "soru_sayisi": int(soru_sayisi),
            "sure_dk": int(sure_dk),
            "tarih": datetime.now().strftime("%Y-%m-%d"),
        },
    )
    with open(SORU_TAKIP_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(kayitlar, f, ensure_ascii=False, indent=4)




def ders_ve_notlar_studyosu_goster(sesli_soyle_fn):
    st.subheader("📚 9. Sınıf Ders Özetleri, Kişisel Ders Notları & Soru Çözüm Takip Merkezi")
    d_tab1, d_tab2, d_tab3 = st.tabs([
        "📝 Ders Notlarım & Yeni Not Ekle",
        "📖 9. Sınıf Hızlı Ders & Formül Özetleri",
        "✅ Günlük Çalışılan Ders & Soru Takibi",
    ])

    with d_tab1:
        col_dn1, col_dn2 = st.columns([1.05, 1.45], gap="large")
        with col_dn1:
            st.markdown("#### ➕ Yeni Ders Notu Kaydet")
            with st.form("yeni_ders_notu_formu", clear_on_submit=True):
                sec_ders = st.selectbox(
                    "Ders Seç:",
                    ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türk Dili ve Edebiyatı", "Tarih", "Coğrafya", "Din Kültürü", "İngilizce", "Arapça", "Bilişim & Yazılım"],
                )
                sec_etiket = st.selectbox(
                    "Not Türü:",
                    ["📌 Sınavda Çıkar", "📐 Önemli Formül", "📝 Konu Özeti", "📚 Ödev / Tekrar"],
                )
                not_baslik = st.text_input("Konu Başlığı:", placeholder="Örn: Köklü Sayılarda Eşlenik")
                not_icerik = st.text_area("Ders Notun:", height=120, placeholder="Formülü, kuralı veya önemli noktayı buraya yaz...")
                if st.form_submit_button("💾 Ders Notunu Kaydet", use_container_width=True):
                    if not_baslik.strip() and not_icerik.strip():
                        ders_notu_kaydet(sec_ders, not_baslik, sec_etiket, not_icerik)
                        st.success(f"{sec_ders} notu başarıyla kaydedildi!")
                        st.rerun()
                    else:
                        st.warning("Lütfen konu başlığını ve not içeriğini doldur.")

        with col_dn2:
            st.markdown("#### 🗂️ Kayıtlı Ders Notlarım")
            tum_ders_notlari = ders_notlarini_oku()
            filtre_ders = st.selectbox(
                "Derse Göre Filtrele:",
                ["Tümü", "Matematik", "Fizik", "Kimya", "Biyoloji", "Türk Dili ve Edebiyatı", "Tarih", "Coğrafya", "Din Kültürü", "İngilizce", "Arapça", "Bilişim & Yazılım"],
            )
            for idx_dn, dn in enumerate(tum_ders_notlari):
                if filtre_ders != "Tümü" and dn["ders"] != filtre_ders:
                    continue
                st.markdown(
                    bilgi_karti_olustur(
                        f"📘 [{dn['ders']}] {dn['baslik']}",
                        f"{dn['etiket']} | 🕒 {dn['tarih']}",
                        dn["icerik"].replace("\n", "<br>"),
                    ),
                    unsafe_allow_html=True,
                )
                if st.button(f"🔊 Notu Sesli Dinle #{idx_dn + 1}", key=f"ders_not_dinle_{idx_dn}"):
                    sesli_soyle_fn(f"{dn['ders']} dersi, {dn['baslik']}. {dn['icerik']}", dil="tr")

    with d_tab2:
        secili_ozet_ders = st.selectbox("9. Sınıf Ders Özeti Seç:", list(DOKUZUNCU_SINIF_DERS_OZETLERI.keys()))
        ozet_veri = DOKUZUNCU_SINIF_DERS_OZETLERI[secili_ozet_ders]
        st.markdown(
            bilgi_karti_olustur(
                secili_ozet_ders,
                f"📚 Müfredat Konuları: {ozet_veri['konular']}",
                ozet_veri["ozet"].replace("\n", "<br>"),
            ),
            unsafe_allow_html=True,
        )
        if st.button("🔊 Bu Ders Özetini Sesli Anlat"):
            sesli_soyle_fn(ozet_veri["ozet"], dil="tr")

    with d_tab3:
        kayitlar = soru_takip_oku()
        toplam_soru = sum(k.get("soru_sayisi", 0) for k in kayitlar)
        toplam_dk = sum(k.get("sure_dk", 0) for k in kayitlar)
        sk1, sk2, sk3 = st.columns(3)
        sk1.metric("Toplam Çözülen Soru", f"{toplam_soru} Soru", "Aktif Takip")
        sk2.metric("Toplam Çalışma Süresi", f"{toplam_dk} Dakika", f"{toplam_dk / 60:.1f} Saat")
        sk3.metric("Kayıtlı Çalışma Oturumu", f"{len(kayitlar)} Oturum", "9. Sınıf")

        c_st1, c_st2 = st.columns([1.0, 1.4], gap="large")
        with c_st1:
            with st.form("soru_takip_formu", clear_on_submit=True):
                st_ders = st.selectbox("Çalışılan Ders:", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Edebiyat", "Tarih", "Coğrafya", "İngilizce", "Arapça"])
                st_konu = st.text_input("Çalışılan Konu:", placeholder="Örn: Üslü Sayılar Test Çözümü")
                st_soru = st.number_input("Çözülen Soru Sayısı:", min_value=1, max_value=500, value=25, step=5)
                st_sure = st.number_input("Çalışma Süresi (Dakika):", min_value=5, max_value=600, value=40, step=5)
                if st.form_submit_button("➕ Çalışmayı Kaydet", use_container_width=True):
                    soru_takip_ekle(st_ders, st_konu or "Genel Tekrar", st_soru, st_sure)
                    st.success("Çalışma kaydı eklendi Ahmet!")
                    st.rerun()
        with c_st2:
            for k_item in kayitlar[:10]:
                st.markdown(
                    bilgi_karti_olustur(
                        f"✅ {k_item['ders']} — {k_item['konu']}",
                        f"📅 {k_item['tarih']} | ⏱️ {k_item['sure_dk']} dk",
                        f"Bu oturumda **{k_item['soru_sayisi']} soru** çözüldü.",
                    ),
                    unsafe_allow_html=True,
                )


def pomodoro_ve_canli_calisma_yeri_goster():
    """
    v13.0 — PREMIUM GÖRSEL POMODORO, 5 BİLİMSEL ÇALIŞMA TEKNİĞİ & CANLI ÇALIŞMA YERİ:
      • Sade ve premium 5'li teknik kutucuk seçici (Klasik 25/5, 52/17 Derin Odak,
        90/20 Ultradian, Feynman 20/5, Aktif Hatırlama 15/3 + Özel Süre)
      • Dairesel animasyonlu SVG halka geri sayım sayacı (Glassmorphism Asil Lacivert)
      • Yerleşik Web Audio API odak ortam sesi (Sessiz / Hafif Yağmur / Kahverengi Gürültü)
      • Temiz 3 adımlı mantık akışı: Teknik Seç -> Canlı Sayaç & Görevler -> Not & Özet
    """
    import streamlit.components.v1 as _st_comp

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#0b132b 0%,#162447 55%,#1b3a5c 100%);
                    border:1px solid rgba(56,189,248,0.28);border-radius:18px;
                    padding:20px 24px;margin-bottom:16px;
                    box-shadow:0 10px 28px rgba(2,6,23,0.45);">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
                <div>
                    <div style="font-size:12px;letter-spacing:1.6px;color:#38bdf8;font-weight:700;text-transform:uppercase;">
                        AREX PREMIUM ODAK STÜDYOSU
                    </div>
                    <div style="font-size:24px;font-weight:800;color:#f8fafc;margin-top:2px;">
                        🍅 Pomodoro & Canlı Çalışma Yeri
                    </div>
                    <div style="font-size:13.5px;color:#cbd5e1;margin-top:4px;">
                        1) Tekniğini seç  •  2) Dairesel canlı sayacı başlat  •  3) Görevlerini tikle ve notunu kaydet
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Oturum durumlarını güvenle hazırla
    if "canli_calisma_gorevler" not in st.session_state:
        st.session_state["canli_calisma_gorevler"] = [
            {"metin": "9. sınıf Matematik 20 çözümlü soru", "tamam": False},
            {"metin": "Günlük konu özeti ve tekrar", "tamam": False},
            {"metin": "TEKNOFEST / yazılım proje oturumu", "tamam": False},
        ]
    if "pomodoro_tamamlanan_tur" not in st.session_state:
        st.session_state["pomodoro_tamamlanan_tur"] = 0
    if "pomodoro_toplam_dk" not in st.session_state:
        st.session_state["pomodoro_toplam_dk"] = 0
    if "pomo_aktif_teknik" not in st.session_state:
        st.session_state["pomo_aktif_teknik"] = "klasik"

    # 5 Bilimsel Çalışma Tekniği (Sade & Premium Kutucuk Mimarisi)
    teknikler = [
        {
            "kod": "klasik",
            "ikon": "🍅",
            "ad": "Klasik Pomodoro",
            "odak": 25,
            "mola": 5,
            "etiket": "25 / 5 dk",
            "aciklama": "Günlük tekrar ve dengeli odaklanma",
            "ipucu": "25 dk boyunca sadece tek derse odaklan, 5 dk ekrandan uzaklaş.",
            "renk": "#38bdf8",
        },
        {
            "kod": "derin_52",
            "ikon": "🧠",
            "ad": "52 / 17 Derin Odak",
            "odak": 52,
            "mola": 17,
            "etiket": "52 / 17 dk",
            "aciklama": "Matematik, fizik ve ağır konular",
            "ipucu": "Derin problem çözümü ve uzun kodlama için bilimsel en verimli blok.",
            "renk": "#818cf8",
        },
        {
            "kod": "ultradian",
            "ikon": "⚡",
            "ad": "90 / 20 Ultradian",
            "odak": 90,
            "mola": 20,
            "etiket": "90 / 20 dk",
            "aciklama": "Deneme sınavı & proje maratonu",
            "ipucu": "İnsan beyninin doğal 90 dakikalık yüksek odak ritmine göre çalış.",
            "renk": "#f59e0b",
        },
        {
            "kod": "feynman",
            "ikon": "🎯",
            "ad": "Feynman Tekniği",
            "odak": 20,
            "mola": 5,
            "etiket": "20 / 5 dk",
            "aciklama": "Kendi cümlenle anlatarak öğren",
            "ipucu": "15 dk konuyu oku, son 5 dk bir arkadaşına anlatır gibi not defterine özetle.",
            "renk": "#34d399",
        },
        {
            "kod": "aktif_hatirlama",
            "ikon": "🔁",
            "ad": "Aktif Hatırlama",
            "odak": 15,
            "mola": 3,
            "etiket": "15 / 3 dk",
            "aciklama": "Hızlı formül & soru sprinti",
            "ipucu": "Defteri kapat, aklında kalan formülleri ve soruları yüksek hızla test et.",
            "renk": "#f472b6",
        },
    ]

    # ADIM 1: SADE & PREMİUM TEKNİK KUTUCUKLARI
    st.markdown("#### 1️⃣ Çalışma Tekniğini Seç")
    t_cols = st.columns(5, gap="small")
    for idx, tk in enumerate(teknikler):
        secili_mi = (st.session_state["pomo_aktif_teknik"] == tk["kod"])
        border_c = tk["renk"] if secili_mi else "rgba(148,163,184,0.22)"
        bg_c = "linear-gradient(160deg,rgba(30,41,59,0.95),rgba(15,23,42,0.98))" if secili_mi else "rgba(15,23,42,0.72)"
        glow = f"0 0 18px {tk['renk']}33" if secili_mi else "none"
        with t_cols[idx]:
            st.markdown(
                f"""
                <div style="background:{bg_c};border:1.5px solid {border_c};border-radius:14px;
                            padding:12px 10px;text-align:center;min-height:112px;
                            box-shadow:{glow};margin-bottom:6px;">
                    <div style="font-size:22px;line-height:1.1;">{tk['ikon']}</div>
                    <div style="font-size:13px;font-weight:700;color:#f8fafc;margin-top:5px;">{tk['ad']}</div>
                    <div style="display:inline-block;margin-top:5px;padding:2px 8px;border-radius:99px;
                                font-size:11px;font-weight:700;background:{tk['renk']}22;color:{tk['renk']};">
                        {tk['etiket']}
                    </div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:6px;line-height:1.3;">{tk['aciklama']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            btn_lbl = "✓ Aktif" if secili_mi else "Seç"
            if st.button(btn_lbl, key=f"pomo_tk_btn_{tk['kod']}", use_container_width=True):
                st.session_state["pomo_aktif_teknik"] = tk["kod"]
                st.rerun()

    aktif_tk = next((t for t in teknikler if t["kod"] == st.session_state["pomo_aktif_teknik"]), teknikler[0])

    # ADIM 2: SOLDA PREMİUM DAİRESEL SVG SAYAÇ, SAĞDA CANLI ÇALIŞMA MASASI
    col_sol, col_sag = st.columns([1.15, 1.0], gap="large")

    with col_sol:
        faz_sec = st.radio(
            "Aktif Faz:",
            [
                f"🎯 Odak ({aktif_tk['odak']} dk)",
                f"☕ Mola ({aktif_tk['mola']} dk)",
                "⚙️ Özel Süre",
            ],
            horizontal=True,
            key="pomo_faz_radio",
        )
        if faz_sec.startswith("🎯"):
            sure_dk = int(aktif_tk["odak"])
            faz_renk = aktif_tk["renk"]
            faz_etiket = f"{aktif_tk['ikon']} {aktif_tk['ad']} — ODAK"
        elif faz_sec.startswith("☕"):
            sure_dk = int(aktif_tk["mola"])
            faz_renk = "#22c55e"
            faz_etiket = f"☕ {aktif_tk['ad']} — MOLA"
        else:
            sure_dk = int(st.number_input("Özel Dakika:", min_value=1, max_value=180, value=30, step=5, key="pomo_ozel_dk_v13"))
            faz_renk = "#38bdf8"
            faz_etiket = f"⚙️ ÖZEL ODAK ({sure_dk} DK)"

        pomo_svg_html = f"""
        <div style="background:radial-gradient(circle at top,#1e293b 0%,#0b132b 75%);
                    border:1px solid rgba(56,189,248,0.28);border-radius:22px;
                    padding:24px 20px;text-align:center;color:#f8fafc;
                    font-family:'Inter',system-ui,sans-serif;
                    box-shadow:0 16px 36px rgba(2,6,23,0.55);">
          <div style="display:inline-block;padding:4px 14px;border-radius:99px;
                      background:{faz_renk}22;border:1px solid {faz_renk}55;
                      color:{faz_renk};font-size:12px;font-weight:700;letter-spacing:1px;">
            {faz_etiket}
          </div>

          <div style="position:relative;width:216px;height:216px;margin:18px auto 14px auto;">
            <svg width="216" height="216" viewBox="0 0 216 216" style="transform:rotate(-90deg);">
              <circle cx="108" cy="108" r="94" fill="none" stroke="rgba(148,163,184,0.16)" stroke-width="10"/>
              <circle id="ringProg" cx="108" cy="108" r="94" fill="none" stroke="{faz_renk}" stroke-width="10"
                      stroke-linecap="round" stroke-dasharray="590.6" stroke-dashoffset="0"
                      style="transition:stroke-dashoffset 0.6s ease;filter:drop-shadow(0 0 8px {faz_renk}88);"/>
            </svg>
            <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <div id="pomoClock" style="font-size:48px;font-weight:800;letter-spacing:2px;font-variant-numeric:tabular-nums;color:#ffffff;">
                {sure_dk:02d}:00
              </div>
              <div id="pomoPct" style="font-size:12px;color:#94a3b8;margin-top:2px;">%100 kalan</div>
            </div>
          </div>

          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;">
            <button onclick="pomoStart()" style="background:linear-gradient(135deg,#22c55e,#16a34a);color:#ffffff;border:none;border-radius:12px;padding:10px 22px;font-weight:700;font-size:14px;cursor:pointer;box-shadow:0 4px 14px rgba(34,197,94,0.35);">▶ Başlat</button>
            <button onclick="pomoPause()" style="background:rgba(245,158,11,0.18);color:#fbbf24;border:1px solid rgba(245,158,11,0.45);border-radius:12px;padding:10px 18px;font-weight:700;font-size:14px;cursor:pointer;">⏸ Duraklat</button>
            <button onclick="pomoReset()" style="background:rgba(148,163,184,0.14);color:#e2e8f0;border:1px solid rgba(148,163,184,0.32);border-radius:12px;padding:10px 18px;font-weight:700;font-size:14px;cursor:pointer;">↺ Sıfırla</button>
          </div>

          <div style="display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap;margin-bottom:10px;">
            <span style="font-size:12px;color:#94a3b8;">🎧 Odak Sesi:</span>
            <button id="sndOff" onclick="setAmbient('off')" style="background:#334155;color:#f8fafc;border:1px solid #475569;border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer;">Sessiz</button>
            <button id="sndRain" onclick="setAmbient('rain')" style="background:transparent;color:#94a3b8;border:1px solid #334155;border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer;">🌧️ Yağmur</button>
            <button id="sndBrown" onclick="setAmbient('brown')" style="background:transparent;color:#94a3b8;border:1px solid #334155;border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer;">🌊 Derin Odak</button>
          </div>

          <div id="pomoStatus" style="font-size:12.5px;color:#cbd5e1;">💡 {aktif_tk['ipucu']}</div>
        </div>
        <script>
          const totalSec = {sure_dk * 60};
          const circ = 590.6;
          let rem = totalSec;
          let timer = null;
          let ambCtx = null, ambNode = null;

          function fmt(s) {{
            const m = Math.floor(s / 60);
            const r = s % 60;
            return String(m).padStart(2,'0') + ':' + String(r).padStart(2,'0');
          }}
          function render() {{
            document.getElementById('pomoClock').innerText = fmt(rem);
            const ratio = Math.max(0, rem / totalSec);
            document.getElementById('ringProg').style.strokeDashoffset = (circ * (1 - ratio)).toFixed(1);
            document.getElementById('pomoPct').innerText = '%' + Math.round(ratio * 100) + ' kalan';
          }}
          function chime() {{
            try {{
              const ctx = new (window.AudioContext || window.webkitAudioContext)();
              [523.25, 659.25, 783.99].forEach((freq, i) => {{
                const o = ctx.createOscillator();
                const g = ctx.createGain();
                o.type = 'sine'; o.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.16);
                g.gain.setValueAtTime(0.12, ctx.currentTime + i * 0.16);
                g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.16 + 0.45);
                o.connect(g); g.connect(ctx.destination);
                o.start(ctx.currentTime + i * 0.16);
                o.stop(ctx.currentTime + i * 0.16 + 0.48);
              }});
            }} catch(e) {{}}
          }}
          function setAmbient(mode) {{
            if (ambNode) {{ try {{ ambNode.disconnect(); }} catch(e) {{}} ambNode = null; }}
            if (ambCtx) {{ try {{ ambCtx.close(); }} catch(e) {{}} ambCtx = null; }}
            ['sndOff','sndRain','sndBrown'].forEach(id => {{
              const el = document.getElementById(id);
              if (el) {{ el.style.background = 'transparent'; el.style.color = '#94a3b8'; }}
            }});
            const activeId = mode === 'rain' ? 'sndRain' : (mode === 'brown' ? 'sndBrown' : 'sndOff');
            const aEl = document.getElementById(activeId);
            if (aEl) {{ aEl.style.background = '#334155'; aEl.style.color = '#f8fafc'; }}
            if (mode === 'off') return;
            try {{
              ambCtx = new (window.AudioContext || window.webkitAudioContext)();
              const bufSize = 2 * ambCtx.sampleRate;
              const buf = ambCtx.createBuffer(1, bufSize, ambCtx.sampleRate);
              const out = buf.getChannelData(0);
              let last = 0.0;
              for (let i = 0; i < bufSize; i++) {{
                const w = Math.random() * 2 - 1;
                if (mode === 'brown') {{
                  out[i] = (last + 0.02 * w) / 1.02;
                  last = out[i];
                  out[i] *= 0.25;
                }} else {{
                  out[i] = w * 0.04;
                }}
              }}
              const src = ambCtx.createBufferSource();
              src.buffer = buf; src.loop = true;
              const filter = ambCtx.createBiquadFilter();
              filter.type = 'lowpass';
              filter.frequency.value = mode === 'brown' ? 420 : 1200;
              const gain = ambCtx.createGain();
              gain.gain.value = 0.22;
              src.connect(filter); filter.connect(gain); gain.connect(ambCtx.destination);
              src.start();
              ambNode = src;
            }} catch(e) {{}}
          }}
          function pomoStart() {{
            if (timer) return;
            document.getElementById('pomoStatus').innerText = '🔥 Odak akışı aktif — bildirimleri sustur ve sadece bu bloğa odaklan.';
            timer = setInterval(() => {{
              if (rem > 0) {{ rem--; render(); }}
              else {{
                clearInterval(timer); timer = null; chime();
                document.getElementById('pomoStatus').innerText = '🎉 Oturum tamamlandı! Alttan turu kaydedip mola ver.';
              }}
            }}, 1000);
          }}
          function pomoPause() {{
            if (timer) {{ clearInterval(timer); timer = null; document.getElementById('pomoStatus').innerText = '⏸ Duraklatıldı.'; }}
          }}
          function pomoReset() {{
            pomoPause(); rem = totalSec; render();
            document.getElementById('pomoStatus').innerText = '↺ Sayaç sıfırlandı.';
          }}
        </script>
        """
        _st_comp.html(pomo_svg_html, height=430)

        k1, k2, k3 = st.columns(3)
        k1.metric("🏆 Tamamlanan Tur", f"{st.session_state['pomodoro_tamamlanan_tur']}")
        k2.metric("⏳ Toplam Odak", f"{st.session_state['pomodoro_toplam_dk']} dk")
        k3.metric("🎯 Aktif Teknik", aktif_tk["etiket"])

        if st.button("✅ Bu Oturumu Tamamladım (+Kaydet)", use_container_width=True, key="pomo_tur_kaydet_v13"):
            st.session_state["pomodoro_tamamlanan_tur"] += 1
            st.session_state["pomodoro_toplam_dk"] += sure_dk
            try:
                soru_takip_ekle("Pomodoro Odak", f"{aktif_tk['ad']} ({sure_dk} dk)", 0, sure_dk)
            except Exception:
                pass
            st.success(f"🎉 Harika! {st.session_state['pomodoro_tamamlanan_tur']}. oturum ({sure_dk} dk) kaydedildi.")
            st.rerun()

    with col_sag:
        st.markdown("#### 2️⃣ Canlı Görev Listesi")
        g_inp1, g_inp2 = st.columns([0.76, 0.24])
        with g_inp1:
            yeni_gorev = st.text_input("Görev", label_visibility="collapsed", placeholder="Yeni hedef yaz (Örn: 20 Matematik sorusu)...", key="calisma_yeni_gorev_v13")
        with g_inp2:
            if st.button("➕ Ekle", use_container_width=True, key="calisma_gorev_ekle_v13"):
                if yeni_gorev.strip():
                    st.session_state["canli_calisma_gorevler"].append({"metin": yeni_gorev.strip(), "tamam": False})
                    st.rerun()

        gorevler = st.session_state["canli_calisma_gorevler"]
        tamam_say = sum(1 for g in gorevler if g["tamam"])
        if gorevler:
            st.progress(tamam_say / len(gorevler), text=f"Günlük Görev İlerlemesi: {tamam_say} / {len(gorevler)}")
        for idx, g in enumerate(gorevler):
            gc1, gc2 = st.columns([0.86, 0.14])
            with gc1:
                gorevler[idx]["tamam"] = st.checkbox(g["metin"], value=g["tamam"], key=f"gorev_chk_v13_{idx}")
            with gc2:
                if st.button("🗑️", key=f"gorev_sil_v13_{idx}"):
                    gorevler.pop(idx)
                    st.rerun()

        st.markdown("#### 3️⃣ Hızlı Çalışma Notu (Feynman / Özet)")
        with st.form("canli_calisma_not_formu_v13", clear_on_submit=True):
            c_ders = st.selectbox("Ders / Alan:", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih", "TEKNOFEST / Yazılım", "Genel"], key="calisma_not_ders_v13")
            c_baslik = st.text_input("Not Başlığı:", placeholder="Örn: Kümeler & Mantık Özeti")
            c_icerik = st.text_area("Çalışma Notun:", height=120, placeholder="Öğrendiğin formülleri veya Feynman özetini buraya yaz...")
            if st.form_submit_button("💾 Kalıcı Deftere Kaydet", use_container_width=True):
                if c_baslik.strip() and c_icerik.strip():
                    ders_notu_kaydet(c_ders, c_baslik.strip(), f"Odak ({aktif_tk['ad']})", c_icerik.strip())
                    st.success("✅ Çalışma notun kalıcı deftere kaydedildi!")
                else:
                    st.warning("Başlık ve not içeriğini doldur.")
