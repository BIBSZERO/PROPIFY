# Bu sayfayı bu komutla çalıştırabilirsin: python -m src.services.contact_service
from src.core.database import db
from src.models.contacts import Contact, ContactCategory
from typing import List, Optional

class ContactService:
    @staticmethod
    def get_all() -> List[Contact]:
        response = db.get_data("contacts")
        if response and response.data:
            return [Contact.from_dict(item) for item in response.data]
        return []
    
    @staticmethod
    def add(contact: Contact) -> bool:
        data = contact.to_dict()
        response = db.insert_data("contacts", data)
        return response is not None
    
    @staticmethod
    def delete(contact_id: str) -> bool:
        response = db.delete_data("contacts", contact_id)
        return response is not None
    
    @staticmethod
    def update(contact: Contact) -> bool:
        """ID'si belli olan bir kişinin bilgilerini günceller."""
        if not contact.id:
            print("❌ Hata: ID'si olmayan bir kayıt güncellenemez!")
            return False
            
        data = contact.to_dict()
        response = db.update_data("contacts", data, contact.id)
        return response is not None
    
    @staticmethod
    def get_filtered(column: str, value) -> List[Contact]:
        response = db.get_filtered_data("contacts", column, value)
        if response and response.data:
            return [Contact.from_dict(item) for item in response.data]
        return []
    
contact_service = ContactService()

# --- TEST BLOĞU ---
if __name__ == "__main__": 
    # 1. TEST: VERİLERİ ÇEKME

    print("\n🚀 Müşteri verileri çekiliyor...")
    musteriler = contact_service.get_all()

    if musteriler:
        for m in musteriler:
            print(f"✅ Kayıtlı: {m.full_name} | Kategori: {m.category.value}")
    else:
        print("⚠️ Veritabanında hiç müşteri bulunamadı.")
    
    print("\n🔍 Müşteri Filtreleme Deneyi...")
    mulk_sahipleri = contact_service.get_filtered("category", ContactCategory.MULK_SAHIBI.value)

    if mulk_sahipleri:
        print(f"✅ Toplam {len(mulk_sahipleri)} adet Mülk Sahibi bulundu:")
        for m in mulk_sahipleri:
            print(f"👤 İsim: {m.full_name} | Telefon: {m.phone}")
    else:
        print("⚠️ Kriterlere uygun kimse bulunamadı.")