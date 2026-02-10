import os
from typing import Any, Optional, Dict, List, Union
from dotenv import load_dotenv
from supabase import create_client, Client

# .env dosyasındaki değişkenleri sisteme yükle
load_dotenv()

class DatabaseManager:
    """
    PPOPIFY Merkezi Veritabanı Yöneticisi.
    Supabase ile tüm CRUD işlemlerini tip güvenliğiyle yönetir.
    """
    
    def __init__(self) -> None:
        url: Optional[str] = os.getenv("SUPABASE_URL")
        key: Optional[str] = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Hata: .env dosyasında SUPABASE_URL veya KEY eksik!")
            
        self.client: Client = create_client(url, key)

    # --- VERİ OKUMA (READ) ---
    def get_data(self, table_name: str, select_query: str = "*") -> Any:
        """Tablodaki tüm verileri veya seçili sütunları getirir."""
        try:
            return self.client.table(table_name).select(select_query).execute()
        except Exception as e:
            print(f"❌ Veri çekme hatası ({table_name}): {e}")
            return None

    def get_filtered_data(self, table_name: str, column: str, value: Any) -> Any:
        """Belirli bir sütuna göre filtreleme yaparak veri getirir."""
        try:
            return self.client.table(table_name).select("*").eq(column, value).execute()
        except Exception as e:
            print(f"❌ Filtreli veri çekme hatası ({table_name}): {e}")
            return None

    # --- VERİ EKLEME (CREATE) ---
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> Any:
        """Tabloya yeni bir satır ekler."""
        try:
            return self.client.table(table_name).insert(data).execute()
        except Exception as e:
            print(f"❌ Veri ekleme hatası ({table_name}): {e}")
            return None

    # --- VERİ GÜNCELLEME (UPDATE) ---
    def update_data(self, table_name: str, data: Dict[str, Any], row_id: Union[str, int]) -> Any:
        """Belirli bir ID'ye sahip satırı günceller."""
        try:
            return self.client.table(table_name).update(data).eq("id", row_id).execute()
        except Exception as e:
            print(f"❌ Veri güncelleme hatası ({table_name}): {e}")
            return None

    # --- VERİ SİLME (DELETE) ---
    def delete_data(self, table_name: str, row_id: Union[str, int]) -> Any:
        """Belirli bir ID'ye sahip satırı siler."""
        try:
            return self.client.table(table_name).delete().eq("id", row_id).execute()
        except Exception as e:
            print(f"❌ Veri silme hatası ({table_name}): {e}")
            return None

# Uygulama genelinde kullanılacak Singleton nesnesi
db = DatabaseManager()