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

/** Hızlı eylemler: [simge, ad, komut, renk] */
const EYLEMLER: [string, string, string, string][] = [
  ["document-text", "Özetle", "ekranı özetle", "#7aa7ff"], ["arrow-back", "Geri", "geri", "#c4b5fd"], ["home", "Ana ekran", "ana ekran", "#5eead4"],
  ["notifications", "Bildirim", "bildirimleri aç", "#fbbf24"], ["chevron-down-circle", "Kaydır", "aşağı kaydır", "#f9a8d4"], ["shield-checkmark", "İzinler", "#izin", "#a78bfa"],
];
const selam = () => { const h = new Date().getHours(); return h < 6 ? "İyi geceler 🌙" : h < 12 ? "Günaydın ☀️" : h < 18 ? "Merhaba 👋" : "İyi akşamlar 🌆"; };
const PARILTI = ["#4f8cff", "#a259ff", "#ff5fa2", "#ffb84d", "#4f8cff"] as const;

/** Uygulamaya derin bağlantı: arex://canli, arex://sohbet?m=…&c=… */
export function anaUygulamayiAc(yol: string) { Linking.openURL("arex://" + yol).catch(() => {}); }
/** Asistan kartından ana sohbete aktarılacak mesaj. İki pencere aynı JS motorunu paylaştığından bellekte taşınır;
 * URL'e konmaz (aksi halde herhangi bir site arex://sohbet?c=… ile sahte "AREX cevabı" ekleyebilirdi). */
export const bekleyenSohbet: { deger: { metin: string; cevap: string } | null } = { deger: null };
const kapatPencere = () => { if (Platform.OS === "android") BackHandler.exitApp(); };

function Panel() {
  const ic = useSafeAreaInsets();
  const H = Dimensions.get("window").height;
  const yukseklik = Math.min(540, H * 0.56);  // yalnız Canlı (ses+kamera) açıkken
  const y = useRef(new Animated.Value(yukseklik + 40)).current;
  const perde = useRef(new Animated.Value(0)).current;
  const isilti = useRef(new Animated.Value(0)).current;
  const [hazir, setHazir] = useState(false);
  const [kilitli, setKilitli] = useState(false);
  const kapaniyor = useRef(false);
  const [komut, setKomut] = useState("");
  const [sonuc, setSonuc] = useState("");
  const [isliyor, setIsliyor] = useState(false);
  /** Varsayılan: küçük komut çubuğu. 🎙 ya da yukarı kaydır → Canlı sohbet (kart büyür) */
  const [canli, setCanli] = useState(false);
  const canliRef = useRef(false);
  const canliAc = () => { titret(); canliRef.current = true; setCanli(true); };
  const calistir = async (k: string) => {
    if (!k.trim() || isliyor) return;
    if (kilitli) { canliAc(); return; }  // kilitliyken telefon komutu yok: önce kilidi aç
    titret(); setIsliyor(true); setKomut("");
    const r = await telefonKomutu(k).catch(() => null);
    setSonuc(r ? r.replace(/[#*_>]/g, "").trim() : "Bunu telefon komutu olarak anlayamadım. Sesli sormak için aşağıdaki Canlı asistanı kullan.");
    setIsliyor(false);
  };

  useEffect(() => {
    Promise.all([anahtarlariYukle(), kilitAcikMi().then(setKilitli)]).finally(() => setHazir(true));
    Erisim.onar().catch(() => {});  // yan tuşla açılınca servis bağlantısını tazele
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
  /** ⤢ Büyüt: ana AREX'i Canlı sekmesinde açar. Bu pencere, ana uygulama öne gelince yerel tarafta (onStop) kendiliğinden kapanır —
   * erken kapatmak ortak React motorunu durdurup ana uygulamayı donduruyordu. */
  const gecis = useRef(false);
  const anaya = (yol: string) => {
    if (gecis.current) return;
    gecis.current = true; titret();
    Animated.timing(perde, { toValue: 0, duration: 120, useNativeDriver: true }).start();
    anaUygulamayiAc(yol);
  };
  const buyut = () => anaya("canli");
  const sohbeteGonder = (m: string, c: string) => { bekleyenSohbet.deger = { metin: m, cevap: c.slice(0, 6000) }; anaya("sohbet"); };

  const surukle = useRef(PanResponder.create({
    onMoveShouldSetPanResponder: (_e, g) => Math.abs(g.dy) > 6,
    onPanResponderMove: (_e, g) => y.setValue(Math.max(-60, g.dy)),
    onPanResponderRelease: (_e, g) => {
      if (g.dy < -50) { if (canliRef.current) buyut(); else { canliAc(); Animated.spring(y, { toValue: 0, useNativeDriver: true }).start(); } }
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
        <View style={{ height: canli ? yukseklik : undefined, borderRadius: 28, overflow: "hidden", backgroundColor: "#0a0e22", margin: 1.5 }}>
          <View {...surukle.panHandlers} style={{ paddingTop: 7, paddingBottom: 2, paddingHorizontal: 14 }}>
            <View style={{ alignSelf: "center", width: 34, height: 4, borderRadius: 2, backgroundColor: "rgba(255,255,255,0.22)", marginBottom: 8 }} />
            <View style={{ flexDirection: "row", alignItems: "center", gap: 10 }}>
              <LinearGradient colors={["#4f8cff", "#a259ff", "#ff5fa2"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ width: 30, height: 30, borderRadius: 15, alignItems: "center", justifyContent: "center" }}>
                <Ionicons name="sparkles" size={15} color="#fff" />
              </LinearGradient>
              <View style={{ flex: 1 }}>
                <Text style={{ color: "#fff", fontWeight: "800", fontSize: 15.5, letterSpacing: 0.2 }}>{canli ? "AREX Canlı" : selam()}</Text>
                <Text style={{ color: "#8f98c4", fontSize: 11.5 }}>{canli ? "Ses ve kamera ile konuş" : "Ne yapmamı istersin?"}</Text>
              </View>
              <Pressable onPress={buyut} hitSlop={10} style={st.yuvarlak}><Ionicons name="open-outline" size={15} color="#cfd5f5" /></Pressable>
              <Pressable onPress={kapat} hitSlop={10} style={st.yuvarlak}><Ionicons name="close" size={17} color="#cfd5f5" /></Pressable>
            </View>
          </View>
          {!canli ? (
            <View style={{ paddingHorizontal: 12, paddingTop: 10, paddingBottom: 12 }}>
              {/* Hızlı eylemler: simgeli döşemeler (Erişilebilirlik ile arkadaki uygulamaya etki eder) */}
              <View style={{ flexDirection: "row", justifyContent: "space-between" }}>
                {EYLEMLER.map(([ikon, ad, k, renk]) => (
                  <Pressable key={k} onPress={() => (k === "#izin" ? anaya("ayarlar") : calistir(k))} style={({ pressed }) => ({ alignItems: "center", width: "16%", opacity: pressed ? 0.6 : 1, transform: [{ scale: pressed ? 0.94 : 1 }] })}>
                    <View style={{ width: 44, height: 44, borderRadius: 15, alignItems: "center", justifyContent: "center", backgroundColor: renk + "22", borderWidth: 1, borderColor: renk + "55" }}>
                      <Ionicons name={ikon as any} size={20} color={renk} />
                    </View>
                    <Text numberOfLines={1} style={{ color: "#c9cfee", fontSize: 10.5, fontWeight: "600", marginTop: 4 }}>{ad}</Text>
                  </Pressable>
                ))}
              </View>
              {/* Komut kutusu: boşken mikrofon (Canlı), yazınca gönder */}
              <LinearGradient colors={["rgba(79,140,255,0.55)", "rgba(162,89,255,0.55)", "rgba(255,95,162,0.55)"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={{ borderRadius: 24, padding: 1.2, marginTop: 12 }}>
                <View style={{ flexDirection: "row", alignItems: "center", backgroundColor: "#121733", borderRadius: 23, paddingLeft: 14, paddingRight: 5, paddingVertical: 4 }}>
                  <TextInput value={komut} onChangeText={setKomut} onSubmitEditing={() => calistir(komut)} returnKeyType="send" onFocus={() => { if (kilitli) canliAc(); }}
                    placeholder={kilitli ? "🔒 AREX kilitli — açmak için dokun" : "AREX'e sor ya da komut ver…"} placeholderTextColor="#7d86ad"
                    style={{ flex: 1, color: "#fff", fontSize: 14, paddingVertical: 7 }} />
                  <Pressable onPress={() => (komut.trim() ? calistir(komut) : canliAc())} hitSlop={6}>
                    <LinearGradient colors={["#4f8cff", "#a259ff", "#ff5fa2"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ width: 36, height: 36, borderRadius: 18, alignItems: "center", justifyContent: "center" }}>
                      {isliyor ? <ActivityIndicator color="#fff" size="small" /> : <Ionicons name={komut.trim() ? "arrow-up" : "mic"} size={18} color="#fff" />}
                    </LinearGradient>
                  </Pressable>
                </View>
              </LinearGradient>
              {sonuc ? (
                <ScrollView style={{ maxHeight: 110, marginTop: 10 }} contentContainerStyle={{ flexDirection: "row", gap: 8, backgroundColor: "rgba(255,255,255,0.05)", borderRadius: 16, padding: 11, borderWidth: 1, borderColor: "rgba(255,255,255,0.08)" }}>
                  <Ionicons name="sparkles" size={14} color="#a259ff" style={{ marginTop: 2 }} />
                  <Text style={{ color: "#e6e9ff", fontSize: 13, lineHeight: 19, flex: 1 }}>{sonuc}</Text>
                </ScrollView>
              ) : Erisim.destekVar() && !Erisim.etkinMi() ? (
                <Pressable onPress={() => Erisim.ayarAc("erisim")} style={{ flexDirection: "row", alignItems: "center", gap: 6, marginTop: 9, alignSelf: "center" }}>
                  <Ionicons name="alert-circle" size={14} color="#ffb84d" />
                  <Text style={{ color: "#ffb84d", fontSize: 12, fontWeight: "600" }}>Ekrana dokunma/okuma kapalı • Aç ›</Text>
                </Pressable>
              ) : null}
            </View>
          ) : (
          <View style={{ flex: 1 }}>
            {!hazir ? <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}><ActivityIndicator color={R.acc2} /></View>
              : kilitli ? <KilitEkrani acildi={() => setKilitli(false)} />
              : <CanliEkrani mini sohbeteGonder={sohbeteGonder} />}
          </View>
          )}
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
  cip: { paddingHorizontal: 10, paddingVertical: 6, borderRadius: 999, backgroundColor: "rgba(255,255,255,0.07)", borderWidth: 1, borderColor: "rgba(255,255,255,0.12)" },
  yuvarlak: { width: 30, height: 30, borderRadius: 15, backgroundColor: "rgba(255,255,255,0.08)", alignItems: "center", justifyContent: "center" },
});
