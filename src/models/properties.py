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

class HeatingType(Enum):
    YOK = "Yok"
    SOBA = "Soba"
    DOGALGAZ_SOBA = "Doğalgaz Sobası"
    KOMBI_DOGALGAZ = "Kombi (Doğalgaz)"
    MERKEZI = "Merkezi Sistem"
    MERKEZI_PAY = "Merkezi (Isı Pay Ölçer)"
    YERDEN_ISITMA = "Yerden Isıtma"
    KLIMA = "Klima"
    ISI_POMPASI = "Isı Pompası"

class KitchenType(Enum):
    KAPALI = "Kapalı Mutfak"
    AMERIKAN = "Amerikan Mutfak"

class BalconyStatus(Enum):
    VAR = "Var"
    YOK = "Yok"

class ElevatorStatus(Enum):
    VAR = "Var"
    YOK = "Yok"

class ParkingStatus(Enum):
    YOK = "Yok"
    KAPALI = "Kapalı"
    ACIK = "Açık"
    KAPALI_ACIK = "Kapalı + Açık"

class FurnishedStatus(Enum):
    ESYALI = "Eşyalı"
    ESYASIZ = "Eşyasız"

class OccupationStatus(Enum):
    BOS = "Boş"
    MULK_SAHIBI = "Mülk Sahibi"
    KIRACILI = "Kiracılı"

class InSiteStatus(Enum):
    EVET = "Evet"
    HAYIR = "Hayır"

@dataclass
class Property:
    # 🛠️ Zorunlu olmayan alanlar için varsayılan değerler ve doğru Type Hinting
    id: Optional[str] = None
    listing_no: str = ""
    title: str = ""
    property_type: PropertyType = PropertyType.DAIRE
    status: PropertyStatus = PropertyStatus.AKTIF
    price: float = 0.0
    m2_gross: int = 0
    m2_net: int = 0
    floor_level: str = ""
    total_floors: int = 0
    room_count: RoomCount = RoomCount.TWO_ONE
    building_age: BuildingAge = BuildingAge.ZERO
    heating: HeatingType = HeatingType.YOK
    kitchen_type: KitchenType = KitchenType.KAPALI
    balcony: BalconyStatus = BalconyStatus.VAR
    elevator: ElevatorStatus = ElevatorStatus.YOK
    parking: ParkingStatus = ParkingStatus.YOK
    furnished: FurnishedStatus = FurnishedStatus.ESYASIZ
    occupation: OccupationStatus = OccupationStatus.BOS
    in_site: InSiteStatus = InSiteStatus.HAYIR
    site_name: Optional[str] = "" # 🚀 Düzelttik!
    bath_count: int = 0
    owner_id: Optional[str] = None # 🚀 Düzelttik!
    address: Optional[str] = ""
    images: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        # Enum değerlerini güvenli bir şekilde çekiyoruz
        def get_enum_value(enum_class, key, default):
            val = data.get(key)
            return next((x for x in enum_class if x.value == val), default)

        return Property(
            id=data.get("id"),
            listing_no=data.get("listing_no", ""),
            title=data.get("title", ""),
            # Supabase'de 'type' olarak tutuluyorsa:
            property_type=get_enum_value(PropertyType, "type", PropertyType.DAIRE),
            status=get_enum_value(PropertyStatus, "status", PropertyStatus.AKTIF),
            price=float(data.get("price") or 0),
            m2_gross=int(data.get("m2_gross") or 0),
            m2_net=int(data.get("m2_net") or 0),
            floor_level=str(data.get("floor_level") or ""),
            total_floors=int(data.get("total_floors") or 0),
            room_count=get_enum_value(RoomCount, "room_count", RoomCount.TWO_ONE),
            building_age=get_enum_value(BuildingAge, "building_age", BuildingAge.ZERO),
            heating=get_enum_value(HeatingType, "heating", HeatingType.YOK),
            kitchen_type=get_enum_value(KitchenType, "kitchen_type", KitchenType.KAPALI),
            balcony=get_enum_value(BalconyStatus, "balcony", BalconyStatus.VAR),
            elevator=get_enum_value(ElevatorStatus, "elevator", ElevatorStatus.YOK),
            parking=get_enum_value(ParkingStatus, "parking", ParkingStatus.YOK),
            furnished=get_enum_value(FurnishedStatus, "furnished", FurnishedStatus.ESYASIZ),
            occupation=get_enum_value(OccupationStatus, "occupation", OccupationStatus.BOS),
            in_site=get_enum_value(InSiteStatus, "in_site", InSiteStatus.HAYIR),
            site_name=data.get("site_name", ""),
            bath_count=int(data.get("bath_count") or 0),
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
            "floor_level": self.floor_level,
            "total_floors": self.total_floors,
            "room_count": self.room_count.value,
            "building_age": self.building_age.value,
            "heating": self.heating.value,
            "kitchen_type": self.kitchen_type.value,
            "balcony": self.balcony.value,
            "elevator": self.elevator.value,
            "parking": self.parking.value,
            "furnished": self.furnished.value,
            "occupation": self.occupation.value,
            "in_site": self.in_site.value,
            "site_name": self.site_name,
            "bath_count": self.bath_count,
            "owner_id": self.owner_id,
            "address": self.address,
            "images": self.images
        }