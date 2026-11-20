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

    def test_formuller(self):
        self.assertIn("Zincir", self._y("türev formülleri")[0])
        self.assertIn("P·V = n·R·T", self._y("kimya formülleri")[0])
        self.assertIn("hangisini", self._y("formül kartları")[0])
        for soru in ("suyun formülü nedir", "python program yaz", "tv programı ne", "türev nedir"):
            self.assertIsNone(self._y(soru)[0], soru)


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
        self.assertIn("Program", self._etiket("bana haftalık çalışma programı hazırla"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
