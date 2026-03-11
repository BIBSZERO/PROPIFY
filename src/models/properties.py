from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List

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
    listing_no: str = ""
    title: str = ""
    property_type: PropertyType = PropertyType.DAIRE
    status: PropertyStatus = PropertyStatus.AKTIF
    price: float = 0.0
    m2_gross: int = 0
    m2_net: int = 0
    owner_id: Optional[str] = None
    address: Optional[str] = None
    # 📸 Görsel URL'lerini tutacak yeni alanımız
    images: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        return Property(
            id=data.get("id"),
            listing_no=data.get("listing_no", ""),
            title=data.get("title", ""),
            property_type=PropertyType(data.get("type", "Daire")),
            status=PropertyStatus(data.get("status", "Aktif")),
            price=float(data.get("price", 0)),
            m2_gross=int(data.get("m2_gross", 0)),
            m2_net=int(data.get("m2_net", 0)),
            owner_id=data.get("owner_id"),
            address=data.get("address"),
            # 🕵️ Veritabanından gelen images listesini al, yoksa boş liste döndür
            images=data.get("images", [])
        )
    
    def to_dict(self):
        return {
            "listing_no": self.listing_no,
            "title": self.title,
            "type": self.property_type.value,
            "status": self.status.value,
            "price": self.price,
            "m2_gross": self.m2_gross,
            "m2_net": self.m2_net,
            "owner_id": self.owner_id,
            "address": self.address,
            # 🚀 Veritabanına gönderilecek görseller
            "images": self.images
        }