# -*- coding: utf-8 -*-
"""
AREX AI Studio — otomatik regresyon testleri (internetsiz).

Çalıştırma (proje klasöründe):
    python -m unittest tests/test_arex.py -v

Ağ erişimi testler boyunca kapatılır; yapay zekâ/servis çağrısı yapılmaz,
kişisel veri dosyaları geçici klasöre yönlendirilir.
"""

import contextlib
import io
import json
import logging
import os
import random
import socket
import sys
import tempfile
import time
import unittest
import urllib.request
import warnings
import zipfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
os.chdir(KOK)
warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)


def _ag_kapali(*_a, **_k):
    raise OSError("testlerde ağ kapalı")


_GERCEK_URLOPEN, _GERCEK_BAGLANTI = urllib.request.urlopen, socket.create_connection
urllib.request.urlopen = _ag_kapali
socket.create_connection = _ag_kapali

import modul_14_pro_matematik as m14  # noqa: E402
import modul_16_guncel_asistan as m16  # noqa: E402
import modul_17_medya_ve_grafik as m17  # noqa: E402
import modul_18_calisma_kocu as m18  # noqa: E402
import modul_19_cevap_varyantlari as m19  # noqa: E402
import modul_20_yedekleme as m20  # noqa: E402
import modul_21_ogrenci_araclari as m21  # noqa: E402
import modul_22_plan_ve_formuller as m22  # noqa: E402
import modul_23_erisim as m23  # noqa: E402
import modul_24_kalici_depo as m24  # noqa: E402


def _sonuc(metin):
    cevap, _ = m14.pro_matematik_coz(metin)
    return cevap or ""


class ProMatematik(unittest.TestCase):
    def test_islem_onceligi_ve_us(self):
        self.assertIn("`14`", _sonuc("2+3*4"))
        self.assertIn("`-9`", _sonuc("-3^2"))
        self.assertIn("`512`", _sonuc("2^3^2"))
        self.assertIn("`14`", _sonuc("2(3+4)"))

    def test_kesir_ve_kok(self):
        self.assertIn("5/2", _sonuc("10/4"))
        self.assertIn("3/10", _sonuc("0.1+0.2"))
        self.assertIn("4√3", _sonuc("√27 + √3"))
        self.assertIn("√2/2", _sonuc("1/√2"))

    def test_trigonometri_ve_log(self):
        self.assertIn("1/2", _sonuc("sin 30"))
        self.assertIn("√2/2", _sonuc("sin 45"))
        self.assertIn("`2`", _sonuc("log 100"))
        self.assertIn("tanımsız", _sonuc("tan 90"))

    def test_denklemler(self):
        self.assertIn("x = 5", _sonuc("3(x-2)=x+4"))
        self.assertIn("Ç = {2, 3}", _sonuc("x^2-5x+6=0"))
        self.assertIn("reel kök yoktur", _sonuc("x^2+x+1=0"))
        self.assertIn("sonsuz çözüm", _sonuc("2x=2x"))

    def test_turkce_kaliplar(self):
        self.assertIn("2³", _sonuc("120'nin asal çarpanları"))
        self.assertIn("asal değildir", _sonuc("91 asal mı"))
        self.assertIn("120", _sonuc("80'e yüzde 50 zam"))
        self.assertIn("%25", _sonuc("20 80'in yüzde kaçı"))

    def test_matematik_olmayan_metinler(self):
        for metin in ("merhaba nasılsın", "1-2 gün sonra gel", "fenerbahçe 3-1 kazandı", "5", "saat 10:30"):
            self.assertIsNone(m14.pro_matematik_coz(metin)[0], metin)


class GuncelAsistanInternetsiz(unittest.TestCase):
    def _y(self, metin):
        return m16.guncel_asistan_yanitla(metin)[0] or ""

    def test_birim_cevirici(self):
        self.assertIn("3,1069 mil", self._y("5 km kaç mil"))
        self.assertIn("400 ml", self._y("2 su bardağı kaç ml"))
        self.assertIn("37,7778", self._y("100 fahrenheit kaç celsius"))

    def test_tarih(self):
        self.assertIn("Cuma", self._y("1 ocak 2027 hangi gün"))
        self.assertIn("geçerli değil", self._y("31.02.2026 hangi gün"))
        self.assertIn("gün", self._y("1.1.2026 ile 20.11.2026 arası kaç gün"))

    def test_dunya_saati(self):
        self.assertIn("Tokyo", self._y("tokyo'da saat kaç"))
        self.assertEqual(self._y("saat kaç"), "")

    def test_alakasiz_metinlere_karismaz(self):
        for metin in ("merhaba", "atatürk kimdir", "2+2", "bana fotosentezi hatırlat"):
            self.assertIsNone(m16.guncel_asistan_yanitla(metin)[0], metin)


class GoreliTarih(unittest.TestCase):
    def test_n_gun_sonra_ne_gun(self):
        from datetime import timedelta
        bugun = m16._simdi().date()
        hedef = bugun + timedelta(days=3)
        cevap = m16.guncel_asistan_yanitla("3 gün sonra ne gün")[0]
        self.assertIn(f"**{hedef.day} {m16._AYLAR[hedef.month - 1]} {hedef.year}, {m16._GUNLER[hedef.weekday()]}**", cevap)
        hedef = bugun - timedelta(days=14)
        self.assertIn(f"{hedef.day} {m16._AYLAR[hedef.month - 1]}", m16.guncel_asistan_yanitla("2 hafta önce hangi gündü")[0])
        self.assertIsNone(m16.guncel_asistan_yanitla("3 gün sonra arayacağım")[0])

    def test_saat_dilimi_sabitlenmis(self):
        with open(os.path.join(KOK, "main.py"), encoding="utf-8") as f:
            kaynak = f.read()
        # Bulut sunucusu UTC'dir: main.py, streamlit içe aktarılmadan önce saat dilimini İstanbul'a sabitlemeli
        self.assertLess(kaynak.index('os.environ["TZ"] = "Europe/Istanbul"'), kaynak.index("import streamlit as st"))


class WikipediaKonu(unittest.TestCase):
    def test_iyelik_ayirma(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            import modul_10_wikipedia as m10
        self.assertEqual(m10.iyelik_ayir("fransanın başkenti"), ("fransa'nın başkenti", "fransa", "başkenti"))
        # belirsiz bölünmelerde her iki kök de aday olmalı (doğrusunu Wikipedia seçer)
        self.assertIn("newton", [k for _, k, _ in m10.iyelik_adaylari("newtonun hareket yasaları")])
        self.assertIn("fransa", [k for _, k, _ in m10.iyelik_adaylari("fransanın başkenti")])
        self.assertIn("türkiye", [k for _, k, _ in m10.iyelik_adaylari("türkiyenin başkenti")])
        self.assertIn("einstein", [k for _, k, _ in m10.iyelik_adaylari("einsteinın görelilik teorisi")])
        for konu in ("yapay zeka", "fotosentez", "mısır piramitleri", "osmanlı imparatorluğu"):
            self.assertIsNone(m10.iyelik_ayir(konu), konu)

    def test_soru_sonu_temizligi(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            import modul_10_wikipedia as m10
        self.assertEqual(m10.wikipedia_konu_ayikla("istanbulun fethi ne zaman"), "istanbulun fethi")
        self.assertEqual(m10.wikipedia_konu_ayikla("almanyanın nüfusu kaç"), "almanyanın nüfusu")
        self.assertEqual(m10.wikipedia_konu_ayikla("dünyanın en uzun nehri hangisi"), "dünyanın en uzun nehri")
        # "ar" (eski asistan adı) yalnızca ayrı kelimeyse silinmeli: "arşimet" → "şimet" OLMAMALI
        for soru, konu in (("arşimet kimdir", "arşimet"), ("arjantin nerede", "arjantin"), ("ar: fotosentez nedir", "fotosentez"),
                           ("pekin nerede", "pekin"), ("peki ya mars", "mars"), ("selamlar nasılsın", "selamlar nasılsın")):
            self.assertEqual(m10.wikipedia_konu_ayikla(soru), konu, soru)


class GrafikCizici(unittest.TestCase):
    def test_parabol_analizi(self):
        cevap, etiket = m17.grafik_ciz("y = -x^2 + 2x + 3 grafiğini çiz")
        self.assertEqual(etiket, "📈 Grafik Çizici")
        metin, svg = m17.svg_ayikla(cevap)
        self.assertIn("T(1, 4)", metin)
        self.assertIn("x = -1", metin)
        self.assertIn("x = 3", metin)
        self.assertTrue(svg and svg.startswith("<svg"))

    def test_kok_bulma_ve_tanim_kumesi(self):
        self.assertIn("x ≈ 0", m17.svg_ayikla(m17.grafik_ciz("y = √x grafiği")[0])[0])
        self.assertIn("kesmiyor", m17.svg_ayikla(m17.grafik_ciz("y = 1/x grafiği -5 ile 5 arasında")[0])[0])

    def test_grafik_olmayan(self):
        for metin in ("merhaba", "resim çiz", "grafik nedir"):
            self.assertIsNone(m17.grafik_ciz(metin)[0], metin)

    def test_youtube_kimligi(self):
        self.assertEqual(m17.youtube_kimligi("bak https://youtu.be/aircAruvnKk"), "aircAruvnKk")
        self.assertEqual(m17.youtube_kimligi("https://www.youtube.com/watch?v=aircAruvnKk&t=3"), "aircAruvnKk")
        self.assertIsNone(m17.youtube_kimligi("youtube nedir"))

    def test_sik_saglamasi(self):
        siklar = m17._siklari_bul(["Soru\nA)19 B)21 C)23 D)25"])
        self.assertEqual(siklar, {"A": "19", "B": "21", "C": "23", "D": "25"})
        self.assertTrue(m17._cevap_sikka_uyuyor_mu("**Cevap:** B) 21", siklar))
        self.assertFalse(m17._cevap_sikka_uyuyor_mu("**Cevap:** 340,745", siklar))


class CalismaKocu(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        m18.TAKIP_DOSYASI = os.path.join(self.klasor, "takip.json")
        m18.AYAR_DOSYASI = os.path.join(self.klasor, "ayar.json")
        m18.HATIRLATICI_DOSYASI = os.path.join(self.klasor, "hat.json")
        m18.YANLIS_DOSYASI = os.path.join(self.klasor, "yanlis.json")
        self.oturum = {}

    def _y(self, metin):
        return m18.calisma_kocu_yanitla(metin, self.oturum)

    def test_yanlis_defteri(self):
        random.seed(2)
        self._y("bana 2 matematik sorusu sor")
        self._y("999999")
        self.assertIn("**2** soru yanlış defterine eklendi", self._y("geç")[0])
        defter = self._y("yanlış defterim")[0]
        self.assertIn("2 kayıt", defter)
        for _ in range(2):
            self._y("yanlışlarımı tekrar et")
            while "arex_test" in self.oturum:
                d = self.oturum["arex_test"]
                self._y(str(d["sorular"][d["sira"]]["cevap"]))
        self.assertIn("boş", self._y("yanlış defterim")[0])
        self.assertIn("eklendi (#", self._y("yanlış defterine ekle: zincir kuralını unuttum")[0])

    def test_takip_ve_rapor(self):
        self.assertIn("Kaydettim: Matematik", self._y("bugün 30 matematik sorusu çözdüm")[0])
        self.assertIn("Fizik", self._y("fizikten 15 soru çözdüm 40 dakika")[0])
        rapor = self._y("bu hafta ne kadar çalıştım")[0]
        self.assertIn("45 soru", rapor)
        self.assertIn("<!--AREX_SVG:", rapor)

    def test_test_modu(self):
        random.seed(1)
        self.assertIn("testi başlıyor", self._y("köklü sayılardan bana 2 soru sor")[0])
        dogru = self.oturum["arex_test"]["sorular"][0]["cevap"]
        self.assertIn("Doğru", self._y(dogru.replace("√", " kök "))[0])
        self.assertIn("Test bitti", self._y("geç")[0])
        self.assertNotIn("arex_test", self.oturum)

    def test_hatirlatici(self):
        cevap = self._y("yarın 8'de fizik sınavımı hatırlat")[0]
        self.assertIn("08:00", cevap)
        self.assertIn("calendar.google.com", cevap)
        self.assertIsNone(self._y("bana fotosentezi hatırlat")[0])
        self.assertIn("Fizik sınavımı", self._y("hatırlatıcılarım")[0])

    def test_gecmis_zaman_test_baslatmaz(self):
        self.assertIn("Çalışma", self._y("fizikten 15 soru çözdüm")[1])


class CevapVaryantlari(unittest.TestCase):
    def test_cesitlilik_ve_tekrar_yok(self):
        orijinal = "Merhaba Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?"
        secimler = [m19.cevabi_cesitlendir(orijinal, "💬 Selamlaşma (merhaba)") for _ in range(12)]
        self.assertGreaterEqual(len(set(secimler)), 3)
        self.assertFalse(any(a == b for a, b in zip(secimler, secimler[1:])))

    def test_cift_selam_ve_eski_ad(self):
        cift = "Merhaba Ahmet! ⚡ Merhaba Ahmet! ⚡ Hoş geldin, sana nasıl yardımcı olabilirim?"
        self.assertEqual(m19.cevabi_cesitlendir(cift, "x").count("Merhaba"), 1)
        eski = "Benim adım Ar. Ahmet tarafından Python ve Streamlit kullanılarak geliştirilen akıllı bir yapay zeka asistanıyım."
        for _ in range(6):
            self.assertIn("AREX", m19.cevabi_cesitlendir(eski, "x"))

    def test_ai_cevaplarina_dokunmaz(self):
        self.assertEqual(m19.cevabi_cesitlendir("🧮 2+2=4", "🧠 Otonom Akış: Matematik"), "🧮 2+2=4")


class Yedekleme(unittest.TestCase):
    def test_yedek_ve_guvenli_geri_yukleme(self):
        klasor = tempfile.mkdtemp()
        eski_kok = m20._KOK
        m20._KOK = klasor
        try:
            with open(os.path.join(klasor, "komutlar.json"), "w", encoding="utf-8") as f:
                json.dump({"a": {"kelimeler": ["x"], "yanit": "y"}}, f)
            veri, dahil = m20.yedek_zip_olustur()
            self.assertEqual(dahil, ["komutlar.json"])
            with open(os.path.join(klasor, "komutlar.json"), "w") as f:
                f.write("{}")
            tamam, _, hata = m20.yedekten_geri_yukle(veri)
            self.assertIsNone(hata)
            with open(os.path.join(klasor, "komutlar.json"), encoding="utf-8") as f:
                self.assertIn("yanit", f.read())
            kotu = io.BytesIO()
            with zipfile.ZipFile(kotu, "w") as z:
                z.writestr("../kaçak.json", "{}")
                z.writestr("main.py", "x")
                z.writestr("ahmet_notlar.json", "{bozuk")
            tamam, atlanan, hata = m20.yedekten_geri_yukle(kotu.getvalue())
            self.assertEqual(tamam, [])
            self.assertEqual(len(atlanan), 3)
        finally:
            m20._KOK = eski_kok


class OgrenciAraclari(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        self._eski = (m18.AYAR_DOSYASI, m18.HATIRLATICI_DOSYASI)
        m18.AYAR_DOSYASI = os.path.join(self.klasor, "ayar.json")
        m18.HATIRLATICI_DOSYASI = os.path.join(self.klasor, "hat.json")
        m21.SINAV_DOSYASI = os.path.join(self.klasor, "sinav.json")
        m21.KART_DOSYASI = os.path.join(self.klasor, "kart.json")
        m21.DENEME_DOSYASI = os.path.join(self.klasor, "deneme.json")
        self.oturum = {}

    def tearDown(self):
        m18.AYAR_DOSYASI, m18.HATIRLATICI_DOSYASI = self._eski

    def _y(self, metin):
        return m21.ogrenci_araclari_yanitla(metin, self.oturum)

    def test_net_hesaplama(self):
        self.assertIn("Net: 37**", self._y("40 doğru 12 yanlış kaç net")[0])
        self.assertIn("Net: 14**", self._y("lgs 15 doğru 3 yanlış")[0])
        tablo = self._y("türkçe 30 doğru 6 yanlış matematik 22 doğru 8 yanlış")[0]
        self.assertIn("**48,5**", tablo)
        self.assertIn("Türkçe", tablo)

    def test_sinav_takvimi(self):
        self.assertIn("Kaydettim (#1)", self._y("fizik sınavım 5 aralıkta")[0])
        self.assertIn("Fizik sınavı", self._y("sınavlarıma kaç gün kaldı")[0])
        self.assertIn("silindi", self._y("#1 sınavı sil")[0])
        self.assertIsNone(self._y("yarın fizik sınavım var çok stresliyim")[0])

    def test_pomodoro_hatirlatici_kurar(self):
        self.assertIn("Pomodoro başladı", self._y("pomodoro başlat")[0])
        with open(m18.HATIRLATICI_DOSYASI, encoding="utf-8") as f:
            self.assertIn("Pomodoro bitti", json.load(f)[0]["baslik"])

    def test_kartlar_leitner(self):
        random.seed(3)
        self.assertIn("2 kart eklendi", self._y("kart ekle: apple = elma; book = kitap")[0])
        self.assertIn("Kart tekrarı başladı", self._y("kartları çalış")[0])
        with open(m21.KART_DOSYASI, encoding="utf-8") as f:
            kartlar = json.load(f)
        ilk = kartlar[self.oturum["arex_kart"]["sira"][0]]
        self.assertIn("✅", self._y(ilk["arka"])[0])
        self.assertIn("Tekrar bitti", self._y("bilmiyorum")[0])
        with open(m21.KART_DOSYASI, encoding="utf-8") as f:
            kutular = sorted(k["kutu"] for k in json.load(f))
        self.assertEqual(kutular, [1, 2])

    def test_deneme_takibi(self):
        self.assertIn("Deneme #1 kaydedildi", self._y("deneme: tyt türkçe 28 doğru 8 yanlış matematik 18 doğru 10 yanlış")[0])
        self.assertIn("+8,75 net", self._y("deneme: tyt türkçe 31 doğru 5 yanlış matematik 22 doğru 6 yanlış")[0])
        # farklı ders yapısı karşılaştırılmaz
        self.assertNotIn("Önceki", self._y("tyt deneme 40 doğru 12 yanlış")[0])
        self.assertIn("<!--AREX_SVG:", self._y("deneme: tyt türkçe 33 doğru 3 yanlış matematik 25 doğru 5 yanlış")[0] + self._y("denemelerim")[0])
        self.assertIn("Matematik", self._y("denemelerim")[0])
        self.assertIsNone(self._y("deneme sınavında stres yapıyorum ne yapmalıyım")[0])

    def test_hazir_deste(self):
        self.assertIn("35 yeni kart", self._y("başkentler destesini yükle")[0])
        self.assertIn("zaten", self._y("başkentler destesini yükle")[0])
        for anahtar, (_ad, kartlar) in m21.HAZIR_DESTELER.items():
            self.assertEqual(len({k[0] for k in kartlar}), len(kartlar), anahtar)

    def test_ilgisiz_sorulara_karismaz(self):
        for soru in ("internet nedir", "2+3*4", "fotosentez nedir", "yks ne zaman", "bana 5 matematik sorusu sor"):
            self.assertIsNone(self._y(soru)[0], soru)


class PlanVeFormuller(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        self._eski = (m18.AYAR_DOSYASI, m18.TAKIP_DOSYASI, m21.SINAV_DOSYASI, m21.DENEME_DOSYASI)
        m18.YANLIS_DOSYASI = os.path.join(self.klasor, "yanlis.json")
        m18.HATIRLATICI_DOSYASI = os.path.join(self.klasor, "hat.json")
        m21.KART_DOSYASI = os.path.join(self.klasor, "kart.json")
        m18.AYAR_DOSYASI = os.path.join(self.klasor, "ayar.json")
        m18.TAKIP_DOSYASI = os.path.join(self.klasor, "takip.json")
        m21.SINAV_DOSYASI = os.path.join(self.klasor, "sinav.json")
        m21.DENEME_DOSYASI = os.path.join(self.klasor, "deneme.json")

    def tearDown(self):
        m18.AYAR_DOSYASI, m18.TAKIP_DOSYASI, m21.SINAV_DOSYASI, m21.DENEME_DOSYASI = self._eski

    def _y(self, metin):
        return m22.plan_ve_formul_yanitla(metin)

    def test_program_kisisellesir(self):
        self.assertIn("Henüz bir programın yok", self._y("bugün ne çalışayım")[0])
        m21.ogrenci_araclari_yanitla("deneme: tyt türkçe 31 doğru 5 yanlış matematik 22 doğru 6 yanlış fizik 3 doğru 1 yanlış", {})
        program = self._y("tyt için günde 3 saat program yap")[0]
        self.assertIn("(YKS", program)
        self.assertIn("**Fizik** → ek oturum", program)
        self.assertIn("Deneme sınavı", program)
        self.assertEqual(program.count("| **"), 7)
        self.assertIn("programın:", self._y("bugün ne çalışayım")[0])

    def test_panelim(self):
        bos = self._y("panelim")[0]
        self.assertIn("Sıradaki adım", bos)
        self.assertNotIn("- \n", bos)
        m21.ogrenci_araclari_yanitla("YKS sınavım 20.06.2027", {})
        m21.ogrenci_araclari_yanitla("kart ekle: apple = elma", {})
        dolu = self._y("panelim")[0]
        self.assertIn("**YKS**", dolu)
        self.assertIn("kartları çalış", dolu)
        for soru in ("panel nasıl yapılır", "güneş paneli fiyatları", "durumum kötü"):
            self.assertIsNone(self._y(soru)[0], soru)

    def test_rozetler(self):
        m18.TAKIP_DOSYASI = os.path.join(self.klasor, "takip.json")
        self.assertIn("0/19", self._y("rozetlerim")[0])
        bugun = m18._simdi().date()
        with open(m18.TAKIP_DOSYASI, "w", encoding="utf-8") as f:
            json.dump([{"ders": "Matematik", "konu": "x", "soru_sayisi": 40, "sure_dk": 60,
                        "tarih": (bugun - __import__("datetime").timedelta(days=i)).isoformat()} for i in range(3)], f)
        cevap = self._y("rozetlerim")[0]
        self.assertIn("İlk Adım", cevap)
        self.assertIn("Yüzlük", cevap)
        self.assertIn("Isınma", cevap)
        self.assertIn("Rozetler", self._y("panelim")[0])
        for soru in ("rozet nasıl yapılır kumaştan", "madalya kazanan türk sporcular"):
            self.assertIsNone(self._y(soru)[0], soru)

    def test_formuller(self):
        self.assertIn("Zincir", self._y("türev formülleri")[0])
        self.assertIn("P·V = n·R·T", self._y("kimya formülleri")[0])
        self.assertIn("hangisini", self._y("formül kartları")[0])
        for soru in ("suyun formülü nedir", "python program yaz", "tv programı ne", "türev nedir"):
            self.assertIsNone(self._y(soru)[0], soru)


class ErisimSifresi(unittest.TestCase):
    def setUp(self):
        self._eski = os.environ.pop("AREX_ERISIM_SIFRESI", None)

    def tearDown(self):
        os.environ.pop("AREX_ERISIM_SIFRESI", None)
        if self._eski is not None:
            os.environ["AREX_ERISIM_SIFRESI"] = self._eski

    def test_varsayilan_sifre_yok(self):
        # Kodda gömülü varsayılan şifre olmamalı: tanımlı değilse kilit devre dışı, hiçbir şifre kabul edilmez
        self.assertEqual(m23.tanimli_sifre_ozeti(), "")
        self.assertFalse(m23.sifre_dogru_mu("1453", m23.tanimli_sifre_ozeti()))

    def test_dogrulama_ve_bekleme(self):
        os.environ["AREX_ERISIM_SIFRESI"] = "  test-sifre-xyz "
        hedef = m23.tanimli_sifre_ozeti()
        self.assertTrue(m23.sifre_dogru_mu("test-sifre-xyz", hedef))
        self.assertFalse(m23.sifre_dogru_mu("test-sifre-xy", hedef))
        self.assertFalse(m23.sifre_dogru_mu("", hedef))
        self.assertEqual([m23.bekleme_suresi(n) for n in (0, 4, 5, 6, 100)], [0, 0, 30, 60, 600])

    def test_yonetici_pin_erisim_sifresine_baglanir(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            import modul_11_guvenlik_kalkani as m11
        eski_admin = os.environ.pop("AR_ADMIN_PIN", None)
        try:
            os.environ["AREX_ERISIM_SIFRESI"] = "test-sifre-xyz"
            self.assertTrue(m11.pin_dogrula("test-sifre-xyz"))
            self.assertFalse(m11.pin_dogrula("1453"))  # koddaki varsayılan PIN bulutta geçersiz
        finally:
            if eski_admin is not None:
                os.environ["AR_ADMIN_PIN"] = eski_admin


class YanlisTetiklemeYok(unittest.TestCase):
    """Öğrenci araçları gündelik sorulara karışmamalı (bilgi soruları sohbet motoruna gitmeli)."""

    SOHBETE_GITMELI = [
        "doğru ile yanlış arasındaki fark nedir", "sınav kaygısı nasıl yenilir", "yks sınavı kaç dakika",
        "sınavım iyi geçmedi moralim bozuk", "net nedir", "internet hızımı nasıl artırırım",
        "pomodoro tekniği nedir", "pomodoro tekniği işe yarar mı", "kredi kartı borcu nasıl kapatılır",
        "ingilizce kelime nasıl ezberlenir", "bugün ne yemek yapayım", "program nasıl yazılır",
        "haftalık plan nasıl yapılır", "formül 1 yarışı ne zaman", "excel formülleri", "türev nedir",
        "güneş paneli kaç watt", "rozet ne demek", "deneme yazısı nasıl yazılır",
        "denemelerim hep kötü geçiyor ne yapayım", "bu hafta ne kadar sıcak olacak",
        "günde 3 saat ders çalışmak yeterli mi", "yanlışlarımı affet",
    ]
    ARACA_GITMELI = [
        "pomodoro başlat", "bana haftalık çalışma programı hazırla", "türev formülleri", "formül kartları",
        "denemelerim", "40 doğru 12 yanlış kaç net", "lgs 40 soruda 6 yanlış 2 boş kaç net",
        "bu hafta ne kadar çalıştım", "yanlış defterim", "rozetlerim", "panelim", "sınavlarıma kaç gün kaldı",
    ]

    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        self._eski = {(m, a): getattr(m, a) for m, a in [
            (m18, "TAKIP_DOSYASI"), (m18, "AYAR_DOSYASI"), (m18, "HATIRLATICI_DOSYASI"), (m18, "YANLIS_DOSYASI"),
            (m21, "SINAV_DOSYASI"), (m21, "KART_DOSYASI"), (m21, "DENEME_DOSYASI")]}
        for (m, a) in self._eski:
            setattr(m, a, os.path.join(self.klasor, a + ".json"))

    def tearDown(self):
        for (m, a), v in self._eski.items():
            setattr(m, a, v)

    def _arac(self, q):
        for f in (lambda: m18.calisma_kocu_yanitla(q, {}), lambda: m21.ogrenci_araclari_yanitla(q, {}),
                  lambda: m22.plan_ve_formul_yanitla(q)):
            y, e = f()
            if y:
                return e
        return None

    def test_gundelik_sorular_sohbete_gider(self):
        for q in self.SOHBETE_GITMELI:
            self.assertIsNone(self._arac(q), q)
        # bilgi sorusu hiçbir dosyaya yazmamalı (ör. pomodoro hatırlatıcısı kurulmamalı)
        self.assertEqual(os.listdir(self.klasor), [])

    def test_komutlar_araca_gider(self):
        for q in self.ARACA_GITMELI:
            self.assertIsNotNone(self._arac(q), q)

    def test_eksik_dogru_sayisi_ile_net(self):
        cevap = m21.ogrenci_araclari_yanitla("40 soruda 10 yanlış kaç net eder", {})[0]
        self.assertIn("**30 doğru**", cevap)
        self.assertIn("Net: 27,5", cevap)


class YedekHatirlatici(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.mkdtemp()
        self._eski = (m20._KOK, m20._AYAR_DOSYASI)
        m20._KOK = self.klasor
        m20._AYAR_DOSYASI = os.path.join(self.klasor, "arex_calisma_ayarlari.json")

    def tearDown(self):
        m20._KOK, m20._AYAR_DOSYASI = self._eski

    def test_yedek_gerekli_mi(self):
        self.assertEqual(m20.yedek_gerekli_mi(), (False, None))  # kayıt yok → uyarı yok
        with open(os.path.join(self.klasor, "arex_kartlar.json"), "w") as f:
            f.write("[]")
        self.assertEqual(m20.yedek_gerekli_mi(), (True, None))  # kayıt var, hiç yedek yok
        m20.son_yedek_kaydet()
        self.assertEqual(m20.yedek_gerekli_mi(), (False, 0))
        with open(m20._AYAR_DOSYASI, encoding="utf-8") as f:
            ayar = json.load(f)
        ayar["son_yedek"] = "2020-01-01T10:00"
        with open(m20._AYAR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(ayar, f)
        self.assertTrue(m20.yedek_gerekli_mi()[0])

    def test_panelde_bulutta_uyari(self):
        with open(os.path.join(self.klasor, "arex_kartlar.json"), "w") as f:
            f.write("[]")
        eski_bulut = m23.bulutta_mi
        eski = {(m, a): getattr(m, a) for m, a in [(m18, "TAKIP_DOSYASI"), (m18, "AYAR_DOSYASI"),
                (m18, "HATIRLATICI_DOSYASI"), (m18, "YANLIS_DOSYASI"), (m21, "SINAV_DOSYASI"),
                (m21, "KART_DOSYASI"), (m21, "DENEME_DOSYASI")]}
        try:
            for (m, a) in eski:
                setattr(m, a, os.path.join(self.klasor, "x_" + a))
            m23.bulutta_mi = lambda: True
            self.assertIn("Hiç yedek almadın", m22.plan_ve_formul_yanitla("panelim")[0])
            m23.bulutta_mi = lambda: False
            self.assertNotIn("yedek", m22.plan_ve_formul_yanitla("panelim")[0])
        finally:
            m23.bulutta_mi = eski_bulut
            for (m, a), v in eski.items():
                setattr(m, a, v)


class KaliciDepo(unittest.TestCase):
    """Supabase REST (PostgREST) arayüzünü taklit eden yerel sahte sunucuyla uçtan uca eşitleme testi."""

    @classmethod
    def setUpClass(cls):
        import http.server
        import threading
        cls.tablo = {}
        cls.istekler = []
        test = cls

        class Sahte(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _yaz(self, kod, govde=b""):
                self.send_response(kod)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(govde)

            def do_GET(self):
                test.istekler.append(("GET", self.path, self.headers.get("apikey")))
                if self.headers.get("apikey") != "test-anahtar":
                    return self._yaz(401)
                self._yaz(200, json.dumps(list(test.tablo.values())).encode())

            def do_POST(self):
                govde = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                test.istekler.append(("POST", self.path, [r["ad"] for r in govde]))
                for r in govde:
                    test.tablo[r["ad"]] = r
                self._yaz(201)

        cls.sunucu = http.server.HTTPServer(("127.0.0.1", 0), Sahte)
        threading.Thread(target=cls.sunucu.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.sunucu.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.sunucu.shutdown()

    def setUp(self):
        urllib.request.urlopen, socket.create_connection = _GERCEK_URLOPEN, _GERCEK_BAGLANTI  # yalnızca 127.0.0.1
        self.klasor = tempfile.mkdtemp()
        self._eski_kok = m24._KOK
        m24._KOK = self.klasor
        self.tablo.clear()
        self.istekler.clear()
        m24._DURUM.update({"geri_yuklendi": False, "imzalar": {}, "son_esitleme": None, "son_hata": None})
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"] = self.url, "test-anahtar"

    def tearDown(self):
        urllib.request.urlopen = socket.create_connection = _ag_kapali
        m24._KOK = self._eski_kok
        os.environ.pop("SUPABASE_URL", None)
        os.environ.pop("SUPABASE_KEY", None)

    def _dosya(self, ad, veri):
        with open(os.path.join(self.klasor, ad), "w", encoding="utf-8") as f:
            json.dump(veri, f)

    def _oku(self, ad):
        with open(os.path.join(self.klasor, ad), encoding="utf-8") as f:
            return json.load(f)

    def test_yapilandirma_yoksa_hicbir_sey_yapmaz(self):
        os.environ.pop("SUPABASE_URL")
        self.assertFalse(m24.etkin_mi())
        m24.esitle(arka_planda=False)
        self.assertEqual(self.istekler, [])

    def test_ilk_yukleme_ve_yalnizca_degisenler(self):
        self._dosya("arex_kartlar.json", [{"on": "apple", "arka": "elma"}])
        self._dosya("komutlar.json", {"selam": "merhaba"})
        m24.esitle(arka_planda=False)
        self.assertEqual(set(self.tablo), {"arex_kartlar.json", "komutlar.json"})
        self.istekler.clear()
        m24.esitle(arka_planda=False)  # değişiklik yok → gönderim yok
        self.assertFalse([i for i in self.istekler if i[0] == "POST"])
        time.sleep(0.01)
        self._dosya("arex_kartlar.json", [{"on": "book", "arka": "kitap"}])
        m24.esitle(arka_planda=False)
        self.assertEqual([i[2] for i in self.istekler if i[0] == "POST"], [["arex_kartlar.json"]])

    def test_yeniden_baslangicta_geri_yukleme_ve_guvenlik_kopyasi(self):
        self.tablo["komutlar.json"] = {"ad": "komutlar.json", "icerik": json.dumps({"ogrettigim": "cevap"}), "guncelleme": "x"}
        self.tablo["arex_denemeler.json"] = {"ad": "arex_denemeler.json", "icerik": "[1, 2]", "guncelleme": "x"}
        self.tablo["../main.py"] = {"ad": "../main.py", "icerik": "{}", "guncelleme": "x"}  # kötü niyetli ad
        self._dosya("komutlar.json", {"repo": "eski hali"})  # bulut yeniden başladı: GitHub'daki eski dosya
        m24.esitle(arka_planda=False)
        self.assertEqual(self._oku("komutlar.json"), {"ogrettigim": "cevap"})
        self.assertEqual(self._oku("arex_denemeler.json"), [1, 2])
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(self.klasor), "main.py")))
        kopyalar = os.listdir(os.path.join(self.klasor, "ar_acil_yedekler"))
        self.assertTrue(kopyalar and kopyalar[0].startswith("bulut_oncesi_"))
        # geri yüklenen içerik tekrar gönderilmemeli
        self.assertFalse([i for i in self.istekler if i[0] == "POST"])

    def test_ulasilamazsa_yerel_veri_ezilmez_ve_gonderilmez(self):
        os.environ["SUPABASE_KEY"] = "yanlis-anahtar"
        self._dosya("arex_kartlar.json", [1])
        m24.esitle(arka_planda=False)
        self.assertEqual(self._oku("arex_kartlar.json"), [1])
        self.assertFalse([i for i in self.istekler if i[0] == "POST"])
        self.assertIn("ulaşılamadı", m24.durum_metni())


class SohbetYonlendirme(unittest.TestCase):
    """Sohbet motorunun soruları doğru modüle yönlendirdiğini doğrular (ağ kapalı)."""

    @classmethod
    def setUpClass(cls):
        import streamlit as st
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            import modul_8_zeka_ve_hibrit_ai as m8
        cls.m8, cls.st = m8, st
        klasor = tempfile.mkdtemp()
        m8._m18.TAKIP_DOSYASI = os.path.join(klasor, "t.json")
        m8._m18.AYAR_DOSYASI = os.path.join(klasor, "a.json")
        m8._m18.HATIRLATICI_DOSYASI = os.path.join(klasor, "h.json")
        m8._m18.YANLIS_DOSYASI = os.path.join(klasor, "y.json")
        m8._m21.SINAV_DOSYASI = os.path.join(klasor, "s.json")
        m8._m21.KART_DOSYASI = os.path.join(klasor, "k.json")
        m8._m21.DENEME_DOSYASI = os.path.join(klasor, "d.json")
        m8._m22.m18.AYAR_DOSYASI = os.path.join(klasor, "a.json")
        m8._m22.m18.TAKIP_DOSYASI = os.path.join(klasor, "t.json")
        m8._m22.m18.YANLIS_DOSYASI = os.path.join(klasor, "y.json")
        m8._m22.m18.HATIRLATICI_DOSYASI = os.path.join(klasor, "h.json")
        m8._m22.m21.KART_DOSYASI = os.path.join(klasor, "k.json")
        m8._m22.m21.SINAV_DOSYASI = os.path.join(klasor, "s.json")
        m8._m22.m21.DENEME_DOSYASI = os.path.join(klasor, "d.json")
        m8._m21.m18.AYAR_DOSYASI = os.path.join(klasor, "a.json")
        m8._m21.m18.HATIRLATICI_DOSYASI = os.path.join(klasor, "h.json")
        st.session_state["messages"] = []

    def _etiket(self, metin):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.m8.akilli_yanit_uret(metin)[2]

    def test_konu_degisimi_takip_sorusu(self):
        m8, st = self.m8, self.st
        st.session_state["messages"] = [{"role": "user", "content": "osmanlı neden çöktü"},
                                        {"role": "assistant", "content": "..."}]
        self.assertEqual(m8._konu_degisimi_sorgusu("peki ya bizans", "Osmanlı İmparatorluğu"),
                         ("bizans neden çöktü", "bizans"))
        self.assertEqual(m8._konu_degisimi_sorgusu("ya almanya?", "osmanlı")[1], "almanya")
        # zamirli/soru kelimeli takipler konu değişimi DEĞİLDİR → bağlam korunur
        for q in ("peki bunun önemi ne", "peki neden", "ya sonra", "peki daha fazla", "bir de onu anlat",
                  "bir de selam söyle", "ya şaka yapıyorsun", "ya kardeşim", "peki anladım", "ya sen",
                  "ya bilmiyorum", "peki tamam"):
            self.assertIsNone(m8._konu_degisimi_sorgusu(q, "osmanlı"), q)
        st.session_state["messages"] = []

    def test_kota_bekleme_ve_durust_takip_mesaji(self):
        m9 = self.m8._m9
        import time as _t
        eski = dict(m9._KOTA_BEKLEME)
        try:
            m9._KOTA_BEKLEME.clear()
            self.assertFalse(m9.ai_kotasi_dolu_mu())
            for model in ("openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"):
                m9._KOTA_BEKLEME[f"groq_cloud:{model}"] = _t.time() + 60
            self.assertTrue(m9.ai_kotasi_dolu_mu())
            # Ağ kapalı + kota dolu → takip sorusu haber aramasına değil dürüst mesaja gitmeli
            self.st.session_state["messages"] = [{"role": "user", "content": "fotosentez nedir"},
                                                 {"role": "assistant", "content": "..."}]
            self.assertIn("Meşgul", self._etiket("peki bitkiler geceleri ne yapar"))
        finally:
            m9._KOTA_BEKLEME.clear()
            m9._KOTA_BEKLEME.update(eski)
            self.st.session_state["messages"] = []

    def test_yonlendirme(self):
        self.assertIn("Matematik", self._etiket("2+3*4"))
        self.assertIn("Matematik", self._etiket("sin 30"))
        self.assertIn("Grafik", self._etiket("y = x^2 - 4 grafiğini çiz"))
        self.assertIn("Birim", self._etiket("5 km kaç mil"))
        self.assertIn("Selamlaşma", self._etiket("merhaba"))
        self.assertIn("Yardım", self._etiket("help"))
        self.assertNotIn("Matematik", self._etiket("1-2 gün sonra gel"))
        self.assertNotIn("Hal", self._etiket("çalışmalar nasıl gidiyor"))
        self.assertIn("Çalışma", self._etiket("bugün 10 fizik sorusu çözdüm"))
        self.assertIn("Net", self._etiket("40 doğru 12 yanlış kaç net"))
        self.assertIn("Pomodoro", self._etiket("pomodoro başlat"))
        self.assertIn("Deneme", self._etiket("denemelerim"))
        self.assertIn("Kart", self._etiket("hazır desteler"))
        self.assertIn("Formül", self._etiket("türev formülleri"))
        self.assertIn("Yanlış", self._etiket("yanlış defterim"))
        self.assertIn("Panel", self._etiket("panelim"))
        self.assertIn("Rozet", self._etiket("rozetlerim"))
        self.assertIn("Program", self._etiket("bana haftalık çalışma programı hazırla"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
