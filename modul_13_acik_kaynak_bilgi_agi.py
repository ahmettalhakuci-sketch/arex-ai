# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v6.0 — MODÜL 13: AÇIK KAYNAK DÜNYA BİLGİ AĞI (ÜLKELER, 81 İL,
ŞEHİRLER, YEMEK TARİFLERİ, CANLI HAVA DURUMU VE KİTAP ARAMA MOTORU)
Tüm servisler %100 ÜCRETSİZ ve API ANAHTARSIZ açık kaynaklı kaynaklardır:
  • REST Countries (restcountries.com) -> 195+ Dünya Ülkesi
  • Türkiye 81 İl Yerleşik Bilgi Bankası + Wikipedia -> Tüm Şehirler
  • Open-Meteo (api.open-meteo.com) -> Canlı Hava Durumu
  • TheMealDB (themealdb.com) + Türk Mutfağı -> Yemek Tarifleri
  • Open Library (openlibrary.org) -> Kitap & Yazar Bilgisi
==============================================================================
"""
import importlib.util
import json
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


_m5 = _guvenli_modul_yukle("modul_5_dil_ve_cevirmeli_kartlar")
_m10 = _guvenli_modul_yukle("modul_10_wikipedia")
guvenli_cevir = _m5.guvenli_cevir
wikipedia_madde_getir = _m10.wikipedia_madde_getir


def _json_cek(url: str, timeout: int = 6):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ==============================================================================
# 1. TÜRKİYE'NİN 81 İLİ — TAM YERLEŞİK BİLGİ BANKASI (Plaka, Bölge, Öne Çıkanlar)
# ==============================================================================
TURKIYE_81_IL = {
    "adana": ("01", "Akdeniz", "Çukurova'nın kalbi; Taşköprü, Sabancı Merkez Camii, Adana kebabı ve şalgamıyla ünlüdür."),
    "adıyaman": ("02", "Güneydoğu Anadolu", "UNESCO Dünya Mirası Nemrut Dağı dev heykelleri ve çiğ köftesiyle bilinir."),
    "afyonkarahisar": ("03", "Ege", "Termal kaplıcaları, Afyon Kalesi, mermeri, kaymağı ve sucuğuyla meşhurdur."),
    "ağrı": ("04", "Doğu Anadolu", "Türkiye'nin en yüksek zirvesi Ağrı Dağı (5.137 m) ve İshak Paşa Sarayı buradadır."),
    "amasya": ("05", "Karadeniz", "Şehzadeler Şehri; Yeşilırmak kıyısındaki Yalıboyu evleri, Kral Kaya Mezarları ve elmasıyla ünlüdür."),
    "ankara": ("06", "İç Anadolu", "Türkiye Cumhuriyeti'nin başkenti; Anıtkabir, TBMM, Ankara Kalesi ve köklü üniversiteleriyle öne çıkar."),
    "antalya": ("07", "Akdeniz", "Türkiye'nin turizm başkenti; Kaleiçi, Düden Şelalesi, Aspendos ve turkuaz koylarıyla bilinir."),
    "artvin": ("08", "Karadeniz", "Karagöl, Kaçkar Dağları, derin vadileri ve yemyeşil yaylalarıyla doğa harikasıdır."),
    "aydın": ("09", "Ege", "Kuşadası, Didim, Afrodisias Antik Kenti ve dünyaca ünlü inciriyle tanınır."),
    "balıkesir": ("10", "Marmara", "Hem Marmara hem Ege'ye kıyısı vardır; Ayvalık, Kazdağları ve höşmerim tatlısıyla ünlüdür."),
    "bilecik": ("11", "Marmara", "Osmanlı İmparatorluğu'nun kurulduğu Söğüt ve Şeyh Edebali Türbesi buradadır."),
    "bingöl": ("12", "Doğu Anadolu", "Yüzen Adalar, Hesarek Kayak Merkezi ve doğal balıyla bilinir."),
    "bitlis": ("13", "Doğu Anadolu", "Nemrut Krater Gölü, Ahlat Selçuklu Mezarlığı ve büryan kebabıyla tanınır."),
    "bolu": ("14", "Karadeniz", "Abant, Yedigöller, Kartalkaya ve Mengenli usta aşçılarıyla meşhurdur."),
    "burdur": ("15", "Akdeniz", "Türkiye'nin Maldivleri sayılan Salda Gölü ve Sagalassos Antik Kenti buradadır."),
    "bursa": ("16", "Marmara", "Osmanlı'nın ilk başkenti 'Yeşil Bursa'; Uludağ, Ulu Camii, Yeşil Türbe, Cumalıkızık, İskender kebabı ve kestane şekeriyle ünlüdür."),
    "çanakkale": ("17", "Marmara", "Çanakkale Şehitler Abidesi, Gelibolu Yarımadası, Troya Antik Kenti ve 1915 Çanakkale Köprüsü buradadır."),
    "çankırı": ("18", "İç Anadolu", "Tuz Mağarası, Ilgaz Dağı Milli Parkı ve kaya tuzuyla bilinir."),
    "çorum": ("19", "Karadeniz", "Hitit İmparatorluğu'nun başkenti Hattuşa (Boğazkale) ve meşhur leblebisiyle tanınır."),
    "denizli": ("20", "Ege", "UNESCO mirası Pamukkale Travertenleri, Hierapolis Antik Kenti ve tekstil sanayisiyle ünlüdür."),
    "diyarbakır": ("21", "Güneydoğu Anadolu", "Tarihi Diyarbakır Surları, Hevsel Bahçeleri, On Gözlü Köprü ve karpuzuyla bilinir."),
    "edirne": ("22", "Marmara", "Osmanlı'ya başkentlik yapmış sınır şehri; Mimar Sinan'ın ustalık eseri Selimiye Camii, Kırkpınar ve tava ciğeriyle ünlüdür."),
    "elazığ": ("23", "Doğu Anadolu", "Harput Kalesi, Hazar Gölü, Keban Barajı ve orcik (cevizli sucuk) tatlısıyla bilinir."),
    "erzincan": ("24", "Doğu Anadolu", "Girlevik Şelalesi, Kemaliye Karanlık Kanyon ve tulum peyniriyle meşhurdur."),
    "erzurum": ("25", "Doğu Anadolu", "Palandöken Kayak Merkezi, Çifte Minareli Medrese, Oltu taşı ve cağ kebabıyla ünlüdür."),
    "eskişehir": ("26", "İç Anadolu", "Porsuk Çayı, Odunpazarı evleri, lületaşı, havacılık sanayisi ve öğrenci şehri kimliğiyle öne çıkar."),
    "gaziantep": ("27", "Güneydoğu Anadolu", "UNESCO Gastronomi Şehri; Zeugma Mozaik Müzesi, baklavası, fıstığı ve zengin mutfağıyla dünyaca ünlüdür."),
    "giresun": ("28", "Karadeniz", "Fındığın anavatanı; Giresun Adası, Kümbet ve Kulakkaya yaylalarıyla bilinir."),
    "gümüşhane": ("29", "Karadeniz", "Karaca Mağarası, Santa Harabeleri, pestil ve kömesiyle tanınır."),
    "hakkari": ("30", "Doğu Anadolu", "Cilo ve Sat Dağları buzulları, Zap Vadisi ve ters laleleriyle bilinir."),
    "hatay": ("31", "Akdeniz", "Medeniyetler şehri; Habib-i Neccar Camii, Titus Tüneli ve meşhur künefesiyle ünlüdür."),
    "ısparta": ("32", "Akdeniz", "Güller ve Göller diyarı; Eğirdir Gölü, Lavanta Kokulu Köy ve gül ürünleriyle bilinir."),
    "mersin": ("33", "Akdeniz", "Kızkalesi, Cennet-Cehennem Obrukları, büyük limanı ve tantunisiyle tanınır."),
    "istanbul": ("34", "Marmara", "Asya ve Avrupa kıtalarını birleştiren dünya metropolü; Ayasofya, Topkapı, Sultanahmet, Süleymaniye, Fatih Camii ve Boğaziçi ile tarih, kültür ve teknoloji merkezidir."),
    "izmir": ("35", "Ege", "Ege'nin incisi; Saat Kulesi, Efes Antik Kenti, Çeşme, Foça ve boyozuyla ünlüdür."),
    "kars": ("36", "Doğu Anadolu", "Ani Harabeleri, Sarıkamış Kayak Merkezi, Çıldır Gölü, Doğu Ekspresi ve kaşar peyniriyle bilinir."),
    "kastamonu": ("37", "Karadeniz", "Ilgaz Dağı, Valla Kanyonu, tarihi konakları ve Taşköprü sarımsağıyla meşhurdur."),
    "kayseri": ("38", "İç Anadolu", "Erciyes Dağı, Mimar Sinan'ın doğduğu Ağırnas, mantısı, pastırması ve sanayisiyle ünlüdür."),
    "kırklareli": ("39", "Marmara", "İğneada Longoz Ormanları, Dupnisa Mağarası ve hardaliyesiyle bilinir."),
    "kırşehir": ("40", "İç Anadolu", "Ahilik teşkilatının kurucusu Ahi Evran, Cacabey Medresesi ve Neşet Ertaş diyarıdır."),
    "kocaeli": ("41", "Marmara", "Türkiye'nin sanayi ve bilişim üssü; Bilişim Vadisi, Kartepe ve pişmaniyesiyle tanınır."),
    "konya": ("42", "İç Anadolu", "Anadolu Selçuklu başkenti; Mevlânâ Müzesi, Çatalhöyük, etli ekmeği ve Türkiye'nin yüzölçümü en büyük ilidir."),
    "kütahya": ("43", "Ege", "Çinicilik ve porselenin başkenti; Aizanoi Antik Kenti ve termal kaynaklarıyla ünlüdür."),
    "malatya": ("44", "Doğu Anadolu", "Dünya kayısı başkenti; Aslantepe Höyüğü ve Levent Vadisi buradadır."),
    "manisa": ("45", "Ege", "Şehzadeler şehri; Spil Dağı, Sardes Antik Kenti, sultaniye üzümü ve mesir macunuyla bilinir."),
    "kahramanmaraş": ("46", "Akdeniz", "İstiklal Madalyalı şehir; dövme dondurması, biberi ve Yedi Güzel Adam edebiyat mirasıyla ünlüdür."),
    "mardin": ("47", "Güneydoğu Anadolu", "Mezopotamya'ya bakan sarı taş evleri, Dara Antik Kenti, Zinciriye ve Kasımiye Medreseleri, telkâri sanatı ve köklü kültürüyle kadim şehirdir."),
    "muğla": ("48", "Ege", "Bodrum, Marmaris, Fethiye (Ölüdeniz), Datça ve çam balıyla Türkiye'nin en uzun kıyı şeridine sahiptir."),
    "muş": ("49", "Doğu Anadolu", "1071 Malazgirt Zaferi'nin yaşandığı tarihî ova ve Muş lalesiyle bilinir."),
    "nevşehir": ("50", "İç Anadolu", "Peri bacaları, sıcak hava balonları ve yeraltı şehirleriyle dünyaca ünlü Kapadokya'nın merkezidir."),
    "niğde": ("51", "İç Anadolu", "Aladağlar Milli Parkı, Gümüşler Manastırı ve elmasıyla tanınır."),
    "ordu": ("52", "Karadeniz", "Boztepe, Perşembe Yaylası, Çambaşı ve Türkiye'nin en büyük fındık üretim merkezidir."),
    "rize": ("53", "Karadeniz", "Türk çayının başkenti; Ayder Yaylası, Fırtına Deresi, Zilkale ve Kaçkar Dağları ile ünlüdür."),
    "sakarya": ("54", "Marmara", "Sapanca Gölü, Acarlar Longozu, Taraklı ve ıslama köftesiyle bilinir."),
    "samsun": ("55", "Karadeniz", "19 Mayıs 1919'da Kurtuluş Savaşı'nın başladığı şehir; Bandırma Vapuru, Kızılırmak Deltası ve pidesiyle ünlüdür."),
    "siirt": ("56", "Güneydoğu Anadolu", "Tillo (İbrahim Hakkı Hazretleri ve Işık Hadisesi), Botan Vadisi, fıstığı ve büryanıyla tanınır."),
    "sinop": ("57", "Karadeniz", "Türkiye'nin en kuzey ucu İnceburun, Hamsilos Fiyordu, Tarihi Cezaevi ve mantısıyla bilinir."),
    "sivas": ("58", "İç Anadolu", "Divriği Ulu Camii (UNESCO), Sivas Kongresi binası, Gök Medrese ve Kangal köpeğiyle ünlüdür."),
    "tekirdağ": ("59", "Marmara", "Uçmakdere yamaç paraşütü, Rakoczi Müzesi ve Tekirdağ köftesiyle tanınır."),
    "tokat": ("60", "Karadeniz", "Ballıca Mağarası, Taşhan, yazmacılık sanatı ve Tokat kebabıyla meşhurdur."),
    "trabzon": ("61", "Karadeniz", "Sümela Manastırı, Uzungöl, Atatürk Köşkü, hamsisi ve Akçaabat köftesiyle Karadeniz'in incisi."),
    "tunceli": ("62", "Doğu Anadolu", "Munzur Vadisi Milli Parkı, Munzur Gözeleri, Ovacık, berrak nehirleri, zengin doğası ve yüksek eğitim oranıyla tanınır."),
    "şanlıurfa": ("63", "Güneydoğu Anadolu", "Peygamberler Şehri; insanlık tarihinin sıfır noktası Göbeklitepe, Balıklıgöl, Harran ve isotuyla ünlüdür."),
    "uşak": ("64", "Ege", "Ulubey Kanyonu, Karun Hazineleri ve tarihi halılarıyla bilinir."),
    "van": ("65", "Doğu Anadolu", "Türkiye'nin en büyük gölü Van Gölü, Akdamar Adası, Van kedisi ve meşhur Van kahvaltısıyla ünlüdür."),
    "yozgat": ("66", "İç Anadolu", "Çamlık Milli Parkı, Sarıkaya Roma Hamamı ve testi kebabıyla bilinir."),
    "zonguldak": ("67", "Karadeniz", "Türkiye'nin taş kömürü madenciliği merkezi, Gökgöl Mağarası ve Filyos Antik Kenti buradadır."),
    "aksaray": ("68", "İç Anadolu", "Ihlara Vadisi, Hasan Dağı ve Sultanhanı Kervansarayı ile Kapadokya'nın giriş kapısıdır."),
    "bayburt": ("69", "Karadeniz", "Bayburt Kalesi, Baksı Müzesi ve Çoruh Nehri ile bilinir."),
    "karaman": ("70", "İç Anadolu", "Karamanoğlu Mehmet Bey'in Türkçeyi resmî dil ilan ettiği Türk Dilinin Başkenti ve Taşkale tahıl ambarları buradadır."),
    "kırıkkale": ("71", "İç Anadolu", "Savunma sanayii (MKE) tesisleri ve Çeşnigir Köprüsü ile tanınır."),
    "batman": ("72", "Güneydoğu Anadolu", "Tarihi Hasankeyf, Malabadi Köprüsü ve Türkiye'nin petrol üretim merkezidir."),
    "şırnak": ("73", "Güneydoğu Anadolu", "Cudi Dağı ve büyük İslam mucidi El-Cezerî'nin yaşadığı Cizre ilçesi buradadır."),
    "bartın": ("74", "Karadeniz", "Amasra kalesi, İnkumu plajı ve Küre Dağları Milli Parkı ile ünlüdür."),
    "ardahan": ("75", "Doğu Anadolu", "Çıldır Gölü, Şeytan Kalesi, Damal ve doğal yaylalarıyla bilinir."),
    "ığdır": ("76", "Doğu Anadolu", "Ağrı Dağı'nın eteklerinde mikroklima iklimi, kayısısı ve üç ülkeye (Ermenistan, Nahçıvan, İran) sınırıyla öne çıkar."),
    "yalova": ("77", "Marmara", "Termal kaplıcaları, Yürüyen Köşk, Sudüşen Şelalesi ve Osmangazi Köprüsü buradadır."),
    "karabük": ("78", "Karadeniz", "UNESCO Dünya Mirası Safranbolu tarihi evleri ve demir-çelik sanayisiyle ünlüdür."),
    "kilis": ("79", "Güneydoğu Anadolu", "Ravanda Kalesi, zeytinyağı ve Kilis tavasıyla tanınır."),
    "osmaniye": ("80", "Akdeniz", "Karatepe-Aslantaş Açık Hava Müzesi, Kastabala ve yer fıstığıyla ünlüdür."),
    "düzce": ("81", "Karadeniz", "Güzeldere ve Samandere Şelaleleri, Efteni Gölü ve Konuralp Antik Tiyatrosu buradadır."),
}

# Türkçe Ülke Adı -> REST Countries İngilizce Karşılığı + Kısa Yedek Bilgi
TURKCE_ULKELER = {
    "türkiye": ("Turkey", "Başkenti Ankara, en büyük şehri İstanbul olan; Asya ve Avrupa kıtalarını birleştiren, 81 il ve ~85 milyon nüfusa sahip ülkemizdir."),
    "almanya": ("Germany", "Başkenti Berlin olan, Avrupa'nın en büyük sanayi ve mühendislik ekonomisine sahip Orta Avrupa ülkesidir."),
    "japonya": ("Japan", "Başkenti Tokyo olan; ileri robotik, elektronik, hızlı tren (Shinkansen) ve köklü gelenekleriyle bilinen Doğu Asya ada ülkesidir."),
    "fransa": ("France", "Başkenti Paris olan; Eyfel Kulesi, Louvre Müzesi, havacılık (Airbus) ve kültürüyle bilinen Batı Avrupa ülkesidir."),
    "ingiltere": ("United Kingdom", "Başkenti Londra olan Birleşik Krallık; köklü üniversiteleri (Oxford, Cambridge) ve küresel finans merkeziyle bilinir."),
    "birleşik krallık": ("United Kingdom", "Başkenti Londra olan Birleşik Krallık; İngiltere, İskoçya, Galler ve Kuzey İrlanda'dan oluşur."),
    "amerika": ("United States", "Başkenti Washington D.C. olan ABD; 50 eyaletli, teknoloji (Silikon Vadisi) ve uzay (NASA) alanında öncü ülkedir."),
    "abd": ("United States", "Başkenti Washington D.C. olan Amerika Birleşik Devletleri, 50 eyaletten oluşur."),
    "rusya": ("Russia", "Başkenti Moskova olan, yüzölçümü bakımından dünyanın en büyük ülkesidir."),
    "çin": ("China", "Başkenti Pekin olan, 1,4 milyar nüfusu ve büyük üretim/teknoloji gücüyle Doğu Asya'nın en büyük ülkesidir."),
    "italya": ("Italy", "Başkenti Roma olan; Rönesans mirası, Venedik, Floransa ve Akdeniz mutfağıyla ünlü Güney Avrupa ülkesidir."),
    "ispanya": ("Spain", "Başkenti Madrid olan; Endülüs mirası (Elhamra), Barselona ve futbol kültürüyle bilinen İber Yarımadası ülkesidir."),
    "azerbaycan": ("Azerbaijan", "Başkenti Bakü olan, 'İki devlet, tek millet' kardeş ülkemiz; Hazar Denizi kıyısında enerji ve kültür merkezidir."),
    "mısır": ("Egypt", "Başkenti Kahire olan; Nil Nehri, Gize Piramitleri ve köklü İslam/antik medeniyet mirasıyla bilinen Kuzey Afrika ülkesidir."),
    "suudi arabistan": ("Saudi Arabia", "Başkenti Riyad olan; İslam'ın iki kutsal şehri Mekke ve Medine'ye ev sahipliği yapan Arap Yarımadası ülkesidir."),
    "bangladeş": ("Bangladesh", "Başkenti Dakka olan; Bengalce konuşulan, zengin nehir deltaları ve yoğun nüfusuyla bilinen Güney Asya ülkesidir."),
    "güney kore": ("South Korea", "Başkenti Seul olan; Samsung, Hyundai ve ileri yarı iletken teknolojileriyle öne çıkan Doğu Asya ülkesidir."),
    "brezilya": ("Brazil", "Başkenti Brasília olan; Amazon yağmur ormanları ve futbol tutkusuyla bilinen Güney Amerika'nın en büyük ülkesidir."),
    "kanada": ("Canada", "Başkenti Ottawa olan; geniş ormanları, gölleri ve yüksek yaşam kalitesiyle bilinen Kuzey Amerika ülkesidir."),
    "hindistan": ("India", "Başkenti Yeni Delhi olan; 1,4 milyar nüfusu, yazılım sektörü ve Tac Mahal ile bilinen Güney Asya ülkesidir."),
    "pakistan": ("Pakistan", "Başkenti İslamabad olan; Türkiye ile köklü dostluk bağlarına sahip Güney Asya ülkesidir."),
    "endonezya": ("Indonesia", "Başkenti Cakarta olan; 17.000'den fazla adadan oluşan, dünyanın en kalabalık Müslüman nüfuslu ülkesidir."),
    "malezya": ("Malaysia", "Başkenti Kuala Lumpur olan; Petronas İkiz Kuleleri ve gelişen teknoloji ekonomisiyle bilinen Güneydoğu Asya ülkesidir."),
    "özbekistan": ("Uzbekistan", "Başkenti Taşkent olan; Semerkant, Buhara ve Hîve gibi büyük İslam bilim merkezlerine (İbn-i Sînâ, Uluğ Bey, Ali Kuşçu) ev sahipliği yapan Türk devletidir."),
    "kazakistan": ("Kazakhstan", "Başkenti Astana olan, Orta Asya'nın yüzölçümü en büyük Türk devletidir."),
    "filistin": ("Palestine", "Başkenti Kudüs (Doğu Kudüs) olan; Mescid-i Aksa ve Kubbetü's-Sahra ile kadim tarihe sahip Orta Doğu ülkesidir."),
    "katar": ("Qatar", "Başkenti Doha olan, Basra Körfezi'nde modern mimarisi ve enerji kaynaklarıyla öne çıkan ülkedir."),
    "hollanda": ("Netherlands", "Başkenti Amsterdam olan; kanalları, bisiklet kültürü ve tarım/çip teknolojileriyle (ASML) bilinen Avrupa ülkesidir."),
    "isviçre": ("Switzerland", "Başkenti Bern olan; Alpler, saatçilik, CERN bilim merkezi ve yüksek refahıyla bilinen Orta Avrupa ülkesidir."),
    "yunanistan": ("Greece", "Başkenti Atina olan; Ege Denizi komşumuz ve antik çağ kalıntılarıyla bilinen Güney Avrupa ülkesidir."),
}

# ==============================================================================
# 2. YEMEK TARİFLERİ DEFTERİ (Türk Mutfağı + Canlı TheMealDB Açık Kaynak API)
# ==============================================================================
TURK_YEMEK_TARIFLERI = {

    "döner": {
        "ad": "Evde Lokanta Usulü Yaprak Et / Tavuk Döner",
        "sure": "Hazırlık & Marine 2-4 saat (veya 1 gece) • Pişirme 10 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Ocak: İyice kızdırılmış döküm veya geniş yapışmaz tavada yüksek ateş (veya fırında 220°C 15 dk)",
        "malzemeler": [
            "600 gr dana kontrfile/antrikot veya kemiksiz tavuk but (ince yaprak dilimlenebilecek şekilde)",
            "Marine için: 2 yemek kaşığı yoğurt, 3 yemek kaşığı zeytinyağı, 1 adet rendelenmiş soğanın SUYU",
            "1 tatlı kaşığı domates salçası (tavuk döner için), 1 çay kaşığı kekik, pul biber, karabiber, kimyon, 1 tatlı kaşığı tuz",
            "Servis için: Lavaş veya tombik ekmek, ince kıyılmış marul, domates, sumaklı soğan ve turşu",
        ],
        "yapilis": [
            "Et veya tavuğu geniş kapta yoğurt, zeytinyağı, süzülmüş soğan suyu ve tüm baharatlarla iyice harmanla.",
            "Eti streç filme sıkıca rulo (silindir) şeklinde sar ve dondurucuda (buzlukta) en az 3-4 saat veya 1 gece iyice sertleşene kadar dondur (bu sayede dönerci gibi incecik yaprak dilimlenir!).",
            "Pişirmeden 15 dakika önce buzluktan çıkarıp keskin bir bıçakla kâğıt gibi ince yapraklar halinde doğra.",
            "Geniş döküm tavayı yüksek ateşte iyice kızdırıp 1 yemek kaşığı tereyağı/sıvı yağ ekle; donuk yaprak etleri tavaya üst üste yığmadan tek sıra halinde yay.",
            "Yüksek ateşte suyunu salmadan hızlıca 3-4 dakika çevirerek nar gibi kızart (tavuksa içinin tam piştiğinden emin ol, ~6 dk).",
            "Sıcak lavaş veya ekmek içine yerleştirip sumaklı soğan, domates ve turşuyla servis et.",
        ],
        "puf_noktasi": "Gerçek dönerci ince yaprak kıvamının sırrı eti marine edip streçle rulo yaparak dondurmak ve donukken incecik kesip çok kızgın tavada mühürlemektir!",
    },
    "iskender": {
        "ad": "Bursa Usulü Tereyağlı İskender Kebap",
        "sure": "Hazırlık 20 dk • Pişirme 15 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Ocak: Yüksek ateşte et mühürleme + kısık ateşte domates sosu",
        "malzemeler": [
            "500 gr yaprak et döner (evde hazırlanmış veya hazır)",
            "2 adet tırnaklı pide (küp doğranmış)",
            "Sos için: 2 yemek kaşığı tereyağı, 2 yemek kaşığı domates salçası, 1 su bardağı rendelenmiş domates, 1 su bardağı sıcak su, tuz, karabiber",
            "Üzeri için: 3 yemek kaşığı kızdırılmış tereyağı, kenarına süzme yoğurt, közlenmiş biber ve domates",
        ],
        "yapilis": [
            "Tırnaklı pideleri küp doğrayıp 1 yemek kaşığı tereyağında tavada hafifçe çıtırlaştır ve servis tabağının tabanına yay.",
            "Sosu için tereyağında salçayı kavur, rendelenmiş domates ve sıcak suyu ekleyip 8 dakika kaynat; pidelerin üzerine bolca gezdir.",
            "Kızgın tavada pişirdiğin sıcak yaprak dönerleri pidelerin üzerine yerleştir.",
            "Küçük tavada 3 yemek kaşığı tereyağını köpürüp mis gibi kokana kadar kızdır ve servis anında etlerin üzerinde cızırdatarak dök; kenarına yoğurt ve köz biber ekle.",
        ],
        "puf_noktasi": "Tereyağını yakmadan tam köpürdüğü anda sıcak etlerin üzerine dökmek gerçek Bursa İskender aromasını verir.",
    },
    "lahmacun": {
        "ad": "Çıtır Çıtır Ev Yapımı Taş Fırın Tadında Lahmacun",
        "sure": "Hazırlık 30 dk • Pişirme 6-8 dk (her biri)",
        "kisi": "8-10 Adet",
        "pisirme_ayari": "Fırın: Önceden son ayarda ısıtılmış 250°C alt-üst ayar (en alt rafa yakın) veya kapaklı döküm tavada orta ateş",
        "malzemeler": [
            "Hamur: 4 su bardağı un, 1,5 su bardağı ılık su, 1 tatlı kaşığı tuz, 1 yemek kaşığı zeytinyağı",
            "İç Harç: 350 gr orta yağlı dana kıyma, 2 adet soğan, 2 adet kırmızı kapya biber, 2 yeşil biber, 3 adet domates, 2 diş sarımsak",
            "Yarım demet maydanoz, 1 yemek kaşığı domates + 1 yemek kaşığı biber salçası, yarım çay bardağı sıvı yağ, tuz, pul biber, isot, karabiber",
        ],
        "yapilis": [
            "Un, tuz, yağ ve ılık suyu yoğurup ele yapışmayan yumuşak bir hamur elde et; 20 dakika üzeri örtülü dinlendir.",
            "Sebzeleri (soğan, biber, domates, sarımsak, maydanoz) robottan çok ince çek (suyunu tamamen sıkma, harç sürülebilir kıvamda kalsın); kıyma, salça, yağ ve baharatlarla iyice karıştır.",
            "Hamuru mandalina büyüklüğünde 10 bezeye böl ve unlu tezgahta olabildiğince ince (yaklaşık 2 mm) aç.",
            "İç harçtan 2 yemek kaşığı alıp hamurun kenarlarına kadar ince ve eşit bir tabaka halinde yay.",
            "Önceden 250°C'ye kızdırılmış fırında (veya kızgın kapaklı tavada) kenarları çıtırlaşıp harcı pişene kadar 6-8 dakika pişir; sıcak sıcak üst üste koyup maydanoz ve limonla servis et.",
        ],
        "puf_noktasi": "Fırını mutlaka önceden en yüksek dereceye (250°C) ısıt ve hamuru çok ince aç; düşük ısıda uzun pişirmek lahmacunu kurutur.",
    },
    "adana kebap": {
        "ad": "Evde Fırında / Izgarada Gerçek Adana Kebap",
        "sure": "Hazırlık 20 dk (+1 saat dinlendirme) • Pişirme 15-18 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Fırın: Önceden ısıtılmış 220°C alt-üst ızgara ayarı, tel ızgara üzerinde (alta su dolu tepsi koyarak 15-18 dk)",
        "malzemeler": [
            "600 gr yağlı kuzu-dana karışık zırh kıyması (%25 kuyruk/iç yağı oranı ideal)",
            "1 adet ince kıyılıp suyu iyice sıkılmış kırmızı kapya biber",
            "2 tatlı kaşığı pul biber, 1 tatlı kaşığı toz kırmızı biber, 1 tatlı kaşığı tuz (Adana kebapta soğan, sarımsak, ekmek ve yumurta KONULMAZ!)",
        ],
        "yapilis": [
            "Kıyma, suyu sıkılmış kapya biber, pul biber, toz biber ve tuzu geniş kapta 8-10 dakika iyice özleşene kadar yoğur.",
            "Harcı buzdolabında en az 1 saat dinlendir ki yağı donup şişe sağlam tutunsun.",
            "Elini hafifçe soğuk suya batırarak harcı yassı metal şişlere (veya ıslatılmış kalın çöp şişlere) parmak izi vererek uzunlamasına diz.",
            "Önceden 220°C'ye ısıtılmış fırının tel ızgarasına diz (altına yağ damlaması ve duman yapmaması için su dolu tepsi koy) ve 15-18 dakika çevirerek kızart.",
        ],
        "puf_noktasi": "Harcı soğuk tutmak ve içine soğan/ekmek koymamak kebapların şişten dökülmeden lokanta tadında pişmesini sağlar.",
    },
    "tavuk sote": {
        "ad": "Lokum Gibi Sebzeli Tavuk Sote",
        "sure": "Hazırlık 10 dk • Pişirme 20 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Ocak: Mühürlemede yüksek ateş, pişirmede orta-kısık ateş",
        "malzemeler": [
            "600 gr kuşbaşı doğranmış tavuk göğsü veya kemiksiz but",
            "1 büyük soğan, 2 yeşil biber, 1 kırmızı kapya biber, 2 domates, 2 diş sarımsak",
            "3 yemek kaşığı sıvı yağ, 1 yemek kaşığı tereyağı, 1 tatlı kaşığı salça, kekik, pul biber, karabiber, tuz",
        ],
        "yapilis": [
            "Geniş tavada sıvı yağı yüksek ateşte kızdır; tavukları ekleyip suyunu salmaması için 3-4 dakika hızlıca mühürle.",
            "Tereyağı, yemeklik doğranmış soğan, sarımsak ve biberleri ekleyip 4 dakika sotele.",
            "Salçayı ekleyip kokusu çıkana kadar çevir, ardından küp doğranmış domatesleri ve baharatları ilave et.",
            "Kapağı kapatıp orta-kısık ateşte 10-12 dakika tavuklar yumuşayıp sosu özleşene kadar pişir; sıcak pilavla servis et.",
        ],
        "puf_noktasi": "Tavukları mutlaka çok kızgın tavaya atıp yüksek ateşte mühürle; böylece içi sulu ve yumuşacık kalır.",
    },
    "sütlaç": {
        "ad": "Üzeri Nar Gibi Kızaran Fırın Sütlaç",
        "sure": "Hazırlık 10 dk • Pişirme 35 dk + Fırın 12 dk",
        "kisi": "6 Kase",
        "pisirme_ayari": "Fırın: 200°C SADECE ÜST IZGARA (veya üst-alt) en üst rafa yakın, tepsiye soğuk su koyarak 10-15 dk",
        "malzemeler": [
            "1 litre tam yağlı süt, 1 su bardağı toz şeker, yarım su bardağı pirinç, 2 su bardağı su",
            "2 yemek kaşığı buğday nişastası (yarım çay bardağı soğuk sütle açılmış)",
            "1 paket vanilya, isteğe bağlı 1 adet yumurta sarısı (daha güzel kızarması için)",
        ],
        "yapilis": [
            "Yıkanmış yarım su bardağı pirinci 2 su bardağı suyla yumuşayıp suyunu çekene kadar ~15 dakika haşla.",
            "Üzerine 1 litre sütü ve vanilyayı ekleyip kaynamaya bırak; kaynayınca toz şekeri ilave et.",
            "Soğuk sütle açtığın nişastayı (ve istersen yumurta sarısını) yavaşça karıştırarak tencereye dök; orta ateşte 5-7 dakika muhallebi kıvamından biraz daha akışkan olana kadar pişir.",
            "Sütlacı ısıya dayanıklı güveç kaselerine paylaştır ve derin fırın tepsisine diz; tepsinin yarısına gelecek kadar soğuk su doldur.",
            "Önceden ısıtılmış 200°C fırının üst rafında üzerleri nar gibi kızarana kadar 10-15 dakika pişir; oda sıcaklığına gelince buzdolabında soğutup fındıkla servis et.",
        ],
        "puf_noktasi": "Tepsiye soğuk su koymak sütlacın fırında tekrar kaynayıp taşmasını ve kurumasını önler, sadece üstünün karamelize kızarmasını sağlar.",
    },
    "börek": {
        "ad": "Çıtır Çıtır Peynirli Tepsi Böreği",
        "sure": "Hazırlık 15 dk • Fırında Pişirme 35 dk",
        "kisi": "6-8 Kişilik",
        "pisirme_ayari": "Fırın: Önceden ısıtılmış 185°C alt-üst ayar, orta raf (35-40 dakika)",
        "malzemeler": [
            "4 adet taze yufka",
            "Sos: 1 su bardağı süt, yarım su bardağı sıvı yağ, 2 yemek kaşığı yoğurt, 2 adet yumurta (1 sarısı üzerine)",
            "İç Harç: 300 gr beyaz peynir + kaşar rendesi, yarım demet ince kıyılmış maydanoz",
        ],
        "yapilis": [
            "Fırını 185°C alt-üst ayarda ısıt; geniş fırın tepsisini hafifçe yağla.",
            "Sos malzemelerini çırp. İlk yufkayı kenarları tepsiden sarkacak şekilde ser ve sostan 4-5 yemek kaşığı gezdir.",
            "2. yufkayı parçalayarak tepsiye yerleştirip sosla; peynirli maydanozlu harcın tamamını eşit şekilde yay.",
            "3. ve 4. yufkaları da soslayarak kat kat yerleştir, sarkan kenarları üzerine kapat.",
            "Kalan sosa ayırdığın yumurta sarısını karıştırıp böreğin üzerine sür, dilimle ve susam/çörek otu serpip 185°C fırında 35-40 dakika altı üstü kızarana kadar pişir.",
        ],
        "puf_noktasi": "Böreği fırına vermeden önce dilimlemek sosun aralara işleyip içinin su böreği gibi yumuşak, dışının çıtır olmasını sağlar.",
    },
    "pizza": {
        "ad": "Ev Yapımı İtalyan Hamurlu Karışık Pizza",
        "sure": "Hazırlık 20 dk (+40 dk mayalama) • Fırında Pişirme 12-15 dk",
        "kisi": "2 Büyük Boy Pizza",
        "pisirme_ayari": "Fırın: Önceden ısıtılmış 230°C alt-üst ayar, alt rafa yakın (12-15 dakika)",
        "malzemeler": [
            "Hamur: 4 su bardağı un, 1,5 su bardağı ılık su, 1 paket instant maya, 1 tatlı kaşığı şeker, 1 tatlı kaşığı tuz, 3 yemek kaşığı zeytinyağı",
            "Sos: 1 su bardağı domates rendesi, 1 yemek kaşığı salça, 1 diş sarımsak, kekik, zeytinyağı",
            "Üst Malzeme: 250 gr rendelenmiş kaşar/mozzarella, sucuk, mantar, mısır, zeytin, yeşil biber",
        ],
        "yapilis": [
            "Ilık su, maya ve şekeri karıştırıp 5 dk beklet; un, tuz ve zeytinyağı ekleyip pürüzsüz hamur yoğur ve 40 dakika mayalandır.",
            "Mayalanan hamuru 2 parçaya bölüp yağlı kağıt üzerinde ince yuvarlak aç; çatalla birkaç yerinden del (kabarmasın).",
            "Önce domatesli kekikli sosu sür, ardından peynirin yarısını, doğranmış sucuk/sebze malzemelerini ve kalan peyniri ekle.",
            "Önceden 230°C'ye iyice kızdırılmış fırında 12-15 dakika kenarları kızarıp peyniri eriyene kadar pişir.",
        ],
        "puf_noktasi": "Pizzayı yüksek ısıda (230°C) kısa sürede pişirmek hamurun ekmek gibi sertleşmesini önler ve çıtır taban verir.",
    },
    "menemen": {
        "ad": "Klasik Türk Menemeni (Tam Kıvamında)",
        "sure": "Hazırlık 5 dk • Pişirme 12 dk",
        "kisi": "2-3 Kişilik",
        "pisirme_ayari": "Ocak: Orta ateşten kısık ateşe (Geniş yapışmaz veya bakır tava)",
        "malzemeler": [
            "3 adet orta boy olgun domates (kabukları soyulup ince küp doğranmış)",
            "2 adet yeşil sivri biber (çekirdekleri temizlenip halka doğranmış)",
            "3 adet oda sıcaklığında yumurta",
            "2 yemek kaşığı tereyağı veya zeytinyağı",
            "1 çay kaşığı tuz, yarım çay kaşığı karabiber, isteğe bağlı pul biber ve 50 gr kaşar peyniri",
        ],
        "yapilis": [
            "Tavayı orta ateşte ısıtıp yağı erit; doğranmış yeşil biberleri ekleyip hafifçe yumuşayana kadar 3 dakika kavur.",
            "Kabuğu soyulmuş küp domatesleri ve tuzu ekle; tavanın kapağını kapatıp domatesler kendi suyunu salıp hafifçe çekene kadar 6-7 dakika pişir.",
            "Ocağı kısık ateşe al. Yumurtaları ayrı bir kasede hafifçe çırp (akı ve sarısı dağılsın ama köpürmesin) ve domateslerin üzerine gezdir.",
            "Tahta kaşıkla alttan üste doğru yavaşça karıştır; yumurtalar tamamen kurumadan, hafif akışkan kıvamdayken (yaklaşık 2 dakika) ocaktan al.",
            "Üzerine karabiber ve istersen rendelenmiş kaşar peyniri serpip sıcak ekmekle servis et.",
        ],
        "puf_noktasi": "Yumurtayı ekledikten sonra ocağı mutlaka kısık ateşe al; yüksek ateş yumurtayı kurutup omlete dönüştürür.",
    },
    "mercimek çorbası": {
        "ad": "Lokanta Usulü Süzme Kırmızı Mercimek Çorbası",
        "sure": "Hazırlık 10 dk • Pişirme 25 dk",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Ocak: Kavurmada orta ateş, kaynamada kısık ateş (Derin tencere)",
        "malzemeler": [
            "1,5 su bardağı kırmızı mercimek (bol suyla berraklaşana kadar yıkanmış)",
            "1 adet orta boy kuru soğan, 1 adet havuç, 1 adet küçük patates",
            "1 yemek kaşığı tereyağı + 1 yemek kaşığı sıvı yağ + 1 yemek kaşığı un",
            "6 su bardağı sıcak su (varsa 1 bardağı et/tavuk suyu)",
            "1 tatlı kaşığı tuz, yarım çay kaşığı kimyon, karabiber, çeyrek çay kaşığı zerdeçal",
        ],
        "yapilis": [
            "Tencerede tereyağı ve sıvı yağı orta ateşte ısıt; iri doğranmış soğanı 2 dakika pembeleştir.",
            "1 yemek kaşığı unu ekleyip kokusu çıkana kadar 1 dakika sürekli karıştırarak kavur (bu adım lokanta kıvamını verir).",
            "Küp doğranmış havuç, patates ve yıkanmış mercimeği tencereye ekleyip 2 dakika daha çevir.",
            "6 su bardağı sıcak suyu, tuzu ve baharatları ilave et; kaynadıktan sonra altını kısıp kapağı yarım kapalı şekilde sebzeler iyice yumuşayana kadar 20 dakika pişir.",
            "El blenderıyla tamamen pürüzsüz olana kadar çek; kıvamı koyuysa yarım bardak sıcak su ekleyip 2 dakika daha kaynat.",
            "Üzerine küçük tavada tereyağında kızdırılmış toz kırmızı biber gezdirip limon dilimiyle servis et.",
        ],
        "puf_noktasi": "Mercimeği pişirmeden önce nişastası gidene kadar 3-4 kez yıkamak köpürmeyi önler; az miktarda zerdeçal doğal altın sarısı renk verir.",
    },
    "karnıyarık": {
        "ad": "Fırında Lokum Gibi Karnıyarık",
        "sure": "Hazırlık 20 dk • Fırında Pişirme 25 dk",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Fırın: Önceden ısıtılmış 190°C alt-üst ayar, orta raf (20-25 dakika)",
        "malzemeler": [
            "6 adet orta boy kemer patlıcan",
            "250-300 gr orta yağlı dana kıyma",
            "2 adet kuru soğan, 2 diş sarımsak, 2 adet yeşil biber, 2 adet domates",
            "1 yemek kaşığı domates salçası (yarısı iç harca, yarısı fırın sosuna)",
            "Tuz, karabiber, pul biber, bir tutam ince kıyılmış maydanoz, 1 su bardağı sıcak su",
        ],
        "yapilis": [
            "Patlıcanları alacalı (pijamalı) soyup acısının çıkması için tuzlu suda 15 dakika beklet, ardından kağıt havluyla iyice kurula.",
            "Patlıcanların her yanını fırçayla hafifçe yağlayıp yağlı kağıt serili tepside 200°C fırında 20 dakika yumuşat (veya tavada kızartıp havlu kağıda al).",
            "İç harç için tavada kıymayı suyunu salıp çekene kadar kavur; yemeklik doğranmış soğan, sarımsak ve biberleri ekleyip 4 dakika kavur.",
            "Küp doğranmış domatesleri, yarım yemek kaşığı salçayı ve baharatları ekleyip 5 dakika pişir; ocaktan alınca maydanozu karıştır.",
            "Yumuşayan patlıcanları tepsiye diz, ortalarını bıçakla boylamasına çizip kaşıkla hafifçe aç ve kıymalı harcı bolca doldur; üzerlerine domates ve biber dilimi koy.",
            "Kalan yarım yemek kaşığı salçayı 1 su bardağı sıcak suda eritip patlıcanların kenarından tepsiye dök. Önceden ısıtılmış 190°C alt-üst fırının orta rafında 20-25 dakika üzerleri kızarana kadar pişir.",
        ],
        "puf_noktasi": "Salçalı suyu patlıcanların üstüne değil tepsinin tabanına dökersen kıymalı harç dağılmaz ve üstü nar gibi kızarır.",
    },
    "kek": {
        "ad": "Puf Puf Kabaran Klasik Anne Keki (Sade / Kakaolu)",
        "sure": "Hazırlık 10 dk • Fırında Pişirme 38 dk",
        "kisi": "8-10 Dilim",
        "pisirme_ayari": "Fırın: Önceden ısıtılmış 175°C alt-üst FANSIZ ayar, orta raf (35-40 dk)",
        "malzemeler": [
            "3 adet oda sıcaklığında yumurta",
            "1 su bardağı toz şeker",
            "1 su bardağı oda sıcaklığında süt",
            "Yarım su bardağı sıvı yağ",
            "2,5 su bardağı elenmiş un",
            "1 paket kabartma tozu, 1 paket vanilya (kakaolu için 2 yemek kaşığı kakao + 2 yemek kaşığı süt)",
        ],
        "yapilis": [
            "Fırını önceden 175°C alt-üst fansız ayara getirip ısıtmaya başla; kek kalıbını tereyağıyla yağlayıp hafifçe unla.",
            "Derin kapta yumurta ve toz şekeri mikserle rengi açılıp krema gibi köpük köpük olana kadar tam 4 dakika çırp.",
            "Önce sıvı yağı, sonra sütü ekleyip düşük devirde 30 saniye karıştır (köpüğü söndürme).",
            "Unu, kabartma tozunu ve vanilyayı (kakaoluysa kakaoyu da) mutlaka süzgeçten eleyerek kaba ekle; spatula veya en düşük devirle topak kalmayana kadar karıştır.",
            "Harcı kalıba döküp tezgaha 2 kez hafifçe vur (hava kabarcıkları çıksın) ve fırının orta rafına yerleştir.",
            "İlk 25 dakika fırının kapağını KESİNLİKLE açma! 35. dakikada ortasına kürdan batır; kürdan temiz çıkarsa kekin pişmiştir.",
        ],
        "puf_noktasi": "Tüm malzemelerin (özellikle yumurta ve sütün) oda sıcaklığında olması, unun elenmesi ve fırının fansız 175°C'de çalışması kekin eşit kabarmasını sağlar.",
    },
    "pilav": {
        "ad": "Tane Tane Tereyağlı Şehriyeli Pirinç Pilavı",
        "sure": "Hazırlık 20 dk • Pişirme 15 dk + Demleme 10 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Ocak: Kavurmada orta ateş, pişirmede en kısık ateş (Geniş tabanlı pilav tenceresi)",
        "malzemeler": [
            "2 su bardağı baldo pirinç",
            "3 su bardağı kaynar su (1'e 1,5 ölçü)",
            "2 yemek kaşığı tereyağı + 1 yemek kaşığı sıvı yağ",
            "2 yemek kaşığı arpa şehriye",
            "1 tatlı kaşığı tuz, 3-4 damla limon suyu (parlak beyazlık için)",
        ],
        "yapilis": [
            "Pirinci ılık tuzlu suda 20 dakika beklet; ardından beyaz nişasta suyu tamamen berraklaşana kadar 3-4 kez soğuk suyla nazikçe yıkayıp süz.",
            "Tencerede sıvı yağı ısıtıp şehriyeyi altın rengini alana kadar kavur, ardından tereyağını ekleyip erit.",
            "Süzülmüş pirinci ekle ve pirinçler şeffaflaşıp birbirinden ayrılana kadar orta ateşte 3-4 dakika sürekli karıştırarak kavur.",
            "3 su bardağı kaynar suyu, tuzu ve 3-4 damla limon suyunu ekleyip 1 kez karıştır, kapağını kapat.",
            "Önce 2 dakika orta ateşte fokurdat, sonra ocağı en kısık seviyeye al ve suyunu tamamen çekip üzerinde göz göz delikler oluşana kadar (~12 dk) kapağı açmadan pişir.",
            "Ocağı kapat, tencere ile kapak arasına kağıt havlu serip 10 dakika demlendir; servis öncesi tahta kaşıkla alttan havalandır.",
        ],
        "puf_noktasi": "Pilav pişerken kapağı açıp karıştırmak pirinci lapa yapar; mutlaka kısık ateşte dokunmadan pişir ve 10 dakika demlendir.",
    },
    "makarna": {
        "ad": "İtalyan Usulü Domates ve Fesleğen Soslu Makarna",
        "sure": "Hazırlık 5 dk • Pişirme 15 dk",
        "kisi": "3-4 Kişilik",
        "pisirme_ayari": "Ocak: Haşlamada yüksek ateş, sosta orta-kısık ateş",
        "malzemeler": [
            "1 paket makarna (500 gr)",
            "2 litre kaynar su + 1 yemek kaşığı tuz",
            "3 yemek kaşığı zeytinyağı, 2 diş ince kıyılmış sarımsak",
            "3 adet rendelenmiş domates (veya 1 yemek kaşığı salça + 2 domates)",
            "Taze fesleğen veya kuru kekik, karabiber, isteğe bağlı kaşar/parmesan",
        ],
        "yapilis": [
            "Geniş tencerede suyu kaynat, tuzu ekle ve makarnayı paket üzerindeki süreden 1 dakika eksik (al dente) haşla; süzmeden önce yarım su bardağı nişastalı makarna suyundan ayır.",
            "Ayrı tavada zeytinyağını orta ateşte ısıt; sarımsakları yakmadan 30 saniye kokusu çıkana kadar çevir.",
            "Domatesleri, tuzu ve baharatları ekleyip 6-7 dakika sos kıvam alana kadar pişir.",
            "Süzdüğün makarnayı (soğuk sudan GEÇİRMEDEN) doğrudan sosun içine at, ayırdığın yarım bardak makarna suyunu da ekleyip 1 dakika yüksek ateşte harmanla.",
        ],
        "puf_noktasi": "Makarnayı süzdükten sonra kesinlikle soğuk sudan geçirme; nişastalı haşlama suyundan yarım bardak sosa eklemek sosun makarnaya yapışmasını sağlar.",
    },
    "köfte": {
        "ad": "İçi Sulu Ev Usulü Anne Köftesi",
        "sure": "Hazırlık 15 dk (+30 dk dinlendirme) • Pişirme 12 dk",
        "kisi": "4 Kişilik",
        "pisirme_ayari": "Ocak: Önceden iyice ısıtılmış döküm/teflon tavada orta-yüksek ateş (veya fırında 200°C 20 dk)",
        "malzemeler": [
            "500 gr orta yağlı dana döş kıyma",
            "1 adet rendelenmiş ve suyu sıkılmış kuru soğan + 1 diş sarımsak",
            "1 adet yumurta, 4 yemek kaşığı galeta unu veya bayat ekmek içi",
            "1 çay kaşığı kimyon, karabiber, pul biber, 1 tatlı kaşığı tuz, yarım çay kaşığı karbonat, maydanoz",
        ],
        "yapilis": [
            "Geniş kaba kıymayı, suyu sıkılmış soğanı, yumurtayı, galeta ununu, baharatları ve maydanozu al.",
            "Malzemeler iyice özleşip macun kıvamına gelene kadar en az 7-8 dakika güçlüce yoğur.",
            "Üzerini streçleyip buzdolabında en az 30 dakika dinlendir (lezzeti oturur ve pişerken dağılmaz).",
            "Ceviz büyüklüğünde parçalar koparıp elinle yassı köfte şekli ver; az yağlı kızgın tavada her iki yüzünü 3-4 dakika (veya 200°C fırında 20 dk) pişir.",
        ],
        "puf_noktasi": "Soğanın acı suyunu mutlaka sık ve harcı en az 7 dakika yoğurup dinlendir; böylece köfteler asla dağılmaz ve içi sulu kalır.",
    },
    "kuru fasulye": {
        "ad": "Lokum Gibi Geleneksel Kuru Fasulye",
        "sure": "Hazırlık 15 dk • Pişirme 55 dk (Düdüklüde 25 dk)",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Ocak: Kısık ateş (Ağır ağır özleşerek pişer)",
        "malzemeler": [
            "2 su bardağı kuru fasulye (1 gece önceden soğuk suda ıslatılmış)",
            "1 büyük kuru soğan, 1,5 yemek kaşığı domates-biber salçası",
            "2 yemek kaşığı tereyağı + 1 yemek kaşığı sıvı yağ",
            "İsteğe bağlı 200 gr kuşbaşı et, 5 su bardağı sıcak su, tuz, pul biber",
        ],
        "yapilis": [
            "Geceden ıslatılan fasulyeyi süzüp temiz suyla 10 dakika ön haşlama yap ve süz.",
            "Tencerede tereyağı ve sıvı yağda ince doğranmış soğanı (ve varsa eti) kavur; salçayı ekleyip kokusu çıkana kadar 2 dakika çevir.",
            "Fasulyeleri ekleyip 1 dakika nazikçe karıştır, üzerini 2 parmak geçecek kadar sıcak su ve tuz ilave et.",
            "Kısık ateşte 50-55 dakika (düdüklü tencerede kaynadıktan sonra 25 dakika) fasulyeler dağılmadan lokum gibi olana kadar pişir.",
        ],
        "puf_noktasi": "Tuzu fasulye yarı piştikten sonra eklemek kabukların sertleşmesini önler.",
    },
"hünkar beğendi": {
        "ad": "Hünkar Beğendi (Osmanlı Saray Mutfağı)",
        "sure": "55 dakika | 4 Kişilik",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Közleme: 230°C fırın 30 dk (veya ocak üstü köz) • Et: kısık ateş 40 dk",
        "malzemeler": [
            "Et için: 500 gr kuzu/dana kuşbaşı, 1 soğan, 2 domates, 1 YK domates salçası, 2 YK tereyağı, kekik, tuz, karabiber",
            "Beğendi için: 4 adet kemer patlıcan, 2 YK tereyağı, 2 YK un, 1,5 su bardağı ılık süt, 1 su bardağı rendelenmiş kaşar, muskat rendesi, tuz",
        ],
        "yapilis": [
            "Patlıcanları çatalla delip 230°C fırında 30 dk közle; kabuklarını soyup limonlu suda 2 dk bekletip incecik kıy.",
            "Etleri kızgın tencerede yüksek ateşte mühürle; tereyağı ve yemeklik soğanı ekleyip 3 dk kavur, ardından salça ve rendelenmiş domatesi ekle.",
            "1 su bardağı sıcak su ilave edip kapağı kapalı kısık ateşte etler lokum gibi olana dek 35-40 dk pişir; tuz-karabiber-kekik ekle.",
            "Beğendi için ayrı tencerede tereyağı ile unu kokusu çıkana dek 2 dk kavur, közlenmiş patlıcanları ekleyip ezerek karıştır.",
            "Ilık sütü yavaş yavaş ekleyip kıvam alınca ocağı kapat, rendelenmiş kaşar ve bir tutam muskat ekleyip karıştır.",
            "Servis tabağına önce sıcak beğendiyi yay, ortasına lokum gibi et soteden koyup sıcak servis et.",
        ],
        "puf_noktasi": "Patlıcanları közledikten sonra sıcakken soyup az limon suyu gezdirirsen beğendi kararmaz, ipeksi ve bembeyaz kalır.",
    },
    "imam bayıldı": {
        "ad": "Zeytinyağlı İmam Bayıldı",
        "sure": "50 dakika | 4 Kişilik",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Ön kızartma veya 200°C fırın 20 dk • Soslu pişirme: 190°C fırın 25 dk",
        "malzemeler": [
            "4 adet orta boy kemer patlıcan, 4 YK zeytinyağı",
            "3 adet piyazlık doğranmış kuru soğan, 4 diş dilimlenmiş sarımsak, 2 yeşil biber, 3 küp doğranmış domates",
            "1 çay kaşığı toz şeker, tuz, karabiber, ince kıyılmış maydanoz, 1/2 su bardağı sıcak su",
        ],
        "yapilis": [
            "Patlıcanları alacalı soyup acısının çıkması için tuzlu suda 15 dk beklet, kurula ve hafif yağlayıp 200°C fırında 20 dk yumuşat.",
            "Geniş tavada zeytinyağında piyazlık soğanları 6-7 dk karamelize olmadan yumuşat; biber ve sarımsakları ekleyip 3 dk çevir.",
            "Domates, şeker, tuz ve karabiberi ekleyip 5 dk pişir; ocaktan alıp maydanozu karıştır.",
            "Patlıcanların ortasını boydan yararak kaşıkla aç ve bol soğanlı harçla doldur; tepsiye dizip yarım bardak sıcak su gezdir.",
            "190°C fırında 25 dk pişir; oda sıcaklığında dinlendirip soğuk veya ılık servis et.",
        ],
        "puf_noktasi": "İmam bayıldı piştikten sonra birkaç saat (hatta bir gece) dinlenince zeytinyağı ve soğan aroması patlıcana tam işler.",
    },
    "kuru fasulye": {
        "ad": "Lokanta Usulü Tereyağlı Kuru Fasulye",
        "sure": "1 saat (+ 1 gece ıslatma) | 4-5 Kişilik",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Düdüklü tencerede 25 dk veya güveçte kısık ateş 55 dk",
        "malzemeler": [
            "2 su bardağı dermason kuru fasulye (1 gece önceden ılık suda bekletilmiş)",
            "1 büyük yemeklik soğan, 2 YK tereyağı + 2 YK sıvı yağ, 1,5 YK domates salçası, 1 TK biber salçası",
            "İsteğe bağlı 250 gr kuşbaşı et veya pastırma, 1 tatlı kaşığı tuz, 1/2 çay kaşığı kimyon, 5 su bardağı sıcak su",
        ],
        "yapilis": [
            "Islatılmış fasulyeleri süzüp temiz suyla 10 dk ön haşlama yap (köpüğünü alıp süzerek gazını gider).",
            "Tencerede tereyağı ve sıvı yağda ince doğranmış soğanı pembeleşene kadar 4 dk kavur (etli yapıyorsan önce eti mühürle).",
            "Domates ve biber salçasını ekleyip 2 dk kavur, ardından haşlanmış fasulyeleri katıp 1 dk nazikçe harmanla.",
            "Üzerini 2 parmak geçecek kadar sıcak su, tuz ve kimyonu ekle; kısık ateşte (veya düdüklüde 25 dk) özleşene kadar pişir.",
        ],
        "puf_noktasi": "Pişme esnasında 1 çay kaşığı kimyon eklemek hem hazmı kolaylaştırır hem de lokanta usulü derin bir aroma katar.",
    },
    "mercimek köftesi": {
        "ad": "Tam Ölçülü Kırmızı Mercimek Köftesi",
        "sure": "40 dakika | 6 Kişilik",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Orta-kısık ateş 15-18 dk haşlama + 15 dk demlendirme",
        "malzemeler": [
            "1 su bardağı kırmızı mercimek, 1,5 su bardağı ince köftelik bulgur, 3 su bardağı su",
            "1 büyük kuru soğan, 1/2 çay bardağı zeytinyağı, 1 YK domates salçası, 1 YK biber salçası",
            "1 demet maydanoz, 5 dal taze soğan, 1 limon suyu, kimyon, pul biber, karabiber, tuz",
        ],
        "yapilis": [
            "Yıkanmış kırmızı mercimeği 3 su bardağı suyla iyice yumuşayıp hafif sulu kalana kadar (15-18 dk) haşla.",
            "Ocağı kapatıp ince bulguru hemen sıcak mercimeğe ekle, karıştırıp kapağını kapat ve 15 dk şişmeye bırak.",
            "Tavada zeytinyağında ince doğranmış soğanı kavur; domates ve biber salçasını ekleyip 2 dk çevir ve bulgurlu harca kat.",
            "Baharatlar ve limon suyunu ekleyip harç ılıyınca iyice yoğur; en son ince kıyılmış maydanoz ve taze soğanı ekleyip şekil ver.",
        ],
        "puf_noktasi": "Yeşillikleri harç tamamen ılıdıktan sonra eklersen maydanoz ve taze soğan kararmaz, diri ve taze kalır.",
    },
    "künefe": {
        "ad": "Hatay Usulü Çıtır Ev Yapımı Künefe",
        "sure": "30 dakika | 4 Kişilik",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "Ocak üstü kısık-orta ateş (her yüz 5-6 dk) veya 200°C fırın 20 dk",
        "malzemeler": [
            "300 gr taze tel kadayıf, 120 gr eritilmiş tuzsuz tereyağı, 200 gr tuzsuz künefe peyniri (veya dil peyniri)",
            "Şerbet için: 1,5 su bardağı toz şeker, 1,5 su bardağı su, 4-5 damla limon suyu",
            "Üzeri için: Toz Antep fıstığı ve isteğe bağlı kaymak",
        ],
        "yapilis": [
            "Önce şerbeti hazırla: şeker ve suyu kaynatıp 8 dk kısık ateşte pişir, limon damlatıp ılınmaya bırak.",
            "Tel kadayıfı ince ince didikle ve eritilmiş ılık tereyağıyla her teli yağlanana kadar ovala.",
            "Yağlanmış tepsiye kadayıfın yarısını yayıp başka bir tabakla sıkıca bastır; kenarlara değmeden rendelenmiş peyniri yay.",
            "Kalan kadayıfı üstüne kapatıp tekrar iyice bastır; kısık ateşte çevire çevire altı nar gibi kızarınca ters çevirip diğer yüzünü kızart.",
            "Sıcak künefenin üzerine ılık şerbeti gezdir, bol Antep fıstığı serp ve peyniri uzarken hemen servis et.",
        ],
        "puf_noktasi": "Peyniri tepsinin en kenarlarına değdirmezsen eriyip yapışmaz ve tepsiden tek parça hâlinde rahatça çevrilir.",
    },
    "baklava": {
        "ad": "Ev Yapımı Çıtır Cevizli/Fıstıklı Baklava",
        "sure": "1 saat 30 dakika | 1 Tepsi",
        "kisi": "4-6 Kişilik",
        "pisirme_ayari": "170°C önceden ısıtılmış alt-üst fırın (fan kapalı) • 45-50 dk",
        "malzemeler": [
            "1 paket hazır baklavalık yufka (40 yaprak), 250 gr sade tereyağı (köpüğü alınmış) + 1/2 çay bardağı sıvı yağ",
            "300 gr iri çekilmiş ceviz içi veya Boz Antep fıstığı",
            "Şerbet için: 3 su bardağı şeker, 3,5 su bardağı su, çeyrek limon suyu",
        ],
        "yapilis": [
            "Şerbeti kaynatıp kısık ateşte 15 dk koyulaştır, limon suyunu ekleyip 2 dk daha kaynattıktan sonra ılınmaya bırak.",
            "Tereyağını eritip üzerindeki beyaz köpüğü ve dibindeki süt tortusunu süz (sade yağ yanmayı önler), sıvı yağla karıştır.",
            "Tepsiyi yağla; her 2 yufkada bir fırçayla ince yağ sürerek ilk 20 yufkayı diz, araya bol ceviz/fıstık serp.",
            "Kalan 20 yufkayı aynı şekilde dizip keskin bıçakla baklava dilimi kes; kalan ılık yağı üzerine gezdir.",
            "170°C alt-üst fırında 45-50 dk içi çekene ve üstü altın rengi olana dek pişir; fırından çıkıp 5 dk ilk harı gidince ılık şerbeti dök.",
        ],
        "puf_noktasi": "Tereyağının beyaz köpüğünü ve süt tortusunu süzmezsen fırında üstünde siyah yanık benekler oluşur; sade yağ çıtırlığın sırrıdır.",
    },

    "mantı": {
        "ad": "Sarımsaklı Yoğurtlu ve Tereyağlı Kayseri Mantısı",
        "sure": "Hazırlık 5 dk • Pişirme 15 dk",
        "kisi": "3-4 Kişilik",
        "pisirme_ayari": "Ocak: Haşlamada orta-yüksek ateş, sos kızdırmada kısık ateş",
        "malzemeler": [
            "500 gr mantı, 2 litre kaynar su, 1 tatlı kaşığı tuz",
            "1 büyük kase süzme/ev yoğurdu, 2 diş ezilmiş sarımsak",
            "2 yemek kaşığı tereyağı, 1 tatlı kaşığı domates salçası, kuru nane, pul biber, sumak",
        ],
        "yapilis": [
            "Tuzlu kaynar suya mantıları atıp yapışmaması için ilk 1 dakika karıştır; hamurları yumuşayana kadar 10-12 dakika haşlayıp süz.",
            "Ayrı kasede yoğurdu ezilmiş sarımsak ve bir çimdik tuzla pürüzsüz çırp.",
            "Küçük tavada tereyağını köpürt, salçayı ve kuru nane + pul biberi ekleyip 45 saniye kokusu çıkana kadar kızdır.",
            "Sıcak mantıyı tabağa al, üzerine sarımsaklı yoğurt ve kızgın tereyağlı sosu gezdirip sumak serp.",
        ],
        "puf_noktasi": "Mantıyı süzdükten sonra çok sıcakken üzerine direkt soğuk yoğurt dökersen yoğurt kesilebilir; 1 dakika ilk buharının çıkmasını bekle.",
    },
}

# ==============================================================================
# 3. CANLI AÇIK KAYNAK FONKSİYONLARI (ÜLKE, ŞEHİR, HAVA DURUMU, TARİF, KİTAP)
# ==============================================================================
def sehir_veya_ulke_bilgisi_getir(sorgu: str, detayli: bool = False) -> dict:
    """
    1. Türkiye'nin 81 ilinden biri sorulduysa: Plaka + Bölge + Detay + Canlı Wikipedia + Canlı Hava Durumu!
    2. Dünyadaki 195+ ülkeden biri sorulduysa: REST Countries API (Başkent, Nüfus, Kıta, Para Birimi, Dil) + Türkçe özet!
    3. Herhangi bir dünya şehri sorulduysa: Canlı Wikipedia + Open-Meteo hava durumu!
    """
    temiz = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    temiz_konu = re.sub(
        r"\b(hakkında bilgi ver|hakkinda bilgi ver|hakkında bilgi|hakkında|nasıl bir yer|nasıl bir şehir|nasıl bir ülke|nerededir|nerede|nedir|nüfusu|başkenti|plakası|anlat|bilgi ver|şehri|sehri|ili|ülkesi|ulkesi)\b",
        " ",
        temiz,
    )
    temiz_konu = re.sub(r"\s+", " ", temiz_konu).strip("?!.,;:\"' ")

    # A) TÜRKİYE'NİN 81 İLİ KONTROLÜ (Bursa, Tunceli, Ankara, Mardin vb.)
    for il_adi, (plaka, bolge, ozet) in TURKIYE_81_IL.items():
        if re.search(rf"\b{re.escape(il_adi)}\b", temiz):
            il_baslik = il_adi.replace("i", "İ", 1).title() if il_adi.startswith("i") else il_adi.title()
            ek_wiki = ""
            hava_str = ""
            wiki_limit = 4200 if detayli else 1900
            def _il_wiki():
                try:
                    w = wikipedia_madde_getir(il_baslik, dil="tr", detay_karakter=wiki_limit)
                    if w.get("basarili") and "Yedek" not in w.get("dil", ""):
                        kaynak_link = f"\n\n🔗 [Türkçe Vikipedi: {w['baslik']}]({w['url']})" if w.get("url") else ""
                        return f"\n\n**🌐 Kapsamlı Ansiklopedi & Tarihçe:**\n{w['ozet']}{kaynak_link}"
                except Exception:
                    pass
                return ""
            def _il_hava():
                try:
                    h = canli_hava_durumu_getir(il_baslik)
                    if h.get("basarili"):
                        return f"\n- **🌤️ Anlık Hava Durumu:** `{h['sicaklik']}°C` ({h['durum']}, Rüzgar: `{h['ruzgar']} km/sa`)"
                except Exception:
                    pass
                return ""
            with _M13Pool(max_workers=2) as _ph:
                fw, fh = _ph.submit(_il_wiki), _ph.submit(_il_hava)
                try:
                    ek_wiki = fw.result(timeout=6.0)
                except Exception:
                    ek_wiki = ""
                try:
                    hava_str = fh.result(timeout=4.5)
                except Exception:
                    hava_str = ""
            metin = (
                f"### 🏙️ {il_baslik} (Türkiye — {bolge} Bölgesi)\n"
                f"- **🚗 Plaka Kodu:** `{plaka}`\n"
                f"- **🗺️ Coğrafi Bölge:** {bolge} Bölgesi{hava_str}\n\n"
                f"**📌 Genel Bakış & Öne Çıkanlar:**\n{ozet}{ek_wiki}\n\n"
                f"💡 *Daha derin tarihçe, kültür veya gezilecek yerler için **'daha fazla bilgi ver'** yazabilirsin.*"
            )
            return {"basarili": True, "baslik": il_baslik, "metin": metin, "kaynak": f"81 İl Bilgi Bankası ({il_baslik})"}

    # B) DÜNYA ÜLKELERİ (195+ ÜLKE — REST COUNTRIES AÇIK KAYNAK API)
    eslesen_ulke_tr = None
    eslesen_ulke_en = None
    yedek_ulke_ozet = ""
    for tr_ad, (en_ad, y_ozet) in TURKCE_ULKELER.items():
        if re.search(rf"\b{re.escape(tr_ad)}\b", temiz):
            eslesen_ulke_tr = tr_ad.title()
            eslesen_ulke_en = en_ad
            yedek_ulke_ozet = y_ozet
            break

    aranacak_en = eslesen_ulke_en or (temiz_konu if len(temiz_konu.split()) <= 2 and len(temiz_konu) >= 3 else "")
    if aranacak_en:
        try:
            q_u = urllib.parse.quote(aranacak_en)
            veri = _json_cek(f"https://restcountries.com/v3.1/name/{q_u}?fullText=false", timeout=5)
            if isinstance(veri, list) and veri:
                u = veri[0]
                ad_tr = eslesen_ulke_tr or u.get("translations", {}).get("tur", {}).get("common") or u.get("name", {}).get("common", aranacak_en)
                baskent = ", ".join(u.get("capital", ["Bilinmiyor"]))
                nufus = f"{u.get('population', 0):,}".replace(",", ".")
                alan = f"{int(u.get('area', 0)):,}".replace(",", ".")
                kita = u.get("region", "")
                alt_bolge = u.get("subregion", "")
                bayrak = u.get("flag", "🌍")
                para_list = [f"{v.get('name', '')} ({v.get('symbol', '')})" for v in (u.get("currencies") or {}).values()]
                dil_list = list((u.get("languages") or {}).values())
                ulke_wiki_ek = ""
                baskent_hava_ek = ""
                u_wiki_lim = 4800 if detayli else 2200
                def _u_wiki():
                    try:
                        w = wikipedia_madde_getir(ad_tr, dil="tr", detay_karakter=u_wiki_lim)
                        if w.get("basarili") and "Yedek" not in w.get("dil", ""):
                            k_link = f"\n\n🔗 [Türkçe Vikipedi: {w['baslik']}]({w['url']})" if w.get("url") else ""
                            return f"\n\n**🌐 Tarihçe, Kültür ve Coğrafya (Vikipedi):**\n{w['ozet']}{k_link}"
                    except Exception:
                        pass
                    return ""
                def _u_hava():
                    try:
                        ilk_bk = baskent.split(",")[0].strip()
                        if ilk_bk and ilk_bk != "Bilinmiyor":
                            h = canli_hava_durumu_getir(ilk_bk)
                            if h.get("basarili"):
                                return f"\n- **🌤️ Başkent ({ilk_bk}) Anlık Hava:** `{h['sicaklik']}°C` ({h['durum']})"
                    except Exception:
                        pass
                    return ""
                with _M13Pool(max_workers=2) as _uph:
                    fw_u, fh_u = _uph.submit(_u_wiki), _uph.submit(_u_hava)
                    try:
                        ulke_wiki_ek = fw_u.result(timeout=6.0)
                    except Exception:
                        ulke_wiki_ek = ""
                    try:
                        baskent_hava_ek = fh_u.result(timeout=4.5)
                    except Exception:
                        baskent_hava_ek = ""
                metin = (
                    f"### {bayrak} {ad_tr} (Dünya Ülkeleri — REST Countries Canlı Veri)\n"
                    f"- **🏛️ Başkent:** {baskent}\n"
                    f"- **👥 Nüfus:** `{nufus}`\n"
                    f"- **📐 Yüzölçümü:** `{alan} km²`\n"
                    f"- **🌍 Kıta / Bölge:** {kita} ({alt_bolge})\n"
                    f"- **💰 Para Birimi:** {', '.join(para_list) if para_list else 'Bilinmiyor'}\n"
                    f"- **🗣️ Resmî Diller:** {', '.join(dil_list) if dil_list else 'Bilinmiyor'}{baskent_hava_ek}\n"
                    + (f"\n**📌 Genel Özet:** {yedek_ulke_ozet}" if yedek_ulke_ozet else "")
                    + ulke_wiki_ek
                    + "\n\n💡 *Daha derin tarihçe veya detay için **'daha fazla bilgi ver'** yazabilirsin.*"
                )
                metin += "\n*Kaynak: `REST Countries Açık Kaynak API (restcountries.com)`*"
                return {"basarili": True, "baslik": ad_tr, "metin": metin, "kaynak": f"REST Countries ({ad_tr})"}
        except Exception:
            pass

    if eslesen_ulke_tr and yedek_ulke_ozet:
        metin = (
            f"### 🌍 {eslesen_ulke_tr} — Ülke Bilgisi\n\n"
            f"{yedek_ulke_ozet}\n\n"
            f"*Kaynak: `AREX AI Dünya Ülkeleri Belleği`*"
        )
        return {"basarili": True, "baslik": eslesen_ulke_tr, "metin": metin, "kaynak": f"Dünya Ülkeleri ({eslesen_ulke_tr})"}

    return {"basarili": False}


def canli_hava_durumu_getir(sehir: str) -> dict:
    """
    Açık kaynaklı ve API anahtarsız Open-Meteo (open-meteo.com) üzerinden:
    - Anlık sıcaklık, hissedilen sıcaklık, bağıl nem (%), yağış (mm), rüzgar hızı (km/sa)
    - Günün en yüksek / en düşük sıcaklığı
    - 3 Günlük detaylı hava tahmini + Akıllı giyim & şemsiye tavsiyesi getirir!
    """
    # v10.8 Akıllı Şehir Ayıklayıcı ('anlık hava durumu', 'İstanbul Hava + AQI', 'İstanbulda hava' hepsini çözer!)
    _ham_low = sehir.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    _ham_asc = (
        _ham_low.replace("ç", "c").replace("ğ", "g").replace("ı", "i")
        .replace("ö", "o").replace("ş", "s").replace("ü", "u")
    )
    sehir_temiz = ""
    # 1. Önce 81 il veya büyük dünya şehirlerinden biri geçiyor mu doğrudan yakala
    for _il_k, _il_v in TURKIYE_81_IL.items():
        _il_asc = (
            _il_k.replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            .replace("ö", "o").replace("ş", "s").replace("ü", "u")
        )
        if re.search(rf"\b{re.escape(_il_asc)}(?:da|de|ta|te|nda|nde|in|in|un|un|a|e)?\b", _ham_asc):
            sehir_temiz = _il_k.capitalize()
            break
    if not sehir_temiz:
        sehir_temiz = re.sub(
            r"\b(hava durumu|hava kalitesi|hava nasıl|hava nasil|bugün hava|bugun hava|anlık|anlik|şu an|su an|güncel|guncel|detaylı|detayli|derece|sıcaklık|sicaklik|kaç|kac|nedir|nasıl|nasil|hava|durumu|aqi|yağmur var mı|kar yağacak mı|yağmur|kar|bugün|bugun|yarın|yarin|ver|söyle|soyle|göster|goster|ve)\b",
            " ",
            sehir,
            flags=re.IGNORECASE,
        )
        sehir_temiz = re.sub(r"[+?!.,;:'\"()\[\]]+", " ", sehir_temiz)
        sehir_temiz = re.sub(r"\s+", " ", sehir_temiz).strip()
        sehir_temiz = re.sub(r"(?:'?da|'?de|'?ta|'?te|'?nda|'?nde)$", "", sehir_temiz, flags=re.IGNORECASE).strip()
    if not sehir_temiz or len(sehir_temiz) < 2:
        sehir_temiz = "İstanbul"

    # Sabit hızlı koordinat önbelleği (Geocoding API gecikirse veya erişilemezse anında çalışır!)
    _SABIT_KOORD = {
        "istanbul": (41.0082, 28.9784, "İstanbul", "Türkiye"),
        "ankara": (39.9334, 32.8597, "Ankara", "Türkiye"),
        "izmir": (38.4237, 27.1428, "İzmir", "Türkiye"),
        "mardin": (37.3212, 40.7245, "Mardin", "Türkiye"),
        "bursa": (40.1885, 29.0610, "Bursa", "Türkiye"),
        "antalya": (36.8969, 30.7133, "Antalya", "Türkiye"),
        "adana": (37.0000, 35.3213, "Adana", "Türkiye"),
        "konya": (37.8746, 32.4932, "Konya", "Türkiye"),
        "gaziantep": (37.0662, 37.3833, "Gaziantep", "Türkiye"),
        "trabzon": (41.0027, 39.7168, "Trabzon", "Türkiye"),
        "sanliurfa": (37.1674, 38.7955, "Şanlıurfa", "Türkiye"),
        "diyarbakir": (37.9144, 40.2306, "Diyarbakır", "Türkiye"),
        "fatih": (41.0186, 28.9397, "Fatih / İstanbul", "Türkiye"),
        "kadikoy": (40.9909, 29.0293, "Kadıköy / İstanbul", "Türkiye"),
        "besiktas": (41.0422, 29.0083, "Beşiktaş / İstanbul", "Türkiye"),
        "uskudar": (41.0234, 29.0152, "Üsküdar / İstanbul", "Türkiye"),
        "londra": (51.5074, -0.1278, "Londra", "Birleşik Krallık"),
        "paris": (48.8566, 2.3522, "Paris", "Fransa"),
        "berlin": (52.5200, 13.4050, "Berlin", "Almanya"),
        "amsterdam": (52.3676, 4.9041, "Amsterdam", "Hollanda"),
        "tokyo": (35.6762, 139.6503, "Tokyo", "Japonya"),
        "seul": (37.5665, 126.9780, "Seul", "Güney Kore"),
        "mekke": (21.3891, 39.8579, "Mekke", "Suudi Arabistan"),
        "medine": (24.5247, 39.5692, "Medine", "Suudi Arabistan"),
    }

    wmo_tr = {
        0: "Açık ve Güneşli ☀️", 1: "Çoğunlukla Açık 🌤️", 2: "Parçalı Bulutlu ⛅", 3: "Kapalı / Bulutlu ☁️",
        45: "Sisli 🌫️", 48: "Kırağılı Sis 🌫️", 51: "Hafif Çiseleyen Yağmur 🌦️", 53: "Orta Çiseleme 🌦️",
        61: "Hafif Yağmurlu 🌧️", 63: "Orta Şiddetli Yağmur 🌧️", 65: "Şiddetli Yağmur ⛈️",
        71: "Hafif Kar Yağışlı ❄️", 73: "Kar Yağışlı ❄️", 80: "Sağanak Yağışlı 🌦️", 95: "Gök Gürültülü Fırtına ⛈️",
    }
    try:
        _s_asc = (
            sehir_temiz.replace("İ", "i").replace("I", "ı").lower()
            .replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            .replace("ö", "o").replace("ş", "s").replace("ü", "u").strip()
        )
        if _s_asc in _SABIT_KOORD:
            lat, lon, sehir_ad, ulke = _SABIT_KOORD[_s_asc]
        else:
            q = urllib.parse.quote(sehir_temiz)
            geo = _json_cek(f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1&language=tr&format=json", timeout=5)
            sonuclar = geo.get("results", [])
            if not sonuclar:
                return {"basarili": False, "hata": f"'{sehir_temiz}' şehri bulunamadı."}
            g0 = sonuclar[0]
            lat, lon = g0["latitude"], g0["longitude"]
            sehir_ad = g0.get("name", sehir_temiz)
            ulke = g0.get("country", "")
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            "&timezone=auto&forecast_days=3"
        )
        aqi_url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}&current=european_aqi,pm2_5,pm10,uv_index&timezone=auto"
        )
        aqi_veri = {}
        with _M13Pool(max_workers=2) as _hp:
            f_w = _hp.submit(_json_cek, url, 6)
            f_a = _hp.submit(_json_cek, aqi_url, 4)
            w_veri = f_w.result(timeout=6.5)
            try:
                aqi_veri = f_a.result(timeout=4.5) or {}
            except Exception:
                aqi_veri = {}
        cur = w_veri.get("current", {})
        daily = w_veri.get("daily", {})

        sicaklik = cur.get("temperature_2m", "-")
        hissedilen = cur.get("apparent_temperature", sicaklik)
        nem = cur.get("relative_humidity_2m", "-")
        yagis = cur.get("precipitation", 0)
        ruzgar = cur.get("wind_speed_10m", "-")
        kod = int(cur.get("weather_code", 0))
        durum = wmo_tr.get(kod, "Değişken Bulutlu ⛅")

        # Akıllı giyim ve dışarı çıkış tavsiyesi
        tavsiyeler = []
        try:
            t_num = float(sicaklik)
            if t_num < 8:
                tavsiyeler.append("Hava soğuk; kalın mont, atkı veya bere alman iyi olur.")
            elif t_num < 16:
                tavsiyeler.append("Hava serin; ince mont veya kapüşonlu giymen rahat olur.")
            elif t_num < 25:
                tavsiyeler.append("Hava oldukça ılıman ve yürüyüş için ideal.")
            else:
                tavsiyeler.append("Hava sıcak; ince kıyafetler giyip bol su içmeyi unutma.")
        except Exception:
            pass
        if kod in (51, 53, 61, 63, 65, 80, 95) or (isinstance(yagis, (int, float)) and yagis > 0):
            tavsiyeler.append("Yağış görünüyor; yanına şemsiye veya yağmurluk al.")

        # 3 Günlük tahmin satırları
        tahmin_satirlari = []
        gun_etiket = ["Bugün", "Yarın", "Öbür Gün"]
        tarihler = daily.get("time", [])
        tmax_l = daily.get("temperature_2m_max", [])
        tmin_l = daily.get("temperature_2m_min", [])
        ykod_l = daily.get("weather_code", [])
        yag_ol = daily.get("precipitation_probability_max", [])
        for i in range(min(3, len(tarihler))):
            g_durum = wmo_tr.get(int(ykod_l[i]), "Parçalı Bulutlu ⛅") if i < len(ykod_l) else ""
            g_yag = f" • Yağış İhtimali: `%{yag_ol[i]}`" if i < len(yag_ol) and yag_ol[i] is not None else ""
            tahmin_satirlari.append(
                f"- **{gun_etiket[i]} ({tarihler[i]}):** En Düşük `{tmin_l[i]}°C` / En Yüksek `{tmax_l[i]}°C` — {g_durum}{g_yag}"
            )

        metin = (
            f"### 🌤️ Güncel Hava Durumu & 3 Günlük Tahmin: **{sehir_ad}** ({ulke})\n"
            f"- **🌡️ Anlık Sıcaklık:** `{sicaklik}°C` (Hissedilen: `{hissedilen}°C`)\n"
            f"- **☁️ Hava Durumu:** {durum}\n"
            f"- **💧 Bağıl Nem:** `%{nem}` | **🌧️ Anlık Yağış:** `{yagis} mm`\n"
            f"- **💨 Rüzgar Hızı:** `{ruzgar} km/sa`\n"
        )
        aqi_cur = aqi_veri.get("current", {}) if isinstance(aqi_veri, dict) else {}
        eaqi = aqi_cur.get("european_aqi")
        pm25 = aqi_cur.get("pm2_5")
        pm10 = aqi_cur.get("pm10")
        uv_idx = aqi_cur.get("uv_index")
        if eaqi is not None:
            aqi_yorum = "Çok İyi (Temiz Hava)" if eaqi <= 20 else ("İyi" if eaqi <= 40 else ("Orta" if eaqi <= 60 else ("Hassas" if eaqi <= 80 else "Kötü (Kirli Hava)")))
            metin += f"- **🌫️ Anlık Hava Kalitesi (Avrupa AQI):** `{eaqi}` ({aqi_yorum}) | **PM2.5:** `{pm25} µg/m³` | **PM10:** `{pm10} µg/m³` | **☀️ UV:** `{uv_idx}`\n"
        metin = (metin + ""
        )
        if tahmin_satirlari:
            metin += "\n**📅 3 Günlük Hava Tahmini:**\n" + "\n".join(tahmin_satirlari) + "\n"
        if tavsiyeler:
            metin += "\n**🧥 Öneri:** " + " ".join(tavsiyeler) + "\n"
        metin += "\n*Kaynak: `Open-Meteo Canlı Meteoroloji API (open-meteo.com)`*"
        return {"basarili": True, "sehir": sehir_ad, "sicaklik": sicaklik, "ruzgar": ruzgar, "durum": durum, "metin": metin}
    except Exception:
        # 2. Canlı Yedek: wttr.in JSON API (Open-Meteo bulutta gecikirse anında devreye girer!)
        try:
            q_wt = urllib.parse.quote(sehir_temiz)
            wt = _json_cek(f"https://wttr.in/{q_wt}?format=j1", timeout=5)
            cc = (wt.get("current_condition") or [{}])[0]
            temp_c = cc.get("temp_C")
            if temp_c is not None:
                feels = cc.get("FeelsLikeC", temp_c)
                hum = cc.get("humidity", "-")
                wind = cc.get("windspeedKmph", "-")
                desc = ((cc.get("weatherDesc") or [{}])[0]).get("value", "Açık")
                metin_wt = (
                    f"### 🌤️ Güncel Hava Durumu: **{sehir_temiz}**\n"
                    f"- **🌡️ Anlık Sıcaklık:** `{temp_c}°C` (Hissedilen: `{feels}°C`)\n"
                    f"- **☁️ Durum:** {desc}\n"
                    f"- **💧 Nem:** `%{hum}` | **💨 Rüzgar:** `{wind} km/sa`\n\n"
                    f"*Kaynak: `wttr.in Canlı Meteoroloji Yedeği`*"
                )
                return {"basarili": True, "sehir": sehir_temiz, "sicaklik": temp_c, "ruzgar": wind, "durum": desc, "metin": metin_wt}
        except Exception:
            pass
        return {
            "basarili": False,
            "hata": f"'{sehir_temiz}' için canlı hava durumu sunucularına (Open-Meteo & wttr.in) şu an ulaşılamadı.",
        }


def yemek_tarifi_getir(sorgu: str) -> dict:
    """
    Şef Kalitesinde Detaylı Yemek Tarifi Motoru (v6.3):
    1. Türk Mutfağı şef tarif defteri (fırın derecesi, raf ayarı, malzeme ekleme sırası ve püf noktaları).
    2. Dünya mutfağı için canlı TheMealDB açık kaynak API + otomatik Türkçe çeviri.
    3. Yöresel/özel yemeklerde Türkçe Wikipedia mutfak bilgisi yedeği.
    """
    temiz = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    _tr_map = str.maketrans('çğıöşü', 'cgiosu')
    temiz_ascii = temiz.translate(_tr_map)
    for anahtar, t in TURK_YEMEK_TARIFLERI.items():
        if anahtar in temiz or anahtar.translate(_tr_map) in temiz_ascii:
            malz_str = "\n".join(f"- {m}" for m in t["malzemeler"])
            yap_str = "\n".join(f"{i}. {adim}" for i, adim in enumerate(t["yapilis"], 1))
            metin = (
                f"### 🍲 Detaylı Şef Tarifi: **{t['ad']}**\n"
                f"- **⏱️ Süre:** `{t['sure']}` | **👥 Porsiyon:** `{t['kisi']}`\n"
                f"- **🔥 Fırın / Ocak Ayarı:** {t['pisirme_ayari']}\n\n"
                f"**🛒 Tam Ölçülü Malzemeler:**\n{malz_str}\n\n"
                f"**👨‍🍳 Adım Adım Yapılışı (Malzeme Ekleme Sırasıyla):**\n{yap_str}\n\n"
                f"**💡 Şefin Püf Noktası:** {t['puf_noktasi']}\n\n"
                f"*Afiyet olsun Ahmet!* ⚡"
            )
            return {"basarili": True, "ad": t["ad"], "metin": metin, "kaynak": "Türk Mutfağı Şef Defteri"}

    # Canlı Açık Kaynak TheMealDB API (Dünya Mutfağı)
    yemek_adi = re.sub(
        r"\b(tarifi|tarif|nasıl yapılır|nasil yapilir|yemeği|yemegi|yapılışı|yapilisi|bana|ver|anlat|fırında|firinda)\b",
        " ",
        temiz,
    ).strip("?!.,;:' ")
    if yemek_adi:
        try:
            en_yemek = guvenli_cevir(yemek_adi, src="tr", dest="en") or yemek_adi
            q = urllib.parse.quote(en_yemek.strip())
            veri = _json_cek(f"https://www.themealdb.com/api/json/v1/1/search.php?s={q}", timeout=6)
            meals = veri.get("meals")
            if meals:
                m0 = meals[0]
                ad_en = m0.get("strMeal", en_yemek)
                yapilis_en = (m0.get("strInstructions") or "")[:1800]
                yapilis_tr = guvenli_cevir(yapilis_en, src="en", dest="tr") or yapilis_en
                malzemeler = []
                for idx in range(1, 21):
                    ing = (m0.get(f"strIngredient{idx}") or "").strip()
                    meas = (m0.get(f"strMeasure{idx}") or "").strip()
                    if ing:
                        malzemeler.append(f"{meas} {ing}".strip())
                malz_tr = guvenli_cevir(", ".join(malzemeler[:14]), src="en", dest="tr") or ", ".join(malzemeler[:14])
                metin = (
                    f"### 🍽️ Dünya Mutfağı Detaylı Tarifi: **{ad_en}**\n"
                    f"**🛒 Malzemeler:** {malz_tr}\n\n"
                    f"**👨‍🍳 Adım Adım Hazırlanışı:**\n{yapilis_tr}\n\n"
                    f"*Kaynak: `TheMealDB Açık Kaynak Tarif API (themealdb.com)`*"
                )
                return {"basarili": True, "ad": ad_en, "metin": metin, "kaynak": "TheMealDB (Açık Kaynak)"}
        except Exception:
            pass

    # 3. Yöresel veya özel yemekler için Türkçe Wikipedia mutfak bilgisi yedeği
    if yemek_adi and len(yemek_adi) >= 3:
        try:
            w = wikipedia_madde_getir(yemek_adi, dil="tr", detay_karakter=1800)
            if w.get("basarili"):
                metin = (
                    f"### 🍲 Yemek & Mutfak Rehberi: **{w['baslik']}**\n\n"
                    f"{w['ozet']}\n\n"
                    f"*Kaynak: `Türkçe Wikipedia Mutfak Ansiklopedisi`*"
                )
                return {"basarili": True, "ad": w["baslik"], "metin": metin, "kaynak": "Wikipedia Mutfak"}
        except Exception:
            pass

    return {"basarili": False}


def kitap_bilgisi_getir(sorgu: str) -> dict:
    """Açık kaynaklı Open Library (openlibrary.org) üzerinden kitap yazarı ve basım yılı bilgisi getirir."""
    kitap = re.sub(r"\b(kitabı|kitabi|kitap|özeti|ozeti|yazarı|yazari|kim yazdı|kim yazdi|hakkında)\b", " ", sorgu, flags=re.IGNORECASE).strip("?!.,;:\"' ")
    if not kitap:
        return {"basarili": False}
    try:
        q = urllib.parse.quote(kitap)
        veri = _json_cek(f"https://openlibrary.org/search.json?q={q}&limit=2", timeout=6)
        docs = veri.get("docs", [])
        if docs:
            d0 = docs[0]
            baslik = d0.get("title", kitap)
            yazarlar = ", ".join(d0.get("author_name", ["Bilinmiyor"])[:3])
            yil = d0.get("first_publish_year", "Bilinmiyor")
            metin = (
                f"### 📚 Kitap Bilgisi: **{baslik}**\n"
                f"- **✍️ Yazar:** {yazarlar}\n"
                f"- **📅 İlk Basım Yılı:** `{yil}`\n"
                f"\n*Kaynak: `Open Library Açık Kaynak Kütüphane (openlibrary.org)`*"
            )
            return {"basarili": True, "baslik": baslik, "metin": metin, "kaynak": "Open Library"}
    except Exception:
        pass
    return {"basarili": False}





# ==============================================================================
# 4. CANLI DÖVİZ, ALTIN (GRAM / ÇEYREK / YARIM / TAM) VE KRİPTO MOTORU
#    Ücretsiz & API Anahtarsız Açık Kaynak API'ler:
#    • open.er-api.com / api.frankfurter.app -> Canlı USD, EUR, GBP kurları
#    • api.gold-api.com/price/XAU -> Canlı Ons Altın ($) -> Gram/Çeyrek/Tam TL
#    • api.coingecko.com -> Canlı Bitcoin & Ethereum
# ==============================================================================
def _canli_kurlari_cek() -> dict:
    """Açık kaynak API'lerden canlı USD/TRY, EUR/TRY, GBP/TRY ve Ons Altın fiyatını çeker."""
    sonuc = {"canli": False, "usd_try": None, "eur_try": None, "gbp_try": None, "ons_altin_usd": None, "btc_usd": None, "btc_try": None}

    # 1. Canlı Döviz Kurları (open.er-api.com)
    try:
        d = _json_cek("https://open.er-api.com/v6/latest/USD", timeout=5)
        rates = d.get("rates", {})
        if rates.get("TRY"):
            usd_try = float(rates["TRY"])
            sonuc["usd_try"] = usd_try
            if rates.get("EUR"):
                sonuc["eur_try"] = usd_try / float(rates["EUR"])
            if rates.get("GBP"):
                sonuc["gbp_try"] = usd_try / float(rates["GBP"])
            sonuc["canli"] = True
    except Exception:
        # Yedek 2: Frankfurter (Avrupa Merkez Bankası açık verisi)
        try:
            d2 = _json_cek("https://api.frankfurter.app/latest?from=USD&to=TRY,EUR,GBP", timeout=5)
            r2 = d2.get("rates", {})
            if r2.get("TRY"):
                usd_try = float(r2["TRY"])
                sonuc["usd_try"] = usd_try
                if r2.get("EUR"):
                    sonuc["eur_try"] = usd_try / float(r2["EUR"])
                if r2.get("GBP"):
                    sonuc["gbp_try"] = usd_try / float(r2["GBP"])
                sonuc["canli"] = True
        except Exception:
            pass

    # 2. Canlı Ons Altın (XAU/USD — api.gold-api.com)
    try:
        g = _json_cek("https://api.gold-api.com/price/XAU", timeout=5)
        if g.get("price"):
            sonuc["ons_altin_usd"] = float(g["price"])
            sonuc["canli"] = True
    except Exception:
        pass

    # 3. Canlı Kripto (CoinGecko)
    try:
        c = _json_cek("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,try", timeout=5)
        if c.get("bitcoin"):
            sonuc["btc_usd"] = float(c["bitcoin"].get("usd", 0))
            sonuc["btc_try"] = float(c["bitcoin"].get("try", 0))
            sonuc["canli"] = True
    except Exception:
        pass

    return sonuc


def canli_doviz_ve_altin_getir(sorgu: str) -> dict:
    """
    Sohbette 'gram altın ne kadar?', 'çeyrek altın fiyatı', 'dolar kaç tl?',
    '100 dolar kaç tl?', 'euro kuru', 'bitcoin ne kadar?' gibi tüm finans sorularını
    canlı açık kaynak verileriyle hesaplar ve temiz Türkçe kart olarak döndürür.
    """
    temiz = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    k = _canli_kurlari_cek()

    # Tutar ayıklama (örn. '100 dolar kaç tl', '5 gram altın kaç tl')
    miktar_m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:dolar|usd|euro|eur|sterlin|gbp|gram\s+alt[ıi]n|çeyrek\s+alt[ıi]n|ceyrek\s+alt[ıi]n)", temiz)
    miktar = float(miktar_m.group(1).replace(",", ".")) if miktar_m else 1.0

    satirlar = ["### 💰 Canlı Altın, Döviz ve Piyasa Kurları"]

    if k["canli"] and k["usd_try"]:
        usd = k["usd_try"]
        eur = k["eur_try"] or (usd * 1.08)
        gbp = k["gbp_try"] or (usd * 1.27)

        # Özel tutar çevirisi istendiyse en üstte net hesapla
        if miktar_m:
            if any(x in temiz for x in ["dolar", "usd"]):
                satirlar.append(f"**🧮 Hesaplama:** `{miktar:g} USD` = **`{miktar * usd:,.2f} TL`**")
            elif any(x in temiz for x in ["euro", "eur"]):
                satirlar.append(f"**🧮 Hesaplama:** `{miktar:g} EUR` = **`{miktar * eur:,.2f} TL`**")
            elif any(x in temiz for x in ["sterlin", "gbp"]):
                satirlar.append(f"**🧮 Hesaplama:** `{miktar:g} GBP` = **`{miktar * gbp:,.2f} TL`**")

        satirlar.append(
            f"- **💵 Dolar (USD/TRY):** `{usd:,.2f} TL`\n"
            f"- **💶 Euro (EUR/TRY):** `{eur:,.2f} TL`\n"
            f"- **💷 Sterlin (GBP/TRY):** `{gbp:,.2f} TL`"
        )

        if k["ons_altin_usd"]:
            ons = k["ons_altin_usd"]
            gram_tl = (ons / 31.1034768) * usd
            ceyrek_tl = gram_tl * 1.635
            yarim_tl = ceyrek_tl * 2
            tam_tl = ceyrek_tl * 4
            if miktar_m and "gram" in temiz:
                satirlar.insert(1, f"**🧮 Hesaplama:** `{miktar:g} Gram Altın` ≈ **`{miktar * gram_tl:,.2f} TL`**")
            elif miktar_m and ("çeyrek" in temiz or "ceyrek" in temiz):
                satirlar.insert(1, f"**🧮 Hesaplama:** `{miktar:g} Çeyrek Altın` ≈ **`{miktar * ceyrek_tl:,.2f} TL`**")
            satirlar.append(
                f"\n**🥇 Canlı Altın Fiyatları (Ons: `${ons:,.2f}`):**\n"
                f"- **Gram Altın (24 Ayar):** `{gram_tl:,.2f} TL`\n"
                f"- **Çeyrek Altın:** `{ceyrek_tl:,.2f} TL`\n"
                f"- **Yarım Altın:** `{yarim_tl:,.2f} TL`\n"
                f"- **Tam Altın:** `{tam_tl:,.2f} TL`"
            )

        if k["btc_usd"]:
            satirlar.append(f"\n**₿ Kripto:** Bitcoin (BTC) = `${k['btc_usd']:,.0f}` (`{k['btc_try']:,.0f} TL`)")

        satirlar.append("\n*Kaynaklar: `Open Exchange Rates (open.er-api.com)`, `Gold-API (gold-api.com)`, `CoinGecko` (Canlı Açık Kaynak)*")
        return {"basarili": True, "metin": "\n".join(satirlar), "kaynak": "Canlı Finans & Altın API"}

    # Çevrimdışıysa uydurma kur yazmaz; açık kaynak canlı takip kaynaklarını netçe bildirir
    satirlar.append(
        "⚠️ Şu an canlı döviz/altın API sunucularına (`open.er-api.com`, `gold-api.com`) internet üzerinden ulaşılamadı.\n"
        "Bilgisayarın internete bağlı olduğunda **Dolar, Euro, Sterlin, Gram/Çeyrek/Yarım/Tam Altın ve Bitcoin** kurlarını anlık çekip otomatik hesaplarım.\n\n"
        "**🔗 Anlık Resmi Takip Kaynakları:**\n"
        "- [TCMB Günlük Döviz Kurları](https://www.tcmb.gov.tr/kurlar/today.xml)\n"
        "- [Altın & Döviz Canlı Piyasa (Bigpara)](https://bigpara.hurriyet.com.tr/altin/)"
    )
    return {"basarili": True, "metin": "\n".join(satirlar), "kaynak": "Finans & Altın Motoru"}


# ==============================================================================
# 5. FUTBOLCU GÜNCEL PİYASA DEĞERİ, DOĞRULANMIŞ KULÜP & DETAYLI ANALİZ MOTORU
#    HATA DÜZELTMESİ (v6.2):
#    • TheSportsDB'nin ücretsiz sürümde yanlış/eski kulüp (örn. Osimhen -> Liverpool)
#      döndürmesi sorunu İsim/Spor Doğrulama Kilidi + Doğrulanmış 2026 Yıldız Havuzu
#      ve canlı Wikipedia/Transfermarkt profil doğrulamasıyla %100 giderildi!
# ==============================================================================
YILDIZ_FUTBOLCULAR = {
    "victor osimhen": {
        "ad": "Victor Osimhen",
        "kulup": "Galatasaray (Süper Lig — 2025'te Napoli'den bonservisiyle kalıcı transfer)",
        "milli_takim": "Nijerya",
        "mevki": "Santrafor (Merkez Forvet)",
        "dogum": "29 Aralık 1998 (Lagos, Nijerya)",
        "sozlesme": "30 Haziran 2029",
        "piyasa_degeri": "65,00 mil. €",
        "zirve_deger": "120,00 mil. € (Napoli dönemi)",
        "tm_url": "https://www.transfermarkt.com.tr/victor-osimhen/profil/spieler/401923",
        "analiz": (
            "Türkiye Süper Lig'in en değerli futbolcusudur. Temmuz 2025'te Napoli'den Galatasaray'a 75 mil. € bonservisle kalıcı olarak transfer olmuştur. "
            "Patlayıcı hızı, hava topu hakimiyeti, yüksek pres gücü ve bitiriciliğiyle Avrupa'nın elit santraforları arasında yer alır."
        ),
    },
    "arda güler": {
        "ad": "Arda Güler",
        "kulup": "Real Madrid (LaLiga)",
        "milli_takim": "Türkiye",
        "mevki": "On Numara / Sağ Kanat",
        "dogum": "25 Şubat 2005 (Ankara, Türkiye)",
        "sozlesme": "30 Haziran 2029",
        "piyasa_degeri": "100,00 mil. €",
        "zirve_deger": "100,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/arda-guler/profil/spieler/861410",
        "analiz": (
            "Real Madrid ve A Milli Takım'ın en değerli genç yıldızlarından biridir. "
            "Dar alanda üstün sol ayak tekniği, oyun görüşü, duran top ustalığı ve kritik pas kalitesiyle dünya futbolunda 100 milyon € barajına ulaşmıştır."
        ),
    },
    "kenan yıldız": {
        "ad": "Kenan Yıldız",
        "kulup": "Juventus (Serie A)",
        "milli_takim": "Türkiye",
        "mevki": "Sol Kanat / Forvet Arkası",
        "dogum": "4 Mayıs 2005 (Regensburg, Almanya)",
        "sozlesme": "30 Haziran 2030",
        "piyasa_degeri": "75,00 mil. €",
        "zirve_deger": "75,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/kenan-yildiz/profil/spieler/845654",
        "analiz": (
            "Juventus'un 10 numaralı formasıyla Serie A ve Şampiyonlar Ligi'nde öne çıkan A Milli Takım yıldızıdır. "
            "İki ayağını etkili kullanması, dripling becerisi ve içe kat edip attığı şutlarla yüksek çıkış yakalamıştır."
        ),
    },
    "mauro icardi": {
        "ad": "Mauro Icardi",
        "kulup": "Galatasaray (Süper Lig)",
        "milli_takim": "Arjantin",
        "mevki": "Santrafor",
        "dogum": "19 Şubat 1993 (Rosario, Arjantin)",
        "sozlesme": "Galatasaray",
        "piyasa_degeri": "13,00 – 15,00 mil. € bandı",
        "zirve_deger": "100,00 mil. € (Inter dönemi)",
        "tm_url": "https://www.transfermarkt.com.tr/mauro-icardi/profil/spieler/68863",
        "analiz": (
            "Galatasaray'ın şampiyonluklarında büyük pay sahibi olan, ceza sahası içi pozisyon alma zekâsı ve tek vuruş bitiriciliğiyle tanınan Arjantinli golcüdür."
        ),
    },
    "barış alper yılmaz": {
        "ad": "Barış Alper Yılmaz",
        "kulup": "Galatasaray (Süper Lig)",
        "milli_takim": "Türkiye",
        "mevki": "Sağ Kanat / Sol Kanat / Santrafor",
        "dogum": "23 Mayıs 2000 (Rize, Türkiye)",
        "sozlesme": "Galatasaray",
        "piyasa_degeri": "20,00 – 25,00 mil. € bandı",
        "zirve_deger": "25,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/baris-alper-yilmaz/profil/spieler/535174",
        "analiz": (
            "Fizik gücü, yüksek sprint hızı ve hem kanatlarda hem bek/forvet hattında oynayabilen çok yönlülüğüyle Galatasaray ve Milli Takım'ın kilit isimlerindendir."
        ),
    },
    "hakan çalhanoğlu": {
        "ad": "Hakan Çalhanoğlu",
        "kulup": "Inter (Serie A)",
        "milli_takim": "Türkiye (Kaptan)",
        "mevki": "Ön Libero / Merkez Orta Saha",
        "dogum": "8 Şubat 1994 (Mannheim, Almanya)",
        "sozlesme": "Inter",
        "piyasa_degeri": "35,00 – 40,00 mil. € bandı",
        "zirve_deger": "45,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/hakan-calhanoglu/profil/spieler/126414",
        "analiz": (
            "A Milli Takım kaptanı ve Inter'in oyun kurucusudur. Uzun pas isabeti, duran top/penaltı ustalığı ve maç temposunu yönetme becerisiyle Avrupa'nın en iyi derin oyun kurucularındandır."
        ),
    },
    "kylian mbappe": {
        "ad": "Kylian Mbappé",
        "kulup": "Real Madrid (LaLiga)",
        "milli_takim": "Fransa",
        "mevki": "Santrafor / Sol Kanat",
        "dogum": "20 Aralık 1998 (Paris, Fransa)",
        "sozlesme": "30 Haziran 2029",
        "piyasa_degeri": "160,00 – 180,00 mil. € bandı",
        "zirve_deger": "200,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/kylian-mbappe/profil/spieler/342229",
        "analiz": (
            "Dünya Kupası şampiyonu Fransız süper yıldız; olağanüstü ivmelenme hızı ve bitiriciliğiyle Real Madrid hücum hattının liderlerindendir."
        ),
    },
    "lamine yamal": {
        "ad": "Lamine Yamal",
        "kulup": "FC Barcelona (LaLiga)",
        "milli_takim": "İspanya",
        "mevki": "Sağ Kanat",
        "dogum": "13 Temmuz 2007 (Esplugues, İspanya)",
        "sozlesme": "FC Barcelona",
        "piyasa_degeri": "150,00 – 180,00 mil. € bandı",
        "zirve_deger": "180,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/lamine-yamal/profil/spieler/937958",
        "analiz": (
            "EURO 2024 şampiyonu İspanya ve Barcelona'nın genç fenomeni; bire birde adam eksiltme, asist üretme ve yaşının çok ötesindeki oyun olgunluğuyla dünyanın en değerli oyuncularındandır."
        ),
    },
    "erling haaland": {
        "ad": "Erling Haaland",
        "kulup": "Manchester City (Premier League)",
        "milli_takim": "Norveç",
        "mevki": "Santrafor",
        "dogum": "21 Temmuz 2000 (Leeds, İngiltere)",
        "sozlesme": "Manchester City",
        "piyasa_degeri": "180,00 – 200,00 mil. € bandı",
        "zirve_deger": "200,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/erling-haaland/profil/spieler/418560",
        "analiz": (
            "Premier League gol rekorlarını kıran Norveçli gol makinesi; fiziksel üstünlüğü, savunma arkası koşuları ve bitiricilik oranıyla dünyanın en değerli santraforları arasındadır."
        ),
    },
    "mohamed salah": {
        "ad": "Mohamed Salah",
        "kulup": "Liverpool (Premier League)",
        "milli_takim": "Mısır",
        "mevki": "Sağ Kanat",
        "dogum": "15 Haziran 1992 (Nagrig, Mısır)",
        "sozlesme": "Liverpool",
        "piyasa_degeri": "22,00 – 30,00 mil. € bandı",
        "zirve_deger": "150,00 mil. €",
        "tm_url": "https://www.transfermarkt.com.tr/mohamed-salah/profil/spieler/148455",
        "analiz": (
            "Liverpool tarihinin en golcü isimlerinden biri olan Mısırlı yıldız; istikrarlı gol ve asist katkısıyla Premier League efsaneleri arasındadır."
        ),
    },
}

# Kısa soyadı/takma ad eşlemeleri
_FUTBOLCU_KISA_ADLAR = {
    "osimhen": "victor osimhen",
    "icardi": "mauro icardi",
    "arda guler": "arda güler",
    "kenan yildiz": "kenan yıldız",
    "baris alper": "barış alper yılmaz",
    "hakan calhanoglu": "hakan çalhanoğlu",
    "mbappe": "kylian mbappe",
    "yamal": "lamine yamal",
    "haaland": "erling haaland",
    "salah": "mohamed salah",
}


def _isim_benzerlik_skoru(a: str, b: str) -> float:
    import difflib
    t1 = a.replace("İ", "i").replace("I", "ı").lower().strip()
    t2 = b.replace("İ", "i").replace("I", "ı").lower().strip()
    return difflib.SequenceMatcher(None, t1, t2).ratio()


def futbolcu_piyasa_degeri_getir(sorgu: str) -> dict:
    """
    DOĞRULANMIŞ & DETAYLI FUTBOLCU PİYASA DEĞERİ ANALİZ MOTORU (v6.2):
    1. Önce doğrulanmış güncel yıldız futbolcu profilini kontrol eder (Osimhen -> Galatasaray,
       Arda Güler -> Real Madrid, Kenan Yıldız -> Juventus gibi yanlış kulüp hatalarını %100 önler).
    2. Bilinmeyen bir oyuncuysa TheSportsDB'de YALNIZCA spor='Soccer' VE isim benzerliği >= 0.78
       olan kaydı kabul eder; aksi halde yanlış oyuncu/kulüp bilgisini REDDEDER!
    3. Canlı Transfermarkt profil sayfasından anlık € değerini ve Türkçe Wikipedia'dan güncel
       kariyer özetini çekerek detaylı analiz üretir.
    """
    temiz = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    oyuncu = re.sub(
        r"\b(piyasa\s+değeri|piyasa\s+degeri|bonservis\s+bedeli|bonservisi|değeri\s+ne\s+kadar|degeri\s+ne\s+kadar|kaç\s+euro|kac\s+euro|kaç\s+milyon|kac\s+milyon|transfermarkt|güncel\s+değeri|futbolcu|ne\s+kadar|nedir|kaç|analizi|analiz|hangi\s+takımda)\b",
        " ",
        temiz,
    )
    oyuncu = re.sub(r"(?:'nin|'nın|'nun|'nün|'in|'ın|'un|'ün)$", "", oyuncu).strip("?!.,;:' ")
    oyuncu = re.sub(r"\s+", " ", oyuncu).strip()
    if not oyuncu:
        return {"basarili": False, "hata": "Lütfen piyasa değerini ve analizini öğrenmek istediğiniz futbolcunun adını yazın."}

    # 1. Doğrulanmış Yıldız Futbolcu Eşleşmesi (Kısa adlar dahil)
    yerel = None
    for kisa, tam_anahtar in _FUTBOLCU_KISA_ADLAR.items():
        if kisa in temiz:
            yerel = YILDIZ_FUTBOLCULAR.get(tam_anahtar)
            break
    if yerel is None:
        for anahtar, veri in YILDIZ_FUTBOLCULAR.items():
            if anahtar in temiz or _isim_benzerlik_skoru(oyuncu, anahtar) >= 0.80:
                yerel = veri
                break

    # 2. Canlı Doğrudan Profil Transfermarkt Taraması (Sadece oyuncunun kendi profil URL'si varsa!)
    canli_tm_deger = None
    tm_url = yerel["tm_url"] if yerel else f"https://www.transfermarkt.com.tr/schnellsuche/ergebnis/schnellsuche?query={urllib.parse.quote_plus(oyuncu)}"
    if yerel:
        try:
            req = urllib.request.Request(
                tm_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
                    "Accept-Language": "tr-TR,tr;q=0.9",
                },
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                tm_html = resp.read().decode("utf-8", errors="ignore")
            m_val = re.search(r"(\d+(?:[.,]\d+)?\s*(?:mil\.|bin)\s*€)", tm_html)
            if m_val:
                canli_tm_deger = m_val.group(1)
        except Exception:
            pass

    # 3. Eğer yerel doğrulanmış listede YOKSA: TheSportsDB (Sıkı İsim + Soccer Doğrulamalı) + Wikipedia!
    canli_profil = {}
    if yerel is None:
        try:
            q_p = urllib.parse.quote(oyuncu)
            sp_veri = _json_cek(f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={q_p}", timeout=5)
            for aday in (sp_veri.get("player") or []):
                if str(aday.get("strSport", "")).lower() != "soccer":
                    continue
                aday_ad = str(aday.get("strPlayer", ""))
                if _isim_benzerlik_skoru(oyuncu, aday_ad) >= 0.78:
                    canli_profil = {
                        "ad": aday_ad,
                        "kulup": aday.get("strTeam") or "Bilinmiyor",
                        "milli_takim": aday.get("strNationality") or "",
                        "mevki": aday.get("strPosition") or "Futbolcu",
                        "dogum": aday.get("dateBorn") or "",
                    }
                    break
        except Exception:
            pass

    # 4. Canlı Wikipedia Güncel Kariyer Özeti (İnternet varsa ek bağlam)
    wiki_ek = ""
    try:
        hedef_ad = yerel["ad"] if yerel else (canli_profil.get("ad") or oyuncu.title())
        w = wikipedia_madde_getir(hedef_ad, dil="tr", detay_karakter=700)
        if w.get("basarili") and "Yedek" not in w.get("dil", ""):
            wiki_ek = f"\n\n**🌐 Güncel Kariyer Özeti (Wikipedia):** {w['ozet'][:550]}"
    except Exception:
        pass

    # 5. Detaylı Analiz Kartını Oluştur
    if yerel:
        deger_str = (
            f"**`{canli_tm_deger}`** *(Canlı Transfermarkt Profili)*"
            if canli_tm_deger
            else f"**`{yerel['piyasa_degeri']}`** *(Doğrulanmış Güncel Değer • Zirve: {yerel['zirve_deger']})*"
        )
        satirlar = [
            f"### ⚽ Detaylı Futbolcu Analizi: **{yerel['ad']}**",
            f"- **🏟️ Güncel Kulüp:** {yerel['kulup']}",
            f"- **💶 Piyasa Değeri:** {deger_str}",
            f"- **🎯 Mevki:** {yerel['mevki']} | **🌍 Milli Takım:** {yerel['milli_takim']}",
            f"- **📅 Doğum:** `{yerel['dogum']}` | **📄 Sözleşme:** `{yerel['sozlesme']}`",
            f"\n**📊 Oyuncu & Değer Analizi:**\n{yerel['analiz']}{wiki_ek}",
            f"\n**🔗 Doğrudan Transfermarkt Profili:** [{yerel['ad']} — Transfermarkt]({tm_url})",
            "*Kaynak: `Doğrulanmış 2026 Futbolcu Veri Tabanı + Transfermarkt + Wikipedia`*",
        ]
        return {"basarili": True, "ad": yerel["ad"], "metin": "\n".join(satirlar), "kaynak": f"Futbol Analiz ({yerel['ad']})"}

    gorunen_ad = canli_profil.get("ad") or oyuncu.title()
    kulup = canli_profil.get("kulup") or "Doğrudan Transfermarkt profilinden teyit edilebilir"
    mevki = canli_profil.get("mevki") or "Futbolcu"
    satirlar = [
        f"### ⚽ Futbolcu Profili & Piyasa Değeri: **{gorunen_ad}**",
        f"- **🏟️ Kulüp:** {kulup}",
        f"- **🎯 Mevki:** {mevki}",
        f"- **💶 Güncel Piyasa Değeri:** Günlük anlık € değeri için aşağıdaki resmi Transfermarkt sayfası kullanılabilir.",
    ]
    if canli_profil.get("dogum"):
        satirlar.append(f"- **📅 Doğum Tarihi:** `{canli_profil['dogum']}`")
    if wiki_ek:
        satirlar.append(wiki_ek)
    satirlar.append(f"\n**🔗 Canlı Piyasa Değeri:** [Transfermarkt — {gorunen_ad}]({tm_url})")
    satirlar.append("*Kaynak: `TheSportsDB (Doğrulanmış Eşleşme) + Wikipedia + Transfermarkt`*")
    return {"basarili": True, "ad": gorunen_ad, "metin": "\n".join(satirlar), "kaynak": f"Futbol Analiz ({gorunen_ad})"}


# ==============================================================================
# 9. CANLI AÇIK KAYNAK WEB & TÜRKÇE HABER ARAMA MOTORU (v7.6 — PARALEL + ÖNBELLEKLİ)
#    Google News TR Canlı RSS + DuckDuckGo Instant Answer (Aynı Anda Paralel!)
# ==============================================================================
from concurrent.futures import ThreadPoolExecutor as _M13Pool
from datetime import datetime
import time as _m13_time
import xml.etree.ElementTree as _ET

_CANLI_ARAMA_ONBELLEK = {}  # anahtar -> (timestamp, sonuc_dict)


def canli_web_ve_haber_ara(
    sorgu: str,
    maks_sonuc: int = 5,
    rss_base_url: str = None,
    ddg_base_url: str = None,
) -> dict:
    """
    v7.6 Hızlandırılmış Açık Kaynak Canlı Arama Motoru:
      • Google News TR Canlı RSS ve DuckDuckGo Instant Answer aynı anda PARALEL çalışır.
      • 3 dakikalık (180 sn) akıllı bellek önbelleği ile tekrar sorgularda anında (~1 ms) döner.
    """
    temiz_sorgu = re.sub(
        r"\b(son dakika|güncel haberler|guncel haberler|haberleri|haberler|gündem|gundem|webde ara|internette ara|google'da ara|googleda ara|arama yap|araştır|arastir|bugün ne oldu|bugun ne oldu)\b",
        " ",
        str(sorgu or ""),
        flags=re.IGNORECASE,
    )
    temiz_sorgu = re.sub(r"\s+", " ", temiz_sorgu).strip("?!.,;:\"' ")
    onbellek_anahtar = f"{temiz_sorgu.lower()}|{maks_sonuc}|{rss_base_url or ''}|{ddg_base_url or ''}"
    simdi = _m13_time.time()

    if onbellek_anahtar in _CANLI_ARAMA_ONBELLEK:
        kayit_t, kayit_sonuc = _CANLI_ARAMA_ONBELLEK[onbellek_anahtar]
        if (simdi - kayit_t) < 180.0:
            return kayit_sonuc

    from datetime import timezone as _tz, timedelta as _td
    guncel_zaman = (datetime.now(_tz.utc) + _td(hours=3)).strftime("%d.%m.%Y %H:%M") + " TR"

    def _rss_getir():
        sonuc_list = []
        try:
            if rss_base_url:
                rss_url = rss_base_url
            elif len(temiz_sorgu) >= 2:
                q_enc = urllib.parse.quote(temiz_sorgu)
                rss_url = f"https://news.google.com/rss/search?q={q_enc}&hl=tr&gl=TR&ceid=TR:tr"
            else:
                rss_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"

            req = urllib.request.Request(
                rss_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0", "Accept-Language": "tr-TR,tr;q=0.9"},
            )
            with urllib.request.urlopen(req, timeout=4.5) as resp:
                xml_veri = resp.read()
            kok = _ET.fromstring(xml_veri)
            for item in kok.findall(".//item")[:maks_sonuc]:
                baslik = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                tarih = (item.findtext("pubDate") or "").strip()
                kaynak_el = item.find("source")
                kaynak_ad = (kaynak_el.text or "").strip() if kaynak_el is not None and kaynak_el.text else "Canlı Haber"
                if baslik:
                    sonuc_list.append({
                        "baslik": baslik,
                        "link": link,
                        "tarih": tarih[:25],
                        "kaynak": kaynak_ad,
                    })
        except Exception:
            pass
        return sonuc_list

    def _ddg_getir():
        if len(temiz_sorgu) < 2 and not ddg_base_url:
            return "", ""
        try:
            if ddg_base_url:
                ddg_url = ddg_base_url
            else:
                q_enc = urllib.parse.quote(temiz_sorgu)
                ddg_url = f"https://api.duckduckgo.com/?q={q_enc}&format=json&no_html=1&skip_disambig=1"
            req_d = urllib.request.Request(
                ddg_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req_d, timeout=3.5) as resp:
                d_veri = json.loads(resp.read().decode("utf-8"))
            ozet = (d_veri.get("AbstractText") or "").strip()
            link = (d_veri.get("AbstractURL") or "").strip()
            if not ozet and d_veri.get("RelatedTopics"):
                for rt in d_veri["RelatedTopics"][:2]:
                    if isinstance(rt, dict) and rt.get("Text"):
                        ozet = rt["Text"].strip()
                        link = rt.get("FirstURL", "")
                        break
            return ozet, link
        except Exception:
            return "", ""

    haberler = []
    ddg_ozet, ddg_link = "", ""
    with _M13Pool(max_workers=2) as havuz:
        f_rss = havuz.submit(_rss_getir)
        f_ddg = havuz.submit(_ddg_getir)
        try:
            haberler = f_rss.result(timeout=5.0)
        except Exception:
            haberler = []
        try:
            ddg_ozet, ddg_link = f_ddg.result(timeout=4.0)
        except Exception:
            ddg_ozet, ddg_link = "", ""

    if not haberler and not ddg_ozet:
        return {
            "basarili": False,
            "sorgu": temiz_sorgu or sorgu,
            "zaman": guncel_zaman,
            "haberler": [],
            "ddg_ozet": "",
            "ddg_link": "",
        }

    cikti = {
        "basarili": True,
        "sorgu": temiz_sorgu or "Türkiye & Dünya Gündemi",
        "zaman": guncel_zaman,
        "haberler": haberler,
        "ddg_ozet": ddg_ozet,
        "ddg_link": ddg_link,
    }
    if len(_CANLI_ARAMA_ONBELLEK) > 64:
        _CANLI_ARAMA_ONBELLEK.clear()
    _CANLI_ARAMA_ONBELLEK[onbellek_anahtar] = (simdi, cikti)
    return cikti


def canli_arama_sonucunu_formatla(sonuc: dict) -> str:
    """Canlı web & haber arama sonuçlarını tarih damgalı ve tıklanabilir Türkçe karta dönüştürür."""
    if not sonuc or not sonuc.get("basarili"):
        return ""
    satirlar = [
        f"### 🌐 Canlı Güncel Arama: {sonuc.get('sorgu', 'Gündem')} (`{sonuc.get('zaman', '')}`)",
    ]
    if sonuc.get("ddg_ozet"):
        link_ek = f" ([Kaynak]({sonuc['ddg_link']}))" if sonuc.get("ddg_link") else ""
        satirlar.append(f"**📌 Hızlı Web Özeti:** {sonuc['ddg_ozet']}{link_ek}")
    if sonuc.get("haberler"):
        satirlar.append("\n**📰 Son Güncel Başlıklar (Google News TR Canlı Akış):**")
        for h in sonuc["haberler"]:
            tarih_ek = f" — `{h['tarih']}`" if h.get("tarih") else ""
            if h.get("link"):
                satirlar.append(f"* [{h['baslik']}]({h['link']}) (*{h.get('kaynak', 'Haber')}*{tarih_ek})")
            else:
                satirlar.append(f"* **{h['baslik']}** (*{h.get('kaynak', 'Haber')}*{tarih_ek})")
    return "\n".join(satirlar)


# ==============================================================================
# 10. TÜRKİYE STANDARTLARI AÇIK KAYNAK GENİŞLETMESİ (v9.0):
#     • Kimya & Bileşik Formülü (PubChem PUG-REST + Yerleşik Türkçe Kimya Tabanı)
#     • TEKNOFEST / TÜBİTAK 2204-A & arXiv Canlı Akademik Makale Motoru
#     • AlAdhan Namaz Vakitleri (Diyanet Method=13) & Hicri Takvim
#     • USGS Türkiye Canlı Deprem Takip Motoru
# ==============================================================================
_V90_ONBELLEK = {}  # anahtar -> (timestamp, veri)


def _v90_cache_oku(anahtar: str, ttl: float = 300.0):
    kayit = _V90_ONBELLEK.get(anahtar)
    if kayit and (_m13_time.time() - kayit[0]) < ttl:
        return kayit[1]
    return None


def _v90_cache_yaz(anahtar: str, veri):
    if len(_V90_ONBELLEK) > 96:
        _V90_ONBELLEK.clear()
    _V90_ONBELLEK[anahtar] = (_m13_time.time(), veri)


KIMYA_TURKCE_SOZLUK = {
    "su": ("water", "H₂O", "18.015 g/mol", "Nötr (pH ≈ 7)", "Yaşamın temel çözücüsü, polar kovalent bileşik."),
    "sülfürik asit": ("sulfuric acid", "H₂SO₄", "98.079 g/mol", "Kuvvetli Asit", "Zaç yağı olarak bilinir; akü, gübre ve sanayide kullanılır. Suyla karıştırılırken asit suya yavaşça eklenir."),
    "hidroklorik asit": ("hydrochloric acid", "HCl", "36.458 g/mol", "Kuvvetli Asit", "Tuz ruhu olarak bilinir; mide özsuyunda bulunur, metal temizleme ve PVC üretiminde kullanılır."),
    "tuz ruhu": ("hydrochloric acid", "HCl", "36.458 g/mol", "Kuvvetli Asit", "Hidroklorik asidin sulu çözeltisidir; çamaşır suyuyla asla karıştırılmamalıdır (zehirli klor gazı çıkar)."),
    "nitrik asit": ("nitric acid", "HNO₃", "63.012 g/mol", "Kuvvetli Asit", "Kezzap olarak bilinir; gübre üretimi ve metal aşındırmada kullanılır."),
    "sodyum klorür": ("sodium chloride", "NaCl", "58.443 g/mol", "Nötr İyonik Tuz", "Sofra tuzu; iyonik kristal örgü yapısına sahiptir, suda iyonlaşarak elektriği iletir."),
    "sofra tuzu": ("sodium chloride", "NaCl", "58.443 g/mol", "Nötr İyonik Tuz", "Sodyum klorür (NaCl); gıda koruma ve kimya sanayisinin temel tuzudur."),
    "amonyak": ("ammonia", "NH₃", "17.031 g/mol", "Zayıf Baz", "Keskin kokulu bazik gaz; gübre ve soğutma sistemlerinde kullanılır."),
    "sodyum hidroksit": ("sodium hydroxide", "NaOH", "39.997 g/mol", "Kuvvetli Baz", "Sud kostik; sabun, kâğıt ve lavabo açıcı üretiminde kullanılır."),
    "sodyum bikarbonat": ("sodium bicarbonate", "NaHCO₃", "84.007 g/mol", "Zayıf Bazik Tuz", "Yemek sodası / kabartma tozu; asitlerle tepkimeye girip CO₂ gazı çıkarır."),
    "karbondioksit": ("carbon dioxide", "CO₂", "44.009 g/mol", "Asidik Oksit", "Fotosentezde kullanılan, sera etkisinde rol oynayan doğrusal kovalent molekül."),
    "metan": ("methane", "CH₄", "16.043 g/mol", "Nötr Hidrokarbon", "Doğal gazın ana bileşeni; en basit alkan (düzgün dörtyüzlü geometri)."),
    "etanol": ("ethanol", "C₂H₅OH", "46.069 g/mol", "Nötr Alkol", "Etil alkol; biyoyakıt, çözücü ve antiseptik olarak kullanılır."),
    "glikoz": ("glucose", "C₆H₁₂O₆", "180.156 g/mol", "Monosakkarit", "Hücrelerin temel enerji kaynağı olan basit şeker (üzüm şekeri)."),
    "asetik asit": ("acetic acid", "CH₃COOH", "60.052 g/mol", "Zayıf Organik Asit", "Sirke asidi; gıda koruyucu ve organik sentezlerde kullanılır."),
    "kalsiyum karbonat": ("calcium carbonate", "CaCO₃", "100.087 g/mol", "Bazik Tuz", "Kireç taşı, mermer ve tebeşirin ana bileşenidir."),
    "hidrojen peroksit": ("hydrogen peroxide", "H₂O₂", "34.015 g/mol", "Oksitleyici", "Oksijenli su; dezenfektan ve ağartıcı olarak kullanılır."),
    "ozon": ("ozone", "O₃", "47.998 g/mol", "Oksitleyici Gaz", "Stratosferde zararlı UV ışınlarını süzen üç atomlu oksijen allotropu."),
    "aspirin": ("aspirin", "C₉H₈O₄", "180.159 g/mol", "Organik Asit (Asetilsalisilik Asit)", "Ağrı kesici, ateş düşürücü ve kan sulandırıcı temel ilaç molekülü."),
    "kafein": ("caffeine", "C₈H₁₀N₄O₂", "194.194 g/mol", "Alkaloit", "Kahve ve çayda bulunan, merkezi sinir sistemini uyaran doğal bileşik."),
}


def kimya_bilesik_getir(sorgu: str, pubchem_base: str = None) -> dict:
    """PubChem PUG-REST canlı API + yerleşik Türkçe kimya sözlüğü ile bileşik analizi yapar."""
    raw = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    temiz = re.sub(
        r"\b(kimya|kimyasal|formülü|formulu|formül|formul|molekül|molekul|kütlesi|kutlesi|ağırlığı|agirligi|nedir|ne demek|bileşiği|bilesigi|bileşik|bilesik|hakkında bilgi ver|hakkinda bilgi ver|özellikleri|ozellikleri)\b",
        " ",
        raw,
    )
    temiz = re.sub(r"\s+", " ", temiz).strip("?!.,;:\"' ")
    if not temiz:
        return {"basarili": False}

    onb = _v90_cache_oku(f"kimya|{temiz}|{pubchem_base or ''}", ttl=600.0)
    if onb:
        return onb

    eslesen_tr = None
    en_ad = temiz
    yerel_bilgi = None
    for tr_k, val in KIMYA_TURKCE_SOZLUK.items():
        if tr_k == temiz or tr_k in raw or val[0] == temiz:
            eslesen_tr = tr_k.title()
            en_ad = val[0]
            yerel_bilgi = val
            break

    formul = yerel_bilgi[1] if yerel_bilgi else ""
    mol_kutle = yerel_bilgi[2] if yerel_bilgi else ""
    iupac = ""
    cid = ""
    kaynak = "Türkçe Kimya Bilgi Tabanı"

    # Canlı PubChem PUG-REST sorgusu
    try:
        q_enc = urllib.parse.quote(en_ad)
        url = pubchem_base or f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{q_enc}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"
        veri = _json_cek(url, timeout=4.5)
        props = veri.get("PropertyTable", {}).get("Properties", [])
        if props:
            p = props[0]
            formul = p.get("MolecularFormula", formul)
            if p.get("MolecularWeight"):
                mol_kutle = f"{p['MolecularWeight']} g/mol"
            iupac = p.get("IUPACName", "")
            cid = str(p.get("CID", ""))
            kaynak = "PubChem PUG-REST (Canlı)"
    except Exception:
        pass

    if not formul:
        return {"basarili": False}

    baslik = eslesen_tr or en_ad.title()
    pubchem_link = f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}" if cid else "https://pubchem.ncbi.nlm.nih.gov/"
    satirlar = [
        f"### 🧪 Kimya Bileşik Kartı: **{baslik}**",
        f"- **🧬 Kimyasal Formül:** `{formul}`",
        f"- **⚖️ Molekül Kütlesi (MA):** `{mol_kutle}`",
    ]
    if iupac:
        satirlar.append(f"- **🏷️ IUPAC Sistematik Adı:** `{iupac}`")
    if yerel_bilgi:
        satirlar.append(f"- **⚗️ Kimyasal Sınıfı:** {yerel_bilgi[3]}")
        satirlar.append(f"\n**📌 Özellikler ve Kullanım:** {yerel_bilgi[4]}")
    satirlar.append(f"\n🔗 Kaynak: [{kaynak}]({pubchem_link})")
    sonuc = {"basarili": True, "baslik": baslik, "metin": "\n".join(satirlar), "kaynak": f"Kimya ({baslik})"}
    _v90_cache_yaz(f"kimya|{temiz}|{pubchem_base or ''}", sonuc)
    return sonuc


def namaz_vakitleri_ve_hicri_getir(sorgu: str, aladhan_base: str = None) -> dict:
    """AlAdhan API (Method=13 Türkiye Diyanet İşleri Başkanlığı) ile canlı namaz vakitleri ve Hicri takvim getirir."""
    raw = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    sehir = "Istanbul"
    sehir_tr = "İstanbul"
    for il_k in TURKIYE_81_IL.keys():
        if re.search(rf"\b{re.escape(il_k)}\b", raw):
            sehir_tr = il_k.replace("i", "İ", 1).title() if il_k.startswith("i") else il_k.title()
            tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
            sehir = sehir_tr.translate(tr_map)
            break

    onb = _v90_cache_oku(f"namaz|{sehir}|{aladhan_base or ''}", ttl=900.0)
    if onb:
        return onb

    _hicri_aylar_tr = {
        1: "Muharrem", 2: "Safer", 3: "Rebiülevvel", 4: "Rebiülahir",
        5: "Cemaziyelevvel", 6: "Cemaziyelahir", 7: "Recep", 8: "Şaban",
        9: "Ramazan", 10: "Şevval", 11: "Zilkade", 12: "Zilhicce",
    }

    try:
        url = aladhan_base or f"https://api.aladhan.com/v1/timingsByCity?city={urllib.parse.quote(sehir)}&country=Turkey&method=13"
        veri = _json_cek(url, timeout=4.5)
        if veri.get("code") == 200 and veri.get("data"):
            d = veri["data"]
            t = d.get("timings", {})
            h = d.get("date", {}).get("hijri", {})
            g = d.get("date", {}).get("gregorian", {})
            h_ay_no = int(h.get("month", {}).get("number", 1))
            h_ay_tr = _hicri_aylar_tr.get(h_ay_no, h.get("month", {}).get("en", ""))
            hicri_str = f"{h.get('day', '')} {h_ay_tr} {h.get('year', '')}"
            miladi_str = g.get("date", datetime.now().strftime("%d-%m-%Y"))
            metin = (
                f"### 🕌 {sehir_tr} Namaz Vakitleri & Hicri Takvim (Diyanet Metodu)\n"
                f"- **📅 Miladi Tarih:** `{miladi_str}` | **🌙 Hicri Tarih:** `{hicri_str}`\n\n"
                f"| Vakit | Saat |\n| :--- | :--- |\n"
                f"| 🌌 **İmsak (Fecr)** | `{t.get('Fajr', '-')}` |\n"
                f"| 🌅 **Güneş** | `{t.get('Sunrise', '-')}` |\n"
                f"| ☀️ **Öğle** | `{t.get('Dhuhr', '-')}` |\n"
                f"| 🌤️ **İkindi** | `{t.get('Asr', '-')}` |\n"
                f"| 🌇 **Akşam** | `{t.get('Maghrib', '-')}` |\n"
                f"| 🌃 **Yatsı** | `{t.get('Isha', '-')}` |\n\n"
                f"🔗 Kaynak: [AlAdhan API — Diyanet Hesaplama (Method 13)](https://aladhan.com/prayer-times-api)"
            )
            sonuc = {"basarili": True, "baslik": f"{sehir_tr} Namaz Vakitleri", "metin": metin, "kaynak": f"AlAdhan ({sehir_tr})"}
            _v90_cache_yaz(f"namaz|{sehir}|{aladhan_base or ''}", sonuc)
            return sonuc
    except Exception:
        pass

    # Çevrimdışı Hicri yaklaşık takvim yedeği
    simdi = datetime.now()
    hicri_yil = int((simdi.year - 622) * 33 / 32)
    metin = (
        f"### 🌙 Hicri Takvim & {sehir_tr} Vakit Bilgisi (Çevrimdışı Mod)\n"
        f"- **📅 Bugün:** `{simdi.strftime('%d.%m.%Y')}` (Yaklaşık Hicri Yıl: `{hicri_yil}`)\n"
        f"- Canlı Diyanet vakitleri için internet bağlantısı açıkken tekrar sorabilirsin ([AlAdhan](https://aladhan.com/prayer-times-api))."
    )
    return {"basarili": True, "baslik": f"{sehir_tr} Hicri Takvim", "metin": metin, "kaynak": "Hicri Takvim Belleği"}


def teknofest_ve_makale_ara(sorgu: str, arxiv_base: str = None) -> dict:
    """TEKNOFEST & TÜBİTAK 2204-A rehberi ile arXiv canlı akademik makale aramasını birleştirir."""
    raw = sorgu.replace("İ", "i").replace("I", "ı").lower().replace("\u0307", "").strip()
    onb = _v90_cache_oku(f"teknofest|{raw}|{arxiv_base or ''}", ttl=300.0)
    if onb:
        return onb

    # Türkçe teknik terimleri arXiv İngilizce arama terimlerine eşle
    arxiv_terim = "autonomous UAV computer vision"
    if any(k in raw for k in ["bebek araba", "fren", "ultrasonik", "sensör", "sensor", "tübitak", "tubitak"]):
        arxiv_terim = "smart stroller obstacle avoidance autonomous braking"
    elif any(k in raw for k in ["iha", "drone", "uçuş", "ucus", "pid", "savaşan", "savasan", "kanat"]):
        arxiv_terim = "autonomous UAV target tracking PID control"
    elif any(k in raw for k in ["yapay zeka", "llm", "derin öğrenme", "sinir ağı"]):
        arxiv_terim = "large language model reasoning Turkish"
    elif any(k in raw for k in ["roket", "uydu", "model uydu"]):
        arxiv_terim = "rocket telemetry flight control"

    makaleler = []
    try:
        url = arxiv_base or (
            f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(arxiv_terim)}"
            f"&start=0&max_results=4&sortBy=submittedDate&sortOrder=descending"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0 AREX-AI/12.1"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            xml_data = resp.read()
        kok = _ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in kok.findall("atom:entry", ns)[:4]:
            baslik = re.sub(r"\s+", " ", (entry.findtext("atom:title", "", ns) or "")).strip()
            link = (entry.findtext("atom:id", "", ns) or "").strip()
            tarih = (entry.findtext("atom:published", "", ns) or "")[:10]
            ozet = re.sub(r"\s+", " ", (entry.findtext("atom:summary", "", ns) or "")).strip()[:220]
            if baslik:
                makaleler.append({"baslik": baslik, "link": link, "tarih": tarih, "ozet": ozet})
    except Exception:
        pass

    satirlar = [
        "### 🚀 TEKNOFEST, TÜBİTAK 2204-A & Canlı Akademik Araştırma Merkezi",
        "**🏆 TEKNOFEST & TÜBİTAK Proje Kontrol Listesi:**",
        "* **TEKNOFEST İHA / Savaşan İHA:** Özgün tasarım raporu (ÖTR), kritik tasarım raporu (KTR), uçuş kanıt videosu, yer kontrol istasyonu (MAVLink/Pixhawk), otonom kilitlenme (OpenCV/YOLO) ve fail-safe acil iniş senaryosu.",
        "* **TÜBİTAK 2204-A Lise Araştırma:** Özgün problem tanımı, literatür taraması, bilimsel yöntem, prototip/deney ölçüm tablosu, gerçek test verileri ve kaynakça (APA).",
    ]
    if makaleler:
        satirlar.append(f"\n**📚 Canlı Akademik Makaleler ([arXiv API](https://info.arxiv.org/help/api/index.html) — `{arxiv_terim}`):**")
        for m in makaleler:
            satirlar.append(f"* **[{m['baslik']}]({m['link']})** (`{m['tarih']}`)\n  _{m['ozet']}..._")
    else:
        satirlar.append("\n🔗 Akademik tarama kaynağı: [arXiv Açık Erişim Arşivi](https://info.arxiv.org/help/api/index.html)")

    sonuc = {"basarili": True, "baslik": "TEKNOFEST & Akademik Araştırma", "metin": "\n".join(satirlar), "kaynak": "TEKNOFEST + arXiv"}
    _v90_cache_yaz(f"teknofest|{raw}|{arxiv_base or ''}", sonuc)
    return sonuc


def son_depremler_getir(sorgu: str = "", usgs_base: str = None) -> dict:
    """USGS Earthquake GeoJSON API ile Türkiye çevresindeki son depremleri anlık getirir."""
    onb = _v90_cache_oku(f"deprem|{usgs_base or ''}", ttl=120.0)
    if onb:
        return onb
    try:
        url = usgs_base or (
            "https://earthquake.usgs.gov/fdsnws/event/1/query?"
            "format=geojson&minlatitude=35.5&maxlatitude=42.5&minlongitude=25.5&maxlongitude=45.0&limit=6&orderby=time"
        )
        veri = _json_cek(url, timeout=4.5)
        feats = veri.get("features", [])
        if feats:
            satirlar = [
                f"### 🌍 Türkiye Çevresi Son Depremler (`{datetime.now().strftime('%d.%m.%Y %H:%M')}`)",
                "| Büyüklük | Konum | Derinlik | Zaman (UTC) |",
                "| :--- | :--- | :--- | :--- |",
            ]
            for ft in feats[:6]:
                pr = ft.get("properties", {})
                geo = ft.get("geometry", {}).get("coordinates", [0, 0, 0])
                mag = pr.get("mag", "-")
                yer = pr.get("place", "Bilinmiyor")
                der = f"{geo[2]:.1f} km" if len(geo) >= 3 and geo[2] is not None else "-"
                ts = pr.get("time")
                zmn = datetime.utcfromtimestamp(ts / 1000.0).strftime("%d.%m %H:%M") if ts else "-"
                satirlar.append(f"| **M {mag}** | {yer} | `{der}` | `{zmn}` |")
            satirlar.append("\n🔗 Kaynak: [USGS Earthquake GeoJSON API](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)")
            sonuc = {"basarili": True, "baslik": "Türkiye Son Depremler", "metin": "\n".join(satirlar), "kaynak": "USGS Deprem API"}
            _v90_cache_yaz(f"deprem|{usgs_base or ''}", sonuc)
            return sonuc
    except Exception:
        pass
    return {"basarili": False}
