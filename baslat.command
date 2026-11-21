#!/bin/bash
# AREX AI — çift tıkla başlat (macOS).
#  • Premium masaüstü uygulamasını (AREX AI.app) açar.
#  • Klasik Streamlit sürümü de arka planda çalışır (telefondan aynı Wi-Fi ile tarayıcıdan açmak için).
cd "$(dirname "$0")"
UYGULAMA="masaustu/cikti/AREX AI-darwin-arm64/AREX AI.app"
if [ -d "$UYGULAMA" ]; then
  open "$UYGULAMA"
  echo "✨ AREX AI masaüstü uygulaması açıldı."
fi
if [ ! -x .venv/bin/streamlit ]; then
  echo "İlk kurulum yapılıyor (bir kez, 1-2 dakika)…"
  /usr/bin/python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt || { echo "Kurulum başarısız"; read -r; exit 1; }
fi
IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)
echo ""
echo "⚡ Klasik AREX (Streamlit) de hazırlanıyor…"
echo "   Bilgisayarda : http://localhost:8501"
[ -n "$IP" ] && echo "   Telefonda    : http://$IP:8501   (aynı Wi-Fi'de olmalı; en iyisi AREX APK'sını kurmak)"
echo "   Kapatmak için bu pencereyi kapat."
echo ""
if lsof -nP -iTCP:8501 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "(Klasik sürüm zaten çalışıyor.)"
  read -r -p "Kapatmak için Enter'a bas…"
  exit 0
fi
[ -d "$UYGULAMA" ] || ( sleep 4; open "http://localhost:8501" ) &
exec .venv/bin/streamlit run main.py --server.port 8501 --server.headless true
