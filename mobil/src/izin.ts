// AREX — izin isteme yardımcısı. Samsung/Android'de izin bir kez reddedildiyse (ya da pencere kapatıldıysa) sistem
// izin penceresini BİR DAHA GÖSTERMEZ; düğme "çalışmıyor" gibi görünür. Bu durumda kullanıcıyı doğrudan AREX'in
// izin sayfasına yönlendiririz.
import { Alert, Linking, Platform } from "react-native";

type Yanit = { granted: boolean; canAskAgain?: boolean; accessPrivileges?: string };

/** İzni ister; sorulamıyorsa ayarlara yönlendirir. Dönüş: izin verildi mi */
export async function izinIste(ad: string, iste: () => Promise<Yanit>, mevcut?: () => Promise<Yanit>): Promise<boolean> {
  // 1) Zaten verilmişse hiç sormadan geç (sorma isteği bazen cevapsız kalıyor — aşağıya bak)
  if (mevcut) { try { const m = await mevcut(); if (m.granted) return true; } catch {} }
  // 2) Sor; ama en fazla 8 sn bekle. Yan tuş penceresi açılıp kapandıktan sonra Android izin isteğini KAPANMIŞ pencereye
  //    bağlıyor ve istek hiç dönmüyordu → "İzin ver" düğmesi donuyordu (telefonda gerçek testte bulundu).
  let r: Yanit;
  try {
    r = await Promise.race([iste(), new Promise<Yanit>((ok) => setTimeout(() => ok({ granted: false, canAskAgain: false }), 8000))]);
  } catch { r = { granted: false, canAskAgain: false }; }
  if (!r.granted && mevcut) { try { if ((await mevcut()).granted) return true; } catch {} }
  if (r.granted || r.accessPrivileges === "limited" || r.accessPrivileges === "all") return true;
  if (Platform.OS !== "web") {
    Alert.alert(`${ad} izni gerekli`,
      r.canAskAgain === false
        ? `Telefon izin penceresini artık göstermiyor. Açılacak sayfada: İzinler → ${ad} → "Uygulamayı kullanırken izin ver".`
        : `${ad} izni verilmedi. Ayarlardan açabilirsin: İzinler → ${ad} → "Uygulamayı kullanırken izin ver".`,
      [{ text: "Vazgeç", style: "cancel" }, { text: "Ayarları aç", onPress: () => Linking.openSettings().catch(() => {}) }]);
  }
  return false;
}
