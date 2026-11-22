// AREX Erişim: Android Erişilebilirlik Servisi köprüsü (ekranı oku, dokun, yaz, kaydır, geri/ana ekran, uygulama aç)
import { Platform } from "react-native";
let N: any = null;
try { if (Platform.OS === "android") N = require("expo-modules-core").requireNativeModule("ArexErisim"); } catch { N = null; }
export const destekVar = () => !!N;
export const etkinMi = (): boolean => { try { return !!N?.etkinMi(); } catch { return false; } };
export const ayarlariAc = () => { try { N?.ayarlariAc(); } catch {} };
export const ekranOku = (): string => { try { return N?.ekranOku() || ""; } catch { return ""; } };
export const tikla = (metin: string): boolean => { try { return !!N?.tikla(metin); } catch { return false; } };
export const yaz = (metin: string): boolean => { try { return !!N?.yaz(metin); } catch { return false; } };
export const kaydir = (ileri: boolean): boolean => { try { return !!N?.kaydir(ileri); } catch { return false; } };
export const genel = (eylem: "geri" | "ana" | "son" | "bildirim" | "hizli" | "kilit" | "ekranGoruntusu"): boolean => { try { return !!N?.genel(eylem); } catch { return false; } };
export const uygulamaAc = (ad: string): string => { try { return N?.uygulamaAc(ad) || ""; } catch { return ""; } };
export type IzinTuru = "erisim" | "uygulama" | "bildirim" | "pil" | "asistan" | "kurulum" | "guvenlik";
export const ayarAc = (tur: IzinTuru): boolean => { try { return !!N?.ayarAc(tur); } catch { return false; } };
export const durumlar = (): { erisim: boolean; pil: boolean; asistan: boolean; asistanBiliniyor: boolean } => {
  try { return N?.durumlar() || { erisim: false, pil: false, asistan: false, asistanBiliniyor: false }; } catch { return { erisim: false, pil: false, asistan: false, asistanBiliniyor: false }; }
};
/** Ayarlarda açık mı (çalışmasa bile) */
export const ayardaAcik = (): boolean => { try { return !!N?.ayardaAcik(); } catch { return false; } };
/** Açık ama bağlantısı kopmuşsa kendini yeniden bağlar: "bagli" | "onarildi" | "kapali" | "izin-yok" */
export const onar = async (): Promise<string> => { try { return N ? await N.onar() : "kapali"; } catch { return "kapali"; } };
