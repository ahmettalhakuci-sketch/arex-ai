// AREX — 🧸 Çocuk Dünyası: 3 yaş grubu, 18 dil, hikâye atölyesi, sen-seç macerası, sohbet arkadaşları, kitaplık
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Image, Pressable, ScrollView, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ANLATICILAR, sohbetTamamla, type Rol } from "../ai";
import CocukOyunlari from "./CocukOyun";
import { useAyar } from "../ayar";
import { baslikBul, DEGERLER, hikayeIstemi, KARAKTERLER, maceraSistemi, OYUNLAR, resimAdresi, secenekleriAyikla, sohbetSistemi, TEMALAR, tercihDil, TONLAR, TURLER, YAS } from "../cocuk";
import { kitapligaEkle, kitaplikOku, kitapliktanSil, oku, yaz, type KitapKaydi } from "../depo";
import { LinearGradient } from "expo-linear-gradient";
import { anlat, sesiDurdur } from "../ses";
import { DILLER, R, RTL_DILLER } from "../tema";
import { Baslik, Dugme, Girdi, Hap, Kart, MdMetin, s as us, Secici } from "../ui";

type Sekme = "atolye" | "macera" | "arkadas" | "kitaplik" | "oyun";
const USLUP_TUR: Record<string, string> = { uyku: "uyku", komik: "komik", macera: "macera", bilim: "bilgi" };

const YAS_RENK: Record<string, [string, string]> = { "3-6": ["#ffb347", "#ff7eb3"], "7-9": ["#5ee7df", "#7c5cff"], "10-12": ["#4facfe", "#7c5cff"] };
const DOSEMELER: [Sekme, string, string, [string, string]][] = [
  ["atolye", "📖", "Masal & hikâye", ["#ff9a8b", "#ff6a88"]],
  ["macera", "🎭", "Sen seç macerası", ["#a18cd1", "#7c5cff"]],
  ["arkadas", "💬", "Arkadaşımla konuş", ["#43e97b", "#16a085"]],
  ["kitaplik", "🗂️", "Kitaplığım", ["#f6d365", "#fda085"]],
  ["oyun", "🎮", "Eğitici oyunlar", ["#4facfe", "#00c6fb"]],
];

export default function CocukEkrani() {
  const ic = useSafeAreaInsets();
  const { ayar, guncelle } = useAyar();
  const [sekme, setSekme] = useState<Sekme | null>(null);
  const [yas, setYas] = useState(ayar.yas || "7-9");
  const [dil, setDil] = useState(ayar.yanitDili || "tr");
  const [ad, setAd] = useState("");
  const [ayarAcik, setAyarAcik] = useState(false);
  const [konusuyor, setKonusuyor] = useState(false);
  useEffect(() => { oku<string>("arex_cocuk_adi", "").then(setAd); }, []);
  const sesli = async (metin: string, uslup: string) => {
    if (konusuyor) { await sesiDurdur(); setKonusuyor(false); return; }
    setKonusuyor(true);
    await anlat(metin, dil, uslup, ayar.anlatici, ayar.dogalSes);
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 40 }} keyboardShouldPersistTaps="handled">
      <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 12 }}>
        {sekme ? <Pressable onPress={() => setSekme(null)} hitSlop={12} style={{ marginRight: 10 }}><Text style={{ color: "#fff", fontSize: 26 }}>‹</Text></Pressable> : null}
        <View style={{ flex: 1 }}>
          <Text style={{ color: "#fff", fontSize: 26, fontWeight: "800" }}>🧸 Çocuk Dünyası</Text>
          <Text style={{ color: R.soluk, fontSize: 13 }}>{ad ? `Merhaba ${ad}! ` : ""}{DILLER[dil]?.bayrak} {DILLER[dil]?.ad} • {ANLATICILAR[ayar.anlatici]?.ad}</Text>
        </View>
        <Pressable onPress={() => setAyarAcik(!ayarAcik)} hitSlop={10} style={{ backgroundColor: R.kart, borderRadius: 14, padding: 10, borderWidth: 1, borderColor: R.cizgi }}><Text style={{ fontSize: 18 }}>⚙️</Text></Pressable>
      </View>

      {ayarAcik ? (
        <Kart>
          <Girdi etiket="Çocuğun adı" value={ad} onChangeText={(v) => { setAd(v); yaz("arex_cocuk_adi", v); }} placeholder="ör. Elif" />
          <Secici etiket="Dil" deger={dil} onChange={setDil} secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />
          <Secici etiket="🎙️ Anlatıcı sesi" deger={ayar.anlatici} onChange={(v) => guncelle({ anlatici: v })}
            secenekler={Object.entries(ANLATICILAR).map(([k, v]) => ({ k, ad: v.ad }))} />
        </Kart>
      ) : null}

      <View style={{ flexDirection: "row", gap: 10, marginBottom: 14 }}>
        {Object.entries(YAS).map(([k, v]) => (
          <Pressable key={k} style={{ flex: 1 }} onPress={() => { setYas(k); guncelle({ yas: k }); }}>
            <LinearGradient colors={yas === k ? YAS_RENK[k] : ["rgba(255,255,255,0.06)", "rgba(255,255,255,0.03)"]} style={{ borderRadius: 20, paddingVertical: 14, alignItems: "center", borderWidth: 1, borderColor: yas === k ? "transparent" : R.cizgi }}>
              <Text style={{ fontSize: 28 }}>{v.ad.split(" ")[0]}</Text>
              <Text style={{ color: "#fff", fontWeight: "800", marginTop: 2 }}>{k} yaş</Text>
              <Text style={{ color: yas === k ? "#fff" : R.soluk, fontSize: 11 }}>{v.ad.split(" ").slice(1).join(" ")}</Text>
            </LinearGradient>
          </Pressable>
        ))}
      </View>

      {!sekme ? (
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 12 }}>
          {DOSEMELER.map(([k, ikon, ad2, renk]) => (
            <Pressable key={k} style={{ width: k === "oyun" ? "100%" : "47.5%" }} onPress={() => setSekme(k)}>
              <LinearGradient colors={renk} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 24, height: 130, padding: 16, justifyContent: "space-between" }}>
                <Text style={{ fontSize: 40 }}>{ikon}</Text>
                <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16 }}>{ad2}</Text>
              </LinearGradient>
            </Pressable>
          ))}
        </View>
      ) : null}
      {sekme === "atolye" && <Atolye yas={yas} dil={dil} ad={ad} sesli={sesli} konusuyor={konusuyor} />}
      {sekme === "macera" && <Macera yas={yas} dil={dil} ad={ad} sesli={sesli} konusuyor={konusuyor} />}
      {sekme === "arkadas" && <Arkadas yas={yas} dil={dil} ad={ad} sesli={sesli} />}
      {sekme === "kitaplik" && <Kitaplik sesli={sesli} />}
      {sekme === "oyun" && <CocukOyunlari yas={yas} />}
    </ScrollView>
  );
}

type Ortak = { yas: string; dil: string; ad: string; sesli: (m: string, u: string) => void; konusuyor?: boolean };

function Atolye({ yas, dil, ad, sesli, konusuyor }: Ortak) {
  const [tur, setTur] = useState("masal");
  const [tema, setTema] = useState("🎲 Sürpriz");
  const [deger, setDeger] = useState("—");
  const [ton, setTon] = useState(TONLAR[0]);
  const [uzunluk, setUzunluk] = useState("Orta");
  const [yer, setYer] = useState("");
  const [ek, setEk] = useState("");
  const [ceviri, setCeviri] = useState("tr");
  const [resim, setResim] = useState(true);
  const [bekle, setBekle] = useState(false);
  const [metin, setMetin] = useState("");
  const [kullanilanTema, setKullanilanTema] = useState("");

  const yaz2 = async (devam = false) => {
    setBekle(true);
    try {
      if (devam) {
        const r = await sohbetTamamla([{ role: "assistant", content: metin }, { role: "user", content: "Bu hikâyenin yeni bir bölümünü yaz ('## Bölüm 2' gibi ara başlıkla), aynı dil, üslup ve karakterlerle." }],
          { sistem: "Aynı çocuk kitabı yazarısın; güvenli, yaşa uygun devam et.", sicaklik: 0.9, maks: 3000, tercih: tercihDil(dil) });
        if (r.metin) setMetin(metin + "\n\n" + r.metin);
        return;
      }
      const t = tema.startsWith("🎲") ? TEMALAR[Math.floor(Math.random() * TEMALAR.length)] : tema;
      setKullanilanTema(t);
      const [sistem, govde] = hikayeIstemi({ yas, dil, tur, tema: t, deger: deger === "—" ? "" : deger, ton, uzunluk, kahraman: ad, yer, ek, ceviriDili: ceviri, sorular: true });
      const r = await sohbetTamamla([{ role: "user", content: govde }], { sistem, sicaklik: 0.9, maks: 3000, tercih: tercihDil(dil) });
      setMetin(r.metin || "⚠️ Şu an hikâye yazılamadı, biraz sonra tekrar dene.");
    } finally { setBekle(false); }
  };

  const [fazla, setFazla] = useState(false);
  return (
    <View>
      <Kart>
        <Secici etiket="Ne dinlemek istersin?" deger={tur} onChange={setTur} secenekler={Object.entries(TURLER).map(([k, v]) => ({ k, ad: v[0] }))} />
        <Secici etiket="Konusu ne olsun?" deger={tema} onChange={setTema} secenekler={["🎲 Sürpriz", ...TEMALAR].map((k) => ({ k, ad: k }))} />
        <Dugme yazi={tur === "siir" ? "✨ Şiiri yaz" : "✨ Masalı yaz"} onPress={() => yaz2()} yukleniyor={bekle} />
        <Pressable onPress={() => setFazla(!fazla)} style={{ alignSelf: "center", marginTop: 10 }}>
          <Text style={{ color: R.acc2, fontWeight: "700" }}>{fazla ? "▾ Daha az seçenek" : "⚙️ Daha fazla seçenek"}</Text>
        </Pressable>
        {fazla ? (
          <View style={{ marginTop: 10 }}>
            <Secici etiket="Değer" deger={deger} onChange={setDeger} secenekler={["—", ...DEGERLER].map((k) => ({ k, ad: k }))} />
            <Secici etiket="Ton" deger={ton} onChange={setTon} secenekler={TONLAR.map((k) => ({ k, ad: k }))} />
            <Secici etiket="Uzunluk" deger={uzunluk} onChange={setUzunluk} secenekler={["Kısa", "Orta", "Uzun"].map((k) => ({ k, ad: k }))} />
            {tur === "ikidilli" && <Secici etiket="Çeviri dili" deger={ceviri} onChange={setCeviri} secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />}
            <Girdi etiket="Nerede geçsin?" value={yer} onChangeText={setYer} placeholder="ör. Kapadokya, Ay'da bir köy…" />
            <Girdi etiket="Özel istek" value={ek} onChangeText={setEk} placeholder="ör. içinde kedimiz Pamuk olsun" />
            <Secici etiket="Resim" deger={resim ? "e" : "h"} onChange={(v) => setResim(v === "e")} secenekler={[{ k: "e", ad: "🎨 Resimli" }, { k: "h", ad: "Resimsiz" }]} />
          </View>
        ) : null}
      </Kart>
      {metin ? (
        <Kart>
          {resim && !metin.startsWith("⚠️") ? <Image source={{ uri: resimAdresi(baslikBul(metin), kullanilanTema) }} style={{ width: "100%", aspectRatio: 1.5, borderRadius: 16, marginBottom: 10, backgroundColor: R.kart }} /> : null}
          <MdMetin rtl={RTL_DILLER.has(dil)}>{metin}</MdMetin>
          <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10 }}>
            <Dugme kucuk ikincil yazi={konusuyor ? "⏹ Durdur" : "🔊 Sesli anlat"} onPress={() => sesli(metin, USLUP_TUR[tur] || "masal")} />
            <Dugme kucuk ikincil yazi="➡️ Devamı" onPress={() => yaz2(true)} yukleniyor={bekle} />
            <Dugme kucuk ikincil yazi="💾 Kaydet" onPress={() => kitapligaEkle({ baslik: baslikBul(metin), metin, yas, dil, tur })} />
          </View>
        </Kart>
      ) : null}
    </View>
  );
}

function Macera({ yas, dil, ad, sesli, konusuyor }: Ortak) {
  const [tema, setTema] = useState(TEMALAR[1]);
  const [gecmis, setGecmis] = useState<Rol[]>([]);
  const [bekle, setBekle] = useState(false);
  const sistem = maceraSistemi(yas, dil, tema, ad);
  const ilerle = async (secim: string) => {
    setBekle(true);
    const yeni: Rol[] = [...gecmis, { role: "user", content: secim }];
    const r = await sohbetTamamla(yeni.slice(-14), { sistem, sicaklik: 0.9, maks: 1200, tercih: tercihDil(dil) });
    setBekle(false);
    if (r.metin) setGecmis([...yeni, { role: "assistant", content: r.metin }]);
  };
  const son = gecmis[gecmis.length - 1]?.content || "";
  const secenekler = son ? secenekleriAyikla(son) : [];
  return (
    <View>
      {!gecmis.length ? (
        <Kart>
          <Secici etiket="Macera teması" deger={tema} onChange={setTema} secenekler={TEMALAR.map((k) => ({ k, ad: k }))} />
          <Dugme yazi="🚀 Macerayı başlat" onPress={() => ilerle("Macerayı başlat: 1. bölüm.")} yukleniyor={bekle} />
        </Kart>
      ) : null}
      {gecmis.map((m, i) => m.role === "assistant" ? (
        <Kart key={i}><MdMetin rtl={RTL_DILLER.has(dil)}>{m.content}</MdMetin></Kart>
      ) : i > 0 ? <Text key={i} style={{ color: R.acc2, marginBottom: 8, fontWeight: "700" }}>👉 {m.content}</Text> : null)}
      {bekle ? <ActivityIndicator color={R.acc2} style={{ marginVertical: 12 }} /> : null}
      {son && !bekle ? (
        <View style={{ gap: 8 }}>
          <Dugme kucuk ikincil yazi={konusuyor ? "⏹ Durdur" : "🔊 Bu bölümü anlat"} onPress={() => sesli(son, "macera")} />
          {secenekler.map((s, i) => <Dugme key={i} yazi={`${i + 1}. ${s}`} onPress={() => ilerle(s)} />)}
          <View style={{ flexDirection: "row", gap: 8 }}>
            <Dugme kucuk ikincil yazi="💾 Kaydet" onPress={() => kitapligaEkle({ baslik: "🎭 " + baslikBul(gecmis[1]?.content || "Macera"), metin: gecmis.slice(1).map((m) => (m.role === "user" ? "👉 " : "") + m.content).join("\n\n"), yas, dil, tur: "macera" })} />
            <Dugme kucuk ikincil yazi="🔄 Yeni macera" onPress={() => setGecmis([])} />
          </View>
        </View>
      ) : null}
    </View>
  );
}

function Arkadas({ yas, dil, ad, sesli }: Ortak) {
  const [karakter, setKarakter] = useState("baykus");
  const [mesajlar, setMesajlar] = useState<Rol[]>([]);
  const [girdi, setGirdi] = useState("");
  const [bekle, setBekle] = useState(false);
  useEffect(() => setMesajlar([]), [karakter]);
  const gonder = async (metin: string) => {
    if (!metin.trim() || bekle) return;
    setGirdi("");
    const yeni: Rol[] = [...mesajlar, { role: "user", content: metin }];
    setMesajlar(yeni); setBekle(true);
    const r = await sohbetTamamla(yeni.slice(-16), { sistem: sohbetSistemi(yas, dil, karakter, ad), sicaklik: 0.85, maks: 700, tercih: tercihDil(dil) });
    setBekle(false);
    setMesajlar([...yeni, { role: "assistant", content: r.metin || "Hımm, biraz uykum geldi 😴 Tekrar dener misin?" }]);
  };
  const avatar = KARAKTERLER[karakter][0].split(" ")[0];
  return (
    <View>
      <Secici etiket="Arkadaşını seç" deger={karakter} onChange={setKarakter} secenekler={Object.entries(KARAKTERLER).map(([k, v]) => ({ k, ad: v[0] }))} />
      <Secici etiket="Oyunlar" deger={""} onChange={(k) => gonder(OYUNLAR[k])} secenekler={Object.keys(OYUNLAR).map((k) => ({ k, ad: k }))} />
      <Kart style={{ minHeight: 220 }}>
        {!mesajlar.length ? <Text style={us.alt}>{avatar} Merhaba{ad ? " " + ad : ""}! Ben {KARAKTERLER[karakter][0].slice(2)}. Benimle konuş ya da bir oyun seç! 🌟</Text> : null}
        {mesajlar.map((m, i) => (
          <View key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "88%", marginBottom: 8, backgroundColor: m.role === "user" ? "rgba(124,92,255,0.4)" : "rgba(255,255,255,0.05)", borderRadius: 16, padding: 10 }}>
            {m.role === "assistant" ? <MdMetin rtl={RTL_DILLER.has(dil)}>{`${avatar} ${m.content}`}</MdMetin> : <Text style={{ color: "#fff", fontSize: 16 }}>🧒 {m.content}</Text>}
            {m.role === "assistant" ? <Pressable onPress={() => sesli(m.content, "sohbet")}><Text style={{ fontSize: 16, marginTop: 4 }}>🔊</Text></Pressable> : null}
          </View>
        ))}
        {bekle ? <ActivityIndicator color={R.acc2} /> : null}
      </Kart>
      <View style={{ flexDirection: "row", gap: 8 }}>
        <TextInput value={girdi} onChangeText={setGirdi} placeholder="Arkadaşına yaz…" placeholderTextColor={R.soluk} style={[us.girdi, { flex: 1 }]} onSubmitEditing={() => gonder(girdi)} />
        <Dugme yazi="➤" onPress={() => gonder(girdi)} />
      </View>
    </View>
  );
}

function Kitaplik({ sesli }: { sesli: (m: string, u: string) => void }) {
  const [liste, setListe] = useState<KitapKaydi[]>([]);
  const [acik, setAcik] = useState<string | null>(null);
  const yenile = () => kitaplikOku().then(setListe);
  useEffect(() => { yenile(); }, []);
  if (!liste.length) return <Kart><Text style={us.alt}>Kitaplığın boş. Beğendiğin hikâyeleri 💾 ile kaydet.</Text></Kart>;
  return (
    <View>
      {liste.map((k) => (
        <Kart key={k.id}>
          <Pressable onPress={() => setAcik(acik === k.id ? null : k.id)}>
            <Text style={{ color: "#fff", fontWeight: "700", fontSize: 16 }}>{k.baslik}</Text>
            <Text style={us.alt}>{YAS[k.yas]?.ad} • {DILLER[k.dil]?.bayrak} {DILLER[k.dil]?.ad} • {k.tarih}</Text>
          </Pressable>
          {acik === k.id ? (
            <View style={{ marginTop: 8 }}>
              <MdMetin rtl={RTL_DILLER.has(k.dil)}>{k.metin}</MdMetin>
              <View style={{ flexDirection: "row", gap: 8, marginTop: 8 }}>
                <Dugme kucuk ikincil yazi="🔊 Anlat" onPress={() => sesli(k.metin, USLUP_TUR[k.tur] || "masal")} />
                <Dugme kucuk ikincil yazi="🗑️ Sil" onPress={async () => { await kitapliktanSil(k.id); yenile(); }} />
              </View>
            </View>
          ) : null}
        </Kart>
      ))}
    </View>
  );
}
