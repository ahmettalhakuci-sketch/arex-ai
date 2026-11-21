// AREX — Android "Dijital asistan" eklentisi: yan tuşa / ana ekran tuşuna basılı tutunca (ACTION_ASSIST)
// küçük bir köprü aktivite AREX'i arex://asistan derin bağlantısıyla açar (altta mini Canlı paneli).
const { withAndroidManifest, withDangerousMod } = require("@expo/config-plugins");
const fs = require("fs");
const path = require("path");

const KOTLIN = (paket) => `package ${paket}

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle

/** Asistan tuşu (ACTION_ASSIST / VOICE_COMMAND) → AREX mini Canlı paneli */
class AsistanActivity : Activity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val hedef = Intent(Intent.ACTION_VIEW, Uri.parse("arex://asistan"), this, MainActivity::class.java)
    hedef.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP)
    startActivity(hedef)
    finish()
    overridePendingTransition(0, 0)
  }
}
`;

module.exports = function asistanEklentisi(config) {
  config = withAndroidManifest(config, (c) => {
    const app = c.modResults.manifest.application[0];
    app.activity = (app.activity || []).filter((a) => a.$["android:name"] !== ".AsistanActivity");
    app.activity.push({
      $: { "android:name": ".AsistanActivity", "android:exported": "true", "android:label": "AREX AI",
        "android:theme": "@android:style/Theme.Translucent.NoTitleBar", "android:excludeFromRecents": "true", "android:noHistory": "true" },
      "intent-filter": [
        { action: [{ $: { "android:name": "android.intent.action.ASSIST" } }], category: [{ $: { "android:name": "android.intent.category.DEFAULT" } }] },
        { action: [{ $: { "android:name": "android.intent.action.VOICE_COMMAND" } }], category: [{ $: { "android:name": "android.intent.category.DEFAULT" } }] },
      ],
    });
    return c;
  });
  config = withDangerousMod(config, ["android", async (c) => {
    const paket = c.android?.package || "com.arex.ai";
    const klasor = path.join(c.modRequest.platformProjectRoot, "app", "src", "main", "java", ...paket.split("."));
    fs.mkdirSync(klasor, { recursive: true });
    fs.writeFileSync(path.join(klasor, "AsistanActivity.kt"), KOTLIN(paket));
    return c;
  }]);
  return config;
};
