# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 14: PROFESYONEL MATEMATİK ÇEKİRDEĞİ (modul_14_pro_matematik.py)
==============================================================================
Modül 4'teki matematik motorunun önüne takılan, kalıp (regex) yerine gerçek
bir ifade ayrıştırıcısı (recursive-descent parser) kullanan çekirdek:

  • Doğru işlem önceliği:  2+3*4 = 14,  -3^2 = -9,  2^3^2 = 512
  • Parantez ve gizli çarpma:  2(3+4), (1+2)(3-1), 3π
  • Tam kesirli sonuç:  10/4 = 5/2 = 2,5   (0,1+0,2 = 0,3 — kayan nokta hatası yok)
  • Fonksiyonlar: sin/cos/tan/cot (derece), arcsin/arccos/arctan, log, ln,
    √ / karekök, küpkök, mutlak, faktöriyel (!), yüzde (%)
  • Türkçe sözel işlemler: "12 artı 5 çarpı 3", "2 üzeri 10", "100 bölü 8 kaç eder"
  • Denklem çözücü (x'e göre 1. ve 2. derece, her biçimde):
        3(x-2) = x+4,   x^2 = 9,   2x² + 3x - 2 = 0,   x^2 + x + 1 = 0 (karmaşık kök)
  • Asal çarpanlar, asallık testi, yüzde artış/azalış/indirim, "yüzde kaçı"

Dışarıya açılan tek giriş noktası: pro_matematik_coz(metin) -> (cevap, etiket) | (None, None)
"""

import math
import re
from fractions import Fraction

__all__ = ["pro_matematik_coz", "ifade_hesapla", "denklem_coz", "sayi_yaz"]

# ------------------------------------------------------------------------------
# Biçimlendirme
# ------------------------------------------------------------------------------
_UST_SINIR_BIT = 4000  # ~1200 basamaklı sayılara kadar izin ver (donmayı önler)


def _tr_sayi(x: float, basamak: int = 10) -> str:
    """Türkçe sayı yazımı: binlik '.', ondalık ','."""
    if isinstance(x, int):
        return f"{x:,}".replace(",", ".")
    if math.isinf(x) or math.isnan(x):
        return "tanımsız"
    if x != 0 and (abs(x) >= 1e15 or abs(x) < 1e-6):
        return f"{x:.{basamak}g}".replace(".", ",")
    yuvarlak = round(x, basamak)
    if yuvarlak == int(yuvarlak):
        return _tr_sayi(int(yuvarlak))
    s = f"{yuvarlak:,.{basamak}f}".rstrip("0").rstrip(".")
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def sayi_yaz(deger) -> str:
    """Fraction / int / float değeri okunaklı yazar (kesirse ondalığını da gösterir)."""
    if isinstance(deger, complex):
        r, i = _tr_sayi(deger.real, 6), _tr_sayi(abs(deger.imag), 6)
        return f"{r} {'+' if deger.imag >= 0 else '−'} {i}i"
    if isinstance(deger, Koklu):
        return f"{deger.yaz()} ≈ {_tr_sayi(float(deger))}"
    if isinstance(deger, Fraction):
        if deger.denominator == 1:
            return _tr_sayi(deger.numerator)
        kesir = f"{deger.numerator}/{deger.denominator}"
        return f"{kesir} ≈ {_tr_sayi(float(deger))}" if len(kesir) <= 24 else _tr_sayi(float(deger))
    if isinstance(deger, float):
        # Trigonometri gibi işlemlerden gelen 0,49999999999 tarzı artıkları temizle
        yuvarlak = round(deger, 12)
        if yuvarlak == int(yuvarlak) and abs(yuvarlak) < 1e15:
            return _tr_sayi(int(yuvarlak))
        return _tr_sayi(yuvarlak)
    return _tr_sayi(deger)


# ------------------------------------------------------------------------------
# Türkçe metni matematik ifadesine çevirme
# ------------------------------------------------------------------------------
_SOZEL = [
    (r"\bart[ıi]\b", "+"),
    (r"\bek[sş]i\b", "-"),
    (r"\b(?:çarp[ıi]|carpi|kere|defa)\b", "*"),
    (r"\b(?:böl[üu]|bolu)\b", "/"),
    (r"\b(?:üzeri|uzeri|üssü|ussu)\b", "^"),
    (r"\bkare\s*k[öo]k[üu]?\b", "√"),
    (r"\bk[üu]p\s*k[öo]k[üu]?\b", "kupkok"),
    (r"\bmutlak\s*de[ğg]er(?:i)?\b", "abs"),
    (r"\bmutlak\b", "abs"),
    (r"\bfakt[öo]riyel(?:i)?\b", "!"),
    (r"\bpi\b", "π"),
]
# Soru kalıplarını temizle: "... kaç eder?", "hesapla: ...", "sonucu nedir"
_GURULTU = re.compile(
    r"(?:\bhesapla(?:r m[ıi]s[ıi]n|y[ıi]n|)\b|\bsonucu?\b|\bka[çc]\s*(?:eder|olur|yapar)?\b|\bnedir\b|"
    r"\bne(?:dir)?\s*(?:eder|olur)\b|\beder\b|\bolur\b|\bişlemi\b|\bislemi\b|\bçöz(?:ün|)?\b|\bcoz\b|"
    r"\bdenklemi(?:ni)?\b|\bbul\b|\bl[üu]tfen\b|[?:]$)"
)

_FONKSIYONLAR = {
    "sin": lambda v: math.sin(math.radians(v)),
    "cos": lambda v: math.cos(math.radians(v)),
    "tan": lambda v: math.tan(math.radians(v)),
    "tg": lambda v: math.tan(math.radians(v)),
    "cot": lambda v: 1 / math.tan(math.radians(v)),
    "cotg": lambda v: 1 / math.tan(math.radians(v)),
    "arcsin": lambda v: math.degrees(math.asin(v)),
    "asin": lambda v: math.degrees(math.asin(v)),
    "arccos": lambda v: math.degrees(math.acos(v)),
    "acos": lambda v: math.degrees(math.acos(v)),
    "arctan": lambda v: math.degrees(math.atan(v)),
    "atan": lambda v: math.degrees(math.atan(v)),
    "log": lambda v: math.log10(v),
    "ln": lambda v: math.log(v),
    "sqrt": None,  # özel (tam kök korunur)
    "kok": None,
    "kök": None,
    "kupkok": lambda v: math.copysign(abs(v) ** (1 / 3), v),
    "abs": None,  # özel (kesir korunur)
}

# Trigonometri için tam değerler (derece): sin 30 = 1/2 gibi
_TAM_TRIG = {
    ("sin", 0): Fraction(0), ("sin", 30): Fraction(1, 2), ("sin", 90): Fraction(1),
    ("sin", 150): Fraction(1, 2), ("sin", 180): Fraction(0), ("sin", 270): Fraction(-1),
    ("sin", 210): Fraction(-1, 2), ("sin", 330): Fraction(-1, 2), ("sin", 360): Fraction(0),
    ("cos", 0): Fraction(1), ("cos", 60): Fraction(1, 2), ("cos", 90): Fraction(0),
    ("cos", 120): Fraction(-1, 2), ("cos", 180): Fraction(-1), ("cos", 240): Fraction(-1, 2),
    ("cos", 270): Fraction(0), ("cos", 300): Fraction(1, 2), ("cos", 360): Fraction(1),
    ("tan", 0): Fraction(0), ("tan", 45): Fraction(1), ("tan", 135): Fraction(-1),
    ("tan", 180): Fraction(0), ("tan", 225): Fraction(1), ("tan", 315): Fraction(-1),
    ("tg", 45): Fraction(1), ("cot", 45): Fraction(1), ("cotg", 45): Fraction(1),
}


class MatHata(ValueError):
    """Kullanıcıya gösterilebilir matematik hatası (tanımsız işlem vb.)."""


class SozdizimHatasi(MatHata):
    """Metin geçerli bir matematik ifadesi değil → başka motorlara bırakılır."""


# ------------------------------------------------------------------------------
# Tam köklü sayılar: a + b√2 + c√3 ... biçiminde sembolik hesap (√27 + √3 = 4√3)
# ------------------------------------------------------------------------------
def _karesiz(n: int):
    """n = d² · r  (r karesiz) → (d, r)"""
    d, r, k = 1, n, 2
    while k * k <= r:
        while r % (k * k) == 0:
            d *= k
            r //= k * k
        k += 1
    return d, r


class Koklu:
    """Σ katsayı·√kök  (kök karesiz tam sayı, kök=1 rasyonel kısım)."""

    __slots__ = ("t",)

    def __init__(self, terimler):
        self.t = {r: c for r, c in terimler.items() if c != 0}

    @staticmethod
    def sadele(terimler):
        k = Koklu(terimler)
        if not k.t:
            return Fraction(0)
        if set(k.t) == {1}:
            return k.t[1]
        return k

    @staticmethod
    def _al(v):
        if isinstance(v, Koklu):
            return v.t
        if isinstance(v, (int, Fraction)):
            return {1: Fraction(v)}
        return None

    def __float__(self):
        return float(sum(float(c) * math.sqrt(r) for r, c in self.t.items()))

    def __add__(self, o):
        ot = Koklu._al(o)
        if ot is None:
            return float(self) + o
        yeni = dict(self.t)
        for r, c in ot.items():
            yeni[r] = yeni.get(r, Fraction(0)) + c
        return Koklu.sadele(yeni)

    __radd__ = __add__

    def __neg__(self):
        return Koklu({r: -c for r, c in self.t.items()})

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        ot = Koklu._al(o)
        if ot is None:
            return float(self) * o
        yeni = {}
        for r1, c1 in self.t.items():
            for r2, c2 in ot.items():
                d, r = _karesiz(r1 * r2)
                yeni[r] = yeni.get(r, Fraction(0)) + c1 * c2 * d
        return Koklu.sadele(yeni)

    __rmul__ = __mul__

    def _ters(self):
        # Tek terimli: 1/(c√r) = √r/(c·r)  (paydayı rasyonelleştir)
        if len(self.t) == 1:
            (r, c), = self.t.items()
            return Koklu({r: 1 / (c * r)})
        # İki terimli a + b√r: eşleniği ile çarp → (a − b√r)/(a² − b²r)
        if len(self.t) == 2 and 1 in self.t:
            a = self.t[1]
            (r, b), = [(r, c) for r, c in self.t.items() if r != 1]
            payda = a * a - b * b * r
            if payda != 0:
                return Koklu({1: a / payda, r: -b / payda})
        return None

    def __truediv__(self, o):
        ot = Koklu._al(o)
        if ot is None:
            return float(self) / o
        if isinstance(o, Koklu):
            ters = o._ters()
            return self * ters if ters is not None else float(self) / float(o)
        if o == 0:
            raise MatHata("Sıfıra bölme tanımsızdır")
        return Koklu.sadele({r: c / Fraction(o) for r, c in self.t.items()})

    def __rtruediv__(self, o):
        ters = self._ters()
        if ters is None:
            return o / float(self)
        return ters * o

    def __eq__(self, o):
        ot = Koklu._al(o)
        return ot is not None and Koklu(ot).t == self.t

    def __hash__(self):
        return hash(tuple(sorted(self.t.items())))

    def __lt__(self, o):
        return float(self) < float(o)

    def __le__(self, o):
        return float(self) <= float(o)

    def __gt__(self, o):
        return float(self) > float(o)

    def __ge__(self, o):
        return float(self) >= float(o)

    def __abs__(self):
        return -self if float(self) < 0 else self

    def yaz(self):
        parcalar = []
        for r in sorted(self.t):
            c = self.t[r]
            isaret = "−" if c < 0 else "+"
            m = abs(c)
            if r == 1:
                govde = f"{m.numerator}/{m.denominator}" if m.denominator != 1 else str(m.numerator)
            else:
                pay = "" if m.numerator == 1 else str(m.numerator)
                govde = f"{pay}√{r}" + (f"/{m.denominator}" if m.denominator != 1 else "")
            parcalar.append((isaret, govde))
        metin = ("−" if parcalar[0][0] == "−" else "") + parcalar[0][1]
        for isaret, govde in parcalar[1:]:
            metin += f" {isaret} {govde}"
        return metin


def _normalize(metin: str, denklem: bool) -> str:
    s = metin.replace("İ", "i").replace("I", "ı").lower().replace("̇", "")
    s = (s.replace("×", "*").replace("·", "*").replace("÷", "/").replace("−", "-")
           .replace("–", "-").replace("²", "^2").replace("³", "^3").replace("**", "^")
           .replace("√", " √ ").replace("π", " π "))
    for desen, yerine in _SOZEL:
        s = re.sub(desen, f" {yerine} ", s)
    s = _GURULTU.sub(" ", s)
    if not denklem:
        # "5 x 6" → 5 * 6 (denklem değilse x çarpmadır)
        s = re.sub(r"(?<=[\d)])\s*x\s*(?=[\d(])", " * ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.rstrip("?:.").strip() if denklem else s.rstrip("=?:.").strip()


# ------------------------------------------------------------------------------
# Sözcük ayırıcı (tokenizer)
# ------------------------------------------------------------------------------
_TOKEN = re.compile(r"\s*(?:(\d+(?:[.,]\d+)?)|([a-zçğıöşü]+)|(√|π|[-+*/^()!%=]))")


def _tokenlara_ayir(s: str):
    tokenlar, i = [], 0
    while i < len(s):
        m = _TOKEN.match(s, i)
        if not m or m.end() == i:
            if s[i:].strip() == "":
                break
            raise SozdizimHatasi(f"Tanınmayan karakter: '{s[i]}'")
        sayi, ad, op = m.groups()
        if sayi is not None:
            tokenlar.append(("sayi", Fraction(sayi.replace(",", "."))))
        elif ad is not None:
            if ad in _FONKSIYONLAR:
                tokenlar.append(("fonk", ad))
            elif ad in ("x",):
                tokenlar.append(("deg", ad))
            elif ad == "e":
                tokenlar.append(("sabit", "e"))
            else:
                raise SozdizimHatasi(f"Bilinmeyen sözcük: '{ad}'")
        else:
            tokenlar.append(("sabit", "π") if op == "π" else ("op", op))
        i = m.end()
    return tokenlar


# ------------------------------------------------------------------------------
# Ayrıştırıcı + değerlendirici
#   ifade  := terim (('+'|'-') terim)*
#   terim  := tekli (('*'|'/'|gizli çarpma) tekli)*
#   tekli  := ('-'|'+') tekli | us
#   us     := sonek ('^' tekli)?            (sağdan birleşir: 2^3^2 = 2^9)
#   sonek  := temel ('!' | '%')*
#   temel  := sayı | sabit | x | '(' ifade ')' | fonk tekli | '√' tekli
# ------------------------------------------------------------------------------
def _float_mi(v):
    return isinstance(v, float)


def _tamsayi_mi(v):
    return isinstance(v, Fraction) and v.denominator == 1


class _Ayristirici:
    def __init__(self, tokenlar, x_degeri=None):
        self.t = tokenlar
        self.i = 0
        self.x = x_degeri

    def bak(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def al(self):
        tok = self.bak()
        self.i += 1
        return tok

    def calistir(self):
        if not self.t:
            raise SozdizimHatasi("Boş ifade")
        v = self.ifade()
        if self.i != len(self.t):
            raise SozdizimHatasi(f"Beklenmeyen ifade: '{self.bak()[1]}'")
        return v

    def ifade(self):
        v = self.terim()
        while self.bak() in (("op", "+"), ("op", "-")):
            op = self.al()[1]
            sag = self.terim()
            v = v + sag if op == "+" else v - sag
        return v

    def _temel_baslar_mi(self):
        tur, deger = self.bak()
        return tur in ("sayi", "sabit", "deg", "fonk") or (tur == "op" and deger in ("(", "√"))

    def terim(self):
        v = self.tekli()
        while True:
            tok = self.bak()
            if tok in (("op", "*"), ("op", "/")):
                op = self.al()[1]
                sag = self.tekli()
                if op == "*":
                    v = v * sag
                else:
                    if sag == 0:
                        raise MatHata("Sıfıra bölme tanımsızdır")
                    v = v / sag
            elif self._temel_baslar_mi():  # gizli çarpma: 2x, 2(3+4), 3π
                v = v * self.tekli()
            else:
                return v

    def tekli(self):
        if self.bak() == ("op", "-"):
            self.al()
            return -self.tekli()
        if self.bak() == ("op", "+"):
            self.al()
            return self.tekli()
        return self.us()

    def us(self):
        taban = self.sonek()
        if self.bak() == ("op", "^"):
            self.al()
            ust = self.tekli()
            return _us_al(taban, ust)
        return taban

    def sonek(self):
        v = self.temel()
        while self.bak() in (("op", "!"), ("op", "%")):
            op = self.al()[1]
            if op == "!":
                if not _tamsayi_mi(v) or v < 0:
                    raise MatHata("Faktöriyel yalnızca doğal sayılar için tanımlıdır")
                if v > 1000:
                    raise MatHata("Faktöriyel için sayı çok büyük (en fazla 1000!)")
                v = Fraction(math.factorial(int(v)))
            else:
                v = v / 100
        return v

    def temel(self):
        tur, deger = self.al()
        if tur == "sayi":
            return deger
        if tur == "sabit":
            return math.pi if deger == "π" else math.e
        if tur == "deg":
            if self.x is None:
                raise MatHata("Bilinmeyen içeren ifade")
            return self.x
        if tur == "op" and deger == "(":
            v = self.ifade()
            if self.al() != ("op", ")"):
                raise SozdizimHatasi("Kapanmamış parantez")
            return v
        if tur == "op" and deger == "√":
            return _karekok(self.tekli_arg())
        if tur == "fonk":
            arg = self.tekli_arg()
            return _fonksiyon(deger, arg)
        raise SozdizimHatasi("Eksik ya da hatalı ifade")

    def tekli_arg(self):
        """Fonksiyon argümanı: sin 30, sin(30), √2x → √2 · x değil √(2)·x olacak şekilde."""
        if self.bak() == ("op", "-"):
            self.al()
            return -self.tekli_arg()
        return self.us()


def _us_al(taban, ust):
    if isinstance(taban, Koklu):
        if _tamsayi_mi(ust) and abs(int(ust)) <= 64:
            n, sonuc = int(ust), Fraction(1)
            for _ in range(abs(n)):
                sonuc = sonuc * taban
            return sonuc if n >= 0 else 1 / sonuc
        taban = float(taban)
    if isinstance(taban, Fraction) and _tamsayi_mi(ust):
        n = int(ust)
        if taban == 0 and n < 0:
            raise MatHata("0'ın negatif kuvveti tanımsızdır")
        bit = max(taban.numerator.bit_length(), taban.denominator.bit_length())
        if bit * abs(n) > _UST_SINIR_BIT * 4:
            raise MatHata("Sonuç çok büyük (üs sınırı aşıldı)")
        return taban ** n
    if isinstance(taban, Fraction) and isinstance(ust, Fraction) and taban >= 0:
        # Tam kök kontrolü: 8^(1/3) = 2, 16^(1/2) = 4
        kok_derece = ust.denominator
        if kok_derece <= 10:
            for parca in (taban.numerator, taban.denominator):
                r = round(parca ** (1 / kok_derece))
                if r ** kok_derece != parca:
                    break
            else:
                pay = round(taban.numerator ** (1 / kok_derece))
                payda = round(taban.denominator ** (1 / kok_derece))
                return _us_al(Fraction(pay, payda), Fraction(ust.numerator))
    tf, uf = float(taban), float(ust)
    if tf < 0 and not float(uf).is_integer():
        raise MatHata("Negatif sayının kesirli kuvveti reel sayı değildir")
    try:
        return tf ** uf
    except OverflowError:
        raise MatHata("Sonuç çok büyük")


def _karekok(v):
    if v < 0:
        raise MatHata("Negatif sayının karekökü reel sayı değildir")
    if isinstance(v, Fraction):
        p, q = math.isqrt(v.numerator), math.isqrt(v.denominator)
        if p * p == v.numerator and q * q == v.denominator:
            return Fraction(p, q)
        if v.numerator < 10 ** 12 and v.denominator < 10 ** 12:
            # √(p/q) = √(p·q)/q  →  d√r / q
            d, r = _karesiz(v.numerator * v.denominator)
            return Koklu({r: Fraction(d, v.denominator)})
    return math.sqrt(float(v))


def _koklu_trig(ad, derece):
    """30-45-60 katlarının köklü tam değerleri: sin 45 = √2/2, tan 60 = √3 ..."""
    yari = Fraction(1, 2)
    temel = {  # 0-90 arası referans açılar → (sin, cos)
        30: (Fraction(1, 2), Koklu({3: yari})),
        45: (Koklu({2: yari}), Koklu({2: yari})),
        60: (Koklu({3: yari}), Fraction(1, 2)),
    }
    for ref, (sn, cs) in temel.items():
        for bolge, (s_isaret, c_isaret, ters) in {0: (1, 1, False), 1: (1, -1, True), 2: (-1, -1, False), 3: (-1, 1, True)}.items():
            aci = (bolge * 90 + (90 - ref if ters else ref)) % 360
            if aci != derece:
                continue
            sin_v, cos_v = s_isaret * sn, c_isaret * cs
            if ad == "sin":
                return sin_v
            if ad == "cos":
                return cos_v
            if ad in ("tan", "tg"):
                return sin_v / cos_v
            if ad in ("cot", "cotg"):
                return cos_v / sin_v
    return None


def _fonksiyon(ad, arg):
    if ad in ("sqrt", "kok", "kök"):
        return _karekok(arg)
    if ad == "abs":
        return abs(arg)
    if isinstance(arg, Koklu):
        arg = float(arg)
    if isinstance(arg, Fraction) and _tamsayi_mi(arg):
        derece = int(arg) % 360
        if (ad, derece) in _TAM_TRIG:
            return _TAM_TRIG[(ad, derece)]
        kok_deger = _koklu_trig(ad, derece)
        if kok_deger is not None:
            return kok_deger
        if ad in ("tan", "tg") and derece in (90, 270):
            raise MatHata(f"tan {derece}° tanımsızdır")
        if ad in ("cot", "cotg") and derece in (0, 180):
            raise MatHata(f"cot {derece}° tanımsızdır")
        if ad == "log" and arg > 0:
            n = int(arg)
            us = round(math.log10(n))
            if 10 ** us == n:
                return Fraction(us)
    if ad in ("log", "ln") and arg <= 0:
        raise MatHata("Logaritma yalnızca pozitif sayılar için tanımlıdır")
    if ad in ("arcsin", "asin", "arccos", "acos") and not -1 <= arg <= 1:
        raise MatHata("arcsin/arccos için değer -1 ile 1 arasında olmalı")
    try:
        return _FONKSIYONLAR[ad](float(arg))
    except (ValueError, ZeroDivisionError, OverflowError):
        raise MatHata(f"{ad} bu değer için tanımsız")


def ifade_hesapla(metin: str):
    """Saf bir matematik ifadesini hesaplar. Hata durumunda MatHata fırlatır."""
    return _Ayristirici(_tokenlara_ayir(_normalize(metin, denklem=False))).calistir()


# ------------------------------------------------------------------------------
# Denklem çözücü (x'e göre en fazla 2. derece)
# ------------------------------------------------------------------------------
def _kok_sadelestir(n: int):
    disari, iceri, k = 1, n, 2
    while k * k <= iceri:
        while iceri % (k * k) == 0:
            disari *= k
            iceri //= k * k
        k += 1
    return disari, iceri


def denklem_coz(metin: str):
    """'sol = sağ' biçimindeki denklemi çözer → (adımlar_metni, etiket)."""
    s = _normalize(metin, denklem=True)
    if s.count("=") != 1:
        raise MatHata("Denklemde tek bir '=' olmalı")
    sol, sag = s.split("=")
    t_sol, t_sag = _tokenlara_ayir(sol), _tokenlara_ayir(sag)
    if ("deg", "x") not in t_sol + t_sag:
        raise MatHata("Denklemde x bilinmeyeni yok")

    def f(x):
        return _Ayristirici(t_sol, x).calistir() - _Ayristirici(t_sag, x).calistir()

    try:
        f0, f1, fm1 = f(Fraction(0)), f(Fraction(1)), f(Fraction(-1))
    except MatHata:
        raise MatHata("Bu denklem polinom biçiminde değil")
    if any(not isinstance(v, Fraction) for v in (f0, f1, fm1)):
        raise MatHata("Denklemde ondalık fonksiyon var, sayısal çözüm desteklenmiyor")
    c = f0
    a = (f1 + fm1) / 2 - c
    b = (f1 - fm1) / 2
    # Doğrulama: gerçekten ≤ 2. derece mi?
    for deneme in (2, 3, -2, Fraction(1, 2)):
        try:
            if f(Fraction(deneme)) != a * deneme * deneme + b * deneme + c:
                raise MatHata("Bu çözücü en fazla 2. derece denklemleri çözer")
        except ZeroDivisionError:
            raise MatHata("Bu denklem polinom biçiminde değil")

    def yaz(v):
        return sayi_yaz(v).split(" ≈")[0]

    def yazp(v):  # bölme adımında kesirleri parantez içine al
        y = yaz(v)
        return f"({y})" if "/" in y or y.startswith("-") else y

    baslik = f"📐 **Denklem Çözümü:** `{metin.strip()}`\n"
    if a == 0:
        if b == 0:
            if c == 0:
                return baslik + "Her iki taraf her x için eşit → **sonsuz çözüm** (özdeşlik).", "Denklem: Özdeşlik"
            return baslik + f"Sadeleşince `{yaz(c)} = 0` çıkıyor → **çözüm yok** (Ç = ∅).", "Denklem: Çözümsüz"
        x = -c / b
        adim = (f"1. Adım (Düzenle): `{yaz(b)}x {'+' if c >= 0 else '−'} {yaz(abs(c))} = 0`\n"
                f"2. Adım: `{yaz(b)}x = {yaz(-c)}`\n"
                f"3. Adım: `x = {yazp(-c)} / {yazp(b)}` → **`x = {sayi_yaz(x)}`**")
        return baslik + adim, "Denklem: 1. Derece"

    delta = b * b - 4 * a * c
    a_yazi = "" if a == 1 else ("−" if a == -1 else yaz(a))
    adim = (f"1. Adım (Standart biçim): `{a_yazi}x² {'+' if b >= 0 else '−'} {yaz(abs(b))}x "
            f"{'+' if c >= 0 else '−'} {yaz(abs(c))} = 0`  →  `a = {yaz(a)}, b = {yaz(b)}, c = {yaz(c)}`\n"
            f"2. Adım (Diskriminant): `Δ = b² − 4ac = {yaz(delta)}`\n")
    if delta == 0:
        x0 = -b / (2 * a)
        return baslik + adim + f"3. Adım: `Δ = 0` → çift katlı kök: **`x₁ = x₂ = {sayi_yaz(x0)}`**", "Denklem: 2. Derece"
    if delta > 0:
        p, q = math.isqrt(delta.numerator), math.isqrt(delta.denominator)
        if p * p == delta.numerator and q * q == delta.denominator:
            kd = Fraction(p, q)
            x1, x2 = (-b + kd) / (2 * a), (-b - kd) / (2 * a)
            return (baslik + adim + f"3. Adım: `x = (−b ± √Δ) / 2a`  →  **`x₁ = {sayi_yaz(x1)}`**, **`x₂ = {sayi_yaz(x2)}`**\n"
                    f"Çözüm kümesi: **Ç = {{{yaz(min(x1, x2))}, {yaz(max(x1, x2))}}}**"), "Denklem: 2. Derece"
        kd = math.sqrt(float(delta))
        x1, x2 = (-float(b) + kd) / (2 * float(a)), (-float(b) - kd) / (2 * float(a))
        kok_yazi = f"√{yaz(delta)}"
        if _tamsayi_mi(delta):
            d, i = _kok_sadelestir(int(delta))
            kok_yazi = f"{d}√{i}" if d > 1 else f"√{i}"
        return (baslik + adim + f"3. Adım: `x = ({yaz(-b)} ± {kok_yazi}) / {yaz(2 * a)}`\n"
                f"**`x₁ ≈ {sayi_yaz(x1)}`**, **`x₂ ≈ {sayi_yaz(x2)}`** (irrasyonel kökler)"), "Denklem: 2. Derece"
    re_k = -float(b) / (2 * float(a))
    im_k = math.sqrt(-float(delta)) / (2 * abs(float(a)))
    return (baslik + adim + f"3. Adım: `Δ < 0` → **reel kök yoktur**. Karmaşık kökler: "
            f"**`x = {sayi_yaz(re_k)} ± {sayi_yaz(im_k)}i`**"), "Denklem: 2. Derece (karmaşık)"


# ------------------------------------------------------------------------------
# Özel Türkçe kalıplar: asal çarpan, asallık, yüzde artış/azalış, "yüzde kaçı"
# ------------------------------------------------------------------------------
_SAYI = r"(\d+(?:[.,]\d+)?)"
_EK = r"(?:'?\s*(?:[iıuü]n|n[iıuü]n|[ae]|y[ae]|d[ae]|t[ae]|[iıuü]|y[iıuü]|s[iıuü]))?"


def _f(s):
    return Fraction(s.replace(",", "."))


def _asal_mi(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    k = 3
    while k * k <= n:
        if n % k == 0:
            return False
        k += 2
    return True


def _asal_carpanlar(n: int):
    sonuc, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            sonuc[d] = sonuc.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        sonuc[n] = sonuc.get(n, 0) + 1
    return sonuc


_UST_RAKAM = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _ozel_kaliplar(t: str):
    # Asal çarpanlar
    m = re.search(r"(\d+)\D{0,12}asal\s*çarpan", t) or re.search(r"asal\s*çarpan\w*\D{0,12}(\d+)", t)
    if m:
        n = int(m.group(1))
        if n < 2:
            return f"🔢 `{n}` sayısının asal çarpanı yoktur (asal çarpanlar 2 ve üzeri sayılar için tanımlıdır).", "Asal Çarpanlar"
        if n > 10 ** 14:
            return "🔢 Sayı çok büyük (en fazla 15 basamak).", "Asal Çarpanlar"
        c = _asal_carpanlar(n)
        yazi = " · ".join(f"{p}{str(k).translate(_UST_RAKAM) if k > 1 else ''}" for p, k in c.items())
        bolen_sayisi = math.prod(k + 1 for k in c.values())
        return (f"🔢 **Asal Çarpanlara Ayırma:** `{_tr_sayi(n)} = {yazi}`\n"
                f"• Asal çarpanlar: **{', '.join(map(str, c))}**\n"
                f"• Pozitif bölen sayısı: `{' · '.join(f'({k}+1)' for k in c.values())}` = **{bolen_sayisi}**"), "Asal Çarpanlar"

    # Asal mı?
    m = re.search(r"(\d+)\D{0,6}asal\s*(?:say[ıi]\s*)?m[ıi]", t)
    if m:
        n = int(m.group(1))
        if n > 10 ** 14:
            return "🔢 Sayı çok büyük (en fazla 15 basamak).", "Asallık Testi"
        if _asal_mi(n):
            return f"✅ **{_tr_sayi(n)} asal sayıdır** (yalnızca 1'e ve kendisine bölünür).", "Asallık Testi"
        if n < 2:
            return f"❌ **{n} asal değildir** (asal sayılar 2'den başlar).", "Asallık Testi"
        c = _asal_carpanlar(n)
        en_kucuk = min(c)
        return (f"❌ **{_tr_sayi(n)} asal değildir**: `{_tr_sayi(n)} = {en_kucuk} × {_tr_sayi(n // en_kucuk)}`"), "Asallık Testi"

    # "A, B'nin yüzde kaçı?"  /  "20 80'in yüzde kaçıdır"
    m = re.search(_SAYI + r"\s*,?\s*" + _SAYI + _EK + r"\s*y[üu]zde\s*ka[çc]", t)
    if m:
        a, b = _f(m.group(1)), _f(m.group(2))
        if b == 0:
            return "⚠️ 0'ın yüzdesi hesaplanamaz (paydada 0 olur).", "Yüzde Oranı"
        oran = a / b * 100
        return (f"💯 **Yüzde Oranı:** `{sayi_yaz(a)}`, `{sayi_yaz(b)}` sayısının "
                f"`({sayi_yaz(a)} / {sayi_yaz(b)}) × 100` = **%{sayi_yaz(oran).split(' ≈')[-1].strip()}**'idir."), "Yüzde Oranı"

    # "120'nin %15'i kaç", "200'ün yüzde 30'u", "%15'i 120'nin"  → doğrudan yüzde hesabı
    m = (re.search(_SAYI + _EK + r"\s*(?:%|y[üu]zde)\s*" + _SAYI + r"\s*'?\s*(?:[ıiuü]|s[ıiuü]|n[ıiuü]|y[ıiuü])\b(?!\s*(?:" +
                   r"art|azal|zam|indirim|fazla|eksil|d[üu][şs]))", t))
    if m:
        ana, oran = _f(m.group(1)), _f(m.group(2))
        sonuc = ana * oran / 100
        return (f"💯 **Yüzde Hesabı:** `{sayi_yaz(ana)}` sayısının yüzde `{sayi_yaz(oran)}` kadarı\n"
                f"• `{sayi_yaz(ana)} × {sayi_yaz(oran)} / 100` = **`{sayi_yaz(sonuc)}`**"), "Yüzde Hesabı"

    # Yüzde artış / zam / azalış / indirim
    artis = r"(?:art[ıi][şs]|art[ıi]r|zam|fazla|ekle)"
    azalis = r"(?:azal[ıi][şs]|azalt|indirim|eksil|d[üu][şs][üu][şs]|d[üu][şs]|iskonto)"
    m = (re.search(_SAYI + _EK + r"\s*(?:%|y[üu]zde)\s*" + _SAYI + r"\s*(?:'?\s*\w{0,3})?\s*(" + artis + "|" + azalis + ")", t)
         or re.search(r"(?:%|y[üu]zde)\s*" + _SAYI + r"\s*(" + artis + "|" + azalis + r")\w*\s*" + _SAYI, t))
    if m:
        g = m.groups()
        if re.match(r"\d", g[1] or ""):
            ana, oran, tur = _f(g[0]), _f(g[1]), g[2]
        else:
            oran, tur, ana = _f(g[0]), g[1], _f(g[2])
        artis_mi = re.match(artis, tur) is not None
        fark = ana * oran / 100
        yeni = ana + fark if artis_mi else ana - fark
        isaret, ad = ("+", "Artış/Zam") if artis_mi else ("−", "Azalış/İndirim")
        return (f"💯 **Yüzde {ad}:** `{sayi_yaz(ana)}` sayısına %{sayi_yaz(oran)} {ad.lower()}\n"
                f"• Değişim: `{sayi_yaz(ana)} × {sayi_yaz(oran)} / 100` = `{sayi_yaz(fark)}`\n"
                f"• Sonuç: `{sayi_yaz(ana)} {isaret} {sayi_yaz(fark)}` = **`{sayi_yaz(yeni)}`**"), f"Yüzde {ad}"
    return None


# ------------------------------------------------------------------------------
# Giriş noktası
# ------------------------------------------------------------------------------
_IFADE_KARAKTERLERI = re.compile(r"[\d√π][\s\d.,+\-*/^()!%√πa-zçğıöşü]*")


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


def pro_matematik_coz(metin: str):
    """Metin bir matematik sorusuysa (cevap, etiket) döndürür; değilse (None, None)."""
    cevap, etiket = _pro_matematik_coz_ham(metin)
    return (_md_satirlari_koru(cevap), etiket) if cevap else (None, None)


def _pro_matematik_coz_ham(metin: str):
    if not metin or len(metin) > 300:
        return None, None
    kucuk = metin.replace("İ", "i").replace("I", "ı").lower().replace("̇", "").strip()

    try:
        ozel = _ozel_kaliplar(kucuk)
    except (ValueError, ZeroDivisionError, OverflowError):
        ozel = None
    if ozel:
        return ozel

    # Denklem
    if "=" in kucuk and re.search(r"\bx\b|\dx|x[\^²\d(]|\)x", kucuk):
        try:
            return denklem_coz(metin)
        except MatHata as h:
            if "polinom" in str(h) or "2. derece" in str(h):
                return f"📐 **Denklem:** `{metin.strip()}`\n⚠️ {h}.", "Denklem"
            return None, None
        except (ZeroDivisionError, OverflowError):
            return None, None

    # Saf ifade
    s = _normalize(metin, denklem=False)
    if not s or not re.search(r"\d|π|\be\b", s):
        return None, None
    if re.fullmatch(r"√ ?\d+", s):
        return None, None  # tek karekök → Modül 4'ün a√b sadeleştirmesi daha öğretici
    # En az bir işlem/fonksiyon olmalı ("5" tek başına hesaplama değildir)
    if not re.search(r"[+\-*/^!%√]|\b(?:" + "|".join(_FONKSIYONLAR) + r")\b|\d\s*\(|\)\s*\(", s):
        return None, None
    try:
        tokenlar = _tokenlara_ayir(s)
    except MatHata:
        return None, None  # metin matematik ifadesi değil → diğer motorlara bırak
    if ("deg", "x") in tokenlar:
        return None, None
    try:
        sonuc = _Ayristirici(tokenlar).calistir()
    except SozdizimHatasi:
        return None, None
    except MatHata as h:
        return f"🧮 **Hesaplama:** `{s}`\n⚠️ {h}.", "Hesaplama Uyarısı"
    except (ZeroDivisionError,):
        return f"🧮 **Hesaplama:** `{s}`\n⚠️ Sıfıra bölme tanımsızdır.", "Hesaplama Uyarısı"
    except OverflowError:
        return f"🧮 **Hesaplama:** `{s}`\n⚠️ Sonuç çok büyük.", "Hesaplama Uyarısı"

    gorunen = re.sub(r"√ ", "√", s).replace("*", "×").replace("/", "÷")
    gorunen = re.sub(r"(?<=[\w)π!%])\s*([+\-×÷])\s*", r" \1 ", gorunen)  # ikili işlemlerin etrafına boşluk
    sonuc_yazi = sayi_yaz(sonuc)
    if isinstance(sonuc, Fraction) and sonuc.denominator == 1 and len(sonuc_yazi) > 60:
        rakam = str(abs(sonuc.numerator))
        sonuc_yazi = f"{'-' if sonuc < 0 else ''}{rakam[:20]}…{rakam[-10:]} ({len(rakam)} basamak)"
    return f"🧮 **Hesaplama:** `{gorunen}` = **`{sonuc_yazi}`**", "Hesaplama"
