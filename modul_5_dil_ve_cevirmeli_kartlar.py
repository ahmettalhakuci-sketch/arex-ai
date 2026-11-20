# -*- coding: utf-8 -*-
"""
==============================================================================
AR AI STUDIO v4.0 — MODÜL 5: 60 ADET A1-A2 3D ÇEVİRMELİ DİL KARTI (İNGİLİZCE • ARAPÇA • BENGALCE),
28 DİLLİ ÇEVİRİ, NEURAL SES VE MİKROFON STT MOTORU (modul_5_dil_ve_cevirmeli_kartlar.py)
==============================================================================
"""
import asyncio
import inspect
import io
import json
import random
import re
import time
import urllib.parse
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

_m1 = _guvenli_modul_yukle("modul_1_arayuz_ve_tema")
bilgi_karti_olustur = _m1.bilgi_karti_olustur
cevirmeli_dil_karti_olustur = _m1.cevirmeli_dil_karti_olustur

try:
    from googletrans import Translator as _GoogleTranslator
    _translator_nesnesi = _GoogleTranslator()
except Exception:
    _translator_nesnesi = None

try:
    from gtts import gTTS
    GTTS_MEVCUT = True
except Exception:
    gTTS = None
    GTTS_MEVCUT = False

try:
    import edge_tts
    EDGE_TTS_MEVCUT = True
except Exception:
    EDGE_TTS_MEVCUT = False

try:
    import pygame
    PYGAME_MEVCUT = True
except Exception:
    PYGAME_MEVCUT = False

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_MEVCUT = True
except Exception:
    sr = None
    SPEECH_RECOGNITION_MEVCUT = False

DESTEKLENEN_DILLER = {   'tr': '🇹🇷 Türkçe (Ana Dilimiz)',
    'en': '🇬🇧 İngilizce (English)',
    'ar': '🇸🇦 Arapça (العربية)',
    'bn': '🇧🇩 Bengalce (বাংলা)',
    'az': '🇦🇿 Azerbaycanca (Azərbaycanca)',
    'de': '🇩🇪 Almanca (Deutsch)',
    'fr': '🇫🇷 Fransızca (Français)',
    'es': '🇪🇸 İspanyolca (Español)',
    'it': '🇮🇹 İtalyanca (Italiano)',
    'ru': '🇷🇺 Rusça (Русский)',
    'ja': '🇯🇵 Japonca (日本語)',
    'ko': '🇰🇷 Korece (한국어)',
    'zh-cn': '🇨🇳 Çince (中文 - Basitleştirilmiş)',
    'fa': '🇮🇷 Farsça (فارسی)',
    'ur': '🇵🇰 Urduca (اردو)',
    'nl': '🇳🇱 Hollandaca (Nederlands)',
    'pt': '🇵🇹 Portekizce (Português)',
    'pl': '🇵🇱 Lehçe (Polski)',
    'sv': '🇸🇪 İsveççe (Svenska)',
    'el': '🇬🇷 Yunanca (Ελληνικά)',
    'cs': '🇨🇿 Çekçe (Čeština)',
    'ro': '🇷🇴 Rumence (Română)',
    'uk': '🇺🇦 Ukraynaca (Українська)',
    'hi': '🇮🇳 Hintçe (हिन्दी)',
    'id': '🇮🇩 Endonezce (Bahasa Indonesia)',
    'ms': '🇲🇾 Malayca (Bahasa Melayu)',
    'th': '🇹🇭 Tayca (ภาษาไทย)',
    'vi': '🇻🇳 Vietnamca (Tiếng Việt)'}
EDGE_SESLER = {   'ar': 'ar-SA-HamedNeural',
    'az': 'az-AZ-BabekNeural',
    'bn': 'bn-BD-PradeepNeural',
    'cs': 'cs-CZ-AntoninNeural',
    'de': 'de-DE-ConradNeural',
    'el': 'el-GR-NestorasNeural',
    'en': 'en-US-AndrewNeural',
    'es': 'es-ES-AlvaroNeural',
    'fa': 'fa-IR-FaridNeural',
    'fr': 'fr-FR-HenriNeural',
    'hi': 'hi-IN-MadhurNeural',
    'id': 'id-ID-ArdiNeural',
    'it': 'it-IT-DiegoNeural',
    'ja': 'ja-JP-KeitaNeural',
    'ko': 'ko-KR-InJoonNeural',
    'ms': 'ms-MY-OsmanNeural',
    'nl': 'nl-NL-MaartenNeural',
    'pl': 'pl-PL-MarekNeural',
    'pt': 'pt-BR-AntonioNeural',
    'ro': 'ro-RO-EmilNeural',
    'ru': 'ru-RU-DmitryNeural',
    'sv': 'sv-SE-MattiasNeural',
    'th': 'th-TH-NiwatNeural',
    'tr': 'tr-TR-AhmetNeural',
    'uk': 'uk-UA-OstapNeural',
    'ur': 'ur-PK-AsadNeural',
    'vi': 'vi-VN-NamMinhNeural',
    'zh-cn': 'zh-CN-YunxiNeural'}
EDGE_KADIN_SESLER = {   'ar': 'ar-SA-ZariyahNeural',
    'az': 'az-AZ-BanuNeural',
    'bn': 'bn-BD-NabanitaNeural',
    'cs': 'cs-CZ-VlastaNeural',
    'de': 'de-DE-KatjaNeural',
    'el': 'el-GR-AthinaNeural',
    'en': 'en-US-AriaNeural',
    'es': 'es-ES-ElviraNeural',
    'fa': 'fa-IR-DilaraNeural',
    'fr': 'fr-FR-DeniseNeural',
    'hi': 'hi-IN-SwaraNeural',
    'id': 'id-ID-GadisNeural',
    'it': 'it-IT-ElsaNeural',
    'ja': 'ja-JP-NanamiNeural',
    'ko': 'ko-KR-SunHiNeural',
    'ms': 'ms-MY-YasminNeural',
    'nl': 'nl-NL-ColetteNeural',
    'pl': 'pl-PL-ZofiaNeural',
    'pt': 'pt-BR-FranciscaNeural',
    'ro': 'ro-RO-AlinaNeural',
    'ru': 'ru-RU-SvetlanaNeural',
    'sv': 'sv-SE-SofieNeural',
    'th': 'th-TH-PremwadeeNeural',
    'tr': 'tr-TR-EmelNeural',
    'uk': 'uk-UA-PolinaNeural',
    'ur': 'ur-PK-UzmaNeural',
    'vi': 'vi-VN-HoaiMyNeural',
    'zh-cn': 'zh-CN-XiaoxiaoNeural'}
GTTS_DIL_ESLESME = {   'ar': 'ar',
    'az': 'az',
    'bn': 'bn',
    'cs': 'cs',
    'de': 'de',
    'el': 'el',
    'en': 'en',
    'es': 'es',
    'fa': 'fa',
    'fr': 'fr',
    'hi': 'hi',
    'id': 'id',
    'it': 'it',
    'ja': 'ja',
    'ko': 'ko',
    'ms': 'ms',
    'nl': 'nl',
    'pl': 'pl',
    'pt': 'pt',
    'ro': 'ro',
    'ru': 'ru',
    'sv': 'sv',
    'th': 'th',
    'tr': 'tr',
    'uk': 'uk',
    'ur': 'ur',
    'vi': 'vi',
    'zh-cn': 'zh-CN'}
TURKCE_AYLAR = [   '',
    'Ocak',
    'Şubat',
    'Mart',
    'Nisan',
    'Mayıs',
    'Haziran',
    'Temmuz',
    'Ağustos',
    'Eylül',
    'Ekim',
    'Kasım',
    'Aralık']
TURKCE_GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
A1_A2_DIL_PRATIK_KARTLARI = [   {   'ara_okunus': 'Merhaben, keyfe hâluke?',
        'arapca': 'مَرْحَبًا، كَيْفَ حَالُكَ؟',
        'ben_okunus': 'Hyalo, apni kemon achen?',
        'bengalce': 'হ্যালো, আপনি কেমন আছেন?',
        'id': 1,
        'ing_okunus': 'Helo, hav ar yu?',
        'ingilizce': 'Hello, how are you?',
        'kategori': 'Selamlaşma & Tanışma',
        'ornek_ar': 'مَرْحَبًا يَا صَدِيقِي، كَيْفَ حَالُكَ الْيَوْمَ؟ (Merhaben yâ sadîkî, keyfe '
                    'hâluke el-yevm?)',
        'ornek_bn': 'হ্যালো ভাই, আপনি আজ কেমন আছেন? (Hyalo bhai, apni aj kemon achen?)',
        'ornek_en': 'Hello, how are you today?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Merhaba, nasılsın?'},
    {   'ara_okunus': 'Ene bi-hayrin, şükran leke.',
        'arapca': 'أَنَا بِخَيْرٍ، شُكْرًا لَكَ.',
        'ben_okunus': 'Ami bhalo achi, dhonnobad.',
        'bengalce': 'আমি ভালো আছি, ধন্যবাদ।',
        'id': 2,
        'ing_okunus': 'Ay em fayn, tenk yu.',
        'ingilizce': 'I am fine, thank you.',
        'kategori': 'Selamlaşma & Tanışma',
        'ornek_ar': 'أَنَا بِخَيْرٍ وَالْحَمْدُ لِلَّهِ، شُكْرًا لَكَ. (Ene bi-hayrin '
                    'velhamdülillah, şükran leke.)',
        'ornek_bn': 'আমি খুব ভালো আছি, আপনাকে ধন্যবাদ। (Ami khub bhalo achi, apnake dhonnobad.)',
        'ornek_en': 'I am fine, thank you very much.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'İyiyim, teşekkür ederim.'},
    {   'ara_okunus': 'İsmî Ahmed.',
        'arapca': 'اِسْمِي أَحْمَدُ.',
        'ben_okunus': 'Amar nam Ahmed.',
        'bengalce': 'আমার নাম আহমেদ।',
        'id': 3,
        'ing_okunus': 'May neym iz Ahmet.',
        'ingilizce': 'My name is Ahmet.',
        'kategori': 'Tanışma & Kimlik',
        'ornek_ar': 'اِسْمِي أَحْمَدُ وَأَنَا طَالِبٌ. (İsmî Ahmed ve ene tâlibun.)',
        'ornek_bn': 'আমার নাম আহমেদ এবং আমি একজন ছাত্র। (Amar nam Ahmed ebong ami ekjon chatro.)',
        'ornek_en': 'My name is Ahmet and I am a student.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Benim adım Ahmet.'},
    {   'ara_okunus': "Teşerraftü bi-ma'rifetike.",
        'arapca': 'تَشَرَّفْتُ بِمَعْرِفَتِكَ.',
        'ben_okunus': 'Apnar sathe dekha kore bhalo laglo.',
        'bengalce': 'আপনার সাথে দেখা করে ভালো লাগলো।',
        'id': 4,
        'ing_okunus': 'Nays tu mit yu.',
        'ingilizce': 'Nice to meet you.',
        'kategori': 'Tanışma & Kimlik',
        'ornek_ar': 'أَهْلًا بِكَ فِي إِسْطَنْبُولَ، تَشَرَّفْتُ بِمَعْرِفَتِكَ! (Ehlen bike fî '
                    "İstanbul, teşerraftü bi-ma'rifetike!)",
        'ornek_bn': 'ইস্তাম্বুলে স্বাগতম, আপনার সাথে দেখা করে ভালো লাগলো! (Istambule sbagotom, '
                    'apnar sathe dekha kore bhalo laglo!)',
        'ornek_en': 'Welcome to Istanbul, nice to meet you!',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Tanıştığımıza memnun oldum.'},
    {   'ara_okunus': "Sabâhu'l-hayr",
        'arapca': 'صَبَاحُ الْخَيْرِ',
        'ben_okunus': 'Shubho shokal',
        'bengalce': 'শুভ সকাল',
        'id': 5,
        'ing_okunus': 'Gud morning',
        'ingilizce': 'Good morning',
        'kategori': 'Günlük İfadeler',
        'ornek_ar': "صَبَاحُ الْخَيْرِ، أَتَمَنَّى لَكَ يَوْمًا جَمِيلًا! (Sabâhu'l-hayr, etemennâ "
                    'leke yevmen cemîlen!)',
        'ornek_bn': 'শুভ সকাল, আপনার দিনটি ভালো কাটুক! (Shubho shokal, apnar dinti bhalo katuk!)',
        'ornek_en': 'Good morning, have a great day!',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Günaydın / İyi sabahlar'},
    {   'ara_okunus': "Mesâu'l-hayr / Tusbihu alâ hayr",
        'arapca': 'مَسَاءُ الْخَيْرِ / تُصْبِحُ عَلَى خَيْرٍ',
        'ben_okunus': 'Shubho shondhya / Shubho ratri',
        'bengalce': 'শুভ সন্ধ্যা / শুভ রাত্রি',
        'id': 6,
        'ing_okunus': 'Gud ivning / Gud nayt',
        'ingilizce': 'Good evening / Good night',
        'kategori': 'Günlük İfadeler',
        'ornek_ar': 'تُصْبِحُ عَلَى خَيْرٍ، أَرَاكَ غَدًا. (Tusbihu alâ hayr, erâke gaden.)',
        'ornek_bn': 'শুভ রাত্রি, আগামীকাল দেখা হবে। (Shubho ratri, agamikal dekha hobe.)',
        'ornek_en': 'Good night, see you tomorrow.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'İyi akşamlar / İyi geceler'},
    {   'ara_okunus': 'Ebî ve ümmî',
        'arapca': 'أَبِي وَأُمِّي',
        'ben_okunus': 'Amar baba ebong amar ma',
        'bengalce': 'আমার বাবা এবং আমার মা',
        'id': 7,
        'ing_okunus': 'May fadır end may madır',
        'ingilizce': 'My father and my mother',
        'kategori': 'Aile & Kişiler',
        'ornek_ar': 'أَنَا أُحِبُّ أَبِي وَأُمِّي كَثِيرًا. (Ene uhibbu ebî ve ümmî kesîran.)',
        'ornek_bn': 'আমি আমার বাবা এবং মাকে খুব ভালোবাসি। (Ami amar baba ebong make khub '
                    'bhalobashi.)',
        'ornek_en': 'I love my father and my mother very much.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Babam ve annem'},
    {   'ara_okunus': "Ene tâlibun fi'l-medreseti's-sâneviyyeti.",
        'arapca': 'أَنَا طَالِبٌ فِي الْمَدْرَسَةِ الثَّانَوِيَّةِ.',
        'ben_okunus': 'Ami hai skuler chatro.',
        'bengalce': 'আমি হাই স্কুলের ছাত্র।',
        'id': 8,
        'ing_okunus': 'Ay em e hay skul studınt.',
        'ingilizce': 'I am a high school student.',
        'kategori': 'Okul & Eğitim',
        'ornek_ar': 'أَنَا طَالِبٌ فِي الْمَدْرَسَةِ الثَّانَوِيَّةِ فِي إِسْطَنْبُولَ. (Ene '
                    "tâlibun fi'l-medreseti's-sâneviyyeti fî İstanbul.)",
        'ornek_bn': 'আমি ইস্তাম্বুলের একটি হাই স্কুলের ছাত্র। (Ami Istambuler ekti hai skuler '
                    'chatro.)',
        'ornek_en': 'I am a high school student in Istanbul.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Ben lise öğrencisiyim.'},
    {   'ara_okunus': 'Kitâbun, defterun ve kalemun',
        'arapca': 'كِتَابٌ، دَفْتَرٌ وَقَلَمٌ',
        'ben_okunus': 'Boi, khata ebong kolom',
        'bengalce': 'বই, খাতা এবং কলম',
        'id': 9,
        'ing_okunus': 'Buk, notbuk end pen',
        'ingilizce': 'Book, notebook and pen',
        'kategori': 'Okul & Eğitim',
        'ornek_ar': 'كِتَابِي وَدَفْتَرِي وَقَلَمِي عَلَى الطَّاوِلَةِ. (Kitâbî ve defterî ve '
                    "kalemî ale't-tâvileti.)",
        'ornek_bn': 'আমার বই, খাতা এবং কলম টেবিলের ওপর আছে। (Amar boi, khata ebong kolom tebiler '
                    'opor ache.)',
        'ornek_en': 'My book, notebook and pen are on the table.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Kitap, defter ve kalem'},
    {   'ara_okunus': 'Mâ hâzâ? / Men hâzâ?',
        'arapca': 'مَا هَذَا؟ / مَنْ هَذَا؟',
        'ben_okunus': 'Eta ki? / Uni ke?',
        'bengalce': 'এটা কী? / উনি কে?',
        'id': 10,
        'ing_okunus': 'Vat iz dis? / Hu iz dis?',
        'ingilizce': 'What is this? / Who is this?',
        'kategori': 'Temel Sorular',
        'ornek_ar': "مَا هَذَا الْجِهَازُ؟ هَذَا مُسْتَشْعِرٌ. (Mâ hâze'l-cihâz? Hâzâ "
                    "müsteş'irun.)",
        'ornek_bn': 'এই যন্ত্রটি কী? এটি একটি সেন্সর। (Ei jontroti ki? Eti ekti sensor.)',
        'ornek_en': 'What is this device? This is a sensor.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Bu nedir? / Kimdir?'},
    {   'ara_okunus': "Kemi's-sâatü? / El-yevm",
        'arapca': 'كَمِ السَّاعَةُ؟ / الْيَوْمَ',
        'ben_okunus': 'Ekhon koyta baje? / Aj',
        'bengalce': 'এখন কয়টা বাজে? / আজ',
        'id': 11,
        'ing_okunus': 'Vat taym iz it? / Tudey',
        'ingilizce': 'What time is it? / Today',
        'kategori': 'Zaman & Saat',
        'ornek_ar': "كَمِ السَّاعَةُ الْآنَ مَنْ فَضْلِكَ؟ (Kemi's-sâatü el-âne min fadlike?)",
        'ornek_bn': 'অনুগ্রহ করে বলবেন এখন কয়টা বাজে? (Onugroho kore bolben ekhon koyta baje?)',
        'ornek_en': 'What time is it right now?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Saat kaç? / Bugün'},
    {   'ara_okunus': 'Ürîdü mâen ve taâmen.',
        'arapca': 'أُرِيدُ مَاءً وَطَعَامًا.',
        'ben_okunus': 'Ami pani ebong khabar chai.',
        'bengalce': 'আমি পানি এবং খাবার চাই।',
        'id': 12,
        'ing_okunus': 'Ay vant votır end fud.',
        'ingilizce': 'I want water and food.',
        'kategori': 'Günlük İhtiyaçlar',
        'ornek_ar': 'هَلْ يُمْكِنُنِي الْحُصُولُ عَلَى كُوبِ مَاءٍ مَنْ فَضْلِكَ؟ (Hel yümkınunî '
                    'el-husûlü alâ kûbi mâin min fadlike?)',
        'ornek_bn': 'দয়া করে আমাকে এক গ্লাস পানি দেবেন? (Doya kore amake ek glas pani deben?)',
        'ornek_en': 'Can I have a glass of cold water, please?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Su ve yemek istiyorum.'},
    {   'ara_okunus': 'Vâhid, isnân, selâse, erbaa, hamse',
        'arapca': 'وَاحِدٌ، اِثْنَانِ، ثَلَاثَةٌ، أَرْبَعَةٌ، خَمْسَةٌ',
        'ben_okunus': 'Ek, dui, tin, char, panch',
        'bengalce': 'এক, দুই, তিন, চার, পাঁচ',
        'id': 13,
        'ing_okunus': 'Van, tu, tri, for, fayv',
        'ingilizce': 'One, two, three, four, five',
        'kategori': 'Sayılar & Hesap',
        'ornek_ar': 'عِنْدِي خَمْسَةُ كُتُبٍ جَدِيدَةٍ فِي حَقِيبَتِي. (İndî hamsetü kütübin '
                    'cedîdetin fî hakîbetî.)',
        'ornek_bn': 'আমার ব্যাগে পাঁচটি নতুন বই আছে। (Amar byage panchti notun boi ache.)',
        'ornek_en': 'I have five new books in my bag.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Bir, iki, üç, dört, beş'},
    {   'ara_okunus': 'Hel yümkınuke müsâadetî min fadlike?',
        'arapca': 'هَلْ يُمْكِنُكَ مُسَاعَدَتِي مَنْ فَضْلِكَ؟',
        'ben_okunus': 'Doya kore amake shahajjo korte parben?',
        'bengalce': 'দয়া করে আমাকে সাহায্য করতে পারবেন?',
        'id': 14,
        'ing_okunus': 'Ken yu help mi, pliz?',
        'ingilizce': 'Can you help me, please?',
        'kategori': 'Yardım & İletişim',
        'ornek_ar': 'عَفْوًا، هَلْ يُمْكِنُكَ مُسَاعَدَتِي فِي هَذَا السُّؤَالِ؟ (Afven, hel '
                    "yümkınuke müsâadetî fî hâze's-süâli?)",
        'ornek_bn': 'আমাকে এই প্রশ্নে একটু সাহায্য করতে পারবেন? (Amake ei proshne ektu shahajjo '
                    'korte parben?)',
        'ornek_en': 'Excuse me, can you help me with this question?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Lütfen bana yardım eder misin?'},
    {   'ara_okunus': "Ene eteal-lemu el-İncilîziyyete ve'l-Arabiyyete ve'l-Bengâliyyete.",
        'arapca': 'أَنَا أَتَعَلَّمُ الْإِنْجِلِيزِيَّةَ وَالْعَرَبِيَّةَ وَالْبَنْغَالِيَّةَ.',
        'ben_okunus': 'Ami Ingreji, Arbi ebong Bangla shikhchi.',
        'bengalce': 'আমি ইংরেজি, আরবি এবং বাংলা শিখছি।',
        'id': 15,
        'ing_okunus': 'Ay em lörning İngliş, Arabik end Bengali.',
        'ingilizce': 'I am learning English, Arabic and Bengali.',
        'kategori': 'Dil Öğrenimi',
        'ornek_ar': 'أَنَا أَتَدَرَّبُ عَلَى كَلِمَاتٍ جَدِيدَةٍ كُلَّ يَوْمٍ. (Ene etederrabu alâ '
                    'kelimâtin cedîdetin külle yevmin.)',
        'ornek_bn': 'আমি প্রতিদিন নতুন শব্দ অনুশীলন করি। (Ami protidin notun shobdo onushilon '
                    'kori.)',
        'ornek_en': 'I practice new words every day.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'İngilizce, Arapça ve Bengalce öğreniyorum.'},
    {   'ara_okunus': "Ene ektübü bermecete Python ale'l-hâsûbi.",
        'arapca': 'أَنَا أَكْتُبُ بَرْمَجَةَ بَايْثُون عَلَى الْحَاسُوبِ.',
        'ben_okunus': 'Ami kompiutare Python kod likhchi.',
        'bengalce': 'আমি কম্পিউটারে পাইথন কোড লিখছি।',
        'id': 16,
        'ing_okunus': 'Ay em rayting Paytın kod on dı kompyutır.',
        'ingilizce': 'I am writing Python code on the computer.',
        'kategori': 'Teknoloji & Yazılım',
        'ornek_ar': 'أَنَا أُطَوِّرُ مُسَاعِدَ الذَّكَاءِ الِاصْطِنَاعِيِّ الْخَاصَّ بِي. (Ene '
                    "utavviru müsâide'z-zekâi'l-ıstınâiyyi el-hâssa bî.)",
        'ornek_bn': 'আমি পাইথন দিয়ে আমার নিজের এআই সহকারী তৈরি করছি। (Ami Python diye amar nijer '
                    'AI shohokari toiri korchi.)',
        'ornek_en': 'I am developing my own artificial intelligence assistant with Python.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Bilgisayarda Python kodu yazıyorum.'},
    {   'ara_okunus': 'Ene usammimu tâiraten müseyyeraten zâtiyyeten ve arabete etfâlin '
                      'zekiyyeten.',
        'arapca': 'أَنَا أُصَمِّمُ طَائِرَةً مُسَيَّرَةً ذَاتِيَّةً وَعَرَبَةَ أَطْفَالٍ '
                  'ذَكِيَّةً.',
        'ben_okunus': 'Ami ekti sboyongkriyo drone ebong smart bebi strolar dijain korchi.',
        'bengalce': 'আমি একটি স্বয়ংক্রিয় ড্রোন এবং স্মার্ট বেবি স্ট্রলার ডিজাইন করছি।',
        'id': 17,
        'ing_okunus': 'Ay em dizayning en otonomıs dron end e smart beybi strolır.',
        'ingilizce': 'I am designing an autonomous drone and a smart baby stroller.',
        'kategori': 'Mühendislik & Projeler',
        'ornek_ar': 'سَيُشَارِكُ هَذَا الْمَشْرُوعُ فِي مِهْرَجَانِ تَكْنُوفِسْت. (Seyüşâriku '
                    "hâze'l-meşrûu fî mihrecâni Teknofest.)",
        'ornek_bn': 'এই প্রজেক্টটি টেকনোফেস্ট প্রতিযোগিতায় অংশ নেবে। (Ei projektti Teknofest '
                    'protijogitay ongsho nebe.)',
        'ornek_en': 'This project will compete in TEKNOFEST.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Otonom bir drone ve akıllı bebek arabası tasarlıyorum.'},
    {   'ara_okunus': "Ene uhibbu dürûse'r-riyâdiyyâti ve'l-fîzyâi kesîran.",
        'arapca': 'أَنَا أُحِبُّ دُرُوسَ الرِّيَاضِيَّاتِ وَالْفِيزْيَاءِ كَثِيرًا.',
        'ben_okunus': 'Ami gonit ebong podarthobiggan klas khub pochondo kori.',
        'bengalce': 'আমি গণিত এবং পদার্থবিজ্ঞান ক্লাস খুব পছন্দ করি।',
        'id': 18,
        'ing_okunus': 'Ay layk matematiks end fiziks lesıns veri maç.',
        'ingilizce': 'I like mathematics and physics lessons very much.',
        'kategori': 'Ders & Sınavlar',
        'ornek_ar': 'حَلُّ مَسَائِلِ الْجَبْرِ وَالْجُذُورِ التَّرْبِيعِيَّةِ مُمْتِعٌ جِدًّا. '
                    "(Hallü mesâili'l-cebri ve'l-cüzûri't-terbîiyyeti mümtiun cidden.)",
        'ornek_bn': 'বীজগণিত এবং বর্গমূলের সমস্যা সমাধান করা খুব আনন্দের। (Bijgonit ebong '
                    'borgomuler shomossha shomadhan kora khub anonder.)',
        'ornek_en': 'Solving square root and algebra problems is fun.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Matematik ve fizik derslerini çok seviyorum.'},
    {   'ara_okunus': "Esteykızu mübekkiran fi's-sabâhı ve ünhî vâcibâtî.",
        'arapca': 'أَسْتَيْقِظُ مُبَكِّرًا فِي الصَّبَاحِ وَأُنْهِـي وَاجِبَاتِي.',
        'ben_okunus': 'Ami shokale taratari uthi ebong amar barir kaj shesh kori.',
        'bengalce': 'আমি সকালে তাড়াতাড়ি উঠি এবং আমার বাড়ির কাজ শেষ করি।',
        'id': 19,
        'ing_okunus': 'Ay veyk ap örli in dı morning end finiş may homvörk.',
        'ingilizce': 'I wake up early in the morning and finish my homework.',
        'kategori': 'Günlük Rutin',
        'ornek_ar': 'النَّوْمُ الْمُنْتَظَمُ وَالِانْضِبَاطُ مُهِمَّانِ لِلنَّجَاحِ. '
                    "(En-nevmü'l-müntazamü ve'l-indibâtu mühimmâni li'n-necâhı.)",
        'ornek_bn': 'সাফল্যের জন্য নিয়মিত ঘুম এবং শৃঙ্খলা অত্যন্ত গুরুত্বপূর্ণ। (Shafoller jonno '
                    'niyomito ghum ebong srinkhola ottonto guruttovurno.)',
        'ornek_en': 'Regular sleep and discipline are important for success.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Sabah erken uyanırım ve ödevlerimi tamamlarım.'},
    {   'ara_okunus': "El'abu kürate'l-kademi mea esdıkâî fî utleti nihâyeti'l-üsbûi.",
        'arapca': 'أَلْعَبُ كُرَةَ الْقَدَمِ مَعَ أَصْدِقَائِي فِي عُطْلَةِ نِهَايَةِ '
                  'الْأُسْبُوعِ.',
        'ben_okunus': 'Shoptahante ami amar bondhuder sathe futbol kheli.',
        'bengalce': 'সপ্তাহান্তে আমি আমার বন্ধুদের সাথে ফুটবল খেলি।',
        'id': 20,
        'ing_okunus': 'Ay pley futbol vit may frendz on dı vikend.',
        'ingilizce': 'I play football with my friends on the weekend.',
        'kategori': 'Spor & Hobiler',
        'ornek_ar': 'فَرِيقِي الْمُفَضَّلُ فِي كُرَةِ الْقَدَمِ هُوَ غَلَطَة سَرَاي. (Ferîkî '
                    "el-mufaddalü fî kürati'l-kademi hüve Galatasarây.)",
        'ornek_bn': 'গ্যালাতাসারাই আমার প্রিয় ফুটবল দল। (Galatasaray amar priyo futbol dol.)',
        'ornek_en': 'Galatasaray is my favorite football team.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Hafta sonu arkadaşlarımla futbol oynuyorum.'},
    {   'ara_okunus': "Keyfe yümkınunî ez-zehâbu ile'l-medreseti evi'l-mektebeti?",
        'arapca': 'كَيْفَ يُمْكِنُنِي الذَّهَابُ إِلَى الْمَدْرَسَةِ أَوِ الْمَكْتَبَةِ؟',
        'ben_okunus': 'Ami kibhabe skul ba laibrerite jete pari?',
        'bengalce': 'আমি কীভাবে স্কুল বা লাইব্রেরিতে যেতে পারি?',
        'id': 21,
        'ing_okunus': 'Hav ken ay get tu dı skul or dı laybreri?',
        'ingilizce': 'How can I get to the school or the library?',
        'kategori': 'Yön & Ulaşım',
        'ornek_ar': 'اِذْهَبْ مُبَاشَرَةً ثُمَّ انْعَطِفْ يَمِينًا عِنْدَ الزَّاوِيَةِ. (İzheb '
                    "mübâşeraten sümme in'atıf yemînen inde'z-zâviyeti.)",
        'ornek_bn': 'সোজা সামনে যান এবং মোড় থেকে ডানে ঘুরুন। (Shoja shamne jan ebong mor theke '
                    'dane ghurun.)',
        'ornek_en': 'Go straight ahead and turn right at the corner.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Okula veya kütüphaneye nasıl gidebilirim?'},
    {   'ara_okunus': "Hel yümkınuke et-tehaddüsü bi-but'in eksera min fadlike?",
        'arapca': 'هَلْ يُمْكِنُكَ التَّحَدُّثُ بِبُطْءٍ أَكْثَرَ مَنْ فَضْلِكَ؟',
        'ben_okunus': 'Doya kore arektu dhire kotha bolte parben?',
        'bengalce': 'দয়া করে আরেকটু ধীরে কথা বলতে পারবেন?',
        'id': 22,
        'ing_okunus': 'Kud yu spik e litıl mor slovli, pliz?',
        'ingilizce': 'Could you speak a little more slowly, please?',
        'kategori': 'İletişim & Anlama',
        'ornek_ar': 'هَلْ يُمْكِنُكَ إِعَادَةُ هَذِهِ الْجُمْلَةِ مَنْ فَضْلِكَ؟ (Hel yümkınuke '
                    "iâdetü hâzihi'l-cümleti min fadlike?)",
        'ornek_bn': 'দয়া করে এই বাক্যটি আবার বলবেন? (Doya kore ei bakkoti abar bolben?)',
        'ornek_en': 'Could you repeat that sentence, please?',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Lütfen biraz daha yavaş konuşabilir misiniz?'},
    {   'ara_okunus': "Yekteşifu'l-müsteş'iru el-âika ve yûkıfu'l-muharrikâti tilkâiyyen.",
        'arapca': 'يَكْتَشِفُ الْمُسْتَشْعِرُ الْعَائِقَ وَيُوقِفُ الْمُحَرِّكَاتِ تِلْقَائِيًّا.',
        'ben_okunus': 'Sensorti badha shonakto kore ebong sboyongkriyobhabe motor thamiye dey.',
        'bengalce': 'সেন্সরটি বাধা শনাক্ত করে এবং স্বয়ংক্রিয়ভাবে মোটর থামিয়ে দেয়।',
        'id': 23,
        'ing_okunus': 'Dı sensör ditekts dı obstıkıl end stops dı motors otomatikli.',
        'ingilizce': 'The sensor detects the obstacle and stops the motors automatically.',
        'kategori': 'Robotik & Sensör',
        'ornek_ar': 'السَّلَامَةُ هِيَ أَهَمُّ جُزْءٍ فِي عَرَبَةِ الْأَطْفَالِ الذَّكِيَّةِ. '
                    "(Es-selâmetü hiye ehemmü cüz'in fî arabeti'l-etfâli'z-zekiyyeti.)",
        'ornek_bn': 'স্মার্ট বেবি স্ট্রলারের সবচেয়ে গুরুত্বপূর্ণ অংশ হলো নিরাপত্তা। (Smart bebi '
                    'strolarer shobcheye guruttovurno ongsho holo nirapotta.)',
        'ornek_en': 'Safety is the most important part of the smart baby stroller.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Sensör engeli algılar ve motorları otomatik durdurur.'},
    {   'ara_okunus': 'Ürîdü en usbiha mühendise bermeciyyâtin ve rûbûtâtin nâcihan '
                      "fi'l-müstakbeli.",
        'arapca': 'أُرِيدُ أَنْ أُصْبِحَ مُهَنْدِسَ بَرْمَجِيَّاتٍ وَرُوبُوتَاتٍ نَاجِحًا فِي '
                  'الْمُسْتَقْبَلِ.',
        'ben_okunus': 'Ami bhobishshote ekjon shofol software ebong robotics injiniyar hote chai.',
        'bengalce': 'আমি ভবিষ্যতে একজন সফল সফটওয়্যার এবং রোবোটিক্স ইঞ্জিনিয়ার হতে চাই।',
        'id': 24,
        'ing_okunus': 'Ay vant tu bikam e saksesful softveyr end robotiks encinir in dı fyuçır.',
        'ingilizce': 'I want to become a successful software and robotics engineer in the future.',
        'kategori': 'Bilim & Gelecek',
        'ornek_ar': 'الْعَمَلُ الْجَادُّ كُلَّ يَوْمٍ يَجْلِبُ إِنْجَازَاتٍ عَظِيمَةً. '
                    "(El-amelü'l-câddü külle yevmin yeclibü incâzâtin azîmeten.)",
        'ornek_bn': 'প্রতিদিন কঠোর পরিশ্রম করলে বড় সাফল্য আসে। (Protidin kothor porishrom korle '
                    'boro shafollo ashe.)',
        'ornek_en': 'Working hard every day brings great achievements.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Gelecekte başarılı bir yazılım ve robotik mühendisi olmak istiyorum.'},
    {   'ara_okunus': 'Beytun, medresetün ve mektebetün',
        'arapca': 'بَيْتٌ، مَدْرَسَةٌ وَمَكْتَبَةٌ',
        'ben_okunus': 'Bari, skul ebong laibreri',
        'bengalce': 'বাড়ি, স্কুল এবং লাইব্রেরি',
        'id': 25,
        'ing_okunus': 'Hauz, skul end laybreri',
        'ingilizce': 'House, school and library',
        'kategori': 'Günlük Hayat',
        'ornek_ar': 'بَيْتٌ، مَدْرَسَةٌ وَمَكْتَبَةٌ (Beytun, medresetün ve mektebetün)',
        'ornek_bn': 'বাড়ি, স্কুল এবং লাইব্রেরি (Bari, skul ebong laibreri)',
        'ornek_en': 'House, school and library',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Ev, okul ve kütüphane'},
    {   'ara_okunus': 'Et-taksu cemîlün cidden el-yevm.',
        'arapca': 'الطَّقْسُ جَمِيلٌ جِدًّا الْيَوْمَ.',
        'ben_okunus': 'Aj abohawa khub shundor.',
        'bengalce': 'আজ আবহাওয়া খুব সুন্দর।',
        'id': 26,
        'ing_okunus': 'Dı vedır iz veri nays tudey.',
        'ingilizce': 'The weather is very nice today.',
        'kategori': 'Zaman & Günler',
        'ornek_ar': 'الطَّقْسُ جَمِيلٌ جِدًّا الْيَوْمَ. (Et-taksu cemîlün cidden el-yevm.)',
        'ornek_bn': 'আজ আবহাওয়া খুব সুন্দর। (Aj abohawa khub shundor.)',
        'ornek_en': 'The weather is very nice today.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Bugün hava çok güzel.'},
    {   'ara_okunus': 'Ledeyye sittetü ihvetin.',
        'arapca': 'لَدَيَّ سِتَّةُ إِخْوَةٍ.',
        'ben_okunus': 'Amar choy bhaibon ache.',
        'bengalce': 'আমার ছয় ভাইবোন আছে।',
        'id': 27,
        'ing_okunus': 'Ay hev siks siblings.',
        'ingilizce': 'I have six siblings.',
        'kategori': 'Aile & Kişiler',
        'ornek_ar': 'لَدَيَّ سِتَّةُ إِخْوَةٍ. (Ledeyye sittetü ihvetin.)',
        'ornek_bn': 'আমার ছয় ভাইবোন আছে। (Amar choy bhaibon ache.)',
        'ornek_en': 'I have six siblings.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Benim altı kardeşim var.'},
    {   'ara_okunus': "El-muallimu yeşrahu'd-derse fi's-saffi.",
        'arapca': 'الْمُعَلِّمُ يَشْرَحُ الدَّرْسَ فِي الصَّفِّ.',
        'ben_okunus': 'Shikkhok shrenikokkhe pathdan korchen.',
        'bengalce': 'শিক্ষক শ্রেণিকক্ষে পাঠদান করছেন।',
        'id': 28,
        'ing_okunus': 'Dı tiçır iz tiçing in dı klasrum.',
        'ingilizce': 'The teacher is teaching in the classroom.',
        'kategori': 'Okul & Ders',
        'ornek_ar': "الْمُعَلِّمُ يَشْرَحُ الدَّرْسَ فِي الصَّفِّ. (El-muallimu yeşrahu'd-derse "
                    "fi's-saffi.)",
        'ornek_bn': 'শিক্ষক শ্রেণিকক্ষে পাঠদান করছেন। (Shikkhok shrenikokkhe pathdan korchen.)',
        'ornek_en': 'The teacher is teaching in the classroom.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Öğretmen sınıfta ders anlatıyor.'},
    {   'ara_okunus': "Uhibbu'ş-şâye ve'l-cübne fi'l-fatûri.",
        'arapca': 'أُحِبُّ الشَّايَ وَالْجُبْنَ فِي الْفَطُورِ.',
        'ben_okunus': 'Ami nastay cha ebong ponir pochondo kori.',
        'bengalce': 'আমি নাস্তায় চা এবং পনির পছন্দ করি।',
        'id': 29,
        'ing_okunus': 'Ay layk ti end çiz for brekfıst.',
        'ingilizce': 'I like tea and cheese for breakfast.',
        'kategori': 'Yiyecek & İçecek',
        'ornek_ar': "أُحِبُّ الشَّايَ وَالْجُبْنَ فِي الْفَطُورِ. (Uhibbu'ş-şâye ve'l-cübne "
                    "fi'l-fatûri.)",
        'ornek_bn': 'আমি নাস্তায় চা এবং পনির পছন্দ করি। (Ami nastay cha ebong ponir pochondo '
                    'kori.)',
        'ornek_en': 'I like tea and cheese for breakfast.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Kahvaltıda çay ve peynir severim.'},
    {   'ara_okunus': 'İstanbul hiye ekberu medînetin fî Türkiyâ.',
        'arapca': 'إِسْطَنْبُولُ هِيَ أَكْبَرُ مَدِينَةٍ فِي تُرْكِيَا.',
        'ben_okunus': 'Istambul Turosker brihottomo shohor.',
        'bengalce': 'ইস্তাম্বুল তুরস্কের বৃহত্তম শহর।',
        'id': 30,
        'ing_okunus': 'İstanbul iz dı larcıst siti in Törki.',
        'ingilizce': 'Istanbul is the largest city in Turkey.',
        'kategori': 'Yön & Konum',
        'ornek_ar': 'إِسْطَنْبُولُ هِيَ أَكْبَرُ مَدِينَةٍ فِي تُرْكِيَا. (İstanbul hiye ekberu '
                    'medînetin fî Türkiyâ.)',
        'ornek_bn': 'ইস্তাম্বুল তুরস্কের বৃহত্তম শহর। (Istambul Turosker brihottomo shohor.)',
        'ornek_en': 'Istanbul is the largest city in Turkey.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': "İstanbul Türkiye'nin en büyük şehridir."},
    {   'ara_okunus': "El-kırâetü, el-kitâbetü ve't-tefkîru",
        'arapca': 'الْقِرَاءَةُ، الْكِتَابَةُ وَالتَّفْكِيرُ',
        'ben_okunus': 'Pora, lekha ebong chinta kora',
        'bengalce': 'পড়া, লেখা এবং চিন্তা করা',
        'id': 31,
        'ing_okunus': 'Tu rid, tu rayt end tu tink',
        'ingilizce': 'To read, to write and to think',
        'kategori': 'Temel Fiiller',
        'ornek_ar': 'الْقِرَاءَةُ، الْكِتَابَةُ وَالتَّفْكِيرُ (El-kırâetü, el-kitâbetü '
                    "ve't-tefkîru)",
        'ornek_bn': 'পড়া, লেখা এবং চিন্তা করা (Pora, lekha ebong chinta kora)',
        'ornek_en': 'To read, to write and to think',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Okumak, yazmak ve düşünmek'},
    {   'ara_okunus': 'Ezraku dâkinun, ezraku ve ebyadu',
        'arapca': 'أَزْرَقُ دَاكِنٌ، أَزْرَقُ وَأَبْيَضُ',
        'ben_okunus': 'Garho nebhi, nil ebong shada',
        'bengalce': 'গাঢ় নেভি, নীল এবং সাদা',
        'id': 32,
        'ing_okunus': 'Dark neyvi, blu end vayt',
        'ingilizce': 'Dark navy, blue and white',
        'kategori': 'Renkler & Sıfatlar',
        'ornek_ar': 'أَزْرَقُ دَاكِنٌ، أَزْرَقُ وَأَبْيَضُ (Ezraku dâkinun, ezraku ve ebyadu)',
        'ornek_bn': 'গাঢ় নেভি, নীল এবং সাদা (Garho nebhi, nil ebong shada)',
        'ornek_en': 'Dark navy, blue and white',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Koyu lacivert, mavi ve beyaz'},
    {   'ara_okunus': 'Eyne teîşu?',
        'arapca': 'أَيْنَ تَعِيشُ؟',
        'ben_okunus': 'Apni kothay thaken?',
        'bengalce': 'আপনি কোথায় থাকেন?',
        'id': 33,
        'ing_okunus': 'Ver du yu liv?',
        'ingilizce': 'Where do you live?',
        'kategori': 'Soru Kalıpları',
        'ornek_ar': 'أَيْنَ تَعِيشُ؟ (Eyne teîşu?)',
        'ornek_bn': 'আপনি কোথায় থাকেন? (Apni kothay thaken?)',
        'ornek_en': 'Where do you live?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Nerede yaşıyorsun?'},
    {   'ara_okunus': 'Kem umruke?',
        'arapca': 'كَمْ عُمْرُكَ؟',
        'ben_okunus': 'Apnar boyosh koto?',
        'bengalce': 'আপনার বয়স কত?',
        'id': 34,
        'ing_okunus': 'Hav old ar yu?',
        'ingilizce': 'How old are you?',
        'kategori': 'Soru Kalıpları',
        'ornek_ar': 'كَمْ عُمْرُكَ؟ (Kem umruke?)',
        'ornek_bn': 'আপনার বয়স কত? (Apnar boyosh koto?)',
        'ornek_en': 'How old are you?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Kaç yaşındasın?'},
    {   'ara_okunus': "Şâşetü'l-hâtifi ve'l-hâsûbi",
        'arapca': 'شَاشَةُ الْهَاتِفِ وَالْحَاسُوبِ',
        'ben_okunus': 'Fon ebong kompiutarer porda',
        'bengalce': 'ফোন এবং কম্পিউটারের পর্দা',
        'id': 35,
        'ing_okunus': 'Fon end kompyutır skrin',
        'ingilizce': 'Phone and computer screen',
        'kategori': 'Teknoloji',
        'ornek_ar': "شَاشَةُ الْهَاتِفِ وَالْحَاسُوبِ (Şâşetü'l-hâtifi ve'l-hâsûbi)",
        'ornek_bn': 'ফোন এবং কম্পিউটারের পর্দা (Fon ebong kompiutarer porda)',
        'ornek_en': 'Phone and computer screen',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Telefon ve bilgisayar ekranı'},
    {   'ara_okunus': "Afven, ale'r-rahbi ve's-seati.",
        'arapca': 'عَفْوًا، عَلَى الرَّحْبِ وَالسَّعَةِ.',
        'ben_okunus': 'Dukkhito, apnake sbagotom.',
        'bengalce': 'দুঃখিত, আপনাকে স্বাগতম।',
        'id': 36,
        'ing_okunus': 'Ekskyuz mi, yu ar velkım.',
        'ingilizce': 'Excuse me, you are welcome.',
        'kategori': 'Nezaket',
        'ornek_ar': "عَفْوًا، عَلَى الرَّحْبِ وَالسَّعَةِ. (Afven, ale'r-rahbi ve's-seati.)",
        'ornek_bn': 'দুঃখিত, আপনাকে স্বাগতম। (Dukkhito, apnake sbagotom.)',
        'ornek_en': 'Excuse me, you are welcome.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Özür dilerim, rica ederim.'},
    {   'ara_okunus': "Kaddeme ulemâu'l-İslâmi müsâhemâtin azîmeten li'l-ilmi.",
        'arapca': 'قَدَّمَ عُلَمَاءُ الْإِسْلَامِ مُسَاهَمَاتٍ عَظِيمَةً لِلْعِلْمِ.',
        'ben_okunus': 'Islami ponditgon biggane bishal obodan rekhechen.',
        'bengalce': 'ইসলামী পণ্ডিতগণ বিজ্ঞানে বিশাল অবদান রেখেছেন।',
        'id': 37,
        'ing_okunus': 'İslamik skolırs meyd greyt kontribyuşınz tu sayns.',
        'ingilizce': 'Islamic scholars made great contributions to science.',
        'kategori': 'Bilim & Tarih',
        'ornek_ar': 'قَدَّمَ عُلَمَاءُ الْإِسْلَامِ مُسَاهَمَاتٍ عَظِيمَةً لِلْعِلْمِ. (Kaddeme '
                    "ulemâu'l-İslâmi müsâhemâtin azîmeten li'l-ilmi.)",
        'ornek_bn': 'ইসলামী পণ্ডিতগণ বিজ্ঞানে বিশাল অবদান রেখেছেন। (Islami ponditgon biggane '
                    'bishal obodan rekhechen.)',
        'ornek_en': 'Islamic scholars made great contributions to science.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'İslam âlimleri bilime büyük katkı sağladı.'},
    {   'ara_okunus': "Yünticü'l-muharrikü'l-kehrabâiyyü azme deverânin âlin.",
        'arapca': 'يُنْتِجُ الْمُحَرِّكُ الْكَهْرَبَائِيُّ عَزْمَ دَوَرَانٍ عَالٍ.',
        'ben_okunus': 'Boiddutik motor uccho tork utponno kore.',
        'bengalce': 'বৈদ্যুতিক মোটর উচ্চ টর্ক উৎপন্ন করে।',
        'id': 38,
        'ing_okunus': 'Dı elektrik motor prodüsuz hay tork.',
        'ingilizce': 'The electric motor produces high torque.',
        'kategori': 'Mühendislik',
        'ornek_ar': 'يُنْتِجُ الْمُحَرِّكُ الْكَهْرَبَائِيُّ عَزْمَ دَوَرَانٍ عَالٍ. '
                    "(Yünticü'l-muharrikü'l-kehrabâiyyü azme deverânin âlin.)",
        'ornek_bn': 'বৈদ্যুতিক মোটর উচ্চ টর্ক উৎপন্ন করে। (Boiddutik motor uccho tork utponno '
                    'kore.)',
        'ornek_en': 'The electric motor produces high torque.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Elektrik motoru yüksek tork üretir.'},
    {   'ara_okunus': "Tetîru't-tâiratü bidûni tayyârin zâtiyyen ile'l-hedefi.",
        'arapca': 'تَطِيرُ الطَّائِرَةُ بِدُونِ طَيَّارٍ ذَاتِيًّا إِلَى الْهَدَفِ.',
        'ben_okunus': 'Monusshobihin bimanti sboyongkriyobhabe lokkhe ure jay.',
        'bengalce': 'মনুষ্যবিহীন বিমানটি স্বয়ংক্রিয়ভাবে লক্ষ্যে উড়ে যায়।',
        'id': 39,
        'ing_okunus': 'Dı anmend eriyıl viikıl flayz otonomısli tu dı targıt.',
        'ingilizce': 'The unmanned aerial vehicle flies autonomously to the target.',
        'kategori': 'Havacılık',
        'ornek_ar': 'تَطِيرُ الطَّائِرَةُ بِدُونِ طَيَّارٍ ذَاتِيًّا إِلَى الْهَدَفِ. '
                    "(Tetîru't-tâiratü bidûni tayyârin zâtiyyen ile'l-hedefi.)",
        'ornek_bn': 'মনুষ্যবিহীন বিমানটি স্বয়ংক্রিয়ভাবে লক্ষ্যে উড়ে যায়। (Monusshobihin '
                    'bimanti sboyongkriyobhabe lokkhe ure jay.)',
        'ornek_en': 'The unmanned aerial vehicle flies autonomously to the target.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'İnsansız hava aracı hedefe otonom uçar.'},
    {   'ara_okunus': "Tehfazu kâidetü'l-beyânâti cemîa'l-ma'lûmâti bi-emânin.",
        'arapca': 'تَحْفَظُ قَاعِدَةُ الْبَيَانَاتِ جَمِيعَ الْمَعْلُومَاتِ بِأَمَانٍ.',
        'ben_okunus': 'Detabes shomosto tottho nirapode shongrokkhon kore.',
        'bengalce': 'ডেটাবেস সমস্ত তথ্য নিরাপদে সংরক্ষণ করে।',
        'id': 40,
        'ing_okunus': 'Dı deytabeys stors ol informeyşın seyfli.',
        'ingilizce': 'The database stores all information safely.',
        'kategori': 'Yazılım',
        'ornek_ar': 'تَحْفَظُ قَاعِدَةُ الْبَيَانَاتِ جَمِيعَ الْمَعْلُومَاتِ بِأَمَانٍ. (Tehfazu '
                    "kâidetü'l-beyânâti cemîa'l-ma'lûmâti bi-emânin.)",
        'ornek_bn': 'ডেটাবেস সমস্ত তথ্য নিরাপদে সংরক্ষণ করে। (Detabes shomosto tottho nirapode '
                    'shongrokkhon kore.)',
        'ornek_en': 'The database stores all information safely.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Veritabanı tüm bilgileri güvenle saklar.'},
    {   'ara_okunus': "Yümkınunî hallü'l-muâdelâti hutveten bi-hutvetin.",
        'arapca': 'يُمْكِنُنِي حَلُّ الْمُعَادَلَاتِ خُطْوَةً بِخُطْوَةٍ.',
        'ben_okunus': 'Ami dhape dhape shomikoron shomadhan korte pari.',
        'bengalce': 'আমি ধাপে ধাপে সমীকরণ সমাধান করতে পারি।',
        'id': 41,
        'ing_okunus': 'Ay ken solv ikveyjıns step bay step.',
        'ingilizce': 'I can solve equations step by step.',
        'kategori': 'Matematik',
        'ornek_ar': 'يُمْكِنُنِي حَلُّ الْمُعَادَلَاتِ خُطْوَةً بِخُطْوَةٍ. (Yümkınunî '
                    "hallü'l-muâdelâti hutveten bi-hutvetin.)",
        'ornek_bn': 'আমি ধাপে ধাপে সমীকরণ সমাধান করতে পারি। (Ami dhape dhape shomikoron shomadhan '
                    'korte pari.)',
        'ornek_en': 'I can solve equations step by step.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Denklemleri adım adım çözebilirim.'},
    {   'ara_okunus': 'Edrusu kelimâtin cedîdeten li-müddeti işrîne dekîkaten külle yevmin.',
        'arapca': 'أَدْرُسُ كَلِمَاتٍ جَدِيدَةً لِمُدَّةِ عِشْرِينَ دَقِيقَةً كُلَّ يَوْمٍ.',
        'ben_okunus': 'Ami protidin bish minit notun shobdo pori.',
        'bengalce': 'আমি প্রতিদিন বিশ মিনিট নতুন শব্দ পড়ি।',
        'id': 42,
        'ing_okunus': 'Ay stadi nyu vördz for tventi minıts evri dey.',
        'ingilizce': 'I study new words for twenty minutes every day.',
        'kategori': 'Kişisel Gelişim',
        'ornek_ar': 'أَدْرُسُ كَلِمَاتٍ جَدِيدَةً لِمُدَّةِ عِشْرِينَ دَقِيقَةً كُلَّ يَوْمٍ. '
                    '(Edrusu kelimâtin cedîdeten li-müddeti işrîne dekîkaten külle yevmin.)',
        'ornek_bn': 'আমি প্রতিদিন বিশ মিনিট নতুন শব্দ পড়ি। (Ami protidin bish minit notun shobdo '
                    'pori.)',
        'ornek_en': 'I study new words for twenty minutes every day.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Her gün yirmi dakika yeni kelimeler çalışıyorum.'},
    {   'ara_okunus': "Tetevekkafu arabetü'l-etfâli tilkâiyyen inde'n-nüzûli mine'l-münhaderi.",
        'arapca': 'تَتَوَقَّفُ عَرَبَةُ الْأَطْفَالِ تِلْقَائِيًّا عِنْدَ النُّزُولِ مِنَ '
                  'الْمُنْحَدَرِ.',
        'ben_okunus': 'Bebi strolarti dhalu pothe namar shomoy sboyongkriyobhabe brek kore.',
        'bengalce': 'বেবি স্ট্রলারটি ঢালু পথে নামার সময় স্বয়ংক্রিয়ভাবে ব্রেক করে।',
        'id': 43,
        'ing_okunus': 'Dı beybi strolır breyks otomatikli ven going daunhil.',
        'ingilizce': 'The baby stroller brakes automatically when going downhill.',
        'kategori': 'Bebek Arabası Projesi',
        'ornek_ar': 'تَتَوَقَّفُ عَرَبَةُ الْأَطْفَالِ تِلْقَائِيًّا عِنْدَ النُّزُولِ مِنَ '
                    "الْمُنْحَدَرِ. (Tetevekkafu arabetü'l-etfâli tilkâiyyen inde'n-nüzûli "
                    "mine'l-münhaderi.)",
        'ornek_bn': 'বেবি স্ট্রলারটি ঢালু পথে নামার সময় স্বয়ংক্রিয়ভাবে ব্রেক করে। (Bebi '
                    'strolarti dhalu pothe namar shomoy sboyongkriyobhabe brek kore.)',
        'ornek_en': 'The baby stroller brakes automatically when going downhill.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Bebek arabası yokuş aşağı inerken otomatik fren yapar.'},
    {   'ara_okunus': "Yekîsü'l-müsteş'iru fevka's-savtiyyi el-mesâfete bi'l-mevcâti's-savtiyyeti.",
        'arapca': 'يَقِيسُ الْمُسْتَشْعِرُ فَوْقَ الصَّوْتِيِّ الْمَسَافَةَ بِالْمَوْجَاتِ '
                  'الصَّوْتِيَّةِ.',
        'ben_okunus': 'Altrasonik sensor shobdo torongo diye durottvo porimap kore.',
        'bengalce': 'আল্ট্রাসনিক সেন্সর শব্দ তরঙ্গ দিয়ে দূরত্ব পরিমাপ করে।',
        'id': 44,
        'ing_okunus': 'Dı ultrasonik sensör mejırs distıns vit saund veyvz.',
        'ingilizce': 'The ultrasonic sensor measures distance with sound waves.',
        'kategori': 'Sensör & Donanım',
        'ornek_ar': 'يَقِيسُ الْمُسْتَشْعِرُ فَوْقَ الصَّوْتِيِّ الْمَسَافَةَ بِالْمَوْجَاتِ '
                    "الصَّوْتِيَّةِ. (Yekîsü'l-müsteş'iru fevka's-savtiyyi el-mesâfete "
                    "bi'l-mevcâti's-savtiyyeti.)",
        'ornek_bn': 'আল্ট্রাসনিক সেন্সর শব্দ তরঙ্গ দিয়ে দূরত্ব পরিমাপ করে। (Altrasonik sensor '
                    'shobdo torongo diye durottvo porimap kore.)',
        'ornek_en': 'The ultrasonic sensor measures distance with sound waves.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Ultrasonik sensör ses dalgalarıyla mesafeyi ölçer.'},
    {   'ara_okunus': "En-nevmü'l-müntazamü ve'r-riyâdatü darûriyyâni li-hayâtin sıhhiyyetin.",
        'arapca': 'النَّوْمُ الْمُنْتَظَمُ وَالرِّيَاضَةُ ضَرُورِيَّانِ لِحَيَاةٍ صِحِّيَّةٍ.',
        'ben_okunus': 'Shustho jiboner jonno niyomito ghum ebong kheladhula oporiharjo.',
        'bengalce': 'সুস্থ জীবনের জন্য নিয়মিত ঘুম এবং খেলাধুলা অপরিহার্য।',
        'id': 45,
        'ing_okunus': 'Regyulır slip end sports ar esenşıl for e helti layf.',
        'ingilizce': 'Regular sleep and sports are essential for a healthy life.',
        'kategori': 'Sağlık & Spor',
        'ornek_ar': 'النَّوْمُ الْمُنْتَظَمُ وَالرِّيَاضَةُ ضَرُورِيَّانِ لِحَيَاةٍ صِحِّيَّةٍ. '
                    "(En-nevmü'l-müntazamü ve'r-riyâdatü darûriyyâni li-hayâtin sıhhiyyetin.)",
        'ornek_bn': 'সুস্থ জীবনের জন্য নিয়মিত ঘুম এবং খেলাধুলা অপরিহার্য। (Shustho jiboner jonno '
                    'niyomito ghum ebong kheladhula oporiharjo.)',
        'ornek_en': 'Regular sleep and sports are essential for a healthy life.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Sağlıklı yaşam için düzenli uyku ve spor şarttır.'},
    {   'ara_okunus': "Ne'huzü dürûse'l-ulûmi ve't-tiknûlûcyâ fî medreseti'l-meşârîi.",
        'arapca': 'نَأْخُذُ دُرُوسَ الْعُلُومِ وَالتِّكْنُولُوجْيَا فِي مَدْرَسَةِ الْمَشَارِيعِ.',
        'ben_okunus': 'Amra projekt skule biggan o projukti klas kori.',
        'bengalce': 'আমরা প্রজেক্ট স্কুলে বিজ্ঞান ও প্রযুক্তি ক্লাস করি।',
        'id': 46,
        'ing_okunus': 'Vi teyk sayns end teknoloji klasız et dı procekt skul.',
        'ingilizce': 'We take science and technology classes at the project school.',
        'kategori': 'Okul & Başarı',
        'ornek_ar': 'نَأْخُذُ دُرُوسَ الْعُلُومِ وَالتِّكْنُولُوجْيَا فِي مَدْرَسَةِ '
                    "الْمَشَارِيعِ. (Ne'huzü dürûse'l-ulûmi ve't-tiknûlûcyâ fî "
                    "medreseti'l-meşârîi.)",
        'ornek_bn': 'আমরা প্রজেক্ট স্কুলে বিজ্ঞান ও প্রযুক্তি ক্লাস করি। (Amra projekt skule '
                    'biggan o projukti klas kori.)',
        'ornek_en': 'We take science and technology classes at the project school.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Proje okulunda fen ve teknoloji dersleri alıyoruz.'},
    {   'ara_okunus': "Yümkınunî el-ittisâlü bi-müsâidi'z-zekâi'l-ıstınâiyyi min hâtifî.",
        'arapca': 'يُمْكِنُنِي الِاتِّصَالُ بِمُسَاعِدِ الذَّكَاءِ الِاصْطِنَاعِيِّ مِنْ هَاتِفِي.',
        'ben_okunus': 'Ami amar fon theke amar AI shohokarir sathe shongjog korte pari.',
        'bengalce': 'আমি আমার ফোন থেকে আমার এআই সহকারীর সাথে সংযোগ করতে পারি।',
        'id': 47,
        'ing_okunus': 'Ay ken konekt tu may ey-ay asistınt from may fon.',
        'ingilizce': 'I can connect to my AI assistant from my phone.',
        'kategori': 'İletişim',
        'ornek_ar': 'يُمْكِنُنِي الِاتِّصَالُ بِمُسَاعِدِ الذَّكَاءِ الِاصْطِنَاعِيِّ مِنْ '
                    "هَاتِفِي. (Yümkınunî el-ittisâlü bi-müsâidi'z-zekâi'l-ıstınâiyyi min hâtifî.)",
        'ornek_bn': 'আমি আমার ফোন থেকে আমার এআই সহকারীর সাথে সংযোগ করতে পারি। (Ami amar fon theke '
                    'amar AI shohokarir sathe shongjog korte pari.)',
        'ornek_en': 'I can connect to my AI assistant from my phone.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Telefonumdan yapay zeka asistanıma bağlanabiliyorum.'},
    {   'ara_okunus': "Es-sabru ve'l-amelü'l-müntazamü yeftehâni külle bâbin.",
        'arapca': 'الصَّبْرُ وَالْعَمَلُ الْمُنْتَظَمُ يَفْتَحَانِ كُلَّ بَابٍ.',
        'ben_okunus': 'Dhoirjo ebong niyomito oddhoyon protiti dorja khule dey.',
        'bengalce': 'ধৈর্য এবং নিয়মিত অধ্যয়ন প্রতিটি দরজা খুলে দেয়।',
        'id': 48,
        'ing_okunus': 'Peyşıns end regyulır stadi opın evri dor.',
        'ingilizce': 'Patience and regular study open every door.',
        'kategori': 'Hedef & Başarı',
        'ornek_ar': 'الصَّبْرُ وَالْعَمَلُ الْمُنْتَظَمُ يَفْتَحَانِ كُلَّ بَابٍ. (Es-sabru '
                    "ve'l-amelü'l-müntazamü yeftehâni külle bâbin.)",
        'ornek_bn': 'ধৈর্য এবং নিয়মিত অধ্যয়ন প্রতিটি দরজা খুলে দেয়। (Dhoirjo ebong niyomito '
                    'oddhoyon protiti dorja khule dey.)',
        'ornek_en': 'Patience and regular study open every door.',
        'seviye': 'A2 (Temel Orta)',
        'turkce': 'Sabır ve düzenli çalışma her kapıyı açar.'},
    {   'ara_okunus': 'Beytun, medresetün ve mektebetün',
        'arapca': 'بَيْتٌ، مَدْرَسَةٌ وَمَكْتَبَةٌ',
        'ben_okunus': 'Bari, skul ebong laibreri',
        'bengalce': 'বাড়ি, স্কুল এবং লাইব্রেরি',
        'id': 49,
        'ing_okunus': 'Hauz, skul end laybreri',
        'ingilizce': 'House, school and library',
        'kategori': 'Günlük Hayat',
        'ornek_ar': 'بَيْتٌ، مَدْرَسَةٌ وَمَكْتَبَةٌ (Beytun, medresetün ve mektebetün)',
        'ornek_bn': 'বাড়ি, স্কুল এবং লাইব্রেরি (Bari, skul ebong laibreri)',
        'ornek_en': 'House, school and library',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Ev, okul ve kütüphane'},
    {   'ara_okunus': 'Et-taksu cemîlün cidden el-yevm.',
        'arapca': 'الطَّقْسُ جَمِيلٌ جِدًّا الْيَوْمَ.',
        'ben_okunus': 'Aj abohawa khub shundor.',
        'bengalce': 'আজ আবহাওয়া খুব সুন্দর।',
        'id': 50,
        'ing_okunus': 'Dı vedır iz veri nays tudey.',
        'ingilizce': 'The weather is very nice today.',
        'kategori': 'Zaman & Günler',
        'ornek_ar': 'الطَّقْسُ جَمِيلٌ جِدًّا الْيَوْمَ. (Et-taksu cemîlün cidden el-yevm.)',
        'ornek_bn': 'আজ আবহাওয়া খুব সুন্দর। (Aj abohawa khub shundor.)',
        'ornek_en': 'The weather is very nice today.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Bugün hava çok güzel.'},
    {   'ara_okunus': 'Ledeyye sittetü ihvetin.',
        'arapca': 'لَدَيَّ سِتَّةُ إِخْوَةٍ.',
        'ben_okunus': 'Amar choy bhaibon ache.',
        'bengalce': 'আমার ছয় ভাইবোন আছে।',
        'id': 51,
        'ing_okunus': 'Ay hev siks siblings.',
        'ingilizce': 'I have six siblings.',
        'kategori': 'Aile & Kişiler',
        'ornek_ar': 'لَدَيَّ سِتَّةُ إِخْوَةٍ. (Ledeyye sittetü ihvetin.)',
        'ornek_bn': 'আমার ছয় ভাইবোন আছে। (Amar choy bhaibon ache.)',
        'ornek_en': 'I have six siblings.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Benim altı kardeşim var.'},
    {   'ara_okunus': "El-muallimu yeşrahu'd-derse fi's-saffi.",
        'arapca': 'الْمُعَلِّمُ يَشْرَحُ الدَّرْسَ فِي الصَّفِّ.',
        'ben_okunus': 'Shikkhok shrenikokkhe pathdan korchen.',
        'bengalce': 'শিক্ষক শ্রেণিকক্ষে পাঠদান করছেন।',
        'id': 52,
        'ing_okunus': 'Dı tiçır iz tiçing in dı klasrum.',
        'ingilizce': 'The teacher is teaching in the classroom.',
        'kategori': 'Okul & Ders',
        'ornek_ar': "الْمُعَلِّمُ يَشْرَحُ الدَّرْسَ فِي الصَّفِّ. (El-muallimu yeşrahu'd-derse "
                    "fi's-saffi.)",
        'ornek_bn': 'শিক্ষক শ্রেণিকক্ষে পাঠদান করছেন। (Shikkhok shrenikokkhe pathdan korchen.)',
        'ornek_en': 'The teacher is teaching in the classroom.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Öğretmen sınıfta ders anlatıyor.'},
    {   'ara_okunus': "Uhibbu'ş-şâye ve'l-cübne fi'l-fatûri.",
        'arapca': 'أُحِبُّ الشَّايَ وَالْجُبْنَ فِي الْفَطُورِ.',
        'ben_okunus': 'Ami nastay cha ebong ponir pochondo kori.',
        'bengalce': 'আমি নাস্তায় চা এবং পনির পছন্দ করি।',
        'id': 53,
        'ing_okunus': 'Ay layk ti end çiz for brekfıst.',
        'ingilizce': 'I like tea and cheese for breakfast.',
        'kategori': 'Yiyecek & İçecek',
        'ornek_ar': "أُحِبُّ الشَّايَ وَالْجُبْنَ فِي الْفَطُورِ. (Uhibbu'ş-şâye ve'l-cübne "
                    "fi'l-fatûri.)",
        'ornek_bn': 'আমি নাস্তায় চা এবং পনির পছন্দ করি। (Ami nastay cha ebong ponir pochondo '
                    'kori.)',
        'ornek_en': 'I like tea and cheese for breakfast.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Kahvaltıda çay ve peynir severim.'},
    {   'ara_okunus': 'İstanbul hiye ekberu medînetin fî Türkiyâ.',
        'arapca': 'إِسْطَنْبُولُ هِيَ أَكْبَرُ مَدِينَةٍ فِي تُرْكِيَا.',
        'ben_okunus': 'Istambul Turosker brihottomo shohor.',
        'bengalce': 'ইস্তাম্বুল তুরস্কের বৃহত্তম শহর।',
        'id': 54,
        'ing_okunus': 'İstanbul iz dı larcıst siti in Törki.',
        'ingilizce': 'Istanbul is the largest city in Turkey.',
        'kategori': 'Yön & Konum',
        'ornek_ar': 'إِسْطَنْبُولُ هِيَ أَكْبَرُ مَدِينَةٍ فِي تُرْكِيَا. (İstanbul hiye ekberu '
                    'medînetin fî Türkiyâ.)',
        'ornek_bn': 'ইস্তাম্বুল তুরস্কের বৃহত্তম শহর। (Istambul Turosker brihottomo shohor.)',
        'ornek_en': 'Istanbul is the largest city in Turkey.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': "İstanbul Türkiye'nin en büyük şehridir."},
    {   'ara_okunus': "El-kırâetü, el-kitâbetü ve't-tefkîru",
        'arapca': 'الْقِرَاءَةُ، الْكِتَابَةُ وَالتَّفْكِيرُ',
        'ben_okunus': 'Pora, lekha ebong chinta kora',
        'bengalce': 'পড়া, লেখা এবং চিন্তা করা',
        'id': 55,
        'ing_okunus': 'Tu rid, tu rayt end tu tink',
        'ingilizce': 'To read, to write and to think',
        'kategori': 'Temel Fiiller',
        'ornek_ar': 'الْقِرَاءَةُ، الْكِتَابَةُ وَالتَّفْكِيرُ (El-kırâetü, el-kitâbetü '
                    "ve't-tefkîru)",
        'ornek_bn': 'পড়া, লেখা এবং চিন্তা করা (Pora, lekha ebong chinta kora)',
        'ornek_en': 'To read, to write and to think',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Okumak, yazmak ve düşünmek'},
    {   'ara_okunus': 'Ezraku dâkinun, ezraku ve ebyadu',
        'arapca': 'أَزْرَقُ دَاكِنٌ، أَزْرَقُ وَأَبْيَضُ',
        'ben_okunus': 'Garho nebhi, nil ebong shada',
        'bengalce': 'গাঢ় নেভি, নীল এবং সাদা',
        'id': 56,
        'ing_okunus': 'Dark neyvi, blu end vayt',
        'ingilizce': 'Dark navy, blue and white',
        'kategori': 'Renkler & Sıfatlar',
        'ornek_ar': 'أَزْرَقُ دَاكِنٌ، أَزْرَقُ وَأَبْيَضُ (Ezraku dâkinun, ezraku ve ebyadu)',
        'ornek_bn': 'গাঢ় নেভি, নীল এবং সাদা (Garho nebhi, nil ebong shada)',
        'ornek_en': 'Dark navy, blue and white',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Koyu lacivert, mavi ve beyaz'},
    {   'ara_okunus': 'Eyne teîşu?',
        'arapca': 'أَيْنَ تَعِيشُ؟',
        'ben_okunus': 'Apni kothay thaken?',
        'bengalce': 'আপনি কোথায় থাকেন?',
        'id': 57,
        'ing_okunus': 'Ver du yu liv?',
        'ingilizce': 'Where do you live?',
        'kategori': 'Soru Kalıpları',
        'ornek_ar': 'أَيْنَ تَعِيشُ؟ (Eyne teîşu?)',
        'ornek_bn': 'আপনি কোথায় থাকেন? (Apni kothay thaken?)',
        'ornek_en': 'Where do you live?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Nerede yaşıyorsun?'},
    {   'ara_okunus': 'Kem umruke?',
        'arapca': 'كَمْ عُمْرُكَ؟',
        'ben_okunus': 'Apnar boyosh koto?',
        'bengalce': 'আপনার বয়স কত?',
        'id': 58,
        'ing_okunus': 'Hav old ar yu?',
        'ingilizce': 'How old are you?',
        'kategori': 'Soru Kalıpları',
        'ornek_ar': 'كَمْ عُمْرُكَ؟ (Kem umruke?)',
        'ornek_bn': 'আপনার বয়স কত? (Apnar boyosh koto?)',
        'ornek_en': 'How old are you?',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Kaç yaşındasın?'},
    {   'ara_okunus': "Şâşetü'l-hâtifi ve'l-hâsûbi",
        'arapca': 'شَاشَةُ الْهَاتِفِ وَالْحَاسُوبِ',
        'ben_okunus': 'Fon ebong kompiutarer porda',
        'bengalce': 'ফোন এবং কম্পিউটারের পর্দা',
        'id': 59,
        'ing_okunus': 'Fon end kompyutır skrin',
        'ingilizce': 'Phone and computer screen',
        'kategori': 'Teknoloji',
        'ornek_ar': "شَاشَةُ الْهَاتِفِ وَالْحَاسُوبِ (Şâşetü'l-hâtifi ve'l-hâsûbi)",
        'ornek_bn': 'ফোন এবং কম্পিউটারের পর্দা (Fon ebong kompiutarer porda)',
        'ornek_en': 'Phone and computer screen',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Telefon ve bilgisayar ekranı'},
    {   'ara_okunus': "Afven, ale'r-rahbi ve's-seati.",
        'arapca': 'عَفْوًا، عَلَى الرَّحْبِ وَالسَّعَةِ.',
        'ben_okunus': 'Dukkhito, apnake sbagotom.',
        'bengalce': 'দুঃখিত, আপনাকে স্বাগতম।',
        'id': 60,
        'ing_okunus': 'Ekskyuz mi, yu ar velkım.',
        'ingilizce': 'Excuse me, you are welcome.',
        'kategori': 'Nezaket',
        'ornek_ar': "عَفْوًا، عَلَى الرَّحْبِ وَالسَّعَةِ. (Afven, ale'r-rahbi ve's-seati.)",
        'ornek_bn': 'দুঃখিত, আপনাকে স্বাগতম। (Dukkhito, apnake sbagotom.)',
        'ornek_en': 'Excuse me, you are welcome.',
        'seviye': 'A1 (Başlangıç)',
        'turkce': 'Özür dilerim, rica ederim.'}]

_CEVIRI_ONBELLEK = {}  # (src, dest, metin) -> (ts, ceviri)

_DIL_AD_KOD_HARITASI = {
    "türkçe": "tr", "turkce": "tr", "türkçeye": "tr", "turkceye": "tr",
    "ingilizce": "en", "ingilizceye": "en", "english": "en",
    "arapça": "ar", "arapca": "ar", "arapçaya": "ar", "arapcaya": "ar",
    "bengalce": "bn", "bengalceye": "bn",
    "azerbaycanca": "az", "azerbaycancaya": "az", "azerice": "az", "azericeye": "az",
    "almanca": "de", "almancaya": "de", "german": "de",
    "fransızca": "fr", "fransizca": "fr", "fransızcaya": "fr", "fransizcaya": "fr",
    "ispanyolca": "es", "ispanyolcaya": "es", "spanish": "es",
    "italyanca": "it", "italyancaya": "it", "italian": "it",
    "rusça": "ru", "rusca": "ru", "rusçaya": "ru", "ruscaya": "ru",
    "japonca": "ja", "japoncaya": "ja",
    "korece": "ko", "koreceye": "ko",
    "çince": "zh-cn", "cince": "zh-cn", "çinceye": "zh-cn", "cinceye": "zh-cn",
    "farsça": "fa", "farsca": "fa", "farsçaya": "fa", "farscaya": "fa",
    "urduca": "ur", "urducaya": "ur",
    "felemenkçe": "nl", "felemenkce": "nl", "felemenkçeye": "nl", "hollandaca": "nl", "hollandacaya": "nl",
    "portekizce": "pt", "portekizceye": "pt",
    "lehçe": "pl", "lehce": "pl", "lehçeye": "pl", "polonyaca": "pl",
    "isveççe": "sv", "isvecce": "sv", "isveççeye": "sv",
    "yunanca": "el", "yunancaya": "el",
    "çekçe": "cs", "cekce": "cs", "çekçeye": "cs",
    "rumence": "ro", "rumenceye": "ro",
    "ukraynaca": "uk", "ukraynacaya": "uk",
    "hintçe": "hi", "hintce": "hi", "hintçeye": "hi",
    "endonezce": "id", "endonezceye": "id",
    "malayca": "ms", "malaycaya": "ms",
    "tayca": "th", "taycaya": "th",
    "vietnamca": "vi", "vietnamcaya": "vi",
}

_DIL_KOD_AD_HARITASI = {
    "tr": "Türkçe", "en": "İngilizce", "ar": "Arapça", "bn": "Bengalce",
    "az": "Azerbaycanca", "de": "Almanca", "fr": "Fransızca", "es": "İspanyolca",
    "it": "İtalyanca", "ru": "Rusça", "ja": "Japonca", "ko": "Korece",
    "zh-cn": "Çince", "zh-CN": "Çince", "fa": "Farsça", "ur": "Urduca",
    "nl": "Felemenkçe", "pt": "Portekizce", "pl": "Lehçe", "sv": "İsveççe",
    "el": "Yunanca", "cs": "Çekçe", "ro": "Rumence", "uk": "Ukraynaca",
    "hi": "Hintçe", "id": "Endonezce", "ms": "Malayca", "th": "Tayca", "vi": "Vietnamca",
}


def _kaynak_dil_tahmin_et(metin: str, dest: str) -> str:
    """MyMemory gibi 'auto' desteklemeyen yedek API'ler için alfabe tabanlı kaynak dil tahmini yapar."""
    if re.search(r"[؀-ۿ]", metin):
        return "ar"
    if re.search(r"[Ѐ-ӿ]", metin):
        return "ru"
    if re.search(r"[ঀ-৿]", metin):
        return "bn"
    if re.search(r"[぀-ヿ]", metin):
        return "ja"
    if re.search(r"[가-힯]", metin):
        return "ko"
    if re.search(r"[一-鿿]", metin):
        return "zh-CN"
    if any(c in metin for c in "çğıöşüÇĞİÖŞÜ"):
        return "tr"
    return "en" if dest == "tr" else "tr"


def guvenli_cevir(
    metin: str,
    src: str = "auto",
    dest: str = "tr",
    gtx_url_ozel: str = None,
    mymemory_url_ozel: str = None,
) -> str:
    """
    v10.0 Bulut & Mobil Uyumlu 3 Katmanlı Ücretsiz Çeviri Motoru (ek paket gerektirmez!):
      1. Google Translate Web HTTP (client=gtx) — çok hızlı, 100+ dil
      2. MyMemory Open Translation API — ücretsiz açık yedek
      3. Yerel googletrans (yüklüyse)
    """
    temiz = str(metin or "").strip()
    if not temiz:
        return ""
    if src == dest and src != "auto":
        return temiz

    anahtar = (src, dest, temiz[:500])
    simdi = time.time()
    if anahtar in _CEVIRI_ONBELLEK and (simdi - _CEVIRI_ONBELLEK[anahtar][0]) < 300.0:
        return _CEVIRI_ONBELLEK[anahtar][1]

    # 1. Google Translate Public Web Endpoint (Streamlit Cloud & Mobil'de %100 çalışır!)
    try:
        q = urllib.parse.quote(temiz[:1800])
        _tl_gtx = "zh-CN" if dest.lower() == "zh-cn" else dest
        url = gtx_url_ozel or f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={_tl_gtx}&dt=t&q={q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            veri = json.loads(resp.read().decode("utf-8"))
        if isinstance(veri, list) and veri and isinstance(veri[0], list):
            parcalar = [str(p[0]) for p in veri[0] if isinstance(p, list) and p and p[0]]
            sonuc_metin = "".join(parcalar).strip()
            if sonuc_metin:
                if len(_CEVIRI_ONBELLEK) > 128:
                    _CEVIRI_ONBELLEK.clear()
                _CEVIRI_ONBELLEK[anahtar] = (simdi, sonuc_metin)
                return sonuc_metin
    except Exception:
        pass

    # 2. MyMemory Open Translation API (Yedek)
    try:
        src_mm = src if src != "auto" else _kaynak_dil_tahmin_et(temiz, dest)
        q = urllib.parse.quote(temiz[:500])
        url_mm = mymemory_url_ozel or f"https://api.mymemory.translated.net/get?q={q}&langpair={src_mm}|{dest}"
        req_mm = urllib.request.Request(url_mm, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"})
        with urllib.request.urlopen(req_mm, timeout=5.0) as resp:
            veri_mm = json.loads(resp.read().decode("utf-8"))
        cev = (veri_mm.get("responseData", {}) or {}).get("translatedText", "").strip()
        if cev and "INVALID LANGUAGE" not in cev.upper():
            _CEVIRI_ONBELLEK[anahtar] = (simdi, cev)
            return cev
    except Exception:
        pass

    # 3. Yüklüyse googletrans nesnesi
    if _translator_nesnesi is not None:
        try:
            sonuc = _translator_nesnesi.translate(temiz, src=src, dest=dest)
            if inspect.iscoroutine(sonuc):
                sonuc = asyncio.run(sonuc)
            if hasattr(sonuc, "text") and sonuc.text:
                return sonuc.text.strip()
        except Exception:
            pass

    return temiz


def sohbet_cevirisi_yap(kullanici_girdisi: str, gtx_url_ozel: str = None, mymemory_url_ozel: str = None) -> dict:
    """
    Sohbet içinden doğrudan çeviri yapar (dışarıda telefondan kullanım için):
      • 'İngilizceye çevir: Merhaba, metro nerede?'
      • 'Arapçaya çevir: Günaydın'
      • 'çevir: How much is this?'
    """
    ham = str(kullanici_girdisi or "").strip()
    hedef_kod = None
    hedef_ad = "İngilizce"
    metin = ham

    # 1. Hedef dil adı belirtilmiş mi?
    for d_ad, d_kod in _DIL_AD_KOD_HARITASI.items():
        if re.search(rf"\b{re.escape(d_ad)}\b", ham, flags=re.IGNORECASE):
            hedef_kod = d_kod
            hedef_ad = _DIL_KOD_AD_HARITASI.get(d_kod, d_ad.capitalize())
            break

    # 2. Çevrilecek metni ayıkla
    if ":" in ham:
        metin = ham.split(":", 1)[1].strip()
    else:
        metin = re.sub(
            r"\b(" + "|".join(re.escape(k) for k in sorted(_DIL_AD_KOD_HARITASI.keys(), key=len, reverse=True)) + r"|çevirir\s*misin|cevirir\s*misin|çevir|cevir|translate|tercüme\s*et|tercume\s*et|nedir|ne\s+demek)\b",
            " ",
            ham,
            flags=re.IGNORECASE,
        )
        metin = re.sub(r"\s+", " ", metin).strip("?!.,;:\"' ")

    if not metin:
        return {"basarili": False}

    # Hedef dil verilmediyse: metinde Türkçe harf/kelime varsa EN'ye, yoksa TR'ye çevir
    if not hedef_kod:
        tr_isaret = any(c in metin for c in "çğıöşüÇĞİÖŞÜ") or bool(re.search(r"\b(merhaba|nasılsın|nerede|kaç|teşekkür|günaydın|iyi|ben|sen)\b", metin.lower()))
        hedef_kod = "en" if tr_isaret else "tr"
        hedef_ad = "İngilizce" if hedef_kod == "en" else "Türkçe"

    cevrilen = guvenli_cevir(metin, src="auto", dest=hedef_kod, gtx_url_ozel=gtx_url_ozel, mymemory_url_ozel=mymemory_url_ozel)
    return {
        "basarili": True,
        "kaynak_metin": metin,
        "ceviri": cevrilen,
        "hedef_kod": hedef_kod,
        "hedef_ad": hedef_ad,
        "metin": (
            f"### 🌐 Canlı Çeviri ({hedef_ad})\n"
            f"- **📝 Orijinal:** {metin}\n"
            f"- **✨ Çeviri:** **{cevrilen}**"
        ),
    }

def ses_metnini_dogallastir(metin: str, maks_karakter: int = 8000) -> str:
    """
    Uzun metinleri (yemek tarifleri, biyografiler, hava durumu) seslendirmeye hazırlar:
    - Markdown linklerini ([Başlık](https://...)) sadece 'Başlık' yapar, ham URL'leri siler.
    - 750 karakter kesilmesini kaldırır (4000 karaktere kadar tam okur) ve asla cümle ortasında kesmez!
    """
    yazi = str(metin)
    # Markdown linkleri: [Başlık](url) -> Başlık
    yazi = re.sub(r"\[([^\]]+)\]\(https?://[^\)]+\)", r"\1", yazi)
    # Kalan ham URL'leri sil
    yazi = re.sub(r"https?://\S+", "", yazi)
    yazi = re.sub(r"<[^>]+>", " ", yazi)
    yazi = yazi.replace("×", " çarpı ").replace("÷", " bölü ").replace("=", " eşittir ")
    yazi = yazi.replace("√", " karekök ").replace("+", " artı ").replace("%", " yüzde ").replace("°C", " derece")
    yazi = re.sub(r"[#*`_•|>]", " ", yazi)
    # Emojileri temizle
    yazi = re.sub(r"[\U00010000-\U0010ffff]", "", yazi)
    yazi = re.sub(r"[⚡🚀📜➕➖✖️➗🔺📐🥧🤖🔌🚁🖨️⚙️🇹🇷🏰🪐💧🧬🕌✨🤲💪😄🛠️⚽🌍🧑💻🕒🏷️📅🔢🧩❗💯ℹ️⚠️✅🎉❌🔬🍎⚗️📖☀️🌤️⛅☁️🌧️⛈️❄️💨🍲🛒👨‍🍳🔥💡⏱️👥]", "", yazi)
    yazi = re.sub(r"\s+", " ", yazi).strip()

    if len(yazi) > maks_karakter:
        kesik = yazi[:maks_karakter]
        son_nokta = max(kesik.rfind("."), kesik.rfind("!"), kesik.rfind("?"))
        yazi = kesik[:son_nokta + 1] if son_nokta > 200 else kesik
    return yazi.strip()


def _metni_ses_parcalarina_bol(metin: str, parca_boyutu: int = 900) -> list:
    """Uzun metni cümle bütünlüğünü bozmadan seslendirilecek parçalara böler."""
    if len(metin) <= parca_boyutu:
        return [metin]
    cumleler = re.split(r"(?<=[.!?])\s+", metin)
    parcalar = []
    aktif = ""
    for c in cumleler:
        if len(aktif) + len(c) + 1 <= parca_boyutu:
            aktif = f"{aktif} {c}".strip()
        else:
            if aktif:
                parcalar.append(aktif)
            aktif = c
    if aktif:
        parcalar.append(aktif)
    return parcalar or [metin]


async def _edge_ses_olustur(metin: str, ses_adi: str, dosya_adi: str):
    parcalar = _metni_ses_parcalarina_bol(metin, parca_boyutu=900)
    tum_baytlar = bytearray()
    for p in parcalar:
        iletisim = edge_tts.Communicate(p, ses_adi, rate="+4%")
        async for chunk in iletisim.stream():
            if chunk["type"] == "audio":
                tum_baytlar.extend(chunk["data"])
    with open(dosya_adi, "wb") as f_ses:
        f_ses.write(tum_baytlar)


def sesli_soyle(metin: str, dil: str = "tr", rerun_sonrasi: bool = False):
    if st.session_state.get("sessiz_mod", False) or not st.session_state.get("ses_aktif", True):
        return
    try:
        temiz_metin = ses_metnini_dogallastir(metin, maks_karakter=8000)
        if not temiz_metin:
            return

        dosya_adi = f"gecici_ses_{int(time.time() * 1000)}.mp3"
        uretim_basarili = False

        if EDGE_TTS_MEVCUT:
            try:
                cinsiyet = st.session_state.get("ses_cinsiyet", "Erkek")
                if dil == "tr":
                    ses_adi = "tr-TR-AhmetNeural" if cinsiyet == "Erkek" else "tr-TR-EmelNeural"
                else:
                    ses_adi = EDGE_SESLER.get(dil, "tr-TR-AhmetNeural") if cinsiyet == "Erkek" else EDGE_KADIN_SESLER.get(dil, "tr-TR-EmelNeural")
                try:
                    asyncio.get_running_loop()
                    import concurrent.futures as _cf
                    with _cf.ThreadPoolExecutor(max_workers=1) as _ex:
                        _ex.submit(asyncio.run, _edge_ses_olustur(temiz_metin, ses_adi, dosya_adi)).result(timeout=20)
                except RuntimeError:
                    asyncio.run(_edge_ses_olustur(temiz_metin, ses_adi, dosya_adi))
                uretim_basarili = os.path.exists(dosya_adi) and os.path.getsize(dosya_adi) > 0
            except Exception:
                uretim_basarili = False

        if not uretim_basarili and GTTS_MEVCUT and gTTS is not None:
            gtts_dil = GTTS_DIL_ESLESME.get(dil, dil)
            parcalar = _metni_ses_parcalarina_bol(temiz_metin, parca_boyutu=800)
            tum_bayt = bytearray()
            for p in parcalar:
                buf = io.BytesIO()
                tts = gTTS(text=p, lang=gtts_dil, slow=False)
                tts.write_to_fp(buf)
                tum_bayt.extend(buf.getvalue())
            with open(dosya_adi, "wb") as f_out:
                f_out.write(tum_bayt)
            uretim_basarili = os.path.exists(dosya_adi) and os.path.getsize(dosya_adi) > 0

        if not uretim_basarili:
            return

        with open(dosya_adi, "rb") as f:
            ses_bayt = f.read()

        if rerun_sonrasi:
            st.session_state.son_ses_bayt = ses_bayt
        else:
            st.audio(ses_bayt, format="audio/mp3", autoplay=True)

        if PYGAME_MEVCUT and st.session_state.get("pygame_aktif", False):
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                pygame.mixer.music.load(dosya_adi)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
            except Exception:
                pass

    except Exception as e:
        st.toast(f"Ses motoru uyarısı: {e}", icon="⚠️")
    finally:
        try:
            if "dosya_adi" in locals() and dosya_adi and os.path.exists(dosya_adi):
                os.remove(dosya_adi)
        except Exception:
            pass


# ==============================================================================
# 5. ÇEKİRDEK YAPAY ZEKA YANIT MOTORU
# ==============================================================================


def mikrofon_sesini_metne_cevir(ses_bayt: bytes, dil: str = "tr-TR"):
    """Mikrofondan kaydedilen WAV ses verisini metne çevirir."""
    if not SPEECH_RECOGNITION_MEVCUT or sr is None:
        return None, "Ses tanıma için PyCharm terminalinde `pip install SpeechRecognition` komutunu bir kez çalıştırabilirsin Ahmet."
    try:
        taniyici = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(ses_bayt)) as kaynak:
            ses_verisi = taniyici.record(kaynak)
        metin = taniyici.recognize_google(ses_verisi, language=dil)
        return metin, None
    except Exception as e:
        return None, f"Ses net duyulamadı veya dönüştürülemedi ({e}). Lütfen mikrofona biraz daha yakın konuşarak tekrar dene."





def dil_ve_cevirmeli_kart_studyosu_goster():
    st.subheader("🌐 A1 & A2 3D Çevirmeli Dil Kartları (İngilizce 🇬🇧 • Arapça 🇸🇦 • Bengalce 🇧🇩) & 28 Dilli Çeviri")
    tab_kart_calis, tab_interaktif_test, tab_ceviri = st.tabs([
        "🃏 3D Çevirmeli Kartlar (60 Kart: İngilizce - Arapça - Bengalce)",
        "🎯 Kart Üzerinden İnteraktif Dil Testi",
        "🔄 28 Dilli Akıllı Çeviri & Seslendirme",
    ])

    with tab_kart_calis:
        fk1, fk2, fk3, fk4 = st.columns([1.2, 1.2, 1.2, 1.0])
        with fk1:
            secili_seviye = st.selectbox("Seviye Seç:", ["Tümü (A1 + A2)", "A1 (Başlangıç)", "A2 (Temel Orta)"])
        with fk2:
            on_yuz_dili = st.selectbox("Kartın Ön Yüzünde Hangi Dil Olsun?", ["🇬🇧 İngilizce", "🇸🇦 Arapça", "🇧🇩 Bengalce", "🇹🇷 Türkçe (Tahmin Et)"])
        with fk3:
            gorunum_modu = st.selectbox("Kart Görünümü:", ["🃏 Tek Büyük Çevirmeli Kart", "🎛️ Çoklu Çevirmeli Kart Masası (6'lı)"])
        with fk4:
            st.metric("Öğrenilen Kart", f"{len(st.session_state.ogrenilen_kart_idleri)} / {len(A1_A2_DIL_PRATIK_KARTLARI)}", "A1 & A2")

        filtrelenmis_kartlar = [
            k for k in A1_A2_DIL_PRATIK_KARTLARI
            if secili_seviye == "Tümü (A1 + A2)" or k["seviye"] == secili_seviye
        ]
        toplam_k = len(filtrelenmis_kartlar)
        aktif_idx = st.session_state.aktif_flip_indeks % toplam_k
        aktif_kart = filtrelenmis_kartlar[aktif_idx]

        if gorunum_modu == "🃏 Tek Büyük Çevirmeli Kart":
            nb1, nb2, nb3, nb4, nb5 = st.columns(5)
            if nb1.button("⬅️ Önceki Kart", use_container_width=True):
                st.session_state.aktif_flip_indeks = (aktif_idx - 1) % toplam_k
                st.session_state.kart_ters_mi = False
                st.rerun()
            if nb2.button("🔄 Kartı Çevir", use_container_width=True):
                st.session_state.kart_ters_mi = not st.session_state.kart_ters_mi
                st.rerun()
            if nb3.button("🎲 Rastgele Kart", use_container_width=True):
                st.session_state.aktif_flip_indeks = random.randint(0, toplam_k - 1)
                st.session_state.kart_ters_mi = False
                st.rerun()
            if nb4.button("➡️ Sonraki Kart", use_container_width=True):
                st.session_state.aktif_flip_indeks = (aktif_idx + 1) % toplam_k
                st.session_state.kart_ters_mi = False
                st.rerun()
            if nb5.button("✅ Öğrendim!", use_container_width=True):
                if aktif_kart["id"] not in st.session_state.ogrenilen_kart_idleri:
                    st.session_state.ogrenilen_kart_idleri.append(aktif_kart["id"])
                st.toast(f"Kart #{aktif_kart['id']} öğrenilenlere eklendi! 🎉", icon="✅")
                st.rerun()

            st.markdown(
                cevirmeli_dil_karti_olustur(
                    aktif_kart,
                    on_yuz_dili=on_yuz_dili,
                    ters_cevir=st.session_state.kart_ters_mi,
                    kart_key="tek_sahne",
                ),
                unsafe_allow_html=True,
            )

            dk1, dk2, dk3 = st.columns(3)
            if dk1.button("🔊 İngilizce Seslendir", use_container_width=True):
                sesli_soyle(aktif_kart["ingilizce"], dil="en")
            if dk2.button("🔊 Arapça Seslendir", use_container_width=True):
                sesli_soyle(aktif_kart["arapca"], dil="ar")
            if dk3.button("🔊 Bengalce Seslendir", use_container_width=True):
                sesli_soyle(aktif_kart["bengalce"], dil="bn")
        else:
            st.caption("👆 Masadaki herhangi bir kartın üzerine dokunduğunda o kart 3 boyutlu olarak döner!")
            g_col1, g_col2 = st.columns(2, gap="medium")
            for i_k, k_item in enumerate(filtrelenmis_kartlar[:6]):
                with (g_col1 if i_k % 2 == 0 else g_col2):
                    st.markdown(
                        cevirmeli_dil_karti_olustur(
                            k_item,
                            on_yuz_dili=on_yuz_dili,
                            ters_cevir=False,
                            kart_key=f"masa_{i_k}",
                        ),
                        unsafe_allow_html=True,
                    )

    with tab_interaktif_test:
        st.markdown("#### 🎯 Kart Üzerinden Kendini Dene (A1 & A2 İngilizce • Arapça • Bengalce)")
        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            pratik_dil = st.selectbox("Pratik Dili Seç:", ["🇬🇧 İngilizce", "🇸🇦 Arapça", "🇧🇩 Bengalce"])
        with t_col2:
            pratik_seviye = st.selectbox("Pratik Seviyesi:", ["A1 (Başlangıç)", "A2 (Temel Orta)", "Karışık (A1 + A2)"])
        with t_col3:
            st.metric("Dil Pratiği Puanın", f"{st.session_state.dil_quiz_puan} Puan", "A1/A2 Aktif")

        havuz_kartlar = [
            k for k in A1_A2_DIL_PRATIK_KARTLARI
            if pratik_seviye == "Karışık (A1 + A2)" or k["seviye"] == pratik_seviye
        ]
        if st.button("🎲 Bana Yeni Çalışma Kartı Ver", use_container_width=True):
            st.session_state.dil_quiz_indeks = random.randint(0, len(havuz_kartlar) - 1)

        sec_idx = st.session_state.dil_quiz_indeks % len(havuz_kartlar)
        soru_kart = havuz_kartlar[sec_idx]

        st.markdown(
            cevirmeli_dil_karti_olustur(
                soru_kart,
                on_yuz_dili=pratik_dil,
                ters_cevir=False,
                kart_key="test_sahne",
            ),
            unsafe_allow_html=True,
        )

        secenekler = [soru_kart["turkce"]]
        digerleri = [k["turkce"] for k in A1_A2_DIL_PRATIK_KARTLARI if k["id"] != soru_kart["id"]]
        _yerel_rng = random.Random(soru_kart["id"])
        secenekler.extend(_yerel_rng.sample(digerleri, 3))
        _yerel_rng.shuffle(secenekler)

        secilen_cevap = st.radio("Bu karttaki ifadenin Türkçe anlamı nedir?", secenekler, key=f"dil_secim_{soru_kart['id']}_{pratik_dil}")
        if st.button("✅ Cevabımı Kontrol Et", key="dil_cevap_kontrol", use_container_width=True):
            if secilen_cevap == soru_kart["turkce"]:
                st.session_state.dil_quiz_puan += 10
                st.success(f"🎉 Tebrikler Ahmet! Doğru cevap: **{soru_kart['turkce']}** (+10 Puan)")
            else:
                st.error(f"❌ Doğru anlamı: **{soru_kart['turkce']}**")

    with tab_ceviri:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            kaynak = st.selectbox("Kaynak Dil:", options=["auto"] + list(DESTEKLENEN_DILLER.keys()), format_func=lambda x: "✨ Otomatik Algıla" if x == "auto" else DESTEKLENEN_DILLER[x])
            metin_giris = st.text_area("Çevrilecek Metin:", height=190, placeholder="Çevirmek istediğin metni buraya yaz...")
        with c2:
            hedef = st.selectbox("Hedef Dil:", options=list(DESTEKLENEN_DILLER.keys()), index=1, format_func=lambda x: DESTEKLENEN_DILLER[x])
            cikti = st.empty()
            cikti.text_area("Çeviri Sonucu:", value="", height=190, key="ceviri_bos")

        b1, b2 = st.columns(2)
        btn_cevir = b1.button("🔄 Sadece Çevir", use_container_width=True)
        btn_sesli = b2.button("🔊 Çevir ve Doğal Sesle Oku", use_container_width=True)
        if btn_cevir or btn_sesli:
            if metin_giris.strip():
                try:
                    cevrilen = guvenli_cevir(metin_giris, src=kaynak, dest=hedef)
                    cikti.text_area("Çeviri Sonucu:", value=cevrilen, height=190, key="ceviri_dolu")
                    if btn_sesli:
                        sesli_soyle(cevrilen, dil=hedef)
                except Exception as e:
                    st.error(f"Çeviri hatası: {e}")
            else:
                st.warning("Lütfen çevirmek için bir metin girin.")
