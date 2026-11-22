// AREX — ses çalma: önce Gemini doğal anlatıcı (WAV), olmazsa cihazın kendi sesi (expo-speech)
import { createAudioPlayer, setAudioModeAsync, type AudioPlayer } from "expo-audio";
import * as Speech from "expo-speech";
import { Platform } from "react-native";
import { baytB64, dogalSes, seseUygun } from "./ai";
import { DILLER } from "./tema";

let oynatici: AudioPlayer | null = null;
let anlatimNo = 0;  // durdurulunca artar → bekleyen devam parçaları iptal
let webUrl: string | null = null;

/** Kullanıcı durdurunca: çalanı durdur + bekleyen devam parçalarını iptal et */
export async function sesiDurdur() {
  anlatimNo++;
  await calariDurdur();
}

/** Yalnız çalanı durdurur (parça geçişlerinde; devam zincirini iptal etmez) */
async function calariDurdur() {
  try { oynatici?.pause(); oynatici?.remove(); } catch {}
  oynatici = null;
  if (webUrl) { try { URL.revokeObjectURL(webUrl); } catch {} webUrl = null; }
  try { await Speech.stop(); } catch {}
}

export async function baytlariCal(bayt: Uint8Array) {
  await calariDurdur();
  let kaynak: string;
  if (Platform.OS === "web") {
    webUrl = URL.createObjectURL(new Blob([bayt as BlobPart], { type: "audio/wav" }));
    kaynak = webUrl;
  } else {
    const { File, Paths } = await import("expo-file-system");
    const f = new File(Paths.cache, `arex_ses_${Date.now()}.wav`);
    f.write(bayt);
    kaynak = f.uri;
  }
  // Arka plan modu KAPALI: aksi halde Android kalıcı medya bildirimi ("hazırlanıyor/çalıyor") gösteriyordu
  try { await setAudioModeAsync({ playsInSilentMode: true, shouldPlayInBackground: false, interruptionMode: "mixWithOthers" }); } catch {}
  const o = createAudioPlayer({ uri: kaynak });
  oynatici = o;
  return new Promise<void>((bitti) => {
    let tamam = false;
    const son = () => { if (tamam) return; tamam = true; if (oynatici === o) { try { o.remove(); } catch {} oynatici = null; } bitti(); };
    (o as any).addListener("playbackStatusUpdate", (d: any) => { if (d.didJustFinish) son(); });
    o.play();
    setTimeout(son, 10 * 60_000);  // güvenlik: takılırsa
  });
}

/** İlk 1-2 cümle (≤ ~220 harf) + kalan — doğal ses hemen başlasın diye */
function ilkParca(metin: string): [string, string] {
  const t = seseUygun(metin).trim();
  if (t.length <= 260) return [t, ""];
  const cumleler = t.match(/[^.!?…]+[.!?…]+["'”’)]*\s*|[^.!?…]+$/g) || [t];
  let ilk = "";
  for (const c of cumleler) { if ((ilk + c).length > 220 && ilk) break; ilk += c; }
  return [ilk.trim(), t.slice(ilk.length).trim()];
}

/** Metni doğal sesle anlatır. Dönüş: "dogal" | "cihaz" | "" */
export async function anlat(metin: string, dil: string, uslup = "masal", anlatici = "masalci", dogalDene = true): Promise<string> {
  if (dogalDene) {
    // Hızlı başlangıç: ilk cümleler seslendirilip HEMEN çalınır, kalan arkada hazırlanır ve kesintisiz devam eder
    const [ilk, kalan] = ilkParca(metin);
    const kalanSoz = kalan ? dogalSes(kalan, uslup, anlatici) : Promise.resolve(null);
    const bayt = await dogalSes(ilk, uslup, anlatici);
    if (bayt) {
      const oturum = ++anlatimNo;
      baytlariCal(bayt).then(async () => {
        if (oturum !== anlatimNo) return;  // bu sırada durduruldu/yeni anlatım başladı
        const b2 = await kalanSoz;
        if (oturum !== anlatimNo) return;
        if (b2) await baytlariCal(b2);
        else if (kalan) Speech.speak(kalan, { language: DILLER[dil]?.speech || "tr-TR", rate: 1.0 });
      });
      return "dogal";
    }
  }
  await sesiDurdur();
  Speech.speak(seseUygun(metin), {
    language: DILLER[dil]?.speech || "tr-TR",
    rate: uslup === "uyku" ? 0.85 : 1.0,
    pitch: anlatici === "dede" ? 0.9 : 1.05,
  });
  return "cihaz";
}

export { baytB64 };
