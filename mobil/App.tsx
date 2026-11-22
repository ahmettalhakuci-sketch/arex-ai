// AREX AI — mobil & masaüstü uygulaması (React Native / Expo)
import { Ionicons } from "@expo/vector-icons";
import { BlurView } from "expo-blur";
import { StatusBar } from "expo-status-bar";
import * as SystemUI from "expo-system-ui";
import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, AppState, Animated, Dimensions, Linking, PanResponder, Platform, Pressable, StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider, useSafeAreaInsets } from "react-native-safe-area-context";
import { AyarSaglayici, useAyar } from "./src/ayar";
import { anahtarlariYukle } from "./src/depo";
import { guncellemeDenetle, guncellemeyiIndir, type Guncelleme } from "./src/guncelleme";
import AnalizEkrani from "./src/ekranlar/Analiz";
import AraclarEkrani from "./src/ekranlar/Araclar";
import AyarlarEkrani from "./src/ekranlar/Ayarlar";
import CanliEkrani from "./src/ekranlar/Canli";
import CocukEkrani from "./src/ekranlar/Cocuk";
import KuranEkrani from "./src/ekranlar/Kuran";
import { bekleyenSohbet } from "./src/Asistan";
import KilitEkrani, { kilitAcikMi } from "./src/Kilit";
import SohbetEkrani from "./src/ekranlar/Sohbet";
import { R } from "./src/tema";
import * as Erisim from "./modules/arex-erisim";
import { Arkaplan, titret } from "./src/ui";

type Sekme = "sohbet" | "canli" | "kuran" | "cocuk" | "analiz" | "araclar" | "ayarlar";
// Vektör simgeler (Ionicons): her cihazda keskin ve tutarlı; seçiliyken dolu, değilken çizgi
const SEKMELER: [Sekme, string, string][] = [
  ["sohbet", "chatbubbles", "Sohbet"], ["canli", "radio", "Canlı"], ["kuran", "book", "Kur'an"], ["cocuk", "happy", "Çocuk"],
  ["analiz", "scan", "Analiz"], ["araclar", "compass", "Araçlar"], ["ayarlar", "settings", "Ayarlar"],
];

function Uygulama() {
  const ic = useSafeAreaInsets();
  const { ayar } = useAyar();
  const [sekme, setSekme] = useState<Sekme>("sohbet");
  const [disMesaj, setDisMesaj] = useState<{ metin: string; cevap: string } | null>(null);
  const [asistan, setAsistan] = useState(false);
  useEffect(() => {
    // Yan tuş / asistan tuşu → arex://asistan → altta mini Canlı paneli
    const isle = (u?: string | null) => {
      if (!u) return;
      if (u.startsWith("arex://asistan")) setAsistan(true);
      // yan tuş kartından: ⤢ büyüt → Canlı, sohbete aktar → Sohbet
      else if (u.startsWith("arex://canli")) { setAsistan(false); setSekme("canli"); }
      else if (u.startsWith("arex://ayarlar")) { setAsistan(false); setSekme("ayarlar"); }
      else if (u.startsWith("arex://sohbet")) {
        // Mesaj yalnız asistan kartının bellekte bıraktığı veriden alınır; URL'deki parametreler yok sayılır (sahte mesaj engeli)
        const b = bekleyenSohbet.deger; bekleyenSohbet.deger = null;
        if (b) setDisMesaj(b);
        setSekme("sohbet");
      }
    };
    Linking.getInitialURL().then(isle).catch(() => {});
    const abone = Linking.addEventListener("url", (e) => isle(e.url));
    return () => abone.remove();
  }, []);
  const buyut = () => { setAsistan(false); setSekme("canli"); };
  const [yeniSurum, setYeniSurum] = useState<Guncelleme | null>(null);
  useEffect(() => { guncellemeDenetle().then(setYeniSurum); }, []);
  // Erişim servisi güncelleme/kapanma sonrası bağlantısız kalabiliyor → açılışta ve uygulamaya her dönüşte onar
  useEffect(() => {
    Erisim.onar().catch(() => {});
    const a = AppState.addEventListener("change", (x) => { if (x === "active") Erisim.onar().catch(() => {}); });
    return () => a.remove();
  }, []);
  const sohbeteGonder = (metin: string, cevap: string) => { setDisMesaj({ metin, cevap }); setSekme("sohbet"); };
  const ekran = {
    sohbet: <SohbetEkrani disaridanMesaj={disMesaj} temizle={() => setDisMesaj(null)} canliyaGit={() => setSekme("canli")} />,
    canli: <CanliEkrani sohbeteGonder={sohbeteGonder} />,
    kuran: <KuranEkrani />,
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
      {yeniSurum ? (
        <Pressable onPress={() => guncellemeyiIndir(yeniSurum)} style={{ position: "absolute", top: ic.top + 56, left: 14, right: 14, zIndex: 40 }}>
          <View style={{ backgroundColor: R.hap, borderColor: R.acc, borderWidth: 1, borderRadius: 18, padding: 12, flexDirection: "row", alignItems: "center", gap: 10 }}>
            <Ionicons name="cloud-download" size={22} color="#fff" />
            <View style={{ flex: 1 }}>
              <Text style={{ color: "#fff", fontWeight: "800" }}>Yeni sürüm hazır: {yeniSurum.surum}</Text>
              <Text style={{ color: "#e6e9ff", fontSize: 12 }} numberOfLines={1}>{yeniSurum.notlar?.[0] || "Dokun, indir ve kur"}</Text>
            </View>
            <Pressable hitSlop={10} onPress={() => setYeniSurum(null)}><Ionicons name="close" size={20} color="#fff" /></Pressable>
          </View>
        </Pressable>
      ) : null}
      {asistan ? <AsistanPaneli kapat={() => setAsistan(false)} buyut={buyut} sohbeteGonder={sohbeteGonder} /> : null}
      {ayar.gozKoruma ? <View pointerEvents="none" style={[StyleSheet.absoluteFill, { backgroundColor: "rgba(255,150,40,0.10)", zIndex: 50 }]} /> : null}
      <View style={[st.cubukDis, { paddingBottom: Math.max(ic.bottom, 6) }]}>
        {Platform.OS !== "web" ? <BlurView intensity={40} tint="dark" style={StyleSheet.absoluteFill} /> : null}
        {SEKMELER.map(([k, ikon, ad]) => {
          const secili = sekme === k;
          return (
            <Pressable key={k} style={st.sekme} onPress={() => { titret(); setSekme(k); }}>
              <View style={[st.ikonKap, secili && { backgroundColor: R.hap }]}>
                <Ionicons name={(secili ? ikon : ikon + "-outline") as any} size={22} color={secili ? "#fff" : k === "canli" ? "#ff8a9b" : R.soluk} />
              </View>
              <Text style={[st.sekmeYazi, secili && { color: "#fff", fontWeight: "800" }]}>{ad}</Text>
              {k === "canli" ? <CanliIsareti /> : null}
            </Pressable>
          );
        })}
      </View>
    </Arkaplan>
  );
}

/** Sekme çubuğunda "Canlı"nın altında yanıp sönen kırmızı CANLI işareti (yerel sürücüyle, performansı etkilemez) */
function CanliIsareti() {
  const nabiz = useRef(new Animated.Value(1)).current;
  useEffect(() => {
    const dongu = Animated.loop(Animated.sequence([
      Animated.timing(nabiz, { toValue: 0.35, duration: 700, useNativeDriver: true }),
      Animated.timing(nabiz, { toValue: 1, duration: 700, useNativeDriver: true }),
    ]));
    dongu.start();
    return () => dongu.stop();
  }, []);
  return (
    <View style={{ flexDirection: "row", alignItems: "center", gap: 3, marginTop: 1 }}>
      <Animated.View style={{ width: 6, height: 6, borderRadius: 3, backgroundColor: "#ff3b5c", opacity: nabiz }} />
      <Text style={{ color: "#ff6b81", fontSize: 8.5, fontWeight: "900", letterSpacing: 0.8 }}>CANLI</Text>
    </View>
  );
}

/** Gemini tarzı alttan açılan mini asistan paneli: yukarı sürükle → tam ekran, aşağı sürükle → kapat */
function AsistanPaneli({ kapat, buyut, sohbeteGonder }: { kapat: () => void; buyut: () => void; sohbeteGonder: (m: string, c: string) => void }) {
  const ic = useSafeAreaInsets();
  const yukseklik = Dimensions.get("window").height * 0.5;
  const y = useRef(new Animated.Value(yukseklik)).current;
  useEffect(() => { Animated.spring(y, { toValue: 0, useNativeDriver: true, bounciness: 6 }).start(); }, []);
  const surukle = useRef(PanResponder.create({
    onMoveShouldSetPanResponder: (_e, g) => Math.abs(g.dy) > 6,
    onPanResponderMove: (_e, g) => y.setValue(Math.max(-80, g.dy)),
    onPanResponderRelease: (_e, g) => {
      if (g.dy < -60) buyut();
      else if (g.dy > 90) Animated.timing(y, { toValue: yukseklik, duration: 180, useNativeDriver: true }).start(kapat);
      else Animated.spring(y, { toValue: 0, useNativeDriver: true }).start();
    },
  })).current;
  return (
    <View style={[StyleSheet.absoluteFill, { zIndex: 60 }]}>
      <Pressable style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.45)" }} onPress={kapat} />
      <Animated.View style={{ height: yukseklik + ic.bottom, transform: [{ translateY: y }], backgroundColor: R.bg2, borderTopLeftRadius: 28, borderTopRightRadius: 28, overflow: "hidden", borderWidth: 1, borderColor: R.cizgi }}>
        <View {...surukle.panHandlers} style={{ alignItems: "center", paddingVertical: 8, flexDirection: "row", justifyContent: "center" }}>
          <View style={{ width: 44, height: 5, borderRadius: 3, backgroundColor: "rgba(255,255,255,0.3)" }} />
          <Pressable onPress={buyut} hitSlop={12} style={{ position: "absolute", right: 54 }}><Text style={{ color: "#fff", fontSize: 18 }}>⤢</Text></Pressable>
          <Pressable onPress={kapat} hitSlop={12} style={{ position: "absolute", right: 18 }}><Text style={{ color: "#fff", fontSize: 18 }}>✕</Text></Pressable>
        </View>
        <View style={{ flex: 1, paddingBottom: ic.bottom }}><CanliEkrani mini sohbeteGonder={sohbeteGonder} /></View>
      </Animated.View>
    </View>
  );
}

export default function App() {
  const [hazir, setHazir] = useState(false);
  const [kilitli, setKilitli] = useState(false);
  useEffect(() => {
    if (Platform.OS === "web" && typeof document !== "undefined") {
      // Masaüstü/web: tarayıcının turuncu odak çerçevesi tasarımı bozmasın; ince kaydırma çubukları
      const st = document.createElement("style");
      st.textContent = "input,textarea{outline:none!important;caret-color:#22d3ee}::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.14);border-radius:8px}::-webkit-scrollbar-track{background:transparent}body{background:#050816}";
      document.head.appendChild(st);
      // Masaüstü (Electron): macOS kum havuzu sistem emoji fontunu engelliyor → açık kaynak Noto Color Emoji web fontu,
      // yalnızca emoji karakter aralıklarına ("Segoe UI" adıyla, yığındaki yerine) uygulanır; yazı ve simgeler etkilenmez
      if (/Electron/.test(navigator.userAgent)) {
        fetch("https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&display=swap").then((r) => r.text()).then((css) => {
          const ef = document.createElement("style");
          ef.textContent = css + css.replace(/font-family: 'Noto Color Emoji'/g, "font-family: 'Segoe UI'");
          document.head.appendChild(ef);
        }).catch(() => {});
      }
    }
    SystemUI.setBackgroundColorAsync(R.bg1).catch(() => {});
    Promise.all([anahtarlariYukle(), kilitAcikMi().then(setKilitli)]).finally(() => setHazir(true));
  }, []);
  return (
    <SafeAreaProvider>
      <AyarSaglayici>
        {hazir && kilitli ? <KilitEkrani acildi={() => setKilitli(false)} /> : hazir ? <Uygulama /> : (
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
