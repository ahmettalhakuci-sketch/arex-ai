// AREX — Kur'an, hadis ve Esmâ-i Hüsnâ (açık kaynak): alquran.cloud (Diyanet Vakfı meali + Alafasy tilaveti),
// HadeethEnc (kaynaklı, dereceli Türkçe hadis), AlAdhan (Esmâ-i Hüsnâ). Sohbet motoru da bunları kullanır.
import { oku, yaz } from "./depo";

async function json(url: string, ms = 12000) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  try { const r = await fetch(url, { signal: c.signal }); if (!r.ok) throw new Error("HTTP " + r.status); return await r.json(); }
  finally { clearTimeout(t); }
}

export type Ayet = { sure: number; sureAd: string; sureArapca: string; no: number; arapca: string; meal: string; ses: string };
export type Hadis = { baslik: string; metin: string; kaynak: string; derece: string; aciklama: string };

// Türkçe sure adları (arama ve gösterim için)
export const SURELER = ["Fâtiha", "Bakara", "Âl-i İmrân", "Nisâ", "Mâide", "En'âm", "A'râf", "Enfâl", "Tevbe", "Yûnus", "Hûd", "Yûsuf", "Ra'd",
  "İbrâhîm", "Hicr", "Nahl", "İsrâ", "Kehf", "Meryem", "Tâhâ", "Enbiyâ", "Hac", "Mü'minûn", "Nûr", "Furkân", "Şuarâ", "Neml", "Kasas",
  "Ankebût", "Rûm", "Lokmân", "Secde", "Ahzâb", "Sebe'", "Fâtır", "Yâsîn", "Sâffât", "Sâd", "Zümer", "Mü'min", "Fussilet", "Şûrâ",
  "Zuhruf", "Duhân", "Câsiye", "Ahkâf", "Muhammed", "Fetih", "Hucurât", "Kâf", "Zâriyât", "Tûr", "Necm", "Kamer", "Rahmân", "Vâkıa",
  "Hadîd", "Mücâdele", "Haşr", "Mümtehine", "Saff", "Cuma", "Münâfikûn", "Teğâbün", "Talâk", "Tahrîm", "Mülk", "Kalem", "Hâkka",
  "Meâric", "Nûh", "Cin", "Müzzemmil", "Müddessir", "Kıyâme", "İnsân", "Mürselât", "Nebe'", "Nâziât", "Abese", "Tekvîr", "İnfitâr",
  "Mutaffifîn", "İnşikâk", "Bürûc", "Târık", "A'lâ", "Gâşiye", "Fecr", "Beled", "Şems", "Leyl", "Duhâ", "İnşirâh", "Tîn", "Alak",
  "Kadir", "Beyyine", "Zilzâl", "Âdiyât", "Kâria", "Tekâsür", "Asr", "Hümeze", "Fîl", "Kureyş", "Mâûn", "Kevser", "Kâfirûn", "Nasr",
  "Tebbet", "İhlâs", "Felak", "Nâs"];

const sadele = (s: string) => s.toLocaleLowerCase("tr").normalize("NFD").replace(/[̀-ͯ'’^]/g, "").replace(/[âáà]/g, "a").replace(/[îí]/g, "i").replace(/[ûú]/g, "u");
export function sureBul(ad: string): number {
  const q = sadele(ad.trim());
  if (/^\d+$/.test(q)) return Math.min(114, Math.max(1, Number(q)));
  const i = SURELER.findIndex((x) => sadele(x) === q);
  if (i >= 0) return i + 1;
  const j = SURELER.findIndex((x) => sadele(x).startsWith(q) || q.startsWith(sadele(x)));
  return j >= 0 ? j + 1 : 0;
}

/** Bir sureden ayet aralığı (en fazla 30) — Arapça, Diyanet meali, Alafasy tilaveti */
export const MEALLER: Record<string, string> = { "tr.vakfi": "Diyanet Vakfı", "tr.yazir": "Elmalılı Hamdi Yazır", "tr.golpinarli": "Abdülbaki Gölpınarlı" };
export async function ayetler(sure: number, bas = 1, son = bas, meal = "tr.vakfi"): Promise<Ayet[]> {
  const limit = Math.min(30, Math.max(1, son - bas + 1));
  const d = await json(`https://api.alquran.cloud/v1/surah/${sure}/editions/quran-uthmani,${MEALLER[meal] ? meal : "tr.vakfi"},ar.alafasy?offset=${bas - 1}&limit=${limit}`);
  const [ar, tr, ses] = d.data;
  return ar.ayahs.map((a: any, i: number) => ({ sure, sureAd: SURELER[sure - 1], sureArapca: ar.name, no: a.numberInSurah, arapca: a.text, meal: tr.ayahs[i].text, ses: ses.ayahs[i].audio }));
}

const bugun = () => new Date().toISOString().slice(0, 10);
const gunNo = () => Math.floor(Date.now() / 86400000);

export async function gununAyeti(): Promise<Ayet> {
  const ons = await oku<{ tarih: string; ayet: Ayet } | null>("arex_gunun_ayeti2", null);
  if (ons && ons.tarih === bugun()) return ons.ayet;
  const n = ((gunNo() * 37) % 6236) + 1;  // her gün farklı, deterministik
  const d = await json(`https://api.alquran.cloud/v1/ayah/${n}/editions/quran-uthmani,tr.vakfi,ar.alafasy`);
  const [ar, tr, ses] = d.data;
  const ayet: Ayet = { sure: ar.surah.number, sureAd: SURELER[ar.surah.number - 1], sureArapca: ar.surah.name, no: ar.numberInSurah, arapca: ar.text, meal: tr.text, ses: ses.audio };
  await yaz("arex_gunun_ayeti2", { tarih: bugun(), ayet });
  return ayet;
}

let kategoriler: any[] | null = null;
const KURAN_KATEGORILERI = [31, 12, 39, 272, 1];  // hafızlık adabı, Kur'an'ın faziletleri…
const KONU_KATEGORI: Record<string, number[]> = { sabi: [282, 646], sabr: [282, 646], nama: [134], oruc: [137], anne: [273], baba: [273], ebev: [273],
  kura: [31, 12, 39, 272], hafi: [31], dua: [268], zikr: [268, 301], ahla: [282, 266], ilim: [31, 12], suku: [282], sukr: [282], tevb: [282], merh: [282, 646] };
/** Türkçe ünlü düşmesine dayanıklı kökler: sabır→{sabi, sabr} */
const kokler = (q: string) => (q.length < 3 ? [] : q.length >= 5 ? [q.slice(0, 4), q.slice(0, 3) + q[4]] : [q.slice(0, 4)]);
const kokluMu = (metin: string, k: string[]) => k.length > 0 && sadele(metin).split(/\s+/).some((w) => k.some((x) => w.startsWith(x)));

export async function hadisGetir(konu = "", sabitSecim?: number, katId?: number): Promise<Hadis & { tamEslesme: boolean }> {
  if (!kategoriler) kategoriler = await json("https://hadeethenc.com/api/v1/categories/list/?language=tr");
  const q = sadele(konu).replace(/\b(ile|ilgili|hakkinda|konulu|bir|hadis\S*)\b/g, "").trim();
  const rnd = (n: number) => (sabitSecim !== undefined ? sabitSecim % n : Math.floor(Math.random() * n));
  const k = q ? kokler(q.split(/\s+/)[0]) : [];
  let adaylar: number[] = katId ? [katId] : [];
  for (const x of k) adaylar.push(...(KONU_KATEGORI[x] || []));
  adaylar.push(...kategoriler!.filter((c) => kokluMu(String(c.title), k)).map((c) => Number(c.id)));
  if (!adaylar.length) adaylar = [Number(kategoriler![rnd(kategoriler!.length)].id)];
  let eslesen: any[] = [], yedek: any[] = [];
  for (const id of Array.from(new Set(adaylar)).slice(0, 5)) {
    const liste = (await json(`https://hadeethenc.com/api/v1/hadeeths/list/?language=tr&category_id=${id}&page=1&per_page=60`)).data || [];
    if (!yedek.length) yedek = liste;
    eslesen = liste.filter((h: any) => kokluMu(h.title, k));
    if (eslesen.length) break;
  }
  const havuz = eslesen.length ? eslesen : yedek.length ? yedek : (await json(`https://hadeethenc.com/api/v1/hadeeths/list/?language=tr&category_id=31&page=1&per_page=50`)).data;
  const sec = havuz[rnd(havuz.length)];
  const h = await json(`https://hadeethenc.com/api/v1/hadeeths/one/?language=tr&id=${sec.id}`);
  return { baslik: h.title, metin: h.hadeeth, kaynak: h.attribution, derece: h.grade, aciklama: String(h.explanation || ""), tamEslesme: eslesen.length > 0 || !q };
}

export async function gununHadisi(): Promise<Hadis> {
  const ons = await oku<{ tarih: string; hadis: Hadis } | null>("arex_gunun_hadisi2", null);
  if (ons && ons.tarih === bugun()) return ons.hadis;
  // Hafız için: Kur'an ve hafızlık adabı kategorilerinden, her gün farklı
  const hadis = await hadisGetir("", gunNo(), KURAN_KATEGORILERI[gunNo() % KURAN_KATEGORILERI.length]);
  await yaz("arex_gunun_hadisi2", { tarih: bugun(), hadis });
  return hadis;
}

export async function esma(no?: number) {
  const n = no && no >= 1 && no <= 99 ? no : (gunNo() % 99) + 1;
  const d = await json(`https://api.aladhan.com/v1/asmaAlHusna/${n}`);
  const x = d.data[0];
  return { no: x.number, isim: x.name, okunus: x.transliteration, anlam: x.en.meaning };
}

const ayetMd = (a: Ayet) => `**${a.sureAd} ${a.no}**\n\n> ${a.arapca}\n\n${a.meal}`;
const hadisMd = (h: Hadis) => `### 📜 ${h.baslik}\n\n${h.metin}\n\n_Kaynak: ${h.kaynak || "—"} • Derece: ${h.derece || "—"} (HadeethEnc.com)_`;

/** Sohbet motoru senkronu: Kur'an/hadis/esma istekleri doğrudan açık kaynaktan cevaplanır (uydurma yok). */
export async function dinSorusuCevapla(metin: string): Promise<string | null> {
  const t = metin.trim();
  const tl = t.toLocaleLowerCase("tr");
  try {
    if (/günün ayeti|bugünün ayeti|gunun ayeti/.test(tl)) {
      const a = await gununAyeti();
      return `### 📖 Günün Ayeti\n\n${ayetMd(a)}\n\n_Kaynak: Kur'an-ı Kerim, Diyanet Vakfı meali (alquran.cloud)_`;
    }
    if (/günün hadisi|bugünün hadisi|gunun hadisi/.test(tl)) return "### 🌙 Günün Hadisi\n\n" + hadisMd(await gununHadisi());
    let m = tl.match(/(.{2,40}?)\s+(?:ile|hakkında|ilgili|konulu)\s+(?:bir\s+)?hadis/) || tl.match(/hadis\w*\s+(?:söyle|oku|ver|anlat)?\s*[:\-]?\s*(.{3,30})?$/);
    if (/\bhadis/.test(tl) && /söyle|oku|ver|anlat|getir|paylaş|bir hadis|hadis-i şerif/.test(tl)) {
      const konu = (m && m[1] && !/bir|bana|söyle|oku/.test(m[1]) ? m[1] : "").replace(/\b(bana|bir|lütfen)\b/g, "").trim();
      const h = await hadisGetir(konu);
      return (h.tamEslesme ? "" : `_ℹ️ Kaynakta "${konu}" başlığıyla birebir hadis bulamadım; ilgili bir hadis paylaşıyorum._\n\n`) + hadisMd(h);
    }
    if (/esma|esmaül|esmaul|esmâ|allah'ın isimleri/.test(tl)) {
      const no = Number((tl.match(/\b(\d{1,2})\b/) || [])[1]) || undefined;
      const e = await esma(no);
      return `### ✨ Esmâ-i Hüsnâ — ${e.no}.\n\n> **${e.isim}** (${e.okunus})\n\nAnlamı: ${e.anlam}\n\n_Kaynak: AlAdhan_`;
    }
    m = t.match(/^\s*([A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ'’\- ]{2,20}?)\s*(?:suresi(?:nin)?\s*)?(\d{1,3})\s*(?:[-–:]\s*(\d{1,3}))?\.?\s*(?:ayet\w*)?\s*(?:meal\w*|oku|nedir|ne diyor)?\s*\??$/i);
    if (m && /\d/.test(t) && /(sure|ayet|meal|oku)|^[A-Za-zÇĞİÖŞÜçğıöşüâîû'’ -]+\s+\d+/i.test(t)) {
      const sure = sureBul(m[1]);
      if (sure) {
        const bas = Number(m[2]), son = m[3] ? Number(m[3]) : bas;
        const l = await ayetler(sure, bas, Math.min(son, bas + 9));
        if (l.length) return `### 📖 ${SURELER[sure - 1]} ${bas}${son > bas ? "-" + l[l.length - 1].no : ""}\n\n` + l.map((a) => `> ${a.arapca}\n\n**${a.no}.** ${a.meal}`).join("\n\n") + "\n\n_Kaynak: Kur'an-ı Kerim, Diyanet Vakfı meali (alquran.cloud)_";
      }
    }
  } catch {
    return "⚠️ Kur'an/hadis kaynağına şu an ulaşılamadı; biraz sonra tekrar dener misin?";
  }
  return null;
}

// ---------- Hafızlık takibi ----------
export type HafizKayit = { tarih: string; tur: "ezber" | "tekrar"; cuz?: number; sayfa: number; not?: string };
export type Hafizlik = { hedefSayfa: number; kayitlar: HafizKayit[]; cuzTekrar: Record<number, string> };
export const hafizlikOku = () => oku<Hafizlik>("arex_hafizlik", { hedefSayfa: 20, kayitlar: [], cuzTekrar: {} });
export const hafizlikYaz = (h: Hafizlik) => yaz("arex_hafizlik", h);
export function seri(h: Hafizlik): number {
  const gunler = new Set(h.kayitlar.map((k) => k.tarih));
  let n = 0; const d = new Date();
  for (;;) { const g = d.toISOString().slice(0, 10); if (!gunler.has(g)) { if (n === 0 && g === bugun()) { d.setDate(d.getDate() - 1); continue; } break; } n++; d.setDate(d.getDate() - 1); }
  return n;
}
export function bugunkuSayfa(h: Hafizlik) { return h.kayitlar.filter((k) => k.tarih === bugun()).reduce((a, k) => a + k.sayfa, 0); }
/** Tekrar önerisi: en uzun süredir tekrar edilmeyen 2 cüz */
export function tekrarOnerisi(h: Hafizlik): number[] {
  return Array.from({ length: 30 }, (_, i) => i + 1).sort((a, b) => (h.cuzTekrar[a] || "0000").localeCompare(h.cuzTekrar[b] || "0000")).slice(0, 2);
}
export { bugun };
