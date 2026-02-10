import os
from dotenv import load_dotenv
from supabase import create_client, Client

# .env dosyasındaki değişkenleri yükle
load_dotenv()

class DatabaseManager:
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase URL veya KEY bulunamadı! .env dosyasını kontrol et.")
            
        self.client: Client = create_client(url, key)

    # Verileri profesyonelce çekmek için yardımcı metodlar
    def get_all(self, table_name: str):
        return self.client.table(table_name).select("*").execute()

    def insert(self, table_name: str, data: dict):
        return self.client.table(table_name).insert(data).execute()

# Tek bir instance oluşturup her yerden buna erişeceğiz (Singleton Mantığı)
db = DatabaseManager()