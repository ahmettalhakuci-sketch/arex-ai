// AREX — uygulama genel ayarları (kalıcı)
import React, { createContext, useContext, useEffect, useState } from "react";
import { ollamaBildir } from "./ai";
import { modBildir, oku, yaz } from "./depo";
import { temaUygula } from "./tema";

export type Ayarlar = {
  yanitDili: string;
  cocukModu: boolean;
  yas: string;
  yaraticilik: number;
  anlatici: string;
  otomatikSes: boolean;
  dogalSes: boolean;
  tema: string;
  yaziOlcek: number;
  kullanimModu: string;
  gozKoruma: boolean;
  sohbetTarzi: string;
  /** Yan tuşa basınca kart açılır açılmaz sesli dinlemeye başla (Gemini gibi) */
  yanTusOtomatik: boolean;
  /** Ev Wi-Fi'sindeki Mac'te Ollama (Llama 3.2 sohbet + Gemma 3 görsel) */
  ollamaAcik: boolean;
  ollamaAdres: string;
};
const VARSAYILAN: Ayarlar = { yanitDili: "tr", cocukModu: false, yas: "7-9", yaraticilik: 0.75, anlatici: "masalci", otomatikSes: false, dogalSes: true, tema: "gece", yaziOlcek: 1, kullanimModu: "kisisel", gozKoruma: false, sohbetTarzi: "dengeli", yanTusOtomatik: true, ollamaAcik: false, ollamaAdres: "192.168.1.45:11434" };

const Ctx = createContext<{ ayar: Ayarlar; guncelle: (p: Partial<Ayarlar>) => void }>({ ayar: VARSAYILAN, guncelle: () => {} });

export function AyarSaglayici({ children }: { children: React.ReactNode }) {
  const [ayar, setAyar] = useState<Ayarlar>(VARSAYILAN);
  useEffect(() => { oku<Partial<Ayarlar>>("arex_ayar", {}).then((a) => { const y = { ...VARSAYILAN, ...a }; temaUygula(y.tema, y.yaziOlcek); modBildir(y.kullanimModu); ollamaBildir(!!y.ollamaAcik, y.ollamaAdres); setAyar(y); }); }, []);
  const guncelle = (p: Partial<Ayarlar>) => setAyar((eski) => {
    const y = { ...eski, ...p };
    if (p.tema !== undefined || p.yaziOlcek !== undefined) temaUygula(y.tema, y.yaziOlcek);
    if (p.kullanimModu !== undefined) modBildir(y.kullanimModu);
    if (p.ollamaAcik !== undefined || p.ollamaAdres !== undefined) ollamaBildir(!!y.ollamaAcik, y.ollamaAdres);
    yaz("arex_ayar", y);
    return y;
  });
  return <Ctx.Provider value={{ ayar, guncelle }}>{children}</Ctx.Provider>;
}
export const useAyar = () => useContext(Ctx);
