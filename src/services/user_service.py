from typing import Optional, List, Dict, Any
from src.core.database import db
from src.models.user import User, UserRole

class UserService:
    """
    Personel ve Profil işlemlerini yöneten servis katmanı.
    """
    @staticmethod
    def get_profile(user_id: str) -> Optional[User]:
        """
        Supabase UUID üzerinden kullanıcının tüm profil detaylarını getirir.
        """
        response = db.get_user_profile(user_id)
        if response and response.data:
            return User.from_dict(response.data)
        return None

    @staticmethod
    def sync_profile(user: User) -> bool:
        """
        Kullanıcı bilgilerini veritabanı ile senkronize eder (Ekleme veya Güncelleme).
        Özellikle kayıt sonrası ilk profil oluşumu için kritiktir.
        """
        profile_data = user.to_dict()
        # ID bilgisini de ekliyoruz ki Upsert işlemi hangi satırı etkileyeceğini bilsin
        profile_data["id"] = user.id
        
        response = db.upsert_user_profile(profile_data)
        return response is not None

    @staticmethod
    def get_team_members() -> List[User]:
        """
        Ofisteki tüm ekibi (Admin, Agent, Viewer) listeler.
        Emlak ofisindeki hiyerarşiyi görmek için kullanılır.
        """
        # created_at'e göre sıralı getiriyoruz (DatabaseManager'daki default order)
        response = db.get_data("profiles")
        if response and response.data:
            return [User.from_dict(item) for item in response.data]
        return []

    @staticmethod
    def update_role(user_id: str, new_role: UserRole) -> bool:
        """
        Bir personelin yetkisini değiştirir. 
        Sadece ADMIN yetkisi olanların çağırabileceği bir fonksiyondur.
        """
        data = {"role": new_role.value}
        response = db.update_data("profiles", data, user_id)
        return response is not None

    @staticmethod
    def deactivate_account(user_id: str) -> bool:
        """
        Personel işten ayrıldığında hesabını silmek yerine pasife alırız.
        Bu sayede geçmiş ilan ve randevu kayıtları bozulmaz.
        """
        data = {"is_active": False}
        response = db.update_data("profiles", data, user_id)
        return response is not None

# Singleton Pattern
user_service = UserService()