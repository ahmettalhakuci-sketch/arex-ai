// AREX — 🧭 Araçlar: canlı pano (saat, hava, döviz/altın/kripto, deprem, namaz) + cihaz içi matematik motoru
import React, { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, Pressable, RefreshControl, ScrollView, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { sohbetTamamla } from "../ai";
import { coz, sonucMd } from "../matematik";
import { notKaydet, notlariOku, notuSil, type Not } from "../depo";
import { R } from "../tema";
import { Baslik, Dugme, Girdi, Hap, Kart, MdMetin, s as us } from "../ui";

async function json(url: string, ms = 9000) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  try { const r = await fetch(url, { signal: c.signal }); return r.ok ? await r.json() : null; } catch { return null; } finally { clearTimeout(t); }
}

const HAVA_KOD: Record<number, string> = { 0: "☀️ Açık", 1: "🌤️ Az bulutlu", 2: "⛅ Parçalı bulutlu", 3: "☁️ Kapalı", 45: "🌫️ Sisli", 48: "🌫️ Kırağılı sis",
  51: "🌦️ Hafif çisenti", 53: "🌦️ Çisenti", 55: "🌧️ Yoğun çisenti", 61: "🌧️ Hafif yağmur", 63: "🌧️ Yağmur", 65: "🌧️ Şiddetli yağmur", 71: "🌨️ Hafif kar",
  73: "🌨️ Kar", 75: "❄️ Yoğun kar", 80: "🌦️ Sağanak", 81: "🌧️ Kuvvetli sağanak", 82: "⛈️ Çok kuvvetli sağanak", 95: "⛈️ Gök gürültülü fırtına" };
const SEHIRLER = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Konya", "Trabzon", "Dakka", "Riyad", "Moskova", "Londra"];
const SAAT_DILIMLERI: [string, string][] = [["🇹🇷 İstanbul", "Europe/Istanbul"], ["🇧🇩 Dakka", "Asia/Dhaka"], ["🇸🇦 Mekke", "Asia/Riyadh"], ["🇷🇺 Moskova", "Europe/Moscow"], ["🇬🇧 Londra", "Europe/London"], ["🇺🇸 New York", "America/New_York"], ["🇯🇵 Tokyo", "Asia/Tokyo"]];

export default function AraclarEkrani() {
  const ic = useSafeAreaInsets();
  const [sekme, setSekme] = useState<"pano" | "mat" | "not">("pano");
  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 40 }} keyboardShouldPersistTaps="handled">
      <Baslik alt="Canlı bilgiler ve cihaz içi matematik motoru (açık kaynak & ücretsiz veriler).">🧭 Araçlar</Baslik>
      <View style={{ flexDirection: "row", gap: 8, marginBottom: 12 }}>
        <Hap yazi="📡 Güncel Pano" secili={sekme === "pano"} onPress={() => setSekme("pano")} />
        <Hap yazi="🧮 Matematik" secili={sekme === "mat"} onPress={() => setSekme("mat")} />
        <Hap yazi="📝 Notlarım" secili={sekme === "not"} onPress={() => setSekme("not")} />
      </View>
      {sekme === "pano" ? <Pano /> : sekme === "mat" ? <Matematik /> : <Notlarim />}
    </ScrollView>
  );
}

function Saat() {
  const [simdi, setSimdi] = useState(new Date());
  useEffect(() => { const t = setInterval(() => setSimdi(new Date()), 1000); return () => clearInterval(t); }, []);
  const fmt = (tz: string, o: Intl.DateTimeFormatOptions) => simdi.toLocaleString("tr-TR", { timeZone: tz, ...o });
  return (
    <Kart>
      <Text style={{ color: "#fff", fontSize: 44, fontWeight: "800", fontVariant: ["tabular-nums"], textAlign: "center" }}>{fmt("Europe/Istanbul", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}</Text>
      <Text style={[us.alt, { textAlign: "center" }]}>{fmt("Europe/Istanbul", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</Text>
      <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10, justifyContent: "center" }}>
        {SAAT_DILIMLERI.slice(1).map(([ad, tz]) => (
          <View key={tz} style={{ backgroundColor: R.kart, borderRadius: 12, paddingHorizontal: 10, paddingVertical: 6 }}>
            <Text style={{ color: R.yazi, fontSize: 13 }}>{ad} <Text style={{ fontWeight: "700" }}>{fmt(tz, { hour: "2-digit", minute: "2-digit" })}</Text></Text>
          </View>
        ))}
      </View>
    </Kart>
  );
}

function Pano() {
  const [sehir, setSehir] = useState("İstanbul");
  const [hava, setHava] = useState<any>(null);
  const [kur, setKur] = useState<any>(null);
  const [deprem, setDeprem] = useState<any[]>([]);
  const [namaz, setNamaz] = useState<any>(null);
  const [yuk, setYuk] = useState(false);

  const yenile = useCallback(async () => {
    setYuk(true);
    const g = await json(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(sehir)}&count=1&language=tr`);
    const y = g?.results?.[0];
    const [h, er, altin, kripto, dep, nmz] = await Promise.all([
      y ? json(`https://api.open-meteo.com/v1/forecast?latitude=${y.latitude}&longitude=${y.longitude}&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=4`) : null,
      json("https://open.er-api.com/v6/latest/USD"),
      json("https://api.gold-api.com/price/XAU"),
      json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,try"),
      json("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=35&maxlatitude=43&minlongitude=25&maxlongitude=45&minmagnitude=2.5&orderby=time&limit=6"),
      json(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(sehir)}&country=${encodeURIComponent(y?.country || "Turkey")}&method=13`),
    ]);
    setHava(h && y ? { ...h, ad: y.name, ulke: y.country } : null);
    const usd = er?.rates?.TRY;
    setKur(usd ? {
      usd, eur: usd / er.rates.EUR, gbp: usd / er.rates.GBP, sar: usd / er.rates.SAR, bdt: usd / er.rates.BDT,
      gram: altin?.price ? (altin.price / 31.1035) * usd : null, ons: altin?.price, btc: kripto?.bitcoin?.try, eth: kripto?.ethereum?.try,
    } : null);
    setDeprem(dep?.features || []);
    setNamaz(nmz?.data?.timings || null);
    setYuk(false);
  }, [sehir]);
  useEffect(() => { yenile(); }, [yenile]);
  const tl = (v?: number | null, b = 2) => (v ? v.toLocaleString("tr-TR", { maximumFractionDigits: b, minimumFractionDigits: b }) + " ₺" : "—");

  return (
    <View>
      <Saat />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8, marginBottom: 10 }}>
        {SEHIRLER.map((s) => <Hap key={s} yazi={s} secili={sehir === s} onPress={() => setSehir(s)} />)}
      </ScrollView>
      {yuk ? <ActivityIndicator color={R.acc2} style={{ marginVertical: 10 }} /> : null}
      <Kart>
        <Text style={st.kb}>🌤️ Hava — {hava?.ad || sehir}</Text>
        {hava ? (
          <>
            <Text style={{ color: "#fff", fontSize: 34, fontWeight: "800" }}>{Math.round(hava.current.temperature_2m)}° <Text style={{ fontSize: 16, fontWeight: "500" }}>{HAVA_KOD[hava.current.weather_code] || ""}</Text></Text>
            <Text style={us.alt}>Hissedilen {Math.round(hava.current.apparent_temperature)}° • Nem %{hava.current.relative_humidity_2m} • Rüzgâr {hava.current.wind_speed_10m} km/s</Text>
            <View style={{ flexDirection: "row", justifyContent: "space-between", marginTop: 10 }}>
              {hava.daily.time.map((g: string, i: number) => (
                <View key={g} style={{ alignItems: "center" }}>
                  <Text style={us.alt}>{new Date(g).toLocaleDateString("tr-TR", { weekday: "short" })}</Text>
                  <Text style={{ fontSize: 20 }}>{(HAVA_KOD[hava.daily.weather_code[i]] || "•").split(" ")[0]}</Text>
                  <Text style={{ color: "#fff" }}>{Math.round(hava.daily.temperature_2m_max[i])}° / {Math.round(hava.daily.temperature_2m_min[i])}°</Text>
                  <Text style={{ color: R.acc2, fontSize: 11 }}>☔ %{hava.daily.precipitation_probability_max[i] ?? 0}</Text>
                </View>
              ))}
            </View>
          </>
        ) : <Text style={us.alt}>Hava verisi alınamadı.</Text>}
      </Kart>
      <Kart>
        <Text style={st.kb}>💰 Piyasalar (canlı, açık kaynak)</Text>
        {kur ? (
          <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
            {[["💵 Dolar", tl(kur.usd)], ["💶 Euro", tl(kur.eur)], ["💷 Sterlin", tl(kur.gbp)], ["🇸🇦 Riyal", tl(kur.sar)], ["🇧🇩 Taka", tl(kur.bdt, 3)],
              ["🥇 Gram altın", tl(kur.gram)], ["🪙 Ons ($)", kur.ons ? "$" + kur.ons.toFixed(0) : "—"], ["₿ Bitcoin", tl(kur.btc, 0)], ["Ξ Ethereum", tl(kur.eth, 0)]].map(([a, v]) => (
              <View key={a} style={st.hucre}><Text style={us.alt}>{a}</Text><Text style={{ color: "#fff", fontWeight: "700", fontSize: 16 }}>{v}</Text></View>
            ))}
          </View>
        ) : <Text style={us.alt}>Kur verisi alınamadı.</Text>}
        <Text style={{ color: R.soluk, fontSize: 11, marginTop: 6 }}>Gram altın = ons × kur / 31,1 (kuyumcu fiyatı işçilik/makas nedeniyle farklıdır).</Text>
      </Kart>
      {namaz ? (
        <Kart>
          <Text style={st.kb}>🕌 Namaz vakitleri — {sehir}</Text>
          <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
            {[["İmsak", "Fajr"], ["Güneş", "Sunrise"], ["Öğle", "Dhuhr"], ["İkindi", "Asr"], ["Akşam", "Maghrib"], ["Yatsı", "Isha"]].map(([a, k]) => (
              <View key={k} style={st.hucre}><Text style={us.alt}>{a}</Text><Text style={{ color: "#fff", fontWeight: "700" }}>{namaz[k]}</Text></View>
            ))}
          </View>
        </Kart>
      ) : null}
      <Kart>
        <Text style={st.kb}>🌍 Son depremler (Türkiye ve çevresi, M2.5+)</Text>
        {deprem.length ? deprem.map((d) => (
          <Text key={d.id} style={{ color: R.yazi, marginBottom: 4 }}>
            <Text style={{ fontWeight: "800", color: d.properties.mag >= 4 ? R.kirmizi : R.sari }}>M{d.properties.mag.toFixed(1)}</Text> {d.properties.place} • {new Date(d.properties.time).toLocaleString("tr-TR", { hour: "2-digit", minute: "2-digit", day: "numeric", month: "short" })}
          </Text>
        )) : <Text style={us.alt}>Veri alınamadı.</Text>}
      </Kart>
      <Dugme ikincil yazi="🔄 Yenile" onPress={yenile} yukleniyor={yuk} />
    </View>
  );
}

const ORNEKLER = ["türev x^3 + 2x^2", "0'dan 2'ye integral 3x^2+1", "x^3 - 6x^2 + 11x - 6 = 0", "x+y=10, x-y=4", "limit x->0 sin(x)/x", "ortalama 70, 85, 90", "C(10,3)", "5 km to m", "sqrt(144)+5!"];

function Matematik() {
  const [girdi, setGirdi] = useState("");
  const [sonuc, setSonuc] = useState("");
  const [aciklama, setAciklama] = useState("");
  const [bekle, setBekle] = useState(false);
  const hesapla = (m = girdi) => {
    setAciklama("");
    const r = coz(m);
    setSonuc(r ? sonucMd(r) : "🤔 Bunu cihaz içi motor çözemedi. **Yapay zekâya sor** ile adım adım çözüm alabilirsin.");
  };
  const aiSor = async () => {
    setBekle(true);
    const yerel = coz(girdi);
    const r = await sohbetTamamla([{ role: "user", content: `Soru: ${girdi}\n${yerel ? `CİHAZ İÇİ MOTORUN DOĞRULANMIŞ SONUCU: ${yerel.sonuc} — bu sonucu DEĞİŞTİRME, yalnızca nasıl bulunduğunu açıkla.` : "Adım adım çöz."}\n9. sınıf öğrencisine anlatır gibi numaralı adımlarla, sonunda sonucu kalın yaz.` }],
      { sistem: "Sen sabırlı bir matematik öğretmenisin. Hesap hatası yapma; emin değilsen belirt.", sicaklik: 0.2, maks: 1500 });
    setBekle(false);
    setAciklama(r.metin || "Şu an yapay zekâya ulaşılamadı.");
  };
  return (
    <View>
      <Kart>
        <Girdi etiket="İşlem / denklem / soru" value={girdi} onChangeText={setGirdi} placeholder="ör. x^2 - 5x + 6 = 0" onSubmitEditing={() => hesapla()} autoCapitalize="none" />
        <View style={{ flexDirection: "row", gap: 8 }}>
          <Dugme yazi="🧮 Hesapla" onPress={() => hesapla()} style={{ flex: 1 }} />
          <Dugme ikincil yazi="📝 Adım adım (AI)" onPress={aiSor} yukleniyor={bekle} style={{ flex: 1 }} />
        </View>
        <Text style={[us.etiket, { marginTop: 12 }]}>Örnekler</Text>
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 6 }}>
          {ORNEKLER.map((o) => <Pressable key={o} onPress={() => { setGirdi(o); hesapla(o); }} style={st.ornek}><Text style={{ color: R.yazi, fontSize: 13 }}>{o}</Text></Pressable>)}
        </View>
      </Kart>
      {sonuc ? <Kart><MdMetin>{sonuc}</MdMetin></Kart> : null}
      {aciklama ? <Kart><MdMetin>{"#### 📝 Adım adım\n" + aciklama}</MdMetin></Kart> : null}
      <Text style={[us.alt, { fontSize: 12 }]}>💡 Fotoğraftaki soruları çözmek için Sohbet'te 📎 ile fotoğraf ekle; sonuçlar bu motorla otomatik doğrulanır.</Text>
    </View>
  );
}

const st = {
  kb: { color: "#fff", fontWeight: "800" as const, fontSize: 16, marginBottom: 8 },
  hucre: { backgroundColor: "rgba(255,255,255,0.05)", borderRadius: 14, paddingHorizontal: 12, paddingVertical: 8, minWidth: "30%" as const, flexGrow: 1 },
  ornek: { backgroundColor: R.kart, borderWidth: 1, borderColor: R.cizgi, borderRadius: 12, paddingHorizontal: 10, paddingVertical: 6 },
};


function Notlarim() {
  const [liste, setListe] = useState<Not[]>([]);
  const [yeni, setYeni] = useState("");
  const [ara, setAra] = useState("");
  const yenile = () => notlariOku().then((l) => setListe([...l].reverse()));
  useEffect(() => { yenile(); }, []);
  const gorunen = ara ? liste.filter((n) => n.metin.toLocaleLowerCase("tr").includes(ara.toLocaleLowerCase("tr"))) : liste;
  return (
    <View>
      <Kart>
        <Girdi etiket="Yeni not" value={yeni} onChangeText={setYeni} multiline placeholder="Aklındakini yaz… (sohbette 'notlarıma kaydet: …' ya da sesli de olur)" />
        <Dugme yazi="➕ Kaydet" onPress={async () => { if (yeni.trim()) { await notKaydet(yeni, "araçlar"); setYeni(""); yenile(); } }} />
      </Kart>
      <Girdi value={ara} onChangeText={setAra} placeholder="🔎 Notlarda ara…" />
      {!gorunen.length ? <Text style={us.alt}>{ara ? "Eşleşen not yok." : "Henüz not yok."}</Text> : null}
      {gorunen.map((n) => (
        <Kart key={n.no} style={{ paddingVertical: 12 }}>
          <View style={{ flexDirection: "row", gap: 10 }}>
            <Text style={{ color: R.acc2, fontWeight: "800" }}>{n.no}.</Text>
            <View style={{ flex: 1 }}>
              <MdMetin>{n.metin}</MdMetin>
              <Text style={{ color: R.soluk, fontSize: 11, marginTop: 4 }}>🕒 {n.tarih} • {n.kaynak}</Text>
            </View>
            <Pressable hitSlop={8} onPress={async () => { await notuSil(n.no); yenile(); }}><Text style={{ fontSize: 17 }}>🗑️</Text></Pressable>
          </View>
        </Kart>
      ))}
    </View>
  );
}
