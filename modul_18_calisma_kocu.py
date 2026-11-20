# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 18: ÇALIŞMA KOÇU (TAKİP • SOHBET İÇİ TEST • HATIRLATICI)
(modul_18_calisma_kocu.py)
==============================================================================
  1. 📊 Çalışma takibi   : "bugün 30 matematik sorusu çözdüm", "45 dakika fizik çalıştım",
                           "bu hafta ne kadar çalıştım", "günlük hedefim 50 soru"
                           → kayıtlar Modül 7'nin soru takip dosyasına (aynı biçimde) yazılır;
                             haftalık rapor SVG çubuk grafik + seri (streak) + hedef ilerlemesi
  2. 📝 Sohbet içi test   : "bana 5 matematik sorusu sor", "köklü sayılardan test yap"
                           → 130 tekil soruluk bankadan sorar, cevabı (6√3 = "6 kök 3" gibi
                             eşdeğer yazımlar dahil) kontrol eder, çözümü gösterir, puanlar
     📒 Yanlış defteri: testte yanlış/boş bırakılan sorular otomatik kaydedilir;
                           "yanlış defterim", "yanlışlarımı tekrar et" (2 kez doğru → öğrenildi),
                           "yanlış defterine ekle: <not>", "#3 yanlışı sil"
  3. ⏰ Hatırlatıcı       : "yarın 8'de fizik sınavımı hatırlat", "20 dakika sonra su içmeyi hatırlat"
                           → uygulama açıkken bildirim (toast) + telefonda gerçek alarm için
                             tek dokunuşla Google Takvim'e ekleme bağlantısı

Giriş noktası: calisma_kocu_yanitla(metin, oturum) -> (yanıt, etiket) | (None, None)
  oturum: st.session_state (test durumu burada tutulur)
"""

import base64
import json
import math
import os
import random
import re
import urllib.parse
from datetime import date, datetime, timedelta

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("Europe/Istanbul")
except Exception:  # pragma: no cover
    _TZ = None

import modul_14_pro_matematik as m14

_KOK = os.path.dirname(os.path.abspath(__file__))
TAKIP_DOSYASI = os.path.join(_KOK, "ahmet_soru_takip.json")      # Modül 7 ile ortak
AYAR_DOSYASI = os.path.join(_KOK, "arex_calisma_ayarlari.json")
HATIRLATICI_DOSYASI = os.path.join(_KOK, "arex_hatirlaticilar.json")
YANLIS_DOSYASI = os.path.join(_KOK, "arex_yanlis_defteri.json")

_GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
_GUN_KISA = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
_AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
_AY_NO = {a.lower(): i + 1 for i, a in enumerate(_AYLAR)}

# Ders adı → (kanonik ad, eşleşen kökler)
_DERSLER = {
    "Matematik": ("matematik", "mat ", "geometri"),
    "Fizik": ("fizik",),
    "Kimya": ("kimya",),
    "Biyoloji": ("biyoloji",),
    "Türk Dili ve Edebiyatı": ("edebiyat", "türkçe", "turkce", "paragraf"),
    "Tarih": ("tarih",),
    "Coğrafya": ("coğrafya", "cografya"),
    "İngilizce": ("ingilizce", "english"),
    "Din Kültürü": ("din kültürü", "din "),
    "Felsefe": ("felsefe",),
}


def _simdi():
    return datetime.now(_TZ).replace(tzinfo=None) if _TZ else datetime.now()


def _kucult(m: str) -> str:
    return m.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()


def _oku(yol, varsayilan):
    try:
        with open(yol, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return varsayilan


def _yaz(yol, veri):
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)


def _svg_isaretle(svg: str) -> str:
    return f"\n<!--AREX_SVG:{base64.b64encode(svg.encode()).decode()}-->"


def _ders_bul(t: str):
    for ad, kokler in _DERSLER.items():
        if any(k in t + " " for k in kokler):
            return ad
    return None


# ==============================================================================
# 1. ÇALIŞMA TAKİBİ
# ==============================================================================
def _kayit_ekle(ders, konu, soru, sure_dk, tarih: date):
    kayitlar = _oku(TAKIP_DOSYASI, [])
    kayitlar.insert(0, {"ders": ders, "konu": konu, "soru_sayisi": int(soru), "sure_dk": int(sure_dk),
                        "tarih": tarih.isoformat()})
    _yaz(TAKIP_DOSYASI, kayitlar)


def _gunluk_toplamlar(gun_sayisi=7):
    bugun = _simdi().date()
    kayitlar = _oku(TAKIP_DOSYASI, [])
    gunler = {bugun - timedelta(days=i): {"soru": 0, "dk": 0} for i in range(gun_sayisi)}
    dersler = {}
    for k in kayitlar:
        try:
            t = date.fromisoformat(k.get("tarih", ""))
        except ValueError:
            continue
        if t in gunler:
            gunler[t]["soru"] += int(k.get("soru_sayisi", 0) or 0)
            gunler[t]["dk"] += int(k.get("sure_dk", 0) or 0)
            d = dersler.setdefault(k.get("ders", "Diğer"), {"soru": 0, "dk": 0})
            d["soru"] += int(k.get("soru_sayisi", 0) or 0)
            d["dk"] += int(k.get("sure_dk", 0) or 0)
    return dict(sorted(gunler.items())), dersler, kayitlar


def _seri_hesapla(kayitlar):
    """Bugünden (veya dünden) geriye kesintisiz çalışılan gün sayısı."""
    gunler = set()
    for k in kayitlar:
        try:
            if int(k.get("soru_sayisi", 0) or 0) > 0 or int(k.get("sure_dk", 0) or 0) > 0:
                gunler.add(date.fromisoformat(k["tarih"]))
        except Exception:
            pass
    g = _simdi().date()
    if g not in gunler:
        g -= timedelta(days=1)
    seri = 0
    while g in gunler:
        seri += 1
        g -= timedelta(days=1)
    return seri


def _hafta_grafigi(gunler: dict, hedef: int):
    G, Y, kenar, ust = 640, 300, 40, 40
    degerler = [v["soru"] for v in gunler.values()]
    en_buyuk = max(degerler + [hedef or 0, 10])
    bar_g = (G - 2 * kenar) / len(gunler)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {G} {Y}" style="width:100%;max-width:640px;height:auto;'
         f'display:block;margin:6px 0;background:rgba(15,23,42,.55);border-radius:14px;border:1px solid rgba(148,163,184,.25)" '
         f'font-family="Inter,system-ui,sans-serif" role="img" aria-label="Son 7 gün çözülen soru">',
         f'<text x="{G / 2}" y="24" fill="#e2e8f0" font-size="14" font-weight="600" text-anchor="middle">Son 7 gün · çözülen soru</text>']
    taban = Y - kenar
    yuk = taban - ust
    if hedef:
        hy = taban - hedef / en_buyuk * yuk
        p.append(f'<line x1="{kenar}" y1="{hy:.1f}" x2="{G - kenar}" y2="{hy:.1f}" stroke="#facc15" stroke-dasharray="6 5" stroke-width="1.5"/>')
        p.append(f'<text x="{G - kenar}" y="{hy - 6:.1f}" fill="#facc15" font-size="11" text-anchor="end">hedef {hedef}</text>')
    bugun = _simdi().date()
    for i, (gun, v) in enumerate(gunler.items()):
        h = v["soru"] / en_buyuk * yuk
        x = kenar + i * bar_g + bar_g * 0.18
        w = bar_g * 0.64
        renk = "#38bdf8" if gun != bugun else "#a78bfa"
        if h > 0:
            p.append(f'<rect x="{x:.1f}" y="{taban - h:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="{renk}"/>')
            p.append(f'<text x="{x + w / 2:.1f}" y="{taban - h - 6:.1f}" fill="#e2e8f0" font-size="12" font-weight="600" text-anchor="middle">{v["soru"]}</text>')
        p.append(f'<text x="{x + w / 2:.1f}" y="{taban + 16}" fill="{"#c4b5fd" if gun == bugun else "#94a3b8"}" font-size="11.5" '
                 f'text-anchor="middle">{"Bugün" if gun == bugun else _GUN_KISA[gun.weekday()]}</text>')
    p.append(f'<line x1="{kenar}" y1="{taban}" x2="{G - kenar}" y2="{taban}" stroke="#475569"/>')
    p.append("</svg>")
    return "".join(p)


def _sure_dk_bul(t: str):
    dk = 0
    for sayi, birim in re.findall(r"(\d+(?:[.,]\d+)?)\s*(saat|sa\b|dakika|dk)", t):
        deger = float(sayi.replace(",", "."))
        dk += deger * 60 if birim.startswith("sa") else deger
    if re.search(r"yarım\s*saat", t):
        dk += 30
    if re.search(r"bir\s*buçuk\s*saat", t):
        dk += 90
    return int(round(dk))


def _calisma_kaydi(t: str):
    if not re.search(r"çözdüm|cozdum|çalıştım|calistim|bitirdim|yaptım|yaptim|tamamladım|okudum", t):
        return None
    if re.search(r"\b(?:nasıl|ne kadar|kaç|mı|mi)\b.*\?$", t):
        return None
    soru_m = re.search(r"(\d+)\s*(?:tane\s*)?(?:\w+\s+){0,2}?(?:soru|test|problem)", t)
    soru = int(soru_m.group(1)) if soru_m else 0
    dk = _sure_dk_bul(t)
    if soru == 0 and dk == 0:
        return None
    if soru > 2000 or dk > 1440:
        return "🤔 Bu sayı biraz fazla görünüyor; yanlış yazmış olabilir misin?", "📊 Çalışma Takibi"
    ders = _ders_bul(t) or "Genel"
    tarih = _simdi().date() - timedelta(days=1 if re.search(r"\bdün\b|\bdun\b", t) else 0)
    konu_m = re.search(r"([a-zçğıöşü ]{3,40}?)\s*konusundan", t)
    konu = konu_m.group(1).strip().title() if konu_m else "Sohbetten kayıt"
    _kayit_ekle(ders, konu, soru, dk, tarih)

    gunler, _, kayitlar = _gunluk_toplamlar()
    ayar = _oku(AYAR_DOSYASI, {})
    hedef = int(ayar.get("gunluk_soru_hedefi", 0) or 0)
    bugun = gunler.get(_simdi().date(), {"soru": 0, "dk": 0})
    seri = _seri_hesapla(kayitlar)
    parca = []
    if soru:
        parca.append(f"**{soru} soru**")
    if dk:
        parca.append(f"**{dk} dk**")
    satirlar = [f"✅ Kaydettim: {ders} — {' · '.join(parca)}{' (dün)' if tarih != _simdi().date() else ''}", ""]
    satirlar.append(f"- Bugün toplam: **{bugun['soru']} soru**, **{bugun['dk']} dk**")
    if hedef:
        oran = min(100, round(bugun["soru"] / hedef * 100))
        dolu = round(oran / 10)
        satirlar.append(f"- Günlük hedef: `{'█' * dolu}{'░' * (10 - dolu)}` %{oran} ({bugun['soru']}/{hedef})"
                        + (" 🎯 **Hedef tamam!**" if bugun["soru"] >= hedef else ""))
    if seri >= 2:
        satirlar.append(f"- 🔥 **{seri} gündür** aralıksız çalışıyorsun!")
    satirlar.append("\n💡 Haftalık özet için: *\"bu hafta ne kadar çalıştım\"*")
    return "\n".join(satirlar), "📊 Çalışma Takibi"


def _hedef_ayarla(t: str):
    m = re.search(r"(?:günlük\s*)?hedef(?:im)?\s*(?:günde\s*)?(\d+)\s*soru|günde\s*(\d+)\s*soru\s*(?:hedef|çözmek\s*istiyorum)", t)
    if not m:
        return None
    hedef = int(m.group(1) or m.group(2))
    if not 1 <= hedef <= 1000:
        return "🎯 Hedef 1 ile 1000 soru arasında olmalı.", "🎯 Günlük Hedef"
    ayar = _oku(AYAR_DOSYASI, {})
    ayar["gunluk_soru_hedefi"] = hedef
    _yaz(AYAR_DOSYASI, ayar)
    return (f"🎯 Günlük hedefin **{hedef} soru** olarak ayarlandı. Her kayıtta ilerlemeni göstereceğim; "
            f"haftalık raporda da hedef çizgisi olarak göreceksin. Başarılar! 💪"), "🎯 Günlük Hedef"


def _rapor(t: str):
    if not re.search(r"(?:bu\s*hafta|haftalık|haftalik|son\s*7\s*gün|bugün).{0,25}(?:ne\s*kadar|kaç\s*soru|çalıştım|rapor|özet)"
                     r"|çalışma\s*(?:raporu|özeti|istatisti)|istatistiklerim|ilerlememi\s*göster", t):
        return None
    gunler, dersler, kayitlar = _gunluk_toplamlar()
    toplam_soru = sum(v["soru"] for v in gunler.values())
    toplam_dk = sum(v["dk"] for v in gunler.values())
    if toplam_soru == 0 and toplam_dk == 0:
        return ("📊 Son 7 günde henüz kayıt yok. Çalıştıkça bana yaz, ben tutayım:\n"
                "- *\"bugün 30 matematik sorusu çözdüm\"*\n- *\"45 dakika fizik çalıştım\"*\n"
                "- *\"günlük hedefim 50 soru\"*"), "📊 Çalışma Raporu"
    ayar = _oku(AYAR_DOSYASI, {})
    hedef = int(ayar.get("gunluk_soru_hedefi", 0) or 0)
    aktif_gun = sum(1 for v in gunler.values() if v["soru"] or v["dk"])
    en_iyi_gun, en_iyi = max(gunler.items(), key=lambda kv: kv[1]["soru"])
    satirlar = ["📊 **Son 7 Günlük Çalışma Raporu**", "",
                f"- Toplam: **{toplam_soru} soru** · **{toplam_dk // 60} sa {toplam_dk % 60} dk**",
                f"- Çalışılan gün: **{aktif_gun}/7** · günlük ortalama **{round(toplam_soru / 7)} soru**"]
    if en_iyi["soru"]:
        satirlar.append(f"- En verimli gün: **{_GUNLER[en_iyi_gun.weekday()]}** ({en_iyi['soru']} soru)")
    seri = _seri_hesapla(kayitlar)
    if seri:
        satirlar.append(f"- 🔥 Seri: **{seri} gün**")
    if hedef:
        tutan = sum(1 for v in gunler.values() if v["soru"] >= hedef)
        satirlar.append(f"- 🎯 Hedefi ({hedef} soru) tutturduğun gün: **{tutan}/7**")
    if dersler:
        satirlar.append("\n**Derslere göre:**")
        for ad, v in sorted(dersler.items(), key=lambda kv: -kv[1]["soru"]):
            sure_ek = f" · {v['dk']} dk" if v["dk"] else ""
            satirlar.append(f"- {ad}: {v['soru']} soru{sure_ek}")
        eksik = [d for d in ("Matematik", "Fizik", "Kimya", "Biyoloji") if d not in dersler]
        if eksik:
            satirlar.append(f"\n💡 Bu hafta **{', '.join(eksik[:2])}** çalışmadın; yarın kısa bir tekrar iyi gelir.")
    return "\n".join(satirlar) + _svg_isaretle(_hafta_grafigi(gunler, hedef)), "📊 Çalışma Raporu"


# ==============================================================================
# 2. SOHBET İÇİ TEST
# ==============================================================================
_BANKA_ONBELLEK = None


def _banka():
    global _BANKA_ONBELLEK
    if _BANKA_ONBELLEK is None:
        try:
            import modul_4_matematik_motoru as m4
            tekil = {}
            for q in m4.COZUMLU_SORU_BANKASI:
                tekil.setdefault(q["soru"], q)
            _BANKA_ONBELLEK = list(tekil.values())
        except Exception:
            _BANKA_ONBELLEK = []
    return _BANKA_ONBELLEK


_KONU_ANAHTAR = {
    "denklem": "1. Derece Denklemler", "üslü": "Üslü Sayılar", "uslu": "Üslü Sayılar", "mantık": "Mantık & Önermeler",
    "önerme": "Mantık & Önermeler", "küme": "Kümeler", "mutlak": "Mutlak Değer & Eşitsizlikler",
    "eşitsizlik": "Mutlak Değer & Eşitsizlikler", "oran": "Oran-Orantı & Yüzde", "yüzde": "Oran-Orantı & Yüzde",
    "fonksiyon": "Fonksiyonlar", "üçgen": "Üçgenler & Geometri", "geometri": "Üçgenler & Geometri",
    "polinom": "Polinomlar & Özdeşlikler", "özdeşlik": "Polinomlar & Özdeşlikler", "olasılık": "Olasılık & Veri",
    "sözel": "Sözel Problemler", "problem": "Sözel Problemler", "köklü": "Köklü Sayılar", "kök": "Köklü Sayılar",
    "ebob": "EBOB - EKOK", "ekok": "EBOB - EKOK",
}


def _cevap_normalize(c: str) -> str:
    c = _kucult(str(c)).replace("`", "").replace(" ", "")
    c = re.sub(r"^(?:x|cevap|sonuç|sonuc)[=:]", "", c)
    c = c.replace("kök", "√").replace("kok", "√").replace("°", "").replace("derece", "")
    return c.rstrip(".")


def _cevap_dogru_mu(verilen: str, dogru: str) -> bool:
    v, d = _cevap_normalize(verilen), _cevap_normalize(dogru)
    if not v:
        return False
    if v == d:
        return True
    # Sayısal / sembolik eşdeğerlik: "6 kök 3" = "6√3", "0,5" = "1/2", "3125" = "3.125" değil (binlik ayraç belirsiz)
    try:
        a = m14.ifade_hesapla(verilen.replace("kök", "√").replace("kok", "√"))
        b = m14.ifade_hesapla(str(dogru))
        if isinstance(a, float) or isinstance(b, float):
            return abs(float(a) - float(b)) < 1e-9
        return a == b
    except Exception:
        return False


_OGRENILDI_ESIGI = 2


def _yanlisa_ekle(q, verilen: str = "") -> bool:
    """Testte yanlış/boş bırakılan soruyu yanlış defterine yazar (aynı soru tekrar eklenmez, sayacı artar)."""
    liste = _oku(YANLIS_DOSYASI, [])
    for k in liste:
        if k.get("soru") == q["soru"]:
            k["kac_kez"] = k.get("kac_kez", 1) + 1
            k["dogru_tekrar"] = 0
            k["son"] = _simdi().date().isoformat()
            _yaz(YANLIS_DOSYASI, liste)
            return False
    no = max([k["no"] for k in liste] + [0]) + 1
    liste.append({"no": no, "ders": "Matematik", "konu": q.get("konu", ""), "soru": q["soru"], "cevap": q.get("cevap"),
                  "cozum": q.get("cozum", ""), "verilen": verilen[:60], "kac_kez": 1, "dogru_tekrar": 0,
                  "tarih": _simdi().date().isoformat(), "son": _simdi().date().isoformat()})
    _yaz(YANLIS_DOSYASI, liste)
    return True


def _defter_dogru(q) -> str:
    """Defterden sorulan soru doğru bilindi → sayaç; eşiğe ulaşınca defterden çıkar."""
    liste = _oku(YANLIS_DOSYASI, [])
    for k in liste:
        if k.get("soru") == q["soru"]:
            k["dogru_tekrar"] = k.get("dogru_tekrar", 0) + 1
            if k["dogru_tekrar"] >= _OGRENILDI_ESIGI:
                liste.remove(k)
                _yaz(YANLIS_DOSYASI, liste)
                return "\n\n🎓 Bu soruyu üst üste 2 kez doğru yaptın — **öğrenildi**, yanlış defterinden çıkardım!"
            _yaz(YANLIS_DOSYASI, liste)
            return f"\n\n📒 Defterde: {k['dogru_tekrar']}/{_OGRENILDI_ESIGI} doğru tekrar"
    return ""


def _yanlis_defteri(t: str, ham: str):
    m = re.match(r"\s*yanlış\s*defter\w*\s*ekle\s*[:\-]?\s*(.+)$", ham, flags=re.I | re.S) or \
        re.match(r"\s*yanl[ıi]ş\s*defter\w*\s*ekle\s*[:\-]?\s*(.+)$", _kucult(ham), flags=re.S)
    if m:
        not_metni = m.group(1).strip()[:400]
        if len(not_metni) < 3:
            return "📒 Ne ekleyeyim? Örnek: *\"yanlış defterine ekle: zincir kuralında içi türevlemeyi unuttum\"*", "📒 Yanlış Defteri"
        liste = _oku(YANLIS_DOSYASI, [])
        no = max([k["no"] for k in liste] + [0]) + 1
        liste.append({"no": no, "ders": _ders_bul(_kucult(not_metni)) or "Genel", "konu": "Not", "soru": not_metni,
                      "cevap": None, "kac_kez": 1, "dogru_tekrar": 0, "tarih": _simdi().date().isoformat(),
                      "son": _simdi().date().isoformat()})
        _yaz(YANLIS_DOSYASI, liste)
        return f"📒 Yanlış defterine eklendi (#{no}). Görmek için: *\"yanlış defterim\"*", "📒 Yanlış Defteri"
    m = re.search(r"#?(\d+)\s*(?:nolu|numaralı)?\s*yanlış\w*\s*sil", t)
    if m:
        no = int(m.group(1))
        liste = _oku(YANLIS_DOSYASI, [])
        yeni = [k for k in liste if k["no"] != no]
        if len(yeni) == len(liste):
            return f"📒 #{no} numaralı kayıt bulamadım.", "📒 Yanlış Defteri"
        _yaz(YANLIS_DOSYASI, yeni)
        return f"🗑️ #{no} yanlış defterinden silindi.", "📒 Yanlış Defteri"
    if not re.search(r"yanlış\s*defter(?:im|imi|imde)|yanlışlarım(?:ı\s*(?:göster|listele))?$|yanlışlarımı\s*göster", t):
        return None
    liste = _oku(YANLIS_DOSYASI, [])
    if not liste:
        return ("📒 Yanlış defterin boş. Sohbet içi testte yanlış yaptığın ya da geçtiğin sorular buraya otomatik "
                "eklenir. Kendin not eklemek için: *\"yanlış defterine ekle: ...\"*"), "📒 Yanlış Defteri"
    gruplar = {}
    for k in liste:
        gruplar.setdefault(f"{k.get('ders', 'Genel')} · {k.get('konu') or 'Genel'}", []).append(k)
    satirlar = [f"📒 **Yanlış Defterin** — {len(liste)} kayıt", ""]
    for grup, kayitlar in sorted(gruplar.items(), key=lambda g: -len(g[1])):
        satirlar.append(f"**{grup}** ({len(kayitlar)})")
        for k in kayitlar[:6]:
            soru = re.sub(r"\s+", " ", k["soru"])
            ek = f" · ✍️ {k['kac_kez']} kez yanlış" if k.get("kac_kez", 1) > 1 else ""
            ek += f" · ✅ {k['dogru_tekrar']}/{_OGRENILDI_ESIGI}" if k.get("dogru_tekrar") else ""
            satirlar.append(f"- #{k['no']} {soru[:90]}{'…' if len(soru) > 90 else ''}{ek}")
        satirlar.append("")
    sorulabilir = sum(1 for k in liste if k.get("cevap"))
    if sorulabilir:
        satirlar.append(f"🔁 {sorulabilir} soruyu tekrar çözebilirsin: *\"yanlışlarımı tekrar et\"* "
                        f"(üst üste {_OGRENILDI_ESIGI} kez doğru yapınca defterden çıkar)")
    satirlar.append("Silmek için: *\"#3 yanlışı sil\"*")
    return "\n".join(satirlar), "📒 Yanlış Defteri"


def _defter_testi_baslat(t: str, oturum):
    if not re.search(r"yanlışlarım\w*\s*(?:tekrar|sor|çöz|çalış)|yanlış\s*defter\w*\s*(?:den|ndan)?\s*(?:soru|test|tekrar)", t):
        return None
    havuz = [k for k in _oku(YANLIS_DOSYASI, []) if k.get("cevap")]
    if not havuz:
        return ("📒 Tekrar edilecek soru yok — yanlış defterin boş ya da sadece not içeriyor. "
                "Önce bir test çöz: *\"bana 5 matematik sorusu sor\"*"), "📒 Yanlış Defteri"
    havuz.sort(key=lambda k: (k.get("son", ""), -k.get("kac_kez", 1)))
    sorular = [{"soru": k["soru"], "cevap": k["cevap"], "cozum": k.get("cozum", ""), "konu": k.get("konu", "")}
               for k in havuz[:10]]
    random.shuffle(sorular)
    oturum.pop("arex_kart", None)
    oturum["arex_test"] = {"sorular": sorular, "sira": 0, "dogru": 0, "yanlis": 0, "bos": 0, "ipucu": False,
                           "konu": "Yanlış Defteri", "kaynak": "defter"}
    return (f"🔁 **Yanlış defteri tekrarı** — {len(sorular)} soru. Bu sefer olacak! 💪\n\n"
            + _soru_metni(oturum["arex_test"])), "📒 Yanlış Defteri"


def _soru_metni(durum) -> str:
    q = durum["sorular"][durum["sira"]]
    return (f"**Soru {durum['sira'] + 1}/{len(durum['sorular'])}** · _{q['konu']}_\n\n{q['soru']}\n\n"
            f"✍️ Cevabını yaz · *\"ipucu\"* · *\"geç\"* · *\"testi bitir\"*")


def _test_baslat(t: str, oturum):
    if re.search(r"çözdüm|cozdum|çalıştım|calistim|yaptım|yaptim|bitirdim", t):
        return None  # geçmiş zaman → çalışma kaydı, test isteği değil
    if not re.search(r"(?:test|quiz|deneme|soru)\s*(?:başlat|yap|çöz|sor)|bana\s*\d*\s*(?:tane\s*)?(?:\w+\s+){0,2}soru(?:su|ları)?\s*sor"
                     r"|beni\s*(?:test|sına)|sınav\s*yap", t):
        return None
    if re.search(r"fizik|kimya|biyoloji|tarih|coğrafya|ingilizce|edebiyat", t):
        return None  # banka yalnızca matematik → diğer dersleri yapay zekâ hazırlasın
    n_m = re.search(r"(\d+)\s*(?:tane\s*)?(?:\w+\s+){0,2}?soru", t)
    n = max(1, min(int(n_m.group(1)) if n_m else 5, 20))
    konu = next((v for k, v in _KONU_ANAHTAR.items() if k in t), None)
    havuz = [q for q in _banka() if not konu or q["konu"] == konu]
    if not havuz:
        return "📝 Soru bankasına ulaşamadım, birazdan tekrar dener misin?", "📝 Test"
    sorular = random.sample(havuz, min(n, len(havuz)))
    oturum["arex_test"] = {"sorular": sorular, "sira": 0, "dogru": 0, "yanlis": 0, "bos": 0,
                           "ipucu": False, "konu": konu or "Karışık Matematik"}
    return (f"📝 **{oturum['arex_test']['konu']} testi başlıyor!** {len(sorular)} soru — bol şans 🍀\n\n"
            + _soru_metni(oturum["arex_test"])), "📝 Sohbet İçi Test"


def _konu_kisa_adi(konu: str) -> str:
    return next((k for k, v in _KONU_ANAHTAR.items() if v == konu), "matematik")


def _defter_ozeti(d) -> str:
    n = d.get("defter_eklenen", 0)
    if d.get("kaynak") == "defter":
        kalan = len(_oku(YANLIS_DOSYASI, []))
        return f"\n- 📒 Yanlış defterinde **{kalan}** kayıt kaldı"
    return f"\n- 📒 **{n}** soru yanlış defterine eklendi → *\"yanlışlarımı tekrar et\"*" if n else ""


def _test_bitir(oturum, erken=False):
    d = oturum.pop("arex_test", None)
    if not d:
        return None
    toplam = d["dogru"] + d["yanlis"] + d["bos"]
    if toplam == 0:
        return "📝 Test kapatıldı. İstediğin zaman *\"bana 5 matematik sorusu sor\"* yazabilirsin.", "📝 Test Sonucu"
    puan = round(d["dogru"] / toplam * 100)
    yorum = ("🏆 Mükemmel!" if puan == 100 else "🌟 Çok iyi!" if puan >= 80 else "👍 Fena değil, biraz tekrarla daha da iyi olur."
             if puan >= 50 else "💪 Bu konuyu birlikte tekrar edelim; konu anlatımı için Eğitim sekmesine bakabilirsin.")
    try:
        _kayit_ekle("Matematik", f"Sohbet testi: {d['konu']}", toplam, 0, _simdi().date())
    except Exception:
        pass
    return (f"🏁 **Test {'erken ' if erken else ''}bitti!**\n\n"
            f"- ✅ Doğru: **{d['dogru']}** · ❌ Yanlış: **{d['yanlis']}** · ⏭️ Boş: **{d['bos']}**\n"
            f"- Puan: **{puan}/100** {yorum}\n- Çözdüğün {toplam} soru çalışma takibine eklendi 📊{_defter_ozeti(d)}\n\n"
            f"Yeniden denemek için: *\"bana 5 {_konu_kisa_adi(d['konu'])} sorusu sor\"*"), "📝 Test Sonucu"


def _test_cevapla(metin: str, oturum):
    d = oturum.get("arex_test")
    if not d:
        return None
    t = _kucult(metin)
    if re.search(r"^(?:testi?\s*(?:bitir|kapat|bırak|iptal)|çık|cik|bitir|yeter)\b", t):
        return _test_bitir(oturum, erken=True)
    q = d["sorular"][d["sira"]]
    if re.search(r"^(?:ipucu|ipucu ver|yardım|ipucu lütfen)$", t):
        d["ipucu"] = True
        # Yalnızca ilk adım (sonucu ele vermeden): "√147 = 7√3 olduğundan ... = 8√3" → "√147 = 7√3"
        ilk = re.split(r"\s(?:olduğundan|oldugundan|→|ise|bu nedenle|yani)\s", q.get("cozum", ""))[0].strip(" .")
        if not ilk or _cevap_normalize(q["cevap"]) in _cevap_normalize(ilk.split("=")[-1]):
            ilk = f"Konu: {q['konu']}. Önce verilenleri sadeleştir, sonra adım adım ilerle."
        return f"💡 **İpucu:** {ilk}\n\nŞimdi cevabını yaz 🙂", "📝 Sohbet İçi Test"
    gec = bool(re.search(r"^(?:geç|gec|pas|bilmiyorum|boş|bos)$", t))
    # Sohbetle ilgili belirgin başka bir soru → testi bozmadan normal akışa bırak
    if not gec and len(t.split()) > 6 and not re.search(r"\d|√|kök", t):
        return None
    if gec:
        d["bos"] += 1
        sonuc = f"⏭️ Geçtik. Doğru cevap: **{q['cevap']}**\n> {q.get('cozum', '')}"
    elif _cevap_dogru_mu(metin, q["cevap"]):
        d["dogru"] += 1
        sonuc = f"✅ **Doğru!** {'(ipucuyla 😉)' if d['ipucu'] else '🎉'}\n> {q.get('cozum', '')}"
        if d.get("kaynak") == "defter":
            try:
                sonuc += _defter_dogru(q)
            except Exception:
                pass
    else:
        d["yanlis"] += 1
        sonuc = f"❌ **Yanlış.** Doğru cevap: **{q['cevap']}**\n> {q.get('cozum', '')}"
    if gec or not sonuc.startswith("✅"):
        try:
            if _yanlisa_ekle(q, "" if gec else metin):
                d["defter_eklenen"] = d.get("defter_eklenen", 0) + 1
        except Exception:
            pass
    d["sira"] += 1
    d["ipucu"] = False
    if d["sira"] >= len(d["sorular"]):
        bitis, etiket = _test_bitir(oturum)
        return sonuc + "\n\n---\n\n" + bitis, etiket
    return sonuc + "\n\n---\n\n" + _soru_metni(d), "📝 Sohbet İçi Test"


# ==============================================================================
# 3. HATIRLATICI
# ==============================================================================
def _saat_bul(t: str):
    m = re.search(r"(?:saat\s*)?(\d{1,2})[:.](\d{2})", t)
    if m and int(m.group(1)) < 24 and int(m.group(2)) < 60:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(?:saat\s*)(\d{1,2})(?!\d)|(\d{1,2})\s*'?\s*(?:de|da|te|ta)\b", t)
    if m:
        s = int(m.group(1) or m.group(2))
        if s < 24:
            if re.search(r"akşam|aksam|gece|öğleden sonra", t) and s < 12:
                s += 12
            return s, 0
    if re.search(r"sabah", t):
        return 8, 0
    if re.search(r"öğlen|oglen", t):
        return 12, 0
    if re.search(r"akşam|aksam", t):
        return 19, 0
    return None


def _zaman_coz(t: str):
    simdi = _simdi().replace(second=0, microsecond=0)
    m = re.search(r"(\d+)\s*(dakika|dk|saat)\s*sonra", t)
    if m:
        n = int(m.group(1))
        return simdi + (timedelta(hours=n) if m.group(2) == "saat" else timedelta(minutes=n))
    gun = None
    if re.search(r"\byarın\b|\byarin\b", t):
        gun = simdi.date() + timedelta(days=1)
    elif re.search(r"\bbugün\b|\bbugun\b", t):
        gun = simdi.date()
    else:
        m = re.search(r"(\d{1,2})[./](\d{1,2})(?:[./](\d{4}))?", t)
        if m:
            try:
                gun = date(int(m.group(3) or simdi.year), int(m.group(2)), int(m.group(1)))
            except ValueError:
                return None
        else:
            m = re.search(r"(\d{1,2})\s*(" + "|".join(_AY_NO) + r")", t)
            if m:
                try:
                    gun = date(simdi.year, _AY_NO[m.group(2)], int(m.group(1)))
                except ValueError:
                    return None
            else:
                for i, g in enumerate(_GUNLER):
                    if re.search(r"\b" + _kucult(g) + r"(?:\s*günü|\s*gunu|ya|ye|'?ya|'?ye)?\b", t):
                        ileri = (i - simdi.weekday()) % 7 or 7
                        gun = simdi.date() + timedelta(days=ileri)
                        break
    saat = _saat_bul(t)
    if gun is None and saat is None:
        return None
    gun = gun or simdi.date()
    s, dk = saat or (9, 0)
    zaman = datetime(gun.year, gun.month, gun.day, s, dk)
    if zaman < simdi and gun == simdi.date() and saat and saat[0] < 12 and not re.search(r"sabah", t):
        zaman += timedelta(hours=12)  # "bugün 6'da" ve saat geçmişse → 18:00
    if zaman < simdi and not re.search(r"\d{4}", t) and gun != simdi.date() and gun.month < simdi.month:
        zaman = zaman.replace(year=zaman.year + 1)
    return zaman


def _takvim_baglantisi(baslik: str, zaman: datetime) -> str:
    bitis = zaman + timedelta(minutes=30)
    params = {"action": "TEMPLATE", "text": f"⏰ {baslik}", "dates": f"{zaman:%Y%m%dT%H%M%S}/{bitis:%Y%m%dT%H%M%S}",
              "ctz": "Europe/Istanbul", "details": "AREX AI hatırlatıcısı"}
    return "https://calendar.google.com/calendar/render?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def _hatirlatici(t: str, ham: str):
    # Listeleme / silme
    if re.search(r"hatırlatıcılarım|hatirlaticilarim|hatırlatmalarım|hatırlatıcıları\s*(?:göster|listele)", t):
        liste = [h for h in _oku(HATIRLATICI_DOSYASI, []) if not h.get("silindi")]
        gelecek = sorted((h for h in liste if datetime.fromisoformat(h["zaman"]) >= _simdi() - timedelta(minutes=1)),
                         key=lambda h: h["zaman"])
        if not gelecek:
            return "⏰ Bekleyen hatırlatıcın yok. Örnek: *\"yarın 8'de fizik sınavımı hatırlat\"*", "⏰ Hatırlatıcı"
        satirlar = ["⏰ **Bekleyen Hatırlatıcıların**", ""]
        for h in gelecek[:10]:
            z = datetime.fromisoformat(h["zaman"])
            satirlar.append(f"- **#{h['no']}** {h['baslik']} — {z.day} {_AYLAR[z.month - 1]} {_GUNLER[z.weekday()]} `{z:%H:%M}`")
        satirlar.append("\nSilmek için: *\"#2 hatırlatıcıyı sil\"*")
        return "\n".join(satirlar), "⏰ Hatırlatıcı"
    m = re.search(r"#?(\d+)\s*(?:nolu|numaralı)?\s*hatırlat\w*\s*sil|hatırlat\w*\s*#?(\d+)\s*sil", t)
    if m:
        no = int(m.group(1) or m.group(2))
        liste = _oku(HATIRLATICI_DOSYASI, [])
        for h in liste:
            if h["no"] == no and not h.get("silindi"):
                h["silindi"] = True
                _yaz(HATIRLATICI_DOSYASI, liste)
                return f"🗑️ **#{no}** hatırlatıcı silindi: {h['baslik']}", "⏰ Hatırlatıcı"
        return f"⏰ #{no} numaralı bekleyen hatırlatıcı bulamadım.", "⏰ Hatırlatıcı"

    if not re.search(r"hatırlat|hatirlat|uyar\b|haber\s*ver|alarm\s*kur", t):
        return None
    zaman = _zaman_coz(t)
    if zaman is None:
        return None  # "bana fotosentezi hatırlat" gibi zaman içermeyenler → normal sohbet
    if zaman < _simdi() - timedelta(minutes=1):
        return "⏰ Bu zaman geçmişte kaldı; ileri bir zaman söyler misin?", "⏰ Hatırlatıcı"
    # Başlık: zaman ifadelerini ve komut sözcüklerini ayıkla
    baslik = re.sub(r"\b(?:bana|lütfen|lutfen|bunu|beni|bir|tane)\b", " ", ham, flags=re.I)
    baslik = re.sub(r"(?i)(\d+\s*(?:dakika|dk|saat)\s*sonra|yarın|yarin|bugün|bugun|(?:saat\s*)?\d{1,2}[:.]\d{2}|saat\s*\d{1,2}"
                    r"|\d{1,2}\s*'?\s*(?:de|da|te|ta)\b|\d{1,2}[./]\d{1,2}(?:[./]\d{4})?|sabah|öğlen|akşam|aksam|gece"
                    r"|\d{1,2}\s*(?:" + "|".join(_AY_NO) + r")\w*|(?:" + "|".join(_GUNLER) + r")\w*(?:\s*günü)?)", " ", baslik)
    baslik = re.sub(r"(?i)\s*(?:hatırlat\w*|hatirlat\w*|uyar\w*|haber\s*ver\w*|alarm\s*kur\w*)\s*", " ", baslik)
    baslik = re.sub(r"\s+", " ", baslik).strip(" .,!?:-'")
    baslik = re.sub(r"(?i)(ım|im|um|üm|mı|mi|yı|yi|ı|i|u|ü|ını|ini|unu|ünü)$", "", baslik).strip() if len(baslik) > 25 else baslik
    baslik = (baslik[:1].upper() + baslik[1:]) if baslik else "Hatırlatma"
    liste = _oku(HATIRLATICI_DOSYASI, [])
    no = max([h["no"] for h in liste] + [0]) + 1
    liste.append({"no": no, "baslik": baslik, "zaman": zaman.isoformat(timespec="minutes"), "bildirildi": False})
    _yaz(HATIRLATICI_DOSYASI, liste)
    kalan = zaman - _simdi()
    kalan_yazi = (f"{int(kalan.total_seconds() // 60)} dakika sonra" if kalan < timedelta(hours=1)
                  else f"{int(kalan.total_seconds() // 3600)} saat sonra" if kalan < timedelta(days=1)
                  else f"{kalan.days} gün sonra")
    return (f"⏰ **Hatırlatıcı kuruldu (#{no})**\n\n"
            f"- 📝 {baslik}\n- 📅 {zaman.day} {_AYLAR[zaman.month - 1]} {_GUNLER[zaman.weekday()]}, saat **{zaman:%H:%M}** ({kalan_yazi})\n\n"
            f"📲 **Telefonun alarm versin:** [Google Takvim'e ekle]({_takvim_baglantisi(baslik, zaman)}) — uygulama kapalıyken de bildirim gelir.\n"
            f"AREX açıkken zamanı gelince ekranda da hatırlatırım 🔔"), "⏰ Hatırlatıcı"


def zamani_gelen_hatirlaticilar():
    """Zamanı gelmiş ve henüz bildirilmemiş hatırlatıcıları döndürür ve 'bildirildi' işaretler."""
    liste = _oku(HATIRLATICI_DOSYASI, [])
    simdi = _simdi()
    gelenler = []
    for h in liste:
        if h.get("silindi") or h.get("bildirildi"):
            continue
        try:
            z = datetime.fromisoformat(h["zaman"])
        except Exception:
            continue
        if z <= simdi:
            h["bildirildi"] = True
            if simdi - z < timedelta(hours=12):  # çok eskiyse sessizce kapat
                gelenler.append(h)
    if gelenler or any(h.get("bildirildi") for h in liste):
        _yaz(HATIRLATICI_DOSYASI, liste)
    return gelenler


# ==============================================================================
# GİRİŞ NOKTASI
# ==============================================================================
def calisma_kocu_yanitla(metin: str, oturum):
    if not metin or len(metin) > 300:
        return None, None
    try:
        sonuc = _test_cevapla(metin, oturum)
        if sonuc:
            return sonuc
    except Exception:
        oturum.pop("arex_test", None)
    t = _kucult(metin)
    for fonk in (lambda: _defter_testi_baslat(t, oturum), lambda: _yanlis_defteri(t, metin),
                 lambda: _test_baslat(t, oturum), lambda: _hatirlatici(t, metin), lambda: _hedef_ayarla(t),
                 lambda: _rapor(t), lambda: _calisma_kaydi(t)):
        try:
            sonuc = fonk()
        except Exception:
            sonuc = None
        if sonuc:
            return sonuc[0], sonuc[1] or "📝 Çalışma Koçu"
    return None, None
