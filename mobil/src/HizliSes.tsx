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
const SES_KURALI = "Sen AREX'sin; kullanıcıyla SESLİ konuşuyorsun. Cevapların kısa (1-3 cümle), sıcak, doğal Türkçe; madde işareti, emoji, markdown, başlık YOK. " +
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

  const parlak = nefes.interpolate({ inputRange: [0, 0.5, 1], outputRange: [0.55, 1, 0.55] });
  const yazi = { hazir: "Konuşmak için dokun", dinliyor: "Dinliyorum…", dusunuyor: "Düşünüyorum…", konusuyor: "Konuşuyorum…" }[faz];
  const renk: [string, string, string] = faz === "dinliyor" ? ["#22d3ee", "#7c5cff", "#ff5fa2"] : faz === "dusunuyor" ? ["#ffb84d", "#a259ff", "#4f8cff"] : ["#7c5cff", "#4f8cff", "#22d3ee"];
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center", paddingHorizontal: 20 }}>
      <View style={{ position: "absolute", top: 8, flexDirection: "row", alignItems: "center", gap: 6, paddingHorizontal: 12, paddingVertical: 5, borderRadius: 14, backgroundColor: "rgba(255,255,255,0.06)", borderWidth: 1, borderColor: "rgba(255,255,255,0.1)" }}>
        <Ionicons name="flash" size={13} color="#ffd166" /><Text style={{ color: "#dfe3ff", fontSize: 12, fontWeight: "700" }}>Hızlı Ses{kisitli ? " • kısıtlı" : ""}</Text>
      </View>
      <Pressable onPress={dokun}>
        <Animated.View style={{ opacity: parlak, position: "absolute", left: -30, right: -30, top: -30, bottom: -30, borderRadius: 999 }}>
          <LinearGradient colors={[renk[0] + "55", renk[1] + "22", "transparent"]} style={{ flex: 1, borderRadius: 999 }} />
        </Animated.View>
        <Animated.View style={{ transform: [{ scale: olcek }] }}>
          <LinearGradient colors={renk} start={{ x: 0.1, y: 0 }} end={{ x: 0.9, y: 1 }} style={{ width: 190, height: 190, borderRadius: 95, alignItems: "center", justifyContent: "center",
            shadowColor: renk[1], shadowOpacity: 0.8, shadowRadius: 40, elevation: 18 }}>
            <View style={{ position: "absolute", top: 22, left: 34, width: 70, height: 40, borderRadius: 40, backgroundColor: "rgba(255,255,255,0.35)", transform: [{ rotate: "-20deg" }] }} />
            <Ionicons name={faz === "dinliyor" ? "mic" : faz === "dusunuyor" ? "ellipsis-horizontal" : faz === "konusuyor" ? "volume-high" : "mic-outline"} size={46} color="#fff" />
          </LinearGradient>
        </Animated.View>
      </Pressable>
      <Text style={{ color: "#fff", fontSize: 24, fontWeight: "300", letterSpacing: 0.5, marginTop: 30 }}>{yazi}</Text>
      {sure ? <Text style={{ color: "#7d86ad", fontSize: 11, marginTop: 4 }}>{sure}</Text> : null}
      <ScrollView style={{ maxHeight: 190, width: "100%", marginTop: 18 }} contentContainerStyle={{ gap: 8 }}>
        {sen ? <Text style={{ color: "#9aa3c7", fontSize: 15, textAlign: "center" }}>“{sen}”</Text> : null}
        {arex ? <Text style={{ color: "#eef2ff", fontSize: 17, lineHeight: 25, textAlign: "center" }}>{arex}</Text> : null}
      </ScrollView>
    </View>
  );
}
