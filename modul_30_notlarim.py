# -*- coding: utf-8 -*-
"""
AREX — Modül 30: 📝 NOTLARIM (sohbetten yazılı/sesli not alma)
==============================================================================
Sohbette (yazarak ya da 🎤 sesli):
  • "notlarıma kaydet: yarın fizik ödevi var"   • "not al: süt al"   • "şunu not et …"
  • "bunu notlarıma kaydet" / "bunu not al"  → AREX'in son cevabını not olarak kaydeder
  • "yarın 10'da toplantı diye not al"        • "notlarım" / "notlarımı göster"
  • "3. notu sil" / "notu sil 3"               • "notlarımda fizik ara"
Dosya: arex_notlarim.json (kişisel veri; git'e gitmez).
"""
import json
import os
import re
import time

_PROJE = os.path.dirname(os.path.abspath(__file__))
NOT_DOSYASI = os.path.join(_PROJE, "arex_notlarim.json")


def notlari_oku() -> list:
    try:
        with open(NOT_DOSYASI, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return veri if isinstance(veri, list) else []
    except Exception:
        return []


def _yaz(liste: list) -> None:
    gecici = NOT_DOSYASI + ".tmp"
    with open(gecici, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=1)
    os.replace(gecici, NOT_DOSYASI)


def not_ekle(metin: str, kaynak: str = "sohbet") -> dict:
    liste = notlari_oku()
    kayit = {"no": (max([n.get("no", 0) for n in liste]) + 1) if liste else 1, "metin": metin.strip()[:4000],
             "tarih": time.strftime("%d.%m.%Y %H:%M"), "kaynak": kaynak}
    liste.append(kayit)
    _yaz(liste)
    return kayit


def not_sil(no: int) -> bool:
    liste = notlari_oku()
    yeni = [n for n in liste if n.get("no") != no]
    if len(yeni) == len(liste):
        return False
    _yaz(yeni)
    return True


def _kisalt(metin: str, n: int = 140) -> str:
    t = re.sub(r"\s+", " ", re.sub(r"[#*`>|]", "", metin)).strip()
    return t if len(t) <= n else t[:n].rstrip() + "…"


def _son_cevap(oturum) -> str:
    for m in reversed((oturum or {}).get("messages") or []):
        if m.get("role") == "assistant" and m.get("content"):
            return re.sub(r"^\s*(?:🤖|🧠)\s*\*\*AREX AI[^*\n]*\*\*\s*", "", str(m["content"])).strip()
    return ""


_KAYDET_BAS = re.compile(
    r"^(?:lütfen\s+)?(?:notlar[ıi]ma\s+(?:kaydet|ekle|yaz|al)|not(?:larıma)?\s+(?:al|et|ekle|kaydet|düş|dus)|"
    r"(?:şunu|sunu|bunu|bunları|bunlari)\s+(?:notlar[ıi]ma\s+(?:kaydet|ekle)|not\s+(?:al|et))|yeni\s+not)\s*[:\-,]?\s*(.*)$",
    re.IGNORECASE | re.DOTALL)
_KAYDET_SON = re.compile(r"^(.+?)\s*(?:diye\s+)?(?:notlar[ıi]ma\s+(?:kaydet|ekle|yaz)|not\s+(?:al|et))[.!]?$",
                         re.IGNORECASE | re.DOTALL)


def notlarim_yanitla(metin: str, oturum=None):
    """Not komutuysa (cevap, etiket), değilse (None, None)."""
    t = (metin or "").strip()
    tl = t.replace("İ", "i").replace("I", "ı").lower()
    if not t or len(t) > 4000:
        return None, None
    # Listele / ara
    if re.fullmatch(r"(?:notlar[ıi]m|notlar[ıi]m[ıi]\s+(?:göster|goster|listele|oku|aç|ac)|notlar[ıi]ma\s+bak|kayıtlı notlar[ıi]m)[.!?]*", tl):
        liste = notlari_oku()
        if not liste:
            return ("📝 Henüz notun yok. *\"notlarıma kaydet: …\"* yazarak ya da 🎤 ile söyleyerek ekleyebilirsin."), "📝 Notlarım"
        satirlar = [f"**{n['no']}.** {_kisalt(n['metin'])}  <sub>{n.get('tarih', '')}</sub>" for n in liste[-25:][::-1]]
        return ("### 📝 Notlarım\n\n" + "\n\n".join(satirlar) +
                "\n\n_Silmek için: \"3. notu sil\" • Aramak için: \"notlarımda fizik ara\"_"), "📝 Notlarım"
    m = re.search(r"notlar[ıi]mda\s+(.+?)\s+(?:ara|bul)", tl)
    if m:
        q = m.group(1).strip()
        bulunan = [n for n in notlari_oku() if q in n["metin"].lower()]
        if not bulunan:
            return f"🔎 Notlarında **{q}** geçen bir şey bulamadım.", "📝 Notlarım"
        return ("### 🔎 Bulunan notlar\n\n" + "\n\n".join(f"**{n['no']}.** {_kisalt(n['metin'], 200)}" for n in bulunan[-15:])), "📝 Notlarım"
    # Sil
    m = re.search(r"(?:^|\s)(\d+)\s*\.?\s*not(?:u|umu)?\s+sil|not(?:u|umu)?\s+sil\s*(\d+)", tl)
    if m and "sil" in tl:
        no = int(m.group(1) or m.group(2))
        return ((f"🗑️ {no}. notu sildim." if not_sil(no) else f"❓ {no} numaralı bir not bulamadım. *\"notlarım\"* yazıp numaraya bak."),
                "📝 Notlarım")
    # Kaydet
    icerik = None
    m = _KAYDET_BAS.match(t)
    if m:
        icerik = m.group(1).strip()
        if not icerik or re.fullmatch(r"(?:bunu|bunları|bunlari|şunu|sunu|son cevabı|son cevabi|cevabı|cevabi)?", icerik.lower()):
            icerik = _son_cevap(oturum)
    else:
        m = _KAYDET_SON.match(t)
        if m:
            icerik = m.group(1).strip()
            if re.fullmatch(r"(?:bunu|bunları|bunlari|şunu|sunu|son cevabı|son cevabi|cevabı|cevabi)", icerik.lower()):
                icerik = _son_cevap(oturum)
    if icerik is None:
        return None, None
    if not icerik:
        return "📝 Neyi not almamı istersin? Ör: *\"notlarıma kaydet: cuma günü fizik sınavı\"*", "📝 Notlarım"
    kayit = not_ekle(icerik)
    return (f"📝 **Notlarına kaydettim (#{kayit['no']})**\n\n> {_kisalt(icerik, 300)}\n\n"
            f"_Görmek için: \"notlarım\"_"), "📝 Notlarım"


def notlarim_paneli():
    import streamlit as st
    st.markdown("### 📝 Notlarım")
    st.caption("Sohbette 'notlarıma kaydet: …' yazarak veya 🎤 ile söyleyerek de not ekleyebilirsin.")
    yeni = st.text_area("Yeni not", key="m30_yeni", height=80, placeholder="Aklındakini yaz…")
    if st.button("➕ Notu kaydet", use_container_width=True, key="m30_ekle") and yeni.strip():
        not_ekle(yeni, "panel")
        st.rerun()
    ara = st.text_input("🔎 Ara", key="m30_ara")
    liste = [n for n in notlari_oku() if not ara or ara.lower() in n["metin"].lower()]
    if not liste:
        st.info("Not yok.")
    for n in liste[::-1]:
        with st.container(border=True):
            c1, c2 = st.columns([8, 1])
            c1.markdown(f"**{n['no']}.** {n['metin']}")
            c1.caption(f"🕒 {n.get('tarih', '')} • {n.get('kaynak', '')}")
            if c2.button("🗑️", key=f"m30_sil_{n['no']}"):
                not_sil(n["no"])
                st.rerun()
    if notlari_oku():
        st.download_button("📥 Notları indir (.md)", "\n\n".join(f"## {n['no']}. ({n.get('tarih', '')})\n{n['metin']}" for n in notlari_oku()),
                           file_name="arex_notlarim.md", use_container_width=True, key="m30_indir")
