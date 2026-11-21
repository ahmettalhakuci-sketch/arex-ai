// AREX AI — mobil & masaüstü uygulaması (React Native / Expo)
import { BlurView } from "expo-blur";
import { StatusBar } from "expo-status-bar";
import * as SystemUI from "expo-system-ui";
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Platform, Pressable, StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider, useSafeAreaInsets } from "react-native-safe-area-context";
import { AyarSaglayici, useAyar } from "./src/ayar";
import { anahtarlariYukle } from "./src/depo";
import AnalizEkrani from "./src/ekranlar/Analiz";
import AraclarEkrani from "./src/ekranlar/Araclar";
import AyarlarEkrani from "./src/ekranlar/Ayarlar";
import CanliEkrani from "./src/ekranlar/Canli";
import CocukEkrani from "./src/ekranlar/Cocuk";
import SohbetEkrani from "./src/ekranlar/Sohbet";
import { R } from "./src/tema";
import { Arkaplan, titret } from "./src/ui";

type Sekme = "sohbet" | "canli" | "cocuk" | "analiz" | "araclar" | "ayarlar";
const SEKMELER: [Sekme, string, string][] = [
  ["sohbet", "💬", "Sohbet"], ["canli", "🎙️", "Canlı"], ["cocuk", "🧸", "Çocuk"],
  ["analiz", "🔬", "Analiz"], ["araclar", "🧭", "Araçlar"], ["ayarlar", "⚙️", "Ayarlar"],
];

function Uygulama() {
  const ic = useSafeAreaInsets();
  const { ayar } = useAyar();
  const [sekme, setSekme] = useState<Sekme>("sohbet");
  const [disMesaj, setDisMesaj] = useState<{ metin: string; cevap: string } | null>(null);
  const sohbeteGonder = (metin: string, cevap: string) => { setDisMesaj({ metin, cevap }); setSekme("sohbet"); };
  const ekran = {
    sohbet: <SohbetEkrani disaridanMesaj={disMesaj} temizle={() => setDisMesaj(null)} canliyaGit={() => setSekme("canli")} />,
    canli: <CanliEkrani sohbeteGonder={sohbeteGonder} />,
    cocuk: <CocukEkrani />,
    analiz: <AnalizEkrani sohbeteGonder={sohbeteGonder} />,
    araclar: <AraclarEkrani />,
    ayarlar: <AyarlarEkrani />,
  }[sekme];
  return (
    // tema/yazı boyutu değişince tüm ağaç yeni tonla yeniden çizilir
    <Arkaplan key={ayar.tema + ayar.yaziOlcek}>
      <StatusBar style="light" />
      <View style={{ flex: 1, maxWidth: Platform.OS === "web" ? 980 : undefined, width: "100%", alignSelf: "center" }}>{ekran}</View>
      {ayar.gozKoruma ? <View pointerEvents="none" style={[StyleSheet.absoluteFill, { backgroundColor: "rgba(255,150,40,0.10)", zIndex: 50 }]} /> : null}
      <View style={[st.cubukDis, { paddingBottom: Math.max(ic.bottom, 6) }]}>
        {Platform.OS !== "web" ? <BlurView intensity={40} tint="dark" style={StyleSheet.absoluteFill} /> : null}
        {SEKMELER.map(([k, ikon, ad]) => {
          const secili = sekme === k;
          return (
            <Pressable key={k} style={st.sekme} onPress={() => { titret(); setSekme(k); }}>
              <View style={[st.ikonKap, secili && { backgroundColor: R.hap }]}><Text style={{ fontSize: 20 }}>{ikon}</Text></View>
              <Text style={[st.sekmeYazi, secili && { color: "#fff", fontWeight: "800" }]}>{ad}</Text>
            </Pressable>
          );
        })}
      </View>
    </Arkaplan>
  );
}

export default function App() {
  const [hazir, setHazir] = useState(false);
  useEffect(() => {
    if (Platform.OS === "web" && typeof document !== "undefined") {
      // Masaüstü/web: tarayıcının turuncu odak çerçevesi tasarımı bozmasın; ince kaydırma çubukları
      const st = document.createElement("style");
      st.textContent = "input,textarea{outline:none!important;caret-color:#22d3ee}::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.14);border-radius:8px}::-webkit-scrollbar-track{background:transparent}body{background:#050816}";
      document.head.appendChild(st);
    }
    SystemUI.setBackgroundColorAsync(R.bg1).catch(() => {});
    anahtarlariYukle().finally(() => setHazir(true));
  }, []);
  return (
    <SafeAreaProvider>
      <AyarSaglayici>
        {hazir ? <Uygulama /> : (
          <View style={{ flex: 1, backgroundColor: R.bg1, alignItems: "center", justifyContent: "center" }}>
            <Text style={{ color: "#fff", fontSize: 28, fontWeight: "800", marginBottom: 14 }}>⚡ AREX AI</Text>
            <ActivityIndicator color={R.acc2} />
          </View>
        )}
      </AyarSaglayici>
    </SafeAreaProvider>
  );
}

const st = StyleSheet.create({
  cubukDis: { flexDirection: "row", borderTopWidth: 1, borderTopColor: "rgba(255,255,255,0.08)", paddingTop: 6, backgroundColor: Platform.OS === "web" ? "rgba(5,8,22,0.92)" : "rgba(5,8,22,0.55)", overflow: "hidden" },
  sekme: { flex: 1, alignItems: "center", gap: 2 },
  ikonKap: { paddingHorizontal: 14, paddingVertical: 4, borderRadius: 14 },
  sekmeYazi: { color: R.soluk, fontSize: 11 },
});
