#!/bin/bash
# AREX AI — yeni sürüm yayınla: sürümü yükseltir, APK derler, guncelleme.json'u günceller, GitHub'a gönderir
# ve APK'yı GitHub Releases'a "AREX-AI.apk" adıyla yükler → telefondaki AREX "Yeni sürüm hazır" der.
# Gerekli: depoya yazma izni + GITHUB_TOKEN (repo yetkili kişisel erişim anahtarı) — ~/.arex/github_token dosyasında da olabilir.
set -e
cd "$(dirname "$0")"
TOKEN="${GITHUB_TOKEN:-$(cat ~/.arex/github_token 2>/dev/null || true)}"
[ -n "$TOKEN" ] || { echo "GITHUB_TOKEN yok (~/.arex/github_token dosyasına koyabilirsin)."; read -r; exit 1; }
ESKI=$(grep -o '"kod": *[0-9]*' guncelleme.json | grep -o '[0-9]*')
KOD=$((ESKI + 1)); SURUM="15.$((KOD - 150)).0"
echo "Yeni sürüm: $SURUM (kod $KOD)"
sed -i '' "s/version: \"[0-9.]*\"/version: \"$SURUM\"/; s/versionCode: [0-9]*/versionCode: $KOD/; s/surumKodu: [0-9]*/surumKodu: $KOD/" mobil/app.config.js
python3 - "$SURUM" "$KOD" <<'PY'
import json, sys
d = json.load(open("guncelleme.json")); d["surum"], d["kod"] = sys.argv[1], int(sys.argv[2])
json.dump(d, open("guncelleme.json", "w"), ensure_ascii=False, indent=2)
PY
export JAVA_HOME=$(/usr/libexec/java_home -v 21) ANDROID_HOME=$HOME/Library/Android/sdk
( cd mobil && node scripts/html-gom.js && npx expo prebuild --platform android --clean --no-install >/dev/null \
  && sed -i '' 's/^reactNativeArchitectures=.*/reactNativeArchitectures=arm64-v8a/' android/gradle.properties \
  && cd android && NODE_ENV=production ./gradlew assembleRelease --no-daemon -q )
APK=mobil/android/app/build/outputs/apk/release/app-release.apk
cp "$APK" ~/Desktop/AREX-AI-v$SURUM.apk
git add -A mobil guncelleme.json && git commit -q -m "Sürüm $SURUM" && git push origin master
DEPO="ahmettalhakuci-sketch/arex-ai"
SURUM_ID=$(curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$DEPO/releases" -d "{\"tag_name\":\"v$SURUM\",\"name\":\"AREX AI $SURUM\",\"make_latest\":\"true\"}" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/vnd.android.package-archive" \
  --data-binary @"$APK" "https://uploads.github.com/repos/$DEPO/releases/$SURUM_ID/assets?name=AREX-AI.apk" >/dev/null
echo "✅ $SURUM yayınlandı. Telefondaki AREX açılışta yeni sürümü görecek."
read -r -p "Kapatmak için Enter…"
