# ⚡ AREX AI Studio

Türkçe, mobil öncelikli kişisel yapay zekâ asistanı. Python + Streamlit ile yazıldı; telefonda
uygulama gibi (ana ekrana eklenerek), bilgisayarda masaüstü düzeninde çalışır. Yapay zekâ için
ücretsiz **Groq** kullanır; diğer tüm kaynaklar ücretsiz ve anahtarsızdır.

## Neler yapabilir?

| Alan | Örnek |
|---|---|
| 💬 Sohbet (Groq GPT-OSS 120B + Wikipedia bağlamı) | *"fotosentez nedir kısaca anlat"*, *"peki bitkiler geceleri ne yapar"* |
| 🧮 Profesyonel matematik | *"2+3*4"*, *"√27 + √3"*, *"sin 45"*, *"3(x-2)=x+4"*, *"x^2-5x+6=0"*, *"120'nin asal çarpanları"* |
| 📈 Grafik çizici | *"y = x^2 - 4 grafiğini çiz"*, *"y = sin(x) grafiği"* |
| 📸 Fotoğraftan soru | 📎 Fotoğraf / Video → soru fotoğrafı (Tesseract OCR + Groq, şık sağlamalı) |
| 🎬 Video / ses özeti | 📎 Fotoğraf / Video → MP4/MP3 (Groq Whisper) · sohbete YouTube bağlantısı |
| 🎤 Sesli soru | Sohbetin altındaki mikrofon (Groq Whisper) |
| 📊 Çalışma koçu | *"bugün 30 matematik sorusu çözdüm"*, *"bu hafta ne kadar çalıştım"*, *"günlük hedefim 50 soru"* |
| 📝 Sohbet içi test | *"bana 5 matematik sorusu sor"* (130 soruluk banka, ipucu · geç · testi bitir) |
| 🧮 Net hesaplama | *"40 doğru 12 yanlış kaç net"*, *"lgs 15 doğru 3 yanlış"*, ders ders tablo |
| 📅 Sınav geri sayımı | *"fizik sınavım 5 aralıkta"*, *"sınavlarıma kaç gün kaldı"* (+ çalışma planı önerisi) |
| 🍅 Pomodoro | *"pomodoro başlat"*, *"50 dakika pomodoro"* — süre bitince ekranda hatırlatır |
| 🃏 Kelime kartları | *"kart ekle: apple = elma; book = kitap"*, *"kartları çalış"* (Leitner aralıklı tekrar), *"hazır desteler"* (İngilizce, başkentler, elementler) |
| 📈 Deneme takibi | *"deneme: türkçe 30 doğru 6 yanlış matematik 22 doğru 8 yanlış"* → kaydeder; *"denemelerim"* → gelişim grafiği |
| ⏰ Hatırlatıcı | *"yarın 8'de fizik sınavımı hatırlat"* (+ Google Takvim'e ekle bağlantısı) |
| 🌍 Güncel kaynaklar | Kandilli depremleri, hava durumu, döviz/altın/kripto, haberler, resmî tatiller, Tarihte Bugün |
| 📖 Kur'an & meal | *"bakara 255"*, *"ayetel kürsi"*, *"ihlas suresi"* (Diyanet meali) |
| 📏 Günlük araçlar | birim çevirici, tarih/yaş hesabı, dünya saati, gün doğumu/batımı, İngilizce sözlük, TDK |
| 🎓 Öğretme | *"öğret: favori rengim = lacivert"* — öğretilen cevaplar olasılıklı çeşitlenir |

## Yerelde çalıştırma

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Fotoğraf/video için (macOS): brew install tesseract tesseract-lang ffmpeg
streamlit run main.py
```

`.streamlit/secrets.toml` dosyası (git'e **yüklenmez**):

```toml
GROQ_API_KEY = "gsk_..."        # https://console.groq.com/keys (ücretsiz)
# GEMINI_API_KEY = "AIza..."    # isteğe bağlı: fotoğraf çözümü daha isabetli olur
```

## Telefona kurulum (Streamlit Community Cloud — ücretsiz)

1. Kodu GitHub'a gönder: `git push -u origin mobil-premium-v14`
2. [share.streamlit.io](https://share.streamlit.io) → **New app** → depo, dal `mobil-premium-v14`, dosya `main.py`
3. **Advanced settings → Secrets** kısmına `GROQ_API_KEY = "..."` yaz → **Deploy**
   (`packages.txt` sayesinde Tesseract ve ffmpeg otomatik kurulur)
4. Telefonda adresi Chrome'da aç → ⋮ → **Ana ekrana ekle** → AREX ikonuyla tam ekran açılır
5. İstersen [pwabuilder.com](https://www.pwabuilder.com)'a adresi verip Android paketi (APK/AAB) üretebilirsin

> ⚠️ Bulutta uygulama yeniden başladığında dosyalar sıfırlanabilir. Yan menüdeki
> **💾 Verilerimi Yedekle / Geri Yükle** ile ara sıra yedek indir.

## Testler

```bash
python -m unittest tests/test_arex.py -v
```

İnternet gerektirmez (ağ testte kapatılır); matematik, grafik, çalışma koçu, cevap varyantları,
yedekleme ve sohbet yönlendirmesini doğrular. Kod değiştirdikten sonra çalıştır.

## Modüller

| Dosya | Görev |
|---|---|
| `main.py` | Ana uygulama, sayfa düzeni, sohbet akışı |
| `modul_1_arayuz_ve_tema.py` | Temalar, kartlar |
| `modul_3_veri_ve_kisiler.py` | Kişisel bilgi, özel cevaplar, bilgi bankası |
| `modul_4_matematik_motoru.py` | Matematik stüdyosu, 130 soruluk banka |
| `modul_8_zeka_ve_hibrit_ai.py` | Sohbet motoru ve yönlendirici |
| `modul_9_ollama_ve_tdk.py` | Groq / açık kaynak AI zinciri, TDK |
| `modul_10_wikipedia.py` | Wikipedia araştırma |
| `modul_13_acik_kaynak_bilgi_agi.py` | Hava, döviz, haber, ülke/şehir, tarif |
| `modul_14_pro_matematik.py` | İfade ayrıştırıcı, denklem çözücü, tam köklü sayılar |
| `modul_15_mobil_arayuz.py` | Açılış kapağı, mobil CSS, PWA |
| `modul_16_guncel_asistan.py` | Deprem, tatil, sözlük, Kur'an, gün doğumu, birim/tarih/saat |
| `modul_17_medya_ve_grafik.py` | Grafik, Whisper, OCR, video ve YouTube özeti |
| `modul_18_calisma_kocu.py` | Çalışma takibi, sohbet içi test, hatırlatıcı |
| `modul_19_cevap_varyantlari.py` | Soru genişletme ve olasılıklı cevaplar |
| `modul_20_yedekleme.py` | Kişisel veri yedekleme / geri yükleme |
| `modul_21_ogrenci_araclari.py` | Net hesaplama, deneme takibi, sınav geri sayımı, pomodoro, kelime kartları |
