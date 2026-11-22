// AREX — Tilavet motoru: tek oynatıcı + sıradaki ayeti önceden yükleme (boşluksuz geçiş), ayet tekrarı (hafızlık),
// hız, sayfa bitince otomatik devam, arka planda çalma ve kilit ekranı kontrolleri.
import { clearPreloadedSource, createAudioPlayer, preload, setAudioModeAsync, type AudioPlayer } from "expo-audio";
import { Platform } from "react-native";
import { kariBul, SURELER, sesUrl } from "./kuran";

export type Parca = { sure: number; no: number; sayfa?: number; besmele?: boolean };
export type TilavetDurum = {
  aktif: boolean; caliyor: boolean; yukleniyor: boolean;
  parca: Parca | null; sira: number; toplam: number;
  kari: string; tekrar: number; tekrarSayac: number; hiz: number;
  /** önizlemede çalan kâri (seçili kâri değişmez) */
  onizleme: string | null;
};

type Devam = (son: Parca) => Promise<Parca[] | null>;

let oynatici: AudioPlayer | null = null;
let kuyruk: Parca[] = [];
let devamFn: Devam | null = null;
let onYuklenen: string | null = null;
let kilitAcik = false;
const dinleyiciler = new Set<(d: TilavetDurum) => void>();
let d: TilavetDurum = { aktif: false, caliyor: false, yukleniyor: false, parca: null, sira: -1, toplam: 0, kari: "Alafasy_128kbps", tekrar: 1, tekrarSayac: 1, hiz: 1, onizleme: null };

const yay = (yama: Partial<TilavetDurum>) => { d = { ...d, ...yama }; dinleyiciler.forEach((f) => f(d)); };
export const durum = () => d;
export function abone(f: (d: TilavetDurum) => void) { dinleyiciler.add(f); f(d); return () => { dinleyiciler.delete(f); }; }

const url = (p: Parca) => { const k = d.onizleme || d.kari; return p.besmele ? sesUrl(k, 1, 1) : sesUrl(k, p.sure, p.no); };
/** Sure başında (Fâtiha ve Tevbe hariç) önce besmele okunur */
export function besmeleEkle(l: Parca[]): Parca[] {
  const o: Parca[] = [];
  for (const p of l) { if (p.no === 1 && p.sure !== 1 && p.sure !== 9 && !p.besmele) o.push({ ...p, besmele: true }); o.push(p); }
  return o;
}

async function hazirla() {
  // Tilavet her başladığında arka plan modunu aç (durdurulunca kapanır)
  try {
    await setAudioModeAsync({ playsInSilentMode: true, shouldPlayInBackground: true, interruptionMode: "doNotMix" });
  } catch {}
  if (oynatici) return oynatici;
  oynatici = createAudioPlayer(null, { updateInterval: 250 } as any);
  (oynatici as any).addListener("playbackStatusUpdate", (s: any) => {
    if (s.didJustFinish) { ilerle(); return; }
    const yuk = !!s.isBuffering && !s.playing;
    if (yuk !== d.yukleniyor || !!s.playing !== d.caliyor) yay({ yukleniyor: yuk, caliyor: !!s.playing || (d.caliyor && yuk) });
  });
  return oynatici;
}

function kilitEkrani(p: Parca) {
  if (Platform.OS === "web" || !oynatici) return;
  const meta = { title: p.besmele ? "Besmele" : `${SURELER[p.sure - 1]} ${p.no}`, artist: kariBul(d.onizleme || d.kari).ad, albumTitle: "AREX • Kur'an-ı Kerim" };
  try {
    if (!kilitAcik) { oynatici.setActiveForLockScreen(true, meta); kilitAcik = true; }
    else oynatici.updateLockScreenMetadata(meta);
  } catch {}
}

/** Platforma göre senkron/asenkron dönen çağrıları sessizce güvenli çalıştırır */
function guvenli(f: () => unknown) { try { Promise.resolve(f()).catch(() => {}); } catch {} }

function onYukle(i: number) {
  const p = kuyruk[i];
  if (!p) return;
  const u = url(p);
  if (u === onYuklenen) return;
  if (onYuklenen) guvenli(() => clearPreloadedSource(onYuklenen!));
  onYuklenen = u;
  guvenli(() => preload(u));
}

async function oynat(i: number, tekrarSayac = 1) {
  const o = await hazirla();
  const p = kuyruk[i];
  if (!p) { durdur(); return; }
  yay({ aktif: true, parca: p, sira: i, toplam: kuyruk.length, tekrarSayac, yukleniyor: true, caliyor: true });
  try {
    o.replace({ uri: url(p) });
    o.setPlaybackRate(d.hiz, "high" as any);
    o.play();
  } catch { yay({ yukleniyor: false }); }
  kilitEkrani(p);
  // tekrar bitmediyse aynı ayet, bittiyse sıradaki önceden yüklensin
  onYukle(tekrarSayac < d.tekrar && !p.besmele ? i : i + 1);
}

async function ilerle() {
  const p = kuyruk[d.sira];
  if (p && !p.besmele && d.tekrarSayac < d.tekrar) { oynat(d.sira, d.tekrarSayac + 1); return; }
  if (d.sira + 1 < kuyruk.length) { oynat(d.sira + 1); return; }
  // sayfa/sure bitti → devam kaynağı varsa sıradakini getir (ör. sonraki mushaf sayfası)
  if (devamFn && p) {
    yay({ yukleniyor: true });
    try {
      const yeni = await devamFn(p);
      if (yeni && yeni.length) { kuyruk = besmeleEkle(yeni); oynat(0); return; }
    } catch {}
  }
  durdur();
}

/** Ayet listesini baştan (ya da `bas` sırasından) çalar. `devam` verilirse liste bitince sıradaki parçaları ister. */
export function cal(l: Parca[], bas = 0, devam?: Devam, onizleme: string | null = null) {
  yay({ onizleme });
  const tam = besmeleEkle(l);
  // istenen ayetin besmeleli listede doğru sırası
  const hedef = l[bas];
  let i = hedef ? tam.findIndex((x) => !x.besmele && x.sure === hedef.sure && x.no === hedef.no) : 0;
  if (i > 0 && tam[i - 1].besmele && bas === 0) i -= 1;
  kuyruk = tam; devamFn = devam || null;
  oynat(Math.max(0, i));
}

export function duraklat() { try { oynatici?.pause(); } catch {} yay({ caliyor: false }); }
export function surdur() { if (!d.aktif) return; try { oynatici?.play(); } catch {} yay({ caliyor: true }); }
export function sonraki() { if (d.aktif) { if (d.sira + 1 < kuyruk.length) oynat(d.sira + 1); else ilerle(); } }
export function onceki() { if (d.aktif) oynat(Math.max(0, d.sira - 1)); }
export function durdur() {
  try { oynatici?.pause(); if (kilitAcik) oynatici?.clearLockScreenControls(); } catch {}
  // Arka plan modunu kapat: başka sesler (masal, sohbet) kalıcı medya bildirimi açmasın
  setAudioModeAsync({ playsInSilentMode: true, shouldPlayInBackground: false, interruptionMode: "mixWithOthers" }).catch(() => {});
  kilitAcik = false; kuyruk = []; devamFn = null;
  if (onYuklenen) { const u = onYuklenen; guvenli(() => clearPreloadedSource(u)); onYuklenen = null; }
  yay({ aktif: false, caliyor: false, yukleniyor: false, parca: null, sira: -1, toplam: 0, onizleme: null });
}
export function ayarla(y: { kari?: string; tekrar?: number; hiz?: number }) {
  const kariDegisti = y.kari && y.kari !== d.kari;
  yay(y);
  if (y.hiz && oynatici) try { oynatici.setPlaybackRate(y.hiz, "high" as any); } catch {}
  if (kariDegisti && d.aktif) oynat(d.sira, d.tekrarSayac);  // yeni kâriyle aynı ayetten devam
}
/** Kâri önizlemesi: Fâtiha 1-2'yi o kâriden çalar, seçimi değiştirmez */
export const onizle = (kari: string) => cal([{ sure: 1, no: 1 }, { sure: 1, no: 2 }], 0, undefined, kari);
