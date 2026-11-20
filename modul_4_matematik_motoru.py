# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v4.0 — MODÜL 4: GELİŞMİŞ MATEMATİK, DÖRT İŞLEM, KÖKLÜ/ÜSLÜ SAYILAR,
DENKLEM, PİSAGOR, 224 REFERANS SAYI VE 154 ÇÖZÜMLÜ SORU (modul_4_matematik_motoru.py)
==============================================================================
"""
import ast
import math
import operator
import random
import re
import streamlit as st
import importlib.util
import os
import sys

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
if _MODUL_DIZINI not in sys.path:
    sys.path.insert(0, _MODUL_DIZINI)


def _guvenli_modul_yukle(modul_adi: str):
    if modul_adi in sys.modules and getattr(sys.modules[modul_adi], "__file__", None):
        return sys.modules[modul_adi]
    aday_yollar = [os.path.join(_MODUL_DIZINI, f"{modul_adi}.py")]
    for _ana in [_MODUL_DIZINI]:
        for _kok, _altlar, _dosyalar in os.walk(_ana):
            _altlar[:] = [d for d in _altlar if not d.startswith(".") and d not in ("__pycache__", "venv", ".venv")]
            if f"{modul_adi}.py" in _dosyalar:
                tam = os.path.join(_kok, f"{modul_adi}.py")
                if tam not in aday_yollar:
                    aday_yollar.append(tam)
    for yol in aday_yollar:
        if os.path.exists(yol):
            spec = importlib.util.spec_from_file_location(modul_adi, yol)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[modul_adi] = mod
                spec.loader.exec_module(mod)
                return mod
    return __import__(modul_adi)

_m1 = _guvenli_modul_yukle("modul_1_arayuz_ve_tema")
bilgi_karti_olustur = _m1.bilgi_karti_olustur

# Profesyonel matematik çekirdeği (Modül 14): gerçek ifade ayrıştırıcı + denklem çözücü.
try:
    _m14 = _guvenli_modul_yukle("modul_14_pro_matematik")
    _pro_matematik_coz = _m14.pro_matematik_coz
except Exception:
    _pro_matematik_coz = None

_IZINLI_OPERATORLER = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# ==============================================================================
# 1. MATEMATİK, GEOMETRİ VE FİZİK KONU ANLATIM ANSİKLOPEDİSİ
# ==============================================================================
MATEMATIK_KONU_REHBERI = {
    "➕ Toplama ve Çıkarma Teknikleri": {
        "alt_baslik": "Temel Aritmetik & Zihinden Hızlı İşlem",
        "icerik": "• **Değişme ve Birleşme:** Toplamada sayıların yeri değişse de sonuç değişmez (`a + b = b + a`).\n• **İşaret Kuralları:** İki eksi yan yana gelirse artıya dönüşür (`12 - (-8) = 12 + 8 = 20`).\n• **Zihinden Tamamlama:** `78 + 46` işleminde `78 + 2 = 80`, `80 + 44 = 124`.",
    },
    "✖️ Çarpma ve Bölme & Ahmet'in Tekniği": {
        "alt_baslik": "Hızlı Zihinden Çarpma & Bölünebilme",
        "icerik": "• **Ahmet'in 25 ile Çarpma Tekniği:** Sayıyı 4'e böl, yanına iki sıfır ekle (`76 × 25` → `76 / 4 = 19` → `1900`).\n• **Ahmet'in 24 ile Çarpma Tekniği:** `76 × 24 = (76 × 25) - 76 = 1900 - 76 = 1824`.\n• **11 ile Pratik Çarpma:** `43 × 11` → Rakamları topla ortasına yaz → `4 (4+3) 3 = 473`.\n• **Sıfır Kuralı:** `0 / a = 0`, fakat `a / 0` tanımsızdır!",
    },
    "√ Köklü Sayılar (Karekök & a√b)": {
        "alt_baslik": "9. Sınıf & LGS İleri Matematik",
        "icerik": "• **Tam Kare Sayılar:** `1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400`.\n• **Kök Dışına Çıkarma (`a√b`):** `√72 = √(36 × 2) = 6√2` | `√128 = √(64 × 2) = 8√2`.\n• **Toplama / Çıkarma:** Kök içleri eşitse katsayılar toplanır (`5√3 + 2√3 = 7√3`).\n• **Paydayı Rasyonel Yapma:** `6 / √3 = (6√3) / 3 = 2√3`.",
    },
    "🔺 Üslü Sayılar ve Bilimsel Gösterim": {
        "alt_baslik": "Kuvvet Kuralları & Üslü Denklemler",
        "icerik": "• **Temel Kurallar:** `a⁰ = 1` (`a ≠ 0`), `a⁻ⁿ = 1 / aⁿ`.\n• **Çarpma ve Bölme:** Tabanlar aynıysa çarpmada üsler toplanır (`2⁵ × 2³ = 2⁸`), bölmede çıkarılır (`2⁵ / 2³ = 2²`).\n• **Üssün Üssü:** `(aⁿ)ᵐ = aⁿˣᵐ` (Örn: `(3²)⁴ = 3⁸`).",
    },
    "📐 1. ve 2. Dereceden Denklemler": {
        "alt_baslik": "Cebir & Diskriminant (Δ) Çözümü",
        "icerik": "• **1. Derece (`ax + b = c`):** Bilinenler bir tarafa, bilinmeyenler diğer tarafa toplanır (`x = (c - b) / a`).\n• **2. Derece (`ax² + bx + c = 0`):** Diskriminant `Δ = b² - 4ac`.\n• `Δ > 0` ise iki farklı reel kök vardır: `x₁,₂ = (-b ± √Δ) / (2a)`.",
    },
    "🔢 EBOB, EKOK ve Asal Çarpanlar": {
        "alt_baslik": "Sayılar Teorisi & Problemler",
        "icerik": "• **EBOB:** İki veya daha fazla sayıyı aynı anda bölen en büyük tam sayıdır (Büyük parçadan küçük parçaya giderken).\n• **EKOK:** Sayıların ortak katlarının en küçüğüdür (Küçük parçaları birleştirip nöbet/zaman problemi çözerken).\n• **Altın Özdeşlik:** İki sayı için `EBOB(a, b) × EKOK(a, b) = a × b`.",
    },
    "📏 Geometri, Pisagor ve Alan/Hacim": {
        "alt_baslik": "Üçgenler, Çember ve Katı Cisimler",
        "icerik": "• **Pisagor Teoremi:** Dik üçgende `a² + b² = c²` (Özel üçgenler: `3-4-5`, `5-12-13`, `8-15-17`, `7-24-25`).\n• **Daire:** Alan = `πr²`, Çevre = `2πr`.\n• **Küre:** Hacim = `(4/3)πr³`, Yüzey Alanı = `4πr²`.",
    },
    "🚀 Fizik & İHA Mühendislik Hesapları": {
        "alt_baslik": "Hareket, Kuvvet, Enerji ve Elektrik",
        "icerik": "• **Newton'un 2. Yasası:** `F = m × a` (Kuvvet = Kütle × İvme).\n• **Kinetik Enerji:** `Ek = ½ × m × v²` | **Potansiyel Enerji:** `Ep = m × g × h`.\n• **Ohm Yasası (Elektronik):** `V = I × R` (Gerilim = Akım × Direnç) | **Güç:** `P = V × I`.",
    },
}

# ==============================================================================
# 2. ÖN HESAPLANMIŞ KAREKÖK, KARE, KÜP VE ASAL ÇARPAN TABLOSU (220+ SAYI)
# ==============================================================================
MATEMATIK_REFERANS_TABLOSU = {
    1: {
        "sayi": 1,
        "karesi": 1,
        "kupu": 1,
        "karekok_sade": "1",
        "karekok_ondalik": 1.0,
        "cift_mi": False,
    },
    2: {
        "sayi": 2,
        "karesi": 4,
        "kupu": 8,
        "karekok_sade": "√2",
        "karekok_ondalik": 1.4142,
        "cift_mi": True,
    },
    3: {
        "sayi": 3,
        "karesi": 9,
        "kupu": 27,
        "karekok_sade": "√3",
        "karekok_ondalik": 1.7321,
        "cift_mi": False,
    },
    4: {
        "sayi": 4,
        "karesi": 16,
        "kupu": 64,
        "karekok_sade": "2",
        "karekok_ondalik": 2.0,
        "cift_mi": True,
    },
    5: {
        "sayi": 5,
        "karesi": 25,
        "kupu": 125,
        "karekok_sade": "√5",
        "karekok_ondalik": 2.2361,
        "cift_mi": False,
    },
    6: {
        "sayi": 6,
        "karesi": 36,
        "kupu": 216,
        "karekok_sade": "√6",
        "karekok_ondalik": 2.4495,
        "cift_mi": True,
    },
    7: {
        "sayi": 7,
        "karesi": 49,
        "kupu": 343,
        "karekok_sade": "√7",
        "karekok_ondalik": 2.6458,
        "cift_mi": False,
    },
    8: {
        "sayi": 8,
        "karesi": 64,
        "kupu": 512,
        "karekok_sade": "2√2",
        "karekok_ondalik": 2.8284,
        "cift_mi": True,
    },
    9: {
        "sayi": 9,
        "karesi": 81,
        "kupu": 729,
        "karekok_sade": "3",
        "karekok_ondalik": 3.0,
        "cift_mi": False,
    },
    10: {
        "sayi": 10,
        "karesi": 100,
        "kupu": 1000,
        "karekok_sade": "√10",
        "karekok_ondalik": 3.1623,
        "cift_mi": True,
    },
    11: {
        "sayi": 11,
        "karesi": 121,
        "kupu": 1331,
        "karekok_sade": "√11",
        "karekok_ondalik": 3.3166,
        "cift_mi": False,
    },
    12: {
        "sayi": 12,
        "karesi": 144,
        "kupu": 1728,
        "karekok_sade": "2√3",
        "karekok_ondalik": 3.4641,
        "cift_mi": True,
    },
    13: {
        "sayi": 13,
        "karesi": 169,
        "kupu": 2197,
        "karekok_sade": "√13",
        "karekok_ondalik": 3.6056,
        "cift_mi": False,
    },
    14: {
        "sayi": 14,
        "karesi": 196,
        "kupu": 2744,
        "karekok_sade": "√14",
        "karekok_ondalik": 3.7417,
        "cift_mi": True,
    },
    15: {
        "sayi": 15,
        "karesi": 225,
        "kupu": 3375,
        "karekok_sade": "√15",
        "karekok_ondalik": 3.873,
        "cift_mi": False,
    },
    16: {
        "sayi": 16,
        "karesi": 256,
        "kupu": 4096,
        "karekok_sade": "4",
        "karekok_ondalik": 4.0,
        "cift_mi": True,
    },
    17: {
        "sayi": 17,
        "karesi": 289,
        "kupu": 4913,
        "karekok_sade": "√17",
        "karekok_ondalik": 4.1231,
        "cift_mi": False,
    },
    18: {
        "sayi": 18,
        "karesi": 324,
        "kupu": 5832,
        "karekok_sade": "3√2",
        "karekok_ondalik": 4.2426,
        "cift_mi": True,
    },
    19: {
        "sayi": 19,
        "karesi": 361,
        "kupu": 6859,
        "karekok_sade": "√19",
        "karekok_ondalik": 4.3589,
        "cift_mi": False,
    },
    20: {
        "sayi": 20,
        "karesi": 400,
        "kupu": 8000,
        "karekok_sade": "2√5",
        "karekok_ondalik": 4.4721,
        "cift_mi": True,
    },
    21: {
        "sayi": 21,
        "karesi": 441,
        "kupu": 9261,
        "karekok_sade": "√21",
        "karekok_ondalik": 4.5826,
        "cift_mi": False,
    },
    22: {
        "sayi": 22,
        "karesi": 484,
        "kupu": 10648,
        "karekok_sade": "√22",
        "karekok_ondalik": 4.6904,
        "cift_mi": True,
    },
    23: {
        "sayi": 23,
        "karesi": 529,
        "kupu": 12167,
        "karekok_sade": "√23",
        "karekok_ondalik": 4.7958,
        "cift_mi": False,
    },
    24: {
        "sayi": 24,
        "karesi": 576,
        "kupu": 13824,
        "karekok_sade": "2√6",
        "karekok_ondalik": 4.899,
        "cift_mi": True,
    },
    25: {
        "sayi": 25,
        "karesi": 625,
        "kupu": 15625,
        "karekok_sade": "5",
        "karekok_ondalik": 5.0,
        "cift_mi": False,
    },
    26: {
        "sayi": 26,
        "karesi": 676,
        "kupu": 17576,
        "karekok_sade": "√26",
        "karekok_ondalik": 5.099,
        "cift_mi": True,
    },
    27: {
        "sayi": 27,
        "karesi": 729,
        "kupu": 19683,
        "karekok_sade": "3√3",
        "karekok_ondalik": 5.1962,
        "cift_mi": False,
    },
    28: {
        "sayi": 28,
        "karesi": 784,
        "kupu": 21952,
        "karekok_sade": "2√7",
        "karekok_ondalik": 5.2915,
        "cift_mi": True,
    },
    29: {
        "sayi": 29,
        "karesi": 841,
        "kupu": 24389,
        "karekok_sade": "√29",
        "karekok_ondalik": 5.3852,
        "cift_mi": False,
    },
    30: {
        "sayi": 30,
        "karesi": 900,
        "kupu": 27000,
        "karekok_sade": "√30",
        "karekok_ondalik": 5.4772,
        "cift_mi": True,
    },
    31: {
        "sayi": 31,
        "karesi": 961,
        "kupu": 29791,
        "karekok_sade": "√31",
        "karekok_ondalik": 5.5678,
        "cift_mi": False,
    },
    32: {
        "sayi": 32,
        "karesi": 1024,
        "kupu": 32768,
        "karekok_sade": "4√2",
        "karekok_ondalik": 5.6569,
        "cift_mi": True,
    },
    33: {
        "sayi": 33,
        "karesi": 1089,
        "kupu": 35937,
        "karekok_sade": "√33",
        "karekok_ondalik": 5.7446,
        "cift_mi": False,
    },
    34: {
        "sayi": 34,
        "karesi": 1156,
        "kupu": 39304,
        "karekok_sade": "√34",
        "karekok_ondalik": 5.831,
        "cift_mi": True,
    },
    35: {
        "sayi": 35,
        "karesi": 1225,
        "kupu": 42875,
        "karekok_sade": "√35",
        "karekok_ondalik": 5.9161,
        "cift_mi": False,
    },
    36: {
        "sayi": 36,
        "karesi": 1296,
        "kupu": 46656,
        "karekok_sade": "6",
        "karekok_ondalik": 6.0,
        "cift_mi": True,
    },
    37: {
        "sayi": 37,
        "karesi": 1369,
        "kupu": 50653,
        "karekok_sade": "√37",
        "karekok_ondalik": 6.0828,
        "cift_mi": False,
    },
    38: {
        "sayi": 38,
        "karesi": 1444,
        "kupu": 54872,
        "karekok_sade": "√38",
        "karekok_ondalik": 6.1644,
        "cift_mi": True,
    },
    39: {
        "sayi": 39,
        "karesi": 1521,
        "kupu": 59319,
        "karekok_sade": "√39",
        "karekok_ondalik": 6.245,
        "cift_mi": False,
    },
    40: {
        "sayi": 40,
        "karesi": 1600,
        "kupu": 64000,
        "karekok_sade": "2√10",
        "karekok_ondalik": 6.3246,
        "cift_mi": True,
    },
    41: {
        "sayi": 41,
        "karesi": 1681,
        "kupu": 68921,
        "karekok_sade": "√41",
        "karekok_ondalik": 6.4031,
        "cift_mi": False,
    },
    42: {
        "sayi": 42,
        "karesi": 1764,
        "kupu": 74088,
        "karekok_sade": "√42",
        "karekok_ondalik": 6.4807,
        "cift_mi": True,
    },
    43: {
        "sayi": 43,
        "karesi": 1849,
        "kupu": 79507,
        "karekok_sade": "√43",
        "karekok_ondalik": 6.5574,
        "cift_mi": False,
    },
    44: {
        "sayi": 44,
        "karesi": 1936,
        "kupu": 85184,
        "karekok_sade": "2√11",
        "karekok_ondalik": 6.6332,
        "cift_mi": True,
    },
    45: {
        "sayi": 45,
        "karesi": 2025,
        "kupu": 91125,
        "karekok_sade": "3√5",
        "karekok_ondalik": 6.7082,
        "cift_mi": False,
    },
    46: {
        "sayi": 46,
        "karesi": 2116,
        "kupu": 97336,
        "karekok_sade": "√46",
        "karekok_ondalik": 6.7823,
        "cift_mi": True,
    },
    47: {
        "sayi": 47,
        "karesi": 2209,
        "kupu": 103823,
        "karekok_sade": "√47",
        "karekok_ondalik": 6.8557,
        "cift_mi": False,
    },
    48: {
        "sayi": 48,
        "karesi": 2304,
        "kupu": 110592,
        "karekok_sade": "4√3",
        "karekok_ondalik": 6.9282,
        "cift_mi": True,
    },
    49: {
        "sayi": 49,
        "karesi": 2401,
        "kupu": 117649,
        "karekok_sade": "7",
        "karekok_ondalik": 7.0,
        "cift_mi": False,
    },
    50: {
        "sayi": 50,
        "karesi": 2500,
        "kupu": 125000,
        "karekok_sade": "5√2",
        "karekok_ondalik": 7.0711,
        "cift_mi": True,
    },
    51: {
        "sayi": 51,
        "karesi": 2601,
        "kupu": 132651,
        "karekok_sade": "√51",
        "karekok_ondalik": 7.1414,
        "cift_mi": False,
    },
    52: {
        "sayi": 52,
        "karesi": 2704,
        "kupu": 140608,
        "karekok_sade": "2√13",
        "karekok_ondalik": 7.2111,
        "cift_mi": True,
    },
    53: {
        "sayi": 53,
        "karesi": 2809,
        "kupu": 148877,
        "karekok_sade": "√53",
        "karekok_ondalik": 7.2801,
        "cift_mi": False,
    },
    54: {
        "sayi": 54,
        "karesi": 2916,
        "kupu": 157464,
        "karekok_sade": "3√6",
        "karekok_ondalik": 7.3485,
        "cift_mi": True,
    },
    55: {
        "sayi": 55,
        "karesi": 3025,
        "kupu": 166375,
        "karekok_sade": "√55",
        "karekok_ondalik": 7.4162,
        "cift_mi": False,
    },
    56: {
        "sayi": 56,
        "karesi": 3136,
        "kupu": 175616,
        "karekok_sade": "2√14",
        "karekok_ondalik": 7.4833,
        "cift_mi": True,
    },
    57: {
        "sayi": 57,
        "karesi": 3249,
        "kupu": 185193,
        "karekok_sade": "√57",
        "karekok_ondalik": 7.5498,
        "cift_mi": False,
    },
    58: {
        "sayi": 58,
        "karesi": 3364,
        "kupu": 195112,
        "karekok_sade": "√58",
        "karekok_ondalik": 7.6158,
        "cift_mi": True,
    },
    59: {
        "sayi": 59,
        "karesi": 3481,
        "kupu": 205379,
        "karekok_sade": "√59",
        "karekok_ondalik": 7.6811,
        "cift_mi": False,
    },
    60: {
        "sayi": 60,
        "karesi": 3600,
        "kupu": 216000,
        "karekok_sade": "2√15",
        "karekok_ondalik": 7.746,
        "cift_mi": True,
    },
    61: {
        "sayi": 61,
        "karesi": 3721,
        "kupu": 226981,
        "karekok_sade": "√61",
        "karekok_ondalik": 7.8102,
        "cift_mi": False,
    },
    62: {
        "sayi": 62,
        "karesi": 3844,
        "kupu": 238328,
        "karekok_sade": "√62",
        "karekok_ondalik": 7.874,
        "cift_mi": True,
    },
    63: {
        "sayi": 63,
        "karesi": 3969,
        "kupu": 250047,
        "karekok_sade": "3√7",
        "karekok_ondalik": 7.9373,
        "cift_mi": False,
    },
    64: {
        "sayi": 64,
        "karesi": 4096,
        "kupu": 262144,
        "karekok_sade": "8",
        "karekok_ondalik": 8.0,
        "cift_mi": True,
    },
    65: {
        "sayi": 65,
        "karesi": 4225,
        "kupu": 274625,
        "karekok_sade": "√65",
        "karekok_ondalik": 8.0623,
        "cift_mi": False,
    },
    66: {
        "sayi": 66,
        "karesi": 4356,
        "kupu": 287496,
        "karekok_sade": "√66",
        "karekok_ondalik": 8.124,
        "cift_mi": True,
    },
    67: {
        "sayi": 67,
        "karesi": 4489,
        "kupu": 300763,
        "karekok_sade": "√67",
        "karekok_ondalik": 8.1854,
        "cift_mi": False,
    },
    68: {
        "sayi": 68,
        "karesi": 4624,
        "kupu": 314432,
        "karekok_sade": "2√17",
        "karekok_ondalik": 8.2462,
        "cift_mi": True,
    },
    69: {
        "sayi": 69,
        "karesi": 4761,
        "kupu": 328509,
        "karekok_sade": "√69",
        "karekok_ondalik": 8.3066,
        "cift_mi": False,
    },
    70: {
        "sayi": 70,
        "karesi": 4900,
        "kupu": 343000,
        "karekok_sade": "√70",
        "karekok_ondalik": 8.3666,
        "cift_mi": True,
    },
    71: {
        "sayi": 71,
        "karesi": 5041,
        "kupu": 357911,
        "karekok_sade": "√71",
        "karekok_ondalik": 8.4261,
        "cift_mi": False,
    },
    72: {
        "sayi": 72,
        "karesi": 5184,
        "kupu": 373248,
        "karekok_sade": "6√2",
        "karekok_ondalik": 8.4853,
        "cift_mi": True,
    },
    73: {
        "sayi": 73,
        "karesi": 5329,
        "kupu": 389017,
        "karekok_sade": "√73",
        "karekok_ondalik": 8.544,
        "cift_mi": False,
    },
    74: {
        "sayi": 74,
        "karesi": 5476,
        "kupu": 405224,
        "karekok_sade": "√74",
        "karekok_ondalik": 8.6023,
        "cift_mi": True,
    },
    75: {
        "sayi": 75,
        "karesi": 5625,
        "kupu": 421875,
        "karekok_sade": "5√3",
        "karekok_ondalik": 8.6603,
        "cift_mi": False,
    },
    76: {
        "sayi": 76,
        "karesi": 5776,
        "kupu": 438976,
        "karekok_sade": "2√19",
        "karekok_ondalik": 8.7178,
        "cift_mi": True,
    },
    77: {
        "sayi": 77,
        "karesi": 5929,
        "kupu": 456533,
        "karekok_sade": "√77",
        "karekok_ondalik": 8.775,
        "cift_mi": False,
    },
    78: {
        "sayi": 78,
        "karesi": 6084,
        "kupu": 474552,
        "karekok_sade": "√78",
        "karekok_ondalik": 8.8318,
        "cift_mi": True,
    },
    79: {
        "sayi": 79,
        "karesi": 6241,
        "kupu": 493039,
        "karekok_sade": "√79",
        "karekok_ondalik": 8.8882,
        "cift_mi": False,
    },
    80: {
        "sayi": 80,
        "karesi": 6400,
        "kupu": 512000,
        "karekok_sade": "4√5",
        "karekok_ondalik": 8.9443,
        "cift_mi": True,
    },
    81: {
        "sayi": 81,
        "karesi": 6561,
        "kupu": 531441,
        "karekok_sade": "9",
        "karekok_ondalik": 9.0,
        "cift_mi": False,
    },
    82: {
        "sayi": 82,
        "karesi": 6724,
        "kupu": 551368,
        "karekok_sade": "√82",
        "karekok_ondalik": 9.0554,
        "cift_mi": True,
    },
    83: {
        "sayi": 83,
        "karesi": 6889,
        "kupu": 571787,
        "karekok_sade": "√83",
        "karekok_ondalik": 9.1104,
        "cift_mi": False,
    },
    84: {
        "sayi": 84,
        "karesi": 7056,
        "kupu": 592704,
        "karekok_sade": "2√21",
        "karekok_ondalik": 9.1652,
        "cift_mi": True,
    },
    85: {
        "sayi": 85,
        "karesi": 7225,
        "kupu": 614125,
        "karekok_sade": "√85",
        "karekok_ondalik": 9.2195,
        "cift_mi": False,
    },
    86: {
        "sayi": 86,
        "karesi": 7396,
        "kupu": 636056,
        "karekok_sade": "√86",
        "karekok_ondalik": 9.2736,
        "cift_mi": True,
    },
    87: {
        "sayi": 87,
        "karesi": 7569,
        "kupu": 658503,
        "karekok_sade": "√87",
        "karekok_ondalik": 9.3274,
        "cift_mi": False,
    },
    88: {
        "sayi": 88,
        "karesi": 7744,
        "kupu": 681472,
        "karekok_sade": "2√22",
        "karekok_ondalik": 9.3808,
        "cift_mi": True,
    },
    89: {
        "sayi": 89,
        "karesi": 7921,
        "kupu": 704969,
        "karekok_sade": "√89",
        "karekok_ondalik": 9.434,
        "cift_mi": False,
    },
    90: {
        "sayi": 90,
        "karesi": 8100,
        "kupu": 729000,
        "karekok_sade": "3√10",
        "karekok_ondalik": 9.4868,
        "cift_mi": True,
    },
    91: {
        "sayi": 91,
        "karesi": 8281,
        "kupu": 753571,
        "karekok_sade": "√91",
        "karekok_ondalik": 9.5394,
        "cift_mi": False,
    },
    92: {
        "sayi": 92,
        "karesi": 8464,
        "kupu": 778688,
        "karekok_sade": "2√23",
        "karekok_ondalik": 9.5917,
        "cift_mi": True,
    },
    93: {
        "sayi": 93,
        "karesi": 8649,
        "kupu": 804357,
        "karekok_sade": "√93",
        "karekok_ondalik": 9.6437,
        "cift_mi": False,
    },
    94: {
        "sayi": 94,
        "karesi": 8836,
        "kupu": 830584,
        "karekok_sade": "√94",
        "karekok_ondalik": 9.6954,
        "cift_mi": True,
    },
    95: {
        "sayi": 95,
        "karesi": 9025,
        "kupu": 857375,
        "karekok_sade": "√95",
        "karekok_ondalik": 9.7468,
        "cift_mi": False,
    },
    96: {
        "sayi": 96,
        "karesi": 9216,
        "kupu": 884736,
        "karekok_sade": "4√6",
        "karekok_ondalik": 9.798,
        "cift_mi": True,
    },
    97: {
        "sayi": 97,
        "karesi": 9409,
        "kupu": 912673,
        "karekok_sade": "√97",
        "karekok_ondalik": 9.8489,
        "cift_mi": False,
    },
    98: {
        "sayi": 98,
        "karesi": 9604,
        "kupu": 941192,
        "karekok_sade": "7√2",
        "karekok_ondalik": 9.8995,
        "cift_mi": True,
    },
    99: {
        "sayi": 99,
        "karesi": 9801,
        "kupu": 970299,
        "karekok_sade": "3√11",
        "karekok_ondalik": 9.9499,
        "cift_mi": False,
    },
    100: {
        "sayi": 100,
        "karesi": 10000,
        "kupu": 1000000,
        "karekok_sade": "10",
        "karekok_ondalik": 10.0,
        "cift_mi": True,
    },
    101: {
        "sayi": 101,
        "karesi": 10201,
        "kupu": 1030301,
        "karekok_sade": "√101",
        "karekok_ondalik": 10.0499,
        "cift_mi": False,
    },
    102: {
        "sayi": 102,
        "karesi": 10404,
        "kupu": 1061208,
        "karekok_sade": "√102",
        "karekok_ondalik": 10.0995,
        "cift_mi": True,
    },
    103: {
        "sayi": 103,
        "karesi": 10609,
        "kupu": 1092727,
        "karekok_sade": "√103",
        "karekok_ondalik": 10.1489,
        "cift_mi": False,
    },
    104: {
        "sayi": 104,
        "karesi": 10816,
        "kupu": 1124864,
        "karekok_sade": "2√26",
        "karekok_ondalik": 10.198,
        "cift_mi": True,
    },
    105: {
        "sayi": 105,
        "karesi": 11025,
        "kupu": 1157625,
        "karekok_sade": "√105",
        "karekok_ondalik": 10.247,
        "cift_mi": False,
    },
    106: {
        "sayi": 106,
        "karesi": 11236,
        "kupu": 1191016,
        "karekok_sade": "√106",
        "karekok_ondalik": 10.2956,
        "cift_mi": True,
    },
    107: {
        "sayi": 107,
        "karesi": 11449,
        "kupu": 1225043,
        "karekok_sade": "√107",
        "karekok_ondalik": 10.3441,
        "cift_mi": False,
    },
    108: {
        "sayi": 108,
        "karesi": 11664,
        "kupu": 1259712,
        "karekok_sade": "6√3",
        "karekok_ondalik": 10.3923,
        "cift_mi": True,
    },
    109: {
        "sayi": 109,
        "karesi": 11881,
        "kupu": 1295029,
        "karekok_sade": "√109",
        "karekok_ondalik": 10.4403,
        "cift_mi": False,
    },
    110: {
        "sayi": 110,
        "karesi": 12100,
        "kupu": 1331000,
        "karekok_sade": "√110",
        "karekok_ondalik": 10.4881,
        "cift_mi": True,
    },
    111: {
        "sayi": 111,
        "karesi": 12321,
        "kupu": 1367631,
        "karekok_sade": "√111",
        "karekok_ondalik": 10.5357,
        "cift_mi": False,
    },
    112: {
        "sayi": 112,
        "karesi": 12544,
        "kupu": 1404928,
        "karekok_sade": "4√7",
        "karekok_ondalik": 10.583,
        "cift_mi": True,
    },
    113: {
        "sayi": 113,
        "karesi": 12769,
        "kupu": 1442897,
        "karekok_sade": "√113",
        "karekok_ondalik": 10.6301,
        "cift_mi": False,
    },
    114: {
        "sayi": 114,
        "karesi": 12996,
        "kupu": 1481544,
        "karekok_sade": "√114",
        "karekok_ondalik": 10.6771,
        "cift_mi": True,
    },
    115: {
        "sayi": 115,
        "karesi": 13225,
        "kupu": 1520875,
        "karekok_sade": "√115",
        "karekok_ondalik": 10.7238,
        "cift_mi": False,
    },
    116: {
        "sayi": 116,
        "karesi": 13456,
        "kupu": 1560896,
        "karekok_sade": "2√29",
        "karekok_ondalik": 10.7703,
        "cift_mi": True,
    },
    117: {
        "sayi": 117,
        "karesi": 13689,
        "kupu": 1601613,
        "karekok_sade": "3√13",
        "karekok_ondalik": 10.8167,
        "cift_mi": False,
    },
    118: {
        "sayi": 118,
        "karesi": 13924,
        "kupu": 1643032,
        "karekok_sade": "√118",
        "karekok_ondalik": 10.8628,
        "cift_mi": True,
    },
    119: {
        "sayi": 119,
        "karesi": 14161,
        "kupu": 1685159,
        "karekok_sade": "√119",
        "karekok_ondalik": 10.9087,
        "cift_mi": False,
    },
    120: {
        "sayi": 120,
        "karesi": 14400,
        "kupu": 1728000,
        "karekok_sade": "2√30",
        "karekok_ondalik": 10.9545,
        "cift_mi": True,
    },
    121: {
        "sayi": 121,
        "karesi": 14641,
        "kupu": 1771561,
        "karekok_sade": "11",
        "karekok_ondalik": 11.0,
        "cift_mi": False,
    },
    122: {
        "sayi": 122,
        "karesi": 14884,
        "kupu": 1815848,
        "karekok_sade": "√122",
        "karekok_ondalik": 11.0454,
        "cift_mi": True,
    },
    123: {
        "sayi": 123,
        "karesi": 15129,
        "kupu": 1860867,
        "karekok_sade": "√123",
        "karekok_ondalik": 11.0905,
        "cift_mi": False,
    },
    124: {
        "sayi": 124,
        "karesi": 15376,
        "kupu": 1906624,
        "karekok_sade": "2√31",
        "karekok_ondalik": 11.1355,
        "cift_mi": True,
    },
    125: {
        "sayi": 125,
        "karesi": 15625,
        "kupu": 1953125,
        "karekok_sade": "5√5",
        "karekok_ondalik": 11.1803,
        "cift_mi": False,
    },
    126: {
        "sayi": 126,
        "karesi": 15876,
        "kupu": 2000376,
        "karekok_sade": "3√14",
        "karekok_ondalik": 11.225,
        "cift_mi": True,
    },
    127: {
        "sayi": 127,
        "karesi": 16129,
        "kupu": 2048383,
        "karekok_sade": "√127",
        "karekok_ondalik": 11.2694,
        "cift_mi": False,
    },
    128: {
        "sayi": 128,
        "karesi": 16384,
        "kupu": 2097152,
        "karekok_sade": "8√2",
        "karekok_ondalik": 11.3137,
        "cift_mi": True,
    },
    129: {
        "sayi": 129,
        "karesi": 16641,
        "kupu": 2146689,
        "karekok_sade": "√129",
        "karekok_ondalik": 11.3578,
        "cift_mi": False,
    },
    130: {
        "sayi": 130,
        "karesi": 16900,
        "kupu": 2197000,
        "karekok_sade": "√130",
        "karekok_ondalik": 11.4018,
        "cift_mi": True,
    },
    131: {
        "sayi": 131,
        "karesi": 17161,
        "kupu": 2248091,
        "karekok_sade": "√131",
        "karekok_ondalik": 11.4455,
        "cift_mi": False,
    },
    132: {
        "sayi": 132,
        "karesi": 17424,
        "kupu": 2299968,
        "karekok_sade": "2√33",
        "karekok_ondalik": 11.4891,
        "cift_mi": True,
    },
    133: {
        "sayi": 133,
        "karesi": 17689,
        "kupu": 2352637,
        "karekok_sade": "√133",
        "karekok_ondalik": 11.5326,
        "cift_mi": False,
    },
    134: {
        "sayi": 134,
        "karesi": 17956,
        "kupu": 2406104,
        "karekok_sade": "√134",
        "karekok_ondalik": 11.5758,
        "cift_mi": True,
    },
    135: {
        "sayi": 135,
        "karesi": 18225,
        "kupu": 2460375,
        "karekok_sade": "3√15",
        "karekok_ondalik": 11.619,
        "cift_mi": False,
    },
    136: {
        "sayi": 136,
        "karesi": 18496,
        "kupu": 2515456,
        "karekok_sade": "2√34",
        "karekok_ondalik": 11.6619,
        "cift_mi": True,
    },
    137: {
        "sayi": 137,
        "karesi": 18769,
        "kupu": 2571353,
        "karekok_sade": "√137",
        "karekok_ondalik": 11.7047,
        "cift_mi": False,
    },
    138: {
        "sayi": 138,
        "karesi": 19044,
        "kupu": 2628072,
        "karekok_sade": "√138",
        "karekok_ondalik": 11.7473,
        "cift_mi": True,
    },
    139: {
        "sayi": 139,
        "karesi": 19321,
        "kupu": 2685619,
        "karekok_sade": "√139",
        "karekok_ondalik": 11.7898,
        "cift_mi": False,
    },
    140: {
        "sayi": 140,
        "karesi": 19600,
        "kupu": 2744000,
        "karekok_sade": "2√35",
        "karekok_ondalik": 11.8322,
        "cift_mi": True,
    },
    141: {
        "sayi": 141,
        "karesi": 19881,
        "kupu": 2803221,
        "karekok_sade": "√141",
        "karekok_ondalik": 11.8743,
        "cift_mi": False,
    },
    142: {
        "sayi": 142,
        "karesi": 20164,
        "kupu": 2863288,
        "karekok_sade": "√142",
        "karekok_ondalik": 11.9164,
        "cift_mi": True,
    },
    143: {
        "sayi": 143,
        "karesi": 20449,
        "kupu": 2924207,
        "karekok_sade": "√143",
        "karekok_ondalik": 11.9583,
        "cift_mi": False,
    },
    144: {
        "sayi": 144,
        "karesi": 20736,
        "kupu": 2985984,
        "karekok_sade": "12",
        "karekok_ondalik": 12.0,
        "cift_mi": True,
    },
    145: {
        "sayi": 145,
        "karesi": 21025,
        "kupu": 3048625,
        "karekok_sade": "√145",
        "karekok_ondalik": 12.0416,
        "cift_mi": False,
    },
    146: {
        "sayi": 146,
        "karesi": 21316,
        "kupu": 3112136,
        "karekok_sade": "√146",
        "karekok_ondalik": 12.083,
        "cift_mi": True,
    },
    147: {
        "sayi": 147,
        "karesi": 21609,
        "kupu": 3176523,
        "karekok_sade": "7√3",
        "karekok_ondalik": 12.1244,
        "cift_mi": False,
    },
    148: {
        "sayi": 148,
        "karesi": 21904,
        "kupu": 3241792,
        "karekok_sade": "2√37",
        "karekok_ondalik": 12.1655,
        "cift_mi": True,
    },
    149: {
        "sayi": 149,
        "karesi": 22201,
        "kupu": 3307949,
        "karekok_sade": "√149",
        "karekok_ondalik": 12.2066,
        "cift_mi": False,
    },
    150: {
        "sayi": 150,
        "karesi": 22500,
        "kupu": 3375000,
        "karekok_sade": "5√6",
        "karekok_ondalik": 12.2474,
        "cift_mi": True,
    },
    151: {
        "sayi": 151,
        "karesi": 22801,
        "kupu": 3442951,
        "karekok_sade": "√151",
        "karekok_ondalik": 12.2882,
        "cift_mi": False,
    },
    152: {
        "sayi": 152,
        "karesi": 23104,
        "kupu": 3511808,
        "karekok_sade": "2√38",
        "karekok_ondalik": 12.3288,
        "cift_mi": True,
    },
    153: {
        "sayi": 153,
        "karesi": 23409,
        "kupu": 3581577,
        "karekok_sade": "3√17",
        "karekok_ondalik": 12.3693,
        "cift_mi": False,
    },
    154: {
        "sayi": 154,
        "karesi": 23716,
        "kupu": 3652264,
        "karekok_sade": "√154",
        "karekok_ondalik": 12.4097,
        "cift_mi": True,
    },
    155: {
        "sayi": 155,
        "karesi": 24025,
        "kupu": 3723875,
        "karekok_sade": "√155",
        "karekok_ondalik": 12.4499,
        "cift_mi": False,
    },
    156: {
        "sayi": 156,
        "karesi": 24336,
        "kupu": 3796416,
        "karekok_sade": "2√39",
        "karekok_ondalik": 12.49,
        "cift_mi": True,
    },
    157: {
        "sayi": 157,
        "karesi": 24649,
        "kupu": 3869893,
        "karekok_sade": "√157",
        "karekok_ondalik": 12.53,
        "cift_mi": False,
    },
    158: {
        "sayi": 158,
        "karesi": 24964,
        "kupu": 3944312,
        "karekok_sade": "√158",
        "karekok_ondalik": 12.5698,
        "cift_mi": True,
    },
    159: {
        "sayi": 159,
        "karesi": 25281,
        "kupu": 4019679,
        "karekok_sade": "√159",
        "karekok_ondalik": 12.6095,
        "cift_mi": False,
    },
    160: {
        "sayi": 160,
        "karesi": 25600,
        "kupu": 4096000,
        "karekok_sade": "4√10",
        "karekok_ondalik": 12.6491,
        "cift_mi": True,
    },
    161: {
        "sayi": 161,
        "karesi": 25921,
        "kupu": 4173281,
        "karekok_sade": "√161",
        "karekok_ondalik": 12.6886,
        "cift_mi": False,
    },
    162: {
        "sayi": 162,
        "karesi": 26244,
        "kupu": 4251528,
        "karekok_sade": "9√2",
        "karekok_ondalik": 12.7279,
        "cift_mi": True,
    },
    163: {
        "sayi": 163,
        "karesi": 26569,
        "kupu": 4330747,
        "karekok_sade": "√163",
        "karekok_ondalik": 12.7671,
        "cift_mi": False,
    },
    164: {
        "sayi": 164,
        "karesi": 26896,
        "kupu": 4410944,
        "karekok_sade": "2√41",
        "karekok_ondalik": 12.8062,
        "cift_mi": True,
    },
    165: {
        "sayi": 165,
        "karesi": 27225,
        "kupu": 4492125,
        "karekok_sade": "√165",
        "karekok_ondalik": 12.8452,
        "cift_mi": False,
    },
    166: {
        "sayi": 166,
        "karesi": 27556,
        "kupu": 4574296,
        "karekok_sade": "√166",
        "karekok_ondalik": 12.8841,
        "cift_mi": True,
    },
    167: {
        "sayi": 167,
        "karesi": 27889,
        "kupu": 4657463,
        "karekok_sade": "√167",
        "karekok_ondalik": 12.9228,
        "cift_mi": False,
    },
    168: {
        "sayi": 168,
        "karesi": 28224,
        "kupu": 4741632,
        "karekok_sade": "2√42",
        "karekok_ondalik": 12.9615,
        "cift_mi": True,
    },
    169: {
        "sayi": 169,
        "karesi": 28561,
        "kupu": 4826809,
        "karekok_sade": "13",
        "karekok_ondalik": 13.0,
        "cift_mi": False,
    },
    170: {
        "sayi": 170,
        "karesi": 28900,
        "kupu": 4913000,
        "karekok_sade": "√170",
        "karekok_ondalik": 13.0384,
        "cift_mi": True,
    },
    171: {
        "sayi": 171,
        "karesi": 29241,
        "kupu": 5000211,
        "karekok_sade": "3√19",
        "karekok_ondalik": 13.0767,
        "cift_mi": False,
    },
    172: {
        "sayi": 172,
        "karesi": 29584,
        "kupu": 5088448,
        "karekok_sade": "2√43",
        "karekok_ondalik": 13.1149,
        "cift_mi": True,
    },
    173: {
        "sayi": 173,
        "karesi": 29929,
        "kupu": 5177717,
        "karekok_sade": "√173",
        "karekok_ondalik": 13.1529,
        "cift_mi": False,
    },
    174: {
        "sayi": 174,
        "karesi": 30276,
        "kupu": 5268024,
        "karekok_sade": "√174",
        "karekok_ondalik": 13.1909,
        "cift_mi": True,
    },
    175: {
        "sayi": 175,
        "karesi": 30625,
        "kupu": 5359375,
        "karekok_sade": "5√7",
        "karekok_ondalik": 13.2288,
        "cift_mi": False,
    },
    176: {
        "sayi": 176,
        "karesi": 30976,
        "kupu": 5451776,
        "karekok_sade": "4√11",
        "karekok_ondalik": 13.2665,
        "cift_mi": True,
    },
    177: {
        "sayi": 177,
        "karesi": 31329,
        "kupu": 5545233,
        "karekok_sade": "√177",
        "karekok_ondalik": 13.3041,
        "cift_mi": False,
    },
    178: {
        "sayi": 178,
        "karesi": 31684,
        "kupu": 5639752,
        "karekok_sade": "√178",
        "karekok_ondalik": 13.3417,
        "cift_mi": True,
    },
    179: {
        "sayi": 179,
        "karesi": 32041,
        "kupu": 5735339,
        "karekok_sade": "√179",
        "karekok_ondalik": 13.3791,
        "cift_mi": False,
    },
    180: {
        "sayi": 180,
        "karesi": 32400,
        "kupu": 5832000,
        "karekok_sade": "6√5",
        "karekok_ondalik": 13.4164,
        "cift_mi": True,
    },
    181: {
        "sayi": 181,
        "karesi": 32761,
        "kupu": 5929741,
        "karekok_sade": "√181",
        "karekok_ondalik": 13.4536,
        "cift_mi": False,
    },
    182: {
        "sayi": 182,
        "karesi": 33124,
        "kupu": 6028568,
        "karekok_sade": "√182",
        "karekok_ondalik": 13.4907,
        "cift_mi": True,
    },
    183: {
        "sayi": 183,
        "karesi": 33489,
        "kupu": 6128487,
        "karekok_sade": "√183",
        "karekok_ondalik": 13.5277,
        "cift_mi": False,
    },
    184: {
        "sayi": 184,
        "karesi": 33856,
        "kupu": 6229504,
        "karekok_sade": "2√46",
        "karekok_ondalik": 13.5647,
        "cift_mi": True,
    },
    185: {
        "sayi": 185,
        "karesi": 34225,
        "kupu": 6331625,
        "karekok_sade": "√185",
        "karekok_ondalik": 13.6015,
        "cift_mi": False,
    },
    186: {
        "sayi": 186,
        "karesi": 34596,
        "kupu": 6434856,
        "karekok_sade": "√186",
        "karekok_ondalik": 13.6382,
        "cift_mi": True,
    },
    187: {
        "sayi": 187,
        "karesi": 34969,
        "kupu": 6539203,
        "karekok_sade": "√187",
        "karekok_ondalik": 13.6748,
        "cift_mi": False,
    },
    188: {
        "sayi": 188,
        "karesi": 35344,
        "kupu": 6644672,
        "karekok_sade": "2√47",
        "karekok_ondalik": 13.7113,
        "cift_mi": True,
    },
    189: {
        "sayi": 189,
        "karesi": 35721,
        "kupu": 6751269,
        "karekok_sade": "3√21",
        "karekok_ondalik": 13.7477,
        "cift_mi": False,
    },
    190: {
        "sayi": 190,
        "karesi": 36100,
        "kupu": 6859000,
        "karekok_sade": "√190",
        "karekok_ondalik": 13.784,
        "cift_mi": True,
    },
    191: {
        "sayi": 191,
        "karesi": 36481,
        "kupu": 6967871,
        "karekok_sade": "√191",
        "karekok_ondalik": 13.8203,
        "cift_mi": False,
    },
    192: {
        "sayi": 192,
        "karesi": 36864,
        "kupu": 7077888,
        "karekok_sade": "8√3",
        "karekok_ondalik": 13.8564,
        "cift_mi": True,
    },
    193: {
        "sayi": 193,
        "karesi": 37249,
        "kupu": 7189057,
        "karekok_sade": "√193",
        "karekok_ondalik": 13.8924,
        "cift_mi": False,
    },
    194: {
        "sayi": 194,
        "karesi": 37636,
        "kupu": 7301384,
        "karekok_sade": "√194",
        "karekok_ondalik": 13.9284,
        "cift_mi": True,
    },
    195: {
        "sayi": 195,
        "karesi": 38025,
        "kupu": 7414875,
        "karekok_sade": "√195",
        "karekok_ondalik": 13.9642,
        "cift_mi": False,
    },
    196: {
        "sayi": 196,
        "karesi": 38416,
        "kupu": 7529536,
        "karekok_sade": "14",
        "karekok_ondalik": 14.0,
        "cift_mi": True,
    },
    197: {
        "sayi": 197,
        "karesi": 38809,
        "kupu": 7645373,
        "karekok_sade": "√197",
        "karekok_ondalik": 14.0357,
        "cift_mi": False,
    },
    198: {
        "sayi": 198,
        "karesi": 39204,
        "kupu": 7762392,
        "karekok_sade": "3√22",
        "karekok_ondalik": 14.0712,
        "cift_mi": True,
    },
    199: {
        "sayi": 199,
        "karesi": 39601,
        "kupu": 7880599,
        "karekok_sade": "√199",
        "karekok_ondalik": 14.1067,
        "cift_mi": False,
    },
    200: {
        "sayi": 200,
        "karesi": 40000,
        "kupu": 8000000,
        "karekok_sade": "10√2",
        "karekok_ondalik": 14.1421,
        "cift_mi": True,
    },
    201: {
        "sayi": 201,
        "karesi": 40401,
        "kupu": 8120601,
        "karekok_sade": "√201",
        "karekok_ondalik": 14.1774,
        "cift_mi": False,
    },
    202: {
        "sayi": 202,
        "karesi": 40804,
        "kupu": 8242408,
        "karekok_sade": "√202",
        "karekok_ondalik": 14.2127,
        "cift_mi": True,
    },
    203: {
        "sayi": 203,
        "karesi": 41209,
        "kupu": 8365427,
        "karekok_sade": "√203",
        "karekok_ondalik": 14.2478,
        "cift_mi": False,
    },
    204: {
        "sayi": 204,
        "karesi": 41616,
        "kupu": 8489664,
        "karekok_sade": "2√51",
        "karekok_ondalik": 14.2829,
        "cift_mi": True,
    },
    205: {
        "sayi": 205,
        "karesi": 42025,
        "kupu": 8615125,
        "karekok_sade": "√205",
        "karekok_ondalik": 14.3178,
        "cift_mi": False,
    },
    206: {
        "sayi": 206,
        "karesi": 42436,
        "kupu": 8741816,
        "karekok_sade": "√206",
        "karekok_ondalik": 14.3527,
        "cift_mi": True,
    },
    207: {
        "sayi": 207,
        "karesi": 42849,
        "kupu": 8869743,
        "karekok_sade": "3√23",
        "karekok_ondalik": 14.3875,
        "cift_mi": False,
    },
    208: {
        "sayi": 208,
        "karesi": 43264,
        "kupu": 8998912,
        "karekok_sade": "4√13",
        "karekok_ondalik": 14.4222,
        "cift_mi": True,
    },
    209: {
        "sayi": 209,
        "karesi": 43681,
        "kupu": 9129329,
        "karekok_sade": "√209",
        "karekok_ondalik": 14.4568,
        "cift_mi": False,
    },
    210: {
        "sayi": 210,
        "karesi": 44100,
        "kupu": 9261000,
        "karekok_sade": "√210",
        "karekok_ondalik": 14.4914,
        "cift_mi": True,
    },
    211: {
        "sayi": 211,
        "karesi": 44521,
        "kupu": 9393931,
        "karekok_sade": "√211",
        "karekok_ondalik": 14.5258,
        "cift_mi": False,
    },
    212: {
        "sayi": 212,
        "karesi": 44944,
        "kupu": 9528128,
        "karekok_sade": "2√53",
        "karekok_ondalik": 14.5602,
        "cift_mi": True,
    },
    213: {
        "sayi": 213,
        "karesi": 45369,
        "kupu": 9663597,
        "karekok_sade": "√213",
        "karekok_ondalik": 14.5945,
        "cift_mi": False,
    },
    214: {
        "sayi": 214,
        "karesi": 45796,
        "kupu": 9800344,
        "karekok_sade": "√214",
        "karekok_ondalik": 14.6287,
        "cift_mi": True,
    },
    215: {
        "sayi": 215,
        "karesi": 46225,
        "kupu": 9938375,
        "karekok_sade": "√215",
        "karekok_ondalik": 14.6629,
        "cift_mi": False,
    },
    216: {
        "sayi": 216,
        "karesi": 46656,
        "kupu": 10077696,
        "karekok_sade": "6√6",
        "karekok_ondalik": 14.6969,
        "cift_mi": True,
    },
    217: {
        "sayi": 217,
        "karesi": 47089,
        "kupu": 10218313,
        "karekok_sade": "√217",
        "karekok_ondalik": 14.7309,
        "cift_mi": False,
    },
    218: {
        "sayi": 218,
        "karesi": 47524,
        "kupu": 10360232,
        "karekok_sade": "√218",
        "karekok_ondalik": 14.7648,
        "cift_mi": True,
    },
    219: {
        "sayi": 219,
        "karesi": 47961,
        "kupu": 10503459,
        "karekok_sade": "√219",
        "karekok_ondalik": 14.7986,
        "cift_mi": False,
    },
    220: {
        "sayi": 220,
        "karesi": 48400,
        "kupu": 10648000,
        "karekok_sade": "2√55",
        "karekok_ondalik": 14.8324,
        "cift_mi": True,
    },
    221: {
        "sayi": 221,
        "karesi": 48841,
        "kupu": 10793861,
        "karekok_sade": "√221",
        "karekok_ondalik": 14.8661,
        "cift_mi": False,
    },
    222: {
        "sayi": 222,
        "karesi": 49284,
        "kupu": 10941048,
        "karekok_sade": "√222",
        "karekok_ondalik": 14.8997,
        "cift_mi": True,
    },
    223: {
        "sayi": 223,
        "karesi": 49729,
        "kupu": 11089567,
        "karekok_sade": "√223",
        "karekok_ondalik": 14.9332,
        "cift_mi": False,
    },
    224: {
        "sayi": 224,
        "karesi": 50176,
        "kupu": 11239424,
        "karekok_sade": "4√14",
        "karekok_ondalik": 14.9666,
        "cift_mi": True,
    },
}

# ==============================================================================
# 3. GÜVENLİ AST İFADE HESAPLAYICI VE YARDIMCI MATEMATİK FONKSİYONLARI
# ==============================================================================
def guvenli_ifade_hesapla(ifade: str):
    """eval() kullanmadan AST ile güvenli matematiksel ifade hesaplar."""
    temiz = ifade.replace("^", "**").replace("×", "*").replace("÷", "/").replace(",", ".")
    agac = ast.parse(temiz, mode="eval")

    def _degerlendir(dugum):
        if isinstance(dugum, ast.Expression):
            return _degerlendir(dugum.body)
        if isinstance(dugum, ast.Constant) and isinstance(dugum.value, (int, float)):
            return dugum.value
        if isinstance(dugum, ast.UnaryOp) and type(dugum.op) in _IZINLI_OPERATORLER:
            return _IZINLI_OPERATORLER[type(dugum.op)](_degerlendir(dugum.operand))
        if isinstance(dugum, ast.BinOp) and type(dugum.op) in _IZINLI_OPERATORLER:
            sol = _degerlendir(dugum.left)
            sag = _degerlendir(dugum.right)
            if isinstance(dugum.op, ast.Pow) and abs(sag) > 1000:
                raise ValueError("Üs çok büyük.")
            return _IZINLI_OPERATORLER[type(dugum.op)](sol, sag)
        raise ValueError("Desteklenmeyen ifade")

    return _degerlendir(agac)


def sayi_formatla(val) -> str:
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    if isinstance(val, int):
        return f"{val:,}".replace(",", ".")
    return f"{val:,.4f}".rstrip("0").rstrip(".").replace(",", "X").replace(".", ",").replace("X", ".")


def karekok_sadelestir(n: int):
    """√n ifadesini a√b biçiminde sadeleştirir."""
    if n < 0:
        return None
    if n == 0:
        return 0, 1
    disari = 1
    iceri = n
    carpan = 2
    while carpan * carpan <= iceri:
        while iceri % (carpan * carpan) == 0:
            disari *= carpan
            iceri //= carpan * carpan
        carpan += 1
    return disari, iceri


def asal_carpanlara_ayir(n: int):
    carpanlar = {}
    d = 2
    kalan = n
    while d * d <= kalan:
        while kalan % d == 0:
            carpanlar[d] = carpanlar.get(d, 0) + 1
            kalan //= d
        d += 1
    if kalan > 1:
        carpanlar[kalan] = carpanlar.get(kalan, 0) + 1
    return carpanlar


def ikinci_derece_denklem_coz(a_katsayi: float, b_katsayi: float, c_katsayi: float) -> str:
    """ax² + bx + c = 0 denklemini diskriminant (Δ) adımlarıyla çözer."""
    if a_katsayi == 0:
        if b_katsayi == 0:
            return "⚠️ Geçersiz denklem (a ve b aynı anda 0 olamaz)."
        x = -c_katsayi / b_katsayi
        return f"📐 **1. Derece Denklem Çözümü:** `x = {sayi_formatla(x)}`"
    delta = (b_katsayi ** 2) - (4 * a_katsayi * c_katsayi)
    adim1 = f"1. **Diskriminant (Δ):** `Δ = b² - 4ac = ({b_katsayi})² - 4·({a_katsayi})·({c_katsayi}) = {sayi_formatla(delta)}`"
    if delta < 0:
        return f"📐 **2. Derece Denklem:**\n{adim1}\n2. **Sonuç:** `Δ < 0` olduğu için **reel kök yoktur** (karmaşık kök vardır)."
    if delta == 0:
        x_tek = -b_katsayi / (2 * a_katsayi)
        return f"📐 **2. Derece Denklem:**\n{adim1}\n2. **Çakışık Kök (`Δ = 0`):** **`x₁ = x₂ = {sayi_formatla(x_tek)}`**"
    kok_delta = math.sqrt(delta)
    x1 = (-b_katsayi + kok_delta) / (2 * a_katsayi)
    x2 = (-b_katsayi - kok_delta) / (2 * a_katsayi)
    return (
        f"📐 **2. Derece Denklem Çözümü:**\n"
        f"{adim1}\n"
        f"2. **Kökler (`x = (-b ± √Δ) / 2a`):** **`x₁ = {sayi_formatla(x1)}`** ve **`x₂ = {sayi_formatla(x2)}`**"
    )


def pisagor_hesapla(dik_kenar1: float, dik_kenar2: float) -> str:
    hipotenus = math.sqrt(dik_kenar1 ** 2 + dik_kenar2 ** 2)
    alan = (dik_kenar1 * dik_kenar2) / 2
    cevre = dik_kenar1 + dik_kenar2 + hipotenus
    return (
        f"📐 **Dik Üçgen & Pisagor Analizi:**\n"
        f"* **Hipotenüs (`c = √(a² + b²)`):** **`{sayi_formatla(hipotenus)}`**\n"
        f"* **Üçgenin Alanı:** **`{sayi_formatla(alan)}`** | **Çevresi:** **`{sayi_formatla(cevre)}`**"
    )


# ==============================================================================
# 4. ANA DOĞAL DİL MATEMATİK MOTORU
# ==============================================================================
def matematik_motoru_calistir(user_text: str):
    """Dört işlem, köklü/üslü sayılar, 1. ve 2. derece denklemler, EBOB/EKOK, yüzde, faktöriyel ve sözel geometri/fizik problemlerini çözer."""
    temiz_m = user_text.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()

    # 0) Profesyonel çekirdek: işlem önceliği, parantez, kesir, trigonometri, log,
    #    her biçimde 1./2. derece denklem, asal çarpan, yüzde artış/azalış.
    if _pro_matematik_coz is not None:
        try:
            pro_cevap, pro_etiket = _pro_matematik_coz(user_text)
            if pro_cevap:
                return pro_cevap, pro_etiket
        except Exception:
            pass  # çekirdek hata verirse eski kalıplarla devam et

    # 0-A) 2. Derece Denklem (ax^2 + bx + c = 0 veya ax² + bx + c = d)
    denk2_str = temiz_m.replace("²", "^2").replace(" ", "")
    if ("x^2" in denk2_str or "x**2" in denk2_str) and "=" in denk2_str:
        d2 = re.search(r"([+-]?\d*)x(?:\^2|\*\*2)([+-]\d*x)?([+-]\d+)?=([+-]?\d+)", denk2_str)
        if d2:
            a_s = d2.group(1)
            a_v = 1 if a_s in ("", "+") else (-1 if a_s == "-" else int(a_s))
            b_raw = d2.group(2) or ""
            if b_raw:
                b_s = b_raw.replace("x", "")
                b_v = 1 if b_s in ("", "+") else (-1 if b_s == "-" else int(b_s))
            else:
                b_v = 0
            c_sol = int(d2.group(3)) if d2.group(3) else 0
            c_sag = int(d2.group(4))
            c_v = c_sol - c_sag
            if a_v != 0:
                delta = b_v * b_v - 4 * a_v * c_v
                if delta > 0:
                    x1 = (-b_v + math.sqrt(delta)) / (2 * a_v)
                    x2 = (-b_v - math.sqrt(delta)) / (2 * a_v)
                    return (
                        f"📐 **2. Derece Denklem Çözümü:** `{user_text}`\n"
                        f"1. Adım (Katsayılar): `a = {a_v}, b = {b_v}, c = {c_v}`\n"
                        f"2. Adım (Diskriminant): `Δ = b² - 4ac = ({b_v})² - 4·({a_v})·({c_v}) = {delta}`\n"
                        f"3. Adım (Kökler): **`x₁ = {sayi_formatla(x1)}`** ve **`x₂ = {sayi_formatla(x2)}`**",
                        "2. Derece Denklem",
                    )
                elif delta == 0:
                    x0 = -b_v / (2 * a_v)
                    return (
                        f"📐 **2. Derece Denklem Çözümü:** `{user_text}`\n"
                        f"`Δ = 0` (Çift katlı kök) → **`x₁ = x₂ = {sayi_formatla(x0)}`**",
                        "2. Derece Denklem",
                    )
                else:
                    return (
                        f"📐 **2. Derece Denklem Çözümü:** `{user_text}`\n"
                        f"`Δ = {delta} < 0` olduğundan **gerçel (reel) kökü yoktur** (karmaşık kökler mevcuttur).",
                        "2. Derece Denklem",
                    )

    # 0-B) Sözel Problem 1: Hız - Zaman - Yol (x = v · t)
    hiz_m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:km|km/s|km/sa)?\s*h[ıi]zla\s*(\d+(?:[.,]\d+)?)\s*saat", temiz_m)
    if hiz_m:
        v = float(hiz_m.group(1).replace(",", "."))
        t = float(hiz_m.group(2).replace(",", "."))
        yol = v * t
        return (
            f"🚗 **Hız–Zaman–Yol Çözümü (`x = v · t`):**\n"
            f"• Hız (`v`) = `{sayi_formatla(v)} km/sa` | Süre (`t`) = `{sayi_formatla(t)} saat`\n"
            f"• Alınan Yol (`x`) = `{sayi_formatla(v)} × {sayi_formatla(t)}` = **`{sayi_formatla(yol)} km`**",
            "Sözel Problem: Yol-Hız",
        )

    # 0-C) Sözel Problem 2: Üçgen Alanı ((taban × yükseklik) / 2)
    if "üçgen" in temiz_m or "ucgen" in temiz_m:
        alan_m = re.search(r"taban[ıi]?\s*(\d+(?:[.,]\d+)?)[^\d]+y[üu]ksekli[ğg]i?\s*(\d+(?:[.,]\d+)?)", temiz_m)
        if alan_m and "alan" in temiz_m:
            taban = float(alan_m.group(1).replace(",", "."))
            yuk = float(alan_m.group(2).replace(",", "."))
            alan = (taban * yuk) / 2.0
            return (
                f"📐 **Üçgen Alanı Çözümü (`A = (taban × yükseklik) / 2`):**\n"
                f"• Taban = `{sayi_formatla(taban)}` | Yükseklik = `{sayi_formatla(yuk)}`\n"
                f"• Alan = `({sayi_formatla(taban)} × {sayi_formatla(yuk)}) / 2` = **`{sayi_formatla(alan)} br²`**",
                "Geometri: Üçgen Alanı",
            )
        hip_m = re.search(r"kenarlar[ıi]?\s*(\d+(?:[.,]\d+)?)[^\d]+(\d+(?:[.,]\d+)?)", temiz_m)
        if hip_m and ("hipoten" in temiz_m or "pisagor" in temiz_m or "dik" in temiz_m):
            k1 = float(hip_m.group(1).replace(",", "."))
            k2 = float(hip_m.group(2).replace(",", "."))
            hip = math.sqrt(k1 * k1 + k2 * k2)
            return (
                f"📐 **Pisagor Teoremi (`c = √(a² + b²)`):**\n"
                f"• Dik kenarlar: `a = {sayi_formatla(k1)}`, `b = {sayi_formatla(k2)}`\n"
                f"• Hipotenüs (`c`) = `√({sayi_formatla(k1)}² + {sayi_formatla(k2)}²) = √({sayi_formatla(k1*k1 + k2*k2)})` = **`{sayi_formatla(hip)}`**",
                "Geometri: Pisagor",
            )

    # 0-D) Türkçe Yazılı Yüzde ('200 ün yüzde 15 i' veya 'yüzde 20 si 500')
    yuzde_tr = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:'?(?:ün|un|ın|in|nin|nın|nun|nün))?\s*y[üu]zde\s*(\d+(?:[.,]\d+)?)", temiz_m)
    if yuzde_tr:
        ana = float(yuzde_tr.group(1).replace(",", "."))
        oran = float(yuzde_tr.group(2).replace(",", "."))
        return (
            f"💯 **Yüzde Hesabı:** `{sayi_formatla(ana)}` sayısının `%{sayi_formatla(oran)}`'i = `{sayi_formatla(ana)} × {sayi_formatla(oran)} / 100` = **`{sayi_formatla(ana * oran / 100)}`**",
            "Yüzde Hesabı",
        )

    # 0-E) EBOB / EKOK (Sayılar önce gelse bile: '12 ve 18 ebob ekok')
    ebob_ters = re.search(r"(\d+)\s*(?:ve|ile|,|\s)\s*(\d+)[^\d]*(ebob|ekok)", temiz_m)
    if ebob_ters:
        s1, s2 = int(ebob_ters.group(1)), int(ebob_ters.group(2))
        ebob_val = math.gcd(s1, s2)
        ekok_val = abs(s1 * s2) // ebob_val if s1 and s2 else 0
        return (
            f"🔢 **EBOB & EKOK ({s1}, {s2}):**\n"
            f"• **EBOB({s1}, {s2})** = **`{ebob_val}`**\n"
            f"• **EKOK({s1}, {s2})** = **`{ekok_val}`**",
            f"EBOB/EKOK({s1},{s2})",
        )

    # 0-F) Türkçe Yazılı Toplama / Çıkarma ('15 artı 27', '50 eksi 18')
    arti_m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(?:art[ıi]|topla)\s*(-?\d+(?:[.,]\d+)?)", temiz_m)
    if arti_m:
        a, b = float(arti_m.group(1).replace(",", ".")), float(arti_m.group(2).replace(",", "."))
        return f"➕ **Toplama:** `{sayi_formatla(a)} + {sayi_formatla(b)}` = **{sayi_formatla(a + b)}**", "Toplama İşlemi"
    eksi_m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(?:eksi|ç[ıi]kar|cikar)\s*(-?\d+(?:[.,]\d+)?)", temiz_m)
    if eksi_m:
        a, b = float(eksi_m.group(1).replace(",", ".")), float(eksi_m.group(2).replace(",", "."))
        return f"➖ **Çıkarma:** `{sayi_formatla(a)} - {sayi_formatla(b)}` = **{sayi_formatla(a - b)}**", "Çıkarma İşlemi"

    # 1) Karekök / Köklü Sayı
    kok_eslesme = re.search(r"(?:karekök|karekok|kök|kok|√)\s*(\d+)", user_text)
    if kok_eslesme:
        n = int(kok_eslesme.group(1))
        disari, iceri = karekok_sadelestir(n)
        yaklasik = math.sqrt(n)
        if iceri == 1:
            return (
                f"√ **Köklü Sayı Çözümü:** `√{n}` = **{disari}** (Tam kare sayı! Çünkü `{disari} × {disari} = {n}`)",
                f"Karekök: √{n}",
            )
        if disari == 1:
            return (
                f"√ **Köklü Sayı Çözümü:** `√{n}` kök dışına çıkmaz (`a√b` hali: **`√{n}`**), yaklaşık değeri **`{yaklasik:.4f}`**",
                f"Karekök: √{n}",
            )
        return (
            f"√ **Köklü Sayı Çözümü:** `√{n}` = `√({disari**2} × {iceri})` = **`{disari}√{iceri}`** (Yaklaşık: `{yaklasik:.4f}`)",
            f"Karekök: √{n}",
        )

    # 2) Faktöriyel
    fak_eslesme = re.search(r"(\d+)\s*(?:!|faktöriyel|faktoriyel)", user_text)
    if fak_eslesme:
        n = int(fak_eslesme.group(1))
        if n > 100:
            return "⚠️ Çok büyük faktöriyel! Lütfen 0 ile 100 arasında bir sayı gir.", "Matematik Sınırı"
        return f"❗ **Faktöriyel:** `{n}!` = **{sayi_formatla(math.factorial(n))}**", f"Faktöriyel: {n}!"

    # 3) EBOB / EKOK
    ebob_ekok = re.search(r"\b(ebob|ekok)\b[^\d]*(\d+)[^\d]+(\d+)", user_text)
    if ebob_ekok:
        tur, s1, s2 = ebob_ekok.group(1), int(ebob_ekok.group(2)), int(ebob_ekok.group(3))
        ebob_val = math.gcd(s1, s2)
        ekok_val = abs(s1 * s2) // ebob_val if s1 and s2 else 0
        if tur == "ebob":
            return f"🔢 **EBOB({s1}, {s2})** = **{ebob_val}** (EKOK: `{ekok_val}`)", f"EBOB({s1},{s2})"
        return f"🔢 **EKOK({s1}, {s2})** = **{ekok_val}** (EBOB: `{ebob_val}`)", f"EKOK({s1},{s2})"

    # 4) Asal Sayı / Asal Çarpanlar
    asal_eslesme = re.search(r"(\d+)\s*(?:asal mı|asal mi|asal çarpan|asal carpan)", user_text)
    if asal_eslesme:
        n = int(asal_eslesme.group(1))
        if n < 2:
            return f"ℹ️ `{n}` asal sayı değildir.", f"Asal Kontrolü: {n}"
        carpanlar = asal_carpanlara_ayir(n)
        if len(carpanlar) == 1 and list(carpanlar.values())[0] == 1:
            return f"✅ **`{n}` bir ASAL sayıdır!**", f"Asal: {n}"
        gosterim = " × ".join(f"{k}^{v}" if v > 1 else str(k) for k, v in carpanlar.items())
        return f"🧩 **`{n}` asal değildir.** Asal çarpanları: **`{gosterim}`**", f"Asal Çarpan: {n}"

    # 5) 1. Dereceden Denklem
    denklem_eslesme = re.search(r"([+-]?\s*\d*)\s*x\s*([+-]\s*\d+)?\s*=\s*([+-]?\s*\d+)", user_text.replace(" ", ""))
    if denklem_eslesme and "=" in user_text:
        a_str = denklem_eslesme.group(1)
        a_val = 1 if a_str in ("", "+") else (-1 if a_str == "-" else int(a_str))
        b_val = int(denklem_eslesme.group(2)) if denklem_eslesme.group(2) else 0
        c_val = int(denklem_eslesme.group(3))
        if a_val == 0:
            return "⚠️ `x` katsayısı 0 olamaz.", "Denklem Hatası"
        x_val = (c_val - b_val) / a_val
        return (
            f"📐 **Denklem Çözümü:** `{user_text}`\n"
            f"1. Adım: `{a_val}x = {c_val} - ({b_val})` → `{a_val}x = {c_val - b_val}`\n"
            f"2. Adım: `x = {c_val - b_val} / {a_val}` → **`x = {sayi_formatla(x_val)}`**",
            "Denklem Çözümü",
        )

    # 6) Yüzde Hesaplama
    yuzde1 = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:'?[uüıi]n)?\s*%\s*(\d+(?:[.,]\d+)?)", user_text)
    yuzde2 = re.search(r"%\s*(\d+(?:[.,]\d+)?)\s*(?:si|sı|su|sü)?\s*(\d+(?:[.,]\d+)?)", user_text)
    if yuzde1:
        ana, oran = float(yuzde1.group(1).replace(",", ".")), float(yuzde1.group(2).replace(",", "."))
        return f"💯 **Yüzde Hesabı:** `{sayi_formatla(ana)}` sayısının `%{sayi_formatla(oran)}`'i = **{sayi_formatla(ana * oran / 100)}**", "Yüzde Hesabı"
    if yuzde2:
        oran, ana = float(yuzde2.group(1).replace(",", ".")), float(yuzde2.group(2).replace(",", "."))
        return f"💯 **Yüzde Hesabı:** `{sayi_formatla(ana)}` sayısının `%{sayi_formatla(oran)}`'i = **{sayi_formatla(ana * oran / 100)}**", "Yüzde Hesabı"

    # 7) Üslü Sayılar
    us_eslesme = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:üzeri|uzeri|üssü|ussu|\^)\s*(-?\d+)", user_text)
    if us_eslesme:
        taban, us = float(us_eslesme.group(1).replace(",", ".")), int(us_eslesme.group(2))
        if abs(us) > 200:
            return "⚠️ Üs değeri çok büyük.", "Matematik Sınırı"
        return f"🔺 **Üslü Sayı:** `{sayi_formatla(taban)}^{us}` = **{sayi_formatla(taban ** us)}**", f"Üs: {taban}^{us}"

    kare_kup = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:'?[ıiuü]n)?\s*(karesi|küpü|kupu)", user_text)
    if kare_kup:
        taban = float(kare_kup.group(1).replace(",", "."))
        us = 2 if "kare" in kare_kup.group(2) else 3
        return f"🔺 **Üslü Sayı:** `{sayi_formatla(taban)}^{us}` = **{sayi_formatla(taban ** us)}**", f"Üs: {taban}^{us}"

    # 8-A) Türkçe Sonda Fiilli Dört İşlem ("12 ile 15'i çarp", "20 ile 30 topla", "100'ü 4'e böl", "50'den 15 çıkar")
    sonda_op = re.search(
        r"(-?\d+(?:[.,]\d+)?)(?:'?[a-zçğıöşü]+)?\s+(?:(?:ile|ve|den|dan|ten|tan)\s+)?(-?\d+(?:[.,]\d+)?)(?:'?[a-zçğıöşü]+)?\s+\b(çarp|carp|topla|böl|bol|çıkar|cikar)\b",
        user_text,
    )
    if sonda_op:
        s1 = float(sonda_op.group(1).replace(",", "."))
        s2 = float(sonda_op.group(2).replace(",", "."))
        fiil = sonda_op.group(3)
        if fiil in ("çarp", "carp"):
            return f"✖️ **Çarpma:** `{sayi_formatla(s1)} × {sayi_formatla(s2)}` = **{sayi_formatla(s1 * s2)}**", "Çarpma İşlemi"
        if fiil == "topla":
            return f"➕ **Toplama:** `{sayi_formatla(s1)} + {sayi_formatla(s2)}` = **{sayi_formatla(s1 + s2)}**", "Toplama İşlemi"
        if fiil in ("böl", "bol"):
            if s2 == 0:
                return "⚠️ Matematikte hiçbir sayı **0'a bölünemez** (Tanımsız)!", "Sıfıra Bölme"
            return f"➗ **Bölme:** `{sayi_formatla(s1)} ÷ {sayi_formatla(s2)}` = **{sayi_formatla(s1 / s2)}**", "Bölme İşlemi"
        if fiil in ("çıkar", "cikar"):
            return f"➖ **Çıkarma:** `{sayi_formatla(s1)} - {sayi_formatla(s2)}` = **{sayi_formatla(s1 - s2)}**", "Çıkarma İşlemi"

    # 8-B) Ortada Operatörlü Sözel ve Sembolik Dört İşlem ("76 çarpı 25", "76 x 25", "76 kere 25", "76*25 kaç eder")
    sozel_op = re.search(
        r"(-?\d+(?:[.,]\d+)?)\s*(?:ile)?\s*(çarpı|carpi|çarp|carp|kere|x|×|\*|bölü|bolu|böl|bol|/|÷|artı|arti|topla|\+|eksi|çıkar|cikar|-)\s*(-?\d+(?:[.,]\d+)?)",
        user_text,
    )
    if sozel_op:
        s1, op, s2 = float(sozel_op.group(1).replace(",", ".")), sozel_op.group(2), float(sozel_op.group(3).replace(",", "."))
        if op in ("çarpı", "carpi", "çarp", "carp", "kere", "x", "×", "*"):
            sonuc = s1 * s2
            ekstra = ""
            if s1.is_integer() and s2.is_integer() and 10 <= abs(s1) <= 999 and 10 <= abs(s2) <= 999:
                a_int, b_int = int(s1), int(s2)
                onluk, birlik = (b_int // 10) * 10, b_int % 10
                if birlik != 0:
                    ekstra = f"\n💡 *Zihinden Dağılma:* `({a_int} × {onluk}) + ({a_int} × {birlik}) = {sayi_formatla(a_int * onluk)} + {sayi_formatla(a_int * birlik)}`"
            return f"✖️ **Çarpma:** `{sayi_formatla(s1)} × {sayi_formatla(s2)}` = **{sayi_formatla(sonuc)}**{ekstra}", "Çarpma İşlemi"
        if op in ("böl", "bol", "bölü", "bolu", "/", "÷"):
            if s2 == 0:
                return "⚠️ Matematikte hiçbir sayı **0'a bölünemez** (Tanımsız)!", "Sıfıra Bölme"
            return f"➗ **Bölme:** `{sayi_formatla(s1)} ÷ {sayi_formatla(s2)}` = **{sayi_formatla(s1 / s2)}**", "Bölme İşlemi"
        if op in ("artı", "arti", "topla", "+"):
            return f"➕ **Toplama:** `{sayi_formatla(s1)} + {sayi_formatla(s2)}` = **{sayi_formatla(s1 + s2)}**", "Toplama İşlemi"
        if op in ("eksi", "çıkar", "cikar", "-"):
            return f"➖ **Çıkarma:** `{sayi_formatla(s1)} - {sayi_formatla(s2)}` = **{sayi_formatla(s1 - s2)}**", "Çıkarma İşlemi"

    # 9) Karmaşık İfade
    temiz_ifade = re.sub(r"\b(kaçtır|kactir|kaç|kac|eder|eşittir|esittir|sonucu|nedir)\b|[?=]", "", user_text).strip()
    if re.fullmatch(r"[\d\s+\-*/().^×÷,%]+", temiz_ifade) and any(op in temiz_ifade for op in "+-*/^×÷"):
        try:
            return f"⚡ **Hesap Motoru:** `{user_text}` = **{sayi_formatla(guvenli_ifade_hesapla(temiz_ifade))}**", "Karma İşlem"
        except ZeroDivisionError:
            return "⚠️ İşlemde sıfıra bölme hatası var!", "Sıfıra Bölme"
        except Exception:
            pass

    return None, None

# ==============================================================================
# 5. ADIM ADIM ÇÖZÜMLÜ MATEMATİK VE FİZİK SORU BANKASI (150 ÖRNEK PROBLEM)
# ==============================================================================
COZUMLU_SORU_BANKASI = [
    {
        "no": 1,
        "konu": "Köklü Sayılar",
        "soru": "`√27 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√27 = √(9×3) = 3√3` olduğundan `3√3 + 1√3 = 4√3` bulunur.",
        "cevap": "4√3",
    },
    {
        "no": 2,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 21` denkleminde `x` kaçtır?",
        "cozum": "`4x = 21 - 5 = 16` → `x = 16 / 4 = 4`.",
        "cevap": "4",
    },
    {
        "no": 3,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 4,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 5,
        "konu": "Köklü Sayılar",
        "soru": "`√147 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√147 = √(49×3) = 7√3` olduğundan `7√3 + 1√3 = 8√3` bulunur.",
        "cevap": "8√3",
    },
    {
        "no": 6,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 33` denkleminde `x` kaçtır?",
        "cozum": "`3x = 33 - 9 = 24` → `x = 24 / 3 = 8`.",
        "cevap": "8",
    },
    {
        "no": 7,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 8,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 9,
        "konu": "Köklü Sayılar",
        "soru": "`√12 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√12 = √(4×3) = 2√3` olduğundan `2√3 + 1√3 = 3√3` bulunur.",
        "cevap": "3√3",
    },
    {
        "no": 10,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 27` denkleminde `x` kaçtır?",
        "cozum": "`2x = 27 - 3 = 24` → `x = 24 / 2 = 12`.",
        "cevap": "12",
    },
    {
        "no": 11,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 12,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 13,
        "konu": "Köklü Sayılar",
        "soru": "`√108 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√108 = √(36×3) = 6√3` olduğundan `6√3 + 1√3 = 7√3` bulunur.",
        "cevap": "7√3",
    },
    {
        "no": 14,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 31` denkleminde `x` kaçtır?",
        "cozum": "`6x = 31 - 7 = 24` → `x = 24 / 6 = 4`.",
        "cevap": "4",
    },
    {
        "no": 15,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 16,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 17,
        "konu": "Köklü Sayılar",
        "soru": "`√300 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√300 = √(100×3) = 10√3` olduğundan `10√3 + 1√3 = 11√3` bulunur.",
        "cevap": "11√3",
    },
    {
        "no": 18,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 51` denkleminde `x` kaçtır?",
        "cozum": "`5x = 51 - 11 = 40` → `x = 40 / 5 = 8`.",
        "cevap": "8",
    },
    {
        "no": 19,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 20,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 21,
        "konu": "Köklü Sayılar",
        "soru": "`√75 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√75 = √(25×3) = 5√3` olduğundan `5√3 + 1√3 = 6√3` bulunur.",
        "cevap": "6√3",
    },
    {
        "no": 22,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 53` denkleminde `x` kaçtır?",
        "cozum": "`4x = 53 - 5 = 48` → `x = 48 / 4 = 12`.",
        "cevap": "12",
    },
    {
        "no": 23,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 24,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 25,
        "konu": "Köklü Sayılar",
        "soru": "`√243 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√243 = √(81×3) = 9√3` olduğundan `9√3 + 1√3 = 10√3` bulunur.",
        "cevap": "10√3",
    },
    {
        "no": 26,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 21` denkleminde `x` kaçtır?",
        "cozum": "`3x = 21 - 9 = 12` → `x = 12 / 3 = 4`.",
        "cevap": "4",
    },
    {
        "no": 27,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 28,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 29,
        "konu": "Köklü Sayılar",
        "soru": "`√48 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√48 = √(16×3) = 4√3` olduğundan `4√3 + 1√3 = 5√3` bulunur.",
        "cevap": "5√3",
    },
    {
        "no": 30,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 19` denkleminde `x` kaçtır?",
        "cozum": "`2x = 19 - 3 = 16` → `x = 16 / 2 = 8`.",
        "cevap": "8",
    },
    {
        "no": 31,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 32,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 33,
        "konu": "Köklü Sayılar",
        "soru": "`√192 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√192 = √(64×3) = 8√3` olduğundan `8√3 + 1√3 = 9√3` bulunur.",
        "cevap": "9√3",
    },
    {
        "no": 34,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 79` denkleminde `x` kaçtır?",
        "cozum": "`6x = 79 - 7 = 72` → `x = 72 / 6 = 12`.",
        "cevap": "12",
    },
    {
        "no": 35,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 36,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 37,
        "konu": "Köklü Sayılar",
        "soru": "`√27 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√27 = √(9×3) = 3√3` olduğundan `3√3 + 1√3 = 4√3` bulunur.",
        "cevap": "4√3",
    },
    {
        "no": 38,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 31` denkleminde `x` kaçtır?",
        "cozum": "`5x = 31 - 11 = 20` → `x = 20 / 5 = 4`.",
        "cevap": "4",
    },
    {
        "no": 39,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 40,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 41,
        "konu": "Köklü Sayılar",
        "soru": "`√147 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√147 = √(49×3) = 7√3` olduğundan `7√3 + 1√3 = 8√3` bulunur.",
        "cevap": "8√3",
    },
    {
        "no": 42,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 37` denkleminde `x` kaçtır?",
        "cozum": "`4x = 37 - 5 = 32` → `x = 32 / 4 = 8`.",
        "cevap": "8",
    },
    {
        "no": 43,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 44,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 45,
        "konu": "Köklü Sayılar",
        "soru": "`√12 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√12 = √(4×3) = 2√3` olduğundan `2√3 + 1√3 = 3√3` bulunur.",
        "cevap": "3√3",
    },
    {
        "no": 46,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 45` denkleminde `x` kaçtır?",
        "cozum": "`3x = 45 - 9 = 36` → `x = 36 / 3 = 12`.",
        "cevap": "12",
    },
    {
        "no": 47,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 48,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 49,
        "konu": "Köklü Sayılar",
        "soru": "`√108 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√108 = √(36×3) = 6√3` olduğundan `6√3 + 1√3 = 7√3` bulunur.",
        "cevap": "7√3",
    },
    {
        "no": 50,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 11` denkleminde `x` kaçtır?",
        "cozum": "`2x = 11 - 3 = 8` → `x = 8 / 2 = 4`.",
        "cevap": "4",
    },
    {
        "no": 51,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 52,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 53,
        "konu": "Köklü Sayılar",
        "soru": "`√300 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√300 = √(100×3) = 10√3` olduğundan `10√3 + 1√3 = 11√3` bulunur.",
        "cevap": "11√3",
    },
    {
        "no": 54,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 55` denkleminde `x` kaçtır?",
        "cozum": "`6x = 55 - 7 = 48` → `x = 48 / 6 = 8`.",
        "cevap": "8",
    },
    {
        "no": 55,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 56,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 57,
        "konu": "Köklü Sayılar",
        "soru": "`√75 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√75 = √(25×3) = 5√3` olduğundan `5√3 + 1√3 = 6√3` bulunur.",
        "cevap": "6√3",
    },
    {
        "no": 58,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 71` denkleminde `x` kaçtır?",
        "cozum": "`5x = 71 - 11 = 60` → `x = 60 / 5 = 12`.",
        "cevap": "12",
    },
    {
        "no": 59,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 60,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 61,
        "konu": "Köklü Sayılar",
        "soru": "`√243 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√243 = √(81×3) = 9√3` olduğundan `9√3 + 1√3 = 10√3` bulunur.",
        "cevap": "10√3",
    },
    {
        "no": 62,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 21` denkleminde `x` kaçtır?",
        "cozum": "`4x = 21 - 5 = 16` → `x = 16 / 4 = 4`.",
        "cevap": "4",
    },
    {
        "no": 63,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 64,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 65,
        "konu": "Köklü Sayılar",
        "soru": "`√48 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√48 = √(16×3) = 4√3` olduğundan `4√3 + 1√3 = 5√3` bulunur.",
        "cevap": "5√3",
    },
    {
        "no": 66,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 33` denkleminde `x` kaçtır?",
        "cozum": "`3x = 33 - 9 = 24` → `x = 24 / 3 = 8`.",
        "cevap": "8",
    },
    {
        "no": 67,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 68,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 69,
        "konu": "Köklü Sayılar",
        "soru": "`√192 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√192 = √(64×3) = 8√3` olduğundan `8√3 + 1√3 = 9√3` bulunur.",
        "cevap": "9√3",
    },
    {
        "no": 70,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 27` denkleminde `x` kaçtır?",
        "cozum": "`2x = 27 - 3 = 24` → `x = 24 / 2 = 12`.",
        "cevap": "12",
    },
    {
        "no": 71,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 72,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 73,
        "konu": "Köklü Sayılar",
        "soru": "`√27 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√27 = √(9×3) = 3√3` olduğundan `3√3 + 1√3 = 4√3` bulunur.",
        "cevap": "4√3",
    },
    {
        "no": 74,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 31` denkleminde `x` kaçtır?",
        "cozum": "`6x = 31 - 7 = 24` → `x = 24 / 6 = 4`.",
        "cevap": "4",
    },
    {
        "no": 75,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 76,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 77,
        "konu": "Köklü Sayılar",
        "soru": "`√147 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√147 = √(49×3) = 7√3` olduğundan `7√3 + 1√3 = 8√3` bulunur.",
        "cevap": "8√3",
    },
    {
        "no": 78,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 51` denkleminde `x` kaçtır?",
        "cozum": "`5x = 51 - 11 = 40` → `x = 40 / 5 = 8`.",
        "cevap": "8",
    },
    {
        "no": 79,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 80,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 81,
        "konu": "Köklü Sayılar",
        "soru": "`√12 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√12 = √(4×3) = 2√3` olduğundan `2√3 + 1√3 = 3√3` bulunur.",
        "cevap": "3√3",
    },
    {
        "no": 82,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 53` denkleminde `x` kaçtır?",
        "cozum": "`4x = 53 - 5 = 48` → `x = 48 / 4 = 12`.",
        "cevap": "12",
    },
    {
        "no": 83,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 84,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 85,
        "konu": "Köklü Sayılar",
        "soru": "`√108 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√108 = √(36×3) = 6√3` olduğundan `6√3 + 1√3 = 7√3` bulunur.",
        "cevap": "7√3",
    },
    {
        "no": 86,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 21` denkleminde `x` kaçtır?",
        "cozum": "`3x = 21 - 9 = 12` → `x = 12 / 3 = 4`.",
        "cevap": "4",
    },
    {
        "no": 87,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 88,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 89,
        "konu": "Köklü Sayılar",
        "soru": "`√300 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√300 = √(100×3) = 10√3` olduğundan `10√3 + 1√3 = 11√3` bulunur.",
        "cevap": "11√3",
    },
    {
        "no": 90,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 19` denkleminde `x` kaçtır?",
        "cozum": "`2x = 19 - 3 = 16` → `x = 16 / 2 = 8`.",
        "cevap": "8",
    },
    {
        "no": 91,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 92,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 93,
        "konu": "Köklü Sayılar",
        "soru": "`√75 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√75 = √(25×3) = 5√3` olduğundan `5√3 + 1√3 = 6√3` bulunur.",
        "cevap": "6√3",
    },
    {
        "no": 94,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 79` denkleminde `x` kaçtır?",
        "cozum": "`6x = 79 - 7 = 72` → `x = 72 / 6 = 12`.",
        "cevap": "12",
    },
    {
        "no": 95,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 96,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 97,
        "konu": "Köklü Sayılar",
        "soru": "`√243 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√243 = √(81×3) = 9√3` olduğundan `9√3 + 1√3 = 10√3` bulunur.",
        "cevap": "10√3",
    },
    {
        "no": 98,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 31` denkleminde `x` kaçtır?",
        "cozum": "`5x = 31 - 11 = 20` → `x = 20 / 5 = 4`.",
        "cevap": "4",
    },
    {
        "no": 99,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 100,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 101,
        "konu": "Köklü Sayılar",
        "soru": "`√48 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√48 = √(16×3) = 4√3` olduğundan `4√3 + 1√3 = 5√3` bulunur.",
        "cevap": "5√3",
    },
    {
        "no": 102,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 37` denkleminde `x` kaçtır?",
        "cozum": "`4x = 37 - 5 = 32` → `x = 32 / 4 = 8`.",
        "cevap": "8",
    },
    {
        "no": 103,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 104,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 105,
        "konu": "Köklü Sayılar",
        "soru": "`√192 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√192 = √(64×3) = 8√3` olduğundan `8√3 + 1√3 = 9√3` bulunur.",
        "cevap": "9√3",
    },
    {
        "no": 106,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 45` denkleminde `x` kaçtır?",
        "cozum": "`3x = 45 - 9 = 36` → `x = 36 / 3 = 12`.",
        "cevap": "12",
    },
    {
        "no": 107,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 108,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 109,
        "konu": "Köklü Sayılar",
        "soru": "`√27 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√27 = √(9×3) = 3√3` olduğundan `3√3 + 1√3 = 4√3` bulunur.",
        "cevap": "4√3",
    },
    {
        "no": 110,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 11` denkleminde `x` kaçtır?",
        "cozum": "`2x = 11 - 3 = 8` → `x = 8 / 2 = 4`.",
        "cevap": "4",
    },
    {
        "no": 111,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 112,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 113,
        "konu": "Köklü Sayılar",
        "soru": "`√147 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√147 = √(49×3) = 7√3` olduğundan `7√3 + 1√3 = 8√3` bulunur.",
        "cevap": "8√3",
    },
    {
        "no": 114,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 55` denkleminde `x` kaçtır?",
        "cozum": "`6x = 55 - 7 = 48` → `x = 48 / 6 = 8`.",
        "cevap": "8",
    },
    {
        "no": 115,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 116,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 117,
        "konu": "Köklü Sayılar",
        "soru": "`√12 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√12 = √(4×3) = 2√3` olduğundan `2√3 + 1√3 = 3√3` bulunur.",
        "cevap": "3√3",
    },
    {
        "no": 118,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 71` denkleminde `x` kaçtır?",
        "cozum": "`5x = 71 - 11 = 60` → `x = 60 / 5 = 12`.",
        "cevap": "12",
    },
    {
        "no": 119,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 120,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 121,
        "konu": "Köklü Sayılar",
        "soru": "`√108 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√108 = √(36×3) = 6√3` olduğundan `6√3 + 1√3 = 7√3` bulunur.",
        "cevap": "7√3",
    },
    {
        "no": 122,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 21` denkleminde `x` kaçtır?",
        "cozum": "`4x = 21 - 5 = 16` → `x = 16 / 4 = 4`.",
        "cevap": "4",
    },
    {
        "no": 123,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 124,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 125,
        "konu": "Köklü Sayılar",
        "soru": "`√300 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√300 = √(100×3) = 10√3` olduğundan `10√3 + 1√3 = 11√3` bulunur.",
        "cevap": "11√3",
    },
    {
        "no": 126,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 33` denkleminde `x` kaçtır?",
        "cozum": "`3x = 33 - 9 = 24` → `x = 24 / 3 = 8`.",
        "cevap": "8",
    },
    {
        "no": 127,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 128,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 129,
        "konu": "Köklü Sayılar",
        "soru": "`√75 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√75 = √(25×3) = 5√3` olduğundan `5√3 + 1√3 = 6√3` bulunur.",
        "cevap": "6√3",
    },
    {
        "no": 130,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 27` denkleminde `x` kaçtır?",
        "cozum": "`2x = 27 - 3 = 24` → `x = 24 / 2 = 12`.",
        "cevap": "12",
    },
    {
        "no": 131,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 132,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 133,
        "konu": "Köklü Sayılar",
        "soru": "`√243 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√243 = √(81×3) = 9√3` olduğundan `9√3 + 1√3 = 10√3` bulunur.",
        "cevap": "10√3",
    },
    {
        "no": 134,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 31` denkleminde `x` kaçtır?",
        "cozum": "`6x = 31 - 7 = 24` → `x = 24 / 6 = 4`.",
        "cevap": "4",
    },
    {
        "no": 135,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 136,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 137,
        "konu": "Köklü Sayılar",
        "soru": "`√48 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√48 = √(16×3) = 4√3` olduğundan `4√3 + 1√3 = 5√3` bulunur.",
        "cevap": "5√3",
    },
    {
        "no": 138,
        "konu": "1. Derece Denklemler",
        "soru": "`5x + 11 = 51` denkleminde `x` kaçtır?",
        "cozum": "`5x = 51 - 11 = 40` → `x = 40 / 5 = 8`.",
        "cevap": "8",
    },
    {
        "no": 139,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 140,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 141,
        "konu": "Köklü Sayılar",
        "soru": "`√192 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√192 = √(64×3) = 8√3` olduğundan `8√3 + 1√3 = 9√3` bulunur.",
        "cevap": "9√3",
    },
    {
        "no": 142,
        "konu": "1. Derece Denklemler",
        "soru": "`4x + 5 = 53` denkleminde `x` kaçtır?",
        "cozum": "`4x = 53 - 5 = 48` → `x = 48 / 4 = 12`.",
        "cevap": "12",
    },
    {
        "no": 143,
        "konu": "Üslü Sayılar",
        "soru": "`5^4 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(4+2) = 5^6 = 15625`.",
        "cevap": "15625",
    },
    {
        "no": 144,
        "konu": "EBOB - EKOK",
        "soru": "`12` ve `18` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 145,
        "konu": "Köklü Sayılar",
        "soru": "`√27 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√27 = √(9×3) = 3√3` olduğundan `3√3 + 1√3 = 4√3` bulunur.",
        "cevap": "4√3",
    },
    {
        "no": 146,
        "konu": "1. Derece Denklemler",
        "soru": "`3x + 9 = 21` denkleminde `x` kaçtır?",
        "cozum": "`3x = 21 - 9 = 12` → `x = 12 / 3 = 4`.",
        "cevap": "4",
    },
    {
        "no": 147,
        "konu": "Üslü Sayılar",
        "soru": "`5^2 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(2+2) = 5^4 = 625`.",
        "cevap": "625",
    },
    {
        "no": 148,
        "konu": "EBOB - EKOK",
        "soru": "`36` ve `42` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 149,
        "konu": "Köklü Sayılar",
        "soru": "`√147 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√147 = √(49×3) = 7√3` olduğundan `7√3 + 1√3 = 8√3` bulunur.",
        "cevap": "8√3",
    },
    {
        "no": 150,
        "konu": "1. Derece Denklemler",
        "soru": "`2x + 3 = 19` denkleminde `x` kaçtır?",
        "cozum": "`2x = 19 - 3 = 16` → `x = 16 / 2 = 8`.",
        "cevap": "8",
    },
    {
        "no": 151,
        "konu": "Üslü Sayılar",
        "soru": "`5^3 × 5^2` işleminin sonucu kaçtır?",
        "cozum": "Tabanlar aynı olduğu için üsler toplanır: `5^(3+2) = 5^5 = 3125`.",
        "cevap": "3125",
    },
    {
        "no": 152,
        "konu": "EBOB - EKOK",
        "soru": "`24` ve `30` sayılarının EBOB'u kaçtır?",
        "cozum": "Her iki sayıyı da tam bölen en büyük ortak tam sayı `6`'dir.",
        "cevap": "6",
    },
    {
        "no": 153,
        "konu": "Köklü Sayılar",
        "soru": "`√12 + √3` işleminin en sade sonucu nedir?",
        "cozum": "`√12 = √(4×3) = 2√3` olduğundan `2√3 + 1√3 = 3√3` bulunur.",
        "cevap": "3√3",
    },
    {
        "no": 154,
        "konu": "1. Derece Denklemler",
        "soru": "`6x + 7 = 79` denkleminde `x` kaçtır?",
        "cozum": "`6x = 79 - 7 = 72` → `x = 72 / 6 = 12`.",
        "cevap": "12",
    },
]




# ==============================================================================
# v13.0 — GENİŞLETİLMİŞ 9. SINIF & TYT MATEMATİK SORU BANKASI (+100 BENZERSİZ SORU -> 254 SORU)
# ==============================================================================
def _v13_ek_sorulari_uret():
    ek = [
        # Mantık & Önermeler (155-166)
        ("Mantık & Önermeler", "`p ≡ 1` ve `q ≡ 0` iken `(p ∧ q) ∨ p` bileşik önermesinin doğruluk değeri kaçtır?", "`1 ∧ 0 ≡ 0`, ardından `0 ∨ 1 ≡ 1` bulunur.", "1"),
        ("Mantık & Önermeler", "`p ≡ 1` ve `q ≡ 0` iken `p ⇒ q` koşullu önermesinin doğruluk değeri kaçtır?", "Koşullu önermede yalnızca `1 ⇒ 0 ≡ 0` olur.", "0"),
        ("Mantık & Önermeler", "`p ≡ 0` ve `q ≡ 0` iken `p ⇔ q` iki yönlü koşullu önermesinin değeri kaçtır?", "İki önerme aynı doğruluk değerine sahipse `0 ⇔ 0 ≡ 1` olur.", "1"),
        ("Mantık & Önermeler", "`(1 ⇒ 0) ∨ (0 ⇒ 1)` bileşik önermesinin doğruluk değeri kaçtır?", "`1 ⇒ 0 ≡ 0` ve `0 ⇒ 1 ≡ 1` olduğundan `0 ∨ 1 ≡ 1`.", "1"),
        ("Mantık & Önermeler", "4 farklı önermenin doğruluk tablosunda kaç farklı durum vardır?", "`n` önerme için `2^n` durum vardır: `2^4 = 16`.", "16"),
        ("Mantık & Önermeler", "`(p ∧ p') ∨ 1` önermesinin en sade doğruluk değeri kaçtır?", "`p ∧ p' ≡ 0` ve `0 ∨ 1 ≡ 1` (totoloji).", "1"),
        ("Mantık & Önermeler", "`(p ∨ p') ∧ 0` önermesinin en sade doğruluk değeri kaçtır?", "`p ∨ p' ≡ 1` ve `1 ∧ 0 ≡ 0` (çelişki).", "0"),
        ("Mantık & Önermeler", "`(0 ⇒ 0) ∧ (1 ⇔ 1)` önermesinin doğruluk değeri kaçtır?", "`0 ⇒ 0 ≡ 1` ve `1 ⇔ 1 ≡ 1`, `1 ∧ 1 ≡ 1`.", "1"),
        ("Mantık & Önermeler", "`(p ⇒ q)'` ifadesinin `p ≡ 1, q ≡ 1` için doğruluk değeri kaçtır?", "`1 ⇒ 1 ≡ 1`, değili `1' ≡ 0`.", "0"),
        ("Mantık & Önermeler", "5 farklı önermenin doğruluk tablosunda kaç satır bulunur?", "`2^5 = 32` satır bulunur.", "32"),
        # Kümeler (165-176)
        ("Kümeler", "5 elemanlı bir kümenin kaç tane alt kümesi vardır?", "`n` elemanlı kümenin alt küme sayısı `2^n = 2^5 = 32`.", "32"),
        ("Kümeler", "4 elemanlı bir kümenin kaç tane öz alt kümesi vardır?", "Öz alt küme sayısı `2^n - 1 = 2^4 - 1 = 15`.", "15"),
        ("Kümeler", "`s(A) = 12`, `s(B) = 9` ve `s(A ∩ B) = 4` ise `s(A ∪ B)` kaçtır?", "`s(A ∪ B) = s(A) + s(B) - s(A ∩ B) = 12 + 9 - 4 = 17`.", "17"),
        ("Kümeler", "`s(A) = 6` ve `s(B) = 5` ise `A × B` kartezyen çarpım kümesi kaç elemanlıdır?", "`s(A × B) = s(A) · s(B) = 6 · 5 = 30`.", "30"),
        ("Kümeler", "Alt küme sayısı 64 olan bir kümenin eleman sayısı kaçtır?", "`2^n = 64 = 2^6` olduğundan `n = 6`.", "6"),
        ("Kümeler", "`s(A \ B) = 7`, `s(A ∩ B) = 5` ve `s(B \ A) = 6` ise `s(A ∪ B)` kaçtır?", "Üç ayrık bölgenin toplamı `7 + 5 + 6 = 18`.", "18"),
        ("Kümeler", "6 elemanlı bir kümenin boş küme dışındaki alt küme sayısı kaçtır?", "`2^6 - 1 = 64 - 1 = 63`.", "63"),
        ("Kümeler", "`A = {1, 2, 3, 4, 5}` kümesinin 2 elemanlı kaç alt kümesi vardır?", "Kombinasyon `C(5,2) = (5×4)/2 = 10`.", "10"),
        ("Kümeler", "`s(A ∪ B) = 25`, `s(A) = 15`, `s(B) = 16` ise `s(A ∩ B)` kaçtır?", "`s(A ∩ B) = 15 + 16 - 25 = 6`.", "6"),
        ("Kümeler", "3 elemanlı bir kümenin alt küme sayısı ile öz alt küme sayısının toplamı kaçtır?", "`2^3 = 8` ve `2^3 - 1 = 7`, toplam `8 + 7 = 15`.", "15"),
        # Üslü Sayılar (175-186)
        ("Üslü Sayılar", "`2^5 · 2^3 / 2^4` işleminin sonucu kaçtır?", "`2^(5+3-4) = 2^4 = 16`.", "16"),
        ("Üslü Sayılar", "`3^4 + 3^4 + 3^4` toplamı `3^x` ise `x` kaçtır?", "`3 · 3^4 = 3^5` olduğundan `x = 5`.", "5"),
        ("Üslü Sayılar", "`(2^3)^2 - 4^2` işleminin sonucu kaçtır?", "`2^6 - 16 = 64 - 16 = 48`.", "48"),
        ("Üslü Sayılar", "`5^0 + 5^1 + 5^2` toplamı kaçtır?", "`1 + 5 + 25 = 31`.", "31"),
        ("Üslü Sayılar", "`8^4 / 4^5` işleminin sonucu kaçtır?", "`(2^3)^4 / (2^2)^5 = 2^12 / 2^10 = 2^2 = 4`.", "4"),
        ("Üslü Sayılar", "`2^x = 32` ve `3^y = 27` ise `x + y` kaçtır?", "`x = 5`, `y = 3` olduğundan `x + y = 8`.", "8"),
        ("Üslü Sayılar", "`(1/2)^(-3) + (1/3)^(-2)` işleminin sonucu kaçtır?", "`2^3 + 3^2 = 8 + 9 = 17`.", "17"),
        ("Üslü Sayılar", "`9^3 / 27^2` işleminin sonucu kaçtır?", "`(3^2)^3 / (3^3)^2 = 3^6 / 3^6 = 1`.", "1"),
        ("Üslü Sayılar", "`2^10` sayısının yarısı `2^k` ise `k` kaçtır?", "`2^10 / 2^1 = 2^9` olduğundan `k = 9`.", "9"),
        ("Üslü Sayılar", "`(-2)^4 + (-3)^3` işleminin sonucu kaçtır?", "`16 + (-27) = -11`.", "-11"),
        # Mutlak Değer & Eşitsizlikler (185-196)
        ("Mutlak Değer & Eşitsizlikler", "`|-7| + |3 - 8|` işleminin sonucu kaçtır?", "`7 + |-5| = 7 + 5 = 12`.", "12"),
        ("Mutlak Değer & Eşitsizlikler", "`|x - 4| = 6` denklemini sağlayan `x` değerlerinin toplamı kaçtır?", "`x - 4 = 6 ⇒ x = 10` ve `x - 4 = -6 ⇒ x = -2`; toplam `10 + (-2) = 8`.", "8"),
        ("Mutlak Değer & Eşitsizlikler", "`2x - 5 < 11` eşitsizliğini sağlayan en büyük tam sayı kaçtır?", "`2x < 16 ⇒ x < 8` olduğundan en büyük tam sayı `7`.", "7"),
        ("Mutlak Değer & Eşitsizlikler", "`|2x + 1| = 9` denkleminin pozitif kökü kaçtır?", "`2x + 1 = 9 ⇒ 2x = 8 ⇒ x = 4`.", "4"),
        ("Mutlak Değer & Eşitsizlikler", "`-3 ≤ x < 5` aralığında kaç tane tam sayı vardır?", "`-3, -2, -1, 0, 1, 2, 3, 4` olmak üzere `8` tam sayı vardır.", "8"),
        ("Mutlak Değer & Eşitsizlikler", "`|x - 5| ≤ 2` eşitsizliğini sağlayan tam sayıların toplamı kaçtır?", "`3 ≤ x ≤ 7` olduğundan `3 + 4 + 5 + 6 + 7 = 25`.", "25"),
        ("Mutlak Değer & Eşitsizlikler", "`3x + 4 ≥ 19` eşitsizliğini sağlayan en küçük tam sayı kaçtır?", "`3x ≥ 15 ⇒ x ≥ 5` olduğundan en küçük tam sayı `5`.", "5"),
        ("Mutlak Değer & Eşitsizlikler", "`|-12| / |-3| + |-5|` işleminin sonucu kaçtır?", "`12 / 3 + 5 = 4 + 5 = 9`.", "9"),
        ("Mutlak Değer & Eşitsizlikler", "`|x + 3| = 0` denkleminin kökü kaçtır?", "Mutlak değeri 0 yapan tek değer `x + 3 = 0 ⇒ x = -3`.", "-3"),
        ("Mutlak Değer & Eşitsizlikler", "`5 - x > 2` eşitsizliğini sağlayan en büyük tam sayı kaçtır?", "`3 > x` olduğundan en büyük tam sayı `2`.", "2"),
        # Oran-Orantı & Yüzde-Kâr-Zarar (195-206)
        ("Oran-Orantı & Yüzde", "`240` sayısının `%25`'i kaçtır?", "`240 × 25 / 100 = 60`.", "60"),
        ("Oran-Orantı & Yüzde", "`400 TL`'lik bir ürüne `%15` indirim yapılırsa yeni fiyatı kaç TL olur?", "İndirim `400 × 15 / 100 = 60 TL`, yeni fiyat `400 - 60 = 340`.", "340"),
        ("Oran-Orantı & Yüzde", "`%20` kârla `360 TL`'ye satılan ürünün maliyeti kaç TL'dir?", "`120% = 360` ise `100% = 360 × 100 / 120 = 300`.", "300"),
        ("Oran-Orantı & Yüzde", "`a / b = 3 / 5` ve `a + b = 64` ise `a` kaçtır?", "`3k + 5k = 8k = 64 ⇒ k = 8 ⇒ a = 3×8 = 24`.", "24"),
        ("Oran-Orantı & Yüzde", "6 işçi bir işi 10 günde bitiriyorsa, aynı hızda 15 işçi kaç günde bitirir?", "Ters orantı: `6 × 10 = 15 × x ⇒ x = 60 / 15 = 4`.", "4"),
        ("Oran-Orantı & Yüzde", "`80` sayısının yüzde kaçı `20`'dir?", "`(20 / 80) × 100 = 25`.", "25"),
        ("Oran-Orantı & Yüzde", "Bir araç 4 saatte 360 km yol gidiyorsa, aynı hızla 7 saatte kaç km gider?", "Hız `360 / 4 = 90 km/sa`, 7 saatte `90 × 7 = 630`.", "630"),
        ("Oran-Orantı & Yüzde", "`500 TL`'lik ürün önce `%20` zamlanıp sonra `%20` indirilirse son fiyatı kaç TL olur?", "`500 → 600 → 600 × 0.8 = 480`.", "480"),
        ("Oran-Orantı & Yüzde", "`x : y = 2 : 7` ve `y - x = 35` ise `y` kaçtır?", "`7k - 2k = 5k = 35 ⇒ k = 7 ⇒ y = 49`.", "49"),
        ("Oran-Orantı & Yüzde", "30 kişilik sınıfta 18 kız öğrenci varsa kızların yüzdesi kaçtır?", "`(18 / 30) × 100 = 60`.", "60"),
        # Fonksiyonlar (205-216)
        ("Fonksiyonlar", "`f(x) = 3x - 4` ise `f(5)` kaçtır?", "`f(5) = 3(5) - 4 = 15 - 4 = 11`.", "11"),
        ("Fonksiyonlar", "`f(x) = 2x + 7` ve `f(a) = 19` ise `a` kaçtır?", "`2a + 7 = 19 ⇒ 2a = 12 ⇒ a = 6`.", "6"),
        ("Fonksiyonlar", "`f(x) = x^2 - 3x + 2` ise `f(4)` kaçtır?", "`4^2 - 3(4) + 2 = 16 - 12 + 2 = 6`.", "6"),
        ("Fonksiyonlar", "`f(x) = 2x + 1` ve `g(x) = x - 3` ise `(f ∘ g)(5)` kaçtır?", "`g(5) = 2`, `f(2) = 2(2) + 1 = 5`.", "5"),
        ("Fonksiyonlar", "`f(x) = 4x - 8` fonksiyonunun sıfırı (kökü) kaçtır?", "`4x - 8 = 0 ⇒ x = 2`.", "2"),
        ("Fonksiyonlar", "`f(x) = 5x + 2` ise `f⁻¹(17)` kaçtır?", "`5x + 2 = 17 ⇒ 5x = 15 ⇒ x = 3`.", "3"),
        ("Fonksiyonlar", "`f(x) = 7` sabit fonksiyonu için `f(2026) + f(-5)` kaçtır?", "Sabit fonksiyon her değerde 7 verir: `7 + 7 = 14`.", "14"),
        ("Fonksiyonlar", "`f(2x - 1) = 6x + 5` ise `f(3)` kaçtır?", "`2x - 1 = 3 ⇒ x = 2`, `f(3) = 6(2) + 5 = 17`.", "17"),
        ("Fonksiyonlar", "`f(x) = x` birim fonksiyonu için `f(12) + f(8)` kaçtır?", "Birim fonksiyon girdiyi aynen verir: `12 + 8 = 20`.", "20"),
        ("Fonksiyonlar", "`f(x) = 3x + 1` ve `g(x) = 2x` ise `(g ∘ f)(2)` kaçtır?", "`f(2) = 7`, `g(7) = 14`.", "14"),
        # Üçgenler & Geometri (215-228)
        ("Üçgenler & Geometri", "İki iç açısı `48°` ve `67°` olan üçgenin üçüncü iç açısı kaç derecedir?", "`180 - (48 + 67) = 180 - 115 = 65`.", "65"),
        ("Üçgenler & Geometri", "Dik kenarları `5 cm` ve `12 cm` olan dik üçgenin hipotenüsü kaç cm'dir?", "5-12-13 özel dik üçgeni: `√(25 + 144) = 13`.", "13"),
        ("Üçgenler & Geometri", "Dik kenarları `8 cm` ve `15 cm` olan dik üçgenin hipotenüsü kaç cm'dir?", "8-15-17 özel dik üçgeni: `√(64 + 225) = 17`.", "17"),
        ("Üçgenler & Geometri", "Tabanı `14 cm` ve bu tabana ait yüksekliği `9 cm` olan üçgenin alanı kaç `cm²`'dir?", "Alan = `(14 × 9) / 2 = 63`.", "63"),
        ("Üçgenler & Geometri", "Tepe açısı `40°` olan ikizkenar üçgenin taban açılarından biri kaç derecedir?", "`(180 - 40) / 2 = 70`.", "70"),
        ("Üçgenler & Geometri", "Bir kenarı `6 cm` olan eşkenar üçgenin çevresi kaç cm'dir?", "`3 × 6 = 18`.", "18"),
        ("Üçgenler & Geometri", "Kenarları `7 cm` ve `10 cm` olan üçgenin 3. kenarının alabileceği en büyük tam sayı değeri kaçtır?", "Üçgen eşitsizliği: `x < 7 + 10 = 17` olduğundan en büyük tam sayı `16`.", "16"),
        ("Üçgenler & Geometri", "İç açıları `2 : 3 : 4` oranında olan üçgenin en büyük açısı kaç derecedir?", "`9k = 180 ⇒ k = 20`, en büyük açı `4 × 20 = 80`.", "80"),
        ("Üçgenler & Geometri", "Hipotenüsü `25 cm` ve bir dik kenarı `7 cm` olan dik üçgenin diğer dik kenarı kaç cm'dir?", "7-24-25 özel üçgeni: `√(625 - 49) = 24`.", "24"),
        ("Üçgenler & Geometri", "Benzerlik oranı `2/3` olan iki üçgenin alanları oranı `4/k` ise `k` kaçtır?", "Alanlar oranı benzerlik oranının karesidir: `(2/3)^2 = 4/9 ⇒ k = 9`.", "9"),
        # Polinomlar & Özdeşlikler (225-238)
        ("Polinomlar & Özdeşlikler", "`53^2 - 47^2` işleminin sonucu kaçtır?", "İki kare farkı: `(53 - 47)(53 + 47) = 6 × 100 = 600`.", "600"),
        ("Polinomlar & Özdeşlikler", "`a + b = 9` ve `a · b = 14` ise `a^2 + b^2` kaçtır?", "`(a+b)^2 - 2ab = 81 - 28 = 53`.", "53"),
        ("Polinomlar & Özdeşlikler", "`P(x) = 2x^3 - x + 5` polinomunun sabit terimi kaçtır?", "Sabit terim `P(0) = 5`.", "5"),
        ("Polinomlar & Özdeşlikler", "`P(x) = 3x^2 - 4x + 7` polinomunun katsayılar toplamı kaçtır?", "Katsayılar toplamı `P(1) = 3 - 4 + 7 = 6`.", "6"),
        ("Polinomlar & Özdeşlikler", "`x - y = 5` ve `x · y = 6` ise `x^2 + y^2` kaçtır?", "`(x-y)^2 + 2xy = 25 + 12 = 37`.", "37"),
        ("Polinomlar & Özdeşlikler", "`101^2 - 99^2` işleminin sonucu kaçtır?", "`(101 - 99)(101 + 99) = 2 × 200 = 400`.", "400"),
        ("Polinomlar & Özdeşlikler", "`P(x) = x^2 + 4x + 4` ise `P(8)` kaçtır?", "`P(x) = (x + 2)^2 ⇒ P(8) = 10^2 = 100`.", "100"),
        ("Polinomlar & Özdeşlikler", "`x^2 - 9 = 0` denkleminin pozitif kökü kaçtır?", "`(x-3)(x+3) = 0` olduğundan pozitif kök `3`.", "3"),
        ("Polinomlar & Özdeşlikler", "`(x + 3)^2 = x^2 + ax + 9` özdeşliğinde `a` kaçtır?", "`(x+3)^2 = x^2 + 6x + 9` olduğundan `a = 6`.", "6"),
        ("Polinomlar & Özdeşlikler", "`P(x) = x^3 - 2x^2 + 3` polinomunun `x - 2` ile bölümünden kalan kaçtır?", "Kalan `P(2) = 8 - 8 + 3 = 3`.", "3"),
        # Olasılık & Veri Analizi (235-254)
        ("Olasılık & Veri", "Hilesiz bir zar atıldığında üst yüze asal sayı gelme olasılığı yüzde kaçtır?", "Asal sayılar `{2, 3, 5}` (3/6 = 1/2 = `%50`).", "50"),
        ("Olasılık & Veri", "`12, 18, 24, 26` sayılarının aritmetik ortalaması kaçtır?", "`(12 + 18 + 24 + 26) / 4 = 80 / 4 = 20`.", "20"),
        ("Olasılık & Veri", "`4, 7, 9, 13, 21` veri grubunun ortancası (medyanı) kaçtır?", "Sıralı 5 verinin tam ortasındaki sayı `9`.", "9"),
        ("Olasılık & Veri", "Bir torbada 4 kırmızı ve 6 mavi top vardır. Rastgele çekilen topun kırmızı olma olasılığı `a/5` ise `a` kaçtır?", "`4 / 10 = 2 / 5` olduğundan `a = 2`.", "2"),
        ("Olasılık & Veri", "İki madeni para aynı anda atıldığında örnek uzay kaç elemanlıdır?", "`2 × 2 = 4` (YY, YT, TY, TT).", "4"),
        ("Olasılık & Veri", "3 farklı gömlek ve 4 farklı pantolon kaç farklı şekilde kombinlenebilir?", "Saymanın temel ilkesi: `3 × 4 = 12`.", "12"),
        ("Olasılık & Veri", "`5!` (5 faktöriyel) değeri kaçtır?", "`5 × 4 × 3 × 2 × 1 = 120`.", "120"),
        ("Olasılık & Veri", "`6! / 4!` işleminin sonucu kaçtır?", "`6 × 5 = 30`.", "30"),
        ("Olasılık & Veri", "`10, 14, 14, 18, 22` veri grubunun tepe değeri (modu) kaçtır?", "En çok tekrar eden değer `14`.", "14"),
        ("Olasılık & Veri", "Bir sınıfta 5 sınavdan ortalama 84 alan öğrencinin toplam puanı kaçtır?", "`5 × 84 = 420`.", "420"),
        # Ek Problem & Denklem Çeşitliliği (245-254)
        ("Sözel Problemler", "Ardışık 3 tek tam sayının toplamı `57` ise en büyük sayı kaçtır?", "Ortanca sayı `57 / 3 = 19`, en büyük sayı `19 + 2 = 21`.", "21"),
        ("Sözel Problemler", "Bir babanın yaşı oğlunun yaşının 4 katıdır. Yaşları toplamı 50 ise oğul kaç yaşındadır?", "`4x + x = 5x = 50 ⇒ x = 10`.", "10"),
        ("Sözel Problemler", "Hangi sayının 3 katının 7 fazlası 40 eder?", "`3x + 7 = 40 ⇒ 3x = 33 ⇒ x = 11`.", "11"),
        ("Sözel Problemler", "Bir kitabın önce `1/3`'ünü sonra `1/6`'sını okuyan öğrencinin okumadığı kısım `60` sayfa ise kitap kaç sayfadır?", "Okunan `1/3 + 1/6 = 1/2`, kalan `1/2 = 60 ⇒ 120` sayfa.", "120"),
        ("Sözel Problemler", "Bir telin ucundan `1/5`'i kesildiğinde orta noktası `6 cm` kayıyorsa telin ilk uzunluğu kaç cm'dir?", "Kesilen parça `2 × 6 = 12 cm`, tamamı `12 × 5 = 60`.", "60"),
        ("Sözel Problemler", "Aralarında 360 km bulunan iki araç 40 km/sa ve 50 km/sa hızla birbirine doğru hareket ederse kaç saat sonra karşılaşırlar?", "`360 / (40 + 50) = 360 / 90 = 4` saat.", "4"),
        ("Sözel Problemler", "Bir musluk boş havuzu 6 saatte, diğeri 12 saatte dolduruyorsa ikisi birlikte kaç saatte doldurur?", "`1/6 + 1/12 = 3/12 = 1/4` olduğundan `4` saatte.", "4"),
        ("Sözel Problemler", "Bir sınıfta öğrenciler sıralara 2'şerli oturursa 6 öğrenci ayakta kalıyor, 3'erli oturursa 2 sıra boş kalıyor. Sınıfta kaç sıra vardır?", "`2x + 6 = 3(x - 2) ⇒ 2x + 6 = 3x - 6 ⇒ x = 12`.", "12"),
        ("Sözel Problemler", "Tuz oranı `%20` olan `60 g` tuzlu suya `40 g` saf su eklenirse yeni tuz yüzdesi kaç olur?", "Tuz `12 g`, toplam karışım `100 g` ⇒ `%12`.", "12"),
        ("Sözel Problemler", "Bir karenin bir kenarı `%10` artırılırsa alanı yüzde kaç artar?", "`1.1 × 1.1 = 1.21` olduğundan alan `%21` artar.", "21"),
    ]
    bas_no = len(COZUMLU_SORU_BANKASI) + 1
    sonuc = []
    for i, (konu, soru, cozum, cevap) in enumerate(ek):
        sonuc.append({
            "no": bas_no + i,
            "konu": konu,
            "soru": soru,
            "cozum": cozum,
            "cevap": cevap,
        })
    return sonuc

COZUMLU_SORU_BANKASI.extend(_v13_ek_sorulari_uret())


def matematik_studyosu_goster(sesli_soyle_fn):
    """v13.0 — Premium Matematik Stüdyosu (254+ Çözümlü Soru, Konu Filtreli Kartlar & Canlı Quiz)."""
    toplam_soru = len(COZUMLU_SORU_BANKASI)
    tum_konular = sorted({s["konu"] for s in COZUMLU_SORU_BANKASI})

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#0b132b 0%,#162447 55%,#1e3a5f 100%);
                    border:1px solid rgba(56,189,248,0.28);border-radius:18px;
                    padding:18px 22px;margin-bottom:14px;
                    box-shadow:0 10px 26px rgba(2,6,23,0.42);">
            <div style="font-size:11.5px;letter-spacing:1.5px;color:#38bdf8;font-weight:700;text-transform:uppercase;">
                AREX MATEMATİK & GEOMETRİ LABORATUVARI
            </div>
            <div style="font-size:23px;font-weight:800;color:#f8fafc;margin-top:2px;">
                🧮 İnteraktif Matematik Stüdyosu
            </div>
            <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;font-size:12.5px;color:#cbd5e1;">
                <span>📚 <b>{len(MATEMATIK_KONU_REHBERI)}</b> Konu Rehberi</span>
                <span>•</span>
                <span>📖 <b>{toplam_soru}</b> Çözümlü Soru</span>
                <span>•</span>
                <span>🏷️ <b>{len(tum_konular)}</b> Kategori</span>
                <span>•</span>
                <span>⚡ Canlı Denklem & Geometri Çözücü</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.tabs([
        "📚 Konu Anlatımları",
        "⚡ Çözücü & Geometri",
        f"📖 {toplam_soru} Çözümlü Soru",
        "🎯 Canlı Test & Seri",
    ])

    with t1:
        secili_konu = st.selectbox("Öğrenmek İstediğin Konuyu Seç:", list(MATEMATIK_KONU_REHBERI.keys()), key="mat_konu_sec_v13")
        k_veri = MATEMATIK_KONU_REHBERI[secili_konu]
        st.markdown(
            bilgi_karti_olustur(secili_konu, f"📘 {k_veri['alt_baslik']}", k_veri["icerik"].replace("\n", "<br>")),
            unsafe_allow_html=True,
        )
        if st.button("🔊 Bu Konuyu Sesli Anlat", key="mat_sesli_v13"):
            sesli_soyle_fn(k_veri["icerik"], dil="tr")

    with t2:
        c_m1, c_m2, c_m3 = st.columns(3, gap="medium")
        with c_m1:
            st.markdown("#### √ Karekök (`a√b`) & Referans")
            kok_n = st.number_input("Sayı gir:", min_value=1, max_value=1000000, value=72, step=1, key="mat_kok_v13")
            dis, ic = karekok_sadelestir(int(kok_n))
            if ic == 1:
                st.success(f"`√{kok_n}` = **{dis}** (Tam Kare)")
            else:
                st.success(f"`√{kok_n}` = **`{dis if dis > 1 else ''}√{ic}`** (`{math.sqrt(kok_n):.4f}`)")
            if int(kok_n) in MATEMATIK_REFERANS_TABLOSU:
                ref = MATEMATIK_REFERANS_TABLOSU[int(kok_n)]
                st.info(f"**Karesi:** `{ref['karesi']}` | **Küpü:** `{ref['kupu']}`")

        with c_m2:
            st.markdown("#### 📐 2. Derece Denklem (`ax²+bx+c=0`)")
            da = st.number_input("a katsayısı:", value=1.0, step=1.0, key="mat_da_v13")
            db = st.number_input("b katsayısı:", value=-5.0, step=1.0, key="mat_db_v13")
            dc = st.number_input("c sabiti:", value=6.0, step=1.0, key="mat_dc_v13")
            st.markdown(ikinci_derece_denklem_coz(da, db, dc))

        with c_m3:
            st.markdown("#### 📏 Pisagor & Dik Üçgen")
            k_a = st.number_input("1. Dik Kenar (a):", min_value=1.0, value=6.0, step=1.0, key="mat_ka_v13")
            k_b = st.number_input("2. Dik Kenar (b):", min_value=1.0, value=8.0, step=1.0, key="mat_kb_v13")
            st.markdown(pisagor_hesapla(k_a, k_b))

    with t3:
        f_col1, f_col2 = st.columns([1.1, 1.3])
        with f_col1:
            sec_kat = st.selectbox("🏷️ Konuya Göre Filtrele:", ["Tümü"] + tum_konular, key="mat_soru_kat_v13")
        filtreli = COZUMLU_SORU_BANKASI if sec_kat == "Tümü" else [s for s in COZUMLU_SORU_BANKASI if s["konu"] == sec_kat]
        with f_col2:
            if len(filtreli) > 1:
                sec_idx = st.slider(f"Soru Seç (1 - {len(filtreli)}):", 1, len(filtreli), 1, key="mat_soru_sl_v13") - 1
            else:
                sec_idx = 0
        s_obj = filtreli[sec_idx]
        st.markdown(
            f"""
            <div style="background:linear-gradient(155deg,#0f172a,#1e293b);
                        border:1px solid rgba(56,189,248,0.32);border-radius:16px;
                        padding:18px 20px;margin-top:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <span style="font-size:12px;font-weight:700;color:#38bdf8;letter-spacing:0.6px;">
                        SORU #{s_obj['no']} • {s_obj['konu'].upper()}
                    </span>
                    <span style="background:rgba(34,197,94,0.18);color:#4ade80;border:1px solid rgba(34,197,94,0.38);
                                 border-radius:99px;padding:3px 12px;font-size:12px;font-weight:700;">
                        Doğru Cevap: {s_obj['cevap']}
                    </span>
                </div>
                <div style="font-size:16px;color:#f8fafc;margin-top:12px;line-height:1.55;">
                    <b>Soru:</b> {s_obj['soru']}
                </div>
                <div style="background:rgba(15,23,42,0.7);border-left:3px solid #38bdf8;
                            border-radius:8px;padding:12px 14px;margin-top:14px;color:#cbd5e1;font-size:14px;">
                    <b>💡 Adım Adım Çözüm:</b> {s_obj['cozum']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t4:
        if "quiz_dogru" not in st.session_state:
            st.session_state["quiz_dogru"] = 0
        if "quiz_yanlis" not in st.session_state:
            st.session_state["quiz_yanlis"] = 0
        if "quiz_seri" not in st.session_state:
            st.session_state["quiz_seri"] = 0

        q_k1, q_k2, q_k3, q_k4 = st.columns(4)
        q_k1.metric("⭐ Puan", st.session_state.get("quiz_puan", 0))
        q_k2.metric("✅ Doğru", st.session_state["quiz_dogru"])
        q_k3.metric("❌ Yanlış", st.session_state["quiz_yanlis"])
        q_k4.metric("🔥 Seri", f"{st.session_state['quiz_seri']}x")

        q_kat = st.selectbox("🎯 Test Konusu:", ["Karışık (Tüm 254 Soru)"] + tum_konular, key="quiz_kat_v13")
        q_havuz = COZUMLU_SORU_BANKASI if q_kat.startswith("Karışık") else [s for s in COZUMLU_SORU_BANKASI if s["konu"] == q_kat]

        if st.button("🎲 Yeni Test Sorusu Getir", use_container_width=True, key="quiz_yeni_v13") or st.session_state.quiz_soru is None:
            rast = random.choice(q_havuz)
            st.session_state.quiz_soru = (rast["soru"], rast["cevap"], rast["cozum"], rast["konu"])

        q_pack = st.session_state.quiz_soru
        q_soru, q_cevap, q_cozum = q_pack[0], q_pack[1], q_pack[2]
        q_konu_ad = q_pack[3] if len(q_pack) > 3 else "Matematik"

        st.markdown(
            f"""
            <div style="background:rgba(15,23,42,0.88);border:1px solid rgba(56,189,248,0.3);
                        border-radius:14px;padding:16px 18px;margin:10px 0;">
                <div style="font-size:11.5px;color:#38bdf8;font-weight:700;text-transform:uppercase;">{q_konu_ad}</div>
                <div style="font-size:16px;color:#f8fafc;margin-top:6px;">{q_soru}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        k_yanit = st.text_input("Cevabın:", key="canli_quiz_girdi_v13", placeholder="Örn: 12 veya 3√3")
        if st.button("✅ Cevabı Kontrol Et", use_container_width=True, key="quiz_kontrol_v13"):
            if k_yanit.strip().replace(" ", "").lower() == q_cevap.replace(" ", "").lower():
                st.session_state.quiz_puan += 10
                st.session_state["quiz_dogru"] += 1
                st.session_state["quiz_seri"] += 1
                st.success(f"🎉 Harika Ahmet! Doğru cevap: **{q_cevap}** (+10 Puan | 🔥 {st.session_state['quiz_seri']}x Seri)")
            else:
                st.session_state["quiz_yanlis"] += 1
                st.session_state["quiz_seri"] = 0
                st.error(f"❌ Doğru cevap: **{q_cevap}** | Çözüm: {q_cozum}")
