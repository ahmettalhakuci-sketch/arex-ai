#!/bin/bash
# AREX "AREX" uyandırma + ses imzası modelleri (Vosk, Apache-2.0) — git'e girmez; derlemeden önce bir kez çalıştır.
set -e
A="$(dirname "$0")/../modules/arex-erisim/android/src/main/assets"; mkdir -p "$A"; T=$(mktemp -d)
[ -f "$A/vosk-en/uuid" ] || { curl -sL -o $T/en.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && unzip -q $T/en.zip -d $T && rm -rf "$A/vosk-en" && mv $T/vosk-model-small-en-us-0.15 "$A/vosk-en" && rm -f "$A/vosk-en/README" && echo "en-0.15-arex1" > "$A/vosk-en/uuid"; }
[ -f "$A/vosk-spk/uuid" ] || { curl -sL -o $T/spk.zip https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip && unzip -q $T/spk.zip -d $T && rm -rf "$A/vosk-spk" && mv $T/vosk-model-spk-0.4 "$A/vosk-spk" && rm -f "$A/vosk-spk/README" && echo "spk-0.4-arex1" > "$A/vosk-spk/uuid"; }
[ -f "$A/spk-guclu.onnx" ] || curl -sL -o "$A/spk-guclu.onnx" https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/3dspeaker_speech_eres2net_sv_en_voxceleb_16k.onnx
L="$(dirname "$0")/../modules/arex-erisim/android/maven/com/k2fsa/sherpa-onnx/2.0.3"; mkdir -p "$L"
[ -f "$L/sherpa-onnx-2.0.3.pom" ] || printf '<?xml version="1.0"?><project xmlns="http://maven.apache.org/POM/4.0.0"><modelVersion>4.0.0</modelVersion><groupId>com.k2fsa</groupId><artifactId>sherpa-onnx</artifactId><version>2.0.3</version><packaging>aar</packaging></project>' > "$L/sherpa-onnx-2.0.3.pom"
[ -f "$L/sherpa-onnx-2.0.3.aar" ] || curl -sL -o "$L/sherpa-onnx-2.0.3.aar" https://github.com/k2-fsa/sherpa-onnx/releases/download/v2.0.3/sherpa-onnx-static-link-onnxruntime-2.0.3.aar
rm -rf $T; echo "Ses modelleri hazır: $A"
