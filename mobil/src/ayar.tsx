// AREX — uygulama genel ayarları (kalıcı)
import React, { createContext, useContext, useEffect, useState } from "react";
import { oku, yaz } from "./depo";

export type Ayarlar = {
  yanitDili: string;
  cocukModu: boolean;
  yas: string;
  yaraticilik: number;
  anlatici: string;
  otomatikSes: boolean;
  dogalSes: boolean;
};
const VARSAYILAN: Ayarlar = { yanitDili: "tr", cocukModu: false, yas: "7-9", yaraticilik: 0.75, anlatici: "masalci", otomatikSes: false, dogalSes: true };

const Ctx = createContext<{ ayar: Ayarlar; guncelle: (p: Partial<Ayarlar>) => void }>({ ayar: VARSAYILAN, guncelle: () => {} });

export function AyarSaglayici({ children }: { children: React.ReactNode }) {
  const [ayar, setAyar] = useState<Ayarlar>(VARSAYILAN);
  useEffect(() => { oku<Partial<Ayarlar>>("arex_ayar", {}).then((a) => setAyar({ ...VARSAYILAN, ...a })); }, []);
  const guncelle = (p: Partial<Ayarlar>) => setAyar((eski) => { const y = { ...eski, ...p }; yaz("arex_ayar", y); return y; });
  return <Ctx.Provider value={{ ayar, guncelle }}>{children}</Ctx.Provider>;
}
export const useAyar = () => useContext(Ctx);
