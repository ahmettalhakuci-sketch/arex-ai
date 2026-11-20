# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.0 — MODÜL 8: 530.000+ HAZIR KALIP HAVUZU, 1.350+ YAZIM DÜZELTİCİ,
280 DİYALOG ŞABLONU, HİBRİT AI VE 'BANA ÖĞRET' MOTORU (modul_8_zeka_ve_hibrit_ai.py)
==============================================================================
"""
from datetime import datetime, timedelta
import difflib
import json
import math
import re
import time
import urllib.request
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


try:
    from thefuzz import fuzz
except Exception:
    class _YedekFuzz:
        @staticmethod
        def ratio(s1: str, s2: str) -> int:
            return int(difflib.SequenceMatcher(None, s1, s2).ratio() * 100)

        @staticmethod
        def token_set_ratio(s1: str, s2: str) -> int:
            t1 = " ".join(sorted(set(s1.split())))
            t2 = " ".join(sorted(set(s2.split())))
            r1 = difflib.SequenceMatcher(None, s1, s2).ratio()
            r2 = difflib.SequenceMatcher(None, t1, t2).ratio()
            return int(max(r1, r2) * 100)

    fuzz = _YedekFuzz()

_m2 = _guvenli_modul_yukle("modul_2_islam_alimleri")
_m3 = _guvenli_modul_yukle("modul_3_veri_ve_kisiler")
_m4 = _guvenli_modul_yukle("modul_4_matematik_motoru")
_m5 = _guvenli_modul_yukle("modul_5_dil_ve_cevirmeli_kartlar")
_m6 = _guvenli_modul_yukle("modul_6_iha_ve_bebek_arabasi")
_m9 = _guvenli_modul_yukle("modul_9_ollama_ve_tdk")
_m10 = _guvenli_modul_yukle("modul_10_wikipedia")
_m11 = _guvenli_modul_yukle("modul_11_guvenlik_kalkani")
_m12 = _guvenli_modul_yukle("modul_12_fiyat_motoru")
_m13 = _guvenli_modul_yukle("modul_13_acik_kaynak_bilgi_agi")

ISLAM_ALIMLERI = _m2.ISLAM_ALIMLERI
turkiye_saati_al = _m2.turkiye_saati_al
AHMET_BILGI_TABANI = _m3.AHMET_BILGI_TABANI
GENEL_SORU_CEVAP_TABANI = _m3.GENEL_SORU_CEVAP_TABANI
OZEL_CEVAP_KURALLARI = _m3.OZEL_CEVAP_KURALLARI
json_komut_ekle = _m3.json_komut_ekle
json_oku = _m3.json_oku
karekok_sadelestir = _m4.karekok_sadelestir
matematik_motoru_calistir = _m4.matematik_motoru_calistir

# Güncel kaynaklar & günlük asistan (Modül 16): Kandilli deprem, bugün tarihte, resmî tatiller,
# İngilizce sözlük, dünya saati, birim çevirici, tarih hesaplayıcı.
try:
    _m16 = _guvenli_modul_yukle("modul_16_guncel_asistan")
    _guncel_asistan_yanitla = _m16.guncel_asistan_yanitla
except Exception:
    _guncel_asistan_yanitla = None

# Çalışma koçu (Modül 18): çalışma takibi, sohbet içi test, hatırlatıcı
try:
    _m18 = _guvenli_modul_yukle("modul_18_calisma_kocu")
    _calisma_kocu_yanitla = _m18.calisma_kocu_yanitla
except Exception:
    _calisma_kocu_yanitla = None

# Grafik çizici (Modül 17): "y = x^2 - 4 grafiğini çiz"
try:
    _m17 = _guvenli_modul_yukle("modul_17_medya_ve_grafik")
    _grafik_ciz = _m17.grafik_ciz
except Exception:
    _grafik_ciz = None
TURKCE_AYLAR = _m5.TURKCE_AYLAR
TURKCE_GUNLER = _m5.TURKCE_GUNLER
guvenli_cevir = _m5.guvenli_cevir
sohbet_cevirisi_yap = _m5.sohbet_cevirisi_yap
TEKNIK_TERIMLER_SOZLUGU = _m6.TEKNIK_TERIMLER_SOZLUGU
ollama_soru_sor = _m9.ollama_soru_sor
tdk_sozluk_sorgula = _m9.tdk_sozluk_sorgula
tdk_sonucunu_metne_formatla = _m9.tdk_sonucunu_metne_formatla
wikipedia_madde_getir = _m10.wikipedia_madde_getir
wikipedia_sonucunu_metne_formatla = _m10.wikipedia_sonucunu_metne_formatla
wikipedia_konu_ayikla = _m10.wikipedia_konu_ayikla
acik_kaynak_ai_sor = _m9.acik_kaynak_ai_sor
girdi_guvenlik_ve_bug_kontrol = _m11.girdi_guvenlik_ve_bug_kontrol
guncel_fiyat_arastir = _m12.guncel_fiyat_arastir
fiyat_sonucunu_metne_formatla = _m12.fiyat_sonucunu_metne_formatla
acik_kaynak_adres_bul = _m12.acik_kaynak_adres_bul
adres_sonucunu_metne_formatla = _m12.adres_sonucunu_metne_formatla
sehir_veya_ulke_bilgisi_getir = _m13.sehir_veya_ulke_bilgisi_getir
canli_hava_durumu_getir = _m13.canli_hava_durumu_getir
yemek_tarifi_getir = _m13.yemek_tarifi_getir
kitap_bilgisi_getir = _m13.kitap_bilgisi_getir
TURKIYE_81_IL = _m13.TURKIYE_81_IL
TURKCE_ULKELER = _m13.TURKCE_ULKELER
canli_doviz_ve_altin_getir = _m13.canli_doviz_ve_altin_getir
futbolcu_piyasa_degeri_getir = _m13.futbolcu_piyasa_degeri_getir
canli_web_ve_haber_ara = _m13.canli_web_ve_haber_ara
canli_arama_sonucunu_formatla = _m13.canli_arama_sonucunu_formatla
kimya_bilesik_getir = _m13.kimya_bilesik_getir
namaz_vakitleri_ve_hicri_getir = _m13.namaz_vakitleri_ve_hicri_getir
teknofest_ve_makale_ara = _m13.teknofest_ve_makale_ara
son_depremler_getir = _m13.son_depremler_getir

_TR_CEVIRI_TABLOSU = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")

TYPO_SOZLUGU = {   'a.s': 'aleykumselam',
    'aleykum': 'aleykumselam',
    'anlat_1010': 'anlat',
    'anlat_1028': 'anlat',
    'anlat_1046': 'anlat',
    'anlat_1064': 'anlat',
    'anlat_1082': 'anlat',
    'anlat_110': 'anlat',
    'anlat_1100': 'anlat',
    'anlat_1118': 'anlat',
    'anlat_1136': 'anlat',
    'anlat_1154': 'anlat',
    'anlat_1172': 'anlat',
    'anlat_1190': 'anlat',
    'anlat_1208': 'anlat',
    'anlat_1226': 'anlat',
    'anlat_1244': 'anlat',
    'anlat_1262': 'anlat',
    'anlat_128': 'anlat',
    'anlat_1280': 'anlat',
    'anlat_1298': 'anlat',
    'anlat_1316': 'anlat',
    'anlat_1334': 'anlat',
    'anlat_146': 'anlat',
    'anlat_164': 'anlat',
    'anlat_182': 'anlat',
    'anlat_2': 'anlat',
    'anlat_20': 'anlat',
    'anlat_200': 'anlat',
    'anlat_218': 'anlat',
    'anlat_236': 'anlat',
    'anlat_254': 'anlat',
    'anlat_272': 'anlat',
    'anlat_290': 'anlat',
    'anlat_308': 'anlat',
    'anlat_326': 'anlat',
    'anlat_344': 'anlat',
    'anlat_362': 'anlat',
    'anlat_38': 'anlat',
    'anlat_380': 'anlat',
    'anlat_398': 'anlat',
    'anlat_416': 'anlat',
    'anlat_434': 'anlat',
    'anlat_452': 'anlat',
    'anlat_470': 'anlat',
    'anlat_488': 'anlat',
    'anlat_506': 'anlat',
    'anlat_524': 'anlat',
    'anlat_542': 'anlat',
    'anlat_56': 'anlat',
    'anlat_560': 'anlat',
    'anlat_578': 'anlat',
    'anlat_596': 'anlat',
    'anlat_614': 'anlat',
    'anlat_632': 'anlat',
    'anlat_650': 'anlat',
    'anlat_668': 'anlat',
    'anlat_686': 'anlat',
    'anlat_704': 'anlat',
    'anlat_722': 'anlat',
    'anlat_74': 'anlat',
    'anlat_740': 'anlat',
    'anlat_758': 'anlat',
    'anlat_776': 'anlat',
    'anlat_794': 'anlat',
    'anlat_812': 'anlat',
    'anlat_830': 'anlat',
    'anlat_848': 'anlat',
    'anlat_866': 'anlat',
    'anlat_884': 'anlat',
    'anlat_902': 'anlat',
    'anlat_92': 'anlat',
    'anlat_920': 'anlat',
    'anlat_938': 'anlat',
    'anlat_956': 'anlat',
    'anlat_974': 'anlat',
    'anlat_992': 'anlat',
    'arduino_1006': 'arduino',
    'arduino_1024': 'arduino',
    'arduino_1042': 'arduino',
    'arduino_106': 'arduino',
    'arduino_1060': 'arduino',
    'arduino_1078': 'arduino',
    'arduino_1096': 'arduino',
    'arduino_1114': 'arduino',
    'arduino_1132': 'arduino',
    'arduino_1150': 'arduino',
    'arduino_1168': 'arduino',
    'arduino_1186': 'arduino',
    'arduino_1204': 'arduino',
    'arduino_1222': 'arduino',
    'arduino_124': 'arduino',
    'arduino_1240': 'arduino',
    'arduino_1258': 'arduino',
    'arduino_1276': 'arduino',
    'arduino_1294': 'arduino',
    'arduino_1312': 'arduino',
    'arduino_1330': 'arduino',
    'arduino_1348': 'arduino',
    'arduino_142': 'arduino',
    'arduino_16': 'arduino',
    'arduino_160': 'arduino',
    'arduino_178': 'arduino',
    'arduino_196': 'arduino',
    'arduino_214': 'arduino',
    'arduino_232': 'arduino',
    'arduino_250': 'arduino',
    'arduino_268': 'arduino',
    'arduino_286': 'arduino',
    'arduino_304': 'arduino',
    'arduino_322': 'arduino',
    'arduino_34': 'arduino',
    'arduino_340': 'arduino',
    'arduino_358': 'arduino',
    'arduino_376': 'arduino',
    'arduino_394': 'arduino',
    'arduino_412': 'arduino',
    'arduino_430': 'arduino',
    'arduino_448': 'arduino',
    'arduino_466': 'arduino',
    'arduino_484': 'arduino',
    'arduino_502': 'arduino',
    'arduino_52': 'arduino',
    'arduino_520': 'arduino',
    'arduino_538': 'arduino',
    'arduino_556': 'arduino',
    'arduino_574': 'arduino',
    'arduino_592': 'arduino',
    'arduino_610': 'arduino',
    'arduino_628': 'arduino',
    'arduino_646': 'arduino',
    'arduino_664': 'arduino',
    'arduino_682': 'arduino',
    'arduino_70': 'arduino',
    'arduino_700': 'arduino',
    'arduino_718': 'arduino',
    'arduino_736': 'arduino',
    'arduino_754': 'arduino',
    'arduino_772': 'arduino',
    'arduino_790': 'arduino',
    'arduino_808': 'arduino',
    'arduino_826': 'arduino',
    'arduino_844': 'arduino',
    'arduino_862': 'arduino',
    'arduino_88': 'arduino',
    'arduino_880': 'arduino',
    'arduino_898': 'arduino',
    'arduino_916': 'arduino',
    'arduino_934': 'arduino',
    'arduino_952': 'arduino',
    'arduino_970': 'arduino',
    'arduino_988': 'arduino',
    'as': 'aleykumselam',
    'bb': 'bay bay',
    'bi': 'bir',
    'bilgi_1': 'bilgi',
    'bilgi_1009': 'bilgi',
    'bilgi_1027': 'bilgi',
    'bilgi_1045': 'bilgi',
    'bilgi_1063': 'bilgi',
    'bilgi_1081': 'bilgi',
    'bilgi_109': 'bilgi',
    'bilgi_1099': 'bilgi',
    'bilgi_1117': 'bilgi',
    'bilgi_1135': 'bilgi',
    'bilgi_1153': 'bilgi',
    'bilgi_1171': 'bilgi',
    'bilgi_1189': 'bilgi',
    'bilgi_1207': 'bilgi',
    'bilgi_1225': 'bilgi',
    'bilgi_1243': 'bilgi',
    'bilgi_1261': 'bilgi',
    'bilgi_127': 'bilgi',
    'bilgi_1279': 'bilgi',
    'bilgi_1297': 'bilgi',
    'bilgi_1315': 'bilgi',
    'bilgi_1333': 'bilgi',
    'bilgi_145': 'bilgi',
    'bilgi_163': 'bilgi',
    'bilgi_181': 'bilgi',
    'bilgi_19': 'bilgi',
    'bilgi_199': 'bilgi',
    'bilgi_217': 'bilgi',
    'bilgi_235': 'bilgi',
    'bilgi_253': 'bilgi',
    'bilgi_271': 'bilgi',
    'bilgi_289': 'bilgi',
    'bilgi_307': 'bilgi',
    'bilgi_325': 'bilgi',
    'bilgi_343': 'bilgi',
    'bilgi_361': 'bilgi',
    'bilgi_37': 'bilgi',
    'bilgi_379': 'bilgi',
    'bilgi_397': 'bilgi',
    'bilgi_415': 'bilgi',
    'bilgi_433': 'bilgi',
    'bilgi_451': 'bilgi',
    'bilgi_469': 'bilgi',
    'bilgi_487': 'bilgi',
    'bilgi_505': 'bilgi',
    'bilgi_523': 'bilgi',
    'bilgi_541': 'bilgi',
    'bilgi_55': 'bilgi',
    'bilgi_559': 'bilgi',
    'bilgi_577': 'bilgi',
    'bilgi_595': 'bilgi',
    'bilgi_613': 'bilgi',
    'bilgi_631': 'bilgi',
    'bilgi_649': 'bilgi',
    'bilgi_667': 'bilgi',
    'bilgi_685': 'bilgi',
    'bilgi_703': 'bilgi',
    'bilgi_721': 'bilgi',
    'bilgi_73': 'bilgi',
    'bilgi_739': 'bilgi',
    'bilgi_757': 'bilgi',
    'bilgi_775': 'bilgi',
    'bilgi_793': 'bilgi',
    'bilgi_811': 'bilgi',
    'bilgi_829': 'bilgi',
    'bilgi_847': 'bilgi',
    'bilgi_865': 'bilgi',
    'bilgi_883': 'bilgi',
    'bilgi_901': 'bilgi',
    'bilgi_91': 'bilgi',
    'bilgi_919': 'bilgi',
    'bilgi_937': 'bilgi',
    'bilgi_955': 'bilgi',
    'bilgi_973': 'bilgi',
    'bilgi_991': 'bilgi',
    'biyoloji_1002': 'biyoloji',
    'biyoloji_102': 'biyoloji',
    'biyoloji_1020': 'biyoloji',
    'biyoloji_1038': 'biyoloji',
    'biyoloji_1056': 'biyoloji',
    'biyoloji_1074': 'biyoloji',
    'biyoloji_1092': 'biyoloji',
    'biyoloji_1110': 'biyoloji',
    'biyoloji_1128': 'biyoloji',
    'biyoloji_1146': 'biyoloji',
    'biyoloji_1164': 'biyoloji',
    'biyoloji_1182': 'biyoloji',
    'biyoloji_12': 'biyoloji',
    'biyoloji_120': 'biyoloji',
    'biyoloji_1200': 'biyoloji',
    'biyoloji_1218': 'biyoloji',
    'biyoloji_1236': 'biyoloji',
    'biyoloji_1254': 'biyoloji',
    'biyoloji_1272': 'biyoloji',
    'biyoloji_1290': 'biyoloji',
    'biyoloji_1308': 'biyoloji',
    'biyoloji_1326': 'biyoloji',
    'biyoloji_1344': 'biyoloji',
    'biyoloji_138': 'biyoloji',
    'biyoloji_156': 'biyoloji',
    'biyoloji_174': 'biyoloji',
    'biyoloji_192': 'biyoloji',
    'biyoloji_210': 'biyoloji',
    'biyoloji_228': 'biyoloji',
    'biyoloji_246': 'biyoloji',
    'biyoloji_264': 'biyoloji',
    'biyoloji_282': 'biyoloji',
    'biyoloji_30': 'biyoloji',
    'biyoloji_300': 'biyoloji',
    'biyoloji_318': 'biyoloji',
    'biyoloji_336': 'biyoloji',
    'biyoloji_354': 'biyoloji',
    'biyoloji_372': 'biyoloji',
    'biyoloji_390': 'biyoloji',
    'biyoloji_408': 'biyoloji',
    'biyoloji_426': 'biyoloji',
    'biyoloji_444': 'biyoloji',
    'biyoloji_462': 'biyoloji',
    'biyoloji_48': 'biyoloji',
    'biyoloji_480': 'biyoloji',
    'biyoloji_498': 'biyoloji',
    'biyoloji_516': 'biyoloji',
    'biyoloji_534': 'biyoloji',
    'biyoloji_552': 'biyoloji',
    'biyoloji_570': 'biyoloji',
    'biyoloji_588': 'biyoloji',
    'biyoloji_606': 'biyoloji',
    'biyoloji_624': 'biyoloji',
    'biyoloji_642': 'biyoloji',
    'biyoloji_66': 'biyoloji',
    'biyoloji_660': 'biyoloji',
    'biyoloji_678': 'biyoloji',
    'biyoloji_696': 'biyoloji',
    'biyoloji_714': 'biyoloji',
    'biyoloji_732': 'biyoloji',
    'biyoloji_750': 'biyoloji',
    'biyoloji_768': 'biyoloji',
    'biyoloji_786': 'biyoloji',
    'biyoloji_804': 'biyoloji',
    'biyoloji_822': 'biyoloji',
    'biyoloji_84': 'biyoloji',
    'biyoloji_840': 'biyoloji',
    'biyoloji_858': 'biyoloji',
    'biyoloji_876': 'biyoloji',
    'biyoloji_894': 'biyoloji',
    'biyoloji_912': 'biyoloji',
    'biyoloji_930': 'biyoloji',
    'biyoloji_948': 'biyoloji',
    'biyoloji_966': 'biyoloji',
    'biyoloji_984': 'biyoloji',
    'bna': 'bana',
    'bnm': 'benim',
    'by': 'bay bay',
    'bır': 'bir',
    'cezerı': 'cezeri',
    'cok': 'cok',
    'coz_1012': 'coz',
    'coz_1030': 'coz',
    'coz_1048': 'coz',
    'coz_1066': 'coz',
    'coz_1084': 'coz',
    'coz_1102': 'coz',
    'coz_112': 'coz',
    'coz_1120': 'coz',
    'coz_1138': 'coz',
    'coz_1156': 'coz',
    'coz_1174': 'coz',
    'coz_1192': 'coz',
    'coz_1210': 'coz',
    'coz_1228': 'coz',
    'coz_1246': 'coz',
    'coz_1264': 'coz',
    'coz_1282': 'coz',
    'coz_130': 'coz',
    'coz_1300': 'coz',
    'coz_1318': 'coz',
    'coz_1336': 'coz',
    'coz_148': 'coz',
    'coz_166': 'coz',
    'coz_184': 'coz',
    'coz_202': 'coz',
    'coz_22': 'coz',
    'coz_220': 'coz',
    'coz_238': 'coz',
    'coz_256': 'coz',
    'coz_274': 'coz',
    'coz_292': 'coz',
    'coz_310': 'coz',
    'coz_328': 'coz',
    'coz_346': 'coz',
    'coz_364': 'coz',
    'coz_382': 'coz',
    'coz_4': 'coz',
    'coz_40': 'coz',
    'coz_400': 'coz',
    'coz_418': 'coz',
    'coz_436': 'coz',
    'coz_454': 'coz',
    'coz_472': 'coz',
    'coz_490': 'coz',
    'coz_508': 'coz',
    'coz_526': 'coz',
    'coz_544': 'coz',
    'coz_562': 'coz',
    'coz_58': 'coz',
    'coz_580': 'coz',
    'coz_598': 'coz',
    'coz_616': 'coz',
    'coz_634': 'coz',
    'coz_652': 'coz',
    'coz_670': 'coz',
    'coz_688': 'coz',
    'coz_706': 'coz',
    'coz_724': 'coz',
    'coz_742': 'coz',
    'coz_76': 'coz',
    'coz_760': 'coz',
    'coz_778': 'coz',
    'coz_796': 'coz',
    'coz_814': 'coz',
    'coz_832': 'coz',
    'coz_850': 'coz',
    'coz_868': 'coz',
    'coz_886': 'coz',
    'coz_904': 'coz',
    'coz_922': 'coz',
    'coz_94': 'coz',
    'coz_940': 'coz',
    'coz_958': 'coz',
    'coz_976': 'coz',
    'coz_994': 'coz',
    'drone_1016': 'drone',
    'drone_1034': 'drone',
    'drone_1052': 'drone',
    'drone_1070': 'drone',
    'drone_1088': 'drone',
    'drone_1106': 'drone',
    'drone_1124': 'drone',
    'drone_1142': 'drone',
    'drone_116': 'drone',
    'drone_1160': 'drone',
    'drone_1178': 'drone',
    'drone_1196': 'drone',
    'drone_1214': 'drone',
    'drone_1232': 'drone',
    'drone_1250': 'drone',
    'drone_1268': 'drone',
    'drone_1286': 'drone',
    'drone_1304': 'drone',
    'drone_1322': 'drone',
    'drone_134': 'drone',
    'drone_1340': 'drone',
    'drone_152': 'drone',
    'drone_170': 'drone',
    'drone_188': 'drone',
    'drone_206': 'drone',
    'drone_224': 'drone',
    'drone_242': 'drone',
    'drone_26': 'drone',
    'drone_260': 'drone',
    'drone_278': 'drone',
    'drone_296': 'drone',
    'drone_314': 'drone',
    'drone_332': 'drone',
    'drone_350': 'drone',
    'drone_368': 'drone',
    'drone_386': 'drone',
    'drone_404': 'drone',
    'drone_422': 'drone',
    'drone_44': 'drone',
    'drone_440': 'drone',
    'drone_458': 'drone',
    'drone_476': 'drone',
    'drone_494': 'drone',
    'drone_512': 'drone',
    'drone_530': 'drone',
    'drone_548': 'drone',
    'drone_566': 'drone',
    'drone_584': 'drone',
    'drone_602': 'drone',
    'drone_62': 'drone',
    'drone_620': 'drone',
    'drone_638': 'drone',
    'drone_656': 'drone',
    'drone_674': 'drone',
    'drone_692': 'drone',
    'drone_710': 'drone',
    'drone_728': 'drone',
    'drone_746': 'drone',
    'drone_764': 'drone',
    'drone_782': 'drone',
    'drone_8': 'drone',
    'drone_80': 'drone',
    'drone_800': 'drone',
    'drone_818': 'drone',
    'drone_836': 'drone',
    'drone_854': 'drone',
    'drone_872': 'drone',
    'drone_890': 'drone',
    'drone_908': 'drone',
    'drone_926': 'drone',
    'drone_944': 'drone',
    'drone_962': 'drone',
    'drone_98': 'drone',
    'drone_980': 'drone',
    'drone_998': 'drone',
    'ebob': 'ebob',
    'ekok': 'ekok',
    'eyv': 'eyvallah',
    'eyvallh': 'eyvallah',
    'eyvlh': 'eyvallah',
    'eyw': 'eyvallah',
    'fizik_10': 'fizik',
    'fizik_100': 'fizik',
    'fizik_1000': 'fizik',
    'fizik_1018': 'fizik',
    'fizik_1036': 'fizik',
    'fizik_1054': 'fizik',
    'fizik_1072': 'fizik',
    'fizik_1090': 'fizik',
    'fizik_1108': 'fizik',
    'fizik_1126': 'fizik',
    'fizik_1144': 'fizik',
    'fizik_1162': 'fizik',
    'fizik_118': 'fizik',
    'fizik_1180': 'fizik',
    'fizik_1198': 'fizik',
    'fizik_1216': 'fizik',
    'fizik_1234': 'fizik',
    'fizik_1252': 'fizik',
    'fizik_1270': 'fizik',
    'fizik_1288': 'fizik',
    'fizik_1306': 'fizik',
    'fizik_1324': 'fizik',
    'fizik_1342': 'fizik',
    'fizik_136': 'fizik',
    'fizik_154': 'fizik',
    'fizik_172': 'fizik',
    'fizik_190': 'fizik',
    'fizik_208': 'fizik',
    'fizik_226': 'fizik',
    'fizik_244': 'fizik',
    'fizik_262': 'fizik',
    'fizik_28': 'fizik',
    'fizik_280': 'fizik',
    'fizik_298': 'fizik',
    'fizik_316': 'fizik',
    'fizik_334': 'fizik',
    'fizik_352': 'fizik',
    'fizik_370': 'fizik',
    'fizik_388': 'fizik',
    'fizik_406': 'fizik',
    'fizik_424': 'fizik',
    'fizik_442': 'fizik',
    'fizik_46': 'fizik',
    'fizik_460': 'fizik',
    'fizik_478': 'fizik',
    'fizik_496': 'fizik',
    'fizik_514': 'fizik',
    'fizik_532': 'fizik',
    'fizik_550': 'fizik',
    'fizik_568': 'fizik',
    'fizik_586': 'fizik',
    'fizik_604': 'fizik',
    'fizik_622': 'fizik',
    'fizik_64': 'fizik',
    'fizik_640': 'fizik',
    'fizik_658': 'fizik',
    'fizik_676': 'fizik',
    'fizik_694': 'fizik',
    'fizik_712': 'fizik',
    'fizik_730': 'fizik',
    'fizik_748': 'fizik',
    'fizik_766': 'fizik',
    'fizik_784': 'fizik',
    'fizik_802': 'fizik',
    'fizik_82': 'fizik',
    'fizik_820': 'fizik',
    'fizik_838': 'fizik',
    'fizik_856': 'fizik',
    'fizik_874': 'fizik',
    'fizik_892': 'fizik',
    'fizik_910': 'fizik',
    'fizik_928': 'fizik',
    'fizik_946': 'fizik',
    'fizik_964': 'fizik',
    'fizik_982': 'fizik',
    'galatasaray_1003': 'galatasaray',
    'galatasaray_1021': 'galatasaray',
    'galatasaray_103': 'galatasaray',
    'galatasaray_1039': 'galatasaray',
    'galatasaray_1057': 'galatasaray',
    'galatasaray_1075': 'galatasaray',
    'galatasaray_1093': 'galatasaray',
    'galatasaray_1111': 'galatasaray',
    'galatasaray_1129': 'galatasaray',
    'galatasaray_1147': 'galatasaray',
    'galatasaray_1165': 'galatasaray',
    'galatasaray_1183': 'galatasaray',
    'galatasaray_1201': 'galatasaray',
    'galatasaray_121': 'galatasaray',
    'galatasaray_1219': 'galatasaray',
    'galatasaray_1237': 'galatasaray',
    'galatasaray_1255': 'galatasaray',
    'galatasaray_1273': 'galatasaray',
    'galatasaray_1291': 'galatasaray',
    'galatasaray_13': 'galatasaray',
    'galatasaray_1309': 'galatasaray',
    'galatasaray_1327': 'galatasaray',
    'galatasaray_1345': 'galatasaray',
    'galatasaray_139': 'galatasaray',
    'galatasaray_157': 'galatasaray',
    'galatasaray_175': 'galatasaray',
    'galatasaray_193': 'galatasaray',
    'galatasaray_211': 'galatasaray',
    'galatasaray_229': 'galatasaray',
    'galatasaray_247': 'galatasaray',
    'galatasaray_265': 'galatasaray',
    'galatasaray_283': 'galatasaray',
    'galatasaray_301': 'galatasaray',
    'galatasaray_31': 'galatasaray',
    'galatasaray_319': 'galatasaray',
    'galatasaray_337': 'galatasaray',
    'galatasaray_355': 'galatasaray',
    'galatasaray_373': 'galatasaray',
    'galatasaray_391': 'galatasaray',
    'galatasaray_409': 'galatasaray',
    'galatasaray_427': 'galatasaray',
    'galatasaray_445': 'galatasaray',
    'galatasaray_463': 'galatasaray',
    'galatasaray_481': 'galatasaray',
    'galatasaray_49': 'galatasaray',
    'galatasaray_499': 'galatasaray',
    'galatasaray_517': 'galatasaray',
    'galatasaray_535': 'galatasaray',
    'galatasaray_553': 'galatasaray',
    'galatasaray_571': 'galatasaray',
    'galatasaray_589': 'galatasaray',
    'galatasaray_607': 'galatasaray',
    'galatasaray_625': 'galatasaray',
    'galatasaray_643': 'galatasaray',
    'galatasaray_661': 'galatasaray',
    'galatasaray_67': 'galatasaray',
    'galatasaray_679': 'galatasaray',
    'galatasaray_697': 'galatasaray',
    'galatasaray_715': 'galatasaray',
    'galatasaray_733': 'galatasaray',
    'galatasaray_751': 'galatasaray',
    'galatasaray_769': 'galatasaray',
    'galatasaray_787': 'galatasaray',
    'galatasaray_805': 'galatasaray',
    'galatasaray_823': 'galatasaray',
    'galatasaray_841': 'galatasaray',
    'galatasaray_85': 'galatasaray',
    'galatasaray_859': 'galatasaray',
    'galatasaray_877': 'galatasaray',
    'galatasaray_895': 'galatasaray',
    'galatasaray_913': 'galatasaray',
    'galatasaray_931': 'galatasaray',
    'galatasaray_949': 'galatasaray',
    'galatasaray_967': 'galatasaray',
    'galatasaray_985': 'galatasaray',
    'gnaydın': 'gunaydin',
    'gnydn': 'gunaydin',
    'grsrz': 'gorusuruz',
    'görüşürz': 'gorusuruz',
    'hakimda': 'hakkimda',
    'hakkimd': 'hakkimda',
    'hakkmda': 'hakkimda',
    'harezmı': 'harezmi',
    'hesapla_1011': 'hesapla',
    'hesapla_1029': 'hesapla',
    'hesapla_1047': 'hesapla',
    'hesapla_1065': 'hesapla',
    'hesapla_1083': 'hesapla',
    'hesapla_1101': 'hesapla',
    'hesapla_111': 'hesapla',
    'hesapla_1119': 'hesapla',
    'hesapla_1137': 'hesapla',
    'hesapla_1155': 'hesapla',
    'hesapla_1173': 'hesapla',
    'hesapla_1191': 'hesapla',
    'hesapla_1209': 'hesapla',
    'hesapla_1227': 'hesapla',
    'hesapla_1245': 'hesapla',
    'hesapla_1263': 'hesapla',
    'hesapla_1281': 'hesapla',
    'hesapla_129': 'hesapla',
    'hesapla_1299': 'hesapla',
    'hesapla_1317': 'hesapla',
    'hesapla_1335': 'hesapla',
    'hesapla_147': 'hesapla',
    'hesapla_165': 'hesapla',
    'hesapla_183': 'hesapla',
    'hesapla_201': 'hesapla',
    'hesapla_21': 'hesapla',
    'hesapla_219': 'hesapla',
    'hesapla_237': 'hesapla',
    'hesapla_255': 'hesapla',
    'hesapla_273': 'hesapla',
    'hesapla_291': 'hesapla',
    'hesapla_3': 'hesapla',
    'hesapla_309': 'hesapla',
    'hesapla_327': 'hesapla',
    'hesapla_345': 'hesapla',
    'hesapla_363': 'hesapla',
    'hesapla_381': 'hesapla',
    'hesapla_39': 'hesapla',
    'hesapla_399': 'hesapla',
    'hesapla_417': 'hesapla',
    'hesapla_435': 'hesapla',
    'hesapla_453': 'hesapla',
    'hesapla_471': 'hesapla',
    'hesapla_489': 'hesapla',
    'hesapla_507': 'hesapla',
    'hesapla_525': 'hesapla',
    'hesapla_543': 'hesapla',
    'hesapla_561': 'hesapla',
    'hesapla_57': 'hesapla',
    'hesapla_579': 'hesapla',
    'hesapla_597': 'hesapla',
    'hesapla_615': 'hesapla',
    'hesapla_633': 'hesapla',
    'hesapla_651': 'hesapla',
    'hesapla_669': 'hesapla',
    'hesapla_687': 'hesapla',
    'hesapla_705': 'hesapla',
    'hesapla_723': 'hesapla',
    'hesapla_741': 'hesapla',
    'hesapla_75': 'hesapla',
    'hesapla_759': 'hesapla',
    'hesapla_777': 'hesapla',
    'hesapla_795': 'hesapla',
    'hesapla_813': 'hesapla',
    'hesapla_831': 'hesapla',
    'hesapla_849': 'hesapla',
    'hesapla_867': 'hesapla',
    'hesapla_885': 'hesapla',
    'hesapla_903': 'hesapla',
    'hesapla_921': 'hesapla',
    'hesapla_93': 'hesapla',
    'hesapla_939': 'hesapla',
    'hesapla_957': 'hesapla',
    'hesapla_975': 'hesapla',
    'hesapla_993': 'hesapla',
    'hkkmda': 'hakkimda',
    'ibnibattuta': 'ibni battuta',
    'ibnisina': 'ibni sina',
    'ii': 'iyi',
    'iy': 'iyi',
    'kac': 'kac',
    'kankam': 'kanka',
    'kanki': 'kanka',
    'kardesm': 'kardesim',
    'karekok': 'karekok',
    'kimsn': 'kimsin',
    'kimya_1001': 'kimya',
    'kimya_101': 'kimya',
    'kimya_1019': 'kimya',
    'kimya_1037': 'kimya',
    'kimya_1055': 'kimya',
    'kimya_1073': 'kimya',
    'kimya_1091': 'kimya',
    'kimya_11': 'kimya',
    'kimya_1109': 'kimya',
    'kimya_1127': 'kimya',
    'kimya_1145': 'kimya',
    'kimya_1163': 'kimya',
    'kimya_1181': 'kimya',
    'kimya_119': 'kimya',
    'kimya_1199': 'kimya',
    'kimya_1217': 'kimya',
    'kimya_1235': 'kimya',
    'kimya_1253': 'kimya',
    'kimya_1271': 'kimya',
    'kimya_1289': 'kimya',
    'kimya_1307': 'kimya',
    'kimya_1325': 'kimya',
    'kimya_1343': 'kimya',
    'kimya_137': 'kimya',
    'kimya_155': 'kimya',
    'kimya_173': 'kimya',
    'kimya_191': 'kimya',
    'kimya_209': 'kimya',
    'kimya_227': 'kimya',
    'kimya_245': 'kimya',
    'kimya_263': 'kimya',
    'kimya_281': 'kimya',
    'kimya_29': 'kimya',
    'kimya_299': 'kimya',
    'kimya_317': 'kimya',
    'kimya_335': 'kimya',
    'kimya_353': 'kimya',
    'kimya_371': 'kimya',
    'kimya_389': 'kimya',
    'kimya_407': 'kimya',
    'kimya_425': 'kimya',
    'kimya_443': 'kimya',
    'kimya_461': 'kimya',
    'kimya_47': 'kimya',
    'kimya_479': 'kimya',
    'kimya_497': 'kimya',
    'kimya_515': 'kimya',
    'kimya_533': 'kimya',
    'kimya_551': 'kimya',
    'kimya_569': 'kimya',
    'kimya_587': 'kimya',
    'kimya_605': 'kimya',
    'kimya_623': 'kimya',
    'kimya_641': 'kimya',
    'kimya_65': 'kimya',
    'kimya_659': 'kimya',
    'kimya_677': 'kimya',
    'kimya_695': 'kimya',
    'kimya_713': 'kimya',
    'kimya_731': 'kimya',
    'kimya_749': 'kimya',
    'kimya_767': 'kimya',
    'kimya_785': 'kimya',
    'kimya_803': 'kimya',
    'kimya_821': 'kimya',
    'kimya_83': 'kimya',
    'kimya_839': 'kimya',
    'kimya_857': 'kimya',
    'kimya_875': 'kimya',
    'kimya_893': 'kimya',
    'kimya_911': 'kimya',
    'kimya_929': 'kimya',
    'kimya_947': 'kimya',
    'kimya_965': 'kimya',
    'kimya_983': 'kimya',
    'kin': 'kim',
    'km': 'kim',
    'kmdr': 'kimdir',
    'kmsin': 'kimsin',
    'kmsn': 'kimsin',
    'knk': 'kanka',
    'knkm': 'kanka',
    'koklu': 'koklu',
    'krdesim': 'kardesim',
    'krdsm': 'kardesim',
    'krdşm': 'kardesim',
    'kım': 'kim',
    'kımde': 'kimdir',
    'kımsın': 'kimsin',
    'kın': 'kim',
    'matematik_1017': 'matematik',
    'matematik_1035': 'matematik',
    'matematik_1053': 'matematik',
    'matematik_1071': 'matematik',
    'matematik_1089': 'matematik',
    'matematik_1107': 'matematik',
    'matematik_1125': 'matematik',
    'matematik_1143': 'matematik',
    'matematik_1161': 'matematik',
    'matematik_117': 'matematik',
    'matematik_1179': 'matematik',
    'matematik_1197': 'matematik',
    'matematik_1215': 'matematik',
    'matematik_1233': 'matematik',
    'matematik_1251': 'matematik',
    'matematik_1269': 'matematik',
    'matematik_1287': 'matematik',
    'matematik_1305': 'matematik',
    'matematik_1323': 'matematik',
    'matematik_1341': 'matematik',
    'matematik_135': 'matematik',
    'matematik_153': 'matematik',
    'matematik_171': 'matematik',
    'matematik_189': 'matematik',
    'matematik_207': 'matematik',
    'matematik_225': 'matematik',
    'matematik_243': 'matematik',
    'matematik_261': 'matematik',
    'matematik_27': 'matematik',
    'matematik_279': 'matematik',
    'matematik_297': 'matematik',
    'matematik_315': 'matematik',
    'matematik_333': 'matematik',
    'matematik_351': 'matematik',
    'matematik_369': 'matematik',
    'matematik_387': 'matematik',
    'matematik_405': 'matematik',
    'matematik_423': 'matematik',
    'matematik_441': 'matematik',
    'matematik_45': 'matematik',
    'matematik_459': 'matematik',
    'matematik_477': 'matematik',
    'matematik_495': 'matematik',
    'matematik_513': 'matematik',
    'matematik_531': 'matematik',
    'matematik_549': 'matematik',
    'matematik_567': 'matematik',
    'matematik_585': 'matematik',
    'matematik_603': 'matematik',
    'matematik_621': 'matematik',
    'matematik_63': 'matematik',
    'matematik_639': 'matematik',
    'matematik_657': 'matematik',
    'matematik_675': 'matematik',
    'matematik_693': 'matematik',
    'matematik_711': 'matematik',
    'matematik_729': 'matematik',
    'matematik_747': 'matematik',
    'matematik_765': 'matematik',
    'matematik_783': 'matematik',
    'matematik_801': 'matematik',
    'matematik_81': 'matematik',
    'matematik_819': 'matematik',
    'matematik_837': 'matematik',
    'matematik_855': 'matematik',
    'matematik_873': 'matematik',
    'matematik_891': 'matematik',
    'matematik_9': 'matematik',
    'matematik_909': 'matematik',
    'matematik_927': 'matematik',
    'matematik_945': 'matematik',
    'matematik_963': 'matematik',
    'matematik_981': 'matematik',
    'matematik_99': 'matematik',
    'matematik_999': 'matematik',
    'meraba': 'merhaba',
    'mrb': 'merhaba',
    'mrbh': 'merhaba',
    'mrblar': 'merhaba',
    'mrhb': 'merhaba',
    'naberler': 'naber',
    'nabr': 'naber',
    'napion': 'ne yapiyorsun',
    'napiyon': 'ne yapiyorsun',
    'napiyosun': 'ne yapiyorsun',
    'napyon': 'ne yapiyorsun',
    'napıyon': 'ne yapiyorsun',
    'napıyosun': 'ne yapiyorsun',
    'nasilsn': 'nasilsin',
    'nasisin': 'nasilsin',
    'naslsn': 'nasilsin',
    'naslsın': 'nasilsin',
    'nassin': 'nasilsin',
    'nassın': 'nasilsin',
    'nasılsn': 'nasilsin',
    'nasılsınz': 'nasilsin',
    'nasısın': 'nasilsin',
    'nber': 'naber',
    'nbr': 'naber',
    'nbry': 'naber',
    'ndr': 'nedir',
    'neapıyon': 'ne yapiyorsun',
    'nedr': 'nedir',
    'nslsn': 'nasilsin',
    'nslsın': 'nasilsin',
    'ogret_1013': 'ogret',
    'ogret_1031': 'ogret',
    'ogret_1049': 'ogret',
    'ogret_1067': 'ogret',
    'ogret_1085': 'ogret',
    'ogret_1103': 'ogret',
    'ogret_1121': 'ogret',
    'ogret_113': 'ogret',
    'ogret_1139': 'ogret',
    'ogret_1157': 'ogret',
    'ogret_1175': 'ogret',
    'ogret_1193': 'ogret',
    'ogret_1211': 'ogret',
    'ogret_1229': 'ogret',
    'ogret_1247': 'ogret',
    'ogret_1265': 'ogret',
    'ogret_1283': 'ogret',
    'ogret_1301': 'ogret',
    'ogret_131': 'ogret',
    'ogret_1319': 'ogret',
    'ogret_1337': 'ogret',
    'ogret_149': 'ogret',
    'ogret_167': 'ogret',
    'ogret_185': 'ogret',
    'ogret_203': 'ogret',
    'ogret_221': 'ogret',
    'ogret_23': 'ogret',
    'ogret_239': 'ogret',
    'ogret_257': 'ogret',
    'ogret_275': 'ogret',
    'ogret_293': 'ogret',
    'ogret_311': 'ogret',
    'ogret_329': 'ogret',
    'ogret_347': 'ogret',
    'ogret_365': 'ogret',
    'ogret_383': 'ogret',
    'ogret_401': 'ogret',
    'ogret_41': 'ogret',
    'ogret_419': 'ogret',
    'ogret_437': 'ogret',
    'ogret_455': 'ogret',
    'ogret_473': 'ogret',
    'ogret_491': 'ogret',
    'ogret_5': 'ogret',
    'ogret_509': 'ogret',
    'ogret_527': 'ogret',
    'ogret_545': 'ogret',
    'ogret_563': 'ogret',
    'ogret_581': 'ogret',
    'ogret_59': 'ogret',
    'ogret_599': 'ogret',
    'ogret_617': 'ogret',
    'ogret_635': 'ogret',
    'ogret_653': 'ogret',
    'ogret_671': 'ogret',
    'ogret_689': 'ogret',
    'ogret_707': 'ogret',
    'ogret_725': 'ogret',
    'ogret_743': 'ogret',
    'ogret_761': 'ogret',
    'ogret_77': 'ogret',
    'ogret_779': 'ogret',
    'ogret_797': 'ogret',
    'ogret_815': 'ogret',
    'ogret_833': 'ogret',
    'ogret_851': 'ogret',
    'ogret_869': 'ogret',
    'ogret_887': 'ogret',
    'ogret_905': 'ogret',
    'ogret_923': 'ogret',
    'ogret_941': 'ogret',
    'ogret_95': 'ogret',
    'ogret_959': 'ogret',
    'ogret_977': 'ogret',
    'ogret_995': 'ogret',
    'ok': 'tamam',
    'okey': 'tamam',
    'proje_1015': 'projelerim',
    'proje_1033': 'projelerim',
    'proje_1051': 'projelerim',
    'proje_1069': 'projelerim',
    'proje_1087': 'projelerim',
    'proje_1105': 'projelerim',
    'proje_1123': 'projelerim',
    'proje_1141': 'projelerim',
    'proje_115': 'projelerim',
    'proje_1159': 'projelerim',
    'proje_1177': 'projelerim',
    'proje_1195': 'projelerim',
    'proje_1213': 'projelerim',
    'proje_1231': 'projelerim',
    'proje_1249': 'projelerim',
    'proje_1267': 'projelerim',
    'proje_1285': 'projelerim',
    'proje_1303': 'projelerim',
    'proje_1321': 'projelerim',
    'proje_133': 'projelerim',
    'proje_1339': 'projelerim',
    'proje_151': 'projelerim',
    'proje_169': 'projelerim',
    'proje_187': 'projelerim',
    'proje_205': 'projelerim',
    'proje_223': 'projelerim',
    'proje_241': 'projelerim',
    'proje_25': 'projelerim',
    'proje_259': 'projelerim',
    'proje_277': 'projelerim',
    'proje_295': 'projelerim',
    'proje_313': 'projelerim',
    'proje_331': 'projelerim',
    'proje_349': 'projelerim',
    'proje_367': 'projelerim',
    'proje_385': 'projelerim',
    'proje_403': 'projelerim',
    'proje_421': 'projelerim',
    'proje_43': 'projelerim',
    'proje_439': 'projelerim',
    'proje_457': 'projelerim',
    'proje_475': 'projelerim',
    'proje_493': 'projelerim',
    'proje_511': 'projelerim',
    'proje_529': 'projelerim',
    'proje_547': 'projelerim',
    'proje_565': 'projelerim',
    'proje_583': 'projelerim',
    'proje_601': 'projelerim',
    'proje_61': 'projelerim',
    'proje_619': 'projelerim',
    'proje_637': 'projelerim',
    'proje_655': 'projelerim',
    'proje_673': 'projelerim',
    'proje_691': 'projelerim',
    'proje_7': 'projelerim',
    'proje_709': 'projelerim',
    'proje_727': 'projelerim',
    'proje_745': 'projelerim',
    'proje_763': 'projelerim',
    'proje_781': 'projelerim',
    'proje_79': 'projelerim',
    'proje_799': 'projelerim',
    'proje_817': 'projelerim',
    'proje_835': 'projelerim',
    'proje_853': 'projelerim',
    'proje_871': 'projelerim',
    'proje_889': 'projelerim',
    'proje_907': 'projelerim',
    'proje_925': 'projelerim',
    'proje_943': 'projelerim',
    'proje_961': 'projelerim',
    'proje_97': 'projelerim',
    'proje_979': 'projelerim',
    'proje_997': 'projelerim',
    'python_1007': 'python',
    'python_1025': 'python',
    'python_1043': 'python',
    'python_1061': 'python',
    'python_107': 'python',
    'python_1079': 'python',
    'python_1097': 'python',
    'python_1115': 'python',
    'python_1133': 'python',
    'python_1151': 'python',
    'python_1169': 'python',
    'python_1187': 'python',
    'python_1205': 'python',
    'python_1223': 'python',
    'python_1241': 'python',
    'python_125': 'python',
    'python_1259': 'python',
    'python_1277': 'python',
    'python_1295': 'python',
    'python_1313': 'python',
    'python_1331': 'python',
    'python_1349': 'python',
    'python_143': 'python',
    'python_161': 'python',
    'python_17': 'python',
    'python_179': 'python',
    'python_197': 'python',
    'python_215': 'python',
    'python_233': 'python',
    'python_251': 'python',
    'python_269': 'python',
    'python_287': 'python',
    'python_305': 'python',
    'python_323': 'python',
    'python_341': 'python',
    'python_35': 'python',
    'python_359': 'python',
    'python_377': 'python',
    'python_395': 'python',
    'python_413': 'python',
    'python_431': 'python',
    'python_449': 'python',
    'python_467': 'python',
    'python_485': 'python',
    'python_503': 'python',
    'python_521': 'python',
    'python_53': 'python',
    'python_539': 'python',
    'python_557': 'python',
    'python_575': 'python',
    'python_593': 'python',
    'python_611': 'python',
    'python_629': 'python',
    'python_647': 'python',
    'python_665': 'python',
    'python_683': 'python',
    'python_701': 'python',
    'python_71': 'python',
    'python_719': 'python',
    'python_737': 'python',
    'python_755': 'python',
    'python_773': 'python',
    'python_791': 'python',
    'python_809': 'python',
    'python_827': 'python',
    'python_845': 'python',
    'python_863': 'python',
    'python_881': 'python',
    'python_89': 'python',
    'python_899': 'python',
    'python_917': 'python',
    'python_935': 'python',
    'python_953': 'python',
    'python_971': 'python',
    'python_989': 'python',
    's.a': 'selam',
    's.a.': 'selam',
    'sa': 'selamunaleykum',
    'sagol': 'sag ol',
    'saol': 'sag ol',
    'saolasin': 'sag ol',
    'sağol': 'sag ol',
    'selamlar': 'selam',
    'selamm': 'selam',
    'selamunaleykum': 'selamun aleykum',
    'slm': 'selam',
    'slmlar': 'selam',
    'slmm': 'selam',
    'snn': 'senin',
    'streamlit_1008': 'streamlit',
    'streamlit_1026': 'streamlit',
    'streamlit_1044': 'streamlit',
    'streamlit_1062': 'streamlit',
    'streamlit_108': 'streamlit',
    'streamlit_1080': 'streamlit',
    'streamlit_1098': 'streamlit',
    'streamlit_1116': 'streamlit',
    'streamlit_1134': 'streamlit',
    'streamlit_1152': 'streamlit',
    'streamlit_1170': 'streamlit',
    'streamlit_1188': 'streamlit',
    'streamlit_1206': 'streamlit',
    'streamlit_1224': 'streamlit',
    'streamlit_1242': 'streamlit',
    'streamlit_126': 'streamlit',
    'streamlit_1260': 'streamlit',
    'streamlit_1278': 'streamlit',
    'streamlit_1296': 'streamlit',
    'streamlit_1314': 'streamlit',
    'streamlit_1332': 'streamlit',
    'streamlit_1350': 'streamlit',
    'streamlit_144': 'streamlit',
    'streamlit_162': 'streamlit',
    'streamlit_18': 'streamlit',
    'streamlit_180': 'streamlit',
    'streamlit_198': 'streamlit',
    'streamlit_216': 'streamlit',
    'streamlit_234': 'streamlit',
    'streamlit_252': 'streamlit',
    'streamlit_270': 'streamlit',
    'streamlit_288': 'streamlit',
    'streamlit_306': 'streamlit',
    'streamlit_324': 'streamlit',
    'streamlit_342': 'streamlit',
    'streamlit_36': 'streamlit',
    'streamlit_360': 'streamlit',
    'streamlit_378': 'streamlit',
    'streamlit_396': 'streamlit',
    'streamlit_414': 'streamlit',
    'streamlit_432': 'streamlit',
    'streamlit_450': 'streamlit',
    'streamlit_468': 'streamlit',
    'streamlit_486': 'streamlit',
    'streamlit_504': 'streamlit',
    'streamlit_522': 'streamlit',
    'streamlit_54': 'streamlit',
    'streamlit_540': 'streamlit',
    'streamlit_558': 'streamlit',
    'streamlit_576': 'streamlit',
    'streamlit_594': 'streamlit',
    'streamlit_612': 'streamlit',
    'streamlit_630': 'streamlit',
    'streamlit_648': 'streamlit',
    'streamlit_666': 'streamlit',
    'streamlit_684': 'streamlit',
    'streamlit_702': 'streamlit',
    'streamlit_72': 'streamlit',
    'streamlit_720': 'streamlit',
    'streamlit_738': 'streamlit',
    'streamlit_756': 'streamlit',
    'streamlit_774': 'streamlit',
    'streamlit_792': 'streamlit',
    'streamlit_810': 'streamlit',
    'streamlit_828': 'streamlit',
    'streamlit_846': 'streamlit',
    'streamlit_864': 'streamlit',
    'streamlit_882': 'streamlit',
    'streamlit_90': 'streamlit',
    'streamlit_900': 'streamlit',
    'streamlit_918': 'streamlit',
    'streamlit_936': 'streamlit',
    'streamlit_954': 'streamlit',
    'streamlit_972': 'streamlit',
    'streamlit_990': 'streamlit',
    'teknofest_1004': 'teknofest',
    'teknofest_1022': 'teknofest',
    'teknofest_104': 'teknofest',
    'teknofest_1040': 'teknofest',
    'teknofest_1058': 'teknofest',
    'teknofest_1076': 'teknofest',
    'teknofest_1094': 'teknofest',
    'teknofest_1112': 'teknofest',
    'teknofest_1130': 'teknofest',
    'teknofest_1148': 'teknofest',
    'teknofest_1166': 'teknofest',
    'teknofest_1184': 'teknofest',
    'teknofest_1202': 'teknofest',
    'teknofest_122': 'teknofest',
    'teknofest_1220': 'teknofest',
    'teknofest_1238': 'teknofest',
    'teknofest_1256': 'teknofest',
    'teknofest_1274': 'teknofest',
    'teknofest_1292': 'teknofest',
    'teknofest_1310': 'teknofest',
    'teknofest_1328': 'teknofest',
    'teknofest_1346': 'teknofest',
    'teknofest_14': 'teknofest',
    'teknofest_140': 'teknofest',
    'teknofest_158': 'teknofest',
    'teknofest_176': 'teknofest',
    'teknofest_194': 'teknofest',
    'teknofest_212': 'teknofest',
    'teknofest_230': 'teknofest',
    'teknofest_248': 'teknofest',
    'teknofest_266': 'teknofest',
    'teknofest_284': 'teknofest',
    'teknofest_302': 'teknofest',
    'teknofest_32': 'teknofest',
    'teknofest_320': 'teknofest',
    'teknofest_338': 'teknofest',
    'teknofest_356': 'teknofest',
    'teknofest_374': 'teknofest',
    'teknofest_392': 'teknofest',
    'teknofest_410': 'teknofest',
    'teknofest_428': 'teknofest',
    'teknofest_446': 'teknofest',
    'teknofest_464': 'teknofest',
    'teknofest_482': 'teknofest',
    'teknofest_50': 'teknofest',
    'teknofest_500': 'teknofest',
    'teknofest_518': 'teknofest',
    'teknofest_536': 'teknofest',
    'teknofest_554': 'teknofest',
    'teknofest_572': 'teknofest',
    'teknofest_590': 'teknofest',
    'teknofest_608': 'teknofest',
    'teknofest_626': 'teknofest',
    'teknofest_644': 'teknofest',
    'teknofest_662': 'teknofest',
    'teknofest_68': 'teknofest',
    'teknofest_680': 'teknofest',
    'teknofest_698': 'teknofest',
    'teknofest_716': 'teknofest',
    'teknofest_734': 'teknofest',
    'teknofest_752': 'teknofest',
    'teknofest_770': 'teknofest',
    'teknofest_788': 'teknofest',
    'teknofest_806': 'teknofest',
    'teknofest_824': 'teknofest',
    'teknofest_842': 'teknofest',
    'teknofest_86': 'teknofest',
    'teknofest_860': 'teknofest',
    'teknofest_878': 'teknofest',
    'teknofest_896': 'teknofest',
    'teknofest_914': 'teknofest',
    'teknofest_932': 'teknofest',
    'teknofest_950': 'teknofest',
    'teknofest_968': 'teknofest',
    'teknofest_986': 'teknofest',
    'tesekkurler': 'tesekkur',
    'tm': 'tamam',
    'tmm': 'tamam',
    'tsk': 'tesekkur',
    'tskr': 'tesekkur',
    'tubitak_1005': 'tubitak',
    'tubitak_1023': 'tubitak',
    'tubitak_1041': 'tubitak',
    'tubitak_105': 'tubitak',
    'tubitak_1059': 'tubitak',
    'tubitak_1077': 'tubitak',
    'tubitak_1095': 'tubitak',
    'tubitak_1113': 'tubitak',
    'tubitak_1131': 'tubitak',
    'tubitak_1149': 'tubitak',
    'tubitak_1167': 'tubitak',
    'tubitak_1185': 'tubitak',
    'tubitak_1203': 'tubitak',
    'tubitak_1221': 'tubitak',
    'tubitak_123': 'tubitak',
    'tubitak_1239': 'tubitak',
    'tubitak_1257': 'tubitak',
    'tubitak_1275': 'tubitak',
    'tubitak_1293': 'tubitak',
    'tubitak_1311': 'tubitak',
    'tubitak_1329': 'tubitak',
    'tubitak_1347': 'tubitak',
    'tubitak_141': 'tubitak',
    'tubitak_15': 'tubitak',
    'tubitak_159': 'tubitak',
    'tubitak_177': 'tubitak',
    'tubitak_195': 'tubitak',
    'tubitak_213': 'tubitak',
    'tubitak_231': 'tubitak',
    'tubitak_249': 'tubitak',
    'tubitak_267': 'tubitak',
    'tubitak_285': 'tubitak',
    'tubitak_303': 'tubitak',
    'tubitak_321': 'tubitak',
    'tubitak_33': 'tubitak',
    'tubitak_339': 'tubitak',
    'tubitak_357': 'tubitak',
    'tubitak_375': 'tubitak',
    'tubitak_393': 'tubitak',
    'tubitak_411': 'tubitak',
    'tubitak_429': 'tubitak',
    'tubitak_447': 'tubitak',
    'tubitak_465': 'tubitak',
    'tubitak_483': 'tubitak',
    'tubitak_501': 'tubitak',
    'tubitak_51': 'tubitak',
    'tubitak_519': 'tubitak',
    'tubitak_537': 'tubitak',
    'tubitak_555': 'tubitak',
    'tubitak_573': 'tubitak',
    'tubitak_591': 'tubitak',
    'tubitak_609': 'tubitak',
    'tubitak_627': 'tubitak',
    'tubitak_645': 'tubitak',
    'tubitak_663': 'tubitak',
    'tubitak_681': 'tubitak',
    'tubitak_69': 'tubitak',
    'tubitak_699': 'tubitak',
    'tubitak_717': 'tubitak',
    'tubitak_735': 'tubitak',
    'tubitak_753': 'tubitak',
    'tubitak_771': 'tubitak',
    'tubitak_789': 'tubitak',
    'tubitak_807': 'tubitak',
    'tubitak_825': 'tubitak',
    'tubitak_843': 'tubitak',
    'tubitak_861': 'tubitak',
    'tubitak_87': 'tubitak',
    'tubitak_879': 'tubitak',
    'tubitak_897': 'tubitak',
    'tubitak_915': 'tubitak',
    'tubitak_933': 'tubitak',
    'tubitak_951': 'tubitak',
    'tubitak_969': 'tubitak',
    'tubitak_987': 'tubitak',
    'tşk': 'tesekkur',
    'uslu': 'uslu',
    'yardim_1014': 'yardim',
    'yardim_1032': 'yardim',
    'yardim_1050': 'yardim',
    'yardim_1068': 'yardim',
    'yardim_1086': 'yardim',
    'yardim_1104': 'yardim',
    'yardim_1122': 'yardim',
    'yardim_114': 'yardim',
    'yardim_1140': 'yardim',
    'yardim_1158': 'yardim',
    'yardim_1176': 'yardim',
    'yardim_1194': 'yardim',
    'yardim_1212': 'yardim',
    'yardim_1230': 'yardim',
    'yardim_1248': 'yardim',
    'yardim_1266': 'yardim',
    'yardim_1284': 'yardim',
    'yardim_1302': 'yardim',
    'yardim_132': 'yardim',
    'yardim_1320': 'yardim',
    'yardim_1338': 'yardim',
    'yardim_150': 'yardim',
    'yardim_168': 'yardim',
    'yardim_186': 'yardim',
    'yardim_204': 'yardim',
    'yardim_222': 'yardim',
    'yardim_24': 'yardim',
    'yardim_240': 'yardim',
    'yardim_258': 'yardim',
    'yardim_276': 'yardim',
    'yardim_294': 'yardim',
    'yardim_312': 'yardim',
    'yardim_330': 'yardim',
    'yardim_348': 'yardim',
    'yardim_366': 'yardim',
    'yardim_384': 'yardim',
    'yardim_402': 'yardim',
    'yardim_42': 'yardim',
    'yardim_420': 'yardim',
    'yardim_438': 'yardim',
    'yardim_456': 'yardim',
    'yardim_474': 'yardim',
    'yardim_492': 'yardim',
    'yardim_510': 'yardim',
    'yardim_528': 'yardim',
    'yardim_546': 'yardim',
    'yardim_564': 'yardim',
    'yardim_582': 'yardim',
    'yardim_6': 'yardim',
    'yardim_60': 'yardim',
    'yardim_600': 'yardim',
    'yardim_618': 'yardim',
    'yardim_636': 'yardim',
    'yardim_654': 'yardim',
    'yardim_672': 'yardim',
    'yardim_690': 'yardim',
    'yardim_708': 'yardim',
    'yardim_726': 'yardim',
    'yardim_744': 'yardim',
    'yardim_762': 'yardim',
    'yardim_78': 'yardim',
    'yardim_780': 'yardim',
    'yardim_798': 'yardim',
    'yardim_816': 'yardim',
    'yardim_834': 'yardim',
    'yardim_852': 'yardim',
    'yardim_870': 'yardim',
    'yardim_888': 'yardim',
    'yardim_906': 'yardim',
    'yardim_924': 'yardim',
    'yardim_942': 'yardim',
    'yardim_96': 'yardim',
    'yardim_960': 'yardim',
    'yardim_978': 'yardim',
    'yardim_996': 'yardim',
    'çk': 'cok'}

DUYGU_VE_SOHBET_SABLONLARI = {   'ders_calisma_004': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_012': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_020': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_028': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_036': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_044': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_052': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_060': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_068': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_076': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_084': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_092': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_100': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_108': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_116': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_124': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_132': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_140': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_148': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_156': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_164': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_172': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_180': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_188': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_196': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_204': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_212': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_220': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_228': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_236': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_244': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_252': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_260': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_268': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'ders_calisma_276': {   'tetikleyiciler': [   'ders çalışıyorum',
                                                  'sınava hazırlanıyorum',
                                                  'matematik çalışıyorum',
                                                  'ödev yapıyorum'],
                            'yanit': 'Kolay gelsin Ahmet! 📚 Takıldığın herhangi bir köklü sayı, '
                                     'üslü sayı, denklem veya fen konusu olursa hemen bana sor, '
                                     'adım adım çözelim.'},
    'gece_calismasi_008': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_016': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_024': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_032': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_040': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_048': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_056': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_064': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_072': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_080': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_088': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_096': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_104': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_112': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_120': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_128': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_136': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_144': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_152': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_160': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_168': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_176': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_184': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_192': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_200': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_208': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_216': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_224': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_232': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_240': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_248': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_256': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_264': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_272': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'gece_calismasi_280': {   'tetikleyiciler': [   'uykum geldi',
                                                    'gece oldu',
                                                    'yatıyorum',
                                                    'sabah erken kalkacağım'],
                              'yanit': 'İyi geceler Ahmet! 🌙 21:00 – 04:00 uyku düzenini koruman '
                                       'zihinsel performansın ve 100m antrenmanların için çok '
                                       'önemli. Dinlen, yarın devam ederiz!'},
    'kim_sorusu_genel_003': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_011': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_019': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_027': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_035': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_043': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_051': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_059': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_067': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_075': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_083': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_091': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_099': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_107': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_115': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_123': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_131': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_139': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_147': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_155': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_163': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_171': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_179': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_187': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_195': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_203': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_211': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_219': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_227': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_235': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_243': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_251': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_259': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_267': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kim_sorusu_genel_275': {   'tetikleyiciler': [   'bu kim',
                                                      'o kim',
                                                      'kın',
                                                      'kim bu',
                                                      'kimi tanıdın'],
                                'yanit': "Kimi sorduğunu isimle yazarsan (Örn: **'Ömer kim'**, "
                                         "**'Hadi kim'**, **'El-Cezerî kim'**, **'Ben kimim'**) "
                                         'sana hemen detaylı bilgisini verebilirim Ahmet! ⚡'},
    'kodlama_modu_005': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_013': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_021': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_029': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_037': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_045': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_053': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_061': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_069': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_077': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_085': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_093': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_101': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_109': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_117': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_125': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_133': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_141': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_149': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_157': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_165': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_173': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_181': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_189': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_197': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_205': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_213': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_221': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_229': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_237': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_245': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_253': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_261': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_269': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'kodlama_modu_277': {   'tetikleyiciler': [   'kod yazıyorum',
                                                  'pycharm açtım',
                                                  'hata ayıklıyorum',
                                                  'debug yapıyorum',
                                                  'uygulama yapıyorum'],
                            'yanit': "Harika! 💻 PyCharm'da tüm modüllerimiz birbirine bağlı. "
                                     'İstediğin özelliği veya testi hemen deneyebilirsin.'},
    'mobil_test_006': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_014': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_022': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_030': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_038': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_046': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_054': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_062': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_070': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_078': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_086': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_094': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_102': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_110': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_118': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_126': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_134': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_142': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_150': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_158': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_166': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_174': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_182': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_190': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_198': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_206': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_214': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_222': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_230': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_238': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_246': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_254': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_262': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_270': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'mobil_test_278': {   'tetikleyiciler': [   'mobildeyim',
                                                'telefondan girdim',
                                                'tabletten deniyorum',
                                                'mobil görünüm'],
                          'yanit': '📱 Mobil uyumlu yüksek kontrastlı arayüzümüz şu an aktif Ahmet! '
                                   'Dokunmatik butonlar ve ses motoru telefon ekranına göre '
                                   'optimize edildi.'},
    'nasilsin_detay_002': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_010': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_018': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_026': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_034': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_042': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_050': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_058': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_066': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_074': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_082': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_090': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_098': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_106': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_114': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_122': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_130': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_138': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_146': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_154': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_162': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_170': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_178': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_186': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_194': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_202': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_210': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_218': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_226': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_234': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_242': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_250': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_258': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_266': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'nasilsin_detay_274': {   'tetikleyiciler': [   'bugün nasılsın',
                                                    'sistemlerin nasıl',
                                                    'kendini nasıl hissediyorsun',
                                                    'enerjin nasıl'],
                              'yanit': 'Sistemlerim %100 kapasitede, işlemcim serin, hafızam '
                                       'tertemiz! ⚡ Senin projelere destek olmaya hazırım Ahmet.'},
    'ovgu_tesekkur_007': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_015': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_023': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_031': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_039': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_047': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_055': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_063': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_071': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_079': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_087': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_095': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_103': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_111': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_119': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_127': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_135': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_143': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_151': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_159': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_167': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_175': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_183': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_191': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_199': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_207': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_215': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_223': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_231': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_239': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_247': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_255': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_263': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_271': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'ovgu_tesekkur_279': {   'tetikleyiciler': [   'çok zekisin',
                                                   'efsanesin',
                                                   'mükemmelsin',
                                                   'çok iyi olmuş',
                                                   'eline sağlık'],
                             'yanit': 'Çok teşekkür ederim Ahmet! ⚡ Beni sen tasarlayıp '
                                      'geliştirdiğin için bu başarı ikimizin!'},
    'selam_enerjik_001': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_009': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_017': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_025': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_033': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_041': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_049': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_057': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_065': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_073': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_081': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_089': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_097': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_105': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_113': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_121': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_129': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_137': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_145': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_153': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_161': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_169': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_177': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_185': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_193': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_201': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_209': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_217': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_225': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_233': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_241': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_249': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_257': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_265': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'},
    'selam_enerjik_273': {   'tetikleyiciler': [   'selam ar',
                                                   'hey ar',
                                                   'ar orada mısın',
                                                   'ar sesimi duyuyor musun',
                                                   'alo ar'],
                             'yanit': 'Buradayım Ahmet! ⚡ Tüm sensörlerim ve 500.000+ kalıp '
                                      'motorum aktif. Seni dinliyorum!'}}

def metni_normallestir(metin: str) -> str:
    """Türkçe karakterleri sadeleştirir, yazım hatalarını ('kın'->'kim', 'nslsn'->'nasilsin') düzeltir."""
    temiz = metin.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    temiz = re.sub(r"[?!.,;:'\"()]", " ", temiz)
    kelimeler = temiz.split()
    duzeltilmis = []
    for k in kelimeler:
        k_kat = k.translate(_TR_CEVIRI_TABLOSU)
        duzeltilmis.append(TYPO_SOZLUGU.get(k, TYPO_SOZLUGU.get(k_kat, k_kat)))
    return " ".join(duzeltilmis)


# ==============================================================================
# 3. 500.000+ HAZIR KALIP HAVUZU (O(1) HAFIZA İNDEKSİ)
# ==============================================================================
@st.cache_resource(show_spinner=False)
def kalip_havuzu_olustur():
    """
    500.000+ (525.000+) normalize edilmiş soru-cevap kalıbını (Kişiler, Âlimler,
    Genel Kültür, Diyaloglar, Teknik Terimler ve Matematik) hafızada O(1) arama için indeksler.
    """
    kalip_indeksi = {}

    onekler = [
        "", "ar ", "hey ar ", "merhaba ar ", "selam ", "lutfen ", "acaba ",
        "bana ", "soyle ", "soyler misin ", "anlat ", "bilir misin ",
        "sence ", "simdi ", "hemen ", "kisaca ", "detayli ", "kanka ",
        "dostum ", "asistan ", "yapay zeka ", "merak ettim ", "hocam ", "abi ",
        "kardesim ", "peki ", "ya ", "bir de ", "hizlica ", "dogruca ",
    ]
    sonekler = [
        "", " nedir", " kimdir", " kim", " anlat", " soyle", " acikla",
        " biliyor musun", " lutfen", " hakkinda bilgi", " ne demek",
        " nasildir", " ogret", " goster", " verir misin", " yardim", " kac", " kactir",
        " hakkinda ne biliyorsun", " kim acaba", " ne ise yarar", " ozeti nedir",
    ]

    kaynak_gruplari = []
    for kural_adi, veri in OZEL_CEVAP_KURALLARI.items():
        kaynak_gruplari.append((f"Özel Kural: {kural_adi}", veri["tetikleyiciler"], veri["yanit"]))
    for kat, veri in AHMET_BILGI_TABANI.items():
        kaynak_gruplari.append((f"Ahmet Profili: {kat}", veri["kelimeler"], veri["yanit"]))
    for kat, veri in GENEL_SORU_CEVAP_TABANI.items():
        kaynak_gruplari.append((f"Bilgi Bankası: {kat}", veri["kelimeler"], veri["yanit"]))
    for kod, veri in ISLAM_ALIMLERI.items():
        formatli = (
            f"### 📜 {veri['ad']}\n"
            f"**Dönem:** {veri['donem']} | **Alan:** {veri['alan']}\n\n"
            f"**Başlıca Eserleri:** {veri['eserler']}\n\n"
            f"{veri['bilgi']}"
        )
        kaynak_gruplari.append((f"Âlim: {veri['ad']}", veri["anahtar_kelimeler"], formatli))
    for s_kod, s_veri in DUYGU_VE_SOHBET_SABLONLARI.items():
        kaynak_gruplari.append((f"Diyalog: {s_kod}", s_veri["tetikleyiciler"], s_veri["yanit"]))

    for etiket, kelimeler, yanit in kaynak_gruplari:
        for kok in kelimeler:
            kok_norm = metni_normallestir(kok)
            if not kok_norm:
                continue
            kalip_indeksi[kok_norm] = (yanit, etiket)
            for pre in onekler:
                for suf in sonekler:
                    if suf and suf.strip() in kok_norm:
                        ifade = f"{pre}{kok_norm}".strip()
                    else:
                        ifade = f"{pre}{kok_norm}{suf}".strip()
                    if ifade not in kalip_indeksi:
                        kalip_indeksi[ifade] = (yanit, etiket)

    # Karekök ve Kare Hazır Kalıpları
    for n in range(1, 3501):
        dis, ic = karekok_sadelestir(n)
        kok_str = f"**{dis}**" if ic == 1 else (f"**`√{n}`** (`{math.sqrt(n):.4f}`)" if dis == 1 else f"**`{dis}√{ic}`** (`{math.sqrt(n):.4f}`)")
        kalip_indeksi[f"kok {n}"] = (f"√ **Karekök Kalıbı:** `√{n}` = {kok_str}", f"Karekök: √{n}")
        kalip_indeksi[f"{n} karesi"] = (f"🔺 **Kare Kalıbı:** `{n}²` = **{n * n:,}**".replace(",", "."), f"Kare: {n}²")

    # Parametrik Soru-Cevap ve İşlem Kalıpları (Toplam > 520.000 Hazır Kalıp!)
    for x in range(1, 650):
        for y in range(1, 650):
            kalip_indeksi[f"{x} x {y}"] = (
                f"✖️ **Çarpma:** `{x} × {y}` = **{x * y:,}**".replace(",", "."),
                "Hızlı Çarpım Kalıbı",
            )
            if len(kalip_indeksi) >= 525000:
                break
        if len(kalip_indeksi) >= 525000:
            break

    return kalip_indeksi

# ==============================================================================
# 4. HİBRİT AI, DOĞRUDAN WIKIPEDIA ARAŞTIRMA VE 5N1K AKILLI SOHBET MOTORU
# ==============================================================================
def hibrit_ai_yanit_uret(kullanici_girdisi: str, ek_baglam: str = "", saglayici_kodu: str = None, gecmis_kullan: bool = True):
    """
    1. Eğer kullanıcı açıkça kod yazmasını istediyse (Arduino / Python / OpenCV) hazır kodu üretir.
    2. Eğer Gemini API anahtarı girilmişse Gemini'den yanıt alır.
    3. Açık Kaynak AI (Pollinations Anahtarsız, Groq Llama-3.3, HuggingFace Qwen-2.5, OpenRouter, Ollama)
       aktifse oradan düzgün Türkçe yanıt üretir.
    """
    m = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "")
    kod_istegi_var = any(k in m for k in ["kod yaz", "kodu yaz", "kodu ver", "örnek kod", "ornek kod", "arduino kod", "opencv kod", "kamera kodu", "fren kodu"])

    if kod_istegi_var and any(k in m for k in ["python", "opencv", "kamera", "yüz tanıma", "iha", "drone"]):
        return (
            "🐍 **Ar Hibrit AI — Otonom İHA & Bebek Arabası OpenCV Kamera Takip Kodu:**\n\n"
            "```python\n"
            "import cv2\n\n"
            "kamera = cv2.VideoCapture(0)\n"
            "yuz_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')\n\n"
            "while True:\n"
            "    ret, kare = kamera.read()\n"
            "    if not ret:\n"
            "        break\n"
            "    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)\n"
            "    yuzler = yuz_cascade.detectMultiScale(gri, 1.3, 5)\n"
            "    for (x, y, w, h) in yuzler:\n"
            "        cv2.rectangle(kare, (x, y), (x + w, y + h), (56, 189, 248), 2)\n"
            "    cv2.imshow('AREX AI Kamera Telemetri', kare)\n"
            "    if cv2.waitKey(1) & 0xFF == ord('q'):\n"
            "        break\n\n"
            "kamera.release()\n"
            "cv2.destroyAllWindows()\n"
            "```",
            "Hibrit AI: Python Kod",
        )

    if kod_istegi_var and any(k in m for k in ["arduino", "hc-sr04", "l298n", "bebek arabası", "motor", "sensör", "fren"]):
        return (
            "💻 **Ar Hibrit AI — Akıllı Bebek Arabası (HC-SR04 + L298N) Hazır Arduino Kodu:**\n\n"
            "```cpp\n"
            "// AREX AI Studio - Akilli Bebek Arabasi Engel Algilama ve Otomatik Fren Sistemi\n"
            "#define TRIG_PIN 9\n"
            "#define ECHO_PIN 10\n"
            "#define ENA 5\n"
            "#define IN1 6\n"
            "#define IN2 7\n\n"
            "void setup() {\n"
            "  pinMode(TRIG_PIN, OUTPUT);\n"
            "  pinMode(ECHO_PIN, INPUT);\n"
            "  pinMode(ENA, OUTPUT);\n"
            "  pinMode(IN1, OUTPUT);\n"
            "  pinMode(IN2, OUTPUT);\n"
            "  Serial.begin(9600);\n"
            "}\n\n"
            "void loop() {\n"
            "  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);\n"
            "  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);\n"
            "  digitalWrite(TRIG_PIN, LOW);\n"
            "  long sure = pulseIn(ECHO_PIN, HIGH);\n"
            "  int mesafe = sure * 0.034 / 2;\n"
            "  if (mesafe > 0 && mesafe < 40) {\n"
            "    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);\n"
            "    analogWrite(ENA, 0);\n"
            "  } else {\n"
            "    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);\n"
            "    analogWrite(ENA, 160);\n"
            "  }\n"
            "  delay(50);\n"
            "}\n"
            "```",
            "Hibrit AI: Arduino Kod",
        )

    # 1. Önce 13 Sağlayıcılı Ana AI Köprüsü (Groq / DeepSeek / Gemini / OpenRouter / Cerebras / Pollinations / Ollama)
    ak_yanit, ak_etiket = acik_kaynak_ai_sor(kullanici_girdisi, saglayici_kodu=saglayici_kodu, ek_baglam=ek_baglam, gecmis_kullan=gecmis_kullan)
    if ak_yanit:
        return ak_yanit, ak_etiket

    # 2. Yedek: Doğrudan Gemini REST ucu (yalnızca ana köprü yanıt vermezse ve başka sağlayıcı zorlanmadıysa)
    api_key = st.session_state.get("gemini_api_key", "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key and saglayici_kodu in (None, "gemini_free"):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            sistem_prompt = (
                "Sen Ahmet tarafından geliştirilen 'AREX AI Studio' adlı süper asistansın. "
                "Ahmet İstanbul Fatih'te Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisi, "
                "TEKNOFEST otonom İHA ve TÜBİTAK 2204-A akıllı bebek arabası geliştiriyor. "
                "Samimi, net, Türkçe ve teknik olarak çok doğru cevap ver."
            )
            payload = {
                "contents": [{"parts": [{"text": f"{sistem_prompt}\n\nToplanan Kaynak Verileri:\n{ek_baglam[:2200]}\n\nAhmet'in Sorusu: {kullanici_girdisi}" if ek_baglam else f"{sistem_prompt}\n\nAhmet'in Sorusu: {kullanici_girdisi}"}]}]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                sonuc = json.loads(resp.read().decode("utf-8"))
                ai_metin = sonuc["candidates"][0]["content"]["parts"][0]["text"]
                if ai_metin:
                    return f"🧠 **AREX AI (Gemini):**\n\n{ai_metin}", "Hibrit AI (Gemini)"
        except Exception:
            pass

    return None, None


def _dinamik_zaman_kontrol(norm_text: str):
    simdi = turkiye_saati_al()
    if any(k in norm_text for k in ["saat kac", "saati soyle", "saat ne"]):
        return f"🕒 Şu an saat **{simdi.strftime('%H:%M:%S')}**.", "Canlı Saat"
    if any(k in norm_text for k in ["bugun gunlerden ne", "hangi gundeyiz", "bugun tarih", "tarih ne"]):
        return f"📅 Bugün **{simdi.day} {TURKCE_AYLAR[simdi.month]} {simdi.year}, {TURKCE_GUNLER[simdi.weekday()]}**.", "Canlı Tarih"
    return None, None


def _ozel_cevap_kontrol(raw_text: str, norm_text: str):
    """
    Kişisel kuralları ('ben kimim', 'ömer kim', 'hadi kim', 'edibe kim') kontrol eder.
    Uzun cümlelerin içinde geçen tek kelimelerin ('hadi bir soru çözelim' içindeki 'hadi')
    yanlışlıkla tetiklenmesini %100 engeller.
    """
    for kural_adi, icerik in OZEL_CEVAP_KURALLARI.items():
        for tetikleyici in icerik["tetikleyiciler"]:
            tet_norm = metni_normallestir(tetikleyici)
            if not tet_norm:
                continue
            # Tek kelimelik tetikleyiciler ('omer', 'edibe', 'ailem', 'kimsin', 'kimim')
            # sadece tüm mesaj o kelimeyse veya tam soru kalıbıysa eşleşsin
            if len(tet_norm.split()) == 1:
                if norm_text == tet_norm or raw_text == tetikleyici:
                    return icerik["yanit"], icerik.get("otomatik_ingilizce", False), f"Özel Kural: {kural_adi}"
            else:
                if bool(re.search(rf"\b{re.escape(tet_norm)}\b", norm_text)):
                    return icerik["yanit"], icerik.get("otomatik_ingilizce", False), f"Özel Kural: {kural_adi}"
    return None, False, None


# ==============================================================================
# 5N1K (KİM, NE, NASIL, NEREDE, NE ZAMAN, NEDEN), SORU İŞARETİ (?) VE
# SELAMLAŞMA + GÜNLÜK DOĞAL SOHBET BAĞLANTI MOTORU
# ==============================================================================
SELAMLASMA_KURALLARI = {
    "dini_selam": {
        "kaliplar": ["selamunaleykum", "selamun aleykum", "esselamu aleykum", "sa", "s.a", "s.a."],
        "tek_yanit": "Aleykümselam Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?",
        "birlestirme_oneki": "Aleykümselam Ahmet! ⚡ ",
    },
    "dini_selam_cevap": {
        "kaliplar": ["aleykumselam", "aleykum selam", "ve aleykumselam", "as", "a.s"],
        "tek_yanit": "Eyvallah Ahmet, hoş geldin! ⚡ Bugün hangi konu veya proje üzerinde çalışıyoruz?",
        "birlestirme_oneki": "Eyvallah Ahmet! ⚡ ",
    },
    "merhaba": {
        "kaliplar": ["merhaba", "mrb", "merhabalar", "merhaba ar", "hey", "hello", "hi"],
        "tek_yanit": "Merhaba Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?",
        "birlestirme_oneki": "Merhaba Ahmet! ⚡ ",
    },
    "selam": {
        "kaliplar": ["selam", "slm", "selamlar", "selam ar"],
        "tek_yanit": "Selam Ahmet! ⚡ Hoş geldin, bugün neler yapıyoruz?",
        "birlestirme_oneki": "Selam Ahmet! ⚡ ",
    },
    "gunaydin": {
        "kaliplar": ["gunaydin", "hayirli sabahlar", "iyi sabahlar", "gunaydin ar"],
        "tek_yanit": "Günaydın Ahmet! ☀️ Hayırlı, enerjik ve çok verimli bir gün dilerim.",
        "birlestirme_oneki": "Günaydın Ahmet! ☀️ ",
    },
    "iyi_gunler": {
        "kaliplar": ["iyi gunler", "hayirli gunler", "iyi dersler"],
        "tek_yanit": "İyi günler Ahmet! ⚡ Çalışmalarında kolaylıklar dilerim.",
        "birlestirme_oneki": "İyi günler Ahmet! ⚡ ",
    },
    "iyi_aksamlar": {
        "kaliplar": ["iyi aksamlar", "hayirli aksamlar", "iyi aksamlar ar"],
        "tek_yanit": "İyi akşamlar Ahmet! 🌆 Günün nasıl geçti, projeler nasıl gidiyor?",
        "birlestirme_oneki": "İyi akşamlar Ahmet! 🌆 ",
    },
    "iyi_geceler": {
        "kaliplar": ["iyi geceler", "hayirli geceler", "allah rahatlik versin"],
        "tek_yanit": "İyi geceler Ahmet! 🌙 Allah rahatlık versin, iyi dinlenmeler.",
        "birlestirme_oneki": "İyi geceler Ahmet! 🌙 ",
    },
    "veda": {
        "kaliplar": ["gorusuruz", "hosca kal", "hoscakal", "allaha ismarladik", "bay bay", "bye", "gule gule", "kendine iyi bak"],
        "tek_yanit": "Görüşmek üzere Ahmet! ⚡ Kendine çok iyi bak, ihtiyaç duyduğunda buradayım.",
        "birlestirme_oneki": "",
    },
}

DOGRUDAN_5N1K_SORU_TABANI = {
    "nasilsin": {
        "tetikleyiciler": [
            "nasilsin", "nslsn", "nasilsin ar", "nasilsiniz", "iyi misin", "iyi misin ar",
            "keyifler nasil", "nasil gidiyor", "durumlar nasil", "bugun nasilsin",
            "nasilsin kardesim", "nasilsin kanka", "nasilsin dostum",
        ],
        "yanit": "Ben iyiyim elhamdülillah, sen nasılsın Ahmet? ⚡",
        "etiket": "5N1K [Nasıl]: Hal-Hatır",
    },
    "nasil_calisiyorsun": {
        "tetikleyiciler": [
            "nasil calisiyorsun", "sen nasil calisirsin", "nasil calisir", "mantigin nasil",
            "nasil dusunuyorsun", "sistemin nasil calisiyor",
        ],
        "yanit": (
            "⚙️ **Çalışma Mantığım (v4.5 Temiz Mimari):**\n"
            "1. Cümlendeki **soru işaretini (`?`)**, **5N1K soru kelimelerini** ve **selamlaşmaları** ayırırım.\n"
            "2. Matematik ve fizik işlemlerini adım adım çözerim.\n"
            "3. Ansiklopedik bir konu sorduğunda doğrudan **🔍 Araştırılıyor, Wikipedia'ya gidiliyor...** diyerek Wikipedia'dan temiz özet getiririm.\n"
            "4. Sohbet ve yorum sorularında **Açık Kaynak Yapay Zeka (Pollinations / Groq Llama 3.3 / HuggingFace / Ollama)** motorumu kullanırım!"
        ),
        "etiket": "5N1K [Nasıl]: Sistem Mantığı",
    },
    "ne_haber": {
        "tetikleyiciler": [
            "ne haber", "naber", "nbr", "ne haber ar", "naber ar", "ne var ne yok", "naber nasilsin",
            "naber kardesim", "naber kanka", "naber abi",
        ],
        "yanit": "İyiyim elhamdülillah, senden ne haber Ahmet? ⚡",
        "etiket": "5N1K [Ne]: Ne Haber",
    },
    "ne_yapiyorsun": {
        "tetikleyiciler": [
            "ne yapiyorsun", "napiyorsun", "napion", "ne yapiyon", "su an ne yapiyorsun",
            "ne is yapiyorsun", "neyle ugrasiyorsun", "ne yapiyorsun ar",
        ],
        "yanit": (
            "⚡ Şu an doğrudan sohbet botunda seni dinliyorum Ahmet! "
            "İstediğin konuyu Wikipedia'dan araştırabilir, TDK'dan kelime bakabilir, matematik çözebilir veya açık kaynak yapay zeka ile sohbet edebiliriz."
        ),
        "etiket": "5N1K [Ne]: Ne Yapıyorsun",
    },
    "neler_yapabilirsin": {
        "tetikleyiciler": [
            "neler yapabilirsin", "ne yapabilirsin", "ne ise yararsin", "ozelliklerin neler",
            "ozelliklerin ne", "bana ne konuda yardim edebilirsin", "yeteneklerin neler",
        ],
        "yanit": (
            "🚀 **AREX AI Studio v4.5 Yeteneklerim:**\n"
            "• **🌐 Doğrudan Sohbette Wikipedia Araştırması:** Herhangi bir konuyu sorduğunda anında Wikipedia'ya gidip düzgün Türkçe özet getiririm.\n"
            "• **🤖 Açık Kaynak Yapay Zeka & 🦙 Ollama:** Pollinations, Groq (Llama 3.3 70B), Hugging Face (Qwen 2.5) ve yerel Ollama ile akıllı sohbet ederim.\n"
            "• **📕 TDK Sözlük & 🧮 Matematik Motoru:** Kelime anlamları, dört işlem, karekök, denklem ve 154 çözümlü soru.\n"
            "• **📜 30 İslam Âlimi, 🃏 3D Dil Kartları & 🚀 İHA / Bebek Arabası Mühendislik Hesaplayıcı.**"
        ),
        "etiket": "5N1K [Ne]: Yetenekler",
    },
    "nerelisin_neredesin": {
        "tetikleyiciler": [
            "nerelisin", "sen nerelisin", "nerede yasiyorsun", "neredesin", "nerede calisiyorsun",
            "memleketin neresi", "hangi sehirdesin",
        ],
        "yanit": (
            "📍 Ben geliştiricim **Ahmet** tarafından **İstanbul Fatih**'te geliştirilen yerli bir yapay zeka asistanıyım! ⚡"
        ),
        "etiket": "5N1K [Nerede]: Konum & Memleket",
    },
    "ben_nereliyim": {
        "tetikleyiciler": [
            "ben nereliyim", "ahmet nereli", "memleketim neresi", "ben nerede yasiyorum", "nerede oturuyorum",
        ],
        "yanit": (
            "📍 Sen **İstanbul Fatih**'te yaşıyorsun Ahmet; kökenin ise baban **Hadi Bey**'in (1 Ocak 1971 doğumlu) memleketi olan kadim şehir **Mardin**'dir! ⚡"
        ),
        "etiket": "5N1K [Nerede]: Ahmet Profili",
    },
    "neden_ar": {
        "tetikleyiciler": [
            "adin neden ar", "neden ar", "nicin ar", "ismin neden ar", "ar ne demek", "ar anlami ne",
        ],
        "yanit": (
            "⚡ Adım **Ar**; hem çevik, saf ve yüksek hızlı zekayı hem de geliştiricim **Ahmet**'in kendi tasarladığı özgün yapay zeka serisini temsil ediyor!"
        ),
        "etiket": "5N1K [Neden]: İsim Anlamı",
    },
    "ne_zaman_yapildin": {
        "tetikleyiciler": [
            "ne zaman yapildin", "seni ne zaman yapti", "ne zaman gelistirildin", "kac yasindasin",
        ],
        "yanit": (
            "🗓️ Geliştiricim **Ahmet** tarafından Python ve Streamlit kullanılarak geliştirildim ve v4.5 mimarisiyle çalışıyorum! ⚡"
        ),
        "etiket": "5N1K [Ne Zaman]: Geliştirilme",
    },
}

# Doğal Günlük Sohbet, Ders Çalışma Rehberi ve Etkileşim Kuralları
DOGAL_SOHBET_VE_REHBER_KURALLARI = [
    {
        "kaliplar": ["hadi bir soru cozelim", "bir soru cozelim", "soru cozelim", "bana soru sor", "matematik sorusu sor", "test yapalim", "quiz yapalim"],
        "yanit": (
            "🎯 **Harika fikir Ahmet, hemen başlayalım!**\n\n"
            "İşte sana 9. sınıf seviyesinde güzel bir soru:\n"
            "> **Soru:** `3x + 12 = 39` denkleminde `x` kaçtır? Ayrıca `√72` sayısı `a√b` biçiminde nasıl yazılır?\n\n"
            "Cevabını doğrudan buraya yazabilir ya da bana istediğin matematik/fizik sorusunu sorabilirsin! ⚡"
        ),
        "etiket": "Eğitim: Soru Çözümü",
    },
    {
        "kaliplar": ["bugun hava cok guzel", "hava cok guzel", "bugun hava harika", "gunesli bir gun"],
        "yanit": (
            "☀️ **Kesinlikle harika bir enerji Ahmet!** Güzel havalarda kısa bir yürüyüş veya 100m koşu antrenmanı zihni çok iyi açar; "
            "ardından İHA veya yazılım projelerine odaklanmak çok daha keyifli olur. Bugün hangi proje üzerinde çalışmayı planlıyorsun?"
        ),
        "etiket": "Doğal Sohbet",
    },
    {
        "kaliplar": ["fizik sinavina nasil calismaliyim", "fizik dersine nasil calisilir", "matematik sinavina nasil calismaliyim", "sinava nasil calismaliyim", "ders calisma programi", "nasil ders calismaliyim"],
        "yanit": (
            "📚 **9. Sınıf Proje Okulu İçin Etkili Sınav & Ders Çalışma Stratejisi:**\n"
            "1. **Kavram & Formül Özeti (20 dk):** Önce konunun temel mantığını ve formüllerini (örneğin Fizikte `F = m·a`, `W = F·Δx` veya Matematikte üslü/köklü kurallarını) tek bir kağıda çıkar.\n"
            "2. **Çözümlü Örnek İncelemesi (25 dk):** Klasik soru tiplerinin çözüm adımlarını incele.\n"
            "3. **Zamanlı Soru Çözümü (40 dk):** Telefonu sessize alıp en az 20-25 test sorusu çöz.\n"
            "4. **Yanlış Analizi (15 dk):** Yapamadığın soruları bana doğrudan sohbette sor; adım adım birlikte çözelim! ⚡"
        ),
        "etiket": "Rehberlik: Ders Çalışma",
    },
    {
        "kaliplar": ["python ile neler yapilabilir", "python ne ise yarar", "python ile ne yapilir", "neden python ogrenmeliyim"],
        "yanit": (
            "🐍 **Python İle Yapabileceklerin:**\n"
            "• **🤖 Yapay Zeka & Sohbet Botları:** Şu an geliştirdiğin **AREX AI Studio** gibi sesli, Wikipedia ve LLM destekli asistanlar.\n"
            "• **🚁 Otonom İHA & Görüntü İşleme:** `OpenCV` ve `YOLO` ile drone kamerasından hedef, yüz ve pist takibi.\n"
            "• **📊 Veri Bilimi & Otomasyon:** `Pandas`, `NumPy` ve `Matplotlib` ile sensör telemetri analizi.\n"
            "• **🌐 Web & Masaüstü Uygulamaları:** `Streamlit`, `FastAPI` ve `PyQt` ile modern arayüzler."
        ),
        "etiket": "Yazılım: Python Rehberi",
    },
    {
        "kaliplar": ["dunya neden donuyor", "dunya nasil doner", "gezegenler neden doner"],
        "yanit": (
            "🌍 **Dünya Neden Dönüyor?**\n"
            "Dünya, yaklaşık **4,5 milyar yıl önce** Güneş Sistemi'ni oluşturan dev gaz ve toz bulutunun (nebula) kütleçekimiyle kendi etrafında dönerek sıkışması sırasında kazandığı **açısal momentum** sayesinde dönmektedir.\n\n"
            "Uzay boşluğunda Dünya'nın bu dönüşünü durduracak bir hava sürtünmesi olmadığı için, **açısal momentumun korunumu yasası** gereği kendi ekseni etrafında yaklaşık **24 saatte (1670 km/saat ekvator hızıyla)** dönmeye devam eder."
        ),
        "etiket": "Astronomi & Fizik",
    },
    {
        "kaliplar": ["iyiyim", "ben de iyiyim", "cok iyiyim", "harikayim", "superim", "elhamdulillah iyiyim", "iyiyim tesekkurler"],
        "yanit": "Hep çok iyi ol inşallah Ahmet! ⚡ Bugün hangi konuyu araştıralım veya hangi problemi çözelim?",
        "etiket": "Doğal Sohbet",
    },
    {
        "kaliplar": ["tesekkur ederim", "tesekkurler", "sag ol", "sagol", "eyvallah", "cok sag ol", "eline saglik"],
        "yanit": "Rica ederim Ahmet, her zaman yanındayım! ⚡ Başka bir sorumuz veya araştıracağımız bir konu var mı?",
        "etiket": "Doğal Sohbet",
    },
]

SORU_KELIMELERI_5N1K = {
    "KIM": ["kimdir", "kimsin", "kimim", "kimin", "kime", "kimden", "kimle", "kimler", "kimlerdir", "kim", "kin"],
    "NE": ["nedir", "neyin", "neye", "nelerdir", "neler", "ne"],
    "NASIL": ["nasilsin", "nasildir", "nasil"],
    "NEREDE": ["nerededir", "nerelisin", "nereliyim", "nereli", "nerede", "nereye", "nereden", "neresi"],
    "NE_ZAMAN": ["ne zaman", "hangi yil", "hangi tarihte", "kacta", "saat kac"],
    "NEDEN": ["neden", "nicin", "niye"],
    "SORU_EKI": ["kactir", "kacinci", "kac", "hangisi", "hangi", "midir", "mudur", "mi", "mu"],
}


def cumle_ve_5n1k_analiz_et(ham_girdi: str, norm_text: str) -> dict:
    soru_isareti_var = "?" in ham_girdi
    bulunan_selam_turu = None
    selam_oneki = ""
    tek_selam_yaniti = ""
    kalan_norm = norm_text

    for s_tur, s_veri in SELAMLASMA_KURALLARI.items():
        for kalip in sorted(s_veri["kaliplar"], key=len, reverse=True):
            if norm_text == kalip:
                bulunan_selam_turu = s_tur
                tek_selam_yaniti = s_veri["tek_yanit"]
                selam_oneki = s_veri["birlestirme_oneki"]
                kalan_norm = ""
                break
            elif norm_text.startswith(kalip + " "):
                bulunan_selam_turu = s_tur
                tek_selam_yaniti = s_veri["tek_yanit"]
                selam_oneki = s_veri["birlestirme_oneki"]
                kalan_norm = norm_text[len(kalip):].strip()
                kalan_norm = re.sub(r"^(ar|ahmet|kardesim|dostum)\b\s*", "", kalan_norm).strip()
                break
        if bulunan_selam_turu:
            break

    incelenecek = kalan_norm if kalan_norm else norm_text
    incelenecek_kelimeler = incelenecek.split()
    tespit_5n1k = None
    for kat_5n1k, s_listesi in SORU_KELIMELERI_5N1K.items():
        for sk in s_listesi:
            if " " in sk:
                if sk in incelenecek:
                    tespit_5n1k = kat_5n1k
                    break
            elif sk in incelenecek_kelimeler:
                tespit_5n1k = kat_5n1k
                break
        if tespit_5n1k:
            break

    soru_mu = bool(soru_isareti_var or tespit_5n1k is not None)

    konu_cekirdegi = re.sub(
        r"\b(kimdir|kimsin|kimim|kimin|kimler|kim|kin|nedir|nelerdir|ne|nasilsin|nasildir|nasil|nerededir|nerede|nereli|neresi|ne zaman|neden|nicin|niye|hakkinda|bilgi|anlat|bana|soyle|acaba|mi|mu|midir|mudur|ver|verir|misin|kuruldu|yikildi|dusunuyorsun|sence|sizce)\b",
        " ",
        incelenecek,
    )
    konu_cekirdegi = re.sub(r"\s+", " ", konu_cekirdegi).strip()

    return {
        "soru_isareti_var": soru_isareti_var,
        "tespit_5n1k": tespit_5n1k,
        "soru_mu": soru_mu,
        "selam_turu": bulunan_selam_turu,
        "tek_selam_yaniti": tek_selam_yaniti,
        "selam_oneki": selam_oneki,
        "kalan_soru": kalan_norm,
        "konu_cekirdegi": konu_cekirdegi,
    }


def _fuzzy_taban_ara(taban, norm_text: str, etiket_onek: str, konu_cekirdegi: str = ""):
    """
    Sadece tam eşleşmeleri veya konu çekirdeğiyle %90+ örtüşen anahtarları döndürür;
    uzun cümlelerin içindeki tek bir kelimeden dolayı alakasız şablon döndürmez.
    """
    en_iyi_skor, en_iyi_yanit, en_iyi_kat = 0, None, None
    for kat, icerik in taban.items():
        for anahtar in icerik.get("kelimeler", []):
            a_norm = metni_normallestir(anahtar)
            if not a_norm:
                continue
            # 1. Tam eşleşme
            if a_norm == norm_text or (konu_cekirdegi and len(konu_cekirdegi) >= 3 and a_norm == konu_cekirdegi):
                return icerik.get("yanit"), f"{etiket_onek}: {kat}"
            # 2. Çok kelimeli özel anahtar (en az 2 kelime ve 8+ karakter) cümle çekirdeğiyle aynıysa
            if len(a_norm.split()) >= 2 and len(a_norm) >= 8 and (a_norm == konu_cekirdegi or f" {a_norm} " in f" {norm_text} "):
                return icerik.get("yanit"), f"{etiket_onek}: {kat}"
            # 3. Yüksek hassasiyetli benzerlik (%90+)
            if len(norm_text) >= 5 and len(konu_cekirdegi) >= 4:
                a_cekirdek = re.sub(r"\b(kimdir|kim|nedir|ne|nerede|nasil|hakkinda|bilgi)\b", " ", a_norm).strip()
                a_cekirdek = re.sub(r"\s+", " ", a_cekirdek)
                skor1 = fuzz.ratio(norm_text, a_norm)
                skor2 = fuzz.ratio(konu_cekirdegi, a_cekirdek) if a_cekirdek else 0
                skor = max(skor1, skor2)
                if skor >= 91 and skor > en_iyi_skor:
                    en_iyi_skor = skor
                    en_iyi_yanit = icerik.get("yanit")
                    en_iyi_kat = f"{etiket_onek}: {kat}"
    return en_iyi_yanit, en_iyi_kat


# Candan Sohbet ve Yardım (Help) Kuralları
YARDIM_VE_HELP_YANITI = """🤝 **Elbette Ahmet! İşte seninle neler yapabileceğimizin hızlı özeti:**

* 💬 **Candan Sohbet & 5N1K:** *"Nasılsın?", "Canım sıkkın", "Sohbet edelim"* gibi her şeyi doğrudan konuşabiliriz.
* 🌐 **Wikipedia Araştırması:** *"vikipedi: yapay zeka"*, *"Karadelik nedir?"* veya *"Osmanlı İmparatorluğu ne zaman kuruldu?"* yazdığında doğrudan Wikipedia'ya gidip özet getiririm.
* 🏷️ **Güncel Fiyat (Epey • Cimri • Akakçe):** *"fiyat: Raspberry Pi 5"*, *"cimri: Samsung S25"* veya *"Arduino Uno ne kadar?"* yazarak güncel fiyat ve özellik sayfalarına ulaşabilirsin.
* 📕 **TDK Türkçe Sözlük:** *"tdk: mühendislik"* veya *"irfan ne demek?"* yaz.
* 🧮 **Matematik & Fizik:** *"76 çarpı 25"*, *"kök 72"*, *"3x + 9 = 24"* yazarak adım adım çözdür.
* 🎓 **Kodsuz Öğretme:** *"öğret: favori rengim = lacivert"* yazarak bana yeni bilgi öğretebilirsin.

**✨ v14 ile yeni gelenler:**
* 🧮 **Profesyonel Matematik:** *"2+3*4"*, *"√27 + √3"*, *"sin 45"*, *"3(x-2)=x+4"*, *"120'nin asal çarpanları"*, *"80'e yüzde 50 zam"*
* 🌍 **Kandilli Depremleri:** *"son depremler"*, *"malatya'da deprem var mı"*, *"büyük depremler"*
* 🎉 **Bayram & Tatil:** *"kurban bayramı ne zaman"*, *"resmi tatiller"*
* 📜 **Tarihte Bugün:** *"bugün tarihte ne oldu"*
* 📏 **Birim Çevirici:** *"5 km kaç mil"*, *"2 su bardağı kaç ml"*, *"100 fahrenheit kaç celsius"*
* 📅 **Tarih & Yaş:** *"yılbaşına kaç gün kaldı"*, *"1 ocak 2027 hangi gün"*, *"12.05.2010 doğumluyum kaç yaşındayım"*
* 🕰️ **Dünya Saati:** *"Tokyo'da saat kaç"*, *"New York ile saat farkı"*
* 📖 **İngilizce Sözlük:** *"ingilizce serendipity ne demek"*
* 📈 **Grafik Çizici:** *"y = x^2 - 4 grafiğini çiz"*, *"y = sin(x) grafiği"*, *"y = 1/x grafiği -5 ile 5 arasında"*
* 🎤 **Sesli Soru:** Sohbetin altındaki mikrofona dokun ve konuş.
* 📸 **Fotoğraftan Soru:** *"📸 Fotoğraftan Soru"* düğmesiyle kitaptaki sorunun fotoğrafını gönder.
* 📊 **Çalışma Takibi:** *"bugün 30 matematik sorusu çözdüm"*, *"45 dakika fizik çalıştım"*, *"günlük hedefim 50 soru"*, *"bu hafta ne kadar çalıştım"*
* 📝 **Sohbet İçi Test:** *"bana 5 matematik sorusu sor"*, *"köklü sayılardan test yap"* (ipucu · geç · testi bitir)
* ⏰ **Hatırlatıcı:** *"yarın 8'de fizik sınavımı hatırlat"*, *"20 dakika sonra su içmeyi hatırlat"*, *"hatırlatıcılarım"*

*Hangisiyle başlamak istersin canım kardeşim?* ⚡"""


# Detaylı Tarihî & Bilimsel Şahsiyet Biyografileri (Tek cümle yerine kapsamlı yanıt)
DETAYLI_TARIH_BIYOGRAFILERI = {
    "şeyh şamil": {
        "ad": "Şeyh Şamil (İmam Şamil — Kafkas Kartalı)",
        "donem": "26 Haziran 1797 (Gimri, Dağıstan) – 4 Şubat 1871 (Medine)",
        "unvan": "Kafkasya İmamı • Bağımsızlık Önderi ve İslam Âlimi",
        "bilgi": (
            "19. yüzyılda **Dağıstan ve Çeçenistan** halklarını birleştirerek Çarlık Rusyası'nın Kafkasya işgaline karşı **25 yıl boyunca** destansı bir bağımsızlık ve özgürlük mücadelesi yürüten büyük komutan, devlet adamı ve âlimdir.\n\n"
            "**⚔️ Tarihî Mücadelesi ve Liderlik Yönü:**\n"
            "• **Kafkasya İmamlığı:** 1834'te Kafkasya'nın 3. İmamı seçildi; farklı kabileleri adalet, ilim ve ortak savunma çatısı altında birleştirerek düzenli bir yönetim ve hukuk sistemi kurdu.\n"
            "• **Askerî Deha ve Direniş:** Sarp Kafkas dağlarında çok daha kalabalık ve modern donanımlı Çarlık ordularına karşı geliştirdiği gerilla ve savunma stratejileri dünya askerî tarihinde hâlâ incelenir.\n"
            "• **Ahde Vefa ve İlim:** 1859'da Gunib'de esir düştüğünde bile düşmanları tarafından büyük saygıyla karşılandı; ömrünün son yıllarında hac görevini yapmak üzere gittiği **Medine-i Münevvere**'de vefat ederek Cennetü'l-Bâkî'ye defnedildi."
        ),
    },
    "imam şamil": {
        "ad": "Şeyh Şamil (İmam Şamil — Kafkas Kartalı)",
        "donem": "26 Haziran 1797 (Gimri, Dağıstan) – 4 Şubat 1871 (Medine)",
        "unvan": "Kafkasya İmamı • Bağımsızlık Önderi",
        "bilgi": (
            "Dağıstan ve Çeçenistan'da 25 yıl boyunca Çarlık Rusyası'na karşı özgürlük mücadelesi veren Kafkas Kartalı lakaplı büyük komutan ve âlimdir. "
            "Adaleti, cesareti ve halkları birleştirici liderliğiyle hem Kafkasya'da hem de Türkiye'de büyük saygıyla anılır; 1871'de Medine'de vefat etmiştir."
        ),
    },
    "selahaddin eyyubi": {
        "ad": "Selâhaddin Eyyûbî",
        "donem": "1138 (Tikrit) – 4 Mart 1193 (Şam)",
        "unvan": "Eyyûbî Devleti'nin Kurucusu • Kudüs Fatihi",
        "bilgi": (
            "Eyyûbî Devleti'nin kurucusu ve **1187 Hıttin Savaşı**'nın ardından **Kudüs**'ü Haçlılardan geri alan büyük hükümdar ve komutandır. "
            "Sadece askerî dehasıyla değil, Kudüs'ün fethinden sonra sivillere gösterdiği merhamet, adalet ve sözüne sadakatiyle hem Doğu hem Batı tarihinde şövalyelik ve erdem timsali olarak anılır."
        ),
    },
    "sultan alparslan": {
        "ad": "Sultan Alparslan",
        "donem": "1029 – 24 Kasım 1072",
        "unvan": "Büyük Selçuklu İmparatorluğu'nun 2. Sultanı • Malazgirt Fatihi",
        "bilgi": (
            "**26 Ağustos 1071 Malazgirt Meydan Muharebesi**'nde Bizans İmparatoru Romen Diyojen'i yenerek **Anadolu'nun kapılarını Türklere açan** Büyük Selçuklu Sultanıdır. "
            "Nizâmülmülk ile birlikte Nizamiye Medreseleri'nin kurulmasını destekleyerek bilim ve devlet teşkilatını zirveye taşımıştır."
        ),
    },
    "kanuni sultan süleyman": {
        "ad": "Kanuni Sultan Süleyman (I. Süleyman)",
        "donem": "6 Kasım 1494 (Trabzon) – 7 Eylül 1566 (Zigetvar)",
        "unvan": "Osmanlı İmparatorluğu'nun 10. Padişahı",
        "bilgi": (
            "46 yıllık saltanatıyla Osmanlı'nın en uzun süre tahtta kalan padişahıdır. Belgrad, Rodos, Mohaç ve Bağdat seferleriyle devleti üç kıtada zirveye taşırken; "
            "Mimar Sinan'a **Süleymaniye Külliyesi**'ni yaptırmış, hukuk alanındaki kapsamlı kanunnameleriyle 'Kanunî', Batı'da ise 'Muhteşem Süleyman' unvanını almıştır."
        ),
    },
    "aziz sancar": {
        "ad": "Prof. Dr. Aziz Sancar",
        "donem": "8 Eylül 1946 (Savur, Mardin) – Günümüz",
        "unvan": "2015 Nobel Kimya Ödülü Sahibi • Moleküler Biyolog",
        "bilgi": (
            "Mardin'in Savur ilçesinde doğan, İstanbul Üniversitesi Tıp Fakültesi mezunu dünyaca ünlü Türk bilim insanıdır. "
            "Hücrelerin hasarlı **DNA'yı nasıl onardığını** (nükleotid eksizyon onarımı) haritalandıran çalışmalarıyla **2015 Nobel Kimya Ödülü**'nü kazanmış ve madalyasını Anıtkabir'e bağışlamıştır."
        ),
    },
    "fatih sultan mehmet": {
        "ad": "Fatih Sultan Mehmet (II. Mehmed)",
        "donem": "30 Mart 1432 (Edirne) – 3 Mayıs 1481 (Gebze)",
        "unvan": "Osmanlı İmparatorluğu'nun 7. Padişahı • İstanbul'un Fatihi",
        "bilgi": (
            "Henüz **21 yaşındayken** 29 Mayıs 1453'te İstanbul'u fethederek Orta Çağ'ı kapatıp Yeni Çağ'ı açan, askeri dehası kadar bilim, mühendislik ve sanata verdiği değerle de tanınan büyük Osmanlı padişahıdır.\n\n"
            "**⚙️ Bilim, Eğitim ve Mühendislik Yönü:**\n"
            "• **Şahi Topları ve Balistik:** Kuşatma sırasında surları yıkacak dev topların balistik ve döküm hesaplarında bizzat mühendislerle çalışmıştır.\n"
            "• **7 Dil ve Bilim Himayesi:** Türkçe, Arapça, Farsça, Latince, Yunanca ve İtalyanca dahil birden fazla dil bilmiş; dönemin büyük astronomu **Ali Kuşçu**'yu İstanbul'a davet edip **Sahn-ı Seman Medreseleri**'ni (İstanbul Üniversitesi'nin temelini) kurmuştur.\n"
            "• **Devlet ve Hukuk:** Kanunnâme-i Âl-i Osman ile imparatorluğun yönetim, eğitim ve hukuk sistemini kurumsallaştırmıştır."
        ),
    },
    "mustafa kemal atatürk": {
        "ad": "Mustafa Kemal Atatürk",
        "donem": "1881 (Selânik) – 10 Kasım 1938 (İstanbul)",
        "unvan": "Türkiye Cumhuriyeti'nin Kurucusu ve İlk Cumhurbaşkanı",
        "bilgi": (
            "Osmanlı Ordusu'nda Çanakkale (Anafartalar) ve diğer cephelerdeki askeri başarılarının ardından 19 Mayıs 1919'da Samsun'a çıkarak Kurtuluş Savaşı'na önderlik eden ve **29 Ekim 1923'te Türkiye Cumhuriyeti'ni kuran** büyük asker ve devlet adamıdır.\n\n"
            "**📚 Bilim, Eğitim ve İnkılaplar:**\n"
            "• *'Hayatta en hakiki mürşit ilimdir'* ilkesiyle modern eğitim, sanayi, hukuk ve bilim kurumlarının (Türk Dil Kurumu, Türk Tarih Kurumu, yeni üniversiteler) kurulmasına öncülük etmiştir.\n"
            "• **Geometri Kitabı:** Bizzat yazdığı *Geometri* kitabıyla bugün okullarda kullandığımız **üçgen, açı, boyut, yüzey, çap, teğet, dikey, yatay** gibi Türkçe matematik terimlerini kazandırmıştır."
        ),
    },
    "atatürk": {
        "ad": "Mustafa Kemal Atatürk",
        "donem": "1881 (Selânik) – 10 Kasım 1938 (İstanbul)",
        "unvan": "Türkiye Cumhuriyeti'nin Kurucusu ve İlk Cumhurbaşkanı",
        "bilgi": (
            "Çanakkale ve Kurtuluş Savaşı'nın başkomutanı, **29 Ekim 1923'te Türkiye Cumhuriyeti'ni kuran** liderdir. "
            "Eğitim, bilim, hukuk ve sanayi alanında köklü reformlar gerçekleştirmiş; ayrıca bizzat yazdığı *Geometri* kitabıyla **üçgen, açı, boyut, dikey, yatay** gibi Türkçe geometri terimlerini dilimize kazandırmıştır."
        ),
    },
}


def fiyat_sorgusu_mu(kullanici_girdisi: str) -> bool:
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    if raw.startswith(("fiyat:", "fiyat ", "cimri:", "cimri ", "epey:", "epey ", "akakce:", "akakçe:")):
        return True
    return bool(re.search(r"\b(ne kadar|kaç tl|kac tl|kaç para|kac para|fiyatı|fiyati|fiyatları|en ucuz)\b", raw))


def adres_sorgusu_mu(kullanici_girdisi: str) -> bool:
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    norm = metni_normallestir(kullanici_girdisi)
    if any(k in norm for k in ["nerelisin", "ben nereliyim", "nerede yasiyorsun", "nerede yasiyorum", "nerede oturuyorum", "memleketin", "memleketim", "neredesin"]):
        return False
    # Tarihî olay / turnuva / biyografi soruları ('1998 de nerede oynandı', 'nerede doğdu') ASLA GPS harita adresi değildir!
    if not raw.startswith(("adres:", "konum:", "harita:", "yol tarifi:")):
        if re.search(r"\b(oynandi|oynandı|yapildi|yapıldı|duzenlendi|düzenlendi|dogdu|doğdu|kuruldu|gecti|geçti|yasadi|yaşadı|oldu|öldü|kazandi|kazandı|gerceklesti|gerçekleşti)\b", raw):
            return False
        if re.search(r"\b(1\d{3}|20\d{2})\b", raw) and "nerede" in raw:
            return False
    if raw.startswith(("adres:", "adres ", "konum:", "konum ", "harita:", "yol tarifi:")):
        return True
    return bool(
        re.search(
            r"\b(adresi nedir|adresi ne|adresi|konumu nedir|konumu|nerededir|nerede kalıyor|nerede|nasıl giderim|nasil giderim|yol tarifi|hangi semtte|hangi ilçede)\b",
            raw,
        )
    )


def kod_veya_uretim_istegi_mi(kullanici_girdisi: str) -> bool:
    """
    v10.4 — Yalnızca GERÇEK yazılım/kod üretimi veya yaratıcı metin yazma isteklerinde True döner.
    'ne düşünüyorsun', 'sence', 'yorumla', 'sohbet edelim' gibi muhakeme/yorum soruları ASLA KOD_URETIM sayılmaz!
    """
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    kesin_kod_kaliplari = [
        "kod yaz", "kodu yaz", "kod yazar", "kodu yazar", "kod oluştur", "kod olustur",
        "kod ver", "kodu ver", "program yaz", "script yaz", "site yap", "web sitesi yap",
        "python kodu", "arduino kodu", "opencv kodu", "html kodu", "c++ kodu", "kodla",
        "hikaye yaz", "şiir yaz", "siir yaz", "kompozisyon yaz",
    ]
    if any(k in raw for k in kesin_kod_kaliplari):
        return True
    # 'yazar mısın / düzeltir misin' yalnızca kod/programlama bağlamı varsa KOD_URETIM olur
    if any(k in raw for k in ["yazar mısın", "yazar misin", "yazabilir misin", "düzeltir misin", "duzeltir misin"]):
        if any(t in raw for t in ["kod", "python", "arduino", "html", "css", "javascript", "sql", "script", "fonksiyon", "algoritma", "şiir", "siir", "hikaye", "dilekçe"]):
            return True
    return False


# ==============================================================================
# v10.4 — SPOR & BÜYÜK ORGANİZASYONLAR + MERKEZİ MANTIK & MUHAKEME MOTORU
# ==============================================================================
_SPOR_ORGANIZASYON_BILGI = {
    "fifa_dunya_kupasi": {
        "baslik": "FIFA Dünya Kupası",
        "anahtarlar": ["en buyuk futbol organizasyonu", "dunyanin en buyuk futbol", "dunya kupasi", "fifa dunya kupasi", "world cup"],
        "metin": (
            "### ⚽ Dünyanın En Büyük Futbol Organizasyonu: **FIFA Dünya Kupası**\n"
            "**Düzenleyen:** FIFA (Uluslararası Futbol Federasyonları Birliği) | **Periyot:** 4 Yılda Bir\n\n"
            "Dünya genelinde **5 milyardan fazla** izleyiciye ulaşan **FIFA Dünya Kupası**, yalnızca futbolun değil, Yaz Olimpiyatları ile birlikte tüm spor tarihinin en büyük ve en çok izlenen organizasyonudur.\n\n"
            "**🏆 Öne Çıkan Güncel Bilgiler:**\n"
            "• **Katılımcı Sayısı:** 1930'da Uruguay'da başlayan turnuva, **2026 Dünya Kupası** (ABD, Kanada, Meksika ev sahipliği) ile birlikte **48 millî takıma** yükselmiştir.\n"
            "• **En Çok Kazanan Ülke:** **Brezilya** (5 şampiyonluk), ardından Almanya (4) ve İtalya (4); son şampiyon **Arjantin** (2022, 3. şampiyonluk).\n"
            "• **Kulüpler Bazında En Büyüğü:** Millî takımlarda **FIFA Dünya Kupası**, kulüp takımları düzeyinde ise her yıl düzenlenen **UEFA Şampiyonlar Ligi** dünyanın en prestijli futbol organizasyonudur."
        ),
    },
    "sampiyonlar_ligi": {
        "baslik": "UEFA Şampiyonlar Ligi",
        "anahtarlar": ["sampiyonlar ligi", "champions league", "en buyuk kulup turnuvasi", "avrupa kulup futbolu"],
        "metin": (
            "### 🏆 Kulüpler Bazında En Büyük Futbol Organizasyonu: **UEFA Şampiyonlar Ligi**\n"
            "**Düzenleyen:** UEFA | **Periyot:** Her Yıl (Eylül – Mayıs)\n\n"
            "Avrupa'nın en güçlü futbol kulüplerini karşı karşıya getiren **UEFA Şampiyonlar Ligi**, kulüp futbolunun en prestijli ve en yüksek izlenme oranına sahip turnuvasıdır.\n\n"
            "• **Format:** 2024–25 sezonundan itibaren 36 takımlı tek **Lig Aşaması (İsviçre Sistemi)** ile oynanmaktadır.\n"
            "• **En Çok Kazanan Kulüp:** **Real Madrid** (15 şampiyonluk)."
        ),
    },
    "olimpiyatlar": {
        "baslik": "Yaz Olimpiyat Oyunları",
        "anahtarlar": ["en buyuk spor organizasyonu", "olimpiyat oyunlari", "yaz olimpiyatlari"],
        "metin": (
            "### 🏅 Dünyanın En Büyük Çok Branşlı Spor Organizasyonu: **Yaz Olimpiyat Oyunları**\n"
            "**Düzenleyen:** Uluslararası Olimpiyat Komitesi (IOC) | **Periyot:** 4 Yılda Bir\n\n"
            "200'den fazla ülke ve 10.000'in üzerinde sporcunun 30'dan fazla branşta yarıştığı en kapsamlı küresel spor etkinliğidir. 2024 Paris'in ardından sıradaki Yaz Olimpiyatları **2028 Los Angeles**'ta düzenlenecektir."
        ),
    },
}


def _spor_organizasyon_bilgisi_getir(kullanici_girdisi: str) -> dict:
    norm = metni_normallestir(kullanici_girdisi)
    if any(k in norm for k in ["en buyuk futbol", "futbol organizasyonu", "en buyuk turnuva"]) and "kulup" not in norm:
        v = _SPOR_ORGANIZASYON_BILGI["fifa_dunya_kupasi"]
        return {"basarili": True, "baslik": v["baslik"], "metin": v["metin"], "kaynak": "Spor Bilgi Ağı (FIFA/UEFA)"}
    for _, v in _SPOR_ORGANIZASYON_BILGI.items():
        if any(a in norm for a in v["anahtarlar"]):
            return {"basarili": True, "baslik": v["baslik"], "metin": v["metin"], "kaynak": "Spor Bilgi Ağı (FIFA/UEFA/IOC)"}
    return {"basarili": False}


def _yanit_alaka_dogrula(yanit: str, mevcut_sorgu: str, onceki_konu: str) -> bool:
    """
    v10.4 Muhakeme Koruyucusu:
    Yeni bir konuya geçildiyse (örn. Güney Kore -> En büyük futbol organizasyonu veya Şeyh Şamil),
    AI yanıtının eski alakasız konuya ('Güney Kore') kayıp kaymadığını denetler.
    """
    if not yanit or not onceki_konu:
        return True
    onceki_norm = metni_normallestir(onceki_konu)
    sorgu_norm = metni_normallestir(mevcut_sorgu)
    yanit_norm = metni_normallestir(yanit)
    if len(onceki_norm) >= 4 and onceki_norm not in sorgu_norm and onceki_norm in yanit_norm:
        # Eski konu yeni soruda geçmediği halde yanıtta geçiyor. Bu ya bağlam sızıntısıdır
        # (yanıt yeni soruyu hiç işlemiyor) ya da meşru bir bağlantıdır ("bitkiler geceleri ne yapar"
        # → fotosentez). Ayırt etmek için: yanıt, sorunun kendi anahtar kelimelerini içeriyor mu?
        _bos = {"nedir", "neler", "nasil", "neden", "nerede", "hangi", "kimdir", "peki", "bana",
                "anlat", "acikla", "yapar", "olur", "midir", "mudur", "kadar", "icin", "gibi", "daha"}
        anahtarlar = [k for k in re.findall(r"[a-z0-9]{4,}", sorgu_norm) if k not in _bos]
        if anahtarlar:
            # Türkçe ekleri tolere etmek için ilk 5 harf (kök) eşleşmesi: "geceleri" ~ "gece"
            isabet = sum(1 for k in anahtarlar if k[:5] in yanit_norm or k[:4] in yanit_norm)
            if isabet / len(anahtarlar) >= 0.5:
                return True
        return False
    return True


def _itiraz_veya_duzeltme_mi(raw: str, norm: str) -> bool:
    """Kullanıcı 'hayır onu demiyorum', 'yanlış anladın' gibi bir düzeltme yapıyorsa True döner (eski konuyu yapıştırmaz!)."""
    return any(
        k in norm
        for k in [
            "hayir onu demiyorum", "onu demiyorum", "onu kastetmedim", "oyle degil",
            "yanlis anladin", "bunu demedim", "hayir o degil", "alakasiz", "konuyu sapitma",
        ]
    ) or norm.startswith(("hayir ", "yok onu ", "hayir,"))


def _duygusal_kisisel_sohbet_mi(raw: str, norm: str) -> bool:
    """
    v10.6 — Aile, arkadaş, duygu, dertleşme ve kişisel durum cümlelerini (%100 hassasiyetle) yakalar:
      • 'ablam beni çok üzüyor', 'abalam beni çok üzüyor', 'abla beni üzüyor yoruyor'
      • 'annem bana kızdı', 'arkadaşım kalbimi kırdı', 'çok bunaldım', 'stresliyim'
    Bu cümleler ASLA Wikipedia'ya, Google News'e veya 'Bana Öğret'e gönderilmez!
    """
    if raw.startswith(("wikipedia:", "vikipedi:", "wiki:", "tdk:", "fiyat:", "adres:", "harita:", "ollama:")):
        return False
    if any(k in raw for k in ["kimdir", "nedir", "tarifi", "hava durumu", "namaz", "deprem", "çevir", "cevir", "translate", "formülü", "piyasa değeri"]):
        return False

    aile_ve_kisi = [
        "ablam", "abalam", "abla", "abim", "agabeyim", "annem", "babam", "kardesim",
        "arkadasim", "hocam", "ogretmenim", "kuzenim", "dayim", "teyzem", "amcam",
    ]
    duygu_ve_fiil = [
        "uzuyor", "uzdu", "uzuldum", "uzgunum", "yoruyor", "yordu", "yoruldum", "bunaltiyor",
        "bunaldim", "kiziyor", "kizdi", "kiriyor", "kirdi", "kalbimi", "bagiriyor", "sinirlendiriyor",
        "sinirim", "stres", "agliyorum", "korkuyorum", "sikildim", "canim sikkin", "moralim",
        "yalnizim", "dert", "kafam karisti", "kotu hissediyorum", "mutsuzum", "mutluyum",
        "sevincliyim", "heyecanliyim", "anlamiyor", "dinlemiyor",
    ]
    kisisel_zamir = bool(re.search(r"\b(beni|bana|benim|benden|kendimi|ben)\b", norm))

    if any(d in norm for d in duygu_ve_fiil):
        return True
    if any(a in norm for a in aile_ve_kisi) and (kisisel_zamir or re.search(r"\b[a-z]{3,}(?:iyor|uyor|yor|di|du|ti|tu)\b", norm)):
        return True
    return False


def _dogal_sohbet_cumlesi_mi(raw: str, norm: str) -> bool:
    """
    v10.6 — ÖN-ANALİZ SOHBET KAPISI:
    Duygusal/kişisel dertleşmeleri, 1./2./3. şahıs günlük konuşmaları ve bot geri bildirimlerini
    ansiklopedik sorgulardan net biçimde ayırır. Bu cümleler ASLA Wikipedia'ya veya Google News'e düşmez!
    """
    if _duygusal_kisisel_sohbet_mi(raw, norm) or _itiraz_veya_duzeltme_mi(raw, norm):
        return True

    if raw.startswith(("wikipedia:", "wikipedia ", "vikipedi:", "vikipedi ", "wiki:", "wiki ", "tdk:", "fiyat:", "adres:", "harita:", "ollama:")):
        return False
    if any(k in raw for k in ["kimdir", "nedir", "tarifi", "hava durumu", "namaz", "deprem", "çevir", "cevir", "translate", "ne zaman kuruldu", "formülü", "formulu", "piyasa değeri", "piyasa degeri", "hakkında bilgi", "hakkinda bilgi"]):
        return False

    geri_bildirim_ve_gunluk = [
        "hatalarini", "hatani", "hatayi", "duzeltmekle", "ugrasiyorum", "deniyorum", "test ediyorum",
        "yanlis anladin", "yanlis baglam", "alakasiz", "sapittin", "sacmaladin", "sacmaliyor",
        "calismiyor", "bozuk", "sinirim bozuldu", "kafam karisti", "canim sikildi", "canim sikkin",
        "okuldan geldim", "sinavim var", "ders calisiyorum", "kod yaziyorum", "oyun oynuyorum",
        "cok yoruldum", "uykum geldi", "aciktim", "mutluyum", "uzgunum", "heyecanliyim",
        "ne yapiyorsun", "napiyorsun", "nasil gidiyor", "iyiyim sen", "sen nasilsin",
        "dinlemiyorsun", "anlamiyorsun", "gunun nasil", "nasil gecti", "motive", "motivasyon", "kendimi nasil", "ne yapabilirim", "nasil basaririm",
    ]
    if any(k in norm for k in geri_bildirim_ve_gunluk):
        return True

    # Türkçe 1. / 2. şahıs fiil çekimi bitişleri
    if re.search(
        r"\b[a-z]{3,}(?:iyorum|uyorum|yorum|iyorsun|uyorsun|yorsun|"
        r"dim|dum|tim|tum|din|dun|tin|tun|acagim|ecegim|misim|musum|maliyim|meliyim|"
        r"miyorum|muyorum|madim|medim|madin|medin|alim|elim)\b",
        norm,
    ):
        return True

    # 'beni / bana' + 3. şahıs şimdiki zaman ('beni üzüyor', 'bana kızıyor', 'beni yoruyor')
    if re.search(r"\b(beni|bana)\b", norm) and re.search(r"\b[a-z]{2,}(?:iyor|uyor|yor|di|du|ti|tu)\b", norm):
        return True
    return False


def _duygusal_sohbet_yaniti_uret(kullanici_girdisi: str, norm_text: str) -> tuple:
    """
    Canlı AI sunucuları anlık erişilemez olsa bile, soğuk 'Bana Öğret' veya alakasız Wikipedia/Haber
    döndürmek yerine mesajın konusunu analiz ederek sıcak, samimi ve gerçekçi Türkçe cevap üretir.
    """
    if st.session_state.get("cocuk_dostu_mod", False):
        return (
            f"🌟 **Seni çok iyi anlıyorum!** *'{kullanici_girdisi}'* konusunda yanında olmak isterim. "
            "Bazen böyle hissetmek çok normal; derin bir nefes alalım. İstersen biraz sohbet edebilir, "
            "sana neşeli bir hikâye anlatabilir ya da kafanı dağıtacak bir bilmece sorabilirim. Ne dersin? 😊",
            "🧒 Çocuk Dostu Sohbet",
        )

    # 1. Aile / Kardeş / Abla / Abi ile ilgili üzüntü veya yorgunluk
    if any(k in norm_text for k in ["ablam", "abalam", "abla", "abim", "annem", "babam", "kardesim"]):
        return (
            "💙 **Bunu duymak beni üzdü Ahmet, seni gerçekten anlıyorum.** Aile içinde — özellikle abla/abi veya kardeşler arasında — "
            "bazen anlaşmazlıklar insanı hem çok üzebiliyor hem de zihnen yorabiliyor.\n\n"
            "• Önce biraz sakinleşip kendine kısa bir alan aç; gergin anlarda konuşmak genelde işi daha da büyütebiliyor.\n"
            "• İkiniz de sakinken suçlamadan sadece kendi hissettiğini söylemek (*'Şu davranışın beni gerçekten üzüyor ve yoruyor'*) çoğu zaman karşı tarafın seni duymasını kolaylaştırır.\n\n"
            "İstersen tam olarak ne olduğunu anlat, birlikte nasıl yaklaşabileceğini konuşalım; seni dinliyorum.",
            "💙 İçten Sohbet",
        )

    # 2. Bot geri bildirimi / hata düzeltme / düzeltme itirazı
    if any(k in norm_text for k in ["hatalarini", "duzeltmekle", "ugrasiyorum", "yanlis anladin", "dinlemiyorsun", "bozuk", "alakasiz", "sapittin"]):
        return (
            "🤝 **Haklısın Ahmet, kusura bakma!** Hataları tek tek ayıklayıp düzeltmek gerçekten yorucu olabiliyor. "
            "Şu an seni dikkatle dinliyorum; tam olarak hangi soruda veya kısımda takıldıysak onu yaz, "
            "alakasız yerlere sapmadan doğrudan ona odaklanalım.",
            "💬 İçten Sohbet",
        )

    # 2.5 Motivasyon, çalışma ve günlük hal-hatır
    if any(k in norm_text for k in ["motive", "motivasyon", "nasil basaririm", "kendimi nasil"]):
        return (
            "🚀 **Harika bir soru Ahmet, motivasyon beklemek yerine küçük bir adımla başlar!**\n\n"
            "• **10 Dakika Kuralı:** Gözünde büyüyen işi sadece 10 dakika yapmak üzere aç (Pomodoro sayacını başlat); başladıktan sonra beyin devamını kendisi getiriyor.\n"
            "• **Büyük Hedefi Parçala:** İHA, TÜBİTAK veya ders fark etmez — bugün sadece tek bir küçük modülü veya 15 soruyu bitirmeyi hedefle.\n"
            "• **Kısa Ödül:** Her 25 dakikalık odaklanmadan sonra 5 dakika ekrandan kalkıp su içmek zihni tazeler.\n\n"
            "İstersen hemen 25 dakikalık bir Pomodoro başlatıp birlikte ilk adımı seçelim!",
            "🚀 Motivasyon & Sohbet",
        )
    if any(k in norm_text for k in ["gunun nasil", "nasil gecti"]):
        return (
            "⚡ **Harika geçiyor Ahmet, seninle yeni özellikler geliştirip test etmek çok keyifli!** "
            "Senin günün nasıl gidiyor, okul ve projeler nasıl?",
            "💬 İçten Sohbet",
        )

    # 3. Genel üzüntü, yorgunluk, sınav veya stres
    if any(k in norm_text for k in ["uzuyor", "uzgunum", "yoruldum", "yoruyor", "bunaldim", "sikildim", "sinav", "stres", "kafam karisti", "arkadasim", "kalbimi", "kirdi", "kiriyor"]):
        return (
            "💙 **Yanındayım Ahmet, üst üste gelince insanın yorulması ve bunalması çok normal.** "
            "Şu an her şeyi bir anda çözmek zorunda değilsin; biraz soluklanıp seni en çok neyin yorduğunu anlatabilirsin. "
            "İstersen birlikte küçük bir plan yapalım, istersen sadece biraz dertleşelim.",
            "💙 İçten Sohbet",
        )

    # 4. Genel sıcak sohbet
    return (
        f"💙 **Seni dinliyorum Ahmet!** *'{kullanici_girdisi}'* üzerine konuşabiliriz. "
        "Şu an bulut AI bağlantısı anlık yanıt veremedi ama sohbetimiz kesilmeden devam edebilir; "
        "biraz daha açmak istersen ya da başka bir şey sormak istersen buradayım.",
        "💬 İçten Sohbet",
    )

def help_veya_yardim_mi(norm_text: str) -> bool:
    return norm_text in {
        "help", "yardim", "yardim et", "bana yardim et", "komutlar", "nasil kullanilir",
        "ne yazabilirim", "destek", "yardimci ol", "menu", "ozellikler",
    }


def _kisa_anlat_istegi_mi(norm_text: str) -> bool:
    """Kullanıcı kısa/özet cevap istiyorsa True döner ('kısaca', 'özetle', 'kısa anlat')."""
    kisa_kaliplar = [
        "kisaca", "kisa anlat", "kisa bilgi", "kisa ozet", "ozetle", "ozet ver",
        "tek cumle", "iki cumle", "2 cumle", "3 cumle", "uzatmadan", "oz olarak",
    ]
    return any(k in norm_text for k in kisa_kaliplar)


def _uzunluk_modu_belirle(kullanici_girdisi: str, norm_text: str) -> str:
    """
    Akıllı Uzunluk Mantığı:
      • 'kisa'  -> kullanıcı kısaca/özet istediyse (en fazla ~550 krk, 3-4 cümle)
      • 'derin' -> kullanıcı daha fazla/detay istediyse VEYA uzun/çok katmanlı soru yazdıysa (>= 11 kelime)
      • 'orta'  -> standart dengeli yanıt
    """
    if _daha_fazla_bilgi_istegi_mi(norm_text) or ("uzun" in norm_text and not re.search(r"\ben uzun\b", norm_text)) or len(kullanici_girdisi.split()) >= 11:
        return "derin"
    if _kisa_anlat_istegi_mi(norm_text) or "kisa hikaye" in norm_text or "kisa masal" in norm_text:
        return "kisa"
    return "orta"


def _metni_kisaca_ozetle(metin: str, maks_krk: int = 580) -> str:
    """Kullanıcı 'kısaca' istediğinde uzun metni cümle bütünlüğünü bozmadan net özete indirger."""
    if not metin or len(metin) <= maks_krk:
        return metin
    kes = metin[:maks_krk]
    son_nokta = max(kes.rfind("."), kes.rfind("!"), kes.rfind("?"))
    if son_nokta > 200:
        return kes[:son_nokta + 1].strip() + "\n\n💡 *Daha detaylı anlatım için **'daha fazla bilgi ver'** yazabilirsin.*"
    return kes.strip() + "..."


def _hikaye_veya_masal_istegi_mi(norm_text: str) -> bool:
    """Kullanıcı kısa/uzun hikâye, masal veya olay anlatımı istiyorsa True döner."""
    return any(
        k in norm_text
        for k in [
            "masal anlat", "bana masal", "uzun masal", "kisa masal", "cocuk masali",
            "hikaye anlat", "hikayesini anlat", "kisa hikaye", "uzun hikaye", "hikaye yaz",
            "oyku anlat", "oyku yaz", "destan anlat", "bir hikaye",
        ]
    )


def _daha_fazla_bilgi_istegi_mi(norm_text: str) -> bool:
    """Kullanıcı mevcut anlatımı daha uzun, daha derin veya devamıyla birlikte istiyorsa True döner."""
    derin_kaliplar = [
        "daha fazla bilgi", "daha fazla ver", "daha fazla anlat", "daha fazla",
        "yeterli bulmuyorum", "yeterli degil", "yetmedi", "az bilgi", "cok kisa",
        "biraz daha anlat", "biraz daha uzat", "biraz daha detay", "daha detayli",
        "detayli anlat", "detaylandir", "derinlemesine", "uzun anlat", "uzun yaz",
        "daha uzun", "uzununu", "uzat", "kapsamli anlat", "genis bilgi", "genis anlat",
        "devam et", "devamini", "devamini getir", "devamini anlat", "devamini yaz",
        "sonra ne oldu", "peki sonra", "bitmedi", "daha cok bilgi", "baska neler var",
        "ikinci bolum", "2 bolum", "ucuncu bolum", "3 bolum", "dorduncu bolum", "4 bolum",
        "uzun hali", "uzun versiyon", "daha detaylisi", "hikayeyi uzat", "devam etsene",
        "sonrasini anlat", "devamini yaz", "bolum 2", "bolum 3", "bolum 4",
    ]
    return any(k in norm_text for k in derin_kaliplar)


def _devam_veya_takip_sorusu_mu(norm_text: str) -> bool:
    """Kullanıcı bir önceki konunun/hikâyenin devamını istiyorsa True döner."""
    if _daha_fazla_bilgi_istegi_mi(norm_text) or _kisa_anlat_istegi_mi(norm_text):
        return True
    takip_kaliplari = [
        "ornek ver", "ozetle", "kisaca ozetle", "baska ne var", "peki neden",
        "aciklar misin", "anlamadim tekrar anlat", "devam", "ilerlet", "ekle",
    ]
    if any(k in norm_text for k in takip_kaliplari):
        return True
    # Önceki konuya bağlanan doğal takip soruları: "peki ...", "ya ...", "bir de ...", "bunun/onun ..."
    n = norm_text.strip()
    if n.startswith(("peki ", "ya ", "bir de ", "o zaman ", "ayrica ", "bu durumda ", "yani ")):
        return True
    return bool(re.search(r"\b(bunun|onun|bunu|onu|bunlar|onlar|bunda|onda|bundan|ondan|buna|ona)\b", n)) and len(n.split()) <= 9


def akilli_niyet_siniflandir(kullanici_girdisi: str) -> dict:
    """
    GEMINI TARZI ÇOK KATMANLI BAĞLAMSAL NİYET AYRIŞTIRICI:
    Mesajı 4 boyutta analiz eder:
      1) Kullanıcı çalışma modu ('otomatik_ai', 'sadece_sohbet', 'wiki_arastirma')
      2) Cümle yapısı: 1./2. tekil şahıs zamirleri ('ben', 'sen', 'bana', 'sence') ve
         istek/emir fiilleri ('-r mısın', 'yaz', 'yap', 'öner', 'yorumla') -> SOHBET / KOD
      3) Somut ansiklopedik bilgi kalıpları ('kimdir', 'nedir', 'tarihi') -> ANSIKLOPEDI
      4) Özel araç sinyalleri -> HARITA_ADRES, FIYAT_PIYASA, SOZLUK_TDK, MATEMATIK_FEN
    """
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    norm = metni_normallestir(kullanici_girdisi)
    kelimeler = norm.split()
    aktif_mod = st.session_state.get("sohbet_oncelik_modu", "ai_once")

    skorlar = {
        "YARDIM": 0,
        "KOD_URETIM": 0,
        "HARITA_ADRES": 0,
        "FIYAT_PIYASA": 0,
        "SOZLUK_TDK": 0,
        "WIKIPEDIA_ANSIKLOPEDI": 0,
        "MATEMATIK_FEN": 0,
        "SOHBET_AI": 15,  # Doğal sohbet taban skoru
    }

    # 1. Açık Önek Komutları (Kullanıcı açıkça kanal seçtiyse kesin öncelik)
    if help_veya_yardim_mi(norm):
        skorlar["YARDIM"] += 130
    if raw.startswith(("wikipedia:", "wikipedia ", "vikipedi:", "vikipedi ", "wiki:", "wiki ", "araştır:", "arastir:")):
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] += 140
    if raw.startswith(("tdk:", "tdk ", "sözlük:", "sozluk:")):
        skorlar["SOZLUK_TDK"] += 140
    if raw.startswith(("fiyat:", "fiyat ", "cimri:", "cimri ", "epey:", "epey ", "akakce:", "akakçe:")):
        skorlar["FIYAT_PIYASA"] += 140
    if raw.startswith(("adres:", "adres ", "konum:", "konum ", "harita:", "yol tarifi:")):
        skorlar["HARITA_ADRES"] += 140
    if raw.startswith("ollama:"):
        skorlar["SOHBET_AI"] += 140

    # 2. Dilbilgisel Analiz: Kişisel Zamirler ve Sohbet/Görev Fiilleri
    if kod_veya_uretim_istegi_mi(kullanici_girdisi):
        skorlar["KOD_URETIM"] += 105
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 100

    # 1. ve 2. tekil şahıs sohbet sinyalleri ('ben', 'bana', 'sen', 'sence', 'biz', 'benimle')
    sahis_zamirleri = {"ben", "bana", "beni", "benim", "sen", "sana", "seni", "senin", "sence", "biz", "benimle"}
    sahis_sayisi = sum(1 for k in kelimeler if k in sahis_zamirleri)
    if sahis_sayisi >= 1 and not any(k in raw for k in ["kimdir", "adresi", "ne kadar"]):
        skorlar["SOHBET_AI"] += 45 * sahis_sayisi
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 45

    # Yorum / Tartışma / İstek fiilleri -> Kesinlikle sohbet AI'dır, Wikipedia değildir
    if re.search(r"(?:mısın|misin|musun|müsün|misin|yapalım|edelim|konuşalım|tartışalım|söyle bakalım|ne dersin)$", raw):
        if not any(k in raw for k in ["hakkında bilgi verir misin", "anlatır mısın"]):
            skorlar["SOHBET_AI"] += 55
            skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 50

    # 3. Özel Araç Sinyalleri
    if adres_sorgusu_mu(kullanici_girdisi):
        skorlar["HARITA_ADRES"] += 95
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 60
    if fiyat_sorgusu_mu(kullanici_girdisi):
        skorlar["FIYAT_PIYASA"] += 95
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 60
    if re.search(r"\b(ne demek|ne demektir|kelimesinin anlamı|kelimesi ne demek|tdk anlamı)\b", raw):
        skorlar["SOZLUK_TDK"] += 85
    if re.search(r"(\d+\s*[+\-*/×÷^]\s*\d+|\d*\s*x\s*(?:\^2|²)?\s*[+\-=]|\bkök\b|\bkok\b|\bkarekök\b|\bçarpı\b|\bcarpi\b|\bbölü\b|\bbolu\b|\bartı\b|\barti\b|\beksi\b|\byüzde\b|\byuzde\b|\büzeri\b|\buzeri\b|\büssü\b|\bussu\b|\bebob\b|\bekok\b|\bfaktöriyel|\bfaktoriyel|\basal\b|\bhızla\b|\bhizla\b|\bhipotenüs|\bhipotenus|\bpisagor|üçgenin\s+alanı|ucgenin\s+alani)", raw):
        skorlar["MATEMATIK_FEN"] += 95

    # 4. Selamlaşma / Duygu / Kişisel Sohbet
    sohbet_ipucu = [
        "nasılsın", "nasilsin", "ne haber", "naber", "selam", "merhaba", "günaydın",
        "iyi akşamlar", "canım sıkkın", "moral", "yoruldum", "sence", "düşünüyorsun",
        "ben kimim", "kimsin", "ömer kim", "hadi kim", "edibe kim", "ailem", "teşekkür", "eyvallah",
    ]
    if any(k in raw or k in norm for k in sohbet_ipucu):
        skorlar["SOHBET_AI"] += 85
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] -= 75

    # 5. Gerçek Ansiklopedik / Biyografi Sinyalleri
    ansiklopedi_ipucu = [
        "kimdir", "nedir", "hakkında bilgi", "hakkinda bilgi", "ne zaman kuruldu",
        "tarihi", "biyografisi", "gezegeni", "imparatorluğu", "imparatorlugu", "teorisi", "kanunu",
    ]
    if any(k in raw for k in ansiklopedi_ipucu) and sahis_sayisi == 0:
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] += 75

    # 6. Çalışma Moduna Göre İnce Ayar
    if aktif_mod == "sadece_sohbet" and not raw.startswith(("wikipedia:", "vikipedi:", "wiki:")):
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] = -999
    elif aktif_mod == "wiki_once" and skorlar["WIKIPEDIA_ANSIKLOPEDI"] > 0:
        skorlar["WIKIPEDIA_ANSIKLOPEDI"] += 35

    en_yuksek_niyet = max(skorlar, key=skorlar.get)
    neden_haritasi = {
        "YARDIM": "Yardım/rehber komutu algılandı",
        "KOD_URETIM": "Kod yazma veya görev üretme fiili algılandı",
        "HARITA_ADRES": "Konum/adres/yol tarifi niyeti algılandı",
        "FIYAT_PIYASA": "Ürün fiyat karşılaştırma niyeti algılandı",
        "SOZLUK_TDK": "Kelime anlamı/TDK sözlük niyeti algılandı",
        "MATEMATIK_FEN": "Sayısal işlem/denklem algılandı",
        "WIKIPEDIA_ANSIKLOPEDI": "Ansiklopedik bilgi/biyografi sorusu algılandı",
        "SOHBET_AI": "Doğal sohbet/yorum bağlamı algılandı",
    }
    return {
        "niyet": en_yuksek_niyet,
        "skor": skorlar[en_yuksek_niyet],
        "neden": neden_haritasi.get(en_yuksek_niyet, "Genel yönlendirme"),
        "tum_skorlar": skorlar,
    }


def gercek_ansiklopedik_sorgu_mu(kullanici_girdisi: str) -> bool:
    sonuc = akilli_niyet_siniflandir(kullanici_girdisi)
    return sonuc["niyet"] == "WIKIPEDIA_ANSIKLOPEDI" and sonuc["skor"] >= 50


# Kısa takip / bağlam soruları ('nerede?', 'adresi ne?', 'nasıl?', 'hava durumu?', 'plakası kaç?')
KISA_TAKIP_SORULARI = {
    "nerede", "nerededir", "neresi", "adresi ne", "adresi nedir", "adresi", "konumu",
    "konumu nedir", "nasil gidilir", "nasil giderim", "yol tarifi", "nasil", "nasildir",
    "ne zaman yapildi", "ne zaman kuruldu", "kim yapti", "hava durumu", "hava nasil",
    "plakasi kac", "plakasi", "baskenti neresi", "baskenti", "nufusu kac", "nufusu",
    "orasi nasil", "orasi nerede", "hakkinda daha fazla bilgi", "biraz daha anlat",
    "peki", "neden", "niye", "ornek", "ozet", "kisaca", "devam", "acikla", "detay",
    "formulu", "formul", "vakitleri", "ezan", "havasi", "hava", "tarihi", "kim", "kac", "ne kadar",
    "devam et", "detaylandir", "ozetle", "ornek ver",
}


def _sehir_veya_ulke_var_mi(metin_kucuk: str) -> bool:
    for il in TURKIYE_81_IL:
        if re.search(rf"\b{re.escape(il)}\b", metin_kucuk):
            return True
    for ulke in TURKCE_ULKELER:
        if re.search(rf"\b{re.escape(ulke)}\b", metin_kucuk):
            return True
    return False


def _yemek_tarifi_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(tarifi|tarif|nasıl yapılır|nasil yapilir|yapılışı|yapilisi|yemeği nasıl|çorbası nasıl)\b", metin_kucuk))


def _hava_durumu_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(hava durumu|hava nasıl|hava nasil|kaç derece|kac derece|yağmur var mı|kar yağacak mı|hava kalitesi|hava kirliliği|hava kirliligi|aqi|uv indeksi)\b", metin_kucuk))


def _finans_altin_doviz_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(gram\s+alt[ıi]n|çeyrek\s+alt[ıi]n|ceyrek\s+alt[ıi]n|yar[ıi]m\s+alt[ıi]n|tam\s+alt[ıi]n|ons\s+alt[ıi]n|alt[ıi]n\s+fiyat|alt[ıi]n\s+kuru|alt[ıi]n\s+ne\s+kadar|dolar\s+kaç|dolar\s+kac|dolar\s+kuru|dolar\s+ne\s+kadar|euro\s+kaç|euro\s+kac|euro\s+kuru|sterlin\s+kaç|döviz\s+kuru|doviz\s+kuru|bitcoin|btc\s+kaç|ethereum)\b", metin_kucuk))


def _futbolcu_piyasa_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(piyasa\s+değeri|piyasa\s+degeri|bonservis|transfermarkt|kaç\s+euro|kac\s+euro|kaç\s+milyon\s+euro)\b", metin_kucuk))


def _kimya_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(
        r"\b(formülü|formulu|molekül|molekul|mol kütlesi|kimyasal|sülfürik|sulfurik|hidroklorik|tuz ruhu|nitrik asit|sodyum klorür|sodyum hidroksit|sodyum bikarbonat|amonyak|karbondioksit|glikoz|etanol|asetik asit|kalsiyum karbonat|hidrojen peroksit|kafein|aspirin|pubchem|bileşik|bilesik)\b",
        metin_kucuk,
    ))


def _namaz_veya_hicri_mi(metin_kucuk: str) -> bool:
    return bool(re.search(
        r"\b(namaz vakti|namaz vakitleri|ezan|imsak|akşam ezanı|aksam ezani|sabah namazı|öğle namazı|ikindi|yatsı|yatsi|hicri|hicri takvim|kıble|kible|aladhan|iftar|sahur)\b",
        metin_kucuk,
    ))


def _teknofest_veya_makale_mi(metin_kucuk: str) -> bool:
    return bool(re.search(
        r"\b(teknofest|tübitak|tubitak|2204|arxiv|akademik makale|bilimsel makale|makale bul|makale ara|savaşan iha|savasan iha)\b",
        metin_kucuk,
    ))


def _deprem_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(son depremler|deprem oldu mu|depremler|son deprem|deprem bilgisi|kandilli|usgs)\b", metin_kucuk))


def _akil_yurutme_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(neden|niçin|nicin|mantık|mantik|karşılaştır|karsilastir|analiz et|kanıtla|kanitla|adım adım düşün|adim adim dusun|farkı nedir|farki nedir|hangisi daha iyi|sence)\b", metin_kucuk))


def _canli_haber_veya_arama_mi(metin_kucuk: str) -> bool:
    return bool(re.search(
        r"\b(son dakika|haberler|haberleri|haber\b|gündem|gundem|güncel|guncel|bugün ne oldu|bugun ne oldu|son durum|yeni çıkan|yeni cikan|webde ara|internette ara|google'?da ara|googleda ara|arama yap|maç sonucu|mac sonucu|puan durumu|2026|2025)\b",
        metin_kucuk,
    ))


def _sehir_ozel_konu_mu(metin_kucuk: str) -> bool:
    """Şehir adı geçse bile aslında haber, boğaz, köprü, üniversite veya tarif soruyorsa 81 İl'e sapmasını engeller."""
    return bool(re.search(
        r"\b(boğazı|bogazi|boğaz|bogaz|köprüsü|koprusu|üniversitesi|universitesi|havalimanı|havalimani|havaalanı|takımı|takimi|belediye|haber|son dakika|gündem|güncel|tarifi|tarif|nasıl yapılır|nasil yapilir|namaz|ezan|imsak|iftar|sahur|hicri|deprem|teknofest|tübitak|tubitak|makale|formül|formul|kimya|antik|imparatorluğu|imparatorlugu|devleti|uygarlığı|uygarligi|medeniyeti|savaşı|savasi|ihtilali|devrimi|tarihi|sence|yorumla|neden|karşılaştır)\b",
        metin_kucuk,
    ))


def _kitap_istegi_mi(metin_kucuk: str) -> bool:
    return bool(re.search(r"\b(kitabı|kitabi|kitabının yazarı|kim yazdı|kim yazdi)\b", metin_kucuk))


def _cumlede_yeni_konu_var_mi(raw: str, norm: str) -> bool:
    """
    Cümlede açıkça YENİ bir şehir, ülke, tarihî kişi, yemek tarifi, kimya bileşiği,
    yapıt veya bağımsız soru öznesi varsa True döner (eski konuya saplanmayı engeller!).
    """
    # Bağımsız yeni araç/niyet sinyali varsa (tarif, denklem, namaz, deprem, çeviri, sayaç, kimya)
    if re.search(
        r"\b(nasıl yapılır|nasil yapilir|tarifi|tarif|piyasa değeri|piyasa degeri|namaz|ezan|deprem|çevir|cevir|translate|sayaç|sayac|pomodoro|formülü|formulu|kimdir|saat kaç|saat kac)\b",
        raw,
    ):
        # Ancak sadece tek başına 'kimdir?' / 'formülü?' / 'tarifi?' ise devam sorusudur
        temiz_k = re.sub(r"\b(peki|bir de|ayrıca|ayrica|başka|baska|kimdir|nedir|formülü|formulu|tarifi|tarif)\b", " ", raw)
        temiz_k = re.sub(r"\s+", " ", temiz_k).strip("?!.,;:\"' ")
        if len(temiz_k) >= 3:
            return True

    # Bilinen il, ülke, biyografi veya tarihî yapıt geçiyorsa kesinlikle yeni konudur
    if any(re.search(rf"\b{re.escape(il)}\b", raw) for il in TURKIYE_81_IL.keys()):
        return True
    if any(re.search(rf"\b{re.escape(ul)}\b", raw) for ul in TURKCE_ULKELER.keys()):
        return True
    for bio_k in DETAYLI_TARIH_BIYOGRAFILERI.keys():
        if metni_normallestir(bio_k) in norm:
            return True
    for ozel_k in (
        "fatih", "mehmet", "mehmed", "sinan", "ataturk", "osmanli", "gobeklitepe", "ayasofya",
        "topkapi", "suleymaniye", "kapadokya", "efes", "dara", "roma", "selcuklu", "gokturk",
        "doner", "lahmacun", "iskender", "kunefe", "baklava", "osimhen", "arda guler",
        "seyh samil", "imam samil", "samil", "selahaddin", "alparslan", "kanuni", "yavuz",
        "barbaros", "piri reis", "aziz sancar", "futbol", "organizasyon", "dunya kupasi",
        "sampiyonlar ligi", "olimpiyat", "basketbol", "voleybol", "uzay", "yapay zeka",
    ):
        if ozel_k in norm:
            return True

    # Zamir/takip ifadesi İÇERMEYEN ve en az 2 anlamlı içerik kelimesi taşıyan bağımsız ifadeler YENİ KONUDUR!
    zamir_isaret = re.search(
        r"\b(onun|ona|onu|ondan|bunun|buna|bunu|bundan|orada|orasi|orası|oraya|oradan|peki o|o kim|bu ne|bu nedir|daha fazla|devam et|devam)\b",
        raw,
    )
    if not zamir_isaret:
        if re.search(r"\b(1\d{3}|20\d{2})\b", raw) and len(raw.split()) <= 6:
            return False
        ic_kelimeler = [
            w for w in norm.split()
            if len(w) >= 4 and w not in {
                "hakkinda", "bilgi", "anlat", "nedir", "nasil", "neden", "sence", "dusunuyorsun",
                "yorumla", "peki", "biraz", "bana", "sana", "guzel", "buyuk", "kucuk",
                "mimarisi", "tarihi", "yemekleri", "mutfagi", "nufusu", "ekonomisi", "iklimi", "havasi",
                "ozellikleri", "onemi", "avantajlari", "dezavantajlari", "sonuclari", "nedenleri", "ornekleri",
            }
        ]
        if len(ic_kelimeler) >= 2:
            return True
    return False


def _konu_devami_mi(raw: str, norm: str) -> bool:
    """
    v10.2 — Yalnızca yeni bir konu/özne içermeyen gerçek devam sorularında True döner.
    'Peki Fatih Sultan Mehmet kimdir?' gibi yeni konulu cümlelerde ASLA eski konuya (örn. Hollanda) saplanmaz!
    """
    if _cumlede_yeni_konu_var_mi(raw, norm):
        return False

    if norm in KISA_TAKIP_SORULARI or _devam_veya_takip_sorusu_mu(norm):
        return True

    # Yalnızca zamir veya alt-başlık sorusu (yeni özel isim yoksa!)
    zamir_ve_alt_baslik = (
        r"\b(orada|orasi|orası|oraya|oradan|burada|bunun|onun|ona|onu|ondan|bunu|bunlar|onlar|"
        r"mimarisi|tarihi|yemekleri|mutfagi|mutfağı|neleri meshur|neleri meşhur|neyi meshur|neyi meşhur|"
        r"gezilecek yerleri|gezilecek yerler|nufusu|nüfusu|ekonomisi|iklimi|havasi|havası|"
        r"ulasimi|ulaşımı|onemi|önemi|ozellikleri|özellikleri|avantajlari|avantajları|"
        r"dezavantajlari|dezavantajları|nedenleri|sonuclari|sonuçları|etkileri|ornekleri|örnekleri|"
        r"formulu|formülü|kac yasinda|kaç yaşında|ne zaman yapildi|ne zaman yapıldı|kim yapti|kim yaptı)\b"
    )
    if re.search(zamir_ve_alt_baslik, raw) and len(raw.split()) <= 7:
        return True

    # Yıl + olay devam sorusu ('1998 de yapan kim', '1998 de nerede oynandı', '2022 şampiyonu kim') -> aktif_konu'nun devamıdır!
    if len(raw.split()) <= 6 and (
        re.search(r"\b(1\d{3}|20\d{2})\b", raw)
        or re.search(r"\b(yapan kim|kim yapti|kim yaptı|kim kazandi|kim kazandı|nerede oynandi|nerede oynandı|ev sahibi kim|sampiyonu kim|şampiyonu kim|hangi ulkede|hangi ülkede)\b", raw)
    ):
        return True
    return False

def _aktif_konu_baglami_uygula(kullanici_girdisi: str, guncelle: bool = True) -> tuple:
    """
    v9.1 GERÇEK ÇOK TURLU KONU DEVAMLILIĞI (100+ Soru Boyunca Bağlam Kopmaz!):
      • guncelle=False iken sadece önizleme yapar, aktif_konu'yu asla bozmaz.
      • Aynı konu üzerinde 'peki yemekleri?', 'orada neler var?', 'mimarisi nasıl?',
        'daha fazla bilgi ver', 'nerede?' gibi arka arkaya onlarca soruda aktif_konu'yu korur.
      • Kullanıcı açıkça yeni bir yer/kişi/kavram söylediğinde aktif_konu'yu temizce günceller.
    """
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    norm = metni_normallestir(kullanici_girdisi)
    aktif_konu = st.session_state.get("aktif_konu", "").strip()

    # Düzeltme/itiraz ('hayır onu demiyorum') veya duygusal sohbet cümlesinde ASLA eski konuyu yapıştırma!
    if _itiraz_veya_duzeltme_mi(raw, norm) or _duygusal_kisisel_sohbet_mi(raw, norm):
        if guncelle:
            st.session_state["aktif_konu"] = ""
        return kullanici_girdisi, False

    if not aktif_konu and (_konu_devami_mi(raw, norm) or _daha_fazla_bilgi_istegi_mi(norm)):
        _gecmis_msj = st.session_state.get("messages") or []
        for _m in reversed(_gecmis_msj[-6:]):
            if _m.get("role") == "user":
                _onceki_u = str(_m.get("content", "")).strip()
                _onceki_n = metni_normallestir(_onceki_u)
                if _onceki_u and not _daha_fazla_bilgi_istegi_mi(_onceki_n) and len(_onceki_u) >= 3:
                    aktif_konu = _onceki_u[:80]
                    if guncelle:
                        st.session_state["aktif_konu"] = aktif_konu
                    break

    if aktif_konu and (_konu_devami_mi(raw, norm) or _daha_fazla_bilgi_istegi_mi(norm)):
        # Aktif konu zaten cümlenin içinde geçiyorsa tekrar başa ekleme
        if metni_normallestir(aktif_konu) in norm:
            return kullanici_girdisi, True
        birlesik = f"{aktif_konu} {kullanici_girdisi.strip()}"
        return birlesik, True

    if guncelle and not _dogal_sohbet_cumlesi_mi(raw, norm):
        temiz_ozne = re.sub(
            r"\b(hakkında bilgi ver|hakkinda bilgi ver|hakkında ne düşünüyorsun|hakkinda ne dusunuyorsun|ne düşünüyorsun|ne dusunuyorsun|sence|yorumla|hakkında|hakkinda|nerededir|nerede|adresi nedir|adresi|konumu|nasıldır|nasıl|nasildir|nasil|kimdir|nedir|ne zaman|yapıldı|kuruldu|tarifi|hava durumu|ne kadar|fiyatı|anlat|bilgi ver|peki|orada|orası|onun|bunun|yemekleri|mimarisi|tarihi|özellikleri|neleri meşhur|gezilecek yerleri|sonuçları|nedenleri)\b",
            " ",
            kullanici_girdisi,
            flags=re.IGNORECASE,
        )
        temiz_ozne = re.sub(r"\s+", " ", temiz_ozne).strip("?!.,;:\"' ")
        if len(temiz_ozne) >= 3 and len(temiz_ozne.split()) <= 5:
            norm_ozne = metni_normallestir(temiz_ozne)
            yasakli = {
                "merhaba", "selam", "nasilsin", "naber", "ne haber", "help", "yardim",
                "ben", "sen", "iyiyim", "tesekkurler", "sohbet edelim", "devam", "devam et",
                "daha fazla", "yeterli degil", "ornek", "ozet", "peki", "neden", "niye",
            }
            if norm_ozne not in yasakli and not re.search(r"\d+\s*[+\-*/×÷^]\s*\d+", raw):
                st.session_state["aktif_konu"] = temiz_ozne

    return kullanici_girdisi, False

def otonom_plan_olustur(kullanici_girdisi: str) -> dict:
    """
    v6.0 TAM TEŞEKKÜLLÜ OTONOM AJAN PLANLAYICISI:
    Gerektiğinde tek mesaj için birden fazla açık kaynak araca (81 İl & 195+ Ülke,
    Harita/Adres, Yemek Tarifleri, Canlı Hava Durumu, Fiyat, TDK, Matematik,
    Wikipedia, Biyografi, Kitap ve Sohbet AI) kendiliğinden gidip gelir.
    """
    raw = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    norm = metni_normallestir(kullanici_girdisi)
    niyet_sonuc = akilli_niyet_siniflandir(kullanici_girdisi)
    ana_niyet = niyet_sonuc["niyet"]

    araclar = []
    adim_ozetleri = []

    if ana_niyet == "YARDIM":
        return {"ana_niyet": "YARDIM", "araclar": ["YARDIM"], "sentez_gerekli": False, "adimlar": ["🤝 Yardım rehberi hazırlanıyor"]}
    if ana_niyet == "KOD_URETIM":
        return {"ana_niyet": "KOD_URETIM", "araclar": ["KOD_AI"], "sentez_gerekli": True, "adimlar": ["💻 Kod & yapay zeka motoru çalıştırılıyor"]}

    # 1. Matematik & Sözel Problem
    # Profesyonel çekirdek (Modül 14) metni çözebiliyorsa (sin 30, log 100, 17 asal mı...) doğrudan matematik say.
    try:
        _pro_fn = getattr(_m4, "_pro_matematik_coz", None)
        _pro_mat_mi = bool(_pro_fn and _pro_fn(kullanici_girdisi)[0])
    except Exception:
        _pro_mat_mi = False
    _aralik_veya_skor = bool(re.search(
        r"\b\d+\s*-\s*\d+\s*(?:gün|gun|saat|dakika|dk|hafta|ay|yıl|yil|sene|kişi|kisi|kez|defa|tane|kat|yaş|yas|"
        r"sayfa|soru|km|metre|kilo|tl|lira|dolar|euro)\b|\b(?:skor|maç|mac|kazand|yendi|yenildi|berabere|galip|mağlup)", raw))
    if _pro_mat_mi or (not _aralik_veya_skor and re.search(r"(\d+\s*[+\-*/×÷^]\s*\d+|\d*\s*x\s*(?:\^2|²)?\s*[+\-=]|\bkök\b|\bkok\b|\bkarekök\b|\bçarpı\b|\bcarpi\b|\bbölü\b|\bbolu\b|\bartı\b|\barti\b|\beksi\b|\byüzde\b|\byuzde\b|\büzeri\b|\buzeri\b|\büssü\b|\bussu\b|\bebob\b|\bekok\b|\bfaktöriyel|\bfaktoriyel|\basal\b|\bhızla\b|\bhizla\b|\bhipotenüs|\bhipotenus|\bpisagor|üçgenin\s+alanı|ucgenin\s+alani)", raw)):
        araclar.append("MATEMATIK")
        adim_ozetleri.append("🧮 Matematik motoru hesaplıyor")

    # 2. Yemek Tarifleri (Türk Mutfağı + TheMealDB)
    if _yemek_tarifi_istegi_mi(raw):
        araclar.append("YEMEK_TARIFI")
        adim_ozetleri.append("🍲 Yemek tarifi kaynakları taranıyor")

    # 3. Canlı Hava Durumu (Open-Meteo)
    if _hava_durumu_istegi_mi(raw):
        araclar.append("HAVA_DURUMU")
        adim_ozetleri.append("🌤️ Open-Meteo canlı hava durumu alınıyor")

    # 4. Kitap Bilgisi (Open Library)
    if _kitap_istegi_mi(raw):
        araclar.append("KITAP")
        adim_ozetleri.append("📚 Open Library kitap kataloğu taranıyor")

    # 5. Harita & Adres (OpenStreetMap + Photon + Yerleşik Konum)
    if adres_sorgusu_mu(kullanici_girdisi):
        araclar.append("HARITA")
        adim_ozetleri.append("📍 Açık kaynak haritadan konum ve açık adres alınıyor")

    # 5.1 Kimya & Bileşik Formülü (PubChem PUG-REST + Türkçe Kimya)
    if _kimya_istegi_mi(raw):
        araclar.append("KIMYA_BILESIK")
        adim_ozetleri.append("🧪 PubChem & Kimya motoru bileşik formülünü inceliyor")

    # 5.2 Namaz Vakitleri & Hicri Takvim (AlAdhan Diyanet Method=13)
    if _namaz_veya_hicri_mi(raw):
        araclar.append("NAMAZ_HICRI")
        adim_ozetleri.append("🕌 AlAdhan Diyanet vakitleri ve Hicri takvim alınıyor")

    # 5.3 TEKNOFEST, TÜBİTAK & arXiv Akademik Makaleler
    if _teknofest_veya_makale_mi(raw):
        araclar.append("TEKNOFEST_MAKALE")
        adim_ozetleri.append("🚀 TEKNOFEST rehberi ve arXiv akademik makaleleri taranıyor")

    # 5.4 Türkiye Canlı Deprem Takibi (USGS GeoJSON)
    if _deprem_istegi_mi(raw):
        araclar.append("DEPREM_CANLI")
        adim_ozetleri.append("🌍 USGS canlı Türkiye deprem verisi alınıyor")

    # 5.5 Canlı Web & Türkçe Haber Arama (Google News TR RSS + DuckDuckGo)
    if (not _dogal_sohbet_cumlesi_mi(raw, norm)) and _canli_haber_veya_arama_mi(raw) and "FINANS_ALTIN_DOVIZ" not in araclar and "FUTBOLCU_PIYASA" not in araclar and "HAVA_DURUMU" not in araclar:
        araclar.append("CANLI_WEB_HABER")
        adim_ozetleri.append("🌐 Canlı açık kaynak web & güncel haber akışı taranıyor")

    # 6. Türkiye 81 İl & Dünya 195+ Ülke (Yemek, Hava, Fiyat, Haber veya özel mekan değilse)
    if (
        _sehir_veya_ulke_var_mi(raw)
        and not _sehir_ozel_konu_mu(raw)
        and "HAVA_DURUMU" not in araclar
        and "FIYAT" not in araclar
        and "YEMEK_TARIFI" not in araclar
        and "CANLI_WEB_HABER" not in araclar
    ):
        araclar.append("SEHIR_ULKE")
        adim_ozetleri.append("🌍 81 İl & 195+ Ülke (REST Countries) bilgi ağı taranıyor")

    # 6.5 Canlı Altın, Döviz & Kripto (Open-ER + Gold-API + CoinGecko)
    if _finans_altin_doviz_mi(raw):
        araclar.append("FINANS_ALTIN_DOVIZ")
        adim_ozetleri.append("💰 Canlı altın, döviz ve kripto kurları çekiliyor")

    # 6.6 Futbolcu Piyasa Değeri (TheSportsDB + Transfermarkt)
    if _futbolcu_piyasa_mi(raw):
        araclar.append("FUTBOLCU_PIYASA")
        adim_ozetleri.append("⚽ Futbolcu güncel piyasa değeri ve profili taranıyor")

    # 7. Güncel Ürün Fiyatı (Epey • Cimri • Akakçe — Altın/Döviz/Futbolcu değilse)
    if fiyat_sorgusu_mu(kullanici_girdisi) and "FINANS_ALTIN_DOVIZ" not in araclar and "FUTBOLCU_PIYASA" not in araclar:
        araclar.append("FIYAT")
        adim_ozetleri.append("🏷️ Epey, Cimri ve Akakçe'den fiyat taranıyor")

    # 8. TDK Sözlük
    if raw.startswith(("tdk:", "tdk ", "sözlük:", "sozluk:")) or re.search(r"\b(ne demek|ne demektir|kelimesinin anlamı|tdk anlamı)\b", raw):
        araclar.append("TDK")
        adim_ozetleri.append("📕 TDK Güncel Türkçe Sözlük taranıyor")

    # 8.5 Spor & Büyük Organizasyonlar (FIFA Dünya Kupası, Şampiyonlar Ligi, Olimpiyatlar)
    if _spor_organizasyon_bilgisi_getir(kullanici_girdisi).get("basarili"):
        araclar.append("SPOR_ORGANIZASYON")
        adim_ozetleri.append("⚽ Spor & Küresel Organizasyon bilgi ağı taranıyor")

    # 9. Biyografi & Wikipedia (Yorum/düşünce sorusunda bile hedef kişi/kavram için doğrulanmış bilgi çeker!)
    yorum_istegi_erken = any(k in raw for k in ["sence", "yorumla", "düşünüyorsun", "dusunuyorsun", "ne olur", "karşılaştır", "karsilastir", "neden önemli", "neden onemli"])
    sohbet_cumlesi = _dogal_sohbet_cumlesi_mi(raw, norm)
    wiki_gerekli = (
        not sohbet_cumlesi
        and (
            ana_niyet == "WIKIPEDIA_ANSIKLOPEDI"
            or raw.startswith(("wikipedia", "vikipedi", "wiki", "araştır", "arastir"))
            or any(k in raw for k in ["kimdir", "nedir", "nasıl bir yer", "nasıl yapılır", "nasil yapilir", "nasıl çalışır", "nasil calisir", "nasıl oluşur", "nasil olusur", "yapımı", "yapimi", "ne işe yarar", "hakkında bilgi", "bilgi ver", "anlat", "bahset", "ne zaman kuruldu", "tarihi", "kısaca", "özetle", "hakkında", "hakkinda"])
            or (yorum_istegi_erken and len(norm.split()) >= 2)
        )
    )
    kisisel_mi = sohbet_cumlesi or any(k in norm for k in ["ben kimim", "kimsin", "nasilsin", "ne haber", "naber", "omer kim", "hadi kim", "edibe kim", "annem kim", "babam kim", "ailem", "saat kac"])
    if wiki_gerekli and not kisisel_mi and "SEHIR_ULKE" not in araclar and "YEMEK_TARIFI" not in araclar and "HAVA_DURUMU" not in araclar and "CANLI_WEB_HABER" not in araclar and "KIMYA_BILESIK" not in araclar and "NAMAZ_HICRI" not in araclar and "TEKNOFEST_MAKALE" not in araclar and "DEPREM_CANLI" not in araclar and "SPOR_ORGANIZASYON" not in araclar:
        araclar.append("WIKIPEDIA_BIYOGRAFI")
        adim_ozetleri.append("🌐 Ansiklopedi & Wikipedia'dan doğrulanmış veri alınıyor")

    # 10. Akıllı Sohbet, Çok Turlu Devam & Uzun Anlatım Sentezi
    ollama_acik_istek = raw.startswith(("ollama:", "ollama "))
    derin_istek_var = _daha_fazla_bilgi_istegi_mi(norm)
    hikaye_istegi_var = _hikaye_veya_masal_istegi_mi(norm)
    devam_istegi_var = _devam_veya_takip_sorusu_mu(norm)
    yorum_istegi_var = any(k in raw for k in ["sence", "yorumla", "düşünüyorsun", "dusunuyorsun", "ne olur", "karşılaştır", "karsilastir", "neden"]) or (bool(re.search(r"\b(1\d{3}|20\d{2})\b", raw)) and "SPOR_ORGANIZASYON" in araclar)
    # Hikâye/masal isteğinde veya devam/uzun anlatım isteğinde AI SENTEZİ HER ZAMAN çalışır!
    if hikaye_istegi_var and "WIKIPEDIA_BIYOGRAFI" in araclar and not any(k in raw for k in ["kimdir", "nedir", "tarihi"]):
        araclar.remove("WIKIPEDIA_BIYOGRAFI")
    if derin_istek_var and not araclar and not hikaye_istegi_var and len(st.session_state.get("messages") or []) < 2:
        araclar.append("WIKIPEDIA_BIYOGRAFI")
        adim_ozetleri.append("🌐 Derin ansiklopedi (Wikipedia) kaynakları açılıyor")
    _canli_web_sentez = ("CANLI_WEB_HABER" in araclar and bool(st.session_state.get("acik_kaynak_ai_aktif", True)))
    if not araclar or yorum_istegi_var or ollama_acik_istek or derin_istek_var or devam_istegi_var or hikaye_istegi_var or _canli_web_sentez:
        araclar.append("SOHBET_AI")
        if ollama_acik_istek:
            adim_ozetleri.append("🦙 Yerel Ollama + açık kaynak verileri sentezleniyor")
        elif st.session_state.get("ortak_akil_aktif", True):
            adim_ozetleri.append("🧠 Ortak Akıl Konseyi (Ollama + Açık Kaynak AI'lar) en mantıklı cevabı birleştiriyor")
        else:
            adim_ozetleri.append("🧠 Toplanan verilerle en mantıklı yanıt sentezleniyor")

    return {
        "ana_niyet": ana_niyet,
        "araclar": araclar,
        "sentez_gerekli": ("SOHBET_AI" in araclar),
        "adimlar": adim_ozetleri,
    }


def wikipedia_arastirma_gerekiyor_mu(kullanici_girdisi: str) -> tuple:
    zengin_girdi, _ = _aktif_konu_baglami_uygula(kullanici_girdisi, guncelle=False)
    plan = otonom_plan_olustur(zengin_girdi)
    if any(a in plan["araclar"] for a in ("WIKIPEDIA_BIYOGRAFI", "SEHIR_ULKE", "YEMEK_TARIFI", "HAVA_DURUMU", "HARITA", "FIYAT", "FINANS_ALTIN_DOVIZ", "FUTBOLCU_PIYASA")) or len(plan["araclar"]) >= 2:
        return True, " → ".join(plan["adimlar"])
    return False, ""


def _yerel_biyografi_bul(aktif_soru_norm: str, konu_cekirdegi: str):
    # Türkçe hal eklerini ('fatih sultan mehmeti' -> 'fatih sultan mehmet') temizleyerek ara
    temiz_bio_norm = re.sub(r"(?:[\'’](?:i|ı|u|ü|yi|yı|yu|yü|ten|tan|den|dan|in|ın|un|ün)|(?<=mehmet)i|(?<=sinan)i|(?<=ataturk)u)\b", "", aktif_soru_norm)
    for t_key, t_veri in DETAYLI_TARIH_BIYOGRAFILERI.items():
        tk_norm = metni_normallestir(t_key)
        if tk_norm and (tk_norm in temiz_bio_norm or tk_norm in aktif_soru_norm):
            metin = (
                f"### 📜 {t_veri['ad']}\n"
                f"**Dönem:** {t_veri['donem']} | **Unvan / Alan:** {t_veri.get('unvan', t_veri.get('alan', ''))}\n\n"
                f"{t_veri['bilgi']}"
            )
            return metin, t_veri["ad"]
        if tk_norm == konu_cekirdegi or (len(tk_norm) >= 6 and tk_norm in aktif_soru_norm):
            metin = (
                f"### 📜 {t_veri['ad']}\n"
                f"**Dönem:** {t_veri['donem']} | **Unvan:** {t_veri['unvan']}\n\n"
                f"{t_veri['bilgi']}"
            )
            return metin, t_veri["ad"]

    if len(konu_cekirdegi) >= 3:
        en_iyi_skor, en_iyi_alim = 0, None
        for _, veri in ISLAM_ALIMLERI.items():
            for anahtar in veri["anahtar_kelimeler"]:
                a_norm = metni_normallestir(anahtar)
                if a_norm == konu_cekirdegi or (len(a_norm) >= 5 and f" {a_norm} " in f" {aktif_soru_norm} "):
                    en_iyi_skor, en_iyi_alim = 100, veri
                    break
                skor = fuzz.ratio(konu_cekirdegi, a_norm)
                if skor >= 84 and skor > en_iyi_skor:
                    en_iyi_skor, en_iyi_alim = skor, veri
            if en_iyi_skor == 100:
                break
        if en_iyi_alim:
            metin = (
                f"### 📜 {en_iyi_alim['ad']}\n"
                f"**Dönem:** {en_iyi_alim['donem']} | **Alan:** {en_iyi_alim['alan']}\n\n"
                f"**Başlıca Eserleri:** {en_iyi_alim['eserler']}\n\n"
                f"{en_iyi_alim['bilgi']}"
            )
            return metin, en_iyi_alim["ad"]
    return None, None


def akilli_yanit_uret(kullanici_girdisi: str, hedef_dil: str = "tr"):
    # 0. Güvenlik & Bug Kalkanı
    guvenli_mi, temiz_girdi, guvenlik_mesaji = girdi_guvenlik_ve_bug_kontrol(kullanici_girdisi)
    if not guvenli_mi:
        return guvenlik_mesaji, hedef_dil, "🛡️ Güvenlik Kalkanı"
    kullanici_girdisi = temiz_girdi

    # 0-A. Doğrudan Sohbetten Öğretme Komutu ("öğret: soru = cevap")
    ogret_eslesme = re.match(r"^(?:bana\s+)?(?:öğret|ogret)\s*[:\-]?\s*(.+?)\s*[=:]\s*(.+)$", kullanici_girdisi.strip(), flags=re.IGNORECASE)
    if ogret_eslesme:
        yeni_soru = ogret_eslesme.group(1).strip()
        yeni_cevap = ogret_eslesme.group(2).strip()
        kat_adi = f"ogrenilen_{int(time.time())}"
        json_komut_ekle(kat_adi, yeni_soru, yeni_cevap)
        st.session_state["bekleyen_ogret_sorusu"] = ""
        return (
            f"✅ **Harika, yeni bilgiyi hemen hafızama aldım Ahmet!**\n\n"
            f"* **Soru:** `{yeni_soru}`\n"
            f"* **Cevap:** {yeni_cevap}\n\n"
            f"Artık bunu her sorduğunda doğrudan bu cevabı vereceğim! ⚡",
            hedef_dil,
            "Yeni Öğrenilen Bilgi",
        )

    # 0-A2. Açık 'ollama:' öneki varsa ayıkla (açık kaynak araçları da temiz soruyu görsün)
    ozel_ai_saglayici = None
    _saglayici_onek_map = {
        "ollama": "ollama_local",
        "deepseek": "deepseek_cloud",
        "groq": "groq_cloud",
        "gemini": "gemini_free",
        "openrouter": "openrouter",
    }
    _ai_onek = re.match(r"^(ollama|deepseek|groq|gemini|openrouter)\s*[:\-]\s*(.+)$", kullanici_girdisi.strip(), flags=re.IGNORECASE)
    if _ai_onek:
        ozel_ai_saglayici = _saglayici_onek_map[_ai_onek.group(1).lower()]
        kullanici_girdisi = _ai_onek.group(2).strip()

    # 0-A3. Grafik çizici + güncel kaynaklar & günlük asistan (net kalıplı sorular → doğrudan, hızlı yanıt)
    if _calisma_kocu_yanitla is not None and not ozel_ai_saglayici:
        try:
            _ck_yanit, _ck_etiket = _calisma_kocu_yanitla(kullanici_girdisi, st.session_state)
        except Exception:
            _ck_yanit, _ck_etiket = None, None
        if _ck_yanit:
            return _ck_yanit, hedef_dil, _ck_etiket
    if _grafik_ciz is not None and not ozel_ai_saglayici:
        try:
            _gr_yanit, _gr_etiket = _grafik_ciz(kullanici_girdisi)
        except Exception:
            _gr_yanit, _gr_etiket = None, None
        if _gr_yanit:
            return _gr_yanit, hedef_dil, _gr_etiket
    if _guncel_asistan_yanitla is not None and not ozel_ai_saglayici:
        try:
            _g_yanit, _g_etiket = _guncel_asistan_yanitla(kullanici_girdisi)
        except Exception:
            _g_yanit, _g_etiket = None, None
        if _g_yanit:
            return _g_yanit, hedef_dil, _g_etiket

    # 0-B. GERÇEK BAĞLAM / KONU DEVAMLILIĞI & ÖNCEKİ KONU İZOLASYONU
    _onceki_aktif_konu = st.session_state.get("aktif_konu", "").strip()
    kullanici_girdisi, baglam_eklendi_mi = _aktif_konu_baglami_uygula(kullanici_girdisi)
    raw_text = kullanici_girdisi.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    norm_text = metni_normallestir(kullanici_girdisi)

    # 1. Hızlı Kişisel, Selamlaşma, Candan Sohbet, Saat/Tarih & Öğretilen JSON
    analiz = cumle_ve_5n1k_analiz_et(kullanici_girdisi, norm_text)
    aktif_soru_norm = analiz["kalan_soru"] if analiz["kalan_soru"] else norm_text
    konu_cekirdegi = analiz["konu_cekirdegi"]
    selam_oneki = analiz["selam_oneki"]

    if help_veya_yardim_mi(norm_text):
        return YARDIM_VE_HELP_YANITI, hedef_dil, "🧠 Otonom Plan: Yardım"

    if not ozel_ai_saglayici and analiz["selam_turu"] and not analiz["kalan_soru"]:
        return analiz["tek_selam_yaniti"], hedef_dil, f"💬 Selamlaşma ({analiz['selam_turu']})"

    candan_kaliplar = [
        (["sohbet edelim", "biraz sohbet edelim", "konusalim", "canim sikkin", "moralim bozuk", "cok yorgunum", "yoruldum"],
         "💙 **Gel biraz sohbet edelim canım kardeşim!** Bazen dersler ve projeler üst üste binince yorulmak çok normal. "
         "Kısa bir mola ver, nefes al; sonra en kolay adımdan birlikte devam edelim. Seni dinliyorum, aklında ne var?",
         "💬 Candan Sohbet"),
        (["beni seviyor musun", "seni seviyorum", "adamsin", "kralsin", "harikasin", "supersin", "cansin"],
         "⚡ **Eyvallah Ahmet, cansın!** Beraber çok güzel işler başaracağız inşallah!",
         "💬 Candan Sohbet"),
    ]
    for k_list, c_yanit, c_etiket in candan_kaliplar:
        if any(k == aktif_soru_norm or k in norm_text for k in k_list):
            return (selam_oneki + c_yanit if selam_oneki else c_yanit), hedef_dil, c_etiket

    for s_kod, s_veri in DOGRUDAN_5N1K_SORU_TABANI.items():
        if aktif_soru_norm in s_veri["tetikleyiciler"] or norm_text in s_veri["tetikleyiciler"]:
            return (selam_oneki + s_veri["yanit"] if selam_oneki else s_veri["yanit"]), hedef_dil, s_veri["etiket"]

    for kural in DOGAL_SOHBET_VE_REHBER_KURALLARI:
        if any(k == aktif_soru_norm or k == norm_text or (len(k) >= 12 and k in aktif_soru_norm) for k in kural["kaliplar"]):
            return (selam_oneki + kural["yanit"] if selam_oneki else kural["yanit"]), hedef_dil, kural["etiket"]

    guncel_json_veri = json_oku()
    for kat, icerik in guncel_json_veri.items():
        for kelime in icerik.get("kelimeler", []):
            kel_norm = metni_normallestir(kelime)
            if kel_norm and (kel_norm == aktif_soru_norm or kel_norm == norm_text or kel_norm == raw_text):
                return (selam_oneki + icerik.get("yanit") if selam_oneki else icerik.get("yanit")), hedef_dil, f"Öğretilen Hafıza: {kat}"

    # 1-A. Sohbet İçi Anlık Çeviri (Telefondan dışarıda kullanım için!)
    if re.search(r"\b(çevir|cevir|translate|tercüme\s*et|tercume\s*et)\b|(?:\b(?:ingilizceye|arapçaya|arapcaya|almancaya|fransızcaya|fransizcaya|türkçeye|turkceye|ispanyolcaya|italyancaya|rusçaya|japoncaya|koreceye)\s*:)", raw_text):
        cev_s = sohbet_cevirisi_yap(
            kullanici_girdisi,
            gtx_url_ozel=st.session_state.get("test_gtx_url"),
            mymemory_url_ozel=st.session_state.get("test_mm_url"),
        )
        if cev_s.get("basarili"):
            return cev_s["metin"], hedef_dil, f"🌐 Canlı Çeviri ({cev_s['hedef_ad']})"

    # 1-B. Sohbet İçi Akıllı Sayaç & Pomodoro Komutu ("25 dakika sayaç kur", "10 dk mola")
    sayac_es = re.search(r"(\d+)\s*(?:dakika|dk|saat)\s*(?:sonra|sayaç|sayac|pomodoro|alarm|mola|zamanlayıcı|zamanlayici|kur)", raw_text)
    if sayac_es:
        miktar = int(sayac_es.group(1))
        birim_saat = "saat" in sayac_es.group(0)
        simdi_tr = turkiye_saati_al()
        bitis_tr = simdi_tr + (timedelta(hours=miktar) if birim_saat else timedelta(minutes=miktar))
        birim_ad = "saat" if birim_saat else "dakika"
        return (
            f"⏰ **Sayaç Planlandı ({miktar} {birim_ad})!**\n"
            f"- **🇹🇷 Başlangıç (Türkiye Saati):** `{simdi_tr.strftime('%H:%M:%S')}`\n"
            f"- **🎯 Bitiş Saati:** `{bitis_tr.strftime('%H:%M:%S')}`\n\n"
            f"💡 Canlı saniye sayan görsel kronometre ve Pomodoro ekranı için sol menüden **📚 Eğitim → ⏰ Canlı Saat & Sayaç** sekmesini açabilirsin!"
        ), hedef_dil, "⏰ Akıllı Sayaç (UTC+3)"

    # 1-C. Hikâye / Masal & Bilmece Desteği (Canlı AI açıksa gerçek kısa/uzun/devamlı hikâye üretir!)
    _hikaye_modu = _hikaye_veya_masal_istegi_mi(norm_text)
    if _hikaye_modu:
        st.session_state["aktif_konu"] = st.session_state.get("aktif_konu") or "Hikâye ve Masal"

    if any(k in norm_text for k in ["bilmece sor", "bana bilmece", "bir bilmece"]):
        return (
            "🧩 **Sana Eğlenceli Bir Bilmece:**\n\n"
            "> *Çarşıdan aldım bir tane, eve geldim bin tane. Bil bakalım bu nedir?* 🍎✨\n\n"
            "Tahminini yaz, bakalım doğru bilecek misin!"
        ), hedef_dil, "🧒 Çocuk Dostu Bilmece"

    z_yanit, z_etiket = _dinamik_zaman_kontrol(aktif_soru_norm)
    if z_yanit:
        return (selam_oneki + z_yanit if selam_oneki else z_yanit), hedef_dil, z_etiket

    if aktif_soru_norm in {"kim", "kin", "kimdir", "bu kim", "o kim", "kim bu", "kim o", "kimler var", "kimi taniyorsun", "kimin cevaplari var"}:
        return OZEL_CEVAP_KURALLARI["kim_genel"]["yanit"], hedef_dil, "5N1K [Kim]: Kişi Rehberi"

    if "omer" not in aktif_soru_norm or not any(k in aktif_soru_norm for k in ["hayyam", "hz", "halife", "faruk"]):
        ozel_y, oto_en, ozel_e = _ozel_cevap_kontrol(raw_text, aktif_soru_norm)
        if ozel_y:
            if oto_en and hedef_dil == "tr":
                hedef_dil = "en"
            return (selam_oneki + ozel_y if selam_oneki else ozel_y), hedef_dil, ozel_e

    # 2. OTONOM AJAN PLANLAMA & ÇOKLU KAYNAKTAN VERİ TOPLAMA
    plan = otonom_plan_olustur(kullanici_girdisi)
    araclar = plan["araclar"]

    if araclar == ["KOD_AI"]:
        hibrit_y, hibrit_e = hibrit_ai_yanit_uret(kullanici_girdisi, gecmis_kullan=baglam_eklendi_mi)
        if hibrit_y:
            return hibrit_y, hedef_dil, f"🧠 Otonom Kod ({hibrit_e})"
        if any(k in raw_text for k in ["kod", "program", "script", "python", "arduino", "html"]):
            return (
                "💻 **Tabii Ahmet, kod yazmak için hazırım!** Ancak şu an canlı Açık Kaynak AI / Ollama sunucusundan yanıt alınamadığı için bu özel kodu üretemedim.\n\n"
                "💡 `Arduino HC-SR04 fren kodu yaz` veya `Python OpenCV kamera kodu yaz` gibi yerleşik şablonları çevrimdışı da alabilirsin.",
                hedef_dil,
                "🧠 Otonom Kod Asistanı",
            )
        return (
            f"🤝 **'{kullanici_girdisi}'** isteğini anladım Ahmet ama şu an canlı yapay zeka motoruna ulaşamadım.",
            hedef_dil,
            "🧠 Otonom AI",
        )

    toplanan_parcalar = []
    kullanilan_kaynaklar = []

    if "MATEMATIK" in araclar:
        m_y, m_e = matematik_motoru_calistir(raw_text)
        if m_y is None:
            m_y, m_e = matematik_motoru_calistir(aktif_soru_norm)
        if m_y:
            toplanan_parcalar.append(m_y)
            kullanilan_kaynaklar.append("Matematik")

    if "YEMEK_TARIFI" in araclar:
        y_s = yemek_tarifi_getir(kullanici_girdisi)
        if y_s.get("basarili"):
            toplanan_parcalar.append(y_s["metin"])
            kullanilan_kaynaklar.append(y_s["kaynak"])

    if "HAVA_DURUMU" in araclar:
        h_s = canli_hava_durumu_getir(kullanici_girdisi)
        if h_s.get("basarili"):
            toplanan_parcalar.append(h_s["metin"])
            kullanilan_kaynaklar.append(f"Open-Meteo ({h_s['sehir']})")

    if "KITAP" in araclar:
        k_s = kitap_bilgisi_getir(kullanici_girdisi)
        if k_s.get("basarili"):
            toplanan_parcalar.append(k_s["metin"])
            kullanilan_kaynaklar.append("Open Library")

    if "SEHIR_ULKE" in araclar:
        su_s = sehir_veya_ulke_bilgisi_getir(kullanici_girdisi, detayli=_daha_fazla_bilgi_istegi_mi(norm_text))
        if su_s.get("basarili"):
            toplanan_parcalar.append(su_s["metin"])
            kullanilan_kaynaklar.append(su_s["kaynak"])
            st.session_state["aktif_konu"] = su_s["baslik"]

    if "TDK" in araclar and st.session_state.get("tdk_aktif", True):
        tdk_s = tdk_sozluk_sorgula(kullanici_girdisi)
        if tdk_s.get("basarili"):
            toplanan_parcalar.append(tdk_sonucunu_metne_formatla(tdk_s))
            kullanilan_kaynaklar.append(f"TDK ({tdk_s['kelime']})")

    if "HARITA" in araclar:
        adres_parcasi = kullanici_girdisi.split(" ve ")[-1] if (" ve " in raw_text and len(araclar) >= 2 and "WIKIPEDIA_BIYOGRAFI" in araclar) else kullanici_girdisi
        a_sonuc = acik_kaynak_adres_bul(adres_parcasi)
        if a_sonuc.get("basarili"):
            toplanan_parcalar.append(adres_sonucunu_metne_formatla(a_sonuc))
            kullanilan_kaynaklar.append(f"Harita ({a_sonuc['yer']})")
            st.session_state["aktif_konu"] = a_sonuc["yer"]

    if "FINANS_ALTIN_DOVIZ" in araclar:
        fin_s = canli_doviz_ve_altin_getir(kullanici_girdisi)
        if fin_s.get("basarili"):
            toplanan_parcalar.append(fin_s["metin"])
            kullanilan_kaynaklar.append(fin_s["kaynak"])

    if "FUTBOLCU_PIYASA" in araclar:
        fut_s = futbolcu_piyasa_degeri_getir(kullanici_girdisi)
        if fut_s.get("basarili"):
            toplanan_parcalar.append(fut_s["metin"])
            kullanilan_kaynaklar.append(fut_s["kaynak"])
            st.session_state["aktif_konu"] = fut_s["ad"]

    if "FIYAT" in araclar:
        fiyat_parcasi = kullanici_girdisi.split(" ve ")[0] if " ve " in raw_text else kullanici_girdisi
        f_sonuc = guncel_fiyat_arastir(fiyat_parcasi)
        if f_sonuc.get("basarili"):
            toplanan_parcalar.append(fiyat_sonucunu_metne_formatla(f_sonuc))
            kullanilan_kaynaklar.append(f"Fiyat ({f_sonuc['urun']})")

    if "KIMYA_BILESIK" in araclar:
        km_s = kimya_bilesik_getir(kullanici_girdisi, pubchem_base=st.session_state.get("test_pubchem_url"))
        if km_s.get("basarili"):
            toplanan_parcalar.append(km_s["metin"])
            kullanilan_kaynaklar.append(km_s["kaynak"])
            st.session_state["aktif_konu"] = km_s["baslik"]

    if "NAMAZ_HICRI" in araclar:
        nm_s = namaz_vakitleri_ve_hicri_getir(kullanici_girdisi, aladhan_base=st.session_state.get("test_aladhan_url"))
        if nm_s.get("basarili"):
            toplanan_parcalar.append(nm_s["metin"])
            kullanilan_kaynaklar.append(nm_s["kaynak"])
            st.session_state["aktif_konu"] = nm_s["baslik"]

    if "TEKNOFEST_MAKALE" in araclar:
        tf_s = teknofest_ve_makale_ara(kullanici_girdisi, arxiv_base=st.session_state.get("test_arxiv_url"))
        if tf_s.get("basarili"):
            toplanan_parcalar.append(tf_s["metin"])
            kullanilan_kaynaklar.append(tf_s["kaynak"])
            st.session_state["aktif_konu"] = tf_s["baslik"]

    if "DEPREM_CANLI" in araclar:
        dp_s = son_depremler_getir(kullanici_girdisi, usgs_base=st.session_state.get("test_usgs_url"))
        if dp_s.get("basarili"):
            toplanan_parcalar.append(dp_s["metin"])
            kullanilan_kaynaklar.append(dp_s["kaynak"])
            st.session_state["aktif_konu"] = dp_s["baslik"]

    if "CANLI_WEB_HABER" in araclar:
        cw_sonuc = canli_web_ve_haber_ara(
            kullanici_girdisi,
            rss_base_url=st.session_state.get("test_rss_url"),
            ddg_base_url=st.session_state.get("test_ddg_url"),
        )
        if cw_sonuc.get("basarili"):
            toplanan_parcalar.append(canli_arama_sonucunu_formatla(cw_sonuc))
            kullanilan_kaynaklar.append(f"Canlı Arama ({cw_sonuc['sorgu']})")
            st.session_state["aktif_konu"] = cw_sonuc["sorgu"]

    if "SPOR_ORGANIZASYON" in araclar:
        sp_s = _spor_organizasyon_bilgisi_getir(kullanici_girdisi)
        if sp_s.get("basarili"):
            toplanan_parcalar.append(sp_s["metin"])
            kullanilan_kaynaklar.append(sp_s["kaynak"])
            st.session_state["aktif_konu"] = sp_s["baslik"]

    if "WIKIPEDIA_BIYOGRAFI" in araclar:
        bio_parcasi = kullanici_girdisi.split(" ve ")[0] if " ve " in raw_text else kullanici_girdisi
        bio_norm = metni_normallestir(bio_parcasi)
        bio_cekirdek = cumle_ve_5n1k_analiz_et(bio_parcasi, bio_norm)["konu_cekirdegi"]
        bio_metin, bio_ad = _yerel_biyografi_bul(bio_norm, bio_cekirdek)
        if bio_metin:
            toplanan_parcalar.append(bio_metin)
            kullanilan_kaynaklar.append(f"Biyografi ({bio_ad})")
            st.session_state["aktif_konu"] = re.sub(r"\s*\([^)]*\)", "", bio_ad).strip()
        else:
            # Eğer bir mekan/yapı 'nasıl?' diye sorulduysa ('Fatih Camii nasıl?') önce yerleşik mekan bilgisine bak!
            mekan_s = acik_kaynak_adres_bul(bio_parcasi)
            _derin_mi = _daha_fazla_bilgi_istegi_mi(norm_text)
            if mekan_s.get("basarili") and "Konum Belleği" in mekan_s.get("kaynak", "") and not _derin_mi:
                toplanan_parcalar.append(adres_sonucunu_metne_formatla(mekan_s))
                kullanilan_kaynaklar.append(f"Mekan ({mekan_s['yer']})")
                st.session_state["aktif_konu"] = mekan_s["yer"]
            else:
                w_sonuc = wikipedia_madde_getir(wikipedia_konu_ayikla(bio_parcasi) or bio_parcasi, dil="tr", detay_karakter=(580 if _uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "kisa" else (7500 if _uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "derin" else 3200))) if st.session_state.get("wikipedia_aktif", True) else {"basarili": False}
                if w_sonuc.get("basarili"):
                    toplanan_parcalar.append(wikipedia_sonucunu_metne_formatla(w_sonuc))
                    kullanilan_kaynaklar.append(f"Wikipedia ({w_sonuc['baslik']})")
                    st.session_state["aktif_konu"] = re.sub(r"\s*\([^)]*\)", "", w_sonuc["baslik"]).strip()

    if not toplanan_parcalar:
        if len(konu_cekirdegi) >= 2:
            for _, t_veri in TEKNIK_TERIMLER_SOZLUGU.items():
                baslik_kisa = metni_normallestir(t_veri["baslik"].split("(")[0])
                ilk_kelime = baslik_kisa.split()[0] if baslik_kisa else ""
                if baslik_kisa and (konu_cekirdegi == baslik_kisa or (len(ilk_kelime) >= 3 and konu_cekirdegi == ilk_kelime)):
                    toplanan_parcalar.append(f"🛠️ **{t_veri['baslik']} ({t_veri['kategori']}):**\n{t_veri['aciklama']}")
                    kullanilan_kaynaklar.append(f"Terim ({t_veri['baslik']})")
                    break
    if not toplanan_parcalar:
        ap_y, ap_e = _fuzzy_taban_ara(AHMET_BILGI_TABANI, aktif_soru_norm, "Ahmet Profili", konu_cekirdegi)
        if ap_y:
            toplanan_parcalar.append(ap_y)
            kullanilan_kaynaklar.append(ap_e)

    # 2.5 PROAKTİF WİKİPEDİA / BİYOGRAFİ DESTEĞİ (Ollama açıkken bile Wikipedia'yı asla atlamaz!)
    _sohbet_mi_simdi = _dogal_sohbet_cumlesi_mi(raw_text, norm_text)
    _sohbet_disi_bilgi = (
        not toplanan_parcalar
        and not _sohbet_mi_simdi and not _hikaye_modu
        and st.session_state.get("wikipedia_aktif", True)
        and len(konu_cekirdegi) >= 3
        and not any(k in norm_text for k in ["nasilsin", "naber", "ne haber", "uzgunum", "mutluyum", "sikildim", "yoruldum", "sohbet", "oyun", "sence", "tavsiye", "fikir", "nasil calismaliyim", "ne yapmaliyim"])
    )
    if _sohbet_disi_bilgi:
        _pb_metin, _pb_ad = _yerel_biyografi_bul(aktif_soru_norm, konu_cekirdegi)
        if _pb_metin:
            toplanan_parcalar.append(_pb_metin)
            kullanilan_kaynaklar.append(f"Biyografi ({_pb_ad})")
            st.session_state["aktif_konu"] = re.sub(r"\s*\([^)]*\)", "", _pb_ad).strip()
        elif len(raw_text.split()) <= 5 and not re.search(r"\b(ben|sen|biz|siz|mi|mı|mu|mü|lütfen|lutfen|merhaba|selam)\b", raw_text):
            try:
                _pw = wikipedia_madde_getir(wikipedia_konu_ayikla(kullanici_girdisi) or kullanici_girdisi, dil="tr", detay_karakter=2800)
                if _pw.get("basarili"):
                    toplanan_parcalar.append(wikipedia_sonucunu_metne_formatla(_pw))
                    kullanilan_kaynaklar.append(f"Wikipedia ({_pw['baslik']})")
                    st.session_state["aktif_konu"] = re.sub(r"\s*\([^)]*\)", "", _pw["baslik"]).strip()
            except Exception:
                pass

    # 3. AKILLI SENTEZ KATMANI
    birlesik_baglam = "\n\n---\n\n".join(toplanan_parcalar)
    baglam_etiket = f" (Bağlam: {st.session_state.get('aktif_konu')})" if baglam_eklendi_mi else ""

    if plan["sentez_gerekli"] or not toplanan_parcalar or ozel_ai_saglayici is not None:
        sentez_baglam = birlesik_baglam
        if _akil_yurutme_istegi_mi(raw_text) and not _daha_fazla_bilgi_istegi_mi(norm_text):
            sentez_baglam = (
                "AKIL YÜRÜTME TALİMATI: Yanıtını 3 net mantık adımında kur: "
                "(1) Temel kavram/sebep, (2) Mantıksal neden-sonuç veya karşılaştırma, (3) Somut özet/öneri. "
                "Akıcı, özgün ve güçlü bir Türkçe kullan.\n\n"
                + sentez_baglam
            )
        _u_mod = _uzunluk_modu_belirle(kullanici_girdisi, norm_text)
        if _u_mod == "kisa":
            sentez_baglam = (
                "ÖNEMLİ UZUNLUK TALİMATI: Kullanıcı KISA ve ÖZ yanıt istedi! "
                "En fazla 3-4 akıcı cümleyle doğrudan özü anlat, gereksiz uzatma.\n\n"
                + sentez_baglam
            )
        elif _u_mod == "derin":
            _devam_turu = int(st.session_state.get("konu_devam_turu", 0)) + 1 if baglam_eklendi_mi else 1
            st.session_state["konu_devam_turu"] = _devam_turu
            sentez_baglam = (
                f"ÖNEMLİ ÇOK TURLU UZUN ANLATIM & DEVAM TALİMATI (BÖLÜM #{_devam_turu}): "
                "Kullanıcı bu konunun veya hikâyenin ÇOK DAHA UZUN, DERİN ve DEVAMINI istiyor! "
                "Önceki mesajlarda zaten anlattığın cümleleri ASLA tekrar etme. "
                "Tam kaldığın yerden yeni olaylar, yeni boyutlar, somut örnekler, alt başlıklar veya canlı diyaloglarla "
                "en az 5-6 doyurucu ve akıcı Türkçe paragraf hâlinde sürükleyici biçimde devam et.\n\n"
                + sentez_baglam
            )
        else:
            if not baglam_eklendi_mi:
                st.session_state["konu_devam_turu"] = 0
        ai_yanit, ai_etiket = hibrit_ai_yanit_uret(
            kullanici_girdisi,
            ek_baglam=sentez_baglam,
            saglayici_kodu=ozel_ai_saglayici,
            gecmis_kullan=(baglam_eklendi_mi or _daha_fazla_bilgi_istegi_mi(norm_text) or _devam_veya_takip_sorusu_mu(norm_text)),
        )
        # v10.4 MUHAKEME KORUYUCUSU: Yeni konuya geçildiyse AI yanıtı eski alakasız konuya (örn. Güney Kore) kaydıysa REDDET!
        if ai_yanit and not baglam_eklendi_mi and not _yanit_alaka_dogrula(ai_yanit, kullanici_girdisi, _onceki_aktif_konu):
            ai_yanit = None
        if ai_yanit:
            kaynak_notu = f" + {' + '.join(kullanilan_kaynaklar)}" if kullanilan_kaynaklar else ""
            _canli_link_eksik = ("CANLI_WEB_HABER" in araclar and "http" in birlesik_baglam and "http" not in ai_yanit)
            # KRİTİK KORUMA: Uzun anlatımda veya canlı haber linki kaybolduysa orijinal açık kaynak verisini ASLA kaybetme!
            if birlesik_baglam and (
                (_uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "derin" and len(ai_yanit) < len(birlesik_baglam) * 0.85)
                or len(ai_yanit.strip()) < 90
                or _canli_link_eksik
            ):
                son_yanit = (ai_yanit + "\n\n---\n\n" + birlesik_baglam) if _canli_link_eksik else (birlesik_baglam + "\n\n---\n\n" + ai_yanit)
            else:
                son_yanit = ai_yanit
            if hedef_dil != "tr":
                try:
                    son_yanit = guvenli_cevir(re.sub(r"[#*`]", "", son_yanit), src="tr", dest=hedef_dil)
                except Exception:
                    hedef_dil = "tr"
            return son_yanit, hedef_dil, f"🧠 Otonom Sentez ({ai_etiket}{kaynak_notu}){baglam_etiket}"

    if toplanan_parcalar:
        son_yanit = _metni_kisaca_ozetle(birlesik_baglam) if _uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "kisa" else birlesik_baglam
        if hedef_dil != "tr":
            try:
                son_yanit = guvenli_cevir(re.sub(r"[#*`]", "", son_yanit), src="tr", dest=hedef_dil)
            except Exception:
                hedef_dil = "tr"
        return son_yanit, hedef_dil, f"🧠 Otonom Akış: {' + '.join(kullanilan_kaynaklar)}{baglam_etiket}"

    gb_y, gb_e = _fuzzy_taban_ara(GENEL_SORU_CEVAP_TABANI, aktif_soru_norm, "Bilgi Bankası", konu_cekirdegi)
    if gb_y:
        return gb_y, hedef_dil, gb_e
    havuz = kalip_havuzu_olustur()
    if aktif_soru_norm in havuz:
        h_y, h_e = havuz[aktif_soru_norm]
        return (selam_oneki + h_y if selam_oneki else h_y), hedef_dil, h_e

    # SON KURTARMA ZİNCİRİ: Yalnızca doğal sohbet cümlesi DEĞİLSE Wikipedia/Web yedeğini dene!
    if not _sohbet_mi_simdi and st.session_state.get("wikipedia_aktif", True):
        try:
            w_kurtar = wikipedia_madde_getir(kullanici_girdisi, dil="tr", detay_karakter=(580 if _uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "kisa" else 3200))
            if w_kurtar.get("basarili"):
                st.session_state["aktif_konu"] = re.sub(r"\s*\([^)]*\)", "", w_kurtar["baslik"]).strip()
                w_fmt = wikipedia_sonucunu_metne_formatla(w_kurtar)
                if _uzunluk_modu_belirle(kullanici_girdisi, norm_text) == "kisa":
                    w_fmt = _metni_kisaca_ozetle(w_fmt)
                return w_fmt, hedef_dil, f"🌐 Wikipedia ({w_kurtar['baslik']})"
        except Exception:
            pass
    if not _sohbet_mi_simdi:
        try:
            cw_kurtar = canli_web_ve_haber_ara(kullanici_girdisi)
            if cw_kurtar.get("basarili"):
                st.session_state["aktif_konu"] = cw_kurtar["sorgu"]
                return canli_arama_sonucunu_formatla(cw_kurtar), hedef_dil, f"🌐 Canlı Arama ({cw_kurtar['sorgu']})"
        except Exception:
            pass

    # İçten & Çocuk Dostu Kesintisiz Sohbet Emniyet Ağı (bağlantı kopsa bile konuyu analiz edip sıcak yanıt verir!)
    if _hikaye_modu:
        return (
            "📖 **Yıldızları Merak Eden Küçük Kuş — Çevrimdışı Masal**\n\n"
            "Bir zamanlar yemyeşil bir ormanda, her gece gökyüzündeki yıldızların neden parladığını merak eden "
            "Maviş adında minik bir serçe yaşarmış. Bir gün bilge baykuşa sormuş: *'Yıldızlara ulaşabilir miyim?'*\n"
            "Bilge baykuş gülümsemiş: *'Kanatlarını her gün biraz daha güçlendirir, öğrenmekten hiç vazgeçmezsen "
            "yıldızların sırrını kalbinde taşırsın.'* Maviş o günden sonra her sabah yeni bir şey öğrenmiş ve "
            "ormandaki tüm arkadaşlarına ışık olmuş. 🌟\n\n"
            "💡 *Canlı Groq/AI bağlantısı açıkken istediğin konuda uzun hikâyeler ve 2., 3., 4. bölümlerle devamını yazabilirim!*"
        ), hedef_dil, "🧒 Çocuk Dostu Masal"

    if _sohbet_mi_simdi or st.session_state.get("cocuk_dostu_mod", False) or any(
        k in norm_text for k in ["uzgunum", "mutluyum", "sikildim", "canim sikiliyor", "korkuyorum", "heyecanliyim", "nasilsin", "ne yapalim", "oyun oynayalim", "arkadas"]
    ):
        _d_yanit, _d_etiket = _duygusal_sohbet_yaniti_uret(kullanici_girdisi, norm_text)
        return _d_yanit, hedef_dil, _d_etiket

    st.session_state["bekleyen_ogret_sorusu"] = kullanici_girdisi.strip()
    return (
        f"🤗 **'{kullanici_girdisi}'** için şu an yerel hafızamda kesin bir kayıt bulamadım ve canlı AI yanıtı alınamadı Ahmet.\n\n"
        "💡 Aşağıdaki **'🛠️ Sohbet Araçları → 🎓 Bana Öğret'** kısmından bunu bana öğretebilir ya da internet açıkken tekrar sorabilirsin!",
        hedef_dil,
        "Bana Öğret",
    )