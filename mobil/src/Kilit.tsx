// AREX — uygulama kilidi: biyometrik (parmak izi / yüz) + PIN yedeği. PIN cihazın güvenli deposunda saklanır.
import * as LocalAuthentication from "expo-local-authentication";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect, useState } from "react";
import { Platform, Pressable, Text, View } from "react-native";
import { ARKA_GRADYAN, GRADYAN, R } from "./tema";
import { titret } from "./ui";

const ANAHTAR = "arex_kilit_pin";
async function deger(): Promise<string | null> {
  if (Platform.OS === "web") { try { return globalThis.localStorage?.getItem(ANAHTAR) ?? null; } catch { return null; } }
  const SS = await import("expo-secure-store");
  return SS.getItemAsync(ANAHTAR);
}
export async function kilitAcikMi(): Promise<boolean> { return !!(await deger()); }
export async function pinAyarla(pin: string | null) {
  if (Platform.OS === "web") { try { pin ? globalThis.localStorage?.setItem(ANAHTAR, pin) : globalThis.localStorage?.removeItem(ANAHTAR); } catch {} return; }
  const SS = await import("expo-secure-store");
  if (pin) await SS.setItemAsync(ANAHTAR, pin); else await SS.deleteItemAsync(ANAHTAR);
}
export async function biyometrikVarMi(): Promise<boolean> {
  if (Platform.OS === "web") return false;
  try { return (await LocalAuthentication.hasHardwareAsync()) && (await LocalAuthentication.isEnrolledAsync()); } catch { return false; }
}
/** YALNIZ parmak izi / yüz (PIN ya da şifre seçeneği yok) — ses imzası ve tanınmayan ses kilidi için */
export async function biyometrikZorunlu(mesaj = "Parmak izinle doğrula"): Promise<boolean> {
  if (Platform.OS === "web") return false;
  try {
    const r = await LocalAuthentication.authenticateAsync({ promptMessage: mesaj, cancelLabel: "Vazgeç", disableDeviceFallback: true, biometricsSecurityLevel: "strong" } as any);
    return r.success;
  } catch { return false; }
}
export async function biyometrikDogrula(): Promise<boolean> {
  try {
    const r = await LocalAuthentication.authenticateAsync({ promptMessage: "AREX AI kilidini aç", cancelLabel: "PIN kullan", disableDeviceFallback: false });
    return r.success;
  } catch { return false; }
}

export default function KilitEkrani({ acildi }: { acildi: () => void }) {
  const [pin, setPin] = useState("");
  const [hata, setHata] = useState("");
  const [bio, setBio] = useState(false);
  const [hazir, setHazir] = useState(false);
  const basarisiz = React.useRef(0);
  const parmak = () => biyometrikZorunlu("AREX — parmak izinle aç").then((ok) => {
    if (ok) { basarisiz.current = 0; acildi(); return; }
    setHata("Parmak izi doğrulanamadı — tekrar dene");
    // 3 başarısız denemede sahibine güvenlik bildirimi
    if (++basarisiz.current === 3) import("../modules/arex-erisim").then((E) => E.guvenlikUyari("AREX kilidi açılamadı", "Üst üste 3 başarısız parmak izi denemesi")).catch(() => {});
  });
  useEffect(() => { biyometrikVarMi().then((v) => { setBio(v); setHazir(true); if (v) parmak(); }); }, []);
  const tus = async (t: string) => {
    titret(); setHata("");
    if (t === "⌫") { setPin(pin.slice(0, -1)); return; }
    const y = (pin + t).slice(0, 6);
    setPin(y);
    const dogru = await deger();
    if (dogru && y.length === dogru.length) {
      if (y === dogru) acildi(); else { setHata("Yanlış PIN"); setPin(""); }
    }
  };
  // Parmak izi varsa YALNIZ parmak izi (PIN/şifre yok — şifre görülüp öğrenilebilir). PIN yalnız parmak izi donanımı yoksa.
  if (hazir && bio) return (
    <LinearGradient colors={ARKA_GRADYAN} style={{ flex: 1, alignItems: "center", justifyContent: "center", padding: 24 }}>
      <LinearGradient colors={GRADYAN} style={{ width: 96, height: 96, borderRadius: 48, alignItems: "center", justifyContent: "center", marginBottom: 18 }}>
        <Text style={{ fontSize: 44 }}>👆</Text>
      </LinearGradient>
      <Text style={{ color: "#fff", fontSize: 24, fontWeight: "800" }}>AREX kilitli</Text>
      <Text style={{ color: R.soluk, marginTop: 6, textAlign: "center" }}>Yalnız sen: parmak izin ya da sesin ("AREX")</Text>
      {hata ? <Text style={{ color: R.kirmizi, marginTop: 12 }}>{hata}</Text> : null}
      <Pressable onPress={() => { titret(); setHata(""); parmak(); }} style={{ marginTop: 26 }}>
        <LinearGradient colors={GRADYAN} style={{ paddingHorizontal: 30, paddingVertical: 15, borderRadius: 26 }}>
          <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16 }}>👆 Parmak izimle aç</Text>
        </LinearGradient>
      </Pressable>
    </LinearGradient>
  );
  return (
    <LinearGradient colors={ARKA_GRADYAN} style={{ flex: 1, alignItems: "center", justifyContent: "center", padding: 24 }}>
      <LinearGradient colors={GRADYAN} style={{ width: 84, height: 84, borderRadius: 42, alignItems: "center", justifyContent: "center", marginBottom: 18 }}>
        <Text style={{ fontSize: 36 }}>🔐</Text>
      </LinearGradient>
      <Text style={{ color: "#fff", fontSize: 24, fontWeight: "800" }}>AREX AI kilitli</Text>
      <Text style={{ color: R.soluk, marginTop: 6 }}>Devam etmek için PIN gir{bio ? " ya da parmak izini kullan" : ""}</Text>
      <View style={{ flexDirection: "row", gap: 14, marginVertical: 26 }}>
        {Array.from({ length: 6 }, (_, i) => <View key={i} style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: i < pin.length ? R.acc2 : "rgba(255,255,255,0.15)" }} />)}
      </View>
      {hata ? <Text style={{ color: R.kirmizi, marginBottom: 10 }}>{hata}</Text> : null}
      <View style={{ width: 270, flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", rowGap: 14 }}>
        {["1", "2", "3", "4", "5", "6", "7", "8", "9", bio ? "👆" : "", "0", "⌫"].map((t, i) => (
          <Pressable key={i} disabled={!t} onPress={() => (t === "👆" ? biyometrikDogrula().then((ok) => ok && acildi()) : tus(t))}
            style={({ pressed }) => ({ width: 78, height: 78, borderRadius: 39, alignItems: "center", justifyContent: "center", backgroundColor: t ? (pressed ? R.hap : R.kart) : "transparent", borderWidth: t ? 1 : 0, borderColor: R.cizgi })}>
            <Text style={{ color: "#fff", fontSize: 26, fontWeight: "600" }}>{t}</Text>
          </Pressable>
        ))}
      </View>
    </LinearGradient>
  );
}
