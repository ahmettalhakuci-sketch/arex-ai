// AREX — ana sohbet ekranı (Gemini tarzı ek önizleme, sesli yazma, doğal sesli dinleme, geçmiş)
import { getRecordingPermissionsAsync, RecordingPresets, requestRecordingPermissionsAsync, setAudioModeAsync, useAudioRecorder } from "expo-audio";
import * as Clipboard from "expo-clipboard";
import { LinearGradient } from "expo-linear-gradient";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { ActivityIndicator, Alert, FlatList, Image, KeyboardAvoidingView, Modal, Platform, Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { medyaAnaliz, sesiYaziyaDok, type Rol } from "../ai";
import { analizTalimati, ETIK, turTahmin } from "../analiz";
import { useAyar } from "../ayar";
import { cevapUret, KULLANIM_MODLARI, SOHBET_TARZLARI } from "../beyin";
import { notKomutu, sohbetKaydet, sohbetleriOku, sohbettenOgren, yeniId, type Mesaj, type Sohbet } from "../depo";
import GecmisPaneli from "../GecmisPaneli";
import { telefonKomutu } from "../telefon";
import { izinIste } from "../izin";
import { SYMPY_KURALI, yanitiDogrula } from "../matematik";
import { medyaSec, type Ek } from "../medya";
import { anlat, sesiDurdur } from "../ses";
import { DILLER, GRADYAN, R, RTL_DILLER, yazidanDilTahmin } from "../tema";
import { MdMetin, titret } from "../ui";

const ONERILER = [
  "✨ Bana ilginç bir bilgi ver", "🧠 Beni tanıyor musun?", "📖 Kısa bir hikâye anlat", "🌤️ İstanbul hava durumu",
  "🧮 Bir matematik sorusu sor", "🌍 'Merhaba dostum' Bengalce, Arapça ve Rusça nasıl denir?",
];

export default function SohbetEkrani({ disaridanMesaj, temizle, canliyaGit }: { disaridanMesaj?: { metin: string; cevap: string } | null; temizle?: () => void; canliyaGit?: () => void }) {
  const { ayar, guncelle } = useAyar();
  const ic = useSafeAreaInsets();
  const [sohbet, setSohbet] = useState<Sohbet>({ id: yeniId(), baslik: "Yeni sohbet", mesajlar: [], guncel: Date.now() });
  const [girdi, setGirdi] = useState("");
  const [ek, setEk] = useState<Ek | null>(null);
  const [bekliyor, setBekliyor] = useState(false);
  const [kayitta, setKayitta] = useState(false);
  const [ekMenu, setEkMenu] = useState(false);
  const [gecmisAcik, setGecmisAcik] = useState(false);
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
      const kisisel = (ayar.kullanimModu || "kisisel") === "kisisel";
      // 📱 Telefon komutları: "YouTube aç", "YouTube'da X ara", "WhatsApp aç", "haritada X göster", "05xx ara"
      if (!ekSimdi) {
        const tel = await telefonKomutu(metin);
        if (tel) { ekle([{ id: yeniId(), rol: "assistant", metin: tel, etiket: "📱 Telefon", zaman: Date.now() }]); return; }
      }
      // 🎭 Sohbet tarzı / mod komutları: "mizah modu aç", "içten sohbet modu", "mümin modu", "normal moda dön", "genç modu"
      if (!ekSimdi) {
        const tl = metin.toLocaleLowerCase("tr");
        const kapat = /(kapat|kapa|bitir|normal moda|dengeli moda)/.test(tl);
        let tarz: string | null = null, kmod: string | null = null;
        if (/mizah mod/.test(tl)) tarz = kapat ? "dengeli" : "mizah";
        else if (/içten (sohbet )?mod|icten (sohbet )?mod/.test(tl)) tarz = kapat ? "dengeli" : "icten";
        else if (/m[üu]min mod|m[üu]'?min mod/.test(tl)) tarz = kapat ? "dengeli" : "mumin";
        else if (/normal moda d[öo]n|dengeli moda/.test(tl)) tarz = "dengeli";
        if (/^(?:genç|genc) mod/.test(tl)) kmod = "genc"; else if (/^yetişkin mod/.test(tl)) kmod = "yetiskin";
        else if (/^(?:misafir|genel) mod/.test(tl)) kmod = "genel"; else if (/^kişisel mod|^kisisel mod/.test(tl)) kmod = "kisisel";
        if (tarz || kmod) {
          guncelle({ ...(tarz ? { sohbetTarzi: tarz } : {}), ...(kmod ? { kullanimModu: kmod } : {}) });
          const ad = tarz ? SOHBET_TARZLARI[tarz].ad : KULLANIM_MODLARI[kmod!];
          const selam: Record<string, string> = { mizah: "😄 Mizah modu açıldı! Hazırlan, iltifat yağmuru başlıyor 🎉", icten: "💞 İçten sohbet modu açık. Acele yok; seni dinliyorum…", mumin: "🕌 Mümin modu açık. Hoş geldin, Allah razı olsun.", dengeli: "🎯 Normal (dengeli) moda döndüm." };
          ekle([{ id: yeniId(), rol: "assistant", metin: tarz ? selam[tarz] : `✅ ${ad} açıldı.`, etiket: "🎭 Mod", zaman: Date.now() }]);
          return;
        }
      }
      // 📝 Not komutları (yazılı veya sesli): "notlarıma kaydet: …", "bunu not al", "notlarım", "3. notu sil"
      if (!ekSimdi) {
        const sonCevap = [...onceki].reverse().find((m) => m.rol === "assistant")?.metin || "";
        const notCevap = await notKomutu(metin, sonCevap);
        if (notCevap) {
          ekle([{ id: yeniId(), rol: "assistant", metin: kisisel ? notCevap : "🔒 Notlar yalnızca 👤 Kişisel modda kullanılabilir.", etiket: "📝 Notlarım", zaman: Date.now() }]);
          return;
        }
      }
      const ogrenilen = kisisel ? await sohbettenOgren(metin) : "";
      let cevap: string, motor: string;
      if (ekSimdi && (ayar.kullanimModu || "kisisel") === "genel") {
        cevap = "🔒 Fotoğraf/video analizi misafir modunda kapalı (kişisel API kullanılmaz). 👤 Kişisel moda geçince açılır."; motor = "🔒 Misafir";
      } else if (ekSimdi) {
        const turler = turTahmin(metin, ekSimdi.video);
        const { talimat: t0, derin, maks } = analizTalimati(turler.length || metin ? turler : [], metin);
        const talimat = turler.length ? t0 : t0 + " Görselde bir ders/sınav sorusu veya ödev varsa onu çöz (soruyu yaz, adım adım çöz, sonucu ve doğru şıkkı kalın yaz).";
        const dil = DILLER[yazidanDilTahmin(metin) || ayar.yanitDili]?.ad || "Türkçe";
        const gec: Rol[] = onceki.slice(-6).map((m) => ({ role: m.rol, content: m.metin }));
        const r = await medyaAnaliz(ekSimdi.b64, ekSimdi.mime, talimat + (ekSimdi.video ? "" : SYMPY_KURALI), { sistem: ETIK(dil), gecmis: gec, derin: derin || ekSimdi.video, maks });
        cevap = r.metin ? yanitiDogrula(r.metin) : "⚠️ " + r.motor;
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
    await anlat(m.metin, dil, "sohbet", ayar.anlatici, ayar.dogalSes && (ayar.kullanimModu || "kisisel") !== "genel");
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
    if (!(await izinIste("Mikrofon", requestRecordingPermissionsAsync, getRecordingPermissionsAsync))) return;
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
        {!ben && <LinearGradient colors={GRADYAN } style={st.avatar}><Text style={{ fontSize: 15 }}>⚡</Text></LinearGradient>}
        <View style={[st.balon, ben ? [st.balonBen, { backgroundColor: R.balon }] : st.balonO]}>
          {m.gorsel ? <Image source={{ uri: m.gorsel }} style={st.onizleme} resizeMode="cover" /> : null}
          {m.video ? <Text style={st.videoEtiket}>🎬 {m.video}</Text> : null}
          {ben ? <Text style={[st.benYazi, { fontSize: 16 * (R.olcek || 1), lineHeight: 23 * (R.olcek || 1) }, rtl && { textAlign: "right" }]}>{m.metin}</Text> : <MdMetin rtl={rtl}>{m.metin}</MdMetin>}
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
        <Pressable onPress={() => setGecmisAcik(true)} hitSlop={10}><Text style={st.ustIkon}>☰</Text></Pressable>
        <View style={{ alignItems: "center" }}>
          <Text style={st.marka}>⚡ AREX <Text style={{ color: R.acc2 }}>AI</Text></Text>
          <Text style={st.durum}>{KULLANIM_MODLARI[ayar.kullanimModu || "kisisel"]}{ayar.sohbetTarzi && ayar.sohbetTarzi !== "dengeli" ? " • " + SOHBET_TARZLARI[ayar.sohbetTarzi].ad : ""}</Text>
        </View>
        <View style={{ flexDirection: "row", gap: 6 }}>
          <Pressable onPress={() => guncelle({ gozKoruma: !ayar.gozKoruma })} hitSlop={10}><Text style={[st.ustIkon, { opacity: ayar.gozKoruma ? 1 : 0.55 }]}>👁️</Text></Pressable>
          <Pressable onPress={yeniSohbet} hitSlop={10}><Text style={st.ustIkon}>✚</Text></Pressable>
        </View>
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
            <LinearGradient colors={GRADYAN } style={st.bosKure}><Text style={{ fontSize: 40 }}>⚡</Text></LinearGradient>
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
            blurOnSubmit={false}
            onKeyPress={(e: any) => {
              // Bilgisayarda Enter = gönder, Shift+Enter = yeni satır
              if (Platform.OS === "web" && e.nativeEvent.key === "Enter" && !e.nativeEvent.shiftKey) { e.preventDefault?.(); gonder(); }
            }}
          />
          {girdi.trim() || ek ? (
            <Pressable onPress={() => gonder()} disabled={bekliyor}>
              <LinearGradient colors={GRADYAN } style={st.gonder}><Text style={st.gonderIkon}>➤</Text></LinearGradient>
            </Pressable>
          ) : (
            <View style={{ flexDirection: "row", gap: 8 }}>
              <Pressable style={[st.yuvarlak, kayitta && { backgroundColor: R.kirmizi }]} onPress={mikrofon}><Text style={st.cubukIkon}>{kayitta ? "⏹" : "🎙️"}</Text></Pressable>
              {!kayitta && canliyaGit ? (
                <Pressable onPress={canliyaGit} accessibilityLabel="Canlı sohbet">
                  <LinearGradient colors={GRADYAN} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={st.gonder}><Text style={{ fontSize: 19 }}>✨</Text></LinearGradient>
                </Pressable>
              ) : null}
            </View>
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

      <GecmisPaneli acik={gecmisAcik} kapat={() => setGecmisAcik(false)} sec={(x) => { sesiDurdur(); setSohbet(x); }} aktifId={sohbet.id} />
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
  oneri: { backgroundColor: "rgba(124,92,255,0.09)", borderWidth: 1, borderColor: "rgba(162,140,255,0.28)", borderRadius: 18, paddingHorizontal: 12, paddingVertical: 10, maxWidth: "48%" },
  oneriYazi: { color: R.yazi, fontSize: 13.5 },
  yaziyor: { flexDirection: "row", alignItems: "center", gap: 8, paddingLeft: 40 },
  yaziyorYazi: { color: R.soluk, fontSize: 13 },
  alt: { paddingHorizontal: 10, paddingTop: 8, paddingBottom: 2, borderTopWidth: 1, borderTopColor: "rgba(162,140,255,0.16)", backgroundColor: "rgba(7,10,28,0.94)" },
  ekKutu: { flexDirection: "row", alignItems: "center", gap: 10, backgroundColor: R.kart, borderRadius: 16, padding: 8, marginBottom: 6, borderWidth: 1, borderColor: R.cizgi },
  ekResim: { width: 52, height: 52, borderRadius: 12 },
  ekVideo: { width: 52, height: 52, borderRadius: 12, backgroundColor: "rgba(124,92,255,0.35)", alignItems: "center", justifyContent: "center" },
  ekAd: { color: R.soluk, flex: 1, fontSize: 12.5 },
  ekSil: { color: R.yazi, fontSize: 18, paddingHorizontal: 6 },
  cubuk: { flexDirection: "row", alignItems: "flex-end", gap: 8 },
  yuvarlak: { width: 46, height: 46, borderRadius: 23, backgroundColor: "rgba(255,255,255,0.07)", borderWidth: 1, borderColor: "rgba(255,255,255,0.14)", alignItems: "center", justifyContent: "center" },
  cubukIkon: { fontSize: 20 },
  girdi: { flex: 1, minHeight: 46, maxHeight: 140, backgroundColor: "rgba(124,92,255,0.10)", borderWidth: 1.2, borderColor: "rgba(162,140,255,0.38)", borderRadius: 23, color: R.yazi, paddingHorizontal: 16, paddingTop: 12, paddingBottom: 12, fontSize: 16 },
  gonder: { width: 46, height: 46, borderRadius: 23, alignItems: "center", justifyContent: "center", shadowColor: "#a259ff", shadowOpacity: 0.6, shadowRadius: 10, elevation: 6 },
  gonderIkon: { color: "#fff", fontSize: 20, fontWeight: "800" },
  perde: { flex: 1, backgroundColor: "rgba(0,0,0,0.55)", justifyContent: "flex-end" },
  menu: { backgroundColor: R.bg2, borderTopLeftRadius: 26, borderTopRightRadius: 26, padding: 18, borderWidth: 1, borderColor: R.cizgi },
  menuSatir: { paddingVertical: 16, borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.06)" },
  menuYazi: { color: R.yazi, fontSize: 17 },
  gecmisSatir: { flexDirection: "row", alignItems: "center", paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: "rgba(255,255,255,0.06)", gap: 10 },
});
