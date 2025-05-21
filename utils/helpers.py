import pandas as pd
import os
from datetime import datetime, timedelta, date

def load_holidays(filepath: str,
                  year: int | None = None) -> list[date]:
    """
    CSV'den tatil günlerini yükler.
    • year=None  -> dosyadaki tüm yıllar
    • year=YYYY  -> sadece o yıla ait günler
    Dosya yoksa aynı yıl için örnek tatil listesi üretir.
    """
    if not os.path.exists(filepath):
        # örnek dosya üret – yıl parametresi verilmemişse içinde bulunduğumuz yılı kullan
        create_sample_holidays(filepath, year or datetime.now().year)

    df = pd.read_csv(filepath)
    days: list[date] = []

    for _, row in df.iterrows():
        start = datetime.strptime(row["start_date"], "%Y-%m-%d").date()
        end   = datetime.strptime(row["end_date"],   "%Y-%m-%d").date()

        # yıl filtresi
        if year and (start.year != year and end.year != year):
            continue

        cur = start
        while cur <= end:
            days.append(cur)
            cur += timedelta(days=1)

    return days

def create_sample_holidays(filepath: str, year: int):
    """
    Basit, yıl-bağımlı bir örnek tatil dosyası üretir.
    Gerçek projede her yıl için resmi listeyi ayrı CSV olarak ekleyebilirsiniz.
    """
    # Örnek: sadece 4 ana resmî gün + 2 final/vize aralığı
    sample = {
        "name": [
            "Yılbaşı",
            "Ulusal Egemenlik ve Çocuk Bayramı",
            "Emek ve Dayanışma Günü",
            "Cumhuriyet Bayramı",
            "Fırat Üniversitesi Vize Haftası (Güz)",
            "Fırat Üniversitesi Final Haftası (Güz)"
        ],
        "start_date": [
            f"{year}-01-01",
            f"{year}-04-23",
            f"{year}-05-01",
            f"{year}-10-29",
            f"{year}-11-11",
            f"{year}-12-16"
        ],
        "end_date": [
            f"{year}-01-01",
            f"{year}-04-23",
            f"{year}-05-01",
            f"{year}-10-29",
            f"{year}-11-15",
            f"{year}-12-20"
        ]
    }

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pd.DataFrame(sample).to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"⚠  Örnek tatil dosyası oluşturuldu: {filepath}")
    
def export_to_excel(schedule, output_path, topic_writers=None):
    """
    Çizelgeyi çok sekmeli Excel dosyasına yazar.
    topic_writers -> {"Topic": [writer1, writer2, ...], ... }
    """
    import xlsxwriter, os
    from datetime import datetime

    # ------------------------------------------------- #
    #  Dosya açıksa sil / timestamp ekle
    # ------------------------------------------------- #
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except PermissionError:
            base, ext   = os.path.splitext(output_path)
            output_path = f"{base}_{datetime.now():%Y%m%d_%H%M%S}{ext}"
            print(f"❗ Dosya açıktı, yeni dosya: {output_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    wb     = xlsxwriter.Workbook(output_path)
    fmtD   = wb.add_format({'num_format': 'yyyy-mm-dd'})
    fmtW   = wb.add_format({'text_wrap': True})

    def _write_sheet(df, name):
        sh = wb.add_worksheet(name[:31])      # Excel isim limiti
        cols = df.columns.tolist()
        for c, h in enumerate(cols):
            sh.write(0, c, h)

        for r, row in enumerate(df.itertuples(index=False), start=1):
            for c, val in enumerate(row):
                if c == 0:                       # Date
                    sh.write_datetime(r, c, val, fmtD)
                elif c == 3:                     # Topic
                    sh.write(r, c, val, fmtW)
                else:
                    sh.write(r, c, val)

        # sütun genişlikleri
        sh.set_column(0, 0, 12)
        sh.set_column(1, 2, 10)
        sh.set_column(3, 3, 28)
        sh.set_column(4, 4, 16)
        sh.set_column(5, 5, 6)

    # 1️⃣ Ana tablo
    _write_sheet(schedule, "Tüm Çizelge")

    # 2️⃣ Paylaşımcı sekmeleri
    for owner in schedule['Owner'].unique():
        _write_sheet(schedule[schedule['Owner'] == owner], owner)

    # 3️⃣ Ay sekmeleri
    for m in range(1, 13):
        month_df = schedule[schedule['Date'].apply(lambda d: d.month) == m]
        _write_sheet(month_df, f"Ay {m}")

    # 4️⃣ Yazar-Konular haritası
    if topic_writers:
        sh = wb.add_worksheet("Yazar-Konular")
        sh.write(0, 0, "Writer")
        sh.write(0, 1, "Topic")

        row = 1
        for topic, writers in topic_writers.items():
            for w in writers:
                sh.write(row, 0, w)
                sh.write(row, 1, topic)
                row += 1

        sh.set_column(0, 0, 15)
        sh.set_column(1, 1, 30)

    wb.close()
    print(f"✅ Çizelge kaydedildi: {output_path}")

def assign_writers_to_topics(topics: dict) -> dict:
    """
    Konu → yazar listesi haritası.
    Özel konular için daha anlamlı etiketler üretir
    (SCM_Yazar1, HMS_Yazar... vb), diğerlerinde Yazar1…
    """
    topic_writers = {}
    sequential_id = 1

    for topic, count in topics.items():
        if topic == "Software Community Management":
            topic_writers[topic] = [f"SCM_Yazar{i+1}" for i in range(count)]
        elif topic == "Huawei Mobil Service":
            topic_writers[topic] = [f"HMS_Yazar{i+1}" for i in range(count)]
        elif topic == "Game Development":
            topic_writers[topic] = [f"GameDev_Yazar{i+1}" for i in range(count)]
        else:
            topic_writers[topic] = [f"Yazar{sequential_id + i}" for i in range(count)]
            sequential_id += count
    return topic_writers
