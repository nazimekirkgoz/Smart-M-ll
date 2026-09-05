# Servo Güç Sorunu Çözümü (9V + Modül)

> [!CAUTION]
> **DİKKAT:** **9V Pili SAKIN doğrudan Servo motora bağlama!**
> Servo motorlar en fazla 6V ile çalışır. 9V verirsen motor **YANAR**.

Kitin içinde muhtemelen bir **"Power Supply Module" (Güç Modülü)** vardır. Breadboard'un ucuna takılan küçük siyah/dikdörtgen bir parça.

## Güvenli Bağlantı (9V Pil + Modül)

1.  **Güç Modülünü** Breadboard'a tak.
2.  **9V Pili**, bu modülün üzerindeki siyah güç girişine (jak) veya kablo girişine tak.
3.  Modülün üzerindeki düğmeye bas (Işığı yansın).
4.  Modül 5V ve 3.3V verir.
5.  **Servo Bağlantısı:**
    *   **Kırmızı (+):** Modülün **5V** pinine.
    *   **Kahverengi (-):** Modülün **GND** pinine.
    *   **Turuncu (Sinyal):** ESP32'nin **13. pinine**.
6.  **Ortak GND (Çok Önemli):**
    *   ESP32'nin bir **GND** bacağını, Güç Modülünün **GND** bacağına (eksi hattına) bir kablo ile bağla.
    *   Zaten ESP32 ve Modül aynı breadboard üzerindeyse ve eksi hatları birleşikse sorun yok. Ama emin olmak için kablo çek.

Eğer Güç Modülü yoksa, **3V (2 pil)** deneyebilirsin ama servo için **yetersiz** kalabilir (yavaş döner). Ama 9V'dan güvenlidir.
