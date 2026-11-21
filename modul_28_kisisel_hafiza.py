# -*- coding: utf-8 -*-
"""
AREX — Modül 28: 🧠 KİŞİSEL HAFIZA & PROFİL
==============================================================================
• Kullanıcı profili (ad, okul/sınıf, ilgi alanları, hedefler, projeler, cevap tarzı tercihi …)
• Sohbetten otomatik öğrenme: "benim adım …", "… seviyorum", "doğum günüm …", "hatırla: …"
• Her yapay zekâ isteğine kısa bir "kullanıcıyı tanı" özeti eklenir → daha kişisel, tutarlı sohbet.
• Dosya: arex_profil.json (kişisel veri; git'e gitmez).
• Ayrıca istek bazında "yabancı dil serbest" bayrağı: kullanıcı başka dilde yazdıysa ya da çeviri/
  yabancı dilde hikâye istediyse Türkçe kilidi devre dışı kalır.
"""
import json
import os
import re
import time

_PROJE = os.path.dirname(os.path.abspath(__file__))
PROFIL_DOSYASI = os.path.join(_PROJE, "arex_profil.json")

VARSAYILAN_PROFIL = {
    "ad": "Ahmet",
    "hakkinda": "İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi. TEKNOFEST İHA ve "
                "TÜBİTAK akıllı bebek arabası projeleri geliştiriyor.",
    "ilgi_alanlari": "yapay zekâ, İHA, robotik, matematik, yazılım",
    "hedefler": "",
    "cevap_tarzi": "samimi, net, gerektiğinde detaylı",
    "diller": "Türkçe, İngilizce, Arapça, Bengalce",
    "notlar": [],  # [{"metin": "...", "tarih": "..."}]
}

FIELD_ADLARI = {
    "ad": "👤 Adın", "hakkinda": "📝 Kendinden kısaca bahset", "ilgi_alanlari": "💡 İlgi alanların",
    "hedefler": "🎯 Hedeflerin", "cevap_tarzi": "🗣️ Nasıl cevap vereyim?", "diller": "🌍 Bildiğin / öğrendiğin diller",
}


def profil_oku() -> dict:
    p = json.loads(json.dumps(VARSAYILAN_PROFIL))
    try:
        with open(PROFIL_DOSYASI, "r", encoding="utf-8") as f:
            veri = json.load(f)
        if isinstance(veri, dict):
            p.update(veri)
    except Exception:
        pass
    if not isinstance(p.get("notlar"), list):
        p["notlar"] = []
    return p


def profil_kaydet(p: dict) -> None:
    try:
        gecici = PROFIL_DOSYASI + ".tmp"
        with open(gecici, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        os.replace(gecici, PROFIL_DOSYASI)
    except Exception:
        pass


def not_ekle(metin: str) -> bool:
    metin = re.sub(r"\s+", " ", (metin or "")).strip(" .!")
    if len(metin) < 3:
        return False
    p = profil_oku()
    kucuk = metin.lower()
    if any(n.get("metin", "").lower() == kucuk for n in p["notlar"]):
        return False
    p["notlar"].append({"metin": metin[:200], "tarih": time.strftime("%d.%m.%Y")})
    p["notlar"] = p["notlar"][-60:]
    profil_kaydet(p)
    return True


def not_sil(indeks: int) -> None:
    p = profil_oku()
    if 0 <= indeks < len(p["notlar"]):
        p["notlar"].pop(indeks)
        profil_kaydet(p)


# ------------------------------------------------------------------------------
# Sohbetten otomatik öğrenme (yalnızca açık, birinci tekil şahıs ifadeleri)
# ------------------------------------------------------------------------------
_OGRENME_KALIPLARI = [
    (r"^(?:hatırla|hatirla|unutma|aklında tut|aklinda tut)\s*[:\-,]?\s*(.{3,180})$", "{0}"),
    (r"\b(?:benim adım|benim adim|adım|adim)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,20})\b(?!\s*(?:ne|nedir))", "Adı: {0}"),
    (r"\b(?:doğum günüm|dogum gunum)\s+(.{3,40}?)(?:[.!,]|$)", "Doğum günü: {0}"),
    (r"\b(?:en sevdiğim|en sevdigim|favori)\s+([a-zçğıöşü ]{2,25}?)\s+(.{2,40}?)(?:[.!,]|$)", "En sevdiği {0}: {1}"),
    (r"^(?:ben\s+)?(.{3,40}?)\s+(?:çok\s+)?(?:seviyorum|bayılırım|bayiliyorum|bayılıyorum)(?:[.!]|$)", "Sevdiği şey: {0}"),
    (r"^(?:ben\s+)?(.{3,40}?)\s+(?:sevmem|sevmiyorum|nefret ediyorum)(?:[.!]|$)", "Sevmediği şey: {0}"),
    (r"\b(?:ben|şu an|su an)\s+(\d{1,2})\.?\s*sınıf(?:tayım|ta okuyorum)", "{0}. sınıf öğrencisi"),
    (r"\b(\d{1,2})\s*yaşındayım\b", "{0} yaşında"),
]


def sohbetten_ogren(mesaj: str) -> str:
    """Mesajda kişisel bir bilgi varsa hafızaya ekler, eklediği notu döndürür (yoksa '')."""
    t = (mesaj or "").strip()
    if not t or len(t) > 220 or "?" in t:
        return ""
    for desen, sablon in _OGRENME_KALIPLARI:
        m = re.search(desen, t, flags=re.IGNORECASE)
        if m:
            parcalar = [g.strip() for g in m.groups()]
            if any(len(g) < 2 for g in parcalar):
                continue
            notu = sablon.format(*parcalar)
            if notu.startswith("Adı: "):
                p = profil_oku()
                p["ad"] = parcalar[0]
                profil_kaydet(p)
            return notu if not_ekle(notu) else ""
    return ""


def profil_ozeti(maks: int = 900) -> str:
    p = profil_oku()
    satirlar = []
    if p.get("ad"):
        satirlar.append(f"Adı: {p['ad']}")
    for alan, etiket in (("hakkinda", "Hakkında"), ("ilgi_alanlari", "İlgi alanları"), ("hedefler", "Hedefleri"),
                         ("diller", "Diller"), ("cevap_tarzi", "Tercih ettiği cevap tarzı")):
        if str(p.get(alan, "")).strip():
            satirlar.append(f"{etiket}: {str(p[alan]).strip()}")
    notlar = [n.get("metin", "") for n in p.get("notlar", [])][-15:]
    if notlar:
        satirlar.append("Kendisi hakkında söyledikleri: " + "; ".join(notlar))
    return " | ".join(satirlar)[:maks]


def sistem_eki() -> str:
    oz = profil_ozeti()
    if not oz:
        return ""
    return ("\n\nKULLANICIYI TANI (bunu doğal kullan; her cevapta tekrar etme, yalnızca ilgili olduğunda "
            f"kişiselleştir): {oz}")


# ------------------------------------------------------------------------------
# Yabancı dil serbestliği (Türkçe kilidini istek bazında kapatır)
# ------------------------------------------------------------------------------
_YABANCI_DIL_ISTEGI = re.compile(
    r"ingilizce|english|arapça|arapca|rusça|rusca|bengalce|bangla|almanca|fransızca|fransizca|ispanyolca|"
    r"japonca|çince|cince|urduca|hintçe|farsça|azerice|italyanca|portekizce|korece|çevir|cevir|translate|"
    r"tercüme|tercume|in english|dilinde|diline", re.IGNORECASE)


def yabanci_dil_serbest_mi(mesaj: str, hedef_dil: str = "tr") -> bool:
    if hedef_dil and hedef_dil != "tr":
        return True
    try:
        import modul_25_ai_cekirdek as ai
        tahmin = ai.yazidan_dil_tahmin(mesaj)
    except Exception:
        tahmin = ""
    if tahmin and tahmin != "tr":
        return True
    return bool(_YABANCI_DIL_ISTEGI.search(mesaj or ""))


# ------------------------------------------------------------------------------
# Streamlit paneli
# ------------------------------------------------------------------------------
def hafiza_paneli():
    import streamlit as st

    st.markdown("### 🧠 Beni Tanı — Kişisel Hafıza")
    st.caption("AREX bu bilgileri her sohbette dikkate alır; sohbette 'hatırla: …' yazarak da ekleyebilirsin. "
               "Veriler yalnızca bu cihazda (arex_profil.json) tutulur.")
    p = profil_oku()
    with st.form("m28_profil"):
        yeni = {}
        for alan, etiket in FIELD_ADLARI.items():
            if alan == "hakkinda":
                yeni[alan] = st.text_area(etiket, value=p.get(alan, ""), height=90)
            else:
                yeni[alan] = st.text_input(etiket, value=p.get(alan, ""))
        if st.form_submit_button("💾 Kaydet", use_container_width=True, type="primary"):
            p.update(yeni)
            profil_kaydet(p)
            st.success("Kaydedildi! Artık seni daha iyi tanıyorum. 💙")
    st.markdown("#### 📌 Öğrendiklerim")
    if not p["notlar"]:
        st.info("Henüz not yok. Sohbette 'hatırla: matematik sınavım 12 Aralık'ta' gibi yazabilirsin.")
    for i, n in enumerate(reversed(p["notlar"])):
        gercek = len(p["notlar"]) - 1 - i
        c1, c2 = st.columns([6, 1])
        c1.markdown(f"• {n.get('metin', '')}  <span style='opacity:.55;font-size:.8em'>({n.get('tarih', '')})</span>",
                    unsafe_allow_html=True)
        if c2.button("🗑️", key=f"m28_sil_{gercek}"):
            not_sil(gercek)
            st.rerun()
    yeni_not = st.text_input("➕ Yeni not", key="m28_yeni_not", placeholder="ör. Kedimin adı Pamuk")
    if st.button("Ekle", key="m28_ekle") and yeni_not.strip():
        not_ekle(yeni_not)
        st.rerun()
