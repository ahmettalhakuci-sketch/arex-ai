// AREX — 🔬 Fotoğraf & Video Analiz Laboratuvarı (Gemini görsel zekâ + cihaz içi matematik doğrulaması)
import * as Clipboard from "expo-clipboard";
import React, { useState } from "react";
import { Image, Text, View, ScrollView } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { medyaAnaliz } from "../ai";
import { ANALIZLER, analizTalimati, ETIK, TAM_RAPOR } from "../analiz";
import { SYMPY_KURALI, yanitiDogrula } from "../matematik";
import { medyaSec, type Ek } from "../medya";
import { DILLER, R } from "../tema";
import { Baslik, Dugme, Girdi, Kart, MdMetin, s as us, Secici } from "../ui";

export default function AnalizEkrani({ sohbeteGonder }: { sohbeteGonder: (metin: string, cevap: string) => void }) {
  const ic = useSafeAreaInsets();
  const [ek, setEk] = useState<Ek | null>(null);
  const [turler, setTurler] = useState<string[]>(["genel"]);
  const [dil, setDil] = useState("tr");
  const [not, setNot] = useState("");
  const [bekle, setBekle] = useState(false);
  const [sonuc, setSonuc] = useState<{ metin: string; motor: string } | null>(null);

  const sec = async (k: "galeri" | "kamera" | "video") => {
    const e = await medyaSec(k);
    if (e) { setEk(e); setSonuc(null); setTurler(e.video ? ["v_genel"] : ["genel"]); }
  };
  const uygun = Object.entries(ANALIZLER).filter(([, v]) => !!v.video === !!ek?.video);

  const baslat = async () => {
    if (!ek) return;
    setBekle(true); setSonuc(null);
    const { talimat, derin, maks } = analizTalimati(turler, not);
    const r = await medyaAnaliz(ek.b64, ek.mime, talimat + (ek.video ? "" : SYMPY_KURALI), { sistem: ETIK(DILLER[dil]?.ad || "Türkçe"), derin: derin || ek.video || turler.includes("ders"), maks });
    setBekle(false);
    setSonuc(r.metin ? { metin: yanitiDogrula(r.metin), motor: r.motor } : { metin: "⚠️ " + r.motor, motor: "" });
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 40 }}>
      <Baslik alt="Gemini görsel zekâsıyla sistematik analiz. Kişi tanıma yapılmaz; duygular görünen ifade olarak, kanıt ve güven düzeyiyle raporlanır. Tamamen cihaz içi analiz için 🎙️ Canlı → 🧠 Yerel Analiz.">🔬 Analiz Laboratuvarı</Baslik>
      <View style={{ flexDirection: "row", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
        <Dugme kucuk yazi="📷 Fotoğraf çek" onPress={() => sec("kamera")} />
        <Dugme kucuk ikincil yazi="🖼️ Galeri" onPress={() => sec("galeri")} />
        <Dugme kucuk ikincil yazi="🎬 Video" onPress={() => sec("video")} />
      </View>
      {ek ? (
        <Kart>
          {ek.video ? <Text style={{ color: "#fff", fontWeight: "700" }}>🎬 {ek.ad}</Text> : <Image source={{ uri: ek.onizleme }} style={{ width: 220, height: 220, borderRadius: 16, alignSelf: "center" }} />}
          <View style={{ height: 12 }} />
          {!ek.video ? <Dugme kucuk ikincil yazi="🧩 Tam sistematik rapor (genel + ifade + yüz + beden + risk + kalite)" onPress={() => setTurler(TAM_RAPOR)} style={{ marginBottom: 10 }} /> : null}
          <Secici coklu etiket="Analiz türleri (birden çok seçebilirsin)" deger={turler} onChange={setTurler} secenekler={uygun.map(([k, v]) => ({ k, ad: v.ad }))} />
          <Secici etiket="Rapor dili" deger={dil} onChange={setDil} secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />
          <Girdi etiket="Not / soru (isteğe bağlı)" value={not} onChangeText={setNot} placeholder="ör. soldaki kişi tedirgin görünüyor mu?" />
          <Dugme yazi="🔬 Analizi Başlat" onPress={baslat} yukleniyor={bekle} />
          {bekle ? <Text style={[us.alt, { textAlign: "center", marginTop: 8 }]}>{ek.video ? "Video izleniyor… (20-60 sn)" : "İnceleniyor…"}</Text> : null}
        </Kart>
      ) : (
        <Kart><Text style={us.alt}>📸 Bir fotoğraf ya da kısa video seç (≤18 MB). Sonra analiz türlerini işaretle: ifade & gerginlik, yüz şekli, beden dili, kavga riski, soru çözme, yazı okuma, kalite, kalori, bitki/hayvan…</Text></Kart>
      )}
      {sonuc ? (
        <Kart>
          <MdMetin>{sonuc.metin}</MdMetin>
          <Text style={{ color: R.soluk, fontSize: 11, marginTop: 6 }}>🏷️ {sonuc.motor}</Text>
          <View style={{ flexDirection: "row", gap: 8, marginTop: 10 }}>
            <Dugme kucuk ikincil yazi="📋 Kopyala" onPress={() => Clipboard.setStringAsync(sonuc.metin)} />
            <Dugme kucuk ikincil yazi="💬 Sohbete gönder" onPress={() => sohbeteGonder(`🔬 ${ek?.video ? "Video" : "Fotoğraf"} analizi${not ? ": " + not : ""}`, sonuc.metin)} />
          </View>
        </Kart>
      ) : null}
    </ScrollView>
  );
}
