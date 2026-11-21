// AREX — cihaz içi (çevrimdışı) matematik motoru: mathjs + sayısal yöntemler
import { all, create } from "mathjs";

const m = create(all, { number: "number", precision: 64 });

export type MatSonuc = { baslik: string; girdi: string; sonuc: string; ek?: string };

const fmt = (v: number) => {
  if (!isFinite(v)) return v > 0 ? "∞" : v < 0 ? "-∞" : "tanımsız";
  const r = Math.abs(v - Math.round(v)) < 1e-10 ? Math.round(v) : +v.toPrecision(10);
  return String(r).replace(".", ",");
};
const kesir = (v: number) => {
  try {
    if (Number.isInteger(v)) return "";
    const f = m.fraction(v) as any;
    return Math.abs(f.d) < 10000 ? ` = ${f.s * f.n}/${f.d}` : "";
  } catch { return ""; }
};

export function hazirla(s: string): string {
  return (s || "")
    .replace(/[²]/g, "^2").replace(/[³]/g, "^3").replace(/×/g, "*").replace(/÷/g, "/").replace(/−/g, "-")
    .replace(/√\s*\(/g, "sqrt(").replace(/√\s*(\d+(?:\.\d+)?|[a-z])/g, "sqrt($1)").replace(/π/g, "pi").replace(/∞/g, "Infinity")
    .replace(/(\d),(\d)/g, "$1.$2").replace(/\bln\(/g, "log(").replace(/\b(kaçtır|kaç|nedir|eder|olur|hesapla|bul)\b/gi, "")
    .replace(/[?=]\s*$/g, "").trim();
}

function polinomKatsayi(ifade: string, v = "x"): number[] | null {
  try {
    const node = m.rationalize(ifade, {}, true) as any;
    const katsayi: number[] = (node.coefficients || []).map((c: any) => Number(c));
    if (!katsayi.length || katsayi.some((c) => !isFinite(c))) return null;
    return katsayi; // artan derece
  } catch { return null; }
}

/** Durand–Kerner ile tüm (karmaşık) kökler */
function kokler(katsayiArtan: number[]): { re: number; im: number }[] {
  const a = [...katsayiArtan].reverse(); // azalan
  while (a.length && Math.abs(a[0]) < 1e-14) a.shift();
  const n = a.length - 1;
  if (n < 1) return [];
  const b = a.map((c) => c / a[0]);
  let z = Array.from({ length: n }, (_, i) => m.complex(Math.cos((2 * Math.PI * i) / n + 0.4) * 0.9, Math.sin((2 * Math.PI * i) / n + 0.4) * 0.9) as any);
  const p = (x: any) => b.reduce((acc: any, c) => m.add(m.multiply(acc, x), c), m.complex(0, 0));
  for (let it = 0; it < 500; it++) {
    let deg = 0;
    z = z.map((zi: any, i: number) => {
      let pay = p(zi), payda: any = m.complex(1, 0);
      z.forEach((zj: any, j: number) => { if (i !== j) payda = m.multiply(payda, m.subtract(zi, zj)); });
      const yeni = m.subtract(zi, m.divide(pay, payda));
      deg = Math.max(deg, m.abs(m.subtract(yeni, zi) as any) as number);
      return yeni;
    });
    if (deg < 1e-13) break;
  }
  return z.map((c: any) => ({ re: Math.abs(c.re) < 1e-9 ? 0 : c.re, im: Math.abs(c.im) < 1e-9 ? 0 : c.im }));
}

function simpson(f: (x: number) => number, a: number, b: number, n = 2000) {
  const h = (b - a) / n;
  let s = f(a) + f(b);
  for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2);
  return (s * h) / 3;
}

export function coz(girdi: string): MatSonuc | null {
  const t = girdi.trim();
  const tl = t.toLocaleLowerCase("tr");
  let r: RegExpMatchArray | null = null;
  try {
    // Türev
    if (/türev/.test(tl)) {
      const mertebe = Number(tl.match(/(\d)\s*\.?\s*(?:mertebe\S*\s*)?türev/)?.[1] || 1);
      const ifade = hazirla(t.replace(/(\d)\s*\.?\s*(?:mertebe\S*\s*)?türev\S*/i, " ").replace(/türev\S*/gi, " ")
        .replace(/\s*'?n?[ıiuü]n\s*$/i, "").replace(/^\s*[:]\s*/, "").replace(/^(f\(x\)|y)\s*=\s*/i, "").replace(/(?<=[)\dx])\s*'?n?[ıiuü]n\b/i, ""));
      let d: any = m.parse(ifade);
      for (let i = 0; i < mertebe; i++) d = m.derivative(d, "x");
      return { baslik: `${mertebe > 1 ? mertebe + ". " : ""}Türev (d/dx)`, girdi: ifade, sonuc: m.simplify(d).toString() };
    }
    // Belirli integral (sayısal)
    if (/integral|∫/.test(tl)) {
      let a: string | undefined, b: string | undefined, govde = t;
      const s1 = t.match(/(-?[\d.]+|pi|π)\s*'?(?:dan|den|tan|ten)\s*(-?[\d.]+|pi|π)\s*'?(?:a|e|ya|ye)\s*(?:kadar)?/i);
      if (s1) { a = s1[1]; b = s1[2]; govde = t.replace(s1[0], " "); }
      const s2 = govde.match(/^(.*?),\s*(-?[\d.]+|pi)\s*,\s*(-?[\d.]+|pi)\s*$/);
      if (!s1 && s2) { govde = s2[1]; a = s2[2]; b = s2[3]; }
      govde = govde.replace(/belirli|integral\S*|∫/gi, " ").replace(/\s*d\s*x\s*(=\s*\?)?\s*$/i, "").replace(/(?<=[)\dx])\s*'?n?[ıiuü]n\s*$/i, "").replace(/^\s*:\s*/, "");
      if (a !== undefined && b !== undefined) {
        const f = m.compile(hazirla(govde));
        const v = simpson((x) => f.evaluate({ x }), Number(m.evaluate(hazirla(a))), Number(m.evaluate(hazirla(b))));
        return { baslik: "Belirli İntegral (sayısal)", girdi: `∫[${a}, ${b}] ${govde.trim()} dx`, sonuc: fmt(v) + kesir(v) };
      }
      return null; // belirsiz integral → yapay zekâ + bulut doğrulaması
    }
    // Limit (sayısal)
    r = tl.match(/lim(?:it)?\s*[:\-]?\s*x\s*(?:->|→)\s*(-?[\d.]+|∞|sonsuz|infinity|pi)\s*[,:]?\s*(.+)/);
    if (r) {
      const f = m.compile(hazirla(r[2]));
      const sonsuz = /∞|sonsuz|infinity/.test(r[1]);
      const h = sonsuz ? null : Number(m.evaluate(r[1]));
      const deg = sonsuz ? [1e6, 1e8].map((x) => f.evaluate({ x })) : [h! + 1e-7, h! - 1e-7].map((x) => f.evaluate({ x }));
      const ok = Math.abs(deg[0] - deg[1]) < 1e-3 * Math.max(1, Math.abs(deg[0]));
      return { baslik: "Limit (sayısal yaklaşım)", girdi: `lim x→${r[1]} ${r[2]}`, sonuc: ok ? fmt(deg[0]) : "Limit yok / sağ-sol farklı", ek: ok ? "" : `sağ ≈ ${fmt(deg[0])}, sol ≈ ${fmt(deg[1])}` };
    }
    // Sadeleştir / çarpan
    r = tl.match(/(?:sadeleştir|basitleştir|simplify)\s*[:\-]?\s*(.+)/);
    if (r) return { baslik: "Sadeleştirme", girdi: r[1], sonuc: m.simplify(hazirla(r[1])).toString() };
    // Denklem sistemi (doğrusal)
    const parcalar = t.split(/[;,]\s*|\s+ve\s+/i).filter((p) => p.includes("=") && !/[<>]/.test(p));
    if (parcalar.length >= 2) {
      const degisken = Array.from(new Set((parcalar.join(" ").match(/\b[xyzt]\b|(?<=\d)[xyzt]/g) || []))).sort();
      const A: number[][] = [], B: number[] = [];
      for (const p of parcalar) {
        const [sol, sag] = p.split("=");
        const ifade = `(${hazirla(sol)})-(${hazirla(sag)})`;
        const f = m.compile(ifade);
        const sifir = Object.fromEntries(degisken.map((d) => [d, 0]));
        const c0 = f.evaluate(sifir);
        A.push(degisken.map((d) => f.evaluate({ ...sifir, [d]: 1 }) - c0));
        B.push(-c0);
      }
      const x = m.lusolve(A, B) as any;
      return { baslik: "Denklem Sistemi", girdi: parcalar.join(" ; "), sonuc: degisken.map((d, i) => `${d} = ${fmt(Number(x[i][0] ?? x[i]))}${kesir(Number(x[i][0] ?? x[i]))}`).join(", ") };
    }
    // Tek bilinmeyenli denklem (polinom)
    if (t.includes("=") && /x/.test(t) && !/[<>]/.test(t)) {
      const [sol, sag] = t.replace(/\b(çöz|denklemini|denklemi|kökleri|bul)\b/gi, "").split("=");
      const ifade = `(${hazirla(sol)})-(${hazirla(sag || "0")})`;
      const k = polinomKatsayi(ifade);
      if (k) {
        const kk = kokler(k).sort((a, b) => (a.im === 0 ? 0 : 1) - (b.im === 0 ? 0 : 1) || a.re - b.re || a.im - b.im);
        const yaz = kk.map((z) => (z.im === 0 ? fmt(z.re) + kesir(z.re) : `${fmt(z.re)} ${z.im > 0 ? "+" : "-"} ${fmt(Math.abs(z.im))}i`));
        return { baslik: `Denklem (${k.length - 1}. derece)`, girdi: `${sol.trim()} = ${(sag || "0").trim()}`, sonuc: kk.length ? "x ∈ { " + yaz.join(" ; ") + " }" : "Çözüm yok / her x için doğru",
          ek: kk.some((z) => z.im !== 0) ? `Reel kök: ${kk.filter((z) => z.im === 0).length}, karmaşık kök: ${kk.filter((z) => z.im !== 0).length}` : "" };
      }
    }
    // İstatistik
    if (/ortalama|medyan|ortanca|varyans|standart sapma|açıklık/.test(tl)) {
      const s = (t.replace(/(\d),(\d)/g, "$1.$2").match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
      if (s.length >= 2) {
        return { baslik: "İstatistik", girdi: s.map(fmt).join(", "), sonuc: `Ortalama ${fmt(m.mean(s) as number)} • Medyan ${fmt(m.median(s) as number)} • Std (örneklem) ${fmt(m.std(s) as unknown as number)} • Varyans ${fmt(m.variance(s) as unknown as number)} • Açıklık ${fmt(Math.max(...s) - Math.min(...s))}` };
      }
    }
    r = tl.match(/(?:c|kombinasyon)\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)/);
    if (r) return { baslik: "Kombinasyon", girdi: `C(${r[1]},${r[2]})`, sonuc: fmt(m.combinations(+r[1], +r[2])) };
    r = tl.match(/(?:p|permütasyon)\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)/);
    if (r) return { baslik: "Permütasyon", girdi: `P(${r[1]},${r[2]})`, sonuc: fmt(m.permutations(+r[1], +r[2])) };
    r = tl.match(/(obeb|ebob|okek|ekok)\D+((?:\d+\D+)+\d+)/);
    if (r) {
      const s = (r[2].match(/\d+/g) || []).map(Number);
      const obeb = /obeb|ebob/.test(r[1]);
      return { baslik: obeb ? "OBEB" : "OKEK", girdi: s.join(", "), sonuc: fmt(s.reduce((a, b) => (obeb ? m.gcd(a, b) : m.lcm(a, b)) as number)) };
    }
    // Birim çevirme (ör. "5 km to m", "100 fahrenheit to celsius")
    if (/\bto\b|\bin\b/.test(tl) && /\d/.test(tl)) {
      const v = m.evaluate(t.replace(/(\d),(\d)/g, "$1.$2"));
      return { baslik: "Birim Çevirme", girdi: t, sonuc: v.toString() };
    }
    // Saf ifade
    if (/^[\d\s+\-*/^().,%!a-zπ√²³×÷]+$/i.test(t) && /\d/.test(t) && /[+\-*/^!√²³×÷%]|sqrt|sin|cos|tan|log/.test(t)) {
      const v = m.evaluate(hazirla(t));
      if (typeof v === "number") return { baslik: "Hesaplama", girdi: t, sonuc: fmt(v) + kesir(v) };
    }
  } catch {
    return null;
  }
  return null;
}

export const sonucMd = (s: MatSonuc) => `### 🧮 ${s.baslik}\n\`${s.girdi}\`\n\n**Sonuç:** ${s.sonuc}${s.ek ? "\n\n" + s.ek : ""}`;

/** AI yanıtındaki SYMPY: satırlarını cihaz içi motorla doğrular */
export function yanitiDogrula(metin: string): string {
  const satirlar = [...(metin || "").matchAll(/^\s*`?SYMPY:\s*(.+?)`?\s*$/gim)].map((x) => x[1]);
  let temiz = (metin || "").replace(/^\s*`?SYMPY:.*$\n?/gim, "").replace(/^#+[^\n]*doğrulama satır[^\n]*$/gim, "").replace(/(?:\n\s*---\s*)+$/, "").trimEnd();
  if (!satirlar.length) return temiz;
  const d = satirlar.slice(0, 8).map((s, i) => {
    const r = coz(s);
    return `**${i + 1}.** \`${s}\` → ${r ? "**" + r.sonuc + "**" : "otomatik doğrulanamadı (sözel/şekilli soru)"}`;
  });
  return temiz + "\n\n---\n### ✅ Cihaz içi matematik doğrulaması\n_Yapay zekâdan bağımsız yeniden hesaplandı; farklıysa bu sonuç esas alınmalı._\n\n" + d.join("\n\n");
}

export const SYMPY_KURALI = "\n\nÖNEMLİ — DOĞRULAMA SATIRI: Görselde matematik sorusu varsa cevabının EN SONUNA her soru için ayrı satırda `SYMPY: <ifade>` yaz (ör. `SYMPY: 3x+7=22`, `SYMPY: x^3-6x^2+11x-6=0`, `SYMPY: x+y=5, x-y=1`, `SYMPY: türev x^2*sin(x)`, `SYMPY: 0'dan 2'ye integral x^2`, `SYMPY: (3/4+1/2)*8`). Matematik sorusu yoksa yazma.";
