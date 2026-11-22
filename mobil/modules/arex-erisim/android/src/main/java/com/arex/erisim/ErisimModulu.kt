package com.arex.erisim

import android.accessibilityservice.AccessibilityService
import android.content.ComponentName
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.PowerManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.accessibility.AccessibilityNodeInfo
import android.view.accessibility.AccessibilityWindowInfo
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition
import java.text.Normalizer
import java.util.Locale

class ErisimModulu : Module() {
  private val ctx get() = appContext.reactContext!!
  private val tr = Locale.forLanguageTag("tr")
  private fun sade(s: String) = Normalizer.normalize(s.lowercase(tr), Normalizer.Form.NFD).replace(Regex("\\p{M}"), "").replace("ı", "i").trim()

  /** Kullanıcının baktığı UYGULAMA penceresi (klavye, sistem çubukları ve AREX'in kendi asistan kartı hariç).
   *  Yalnız AREX açıksa null → "okunacak başka uygulama yok". */
  private fun kok(): AccessibilityNodeInfo? {
    val s = ArexErisimServisi.ornek ?: return null
    val uygulamalar = s.windows.filter { it.type == AccessibilityWindowInfo.TYPE_APPLICATION }
      .mapNotNull { w -> w.root?.let { w to it } }
      .filter { it.second.packageName?.toString() != ctx.packageName }
    val sec = uygulamalar.firstOrNull { it.first.isFocused } ?: uygulamalar.firstOrNull { it.first.isActive } ?: uygulamalar.firstOrNull()
    if (sec != null) return sec.second
    val aktif = s.rootInActiveWindow ?: return null
    return if (aktif.packageName?.toString() == ctx.packageName) null else aktif
  }

  private fun eylemKodu(eylem: String): Int? = when (eylem) {
    "geri" -> AccessibilityService.GLOBAL_ACTION_BACK
    "ana" -> AccessibilityService.GLOBAL_ACTION_HOME
    "son" -> AccessibilityService.GLOBAL_ACTION_RECENTS
    "bildirim" -> AccessibilityService.GLOBAL_ACTION_NOTIFICATIONS
    "hizli" -> AccessibilityService.GLOBAL_ACTION_QUICK_SETTINGS
    "kilit" -> AccessibilityService.GLOBAL_ACTION_LOCK_SCREEN
    "ekranGoruntusu" -> AccessibilityService.GLOBAL_ACTION_TAKE_SCREENSHOT
    else -> null
  }

  private fun bilesen() = ComponentName(ctx.packageName, "com.arex.erisim.ArexErisimServisi").flattenToString()
  private fun ayardaAcik(): Boolean {
    val liste = Settings.Secure.getString(ctx.contentResolver, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES) ?: return false
    val b = bilesen(); val kisa = ctx.packageName + "/com.arex.erisim.ArexErisimServisi"
    return liste.split(":").any { it.equals(b, true) || it.equals(kisa, true) }
  }

  /** Ekranda (kullanıcının baktığı uygulamada) yazısı/açıklaması eşleşen öğeye dokunur; tam eşleşme önceliklidir */
  private fun tiklaIc(metin: String): Boolean {
      val r = kok() ?: return false
      val q = sade(metin)
      var aday: AccessibilityNodeInfo? = null
      var tam: AccessibilityNodeInfo? = null
      gez(r) { n ->
        val t = sade((n.text ?: n.contentDescription)?.toString() ?: "")
        if (t.isNotEmpty() && n.isVisibleToUser) {
          if (t == q && tam == null) tam = n
          else if (t.contains(q) && aday == null) aday = n
        }
      }
      val h = tiklanabilir(tam ?: aday) ?: return false
      return h.performAction(AccessibilityNodeInfo.ACTION_CLICK)
      }

  private fun gez(n: AccessibilityNodeInfo?, f: (AccessibilityNodeInfo) -> Unit) {
    if (n == null) return
    f(n)
    for (i in 0 until n.childCount) gez(n.getChild(i), f)
  }

  private fun tiklanabilir(n: AccessibilityNodeInfo?): AccessibilityNodeInfo? {
    var x = n
    while (x != null && !x.isClickable) x = x.parent
    return x
  }

  override fun definition() = ModuleDefinition {
    Name("ArexErisim")

    Function("etkinMi") { ArexErisimServisi.ornek != null }

    Function("ayarlariAc") {
      ctx.startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    }

    /** İzin ayar sayfalarını doğrudan açar; özel sayfa yoksa en yakın genel sayfaya düşer */
    Function("ayarAc") { tur: String ->
      val pkt = ctx.packageName
      val uyg = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$pkt"))
      val adaylar: List<Intent> = when (tur) {
        "erisim" -> listOf(
          Intent("android.settings.ACCESSIBILITY_DETAILS_SETTINGS").putExtra(Intent.EXTRA_COMPONENT_NAME, ComponentName(pkt, "com.arex.erisim.ArexErisimServisi").flattenToString()),
          Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
        "uygulama" -> listOf(uyg)
        "bildirim" -> listOf(Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(Settings.EXTRA_APP_PACKAGE, pkt), uyg)
        "pil" -> listOf(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS), uyg)
        "asistan" -> listOf(Intent(Settings.ACTION_VOICE_INPUT_SETTINGS), Intent("android.settings.MANAGE_DEFAULT_APPS_SETTINGS"), Intent(Settings.ACTION_SETTINGS))
        "kurulum" -> listOf(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES), Intent(Settings.ACTION_SECURITY_SETTINGS))
        "guvenlik" -> listOf(Intent(Settings.ACTION_SECURITY_SETTINGS), Intent(Settings.ACTION_SETTINGS))
        "ustte" -> listOf(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$pkt")), uyg)
        else -> listOf(uyg)
      }
      for (i in adaylar) {
        try { ctx.startActivity(i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); return@Function true } catch (_: Exception) {}
      }
      false
    }

    /** İzin durumları: pil muafiyeti, varsayılan asistan */
    Function("durumlar") {
      val pm = ctx.getSystemService(android.content.Context.POWER_SERVICE) as PowerManager
      val asistan = try { Settings.Secure.getString(ctx.contentResolver, "assistant") ?: "" } catch (_: Exception) { "" }
      mapOf(
        "erisim" to (ArexErisimServisi.ornek != null),
        "pil" to pm.isIgnoringBatteryOptimizations(ctx.packageName),
        "asistan" to asistan.contains(ctx.packageName),
        "asistanBiliniyor" to asistan.isNotEmpty()
      )
    }

    /** Yan tuş penceresini kart yüksekliğine göre boyutlandırır (AsistanActivity.pencereBoyu, yansıma ile — paket bağımlılığı yok) */
    Function("pencereBoyu") { dp: Int ->
      val a = appContext.currentActivity ?: return@Function false
      if (!a.javaClass.name.endsWith("AsistanActivity")) return@Function false
      try { a.javaClass.getMethod("pencereBoyu", Int::class.javaPrimitiveType).invoke(a, dp); true } catch (_: Exception) { false }
    }

    /** Rehberde ada göre kişi arar (Türkçe harf/ek duyarsız): "baba" → "Babam", "Baba 💙" … En iyi 5 eşleşme. */
    Function("kisiBul") { ad: String ->
      if (ctx.checkSelfPermission(android.Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED) return@Function listOf<Map<String, String>>()
      val q = sade(ad).replace(Regex("[^a-z0-9 ]"), "").trim()
      if (q.isEmpty()) return@Function listOf<Map<String, String>>()
      val sonuc = ArrayList<Triple<Int, String, String>>()
      val c = ctx.contentResolver.query(android.provider.ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
        arrayOf(android.provider.ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, android.provider.ContactsContract.CommonDataKinds.Phone.NUMBER), null, null, null)
      c?.use {
        while (it.moveToNext()) {
          val isim = it.getString(0) ?: continue; val no = it.getString(1) ?: continue
          val s = sade(isim).replace(Regex("[^a-z0-9 ]"), "").trim()
          val puan = when { s == q -> 100; s.startsWith(q) && s.length - q.length <= 2 -> 90; s.split(" ").any { w -> w == q } -> 80; s.startsWith(q) -> 70; s.contains(q) -> 50; else -> 0 }
          if (puan > 0) sonuc.add(Triple(puan, isim, no))
        }
      }
      sonuc.sortedWith(compareByDescending<Triple<Int, String, String>> { it.first }.thenBy { it.second.length })
        .distinctBy { it.third.replace(Regex("[^0-9+]"), "") }.take(5).map { mapOf("ad" to it.second, "numara" to it.third) }
    }

    /** Numarayı arar: CALL_PHONE izni varsa doğrudan arar, yoksa çevirici numarayla açılır */
    Function("ara") { numara: String ->
      val uri = Uri.parse("tel:" + numara.replace(Regex("[^0-9+]"), ""))
      val dogrudan = ctx.checkSelfPermission(android.Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED
      ctx.startActivity(Intent(if (dogrudan) Intent.ACTION_CALL else Intent.ACTION_DIAL, uri).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
      dogrudan
    }

    /** WhatsApp'ta kişinin sohbetini mesaj YAZILMIŞ olarak açar (gönder tuşu kullanıcıda) */
    Function("whatsapp") { numara: String, metin: String ->
      val no = numara.replace(Regex("[^0-9]"), "").let { if (it.startsWith("0")) "90" + it.substring(1) else if (it.length == 10) "90$it" else it }
      val i = Intent(Intent.ACTION_VIEW, Uri.parse("https://api.whatsapp.com/send?phone=$no&text=" + Uri.encode(metin))).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      val pm = ctx.packageManager
      val paket = listOf("com.whatsapp", "com.whatsapp.w4b").firstOrNull { p -> try { pm.getPackageInfo(p, 0); true } catch (_: Exception) { false } }
      if (paket != null) i.setPackage(paket)
      ctx.startActivity(i); paket != null
    }

    /** SMS uygulamasını kişi + metinle açar */
    Function("sms") { numara: String, metin: String ->
      ctx.startActivity(Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:" + numara.replace(Regex("[^0-9+]"), ""))).putExtra("sms_body", metin).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); true
    }

    /** Servisi olmadan asılı kalmış medya bildirimini (expo_audio_channel) siler — açılışta, hiçbir şey çalmıyorken */
    Function("medyaBildirimTemizle") {
      val nm = ctx.getSystemService(android.content.Context.NOTIFICATION_SERVICE) as android.app.NotificationManager
      var n = 0
      for (b in nm.activeNotifications) if (b.notification.channelId == "expo_audio_channel") { nm.cancel(b.tag, b.id); n++ }
      n
    }

    // ---------- "AREX" uyandırma + ses imzası ----------
    /** Ekran kilitli mi (kilit ekranı gösteriliyor mu) */
    Function("ekranKilitli") { (ctx.getSystemService(android.content.Context.KEYGUARD_SERVICE) as android.app.KeyguardManager).isKeyguardLocked }
    /** Kilit ekranını kaldırma isteği: PIN/parmak izi/yüz sorar (Android'in kendi ekranı) → true: açıldı */
    AsyncFunction("kilidiKaldir") { p: expo.modules.kotlin.Promise ->
      val a = appContext.currentActivity
      val km = ctx.getSystemService(android.content.Context.KEYGUARD_SERVICE) as android.app.KeyguardManager
      if (a == null || !km.isKeyguardLocked) { p.resolve(!km.isKeyguardLocked); return@AsyncFunction }
      a.runOnUiThread {
        km.requestDismissKeyguard(a, object : android.app.KeyguardManager.KeyguardDismissCallback() {
          override fun onDismissSucceeded() { p.resolve(true) }
          override fun onDismissCancelled() { p.resolve(false) }
          override fun onDismissError() { p.resolve(false) }
        })
      }
    }
    // ---------- ⏰ Saat / sayaç / alarm (telefonun Saat uygulaması; ekran açmadan kurar) ----------
    Function("sayac") { saniye: Int, etiket: String ->
      ctx.startActivity(Intent(android.provider.AlarmClock.ACTION_SET_TIMER).putExtra(android.provider.AlarmClock.EXTRA_LENGTH, saniye)
        .putExtra(android.provider.AlarmClock.EXTRA_MESSAGE, etiket).putExtra(android.provider.AlarmClock.EXTRA_SKIP_UI, true).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); true
    }
    Function("alarm") { saat: Int, dakika: Int, etiket: String ->
      ctx.startActivity(Intent(android.provider.AlarmClock.ACTION_SET_ALARM).putExtra(android.provider.AlarmClock.EXTRA_HOUR, saat).putExtra(android.provider.AlarmClock.EXTRA_MINUTES, dakika)
        .putExtra(android.provider.AlarmClock.EXTRA_MESSAGE, etiket).putExtra(android.provider.AlarmClock.EXTRA_SKIP_UI, true).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); true
    }
    Function("alarmlariGoster") { ctx.startActivity(Intent(android.provider.AlarmClock.ACTION_SHOW_ALARMS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); true }
    /** Tanımadığım sesin kaç kez "AREX" dediği */
    Function("yabanciDurum") { val (n, t) = SesAyar.yabanci(ctx); mapOf("sayi" to n, "son" to t) }
    Function("uyanmaBaslat") { SesAyar.otomatikYaz(ctx, true); UyanmaServisi.baslat(ctx); true }
    Function("uyanmaDurdur") { SesAyar.otomatikYaz(ctx, false); UyanmaServisi.durdur(ctx); true }
    /** Açılışta: kullanıcı açtıysa servisi yeniden başlat */
    Function("uyanmaSurdur") { if (SesAyar.otomatik(ctx) && !UyanmaServisi.calisiyor) { try { UyanmaServisi.baslat(ctx) } catch (_: Exception) {} }; SesAyar.otomatik(ctx) }
    Function("uyanmaDurum") { mapOf("acik" to SesAyar.otomatik(ctx), "calisiyor" to UyanmaServisi.calisiyor, "imzaVar" to (SesAyar.imza(ctx) != null), "yenidenKayit" to SesAyar.eskiImzaVar(ctx), "esik" to (SesAyar.imza(ctx)?.second ?: 0.0), "yabanciSayi" to SesAyar.yabancilar(ctx).size,
      "ustteGoster" to (Build.VERSION.SDK_INT < 23 || Settings.canDrawOverlays(ctx))) }
    /** Son uyanma bilgisini bir kez verir (kart açılınca: sahip mi?) */
    Function("sonUyanma") { val j = UyanmaServisi.sonUyanma; UyanmaServisi.sonUyanma = null
      if (j == null) null else mapOf("zaman" to j.optLong("zaman"), "sahip" to j.optBoolean("sahip"), "seviye" to j.optInt("seviye", if (j.optBoolean("sahip")) 2 else 0), "benzerlik" to j.optDouble("benzerlik"), "imzaVar" to j.optBoolean("imzaVar")) }
    /** Kart kapanınca dinlemeye devam */
    Function("uyanmaDevam") { UyanmaServisi.duraklat = false; true }
    /** Uygulama mikrofonu kullanırken (Canlı, sesle yazma) "AREX" dinlemeyi duraklat */
    Function("uyanmaDuraklat") { b: Boolean -> UyanmaServisi.duraklat = b; true }

    /** Ses imzası için 'saniye' kadar kayıt alır (uyanma servisini geçici durdurur) → {vektor, metin, ses} */
    AsyncFunction("imzaOrnek") { saniye: Int, etiket: String ->
      if (ctx.checkSelfPermission(android.Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) return@AsyncFunction mapOf("hata" to "mikrofon izni yok")
      val eskiDuraklat = UyanmaServisi.duraklat; UyanmaServisi.duraklat = true
      Thread.sleep(350)
      try {
        val rec = org.vosk.Recognizer(SesModelleri.model(ctx), 16000f).apply { setSpeakerModel(SesModelleri.spk(ctx)) }
        val min = android.media.AudioRecord.getMinBufferSize(16000, android.media.AudioFormat.CHANNEL_IN_MONO, android.media.AudioFormat.ENCODING_PCM_16BIT)
        val ar = android.media.AudioRecord(android.media.MediaRecorder.AudioSource.VOICE_RECOGNITION, 16000, android.media.AudioFormat.CHANNEL_IN_MONO, android.media.AudioFormat.ENCODING_PCM_16BIT, maxOf(min, 32000))
        val buf = ShortArray(1600); var top = 0; var tepe = 0.0
        val tum = java.io.ByteArrayOutputStream()
        val ornekler = ArrayList<Short>(saniye * 16000)
        ar.startRecording()
        val bitis = android.os.SystemClock.elapsedRealtime() + saniye * 1000L
        while (android.os.SystemClock.elapsedRealtime() < bitis) {
          val n = ar.read(buf, 0, buf.size); if (n <= 0) continue
          var t = 0.0; for (k in 0 until n) t += buf[k].toDouble() * buf[k]; tepe = maxOf(tepe, kotlin.math.sqrt(t / n)); top += n
          rec.acceptWaveForm(buf, n)
          for (k in 0 until n) { tum.write(buf[k].toInt() and 0xff); tum.write((buf[k].toInt() shr 8) and 0xff) }
          for (k in 0 until n) ornekler.add(buf[k])
        }
        ar.stop(); ar.release()
        // Model karşılaştırması için kayıt (yalnız bu telefonda: Android/data/com.arex.ai/files/ses) — 16 kHz mono WAV
        try {
          val dir = java.io.File(ctx.getExternalFilesDir(null), "ses").apply { mkdirs() }
          val pcm = tum.toByteArray()
          val f = java.io.File(dir, "${System.currentTimeMillis()}_${etiket.replace(Regex("[^a-z0-9]"), "")}.wav")
          java.io.FileOutputStream(f).use { o ->
            val bb = java.nio.ByteBuffer.allocate(44).order(java.nio.ByteOrder.LITTLE_ENDIAN)
            bb.put("RIFF".toByteArray()).putInt(36 + pcm.size).put("WAVE".toByteArray()).put("fmt ".toByteArray()).putInt(16).putShort(1).putShort(1)
              .putInt(16000).putInt(32000).putShort(2).putShort(16).put("data".toByteArray()).putInt(pcm.size)
            o.write(bb.array()); o.write(pcm)
          }
        } catch (_: Exception) {}
        val j = org.json.JSONObject(rec.finalResult); rec.close()
        // Güçlü model (3D-Speaker ERes2Net) ile imza — Vosk'unki yalnız yedek değil, artık kullanılmıyor
        val g = GucluImza.vektor(ctx, ornekler.toShortArray())
        mapOf("vektor" to g?.toList(), "metin" to j.optString("text"), "ses" to tepe)
      } finally { UyanmaServisi.duraklat = eskiDuraklat }
    }

    /** Örneklerden imza oluştur: tüm örnekler saklanır; eşik "birini çıkar, kalanlarla karşılaştır" ile kendi sesinin tutarlılığından */
    Function("imzaKaydet") { orn: List<List<Double>> ->
      val l = orn.map { it.toDoubleArray() }.filter { it.isNotEmpty() }
      if (l.size < 3) return@Function mapOf("hata" to "en az 3 örnek gerekli")
      val ort = SesImza.ortalama(l)
      val loo = l.indices.map { i -> l.filterIndexed { j, _ -> j != i }.map { SesImza.kosinus(l[i], it) }.sortedDescending().take(2).average() }
      val esik = (loo.minOrNull()!! - 0.0).coerceIn(0.62, 0.85)  // telefonda: sahip 0.71-0.81, Mac yapay sesi 0.63 (oda/mikrofon benzerliği) → kendi en düşük tutarlılığın
      SesAyar.imzaYaz(ctx, ort, esik); SesAyar.orneklerYaz(ctx, l)
      mapOf("esik" to esik, "enDusuk" to loo.minOrNull()!!, "ortalama" to loo.average())
    }
    /** Başka birinin sesini (ör. abi) "bu ben değilim" olarak öğret */
    Function("yabanciEkle") { v: List<Double> -> SesAyar.yabanciEkle(ctx, v.toDoubleArray()); SesAyar.yabancilar(ctx).size }
    /** Son "AREX" kararı (Ayarlar'da gösterilir) */
    Function("sonKarar") { val j = SesAyar.sonKararOku(ctx); if (j == null) null else mapOf("benzerlik" to j.optDouble("b"), "yabanci" to j.optDouble("y"), "esik" to j.optDouble("e"), "sahip" to j.optBoolean("s"), "zaman" to j.optLong("z")) }
    /** Parmak iziyle onaylanan son "AREX": o anki sesi sahip örneklerine ekle → gerçek kullanım koşullarını öğrenir */
    Function("sonUyanmayiOgren") { val v = UyanmaServisi.sonVektor; if (v != null) { SesAyar.ornekOgren(ctx, v); UyanmaServisi.sonVektor = null; true } else false }
    Function("yabancilariSil") { SesAyar.yabancilariSil(ctx); true }
    Function("imzaSil") { SesAyar.imzaSil(ctx); true }
    /** Bir örneği kayıtlı imzayla karşılaştır → {benzerlik, esik, sahip} */
    Function("imzaKarsilastir") { v: List<Double> ->
      val k = SesAyar.karar(ctx, v.toDoubleArray()) ?: return@Function mapOf("hata" to "imza yok")
      mapOf("benzerlik" to k.benzerlik, "esik" to k.esik, "sahip" to k.sahip, "yabanci" to k.yabanciBenzerlik)
    }

    /** Ayarlarda açık mı (sistem listesinde var mı) */
    Function("ayardaAcik") { ayardaAcik() }

    /** Ayarlarda açık ama bağlı değilse (güncelleme/zorla durdurma sonrası) servisi kapatıp açarak yeniden bağlar.
     *  Dönüş: "bagli" | "onarildi" | "kapali" | "izin-yok" */
    AsyncFunction("onar") {
      if (ArexErisimServisi.ornek != null) return@AsyncFunction "bagli"
      if (!ayardaAcik()) return@AsyncFunction "kapali"
      if (ctx.checkSelfPermission("android.permission.WRITE_SECURE_SETTINGS") != PackageManager.PERMISSION_GRANTED) return@AsyncFunction "izin-yok"
      val cr = ctx.contentResolver
      val liste = Settings.Secure.getString(cr, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES) ?: ""
      val digerleri = liste.split(":").filter { it.isNotBlank() && !it.contains(ctx.packageName + "/") }
      Settings.Secure.putString(cr, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES, digerleri.joinToString(":"))
      Thread.sleep(400)
      Settings.Secure.putString(cr, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES, (digerleri + bilesen()).joinToString(":"))
      Settings.Secure.putInt(cr, Settings.Secure.ACCESSIBILITY_ENABLED, 1)
      for (i in 0 until 20) { if (ArexErisimServisi.ornek != null) return@AsyncFunction "onarildi"; Thread.sleep(150) }
      if (ArexErisimServisi.ornek != null) "onarildi" else "kapali"
    }

    Function("ekranOku") {
      val r = kok() ?: return@Function ""
      val sb = StringBuilder("[Uygulama: ${r.packageName}]\n")
      val gorulen = HashSet<String>()
      gez(r) { n ->
        val t = (n.text ?: n.contentDescription)?.toString()?.trim()
        if (!t.isNullOrEmpty() && n.isVisibleToUser && gorulen.add(t) && sb.length < 6000) {
          val tur = when { n.isEditable -> "✏️ "; n.isClickable || n.parent?.isClickable == true -> "🔘 "; else -> "" }
          sb.append(tur).append(t.replace("\n", " ")).append('\n')
        }
      }
      sb.toString()
    }

    Function("tikla") { metin: String -> tiklaIc(metin) }

    /** Başka bir uygulama açıldıktan SONRA (ms) ekranda verilen yazılardan birine dokunur; bulamazsa kısa aralıklarla yeniden dener.
     *  Ör. Instagram profili açılınca "Takip Et". Native tarafta: AREX arka plana geçince JS zamanlayıcıları durur. */
    Function("sonraTikla") { metinler: List<String>, ms: Int, deneme: Int ->
      if (ArexErisimServisi.ornek == null) return@Function false
      val h = Handler(Looper.getMainLooper())
      fun dene(kalan: Int) {
        val ok = metinler.any { m -> try { tiklaIc(m) } catch (_: Exception) { false } }
        if (!ok && kalan > 1) h.postDelayed({ dene(kalan - 1) }, 900)
      }
      h.postDelayed({ dene(deneme) }, ms.toLong())
      true
    }

    Function("yaz") { metin: String ->
      val r = kok() ?: return@Function false
      var alan = r.findFocus(AccessibilityNodeInfo.FOCUS_INPUT)
      if (alan == null || !alan.isEditable) { alan = null; gez(r) { n -> if (alan == null && n.isEditable && n.isVisibleToUser) alan = n } }
      val a = alan ?: return@Function false
      a.performAction(AccessibilityNodeInfo.ACTION_FOCUS)
      val b = Bundle(); b.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, metin)
      a.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, b)
    }

    Function("kaydir") { ileri: Boolean ->
      val r = kok() ?: return@Function false
      var k: AccessibilityNodeInfo? = null
      gez(r) { n -> if (k == null && n.isScrollable && n.isVisibleToUser) k = n }
      k?.performAction(if (ileri) AccessibilityNodeInfo.ACTION_SCROLL_FORWARD else AccessibilityNodeInfo.ACTION_SCROLL_BACKWARD) ?: false
    }

    Function("genel") { eylem: String ->
      val s = ArexErisimServisi.ornek ?: return@Function false
      val e = eylemKodu(eylem) ?: return@Function false
      s.performGlobalAction(e)
    }

    /** Yan tuş kartı kapandıktan SONRA eylemi yapar (aksi halde "geri" kartın kendisini kapatır, arkadaki uygulamaya ulaşmaz).
     *  Gecikme Android tarafında: kart kapanınca JS zamanlayıcıları durabilir. */
    Function("genelSonra") { eylem: String, ms: Int ->
      val e = eylemKodu(eylem) ?: return@Function false
      if (ArexErisimServisi.ornek == null) return@Function false
      Handler(Looper.getMainLooper()).postDelayed({ ArexErisimServisi.ornek?.performGlobalAction(e) }, ms.toLong())
      true
    }

    /** Yüklü uygulamayı adıyla açar (ör. "google", "saat", "hesap makinesi"); açılan uygulamanın adını döndürür */
    Function("uygulamaAc") { ad: String ->
      val pm = ctx.packageManager
      val q = sade(ad)
      val liste = pm.queryIntentActivities(Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER), 0)
      val etiketli = liste.map { it to sade(it.loadLabel(pm).toString()) }
      val sec = etiketli.firstOrNull { it.second == q } ?: etiketli.firstOrNull { it.second.startsWith(q) } ?: etiketli.firstOrNull { it.second.contains(q) }
        ?: return@Function ""
      val i = pm.getLaunchIntentForPackage(sec.first.activityInfo.packageName) ?: return@Function ""
      ctx.startActivity(i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
      sec.first.loadLabel(pm).toString()
    }
  }
}
