# -*- coding: utf-8 -*-
"""
AREX — Modül 25: KALICI ANAHTAR KASASI + ORTAK YAPAY ZEKA ÇEKİRDEĞİ
==============================================================================
• Anahtar kasası: ~/.arex/anahtarlar.json (proje klasörü DIŞINDA → git dal değişimi,
  yeniden klonlama veya klasör silme anahtarları SİLEMEZ). Açılışta ortam değişkenlerine
  yüklenir; .streamlit/secrets.toml yalnızca yedek kaynaktır.
• Sağlayıcı zinciri (hepsi ücretsiz katman): Groq → Gemini → OpenRouter (:free) → Pollinations.
• Görsel / video analizi: Gemini (görüntü + video doğrudan), yedek OpenRouter görsel model.
Anahtar değerleri hiçbir zaman ekrana / loga yazılmaz.
"""
import base64
import json
import os
import re
import time
import urllib.error
import urllib.request

KASA_DIZINI = os.path.join(os.path.expanduser("~"), ".arex")
KASA_DOSYASI = os.path.join(KASA_DIZINI, "anahtarlar.json")
_PROJE = os.path.dirname(os.path.abspath(__file__))
_SECRETS = os.path.join(_PROJE, ".streamlit", "secrets.toml")

ANAHTAR_ADLARI = {
    "GROQ_API_KEY": "⚡ Groq",
    "GEMINI_API_KEY": "💎 Google Gemini",
    "OPENROUTER_API_KEY": "🔀 OpenRouter",
}
_UA = "Mozilla/5.0 (AREX-AI-Studio)"


# ------------------------------------------------------------------------------
# 1. KALICI KASA
# ------------------------------------------------------------------------------
def kasayi_oku() -> dict:
    try:
        with open(KASA_DOSYASI, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return {k: str(v).strip() for k, v in veri.items() if str(v or "").strip()} if isinstance(veri, dict) else {}
    except Exception:
        return {}


def _secrets_toml_oku() -> dict:
    sonuc = {}
    try:
        with open(_SECRETS, "r", encoding="utf-8") as f:
            for satir in f:
                m = re.match(r'^\s*([A-Z0-9_]+)\s*=\s*["\']?([^"\'\n]+)["\']?\s*$', satir)
                if m:
                    sonuc[m.group(1)] = m.group(2).strip()
    except Exception:
        pass
    return sonuc


def _secrets_toml_yaz(ad: str, deger: str):
    """Yerel çalışmada Streamlit'in st.secrets'ı da görsün diye (bulutta dokunmaz)."""
    if os.path.exists("/mount/src"):
        return
    try:
        os.makedirs(os.path.dirname(_SECRETS), exist_ok=True)
        satirlar = []
        if os.path.exists(_SECRETS):
            with open(_SECRETS, "r", encoding="utf-8") as f:
                satirlar = [s.rstrip("\n") for s in f if not re.match(rf"^\s*{ad}\s*=", s)]
        if deger:
            satirlar.append(f'{ad} = "{deger}"')
        with open(_SECRETS, "w", encoding="utf-8") as f:
            f.write("\n".join(satirlar) + "\n")
    except Exception:
        pass


def anahtar_kaydet(ad: str, deger: str) -> bool:
    """Anahtarı kalıcı kasaya (+ yerel secrets.toml'a) yazar ve hemen etkinleştirir. Boş değer = sil."""
    deger = (deger or "").strip().strip('"').strip("'")
    try:
        os.makedirs(KASA_DIZINI, exist_ok=True)
        try:
            os.chmod(KASA_DIZINI, 0o700)
        except Exception:
            pass
        veri = kasayi_oku()
        if deger:
            veri[ad] = deger
        else:
            veri.pop(ad, None)
        gecici = KASA_DOSYASI + ".tmp"
        with open(gecici, "w", encoding="utf-8") as f:
            json.dump(veri, f, indent=1)
        os.replace(gecici, KASA_DOSYASI)
        try:
            os.chmod(KASA_DOSYASI, 0o600)
        except Exception:
            pass
    except Exception:
        return False
    if deger:
        os.environ[ad] = deger
    else:
        os.environ.pop(ad, None)
    _secrets_toml_yaz(ad, deger)
    return True


def anahtarlari_yukle() -> dict:
    """Açılışta: kasa → secrets.toml → (Streamlit Cloud) st.secrets. Bulunanları os.environ'a koyar."""
    bulunan = {}
    bulunan.update(_secrets_toml_oku())
    bulunan.update(kasayi_oku())  # kasa önceliklidir
    try:
        import streamlit as st
        for ad in ANAHTAR_ADLARI:
            if ad not in bulunan:
                try:
                    v = str(st.secrets.get(ad, "") or "").strip()
                except Exception:
                    v = ""
                if v:
                    bulunan[ad] = v
    except Exception:
        pass
    for ad, deger in bulunan.items():
        if ad.endswith(("_KEY", "_TOKEN")) and deger and not os.environ.get(ad):
            os.environ[ad] = deger
    # Kasada yoksa ama secrets'ta varsa kasaya da kopyala → bir daha kaybolmaz
    kasa = kasayi_oku()
    for ad in ANAHTAR_ADLARI:
        if bulunan.get(ad) and not kasa.get(ad) and not os.path.exists("/mount/src"):
            anahtar_kaydet(ad, bulunan[ad])
    return {ad: bool(os.environ.get(ad)) for ad in ANAHTAR_ADLARI}


def anahtar(ad: str) -> str:
    return (os.environ.get(ad) or kasayi_oku().get(ad) or "").strip()


def maskele(deger: str) -> str:
    deger = deger or ""
    return (deger[:4] + "•" * 8 + deger[-3:]) if len(deger) > 10 else ("•" * len(deger))


# ------------------------------------------------------------------------------
# 2. HTTP YARDIMCISI + KOTA HAFIZASI
# ------------------------------------------------------------------------------
_KOTA = {}  # "saglayici:model" -> tekrar denenebilir zaman
SON_HATALAR = {}


def _post(url: str, govde: dict, basliklar: dict, zaman_asimi: float):
    istek = urllib.request.Request(
        url, data=json.dumps(govde).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": _UA, **basliklar}, method="POST")
    with urllib.request.urlopen(istek, timeout=zaman_asimi) as yanit:
        return json.loads(yanit.read().decode("utf-8"))


def _temizle(metin: str) -> str:
    metin = re.sub(r"<think>.*?</think>", "", metin or "", flags=re.DOTALL)
    return metin.strip()


GROQ_MODELLER = ("openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b")
GEMINI_METIN = ("gemini-3.5-flash-lite", "gemini-3.5-flash")
GEMINI_GORSEL = ("gemini-3.5-flash", "gemini-3.5-flash-lite")
OPENROUTER_MODELLER = ("openrouter/free", "nvidia/nemotron-3-ultra-550b-a55b:free", "google/gemma-4-31b-it:free")
OPENROUTER_GORSEL = ("nvidia/nemotron-3.5-super-vl:free", "google/gemma-4-31b-it:free")


def _openai_uyumlu(saglayici, url, key, model, mesajlar, sicaklik, maks, zaman_asimi, ek_baslik=None):
    kota_k = f"{saglayici}:{model}"
    if _KOTA.get(kota_k, 0) > time.time():
        return None
    govde = {"model": model, "messages": mesajlar, "temperature": sicaklik, "max_tokens": maks}
    if "gpt-oss" in model:
        govde["reasoning_effort"] = "low"
    try:
        veri = _post(url, govde, {"Authorization": f"Bearer {key}", **(ek_baslik or {})}, zaman_asimi)
        metin = _temizle(((veri.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
        if metin:
            SON_HATALAR[saglayici] = f"OK ({model})"
            return metin
    except urllib.error.HTTPError as e:
        SON_HATALAR[saglayici] = f"HTTP {e.code} ({model})"
        if e.code == 429:
            _KOTA[kota_k] = time.time() + 60
        if e.code in (401, 403):
            _KOTA[kota_k] = time.time() + 600
    except Exception as e:
        SON_HATALAR[saglayici] = f"{type(e).__name__} ({model})"
    return None


def sohbet_tamamla(mesajlar: list, sistem: str = "", sicaklik: float = 0.7, maks_token: int = 1800,
                   tercih: str = "") -> tuple:
    """
    OpenAI biçimli mesajlarla (role/content) sağlayıcı zincirini dener.
    tercih: "gemini" verilirse önce Gemini (çok dilli yaratıcı yazıda çok iyi), "groq" → önce Groq.
    Dönüş: (metin | None, kullanılan_motor_etiketi)
    """
    tam = ([{"role": "system", "content": sistem}] if sistem else []) + [
        {"role": m["role"], "content": str(m["content"])} for m in mesajlar
        if m.get("role") in ("user", "assistant", "system") and m.get("content")]

    def groq():
        k = anahtar("GROQ_API_KEY")
        if not k:
            return None, None
        for m in GROQ_MODELLER:
            t = _openai_uyumlu("groq", "https://api.groq.com/openai/v1/chat/completions", k, m, tam,
                               sicaklik, min(maks_token, 2500), 30)
            if t:
                return t, f"Groq {m.split('/')[-1]}"
        return None, None

    def gemini():
        k = anahtar("GEMINI_API_KEY")
        if not k:
            return None, None
        for m in GEMINI_METIN:
            t = _openai_uyumlu("gemini", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                               k, m, tam, sicaklik, maks_token, 45)
            if t:
                return t, f"Gemini {m.replace('gemini-', '')}"
        return None, None

    def openrouter():
        k = anahtar("OPENROUTER_API_KEY")
        if not k:
            return None, None
        for m in OPENROUTER_MODELLER:
            t = _openai_uyumlu("openrouter", "https://openrouter.ai/api/v1/chat/completions", k, m, tam,
                               sicaklik, maks_token, 40, {"X-Title": "AREX AI Studio"})
            if t:
                return t, f"OpenRouter {m.split('/')[-1].replace(':free', '')}"
        return None, None

    def pollinations():
        t = _openai_uyumlu("pollinations", "https://text.pollinations.ai/openai", "anon", "openai-fast", tam,
                           sicaklik, maks_token, 40)
        return (t, "Pollinations") if t else (None, None)

    sira = [groq, gemini, openrouter, pollinations]
    if tercih == "gemini":
        sira = [gemini, groq, openrouter, pollinations]
    elif tercih == "openrouter":
        sira = [openrouter, groq, gemini, pollinations]
    for fn in sira:
        metin, etiket = fn()
        if metin:
            return metin, etiket
    return None, None


# ------------------------------------------------------------------------------
# 3. GÖRSEL & VİDEO ANALİZİ (Gemini çok kipli; yedek: OpenRouter görsel model)
# ------------------------------------------------------------------------------
def _mime_bul(ad: str, varsayilan: str = "image/jpeg") -> str:
    uz = (ad or "").lower().rsplit(".", 1)[-1]
    return {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "heic": "image/heic",
        "gif": "image/gif", "mp4": "video/mp4", "mov": "video/quicktime", "webm": "video/webm", "3gp": "video/3gpp",
        "m4a": "audio/mp4", "mp3": "audio/mpeg", "wav": "audio/wav", "ogg": "audio/ogg",
    }.get(uz, varsayilan)


GEMINI_SATIR_ICI_SINIR = 18 * 1024 * 1024  # istek başına ~20 MB sınırı


def medya_analiz_et(veri: bytes, dosya_adi: str, talimat: str, sistem: str = "", gecmis: list = None,
                    maks_token: int = 2500, derin: bool = False) -> tuple:
    """Fotoğraf / kısa video / ses dosyasını metin talimatıyla analiz eder. (metin | None, etiket | hata)"""
    mime = _mime_bul(dosya_adi)
    if len(veri) > GEMINI_SATIR_ICI_SINIR:
        return None, "Dosya çok büyük (en fazla ~18 MB). Videoyu kısaltıp veya sıkıştırıp tekrar dene."
    b64 = base64.b64encode(veri).decode("ascii")
    k = anahtar("GEMINI_API_KEY")
    if k:
        icerik = []
        for m in (gecmis or [])[-6:]:
            if m.get("role") in ("user", "assistant") and m.get("content"):
                icerik.append({"role": "user" if m["role"] == "user" else "model",
                               "parts": [{"text": str(m["content"])[:1500]}]})
        icerik.append({"role": "user", "parts": [{"inline_data": {"mime_type": mime, "data": b64}}, {"text": talimat}]})
        govde = {"contents": icerik, "generationConfig": {"temperature": 0.4, "maxOutputTokens": maks_token}}
        if sistem:
            govde["systemInstruction"] = {"parts": [{"text": sistem}]}
        for model in (GEMINI_GORSEL if derin else tuple(reversed(GEMINI_GORSEL))):
            if _KOTA.get(f"gemini:{model}", 0) > time.time():
                continue
            try:
                yanit = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                              govde, {"x-goog-api-key": k}, 90 if mime.startswith("video") else 60)
                parcalar = (((yanit.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [])
                metin = _temizle("".join(p.get("text", "") for p in parcalar))
                if metin:
                    return metin, f"Gemini {model.replace('gemini-', '')} (görsel)"
            except urllib.error.HTTPError as e:
                SON_HATALAR["gemini"] = f"HTTP {e.code} ({model})"
                if e.code == 429:
                    _KOTA[f"gemini:{model}"] = time.time() + 60
            except Exception as e:
                SON_HATALAR["gemini"] = f"{type(e).__name__} ({model})"
    # Yedek: OpenRouter ücretsiz görsel model (yalnız fotoğraf)
    ork = anahtar("OPENROUTER_API_KEY")
    if ork and mime.startswith("image"):
        mesajlar = ([{"role": "system", "content": sistem}] if sistem else []) + [{
            "role": "user", "content": [
                {"type": "text", "text": talimat},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]}]
        for model in OPENROUTER_GORSEL:
            t = _openai_uyumlu("openrouter", "https://openrouter.ai/api/v1/chat/completions", ork, model,
                               mesajlar, 0.4, maks_token, 60, {"X-Title": "AREX AI Studio"})
            if t:
                return t, f"OpenRouter {model.split('/')[-1].replace(':free', '')} (görsel)"
    if not k and not ork:
        return None, "Görsel analiz için Gemini (veya OpenRouter) anahtarı gerekli — 🔌 API bölümünden ekle."
    return None, "Görsel analiz servisleri şu an yanıt vermedi (kota/bağlantı). Biraz sonra tekrar dene."


# ------------------------------------------------------------------------------
# 4. DİL ALGILAMA (yazı sisteminden; hızlı ve çevrimdışı)
# ------------------------------------------------------------------------------
DIL_ADLARI = {
    "tr": "Türkçe", "en": "English", "bn": "বাংলা (Bengalce)", "ar": "العربية (Arapça)", "ru": "Русский (Rusça)",
    "de": "Deutsch", "fr": "Français", "es": "Español", "zh": "中文", "ja": "日本語", "hi": "हिन्दी", "ur": "اردو",
    "fa": "فارسی", "az": "Azərbaycanca", "uk": "Українська", "it": "Italiano", "pt": "Português", "id": "Bahasa Indonesia",
}


def yazidan_dil_tahmin(metin: str) -> str:
    metin = metin or ""
    if re.search(r"[ঀ-৿]", metin):
        return "bn"
    if re.search(r"[؀-ۿ]", metin):
        return "fa" if re.search(r"[پچژگ]", metin) else "ar"
    if re.search(r"[Ѐ-ӿ]", metin):
        return "uk" if re.search(r"[іїєґ]", metin.lower()) else "ru"
    if re.search(r"[ऀ-ॿ]", metin):
        return "hi"
    if re.search(r"[぀-ヿ]", metin):
        return "ja"
    if re.search(r"[一-鿿]", metin):
        return "zh"
    if re.search(r"[çğıöşüÇĞİÖŞÜ]", metin) or re.search(r"\b(ve|bir|bu|ne|nasıl|mı|mi|için|ben|sen)\b", metin.lower()):
        return "tr"
    kelimeler = re.findall(r"[a-zA-Z']+", metin.lower())
    ing = {"the", "is", "are", "what", "how", "you", "i", "my", "can", "please", "tell", "me", "a", "an", "and",
           "story", "write", "why", "do", "does", "hello", "hi", "thanks"}
    if len(kelimeler) >= 3 and sum(1 for k in kelimeler if k in ing) / len(kelimeler) >= 0.25:
        return "en"
    return ""


# ------------------------------------------------------------------------------
# 5. DOĞAL ANLATICI SESİ (Gemini TTS — üslup talimatlı; çok dilli) → WAV
# ------------------------------------------------------------------------------
ANLATICILAR = {
    "masalci": ("🧚 Masal Perisi", "Leda"),
    "anne": ("👩 Sıcak Anne Sesi", "Sulafat"),
    "dede": ("👴 Dede Masalcı", "Algieba"),
    "neseli": ("😄 Neşeli Anlatıcı", "Puck"),
    "fisilti": ("🌙 Uyku Fısıltısı", "Achernar"),
    "abla": ("👧 Abla / Ağabey", "Aoede"),
}
ANLATIM_USLUPLARI = {
    "masal": "Sıcak, merak uyandıran, usta bir masalcı gibi; cümle aralarında doğal duraksamalarla, karakterlerin "
             "konuşmalarında hafifçe farklı ses tonları kullanarak, gülümseyerek anlat",
    "uyku": "Çok yavaş, yumuşacık, fısıltıya yakın ve huzurlu bir sesle; uzun nefesli duraksamalarla, uyutacak gibi anlat",
    "komik": "Neşeli, enerjik ve şakacı; komik yerlerde gülümseyen bir tonla, karakterlere eğlenceli sesler vererek anlat",
    "macera": "Heyecanlı ama sevecen; merak anlarında yavaşlayıp, sürprizlerde canlanan bir tonla anlat",
    "sohbet": "Doğal, samimi ve sevecen bir arkadaş gibi konuş",
    "bilgi": "Açık, anlaşılır, sıcak bir öğretmen gibi anlat",
}


def _pcm_wav(pcm: bytes, hz: int = 24000) -> bytes:
    import struct
    return (b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, hz, hz * 2, 2, 16) + b"data" + struct.pack("<I", len(pcm)) + pcm)


def _parcala(metin: str, sinir: int = 1400) -> list:
    parcalar, simdiki = [], ""
    for paragraf in re.split(r"\n\s*\n|\n", metin):
        paragraf = paragraf.strip()
        if not paragraf:
            continue
        if len(simdiki) + len(paragraf) + 2 > sinir and simdiki:
            parcalar.append(simdiki)
            simdiki = ""
        while len(paragraf) > sinir:
            kes = paragraf.rfind(". ", 0, sinir)
            kes = kes + 1 if kes > 200 else sinir
            parcalar.append(paragraf[:kes])
            paragraf = paragraf[kes:].strip()
        simdiki = (simdiki + "\n\n" + paragraf).strip()
    if simdiki:
        parcalar.append(simdiki)
    return parcalar


def dogal_anlatim_sesi(metin: str, uslup: str = "masal", anlatici: str = "masalci") -> bytes:
    """Gemini TTS ile doğal anlatıcı sesi (WAV). Kota/anahtar yoksa b'' döner (çağıran edge-tts'e düşer)."""
    k = anahtar("GEMINI_API_KEY")
    if not k or _KOTA.get("gemini:tts", 0) > time.time():
        return b""
    ses_adi = ANLATICILAR.get(anlatici, ANLATICILAR["masalci"])[1]
    talimat = ANLATIM_USLUPLARI.get(uslup, ANLATIM_USLUPLARI["masal"])
    parcalar = _parcala(metin)[:8]

    def _tek(p):
        govde = {"contents": [{"parts": [{"text": f"{talimat}:\n\n{p}"}]}],
                 "generationConfig": {"responseModalities": ["AUDIO"],
                                      "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": ses_adi}}}}}
        y = _post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent",
                  govde, {"x-goog-api-key": k}, 120)
        veri = y["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        return base64.b64decode(veri)

    try:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as h:
            pcm_listesi = list(h.map(_tek, parcalar))
        sessizlik = b"\x00\x00" * 12000  # parçalar arası 0,5 sn nefes
        return _pcm_wav(sessizlik.join(pcm_listesi))
    except urllib.error.HTTPError as e:
        SON_HATALAR["gemini_tts"] = f"HTTP {e.code}"
        if e.code == 429:
            _KOTA["gemini:tts"] = time.time() + 300
    except Exception as e:
        SON_HATALAR["gemini_tts"] = type(e).__name__
    return b""


# ------------------------------------------------------------------------------
# 6. CANLI SOHBET (Gemini Live) — GEÇİCİ TOKEN: asıl anahtar tarayıcıya gitmez
# ------------------------------------------------------------------------------
def canli_gecici_token(dakika: int = 30, kullanim: int = 20) -> str:
    import datetime as _dt
    k = anahtar("GEMINI_API_KEY")
    if not k:
        return ""
    simdi = _dt.datetime.now(_dt.timezone.utc)
    govde = {"uses": kullanim,
             "expireTime": (simdi + _dt.timedelta(minutes=dakika)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "newSessionExpireTime": (simdi + _dt.timedelta(minutes=dakika)).strftime("%Y-%m-%dT%H:%M:%SZ")}
    try:
        return _post("https://generativelanguage.googleapis.com/v1alpha/auth_tokens", govde,
                     {"x-goog-api-key": k}, 20).get("name", "")
    except Exception as e:
        SON_HATALAR["gemini_live"] = type(e).__name__
        return ""


def canli_sayfa_html(mod: str = "asistan", dil: str = "tr", ses: str = "Leda", yas: str = "7-9",
                     profil: str = "", ad: str = "") -> str:
    """static/canli.html'i geçici token ve ayarlarla gömülmeye hazır hale getirir."""
    yol = os.path.join(_PROJE, "static", "canli.html")
    with open(yol, "r", encoding="utf-8") as f:
        html = f.read()
    cfg = {"t": canli_gecici_token(), "mod": mod, "dil": dil, "ses": ses, "yas": yas, "profil": profil[:1500], "ad": ad}
    enjekte = "<script>window.AREX_CANLI=" + json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/") + ";</script>"
    return html.replace("<head>", "<head>" + enjekte, 1)
