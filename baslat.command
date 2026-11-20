#!/bin/bash
# AREX AI — çift tıkla başlat (macOS). Telefondan aynı Wi-Fi üzerinden de açılabilir.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/streamlit ]; then
  echo "İlk kurulum yapılıyor (bir kez, 1-2 dakika)…"
  /usr/bin/python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt || { echo "Kurulum başarısız"; read -r; exit 1; }
fi
IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)
echo ""
echo "⚡ AREX AI başlıyor…"
echo "   Bilgisayarda : http://localhost:8501"
[ -n "$IP" ] && echo "   Telefonda    : http://$IP:8501   (aynı Wi-Fi'de olmalı)"
echo "   Kapatmak için bu pencereyi kapat."
echo ""
( sleep 4; open "http://localhost:8501" ) &
exec .venv/bin/streamlit run main.py --server.port 8501 --server.headless true
