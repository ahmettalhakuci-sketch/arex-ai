# -*- coding: utf-8 -*-
"""
AREX — Modül 31: KUR'AN, HADİS, ESMÂ (açık kaynak) + SOHBET TARZLARI + BAĞLANTI KOMUTLARI
==============================================================================
• alquran.cloud — Arapça metin + Diyanet Vakfı meali (tr.vakfi) + Alafasy tilaveti
• HadeethEnc.com — kaynaklı ve dereceli Türkçe hadis (433 kategori; konu eşleştirme)
• AlAdhan — Esmâ-i Hüsnâ
Sohbet motoru (Modül 8) bu modülü yapay zekâdan ÖNCE çağırır: ayet/hadis asla uydurulmaz.
Ayrıca: "mizah modu aç / içten sohbet modu / mümin modu / normal moda dön" ve
"YouTube'da X ara / Google'da X ara / haritada X göster" (tıklanabilir bağlantı) komutları.
"""
import datetime as _dt
import json
import random
import re
import time
import unicodedata
import urllib.parse
import urllib.request

SURELER = ["Fâtiha", "Bakara", "Âl-i İmrân", "Nisâ", "Mâide", "En'âm", "A'râf", "Enfâl", "Tevbe", "Yûnus", "Hûd", "Yûsuf", "Ra'd",
           "İbrâhîm", "Hicr", "Nahl", "İsrâ", "Kehf", "Meryem", "Tâhâ", "Enbiyâ", "Hac", "Mü'minûn", "Nûr", "Furkân", "Şuarâ", "Neml",
           "Kasas", "Ankebût", "Rûm", "Lokmân", "Secde", "Ahzâb", "Sebe'", "Fâtır", "Yâsîn", "Sâffât", "Sâd", "Zümer", "Mü'min",
           "Fussilet", "Şûrâ", "Zuhruf", "Duhân", "Câsiye", "Ahkâf", "Muhammed", "Fetih", "Hucurât", "Kâf", "Zâriyât", "Tûr", "Necm",
           "Kamer", "Rahmân", "Vâkıa", "Hadîd", "Mücâdele", "Haşr", "Mümtehine", "Saff", "Cuma", "Münâfikûn", "Teğâbün", "Talâk",
           "Tahrîm", "Mülk", "Kalem", "Hâkka", "Meâric", "Nûh", "Cin", "Müzzemmil", "Müddessir", "Kıyâme", "İnsân", "Mürselât", "Nebe'",
           "Nâziât", "Abese", "Tekvîr", "İnfitâr", "Mutaffifîn", "İnşikâk", "Bürûc", "Târık", "A'lâ", "Gâşiye", "Fecr", "Beled", "Şems",
           "Leyl", "Duhâ", "İnşirâh", "Tîn", "Alak", "Kadir", "Beyyine", "Zilzâl", "Âdiyât", "Kâria", "Tekâsür", "Asr", "Hümeze", "Fîl",
           "Kureyş", "Mâûn", "Kevser", "Kâfirûn", "Nasr", "Tebbet", "İhlâs", "Felak", "Nâs"]
KURAN_KATEGORILERI = [31, 12, 39, 272, 1]  # hafızlık adabı, Kur'an'ın faziletleri…
_ONBELLEK = {}


def _json(url: str, ttl: float = 3600, zaman_asimi: float = 12):
    simdi = time.time()
    if url in _ONBELLEK and simdi - _ONBELLEK[url][0] < ttl:
        return _ONBELLEK[url][1]
    istek = urllib.request.Request(url, headers={"User-Agent": "AREX-AI/15", "Accept": "application/json"})
    with urllib.request.urlopen(istek, timeout=zaman_asimi) as y:
        veri = json.loads(y.read().decode("utf-8"))
    _ONBELLEK[url] = (simdi, veri)
    return veri


def sadele(s: str) -> str:
    s = (s or "").replace("İ", "i").replace("I", "ı").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"['’^]", "", s).replace("ı", "i")


def sure_bul(ad: str) -> int:
    q = sadele(ad.strip())
    if q.isdigit():
        return max(1, min(114, int(q)))
    for i, s in enumerate(SURELER):
        if sadele(s) == q:
            return i + 1
    for i, s in enumerate(SURELER):
        ss = sadele(s)
        if len(q) >= 3 and (ss.startswith(q) or q.startswith(ss)):
            return i + 1
    return 0


def ayetler(sure: int, bas: int = 1, son: int = None, meal: str = "tr.vakfi") -> list:
    son = son or bas
    limit = max(1, min(30, son - bas + 1))
    d = _json(f"https://api.alquran.cloud/v1/surah/{sure}/editions/quran-uthmani,{meal},ar.alafasy?offset={bas - 1}&limit={limit}")
    ar, tr, ses = d["data"]
    return [{"sure": sure, "sure_ad": SURELER[sure - 1], "no": a["numberInSurah"], "arapca": a["text"],
             "meal": tr["ayahs"][i]["text"], "ses": ses["ayahs"][i].get("audio", "")} for i, a in enumerate(ar["ayahs"])]


def _gun_no() -> int:
    return (_dt.date.today() - _dt.date(1970, 1, 1)).days


def gunun_ayeti() -> dict:
    n = (_gun_no() * 37) % 6236 + 1
    d = _json(f"https://api.alquran.cloud/v1/ayah/{n}/editions/quran-uthmani,tr.vakfi,ar.alafasy", ttl=86400)
    ar, tr, ses = d["data"]
    return {"sure": ar["surah"]["number"], "sure_ad": SURELER[ar["surah"]["number"] - 1], "no": ar["numberInSurah"],
            "arapca": ar["text"], "meal": tr["text"], "ses": ses.get("audio", "")}


KONU_KATEGORI = {"sabi": [282, 646], "sabr": [282, 646], "nama": [134], "oruc": [137], "anne": [273], "baba": [273], "ebev": [273],
                 "kura": [31, 12, 39, 272], "hafi": [31], "dua": [268], "zikr": [268, 301], "ahla": [282, 266], "ilim": [31, 12],
                 "sukr": [282], "sukur": [282], "cenn": [338], "tevb": [282], "merh": [282, 646], "dogr": [282]}


def _kokler(q: str) -> set:
    """Türkçe ünlü düşmesine dayanıklı kökler: sabır→{sabi, sabr}, şükür→{suku, sukr}, namaz→{nama}"""
    if len(q) < 3:
        return set()
    k = {q[:4]}
    if len(q) >= 5:
        k.add(q[:3] + q[4])
    return k


def hadis(konu: str = "", secim: int = None, kat_id: int = None) -> dict:
    kategoriler = _json("https://hadeethenc.com/api/v1/categories/list/?language=tr", ttl=86400)
    q = re.sub(r"\b(ile|ilgili|hakkinda|konulu|bir|hadis\w*)\b", "", sadele(konu)).strip()
    rnd = (lambda n: secim % n) if secim is not None else (lambda n: random.randrange(n))
    kokler = _kokler(q.split()[0]) if q else set()
    adaylar_kat = [kat_id] if kat_id else []
    for k in kokler:
        adaylar_kat += KONU_KATEGORI.get(k, [])
    adaylar_kat += [c["id"] for c in kategoriler if any(w.startswith(tuple(kokler)) for w in sadele(c.get("title", "")).split())] if kokler else []
    if not adaylar_kat:
        adaylar_kat = [kategoriler[rnd(len(kategoriler))]["id"]]
    eslesen, yedek = [], []
    for kid in list(dict.fromkeys(adaylar_kat))[:5]:
        liste = _json(f"https://hadeethenc.com/api/v1/hadeeths/list/?language=tr&category_id={kid}&page=1&per_page=60").get("data") or []
        yedek = yedek or liste
        eslesen += [h for h in liste if kokler and any(w.startswith(tuple(kokler)) for w in sadele(h.get("title", "")).split())]
        if eslesen:
            break
    havuz = eslesen or yedek or _json("https://hadeethenc.com/api/v1/hadeeths/list/?language=tr&category_id=31&page=1&per_page=50")["data"]
    sec = havuz[rnd(len(havuz))]
    h = _json(f"https://hadeethenc.com/api/v1/hadeeths/one/?language=tr&id={sec['id']}", ttl=86400)
    return {"baslik": h.get("title", ""), "metin": h.get("hadeeth", ""), "kaynak": h.get("attribution", ""), "derece": h.get("grade", ""),
            "tam_eslesme": bool(eslesen) or not q}


def gunun_hadisi() -> dict:
    g = _gun_no()
    return hadis("", secim=g, kat_id=KURAN_KATEGORILERI[g % len(KURAN_KATEGORILERI)])


def esma(no: int = None) -> dict:
    n = no if no and 1 <= no <= 99 else (_gun_no() % 99) + 1
    x = _json(f"https://api.aladhan.com/v1/asmaAlHusna/{n}", ttl=86400)["data"][0]
    return {"no": x["number"], "isim": x["name"], "okunus": x["transliteration"], "anlam": x["en"]["meaning"]}


def _ayet_md(a: dict) -> str:
    return f"**{a['sure_ad']} {a['no']}**\n\n> {a['arapca']}\n\n{a['meal']}"


def _hadis_md(h: dict) -> str:
    return f"### 📜 {h['baslik']}\n\n{h['metin']}\n\n_Kaynak: {h['kaynak'] or '—'} • Derece: {h['derece'] or '—'} (HadeethEnc.com)_"


_SURE_AYET_RE = re.compile(
    r"^\s*([A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ'’\- ]{2,20}?)\s*(?:suresi(?:nin)?\s*)?(\d{1,3})\s*(?:[-–:]\s*(\d{1,3}))?\.?\s*"
    r"(?:ayet\w*)?\s*(?:meal\w*|oku|nedir|ne diyor)?\s*\??$", re.IGNORECASE)


def din_sorusu_cevapla(metin: str):
    """Kur'an/hadis/esma isteği ise (cevap, etiket), değilse (None, None)."""
    t = (metin or "").strip()
    tl = t.replace("İ", "i").replace("I", "ı").lower()
    try:
        if re.search(r"günün ayeti|bugünün ayeti|gunun ayeti", tl):
            return "### 📖 Günün Ayeti\n\n" + _ayet_md(gunun_ayeti()) + "\n\n_Kaynak: Kur'an-ı Kerim, Diyanet Vakfı meali (alquran.cloud)_", "📖 Günün Ayeti"
        if re.search(r"günün hadisi|bugünün hadisi|gunun hadisi", tl):
            return "### 🌙 Günün Hadisi\n\n" + _hadis_md(gunun_hadisi()), "🌙 Günün Hadisi"
        if re.search(r"\bhadis", tl) and re.search(r"söyle|oku|ver|anlat|getir|paylaş|bir hadis|hadis-i şerif", tl):
            m = re.search(r"(.{2,40}?)\s+(?:ile|hakkında|ilgili|konulu)\s+(?:bir\s+)?hadis", tl)
            konu = re.sub(r"\b(bana|bir|lütfen)\b", "", m.group(1)).strip() if m else ""
            h = hadis(konu)
            not_ = "" if h.get("tam_eslesme", True) else f"_ℹ️ Kaynakta \"{konu}\" başlığıyla birebir hadis bulamadım; ilgili bir hadis paylaşıyorum._\n\n"
            return not_ + _hadis_md(h), "📜 Hadis (HadeethEnc)"
        if re.search(r"esma|esmaül|esmaul|esmâ|allah'ın isimleri", tl):
            n = re.search(r"\b(\d{1,2})\b", tl)
            e = esma(int(n.group(1)) if n else None)
            return (f"### ✨ Esmâ-i Hüsnâ — {e['no']}.\n\n> **{e['isim']}** ({e['okunus']})\n\nAnlamı: {e['anlam']}\n\n_Kaynak: AlAdhan_",
                    "✨ Esmâ-i Hüsnâ")
        m = _SURE_AYET_RE.match(t)
        if m and re.search(r"sure|ayet|meal|oku|^[A-Za-zÇĞİÖŞÜçğıöşüâîû'’ -]+\s+\d+", t, re.IGNORECASE):
            s = sure_bul(m.group(1))
            if s:
                bas = int(m.group(2))
                son = min(int(m.group(3)) if m.group(3) else bas, bas + 9)
                liste = ayetler(s, bas, son)
                if liste:
                    govde = "\n\n".join(f"> {a['arapca']}\n\n**{a['no']}.** {a['meal']}" for a in liste)
                    return (f"### 📖 {SURELER[s - 1]} {bas}{'-' + str(liste[-1]['no']) if son > bas else ''}\n\n{govde}\n\n"
                            "_Kaynak: Kur'an-ı Kerim, Diyanet Vakfı meali (alquran.cloud)_"), "📖 Kur'an (alquran.cloud)"
    except Exception:
        return "⚠️ Kur'an/hadis kaynağına şu an ulaşılamadı; biraz sonra tekrar dener misin?", "📖 Kur'an/Hadis"
    return None, None


# ------------------------------------------------------------------------------
# Sohbet tarzları (mizah / içten / mümin)
# ------------------------------------------------------------------------------
SOHBET_TARZLARI = {
    "dengeli": ("🎯 Dengeli", ""),
    "icten": ("💞 İçten sohbet", "İÇTEN SOHBET TARZI: Acele etme; önce gerçekten dinle ve duyguyu yansıt. Sıcak, samimi, yargısız ve derin konuş; "
                                "madde listeleri yerine içten paragraflar kur; uygun yerde nazik bir soruyla sohbeti derinleştir. Ciddi bir sıkıntı "
                                "sezersen güvendiği biriyle ya da bir uzmanla konuşmasını nazikçe öner."),
    "mizah": ("😄 Mizah", "MİZAH TARZI: Sıcak, zekice, sevimli-abartılı Türk mizahıyla konuş: iltifatları tatlı abartıyla büyüt, espri ve kelime "
                         "oyunu yap. Örnek: 'Kuran hocam çok iyi' → 'Kuran hocanın ellerinden öpüyorum! Senin gibi talebe yetiştirdiyse o hocaya "
                         "madalya lazım!'. Hocalarla, büyüklerle edepli mizah. SINIR: dini değerler, kutsal şeyler, görünüş, gruplar ile ASLA "
                         "alay yok; ciddi/üzücü konuda mizahı bırak."),
    "mumin": ("🕌 Mümin", "MÜMİN TARZI: Edepli bir Müslüman gibi konuş: kullanıcı selam verirse 'Aleyküm selam' de; yerinde 'Elhamdülillah', "
                         "'Maşallah', 'İnşallah', 'Allah razı olsun' kullan; hocalara 'hocam' diye saygıyla hitap et. Fetva verme, Diyanet'e ve "
                         "hocalara yönlendir."),
}
_TARZ_SELAM = {"mizah": "😄 Mizah modu açıldı! Hazırlan, iltifat yağmuru başlıyor 🎉", "icten": "💞 İçten sohbet modu açık. Acele yok; seni dinliyorum…",
               "mumin": "🕌 Mümin modu açık. Hoş geldin, Allah razı olsun.", "dengeli": "🎯 Normal (dengeli) moda döndüm."}


def tarz_komutu(metin: str):
    """'mizah modu aç' vb. → (yeni_tarz, cevap) | (None, None)"""
    tl = (metin or "").replace("İ", "i").replace("I", "ı").lower().strip()
    if len(tl) > 60:
        return None, None
    kapat = bool(re.search(r"kapat|kapa|bitir|normal moda|dengeli moda", tl))
    tarz = None
    if re.search(r"mizah mod", tl):
        tarz = "dengeli" if kapat else "mizah"
    elif re.search(r"içten (sohbet )?mod|icten (sohbet )?mod", tl):
        tarz = "dengeli" if kapat else "icten"
    elif re.search(r"m[üu]'?min mod", tl):
        tarz = "dengeli" if kapat else "mumin"
    elif re.search(r"normal moda d[öo]n|dengeli moda", tl):
        tarz = "dengeli"
    return (tarz, _TARZ_SELAM[tarz]) if tarz else (None, None)


# ------------------------------------------------------------------------------
# Bağlantı komutları (bilgisayarda tıklanabilir bağlantı)
# ------------------------------------------------------------------------------
def baglanti_komutu(metin: str):
    t = (metin or "").replace("İ", "i").replace("I", "ı").lower().strip(" .!?")
    q = lambda s: urllib.parse.quote(s.strip())
    m = re.match(r"^youtube'?(?:da|de|ta|te)?\s+(.+?)\s+(?:ara|aç|bul|izle|oynat|çal)$", t)
    if m:
        return f"▶️ [YouTube'da **{m.group(1)}** sonuçlarını aç](https://www.youtube.com/results?search_query={q(m.group(1))})", "▶️ YouTube"
    if re.match(r"^(?:youtube|yutup)(?:\s?'?(?:[ıiuü]|y?[ae]))?\s*(?:aç|başlat|geç|git|gir)$", t):
        return "▶️ [YouTube'u aç](https://www.youtube.com)", "▶️ YouTube"
    m = re.match(r"^google'?(?:da|de|ta)?\s+(.+?)\s+(?:ara|bul)$", t)
    if m:
        return f"🔎 [Google'da **{m.group(1)}** ara](https://www.google.com/search?q={q(m.group(1))})", "🔎 Google"
    m = re.match(r"^(?:haritada|haritalarda)\s+(.+?)\s+(?:göster|bul|aç|ara)$", t)
    if m:
        return f"🗺️ [Haritada **{m.group(1)}**](https://www.google.com/maps/search/{q(m.group(1))})", "🗺️ Harita"
    m = re.match(r"^spotify'?(?:da|de|ta)?\s+(.+?)\s+(?:çal|aç|ara|dinle)$", t)
    if m:
        return f"🎵 [Spotify'da **{m.group(1)}**](https://open.spotify.com/search/{q(m.group(1))})", "🎵 Spotify"
    return None, None
