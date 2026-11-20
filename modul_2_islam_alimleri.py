# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v4.0 — MODÜL 2: 30 BÜYÜK İSLAM ÂLİMİ ANSİKLOPEDİSİ, ESERLERİ VE
SESLİ BİYOGRAFİ STÜDYOSU (modul_2_islam_alimleri.py)
==============================================================================
"""
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
    for _ana in [_MODUL_DIZINI, os.path.dirname(_MODUL_DIZINI)]:
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

ISLAM_ALIMLERI = {'aksemsettin': {'ad': 'Akşemseddin (Muhammed Şemseddin)',
                 'alan': 'Tıp, Mikrobiyoloji, Tasavvuf',
                 'anahtar_kelimeler': ['akşemseddin', 'aksemsettin', 'mikrop', 'fatihin hocası'],
                 'bilgi': "Fatih Sultan Mehmet'in hocası ve büyük tıp âlimidir. 'Mâddetü'l-Hayât' "
                          'eserinde hastalıkların gözle görülmeyen canlı tohumlar (mikroplar) '
                          'yoluyla bulaştığını açıkça yazmıştır.',
                 'donem': '1389 – 1459 (Şam – Göynük)',
                 'eserler': "Mâddetü'l-Hayât, Risâletü'n-Nûriyye"},
 'ali_kuscu': {'ad': 'Ali Kuşçu (Alâeddin Ali bin Muhammed)',
               'alan': 'Astronomi, Matematik, Kelâm',
               'anahtar_kelimeler': ['ali kuşçu', 'ali kuscu', 'kuşçu'],
               'bilgi': "Fatih Sultan Mehmet'in davetiyle İstanbul'a gelmiş, İstanbul'un enlem ve "
                        "boylamını yeniden hesaplamış ve Ay'ın haritasını çıkarmıştır.",
               'donem': '1403 – 1474 (Semerkant – İstanbul)',
               'eserler': "Risâle fi'l-Hey'e, Risâle fi'l-Hisâb"},
 'biruni': {'ad': 'El-Bîrûnî (Ebû Reyhân Muhammed)',
            'alan': 'Astronomi, Matematik, Jeodezi, Eczacılık',
            'anahtar_kelimeler': ['biruni', 'bîrûnî', 'el biruni', 'dünyanın yarıçapı'],
            'bilgi': "Dünya'nın yarıçapını ve çevresini kendi geliştirdiği trigonometrik "
                     'yöntemlerle bugünkü değerine çok yakın hesaplamış, yer çekiminin varlığına '
                     "Newton'dan asırlar önce işaret etmiştir.",
            'donem': '973 – 1048 (Hârizm – Gazne)',
            'eserler': "El-Kânûnü'l-Mes'ûdî, Tahdîdü Nihâyâti'l-Emâkin"},
 'cabir_bin_hayyan': {'ad': 'Câbir bin Hayyân',
                      'alan': 'Kimya, Simya, Eczacılık',
                      'anahtar_kelimeler': ['cabir', 'câbir', 'cabir bin hayyan', 'kimya kurucusu'],
                      'bilgi': 'Deneysel kimyanın kurucusu kabul edilir. Damıtma (imbik) ve '
                               'kristalleştirme yöntemlerini geliştirmiş, nitrik ve sülfürik asidi '
                               'keşfetmiştir.',
                      'donem': '721 – 815 (Tûs – Kûfe)',
                      'eserler': "Kitâbü'l-Kimyâ, Kitâbü's-Seb'în"},
 'cezeri': {'ad': "El-Cezerî (Bedîüzzamân Ebü'l-İz İsmâil)",
            'alan': 'Sibernetik, Robotik, Mekanik Mühendisliği',
            'anahtar_kelimeler': ['cezeri',
                                  'el cezeri',
                                  'el-cezeri',
                                  'cezerî',
                                  'filli su saati',
                                  'sibernetik kurucusu',
                                  'robotik kurucusu'],
            'bilgi': "1136–1206 yılları arasında Artuklu Beyliği döneminde Diyarbakır ve Cizre'de "
                     'yaşamış; **sibernetik, robotik ve otomatik kontrol mühendisliğinin '
                     "kurucusu** kabul edilen büyük İslam mucididir. Leonardo da Vinci'den "
                     'yaklaşık 300 yıl önce kendi kendine çalışan mekanik sistemler tasarlamış ve '
                     "tüm çizimlerini **Kitâbü'l-Hiyel** (Olağanüstü Mekanik Araçların Bilgisi) "
                     'adlı eserinde toplamıştır.\n'
                     '\n'
                     '**⚙️ Başlıca İcatları ve Mühendislik Mirası:**\n'
                     '• **Filli Su Saati:** Farklı kültürleri temsil eden figürlerle her yarım '
                     'saatte bir sesli ve hareketli çalışan otomatik zaman mekanizması.\n'
                     '• **Krank-Biyel ve Eksantrik Mekanizması:** Dairesel hareketi doğrusal '
                     'harekete çeviren ve bugünkü otomobil motorlarının temelini oluşturan '
                     'düzenek.\n'
                     '• **Otomatik Su Pompaları ve Robotik Hizmetçiler:** Su ve ağırlık dengesiyle '
                     'abdest suyu döken, şerbet ikram eden ve müzik çalan programlanabilir '
                     'otomatlar.',
            'donem': '1136 – 1206 (Artuklu / Cizre)',
            'eserler': "Kitâbü'l-Hiyel"},
 'ebul_vefa': {'ad': "Ebü'l-Vefâ el-Bûzcânî",
               'alan': 'Trigonometri, Astronomi, Matematik',
               'anahtar_kelimeler': ['ebül vefa', 'ebul vefa', 'buzcani', 'tanjant'],
               'bilgi': 'Trigonometride tanjant, kotanjant, sekant ve kosekant fonksiyonlarını '
                        'tanımlayan ve küresel trigonometriyi geliştiren büyük matematikçidir.',
               'donem': '940 – 998 (Bûzcan – Bağdat)',
               'eserler': "Kitâbü'l-Mecistî"},
 'farabi': {'ad': 'Fârâbî (Ebû Nasr Muhammed)',
            'alan': 'Felsefe, Mantık, Siyaset Bilimi, Müzik',
            'anahtar_kelimeler': ['farabi', 'fârâbî', 'muallim-i sani', 'medinetül fazıla'],
            'bilgi': "'Muallim-i Sânî' (İkinci Öğretmen) unvanıyla anılır. İdeal devlet düzenini "
                     "anlattığı El-Medînetü'l-Fâzıla siyaset felsefesinin başyapıtlarındandır.",
            'donem': '872 – 950 (Fârâb – Şam)',
            'eserler': "El-Medînetü'l-Fâzıla, Kitâbü'l-Mûsîka'l-Kebîr"},
 'harezmi': {'ad': 'El-Hârizmî (Muhammed bin Mûsâ el-Hârizmî)',
             'alan': 'Matematik, Cebir, Algoritma, Astronomi',
             'anahtar_kelimeler': ['harezmi',
                                   'hârizmî',
                                   'harizmi',
                                   'algoritma kurucusu',
                                   'cebir kurucusu',
                                   'sıfırı bulan'],
             'bilgi': "780–850 yılları arasında Bağdat'taki büyük bilim merkezi **Beytülhikme**'de "
                      'çalışmış; **cebir (algebra)** biliminin kurucusu ve modern bilgisayar '
                      'biliminin temel taşı olan **algoritma** kavramının isim babasıdır.\n'
                      '\n'
                      '**📐 Matematiğe ve Bilime Mirası:**\n'
                      "• **El-Cebr ve'l-Mukâbele:** 1. ve 2. derece denklemlerin sistematik çözüm "
                      'yöntemlerini ilk kez bağımsız bir bilim dalı olarak ortaya koymuştur.\n'
                      '• **Sıfır (0) ve Onluk Sistem:** Hint-Arap rakamlarını ve sıfırın basamak '
                      "değerini tanıtarak Avrupa'da modern aritmetiğin doğmasını sağlamıştır.\n"
                      "• **Algoritma Adı:** Eserlerinin Latince çevirilerinde adının 'Algorismi' "
                      "şeklinde okunmasıyla adım adım problem çözme yöntemine 'algoritma' adı "
                      'verilmiştir.',
             'donem': '780 – 850 (Abbâsî / Bağdat Beytülhikme)',
             'eserler': "El-Kitâbü'l-Muhtasar fî Hisâbi'l-Cebr ve'l-Mukâbele"},
 'ibn_nefis': {'ad': "İbnü'n-Nefîs",
               'alan': 'Tıp, Fizyoloji, Anatomi',
               'anahtar_kelimeler': ['ibnün nefis', 'ibn nefis', 'küçük kan dolaşımı'],
               'bilgi': "Akciğerlerdeki küçük kan dolaşımını (pulmoner dolaşım) Avrupa'dan "
                        'yaklaşık 300 yıl önce keşfederek tıp tarihinde devrim yapmıştır.',
               'donem': '1213 – 1288 (Şam – Kahire)',
               'eserler': "Şerhu Teşrîhi'l-Kânûn"},
 'ibni_arabi': {'ad': 'Muhyiddin İbn-i Arabî',
                'alan': 'Tasavvuf, İslam Felsefesi, Tefsir',
                'anahtar_kelimeler': ['ibni arabi',
                                      'ibn-i arabi',
                                      'ibn arabi',
                                      'muhyiddin',
                                      'şeyh-i ekber',
                                      'fütuhatı mekkiyye'],
                'bilgi': "İslam düşünce tarihinde 'Şeyh-i Ekber' unvanıyla anılan büyük mutasavvıf "
                         "ve mütefekkirdir. Anadolu'da Konya ve Malatya'da bulunmuş, yüzlerce eser "
                         'kaleme almıştır.',
                'donem': '1165 – 1240 (Endülüs – Şam)',
                'eserler': "Fütûhât-ı Mekkiyye, Fusûsü'l-Hikem"},
 'ibni_battuta': {'ad': 'İbn-i Battûta (Ebû Abdillâh Muhammed)',
                  'alan': 'Coğrafya, Seyahatname, Antropoloji, Tarih',
                  'anahtar_kelimeler': ['ibni batuta',
                                        'ibni battuta',
                                        'ibn-i batuta',
                                        'ibn battuta',
                                        'seyyah',
                                        'rıhle'],
                  'bilgi': "Orta Çağ'ın en büyük seyyahı kabul edilir. Yaklaşık 29 yıl süren "
                           'yolculuklarında 120.000 kilometreden fazla yol katetmiş, üç kıtadaki '
                           'şehirleri ve kültürleri kayıt altına almıştır.',
                  'donem': '1304 – 1369 (Tanca / Fas)',
                  'eserler': 'Rıhle (İbn Battûta Seyahatnamesi)'},
 'ibni_haldun': {'ad': 'İbn-i Haldûn (Abdurrahman bin Muhammed)',
                 'alan': 'Sosyoloji, Tarih Felsefesi, İktisat',
                 'anahtar_kelimeler': ['ibni haldun',
                                       'ibn-i haldun',
                                       'ibn haldun',
                                       'mukaddime',
                                       'sosyoloji kurucusu'],
                 'bilgi': 'Modern sosyolojinin, tarih felsefesinin ve iktisat biliminin öncüsü '
                          "kabul edilir. Mukaddime'de devletlerin yükseliş ve çöküş süreçlerini "
                          "'asabiyet' kavramıyla açıklamıştır.",
                 'donem': '1332 – 1406 (Tunus – Kahire)',
                 'eserler': "Mukaddime, Kitâbü'l-İber"},
 'ibni_rusd': {'ad': 'İbn Rüşd (Averroes)',
               'alan': 'Felsefe, Tıp, Hukuk, Astronomi',
               'anahtar_kelimeler': ['ibni rüşd', 'ibn rüşd', 'ibn rusd', 'averroes'],
               'bilgi': 'Endülüslü büyük filozof ve hekimdir. Aristo üzerine yaptığı şerhler '
                        "Avrupa'da Rönesans düşüncesinin doğuşuna doğrudan kaynaklık etmiştir.",
               'donem': '1126 – 1198 (Kurtuba / Endülüs)',
               'eserler': "Tehâfütü't-Tehâfüt, El-Külliyyât fi't-Tıb"},
 'ibni_sina': {'ad': 'İbn-i Sînâ (Ebû Alî el-Hüseyn bin Abdillâh)',
               'alan': 'Tıp, Felsefe, Kimya, Fizik',
               'anahtar_kelimeler': ['ibni sina',
                                     'ibn-i sina',
                                     'ibn sina',
                                     'avicenna',
                                     'tıbbın hükümdarı',
                                     'el kanun fit tıb'],
               'bilgi': "980–1037 yılları arasında Buhara'da doğup İslam dünyasında "
                        "**'Eş-Şeyhü'r-Reîs'**, Batı dünyasında ise **'Avicenna'** ve **'Tıbbın "
                        "Hükümdarı'** unvanlarıyla anılan çok yönlü tıp, felsefe, fizik ve "
                        "astronomi bilginidir. Henüz 10 yaşında Kur'an-ı Kerim'i ezberlemiş, 18 "
                        'yaşında döneminin tüm tıp ve felsefe kaynaklarına hâkim olarak Samani '
                        'hükümdarını tedavi etmiştir.\n'
                        '\n'
                        '**📚 Bilime Katkıları:**\n'
                        "• **El-Kânûn fi't-Tıb (Tıbbın Kanunu):** 5 ciltlik dev tıp ansiklopedisi, "
                        'Latinceye çevrilerek Avrupa üniversitelerinde **600 yıl boyunca** temel '
                        'ders kitabı olarak okutulmuştur.\n'
                        '• **Klinik Tıp ve Karantina:** Bulaşıcı hastalıkların su ve hava yoluyla '
                        'geçtiğini belirtmiş, 40 günlük karantina yöntemini önermiş, göz anatomisi '
                        've cerrahi aletler üzerine öncü tarifler yazmıştır.',
               'donem': '980 – 1037 (Buhara – Hemedan)',
               'eserler': "El-Kânûn fi't-Tıb, Kitâbü'ş-Şifâ"},
 'ibnul_heysem': {'ad': "İbnü'l-Heysem (Hasan bin Heysem)",
                  'alan': 'Optik, Fizik, Matematik, Bilimsel Yöntem',
                  'anahtar_kelimeler': ['ibnül heysem',
                                        'ibnul heysem',
                                        'heysem',
                                        'optik kurucusu',
                                        'alhazen',
                                        'camera obscura'],
                  'bilgi': 'Modern optik biliminin kurucusu ve deneysel bilimsel yöntemin '
                           'öncüsüdür. Karanlık oda (camera obscura) çalışmaları modern '
                           'kameraların temelini atmıştır.',
                  'donem': '965 – 1040 (Basra – Kahire)',
                  'eserler': "Kitâbü'l-Menâzır"},
 'imam_azam': {'ad': "İmam-ı Âzam Ebû Hanîfe (Nu'mân bin Sâbit)",
               'alan': 'Fıkıh, İslam Hukuku, Kelâm',
               'anahtar_kelimeler': ['imam-ı azam', 'imam azam', 'ebu hanife', 'hanefi'],
               'bilgi': 'İslam hukukunda Hanefî mezhebinin kurucusudur. Kıyas ve istihsan '
                        'yöntemleriyle hukuki meselelerin çözümünde sistematik bir çığır açmıştır.',
               'donem': '699 – 767 (Kûfe – Bağdat)',
               'eserler': "El-Fıkhü'l-Ekber"},
 'imam_buhari': {'ad': 'İmam Buhârî (Muhammed bin İsmâil)',
                 'alan': 'Hadis İlmi, Tarih',
                 'anahtar_kelimeler': ['buhari', 'imam buhari', 'sahih-i buhari'],
                 'bilgi': 'Binlerce hadisi senet ve ravilerini titizlikle inceleyerek derlediği '
                          'Sahîh-i Buhârî eseriyle hadis ilminin zirve ismidir.',
                 'donem': '810 – 870 (Buhara – Semerkant)',
                 'eserler': "El-Câmiu's-Sahîh (Sahîh-i Buhârî)"},
 'imam_gazali': {'ad': "İmam Gazzâlî (Hüccetü'l-İslâm)",
                 'alan': 'Kelâm, Fıkıh, Felsefe, Ahlâk',
                 'anahtar_kelimeler': ['gazali', 'gazzali', 'imam gazali', 'ihya'],
                 'bilgi': 'Nizâmiye Medresesi başmüderrisi ve İslam düşünce tarihinin en etkili '
                          'âlimlerindendir. Akıl ile kalp (maneviyat) arasındaki dengeyi '
                          'sistemleştirmiştir.',
                 'donem': '1058 – 1111 (Tûs / Horasan)',
                 'eserler': "İhyâü Ulûmi'd-Dîn, El-Munkız mine'd-Dalâl"},
 'imam_maturidi': {'ad': 'İmam Mâtürîdî (Ebû Mansûr)',
                   'alan': 'Kelâm, Tefsir, İslam Akaidi',
                   'anahtar_kelimeler': ['maturidi', 'imam maturidi', 'kitabüt tevhid'],
                   'bilgi': 'Ehl-i Sünnet kelâm okulunun kurucularındandır. Dini metinlerin '
                            'anlaşılmasında aklın ve bilginin vazgeçilmez rolünü vurgulamıştır.',
                   'donem': '853 – 944 (Semerkant)',
                   'eserler': "Kitâbü't-Tevhîd, Te'vîlâtü'l-Kur'ân"},
 'imam_safii': {'ad': 'İmam Şâfiî (Muhammed bin İdrîs)',
                'alan': 'Fıkıh Usulü, İslam Hukuku',
                'anahtar_kelimeler': ['imam şafii', 'imam safii', 'er-risale'],
                'bilgi': 'İslam hukuk metodolojisini (Fıkıh Usulü) ilk kez bağımsız bir disiplin '
                         'olarak kaleme alan büyük hukuk bilginidir.',
                'donem': '767 – 820 (Gazze – Kahire)',
                'eserler': 'Er-Risâle, El-Ümm'},
 'katip_celebi': {'ad': 'Kâtip Çelebi (Hacı Halîfe)',
                  'alan': 'Coğrafya, Bibliyografya, Tarih',
                  'anahtar_kelimeler': ['katip çelebi',
                                        'katip celebi',
                                        'cihannüma',
                                        'keşfüz zünun'],
                  'bilgi': "Osmanlı'nın en büyük coğrafya ve ansiklopedi bilginlerindendir. "
                           "Keşfü'z-Zünûn eserinde 15.000'den fazla kitabı ve 10.000'e yakın "
                           'yazarı tanıtmıştır.',
                  'donem': '1609 – 1657 (İstanbul)',
                  'eserler': "Cihannümâ, Keşfü'z-Zünûn"},
 'matrakci_nasuh': {'ad': 'Matrakçı Nasuh',
                    'alan': 'Matematik, Minyatür, Haritacılık, Tarih',
                    'anahtar_kelimeler': ['matrakçı nasuh', 'matrakci nasuh', 'beyanı menazil'],
                    'bilgi': 'Kanuni döneminin çok yönlü matematikçisi, tarihçisi ve minyatür '
                             'sanatçısıdır. Şehirleri kuşbakışı üç boyutlu topografik haritalarla '
                             'resmetmiştir.',
                    'donem': '1480 – 1564 (Bosna – İstanbul)',
                    'eserler': "Beyân-ı Menâzil, Cemâlü'l-Küttâb"},
 'mimar_sinan': {'ad': "Mimar Sinan (Koca Mi'mâr Sinân Âğâ)",
                 'alan': 'Mimari, İnşaat Mühendisliği, Akustik',
                 'anahtar_kelimeler': ['mimar sinan', 'sinan', 'süleymaniye', 'selimiye'],
                 'bilgi': "Osmanlı İmparatorluğu'nun en parlak döneminde (Kanuni Sultan Süleyman, "
                          "II. Selim ve III. Murad) yaklaşık 50 yıl boyunca 'Hassa Başmimarı' "
                          'olarak görev yapmış, dünya mimarlık tarihinin en büyük dahilerinden '
                          "biridir. Kayseri'nin Ağırnas köyünde doğmuş, Yavuz Sultan Selim "
                          "döneminde devşirme olarak İstanbul'a gelmiş ve Yeniçeri Ocağı'nda "
                          'askeri mühendislik (köprü, kale, su kemeri yapımı) konusunda '
                          'uzmanlaşmıştır.\n'
                          '\n'
                          '**🏛️ Üç Büyük Başyapıtı:**\n'
                          '• **Çıraklık Eseri:** Şehzade Camii (İstanbul, 1548)\n'
                          '• **Kalfalık Eseri:** Süleymaniye Camii ve Külliyesi (İstanbul, 1557)\n'
                          '• **Ustalık Eseri:** Selimiye Camii (Edirne, 1575 — tek kubbede '
                          'ulaşılabilen en kusursuz mekân bütünlüğü)\n'
                          '\n'
                          "**⚙️ Mühendislik ve Bilim Dehası:** Yaklaşık 99 yıllık ömrüne **375'ten "
                          'fazla eser** (81 cami, 51 mescit, 55 medrese, 35 saray, 20 kervansaray, '
                          "8 köprü, 7 su kemeri) sığdırmıştır. Süleymaniye'de temel oturması için "
                          'yıllarca bekleyip devekuşu yumurtalı harç ve kurşun kenetli sismik '
                          'yalıtım kullanmış; kubbe içlerine yerleştirdiği **boş ses küpleri '
                          '(rezonatörler)** ile mikrofonsuz kusursuz akustik ve is odasıyla doğal '
                          'hava sirkülasyonu kurmuştur.',
                 'donem': '1489 – 1588 (Kayseri – İstanbul)',
                 'eserler': 'Şehzade, Süleymaniye ve Selimiye Camileri'},
 'nasiruddin_tusi': {'ad': 'Nasîrüddîn-i Tûsî',
                     'alan': 'Astronomi, Trigonometri, Mantık',
                     'anahtar_kelimeler': ['nasirüddin tusi', 'tusi', 'meraga rasathanesi'],
                     'bilgi': "Merâga Rasathanesi'ni kurmuş, trigonometriyi astronomiden bağımsız "
                              "bir matematik dalı haline getirmiş ve 'Tûsî Çifti' teoremini "
                              'geliştirmiştir.',
                     'donem': '1201 – 1274 (Tûs – Merâga)',
                     'eserler': "Zîc-i İlhânî, Şeklü'l-Kattâ"},
 'omer_hayyam': {'ad': "Ömer Hayyâm (Gıyâseddin Ebü'l-Feth)",
                 'alan': 'Matematik, Cebir, Astronomi, Edebiyat',
                 'anahtar_kelimeler': ['ömer hayyam', 'omer hayyam', 'hayyam', 'celali takvimi'],
                 'bilgi': 'Kübik denklemleri geometrik yöntemlerle çözen büyük matematikçidir. '
                          "Binom açılımını kullanmış ve Celâlî Takvimi'ni hazırlamıştır.",
                 'donem': '1048 – 1131 (Nişabur)',
                 'eserler': 'Cebir Risalesi, Rubâiyyât'},
 'piri_reis': {'ad': 'Pîrî Reis (Hacı Ahmed Muhiddin Pîrî)',
               'alan': 'Denizcilik, Haritacılık, Coğrafya',
               'anahtar_kelimeler': ['piri reis', 'pîrî reis', 'kitab-ı bahriye', 'dünya haritası'],
               'bilgi': '1513 yılında çizdiği Dünya Haritası Amerika kıyılarını dönemin en yüksek '
                        'doğruluğuyla gösterir. Kitâb-ı Bahriye eşsiz bir denizcilik kılavuzudur.',
               'donem': '1465 – 1553 (Gelibolu / Osmanlı)',
               'eserler': 'Kitâb-ı Bahriye, 1513 Dünya Haritası'},
 'sabitu_bin_kurra': {'ad': 'Sâbit bin Kurra',
                      'alan': 'Matematik, Astronomi, Mekanik',
                      'anahtar_kelimeler': ['sabit bin kurra', 'harran'],
                      'bilgi': 'Dost sayılar teoremini bulan, diferansiyel ve integral hesabın '
                               'öncü adımlarını atan Harranlı büyük matematikçi ve astronomdur.',
                      'donem': '836 – 901 (Harran – Bağdat)',
                      'eserler': "Kitâbü'l-Karastûn"},
 'takiyuddin': {'ad': 'Takîyüddîn er-Râsıd',
                'alan': 'Astronomi, Optik, Mekanik Saatler',
                'anahtar_kelimeler': ['takiyüddin', 'takiyuddin', 'istanbul rasathanesi'],
                'bilgi': "İstanbul Rasathanesi'nin kurucusudur. Saniyeyi gösteren mekanik saatler "
                         'yapmış ve buhar gücüyle dönen düzenekler tasarlamıştır.',
                'donem': '1526 – 1585 (Şam – İstanbul)',
                'eserler': "Sidretü'l-Müntehâ, Et-Turuku's-Seniyye"},
 'ulug_bey': {'ad': 'Uluğ Bey (Muhammed Taragay)',
              'alan': 'Astronomi, Trigonometri',
              'anahtar_kelimeler': ['uluğ bey', 'ulug bey', 'semerkant rasathanesi'],
              'bilgi': "Semerkant'ta kurduğu dev rasathanede 1000'den fazla yıldızın konumunu "
                       'ölçmüş ve bir yılın süresini saniyeler mertebesinde yakın hesaplamıştır.',
              'donem': '1394 – 1449 (Semerkant)',
              'eserler': 'Zîc-i Uluğ Bey'},
 'zehrawi': {'ad': "ez-Zehrâvî (Ebü'l-Kâsım)",
             'alan': 'Cerrahi, Tıp, Biyomedikal Aletler',
             'anahtar_kelimeler': ['zehravi', 'ez-zehravi', 'cerrahi kurucusu', 'tasrif'],
             'bilgi': "Modern cerrahinin babası kabul edilir. 200'den fazla cerrahi aleti "
                      '(bistüri, pens, koter) çizimleriyle tanıtmış ve ameliyat dikişinde katgüt '
                      'kullanmıştır.',
             'donem': '936 – 1013 (Endülüs / Kurtuba)',
             'eserler': "Kitâbü't-Tasrîf"}}

def islam_alimleri_studyosu_goster(sesli_soyle_fn):
    st.subheader(f"📜 İslam Bilim ve Düşünce Tarihine Yön Veren {len(ISLAM_ALIMLERI)} Büyük Âlim")
    arama = st.text_input(
        "Âlim, Eser veya Bilim Dalı Ara:",
        placeholder="Örn: Cezeri, Harezmi, İbn-i Sina, Optik, Cerrahi, Buhara...",
    ).lower().strip()
    col_a1, col_a2 = st.columns(2, gap="medium")
    for idx, (kod, bilgi) in enumerate(ISLAM_ALIMLERI.items()):
        birlesik = f"{bilgi['ad']} {bilgi['alan']} {bilgi['eserler']} {bilgi['bilgi']}".lower()
        if arama and arama not in birlesik:
            continue
        with (col_a1 if idx % 2 == 0 else col_a2):
            st.markdown(
                bilgi_karti_olustur(
                    f"📜 {bilgi['ad']}",
                    f"🕰️ {bilgi['donem']} | 🔬 {bilgi['alan']}",
                    f"<strong>Başlıca Eserleri:</strong> {bilgi['eserler']}<br><br>{bilgi['bilgi']}",
                ),
                unsafe_allow_html=True,
            )
            if st.button(f"🔊 {bilgi['ad'].split('(')[0].strip()} Biyografisini Dinle", key=f"dinle_{kod}"):
                sesli_soyle_fn(bilgi["bilgi"], dil="tr")


# ==============================================================================
# v10.0: KESİN TÜRKİYE SAATİ (UTC+3) VE CANLI ZAMAN / POMODORO / SAYAÇ MERKEZİ
# ==============================================================================
from datetime import datetime as _dt, timedelta as _td, timezone as _tz
import streamlit.components.v1 as _st_components

try:
    from zoneinfo import ZoneInfo as _ZoneInfo
    _TR_TZ = _ZoneInfo("Europe/Istanbul")
except Exception:
    _TR_TZ = _tz(_td(hours=3))


def turkiye_saati_al() -> _dt:
    """Bulut sunucusu UTC olsa bile her zaman kesin İstanbul / Türkiye saatini (UTC+3) döndürür."""
    return _dt.now(_TR_TZ)


def zaman_ve_sayac_studyosu_goster():
    """
    Canlı akan Türkiye Dijital Saati (JS 1 sn tazeleme), Pomodoro Çalışma Sayacı,
    Özel Geri Sayım ve Kronometre Stüdyosu (sayfa yenilemeden canlı akar!).
    """
    simdi_tr = turkiye_saati_al()
    st.subheader("⏰ Canlı Türkiye Saati, Pomodoro & Akıllı Sayaç Merkezi")
    st.caption(f"🇹🇷 Sunucu konumu fark etmeksizin kesin İstanbul / Türkiye Saati (UTC+3) • Açılış: `{simdi_tr.strftime('%d.%m.%Y %H:%M:%S')}`")

    canli_html = """
    <div style="font-family: 'Segoe UI', system-ui, sans-serif; color: #f8fafc; background: linear-gradient(135deg, #0b1630, #111f3f); border: 1px solid rgba(56,189,248,0.35); border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 10px 28px rgba(0,0,0,0.35);">
      <div style="font-size: 0.9rem; letter-spacing: 1.5px; color: #38bdf8; text-transform: uppercase; font-weight: 700;">🇹🇷 CANLI TÜRKİYE SAATİ (İSTANBUL • UTC+3)</div>
      <div id="ar_clock" style="font-size: 3.1rem; font-weight: 800; margin: 6px 0; font-variant-numeric: tabular-nums; color: #ffffff;">--:--:--</div>
      <div id="ar_date" style="font-size: 1rem; color: #cbd5e1; margin-bottom: 18px;">Yükleniyor...</div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; text-align: left;">
        <!-- POMODORO & GERİ SAYIM -->
        <div style="background: rgba(15,23,42,0.75); border: 1px solid rgba(148,163,184,0.22); border-radius: 12px; padding: 14px;">
          <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">🍅 Pomodoro & Geri Sayım</div>
          <div id="ar_cd_disp" style="font-size: 2.1rem; font-weight: 800; font-variant-numeric: tabular-nums; text-align:center; margin: 8px 0;">25:00</div>
          <div style="display:flex; gap:6px; flex-wrap:wrap; justify-content:center; margin-bottom:8px;">
            <button onclick="setCD(25)" style="background:#1e293b;color:#e2e8f0;border:1px solid #38bdf8;border-radius:8px;padding:4px 9px;cursor:pointer;">25 dk Ders</button>
            <button onclick="setCD(5)" style="background:#1e293b;color:#e2e8f0;border:1px solid #34d399;border-radius:8px;padding:4px 9px;cursor:pointer;">5 dk Mola</button>
            <button onclick="setCD(45)" style="background:#1e293b;color:#e2e8f0;border:1px solid #a78bfa;border-radius:8px;padding:4px 9px;cursor:pointer;">45 dk Etüt</button>
          </div>
          <div style="display:flex; gap:6px; justify-content:center;">
            <button onclick="startCD()" style="background:#0284c7;color:white;border:none;border-radius:8px;padding:6px 14px;font-weight:700;cursor:pointer;">▶ Başlat</button>
            <button onclick="pauseCD()" style="background:#475569;color:white;border:none;border-radius:8px;padding:6px 12px;cursor:pointer;">⏸ Durdur</button>
            <button onclick="resetCD()" style="background:#334155;color:white;border:none;border-radius:8px;padding:6px 12px;cursor:pointer;">↺ Sıfırla</button>
          </div>
          <div id="ar_cd_msg" style="font-size:0.82rem; color:#34d399; text-align:center; margin-top:6px;"></div>
        </div>

        <!-- KRONOMETRE -->
        <div style="background: rgba(15,23,42,0.75); border: 1px solid rgba(148,163,184,0.22); border-radius: 12px; padding: 14px;">
          <div style="font-weight: 700; color: #a78bfa; margin-bottom: 6px;">⏱️ Hassas Kronometre</div>
          <div id="ar_sw_disp" style="font-size: 2.1rem; font-weight: 800; font-variant-numeric: tabular-nums; text-align:center; margin: 8px 0;">00:00.0</div>
          <div style="display:flex; gap:6px; justify-content:center; margin-top: 22px;">
            <button onclick="startSW()" style="background:#7c3aed;color:white;border:none;border-radius:8px;padding:6px 14px;font-weight:700;cursor:pointer;">▶ Başlat</button>
            <button onclick="pauseSW()" style="background:#475569;color:white;border:none;border-radius:8px;padding:6px 12px;cursor:pointer;">⏸ Durdur</button>
            <button onclick="resetSW()" style="background:#334155;color:white;border:none;border-radius:8px;padding:6px 12px;cursor:pointer;">↺ Sıfırla</button>
          </div>
        </div>
      </div>
    </div>
    <script>
      function tickClock() {
        const now = new Date();
        const trTime = now.toLocaleTimeString('tr-TR', { timeZone: 'Europe/Istanbul', hour12: false });
        const trDate = now.toLocaleDateString('tr-TR', { timeZone: 'Europe/Istanbul', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        document.getElementById('ar_clock').textContent = trTime;
        document.getElementById('ar_date').textContent = trDate;
      }
      tickClock();
      setInterval(tickClock, 1000);

      let cdBase = 1500, cdSec = 1500, cdInt = null;
      function renderCD() {
        const m = String(Math.floor(cdSec / 60)).padStart(2, '0');
        const s = String(cdSec % 60).padStart(2, '0');
        document.getElementById('ar_cd_disp').textContent = m + ':' + s;
      }
      function setCD(mins) { pauseCD(); cdBase = mins * 60; cdSec = cdBase; document.getElementById('ar_cd_msg').textContent = ''; renderCD(); }
      function startCD() {
        if (cdInt) return;
        cdInt = setInterval(() => {
          if (cdSec > 0) { cdSec--; renderCD(); }
          else { pauseCD(); document.getElementById('ar_cd_msg').textContent = '🔔 Süre doldu! Harika çalıştın!'; }
        }, 1000);
      }
      function pauseCD() { if (cdInt) { clearInterval(cdInt); cdInt = null; } }
      function resetCD() { pauseCD(); cdSec = cdBase; document.getElementById('ar_cd_msg').textContent = ''; renderCD(); }

      let swDs = 0, swInt = null;
      function renderSW() {
        const m = String(Math.floor(swDs / 600)).padStart(2, '0');
        const s = String(Math.floor((swDs % 600) / 10)).padStart(2, '0');
        const d = String(swDs % 10);
        document.getElementById('ar_sw_disp').textContent = m + ':' + s + '.' + d;
      }
      function startSW() { if (!swInt) swInt = setInterval(() => { swDs++; renderSW(); }, 100); }
      function pauseSW() { if (swInt) { clearInterval(swInt); swInt = null; } }
      function resetSW() { pauseSW(); swDs = 0; renderSW(); }
    </script>
    """
    _st_components.html(canli_html, height=340, scrolling=False)
