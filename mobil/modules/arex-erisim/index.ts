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
/** Yan tuş penceresinin yüksekliği (dp) — yalnız AsistanActivity'de etkili */
export const pencereBoyu = (dp: number) => { try { N?.pencereBoyu(Math.round(dp)); } catch {} };
/** Kart kapandıktan sonra (ms) genel eylem — yan tuş kartından "geri"/"ana ekran" için */
export const genelSonra = (eylem: Parameters<typeof genel>[0], ms = 350): boolean => { try { return !!N?.genelSonra(eylem, ms); } catch { return false; } };
export type Kisi = { ad: string; numara: string };
/** Rehberde kişi ara (READ_CONTACTS gerekir) */
export const kisiBul = (ad: string): Kisi[] => { try { return N?.kisiBul(ad) || []; } catch { return []; } };
/** Ara: izin varsa doğrudan, yoksa çevirici. Dönüş: doğrudan arandı mı */
export const ara = (numara: string): boolean => { try { return !!N?.ara(numara); } catch { return false; } };
/** WhatsApp sohbetini mesaj yazılı açar. Dönüş: WhatsApp yüklü mü */
export const whatsapp = (numara: string, metin: string): boolean => { try { return !!N?.whatsapp(numara, metin); } catch { return false; } };
export const sms = (numara: string, metin: string): boolean => { try { return !!N?.sms(numara, metin); } catch { return false; } };
/** ms sonra ekrandaki yazılardan birine dokun (uygulama açıldıktan sonra), deneme kez tekrarla */
export const sonraTikla = (metinler: string[], ms = 3000, deneme = 6): boolean => { try { return !!N?.sonraTikla(metinler, ms, deneme); } catch { return false; } };
