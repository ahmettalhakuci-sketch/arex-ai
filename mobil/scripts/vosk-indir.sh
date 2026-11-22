#!/bin/bash
# AREX "AREX" uyandırma + ses imzası modelleri (Vosk, Apache-2.0) — git'e girmez; derlemeden önce bir kez çalıştır.
set -e
A="$(dirname "$0")/../modules/arex-erisim/android/src/main/assets"; mkdir -p "$A"; T=$(mktemp -d)
[ -f "$A/vosk-en/uuid" ] || { curl -sL -o $T/en.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && unzip -q $T/en.zip -d $T && rm -rf "$A/vosk-en" && mv $T/vosk-model-small-en-us-0.15 "$A/vosk-en" && rm -f "$A/vosk-en/README" && echo "en-0.15-arex1" > "$A/vosk-en/uuid"; }
[ -f "$A/vosk-spk/uuid" ] || { curl -sL -o $T/spk.zip https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip && unzip -q $T/spk.zip -d $T && rm -rf "$A/vosk-spk" && mv $T/vosk-model-spk-0.4 "$A/vosk-spk" && rm -f "$A/vosk-spk/README" && echo "spk-0.4-arex1" > "$A/vosk-spk/uuid"; }
rm -rf $T; echo "Vosk modelleri hazır: $A"
