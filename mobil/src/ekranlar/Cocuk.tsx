// AREX — 🧸 Çocuk Dünyası: 3 yaş grubu, 18 dil, hikâye atölyesi, sen-seç macerası, sohbet arkadaşları, kitaplık
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Image, Pressable, ScrollView, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ANLATICILAR, sohbetTamamla, type Rol } from "../ai";
import { useAyar } from "../ayar";
import { baslikBul, DEGERLER, hikayeIstemi, KARAKTERLER, maceraSistemi, OYUNLAR, resimAdresi, secenekleriAyikla, sohbetSistemi, TEMALAR, tercihDil, TONLAR, TURLER, YAS } from "../cocuk";
import { kitapligaEkle, kitaplikOku, kitapliktanSil, type KitapKaydi } from "../depo";
import { anlat, sesiDurdur } from "../ses";
import { DILLER, R, RTL_DILLER } from "../tema";
import { Baslik, Dugme, Girdi, Hap, Kart, MdMetin, s as us, Secici } from "../ui";

type Sekme = "atolye" | "macera" | "arkadas" | "kitaplik";
const USLUP_TUR: Record<string, string> = { uyku: "uyku", komik: "komik", macera: "macera", bilim: "bilgi" };

export default function CocukEkrani() {
  const ic = useSafeAreaInsets();
  const { ayar, guncelle } = useAyar();
  const [sekme, setSekme] = useState<Sekme>("atolye");
  const [yas, setYas] = useState(ayar.yas || "7-9");
  const [dil, setDil] = useState("tr");
  const [ad, setAd] = useState("");
  const [konusuyor, setKonusuyor] = useState(false);
  const sesli = async (metin: string, uslup: string) => {
    if (konusuyor) { await sesiDurdur(); setKonusuyor(false); return; }
    setKonusuyor(true);
    await anlat(metin, dil, uslup, ayar.anlatici, ayar.dogalSes);
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 40 }} keyboardShouldPersistTaps="handled">
      <Baslik alt="Masallar, maceralar, sohbet arkadaşları ve oyunlar — yaşa göre, 18 dilde, doğal sesle.">🧸 Çocuk Dünyası</Baslik>
      <Secici etiket="Yaş grubu" deger={yas} onChange={(v) => { setYas(v); guncelle({ yas: v }); }}
        secenekler={Object.entries(YAS).map(([k, v]) => ({ k, ad: `${v.ad} (${k})` }))} />
      <Secici etiket="Dil" deger={dil} onChange={setDil} secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />
      <Secici etiket="🎙️ Anlatıcı" deger={ayar.anlatici} onChange={(v) => guncelle({ anlatici: v })}
        secenekler={Object.entries(ANLATICILAR).map(([k, v]) => ({ k, ad: v.ad }))} />
      <Girdi etiket="Çocuğun adı (isteğe bağlı)" value={ad} onChangeText={setAd} placeholder="ör. Elif" />
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
        {([["atolye", "📖 Hikâye Atölyesi"], ["macera", "🎭 Sen Seç"], ["arkadas", "💬 Arkadaş & Oyun"], ["kitaplik", "🗂️ Kitaplık"]] as [Sekme, string][]).map(([k, a]) => (
          <Hap key={k} yazi={a} secili={sekme === k} onPress={() => setSekme(k)} />
        ))}
      </View>
      {sekme === "atolye" && <Atolye yas={yas} dil={dil} ad={ad} sesli={sesli} konusuyor={konusuyor} />}
      {sekme === "macera" && <Macera yas={yas} dil={dil} ad={ad} sesli={sesli} konusuyor={konusuyor} />}
      {sekme === "arkadas" && <Arkadas yas={yas} dil={dil} ad={ad} sesli={sesli} />}
      {sekme === "kitaplik" && <Kitaplik sesli={sesli} />}
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

  const yaz = async (devam = false) => {
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

  return (
    <View>
      <Kart>
        <Secici etiket="Tür" deger={tur} onChange={setTur} secenekler={Object.entries(TURLER).map(([k, v]) => ({ k, ad: v[0] }))} />
        <Secici etiket="Tema" deger={tema} onChange={setTema} secenekler={["🎲 Sürpriz", ...TEMALAR].map((k) => ({ k, ad: k }))} />
        <Secici etiket="Değer" deger={deger} onChange={setDeger} secenekler={["—", ...DEGERLER].map((k) => ({ k, ad: k }))} />
        <Secici etiket="Ton" deger={ton} onChange={setTon} secenekler={TONLAR.map((k) => ({ k, ad: k }))} />
        <Secici etiket="Uzunluk" deger={uzunluk} onChange={setUzunluk} secenekler={["Kısa", "Orta", "Uzun"].map((k) => ({ k, ad: k }))} />
        {tur === "ikidilli" && <Secici etiket="Çeviri dili" deger={ceviri} onChange={setCeviri} secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />}
        <Girdi etiket="Nerede geçsin?" value={yer} onChangeText={setYer} placeholder="ör. Kapadokya, Ay'da bir köy…" />
        <Girdi etiket="Özel istek" value={ek} onChangeText={setEk} placeholder="ör. içinde kedimiz Pamuk olsun" />
        <Secici etiket="Resim" deger={resim ? "e" : "h"} onChange={(v) => setResim(v === "e")} secenekler={[{ k: "e", ad: "🎨 Resimli" }, { k: "h", ad: "Resimsiz" }]} />
        <Dugme yazi="✨ Hikâyeyi Yaz" onPress={() => yaz()} yukleniyor={bekle} />
      </Kart>
      {metin ? (
        <Kart>
          {resim && !metin.startsWith("⚠️") ? <Image source={{ uri: resimAdresi(baslikBul(metin), kullanilanTema) }} style={{ width: "100%", aspectRatio: 1.5, borderRadius: 16, marginBottom: 10, backgroundColor: R.kart }} /> : null}
          <MdMetin rtl={RTL_DILLER.has(dil)}>{metin}</MdMetin>
          <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10 }}>
            <Dugme kucuk ikincil yazi={konusuyor ? "⏹ Durdur" : "🔊 Sesli anlat"} onPress={() => sesli(metin, USLUP_TUR[tur] || "masal")} />
            <Dugme kucuk ikincil yazi="➡️ Devamı" onPress={() => yaz(true)} yukleniyor={bekle} />
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
