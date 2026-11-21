#!/bin/bash
# GitHub erişim anahtarını (token) güvenli biçimde kaydeder: ~/.arex/github_token (yalnızca senin okuyabileceğin izinlerle).
# Yazdığın anahtar ekranda GÖRÜNMEZ.
mkdir -p ~/.arex && chmod 700 ~/.arex
echo "GitHub anahtarını yapıştır (ekranda görünmeyecek) ve Enter'a bas:"
read -r -s ANAHTAR
ANAHTAR=$(echo "$ANAHTAR" | tr -d '[:space:]')
if [[ "$ANAHTAR" != github_pat_* && "$ANAHTAR" != ghp_* ]]; then
  echo "⚠️ Bu bir GitHub anahtarına benzemiyor (github_pat_… veya ghp_… ile başlamalı). Kaydedilmedi."
else
  printf "%s" "$ANAHTAR" > ~/.arex/github_token && chmod 600 ~/.arex/github_token
  KOD=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $ANAHTAR" https://api.github.com/repos/ahmettalhakuci-sketch/arex-ai)
  [ "$KOD" = "200" ] && echo "✅ Kaydedildi ve arex-ai deposuna erişim doğrulandı." || echo "⚠️ Kaydedildi ama depo erişimi doğrulanamadı (HTTP $KOD) — anahtarın arex-ai'ye Contents: Read and write izni olmalı."
fi
unset ANAHTAR
read -r -p "Kapatmak için Enter…"
