// AREX — ⚙️ Ayarlar: görünüm/tema, sohbet, ses, API anahtarları, beni tanı (profil & hafıza), veriler, hakkında
import * as Clipboard from "expo-clipboard";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect, useState } from "react";
import { Pressable, ScrollView, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ANLATICILAR, sohbetTamamla, sonHatalar } from "../ai";
import { useAyar } from "../ayar";
import { KULLANIM_MODLARI, SOHBET_TARZLARI } from "../beyin";
import { getRecordingPermissionsAsync, requestRecordingPermissionsAsync } from "expo-audio";
import { Camera } from "expo-camera";
import * as ImagePicker from "expo-image-picker";
import { AppState, Linking, Platform } from "react-native";
import * as Erisim from "../../modules/arex-erisim";
import { izinIste } from "../izin";
import { biyometrikVarMi, kilitAcikMi, pinAyarla } from "../Kilit";
import { guncellemeDenetle, guncellemeyiIndir, mevcutSurum, type Guncelleme } from "../guncelleme";
import { anahtar, ANAHTAR_ADLARI, anahtarKaydet, maskele, profilKaydet, profilOku, sohbetleriOku, type AnahtarAdi, type Profil } from "../depo";
import { DILLER, R, TEMALAR } from "../tema";
import { Anahtar as GorselAnahtar, Baslik, Dugme, Girdi, Kart, s as us, Secici } from "../ui";

function Bolum({ baslik, children, acik: ilk = false }: { baslik: string; children: React.ReactNode; acik?: boolean }) {
  const [acik, setAcik] = useState(ilk);
  return (
    <Kart style={{ paddingVertical: 4 }}>
      <Pressable onPress={() => setAcik(!acik)} style={{ flexDirection: "row", alignItems: "center", paddingVertical: 12 }}>
        <Text style={{ color: "#fff", fontSize: 17, fontWeight: "800", flex: 1 }}>{baslik}</Text>
        <Text style={{ color: R.soluk, fontSize: 18 }}>{acik ? "▾" : "▸"}</Text>
      </Pressable>
      {acik ? <View style={{ paddingBottom: 12 }}>{children}</View> : null}
    </Kart>
  );
}

function Anahtar({ etiket, deger, onChange }: { etiket: string; deger: boolean; onChange: (v: boolean) => void }) {
  return (
    <Pressable onPress={() => onChange(!deger)} style={{ flexDirection: "row", alignItems: "center", paddingVertical: 9, gap: 10 }}>
      <Text style={{ color: R.yazi, fontSize: 15, flex: 1 }}>{etiket}</Text>
      <GorselAnahtar acik={deger} onChange={onChange} />
    </Pressable>
  );
}

/** Android 13+ fotoğraf seçici izin istemez */
const galeriIzinsiz = Platform.OS === "android" && Number(Platform.Version) >= 33;

/** 🔐 İzinler: her iznin durumu + doğrudan o ayar sayfasına giden bağlantı. Uygulamaya dönünce durumlar yenilenir. */
function IzinlerKarti() {
  const [d, setD] = useState(Erisim.durumlar());
  const [mik, setMik] = useState(false);
  const [kam, setKam] = useState(false);
  const yenile = async () => {
    setD(Erisim.durumlar());
    try { setMik((await getRecordingPermissionsAsync()).granted); setKam((await Camera.getCameraPermissionsAsync()).granted); } catch {}
  };
  useEffect(() => {
    yenile();
    const a = AppState.addEventListener("change", (x) => { if (x === "active") yenile(); });
    return () => a.remove();
  }, []);
  if (Platform.OS !== "android" || !Erisim.destekVar()) return null;
  const satirlar: { ad: string; alt: string; ok: boolean | null; ac: () => void }[] = [
    { ad: "♿ Telefon erişimi", alt: "Ekranı oku, dokun, yaz, kaydır", ok: d.erisim, ac: () => Erisim.ayarAc("erisim") },
    { ad: "🔓 Kısıtlanmış ayarlar", alt: "Erişim gri/kapanıyorsa: ⋮ → Kısıtlanmış ayarlara izin ver", ok: d.erisim ? true : null, ac: () => Erisim.ayarAc("uygulama") },
    { ad: "🎙️ Mikrofon", alt: "Sesli soru ve Canlı sohbet", ok: mik, ac: async () => { await izinIste("Mikrofon", requestRecordingPermissionsAsync); yenile(); } },
    { ad: "📷 Kamera", alt: "Canlı görüntü ve fotoğraf analizi", ok: kam, ac: async () => { await izinIste("Kamera", Camera.requestCameraPermissionsAsync); yenile(); } },
    { ad: "✨ Yan tuş asistanı", alt: "Dijital asistan uygulaması → AREX AI", ok: d.asistanBiliniyor ? d.asistan : null, ac: () => Erisim.ayarAc("asistan") },
    { ad: "🔋 Pil kısıtlaması yok", alt: "Ekran kapalıyken tilavet kesilmesin", ok: d.pil, ac: () => Erisim.ayarAc("pil") },
    { ad: "🔔 Bildirimler", alt: "Hatırlatıcı ve pomodoro uyarıları", ok: null, ac: () => Erisim.ayarAc("bildirim") },
    { ad: "🛡️ Güvenlik (Otomatik Engelleyici)", alt: "Kurulum/erişim engelleniyorsa", ok: null, ac: () => Erisim.ayarAc("guvenlik") },
  ];
  const tamam = satirlar.filter((x) => x.ok === true).length;
  const bilinen = satirlar.filter((x) => x.ok !== null).length;
  return (
    <Kart style={{ borderColor: R.acc + "88" }}>
      <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 4 }}>
        <Text style={{ color: "#fff", fontSize: 18, fontWeight: "800", flex: 1 }}>🔐 İzinler</Text>
        <Text style={{ color: tamam === bilinen ? R.yesil : R.sari, fontWeight: "800" }}>{tamam}/{bilinen} hazır</Text>
      </View>
      <Text style={[us.alt, { marginBottom: 6, fontSize: 12.5 }]}>Bağlantıya dokun → doğrudan o ayar sayfası açılır. Geri dönünce durum kendiliğinden güncellenir.</Text>
      {satirlar.map((x) => (
        <Pressable key={x.ad} onPress={x.ac} style={({ pressed }) => ({ flexDirection: "row", alignItems: "center", gap: 10, paddingVertical: 10, borderTopWidth: 1, borderTopColor: R.cizgi, opacity: pressed ? 0.6 : 1 })}>
          <View style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: x.ok === true ? R.yesil : x.ok === false ? R.kirmizi : R.soluk }} />
          <View style={{ flex: 1 }}>
            <Text style={{ color: "#fff", fontWeight: "700", fontSize: 14.5 }}>{x.ad}</Text>
            <Text style={{ color: R.soluk, fontSize: 11.5 }}>{x.alt}</Text>
          </View>
          <Text style={{ color: x.ok === true ? R.yesil : R.acc2, fontWeight: "800", fontSize: 13, textDecorationLine: x.ok === true ? "none" : "underline" }}>{x.ok === true ? "✓ Açık" : "Aç ›"}</Text>
        </Pressable>
      ))}
    </Kart>
  );
}

/** ♿ Telefon erişimi (Erişilebilirlik Servisi): durum + aç düğmesi; uygulamaya dönünce durumu yeniler */
function TelefonErisimi() {
  const [acik, setAcik] = useState(Erisim.etkinMi());
  useEffect(() => {
    const a = AppState.addEventListener("change", (d) => { if (d === "active") setAcik(Erisim.etkinMi()); });
    return () => a.remove();
  }, []);
  if (Platform.OS !== "android" || !Erisim.destekVar()) return null;
  return (
    <View>
      <View style={{ flexDirection: "row", alignItems: "center", gap: 10, marginBottom: 6 }}>
        <Text style={[us.etiket, { flex: 1, marginBottom: 0 }]}>📱 Telefon erişimi (tam asistan)</Text>
        <View style={{ paddingHorizontal: 10, paddingVertical: 4, borderRadius: 999, backgroundColor: acik ? R.yesil + "33" : R.kirmizi + "33", borderWidth: 1, borderColor: acik ? R.yesil : R.kirmizi }}>
          <Text style={{ color: acik ? R.yesil : R.kirmizi, fontWeight: "800", fontSize: 12 }}>{acik ? "● AÇIK" : "● KAPALI"}</Text>
        </View>
      </View>
      <Text style={[us.alt, { marginBottom: 8 }]}>Açınca AREX senin komutunla ekranı okur/özetler, düğmelere dokunur, yazar, kaydırır; geri, ana ekran, bildirimler, kilitle ve uygulama açma yapar. Ekran içeriğini kaydetmez; yalnız "ekranı özetle" dediğinde yapay zekâya gönderir.</Text>
      <Text style={[us.alt, { marginBottom: 10, fontSize: 12.5 }]}>Örnekler: "ekranı özetle" • "Gönder'e dokun" • "yaz: geliyorum" • "aşağı kaydır" • "geri" • "ana ekran" • "bildirimleri aç" • "google aç" • "telefonu kilitle"</Text>
      <Dugme ikincil={acik} yazi={acik ? "⚙️ Erişim ayarlarını aç" : "♿ Erişimi aç"} onPress={() => Erisim.ayarlariAc()} />
      {!acik ? <Text style={[us.alt, { fontSize: 12, marginTop: 8 }]}>Açılan ekranda: Yüklü uygulamalar → <Text style={{ color: "#fff", fontWeight: "700" }}>AREX AI Asistan</Text> → Aç. (Samsung "kısıtlanmış ayar" derse: Ayarlar → Uygulamalar → AREX AI → ⋮ → Kısıtlanmış ayarlara izin ver.)</Text> : null}
    </View>
  );
}

export default function AyarlarEkrani() {
  const ic = useSafeAreaInsets();
  const { ayar, guncelle } = useAyar();
  const [, yeniden] = useState(0);
  const [anahtarGirdi, setAnahtarGirdi] = useState<Record<string, string>>({});
  const [test, setTest] = useState("");
  const [testBekle, setTestBekle] = useState(false);
  const [profil, setProfil] = useState<Profil | null>(null);
  const [kayitMesaj, setKayitMesaj] = useState("");
  useEffect(() => { profilOku().then(setProfil); }, []);

  const anahtarlariKaydet = async () => {
    for (const [ad, v] of Object.entries(anahtarGirdi)) if (v.trim()) await anahtarKaydet(ad as AnahtarAdi, v);
    setAnahtarGirdi({}); yeniden((x) => x + 1); setKayitMesaj("✅ Anahtarlar güvenli depoya kaydedildi.");
  };
  const baglantiTesti = async () => {
    setTestBekle(true); setTest("");
    const r = await sohbetTamamla([{ role: "user", content: "Tek kelimeyle: merhaba" }], { maks: 20 });
    setTestBekle(false);
    setTest((r.metin ? `✅ Bağlantı çalışıyor — ${r.motor}` : "❌ Hiçbir sağlayıcıya ulaşılamadı") + "\n" + Object.entries(sonHatalar).map(([k, v]) => `• ${k}: ${v}`).join("\n"));
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 14, paddingTop: ic.top + 10, paddingBottom: 50 }} keyboardShouldPersistTaps="handled">
      <Baslik alt="Görünüm, sohbet, ses, anahtarlar ve kişisel hafıza.">⚙️ Ayarlar</Baslik>
      <IzinlerKarti />

      <Bolum baslik="👤 Kullanım modu" acik>
        <Text style={[us.alt, { marginBottom: 8 }]}>Kişisel modda AREX seni tanır (profil, hafıza, notlar). Başkalarına tanıtırken 🌐 Misafir modunu seç: kişisel bilgilerin gizlenir.</Text>
        <Secici deger={ayar.kullanimModu || "kisisel"} onChange={(v) => guncelle({ kullanimModu: v, cocukModu: v === "cocuk" })}
          secenekler={Object.entries(KULLANIM_MODLARI).map(([k, v]) => ({ k, ad: v }))} />
        <Anahtar etiket="👁️ Göz koruma (sıcak, yumuşak ton)" deger={!!ayar.gozKoruma} onChange={(v) => guncelle({ gozKoruma: v })} />
      </Bolum>

      <Bolum baslik="🎭 Sohbet tarzı">
        <Text style={[us.alt, { marginBottom: 8 }]}>Sohbette "mizah modu aç", "içten sohbet modu", "mümin modu", "normal moda dön" diyerek de değiştirebilirsin.</Text>
        <Secici deger={ayar.sohbetTarzi || "dengeli"} onChange={(v) => guncelle({ sohbetTarzi: v })}
          secenekler={Object.entries(SOHBET_TARZLARI).map(([k, v]) => ({ k, ad: v.ad }))} />
      </Bolum>

      <GuvenlikBolumu Bolum={Bolum} Anahtar={Anahtar} />

      <Bolum baslik="🎨 Görünüm & tema" acik>
        <Text style={us.etiket}>Renk teması</Text>
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
          {Object.entries(TEMALAR).map(([k, t]) => (
            <Pressable key={k} onPress={() => guncelle({ tema: k })} style={{ width: "47%", borderRadius: 18, overflow: "hidden", borderWidth: 2, borderColor: ayar.tema === k ? "#fff" : "transparent" }}>
              <LinearGradient colors={t.arka} style={{ padding: 12, height: 86, justifyContent: "space-between" }}>
                <View style={{ flexDirection: "row", gap: 6 }}>
                  <View style={{ width: 22, height: 22, borderRadius: 11, backgroundColor: t.acc }} />
                  <View style={{ width: 22, height: 22, borderRadius: 11, backgroundColor: t.acc2 }} />
                  <View style={{ flex: 1, height: 22, borderRadius: 11, backgroundColor: t.balon }} />
                </View>
                <Text style={{ color: "#fff", fontWeight: "700" }}>{t.ad}{ayar.tema === k ? "  ✓" : ""}</Text>
              </LinearGradient>
            </Pressable>
          ))}
        </View>
        <View style={{ height: 12 }} />
        <Secici etiket="Yazı boyutu" deger={String(ayar.yaziOlcek)} onChange={(v) => guncelle({ yaziOlcek: Number(v) })}
          secenekler={[{ k: "0.9", ad: "A- Küçük" }, { k: "1", ad: "A Normal" }, { k: "1.15", ad: "A+ Büyük" }]} />
      </Bolum>

      <Bolum baslik="💬 Sohbet">
        <Secici etiket="Varsayılan yanıt dili (başka dilde yazarsan o dilde cevaplar)" deger={ayar.yanitDili} onChange={(v) => guncelle({ yanitDili: v })}
          secenekler={Object.entries(DILLER).map(([k, v]) => ({ k, ad: `${v.bayrak} ${v.ad}` }))} />
        <Secici etiket="Yaratıcılık" deger={String(ayar.yaraticilik)} onChange={(v) => guncelle({ yaraticilik: Number(v) })}
          secenekler={[{ k: "0.4", ad: "🎯 Net & dengeli" }, { k: "0.75", ad: "✨ Yaratıcı" }, { k: "0.95", ad: "🎨 Çok yaratıcı" }]} />
        <Anahtar etiket="🧸 Çocuk modu (güvenli, yaşa uygun dil)" deger={ayar.cocukModu} onChange={(v) => guncelle({ cocukModu: v })} />
        {ayar.cocukModu ? <Secici etiket="Yaş grubu" deger={ayar.yas} onChange={(v) => guncelle({ yas: v })} secenekler={[{ k: "3-6", ad: "🐣 3-6" }, { k: "7-9", ad: "🦊 7-9" }, { k: "10-12", ad: "🚀 10-12" }]} /> : null}
      </Bolum>

      <Bolum baslik="🔊 Ses">
        <Anahtar etiket="🎙️ Doğal anlatıcı sesi (Gemini)" deger={ayar.dogalSes} onChange={(v) => guncelle({ dogalSes: v })} />
        <Anahtar etiket="🔁 Cevapları otomatik sesli oku" deger={ayar.otomatikSes} onChange={(v) => guncelle({ otomatikSes: v })} />
        <Secici etiket="Anlatıcı" deger={ayar.anlatici} onChange={(v) => guncelle({ anlatici: v })} secenekler={Object.entries(ANLATICILAR).map(([k, v]) => ({ k, ad: v.ad }))} />
      </Bolum>

      <Bolum baslik="🔑 API anahtarları">
        <Text style={[us.alt, { marginBottom: 10 }]}>Anahtarlar cihazın güvenli deposunda saklanır; güncelleme veya yeniden başlatma silmez. Boş bırakılan alan mevcut anahtarı değiştirmez.</Text>
        {(Object.keys(ANAHTAR_ADLARI) as AnahtarAdi[]).map((ad) => (
          <Girdi key={ad} etiket={`${ANAHTAR_ADLARI[ad]}  ${anahtar(ad) ? "🟢 " + maskele(anahtar(ad)) : "⚪ yok"}`} value={anahtarGirdi[ad] || ""} secureTextEntry autoCapitalize="none"
            onChangeText={(v) => setAnahtarGirdi({ ...anahtarGirdi, [ad]: v })} placeholder="yeni anahtar yapıştır" />
        ))}
        <View style={{ flexDirection: "row", gap: 8 }}>
          <Dugme yazi="💾 Kaydet" onPress={anahtarlariKaydet} style={{ flex: 1 }} />
          <Dugme ikincil yazi="🩺 Bağlantı testi" onPress={baglantiTesti} yukleniyor={testBekle} style={{ flex: 1 }} />
        </View>
        {kayitMesaj ? <Text style={{ color: R.yesil, marginTop: 8 }}>{kayitMesaj}</Text> : null}
        {test ? <Text style={{ color: R.yazi, marginTop: 8, fontSize: 13 }}>{test}</Text> : null}
      </Bolum>

      <Bolum baslik="🧠 Beni tanı (kişisel hafıza)">
        {profil ? (
          <>
            {([["ad", "👤 Adın"], ["hakkinda", "📝 Kendinden bahset"], ["ilgi", "💡 İlgi alanların"], ["hedef", "🎯 Hedeflerin"], ["tarz", "🗣️ Nasıl cevap vereyim?"], ["diller", "🌍 Dillerin"]] as [keyof Profil, string][]).map(([k, e]) => (
              <Girdi key={k} etiket={e} value={String(profil[k] || "")} multiline={k === "hakkinda"} onChangeText={(v) => setProfil({ ...profil, [k]: v })} />
            ))}
            <Dugme yazi="💾 Profili kaydet" onPress={async () => { await profilKaydet(profil); setKayitMesaj("✅ Profil kaydedildi — AREX seni artık daha iyi tanıyor."); }} />
            <Text style={[us.etiket, { marginTop: 14 }]}>📌 Sohbetten öğrendiklerim (sohbette "hatırla: …" yazarak ekleyebilirsin)</Text>
            {!profil.notlar.length ? <Text style={us.alt}>Henüz not yok.</Text> : profil.notlar.map((n, i) => (
              <View key={i} style={{ flexDirection: "row", alignItems: "center", paddingVertical: 6 }}>
                <Text style={{ color: R.yazi, flex: 1 }}>• {n.metin} <Text style={{ color: R.soluk, fontSize: 11 }}>({n.tarih})</Text></Text>
                <Pressable hitSlop={8} onPress={async () => { const p = { ...profil, notlar: profil.notlar.filter((_, j) => j !== i) }; setProfil(p); await profilKaydet(p); }}><Text>🗑️</Text></Pressable>
              </View>
            ))}
          </>
        ) : null}
      </Bolum>

      <Bolum baslik="🗂️ Veriler">
        <Dugme ikincil yazi="📋 Tüm sohbetleri panoya kopyala (Markdown)" onPress={async () => {
          const l = await sohbetleriOku();
          await Clipboard.setStringAsync(l.map((s) => `# ${s.baslik}\n\n` + s.mesajlar.map((m) => `**${m.rol === "user" ? "Sen" : "AREX"}:** ${m.metin}`).join("\n\n")).join("\n\n---\n\n"));
          setKayitMesaj(`✅ ${l.length} sohbet panoya kopyalandı.`);
        }} />
      </Bolum>

      <GuncellemeBolumu Bolum={Bolum} />

      <Bolum baslik="ℹ️ Hakkında">
        <Text style={us.alt}>AREX AI v15 • Groq + Gemini + OpenRouter (ücretsiz katmanlar) • Gemini Live canlı ses • MediaPipe cihaz içi yüz analizi • mathjs cihaz içi matematik • Project Gutenberg klasik masallar • Open-Meteo, AlAdhan, USGS, CoinGecko açık verileri.</Text>
      </Bolum>
    </ScrollView>
  );
}


function GuvenlikBolumu({ Bolum, Anahtar }: { Bolum: any; Anahtar: any }) {
  const [izin, setIzin] = useState<Record<string, boolean | null>>({ mikrofon: null, kamera: null, galeri: null });
  const [kilit, setKilit] = useState(false);
  const [bio, setBio] = useState(false);
  const [yeniPin, setYeniPin] = useState("");
  const [mesaj, setMesaj] = useState("");
  const yenile = async () => {
    if (Platform.OS === "web") { setIzin({ mikrofon: true, kamera: true, galeri: true }); }
    else {
      const [m, k, g] = await Promise.all([getRecordingPermissionsAsync(), Camera.getCameraPermissionsAsync(), ImagePicker.getMediaLibraryPermissionsAsync()]);
      // Android 13+ (S25 FE): galeri Android'in kendi fotoğraf seçicisiyle izinsiz çalışır; READ_MEDIA izni uygulamada yok,
      // bu yüzden "İzin ver" asla sonuç vermezdi → gerekmez olarak göster
      setIzin({ mikrofon: m.granted, kamera: k.granted, galeri: galeriIzinsiz || g.granted });
    }
    setKilit(await kilitAcikMi()); setBio(await biyometrikVarMi());
  };
  useEffect(() => { yenile(); }, []);
  const iste = async (k: string) => {
    if (k === "mikrofon") await izinIste("Mikrofon", requestRecordingPermissionsAsync);
    if (k === "kamera") await izinIste("Kamera", Camera.requestCameraPermissionsAsync);
    if (k === "galeri" && !galeriIzinsiz) await izinIste("Fotoğraflar", () => ImagePicker.requestMediaLibraryPermissionsAsync());
    yenile();
  };
  const IZINLER: [string, string, string][] = [["mikrofon", "🎙️ Mikrofon", "Sesli yazma ve canlı sohbet"], ["kamera", "📷 Kamera", "Fotoğraf, canlı görüntü, yüz analizi"], ["galeri", "🖼️ Fotoğraflar", "Galeriden fotoğraf/video analizi"]];
  return (
    <Bolum baslik="🔐 Güvenlik & izinler">
      <Text style={us.etiket}>İzinler</Text>
      {IZINLER.map(([k, ad, a]) => (
        <View key={k} style={{ flexDirection: "row", alignItems: "center", paddingVertical: 8, gap: 10 }}>
          <View style={{ flex: 1 }}>
            <Text style={{ color: R.yazi, fontSize: 15 }}>{ad}</Text>
            <Text style={{ color: R.soluk, fontSize: 12 }}>{a}</Text>
          </View>
          {izin[k] ? <Text style={{ color: R.yesil, fontWeight: "700" }}>{k === "galeri" && galeriIzinsiz ? "✓ İzin gerekmez" : "✓ Açık"}</Text> : <Dugme kucuk yazi="İzin ver" onPress={() => iste(k)} />}
        </View>
      ))}
      {Platform.OS !== "web" ? <Dugme kucuk ikincil yazi="⚙️ Telefon ayarlarında AREX izinlerini aç" onPress={() => Linking.openSettings()} style={{ marginTop: 6 }} /> : null}
      {Platform.OS === "android" ? (
        <View style={{ marginTop: 12 }}>
          <Text style={us.etiket}>🤖 Yan tuş asistanı</Text>
          <Text style={[us.alt, { marginBottom: 8 }]}>"Dijital asistan uygulaması" olarak AREX AI'ı seç; yan tuşa (ya da ana ekran tuşuna) basılı tutunca AREX altta açılıp dinlemeye başlar. Bazı telefonlarda ayrıca "Yan tuş → Basılı tut → Dijital asistan" ayarı açılmalıdır.</Text>
          <Dugme kucuk yazi="AREX'i varsayılan asistan yap" onPress={() => Linking.sendIntent("android.settings.VOICE_INPUT_SETTINGS").catch(() => Linking.sendIntent("android.settings.MANAGE_DEFAULT_APPS_SETTINGS").catch(() => Linking.openSettings()))} />
        </View>
      ) : null}
      <View style={{ height: 1, backgroundColor: R.cizgi, marginVertical: 14 }} />
      <TelefonErisimi />
      <View style={{ height: 1, backgroundColor: R.cizgi, marginVertical: 14 }} />
      <Text style={us.etiket}>Uygulama kilidi {kilit ? "🔒 açık" : "🔓 kapalı"}</Text>
      <Text style={[us.alt, { marginBottom: 8 }]}>Açılışta PIN{bio ? " ya da parmak izi / yüz tanıma" : ""} ister; AREX yalnızca sana özel kalır. API anahtarların uygulamada hiçbir yerde açık gösterilmez.</Text>
      <Girdi value={yeniPin} onChangeText={(v) => setYeniPin(v.replace(/\D/g, "").slice(0, 6))} placeholder="4-6 haneli PIN" keyboardType="number-pad" secureTextEntry />
      <View style={{ flexDirection: "row", gap: 8 }}>
        <Dugme yazi={kilit ? "🔁 PIN'i değiştir" : "🔒 Kilidi aç"} onPress={async () => {
          if (yeniPin.length < 4) { setMesaj("PIN en az 4 haneli olmalı."); return; }
          await pinAyarla(yeniPin); setYeniPin(""); setMesaj("✅ Kilit açık. Uygulama bir sonraki açılışta kilit isteyecek."); yenile();
        }} style={{ flex: 1 }} />
        {kilit ? <Dugme ikincil yazi="Kilidi kaldır" onPress={async () => { await pinAyarla(null); setMesaj("Kilit kaldırıldı."); yenile(); }} style={{ flex: 1 }} /> : null}
      </View>
      {mesaj ? <Text style={{ color: R.yesil, marginTop: 8 }}>{mesaj}</Text> : null}
    </Bolum>
  );
}


function GuncellemeBolumu({ Bolum }: { Bolum: any }) {
  const [durum, setDurum] = useState("");
  const [yeni, setYeni] = useState<Guncelleme | null>(null);
  const [bekle, setBekle] = useState(false);
  return (
    <Bolum baslik={`🔄 Güncelleme (sürüm ${mevcutSurum()})`}>
      <Text style={[us.alt, { marginBottom: 8 }]}>AREX açılışta günde bir kez yeni sürümü denetler; varsa üstte bildirim çıkar. Kurulumu Android senden onaylar, verilerin silinmez.</Text>
      <Dugme yazi="🔄 Güncellemeleri denetle" yukleniyor={bekle} onPress={async () => {
        setBekle(true); const g = await guncellemeDenetle(true); setBekle(false);
        setYeni(g); setDurum(g ? "" : "✅ En güncel sürümü kullanıyorsun.");
      }} />
      {yeni ? (
        <View style={{ marginTop: 10 }}>
          <Text style={{ color: "#fff", fontWeight: "800" }}>Yeni sürüm: {yeni.surum}</Text>
          {(yeni.notlar || []).map((n, i) => <Text key={i} style={{ color: R.yazi, fontSize: 13 }}>• {n}</Text>)}
          <Dugme yazi="⬇️ İndir ve kur" onPress={() => guncellemeyiIndir(yeni)} style={{ marginTop: 8 }} />
        </View>
      ) : null}
      {durum ? <Text style={{ color: R.yesil, marginTop: 8 }}>{durum}</Text> : null}
    </Bolum>
  );
}
