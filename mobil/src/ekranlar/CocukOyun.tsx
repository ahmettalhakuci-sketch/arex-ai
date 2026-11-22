// AREX — 🎮 Çocuk Dünyası eğitici oyunlar (internetsiz): yaşa göre Matematik Yarışı, çok dilli Kelime Avı, Hafıza Kartları
import * as Speech from "expo-speech";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect, useMemo, useState } from "react";
import { Pressable, Text, View } from "react-native";
import { titret } from "../ui";

const rnd = (n: number) => Math.floor(Math.random() * n);
const karistir = <T,>(a: T[]) => a.map((x) => [Math.random(), x] as const).sort((p, q) => p[0] - q[0]).map((p) => p[1]);
const soyle = (m: string, dil = "tr-TR") => { try { Speech.stop(); Speech.speak(m, { language: dil, rate: 0.95 }); } catch {} };

function Kart({ children, renk = ["#2a1f5c", "#14183a"] as [string, string] }: { children: React.ReactNode; renk?: [string, string] }) {
  return <LinearGradient colors={renk} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 26, padding: 18, marginBottom: 12, borderWidth: 1, borderColor: "rgba(255,255,255,0.12)" }}>{children}</LinearGradient>;
}
function Puan({ dogru, toplam }: { dogru: number; toplam: number }) {
  return (
    <View style={{ flexDirection: "row", justifyContent: "center", gap: 18, marginBottom: 10 }}>
      <Text style={{ color: "#ffd166", fontSize: 18, fontWeight: "800" }}>⭐ {dogru}</Text>
      <Text style={{ color: "#9aa3c7", fontSize: 15 }}>/ {toplam} soru</Text>
    </View>
  );
}
function Secenek({ yazi, onPress, durum }: { yazi: string; onPress: () => void; durum?: "dogru" | "yanlis" }) {
  return (
    <Pressable onPress={onPress} style={({ pressed }) => ({ width: "47.5%", transform: [{ scale: pressed ? 0.96 : 1 }] })}>
      <View style={{ borderRadius: 20, paddingVertical: 18, alignItems: "center", borderWidth: 2,
        backgroundColor: durum === "dogru" ? "rgba(46,229,157,0.25)" : durum === "yanlis" ? "rgba(255,77,109,0.22)" : "rgba(255,255,255,0.07)",
        borderColor: durum === "dogru" ? "#2ee59d" : durum === "yanlis" ? "#ff4d6d" : "rgba(255,255,255,0.14)" }}>
        <Text style={{ color: "#fff", fontSize: 26, fontWeight: "800" }}>{yazi}</Text>
      </View>
    </Pressable>
  );
}

// ---------- 🧮 Matematik Yarışı (yaşa göre) ----------
const NESNE = ["🍎", "⭐", "🐟", "🎈", "🍓", "🚗", "🐥", "🌸"];
function matSoru(yas: string) {
  if (yas === "3-6") { const n = 1 + rnd(9), e = NESNE[rnd(NESNE.length)]; return { gorsel: e.repeat(n), soru: "Kaç tane var?", cevap: n }; }
  if (yas === "7-9") {
    if (Math.random() < 0.5) { const a = 2 + rnd(30), b = 1 + rnd(20); return { gorsel: "", soru: `${a} + ${b} = ?`, cevap: a + b }; }
    const a = 10 + rnd(40), b = 1 + rnd(a - 1); return { gorsel: "", soru: `${a} − ${b} = ?`, cevap: a - b };
  }
  if (Math.random() < 0.55) { const a = 2 + rnd(11), b = 2 + rnd(11); return { gorsel: "", soru: `${a} × ${b} = ?`, cevap: a * b }; }
  const b = 2 + rnd(10), c = 2 + rnd(10); return { gorsel: "", soru: `${b * c} ÷ ${b} = ?`, cevap: c };
}
export function MatematikYarisi({ yas }: { yas: string }) {
  const [s, setS] = useState(() => matSoru(yas));
  const [secim, setSecim] = useState<number | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  const secenekler = useMemo(() => karistir(Array.from(new Set([s.cevap, ...[1, -1, 2, -2, 3, 10, -10].map((k) => s.cevap + k)])).filter((x) => x >= 0).slice(0, 4)), [s]);
  useEffect(() => { soyle(s.soru.replace("×", "çarpı").replace("÷", "bölü").replace("−", "eksi").replace("+", "artı").replace("= ?", "kaç eder?")); }, [s]);
  const sec = (x: number) => {
    if (secim !== null) return;
    titret(); setSecim(x);
    const ok = x === s.cevap; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 }));
    soyle(ok ? ["Harika!", "Aferin sana!", "Süpersin!", "Doğru!"][rnd(4)] : `Olsun, doğrusu ${s.cevap}`);
    setTimeout(() => { setSecim(null); setS(matSoru(yas)); }, 1400);
  };
  return (
    <View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#3b2b8f", "#1a1b4b"]}>
        {s.gorsel ? <Text style={{ fontSize: 38, textAlign: "center", lineHeight: 52, marginBottom: 8 }}>{s.gorsel}</Text> : null}
        <Text style={{ color: "#fff", fontSize: s.gorsel ? 22 : 44, fontWeight: "900", textAlign: "center", letterSpacing: 1 }}>{s.soru}</Text>
      </Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {secenekler.map((x) => <Secenek key={x} yazi={String(x)} onPress={() => sec(x)} durum={secim === null ? undefined : x === s.cevap ? "dogru" : x === secim ? "yanlis" : undefined} />)}
      </View>
    </View>
  );
}

// ---------- 🌍 Kelime Avı (çok dilli) ----------
const KELIMELER: [string, Record<string, string>][] = [
  ["🍎", { tr: "elma", en: "apple", ar: "تفاحة", de: "Apfel" }], ["🐱", { tr: "kedi", en: "cat", ar: "قطة", de: "Katze" }],
  ["🐶", { tr: "köpek", en: "dog", ar: "كلب", de: "Hund" }], ["☀️", { tr: "güneş", en: "sun", ar: "شمس", de: "Sonne" }],
  ["🌙", { tr: "ay", en: "moon", ar: "قمر", de: "Mond" }], ["📖", { tr: "kitap", en: "book", ar: "كتاب", de: "Buch" }],
  ["🏠", { tr: "ev", en: "house", ar: "بيت", de: "Haus" }], ["💧", { tr: "su", en: "water", ar: "ماء", de: "Wasser" }],
  ["🌳", { tr: "ağaç", en: "tree", ar: "شجرة", de: "Baum" }], ["🐦", { tr: "kuş", en: "bird", ar: "طائر", de: "Vogel" }],
  ["🚗", { tr: "araba", en: "car", ar: "سيارة", de: "Auto" }], ["⭐", { tr: "yıldız", en: "star", ar: "نجمة", de: "Stern" }],
  ["🍞", { tr: "ekmek", en: "bread", ar: "خبز", de: "Brot" }], ["🌸", { tr: "çiçek", en: "flower", ar: "زهرة", de: "Blume" }],
];
const DILLER_OYUN: [string, string, string][] = [["tr", "🇹🇷 Türkçe", "tr-TR"], ["en", "🇬🇧 English", "en-US"], ["ar", "🇸🇦 العربية", "ar-SA"], ["de", "🇩🇪 Deutsch", "de-DE"]];
export function KelimeAvi() {
  const [dil, setDil] = useState("en");
  const yeni = () => { const d = KELIMELER[rnd(KELIMELER.length)]; return { d, sec: karistir([d, ...karistir(KELIMELER.filter((k) => k !== d)).slice(0, 3)]) }; };
  const [s, setS] = useState(yeni);
  const [secim, setSecim] = useState<string | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  const konus = DILLER_OYUN.find((x) => x[0] === dil)![2];
  const sec = (k: string) => {
    if (secim) return;
    titret(); setSecim(k);
    const ok = k === s.d[1][dil]; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 }));
    soyle(s.d[1][dil], konus);
    setTimeout(() => { setSecim(null); setS(yeni()); }, 1600);
  };
  return (
    <View>
      <View style={{ flexDirection: "row", gap: 6, marginBottom: 10, flexWrap: "wrap" }}>
        {DILLER_OYUN.map(([k, ad]) => (
          <Pressable key={k} onPress={() => { titret(); setDil(k); setSecim(null); setS(yeni()); }} style={{ paddingHorizontal: 12, paddingVertical: 8, borderRadius: 16, backgroundColor: dil === k ? "rgba(162,89,255,0.4)" : "rgba(255,255,255,0.06)", borderWidth: 1, borderColor: dil === k ? "#a259ff" : "rgba(255,255,255,0.12)" }}>
            <Text style={{ color: "#fff", fontWeight: "700", fontSize: 13 }}>{ad}</Text>
          </Pressable>
        ))}
      </View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#0f5d5a", "#14183a"]}>
        <Text style={{ fontSize: 86, textAlign: "center" }}>{s.d[0]}</Text>
        <Text style={{ color: "#c9f5ee", textAlign: "center", fontSize: 15, marginTop: 4 }}>Bu nedir? Doğru kelimeyi seç</Text>
      </Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {s.sec.map((k) => <Secenek key={k[1][dil]} yazi={k[1][dil]} onPress={() => sec(k[1][dil])} durum={!secim ? undefined : k[1][dil] === s.d[1][dil] ? "dogru" : k[1][dil] === secim ? "yanlis" : undefined} />)}
      </View>
    </View>
  );
}

// ---------- 🧠 Hafıza Kartları (yaşa göre çift sayısı) ----------
const HAFIZA_EMOJI = ["🦁", "🐼", "🦊", "🐸", "🐙", "🦋", "🐢", "🦄", "🐳", "🦉"];
export function HafizaKartlari({ yas }: { yas: string }) {
  const cift = yas === "3-6" ? 3 : yas === "7-9" ? 6 : 8;
  const kur = () => karistir([...HAFIZA_EMOJI.slice(0, cift), ...HAFIZA_EMOJI.slice(0, cift)]).map((e, i) => ({ id: i, e }));
  const [kartlar, setKartlar] = useState(kur);
  const [acik, setAcik] = useState<number[]>([]);
  const [bulunan, setBulunan] = useState<string[]>([]);
  const [hamle, setHamle] = useState(0);
  const bitti = bulunan.length === cift;
  const ac = (i: number) => {
    if (acik.length === 2 || acik.includes(i) || bulunan.includes(kartlar[i].e)) return;
    titret();
    const y = [...acik, i]; setAcik(y);
    if (y.length === 2) {
      setHamle((h) => h + 1);
      if (kartlar[y[0]].e === kartlar[y[1]].e) { setBulunan((b) => { const n = [...b, kartlar[i].e]; if (n.length === cift) soyle("Tebrikler, hepsini buldun!"); else soyle("Buldun!"); return n; }); setTimeout(() => setAcik([]), 400); }
      else setTimeout(() => setAcik([]), 900);
    }
  };
  const sutun = cift <= 3 ? 3 : 4;
  return (
    <View>
      <Text style={{ color: "#c9cfee", textAlign: "center", marginBottom: 10 }}>Hamle: {hamle} • Bulunan: {bulunan.length}/{cift}</Text>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
        {kartlar.map((k, i) => {
          const gor = acik.includes(i) || bulunan.includes(k.e);
          return (
            <Pressable key={k.id} onPress={() => ac(i)} style={{ width: `${100 / sutun - 3}%`, aspectRatio: 0.85 }}>
              <LinearGradient colors={gor ? ["#ffffff", "#e9e4ff"] : ["#7c5cff", "#4f8cff"]} style={{ flex: 1, borderRadius: 18, alignItems: "center", justifyContent: "center", borderWidth: bulunan.includes(k.e) ? 2 : 0, borderColor: "#2ee59d" }}>
                <Text style={{ fontSize: gor ? 38 : 26, color: "#fff" }}>{gor ? k.e : "✦"}</Text>
              </LinearGradient>
            </Pressable>
          );
        })}
      </View>
      {bitti ? (
        <Pressable onPress={() => { setKartlar(kur()); setAcik([]); setBulunan([]); setHamle(0); }} style={{ alignSelf: "center", marginTop: 16 }}>
          <LinearGradient colors={["#2ee59d", "#22d3ee"]} style={{ paddingHorizontal: 26, paddingVertical: 13, borderRadius: 22 }}>
            <Text style={{ color: "#06281f", fontWeight: "900" }}>🎉 {hamle} hamlede bitirdin • Tekrar oyna</Text>
          </LinearGradient>
        </Pressable>
      ) : null}
    </View>
  );
}

// ---------- Oyun seçici ----------
export default function CocukOyunlari({ yas }: { yas: string }) {
  const [oyun, setOyun] = useState<"mat" | "kelime" | "hafiza" | null>(null);
  const OYUNLAR: ["mat" | "kelime" | "hafiza", string, string, string, [string, string]][] = [
    ["mat", "🧮", "Matematik Yarışı", yas === "3-6" ? "Saymayı öğren" : yas === "7-9" ? "Toplama • çıkarma" : "Çarpma • bölme", ["#7c5cff", "#4f8cff"]],
    ["kelime", "🌍", "Kelime Avı", "4 dilde kelimeler", ["#11998e", "#38ef7d"]],
    ["hafiza", "🧠", "Hafıza Kartları", "Eşleri bul", ["#f093fb", "#f5576c"]],
  ];
  if (!oyun) return (
    <View style={{ gap: 12 }}>
      {OYUNLAR.map(([k, ikon, ad, alt, renk]) => (
        <Pressable key={k} onPress={() => { titret(); setOyun(k); }} style={({ pressed }) => ({ transform: [{ scale: pressed ? 0.98 : 1 }] })}>
          <LinearGradient colors={renk} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={{ borderRadius: 24, padding: 18, flexDirection: "row", alignItems: "center", gap: 16 }}>
            <Text style={{ fontSize: 44 }}>{ikon}</Text>
            <View style={{ flex: 1 }}>
              <Text style={{ color: "#fff", fontSize: 19, fontWeight: "900" }}>{ad}</Text>
              <Text style={{ color: "rgba(255,255,255,0.85)", fontSize: 13, marginTop: 2 }}>{alt}</Text>
            </View>
            <Text style={{ color: "#fff", fontSize: 22 }}>›</Text>
          </LinearGradient>
        </Pressable>
      ))}
    </View>
  );
  return (
    <View>
      <Pressable onPress={() => { Speech.stop(); setOyun(null); }} style={{ alignSelf: "flex-start", marginBottom: 10, paddingHorizontal: 12, paddingVertical: 6, borderRadius: 14, backgroundColor: "rgba(255,255,255,0.07)" }}>
        <Text style={{ color: "#dfe3ff", fontWeight: "700" }}>‹ Oyunlar</Text>
      </Pressable>
      {oyun === "mat" && <MatematikYarisi yas={yas} />}
      {oyun === "kelime" && <KelimeAvi />}
      {oyun === "hafiza" && <HafizaKartlari yas={yas} />}
    </View>
  );
}
