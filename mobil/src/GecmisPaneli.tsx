// AREX — sohbet geçmişi paneli: arama, tarih grupları, yeniden adlandırma, silme
import React, { useEffect, useMemo, useState } from "react";
import { Alert, Modal, Platform, Pressable, ScrollView, Text, TextInput, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { sohbetKaydet, sohbetleriOku, sohbetSil, yaz, type Sohbet } from "./depo";
import { R } from "./tema";

function grup(t: number): string {
  const g = new Date(); g.setHours(0, 0, 0, 0);
  const gun = 86400000;
  if (t >= g.getTime()) return "Bugün";
  if (t >= g.getTime() - gun) return "Dün";
  if (t >= g.getTime() - 7 * gun) return "Son 7 gün";
  if (t >= g.getTime() - 30 * gun) return "Son 30 gün";
  return "Daha eski";
}

export default function GecmisPaneli({ acik, kapat, sec, aktifId }: { acik: boolean; kapat: () => void; sec: (s: Sohbet) => void; aktifId: string }) {
  const ic = useSafeAreaInsets();
  const [liste, setListe] = useState<Sohbet[]>([]);
  const [ara, setAra] = useState("");
  const [duzenle, setDuzenle] = useState<string | null>(null);
  const [yeniAd, setYeniAd] = useState("");
  const yenile = () => sohbetleriOku().then((l) => setListe(l.sort((a, b) => b.guncel - a.guncel)));
  useEffect(() => { if (acik) yenile(); }, [acik]);

  const gruplu = useMemo(() => {
    const q = ara.trim().toLocaleLowerCase("tr");
    const f = q ? liste.filter((s) => s.baslik.toLocaleLowerCase("tr").includes(q) || s.mesajlar.some((m) => m.metin.toLocaleLowerCase("tr").includes(q))) : liste;
    const out: [string, Sohbet[]][] = [];
    for (const s of f) {
      const g = grup(s.guncel);
      const son = out[out.length - 1];
      if (son && son[0] === g) son[1].push(s); else out.push([g, [s]]);
    }
    return out;
  }, [liste, ara]);

  const tumunuSil = () => {
    const sil = async () => { await yaz("arex_sohbetler", []); yenile(); };
    if (Platform.OS === "web") { if (globalThis.confirm?.("Tüm sohbet geçmişi silinsin mi?")) sil(); return; }
    Alert.alert("Tüm geçmiş silinsin mi?", "Bu işlem geri alınamaz.", [{ text: "Vazgeç", style: "cancel" }, { text: "Sil", style: "destructive", onPress: sil }]);
  };

  return (
    <Modal visible={acik} transparent animationType="slide" onRequestClose={kapat}>
      <Pressable style={{ flex: 1, backgroundColor: "rgba(0,0,0,0.55)" }} onPress={kapat} />
      <View style={{ maxHeight: "82%", backgroundColor: R.bg2, borderTopLeftRadius: 28, borderTopRightRadius: 28, borderWidth: 1, borderColor: R.cizgi, paddingTop: 10, paddingBottom: ic.bottom + 12 }}>
        <View style={{ width: 44, height: 5, borderRadius: 3, backgroundColor: R.cizgi, alignSelf: "center", marginBottom: 10 }} />
        <View style={{ flexDirection: "row", alignItems: "center", paddingHorizontal: 18, marginBottom: 10 }}>
          <Text style={{ color: "#fff", fontSize: 20, fontWeight: "800", flex: 1 }}>💬 Sohbet geçmişi</Text>
          <Text style={{ color: R.soluk, fontSize: 12 }}>{liste.length} sohbet</Text>
        </View>
        <TextInput value={ara} onChangeText={setAra} placeholder="🔎 Sohbetlerde ara…" placeholderTextColor={R.soluk}
          style={{ marginHorizontal: 16, marginBottom: 8, backgroundColor: R.kart, borderRadius: 14, borderWidth: 1, borderColor: R.cizgi, color: R.yazi, paddingHorizontal: 14, paddingVertical: 10, fontSize: 15 }} />
        <ScrollView contentContainerStyle={{ paddingHorizontal: 12, paddingBottom: 10 }} keyboardShouldPersistTaps="handled">
          {!gruplu.length ? <Text style={{ color: R.soluk, textAlign: "center", marginTop: 20 }}>{ara ? "Eşleşen sohbet yok." : "Henüz kayıtlı sohbet yok."}</Text> : null}
          {gruplu.map(([g, sohbetler]) => (
            <View key={g} style={{ marginBottom: 6 }}>
              <Text style={{ color: R.acc2, fontSize: 12, fontWeight: "800", letterSpacing: 0.6, marginLeft: 6, marginVertical: 6 }}>{g.toLocaleUpperCase("tr")}</Text>
              {sohbetler.map((s) => {
                const son = [...s.mesajlar].reverse().find((m) => m.rol === "assistant")?.metin.replace(/[#*_`>|]/g, "").replace(/\s+/g, " ").slice(0, 70) || "";
                const aktif = s.id === aktifId;
                return (
                  <View key={s.id} style={{ flexDirection: "row", alignItems: "center", backgroundColor: aktif ? R.hap : R.kart, borderRadius: 16, padding: 12, marginBottom: 6, borderWidth: 1, borderColor: aktif ? R.acc : "transparent" }}>
                    {duzenle === s.id ? (
                      <TextInput autoFocus value={yeniAd} onChangeText={setYeniAd} onSubmitEditing={async () => { await sohbetKaydet({ ...s, baslik: yeniAd.trim() || s.baslik }); setDuzenle(null); yenile(); }}
                        style={{ flex: 1, color: "#fff", fontSize: 15, borderBottomWidth: 1, borderBottomColor: R.acc, paddingVertical: 4 }} />
                    ) : (
                      <Pressable style={{ flex: 1 }} onPress={() => { sec(s); kapat(); }}>
                        <Text style={{ color: "#fff", fontSize: 15, fontWeight: "700" }} numberOfLines={1}>{s.baslik || "Sohbet"}</Text>
                        {son ? <Text style={{ color: R.soluk, fontSize: 12.5, marginTop: 2 }} numberOfLines={1}>{son}</Text> : null}
                        <Text style={{ color: R.soluk, fontSize: 11, marginTop: 3 }}>{new Date(s.guncel).toLocaleString("tr-TR", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })} • {s.mesajlar.length} mesaj</Text>
                      </Pressable>
                    )}
                    <Pressable hitSlop={8} onPress={() => { setDuzenle(duzenle === s.id ? null : s.id); setYeniAd(s.baslik); }} style={{ paddingHorizontal: 8 }}><Text style={{ fontSize: 16 }}>✏️</Text></Pressable>
                    <Pressable hitSlop={8} onPress={async () => { await sohbetSil(s.id); yenile(); }} style={{ paddingHorizontal: 6 }}><Text style={{ fontSize: 16 }}>🗑️</Text></Pressable>
                  </View>
                );
              })}
            </View>
          ))}
          {liste.length ? <Pressable onPress={tumunuSil} style={{ alignSelf: "center", padding: 10 }}><Text style={{ color: R.kirmizi, fontSize: 13 }}>Tüm geçmişi sil</Text></Pressable> : null}
        </ScrollView>
      </View>
    </Modal>
  );
}
