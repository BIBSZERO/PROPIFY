from enum import Enum
from dataclasses import dataclass
from typing import Optional

class ContactCategory(Enum):
    POTANSIYEL = "Potansiyel"
    MUSTERI = "Müşteri"
    MULK_SAHIBI = "Mülk Sahibi"
    ESKI_MUSTERI = "Eski Müşteri"

@dataclass
class Contact:
    id: Optional[str] = None
    full_name: str = ""
    phone: Optional[str] = None
    email: Optional[str] = None
    category: ContactCategory = ContactCategory.POTANSIYEL
    notes: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return Contact(
            id=data.get("id"),
            full_name=data.get("full_name", ""),
            phone=data.get("phone"),
            email=data.get("email"),
            category=ContactCategory(data.get("category", "Potansiyel")),
            notes=data.get("notes")
        )

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
            "category": self.category.value, # Veritabanına metin olarak gidiyor
            "notes": self.notes
        }
