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

class RoomCount(Enum):
    STUDIO = "1+0"
    ONE_ONE = "1+1"
    TWO_ONE = "2+1"
    THREE_ONE = "3+1"
    FOUR_ONE = "4+1"
    FOUR_TWO = "4+2"
    FIVE_ONE = "5+1"
    OTHER = "Diğer"

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
    room_count: RoomCount = RoomCount.TWO_ONE
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
            room_count=(data.get("room_count", "2+1")),
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
            "room_count": self.room_count.value,
            "owner_id": self.owner_id,
            "address": self.address,
            # 🚀 Veritabanına gönderilecek görseller
            "images": self.images
        }