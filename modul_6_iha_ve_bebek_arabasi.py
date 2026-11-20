# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.0 — MODÜL 6: TEKNOFEST OTONOM İHA & TÜBİTAK 2204-A AKILLI BEBEK
ARABASI MÜHENDİSLİK HESAPLAYICISI, 175 TERİM VE 260 KONTROL ADIMI (modul_6_iha_ve_bebek_arabasi.py)
==============================================================================
"""
import math
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
_m3 = _guvenli_modul_yukle("modul_3_veri_ve_kisiler")
bilgi_karti_olustur = _m1.bilgi_karti_olustur
AHMET_BILGI_TABANI = _m3.AHMET_BILGI_TABANI
proje_notlari_oku = _m3.proje_notlari_oku
proje_notu_ekle = _m3.proje_notu_ekle

TEKNIK_TERIMLER_SOZLUGU = {   'terim_001': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #1)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_001',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_002': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #2)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_002',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_003': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #3)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_003',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_004': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #4)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_004',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_005': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #5)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_005',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_006': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #6)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_006',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_007': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #7)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_007',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_008': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #8)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_008',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_009': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #9)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_009',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_010': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #10)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_010',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_011': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #11)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_011',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_012': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #12)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_012',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_013': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #13)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_013',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_014': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #14)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_014',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_015': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #15)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_015',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_016': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #16)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_016',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_017': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #17)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_017',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_018': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #18)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_018',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_019': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #19)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_019',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_020': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #20)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_020',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_021': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #21)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_021',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_022': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #22)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_022',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_023': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #23)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_023',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_024': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #24)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_024',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_025': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #25)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_025',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_026': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #26)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_026',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_027': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #27)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_027',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_028': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #28)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_028',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_029': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #29)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_029',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_030': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #30)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_030',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_031': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #31)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_031',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_032': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #32)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_032',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_033': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #33)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_033',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_034': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #34)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_034',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_035': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #35)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_035',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_036': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #36)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_036',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_037': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #37)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_037',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_038': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #38)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_038',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_039': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #39)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_039',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_040': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #40)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_040',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_041': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #41)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_041',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_042': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #42)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_042',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_043': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #43)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_043',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_044': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #44)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_044',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_045': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #45)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_045',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_046': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #46)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_046',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_047': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #47)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_047',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_048': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #48)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_048',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_049': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #49)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_049',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_050': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #50)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_050',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_051': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #51)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_051',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_052': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #52)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_052',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_053': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #53)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_053',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_054': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #54)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_054',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_055': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #55)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_055',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_056': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #56)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_056',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_057': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #57)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_057',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_058': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #58)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_058',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_059': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #59)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_059',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_060': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #60)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_060',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_061': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #61)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_061',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_062': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #62)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_062',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_063': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #63)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_063',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_064': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #64)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_064',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_065': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #65)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_065',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_066': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #66)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_066',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_067': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #67)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_067',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_068': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #68)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_068',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_069': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #69)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_069',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_070': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #70)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_070',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_071': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #71)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_071',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_072': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #72)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_072',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_073': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #73)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_073',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_074': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #74)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_074',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_075': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #75)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_075',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_076': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #76)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_076',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_077': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #77)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_077',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_078': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #78)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_078',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_079': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #79)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_079',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_080': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #80)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_080',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_081': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #81)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_081',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_082': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #82)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_082',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_083': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #83)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_083',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_084': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #84)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_084',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_085': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #85)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_085',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_086': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #86)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_086',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_087': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #87)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_087',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_088': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #88)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_088',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_089': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #89)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_089',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_090': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #90)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_090',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_091': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #91)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_091',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_092': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #92)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_092',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_093': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #93)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_093',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_094': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #94)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_094',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_095': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #95)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_095',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_096': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #96)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_096',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_097': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #97)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_097',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_098': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #98)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_098',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_099': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #99)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_099',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_100': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #100)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_100',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_101': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #101)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_101',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_102': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #102)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_102',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_103': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #103)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_103',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_104': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #104)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_104',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_105': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #105)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_105',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_106': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #106)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_106',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_107': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #107)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_107',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_108': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #108)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_108',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_109': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #109)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_109',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_110': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #110)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_110',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_111': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #111)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_111',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_112': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #112)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_112',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_113': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #113)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_113',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_114': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #114)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_114',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_115': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #115)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_115',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_116': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #116)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_116',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_117': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #117)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_117',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_118': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #118)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_118',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_119': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #119)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_119',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_120': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #120)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_120',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_121': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #121)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_121',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_122': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #122)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_122',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_123': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #123)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_123',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_124': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #124)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_124',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_125': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #125)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_125',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_126': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #126)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_126',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_127': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #127)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_127',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_128': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #128)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_128',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_129': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #129)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_129',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_130': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #130)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_130',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_131': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #131)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_131',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_132': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #132)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_132',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_133': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #133)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_133',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_134': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #134)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_134',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_135': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #135)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_135',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_136': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #136)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_136',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_137': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #137)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_137',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_138': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #138)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_138',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_139': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #139)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_139',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_140': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #140)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_140',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_141': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #141)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_141',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_142': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #142)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_142',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_143': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #143)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_143',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_144': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #144)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_144',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_145': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #145)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_145',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_146': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #146)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_146',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_147': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #147)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_147',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_148': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #148)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_148',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_149': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #149)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_149',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_150': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #150)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_150',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_151': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #151)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_151',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_152': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #152)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_152',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_153': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #153)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_153',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_154': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #154)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_154',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_155': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #155)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_155',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_156': {   'aciklama': "Python'da matematiksel ifadeleri güvenlik açığı oluşturmadan "
                                 '(`eval` kullanmadan) düğüm düğüm analiz edip hesaplayan yapıdır.',
                     'baslik': 'AST (Soyut Sözdizimi Ağacı) (Modül #156)',
                     'kategori': 'Bilgisayar Bilimi',
                     'kod': 'TERIM_156',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_157': {   'aciklama': 'Kullanıcının yazım hatalı girdiği metinleri Levenshtein mesafesi '
                                 'ile en yakın doğru komuta eşleştiren bulanık mantık tekniğidir.',
                     'baslik': 'Fuzzy String Matching (Modül #157)',
                     'kategori': 'Doğal Dil İşleme',
                     'kod': 'TERIM_157',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_158': {   'aciklama': 'Derin öğrenme modelleriyle insan ses tonlamasını, vurguyu ve '
                                 'nefes aralarını doğal biçimde üreten ses teknolojisidir.',
                     'baslik': 'Neural TTS (Sinirsel Ses Sentezi) (Modül #158)',
                     'kategori': 'Ses Teknolojisi',
                     'kod': 'TERIM_158',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_159': {   'aciklama': 'Akıllı bebek arabası gibi yüksek tork gerektiren sistemlerde '
                                 'motor gücünü kayıpsız olarak tekerleklere ileten mekanik '
                                 'sistemdir.',
                     'baslik': 'Zincir ve Dişli Aktarma (Modül #159)',
                     'kategori': 'Mekanik',
                     'kod': 'TERIM_159',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_160': {   'aciklama': "Uçuş halindeki İHA'nın irtifa, hız, batarya voltajı ve GPS "
                                 'koordinatlarını yer kontrol istasyonuna anlık aktaran kablosuz '
                                 'veri hattıdır.',
                     'baslik': 'Telemetri Sistemi (Modül #160)',
                     'kategori': 'TEKNOFEST İHA',
                     'kod': 'TERIM_160',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_161': {   'aciklama': 'Uçuş kontrol sistemlerinde (drone/İHA) hata payını Oransal (P), '
                                 'İntegral (I) ve Türevsel (D) katsayılarla sıfıra indiren geri '
                                 'besleme algoritmasıdır.',
                     'baslik': 'PID Kontrolcü (Modül #161)',
                     'kategori': 'Otonom Kontrol',
                     'kod': 'TERIM_161',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_162': {   'aciklama': "Arduino ve ESP32'de DC motor hızını veya servo/ESC devrini "
                                 'dijital darbelerin görev döngüsüyle (duty cycle) kontrol etme '
                                 'tekniğidir.',
                     'baslik': 'PWM (Sinyal Genişlik Modülasyonu) (Modül #162)',
                     'kategori': 'Elektronik',
                     'kod': 'TERIM_162',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_163': {   'aciklama': "İvmeölçer ve jiroskop verilerini birleştirerek İHA'nın roll, "
                                 'pitch ve yaw açılarını saniyede yüzlerce kez ölçen sensör '
                                 'modülüdür.',
                     'baslik': 'IMU (Ataletsel Ölçüm Birimi) (Modül #163)',
                     'kategori': 'Havacılık',
                     'kod': 'TERIM_163',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_164': {   'aciklama': 'Sensörlerden gelen gürültülü ölçümleri temizleyerek aracın '
                                 'gerçek konumunu ve açısını yüksek doğrulukla tahmin eden '
                                 'matematiksel algoritmadır.',
                     'baslik': 'Kalman Filtresi (Modül #164)',
                     'kategori': 'Sensör Füzyonu',
                     'kod': 'TERIM_164',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_165': {   'aciklama': 'Uçuş kontrol kartından gelen PWM/DShot sinyallerine göre '
                                 'fırçasız (brushless) drone motorlarının devrini ayarlayan güç '
                                 'sürücüsüdür.',
                     'baslik': 'ESC (Elektronik Hız Kontrolcüsü) (Modül #165)',
                     'kategori': 'İHA / Drone',
                     'kod': 'TERIM_165',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_166': {   'aciklama': '40 kHz ses dalgası gönderip yansıma süresini ölçerek 2 cm ile '
                                 '400 cm arasındaki engellerin mesafesini hesaplayan sensördür.',
                     'baslik': 'HC-SR04 Ultrasonik Sensör (Modül #166)',
                     'kategori': 'Robotik',
                     'kod': 'TERIM_166',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_167': {   'aciklama': 'İki adet DC motorun hem dönüş yönünü hem de PWM ile hızını '
                                 'kontrol etmeye yarayan motor sürücü entegresidir.',
                     'baslik': 'L298N Çift H-Köprüsü (Modül #167)',
                     'kategori': 'Akıllı Bebek Arabası',
                     'kod': 'TERIM_167',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_168': {   'aciklama': 'SDA (veri) ve SCL (saat) olmak üzere sadece iki kablo üzerinden '
                                 'birden fazla sensörü mikrodenetleyiciye bağlayan seri '
                                 'protokoldür.',
                     'baslik': 'I2C Haberleşme Protokolü (Modül #168)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_168',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_169': {   'aciklama': 'MISO, MOSI, SCK ve CS hatlarını kullanarak yüksek hızlı kamera, '
                                 'SD kart ve ekran modüllerini süren senkron seri protokoldür.',
                     'baslik': 'SPI Haberleşme Protokolü (Modül #169)',
                     'kategori': 'Gömülü Sistemler',
                     'kod': 'TERIM_169',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_170': {   'aciklama': 'TX ve RX pinleri üzerinden GPS modülü, telemetri radyosu veya '
                                 'bilgisayar ile mikrodenetleyici arasında veri aktaran '
                                 'protokoldür.',
                     'baslik': 'UART Seri İletişim (Modül #170)',
                     'kategori': 'İletişim',
                     'kod': 'TERIM_170',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_171': {   'aciklama': 'Yüksek akım deşarj kapasitesi (C değeri) sayesinde drone ve '
                                 'robotik projelerinde tercih edilen hafif şarjlı batarya '
                                 'teknolojisidir.',
                     'baslik': 'LiPo Batarya (Lityum Polimer) (Modül #171)',
                     'kategori': 'Güç Sistemleri',
                     'kod': 'TERIM_171',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_172': {   'aciklama': "PLA'nın kolay basılabilirliği ile ABS'nin mekanik ve sıcaklık "
                                 'dayanımını birleştiren, drone ve mekanik parçalar için ideal 3D '
                                 'yazıcı filamentidir.',
                     'baslik': 'PETG Filament (Modül #172)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_172',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_173': {   'aciklama': 'İçerisine karbon fiber lifler katılmış, bükülmeye karşı ultra '
                                 'rijit ve hafif 3D baskı şasi malzemesidir.',
                     'baslik': 'Carbon Fiber PLA (Modül #173)',
                     'kategori': '3D Baskı',
                     'kod': 'TERIM_173',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_174': {   'aciklama': 'Kamera görüntülerinden gerçek zamanlı yüz tanıma, nesne takibi '
                                 've şerit/hedef tespiti yapan görüntü işleme kütüphanesidir.',
                     'baslik': 'OpenCV (Açık Kaynak Bilgisayarlı Görü) (Modül #174)',
                     'kategori': 'Yapay Zeka',
                     'kod': 'TERIM_174',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'},
    'terim_175': {   'aciklama': 'Web ve mobil arayüzde sayfa her yenilendiğinde (rerun) sohbet '
                                 'geçmişini ve değişkenleri hafızada tutan durum yöneticisidir.',
                     'baslik': 'Streamlit Session State (Modül #175)',
                     'kategori': 'Python / Web',
                     'kod': 'TERIM_175',
                     'proje_kullanimi': 'AREX AI Studio, Otonom İHA ve Akıllı Bebek Arabası sistem '
                                        'mimarisinde aktif kullanılır.'}}

MUHENDISLIK_KONTROL_LISTESI = [   {   'adim_no': 1,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #1)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 2,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #2)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 3,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #3)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 4,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #4)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 5,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #5)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 6,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #6)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 7,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #7)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 8,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #8)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 9,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #9)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 10,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #10)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 11,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #11)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 12,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #12)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 13,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #13)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 14,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #14)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 15,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #15)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 16,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #16)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 17,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #17)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 18,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #18)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 19,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #19)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 20,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #20)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 21,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #21)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 22,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #22)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 23,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #23)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 24,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #24)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 25,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #25)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 26,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #26)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 27,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #27)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 28,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #28)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 29,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #29)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 30,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #30)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 31,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #31)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 32,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #32)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 33,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #33)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 34,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #34)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 35,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #35)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 36,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #36)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 37,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #37)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 38,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #38)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 39,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #39)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 40,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #40)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 41,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #41)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 42,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #42)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 43,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #43)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 44,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #44)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 45,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #45)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 46,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #46)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 47,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #47)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 48,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #48)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 49,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #49)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 50,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #50)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 51,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #51)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 52,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #52)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 53,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #53)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 54,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #54)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 55,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #55)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 56,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #56)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 57,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #57)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 58,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #58)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 59,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #59)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 60,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #60)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 61,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #61)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 62,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #62)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 63,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #63)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 64,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #64)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 65,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #65)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 66,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #66)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 67,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #67)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 68,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #68)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 69,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #69)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 70,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #70)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 71,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #71)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 72,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #72)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 73,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #73)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 74,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #74)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 75,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #75)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 76,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #76)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 77,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #77)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 78,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #78)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 79,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #79)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 80,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #80)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 81,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #81)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 82,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #82)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 83,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #83)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 84,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #84)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 85,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #85)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 86,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #86)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 87,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #87)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 88,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #88)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 89,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #89)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 90,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #90)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 91,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #91)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 92,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #92)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 93,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #93)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 94,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #94)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 95,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #95)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 96,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #96)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 97,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #97)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 98,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #98)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 99,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #99)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 100,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #100)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 101,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #101)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 102,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #102)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 103,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #103)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 104,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #104)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 105,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #105)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 106,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #106)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 107,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #107)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 108,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #108)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 109,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #109)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 110,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #110)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 111,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #111)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 112,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #112)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 113,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #113)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 114,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #114)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 115,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #115)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 116,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #116)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 117,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #117)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 118,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #118)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 119,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #119)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 120,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #120)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 121,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #121)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 122,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #122)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 123,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #123)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 124,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #124)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 125,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #125)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 126,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #126)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 127,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #127)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 128,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #128)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 129,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #129)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 130,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #130)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 131,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #131)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 132,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #132)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 133,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #133)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 134,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #134)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 135,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #135)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 136,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #136)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 137,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #137)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 138,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #138)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 139,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #139)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 140,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #140)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 141,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #141)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 142,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #142)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 143,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #143)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 144,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #144)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 145,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #145)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 146,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #146)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 147,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #147)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 148,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #148)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 149,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #149)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 150,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #150)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 151,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #151)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 152,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #152)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 153,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #153)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 154,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #154)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 155,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #155)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 156,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #156)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 157,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #157)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 158,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #158)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 159,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #159)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 160,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #160)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 161,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #161)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 162,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #162)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 163,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #163)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 164,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #164)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 165,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #165)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 166,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #166)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 167,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #167)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 168,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #168)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 169,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #169)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 170,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #170)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 171,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #171)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 172,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #172)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 173,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #173)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 174,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #174)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 175,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #175)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 176,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #176)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 177,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #177)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 178,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #178)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 179,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #179)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 180,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #180)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 181,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #181)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 182,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #182)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 183,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #183)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 184,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #184)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 185,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #185)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 186,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #186)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 187,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #187)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 188,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #188)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 189,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #189)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 190,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #190)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 191,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #191)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 192,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #192)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 193,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #193)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 194,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #194)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 195,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #195)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 196,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #196)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 197,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #197)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 198,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #198)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 199,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #199)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 200,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #200)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 201,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #201)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 202,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #202)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 203,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #203)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 204,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #204)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 205,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #205)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 206,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #206)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 207,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #207)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 208,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #208)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 209,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #209)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 210,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #210)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 211,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #211)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 212,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #212)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 213,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #213)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 214,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #214)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 215,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #215)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 216,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #216)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 217,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #217)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 218,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #218)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 219,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #219)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 220,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #220)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 221,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #221)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 222,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #222)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 223,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #223)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 224,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #224)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 225,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #225)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 226,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #226)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 227,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #227)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 228,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #228)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 229,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #229)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 230,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #230)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 231,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #231)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 232,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #232)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 233,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #233)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 234,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #234)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 235,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #235)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 236,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #236)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 237,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #237)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 238,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #238)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 239,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #239)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 240,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #240)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 241,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #241)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 242,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #242)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 243,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #243)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 244,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #244)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 245,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #245)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 246,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #246)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 247,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #247)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 248,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #248)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 249,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #249)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 250,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #250)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 251,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #251)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 252,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #252)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'},
    {   'adim_no': 253,
        'gorev': 'L298N ve DC dişli motorların zincir aktarma tork ölçümleri',
        'modul': 'Motor Sürücü (Kontrol #253)',
        'oncelik': 'Yüksek',
        'proje': 'Akıllı Bebek Arabası'},
    {   'adim_no': 254,
        'gorev': '500.000+ kalıp indeksinin masaüstü ve mobil tarayıcıda hız testi',
        'modul': 'AREX AI Studio (Kontrol #254)',
        'oncelik': 'Normal',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 255,
        'gorev': 'Edge-TTS AhmetNeural ve EmelNeural seslerinin gecikmesiz oynatılması',
        'modul': 'Doğal Ses Sentezi (Kontrol #255)',
        'oncelik': 'Yüksek',
        'proje': 'Yazılım & AI'},
    {   'adim_no': 256,
        'gorev': 'İngilizce, Çince ve Bengalce mühendislik terimlerinin günlük tekrarı',
        'modul': 'Çok Dilli Pratik (Kontrol #256)',
        'oncelik': 'Normal',
        'proje': 'Kişisel Gelişim'},
    {   'adim_no': 257,
        'gorev': 'Carbon Fiber PLA şasi parçalarının 3D yazıcıda %35 dolulukla basılması',
        'modul': 'Otonom İHA Gövde (Kontrol #257)',
        'oncelik': 'Yüksek',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 258,
        'gorev': 'PID katsayılarının (Roll, Pitch, Yaw) test standında kalibre edilmesi',
        'modul': 'Uçuş Kontrol & IMU (Kontrol #258)',
        'oncelik': 'Normal',
        'proje': 'TEKNOFEST 2027'},
    {   'adim_no': 259,
        'gorev': 'Raspberry Pi 5 üzerinde OpenCV ile gerçek zamanlı hedef/yüz takibi testi',
        'modul': 'Görüntü İşleme (Kontrol #259)',
        'oncelik': 'Yüksek',
        'proje': 'Otonom AI Drone'},
    {   'adim_no': 260,
        'gorev': 'HC-SR04 ultrasonik sensör ile 40 cm altında otomatik frenleme testi',
        'modul': 'Akıllı Bebek Arabası (Kontrol #260)',
        'oncelik': 'Normal',
        'proje': 'TÜBİTAK 2204-A'}]


def iha_ve_bebek_arabasi_studyosu_goster():
    st.subheader("🚀 Geliştirici Ahmet Profili, TEKNOFEST İHA & Akıllı Bebek Arabası Mühendislik Laboratuvarı")
    p_tab_hesap, p_tab1, p_tab2, p_tab3 = st.tabs([
        "🧮 İHA & Bebek Arabası Mühendislik Hesaplayıcısı",
        "👤 Kişisel Profil & Proje Notları",
        "🛠️ Mühendislik Sözlüğü",
        "✅ Proje Kontrol Listesi",
    ])

    with p_tab_hesap:
        col_bebek, col_iha = st.columns(2, gap="large")

        with col_bebek:
            st.markdown("### 👶 Akıllı Bebek Arabası Hesaplayıcısı (TÜBİTAK 2204-A)")
            toplam_kutle_kg = st.number_input("Toplam Kütle (Bebek + Şasi + Akü, kg):", min_value=5.0, max_value=120.0, value=28.0, step=1.0)
            teker_cap_cm = st.number_input("Tekerlek Çapı (cm):", min_value=8.0, max_value=50.0, value=20.0, step=1.0)
            egim_derece = st.number_input("Maksimum Yokuş Eğimi (Derece °):", min_value=0.0, max_value=30.0, value=8.0, step=1.0)
            hedef_hiz_kms = st.number_input("Hedef Yürüyüş Hızı (km/saat):", min_value=1.0, max_value=10.0, value=4.5, step=0.5)
            aku_volt = st.selectbox("Akü / Batarya Voltajı (V):", [12.0, 24.0], index=0)
            aku_ah = st.number_input("Akü Kapasitesi (Ah):", min_value=1.0, max_value=50.0, value=7.0, step=0.5)
            engel_fren_cm = st.slider("HC-SR04 Otomatik Fren Mesafesi (cm):", 15, 100, 40)

            yaricap_m = (teker_cap_cm / 100.0) / 2.0
            egim_rad = math.radians(egim_derece)
            g_ivme = 9.81
            yuvarlanma_katsayisi = 0.025
            f_egim = toplam_kutle_kg * g_ivme * math.sin(egim_rad)
            f_yuvarlanma = toplam_kutle_kg * g_ivme * math.cos(egim_rad) * yuvarlanma_katsayisi
            f_toplam_n = f_egim + f_yuvarlanma
            toplam_tork_nm = f_toplam_n * yaricap_m
            motor_basi_tork_nm = toplam_tork_nm / 2.0
            motor_basi_kgcm = motor_basi_tork_nm * 10.197
            hiz_ms = hedef_hiz_kms / 3.6
            gerekli_guc_watt = (f_toplam_n * hiz_ms) / 0.75
            teker_rpm = (hiz_ms / (2 * math.pi * yaricap_m)) * 60.0
            ort_akim_a = max(1.2, gerekli_guc_watt / aku_volt)
            calisma_saat = (aku_ah * 0.8) / ort_akim_a
            menzil_km = calisma_saat * hedef_hiz_kms
            onerilen_pwm = min(255, max(90, int((hedef_hiz_kms / 6.0) * 255)))

            st.markdown(
                bilgi_karti_olustur(
                    "⚙️ Akıllı Bebek Arabası Motor, Tork & Sensör Sonuçları",
                    f"Toplam Kütle: {toplam_kutle_kg:.0f} kg | Eğim: {egim_derece:.0f}° | Fren Eşiği: {engel_fren_cm} cm",
                    (
                        f"• <strong>Toplam İtki Kuvveti:</strong> <code>{f_toplam_n:.1f} N</code><br>"
                        f"• <strong>Gerekli Toplam Tork:</strong> <code>{toplam_tork_nm:.2f} N·m</code> (Motor Başına: <code>{motor_basi_tork_nm:.2f} N·m</code> / <code>{motor_basi_kgcm:.1f} kg·cm</code>)<br>"
                        f"• <strong>Gerekli Motor Gücü:</strong> <code>{gerekli_guc_watt:.1f} Watt</code> &nbsp;|&nbsp; <strong>Tekerlek Devri:</strong> <code>{teker_rpm:.0f} RPM</code><br>"
                        f"• <strong>Tahmini Akü Süresi:</strong> <code>{calisma_saat:.1f} Saat</code> (Yaklaşık Menzil: <code>{menzil_km:.1f} km</code>)<br>"
                        f"• <strong>L298N Önerilen PWM Hızı:</strong> <code>{onerilen_pwm} / 255</code> &nbsp;|&nbsp; <strong>HC-SR04 Yankı Süresi:</strong> <code>{int(engel_fren_cm * 58.3)} µs</code>"
                    ),
                ),
                unsafe_allow_html=True,
            )

        with col_iha:
            st.markdown("### 🚁 TEKNOFEST Otonom İHA / Drone Hesaplayıcısı")
            iha_agirlik_g = st.number_input("Drone Toplam Uçuş Ağırlığı (gram):", min_value=200, max_value=25000, value=1450, step=50)
            motor_sayisi = st.selectbox("Motor Sayısı (Quadcopter / Hexacopter):", [4, 6, 8], index=0)
            motor_itki_g = st.number_input("Motor Başına Maksimum İtki (gram):", min_value=200, max_value=10000, value=950, step=50)
            lipo_mah = st.number_input("LiPo Batarya Kapasitesi (mAh):", min_value=500, max_value=30000, value=4200, step=100)
            lipo_hucre = st.selectbox("LiPo Hücre Sayısı (S):", ["3S (11.1V)", "4S (14.8V)", "6S (22.2V)"], index=1)
            hover_akim_a = st.number_input("Ortalama Uçuş (Hover) Akımı (Amper):", min_value=2.0, max_value=120.0, value=18.5, step=0.5)

            toplam_itki_g = motor_sayisi * motor_itki_g
            itki_agirlik_orani = toplam_itki_g / iha_agirlik_g
            faydali_yuk_g = max(0.0, (toplam_itki_g / 2.0) - iha_agirlik_g)
            ucus_suresi_dk = ((lipo_mah / 1000.0) * 0.80 / hover_akim_a) * 60.0
            if itki_agirlik_orani >= 2.2:
                ucus_durumu = "✅ Mükemmel (Otonom Görev & Rüzgâr Direnci İçin İdeal)"
            elif itki_agirlik_orani >= 1.7:
                ucus_durumu = "⚠️ Dengeli (Sakin Uçuş İçin Yeterli, Yük Eklenmemeli)"
            else:
                ucus_durumu = "❌ Yetersiz İtki! (Daha güçlü fırçasız motor/pervane seçilmeli)"

            st.markdown(
                bilgi_karti_olustur(
                    "🚁 Otonom İHA İtki, Yük & Uçuş Süresi Analizi",
                    f"{motor_sayisi} Motorlu Şasi | Batarya: {lipo_mah} mAh {lipo_hucre}",
                    (
                        f"• <strong>Toplam Maksimum İtki:</strong> <code>{toplam_itki_g:,} gram</code><br>"
                        f"• <strong>İtki / Ağırlık Oranı:</strong> <code>{itki_agirlik_orani:.2f} : 1</code><br>"
                        f"• <strong>Eklenebilir Güvenli Faydalı Yük:</strong> <code>{faydali_yuk_g:.0f} gram</code><br>"
                        f"• <strong>Tahmini Güvenli Uçuş Süresi (%80 Deşarj):</strong> <code>{ucus_suresi_dk:.1f} Dakika</code><br>"
                        f"• <strong>Mühendislik Değerlendirmesi:</strong> {ucus_durumu}"
                    ),
                ),
                unsafe_allow_html=True,
            )

    with p_tab1:
        col_p1, col_p2 = st.columns([1.4, 1.0], gap="large")
        with col_p1:
            for _, p_veri in AHMET_BILGI_TABANI.items():
                st.markdown(bilgi_karti_olustur("⚡ Ahmet Bilgi Kartı", "Aktif Geliştirici Profili", p_veri["yanit"].replace("\n", "<br>")), unsafe_allow_html=True)
        with col_p2:
            st.markdown("#### 📝 Hızlı Proje Notu Ekle")
            with st.form("proje_not_formu", clear_on_submit=True):
                n_baslik = st.text_input("Proje / Konu Başlığı:", placeholder="Örn: Otonom İHA Kamera Testi")
                n_icerik = st.text_area("Not İçeriği:", height=100)
                if st.form_submit_button("💾 Notu Kaydet", use_container_width=True) and n_baslik and n_icerik:
                    proje_notu_ekle(n_baslik, n_icerik)
                    st.success("Proje notu kaydedildi!")
                    st.rerun()
            for n_item in proje_notlari_oku()[:6]:
                st.markdown(bilgi_karti_olustur(f"📌 {n_item['baslik']}", f"🕒 {n_item['tarih']}", n_item["icerik"]), unsafe_allow_html=True)

    with p_tab2:
        terim_ara = st.text_input("Teknik Terim Ara (PID, PWM, IMU, Kalman, PETG...):").lower().strip()
        for _, t_obj in TEKNIK_TERIMLER_SOZLUGU.items():
            if terim_ara and terim_ara not in f"{t_obj['baslik']} {t_obj['aciklama']}".lower():
                continue
            st.markdown(bilgi_karti_olustur(t_obj["baslik"], f"Kategori: {t_obj['kategori']} | Kod: {t_obj['kod']}", t_obj["aciklama"]), unsafe_allow_html=True)

    with p_tab3:
        for g_item in MUHENDISLIK_KONTROL_LISTESI:
            st.markdown(bilgi_karti_olustur(f"Adım #{g_item['adim_no']} — {g_item['modul']}", f"Proje: {g_item['proje']} | Öncelik: {g_item['oncelik']}", g_item["gorev"]), unsafe_allow_html=True)
