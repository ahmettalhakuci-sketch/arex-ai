# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 21: ÖĞRENCİ ARAÇLARI (modul_21_ogrenci_araclari.py)
==============================================================================
  1. 🧮 Net hesaplama   : "40 doğru 12 yanlış kaç net", "lgs 15 doğru 3 yanlış",
                          "türkçe 30 doğru 6 yanlış matematik 22 doğru 8 yanlış"
                          (YKS/TYT/AYT/KPSS/ALES: 4 yanlış 1 doğruyu götürür; LGS: 3 yanlış)
  2. 📅 Sınav geri sayımı: "fizik sınavım 5 aralıkta", "sınav tarihim 20.06.2027",
                          "sınavlarıma kaç gün kaldı", "#2 sınavı sil"
  3. 🍅 Pomodoro         : "pomodoro başlat", "50 dakika pomodoro" → süre bitince hatırlatır
  4. 🃏 Kelime kartları  : "kart ekle: apple = elma; book = kitap", "kartlarım",
                          "kartları çalış" (Leitner kutuları: bildiklerin seyrek, bilmediklerin sık gelir)

Giriş noktası: ogrenci_araclari_yanitla(metin, oturum) -> (yanıt, etiket) | (None, None)
Hiçbir dış servis kullanılmaz; veriler yerel JSON dosyalarında tutulur.
"""

import os
import random
import re
from datetime import date, datetime, timedelta

import modul_18_calisma_kocu as m18

_KOK = os.path.dirname(os.path.abspath(__file__))
SINAV_DOSYASI = os.path.join(_KOK, "arex_sinavlar.json")
KART_DOSYASI = os.path.join(_KOK, "arex_kartlar.json")

_AYLAR = m18._AYLAR
_AY_NO = m18._AY_NO
_GUNLER = m18._GUNLER
_kucult = m18._kucult
_oku = m18._oku
_yaz = m18._yaz
_simdi = m18._simdi


# ==============================================================================
# 1. NET HESAPLAMA
# ==============================================================================
_NET_DERSLER = ("türkçe", "turkce", "matematik", "mat", "geometri", "fizik", "kimya", "biyoloji", "tarih",
                "coğrafya", "cografya", "felsefe", "din", "fen", "sosyal", "inkılap", "ingilizce", "edebiyat",
                "genel kültür", "genel yetenek", "sayısal", "sözel", "eşit ağırlık")
_PARCA = re.compile(r"(?:([a-zçğıöşü]+(?:\s+[a-zçğıöşü]+)?)\s+)?(\d{1,3})\s*d(?:oğru|ogru)?\b[\s,]*(\d{1,3})\s*y(?:anlış|anlis|anlıs)?\b"
                    r"(?:[\s,]*(\d{1,3})\s*b(?:oş|os)?\b)?")


def _net_hesapla(t: str):
    if not (re.search(r"doğru|dogru", t) and re.search(r"yanlış|yanlis|yanlıs", t)) and "net" not in t:
        return None
    parcalar = _PARCA.findall(t)
    if not parcalar:
        return None
    lgs = bool(re.search(r"\blgs\b|teog|ortaokul|8\.\s*sınıf", t))
    bolen = 3 if lgs else 4
    sinav = "LGS" if lgs else next((s.upper() for s in ("tyt", "ayt", "ydt", "kpss", "ales", "dgs", "yks", "msü", "msu")
                                    if re.search(r"\b" + s + r"\b", t)), "YKS / genel")
    satirlar, toplam_net, toplam_d, toplam_y = [], 0.0, 0, 0
    for ders, d, y, b in parcalar:
        d, y = int(d), int(y)
        if d + y > 200:
            return "🤔 Bu sayılar bir sınav için fazla büyük görünüyor; tekrar yazar mısın?", "🧮 Net Hesaplama"
        net = d - y / bolen
        toplam_net += net
        toplam_d += d
        toplam_y += y
        ad = ""
        if ders:
            kelimeler = [k for k in ders.split() if any(k.startswith(n.split()[0][:3]) for n in _NET_DERSLER)]
            ad = " ".join(kelimeler).title()
        satirlar.append((ad, d, y, int(b) if b else None, net))
    baslik = f"🧮 **Net Hesabı** — {sinav} ({bolen} yanlış 1 doğruyu götürür)"
    if len(satirlar) == 1:
        ad, d, y, b, net = satirlar[0]
        kayip = y / bolen
        metin = [baslik, "", f"- ✅ Doğru: **{d}** · ❌ Yanlış: **{y}**" + (f" · ⚪ Boş: **{b}**" if b is not None else ""),
                 f"- 📉 Yanlışların götürdüğü: **{_sayi(kayip)}** doğru",
                 f"- 🎯 **Net: {_sayi(net)}**"]
        if b is not None and d + y + b:
            metin.append(f"- 📊 Başarı oranı: **%{round(max(net, 0) / (d + y + b) * 100)}**")
        if y >= bolen:
            metin.append(f"\n💡 Emin olmadığın {bolen} soruyu boş bıraksaydın, net kaybın yaklaşık **1** azalırdı. "
                         "Tahmin ederken en az iki şıkkı eleyebiliyorsan işaretlemek genelde kazandırır.")
        return "\n".join(metin), "🧮 Net Hesaplama"
    metin = [baslik, "", "| Ders | Doğru | Yanlış | Net |", "|---|---|---|---|"]
    for i, (ad, d, y, b, net) in enumerate(satirlar, 1):
        metin.append(f"| {ad or f'{i}. bölüm'} | {d} | {y} | **{_sayi(net)}** |")
    metin.append(f"| **Toplam** | **{toplam_d}** | **{toplam_y}** | **{_sayi(toplam_net)}** |")
    en_iyi = max(satirlar, key=lambda s: s[4])
    if en_iyi[0]:
        metin.append(f"\n🌟 En yüksek netin **{en_iyi[0]}** dersinde. Tebrikler!")
    return "\n".join(metin), "🧮 Net Hesaplama"


def _sayi(x: float) -> str:
    x = round(x, 2)
    return str(int(x)) if x == int(x) else f"{x:.2f}".rstrip("0").replace(".", ",")


# ==============================================================================
# 2. SINAV GERİ SAYIMI
# ==============================================================================
def _tarih_bul(t: str):
    bugun = _simdi().date()
    m = re.search(r"(\d{1,2})[./](\d{1,2})(?:[./](\d{4}))?", t)
    if m:
        gun, ay, yil = int(m.group(1)), int(m.group(2)), m.group(3)
    else:
        m = re.search(r"(\d{1,2})\s*(" + "|".join(_AY_NO) + r")\w*(?:\s+(\d{4}))?", t)
        if not m:
            return None
        gun, ay, yil = int(m.group(1)), _AY_NO[m.group(2)], m.group(3)
    try:
        tarih = date(int(yil) if yil else bugun.year, ay, gun)
    except ValueError:
        return None
    if not yil and tarih < bugun:
        tarih = tarih.replace(year=tarih.year + 1)
    return tarih


def _kalan_yazi(tarih: date) -> str:
    gun = (tarih - _simdi().date()).days
    if gun < 0:
        return "geçti"
    if gun == 0:
        return "**BUGÜN!** 🍀"
    if gun == 1:
        return "**yarın!**"
    hafta = f" (~{gun // 7} hafta)" if gun >= 14 else ""
    return f"**{gun} gün** kaldı{hafta}"


def _sinav(t: str, ham: str):
    if "hatırlat" in t or "hatirlat" in t:
        return None
    liste = _oku(SINAV_DOSYASI, [])
    m = re.search(r"#?(\d+)\s*(?:nolu|numaralı)?\s*sınav\w*\s*sil", t)
    if m:
        no = int(m.group(1))
        yeni = [s for s in liste if s["no"] != no]
        if len(yeni) == len(liste):
            return f"📅 #{no} numaralı sınav kaydı bulamadım.", "📅 Sınav Takvimi"
        _yaz(SINAV_DOSYASI, yeni)
        return f"🗑️ #{no} numaralı sınav silindi.", "📅 Sınav Takvimi"

    sorgu = re.search(r"sınav\w*\s*(?:(?:ne\s*kadar|kaç\s*gün)\s*kal|takvim)|sınavlarım\b|sınavlarımı\s*göster", t)
    if sorgu:
        gelecek = sorted((s for s in liste if date.fromisoformat(s["tarih"]) >= _simdi().date()), key=lambda s: s["tarih"])
        if not gelecek:
            return ("📅 Kayıtlı sınavın yok. Eklemek için örneğin: *\"fizik sınavım 5 aralıkta\"* "
                    "veya *\"YKS sınavım 20.06.2027\"*"), "📅 Sınav Takvimi"
        satirlar = ["📅 **Sınav Takvimin**", ""]
        for s in gelecek[:10]:
            d = date.fromisoformat(s["tarih"])
            satirlar.append(f"- **#{s['no']} {s['ad']}** — {d.day} {_AYLAR[d.month - 1]} {_GUNLER[d.weekday()]}: {_kalan_yazi(d)}")
        ilk = date.fromisoformat(gelecek[0]["tarih"])
        kalan = (ilk - _simdi().date()).days
        if kalan > 0:
            ayar = _oku(m18.AYAR_DOSYASI, {})
            hedef = int(ayar.get("gunluk_soru_hedefi", 0) or 0)
            if hedef:
                satirlar.append(f"\n🎯 Günlük {hedef} soru hedefinle ilk sınavına kadar yaklaşık **{hedef * kalan} soru** çözersin.")
        satirlar.append("\nSilmek için: *\"#1 sınavı sil\"*")
        return "\n".join(satirlar), "📅 Sınav Takvimi"

    if not re.search(r"sınav\w*|\b(?:yks|tyt|ayt|lgs|kpss|ales)\b", t):
        return None
    if not re.search(r"sınavım|sınav\s*tarih|sınavı\s*(?:var|olacak)|\b(?:yks|tyt|ayt|lgs|kpss|ales)\b\s*(?:sınavım\s*)?(?:tarih|\d)", t):
        return None
    tarih = _tarih_bul(t)
    if tarih is None or re.search(r"\?|kaç|ne zaman", t):
        return None
    if (tarih - _simdi().date()).days > 800:
        return "📅 Bu tarih çok ileride görünüyor; doğru yazdığından emin misin?", "📅 Sınav Takvimi"
    ad_m = re.search(r"([a-zçğıöşü0-9]+(?:\s+[a-zçğıöşü]+)?)\s+sınav", t)
    ad = ad_m.group(1) if ad_m else None
    if ad:
        ad = re.sub(r"^(?:benim|bir|yarın|yarin|\d+\s*\w+)\s*", "", ad).strip()
    if not ad:
        kisalt = re.search(r"\b(yks|tyt|ayt|lgs|kpss|ales)\b", t)
        ad = kisalt.group(1) if kisalt else "Sınav"
    ad = ad.upper() if ad in ("yks", "tyt", "ayt", "lgs", "kpss", "ales") else ad.title()
    if not ad.lower().endswith("sınav") and ad != "Sınav" and not ad.isupper():
        ad += " sınavı"
    no = max([s["no"] for s in liste] + [0]) + 1
    liste.append({"no": no, "ad": ad, "tarih": tarih.isoformat()})
    _yaz(SINAV_DOSYASI, liste)
    gun = (tarih - _simdi().date()).days
    oneri = ""
    if gun > 1:
        oneri = (f"\n\n💡 Plan önerisi: kalan sürenin ilk %60'ında ({max(1, round(gun * 0.6))} gün) konu çalış, "
                 f"sonraki %30'unda soru çöz, son {max(1, round(gun * 0.1))} günü deneme ve tekrar için ayır.")
    return (f"📅 **Kaydettim (#{no}):** {ad} — {tarih.day} {_AYLAR[tarih.month - 1]} {tarih.year}, "
            f"{_GUNLER[tarih.weekday()]} → {_kalan_yazi(tarih)}{oneri}\n\n"
            "Kalan süreyi görmek için: *\"sınavlarıma kaç gün kaldı\"*"), "📅 Sınav Takvimi"


# ==============================================================================
# 3. POMODORO
# ==============================================================================
def _pomodoro(t: str):
    if not re.search(r"pomodoro|odak\s*modu|odaklanma\s*(?:modu|süresi)\s*başlat", t):
        return None
    ayar = _oku(m18.AYAR_DOSYASI, {})
    bugun = _simdi().date().isoformat()
    sayac = ayar.get("pomodoro", {})
    if re.search(r"kaç\s*pomodoro|pomodoro\w*\s*(?:sayı|say|durum)", t):
        n = sayac.get(bugun, 0)
        return (f"🍅 Bugün **{n}** pomodoro başlattın (≈ {n * 25} dk odak)." if n
                else "🍅 Bugün henüz pomodoro başlatmadın. *\"pomodoro başlat\"* yazman yeterli."), "🍅 Pomodoro"
    m = re.search(r"(\d{1,3})\s*(?:dakika|dk)", t)
    dk = int(m.group(1)) if m else 25
    if not 5 <= dk <= 120:
        return "🍅 Pomodoro süresi 5 ile 120 dakika arasında olmalı.", "🍅 Pomodoro"
    mola = 5 if dk <= 30 else 10
    simdi = _simdi().replace(second=0, microsecond=0)
    bitis = simdi + timedelta(minutes=dk)
    liste = _oku(m18.HATIRLATICI_DOSYASI, [])
    no = max([h["no"] for h in liste] + [0]) + 1
    liste.append({"no": no, "baslik": f"🍅 Pomodoro bitti! {mola} dakika mola ver", "zaman": bitis.isoformat(timespec="minutes"),
                  "bildirildi": False})
    _yaz(m18.HATIRLATICI_DOSYASI, liste)
    sayac = {k: v for k, v in sayac.items() if k >= (_simdi().date() - timedelta(days=30)).isoformat()}
    sayac[bugun] = sayac.get(bugun, 0) + 1
    ayar["pomodoro"] = sayac
    _yaz(m18.AYAR_DOSYASI, ayar)
    n = sayac[bugun]
    uzun_mola = "\n- 🛋️ Bu 4. pomodoron — bitince **15-30 dk uzun mola** hak ettin!" if n % 4 == 0 else ""
    return (f"🍅 **Pomodoro başladı!** ({dk} dk)\n\n"
            f"- ⏱️ Bitiş: **{bitis:%H:%M}** — o zaman ekranda hatırlatacağım 🔔\n"
            f"- 📵 Telefonu sessize al, tek bir işe odaklan\n"
            f"- ☕ Sonra **{mola} dk** mola{uzun_mola}\n"
            f"- 📈 Bugünkü pomodoro sayın: **{n}**\n\n"
            f"Bitince çalıştığını kaydetmeyi unutma: *\"{dk} dakika matematik çalıştım\"*"), "🍅 Pomodoro"


# ==============================================================================
# 4. KELİME / BİLGİ KARTLARI (LEITNER)
# ==============================================================================
_ARALIK_GUN = {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}


def _kart_norm(s: str) -> str:
    s = _kucult(s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _kart_dogru_mu(verilen: str, dogru: str) -> bool:
    v = _kart_norm(verilen)
    secenekler = [_kart_norm(x) for x in re.split(r"[,/;]| veya ", dogru) if x.strip()]
    if v in secenekler:
        return True
    try:
        from thefuzz import fuzz
        return any(len(s) >= 4 and fuzz.ratio(v, s) >= 85 for s in secenekler)
    except Exception:
        return False


def _kartlar(t: str, ham: str, oturum):
    # Ekle: "kart ekle: apple = elma; book = kitap"
    m = re.match(r"\s*(?:kart|kelime|bilgi\s*kartı)\s*ekle\s*[:\-]?\s*(.+)$", ham, flags=re.I | re.S)
    if m:
        kartlar = _oku(KART_DOSYASI, [])
        eklenen = []
        for parca in re.split(r"[;\n]", m.group(1)):
            if "=" not in parca:
                continue
            on, arka = (x.strip() for x in parca.split("=", 1))
            if not on or not arka or len(on) > 120 or len(arka) > 200:
                continue
            mevcut = next((k for k in kartlar if _kart_norm(k["on"]) == _kart_norm(on)), None)
            if mevcut:
                mevcut["arka"] = arka
            else:
                kartlar.append({"on": on, "arka": arka, "kutu": 1, "sonraki": _simdi().date().isoformat()})
            eklenen.append(f"**{on}** → {arka}")
        if not eklenen:
            return ("🃏 Biçim: *\"kart ekle: apple = elma; book = kitap\"* (her kart `ön = arka`, "
                    "birden fazlası `;` ile ayrılır)"), "🃏 Kelime Kartları"
        _yaz(KART_DOSYASI, kartlar)
        return (f"🃏 **{len(eklenen)} kart eklendi** (toplam {len(kartlar)}):\n\n- " + "\n- ".join(eklenen[:15])
                + "\n\nÇalışmak için: *\"kartları çalış\"*"), "🃏 Kelime Kartları"

    m = re.search(r"(.+?)\s+kartını\s+sil", ham, flags=re.I)
    if m:
        kartlar = _oku(KART_DOSYASI, [])
        hedef = _kart_norm(m.group(1))
        yeni = [k for k in kartlar if _kart_norm(k["on"]) != hedef]
        if len(yeni) == len(kartlar):
            return f"🃏 \"{m.group(1).strip()}\" adında bir kart bulamadım.", "🃏 Kelime Kartları"
        _yaz(KART_DOSYASI, yeni)
        return f"🗑️ \"{m.group(1).strip()}\" kartı silindi.", "🃏 Kelime Kartları"

    if re.search(r"^(?:kelime\s*)?kartlarım\b|kartlarımı\s*(?:göster|listele)", t):
        kartlar = _oku(KART_DOSYASI, [])
        if not kartlar:
            return "🃏 Henüz kartın yok. Örnek: *\"kart ekle: apple = elma; book = kitap\"*", "🃏 Kelime Kartları"
        bugun = _simdi().date().isoformat()
        vadesi = sum(1 for k in kartlar if k["sonraki"] <= bugun)
        kutular = [sum(1 for k in kartlar if k["kutu"] == i) for i in range(1, 6)]
        satirlar = [f"🃏 **Kartların** — toplam {len(kartlar)}, bugün tekrar edilecek **{vadesi}**", "",
                    "Kutu 1 (yeni) → 5 (ezber): " + " · ".join(f"{i}️⃣ {n}" for i, n in enumerate(kutular, 1)), ""]
        for k in kartlar[:20]:
            satirlar.append(f"- **{k['on']}** → {k['arka']} · kutu {k['kutu']}")
        if len(kartlar) > 20:
            satirlar.append(f"- … ve {len(kartlar) - 20} kart daha")
        return "\n".join(satirlar), "🃏 Kelime Kartları"

    if re.search(r"kart\w*\s*(?:çalış|calis|tekrar|sor|başlat)|kelime\s*(?:çalış|tekrar|ezber)\w*\s*(?:başlat|yapalım|yap)?$", t):
        kartlar = _oku(KART_DOSYASI, [])
        if not kartlar:
            return "🃏 Önce kart eklemelisin: *\"kart ekle: apple = elma; book = kitap\"*", "🃏 Kelime Kartları"
        bugun = _simdi().date().isoformat()
        sira = [i for i, k in enumerate(kartlar) if k["sonraki"] <= bugun]
        ek = ""
        if not sira:
            sira = sorted(range(len(kartlar)), key=lambda i: kartlar[i]["kutu"])[:10]
            ek = "Bugünlük tekrarın bitmişti; yine de en zayıf kartlarından soruyorum.\n\n"
        random.shuffle(sira)
        sira = sira[:10]
        oturum.pop("arex_test", None)
        oturum["arex_kart"] = {"sira": sira, "i": 0, "dogru": 0}
        return (f"🃏 **Kart tekrarı başladı** ({len(sira)} kart)\n\n{ek}{_kart_sorusu(kartlar, oturum['arex_kart'])}",
                "🃏 Kelime Kartları")
    return None


def _kart_sorusu(kartlar, durum) -> str:
    k = kartlar[durum["sira"][durum["i"]]]
    return (f"**{durum['i'] + 1}/{len(durum['sira'])}** — **{k['on']}** ❓\n\n"
            "_Cevabını yaz · \"bilmiyorum\" · \"bitir\"_")


def _kart_cevapla(metin: str, oturum):
    durum = oturum.get("arex_kart")
    if not durum:
        return None
    t = _kucult(metin)
    kartlar = _oku(KART_DOSYASI, [])
    if durum["i"] >= len(durum["sira"]) or durum["sira"][durum["i"]] >= len(kartlar):
        oturum.pop("arex_kart", None)
        return None
    if re.fullmatch(r"(?:testi\s*|tekrar\w*\s*)?(?:bitir|çık|cik|dur|iptal|yeter)\W*", t):
        return _kart_bitir(oturum, len(durum["sira"]), erken=True)
    if len(metin) > 80 or "?" in metin:
        oturum.pop("arex_kart", None)  # başka bir soru sordu → tekrarı bırak, normal sohbete geç
        return None
    k = kartlar[durum["sira"][durum["i"]]]
    bugun = _simdi().date()
    if re.fullmatch(r"(?:bilmiyorum|geç|gec|pas|bilemedim|hatırlamıyorum)\W*", t):
        dogru = False
    else:
        dogru = _kart_dogru_mu(metin, k["arka"])
    if dogru:
        k["kutu"] = min(5, k["kutu"] + 1)
        durum["dogru"] += 1
        geri = random.choice(["✅ Doğru!", "✅ Harika!", "✅ Bildin!", "✅ Süper!"]) + f" **{k['on']}** → {k['arka']}"
    else:
        k["kutu"] = 1
        geri = f"❌ Doğrusu: **{k['on']}** → **{k['arka']}** (bu kart yarın tekrar gelecek)"
    k["sonraki"] = (bugun + timedelta(days=max(1, _ARALIK_GUN[k["kutu"]]))).isoformat()
    _yaz(KART_DOSYASI, kartlar)
    durum["i"] += 1
    if durum["i"] >= len(durum["sira"]):
        sonuc, etiket = _kart_bitir(oturum, len(durum["sira"]))
        return f"{geri}\n\n{sonuc}", etiket
    return f"{geri}\n\n{_kart_sorusu(kartlar, durum)}", "🃏 Kelime Kartları"


def _kart_bitir(oturum, toplam, erken=False):
    durum = oturum.pop("arex_kart", {}) or {}
    cevaplanan = durum.get("i", 0)
    dogru = durum.get("dogru", 0)
    if not cevaplanan:
        return "🃏 Kart tekrarını bitirdim. İstediğinde *\"kartları çalış\"* yaz.", "🃏 Kelime Kartları"
    oran = round(dogru / cevaplanan * 100)
    yorum = "🌟 Mükemmel!" if oran >= 90 else "👏 Gayet iyi!" if oran >= 60 else "💪 Tekrar ettikçe oturacak."
    return (f"🏁 **Tekrar bitti{' (erken)' if erken else ''}:** {cevaplanan} karttan **{dogru}** doğru (%{oran}) {yorum}\n\n"
            "Bildiğin kartlar daha seyrek, bilmediklerin daha sık karşına çıkacak (Leitner yöntemi)."), "🃏 Kelime Kartları"


# ==============================================================================
# GİRİŞ NOKTASI
# ==============================================================================
def ogrenci_araclari_yanitla(metin: str, oturum):
    if not metin or len(metin) > 1500:
        return None, None
    try:
        sonuc = _kart_cevapla(metin, oturum)
        if sonuc:
            return sonuc
    except Exception:
        oturum.pop("arex_kart", None)
    if len(metin) > 400 and not re.match(r"\s*(?:kart|kelime)\s*ekle", metin, flags=re.I):
        return None, None
    t = _kucult(metin)
    for fonk in (lambda: _kartlar(t, metin, oturum), lambda: _pomodoro(t), lambda: _net_hesapla(t),
                 lambda: _sinav(t, metin)):
        try:
            sonuc = fonk()
        except Exception:
            sonuc = None
        if sonuc:
            return sonuc
    return None, None
