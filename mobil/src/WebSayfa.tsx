// AREX — gömülü HTML sayfası: telefonda WebView (mikrofon/kamera izinli), web/masaüstünde iframe
import React, { useEffect, useRef } from "react";
import { Platform, View } from "react-native";

type Props = { html: string; ayar?: Record<string, unknown>; onMesaj?: (veri: any) => void };

function enjekte(html: string, ayar?: Record<string, unknown>) {
  if (!ayar) return html;
  const js = `<script>window.AREX_CANLI=${JSON.stringify(ayar).replace(/</g, "\\u003c")};</script>`;
  return html.replace("<head>", "<head>" + js);
}

export default function WebSayfa({ html, ayar, onMesaj }: Props) {
  const kaynak = enjekte(html, ayar);
  if (Platform.OS === "web") return <IframeSayfa html={kaynak} onMesaj={onMesaj} />;
  const { WebView } = require("react-native-webview");
  return (
    <WebView
      originWhitelist={["*"]}
      source={{ html: kaynak, baseUrl: "https://arex.local/" }}
      javaScriptEnabled
      domStorageEnabled
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
      mediaCapturePermissionGrantType="grant"
      allowFileAccess
      setSupportMultipleWindows={false}
      style={{ flex: 1, backgroundColor: "#050816" }}
      onMessage={(e: any) => { try { onMesaj?.(JSON.parse(e.nativeEvent.data)); } catch {} }}
    />
  );
}

function IframeSayfa({ html, onMesaj }: { html: string; onMesaj?: (v: any) => void }) {
  const ref = useRef<any>(null);
  useEffect(() => {
    const dinle = (e: MessageEvent) => {
      if (e.source !== ref.current?.contentWindow) return;
      try { onMesaj?.(JSON.parse(String(e.data))); } catch {}
    };
    window.addEventListener("message", dinle);
    return () => window.removeEventListener("message", dinle);
  }, [onMesaj]);
  return (
    <View style={{ flex: 1 }}>
      {React.createElement("iframe", {
        ref, srcDoc: html, allow: "microphone; camera; autoplay; display-capture; clipboard-write",
        style: { border: 0, width: "100%", height: "100%", background: "#050816" },
      })}
    </View>
  );
}
