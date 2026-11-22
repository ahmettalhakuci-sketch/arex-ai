// AREX — fotoğraf / video seçme, küçültme ve base64'e çevirme
import * as ImageManipulator from "expo-image-manipulator";
import * as ImagePicker from "expo-image-picker";
import { Alert, Platform } from "react-native";
import { izinIste } from "./izin";

export type Ek = { uri: string; b64: string; mime: string; video: boolean; onizleme: string; ad: string };

const SINIR = 18 * 1024 * 1024;

async function webB64(uri: string): Promise<string> {
  const blob = await (await fetch(uri)).blob();
  return new Promise((ok, hata) => {
    const r = new FileReader();
    r.onload = () => ok(String(r.result).split(",")[1] || "");
    r.onerror = hata;
    r.readAsDataURL(blob);
  });
}

async function dosyaB64(uri: string): Promise<string> {
  if (Platform.OS === "web") return webB64(uri);
  const { File } = await import("expo-file-system");
  return new File(uri).base64();
}

async function boyutla(uri: string, genislik: number, sikistir: number) {
  const ctx = ImageManipulator.ImageManipulator.manipulate(uri);
  ctx.resize({ width: genislik });
  const ref = await ctx.renderAsync();
  return ref.saveAsync({ compress: sikistir, format: ImageManipulator.SaveFormat.JPEG, base64: true });
}

async function gorselHazirla(uri: string): Promise<Ek> {
  const buyuk = await boyutla(uri, 1600, 0.82);
  const kucuk = await boyutla(uri, 360, 0.7);
  return { uri: buyuk.uri, b64: buyuk.base64 || "", mime: "image/jpeg", video: false, onizleme: "data:image/jpeg;base64," + (kucuk.base64 || ""), ad: "foto.jpg" };
}

export async function medyaSec(kaynak: "galeri" | "kamera" | "video"): Promise<Ek | null> {
  try {
    if (kaynak === "kamera") {
      if (!(await izinIste("Kamera", ImagePicker.requestCameraPermissionsAsync))) return null;
    }
    const ayar: ImagePicker.ImagePickerOptions = { mediaTypes: kaynak === "video" ? ["videos"] : ["images"], quality: 0.85, videoMaxDuration: 120 };
    const sonuc = kaynak === "kamera" ? await ImagePicker.launchCameraAsync(ayar) : await ImagePicker.launchImageLibraryAsync(ayar);
    if (sonuc.canceled || !sonuc.assets?.length) return null;
    const a = sonuc.assets[0];
    if (a.type === "video" || kaynak === "video") {
      if (a.fileSize && a.fileSize > SINIR) { Alert.alert("Video çok büyük", "En fazla ~18 MB. Daha kısa bir video seç."); return null; }
      const b64 = await dosyaB64(a.uri);
      if (b64.length * 0.75 > SINIR) { Alert.alert("Video çok büyük", "En fazla ~18 MB. Daha kısa bir video seç."); return null; }
      const mime = a.mimeType || (a.uri.toLowerCase().endsWith(".mov") ? "video/quicktime" : "video/mp4");
      return { uri: a.uri, b64, mime, video: true, onizleme: "", ad: a.fileName || "video.mp4" };
    }
    return await gorselHazirla(a.uri);
  } catch (e: any) {
    Alert.alert("Medya açılamadı", String(e?.message || e));
    return null;
  }
}
