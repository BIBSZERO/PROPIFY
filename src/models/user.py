from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, Dict

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
    profile_pic_url: Optional[str] = None
    created_at: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        """
        Supabase'den gelen veriyi User nesnesine dönüştürür.
        Mypy tip hatalarını engellemek için tip dönüşümleri garanti altına alınmıştır.
        """
        return User(
            id=str(data.get("id", "")),
            email=str(data.get("email", "")),
            full_name=str(data.get("full_name", "")),
            phone=str(data.get("phone")) if data.get("phone") else None,
            # Role verisi enum içinde yoksa varsayılan olarak AGENT atar
            role=UserRole(data.get("role", "agent")),
            is_active=bool(data.get("is_active", True)),
            profile_pic_url=str(data.get("profile_pic_url")) if data.get("profile_pic_url") else None,
            created_at=str(data.get("created_at")) if data.get("created_at") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        User nesnesini veritabanına gönderilecek sözlük (dict) formatına çevirir.
        """
        return {
            "full_name": self.full_name,
            "phone": self.phone,
            "role": self.role.value,
            "is_active": self.is_active,
            "profile_pic_url": self.profile_pic_url,
            # created_at genellikle DB tarafında otomatik oluştuğu için buraya eklemiyoruz
        }