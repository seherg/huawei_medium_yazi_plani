import argparse, yaml, os
from datetime import datetime
from models.scheduler   import MediumScheduler
from utils.helpers      import load_holidays, export_to_excel
from constraints.rules  import apply_constraints

def main() -> None:
    ap = argparse.ArgumentParser(description="Medium Takvim Üretici")
    ap.add_argument("-c", "--config", default="config.yaml",
                    help="YAML konfigürasyon dosyası (varsayılan: config.yaml)")
    args = ap.parse_args()

    cfg_path = os.path.abspath(args.config)
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Konfigürasyon bulunamadı: {cfg_path}")

    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))

    year         : int   = cfg["year"]
    topics       : dict  = cfg["topics"]
    rules        : dict  = cfg["special_rules"]

    # Liste hâlindeki posting_days'i {weekday_int: {owner,count}} sözlüğüne çevir
    posting_days = {
        item["weekday"]: {"owner": item["owner"], "count": item["slots"]}
        for item in cfg["posting_days"]
    }

    holidays = load_holidays(cfg["holidays_file"], year=year)

    #Takvim üretimi
    scheduler = MediumScheduler(
        start_date  = datetime(year, 1, 1),
        end_date    = datetime(year, 12, 31),
        topics      = topics,
        posting_days= posting_days,
        holidays    = holidays
    )

    schedule = scheduler.generate_schedule()
    schedule = apply_constraints(schedule,
                                 scheduler.topic_writers,
                                 rules)

    #Excel çıktısı
    out_path = f"output/schedule_{year}.xlsx"
    export_to_excel(schedule,
                    out_path,
                    topic_writers=scheduler.topic_writers)

    print(f"✅ Takvim hazır → {out_path}")

if __name__ == "__main__":
    main()
