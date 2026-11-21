# -*- coding: utf-8 -*-
"""
AREX — Modül 29: İLERİ MATEMATİK MOTORU (SymPy — açık kaynak, kesin sembolik hesap)
==============================================================================
Modül 14 (aritmetik, 1.-2. derece denklem) yetmediğinde devreye girer:
  • Türev (n. mertebe, kısmi), integral (belirsiz / belirli), limit (±∞, sağdan/soldan), Taylor serisi
  • 3. ve üstü dereceden denklemler, trigonometrik/üstel denklemler, denklem SİSTEMLERİ, eşitsizlikler
  • Çarpanlara ayırma, açma, sadeleştirme, kesirleri ayırma (apart)
  • Matris: determinant, ters, özdeğer, rank, transpoz, çarpım
  • İstatistik: ortalama, medyan, mod, varyans, standart sapma, açıklık
  • Kombinasyon C(n,r), permütasyon P(n,r), faktöriyel, OBEB/OKEK, mod alma
Sonuç SymPy ile KESİN hesaplanır; istenirse yapay zekâ yalnızca bu doğrulanmış sonucu adım adım açıklar
(sonuç uydurması engellenir).

Giriş: ileri_matematik_coz(metin, aciklama=True) -> (cevap_markdown, etiket) | (None, None)
"""
import re
import statistics

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                            standard_transformations)
    _HAZIR = True
except Exception:  # SymPy yoksa modül sessizce devre dışı
    sp = None
    _HAZIR = False

_DONUSUM = (standard_transformations + (implicit_multiplication_application, convert_xor)) if _HAZIR else None
_SEMBOLLER = {}
if _HAZIR:
    x, y, z, t, n, a, b, c, k = sp.symbols("x y z t n a b c k")
    _SEMBOLLER = {"x": x, "y": y, "z": z, "t": t, "n": n, "a": a, "b": b, "c": c, "k": k, "e": sp.E, "pi": sp.pi,
                  "π": sp.pi, "oo": sp.oo, "sonsuz": sp.oo, "ln": sp.log, "log": lambda v, taban=10: sp.log(v, taban),
                  "sqrt": sp.sqrt, "kok": sp.sqrt, "arcsin": sp.asin, "arccos": sp.acos, "arctan": sp.atan,
                  "cot": sp.cot, "sec": sp.sec, "csc": sp.csc, "abs": sp.Abs, "mutlak": sp.Abs, "exp": sp.exp}

_UST = str.maketrans({"²": "^2", "³": "^3", "⁴": "^4", "⁵": "^5", "⁻": "-", "¹": "^1", "×": "*", "÷": "/", "−": "-",
                      "√": "sqrt", "∞": "oo", "π": "pi", "≤": "<=", "≥": ">="})


def _temiz_ifade(s: str) -> str:
    s = (s or "").translate(_UST).strip().strip("?.!:;")
    s = re.sub(r"(?i)\bsonsuz\b", "oo", s)
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)  # 2,5 → 2.5 (Türkçe ondalık)
    s = re.sub(r"sqrt\s*(\d+(?:\.\d+)?|[a-z])", r"sqrt(\1)", s)
    s = re.sub(r"\be\^", "E^", s)
    s = re.sub(r"(?i)\b(kaçtır|kaç|nedir|bul|hesapla|olur|eder)\b", "", s)
    s = re.sub(r"(?i)\s*(adım adım|adim adim|açıkla(?:r mısın)?|anlat|nasıl|lütfen|göster|çözümlü|detaylı)\b.*$", "", s)
    return s.strip()


def _ifade(s: str):
    return parse_expr(_temiz_ifade(s), local_dict=_SEMBOLLER, transformations=_DONUSUM, evaluate=True)


def _latex(v) -> str:
    try:
        return sp.latex(v)
    except Exception:
        return str(v)


def _blok(baslik: str, girdi, sonuc, ek: str = "") -> str:
    satir = [f"### 🧮 {baslik}", f"$$ {girdi} $$" if girdi else "", f"**Sonuç:**", f"$$ {sonuc} $$"]
    if ek:
        satir.append(ek)
    return "\n\n".join(s for s in satir if s)


def _degisken(ifade, tercih=None):
    serbest = sorted(ifade.free_symbols, key=lambda s: str(s))
    if tercih and _SEMBOLLER.get(tercih) in serbest:
        return _SEMBOLLER[tercih]
    for ad in ("x", "t", "y", "z", "n"):
        if _SEMBOLLER[ad] in serbest:
            return _SEMBOLLER[ad]
    return serbest[0] if serbest else _SEMBOLLER["x"]


def _sayisal(v) -> str:
    try:
        f = complex(sp.N(v, 12))
        if abs(f.imag) < 1e-12:
            r = f.real
            return f"{r:.10g}".replace(".", ",")
        return f"{f.real:.6g} {'+' if f.imag >= 0 else '-'} {abs(f.imag):.6g}i".replace(".", ",")
    except Exception:
        return ""


# ------------------------------------------------------------------------------
# İşlemler
# ------------------------------------------------------------------------------
def _turev(t: str):
    m = re.search(r"(?i)(?:(\d+)\s*\.?\s*(?:mertebe(?:den)?\s*)?)?(?:türev(?:i|ini|ini al)?|derivative|d/d([a-z]))\s*[:\-]?\s*(.+)", t)
    m2 = re.search(r"(?i)^(.+?)\s*(?:'?n?[ıiuü]n\b|ifadesinin|fonksiyonunun)?\s*(?:(\d+)\s*\.\s*)?(?:türevi|türevini)", t)
    if m2:
        ifade_s, mertebe, deg = m2.group(1), m2.group(2), None
    elif m:
        mertebe, deg, ifade_s = m.group(1), m.group(2), m.group(3)
    else:
        return None
    ifade_s = re.sub(r"(?i)^(f\(x\)|y)\s*=\s*", "", ifade_s)
    ifade_s = re.sub(r"(?i)\s*(?:'?n?[ıiuü]n)?\s*(?:türevi|türevini al|türevini bul)\s*$", "", ifade_s)
    ifade_s = re.sub(r"(?i)(?<=[\)\dxyz])\s*'?n?[ıiuü]n\s*$", "", ifade_s.strip())
    f = _ifade(ifade_s)
    v = _degisken(f, deg)
    mer = int(mertebe or 1)
    sonuc = sp.simplify(sp.diff(f, v, mer))
    return _blok(f"{mer if mer > 1 else ''}{'. mertebeden ' if mer > 1 else ''}Türev (d/d{v})",
                 f"\\frac{{d{'^' + str(mer) if mer > 1 else ''}}}{{d{v}{'^' + str(mer) if mer > 1 else ''}}}\\left({_latex(f)}\\right)",
                 _latex(sonuc)), f"türev {f} → {sonuc}"


def _integral(t: str):
    if not re.search(r"(?i)integral|∫|integre", t):
        return None
    sinir = re.search(r"(?i)(-?[\w.π∞]+)\s*(?:'?(?:dan|den|tan|ten))\s*(-?[\w.π∞]+)\s*'?(?:a|e|ya|ye)\s*(?:kadar\s*)?(?:integral(?:i)?)?\s*[:\-]?\s*(.*)", t)
    govde = re.sub(r"(?i)(?:belirli\s+|belirsiz\s+)?(?:integral(?:i|ini al|ini)?|∫|integre et)\s*[:\-]?", " ", t)
    alt = ust = None
    if sinir and sinir.group(3).strip():
        alt, ust, govde = sinir.group(1), sinir.group(2), sinir.group(3)
    else:
        m = re.search(r"(.+?)[,;]\s*(-?[\w.π∞]+)\s*[,;]\s*(-?[\w.π∞]+)\s*$", govde)
        if m:
            govde, alt, ust = m.group(1), m.group(2), m.group(3)
    govde = re.sub(r"(?i)\s*d([a-z])\s*$", "", govde.strip())
    govde = re.sub(r"(?i)(?<=[\)\dxyz])\s*'?n?[ıiuü]n\s*$", "", govde.strip())
    f = _ifade(govde)
    v = _degisken(f)
    if alt is not None:
        a_, b_ = _ifade(alt), _ifade(ust)
        sonuc = sp.simplify(sp.integrate(f, (v, a_, b_)))
        say = _sayisal(sonuc)
        return _blok("Belirli İntegral", f"\\int_{{{_latex(a_)}}}^{{{_latex(b_)}}} {_latex(f)}\\, d{v}", _latex(sonuc),
                     f"≈ **{say}**" if say and say != str(sonuc) else ""), f"∫[{alt},{ust}] {f} = {sonuc}"
    sonuc = sp.integrate(f, v)
    if isinstance(sonuc, sp.Integral):
        return _blok("İntegral", f"\\int {_latex(f)}\\, d{v}", "\\text{Kapalı biçimde ifade edilemiyor}"), "integral yok"
    return _blok("Belirsiz İntegral", f"\\int {_latex(f)}\\, d{v}", _latex(sp.simplify(sonuc)) + " + C"), f"∫ {f} = {sonuc} + C"


def _limit(t: str):
    m = re.search(r"(?i)(?:lim(?:it)?)\s*[:\-]?\s*([a-z])\s*(?:->|→|giderken|yaklaşırken|=>)\s*([+\-]?[\w.π∞]+)\s*([+\-])?\s*(?:için\s*)?[,:]?\s*(.+)", t)
    if not m:
        m2 = re.search(r"(?i)([a-z])\s*(?:->|→)\s*([+\-]?[\w.π∞]+)\s*(?:iken|için)?\s*(.+?)\s*(?:'?[ıiuü]n)?\s*limiti", t)
        if not m2:
            return None
        v_ad, hedef, yon, govde = m2.group(1), m2.group(2), None, m2.group(3)
    else:
        v_ad, hedef, yon, govde = m.group(1), m.group(2), m.group(3), m.group(4)
    if re.search(r"(?i)sağdan", t):
        yon = "+"
    elif re.search(r"(?i)soldan", t):
        yon = "-"
    f = _ifade(govde)
    v = _SEMBOLLER.get(v_ad, sp.Symbol(v_ad))
    h = _ifade(hedef)
    sonuc = sp.limit(f, v, h, dir=yon or "+-") if not h.is_infinite else sp.limit(f, v, h)
    return _blok("Limit", f"\\lim_{{{v} \\to {_latex(h)}{'^' + yon if yon else ''}}} {_latex(f)}", _latex(sonuc)), \
        f"limit {f}, {v}→{h} = {sonuc}"


def _seri(t: str):
    m = re.search(r"(?i)(?:taylor|maclaurin|seri(?:ye aç|si)?)\s*[:\-]?\s*(.+?)(?:\s*,\s*([a-z])\s*=\s*(-?[\w.]+))?(?:\s*,\s*(\d+))?$", t)
    if not m or not re.search(r"(?i)taylor|maclaurin|seri", t):
        return None
    f = _ifade(m.group(1))
    v = _degisken(f, m.group(2))
    nokta = _ifade(m.group(3)) if m.group(3) else 0
    derece = int(m.group(4) or 6)
    sonuc = sp.series(f, v, nokta, derece)
    return _blok(f"Taylor Serisi ({v} = {nokta} civarı)", _latex(f), _latex(sonuc)), f"seri {f}"


def _cebir(t: str):
    kaliplar = [
        (r"(?i)(?:çarpanlarına ayır|çarpanlara ayır|faktör(?:ize)?|factor)\s*[:\-]?\s*(.+)", "Çarpanlara Ayırma", sp.factor),
        (r"(?i)(?:sadeleştir|simplify|basitleştir)\s*[:\-]?\s*(.+)", "Sadeleştirme", sp.simplify),
        (r"(?i)(?:aç|genişlet|expand|açılımı(?:nı)?(?: bul)?)\s*[:\-]?\s*(.+)", "Açılım", sp.expand),
        (r"(?i)(?:basit kesirlere ayır|kesirlere ayır|apart)\s*[:\-]?\s*(.+)", "Basit Kesirlere Ayırma", sp.apart),
    ]
    for desen, ad, fn in kaliplar:
        m = re.search(desen, t)
        if m:
            f = _ifade(m.group(1))
            return _blok(ad, _latex(f), _latex(fn(f))), f"{ad} {f}"
    m = re.search(r"(?i)^(.+?)\s*(?:'?[ıiuü]n)?\s*(?:açılımı|çarpanları)\s*$", t)
    if m:
        f = _ifade(m.group(1))
        fn = sp.expand if "açılım" in t else sp.factor
        return _blok("Açılım" if fn is sp.expand else "Çarpanlara Ayırma", _latex(f), _latex(fn(f))), "cebir"
    return None


def _esitsizlik(t: str):
    if not re.search(r"<=|>=|<|>", _temiz_ifade(t)) or "=>" in t or "->" in t:
        return None
    govde = re.sub(r"(?i)\b(çöz|eşitsizliğini|eşitsizlik|çözüm kümesi(?:ni)?|bul)\b", "", t).strip(" :")
    ifade = _temiz_ifade(govde)
    m = re.match(r"(.+?)(<=|>=|<|>)(.+)", ifade)
    if not m:
        return None
    sol, op, sag = _ifade(m.group(1)), m.group(2), _ifade(m.group(3))
    rel = {"<": sp.Lt, ">": sp.Gt, "<=": sp.Le, ">=": sp.Ge}[op](sol, sag)
    v = _degisken(sol - sag)
    sonuc = sp.solve_univariate_inequality(rel, v, relational=False)
    return _blok("Eşitsizlik", _latex(rel), f"{v} \\in {_latex(sonuc)}"), f"eşitsizlik {rel}: {sonuc}"


def _denklem(t: str):
    govde = re.sub(r"(?i)\b(denklem(?:ini|leri|lerini|i)?|sistemini|sistemi|çöz|çözümü|kökleri(?:ni)?|bul|kaçtır|nedir)\b", "", t)
    parcalar = [p for p in re.split(r"[;,]\s*|\s+ve\s+", govde) if "=" in p]
    if not parcalar or any(op in govde for op in ("<", ">")):
        return None
    denklemler = []
    for p in parcalar:
        sol, sag = p.split("=", 1)
        if not sol.strip() or not sag.strip():
            return None
        denklemler.append(sp.Eq(_ifade(sol), _ifade(sag)))
    degiskenler = sorted(set().union(*[d.free_symbols for d in denklemler]), key=str)
    if not degiskenler:
        return None
    # Tek bilinmeyenli 1.-2. derece basit denklemleri Modül 14'e bırak (kendi adım adım çıktısı var)
    if len(denklemler) == 1 and len(degiskenler) == 1:
        try:
            der = sp.Poly(denklemler[0].lhs - denklemler[0].rhs, degiskenler[0]).degree()
            if der <= 2 and not re.search(r"(?i)sin|cos|tan|log|ln|e\^|exp|sqrt|√", t):
                return None
        except Exception:
            pass
    if len(denklemler) == 1 and len(degiskenler) == 1:
        v = degiskenler[0]
        try:
            kumeler = sp.solveset(denklemler[0], v, domain=sp.S.Complexes)
        except Exception:
            kumeler = None
        cozum = sp.solve(denklemler[0], v)
        reel = [c for c in cozum if c.is_real]
        ek = ""
        if cozum:
            ek = "**Kökler:** " + ", ".join(f"${v} = {_latex(c)}$" + (f" (≈ {_sayisal(c)})" if not c.is_Integer else "") for c in cozum)
            if len(reel) != len(cozum):
                ek += f"\n\n🔹 Reel kök sayısı: **{len(reel)}**, karmaşık kök sayısı: **{len(cozum) - len(reel)}**"
        sonuc = _latex(kumeler) if kumeler is not None and not isinstance(kumeler, sp.ConditionSet) else _latex(set(cozum))
        return _blok("Denklem Çözümü", _latex(denklemler[0]), f"\\text{{Çözüm kümesi: }} {sonuc}", ek), f"denklem {denklemler[0]}: {cozum}"
    cozum = sp.solve(denklemler, degiskenler, dict=True)
    if not cozum:
        return _blok("Denklem Sistemi", " \\\\ ".join(_latex(d) for d in denklemler), "\\text{Çözüm yok (tutarsız sistem)}"), "sistem çözümsüz"
    satirlar = [", ".join(f"{k} = {_latex(v)}" for k, v in c.items()) for c in cozum]
    return _blok("Denklem Sistemi", "\\begin{cases}" + " \\\\ ".join(_latex(d) for d in denklemler) + "\\end{cases}",
                 " \\quad ; \\quad ".join(satirlar)), f"sistem {denklemler}: {cozum}"


def _matris(t: str):
    m = re.search(r"(\[\s*\[.*\]\s*\])", t)
    if not m or not re.search(r"(?i)matris|det|ters|invers|özdeğer|rank|transpoz|determinant|eigen", t):
        return None
    try:
        M = sp.Matrix(eval(m.group(1), {"__builtins__": {}}, {}))
    except Exception:
        return None
    tl = t.lower()
    if "ters" in tl or "invers" in tl:
        if M.det() == 0:
            return _blok("Ters Matris", _latex(M), "\\text{Determinant 0 → tersi yok}"), "ters yok"
        return _blok("Ters Matris", _latex(M) + "^{-1}", _latex(M.inv())), "ters"
    if "özdeğer" in tl or "eigen" in tl:
        return _blok("Özdeğerler", _latex(M), ", ".join(f"\\lambda = {_latex(k)}\\;(\\times{v})" for k, v in M.eigenvals().items())), "özdeğer"
    if "rank" in tl:
        return _blok("Rank", _latex(M), str(M.rank())), "rank"
    if "transpoz" in tl:
        return _blok("Transpoz", _latex(M) + "^T", _latex(M.T)), "transpoz"
    return _blok("Determinant", f"\\det {_latex(M)}", _latex(M.det())), "determinant"


def _istatistik(t: str):
    m = re.search(r"(?i)(ortalama|aritmetik ortalama|medyan|ortanca|tepe değer|varyans|standart sapma|std|açıklık|ranj|istatistik|\bmod(?:u|unu)?\b)", t)
    if not m:
        return None
    if re.search(r"(?i)^\s*\d+\s*mod\s*\d+\s*$|kalan", t):
        return None
    sayilar = [float(s.replace(",", ".")) for s in re.findall(r"-?\d+(?:[.,]\d+)?", re.sub(r"(?<=\d),(?=\d{3}\b)", "", t))]
    sayilar = [float(s) for s in re.findall(r"-?\d+(?:\.\d+)?", re.sub(r"(\d),(\d)", r"\1.\2", re.sub(r",\s+", " ", t)))]
    if len(sayilar) < 2:
        return None
    fmt = lambda v: f"{v:.6g}".replace(".", ",")
    tablo = [
        ("Veri sayısı", str(len(sayilar))), ("Toplam", fmt(sum(sayilar))), ("Aritmetik ortalama", fmt(statistics.mean(sayilar))),
        ("Medyan (ortanca)", fmt(statistics.median(sayilar))),
        ("Mod (tepe değer)", ", ".join(fmt(v) for v in statistics.multimode(sayilar)) if len(set(sayilar)) < len(sayilar) else "yok (tüm değerler farklı)"),
        ("Açıklık (ranj)", fmt(max(sayilar) - min(sayilar))), ("Varyans (örneklem)", fmt(statistics.variance(sayilar))),
        ("Standart sapma (örneklem)", fmt(statistics.stdev(sayilar))), ("Standart sapma (kitle)", fmt(statistics.pstdev(sayilar))),
    ]
    return ("### 📊 İstatistik\n\n**Veri:** " + ", ".join(fmt(s) for s in sayilar) + "\n\n| Ölçü | Değer |\n|---|---|\n" +
            "\n".join(f"| {a} | **{v}** |" for a, v in tablo)), "istatistik"


def _sayilar_kuram(t: str):
    tl = t.lower()
    m = re.search(r"(?i)(?:c|kombinasyon)\s*\(\s*(\d+)\s*[,;]\s*(\d+)\s*\)|(\d+)\s*'?(?:in|ın|un|ün|nin|nın)?\s*(\d+)\s*'?(?:li|lı|lu|lü)\s*kombinasyonu", t)
    if m:
        n_, r_ = int(m.group(1) or m.group(3)), int(m.group(2) or m.group(4))
        return _blok("Kombinasyon", f"C({n_},{r_}) = \\binom{{{n_}}}{{{r_}}} = \\frac{{{n_}!}}{{{r_}!\\,({n_}-{r_})!}}", _latex(sp.binomial(n_, r_))), "kombinasyon"
    m = re.search(r"(?i)(?:p|permütasyon)\s*\(\s*(\d+)\s*[,;]\s*(\d+)\s*\)|(\d+)\s*'?(?:in|ın|un|ün|nin|nın)?\s*(\d+)\s*'?(?:li|lı|lu|lü)\s*permütasyonu", t)
    if m:
        n_, r_ = int(m.group(1) or m.group(3)), int(m.group(2) or m.group(4))
        return _blok("Permütasyon", f"P({n_},{r_}) = \\frac{{{n_}!}}{{({n_}-{r_})!}}", _latex(sp.ff(n_, r_))), "permütasyon"
    m = re.search(r"(?i)(obeb|ebob|ebeb|gcd|okek|ekok|lcm)\D*((?:\d+\D+){1,}\d+)", tl)
    if m:
        sayilar = [int(s) for s in re.findall(r"\d+", m.group(2))]
        if m.group(1) in ("obeb", "ebob", "ebeb", "gcd"):
            return _blok("OBEB (EBOB)", "\\gcd(" + ", ".join(map(str, sayilar)) + ")", str(sp.gcd_list(sayilar))), "obeb"
        return _blok("OKEK (EKOK)", "\\mathrm{lcm}(" + ", ".join(map(str, sayilar)) + ")", str(sp.lcm_list(sayilar))), "okek"
    m = re.search(r"(?i)(\d+)\s*(?:mod|modülo|'?(?:un|ün|in|ın)\s*(\d+)\s*ile bölümünden kalan)\s*(\d+)?", tl)
    if m and ("mod" in tl or "kalan" in tl):
        a_ = int(m.group(1))
        b_ = int(m.group(3) or m.group(2) or 0)
        if b_:
            return _blok("Mod Alma", f"{a_} \\bmod {b_}", str(a_ % b_)), "mod"
    return None


_ISLEMLER = (_matris, _sayilar_kuram, _istatistik, _turev, _integral, _limit, _seri, _cebir, _esitsizlik, _denklem)
_ILERI_ANAHTAR = re.compile(
    r"(?i)türev|integral|∫|limit|\blim\b|taylor|maclaurin|seri|çarpan|sadeleştir|genişlet|açılım|\baç\b|kesirlere|"
    r"matris|determinant|\bdet\b|özdeğer|ortalama|medyan|ortanca|varyans|standart sapma|\bmod\b|açıklık|kombinasyon|"
    r"permütasyon|obeb|ebob|okek|ekok|kalan|\bc\(|\bp\(|eşitsizli|[<>]|=")


def ileri_matematik_coz(metin: str, aciklama: bool = False):
    """İleri matematik isteği ise (cevap, etiket), değilse (None, None)."""
    if not _HAZIR or not metin or not _ILERI_ANAHTAR.search(metin):
        return None, None
    t = metin.strip()
    if re.search(r"(?i)grafi|çiz|ciz|plot|görselleştir", t):  # grafik isteği → Modül 17 grafik çizicisi
        return None, None
    # Matematiksel olmayan cümleleri ele (ör. "ortalama bir gün", "mod değiştir")
    if not re.search(r"[0-9x-z\[\]^²³√π]", t):
        return None, None
    # Sıradan cümleleri ele: matematik dışı kelime sayısı fazlaysa (ör. "a=b mi sence bu iş olur mu") dokunma
    kelimeler = re.findall(r"[a-zçğıöşü]{3,}", t.lower())
    bilinen = set(_ILERI_ANAHTAR.pattern.replace("(?i)", "").replace("\\b", "").split("|")) | {
        "sin", "cos", "tan", "cot", "log", "sqrt", "exp", "abs", "çöz", "bul", "hesapla", "denklem", "denklemini",
        "sistemini", "kaçtır", "nedir", "için", "kadar", "ile", "bölümünden", "türevi", "türevini", "integrali",
        "limiti", "mertebe", "mertebeden", "matris", "ters", "kümesi", "çözüm", "ayır", "adım", "açıkla", "nasıl",
        "belirli", "belirsiz", "giderken", "sağdan", "soldan", "yaklaşırken", "değer", "veri", "sayıların", "nin", "nın"}
    if sum(1 for w in kelimeler if w not in bilinen) > 4:
        return None, None
    for fn in _ISLEMLER:
        try:
            sonuc = fn(t)
        except Exception:
            sonuc = None
        if sonuc:
            cevap, ozet = sonuc
            if aciklama:
                cevap += _adim_adim(t, ozet)
            return cevap, "🧮 İleri Matematik (SymPy)"
    return None, None


def _adim_adim(soru: str, dogrulanmis: str) -> str:
    """Yapay zekâya YALNIZCA doğrulanmış sonucu açıklatır (sonucu değiştirmesi yasak)."""
    try:
        import modul_25_ai_cekirdek as ai
        metin, _ = ai.sohbet_tamamla(
            [{"role": "user", "content": f"Soru: {soru}\nDOĞRULANMIŞ SONUÇ (SymPy): {dogrulanmis}\n"
                                         "Bu sonuca nasıl ulaşıldığını 9. sınıf öğrencisinin anlayacağı şekilde, kısa ve "
                                         "numaralı adımlarla Türkçe açıkla. Sonucu DEĞİŞTİRME, yeni sonuç üretme. LaTeX için $...$ kullan."}],
            sistem="Sen sabırlı bir matematik öğretmenisin. Yalnızca verilen doğrulanmış sonucu açıklarsın.",
            sicaklik=0.2, maks_token=900)
        return f"\n\n---\n#### 📝 Adım adım\n{metin}" if metin else ""
    except Exception:
        return ""
