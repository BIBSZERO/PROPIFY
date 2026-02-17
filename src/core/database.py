import os
from typing import Any, Optional, Dict, List, Union
from dotenv import load_dotenv
from supabase import create_client, Client

# .env dosyasındaki değişkenleri sisteme yükle
load_dotenv()

class DatabaseManager:
    """
    PROPIFY Merkezi Veritabanı Yöneticisi.
    Supabase ile tüm CRUD işlemlerini tip güvenliğiyle yönetir.
    """
    
    def __init__(self) -> None:
        url: Optional[str] = os.getenv("SUPABASE_URL")
        key: Optional[str] = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Hata: .env dosyasında SUPABASE_URL veya KEY eksik!")
            
        self.client: Client = create_client(url, key)

    # --- VERİ OKUMA (READ) ---
    def get_data(self, table_name: str, select_query: str = "*", order_by: str = "created_at") -> Any:
        """Tablodaki verileri getirir ve varsayılan olarak tarihe göre sıralar."""
        try:
            return self.client.table(table_name).select(select_query).order(order_by, desc=True).execute()
        except Exception as e:
            print(f"❌ Veri çekme hatası ({table_name}): {e}")
            return None
    
    def get_joined_data(self, table_name: str, joined_query: str) -> Any:
        """İlişkili tablolarla birlikte veri çeker."""
        try:
            return self.client.table(table_name).select(joined_query).execute()
        except Exception as e:
            print(f"❌ İlişkili veri çekme hatası ({table_name}): {e}")
            return None

    def get_filtered_data(self, table_name: str, column: str, value: Any) -> Any:
        """Belirli bir sütuna göre tam eşleşme filtrelemesi yapar."""
        try:
            return self.client.table(table_name).select("*").eq(column, value).execute()
        except Exception as e:
            print(f"❌ Filtreli veri çekme hatası ({table_name}): {e}")
            return None

    def get_search_data(self, table_name: str, column: str, search_term: str) -> Any:
        """Metin tabanlı arama yapar (Kelimenin herhangi bir yerinde geçmesi yeterlidir)."""
        try:
            # Başına ve sonuna % ekleyerek 'içerir' mantığına çevirdik
            return self.client.table(table_name).select("*").ilike(column, f"%{search_term}%").execute()
        except Exception as e:
            print(f"❌ Arama hatası ({table_name}): {e}")
            return None

    # --- VERİ EKLEME (CREATE) ---
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> Any:
        try:
            return self.client.table(table_name).insert(data).execute()
        except Exception as e:
            print(f"❌ Veri ekleme hatası ({table_name}): {e}")
            return None

    # --- VERİ GÜNCELLEME (UPDATE) ---
    def update_data(self, table_name: str, data: Dict[str, Any], row_id: Union[str, int]) -> Any:
        try:
            return self.client.table(table_name).update(data).eq("id", row_id).execute()
        except Exception as e:
            print(f"❌ Veri güncelleme hatası ({table_name}): {e}")
            return None

    # --- VERİ SİLME (DELETE) ---
    def delete_data(self, table_name: str, row_id: Union[str, int]) -> Any:
        try:
            return self.client.table(table_name).delete().eq("id", row_id).execute()
        except Exception as e:
            print(f"❌ Veri silme hatası ({table_name}): {e}")
            return None
        
    # --- KULLANICI PROFİL İŞLEMLERİ ---
    def get_user_profile(self, user_id: str) -> Any:
        try:
            return self.client.table("profiles").select("*").eq("id", user_id).single().execute()
        except Exception as e:
            print(f"❌ Profil çekme hatası: {e}")
            return None
        
    def upsert_user_profile(self, profile_data: Dict[str, Any]) -> Any:
        try:
            return self.client.table("profiles").upsert(profile_data).execute()
        except Exception as e:
            print(f"❌ Profil güncelleme hatası: {e}")
            return None

db = DatabaseManager()