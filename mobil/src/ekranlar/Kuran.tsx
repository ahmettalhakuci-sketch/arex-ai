// AREX — 🕌 Kur'an & Hafızlık: mushaf sayfası (Sure / Cüz / Sayfa), 37 kâri, boşluksuz tilavet + ayet tekrarı + hız,
// ezber modu, günün ayeti/hadisi/esması, hafızlık takibi, pomodoro, teknikler
import { Ionicons } from "@expo/vector-icons";
import { useFonts } from "expo-font";
import * as Haptics from "expo-haptics";
import { LinearGradient } from "expo-linear-gradient";
import * as Speech from "expo-speech";
import React, { useEffect, useMemo, useRef, useState } from "react";
import { ActivityIndicator, Modal, Platform, Pressable, ScrollView, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { oku, yaz } from "../depo";
import {
  ayetler as ayetGetir, AYET_SAYISI, BESMELE, KARILER, MEALLER, SURELER, SURE_SAYFA, bugun, bugunkuSayfa, cuzBaslangic, cuzBitis, esma, gununAyeti, gununHadisi,
  hafizlikOku, hafizlikYaz, kariBul, kariOku, kariYaz, sayfaGetir, sayfaninCuzu, sayfaninSuresi, seri, sureBul, tekrarOnerisi,
  type Ayet, type Hadis, type Hafizlik, type SayfaAyet,
} from "../kuran";
import * as T from "../tilavet";
import { GRADYAN, R } from "../tema";
import { AnahtarSatiri, Dugme, Girdi, Hap, Kart, s as us, Secici, titret } from "../ui";

const ayetDugme = { flexDirection: "row" as const, alignItems: "center" as const, gap: 4, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 999, borderWidth: 1, borderColor: "rgba(232,200,114,0.35)", backgroundColor: "rgba(232,200,114,0.08)" };
const yuvarlak = { width: 38, height: 38, borderRadius: 19, borderWidth: 1, borderColor: "rgba(255,255,255,0.18)", backgroundColor: "rgba(255,255,255,0.06)", alignItems: "center" as const, justifyContent: "center" as const };

type Sekme = "bugun" | "oku" | "nesid" | "hafizlik" | "pomodoro" | "teknik";
type Mod = "sure" | "cuz" | "sayfa" | "ayet";
type OkuAyar = { mod: Mod; sure: number; cuz: number; sayfa: number; meal: string; mealGoster: boolean; ezber: boolean; yazi: number; ayet?: number; ayetDevam?: boolean };
const OKU_VARSAYILAN: OkuAyar = { mod: "sure", sure: 36, cuz: 1, sayfa: 440, meal: "tr.vakfi", mealGoster: true, ezber: false, yazi: 1 };

const ALTIN = "#e8c872";
const AF = "AmiriQuran";
const arapRakam = (n: number) => String(n).replace(/\d/g, (x) => "٠١٢٣٤٥٦٧٨٩"[Number(x)]);
const ARAPCA = { fontSize: 26, lineHeight: 50, color: "#fff", textAlign: "right" as const, writingDirection: "rtl" as const };

/** Tilavet durumunu dinleyen kanca */
function useTilavet() {
  const [d, setD] = useState(T.durum());
  useEffect(() => T.abone(setD), []);
  return d;
}

export default function KuranEkrani() {
  const ic = useSafeAreaInsets();
  const [sekme, setSekme] = useState<Sekme>("bugun");
  const [yaziHazir] = useFonts({ [AF]: require("../../assets/fonts/AmiriQuran.ttf") });
  const t = useTilavet();
  useEffect(() => { kariOku().then((k) => T.ayarla({ kari: k })); }, []);
  return (
    <View style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: t.aktif ? 130 : 40 }} keyboardShouldPersistTaps="handled">
        <LinearGradient colors={["#1d1a3a", "#0d1a2e"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 26, padding: 18, marginBottom: 12, borderWidth: 1, borderColor: ALTIN + "55" }}>
          <View style={{ flexDirection: "row", alignItems: "center", gap: 12 }}>
            <LinearGradient colors={[ALTIN, "#b8862f"]} style={{ width: 46, height: 46, borderRadius: 15, alignItems: "center", justifyContent: "center" }}>
              <Ionicons name="book" size={24} color="#1a1408" />
            </LinearGradient>
            <View style={{ flex: 1 }}>
              <Text style={{ color: "#fff", fontSize: 22, fontWeight: "800" }}>Kur'an-ı Kerim</Text>
              <Text style={{ color: ALTIN, fontSize: 12.5, fontWeight: "600", marginTop: 2 }}>604 sayfa • 30 cüz • {KARILER.length} kâri • Hafızlık</Text>
            </View>
          </View>
        </LinearGradient>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, marginBottom: 12 }}>
          {([["bugun", "🌅 Bugün"], ["oku", "📖 Oku & Dinle"], ["nesid", "🎵 Neşid & İlahi"], ["hafizlik", "🧠 Hafızlık"], ["pomodoro", "🍅 Pomodoro"], ["teknik", "💡 Teknikler"]] as [Sekme, string][]).map(([k, a]) => (
            <Hap key={k} yazi={a} secili={sekme === k} onPress={() => setSekme(k)} />
          ))}
        </ScrollView>
        {sekme === "bugun" && <Bugun git={setSekme} font={yaziHazir ? AF : undefined} />}
        {sekme === "oku" && <OkuDinle font={yaziHazir ? AF : undefined} />}
        {sekme === "hafizlik" && <HafizlikEkrani />}
        {sekme === "pomodoro" && <Pomodoro />}
        {sekme === "teknik" && <Teknikler />}
        {sekme === "nesid" && <Nesidler />}
      </ScrollView>
      <MiniCalar />
    </View>
  );
}

// ---------- Premium mini çalar (ekranın altında yüzer) ----------
function MiniCalar() {
  const t = useTilavet();
  const [kariAcik, setKariAcik] = useState(false);
  if (!t.aktif || !t.parca) return null;
  const kari = kariBul(t.onizleme || t.kari);
  const oran = t.toplam > 0 ? (t.sira + 1) / t.toplam : 0;
  return (
    <View style={{ position: "absolute", left: 10, right: 10, bottom: 10 }}>
      <LinearGradient colors={["#221d45f2", "#0e1830f2"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 24, borderWidth: 1, borderColor: ALTIN + "66", padding: 12, overflow: "hidden" }}>
        <View style={{ position: "absolute", left: 0, top: 0, height: 3, width: `${oran * 100}%`, backgroundColor: ALTIN }} />
        <View style={{ flexDirection: "row", alignItems: "center", gap: 10 }}>
          <Pressable onPress={() => setKariAcik(true)}><KariAvatar ad={kari.ad} boyut={42} /></Pressable>
          <View style={{ flex: 1 }}>
            <Text style={{ color: "#fff", fontWeight: "800", fontSize: 15 }} numberOfLines={1}>
              {t.parca.besmele ? "Besmele" : `${SURELER[t.parca.sure - 1]} • ${t.parca.no}. ayet`}
              {t.tekrar > 1 && !t.parca.besmele ? `  (${t.tekrarSayac}/${t.tekrar})` : ""}
            </Text>
            <Text style={{ color: ALTIN, fontSize: 12 }} numberOfLines={1}>{kari.ad} • {kari.tarz}{t.hiz !== 1 ? ` • ${t.hiz}x` : ""}</Text>
          </View>
          <Pressable hitSlop={8} onPress={() => { titret(); T.onceki(); }}><Ionicons name="play-skip-back" size={22} color="#fff" /></Pressable>
          <Pressable hitSlop={8} onPress={() => { titret(); t.caliyor ? T.duraklat() : T.surdur(); }}
            style={{ width: 46, height: 46, borderRadius: 23, backgroundColor: ALTIN, alignItems: "center", justifyContent: "center" }}>
            {t.yukleniyor ? <ActivityIndicator color="#1a1408" /> : <Ionicons name={t.caliyor ? "pause" : "play"} size={24} color="#1a1408" style={{ marginLeft: t.caliyor ? 0 : 2 }} />}
          </Pressable>
          <Pressable hitSlop={8} onPress={() => { titret(); T.sonraki(); }}><Ionicons name="play-skip-forward" size={22} color="#fff" /></Pressable>
          <Pressable hitSlop={8} onPress={() => T.durdur()}><Ionicons name="close" size={20} color={R.soluk} /></Pressable>
        </View>
      </LinearGradient>
      <KariSecici acik={kariAcik} kapat={() => setKariAcik(false)} />
    </View>
  );
}

function KariAvatar({ ad, boyut = 40, secili }: { ad: string; boyut?: number; secili?: boolean }) {
  const harf = ad.replace(/^(el-|es-|eş-|er-|ed-)/i, "").split(/[\s-]+/).filter((x) => !/^(el|es|eş|er|ed|et)$/i.test(x)).slice(0, 2).map((x) => x[0]).join("").toLocaleUpperCase("tr");
  return (
    <LinearGradient colors={secili ? [ALTIN, "#b8862f"] : [R.acc, R.acc2]} style={{ width: boyut, height: boyut, borderRadius: boyut / 2, alignItems: "center", justifyContent: "center" }}>
      <Text style={{ color: secili ? "#1a1408" : "#fff", fontWeight: "900", fontSize: boyut * 0.36 }}>{harf}</Text>
    </LinearGradient>
  );
}

// ---------- Kâri seçici (alt sayfa) ----------
function KariSecici({ acik, kapat }: { acik: boolean; kapat: () => void }) {
  const t = useTilavet();
  const ic = useSafeAreaInsets();
  const [filtre, setFiltre] = useState<"Tümü" | "Murattal" | "Mücevved">("Tümü");
  const [ara, setAra] = useState("");
  const liste = KARILER.filter((k) => (filtre === "Tümü" || k.tarz === filtre) && (!ara || k.ad.toLocaleLowerCase("tr").includes(ara.toLocaleLowerCase("tr"))));
  const sec = (k: string) => { titret(); if (t.onizleme) T.durdur(); T.ayarla({ kari: k }); kariYaz(k); kapat(); };
  const dinle = (k: string) => {
    titret();
    if (t.onizleme === k && t.aktif) { T.durdur(); return; }
    T.onizle(k);
  };
  return (
    <Modal visible={acik} transparent animationType="slide" onRequestClose={kapat}>
      <Pressable style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.55)" }} onPress={kapat} />
      <View style={{ maxHeight: "82%", backgroundColor: R.bg2, borderTopLeftRadius: 28, borderTopRightRadius: 28, borderWidth: 1, borderColor: ALTIN + "44", paddingBottom: ic.bottom + 8 }}>
        <View style={{ alignItems: "center", paddingTop: 8 }}><View style={{ width: 44, height: 5, borderRadius: 3, backgroundColor: "rgba(255,255,255,0.25)" }} /></View>
        <View style={{ padding: 16, paddingBottom: 8 }}>
          <Text style={{ color: "#fff", fontSize: 20, fontWeight: "800" }}>🎙️ Kâri seç</Text>
          <Text style={{ color: R.soluk, fontSize: 12.5, marginTop: 2 }}>{KARILER.length} hafız • ▶ ile Fâtiha'dan dinleyip karşılaştır</Text>
          <TextInput value={ara} onChangeText={setAra} placeholder="Hafız ara…" placeholderTextColor={R.soluk}
            style={{ marginTop: 10, backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 14, color: "#fff", paddingHorizontal: 14, paddingVertical: 10 }} />
          <View style={{ flexDirection: "row", gap: 8, marginTop: 10 }}>
            {(["Tümü", "Murattal", "Mücevved"] as const).map((f) => <Hap key={f} yazi={f} secili={filtre === f} onPress={() => setFiltre(f)} />)}
          </View>
        </View>
        <ScrollView contentContainerStyle={{ paddingHorizontal: 12, paddingBottom: 12 }}>
          {liste.map((k) => {
            const secili = t.kari === k.k;
            return (
              <Pressable key={k.k} onPress={() => sec(k.k)} style={({ pressed }) => ({ flexDirection: "row", alignItems: "center", gap: 12, padding: 10, borderRadius: 18, marginBottom: 6,
                backgroundColor: secili ? ALTIN + "22" : pressed ? "rgba(255,255,255,0.06)" : "transparent", borderWidth: 1, borderColor: secili ? ALTIN + "88" : "transparent" })}>
                <KariAvatar ad={k.ad} secili={secili} />
                <View style={{ flex: 1 }}>
                  <Text style={{ color: "#fff", fontWeight: "700", fontSize: 15 }}>{k.ad}</Text>
                  <Text style={{ color: R.soluk, fontSize: 12 }}>{k.ulke} {k.tarz} • {k.kbps >= 128 ? "HD " : ""}{k.kbps} kbps</Text>
                </View>
                <Pressable hitSlop={10} onPress={() => dinle(k.k)} style={{ width: 36, height: 36, borderRadius: 18, borderWidth: 1, borderColor: R.cizgi, alignItems: "center", justifyContent: "center" }}>
                  <Ionicons name={t.onizleme === k.k && t.aktif ? "stop" : "play"} size={16} color="#fff" />
                </Pressable>
                {secili ? <Ionicons name="checkmark-circle" size={22} color={ALTIN} /> : null}
              </Pressable>
            );
          })}
        </ScrollView>
      </View>
    </Modal>
  );
}

// ---------- Sure / cüz seçici ----------
function SureSecici({ acik, kapat, sec }: { acik: boolean; kapat: () => void; sec: (n: number) => void }) {
  const ic = useSafeAreaInsets();
  const [ara, setAra] = useState("");
  const q = ara.trim();
  const liste = Array.from({ length: 114 }, (_, i) => i + 1).filter((n) => !q || String(n) === q || (sureBul(q) === n) || SURELER[n - 1].toLocaleLowerCase("tr").includes(q.toLocaleLowerCase("tr")));
  return (
    <Modal visible={acik} transparent animationType="slide" onRequestClose={kapat}>
      <Pressable style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.55)" }} onPress={kapat} />
      <View style={{ height: "80%", backgroundColor: R.bg2, borderTopLeftRadius: 28, borderTopRightRadius: 28, borderWidth: 1, borderColor: ALTIN + "44", paddingBottom: ic.bottom }}>
        <View style={{ padding: 16, paddingBottom: 6 }}>
          <Text style={{ color: "#fff", fontSize: 20, fontWeight: "800" }}>📜 Sure seç</Text>
          <TextInput value={ara} onChangeText={setAra} placeholder="Ad veya numara (ör. Mülk, 67)" placeholderTextColor={R.soluk}
            style={{ marginTop: 10, backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 14, color: "#fff", paddingHorizontal: 14, paddingVertical: 10 }} />
        </View>
        <ScrollView contentContainerStyle={{ padding: 12, flexDirection: "row", flexWrap: "wrap", gap: 8 }} keyboardShouldPersistTaps="handled">
          {liste.map((n) => (
            <Pressable key={n} onPress={() => { titret(); sec(n); kapat(); setAra(""); }}
              style={({ pressed }) => ({ width: "48.5%", flexDirection: "row", alignItems: "center", gap: 10, padding: 10, borderRadius: 16, backgroundColor: pressed ? ALTIN + "22" : R.kart, borderWidth: 1, borderColor: R.cizgi })}>
              <View style={{ width: 34, height: 34, borderRadius: 10, borderWidth: 1.5, borderColor: ALTIN, alignItems: "center", justifyContent: "center", transform: [{ rotate: "45deg" }] }}>
                <Text style={{ color: ALTIN, fontWeight: "800", fontSize: 12, transform: [{ rotate: "-45deg" }] }}>{n}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={{ color: "#fff", fontWeight: "700" }} numberOfLines={1}>{SURELER[n - 1]}</Text>
                <Text style={{ color: R.soluk, fontSize: 11 }}>{AYET_SAYISI[n - 1]} ayet • s.{SURE_SAYFA[n - 1]}</Text>
              </View>
            </Pressable>
          ))}
        </ScrollView>
      </View>
    </Modal>
  );
}

// ---------- Oku & Dinle (mushaf sayfası) ----------
function OkuDinle({ font }: { font?: string }) {
  const t = useTilavet();
  const [a, setA] = useState<OkuAyar | null>(null);
  const [ayetler, setAyetler] = useState<SayfaAyet[]>([]);
  const [bekle, setBekle] = useState(false);
  const [hata, setHata] = useState("");
  const [sureAcik, setSureAcik] = useState(false);
  const [kariAcik, setKariAcik] = useState(false);
  const [acilan, setAcilan] = useState<Set<string>>(new Set());
  const [sayfaYazi, setSayfaYazi] = useState("");
  useEffect(() => { oku<OkuAyar>("arex_kuran_oku", OKU_VARSAYILAN).then((x) => setA({ ...OKU_VARSAYILAN, ...x })); }, []);
  const guncelle = (y: Partial<OkuAyar>) => setA((o) => { const n = { ...(o || OKU_VARSAYILAN), ...y }; yaz("arex_kuran_oku", n); return n; });
  const sayfa = a?.sayfa || 1;
  useEffect(() => {
    if (!a) return;
    let iptal = false;
    setBekle(true); setHata(""); setAcilan(new Set());
    sayfaGetir(sayfa, a.meal).then((l) => { if (!iptal) setAyetler(l); }).catch(() => { if (!iptal) setHata("Sayfa yüklenemedi (internet)."); }).finally(() => { if (!iptal) setBekle(false); });
    sayfaGetir(sayfa + 1, a.meal).catch(() => {});  // sonraki sayfayı önceden hazırla
    return () => { iptal = true; };
  }, [sayfa, a?.meal, !!a]);
  // tilavet sonraki sayfaya geçince görünüm de takip etsin
  useEffect(() => { if (a && t.parca?.sayfa && t.parca.sayfa !== a.sayfa) guncelle({ sayfa: t.parca.sayfa }); }, [t.parca?.sayfa]);
  if (!a) return <ActivityIndicator color={ALTIN} />;

  const cuz = sayfaninCuzu(sayfa);
  const sureNo = sayfaninSuresi(sayfa);
  const kari = kariBul(t.kari);
  const git = (p: number) => { titret(); guncelle({ sayfa: Math.min(604, Math.max(1, p)) }); };
  const parcalar = (l: SayfaAyet[]) => l.map((x) => ({ sure: x.sure, no: x.no, sayfa: x.sayfa }));
  /** Tilavet bitince sıradaki sayfa — sure modunda sure sonunda, cüz modunda cüz sonunda durur */
  const devam = async (son: T.Parca) => {
    const p = (son.sayfa || sayfa) + 1;
    if (p > 604) return null;
    if (a.mod === "cuz" && p > cuzBitis(a.cuz)) return null;
    let l = await sayfaGetir(p, a.meal);
    if (a.mod === "sure") { l = l.filter((x) => x.sure === son.sure); if (!l.length || l[0].no === 1) return null; }
    return parcalar(l);
  };
  const baslat = (i: number) => {
    titret();
    const l = a.mod === "sure" ? ayetler.filter((x) => x.sure === a.sure || ayetler.every((y) => y.sure !== a.sure)) : ayetler;
    const hedef = ayetler[i];
    const j = Math.max(0, l.findIndex((x) => x.sure === hedef?.sure && x.no === hedef?.no));
    T.cal(parcalar(l.length ? l : ayetler), l.length ? j : i, devam);
  };
  /** Yalnız tek ayeti çalar (sayfa devam etmez); "tekrar" ayarı geçerli — ezber için */
  const tekAyet = (x: SayfaAyet, calanMi: boolean) => {
    titret();
    if (calanMi && t.toplam <= 2) { T.durdur(); return; }
    T.cal([{ sure: x.sure, no: x.no, sayfa: x.sayfa }], 0);
  };
  const sayfaCaliyor = t.aktif && t.toplam > 2 && t.parca?.sayfa === sayfa;
  const fs = 26 * a.yazi;

  const modSecici = (
      <View style={{ flexDirection: "row", backgroundColor: R.kart, borderRadius: 18, padding: 4, borderWidth: 1, borderColor: R.cizgi, marginBottom: 10 }}>
        {([["ayet", "🎯 Ayet"], ["sure", "📜 Sure"], ["cuz", "📚 Cüz"], ["sayfa", "📄 Sayfa"]] as [Mod, string][]).map(([m, ad]) => (
          <Pressable key={m} onPress={() => { titret(); guncelle({ mod: m }); }} style={{ flex: 1, borderRadius: 14, overflow: "hidden" }}>
            {a.mod === m ? <LinearGradient colors={[ALTIN, "#c99a3e"]} style={{ paddingVertical: 10, alignItems: "center" }}><Text style={{ color: "#1a1408", fontWeight: "800", fontSize: 13 }}>{ad}</Text></LinearGradient>
              : <View style={{ paddingVertical: 10, alignItems: "center" }}><Text style={{ color: R.yazi, fontWeight: "600", fontSize: 13 }}>{ad}</Text></View>}
          </Pressable>
        ))}
      </View>
  );
  if (a.mod === "ayet") return (
    <View>
      {modSecici}
      <AyetModu a={a} guncelle={guncelle} font={font} sureSec={() => setSureAcik(true)} kariSec={() => setKariAcik(true)} />
      <SureSecici acik={sureAcik} kapat={() => setSureAcik(false)} sec={(n) => guncelle({ sure: n, ayet: 1, sayfa: SURE_SAYFA[n - 1] })} />
      <KariSecici acik={kariAcik} kapat={() => setKariAcik(false)} />
    </View>
  );

  return (
    <View>
      {modSecici}

      <Kart>
        {a.mod === "sure" ? (
          <Pressable onPress={() => setSureAcik(true)} style={{ flexDirection: "row", alignItems: "center", gap: 12 }}>
            <View style={{ flex: 1 }}>
              <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "600" }}>SURE</Text>
              <Text style={{ color: "#fff", fontSize: 22, fontWeight: "800" }}>{a.sure}. {SURELER[a.sure - 1]}</Text>
              <Text style={{ color: ALTIN, fontSize: 12.5 }}>{AYET_SAYISI[a.sure - 1]} ayet • {SURE_SAYFA[a.sure - 1]}. sayfadan başlar</Text>
            </View>
            <View style={{ flexDirection: "row", alignItems: "center", gap: 4, backgroundColor: R.hap, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 14 }}>
              <Text style={{ color: "#fff", fontWeight: "700" }}>Değiştir</Text><Ionicons name="chevron-down" size={16} color="#fff" />
            </View>
          </Pressable>
        ) : a.mod === "cuz" ? (
          <View>
            <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "600", marginBottom: 8 }}>CÜZ SEÇ • {a.cuz}. cüz: sayfa {cuzBaslangic(a.cuz)}–{cuzBitis(a.cuz)}</Text>
            <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 6 }}>
              {Array.from({ length: 30 }, (_, i) => i + 1).map((c) => {
                const sec = a.cuz === c;
                return (
                  <Pressable key={c} onPress={() => { titret(); guncelle({ cuz: c, sayfa: cuzBaslangic(c) }); }}
                    style={{ width: "15.2%", aspectRatio: 1, borderRadius: 12, alignItems: "center", justifyContent: "center", backgroundColor: sec ? ALTIN : R.kart, borderWidth: 1, borderColor: sec ? ALTIN : R.cizgi }}>
                    <Text style={{ color: sec ? "#1a1408" : "#fff", fontWeight: "800" }}>{c}</Text>
                  </Pressable>
                );
              })}
            </View>
          </View>
        ) : (
          <View style={{ flexDirection: "row", alignItems: "flex-end", gap: 10 }}>
            <View style={{ flex: 1 }}>
              <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "600", marginBottom: 6 }}>SAYFAYA GİT (1–604)</Text>
              <TextInput value={sayfaYazi} onChangeText={setSayfaYazi} keyboardType="number-pad" placeholder={String(sayfa)} placeholderTextColor={R.soluk}
                onSubmitEditing={() => { if (Number(sayfaYazi)) git(Number(sayfaYazi)); setSayfaYazi(""); }}
                style={{ backgroundColor: R.kart, borderColor: R.cizgi, borderWidth: 1, borderRadius: 14, color: "#fff", paddingHorizontal: 14, paddingVertical: 10, fontSize: 18, fontWeight: "700" }} />
            </View>
            <Dugme yazi="Git" onPress={() => { if (Number(sayfaYazi)) git(Number(sayfaYazi)); setSayfaYazi(""); }} style={{ width: 80 }} />
          </View>
        )}
        {/* Kâri */}
        <Pressable onPress={() => setKariAcik(true)} style={{ flexDirection: "row", alignItems: "center", gap: 10, marginTop: 14, padding: 10, borderRadius: 16, backgroundColor: "rgba(255,255,255,0.04)", borderWidth: 1, borderColor: R.cizgi }}>
          <KariAvatar ad={kari.ad} secili />
          <View style={{ flex: 1 }}>
            <Text style={{ color: R.soluk, fontSize: 11, fontWeight: "600" }}>KÂRİ • {KARILER.length} hafız arasından seç</Text>
            <Text style={{ color: "#fff", fontWeight: "800", fontSize: 15 }}>{kari.ad}</Text>
            <Text style={{ color: ALTIN, fontSize: 11.5 }}>{kari.ulke} {kari.tarz} • {kari.kbps} kbps</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={R.soluk} />
        </Pressable>
        {/* Dinleme ayarları */}
        <Text style={[us.etiket, { marginTop: 12 }]}>🔁 Her ayeti tekrarla (ezber için)</Text>
        <View style={{ flexDirection: "row", gap: 6 }}>
          {[1, 3, 5, 7, 10].map((n) => <Hap key={n} yazi={n === 1 ? "1 kez" : n + "x"} secili={t.tekrar === n} onPress={() => T.ayarla({ tekrar: n })} />)}
        </View>
        <Text style={[us.etiket, { marginTop: 10 }]}>⏱ Okuma hızı</Text>
        <View style={{ flexDirection: "row", gap: 6 }}>
          {[0.75, 1, 1.25, 1.5].map((n) => <Hap key={n} yazi={n + "x"} secili={t.hiz === n} onPress={() => T.ayarla({ hiz: n })} />)}
        </View>
        <View style={{ flexDirection: "row", gap: 8, marginTop: 14 }}>
          <Dugme yazi={sayfaCaliyor ? "⏹ Durdur" : a.mod === "sure" ? "🎧 Sureyi dinle" : a.mod === "cuz" ? "🎧 Cüzü dinle" : "🎧 Sayfayı dinle"}
            onPress={() => {
              if (sayfaCaliyor) { T.durdur(); return; }
              if (a.mod === "sure" && sayfa !== SURE_SAYFA[a.sure - 1]) { guncelle({ sayfa: SURE_SAYFA[a.sure - 1] }); setTimeout(() => sayfaGetir(SURE_SAYFA[a.sure - 1], a.meal).then((l) => { const f = l.filter((x) => x.sure === a.sure); T.cal(parcalar(f), 0, devam); }), 0); return; }
              baslat(0);
            }} style={{ flex: 1 }} />
        </View>
      </Kart>

      {/* Okuma seçenekleri — görsel aç/kapat anahtarları */}
      <Kart style={{ paddingVertical: 6 }}>
        <AnahtarSatiri simge="📝" baslik="Meal" alt={a.mealGoster ? MEALLER[a.meal] + " meali gösteriliyor" : "Yalnız Arapça metin"} acik={a.mealGoster} renk={ALTIN} onChange={(v) => guncelle({ mealGoster: v })} />
        <View style={{ height: 1, backgroundColor: R.cizgi }} />
        <AnahtarSatiri simge="🙈" baslik="Ezber modu" alt={a.ezber ? "Ayetler gizli • dokununca açılır" : "Kendini sınamak için ayetleri gizle"} acik={a.ezber} renk={ALTIN} onChange={(v) => { guncelle({ ezber: v }); setAcilan(new Set()); }} />
        <View style={{ height: 1, backgroundColor: R.cizgi }} />
        <View style={{ flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 10 }}>
          <View style={{ width: 38, height: 38, borderRadius: 12, alignItems: "center", justifyContent: "center", backgroundColor: "rgba(255,255,255,0.06)" }}><Text style={{ fontSize: 18 }}>🔠</Text></View>
          <Text style={{ color: "#fff", fontWeight: "700", fontSize: 15, flex: 1 }}>Yazı boyutu</Text>
          <Pressable hitSlop={8} onPress={() => { titret(); guncelle({ yazi: Math.max(0.8, +(a.yazi - 0.1).toFixed(1)) }); }} style={yuvarlak}><Text style={{ color: "#fff", fontWeight: "800" }}>A−</Text></Pressable>
          <Text style={{ color: ALTIN, fontWeight: "800", width: 44, textAlign: "center" }}>%{Math.round(a.yazi * 100)}</Text>
          <Pressable hitSlop={8} onPress={() => { titret(); guncelle({ yazi: Math.min(1.6, +(a.yazi + 0.1).toFixed(1)) }); }} style={yuvarlak}><Text style={{ color: "#fff", fontWeight: "800", fontSize: 17 }}>A+</Text></Pressable>
        </View>
        {a.mealGoster ? (
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 6, paddingBottom: 10 }}>
            {Object.entries(MEALLER).map(([k, v]) => <Hap key={k} yazi={v} secili={a.meal === k} onPress={() => guncelle({ meal: k })} />)}
          </ScrollView>
        ) : null}
      </Kart>

      {/* Mushaf sayfası */}
      <View style={{ borderRadius: 26, borderWidth: 1.5, borderColor: ALTIN + "77", backgroundColor: "rgba(20,18,40,0.75)", padding: 4, marginBottom: 10 }}>
        <View style={{ borderRadius: 22, borderWidth: 1, borderColor: ALTIN + "33", padding: 14 }}>
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginBottom: 8 }}>
            <Text style={{ color: ALTIN, fontWeight: "700", fontSize: 12 }}>{Array.from(new Set(ayetler.map((x) => x.sureAd))).join(" • ") || SURELER[sureNo - 1]}</Text>
            <Text style={{ color: ALTIN, fontWeight: "700", fontSize: 12 }}>{cuz}. Cüz</Text>
          </View>
          {bekle && !ayetler.length ? <ActivityIndicator color={ALTIN} style={{ marginVertical: 30 }} /> : null}
          {hata ? <Text style={{ color: R.kirmizi, textAlign: "center", marginVertical: 20 }}>{hata}</Text> : null}
          {ayetler.map((x, i) => {
            const anahtar = x.sure + ":" + x.no;
            const calan = t.aktif && !t.parca?.besmele && t.parca?.sure === x.sure && t.parca?.no === x.no;
            const gizli = a.ezber && !acilan.has(anahtar) && !calan;
            return (
              <View key={anahtar}>
                {x.no === 1 ? (
                  <View style={{ marginTop: i ? 14 : 4, marginBottom: 8 }}>
                    <LinearGradient colors={[ALTIN + "33", ALTIN + "11", ALTIN + "33"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={{ borderRadius: 14, borderWidth: 1, borderColor: ALTIN + "88", paddingVertical: 8, alignItems: "center" }}>
                      <Text style={{ color: ALTIN, fontSize: 20, fontFamily: font, fontWeight: font ? undefined : "700" }}>{x.sureArapca}</Text>
                      <Text style={{ color: "#fff", fontSize: 12, fontWeight: "700" }}>{x.sure}. {x.sureAd} • {AYET_SAYISI[x.sure - 1]} ayet</Text>
                    </LinearGradient>
                    {x.sure !== 1 && x.sure !== 9 ? <Text style={[ARAPCA, { textAlign: "center", fontFamily: font, fontSize: fs * 0.9, lineHeight: fs * 1.9, marginTop: 6 }]}>{BESMELE}</Text> : null}
                  </View>
                ) : null}
                <Pressable onPress={() => { if (gizli) { titret(); setAcilan(new Set([...acilan, anahtar])); } else tekAyet(x, calan); }} onLongPress={() => baslat(i)} delayLongPress={400}
                  style={{ borderRadius: 14, paddingHorizontal: 6, paddingVertical: 4, backgroundColor: calan ? ALTIN + "22" : "transparent", borderWidth: calan ? 1 : 0, borderColor: ALTIN + "66" }}>
                  {gizli ? (
                    <View style={{ flexDirection: "row-reverse", alignItems: "center", gap: 8, paddingVertical: 10 }}>
                      <Text style={[ARAPCA, { fontFamily: font, fontSize: fs, lineHeight: fs * 1.9 }]}>{x.arapca.split(" ")[0]} …</Text>
                      <Text style={{ color: R.soluk, fontSize: 12 }}>({arapRakam(x.no)}) dokun → göster</Text>
                    </View>
                  ) : (
                    <Text style={[ARAPCA, { fontFamily: font, fontSize: fs, lineHeight: fs * 1.95 }]}>
                      {x.arapca} <Text style={{ color: ALTIN, fontSize: fs * 0.8 }}>﴿{arapRakam(x.no)}﴾</Text>
                    </Text>
                  )}
                  {a.mealGoster && !gizli ? <Text style={{ color: "#d9def7", fontSize: 14.5 * a.yazi, lineHeight: 22 * a.yazi, marginTop: 2, marginBottom: 6 }}><Text style={{ color: ALTIN, fontWeight: "800" }}>{x.no}. </Text>{x.meal}</Text> : null}
                  {/* Ayet düğmeleri: yalnız bu ayet / buradan devam */}
                  <View style={{ flexDirection: "row", gap: 6, marginTop: 2, marginBottom: 6 }}>
                    <Pressable hitSlop={6} onPress={() => tekAyet(x, calan)} style={[ayetDugme, calan && t.toplam <= 2 ? { backgroundColor: ALTIN, borderColor: ALTIN } : null]}>
                      <Ionicons name={calan && t.toplam <= 2 ? "stop" : "play"} size={13} color={calan && t.toplam <= 2 ? "#1a1408" : ALTIN} />
                      <Text style={{ color: calan && t.toplam <= 2 ? "#1a1408" : ALTIN, fontSize: 12, fontWeight: "800" }}>{x.no}. ayeti dinle{t.tekrar > 1 ? ` (${t.tekrar}x)` : ""}</Text>
                    </Pressable>
                    <Pressable hitSlop={6} onPress={() => baslat(i)} style={ayetDugme}>
                      <Ionicons name="play-forward" size={13} color={R.soluk} />
                      <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "700" }}>Buradan devam</Text>
                    </Pressable>
                  </View>
                </Pressable>
              </View>
            );
          })}
          <Text style={{ color: ALTIN, textAlign: "center", fontWeight: "800", marginTop: 8 }}>— {arapRakam(sayfa)} —</Text>
        </View>
      </View>
      <Text style={{ color: R.soluk, fontSize: 11.5, textAlign: "center", marginBottom: 8 }}>Ayete dokun → yalnız o ayet • Basılı tut → oradan devam{a.ezber ? " • Gizli ayete dokun → göster" : ""}</Text>
      <View style={{ flexDirection: "row", gap: 8 }}>
        <Dugme ikincil yazi="‹ Önceki sayfa" onPress={() => git(sayfa - 1)} devreDisi={sayfa <= 1} style={{ flex: 1 }} />
        <Dugme ikincil yazi="Sonraki sayfa ›" onPress={() => git(sayfa + 1)} devreDisi={sayfa >= 604} style={{ flex: 1 }} />
      </View>
      <Text style={{ color: R.soluk, fontSize: 11, marginTop: 10, textAlign: "center" }}>Metin & meal: alquran.cloud ({MEALLER[a.meal]}) • Ses: everyayah.com • Hat: Amiri Quran</Text>
      <SureSecici acik={sureAcik} kapat={() => setSureAcik(false)} sec={(n) => guncelle({ sure: n, sayfa: SURE_SAYFA[n - 1] })} />
      <KariSecici acik={kariAcik} kapat={() => setKariAcik(false)} />
    </View>
  );
}

// ---------- 🎯 Ayet modu: tek ayet seç, dinle, tekrarla (ezber) ----------
function AyetModu({ a, guncelle, font, sureSec, kariSec }: { a: OkuAyar; guncelle: (y: Partial<OkuAyar>) => void; font?: string; sureSec: () => void; kariSec: () => void }) {
  const t = useTilavet();
  const no = Math.min(AYET_SAYISI[a.sure - 1], Math.max(1, a.ayet || 1));
  const [ayet, setAyet] = useState<Ayet | null>(null);
  const [hata, setHata] = useState("");
  const [yazi, setYazi] = useState("");
  const kari = kariBul(t.kari);
  useEffect(() => {
    let iptal = false; setHata("");
    ayetGetir(a.sure, no, no, a.meal).then((l) => { if (!iptal) setAyet(l[0] || null); }).catch(() => { if (!iptal) setHata("Ayet yüklenemedi (internet)."); });
    return () => { iptal = true; };
  }, [a.sure, no, a.meal]);
  // "sonraki ayete geç" açıkken çalan ayeti takip et
  useEffect(() => { if (t.aktif && !t.parca?.besmele && t.parca && (t.parca.sure !== a.sure || t.parca.no !== no)) guncelle({ sure: t.parca.sure, ayet: t.parca.no }); }, [t.parca?.sure, t.parca?.no]);
  const sec = (n: number) => { titret(); guncelle({ ayet: Math.min(AYET_SAYISI[a.sure - 1], Math.max(1, n)) }); };
  const calan = t.aktif && t.parca?.sure === a.sure && (t.parca?.no === no || !!t.parca?.besmele);
  const dinle = () => {
    titret();
    if (calan) { T.durdur(); return; }
    const devam = a.ayetDevam ? async (son: T.Parca) => (son.no < AYET_SAYISI[son.sure - 1] ? [{ sure: son.sure, no: son.no + 1 }] : null) : undefined;
    T.cal([{ sure: a.sure, no }], 0, devam);
  };
  const fs = 30 * a.yazi;
  return (
    <View>
      <Kart>
        <Pressable onPress={sureSec} style={{ flexDirection: "row", alignItems: "center", gap: 12 }}>
          <View style={{ flex: 1 }}>
            <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "600" }}>SURE</Text>
            <Text style={{ color: "#fff", fontSize: 20, fontWeight: "800" }}>{a.sure}. {SURELER[a.sure - 1]}</Text>
          </View>
          <View style={{ flexDirection: "row", alignItems: "center", gap: 4, backgroundColor: R.hap, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 14 }}>
            <Text style={{ color: "#fff", fontWeight: "700" }}>Değiştir</Text><Ionicons name="chevron-down" size={16} color="#fff" />
          </View>
        </Pressable>
        <Text style={{ color: R.soluk, fontSize: 12, fontWeight: "600", marginTop: 14, marginBottom: 8 }}>AYET</Text>
        <View style={{ flexDirection: "row", alignItems: "center", gap: 10 }}>
          <Pressable onPress={() => sec(no - 1)} disabled={no <= 1} style={[yuvarlak, { width: 48, height: 48, borderRadius: 24, opacity: no <= 1 ? 0.4 : 1 }]}><Ionicons name="remove" size={24} color="#fff" /></Pressable>
          <View style={{ flex: 1, alignItems: "center" }}>
            <TextInput value={yazi} onChangeText={setYazi} keyboardType="number-pad" placeholder={String(no)} placeholderTextColor="#fff"
              onSubmitEditing={() => { if (Number(yazi)) sec(Number(yazi)); setYazi(""); }} onBlur={() => { if (Number(yazi)) sec(Number(yazi)); setYazi(""); }}
              style={{ color: "#fff", fontSize: 34, fontWeight: "900", textAlign: "center", minWidth: 90, padding: 0 }} />
            <Text style={{ color: ALTIN, fontSize: 12 }}>/ {AYET_SAYISI[a.sure - 1]} ayet • dokun → numara yaz</Text>
          </View>
          <Pressable onPress={() => sec(no + 1)} disabled={no >= AYET_SAYISI[a.sure - 1]} style={[yuvarlak, { width: 48, height: 48, borderRadius: 24, opacity: no >= AYET_SAYISI[a.sure - 1] ? 0.4 : 1 }]}><Ionicons name="add" size={24} color="#fff" /></Pressable>
        </View>
        <Pressable onPress={kariSec} style={{ flexDirection: "row", alignItems: "center", gap: 10, marginTop: 14, padding: 10, borderRadius: 16, backgroundColor: "rgba(255,255,255,0.04)", borderWidth: 1, borderColor: R.cizgi }}>
          <KariAvatar ad={kari.ad} secili boyut={36} />
          <View style={{ flex: 1 }}>
            <Text style={{ color: "#fff", fontWeight: "800" }}>{kari.ad}</Text>
            <Text style={{ color: ALTIN, fontSize: 11.5 }}>{kari.tarz} • {kari.kbps} kbps • değiştir</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={R.soluk} />
        </Pressable>
        <Text style={[us.etiket, { marginTop: 12 }]}>🔁 Tekrar sayısı</Text>
        <View style={{ flexDirection: "row", gap: 6, flexWrap: "wrap" }}>
          {[1, 3, 5, 7, 10, 20].map((n) => <Hap key={n} yazi={n === 1 ? "1 kez" : n + "x"} secili={t.tekrar === n} onPress={() => T.ayarla({ tekrar: n })} />)}
        </View>
        <Text style={[us.etiket, { marginTop: 10 }]}>⏱ Hız</Text>
        <View style={{ flexDirection: "row", gap: 6 }}>
          {[0.75, 1, 1.25, 1.5].map((n) => <Hap key={n} yazi={n + "x"} secili={t.hiz === n} onPress={() => T.ayarla({ hiz: n })} />)}
        </View>
        <View style={{ height: 1, backgroundColor: R.cizgi, marginTop: 12 }} />
        <AnahtarSatiri simge="⏭" baslik="Bitince sonraki ayete geç" alt={a.ayetDevam ? "Ayetler sırayla devam eder" : "Yalnız seçili ayet okunur"} acik={!!a.ayetDevam} renk={ALTIN} onChange={(v) => guncelle({ ayetDevam: v })} />
        <AnahtarSatiri simge="📝" baslik="Meal" acik={a.mealGoster} renk={ALTIN} onChange={(v) => guncelle({ mealGoster: v })} />
      </Kart>

      <LinearGradient colors={[ALTIN + "26", "rgba(20,18,40,0.8)"]} style={{ borderRadius: 26, borderWidth: 1.5, borderColor: calan ? ALTIN : ALTIN + "66", padding: 18, marginBottom: 12 }}>
        <View style={{ flexDirection: "row", justifyContent: "space-between", marginBottom: 6 }}>
          <Text style={{ color: ALTIN, fontWeight: "800" }}>{SURELER[a.sure - 1]} • {no}. ayet</Text>
          {ayet ? <Text style={{ color: R.soluk, fontSize: 12 }}>{ayet.sureArapca}</Text> : null}
        </View>
        {hata ? <Text style={{ color: R.kirmizi, textAlign: "center", marginVertical: 20 }}>{hata}</Text> : !ayet ? <ActivityIndicator color={ALTIN} style={{ marginVertical: 30 }} /> : (
          <>
            <Text style={[ARAPCA, { fontFamily: font, fontSize: fs, lineHeight: fs * 1.95, textAlign: "center" }]}>{ayet.arapca} <Text style={{ color: ALTIN, fontSize: fs * 0.8 }}>﴿{arapRakam(no)}﴾</Text></Text>
            {a.mealGoster ? <Text style={{ color: "#d9def7", fontSize: 15.5 * a.yazi, lineHeight: 24 * a.yazi, marginTop: 8, textAlign: "center" }}>{ayet.meal}</Text> : null}
          </>
        )}
        <Pressable onPress={dinle} style={{ alignSelf: "center", marginTop: 16, flexDirection: "row", alignItems: "center", gap: 8, backgroundColor: calan ? "#fff" : ALTIN, paddingHorizontal: 22, paddingVertical: 13, borderRadius: 999 }}>
          {calan && t.yukleniyor ? <ActivityIndicator color="#1a1408" /> : <Ionicons name={calan ? "stop" : "play"} size={20} color="#1a1408" />}
          <Text style={{ color: "#1a1408", fontWeight: "900", fontSize: 15 }}>
            {calan ? `Durdur${t.tekrar > 1 ? ` (${t.tekrarSayac}/${t.tekrar})` : ""}` : `Bu ayeti dinle${t.tekrar > 1 ? ` • ${t.tekrar} kez` : ""}`}
          </Text>
        </Pressable>
      </LinearGradient>
      <View style={{ flexDirection: "row", gap: 8 }}>
        <Dugme ikincil yazi="‹ Önceki ayet" onPress={() => sec(no - 1)} devreDisi={no <= 1} style={{ flex: 1 }} />
        <Dugme ikincil yazi="Sonraki ayet ›" onPress={() => sec(no + 1)} devreDisi={no >= AYET_SAYISI[a.sure - 1]} style={{ flex: 1 }} />
      </View>
    </View>
  );
}

function AyetKart({ a, font }: { a: Ayet; font?: string }) {
  const t = useTilavet();
  const calan = t.aktif && t.parca?.sure === a.sure && t.parca?.no === a.no;
  return (
    <Kart style={calan ? { borderColor: ALTIN, backgroundColor: ALTIN + "18" } : undefined}>
      <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 6 }}>
        <View style={{ backgroundColor: ALTIN + "33", borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4 }}><Text style={{ color: ALTIN, fontWeight: "800", fontSize: 12 }}>{a.sureAd} {a.no}</Text></View>
        <View style={{ flex: 1 }} />
        <Pressable onPress={() => { titret(); calan ? T.durdur() : T.cal([{ sure: a.sure, no: a.no }]); }} hitSlop={10}
          style={{ width: 38, height: 38, borderRadius: 19, backgroundColor: ALTIN, alignItems: "center", justifyContent: "center" }}>
          <Ionicons name={calan ? "stop" : "play"} size={18} color="#1a1408" />
        </Pressable>
      </View>
      <Text style={[ARAPCA, { fontFamily: font, lineHeight: 52 }]}>{a.arapca} <Text style={{ color: ALTIN }}>﴿{arapRakam(a.no)}﴾</Text></Text>
      <Text style={{ color: R.yazi, fontSize: 15.5 * (R.olcek || 1), lineHeight: 24 * (R.olcek || 1), marginTop: 8 }}>{a.meal}</Text>
    </Kart>
  );
}

function Bugun({ git, font }: { git: (s: Sekme) => void; font?: string }) {
  const [ayet, setAyet] = useState<Ayet | null>(null);
  const [hadis, setHadis] = useState<Hadis | null>(null);
  const [es, setEs] = useState<any>(null);
  const [h, setH] = useState<Hafizlik | null>(null);
  const [son, setSon] = useState<OkuAyar | null>(null);
  const [hata, setHata] = useState("");
  useEffect(() => {
    gununAyeti().then(setAyet).catch(() => setHata("Ayet yüklenemedi (internet)."));
    gununHadisi().then(setHadis).catch(() => {});
    esma().then(setEs).catch(() => {});
    hafizlikOku().then(setH);
    oku<OkuAyar | null>("arex_kuran_oku", null).then(setSon);
  }, []);
  const yapilan = h ? bugunkuSayfa(h) : 0;
  const oran = h ? Math.min(1, yapilan / Math.max(1, h.hedefSayfa)) : 0;
  return (
    <View>
      {son ? (
        <Pressable onPress={() => git("oku")}>
          <LinearGradient colors={[ALTIN + "30", ALTIN + "0a"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 22, borderWidth: 1, borderColor: ALTIN + "66", padding: 14, marginBottom: 12, flexDirection: "row", alignItems: "center", gap: 12 }}>
            <Ionicons name="bookmark" size={26} color={ALTIN} />
            <View style={{ flex: 1 }}>
              <Text style={{ color: R.soluk, fontSize: 11, fontWeight: "700" }}>KALDIĞIN YER</Text>
              <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16 }}>Sayfa {son.sayfa} • {SURELER[sayfaninSuresi(son.sayfa) - 1]} • {sayfaninCuzu(son.sayfa)}. cüz</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={ALTIN} />
          </LinearGradient>
        </Pressable>
      ) : null}
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
            <LinearGradient colors={[ALTIN, "#c99a3e"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={{ width: `${oran * 100}%`, height: "100%" }} />
          </View>
          <Dugme kucuk ikincil yazi="🧠 Hafızlık kaydı ekle" onPress={() => git("hafizlik")} style={{ marginTop: 10 }} />
        </Kart>
      ) : null}
      <Text style={[us.etiket, { marginTop: 4 }]}>📖 GÜNÜN AYETİ</Text>
      {ayet ? <AyetKart a={ayet} font={font} /> : <Kart>{hata ? <Text style={us.alt}>{hata}</Text> : <ActivityIndicator color={ALTIN} />}</Kart>}
      <Text style={us.etiket}>🌙 GÜNÜN HADİSİ</Text>
      <Kart>
        {hadis ? (
          <>
            <Text style={{ color: "#fff", fontWeight: "800", fontSize: 16, marginBottom: 6 }}>{hadis.baslik}</Text>
            <Text style={{ color: R.yazi, fontSize: 15, lineHeight: 23 }}>{hadis.metin}</Text>
            <Text style={{ color: ALTIN, fontSize: 12, marginTop: 8 }}>{hadis.kaynak} • {hadis.derece} • HadeethEnc</Text>
          </>
        ) : <ActivityIndicator color={ALTIN} />}
      </Kart>
      {es ? (
        <Kart>
          <Text style={us.etiket}>✨ GÜNÜN ESMÂSI — {es.no}.</Text>
          <Text style={[ARAPCA, { textAlign: "center", fontSize: 36, lineHeight: 70, color: ALTIN, fontFamily: font }]}>{es.isim}</Text>
          <Text style={{ color: "#fff", textAlign: "center", fontWeight: "700" }}>{es.okunus}</Text>
          <Text style={[us.alt, { textAlign: "center" }]}>{es.anlam}</Text>
        </Kart>
      ) : null}
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

// ---------- 🎵 Neşid & İlahi: dokununca YouTube'da ilk sonuç doğrudan oynar (sözler uygulamada tutulmaz) ----------
// 4. alan: true → ilk video doğrudan çalar (YouTube adı doğrulandı), false → arama sonuçları açılır (adı farklı olabilir; yanlış video çalmasın)
const NESIDLER: { b: string; liste: [string, string, string, boolean][] }[] = [
  { b: "🔥 Dava & Direniş", liste: [
    ["Dava Aşkı", "dava aşkı neşid", "Sabır ve kararlılık", false], ["Yenileceksiniz", "yenileceksiniz neşid", "Diriliş ve umut", true],
    ["Başkaldırı", "başkaldırı neşid", "Zulme karşı duruş", true], ["Tevhid Aşkı", "tevhid aşkı neşid", "Birlik ve iman", false],
    ["Kudüs", "kudüs neşid türkçe", "Mescid-i Aksa sevgisi", false], ["Gazze", "gazze neşid", "Dayanışma", false] ] },
  { b: "🌙 Aşk & Huzur", liste: [
    ["Aşk Tepelerine Dolunay Yağdı", "aşk tepelerine dolunay yağdı ilahi", "Muhabbet ve hasret", false], ["Tala'al Bedru Aleyna", "tala al bedru aleyna", "Medine'nin karşılaması", true],
    ["Ya Nebi Selam Aleyke", "ya nebi selam aleyke", "Salavat", true], ["Esmaül Hüsna", "esmaül hüsna ilahi", "Allah'ın güzel isimleri", true],
    ["Hasbi Rabbi", "hasbi rabbi cellallah", "Tevekkül", true], ["Medine'ye Varamadım", "medineye varamadım ilahi", "Peygamber özlemi", false] ] },
  { b: "🕊️ Sakin & Derin", liste: [
    ["Mevlana Sözleri ile Ney", "ney taksim huzur", "Ney ile tefekkür", false], ["Kalbim Seni Arar", "kalbim seni arar ilahi", "İç yolculuk", false],
    ["Allah Allah Diyelim", "allah allah diyelim ilahi", "Zikir", true], ["Sübhanallah Zikri", "subhanallah zikir neşid", "Tesbih", false] ] },
];
function Nesidler() {
  const [ara, setAra] = useState("");
  const [bekle, setBekle] = useState("");
  const cal = async (ad: string, sorgu: string, kesin = true) => {
    titret(); setBekle(ad);
    const { ilkVideo } = await import("../telefon");
    const id = kesin ? await ilkVideo(sorgu) : null;
    const { Linking } = await import("react-native");
    try { await Linking.openURL(id ? `vnd.youtube://${id}` : `https://www.youtube.com/results?search_query=${encodeURIComponent(sorgu)}`); }
    catch { await Linking.openURL(id ? `https://www.youtube.com/watch?v=${id}` : `https://www.youtube.com/results?search_query=${encodeURIComponent(sorgu)}`).catch(() => {}); }
    setBekle("");
  };
  return (
    <View>
      <LinearGradient colors={["#2a1748", "#0e1a33"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 22, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: ALTIN + "44" }}>
        <Text style={{ color: "#fff", fontSize: 18, fontWeight: "800" }}>🎵 Neşid & İlahi</Text>
        <Text style={{ color: "#c9cfee", fontSize: 12.5, marginTop: 4 }}>Dokun → YouTube'da hemen çalar. Sesle de: "Dava aşkı neşidini aç".</Text>
        <View style={{ flexDirection: "row", gap: 8, marginTop: 12 }}>
          <TextInput value={ara} onChangeText={setAra} onSubmitEditing={() => ara.trim() && cal(ara.trim(), ara.trim() + " neşid")} returnKeyType="search" placeholder="Başka bir neşid / ilahi ara…" placeholderTextColor={R.soluk}
            style={{ flex: 1, backgroundColor: "rgba(255,255,255,0.07)", borderRadius: 14, borderWidth: 1, borderColor: "rgba(255,255,255,0.14)", color: "#fff", paddingHorizontal: 14, paddingVertical: 10 }} />
          <Pressable onPress={() => ara.trim() && cal(ara.trim(), ara.trim() + " neşid")} style={{ width: 44, borderRadius: 14, backgroundColor: ALTIN, alignItems: "center", justifyContent: "center" }}>
            <Ionicons name="play" size={20} color="#1a1408" />
          </Pressable>
        </View>
      </LinearGradient>
      {NESIDLER.map((g) => (
        <View key={g.b} style={{ marginBottom: 6 }}>
          <Text style={[us.etiket, { marginTop: 6 }]}>{g.b}</Text>
          {g.liste.map(([ad, sorgu, alt, kesin]) => (
            <Pressable key={ad} onPress={() => cal(ad, sorgu, kesin)} style={({ pressed }) => ({ flexDirection: "row", alignItems: "center", gap: 12, padding: 12, borderRadius: 18, marginBottom: 8,
              backgroundColor: pressed ? ALTIN + "22" : R.kart, borderWidth: 1, borderColor: R.cizgi })}>
              <LinearGradient colors={[ALTIN, "#b8862f"]} style={{ width: 42, height: 42, borderRadius: 21, alignItems: "center", justifyContent: "center" }}>
                {bekle === ad ? <ActivityIndicator color="#1a1408" /> : <Ionicons name="play" size={18} color="#1a1408" style={{ marginLeft: 2 }} />}
              </LinearGradient>
              <View style={{ flex: 1 }}>
                <Text style={{ color: "#fff", fontWeight: "800", fontSize: 15 }}>{ad}</Text>
                <Text style={{ color: R.soluk, fontSize: 12 }}>{alt}</Text>
              </View>
              {kesin ? <Ionicons name="logo-youtube" size={20} color="#ff4d4d" /> : <Ionicons name="search" size={18} color={R.soluk} />}
            </Pressable>
          ))}
        </View>
      ))}
    </View>
  );
}
