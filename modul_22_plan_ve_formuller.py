# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 22: ÇALIŞMA PROGRAMI & FORMÜL KARTLARI (modul_22_plan_ve_formuller.py)
==============================================================================
  1. 🗓️ Haftalık program : "bana haftalık çalışma programı hazırla", "günde 3 saat program yap"
                          → sınav takviminden (Modül 21) sınav türünü, deneme sonuçlarından zayıf
                            dersi, çalışma takibinden (Modül 18) bu hafta az çalışılan dersleri bulur;
                            40 dk oturum + 10 dk mola düzeninde 7 günlük program çıkarır ve saklar.
                          "bugün ne çalışayım" → kayıtlı programdan bugünün oturumları
  2. 📐 Formül kartları  : "türev formülleri", "trigonometri formülleri", "alan formülleri",
                          "fizik formülleri", "kimya formülleri", "formül kartları"
                          → internetsiz, anında, doğrulanmış özet

  3. 🎯 Panelim         : "panelim", "durumum", "bugünkü özetim" → sınav geri sayımı, bugünkü program,
                          günlük hedef, seri, son deneme, yanlış defteri, kart tekrarı, sıradaki hatırlatıcı
                          ve "sıradaki adım" önerisi tek kartta

Giriş noktası: plan_ve_formul_yanitla(metin) -> (yanıt, etiket) | (None, None)
"""

import re
from datetime import date, datetime, timedelta

import modul_18_calisma_kocu as m18
import modul_21_ogrenci_araclari as m21

_kucult = m18._kucult
_GUNLER = m18._GUNLER
_OTURUM_DK = 40

_DERS_SETLERI = {
    "LGS": ["Matematik", "Türkçe", "Fen Bilimleri", "İnkılap Tarihi", "İngilizce", "Din Kültürü"],
    "AYT": ["Matematik", "Fizik", "Kimya", "Biyoloji", "Edebiyat", "Tarih", "Coğrafya"],
    "YKS": ["Matematik", "Türkçe", "Fizik", "Kimya", "Biyoloji", "Tarih", "Coğrafya"],
    "KPSS": ["Matematik", "Türkçe", "Tarih", "Coğrafya", "Vatandaşlık", "Güncel Bilgiler"],
    "GENEL": ["Matematik", "Türkçe", "Fen", "Sosyal", "İngilizce"],
}


def _ders_esle(ad: str, dersler) -> str:
    k = _kucult(ad)
    for d in dersler:
        dk = _kucult(d)
        if k[:4] and (dk.startswith(k[:4]) or k.startswith(dk[:4])):
            return d
    if "edebiyat" in k or "türk dili" in k:
        return next((d for d in dersler if d in ("Edebiyat", "Türkçe")), None)
    return None


def _sinav_turu(t: str):
    for anahtar in ("lgs", "ayt", "kpss", "tyt", "yks"):
        if re.search(r"\b" + anahtar + r"\b", t):
            return "YKS" if anahtar == "tyt" else anahtar.upper()
    bugun = m18._simdi().date()
    for s in sorted(m18._oku(m21.SINAV_DOSYASI, []), key=lambda s: s["tarih"]):
        if date.fromisoformat(s["tarih"]) >= bugun:
            ad = _kucult(s["ad"])
            for anahtar in ("lgs", "ayt", "kpss", "tyt", "yks"):
                if anahtar in ad:
                    return "YKS" if anahtar == "tyt" else anahtar.upper()
    return "GENEL"


def _program_olustur(t: str):
    tur = _sinav_turu(t)
    dersler = list(_DERS_SETLERI[tur])
    agirlik = {d: 1.0 for d in dersler}
    if tur in ("YKS", "AYT", "LGS", "KPSS"):
        agirlik["Matematik"] += 0.5
    if tur in ("YKS", "LGS", "KPSS"):
        agirlik["Türkçe"] += 0.3
    gerekceler = []

    # Deneme sonuçlarından zayıf ders
    denemeler = m18._oku(m21.DENEME_DOSYASI, [])
    ortalama = {}
    for d in denemeler[-6:]:
        for ad, n in d.get("dersler", {}).items():
            ortalama.setdefault(ad, []).append(n)
    if len(ortalama) > 1:
        zayif_ad = min(ortalama, key=lambda a: sum(ortalama[a]) / len(ortalama[a]))
        zayif = _ders_esle(zayif_ad, dersler)
        if zayif:
            agirlik[zayif] += 0.8
            gerekceler.append(f"denemelerde ortalaması en düşük ders **{zayif}** → ek oturum")

    # Bu hafta az çalışılan dersler
    _, haftalik, _ = m18._gunluk_toplamlar()
    if haftalik:
        calisilan = {_ders_esle(ad, dersler) for ad in haftalik}
        az = [d for d in dersler if d not in calisilan][:3]
        for d in az:
            agirlik[d] += 0.3
        if az:
            gerekceler.append("bu hafta hiç kayıt girmediğin dersler (" + ", ".join(az) + ") → öncelik")

    # Kullanıcının istediği ek ağırlık: "matematiğe ağırlık ver"
    for d in dersler:
        if re.search(_kucult(d)[:5] + r"\w*\s*(?:ağırlık|agirlik|daha\s*çok|öncelik)", t):
            agirlik[d] += 1.0
            gerekceler.append(f"isteğin üzerine **{d}** ağırlıklı")

    # Günlük süre
    m = re.search(r"günde\s*(\d+(?:[.,]5)?)\s*saat", t)
    hafta_ici = float(m.group(1).replace(",", ".")) if m else 2.0
    m = re.search(r"hafta\s*sonu\s*(\d+(?:[.,]5)?)\s*saat", t)
    hafta_sonu = float(m.group(1).replace(",", ".")) if m else (hafta_ici + 2 if not re.search(r"günde", t) else hafta_ici)
    if not 0.5 <= hafta_ici <= 12 or not 0.5 <= hafta_sonu <= 14:
        return "🗓️ Günlük çalışma süresi 0,5 ile 12 saat arasında olmalı.", "🗓️ Çalışma Programı"
    oturum_sayisi = [max(1, round(hafta_ici * 60 / (_OTURUM_DK + 10)))] * 5 + [max(1, round(hafta_sonu * 60 / (_OTURUM_DK + 10)))] * 2

    # Yaklaşan sınav → pazar deneme
    yakin_sinav = None
    bugun = m18._simdi().date()
    for s in sorted(m18._oku(m21.SINAV_DOSYASI, []), key=lambda s: s["tarih"]):
        tarih = date.fromisoformat(s["tarih"])
        if tarih >= bugun:
            yakin_sinav = (s["ad"], (tarih - bugun).days)
            break
    deneme_gunu = tur != "GENEL"  # sınava hazırlananlar için haftada bir deneme

    # Ağırlıklı dağıtım (en büyük kalan yöntemi) + aynı gün ardışık tekrar yok
    toplam_oturum = sum(oturum_sayisi) - (3 if deneme_gunu and oturum_sayisi[6] >= 3 else 0)
    toplam_agirlik = sum(agirlik.values())
    paylar = {d: toplam_oturum * w / toplam_agirlik for d, w in agirlik.items()}
    kota = {d: int(p) for d, p in paylar.items()}
    for d in sorted(paylar, key=lambda d: paylar[d] - kota[d], reverse=True)[:toplam_oturum - sum(kota.values())]:
        kota[d] += 1
    program = []
    kalan = dict(kota)
    son_ders = None
    for gun_i, n in enumerate(oturum_sayisi):
        gun = []
        if gun_i == 6 and deneme_gunu and n >= 3:
            gun.append("📝 Deneme sınavı (2 sa) + yanlış analizi")
            n -= 3
        for _ in range(n):
            adaylar = sorted((d for d in kalan if kalan[d] > 0), key=lambda d: (-kalan[d], -agirlik[d]))
            if not adaylar:
                break
            secim = next((d for d in adaylar if d != son_ders and d not in gun), None) or \
                next((d for d in adaylar if d != son_ders), adaylar[0])
            gun.append(secim)
            kalan[secim] -= 1
            son_ders = secim
        program.append(gun)

    ayar = m18._oku(m18.AYAR_DOSYASI, {})
    ayar["haftalik_plan"] = {"olusturma": bugun.isoformat(), "tur": tur, "gunler": program}
    m18._yaz(m18.AYAR_DOSYASI, ayar)

    baslik = {"GENEL": "Genel"}.get(tur, tur)
    satirlar = [f"🗓️ **Haftalık Çalışma Programın** ({baslik} · {_OTURUM_DK} dk oturum + 10 dk mola)", ""]
    if yakin_sinav:
        satirlar.append(f"📅 En yakın sınavın: **{yakin_sinav[0]}** — {yakin_sinav[1]} gün kaldı")
    if gerekceler:
        satirlar.append("🧠 Kişiselleştirme: " + "; ".join(gerekceler))
    satirlar += ["", "| Gün | Oturumlar |", "|---|---|"]
    bugun_i = bugun.weekday()
    for i, gun in enumerate(program):
        ad = _GUNLER[i] + (" ⬅️ bugün" if i == bugun_i else "")
        satirlar.append(f"| **{ad}** | {' → '.join(gun) if gun else '🛋️ Dinlenme'} |")
    dagilim = {}
    for gun in program:
        for d in gun:
            if not d.startswith("📝"):
                dagilim[d] = dagilim.get(d, 0) + 1
    satirlar += ["", "⏱️ Haftalık süre: " + " · ".join(
        f"{d} {m21._sayi(n * _OTURUM_DK / 60)} sa" for d, n in sorted(dagilim.items(), key=lambda x: -x[1]))]
    satirlar.append("\n💡 Her oturumda *\"pomodoro 40 dakika\"* başlatabilir, bitince *\"40 dakika matematik çalıştım\"* "
                    "diye kaydedebilirsin. Her gün *\"bugün ne çalışayım\"* yaz, programdan bugünkü dersleri söyleyeyim.")
    satirlar.append("Süreyi değiştirmek için: *\"günde 3 saat hafta sonu 5 saat program yap\"*")
    return "\n".join(satirlar), "🗓️ Çalışma Programı"


def _bugun_ne_calisayim(t: str):
    if not re.search(r"bugün\s*(?:ne|hangi\s*ders\w*)\s*çalış|bugünkü\s*(?:program|ders)|bugün\s*programımda", t):
        return None
    plan = m18._oku(m18.AYAR_DOSYASI, {}).get("haftalik_plan")
    if not plan:
        return ("🗓️ Henüz bir programın yok. *\"bana haftalık çalışma programı hazırla\"* yaz, "
                "senin için sınavına ve deneme sonuçlarına göre hazırlayayım."), "🗓️ Çalışma Programı"
    bugun = m18._simdi().date()
    gun = plan["gunler"][bugun.weekday()]
    _, dersler, _ = m18._gunluk_toplamlar(1)
    yapilan = sum(v["dk"] for v in dersler.values())
    satirlar = [f"📚 **Bugün ({_GUNLER[bugun.weekday()]}) programın:**", ""]
    if not gun:
        satirlar.append("🛋️ Bugün dinlenme günün. Hafif tekrar yapabilirsin.")
    for i, d in enumerate(gun, 1):
        satirlar.append(f"{i}. {d}" + ("" if d.startswith("📝") else f" — {_OTURUM_DK} dk"))
    if yapilan:
        satirlar.append(f"\n✅ Bugün şimdiye kadar **{yapilan} dk** çalışma kaydettin.")
    if (bugun - date.fromisoformat(plan["olusturma"])).days >= 7:
        satirlar.append("\n🔄 Programın 1 haftadan eski; yeni deneme sonuçlarına göre güncellemek için "
                        "*\"haftalık program hazırla\"* yaz.")
    return "\n".join(satirlar), "🗓️ Çalışma Programı"


# ==============================================================================
# FORMÜL KARTLARI
# ==============================================================================
FORMULLER = {
    "türev": ("📐 Türev Formülleri", [
        "(c)′ = 0  ·  (x)′ = 1  ·  (xⁿ)′ = n·xⁿ⁻¹",
        "(f ± g)′ = f′ ± g′  ·  (c·f)′ = c·f′",
        "Çarpım: (f·g)′ = f′·g + f·g′",
        "Bölüm: (f/g)′ = (f′·g − f·g′) / g²",
        "Zincir: (f(g(x)))′ = f′(g(x))·g′(x)",
        "(eˣ)′ = eˣ  ·  (aˣ)′ = aˣ·ln a  ·  (ln x)′ = 1/x  ·  (logₐx)′ = 1/(x·ln a)",
        "(sin x)′ = cos x  ·  (cos x)′ = −sin x  ·  (tan x)′ = 1/cos²x = 1 + tan²x  ·  (cot x)′ = −1/sin²x",
        "(√x)′ = 1/(2√x)",
        "Teğet eğimi: m = f′(a)  ·  Ekstremum adayı: f′(x) = 0",
    ]),
    "integral": ("∫ İntegral Formülleri", [
        "∫xⁿ dx = xⁿ⁺¹/(n+1) + C  (n ≠ −1)",
        "∫1/x dx = ln|x| + C  ·  ∫eˣ dx = eˣ + C  ·  ∫aˣ dx = aˣ/ln a + C",
        "∫sin x dx = −cos x + C  ·  ∫cos x dx = sin x + C",
        "∫1/cos²x dx = tan x + C  ·  ∫1/sin²x dx = −cot x + C",
        "∫(f ± g) dx = ∫f dx ± ∫g dx  ·  ∫c·f dx = c·∫f dx",
        "Belirli integral: ∫ₐᵇ f(x) dx = F(b) − F(a)",
        "Kısmi integral: ∫u dv = u·v − ∫v du",
    ]),
    "trigonometri": ("📐 Trigonometri Formülleri", [
        "sin²x + cos²x = 1  ·  tan x = sin x / cos x  ·  cot x = 1 / tan x",
        "sin 30° = 1/2 · sin 45° = √2/2 · sin 60° = √3/2",
        "cos 30° = √3/2 · cos 45° = √2/2 · cos 60° = 1/2",
        "tan 30° = √3/3 · tan 45° = 1 · tan 60° = √3",
        "sin(a ± b) = sin a·cos b ± cos a·sin b",
        "cos(a ± b) = cos a·cos b ∓ sin a·sin b",
        "sin 2x = 2·sin x·cos x  ·  cos 2x = cos²x − sin²x = 1 − 2sin²x = 2cos²x − 1",
        "Sinüs teoremi: a/sin A = b/sin B = c/sin C = 2R",
        "Kosinüs teoremi: a² = b² + c² − 2bc·cos A",
        "Üçgen alanı: (1/2)·b·c·sin A",
    ]),
    "logaritma": ("📈 Logaritma & Üslü Sayılar", [
        "logₐx = y  ⟺  aʸ = x  (a > 0, a ≠ 1, x > 0)",
        "logₐ(x·y) = logₐx + logₐy  ·  logₐ(x/y) = logₐx − logₐy",
        "logₐ(xⁿ) = n·logₐx  ·  logₐ1 = 0  ·  logₐa = 1",
        "Taban değiştirme: logₐx = log x / log a",
        "aᵐ·aⁿ = aᵐ⁺ⁿ  ·  aᵐ/aⁿ = aᵐ⁻ⁿ  ·  (aᵐ)ⁿ = aᵐ·ⁿ  ·  a⁰ = 1  ·  a⁻ⁿ = 1/aⁿ",
    ]),
    "alan": ("📏 Alan, Çevre ve Hacim", [
        "Kare: A = a² · Ç = 4a  ·  Dikdörtgen: A = a·b · Ç = 2(a+b)",
        "Üçgen: A = (taban·yükseklik)/2  ·  Eşkenar üçgen: A = a²√3/4",
        "Paralelkenar: A = taban·yükseklik  ·  Yamuk: A = (a+c)·h/2",
        "Eşkenar dörtgen: A = (e·f)/2",
        "Daire: A = πr² · Çevre = 2πr  ·  Daire dilimi: A = πr²·α/360",
        "Küp: V = a³  ·  Dikdörtgenler prizması: V = a·b·c",
        "Silindir: V = πr²h  ·  Koni: V = πr²h/3  ·  Küre: V = 4πr³/3, A = 4πr²",
        "Piramit: V = (taban alanı·h)/3",
        "Pisagor: a² + b² = c²",
    ]),
    "fizik": ("⚛️ Temel Fizik Formülleri", [
        "Hız: v = Δx/Δt  ·  İvme: a = Δv/Δt",
        "Düzgün hızlanan hareket: v = v₀ + a·t  ·  x = v₀·t + ½·a·t²  ·  v² = v₀² + 2·a·x",
        "Newton 2: F = m·a  ·  Ağırlık: G = m·g (g ≈ 9,8 m/s²; sorularda genelde 10)",
        "Sürtünme: f = k·N",
        "İş: W = F·x  ·  Güç: P = W/t",
        "Kinetik enerji: Eₖ = ½·m·v²  ·  Potansiyel enerji: Eₚ = m·g·h",
        "Momentum: p = m·v  ·  İtme: F·Δt = Δp",
        "Basınç: P = F/A  ·  Sıvı basıncı: P = h·d·g  ·  Kaldırma kuvveti: F = V·d·g",
        "Ohm: V = I·R  ·  Elektriksel güç: P = V·I = I²·R",
        "Seri direnç: R = R₁ + R₂  ·  Paralel: 1/R = 1/R₁ + 1/R₂",
        "Dalga: v = λ·f  ·  Isı: Q = m·c·ΔT",
    ]),
    "kimya": ("⚗️ Temel Kimya Formülleri", [
        "Mol: n = m / M  (kütle / mol kütlesi)",
        "Tanecik sayısı: N = n·Nₐ  (Nₐ ≈ 6,02·10²³)",
        "Gazlar (NŞA, 0 °C 1 atm): 1 mol gaz = 22,4 L",
        "İdeal gaz: P·V = n·R·T  (R = 0,082 L·atm/mol·K)",
        "Molarite: M = n / V(L)  ·  Seyreltme: M₁·V₁ = M₂·V₂",
        "Kütlece yüzde: (çözünen kütlesi / çözelti kütlesi)·100",
        "pH = −log[H⁺]  ·  pH + pOH = 14 (25 °C)",
        "Özkütle: d = m / V",
    ]),
}
_FORMUL_ESANLAM = {"türev": "türev", "turev": "türev", "integral": "integral", "trigonometri": "trigonometri",
                   "trigo": "trigonometri", "sin cos": "trigonometri", "logaritma": "logaritma", "log": "logaritma",
                   "üslü": "logaritma", "alan": "alan", "hacim": "alan", "çevre": "alan", "geometri": "alan",
                   "fizik": "fizik", "kimya": "kimya", "mol": "kimya"}


def _formuller(t: str):
    if not re.search(r"formüller|formuller|formül\s*(?:kartı|kartları|özeti|ozeti|kağıdı|listesi)", t):
        return None
    anahtar = next((v for k, v in _FORMUL_ESANLAM.items() if re.search(r"\b" + k, t)), None)
    if not anahtar:
        satirlar = ["📐 **Formül Kartları** — hangisini açayım?", ""]
        for k, (ad, liste) in FORMULLER.items():
            satirlar.append(f"- {ad} ({len(liste)} madde) · *\"{k} formülleri\"*")
        return "\n".join(satirlar), "📐 Formül Kartı"
    ad, liste = FORMULLER[anahtar]
    satirlar = [f"**{ad}**", ""] + [f"- {f}" for f in liste]
    satirlar.append("\n💡 Bir formülü örnekle anlamak için sor: *\"zincir kuralını örnekle anlat\"*")
    return "\n".join(satirlar), "📐 Formül Kartı"


# ==============================================================================
# PANELİM — tüm öğrenci verilerinin tek bakışta özeti
# ==============================================================================
def _panel(t: str):
    if not re.search(r"^(?:benim\s*)?(?:panelim|panel|durumum|özetim|ozetim|bugünkü\s*özetim|genel\s*durumum)\W*$"
                     r"|^(?:bugün\w*\s*)?(?:öğrenci|çalışma)\s*panel", t):
        return None
    bugun = m18._simdi().date()
    simdi = m18._simdi()
    s = [f"🎯 **Panelin** — {bugun.day} {m18._AYLAR[bugun.month - 1]} {_GUNLER[bugun.weekday()]}", ""]
    oneriler = []

    # Sınav
    sinavlar = sorted((x for x in m18._oku(m21.SINAV_DOSYASI, []) if date.fromisoformat(x["tarih"]) >= bugun),
                      key=lambda x: x["tarih"])
    if sinavlar:
        x = sinavlar[0]
        s.append(f"📅 **{x['ad']}**: {m21._kalan_yazi(date.fromisoformat(x['tarih']))}"
                 + (f" · +{len(sinavlar) - 1} sınav daha" if len(sinavlar) > 1 else ""))
    else:
        oneriler.append("sınav tarihini kaydet: *\"YKS sınavım 20.06.2027\"*")

    # Bugün çalışma + hedef + seri
    gunler, _, kayitlar = m18._gunluk_toplamlar()
    b = gunler.get(bugun, {"soru": 0, "dk": 0})
    hedef = int(m18._oku(m18.AYAR_DOSYASI, {}).get("gunluk_soru_hedefi", 0) or 0)
    satir = f"📊 Bugün: **{b['soru']} soru · {b['dk']} dk**"
    if hedef:
        oran = min(100, round(b["soru"] / hedef * 100))
        satir += f" · hedef `{'█' * round(oran / 10)}{'░' * (10 - round(oran / 10))}` %{oran}"
    seri = m18._seri_hesapla(kayitlar)
    if seri >= 2:
        satir += f" · 🔥 {seri} gün seri"
    s.append(satir)
    hafta = sum(v["soru"] for v in gunler.values())
    if hafta:
        s.append(f"🗓️ Son 7 gün: **{hafta} soru · {sum(v['dk'] for v in gunler.values())} dk**")

    # Program
    plan = m18._oku(m18.AYAR_DOSYASI, {}).get("haftalik_plan")
    sira_ders = None
    if plan:
        gun = plan["gunler"][bugun.weekday()]
        s.append("📚 Bugünkü program: " + (" → ".join(gun) if gun else "dinlenme 🛋️"))
        sira_ders = next((d for d in gun if not d.startswith("📝")), None)
    else:
        oneriler.append("kendine program çıkar: *\"haftalık çalışma programı hazırla\"*")

    # Pomodoro
    pom = m18._oku(m18.AYAR_DOSYASI, {}).get("pomodoro", {}).get(bugun.isoformat(), 0)
    if pom:
        s.append(f"🍅 Bugün **{pom}** pomodoro")

    # Deneme
    denemeler = m18._oku(m21.DENEME_DOSYASI, [])
    if denemeler:
        son = denemeler[-1]
        onceki = next((d for d in reversed(denemeler[:-1]) if m21._ayni_tur(d, son["sinav"], son.get("dersler", {}))), None)
        fark = f" ({'+' if son['net'] >= onceki['net'] else ''}{m21._sayi(son['net'] - onceki['net'])})" if onceki else ""
        s.append(f"📈 Son {son['sinav']} denemen: **{m21._sayi(son['net'])} net**{fark}")

    # Yanlış defteri + kartlar
    defter = m18._oku(m18.YANLIS_DOSYASI, [])
    sorulabilir = sum(1 for k in defter if k.get("cevap"))
    if defter:
        s.append(f"📒 Yanlış defteri: **{len(defter)}** kayıt" + (f" ({sorulabilir} tekrar edilebilir)" if sorulabilir else ""))
    kartlar = m18._oku(m21.KART_DOSYASI, [])
    vadeli = sum(1 for k in kartlar if k["sonraki"] <= bugun.isoformat())
    if kartlar:
        s.append(f"🃏 Kartlar: bugün **{vadeli}** tekrar · toplam {len(kartlar)}")

    # Sıradaki hatırlatıcı
    hat = sorted((h for h in m18._oku(m18.HATIRLATICI_DOSYASI, []) if not h.get("silindi")
                  and datetime.fromisoformat(h["zaman"]) >= simdi), key=lambda h: h["zaman"])
    if hat:
        z = datetime.fromisoformat(hat[0]["zaman"])
        ne_zaman = f"{z:%H:%M}" if z.date() == bugun else f"{z.day} {m18._AYLAR[z.month - 1]} {z:%H:%M}"
        s.append(f"⏰ Sıradaki: {hat[0]['baslik']} — {ne_zaman}")

    # Sıradaki adım (öncelik sırasıyla tek net öneri)
    if vadeli:
        adim = f"🃏 Önce **{min(vadeli, 10)} kartını** tekrar et → *\"kartları çalış\"*"
    elif sorulabilir:
        adim = "📒 Yanlışlarını kapat → *\"yanlışlarımı tekrar et\"*"
    elif hedef and b["soru"] < hedef:
        adim = f"🎯 Hedefe **{hedef - b['soru']} soru** kaldı" + (f" — {sira_ders} ile başla" if sira_ders else "")
    elif sira_ders and b["dk"] == 0:
        adim = f"📚 Programına göre **{sira_ders}** ile başla → *\"pomodoro 40 dakika\"*"
    elif b["soru"] or b["dk"]:
        adim = "🌟 Bugün iyi iş çıkardın; kısa bir mini test ile kapat → *\"bana 5 matematik sorusu sor\"*"
    else:
        adim = "🚀 Güne kısa bir başlangıç yap → *\"pomodoro başlat\"*"
    s += ["", f"➡️ **Sıradaki adım:** {adim}"]
    if oneriler:
        s += ["", "💡 Paneli doldurmak için: " + " · ".join(oneriler[:2])]
    return "\n".join(x if not x or x.startswith(("➡️", "💡", "🎯 **")) else f"- {x}" for x in s), "🎯 Panelim"


def plan_ve_formul_yanitla(metin: str):
    if not metin or len(metin) > 300:
        return None, None
    t = _kucult(metin)
    if re.search(r"(?:çalışma|calisma|ders)?\s*program\w*\s*(?:hazırla|hazirla|yap|oluştur|olustur|çıkar|cikar|güncelle)"
                 r"|program\w*\s*(?:ister|lazım)|haftalık\s*(?:çalışma\s*)?plan", t) and not re.search(r"bilgisayar|python|yazılım|kod", t):
        try:
            return _program_olustur(t)
        except Exception:
            return None, None
    for fonk in (_panel, _bugun_ne_calisayim, _formuller):
        try:
            sonuc = fonk(t)
        except Exception:
            sonuc = None
        if sonuc:
            return sonuc
    return None, None
