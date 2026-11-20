# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 16: GÜNCEL KAYNAKLAR & AKILLI GÜNLÜK ASİSTAN
(modul_16_guncel_asistan.py)
==============================================================================
Canlı ve ücretsiz (API anahtarsız) yeni kaynaklar:
  • 🌍 Kandilli Rasathanesi son depremler (şehre göre süzme)  — api.orhanaydogdu.com.tr
  • 📜 Bugün Tarihte (Türkçe Vikipedi seçkisi)                  — api.wikimedia.org
  • 🎉 Resmî tatiller & bayramlar, "bayrama kaç gün kaldı"      — date.nager.at
  • 📖 İngilizce sözlük (anlam, okunuş, örnek cümle)            — dictionaryapi.dev

İnternetsiz çalışan akıllı araçlar:
  • 🕰️ Dünya saati ("Tokyo'da saat kaç", "New York ile saat farkı")
  • 📏 Birim çevirici (uzunluk, ağırlık, sıcaklık, hacim, hız, alan, veri, süre)
  • 📅 Tarih hesaplayıcı ("1 Ocak 2027 hangi gün", "yılbaşına kaç gün kaldı",
       "100 gün sonra", "12.05.2010 doğumluyum kaç yaşındayım", iki tarih arası)

Tek giriş noktası: guncel_asistan_yanitla(metin) -> (yanit, etiket) | (None, None)
"""

import json
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None

__all__ = ["guncel_asistan_yanitla"]

_TR_TZ = "Europe/Istanbul"
_ONBELLEK = {}


def _simdi():
    return datetime.now(ZoneInfo(_TR_TZ)) if ZoneInfo else datetime.now()


def _kucult(metin: str) -> str:
    return metin.replace("İ", "i").replace("I", "ı").lower().replace("̇", "").strip()


def _json_cek(url: str, ttl: float = 300.0, timeout: float = 6.0):
    simdi = time.time()
    if url in _ONBELLEK and simdi - _ONBELLEK[url][0] < ttl:
        return _ONBELLEK[url][1]
    ua = "AREX-AI-Studio/14 (egitim amacli asistan)"
    istek = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as yanit:
            ham = yanit.read()
    except urllib.error.URLError as hata:
        # Eski SSL kütüphaneli Python'larda (ör. macOS LibreSSL 2.8) TLS 1.3 isteyen sunuculara
        # bağlanılamaz → sistemdeki curl ile güvenli yedek bağlantı.
        if "SSL" not in str(hata) and "TLS" not in str(hata):
            raise
        ham = subprocess.run(["curl", "-sfL", "--max-time", str(int(timeout)), "-A", ua, url],
                             capture_output=True, check=True, timeout=timeout + 2).stdout
    veri = json.loads(ham.decode("utf-8"))
    _ONBELLEK[url] = (simdi, veri)
    return veri


_GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
_AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
_AY_NO = {a.lower(): i + 1 for i, a in enumerate(_AYLAR)}
_AY_NO.update({"subat": 2, "agustos": 8, "eylul": 9, "kasim": 11, "aralik": 12, "mayis": 5})


def _tarih_yaz(t: date) -> str:
    return f"{t.day} {_AYLAR[t.month - 1]} {t.year} {_GUNLER[t.weekday()]}"


def _sayi_yaz(x: float, basamak: int = 4) -> str:
    if abs(x - round(x)) < 1e-9 and abs(x) < 1e15:
        return f"{int(round(x)):,}".replace(",", ".")
    s = f"{x:,.{basamak}f}".rstrip("0").rstrip(".")
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


# ==============================================================================
# 1. KANDİLLİ SON DEPREMLER
# ==============================================================================
def _deprem(t: str):
    if not re.search(r"\bdeprem|\bzelzele|sars[ıi]nt[ıi]|kandilli", t):
        return None
    if re.search(r"deprem(?:de|e)\s+ne\s+yap|çantas|hazırl|nedir|nasıl\s+olu", t):
        return None  # bilgi/hazırlık sorusu → diğer motorlar
    limit = 100
    try:
        veri = _json_cek(f"https://api.orhanaydogdu.com.tr/deprem/kandilli/live?limit={limit}", ttl=90)
        liste = veri.get("result") or []
    except Exception:
        return None  # Modül 13'teki USGS yedeği devreye girsin
    if not liste:
        return None

    # Şehir süzgeci: "izmir'de deprem", "malatya depremleri"
    sehir = None
    for d in liste:
        for aday in {(d.get("location_properties", {}).get("closestCity") or {}).get("name", ""),
                     (d.get("location_properties", {}).get("epiCenter") or {}).get("name", "")}:
            if aday and _kucult(aday) in t:
                sehir = aday
                break
        if sehir:
            break
    if sehir is None:
        m = re.search(r"([a-zçğıöşü]{3,})(?:'?(?:da|de|ta|te|daki|deki))\s+(?:son\s+)?deprem", t)
        if m and m.group(1) not in ("bugün", "dün", "türkiye", "ülke", "son"):
            sehir = m.group(1).capitalize()

    def eslesir(d):
        if not sehir:
            return True
        lp = d.get("location_properties", {})
        adlar = [d.get("title", ""), (lp.get("closestCity") or {}).get("name", ""), (lp.get("epiCenter") or {}).get("name", "")]
        return any(_kucult(sehir) in _kucult(a) for a in adlar)

    min_buyukluk = 4.0 if re.search(r"büyük|ciddi|önemli|4\s*(?:ve|\+|üzeri)", t) else 0.0
    secilen = [d for d in liste if eslesir(d) and (d.get("mag") or 0) >= min_buyukluk][:8]
    baslik = f"🌍 **Son Depremler{' — ' + sehir if sehir else ''}** (Kandilli Rasathanesi, son 24 saat)"
    if not secilen:
        return (f"{baslik}\n\n✅ Son 24 saatte {'bu bölgede ' if sehir else ''}"
                f"{'M4+ ' if min_buyukluk else ''}deprem kaydı yok.", "🌍 Kandilli Deprem")
    en_buyuk = max(liste, key=lambda d: d.get("mag") or 0)
    satirlar = [baslik, "", "| Büyüklük | Yer | Derinlik | Saat |", "| :-- | :-- | :-- | :-- |"]
    for d in secilen:
        mag = d.get("mag") or 0
        simge = "🔴" if mag >= 5 else ("🟠" if mag >= 4 else ("🟡" if mag >= 3 else "🟢"))
        saat = (d.get("date_time") or "")[11:16]
        satirlar.append(f"| {simge} **M {mag:.1f}** | {d.get('title', '?').title()} | {d.get('depth', '?')} km | {saat} |")
    satirlar.append(f"\n📈 Son 24 saatin en büyüğü: **M {en_buyuk.get('mag', 0):.1f}** — {en_buyuk.get('title', '').title()}"
                    f" ({(en_buyuk.get('date_time') or '')[11:16]})")
    satirlar.append("\n🔗 Kaynak: Boğaziçi Üniversitesi Kandilli Rasathanesi (api.orhanaydogdu.com.tr üzerinden)")
    return "\n".join(satirlar), "🌍 Kandilli Deprem"


# ==============================================================================
# 2. BUGÜN TARİHTE
# ==============================================================================
def _bugun_tarihte(t: str):
    if not re.search(r"bugün\s*(?:ne\s*oldu|tarihte)|tarihte\s*bugün|tarihte\s*(?:ne\s*oldu\s*)?bugün|bugünün\s*tarih", t):
        return None
    an = _simdi()
    try:
        veri = _json_cek(f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/selected/{an.month:02d}/{an.day:02d}",
                         ttl=3600)
    except Exception:
        return None
    olaylar = sorted(veri.get("selected") or [], key=lambda o: o.get("year", 0), reverse=True)[:7]
    if not olaylar:
        return None
    satirlar = [f"📜 **Tarihte Bugün — {an.day} {_AYLAR[an.month - 1]}**", ""]
    for o in olaylar:
        satirlar.append(f"• **{o.get('year')}** — {o.get('text', '').strip()}")
    satirlar.append("\n🔗 Kaynak: Türkçe Vikipedi (Wikimedia API)")
    return "\n".join(satirlar), "📜 Bugün Tarihte"


# ==============================================================================
# 3. RESMÎ TATİLLER & BAYRAMLAR
# ==============================================================================
_TATIL_ANAHTAR = {
    "ramazan": "Ramazan Bayramı", "şeker": "Ramazan Bayramı", "kurban": "Kurban Bayramı",
    "yılbaşı": "Yılbaşı", "23 nisan": "Ulusal Egemenlik", "1 mayıs": "Emek", "19 mayıs": "Atatürk'ü Anma",
    "15 temmuz": "Demokrasi", "30 ağustos": "Zafer", "29 ekim": "Cumhuriyet",
}


def _tatiller(t: str):
    if not re.search(r"bayram|resm[iî]\s*tatil|tatil\s*günleri|tatiller|arife", t):
        return None
    if re.search(r"tatil\s*(?:yeri|önerisi|için|planı)|nereye", t):
        return None
    bugun = _simdi().date()
    liste = []
    for yil in (bugun.year, bugun.year + 1):
        try:
            liste += [dict(g) for g in _json_cek(f"https://date.nager.at/api/v3/PublicHolidays/{yil}/TR", ttl=86400)]
        except Exception:
            pass
    if not liste:
        return None
    for g in liste:
        g["_t"] = date.fromisoformat(g["date"])
        ad = re.sub(r"\s*\(Tentative Date\)", "", g.get("localName", ""))
        g["_tahmini"] = ad != g.get("localName", "")
        g["localName"] = re.sub(r"\s*\d+\.\s*Gün$", "", ad).strip()  # "Ramazan Bayramı 1. Gün" → tek ad
    gelecek = [g for g in liste if g["_t"] >= bugun]

    aranan = next((v for k, v in _TATIL_ANAHTAR.items() if k in t), None)
    if aranan:
        adaylar = [g for g in gelecek if aranan.lower() in g.get("localName", "").lower()]
        if adaylar:
            ilk = adaylar[0]
            ayni = [g for g in adaylar if 0 <= (g["_t"] - ilk["_t"]).days <= 4]
            kalan = (ilk["_t"] - bugun).days
            ne_zaman = "**bugün!** 🎉" if kalan == 0 else f"**{kalan} gün** kaldı"
            arife = ilk["_t"] - timedelta(days=1)
            ek = f"\n• Arife: {_tarih_yaz(arife)}" if ilk["localName"] in ("Ramazan Bayramı", "Kurban Bayramı") else ""
            if ilk.get("_tahmini"):
                ek += "\n• ℹ️ Dini bayram tarihleri ay takvimine göre hesaplanır; Diyanet ilanıyla 1 gün kayabilir."
            bitis = f" → {_tarih_yaz(ayni[-1]['_t'])} ({len(ayni)} gün)" if len(ayni) > 1 else ""
            return (f"🎉 **{ilk['localName']}**\n• Başlangıç: **{_tarih_yaz(ilk['_t'])}**{bitis}"
                    f"{ek}\n• {ne_zaman}\n\n🔗 Kaynak: Nager.Date resmî tatil API"), "🎉 Resmî Tatil"

    satirlar = ["🎉 **Yaklaşan Resmî Tatiller ve Bayramlar**", ""]
    goruldu = set()
    for g in gelecek:
        anahtar = (g["localName"], g["_t"].year)
        if anahtar in goruldu:
            continue
        goruldu.add(anahtar)
        kalan = (g["_t"] - bugun).days
        gun_say = sum(1 for x in gelecek if x["localName"] == g["localName"] and 0 <= (x["_t"] - g["_t"]).days <= 4)
        sure = f" · {gun_say} gün" if gun_say > 1 else ""
        satirlar.append(f"• **{g['localName']}** — {_tarih_yaz(g['_t'])}{sure} "
                        f"({'bugün' if kalan == 0 else f'{kalan} gün sonra'})")
        if len(goruldu) >= 8:
            break
    satirlar.append("\n🔗 Kaynak: Nager.Date resmî tatil API")
    return "\n".join(satirlar), "🎉 Resmî Tatil"


# ==============================================================================
# 4. İNGİLİZCE SÖZLÜK
# ==============================================================================
def _ingilizce_sozluk(t: str):
    m = (re.search(r"(?:ingilizce(?:de)?|english)\s+['\"]?([a-z][a-z\-]{1,30})['\"]?\s*(?:ne\s*demek|anlam|nedir|kelimesinin)", t)
         or re.search(r"['\"]?([a-z][a-z\-]{1,30})['\"]?\s+(?:ingilizce|kelimesi)\s*(?:ne\s*demek|anlam)", t)
         or re.search(r"^(?:define|meaning of)\s+([a-z][a-z\-]{1,30})\??$", t))
    if not m:
        return None
    kelime = m.group(1)
    try:
        veri = _json_cek(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(kelime)}", ttl=86400)
    except urllib.error.HTTPError as hata:
        if hata.code == 404:
            return (f"📖 **{kelime}** kelimesi İngilizce sözlükte bulunamadı. Yazımını kontrol eder misin?", "📖 İngilizce Sözlük")
        return None
    except subprocess.CalledProcessError as hata:
        if hata.returncode == 22:  # curl -f: HTTP 4xx
            return (f"📖 **{kelime}** kelimesi İngilizce sözlükte bulunamadı. Yazımını kontrol eder misin?", "📖 İngilizce Sözlük")
        return None
    except Exception:
        return None  # ağ hatası → diğer motorlar (çeviri / AI) denesin
    if not isinstance(veri, list) or not veri:
        return None
    k = veri[0]
    okunus = k.get("phonetic") or next((p.get("text") for p in k.get("phonetics", []) if p.get("text")), "")
    satirlar = [f"📖 **{k.get('word', kelime)}** {f'`{okunus}`' if okunus else ''}", ""]
    tur_tr = {"noun": "isim", "verb": "fiil", "adjective": "sıfat", "adverb": "zarf", "pronoun": "zamir",
              "preposition": "edat", "conjunction": "bağlaç", "interjection": "ünlem"}
    for anlam in k.get("meanings", [])[:3]:
        tur = anlam.get("partOfSpeech", "")
        satirlar.append(f"**{tur_tr.get(tur, tur)}** ({tur})")
        for tanim in anlam.get("definitions", [])[:2]:
            satirlar.append(f"• {tanim.get('definition', '')}")
            if tanim.get("example"):
                satirlar.append(f"  _Örnek: {tanim['example']}_")
        es = anlam.get("synonyms", [])[:5]
        if es:
            satirlar.append(f"  Eş anlamlılar: {', '.join(es)}")
    satirlar.append("\n💡 Türkçe karşılığı için: `ingilizceden çevir: " + kelime + "`")
    satirlar.append("🔗 Kaynak: Free Dictionary API (Wiktionary)")
    return "\n".join(satirlar), "📖 İngilizce Sözlük"


# ==============================================================================
# 5. DÜNYA SAATİ (internetsiz)
# ==============================================================================
_SAAT_DILIMLERI = {
    "tokyo": "Asia/Tokyo", "japonya": "Asia/Tokyo", "seul": "Asia/Seoul", "kore": "Asia/Seoul",
    "pekin": "Asia/Shanghai", "çin": "Asia/Shanghai", "şanghay": "Asia/Shanghai", "hong kong": "Asia/Hong_Kong",
    "dubai": "Asia/Dubai", "birleşik arap": "Asia/Dubai", "mekke": "Asia/Riyadh", "medine": "Asia/Riyadh",
    "suudi": "Asia/Riyadh", "riyad": "Asia/Riyadh", "katar": "Asia/Qatar", "doha": "Asia/Qatar", "bakü": "Asia/Baku",
    "azerbaycan": "Asia/Baku", "tahran": "Asia/Tehran", "iran": "Asia/Tehran", "bağdat": "Asia/Baghdad",
    "kahire": "Africa/Cairo", "mısır": "Africa/Cairo", "delhi": "Asia/Kolkata", "hindistan": "Asia/Kolkata",
    "bangladeş": "Asia/Dhaka", "dakka": "Asia/Dhaka", "pakistan": "Asia/Karachi", "endonezya": "Asia/Jakarta",
    "cakarta": "Asia/Jakarta", "singapur": "Asia/Singapore", "malezya": "Asia/Kuala_Lumpur",
    "londra": "Europe/London", "ingiltere": "Europe/London", "paris": "Europe/Paris", "fransa": "Europe/Paris",
    "berlin": "Europe/Berlin", "almanya": "Europe/Berlin", "amsterdam": "Europe/Amsterdam", "hollanda": "Europe/Amsterdam",
    "roma": "Europe/Rome", "italya": "Europe/Rome", "madrid": "Europe/Madrid", "ispanya": "Europe/Madrid",
    "moskova": "Europe/Moscow", "rusya": "Europe/Moscow", "atina": "Europe/Athens", "yunanistan": "Europe/Athens",
    "viyana": "Europe/Vienna", "avusturya": "Europe/Vienna", "kiev": "Europe/Kyiv", "ukrayna": "Europe/Kyiv",
    "new york": "America/New_York", "washington": "America/New_York", "amerika": "America/New_York",
    "abd": "America/New_York", "los angeles": "America/Los_Angeles", "kaliforniya": "America/Los_Angeles",
    "chicago": "America/Chicago", "toronto": "America/Toronto", "kanada": "America/Toronto",
    "meksika": "America/Mexico_City", "brezilya": "America/Sao_Paulo", "sao paulo": "America/Sao_Paulo",
    "arjantin": "America/Argentina/Buenos_Aires", "sidney": "Australia/Sydney", "avustralya": "Australia/Sydney",
    "yeni zelanda": "Pacific/Auckland", "kazakistan": "Asia/Almaty", "özbekistan": "Asia/Tashkent",
    "taşkent": "Asia/Tashkent", "kırgızistan": "Asia/Bishkek", "türkmenistan": "Asia/Ashgabat",
}


def _dunya_saati(t: str):
    if ZoneInfo is None or not re.search(r"saat\s*(?:kaç|kac|farkı|farki)|saati\s*(?:kaç|ne)|yerel\s*saat", t):
        return None
    bulunan = [(ad, tz) for ad, tz in _SAAT_DILIMLERI.items() if re.search(r"\b" + re.escape(ad), t)]
    if not bulunan:
        return None
    burasi = datetime.now(ZoneInfo(_TR_TZ))
    satirlar = ["🕰️ **Dünya Saati**", ""]
    goruldu = set()
    for ad, tz in bulunan[:4]:
        if tz in goruldu:
            continue
        goruldu.add(tz)
        orasi = burasi.astimezone(ZoneInfo(tz))
        fark = (orasi.utcoffset() - burasi.utcoffset()).total_seconds() / 3600
        fark_yazi = "Türkiye ile aynı" if fark == 0 else f"Türkiye'den {_sayi_yaz(abs(fark))} saat {'ileri' if fark > 0 else 'geri'}"
        gun_notu = ""
        if orasi.date() != burasi.date():
            gun_notu = " (yarın)" if orasi.date() > burasi.date() else " (dün)"
        satirlar.append(f"• **{ad.title()}**: `{orasi.strftime('%H:%M')}`{gun_notu} — {fark_yazi}")
    satirlar.append(f"\n🇹🇷 Türkiye: `{burasi.strftime('%H:%M')}`")
    return "\n".join(satirlar), "🕰️ Dünya Saati"


# ==============================================================================
# 6. BİRİM ÇEVİRİCİ (internetsiz)
# ==============================================================================
_BIRIMLER = {  # ad: (kategori, temel birime çarpan)
    # uzunluk (metre)
    "mm": ("uzunluk", 0.001), "milimetre": ("uzunluk", 0.001), "cm": ("uzunluk", 0.01), "santimetre": ("uzunluk", 0.01),
    "m": ("uzunluk", 1), "metre": ("uzunluk", 1), "km": ("uzunluk", 1000), "kilometre": ("uzunluk", 1000),
    "inç": ("uzunluk", 0.0254), "inch": ("uzunluk", 0.0254), "inc": ("uzunluk", 0.0254),
    "ayak": ("uzunluk", 0.3048), "feet": ("uzunluk", 0.3048), "ft": ("uzunluk", 0.3048),
    "yarda": ("uzunluk", 0.9144), "mil": ("uzunluk", 1609.344), "deniz mili": ("uzunluk", 1852),
    # kütle (kg)
    "mg": ("kütle", 1e-6), "miligram": ("kütle", 1e-6), "g": ("kütle", 0.001), "gram": ("kütle", 0.001),
    "kg": ("kütle", 1), "kilogram": ("kütle", 1), "kilo": ("kütle", 1), "ton": ("kütle", 1000),
    "pound": ("kütle", 0.45359237), "libre": ("kütle", 0.45359237), "lb": ("kütle", 0.45359237),
    "ons": ("kütle", 0.028349523), "oz": ("kütle", 0.028349523),
    # hacim (litre)
    "ml": ("hacim", 0.001), "mililitre": ("hacim", 0.001), "litre": ("hacim", 1), "lt": ("hacim", 1), "l": ("hacim", 1),
    "galon": ("hacim", 3.785411784), "m3": ("hacim", 1000), "metreküp": ("hacim", 1000),
    "su bardağı": ("hacim", 0.2), "çay bardağı": ("hacim", 0.1), "yemek kaşığı": ("hacim", 0.015),
    "tatlı kaşığı": ("hacim", 0.01), "çay kaşığı": ("hacim", 0.005),
    # hız (m/s)
    "km/s": ("hız", 1 / 3.6), "km/sa": ("hız", 1 / 3.6), "kmh": ("hız", 1 / 3.6), "m/s": ("hız", 1),
    "mph": ("hız", 0.44704), "knot": ("hız", 0.514444), "deniz mili/saat": ("hız", 0.514444),
    # alan (m²)
    "m2": ("alan", 1), "metrekare": ("alan", 1), "km2": ("alan", 1e6), "kilometrekare": ("alan", 1e6),
    "dönüm": ("alan", 1000), "dekar": ("alan", 1000), "hektar": ("alan", 10000), "akre": ("alan", 4046.8564224),
    # veri (bayt)
    "bayt": ("veri", 1), "byte": ("veri", 1), "kb": ("veri", 1024), "mb": ("veri", 1024 ** 2),
    "gb": ("veri", 1024 ** 3), "tb": ("veri", 1024 ** 4),
    # süre (saniye)
    "saniye": ("süre", 1), "sn": ("süre", 1), "dakika": ("süre", 60), "dk": ("süre", 60), "saat": ("süre", 3600),
    "gün": ("süre", 86400), "hafta": ("süre", 604800), "yıl": ("süre", 31557600),
    # sıcaklık (özel)
    "celsius": ("sıcaklık", None), "santigrat": ("sıcaklık", None), "°c": ("sıcaklık", None), "c": ("sıcaklık", None),
    "fahrenheit": ("sıcaklık", None), "°f": ("sıcaklık", None), "f": ("sıcaklık", None),
    "kelvin": ("sıcaklık", None), "k": ("sıcaklık", None),
}
_BIRIM_DESEN = "|".join(sorted((re.escape(b) for b in _BIRIMLER), key=len, reverse=True))


def _sicaklik_c(deger, birim):
    b = birim.replace("°", "")
    if b in ("c", "celsius", "santigrat"):
        return deger
    if b in ("f", "fahrenheit"):
        return (deger - 32) * 5 / 9
    return deger - 273.15


def _sicaklik_den(c, birim):
    b = birim.replace("°", "")
    if b in ("c", "celsius", "santigrat"):
        return c
    if b in ("f", "fahrenheit"):
        return c * 9 / 5 + 32
    return c + 273.15


def _birim_cevir(t: str):
    m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(" + _BIRIM_DESEN + r")\b\s*(?:'?\s*\w{0,4})?\s*(?:kaç|kac|=|->|→|to|ne\s*kadar)?\s*(" +
                  _BIRIM_DESEN + r")\b", t)
    if not m or not re.search(r"kaç|kac|çevir|cevir|=|->|→|\bto\b|ne\s*kadar|eder", t):
        return None
    deger = float(m.group(1).replace(",", "."))
    kaynak, hedef = m.group(2), m.group(3)
    k1, c1 = _BIRIMLER[kaynak]
    k2, c2 = _BIRIMLER[hedef]
    if k1 != k2 or kaynak == hedef:
        return None
    if k1 == "sıcaklık":
        sonuc = _sicaklik_den(_sicaklik_c(deger, kaynak), hedef)
        formul = {"cf": "°F = °C × 9/5 + 32", "fc": "°C = (°F − 32) × 5/9"}.get(
            kaynak.replace("°", "")[0] + hedef.replace("°", "")[0], "K = °C + 273,15")
    else:
        sonuc = deger * c1 / c2
        formul = f"1 {kaynak} = {_sayi_yaz(c1 / c2, 6)} {hedef}"
    return (f"📏 **Birim Çevirme ({k1}):** `{_sayi_yaz(deger)} {kaynak}` = **`{_sayi_yaz(sonuc)} {hedef}`**\n"
            f"• Formül: `{formul}`"), "📏 Birim Çevirici"


# ==============================================================================
# 7. TARİH HESAPLAYICI (internetsiz)
# ==============================================================================
_TARIH_DESENI = (r"(\d{1,2})\s*[./\- ]\s*(\d{1,2}|" + "|".join(sorted(_AY_NO, key=len, reverse=True)) +
                 r")\s*[./\- ]\s*(\d{4})")


def _tarih_coz(eslesme) -> date:
    gun, ay, yil = eslesme.group(1), eslesme.group(2), eslesme.group(3)
    ay_no = int(ay) if ay.isdigit() else _AY_NO[ay]
    return date(int(yil), ay_no, int(gun))


_OZEL_GUNLER = {
    "yılbaşı": (1, 1), "yeni yıl": (1, 1), "23 nisan": (4, 23), "19 mayıs": (5, 19), "29 ekim": (10, 29),
    "cumhuriyet bayramı": (10, 29), "30 ağustos": (8, 30), "sevgililer günü": (2, 14), "anneler günü": None,
    "10 kasım": (11, 10), "yaz tatili": None,
}


def _tarih_hesapla(t: str):
    bugun = _simdi().date()
    tarihler = []
    for m in re.finditer(_TARIH_DESENI, t):
        try:
            tarihler.append(_tarih_coz(m))
        except ValueError:
            return "📅 Bu tarih geçerli değil (ör. 31 Şubat yok). Kontrol eder misin?", "📅 Tarih Hesaplayıcı"

    # Yaş hesabı
    if tarihler and re.search(r"doğum|dogum|doğdum|yaşında|kaç\s*yaş", t):
        d = tarihler[0]
        if d > bugun:
            return "📅 Doğum tarihi gelecekte olamaz 🙂", "📅 Yaş Hesabı"
        yas = bugun.year - d.year - ((bugun.month, bugun.day) < (d.month, d.day))
        gun_ay = (d.month, 28 if (d.month, d.day) == (2, 29) else d.day)  # 29 Şubat → 28 Şubat
        sonraki = date(bugun.year, *gun_ay)
        if sonraki < bugun:
            sonraki = date(bugun.year + 1, *gun_ay)
        if sonraki == bugun:
            dogum_gunu = "🎂 **Bugün doğum günün! İyi ki doğdun!** 🎉"
        else:
            dogum_gunu = f"🎂 Bir sonraki doğum gününe **{(sonraki - bugun).days} gün** kaldı."
        return (f"📅 **Yaş Hesabı:** {_tarih_yaz(d)} doğumlu\n• Yaş: **{yas}**\n"
                f"• Yaşanan gün: **{_sayi_yaz((bugun - d).days)}**\n• {dogum_gunu}\n"
                f"• Doğduğun gün bir **{_GUNLER[d.weekday()]}** idi."), "📅 Yaş Hesabı"

    # İki tarih arası
    if len(tarihler) >= 2 and re.search(r"arası|arasi|kaç\s*gün|fark", t):
        a, b = sorted(tarihler[:2])
        gun = (b - a).days
        return (f"📅 **İki Tarih Arası:** {_tarih_yaz(a)} → {_tarih_yaz(b)}\n"
                f"• **{_sayi_yaz(gun)} gün** (≈ {gun // 7} hafta {gun % 7} gün)"), "📅 Tarih Hesaplayıcı"

    # Hangi gün?
    if tarihler and re.search(r"hangi\s*gün|ne\s*gün|günlerden\s*ne", t):
        d = tarihler[0]
        fark = (d - bugun).days
        zaman = "bugün" if fark == 0 else (f"{_sayi_yaz(fark)} gün sonra" if fark > 0 else f"{_sayi_yaz(-fark)} gün önce")
        return f"📅 **{d.day} {_AYLAR[d.month - 1]} {d.year}** bir **{_GUNLER[d.weekday()]}** günü ({zaman}).", "📅 Tarih Hesaplayıcı"

    # Bir tarihe/özel güne kaç gün kaldı
    if re.search(r"kaç\s*gün\s*(?:kaldı|var)|ne\s*zaman", t):
        hedef, ad = None, None
        if tarihler:
            hedef, ad = tarihler[0], _tarih_yaz(tarihler[0])
        else:
            for anahtar, ay_gun in _OZEL_GUNLER.items():
                if anahtar in t and ay_gun:
                    hedef = date(bugun.year, *ay_gun)
                    if hedef < bugun:
                        hedef = date(bugun.year + 1, *ay_gun)
                    ad = anahtar.title()
                    break
            if hedef is None:
                m = re.search(r"(\d{1,2})\s+(" + "|".join(_AY_NO) + r")(?!\s*\d{4})", t)
                if m:
                    hedef = date(bugun.year, _AY_NO[m.group(2)], int(m.group(1)))
                    if hedef < bugun:
                        hedef = date(bugun.year + 1, hedef.month, hedef.day)
                    ad = f"{hedef.day} {_AYLAR[hedef.month - 1]}"
        if hedef:
            kalan = (hedef - bugun).days
            if kalan < 0:
                return f"📅 **{ad}** {_sayi_yaz(-kalan)} gün önceydi.", "📅 Geri Sayım"
            return (f"⏳ **{ad}**: {_tarih_yaz(hedef)}\n• " +
                    ("**Bugün!** 🎉" if kalan == 0 else f"**{_sayi_yaz(kalan)} gün** kaldı (≈ {kalan // 7} hafta {kalan % 7} gün)")
                    ), "📅 Geri Sayım"

    # N gün/hafta/ay sonra-önce
    m = re.search(r"(\d+)\s*(gün|hafta|ay|yıl)\s*(sonra|önce|once)", t)
    if m and re.search(r"hangi|ne\s*zaman|tarih|kaçı|günü", t):
        n, birim, yon = int(m.group(1)), m.group(2), m.group(3)
        if n > 100000:
            return None
        isaret = 1 if yon == "sonra" else -1
        if birim in ("gün", "hafta"):
            hedef = bugun + timedelta(days=isaret * n * (7 if birim == "hafta" else 1))
        else:
            aylar = n * (12 if birim == "yıl" else 1) * isaret
            yil, ay = divmod(bugun.month - 1 + aylar, 12)
            yil += bugun.year
            ay += 1
            gun = bugun.day
            while True:
                try:
                    hedef = date(yil, ay, gun)
                    break
                except ValueError:
                    gun -= 1
        return f"📅 Bugünden **{n} {birim} {yon}**: **{_tarih_yaz(hedef)}**", "📅 Tarih Hesaplayıcı"
    return None


def _md_satirlari_koru(metin: str) -> str:
    """Markdown'da tek satır sonları birleşir: '•' maddelerini gerçek listeye çevir,
    diğer satırlara zorunlu satır sonu ekle (tablo/başlık/boş satırlara dokunma)."""
    satirlar = []
    for satir in metin.split("\n"):
        if satir.startswith("• "):
            satir = "- " + satir[2:]
        elif satir.startswith("  _") or satir.startswith("  Eş"):
            satir = "  " + satir.strip()  # liste altı girintili satır
        if satir.strip() and not satir.lstrip().startswith(("|", "#", "- ")) and not satir.endswith("  "):
            satir += "  "
        satirlar.append(satir)
    return "\n".join(satirlar)


# ==============================================================================
# GİRİŞ NOKTASI
# ==============================================================================
_SIRA = [_birim_cevir, _tarih_hesapla, _dunya_saati, _ingilizce_sozluk, _bugun_tarihte, _tatiller, _deprem]


def guncel_asistan_yanitla(metin: str):
    """Metin bu modülün alanına giriyorsa (yanıt, etiket); değilse (None, None)."""
    if not metin or len(metin) > 250:
        return None, None
    t = _kucult(metin)
    for fonk in _SIRA:
        try:
            sonuc = fonk(t)
        except Exception:
            sonuc = None
        if sonuc:
            return _md_satirlari_koru(sonuc[0]), sonuc[1]
    return None, None
