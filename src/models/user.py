from enum import Enum
from dataclasses import dataclass
from typing import Optional

class UserRole(Enum):
    ADMIN = "admin"
    AGENT = "agent"
    VIEWER = "viewer"

@dataclass
class User:
    id: str
    email: str
    full_name: str = ""
    phone: Optional[str] = None
    role: UserRole = UserRole.AGENT
    is_active: bool = True
    profile_pic_url: Optional[str] = None # Profil fotoğrafı için
    created_at: Optional[str] = None    # İşe başlama/kayıt tarihi

    @staticmethod
    def from_dict(data: dict):
        """Supabase'den gelen sözlüğü User nesnesine dönüştürür."""
        return User(
            id=data.get("id"),
            email=data.get("email", ""),
            full_name=data.get("full_name", ""),
            phone=data.get("phone"),
            # Enum dönüşümü yaparken hata almamak için güvenli dönüşüm
            role=UserRole(data.get("role", "agent")),
            is_active=data.get("is_active", True),
            profile_pic_url=data.get("profile_pic_url"),
            created_at=data.get("created_at")
        )

    def to_dict(self):
        """User nesnesini Supabase'e kaydedilecek sözlük formatına çevirir."""
        return {
            "full_name": self.full_name,
            "phone": self.phone,
            "role": self.role.value, # Enum'ın string değerini alıyoruz
            "is_active": self.is_active,
            "profile_pic_url": self.profile_pic_url
            # created_at genellikle DB tarafından otomatik atanır, o yüzden göndermiyoruz
        }