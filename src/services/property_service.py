import uuid
import os
from src.core.database import db
from src.models.properties import Property
from typing import List, Optional, Any, cast, Dict

class PropertyService:

    @staticmethod
    def upload_image(file_path: str, file_name: str) -> Optional[str]:
        """
        Dosyayı Supabase Storage'a yükler ve public URL döner.
        """
        try:
            # 1. Uzantıyı al ve benzersiz isim oluştur
            file_ext = os.path.splitext(file_name)[1]
            unique_name = f"{uuid.uuid4()}{file_ext}"

            # 2. Dosyayı binary modda aç ve yükle
            with open(file_path, "rb") as f:
                db.client.storage.from_("property_images").upload(
                    path=unique_name,
                    file=f,
                    file_options={"content-type": f"image/{file_ext.replace('.', '')}"}
                )
            
            # 3. Public URL'yi al
            res = db.client.storage.from_("property_images").get_public_url(unique_name)
            return res if isinstance(res, str) else res.public_url

        except Exception as e:
            print(f"🚀 Servis Yükleme Hatası: {e}")
            return None
        
    @staticmethod
    def get_property_images(property_id: str) -> List[str]:
        """
        Belirli bir mülk ID'sine ait resim URL'lerini getirir.
        Mypy 'Missing return statement' hatasını gidermek için her yol bir return'e çıkar.
        """
        try:
            # 1. Veriyi çek
            response = db.client.table("properties").select("images").eq("id", property_id).single().execute()
            
            # 2. Katı tip kontrolleri (Mypy'ı sakinleştiren kısım)
            if response and response.data and isinstance(response.data, dict):
                data_dict = cast(Dict[str, Any], response.data)
                images = data_dict.get("images")
                
                if isinstance(images, list):
                    # Her elemanı string'e çevirerek garantiye alıyoruz
                    return [str(url) for url in images]
            
            # 🚀 KRİTİK: Eğer yukarıdaki şartlar sağlanmazsa boş liste dön
            return []
            
        except Exception as e:
            print(f"🚀 Resim Getirme Hatası: {e}")
            # Hata anında da mutlaka bir liste dönmelisin
            return []

    @staticmethod
    def get_all() -> List[Property]:
        response = db.get_data("properties")
        if response and response.data:
            return [Property.from_dict(item) for item in response.data]
        return []
    
    @staticmethod
    def add(property_obj: Property) -> bool:
        data = property_obj.to_dict()
        response = db.insert_data("properties", data)
        return response is not None
    
    @staticmethod
    def delete(property_id: str) -> bool:
        response = db.delete_data("properties", property_id)
        return response is not None
    
    @staticmethod
    def update(property_obj: Property) -> bool:
        if not property_obj.id:
            return False
        data = property_obj.to_dict()
        response = db.update_data("properties", data, property_obj.id)
        return response is not None
    
    @staticmethod
    def get_filtered(column: str, value:Any) -> List[Property]:
        response = db.get_filtered_data("properties", column, value)
        if response and response.data:
            return [Property.from_dict(item) for item in response.data]
        return []
    
property_service = PropertyService()

if __name__ == "__main__":
    print("🏠 Portföy verileri kontrol ediliyor...")
    ilanlar = property_service.get_all()

    if ilanlar:
        for ilan in ilanlar:
            print(f"✅ İlan: {ilan.title} | Fiyat: {ilan.price} | Durum: {ilan.status.value} | Müşteri: {ilan.owner_id}")
    else:
        print("⚠️ Henüz hiç ilan bulunamadı.")