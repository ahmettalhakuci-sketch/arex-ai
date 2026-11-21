// AREX — otomatik güncelleme denetimi: GitHub'daki guncelleme.json'daki sürüm kodu uygulamanınkinden büyükse
// kullanıcıya "Yeni sürüm hazır" gösterilir; dokununca yeni APK indirilir (Android kurulumu kullanıcı onaylar).
import Constants from "expo-constants";
import { Linking, Platform } from "react-native";
import { oku, yaz } from "./depo";

export const GUNCELLEME_ADRESI = "https://raw.githubusercontent.com/ahmettalhakuci-sketch/arex-ai/master/guncelleme.json";
export type Guncelleme = { surum: string; kod: number; apk: string; notlar: string[] };

export const mevcutSurum = () => String(Constants.expoConfig?.version || "15.6.0");
export const mevcutKod = () => Number((Constants.expoConfig?.extra as any)?.surumKodu || 0);

/** Yeni sürüm varsa bilgisini döndürür; yoksa null. zorla=false iken günde en fazla bir kez ağa çıkar. */
export async function guncellemeDenetle(zorla = false): Promise<Guncelleme | null> {
  if (Platform.OS === "web") return null;  // masaüstü/web sürümü kendi derlemesiyle güncellenir
  const bugun = new Date().toISOString().slice(0, 10);
  const son = await oku<{ tarih: string; bilgi: Guncelleme | null }>("arex_guncelleme", { tarih: "", bilgi: null });
  if (!zorla && son.tarih === bugun) return son.bilgi && son.bilgi.kod > mevcutKod() ? son.bilgi : null;
  try {
    const c = new AbortController();
    const t = setTimeout(() => c.abort(), 10000);
    const r = await fetch(GUNCELLEME_ADRESI + "?t=" + Date.now(), { signal: c.signal });
    clearTimeout(t);
    if (!r.ok) return null;
    const bilgi = (await r.json()) as Guncelleme;
    await yaz("arex_guncelleme", { tarih: bugun, bilgi });
    return bilgi.kod > mevcutKod() ? bilgi : null;
  } catch {
    return null;
  }
}

export const guncellemeyiIndir = (g: Guncelleme) => Linking.openURL(g.apk);
