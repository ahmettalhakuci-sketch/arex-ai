#!/bin/bash
# AREX AI — APK'yı telefona aktar: bu Mac'te küçük bir indirme sayfası açar.
# Telefon AYNI Wi-Fi'de olmalı. Telefonun tarayıcısında ekranda yazan adresi aç → "İndir" → "Yükle".
cd "$(dirname "$0")"
APK="mobil/android/app/build/outputs/apk/release/app-release.apk"
[ -f "$APK" ] || APK=$(ls -t ~/Desktop/AREX-AI-v*.apk 2>/dev/null | head -1)
if [ ! -f "$APK" ]; then echo "APK bulunamadı."; read -r; exit 1; fi
SURUM=$(grep -o '"surum": *"[^"]*"' guncelleme.json | cut -d'"' -f4)
KLASOR=$(mktemp -d)
cp "$APK" "$KLASOR/AREX-AI.apk"
BOYUT=$(du -m "$KLASOR/AREX-AI.apk" | cut -f1)
cat > "$KLASOR/index.html" <<HTML
<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AREX AI indir</title><style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:-apple-system,Roboto,sans-serif;
background:radial-gradient(120% 80% at 50% 0%,#1a1550,#0b1030 45%,#050816);color:#eef2ff}
.k{max-width:380px;margin:20px;padding:28px;border-radius:28px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);text-align:center}
.l{width:86px;height:86px;border-radius:50%;margin:0 auto 14px;background:linear-gradient(135deg,#7c5cff,#22d3ee);display:flex;align-items:center;justify-content:center;font-size:40px;box-shadow:0 0 50px #7c5cff88}
a.b{display:block;margin:20px 0 14px;padding:16px;border-radius:18px;background:linear-gradient(135deg,#7c5cff,#22d3ee);color:#fff;font-weight:800;font-size:18px;text-decoration:none}
p{color:#a3abcf;font-size:14px;line-height:1.5;text-align:left}
</style></head><body><div class="k"><div class="l">⚡</div><h2 style="margin:0">AREX AI</h2><div style="color:#a3abcf">Sürüm $SURUM • $BOYUT MB</div>
<a class="b" href="AREX-AI.apk" download>⬇️ İndir</a>
<p>1. İndirme bitince bildirimden dosyaya dokun.<br>2. "Bilinmeyen uygulamalar" izni sorulursa <b>izin ver</b>.<br>3. Play Protect uyarırsa <b>Yine de yükle</b>.<br>
4. Eski sürüm yüklüyse üzerine kurulur, verilerin silinmez.</p></div></body></html>
HTML
IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)
echo ""
echo "📱 Telefonun tarayıcısında şu adresi aç (aynı Wi-Fi):"
echo ""
echo "      http://$IP:8600"
echo ""
echo "Bitince bu pencereyi kapat (paylaşım durur)."
cd "$KLASOR" && exec python3 -m http.server 8600 --bind 0.0.0.0
