package com.arex.erisim

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.content.pm.ServiceInfo
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Build
import android.os.IBinder
import android.os.SystemClock
import org.json.JSONArray
import org.json.JSONObject
import org.vosk.Model
import org.vosk.Recognizer
import org.vosk.SpeakerModel
import java.io.File
import kotlin.math.sqrt

/**
 * "AREX" uyandırma kelimesi — tamamen cihaz içi (Vosk, internetsiz; ses hiçbir yere gönderilmez).
 * - Sessizken modeli çalıştırmaz (pil): yalnız ses enerjisi eşiği aşılınca ~1.5 sn tanıyıcıya verir.
 * - "AREX" (a rex / hey rex) duyulunca ses imzasını sahibininkiyle karşılaştırır, yan tuş kartını açar.
 * - Kart açıkken / imza kaydında mikrofonu bırakır (duraklat).
 */
class UyanmaServisi : Service() {
  companion object {
    @Volatile var calisiyor = false
    @Volatile var duraklat = false
    /** Yan tuş kartı (AsistanActivity) şu an açık mı — kart açılamazsa dinleme takılı kalmasın */
    @Volatile var kartAcik = false
    @Volatile var uyanmaZamani = 0L
    /** Son uyanmanın ses imzası: parmak iziyle onaylanırsa sahip örneklerine eklenir (gerçek kullanım koşullarını öğrenir) */
    @Volatile var sonVektor: DoubleArray? = null
    @Volatile var sonUyanma: JSONObject? = null
    const val KANAL = "arex_uyanma"
    const val ID = 4711
    const val ESIK_RMS = 350.0
    const val DILBILGISI = "[\"a rex\", \"hey rex\", \"rex\", \"[unk]\"]"

    fun baslat(ctx: Context) {
      val i = Intent(ctx, UyanmaServisi::class.java)
      if (Build.VERSION.SDK_INT >= 26) ctx.startForegroundService(i) else ctx.startService(i)
    }
    fun durdur(ctx: Context) { ctx.stopService(Intent(ctx, UyanmaServisi::class.java)) }
  }

  @Volatile private var dur = false
  private var halka = ShortArray(0); private var halkaYaz = 0; private var halkaDolu = 0

  /** Son 2 sn sesten ses imzası (x-vector). Kısa "AREX" anında kesildiğinde imza çıkmıyordu (telefon kayıtlarında 9 denemenin 6'sı);
   *  kayıt sırasında da 2 sn alındığı için karşılaştırma tutarlı olur. */
  private fun sonIkiSaniyeImza(): DoubleArray? {
    val uzunluk = minOf(halkaDolu, 16000 * 2)
    if (uzunluk < 8000) return null
    val parca = ShortArray(uzunluk)
    var bas = (halkaYaz - uzunluk + halka.size) % halka.size
    for (i in 0 until uzunluk) { parca[i] = halka[bas]; bas = (bas + 1) % halka.size }
    sonParca = parca
    return GucluImza.vektor(this, parca)
  }
  private var sonParca: ShortArray? = null
  /** Kalibrasyon: uyanma anının 2 sn sesi (yalnız bu telefonda, Android/data/com.arex.ai/files/ses) */
  private fun uyanmaSesiKaydet(sahip: Boolean, b: Double) {
    val p = sonParca ?: return
    try {
      val dir = File(getExternalFilesDir(null), "ses").apply { mkdirs() }
      val f = File(dir, "${System.currentTimeMillis()}_uyanma${if (sahip) "kabul" else "ret"}${(b * 100).toInt()}.wav")
      val pcm = ByteArray(p.size * 2); for (i in p.indices) { pcm[2 * i] = (p[i].toInt() and 0xff).toByte(); pcm[2 * i + 1] = ((p[i].toInt() shr 8) and 0xff).toByte() }
      f.outputStream().use { o ->
        val bb = java.nio.ByteBuffer.allocate(44).order(java.nio.ByteOrder.LITTLE_ENDIAN)
        bb.put("RIFF".toByteArray()).putInt(36 + pcm.size).put("WAVE".toByteArray()).put("fmt ".toByteArray()).putInt(16).putShort(1).putShort(1)
          .putInt(16000).putInt(32000).putShort(2).putShort(16).put("data".toByteArray()).putInt(pcm.size)
        o.write(bb.array()); o.write(pcm)
      }
    } catch (_: Exception) {}
  }
  private var is_: Thread? = null

  override fun onBind(intent: Intent?): IBinder? = null

  override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
    if (intent?.action == "KAPAT") {
      SesAyar.otomatikYaz(this, false); stopSelf(); return START_NOT_STICKY
    }
    bildirimBaslat()
    if (is_ == null) { dur = false; is_ = Thread({ try { dongu() } catch (_: Throwable) {} }, "arex-uyanma").also { it.start() } }
    calisiyor = true
    return START_STICKY
  }

  override fun onDestroy() {
    dur = true; calisiyor = false
    is_?.interrupt(); is_ = null
    super.onDestroy()
  }

  private fun bildirimBaslat() {
    val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
    if (Build.VERSION.SDK_INT >= 26 && nm.getNotificationChannel(KANAL) == null)
      nm.createNotificationChannel(NotificationChannel(KANAL, "AREX dinleme", NotificationManager.IMPORTANCE_MIN).apply { setShowBadge(false); description = "\"AREX\" deyince uyanır. Ses cihazda işlenir, hiçbir yere gönderilmez." })
    val kapat = PendingIntent.getService(this, 1, Intent(this, UyanmaServisi::class.java).setAction("KAPAT"), PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
    val ac = packageManager.getLaunchIntentForPackage(packageName)?.let { PendingIntent.getActivity(this, 2, it, PendingIntent.FLAG_IMMUTABLE) }
    val b = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, KANAL) else Notification.Builder(this)
    val n = b.setSmallIcon(android.R.drawable.ic_btn_speak_now)
      .setContentTitle("🎙 \"AREX\" deyince uyanırım")
      .setContentText("Ses yalnız bu telefonda işlenir")
      .setOngoing(true).setContentIntent(ac)
      .addAction(Notification.Action.Builder(android.graphics.drawable.Icon.createWithResource(this, android.R.drawable.ic_menu_close_clear_cancel), "Kapat", kapat).build())
      .build()
    if (Build.VERSION.SDK_INT >= 29) startForeground(ID, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE) else startForeground(ID, n)
  }

  private fun dongu() {
    if (checkSelfPermission(android.Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) { stopSelf(); return }
    val model = SesModelleri.model(this); val spk = SesModelleri.spk(this)
    var rec = Recognizer(model, 16000f, DILBILGISI).apply { setSpeakerModel(spk) }
    val min = AudioRecord.getMinBufferSize(16000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT)
    val ar = AudioRecord(MediaRecorder.AudioSource.VOICE_RECOGNITION, 16000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, maxOf(min, 32000))
    val buf = ShortArray(1600) // 100 ms
    halka = ShortArray(16000 * 5 / 2); halkaYaz = 0; halkaDolu = 0
    var sonSes = 0L
    var kayitta = false
    var gurultu = 120.0 // ortam gürültüsü tahmini (uyarlanır)
    try {
      while (!dur) {
        if (duraklat) {
          // Güvenlik: "AREX" ile duraklatıldı ama kart 6 sn içinde açılmadıysa (Android engelledi vb.) dinlemeye dön
          if (uyanmaZamani > 0 && !kartAcik && SystemClock.elapsedRealtime() - uyanmaZamani > 6000) { duraklat = false; uyanmaZamani = 0 }
          else {
            if (kayitta) { try { ar.stop() } catch (_: Exception) {}; kayitta = false }
            Thread.sleep(300); continue
          }
        }
        if (kartAcik) uyanmaZamani = 0
        if (!kayitta) { ar.startRecording(); kayitta = true; rec.close(); rec = Recognizer(model, 16000f, DILBILGISI).apply { setSpeakerModel(spk) } }
        val n = ar.read(buf, 0, buf.size)
        if (n <= 0) { Thread.sleep(50); continue }
        for (k in 0 until n) { halka[halkaYaz] = buf[k]; halkaYaz = (halkaYaz + 1) % halka.size }
        halkaDolu = minOf(halka.size, halkaDolu + n)
        var t = 0.0; for (k in 0 until n) { val v = buf[k].toDouble(); t += v * v }
        val rms = sqrt(t / n)
        val simdi = SystemClock.elapsedRealtime()
        // Uyarlanır eşik: sessizde gürültü tabanını öğren; konuşma = tabanın ~3 katı (en az 140)
        if (rms < gurultu * 1.5) gurultu = gurultu * 0.97 + rms * 0.03
        // Daha hassas: normal konuşma sesi de yakalansın (telefonda yalnız yüksek sesle tanıyordu)
        if (rms > maxOf(80.0, minOf(ESIK_RMS, gurultu * 2.2))) sonSes = simdi
        if (simdi - sonSes > 1500) continue // sessizlik: tanıyıcıyı çalıştırma (pil)
        // Yazılımsal ses yükseltme (AGC): kısık konuşmayı tanıyıcı için ~2500 RMS düzeyine çek (en fazla 6x), kırpmadan
        val kazanc = if (rms > 1.0) minOf(6.0, maxOf(1.0, 2500.0 / rms)) else 1.0
        if (kazanc > 1.05) for (k in 0 until n) buf[k] = (buf[k] * kazanc).toInt().coerceIn(-32768, 32767).toShort()
        if (rec.acceptWaveForm(buf, n)) {
          isle(JSONObject(rec.result))
        } else if (JSONObject(rec.partialResult).optString("partial").contains("rex")) {
          isle(JSONObject(rec.finalResult)) // hızlı tepki: kelime duyulur duyulmaz bitir (ses imzası da gelir)
        }
      }
    } finally {
      try { ar.stop() } catch (_: Exception) {}
      ar.release(); rec.close()
    }
  }

  private fun isle(j: JSONObject) {
    if (!j.optString("text").contains("rex")) return
    // Anında geri bildirim: "seni duydum" titreşimi (gecikme hissini kaldırır)
    try { (getSystemService(Context.VIBRATOR_SERVICE) as android.os.Vibrator).vibrate(android.os.VibrationEffect.createOneShot(45, 180)) } catch (_: Exception) {}
    // Ses imzası: son 2 sn tampondan (yetmezse tanıyıcının kendi vektörü)
    val vek = sonIkiSaniyeImza()
    // Eski (Vosk) imza varsa ama yeni modelle yeniden kaydedilmediyse: kimse "sahip" sayılmaz → parmak izi (yeniden kayda kadar)
    val imzaVar = SesAyar.imza(this) != null || SesAyar.eskiImzaVar(this)
    val k = if (vek != null) SesAyar.karar(this, vek) else null
    sonVektor = vek
    val benzerlik = k?.benzerlik ?: -1.0
    // OLASILIKSAL KARAR (3 seviye): 2 = kesin sen, 1 = muhtemelen sen (kişisel işlemler parmak izi ister), 0 = yabancı
    val seviye = when {
      !imzaVar -> 2
      k == null -> 0
      k.sahip -> 2
      k.benzerlik >= k.esik - 0.17 && (k.yabanciBenzerlik < 0 || k.benzerlik > k.yabanciBenzerlik) -> 1  // telefon verisi: gerçek kullanımda sahip 0.50-0.65
      else -> 0
    }
    val sahip = seviye > 0
    // ÖĞRENME: çok emin olunan uyanmalar imzaya eklenir (farklı ton/ortam); ilk kayıtlar korunur, en fazla 20
    if (seviye == 2 && vek != null && k != null && k.benzerlik >= 0.75) SesAyar.ornekOgren(this, vek)
    android.util.Log.i("AREX-SES", "uyanma seviye=$seviye metin='${j.optString("text")}' benzerlik=${"%.3f".format(benzerlik)} yabanci=${"%.3f".format(k?.yabanciBenzerlik ?: -1.0)} esik=${"%.3f".format(k?.esik ?: -1.0)} sahip=$sahip vek=${vek != null}")
    SesAyar.sonKarar(this, benzerlik, k?.yabanciBenzerlik ?: -1.0, k?.esik ?: -1.0, sahip)
    uyanmaSesiKaydet(sahip, benzerlik)
    if (!sahip) yabanciUyari(benzerlik) // sahibin sesi değil: cevap YOK; yalnız parmak izi kilidi açılır (8 sn) + sahibine haber
    sonUyanma = JSONObject().put("zaman", System.currentTimeMillis()).put("sahip", sahip).put("seviye", seviye).put("benzerlik", benzerlik).put("imzaVar", imzaVar)
    duraklat = true // kart açılıyor: mikrofonu ona bırak (AsistanActivity kapanınca devam eder; açılmazsa 6 sn sonra)
    uyanmaZamani = SystemClock.elapsedRealtime()
    val i = Intent().setClassName(packageName, "$packageName.AsistanActivity")
      .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
      .putExtra("uyanma", true).putExtra("sahip", sahip).putExtra("seviye", seviye)
    try {
      // Arka plandan etkinlik açma: bağlı erişilebilirlik servisi ya da "diğer uygulamaların üzerinde göster" izni ile anında
      (ArexErisimServisi.ornek ?: this).startActivity(i)
    } catch (_: Exception) {}
    // Yedek: tam ekran bildirim (kilit ekranında/ekran kapalıyken Android etkinliği hemen açar)
    if (ArexErisimServisi.ornek == null && !(Build.VERSION.SDK_INT >= 23 && android.provider.Settings.canDrawOverlays(this))) tamEkranBildirim(i)
  }
}

/** Kilit ekranında anında açılış için tam ekran bildirim (yalnız diğer yollar yoksa) */
private fun UyanmaServisi.tamEkranBildirim(i: Intent) {
  val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
  if (Build.VERSION.SDK_INT >= 26 && nm.getNotificationChannel("arex_ac") == null)
    nm.createNotificationChannel(NotificationChannel("arex_ac", "AREX açılış", NotificationManager.IMPORTANCE_HIGH).apply { setSound(null, null) })
  val pi = PendingIntent.getActivity(this, 3, i, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
  val b = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, "arex_ac") else Notification.Builder(this)
  nm.notify(4713, b.setSmallIcon(android.R.drawable.ic_btn_speak_now).setContentTitle("AREX").setContentText("Seni dinliyorum…")
    .setCategory(Notification.CATEGORY_CALL).setFullScreenIntent(pi, true).setContentIntent(pi).setAutoCancel(true).setTimeoutAfter(8000).build())
}

/** 🛡️ Tanımadığı ses "AREX" dediğinde sahibine bildirim (dakikada en fazla bir) */
private var sonUyari = 0L
private fun UyanmaServisi.yabanciUyari(benzerlik: Double) {
  val simdi = System.currentTimeMillis()
  SesAyar.yabanciSay(this)
  if (simdi - sonUyari < 60_000) return
  sonUyari = simdi
  val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
  if (Build.VERSION.SDK_INT >= 26 && nm.getNotificationChannel("arex_guvenlik") == null)
    nm.createNotificationChannel(NotificationChannel("arex_guvenlik", "AREX güvenlik", NotificationManager.IMPORTANCE_HIGH).apply { description = "Tanımadığım biri AREX'i kullanmaya çalışınca haber veririm" })
  val saat = java.text.SimpleDateFormat("HH:mm", java.util.Locale("tr")).format(java.util.Date(simdi))
  val b = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, "arex_guvenlik") else Notification.Builder(this)
  nm.notify(4712, b.setSmallIcon(android.R.drawable.ic_lock_idle_lock)
    .setContentTitle("🛡️ Tanımadığım bir ses \"AREX\" dedi")
    .setContentText("$saat • Yok saydım, hiçbir şey açılmadı. (benzerlik %${(benzerlik.coerceAtLeast(0.0) * 100).toInt()})")
    .setAutoCancel(true).build())
}

/** Vosk modelleri: APK içindeki assets → uygulama klasörü (bir kez; sürüm uuid ile) */
object SesModelleri {
  @Volatile private var m: Model? = null
  @Volatile private var s: SpeakerModel? = null
  @Synchronized fun model(ctx: Context): Model = m ?: Model(hazirla(ctx, "vosk-en")).also { m = it }
  @Synchronized fun spk(ctx: Context): SpeakerModel = s ?: SpeakerModel(hazirla(ctx, "vosk-spk")).also { s = it }
  private fun hazirla(ctx: Context, ad: String): String {
    val hedef = File(ctx.filesDir, ad)
    val yeni = ctx.assets.open("$ad/uuid").bufferedReader().readText().trim()
    val eski = File(hedef, "uuid").takeIf { it.exists() }?.readText()?.trim()
    if (eski != yeni) { hedef.deleteRecursively(); kopyala(ctx, ad, hedef) }
    return hedef.absolutePath
  }
  private fun kopyala(ctx: Context, yol: String, hedef: File) {
    val liste = ctx.assets.list(yol) ?: arrayOf()
    if (liste.isEmpty()) { hedef.parentFile?.mkdirs(); ctx.assets.open(yol).use { g -> hedef.outputStream().use { g.copyTo(it) } }; return }
    hedef.mkdirs(); for (c in liste) kopyala(ctx, "$yol/$c", File(hedef, c))
  }
}

/** Güçlü ses imzası: 3D-Speaker ERes2Net (VoxCeleb) / sherpa-onnx — Mac testinde aynı ses 0.73, farklı 0.18 (Vosk: 0.68 / 0.32) */
object GucluImza {
  const val MODEL = "eres2net-vox"
  @Volatile private var ex: com.k2fsa.sherpa.onnx.SpeakerEmbeddingExtractor? = null
  @Synchronized private fun cikarici(ctx: Context) = ex ?: com.k2fsa.sherpa.onnx.SpeakerEmbeddingExtractor(ctx.assets,
    com.k2fsa.sherpa.onnx.SpeakerEmbeddingExtractorConfig("spk-guclu.onnx", 2, false, "cpu")).also { ex = it }
  /** 16 kHz PCM → imza vektörü (en az ~0.5 sn ses) */
  fun vektor(ctx: Context, pcm: ShortArray): DoubleArray? = try {
    if (pcm.size < 8000) null else {
      val e = cikarici(ctx); val st = e.createStream()
      st.acceptWaveform(FloatArray(pcm.size) { pcm[it] / 32768f }, 16000); st.inputFinished()
      val v = if (e.isReady(st)) e.compute(st).map { it.toDouble() }.toDoubleArray() else null
      st.release(); v
    }
  } catch (_: Throwable) { null }
}

/** Ses imzası (x-vector) yardımcıları */
object SesImza {
  fun dizi(a: JSONArray) = DoubleArray(a.length()) { a.getDouble(it) }
  fun kosinus(a: DoubleArray, b: DoubleArray): Double {
    var d = 0.0; var x = 0.0; var y = 0.0
    for (i in 0 until minOf(a.size, b.size)) { d += a[i] * b[i]; x += a[i] * a[i]; y += b[i] * b[i] }
    return if (x == 0.0 || y == 0.0) 0.0 else d / sqrt(x) / sqrt(y)
  }
  fun ortalama(l: List<DoubleArray>): DoubleArray {
    val o = DoubleArray(l[0].size); for (v in l) for (i in o.indices) o[i] += v[i] / l.size; return o
  }
}

/** Kalıcı ayarlar: ses imzası (ortalama vektör + eşik) ve otomatik başlatma */
object SesAyar {
  private fun p(ctx: Context) = ctx.getSharedPreferences("arex_ses", Context.MODE_PRIVATE)
  fun imza(ctx: Context): Pair<DoubleArray, Double>? {
    if (p(ctx).getString("imzaModel", "") != GucluImza.MODEL) return null  // eski (Vosk) imza → yeniden kayıt gerekir
    val s = p(ctx).getString("imza", null) ?: return null
    val j = JSONObject(s); return SesImza.dizi(j.getJSONArray("v")) to maxOf(0.62, j.getDouble("esik") + 0.08)  // eski formüldeki -0.08 payı geri al
  }
  fun imzaYaz(ctx: Context, v: DoubleArray, esik: Double) {
    p(ctx).edit().putString("imza", JSONObject().put("v", JSONArray(v.toList())).put("esik", esik).toString()).putString("imzaModel", GucluImza.MODEL).remove("yabancilar").apply()
  }
  fun eskiImzaVar(ctx: Context) = p(ctx).getString("imza", null) != null && p(ctx).getString("imzaModel", "") != GucluImza.MODEL
  fun imzaSil(ctx: Context) { p(ctx).edit().remove("imza").remove("ornekler").apply() }
  private fun liste(ctx: Context, ad: String): List<DoubleArray> {
    val s = p(ctx).getString(ad, null) ?: return emptyList(); val a = JSONArray(s)
    return (0 until a.length()).map { SesImza.dizi(a.getJSONArray(it)) }
  }
  private fun listeYaz(ctx: Context, ad: String, l: List<DoubleArray>) {
    p(ctx).edit().putString(ad, JSONArray(l.map { JSONArray(it.toList()) }).toString()).apply()
  }
  fun ornekler(ctx: Context) = liste(ctx, "ornekler")
  /** Kesin tanınan uyanmayı imzaya ekle: ilk 6 kayıt hep kalır, öğrenilenler en fazla 14 (toplam ≤ 20) */
  fun ornekOgren(ctx: Context, v: DoubleArray) {
    val l = ornekler(ctx); if (l.size < 3) return
    val ilk = l.take(6); val ogrenilen = (l.drop(6) + listOf(v)).takeLast(14)
    orneklerYaz(ctx, ilk + ogrenilen)
  }
  fun orneklerYaz(ctx: Context, l: List<DoubleArray>) = listeYaz(ctx, "ornekler", l)
  fun yabancilar(ctx: Context) = liste(ctx, "yabancilar")
  fun yabanciEkle(ctx: Context, v: DoubleArray) = listeYaz(ctx, "yabancilar", (yabancilar(ctx) + listOf(v)).takeLast(15))
  fun yabancilariSil(ctx: Context) { p(ctx).edit().remove("yabancilar").apply() }

  data class Karar(val sahip: Boolean, val benzerlik: Double, val yabanciBenzerlik: Double, val esik: Double)
  /** Sahip örneklerine en yakın 2'nin ortalaması ≥ eşik VE öğretilmiş yabancı seslerden belirgin şekilde daha yakın */
  fun karar(ctx: Context, v: DoubleArray): Karar? {
    val im = imza(ctx) ?: return null
    val orn = ornekler(ctx)
    val sO = if (orn.size >= 2) orn.map { SesImza.kosinus(v, it) }.sortedDescending().take(2).average() else SesImza.kosinus(v, im.first)
    val sN = yabancilar(ctx).maxOfOrNull { SesImza.kosinus(v, it) } ?: -1.0
    // Gerçek kullanımdan ≥3 örnek öğrenildiyse eşik 0.72'ye çıkar (telefon verisi simülasyonu: sen 0.73-0.94, yabancı ≤0.74 → 0.72'de seni %100 tanır)
    val esik = if (orn.size >= 9) maxOf(im.second, 0.72) else im.second
    val sahip = sO >= esik && (sN < 0 || sO > sN)  // öğretilen yabancı sesinden daha yakınsa (telefonda %4 pay seni de reddediyordu)
    return Karar(sahip, sO, sN, esik)
  }
  fun yabanciSay(ctx: Context) { p(ctx).edit().putInt("yabanci", p(ctx).getInt("yabanci", 0) + 1).putLong("yabanciSon", System.currentTimeMillis()).apply() }
  fun yabanci(ctx: Context) = p(ctx).getInt("yabanci", 0) to p(ctx).getLong("yabanciSon", 0L)
  fun sonKarar(ctx: Context, b: Double, y: Double, e: Double, sahip: Boolean) {
    p(ctx).edit().putString("sonKarar", JSONObject().put("b", b).put("y", y).put("e", e).put("s", sahip).put("z", System.currentTimeMillis()).toString()).apply()
  }
  fun sonKararOku(ctx: Context): JSONObject? = p(ctx).getString("sonKarar", null)?.let { JSONObject(it) }
  fun otomatik(ctx: Context) = p(ctx).getBoolean("otomatik", false)
  fun otomatikYaz(ctx: Context, v: Boolean) { p(ctx).edit().putBoolean("otomatik", v).apply() }
}
