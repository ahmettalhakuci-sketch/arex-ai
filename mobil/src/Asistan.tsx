// AREX — Yan tuş asistanı (Gemini tarzı): uygulama tam ekran AÇILMAZ. Android'de ayrı, şeffaf bir pencerede (AsistanActivity,
// kök bileşen "asistan") o an kullandığın uygulamanın ÜSTÜNDE alttan yüzen bir kart açılır; arkadaki ekran görünür kalır.
// Dışarı dokun / aşağı kaydır / geri tuşu → kapanır. ⤢ ya da yukarı kaydır → AREX'i Canlı sekmesinde açar.
import { Ionicons } from "@expo/vector-icons";
import { StatusBar } from "expo-status-bar";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, Animated, ScrollView, TextInput, BackHandler, Dimensions, Easing, Linking, PanResponder, Platform, Pressable, StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider, useSafeAreaInsets } from "react-native-safe-area-context";
import * as Erisim from "../modules/arex-erisim";
import { AyarSaglayici } from "./ayar";
import { telefonKomutu } from "./telefon";
import { anahtarlariYukle } from "./depo";
import CanliEkrani from "./ekranlar/Canli";
import KilitEkrani, { kilitAcikMi } from "./Kilit";
import { R } from "./tema";
import { titret } from "./ui";

const PARILTI = ["#4f8cff", "#a259ff", "#ff5fa2", "#ffb84d", "#4f8cff"] as const;

/** Uygulamaya derin bağlantı: arex://canli, arex://sohbet?m=…&c=… */
export function anaUygulamayiAc(yol: string) { Linking.openURL("arex://" + yol).catch(() => {}); }
const kapatPencere = () => { if (Platform.OS === "android") BackHandler.exitApp(); };

function Panel() {
  const ic = useSafeAreaInsets();
  const H = Dimensions.get("window").height;
  const yukseklik = Math.min(640, H * 0.66);
  const y = useRef(new Animated.Value(yukseklik + 40)).current;
  const perde = useRef(new Animated.Value(0)).current;
  const isilti = useRef(new Animated.Value(0)).current;
  const [hazir, setHazir] = useState(false);
  const [kilitli, setKilitli] = useState(false);
  const kapaniyor = useRef(false);
  const [komut, setKomut] = useState("");
  const [sonuc, setSonuc] = useState("");
  const [isliyor, setIsliyor] = useState(false);
  const calistir = async (k: string) => {
    if (!k.trim() || isliyor) return;
    titret(); setIsliyor(true); setKomut("");
    const r = await telefonKomutu(k).catch(() => null);
    setSonuc(r ? r.replace(/[#*_>]/g, "").trim() : "Bunu telefon komutu olarak anlayamadım. Sesli sormak için aşağıdaki Canlı asistanı kullan.");
    setIsliyor(false);
  };

  useEffect(() => {
    Promise.all([anahtarlariYukle(), kilitAcikMi().then(setKilitli)]).finally(() => setHazir(true));
    Animated.parallel([
      Animated.spring(y, { toValue: 0, useNativeDriver: true, damping: 18, stiffness: 180, mass: 0.9 }),
      Animated.timing(perde, { toValue: 1, duration: 260, useNativeDriver: true }),
    ]).start();
    const dongu = Animated.loop(Animated.timing(isilti, { toValue: 1, duration: 2600, easing: Easing.inOut(Easing.sin), useNativeDriver: true }));
    dongu.start();
    const geri = BackHandler.addEventListener("hardwareBackPress", () => { kapat(); return true; });
    return () => { dongu.stop(); geri.remove(); };
  }, []);

  const kapat = () => {
    if (kapaniyor.current) return;
    kapaniyor.current = true;
    Animated.parallel([
      Animated.timing(y, { toValue: yukseklik + 60, duration: 200, easing: Easing.in(Easing.quad), useNativeDriver: true }),
      Animated.timing(perde, { toValue: 0, duration: 200, useNativeDriver: true }),
    ]).start(kapatPencere);
  };
  const buyut = () => { titret(); anaUygulamayiAc("canli"); setTimeout(kapatPencere, 150); };
  const sohbeteGonder = (m: string, c: string) => { anaUygulamayiAc(`sohbet?m=${encodeURIComponent(m)}&c=${encodeURIComponent(c.slice(0, 6000))}`); setTimeout(kapatPencere, 150); };

  const surukle = useRef(PanResponder.create({
    onMoveShouldSetPanResponder: (_e, g) => Math.abs(g.dy) > 6,
    onPanResponderMove: (_e, g) => y.setValue(Math.max(-60, g.dy)),
    onPanResponderRelease: (_e, g) => {
      if (g.dy < -50) buyut();
      else if (g.dy > 90 || g.vy > 1.2) kapat();
      else Animated.spring(y, { toValue: 0, useNativeDriver: true }).start();
    },
  })).current;

  const parlaklik = isilti.interpolate({ inputRange: [0, 0.5, 1], outputRange: [0.55, 1, 0.55] });
  return (
    <View style={StyleSheet.absoluteFill}>
      <StatusBar style="light" />
      {/* Arkadaki uygulama görünür kalır; yalnız alt kısım hafifçe kararır */}
      <Animated.View style={[StyleSheet.absoluteFill, { opacity: perde }]} pointerEvents="none">
        <LinearGradient colors={["rgba(0,0,0,0)", "rgba(0,0,0,0.18)", "rgba(0,0,0,0.55)"]} locations={[0, 0.45, 1]} style={StyleSheet.absoluteFill} />
      </Animated.View>
      <Pressable style={{ flex: 1 }} onPress={kapat} />
      <Animated.View style={{ transform: [{ translateY: y }], marginHorizontal: 8, marginBottom: Math.max(ic.bottom, 8) }}>
        {/* Gemini tarzı renkli ışıltı */}
        <Animated.View pointerEvents="none" style={{ position: "absolute", left: -2, right: -2, top: -2, bottom: -2, borderRadius: 32, opacity: parlaklik }}>
          <LinearGradient colors={PARILTI as any} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ flex: 1, borderRadius: 32 }} />
        </Animated.View>
        <View style={{ height: yukseklik, borderRadius: 30, overflow: "hidden", backgroundColor: "#0b0f24", margin: 1.5 }}>
          <View {...surukle.panHandlers} style={{ paddingTop: 8, paddingBottom: 6, paddingHorizontal: 14 }}>
            <View style={{ alignSelf: "center", width: 40, height: 4.5, borderRadius: 3, backgroundColor: "rgba(255,255,255,0.28)", marginBottom: 8 }} />
            <View style={{ flexDirection: "row", alignItems: "center", gap: 10 }}>
              <LinearGradient colors={["#4f8cff", "#a259ff", "#ff5fa2"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ width: 30, height: 30, borderRadius: 10, alignItems: "center", justifyContent: "center" }}>
                <Ionicons name="sparkles" size={16} color="#fff" />
              </LinearGradient>
              <View style={{ flex: 1 }}>
                <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16 }}>AREX</Text>
                <Text style={{ color: "#9aa3c7", fontSize: 11.5 }}>Seni dinliyorum…</Text>
              </View>
              <Pressable onPress={buyut} hitSlop={10} style={st.yuvarlak}><Ionicons name="expand" size={17} color="#fff" /></Pressable>
              <Pressable onPress={kapat} hitSlop={10} style={st.yuvarlak}><Ionicons name="close" size={19} color="#fff" /></Pressable>
            </View>
          </View>
          {/* Hızlı telefon komutları (Erişilebilirlik servisiyle arkadaki uygulamaya etki eder) */}
          {Erisim.destekVar() ? (
            <View style={{ paddingHorizontal: 12, paddingBottom: 6 }}>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 6 }} keyboardShouldPersistTaps="handled">
                {([["📖 Ekranı özetle", "ekranı özetle"], ["⬅️ Geri", "geri"], ["🏠 Ana ekran", "ana ekran"], ["🔔 Bildirimler", "bildirimleri aç"], ["⬇️ Kaydır", "aşağı kaydır"]] as const).map(([ad, k]) => (
                  <Pressable key={k} onPress={() => calistir(k)} style={st.cip}><Text style={{ color: "#fff", fontSize: 12.5, fontWeight: "700" }}>{ad}</Text></Pressable>
                ))}
              </ScrollView>
              <View style={{ flexDirection: "row", alignItems: "center", gap: 8, marginTop: 8 }}>
                <TextInput value={komut} onChangeText={setKomut} onSubmitEditing={() => calistir(komut)} returnKeyType="send" placeholder="Komut yaz: Gönder'e dokun, yaz: merhaba, google aç…" placeholderTextColor="#7d86ad"
                  style={{ flex: 1, color: "#fff", backgroundColor: "rgba(255,255,255,0.06)", borderRadius: 14, borderWidth: 1, borderColor: "rgba(255,255,255,0.12)", paddingHorizontal: 12, paddingVertical: 8, fontSize: 13.5 }} />
                <Pressable onPress={() => calistir(komut)} style={[st.yuvarlak, { backgroundColor: "#a259ff" }]}>
                  {isliyor ? <ActivityIndicator color="#fff" size="small" /> : <Ionicons name="arrow-up" size={18} color="#fff" />}
                </Pressable>
              </View>
              {sonuc ? (
                <ScrollView style={{ maxHeight: 110, marginTop: 8 }} contentContainerStyle={{ backgroundColor: "rgba(162,89,255,0.12)", borderRadius: 12, padding: 10 }}>
                  <Text style={{ color: "#e6e9ff", fontSize: 13, lineHeight: 19 }}>{sonuc}</Text>
                </ScrollView>
              ) : !Erisim.etkinMi() ? (
                <Pressable onPress={() => Erisim.ayarlariAc()}><Text style={{ color: "#ffb84d", fontSize: 12, marginTop: 6 }}>♿ Ekrana dokunma/okuma için erişimi aç → dokun</Text></Pressable>
              ) : null}
            </View>
          ) : null}
          <View style={{ flex: 1 }}>
            {!hazir ? <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}><ActivityIndicator color={R.acc2} /></View>
              : kilitli ? <KilitEkrani acildi={() => setKilitli(false)} />
              : <CanliEkrani mini sohbeteGonder={sohbeteGonder} />}
          </View>
        </View>
      </Animated.View>
    </View>
  );
}

export default function AsistanKoku() {
  return (
    <SafeAreaProvider style={{ backgroundColor: "transparent" }}>
      <AyarSaglayici>
        <Panel />
      </AyarSaglayici>
    </SafeAreaProvider>
  );
}

const st = StyleSheet.create({
  cip: { paddingHorizontal: 12, paddingVertical: 7, borderRadius: 999, backgroundColor: "rgba(255,255,255,0.07)", borderWidth: 1, borderColor: "rgba(255,255,255,0.12)" },
  yuvarlak: { width: 34, height: 34, borderRadius: 17, backgroundColor: "rgba(255,255,255,0.08)", alignItems: "center", justifyContent: "center" },
});
