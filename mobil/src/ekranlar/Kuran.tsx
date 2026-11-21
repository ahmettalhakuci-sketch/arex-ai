// AREX — 🕌 Kur'an & Hafızlık: günün ayeti/hadisi/esması, oku & dinle (Diyanet meali + Alafasy), hafızlık takibi, pomodoro, teknikler
import { createAudioPlayer, setAudioModeAsync, type AudioPlayer } from "expo-audio";
import * as Haptics from "expo-haptics";
import { LinearGradient } from "expo-linear-gradient";
import * as Speech from "expo-speech";
import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, Platform, Pressable, ScrollView, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { oku, yaz } from "../depo";
import { ayetler, MEALLER, bugun, bugunkuSayfa, esma, gununAyeti, gununHadisi, hafizlikOku, hafizlikYaz, seri, SURELER, sureBul, tekrarOnerisi, type Ayet, type Hadis, type Hafizlik } from "../kuran";
import { GRADYAN, R } from "../tema";
import { Baslik, Dugme, Girdi, Hap, Kart, MdMetin, s as us, Secici } from "../ui";

type Sekme = "bugun" | "oku" | "hafizlik" | "pomodoro" | "teknik";

// ---------- Tilavet çalar (ayet ayet sıralı) ----------
let calar: AudioPlayer | null = null;
let kuyruk: string[] = [];
let degisti: ((i: number) => void) | null = null;
function tilavetDurdur() { try { calar?.pause(); calar?.remove(); } catch {} calar = null; kuyruk = []; degisti?.(-1); }
async function tilavetCal(sesler: string[], bas = 0, cb?: (i: number) => void) {
  tilavetDurdur(); kuyruk = sesler; degisti = cb || null;
  try { await setAudioModeAsync({ playsInSilentMode: true }); } catch {}
  const oynat = (i: number) => {
    if (i >= kuyruk.length) { tilavetDurdur(); return; }
    degisti?.(i);
    try { calar?.remove(); } catch {}
    calar = createAudioPlayer({ uri: kuyruk[i] });
    (calar as any).addListener("playbackStatusUpdate", (d: { didJustFinish?: boolean }) => { if (d.didJustFinish) oynat(i + 1); });
    calar.play();
  };
  oynat(bas);
}

const ARAPCA = { fontSize: 26, lineHeight: 50, color: "#fff", textAlign: "right" as const, writingDirection: "rtl" as const, fontFamily: Platform.OS === "ios" ? "Geeza Pro" : undefined };

export default function KuranEkrani() {
  const ic = useSafeAreaInsets();
  const [sekme, setSekme] = useState<Sekme>("bugun");
  useEffect(() => () => tilavetDurdur(), []);
  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 40 }} keyboardShouldPersistTaps="handled">
      <LinearGradient colors={[R.acc + "55", R.acc2 + "22"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 24, padding: 18, marginBottom: 12, borderWidth: 1, borderColor: R.cizgi }}>
        <Text style={{ color: "#fff", fontSize: 24, fontWeight: "800" }}>🕌 Kur'an & Hafızlık</Text>
        <Text style={[us.alt, { color: "#e6e9ff" }]}>Günün ayeti, hadis, tilavet, hafızlık takibi ve odak sayacı — açık kaynaklarla.</Text>
      </LinearGradient>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, marginBottom: 12 }}>
        {([["bugun", "🌅 Bugün"], ["oku", "📖 Oku & Dinle"], ["hafizlik", "🧠 Hafızlık"], ["pomodoro", "🍅 Pomodoro"], ["teknik", "💡 Teknikler"]] as [Sekme, string][]).map(([k, a]) => (
          <Hap key={k} yazi={a} secili={sekme === k} onPress={() => setSekme(k)} />
        ))}
      </ScrollView>
      {sekme === "bugun" && <Bugun git={setSekme} />}
      {sekme === "oku" && <OkuDinle />}
      {sekme === "hafizlik" && <HafizlikEkrani />}
      {sekme === "pomodoro" && <Pomodoro />}
      {sekme === "teknik" && <Teknikler />}
    </ScrollView>
  );
}

function AyetKart({ a, calan, onCal }: { a: Ayet; calan?: boolean; onCal?: () => void }) {
  return (
    <Kart style={calan ? { borderColor: R.acc2, backgroundColor: R.hap } : undefined}>
      <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 6 }}>
        <View style={{ backgroundColor: R.hap, borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4 }}><Text style={{ color: "#fff", fontWeight: "800", fontSize: 12 }}>{a.sureAd} {a.no}</Text></View>
        <View style={{ flex: 1 }} />
        {onCal ? <Pressable onPress={onCal} hitSlop={10}><Text style={{ fontSize: 20 }}>{calan ? "⏸" : "▶️"}</Text></Pressable> : null}
      </View>
      <Text style={ARAPCA}>{a.arapca}</Text>
      <Text style={{ color: R.yazi, fontSize: 15.5 * (R.olcek || 1), lineHeight: 24 * (R.olcek || 1), marginTop: 8 }}>{a.meal}</Text>
    </Kart>
  );
}

function Bugun({ git }: { git: (s: Sekme) => void }) {
  const [ayet, setAyet] = useState<Ayet | null>(null);
  const [hadis, setHadis] = useState<Hadis | null>(null);
  const [es, setEs] = useState<any>(null);
  const [h, setH] = useState<Hafizlik | null>(null);
  const [calan, setCalan] = useState(false);
  const [hata, setHata] = useState("");
  useEffect(() => {
    gununAyeti().then(setAyet).catch(() => setHata("Ayet yüklenemedi (internet)."));
    gununHadisi().then(setHadis).catch(() => {});
    esma().then(setEs).catch(() => {});
    hafizlikOku().then(setH);
  }, []);
  const yapilan = h ? bugunkuSayfa(h) : 0;
  const oran = h ? Math.min(1, yapilan / Math.max(1, h.hedefSayfa)) : 0;
  return (
    <View>
      {h ? (
        <Kart>
          <View style={{ flexDirection: "row", gap: 10 }}>
            {[["🔥", `${seri(h)} gün`, "seri"], ["📄", `${yapilan}/${h.hedefSayfa}`, "bugün sayfa"], ["🔁", `${tekrarOnerisi(h).join(" & ")}. cüz`, "tekrar önerisi"]].map(([i, d, a]) => (
              <View key={a} style={{ flex: 1, backgroundColor: "rgba(255,255,255,0.05)", borderRadius: 16, padding: 10, alignItems: "center" }}>
                <Text style={{ fontSize: 20 }}>{i}</Text><Text style={{ color: "#fff", fontWeight: "800", fontSize: 15 }}>{d}</Text><Text style={{ color: R.soluk, fontSize: 11 }}>{a}</Text>
              </View>
            ))}
          </View>
          <View style={{ height: 8, borderRadius: 4, backgroundColor: "rgba(255,255,255,0.08)", marginTop: 12, overflow: "hidden" }}>
            <LinearGradient colors={GRADYAN} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={{ width: `${oran * 100}%`, height: "100%" }} />
          </View>
          <Dugme kucuk ikincil yazi="🧠 Hafızlık kaydı ekle" onPress={() => git("hafizlik")} style={{ marginTop: 10 }} />
        </Kart>
      ) : null}
      <Text style={[us.etiket, { marginTop: 4 }]}>📖 GÜNÜN AYETİ</Text>
      {ayet ? <AyetKart a={ayet} calan={calan} onCal={() => { if (calan) { tilavetDurdur(); setCalan(false); } else { tilavetCal([ayet.ses], 0, (i) => setCalan(i >= 0)); } }} /> : <Kart>{hata ? <Text style={us.alt}>{hata}</Text> : <ActivityIndicator color={R.acc2} />}</Kart>}
      <Text style={us.etiket}>🌙 GÜNÜN HADİSİ</Text>
      <Kart>
        {hadis ? (
          <>
            <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16, marginBottom: 6 }}>{hadis.baslik}</Text>
            <Text style={{ color: R.yazi, fontSize: 15, lineHeight: 23 }}>{hadis.metin}</Text>
            <Text style={{ color: R.acc2, fontSize: 12, marginTop: 8 }}>{hadis.kaynak} • {hadis.derece} • HadeethEnc</Text>
          </>
        ) : <ActivityIndicator color={R.acc2} />}
      </Kart>
      {es ? (
        <Kart>
          <Text style={us.etiket}>✨ GÜNÜN ESMÂSI — {es.no}.</Text>
          <Text style={[ARAPCA, { textAlign: "center", fontSize: 34 }]}>{es.isim}</Text>
          <Text style={{ color: "#fff", textAlign: "center", fontWeight: "700" }}>{es.okunus}</Text>
          <Text style={[us.alt, { textAlign: "center" }]}>{es.anlam}</Text>
        </Kart>
      ) : null}
    </View>
  );
}

function OkuDinle() {
  const [sureAra, setSureAra] = useState("Yâsîn");
  const [meal, setMeal] = useState("tr.vakfi");
  const [bas, setBas] = useState("1");
  const [son, setSon] = useState("7");
  const [liste, setListe] = useState<Ayet[]>([]);
  const [calan, setCalan] = useState(-1);
  const [bekle, setBekle] = useState(false);
  const [hata, setHata] = useState("");
  const getir = async () => {
    const s = sureBul(sureAra);
    if (!s) { setHata("Sure bulunamadı. Adını ya da numarasını yaz (ör. Mülk, 67)."); return; }
    setHata(""); setBekle(true); tilavetDurdur();
    try { setListe(await ayetler(s, Math.max(1, Number(bas) || 1), Math.max(Number(bas) || 1, Number(son) || 1), meal)); }
    catch { setHata("Kaynağa ulaşılamadı (internet)."); }
    setBekle(false);
  };
  useEffect(() => { getir(); }, []);
  return (
    <View>
      <Kart>
        <Girdi etiket="Sure (ad veya numara)" value={sureAra} onChangeText={setSureAra} placeholder="ör. Mülk" />
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 6, marginBottom: 10 }}>
          {["Fâtiha", "Yâsîn", "Mülk", "Rahmân", "Vâkıa", "Kehf", "Nebe'", "İhlâs"].map((x) => <Hap key={x} yazi={x} secili={sureAra === x} onPress={() => setSureAra(x)} />)}
        </ScrollView>
        <Secici etiket="Meal" deger={meal} onChange={setMeal} secenekler={Object.entries(MEALLER).map(([k, v]) => ({ k, ad: v }))} />
        <View style={{ flexDirection: "row", gap: 10 }}>
          <View style={{ flex: 1 }}><Girdi etiket="Başlangıç ayeti" value={bas} onChangeText={setBas} keyboardType="number-pad" /></View>
          <View style={{ flex: 1 }}><Girdi etiket="Bitiş ayeti" value={son} onChangeText={setSon} keyboardType="number-pad" /></View>
        </View>
        <View style={{ flexDirection: "row", gap: 8 }}>
          <Dugme yazi="📖 Getir" onPress={getir} yukleniyor={bekle} style={{ flex: 1 }} />
          {liste.length ? <Dugme ikincil yazi={calan >= 0 ? "⏹ Durdur" : "🎧 Tümünü dinle"} onPress={() => (calan >= 0 ? tilavetDurdur() : tilavetCal(liste.map((a) => a.ses), 0, setCalan))} style={{ flex: 1 }} /> : null}
        </View>
        {hata ? <Text style={{ color: R.kirmizi, marginTop: 8 }}>{hata}</Text> : null}
        <Text style={{ color: R.soluk, fontSize: 11, marginTop: 8 }}>Kaynak: alquran.cloud — {MEALLER[meal]} meali • Tilavet: Mişari Raşid el-Afasi • En fazla 30 ayet</Text>
      </Kart>
      {liste.map((a, i) => <AyetKart key={a.no} a={a} calan={calan === i} onCal={() => (calan === i ? tilavetDurdur() : tilavetCal(liste.map((x) => x.ses), i, setCalan))} />)}
    </View>
  );
}

function HafizlikEkrani() {
  const [h, setH] = useState<Hafizlik | null>(null);
  const [tur, setTur] = useState<"ezber" | "tekrar">("tekrar");
  const [cuz, setCuz] = useState("1");
  const [sayfa, setSayfa] = useState("20");
  const [not, setNot] = useState("");
  useEffect(() => { hafizlikOku().then(setH); }, []);
  if (!h) return <ActivityIndicator color={R.acc2} />;
  const kaydet = async () => {
    const c = Math.min(30, Math.max(1, Number(cuz) || 1));
    const y: Hafizlik = { ...h, kayitlar: [...h.kayitlar, { tarih: bugun(), tur, cuz: c, sayfa: Math.max(0, Number(sayfa) || 0), not }].slice(-1000),
      cuzTekrar: tur === "tekrar" ? { ...h.cuzTekrar, [c]: bugun() } : h.cuzTekrar };
    await hafizlikYaz(y); setH(y); setNot("");
    if (Platform.OS !== "web") Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success).catch(() => {});
  };
  const oneri = tekrarOnerisi(h);
  return (
    <View>
      <Kart>
        <Text style={{ color: "#fff", fontSize: 16, fontWeight: "800", marginBottom: 8 }}>🔁 Bugün tekrar önerisi: {oneri.join(" ve ")}. cüz</Text>
        <Text style={us.alt}>En uzun süredir tekrar edilmeyen cüzler önce gelir; her tekrar kaydı haritayı günceller.</Text>
      </Kart>
      <Kart>
        <Secici etiket="Kayıt türü" deger={tur} onChange={setTur} secenekler={[{ k: "tekrar", ad: "🔁 Tekrar" }, { k: "ezber", ad: "🆕 Yeni ezber" }]} />
        <View style={{ flexDirection: "row", gap: 10 }}>
          <View style={{ flex: 1 }}><Girdi etiket="Cüz" value={cuz} onChangeText={setCuz} keyboardType="number-pad" /></View>
          <View style={{ flex: 1 }}><Girdi etiket="Sayfa" value={sayfa} onChangeText={setSayfa} keyboardType="number-pad" /></View>
        </View>
        <Girdi etiket="Not (isteğe bağlı)" value={not} onChangeText={setNot} placeholder="ör. 3. sayfada takıldım, müteşabih ayet" />
        <Dugme yazi="💾 Kaydet" onPress={kaydet} />
        <Secici etiket="Günlük hedef (sayfa)" deger={String(h.hedefSayfa)} onChange={async (v) => { const y = { ...h, hedefSayfa: Number(v) }; await hafizlikYaz(y); setH(y); }}
          secenekler={["5", "10", "20", "30", "40"].map((k) => ({ k, ad: k + " sayfa" }))} />
      </Kart>
      <Kart>
        <Text style={us.etiket}>🗺️ 30 cüz tekrar haritası (yeşil: son 7 gün, sarı: 8-20 gün, kırmızı: daha eski/hiç)</Text>
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 6 }}>
          {Array.from({ length: 30 }, (_, i) => i + 1).map((c) => {
            const t = h.cuzTekrar[c];
            const gun = t ? (Date.now() - new Date(t).getTime()) / 86400000 : 999;
            const renk = gun <= 7 ? "#2ee59d" : gun <= 20 ? "#ffc145" : "#ff4d6d";
            return (
              <Pressable key={c} onPress={() => { setCuz(String(c)); setTur("tekrar"); }} style={{ width: "15%", aspectRatio: 1, borderRadius: 12, backgroundColor: renk + "33", borderWidth: 1, borderColor: renk, alignItems: "center", justifyContent: "center" }}>
                <Text style={{ color: "#fff", fontWeight: "800" }}>{c}</Text>
              </Pressable>
            );
          })}
        </View>
      </Kart>
      <Text style={us.etiket}>📅 Son kayıtlar</Text>
      {[...h.kayitlar].reverse().slice(0, 15).map((k, i) => (
        <Kart key={i} style={{ paddingVertical: 10 }}>
          <Text style={{ color: "#fff" }}>{k.tur === "tekrar" ? "🔁 Tekrar" : "🆕 Ezber"} • {k.cuz}. cüz • {k.sayfa} sayfa</Text>
          <Text style={{ color: R.soluk, fontSize: 12 }}>{k.tarih}{k.not ? " • " + k.not : ""}</Text>
        </Kart>
      ))}
    </View>
  );
}

const POMO_AYAR: Record<string, { ad: string; calis: number; mola: number }> = {
  ezber: { ad: "🆕 Ezber 25/5", calis: 25, mola: 5 },
  tekrar: { ad: "🔁 Tekrar 40/10", calis: 40, mola: 10 },
  ders: { ad: "📚 Ders 50/10", calis: 50, mola: 10 },
  kisa: { ad: "⚡ Kısa 15/3", calis: 15, mola: 3 },
};
function Pomodoro() {
  const [tip, setTip] = useState("ezber");
  const [faz, setFaz] = useState<"calis" | "mola">("calis");
  const [kalan, setKalan] = useState(POMO_AYAR.ezber.calis * 60);
  const [calisiyor, setCalisiyor] = useState(false);
  const [bugunSayi, setBugunSayi] = useState(0);
  const zaman = useRef<any>(null);
  useEffect(() => { oku<{ tarih: string; sayi: number }>("arex_pomodoro", { tarih: "", sayi: 0 }).then((p) => setBugunSayi(p.tarih === bugun() ? p.sayi : 0)); }, []);
  useEffect(() => { if (!calisiyor) setKalan((faz === "calis" ? POMO_AYAR[tip].calis : POMO_AYAR[tip].mola) * 60); }, [tip, faz]);
  useEffect(() => {
    if (!calisiyor) { clearInterval(zaman.current); return; }
    zaman.current = setInterval(() => setKalan((k) => {
      if (k > 1) return k - 1;
      const yeniFaz = faz === "calis" ? "mola" : "calis";
      if (faz === "calis") { const s = bugunSayi + 1; setBugunSayi(s); yaz("arex_pomodoro", { tarih: bugun(), sayi: s }); }
      if (Platform.OS !== "web") Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success).catch(() => {});
      Speech.speak(faz === "calis" ? "Tebrikler, mola zamanı. Biraz dinlen." : "Mola bitti, haydi devam.", { language: "tr-TR" });
      setFaz(yeniFaz);
      return (yeniFaz === "calis" ? POMO_AYAR[tip].calis : POMO_AYAR[tip].mola) * 60;
    }), 1000);
    return () => clearInterval(zaman.current);
  }, [calisiyor, faz, tip, bugunSayi]);
  const toplam = (faz === "calis" ? POMO_AYAR[tip].calis : POMO_AYAR[tip].mola) * 60;
  const oran = 1 - kalan / toplam;
  return (
    <View>
      <Secici deger={tip} onChange={(v) => { setCalisiyor(false); setFaz("calis"); setTip(v); }} secenekler={Object.entries(POMO_AYAR).map(([k, v]) => ({ k, ad: v.ad }))} />
      <LinearGradient colors={faz === "calis" ? [R.acc + "66", R.acc2 + "33"] : ["#2ee59d55", "#22d3ee33"]} style={{ borderRadius: 28, padding: 24, alignItems: "center", borderWidth: 1, borderColor: R.cizgi, marginBottom: 12 }}>
        <Text style={{ color: "#fff", fontSize: 15, fontWeight: "700", letterSpacing: 1 }}>{faz === "calis" ? "🎯 ODAK ZAMANI" : "☕ MOLA"}</Text>
        <Text style={{ color: "#fff", fontSize: 72, fontWeight: "800", fontVariant: ["tabular-nums"], marginVertical: 6 }}>{String(Math.floor(kalan / 60)).padStart(2, "0")}:{String(kalan % 60).padStart(2, "0")}</Text>
        <View style={{ width: "100%", height: 10, borderRadius: 5, backgroundColor: "rgba(255,255,255,0.12)", overflow: "hidden" }}>
          <View style={{ width: `${oran * 100}%`, height: "100%", backgroundColor: "#fff", opacity: 0.85 }} />
        </View>
        <Text style={{ color: "#e6e9ff", marginTop: 10 }}>🍅 Bugün tamamlanan: {bugunSayi} pomodoro</Text>
      </LinearGradient>
      <View style={{ flexDirection: "row", gap: 8 }}>
        <Dugme yazi={calisiyor ? "⏸ Duraklat" : "▶️ Başlat"} onPress={() => setCalisiyor(!calisiyor)} style={{ flex: 2 }} />
        <Dugme ikincil yazi="↺ Sıfırla" onPress={() => { setCalisiyor(false); setFaz("calis"); setKalan(POMO_AYAR[tip].calis * 60); }} style={{ flex: 1 }} />
      </View>
      <Text style={[us.alt, { marginTop: 10, fontSize: 12 }]}>Süre bitince titreşim ve sesli uyarı verir. Uygulama açık kalmalıdır.</Text>
    </View>
  );
}

const TEKNIKLER: [string, string][] = [
  ["🌅 Sabah ezberi", "Zihnin en dinç olduğu sabah namazı sonrası yeni ezber için en verimli zamandır; akşamı tekrara ayır."],
  ["🔁 3 okuma + 5 ezberden", "Yeni sayfayı önce yüzünden 3 kez dikkatle oku, sonra ezberden 5 kez tekrar et; takıldığın yeri işaretle."],
  ["🧩 Parça parça", "Sayfayı 3-5 ayetlik parçalara böl; her parçayı ezberledikten sonra öncekilerle birleştirerek oku (zincir yöntemi)."],
  ["🎧 Dinleyerek pekiştir", "Ezberlediğin sayfayı bir hafızdan (ör. Afasi) dinle; telaffuz ve tecvid hatalarını fark etmeni kolaylaştırır."],
  ["📌 Müteşabih defteri", "Birbirine benzeyen ayetleri (müteşabihleri) not al, farklarını renkli kalemle işaretle; karıştırmayı önler."],
  ["📆 Halka tekrar", "Her gün yeni sayfa + son 5 sayfa + 1 eski cüz tekrar et. Haritadaki kırmızı cüzler önceliklidir."],
  ["🧑‍🏫 Hocaya dinletme", "Ezberi bir başkasına (hoca, arkadaş) dinletmek hatayı yakalamanın en güvenilir yoludur."],
  ["🕌 Namazda okuma", "Ezberlediğin sureleri namazlarda okumak tekrarı doğal ve kalıcı yapar."],
  ["😴 Uyku ve su", "Düzenli uyku ezberin kalıcılaşmasında çok etkilidir; çalışırken su içmeyi ve kısa molaları ihmal etme."],
];
function Teknikler() {
  return (
    <View>
      {TEKNIKLER.map(([b, a]) => (
        <Kart key={b}>
          <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16, marginBottom: 4 }}>{b}</Text>
          <Text style={{ color: R.yazi, fontSize: 15, lineHeight: 22 }}>{a}</Text>
        </Kart>
      ))}
      <Text style={[us.alt, { fontSize: 12 }]}>Bu öneriler genel çalışma teknikleridir; kendi hocanın yöntemini esas al.</Text>
    </View>
  );
}
