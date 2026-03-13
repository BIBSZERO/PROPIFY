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

class BuildingAge(Enum):
    ZERO = "0 (Yeni)"
    ONE_FIVE = "1-5 Yıl"
    SIX_TEN = "6-10 Yıl"
    ELEVEN_FIFTEEN = "11-15 Yıl"
    SIXTEEN_TWENTY = "16-20 Yıl"
    OVER_TWENTY = "21 ve Üzeri"

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
    building_age: BuildingAge = BuildingAge.ZERO
    owner_id: Optional[str] = None
    address: Optional[str] = "" # 🚀 HATA DÜZELTME: Varsayılan değer ekledik (None yerine "")
    images: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        # Enum dönüşümlerinde hata almamak için .get() ile gelen değeri kontrol ediyoruz
        b_age_val = data.get("building_age")
        r_count_val = data.get("room_count")

        return Property(
            id=data.get("id"),
            listing_no=data.get("listing_no", ""),
            title=data.get("title", ""),
            # Supabase'deki anahtar isimlerinin to_dict ile uyumlu olduğundan emin ol (type vs property_type)
            property_type=PropertyType(data.get("type", "Daire")),
            status=PropertyStatus(data.get("status", "Aktif")),
            price=float(data.get("price", 0)),
            m2_gross=int(data.get("m2_gross", 0)),
            m2_net=int(data.get("m2_net", 0)),
            # 🚀 GÜVENLİ DÖNÜŞÜM: Eğer veritabanında geçersiz bir string varsa varsayılana döner
            building_age=next((x for x in BuildingAge if x.value == b_age_val), BuildingAge.ZERO),
            room_count=next((x for x in RoomCount if x.value == r_count_val), RoomCount.TWO_ONE),
            owner_id=data.get("owner_id"),
            address=data.get("address", ""),
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
            "building_age": self.building_age.value,
            "room_count": self.room_count.value,
            "owner_id": self.owner_id,
            "address": self.address,
            "images": self.images
        }