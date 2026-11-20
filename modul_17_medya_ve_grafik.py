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


# ==============================================================================
# 4. ÜCRETSİZ MEDYA ZEKÂSI — OCR (Tesseract) + Groq, Video/Ses (Whisper) ve YouTube
# ==============================================================================
import os
import shutil
import subprocess
import tempfile

_GROQ_SOHBET_URL = "https://api.groq.com/openai/v1/chat/completions"
_GROQ_MODELLER = ("openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b")


def _groq_sohbet(sistem: str, kullanici: str, anahtar: str, effort: str = "low", max_tokens: int = 2500):
    """Groq sohbet çağrısı (model sırasıyla, 429/5xx'te sıradakine geçer) → (metin, hata)."""
    if not anahtar:
        return None, "Groq anahtarı yok"
    son = None
    for model in _GROQ_MODELLER:
        govde = {"model": model, "temperature": 0.3, "max_tokens": max_tokens,
                 "messages": [{"role": "system", "content": sistem}, {"role": "user", "content": kullanici}]}
        if "gpt-oss" in model:
            govde["reasoning_effort"] = effort
        istek = urllib.request.Request(_GROQ_SOHBET_URL, data=json.dumps(govde).encode(),
                                       headers={"Authorization": f"Bearer {anahtar}", "Content-Type": "application/json",
                                                "User-Agent": "AREX-AI-Studio/14"})
        try:
            with urllib.request.urlopen(istek, timeout=40) as y:
                metin = json.loads(y.read().decode())["choices"][0]["message"]["content"].strip()
            if metin:
                return metin, None
        except urllib.error.HTTPError as h:
            son = f"HTTP {h.code}"
            if h.code in (401, 403):
                break
        except Exception as h:
            son = type(h).__name__
    if son == "HTTP 429":
        return None, "Groq ücretsiz kullanım sınırına ulaşıldı; 1 dakika sonra tekrar dener misin?"
    return None, f"Groq yanıt vermedi ({son})"


# ---------- 4.1 Fotoğraf → OCR → çözüm ----------
def ocr_hazir_mi() -> bool:
    try:
        import pytesseract  # noqa: F401
        return bool(shutil.which("tesseract"))
    except Exception:
        return False


def _ocr_temizle(metin: str) -> str:
    metin = re.sub(r"[ \t]+", " ", metin)
    return "\n".join(s.strip() for s in metin.splitlines() if s.strip())


def ocr_metni_cikar(gorsel_bayt: bytes):
    """Tesseract (Türkçe + İngilizce) ile fotoğraftaki yazıyı 3 farklı ön işlemeyle okur.
    → (okumalar_listesi, hata). Tek bir ayar her karakteri doğru okuyamadığı için (ör. '7' → '/')
    farklı okumalar birlikte değerlendirilir (çoğunluk/karşılaştırma)."""
    try:
        import pytesseract
        from PIL import Image, ImageOps, ImageFilter
    except Exception:
        return None, "OCR kütüphanesi (pytesseract) kurulu değil"
    if not shutil.which("tesseract"):
        return None, "Tesseract programı kurulu değil"
    try:
        ham = ImageOps.exif_transpose(Image.open(io.BytesIO(gorsel_bayt))).convert("L")
        diller = "tur+eng" if "tur" in pytesseract.get_languages(config="") else "eng"

        def olcekle(im, hedef):
            oran = hedef / max(im.size)
            return im.resize((max(1, int(im.width * oran)), max(1, int(im.height * oran))), Image.LANCZOS)

        varyantlar = []
        for hedef in (1600, 2400):
            im = ImageOps.autocontrast(olcekle(ham, hedef), cutoff=1)
            esik = im.point(lambda p: 255 if p > 150 else 0)
            varyantlar += [im.filter(ImageFilter.SHARPEN), esik] if hedef == 1600 else [esik]
        okumalar = []
        for v in varyantlar:
            metin = _ocr_temizle(pytesseract.image_to_string(v, lang=diller, config="--psm 6"))
            if len(re.sub(r"\W", "", metin)) >= 4 and metin not in okumalar:
                okumalar.append(metin)
        return (okumalar, None) if okumalar else (None, "Fotoğrafta okunabilir yazı bulunamadı")
    except Exception as h:
        return None, f"OCR hatası ({type(h).__name__})"


_OCR_COZUM_TALIMATI = (
    "Sen AREX adlı Türkçe bir ders asistanısın; kullanıcı 9. sınıf öğrencisi. Aşağıdaki metin bir fotoğraftan OCR ile "
    "okundu; harf/sembol hataları olabilir (ör. 'x2' aslında 'x²', '√' yerine 'V', 'O' yerine '0'). Önce soruyu mantıklı "
    "biçimde düzelterek '**Soru:** ...' diye yaz. Sonra çözümü numaralı kısa adımlarla göster, işlemleri `kod` biçiminde yaz. "
    "En sonda '**Cevap:** ...' satırı olsun; şıklıysa doğru şıkkı belirt. Metinden soru anlaşılmıyorsa uydurma, bunu söyle. "
    "Birden çok soru varsa kullanıcı notunda belirtileni, yoksa ilkini çöz. Tablo kullanma.\n"
    "ÖNEMLİ: Aynı fotoğrafın birden fazla OCR okuması verilebilir. Karakterleri okumalar arasında KARŞILAŞTIR; "
    "bir okumada '/', 'l', 'I' görünen yer diğerinde rakamsa rakamı esas al (çoğunluk). Üslü sayılar OCR'da bozulur: "
    "'^' işareti '4' gibi okunabilir ('2^5' → '245'), küçük yazılmış üsler tabana yapışır ('3²' → '32'); '.' veya '·' "
    "çarpma olabilir. Şıklara uyan en mantıklı yorumu bul. Çözümün sonunda cevabı soruya geri "
    "koyarak SAĞLAMA yap; şıklardan hiçbirine uymuyorsa okumayı yeniden değerlendir. Hâlâ emin değilsen bunu açıkça yaz."
)


def _siklari_bul(okumalar):
    """OCR okumalarından 'A) 19  B) 21 ...' şıklarını çıkarır → {'A': '19', ...} (en çok şık bulan okuma)."""
    en_iyi = {}
    for o in okumalar:
        bulunan = {h.upper(): d.strip(" .") for h, d in re.findall(r"\b([A-Ea-e])\s*[)\.]\s*([^\sA-E)][^\n]*?)(?=\s+[A-Ea-e]\s*[)\.]|\n|$)", o)}
        if len(bulunan) > len(en_iyi):
            en_iyi = bulunan
    return en_iyi if len(en_iyi) >= 3 else {}


def _cevap_sikka_uyuyor_mu(cozum: str, siklar: dict) -> bool:
    satir = (re.findall(r"\*\*Cevap:?\*\*:?\s*(.+)", cozum) or [""])[-1]
    if not satir:
        return False
    satir_n = satir.replace(",", ".").replace(" ", "")
    for harf, deger in siklar.items():
        deger_n = deger.replace(",", ".").replace(" ", "")
        if re.search(rf"(?<![A-Za-z]){harf}(?:\)|\s|\*|$|\.)", satir) or (deger_n and deger_n in satir_n):
            return True
    return False


def fotograftan_soru_coz_ucretsiz(gorsel_bayt: bytes, groq_anahtar: str, ek_not: str = ""):
    """OCR + Groq: tamamen ücretsiz fotoğraf çözümü → (yanıt, hata)."""
    okumalar, hata = ocr_metni_cikar(gorsel_bayt)
    if not okumalar:
        return None, hata
    metin = okumalar[0]
    istek = "\n\n".join(f"OCR OKUMASI {i + 1}:\n{o[:2500]}" for i, o in enumerate(okumalar)) + (
        f"\n\nKULLANICI NOTU: {ek_not}" if ek_not else "")
    cozum, hata = _groq_sohbet(_OCR_COZUM_TALIMATI, istek, groq_anahtar, effort="medium")
    if not cozum:
        return None, hata
    # Şık sağlaması (kodla, modele bırakmadan): cevap şıklardan birine uymuyorsa bir kez daha, daha derin düşün
    siklar = _siklari_bul(okumalar)
    if siklar and not _cevap_sikka_uyuyor_mu(cozum, siklar):
        ikinci, _ = _groq_sohbet(_OCR_COZUM_TALIMATI, istek + "\n\nNOT: Önceki çözümün cevabı şıklardan hiçbirine "
                                 "uymadı. OCR hatalarını (özellikle üs, çarpma, kesir işaretleri) yeniden yorumla ve "
                                 "şıklardan birine ulaşan tutarlı ifadeyi bul.", groq_anahtar, effort="high")
        if ikinci and _cevap_sikka_uyuyor_mu(ikinci, siklar):
            cozum = ikinci
        else:
            cozum = ("⚠️ **Emin değilim:** Fotoğraftaki ifade net okunamadı ve bulduğum sonuç şıklarla uyuşmuyor. "
                     "Soruyu yazarak gönderirsen ya da daha net/düz bir fotoğraf çekersen kesin çözerim.\n\n" + cozum)
    okunan = "\n".join(f"> {s}" for s in metin.splitlines()[:8])
    return (f"📸 **Fotoğraftan Soru Çözümü** *(ücretsiz: Tesseract OCR + Groq)*\n\n{cozum}\n\n"
            f"**🔍 Fotoğraftan okunan metin:**\n{okunan}"), None


# ---------- 4.2 Video / ses dosyası → Whisper → özet ----------
_WHISPER_SINIR = 24 * 1024 * 1024
_SES_UZANTILARI = (".mp3", ".m4a", ".wav", ".ogg", ".webm", ".flac", ".mpga", ".mpeg", ".mp4")


def _ffmpeg_ile_sese_cevir(bayt: bytes, uzanti: str):
    """Video/büyük ses → mono 16 kHz 48 kbps MP3 (Whisper için yeterli, ~20 kat küçük)."""
    if not shutil.which("ffmpeg"):
        return None
    with tempfile.TemporaryDirectory() as d:
        giris, cikis = os.path.join(d, "giris" + uzanti), os.path.join(d, "cikis.mp3")
        with open(giris, "wb") as f:
            f.write(bayt)
        try:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", giris, "-vn", "-ac", "1", "-ar", "16000",
                            "-b:a", "48k", "-t", "5400", cikis], check=True, timeout=300)
            with open(cikis, "rb") as f:
                return f.read()
        except Exception:
            return None


def _whisper_yazi(ses_bayt: bytes, dosya_adi: str, anahtar: str):
    mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4", "mp4": "video/mp4", "ogg": "audio/ogg",
            "webm": "audio/webm", "flac": "audio/flac"}.get(dosya_adi.rsplit(".", 1)[-1].lower(), "application/octet-stream")
    govde, tur = _multipart({"model": "whisper-large-v3-turbo", "response_format": "json", "temperature": "0"},
                            dosya_adi, ses_bayt, mime)
    istek = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=govde,
                                   headers={"Authorization": f"Bearer {anahtar}", "Content-Type": tur,
                                            "User-Agent": "AREX-AI-Studio/14"})
    try:
        with urllib.request.urlopen(istek, timeout=180) as y:
            return (json.loads(y.read().decode()).get("text") or "").strip(), None
    except urllib.error.HTTPError as h:
        return None, f"Whisper hatası (HTTP {h.code})"
    except Exception as h:
        return None, f"Whisper bağlantı hatası ({type(h).__name__})"


_OZET_TALIMATI = (
    "Sen AREX adlı Türkçe bir asistansın. Sana bir video/ses kaydının veya YouTube videosunun yazıya dökülmüş metni "
    "verilecek (başka dilde olabilir). TÜRKÇE yanıt ver ve şu biçimi kullan:\n"
    "**🎯 Kısaca:** 1-2 cümlelik ana fikir\n**📌 Ana noktalar:** 4-7 madde\n"
    "**🧠 Öğrenilecek kavramlar:** (varsa) 2-5 kavram ve kısa açıklaması\n"
    "Metinde olmayan bilgiyi ekleme; konuşma metni anlamsızsa (müzik, gürültü) bunu söyle. Tablo kullanma."
)


def medya_dosyasini_ozetle(bayt: bytes, dosya_adi: str, groq_anahtar: str):
    """Video/ses dosyası → (yanıt, hata)."""
    if not groq_anahtar:
        return None, "Groq anahtarı yok"
    uzanti = "." + dosya_adi.rsplit(".", 1)[-1].lower() if "." in dosya_adi else ".mp4"
    gonderilecek, ad = bayt, dosya_adi
    video_mu = uzanti in (".mp4", ".mov", ".mkv", ".avi", ".3gp", ".webm")
    if len(bayt) > _WHISPER_SINIR or uzanti not in _SES_UZANTILARI or video_mu:
        donusen = _ffmpeg_ile_sese_cevir(bayt, uzanti)
        if donusen:
            gonderilecek, ad = donusen, "ses.mp3"
        elif len(bayt) > _WHISPER_SINIR or uzanti not in _SES_UZANTILARI:
            return None, "Dosya çok büyük ya da biçimi desteklenmiyor (ffmpeg yok). 24 MB altı MP3/MP4/M4A/WAV dene."
    if len(gonderilecek) > _WHISPER_SINIR:
        return None, "Ses çok uzun (sıkıştırıldıktan sonra da 24 MB'ı aşıyor). Daha kısa bir bölüm dene."
    yazi, hata = _whisper_yazi(gonderilecek, ad, groq_anahtar)
    if not yazi:
        return None, hata or "Kayıtta konuşma bulunamadı"
    ozet, hata = _groq_sohbet(_OZET_TALIMATI, f"KAYIT METNİ ({len(yazi)} karakter):\n{yazi[:14000]}", groq_anahtar)
    if not ozet:
        return None, hata
    alinti = yazi[:1500] + ("…" if len(yazi) > 1500 else "")
    return (f"🎬 **Video / Ses Özeti** *(ücretsiz: Groq Whisper + Groq)* — `{dosya_adi}`\n\n{ozet}\n\n"
            f"**📝 Konuşma metninden:**\n> {alinti}"), None


# ---------- 4.3 YouTube bağlantısı → altyazı → özet ----------
_YT_DESEN = re.compile(r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/|embed/)|youtu\.be/)([A-Za-z0-9_-]{11})")


def youtube_kimligi(metin: str):
    m = _YT_DESEN.search(metin or "")
    return m.group(1) if m else None


def youtube_ozetle(metin: str, groq_anahtar: str):
    """Mesajda YouTube bağlantısı varsa altyazıyı çekip özetler → (yanıt, etiket) | (None, None)."""
    vid = youtube_kimligi(metin)
    if not vid:
        return None, None
    if not groq_anahtar:
        return "▶️ YouTube özeti için Groq anahtarı gerekiyor (Streamlit Secrets → `GROQ_API_KEY`).", "▶️ YouTube"
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception:
        return "▶️ YouTube özeti için `youtube-transcript-api` paketi kurulu değil.", "▶️ YouTube"
    try:
        api = YouTubeTranscriptApi()
        try:
            veri = api.fetch(vid, languages=["tr", "en"])
        except Exception:
            liste = api.list(vid)
            veri = next(iter(liste)).fetch()
        yazi = " ".join(p.text for p in veri.snippets if p.text and not re.fullmatch(r"\[.*\]|♪+", p.text.strip()))
        dil = getattr(veri, "language_code", "?")
    except Exception as h:
        ad = type(h).__name__
        neden = ("YouTube bu sunucudan gelen istekleri engelliyor" if "Block" in ad or "IpBlocked" in ad
                 else "Bu videoda altyazı yok veya kapalı" if "Transcript" in ad or "Disabled" in ad
                 else f"altyazı alınamadı ({ad})")
        return (f"▶️ Bu videonun özetini çıkaramadım: **{neden}**.\n\n💡 Alternatif: videoyu indirip "
                f"*📎 Fotoğraf / Video → 🎬 Video* bölümünden yükleyebilirsin; sesi Whisper ile yazıya döküp özetlerim."), "▶️ YouTube"
    if len(yazi) < 40:
        return "▶️ Bu videonun altyazısında özetlenecek konuşma yok (müzik/klip olabilir).", "▶️ YouTube"
    ek = re.sub(_YT_DESEN, "", metin).strip()
    ozet, hata = _groq_sohbet(_OZET_TALIMATI, f"YOUTUBE ALTYAZISI (dil: {dil}):\n{yazi[:14000]}"
                              + (f"\n\nKULLANICININ İSTEĞİ: {ek}" if len(ek) > 3 else ""), groq_anahtar)
    if not ozet:
        return f"▶️ Altyazıyı aldım ama özetleyemedim ({hata}).", "▶️ YouTube"
    return (f"▶️ **YouTube Video Özeti** *(altyazı: {dil}, ücretsiz)*\n\n{ozet}\n\n"
            f"🔗 https://youtu.be/{vid}"), "▶️ YouTube Özeti"
