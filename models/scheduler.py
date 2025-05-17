import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import random
from utils.helpers import assign_writers_to_topics

class MediumScheduler:
    """Medium yazı paylaşım çizelgeleme sınıfı"""
    
    def __init__(self, start_date, end_date, topics, posting_days, holidays=None):
        """
        Args:
            start_date (datetime): Başlangıç tarihi
            end_date (datetime): Bitiş tarihi
            topics (dict): Konular ve yazar sayıları
            posting_days (dict): Paylaşım günleri ve sayıları
            holidays (list): Tatil günleri
        """
        self.start_date = start_date
        self.end_date = end_date
        self.topics = topics
        self.posting_days = posting_days
        self.holidays = holidays if holidays else []
        
        # Yazarları konulara göre dağıt
        self.topic_writers = assign_writers_to_topics(topics)
        
        # Yazarların son yazı yazdığı tarihleri tut
        self.last_writer_date = {writer: None for topic_writers in self.topic_writers.values() 
                               for writer in topic_writers}
        

    def generate_schedule(self):
        """
        Takvimi oluşturur ve pandas DataFrame döndürür.
        """
        schedule_data = []
        current_date  = self.start_date

        while current_date <= self.end_date:
            # Yayın günü + tatil kontrolü
            if (current_date.weekday() in self.posting_days and
                    current_date.date() not in self.holidays):

                cfg        = self.posting_days[current_date.weekday()]
                owner      = cfg["owner"]
                post_count = cfg["count"]

                # O güne ait tüm post kayıtlarını al
                day_posts = self._assign_posts_to_day(current_date,
                                                    owner,
                                                    post_count)
                schedule_data.extend(day_posts)          #  ← KRİTİK

            current_date += timedelta(days=1)

        return pd.DataFrame(schedule_data,
                            columns=["Date", "Day", "Owner",
                                    "Topic", "Writer", "Post_Number"])

    
    def _assign_posts_to_day(self, date, owner, post_count):
        day_posts, used_topics = [], set()

        for i in range(post_count):
            # --- konu seçimi --------------------------
            available = [t for t in self.topics if t not in used_topics] or list(self.topics)
            selected_topic = self._select_topic(available, date, i)
            used_topics.add(selected_topic)

            # --- yazar seçimi -------------------------
            selected_writer = self._select_writer(selected_topic, date)
            self.last_writer_date[selected_writer] = date

            day_posts.append({
                "Date": date,
                "Day": calendar.day_name[date.weekday()],
                "Owner": owner,
                "Topic": selected_topic,
                "Writer": selected_writer,
                "Post_Number": i + 1
            })
        return day_posts


    def _select_topic(self, available_topics, date, post_number):
        """
        Yazı için uygun bir konu seçer
        
        Args:
            available_topics (list): Kullanılabilir konular
            date (datetime): Yazının paylaşılacağı tarih
            post_number (int): O günkü kaçıncı yazı olduğu
            
        Returns:
            str: Seçilen konu
        """
        # Özel durum: Game Dev, HMS ve SCM konuları için ayın son cumartesi günü
        if date.weekday() == 5:  # Cumartesi
            # Ayın son cumartesi günü mü kontrolü
            next_month = date.replace(day=28) + timedelta(days=4)  # Bir sonraki ayın ilk gününü elde et
            next_month = next_month.replace(day=1)
            last_day = next_month - timedelta(days=1)  # Ayın son günü
            
            # Bu ayın son cumartesi günü için 7 günlük bir aralık kontrol et
            days_to_month_end = (last_day - date).days
            
            if days_to_month_end < 7:
                special_topics = ["Game Development", "Huawei Mobil Service", "Software Community Management"]
                
                for topic in special_topics:
                    if topic in available_topics and post_number < len(special_topics):
                        return topic
        
        # Normal konu seçimi
        # Konu ağırlıklarını hesapla (yazar sayılarına göre)
        topic_weights = {topic: count for topic, count in self.topics.items()}
        
        # Game Dev, HMS ve SCM için daha düşük ağırlık
        for topic in ["Game Development", "Huawei Mobil Service", "Software Community Management"]:
            if topic in topic_weights:
                topic_weights[topic] *= 0.5
        
        # Konuları ve ağırlıkları listelere ayır
        topics = list(topic_weights.keys())
        weights = [topic_weights[t] for t in topics]
        
        # Ağırlıklı rastgele seçim
        selected_topic = random.choices(topics, weights=weights, k=1)[0]
        
        return selected_topic
    
    def _select_writer(self, topic, post_date):
        """
        Konuya uygun yazarı seçer
        • Tek yazarlı konular  → doğrudan o yazar
        • SCM'de 2-ay periyotlu rotasyon
        • Diğer konularda      → en uzun süredir yazmayan
        """
        writers = self.topic_writers[topic]

        # — Tek yazarlı konular (GameDev, HMS, vb.) —
        if len(writers) == 1:
            return writers[0]

        # — SCM rotasyonu (2 ayda bir) —
        if topic == "Software Community Management":
            idx = ((post_date.month - 1) // 2) % len(writers)
            return writers[idx]

        # — Genel: en uzun süredir yazmayan —
        writers_sorted = sorted(
            writers,
            key=lambda w: self.last_writer_date[w] or datetime(1900, 1, 1)
        )
        return writers_sorted[0]