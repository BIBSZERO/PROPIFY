from src.core.database import db
from src.models.properties import Property
from typing import List, Optional, Any

class PropertyService:
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