// AREX — Android "Dijital asistan" eklentisi: yan tuşa / ana ekran tuşuna basılı tutunca (ACTION_ASSIST / VOICE_COMMAND)
// AREX tam ekran AÇILMAZ. Gemini gibi: kendi görev yığınında (taskAffinity) şeffaf bir ReactActivity açılır,
// o an kullanılan uygulama arkada görünür kalır ve alttan yüzen asistan kartı ("asistan" kök bileşeni) gösterilir.
const { withAndroidManifest, withAndroidStyles, withDangerousMod } = require("@expo/config-plugins");
const fs = require("fs");
const path = require("path");

const TEMA = "Theme.AREX.Asistan";

const KOTLIN = (paket) => `package ${paket}

import android.os.Bundle
import com.facebook.react.ReactActivity
import com.facebook.react.ReactActivityDelegate
import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint.fabricEnabled
import com.facebook.react.defaults.DefaultReactActivityDelegate
import expo.modules.ReactActivityDelegateWrapper

/** Asistan tuşu → arkadaki uygulamanın üstünde şeffaf pencerede AREX asistan kartı (Gemini tarzı) */
class AsistanActivity : ReactActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(null)
    overridePendingTransition(0, 0)
  }

  override fun getMainComponentName(): String = "asistan"

  override fun createReactActivityDelegate(): ReactActivityDelegate {
    return ReactActivityDelegateWrapper(
      this,
      BuildConfig.IS_NEW_ARCHITECTURE_ENABLED,
      object : DefaultReactActivityDelegate(this, mainComponentName, fabricEnabled) {}
    )
  }

  /** Geri tuşu / JS'ten kapat: yalnız bu pencere kapanır, ana uygulama öne gelmez */
  override fun invokeDefaultOnBackPressed() {
    finish()
  }

  override fun finish() {
    super.finish()
    overridePendingTransition(0, 0)
  }

  /** Ana AREX (⤢ büyüt) ya da başka uygulama öne gelince bu pencere görünmez olur → güvenle kapan */
  override fun onStop() {
    super.onStop()
    if (!isFinishing) finish()
  }

  /** Ana ekrana / başka uygulamaya geçilince kart açık kalmasın */
  override fun onUserLeaveHint() {
    super.onUserLeaveHint()
    finish()
  }
}
`;

module.exports = function asistanEklentisi(config) {
  config = withAndroidStyles(config, (c) => {
    const res = c.modResults.resources;
    res.style = (res.style || []).filter((s) => s.$.name !== TEMA);
    const oge = (ad, deger) => ({ $: { name: ad }, _: deger });
    res.style.push({
      $: { name: TEMA, parent: "Theme.AppCompat.DayNight.NoActionBar" },
      item: [
        oge("android:windowIsTranslucent", "true"),
        oge("android:windowBackground", "@android:color/transparent"),
        oge("android:windowNoTitle", "true"),
        oge("android:backgroundDimEnabled", "false"),
        oge("android:windowAnimationStyle", "@null"),
        oge("android:windowContentOverlay", "@null"),
        oge("android:statusBarColor", "@android:color/transparent"),
        oge("android:navigationBarColor", "@android:color/transparent"),
        oge("android:windowDrawsSystemBarBackgrounds", "true"),
        oge("android:editTextBackground", "@drawable/rn_edit_text_material"),
      ],
    });
    return c;
  });
  config = withAndroidManifest(config, (c) => {
    const app = c.modResults.manifest.application[0];
    app.activity = (app.activity || []).filter((a) => a.$["android:name"] !== ".AsistanActivity");
    app.activity.push({
      $: {
        "android:name": ".AsistanActivity", "android:exported": "true", "android:label": "AREX AI",
        "android:theme": "@style/" + TEMA,
        "android:taskAffinity": "com.arex.ai.asistan",
        "android:launchMode": "singleTask",
        "android:excludeFromRecents": "true",
        "android:noHistory": "true",
        "android:windowSoftInputMode": "adjustResize",
        "android:configChanges": "keyboard|keyboardHidden|orientation|screenSize|screenLayout|uiMode|smallestScreenSize",
      },
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
