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

// ---------- 🎨 Renkler & Şekiller ----------
const RENKLER: [string, string][] = [["kırmızı", "#ff4d4d"], ["mavi", "#3b82f6"], ["sarı", "#facc15"], ["yeşil", "#22c55e"], ["mor", "#a855f7"], ["turuncu", "#f97316"], ["pembe", "#ec4899"]];
const SEKILLER: [string, string][] = [["daire", "●"], ["kare", "■"], ["üçgen", "▲"], ["yıldız", "★"], ["kalp", "♥"]];
export function RenkSekil() {
  const yeni = () => {
    const sec = karistir(RENKLER.flatMap(([rad, r]) => SEKILLER.map(([sad, s]) => ({ rad, r, sad, s })))).slice(0, 4);
    return { sec, hedef: sec[rnd(4)] };
  };
  const [s, setS] = useState(yeni);
  const [secim, setSecim] = useState<number | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  useEffect(() => { soyle(`${s.hedef.rad} ${s.hedef.sad} hangisi?`); }, [s]);
  const sec = (i: number) => {
    if (secim !== null) return; titret(); setSecim(i);
    const ok = s.sec[i] === s.hedef; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 })); soyle(ok ? "Çok güzel!" : "Tekrar bakalım");
    setTimeout(() => { setSecim(null); setS(yeni()); }, 1300);
  };
  return (
    <View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#5b2a86", "#14183a"]}><Text style={{ color: "#fff", fontSize: 26, fontWeight: "900", textAlign: "center" }}>{s.hedef.rad.toLocaleUpperCase("tr")} {s.hedef.sad.toLocaleUpperCase("tr")} hangisi?</Text></Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {s.sec.map((x, i) => (
          <Pressable key={i} onPress={() => sec(i)} style={{ width: "47.5%", aspectRatio: 1.25, borderRadius: 22, alignItems: "center", justifyContent: "center", borderWidth: 2,
            backgroundColor: "rgba(255,255,255,0.06)", borderColor: secim === null ? "rgba(255,255,255,0.12)" : x === s.hedef ? "#2ee59d" : i === secim ? "#ff4d6d" : "rgba(255,255,255,0.12)" }}>
            <Text style={{ fontSize: 70, color: x.r }}>{x.s}</Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}

// ---------- 🔤 Harf Avı (ilk harf) ----------
const HARF_KELIME: [string, string][] = [["🍎", "Elma"], ["🐱", "Kedi"], ["🐶", "Köpek"], ["🌙", "Ay"], ["📖", "Kitap"], ["🏠", "Ev"], ["🌳", "Ağaç"], ["🐦", "Kuş"], ["🚗", "Araba"], ["⭐", "Yıldız"], ["🍞", "Ekmek"], ["🌸", "Çiçek"], ["🐟", "Balık"], ["🦁", "Aslan"], ["🍌", "Muz"], ["🐝", "Arı"], ["🥕", "Havuç"], ["🍉", "Karpuz"], ["⚽", "Top"], ["🐢", "Kaplumbağa"]];
export function HarfAvi() {
  const yeni = () => { const d = HARF_KELIME[rnd(HARF_KELIME.length)]; const dogru = d[1][0]; const harfler = karistir(Array.from(new Set([dogru, ...karistir("ABCÇDEFGHIİKLMNOÖPRSŞTUÜYZ".split("")).filter((h) => h !== dogru).slice(0, 3)]))); return { d, dogru, harfler }; };
  const [s, setS] = useState(yeni);
  const [secim, setSecim] = useState<string | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  useEffect(() => { soyle(`${s.d[1]} hangi harfle başlar?`); }, [s]);
  const sec = (h: string) => {
    if (secim) return; titret(); setSecim(h);
    const ok = h === s.dogru; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 })); soyle(ok ? `Evet! ${s.d[1]}, ${s.dogru} harfiyle başlar` : `${s.d[1]}, ${s.dogru} harfiyle başlar`);
    setTimeout(() => { setSecim(null); setS(yeni()); }, 1700);
  };
  return (
    <View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#8a3c0f", "#14183a"]}>
        <Text style={{ fontSize: 80, textAlign: "center" }}>{s.d[0]}</Text>
        <Text style={{ color: "#ffe2c7", fontSize: 22, fontWeight: "800", textAlign: "center" }}>{secim ? s.d[1] : "_" + s.d[1].slice(1).toLocaleLowerCase("tr")}</Text>
        <Text style={{ color: "#ffd9b8", textAlign: "center", fontSize: 14, marginTop: 4 }}>Hangi harfle başlar?</Text>
      </Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {s.harfler.map((h) => <Secenek key={h} yazi={h} onPress={() => sec(h)} durum={!secim ? undefined : h === s.dogru ? "dogru" : h === secim ? "yanlis" : undefined} />)}
      </View>
    </View>
  );
}

// ---------- 💡 Bil Bakalım (yaşa göre doğru/yanlış) ----------
const BILGILER: Record<string, [string, boolean, string][]> = {
  "3-6": [["Kediler miyavlar.", true, "Evet, kediler miyav der!"], ["Balıklar ağaçta yaşar.", false, "Balıklar suda yaşar."], ["Güneş geceleri parlar.", false, "Geceleri ay ve yıldızlar görünür."], ["İnekler süt verir.", true, "Evet, inekler süt verir."], ["Kar sıcaktır.", false, "Kar soğuktur."], ["Kuşların kanatları vardır.", true, "Evet, kuşlar kanatlarıyla uçar."]],
  "7-9": [["Dünya Güneş'in etrafında döner.", true, "Evet, bir turu yaklaşık 365 günde tamamlar."], ["Örümceklerin 6 bacağı vardır.", false, "Örümceklerin 8 bacağı vardır."], ["Su 100 derecede kaynar.", true, "Evet, deniz seviyesinde 100 °C'de kaynar."], ["Bitkiler güneş ışığıyla besin üretir.", true, "Buna fotosentez denir."], ["Ay kendi ışığını üretir.", false, "Ay, Güneş'in ışığını yansıtır."], ["Bir haftada 8 gün vardır.", false, "Bir haftada 7 gün vardır."]],
  "10-12": [["Işık sesten hızlıdır.", true, "Bu yüzden şimşeği gök gürültüsünden önce görürüz."], ["Yarasa bir kuştur.", false, "Yarasa uçabilen bir memelidir."], ["İnsan vücudunda 206 kemik vardır.", true, "Yetişkinlerde 206 kemik bulunur."], ["Venüs Güneş'e en yakın gezegendir.", false, "Güneş'e en yakın gezegen Merkür'dür."], ["Su molekülü H₂O'dur.", true, "İki hidrojen ve bir oksijen."], ["Kalp vücudun sol tarafındadır, tamamen.", false, "Kalp göğsün ortasında, biraz sola yatıktır."]],
};
export function BilBakalim({ yas }: { yas: string }) {
  const liste = BILGILER[yas] || BILGILER["7-9"];
  const [i, setI] = useState(() => rnd(liste.length));
  const [secim, setSecim] = useState<boolean | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  const [c, dogru, aciklama] = liste[i];
  useEffect(() => { soyle(c + " Doğru mu, yanlış mı?"); }, [i]);
  const sec = (b: boolean) => {
    if (secim !== null) return; titret(); setSecim(b);
    const ok = b === dogru; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 })); soyle((ok ? "Bildin! " : "Aslında… ") + aciklama);
    setTimeout(() => { setSecim(null); setI((x) => (x + 1 + rnd(liste.length - 1)) % liste.length); }, 2600);
  };
  return (
    <View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#0f4c75", "#14183a"]}>
        <Text style={{ color: "#fff", fontSize: 22, fontWeight: "800", textAlign: "center", lineHeight: 31 }}>{c}</Text>
        {secim !== null ? <Text style={{ color: secim === dogru ? "#7cf5c0" : "#ffb3c1", textAlign: "center", marginTop: 10, fontSize: 15 }}>{secim === dogru ? "✅ " : "💡 "}{aciklama}</Text> : null}
      </Kart>
      <View style={{ flexDirection: "row", gap: 10 }}>
        {([[true, "✅ Doğru", "#2ee59d"], [false, "❌ Yanlış", "#ff4d6d"]] as const).map(([b, ad, r]) => (
          <Pressable key={ad} onPress={() => sec(b)} style={{ flex: 1, borderRadius: 20, paddingVertical: 20, alignItems: "center", borderWidth: 2, borderColor: secim !== null && b === dogru ? r : "rgba(255,255,255,0.14)", backgroundColor: r + "22" }}>
            <Text style={{ color: "#fff", fontSize: 20, fontWeight: "900" }}>{ad}</Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}

// ---------- ⚡ Zamana Karşı (gençler): 60 sn, artan zorluk, seri bonusu, en iyi skor ----------
export function ZamanaKarsi() {
  const soru = (seviye: number) => {
    const t = rnd(Math.min(4, 1 + Math.floor(seviye / 3)) + 1);
    const m = 5 + seviye * 3;
    if (t === 0) { const a = 2 + rnd(m), b = 2 + rnd(m); return { q: `${a} + ${b}`, c: a + b }; }
    if (t === 1) { const a = 5 + rnd(m * 2), b = 1 + rnd(a); return { q: `${a} − ${b}`, c: a - b }; }
    if (t === 2) { const a = 2 + rnd(Math.min(12, 3 + seviye)), b = 2 + rnd(12); return { q: `${a} × ${b}`, c: a * b }; }
    if (t === 3) { const b = 2 + rnd(11), c = 2 + rnd(12); return { q: `${b * c} ÷ ${b}`, c }; }
    const a = 2 + rnd(9), b = 2 + rnd(9), c = 1 + rnd(20); return { q: `${a} × ${b} + ${c}`, c: a * b + c };
  };
  const [oyun, setOyun] = useState<"bekle" | "oyna" | "bitti">("bekle");
  const [kalan, setKalan] = useState(60);
  const [puan, setPuan] = useState(0);
  const [seri, setSeri] = useState(0);
  const [s, setS] = useState(() => soru(0));
  const [rekor, setRekor] = useState(0);
  const [isik, setIsik] = useState<"" | "d" | "y">("");
  useEffect(() => { import("../depo").then((d) => d.oku<number>("arex_oyun_rekor", 0).then(setRekor)); }, []);
  useEffect(() => {
    if (oyun !== "oyna") return;
    const t = setInterval(() => setKalan((k) => { if (k <= 1) { clearInterval(t); setOyun("bitti"); return 0; } return k - 1; }), 1000);
    return () => clearInterval(t);
  }, [oyun]);
  useEffect(() => { if (oyun === "bitti" && puan > rekor) { setRekor(puan); import("../depo").then((d) => d.yaz("arex_oyun_rekor", puan)); soyle("Yeni rekor!"); } }, [oyun]);
  const secenekler = useMemo(() => karistir(Array.from(new Set([s.c, s.c + 1, s.c - 1, s.c + 10, s.c - 2, s.c + 3].filter((x) => x >= 0))).slice(0, 4)), [s]);
  const sec = (x: number) => {
    titret();
    if (x === s.c) { const yeniSeri = seri + 1; setSeri(yeniSeri); setPuan((p) => p + 10 + Math.min(20, yeniSeri * 2)); setIsik("d"); }
    else { setSeri(0); setIsik("y"); }
    setTimeout(() => setIsik(""), 250);
    setS(soru(Math.floor(puan / 40)));
  };
  if (oyun !== "oyna") return (
    <Kart renk={["#3a1c71", "#14183a"]}>
      <Text style={{ color: "#fff", fontSize: 24, fontWeight: "900", textAlign: "center" }}>⚡ Zamana Karşı</Text>
      <Text style={{ color: "#c9cfee", textAlign: "center", marginTop: 6 }}>60 saniye • doğru üst üste gelirse seri bonusu • zorluk artar</Text>
      {oyun === "bitti" ? <Text style={{ color: "#ffd166", fontSize: 30, fontWeight: "900", textAlign: "center", marginTop: 14 }}>{puan} puan</Text> : null}
      <Text style={{ color: "#9aa3c7", textAlign: "center", marginTop: 6 }}>🏆 En iyi: {rekor}</Text>
      <Pressable onPress={() => { titret(); setPuan(0); setSeri(0); setKalan(60); setS(soru(0)); setOyun("oyna"); }} style={{ alignSelf: "center", marginTop: 16 }}>
        <LinearGradient colors={["#7c5cff", "#ff5fa2"]} style={{ paddingHorizontal: 34, paddingVertical: 14, borderRadius: 24 }}><Text style={{ color: "#fff", fontWeight: "900", fontSize: 16 }}>{oyun === "bitti" ? "Tekrar" : "Başla"}</Text></LinearGradient>
      </Pressable>
    </Kart>
  );
  return (
    <View>
      <View style={{ flexDirection: "row", justifyContent: "space-between", marginBottom: 8 }}>
        <Text style={{ color: kalan <= 10 ? "#ff4d6d" : "#fff", fontSize: 20, fontWeight: "900" }}>⏱ {kalan}</Text>
        <Text style={{ color: "#ffd166", fontSize: 20, fontWeight: "900" }}>{puan}</Text>
        <Text style={{ color: "#7cf5c0", fontSize: 16, fontWeight: "800" }}>🔥 x{seri}</Text>
      </View>
      <View style={{ height: 6, borderRadius: 3, backgroundColor: "rgba(255,255,255,0.08)", marginBottom: 12, overflow: "hidden" }}>
        <View style={{ width: `${(kalan / 60) * 100}%`, height: "100%", backgroundColor: kalan <= 10 ? "#ff4d6d" : "#7c5cff" }} />
      </View>
      <Kart renk={isik === "d" ? ["#0f6b4f", "#14183a"] : isik === "y" ? ["#7a1f33", "#14183a"] : ["#2a1f5c", "#14183a"]}>
        <Text style={{ color: "#fff", fontSize: 44, fontWeight: "900", textAlign: "center" }}>{s.q}</Text>
      </Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {secenekler.map((x) => <Secenek key={x} yazi={String(x)} onPress={() => sec(x)} />)}
      </View>
    </View>
  );
}

// ---------- 🌍 Başkentler Yarışı ----------
const ULKELER: [string, string, string][] = [["🇹🇷", "Türkiye", "Ankara"], ["🇫🇷", "Fransa", "Paris"], ["🇩🇪", "Almanya", "Berlin"], ["🇯🇵", "Japonya", "Tokyo"], ["🇮🇹", "İtalya", "Roma"],
  ["🇪🇸", "İspanya", "Madrid"], ["🇬🇧", "Birleşik Krallık", "Londra"], ["🇷🇺", "Rusya", "Moskova"], ["🇨🇳", "Çin", "Pekin"], ["🇪🇬", "Mısır", "Kahire"], ["🇸🇦", "Suudi Arabistan", "Riyad"],
  ["🇦🇿", "Azerbaycan", "Bakü"], ["🇵🇰", "Pakistan", "İslamabad"], ["🇧🇷", "Brezilya", "Brasilia"], ["🇨🇦", "Kanada", "Ottawa"], ["🇦🇺", "Avustralya", "Kanberra"], ["🇮🇩", "Endonezya", "Cakarta"],
  ["🇲🇾", "Malezya", "Kuala Lumpur"], ["🇶🇦", "Katar", "Doha"], ["🇰🇿", "Kazakistan", "Astana"], ["🇺🇸", "ABD", "Washington"], ["🇬🇷", "Yunanistan", "Atina"], ["🇳🇱", "Hollanda", "Amsterdam"], ["🇲🇦", "Fas", "Rabat"]];
export function Baskentler() {
  const yeni = () => { const d = ULKELER[rnd(ULKELER.length)]; return { d, sec: karistir([d[2], ...karistir(ULKELER.filter((u) => u !== d)).slice(0, 3).map((u) => u[2])]) }; };
  const [s, setS] = useState(yeni);
  const [secim, setSecim] = useState<string | null>(null);
  const [puan, setPuan] = useState({ d: 0, t: 0 });
  const sec = (x: string) => {
    if (secim) return; titret(); setSecim(x);
    const ok = x === s.d[2]; setPuan((p) => ({ d: p.d + (ok ? 1 : 0), t: p.t + 1 })); soyle(ok ? "Doğru!" : `${s.d[1]}'nin başkenti ${s.d[2]}`);
    setTimeout(() => { setSecim(null); setS(yeni()); }, 1400);
  };
  return (
    <View>
      <Puan dogru={puan.d} toplam={puan.t} />
      <Kart renk={["#134e5e", "#14183a"]}>
        <Text style={{ fontSize: 80, textAlign: "center" }}>{s.d[0]}</Text>
        <Text style={{ color: "#fff", fontSize: 22, fontWeight: "900", textAlign: "center" }}>{s.d[1]}</Text>
        <Text style={{ color: "#b8f1e6", textAlign: "center", marginTop: 2 }}>Başkenti neresi?</Text>
      </Kart>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "space-between" }}>
        {s.sec.map((x) => <Secenek key={x} yazi={x} onPress={() => sec(x)} durum={!secim ? undefined : x === s.d[2] ? "dogru" : x === secim ? "yanlis" : undefined} />)}
      </View>
    </View>
  );
}

// ---------- 🔀 Kelime Bulmaca (karışık harfler) ----------
const BULMACA = ["KİTAP", "OKUL", "BULUT", "DENİZ", "KALEM", "YILDIZ", "GEZEGEN", "BİLGİ", "MÜZİK", "ÇİÇEK", "GÜNEŞ", "SABAH", "ROBOT", "DÜNYA", "KÖPRÜ", "ORMAN", "UÇAK", "YAZILIM"];
export function KelimeBulmaca() {
  const yeni = () => { const k = BULMACA[rnd(BULMACA.length)]; let h = karistir(k.split("")); if (h.join("") === k) h = h.reverse(); return { k, h: h.map((c, i) => ({ c, i })) }; };
  const [s, setS] = useState(yeni);
  const [secilen, setSecilen] = useState<number[]>([]);
  const [puan, setPuan] = useState(0);
  const kelime = secilen.map((i) => s.h.find((x) => x.i === i)!.c).join("");
  useEffect(() => {
    if (kelime.length !== s.k.length) return;
    if (kelime === s.k) { setPuan((p) => p + 1); soyle("Harika! " + s.k.toLocaleLowerCase("tr")); setTimeout(() => { setSecilen([]); setS(yeni()); }, 1100); }
    else { soyle("Olmadı, tekrar dene"); setTimeout(() => setSecilen([]), 700); }
  }, [kelime]);
  return (
    <View>
      <Text style={{ color: "#ffd166", fontSize: 18, fontWeight: "800", textAlign: "center", marginBottom: 10 }}>⭐ {puan}</Text>
      <Kart renk={["#4a1d5c", "#14183a"]}>
        <View style={{ flexDirection: "row", justifyContent: "center", gap: 6, flexWrap: "wrap", minHeight: 52 }}>
          {Array.from({ length: s.k.length }, (_, i) => (
            <View key={i} style={{ width: 38, height: 46, borderRadius: 10, borderBottomWidth: 3, borderColor: "#c9a7ff", alignItems: "center", justifyContent: "center", backgroundColor: "rgba(255,255,255,0.05)" }}>
              <Text style={{ color: "#fff", fontSize: 24, fontWeight: "900" }}>{kelime[i] || ""}</Text>
            </View>
          ))}
        </View>
        <Text style={{ color: "#d9c9f5", textAlign: "center", marginTop: 8 }}>İpucu: {s.k[0]} ile başlar • {s.k.length} harf</Text>
      </Kart>
      <View style={{ flexDirection: "row", justifyContent: "center", gap: 8, flexWrap: "wrap" }}>
        {s.h.map((x) => {
          const kullanildi = secilen.includes(x.i);
          return (
            <Pressable key={x.i} disabled={kullanildi} onPress={() => { titret(); setSecilen([...secilen, x.i]); }} style={{ width: 52, height: 56, borderRadius: 14, alignItems: "center", justifyContent: "center", backgroundColor: kullanildi ? "rgba(255,255,255,0.04)" : "rgba(162,89,255,0.35)", borderWidth: 1, borderColor: "rgba(255,255,255,0.15)" }}>
              <Text style={{ color: kullanildi ? "#555b7a" : "#fff", fontSize: 24, fontWeight: "900" }}>{x.c}</Text>
            </Pressable>
          );
        })}
      </View>
      <Pressable onPress={() => setSecilen(secilen.slice(0, -1))} style={{ alignSelf: "center", marginTop: 12, paddingHorizontal: 16, paddingVertical: 8, borderRadius: 14, backgroundColor: "rgba(255,255,255,0.07)" }}>
        <Text style={{ color: "#dfe3ff", fontWeight: "700" }}>⌫ Geri al</Text>
      </Pressable>
    </View>
  );
}

type Oyun = "mat" | "kelime" | "hafiza" | "renk" | "harf" | "bil" | "zaman" | "baskent" | "bulmaca";
// ---------- Oyun seçici ----------
export default function CocukOyunlari({ yas }: { yas: string }) {
  const [oyun, setOyun] = useState<Oyun | null>(null);
  const OYUNLAR: [Oyun, string, string, string, [string, string]][] = [
    ["mat", "🧮", "Matematik Yarışı", yas === "3-6" ? "Saymayı öğren" : yas === "7-9" ? "Toplama • çıkarma" : "Çarpma • bölme", ["#7c5cff", "#4f8cff"]],
    ["kelime", "🌍", "Kelime Avı", "4 dilde kelimeler", ["#11998e", "#38ef7d"]],
    ["hafiza", "🧠", "Hafıza Kartları", "Eşleri bul", ["#f093fb", "#f5576c"]],
    ["renk", "🎨", "Renkler & Şekiller", "Doğru renkli şekli bul", ["#a855f7", "#ec4899"]],
    ["harf", "🔤", "Harf Avı", "Kelimenin ilk harfi", ["#f97316", "#facc15"]],
    ["bil", "💡", "Bil Bakalım", "Doğru mu yanlış mı?", ["#0ea5e9", "#22d3ee"]],
    ["zaman", "⚡", "Zamana Karşı", "Gençler • 60 sn, rekorunu kır", ["#3a1c71", "#d76d77"]],
    ["baskent", "🌍", "Başkentler Yarışı", "Gençler • bayraklar ve başkentler", ["#134e5e", "#71b280"]],
    ["bulmaca", "🔀", "Kelime Bulmaca", "Gençler • karışık harfler", ["#4a1d5c", "#c471ed"]],
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
      {oyun === "renk" && <RenkSekil />}
      {oyun === "harf" && <HarfAvi />}
      {oyun === "bil" && <BilBakalim yas={yas} />}
      {oyun === "zaman" && <ZamanaKarsi />}
      {oyun === "baskent" && <Baskentler />}
      {oyun === "bulmaca" && <KelimeBulmaca />}
    </View>
  );
}
