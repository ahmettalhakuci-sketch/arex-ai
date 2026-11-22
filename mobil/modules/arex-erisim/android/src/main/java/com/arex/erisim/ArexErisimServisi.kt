package com.arex.erisim

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent

/** AREX erişilebilirlik servisi: yalnız JS komut verdiğinde işlem yapar; olayları kaydetmez. */
class ArexErisimServisi : AccessibilityService() {
  companion object { @Volatile var ornek: ArexErisimServisi? = null }
  override fun onServiceConnected() {
    super.onServiceConnected(); ornek = this
    // Telefon yeniden başlayınca / güncellemeden sonra sistem bu servisi bağlar → "AREX" dinlemesini kendiliğinden sürdür
    if (SesAyar.otomatik(this) && !UyanmaServisi.calisiyor) { try { UyanmaServisi.baslat(this) } catch (_: Exception) {} }
  }
  override fun onAccessibilityEvent(event: AccessibilityEvent?) {}
  override fun onInterrupt() {}
  override fun onDestroy() { if (ornek === this) ornek = null; super.onDestroy() }
}
