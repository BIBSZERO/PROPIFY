import os
from typing import Any, Optional, Dict, List # Gerekli tipleri içeri aktar
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class DatabaseManager:
    # Parametrelerin ve dönüş değerlerinin tipini belirtiyoruz
    def __init__(self) -> None:
        url: Optional[str] = os.getenv("SUPABASE_URL")
        key: Optional[str] = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Hata: .env dosyasında SUPABASE_URL veya KEY eksik!")
            
        self.client: Client = create_client(url, key)

    # select_query'nin string, dönen verinin ise Any (herhangi bir şey) olduğunu belirttik
    def get_data(self, table_name: str, select_query: str = "*") -> Any:
        try:
            # Buradaki dönüş tipini açıkça belirterek --check-untyped-defs uyarısını çözeriz
            response = self.client.table(table_name).select(select_query).execute()
            return response
        except Exception as e:
            print(f"Veri çekme hatası ({table_name}): {e}")
            return None

db = DatabaseManager()