// AREX — premium arayüz bileşenleri
import { LinearGradient } from "expo-linear-gradient";
import * as Haptics from "expo-haptics";
import React from "react";
import { ActivityIndicator, Animated, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View, type StyleProp, type TextStyle, type ViewStyle } from "react-native";
import Markdown from "react-native-markdown-display";
import { ARKA_GRADYAN, GRADYAN, R } from "./tema";

export const titret = () => { if (Platform.OS !== "web") Haptics.selectionAsync().catch(() => {}); };

export function Arkaplan({ children }: { children: React.ReactNode }) {
  return (
    <LinearGradient colors={ARKA_GRADYAN } locations={[0, 0.45, 1]} style={{ flex: 1 }}>
      {children}
    </LinearGradient>
  );
}

export function Kart({ children, style }: { children: React.ReactNode; style?: StyleProp<ViewStyle> }) {
  return <View style={[s.kart, style]}>{children}</View>;
}

export function Baslik({ children, alt }: { children: React.ReactNode; alt?: string }) {
  return (
    <View style={{ marginBottom: 10 }}>
      <Text style={s.baslik}>{children}</Text>
      {alt ? <Text style={s.alt}>{alt}</Text> : null}
    </View>
  );
}

export function Dugme({ yazi, onPress, yukleniyor, ikincil, kucuk, style, devreDisi }: {
  yazi: string; onPress: () => void; yukleniyor?: boolean; ikincil?: boolean; kucuk?: boolean; style?: StyleProp<ViewStyle>; devreDisi?: boolean;
}) {
  const ic = (
    <View style={[s.dugmeIc, kucuk && { paddingVertical: 9 }]}>
      {yukleniyor ? <ActivityIndicator color="#fff" /> : <Text style={[s.dugmeYazi, kucuk && { fontSize: 14 }]}>{yazi}</Text>}
    </View>
  );
  return (
    <Pressable disabled={yukleniyor || devreDisi} onPress={() => { titret(); onPress(); }}
      style={({ pressed }) => [{ borderRadius: 16, overflow: "hidden", opacity: devreDisi ? 0.5 : 1, transform: [{ scale: pressed ? 0.97 : 1 }] }, style]}>
      {ikincil ? <View style={[s.ikincil]}>{ic}</View> : <LinearGradient colors={GRADYAN } start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}>{ic}</LinearGradient>}
    </Pressable>
  );
}

export function Hap({ yazi, secili, onPress }: { yazi: string; secili?: boolean; onPress: () => void }) {
  return (
    <Pressable onPress={() => { titret(); onPress(); }} style={({ pressed }) => [s.hap, secili && { backgroundColor: R.hap, borderColor: R.acc }, pressed && { opacity: 0.7 }]}>
      <Text style={[s.hapYazi, secili && { color: "#fff" }]}>{yazi}</Text>
    </Pressable>
  );
}

export function Secici<T extends string>({ secenekler, deger, onChange, etiket, coklu }: {
  secenekler: { k: T; ad: string }[]; deger: T | T[]; onChange: (v: any) => void; etiket?: string; coklu?: boolean;
}) {
  const seciliMi = (k: T) => (Array.isArray(deger) ? deger.includes(k) : deger === k);
  return (
    <View style={{ marginBottom: 10 }}>
      {etiket ? <Text style={s.etiket}>{etiket}</Text> : null}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, paddingRight: 8 }}>
        {secenekler.map((o) => (
          <Hap key={o.k} yazi={o.ad} secili={seciliMi(o.k)} onPress={() => {
            if (coklu && Array.isArray(deger)) onChange(deger.includes(o.k) ? deger.filter((x) => x !== o.k) : [...deger, o.k]);
            else onChange(o.k);
          }} />
        ))}
      </ScrollView>
    </View>
  );
}

export function Girdi(p: React.ComponentProps<typeof TextInput> & { etiket?: string }) {
  const { etiket, style, ...rest } = p;
  return (
    <View style={{ marginBottom: 10 }}>
      {etiket ? <Text style={s.etiket}>{etiket}</Text> : null}
      <TextInput placeholderTextColor={R.soluk} {...rest} style={[s.girdi, style as StyleProp<TextStyle>]} />
    </View>
  );
}

const mdStil = StyleSheet.create({
  body: { color: R.yazi, fontSize: 16, lineHeight: 24 },
  heading1: { color: "#fff", fontSize: 21, fontWeight: "800", marginBottom: 6 },
  heading2: { color: "#fff", fontSize: 18, fontWeight: "700", marginTop: 8 },
  heading3: { color: "#fff", fontSize: 16, fontWeight: "700", marginTop: 6 },
  strong: { color: "#fff", fontWeight: "700" },
  em: { color: "#dfe3ff" },
  bullet_list: { marginVertical: 4 },
  code_inline: { backgroundColor: "rgba(124,92,255,0.25)", color: "#e9e4ff", borderRadius: 6, paddingHorizontal: 4 },
  fence: { backgroundColor: "rgba(0,0,0,0.35)", color: "#e9e4ff", borderRadius: 10, padding: 10, borderWidth: 0 },
  code_block: { backgroundColor: "rgba(0,0,0,0.35)", color: "#e9e4ff", borderRadius: 10, padding: 10, borderWidth: 0 },
  table: { borderColor: R.cizgi, borderRadius: 8 },
  th: { padding: 6, backgroundColor: "rgba(124,92,255,0.18)" },
  td: { padding: 6, borderColor: R.cizgi },
  tr: { borderColor: R.cizgi },
  blockquote: { backgroundColor: "rgba(34,211,238,0.08)", borderLeftColor: R.acc2, borderLeftWidth: 3, paddingHorizontal: 8 },
  link: { color: R.acc2 },
  hr: { backgroundColor: R.cizgi },
});

export function MdMetin({ children, rtl }: { children: string; rtl?: boolean }) {
  const o = R.olcek || 1;
  const stil = o === 1 ? mdStil : { ...mdStil, body: { ...mdStil.body, fontSize: 16 * o, lineHeight: 24 * o }, link: { color: R.acc2 } };
  return (
    <View style={rtl ? { direction: "rtl" } as ViewStyle : undefined}>
      <Markdown style={stil as any}>{children || ""}</Markdown>
    </View>
  );
}

export const s = StyleSheet.create({
  kart: { backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 22, padding: 16, marginBottom: 12 },
  baslik: { color: "#fff", fontSize: 24, fontWeight: "800", letterSpacing: 0.2 },
  alt: { color: R.soluk, fontSize: 14, marginTop: 4, lineHeight: 20 },
  dugmeIc: { paddingVertical: 14, paddingHorizontal: 18, alignItems: "center", justifyContent: "center" },
  dugmeYazi: { color: "#fff", fontWeight: "700", fontSize: 16 },
  ikincil: { backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 16 },
  hap: { paddingHorizontal: 14, paddingVertical: 9, borderRadius: 999, alignItems: "center", backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi },
  hapSecili: { backgroundColor: "rgba(124,92,255,0.45)", borderColor: R.acc },
  hapYazi: { color: R.yazi, fontSize: 14, fontWeight: "600" },
  etiket: { color: R.soluk, fontSize: 13, marginBottom: 6, fontWeight: "600" },
  girdi: { backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 14, color: R.yazi, paddingHorizontal: 14, paddingVertical: 12, fontSize: 16 },
});

/** Görsel aç/kapat anahtarı: renk/yazı/simge doğrudan duruma bağlı (her cihazda anında değişir), topuz kayarak gider */
export function Anahtar({ acik, onChange, renk }: { acik: boolean; onChange: (v: boolean) => void; renk?: string }) {
  const x = React.useRef(new Animated.Value(acik ? 1 : 0)).current;
  React.useEffect(() => { Animated.spring(x, { toValue: acik ? 1 : 0, useNativeDriver: true, bounciness: 8, speed: 18 }).start(); }, [acik]);
  const r = renk || R.acc;
  return (
    <Pressable onPress={() => { titret(); onChange(!acik); }} hitSlop={8} accessibilityRole="switch" accessibilityState={{ checked: acik }}>
      <View style={{ width: 80, height: 34, borderRadius: 17, justifyContent: "center", borderWidth: 1.5,
        borderColor: acik ? r : "rgba(255,255,255,0.22)", backgroundColor: acik ? r : "rgba(255,255,255,0.06)" }}>
        <Text style={{ position: "absolute", left: acik ? 10 : undefined, right: acik ? undefined : 7, fontSize: 8.5, fontWeight: "900", letterSpacing: 0.3, color: acik ? "#1a1408" : R.soluk }}>{acik ? "AÇIK" : "KAPALI"}</Text>
        <Animated.View style={{ position: "absolute", left: 3, width: 26, height: 26, borderRadius: 13, alignItems: "center", justifyContent: "center",
          backgroundColor: acik ? "#fff" : "#8a90ad", transform: [{ translateX: x.interpolate({ inputRange: [0, 1], outputRange: [0, 48] }) }],
          shadowColor: "#000", shadowOpacity: 0.3, shadowRadius: 3, shadowOffset: { width: 0, height: 1 }, elevation: 3 }}>
          <Text style={{ fontSize: 13, fontWeight: "900", color: acik ? r : "#2a2f48", marginTop: -1 }}>{acik ? "✓" : "✕"}</Text>
        </Animated.View>
      </View>
    </Pressable>
  );
}

/** Simge + başlık + açıklama + anahtar satırı */
export function AnahtarSatiri({ simge, baslik, alt, acik, onChange, renk }: { simge: string; baslik: string; alt?: string; acik: boolean; onChange: (v: boolean) => void; renk?: string }) {
  return (
    <Pressable onPress={() => { titret(); onChange(!acik); }} style={{ flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 10 }}>
      <View style={{ width: 38, height: 38, borderRadius: 12, alignItems: "center", justifyContent: "center", backgroundColor: acik ? (renk || R.acc) + "33" : "rgba(255,255,255,0.06)" }}>
        <Text style={{ fontSize: 18 }}>{simge}</Text>
      </View>
      <View style={{ flex: 1 }}>
        <Text style={{ color: "#fff", fontWeight: "700", fontSize: 15 }}>{baslik}</Text>
        {alt ? <Text style={{ color: R.soluk, fontSize: 12, marginTop: 1 }}>{alt}</Text> : null}
      </View>
      <Anahtar acik={acik} onChange={onChange} renk={renk} />
    </Pressable>
  );
}
