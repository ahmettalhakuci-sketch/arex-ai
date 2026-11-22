// AREX — Canlı: Gemini Live (doğal sesli + kameralı gerçek zamanlı sohbet) ve cihaz içi Yerel Analiz
import { getRecordingPermissionsAsync, requestRecordingPermissionsAsync } from "expo-audio";
import { izinIste as izinIste2 } from "../izin";
import * as Erisim from "../../modules/arex-erisim";
import { Camera } from "expo-camera";
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Platform, Text, View, AppState } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { canliToken } from "../ai";
import { useAyar } from "../ayar";
import { anahtar, notKaydet, notlariOku, profilOku, profilOzeti } from "../depo";
import { CANLI_HTML, YEREL_HTML } from "../gomuluHtml";
import { R } from "../tema";
import { Dugme, Hap, s as us } from "../ui";
import WebSayfa from "../WebSayfa";
import { acHedef, HEDEFLER, telefonKomutu } from "../telefon";

export default function CanliEkrani({ sohbeteGonder, mini = false, tam = false }: { sohbeteGonder: (metin: string, cevap: string) => void; mini?: boolean; tam?: boolean }) {
  const ic = useSafeAreaInsets();
  const { ayar, guncelle } = useAyar();
  const [sekme, setSekme] = useState<"canli" | "yerel">("canli");
  const [izin, setIzin] = useState(Platform.OS === "web");
  const [cfg, setCfg] = useState<Record<string, unknown> | null>(null);
  const [hata, setHata] = useState("");

  /** Mikrofon zorunlu, kamera isteğe bağlı (kamera reddedilse de sesli sohbet çalışır).
   *  Açılışta sessizce sorar; düğmeyle basılınca soramıyorsa izin sayfasına yönlendirir (Samsung "bir daha sorma" durumu). */
  const izinIste = async (dugme = false) => {
    // Önce mevcut durum (sormadan) — sorma isteği yan tuş penceresinden sonra cevapsız kalabiliyordu
    const mik = dugme ? await izinIste2("Mikrofon", requestRecordingPermissionsAsync, getRecordingPermissionsAsync)
      : (await getRecordingPermissionsAsync().catch(() => ({ granted: false }))).granted || await izinIste2("Mikrofon", requestRecordingPermissionsAsync, getRecordingPermissionsAsync).catch(() => false);
    Camera.getCameraPermissionsAsync().then((k) => { if (!k.granted) Camera.requestCameraPermissionsAsync().catch(() => {}); }).catch(() => {});
    setIzin(mik);
    if (!mik) setHata("Mikrofon izni gerekli — aşağıdaki düğmeye dokun.");
  };
  useEffect(() => { if (Platform.OS !== "web") izinIste(); }, []);
  // Canlı açıkken mikrofon onun: "AREX" dinlemesini duraklat, çıkınca sürdür
  useEffect(() => {
    // Yalnız uygulama EKRANDAYKEN duraklat; arka plana geçince "AREX" dinlemesi sürsün (yoksa Canlı sekmesinde kalınca hiç uyanmıyordu)
    if (mini) return;  // yan tuş kartında duraklatmayı yerel taraf yönetiyor
    Erisim.uyanmaDuraklat(AppState.currentState === "active");
    const a = AppState.addEventListener("change", (d) => Erisim.uyanmaDuraklat(d === "active"));
    return () => { a.remove(); Erisim.uyanmaDuraklat(false); };
  }, []);

  const hazirla = async () => {
    setHata(""); setCfg(null);
    if ((ayar.kullanimModu || "kisisel") === "genel") { setHata("🔒 Canlı sohbet misafir modunda kapalı (kişisel API kullanılmaz). 👤 Kişisel moda geçince açılır."); return; }
    if (!anahtar("GEMINI_API_KEY")) { setHata("Canlı sohbet için Gemini anahtarı gerekli (⚙️ Ayarlar)."); return; }
    const t = await canliToken();
    const kisisel = (ayar.kullanimModu || "kisisel") === "kisisel";
    const [p, oz, notlar] = await Promise.all([profilOku(), profilOzeti(), notlariOku()]);
    // Geçici token alınamazsa doğrudan anahtarla (yalnızca bu cihazda) bağlanır
    setCfg({ ...(t ? { t } : { k: anahtar("GEMINI_API_KEY") }), mod: "asistan", kmod: ayar.cocukModu ? "cocuk" : (ayar.kullanimModu || "kisisel"),
      dil: ayar.yanitDili, yas: ayar.yas, profil: kisisel ? oz : "", ad: kisisel ? p.ad : "", goz: ayar.gozKoruma,
      notlar: kisisel ? notlar.slice(-20).map((n) => n.metin.slice(0, 200)) : [], acc: R.acc, acc2: R.acc2, otomatik: mini, tamEkran: tam });
  };
  useEffect(() => { if (sekme === "canli" && izin && !cfg) hazirla(); }, [sekme, izin, ayar.kullanimModu]);

  return (
    <View style={{ flex: 1, paddingTop: mini ? 0 : ic.top }}>
      <View style={{ flexDirection: "row", gap: 8, padding: 10, paddingBottom: 6, display: mini ? "none" : "flex" }}>
        <View style={{ flex: 1 }}><Hap yazi="🎙️ Canlı Sohbet" secili={sekme === "canli"} onPress={() => setSekme("canli")} /></View>
        <View style={{ flex: 1 }}><Hap yazi="🧠 Yerel Analiz" secili={sekme === "yerel"} onPress={() => setSekme("yerel")} /></View>
      </View>
      {!izin ? (
        <View style={{ padding: 20 }}>
          <Text style={us.alt}>Canlı sohbet ve yüz analizi için mikrofon ve kamera izni gerekli.</Text>
          <Dugme yazi="İzin ver" onPress={() => izinIste(true)} style={{ marginTop: 12 }} />
          {hata ? <Text style={{ color: R.kirmizi, marginTop: 10 }}>{hata}</Text> : null}
        </View>
      ) : sekme === "canli" ? (
        cfg ? <WebSayfa key={JSON.stringify(cfg).length + String(cfg.kmod)} html={CANLI_HTML} ayar={cfg} onMesaj={(v) => {
          if (v?.tur === "arex_not" && v.metin) notKaydet(String(v.metin), "canlı");
          if (v?.tur === "arex_goz") guncelle({ gozKoruma: !!v.acik });
          if (v?.tur === "arex_ac" && HEDEFLER.includes(v.hedef)) acHedef(v.hedef, String(v.sorgu || ""));
          if (v?.tur === "arex_komut" && v.komut) telefonKomutu(String(v.komut)).catch(() => {});
        }} /> : (
          <View style={{ flex: 1, alignItems: "center", justifyContent: "center", padding: 20 }}>
            {hata ? <><Text style={{ color: R.kirmizi, textAlign: "center" }}>{hata}</Text><Dugme yazi="Tekrar dene" onPress={hazirla} style={{ marginTop: 12 }} /></> : <ActivityIndicator color={R.acc2} size="large" />}
          </View>
        )
      ) : (
        <WebSayfa html={YEREL_HTML} onMesaj={(v) => { if (v?.tur === "arex_yerel_rapor") sohbeteGonder("🧠 Yerel analiz raporu", v.rapor); }} />
      )}
    </View>
  );
}
