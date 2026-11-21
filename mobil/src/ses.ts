// AREX — ses çalma: önce Gemini doğal anlatıcı (WAV), olmazsa cihazın kendi sesi (expo-speech)
import { createAudioPlayer, setAudioModeAsync, type AudioPlayer } from "expo-audio";
import * as Speech from "expo-speech";
import { Platform } from "react-native";
import { baytB64, dogalSes, seseUygun } from "./ai";
import { DILLER } from "./tema";

let oynatici: AudioPlayer | null = null;
let webUrl: string | null = null;

export async function sesiDurdur() {
  try { oynatici?.pause(); oynatici?.remove(); } catch {}
  oynatici = null;
  if (webUrl) { try { URL.revokeObjectURL(webUrl); } catch {} webUrl = null; }
  try { await Speech.stop(); } catch {}
}

async function baytlariCal(bayt: Uint8Array) {
  await sesiDurdur();
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
  try { await setAudioModeAsync({ playsInSilentMode: true }); } catch {}
  oynatici = createAudioPlayer({ uri: kaynak });
  oynatici.play();
}

/** Metni doğal sesle anlatır. Dönüş: "dogal" | "cihaz" | "" */
export async function anlat(metin: string, dil: string, uslup = "masal", anlatici = "masalci", dogalDene = true): Promise<string> {
  if (dogalDene) {
    const bayt = await dogalSes(metin, uslup, anlatici);
    if (bayt) {
      await baytlariCal(bayt);
      return "dogal";
    }
  }
  await sesiDurdur();
  Speech.speak(seseUygun(metin), {
    language: DILLER[dil]?.speech || "tr-TR",
    rate: uslup === "uyku" ? 0.8 : 0.95,
    pitch: anlatici === "dede" ? 0.9 : 1.05,
  });
  return "cihaz";
}

export { baytB64 };
