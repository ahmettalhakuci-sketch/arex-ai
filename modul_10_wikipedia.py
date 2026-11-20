# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v4.5 — MODÜL 10: DOĞRUDAN SOHBET ENTEGRELİ KAPSAMLI WIKIPEDIA MOTORU
Sohbet Botundan Otomatik "Araştırılıyor, Wikipedia'ya gidiliyor..." Akışı,
Türkçe (tr.wikipedia.org) & İngilizce (en.wikipedia.org) Canlı Arama,
Cümle Bozukluklarını Temizleme ve Geniş Yerleşik Ansiklopedi (modul_10_wikipedia.py)
==============================================================================
"""
import importlib.util
import json
import time
import os
import re
import sys
import urllib.parse
import urllib.request
import streamlit as st

_MODUL_DIZINI = os.path.dirname(os.path.abspath(__file__))
if _MODUL_DIZINI not in sys.path:
    sys.path.insert(0, _MODUL_DIZINI)


def _guvenli_modul_yukle(modul_adi: str):
    if modul_adi in sys.modules and getattr(sys.modules[modul_adi], "__file__", None):
        return sys.modules[modul_adi]
    yol = os.path.join(_MODUL_DIZINI, f"{modul_adi}.py")
    if os.path.exists(yol):
        spec = importlib.util.spec_from_file_location(modul_adi, yol)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[modul_adi] = mod
            spec.loader.exec_module(mod)
            return mod
    return __import__(modul_adi)


_m1 = _guvenli_modul_yukle("modul_1_arayuz_ve_tema")
_m5 = _guvenli_modul_yukle("modul_5_dil_ve_cevirmeli_kartlar")
bilgi_karti_olustur = _m1.bilgi_karti_olustur
guvenli_cevir = _m5.guvenli_cevir

# Genişletilmiş Yerleşik Yedek Wikipedia Ansiklopedisi (İnternet yavaşsa/kesikse bile sıfır cümle bozukluğuyla anında yanıt verir)
YEDEK_WIKIPEDIA_MADDELERI = {
    "roma imparatorluğu": {
        "baslik": "Roma İmparatorluğu",
        "url": "https://tr.wikipedia.org/wiki/Roma_%C4%B0mparatorlu%C4%9Fu",
        "gorsel": "",
        "bolumler": ["Kuruluş ve Pax Romana", "Hukuk ve Mühendislik Mirası", "Bölünme ve Çöküş"],
        "ozet": (
            "Roma İmparatorluğu (MÖ 27 – MS 476 Batı; MS 1453 Doğu/Bizans), Akdeniz havzasının tamamını, "
            "Batı Avrupa'yı, Balkanlar'ı, Anadolu'yu, Mezopotamya'nın bir bölümünü ve Kuzey Afrika'yı kapsayan "
            "Antik Çağ'ın en etkili medeniyetlerinden biridir. Augustus'un MÖ 27'de imparator ilan edilmesiyle "
            "Cumhuriyet döneminden İmparatorluk dönemine geçilmiştir.\n\n"
            "### 📌 Kuruluş ve Pax Romana (Roma Barışı)\n"
            "MÖ 27 ile MS 180 yılları arasındaki yaklaşık iki yüzyıllık dönem 'Pax Romana' olarak bilinir. "
            "Bu süreçte imparatorluk sınırları İskoçya'dan Fırat Nehri'ne kadar genişlemiş; ticaret yolları, "
            "ortak para birimi ve düzenli posta ağı sayesinde ekonomik refah zirveye ulaşmıştır.\n\n"
            "### 📌 Hukuk, Mimari ve Mühendislik Mirası\n"
            "Modern Avrupa hukukunun temeli olan Roma Hukuku (On İki Levha Kanunları ve Corpus Juris Civilis) "
            "bu dönemde şekillenmiştir. Mühendislikte ise su kemerleri (akuadükler), beton kubbe tekniği (Pantheon), "
            "amfitiyatrolar (Kolezyum) ve 80.000 kilometreyi aşan taş döşeli yol ağı geliştirilmiştir.\n\n"
            "### 📌 Bölünme ve Çöküş\n"
            "MS 395'te imparatorluk Batı ve Doğu Roma olarak ikiye ayrıldı. Batı Roma 476'da Kavimler Göçü ve "
            "iç krizler sonucu yıkılırken, Doğu Roma (Bizans) başkenti Konstantinopolis (İstanbul) ile "
            "29 Mayıs 1453'te Fatih Sultan Mehmet'in fethine kadar yaklaşık bin yıl daha varlığını sürdürdü."
        ),
    },
    "islam altın çağı": {
        "baslik": "İslam Altın Çağı",
        "url": "https://tr.wikipedia.org/wiki/%C4%B0slam_Alt%C4%B1n_%C3%87a%C4%9F%C4%B1",
        "gorsel": "",
        "bolumler": ["Beytülhikme ve Tercüme Hareketi", "Bilim, Tıp ve Mühendislik Atılımları", "Dünya Tarihine Etkisi"],
        "ozet": (
            "İslam Altın Çağı (yaklaşık 8. yüzyıl – 13. yüzyıl), Abbasi Halifeliği döneminde Bağdat merkezli "
            "başlayıp Kurtuba (Endülüs), Kahire, Şam, Semerkant ve Buhara'ya yayılan; bilim, felsefe, tıp, "
            "astronomi, matematik ve mühendislikte dünya tarihine yön veren büyük yükseliş dönemidir.\n\n"
            "### 📌 Beytülhikme ve Tercüme Hareketi\n"
            "Halife Harun Reşid ve Memûn döneminde Bağdat'ta kurulan Beytülhikme (Bilgelik Evi), Antik Yunan, "
            "Hint ve Fars eserlerinin Arapçaya çevrildiği, ardından deneysel yöntemlerle geliştirildiği "
            "dev bir araştırma akademisine dönüştü.\n\n"
            "### 📌 Bilim, Tıp ve Mühendislik Atılımları\n"
            "El-Hârizmî cebiri bağımsız bir bilim dalı hâline getirdi ve 'algoritma' kavramına adını verdi. "
            "İbnü'l-Heysem modern optiğin ve deneysel bilimsel yöntemin temellerini attı. İbn-i Sînâ'nın "
            "'El-Kanun fi't-Tıb' eseri Avrupa üniversitelerinde 600 yıl ders kitabı olarak okutuldu. "
            "El-Cezerî ise 1206'da Artuklu sarayında krank mili, kam mekanizması ve programlanabilir otomatlarla "
            "sibernetiğin ve robotiğin öncüsü oldu.\n\n"
            "### 📌 Dünya Tarihine Etkisi\n"
            "Endülüs (Toledo ve Kurtuba) ile Sicilya üzerinden Latinceye çevrilen bu eserler, Avrupa'da "
            "Rönesans'ın ve modern bilimsel devrimin doğrudan ateşleyicisi olmuştur."
        ),
    },
    "büyük selçuklu devleti": {
        "baslik": "Büyük Selçuklu Devleti",
        "url": "https://tr.wikipedia.org/wiki/B%C3%BCy%C3%BCk_Sel%C3%A7uklu_%C4%B0mparatorlu%C4%9Fu",
        "gorsel": "",
        "bolumler": ["Kuruluş ve Malazgirt Zaferi", "Nizamiye Medreseleri ve Bilim", "Devlet Teşkilatı"],
        "ozet": (
            "Büyük Selçuklu Devleti (1037–1157), Oğuz Türklerinin Kınık boyu tarafından Tuğrul ve Çağrı Beyler "
            "liderliğinde kurulan; Orta Asya'dan Anadolu ve Akdeniz kıyılarına kadar uzanan büyük Türk-İslam imparatorluğudur.\n\n"
            "### 📌 Kuruluş ve Malazgirt Zaferi (1071)\n"
            "1040 Dandanakan Savaşı ile Horasan'da bağımsızlığını pekiştiren Selçuklular, Sultan Alparslan "
            "komutasındaki 26 Ağustos 1071 Malazgirt Meydan Muharebesi ile Bizans ordusunu yenerek Anadolu'nun "
            "kapılarını Türklere kalıcı olarak açtı.\n\n"
            "### 📌 Nizamiye Medreseleri, Kültür ve Bilim\n"
            "Sultan Melikşah ve büyük vezir Nizamülmülk döneminde Bağdat, Nişabur ve İsfahan'da kurulan "
            "Nizamiye Medreseleri dünyanın ilk kurumsal üniversite modellerinden biri kabul edilir. "
            "İmam Gazâlî bu medreselerde başmüderrislik yapmış, Ömer Hayyam ise Celâlî Takvimi'ni hazırlamıştır.\n\n"
            "### 📌 Devlet Teşkilatı ve Mirası\n"
            "İkta sistemi (tarım ve askerî finansman modeli), atabeylik kurumu ve kervansaray ağı daha sonra "
            "Anadolu Selçuklu ve Osmanlı devlet teşkilatının temelini oluşturmuştur."
        ),
    },
    "sanayi devrimi": {
        "baslik": "Sanayi Devrimi",
        "url": "https://tr.wikipedia.org/wiki/Sanayi_Devrimi",
        "gorsel": "",
        "bolumler": ["1. Sanayi Devrimi ve Buhar Gücü", "Toplumsal ve Ekonomik Dönüşüm", "Endüstri 2.0'dan 4.0'a"],
        "ozet": (
            "Sanayi Devrimi, 18. yüzyılın ikinci yarısında (yaklaşık 1760'larda) İngiltere'de başlayıp "
            "Avrupa ve dünyaya yayılan; el emeğine dayalı tarım ve atölye üretiminden makineleşmiş fabrika "
            "üretimine geçişi ifade eden köklü tarihsel dönüşümdür.\n\n"
            "### 📌 1. Sanayi Devrimi ve Buhar Gücü\n"
            "James Watt'ın buhar makinesini verimli hâle getirmesi, dokuma tezgâhlarının (Spinning Jenny) "
            "makineleşmesi ve kömür-demir üretiminin artmasıyla fabrikalar, buharlı gemiler ve demiryolları doğdu.\n\n"
            "### 📌 Toplumsal ve Ekonomik Dönüşüm\n"
            "Kırsaldan kentlere büyük göç yaşandı, modern işçi sınıfı ve sendikacılık ortaya çıktı; üretim "
            "maliyetleri düşerken hammadde ve pazar rekabeti küresel siyaseti ve sömürgeciliği hızlandırdı.\n\n"
            "### 📌 Endüstri 2.0'dan 4.0'a\n"
            "19. yüzyıl sonunda elektrik ve seri üretim bandı (Endüstri 2.0), 20. yüzyılda bilgisayar ve "
            "otomasyon (Endüstri 3.0), günümüzde ise yapay zeka, otonom robotik ve nesnelerin interneti "
            "(Endüstri 4.0) bu büyük dönüşümün devamı olarak dünyayı şekillendirmektedir."
        ),
    },
    "rönesans": {
        "baslik": "Rönesans",
        "url": "https://tr.wikipedia.org/wiki/R%C3%B6nesans",
        "gorsel": "",
        "bolumler": ["İtalya'da Doğuşu", "Sanat, Bilim ve Hümanizm", "Dünya Tarihine Etkileri"],
        "ozet": (
            "Rönesans (Fransızca 'yeniden doğuş'), 14. yüzyılda İtalya'nın Floransa, Venedik ve Roma gibi "
            "ticaret şehirlerinde başlayıp 16. yüzyıla kadar Avrupa'ya yayılan kültür, sanat, bilim ve düşünce hareketidir.\n\n"
            "### 📌 Doğuş Sebepleri\n"
            "Akdeniz ticaretiyle zenginleşen İtalyan şehir devletleri (özellikle Medici ailesi gibi sanat koruyucuları), "
            "1453'te İstanbul'un fethinden sonra İtalya'ya giden bilginler, İslam dünyasından çevrilen bilimsel "
            "eserler ve Gutenberg'in hareketli matbaayı (1450) icadı Rönesans'ı hızlandırdı.\n\n"
            "### 📌 Sanat, Bilim ve Hümanizm\n"
            "Leonardo da Vinci, Michelangelo, Rafael ve Donatello sanatta perspektif ve anatomiyi zirveye taşıdı. "
            "Bilimde Kopernik güneş merkezli evren modelini, Galileo teleskopla gözlemsel astronomiyi geliştirdi.\n\n"
            "### 📌 Dünya Tarihine Etkileri\n"
            "Skolastik düşüncenin yerini akıl, gözlem ve eleştirel düşünce aldı; bu süreç Reform hareketine, "
            "Coğrafi Keşifler'e ve modern bilimsel yöntemin doğuşuna zemin hazırladı."
        ),
    },
    "ikinci dünya savaşı": {
        "baslik": "II. Dünya Savaşı",
        "url": "https://tr.wikipedia.org/wiki/II._D%C3%BCnya_Sava%C5%9F%C4%B1",
        "gorsel": "",
        "bolumler": ["Nedenleri ve Başlangıcı", "Kritik Cepheler ve Dönüm Noktaları", "Sonuçları ve Yeni Dünya Düzeni"],
        "ozet": (
            "II. Dünya Savaşı (1 Eylül 1939 – 2 Eylül 1945), Müttefik Devletler (ABD, SSCB, Birleşik Krallık, "
            "Fransa, Çin) ile Mihver Devletleri (Nazi Almanyası, İtalya, Japonya) arasında gerçekleşen ve "
            "insanlık tarihinin en yıkıcı küresel savaşıdır.\n\n"
            "### 📌 Nedenleri ve Başlangıcı\n"
            "I. Dünya Savaşı sonrası imzalanan ağır Versay Antlaşması, 1929 Büyük Buhranı ve totaliter "
            "rejimlerin yayılmacı politikaları gerilimi tırmandırdı. Almanya'nın 1 Eylül 1939'da Polonya'yı "
            "işgaliyle savaş resmen başladı.\n\n"
            "### 📌 Dönüm Noktaları\n"
            "1941'de Almanya'nın SSCB'ye saldırması (Barbarossa Harekâtı) ve Japonya'nın Pearl Harbor baskını "
            "savaşı tüm kıtalara yaydı. Stalingrad Muharebesi (1942-1943), Midway Deniz Savaşı ve 6 Haziran 1944 "
            "Normandiya Çıkarması savaşın kaderini Müttefikler lehine çevirdi. Ağustos 1945'te Hiroşima ve "
            "Nagazaki'ye atom bombası atılmasıyla Japonya teslim oldu.\n\n"
            "### 📌 Sonuçları ve Türkiye'nin Denge Politikası\n"
            "Yaklaşık 70-85 milyon insan hayatını kaybetti. Birleşmiş Milletler kuruldu, Avrupa ikiye bölündü "
            "ve ABD ile SSCB arasında Soğuk Savaş başladı. Türkiye ise aktif tarafsızlık ve denge politikasıyla "
            "savaşın yıkımından korunmayı başardı."
        ),
    },
    "ipek yolu": {
        "baslik": "İpek Yolu",
        "url": "https://tr.wikipedia.org/wiki/%C4%B0pek_Yolu",
        "gorsel": "",
        "bolumler": ["Güzergâh ve Ticaret Malları", "Kültürel ve Bilimsel Etkileşim", "Tarihsel Önemi"],
        "ozet": (
            "İpek Yolu, MÖ 2. yüzyıldan 15. yüzyıla kadar Çin'in Chang'an (Xi'an) şehrinden başlayıp Orta Asya, "
            "İran, Mezopotamya ve Anadolu üzerinden Akdeniz'e ve Avrupa'ya uzanan tarihin en önemli kara ve deniz "
            "ticaret ağlarının ortak adıdır.\n\n"
            "### 📌 Güzergâh ve Ticaret Malları\n"
            "Yalnızca Çin ipeği değil; baharat, porselen, kâğıt, barut, pusula, cam, değerli taşlar, halı ve "
            "atlar bu güzergâhta taşınmıştır. Semerkant, Buhara, Merv, Tebriz, Mardin, Diyarbakır, Konya, "
            "Bursa ve İstanbul yolun kilit kavşakları olmuştur.\n\n"
            "### 📌 Kültürel ve Bilimsel Etkileşim\n"
            "İpek Yolu sadece mal değil; bilim, matematik, tıp, mimari, din ve sanat alışverişini de sağladı. "
            "Kâğıt ve matbaanın Çin'den İslam dünyasına, oradan Avrupa'ya ulaşması bu yol sayesinde gerçekleşti.\n\n"
            "### 📌 Tarihsel Önemi\n"
            "15. yüzyıl sonunda Coğrafi Keşifler ile okyanus ticaret yollarının açılması İpek Yolu'nun ağırlığını "
            "azaltsa da günümüzde 'Kuşak ve Yol' gibi modern lojistik koridorlarıyla stratejik önemi yeniden gündemdedir."
        ),
    },

    "göktürk kağanlığı": {
        "baslik": "Göktürk Kağanlığı (Köktürkler)",
        "url": "https://tr.wikipedia.org/wiki/G%C3%B6kt%C3%BCrk_Ka%C4%9Fanl%C4%B1%C4%9F%C4%B1",
        "gorsel": "",
        "bolumler": ["Kuruluş ve Türk Adının İlk Resmî Kullanımı", "Orhun Yazıtları ve Alfabe", "Devlet Teşkilatı ve Mirası"],
        "ozet": (
            "Göktürk Kağanlığı (552–744), tarihte 'Türk' adını resmî devlet adı olarak kullanan ilk büyük "
            "devlettir. Bumin Kağan'ın 552'de Avar egemenliğine son verip Ötüken'i başkent yapmasıyla kuruldu; "
            "kardeşi İstemi Yabgu batı kanadını yöneterek sınırları Hazar'dan Karadeniz'in kuzeyine kadar genişletti.\n\n"
            "### 📌 İkinci Göktürk Devleti ve Orhun Yazıtları\n"
            "682'de Kutluk (İlteriş) Kağan tarafından yeniden kurulan İkinci Göktürk Kağanlığı döneminde "
            "Bilge Kağan, Kültigin ve Vezir Tonyukuk adına dikilen Orhun Yazıtları (720–735), Türk dilinin "
            "ve devlet felsefesinin günümüze ulaşan en eski yazılı anıtlarıdır.\n\n"
            "### 📌 Devlet Felsefesi ve Mirası\n"
            "Töre (yazısız hukuk), ikili teşkilat (doğu-batı yönetimi) ve sosyal devlet anlayışı ('aç milleti "
            "doyurdum, çıplak milleti giydirdim') sonraki tüm Türk devletlerinin temel yönetim geleneğini belirledi."
        ),
    },
    "anadolu selçuklu devleti": {
        "baslik": "Anadolu Selçuklu Devleti (Türkiye Selçukluları)",
        "url": "https://tr.wikipedia.org/wiki/Anadolu_Sel%C3%A7uklu_Devleti",
        "gorsel": "",
        "bolumler": ["Kuruluş ve Başkentler", "Ticaret, Kervansaraylar ve Mimari", "Bilim, Tasavvuf ve Kültür"],
        "ozet": (
            "Anadolu Selçuklu Devleti (1075–1308), Süleyman Şah tarafından İznik merkezli kurulmuş, I. Haçlı "
            "Seferi sonrası başkentini Konya'ya taşıyarak Anadolu'yu kalıcı bir Türk yurduna dönüştürmüştür.\n\n"
            "### 📌 Yükseliş ve Kervansaray Ağı\n"
            "I. Gıyaseddin Keyhüsrev, I. İzzeddin Keykâvus ve I. Alâeddin Keykubad dönemlerinde Antalya, "
            "Alanya ve Sinop limanları fethedildi. Anadolu boyunca her 30–40 km'de bir inşa edilen kervansaraylar "
            "(Sultanhanı vb.) ve devlet sigortası sistemi sayesinde uluslararası ticaret altın çağını yaşadı.\n\n"
            "### 📌 Bilim, Mimari ve Tasavvuf\n"
            "Karatay ve İnce Minareli Medrese, Sivas Gök Medrese, Kayseri Gevher Nesibe Şifahanesi (ilk tıp "
            "medreselerinden biri) bu dönemde inşa edildi. Mevlânâ Celâleddîn-i Rûmî, Yunus Emre ve Hacı Bektaş-ı "
            "Velî Anadolu'nun manevi ve kültürel birliğini şekillendirdi."
        ),
    },
    "endülüs medeniyeti": {
        "baslik": "Endülüs Medeniyeti (İspanya'da İslam Medeniyeti)",
        "url": "https://tr.wikipedia.org/wiki/End%C3%BCl%C3%BCs",
        "gorsel": "",
        "bolumler": ["Kurtuba Halifeliği ve Bilim", "Elhamra Sarayı ve Mimari", "Avrupa'ya Bilimsel Aktarım"],
        "ozet": (
            "Endülüs (711–1492), Tarık bin Ziyad'ın Cebelitarık Boğazı'nı geçmesiyle İber Yarımadası'nda "
            "(günümüz İspanya ve Portekiz) kurulan ve yaklaşık 8 yüzyıl boyunca bilim, mimari, felsefe ve "
            "hoşgörünün Avrupa'daki merkezi olan büyük medeniyettir.\n\n"
            "### 📌 Kurtuba Kütüphaneleri ve Bilim İnsanları\n"
            "10. yüzyılda Kurtuba (Córdoba), 400.000'i aşkın cilt barındıran kütüphaneleri, sokak lambaları "
            "ve hastaneleriyle Avrupa'nın en gelişmiş şehriydi. Modern cerrahinin kurucusu Zehrâvî, büyük "
            "filozof ve hekim İbn Rüşd (Averroes), astronom Zerkâlî ve mucit Abbas İbn Firnas burada yetişti.\n\n"
            "### 📌 Mimari Şaheserler ve Rönesans'a Köprü\n"
            "Kurtuba Ulu Camii ve Gırnata'daki Elhamra Sarayı İslam mimarisinin zirvelerindendir. Toledo "
            "Tercüme Okulu üzerinden Latinceye aktarılan Endülüs eserleri, Avrupa'da üniversitelerin ve "
            "Rönesans'ın doğuşunda belirleyici rol oynadı."
        ),
    },
    "antik mısır": {
        "baslik": "Antik Mısır Medeniyeti",
        "url": "https://tr.wikipedia.org/wiki/Antik_M%C4%B1s%C4%B1r",
        "gorsel": "",
        "bolumler": ["Nil Nehri ve Krallık Dönemleri", "Piramitler, Hiyeroglif ve Bilim", "Tarihsel Mirası"],
        "ozet": (
            "Antik Mısır (yaklaşık MÖ 3100 – MÖ 30), Nil Nehri'nin bereketli taşkın ovasında doğup üç bin yıl "
            "boyunca kesintisiz varlık gösteren kadim bir uygarlıktır. Tarihçiler bu süreci Eski, Orta ve Yeni "
            "Krallık dönemlerine ayırır.\n\n"
            "### 📌 Mühendislik, Matematik ve Tıp\n"
            "Giza'daki Büyük Keops Piramidi (yaklaşık 2,3 milyon taş blok, MÖ 2560) antik dünyanın ayakta kalan "
            "tek harikasıdır. Mısırlılar Nil taşkınlarını hesaplamak için 365 günlük güneş takvimini, arazi "
            "ölçümü için geometriyi, mumyalama tecrübesiyle de anatomi ve cerrahiyi ileri düzeye taşıdı.\n\n"
            "### 📌 Yazı ve Papirüs\n"
            "Hiyeroglif yazı sistemi ve papirüs kâğıdı bilgi aktarımında devrim yarattı; 1799'da bulunan "
            "Rosetta Taşı sayesinde Jean-François Champollion 1822'de hiyeroglifleri çözmeyi başardı."
        ),
    },
    "mezopotamya": {
        "baslik": "Mezopotamya Uygarlıkları (Sümer, Akad, Babil, Asur)",
        "url": "https://tr.wikipedia.org/wiki/Mezopotamya",
        "gorsel": "",
        "bolumler": ["Sümerler ve Yazının İcadı", "Babil ve Hammurabi Kanunları", "Bilim ve Şehircilik Mirası"],
        "ozet": (
            "Mezopotamya (Yunanca 'iki nehir arası'), Dicle ve Fırat nehirleri arasındaki bereketli coğrafyada "
            "doğan ve 'medeniyetin beşiği' kabul edilen Sümer, Akad, Babil ve Asur uygarlıklarının merkezidir "
            "(Güneydoğu Anadolu'nun Mardin-Diyarbakır-Şanlıurfa hattı Yukarı Mezopotamya'nın kalbidir).\n\n"
            "### 📌 Sümerler ve İnsanlığın İlk İcatları\n"
            "Sümerler MÖ 3200 civarında çivi yazısını icat ederek tarih çağlarını başlattı. Tekerlek, saban, "
            "ziggurat adı verilen basamaklı tapınak-rasathaneler ve 60 tabanlı sayı sistemi (saatin 60 dakika, "
            "dairenin 360 derece olması) Sümerlerden günümüze kalmıştır.\n\n"
            "### 📌 Babil, Asur ve Hukuk\n"
            "Babil Kralı Hammurabi tarihin en kapsamlı erken yazılı kanunlarını hazırladı. Asurlular ise "
            "Ninova'da tarihin ilk sistemli devlet kütüphanesini (Asurbanipal Kütüphanesi) kurdu ve Anadolu'ya "
            "yazıyı (Kültepe tabletleri) taşıdı."
        ),
    },
    "çanakkale savaşı": {
        "baslik": "Çanakkale Savaşı (1915–1916)",
        "url": "https://tr.wikipedia.org/wiki/%C3%87anakkale_Sava%C5%9F%C4%B1",
        "gorsel": "",
        "bolumler": ["18 Mart Deniz Zaferi", "Gelibolu Kara Muharebeleri", "Dünya Tarihine Etkileri"],
        "ozet": (
            "Çanakkale Savaşı (1915–1916), I. Dünya Savaşı sırasında İtilaf Devletleri'nin İstanbul'u ele "
            "geçirip Osmanlı Devleti'ni savaş dışı bırakmak ve Rusya'ya yardım götürmek amacıyla başlattığı "
            "deniz ve kara harekâtına karşı Türk ordusunun kazandığı destansı zaferdir.\n\n"
            "### 📌 18 Mart 1915 Deniz Zaferi\n"
            "Nusret Mayın Gemisi'nin Erenköy Koyu'na döşediği mayınlar ve Seyit Onbaşı gibi kahraman topçuların "
            "isabetli atışlarıyla İtilaf donanmasının en güçlü zırhlıları (Bouvet, Irresistible, Ocean) batırıldı "
            "ve 'Çanakkale Geçilmez!' sözü tarihe kazındı.\n\n"
            "### 📌 Kara Muharebeleri ve Küresel Sonuçlar\n"
            "25 Nisan 1915'te başlayan Arıburnu, Conkbayırı ve Anafartalar muharebelerinde Yarbay Mustafa Kemal "
            "stratejik öngörüsüyle düşman ilerleyişini durdurdu. Zafer, I. Dünya Savaşı'nın süresini uzattı, "
            "Çarlık Rusyası'nın çöküşünü hızlandırdı ve Millî Mücadele'nin lider kadrosunu ortaya çıkardı."
        ),
    },
    "birinci dünya savaşı": {
        "baslik": "I. Dünya Savaşı (1914–1918)",
        "url": "https://tr.wikipedia.org/wiki/I._D%C3%BCnya_Sava%C5%9F%C4%B1",
        "gorsel": "",
        "bolumler": ["Nedenleri ve Bloklaşma", "Osmanlı Cepheleri", "Sonuçları ve Sınırların Değişimi"],
        "ozet": (
            "I. Dünya Savaşı (28 Temmuz 1914 – 11 Kasım 1918), sömürgecilik rekabeti, hammadde yarışı ve "
            "milliyetçilik akımlarının körüklediği; İtilaf Devletleri (İngiltere, Fransa, Rusya, sonradan İtalya "
            "ve ABD) ile İttifak Devletleri (Almanya, Avusturya-Macaristan, Osmanlı, Bulgaristan) arasında "
            "yaşanan ilk küresel topyekûn savaştır.\n\n"
            "### 📌 Osmanlı Cepheleri\n"
            "Osmanlı Devleti Kafkas, Kanal, Çanakkale, Irak (Kut'ül Amâre Zaferi), Hicaz-Yemen ve Suriye-Filistin "
            "cephelerinde savaştı. Çanakkale ve Kut'ül Amâre'de büyük zaferler kazanılsa da 1918'de Mondros "
            "Ateşkes Antlaşması imzalandı.\n\n"
            "### 📌 Sonuçları\n"
            "Osmanlı, Avusturya-Macaristan, Alman ve Rus imparatorlukları tarihe karıştı; yeni ulus devletler "
            "kuruldu. Tank, uçak ve denizaltı ilk kez geniş ölçekte kullanıldı. Ağır barış şartları ise "
            "21 yıl sonra II. Dünya Savaşı'na zemin hazırladı."
        ),
    },
    "coğrafi keşifler": {
        "baslik": "Coğrafi Keşifler (15. – 16. Yüzyıl)",
        "url": "https://tr.wikipedia.org/wiki/Co%C4%9Frafi_Ke%C5%9Fifler",
        "gorsel": "",
        "bolumler": ["Sebepleri ve Denizcilik Teknolojisi", "Büyük Keşifler", "Ekonomik ve Tarihsel Sonuçlar"],
        "ozet": (
            "Coğrafi Keşifler, 15. yüzyıl sonundan 16. yüzyıla kadar Portekizli ve İspanyol denizcilerin "
            "öncülüğünde yeni okyanus yollarının ve kıtaların keşfedilmesidir.\n\n"
            "### 📌 Başlıca Keşifler\n"
            "Bartolomeu Dias 1488'de Ümit Burnu'nu geçti, Kristof Kolomb 1492'de Amerika kıtasına ulaştı, "
            "Vasco da Gama 1498'de Afrika'yı dolaşarak Hindistan'a vardı. Macellan ve Elcano'nun 1519–1522 "
            "seferiyle dünyanın yuvarlak olduğu fiilen kanıtlandı.\n\n"
            "### 📌 Osmanlı ve Dünya Ekonomisine Etkisi\n"
            "Ticaretin ağırlık merkezi Akdeniz'den Atlas Okyanusu'na kaydı; İpek ve Baharat Yolları eski "
            "gelirini kaybetti. Amerika'dan taşınan altın ve gümüş Avrupa'da sermaye birikimini hızlandırırken "
            "Osmanlı ekonomisinde fiyat devrimi (enflasyon) baskısı oluşturdu."
        ),
    },
    "fransız ihtilali": {
        "baslik": "Fransız İhtilali (1789)",
        "url": "https://tr.wikipedia.org/wiki/Frans%C4%B1z_Devrimi",
        "gorsel": "",
        "bolumler": ["Nedenleri ve Bastille Baskını", "İnsan ve Yurttaş Hakları Bildirisi", "Dünyaya ve Osmanlı'ya Etkileri"],
        "ozet": (
            "Fransız İhtilali (1789–1799), Fransa'da mutlak monarşinin yıkılıp halk egemenliği, eşitlik, "
            "özgürlük ve adalet ilkelerinin yükseldiği, Yakın Çağ'ı başlatan büyük toplumsal ve siyasal devrimdir.\n\n"
            "### 📌 Dönüm Noktaları\n"
            "Ağır vergiler, kıtlık ve Aydınlanma düşünürlerinin (Montesquieu, Voltaire, Rousseau) fikirleriyle "
            "14 Temmuz 1789'da Bastille Hapishanesi basıldı. Ardından 'İnsan ve Yurttaş Hakları Bildirisi' "
            "ilan edilerek hukuk önünde eşitlik ve anayasal yönetim fikri dünyaya yayıldı.\n\n"
            "### 📌 Küresel Etkisi\n"
            "Milliyetçilik akımı çok uluslu imparatorlukları (Osmanlı ve Avusturya-Macaristan) derinden etkiledi; "
            "Osmanlı'da Tanzimat Fermanı (1839), Islahat Fermanı (1856) ve Meşrutiyet süreçlerini hızlandırdı."
        ),
    },
    "soğuk savaş": {
        "baslik": "Soğuk Savaş ve Uzay Yarışı (1947–1991)",
        "url": "https://tr.wikipedia.org/wiki/So%C4%9Fuk_Sava%C5%9F",
        "gorsel": "",
        "bolumler": ["İki Kutuplu Dünya (NATO & Varşova)", "Uzay Yarışı ve Teknoloji", "Berlin Duvarı ve Bitiş"],
        "ozet": (
            "Soğuk Savaş (1947–1991), II. Dünya Savaşı sonrası ABD liderliğindeki Batı Bloku (NATO) ile "
            "SSCB liderliğindeki Doğu Bloku (Varşova Paktı) arasında doğrudan sıcak çatışmaya dönüşmeden "
            "yürütülen siyasi, askerî, ekonomik ve teknolojik rekabet dönemidir.\n\n"
            "### 📌 Uzay Yarışı ve İnternetin Doğuşu\n"
            "SSCB 1957'de ilk yapay uydu Sputnik 1'i ve 1961'de ilk insan Yuri Gagarin'i uzaya gönderdi. "
            "ABD ise 20 Temmuz 1969'da Apollo 11 ile Neil Armstrong'u Ay'a indirdi. Aynı rekabet içinde "
            "geliştirilen ARPANET ağı, bugünkü modern internetin temelini attı.\n\n"
            "### 📌 Sona Ermesi\n"
            "9 Kasım 1989'da Berlin Duvarı'nın yıkılması ve 1991'de Sovyetler Birliği'nin dağılmasıyla "
            "Soğuk Savaş dönemi resmen sona erdi."
        ),
    },
    "kuantum fiziği": {
        "baslik": "Kuantum Fiziği (Kuantum Mekaniği)",
        "url": "https://tr.wikipedia.org/wiki/Kuantum_mekani%C4%9Fi",
        "gorsel": "",
        "bolumler": ["Klasik Fizikten Farkı", "Temel İlkeler (Süperpozisyon, Belirsizlik)", "Günlük Teknolojideki Yeri"],
        "ozet": (
            "Kuantum fiziği, atom ve atom altı parçacıklar (elektron, foton, kuark) ölçeğinde doğanın nasıl "
            "işlediğini açıklayan modern fizik kuramıdır. 1900'de Max Planck'ın enerjinin kesikli paketler "
            "(kuanta) hâlinde yayıldığını keşfetmesi ve Albert Einstein'ın fotoelektrik olayı açıklamasıyla doğdu.\n\n"
            "### 📌 Temel İlkeler\n"
            "• **Dalga-Parçacık İkiliği:** Elektron ve ışık hem dalga hem parçacık özelliği gösterir.\n"
            "• **Heisenberg Belirsizlik İlkesi:** Bir parçacığın konumu ve momentumu aynı anda kusursuz ölçülemez.\n"
            "• **Süperpozisyon ve Dolanıklık:** Bir kuantum sistemi ölçülmeden önce birden fazla durumda bulunabilir.\n\n"
            "### 📌 Günümüzdeki Kullanım Alanları\n"
            "Lazerler, yarı iletken transistörler (tüm bilgisayar ve telefon işlemcileri), MR (MRI) tıbbi "
            "görüntüleme cihazları, LED'ler ve yeni nesil kuantum bilgisayarlar tamamen kuantum fiziğine dayanır."
        ),
    },
    "güneş sistemi": {
        "baslik": "Güneş Sistemi ve Gezegenler",
        "url": "https://tr.wikipedia.org/wiki/G%C3%BCne%C5%9F_Sistemi",
        "gorsel": "",
        "bolumler": ["İç Kayalık Gezegenler", "Dış Gaz ve Buz Devleri", "Uzay Keşifleri"],
        "ozet": (
            "Güneş Sistemi, yaklaşık 4,6 milyar yıl önce dev bir gaz ve toz bulutunun kütleçekimiyle çökmesi "
            "sonucu oluşmuştur. Sistemin kütlesinin %99,86'sını merkezdeki yıldızımız Güneş oluşturur.\n\n"
            "### 📌 8 Gezegen (Güneş'ten Dışa Doğru)\n"
            "• **İç (Kayalık) Gezegenler:** Merkür (en küçük ve en hızlı), Venüs (en sıcak, yoğun sera etkisi), "
            "Dünya (yaşam barındıran tek bilinen gezegen) ve Mars (Kızıl Gezegen, Olympus Mons yanardağı).\n"
            "• **Dış (Gaz & Buz Devi) Gezegenler:** Jüpiter (en büyük gezegen, Büyük Kırmızı Leke), Satürn "
            "(buz ve kaya halkaları), Uranüs (yana yatık eksen) ve Neptün (en şiddetli rüzgârlar).\n\n"
            "### 📌 Cüce Gezegenler ve Keşifler\n"
            "Plüton, Eris ve Ceres başlıca cüce gezegenlerdir. Voyager 1 ve 2 uzay araçları yıldızlararası "
            "uzaya ulaşarak insanlığın Güneş Sistemi dışındaki ilk elçileri olmuştur."
        ),
    },

    "kapı yapımı": {
        "baslik": "Ahşap Kapı Yapımı (Adım Adım Marangozluk Rehberi)",
        "url": "https://tr.wikipedia.org/wiki/Kap%C4%B1",
        "gorsel": "",
        "bolumler": ["Ölçü ve Kereste Seçimi", "İskelet (Karkas) ve Panel Montajı", "Zımpara, Vernik ve Menteşe Ayarı"],
        "ozet": (
            "Sağlam bir ahşap kapı yapmak için doğru ölçü, kuru kereste (nem oranı %8–12) ve gönye hassasiyeti temel şarttır.\n\n"
            "### 📌 1. Ölçü Alma ve Malzeme Seçimi\n"
            "Kapı boşluğunun genişliğini ve yüksekliğini üst-orta-alt olmak üzere 3 noktadan ölç. Standart iç oda "
            "kapısı yaklaşık 80×200 cm'dir. Çam, meşe, kayın veya MDF/panel yüzey; 2–3 adet çelik menteşe, ahşap "
            "tutkalı (D3/PVA), kavela veya zıvana bağlantı elemanları ve kapı kilidi hazırla.\n\n"
            "### 📌 2. İskelet (Seren ve Başlık) Kurulumu\n"
            "İki dikey seren (yan direk) ve 3–4 yatay başlığı gönyede kes. Zıvana veya kavela deliklerini açıp "
            "tutkallayarak işkencelerle (kelepçe) sık; çapraz köşegen ölçüleri eşit olana kadar kontrol et ve 12 saat kurumaya bırak.\n\n"
            "### 📌 3. Yüzey Kaplama, Zımpara ve Montaj\n"
            "İskeletin iki yüzüne MDF/kontrplak veya masif ahşap tablaları presle. Sırasıyla 120 ve 220 numara "
            "zımpara yap, astar ve su bazlı vernik/boya uygula. Kilit yuvası ve menteşe kertiklerini açıp kasaya "
            "terazide monte ederek kapının sürtmeden kapanmasını test et."
        ),
    },
    "ev yapımı": {
        "baslik": "Ev Yapımı ve İnşaat Süreci (Temelden Çatıya Rehber)",
        "url": "https://tr.wikipedia.org/wiki/Ev",
        "gorsel": "",
        "bolumler": ["Zemin Etüdü ve Mimari Proje", "Temel, Kaba İnşaat ve Deprem Güvenliği", "Tesisat, Yalıtım ve İnce İşçilik"],
        "ozet": (
            "Güvenli ve yönetmeliğe uygun bir ev yapımı mühendislik hesapları, ruhsat süreci ve aşamalı uygulama gerektirir.\n\n"
            "### 📌 1. Zemin Etüdü, Proje ve Ruhsat\n"
            "Arsanın jeolojik zemin etüdü yapılır; mimari, statik (deprem hesabı), elektrik ve mekanik projeler "
            "hazırlanarak belediyeden yapı ruhsatı alınır.\n\n"
            "### 📌 2. Temel ve Kaba İnşaat (Taşıyıcı Sistem)\n"
            "Hafriyat sonrası radye temel (depreme en dayanıklı temel tipi) demir donatıları döşenir ve C30/C35 sınıfı "
            "hazır beton dökülür. Kolon, perde duvar, kiriş ve döşemeler Türkiye Bina Deprem Yönetmeliği'ne (TBDY) "
            "uygun biçimde tamamlanır; ardından tuğla/gazbeton duvarlar ve çatı kapatılır.\n\n"
            "### 📌 3. Tesisat, Isı-Su Yalıtımı ve İnce İşler\n"
            "Temiz/pis su, doğalgaz ve elektrik tesisatları çekilir. Dış cephe mantolama ve çatı su yalıtımı "
            "yapıldıktan sonra sıva, şap, seramik/parke, kapı-pencere montajı ve boya ile yapı oturuma hazır hâle getirilir."
        ),
    },
    "göbeklitepe": {
        "baslik": "Göbeklitepe (Tarihin Sıfır Noktası — Şanlıurfa)",
        "url": "https://tr.wikipedia.org/wiki/G%C3%B6beklitepe",
        "gorsel": "",
        "bolumler": ["Keşfi ve Tarihlendirmesi", "T Biçimli Dikilitaşlar", "İnsanlık Tarihine Etkisi"],
        "ozet": (
            "Göbeklitepe, Şanlıurfa'nın 18 km kuzeydoğusunda yer alan ve yaklaşık MÖ 9600–8200 yıllarına (günümüzden "
            "yaklaşık 11.600 yıl öncesine) tarihlenen dünyanın bilinen en eski anıtsal inanç ve toplanma merkezidir.\n\n"
            "### 📌 T Biçimli Dikilitaşlar ve Kabartmalar\n"
            "Boyları 3 ila 6 metre, ağırlıkları 10–20 ton arasında değişen T biçimli kireçtaşı sütunların üzerinde "
            "tilki, yaban domuzu, yılan, turna ve akrep kabartmaları bulunur. Bu dikilitaşlar stilize edilmiş insan "
            "figürlerini temsil eder.\n\n"
            "### 📌 Tarih Anlayışını Değiştiren Bulgu\n"
            "1995'te Klaus Schmidt liderliğinde başlayan kazılar, insanların önce tarıma geçip sonra tapınak yaptığı "
            "teorisini tersine çevirdi; avcı-toplayıcı toplulukların ortak inanç etrafında birleşerek yerleşik hayata "
            "geçtiğini kanıtladı. 2018'de UNESCO Dünya Mirası Listesi'ne alındı."
        ),
    },
    "dara antik kenti": {
        "baslik": "Dara Antik Kenti (Mezopotamya'nın Efes'i — Mardin)",
        "url": "https://tr.wikipedia.org/wiki/Dara_(Mezopotamya)",
        "gorsel": "",
        "bolumler": ["Tarihçesi ve Stratejik Önemi", "Dev Sarnıçlar ve Kaya Mezarları", "Ziyaret Bilgisi"],
        "ozet": (
            "Dara Antik Kenti, Mardin'in Artuklu ilçesine yaklaşık 30 km uzaklıkta, tarihi İpek Yolu üzerinde "
            "MS 505 yılında Doğu Roma İmparatoru Anastasios tarafından Sasani saldırılarına karşı sınır garnizon "
            "kenti olarak kurulmuştur.\n\n"
            "### 📌 Mimari Harikalar\n"
            "Ana kayaya oyulmuş 40 metre yüksekliğe ulaşan dev yeraltı su sarnıçları (zindan olarak da anılır), "
            "kilometrelerce uzanan su kanalları, kaya mezarları, agora, köprüler ve nekropol alanıyla Yukarı "
            "Mezopotamya'nın en görkemli arkeolojik yerleşimlerinden biridir."
        ),
    },
    "süleymaniye camii": {
        "baslik": "Süleymaniye Camii ve Külliyesi (Mimar Sinan — İstanbul)",
        "url": "https://tr.wikipedia.org/wiki/S%C3%BCleymaniye_Camii",
        "gorsel": "",
        "bolumler": ["İnşa Süreci ve Mimari Deha", "Akustik ve Mühendislik Sırları", "Külliye Yapıları"],
        "ozet": (
            "Süleymaniye Camii, Kanuni Sultan Süleyman adına Mimar Sinan tarafından 1551–1557 yılları arasında "
            "İstanbul Fatih'te inşa edilen ve Sinan'ın 'kalfalık eserim' dediği klasik Osmanlı mimarisinin zirvelerindendir.\n\n"
            "### 📌 Akustik, İs Odası ve Deprem Mühendisliği\n"
            "53 metre yüksekliğindeki ana kubbe çevresine yerleştirilen 64 adet boş toprak küp sayesinde mekân "
            "içinde eşsiz bir akustik sağlanmıştır. Kandil islerini tek bir odada toplayan hava akımı sistemiyle "
            "toplanan isten devrin en kaliteli mürekkebi üretilmiştir. 4 minaresi Kanuni'nin İstanbul'un fethinden "
            "sonraki 4. padişah, 10 şerefesi ise Osmanlı'nın 10. padişahı olduğunu simgeler."
        ),
    },
    "topkapı sarayı": {
        "baslik": "Topkapı Sarayı (İstanbul — Osmanlı Yönetim Merkezi)",
        "url": "https://tr.wikipedia.org/wiki/Topkap%C4%B1_Saray%C4%B1",
        "gorsel": "",
        "bolumler": ["Kuruluş ve 400 Yıllık Yönetim", "Avlular, Harem ve Kutsal Emanetler", "Müze ve Ziyaret"],
        "ozet": (
            "Topkapı Sarayı, Fatih Sultan Mehmet tarafından 1460–1478 yılları arasında İstanbul Sarayburnu'nda "
            "inşa ettirilen ve yaklaşık 380 yıl boyunca Osmanlı İmparatorluğu'nun idare merkezi ile padişahların "
            "ikametgâhı olan tarihî saray kompleksidir.\n\n"
            "### 📌 Bölümleri ve Eşsiz Koleksiyonları\n"
            "Dört ana avlu, Divân-ı Hümâyun (Kubbealtı), Enderun Mektebi, Harem Dairesi, Bağdat ve Revan Köşkleri "
            "ile dünyanın en zengin porselen, silah ve mücevher koleksiyonlarına ev sahipliği yapar. Hırka-i Saadet "
            "Dairesi'nde İslam dünyasının en kıymetli Kutsal Emanetleri korunmaktadır."
        ),
    },
    "kapadokya": {
        "baslik": "Kapadokya (Peribacaları ve Yeraltı Şehirleri — Nevşehir)",
        "url": "https://tr.wikipedia.org/wiki/Kapadokya",
        "gorsel": "",
        "bolumler": ["Jeolojik Oluşum (Peribacaları)", "Yeraltı Şehirleri ve Göreme", "UNESCO Mirası"],
        "ozet": (
            "Kapadokya, 60 milyon yıl önce Erciyes, Hasandağı ve Güllüdağ yanardağlarının püskürttüğü lav ve "
            "küllerin oluşturduğu yumuşak tüf tabakalarının milyonlarca yıl boyunca yağmur ve rüzgârla aşınmasıyla "
            "ortaya çıkan benzersiz bir doğa ve tarih bölgesidir.\n\n"
            "### 📌 Tarihî Miras ve Öne Çıkanlar\n"
            "Derinkuyu ve Kaymaklı gibi sekiz kat derine inen yeraltı şehirleri, Göreme Açık Hava Müzesi kaya "
            "kiliseleri, Uçhisar Kalesi, Ihlara Vadisi ve gün doğumunda gökyüzünü süsleyen sıcak hava balonlarıyla "
            "1985'ten beri UNESCO Dünya Mirası Listesi'ndedir."
        ),
    },
    "efes antik kenti": {
        "baslik": "Efes Antik Kenti (İzmir — Selçuk)",
        "url": "https://tr.wikipedia.org/wiki/Efes",
        "gorsel": "",
        "bolumler": ["Tarihsel Önemi", "Celsus Kütüphanesi ve Büyük Tiyatro", "Artemis Tapınağı"],
        "ozet": (
            "Efes, İzmir'in Selçuk ilçesinde yer alan; Helenistik ve Roma dönemlerinde Anadolu'nun en büyük liman "
            "ve ticaret metropollerinden biri olmuş, 2015'te UNESCO Dünya Mirası Listesi'ne girmiş antik kenttir.\n\n"
            "### 📌 Öne Çıkan Yapılar\n"
            "İki katlı görkemli cephesiyle Celsus Kütüphanesi, 24.000 kişilik Büyük Tiyatro, mermer döşeli Kuretler "
            "Caddesi, Yamaç Evler ve Antik Dünyanın Yedi Harikası'ndan biri sayılan Artemis Tapınağı'nın kalıntıları "
            "Efes'i dünya arkeolojisinin en önemli merkezlerinden biri yapar."
        ),
    },

    "yapay zeka": {
        "baslik": "Yapay zekâ",
        "ozet": (
            "Yapay zekâ (YZ), bir bilgisayarın veya bilgisayar kontrolündeki bir robotun çeşitli faaliyetleri zeki canlılara benzer şekilde yerine getirme kabiliyetidir. "
            "İnsan zekâsına özgü öğrenme, akıl yürütme, problem çözme, algılama ve doğal dil anlama gibi yüksek bilişsel işlevleri моделleyen yazılım ve donanım sistemlerini kapsar.\n\n"
            "Günümüzde yapay zekâ; makine öğrenmesi, derin öğrenme, büyük dil modelleri (LLM), bilgisayarlı görü ve otonom robotik sistemlerde temel teknoloji olarak kullanılmaktadır."
        ),
        "url": "https://tr.wikipedia.org/wiki/Yapay_zek%C3%A2",
        "gorsel": "",
        "bolumler": ["Tarihçe", "Makine Öğrenmesi", "Derin Öğrenme", "Kullanım Alanları"],
    },
    "insansız hava aracı": {
        "baslik": "İnsansız hava aracı (İHA)",
        "ozet": (
            "İnsansız hava aracı (İHA), içerisinde insan pilot bulunmadan uzaktan kumanda ile veya otonom uçuş kontrol bilgisayarları sayesinde kendi kendine uçabilen hava aracıdır. "
            "Sivil alanda haritalama, tarım, arama-kurtarma ve yangınla mücadelede; savunma alanında ise keşif, gözetleme ve operasyonel görevlerde yaygın olarak kullanılır."
        ),
        "url": "https://tr.wikipedia.org/wiki/%C4%B0nsans%C4%B1z_hava_arac%C4%B1",
        "gorsel": "",
        "bolumler": ["Tarihçe", "Otonom Uçuş Kontrolü", "Sensör ve Aviyonik Sistemler"],
    },
    "kara delik": {
        "baslik": "Kara delik",
        "ozet": (
            "Kara delik, astrofizikte kütleçekim alanı her türlü maddesel oluşumun ve ışık dahil tüm elektromanyetik radyasyonun kendisinden kaçmasına izin vermeyecek derecede güçlü olan kozmik bir gök cismidir. "
            "Genel görelilik kuramına göre yeterince sıkışmış bir kütle, uzay-zamanı bükerek olay ufku adı verilen geri dönülmez bir sınır oluşturur.\n\n"
            "Büyük kütleli yıldızların süpernova patlamasıyla çökmeleri sonucunda yıldızsal kara delikler, galaksilerin merkezlerinde ise milyonlarca Güneş kütleli süper kütleli kara delikler bulunur."
        ),
        "url": "https://tr.wikipedia.org/wiki/Kara_delik",
        "gorsel": "",
        "bolumler": ["Olay Ufku", "Genel Görelilik", "Yıldızsal ve Süper Kütleli Kara Delikler"],
    },
    "karadelik": {
        "baslik": "Kara delik",
        "ozet": (
            "Kara delik, astrofizikte kütleçekim alanı ışık dahil hiçbir maddenin veya radyasyonun kaçmasına izin vermeyecek kadar güçlü olan kozmik gök cismidir. "
            "Sınırına 'olay ufku' adı verilir; büyük kütleli yıldızların ömrünü tamamlayıp kendi içine çökmesiyle oluşur."
        ),
        "url": "https://tr.wikipedia.org/wiki/Kara_delik",
        "gorsel": "",
        "bolumler": ["Olay Ufku", "Oluşumu", "Gözlemlenmesi"],
    },
    "mars": {
        "baslik": "Mars (Kızıl Gezegen)",
        "ozet": (
            "Mars, Güneş Sistemi'nde Güneş'e yakınlık sırasına göre dördüncü gezegendir. Yüzeyindeki yaygın demir oksit nedeniyle kızılımsı bir görünüme sahip olduğu için 'Kızıl Gezegen' olarak da adlandırılır.\n\n"
            "İnce bir atmosferi olan Mars; Güneş Sistemi'nin en yüksek dağı olan Olympus Mons'a ve en büyük kanyon sistemlerinden Valles Marineris'e ev sahipliği yapar. İki küçük doğal uydusu vardır: Phobos ve Deimos."
        ),
        "url": "https://tr.wikipedia.org/wiki/Mars",
        "gorsel": "",
        "bolumler": ["Fiziksel Özellikler", "Atmosfer ve İklim", "Phobos ve Deimos", "Uzay Araştırmaları"],
    },
    "osmanlı imparatorluğu": {
        "baslik": "Osmanlı İmparatorluğu",
        "ozet": (
            "Osmanlı İmparatorluğu veya Osmanlı Devleti, 1299 yılında Osman Gazi tarafından Söğüt ve Domaniç çevresinde kurulan, 1453'te Fatih Sultan Mehmet'in İstanbul'u fethiyle imparatorluk gücüne ulaşan ve 1922 yılına kadar üç kıtada (Avrupa, Asya ve Afrika) hüküm süren Türk-İslam devletidir.\n\n"
            "En geniş sınırlarına 16. ve 17. yüzyıllarda ulaşmış; bilim, mimari, hukuk ve sanatta dünya tarihine derin izler bırakmıştır."
        ),
        "url": "https://tr.wikipedia.org/wiki/Osmanl%C4%B1_%C4%B0mparatorlu%C4%9Fu",
        "gorsel": "",
        "bolumler": ["Kuruluş Dönemi (1299)", "Yükseliş Dönemi (1453)", "Bilim ve Kültür"],
    },
    "albert einstein": {
        "baslik": "Albert Einstein",
        "ozet": (
            "Albert Einstein (14 Mart 1879 – 18 Nisan 1955), modern fiziğin iki temel direğinden biri olan Özel ve Genel Görelilik (İzafiyet) kuramlarını geliştiren teorik fizikçidir. "
            "Kütle-enerji eşdeğerliği formülü (E = mc²) ve fotoelektrik etki yasasıyla 1921 Nobel Fizik Ödülü'nü kazanmıştır."
        ),
        "url": "https://tr.wikipedia.org/wiki/Albert_Einstein",
        "gorsel": "",
        "bolumler": ["Özel ve Genel Görelilik", "Fotoelektrik Etki", "Nobel Fizik Ödülü"],
    },
    "dünya": {
        "baslik": "Dünya",
        "ozet": (
            "Dünya, Güneş Sistemi'nde Güneş'e en yakın üçüncü gezegen olup üzerinde yaşam ve sıvı su barındırdığı bilinen tek astronomik cisimdir. "
            "Kendi ekseni etrafındaki dönüşünü yaklaşık 24 saatte (1 gün) tamamlar ve bu dönüş açısal momentumun korunumu sayesinde gece ile gündüzün oluşmasını sağlar. Güneş etrafındaki yörünge turunu ise 365 gün 6 saatte tamamlar."
        ),
        "url": "https://tr.wikipedia.org/wiki/D%C3%BCnya",
        "gorsel": "",
        "bolumler": ["Dönüş Hareketi", "Atmosfer ve Biyosfer", "İç Yapısı"],
    },
    "kuantum mekaniği": {
        "baslik": "Kuantum mekaniği",
        "ozet": (
            "Kuantum mekaniği, atom ve atom altı parçacıkların (elektron, foton, kuark) davranışlarını inceleyen temel fizik kuramıdır. "
            "Enerjinin kesikli paketçikler (kuanta) halinde yayıldığını, dalga-parçacık ikiliğini ve Heisenberg belirsizlik ilkesini açıklar."
        ),
        "url": "https://tr.wikipedia.org/wiki/Kuantum_mekani%C4%9Fi",
        "gorsel": "",
        "bolumler": ["Dalga-Parçacık İkiliği", "Belirsizlik İlkesi", "Kuantum Bilgisayarlar"],
    },
    "python": {
        "baslik": "Python (programlama dili)",
        "ozet": (
            "Python, Guido van Rossum tarafından 1991 yılında geliştirilen; okunabilirliği yüksek, nesne yönelimli, yorumlamalı ve çok amaçlı bir programlama dilidir. "
            "Yapay zekâ, veri bilimi, görüntü işleme (OpenCV), robotik (Raspberry Pi), web geliştirme (Streamlit, Django) ve otomasyon alanlarında dünyanın en popüler dilidir."
        ),
        "url": "https://tr.wikipedia.org/wiki/Python_(programlama_dili)",
        "gorsel": "",
        "bolumler": ["Tasarım Felsefesi", "Yapay Zekâ ve Veri Bilimi", "Kütüphane Ekosistemi"],
    },
    "dna": {
        "baslik": "Deoksiribonükleik asit (DNA)",
        "ozet": (
            "DNA (Deoksiribonükleik asit), tüm canlı organizmaların ve birçok virüsün yaşamsal işlevleri, büyümesi ve çoğalması için gerekli olan genetik talimatları taşıyan çift sarmallı nükleik asit molekülüdür. "
            "Adenin (A), Timin (T), Guanin (G) ve Sitozin (C) bazlarının dizilimiyle genetik kodu oluşturur."
        ),
        "url": "https://tr.wikipedia.org/wiki/DNA",
        "gorsel": "",
        "bolumler": ["Çift Sarmal Yapı", "Genetik Kod", "Replikasyon"],
    },
}


def wikipedia_metnini_temizle(ham_metin: str) -> str:
    """
    Wikipedia API'sinden gelen metindeki [1], [2] dipnotlarını, bozuk parantezleri,
    IPA telaffuz kalıntılarını ve kopuk satırları temizleyerek akıcı Türkçe cümleler üretir.
    """
    if not ham_metin:
        return ""
    metin = re.sub(r"\[\d+\]|\[kaynak belirtilmeli\]|\[d[üu]zenle\]|\[not \d+\]", "", ham_metin, flags=re.IGNORECASE)
    # Boş veya sadece noktalama içeren parantezleri kaldır
    metin = re.sub(r"\(\s*[;,:\-]*\s*\)", "", metin)
    # Parantez başındaki bozuk noktalama: "(; İngilizce: ...)" -> "(İngilizce: ...)"
    metin = re.sub(r"\(\s*[;,]+\s*", "(", metin)
    # Noktalama öncesi fazla boşlukları düzelt
    metin = re.sub(r"\s+([.,;:!?])", r"\1", metin)
    metin = re.sub(r"[ \t]+", " ", metin)
    metin = re.sub(r"\n{3,}", "\n\n", metin)
    # Bölüm başlıklarını (== Başlık ==) temiz alt başlıklara dönüştür
    metin = re.sub(r"===\s*(.+?)\s*===", r"\n**🔹 \1**", metin)
    metin = re.sub(r"==\s*(.+?)\s*==", r"\n### 📌 \1", metin)
    return metin.strip()


def wikipedia_konu_ayikla(kullanici_girdisi: str) -> str:
    """
    v9.3 — Doğal Türkçe sohbet cümlesinden Wikipedia'da aranacak saf konu başlığını
    (Türkçe karakterleri koruyarak ve kibar/takip eklerini eksiksiz silerek) ayıklar.
    Örn: 'Bursa hakkında daha fazla bilgi verir misiniz?' -> 'Bursa'
         'Fatih Camii bilgi verir misin?' -> 'Fatih Camii'
         'Osmanlı İmparatorluğu kısaca anlatır mısınız?' -> 'Osmanlı İmparatorluğu'
    """
    temiz = str(kullanici_girdisi or "").strip()
    temiz = re.sub(
        r"^(?:wikipedia|vikipedi|wiki|araştır|arastir|bana|lütfen|lutfen|acaba|ar|hey\s+ar|merhaba|selam|peki)\s*[:\-]?\s*",
        "",
        temiz,
        flags=re.IGNORECASE,
    ).strip()

    # Kibar soru, uzunluk ve takip kalıplarını sondan başlayarak döngüyle temizle
    son_ekler = [
        r"\s+(?:verir\s*misiniz|verir\s*misin|verebilir\s*misiniz|verebilir\s*misin|veriniz|verin|ver)$",
        r"\s+(?:anlatır\s*mısınız|anlatir\s*misiniz|anlatır\s*mısın|anlatir\s*misin|anlatınız|anlatın|anlat)$",
        r"\s+(?:söyler\s*misiniz|soyler\s*misiniz|söyler\s*misin|soyler\s*misin|söyle|soyle)$",
        r"\s+(?:açıklar\s*mısınız|aciklar\s*misiniz|açıklar\s*mısın|aciklar\s*misin|açıkla|acikla)$",
        r"\s+(?:özetler\s*misiniz|ozetler\s*misiniz|özetler\s*misin|ozetler\s*misin|özetle|ozetle)$",
        r"\s+(?:araştırır\s*mısınız|arastirir\s*misiniz|araştırır\s*mısın|araştır|arastir)$",
        r"\s+(?:bu\s+bilgiyi\s+)?(?:yeterli\s+bulmuyorum|yeterli\s+değil|yeterli\s+degil|yetmedi)$",
        r"\s+(?:daha\s+fazla|daha\s+çok|daha\s+cok|daha\s+detaylı|daha\s+detayli|biraz\s+daha|detaylı|detayli|kapsamlı|kapsamli|derinlemesine|kısaca|kisaca|kısa|kisa|uzun|geniş|genis)$",
        r"\s+(?:bilgi|bilgiler|özet|ozet|detay|detaylar)$",
        r"\s+(?:hakkında|hakkinda|ile\s+ilgili|konusunda|üzerine|uzerine)$",
        r"\s+(?:ne\s+biliyorsun|ne\s+düşünüyorsun|ne\s+dusunuyorsun|devam\s*et|devam)$",
        r"\s+(?:ne\s+zaman\s+(?:kuruldu|yıkıldı|doğdu|öldü|yapıldı|keşfedildi|icat\s+edildi|başladı|bitti))$",
        r"\s+(?:nasıl\s+(?:oluşur|çalışır|yapılır|yapilir|olur|kuruldu|keşfedildi|bir\s+yer|bir\s+şehir|bir\s+ülke))$",
        r"\s+(?:kimdir|kim|nedir|ne\s+demektir|ne\s+demek|nerededir|nerede\s+bulunur|nerede|neresi(?:dir)?|nasıldır|nasıl|nasil)$",
        # v14: "Osmanlı neden çöktü", "II. Dünya Savaşı niçin başladı", "Roma ne zaman yıkıldı" → soru kalıbını at
        r"\s+(?:neden|niçin|nicin|niye|ne\s+zaman|nasıl|nasil|hangi\s+yıl(?:da)?|kaç\s+yılında)(?:\s+[a-zçğıöşü]+){1,2}$",
        r"\s+(?:mimarisi|tarihi|yemekleri|özellikleri|nedenleri|sonuçları|neler|nelerdir)$",
        r"\s+(?:vikipedi(?:\s*de\s*ara)?|wikipedia(?:\s*da\s*ara)?)$",
    ]
    temiz = temiz.strip("?!.,;:\"' ")
    for _ in range(5):
        onceki = temiz
        for desen in son_ekler:
            temiz = re.sub(desen, "", temiz, flags=re.IGNORECASE).strip("?!.,;:\"' ")
        if temiz == onceki:
            break

    temiz = re.sub(r"^(?:bana|lütfen|lutfen|biraz)\s+", "", temiz, flags=re.IGNORECASE).strip()
    temiz = re.sub(r"^mars\s+gezegeni$", "Mars", temiz, flags=re.IGNORECASE)
    temiz = re.sub(r"^karadelik$", "Kara delik", temiz, flags=re.IGNORECASE)
    return temiz.strip("?!.,;:\"' ")

_WIKI_ONBELLEK = {}


def _http_json_getir(url: str, timeout: int = 7):
    """Wikimedia API isteği: kimlikli User-Agent (Wikimedia politikası, hız sınırına daha az takılır)
    ve 1 saatlik bellek içi önbellek (aynı konu tekrar sorulunca anında yanıt)."""
    simdi = time.time()
    kayit = _WIKI_ONBELLEK.get(url)
    if kayit and simdi - kayit[0] < 3600:
        return kayit[1]
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AREX-AI-Studio/14 (+https://streamlit.io; egitim asistani)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        veri = json.loads(resp.read().decode("utf-8"))
    if len(_WIKI_ONBELLEK) > 400:
        _WIKI_ONBELLEK.clear()
    _WIKI_ONBELLEK[url] = (simdi, veri)
    return veri


def wikipedia_arama_onerileri(sorgu: str, dil: str = "tr", limit: int = 6) -> list:
    """Wikipedia'da sorguya en yakın madde başlıklarını ve kısa açıklamalarını arar."""
    konu = wikipedia_konu_ayikla(sorgu)
    if not konu:
        return []
    try:
        q = urllib.parse.quote(konu)
        url = (
            f"https://{dil}.wikipedia.org/w/api.php?"
            f"action=query&list=search&srsearch={q}&srlimit={limit}&format=json&utf8=1"
        )
        veri = _http_json_getir(url)
        sonuclar = []
        for item in veri.get("query", {}).get("search", []):
            snippet = re.sub(r"<[^>]+>", "", item.get("snippet", ""))
            sonuclar.append({
                "baslik": item.get("title", ""),
                "kisa_ozet": wikipedia_metnini_temizle(snippet),
            })
        if not sonuclar:
            # opensearch yalnızca başlık ön-ekiyle eşleşir; tam metin araması (list=search) çok daha isabetlidir!
            s_url = (
                f"https://{dil}.wikipedia.org/w/api.php?"
                f"action=query&list=search&srsearch={q}&srlimit={limit}&format=json&utf8=1"
            )
            s_veri = _http_json_getir(s_url, timeout=6)
            for item in s_veri.get("query", {}).get("search", []):
                b = item.get("title", "").strip()
                if b:
                    sonuclar.append({
                        "baslik": b,
                        "aciklama": re.sub(r"<[^>]+>", "", item.get("snippet", "")),
                        "url": f"https://{dil}.wikipedia.org/wiki/{urllib.parse.quote(b.replace(' ', '_'))}",
                    })
        return sonuclar
    except Exception:
        return []


def wikipedia_madde_getir(sorgu: str, dil: str = "tr", detay_karakter: int = 4500) -> dict:
    """
    Wikipedia'dan maddenin tam düzgün özetini, alt bölümlerini, kapak görselini
    ve kaynak bağlantısını getirir. Türkçe Vikipedi'de bulunamazsa İngilizce'den
    otomatik arayıp Türkçeye çevirme desteği sunar; çevrimdışıysa yerleşik yedekten döner.
    """
    konu = wikipedia_konu_ayikla(sorgu)
    if not konu:
        return {"basarili": False, "hata": "Lütfen aramak istediğiniz bir konu başlığı girin."}

    def _tr_ascii(s: str) -> str:
        return (
            s.replace("İ", "i").replace("I", "i").lower()
            .replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            .replace("ö", "o").replace("ş", "s").replace("ü", "u")
        )

    def _en_alakali_aday_sec(aranan: str, adaylar_listesi: list):
        """
        v10.5 SIKI WİKİPEDİA BAŞLIK ALAKA KAPISI:
        'hatalarını düzeltmekle uğraşıyorum' -> 'Deep Impact (uzay aracı)' gibi 0 alakalı
        tam-metin eşleşmelerini %100 REDDEDER! En az bir anlamlı sorgu kelimesi başlıkla
        gerçekten örtüşmüyorsa None döndürür.
        """
        if not adaylar_listesi:
            return None
        durak = {
            "bir", "veya", "ile", "icin", "gibi", "daha", "cok", "ama", "fakat", "ancak",
            "nedir", "kimdir", "nasil", "neden", "nerede", "hakkinda", "bilgi", "anlat",
            "olarak", "olan", "olanlar", "uzerine", "bana", "sana", "benim", "senin",
        }
        q_norm = _tr_ascii(aranan).strip()
        q_kelimeler = [w for w in re.findall(r"[a-z0-9]+", q_norm) if len(w) >= 3 and w not in durak]
        if not q_kelimeler:
            return None

        en_iyi_b = None
        en_iyi_p = 0.0
        for idx, aday in enumerate(adaylar_listesi[:5]):
            b = aday.get("baslik", "")
            b_norm = _tr_ascii(b).strip()
            b_kelimeler = [w for w in re.findall(r"[a-z0-9]+", b_norm) if len(w) >= 2]
            if not b_kelimeler:
                continue

            eslesen_kelime = 0
            p = 0.0
            if b_norm == q_norm:
                p += 25.0
                eslesen_kelime += len(q_kelimeler)
            elif q_norm in b_norm or b_norm in q_norm:
                if len(b_norm) >= 3:
                    p += 12.0
                    eslesen_kelime += 1

            for qk in q_kelimeler:
                kok = qk[:5] if len(qk) >= 6 else qk
                if any(qk == bk or (len(kok) >= 4 and (bk.startswith(kok) or kok in bk)) for bk in b_kelimeler):
                    eslesen_kelime += 1
                    p += 5.0

            if "(anlam ayrimi)" in b_norm or "(disambiguation)" in b_norm:
                p -= 10.0

            # SIKI ALAKA KAPISI: Sorgudan tek bir anlamlı kelime bile başlıkta geçmiyorsa REDDET!
            if eslesen_kelime == 0 or p < 4.5:
                continue
            p += max(0.0, 1.0 - idx * 0.2)
            if p > en_iyi_p:
                en_iyi_p = p
                en_iyi_b = b
        return en_iyi_b

    def _detay_url(baslik: str, hedef_dil: str) -> str:
        return (f"https://{hedef_dil}.wikipedia.org/w/api.php?"
                f"action=query&prop=extracts|pageimages|info|pageprops&ppprop=disambiguation&inprop=url&pithumbsize=500"
                f"&explaintext=1&{'exchars=1200' if detay_karakter <= 1200 else 'exintro=1'}&redirects=1"
                f"&titles={urllib.parse.quote(baslik)}&format=json&utf8=1")

    def _dogrudan_baslik_dene(aranan_baslik: str, hedef_dil: str):
        """'Fatih Sultan Mehmet' → (yönlendirme) 'II. Mehmed'. Anlam ayrımı sayfalarını atlar.
        İçerik aynı istekte gelir → arama + içerik için 2 yerine tek istek."""
        if not aranan_baslik or len(aranan_baslik.split()) > 6:
            return None
        baslik = aranan_baslik.strip()
        if hedef_dil == "tr":
            kucuk = baslik.replace("İ", "i").replace("I", "ı").lower()
            kucuk = re.sub(r"^ikinci\s+", "II. ", kucuk)
            kucuk = re.sub(r"^birinci\s+", "I. ", kucuk)
            if kucuk != baslik.replace("İ", "i").replace("I", "ı").lower():
                baslik = kucuk.replace("dünya savaşı", "Dünya Savaşı")
            else:
                baslik = (baslik[:1].replace("i", "İ").replace("ı", "I").upper() if baslik[:1] in "iı" else baslik[:1].upper()) + baslik[1:]
        else:
            baslik = baslik[:1].upper() + baslik[1:]
        try:
            v = _http_json_getir(_detay_url(baslik, hedef_dil), timeout=5)
        except Exception:
            return None
        for pid, sayfa in v.get("query", {}).get("pages", {}).items():
            if str(pid) == "-1" or "missing" in sayfa or "disambiguation" in sayfa.get("pageprops", {}):
                return None
            if not sayfa.get("extract", "").strip():
                return None
            return sayfa.get("title"), baslik
        return None

    def _tek_dil_cek(aranan_baslik: str, hedef_dil: str):
        dogrudan = _dogrudan_baslik_dene(aranan_baslik, hedef_dil)
        istek_basligi = None
        if dogrudan:
            secilen_baslik, istek_basligi = dogrudan
            adaylar = [{"baslik": secilen_baslik, "kisa_ozet": ""}]
        else:
            adaylar = wikipedia_arama_onerileri(aranan_baslik, dil=hedef_dil, limit=5)
            secilen_baslik = _en_alakali_aday_sec(aranan_baslik, adaylar)
        if not secilen_baslik:
            return None

        q_title = urllib.parse.quote(secilen_baslik)
        # Doğrudan başlıkla geldiyse aynı URL önbellekte → ek ağ isteği yok
        veri = _http_json_getir(_detay_url(istek_basligi or secilen_baslik, hedef_dil))
        sayfalar = veri.get("query", {}).get("pages", {})
        for pid, sayfa in sayfalar.items():
            if str(pid) == "-1" or "missing" in sayfa:
                continue
            ham_ozet = sayfa.get("extract", "")
            if not ham_ozet.strip():
                continue
            temiz_ozet = wikipedia_metnini_temizle(ham_ozet)
            if len(temiz_ozet) > detay_karakter:
                kesilmis = temiz_ozet[:detay_karakter]
                son_nokta = kesilmis.rfind(".")
                temiz_ozet = kesilmis[:son_nokta + 1] if son_nokta > 250 else kesilmis + "..."

            bolumler = re.findall(r"^### 📌 (.+)$", temiz_ozet, flags=re.MULTILINE)
            gorsel_url = sayfa.get("thumbnail", {}).get("source", "")
            tam_url = sayfa.get("fullurl", f"https://{hedef_dil}.wikipedia.org/wiki/{q_title}")
            return {
                "basarili": True,
                "baslik": sayfa.get("title", secilen_baslik),
                "ozet": temiz_ozet,
                "gorsel": gorsel_url,
                "url": tam_url,
                "dil": "Türkçe Vikipedi" if hedef_dil == "tr" else "English Wikipedia",
                "bolumler": bolumler,
                "diger_oneriler": [a["baslik"] for a in adaylar[1:5]],
            }
        return None

    try:
        sonuc = _tek_dil_cek(konu, dil)
        if sonuc:
            return sonuc
        if dil == "tr":
            en_sonuc = _tek_dil_cek(konu, "en")
            if en_sonuc:
                try:
                    en_sonuc["ozet"] = guvenli_cevir(en_sonuc["ozet"][:1800], src="en", dest="tr")
                    en_sonuc["dil"] = "Wikipedia (İngilizce -> Türkçe Çeviri)"
                except Exception:
                    pass
                return en_sonuc
    except Exception:
        pass

    # Çevrimdışı / Hızlı Yedek Ansiklopedi Kontrolü
    konu_kucuk = konu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    for anahtar, y in YEDEK_WIKIPEDIA_MADDELERI.items():
        if anahtar == konu_kucuk or anahtar in konu_kucuk or konu_kucuk in anahtar:
            return {
                "basarili": True,
                "baslik": y["baslik"],
                "ozet": y["ozet"],
                "gorsel": y["gorsel"],
                "url": y["url"],
                "dil": "Wikipedia Ansiklopedi Belleği",
                "bolumler": y["bolumler"],
                "diger_oneriler": [],
            }

    return {
        "basarili": False,
        "hata": f"Wikipedia'da '{konu}' ile ilgili madde bulunamadı veya internet bağlantısı kurulamadı.",
    }


def wikipedia_sonucunu_metne_formatla(sonuc: dict) -> str:
    """Sohbet botu için akıcı, düzgün cümleli ve kaynak bağlantılı Wikipedia yanıtı üretir."""
    if not sonuc.get("basarili"):
        return f"🌐 **Wikipedia:** {sonuc.get('hata', 'Sonuç bulunamadı.')}"

    satirlar = [
        f"### 🌐 Wikipedia: **{sonuc['baslik']}**",
        f"*🔍 Araştırıldı — Kaynak: `{sonuc.get('dil', 'Türkçe Vikipedi')}`* | [🔗 Wikipedia Sayfasını Aç]({sonuc.get('url', '')})\n",
        sonuc["ozet"],
    ]
    if sonuc.get("diger_oneriler"):
        satirlar.append("\n**🔎 İlgili Diğer Başlıklar:** " + " • ".join(f"`{b}`" for b in sonuc["diger_oneriler"]))
    return "\n".join(satirlar)


# ==============================================================================
# WIKIPEDIA STÜDYOSU ARAYÜZÜ (Eğitim & Ansiklopedi Merkezinden de Erişilebilir)
# ==============================================================================
def wikipedia_studyosu_goster(sesli_soyle_fn):
    st.markdown("#### 🌐 Wikipedia (Vikipedi) Canlı Ansiklopedi Araştırma Ekranı")
    st.caption("💡 İpucu: Burayı kullanabileceğin gibi doğrudan **Ana Sohbet Botuna** istediğin konuyu yazarak da Wikipedia'dan araştırma yaptırabilirsin!")

    ust1, ust2 = st.columns([1.2, 2.0])
    with ust1:
        st.session_state.wikipedia_aktif = st.toggle(
            "🌐 Sohbette Otomatik Wikipedia (Aç / Kapat)",
            value=st.session_state.get("wikipedia_aktif", True),
            key="studio_wiki_toggle",
        )
    with ust2:
        wiki_dil = st.radio(
            "Ansiklopedi Dili:",
            ["tr", "en"],
            format_func=lambda x: "🇹🇷 Türkçe Vikipedi" if x == "tr" else "🇬🇧 İngilizce Wikipedia",
            horizontal=True,
        )

    hk1, hk2, hk3, hk4, hk5, hk6 = st.columns(6)
    hizli_konu = None
    if hk1.button("🤖 Yapay Zeka", use_container_width=True):
        hizli_konu = "Yapay zeka"
    if hk2.button("🚁 İHA / Drone", use_container_width=True):
        hizli_konu = "İnsansız hava aracı"
    if hk3.button("⚛️ Kuantum", use_container_width=True):
        hizli_konu = "Kuantum mekaniği"
    if hk4.button("🪐 Kara Delik", use_container_width=True):
        hizli_konu = "Kara delik"
    if hk5.button("🏰 Osmanlı", use_container_width=True):
        hizli_konu = "Osmanlı İmparatorluğu"
    if hk6.button("🐍 Python", use_container_width=True):
        hizli_konu = "Python"

    col_w1, col_w2 = st.columns([2.2, 1.0])
    with col_w1:
        aranan_konu = st.text_input(
            "Wikipedia'da Araştırmak İstediğin Konu:",
            value=hizli_konu or st.session_state.get("son_wiki_konu", "Yapay zeka"),
            placeholder="Örn: El-Cezeri, Fatih Sultan Mehmet, Mars, DNA...",
        )
    with col_w2:
        detay_uzunlugu = st.selectbox(
            "Okuma Derinliği:",
            [1500, 3000, 5000],
            index=1,
            format_func=lambda x: "📄 Kısa Özet" if x == 1500 else ("📚 Detaylı Madde" if x == 3000 else "📖 Tam Makale"),
        )

    wb1, wb2 = st.columns(2)
    btn_wiki_ara = wb1.button("🔍 Araştır ve Wikipedia'dan Getir", use_container_width=True)
    btn_wiki_ses = wb2.button("🔊 Bul ve Sesli Dinle", use_container_width=True)

    if btn_wiki_ara or btn_wiki_ses or hizli_konu:
        secilen_konu = hizli_konu or aranan_konu
        st.session_state["son_wiki_konu"] = secilen_konu
        with st.spinner(f"🔍 Araştırılıyor, Wikipedia'ya gidiliyor ('{secilen_konu}')..."):
            sonuc = wikipedia_madde_getir(secilen_konu, dil=wiki_dil, detay_karakter=detay_uzunlugu)
        st.session_state["son_wiki_sonuc"] = sonuc
        if btn_wiki_ses and sonuc.get("basarili"):
            sesli_soyle_fn(f"{sonuc['baslik']}. {sonuc['ozet'][:650]}", dil="tr" if wiki_dil == "tr" else "en")

    aktif_wiki = st.session_state.get("son_wiki_sonuc")
    if aktif_wiki is None:
        aktif_wiki = wikipedia_madde_getir("Yapay zeka", dil="tr", detay_karakter=2400)
        st.session_state["son_wiki_sonuc"] = aktif_wiki

    if aktif_wiki.get("basarili"):
        if aktif_wiki.get("gorsel"):
            col_img, col_txt = st.columns([1.0, 2.4], gap="large")
            with col_img:
                st.image(aktif_wiki["gorsel"], caption=aktif_wiki["baslik"], use_container_width=True)
                st.link_button("🔗 Wikipedia'da Aç", aktif_wiki["url"], use_container_width=True)
            with col_txt:
                st.markdown(
                    bilgi_karti_olustur(
                        f"🌐 {aktif_wiki['baslik']}",
                        f"Kaynak: {aktif_wiki.get('dil', 'Wikipedia')}",
                        aktif_wiki["ozet"].replace("\n", "<br>"),
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                bilgi_karti_olustur(
                    f"🌐 {aktif_wiki['baslik']}",
                    f"Kaynak: {aktif_wiki.get('dil', 'Wikipedia')}",
                    aktif_wiki["ozet"].replace("\n", "<br>"),
                ),
                unsafe_allow_html=True,
            )
            st.link_button("🔗 Orijinal Wikipedia Sayfasını Aç", aktif_wiki["url"])

        if aktif_wiki.get("diger_oneriler"):
            st.info("**🔎 İlgili Diğer Wikipedia Maddeleri:** " + " • ".join(aktif_wiki["diger_oneriler"]))
    else:
        st.warning(aktif_wiki.get("hata", "Madde bulunamadı."))
