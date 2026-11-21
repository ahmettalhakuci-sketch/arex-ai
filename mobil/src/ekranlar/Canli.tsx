// AREX — Canlı: Gemini Live (doğal sesli + kameralı gerçek zamanlı sohbet) ve cihaz içi Yerel Analiz
import { requestRecordingPermissionsAsync } from "expo-audio";
import { Camera } from "expo-camera";
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Platform, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { canliToken } from "../ai";
import { useAyar } from "../ayar";
import { anahtar, profilOku, profilOzeti } from "../depo";
import { CANLI_HTML, YEREL_HTML } from "../gomuluHtml";
import { R } from "../tema";
import { Dugme, Hap, s as us } from "../ui";
import WebSayfa from "../WebSayfa";

export default function CanliEkrani({ sohbeteGonder }: { sohbeteGonder: (metin: string, cevap: string) => void }) {
  const ic = useSafeAreaInsets();
  const { ayar } = useAyar();
  const [sekme, setSekme] = useState<"canli" | "yerel">("canli");
  const [izin, setIzin] = useState(Platform.OS === "web");
  const [cfg, setCfg] = useState<Record<string, unknown> | null>(null);
  const [hata, setHata] = useState("");

  const izinIste = async () => {
    const a = await requestRecordingPermissionsAsync();
    const k = await Camera.requestCameraPermissionsAsync();
    setIzin(a.granted && k.granted);
    if (!a.granted) setHata("Mikrofon izni gerekli (Ayarlar → Uygulamalar → AREX AI → İzinler).");
  };
  useEffect(() => { if (Platform.OS !== "web") izinIste(); }, []);

  const hazirla = async () => {
    setHata(""); setCfg(null);
    if (!anahtar("GEMINI_API_KEY")) { setHata("Canlı sohbet için Gemini anahtarı gerekli (⚙️ Ayarlar)."); return; }
    const t = await canliToken();
    const [p, oz] = await Promise.all([profilOku(), profilOzeti()]);
    // Geçici token alınamazsa doğrudan anahtarla (yalnızca bu cihazda) bağlanır
    setCfg({ ...(t ? { t } : { k: anahtar("GEMINI_API_KEY") }), mod: ayar.cocukModu ? "cocuk" : "asistan", dil: ayar.yanitDili, yas: ayar.yas, profil: oz, ad: p.ad });
  };
  useEffect(() => { if (sekme === "canli" && izin && !cfg) hazirla(); }, [sekme, izin]);

  return (
    <View style={{ flex: 1, paddingTop: ic.top }}>
      <View style={{ flexDirection: "row", gap: 8, padding: 10, paddingBottom: 6 }}>
        <Hap yazi="🎙️ Canlı Sohbet (ses + kamera)" secili={sekme === "canli"} onPress={() => setSekme("canli")} />
        <Hap yazi="🧠 Yerel Analiz (cihaz içi)" secili={sekme === "yerel"} onPress={() => setSekme("yerel")} />
      </View>
      {!izin ? (
        <View style={{ padding: 20 }}>
          <Text style={us.alt}>Canlı sohbet ve yüz analizi için mikrofon ve kamera izni gerekli.</Text>
          <Dugme yazi="İzin ver" onPress={izinIste} style={{ marginTop: 12 }} />
          {hata ? <Text style={{ color: R.kirmizi, marginTop: 10 }}>{hata}</Text> : null}
        </View>
      ) : sekme === "canli" ? (
        cfg ? <WebSayfa key={JSON.stringify(cfg).length + String(cfg.mod)} html={CANLI_HTML} ayar={cfg} /> : (
          <View style={{ flex: 1, alignItems: "center", justifyContent: "center", padding: 20 }}>
            {hata ? <><Text style={{ color: R.kirmizi, textAlign: "center" }}>{hata}</Text><Dugme yazi="Tekrar dene" onPress={hazirla} style={{ marginTop: 12 }} /></> : <ActivityIndicator color={R.acc2} size="large" />}
          </View>
        )
      ) : (
        <WebSayfa html={YEREL_HTML} onMesaj={(v) => { if (v?.tur === "arex_yerel_rapor") sohbeteGonder("🧠 Yerel analiz raporu", v.rapor); }} />
      )}
    </View>
  );
}
