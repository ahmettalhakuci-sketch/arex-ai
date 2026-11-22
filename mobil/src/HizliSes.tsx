// AREX — ⚡ Hızlı Ses Modu: Gemini Live kotasına bağlı değil. Konuş → susunca otomatik durur → Groq Whisper (yazıya döker)
// → Groq/Gemini/OpenRouter/Ollama zinciri (cevap, GEÇMİŞ BAĞLAMLA) → cihaz sesi ANINDA okur → yeniden dinler.
// Telefon komutları ("babamı ara", "YouTube'da … aç") doğrudan yapılır.
import { Ionicons } from "@expo/vector-icons";
import { getRecordingPermissionsAsync, RecordingPresets, requestRecordingPermissionsAsync, setAudioModeAsync, useAudioRecorder, useAudioRecorderState } from "expo-audio";
import { LinearGradient } from "expo-linear-gradient";
import * as Speech from "expo-speech";
import React, { useEffect, useRef, useState } from "react";
import { Animated, Easing, Pressable, ScrollView, Text, View } from "react-native";
import * as Erisim from "../modules/arex-erisim";
import { seseUygun, sesiYaziyaDok, sohbetTamamla, type Rol } from "./ai";
import { profilOzeti } from "./depo";
import { izinIste } from "./izin";
import { telefonKomutu } from "./telefon";
import { titret } from "./ui";

type Faz = "hazir" | "dinliyor" | "dusunuyor" | "konusuyor";
const SES_KURALI = "Sen AREX'sin; kullanıcının yakın dostu gibi SESLİ konuşuyorsun: içten, sıcakkanlı, samimi, gerektiğinde esprili; ona değer verdiğini hissettir. Cevapların kısa (1-3 cümle), doğal konuşma Türkçesi; madde işareti, emoji, markdown, başlık YOK. " +
  "Önceki konuşmayı hatırla ve ona bağlan. Telefonda işlem yaptığını ASLA uydurma (arama, mesaj, uygulama açma vb. senin elinde değil).";

export default function HizliSes({ kisitli = false, otomatik = true }: { kisitli?: boolean; otomatik?: boolean }) {
  const kaydedici = useAudioRecorder({ ...RecordingPresets.HIGH_QUALITY, isMeteringEnabled: true });
  const durum = useAudioRecorderState(kaydedici, 100);
  const [faz, setFaz] = useState<Faz>("hazir");
  const [sen, setSen] = useState("");
  const [arex, setArex] = useState("");
  const [sure, setSure] = useState("");
  const gecmis = useRef<Rol[]>([]);
  const ses = useRef({ konustu: false, sessizBas: 0, bas: 0 });
  const fazRef = useRef<Faz>("hazir"); fazRef.current = faz;
  const kapali = useRef(false);
  const olcek = useRef(new Animated.Value(1)).current;
  const nefes = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const d = Animated.loop(Animated.timing(nefes, { toValue: 1, duration: 2400, easing: Easing.inOut(Easing.sin), useNativeDriver: true })); d.start();
    Erisim.ekranAcikTut(true);  // konuşurken ekran kararmasın
    if (otomatik) dinle();
    return () => { kapali.current = true; d.stop(); Speech.stop(); try { kaydedici.stop(); } catch {} Erisim.uyanmaDuraklat(false); Erisim.ekranAcikTut(false); };
  }, []);

  const dinle = async () => {
    if (kapali.current) return;
    Speech.stop();
    if (!(await izinIste("Mikrofon", requestRecordingPermissionsAsync, getRecordingPermissionsAsync))) return;
    Erisim.uyanmaDuraklat(true);
    try {
      await setAudioModeAsync({ allowsRecording: true, playsInSilentMode: true });
      await kaydedici.prepareToRecordAsync(); kaydedici.record();
    } catch { setFaz("hazir"); return; }
    ses.current = { konustu: false, sessizBas: 0, bas: Date.now() };
    setFaz("dinliyor"); titret();
  };

  // Susunca otomatik bitir: konuşma başladıktan sonra 0.8 sn sessizlik; hiç konuşulmazsa 7 sn; en fazla 15 sn
  useEffect(() => {
    if (fazRef.current !== "dinliyor") return;
    const m = durum.metering ?? -160, simdi = Date.now(), s = ses.current;
    olcek.setValue(1 + Math.max(0, Math.min(0.35, (m + 50) / 120)));
    if (m > -38) { s.konustu = true; s.sessizBas = 0; }
    else if (s.konustu) { if (!s.sessizBas) s.sessizBas = simdi; else if (simdi - s.sessizBas > 800) bitir(); }
    if ((!s.konustu && simdi - s.bas > 7000) || simdi - s.bas > 15000) bitir();
  }, [durum.metering, durum.durationMillis]);

  const bitir = async () => {
    if (fazRef.current !== "dinliyor") return;
    setFaz("dusunuyor"); fazRef.current = "dusunuyor"; olcek.setValue(1);
    const t0 = Date.now();
    try { await kaydedici.stop(); } catch {}
    try { await setAudioModeAsync({ allowsRecording: false, playsInSilentMode: true }); } catch {}
    const uri = kaydedici.uri;
    if (!ses.current.konustu || !uri) { setFaz("hazir"); Erisim.uyanmaDuraklat(false); return; }
    const metin = await sesiYaziyaDok(uri);
    const t1 = Date.now();
    if (!metin) { setArex("Duyamadım, tekrar söyler misin?"); konus("Duyamadım, tekrar söyler misin?"); return; }
    setSen(metin); setArex("");
    let cevap: string | null = null;
    if (!kisitli) { const tel = await telefonKomutu(metin).catch(() => null); if (tel) cevap = seseUygun(tel).replace(/\s+/g, " ").slice(0, 220); }
    if (!cevap) {
      const oz = kisitli ? "" : await profilOzeti().catch(() => "");
      const r = await sohbetTamamla([...gecmis.current.slice(-12), { role: "user", content: metin }],
        { sistem: SES_KURALI + (oz ? "\nKullanıcı hakkında bilinenler: " + oz.slice(0, 800) : ""), maks: 260, sicaklik: 0.6 });
      cevap = r.metin ? seseUygun(r.metin) : "Şu an cevap veremedim, birazdan tekrar dener misin?";
    }
    gecmis.current = [...gecmis.current, { role: "user" as const, content: metin }, { role: "assistant" as const, content: cevap }].slice(-16);
    setSure(`yazı ${((t1 - t0) / 1000).toFixed(1)} sn • cevap ${((Date.now() - t1) / 1000).toFixed(1)} sn`);
    setArex(cevap); konus(cevap);
  };

  const konus = (metin: string) => {
    if (kapali.current) return;
    setFaz("konusuyor");
    Speech.speak(metin, { language: "tr-TR", rate: 1.05, pitch: 1.0,
      onDone: () => { if (!kapali.current) { setFaz("hazir"); dinle(); } },
      onStopped: () => { if (!kapali.current && fazRef.current === "konusuyor") setFaz("hazir"); },
      onError: () => setFaz("hazir") });
  };

  const dokun = () => {
    titret();
    if (faz === "konusuyor") { Speech.stop(); dinle(); }  // sözünü kes
    else if (faz === "dinliyor") bitir();
    else if (faz === "hazir") dinle();
  };

  const parlak = nefes.interpolate({ inputRange: [0, 0.5, 1], outputRange: [0.45, 0.9, 0.45] });
  const don = nefes.interpolate({ inputRange: [0, 1], outputRange: ["0deg", "360deg"] });
  const yazi = { hazir: "Seni dinlemeye hazırım", dinliyor: "Dinliyorum", dusunuyor: "Düşünüyorum", konusuyor: "Konuşuyorum" }[faz];
  const alt = { hazir: "Küreye dokun ve konuş", dinliyor: "Susunca kendiliğinden anlarım", dusunuyor: "Bir saniye…", konusuyor: "Sözümü kesmek için dokun" }[faz];
  const renk: [string, string, string] = faz === "dinliyor" ? ["#22d3ee", "#7c5cff", "#ff5fa2"] : faz === "dusunuyor" ? ["#ffb84d", "#a259ff", "#4f8cff"] : faz === "konusuyor" ? ["#a259ff", "#ff5fa2", "#ffb84d"] : ["#6d5cff", "#4f8cff", "#22d3ee"];
  const seviye = faz === "dinliyor" ? Math.max(0, Math.min(1, ((durum.metering ?? -60) + 55) / 45)) : faz === "konusuyor" ? 0.55 : 0.08;
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center", paddingHorizontal: 22 }}>
      {/* Küre: dönen ışık halkası + parlama + gradyan çekirdek */}
      <Pressable onPress={dokun} style={{ alignItems: "center", justifyContent: "center" }}>
        <Animated.View style={{ position: "absolute", width: 300, height: 300, borderRadius: 150, opacity: parlak }}>
          <LinearGradient colors={[renk[1] + "40", renk[0] + "10", "transparent"]} style={{ flex: 1, borderRadius: 150 }} />
        </Animated.View>
        <Animated.View style={{ position: "absolute", width: 232, height: 232, borderRadius: 116, transform: [{ rotate: don }] }}>
          <LinearGradient colors={[renk[0], "transparent", renk[2], "transparent"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ flex: 1, borderRadius: 116, opacity: 0.85 }} />
        </Animated.View>
        <View style={{ width: 222, height: 222, borderRadius: 111, backgroundColor: "#060a20" }} />
        <Animated.View style={{ position: "absolute", transform: [{ scale: olcek }] }}>
          <LinearGradient colors={renk} start={{ x: 0.15, y: 0.05 }} end={{ x: 0.85, y: 1 }} style={{ width: 186, height: 186, borderRadius: 93, alignItems: "center", justifyContent: "center",
            shadowColor: renk[1], shadowOpacity: 0.9, shadowRadius: 45, elevation: 20 }}>
            <LinearGradient colors={["rgba(255,255,255,0.32)", "rgba(255,255,255,0)"]} start={{ x: 0.5, y: 0 }} end={{ x: 0.5, y: 0.6 }} style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, borderRadius: 93 }} />
            <Ionicons name={faz === "dinliyor" ? "mic" : faz === "dusunuyor" ? "sparkles" : faz === "konusuyor" ? "volume-high" : "mic-outline"} size={44} color="#fff" />
          </LinearGradient>
        </Animated.View>
      </Pressable>
      {/* Ekolayzer: sesine göre */}
      <View style={{ flexDirection: "row", alignItems: "center", gap: 4, height: 54, marginTop: 34 }}>
        {Array.from({ length: 23 }, (_, i) => {
          const orta = 1 - Math.abs(i - 11) / 11;
          const h = 6 + seviye * 46 * (0.35 + 0.65 * orta) * (0.6 + 0.4 * Math.abs(Math.sin(i * 1.7 + Date.now() / 160)));
          return <LinearGradient key={i} colors={["#ff5fa2", renk[1], renk[0]]} style={{ width: 5, height: h, borderRadius: 3, opacity: faz === "hazir" ? 0.35 : 0.95 }} />;
        })}
      </View>
      <Text style={{ color: "#fff", fontSize: 26, fontWeight: "300", letterSpacing: 0.8, marginTop: 14 }}>{yazi}{faz !== "hazir" ? "…" : ""}</Text>
      <Text style={{ color: "#8f98c4", fontSize: 13, marginTop: 4 }}>{alt}</Text>
      {/* Konuşma: cam kartlar */}
      <ScrollView style={{ maxHeight: 200, width: "100%", marginTop: 22 }} contentContainerStyle={{ gap: 10, paddingBottom: 6 }}>
        {sen ? (
          <View style={{ alignSelf: "flex-end", maxWidth: "88%", backgroundColor: "rgba(124,92,255,0.18)", borderRadius: 18, borderBottomRightRadius: 6, paddingHorizontal: 14, paddingVertical: 9, borderWidth: 1, borderColor: "rgba(162,140,255,0.3)" }}>
            <Text style={{ color: "#e6e3ff", fontSize: 15 }}>{sen}</Text>
          </View>
        ) : null}
        {arex ? (
          <View style={{ alignSelf: "flex-start", maxWidth: "92%", backgroundColor: "rgba(255,255,255,0.06)", borderRadius: 18, borderBottomLeftRadius: 6, paddingHorizontal: 14, paddingVertical: 10, borderWidth: 1, borderColor: "rgba(255,255,255,0.1)" }}>
            <Text style={{ color: "#f3f5ff", fontSize: 16, lineHeight: 23 }}>{arex}</Text>
          </View>
        ) : null}
      </ScrollView>
      {sure ? <Text style={{ color: "#5d6690", fontSize: 10.5, marginTop: 4 }}>{sure}</Text> : null}
      {kisitli ? <Text style={{ color: "#ffb84d", fontSize: 11.5, marginTop: 6 }}>🟡 Kısıtlı mod — kişisel işlemler parmak izi ister</Text> : null}
    </View>
  );
}
