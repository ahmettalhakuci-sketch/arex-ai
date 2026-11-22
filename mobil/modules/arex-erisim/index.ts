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
export type IzinTuru = "erisim" | "uygulama" | "bildirim" | "pil" | "asistan" | "kurulum" | "guvenlik" | "ustte";
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
/** Asılı kalmış medya bildirimini temizler (açılışta) */
export const medyaBildirimTemizle = (): number => { try { return N?.medyaBildirimTemizle() || 0; } catch { return 0; } };
// ---------- "AREX" uyandırma + ses imzası (cihaz içi) ----------
export type UyanmaDurum = { acik: boolean; calisiyor: boolean; imzaVar: boolean; esik: number; yabanciSayi?: number; ustteGoster?: boolean; yenidenKayit?: boolean };
export const uyanmaBaslat = () => { try { N?.uyanmaBaslat(); } catch {} };
export const uyanmaDurdur = () => { try { N?.uyanmaDurdur(); } catch {} };
export const uyanmaSurdur = () => { try { N?.uyanmaSurdur(); } catch {} };
export const uyanmaDurum = (): UyanmaDurum => { try { return N?.uyanmaDurum() || { acik: false, calisiyor: false, imzaVar: false, esik: 0 }; } catch { return { acik: false, calisiyor: false, imzaVar: false, esik: 0 }; } };
export const sonUyanma = (): { zaman: number; sahip: boolean; seviye?: number; benzerlik: number; imzaVar: boolean } | null => { try { return N?.sonUyanma() ?? null; } catch { return null; } };
export const imzaOrnek = async (saniye = 4, etiket = "sahip"): Promise<{ vektor?: number[] | null; metin?: string; ses?: number; hata?: string }> => { try { return await N.imzaOrnek(saniye, etiket); } catch (e: any) { return { hata: String(e?.message || e) }; } };
export const imzaKaydet = (ornekler: number[][]): { esik?: number; enDusuk?: number; ortalama?: number; hata?: string } => { try { return N.imzaKaydet(ornekler); } catch (e: any) { return { hata: String(e?.message || e) }; } };
export const imzaSil = () => { try { N?.imzaSil(); } catch {} };
export const imzaKarsilastir = (v: number[]): { benzerlik?: number; esik?: number; sahip?: boolean; yabanci?: number; hata?: string } => { try { return N.imzaKarsilastir(v); } catch (e: any) { return { hata: String(e?.message || e) }; } };
export const uyanmaDuraklat = (b: boolean) => { try { N?.uyanmaDuraklat(b); } catch {} };
/** Kilit ekranı açık mı */
export const ekranKilitli = (): boolean => { try { return !!N?.ekranKilitli(); } catch { return false; } };
/** Android kilit açma ekranını gösterir (PIN/parmak izi). true → kilit açıldı */
export const kilidiKaldir = async (): Promise<boolean> => { try { return !!(await N?.kilidiKaldir()); } catch { return false; } };
// ---------- ⏰ Saat / sayaç / alarm ----------
export const sayac = (saniye: number, etiket = "AREX"): boolean => { try { return !!N?.sayac(Math.round(saniye), etiket); } catch { return false; } };
export const alarm = (saat: number, dakika: number, etiket = "AREX"): boolean => { try { return !!N?.alarm(saat, dakika, etiket); } catch { return false; } };
export const alarmlariGoster = () => { try { N?.alarmlariGoster(); } catch {} };
export const yabanciDurum = (): { sayi: number; son: number } => { try { return N?.yabanciDurum() || { sayi: 0, son: 0 }; } catch { return { sayi: 0, son: 0 }; } };
/** Başka birinin sesini "bu ben değilim" olarak öğret → toplam yabancı örnek sayısı */
export const yabanciEkle = (v: number[]): number => { try { return N?.yabanciEkle(v) || 0; } catch { return 0; } };
export const yabancilariSil = () => { try { N?.yabancilariSil(); } catch {} };
export const sonKarar = (): { benzerlik: number; yabanci: number; esik: number; sahip: boolean; zaman: number } | null => { try { return N?.sonKarar() ?? null; } catch { return null; } };
/** Parmak iziyle onaylanan son "AREX" sesini imzaya öğret */
export const sonUyanmayiOgren = (): boolean => { try { return !!N?.sonUyanmayiOgren(); } catch { return false; } };
