from enum import Enum
from dataclasses import dataclass
from typing import Optional

class PropertyType(Enum):
    DAIRE = "Daire"
    DUKKAN = "Dükkan"
    ARSA = "Arsa"
    VILLA = "Villa"

class PropertyStatus(Enum):
    AKTIF = "Aktif"
    PASIF = "Pasif"
    SATILDI = "Satıldı"
    KIRALANDI = "Kiralandı"

@dataclass
class Property:
    id: Optional[str] = None
    title: str = ""
    property_type: PropertyType = PropertyType.DAIRE
    status: PropertyStatus = PropertyStatus.AKTIF
    price: float = 0.0
    owner_id: Optional[str] = None
    address: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return Property(
            id=data.get("id"),
            title=data.get("title", ""),
            property_type=PropertyType(data.get("type", "Daire")),
            status=PropertyStatus(data.get("status", "Aktif")),
            price=float(data.get("price", 0)),
            owner_id=data.get("owner_id"),
            address=data.get("address")
        )
    
    def to_dict(self):
        return {
            "title": self.title,
            "type": self.property_type.value,
            "status": self.status.value,
            "price": self.price,
            "owner_id": self.owner_id,
            "address": self.address
        }
