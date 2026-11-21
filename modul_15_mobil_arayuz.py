# -*- coding: utf-8 -*-
"""
==============================================================================
AREX AI STUDIO — MODÜL 15: MOBİL PREMIUM ARAYÜZ, AÇILIŞ KAPAĞI VE PWA
(modul_15_mobil_arayuz.py)
==============================================================================
  • kapak_ekrani_goster()  : Oturum başına bir kez, animasyonlu tam ekran açılış kapağı
  • pwa_baglantilarini_ekle(): Android "Ana ekrana ekle" → adres çubuksuz, tam ekran uygulama
  • mobil_stilleri_yukle()  : Telefon öncelikli premium CSS (temanın renk değişkenlerini kullanır)
  • ust_gezinme(...)        : Üstte yapışık, yatay kaydırılabilir bölüm çubuğu

Tüm stiller Modül 1'in tanımladığı CSS değişkenlerine (--accent-primary,
--bg-surface ...) bağlıdır; 7 temanın hepsiyle uyumlu çalışır.
"""

import streamlit as st

try:
    import streamlit.components.v1 as _components
except Exception:  # pragma: no cover
    _components = None

STATIK_YOL = "app/static"  # Streamlit enableStaticServing → /app/static/...


# ------------------------------------------------------------------------------
# 1. AÇILIŞ KAPAĞI
# ------------------------------------------------------------------------------
def kapak_ekrani_goster(surum: str = "v14"):
    """İlk açılışta tam ekran animasyonlu kapak. Saf CSS: 2,6 sn sonra kendiliğinden kaybolur,
    tıklamaları engellemez ve aynı oturumda tekrar gösterilmez."""
    if st.session_state.get("_arex_kapak_gosterildi"):
        # Aynı konumda görünmez yer tutucu: sonraki öğelerin kimliği değişmesin
        # (aksi halde ilk etkileşimde açık bölümler/pencereler kendiliğinden kapanır)
        st.markdown('<span id="arex-kapak-yer" style="display:none"></span>', unsafe_allow_html=True)
        return
    st.session_state["_arex_kapak_gosterildi"] = True
    st.markdown(
        f"""
<style>
#arex-kapak {{
  position: fixed; inset: 0; z-index: 999999;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 22px;
  background:
    radial-gradient(circle at 50% 38%, rgba(56,189,248,.22), transparent 55%),
    radial-gradient(circle at 15% 90%, rgba(139,92,246,.20), transparent 50%),
    radial-gradient(circle at 90% 10%, rgba(14,165,233,.16), transparent 45%),
    linear-gradient(160deg, #020617 0%, #03091a 45%, #0b1533 100%);
  animation: arexKapakCik .7s cubic-bezier(.4,0,.2,1) 2.6s forwards;
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  overflow: hidden;
}}
#arex-kapak .ak-yildizlar {{
  position: absolute; inset: -50%;
  background-image:
    radial-gradient(1.5px 1.5px at 20% 30%, rgba(255,255,255,.7), transparent),
    radial-gradient(1px 1px at 70% 20%, rgba(255,255,255,.5), transparent),
    radial-gradient(1.2px 1.2px at 40% 80%, rgba(186,230,253,.6), transparent),
    radial-gradient(1px 1px at 85% 65%, rgba(255,255,255,.4), transparent),
    radial-gradient(1.4px 1.4px at 10% 60%, rgba(196,181,253,.6), transparent);
  background-size: 340px 340px;
  animation: arexYildiz 24s linear infinite;
  opacity: .8;
}}
#arex-kapak .ak-logo {{
  position: relative; width: 132px; height: 132px; display: grid; place-items: center;
  animation: arexBelir .9s cubic-bezier(.2,.8,.2,1) both;
}}
#arex-kapak .ak-halka {{
  position: absolute; inset: 0; border-radius: 50%;
  background: conic-gradient(from 0deg, #38bdf8, #8b5cf6, #22d3ee, #38bdf8);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 4px), #000 calc(100% - 3px));
          mask: radial-gradient(farthest-side, transparent calc(100% - 4px), #000 calc(100% - 3px));
  animation: arexDon 2.2s linear infinite;
  filter: drop-shadow(0 0 14px rgba(56,189,248,.65));
}}
#arex-kapak .ak-ic {{
  width: 104px; height: 104px; border-radius: 30px; display: grid; place-items: center;
  background: linear-gradient(145deg, rgba(15,23,42,.95), rgba(30,41,82,.95));
  border: 1px solid rgba(148,163,184,.25);
  box-shadow: 0 20px 60px rgba(56,189,248,.25), inset 0 1px 0 rgba(255,255,255,.08);
  font-weight: 800; font-size: 40px; letter-spacing: -1px;
  background-clip: padding-box;
}}
#arex-kapak .ak-ic span {{
  background: linear-gradient(135deg, #e0f2fe 0%, #38bdf8 50%, #a78bfa 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}}
#arex-kapak .ak-baslik {{
  font-size: 34px; font-weight: 800; letter-spacing: 6px; color: #f8fafc; margin: 0;
  animation: arexYukari .8s .25s cubic-bezier(.2,.8,.2,1) both;
  text-shadow: 0 0 30px rgba(56,189,248,.35);
}}
#arex-kapak .ak-baslik b {{ color: #38bdf8; font-weight: 800; }}
#arex-kapak .ak-alt {{
  margin-top: -12px; font-size: 13.5px; color: #94a3b8; letter-spacing: .4px;
  animation: arexYukari .8s .45s cubic-bezier(.2,.8,.2,1) both;
}}
#arex-kapak .ak-cubuk {{
  width: min(220px, 60vw); height: 4px; border-radius: 99px; overflow: hidden;
  background: rgba(148,163,184,.18);
  animation: arexYukari .8s .6s both;
}}
#arex-kapak .ak-cubuk i {{
  display: block; height: 100%; width: 0; border-radius: 99px;
  background: linear-gradient(90deg, #38bdf8, #8b5cf6);
  box-shadow: 0 0 12px rgba(56,189,248,.8);
  animation: arexYukle 1.9s .65s cubic-bezier(.65,0,.35,1) forwards;
}}
#arex-kapak .ak-ozellik {{
  display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; max-width: 88vw;
  animation: arexYukari .8s .8s both;
}}
#arex-kapak .ak-ozellik span {{
  font-size: 11.5px; color: #cbd5e1; padding: 5px 10px; border-radius: 99px;
  border: 1px solid rgba(148,163,184,.22); background: rgba(15,23,42,.55);
}}
#arex-kapak .ak-imza {{
  position: absolute; bottom: calc(22px + env(safe-area-inset-bottom)); font-size: 11px;
  color: #64748b; letter-spacing: 1.5px; animation: arexYukari .8s 1s both;
}}
@keyframes arexKapakCik {{ to {{ opacity: 0; visibility: hidden; transform: scale(1.04); pointer-events: none; }} }}
@keyframes arexBelir {{ from {{ opacity: 0; transform: scale(.6) rotate(-12deg); }} to {{ opacity: 1; transform: none; }} }}
@keyframes arexYukari {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes arexDon {{ to {{ transform: rotate(360deg); }} }}
@keyframes arexYukle {{ to {{ width: 100%; }} }}
@keyframes arexYildiz {{ to {{ transform: translate(340px, 340px); }} }}
@media (prefers-reduced-motion: reduce) {{
  #arex-kapak, #arex-kapak * {{ animation-duration: .01s !important; animation-delay: 0s !important; }}
  #arex-kapak {{ animation: arexKapakCik .3s 1.2s forwards !important; }}
}}
</style>
<div id="arex-kapak" aria-hidden="true">
  <div class="ak-yildizlar"></div>
  <div class="ak-logo"><div class="ak-halka"></div><div class="ak-ic"><span>RX</span></div></div>
  <p class="ak-baslik">AREX <b>AI</b></p>
  <div class="ak-alt">Akıllı asistanın hazırlanıyor…</div>
  <div class="ak-cubuk"><i></i></div>
  <div class="ak-ozellik"><span>💬 Sohbet</span><span>🧮 Matematik</span><span>🌐 Çeviri</span><span>📚 Bilgi</span><span>🌤️ Hava</span></div>
  <div class="ak-imza">AREX AI STUDIO · {surum}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------------------
# 2. PWA (Ana ekrana ekle → uygulama gibi)
# ------------------------------------------------------------------------------
def pwa_baglantilarini_ekle(tema_rengi: str = "#03091a"):
    """manifest, ikon ve tema rengini sayfanın <head> kısmına bir kez ekler."""
    if _components is None:
        return
    _components.html(
        f"""
<script>
(function() {{
  try {{
    const d = window.parent.document;
    if (d.getElementById('arex-pwa')) return;
    const ekle = (tag, attrs) => {{ const e = d.createElement(tag); Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k, v)); d.head.appendChild(e); return e; }};
    ekle('link', {{id: 'arex-pwa', rel: 'manifest', href: './{STATIK_YOL}/manifest.json'}});
    ekle('link', {{rel: 'apple-touch-icon', href: './{STATIK_YOL}/icon-192.png'}});
    ekle('meta', {{name: 'theme-color', content: '{tema_rengi}'}});
    ekle('meta', {{name: 'mobile-web-app-capable', content: 'yes'}});
    ekle('meta', {{name: 'apple-mobile-web-app-capable', content: 'yes'}});
    ekle('meta', {{name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent'}});
    ekle('meta', {{name: 'apple-mobile-web-app-title', content: 'AREX'}});
    const vp = d.querySelector('meta[name=viewport]');
    if (vp && !vp.content.includes('viewport-fit')) vp.content += ', viewport-fit=cover';
  }} catch (e) {{ /* farklı köken: sessizce geç */ }}
}})();
</script>
""",
        height=0,
    )


# ------------------------------------------------------------------------------
# 3. MOBİL PREMIUM CSS
# ------------------------------------------------------------------------------
_MOBIL_CSS = """
<style>
/* ---------- Ortak premium dokunuşlar (tüm ekranlar) ---------- */
#MainMenu, footer, [data-testid="stDecoration"], .stDeployButton, [data-testid="stAppDeployButton"],
[data-testid="stToolbarActions"], [data-testid="stStatusWidget"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; backdrop-filter: none !important; }
iframe[height="0"] { display: none; }

/* Üst gezinme çubuğu: yapışık, cam efektli (sticky, Streamlit sarmalayıcısına uygulanır) */
[data-testid="stElementContainer"]:has(> .st-key-arex_nav),
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-arex_nav),
div:has(> .st-key-arex_nav) {
  position: sticky; top: 0; z-index: 90;
}
.st-key-arex_nav {
  padding: 8px 4px 10px;
  background: linear-gradient(180deg, var(--bg-main) 75%, transparent);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
}
.st-key-arex_nav [data-testid="stButtonGroup"] > div,
.st-key-arex_nav [data-baseweb="button-group"] {
  flex-wrap: nowrap !important; overflow-x: auto; scrollbar-width: none; gap: 6px;
  -webkit-overflow-scrolling: touch; scroll-snap-type: x proximity;
}
.st-key-arex_nav [data-testid="stButtonGroup"] > div::-webkit-scrollbar,
.st-key-arex_nav [data-baseweb="button-group"]::-webkit-scrollbar { display: none; }
.st-key-arex_nav button {
  flex: 0 0 auto; scroll-snap-align: start; white-space: nowrap;
  border-radius: 999px !important; padding: 6px 14px !important; min-height: 38px;
  border: 1px solid var(--border-subtle) !important;
  background: color-mix(in srgb, var(--bg-surface) 85%, transparent) !important;
  transition: transform .15s ease, box-shadow .2s ease;
}
.st-key-arex_nav button[kind$="Active"], .st-key-arex_nav button[aria-checked="true"],
.st-key-arex_nav button[aria-pressed="true"] {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-tertiary)) !important;
  color: #fff !important; border-color: transparent !important;
  box-shadow: 0 6px 18px color-mix(in srgb, var(--accent-primary) 40%, transparent);
}
.st-key-arex_nav button:active { transform: scale(.96); }

/* Sohbet baloncukları: kullanıcı sağda, AREX solda */
[data-testid="stChatMessage"] {
  border-radius: 18px !important; padding: 10px 14px !important; margin-bottom: 8px;
  border: 1px solid var(--border-subtle);
  background: color-mix(in srgb, var(--bg-surface) 92%, transparent) !important;
  animation: arexMesaj .28s ease-out both;
}
[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
  flex-direction: row-reverse; text-align: left; margin-left: 12%;
  background: linear-gradient(135deg,
      color-mix(in srgb, var(--accent-primary) 26%, var(--bg-surface)),
      color-mix(in srgb, var(--accent-tertiary) 22%, var(--bg-surface))) !important;
  border-color: color-mix(in srgb, var(--accent-primary) 35%, transparent);
  border-bottom-right-radius: 6px !important;
}
[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
  margin-right: 6%; border-bottom-left-radius: 6px !important;
}
@keyframes arexMesaj { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

/* Sohbet giriş kutusu */
[data-testid="stChatInput"] {
  border-radius: 22px !important; border: 1px solid var(--border-subtle) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--accent-primary) !important;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent-primary) 25%, transparent), 0 10px 30px rgba(0,0,0,.35);
}
[data-testid="stChatInput"] textarea { font-size: 16px !important; }

/* Hızlı eylem kartları */
.st-key-arex_hizli button {
  border-radius: 16px !important; min-height: 48px;
  border: 1px solid var(--border-subtle) !important;
  background: color-mix(in srgb, var(--bg-surface) 90%, transparent) !important;
  transition: transform .15s ease, border-color .2s ease;
}
.st-key-arex_hizli button:hover { border-color: var(--accent-primary) !important; }
.st-key-arex_hizli button:active { transform: scale(.97); }

/* ---------- v15 Premium dokunuşlar ---------- */
/* Sohbete eklenen fotoğraf: büyük değil, Gemini gibi küçük ve yuvarlak köşeli önizleme */
.arex-kucuk-gorsel {
  display: block; max-width: min(220px, 62vw); max-height: 220px; width: auto; height: auto;
  object-fit: cover; border-radius: 16px; margin: 4px 0 6px auto;
  border: 1px solid color-mix(in srgb, var(--accent-primary) 35%, transparent);
  box-shadow: 0 8px 22px rgba(0,0,0,.35);
}
/* Yazı kutusundaki ek önizlemesi de küçük kalsın, kutu zıplamasın */
[data-testid="stChatInput"] [data-testid^="stChatInputFile"] img,
[data-testid="stChatInput"] img { max-height: 56px !important; width: auto !important; border-radius: 10px; }
[data-testid="stChatInput"] [data-testid^="stChatInputFile"] { max-width: 180px; }
/* Kaydırma: içerik eklenince sayfa yukarı-aşağı sıçramasın */
.st-key-arex_sohbet { overflow-anchor: auto; overscroll-behavior: contain; scroll-behavior: smooth; }
.st-key-arex_sohbet > div { overflow-anchor: none; }
/* Cam efekti ve yumuşak gölgeler */
[data-testid="stChatMessage"] { backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 6px 20px rgba(0,0,0,.22); }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { line-height: 1.62; }
[data-testid="stChatInput"] { backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); }
/* Gömülü canlı sohbet çerçevesi */
iframe[title="st.iframe"], [data-testid="stIFrame"], .stIFrame { border-radius: 24px; border: 0;
  box-shadow: 0 18px 50px rgba(0,0,0,.45); }
/* Sekmeler: hap görünümü */
[data-baseweb="tab-list"] { gap: 6px; }
[data-baseweb="tab"] { border-radius: 999px !important; }
[data-baseweb="tab"][aria-selected="true"] {
  background: color-mix(in srgb, var(--accent-primary) 18%, transparent) !important; }
[data-baseweb="tab-highlight"] { display: none !important; }
/* Genişleticiler (expander) kart görünümü */
[data-testid="stExpander"] details { border-radius: 16px !important; border: 1px solid var(--border-subtle) !important; }

/* ---------- v15.2: yeni öğeler (mevcut görünüme dokunmadan) ---------- */
/* Sohbet penceresi ekran yüksekliğine uyar (kısa ekranlarda ilk mesaj menünün altında kalmasın) */
.st-key-arex_sohbet { height: min(525px, calc(100dvh - 360px)) !important; min-height: 260px; }
.arex-mesaj-alt { display:flex; flex-wrap:wrap; align-items:center; gap:6px; margin-top:4px; }
.arex-kaynak { font-size:11px; padding:3px 8px; border-radius:999px; border:1px solid var(--border-subtle);
  color: inherit !important; text-decoration:none !important; opacity:.75; white-space:nowrap; max-width:60vw; overflow:hidden; text-overflow:ellipsis; }
.arex-motor { font-size:11px; opacity:.5; margin-left:auto; }
.arex-gecmis-grup { font-size:11px; font-weight:700; letter-spacing:.6px; text-transform:uppercase; opacity:.55; margin:8px 2px 2px; }

/* ---------- Telefon (≤ 768px) ---------- */
@media (max-width: 768px) {
  html { -webkit-text-size-adjust: 100%; }
  .block-container, [data-testid="stMainBlockContainer"] {
    padding: 0.4rem 0.7rem calc(5.5rem + env(safe-area-inset-bottom)) !important;
    max-width: 100% !important;
  }
  h1 { font-size: 1.45rem !important; } h2 { font-size: 1.25rem !important; } h3 { font-size: 1.1rem !important; }

  /* Başlık bandını sadeleştir */
  .premium-header { padding: 10px 14px !important; margin-bottom: 6px !important; border-radius: 16px !important; }
  .premium-header-title { font-size: 1.05rem !important; }
  .premium-header-badge { display: none !important; }

  /* Hızlı eylemler: 2 × 2 ızgara */
  .st-key-arex_hizli [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 8px !important; }
  .st-key-arex_hizli [data-testid="stColumn"], .st-key-arex_hizli [data-testid="column"] {
    flex: 1 1 calc(50% - 8px) !important; min-width: calc(50% - 8px) !important; width: auto !important;
  }
  .st-key-arex_hizli button p { font-size: 13px !important; }

  /* Sohbet penceresi ekran boyunu kullansın */
  .st-key-arex_sohbet {
    height: calc(100dvh - 255px) !important; max-height: none !important; min-height: 300px;
    border-radius: 18px !important;
  }
  [data-testid="stChatMessage"] { padding: 8px 11px !important; }
  [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) { margin-left: 8%; }
  [data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) { margin-right: 0; }
  [data-testid="stChatMessageAvatarCustom"], [data-testid^="stChatMessageAvatar"] { width: 28px; height: 28px; }

  /* Giriş kutusu: alt kenara yapışık, çentik/gezinme çubuğu boşluğu */
  [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {
    padding: 8px 10px calc(10px + env(safe-area-inset-bottom)) !important;
  }

  /* Dokunmatik hedefler en az 44px */
  .stButton button, .stDownloadButton button, [data-testid="stBaseButton-secondary"],
  [data-testid="stBaseButton-primary"] { min-height: 44px; }
  input, textarea, select, [data-baseweb="select"] * { font-size: 16px !important; }

  /* Sekmeler yatay kaydırılsın */
  [data-baseweb="tab-list"] { overflow-x: auto !important; flex-wrap: nowrap !important; scrollbar-width: none; }
  [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
  [data-baseweb="tab"] { flex: 0 0 auto !important; white-space: nowrap; padding: 8px 12px !important; }

  /* Yan menü (ayarlar) mobilde tam genişlik çekmece */
  section[data-testid="stSidebar"][aria-expanded="true"] { width: 86vw !important; min-width: 86vw !important; }
  /* Gezinme çubuğu, sol üstteki menü (☰) düğmesinin yanında dursun */
  .st-key-arex_nav { padding-left: 46px !important; }
  header[data-testid="stHeader"] { height: 3.2rem !important; background: transparent !important; border-bottom: 0 !important; }
  /* Mesaj altı saat/etiket satırı küçük ve tek satır */
  [data-testid="stChatMessage"] [data-testid="stCaptionContainer"] p,
  [data-testid="stChatMessage"] .stCaption p {
    font-size: 11px !important; line-height: 1.3 !important; opacity: .75;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  [data-testid="stChatInput"] textarea::placeholder { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  /* Geniş tablolar/kod taşmasın */
  [data-testid="stMarkdownContainer"] pre, [data-testid="stMarkdownContainer"] table {
    display: block; max-width: 100%; overflow-x: auto;
  }
  [data-testid="stMarkdownContainer"] code { word-break: break-word; }
}
</style>
"""


def mobil_stilleri_yukle():
    st.markdown(_MOBIL_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 4. ÜST GEZİNME ÇUBUĞU
# ------------------------------------------------------------------------------
def ust_gezinme(bolumler: dict, varsayilan: str) -> str:
    """bolumler: {kisa_etiket: tam_bolum_adi}. Seçili tam bölüm adını döndürür.
    Seçim kaldırılırsa (aynı hapa tekrar dokunma) önceki bölümde kalır."""
    onceki = st.session_state.get("_arex_aktif_bolum", varsayilan)
    kisa_onceki = next((k for k, v in bolumler.items() if v == onceki), next(iter(bolumler)))
    if "arex_nav_secim" in st.session_state and st.session_state["arex_nav_secim"] is None:
        st.session_state["arex_nav_secim"] = kisa_onceki  # boş seçimi geri al
    with st.container(key="arex_nav"):
        secim_fn = getattr(st, "pills", None) or getattr(st, "segmented_control", None)
        # ÖNEMLİ: 'default' her çalıştırmada AYNI olmalı. Değişirse Streamlit bunu yeni bir widget sayar,
        # sıfırlar ve o anda yapılan dokunuş kaybolur (bölüm değiştikten sonraki ilk tıklama işlemezdi).
        # Güncel seçim zaten key="arex_nav_secim" ile oturumda tutulur.
        kisa_varsayilan = next((k for k, v in bolumler.items() if v == varsayilan), next(iter(bolumler)))
        if "arex_nav_secim" not in st.session_state:
            st.session_state["arex_nav_secim"] = kisa_onceki
        if secim_fn is not None:
            secim = secim_fn("Bölüm", list(bolumler), default=kisa_varsayilan,
                             label_visibility="collapsed", key="arex_nav_secim")
        else:  # çok eski Streamlit
            secim = st.radio("Bölüm", list(bolumler), index=list(bolumler).index(kisa_varsayilan),
                             horizontal=True, label_visibility="collapsed", key="arex_nav_secim")
    tam = bolumler.get(secim) if secim else onceki
    st.session_state["_arex_aktif_bolum"] = tam
    return tam
