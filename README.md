# Medium Yazı Paylaşım Çizelgesi Oluşturucu
Bu projeyi, Huawei Türkiye’de Medium yazı direktör yardımcılığı görevim kapsamında geliştirdim. 60’tan fazla yazarın haftalık içerik takibini manuel yapmak hem vakit alıcı hem de hataya çok açıktı. Bu nedenle kısıtlı optimizasyon yaklaşımı ile çalışan, esnek ve dinamik bir sistem tasarladım.

Amacım; paylaşım günlerine, konu dönüşümlerine, özel tarihlere ve yazar dengelerine uygun adil ve sürdürülebilir bir yazı paylaşım çizelgesi oluşturmaktı. Şimdi sadece config.yaml dosyasını değiştirerek farklı yıllar için otomatik takvimler üretilebiliyorum.
## Ne işe yarar?
| İhtiyaç                          | Nasıl Çözer?                                                     |
| -------------------------------- | ---------------------------------------------------------------- |
| Haftada kim kaç yazı girsin?     | `posting_days` listesine gün / yazar / slot yaz → otomatik plan. |
| Backend & AI sırayla gitsin      | Kurala gömülü; ilk slotlar sürekli B → A → B → A…                |
| Ay sonu özel içerik              | Son Cumartesi: **Game ⇢ HMS ⇢ SCM** üçlü paket ekler.            |
| SCM’de 2 yazar dönüşsün          | `scm_rotation` kadar ayda bir otomatik değiştirir.               |
| Tatil / sınav haftası çakışmasın | Tatil CSV’sindeki günler takvimden silinir.                      |
| Yazarlar adil dağılsın           | “En uzun süredir yazmayan yazar” kuralı.                         |
| Çok sekmeli Excel                | Tüm Çizelge + kişi sekmeleri + Ay 1-12 + Yazar-Konular.          |

![image](https://github.com/user-attachments/assets/05081ac7-2196-4a4a-9b70-68ef9454bb50)

## 🔒 Kısıtlar

1. **Haftalık Paylaşım Programı**:
   - Pazartesi: Bengü - 2 yazı
   - Çarşamba: Ben (Seher) - 2 yazı
   - Cumartesi: Çağatay - 3 yazı

2. **Konu Dönüşümü**:
   - Backend ve AI konuları dönüşümlü olmalı
   - Örneğin: Pazartesi Backend → Çarşamba AI → Cumartesi Backend → Sonraki Pazartesi AI...

3. **Yazar Dağılımı 👥** (toplam 60 yazar):
      🧠 AI/ML Development: 15
      
      🔧 Backend Development: 11
      
      📊 Data Science: 6
      
      🎨 Frontend Development: 8
      
      ☁️ Huawei Cloud: 6
      
      📱 Mobil Development: 9
      
      🎮 Game Development: 1
      
      📲 Huawei Mobil Service: 1
      
      🌐 Software Community Management: 2

4. **Özel Kısıtlar**:
   - Game Development, Huawei Mobil Service ve Software Community Management konuları her ayın sonunda bir kez yazılmalı
   - Software Community Management için 2 yazar olduğundan, bu yazarlar 2 ayda bir dönüşümlü yazmalı

5. **Tatil Günleri**:
   - Türkiye'deki resmi tatiller
   - Fırat Üniversitesi vize ve final haftaları

## 📂 Proje Yapısı

```
huawei_medium_yazi_plani/
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
![image](https://github.com/user-attachments/assets/b2888486-2953-42d1-af7a-9a6b0cf71d1f)

![image](https://github.com/user-attachments/assets/f3be8f2f-2969-4ea3-8c07-262902758fdc)

## Excel Sekmeleri
| Sekme adı                   | İçerik                |
| --------------------------- | --------------------- |
| **Tüm Çizelge**             | Yıllık tam liste      |
| **Bengü / Seher / Çağatay** | Kişiye göre filtre    |
| **Ay 1 … Ay 12**            | Aylık filtre          |
| **Yazar-Konular**           | Yazar → Konu haritası |

