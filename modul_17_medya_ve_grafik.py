# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 17: GRAFİK ÇİZİCİ, SESLİ SORU (WHISPER) VE FOTOĞRAFTAN SORU ÇÖZME
(modul_17_medya_ve_grafik.py)
==============================================================================
  • grafik_ciz(metin)          : "y = x^2 - 4 grafiğini çiz" → SVG grafik + kökler, tepe noktası,
                                 y-kesişimi (tamamen yerel; Modül 14 ayrıştırıcısını kullanır)
  • sesi_metne_cevir(bayt)     : Groq Whisper (whisper-large-v3-turbo) ile Türkçe konuşma tanıma
  • fotograftan_soru_coz(...)  : Google Gemini (ücretsiz anahtar) ile fotoğraftaki soruyu adım adım çözer

Grafik, sohbet geçmişine büyük veri gömmemek için yanıt metninde bir işaretçi olarak
taşınır; main.py bu işaretçiyi ayıklayıp mesajın "svg" alanına koyar.
"""

import base64
import io
import json
import math
import re
import urllib.error
import urllib.request
import uuid
from fractions import Fraction

import modul_14_pro_matematik as m14

__all__ = ["grafik_istegi_mi", "grafik_ciz", "svg_ayikla", "sesi_metne_cevir", "fotograftan_soru_coz"]

_SVG_ISARET = re.compile(r"<!--AREX_SVG:([A-Za-z0-9+/=]+)-->")


# ==============================================================================
# 1. GRAFİK ÇİZİCİ
# ==============================================================================
def grafik_istegi_mi(metin: str) -> bool:
    t = metin.lower()
    return bool(re.search(r"grafi[ğg]|çiz|ciz|plot|graph", t)) and bool(re.search(r"x", t))


def _ifade_ayikla(metin: str):
    t = metin.replace("İ", "i").replace("I", "ı").lower()
    # Aralık: "-5 ile 5 arasında", "[-5, 5]", "x -3'ten 3'e"
    aralik = None
    m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(?:ile|ila|'?(?:den|dan|ten|tan))\s*(-?\d+(?:[.,]\d+)?)\s*(?:'?\w*)?\s*(?:aras|'?(?:e|a|ye|ya)\b)", t) \
        or re.search(r"\[\s*(-?\d+(?:[.,]\d+)?)\s*[,;]\s*(-?\d+(?:[.,]\d+)?)\s*\]", t)
    if m:
        a, b = float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        if a < b and b - a <= 2000:
            aralik = (a, b)
        t = t[:m.start()] + " " + t[m.end():]
    # "y = ...", "f(x) = ..."
    m = re.search(r"(?:\by|f\s*\(\s*x\s*\))\s*=\s*(.+)", t)
    ifade = m.group(1) if m else t
    ifade = re.sub(r"(?:fonksiyonunun|fonksiyonu|denkleminin|in|ın|un|ün|nin|nın)?\s*grafi[ğg]\w*.*$", "", ifade)
    ifade = re.sub(r"\b(?:çiz\w*|ciz\w*|plot|graph|göster\w*|lütfen|bana|aralığında|arasında)\b", " ", ifade)
    ifade = re.sub(r"[?!.:]+$", "", ifade).strip().rstrip("'").strip()
    return ifade, aralik


def _derleyici(ifade: str):
    tokenlar = m14._tokenlara_ayir(m14._normalize(ifade, denklem=True))
    if ("deg", "x") not in tokenlar:
        raise m14.MatHata("İfadede x yok")

    def f(x):
        try:
            v = m14._Ayristirici(tokenlar, x).calistir()
            v = float(v)
            return v if math.isfinite(v) else None
        except (m14.MatHata, ZeroDivisionError, OverflowError, ValueError):
            return None
    return f, tokenlar


def _sayi(v: float, basamak: int = 3) -> str:
    return m14.sayi_yaz(float(round(v, basamak)))


def _kokleri_bul(f, a, b, adim=800):
    kokler, xs = [], [a + (b - a) * i / adim for i in range(adim + 1)]
    onceki_x, onceki_y = xs[0], f(xs[0])
    if onceki_y is not None and abs(onceki_y) < 1e-12:
        kokler.append(onceki_x)
    for x in xs[1:]:
        y = f(x)
        if y is not None and abs(y) < 1e-12:
            kokler.append(x)  # tam sıfır (tanım kümesinin ucundaki kökler dahil: √x → x=0)
        elif y is not None and onceki_y is not None:
            if onceki_y * y < 0 and abs(y - onceki_y) < 1e6:  # asimptot değil, gerçek işaret değişimi
                lo, hi = onceki_x, x
                for _ in range(60):
                    orta = (lo + hi) / 2
                    fo = f(orta)
                    if fo is None:
                        break
                    if (f(lo) or 0) * fo <= 0:
                        hi = orta
                    else:
                        lo = orta
                kokler.append((lo + hi) / 2)
        onceki_x, onceki_y = x, y
    tekil = []
    for k in kokler:
        if not tekil or abs(k - tekil[-1]) > (b - a) / 400:
            tekil.append(k)
    return tekil[:8]


def _svg_olustur(f, a, b, isaretler, baslik):
    G, Y, kenar = 640, 420, 44
    n = 600
    noktalar = [(a + (b - a) * i / n, None) for i in range(n + 1)]
    noktalar = [(x, f(x)) for x, _ in noktalar]
    ys = sorted(y for _, y in noktalar if y is not None)
    if not ys:
        return None
    # Asimptotları kırpmak için %3-%97 yüzdelik aralık
    alt, ust = ys[int(len(ys) * 0.03)], ys[min(len(ys) - 1, int(len(ys) * 0.97))]
    for _, y in isaretler:
        alt, ust = min(alt, y), max(ust, y)
    if ust - alt < 1e-9:
        alt, ust = alt - 1, ust + 1
    pay = (ust - alt) * 0.12
    alt, ust = alt - pay, ust + pay
    if alt > 0 and alt < (ust - alt) * 0.6:
        alt = -(ust - alt) * 0.05  # x eksenini görünür tut
    if ust < 0 and -ust < (ust - alt) * 0.6:
        ust = (ust - alt) * 0.05

    def px(x):
        return kenar + (x - a) / (b - a) * (G - 2 * kenar)

    def py(y):
        return Y - kenar - (y - alt) / (ust - alt) * (Y - 2 * kenar)

    def guzel_adim(aralik):
        ham = aralik / 8
        us = 10 ** math.floor(math.log10(ham))
        for c in (1, 2, 2.5, 5, 10):
            if ham <= c * us:
                return c * us
        return 10 * us

    parcalar = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {G} {Y}" '
                f'style="width:100%;max-width:640px;height:auto;display:block;margin:6px 0;'
                f'background:rgba(15,23,42,.55);border-radius:14px;border:1px solid rgba(148,163,184,.25)" '
                f'font-family="Inter,system-ui,sans-serif" role="img" aria-label="{baslik}">']
    # Izgara + etiketler
    for eksen, (bas, son, cevir, dikey) in {"x": (a, b, px, True), "y": (alt, ust, py, False)}.items():
        adim = guzel_adim(son - bas)
        v = math.ceil(bas / adim) * adim
        while v <= son + 1e-9:
            p = cevir(v)
            etiket = _sayi(v)
            if dikey:
                parcalar.append(f'<line x1="{p:.1f}" y1="{kenar}" x2="{p:.1f}" y2="{Y - kenar}" stroke="rgba(148,163,184,.14)"/>')
                parcalar.append(f'<text x="{p:.1f}" y="{Y - kenar + 16}" fill="#94a3b8" font-size="11" text-anchor="middle">{etiket}</text>')
            else:
                parcalar.append(f'<line x1="{kenar}" y1="{p:.1f}" x2="{G - kenar}" y2="{p:.1f}" stroke="rgba(148,163,184,.14)"/>')
                parcalar.append(f'<text x="{kenar - 6}" y="{p + 4:.1f}" fill="#94a3b8" font-size="11" text-anchor="end">{etiket}</text>')
            v += adim
    # Eksenler
    if alt <= 0 <= ust:
        parcalar.append(f'<line x1="{kenar}" y1="{py(0):.1f}" x2="{G - kenar}" y2="{py(0):.1f}" stroke="#94a3b8" stroke-width="1.3"/>')
    if a <= 0 <= b:
        parcalar.append(f'<line x1="{px(0):.1f}" y1="{kenar}" x2="{px(0):.1f}" y2="{Y - kenar}" stroke="#94a3b8" stroke-width="1.3"/>')
    # Eğri (tanımsız / ekran dışı noktalarda kır)
    yol, kalem_kalkik = [], True
    for x, y in noktalar:
        if y is None or y < alt - (ust - alt) * 2 or y > ust + (ust - alt) * 2:
            kalem_kalkik = True
            continue
        yol.append(f'{"M" if kalem_kalkik else "L"}{px(x):.1f},{py(y):.1f}')
        kalem_kalkik = False
    clip_id = "k" + uuid.uuid4().hex[:8]
    parcalar.append(f'<clipPath id="{clip_id}"><rect x="{kenar}" y="{kenar}" width="{G - 2 * kenar}" height="{Y - 2 * kenar}"/></clipPath>')
    parcalar.append(f'<path d="{" ".join(yol)}" fill="none" stroke="#38bdf8" stroke-width="2.6" '
                    f'stroke-linejoin="round" stroke-linecap="round" clip-path="url(#{clip_id})"/>')
    parcalar.append(f'<text x="{G / 2}" y="24" fill="#e2e8f0" font-size="14" font-weight="600" text-anchor="middle">{baslik}</text>')
    return parcalar, px, py, (G, Y)


def _svg_tamamla(parcalar, px, py, noktalar):
    for x, y, renk, etiket in noktalar:
        parcalar.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="5" fill="{renk}" stroke="#0f172a" stroke-width="1.5"/>')
        parcalar.append(f'<text x="{px(x) + 8:.1f}" y="{py(y) - 8:.1f}" fill="{renk}" font-size="11.5" font-weight="600">{etiket}</text>')
    parcalar.append("</svg>")
    return "".join(parcalar)


def grafik_ciz(metin: str):
    """(yanıt_metni_işaretçili, etiket) veya (None, None)."""
    if not grafik_istegi_mi(metin):
        return None, None
    ifade, aralik = _ifade_ayikla(metin)
    if not ifade:
        return None, None
    try:
        f, tokenlar = _derleyici(ifade)
    except m14.MatHata:
        return None, None
    trig = any(t == ("fonk", ad) for t in tokenlar for ad in ("sin", "cos", "tan", "tg", "cot", "cotg"))
    a, b = aralik or ((-360.0, 360.0) if trig else (-5.0, 5.0))

    # Polinom (≤ 2. derece) ise tam analiz
    analiz, noktalar = [], []
    try:
        F = lambda x: m14._Ayristirici(tokenlar, Fraction(x)).calistir()
        c0, c1, cm1 = F(0), F(1), F(-1)
        if all(isinstance(v, Fraction) for v in (c0, c1, cm1)):
            c = c0
            qa = (c1 + cm1) / 2 - c
            qb = (c1 - cm1) / 2
            polinom = all(F(k) == qa * k * k + qb * k + c for k in (2, 3, -2, Fraction(1, 2)))
        else:
            polinom = False
    except Exception:
        polinom = False

    if polinom and qa != 0:
        tx = -qb / (2 * qa)
        ty = qa * tx * tx + qb * tx + c
        if not aralik:  # tepe noktasını ortala, kökleri kapsa
            yarim = max(5.0, abs(float(tx)) + 1, math.sqrt(abs(float(ty / qa))) * 1.8 if qa else 5)
            a, b = float(tx) - yarim, float(tx) + yarim
        analiz.append(f"- **Tür:** 2. derece (parabol), kollar **{'yukarı ↑' if qa > 0 else 'aşağı ↓'}**")
        analiz.append(f"- **Tepe noktası:** `T({m14.sayi_yaz(tx).split(' ≈')[0]}, {m14.sayi_yaz(ty).split(' ≈')[0]})` → "
                      f"fonksiyonun **en {'küçük' if qa > 0 else 'büyük'}** değeri `{m14.sayi_yaz(ty).split(' ≈')[0]}`")
        noktalar.append((float(tx), float(ty), "#facc15", "Tepe"))
        delta = qb * qb - 4 * qa * c
        if delta < 0:
            analiz.append("- **Kökler:** Δ < 0 → x eksenini **kesmez** (reel kök yok)")
        else:
            kd = math.sqrt(float(delta))
            kokler = sorted({(-float(qb) + kd) / (2 * float(qa)), (-float(qb) - kd) / (2 * float(qa))})
            analiz.append(f"- **Kökler (x eksenini kestiği yerler):** " + ", ".join(f"`x = {_sayi(k)}`" for k in kokler))
            noktalar += [(k, 0.0, "#f472b6", f"x={_sayi(k)}") for k in kokler]
    elif polinom and qb != 0:
        if not aralik:
            a, b = -10.0, 10.0
        kok = float(-c / qb)
        analiz.append(f"- **Tür:** 1. derece (doğru), eğim `m = {m14.sayi_yaz(qb).split(' ≈')[0]}` → "
                      f"{'artan ↗' if qb > 0 else 'azalan ↘'}")
        analiz.append(f"- **Kök:** `x = {_sayi(kok)}`")
        noktalar.append((kok, 0.0, "#f472b6", f"x={_sayi(kok)}"))
    elif polinom:
        analiz.append(f"- **Tür:** sabit fonksiyon `y = {m14.sayi_yaz(c).split(' ≈')[0]}` (yatay doğru)")
    else:
        kokler = _kokleri_bul(f, a, b)
        if kokler:
            analiz.append("- **Bu aralıktaki kökler (yaklaşık):** " + ", ".join(f"`x ≈ {_sayi(k)}`" for k in kokler))
            noktalar += [(k, 0.0, "#f472b6", f"{_sayi(k)}") for k in kokler[:6]]
        else:
            analiz.append("- **Kök:** bu aralıkta x eksenini kesmiyor")
    y0 = f(0.0)
    if a <= 0 <= b and y0 is not None:
        analiz.append(f"- **y-kesişimi:** `(0, {_sayi(y0)})`")
        if not any(abs(x) < 1e-9 and abs(y - y0) < 1e-9 for x, y, _, _ in noktalar):
            noktalar.append((0.0, y0, "#a78bfa", "y-kes."))

    gorunen = ifade.replace("*", "·").replace(" ", "")
    sonuc = _svg_olustur(f, a, b, [(x, y) for x, y, _, _ in noktalar], f"y = {gorunen}")
    if not sonuc:
        return f"📈 `y = {gorunen}` bu aralıkta tanımlı değil, başka bir aralık dener misin? (ör. *-5 ile 5 arasında*)", "📈 Grafik"
    parcalar, px, py, _ = sonuc
    svg = _svg_tamamla(parcalar, px, py, noktalar)
    metin_yanit = (f"📈 **Grafik:** `y = {gorunen}`  (x: {_sayi(a)} … {_sayi(b)}{', derece' if trig else ''})\n\n"
                   + "\n".join(analiz)
                   + "\n\n💡 Aralığı değiştirmek için: *\"y = ... grafiği -3 ile 3 arasında\"*")
    return metin_yanit + f"\n<!--AREX_SVG:{base64.b64encode(svg.encode()).decode()}-->", "📈 Grafik Çizici"


def svg_ayikla(cevap: str):
    """Yanıttaki SVG işaretçisini ayırır → (temiz_metin, svg | None)."""
    if not cevap or "<!--AREX_SVG:" not in cevap:
        return cevap, None
    m = _SVG_ISARET.search(cevap)
    svg = base64.b64decode(m.group(1)).decode() if m else None
    return _SVG_ISARET.sub("", cevap).rstrip(), svg


# ==============================================================================
# 2. SESLİ SORU — GROQ WHISPER
# ==============================================================================
def _multipart(alanlar: dict, dosya_adi: str, dosya_bayt: bytes, mime: str):
    sinir = "----AREX" + uuid.uuid4().hex
    govde = io.BytesIO()
    for ad, deger in alanlar.items():
        govde.write(f"--{sinir}\r\nContent-Disposition: form-data; name=\"{ad}\"\r\n\r\n{deger}\r\n".encode())
    govde.write(f"--{sinir}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{dosya_adi}\"\r\n"
                f"Content-Type: {mime}\r\n\r\n".encode())
    govde.write(dosya_bayt)
    govde.write(f"\r\n--{sinir}--\r\n".encode())
    return govde.getvalue(), f"multipart/form-data; boundary={sinir}"


def sesi_metne_cevir(ses_bayt: bytes, groq_anahtar: str, dil: str = "tr", dosya_adi: str = "ses.wav"):
    """Groq Whisper ile sesi yazıya döker → (metin, hata)."""
    if not groq_anahtar:
        return None, "Groq anahtarı yok"
    mime = "audio/wav" if dosya_adi.endswith(".wav") else "audio/mpeg"
    govde, tur = _multipart({"model": "whisper-large-v3-turbo", "language": dil, "response_format": "json",
                             "temperature": "0"}, dosya_adi, ses_bayt, mime)
    istek = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=govde,
                                   headers={"Authorization": f"Bearer {groq_anahtar}", "Content-Type": tur,
                                            "User-Agent": "AREX-AI-Studio/14"})
    try:
        with urllib.request.urlopen(istek, timeout=30) as yanit:
            metin = (json.loads(yanit.read().decode()).get("text") or "").strip()
        return (metin, None) if metin else (None, "Ses anlaşılamadı")
    except urllib.error.HTTPError as h:
        return None, f"Whisper hatası (HTTP {h.code})"
    except Exception as h:
        return None, f"Whisper bağlantı hatası ({type(h).__name__})"


# ==============================================================================
# 3. FOTOĞRAFTAN SORU ÇÖZME — GEMINI (görüntü destekli, ücretsiz katman)
# ==============================================================================
_FOTO_TALIMATI = (
    "Sen AREX adlı Türkçe bir ders asistanısın. Kullanıcı 9. sınıf öğrencisi. Fotoğraftaki soruyu dikkatle oku. "
    "1) Önce soruyu kısaca yaz ('**Soru:** ...'). 2) Çözümü numaralı, kısa adımlarla göster; işlemleri `kod` biçiminde yaz. "
    "3) En sonda '**Cevap:** ...' satırı olsun; şıklı soruysa doğru şıkkı belirt. "
    "Fotoğraf okunmuyorsa veya soru yoksa bunu dürüstçe söyle, uydurma. Telefondan okunacak; tablo kullanma."
)


def _gorseli_kucult(bayt: bytes, en_fazla: int = 1400):
    try:
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(bayt))).convert("RGB")
        im.thumbnail((en_fazla, en_fazla))
        cikti = io.BytesIO()
        im.save(cikti, "JPEG", quality=85, optimize=True)
        return cikti.getvalue(), "image/jpeg"
    except Exception:
        return bayt, "image/jpeg"


def fotograftan_soru_coz(gorsel_bayt: bytes, gemini_anahtar: str, ek_not: str = ""):
    """→ (yanıt_metni, hata)."""
    if not gemini_anahtar:
        return None, "anahtar_yok"
    veri, mime = _gorseli_kucult(gorsel_bayt)
    b64 = base64.b64encode(veri).decode()
    kullanici = [{"type": "text", "text": ("Bu fotoğraftaki soruyu çöz." + (f" Not: {ek_not}" if ek_not else ""))},
                 {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]
    son_hata = None
    for model in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-4-hydrogen"):
        govde = json.dumps({"model": model, "temperature": 0.2,
                            "messages": [{"role": "system", "content": _FOTO_TALIMATI},
                                         {"role": "user", "content": kullanici}]}).encode()
        istek = urllib.request.Request(
            "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", data=govde,
            headers={"Authorization": f"Bearer {gemini_anahtar}", "Content-Type": "application/json",
                     "User-Agent": "AREX-AI-Studio/14"})
        try:
            with urllib.request.urlopen(istek, timeout=60) as yanit:
                j = json.loads(yanit.read().decode())
            metin = (j.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
            if metin:
                return f"📸 **Fotoğraftan Soru Çözümü** *(Gemini · {model})*\n\n{metin}", None
        except urllib.error.HTTPError as h:
            son_hata = f"HTTP {h.code}"
            if h.code in (401, 403):
                return None, "Gemini anahtarı geçersiz veya yetkisiz (HTTP %d)" % h.code
        except Exception as h:
            son_hata = type(h).__name__
    return None, f"Gemini yanıt vermedi ({son_hata})"
