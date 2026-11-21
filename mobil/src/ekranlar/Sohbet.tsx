// AREX — ana sohbet ekranı (Gemini tarzı ek önizleme, sesli yazma, doğal sesli dinleme, geçmiş)
import { RecordingPresets, requestRecordingPermissionsAsync, setAudioModeAsync, useAudioRecorder } from "expo-audio";
import * as Clipboard from "expo-clipboard";
import { LinearGradient } from "expo-linear-gradient";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { ActivityIndicator, Alert, FlatList, Image, KeyboardAvoidingView, Modal, Platform, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { medyaAnaliz, sesiYaziyaDok, type Rol } from "../ai";
import { analizTalimati, ETIK, turTahmin } from "../analiz";
import { useAyar } from "../ayar";
import { cevapUret } from "../beyin";
import { sohbetKaydet, sohbetleriOku, sohbetSil, sohbettenOgren, yeniId, type Mesaj, type Sohbet } from "../depo";
import { medyaSec, type Ek } from "../medya";
import { anlat, sesiDurdur } from "../ses";
import { DILLER, GRADYAN, R, RTL_DILLER, yazidanDilTahmin } from "../tema";
import { MdMetin, titret } from "../ui";

const ONERILER = [
  "✨ Bana ilginç bir bilgi ver", "🧠 Beni tanıyor musun?", "📖 Kısa bir hikâye anlat", "🌤️ İstanbul hava durumu",
  "🧮 Bir matematik sorusu sor", "🌍 'Merhaba dostum' Bengalce, Arapça ve Rusça nasıl denir?",
];

export default function SohbetEkrani({ disaridanMesaj, temizle }: { disaridanMesaj?: { metin: string; cevap: string } | null; temizle?: () => void }) {
  const { ayar } = useAyar();
  const ic = useSafeAreaInsets();
  const [sohbet, setSohbet] = useState<Sohbet>({ id: yeniId(), baslik: "Yeni sohbet", mesajlar: [], guncel: Date.now() });
  const [girdi, setGirdi] = useState("");
  const [ek, setEk] = useState<Ek | null>(null);
  const [bekliyor, setBekliyor] = useState(false);
  const [kayitta, setKayitta] = useState(false);
  const [ekMenu, setEkMenu] = useState(false);
  const [gecmisAcik, setGecmisAcik] = useState(false);
  const [gecmis, setGecmis] = useState<Sohbet[]>([]);
  const [konusan, setKonusan] = useState<string | null>(null);
  const liste = useRef<FlatList<Mesaj>>(null);
  const kaydedici = useAudioRecorder(RecordingPresets.HIGH_QUALITY);

  useEffect(() => { sohbetleriOku().then((l) => l[0] && setSohbet(l[0])); }, []);
  useEffect(() => {
    if (disaridanMesaj) {
      ekle([{ id: yeniId(), rol: "user", metin: disaridanMesaj.metin, zaman: Date.now() },
        { id: yeniId(), rol: "assistant", metin: disaridanMesaj.cevap, etiket: "🔬 Analiz", zaman: Date.now() }]);
      temizle?.();
    }
  }, [disaridanMesaj]);

  const ekle = useCallback((yeni: Mesaj[]) => {
    setSohbet((s) => {
      const mesajlar = [...s.mesajlar, ...yeni];
      const ilk = mesajlar.find((m) => m.rol === "user");
      const g = { ...s, mesajlar, guncel: Date.now(), baslik: ilk ? ilk.metin.slice(0, 40) : s.baslik };
      sohbetKaydet(g);
      return g;
    });
  }, []);

  const gonder = async (hazirMetin?: string) => {
    const metin = (hazirMetin ?? girdi).trim();
    if ((!metin && !ek) || bekliyor) return;
    titret();
    setGirdi("");
    const ekSimdi = ek;
    setEk(null);
    const kullanici: Mesaj = { id: yeniId(), rol: "user", metin: metin || (ekSimdi?.video ? "🎬 Bu videoyu analiz et" : "📸 Bu fotoğrafı analiz et"),
      gorsel: ekSimdi && !ekSimdi.video ? ekSimdi.onizleme : undefined, video: ekSimdi?.video ? ekSimdi.ad : undefined, zaman: Date.now() };
    const onceki = sohbet.mesajlar;
    ekle([kullanici]);
    setBekliyor(true);
    try {
      const ogrenilen = await sohbettenOgren(metin);
      let cevap: string, motor: string;
      if (ekSimdi) {
        const turler = turTahmin(metin, ekSimdi.video);
        const { talimat, derin, maks } = analizTalimati(turler.length || metin ? turler : [ekSimdi.video ? "v_genel" : "genel"], metin);
        const dil = DILLER[yazidanDilTahmin(metin) || ayar.yanitDili]?.ad || "Türkçe";
        const gec: Rol[] = onceki.slice(-6).map((m) => ({ role: m.rol, content: m.metin }));
        const r = await medyaAnaliz(ekSimdi.b64, ekSimdi.mime, talimat, { sistem: ETIK(dil), gecmis: gec, derin: derin || ekSimdi.video, maks });
        cevap = r.metin || "⚠️ " + r.motor;
        motor = r.metin ? r.motor : "Görsel analiz";
      } else {
        const r = await cevapUret(onceki, metin, ayar);
        cevap = r.metin; motor = r.motor;
      }
      const yanit: Mesaj = { id: yeniId(), rol: "assistant", metin: cevap, etiket: motor + (ogrenilen ? " • 🧠 hafızaya eklendi" : ""), zaman: Date.now() };
      ekle([yanit]);
      if (ayar.otomatikSes) dinle(yanit);
    } finally {
      setBekliyor(false);
    }
  };

  const dinle = async (m: Mesaj) => {
    if (konusan === m.id) { await sesiDurdur(); setKonusan(null); return; }
    setKonusan(m.id);
    const dil = yazidanDilTahmin(m.metin) || ayar.yanitDili;
    await anlat(m.metin, dil, "sohbet", ayar.anlatici, ayar.dogalSes);
  };

  const mikrofon = async () => {
    if (kayitta) {
      setKayitta(false);
      await kaydedici.stop();
      const uri = kaydedici.uri;
      if (!uri) return;
      setBekliyor(true);
      const metin = await sesiYaziyaDok(uri);
      setBekliyor(false);
      if (metin) gonder(metin);
      else Alert.alert("Anlaşılamadı", "Ses yazıya dökülemedi, tekrar dener misin?");
      return;
    }
    const izin = await requestRecordingPermissionsAsync();
    if (!izin.granted) { Alert.alert("İzin gerekli", "Sesli yazmak için mikrofon izni ver."); return; }
    await setAudioModeAsync({ allowsRecording: true, playsInSilentMode: true });
    await kaydedici.prepareToRecordAsync();
    kaydedici.record();
    setKayitta(true);
    titret();
  };

  const ekSec = async (k: "galeri" | "kamera" | "video") => {
    setEkMenu(false);
    const e = await medyaSec(k);
    if (e) setEk(e);
  };

  const yeniSohbet = () => { sesiDurdur(); setSohbet({ id: yeniId(), baslik: "Yeni sohbet", mesajlar: [], guncel: Date.now() }); };

  const balon = ({ item: m }: { item: Mesaj }) => {
    const ben = m.rol === "user";
    const rtl = RTL_DILLER.has(yazidanDilTahmin(m.metin));
    return (
      <View style={[st.satir, ben ? { justifyContent: "flex-end" } : null]}>
        {!ben && <LinearGradient colors={GRADYAN as unknown as string[]} style={st.avatar}><Text style={{ fontSize: 15 }}>⚡</Text></LinearGradient>}
        <View style={[st.balon, ben ? st.balonBen : st.balonO]}>
          {m.gorsel ? <Image source={{ uri: m.gorsel }} style={st.onizleme} resizeMode="cover" /> : null}
          {m.video ? <Text style={st.videoEtiket}>🎬 {m.video}</Text> : null}
          {ben ? <Text style={[st.benYazi, rtl && { textAlign: "right" }]}>{m.metin}</Text> : <MdMetin rtl={rtl}>{m.metin}</MdMetin>}
          {!ben && (
            <View style={st.altSatir}>
              <Text style={st.etiket} numberOfLines={1}>{m.etiket}</Text>
              <Pressable hitSlop={8} onPress={() => dinle(m)}><Text style={st.ikon}>{konusan === m.id ? "⏹" : "🔊"}</Text></Pressable>
              <Pressable hitSlop={8} onPress={() => { Clipboard.setStringAsync(m.metin); titret(); }}><Text style={st.ikon}>📋</Text></Pressable>
            </View>
          )}
        </View>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === "ios" ? "padding" : undefined}>
      <View style={[st.ust, { paddingTop: ic.top + 6 }]}>
        <Pressable onPress={async () => { setGecmis(await sohbetleriOku()); setGecmisAcik(true); }} hitSlop={10}><Text style={st.ustIkon}>☰</Text></Pressable>
        <View style={{ alignItems: "center" }}>
          <Text style={st.marka}>⚡ AREX <Text style={{ color: R.acc2 }}>AI</Text></Text>
          <Text style={st.durum}>{ayar.cocukModu ? "🧸 Çocuk modu • " : ""}{DILLER[ayar.yanitDili]?.bayrak} çok dilli • bağlamlı</Text>
        </View>
        <Pressable onPress={yeniSohbet} hitSlop={10}><Text style={st.ustIkon}>✚</Text></Pressable>
      </View>

      <FlatList
        ref={liste}
        data={sohbet.mesajlar}
        keyExtractor={(m) => m.id}
        renderItem={balon}
        contentContainerStyle={{ padding: 12, paddingBottom: 20, flexGrow: 1 }}
        onContentSizeChange={() => liste.current?.scrollToEnd({ animated: true })}
        keyboardShouldPersistTaps="handled"
        ListEmptyComponent={
          <View style={st.bos}>
            <LinearGradient colors={GRADYAN as unknown as string[]} style={st.bosKure}><Text style={{ fontSize: 40 }}>⚡</Text></LinearGradient>
            <Text style={st.bosBaslik}>Merhaba! Bugün ne yapalım?</Text>
            <Text style={st.bosAlt}>Yaz, konuş ya da 📎 ile fotoğraf/video ekle. Her dilde konuşabilirim.</Text>
            <View style={st.oneriler}>
              {ONERILER.map((o) => (
                <Pressable key={o} style={st.oneri} onPress={() => gonder(o.replace(/^\S+\s/, ""))}><Text style={st.oneriYazi}>{o}</Text></Pressable>
              ))}
            </View>
          </View>
        }
        ListFooterComponent={bekliyor ? <View style={st.yaziyor}><ActivityIndicator color={R.acc2} /><Text style={st.yaziyorYazi}>AREX düşünüyor…</Text></View> : null}
      />

      <View style={[st.alt, { paddingBottom: Math.max(ic.bottom, 8) }]}>
        {ek ? (
          <View style={st.ekKutu}>
            {ek.video ? <View style={st.ekVideo}><Text style={{ fontSize: 22 }}>🎬</Text></View> : <Image source={{ uri: ek.onizleme }} style={st.ekResim} />}
            <Text style={st.ekAd} numberOfLines={1}>{ek.video ? ek.ad : "Fotoğraf eklendi"} — ne sormak istersin? (ör. "tedirgin mi?", "yüz tipim?", "soruyu çöz")</Text>
            <Pressable onPress={() => setEk(null)} hitSlop={10}><Text style={st.ekSil}>✕</Text></Pressable>
          </View>
        ) : null}
        <View style={st.cubuk}>
          <Pressable style={st.yuvarlak} onPress={() => setEkMenu(true)}><Text style={st.cubukIkon}>📎</Text></Pressable>
          <TextInput
            style={st.girdi} value={girdi} onChangeText={setGirdi} placeholder={kayitta ? "🎙️ Dinliyorum… bitince tekrar dokun" : "AREX'e yaz…"}
            placeholderTextColor={R.soluk} multiline maxLength={6000}
            onSubmitEditing={() => Platform.OS === "web" && gonder()} blurOnSubmit={false}
          />
          {girdi.trim() || ek ? (
            <Pressable onPress={() => gonder()} disabled={bekliyor}>
              <LinearGradient colors={GRADYAN as unknown as string[]} style={st.gonder}><Text style={st.gonderIkon}>➤</Text></LinearGradient>
            </Pressable>
          ) : (
            <Pressable style={[st.yuvarlak, kayitta && { backgroundColor: R.kirmizi }]} onPress={mikrofon}><Text style={st.cubukIkon}>{kayitta ? "⏹" : "🎙️"}</Text></Pressable>
          )}
        </View>
      </View>

      <Modal visible={ekMenu} transparent animationType="fade" onRequestClose={() => setEkMenu(false)}>
        <Pressable style={st.perde} onPress={() => setEkMenu(false)}>
          <View style={[st.menu, { paddingBottom: ic.bottom + 16 }]}>
            {[["📷  Fotoğraf çek", "kamera"], ["🖼️  Galeriden fotoğraf", "galeri"], ["🎬  Video seç (≤18 MB)", "video"]].map(([a, k]) => (
              <Pressable key={k} style={st.menuSatir} onPress={() => ekSec(k as any)}><Text style={st.menuYazi}>{a}</Text></Pressable>
            ))}
          </View>
        </Pressable>
      </Modal>

      <Modal visible={gecmisAcik} transparent animationType="slide" onRequestClose={() => setGecmisAcik(false)}>
        <Pressable style={st.perde} onPress={() => setGecmisAcik(false)}>
          <View style={[st.menu, { maxHeight: "75%", paddingBottom: ic.bottom + 16 }]}>
            <Text style={[st.menuYazi, { fontWeight: "800", marginBottom: 8 }]}>💬 Sohbet geçmişi</Text>
            <FlatList data={gecmis} keyExtractor={(x) => x.id} renderItem={({ item }) => (
              <View style={st.gecmisSatir}>
                <Pressable style={{ flex: 1 }} onPress={() => { setSohbet(item); setGecmisAcik(false); }}>
                  <Text style={st.menuYazi} numberOfLines={1}>{item.baslik}</Text>
                  <Text style={st.durum}>{new Date(item.guncel).toLocaleString("tr-TR")} • {item.mesajlar.length} mesaj</Text>
                </Pressable>
                <Pressable hitSlop={10} onPress={async () => { await sohbetSil(item.id); setGecmis(await sohbetleriOku()); }}><Text style={st.ikon}>🗑️</Text></Pressable>
              </View>
            )} ListEmptyComponent={<Text style={st.durum}>Henüz kayıtlı sohbet yok.</Text>} />
          </View>
        </Pressable>
      </Modal>
    </KeyboardAvoidingView>
  );
}

const st = StyleSheet.create({
  ust: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", paddingHorizontal: 16, paddingBottom: 8, borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.06)" },
  ustIkon: { color: R.yazi, fontSize: 24, width: 32, textAlign: "center" },
  marka: { color: "#fff", fontSize: 18, fontWeight: "800" },
  durum: { color: R.soluk, fontSize: 11.5, marginTop: 2 },
  satir: { flexDirection: "row", alignItems: "flex-end", marginBottom: 12, gap: 8 },
  avatar: { width: 30, height: 30, borderRadius: 15, alignItems: "center", justifyContent: "center" },
  balon: { maxWidth: "86%", borderRadius: 20, paddingHorizontal: 14, paddingVertical: 10 },
  balonBen: { backgroundColor: "rgba(124,92,255,0.42)", borderBottomRightRadius: 6 },
  balonO: { backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi, borderBottomLeftRadius: 6, flexShrink: 1 },
  benYazi: { color: "#fff", fontSize: 16, lineHeight: 23 },
  onizleme: { width: 200, height: 200, borderRadius: 14, marginBottom: 6, alignSelf: "flex-end" },
  videoEtiket: { color: "#fff", fontWeight: "700", marginBottom: 4 },
  altSatir: { flexDirection: "row", alignItems: "center", gap: 14, marginTop: 6 },
  etiket: { color: R.soluk, fontSize: 11, flex: 1 },
  ikon: { fontSize: 17 },
  bos: { flex: 1, alignItems: "center", justifyContent: "center", paddingVertical: 30 },
  bosKure: { width: 88, height: 88, borderRadius: 44, alignItems: "center", justifyContent: "center", marginBottom: 16, shadowColor: R.acc, shadowOpacity: 0.7, shadowRadius: 30, elevation: 12 },
  bosBaslik: { color: "#fff", fontSize: 22, fontWeight: "800" },
  bosAlt: { color: R.soluk, fontSize: 14, marginTop: 6, textAlign: "center", paddingHorizontal: 20 },
  oneriler: { flexDirection: "row", flexWrap: "wrap", gap: 8, justifyContent: "center", marginTop: 20, paddingHorizontal: 6 },
  oneri: { backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi, borderRadius: 16, paddingHorizontal: 12, paddingVertical: 10, maxWidth: "48%" },
  oneriYazi: { color: R.yazi, fontSize: 13.5 },
  yaziyor: { flexDirection: "row", alignItems: "center", gap: 8, paddingLeft: 40 },
  yaziyorYazi: { color: R.soluk, fontSize: 13 },
  alt: { paddingHorizontal: 10, paddingTop: 6, borderTopWidth: 1, borderTopColor: "rgba(255,255,255,0.06)", backgroundColor: "rgba(5,8,22,0.85)" },
  ekKutu: { flexDirection: "row", alignItems: "center", gap: 10, backgroundColor: R.kart, borderRadius: 16, padding: 8, marginBottom: 6, borderWidth: 1, borderColor: R.cizgi },
  ekResim: { width: 52, height: 52, borderRadius: 12 },
  ekVideo: { width: 52, height: 52, borderRadius: 12, backgroundColor: "rgba(124,92,255,0.35)", alignItems: "center", justifyContent: "center" },
  ekAd: { color: R.soluk, flex: 1, fontSize: 12.5 },
  ekSil: { color: R.yazi, fontSize: 18, paddingHorizontal: 6 },
  cubuk: { flexDirection: "row", alignItems: "flex-end", gap: 8 },
  yuvarlak: { width: 46, height: 46, borderRadius: 23, backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi, alignItems: "center", justifyContent: "center" },
  cubukIkon: { fontSize: 20 },
  girdi: { flex: 1, minHeight: 46, maxHeight: 140, backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi, borderRadius: 23, color: R.yazi, paddingHorizontal: 16, paddingTop: 12, paddingBottom: 12, fontSize: 16 },
  gonder: { width: 46, height: 46, borderRadius: 23, alignItems: "center", justifyContent: "center" },
  gonderIkon: { color: "#fff", fontSize: 20, fontWeight: "800" },
  perde: { flex: 1, backgroundColor: "rgba(0,0,0,0.55)", justifyContent: "flex-end" },
  menu: { backgroundColor: R.bg2, borderTopLeftRadius: 26, borderTopRightRadius: 26, padding: 18, borderWidth: 1, borderColor: R.cizgi },
  menuSatir: { paddingVertical: 16, borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.06)" },
  menuYazi: { color: R.yazi, fontSize: 17 },
  gecmisSatir: { flexDirection: "row", alignItems: "center", paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.06)", gap: 10 },
});
