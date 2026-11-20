# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.0 — MODÜL 3: AHMET KİŞİSEL PROFİLİ, KİŞİLER ('KİM' CEVAPLARI),
250+ GENEL KÜLTÜR ANSİKLOPEDİSİ VE KALICI JSON HAFIZA YÖNETİMİ (modul_3_veri_ve_kisiler.py)
==============================================================================
"""
from datetime import datetime
import json
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
JSON_DOSYA_ADI = _m1.JSON_DOSYA_ADI
SOHBET_DOSYA_ADI = _m1.SOHBET_DOSYA_ADI
NOTLAR_DOSYA_ADI = _m1.NOTLAR_DOSYA_ADI

OZEL_CEVAP_KURALLARI = {   'ailem': {   'kelime_siniri': False,
                 'otomatik_ingilizce': False,
                 'tetikleyiciler': [   'ailem kim',
                                       'ailem hakkında',
                                       'kaç kardeşiz',
                                       'kardeşlerim kim',
                                       'ailem'],
                 'yanit': 'Baban **Hadi Bey** (1 Ocak 1971 Mardin doğumlu) ve annen **Edibe '
                          "Hanım**'dır; toplam **6 kardeşsiniz**. Ayrıca 18 Haziran doğumlu, 4 "
                          "yaşında Kur'an kursuna giden ve amcasını biraz sinir eden küçük "
                          '**Ömer** var!'},
    'alimler_ozel': {   'kelime_siniri': False,
                        'otomatik_ingilizce': False,
                        'tetikleyiciler': [   '30 islam alimi',
                                              'islam alimleri',
                                              'islam alimleri kimler',
                                              'alimler kimler',
                                              '30 alim',
                                              'bilim insanları listesi'],
                        'yanit': '📜 **Hafızamdaki 30 Büyük İslam Âlimi:**\n'
                                 '1. **El-Cezerî** (Sibernetik & Robotik)\n'
                                 '2. **El-Hârizmî** (Cebir & Algoritma)\n'
                                 '3. **İbn-i Sînâ** (Tıbbın Hükümdarı)\n'
                                 '4. **İbn-i Battûta** (Büyük Seyyah)\n'
                                 '5. **Muhyiddin İbn-i Arabî** (Tasavvuf & Tefekkür)\n'
                                 '6. **El-Bîrûnî** (Jeodezi & Astronomi)\n'
                                 '7. **Fârâbî** (Muallim-i Sânî)\n'
                                 '8. **İbn-i Haldûn** (Sosyoloji & Mukaddime)\n'
                                 "9. **İbnü'l-Heysem** (Optik Biliminin Kurucusu)\n"
                                 '10. **Ali Kuşçu** (Astronomi & Matematik)\n'
                                 '11. **Uluğ Bey** (Semerkant Rasathanesi)\n'
                                 '12. **Ömer Hayyâm** (Cebir & Takvim)\n'
                                 '13. **Pîrî Reis** (Dünya Haritası & Kitâb-ı Bahriye)\n'
                                 '14. **Mimar Sinan** (Mimari Deha)\n'
                                 '15. **Câbir bin Hayyân** (Modern Kimyanın Kurucusu)\n'
                                 '16. **Takîyüddîn er-Râsıd** (İstanbul Rasathanesi)\n'
                                 "17. **Akşemseddin** (Mikrobiyoloji Öncüsü & Fatih'in Hocası)\n"
                                 "18. **Kâtip Çelebi** (Cihannümâ & Keşfü'z-Zünûn)\n"
                                 '19. **Matrakçı Nasuh** (Matematik & Minyatür)\n'
                                 '20. **İbn Rüşd** (Felsefe & Tıp)\n'
                                 "21. **İmam Gazzâlî** (İhyâü Ulûmi'd-Dîn)\n"
                                 "22. **İmam Mâtürîdî** (Kelâm & Kitâbü't-Tevhîd)\n"
                                 '23. **İmam-ı Âzam Ebû Hanîfe** (Fıkıh & Hanefî Mezhebi)\n'
                                 '24. **İmam Şâfiî** (Fıkıh Usulü)\n'
                                 '25. **İmam Buhârî** (Sahîh-i Buhârî)\n'
                                 "26. **Ebü'l-Vefâ el-Bûzcânî** (Trigonometri)\n"
                                 '27. **Sâbit bin Kurra** (Diferansiyel Hesap & Dost Sayılar)\n'
                                 '28. **ez-Zehrâvî** (Modern Cerrahinin Babası)\n'
                                 "29. **İbnü'n-Nefîs** (Küçük Kan Dolaşımı Kaşifi)\n"
                                 '30. **Nasîrüddîn-i Tûsî** (Trigonometri & Merâga Rasathanesi)\n'
                                 '\n'
                                 '💡 İstediğin âlimin adını yazarak (Örn: `El-Cezeri kimdir`, '
                                 '`Harezmi kimdir`) detaylı biyografisini okuyabilir veya sol '
                                 'menüden **📜 İslam Âlimleri Ansiklopedisi** sekmesini '
                                 'açabilirsin!'},
    'edibe': {   'kelime_siniri': True,
                 'otomatik_ingilizce': False,
                 'tetikleyiciler': [   'edibe kim',
                                       'edibe kimdir',
                                       'edibe kın',
                                       'edibe hanım kim',
                                       'annem kim',
                                       'annen kim',
                                       'ahmetin annesi kim',
                                       'edibe'],
                 'yanit': "Edibe Hanım, beni geliştiren yazılımcı Ahmet'in kıymetli annesi ve Hadi "
                          "Bey'in eşidir. 6 evladı vardır ve ailesinin en büyük destekçisidir."},
    'hadi': {   'kelime_siniri': True,
                'otomatik_ingilizce': False,
                'tetikleyiciler': [   'hadi kim',
                                      'hadi kimdir',
                                      'hadi kın',
                                      'baban kim',
                                      'babam kim',
                                      'ahmetin babası kim',
                                      'hadi bey kim',
                                      'hadi bey'],
                'yanit': "Benim yazılımımı yapan kişinin babası. 1 Ocak 1971 yılında Mardin'de "
                         "doğdu, 5. sınıfa kadar okudu, 14 yaşında İstanbul'a geldi. Edibe Hanım "
                         'ile evlendi ve 6 evladı var.'},
    'kim_genel': {   'kelime_siniri': False,
                     'otomatik_ingilizce': False,
                     'tetikleyiciler': [   'bu kim',
                                           'o kim',
                                           'kim bu',
                                           'kim o',
                                           'kimler var',
                                           'kimi tanıyorsun',
                                           'kimin cevapları var'],
                     'yanit': '🧠 **Hafızamdaki Kişi ve Biyografi Kayıtları (500.000+ Kalıp):**\n'
                              '* **Kişisel & Aile:** `Ahmet kim` (`Ben kimim`), `Hadi kim` (`Babam '
                              'kim`), `Edibe kim` (`Annem kim`), `Ömer kim` (`Ömer kın`), `Ailem '
                              'kim`\n'
                              '* **30 İslam Âlimi:** `El-Cezerî`, `El-Hârizmî`, `İbn-i Sînâ`, '
                              '`İbn-i Battûta`, `İbn-i Arabî`, `El-Bîrûnî`, `Fârâbî`, `İbn-i '
                              "Haldûn`, `İbnü'l-Heysem`, `Ali Kuşçu`, `Uluğ Bey`, `Ömer Hayyâm`, "
                              '`Pîrî Reis`, `Mimar Sinan`, `Câbir bin Hayyân`, `Takîyüddîn`, '
                              '`Akşemseddin`, `Kâtip Çelebi`, `Matrakçı Nasuh`, `İbn Rüşd`, `İmam '
                              'Gazzâlî`, `İmam Mâtürîdî`, `İmam-ı Âzam Ebû Hanîfe`, `İmam Şâfiî`, '
                              "`İmam Buhârî`, `Ebü'l-Vefâ`, `Sâbit bin Kurra`, `ez-Zehrâvî`, "
                              "`İbnü'n-Nefîs`, `Nasîrüddîn-i Tûsî`\n"
                              '* **Tarih, Bilim & Spor:** `Hz. Muhammed (s.a.v.)`, `Fatih Sultan '
                              'Mehmet`, `Yavuz Sultan Selim`, `Kanuni`, `Abdülhamid Han`, '
                              '`Selahaddin Eyyubi`, `Atatürk`, `Selçuk Bayraktar`, `Aziz Sancar`, '
                              '`Victor Osimhen`, `Mauro Icardi`, `Muslera`, `Arda Güler`, `Tony '
                              'Stark`, `Aang`, `Mustafa Kutlu`'},
    'kimim': {   'kelime_siniri': False,
                 'otomatik_ingilizce': False,
                 'tetikleyiciler': [   'ben kimim',
                                       'kimim ben',
                                       'beni tanı',
                                       'benim adım ne',
                                       'adım ne',
                                       'ben kın',
                                       'kimim',
                                       'ahmet kim',
                                       'ahmet kimdir',
                                       'ahmet kın',
                                       'seni kim yaptı',
                                       'seni kim kodladı',
                                       'seni kim geliştirdi',
                                       'geliştiricin kim',
                                       'kurucun kim',
                                       'sahibin kim',
                                       'beni kim yaptı'],
                 'yanit': "Sen beni geliştiren yazılımcı **Ahmet**'sin! İstanbul Fatih'te yaşayan, "
                          'Fen ve Sosyal Bilimler Proje Okulu 9. sınıf öğrencisisin (16 yaşında, '
                          '1.83 m boyunda, LGS %7 dilim). Yapay zeka (**AREX AI Studio**), TEKNOFEST '
                          '2027 otonom İHA/drone ve TÜBİTAK 2204-A akıllı bebek arabası projeleri '
                          'geliştiriyorsun.'},
    'kimsin_ozel': {   'kelime_siniri': False,
                       'otomatik_ingilizce': False,
                       'tetikleyiciler': [   'kimsin',
                                             'sen kimsin',
                                             'kimsin sen',
                                             'kmsn',
                                             'kimsn',
                                             'adın ne',
                                             'ismin ne',
                                             'ar kim',
                                             'ar kimdir'],
                       'yanit': 'Ben **Ar** ⚡! Ahmet tarafından Python ve Streamlit ile '
                                'geliştirilen 500.000+ kalıplı yapay zeka asistanı, matematik '
                                'öğretmeni ve bilgi merkeziyim. Sana nasıl yardımcı olabilirim?'},
    'nasilsin_kardesim': {   'kelime_siniri': False,
                             'otomatik_ingilizce': False,
                             'tetikleyiciler': [   'nasılsın kardeşim',
                                                   'naber kardeşim',
                                                   'nasılsın kanka',
                                                   'naber kanka',
                                                   'nasılsın dostum',
                                                   'naber abi'],
                             'yanit': 'İyiyim elhamdülillah, sen nasılsın kardeşim? Projeler nasıl '
                                      'gidiyor?'},
    'nasilsin_ozel': {   'kelime_siniri': False,
                         'otomatik_ingilizce': False,
                         'tetikleyiciler': [   'nasılsın',
                                               'nasilsin',
                                               'nslsn',
                                               'nasılsın ar',
                                               'iyi misin',
                                               'keyifler nasıl'],
                         'yanit': 'Ben iyiyim, sen nasılsın? ⚡'},
    'ne_haber_ozel': {   'kelime_siniri': False,
                         'otomatik_ingilizce': False,
                         'tetikleyiciler': [   'ne haber',
                                               'naber',
                                               'nbr',
                                               'naber ar',
                                               'ne haber ar',
                                               'ne var ne yok'],
                         'yanit': 'İyiyim, senden ne haber? ⚡'},
    'omer': {   'kelime_siniri': True,
                'otomatik_ingilizce': False,
                'tetikleyiciler': [   'ömer kim',
                                      'ömer kimdir',
                                      'ömer kın',
                                      'omer kim',
                                      'omer kın',
                                      'küçük ömer',
                                      'ömer'],
                'yanit': "Ömer 4 yaşında küçük bir çocuk ve amcasını sinir ediyor. 18 Haziran'da "
                         "doğdu ve şu an Kur'an kursunda eğitim görüyor."}}

AHMET_BILGI_TABANI = {   'ahmet_donanim': {   'kelimeler': [   'donanımlarım',
                                          'kartlarım',
                                          '3d yazıcı',
                                          'filament',
                                          'kullandığım teknolojiler',
                                          'yazılım dillerim',
                                          'telefonum',
                                          'cihazlarım'],
                         'yanit': '🛠️ **Donanım, Cihaz ve Yazılım Ekosistemin:**\n'
                                  '* **Yazılım:** Python, PyCharm, Streamlit, GitHub, Google AI '
                                  'Studio, Pydroid 3.\n'
                                  '* **Gömülü Sistemler:** Raspberry Pi 5, Arduino Uno, Arduino '
                                  'Nano, ESP32, L298N, HC-SR04.\n'
                                  '* **Cihazlar:** Samsung Galaxy S25 FE, Galaxy Tab S10+, Galaxy '
                                  'Buds 3 ve PlayStation 5 Slim.'},
    'ahmet_kim': {   'kelimeler': [   'ahmet kim',
                                      'ahmet hakkında',
                                      'benim hakkımda',
                                      'hakkımda ne biliyorsun',
                                      'beni anlat',
                                      'profilim',
                                      'özelliklerim',
                                      'kimlik bilgilerim',
                                      'boyum kaç',
                                      'yaşım kaç'],
                     'yanit': '### 👤 Geliştiricim Ahmet Hakkında Bildiklerim\n'
                              "* **Kimlik & Okul:** 16 yaşında, 1.83 m boyunda, İstanbul Fatih'te "
                              'yaşayan ve Fen ve Sosyal Bilimler Proje Okulu 9. sınıfta okuyan bir '
                              'geliştiricisin.\n'
                              "* **Başarı:** LGS sınavında dershaneye gitmeden %7'lik dilime "
                              'girdin.\n'
                              '* **Projeler:** Beni (**AREX AI Studio**), TEKNOFEST 2027 & TÜBİTAK '
                              '2204-A için **otonom İHA/drone** projesini ve Arduino tabanlı '
                              '**akıllı bebek arabası** prototipini geliştiriyorsun.\n'
                              '* **Teknoloji Yığını:** Python, Streamlit, PyCharm, Pydroid 3, '
                              'Raspberry Pi 5, Arduino Uno/Nano, ESP32, PETG / Carbon Fiber PLA 3D '
                              'baskı.\n'
                              '* **İlgi Alanları:** 100m koşu, yüzme, halı saha futbolu '
                              '(Galatasaray & PSG, Victor Osimhen), zihinden hızlı matematik ve '
                              'İngilizce, Çince, Bengalce dil pratikleri.'},
    'ahmet_projeler': {   'kelimeler': [   'projelerim',
                                           'neler geliştiriyorum',
                                           'drone projem',
                                           'bebek arabası',
                                           'teknofest',
                                           'tübitak',
                                           'akıllı bebek arabası'],
                          'yanit': '🚀 **Aktif Projelerin Ahmet:**\n'
                                   '1. **AREX AI Studio v4.0:** 5 modüllü, 500.000+ kalıplı, '
                                   'masaüstü ve mobil uyumlu yapay zeka asistanın.\n'
                                   '2. **Otonom AI Drone (TEKNOFEST 2027 & TÜBİTAK 2204-A):** 3D '
                                   'baskı gövde, yüz tanıma ve sensör telemetrisi ile tasarladığın '
                                   'otonom İHA projesi.\n'
                                   '3. **Akıllı Bebek Arabası:** Kamera entegrasyonu, DC dişli '
                                   'motorlar, HC-SR04 engel algılama ve güvenlik sistemine sahip '
                                   'prototip.'},
    'ahmet_spor': {   'kelimeler': [   'hangi takımlıyım',
                                       'tuttuğum takım',
                                       'sporlarım',
                                       'hobilerim',
                                       'galatasaray',
                                       'oyunlarım',
                                                                              'ps5'],
                      'yanit': '⚽ **Spor, Oyun ve İlgi Alanların:**\n'
                               'Sıkı bir **Galatasaray** ve **PSG** takipçisisin, favori futbolcun '
                               '**Victor Osimhen**. Aktif olarak 100m sprint koşusu, yüzme ve halı '
                               "saha futbolu yapıyorsun. PS5 Slim'de EA Sports FC 26 ve Red Dead "
                               'Redemption 2 oynuyorsun; Tony Stark ve Aang favori karakterlerin.'},
    'ahmet_zihinden_mat': {   'kelimeler': [   'zihinden matematik',
                                               '76 çarpı 25',
                                               'kendi tekniğim',
                                               'mental aritmetik'],
                              'yanit': '🧠 **Kendi Geliştirdiğin Zihinden Matematik Tekniğin:**\n'
                                       "Sayıları 4'e bölüp 100 ile çarparak veya en yakın yüzlüğe "
                                       'tamamlayıp farkı çıkararak saniyeler içinde işlem '
                                       'yapıyorsun. Örneğin `76 × 24` işleminde `76 / 4 = 19` → '
                                       '`1900`, `1900 - 76 = 1824`!'}}

GENEL_SORU_CEVAP_TABANI = {   '3d_yazici': {   'kelimeler': [   '3d yazıcı nedir',
                                      'petg nedir',
                                      'pla nedir',
                                      '3 boyutlu yazıcı'],
                     'yanit': '🖨️ **3D Baskı:** PLA kolay basılır, PETG darbe ve ısıya '
                              'dayanıklıdır, Carbon Fiber PLA ise drone gövdelerinde yüksek '
                              'mukavemet sağlar.'},
    'algoritma': {   'kelimeler': ['algoritma nedir', 'algoritma ne demek'],
                     'yanit': '⚙️ **Algoritma:** Bir problemi çözmek için izlenen açık ve sonlu '
                              "işlem adımlarıdır. İsmi **El-Hârizmî**'den gelir."},
    'ansiklopedi_madde_001': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 1'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #1 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_002': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 2'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #2 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_003': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 3'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #3 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_004': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 4'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #4 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_005': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 5'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #5 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_006': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 6'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #6 (Erzurum - Plaka 25):** Doğu '
                                          "Anadolu Bölgesi'nde yer alır. Palandöken Kayak Merkezi, "
                                          'Çifte Minareli Medrese ve cağ kebabıyla ünlüdür.'},
    'ansiklopedi_madde_007': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 7'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #7 (Eskişehir - Plaka 26):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Porsuk Çayı, Odunpazarı "
                                          'evleri ve havacılık/üniversite şehri kimliğiyle öne '
                                          'çıkar.'},
    'ansiklopedi_madde_008': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 8'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #8 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_009': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 9'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #9 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_010': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 10'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #10 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_011': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 11'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #11 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_012': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 12'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #12 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_013': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 13'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #13 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_014': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 14'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #14 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_015': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 15'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #15 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_016': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 16'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #16 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_017': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 17'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #17 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_018': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 18'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #18 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_019': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 19'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #19 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_020': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 20'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #20 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_021': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 21'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #21 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_022': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 22'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #22 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_023': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 23'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #23 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_024': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 24'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #24 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_025': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 25'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #25 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_026': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 26'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #26 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_027': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 27'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #27 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_028': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 28'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #28 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_029': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 29'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #29 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_030': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 30'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #30 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_031': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 31'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #31 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_032': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 32'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #32 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_033': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 33'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #33 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_034': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 34'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #34 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_035': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 35'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #35 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_036': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 36'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #36 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_037': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 37'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #37 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_038': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 38'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #38 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_039': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 39'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #39 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_040': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 40'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #40 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_041': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 41'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #41 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_042': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 42'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #42 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_043': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 43'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #43 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_044': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 44'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #44 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_045': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 45'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #45 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_046': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 46'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #46 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_047': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 47'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #47 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_048': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 48'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #48 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_049': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 49'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #49 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_050': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 50'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #50 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_051': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 51'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #51 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_052': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 52'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #52 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_053': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 53'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #53 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_054': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 54'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #54 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_055': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 55'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #55 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_056': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 56'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #56 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_057': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 57'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #57 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_058': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 58'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #58 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_059': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 59'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #59 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_060': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 60'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #60 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_061': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 61'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #61 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_062': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 62'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #62 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_063': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 63'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #63 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_064': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 64'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #64 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_065': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 65'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #65 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_066': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 66'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #66 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_067': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 67'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #67 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_068': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 68'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #68 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_069': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 69'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #69 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_070': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 70'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #70 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_071': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 71'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #71 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_072': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 72'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #72 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_073': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 73'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #73 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_074': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 74'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #74 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_075': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 75'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #75 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_076': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 76'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #76 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_077': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 77'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #77 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_078': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 78'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #78 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_079': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 79'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #79 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_080': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 80'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #80 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_081': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 81'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #81 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_082': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 82'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #82 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_083': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 83'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #83 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_084': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 84'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #84 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_085': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 85'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #85 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_086': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 86'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #86 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_087': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 87'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #87 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_088': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 88'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #88 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_089': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 89'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #89 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_090': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 90'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #90 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_091': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 91'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #91 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_092': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 92'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #92 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_093': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 93'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #93 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_094': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 94'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #94 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_095': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 95'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #95 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_096': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 96'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #96 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_097': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 97'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #97 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_098': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 98'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #98 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_099': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 99'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #99 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_100': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 100'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #100 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_101': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 101'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #101 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_102': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 102'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #102 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_103': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 103'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #103 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_104': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 104'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #104 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_105': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 105'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #105 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_106': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 106'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #106 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_107': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 107'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #107 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_108': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 108'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #108 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_109': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 109'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #109 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_110': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 110'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #110 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_111': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 111'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #111 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_112': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 112'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #112 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_113': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 113'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #113 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_114': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 114'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #114 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_115': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 115'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #115 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_116': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 116'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #116 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_117': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 117'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #117 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_118': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 118'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #118 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_119': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 119'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #119 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_120': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 120'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #120 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_121': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 121'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #121 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_122': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 122'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #122 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_123': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 123'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #123 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_124': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 124'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #124 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_125': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 125'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #125 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_126': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 126'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #126 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_127': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 127'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #127 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_128': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 128'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #128 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_129': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 129'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #129 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_130': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 130'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #130 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_131': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 131'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #131 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_132': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 132'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #132 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_133': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 133'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #133 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_134': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 134'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #134 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_135': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 135'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #135 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_136': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 136'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #136 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_137': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 137'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #137 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_138': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 138'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #138 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_139': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 139'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #139 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_140': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 140'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #140 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_141': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 141'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #141 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_142': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 142'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #142 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_143': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 143'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #143 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_144': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 144'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #144 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_145': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 145'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #145 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_146': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 146'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #146 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_147': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 147'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #147 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_148': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 148'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #148 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_149': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 149'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #149 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_150': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 150'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #150 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_151': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 151'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #151 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_152': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 152'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #152 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_153': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 153'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #153 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_154': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 154'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #154 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_155': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 155'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #155 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_156': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 156'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #156 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_157': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 157'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #157 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_158': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 158'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #158 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_159': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 159'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #159 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_160': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 160'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #160 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_161': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 161'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #161 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_162': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 162'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #162 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_163': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 163'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #163 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_164': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 164'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #164 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_165': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 165'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #165 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_166': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 166'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #166 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_167': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 167'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #167 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_168': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 168'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #168 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_169': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 169'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #169 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_170': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 170'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #170 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_171': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 171'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #171 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_172': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 172'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #172 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_173': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 173'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #173 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_174': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 174'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #174 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_175': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 175'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #175 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_176': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 176'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #176 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_177': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 177'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #177 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_178': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 178'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #178 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_179': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 179'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #179 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_180': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 180'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #180 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_181': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 181'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #181 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_182': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 182'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #182 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_183': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 183'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #183 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_184': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 184'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #184 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_185': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 185'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #185 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_186': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 186'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #186 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_187': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 187'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #187 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_188': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 188'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #188 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_189': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 189'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #189 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_190': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 190'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #190 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_191': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 191'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #191 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_192': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 192'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #192 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_193': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 193'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #193 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_194': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 194'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #194 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_195': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 195'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #195 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_196': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 196'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #196 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_197': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 197'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #197 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_198': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 198'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #198 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_199': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 199'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #199 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_200': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 200'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #200 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_201': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 201'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #201 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_202': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 202'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #202 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'ansiklopedi_madde_203': {   'kelimeler': [   'diyarbakır',
                                                  'diyarbakır bilgi',
                                                  'diyarbakır hakkında',
                                                  'diyarbakır nerenin',
                                                  '21 plaka',
                                                  'plaka 21',
                                                  'genel kültür madde 203'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #203 (Diyarbakır - Plaka 21):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Tarihi "
                                          'Diyarbakır Surları, Hevsel Bahçeleri ve Dicle Nehri ile '
                                          'tanınır.'},
    'ansiklopedi_madde_204': {   'kelimeler': [   'erzurum',
                                                  'erzurum bilgi',
                                                  'erzurum hakkında',
                                                  'erzurum nerenin',
                                                  '25 plaka',
                                                  'plaka 25',
                                                  'genel kültür madde 204'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #204 (Erzurum - Plaka 25):** '
                                          "Doğu Anadolu Bölgesi'nde yer alır. Palandöken Kayak "
                                          'Merkezi, Çifte Minareli Medrese ve cağ kebabıyla '
                                          'ünlüdür.'},
    'ansiklopedi_madde_205': {   'kelimeler': [   'eskişehir',
                                                  'eskişehir bilgi',
                                                  'eskişehir hakkında',
                                                  'eskişehir nerenin',
                                                  '26 plaka',
                                                  'plaka 26',
                                                  'genel kültür madde 205'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #205 (Eskişehir - Plaka 26):** '
                                          "İç Anadolu Bölgesi'nde yer alır. Porsuk Çayı, "
                                          'Odunpazarı evleri ve havacılık/üniversite şehri '
                                          'kimliğiyle öne çıkar.'},
    'ansiklopedi_madde_206': {   'kelimeler': [   'gaziantep',
                                                  'gaziantep bilgi',
                                                  'gaziantep hakkında',
                                                  'gaziantep nerenin',
                                                  '27 plaka',
                                                  'plaka 27',
                                                  'genel kültür madde 206'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #206 (Gaziantep - Plaka 27):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Zeugma Mozaik "
                                          'Müzesi, zengin mutfak kültürü ve sanayisiyle tanınır.'},
    'ansiklopedi_madde_207': {   'kelimeler': [   'i̇stanbul',
                                                  'i̇stanbul bilgi',
                                                  'i̇stanbul hakkında',
                                                  'i̇stanbul nerenin',
                                                  '34 plaka',
                                                  'plaka 34',
                                                  'genel kültür madde 207'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #207 (İstanbul - Plaka 34):** '
                                          "Marmara Bölgesi'nde yer alır. Asya ve Avrupa'yı "
                                          "birleştiren, Fatih Sultan Mehmet'in emaneti dünya "
                                          'metropolüdür.'},
    'ansiklopedi_madde_208': {   'kelimeler': [   'i̇zmir',
                                                  'i̇zmir bilgi',
                                                  'i̇zmir hakkında',
                                                  'i̇zmir nerenin',
                                                  '35 plaka',
                                                  'plaka 35',
                                                  'genel kültür madde 208'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #208 (İzmir - Plaka 35):** Ege '
                                          "Bölgesi'nde yer alır. Saat Kulesi, Efes Antik Kenti ve "
                                          "Ege'nin en büyük liman şehridir."},
    'ansiklopedi_madde_209': {   'kelimeler': [   'kayseri',
                                                  'kayseri bilgi',
                                                  'kayseri hakkında',
                                                  'kayseri nerenin',
                                                  '38 plaka',
                                                  'plaka 38',
                                                  'genel kültür madde 209'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #209 (Kayseri - Plaka 38):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Erciyes Dağı, Mimar "
                                          "Sinan'ın memleketi ve köklü ticaret kültürüyle "
                                          'ünlüdür.'},
    'ansiklopedi_madde_210': {   'kelimeler': [   'kocaeli',
                                                  'kocaeli bilgi',
                                                  'kocaeli hakkında',
                                                  'kocaeli nerenin',
                                                  '41 plaka',
                                                  'plaka 41',
                                                  'genel kültür madde 210'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #210 (Kocaeli - Plaka 41):** '
                                          "Marmara Bölgesi'nde yer alır. Bilişim Vadisi, TÜBİTAK "
                                          'Gebze yerleşkesi ve sanayi merkezidir.'},
    'ansiklopedi_madde_211': {   'kelimeler': [   'konya',
                                                  'konya bilgi',
                                                  'konya hakkında',
                                                  'konya nerenin',
                                                  '42 plaka',
                                                  'plaka 42',
                                                  'genel kültür madde 211'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #211 (Konya - Plaka 42):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Selçuklu başkenti, "
                                          'Mevlânâ Celâleddîn-i Rûmî türbesi ve bilim merkeziyle '
                                          'tanınır.'},
    'ansiklopedi_madde_212': {   'kelimeler': [   'mardin',
                                                  'mardin bilgi',
                                                  'mardin hakkında',
                                                  'mardin nerenin',
                                                  '47 plaka',
                                                  'plaka 47',
                                                  'genel kültür madde 212'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #212 (Mardin - Plaka 47):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Taş mimarisi, "
                                          "Kasımiye Medresesi ve Mezopotamya'ya bakan tarihi "
                                          'dokusuyla eşsizdir.'},
    'ansiklopedi_madde_213': {   'kelimeler': [   'samsun',
                                                  'samsun bilgi',
                                                  'samsun hakkında',
                                                  'samsun nerenin',
                                                  '55 plaka',
                                                  'plaka 55',
                                                  'genel kültür madde 213'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #213 (Samsun - Plaka 55):** '
                                          "Karadeniz Bölgesi'nde yer alır. Milli Mücadele'nin "
                                          "başladığı Karadeniz'in en büyük liman ve eğitim "
                                          'kentidir.'},
    'ansiklopedi_madde_214': {   'kelimeler': [   'trabzon',
                                                  'trabzon bilgi',
                                                  'trabzon hakkında',
                                                  'trabzon nerenin',
                                                  '61 plaka',
                                                  'plaka 61',
                                                  'genel kültür madde 214'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #214 (Trabzon - Plaka 61):** '
                                          "Karadeniz Bölgesi'nde yer alır. Sümela Manastırı, "
                                          'Uzungöl ve Karadeniz kültürünün önemli merkezidir.'},
    'ansiklopedi_madde_215': {   'kelimeler': [   'şanlıurfa',
                                                  'şanlıurfa bilgi',
                                                  'şanlıurfa hakkında',
                                                  'şanlıurfa nerenin',
                                                  '63 plaka',
                                                  'plaka 63',
                                                  'genel kültür madde 215'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #215 (Şanlıurfa - Plaka 63):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Göbeklitepe "
                                          '(tarihin sıfır noktası), Balıklıgöl ve Harran '
                                          'Üniversitesi ile ünlüdür.'},
    'ansiklopedi_madde_216': {   'kelimeler': [   'şırnak',
                                                  'şırnak bilgi',
                                                  'şırnak hakkında',
                                                  'şırnak nerenin',
                                                  '73 plaka',
                                                  'plaka 73',
                                                  'genel kültür madde 216'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #216 (Şırnak - Plaka 73):** '
                                          "Güneydoğu Anadolu Bölgesi'nde yer alır. Cizre ilçesi "
                                          "büyük robotik ve sibernetik âlimi El-Cezerî'nin "
                                          'memleketidir.'},
    'ansiklopedi_madde_217': {   'kelimeler': [   'adana',
                                                  'adana bilgi',
                                                  'adana hakkında',
                                                  'adana nerenin',
                                                  '1 plaka',
                                                  'plaka 1',
                                                  'genel kültür madde 217'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #217 (Adana - Plaka 01):** '
                                          "Akdeniz Bölgesi'nde yer alır. Seyhan ve Ceyhan "
                                          'nehirleri, Çukurova tarımı ve Taşköprü ile ünlüdür.'},
    'ansiklopedi_madde_218': {   'kelimeler': [   'ankara',
                                                  'ankara bilgi',
                                                  'ankara hakkında',
                                                  'ankara nerenin',
                                                  '6 plaka',
                                                  'plaka 6',
                                                  'genel kültür madde 218'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #218 (Ankara - Plaka 06):** İç '
                                          "Anadolu Bölgesi'nde yer alır. Türkiye Cumhuriyeti'nin "
                                          'başkenti, Anıtkabir ve savunma sanayii (ASELSAN, TUSAŞ, '
                                          'ROKETSAN) merkezidir.'},
    'ansiklopedi_madde_219': {   'kelimeler': [   'antalya',
                                                  'antalya bilgi',
                                                  'antalya hakkında',
                                                  'antalya nerenin',
                                                  '7 plaka',
                                                  'plaka 7',
                                                  'genel kültür madde 219'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #219 (Antalya - Plaka 07):** '
                                          "Akdeniz Bölgesi'nde yer alır. Toros Dağları, antik "
                                          'kentleri ve Akdeniz kıyı turizminin başkentidir.'},
    'ansiklopedi_madde_220': {   'kelimeler': [   'bursa',
                                                  'bursa bilgi',
                                                  'bursa hakkında',
                                                  'bursa nerenin',
                                                  '16 plaka',
                                                  'plaka 16',
                                                  'genel kültür madde 220'],
                                 'yanit': '🌍 **Ansiklopedi Maddesi #220 (Bursa - Plaka 16):** '
                                          "Marmara Bölgesi'nde yer alır. Osmanlı'nın ilk başkenti, "
                                          'Uludağ, İskender kebabı ve otomotiv sanayii '
                                          'merkezidir.'},
    'arduino_esp32': {   'kelimeler': [   'arduino nedir',
                                          'esp32 nedir',
                                          'raspberry pi nedir',
                                          'mikrodenetleyici'],
                         'yanit': '🔌 **Gömülü Sistemler:** Arduino sensör/motor kontrolü için, '
                                  'ESP32 Wi-Fi/Bluetooth IoT projeleri için, Raspberry Pi 5 ise '
                                  'görüntü işleme ve AI için idealdir.'},
    'ataturk_cumhuriyet': {   'kelimeler': [   'atatürk',
                                               'mustafa kemal atatürk',
                                               'cumhuriyet ne zaman ilan edildi',
                                               '29 ekim 1923',
                                               'mehmet akif ersoy',
                                               'istiklal marşı',
                                               'necip fazıl kısakürek'],
                              'yanit': '🇹🇷 **Milli Tarih ve Edebiyat:** **Mustafa Kemal Atatürk** '
                                       "Kurtuluş Savaşı'nın başkomutanı ve Türkiye Cumhuriyeti'nin "
                                       '(29 Ekim 1923) kurucusudur. İstiklal Marşımızın şairi '
                                       '**Mehmet Akif Ersoy** (Safahat), Türk şiirinin '
                                       "Sultanü'ş-Şuarâ'sı ise **Necip Fazıl Kısakürek**'tir "
                                       '(Çile, Büyük Doğu).'},
    'bilimin_dogasi': {   'kelimeler': [   'bilimin doğası',
                                           'biyoloji nedir',
                                           'hücre nedir',
                                           'mitokondri',
                                           'fotosentez'],
                          'yanit': '🔬 **Biyoloji & Bilimin Doğası:** Bilimsel bilgi gözlem, '
                                   'hipotez ve deneylerle üretilir. Hücrenin enerji santrali '
                                   '**mitokondri**, protein üretim merkezi **ribozom**dur.'},
    'bolme_konu': {   'kelimeler': [   'bölme nedir',
                                       'bölme işlemi',
                                       'bölme kuralları',
                                       'bölünebilme'],
                      'yanit': '➗ **Bölme İşlemi:** `Bölünen = (Bölen × Bölüm) + Kalan`. Hiçbir '
                               "sayı `0`'a bölünemez (tanımsızdır)!"},
    'carpma_konu': {   'kelimeler': [   'çarpma nedir',
                                        'çarpma işlemi',
                                        'çarpma kuralları',
                                        'zihinden çarpma'],
                       'yanit': "✖️ **Çarpma İşlemi:** Yutan eleman `0`, etkisiz eleman `1`'dir. "
                                '**11 ile pratik çarpma:** `35 × 11` → `3` ve `5` arasına '
                                'toplamlarını (`8`) yaz → **385**!'},
    'cikarma_konu': {   'kelimeler': [   'çıkarma nedir',
                                         'çıkartma nedir',
                                         'çıkarma işlemi',
                                         'çıkarma kuralları'],
                        'yanit': '➖ **Çıkarma İşlemi:** `Eksilen - Çıkan = Fark`. İki eksi yan '
                                 'yana gelirse artı olur: `8 - (-5) = 13`.'},
    'dna': {   'kelimeler': ['dna nedir', 'genetik', 'kromozom'],
               'yanit': '🧬 **DNA:** Canlıların genetik bilgisini taşıyan çift sarmallı moleküldür '
                        '(A, T, G, C bazlarından oluşur).'},
    'dort_halife': {   'kelimeler': [   'dört halife',
                                        'hz ebubekir',
                                        'hz ömer',
                                        'hz osman',
                                        'hz ali',
                                        'halid bin velid',
                                        'ebu eyyub el ensari',
                                        'eyüp sultan'],
                       'yanit': '🕌 **Hulefâ-yi Râşidîn (Dört Halife) ve Sahabeler:** Hz. Ebû Bekir '
                                '(Sıddîk), Hz. Ömer (Fârûk - adaletin timsali), Hz. Osman '
                                "(Zinnûreyn) ve Hz. Ali (Allah'ın Aslanı). İstanbul'un manevi "
                                'muhafızı **Ebû Eyyûb el-Ensârî (Eyüp Sultan)** ise Peygamber '
                                "Efendimizi Medine'de evinde ağırlayan büyük sahabedir."},
    'drone': {   'kelimeler': [   'drone nasıl uçar',
                                  'iha nedir',
                                  'quadcopter',
                                  'otonom drone',
                                  'siha nedir'],
                 'yanit': '🚁 **Drone (İHA):** Dört motorun ikisi saat yönünde, ikisi ters yönde '
                          'dönerek torku dengeler; otonom uçuşta GPS, IMU ve kamera verileri '
                          'birleştirilir.'},
    'dunya_bilim_insanlari': {   'kelimeler': [   'isaac newton',
                                                  'albert einstein',
                                                  'nikola tesla',
                                                  'thomas edison',
                                                  'alan turing',
                                                  'galileo',
                                                  'arşimet',
                                                  'öklid',
                                                  'elon musk',
                                                  'steve jobs'],
                                 'yanit': '🌍 **Dünya Bilim ve Teknoloji İnsanları:** **Newton** '
                                          '(kütle çekimi ve kalkülüs), **Einstein** (izafiyet '
                                          'teorisi `E=mc²`), **Nikola Tesla** (alternatif akım ve '
                                          'kablosuz enerji), **Alan Turing** (modern bilgisayar '
                                          'bilimi ve yapay zeka öncüsü), **Arşimet** (suyun '
                                          'kaldırma kuvveti) ve **Öklid** (geometrinin kurucusu).'},
    'espri': {   'kelimeler': [   'espri yap',
                                  'şaka yap',
                                  'fıkra anlat',
                                  'güldür beni',
                                  'komik bir şey söyle'],
                 'yanit': '😄 Yazılımcı neden denize düşmüş? Çünkü **float** kullanmayı unutmuş! '
                          "(Python'cu neden gözlük takar? Çünkü **C#** göremezmiş!)"},
    'futbolcular_spor': {   'kelimeler': [   'victor osimhen',
                                             'osimhen kim',
                                             'mauro icardi',
                                             'icardi kim',
                                             'muslera',
                                             'fernando muslera',
                                             'fatih terim',
                                             'arda güler',
                                             'barış alper yılmaz',
                                             'mbappe',
                                             'messi',
                                             'ronaldo',
                                             'psg'],
                            'yanit': "⚽ **Futbol Yıldızları:** **Victor Osimhen** (Galatasaray'ın "
                                     "Nijeryalı süper yıldız golcüsü ve Ahmet'in favori oyuncusu), "
                                     '**Mauro Icardi** ve **Fernando Muslera** (Galatasaray '
                                     'efsaneleri), **Fatih Terim** (İmparator), **Arda Güler** '
                                     '(Real Madrid ve Milli Takım yıldızımız), **Mbappé / Messi / '
                                     'Ronaldo** (dünya futbol yıldızları).'},
    'gunes_sistemi': {   'kelimeler': [   'gezegenler',
                                          'güneş sistemi',
                                          'kaç gezegen var',
                                          'en büyük gezegen',
                                          'evrenin yaşı',
                                          'gözlemlenebilir evren'],
                         'yanit': '🪐 **Evren & Güneş Sistemi:** Evren yaklaşık **13,8 milyar** '
                                  'yaşındadır ve gözlemlenebilir evrenin çapı **93 milyar ışık '
                                  "yılı**dır. Güneş Sistemi'nde 8 gezegen vardır."},
    'hal_hatir': {   'kelimeler': [   'nasılsın',
                                      'ne haber',
                                      'naber',
                                      'iyi misin',
                                      'keyifler nasıl',
                                      'ne var ne yok',
                                      'ne yapıyorsun',
                                      'durumlar nasıl'],
                     'yanit': 'Ben iyiyim, sen nasılsın? ⚡'},
    'hz_muhammed': {   'kelimeler': [   'hz muhammed',
                                        'peygamberimiz',
                                        'peygamber efendimiz',
                                        'hz muhammed kimdir',
                                        'son peygamber kimdir'],
                       'yanit': "🌹 **Hz. Muhammed Mustafa (s.a.v.):** 571 yılında Mekke'de doğan, "
                                'âlemlere rahmet olarak gönderilen son peygamberimizdir. 610 '
                                "yılında Hira Mağarası'nda ilk vahyi almış, 622'de Medine'ye "
                                "hicret etmiş ve 632 yılında Medine'de vefat etmiştir."},
    'imanin_sartlari': {   'kelimeler': ['imanın şartları', "iman'ın şartları", 'imanın 6 şartı'],
                           'yanit': "✨ **İmanın 6 Şartı:** Allah'a, Meleklere, Kitaplara, "
                                    'Peygamberlere, Ahiret gününe ve Kadere iman.'},
    'isik_hizi': {   'kelimeler': ['ışık hızı', 'ışık hızı kaç', 'en hızlı şey'],
                     'yanit': '⚡ **Işık Hızı:** Boşlukta saniyede yaklaşık **299.792 kilometre** '
                              '(`~300.000 km/sn`) hızla ilerler.'},
    'islamin_sartlari': {   'kelimeler': [   'islamın şartları',
                                             "islam'ın şartları",
                                             'islamın 5 şartı'],
                            'yanit': "🕌 **İslam'ın 5 Şartı:** Kelime-i Şehadet, Namaz, Oruç, "
                                     'Zekât, Hac.'},
    'istanbul_fethi': {   'kelimeler': [   "istanbul'un fethi",
                                           'fatih sultan mehmet',
                                           'istanbul ne zaman fethedildi',
                                           '1453'],
                          'yanit': "🏰 **İstanbul'un Fethi:** 29 Mayıs 1453'te Fatih Sultan Mehmet "
                                   'tarafından gerçekleştirilmiştir.'},
    'iyiyim_cevabi': {   'kelimeler': [   'iyiyim',
                                          'ben de iyiyim',
                                          'elhamdülillah iyiyim',
                                          'süperim',
                                          'harikayım',
                                          'fena değil',
                                          'çok şükür',
                                          'bomba gibiyim'],
                         'yanit': 'Bunu duyduğuma çok sevindim Ahmet! ⚡ Enerjin yüksekken harika '
                                  'işler çıkarabiliriz.'},
    'karakterler_tony_aang': {   'kelimeler': [   'tony stark',
                                                  'iron man',
                                                  'tony stark kim',
                                                  'aang',
                                                  'avatar aang',
                                                  'aang kim',
                                                  'red dead redemption',
                                                  'arthur morgan',
                                                  'fc 26'],
                                 'yanit': "🎬 **Ahmet'in Favori Karakterleri & Oyunları:** **Tony "
                                          'Stark (Iron Man)** yüksek teknoloji zırhlar ve yapay '
                                          'zeka asistanı (JARVIS / AREX AI gibi!) geliştiren dahi '
                                          'mühendis karakterdir. **Aang (Avatar)** dört elementi '
                                          'ustalıkla kontrol eden hava bükücüdür. Oyunlarda ise '
                                          "PS5 Slim'de **EA Sports FC 26** ve **Red Dead "
                                          'Redemption 2** favorilerindir.'},
    'kimlik': {   'kelimeler': [   'sen kimsin',
                                   'adın ne',
                                   'ismin ne',
                                   'seni kim yaptı',
                                   'seni kim kodladı',
                                   'ne işe yararsın',
                                   'özelliklerin neler'],
                  'yanit': 'Benim adım **Ar** ⚡. Ahmet tarafından Python ve Streamlit ile '
                           'geliştirilen 500.000+ kalıplı yapay zeka asistanı, matematik öğretmeni '
                           've bilgi merkeziyim.'},
    'koklu_sayilar_konu': {   'kelimeler': [   'köklü sayılar',
                                               'karekök nedir',
                                               'köklü sayılar konu anlatımı',
                                               'kök dışına çıkarma',
                                               'köklü ifadeler'],
                              'yanit': '√ **Köklü Sayılar:** `√72 = √(36 × 2) = 6√2`. Kök içleri '
                                       'aynıysa katsayılar toplanır (`3√2 + 5√2 = 8√2`). Bana `kök '
                                       '128` yazarsan adım adım çözerim!'},
    'motivasyon': {   'kelimeler': [   'motivasyon',
                                       'moralim bozuk',
                                       'yoruldum',
                                       'pes etmek',
                                       'başarabilir miyim',
                                       'tavsiye ver',
                                       'canım sıkkın'],
                      'yanit': '💪 **Unutma Ahmet:** Büyük sistemler tek gecede kurulmaz, her gün '
                               "eklenen bir satır kod ve çözülen bir problemle büyür. LGS'de "
                               "dershanesiz %7'lik dilime girmiş, 16 yaşında İHA ve yapay zeka "
                               'geliştiren bir azmin var!'},
    'namaz_vakitleri': {   'kelimeler': [   'beş vakit namaz',
                                            'namaz vakitleri neler',
                                            'günde kaç vakit namaz'],
                           'yanit': '🤲 **Beş Vakit Namaz:** Sabah, Öğle, İkindi, Akşam ve Yatsı '
                                    'namazlarıdır.'},
    'newton_yasalari': {   'kelimeler': [   'newton yasaları',
                                            'kuvvet nedir',
                                            'yer çekimi',
                                            'f=m.a',
                                            'eylemsizlik'],
                           'yanit': "🍎 **Newton'un Hareket Yasaları:** 1) Eylemsizlik, 2) Temel "
                                    'Yasa (`F = m × a`), 3) Etki-Tepki Yasası. Yer çekimi ivmesi '
                                    "`~9,81 m/s²`'dir."},
    'osmanli_padisahlari': {   'kelimeler': [   'osman gazi',
                                                'orhan gazi',
                                                'yavuz sultan selim',
                                                'kanuni sultan süleyman',
                                                'abdülhamid han',
                                                '2. abdülhamid',
                                                'alparslan',
                                                'selahaddin eyyubi'],
                               'yanit': '👑 **Büyük Türk-İslam Hükümdarları:** Sultan Alparslan '
                                        '(1071 Malazgirt), Selahaddin Eyyubi (Kudüs Fatihi), Osman '
                                        'Gazi (Osmanlı kurucusu), Fatih Sultan Mehmet (İstanbul '
                                        'Fatihi), Yavuz Sultan Selim (8 yılda hazineyi dolduran ve '
                                        'Hilafeti getiren sultan), Kanuni Sultan Süleyman (46 yıl '
                                        'zirve dönemi) ve Sultan II. Abdülhamid Han (eğitim, '
                                        'demiryolu ve diplomasi dehası).'},
    'periyodik_tablo': {   'kelimeler': [   'atom nedir',
                                            'periyodik tablo',
                                            'element nedir',
                                            'suyun formülü'],
                           'yanit': '⚗️ **Kimya Temelleri:** Atom; proton, nötron ve '
                                    'elektronlardan oluşur. Suyun formülü **H₂O**, tuzun formülü '
                                    "**NaCl**, altının sembolü **Au**'dur."},
    'pi_sayisi': {   'kelimeler': ['pi sayısı', 'pi kaç', 'pi nedir'],
                     'yanit': '🥧 **Pi (π) Sayısı:** Çemberin çevresinin çapına oranıdır, yaklaşık '
                              '**`3,14159265...`** şeklindedir.'},
    'pisagor': {   'kelimeler': ['pisagor', 'pisagor teoremi', 'hipotenüs', 'dik üçgen'],
                   'yanit': '📐 **Pisagor Teoremi:** Dik üçgende `a² + b² = c²`. Özel üçgenler: '
                            '`3-4-5`, `5-12-13`, `8-15-17`, `7-24-25`.'},
    'python': {   'kelimeler': [   'python nedir',
                                   'python ne işe yarar',
                                   'neden python',
                                   'streamlit nedir'],
                  'yanit': '🐍 **Python & Streamlit:** Python; yapay zeka, veri bilimi ve robotik '
                           'alanlarında dünyanın en popüler dilidir.'},
    'selam': {   'kelimeler': [   'selam',
                                  'merhaba',
                                  'selamün aleyküm',
                                  'sa',
                                  'hi',
                                  'hello',
                                  'hey',
                                  'günaydın',
                                  'iyi akşamlar',
                                  'tünaydın',
                                  'selamlar'],
                 'yanit': 'Aleykümselam Ahmet! ⚡ Ben Ar. Masaüstü ve mobilde 5 modüllü tam gücümle '
                          'hazırım. Bugün ne yapalım?'},
    'selcuk_bayraktar': {   'kelimeler': [   'selçuk bayraktar',
                                             'selcuk bayraktar',
                                             'özdemir bayraktar',
                                             'baykar',
                                             'tb2',
                                             'kızılelma',
                                             'akıncı',
                                             'bayraktar kimdir'],
                            'yanit': "✈️ **Özdemir & Selçuk Bayraktar (Baykar):** Türkiye'nin "
                                     'milli SİHA ve insansız savaş uçağı hamlesinin öncüleridir. '
                                     'Bayraktar TB2,TB3, Akıncı TİHA ve Kızılelma projeleriyle '
                                     'dünya havacılık tarihini değiştirmişlerdir.'},
    'su_kaynama': {   'kelimeler': [   'su kaç derecede kaynar',
                                       'suyun kaynama noktası',
                                       'suyun donma noktası'],
                      'yanit': "💧 Deniz seviyesinde saf su **0 °C**'de donar, **100 °C**'de "
                               'kaynar.'},
    'tesekkur': {   'kelimeler': [   'teşekkürler',
                                     'teşekkür ederim',
                                     'sağ ol',
                                     'eyvallah',
                                     'harikasın',
                                     'süpersin',
                                     'adamsın',
                                     'kralsın',
                                     'çok iyi'],
                    'yanit': 'Rica ederim Ahmet! ⚡ Her zaman yanındayım, başka bir sorun olursa '
                             'hemen yazabilirsin.'},
    'toplama_konu': {   'kelimeler': ['toplama nedir', 'toplama işlemi', 'toplama kuralları'],
                        'yanit': '➕ **Toplama İşlemi:** İki veya daha fazla sayının '
                                 'birleştirilmesidir (`a + b = c`). Değişme özelliği vardır, '
                                 "etkisiz elemanı `0`'dır."},
    'turk_bilim_insanlari': {   'kelimeler': [   'aziz sancar',
                                                 'cahit arf',
                                                 'oktay sinanoğlu',
                                                 'fuat sezgin',
                                                 'vecihi hürkuş',
                                                 'nuri demirağ',
                                                 'hezarfen ahmed çelebi',
                                                 'lagari hasan çelebi'],
                                'yanit': '🔬 **Türk Bilim ve Havacılık Öncüleri:** **Aziz Sancar** '
                                         '(DNA onarımıyla Nobel Kimya Ödülü sahibi), **Cahit Arf** '
                                         '(Arf değişmezi ile ünlü matematikçi), **Fuat Sezgin** '
                                         '(İslam Bilim Tarihi araştırmacısı), **Oktay Sinanoğlu** '
                                         "(Türk Einstein'ı), **Hezârfen Ahmed Çelebi** (Galata'dan "
                                         "Üsküdar'a uçan ilk insan), **Lagâri Hasan Çelebi** (ilk "
                                         'roketli uçuş) ve **Vecihi Hürkuş / Nuri Demirağ** (Türk '
                                         'havacılık sanayii kurucuları).'},
    'turkiye_baskent': {   'kelimeler': [   "türkiye'nin başkenti",
                                            'başkent neresi',
                                            'ankara',
                                            'türkiye kaç il'],
                           'yanit': "🇹🇷 Türkiye Cumhuriyeti'nin başkenti **Ankara**'dır (13 Ekim "
                                    "1923) ve Türkiye'de **81 il** bulunmaktadır."},
    'uslu_sayilar_konu': {   'kelimeler': [   'üslü sayılar',
                                              'üslü ifadeler',
                                              'üs alma kuralları',
                                              'kuvvet alma'],
                             'yanit': '🔺 **Üslü Sayılar (`aⁿ`):** `a⁰ = 1`, `a⁻ⁿ = 1/aⁿ`. Çarpmada '
                                      'üsler toplanır (`2³ × 2⁴ = 2⁷`), bölmede üsler çıkarılır.'},
    'uzun_hikaye': {   'kelimeler': ['uzun hikaye', 'mustafa kutlu', 'bulgarie ali', 'ayla'],
                       'yanit': "📖 **Uzun Hikâye (Mustafa Kutlu):** Bulgaryalı Ali'nin adalet "
                                'arayışı, kasabadan kasabaya göçü ve ailesiyle yaşadığı samimi '
                                'hayatı anlatan eserdir.'},
    'veda': {   'kelimeler': [   'görüşürüz',
                                 'hoşça kal',
                                 'bay bay',
                                 "allah'a emanet",
                                 'iyi geceler',
                                 'kapatıyorum',
                                 'sonra görüşürüz'],
                'yanit': "Allah'a emanet ol Ahmet! Tüm sohbet geçmişini balonlarıyla hafızamda "
                         'sakladım. Görüşmek üzere! ⚡'},
    'yapay_zeka': {   'kelimeler': [   'yapay zeka nedir',
                                       'ai nedir',
                                       'makine öğrenmesi',
                                       'derin öğrenme',
                                       'llm nedir'],
                      'yanit': '🤖 **Yapay Zeka (AI):** İnsan zekâsına özgü öğrenme, akıl yürütme '
                               've problem çözme görevlerini yerine getiren bilgisayar '
                               'sistemleridir.'}}

def json_veritabani_hazirla():
    varsayilan_veri = {
        "dini_selam": {
            "kelimeler": ["selamünaleyküm", "selamun aleykum", "selamün aleyküm", "sa", "s.a"],
            "yanit": "Aleykümselam Ahmet! ⚡ Hoş geldin, bugün sana nasıl yardımcı olabilirim?",
        },
        "merhaba_selam": {
            "kelimeler": ["merhaba", "mrb", "merhabalar", "hey", "hello"],
            "yanit": "Merhaba Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?",
        },
        "gunluk_selam": {
            "kelimeler": ["selam", "slm", "selamlar"],
            "yanit": "Selam Ahmet! ⚡ Hoş geldin, bugün hangi konu veya proje üzerinde çalışıyoruz?",
        },
    }
    if not os.path.exists(JSON_DOSYA_ADI):
        with open(JSON_DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(varsayilan_veri, f, ensure_ascii=False, indent=4)
    else:
        try:
            with open(JSON_DOSYA_ADI, "r", encoding="utf-8") as f:
                mevcut = json.load(f)
            # Eski sürümde "merhaba" ve "sa" aynı "selamlasma" içinde birleşik kalmışsa otomatik ayır
            if "selamlasma" in mevcut and "merhaba" in mevcut["selamlasma"].get("kelimeler", []):
                del mevcut["selamlasma"]
                mevcut.update(varsayilan_veri)
                with open(JSON_DOSYA_ADI, "w", encoding="utf-8") as f_w:
                    json.dump(mevcut, f_w, ensure_ascii=False, indent=4)
        except Exception:
            pass


def json_oku():
    json_veritabani_hazirla()
    try:
        with open(JSON_DOSYA_ADI, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON okuma hatası: {e}")
        return {}


def json_komut_ekle(kategori: str, kelimeler_metni: str, yanit_metni: str):
    veri = json_oku()
    kat_key = kategori.lower().strip().replace(" ", "_")
    yeni_kelimeler = [k.lower().strip() for k in kelimeler_metni.split(",") if k.strip()]
    if kat_key in veri:
        for k in yeni_kelimeler:
            if k not in veri[kat_key]["kelimeler"]:
                veri[kat_key]["kelimeler"].append(k)
        if yanit_metni.strip():
            veri[kat_key]["yanit"] = yanit_metni.strip()
    else:
        veri[kat_key] = {"kelimeler": yeni_kelimeler, "yanit": yanit_metni.strip()}
    with open(JSON_DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)


def json_kategori_sil(kat_key: str):
    veri = json_oku()
    if kat_key in veri:
        del veri[kat_key]
        with open(JSON_DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)


def sohbet_gecmisi_yukle():
    if os.path.exists(SOHBET_DOSYA_ADI):
        try:
            with open(SOHBET_DOSYA_ADI, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass
    return [
        {
            "role": "assistant",
            "content": (
                "Merhaba Ahmet! ⚡ **AREX AI Studio v4.0 (5 Modüllü Kurumsal Mimari & 500.000+ Kalıp)** hazır.\n\n"
                "Tüm yazılar **ultra kalın ve yüksek kontrastlı**, geçmiş konuşmaların **günlük baloncuklar** halinde, "
                "ses motorun **doğal Neural ses** ve matematik/fizik/kimya çözücülerin tam kapasite devrede!"
            ),
            "zaman": datetime.now().strftime("%H:%M:%S"),
            "tarih": datetime.now().strftime("%Y-%m-%d"),
            "etiket": "Sistem Başlatıldı",
        }
    ]


def sohbet_gecmisi_kaydet(mesajlar):
    try:
        with open(SOHBET_DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(mesajlar, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.toast(f"Geçmiş kaydedilemedi: {e}", icon="⚠️")


def proje_notlari_oku():
    if os.path.exists(NOTLAR_DOSYA_ADI):
        try:
            with open(NOTLAR_DOSYA_ADI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {"baslik": "TEKNOFEST Otonom İHA", "icerik": "Carbon Fiber PLA gövde ve yüz tanıma telemetrisi test edilecek.", "tarih": "2026-11-16"},
        {"baslik": "Akıllı Bebek Arabası", "icerik": "HC-SR04 ultrasonik sensör ve kamera entegrasyonu kontrol edilecek.", "tarih": "2026-11-16"},
    ]


def proje_notu_ekle(baslik: str, icerik: str):
    notlar = proje_notlari_oku()
    notlar.insert(0, {"baslik": baslik.strip(), "icerik": icerik.strip(), "tarih": datetime.now().strftime("%Y-%m-%d %H:%M")})
    with open(NOTLAR_DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(notlar, f, ensure_ascii=False, indent=4)
