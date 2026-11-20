# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO v4.0 — MODÜL 1: KOYU LACİVERT TEMA MOTORU, 3D ÇEVİRMELİ KART (FLIP CARD)
CSS TASARIMI, 150 ÇOK DİLLİ KART VE 240 SİSTEM KISAYOLU (modul_1_arayuz_ve_tema.py)
==============================================================================
"""
import streamlit as st

UYGULAMA_ADI = "AREX AI Studio"
UYGULAMA_SURUMU = "v4.0 Enterprise Modular"
GELISTIRICI_ADI = "Ahmet"
JSON_DOSYA_ADI = "komutlar.json"
SOHBET_DOSYA_ADI = "sohbet_gecmisi.json"
NOTLAR_DOSYA_ADI = "ahmet_notlar.json"
DERS_NOTLARI_DOSYASI = "ahmet_ders_notlari.json"
SORU_TAKIP_DOSYASI = "ahmet_soru_takip.json"

TEMA_PALETLERI = {
    "Derin Lacivert (Klasik Ar)": {
        "bg_primary": "#0b1120",
        "bg_secondary": "#080d1a",
        "card_bg": "#111827",
        "elevated_bg": "#162032",
        "accent_neon": "#38bdf8",
        "accent_blue": "#0ea5e9",
        "accent_purple": "#6366f1",
        "accent_rose": "#60a5fa",
        "border_soft": "rgba(56, 189, 248, 0.22)",
        "text_main": "#f1f5f9",
        "text_sub": "#94a3b8",
        "aciklama": "Göz yormayan gece laciverti zemin ve buz mavisi vurgular.",
    },
    "Kraliyet Moru & Altın": {
        "bg_primary": "#110a1f",
        "bg_secondary": "#0b0614",
        "card_bg": "#1b1130",
        "elevated_bg": "#241740",
        "accent_neon": "#f59e0b",
        "accent_blue": "#c084fc",
        "accent_purple": "#9333ea",
        "accent_rose": "#fbbf24",
        "border_soft": "rgba(192, 132, 252, 0.26)",
        "text_main": "#faf5ff",
        "text_sub": "#c4b5fd",
        "aciklama": "Asil koyu mor yüzeyler ve sıcak altın vurgu çizgileri.",
    },
    "Zümrüt Matriks": {
        "bg_primary": "#061511",
        "bg_secondary": "#040e0b",
        "card_bg": "#0c221b",
        "elevated_bg": "#112f25",
        "accent_neon": "#10b981",
        "accent_blue": "#34d399",
        "accent_purple": "#059669",
        "accent_rose": "#6ee7b7",
        "border_soft": "rgba(16, 185, 129, 0.26)",
        "text_main": "#ecfdf5",
        "text_sub": "#86efac",
        "aciklama": "Sakin koyu zümrüt zemin ve mühendislik yeşili detaylar.",
    },
    "Kızıl Süpernova": {
        "bg_primary": "#17090d",
        "bg_secondary": "#100508",
        "card_bg": "#240f16",
        "elevated_bg": "#31151e",
        "accent_neon": "#fb7185",
        "accent_blue": "#f43f5e",
        "accent_purple": "#e11d48",
        "accent_rose": "#fda4af",
        "border_soft": "rgba(251, 113, 133, 0.26)",
        "text_main": "#fff1f2",
        "text_sub": "#fda4af",
        "aciklama": "Sıcak koyu bordo yüzeyler ve yumuşak mercan vurguları.",
    },
    "Okyanus Derinliği": {
        "bg_primary": "#04141c",
        "bg_secondary": "#020d12",
        "card_bg": "#08202c",
        "elevated_bg": "#0d2d3d",
        "accent_neon": "#2dd4bf",
        "accent_blue": "#06b6d4",
        "accent_purple": "#0284c7",
        "accent_rose": "#5eead4",
        "border_soft": "rgba(45, 212, 191, 0.26)",
        "text_main": "#f0fdfa",
        "text_sub": "#99f6e4",
        "aciklama": "Derin okyanus mavisi ve turkuaz cam efektli kartlar.",
    },
    "Saf Koyu Kontrast (OLED)": {
        "bg_primary": "#050507",
        "bg_secondary": "#000000",
        "card_bg": "#111216",
        "elevated_bg": "#1a1c23",
        "accent_neon": "#22d3ee",
        "accent_blue": "#60a5fa",
        "accent_purple": "#818cf8",
        "accent_rose": "#38bdf8",
        "border_soft": "rgba(148, 163, 184, 0.22)",
        "text_main": "#ffffff",
        "text_sub": "#a1a1aa",
        "aciklama": "OLED ekranlar için tam siyah arka plan ve yüksek netlik.",
    },
    "Siber Neon (Koyu Mavi)": {
        "bg_primary": "#070b19",
        "bg_secondary": "#040711",
        "card_bg": "#0f172a",
        "elevated_bg": "#172540",
        "accent_neon": "#00f5d4",
        "accent_blue": "#38bdf8",
        "accent_purple": "#818cf8",
        "accent_rose": "#f472b6",
        "border_soft": "rgba(0, 245, 212, 0.26)",
        "text_main": "#f8fafc",
        "text_sub": "#93c5fd",
        "aciklama": "Modern siber gece mavisi ve ferah mint-cyan vurgular.",
    },
}

DIL_EGITIM_KARTLARI = [   {   'bengalce': 'কৃত্রিম বুদ্ধিমত্তা (Kritrim buddhimotta)',
        'cince': '人工智能 (Réngōng zhìnéng)',
        'id': 1,
        'ingilizce': 'Artificial Intelligence (#1)',
        'kategori': 'Teknoloji',
        'ornek_cumle': 'Ahmet uses artificial intelligence in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Yapay Zeka'},
    {   'bengalce': 'স্বায়ত্তশাসিত ড্রোন (Sbayottoshasito drone)',
        'cince': '自主无人机 (Zìzhǔ wúrénjī)',
        'id': 2,
        'ingilizce': 'Autonomous Drone (#2)',
        'kategori': 'Havacılık',
        'ornek_cumle': 'Ahmet uses autonomous drone in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Otonom İnsansız Hava Aracı'},
    {   'bengalce': 'সফটওয়্যার ইঞ্জিনিয়ারিং (Software engineering)',
        'cince': '软件工程 (Ruǎnjiàn gōngchéng)',
        'id': 3,
        'ingilizce': 'Software Engineering (#3)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses software engineering in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Yazılım Mühendisliği'},
    {   'bengalce': 'মেশিন লার্নিং (Machine learning)',
        'cince': '机器学习 (Jīqì xuéxí)',
        'id': 4,
        'ingilizce': 'Machine Learning (#4)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses machine learning in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Makine Öğrenmesi'},
    {   'bengalce': 'নিউরাল নেটওয়ার্ক (Neural network)',
        'cince': '神经网络 (Shénjīng wǎngluò)',
        'id': 5,
        'ingilizce': 'Neural Network (#5)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses neural network in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Sinir Ağı'},
    {   'bengalce': 'কম্পিউটার ভিশন (Computer vision)',
        'cince': '计算机视觉 (Jìsuànjī shìjué)',
        'id': 6,
        'ingilizce': 'Computer Vision (#6)',
        'kategori': 'Görüntü İşleme',
        'ornek_cumle': 'Ahmet uses computer vision in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Bilgisayarlı Görü'},
    {   'bengalce': 'এম্বেডেড সিস্টেম (Embedded system)',
        'cince': '嵌入式系统 (Qiànrùshì xìtǒng)',
        'id': 7,
        'ingilizce': 'Embedded Systems (#7)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses embedded systems in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Gömülü Sistemler'},
    {   'bengalce': 'মাইক্রোকন্ট্রোলার (Microcontroller)',
        'cince': '微控制器 (Wēi kòngzhìqì)',
        'id': 8,
        'ingilizce': 'Microcontroller (#8)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses microcontroller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Mikrodenetleyici'},
    {   'bengalce': 'আল্ট্রাসনিক সেন্সর (Ultrasonic sensor)',
        'cince': '超声波传感器 (Chāoshēngbō chuángǎnqì)',
        'id': 9,
        'ingilizce': 'Ultrasonic Sensor (#9)',
        'kategori': 'Sensör',
        'ornek_cumle': 'Ahmet uses ultrasonic sensor in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Ultrasonik Sensör'},
    {   'bengalce': 'থ্রিডি প্রিন্টিং (3D printing)',
        'cince': '3D打印 (3D dǎyìn)',
        'id': 10,
        'ingilizce': 'Three Dimensional Printing (#10)',
        'kategori': 'Üretim',
        'ornek_cumle': 'Ahmet uses three dimensional printing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Üç Boyutlu Baskı'},
    {   'bengalce': 'বর্গমূল (Borgomul)',
        'cince': '平方根 (Píngfānggēn)',
        'id': 11,
        'ingilizce': 'Square Root (#11)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses square root in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Karekök'},
    {   'bengalce': 'মৌলিক সংখ্যা (Moulik songkha)',
        'cince': '质数 (Zhìshù)',
        'id': 12,
        'ingilizce': 'Prime Number (#12)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses prime number in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Asal Sayı'},
    {   'bengalce': 'রৈখিক সমীকরণ (Roikhik somikoron)',
        'cince': '线性方程 (Xiànxìng fāngchéng)',
        'id': 13,
        'ingilizce': 'Linear Equation (#13)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses linear equation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Doğrusal Denklem'},
    {   'bengalce': 'গরিষ্ঠ সাধারণ গুণনীয়ক (Goshagu)',
        'cince': '最大公约数 (Zuìdà gōngyuēshù)',
        'id': 14,
        'ingilizce': 'Greatest Common Divisor (#14)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses greatest common divisor in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'En Büyük Ortak Bölen (EBOB)'},
    {   'bengalce': 'লঘিষ্ঠ সাধারণ গুণিতক (Loshagu)',
        'cince': '最小公倍数 (Zuìxiǎo gōngbèishù)',
        'id': 15,
        'ingilizce': 'Least Common Multiple (#15)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses least common multiple in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'En Küçük Ortak Kat (EKOK)'},
    {   'bengalce': 'সূচক (Suchok)',
        'cince': '幂运算 (Mì yùnsuàn)',
        'id': 16,
        'ingilizce': 'Exponentiation (#16)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses exponentiation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Üs Alma / Üslü Sayılar'},
    {   'bengalce': 'পিথাগোরাসের উপপাদ্য (Pithagoraser upopaddo)',
        'cince': '勾股定理 (Gōugǔ dìnglǐ)',
        'id': 17,
        'ingilizce': 'Pythagorean Theorem (#17)',
        'kategori': 'Geometri',
        'ornek_cumle': 'Ahmet uses pythagorean theorem in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Pisagor Teoremi'},
    {   'bengalce': 'অধ্যবসায় এবং শৃঙ্খলা (Oddhobosay ebong srinkhola)',
        'cince': '毅力与纪律 (Yìlì yǔ jìlǜ)',
        'id': 18,
        'ingilizce': 'Perseverance and Discipline (#18)',
        'kategori': 'Kişisel Gelişim',
        'ornek_cumle': 'Ahmet uses perseverance and discipline in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Azim ve Disiplin'},
    {   'bengalce': 'বৈজ্ঞানিক গবেষণা (Boigganik gobeshona)',
        'cince': '科学研究 (Kēxué yánjiū)',
        'id': 19,
        'ingilizce': 'Scientific Research (#19)',
        'kategori': 'Bilim',
        'ornek_cumle': 'Ahmet uses scientific research in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bilimsel Araştırma'},
    {   'bengalce': 'অ্যালগরিদম অপ্টিমাইজেশন (Algorithm optimization)',
        'cince': '算法优化 (Suànfǎ yōuhuà)',
        'id': 20,
        'ingilizce': 'Algorithm Optimization (#20)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses algorithm optimization in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Algoritma Optimizasyonu'},
    {   'bengalce': 'ফ্লাইট কন্ট্রোলার (Flight controller)',
        'cince': '飞行控制器 (Fēixíng kòngzhìqì)',
        'id': 21,
        'ingilizce': 'Flight Controller (#21)',
        'kategori': 'İHA / Drone',
        'ornek_cumle': 'Ahmet uses flight controller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Uçuş Kontrol Kartı'},
    {   'bengalce': 'ব্যাটারি ম্যানেজমেন্ট (Battery management)',
        'cince': '电池管理 (Diànchí guǎnlǐ)',
        'id': 22,
        'ingilizce': 'Battery Management (#22)',
        'kategori': 'Elektronik',
        'ornek_cumle': 'Ahmet uses battery management in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Batarya Yönetimi'},
    {   'bengalce': 'সিগন্যাল প্রসেসিং (Signal processing)',
        'cince': '信号处理 (Xìnhào chǔlǐ)',
        'id': 23,
        'ingilizce': 'Signal Processing (#23)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses signal processing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Sinyal İşleme'},
    {   'bengalce': 'ডেটা স্ট্রাকচার (Data structure)',
        'cince': '数据结构 (Shùjù jiégòu)',
        'id': 24,
        'ingilizce': 'Data Structure (#24)',
        'kategori': 'Bilgisayar Bilimi',
        'ornek_cumle': 'Ahmet uses data structure in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Veri Yapısı'},
    {   'bengalce': 'অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং (OOP)',
        'cince': '面向对象编程 (Miànxiàng duìxiàng biānchéng)',
        'id': 25,
        'ingilizce': 'Object Oriented Programming (#25)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses object oriented programming in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Nesne Yönelimli Programlama'},
    {   'bengalce': 'সাইবার নিরাপত্তা (Cyber nirapotta)',
        'cince': '网络安全 (Wǎngluò ānquán)',
        'id': 26,
        'ingilizce': 'Cyber Security (#26)',
        'kategori': 'Güvenlik',
        'ornek_cumle': 'Ahmet uses cyber security in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Siber Güvenlik'},
    {   'bengalce': 'ক্লাউড কম্পিউটিং (Cloud computing)',
        'cince': '云计算 (Yún jìsuàn)',
        'id': 27,
        'ingilizce': 'Cloud Computing (#27)',
        'kategori': 'Sistem',
        'ornek_cumle': 'Ahmet uses cloud computing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bulut Bilişim'},
    {   'bengalce': 'ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)',
        'cince': '自然语言处理 (Zìrán yǔyán chǔlǐ)',
        'id': 28,
        'ingilizce': 'Natural Language Processing (#28)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses natural language processing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Doğal Dil İşleme'},
    {   'bengalce': 'রোবোটিক্স এবং অটোমেশন (Robotics)',
        'cince': '机器人与自动化 (Jīqìrén yǔ zìdònghuà)',
        'id': 29,
        'ingilizce': 'Robotics and Automation (#29)',
        'kategori': 'Robotik',
        'ornek_cumle': 'Ahmet uses robotics and automation in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Robotik ve Otomasyon'},
    {   'bengalce': 'অ্যারোডাইনামিক্স (Aerodynamics)',
        'cince': '空气动力学 (Kōngqì dònglìxué)',
        'id': 30,
        'ingilizce': 'Aerodynamics (#30)',
        'kategori': 'Fizik',
        'ornek_cumle': 'Ahmet uses aerodynamics in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Orta',
        'turkce': 'Aerodinamik'},
    {   'bengalce': 'কৃত্রিম বুদ্ধিমত্তা (Kritrim buddhimotta)',
        'cince': '人工智能 (Réngōng zhìnéng)',
        'id': 31,
        'ingilizce': 'Artificial Intelligence (#31)',
        'kategori': 'Teknoloji',
        'ornek_cumle': 'Ahmet uses artificial intelligence in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Yapay Zeka'},
    {   'bengalce': 'স্বায়ত্তশাসিত ড্রোন (Sbayottoshasito drone)',
        'cince': '自主无人机 (Zìzhǔ wúrénjī)',
        'id': 32,
        'ingilizce': 'Autonomous Drone (#32)',
        'kategori': 'Havacılık',
        'ornek_cumle': 'Ahmet uses autonomous drone in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Otonom İnsansız Hava Aracı'},
    {   'bengalce': 'সফটওয়্যার ইঞ্জিনিয়ারিং (Software engineering)',
        'cince': '软件工程 (Ruǎnjiàn gōngchéng)',
        'id': 33,
        'ingilizce': 'Software Engineering (#33)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses software engineering in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Yazılım Mühendisliği'},
    {   'bengalce': 'মেশিন লার্নিং (Machine learning)',
        'cince': '机器学习 (Jīqì xuéxí)',
        'id': 34,
        'ingilizce': 'Machine Learning (#34)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses machine learning in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Makine Öğrenmesi'},
    {   'bengalce': 'নিউরাল নেটওয়ার্ক (Neural network)',
        'cince': '神经网络 (Shénjīng wǎngluò)',
        'id': 35,
        'ingilizce': 'Neural Network (#35)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses neural network in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Sinir Ağı'},
    {   'bengalce': 'কম্পিউটার ভিশন (Computer vision)',
        'cince': '计算机视觉 (Jìsuànjī shìjué)',
        'id': 36,
        'ingilizce': 'Computer Vision (#36)',
        'kategori': 'Görüntü İşleme',
        'ornek_cumle': 'Ahmet uses computer vision in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Bilgisayarlı Görü'},
    {   'bengalce': 'এম্বেডেড সিস্টেম (Embedded system)',
        'cince': '嵌入式系统 (Qiànrùshì xìtǒng)',
        'id': 37,
        'ingilizce': 'Embedded Systems (#37)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses embedded systems in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Gömülü Sistemler'},
    {   'bengalce': 'মাইক্রোকন্ট্রোলার (Microcontroller)',
        'cince': '微控制器 (Wēi kòngzhìqì)',
        'id': 38,
        'ingilizce': 'Microcontroller (#38)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses microcontroller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Mikrodenetleyici'},
    {   'bengalce': 'আল্ট্রাসনিক সেন্সর (Ultrasonic sensor)',
        'cince': '超声波传感器 (Chāoshēngbō chuángǎnqì)',
        'id': 39,
        'ingilizce': 'Ultrasonic Sensor (#39)',
        'kategori': 'Sensör',
        'ornek_cumle': 'Ahmet uses ultrasonic sensor in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Ultrasonik Sensör'},
    {   'bengalce': 'থ্রিডি প্রিন্টিং (3D printing)',
        'cince': '3D打印 (3D dǎyìn)',
        'id': 40,
        'ingilizce': 'Three Dimensional Printing (#40)',
        'kategori': 'Üretim',
        'ornek_cumle': 'Ahmet uses three dimensional printing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Üç Boyutlu Baskı'},
    {   'bengalce': 'বর্গমূল (Borgomul)',
        'cince': '平方根 (Píngfānggēn)',
        'id': 41,
        'ingilizce': 'Square Root (#41)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses square root in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Temel',
        'turkce': 'Karekök'},
    {   'bengalce': 'মৌলিক সংখ্যা (Moulik songkha)',
        'cince': '质数 (Zhìshù)',
        'id': 42,
        'ingilizce': 'Prime Number (#42)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses prime number in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Orta',
        'turkce': 'Asal Sayı'},
    {   'bengalce': 'রৈখিক সমীকরণ (Roikhik somikoron)',
        'cince': '线性方程 (Xiànxìng fāngchéng)',
        'id': 43,
        'ingilizce': 'Linear Equation (#43)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses linear equation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Doğrusal Denklem'},
    {   'bengalce': 'গরিষ্ঠ সাধারণ গুণনীয়ক (Goshagu)',
        'cince': '最大公约数 (Zuìdà gōngyuēshù)',
        'id': 44,
        'ingilizce': 'Greatest Common Divisor (#44)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses greatest common divisor in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'En Büyük Ortak Bölen (EBOB)'},
    {   'bengalce': 'লঘিষ্ঠ সাধারণ গুণিতক (Loshagu)',
        'cince': '最小公倍数 (Zuìxiǎo gōngbèishù)',
        'id': 45,
        'ingilizce': 'Least Common Multiple (#45)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses least common multiple in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'En Küçük Ortak Kat (EKOK)'},
    {   'bengalce': 'সূচক (Suchok)',
        'cince': '幂运算 (Mì yùnsuàn)',
        'id': 46,
        'ingilizce': 'Exponentiation (#46)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses exponentiation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Üs Alma / Üslü Sayılar'},
    {   'bengalce': 'পিথাগোরাসের উপপাদ্য (Pithagoraser upopaddo)',
        'cince': '勾股定理 (Gōugǔ dìnglǐ)',
        'id': 47,
        'ingilizce': 'Pythagorean Theorem (#47)',
        'kategori': 'Geometri',
        'ornek_cumle': 'Ahmet uses pythagorean theorem in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Pisagor Teoremi'},
    {   'bengalce': 'অধ্যবসায় এবং শৃঙ্খলা (Oddhobosay ebong srinkhola)',
        'cince': '毅力与纪律 (Yìlì yǔ jìlǜ)',
        'id': 48,
        'ingilizce': 'Perseverance and Discipline (#48)',
        'kategori': 'Kişisel Gelişim',
        'ornek_cumle': 'Ahmet uses perseverance and discipline in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Azim ve Disiplin'},
    {   'bengalce': 'বৈজ্ঞানিক গবেষণা (Boigganik gobeshona)',
        'cince': '科学研究 (Kēxué yánjiū)',
        'id': 49,
        'ingilizce': 'Scientific Research (#49)',
        'kategori': 'Bilim',
        'ornek_cumle': 'Ahmet uses scientific research in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Bilimsel Araştırma'},
    {   'bengalce': 'অ্যালগরিদম অপ্টিমাইজেশন (Algorithm optimization)',
        'cince': '算法优化 (Suànfǎ yōuhuà)',
        'id': 50,
        'ingilizce': 'Algorithm Optimization (#50)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses algorithm optimization in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Algoritma Optimizasyonu'},
    {   'bengalce': 'ফ্লাইট কন্ট্রোলার (Flight controller)',
        'cince': '飞行控制器 (Fēixíng kòngzhìqì)',
        'id': 51,
        'ingilizce': 'Flight Controller (#51)',
        'kategori': 'İHA / Drone',
        'ornek_cumle': 'Ahmet uses flight controller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Uçuş Kontrol Kartı'},
    {   'bengalce': 'ব্যাটারি ম্যানেজমেন্ট (Battery management)',
        'cince': '电池管理 (Diànchí guǎnlǐ)',
        'id': 52,
        'ingilizce': 'Battery Management (#52)',
        'kategori': 'Elektronik',
        'ornek_cumle': 'Ahmet uses battery management in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Batarya Yönetimi'},
    {   'bengalce': 'সিগন্যাল প্রসেসিং (Signal processing)',
        'cince': '信号处理 (Xìnhào chǔlǐ)',
        'id': 53,
        'ingilizce': 'Signal Processing (#53)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses signal processing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Sinyal İşleme'},
    {   'bengalce': 'ডেটা স্ট্রাকচার (Data structure)',
        'cince': '数据结构 (Shùjù jiégòu)',
        'id': 54,
        'ingilizce': 'Data Structure (#54)',
        'kategori': 'Bilgisayar Bilimi',
        'ornek_cumle': 'Ahmet uses data structure in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Veri Yapısı'},
    {   'bengalce': 'অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং (OOP)',
        'cince': '面向对象编程 (Miànxiàng duìxiàng biānchéng)',
        'id': 55,
        'ingilizce': 'Object Oriented Programming (#55)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses object oriented programming in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Nesne Yönelimli Programlama'},
    {   'bengalce': 'সাইবার নিরাপত্তা (Cyber nirapotta)',
        'cince': '网络安全 (Wǎngluò ānquán)',
        'id': 56,
        'ingilizce': 'Cyber Security (#56)',
        'kategori': 'Güvenlik',
        'ornek_cumle': 'Ahmet uses cyber security in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Siber Güvenlik'},
    {   'bengalce': 'ক্লাউড কম্পিউটিং (Cloud computing)',
        'cince': '云计算 (Yún jìsuàn)',
        'id': 57,
        'ingilizce': 'Cloud Computing (#57)',
        'kategori': 'Sistem',
        'ornek_cumle': 'Ahmet uses cloud computing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Bulut Bilişim'},
    {   'bengalce': 'ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)',
        'cince': '自然语言处理 (Zìrán yǔyán chǔlǐ)',
        'id': 58,
        'ingilizce': 'Natural Language Processing (#58)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses natural language processing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Doğal Dil İşleme'},
    {   'bengalce': 'রোবোটিক্স এবং অটোমেশন (Robotics)',
        'cince': '机器人与自动化 (Jīqìrén yǔ zìdònghuà)',
        'id': 59,
        'ingilizce': 'Robotics and Automation (#59)',
        'kategori': 'Robotik',
        'ornek_cumle': 'Ahmet uses robotics and automation in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Robotik ve Otomasyon'},
    {   'bengalce': 'অ্যারোডাইনামিক্স (Aerodynamics)',
        'cince': '空气动力学 (Kōngqì dònglìxué)',
        'id': 60,
        'ingilizce': 'Aerodynamics (#60)',
        'kategori': 'Fizik',
        'ornek_cumle': 'Ahmet uses aerodynamics in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Aerodinamik'},
    {   'bengalce': 'কৃত্রিম বুদ্ধিমত্তা (Kritrim buddhimotta)',
        'cince': '人工智能 (Réngōng zhìnéng)',
        'id': 61,
        'ingilizce': 'Artificial Intelligence (#61)',
        'kategori': 'Teknoloji',
        'ornek_cumle': 'Ahmet uses artificial intelligence in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Yapay Zeka'},
    {   'bengalce': 'স্বায়ত্তশাসিত ড্রোন (Sbayottoshasito drone)',
        'cince': '自主无人机 (Zìzhǔ wúrénjī)',
        'id': 62,
        'ingilizce': 'Autonomous Drone (#62)',
        'kategori': 'Havacılık',
        'ornek_cumle': 'Ahmet uses autonomous drone in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Otonom İnsansız Hava Aracı'},
    {   'bengalce': 'সফটওয়্যার ইঞ্জিনিয়ারিং (Software engineering)',
        'cince': '软件工程 (Ruǎnjiàn gōngchéng)',
        'id': 63,
        'ingilizce': 'Software Engineering (#63)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses software engineering in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Yazılım Mühendisliği'},
    {   'bengalce': 'মেশিন লার্নিং (Machine learning)',
        'cince': '机器学习 (Jīqì xuéxí)',
        'id': 64,
        'ingilizce': 'Machine Learning (#64)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses machine learning in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Makine Öğrenmesi'},
    {   'bengalce': 'নিউরাল নেটওয়ার্ক (Neural network)',
        'cince': '神经网络 (Shénjīng wǎngluò)',
        'id': 65,
        'ingilizce': 'Neural Network (#65)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses neural network in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Sinir Ağı'},
    {   'bengalce': 'কম্পিউটার ভিশন (Computer vision)',
        'cince': '计算机视觉 (Jìsuànjī shìjué)',
        'id': 66,
        'ingilizce': 'Computer Vision (#66)',
        'kategori': 'Görüntü İşleme',
        'ornek_cumle': 'Ahmet uses computer vision in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Bilgisayarlı Görü'},
    {   'bengalce': 'এম্বেডেড সিস্টেম (Embedded system)',
        'cince': '嵌入式系统 (Qiànrùshì xìtǒng)',
        'id': 67,
        'ingilizce': 'Embedded Systems (#67)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses embedded systems in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Gömülü Sistemler'},
    {   'bengalce': 'মাইক্রোকন্ট্রোলার (Microcontroller)',
        'cince': '微控制器 (Wēi kòngzhìqì)',
        'id': 68,
        'ingilizce': 'Microcontroller (#68)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses microcontroller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Mikrodenetleyici'},
    {   'bengalce': 'আল্ট্রাসনিক সেন্সর (Ultrasonic sensor)',
        'cince': '超声波传感器 (Chāoshēngbō chuángǎnqì)',
        'id': 69,
        'ingilizce': 'Ultrasonic Sensor (#69)',
        'kategori': 'Sensör',
        'ornek_cumle': 'Ahmet uses ultrasonic sensor in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Ultrasonik Sensör'},
    {   'bengalce': 'থ্রিডি প্রিন্টিং (3D printing)',
        'cince': '3D打印 (3D dǎyìn)',
        'id': 70,
        'ingilizce': 'Three Dimensional Printing (#70)',
        'kategori': 'Üretim',
        'ornek_cumle': 'Ahmet uses three dimensional printing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Üç Boyutlu Baskı'},
    {   'bengalce': 'বর্গমূল (Borgomul)',
        'cince': '平方根 (Píngfānggēn)',
        'id': 71,
        'ingilizce': 'Square Root (#71)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses square root in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Karekök'},
    {   'bengalce': 'মৌলিক সংখ্যা (Moulik songkha)',
        'cince': '质数 (Zhìshù)',
        'id': 72,
        'ingilizce': 'Prime Number (#72)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses prime number in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Asal Sayı'},
    {   'bengalce': 'রৈখিক সমীকরণ (Roikhik somikoron)',
        'cince': '线性方程 (Xiànxìng fāngchéng)',
        'id': 73,
        'ingilizce': 'Linear Equation (#73)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses linear equation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Doğrusal Denklem'},
    {   'bengalce': 'গরিষ্ঠ সাধারণ গুণনীয়ক (Goshagu)',
        'cince': '最大公约数 (Zuìdà gōngyuēshù)',
        'id': 74,
        'ingilizce': 'Greatest Common Divisor (#74)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses greatest common divisor in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'En Büyük Ortak Bölen (EBOB)'},
    {   'bengalce': 'লঘিষ্ঠ সাধারণ গুণিতক (Loshagu)',
        'cince': '最小公倍数 (Zuìxiǎo gōngbèishù)',
        'id': 75,
        'ingilizce': 'Least Common Multiple (#75)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses least common multiple in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'En Küçük Ortak Kat (EKOK)'},
    {   'bengalce': 'সূচক (Suchok)',
        'cince': '幂运算 (Mì yùnsuàn)',
        'id': 76,
        'ingilizce': 'Exponentiation (#76)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses exponentiation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Üs Alma / Üslü Sayılar'},
    {   'bengalce': 'পিথাগোরাসের উপপাদ্য (Pithagoraser upopaddo)',
        'cince': '勾股定理 (Gōugǔ dìnglǐ)',
        'id': 77,
        'ingilizce': 'Pythagorean Theorem (#77)',
        'kategori': 'Geometri',
        'ornek_cumle': 'Ahmet uses pythagorean theorem in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Pisagor Teoremi'},
    {   'bengalce': 'অধ্যবসায় এবং শৃঙ্খলা (Oddhobosay ebong srinkhola)',
        'cince': '毅力与纪律 (Yìlì yǔ jìlǜ)',
        'id': 78,
        'ingilizce': 'Perseverance and Discipline (#78)',
        'kategori': 'Kişisel Gelişim',
        'ornek_cumle': 'Ahmet uses perseverance and discipline in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Azim ve Disiplin'},
    {   'bengalce': 'বৈজ্ঞানিক গবেষণা (Boigganik gobeshona)',
        'cince': '科学研究 (Kēxué yánjiū)',
        'id': 79,
        'ingilizce': 'Scientific Research (#79)',
        'kategori': 'Bilim',
        'ornek_cumle': 'Ahmet uses scientific research in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bilimsel Araştırma'},
    {   'bengalce': 'অ্যালগরিদম অপ্টিমাইজেশন (Algorithm optimization)',
        'cince': '算法优化 (Suànfǎ yōuhuà)',
        'id': 80,
        'ingilizce': 'Algorithm Optimization (#80)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses algorithm optimization in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Algoritma Optimizasyonu'},
    {   'bengalce': 'ফ্লাইট কন্ট্রোলার (Flight controller)',
        'cince': '飞行控制器 (Fēixíng kòngzhìqì)',
        'id': 81,
        'ingilizce': 'Flight Controller (#81)',
        'kategori': 'İHA / Drone',
        'ornek_cumle': 'Ahmet uses flight controller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Uçuş Kontrol Kartı'},
    {   'bengalce': 'ব্যাটারি ম্যানেজমেন্ট (Battery management)',
        'cince': '电池管理 (Diànchí guǎnlǐ)',
        'id': 82,
        'ingilizce': 'Battery Management (#82)',
        'kategori': 'Elektronik',
        'ornek_cumle': 'Ahmet uses battery management in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Batarya Yönetimi'},
    {   'bengalce': 'সিগন্যাল প্রসেসিং (Signal processing)',
        'cince': '信号处理 (Xìnhào chǔlǐ)',
        'id': 83,
        'ingilizce': 'Signal Processing (#83)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses signal processing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Sinyal İşleme'},
    {   'bengalce': 'ডেটা স্ট্রাকচার (Data structure)',
        'cince': '数据结构 (Shùjù jiégòu)',
        'id': 84,
        'ingilizce': 'Data Structure (#84)',
        'kategori': 'Bilgisayar Bilimi',
        'ornek_cumle': 'Ahmet uses data structure in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Veri Yapısı'},
    {   'bengalce': 'অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং (OOP)',
        'cince': '面向对象编程 (Miànxiàng duìxiàng biānchéng)',
        'id': 85,
        'ingilizce': 'Object Oriented Programming (#85)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses object oriented programming in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Nesne Yönelimli Programlama'},
    {   'bengalce': 'সাইবার নিরাপত্তা (Cyber nirapotta)',
        'cince': '网络安全 (Wǎngluò ānquán)',
        'id': 86,
        'ingilizce': 'Cyber Security (#86)',
        'kategori': 'Güvenlik',
        'ornek_cumle': 'Ahmet uses cyber security in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Siber Güvenlik'},
    {   'bengalce': 'ক্লাউড কম্পিউটিং (Cloud computing)',
        'cince': '云计算 (Yún jìsuàn)',
        'id': 87,
        'ingilizce': 'Cloud Computing (#87)',
        'kategori': 'Sistem',
        'ornek_cumle': 'Ahmet uses cloud computing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bulut Bilişim'},
    {   'bengalce': 'ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)',
        'cince': '自然语言处理 (Zìrán yǔyán chǔlǐ)',
        'id': 88,
        'ingilizce': 'Natural Language Processing (#88)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses natural language processing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Doğal Dil İşleme'},
    {   'bengalce': 'রোবোটিক্স এবং অটোমেশন (Robotics)',
        'cince': '机器人与自动化 (Jīqìrén yǔ zìdònghuà)',
        'id': 89,
        'ingilizce': 'Robotics and Automation (#89)',
        'kategori': 'Robotik',
        'ornek_cumle': 'Ahmet uses robotics and automation in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Robotik ve Otomasyon'},
    {   'bengalce': 'অ্যারোডাইনামিক্স (Aerodynamics)',
        'cince': '空气动力学 (Kōngqì dònglìxué)',
        'id': 90,
        'ingilizce': 'Aerodynamics (#90)',
        'kategori': 'Fizik',
        'ornek_cumle': 'Ahmet uses aerodynamics in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Orta',
        'turkce': 'Aerodinamik'},
    {   'bengalce': 'কৃত্রিম বুদ্ধিমত্তা (Kritrim buddhimotta)',
        'cince': '人工智能 (Réngōng zhìnéng)',
        'id': 91,
        'ingilizce': 'Artificial Intelligence (#91)',
        'kategori': 'Teknoloji',
        'ornek_cumle': 'Ahmet uses artificial intelligence in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Yapay Zeka'},
    {   'bengalce': 'স্বায়ত্তশাসিত ড্রোন (Sbayottoshasito drone)',
        'cince': '自主无人机 (Zìzhǔ wúrénjī)',
        'id': 92,
        'ingilizce': 'Autonomous Drone (#92)',
        'kategori': 'Havacılık',
        'ornek_cumle': 'Ahmet uses autonomous drone in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Otonom İnsansız Hava Aracı'},
    {   'bengalce': 'সফটওয়্যার ইঞ্জিনিয়ারিং (Software engineering)',
        'cince': '软件工程 (Ruǎnjiàn gōngchéng)',
        'id': 93,
        'ingilizce': 'Software Engineering (#93)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses software engineering in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Yazılım Mühendisliği'},
    {   'bengalce': 'মেশিন লার্নিং (Machine learning)',
        'cince': '机器学习 (Jīqì xuéxí)',
        'id': 94,
        'ingilizce': 'Machine Learning (#94)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses machine learning in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Makine Öğrenmesi'},
    {   'bengalce': 'নিউরাল নেটওয়ার্ক (Neural network)',
        'cince': '神经网络 (Shénjīng wǎngluò)',
        'id': 95,
        'ingilizce': 'Neural Network (#95)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses neural network in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Sinir Ağı'},
    {   'bengalce': 'কম্পিউটার ভিশন (Computer vision)',
        'cince': '计算机视觉 (Jìsuànjī shìjué)',
        'id': 96,
        'ingilizce': 'Computer Vision (#96)',
        'kategori': 'Görüntü İşleme',
        'ornek_cumle': 'Ahmet uses computer vision in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Bilgisayarlı Görü'},
    {   'bengalce': 'এম্বেডেড সিস্টেম (Embedded system)',
        'cince': '嵌入式系统 (Qiànrùshì xìtǒng)',
        'id': 97,
        'ingilizce': 'Embedded Systems (#97)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses embedded systems in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Gömülü Sistemler'},
    {   'bengalce': 'মাইক্রোকন্ট্রোলার (Microcontroller)',
        'cince': '微控制器 (Wēi kòngzhìqì)',
        'id': 98,
        'ingilizce': 'Microcontroller (#98)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses microcontroller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Mikrodenetleyici'},
    {   'bengalce': 'আল্ট্রাসনিক সেন্সর (Ultrasonic sensor)',
        'cince': '超声波传感器 (Chāoshēngbō chuángǎnqì)',
        'id': 99,
        'ingilizce': 'Ultrasonic Sensor (#99)',
        'kategori': 'Sensör',
        'ornek_cumle': 'Ahmet uses ultrasonic sensor in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Ultrasonik Sensör'},
    {   'bengalce': 'থ্রিডি প্রিন্টিং (3D printing)',
        'cince': '3D打印 (3D dǎyìn)',
        'id': 100,
        'ingilizce': 'Three Dimensional Printing (#100)',
        'kategori': 'Üretim',
        'ornek_cumle': 'Ahmet uses three dimensional printing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Üç Boyutlu Baskı'},
    {   'bengalce': 'বর্গমূল (Borgomul)',
        'cince': '平方根 (Píngfānggēn)',
        'id': 101,
        'ingilizce': 'Square Root (#101)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses square root in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Temel',
        'turkce': 'Karekök'},
    {   'bengalce': 'মৌলিক সংখ্যা (Moulik songkha)',
        'cince': '质数 (Zhìshù)',
        'id': 102,
        'ingilizce': 'Prime Number (#102)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses prime number in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Orta',
        'turkce': 'Asal Sayı'},
    {   'bengalce': 'রৈখিক সমীকরণ (Roikhik somikoron)',
        'cince': '线性方程 (Xiànxìng fāngchéng)',
        'id': 103,
        'ingilizce': 'Linear Equation (#103)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses linear equation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Doğrusal Denklem'},
    {   'bengalce': 'গরিষ্ঠ সাধারণ গুণনীয়ক (Goshagu)',
        'cince': '最大公约数 (Zuìdà gōngyuēshù)',
        'id': 104,
        'ingilizce': 'Greatest Common Divisor (#104)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses greatest common divisor in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'En Büyük Ortak Bölen (EBOB)'},
    {   'bengalce': 'লঘিষ্ঠ সাধারণ গুণিতক (Loshagu)',
        'cince': '最小公倍数 (Zuìxiǎo gōngbèishù)',
        'id': 105,
        'ingilizce': 'Least Common Multiple (#105)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses least common multiple in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'En Küçük Ortak Kat (EKOK)'},
    {   'bengalce': 'সূচক (Suchok)',
        'cince': '幂运算 (Mì yùnsuàn)',
        'id': 106,
        'ingilizce': 'Exponentiation (#106)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses exponentiation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Üs Alma / Üslü Sayılar'},
    {   'bengalce': 'পিথাগোরাসের উপপাদ্য (Pithagoraser upopaddo)',
        'cince': '勾股定理 (Gōugǔ dìnglǐ)',
        'id': 107,
        'ingilizce': 'Pythagorean Theorem (#107)',
        'kategori': 'Geometri',
        'ornek_cumle': 'Ahmet uses pythagorean theorem in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Pisagor Teoremi'},
    {   'bengalce': 'অধ্যবসায় এবং শৃঙ্খলা (Oddhobosay ebong srinkhola)',
        'cince': '毅力与纪律 (Yìlì yǔ jìlǜ)',
        'id': 108,
        'ingilizce': 'Perseverance and Discipline (#108)',
        'kategori': 'Kişisel Gelişim',
        'ornek_cumle': 'Ahmet uses perseverance and discipline in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Azim ve Disiplin'},
    {   'bengalce': 'বৈজ্ঞানিক গবেষণা (Boigganik gobeshona)',
        'cince': '科学研究 (Kēxué yánjiū)',
        'id': 109,
        'ingilizce': 'Scientific Research (#109)',
        'kategori': 'Bilim',
        'ornek_cumle': 'Ahmet uses scientific research in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Bilimsel Araştırma'},
    {   'bengalce': 'অ্যালগরিদম অপ্টিমাইজেশন (Algorithm optimization)',
        'cince': '算法优化 (Suànfǎ yōuhuà)',
        'id': 110,
        'ingilizce': 'Algorithm Optimization (#110)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses algorithm optimization in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Algoritma Optimizasyonu'},
    {   'bengalce': 'ফ্লাইট কন্ট্রোলার (Flight controller)',
        'cince': '飞行控制器 (Fēixíng kòngzhìqì)',
        'id': 111,
        'ingilizce': 'Flight Controller (#111)',
        'kategori': 'İHA / Drone',
        'ornek_cumle': 'Ahmet uses flight controller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Uçuş Kontrol Kartı'},
    {   'bengalce': 'ব্যাটারি ম্যানেজমেন্ট (Battery management)',
        'cince': '电池管理 (Diànchí guǎnlǐ)',
        'id': 112,
        'ingilizce': 'Battery Management (#112)',
        'kategori': 'Elektronik',
        'ornek_cumle': 'Ahmet uses battery management in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Batarya Yönetimi'},
    {   'bengalce': 'সিগন্যাল প্রসেসিং (Signal processing)',
        'cince': '信号处理 (Xìnhào chǔlǐ)',
        'id': 113,
        'ingilizce': 'Signal Processing (#113)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses signal processing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Sinyal İşleme'},
    {   'bengalce': 'ডেটা স্ট্রাকচার (Data structure)',
        'cince': '数据结构 (Shùjù jiégòu)',
        'id': 114,
        'ingilizce': 'Data Structure (#114)',
        'kategori': 'Bilgisayar Bilimi',
        'ornek_cumle': 'Ahmet uses data structure in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Veri Yapısı'},
    {   'bengalce': 'অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং (OOP)',
        'cince': '面向对象编程 (Miànxiàng duìxiàng biānchéng)',
        'id': 115,
        'ingilizce': 'Object Oriented Programming (#115)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses object oriented programming in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Nesne Yönelimli Programlama'},
    {   'bengalce': 'সাইবার নিরাপত্তা (Cyber nirapotta)',
        'cince': '网络安全 (Wǎngluò ānquán)',
        'id': 116,
        'ingilizce': 'Cyber Security (#116)',
        'kategori': 'Güvenlik',
        'ornek_cumle': 'Ahmet uses cyber security in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Siber Güvenlik'},
    {   'bengalce': 'ক্লাউড কম্পিউটিং (Cloud computing)',
        'cince': '云计算 (Yún jìsuàn)',
        'id': 117,
        'ingilizce': 'Cloud Computing (#117)',
        'kategori': 'Sistem',
        'ornek_cumle': 'Ahmet uses cloud computing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Bulut Bilişim'},
    {   'bengalce': 'ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)',
        'cince': '自然语言处理 (Zìrán yǔyán chǔlǐ)',
        'id': 118,
        'ingilizce': 'Natural Language Processing (#118)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses natural language processing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Doğal Dil İşleme'},
    {   'bengalce': 'রোবোটিক্স এবং অটোমেশন (Robotics)',
        'cince': '机器人与自动化 (Jīqìrén yǔ zìdònghuà)',
        'id': 119,
        'ingilizce': 'Robotics and Automation (#119)',
        'kategori': 'Robotik',
        'ornek_cumle': 'Ahmet uses robotics and automation in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Robotik ve Otomasyon'},
    {   'bengalce': 'অ্যারোডাইনামিক্স (Aerodynamics)',
        'cince': '空气动力学 (Kōngqì dònglìxué)',
        'id': 120,
        'ingilizce': 'Aerodynamics (#120)',
        'kategori': 'Fizik',
        'ornek_cumle': 'Ahmet uses aerodynamics in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Aerodinamik'},
    {   'bengalce': 'কৃত্রিম বুদ্ধিমত্তা (Kritrim buddhimotta)',
        'cince': '人工智能 (Réngōng zhìnéng)',
        'id': 121,
        'ingilizce': 'Artificial Intelligence (#121)',
        'kategori': 'Teknoloji',
        'ornek_cumle': 'Ahmet uses artificial intelligence in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Yapay Zeka'},
    {   'bengalce': 'স্বায়ত্তশাসিত ড্রোন (Sbayottoshasito drone)',
        'cince': '自主无人机 (Zìzhǔ wúrénjī)',
        'id': 122,
        'ingilizce': 'Autonomous Drone (#122)',
        'kategori': 'Havacılık',
        'ornek_cumle': 'Ahmet uses autonomous drone in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Otonom İnsansız Hava Aracı'},
    {   'bengalce': 'সফটওয়্যার ইঞ্জিনিয়ারিং (Software engineering)',
        'cince': '软件工程 (Ruǎnjiàn gōngchéng)',
        'id': 123,
        'ingilizce': 'Software Engineering (#123)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses software engineering in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Yazılım Mühendisliği'},
    {   'bengalce': 'মেশিন লার্নিং (Machine learning)',
        'cince': '机器学习 (Jīqì xuéxí)',
        'id': 124,
        'ingilizce': 'Machine Learning (#124)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses machine learning in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Makine Öğrenmesi'},
    {   'bengalce': 'নিউরাল নেটওয়ার্ক (Neural network)',
        'cince': '神经网络 (Shénjīng wǎngluò)',
        'id': 125,
        'ingilizce': 'Neural Network (#125)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses neural network in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Sinir Ağı'},
    {   'bengalce': 'কম্পিউটার ভিশন (Computer vision)',
        'cince': '计算机视觉 (Jìsuànjī shìjué)',
        'id': 126,
        'ingilizce': 'Computer Vision (#126)',
        'kategori': 'Görüntü İşleme',
        'ornek_cumle': 'Ahmet uses computer vision in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Bilgisayarlı Görü'},
    {   'bengalce': 'এম্বেডেড সিস্টেম (Embedded system)',
        'cince': '嵌入式系统 (Qiànrùshì xìtǒng)',
        'id': 127,
        'ingilizce': 'Embedded Systems (#127)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses embedded systems in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Gömülü Sistemler'},
    {   'bengalce': 'মাইক্রোকন্ট্রোলার (Microcontroller)',
        'cince': '微控制器 (Wēi kòngzhìqì)',
        'id': 128,
        'ingilizce': 'Microcontroller (#128)',
        'kategori': 'Donanım',
        'ornek_cumle': 'Ahmet uses microcontroller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Mikrodenetleyici'},
    {   'bengalce': 'আল্ট্রাসনিক সেন্সর (Ultrasonic sensor)',
        'cince': '超声波传感器 (Chāoshēngbō chuángǎnqì)',
        'id': 129,
        'ingilizce': 'Ultrasonic Sensor (#129)',
        'kategori': 'Sensör',
        'ornek_cumle': 'Ahmet uses ultrasonic sensor in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Ultrasonik Sensör'},
    {   'bengalce': 'থ্রিডি প্রিন্টিং (3D printing)',
        'cince': '3D打印 (3D dǎyìn)',
        'id': 130,
        'ingilizce': 'Three Dimensional Printing (#130)',
        'kategori': 'Üretim',
        'ornek_cumle': 'Ahmet uses three dimensional printing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Üç Boyutlu Baskı'},
    {   'bengalce': 'বর্গমূল (Borgomul)',
        'cince': '平方根 (Píngfānggēn)',
        'id': 131,
        'ingilizce': 'Square Root (#131)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses square root in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Karekök'},
    {   'bengalce': 'মৌলিক সংখ্যা (Moulik songkha)',
        'cince': '质数 (Zhìshù)',
        'id': 132,
        'ingilizce': 'Prime Number (#132)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses prime number in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Asal Sayı'},
    {   'bengalce': 'রৈখিক সমীকরণ (Roikhik somikoron)',
        'cince': '线性方程 (Xiànxìng fāngchéng)',
        'id': 133,
        'ingilizce': 'Linear Equation (#133)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses linear equation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Doğrusal Denklem'},
    {   'bengalce': 'গরিষ্ঠ সাধারণ গুণনীয়ক (Goshagu)',
        'cince': '最大公约数 (Zuìdà gōngyuēshù)',
        'id': 134,
        'ingilizce': 'Greatest Common Divisor (#134)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses greatest common divisor in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'En Büyük Ortak Bölen (EBOB)'},
    {   'bengalce': 'লঘিষ্ঠ সাধারণ গুণিতক (Loshagu)',
        'cince': '最小公倍数 (Zuìxiǎo gōngbèishù)',
        'id': 135,
        'ingilizce': 'Least Common Multiple (#135)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses least common multiple in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'En Küçük Ortak Kat (EKOK)'},
    {   'bengalce': 'সূচক (Suchok)',
        'cince': '幂运算 (Mì yùnsuàn)',
        'id': 136,
        'ingilizce': 'Exponentiation (#136)',
        'kategori': 'Matematik',
        'ornek_cumle': 'Ahmet uses exponentiation in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Üs Alma / Üslü Sayılar'},
    {   'bengalce': 'পিথাগোরাসের উপপাদ্য (Pithagoraser upopaddo)',
        'cince': '勾股定理 (Gōugǔ dìnglǐ)',
        'id': 137,
        'ingilizce': 'Pythagorean Theorem (#137)',
        'kategori': 'Geometri',
        'ornek_cumle': 'Ahmet uses pythagorean theorem in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Pisagor Teoremi'},
    {   'bengalce': 'অধ্যবসায় এবং শৃঙ্খলা (Oddhobosay ebong srinkhola)',
        'cince': '毅力与纪律 (Yìlì yǔ jìlǜ)',
        'id': 138,
        'ingilizce': 'Perseverance and Discipline (#138)',
        'kategori': 'Kişisel Gelişim',
        'ornek_cumle': 'Ahmet uses perseverance and discipline in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Orta',
        'turkce': 'Azim ve Disiplin'},
    {   'bengalce': 'বৈজ্ঞানিক গবেষণা (Boigganik gobeshona)',
        'cince': '科学研究 (Kēxué yánjiū)',
        'id': 139,
        'ingilizce': 'Scientific Research (#139)',
        'kategori': 'Bilim',
        'ornek_cumle': 'Ahmet uses scientific research in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bilimsel Araştırma'},
    {   'bengalce': 'অ্যালগরিদম অপ্টিমাইজেশন (Algorithm optimization)',
        'cince': '算法优化 (Suànfǎ yōuhuà)',
        'id': 140,
        'ingilizce': 'Algorithm Optimization (#140)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses algorithm optimization in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Algoritma Optimizasyonu'},
    {   'bengalce': 'ফ্লাইট কন্ট্রোলার (Flight controller)',
        'cince': '飞行控制器 (Fēixíng kòngzhìqì)',
        'id': 141,
        'ingilizce': 'Flight Controller (#141)',
        'kategori': 'İHA / Drone',
        'ornek_cumle': 'Ahmet uses flight controller in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Temel',
        'turkce': 'Uçuş Kontrol Kartı'},
    {   'bengalce': 'ব্যাটারি ম্যানেজমেন্ট (Battery management)',
        'cince': '电池管理 (Diànchí guǎnlǐ)',
        'id': 142,
        'ingilizce': 'Battery Management (#142)',
        'kategori': 'Elektronik',
        'ornek_cumle': 'Ahmet uses battery management in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Batarya Yönetimi'},
    {   'bengalce': 'সিগন্যাল প্রসেসিং (Signal processing)',
        'cince': '信号处理 (Xìnhào chǔlǐ)',
        'id': 143,
        'ingilizce': 'Signal Processing (#143)',
        'kategori': 'Mühendislik',
        'ornek_cumle': 'Ahmet uses signal processing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Sinyal İşleme'},
    {   'bengalce': 'ডেটা স্ট্রাকচার (Data structure)',
        'cince': '数据结构 (Shùjù jiégòu)',
        'id': 144,
        'ingilizce': 'Data Structure (#144)',
        'kategori': 'Bilgisayar Bilimi',
        'ornek_cumle': 'Ahmet uses data structure in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Akademik',
        'turkce': 'Veri Yapısı'},
    {   'bengalce': 'অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং (OOP)',
        'cince': '面向对象编程 (Miànxiàng duìxiàng biānchéng)',
        'id': 145,
        'ingilizce': 'Object Oriented Programming (#145)',
        'kategori': 'Yazılım',
        'ornek_cumle': 'Ahmet uses object oriented programming in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Nesne Yönelimli Programlama'},
    {   'bengalce': 'সাইবার নিরাপত্তা (Cyber nirapotta)',
        'cince': '网络安全 (Wǎngluò ānquán)',
        'id': 146,
        'ingilizce': 'Cyber Security (#146)',
        'kategori': 'Güvenlik',
        'ornek_cumle': 'Ahmet uses cyber security in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'Orta',
        'turkce': 'Siber Güvenlik'},
    {   'bengalce': 'ক্লাউড কম্পিউটিং (Cloud computing)',
        'cince': '云计算 (Yún jìsuàn)',
        'id': 147,
        'ingilizce': 'Cloud Computing (#147)',
        'kategori': 'Sistem',
        'ornek_cumle': 'Ahmet uses cloud computing in his AREX AI Studio and autonomous drone '
                       'projects.',
        'seviye': 'İleri Mühendislik',
        'turkce': 'Bulut Bilişim'},
    {   'bengalce': 'ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং (NLP)',
        'cince': '自然语言处理 (Zìrán yǔyán chǔlǐ)',
        'id': 148,
        'ingilizce': 'Natural Language Processing (#148)',
        'kategori': 'Yapay Zeka',
        'ornek_cumle': 'Ahmet uses natural language processing in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Akademik',
        'turkce': 'Doğal Dil İşleme'},
    {   'bengalce': 'রোবোটিক্স এবং অটোমেশন (Robotics)',
        'cince': '机器人与自动化 (Jīqìrén yǔ zìdònghuà)',
        'id': 149,
        'ingilizce': 'Robotics and Automation (#149)',
        'kategori': 'Robotik',
        'ornek_cumle': 'Ahmet uses robotics and automation in his AREX AI Studio and autonomous '
                       'drone projects.',
        'seviye': 'Temel',
        'turkce': 'Robotik ve Otomasyon'},
    {   'bengalce': 'অ্যারোডাইনামিক্স (Aerodynamics)',
        'cince': '空气动力学 (Kōngqì dònglìxué)',
        'id': 150,
        'ingilizce': 'Aerodynamics (#150)',
        'kategori': 'Fizik',
        'ornek_cumle': 'Ahmet uses aerodynamics in his AREX AI Studio and autonomous drone projects.',
        'seviye': 'Orta',
        'turkce': 'Aerodinamik'}]

SISTEM_KISAYOL_REHBERI = [   {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'},
    {   'aciklama': 'Seçili metni veya kodu panoya kopyalar.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + C'},
    {   'aciklama': 'Panodaki metni veya kodu imlecin olduğu yere yapıştırır.',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + V'},
    {   'aciklama': 'Fare ile bir satırın üzerine 3 kez hızlıca tıklamak tüm satırı tek seferde '
                    'seçer.',
        'platform': 'Hızlı Seçim',
        'tus': 'Üç Kez Tıklama (Triple Click)'},
    {   'aciklama': 'Dosyadaki tüm kodu tek seferde seçer (Kopyala-Yapıştır için en hızlı yöntem).',
        'platform': 'Masaüstü Genel',
        'tus': 'Ctrl + A'},
    {   'aciklama': 'Son yapılan işlemi geri alır / ileri alır.',
        'platform': 'Düzenleme',
        'tus': 'Ctrl + Z / Ctrl + Y'},
    {   'aciklama': 'PyCharm üzerinde aktif Python dosyasını çalıştırır.',
        'platform': 'PyCharm',
        'tus': 'Shift + F10'},
    {   'aciklama': 'PyCharm içinde alt terminali doğrudan açar (`streamlit run main.py` yazmak '
                    'için).',
        'platform': 'PyCharm',
        'tus': 'Alt + F12'},
    {   'aciklama': 'PyCharm içinde Python kodunu PEP8 standartlarına göre otomatik düzenler.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + Alt + L'},
    {   'aciklama': 'Seçili satırları tek tuşla yorum satırı (`#`) yapar veya yorumdan çıkarır.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + /'},
    {   'aciklama': 'Dosya içinde kelime arar / toplu olarak değiştirir.',
        'platform': 'PyCharm',
        'tus': 'Ctrl + F / Ctrl + R'}]

def tema_paleti_getir(tema_adi: str = "Derin Lacivert (Klasik Ar)") -> dict:
    """Seçilen tema adına ait tüm renk kodlarını güvenli biçimde döndürür."""
    if tema_adi in TEMA_PALETLERI:
        return TEMA_PALETLERI[tema_adi]
    return TEMA_PALETLERI["Derin Lacivert (Klasik Ar)"]


def arayuz_stillerini_yukle(tema_adi: str = "Derin Lacivert (Klasik Ar)"):
    """
    Seçilen tema paletinin (Derin Lacivert, Kraliyet Moru, Zümrüt Matriks,
    Kızıl Süpernova, Okyanus Derinliği, OLED, Siber Neon) TÜM renklerini
    CSS değişkenlerine dinamik olarak bağlar. Tema değiştiğinde anında
    arka plan, yan menü, butonlar, sekmeler, sohbet kutuları ve 3D kartlar güncellenir.
    """
    palet = tema_paleti_getir(tema_adi)
    bg1 = palet["bg_primary"]
    bg2 = palet["bg_secondary"]
    card = palet["card_bg"]
    elev = palet.get("elevated_bg", card)
    acc1 = palet["accent_neon"]
    acc2 = palet["accent_blue"]
    acc3 = palet["accent_purple"]
    acc4 = palet.get("accent_rose", acc1)
    border_soft = palet.get("border_soft", "rgba(148, 163, 184, 0.22)")
    txt_main = palet["text_main"]
    txt_sub = palet["text_sub"]

    css_metni = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg-main: {bg1};
    --bg-sidebar: {bg2};
    --bg-surface: {card};
    --bg-elevated: {elev};
    --accent-primary: {acc1};
    --accent-secondary: {acc2};
    --accent-tertiary: {acc3};
    --accent-soft: {acc4};
    --border-subtle: {border_soft};
    --text-primary: {txt_main};
    --text-secondary: {txt_sub};
}}

/* 1. ANA UYGULAMA ZEMİNİ VE TİPOGRAFİ */
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container {{
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

.block-container {{
    padding-top: 3.8rem !important;
    padding-bottom: 1.15rem !important;
    max-width: 1180px !important;
}}

/* AREX Asil Lacivert İnce Kaydırma Çubuğu */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg-main); }}
::-webkit-scrollbar-thumb {{ background: rgba(56, 189, 248, 0.28); border-radius: 999px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba(56, 189, 248, 0.52); }}

header[data-testid="stHeader"] {{
    background-color: var(--bg-main) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}}

h1, h2, h3, h4 {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}}

p, li, label, span {{
    color: var(--text-primary);
}}

small,
.stCaption,
[data-testid="stCaptionContainer"] p {{
    color: var(--text-secondary) !important;
    font-size: 0.83rem !important;
}}

/* 2. YAN MENÜ (SIDEBAR) — TEMAYA GÖRE DİNAMİK RENK DEĞİŞİMİ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{
    background-color: var(--bg-sidebar) !important;
    background-image: none !important;
    border-right: 1px solid var(--border-subtle) !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {{
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
}}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0.45rem !important;
}}

/* 3. GİRDİ KUTULARI, SEÇİM LİSTELERİ VE SOHBET GİRİŞİ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stChatInput"] textarea,
[data-baseweb="select"] > div {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    font-size: 0.94rem !important;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stChatInput"] textarea:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 1px var(--accent-primary) !important;
}}

[data-testid="stChatInput"] {{
    background-color: transparent !important;
}}

ul[role="listbox"] {{
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
}}

ul[role="listbox"] li {{
    color: var(--text-primary) !important;
}}

ul[role="listbox"] li:hover {{
    background-color: var(--bg-elevated) !important;
}}

/* 4. AÇILIR ÇEKMECELER (EXPANDER) VE DURUM KUTULARI */
[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {{
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}}

/* 5. SOHBET MESAJ BALONCUKLARI */
[data-testid="stChatMessage"] {{
    background: linear-gradient(160deg, rgba(11, 25, 58, 0.92), rgba(7, 17, 42, 0.96)) !important;
    border: 1px solid rgba(56, 189, 248, 0.16) !important;
    border-left: 2px solid rgba(56, 189, 248, 0.45) !important;
    border-radius: 12px !important;
    padding: 11px 15px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 4px 18px rgba(2, 6, 23, 0.35) !important;
}}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {{
    color: var(--text-primary) !important;
    font-size: 0.96rem !important;
    font-weight: 400 !important;
    line-height: 1.65 !important;
}}

[data-testid="stChatMessage"] a {{
    color: var(--accent-primary) !important;
    text-decoration: underline !important;
}}

/* 6. BUTONLAR VE SEKMELER (TABS) — SADE & PREMIUM */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button,
[data-testid="stLinkButton"] a {{
    background-color: var(--bg-elevated) !important;
    background-image: none !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    min-height: 39px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    transition: border-color 0.18s ease, background-color 0.18s ease, transform 0.12s ease !important;
}}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stLinkButton"] a:hover {{
    background-color: var(--bg-surface) !important;
    border-color: var(--accent-primary) !important;
    color: var(--accent-primary) !important;
    box-shadow: none !important;
}}

button[data-baseweb="tab"] {{
    background-color: transparent !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    border-radius: 8px 8px 0 0 !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    background-color: var(--bg-surface) !important;
    color: var(--accent-primary) !important;
    border-bottom: 2px solid var(--accent-primary) !important;
}}

/* 7. METRİKLER, ÜST BAŞLIK VE BİLGİ KARTLARI */
.stMetric {{
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    padding: 14px !important;
    border-radius: 12px !important;
}}

.stMetric label {{
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}}

.stMetric [data-testid="stMetricValue"] {{
    color: var(--accent-primary) !important;
    font-weight: 600 !important;
}}

.premium-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    padding: 10px 16px;
    background: linear-gradient(135deg, #06122b 0%, #0b1e45 55%, #071533 100%);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-left: 3px solid var(--accent-primary);
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 6px 24px rgba(2, 8, 24, 0.45);
}}

.premium-header-title {{
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font-size: 1.04rem;
    font-weight: 700;
    color: #f8fafc !important;
    letter-spacing: 0.04em;
}}

.arex-crest {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 7px;
    background: linear-gradient(135deg, #0ea5e9, #1d4ed8);
    color: #ffffff !important;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
}}

.premium-header-badge {{
    font-size: 0.76rem;
    font-weight: 500;
    color: #bae6fd !important;
    background: rgba(14, 33, 71, 0.78);
    border: 1px solid rgba(56, 189, 248, 0.25);
    padding: 3px 10px;
    border-radius: 999px;
}}

.premium-header-badge {{
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--accent-primary) !important;
    background-color: var(--bg-elevated);
    border: 1px solid var(--border-subtle);
    padding: 4px 11px;
    border-radius: 999px;
}}

.premium-card {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-primary);
    padding: 15px 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}}

.card-title {{
    color: var(--accent-primary) !important;
    font-size: 1.02rem !important;
    font-weight: 600 !important;
    margin-bottom: 4px;
}}

.card-meta {{
    color: var(--text-secondary) !important;
    font-size: 0.81rem !important;
    font-weight: 500 !important;
    margin-bottom: 7px;
}}

.card-desc {{
    color: var(--text-primary) !important;
    font-size: 0.93rem !important;
    font-weight: 400 !important;
    line-height: 1.62;
}}

.history-bubble {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-primary);
    border-radius: 10px;
    padding: 8px 11px;
    margin-bottom: 7px;
}}

.history-bubble-meta {{
    color: var(--accent-primary) !important;
    font-size: 0.74rem;
    font-weight: 500;
    margin-bottom: 3px;
}}

.history-bubble-text {{
    color: var(--text-primary) !important;
    font-size: 0.84rem;
}}

.live-badge {{
    display: inline-block;
    background-color: var(--bg-elevated);
    color: var(--accent-primary) !important;
    border: 1px solid var(--accent-primary);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.76rem;
    font-weight: 500 !important;
}}

.silent-badge {{
    display: inline-block;
    background: rgba(244, 63, 94, 0.12);
    color: #fda4af !important;
    border: 1px solid rgba(244, 63, 94, 0.35);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.76rem;
    font-weight: 500 !important;
}}

/* 8. 3D ÇEVİRMELİ DİL KARTLARI (FLIP CARD) — HEM BUTONLA (.is-flipped) HEM TIKLAMAYLA TAM ÇALIŞIR */
.flip-card-label {{
    display: block;
    width: 100%;
    perspective: 1400px;
    cursor: pointer;
    margin: 10px 0 18px 0;
}}

.flip-card-checkbox {{
    position: absolute;
    opacity: 0;
    pointer-events: none;
    width: 0;
    height: 0;
}}

.flip-card-inner {{
    position: relative;
    width: 100%;
    height: 325px;
    transition: transform 0.65s cubic-bezier(0.22, 1, 0.36, 1);
    transform-style: preserve-3d;
    -webkit-transform-style: preserve-3d;
}}

.flip-card-inner.is-flipped,
.flip-card-checkbox:checked + .flip-card-inner {{
    transform: rotateY(180deg);
    -webkit-transform: rotateY(180deg);
}}

.flip-card-front,
.flip-card-back {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 16px;
    padding: 20px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow-y: auto;
    border: 1px solid var(--border-subtle);
    background-color: var(--bg-surface);
}}

.flip-card-front {{
    border-top: 3px solid var(--accent-primary);
}}

.flip-card-back {{
    transform: rotateY(180deg);
    -webkit-transform: rotateY(180deg);
    border-top: 3px solid var(--accent-secondary);
    background-color: var(--bg-elevated);
}}

.flip-badge-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}}

.flip-badge {{
    background-color: var(--bg-elevated);
    border: 1px solid var(--border-subtle);
    color: var(--accent-primary) !important;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.78rem;
    font-weight: 500 !important;
}}

.flip-card-lang-tag {{
    color: var(--accent-primary) !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}

.flip-main-word {{
    font-size: clamp(1.45rem, 2.8vw, 2.05rem) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin: 12px 0 6px 0;
    line-height: 1.3;
}}

.flip-pronunciation {{
    font-size: 0.98rem !important;
    color: var(--accent-secondary) !important;
    font-weight: 500 !important;
    margin-bottom: 6px;
}}

.flip-example-text {{
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
    line-height: 1.45;
}}

.flip-back-meaning {{
    font-size: 1.22rem !important;
    font-weight: 600 !important;
    color: var(--accent-primary) !important;
    margin-bottom: 10px;
}}

.flip-back-row {{
    margin-bottom: 7px;
    color: var(--text-primary) !important;
    font-size: 0.92rem !important;
    line-height: 1.45;
}}

.flip-hint {{
    display: inline-block;
    background-color: var(--bg-main);
    border: 1px dashed var(--border-subtle);
    color: var(--text-secondary) !important;
    padding: 5px 14px;
    border-radius: 10px;
    font-size: 0.8rem;
}}

/* 9. MOBİL UYUMLULUK (RESPONSIVE) */
@media (max-width: 768px) {{
    .block-container {{
        padding-top: 4.1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }}
    .flip-card-inner {{
        height: 360px;
    }}
    .premium-header {{
        padding: 9px 12px;
    }}
}}
</style>"""
    st.markdown(css_metni, unsafe_allow_html=True)


# ==============================================================================
# 7. YARDIMCI BİLEŞEN RENDER FONKSİYONLARI (SIFIR GİRİNTİLİ, DİNAMİK TEMALI HTML)
# ==============================================================================
def hero_banner_goster(kalip_sayisi: int, aktif_tema: str = "Derin Lacivert (Klasik Ar)"):
    html = (
        '<div class="premium-header">'
        '<span class="premium-header-title"><span class="arex-crest">RX</span> AREX AI STUDIO</span>'
        f'<span class="premium-header-badge">v12.0 • Asil Lacivert • {aktif_tema}</span>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def bilgi_karti_olustur(baslik: str, alt_bilgi: str, aciklama: str) -> str:
    return (
        f'<div class="premium-card">'
        f'<div class="card-title">{baslik}</div>'
        f'<div class="card-meta">{alt_bilgi}</div>'
        f'<div class="card-desc">{aciklama}</div>'
        f'</div>'
    )


def sohbet_baloncuk_karti_olustur(etiket: str, saat: str, kisa_metin: str) -> str:
    return (
        f'<div class="history-bubble">'
        f'<div class="history-bubble-meta">💬 {etiket} &bull; 🕒 {saat}</div>'
        f'<div class="history-bubble-text">👤 {kisa_metin}</div>'
        f'</div>'
    )


def tema_renk_onizleme_karti_olustur(tema_adi: str) -> str:
    """Seçilen tema paletinin ana, yüzey ve vurgu renklerini küçük bir önizleme kartında gösterir."""
    p = tema_paleti_getir(tema_adi)
    return (
        f'<div class="premium-card">'
        f'<div class="card-title">🎨 Aktif Tema: {tema_adi}</div>'
        f'<div class="card-meta">{p.get("aciklama", "Dinamik koyu tema paleti")}</div>'
        f'<div style="display:flex;gap:8px;margin-top:8px;">'
        f'<span style="width:26px;height:26px;border-radius:6px;background:{p["bg_primary"]};border:1px solid #64748b;" title="Ana Zemin"></span>'
        f'<span style="width:26px;height:26px;border-radius:6px;background:{p["card_bg"]};border:1px solid #64748b;" title="Kart Yüzeyi"></span>'
        f'<span style="width:26px;height:26px;border-radius:6px;background:{p["accent_neon"]};border:1px solid #64748b;" title="Birincil Vurgu"></span>'
        f'<span style="width:26px;height:26px;border-radius:6px;background:{p["accent_blue"]};border:1px solid #64748b;" title="İkincil Vurgu"></span>'
        f'</div>'
        f'</div>'
    )


def cevirmeli_dil_karti_olustur(
    kart: dict,
    on_yuz_dili: str = "🇬🇧 İngilizce",
    ters_cevir: bool = False,
    kart_key: str = "tek",
) -> str:
    """
    Üzerine dokunulduğunda veya '🔄 Kartı Çevir' butonuna basıldığında 3D olarak
    pürüzsüz dönen çevirmeli dil kartı (Flip Card) üretir.
    Hem CSS checkbox hem de `.is-flipped` sınıfı ile çift güvenceli çalışır ve
    aktif tema paletinin renklerini otomatik kullanır.
    """
    checked_attr = "checked" if ters_cevir else ""
    flipped_cls = " is-flipped" if ters_cevir else ""

    if "İngilizce" in on_yuz_dili:
        on_baslik = "🇬🇧 İNGİLİZCE KART (ÖN YÜZ)"
        ana_ifade = kart["ingilizce"]
        okunus = f"🗣️ Türkçe Okunuşu: {kart['ing_okunus']}"
        ornek = f"📝 {kart['ornek_en']}"
    elif "Arapça" in on_yuz_dili:
        on_baslik = "🇸🇦 ARAPÇA KART (ÖN YÜZ)"
        ana_ifade = kart["arapca"]
        okunus = f"🗣️ Türkçe Okunuşu: {kart['ara_okunus']}"
        ornek = f"📝 {kart['ornek_ar']}"
    elif "Bengalce" in on_yuz_dili:
        on_baslik = "🇧🇩 BENGALCE KART (ÖN YÜZ)"
        ana_ifade = kart["bengalce"]
        okunus = f"🗣️ Türkçe Okunuşu: {kart['ben_okunus']}"
        ornek = f"📝 {kart['ornek_bn']}"
    else:
        on_baslik = "🇹🇷 TÜRKÇE KART (ÖN YÜZ)"
        ana_ifade = kart["turkce"]
        okunus = "🗣️ 3 Dilde Karşılığı İçin Kartı Çevir"
        ornek = f"Kategori: {kart['kategori']}"

    # Eğer ters_cevir True ise Streamlit'in input temizlemesine karşı doğrudan arka yüzü ön planda da güvenceye al
    return (
        f'<label class="flip-card-label" for="flip_{kart_key}_{kart["id"]}">'
        f'<input type="checkbox" id="flip_{kart_key}_{kart["id"]}" class="flip-card-checkbox" {checked_attr}>'
        f'<div class="flip-card-inner{flipped_cls}">'
        f'<div class="flip-card-front">'
        f'<div class="flip-badge-row">'
        f'<span class="flip-badge">🃏 Kart #{kart["id"]} &bull; {kart["seviye"]}</span>'
        f'<span class="flip-badge">{kart["kategori"]}</span>'
        f'</div>'
        f'<div>'
        f'<div class="flip-card-lang-tag">{on_baslik}</div>'
        f'<div class="flip-main-word">{ana_ifade}</div>'
        f'<div class="flip-pronunciation">{okunus}</div>'
        f'<div class="flip-example-text">{ornek}</div>'
        f'</div>'
        f'<div><span class="flip-hint">🔄 Kartı Çevirmek İçin Üzerine Tıkla veya Yukarıdaki Butona Bas</span></div>'
        f'</div>'
        f'<div class="flip-card-back">'
        f'<div class="flip-badge-row">'
        f'<span class="flip-badge">✅ ARKA YÜZ (TÜRKÇE ANLAMI &amp; 3 DİL)</span>'
        f'<span class="flip-badge">{kart["seviye"]}</span>'
        f'</div>'
        f'<div style="margin:8px 0;">'
        f'<div class="flip-back-meaning">🇹🇷 Anlamı: {kart["turkce"]}</div>'
        f'<div class="flip-back-row">🇬🇧 <strong>İngilizce:</strong> {kart["ingilizce"]} <em>({kart["ing_okunus"]})</em><br><small>{kart["ornek_en"]}</small></div>'
        f'<div class="flip-back-row">🇸🇦 <strong>Arapça:</strong> {kart["arapca"]} <em>({kart["ara_okunus"]})</em><br><small>{kart["ornek_ar"]}</small></div>'
        f'<div class="flip-back-row">🇧🇩 <strong>Bengalce:</strong> {kart["bengalce"]} <em>({kart["ben_okunus"]})</em><br><small>{kart["ornek_bn"]}</small></div>'
        f'</div>'
        f'<div style="text-align:center;"><span class="flip-hint">🔄 Ön Yüze Dönmek İçin Tekrar Tıkla</span></div>'
        f'</div>'
        f'</div>'
        f'</label>'
    )