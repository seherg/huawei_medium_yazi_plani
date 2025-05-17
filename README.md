# Medium Yazı Paylaşım Çizelgesi Oluşturucu (Düzeltilmiş)

Bu proje, belirli kısıtlar altında Medium için optimum yazı paylaşım çizelgesi oluşturmayı amaçlar.

## Kısıtlar

1. **Haftalık Paylaşım Programı**:
   - Pazartesi: Bengü - 2 yazı
   - Çarşamba: Siz - 2 yazı
   - Cumartesi: Çağatay - 3 yazı

2. **Konu Dönüşümü**:
   - Backend ve AI konuları dönüşümlü olmalı
   - Örneğin: Pazartesi Backend → Çarşamba AI → Cumartesi Backend → Sonraki Pazartesi AI...

3. **Yazar Dağılımı** (toplam 60 yazar):
   - AI/ML Development: 15 yazar
   - Backend Development: 11 yazar
   - Data Science: 6 yazar
   - Frontend Development: 8 yazar
   - Huawei Cloud: 6 yazar
   - Mobil Development: 9 yazar
   - Game Development: 1 yazar
   - Huawei Mobil Service: 1 yazar
   - Software Community Management: 2 yazar

4. **Özel Kısıtlar**:
   - Game Development, Huawei Mobil Service ve Software Community Management konuları her ayın sonunda bir kez yazılmalı
   - Software Community Management için 2 yazar olduğundan, bu yazarlar 2 ayda bir dönüşümlü yazmalı

5. **Tatil Günleri**:
   - Türkiye'deki resmi tatiller
   - Fırat Üniversitesi vize ve final haftaları

## Proje Yapısı

```
medium_scheduler/
├── main.py                   # Ana program
├── data/
│   └── holidays_2025_tr.csv  # Tatil günleri verileri
├── output/
│   └── schedule_2025.xlsx    # Oluşturulan çizelge
├── utils/
│   └── helpers.py            # Yardımcı fonksiyonlar
├── constraints/
│   └── rules.py              # Kısıt kuralları
├── models/
│   └── scheduler.py          # Çizelgeleyici sınıf
└── README.md                 # Bu dosya
```

## Düzeltilen Sorunlar

Bu güncellenmiş versiyonda aşağıdaki sorunlar çözülmüştür:

1. **Backend ve AI Dönüşümü**: Artık Backend ve AI konuları sırasıyla ve kesintisiz olarak dönüşümlü atanmaktadır.

2. **Post Numaraları**: Her gün için post numaraları 1'den başlayarak sıralı şekilde atanmıştır.

3. **Özel Konular**: Game Development, Huawei Mobil Service ve Software Community Management konuları her ayın son cumartesi gününde düzenli olarak atanmaktadır.

4. **Yazar Atama**: Özel konular için özel yazarlar atanmış ve Software Community Management için 2 yazarın dönüşümlü olarak seçilmesi sağlanmıştır.

5. **Tatil Günleri**: Tatil günlerinde paylaşım yapılmaması için kontrol eklenmiştir.

## Kurulum ve Çalıştırma

1. Gereksinimleri yükleyin:
   ```
   pip install pandas xlsxwriter
   ```

2. Programı çalıştırın:
   ```
   python main.py
   ```

3. Oluşturulan çizelge `output/schedule_2025.xlsx` dosyasına kaydedilecektir.

## Çizelgeleme Algoritması

1. Tatil günleri yüklenir ve çizelgeden çıkarılır
2. Paylaşım günleri (Pazartesi, Çarşamba, Cumartesi) belirlenir
3. Backend ve AI konuları dönüşümlü olarak atanır
4. Her ayın son cumartesi günü özel konular atanır
5. Yazarlar adil şekilde seçilir ve rotasyona tabi tutulur
6. Excel formatında çıktı oluşturulur

## Örnek Çıktı

Bu projede oluşturulan çizelge, aşağıdaki formatta olacaktır:

| Tarih      | Gün       | Sorumlu | Konu                     | Yazar      | Yazı No |
|------------|-----------|---------|--------------------------|------------|---------|
| 2025-01-06 | Pazartesi | Bengü   | Backend Development      | Yazar11    | 1       |
| 2025-01-06 | Pazartesi | Bengü   | Frontend Development     | Yazar27    | 2       |
| 2025-01-08 | Çarşamba  | Siz     | AI/ML Development        | Yazar3     | 1       |
| ...        | ...       | ...     | ...                      | ...        | ...     |