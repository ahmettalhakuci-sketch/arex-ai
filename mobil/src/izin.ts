// AREX — izin isteme yardımcısı. Samsung/Android'de izin bir kez reddedildiyse (ya da pencere kapatıldıysa) sistem
// izin penceresini BİR DAHA GÖSTERMEZ; düğme "çalışmıyor" gibi görünür. Bu durumda kullanıcıyı doğrudan AREX'in
// izin sayfasına yönlendiririz.
import { Alert, Linking, Platform } from "react-native";

type Yanit = { granted: boolean; canAskAgain?: boolean; accessPrivileges?: string };

/** İzni ister; sorulamıyorsa ayarlara yönlendirir. Dönüş: izin verildi mi */
export async function izinIste(ad: string, iste: () => Promise<Yanit>): Promise<boolean> {
  let r: Yanit;
  try { r = await iste(); } catch { r = { granted: false, canAskAgain: false }; }
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
